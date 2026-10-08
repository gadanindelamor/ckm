"""
device_manager.py — DeviceManager

Registro de devices (AI y HUMAN) conectados a la chatroom. Singleton.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Dict, List, Literal, Optional


@dataclass
class Device:
    device_id: str
    device_type: Literal["AI", "HUMAN"]
    model: Optional[str]
    provider: Optional[str]
    connected_at: str

    def to_dict(self) -> dict:
        return asdict(self)


class DeviceManager:
    _instance: "DeviceManager | None" = None

    def __new__(cls) -> "DeviceManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._devices: Dict[str, Device] = {}

    def register(
        self,
        device_id: str,
        device_type: str,
        model: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> Device:
        device = Device(
            device_id=device_id,
            device_type=device_type,
            model=model,
            provider=provider,
            connected_at=datetime.now(timezone.utc).isoformat(),
        )
        self._devices[device_id] = device
        return device

    def unregister(self, device_id: str) -> bool:
        return self._devices.pop(device_id, None) is not None

    def get(self, device_id: str) -> Optional[Device]:
        return self._devices.get(device_id)

    def list_active(self) -> List[Device]:
        return list(self._devices.values())

    def count(self) -> int:
        return len(self._devices)
