"""Build the First Review presentation.

    python build_slides.py

The slides use the same design as the zeroth review, through ../deck_common.py.
The engineering content follows the build authority, docs/current-architecture.md
(revision 2.1). Every reference was checked against Crossref and its abstract
read; see research-notes.md.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from deck_common import (                                    # noqa: E402
    Presentation, Inches, configure, WARNINGS, SLIDE_W, SLIDE_H,
    title_slide, content_slide, two_section_slide, image_slide,
    table_slide, closing_slide,
)

OUT = os.path.join(HERE, "Predictive_BMS_First_Review.pptx")

configure(
    review_label="First Review-2026-27",
    export_date="29-09-2026",
    diagram_dir=os.path.join(HERE, "diagrams"),
    review_heading="Major Project Stage-1 First Review Presentation",
    title_lines=["Predictive Thermal Battery Management System",
                 "for Li-ion Battery Packs"],
)

LIT_HEAD = ["S.No", "Paper Title", "Outcomes", "Limitation / Research Gap"]
LIT_W = [0.80, 3.35, 3.85, 3.85]

LITERATURE = [
    ["[1]", "Thermal runaway mechanism of lithium ion battery for electric vehicles: A review",
     "Reviewed how thermal runaway starts and spreads through a chain of heat-producing "
     "reactions inside the cell.",
     "Explains the mechanism, but does not give an on-board method to detect it early."],
    ["[2]", "Battery management system: An overview of its application in the smart grid "
            "and electric vehicles",
     "Showed that a BMS needs accurate state estimation and ways to protect the battery "
     "from hazardous conditions.",
     "Focuses on state-of-charge and state-of-health estimation, not on early warning "
     "from temperature."],
    ["[3]", "Protection devices in commercial 18650 lithium-ion batteries",
     "Opened four commercial 18650 cells. Only the current interrupt device and the top "
     "vent are fitted in every cell.",
     "These are last-resort devices inside the cell. Pack-level monitoring and early "
     "warning are not covered."],
    ["[4]", "Advanced fault diagnosis for lithium-ion battery systems: A review of fault "
            "mechanisms, fault features, and diagnosis procedures",
     "Reviewed internal battery faults, sensor faults and actuator faults, and how each "
     "one can be diagnosed.",
     "A review only. It does not build or test a low-cost diagnostic system."],
    ["[5]", "A critical review of thermal runaway prediction and early-warning methods for "
            "lithium-ion batteries",
     "Grouped early-warning methods into electrochemistry-based, big-data and artificial "
     "intelligence methods.",
     "The groups it describes rely on detailed models, large data sets or AI training, "
     "not a simple on-board check."],
    ["[6]", "An online data-driven fault diagnosis and thermal runaway early warning for "
            "electric vehicle batteries",
     "Found the cell heading for thermal runaway before it happened, using voltage and "
     "temperature data from real vehicles.",
     "Compares many cells statistically, which suits large EV packs rather than a "
     "four-cell pack."],
    ["[7]", "A neural network based method for thermal fault detection in lithium-ion "
            "batteries",
     "A neural network predicts the cell surface temperature. A large gap between "
     "prediction and reading flags a fault.",
     "Needs neural network training and retraining, which is heavy for a low-cost "
     "microcontroller."],
    ["[8]", "A combined data-driven and model-based algorithm for accurate battery thermal "
            "runaway warning",
     "Combined K-Means clustering with the Bernardi heat equation and warned 25 minutes "
     "before thermal runaway.",
     "Needs training data and fitted parameters. Its 1 °C/s limit confirms runaway; it is "
     "not an early warning."],
    ["[9]", "Online parameterization of lumped thermal dynamics in cylindrical lithium ion "
            "batteries for core temperature estimation and health monitoring",
     "Showed that only the surface temperature can be measured, while the core can be "
     "hotter, and estimated the core.",
     "Needs online parameter identification, and was tested on one 26650 LFP cell, not "
     "an 18650 pack."],
    ["[10]", "Cloud-based battery condition monitoring platform for large-scale lithium-ion "
             "battery energy storage systems using internet-of-things (IoT)",
     "Sent battery module data over IoT links to Google Cloud, where the cell states were "
     "worked out.",
     "Depends on the cloud and a network link. Protection has to keep working when Wi-Fi "
     "is lost."],
]

REFERENCES = [
    "X. Feng, M. Ouyang, X. Liu, L. Lu, Y. Xia, and X. He, “Thermal runaway mechanism of "
    "lithium ion battery for electric vehicles: A review,” Energy Storage Mater., vol. 10, "
    "pp. 246–267, Jan. 2018, doi: 10.1016/j.ensm.2017.05.013.",
    "H. Rahimi-Eichi, U. Ojha, F. Baronti, and M.-Y. Chow, “Battery management system: An "
    "overview of its application in the smart grid and electric vehicles,” IEEE Ind. "
    "Electron. Mag., vol. 7, no. 2, pp. 4–16, Jun. 2013, doi: 10.1109/MIE.2013.2250351.",
    "B. Xu, L. Kong, G. Wen, and M. G. Pecht, “Protection devices in commercial 18650 "
    "lithium-ion batteries,” IEEE Access, vol. 9, pp. 66687–66695, 2021, "
    "doi: 10.1109/ACCESS.2021.3075972.",
    "X. Hu, K. Zhang, K. Liu, X. Lin, S. Dey, and S. Onori, “Advanced fault diagnosis for "
    "lithium-ion battery systems: A review of fault mechanisms, fault features, and "
    "diagnosis procedures,” IEEE Ind. Electron. Mag., vol. 14, no. 3, pp. 65–91, Sep. 2020, "
    "doi: 10.1109/MIE.2020.2964814.",
    "X. Zhang, S. Chen, J. Zhu, and Y. Gao, “A critical review of thermal runaway "
    "prediction and early-warning methods for lithium-ion batteries,” Energy Mater. Adv., "
    "vol. 4, Art. no. 0008, 2023, doi: 10.34133/energymatadv.0008.",
    "Z. Sun et al., “An online data-driven fault diagnosis and thermal runaway early "
    "warning for electric vehicle batteries,” IEEE Trans. Power Electron., vol. 37, no. 10, "
    "pp. 12636–12646, Oct. 2022, doi: 10.1109/TPEL.2022.3173038.",
    "O. Ojo, H. Lang, Y. Kim, X. Hu, B. Mu, and X. Lin, “A neural network based method for "
    "thermal fault detection in lithium-ion batteries,” IEEE Trans. Ind. Electron., "
    "vol. 68, no. 5, pp. 4068–4078, May 2021, doi: 10.1109/TIE.2020.2984980.",
    "Q. Chen, Y. He, N. Fang, and G. Yu, “A combined data-driven and model-based algorithm "
    "for accurate battery thermal runaway warning,” Sensors, vol. 24, no. 15, Art. no. 4964, "
    "Jul. 2024, doi: 10.3390/s24154964.",
    "X. Lin et al., “Online parameterization of lumped thermal dynamics in cylindrical "
    "lithium ion batteries for core temperature estimation and health monitoring,” IEEE "
    "Trans. Control Syst. Technol., vol. 21, no. 5, pp. 1745–1755, Sep. 2013, "
    "doi: 10.1109/TCST.2012.2217143.",
    "A. Adhikaree, T. Kim, J. Vagdoda, A. Ochoa, P. J. Hernandez, and Y. Lee, “Cloud-based "
    "battery condition monitoring platform for large-scale lithium-ion battery energy "
    "storage systems using internet-of-things (IoT),” in Proc. IEEE Energy Convers. Congr. "
    "Expo. (ECCE), 2017, pp. 1004–1009, doi: 10.1109/ECCE.2017.8095896.",
]


def build():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    n = 1

    title_slide(prs, n, """
