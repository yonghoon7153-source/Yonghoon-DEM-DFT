// 스크린샷 QA: 미리보기 서버(http://localhost:4173 또는 BASE)를 띄운 뒤  node tools/shots.mjs
// 전역 playwright 를 쓰려면 PLAYWRIGHT_MODULE=/경로/node_modules/playwright
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = process.env.BASE || 'http://localhost:4173/';
const out = process.env.OUT || 'docs/screenshots/qa';
const browser = await chromium.launch();
const errors = [];
async function page(vp, opts = {}) {
  const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1, hasTouch: !!opts.touch, isMobile: !!opts.touch, locale: 'ko-KR' });
  const p = await ctx.newPage();
  p.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  p.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  return { ctx, p };
}
async function ready(p) {
  await p.goto(base, { waitUntil: 'networkidle' });
  await p.waitForSelector('.map svg path.pref');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
}
const steps = (process.env.STEPS || 'desktop,select,region,mobile,zukan,search,t23,transit,matsuri,landmarks').split(',');

if (steps.includes('desktop')) {
  const { ctx, p } = await page({ width: 1440, height: 900 });
  await ready(p);
  await p.screenshot({ path: `${out}/01-desktop.png` });
  await p.hover('path.pref[data-slug="nagano"]');
  await p.waitForTimeout(250);
  await p.screenshot({ path: `${out}/02-hover.png` });
  await ctx.close();
}
if (steps.includes('select')) {
  const { ctx, p } = await page({ width: 1440, height: 900 });
  await ready(p);
  await p.click('path.pref[data-slug="kyoto"]');
  await p.waitForTimeout(1600);
  await p.screenshot({ path: `${out}/03-kyoto.png` });
  await p.keyboard.press('Escape');
  await p.waitForTimeout(500);
  await p.click('#zoom-reset');
  await p.waitForTimeout(1000);
  await p.click('path.pref[data-slug="kumamoto"]');
  await p.waitForTimeout(1600);
  await p.screenshot({ path: `${out}/04-kumamoto.png` });
  await p.evaluate(() => { document.querySelector('#panel-body').scrollTop = 600; });
  await p.waitForTimeout(200);
  await p.screenshot({ path: `${out}/05-kumamoto-scrolled.png` });
  await ctx.close();
}
if (steps.includes('region')) {
  const { ctx, p } = await page({ width: 1440, height: 900 });
  await ready(p);
  await p.hover('#legend button[data-region="tohoku"]');
  await p.waitForTimeout(300);
  await p.screenshot({ path: `${out}/06a-legend-hover.png` });
  await p.click('#legend button[data-region="kanto"]');
  await p.waitForTimeout(1400);
  await p.screenshot({ path: `${out}/06-region-kanto.png` });
  await p.click('#label-mode button[data-mode="kana"]');
  await p.waitForTimeout(300);
  await p.screenshot({ path: `${out}/07-kana-mode.png` });
  await ctx.close();
}
if (steps.includes('mobile')) {
  const { ctx, p } = await page({ width: 390, height: 844 }, { touch: true });
  await ready(p);
  await p.screenshot({ path: `${out}/08-mobile.png` });
  await p.evaluate(() => document.querySelector('path.pref[data-slug="tokyo"]').dispatchEvent(new MouseEvent('click', { bubbles: true })));
  await p.waitForTimeout(1600);
  await p.screenshot({ path: `${out}/09-mobile-tokyo.png` });
  await p.evaluate(() => { document.querySelector('#panel-body').scrollTop = 500; });
  await p.waitForTimeout(200);
  await p.screenshot({ path: `${out}/09b-mobile-tokyo-scrolled.png` });
  await ctx.close();
}
if (steps.includes('zukan')) {
  const { ctx, p } = await page({ width: 1440, height: 900 });
  await ready(p);
  // nothing is kept across reloads, so meet friends in this visit — the prefectures with two or three of them too
  for (const slug of ['ehime', 'tochigi', 'ibaraki', 'chiba', 'shiga', 'kochi', 'hokkaido', 'kumamoto', 'osaka']) {
    await p.evaluate((s) => { location.hash = s; }, slug);
    await p.waitForTimeout(1300);
  }
  await p.click('#collection-btn');
  await p.waitForTimeout(700);
  await p.screenshot({ path: `${out}/10-zukan-all.png` });
  await p.keyboard.press('Escape');
  await p.click('#zoom-reset');
  await p.waitForTimeout(1200);
  await p.screenshot({ path: `${out}/11-stickers-on-map.png` });
  await ctx.close();
}
if (steps.includes('t23')) {
  // the 23区 popup: a ward's card pops out beside the map (below it on a phone), never over it
  const { ctx, p } = await page({ width: 1440, height: 900 });
  await ready(p);
  // Tokyo is small on the whole map and its name sits on top of it, so click it the way a tap does
  await p.evaluate(() => document.querySelector('path.pref[data-slug="tokyo"]').dispatchEvent(new MouseEvent('click', { bubbles: true })));
  await p.waitForSelector('.t23__map');
  await p.waitForTimeout(500);
  await p.evaluate(() => document.querySelector('.t23__ward[aria-label="港区"]').dispatchEvent(new MouseEvent('click', { bubbles: true })));
  await p.waitForTimeout(900);
  await p.screenshot({ path: `${out}/15-t23-minato.png` });
  await ctx.close();
}
if (steps.includes('transit')) {
  // 🚄 가는 법 layer: hubs and lines on the whole country, airports · stations · line names when zoomed in
  const { ctx, p } = await page({ width: 1440, height: 900 });
  await ready(p);
  await p.click('button[data-layer="transit"]');
  await p.waitForTimeout(900);
  await p.screenshot({ path: `${out}/16-transit.png` });
  await p.evaluate(() => document.querySelectorAll('#panel .range-item')[0].click());
  await p.waitForTimeout(1500);
  await p.screenshot({ path: `${out}/17-transit-tokaido.png` });
  await ctx.close();
}
if (steps.includes('matsuri')) {
  // 🎆 축제 달력: the calendar page, then a row → the prefecture with its effect mid-flight (fireworks over 新潟)
  const { ctx, p } = await page({ width: 1440, height: 900 });
  await ready(p);
  await p.click('#matsuri-btn');
  await p.waitForTimeout(600);
  await p.screenshot({ path: `${out}/18-matsuri.png` });
  await p.evaluate(() => [...document.querySelectorAll('.fes__go')].find((b) => b.querySelector('b').textContent === '長岡まつり大花火大会').click());
  await p.waitForTimeout(1500);
  await p.screenshot({ path: `${out}/19-matsuri-hanabi.png` });
  await ctx.close();
}
if (steps.includes('landmarks')) {
  // 랜드마크 스티커: the 近畿 region with its stickers, then 京都 open
  const { ctx, p } = await page({ width: 1440, height: 900 });
  await ready(p);
  await p.evaluate(() => { location.hash = 'region/kinki'; });
  await p.waitForTimeout(1600);
  await p.screenshot({ path: `${out}/20-landmarks-kinki.png` });
  await p.evaluate(() => { location.hash = 'kyoto'; });
  await p.waitForTimeout(1800);
  await p.screenshot({ path: `${out}/21-landmarks-kyoto.png` });
  await ctx.close();
}
if (steps.includes('search')) {
  const { ctx, p } = await page({ width: 1440, height: 900 });
  await ready(p);
  await p.fill('#search-input', '오사');
  await p.waitForTimeout(300);
  await p.screenshot({ path: `${out}/12-search.png` });
  await p.keyboard.press('Enter');
  await p.waitForTimeout(1600);
  await p.screenshot({ path: `${out}/13-osaka.png` });
  await p.click('#memo-btn');
  await p.waitForTimeout(500);
  await p.screenshot({ path: `${out}/14-memo.png` });
  await ctx.close();
}
await browser.close();
if (errors.length) { console.log('ERRORS:\n' + errors.join('\n')); } else console.log('no page errors');
