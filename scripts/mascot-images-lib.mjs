// Shared bits for the mascot image tools: data loading, file-name matching, the checklist writer.
import { existsSync, readFileSync, writeFileSync } from 'node:fs';

export const ROOT = new URL('../', import.meta.url);
export const DATA = new URL('data/mascots.json', ROOT);

export function loadDb() {
  const db = JSON.parse(readFileSync(DATA, 'utf8'));
  const prefs = JSON.parse(readFileSync(new URL('data/prefectures.json', ROOT), 'utf8')).prefectures;
  const regions = JSON.parse(readFileSync(new URL('data/regions.json', ROOT), 'utf8')).regions.sort((a, b) => a.order - b.order);
  return { db, prefs, regions, prefBySlug: Object.fromEntries(prefs.map((p) => [p.slug, p])) };
}

export const norm = (s) =>
  String(s ?? '')
    .normalize('NFKC')
    .toLowerCase()
    .replace(/[ァ-ヶ]/g, (ch) => String.fromCharCode(ch.charCodeAt(0) - 0x60)) // katakana → hiragana
    .replace(/[\s_\-()（）・ー~〜.,、。!！?？'"「」『』]/g, '');

/**
 * Which mascot does a file name mean?  Character names win over prefecture names, so
 * "ねば〜る君 茨城.png" is ねば〜る君, while "茨城.png" alone is the official one (ハッスル黄門).
 */
export function matchFile(fileStem, { db, prefs }) {
  const stem = norm(fileStem);
  const score = (keys) => {
    let best = 0;
    for (const k of keys.map(norm)) {
      if (!k || k.length < 2) continue;
      if (stem === k) best = Math.max(best, 1000 + k.length);
      else if (stem.includes(k)) best = Math.max(best, k.length);
    }
    return best;
  };
  const byName = db.mascots
    .map((m) => ({ m, s: score([m.id, m.name.ja, m.name.kana, m.name.ko]) }))
    .filter((x) => x.s > 0)
    .sort((a, b) => b.s - a.s || (a.m.kind === 'official' ? -1 : 1));
  if (byName.length) {
    if (byName.length > 1 && byName[0].s === byName[1].s && byName[0].m.kind === byName[1].m.kind) return { ambiguous: byName.slice(0, 3).map((x) => x.m.id) };
    return { mascot: byName[0].m, by: 'name' };
  }
  const byPref = prefs
    .map((p) => ({ p, s: score([p.slug, p.short.ja, p.name.ja, p.short.kana, p.name.kana, p.name.ko, p.name.ko.replace(/(현|도|부)$/, ''), p.name.en]) }))
    .filter((x) => x.s > 0)
    .sort((a, b) => b.s - a.s);
  if (byPref.length) {
    const m = db.mascots.find((x) => x.prefecture === byPref[0].p.slug && x.kind === 'official');
    if (m) return { mascot: m, by: 'prefecture' };
  }
  return {};
}

/** docs/MASCOT_IMAGES.md — the list of pictures we still need, with status. */
export function writeChecklist({ db, prefBySlug, regions }) {
  const has = (m) => m.image && existsSync(new URL(`public/${m.image}`, ROOT));
  const total = db.mascots.length;
  const done = db.mascots.filter(has).length;
  const search = (m) => `https://www.google.com/search?tbm=isch&q=${encodeURIComponent(`${m.name.ja} ${m.org} 公式 イラスト`)}`;
  const lines = [];
  lines.push('# 마스코트 그림 목록');
  lines.push('');
  lines.push(`받은 그림 **${done} / ${total}** · 이 파일은 \`npm run mascots:list\` 가 데이터에서 만든다 (손으로 고치지 않는다).`);
  lines.push('');
  lines.push('주는 법: 캐릭터당 한 장, 배경 투명 PNG 가 제일 좋다 (흰 배경 JPG 도 자동으로 배경을 지운다). 파일명에 **캐릭터 이름·県 이름·id 중 하나**만 들어 있으면 된다.');
  lines.push('받은 뒤: `npm run mascots:import <폴더>` → 512px WebP 로 줄여 `public/mascots/<id>.webp` 에 넣고 데이터와 이 목록을 갱신한다.');
  lines.push('');
  let no = 0;
  for (const r of regions) {
    const list = db.mascots.filter((m) => prefBySlug[m.prefecture].region === r.id);
    if (!list.length) continue;
    lines.push(`## ${r.name.ja} ${r.name.ko}`);
    lines.push('');
    lines.push('| # | 県 | 캐릭터 | 한글 | 파일명 | 권리자 | 찾을 곳 | 상태 |');
    lines.push('|---|---|---|---|---|---|---|---|');
    for (const m of list) {
      no++;
      const p = prefBySlug[m.prefecture];
      const where = m.url ? `[공식](${m.url})` : `[이미지 검색](${search(m)})`;
      const tag = m.kind === 'extra' ? ' <sub>비공식·선택</sub>' : '';
      lines.push(`| ${no} | ${p.short.ja} | ${m.name.ja}${tag} | ${m.name.ko} | \`${m.id}.png\` | ${m.org} | ${where} | ${has(m) ? (m.art === 'standin' ? `✅ 대체 (${m.credit})` : '✅') : '□'} |`);
    }
    lines.push('');
  }
  writeFileSync(new URL('docs/MASCOT_IMAGES.md', ROOT), lines.join('\n'));
  return { done, total };
}
