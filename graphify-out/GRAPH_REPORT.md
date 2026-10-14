# Graph Report - omnik-wifi-card  (2026-10-14)

## Corpus Check
- 11 files · ~1,422 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 83 nodes · 122 edges · 9 communities (4 shown, 5 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ddf6d469`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _parse_response
- OmnikDataUpdateCoordinator
- manifest.json
- OmnikOptionsFlow
- omnik.py
- Omnik WiFi Card — Home Assistant Integration
- async_setup_entry

## God Nodes (most connected - your core abstractions)
1. `_parse_response()` - 12 edges
2. `OmnikDataUpdateCoordinator` - 9 edges
3. `query_inverter()` - 9 edges
4. `_build_fake_response()` - 7 edges
5. `async_setup_entry()` - 6 edges
6. `OmnikSensorEntity` - 6 edges
7. `Omnik WiFi Card — Home Assistant Integration` - 5 edges
8. `async_setup_entry()` - 4 edges
9. `OmnikOptionsFlow` - 4 edges
10. `async_unload_entry()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `test_parse_energy_today()` --calls--> `_parse_response()`  [EXTRACTED]
  tests/test_omnik.py → custom_components/omnik_wifi_card/omnik.py
- `test_parse_energy_total()` --calls--> `_parse_response()`  [EXTRACTED]
  tests/test_omnik.py → custom_components/omnik_wifi_card/omnik.py
- `test_parse_power()` --calls--> `_parse_response()`  [EXTRACTED]
  tests/test_omnik.py → custom_components/omnik_wifi_card/omnik.py
- `test_parse_temperature()` --calls--> `_parse_response()`  [EXTRACTED]
  tests/test_omnik.py → custom_components/omnik_wifi_card/omnik.py
- `test_parse_voltage_ac()` --calls--> `_parse_response()`  [EXTRACTED]
  tests/test_omnik.py → custom_components/omnik_wifi_card/omnik.py

## Import Cycles
- None detected.

## Communities (9 total, 5 thin omitted)

### Community 1 - "_parse_response"
Cohesion: 0.26
Nodes (8): _parse_response(), _build_fake_response(), test_parse_energy_today(), test_parse_energy_total(), test_parse_power(), test_parse_temperature(), test_parse_voltage_ac(), test_response_too_short()

### Community 2 - "OmnikDataUpdateCoordinator"
Cohesion: 0.19
Nodes (4): OmnikDataUpdateCoordinator, async_setup_entry(), OmnikSensorEntity, OmnikSensorEntityDescription

### Community 3 - "manifest.json"
Cohesion: 0.18
Nodes (10): codeowners, config_flow, dependencies, documentation, domain, iot_class, issue_tracker, name (+2 more)

### Community 6 - "Omnik WiFi Card — Home Assistant Integration"
Cohesion: 0.33
Nodes (5): Configuration, Features, How it works, Installation, Omnik WiFi Card — Home Assistant Integration

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `query_inverter()` connect `omnik.py` to `sensor.py`, `_parse_response`, `OmnikDataUpdateCoordinator`, `OmnikOptionsFlow`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `OmnikDataUpdateCoordinator` (e.g. with `async_setup_entry()` and `OmnikSensorEntity`) actually correct?**
  _`OmnikDataUpdateCoordinator` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `sensor.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14619883040935672 - nodes in this community are weakly interconnected._
- **Why does `_parse_response()` connect `_parse_response` to `omnik.py`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `query_inverter()` (e.g. with `.async_step_user()` and `._async_update_data()`) actually correct?**
  _`query_inverter()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Why does `OmnikDataUpdateCoordinator` connect `OmnikDataUpdateCoordinator` to `sensor.py`, `async_setup_entry`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._