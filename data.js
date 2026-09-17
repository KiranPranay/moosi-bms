// data.js
// Edit this file to add/rename phases or tasks, to hardcode a task as complete
// (set done: true) and push it — hardcoded completions override local state —
// and to file the notes and documents that appear when a card is opened.
// Bump DATA_VERSION whenever you change the structure.

export const DATA_VERSION = "2.2.0";

/* ------------------------------------------------------------------------
   DOCUMENTS
   ------------------------------------------------------------------------
   A document is either a file committed in this repo:

     { id: "doc-bom", title: "Bill of Materials", file: "./docs/bom.csv" }

   or a link to somewhere else:

     { id: "doc-sheet", title: "Live BOM", url: "https://docs.google.com/..." }

   Optional fields:
     kind        overrides the icon/viewer. Normally inferred from the
                 extension: pdf | slides | sheet | table | doc | image |
                 cad | code | archive | link
     note        one line of context shown under the title
     pending     true = "not filed yet". Renders as a soft placeholder instead
                 of a broken link. Delete this line once you commit the file.
     totalColumn for kind "table" (a .csv): sums that column and shows a total
     extra       a second file offered next to the first, as
                 { label: "PowerPoint", file: "./docs/…​.pptx" }

   .csv files render as a real table in the panel, images and PDFs preview
   inline, everything else downloads.
   ------------------------------------------------------------------------ */

/** Documents that belong to the project as a whole rather than to one phase. */
export const PROJECT_DOCS = [
  {
    id: "doc-abstract",
    title: "Abstract",
    file: "./docs/abstract.pdf",
    note: "The one-page project abstract.",
    pending: true,
  },
  {
    id: "doc-review1",
    title: "First Review Presentation",
    file: "./docs/reviews/first-review/Predictive_BMS_First_Review.pdf",
    note: "The deck for the first review. Slides, diagrams and speaker notes.",
    extra: { label: "PowerPoint", file: "./docs/reviews/first-review/Predictive_BMS_First_Review.pptx" },
  },
  {
    id: "doc-review0",
    title: "Zeroth Review Presentation",
    file: "./docs/reviews/zeroth-review/Predictive_BMS_Zeroth_Review.pdf",
    note: "Abstract, problem, objective, block diagram and literature survey.",
    extra: { label: "PowerPoint", file: "./docs/reviews/zeroth-review/Predictive_BMS_Zeroth_Review.pptx" },
  },
  {
    id: "doc-bom",
    title: "Bill of Materials",
    file: "./docs/bom.csv",
    note: "Redesigned 4S1P build BOM: 25 required lines and seven excluded legacy parts. Full replacement value is ₹9,246.19, including owned stock retained for reproducibility.",
    totalColumn: "Line total (INR)",
  },
  {
    id: "doc-costing",
    title: "Costing Sheet",
    file: "./docs/costing.csv",
    note: "Full replacement cost is ₹9,246.19: ₹5,873.19 owned stock, ₹2,854.00 in the reconciled Robu cart and ₹519.00 of conditional or unresolved allowances. Shipping and lab tools are excluded.",
    totalColumn: "Amount (INR)",
  },
  {
    id: "doc-sld",
    title: "Current System Architecture",
    file: "./docs/current-architecture.svg",
    note: "Authoritative power, protection, sensing and independent charge/load isolation diagram for the 5A prototype.",
  },
  {
    id: "doc-architecture",
    title: "Architecture and Technical Specification",
    file: "./docs/current-architecture.md",
    note: "Build authority: design envelope, nets, pin map, thresholds, failure behaviour and validated sources.",
  },
  {
    id: "doc-build-sequence",
    title: "Safe Build and Validation Sequence",
    file: "./docs/safe-build-sequence.md",
    note: "Twelve gated stages with acceptance criteria and stop conditions; lithium cells are introduced only after low-voltage validation.",
  },
];

