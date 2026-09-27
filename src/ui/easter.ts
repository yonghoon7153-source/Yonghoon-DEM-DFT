// Easter eggs: mascots that pop out of a prefecture, the sticker book (図鑑) and sakura petals.
import { mascotById, mascots, prefBySlug, regionOf, regions, secretFor } from '../data';
import type { MapApi } from '../map/map';
import { mascotSticker, mascotVisualHtml } from '../mascots/visual';
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
    if (m && m.kind === 'official') opts.map.addSticker(m.prefecture, mascotSticker(m));
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

  /** Show the official mascot of a prefecture. Returns true when something appeared. */
  function reveal(slug: string): boolean {
    const p = prefBySlug.get(slug);
    if (!p?.mascot) return false;
    return revealMascot(p.mascot);
  }

  /** Show one specific mascot (official or extra) popping out of its prefecture. */
  function revealMascot(id: string): boolean {
    dismiss(true);
    const m = mascotById.get(id);
    if (!m) return false;
    const art = mascotVisualHtml(m);
    if (!art) return false;
    const slug = m.prefecture;
    const isNew = !found.has(m.id);

    const n = el('div', { class: `mascot${m.secret ? ' mascot--secret' : ''}`, role: 'img', 'aria-label': `${m.name.ja} — ${m.line.ja}` });
    const artEl = el('div', { class: 'mascot__art' });
    artEl.innerHTML = art; // our own SVG likeness, or <img> of the official picture
    const bubble = el(
      'div',
      { class: 'mascot__bubble' },
      el('span', { class: 'b-name' }, `${m.name.ja}`, el('span', { class: 'b-org' }, ` · ${m.org}`)),
      el('span', { class: 'b-line', lang: 'ja' }, m.line.ja),
      el('span', { class: 'b-ko' }, m.line.ko),
      el('span', { class: 'b-tip' }, isNew ? (m.secret ? '✦ 숨은 친구를 찾았어요!' : '✦ 図鑑에 추가됐어요') : '또 만났다 ✿'),
    );
    n.append(artEl, bubble);
    // Easter egg: a mascot with a hidden friend turns into it after three taps on the picture.
    const alter = m.secret ? undefined : secretFor(m);
    if (alter) {
      let taps = 0;
      artEl.addEventListener('click', (e) => {
        e.stopPropagation();
        taps++;
        window.clearTimeout(hideTimer);
        hideTimer = window.setTimeout(() => dismiss(), 9000);
        artEl.classList.remove('is-poked');
        void artEl.offsetWidth; // restart the animation
        artEl.classList.add('is-poked');
        if (taps >= 3) {
          n.classList.add('is-darkening');
          window.setTimeout(() => {
            if (node === n) revealMascot(alter.id);
          }, 480);
        }
      });
    }
    n.addEventListener('click', () => dismiss());
    opts.layer.append(n);
    node = n;
    slugShown = slug;
    position(n, slug);
    sparkle(n);

    if (isNew) {
      found.add(m.id);
      save();
      if (m.kind === 'official') opts.map.addSticker(slug, mascotSticker(m));
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
    wrap.append(el('h2', {}, el('span', { lang: 'ja' }, '図鑑'), el('small', {}, `ご当地キャラ 도감 ${found.size} / ${mascots.length}`)));
    wrap.append(
      el(
        'p',
        { class: 'lead' },
        found.size
          ? '県을 누르면 그 県의 공식 캐릭터가, 패널의 「친구들」에서 누르면 나머지 친구가 튀어나와요. 아직 못 만난 친구는 실루엣이에요.'
          : '아직 아무도 못 만났어요. 지도에서 県을 눌러보세요 — 진짜 ご当地キャラ가 살고 있어요!',
      ),
    );
    for (const r of regions) {
      const list = mascots.filter((m) => regionOf(prefBySlug.get(m.prefecture)!).id === r.id);
      if (!list.length) continue;
      wrap.append(el('h3', { class: 'zukan__region', lang: 'ja', style: `--c:${r.color}` }, r.name.ja, el('small', {}, ` ${r.name.ko}`)));
      const grid = el('div', { class: 'zukan' });
      for (const m of list) {
        const p = prefBySlug.get(m.prefecture)!;
        const has = found.has(m.id);
        const host = m.secret ? mascotById.get(m.secret) : undefined;
        const art = el('div', { class: 'zukan__art', 'aria-hidden': 'true' });
        art.innerHTML = mascotVisualHtml(m);
        const hint = !has && host && found.has(host.id) ? `힌트: ${host.name.ja} 톡톡톡` : null;
        const card = el(
          'button',
          {
            type: 'button',
            class: `zukan__card${has ? ' is-found' : ''}${m.kind === 'extra' ? ' is-extra' : ''}${m.secret ? ' is-secret' : ''}`,
            'data-slug': p.slug,
            // an undiscovered hidden friend must not be summoned from the book — show its host instead
            'data-mascot': !has && host ? host.id : m.id,
            'aria-label': has ? `${m.name.ja} (${p.name.ja})` : `??? (${p.name.ja})`,
          },
          art,
          has ? null : el('span', { class: 'zukan__q' }, '?'),
          el('span', { class: 'zukan__name', lang: 'ja' }, has ? m.name.ja : '？？？'),
          el('span', { class: 'zukan__pref' }, has ? m.org : hint ?? `${p.short.ja} · ${p.name.ko}`),
          m.secret ? el('span', { class: 'zukan__tag zukan__tag--secret' }, '숨은 친구') : has && m.kind === 'extra' ? el('span', { class: 'zukan__tag' }, '비공식') : null,
        );
        card.style.setProperty('--c', regionOf(p).color);
        grid.append(card);
      }
      wrap.append(grid);
    }
    wrap.append(el('p', { class: 'meta-line' }, '各キャラクターの権利は各自治体・団体に帰属します。크레딧이 없는 그림은 이 프로젝트가 그린 닮은꼴이에요.'));
    if (found.size === mascots.length) wrap.append(el('p', { class: 'zukan__done' }, '🎉 전부 만났어요! 컴플리트 — おめでとう！'));
    return wrap;
  }

  return {
    reveal,
    revealMascot,
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
