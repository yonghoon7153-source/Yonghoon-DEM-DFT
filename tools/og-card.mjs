// 링크 미리보기 카드 (public/og.png, 1200×630) — 카톡 · 메신저가 링크 위에 크게 보여 주는 그림 (11차 요청).
// 다꾸 카드: 크림 종이 + 마스킹테이프 + 「にほんちず」 글씨 + 작은 일본 지도 (사이트의 지방 색 그대로).
// 캐릭터 그림은 쓰지 않는다 (권리, ADR 0003). 지도는 地球地図日本(国土地理院)이라 출처를 작게 적는다.
//   node tools/og-card.mjs        Playwright 를 쓴다 (shots.mjs 처럼 PLAYWRIGHT_MODULE=/경로/node_modules/playwright)
// 글자는 Google Fonts 에서 카드에 쓰는 글자만 받아 그림 안에 넣는다. 문구를 바꾸면 index.html 의 og:image ?v= 도 올린다.
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { geoMercator, geoPath } from 'd3-geo';
import { feature } from 'topojson-client';
import sharp from 'sharp';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = new URL('../', import.meta.url);
const read = (p) => JSON.parse(readFileSync(new URL(p, root), 'utf8'));

const TITLE = 'にほんちず';
const SUB = '눌러 보는 일본 지도';
const URL_TEXT = 'nihoncheese.bmlwork.kr';
const CREDIT = '地図: 地球地図日本（国土地理院）';
const W = 1200, H = 630;

// ---------------------------------------------------------------- fonts: only the letters on the card
const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36';
async function font(family, weight, text) {
  const css = await (await fetch(`https://fonts.googleapis.com/css2?family=${family}:wght@${weight}&text=${encodeURIComponent(text)}`, { headers: { 'user-agent': UA } })).text();
  const url = css.match(/url\((https:[^)]+)\)/)?.[1];
  if (!url) throw new Error(`no font for ${family}: ${css.slice(0, 200)}`);
  const buf = Buffer.from(await (await fetch(url)).arrayBuffer());
  return `data:font/woff2;base64,${buf.toString('base64')}`;
}
const [kiwi, gaegu, gowun, zen] = await Promise.all([
  font('Kiwi+Maru', 500, TITLE),
  font('Gaegu', 700, SUB),
  font('Gowun+Dodum', 400, URL_TEXT),
  font('Zen+Maru+Gothic', 500, CREDIT),
]);

// ---------------------------------------------------------------- the map, as on the site
const topo = read('public/geo/japan.topo.json');
const regionColor = new Map(read('data/regions.json').regions.map((r) => [r.id, r.color]));
const regionOfId = new Map(read('data/prefectures.json').prefectures.map((p) => [p.id, p.region]));
const shift = topo.meta?.okinawaShift ?? [-0.6, 5.4];
const OKINAWA = 47;
// 沖縄 main group moves up next to 九州 like the site's inset; far islands (小笠原, 大東, 先島, 奄美) stay off the card
const keep = (lon, lat, id) => (id === OKINAWA ? lon > 126.5 && lon < 129 : lat > 30.2 && lon < 146.5);
const centroid = (ring) => ring.reduce((a, [x, y]) => [a[0] + x / ring.length, a[1] + y / ring.length], [0, 0]);
const prefs = feature(topo, topo.objects.japan).features.map((f) => {
  const id = f.properties.id;
  const polys = (f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates)
    .filter((poly) => { const [x, y] = centroid(poly[0]); return keep(x, y, id); })
    .map((poly) => (id === OKINAWA ? poly.map((ring) => ring.map(([x, y]) => [x + shift[0], y + shift[1]])) : poly));
  return { type: 'Feature', properties: { id }, geometry: { type: 'MultiPolygon', coordinates: polys } };
}).filter((f) => f.geometry.coordinates.length);
const land = { type: 'FeatureCollection', features: prefs };
const MAP = 540;
const projection = geoMercator().fitExtent([[24, 24], [MAP - 24, MAP - 24]], land);
const path = geoPath(projection);
// the outline for the sea glow and the white sticker edge: every prefecture together
const outline = prefs.map((f) => path(f)).join(' ');
const shapes = prefs.map((f) => `<path d="${path(f)}" fill="${regionColor.get(regionOfId.get(f.properties.id)) ?? '#eee6d6'}"/>`).join('');

