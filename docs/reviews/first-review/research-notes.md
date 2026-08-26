# Research notes — First Review

Gathered 27 Aug 2026. Anything not confirmed from a primary source is marked
**[to verify]** and is *not* stated as fact on a slide.

---

## 1. Thermal runaway in 18650 Li-ion cells

**Primary source.** X. Feng, M. Ouyang, X. Liu, L. Lu, Y. Xia, X. He, "Thermal
runaway mechanism of lithium ion battery for electric vehicles: A review,"
*Energy Storage Materials*, vol. 10, pp. 246–267, 2018.
<https://ui.adsabs.harvard.edu/abs/2018EneSM..10..246F/abstract>

Feng et al. divide runaway into stages bounded by three characteristic
temperatures:

| Symbol | Meaning |
| --- | --- |
| **T1** | onset of detectable **self-heating** |
| **T2** | **triggering** temperature — runaway becomes self-sustaining |
| **T3** | maximum temperature reached |

Reaction sequence and approximate temperature bands (Feng et al.; corroborated
by the Frontiers time-sequence-map paper below):

| Stage | Approx. range | What happens |
| --- | --- | --- |
| SEI decomposition | **80–120 °C** | first exotherm; self-heating begins |
| Anode–electrolyte reaction | 120–160 °C | lithiated anode attacks electrolyte |
| Separator shutdown → melt | **130–165 °C** | pores close, then the separator melts |
| Cathode decomposition, O₂ release | 150–350 °C | drives the runaway to T3 |

The mechanism is a **Heat–Temperature–Reaction (HTR) loop**: heat raises
temperature, temperature starts the next exotherm, that exotherm makes more
heat. Because the loop is positive-feedback, **temperature *rate* rises sharply
before the absolute temperature does** — which is precisely what this project
detects.

Supporting: "Time Sequence Map for Interpreting the Thermal Runaway Mechanism of
Lithium-Ion Batteries With LiNi_xCo_yMn_zO₂ Cathode," *Frontiers in Energy
Research*, vol. 6, art. 126, 2018.
<https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2018.00126/full>

### Standard

**IS 16046 (Part 2): 2018**, identical to **IEC 62133-2:2017** — "Secondary
cells and batteries containing alkaline or other non-acid electrolytes — Safety
requirements for portable sealed secondary cells… — Part 2: Lithium systems."
This is the standard that applies to sealed portable Li-ion cells in India, and
it is mandatory under MeitY's Compulsory Registration Order (BIS CRS). Test
coverage includes overcharge, external short circuit, crush/drop and thermal
cycling. Sources:
<https://www.standphillindia.in/bis-certification-battery-operated-devices-is-16046.php>,
<https://corpbiz.io/learning/bis-for-lithium-ion-batteries/>

> Used on the slides only as "the design targets the abuse conditions IS 16046
> (Part 2) tests for." No claim of compliance or certification is made.

---

## 2. Predictive / rate-of-change based protection

| # | Citation | Method | Limitation | How this project differs |
| --- | --- | --- | --- | --- |
| [1] | Feng et al., *Energy Storage Mater.*, 10:246–267, 2018 | ARC characterisation of the T1/T2/T3 runaway sequence | Laboratory calorimetry; explains mechanism, is not an online detector | Turns the mechanism into a real-time on-board trip |
| [2] | Zhang X., Chen S., Zhu J. *et al.*, "A Critical Review of Thermal Runaway Prediction and Early-Warning Methods for Lithium-Ion Batteries," *Energy Material Advances*, vol. 4, art. 0008, 2023 | Survey of electrochemical, big-data and AI early-warning methods | Most surveyed methods need gas/pressure sensing or off-board computation | Single 8-bit-class threshold test on an ESP32, no extra sensors |
| [3] | Q. Chen, Y. He, N. Fang, G. Yu, "A Combined Data-Driven and Model-Based Algorithm for Accurate Battery Thermal Runaway Warning," *Sensors*, vol. 24, no. 15, art. 4964, 2024 | K-Means + Bernardi model; trips when **dT/dt ≥ 1 °C/s** *and* a voltage/temperature condition holds | Needs training data and a fitted thermal model | Adopts the same **1 °C/s** criterion but computes it directly in firmware, untrained |
| [4] | A. K. M. A. Habib, M. K. Hasan, G. F. Issa, D. Singh, S. Islam, T. M. Ghazal, "Lithium-Ion Battery Management System for Electric Vehicles: Constraints, Challenges, and Recommendations," *Batteries*, vol. 9, no. 3, art. 152, 2023 | Review of BMS functions and open problems | Names thermal runaway as unsolved; proposes no implementation | Implements and bench-tests one specific mitigation |

