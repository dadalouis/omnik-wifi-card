"""Low-level communication with the Omnik WiFi card."""
from __future__ import annotations

import socket
import struct
import logging

_LOGGER = logging.getLogger(__name__)

# The WiFi card listens for this magic probe and responds with inverter data.
_PROBE_HEADER = b"\x68\x02\x40\x30"

# Response offsets (little-endian unless noted)
_OFF_POWER_NOW = 59      # uint16, W
_OFF_ENERGY_TODAY = 69   # uint16, 0.01 kWh units
_OFF_ENERGY_TOTAL = 71   # uint32, 0.1 kWh units
_OFF_TEMP = 31           # int16, 0.1 °C
_OFF_VOLTAGE_AC = 51     # uint16, 0.1 V
_OFF_CURRENT_AC = 45     # uint16, 0.1 A
_OFF_VOLTAGE_DC1 = 33    # uint16, 0.1 V
_OFF_CURRENT_DC1 = 39    # uint16, 0.1 A
_OFF_FREQ_AC = 57        # uint16, 0.01 Hz


def _build_request(serial: str) -> bytes:
    serial_bytes = serial.encode("ascii")
    payload = _PROBE_HEADER + serial_bytes + b"\x01\x00"
    checksum = sum(payload[1:]) & 0xFF
    return payload + bytes([checksum])


def _parse_response(data: bytes) -> dict:
    if len(data) < 100:
        raise ValueError(f"Response too short: {len(data)} bytes")

    def u16(offset: int) -> int:
        return struct.unpack_from(">H", data, offset)[0]

    def i16(offset: int) -> int:
        return struct.unpack_from(">h", data, offset)[0]

    def u32(offset: int) -> int:
        return struct.unpack_from(">I", data, offset)[0]

    return {
        "power_now": u16(_OFF_POWER_NOW),
        "energy_today": round(u16(_OFF_ENERGY_TODAY) * 0.01, 2),
        "energy_total": round(u32(_OFF_ENERGY_TOTAL) * 0.1, 1),
        "temp_inverter": round(i16(_OFF_TEMP) * 0.1, 1),
        "voltage_ac": round(u16(_OFF_VOLTAGE_AC) * 0.1, 1),
        "current_ac": round(u16(_OFF_CURRENT_AC) * 0.1, 1),
        "voltage_dc1": round(u16(_OFF_VOLTAGE_DC1) * 0.1, 1),
        "current_dc1": round(u16(_OFF_CURRENT_DC1) * 0.1, 1),
        "frequency_ac": round(u16(_OFF_FREQ_AC) * 0.01, 2),
    }


def query_inverter(host: str, serial: str, port: int = 48899, timeout: float = 5.0) -> dict:
    """Send a probe to the Omnik WiFi card and return parsed sensor data."""
    request = _build_request(serial)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        sock.sendto(request, (host, port))
        data, _ = sock.recvfrom(1024)
    _LOGGER.debug("Received %d bytes from %s", len(data), host)
    return _parse_response(data)
