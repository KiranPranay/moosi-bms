// data.js
// Edit this file to add/rename phases or tasks, to hardcode a task as complete
// (set done: true) and push it — hardcoded completions override local state —
// and to file the notes and documents that appear when a card is opened.
// Bump DATA_VERSION whenever you change the structure.

export const DATA_VERSION = "1.1.0";

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
  },
  {
    id: "doc-review0",
    title: "Zeroth Review Presentation",
    file: "./docs/reviews/zeroth-review/zeroth-review.pdf",
    note: "Add your own copy of the zeroth review deck here.",
    pending: true,
  },
  {
    id: "doc-bom",
    title: "Bill of Materials",
    file: "./docs/bom.csv",
    note: "Every part, quantity and source. Doubles as a procurement checklist.",
  },
  {
    id: "doc-costing",
    title: "Costing Sheet",
    file: "./docs/costing.csv",
    note: "Running budget. Prices are indicative until quotes come in.",
    totalColumn: "Amount (INR)",
  },
  {
    id: "doc-sld",
    title: "Single Line Diagram",
    file: "./docs/sld-placeholder.svg",
    note: "Pack, sensing and cutoff in one line. Replace with your own drawing.",
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
      { id: "p1-synopsis",     title: "Synopsis",              done: false },
      { id: "p1-architecture", title: "Architecture Diagram",  done: false },
      { id: "p1-guide",        title: "Guide Approval",        done: false },
    ],
  },
  {
    id: "p2",
    number: 2,
    title: "Procurement",
    blurb: "Gathering the parts.",
    notes: [
      "Keep every quote and invoice in this phase — the costing sheet is only as good as the paperwork behind it.",
      "Order the cells from a seller who will actually give you matched capacities. Mismatched cells will haunt the balancing work in Phase 3.",
    ],
    docs: [
      { id: "p2-doc-quotes", title: "Supplier Quotes", file: "./docs/quotes.pdf", note: "Comparison of the shortlisted sellers.", pending: true },
      { id: "p2-doc-invoices", title: "Invoices", file: "./docs/invoices.pdf", pending: true },
    ],
    docRefs: ["doc-bom", "doc-costing"],
    tasks: [
      { id: "p2-electronics", title: "Procure ESP32 / Thermistors / MOSFETs", done: false },
      { id: "p2-cells",       title: "Procure 18650 cells",                   done: false },
    ],
  },
  {
    id: "p3",
    number: 3,
    title: "Prototyping",
    blurb: "Making it real on the bench.",
    notes: [
      "Photograph the bench at every stage. It costs nothing now and makes the report enormously easier later.",
    ],
    docs: [
      { id: "p3-doc-bench", title: "Bench Photos", file: "./docs/bench-photos.png", note: "Pack assembly and sensing wiring.", pending: true },
      { id: "p3-doc-divider", title: "Divider Calculations", file: "./docs/divider-calcs.csv", note: "Resistor values per cell tap.", pending: true },
    ],
    docRefs: ["doc-sld", "doc-bom"],
    tasks: [
      { id: "p3-pack",      title: "Assemble 4S pack",                         done: false },
      { id: "p3-sensing",   title: "Wire voltage dividers / current sensors",  done: false },
      { id: "p3-ntc",       title: "Attach NTC thermistors",                   done: false },
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
    docRefs: ["doc-sld"],
    tasks: [
      { id: "p4-platformio", title: "Init PlatformIO",                 done: false },
      { id: "p4-analog",     title: "Read analog data",                done: false },
      { id: "p4-roc",        title: "Program rate-of-change logic",    done: false },
      { id: "p4-cutoff",     title: "Code safety cutoff",              done: false },
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
      { id: "p5-dashboard", title: "Build simple web dashboard", done: false },
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
    docRefs: ["doc-bom", "doc-costing", "doc-sld"],
    tasks: [
      { id: "p6-pcb",          title: "Solder permanent PCB",               done: false },
      { id: "p6-enclosure",    title: "Model & 3D print NX enclosure",      done: false },
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
