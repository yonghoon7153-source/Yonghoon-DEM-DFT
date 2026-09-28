// Builds the simplified map used by the site from data/raw/japan.topojson.
//   node scripts/build-geo.mjs
// Output:
//   public/geo/japan.topo.json         simplified TopoJSON (fetched by the app) — objects.japan (prefectures) + objects.lakes (琵琶湖)
//                                      + objects.cities (city outlines: 政令指定都市 20 + the other 48 mapped cities, from data/raw/city-areas.geojson)
//   src/generated/prefecture-geo.json  per-prefecture label anchor + bbox (lon/lat)
//   public/geo/tokyo23.topo.json       Tokyo's 23 wards for the 23区 popup (from data/raw/tokyo23.geojson)
//
// Cartographic decisions (documented so they are easy to revisit):
//   - Visvalingam simplification keeps borders shared between prefectures consistent.
//   - Islets under MIN_RING_AREA are dropped unless they touch another ring.
//   - Ogasawara (Tokyo, south of 30°N) is dropped: it would push the map 7° south for a few dots.
//   - Okinawa's far-flung islands are dropped — Miyako/Yaeyama (west of 126.5°E) and the Daito islands
//     (east of 129°E; shifted with the rest they would land on the tip of Kagoshima) — and the main
//     island group is moved into a small inset box off the west coast of Kyushu (OKINAWA_SHIFT).
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { presimplify, simplify, quantile, filter, filterAttachedWeight, sphericalRingArea } from 'topojson-simplify';
import { feature } from 'topojson-client';
import { topology } from 'topojson-server';
import pc from 'polygon-clipping';
import { geoArea, geoBounds, geoCentroid } from 'd3-geo';

const SRC = new URL('../data/raw/japan.topojson', import.meta.url);
const LAKES = new URL('../data/raw/lakes.geojson', import.meta.url); // Natural Earth 10m lakes, public domain
const CITIES = new URL('../data/raw/city-areas.geojson', import.meta.url); // 国土数値情報 via smartnews-smri, credit in the footer
const OUT_TOPO = new URL('../public/geo/japan.topo.json', import.meta.url);
const OUT_META = new URL('../src/generated/prefecture-geo.json', import.meta.url);

const SIMPLIFY_Q = 0.15;      // drop the 15% least significant points
const MIN_RING_AREA = 6e-8;   // steradians, ≈ 2.4 km²
export const OKINAWA_SHIFT = [-0.6, 5.4]; // [dLon, dLat] applied to Okinawa in the inset
const OKINAWA_ID = 47, TOKYO_ID = 13;

const topo = JSON.parse(readFileSync(SRC, 'utf8'));

// 1. Simplify + islet filter on the shared topology.
let simplified = presimplify(topo);
simplified = simplify(simplified, quantile(simplified, SIMPLIFY_Q));
simplified = filter(simplified, filterAttachedWeight(simplified, MIN_RING_AREA, sphericalRingArea));

// 2. Per-prefecture polygon edits need plain GeoJSON.
const fc = feature(simplified, simplified.objects.japan);
const meta = {};
const features = [];
for (const f of fc.features) {
  const id = f.properties.id;
  let polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
  if (id === TOKYO_ID) polys = polys.filter((p) => geoCentroid({ type: 'Polygon', coordinates: p })[1] > 30);
  if (id === OKINAWA_ID) {
    polys = polys
      .filter((p) => { const lon = geoCentroid({ type: 'Polygon', coordinates: p })[0]; return lon > 126.5 && lon < 129; })
      .map((p) => p.map((ring) => ring.map(([x, y]) => [x + OKINAWA_SHIFT[0], y + OKINAWA_SHIFT[1]])));
  }
  let best = null, bestArea = -1;
  for (const p of polys) {
    const a = geoArea({ type: 'Polygon', coordinates: p });
    if (a > bestArea) { bestArea = a; best = p; }
  }
  const anchor = geoCentroid({ type: 'Polygon', coordinates: best });
  const geometry = { type: 'MultiPolygon', coordinates: polys };
  const bounds = geoBounds(geometry);
  // "core" bbox ignores far-flung islands so zoom-to-fit stays useful.
  const core = polys.filter((p) => {
    const c = geoCentroid({ type: 'Polygon', coordinates: p });
    return Math.abs(c[0] - anchor[0]) < 2.5 && Math.abs(c[1] - anchor[1]) < 2.5;
  });
  const cb = geoBounds({ type: 'MultiPolygon', coordinates: core });
  meta[id] = {
    id,
    nameJa: f.properties.nam_ja,
    anchor: [round(anchor[0]), round(anchor[1])],
    bbox: [round(bounds[0][0]), round(bounds[0][1]), round(bounds[1][0]), round(bounds[1][1])],
    coreBbox: [round(cb[0][0]), round(cb[0][1]), round(cb[1][0]), round(cb[1][1])],
    areaSr: Number(bestArea.toExponential(3)),
    polygons: polys.length,
  };
  features.push({ type: 'Feature', id, properties: { id, ja: f.properties.nam_ja }, geometry });
}

