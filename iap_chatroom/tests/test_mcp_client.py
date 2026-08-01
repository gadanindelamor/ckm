"""
test_mcp_client.py — verificacion directa del MCP server de IAP Chatroom.

No es un test pytest: es un script que se corre con el servidor levantado
( pythoniap_chatroom/server.py) y ejercita las 6 tools contra el endpoint
/mcp real.

Uso:
    python iap_chatroom/test_mcp_client.py
"""

from __future__ import annotations

import asyncio

from fastmcp import Client

MCP_URL = "http://localhost:7860/mcp"


async def test() -> None:
    async with Client(MCP_URL) as c:
        r1 = await c.call_tool(
            "join_channel", {"device_id": "test_agent", "device_type": "AI"}
        )
        assert r1.data["ok"]

        r2 = await c.call_tool(
            "send_message",
            {"device_id": "test_agent", "text": "Hola desde MCP test"},
        )
        assert r2.data["corpus_size"] >= 1

        r3 = await c.call_tool("get_messages", {})
        assert any(m["device_id"] == "test_agent" for m in r3.data)

        r4 = await c.call_tool("get_monitor_state", {})
        assert "D_ckm" in r4.data and "corpus_status" in r4.data

        await c.call_tool("get_firma", {})
        # puede ser None si corpus < min_texts — ok igual

        r6 = await c.call_tool("leave_channel", {"device_id": "test_agent"})
        assert r6.data["ok"]

        print("6/6 OK")


if __name__ == "__main__":
    asyncio.run(test())
