// app.js
// Rendering, state merging, localStorage, progress, and the small delights.
//
// Effective completion for a task is:
//     task.done === true            (hardcoded override, shipped in data.js)
//  OR stored.completed[task.id]     (this browser's own progress)

import { DATA_VERSION, PHASES, PROJECT_DOCS } from './data.js';

/* ── constants ──────────────────────────────────────────────────── */

const STORAGE_KEY = 'predictive-bms-tracker:v1';
const COUNT_ANIM_MS = 500;
const SPARKLE_MS = 800;
const CLOCK_TICK_MS = 60_000;

/* ── flattened views of the data ────────────────────────────────── */

const ALL_TASKS = PHASES.flatMap((phase) => phase.tasks);
const TOTAL_TASKS = ALL_TASKS.length;
const VALID_IDS = new Set(ALL_TASKS.map((task) => task.id));
const VALID_PHASE_IDS = new Set(PHASES.map((phase) => phase.id));

const TASK_BY_ID = new Map(ALL_TASKS.map((task) => [task.id, task]));
const PHASE_BY_TASK_ID = new Map(
  PHASES.flatMap((phase) => phase.tasks.map((task) => [task.id, phase])),
);

const PROJECT_DOC_BY_ID = new Map((PROJECT_DOCS || []).map((doc) => [doc.id, doc]));

/** Phase-level docs + docs hanging off individual tasks + resolved docRefs. */
function docsForPhase(phase) {
  const own = (phase.docs || []).map((doc) => ({ doc, from: null }));

  const fromTasks = phase.tasks.flatMap((task) =>
    (task.docs || []).map((doc) => ({ doc, from: task.title })),
  );

  const referenced = (phase.docRefs || []).map((id) => {
    const doc = PROJECT_DOC_BY_ID.get(id);
    if (!doc) console.warn(`[tracker] data.js: unknown docRef "${id}" in phase "${phase.id}"`);
    return doc ? { doc, from: null, shared: true } : null;
  }).filter(Boolean);

  return { own: own.concat(fromTasks), referenced };
}

function phaseDocCount(phase) {
  const { own, referenced } = docsForPhase(phase);
  return own.length + referenced.length;
}

/* ── element references, filled in during render ────────────────── */

const els = {};
const taskRefs = new Map();  // taskId  -> { row, input, title }
const phaseRefs = new Map(); // phaseId -> { card, counter, track, fill, badge }

/* ── state ──────────────────────────────────────────────────────── */

let state = emptyState();
let countAnimFrame = null;
let countAnimTimer = null;
let displayedPercent = 0;

function emptyState() {
  return { version: DATA_VERSION, completed: {}, completedAt: {}, notes: {} };
}

/**
 * Reads localStorage defensively. Missing, unparseable or foreign-shaped data
 * degrades to an empty state rather than throwing. Stored ids that no longer
 * exist in PHASES are dropped; everything that still matches is carried over,
 * regardless of the stored version — a version bump never wipes progress.
 */
function loadState() {
  const next = emptyState();

  let raw = null;
  try {
    raw = localStorage.getItem(STORAGE_KEY);
  } catch {
    return next; // storage disabled (private mode, blocked cookies, …)
  }
  if (!raw) return next;

  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return next; // corrupt JSON
  }
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return next;

  const completed = isPlainObject(parsed.completed) ? parsed.completed : {};
  const completedAt = isPlainObject(parsed.completedAt) ? parsed.completedAt : {};
  const notes = isPlainObject(parsed.notes) ? parsed.notes : {};

  for (const id of Object.keys(completed)) {
    if (VALID_IDS.has(id) && completed[id] === true) next.completed[id] = true;
  }
  for (const id of Object.keys(completedAt)) {
    if (!next.completed[id]) continue; // no orphan timestamps
    const value = completedAt[id];
    if (typeof value === 'string' && Number.isFinite(Date.parse(value))) {
      next.completedAt[id] = value;
    }
  }
  for (const id of Object.keys(notes)) {
    if (!VALID_PHASE_IDS.has(id)) continue;
    if (typeof notes[id] === 'string' && notes[id].trim() !== '') next.notes[id] = notes[id];
  }
  return next;
}

function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    /* Nothing useful to do if storage is full or unavailable — the UI still works. */
  }
}

function isPlainObject(value) {
  return !!value && typeof value === 'object' && !Array.isArray(value);
}

/** Hardcoded in data.js — checked, disabled, and immune to Reset. */
function isLocked(task) {
  return task.done === true;
}

function isDone(task) {
  return isLocked(task) || state.completed[task.id] === true;
}

