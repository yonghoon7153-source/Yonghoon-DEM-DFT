// Builds the simplified map used by the site from data/raw/japan.topojson.
//   node scripts/build-geo.mjs
// Output:
//   public/geo/japan.topo.json         simplified TopoJSON (fetched by the app)
//   src/generated/prefecture-geo.json  per-prefecture label anchor + bbox (lon/lat)
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
import { geoArea, geoBounds, geoCentroid } from 'd3-geo';

const SRC = new URL('../data/raw/japan.topojson', import.meta.url);
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
const out = topology({ japan: { type: 'FeatureCollection', features } }, 1e4);
out.meta = { okinawaShift: OKINAWA_SHIFT, source: '地球地図日本（国土地理院） via dataofjapan/land' };

mkdirSync(new URL('../public/geo/', import.meta.url), { recursive: true });
mkdirSync(new URL('../src/generated/', import.meta.url), { recursive: true });
writeFileSync(OUT_TOPO, JSON.stringify(out));
writeFileSync(OUT_META, JSON.stringify(meta, null, 2) + '\n');

const size = Buffer.byteLength(JSON.stringify(out));
console.log(`arcs: ${topo.arcs.length} -> ${out.arcs.length}, output ${(size / 1024).toFixed(0)} KB, prefectures: ${features.length}`);
function round(x) { return Math.round(x * 1e4) / 1e4; }
