# Benchmarking and Delta X

**Muskan Sulathana** · Roll No. 23WH1A0208 · Guide: Dr. M. Rupesh, Associate Professor, EEE Department
Predictive Thermal Battery Management System for Li-ion Battery Packs · 27 October 2026

This document compares my project with the battery protection that exists today, in products and in research papers. It then sets out exactly what my project adds to the base paper, Ojo et al. (IEEE TIE, 2021). That difference is the Delta X.

Numbers for other work are taken from their datasheets and papers, which are listed under Sources at the end. Numbers for my project are design targets from the architecture document, revision 2.2. They are not results. The firmware is not written yet, and each target is measured at a named test gate in semester 2. Where a number is my own calculation, the working is shown next to it.

## 1. What the system does, beyond sensing

Sensing is only the first step. Everything after it is estimation, prediction and control, and it runs on the ESP32 five times a second.

| Step | What happens | What comes out |
| --- | --- | --- |
| Measure | Four cell voltages, the pack current, four cell temperatures and the air temperature | 10 readings, 5 times a second |
| Model | A thermal model of every cell, with a core and a surface | What a healthy cell should be doing |
| Estimate | A Kalman filter for each cell compares the model with the readings | Core temperature (°C) and abnormal heat (W) |
| Forecast and confirm | The model is run forward 1 and 5 minutes, and each forecast is checked when its time comes | Forecast temperature (°C) and a record of forecast error (°C RMS) |
| Cross-check | Self-discharge from voltage drift at rest, resistance from every load step, and an energy balance between the two kinds of evidence | Leak current (mA), resistance (mΩ), agree or not |
| Decide | A fixed rule table combines all the evidence | Normal, Watch, Warning or Trip, with the reason |
| Act | Separate charge and load relays, latched, and an alarm | The pack is disconnected before a fixed limit is reached |

Under all of this, an independent hardware BMS keeps its own voltage and current limits, so the cells stay protected even if the ESP32 fails.

## 2. Benchmark against commercial protection

I compared six products, from the board in my own pack to an industrial gas detector. Values are from their datasheets, manuals and maker pages, read on 27 October 2026. Prices are single-unit prices on that date.

<div markdown="1" class="breakable wide">

| Product | What it is | How it handles temperature | Early warning before a limit | Disconnects the pack | Price |
| --- | --- | --- | --- | --- | --- |
| SLCT 4S 20 A board (Layer A of my pack) | Fixed-limit protection board | No temperature function in its listing or datasheet. Over-charge at 4.25 V, over-discharge at 2.7 V (closest available datasheet) | None | Yes, on its own | ₹239 |
| TI BQ76952 | Protection chip, 3–16 cells, up to 9 thermistors | Fixed limits set in 1 °C steps with a 0–255 s delay; defaults 55 °C charging, 60 °C discharging | None found in the 87-page datasheet or the 207-page reference manual | Yes, drives the cut-off MOSFETs | US$4.40 (chip only) |
| ADI LTC6811-1 | Measurement chip, 12 cells, ±1.2 mV | Reads 5 temperature inputs and reports them; a host processor must decide | None | No | US$29.06 (chip only) |
| NXP MC33772C | Cell controller, 6 cells, 7 temperature inputs | Compares each input with a fixed threshold and raises a flag | None | No | ₹1,018.90 (chip only) |
| Orion Jr 2 BMS | Complete BMS, up to 16 cells, 3 thermistors | A table of allowed current for every 5 °C, falling to zero at the cut-off | None | Through an external contactor | US$405 |
| Honeywell Li-ion Tamer | Gas sensor | Does not use temperature; senses the electrolyte vapour a cell gives off when it vents | 6.3 to 17.3 minutes before thermal runaway in tests at Sandia National Laboratories, but only after a cell has vented | No, signal only | US$596 (sensor only) |
| My project | Two-layer pack with ESP32 supervisor | Model-based abnormal heat, forecasts, safe current and leak estimate on every cell | Designed to warn at 0.4 W of abnormal heat, while the cell is still in its normal range | Yes: hardware BMS, plus separate charge and load relays | ₹1,263 for the supervisor parts |