Good morning. I am Muskan Sulathana, and this is my first review. My project is a
battery management system for a small lithium-ion pack that watches how fast the
cells are warming up, not only how hot they are. Since the zeroth review I have
finished the literature survey and the full design of the system, and I will take you
through both.
"""); n += 1

    content_slide(prs, n, "Contents", [
        "Abstract", "Problem Statement", "Literature Survey",
        "Problem Analysis / Research Gap", "Objectives", "Methodology",
        "Block Diagram / Schematic Diagram", "Hardware and Software Requirements",
        "Individual Contribution", "Project Timeline", "References",
    ], """
This is the order I will follow. I start with a short summary of the project and the
problem, then the papers I studied and the gap they leave. After that I explain the
objectives, the method and the design, and finish with my progress and the plan for
the coming months.
""", size=17, numbered=True, number_format="%d.  "); n += 1

    content_slide(prs, n, "Abstract", [
        "Lithium-ion cells store a lot of energy in a small space. A cell that overheats "
        "can go into thermal runaway, where the heat it makes drives it hotter still.",
        "Most low-cost battery protection boards act only on voltage and current, and treat "
        "temperature, if at all, as one fixed limit that is reached late.",
        "This project builds a predictive thermal battery management system for a 4S1P "
        "pack of NCR18650GA cells, with two protection layers that work independently.",
        "A hardware BMS gives over-voltage, under-voltage, over-current and short-circuit "
        "protection. An ESP32 measures every cell voltage, the pack current and four cell "
        "temperatures, and works out how fast the temperature is rising.",
        "When a reading or the rate of rise crosses a limit, the ESP32 opens the charge or "
        "load relay and latches the fault. Readings are shown on a Wi-Fi dashboard that is "
        "not part of the safety chain.",
    ], """
