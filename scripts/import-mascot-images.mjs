// 공식 마스코트 그림 반입.
//   npm run mascots:import <폴더 또는 파일...>
// 파일명에 캐릭터 이름·県 이름·id 중 하나가 들어 있으면 캐릭터에 맞춰
//   · 흰 배경이면 배경을 투명하게 (가장자리에서 이어진 흰색만)
//   · 여백을 잘라내고 512px 안으로 줄여 WebP 로
//   · public/mascots/<id>.webp 에 저장, data/mascots.json 의 image/art/credit 갱신
//   · docs/MASCOT_IMAGES.md 목록 갱신
// 원본 파일은 저장소에 넣지 않는다 (크기·권리).
import { existsSync, mkdirSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { basename, extname, join } from 'node:path';
import sharp from 'sharp';
import { DATA, loadDb, matchFile, ROOT, writeChecklist } from './mascot-images-lib.mjs';

// --standin "<출처>": 공식 그림 대신 사용자가 고른 그림(예: いらすとや). 크레딧은 출처, 화면에는 「공식 그림 아님」.
const argv = process.argv.slice(2);
let standin = null;
let mainOnly = false; // --main-only: keep only the character (drop captions, © marks beside it)
const args = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--standin') standin = argv[++i] ?? '';
  else if (argv[i] === '--main-only') mainOnly = true;
  else args.push(argv[i]);
}
if (!args.length || standin === '') {
  console.error('사용법: npm run mascots:import <그림 폴더 또는 파일...> [--standin "<출처>"] [--main-only]');
  process.exit(1);
}
const IMG = /\.(png|jpe?g|webp|gif|avif|tiff?)$/i;
const files = [];
for (const a of args) {
  if (!existsSync(a)) { console.error(`없는 경로: ${a}`); continue; }
  if (statSync(a).isDirectory()) {
    const walk = (d) => {
      for (const f of readdirSync(d)) {
        const p = join(d, f);
        if (f.startsWith('.') || f === '__MACOSX') continue;
        if (statSync(p).isDirectory()) walk(p);
        else if (IMG.test(f)) files.push(p);
      }
    };
    walk(a);
  } else if (IMG.test(a)) files.push(a);
}

const ctx = loadDb();
const outDir = new URL('public/mascots/', ROOT);
mkdirSync(outDir, { recursive: true });
const report = { ok: [], unmatched: [], ambiguous: [], credit: [] };

/**
 * Remove a plain white/near-white background.
 * Runs when most of the border is opaque and light (images that are already cut out are left alone;
 * images with a white background and a few transparent edge pixels are handled too).
 * The background colour is estimated from the opaque border; only pixels within a few levels of it,
 * nearly grey, and connected to the border are cleared, so white gloves, sashes and eyes that are merely
 * *close* to white survive. The one-pixel ring next to the cleared area is feathered to avoid a white halo.
 */
function knockOutWhite(data, w, h) {
  const alpha = (i) => data[i + 3];
  const minc = (i) => Math.min(data[i], data[i + 1], data[i + 2]);
  const maxc = (i) => Math.max(data[i], data[i + 1], data[i + 2]);
  const border = [];
  for (let x = 0; x < w; x++) border.push(x, (h - 1) * w + x);
  for (let y = 0; y < h; y++) border.push(y * w, y * w + w - 1);
  const opaque = border.filter((p) => alpha(p * 4) >= 250);
  if (opaque.length < border.length * 0.3) return false; // already cut out
  const lights = opaque.map((p) => minc(p * 4)).sort((a, b) => a - b);
  const bg = lights[Math.floor(lights.length / 2)];
  if (bg < 232) return false; // not a white-ish background — leave it alone
  const hard = Math.min(bg - 6, 249); // e.g. pure white → 249
  const soft = hard - 20;             // feather band for the edge ring
  const isBg = (p) => { const i = p * 4; return alpha(i) < 20 || (minc(i) >= hard && maxc(i) - minc(i) <= 10); };
  const cleared = new Uint8Array(w * h);
  const seen = new Uint8Array(w * h);
  const stack = border.slice();
  while (stack.length) {
    const p = stack.pop();
    if (seen[p]) continue;
    seen[p] = 1;
    if (!isBg(p)) continue;
    cleared[p] = 1;
    data[p * 4 + 3] = 0;
    const x = p % w, y = (p / w) | 0;
    if (x > 0) stack.push(p - 1);
    if (x < w - 1) stack.push(p + 1);
    if (y > 0) stack.push(p - w);
    if (y < h - 1) stack.push(p + w);
  }
  for (let p = 0; p < w * h; p++) {
    if (cleared[p] || alpha(p * 4) < 20) continue;
    const x = p % w, y = (p / w) | 0;
    const touches = (x > 0 && cleared[p - 1]) || (x < w - 1 && cleared[p + 1]) || (y > 0 && cleared[p - w]) || (y < h - 1 && cleared[p + w]);
    if (!touches) continue;
    const m = minc(p * 4);
    if (m > soft) data[p * 4 + 3] = Math.round(255 * Math.min(1, Math.max(0, (hard - m) / (hard - soft))));
  }
  return true;
}