</div>

**What this shows.**

- **Every product that uses temperature compares it with a fixed limit, or a table of fixed limits.** I found no rate-of-rise, model-based or predictive thermal function in any of them. The measurement chips are very accurate, but they leave every decision to a host processor. The ESP32 in my project is that host, and the predictive layer is the decision logic they leave out.
- **The board in my own pack has no temperature function in its listing or datasheet.** On its own it would not react to a cell that is heating. This is why Layer A protects voltage and current, and Layer B is needed for heat.
- **The gas sensor is the only early warning on the market list, and it works at a later stage.** It needs the cell to vent electrolyte, which in the Sandia tests came 6 to 17 minutes before runaway. My project aims at the stage before that, when a fault is still a fraction of a watt and the cell is only slightly warm. The two do not compete: a large installation could use both.
- **Cost.** The supervisor parts in my costing sheet come to ₹1,263: the ESP32, the ADS1115, the INA226 and shunt, five NTCs, the relay board, the buck regulator and the buzzer. That is about the price of the NXP measurement chip alone, and a small fraction of the price of the gas sensor or the Orion BMS.

These are absence findings from the documents listed under Sources. They are not statements from the makers.

## 3. Benchmark against research methods

These are the published methods closest to my project. Each figure is from the paper itself. The papers test different faults in different ways, so their warning times cannot be ranked against each other directly. The table shows what each one needs and what it does with the answer.

<div markdown="1" class="breakable wide">

| Method | What it watches | What it needs, and what it runs on | Tested on | Main result | Acts? |
| --- | --- | --- | --- | --- | --- |
| Ojo et al., IEEE TIE 2021 (base paper) | Voltage, current, charge level, air and surface temperature, 2 Hz | Training data for each cell type; about 65 min on two GPUs; retraining as the cell ages. Runs on a Jetson TX2 or a Raspberry Pi | 3 single cells; heating pad for 15 s | 88.59 % of fault samples found, 0.5 % false, at a 0.69 °C gap | Detects only |
| Dey et al., IEEE TCST 2019 | Surface temperature, current, voltage | A detailed heat-flow model with about 10 constants; the shape of the fault must be known | One 26650 cell with a heater pad; a short in simulation | Heater found 5 s after it switched on; fault size within ±15 % in 10 s | Detects only |
| Lin et al., IEEE TCST 2013 | Current, surface and air temperature | Two heat capacities assumed; about 3,000 s of varied current to settle. Said to suit "a typical onboard controller" | One 26650 cell, no faults | Core temperature estimated online; resistance growth tracked in simulation | Estimates only |
| Chen et al., Sensors 2024 | 5 temperatures per cell, voltage, current, charge level | A cooling curve, a voltage curve, a reversible-heat test (a 25-hour rest, then temperature steps) at every 10 % of charge, and runaway data to train the alarm | 2 cells and 2 packs, overcharged and heated until runaway | Warned 23–26 minutes before runaway; no false alarms in 4 tests | Detects only |
| Sun et al., IEEE TPEL 2022 | Cell voltages and module temperatures from the cloud, every 10 s | Data from a vehicle that had already gone into thermal runaway, to set the thresholds. Runs on a PC, 0.09 s per run | 3 electric vehicles, 2 real runaways | Temperature fault found 660 s before runaway on the vehicle used for tuning | Detects; sends the car for service |
| Lyu et al., IEEE TIE 2022 | Cell impedance at 30–90 Hz while charging | A purpose-built impedance meter | Overcharge only | Warned 580 s before runaway | Yes: stops charging |
| Naha et al., Sci. Rep. 2020 | Voltage and current over whole charge–discharge cycles | Training cycles with and without a 150–500 Ω resistor across the cell | Phone cells with real internal shorts made by mechanical abuse | More than 97 % of test cycles classified correctly | Detects only |
| **My project** | 4 cell voltages, pack current, 4 cell and 1 air temperature, 5 Hz | 11 constants from normal discharges and cooling curves. Runs on an ESP32 | Gate 11: a heated dummy, recorded traces, and a 47 Ω soft short on the live pack | Targets: warn at 0.4 W; 5-minute forecasts within 0.5 °C RMS | Yes: two relays, latched |

