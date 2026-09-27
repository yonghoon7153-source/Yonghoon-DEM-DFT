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
for (const [slug, v] of Object.entries(prefNotes)) {
  if (v.root === undefined) continue;
  if (typeof v.root !== 'object' || !Object.keys(v.root).length) err(`notes.${slug}: root must be { ja?, ko? }`);
  for (const [k, x] of Object.entries(v.root ?? {})) if (!['ja', 'ko'].includes(k) || typeof x !== 'string' || !x.trim()) err(`notes.${slug}: root.${k} must be text (ja/ko)`);
}
for (const [rid] of Object.entries(notesDb.regions ?? {})) if (!regionIds.has(rid)) err(`notes: unknown region "${rid}"`);
let boxes = 0;
function walk(items, where, depth = 0) {
  if (!Array.isArray(items)) { err(`${where}: items must be an array`); return; }
  for (const it of items) {
    boxes++;
    if (!it || typeof it.t !== 'string' || !it.t.trim()) err(`${where}: item without "t"`);
    if (it.url && !/^https?:\/\//.test(it.url)) err(`${where}: "${it.t}" has non-http url`);
    if (it.kind && it.kind !== 'photo') err(`${where}: "${it.t}" unknown kind "${it.kind}"`);
    if (it.photo !== undefined && typeof it.photo !== 'boolean' && !(typeof it.photo === 'string' && it.photo.trim())) err(`${where}: "${it.t}" photo must be true or search words`);
    if (it.gloss !== undefined && !(typeof it.gloss === 'string' && /[가-힯]/.test(it.gloss))) err(`${where}: "${it.t}" gloss must be Korean text`);
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

// supplement.json (Claude's boxes for prefectures without notes — never mixed into notes.json)
const supDb = read('supplement.json');
let supBoxes = 0;
function walkSup(items, where, depth = 0) {
  if (!Array.isArray(items)) { err(`${where}: items must be an array`); return; }
  for (const it of items) {
    supBoxes++;
    if (!it || typeof it.t !== 'string' || !it.t.trim()) err(`${where}: item without "t"`);
    for (const k of Object.keys(it ?? {})) if (!['t', 'sub', 'cap', 'ko', 'children'].includes(k)) err(`${where}: "${it.t}" unexpected key "${k}"`);
    if (depth > 4) err(`${where}: nesting too deep at "${it.t}"`);
    if (it.children) walkSup(it.children, `${where} > ${it.t}`, depth + 1);
  }
}
for (const [slug, v] of Object.entries(supDb.prefectures ?? {})) {
  if (!slugs.has(slug)) err(`supplement: unknown prefecture "${slug}"`);
  walkSup(v.items, `supplement.${slug}`);
}

// places.json / mountains.json (map layers). Coordinates are [lon, lat] inside Japan's box.
const inJapan = (at) => Array.isArray(at) && at.length === 2 && at[0] >= 122 && at[0] <= 154 && at[1] >= 20 && at[1] <= 46;
const names = (n, where) => {
  for (const k of ['ja', 'kana', 'ko']) if (!n?.[k]) err(`${where}: name.${k} missing`);
  if (n?.official !== undefined && !(typeof n.official === 'string' && n.official.trim())) err(`${where}: name.official must be text`);
};
const placesDb = read('places.json');
const placeIds = new Set();
const place = (x, kind) => {
  const where = `places.${kind} "${x.id ?? '?'}"`;
  if (!x.id || placeIds.has(`${kind}:${x.id}`)) err(`${where}: missing/duplicate id`); placeIds.add(`${kind}:${x.id}`);
  names(x.name, where);
  if (!inJapan(x.at)) err(`${where}: "at" must be [lon, lat] in Japan`);
  if (x.pref !== undefined && !slugs.has(x.pref)) err(`${where}: unknown prefecture "${x.pref}"`);
};
for (const c of placesDb.cities ?? []) { place(c, 'cities'); if (typeof c.capital !== 'boolean' || typeof c.fromUser !== 'boolean') err(`places.cities "${c.id}": capital/fromUser must be booleans`); if (!c.pref) err(`places.cities "${c.id}": pref missing`); }
for (const kind of ['wards', 'islands', 'extraPlaces']) for (const x of placesDb[kind] ?? []) place(x, kind);
for (const i of placesDb.islands ?? []) if (!inJapan(i.label)) err(`places.islands "${i.id}": "label" must be [lon, lat] (the name's spot in the sea)`);
for (const e of placesDb.extraPlaces ?? []) if (e.mark && !(e.note ?? '').includes(e.mark)) err(`places.extraPlaces "${e.id}": mark "${e.mark}" is not part of the note`);
for (const e of placesDb.extraPlaces ?? []) if (e.radiusKm !== undefined && !(typeof e.radiusKm === 'number' && e.radiusKm > 0 && e.radiusKm <= 200)) err(`places.extraPlaces "${e.id}": radiusKm must be 0–200`);
for (const w of placesDb.wards ?? []) {
  if (w.note !== undefined && !(typeof w.note === 'string' && w.note.trim())) err(`places.wards "${w.id}": note must be text`);
  if (w.mark !== undefined && typeof w.mark !== 'boolean') err(`places.wards "${w.id}": mark must be true/false`);
}
const noteIds = new Set();
for (const m of placesDb.mapNotes ?? []) {
  const where = `places.mapNotes "${m.id ?? '?'}"`;
  if (!m.id || noteIds.has(m.id)) err(`${where}: missing/duplicate id`); noteIds.add(m.id);
  if (!m.t || !inJapan(m.at)) err(`${where}: t and [lon, lat] "at" required`);
  if (m.pref !== undefined && !slugs.has(m.pref)) err(`${where}: unknown prefecture "${m.pref}"`);
}
const sides = new Set();
for (const c of placesDb.compass ?? []) {
  const where = `places.compass "${c.id ?? '?'}"`;
  if (!['top', 'right', 'bottom', 'left'].includes(c.side)) err(`${where}: side must be top/right/bottom/left`);
  if (sides.has(c.side)) err(`${where}: side "${c.side}" used twice`); sides.add(c.side);
  if (!Array.isArray(c.words) || !c.words.length) err(`${where}: words missing`);
  for (const w of c.words ?? []) for (const k of ['ja', 'kana', 'ko']) if (!w?.[k]) err(`${where}: word.${k} missing`);
}
for (const b of placesDb.bridges ?? []) {
  const where = `places.bridges "${b.id ?? '?'}"`;
  names(b.name, where);
  if (!Array.isArray(b.line) || b.line.length < 2 || !b.line.every(inJapan)) err(`${where}: line must be ≥2 [lon, lat] points`);
  if (!/^#[0-9a-f]{6}$/i.test(b.color ?? '')) err(`${where}: color must be #rrggbb`);
  if (b.kind !== undefined && !['tunnel', 'plan'].includes(b.kind)) err(`${where}: kind must be tunnel or plan (or left out for a bridge)`);
}
const capitals = (placesDb.cities ?? []).filter((c) => c.capital).length;
if ((placesDb.cities ?? []).length && capitals !== 47) err(`places.cities: expected 47 capitals, got ${capitals}`);
const mountainsDb = read('mountains.json');
const nos = new Set();
for (const r of mountainsDb.ranges ?? []) {
  const where = `mountains.ranges ${r.no ?? '?'} (${r.id ?? '?'})`;
  if (!Number.isInteger(r.no) || nos.has(r.no)) err(`${where}: missing/duplicate no`); nos.add(r.no);
  names(r.name, where);
  if (!['山脈', '山地', '高地'].includes(r.kind)) err(`${where}: kind must be 山脈/山地/高地`);
  if (!Array.isArray(r.line) || r.line.length < 2 || !r.line.every(inJapan)) err(`${where}: line must be ≥2 [lon, lat] points`);
}
for (const n of mountainsDb.notes ?? []) {
  if (!n.t || !inJapan(n.at)) err(`mountains.notes "${n.id ?? '?'}": t and [lon, lat] "at" required`);
  if (n.arrow && !(n.arrow.length >= 2 && n.arrow.every(inJapan))) err(`mountains.notes "${n.id}": arrow must be ≥2 points`);
}

if (errors.length) {
  console.error(`✗ data check failed (${errors.length}):\n  - ` + errors.join('\n  - '));
  process.exit(1);
}
console.log(`✓ data ok: ${prefectures.length} prefectures, ${regions.length} regions, ${mascots.length} mascots, ${boxes} note boxes, ${(notesDb.extras ?? []).length} extras, ${supBoxes} supplement boxes, ${(placesDb.cities ?? []).length} cities, ${(mountainsDb.ranges ?? []).length} ranges`);
