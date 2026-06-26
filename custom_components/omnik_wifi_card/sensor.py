"""Sensor platform for Omnik WiFi Card."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import OmnikDataUpdateCoordinator
from .const import CONF_SERIAL, DOMAIN


@dataclass(frozen=True)
class OmnikSensorEntityDescription(SensorEntityDescription):
    pass


SENSORS: tuple[OmnikSensorEntityDescription, ...] = (
    OmnikSensorEntityDescription(
        key="power_now",
        name="Current Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    OmnikSensorEntityDescription(
        key="energy_today",
        name="Energy Today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    OmnikSensorEntityDescription(
        key="energy_total",
        name="Total Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    OmnikSensorEntityDescription(
        key="temp_inverter",
        name="Inverter Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    OmnikSensorEntityDescription(
        key="voltage_ac",
        name="AC Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    OmnikSensorEntityDescription(
        key="current_ac",
        name="AC Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    OmnikSensorEntityDescription(
        key="voltage_dc1",
        name="DC Voltage (String 1)",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    OmnikSensorEntityDescription(
        key="current_dc1",
        name="DC Current (String 1)",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    OmnikSensorEntityDescription(
        key="frequency_ac",
        name="AC Frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: OmnikDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        OmnikSensorEntity(coordinator, entry, description) for description in SENSORS
    )


class OmnikSensorEntity(CoordinatorEntity[OmnikDataUpdateCoordinator], SensorEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: OmnikDataUpdateCoordinator,
        entry: ConfigEntry,
        description: OmnikSensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        serial = entry.data[CONF_SERIAL]
        self._attr_unique_id = f"{serial}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial)},
            name=f"Omnik Inverter {serial}",
            manufacturer="Omnik",
            model="WiFi Card",
        )

    @property
    def native_value(self):
        return self.coordinator.data.get(self.entity_description.key)