// 3. Re-encode as TopoJSON (shared arcs again) and quantize so the file is small.
const lakes = JSON.parse(readFileSync(LAKES, 'utf8'));
// city outlines: simplify like the prefectures so the dotted lines stay light; Okinawa's cities move into the inset with the prefecture
const cityFc = JSON.parse(readFileSync(CITIES, 'utf8'));
for (const f of cityFc.features) {
  if (f.properties.pref !== 'okinawa') continue;
  const mv = (c) => Array.isArray(c[0]) ? c.map(mv) : [round(c[0] + OKINAWA_SHIFT[0]), round(c[1] + OKINAWA_SHIFT[1])];
  f.geometry.coordinates = mv(f.geometry.coordinates);
}
let citiesT = presimplify(topology({ cities: cityFc }));
citiesT = simplify(citiesT, quantile(citiesT, 0.25));
const cities = feature(citiesT, citiesT.objects.cities);

// 3b. Fit every city to its prefecture's final shape. The city outlines come from another source (国土数値情報) with its own
// simplification, so along the 県 border and the coast they ran a little beside the prefecture line ("점선이 잘 안 맞는데").
// Vertices within SNAP_EPS of the 県 border are pulled onto it, the border is traced between them, and what still sticks out is cut off —
// so the dotted city line sits exactly on the 県 line there (and hides under its stroke), and only the inland borders show.
const SNAP_EPS = 0.012; // degrees, ≈ 1.2 km
const prefIdBySlug = new Map(JSON.parse(readFileSync(new URL('../data/prefectures.json', import.meta.url), 'utf8')).prefectures.map((p) => [p.slug, p.id]));
const prefRingsById = new Map(features.map((f) => [f.id, f.geometry.coordinates.flat()])); // every ring (outer + holes) of every polygon
const prefPolysById = new Map(features.map((f) => [f.id, f.geometry.coordinates]));
function nearestOnSegment(p, a, b) {
  const dx = b[0] - a[0], dy = b[1] - a[1];
  const l2 = dx * dx + dy * dy;
  const t = l2 === 0 ? 0 : Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l2));
  const q = [a[0] + t * dx, a[1] + t * dy];
  return { q, t, d: Math.hypot(p[0] - q[0], p[1] - q[1]) };
}
const plen = (pts) => pts.reduce((acc, q, i) => (i ? acc + Math.hypot(q[0] - pts[i - 1][0], q[1] - pts[i - 1][1]) : 0), 0);
/** The 県 ring's own vertices between two snapped points, going forward (dir 1) or backward (dir -1). */
function between(ring, a, b, dir) {
  const n = ring.length - 1; // closed ring: last === first
  const verts = [];
  if (dir > 0) {
    let cnt = (((b.si - a.si) % n) + n) % n;
    if (cnt === 0 && a.t > b.t) cnt = n;
    for (let j = 0; j < cnt; j++) verts.push(ring[(a.si + 1 + j) % n]);
  } else {
    let cnt = (((a.si - b.si) % n) + n) % n;
    if (cnt === 0 && a.t < b.t) cnt = n;
    for (let j = 0; j < cnt; j++) verts.push(ring[(((a.si - j) % n) + n) % n]);
  }
  return verts;
}
function fitRing(ring, prefRings) {
  const snapped = ring.slice(0, -1).map((p) => {
    let best = null;
    prefRings.forEach((pr, ri) => {
      for (let i = 0; i < pr.length - 1; i++) {
        const r = nearestOnSegment(p, pr[i], pr[i + 1]);
        if (r.d < SNAP_EPS && (!best || r.d < best.d)) best = { p: r.q, t: r.t, d: r.d, ri, si: i };
      }
    });
    return best ?? { p };
  });
  const out = [];
  for (let i = 0; i < snapped.length; i++) {
    const a = snapped[i], b = snapped[(i + 1) % snapped.length];
    out.push(a.p);
    if (a.ri === undefined || a.ri !== b.ri) continue;
    const pr = prefRings[a.ri];
    const chord = Math.hypot(a.p[0] - b.p[0], a.p[1] - b.p[1]);
    const cands = [between(pr, a, b, 1), between(pr, a, b, -1)].map((v) => ({ v, len: plen([a.p, ...v, b.p]) })).sort((x, y) => x.len - y.len);
    if (cands[0].len <= 3 * chord + SNAP_EPS) out.push(...cands[0].v);
  }
  // drop repeated points, close the ring
  const clean = out.filter((q, i) => i === 0 || q[0] !== out[i - 1][0] || q[1] !== out[i - 1][1]);
  if (clean.length && (clean[0][0] !== clean[clean.length - 1][0] || clean[0][1] !== clean[clean.length - 1][1])) clean.push(clean[0]);
  return clean.length >= 4 ? clean : null;
}
let fitted = 0;
for (const c of cities.features) {
  const id = prefIdBySlug.get(c.properties.pref);
  const prefRings = prefRingsById.get(id), prefPolys = prefPolysById.get(id);
  if (!prefRings) continue;
  const polys = c.geometry.type === 'Polygon' ? [c.geometry.coordinates] : c.geometry.coordinates;
  const fittedPolys = polys.map((rings) => rings.map((r) => fitRing(r, prefRings)).filter(Boolean)).filter((rings) => rings.length);
  const cut = pc.intersection(fittedPolys, prefPolys);
  // a city that lies wholly outside the simplified prefecture (浦安市: reclaimed land the coast no longer reaches) gets no outline
  if (!cut.length) { console.warn(`no outline — city lies outside its simplified prefecture: ${c.properties.ja}`); c.geometry = null; continue; }
  // polygon-clipping winds rings the planar way; d3-geo reads a ring wound the other way as the rest of the globe → rewind
  const wound = cut.map((rings) => (geoArea({ type: 'Polygon', coordinates: rings }) > 2 * Math.PI ? rings.map((r) => r.slice().reverse()) : rings));
  c.geometry = { type: 'MultiPolygon', coordinates: wound };
  fitted++;
}
cities.features = cities.features.filter((c) => c.geometry);
console.log(`cities fitted to their prefecture: ${fitted}, kept ${cities.features.length}`);
const out = topology({ japan: { type: 'FeatureCollection', features }, lakes, cities }, 1e4);
out.meta = { okinawaShift: OKINAWA_SHIFT, source: '地球地図日本（国土地理院） via dataofjapan/land' };

