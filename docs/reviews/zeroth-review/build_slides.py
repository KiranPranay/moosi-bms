"""Build the Zeroth Review presentation.

    python build_slides.py

The slide furniture lives in ../deck_common.py so this deck and the first
review come out looking the same. The order of slides follows the way zeroth
reviews are presented in the department: abstract, problem and objective,
implementation outline, literature survey, references.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from deck_common import (                                    # noqa: E402
    Presentation, Inches, configure, WARNINGS,
    title_slide, content_slide, two_section_slide, two_image_slide,
    table_slide, closing_slide, SLIDE_W, SLIDE_H,
)

OUT = os.path.join(HERE, "Predictive_BMS_Zeroth_Review.pptx")

configure(
    review_label="Zeroth Review-2026-27",
    export_date="22-07-2026",
    diagram_dir=os.path.join(HERE, "diagrams"),
    review_heading="Major Project Stage-1 Zeroth Review Presentation",
    title_lines=["Predictive Thermal Battery Management System",
                 "for Li-ion Battery Packs"],
)


def build():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    n = 1

    title_slide(prs, n, """
Good morning. I am Muskan Sulathana. My project is a battery management system
for a small lithium-ion battery pack. The part that is new is that it watches
how quickly the cells are heating up, and switches the pack off on that, instead
of waiting for a fixed temperature. I will explain the problem, what I plan to
build, and the papers I have read so far.
"""); n += 1

    content_slide(prs, n, "Contents", [
        "Abstract",
        "Problem Statement",
        "Objective",
        "Implementation Outline (Block Diagram / Flowchart)",
        "Components",
        "Implementation and Tools",
        "Literature Survey",
        "References",
    ], """
This is the order I will follow. I will start with a short summary of the whole
project, then the problem I am trying to solve and what I want to achieve. After
that I will show the block diagram and the flowchart of how the system will
work, and finish with the papers I have studied.
""", numbered=True, number_format="%d.  "); n += 1

    content_slide(prs, n, "Abstract", [
        "Lithium-ion cells are used in phones, laptops and electric vehicles, and they "
        "can catch fire if they are allowed to get too hot.",
        "Most small protection boards switch the pack off only after the temperature "
        "crosses a fixed value, usually about 60 °C.",
        "By the time a cell reaches that value it is often already heating itself, and "
        "that heat then causes still more heating.",
        "This project builds a battery management system for a four-cell lithium-ion "
        "pack that watches how fast the temperature is rising, not only how high it has reached.",
        "An ESP32 reads the cell voltages, the pack current and four cell temperatures, "
        "switches the pack off through MOSFETs when the rise is too fast, and sends every "
        "reading over Wi-Fi to a simple web dashboard.",
    ], """
This is the whole project in five lines. The first three explain why the usual
approach is not good enough. The fourth is what I am building, and the fifth is
how it is put together. The important word is rising. Every protection board
measures temperature; what I am adding is the rate at which that temperature
changes, because the rate turns dangerous long before the number does.
""", size=17); n += 1

    two_section_slide(prs, n,
        "Problem Statement", [
            "A fixed temperature limit only acts once the cell is already hot, and it "
            "gives no warning before that point.",
            "A cell that is heating quickly at 35 °C is already faulty, but it passes a "
            "60 °C test without any complaint.",
            "The sensor sits on the outside of the cell, so the inside is always hotter "
            "than the reading suggests.",
        ],
        "Objective", [
            "To design and build a battery management system for a 4S lithium-ion pack "
            "that measures cell voltage, pack current and cell temperature, cuts off "
            "charging and discharging based on how fast the temperature is rising, and "
            "publishes every reading live over Wi-Fi.",
        ], """
The problem is that a fixed limit is a late signal. It tells you a cell is hot;
it never tells you a cell is becoming hot. My objective is written as one
sentence on purpose, because the whole project is one idea: measure the rate of
change, and act on it. Everything else in the system exists to make that
measurement possible and to prove it works.
""", size=17); n += 1

    two_image_slide(prs, n, "Implementation Outline",
        "z1_block_diagram.png", "z2_flowchart.png",
        "Block diagram", "Firmware flowchart", """
