# Predictive 4S BMS — Current Build Architecture

**Status:** build authority for the prototype
**Revision:** 2.1 — 17 September 2026
**Supersedes for construction:** the hardware diagrams in the first-review deck. The submitted review files remain historical records and must not be used as wiring instructions.

## 1. Objective and design envelope

Build a **4S1P, 14.4V nominal / 16.8V maximum, 3.3Ah nameplate (about 47.5Wh nominal) NMC lithium-ion prototype** using four existing red-rewrapped cells marked `PW 3300mAh NCR18650GA` that:

- measures each cell voltage, pack current, and four cell-body temperatures;
- calculates filtered temperature rate-of-rise (`dT/dt`) and raises an early warning;
- independently disconnects the charger and the load under software control;
- retains an independent hardware protection and balancing layer if the ESP32, firmware, Wi-Fi, or sensor code fails;
- exposes readings and latched faults on a Wi-Fi dashboard without making Wi-Fi part of the safety chain.

This is a **5A continuous prototype**, not a 20A system. Charging is limited to **1.5A**. Charge and discharge must not be intentionally operated at the same time during prototype tests.

### Existing-cell configuration and evidence

The four cells remain a normal costed BOM item even though this build can reuse stock recovered from earlier battery packs. The dashboard therefore records both facts: procurement state is **available from existing stock**, while quantity, replacement source, product code, purchase link and full replacement value remain visible for any future builder.

The supplied photographs show a representative red rewrapped cell marked `PW`, `3300mAh` and `NCR18650GA`, with signs of earlier pack attachment around the terminals. The user has confirmed the set is serviceable. Photographs and labels do not establish capacity, internal resistance, common history or authenticity, so the four-cell set must still pass Gate 4 matching before welding. Design calculations use the conservative 3.3Ah label capacity; genuine NCR18650GA references list 3.35Ah minimum and about 3.45Ah typical capacity.

## 2. Why the 4S spring holder is removed

The pack is being spot-welded with pure nickel and enclosed in a printed case. A spring holder would duplicate the pack structure and insert eight spring contacts into the current path. Those contacts add resistance, can loosen, and create extra heating that contaminates the thermal measurements.

The welded pack therefore uses:

- flame-retardant 18650 cell spacers above and below the cells;
- fish-paper rings on every positive terminal;
- pure nickel welds;
- fish/barley-paper barriers over exposed conductors;
- a heat-shrink sleeve around the completed insulated pack;
- a vented PETG enclosure with strain-relieved connectors.

The spacers are not electrical contacts; they only establish cell spacing and mechanical alignment.

## 3. Safety architecture

The design has two independent layers.

### Layer A — hardware protection, always active

The 4S hardware BMS is directly connected to `B-`, `B1`, `B2`, `B3`, and `B+`. It provides cell over-voltage, cell under-voltage, short-circuit/over-current protection, and passive balancing. Its common protected output is `P+ / P-`.

The selected board's published values are approximately:

| Function | Hardware threshold |
| --- | ---: |
| Over-charge detect | 4.25V ± 0.05V per cell |
| Balance start | 4.18V |
| Balance current | 30mA ± 5mA |
| Over-discharge detect | 2.7V ± 0.1V per cell |
| Rated continuous discharge | 20A board rating — **not the project limit** |

The **7.5A fuse at B+** protects the prototype wiring and relay path. The BMS's high current rating is only margin; it does not replace the fuse or the 5A firmware/bench limit.

### Layer B — predictive supervisory control

The ESP32 monitors the pack and drives two normally-open relay contacts:

- `K_LOAD`: connects protected `P-` to `LOAD-`;
- `K_CHARGE`: connects protected `P-` to `CHARGE-`.

`LOAD+` and `CHARGE+` are fed from fused, current-monitored `P+`. Separate negative switching lets firmware disable charging while leaving discharge available, or disable discharge while leaving controlled charging available. Both relay inputs have pull-ups so reset, disconnected GPIO, or unpowered control defaults both contacts **open**.

