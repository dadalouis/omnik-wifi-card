"""Config flow for Omnik WiFi Card."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import callback

from .const import CONF_SERIAL, DEFAULT_PORT, DOMAIN
from .omnik import query_inverter

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_SERIAL): str,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
    }
)


class OmnikConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                await self.hass.async_add_executor_job(
                    query_inverter,
                    user_input[CONF_HOST],
                    user_input[CONF_SERIAL],
                    user_input.get(CONF_PORT, DEFAULT_PORT),
                )
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user_input[CONF_SERIAL])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Omnik {user_input[CONF_SERIAL]}",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OmnikOptionsFlow(config_entry)


class OmnikOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        from homeassistant.const import CONF_SCAN_INTERVAL
        from .const import DEFAULT_SCAN_INTERVAL

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): int,
                }
            ),
        )
