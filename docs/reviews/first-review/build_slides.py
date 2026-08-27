"""Build the First Review presentation.

    python build_slides.py

The slide furniture lives in ../deck_common.py so the zeroth and first review
decks come out looking the same. Diagrams come from diagrams/ — re-run a
diagram script before rebuilding if you change one.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from deck_common import (                                    # noqa: E402
    Presentation, Inches, configure, WARNINGS,
    title_slide, content_slide, image_slide, two_image_slide,
    table_slide, code_slide, closing_slide, SLIDE_W, SLIDE_H,
)

OUT = os.path.join(HERE, "Predictive_BMS_First_Review.pptx")

configure(
    review_label="First Review-2026-27",
    export_date="27-08-2026",
    diagram_dir=os.path.join(HERE, "diagrams"),
    review_heading="Major Project Stage-1 First Review Presentation",
    title_lines=["Predictive Thermal Battery Management System",
                 "for Li-ion Battery Packs"],
)


# ── the deck ────────────────────────────────────────────────────────────
def build():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    n = 1

    title_slide(prs, n, """
Good morning. I am Muskan Sulathana and this is my first review for the major
project. My project is a battery management system for a small lithium-ion
pack. What makes it different is that it watches how fast the cells are heating
up, not just how hot they are. I will take you through the problem, the circuit
I have designed, the firmware plan, and where I am on the schedule.
"""); n += 1

    content_slide(prs, n, "Contents", [
        "Problem statement and objectives",
        "Literature survey",
        "Proposed system, hardware and circuits",
        "Firmware and the predictive algorithm",
        "IoT dashboard, cost and work plan",
    ], """
This is the order I will follow. I will start with the problem I am solving and
why the usual approach falls short. After that I will go through the circuit
design in detail, then the firmware and the algorithm that does the prediction.
I will finish with the cost, what I have finished so far, and the plan for the
rest of the semester.
"""); n += 1

    content_slide(prs, n, "Problem Statement", [
        "A normal small BMS cuts power only when a fixed temperature is crossed, often 60 °C",
        "A cell that is climbing fast at 35 °C is already faulty, but it passes that test",
        "Once a lithium cell starts heating itself, the heat drives more reaction, which makes more heat",
        "A sensor on the outside of a cell always lags what is happening inside it",
        "So a fixed limit reacts late, and it gives no warning at all beforehand",
    ], """
This is the gap I am working on. Almost every small battery protection board
uses one rule: if the temperature goes above a set value, disconnect. The
problem is that the set value tells you nothing until it is reached. A cell that
is heating one degree every second is clearly in trouble even when it is only at
thirty-five degrees, but a fixed limit ignores that completely. On top of that,
the thermistor sits on the outside of the can, so the inside is always hotter
than what I measure. Waiting for an absolute number means acting late.
"""); n += 1

    content_slide(prs, n, "Objectives", [
        "Build a working 4S battery management system for 18650 cells",
        "Measure four cell voltages, the pack current and four cell temperatures",
        "Trip on the rate at which temperature rises, not only on its value",
        "Switch charging and discharging separately, so only the unsafe direction stops",
        "Send every reading over Wi-Fi to a page that opens on a phone or a laptop",
    ], """
These are the five things I want to have working by the end of the project. The
third one is the new part and the reason for the project. The fourth matters
because a pack that is too cold to charge is still perfectly safe to discharge,
so cutting both directions together would be crude. The last one is what makes
it possible to actually see what the board is doing while it runs.
"""); n += 1

    table_slide(prs, n, "Literature Survey",
        ["Ref", "Author and year", "What they did", "What it does not do", "What I do differently"],
        [["[1]", "Feng et al., 2018",
          "Laboratory study of how runaway starts and spreads",
          "Explains the mechanism; it is not a live detector",
          "Turns that mechanism into a trip that runs on the board"],
         ["[2]", "Zhang et al., 2023",
          "Review of ways to predict runaway early",
          "Most methods need gas or pressure sensors, or a server",
          "One threshold test on the ESP32, with no extra sensors"],
         ["[3]", "Chen et al., 2024",
          "Trips when the temperature rise reaches 1 °C per second",
          "Needs training data and a fitted thermal model",
          "Uses the same 1 °C/s figure, computed directly in firmware"],
         ["[4]", "Habib et al., 2023",
          "Review of BMS functions and the problems still open",
          "Lists thermal runaway as unsolved; builds nothing",
          "Builds and bench-tests one specific answer to it"]],
        """
