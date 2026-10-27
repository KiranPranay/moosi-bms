# Project Plan in Two Phases

**Muskan Sulathana** · Roll No. 23WH1A0208 · Guide: Dr. M. Rupesh, Associate Professor, EEE Department
Predictive Thermal Battery Management System for Li-ion Battery Packs · 24 October 2026

The project runs over the two semesters of the major project. Phase 1, in semester 1 (Major Project Stage-1), covers the study, the design and the sensing electronics. Phase 2, in semester 2 (Major Project Stage-2), builds the battery pack, completes the predictive firmware and the dashboard, and tests the whole system.

The split follows the project's safe build sequence, which has twelve gates, each with pass and stop conditions. **Phase 1 uses no lithium cells at all.** Every test that can be done without live cells is finished in phase 1, so phase 2 starts from electronics that are already calibrated and proven to fail safe.

## How the system predicts

The sensors are only the inputs. Five times a second, the ESP32 runs a thermal model of every cell, with a core and a surface, and a Kalman filter that works out what the sensors cannot measure directly. Every output has a physical unit, so each decision can be checked by hand.

<div markdown="1" class="breakable">

| What it predicts or estimates | How it does it | Why it matters |
| --- | --- | --- |
| **Core temperature** of each cell | The Kalman filter estimates it from the surface reading and the current | The core runs hotter than the surface, which is all a sensor can touch |
| **Abnormal heat**, in watts | The part of a cell's heating that its current cannot explain | Normal heating under load is not flagged; a cell heating with little or no current, which is how an internal short starts, is |
| **Temperature 1 and 5 minutes ahead**, then confirmed | Every 10 s it forecasts each cell's temperature; when that time arrives it compares the real reading with the forecast | Within 0.5 °C, the cell is confirmed normal; well above it means a fault too small to see at any one moment. The running record of forecast errors proves, in numbers, that the predictions work |
| **A cell out of step** with the others | The four cells carry the same current, so their abnormal heat should match | Flags one bad cell while every value is still normal |
| **Self-discharge at rest**, in mA | How fast one cell's voltage falls compared with the other three | A soft internal short drains its cell long before it makes enough heat to measure |
| **Internal resistance** of each cell | Voltage change divided by current change at every load step | Rising resistance shows ageing, a weak weld or a cell heating more than it should |
| **Settling temperature and time to limit** | Runs the model forward at the present current | Says either "this load is safe indefinitely" or "the limit is reached in 12 minutes" |
| **Safe continuous current** | The largest current that keeps every cell below its limit | Turns the prediction into an operating limit the user can see |
| **Self-acceleration** | Whether the abnormal heat grows as the cell gets hotter | Heat that feeds itself is how thermal runaway begins, so it trips at once |

</div>

All of this feeds one **risk level** for each cell: Normal, Watch, Warning or Trip, shown on the dashboard with its reason. A soft fault raises the alarm when **two independent kinds of evidence agree** on the same cell: a thermal sign, such as abnormal heat or a forecast that came out too low, and an electrical sign, its self-discharge. A short inside a cell turns its leak current into heat, so the two can also be checked against each other by an energy balance. A clear fault trips on its own.

**What is new compared with the base paper.** Ojo et al. (IEEE TIE, 2021) predict the surface temperature with a trained neural network and flag the gap. This project:

- estimates the abnormal heat itself, in watts, and the core temperature, with a physical model that needs no training data;
- predicts each cell's temperature minutes ahead and then confirms every prediction against the real reading;
- cross-checks thermal and electrical evidence of the same internal short by an energy balance;
- forecasts a safe current, not only a time to limit;
- runs on a ₹639 ESP32, using well under 1 % of its processor.

Within the ten papers reviewed, none combines these on a low-cost controller. The full method is section 9 of the architecture document, revision 2.2.

## At a glance

