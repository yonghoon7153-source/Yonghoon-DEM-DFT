// 🎆 축제 달력 — a page of the year: which festival (or season) is where, month by month (v2, ADR 0009).
// Everything comes from data/festivals.json; the source tag (내 마인드맵 · 보충 · Claude) is worked out from the notes.
import { festivalSource, festivals, prefBySlug, regionOf } from '../data';
import type { Festival } from '../types';
import { el } from './dom';
import { photoSearch } from './notes-render';

const MONTH_JA = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
const SOURCE_LABEL = { notes: '내 마인드맵', supplement: '보충', claude: 'Claude' } as const;

const month = (mmdd: string) => Number(mmdd.slice(0, 2));
const day = (mmdd: string) => Number(mmdd.slice(3));
/** 「8/2 ~ 8/7」 the way I write dates on my map; ≈ when the dates move a little every year. */
function when(f: Festival): string {
  const a = `${month(f.start)}/${day(f.start)}`;
  const b = f.end ? `${month(f.end)}/${day(f.end)}` : '';
  return `${f.approx ? '≈ ' : ''}${a}${b && b !== a ? ` ~ ${b}` : ''}`;
}

export function renderFestivals(cb: { onPick(f: Festival): void }): HTMLElement {
  const wrap = el('div', { class: 'fes' });
  const now = new Date().getMonth() + 1;
  wrap.append(
    el('h2', {}, el('span', { lang: 'ja' }, '🎆 祭り'), el('small', {}, 'まつり · 축제 달력 — 달마다 어디로 갈까')),
    el('p', { class: 'lead' }, '내 마인드맵과 보충에 적힌 축제, 그리고 Claude 가 채운 유명 축제와 벚꽃 · 단풍 시즌이에요. 날짜는 해마다 조금씩 달라요 — 가기 전에 공식 안내를 봐 주세요.'),
  );

  // by month; a span across the new year (夜神楽 11월 ~ 2월) sits in its first month
  const byMonth = new Map<number, Festival[]>();
  for (const f of festivals) {
    const m = month(f.start);
    byMonth.set(m, [...(byMonth.get(m) ?? []), f]);
  }
  for (const list of byMonth.values()) list.sort((a, b) => (a.start < b.start ? -1 : a.start > b.start ? 1 : 0));

  // the month strip: tap a month to jump; the current one is marked
  const strip = el('nav', { class: 'fes__months', 'aria-label': '달' });
  for (let m = 1; m <= 12; m++) {
    const n = byMonth.get(m)?.length ?? 0;
    const b = el('button', { type: 'button', class: `fes__month${m === now ? ' is-now' : ''}${n ? '' : ' is-empty'}`, disabled: n ? undefined : '' }, `${m}월`, n ? el('small', {}, String(n)) : null);
    b.addEventListener('click', () => wrap.querySelector(`#fes-m${m}`)?.scrollIntoView({ block: 'start', behavior: 'smooth' }));
    strip.append(b);
  }
  wrap.append(strip);

  for (let m = 1; m <= 12; m++) {
    const list = byMonth.get(m);
    if (!list?.length) continue;
    const sec = el('section', { class: `fes__sec${m === now ? ' is-now' : ''}`, id: `fes-m${m}` });
    sec.append(el('h3', { class: 'fes__h' }, el('span', { lang: 'ja' }, MONTH_JA[m - 1]), el('small', {}, `${m}월`), m === now ? el('span', { class: 'fes__now' }, '지금') : null));
    const ul = el('ul', { class: 'fes__list' });
    for (const f of list) {
      const p = prefBySlug.get(f.pref)!;
      const r = regionOf(p);
      const src = festivalSource(f);
      const chip = el('button', { type: 'button', class: 'fes__pref', style: `--c:${r.color}`, title: `${p.name.ja} 열기` }, el('span', { lang: 'ja' }, p.short.ja), el('small', {}, p.name.ko.replace(/(현|도|부)$/, '')));
      chip.addEventListener('click', (e) => { e.stopPropagation(); cb.onPick(f); });
      // the whole strip is a button: off to the prefecture, with the festival's own burst
      const body = el('button', { type: 'button', class: 'fes__go', title: `${p.name.ja} 로 · ${f.ko}` },
        el('span', { class: 'fes__name' }, el('span', { class: 'fes__ico', 'aria-hidden': 'true' }, f.kind === 'season' ? (/紅葉/.test(f.ja) ? '🍁' : '🌸') : '🎆'), el('b', { lang: 'ja' }, f.ja), el('span', { class: 'fes__kana', lang: 'ja' }, f.kana)),
        el('span', { class: 'fes__ko' }, f.ko, f.note ? el('span', { class: 'fes__note' }, ` — ${f.note}`) : null));
      body.addEventListener('click', () => cb.onPick(f));
      ul.append(el('li', { class: `fes__item${f.kind === 'season' ? ' fes__item--season' : ''}` },
        el('span', { class: 'fes__when' }, when(f)),
        body,
        el('span', { class: 'fes__side' }, chip, photoSearch(`${f.ja} ${p.name.ja}`), el('span', { class: `fes__src fes__src--${src}` }, SOURCE_LABEL[src])),
      ));
    }
    sec.append(ul);
    wrap.append(sec);
  }
  wrap.append(el('p', { class: 'meta-line' }, '출처 표시: 내 마인드맵 · 보충 = 그 県 페이지에 칸이 있는 축제, Claude = 달력을 위해 채운 것. ≈ = 해마다 날짜가 조금씩 달라요.'));
  return wrap;
}