These four papers frame the work. Feng and his co-authors explain what actually
happens inside a cell as it runs away, and that is where the physics comes from.
Zhang's review shows that most early-warning work needs extra hardware or a
server behind it, which a student project cannot use. The Chen paper is the
closest to what I am doing, and it is where my one degree per second threshold
comes from. Habib's review lists thermal runaway as an open problem but does not
build anything, and that is the gap I am filling.
""",
        widths=[0.62, 1.90, 3.05, 3.05, 3.28], size=13.5, row_h=0.86,
        aligns=["c", "c", "l", "l", "l"]); n += 1

    image_slide(prs, n, "Proposed System", "01_system_block.png", """
This is the whole system on one page. The pack feeds the sensing front end,
which reports voltage, current and temperature to the ESP32. The ESP32 runs the
maths and drives two MOSFETs that sit in the pack's negative return. The same
readings go out over Wi-Fi to a dashboard. The one thing worth pointing out is
the note at the bottom: the ESP32's second ADC block cannot be used while Wi-Fi
is running, so every analogue input has to go to the first block.
""",
        bullets=[
            "The pack, the sensing, the controller and the protection sit in one loop",
            "The same readings are used to protect the pack and to feed the dashboard",
        ]); n += 1

    image_slide(prs, n, "Hardware Architecture", "02_hardware_architecture.png", """
This is the same system with the real parts in it. Four cell taps go through
dividers into the first ADC block. Four thermistors go through a CD4051 analogue
multiplexer, because a DevKit board only exposes six usable ADC1 pins and I need
eight channels. Current is measured by an INA226 over I2C, which costs no ADC
pin at all. A buck module makes the 3.3 volt rail, not a linear regulator,
because dropping thirteen volts in a linear part would waste about two watts.
"""); n += 1

    image_slide(prs, n, "Power Path — Single Line Diagram",
                "03_power_path_sld.png", """
This is the power path on its own. The fuse sits in the positive line as the
last-resort protection if the electronics fail completely. Both MOSFETs sit in
the negative return, which is the same arrangement commercial protection boards
use, because it lets both gates be driven against system ground with no charge
pump. The circles are the measurement points: cell voltages at the taps, pack
current across the shunt, and temperature at the cells themselves.
""",
        bullets=[
            "The 15 A fuse is the backstop if the electronics fail completely",
            "Both switches sit in the negative return, so both gates drive against ground",
        ]); n += 1

    two_image_slide(prs, n, "Sensing Circuits",
        "04_voltage_sense_schematic.png", "05_ntc_schematic.png",
        "Cell voltage", "Cell temperature",
        bullets=[
            "Divider ratio 0.128 puts a full 16.8 V pack at 2.15 V — about 4.7 mV per count",
            "Beta equation: 1/T = 1/T₀ + (1/β)·ln(R/R₀), with T₀ = 298.15 K, R₀ = 10 kΩ, β = 3950 K",
        ], note="""
On the left is the divider for a cell tap. All four taps use the same ratio, so
the top tap sets it: the full pack has to land inside the ADC range, which gives
0.128 and about 4.7 millivolts per count once it is referred back to the tap.
That is not precise enough for a production BMS, which is why I have noted an
external 16-bit converter as the upgrade path. On the right is the thermistor
input. The useful thing here is that a fixed calibration error cancels out when
you take a derivative, so the rate trip is far less sensitive to ADC error than
an absolute reading would be.
"""); n += 1

    image_slide(prs, n, "Protection and Balancing",
                "06_cutoff_balancing_schematic.png", """
The two cut-off MOSFETs are wired source to source. That matters because a
single MOSFET has a body diode which would keep conducting in one direction even
when the device is off. With two facing opposite ways, each one blocks a
different direction, so I can stop charging and discharging separately. I chose
the IRLZ44N because it is a logic-level part, so a five volt gate is enough, and
its on-resistance is about 22 milliohms, which at ten amps is only a couple of
watts. On the right, each cell has its own bleed resistor and switch, and an
optocoupler keeps the drive isolated so one ground-referenced pin can switch a
cell sitting several volts up.
""",
        bullets=[
            "IRLZ44N: logic level, 55 V, about 22 mΩ on-resistance at a 5 V gate",
            "The two body diodes face opposite ways, so each direction blocks separately",
        ]); n += 1

    image_slide(prs, n, "Firmware Architecture", "07_firmware_flowchart.png", """