| | Phase 1 — Semester 1 | Phase 2 — Semester 2 |
| --- | --- | --- |
| Focus | Study, design and sensing electronics | Battery pack, predictive firmware, dashboard and testing |
| Objectives | 1 and 2, and the sensing part of 3 | The pack part of 3, then 4 and 5 |
| Lithium cells | Not used | Matched, welded and tested under supervision |
| Build gates | Gates 0–2 | Gates 3–12 |
| Ends with | A calibrated, fail-safe sensing rig and the Stage-1 report | A tested prototype in its enclosure, the final report and the presentation |

## Phase 1 — Semester 1 (Major Project Stage-1)

**Goal:** finish the design, buy the parts, and build and calibrate all of the sensing and control electronics on the bench, without connecting a lithium cell.

### Completed so far

| Work | Status | Record |
| --- | --- | --- |
| Synopsis, architecture diagram and guide approval | Done | Project tracker |
| Zeroth review | Done, 22-07-2026 | Zeroth review presentation |
| Literature survey of ten papers, with Ojo et al. (IEEE TIE, 2021) as the base paper | Done | First review, References Explained |
| Two-layer protection design, component selection and the predictive thermal model | Done, revision 2.2 on 24-10-2026 | Architecture and technical specification |
| Bill of materials and costing (₹9,260.19 full replacement value, including the fifth NTC) | Done, updated 24-10-2026 | BOM and costing sheet |
| First review | Done, 29-09-2026 | First review presentation |

### Remaining in semester 1

1. **Procurement.** Buy the protection and mechanical parts and the sensing and control parts, settle the ₹519 of open allowances (sleeve, ADC clamps, charger connector and hardware), and inspect every part on arrival.
2. **Gate 0 — freeze the design.** Check every part against the BOM, confirm the 7.5 A fuse fits its holder, and confirm the charger is 16.8 V CC/CV at no more than 1.5 A.
3. **Firmware foundation.** Set up the ESP-IDF project in C++ with FreeRTOS. Write the drivers for the ADS1115, the INA226 and the five NTC channels (four cells and the air), and relay outputs that default to open, with a watchdog.
4. **Gate 1 — sensing at low voltage, no cells.** Calibrate the four cell-tap dividers against a multimeter from 0 to 16.8 V (target ±20 mV). Calibrate the five NTC channels and check that an open or shorted sensor is detected. Fit the 5 mΩ shunt to the INA226 and calibrate it at ±0.25 A, ±0.5 A and ±1 A (target ±2 % or ±20 mA).
5. **Gate 2 — relay fail-safe.** Show that both relays open on power-off, boot, reset, watchdog timeout and loss of the I2C bus, and that the charge and load outputs switch independently on a 12 V lamp load.
6. **First version of the prediction firmware.** Sample at 5 Hz, reject spikes with a median of 5, smooth with a 10 s low-pass filter, and fit a straight line over the last 30 s to get dT/dt. On top of that, write the predictive layer: the two-state thermal model and Kalman filter, the 1- and 5-minute predict-and-confirm check, the cell-to-cell comparison, the forecasts and the risk levels, using estimated parameters until the real ones are fitted in phase 2. Exercise it all with synthetic temperature ramps and with an NTC on a resistor-heated aluminium block. This is development only; the formal check is Gate 11 in phase 2.
7. **Stage-1 report and end-of-semester review.**

### What phase 1 delivers

- The sensing rig on the bench: ESP32, ADS1115, INA226, five NTCs and the relay board, all calibrated.
- A calibration log for every channel.
- A fail-safe test record for both relays.
- A demonstration of the prediction firmware on a dummy heat source: heating with no current flagged as abnormal heat, a 5-minute forecast that comes out too low, and a time-to-limit forecast.
- The Stage-1 report.

**Phase 1 is complete when** Gates 0–2 have passed with signed records and no lithium cell has been connected.

## Phase 2 — Semester 2 (Major Project Stage-2)

**Goal:** build the 4S1P pack, complete and test the predictive firmware and the dashboard, and hand over a working prototype.

### Work, in order

