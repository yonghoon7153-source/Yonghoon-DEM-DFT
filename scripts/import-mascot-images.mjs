// 공식 마스코트 그림 반입.
//   node scripts/import-mascot-images.mjs <그림이 든 폴더> [--credit "©…" 는 데이터에서 직접]
// 폴더 안의 png/jpg/webp/svg/gif 를 캐릭터에 맞춰 public/mascots/<id>.<ext> 로 복사하고
// data/mascots.json 의 image / art 를 갱신한다. 파일명은 id, 일본어 이름, 한국어 이름, 県 이름 중 아무거나 포함하면 된다.
import { copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { basename, extname, join } from 'node:path';

const dir = process.argv[2];
if (!dir || !existsSync(dir)) {
  console.error('사용법: node scripts/import-mascot-images.mjs <그림 폴더>');
  process.exit(1);
}
const dataPath = new URL('../data/mascots.json', import.meta.url);
const prefPath = new URL('../data/prefectures.json', import.meta.url);
const db = JSON.parse(readFileSync(dataPath, 'utf8'));
const prefs = JSON.parse(readFileSync(prefPath, 'utf8')).prefectures;
const prefBySlug = Object.fromEntries(prefs.map((p) => [p.slug, p]));
const outDir = new URL('../public/mascots/', import.meta.url);
mkdirSync(outDir, { recursive: true });

const norm = (s) => s.normalize('NFKC').toLowerCase().replace(/[\s_\-()（）・ー~〜.]/g, '');
const files = readdirSync(dir).filter((f) => /\.(png|jpe?g|webp|svg|gif)$/i.test(f) && statSync(join(dir, f)).isFile());
const report = { matched: [], unmatched: [], needCredit: [] };

for (const f of files) {
  const stem = norm(basename(f, extname(f)));
  const hit = db.mascots.find((m) => {
    const p = prefBySlug[m.prefecture];
    const keys = [m.id, m.name.ja, m.name.kana, m.name.ko, p.short.ja, p.name.ko.replace(/(현|도|부)$/, ''), p.slug].map(norm);
    return keys.some((k) => k && (stem === k || stem.includes(k)));
  });
  if (!hit) { report.unmatched.push(f); continue; }
  const ext = extname(f).toLowerCase().replace('jpeg', 'jpg');
  const target = `mascots/${hit.id}${ext}`;
  copyFileSync(join(dir, f), new URL(`../public/${target}`, import.meta.url));
  hit.image = target;
  hit.art = 'official';
  if (!hit.credit) { hit.credit = `©${hit.org}`; report.needCredit.push(`${hit.id} → "${hit.credit}" (규정에 맞는 표기로 고쳐 주세요)`); }
  report.matched.push(`${f} → ${target} (${hit.name.ja})`);
}
writeFileSync(dataPath, JSON.stringify(db, null, 2) + '\n');
console.log(`반입 ${report.matched.length}개`);
for (const l of report.matched) console.log('  ✓', l);
if (report.unmatched.length) { console.log('못 맞춘 파일 — 파일명에 캐릭터 이름이나 id 를 넣어 주세요:'); for (const f of report.unmatched) console.log('  ✕', f); }
if (report.needCredit.length) { console.log('크레딧 확인 필요:'); for (const l of report.needCredit) console.log('  !', l); }
console.log('다음: npm run data:check → nihon 으로 확인');