This is the whole project in five points. The first two explain why the usual approach
is not enough. The third and fourth describe what I am building: a hardware layer that
protects the cells on its own, and an ESP32 layer that watches the temperature trend.
The last point is how it acts: it disconnects only the unsafe direction and keeps the
fault latched until someone checks it.
""", size=17); n += 1

    content_slide(prs, n, "Problem Statement", [
        "Lithium-ion packs are used in more and more devices, and one overheating cell can "
        "lead to fire or explosion through thermal runaway.",
        "Most low-cost protection boards act only on voltage and current. Temperature, if "
        "it is checked at all, is compared with one fixed limit.",
        "A fixed limit acts only once the cell is already hot. A cell that is steadily "
        "heating at a normal temperature passes it with no warning.",
        "When protection depends on a single microcontroller, a firmware crash or a failed "
        "sensor can leave the pack unprotected.",
        "A system is needed that watches the temperature trend, stops only the unsafe "
        "direction of current, and still protects the pack if the software fails.",
    ], """
The problem has three parts. The first is timing: a fixed temperature limit is a late
signal, because it tells you a cell is hot, never that it is becoming hot. The second
is dependence: if everything relies on one controller, one crash removes all
protection. The third is bluntness: most boards cut everything, even when only
charging is unsafe. My design tries to answer all three.
""", size=17); n += 1

    table_slide(prs, n, "Literature Survey", LIT_HEAD, LITERATURE[:5], """
These are the first five papers. The first explains the physics of thermal runaway. The
next three set out what a battery management system should do and what can go wrong,
including the point that the protection inside an 18650 cell is only a last resort. The
fifth is a review of early-warning methods, and it shows that most of them need detailed
models, large data sets or artificial intelligence.
""", LIT_W, size=13, head_size=14, row_h=0.86, aligns=["c", "l", "l", "l"],
        bold_cols=(0,)); n += 1

    table_slide(prs, n, "Literature Survey (contd.)", LIT_HEAD, LITERATURE[5:], """
These are the next five. Papers six to eight are actual warning methods. They work,
but they rely on comparing many cells, on a trained neural network, or on fitted models.
Paper eight is often quoted for a limit of one degree per second, but in that paper it
is the rule used to confirm that runaway has already happened, not an early warning.
Paper nine shows that a sensor on the surface always reads cooler than the core, and
paper ten moves the analysis to the cloud, which fails when the network does.
""", LIT_W, size=13, head_size=14, row_h=0.86, aligns=["c", "l", "l", "l"],
        bold_cols=(0,)); n += 1

    two_section_slide(prs, n,
        "Problem Analysis", [
            "Existing studies explain how thermal runaway builds up through heat-producing "
            "reactions [1], and show the cell core can be hotter than its surface [9].",
            "Early-warning methods mostly rely on detailed models, large data sets, neural "
            "networks or the cloud [5]–[8], [10].",
            "The protection board used here acts on voltage and current only. It does not "
            "watch temperature at all.",
        ],
        "Research Gap", [
            "A simple method is needed that spots an abnormal temperature rise early, using "
            "only cell-surface sensors and a low-cost microcontroller.",
            "The early warning must be backed by protection that still works if the "
            "controller, a sensor or the network fails [4].",
            "Charging and discharging should be cut off separately, so that only the unsafe "
            "direction is stopped.",
        ], """