</div>

**What this shows.**

- **The longest warnings come from methods that learned from real runaway data.** Chen trained its alarm on cells taken into runaway, and Sun set its thresholds on a car that went into runaway. A student project cannot destroy cells to learn from, and should not need to. My design needs only normal charging and discharging.
- **Only one method acts, and only for overcharge.** Lyu stops the charge. Every other method raises a flag and leaves the action to something else. My design opens separate charge and load relays.
- **The closest method in spirit is Dey et al.** It also uses a physical model to estimate the size of the fault. It works on a single cell, and it needs a detailed heat-flow model and the shape of the fault in advance. My design uses Lin's simpler two-part model, which fits the ESP32, and adds the forecasts, the electrical cross-check, the cell-to-cell comparison and the relays.
- **My Gate 11 test uses an established method.** Naha et al. copied soft internal shorts the same way, with resistors of 150 to 500 Ω across the cell, and then tested on cells with real shorts. At 3.7 V those resistors draw about 7–25 mA and make 0.03–0.09 W. My 20 mA leak level covers the stronger end of that range (up to about 185 Ω), and the 47 Ω Gate 11 short is stronger again.
- **The most common internal short shows up first as a leak, not as heat.** Zhang et al. (2017) made real internal shorts inside cells. The most common kind, between the cathode and the anode, caused only mild self-discharge, while the most severe kind led to an explosion. This is why my design looks for the leak current as well as the heat.

**Are my estimated constants sensible?** Maleki et al. measured an 18650 cell's specific heat at 0.96–1.04 J/g·°C, so a cell of 43–47 g holds about 41–49 J/°C. My estimate of 45 J/°C sits in that range; I will weigh my own cells to check. A surface-to-air resistance of 30 °C/W, over the cell's surface of about 42 cm², means a heat-transfer coefficient of about 8 W/m²·°C, which is normal for still air. Forgez et al. estimated a cell's core temperature from its surface to within 1.5 °C, which is a fair benchmark for my core estimate. Gate 9 replaces all of these with fitted values.

## 4. Delta X over the base paper

### 4.1 What the base paper does

Ojo et al. trained a neural network to predict the surface temperature a healthy cell should have. The network has two LSTM layers of 50 and 30 units, followed by layers of 5 and 1. Its inputs are the cell's voltage, the square of its current, its state of charge, the air temperature, and its own surface temperature measured 4.5 s earlier. When the measured temperature runs ahead of the prediction by more than a threshold, a thermal fault is flagged. The method was tested on three single cells (two LFP and one NMC) on a laboratory battery tester sampling at 2 Hz. The fault was emulated by a heating pad attached to the cell for 15 s.

| Result reported in the paper | Value |
| --- | --- |
| Temperature estimation error, mean (maximum) | 0.02 °C (0.14 °C) on cell A, 0.02 °C (0.15 °C) on cell B, 0.03 °C (0.15 °C) on cell C, and 0.04 °C (0.28 °C) on cell C after 85 cycles |
| Detection at the best threshold, 0.69 °C | 88.59 % of fault samples flagged; 0.5 % of normal samples flagged by mistake |
| Mistaken flags at other thresholds | 9.14 % at 0.3 °C; none at 1.0 °C or 2.5 °C |
| Training | About 65 minutes on two Nvidia Tesla P100 GPUs |
| Time per estimate | 7.3 ms on a Jetson TX2 GPU, 45.2 ms on its CPU, 44.8 ms on a Raspberry Pi CPU |
| Retraining | Needed for each new battery type, and when the battery changes, for example at 4 % capacity loss |