/* ── small utilities ────────────────────────────────────────────── */

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function prefersReducedMotion() {
  return typeof window.matchMedia === 'function'
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function percent(done, total) {
  return total > 0 ? Math.round((done / total) * 100) : 0;
}

function calendarDayDiff(thenMs, nowMs) {
  const a = new Date(thenMs); a.setHours(0, 0, 0, 0);
  const b = new Date(nowMs);  b.setHours(0, 0, 0, 0);
  return Math.round((b.getTime() - a.getTime()) / 86_400_000);
}

/** Tiny relative-time formatter. No libraries, deliberately gentle wording. */
function relativeTime(thenMs) {
  const nowMs = Date.now();
  const diff = Math.max(0, nowMs - thenMs);

  const seconds = Math.round(diff / 1000);
  if (seconds < 45) return 'just now';

  const minutes = Math.round(seconds / 60);
  if (minutes < 2) return 'a minute ago';
  if (minutes < 60) return `${minutes} minutes ago`;

  // Elapsed hours win below a day: just after midnight, "2 hours ago" is far
  // clearer than "yesterday", even though the tick did land on another date.
  const hours = Math.round(minutes / 60);
  if (hours < 2) return 'an hour ago';
  if (hours < 24) return `${hours} hours ago`;

  const days = calendarDayDiff(thenMs, nowMs);
  if (days === 0) return `${hours} hours ago`;
  if (days === 1) return 'yesterday';
  if (days < 7) return `${days} days ago`;
  if (days < 14) return 'last week';
  if (days < 31) return `${Math.round(days / 7)} weeks ago`;

  const months = Math.round(days / 30);
  if (months < 2) return 'last month';
  if (months < 12) return `${months} months ago`;

  const years = Math.round(days / 365);
  return years < 2 ? 'last year' : `${years} years ago`;
}

/* ── markup ─────────────────────────────────────────────────────── */

const CHECK_SVG = `
  <svg class="task-check w-3.5 h-3.5 text-white" viewBox="0 0 20 20" fill="none"
       stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"
       aria-hidden="true" focusable="false">
    <path d="M4.5 10.5 8.3 14.3 15.5 5.9" />
  </svg>`;

const FLOWER_SVG = `
  <svg class="w-3.5 h-3.5" viewBox="0 0 32 32" aria-hidden="true" focusable="false">
    <g fill="#f2b32e">
      ${Array.from({ length: 12 }, (_, i) =>
        `<ellipse cx="16" cy="7.4" rx="2.9" ry="6.2" transform="rotate(${i * 30} 16 16)" />`).join('')}
    </g>
    <circle cx="16" cy="16" r="6.2" fill="#6b4423" />
    <circle cx="16" cy="16" r="3.1" fill="#8a5a2b" />
  </svg>`;

function taskMarkup(task) {
  const locked = isLocked(task);
  const done = isDone(task);

  const rowClasses = [
    'task-row relative flex items-center gap-4 min-h-[44px] rounded-2xl px-4 py-3.5',
    'transition-colors duration-300',
    locked ? 'is-locked' : 'cursor-pointer hover:bg-rose-50/70',
    done ? 'is-done' : '',
  ].join(' ');

  const lockAttrs = locked
    ? ' disabled title="Marked complete 🌻"'
    : '';
  const lockTitle = locked ? ' title="Marked complete 🌻"' : '';

  return `
    <li>
      <label class="${rowClasses}"${lockTitle}>
        <input type="checkbox"
               class="task-input peer sr-only"
               data-task-id="${escapeHtml(task.id)}"
               ${done ? 'checked' : ''}${lockAttrs} />
        <span class="task-box w-6 h-6 shrink-0 rounded-full border-2 border-rose-300 bg-white
                     flex items-center justify-center">${CHECK_SVG}</span>
        <span class="task-label flex-1 min-w-0">
          <span class="task-title font-sans font-semibold text-base md:text-lg text-ink-700">${escapeHtml(task.title)}</span>
        </span>
      </label>
    </li>`;
}

function phaseMarkup(phase) {
  const titleId = `phase-${escapeHtml(phase.id)}-title`;
  const barId = `phase-${escapeHtml(phase.id)}-bar`;

  return `
    <section class="phase-card bg-white/70 backdrop-blur rounded-3xl border border-rose-200/70
                    shadow-petal hover:shadow-petal-lg transition-shadow duration-500 p-8 md:p-10"
             data-phase-id="${escapeHtml(phase.id)}"
             aria-labelledby="${titleId}">

      <div class="flex items-start gap-4">
        <span class="w-10 h-10 shrink-0 rounded-full bg-rose-100 text-mauve-600 font-semibold
                     flex items-center justify-center select-none" aria-hidden="true">${escapeHtml(phase.number)}</span>

        <div class="flex-1 min-w-0">
          <div class="flex items-start justify-between gap-3">
            <h3 id="${titleId}" class="font-display font-semibold text-2xl text-ink-700 leading-snug">
              <span class="sr-only">Phase ${escapeHtml(phase.number)}: </span>${escapeHtml(phase.title)}
            </h3>
            <span class="phase-counter shrink-0 mt-1 text-sm text-ink-400 tabular-nums">0 / 0</span>
          </div>

          <p class="text-ink-400 text-sm mt-1">${escapeHtml(phase.blurb)}</p>

          <p class="phase-badge mt-3 inline-flex items-center gap-1.5 rounded-full bg-sage-200
                    px-3 py-1 text-xs font-semibold text-mauve-600" hidden>
            ${FLOWER_SVG}<span>Complete 🌻</span>
          </p>
        </div>
      </div>

      <div id="${barId}" class="phase-track mt-5 h-1.5 w-full rounded-full bg-rose-100 overflow-hidden"
           role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"
           aria-label="${escapeHtml(phase.title)} progress">
        <div class="phase-fill h-full rounded-full bg-gradient-to-r from-rose-300 via-rose-400 to-mauve-400"
             style="width: 0%"></div>
      </div>

      <ul class="mt-6 space-y-3">
        ${phase.tasks.map(taskMarkup).join('')}
      </ul>

      <button type="button" class="phase-open mt-6 pt-5 border-t border-rose-200/60" aria-haspopup="dialog"
              aria-label="Open notes and documents for ${escapeHtml(phase.title)}">
        <span class="card-hint flex items-center justify-between gap-3 text-sm text-ink-400">
          <span class="phase-hint">Notes &amp; documents</span>
          <span aria-hidden="true">&#8594;</span>
        </span>
      </button>
    </section>`;
}


/* ══════════════════════════════════════════════════════════════════
   DOCUMENTS
   ══════════════════════════════════════════════════════════════════ */

const ALL_DOCS = (PROJECT_DOCS || []).concat(
  PHASES.flatMap((phase) =>
    (phase.docs || []).concat(phase.tasks.flatMap((task) => task.docs || [])),
  ),
);

const DOC_BY_ID = new Map();
for (const doc of ALL_DOCS) {
  if (DOC_BY_ID.has(doc.id)) console.warn(`[tracker] data.js: duplicate document id "${doc.id}"`);
  DOC_BY_ID.set(doc.id, doc);
}

const EXT_KIND = {
  pdf: 'pdf',
  ppt: 'slides', pptx: 'slides', key: 'slides', odp: 'slides',
  xls: 'sheet', xlsx: 'sheet', ods: 'sheet',
  csv: 'table', tsv: 'table',
  doc: 'doc', docx: 'doc', odt: 'doc', rtf: 'doc', txt: 'doc', md: 'doc',
  png: 'image', jpg: 'image', jpeg: 'image', gif: 'image', webp: 'image', svg: 'image', avif: 'image',
  stp: 'cad', step: 'cad', stl: 'cad', iges: 'cad', igs: 'cad', prt: 'cad', f3d: 'cad', dwg: 'cad', dxf: 'cad',
  ino: 'code', cpp: 'code', c: 'code', h: 'code', hpp: 'code', py: 'code', json: 'code', yml: 'code', yaml: 'code',
  zip: 'archive', rar: 'archive', '7z': 'archive', tar: 'archive', gz: 'archive',
};

/** Explicit `kind` wins; otherwise infer from the file extension. */
function docKind(doc) {
  if (doc.kind) return doc.kind;
  if (!doc.file && doc.url) return 'link';
  const match = /\.([a-z0-9]+)(?:[?#].*)?$/i.exec(doc.file || '');
  return (match && EXT_KIND[match[1].toLowerCase()]) || 'file';
}

const KIND_LABEL = {
  pdf: 'PDF', slides: 'Slides', sheet: 'Spreadsheet', table: 'Table',
  doc: 'Document', image: 'Image', cad: 'CAD', code: 'Source',
  archive: 'Archive', link: 'Link', file: 'File',
};

/** image / pdf / csv can be shown without leaving the page. */
const PREVIEWABLE = new Set(['image', 'pdf', 'table']);

function docHref(doc) {
  return doc.url || doc.file || '';
}

function isExternal(doc) {
  return !doc.file && !!doc.url;
}

function canPreview(doc) {
  return !doc.pending && !isExternal(doc) && PREVIEWABLE.has(docKind(doc));
}

const DOC_GLYPH = {
  pdf:     '<path d="M5.5 2.5h6l4 4v11h-10z"/><path d="M11.5 2.5V7h4"/><path d="M8 11.5h4"/>',
  doc:     '<path d="M5.5 2.5h6l4 4v11h-10z"/><path d="M11.5 2.5V7h4"/><path d="M8 10.5h4M8 13.5h4"/>',
  slides:  '<path d="M3 4.5h14v9H3z"/><path d="M10 13.5v3.5M7.5 17h5"/>',
  table:   '<path d="M3.5 4.5h13v11h-13z"/><path d="M3.5 8.5h13M3.5 12h13M8 4.5v11M12.5 4.5v11"/>',
  sheet:   '<path d="M3.5 4.5h13v11h-13z"/><path d="M3.5 8.5h13M3.5 12h13M8 4.5v11M12.5 4.5v11"/>',
  image:   '<path d="M3.5 4.5h13v11h-13z"/><circle cx="7.6" cy="8.4" r="1.3"/><path d="M3.5 13.4l4.2-3.6 2.8 2.3 3.3-2.8 2.7 2.4"/>',
  cad:     '<path d="M10 2.9l6.4 3.6v7.2L10 17.3 3.6 13.7V6.5z"/><path d="M3.6 6.5L10 10.1l6.4-3.6M10 10.1v7.2"/>',
  code:    '<path d="M7 6.2l-3.6 3.9L7 14M13 6.2l3.6 3.9L13 14"/>',
  archive: '<path d="M3.5 4.5h13v3.2h-13z"/><path d="M5 7.7v8.3h10V7.7"/><path d="M8.6 11h2.8"/>',
  link:    '<path d="M8.4 11.6a3.4 3.4 0 004.8 0l2.1-2.1a3.4 3.4 0 00-4.8-4.8l-1 1"/><path d="M11.6 8.4a3.4 3.4 0 00-4.8 0l-2.1 2.1a3.4 3.4 0 004.8 4.8l1-1"/>',
  file:    '<path d="M5.5 2.5h6l4 4v11h-10z"/><path d="M11.5 2.5V7h4"/>',
};

const DOC_TINT = {
  table: 'bg-sage-200 text-sage-600',
  sheet: 'bg-sage-200 text-sage-600',
  image: 'bg-petal text-mauve-600',
  cad:   'bg-blush text-mauve-600',
  code:  'bg-blush text-mauve-600',
  link:  'bg-blush text-mauve-600',
};

function docIcon(kind) {
  const tint = DOC_TINT[kind] || 'bg-rose-100 text-mauve-600';
  return `
    <span class="doc-icon w-10 h-10 rounded-xl ${tint} flex items-center justify-center" aria-hidden="true">
      <svg class="w-5 h-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"
           stroke-linecap="round" stroke-linejoin="round" focusable="false">${DOC_GLYPH[kind] || DOC_GLYPH.file}</svg>
    </span>`;
}

const EMPTY_FLOWER = `
  <svg class="w-10 h-10 mx-auto opacity-70" viewBox="0 0 32 32" aria-hidden="true" focusable="false">
    <g fill="#fdd9e4">
      ${Array.from({ length: 12 }, (_, i) =>
        `<ellipse cx="16" cy="7.4" rx="2.9" ry="6.2" transform="rotate(${i * 30} 16 16)" />`).join('')}
    </g>
    <circle cx="16" cy="16" r="6.2" fill="#f7d6e0" />
  </svg>`;

/* ── CSV ──────────────────────────────────────────────────────────── */

/** RFC-4180-ish: handles quoted fields, embedded commas, doubled quotes, CRLF. */
function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];

    if (quoted) {
      if (char === '"') {
        if (text[i + 1] === '"') { field += '"'; i += 1; }
        else quoted = false;
      } else {
        field += char;
      }
      continue;
    }

    if (char === '"') quoted = true;
    else if (char === ',') { row.push(field); field = ''; }
    else if (char === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else if (char !== '\r') field += char;
  }
  if (field !== '' || row.length) { row.push(field); rows.push(row); }

  return rows.filter((cells) => cells.some((cell) => cell.trim() !== ''));
}

function numericValue(raw) {
  if (typeof raw !== 'string') return null;
  const cleaned = raw.replace(/[\s,₹$€£]/g, '');
  if (cleaned === '' || !/^-?\d*\.?\d+$/.test(cleaned)) return null;
  return Number.parseFloat(cleaned);
}

function renderCsvTable(text, doc) {
  const rows = parseCsv(text);
  if (!rows.length) return '<p class="text-sm text-ink-400">This file is empty.</p>';

  const [header, ...body] = rows;
  const width = header.length;

  const numericCol = header.map((_, col) => {
    const values = body.map((cells) => cells[col]);
    const parsed = values.map(numericValue);
    const filled = parsed.filter((value) => value !== null).length;
    return filled > 0 && filled >= Math.ceil(values.filter((v) => (v || '').trim() !== '').length * 0.8);
  });

  const totalCol = doc.totalColumn
    ? header.findIndex((cell) => cell.trim().toLowerCase() === String(doc.totalColumn).trim().toLowerCase())
    : -1;
  if (doc.totalColumn && totalCol === -1) {
    console.warn(`[tracker] data.js: totalColumn "${doc.totalColumn}" not found in ${doc.file}`);
  }

  const head = header
    .map((cell, col) => `<th scope="col" class="${numericCol[col] ? 'is-numeric' : ''}">${escapeHtml(cell)}</th>`)
    .join('');

  const rowsHtml = body.map((cells) => {
    const tds = [];
    for (let col = 0; col < width; col += 1) {
      tds.push(`<td class="${numericCol[col] ? 'is-numeric' : ''}">${escapeHtml(cells[col] ?? '')}</td>`);
    }
    return `<tr>${tds.join('')}</tr>`;
  }).join('');

  let foot = '';
  if (totalCol > -1) {
    const sum = body.reduce((acc, cells) => acc + (numericValue(cells[totalCol]) || 0), 0);
    const pre = totalCol > 0 ? `<td colspan="${totalCol}">Total</td>` : '';
    const post = totalCol < width - 1 ? `<td colspan="${width - totalCol - 1}"></td>` : '';
    foot = `<tfoot><tr>${pre}<td class="is-numeric">${escapeHtml(sum.toLocaleString(undefined, { maximumFractionDigits: 2 }))}</td>${post}</tr></tfoot>`;
  }

  return `
    <div class="doc-table-wrap">
      <table class="doc-table">
        <thead><tr>${head}</tr></thead>
        <tbody>${rowsHtml}</tbody>
        ${foot}
      </table>
    </div>
    <p class="mt-2 text-xs text-ink-400">${body.length} row${body.length === 1 ? '' : 's'} · from ${escapeHtml(doc.file)}</p>`;
}

/* ── document rows ────────────────────────────────────────────────── */

function docRowMarkup(entry) {
  const { doc, from, shared } = entry;
  const kind = docKind(doc);
  const href = docHref(doc);
  const previewable = canPreview(doc);

  const meta = [KIND_LABEL[kind] || 'File'];
  if (from) meta.push(escapeHtml(from));
  if (shared) meta.push('project-wide');

  let action;
  if (doc.pending) {
    action = `<span class="shrink-0 text-xs text-ink-400 rounded-full bg-rose-50 border border-rose-200/70 px-3 py-1">Not filed yet</span>`;
  } else if (isExternal(doc)) {
    action = `<a href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer"
                 class="doc-link shrink-0 text-xs font-semibold text-mauve-500 hover:text-mauve-600 underline underline-offset-4 decoration-rose-200 rounded px-2 py-1
                        focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-300">Open&nbsp;&#8599;</a>`;
  } else if (previewable) {
    action = `<a href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer"
                 class="doc-link shrink-0 text-xs font-semibold text-mauve-500 hover:text-mauve-600 underline underline-offset-4 decoration-rose-200 rounded px-2 py-1
                        focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-300">Open&nbsp;&#8599;</a>`;
  } else {
    action = `<a href="${escapeHtml(href)}" download
                 class="doc-link shrink-0 text-xs font-semibold text-mauve-500 hover:text-mauve-600 underline underline-offset-4 decoration-rose-200 rounded px-2 py-1
                        focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-300">Download</a>`;
  }

  // A document can offer one extra file alongside the main one — a slide deck
  // published as a PDF, say, with the editable original next to it.
  const extra = (!doc.pending && doc.extra && doc.extra.file)
    ? `<a href="${escapeHtml(doc.extra.file)}" download
           class="doc-link shrink-0 text-xs font-semibold text-mauve-500 hover:text-mauve-600 underline underline-offset-4 decoration-rose-200 rounded px-2 py-1
                        focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-300">${escapeHtml(doc.extra.label || 'Download')}&nbsp;&#8595;</a>`
    : '';

  const title = previewable
    ? `<button type="button" class="doc-toggle text-left font-semibold text-ink-700 rounded
              focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-300 focus-visible:ring-offset-2"
              aria-expanded="false">${escapeHtml(doc.title)}</button>`
    : `<span class="font-semibold ${doc.pending ? 'text-ink-500' : 'text-ink-700'}">${escapeHtml(doc.title)}</span>`;

  return `
    <li class="doc-item">
      <div class="doc-row ${doc.pending ? 'doc-pending' : ''} flex items-center gap-3.5 rounded-2xl border border-rose-200/60
                  bg-white/70 px-4 py-3 ${previewable ? 'cursor-pointer hover:bg-rose-50/70' : ''}"
           data-doc-id="${escapeHtml(doc.id)}" ${previewable ? 'data-previewable="1"' : ''}>
        ${docIcon(kind)}
        <div class="flex-1 min-w-0">
          <p class="text-base leading-snug">${title}</p>
          <p class="text-xs text-ink-400 mt-0.5">${meta.join(' · ')}</p>
          ${doc.note ? `<p class="text-sm text-ink-500 mt-1.5 leading-relaxed">${escapeHtml(doc.note)}</p>` : ''}
        </div>
        <div class="shrink-0 flex items-center gap-1">${action}${extra}</div>
      </div>
      <div class="doc-preview hidden mt-3 rounded-2xl border border-rose-200/60 bg-white/80 p-3"></div>
    </li>`;
}

function docListMarkup(entries, emptyMessage) {
  if (!entries.length) {
    return `
      <div class="text-center py-10">
        ${EMPTY_FLOWER}
        <p class="mt-3 text-sm text-ink-400">${escapeHtml(emptyMessage)}</p>
      </div>`;
  }
  return `<ul class="space-y-3">${entries.map(docRowMarkup).join('')}</ul>`;
}

function sectionHeading(text, count) {
  return `
    <h3 class="font-display font-semibold text-xl text-mauve-600 mb-4 flex items-baseline gap-2">
      ${escapeHtml(text)}
      ${count === undefined ? '' : `<span class="font-sans text-xs font-semibold text-ink-400 tabular-nums">${count}</span>`}
    </h3>`;
}


/* ══════════════════════════════════════════════════════════════════
   DETAIL PANEL
   ══════════════════════════════════════════════════════════════════ */

let panelContext = null;      // { type: 'phase' | 'library', phase? }
let panelReturnFocus = null;
let panelCloseTimer = null;
let notesSaveTimer = null;
let notesFlashTimer = null;

function panelBodyMarkup(context) {
  return context.type === 'library'
    ? libraryPanelMarkup()
    : phasePanelMarkup(context.phase);
}

function phasePanelMarkup(phase) {
  const { own, referenced } = docsForPhase(phase);
  const total = phase.tasks.length;
  const done = phase.tasks.filter(isDone).length;
  const pct = percent(done, total);

  const authored = (phase.notes || [])
    .map((note) => `<p class="text-ink-500 leading-relaxed mb-3 last:mb-0">${escapeHtml(note)}</p>`)
    .join('');

  const savedNote = state.notes[phase.id] || '';

  const referencedBlock = referenced.length
    ? `<section class="mt-9">
         ${sectionHeading('Related documents', referenced.length)}
         <p class="-mt-2 mb-4 text-sm text-ink-400">Filed under the project, relevant here.</p>
         ${docListMarkup(referenced, '')}
       </section>`
    : '';

  return `
    <section>
      <div class="flex items-center justify-between gap-3 mb-2">
        <span class="text-sm text-ink-400">Progress</span>
        <span class="text-sm text-ink-400 tabular-nums">${done} / ${total} · ${pct}%</span>
      </div>
      <div class="h-1.5 w-full rounded-full bg-rose-100 overflow-hidden" role="progressbar"
           aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100"
           aria-label="${escapeHtml(phase.title)} progress">
        <div class="h-full rounded-full bg-gradient-to-r from-rose-300 via-rose-400 to-mauve-400"
             style="width: ${pct}%"></div>
      </div>
    </section>

    <section class="mt-9">
      ${sectionHeading('Notes')}
      ${authored || '<p class="text-sm text-ink-400 mb-3">No notes filed for this phase yet.</p>'}

      <div class="mt-5">
        <div class="flex items-baseline justify-between gap-3 mb-2">
          <label for="panel-notes" class="text-sm font-semibold text-ink-500">Your notes</label>
          <span id="panel-notes-saved" class="notes-saved text-xs text-sage-600 font-semibold">Saved</span>
        </div>
        <textarea id="panel-notes" class="notes-input" spellcheck="true"
                  data-phase-id="${escapeHtml(phase.id)}"
                  placeholder="Anything you want to remember about this phase…">${escapeHtml(savedNote)}</textarea>
        <p class="mt-2 text-xs text-ink-400">Saved in this browser only.</p>
      </div>
    </section>

    <section class="mt-9">
      ${sectionHeading('Documents', own.length)}
      ${docListMarkup(own, 'Nothing filed here yet. Add it in data.js.')}
    </section>

    ${referencedBlock}`;
}

function libraryPanelMarkup() {
  const entries = (PROJECT_DOCS || []).map((doc) => ({ doc, from: null }));

  const byPhase = PHASES.map((phase) => {
    const { own } = docsForPhase(phase);
    if (!own.length) return '';
    return `
      <div class="mt-6">
        <p class="text-sm font-semibold text-ink-500 mb-3">
          <span class="text-ink-400 font-normal">Phase ${escapeHtml(phase.number)} · </span>${escapeHtml(phase.title)}
        </p>
        ${docListMarkup(own, '')}
      </div>`;
  }).join('');

  return `
    <section>
      ${sectionHeading('Project documents', entries.length)}
      <p class="-mt-2 mb-4 text-sm text-ink-400">
        The things that span the whole build — abstract, BOM, costing, diagrams.
      </p>
      ${docListMarkup(entries, 'Nothing filed yet. Add it to PROJECT_DOCS in data.js.')}
    </section>

    ${byPhase ? `<section class="mt-10">${sectionHeading('Filed under phases')}${byPhase}</section>` : ''}`;
}

function openPanel(context) {
  if (panelCloseTimer !== null) {
    window.clearTimeout(panelCloseTimer);
    panelCloseTimer = null;
  }

  panelContext = context;
  panelReturnFocus = document.activeElement;

  const isLibrary = context.type === 'library';
  els.panelBadge.innerHTML = isLibrary ? LIBRARY_GLYPH : escapeHtml(context.phase.number);
  els.panelTitle.textContent = isLibrary ? 'Project documents' : context.phase.title;
  els.panelBlurb.textContent = isLibrary
    ? 'Everything filed for the Predictive BMS.'
    : context.phase.blurb;

  els.panelBody.innerHTML = panelBodyMarkup(context);
  els.panelScroll.scrollTop = 0;

  els.panel.classList.remove('hidden');
  document.body.classList.add('panel-locked');
  requestAnimationFrame(() => els.panel.classList.add('is-open'));

  els.panelClose.focus();
  document.addEventListener('keydown', onPanelKeydown, true);
}

function closePanel() {
  if (!panelContext) return;
  panelContext = null;

  document.removeEventListener('keydown', onPanelKeydown, true);
  els.panel.classList.remove('is-open');
  document.body.classList.remove('panel-locked');

  flushNotes();

  panelCloseTimer = window.setTimeout(() => {
    els.panel.classList.add('hidden');
    els.panelBody.innerHTML = '';
    panelCloseTimer = null;
  }, 340);

  if (panelReturnFocus && typeof panelReturnFocus.focus === 'function') {
    panelReturnFocus.focus();
  }
  panelReturnFocus = null;
}

const FOCUSABLE = 'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])';

function onPanelKeydown(event) {
  if (!panelContext) return;

  if (event.key === 'Escape') {
    event.preventDefault();
    closePanel();
    return;
  }
  if (event.key !== 'Tab') return;

  const focusable = [...els.panelSheet.querySelectorAll(FOCUSABLE)]
    .filter((el) => el.offsetParent !== null || el === document.activeElement);
  if (!focusable.length) return;

  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

/* ── inline previews ──────────────────────────────────────────────── */

async function togglePreview(row) {
  const doc = DOC_BY_ID.get(row.dataset.docId);
  if (!doc) return;

  const item = row.closest('.doc-item');
  const box = item.querySelector('.doc-preview');
  const toggle = row.querySelector('.doc-toggle');
  const isOpen = !box.classList.contains('hidden');

  if (isOpen) {
    box.classList.add('hidden');
    box.innerHTML = '';
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
    return;
  }

  box.classList.remove('hidden');
  if (toggle) toggle.setAttribute('aria-expanded', 'true');

  const kind = docKind(doc);
  const href = docHref(doc);

  if (kind === 'image') {
    box.innerHTML = `<img src="${escapeHtml(href)}" alt="${escapeHtml(doc.title)}" loading="lazy" />`;
    return;
  }
  if (kind === 'pdf') {
    box.innerHTML = `<iframe src="${escapeHtml(href)}" title="${escapeHtml(doc.title)}" loading="lazy"></iframe>`;
    return;
  }

  box.innerHTML = '<p class="text-sm text-ink-400 py-3 text-center">Loading…</p>';
  try {
    const response = await fetch(href, { cache: 'no-cache' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const text = await response.text();
    if (box.classList.contains('hidden')) return;   // closed while loading
    box.innerHTML = renderCsvTable(text, doc);
  } catch {
    box.innerHTML = `
      <p class="text-sm text-ink-500 py-2">
        Couldn't load this file.
        <a class="doc-link underline underline-offset-4 decoration-rose-200 text-mauve-500"
           href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer">Open it directly&nbsp;&#8599;</a>
      </p>`;
  }
}

/* ── personal notes ───────────────────────────────────────────────── */

function onNotesInput(event) {
  const field = event.target;
  if (!field.classList.contains('notes-input')) return;

  if (notesSaveTimer !== null) window.clearTimeout(notesSaveTimer);
  notesSaveTimer = window.setTimeout(() => {
    notesSaveTimer = null;
    commitNotes(field);
    flashSaved();
  }, 450);
}

function commitNotes(field) {
  const phaseId = field.dataset.phaseId;
  if (!phaseId || !VALID_PHASE_IDS.has(phaseId)) return;

  const value = field.value;
  if (value.trim() === '') delete state.notes[phaseId];
  else state.notes[phaseId] = value;

  saveState();
  updateCardHints();
}

/** Save immediately rather than waiting out the debounce (panel closing, unload). */
function flushNotes() {
  if (notesSaveTimer !== null) {
    window.clearTimeout(notesSaveTimer);
    notesSaveTimer = null;
  }
  const field = document.getElementById('panel-notes');
  if (field) commitNotes(field);
}

function flashSaved() {
  const badge = document.getElementById('panel-notes-saved');
  if (!badge) return;
  badge.classList.add('is-visible');
  if (notesFlashTimer !== null) window.clearTimeout(notesFlashTimer);
  notesFlashTimer = window.setTimeout(() => badge.classList.remove('is-visible'), 1600);
}

const LIBRARY_GLYPH = `
  <svg class="w-5 h-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"
       stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
    <path d="M3.5 5.5h5l1.5 2h6.5v8h-13z" /><path d="M3.5 9.5h13" />
  </svg>`;


function libraryCardMarkup() {
  const docs = PROJECT_DOCS || [];
  const chips = docs.slice(0, 6).map((doc) => {
    const kind = docKind(doc);
    return `
      <span class="inline-flex items-center gap-1.5 rounded-full border border-rose-200/70 bg-white/70
                   px-3 py-1.5 text-xs font-semibold ${doc.pending ? 'text-ink-400' : 'text-ink-700'}">
        <span class="w-1.5 h-1.5 rounded-full ${doc.pending ? 'bg-rose-200' : 'bg-rose-400'}"></span>
        ${escapeHtml(doc.title)}
      </span>`;
  }).join('');

  const filed = docs.filter((doc) => !doc.pending).length;

  return `
    <section class="library-card bg-white/70 backdrop-blur rounded-3xl border border-rose-200/70
                    shadow-petal hover:shadow-petal-lg transition-shadow duration-500 p-8 md:p-10"
             aria-labelledby="library-title">
      <div class="flex items-start gap-4">
        <span class="w-10 h-10 shrink-0 rounded-full bg-rose-100 text-mauve-600
                     flex items-center justify-center" aria-hidden="true">${LIBRARY_GLYPH}</span>
        <div class="flex-1 min-w-0">
          <div class="flex items-start justify-between gap-3">
            <h2 id="library-title" class="font-display font-semibold text-2xl text-ink-700 leading-snug">
              Project documents
            </h2>
            <span class="shrink-0 mt-1 text-sm text-ink-400 tabular-nums">${filed} / ${docs.length}</span>
          </div>
          <p class="text-ink-400 text-sm mt-1">Abstract, BOM, costing, diagrams — everything that spans the build.</p>
          <div class="mt-4 flex flex-wrap gap-2">${chips}</div>
        </div>
      </div>

      <button type="button" class="phase-open mt-6 pt-5 border-t border-rose-200/60" aria-haspopup="dialog"
              aria-label="Open the project document library">
        <span class="card-hint flex items-center justify-between gap-3 text-sm text-ink-400">
          <span>Open the library</span>
          <span aria-hidden="true">&#8594;</span>
        </span>
      </button>
    </section>`;
}

/** The "Notes & documents · N" line under each card, kept in sync as notes change. */
function updateCardHints() {
  for (const phase of PHASES) {
    const ref = phaseRefs.get(phase.id);
    if (!ref || !ref.hint) continue;

    const count = phaseDocCount(phase);
    const bits = [];
    bits.push(count === 1 ? '1 document' : `${count} documents`);
    if ((phase.notes || []).length || state.notes[phase.id]) bits.push('notes');
    ref.hint.textContent = bits.join(' · ');
  }
}

/* ── rendering ──────────────────────────────────────────────────── */

function renderPhases() {
  taskRefs.clear();
  phaseRefs.clear();

  els.phases.innerHTML = PHASES.map(phaseMarkup).join('');
  els.library.innerHTML = libraryCardMarkup();

  for (const phase of PHASES) {
    const card = els.phases.querySelector(`[data-phase-id="${phase.id}"]`);
    phaseRefs.set(phase.id, {
      card,
      counter: card.querySelector('.phase-counter'),
      track: card.querySelector('.phase-track'),
      fill: card.querySelector('.phase-fill'),
      badge: card.querySelector('.phase-badge'),
      hint: card.querySelector('.phase-hint'),
    });

    for (const task of phase.tasks) {
      const input = card.querySelector(`input[data-task-id="${task.id}"]`);
      const row = input.closest('.task-row');
      taskRefs.set(task.id, { row, input, title: row.querySelector('.task-title') });
    }
  }
}

/** Repaints exactly one task row — no full rebuild, so transitions survive. */
function updateTaskRow(taskId) {
  const ref = taskRefs.get(taskId);
  const task = TASK_BY_ID.get(taskId);
  if (!ref || !task) return;

  const done = isDone(task);
  ref.input.checked = done;
  ref.row.classList.toggle('is-done', done);
}

function updatePhase(phase) {
  const ref = phaseRefs.get(phase.id);
  if (!ref) return;

  const total = phase.tasks.length;
  const done = phase.tasks.filter(isDone).length;
  const pct = percent(done, total);

  ref.counter.textContent = `${done} / ${total}`;
  ref.fill.style.width = `${pct}%`;
  ref.track.setAttribute('aria-valuenow', String(pct));

  const complete = total > 0 && done === total;
  ref.card.classList.toggle('phase-complete', complete);
  ref.badge.hidden = !complete;
}

function updateOverall({ animate = true } = {}) {
  const done = ALL_TASKS.filter(isDone).length;
  const pct = percent(done, TOTAL_TASKS);

  els.fill.style.width = `${pct}%`;
  els.track.setAttribute('aria-valuenow', String(pct));
  els.count.textContent = `${done} / ${TOTAL_TASKS} ${TOTAL_TASKS === 1 ? 'task' : 'tasks'}`;

  animatePercent(pct, animate && !prefersReducedMotion());

  const finished = TOTAL_TASKS > 0 && done === TOTAL_TASKS;
  els.subheading.classList.toggle('hidden', finished);
  els.celebration.classList.toggle('hidden', !finished);
}

/** Counts the header percentage up or down over ~500ms. */
function animatePercent(target, animate) {
  stopCountAnim();

  const settle = () => {
    stopCountAnim();
    displayedPercent = target;
    els.percent.textContent = `${target}%`;
  };

  const from = displayedPercent;
  if (!animate || from === target) {
    settle();
    return;
  }

  // rAF drives the easing, but a timer guarantees the number lands on the real
  // value even if frames never arrive (background tab, throttled compositor).
  countAnimTimer = window.setTimeout(settle, COUNT_ANIM_MS + 120);

  // `start` is taken from the first frame's own timestamp, not performance.now():
  // rAF reports the frame's start time, which can predate the scheduling call and
  // would otherwise make `t` negative and send the eased value wildly out of range.
  let start = null;
  const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);

  const step = (now) => {
    if (start === null) start = now;
    const t = Math.min(1, Math.max(0, (now - start) / COUNT_ANIM_MS));
    const value = Math.round(from + (target - from) * easeOutCubic(t));
    els.percent.textContent = `${value}%`;
    displayedPercent = value;

    if (t < 1) {
      countAnimFrame = requestAnimationFrame(step);
    } else {
      settle();
    }
  };

  countAnimFrame = requestAnimationFrame(step);
}

function stopCountAnim() {
  if (countAnimFrame !== null) {
    cancelAnimationFrame(countAnimFrame);
    countAnimFrame = null;
  }
  if (countAnimTimer !== null) {
    window.clearTimeout(countAnimTimer);
    countAnimTimer = null;
  }
}

/** A single ✨ that floats up from the checkbox and disappears. */
function showSparkle(row) {
  if (!row || prefersReducedMotion()) return;

  const sparkle = document.createElement('span');
  sparkle.className = 'sparkle';
  sparkle.setAttribute('aria-hidden', 'true');
  sparkle.textContent = '✨';
  row.appendChild(sparkle);

  window.setTimeout(() => sparkle.remove(), SPARKLE_MS);
}

/* ── footer: last ticked ────────────────────────────────────────── */

function latestTickMs() {
  let latest = null;
  for (const id of Object.keys(state.completedAt)) {
    if (!VALID_IDS.has(id)) continue;
    const ms = Date.parse(state.completedAt[id]);
    if (Number.isFinite(ms) && (latest === null || ms > latest)) latest = ms;
  }
  return latest;
}

function updateLastTicked() {
  const latest = latestTickMs();
  if (latest === null) {
    els.lastTicked.classList.add('hidden');
    els.lastTicked.textContent = '';
    return;
  }
  els.lastTicked.textContent = `Last ticked: ${relativeTime(latest)}`;
  els.lastTicked.classList.remove('hidden');
}

/* ── events ─────────────────────────────────────────────────────── */

function onCardClick(event) {
  // Ticking a task must never open the panel.
  if (event.target.closest('.task-row')) return;
  if (event.target.closest('a')) return;

  const phaseCard = event.target.closest('.phase-card');
  if (phaseCard) {
    const phase = PHASES.find((candidate) => candidate.id === phaseCard.dataset.phaseId);
    if (phase) openPanel({ type: 'phase', phase });
    return;
  }
  if (event.target.closest('.library-card')) openPanel({ type: 'library' });
}

function onPanelBodyClick(event) {
  if (event.target.closest('a')) return;           // links handle themselves
  const row = event.target.closest('.doc-row[data-previewable]');
  if (row) togglePreview(row);
}



function onTaskToggle(event) {
  const input = event.target.closest('input.task-input');
  if (!input) return;

  const taskId = input.dataset.taskId;
  const task = TASK_BY_ID.get(taskId);
  if (!task) return;

  // Hardcoded completions can never be turned off.
  if (isLocked(task)) {
    input.checked = true;
    return;
  }

  if (input.checked) {
    state.completed[taskId] = true;
    state.completedAt[taskId] = new Date().toISOString();
  } else {
    delete state.completed[taskId];
    delete state.completedAt[taskId];
  }
  saveState();

  updateTaskRow(taskId);
  const phase = PHASE_BY_TASK_ID.get(taskId);
  if (phase) updatePhase(phase);
  updateOverall();
  updateLastTicked();

  if (input.checked) showSparkle(taskRefs.get(taskId)?.row);
}

function onReset() {
  const message = 'Reset your progress on this device?\n\n'
    + 'Your notes are kept, and anything already marked complete in the project file stays complete.';
  if (!window.confirm(message)) return;

  // Notes are not progress — a reset clears ticks and leaves them alone.
  const keptNotes = state.notes;
  state = emptyState();
  state.notes = keptNotes;

  if (Object.keys(keptNotes).length > 0) {
    saveState();
  } else {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch {
      /* ignore */
    }
  }

  for (const task of ALL_TASKS) updateTaskRow(task.id);
  for (const phase of PHASES) updatePhase(phase);
  updateOverall();
  updateLastTicked();
}

/* ── init ───────────────────────────────────────────────────────── */

function init() {
  els.phases = document.getElementById('phases');
  els.percent = document.getElementById('progress-percent');
  els.count = document.getElementById('progress-count');
  els.track = document.getElementById('progress-track');
  els.fill = document.getElementById('progress-fill');
  els.subheading = document.getElementById('subheading');
  els.celebration = document.getElementById('celebration');
  els.lastTicked = document.getElementById('last-ticked');
  els.reset = document.getElementById('reset-progress');
  els.library = document.getElementById('library');
  els.panel = document.getElementById('panel');
  els.panelSheet = document.getElementById('panel-sheet');
  els.panelScroll = document.getElementById('panel-scroll');
  els.panelBackdrop = document.getElementById('panel-backdrop');
  els.panelClose = document.getElementById('panel-close');
  els.panelBadge = document.getElementById('panel-badge');
  els.panelTitle = document.getElementById('panel-title');
  els.panelBlurb = document.getElementById('panel-blurb');
  els.panelBody = document.getElementById('panel-body');

  state = loadState();

  // Render everything synchronously, then paint the numbers, so nothing shifts.
  renderPhases();
  for (const phase of PHASES) updatePhase(phase);
  updateOverall();
  updateLastTicked();
  updateCardHints();

  els.phases.addEventListener('change', onTaskToggle);
  els.phases.addEventListener('click', onCardClick);
  els.library.addEventListener('click', onCardClick);
  els.reset.addEventListener('click', onReset);

  els.panelClose.addEventListener('click', closePanel);
  els.panelBackdrop.addEventListener('click', closePanel);
  els.panelBody.addEventListener('click', onPanelBodyClick);
  els.panelBody.addEventListener('input', onNotesInput);
  window.addEventListener('pagehide', flushNotes);

  // Keep "2 minutes ago" honest without a library.
  window.setInterval(updateLastTicked, CLOCK_TICK_MS);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init, { once: true });
} else {
  init();
}