/** Keep only the largest opaque blob (8-connected) — drops captions and © marks printed beside the character. */
function keepLargestComponent(data, w, h) {
  const n = w * h;
  const label = new Int32Array(n).fill(-1);
  const stack = new Int32Array(n);
  let best = -1, bestSize = 0, count = 0;
  for (let p = 0; p < n; p++) {
    if (label[p] !== -1 || data[p * 4 + 3] <= 8) continue;
    let sp = 0, size = 0;
    stack[sp++] = p; label[p] = count;
    while (sp) {
      const q = stack[--sp]; size++;
      const x = q % w, y = (q / w) | 0;
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        if (!dx && !dy) continue;
        const nx = x + dx, ny = y + dy;
        if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
        const r = ny * w + nx;
        if (label[r] === -1 && data[r * 4 + 3] > 8) { label[r] = count; stack[sp++] = r; }
      }
    }
    if (size > bestSize) { bestSize = size; best = count; }
    count++;
  }
  let removed = 0;
  for (let p = 0; p < n; p++) if (label[p] !== -1 && label[p] !== best) { data[p * 4 + 3] = 0; removed++; }
  return { count, removed };
}

function alphaBox(data, w, h) {
  let x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (data[(y * w + x) * 4 + 3] > 8) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  }
  return x1 < 0 ? null : { left: x0, top: y0, width: x1 - x0 + 1, height: y1 - y0 + 1 };
}

for (const f of files) {
  const hit = matchFile(basename(f, extname(f)), ctx);
  if (hit.ambiguous) { report.ambiguous.push(`${basename(f)} → ${hit.ambiguous.join(' / ')}`); continue; }
  if (!hit.mascot) { report.unmatched.push(basename(f)); continue; }
  const m = hit.mascot;
  const { data, info } = await sharp(f).rotate().ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const knocked = knockOutWhite(data, info.width, info.height);
  const main = mainOnly ? keepLargestComponent(data, info.width, info.height) : null;
  const box = alphaBox(data, info.width, info.height);
  let img = sharp(data, { raw: { width: info.width, height: info.height, channels: 4 } });
  if (box) {
    const pad = Math.round(Math.max(box.width, box.height) * 0.03);
    const left = Math.max(0, box.left - pad), top = Math.max(0, box.top - pad);
    img = img.extract({ left, top, width: Math.min(info.width - left, box.width + pad * 2), height: Math.min(info.height - top, box.height + pad * 2) });
  }
  const target = `mascots/${m.id}.webp`;
  await img.resize(512, 512, { fit: 'inside', withoutEnlargement: true }).webp({ quality: 88, alphaQuality: 100, effort: 5 }).toFile(new URL(`public/${target}`, ROOT).pathname);
  m.image = target;
  if (standin) {
    m.art = 'standin';
    m.credit = standin;
    report.credit.push(`${m.name.ja}: 대체 그림 — 크레딧 "${standin}", 화면에 「공식 그림 아님」`);
    report.ok.push(`${basename(f)} → ${target}  ${m.name.ja} (대체 그림)`);
    continue;
  }
  if (m.art === 'standin') delete m.credit; // the old credit belonged to the stand-in picture
  m.art = 'official';
  if (!m.credit) {
    const org = m.org.replace(/（.*?）|\(.*?\)/g, '').trim();
    m.credit = !org || org === '民間' ? `©${m.name.ja}` : `©${org}`;
    report.credit.push(`${m.name.ja}: "${m.credit}" (규정의 표기와 다르면 data/mascots.json 에서 고치기)`);
  }
  report.ok.push(`${basename(f)} → ${target}  ${m.name.ja}${hit.by === 'prefecture' ? ' (県 이름으로 맞춤)' : ''}${knocked ? ' · 흰 배경 제거' : ''}${main && main.removed ? ` · 캐릭터 밖 조각 ${main.count - 1}개 제거` : ''}`);
}

writeFileSync(DATA, JSON.stringify(ctx.db, null, 2) + '\n');
const { done, total } = writeChecklist(ctx);
console.log(`반입 ${report.ok.length}개 · 전체 ${done}/${total}`);
for (const l of report.ok) console.log('  ✓', l);
if (report.ambiguous.length) { console.log('누구인지 애매한 파일 — 이름을 더 구체적으로:'); for (const l of report.ambiguous) console.log('  ?', l); }
if (report.unmatched.length) { console.log('못 맞춘 파일 — 파일명에 캐릭터 이름이나 id 를 넣어 주세요:'); for (const l of report.unmatched) console.log('  ✕', l); }
if (report.credit.length) { console.log('크레딧 확인:'); for (const l of report.credit) console.log('  !', l); }