**Key number carried onto the slides:** Chen et al. (2024) use **dT/dt ≥ 1 °C/s**
as a thermal-runaway criterion, and report ~25 min of advance warning for their
combined method. The 1 °C/s figure is the literature anchor for our trip
threshold. <https://pmc.ncbi.nlm.nih.gov/articles/PMC11314762/>

Not used: <https://www.nature.com/articles/s44172-025-00442-1> (paywalled, could
not verify contents) — **[to verify]**, excluded from the deck.

---

## 3. Components

### ESP32 ADC — from the Espressif ESP-IDF programming guide
<https://docs.espressif.com/projects/esp-idf/en/v4.4/esp32/api-reference/peripherals/adc.html>

- SAR ADC, **12-bit** in single-read mode (0–4095).
- **ADC1 = GPIO32–GPIO39** (8 channels). On common DevKit boards GPIO37/38 are
  not broken out, leaving **6 usable ADC1 pins: 32, 33, 34, 35, 36, 39**.
- **ADC2 is shared with the Wi-Fi radio** — `adc2_get_raw()` can block until
  Wi-Fi stops. Since this project needs Wi-Fi continuously, **ADC2 is unusable**
  and every analogue input must be on ADC1. Stated explicitly on the slide.
- Attenuation ranges: 0 dB 100–950 mV, 2.5 dB 100–1250 mV, 6 dB 150–1750 mV,
  **11 dB 150–2450 mV**. Internal reference varies **1000–1200 mV** chip to
  chip, so calibration APIs are required for absolute accuracy.

> Consequence: 4 cell taps + 4 thermistors = 8 analogue channels but only 6 pins.
> Resolved with a **CD4051B 8:1 analogue multiplexer** on the thermistors.
> Also the reason the deck names an external 16-bit ADC / dedicated cell-monitor
> AFE (e.g. TI BQ769x0 class) as the upgrade path — **[to verify: exact part
> choice not yet fixed]**.

### NTC thermistor
10 kΩ at 25 °C, **β ≈ 3950 K**. β-equation used in firmware:

```
1/T = 1/T0 + (1/β)·ln(R/R0)      T0 = 298.15 K, R0 = 10 kΩ
```

Steinhart–Hart is the three-coefficient refinement; β is sufficient here because
**the trip depends on dT/dt, and a constant calibration offset cancels in a
derivative**. Price confirmed: **₹33 for a pack of 5** (₹6.60 each) at Robu.
<https://robu.in/product/10k-ohm-ntc-thermistor/>

### Current sensing — INA226 chosen over ACS712

| | ACS712 | Shunt + op-amp | **INA226 (chosen)** |
| --- | --- | --- | --- |
| Principle | Hall effect | resistive | resistive + integrated 16-bit ADC |
| Resolution | ~8–10 bits via ESP32 ADC | depends on ADC | **16-bit, on-chip** |
| Uses an ESP32 ADC pin | yes | yes | **no — I²C** |
| Offset drift | significant | low | low |

Decisive reason: ADC1 pins are the scarce resource, and the INA226 reports over
I²C, freeing a channel. Bus voltage range 0–36 V covers a 4S pack (16.8 V max).
**[to verify: exact Robu price — page blocked automated fetch]**

### MOSFET — IRLZ44N class
Logic-level N-channel HEXFET, V_DS 55 V, R_DS(on) ≈ 0.022 Ω at V_GS = 5 V,
I_D 47 A. Comfortable for a 4S pack at ≤ 10 A. **[to verify against the exact
datasheet revision of the part actually purchased]**

### 18650 cells
2500–3000 mAh class (Samsung/LG/Molicel), 3.6–3.7 V nominal, **4.2 V** charge
cut-off, **3.0 V** discharge cut-off. Manufacturer-recommended windows are
typically **0–45 °C charging** and **−20 to 60 °C discharging**, which is why
60 °C is used as the *absolute* backstop while dT/dt provides the early trip.
**[to verify against the datasheet of the specific cells purchased]**

---

## 4. Indicative Indian prices (₹, approx., Aug 2026)

Only the NTC price was confirmed on a live product page; the rest are typical
Indian retail figures and are labelled "approx." on the BOM slide. They must be
replaced with real quotes before the costing is treated as final.

| Item | Approx. ₹ | Source confidence |
| --- | --- | --- |
| NTC 10 kΩ B3950 (each) | 7 | **confirmed** (Robu, pack of 5 @ ₹33) |
| ESP32 DevKit V1 | 450 | typical retail — **[to verify]** |
| 18650 cell 2600 mAh (each) | 250 | typical retail — **[to verify]** |
| INA226 module | 250 | typical retail — **[to verify]** |
| IRLZ44N (each) | 45 | typical retail — **[to verify]** |
| CD4051B | 25 | typical retail — **[to verify]** |
| MP1584EN buck module | 90 | typical retail — **[to verify]** |
| TC4420 gate driver | 120 | typical retail — **[to verify]** |