The relays are safety disconnects, not PWM devices. A trip is latched until a deliberate manual reset after the cause has cleared.

## 4. Power path and named nets

```text
4S1P cells → BMS B+/B-/B1/B2/B3 → P+
P+ → 7.5A fuse → 5mΩ shunt → FUSED+
FUSED+ → LOAD+ and CHARGE+
P- → relay K_LOAD NO contact → LOAD-
P- → relay K_CHARGE NO contact → CHARGE-
P+/P- → LM2596 (5.0V) → ESP32 VIN + relay VCC
ESP32 3.3V → ADS1115 + INA226 logic + divider/NTC references
```

Mount the fuse physically next to the pack positive exit. Put the INA226 shunt after the fuse and before the charge/load split. Positive current means discharge; negative current means charge. Because the monitor is common to both branches, do not charge and power the load simultaneously during the prototype phase.

The LM2596 is connected to protected `P+/P-` before the two branch relays. A software relay trip therefore leaves logging alive, while a hardware BMS under-voltage trip also removes controller power and prevents the controller from bypass-draining the pack.

## 5. Cell-voltage measurement

The ADS1115 runs from 3.3V and measures four cumulative tap voltages relative to `B-`:

| ADS1115 channel | Source | Nominal maximum | Computed cell |
| --- | --- | ---: | --- |
| A0 | `B1` | 4.2V | `Vcell1 = Vtap1` |
| A1 | `B2` | 8.4V | `Vcell2 = Vtap2 - Vtap1` |
| A2 | `B3` | 12.6V | `Vcell3 = Vtap3 - Vtap2` |
| A3 | `B+` | 16.8V | `Vcell4 = Vtap4 - Vtap3` |

Each tap uses a nominal **330kΩ high-side / 56kΩ low-side divider**, a 10kΩ series resistor, a 100nF filter capacitor, and low-leakage clamps. The divider ratio is about 0.145; 16.8V becomes about 2.44V. Measure the actual resistance of every divider and store its calibration coefficient. The firmware must reject impossible tap order, negative derived cell voltage, or a jump larger than 100mV between adjacent samples.

High-value dividers reduce permanent imbalance but make contamination and clamp leakage important. Clean flux residue and verify each channel against a calibrated multimeter over the full range before connecting cells.

## 6. Temperature measurement

Use four small 10k B3950 bead NTCs, one at the middle of each cell can. Bond them with electrically insulating, thermally conductive tape; do not place the bead on exposed nickel.

Each NTC forms a divider with a 10kΩ 1% pull-up to 3.3V and a 100nF filter. Connect only to ESP32 **ADC1** pins because ESP32 ADC2 is unavailable while Wi-Fi is active.

| Cell | ESP32 pin |
| --- | --- |
| NTC1 | GPIO32 / ADC1_CH4 |
| NTC2 | GPIO33 / ADC1_CH5 |
| NTC3 | GPIO34 / ADC1_CH6 |
| NTC4 | GPIO35 / ADC1_CH7 |

Calibrate every channel at ambient and at one controlled warm reference point. A disconnected or shorted NTC is a fault, not a valid extreme temperature.

## 7. Digital interfaces and outputs

| Function | ESP32 pin | Notes |
| --- | --- | --- |
| I2C SDA | GPIO21 | ADS1115 and INA226 at 3.3V |
| I2C SCL | GPIO22 | 4.7kΩ pull-ups only if not already fitted |
| Load relay | GPIO25 | Active LOW; 10kΩ pull-up; normally-open power contact |
| Charge relay | GPIO26 | Active LOW; 10kΩ pull-up; normally-open power contact |
| Fault buzzer/LED | GPIO27 | Latched alarm output through suitable driver/resistor |

Verify the exact relay board input state with a bench supply before connecting pack power. If either relay energises during ESP32 reset, add a transistor stage that guarantees de-energised startup.

## 8. Software limits for the prototype

These are conservative supervisory limits, not cell-manufacturer absolutes.

