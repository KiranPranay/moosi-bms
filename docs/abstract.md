# Predictive Thermal Battery Management System for Li-ion Battery Packs

**Muskan Sulathana** · Roll No. 23WH1A0208 · EEE, BVRIT HYDERABAD College of Engineering for Women · Guide: Dr. M. Rupesh, Associate Professor · 27 October 2026

## Abstract

An internal short inside one cell is often named as the cause of lithium-ion battery accidents. In its most common form it starts small: it slowly drains its own cell and makes only a fraction of a watt of heat. A normal battery management system (BMS) cannot see this stage, because it acts only when a voltage, current or temperature crosses a fixed limit. I am building a four-cell pack (4S1P, NCR18650GA) with two layers of protection: an independent hardware BMS, and an ESP32 supervisor that predicts. Five times a second, the ESP32 runs a physical thermal model of every cell with a Kalman filter. It estimates what no sensor can measure: the core temperature, and the abnormal heat, in watts, that the cell's own current cannot explain. It forecasts each cell's temperature 1 and 5 minutes ahead and checks every forecast against the real reading. At rest, it estimates each cell's self-discharge from its voltage. All the evidence becomes one risk level (Normal, Watch, Warning or Trip) that can open separate charge and load relays and latch them.

## Benchmark against existing solutions

| Solution | What it acts on | Earliest warning | Needs before use | Disconnects |
| --- | --- | --- | --- | --- |
| Hardware BMS board (SLCT 4S, ₹239; Layer A of my pack) | Fixed voltage and current limits; no temperature function | None | Nothing | Yes |
| Protection chips (TI BQ76952, NXP MC33772C) | Fixed temperature limits, e.g. 55 °C charging | None found in their datasheets | Settings | BQ76952 only |
| Orion Jr 2 BMS (US$405) | A current limit for every 5 °C | None | Settings | Via a contactor |
| Li-ion Tamer gas sensor (US$596) | Electrolyte vapour, after a cell vents | 6–17 min before runaway (Sandia tests) | Nothing | No, signal only |
| Chen 2024; Sun 2022 (research) | Temperature patterns; outlier cells in a fleet | 23–26 min; 660 s before runaway | Data from cells or a car taken into runaway | No |
| Ojo 2021 (base paper) | Neural-network temperature gap above 0.69 °C | Heating above about 9 °C/min | Training for each cell type | No |
| **My project** (supervisor parts ₹1,263) | Abnormal heat (W), 5-minute forecast check, leak current | 0.4 W of abnormal heat (0.2 W over 5 min), or a 20 mA leak at rest | 11 constants from normal use | Yes, two latched relays |

## Delta X over the base paper (Ojo et al., IEEE TIE, 2021)

| | Base paper (measured) | My project (design target) |
| --- | --- | --- |
| Healthy-cell prediction | Neural network, about 21,000 trained weights; retrained for each cell type and as the cell ages | Physical model and Kalman filter: 11 constants with units, fitted once; no training data |
| Slowest heating caught | About 9 °C/min: a 0.69 °C gap inside its 4.5 s window | Warning at 0.5 °C/min (0.4 W): **18×** slower heating; the 5-minute check catches 0.2 W: **34×** |
| Evidence used | Surface temperature gap only | Core temperature, abnormal heat, leak current (from 20 mA), resistance; thermal and electrical checked by an energy balance |
| Mistaken alarms | 0.5 % of samples: up to 36 an hour at 2 Hz | Each level held 10–30 s; a soft fault needs thermal and electrical evidence to agree |
| Hardware | Jetson TX2 or Raspberry Pi; 45 ms per estimate on its CPU | ₹639 ESP32; about **2,000×** less arithmetic per estimate; under 1 % of the processor |
| Scale and action | One cell on a lab tester; flags only | Four-cell pack, each cell compared with the others; opens latched relays, over an independent BMS |

## Worked example: a soft internal short

Gate 11 copies such a short safely, with a 47 Ω resistor bonded across one cell at rest (about 79 mA and 0.29 W; no fault inside the cell). With the estimated constants, the cell heats at only 0.39 °C/min and settles near 34 °C on a 25 °C day, so the hardware BMS, a 55 °C limit and a raw rate-of-rise warning all miss it. The base paper would see a gap of 0.03 °C against its 0.69 °C threshold. My design sees the cell 1.7 °C hotter than its 5-minute forecast (thermal Watch) and a leak four times the 20 mA level (electrical Watch); both agree on the same cell, and the level becomes **Warning**.

## Two semesters

**Semester 1 (Gates 0–2, no lithium cells):** design, ESP-IDF firmware in C++, calibration of all 10 channels, relay fail-safe tests, and the first version of the model, filter, forecasts and risk levels, tested on synthetic data and a heated dummy. **Semester 2 (Gates 3–12):** cell matching and the welded pack, fitting the model, the safety state machine, Gate 11 validation, the Wi-Fi dashboard and the enclosure.

Within the papers reviewed, none combines abnormal heat in watts, confirmed forecasts, an electrical cross-check and a safe-current forecast on a low-cost controller. My figures are design targets (architecture revision 2.2), to be proven at Gates 9–11; no results are claimed yet. Ratios are my own calculations from the papers' figures, shown in full in the Benchmarking and Delta X document.
