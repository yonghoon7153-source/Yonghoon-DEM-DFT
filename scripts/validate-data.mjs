// Cross-checks the JSON database in data/ (runs before every build: npm run data:check).
// Deliberately dependency-free; the *.schema.json files document the shapes for editors.
import { existsSync, readFileSync } from 'node:fs';

const read = (f) => JSON.parse(readFileSync(new URL(`../data/${f}`, import.meta.url), 'utf8'));
const { regions, groups = [] } = read('regions.json');
const { prefectures } = read('prefectures.json');
const { mascots } = read('mascots.json');
const notesDb = read('notes.json');
const geo = JSON.parse(readFileSync(new URL('../src/generated/prefecture-geo.json', import.meta.url), 'utf8'));

const errors = [];
const err = (m) => errors.push(m);
const regionIds = new Set(regions.map((r) => r.id));
// groups (中部): a big region that only names its members — never a prefecture's region
const groupIds = new Set(groups.map((g) => g.id));
for (const g of groups) {
  if (!/^[a-z]+$/.test(g.id ?? '')) err(`regions.groups: bad id "${g.id}"`);
  if (regionIds.has(g.id)) err(`regions.groups "${g.id}": same id as a region`);
  for (const k of ['ja', 'kana', 'ko', 'en']) if (!g.name?.[k]) err(`regions.groups "${g.id}": name.${k} missing`);
}
for (const r of regions) if (r.group !== undefined && !groupIds.has(r.group)) err(`regions "${r.id}": unknown group "${r.group}"`);
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
  if (m.poke !== undefined && (!m.poke?.ja || !m.poke?.ko)) err(`${where}: poke needs ja and ko`);
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
for (const [rid] of Object.entries(notesDb.regions ?? {})) if (!regionIds.has(rid) && !groupIds.has(rid)) err(`notes: unknown region "${rid}"`);
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
  for (const r of ex.targets?.regions ?? []) if (!regionIds.has(r) && !groupIds.has(r)) err(`${where}: unknown region target "${r}"`);
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
    for (const k of Object.keys(it ?? {})) if (!['t', 'sub', 'cap', 'ko', 'photo', 'children'].includes(k)) err(`${where}: "${it.t}" unexpected key "${k}"`);
    if (it.photo !== undefined && typeof it.photo !== 'boolean' && !(typeof it.photo === 'string' && it.photo.trim())) err(`${where}: "${it.t}" photo must be true or search words`);
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
for (const kind of ['wards', 'islands', 'extraPlaces', 'lakes']) for (const x of placesDb[kind] ?? []) place(x, kind);
for (const l of placesDb.lakes ?? []) if (!l.pref) err(`places.lakes "${l.id}": pref missing`);
for (const i of placesDb.islands ?? []) if (!inJapan(i.label)) err(`places.islands "${i.id}": "label" must be [lon, lat] (the name's spot in the sea)`);
for (const e of placesDb.extraPlaces ?? []) if (e.mark && !(e.note ?? '').includes(e.mark)) err(`places.extraPlaces "${e.id}": mark "${e.mark}" is not part of the note`);
for (const e of placesDb.extraPlaces ?? []) if (e.radiusKm !== undefined && !(typeof e.radiusKm === 'number' && e.radiusKm > 0 && e.radiusKm <= 200)) err(`places.extraPlaces "${e.id}": radiusKm must be 0–200`);
for (const w of placesDb.wards ?? []) {
  if (w.note !== undefined && !(typeof w.note === 'string' && w.note.trim())) err(`places.wards "${w.id}": note must be text`);
  if (w.mark !== undefined && typeof w.mark !== 'boolean') err(`places.wards "${w.id}": mark must be true/false`);
}
// transit.json (🚄 가는 법: airports + shinkansen lines)
const transitDb = read('transit.json');
const airportIds = new Set();
for (const a of transitDb.airports ?? []) {
  const where = `transit.airports "${a.id ?? '?'}"`;
  if (!/^[a-z]{3}$/.test(a.id ?? '') || airportIds.has(a.id)) err(`${where}: bad/duplicate id`); airportIds.add(a.id);
  if (!/^[A-Z]{3}$/.test(a.iata ?? '') || a.iata.toLowerCase() !== a.id) err(`${where}: iata must be 3 capitals matching id`);
  names(a.name, where);
  if (!slugs.has(a.pref)) err(`${where}: unknown prefecture "${a.pref}"`);
  if (!inJapan(a.at)) err(`${where}: "at" must be [lon, lat] in Japan`);
  if (a.hub !== undefined && a.hub !== true) err(`${where}: hub must be true when present`);
}
const lineIds = new Set();
for (const l of transitDb.shinkansen ?? []) {
  const where = `transit.shinkansen "${l.id ?? '?'}"`;
  if (!/^[a-z-]+$/.test(l.id ?? '') || lineIds.has(l.id)) err(`${where}: bad/duplicate id`); lineIds.add(l.id);
  names(l.name, where);
  if (!/^#[0-9A-Fa-f]{6}$/.test(l.color ?? '')) err(`${where}: color must be #rrggbb`);
  if (l.kind !== undefined && !['mini', 'plan'].includes(l.kind)) err(`${where}: kind must be mini or plan`);
  if (!Array.isArray(l.stations) || l.stations.length < 2) err(`${where}: needs at least two stations`);
  for (const s of l.stations ?? []) {
    const w = `${where} station "${s.ja ?? '?'}"`;
    if (!s.ja || !inJapan(s.at)) err(`${w}: ja and [lon, lat] "at" required`);
    if (s.major && !(s.kana && s.ko && slugs.has(s.pref))) err(`${w}: a major station needs kana, ko and a known pref`);
    if (s.pref !== undefined && !slugs.has(s.pref)) err(`${w}: unknown prefecture "${s.pref}"`);
  }
}
// festivals.json (🎆 축제 달력)
const festivalsDb = read('festivals.json');
const festivalIds = new Set();
const MMDD = /^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$/;
for (const f of festivalsDb.festivals ?? []) {
  const where = `festivals "${f.id ?? '?'}"`;
  if (!/^[a-z0-9-]+$/.test(f.id ?? '') || festivalIds.has(f.id)) err(`${where}: bad/duplicate id`); festivalIds.add(f.id);
  for (const k of ['ja', 'kana', 'ko']) if (!f[k]) err(`${where}: ${k} missing`);
  if (!slugs.has(f.pref)) err(`${where}: unknown prefecture "${f.pref}"`);
  if (!MMDD.test(f.start ?? '')) err(`${where}: start must be MM-DD`);
  if (f.end !== undefined && !MMDD.test(f.end)) err(`${where}: end must be MM-DD`);
  if (f.kind !== undefined && f.kind !== 'season') err(`${where}: kind must be season`);
  if (!['fireworks', 'snow', 'sakura', 'momiji', 'lanterns', 'drums', 'streamers'].includes(f.fx)) err(`${where}: fx must name an effect`);
  if (f.approx !== undefined && typeof f.approx !== 'boolean') err(`${where}: approx must be true/false`);
}
// landmarks.json (확대하면 붙는 랜드마크 스티커, ADR 0011): the box must be one of that prefecture's boxes — or, instead, the
// spot one of its 기본 정보 観光 (#93) — the point inside its box (bbox, dependency-free — the full check against the shapes
// was done once when the points were written), the icon drawn
const landmarksDb = read('landmarks.json');
const okinawaShift = JSON.parse(readFileSync(new URL('../public/geo/japan.topo.json', import.meta.url), 'utf8')).meta?.okinawaShift ?? [0, 0];
const artSrc = ['art-a.ts', 'art-b.ts', 'art-c.ts', 'art-d.ts', 'art-e.ts', 'art-f.ts'].map((f) => readFileSync(new URL(`../src/landmarks/${f}`, import.meta.url), 'utf8')).join('\n');
const artIds = new Set([...artSrc.matchAll(/^ {2}([a-z]+): /gm)].map((m) => m[1]));
const boxesOf = (slug) => {
  const out = new Set();
  const walkT = (items) => { for (const it of items ?? []) { out.add(it.t); walkT(it.children); } };
  walkT(notesDb.prefectures?.[slug]?.items);
  walkT(supDb.prefectures?.[slug]?.items);
  return out;
};
const wardNames = new Set((placesDb.wards ?? []).map((w) => w.name.ja));
const prefIdBySlug = new Map(prefectures.map((p) => [p.slug, p.id]));
const landmarkIds = new Set();
const landmarkSpots = new Set();
for (const l of landmarksDb.landmarks ?? []) {
  const where = `landmarks "${l.id ?? '?'}"`;
  if (!/^[a-z0-9-]+$/.test(l.id ?? '') || landmarkIds.has(l.id)) err(`${where}: bad/duplicate id`); landmarkIds.add(l.id);
  names(l.name, where);
  if (!slugs.has(l.pref)) { err(`${where}: unknown prefecture "${l.pref}"`); continue; }
  if ((l.box === undefined) === (l.spot === undefined)) err(`${where}: exactly one of box / spot`);
  else if (l.box !== undefined && !boxesOf(l.pref).has(l.box)) err(`${where}: no box "${l.box}" in ${l.pref} (내 마인드맵 · 보충)`);
  else if (l.spot !== undefined && !prefectures.find((p) => p.slug === l.pref)?.spots?.some((t) => t.ja === l.spot)) err(`${where}: no 観光 spot "${l.spot}" in ${l.pref} (prefectures.json)`);
  if (l.spot !== undefined) { if (landmarkSpots.has(`${l.pref}|${l.spot}`)) err(`${where}: spot "${l.spot}" has a sticker already`); landmarkSpots.add(`${l.pref}|${l.spot}`); }
  if (!artIds.has(l.icon)) err(`${where}: no drawing "${l.icon}" in src/landmarks`);
  if (l.ward !== undefined && (l.pref !== 'tokyo' || !wardNames.has(l.ward))) err(`${where}: ward only for 東京, one of places.json wards`);
  const b = geo[prefIdBySlug.get(l.pref)]?.bbox;
  // 沖縄 is drawn in the inset (its bbox too), moved by the map's okinawaShift — and without 宮古 · 八重山
  const [x, y] = l.pref === 'okinawa' && inJapan(l.at) ? [l.at[0] + okinawaShift[0], l.at[1] + okinawaShift[1]] : l.at ?? [];
  if (!inJapan(l.at) || !b || x < b[0] - 0.05 || x > b[2] + 0.05 || y < b[1] - 0.05 || y > b[3] + 0.05) err(`${where}: at [lon, lat] is not in ${l.pref}`);
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
console.log(`✓ data ok: ${prefectures.length} prefectures, ${regions.length} regions (+${groups.length} group), ${mascots.length} mascots, ${boxes} note boxes, ${(notesDb.extras ?? []).length} extras, ${supBoxes} supplement boxes, ${(placesDb.cities ?? []).length} cities, ${(mountainsDb.ranges ?? []).length} ranges, ${(transitDb.airports ?? []).length} airports, ${(transitDb.shinkansen ?? []).length} shinkansen lines, ${(festivalsDb.festivals ?? []).length} festivals, ${(landmarksDb.landmarks ?? []).length} landmarks`);
