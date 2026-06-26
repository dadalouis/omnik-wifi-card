"""Unit tests for the Omnik protocol parser."""
import struct
import pytest
from custom_components.omnik_wifi_card.omnik import _parse_response


def _build_fake_response(
    power_now=1000,
    energy_today=550,   # 5.50 kWh
    energy_total=12345, # 1234.5 kWh
    temp=250,           # 25.0 °C
    voltage_ac=2300,    # 230.0 V
    current_ac=44,      # 4.4 A
    voltage_dc1=3200,   # 320.0 V
    current_dc1=32,     # 3.2 A
    freq_ac=5000,       # 50.00 Hz
) -> bytes:
    data = bytearray(110)
    struct.pack_into(">H", data, 59, power_now)
    struct.pack_into(">H", data, 69, energy_today)
    struct.pack_into(">I", data, 71, energy_total)
    struct.pack_into(">h", data, 31, temp)
    struct.pack_into(">H", data, 51, voltage_ac)
    struct.pack_into(">H", data, 45, current_ac)
    struct.pack_into(">H", data, 33, voltage_dc1)
    struct.pack_into(">H", data, 39, current_dc1)
    struct.pack_into(">H", data, 57, freq_ac)
    return bytes(data)


def test_parse_power():
    data = _build_fake_response(power_now=1500)
    result = _parse_response(data)
    assert result["power_now"] == 1500


def test_parse_energy_today():
    data = _build_fake_response(energy_today=550)
    result = _parse_response(data)
    assert result["energy_today"] == 5.50


def test_parse_energy_total():
    data = _build_fake_response(energy_total=12345)
    result = _parse_response(data)
    assert result["energy_total"] == 1234.5


def test_parse_temperature():
    data = _build_fake_response(temp=253)
    result = _parse_response(data)
    assert result["temp_inverter"] == 25.3


def test_parse_voltage_ac():
    data = _build_fake_response(voltage_ac=2301)
    result = _parse_response(data)
    assert result["voltage_ac"] == 230.1


def test_response_too_short():
    with pytest.raises(ValueError, match="too short"):
        _parse_response(b"\x00" * 50)