It is a careful and well-tested method, and it is the structure my project follows: predict what a healthy cell should do, compare, and flag the gap. What I change is how the prediction is made and what is done with it.

### 4.2 Side by side

<div markdown="1" class="breakable">

| | Base paper (measured) | My project (design target) | Change |
| --- | --- | --- | --- |
| How the healthy cell is predicted | Trained neural network, about 21,000 weights | Physical thermal model and Kalman filter: 11 constants for the whole pack, each with a unit (J/°C, °C/W or mΩ) | No training data needed |
| Data needed before use | Charge–discharge training data from each cell type, about 65 min of GPU training, and retraining as the cell ages | A normal 1 A and 2 A discharge and the cooling curves after them (Gate 9) | Fitted once, from normal use |
| What it reports | Surface temperature gap, °C | Core temperature (°C), abnormal heat (W), 1- and 5-minute forecasts (°C), leak current (mA), resistance (mΩ), time to limit (min) and safe current (A) | 1 quantity → 7 |
| Slowest heating it is built to catch | About 9 °C/min (my calculation, 4.3) | Warning at 0.5 °C/min (about 0.4 W); trip at 1.0 °C/min (about 0.75 W) | About 18 times slower at warning |
| A fault too small for any one moment | Not covered: the gap can only build up over 4.5 s | 5-minute forecast check; catches 0.2 W (0.27 °C/min), shown as about 1.3 °C hotter than forecast | About 34 times slower than the base paper's limit |
| Electrical evidence of an internal short | None | Self-discharge at rest, from 20 mA (about 0.07 W of heat, too little to see thermally) | New kind of evidence |
| Mistaken alarms | 0.5 % of samples at 2 Hz: up to 36 flags an hour if each one were acted on | A level must hold for 10–30 s (50–150 samples at 5 Hz); a soft fault needs thermal and electrical evidence to agree; normal use must stay below half the warning level (Gates 9–10) | Designed out by persistence and agreement |
| Hardware | Jetson TX2 or Raspberry Pi | ESP32, ₹639 | Microcontroller |
| Arithmetic per estimate, one cell | About 206,000 multiply-adds (my calculation, 4.5) | About 100 multiply-adds | About 2,000 times less |
| Scale | One cell at a time, on a lab tester with a PC | Four cells in series, each compared with the other three | Pack level |
| What happens on a fault | A flag | Normal → Watch → Warning → Trip; separate charge and load relays open and stay latched | Detection → protection |
| Faulty sensor | Not covered | A lifted, open or shorted sensor is found and both relays open | Fails safe |
| Telling a slow fault from ageing | Named by the authors as future work | Model constants fixed after Gate 9, so a fault cannot be learnt as normal; ageing tracked separately through resistance | Addressed in the design |

</div>

### 4.3 Slow faults: why the base paper misses them

The network is given the measured surface temperature from 9 samples earlier, which is 4.5 s at 2 Hz. The authors chose this delay so that the network has a correct starting point. The cost, which they describe themselves, is that the network soon receives the faulty readings as its starting point, so a slow fault appears as only a minor gap. They define a slow fault as one whose gap takes longer than this delay to cross the threshold, and they note that slow thermal faults are rare. In their conclusion they list telling slow faults apart from ageing as work still to be done.

My own estimate of the slowest heating their threshold catches:

```text
gap needed in 4.5 s       0.69 °C
heating rate needed       0.69 / 4.5 = 0.153 °C/s ≈ 9.2 °C/min
```

For an 18650 cell (heat capacity about 45 J/°C), 9.2 °C/min is about 6.9 W of extra heat. The soft shorts copied by Naha et al. (section 3) make 0.03–0.09 W, roughly 75 to 250 times less. The early stage of an internal short is exactly what the base paper cannot see.

My design does not compare the reading with a 4.5 s guess. The abnormal heat is a quantity the Kalman filter keeps estimating, in watts, for as long as the fault lasts, so a small fault does not fade away. The 5-minute forecast check adds up a small error over 300 s instead of 4.5 s, which is 67 times longer. And because the model's constants are fixed after Gate 9, the model cannot slowly accept a fault as the new normal.