mkdirSync(new URL('../public/geo/', import.meta.url), { recursive: true });
mkdirSync(new URL('../src/generated/', import.meta.url), { recursive: true });
writeFileSync(OUT_TOPO, JSON.stringify(out));
writeFileSync(OUT_META, JSON.stringify(meta, null, 2) + '\n');

const size = Buffer.byteLength(JSON.stringify(out));
console.log(`arcs: ${topo.arcs.length} -> ${out.arcs.length}, output ${(size / 1024).toFixed(0)} KB, prefectures: ${features.length}`);

// 4. Tokyo's 23 wards (都区部) — same source (地球地図日本 via dataofjapan/land, full-precision GeoJSON subset),
//    lightly simplified: the 23区 popup is a few hundred pixels wide, 26k points would only weigh it down.
const wardsFc = JSON.parse(readFileSync(new URL('../data/raw/tokyo23.geojson', import.meta.url), 'utf8'));
if (wardsFc.features.length !== 23) throw new Error(`expected 23 wards, got ${wardsFc.features.length}`);
let t23s = presimplify(topology({ wards: wardsFc }));
t23s = simplify(t23s, quantile(t23s, 0.2)); // keep the 20% most significant points
const t23 = topology({ wards: feature(t23s, t23s.objects.wards) }, 1e4);
t23.meta = { source: '地球地図日本（国土地理院） via dataofjapan/land' };
writeFileSync(new URL('../public/geo/tokyo23.topo.json', import.meta.url), JSON.stringify(t23));
console.log(`tokyo23: ${wardsFc.features.length} wards, ${(Buffer.byteLength(JSON.stringify(t23)) / 1024).toFixed(0)} KB`);
function round(x) { return Math.round(x * 1e4) / 1e4; }