Putting the papers together, the analysis is this. We understand the physics well, and
there are clever warning methods, but they all need something a small pack does not
have: many cells to compare, trained models or a cloud connection. And the cheap
protection boards that small packs do have ignore temperature entirely. So the gap is a
simple trend-based warning that runs on the board, backed by protection that does not
depend on it.
""", size=17); n += 1

    content_slide(prs, n, "Objectives", [
        "To study thermal runaway in lithium-ion cells and the methods used to detect it early.",
        "To design a two-layer protection system: an independent hardware BMS, and an ESP32 "
        "supervisor that can disconnect charging and discharging separately.",
        "To measure every cell voltage, the pack current and four cell temperatures "
        "accurately, using an ADS1115, an INA226 and NTC thermistors.",
        "To estimate the rate of temperature rise (dT/dt) in firmware and act on it before "
        "any fixed temperature limit is reached, with every trip latched.",
        "To show live readings and faults on a Wi-Fi dashboard, while every safety function "
        "keeps working without Wi-Fi.",
    ], """
These five objectives map directly onto the project timeline later in the talk. The
first two are about understanding the problem and designing the answer, and both are
done. The third and fourth are the hardware and firmware work for the coming months.
The last one makes the system visible, but I have deliberately kept it out of the
safety chain.
""", size=17); n += 1

    image_slide(prs, n, "Methodology", "r1_methodology.png", """
This is how the controller works, five times every second. It reads the four cell taps,
the pack current and the four temperatures, removes noise with a median filter and a
ten-second low-pass filter, and then works out the rate of temperature rise by fitting a
straight line over the last thirty seconds. Before trusting any reading it checks that
the sensors are plausible. Then it compares everything with the trip limits and the
warning limits. A trip opens only the relay for the unsafe direction and stays latched
until a manual reset.
"""); n += 1

    image_slide(prs, n, "Block Diagram", "r1_block_diagram.png", """
The design has two layers. Layer A, at the top, is a hardware BMS board connected
directly to the cells. It handles over-voltage, under-voltage, over-current and short
circuit on its own, and it keeps working even if the ESP32 or the Wi-Fi fails. Layer B
is the ESP32 supervisor. It reads the ADS1115 for the cell voltages, the INA226 for the
current and four thermistors for temperature, and it drives two relays that connect the
load and the charger separately.
"""); n += 1

    image_slide(prs, n, "Schematic Diagram", "r1_schematic.png", """
This is the power path. The cells connect to the hardware BMS through five balance taps.
The protected positive goes through a 7.5 ampere fuse and a 5 milliohm shunt, where the
INA226 measures the current, and then to the load and the charger. Each branch has its
own relay in the negative return. Both relays are normally open and held off by
pull-ups, so if the ESP32 resets or crashes, both branches disconnect.
""", bullets=[
        "The hardware BMS protects the cells on its own, even if the ESP32 or Wi-Fi fails.",
        "Each relay is normally open and held off by a pull-up, so a reset disconnects both branches.",
    ]); n += 1

    table_slide(prs, n, "Hardware and Software Requirements",
        ["Type", "Item", "Used for"],
        [["Hardware", "ESP32-WROOM-32 DevKit", "Sensing, dT/dt, relay control and Wi-Fi"],
         ["Hardware", "4 × NCR18650GA 3300 mAh", "The 4S1P pack, with a 16.8 V 1.5 A charger"],
         ["Hardware", "4S 20 A hardware BMS", "Voltage, current and short-circuit protection"],
         ["Hardware", "ADS1115 16-bit ADC", "The four cell-tap voltages"],
         ["Hardware", "INA226 with 5 mΩ shunt", "Pack current, charging and discharging"],
         ["Hardware", "4 × NTC 10 kΩ B3950", "Temperature on each cell"],
         ["Hardware", "2-channel 5 V relay module", "Separate charge and load disconnect"],
         ["Hardware", "LM2596, 7.5 A fuse, buzzer", "5 V supply, wiring protection, local alarm"],
         ["Software", "ESP-IDF with C++", "Firmware framework and language"],
         ["Software", "FreeRTOS", "Sensor, safety and telemetry tasks"],
         ["Software", "HTML, CSS, JavaScript", "The Wi-Fi dashboard"],
         ["Software", "Siemens NX, Git and GitHub", "Enclosure model, version control"]],
        """