| Heating | Abnormal heat | Base paper: gap in 4.5 s | My project |
| --- | --- | --- | --- |
| 9.2 °C/min | 6.9 W | 0.69 °C, at its threshold | Trip |
| 1.0 °C/min | 0.75 W | 0.08 °C, not flagged | Trip, held 10 s |
| 0.5 °C/min | 0.38 W | 0.04 °C, not flagged | Warning, held 30 s |
| 0.27 °C/min | 0.2 W | 0.02 °C, not flagged | Watch from the 5-minute check |
| about 0.1 °C/min | 0.07 W (a 20 mA leak) | 0.01 °C, not flagged | Watch from the leak estimate, at rest |

### 4.4 Mistaken alarms

At its best threshold the base paper flags 0.5 % of normal samples. At 2 Hz there are 7,200 samples an hour, so that is up to 36 mistaken flags an hour if each one were acted on. Lowering the threshold to 0.3 °C, to catch smaller faults, raises the rate to 9.14 %. The authors name the false-positive rate as something to improve.

No thermal level in my design is set by a single sample. Warning needs the condition to hold for 30 s and a trip for 10 s, which is 150 and 50 samples at 5 Hz. A soft fault reaches Warning only when two independent kinds of evidence, thermal and electrical, point to the same cell. Gates 9 and 10 also set a margin: in normal charging and discharging, the abnormal heat must stay below 0.25 °C/min, half the warning level. The mistaken-alarm rate itself will be measured at those gates.

### 4.5 Computing cost

From the layer sizes in the paper, the network has about 21,000 weights. Each estimate passes a window of 10 time steps through both LSTM layers, which is about 206,000 multiply-adds. The three-state Kalman filter in my design takes about 100 multiply-adds per cell per update. Four cells at 5 Hz, with the forecasts and their checks, come to a few tens of thousands of operations a second at most, well under 1 % of a 240 MHz ESP32 with its floating-point unit.

To be fair to the base paper, a network of this size could perhaps be made to run on a microcontroller with effort. It would still need its training data and its retraining. My design needs neither.

### 4.6 Where the base paper is stronger

- It has results. Its estimation error of 0.02–0.04 °C is measured; mine is a target to be proven. The two are also over different horizons: the base paper predicts 4.5 s ahead, and my 0.5 °C RMS target is for 5 minutes ahead.
- It was tested on three cell types and two chemistries. Mine is designed for one cell type.
- A network can learn effects a simple model leaves out. My model leaves out reversible (entropic) heat, and Gates 9 and 10 check whether it is accurate enough without it.

## 5. Worked example: a soft internal short

Gate 11 copies the early stage of an internal short safely. A 47 Ω resistor is bonded to one cell and connected across it, with the pack at rest near 3.7 V per cell. No fault is made inside the cell. The figures below are calculated with the estimated constants (45 J/°C, 30 °C/W), assuming all of the resistor's heat goes into the cell. Gate 11 measures the real values.

```text
leak current      3.7 V / 47 Ω       ≈ 79 mA
heat              3.7 × 0.079        ≈ 0.29 W
heating rate      0.29 / 45 × 60     ≈ 0.39 °C/min at first
settles at        0.29 × 30          ≈ 8.7 °C above the air
time constant     45 × 30            = 1,350 s ≈ 22 min
after 5 minutes   8.7 × (1 − e^(−300/1350)) ≈ 1.7 °C above the healthy forecast
```

