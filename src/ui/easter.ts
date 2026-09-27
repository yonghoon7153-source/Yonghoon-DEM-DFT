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
  // the mascots standing on the map right now — all from one prefecture, side by side; one of them talks
  let shown: { id: string; node: HTMLElement }[] = [];
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

  /** Stand the group next to each other on the prefecture's anchor. */
  function layout() {
    if (!slugShown || !shown.length) return;
    const pos = opts.map.anchorScreen(slugShown);
    if (!pos) return;
    const size = parseFloat(getComputedStyle(shown[0]!.node).getPropertyValue('--size')) || 112;
    const gap = size * 0.92;
    const flip = pos.x > opts.stage.clientWidth / 2;
    shown.forEach(({ node }, i) => {
      node.style.left = `${(pos.x + (i - (shown.length - 1) / 2) * gap).toFixed(1)}px`;
      node.style.top = `${pos.y}px`;
      node.classList.toggle('mascot--flip', flip);
    });
  }

  /** Only one speech bubble at a time: the mascot that was met or tapped last. */
  function speak(id: string) {
    for (const s of shown) s.node.classList.toggle('is-quiet', s.id !== id);
  }

  function restartTimer() {
    window.clearTimeout(hideTimer);
    hideTimer = window.setTimeout(() => dismiss(), 9000);
  }

  /** Show a prefecture's official mascot together with its unofficial friends (hidden friends stay hidden). */
  function reveal(slug: string, speaker?: string): boolean {
    const p = prefBySlug.get(slug);
    if (!p) return false;
    const group = mascots.filter((m) => m.prefecture === slug && !m.secret).sort((a, b) => (a.kind === b.kind ? 0 : a.kind === 'official' ? -1 : 1));
    if (!group.length) return false;
    dismiss(true);
    const first = speaker && group.some((m) => m.id === speaker) ? speaker : group[0]!.id;
    for (const m of group) add(m.id);
    speak(first);
    return true;
  }

  /** Show one mascot popping out of its prefecture; the others of the same prefecture stay beside it. */
  function revealMascot(id: string): boolean {
    const m = mascotById.get(id);
    if (!m) return false;
    if (m.prefecture !== slugShown) dismiss(true);
    const ok = add(id);
    if (ok) speak(id);
    return ok;
  }

  function add(id: string): boolean {
    const m = mascotById.get(id);
    if (!m) return false;
    const already = shown.find((s) => s.id === id);
    if (already) {
      sparkle(already.node);
      restartTimer();
      return true;
    }
    const art = mascotVisualHtml(m);
    if (!art) return false;
    const slug = m.prefecture;
    const isNew = !found.has(m.id);

    const n = el('div', { class: `mascot${m.secret ? ' mascot--secret' : ''}`, role: 'img', 'aria-label': `${m.name.ja} — ${m.line.ja}` });
    const artEl = el('div', { class: 'mascot__art' });
    artEl.innerHTML = art; // our own SVG likeness, or <img> of the official picture
    const lineJa = el('span', { class: 'b-line', lang: 'ja' }, m.line.ja);
    const lineKo = el('span', { class: 'b-ko' }, m.line.ko);
    const bubble = el(
      'div',
      { class: 'mascot__bubble' },
      el('span', { class: 'b-name' }, `${m.name.ja}`, el('span', { class: 'b-org' }, ` · ${m.org}`)),
      lineJa,
      lineKo,
      el('span', { class: 'b-tip' }, isNew ? (m.secret ? '✦ 숨은 친구를 찾았어요!' : '✦ 図鑑에 추가됐어요') : '또 만났다 ✿'),
    );
    n.append(artEl, bubble, el('span', { class: 'mascot__tag', lang: 'ja' }, m.name.ja));
    // Easter egg: a mascot with a hidden friend turns into it after three taps on the picture.
    const alter = m.secret ? undefined : secretFor(m);
    if (alter) {
      let taps = 0;
      artEl.addEventListener('click', (e) => {
        e.stopPropagation();
        taps++;
        speak(m.id);
        restartTimer();
        artEl.classList.remove('is-poked');
        void artEl.offsetWidth; // restart the animation
        artEl.classList.add('is-poked');
        if (m.poke && taps < 3) {
          lineJa.textContent = m.poke.ja;
          lineKo.textContent = m.poke.ko;
        }
        if (taps >= 3) {
          n.classList.add('is-darkening');
          window.setTimeout(() => {
            if (!shown.some((s) => s.node === n)) return;
            removeOne(m.id, true);
            if (add(alter.id)) speak(alter.id);
          }, 480);
        }
      });
    }
    // a quiet mascot starts talking when tapped; tapping the one that talks sends it off
    n.addEventListener('click', () => {
      if (n.classList.contains('is-quiet')) { speak(m.id); restartTimer(); }
      else removeOne(m.id);
    });
    opts.layer.append(n);
    shown.push({ id: m.id, node: n });
    slugShown = slug;
    layout();
    sparkle(n);

    if (isNew) {
      found.add(m.id);
      save();
      if (m.kind === 'official') opts.map.addSticker(slug, mascotSticker(m));
    }
    opts.onCount(found.size, mascots.length, isNew);
    restartTimer();
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

  function leave(n: HTMLElement, immediate: boolean) {
    if (immediate) n.remove();
    else {
      n.classList.add('is-leaving');
      setTimeout(() => n.remove(), 420);
    }
  }

  function removeOne(id: string, immediate = false) {
    const s = shown.find((x) => x.id === id);
    if (!s) return;
    shown = shown.filter((x) => x !== s);
    leave(s.node, immediate);
    if (!shown.length) { slugShown = null; window.clearTimeout(hideTimer); return; }
    if (!shown.some((x) => !x.node.classList.contains('is-quiet'))) speak(shown[shown.length - 1]!.id);
    layout();
  }

  function dismiss(immediate = false) {
    window.clearTimeout(hideTimer);
    const all = shown;
    shown = [];
    slugShown = null;
    for (const s of all) leave(s.node, immediate);
  }

  /** Keep the mascots glued to their prefecture while the map moves. */
  function reposition() {
    layout();
  }

  function collectionView(): HTMLElement {
    const wrap = el('div', {});
    wrap.append(el('h2', {}, el('span', { lang: 'ja' }, '図鑑'), el('small', {}, `ご当地キャラ 도감 ${found.size} / ${mascots.length}`)));
    wrap.append(
      el(
        'p',
        { class: 'lead' },
        found.size
          ? '県을 누르면 그 県의 친구들(공식 + 비공식)이 같이 튀어나와요. 누른 친구가 말을 해요. 아직 못 만난 친구는 실루엣이에요.'
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
    const drawn = mascots.some((m) => m.art === 'likeness');
    wrap.append(el('p', { class: 'meta-line' }, `各キャラクターの権利は各自治体・団体・企業に帰属します。${drawn ? '크레딧이 없는 그림은 이 프로젝트가 그린 닮은꼴이에요.' : ''}`));
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