On the left is the block diagram. The pack feeds the sensing stage, which
reports voltage, current and temperature to the ESP32. The ESP32 decides whether
to keep the MOSFETs closed, and sends the same readings out over Wi-Fi. On the
right is what the software does, in a loop. It reads the sensors, works out how
fast each cell is heating, and if the rise is too fast or any limit is crossed
it cuts off charging and discharging. If everything is fine it sends the
readings to the dashboard and starts again.
"""); n += 1

    table_slide(prs, n, "Components",
        ["Component", "How many", "What it does"],
        [["18650 lithium-ion cells", "4", "The battery pack the system looks after"],
         ["ESP32 board", "1", "Reads the sensors and decides when to cut off"],
         ["NTC thermistors", "4", "Measure the temperature of each cell"],
         ["Resistor dividers", "4", "Bring each cell voltage down to a level the ESP32 can read"],
         ["Current sensor with shunt", "1", "Measures the current going into and out of the pack"],
         ["Analogue multiplexer", "1", "Lets one input pin read all four thermistors"],
         ["MOSFETs", "2", "The switches that stop charging and discharging"],
         ["Bleed resistors", "4", "Drain a little charge from a cell that is fuller than the rest"],
         ["Buck converter", "1", "Makes the 3.3 V supply for the ESP32 from the pack"],
         ["Fuse", "1", "The last protection if the electronics fail"]],
        """
These are the main parts. The pack is four 18650 cells in series. Around it sit
the things that watch it: four thermistors for temperature, a resistor divider
on each cell for voltage, and one current sensor for the whole pack. The
multiplexer is there because the ESP32 does not have enough analogue pins for
four thermistors as well as four cell taps, so one pin reads all four in turn.
The MOSFETs are the switches that actually stop the current. The fuse is there
in case everything else fails. I have priced all of these and the full list with
costs will come in the next review.
""",
        widths=[3.50, 1.50, 6.15], size=15, row_h=0.44,
        aligns=["l", "c", "l"]); n += 1

    table_slide(prs, n, "Implementation and Tools",
        ["Side", "Tool", "What it is used for"],
        [["Hardware", "Siemens NX", "Modelling the enclosure"],
         ["Hardware", "3D printer, PLA+", "Printing the enclosure"],
         ["Hardware", "Soldering station", "Building the board, perfboard first, then a soldered PCB"],
         ["Hardware", "Multimeter, bench supply", "Measuring and testing the circuit"],
         ["Software", "ESP-IDF", "The framework the firmware is built on"],
         ["Software", "C++", "The language the firmware is written in"],
         ["Software", "FreeRTOS", "Running the sensor, safety and telemetry tasks"],
         ["Software", "HTML, CSS, JavaScript", "The dashboard page in the browser"],
         ["Software", "Git and GitHub", "Keeping the code and the documents"]],
        """
This project is not one or the other. There is a circuit to build and there is
firmware to write for it, and neither works without the other. The hardware side
is the pack, the sensing, the protection MOSFETs and the enclosure. The software
side is the firmware on the ESP32 and the dashboard page. The firmware is
written in C++ on ESP-IDF, which is the framework Espressif supply for the
ESP32, and it uses FreeRTOS underneath to keep the sensor, safety and telemetry
work in separate tasks.
""",
        widths=[1.90, 3.20, 6.10], size=15, row_h=0.46,
        aligns=["c", "l", "l"],
        statement="This project has a hardware part and a software part. Both are built here."); n += 1

    table_slide(prs, n, "Literature Survey",
        ["References", "Summary of the work"],
        [["[1]", "How thermal runaway starts inside a lithium-ion cell, and the "
                 "temperature at which each stage begins."],
         ["[2]", "A review of the ways thermal runaway can be predicted early, and "
                 "what each method needs in order to work."],
         ["[3]", "A warning method that acts when the temperature rise reaches "
                 "1 °C per second."],
         ["[4]", "A review of what a battery management system does, and which "
                 "problems in it are still open."],
         ["[5]", "The Indian safety standard for sealed lithium cells, and the abuse "
                 "tests it lays down."]],
        """
These five sources shaped the project. The first explains the physics: the heat
inside a cell feeds more reaction, which makes more heat, so the temperature
curve bends upward sharply. The second and fourth show that early warning is a
known open problem. The third is the closest work to mine and is where the one
degree per second figure comes from. The last is the standard my design is aimed
at, although I am not claiming certification.
""",
        widths=[1.60, 9.60], size=16, row_h=0.78, aligns=["c", "l"]); n += 1

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
These are the five sources, numbered in the same order as the survey table on
the previous slide. The first four are papers and reviews. The fifth is the
Indian standard for sealed lithium cells, which sets out the abuse tests a pack
of this kind is expected to survive.
""", size=14, numbered=True); n += 1

    closing_slide(prs, n); n += 1

    prs.save(OUT)
    print("saved %s  (%d slides)" % (os.path.basename(OUT), len(prs.slides._sldIdLst)))
    if WARNINGS:
        print("\noverflow warnings:")
        for w in WARNINGS:
            print("   !!", w)
    else:
        print("no overflow warnings")


if __name__ == "__main__":
    build()