| Condition | Warning | Trip action |
| --- | --- | --- |
| Any cell high | 4.10V | At 4.15V disable charge |
| Any cell low | 3.20V | At 3.10V disable load |
| Charge temperature | 40°C | At 45°C disable charge |
| Discharge temperature | 50°C | At 55°C disable load |
| Temperature spread | 7°C | At 10°C disable both branches |
| Rate of rise | 0.5°C/min for 30s | At 1.0°C/min for 10s disable both branches |
| Pack current | 4.5A | At 5.0A disable load; 1.6A disables charge |
| Sensor plausibility | one invalid sample | persistent 2s fault disables affected branch or both if ambiguous |

Implementation rules:

1. Sample raw sensors at 5Hz and timestamp with a monotonic clock.
2. Apply a median-of-5 rejection stage, then a 10s low-pass estimate for temperature.
3. Calculate `dT/dt` by linear regression over the most recent 30s window; do not differentiate adjacent samples.
4. Require both persistence and hysteresis; do not chatter relays around a threshold.
5. Latch every trip with timestamp, measurements, reason, and relay state.
6. Permit manual reset only when every cell is 3.20–4.10V, every NTC is below 40°C, all sensors are plausible, and the initiating condition has cleared for 60s.
7. Hardware BMS protection remains the final backstop; software must never attempt to defeat it.

The numerical limits must be revisited after sensor calibration and controlled benign tests. Never tune them by provoking thermal runaway in a live cell.

## 9. Failure behaviour

| Failure | Required result |
| --- | --- |
| ESP32 reset or crash | Both software relays open; hardware BMS remains active |
| Wi-Fi loss | Local monitoring and cutoffs continue; telemetry queues or drops safely |
| One NTC open/short | Latch sensor fault; disable both branches until diagnosis |
| ADS1115/INA226 communication loss | Open both relays and latch fault |
| Software relay welded closed | Hardware BMS and fuse remain capable of opening/clearing severe faults; remove pack from service |
| Hardware BMS opens | Controller loses power; pack remains disconnected until BMS recovery conditions are met |
| Reverse/misordered balance harness | Prevent connection during staged voltage check; never hot-plug an unverified harness |

## 10. Physical layout

- Put the fuse at the B+ exit, then shunt, then branch wiring.
- Keep BMS and electronics on insulated standoffs away from cell terminals.
- Route cell taps as a restrained low-current harness; add 1k–10k series resistance near each tap entry.
- Keep INA226 Kelvin pairs together and away from relay/contact current loops.
- Put relay contacts and power wiring on one side of the enclosure; analog sensing on the other.
- Provide vents around cells and electronics. Do not seal the enclosure or claim fire containment.
- Make the electronics cover removable without exposing cell terminals.

## 11. Sources used to validate the redesign

- [Orange/Robu 4S 20A BMS datasheet](https://robu.in/wp-content/uploads/2021/11/4S20A.pdf)
- [Robu 4S BMS wiring guide](https://robu.in/wp-content/uploads/2021/08/4S-20A.pdf)
- [TI INA226 product page](https://www.ti.com/product/INA226)
- [TI ADS1115 datasheet](https://www.ti.com/lit/ds/symlink/ads1115.pdf)
- [Espressif ESP32 ADC documentation](https://docs.espressif.com/projects/esp-idf/en/v4.4/esp32/api-reference/peripherals/adc.html)
- [Panasonic NCR18650GA product specification](https://industrial.panasonic.com/ww/products/pt/lithium-ion/models/NCR18650GA)
- [NCR18650GA replacement listing used for project costing](https://batteryworks.in/products/panasonic-ncr18650ga-3-6v-3300mah-li-ion-battery)
- [SmartElex 5V 10A dual-relay manual](https://robu.in/wp-content/uploads/2025/01/USER-MANUAL-2.pdf)
- [16.8V/1.5A 4S NMC CC/CV charger listing](https://lionbattery.in/shop/shop/power-supply/ac-to-dc-power-supply/16-8v-1-5a-nmc-battery-charger-for-4s-li-ion-pack-cc-cv-charger/)
