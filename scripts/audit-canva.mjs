// Canva 전수조사: every line of text in my Canva PDF (data/raw/canva-text.json) must be somewhere in the site's data.
//   node scripts/audit-canva.mjs          check (exit 1 when a line is missing)
//   node scripts/audit-canva.mjs --list   also print where each line went, and note text that is not in the PDF
//
// Matching is deliberately strict — no fuzzy "somewhere in the haystack":
//   - a line is used up by a data field that contains it, and a note field can take a piece of text only as many
//     times as the text occurs in it (the PDF saying 「高い」 four times needs four 「高い」 in the data);
//   - names (prefectures, regions, cities, wards, ranges, directions, mascots, UI titles) may take any number of
//     copies, because the PDF repeats them on its maps and in its boxes;
//   - a line that is not found whole is split at brackets and commas, and every piece must be found.
// Lines that are knowingly not in the data are listed with a reason in data/raw/canva-audit.json.
import { readFileSync } from 'node:fs';

const read = (p) => readFileSync(new URL(`../${p}`, import.meta.url), 'utf8');
const J = (p) => JSON.parse(read(p));
const list = process.argv.includes('--list');

const norm = (s) => (s ?? '').normalize('NFKC').replace(/[\s()（）［］\[\]「」『』"“”'`]/g, '').toLowerCase();
const SPLIT = /[()（）,，、/／+]|\s{2,}/;
const trivial = (n) => !n || /^[・,.\-~→←↑↓+·…:;!?]+$/u.test(n);

// ------------------------------------------------------------------ what the site knows
const fields = []; // { n, rest, where, reusable, exact }
const add = (s, where, reusable, exact = false) => {
  if (typeof s === 'string' && norm(s)) fields.push({ n: norm(s), rest: norm(s), where, reusable, exact });
};
const names = (o, where) => { for (const [k, v] of Object.entries(o ?? {})) add(v, `${where}.${k}`, true); };
function walk(items, where) {
  for (const it of items ?? []) {
    const w = `${where} > ${it.t}`;
    for (const k of ['t', 'sub', 'cap', 'ko']) add(it[k], `${w} [${k}]`, false);
    walk(it.children, w);
  }
}
const notes = J('data/notes.json');
for (const [slug, v] of Object.entries(notes.prefectures)) {
  if (v.root) names(v.root, `notes.${slug}.root`);
  walk(v.items, `notes.${slug}`);
}
for (const [rid, v] of Object.entries(notes.regions ?? {})) { add(v.memo, `notes.regions.${rid} [memo]`, false); walk(v.items, `notes.regions.${rid}`); }
for (const e of notes.extras ?? []) { add(e.title, `extra ${e.id} [title]`, false); add(e.sub, `extra ${e.id} [sub]`, false); walk(e.items, `extra ${e.id}`); }
for (const p of J('data/prefectures.json').prefectures) {
  names(p.name, `pref ${p.slug} name`);
  add(p.name.ko.replace(/[현부도]$/, ''), `pref ${p.slug} name.ko (short)`, true);
  names(p.short, `pref ${p.slug} short`);
  names(p.capital, `pref ${p.slug} capital`);
}
const regionsDb = J('data/regions.json');
for (const r of [...regionsDb.regions, ...(regionsDb.groups ?? [])]) {
  names(r.name, `region ${r.id}`);
  add(`${r.name.ja}地方`, `region ${r.id} label`, true);
  add(`${r.name.kana}ちほう`, `region ${r.id} label.kana`, true);
}
const places = J('data/places.json');
for (const kind of ['cities', 'wards', 'islands', 'lakes', 'extraPlaces', 'bridges']) {
  for (const x of places[kind] ?? []) {
    const w = `places.${kind} ${x.id}`;
    names(x.name, `${w} name`);
    add(x.note, `${w} note`, false);
    if (x.route) names(x.route, `${w} route`);
    add(x.ko, `${w} ko`, false);
  }
}
for (const m of places.mapNotes ?? []) add(m.t, `places.mapNotes ${m.id}`, false);
for (const c of places.compass ?? []) for (const w of c.words) names(w, `places.compass ${c.id}`);
const mountains = J('data/mountains.json');
for (const r of mountains.ranges) names(r.name, `mountains.ranges ${r.no}`);
for (const n of mountains.notes) { add(n.t, `mountains.notes ${n.id} t`, false); add(n.sub, `mountains.notes ${n.id} sub`, false); }
// mascot names only count whole: 「치바」 is not in 「치바쿤」
for (const m of J('data/mascots.json').mascots) for (const [k, v] of Object.entries(m.name)) add(v, `mascot ${m.id}.${k}`, true, true);
for (const m of read('index.html').matchAll(/(?:title|aria-label)="([^"]+)"/g)) add(m[1], 'index.html', true);

// ------------------------------------------------------------------ use the PDF lines up
function absorb(n) {
  const f =
    fields.find((x) => !x.reusable && x.rest === n) ??
    fields.find((x) => x.reusable && x.n === n) ??
    fields.filter((x) => !x.exact && (x.reusable ? x.n : x.rest).includes(n)).sort((a, b) => (a.reusable ? a.n : a.rest).length - (b.reusable ? b.n : b.rest).length)[0];
  if (!f) return null;
  if (!f.reusable) f.rest = f.rest.replace(n, '#');
  return f.where;
}
const { spans } = J('data/raw/canva-text.json');
const lines = spans.map(([t, x, y, size, color]) => ({ t, x, y, size, color }));
const res = new Map();
for (const l of [...lines].sort((a, b) => norm(b.t).length - norm(a.t).length)) {
  const n = norm(l.t);
  if (trivial(n)) { res.set(l, 'trivial'); continue; }
  const whole = absorb(n);
  if (whole) { res.set(l, whole); continue; }
  const parts = l.t.normalize('NFKC').split(SPLIT).map(norm).filter((q) => !trivial(q));
  // all pieces of one line are tried together; a line that fails gives back what it had taken
  const saved = fields.map((f) => f.rest);
  const got = [];
  let miss = null;
  for (const q of parts) {
    const w = absorb(q);
    if (!w) { miss = q; break; }
    got.push(w);
  }
  if (miss !== null || !got.length) fields.forEach((f, i) => { f.rest = saved[i]; });
  res.set(l, miss === null && got.length ? got.join(' ; ') : { miss: miss ?? n });
}

// ------------------------------------------------------------------ report
const { accepted } = J('data/raw/canva-audit.json');
const known = new Map(accepted.map((a) => [a.t, a]));
const missing = lines.filter((l) => typeof res.get(l) === 'object');
const unexplained = missing.filter((l) => !known.has(l.t));
const pending = missing.filter((l) => known.get(l.t)?.state === 'pending');
const stale = accepted.filter((a) => !missing.some((l) => l.t === a.t));

if (list) {
  for (const l of lines) console.log(`${String(Math.round(l.x)).padStart(4)},${String(Math.round(l.y)).padStart(3)}  ${l.t}  →  ${typeof res.get(l) === 'object' ? '✗ ' + (known.get(l.t)?.why ?? 'MISSING') : res.get(l)}`);
  console.log('\n— note text in the data that is not in the PDF (additions, or text found under another box):');
  for (const f of fields.filter((x) => !x.reusable)) {
    const left = f.rest.replace(/#/g, '').replace(/[・,.\-~→←↑↓+·…:;!?=—–]/g, '');
    if (left.length >= 2) console.log(`  ${f.where}: "${left}"`);
  }
}
for (const a of stale) console.log(`  ⚠ canva-audit.json 의 「${a.t}」 는 이제 데이터에 있어요 — 목록에서 지워도 됩니다`);
if (unexplained.length) {
  console.error(`✗ Canva 전수조사: PDF 글줄 ${lines.length}줄 중 ${unexplained.length}줄이 데이터에 없어요`);
  for (const l of unexplained) console.error(`  - (${Math.round(l.x)}, ${Math.round(l.y)}) 「${l.t}」 — 없는 조각: ${res.get(l).miss}`);
  console.error('  데이터에 넣거나, 일부러 뺀 거면 data/raw/canva-audit.json 에 이유와 함께 적어요.');
  process.exit(1);
}
const found = lines.length - missing.length;
console.log(`✓ Canva 전수조사: PDF 글줄 ${lines.length}줄 — ${found}줄 데이터에 있음, ${missing.length - pending.length}줄 이유 있음${pending.length ? `, ${pending.length}줄 확인 기다리는 중` : ''}`);