| Method | What it sees | Result |
| --- | --- | --- |
| Hardware BMS | Cell voltage still between 2.7 and 4.25 V; no over-current | Not seen |
| Fixed temperature limit (55 °C) | The cell settles near 34 °C on a 25 °C day | Not seen |
| Raw rate of rise (warning at 0.5 °C/min) | 0.39 °C/min at most | Not seen |
| Base paper | A gap of about 0.03 °C in 4.5 s, against a threshold of 0.69 °C | Not seen |
| My project, thermal | Abnormal heat about 0.29 W, about 0.39 °C/min more than the other cells; 1.7 °C hotter than the 5-minute forecast | Watch |
| My project, electrical | Leak about 79 mA, four times the 20 mA level | Watch |
| My project, together | Both on the same cell; the energy balance agrees (0.29 W thermal, 3.7 V × 79 mA electrical) | **Warning** |

The leak estimate uses a 60-minute window, so Warning is expected within about an hour of rest. The cell is then about 8 °C above the air, about 33 °C on a 25 °C day, below the 40 °C at which Gate 11 removes the resistor.

## 6. How each target will be proven

| Target | Proven at | Pass condition |
| --- | --- | --- |
| Sensing accuracy | Gate 1, no cells | Cell taps within ±20 mV; current within ±2 % or ±20 mA; open and shorted NTCs detected |
| Relays fail safe | Gate 2, no cells | Both relays open on power-off, reset, watchdog and I²C loss |
| Model fitted, forecasts accurate | Gates 9–10 | 5-minute forecast error no more than 0.5 °C RMS; abnormal heat below 0.25 °C/min in normal use; resistance within 15 % of Gate 4 |
| Every warning and trip | Gate 11, on recorded traces, synthetic ramps and a heated dummy cylinder | Warning and trip timing match the architecture; heating with no current is flagged; the heating expected at 5 A is not; a lifted sensor is found |
| Soft internal short | Gate 11, 47 Ω emulation | The right cell is found, thermal and electrical evidence agree, the level reaches Warning |

No test drives a live cell outside its normal range.

## 7. Why this needs two semesters

### Semester 1: Gates 0–2, with no lithium cells

- Design, parts and costing.
- ESP-IDF firmware in C++: drivers for all 10 channels, relays that default to open, and a watchdog.
- Calibration of every channel, and fail-safe tests of both relays.
- The first version of the thermal model, Kalman filter, forecasts and risk levels, tested on synthetic data and a heated dummy.
- The Stage-1 report.

### Semester 2: Gates 3–12

- Cell matching, spot welding and the 4S1P pack.
- Fitting the thermal model on the real pack, and checking the forecasts.
- The safety state machine, sensor faults and the trip log.
- Gate 11 validation, including the emulated soft short.
- The Wi-Fi dashboard, the enclosure, the final report and the presentation.

Each gate has a written pass and stop condition, and no lithium cell is connected until the electronics have passed Gates 0–2.

## Sources

**Papers**