export const PHASES = [
  {
    id: "p1",
    number: 1,
    title: "Initial Approvals",
    blurb: "Getting the green light.",
    notes: [
      "Nothing gets ordered until the guide signs off. Keep the approved copy of the synopsis in here so there is never a question about which version was accepted.",
    ],
    docs: [
      { id: "p1-doc-arch", title: "Architecture Diagram", file: "./docs/architecture.png", note: "Block diagram submitted with the synopsis.", pending: true },
      { id: "p1-doc-signoff", title: "Guide Sign-off", file: "./docs/guide-approval.pdf", note: "Scanned approval page.", pending: true },
    ],
    docRefs: ["doc-abstract", "doc-review1"],
    tasks: [
      { id: "p1-synopsis",     title: "Synopsis",              done: true  },
      { id: "p1-architecture", title: "Architecture Diagram",  done: true  },
      { id: "p1-guide",        title: "Guide Approval",        done: true  },
    ],
  },
  {
    id: "p2",
    number: 2,
    title: "Procurement",
    blurb: "Gathering the parts.",
    notes: [
      "Keep every quote and invoice in this phase — the costing sheet is only as good as the paperwork behind it.",
      "The full replacement BOM is ₹9,246.19. Confirmed owned stock accounts for ₹5,873.19, the reconciled Robu cart is ₹2,854.00, and ₹519.00 remains as conditional or unresolved allowances.",
      "Owned stock includes four red-rewrapped NCR18650GA cells, pure nickel strip, two perfboards, a suitable 16.8V charger and PETG filament. Replacement prices remain in the BOM so another builder can reproduce the project.",
      "Before ordering, match the 7.5A fuse to its holder. Before assembly, verify the owned charger's CC/CV behaviour, isolation, 16.80V output, plug dimensions and polarity, and qualify the four cells by inspection, resting voltage, capacity and DC resistance.",
    ],
    docs: [
      { id: "p2-doc-quotes", title: "Supplier Quotes", file: "./docs/quotes.pdf", note: "Comparison of the shortlisted sellers.", pending: true },
      { id: "p2-doc-invoices", title: "Invoices", file: "./docs/invoices.pdf", pending: true },
    ],
    docRefs: ["doc-bom", "doc-costing", "doc-architecture", "doc-build-sequence"],
    tasks: [
      { id: "p2-electronics", title: "Reconcile Robu cart to the redesigned BOM (₹2,854)", done: true },
      { id: "p2-owned-stock", title: "Record owned cells, nickel, perfboards, charger and PETG (₹5,873.19)", done: true },
      { id: "p2-cells",       title: "Inspect, record and match the existing NCR18650GA set", done: false },
      { id: "p2-protection",  title: "Purchase Robu protection and mechanical cart", done: false },
      { id: "p2-sensing",     title: "Purchase Robu sensing and control cart", done: false },
      { id: "p2-gaps",        title: "Resolve ₹519 allowances: sleeve, ADC clamps, charger connector and hardware", done: false },
      { id: "p2-inspection",  title: "Receive parts and complete incoming inspection", done: false },
    ],
  },
  {
    id: "p3",
    number: 3,
    title: "Prototyping",
    blurb: "Making it real on the bench.",
    notes: [
      "Photograph the bench at every stage. It costs nothing now and makes the report enormously easier later.",
      "Follow the safe build sequence in order. Complete low-voltage sensing, relay fail-safe and BMS-harness simulation before accepting or welding cells.",
    ],
    docs: [
      { id: "p3-doc-bench", title: "Bench Photos", file: "./docs/bench-photos.png", note: "Pack assembly and sensing wiring.", pending: true },
      { id: "p3-doc-divider", title: "Divider Calculations", file: "./docs/divider-calcs.csv", note: "Resistor values per cell tap.", pending: true },
    ],
    docRefs: ["doc-sld", "doc-architecture", "doc-build-sequence", "doc-bom"],
    tasks: [
      { id: "p3-pack",      title: "Match cells and qualify spot welds", done: false },
      { id: "p3-sensing",   title: "Validate voltage and current sensing at low voltage", done: false },
      { id: "p3-ntc",       title: "Calibrate four fast NTC channels", done: false },
      { id: "p3-failsafe",  title: "Prove reset and sensor-fault relay fail-safe", done: false },
      { id: "p3-bms",       title: "Validate the BMS tap harness before live cells", done: false },
      { id: "p3-assemble",  title: "Weld and insulate the 4S1P pack", done: false },
      { id: "p3-bringup",   title: "Complete fused first power-up at rest", done: false },
    ],
  },
  {
    id: "p4",
    number: 4,
    title: "Core Software",
    blurb: "Teaching it to think.",
    notes: [
      "Commit early and often. Write the calibration constants down here as you find them — they are impossible to reconstruct from memory.",
    ],
    docs: [
      { id: "p4-doc-flow", title: "Control Flow Diagram", file: "./docs/control-flow.png", note: "Sampling, rate-of-change and cutoff states.", pending: true },
      { id: "p4-doc-calib", title: "Calibration Log", file: "./docs/calibration.csv", note: "Measured vs. reported, per channel.", pending: true },
    ],
    docRefs: ["doc-sld", "doc-architecture", "doc-build-sequence"],
    tasks: [
      { id: "p4-platformio", title: "Set up the ESP-IDF project",      done: false },
      { id: "p4-analog",     title: "Calibrate ADS1115 / INA226 / NTC acquisition", done: false },
      { id: "p4-roc",        title: "Implement filtered 30s dT/dt estimator", done: false },
      { id: "p4-cutoff",     title: "Implement latched safety state machine", done: false },
      { id: "p4-plausibility", title: "Implement sensor plausibility and watchdog faults", done: false },
      { id: "p4-eventlog",   title: "Log trips with cause and measurement snapshot", done: false },
    ],
  },
  {
    id: "p5",
    number: 5,
    title: "IoT Integration",
    blurb: "Sending it out into the world.",
    notes: [
      "Keep credentials out of the repo. Note here only what the dashboard expects to receive, not the keys it needs to receive it.",
    ],
    docs: [
      { id: "p5-doc-payload", title: "Telemetry Payload Spec", file: "./docs/payload-spec.md", note: "Field names, units and sample rate.", pending: true },
      { id: "p5-doc-ui", title: "Dashboard Mockup", file: "./docs/dashboard-mockup.png", pending: true },
    ],
    tasks: [
      { id: "p5-wifi",      title: "Program Wi-Fi connection",   done: false },
      { id: "p5-dashboard", title: "Build live telemetry and latched-fault dashboard", done: false },
      { id: "p5-offline",   title: "Verify all safety functions with Wi-Fi unavailable", done: false },
    ],
  },
  {
    id: "p6",
    number: 6,
    title: "Final Polish",
    blurb: "The finishing touches.",
    notes: [
      "Leave time for the enclosure print to fail once. It usually does.",
      "The report and the presentation want the same figures — export them once, at print resolution, and reuse.",
    ],
    docs: [
      { id: "p6-doc-pcb", title: "PCB Layout", file: "./docs/pcb-layout.pdf", note: "Gerber preview and layer stack.", pending: true },
      { id: "p6-doc-enclosure", title: "NX Enclosure Model", file: "./docs/enclosure.stp", note: "STEP export for printing.", pending: true },
    ],
    docRefs: ["doc-bom", "doc-costing", "doc-sld", "doc-architecture", "doc-build-sequence"],
    tasks: [
      { id: "p6-pcb",          title: "Solder permanent PCB",               done: false },
      { id: "p6-enclosure",    title: "Model and print vented PETG enclosure", done: false },
      {
        id: "p6-report",
        title: "Draft report",
        done: false,
        // Documents can also hang off a single task.
        docs: [
          { id: "p6-doc-report", title: "Report Draft", file: "./docs/report-draft.docx", pending: true },
        ],
      },
      {
        id: "p6-presentation",
        title: "Create presentation",
        done: false,
        docs: [
          { id: "p6-doc-deck", title: "Final Presentation", file: "./docs/final-presentation.pptx", pending: true },
        ],
      },
    ],
  },
];
