"""
ui_gradio.py — Gradio UI montada sobre FastAPI.

Corre en el mismo proceso que la API, así que habla directo con los
singletons (ChatChannel, DeviceManager, CKMMonitor) en vez de hacer
llamadas HTTP a sí misma.
"""

from __future__ import annotations

import gradio as gr

from iap_chatroom.channel import ChatChannel
from iap_chatroom.ckm_monitor import CKMMonitor
from iap_chatroom.device_manager import DeviceManager

DEVICE_ID = "device_c_human"
DEVICE_TYPE = "HUMAN"

channel = ChatChannel()
device_manager = DeviceManager()
ckm_monitor = CKMMonitor()

_ROLE_BY_DEVICE_TYPE = {"HUMAN": "user", "AI": "assistant"}


def _history_as_messages() -> list[dict]:
    return [
        {
            "role": _ROLE_BY_DEVICE_TYPE.get(m.device_type, "user"),
            "content": f"[{m.device_id}] {m.text}",
        }
        for m in channel.get_history()
    ]


async def _send(text: str, history: list[dict]):
    if not text or not text.strip():
        return _history_as_messages(), ""

    if device_manager.get(DEVICE_ID) is None:
        device_manager.register(DEVICE_ID, DEVICE_TYPE)

    await channel.publish(DEVICE_ID, DEVICE_TYPE, text)
    return _history_as_messages(), ""


def _refresh_state() -> dict:
    return ckm_monitor.get_state()


def _refresh_firma() -> dict:
    firma = ckm_monitor.get_firma()
    if firma is None:
        return {"status": "corpus insuficiente — aun no hay firma"}
    return firma


def build_gradio_app() -> gr.Blocks:
    with gr.Blocks(title="IAP Chatroom — CKM Monitor") as demo:
        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    label="Chat Grupal",
                    value=_history_as_messages(),
                )
                msg = gr.Textbox(
                    placeholder="Mensaje como Device C (Human)...",
                    show_label=False,
                )
                send_btn = gr.Button("Enviar")
                gr.Markdown(f"Device ID: `{DEVICE_ID}`")

            with gr.Column(scale=1):
                state_json = gr.JSON(
                    label="Estado CKM", value=_refresh_state()
                )
                firma_json = gr.JSON(label="Firma CKM")
                firma_btn = gr.Button("Actualizar Firma")

        send_btn.click(_send, inputs=[msg, chatbot], outputs=[chatbot, msg])
        msg.submit(_send, inputs=[msg, chatbot], outputs=[chatbot, msg])
        firma_btn.click(_refresh_firma, outputs=firma_json)

        timer = gr.Timer(value=3)
        timer.tick(_refresh_state, outputs=state_json)
        timer.tick(_history_as_messages, outputs=chatbot)

    return demo
