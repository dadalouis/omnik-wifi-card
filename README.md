# Omnik WiFi Card — Home Assistant Integration

A custom Home Assistant integration for Omnik solar inverters with a WiFi data logger card.

## Features

- Polls the inverter's WiFi card directly over UDP (no cloud dependency)
- Sensors: current power, energy today, total energy, AC/DC voltage & current, frequency, inverter temperature
- Configurable polling interval
- Full UI config flow

## Installation

1. Copy `custom_components/omnik_wifi_card/` into your Home Assistant `custom_components/` directory.
2. Restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration** and search for **Omnik WiFi Card**.
4. Enter your inverter's IP address and serial number (found on the label of the WiFi card).

## Configuration

| Field | Description | Default |
|-------|-------------|---------|
| IP Address | Local IP of the WiFi card | — |
| Serial Number | Inverter serial (used for auth) | — |
| Port | UDP port | 48899 |
| Polling interval | Seconds between updates (options) | 60 |

## How it works

The WiFi card listens on UDP port 48899. This integration sends a probe packet containing the inverter serial number and parses the binary response to extract sensor values.