// ---------------------------------------------------------------- the card
const tape = (x, y, w, rot, c1, c2) =>
  `<div class="tape" style="left:${x}px;top:${y}px;width:${w}px;transform:rotate(${rot}deg);background:repeating-linear-gradient(90deg,${c1} 0 10px,${c2} 10px 20px)"></div>`;
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: Kiwi; src: url(${kiwi}) format('woff2'); }
@font-face { font-family: Gaegu; src: url(${gaegu}) format('woff2'); }
@font-face { font-family: Gowun; src: url(${gowun}) format('woff2'); }
@font-face { font-family: Zen; src: url(${zen}) format('woff2'); }
* { margin: 0; box-sizing: border-box; }
body { width: ${W}px; height: ${H}px; overflow: hidden; position: relative; color: #4a3f3a;
  background: #fbf7ee radial-gradient(circle, #e7ddcf 1.6px, transparent 1.9px) 0 0 / 28px 28px; }
.title { position: absolute; left: 86px; top: 158px; font: 500 132px/1 Kiwi; letter-spacing: 2px; }
.sub { position: absolute; left: 92px; top: 330px; font: 700 64px/1 Gaegu; letter-spacing: -.16em; word-spacing: .22em; }
/* a honey highlighter stroke under the words, as if marked in a diary */
.sub::before { content: ''; position: absolute; left: -10px; right: -12px; bottom: 2px; height: 26px; z-index: -1;
  background: rgba(242, 184, 75, .38); border-radius: 12px 4px 14px 6px; transform: rotate(-1.2deg); }
.url { position: absolute; left: 96px; top: 452px; font: 400 26px/1 Gowun; color: #a8998f; letter-spacing: .5px; }
.sticker { position: absolute; left: 610px; top: 44px; width: ${MAP}px; height: ${MAP}px; transform: rotate(-3.5deg);
  filter: drop-shadow(0 10px 14px rgba(74, 63, 58, .16)); }
.tape { position: absolute; height: 34px; border-radius: 3px; opacity: .85; box-shadow: 0 1px 2px rgba(74, 63, 58, .15); }
.credit { position: absolute; right: 26px; bottom: 16px; font: 500 15px/1 Zen; color: #a8998f; }
</style></head><body>
<div class="title">${TITLE}</div>
<div class="sub">${SUB}</div>
<div class="url">${URL_TEXT}</div>
<svg class="sticker" viewBox="0 0 ${MAP} ${MAP}" xmlns="http://www.w3.org/2000/svg">
  <path d="${outline}" fill="none" stroke="#d6e9f1" stroke-width="30" stroke-linejoin="round"/>
  <path d="${outline}" fill="none" stroke="#fffdf9" stroke-width="12" stroke-linejoin="round"/>
  <g stroke="#fffdf9" stroke-width="1.4" stroke-linejoin="round">${shapes}</g>
</svg>
${tape(640, 70, 150, -32, 'rgba(229,112,141,.55)', 'rgba(255,255,255,.5)')}
${tape(1010, 520, 150, -28, 'rgba(111,176,166,.55)', 'rgba(255,255,255,.5)')}
${tape(70, 112, 120, -4, 'rgba(242,184,75,.5)', 'rgba(255,255,255,.5)')}
<div class="credit">${CREDIT}</div>
</body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.setContent(html, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
const shot = await page.screenshot({ type: 'png' });
await browser.close();
const out = await sharp(shot).png({ palette: true, quality: 92, compressionLevel: 9 }).toBuffer();
writeFileSync(new URL('public/og.png', root), out);
console.log(`public/og.png ${W}×${H}, ${(out.length / 1024).toFixed(0)} KB`);