1. O. Ojo, H. Lang, Y. Kim, X. Hu, B. Mu, and X. Lin, "A neural network based method for thermal fault detection in lithium-ion batteries," *IEEE Trans. Ind. Electron.*, vol. 68, no. 5, pp. 4068–4078, May 2021, doi:10.1109/TIE.2020.2984980. The base paper. All of its figures above are from sections II–IV of the paper.
2. X. Lin *et al.*, "Online parameterization of lumped thermal dynamics in cylindrical lithium ion batteries for core temperature estimation and health monitoring," *IEEE Trans. Control Syst. Technol.*, vol. 21, no. 5, pp. 1745–1755, Sep. 2013, doi:10.1109/TCST.2012.2217143.
3. L. Torres-Castro, A. M. Bates, N. B. Johnson, G. Quintana, and L. Gray, "Early detection of Li-ion battery thermal runaway using commercial diagnostic technologies," *J. Electrochem. Soc.*, vol. 171, no. 2, Art. no. 020520, Feb. 2024, doi:10.1149/1945-7111/ad2440. Sandia National Laboratories; the source of the off-gas sensor's 6.3–17.3 minute warning times.
4. S. Dey, H. E. Perez, and S. J. Moura, "Model-based battery thermal fault diagnostics: Algorithms, analysis, and experiments," *IEEE Trans. Control Syst. Technol.*, vol. 27, no. 2, pp. 576–587, Mar. 2019, doi:10.1109/TCST.2017.2776218.
5. Q. Chen, Y. He, N. Fang, and G. Yu, "A combined data-driven and model-based algorithm for accurate battery thermal runaway warning," *Sensors*, vol. 24, no. 15, Art. no. 4964, Jul. 2024, doi:10.3390/s24154964.
6. Z. Sun *et al.*, "An online data-driven fault diagnosis and thermal runaway early warning for electric vehicle batteries," *IEEE Trans. Power Electron.*, vol. 37, no. 10, pp. 12636–12646, Oct. 2022, doi:10.1109/TPEL.2022.3173038.
7. N. Lyu, Y. Jin, R. Xiong, S. Miao, and J. Gao, "Real-time overcharge warning and early thermal runaway prediction of Li-ion battery by online impedance measurement," *IEEE Trans. Ind. Electron.*, vol. 69, no. 2, pp. 1929–1936, Feb. 2022, doi:10.1109/TIE.2021.3062267.
8. A. Naha *et al.*, "Internal short circuit detection in Li-ion batteries using supervised machine learning," *Sci. Rep.*, vol. 10, Art. no. 1301, Jan. 2020, doi:10.1038/s41598-020-58021-7.
9. M. Zhang *et al.*, "Internal short circuit trigger method for lithium-ion battery based on shape memory alloy," *J. Electrochem. Soc.*, vol. 164, no. 13, pp. A3038–A3044, 2017, doi:10.1149/2.0731713jes.
10. H. Maleki, S. Al Hallaj, J. R. Selman, R. B. Dinwiddie, and H. Wang, "Thermal properties of lithium-ion battery and components," *J. Electrochem. Soc.*, vol. 146, no. 3, pp. 947–954, Mar. 1999, doi:10.1149/1.1391704.
11. C. Forgez, D. V. Do, G. Friedrich, M. Morcrette, and C. Delacourt, "Thermal modeling of a cylindrical LiFePO4/graphite lithium-ion battery," *J. Power Sources*, vol. 195, no. 9, pp. 2961–2968, May 2010, doi:10.1016/j.jpowsour.2009.10.105.

**Datasheets and product pages** (read on 27 October 2026)

- SLCT 4S 20 A hardware BMS, Robu listing R266987: <https://robu.in/product/slct-li-ion-nmc-04s-148v-20a-hardware-battery-management-system/>; closest available datasheet (Orange 4S 20 A board): <https://robu.in/wp-content/uploads/2021/08/4S-20A.pdf>
- Texas Instruments BQ76952 datasheet (SLUSE13B) and technical reference manual (SLUUBY2B): <https://www.ti.com/lit/ds/symlink/bq76952.pdf>, <https://www.ti.com/lit/ug/sluuby2b/sluuby2b.pdf>; price from <https://www.ti.com/product/BQ76952>
- Analog Devices LTC6811-1 datasheet, Rev. C: <https://www.analog.com/media/en/technical-documentation/data-sheets/LTC6811-1-6811-2.pdf>; price from DigiKey, part LTC6811HG-1#PBF
- NXP MC33772C datasheet, Rev. 4.1: <https://www.nxp.com/docs/en/data-sheet/MC33772C-DS.pdf>; price from element14 India, part MC33772CTA1AE
- Orion Jr 2 BMS specifications and Orion BMS 2 operation manual: <https://www.orionbms.com/products/orion-jr-2-bms/>, <https://www.orionbms.com/manuals/pdf/orionbms2_operational_manual.pdf>
- Honeywell Li-ion Tamer: <https://buildings.honeywell.com/us/en/brands/our-brands/li-ion-tamer>; sensor price from FireAlarm.com, part LT-SEN-M3
- Espressif ESP32 datasheet, v5.3: <https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf>

**Project documents:** the architecture and technical specification, revision 2.2 (section 9, the predictive thermal layer), the safe build and validation sequence (Gates 0–12), and the costing sheet, all on the project site.
