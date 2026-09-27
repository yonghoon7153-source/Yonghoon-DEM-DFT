// Cross-checks the JSON database in data/ (runs before every build: npm run data:check).
// Deliberately dependency-free; the *.schema.json files document the shapes for editors.
import { existsSync, readFileSync } from 'node:fs';

const read = (f) => JSON.parse(readFileSync(new URL(`../data/${f}`, import.meta.url), 'utf8'));
const { regions } = read('regions.json');
const { prefectures } = read('prefectures.json');
const { mascots } = read('mascots.json');
const notesDb = read('notes.json');
const geo = JSON.parse(readFileSync(new URL('../src/generated/prefecture-geo.json', import.meta.url), 'utf8'));

const errors = [];
const err = (m) => errors.push(m);
const regionIds = new Set(regions.map((r) => r.id));
const slugs = new Set();
const ids = new Set();
const mascotIds = new Set(mascots.map((m) => m.id));

if (prefectures.length !== 47) err(`prefectures: expected 47, got ${prefectures.length}`);
for (const p of prefectures) {
  const where = `prefecture ${p.id ?? '?'} (${p.slug ?? '?'})`;
  if (!Number.isInteger(p.id) || p.id < 1 || p.id > 47) err(`${where}: bad id`);
  if (ids.has(p.id)) err(`${where}: duplicate id`); ids.add(p.id);
  if (!/^[a-z]+$/.test(p.slug ?? '')) err(`${where}: bad slug`);
  if (slugs.has(p.slug)) err(`${where}: duplicate slug`); slugs.add(p.slug);
  if (!regionIds.has(p.region)) err(`${where}: unknown region "${p.region}"`);
  for (const k of ['ja', 'kana', 'romaji', 'ko', 'en']) if (!p.name?.[k]) err(`${where}: name.${k} missing`);
  if (!p.short?.ja || !p.short?.kana) err(`${where}: short.ja/kana missing`);
  if (!p.capital?.ja) err(`${where}: capital missing`);
  if (!p.hitokoto?.ja || !p.hitokoto?.ko) err(`${where}: hitokoto.ja/ko missing`);
  for (const list of ['meibutsu', 'spots']) {
    if (!Array.isArray(p[list]) || p[list].length === 0) err(`${where}: ${list} empty`);
    for (const t of p[list] ?? []) {
      if (!t.ja) err(`${where}: ${list} item without ja`);
      if (/[一-龯]/.test(t.ja) && !t.kana) err(`${where}: "${t.ja}" has kanji but no kana reading`);
    }
  }
  if (!geo[p.id]) err(`${where}: no geometry in prefecture-geo.json (run npm run geo:build)`);
  else if (geo[p.id].nameJa !== p.name.ja) err(`${where}: name.ja "${p.name.ja}" != geometry "${geo[p.id].nameJa}"`);
}
for (const m of mascots) {
  const where = `mascot ${m.id}`;
  if (!slugs.has(m.prefecture)) err(`${where}: unknown prefecture "${m.prefecture}"`);
  if (!['official', 'extra'].includes(m.kind)) err(`${where}: kind must be official|extra`);
  for (const k of ['ja', 'kana', 'ko']) if (!m.name?.[k]) err(`${where}: name.${k} missing`);
  if (!m.org) err(`${where}: org missing`);
  if (!m.about?.ja || !m.about?.ko) err(`${where}: about.ja/ko missing`);
  if (!m.line?.ja || !m.line?.ko) err(`${where}: line.ja/ko missing`);
  if (!['likeness', 'official', 'standin'].includes(m.art)) err(`${where}: art must be likeness|official|standin`);
  if ((m.art === 'official' || m.art === 'standin') && !m.credit) err(`${where}: ${m.art} art needs a credit`);
  if (m.art === 'standin' && !m.image) err(`${where}: standin art needs an image`);
  if (m.image) {
    if (m.art === 'likeness') err(`${where}: has an image but art is "likeness" (set "official" or "standin")`);
    if (!/^mascots\/[a-z]+\.(png|jpg|jpeg|webp|svg|gif)$/.test(m.image)) err(`${where}: image must look like mascots/<id>.png`);
    else if (!existsSync(new URL(`../public/${m.image}`, import.meta.url))) err(`${where}: image file public/${m.image} not found`);
  }
  if (m.url && !/^https?:\/\//.test(m.url)) err(`${where}: bad url`);
  if (m.secret) {
    const host = mascots.find((x) => x.id === m.secret);
    if (!host) err(`${where}: secret host "${m.secret}" not found`);
    else if (host.prefecture !== m.prefecture) err(`${where}: secret host must live in the same prefecture`);
    if (m.kind !== 'extra') err(`${where}: a secret mascot must be kind "extra"`);
  }
}
for (const p of prefectures) {
  const m = mascots.find((x) => x.id === p.mascot);
  if (!m) err(`prefecture ${p.slug}: mascot "${p.mascot}" not found`);
  else if (m.prefecture !== p.slug || m.kind !== 'official') err(`prefecture ${p.slug}: mascot "${p.mascot}" is not its official mascot`);
  const officials = mascots.filter((x) => x.prefecture === p.slug && x.kind === 'official');
  if (officials.length !== 1) err(`prefecture ${p.slug}: expected exactly 1 official mascot, got ${officials.length}`);
}
const mascotIdSet = new Set();
for (const m of mascots) { if (mascotIdSet.has(m.id)) err(`mascot ${m.id}: duplicate id`); mascotIdSet.add(m.id); }

// notes.json (mind-map layer)
const prefNotes = notesDb.prefectures ?? {};
for (const slug of slugs) if (!prefNotes[slug]) err(`notes: prefectures.${slug} missing (use "items": [])`);
for (const [slug, v] of Object.entries(prefNotes)) if (!slugs.has(slug)) err(`notes: unknown prefecture "${slug}"`);
for (const [rid] of Object.entries(notesDb.regions ?? {})) if (!regionIds.has(rid)) err(`notes: unknown region "${rid}"`);
let boxes = 0;
function walk(items, where, depth = 0) {
  if (!Array.isArray(items)) { err(`${where}: items must be an array`); return; }
  for (const it of items) {
    boxes++;
    if (!it || typeof it.t !== 'string' || !it.t.trim()) err(`${where}: item without "t"`);
    if (it.url && !/^https?:\/\//.test(it.url)) err(`${where}: "${it.t}" has non-http url`);
    if (it.kind && it.kind !== 'photo') err(`${where}: "${it.t}" unknown kind "${it.kind}"`);
    if (depth > 8) err(`${where}: nesting too deep at "${it.t}"`);
    if (it.children) walk(it.children, `${where} > ${it.t}`, depth + 1);
  }
}
for (const [slug, v] of Object.entries(prefNotes)) walk(v.items, `notes.${slug}`);
for (const [rid, v] of Object.entries(notesDb.regions ?? {})) if (v.items) walk(v.items, `notes.regions.${rid}`);
const extraIds = new Set();
for (const ex of notesDb.extras ?? []) {
  const where = `extra "${ex.id ?? '?'}"`;
  if (!ex.id || extraIds.has(ex.id)) err(`${where}: missing/duplicate id`); extraIds.add(ex.id);
  if (!ex.title) err(`${where}: title missing`);
  for (const r of ex.targets?.regions ?? []) if (!regionIds.has(r)) err(`${where}: unknown region target "${r}"`);
  for (const p of ex.targets?.prefectures ?? []) if (!slugs.has(p)) err(`${where}: unknown prefecture target "${p}"`);
  walk(ex.items, where);
}

if (errors.length) {
  console.error(`✗ data check failed (${errors.length}):\n  - ` + errors.join('\n  - '));
  process.exit(1);
}
console.log(`✓ data ok: ${prefectures.length} prefectures, ${regions.length} regions, ${mascots.length} mascots, ${boxes} note boxes, ${(notesDb.extras ?? []).length} extras`);