The firmware runs three FreeRTOS tasks. The sensor task reads everything at ten
hertz and filters it. The safety task owns the state machine and is the only
thing allowed to touch the MOSFET pins, so there is no way for the telemetry
code to accidentally switch the pack. The telemetry task builds the JSON message
once a second. On the right is the state machine. The important part is that
leaving the cut-off state needs both a low rate and a low temperature, held for
five seconds, and after three trips in ten minutes it latches until someone
resets it by hand.
"""); n += 1

    code_slide(prs, n, "The Predictive Algorithm",
        ["Temperature is sampled every 100 ms and smoothed before the slope is taken",
         "The slope is an exponential moving average over a one-second window"],
        ["T_filt  = ema(T_raw, alpha = 0.2)",
         "slope   = (T_filt - T_filt_1s_ago) / 1.0",
         "dTdt    = ema(slope, alpha = 0.3)",
         "",
         "if dTdt >= 1.0 or T_filt >= 60.0:",
         "    open_both_mosfets()",
         "    state = CUTOFF",
         "elif dTdt >= 0.5:",
         "    state = WARNING",
         "# leave CUTOFF only when dTdt < 0.2 and T_filt < 40 for 5 s"],
        ["Smoothing comes first: a slope taken from raw counts is mostly noise",
         "A fixed calibration error cancels in a slope, so the trip tolerates ADC drift"],
        """
This is the core of the project in ten lines. The order matters. If you take the
slope of raw readings you mostly measure noise, because differentiating makes
noise worse, so the smoothing has to come first. Then the slope itself gets
smoothed again over a one second window. The threshold of one degree per second
comes from the Chen paper in my literature survey. The sixty degree line is
still there as a backstop, but in a real runaway the rate trip fires well before
it. The last point is the one I like most: because a derivative removes any
constant offset, a calibration error that would ruin an absolute reading has
almost no effect on the rate.
"""); n += 1

    image_slide(prs, n, "Predictive Compared With a Fixed Limit",
                "08_predictive_vs_reactive.png", """
This is a simulated curve, not measured data, and the slide says so. The cell
warms slowly, then self-heating takes over and the temperature climbs
exponentially. The green line is where the rate trip fires: thirty point eight
seconds, with the cell still at only thirty-six degrees. The red line is where a
fixed sixty degree limit would fire, at forty point four seconds. That is almost
ten seconds earlier, and more importantly the pack is twenty-four degrees cooler
when the power is removed. I will replace this with real bench data once the
prototype is running.
""",
        caption="Simulated for illustration. Real measurements will replace this after bench testing."); n += 1

    image_slide(prs, n, "IoT Dashboard", "09_iot_architecture.png", """
The ESP32 joins the local Wi-Fi and serves a small web page itself, so there is
no cloud account and no broker to set up. Once a second the telemetry task
builds the JSON message you can see at the bottom left, and pushes it over a
WebSocket. The browser draws live gauges and a rolling chart from that. The one
message going the other way is the command to clear a latched cut-off, and that
is deliberately the only thing the dashboard is allowed to do.
"""); n += 1

    table_slide(prs, n, "Bill of Materials",
        ["Item", "Qty", "Unit (₹)", "Amount (₹)"],
        [["ESP32-WROOM-32 DevKit V1", "1", "450", "450"],
         ["18650 cells, 2600 mAh", "4", "250", "1000"],
         ["4S holder and nickel strip", "1 set", "270", "270"],
         ["NTC thermistor 10 kΩ B3950", "4", "7", "28"],
         ["INA226 module with shunt", "1", "250", "250"],
         ["IRLZ44N cut-off MOSFETs", "2", "45", "90"],
         ["Balancing parts per cell (P-FET, opto, bleed)", "4 sets", "45", "180"],
         ["CD4051B multiplexer and TC4420 driver", "1 set", "145", "145"],
         ["MP1584EN buck module", "1", "90", "90"],
         ["Passives, fuse, board and wiring", "1 set", "550", "550"],
         ["Total", "", "", "3053"]],
        """
