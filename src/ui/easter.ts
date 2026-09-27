// Easter eggs: mascots that pop out of a prefecture, the sticker book (図鑑) and sakura petals.
import { mascotById, mascots, prefBySlug, regionOf } from '../data';
import type { MapApi } from '../map/map';
import { mascotArt } from '../mascots/art';
import { clear, el } from './dom';

const STORAGE_KEY = 'nihonchizu.found.v1';

export interface EasterOptions {
  layer: HTMLElement;
  stage: HTMLElement;
  map: MapApi;
  onCount(found: number, total: number, isNew: boolean): void;
}

export function createEaster(opts: EasterOptions) {
  const found = new Set<string>(load());
  let node: HTMLElement | null = null;
  let slugShown: string | null = null;
  let hideTimer = 0;

  for (const id of found) {
    const m = mascotById.get(id);
    const art = mascotArt[id];
    if (m && art) opts.map.addSticker(m.prefecture, art);
  }
  opts.onCount(found.size, mascots.length, false);

  function load(): string[] {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      const arr = raw ? (JSON.parse(raw) as unknown) : [];
      return Array.isArray(arr) ? arr.filter((x): x is string => typeof x === 'string' && mascotById.has(x)) : [];
    } catch {
      return [];
    }
  }
  function save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify([...found]));
    } catch {
      /* private mode etc. */
    }
  }

  function position(n: HTMLElement, slug: string) {
    const pos = opts.map.anchorScreen(slug);
    if (!pos) return;
    n.style.left = `${pos.x}px`;
    n.style.top = `${pos.y}px`;
    n.classList.toggle('mascot--flip', pos.x > opts.stage.clientWidth / 2);
  }

  /** Show the mascot of a prefecture (if it has one). Returns true when something appeared. */
  function reveal(slug: string): boolean {
    dismiss(true);
    const p = prefBySlug.get(slug);
    if (!p?.mascot) return false;
    const m = mascotById.get(p.mascot);
    const art = m && mascotArt[m.id];
    if (!m || !art) return false;
    const isNew = !found.has(m.id);

    const n = el('div', { class: 'mascot', role: 'img', 'aria-label': `${m.name.ja} — ${m.line.ja}` });
    const artEl = el('div', { class: 'mascot__art' });
    artEl.innerHTML = art; // static, hand-written SVG from src/mascots/art.ts
    const bubble = el(
      'div',
      { class: 'mascot__bubble' },
      el('span', { class: 'b-name' }, `${m.name.ja} · ${m.name.ko}`),
      el('span', { class: 'b-line', lang: 'ja' }, m.line.ja),
      el('span', { class: 'b-ko' }, m.line.ko),
      el('span', { class: 'b-tip' }, isNew ? '✦ 図鑑에 추가됐어요' : '또 만났다 ✿'),
    );
    n.append(artEl, bubble);
    n.addEventListener('click', () => dismiss());
    opts.layer.append(n);
    node = n;
    slugShown = slug;
    position(n, slug);
    sparkle(n);

    if (isNew) {
      found.add(m.id);
      save();
      opts.map.addSticker(slug, art);
    }
    opts.onCount(found.size, mascots.length, isNew);
    hideTimer = window.setTimeout(() => dismiss(), 9000);
    return true;
  }

  function sparkle(n: HTMLElement) {
    for (let i = 0; i < 7; i++) {
      const a = (Math.PI * 2 * i) / 7 + Math.random() * 0.6;
      const d = 34 + Math.random() * 30;
      const s = el('span', { class: 'sparkle', style: `--dx:${(Math.cos(a) * d).toFixed(0)}px;--dy:${(Math.sin(a) * d - 30).toFixed(0)}px;left:-5px;top:-40px;animation-delay:${(i * 40).toFixed(0)}ms` });
      n.append(s);
      setTimeout(() => s.remove(), 1200);
    }
  }

  function dismiss(immediate = false) {
    window.clearTimeout(hideTimer);
    const n = node;
    node = null;
    slugShown = null;
    if (!n) return;
    if (immediate) n.remove();
    else {
      n.classList.add('is-leaving');
      setTimeout(() => n.remove(), 420);
    }
  }

  /** Keep the mascot glued to its prefecture while the map moves. */
  function reposition() {
    if (node && slugShown) position(node, slugShown);
  }

  function collectionView(): HTMLElement {
    const wrap = el('div', {});
    wrap.append(el('h2', {}, el('span', { lang: 'ja' }, '図鑑'), el('small', {}, `스티커 도감 ${found.size} / ${mascots.length}`)));
    wrap.append(el('p', { class: 'lead' }, found.size ? '県을 누르면 거기 사는 친구가 튀어나와요. 아직 못 만난 친구는 실루엣이에요.' : '아직 아무도 못 만났어요. 지도에서 県을 눌러보세요 — 누군가 숨어 있을지도!'));
    const grid = el('div', { class: 'zukan' });
    for (const m of mascots) {
      const p = prefBySlug.get(m.prefecture)!;
      const has = found.has(m.id);
      const art = el('div', { class: 'zukan__art', 'aria-hidden': 'true' });
      art.innerHTML = mascotArt[m.id] ?? '';
      const card = el(
        'button',
        { type: 'button', class: `zukan__card${has ? ' is-found' : ''}`, 'data-slug': p.slug, 'aria-label': has ? `${m.name.ja} (${p.name.ja})` : `??? (${p.name.ja})` },
        art,
        has ? null : el('span', { class: 'zukan__q' }, '?'),
        el('span', { class: 'zukan__name', lang: 'ja' }, has ? m.name.ja : '？？？'),
        el('span', { class: 'zukan__pref' }, `${p.short.ja} · ${p.name.ko}`),
      );
      card.style.setProperty('--c', regionOf(p).color);
      grid.append(card);
    }
    wrap.append(grid);
    if (found.size === mascots.length) wrap.append(el('p', { class: 'zukan__done' }, '🎉 전부 만났어요! 컴플리트 — おめでとう！'));
    return wrap;
  }

  return {
    reveal,
    dismiss,
    reposition,
    collectionView,
    isFound: (id: string) => found.has(id),
    foundCount: () => found.size,
    total: mascots.length,
  };
}

/** Sakura petals drifting over the page. Toggle on/off. */
export function createPetals(root: HTMLElement) {
  let on = false;
  function build() {
    clear(root);
    for (let i = 0; i < 22; i++) {
      const p = el('span', { class: 'petal' });
      p.style.left = `${Math.random() * 100}%`;
      p.style.animationDuration = `${7 + Math.random() * 7}s, ${2 + Math.random() * 2.5}s`;
      p.style.animationDelay = `${-Math.random() * 12}s, ${-Math.random() * 3}s`;
      p.style.opacity = String(0.55 + Math.random() * 0.4);
      p.style.transform = `scale(${0.7 + Math.random() * 0.7})`;
      root.append(p);
    }
  }
  return {
    toggle() {
      on = !on;
      if (on) build();
      root.hidden = !on;
      return on;
    },
    isOn: () => on,
  };
}