1. **Gate 3 — BMS harness check.** Check the balance-lead order and polarity with simulated cell voltages before any real cell is connected.
2. **Gate 4 — match the cells.** Measure the four NCR18650GA cells and accept them as one set only if they are within 20 mV resting voltage, 3 % capacity and 10 % DC resistance of the group mean.
3. **Gates 5–7 — build the pack.** Dry-fit the cells in their spacers, qualify the spot weld on spare nickel, then weld the 4S1P pack one link at a time and fit the NTCs, insulation and sleeve.
4. **Gate 8 — first live power-up.** Power up through the fuse with both relays disconnected, and log the pack at rest for 30 minutes.
5. **Safety firmware (Objective 4).** Complete the latched safety state machine with persistence and hysteresis, the sensor plausibility and watchdog faults, and a log of every trip with its cause and readings. The limits are those in the architecture document: for example, charging stops at 4.15 V per cell or 45 °C, and the load stops at 3.10 V per cell, 55 °C or 5.0 A.
6. **Gates 9–10 — controlled discharge and charge, and fitting the model.** Discharge in steps up to 5 A, then charge at no more than 1.5 A, ending the first charge at about 4.10 V per cell. Fit the thermal model from normal 1 A and 2 A discharges and the cooling curves after them. Check that, in normal use, abnormal heat stays near zero and the 5-minute forecasts are accurate to within 0.5 °C RMS. Record each cell's rested voltage at three points during the charge for the self-discharge check. Confirm that each simulated fault opens only the relay it should.
7. **Gate 11 — test the prediction.** Use recorded traces, synthetic ramps and the heated dummy to confirm every warning and trip of the predictive layer: abnormal heat (0.5 °C/min warning, 1.0 °C/min trip), the cell-to-cell comparison, the 5-minute confirmation, the forecasts, self-acceleration and the 2.0 °C/min backstop. Confirm that heating with no current is flagged, that the heating expected at 5 A is not, that a lifted sensor is detected, and that faulty sensors cannot bypass the trip. Then emulate a soft internal short on the live pack, safely and under supervision. A small resistor is bonded to one cell and connected across it, so the cell both self-discharges and warms, within its normal range. Show that the system finds the cell, that the thermal and electrical evidence agree, and that it raises Warning. No fault is ever created inside a cell.
8. **Wi-Fi dashboard (Objective 5).** Show live readings, each cell's core temperature, abnormal heat, 1- and 5-minute forecasts with their confirmations, time to limit, safe current and risk level, and latched faults, over Wi-Fi, then turn Wi-Fi off and confirm that every protection still works.
9. **Gate 12 — enclosure and release.** Solder the permanent board, print the vented PETG enclosure, repeat the rest, discharge and charge tests inside it, and get the guide's sign-off.
10. **Final report, presentation and demonstration.**

### What phase 2 delivers

- The working 4S1P prototype in its enclosure.
- The firmware source, with its version recorded.
- The fitted thermal-model parameters, the prediction-accuracy record, and a test record for every gate, including the emulated soft-short test.
- The Wi-Fi dashboard.
- The final report and presentation.

## How the objectives are split

| Objective | Phase 1 — Semester 1 | Phase 2 — Semester 2 |
| --- | --- | --- |
| 1. Study thermal runaway and early-detection methods | Done | — |
| 2. Design the two-layer protection system | Done | — |
| 3. Measure every cell voltage, the pack current, four cell temperatures and the air temperature | Sensing electronics built and calibrated (Gate 1) | Connected to the welded pack and checked live (Gates 3–8) |
| 4. Predict each cell's heating and act on abnormal heat before a fixed limit is reached, with latched trips | Predictive layer written and tested on dummy data | Model fitted on the pack and tested with the safety state machine (Gates 9–11) |
| 5. Wi-Fi dashboard, with safety working without Wi-Fi | — | Dashboard built and tested with Wi-Fi off |

## Safety rules for both phases

- No cell is ever driven into thermal runaway, overcharged or over-discharged to prove a limit. Limits are proven with simulated signals and dummy heat sources.
- Lithium cells are introduced only after the low-voltage electronics have passed their gates.
- The first live power-up and the first charge are never done alone.
- The hardware BMS stays connected as the final backstop, and the firmware never tries to override it.

The dates of the Stage-1 end-of-semester review and the semester 2 reviews will be added when the department announces them.