This is the full parts list. It comes to about three thousand rupees, which is
within what I can fund myself. The thermistor price is the only one I have
confirmed on a live product page; the rest are the usual retail figures and I
have marked them as approximate. The cells are the biggest single line, and I
plan to buy them from a seller who will supply matched capacities, because
mismatched cells would make the balancing work much harder later.
""",
        widths=[5.20, 1.10, 1.60, 1.90], size=14, total_row=True,
        aligns=["l", "c", "c", "c"],
        sub="Approximate Indian retail prices, August 2026"); n += 1

    table_slide(prs, n, "Work Completed",
        ["Phase", "Status", "What is done"],
        [["1 · Initial approvals", "Complete", "Synopsis, block diagram and guide approval"],
         ["2 · Procurement", "In progress", "Parts list finalised and priced; ordering next"],
         ["3 · Prototyping", "Not started", "Waiting on parts"],
         ["4 · Core software", "Not started", "Algorithm and state machine designed on paper"],
         ["5 · IoT integration", "Not started", "Message format decided"],
         ["6 · Final polish", "Not started", "—"]],
        """
This is where I actually am. The approvals phase is finished. Procurement is the
live one: the parts list is final and priced, and I am placing the order this
week. Nothing on the bench has been built yet, which is honest, but the design
work for the later phases is not zero either. The algorithm and the state
machine are worked out on paper, and the telemetry message format is decided, so
those phases should move quickly once the hardware exists.
""",
        widths=[3.10, 2.05, 6.00], size=15, row_h=0.72,
        aligns=["l", "c", "l"]); n += 1

    image_slide(prs, n, "Work Plan", "10_gantt.png", """
This is the plan for the rest of the semester, twelve weeks from the end of
August. Procurement takes two weeks. Prototyping overlaps with it slightly
because I can start the sensing board before the cells arrive. The software
phase is the longest at four and a half weeks, and it deliberately overlaps
prototyping, since I can test the reading and filtering code on the bench supply
before the pack is finished. The four dashed lines are the checkpoints I am
holding myself to.
"""); n += 1

    content_slide(prs, n, "Expected Outcomes", [
        "A working 4S BMS that cuts off on temperature rate, demonstrated on the bench",
        "Measured proof that the rate trip fires earlier than a fixed 60 °C limit",
        "A live dashboard showing voltage, current, temperature and rate for every cell",
        "A design that costs about ₹3,000 and uses only parts available in India",
    ], """
These are the four things I expect to be able to show at the end. The second one
is the real test of the project, and I plan to prove it by warming a cell with a
small heater and recording when each trip fires. The last point matters for a
college project: everything on the list can be bought locally, so the work can
actually be repeated by someone else in the department.
"""); n += 1

    content_slide(prs, n, "References", [
        "X. Feng, M. Ouyang, X. Liu, L. Lu, Y. Xia and X. He, “Thermal runaway mechanism of "
        "lithium ion battery for electric vehicles: A review,” Energy Storage Materials, "
        "vol. 10, pp. 246–267, 2018.",
        "X. Zhang, S. Chen, J. Zhu et al., “A critical review of thermal runaway prediction and "
        "early-warning methods for lithium-ion batteries,” Energy Material Advances, "
        "vol. 4, art. 0008, 2023.",
        "Q. Chen, Y. He, N. Fang and G. Yu, “A combined data-driven and model-based algorithm for "
        "accurate battery thermal runaway warning,” Sensors, vol. 24, no. 15, art. 4964, 2024.",
        "A. K. M. A. Habib, M. K. Hasan, G. F. Issa, D. Singh, S. Islam and T. M. Ghazal, "
        "“Lithium-ion battery management system for electric vehicles: Constraints, challenges "
        "and recommendations,” Batteries, vol. 9, no. 3, art. 152, 2023.",
        "IS 16046 (Part 2) : 2018 / IEC 62133-2 : 2017, Secondary cells and batteries containing "
        "alkaline or other non-acid electrolytes — Part 2: Lithium systems.",
    ], """
These are the five sources I have used. The first four are the papers in my
literature survey table, numbered in the same order. The last one is the Indian
standard that covers sealed lithium cells, and it is the standard whose abuse
tests my design is aimed at, although I am not claiming any certification.
""", size=14, numbered=True); n += 1

    closing_slide(prs, n); n += 1

    prs.save(OUT)
    print("saved %s  (%d slides)" % (os.path.basename(OUT), len(prs.slides.__iter__.__self__._sldIdLst)))
    if WARNINGS:
        print("\noverflow warnings:")
        for w in WARNINGS:
            print("   !!", w)
    else:
        print("no overflow warnings")


if __name__ == "__main__":
    build()
