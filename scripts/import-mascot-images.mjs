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

const args = process.argv.slice(2);
if (!args.length) {
  console.error('사용법: npm run mascots:import <그림 폴더 또는 파일...>');
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

/** Make near-white pixels connected to the border transparent (only for fully opaque images). */
function knockOutWhite(data, w, h) {
  let opaque = true;
  for (let i = 3; i < data.length; i += 4) if (data[i] < 250) { opaque = false; break; }
  if (!opaque) return false;
  const white = (i) => data[i] > 238 && data[i + 1] > 238 && data[i + 2] > 238;
  const corners = [0, (w - 1) * 4, (h - 1) * w * 4, ((h - 1) * w + w - 1) * 4];
  if (corners.filter(white).length < 3) return false;
  const seen = new Uint8Array(w * h);
  const stack = [];
  for (let x = 0; x < w; x++) { stack.push(x, (h - 1) * w + x); }
  for (let y = 0; y < h; y++) { stack.push(y * w, y * w + w - 1); }
  while (stack.length) {
    const p = stack.pop();
    if (seen[p]) continue;
    seen[p] = 1;
    const i = p * 4;
    if (!white(i)) continue;
    data[i + 3] = 0;
    const x = p % w, y = (p / w) | 0;
    if (x > 0) stack.push(p - 1);
    if (x < w - 1) stack.push(p + 1);
    if (y > 0) stack.push(p - w);
    if (y < h - 1) stack.push(p + w);
  }
  return true;
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
  m.art = 'official';
  if (!m.credit) {
    const org = m.org.replace(/（.*?）|\(.*?\)/g, '').trim();
    m.credit = !org || org === '民間' ? `©${m.name.ja}` : `©${org}`;
    report.credit.push(`${m.name.ja}: "${m.credit}" (규정의 표기와 다르면 data/mascots.json 에서 고치기)`);
  }
  report.ok.push(`${basename(f)} → ${target}  ${m.name.ja}${hit.by === 'prefecture' ? ' (県 이름으로 맞춤)' : ''}${knocked ? ' · 흰 배경 제거' : ''}`);
}

writeFileSync(DATA, JSON.stringify(ctx.db, null, 2) + '\n');
const { done, total } = writeChecklist(ctx);
console.log(`반입 ${report.ok.length}개 · 전체 ${done}/${total}`);
for (const l of report.ok) console.log('  ✓', l);
if (report.ambiguous.length) { console.log('누구인지 애매한 파일 — 이름을 더 구체적으로:'); for (const l of report.ambiguous) console.log('  ?', l); }
if (report.unmatched.length) { console.log('못 맞춘 파일 — 파일명에 캐릭터 이름이나 id 를 넣어 주세요:'); for (const l of report.unmatched) console.log('  ✕', l); }
if (report.credit.length) { console.log('크레딧 확인:'); for (const l of report.credit) console.log('  !', l); }