This is everything the project uses. On the hardware side the main parts are the ESP32,
the four cells, the hardware BMS board, the ADS1115 for accurate cell voltages, the
INA226 for current and the four thermistors. The relay module gives the separate charge
and load control. On the software side the firmware is written in C++ on ESP-IDF, with
FreeRTOS running the sensing, safety and telemetry work as separate tasks.
""", [2.00, 4.20, 5.60], size=14, row_h=0.39, aligns=["c", "l", "l"]); n += 1

    slide = table_slide(prs, n, "Individual Contribution",
        ["Member", "Contributions"],
        [[["Ms. Muskan Sulathana", "(individual project)"],
          "Studied research papers on thermal runaway, early-warning methods and BMS design, "
          "and identified the research gap."],
         ["", "Designed the two-layer protection: an independent hardware BMS and an ESP32 "
              "supervisor with separate charge and load relays."],
         ["", "Selected and costed every component, reconciled the purchase list and recorded "
              "the parts already in hand."],
         ["", "Prepared a twelve-stage build and test plan, in which the cells are added only "
              "after low-voltage testing."],
         ["", "Prepared the project documents and this presentation."]],
        """
This is an individual project, so all of the work so far is mine. The main pieces are
the literature survey, the two-layer design, the component selection and costing, and a
staged build and test plan. That plan matters for safety: the lithium cells are only
connected after every sensor and both relays have been tested at low voltage.
""", [3.30, 8.40], size=15, row_h=0.80, aligns=["c", "l"])
    table = [s for s in slide.shapes if s.has_table][0].table
    table.cell(1, 0).merge(table.cell(5, 0))
    n += 1

    table_slide(prs, n, "Project Timeline",
        ["Activity", "Month 1", "Month 2", "Month 3", "Month 4", "Month 5"],
        [[{"b": "Objective 1: ", "t": "Literature Survey & System Study"}, "✓", "✓", "", "", ""],
         [{"b": "Objective 2: ", "t": "Two-Layer Design & Component Selection"}, "✗", "✓", "", "", ""],
         [{"b": "Objective 3: ", "t": "Sensing Hardware, Pack Assembly & Calibration"}, "✗", "✗", "", "", ""],
         [{"b": "Objective 4: ", "t": "dT/dt Estimation & Safety State Machine"}, "✗", "✗", "", "", ""],
         [{"b": "Objective 5: ", "t": "Wi-Fi Dashboard, Testing & Documentation"}, "✗", "✗", "", "", ""]],
        """
This is where I am. The literature survey was done over the first two months, and the
two-layer design and component selection were finished in the second month. The
remaining three objectives are the build: assembling and calibrating the sensing
hardware, writing and testing the firmware, and then the dashboard, full testing and
documentation.
""", [4.80, 1.40, 1.40, 1.40, 1.40, 1.40], size=15, row_h=0.74,
        aligns=["l", "c", "c", "c", "c", "c"],
        legend=["✓ = Completed", "✗ = Yet to be done"]); n += 1

    content_slide(prs, n, "References", REFERENCES[:5], """
These are the first five references, in IEEE style, numbered as in the survey tables.
""", size=14, numbered=True); n += 1

    refs = content_slide(prs, n, "References (contd.)", REFERENCES[5:], """
These are references six to ten. Seven of the ten are IEEE publications.
""", size=14, numbered=True)
    # continue the numbering from the previous page
    for i, p in enumerate([s for s in refs.shapes if s.has_text_frame][-1].text_frame.paragraphs):
        p.runs[0].text = "[%d]  " % (i + 6)
    n += 1

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
