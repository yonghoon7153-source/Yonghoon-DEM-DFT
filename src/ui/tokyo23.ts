// 東京23区 popup, like the Tokyo page of my Canva: the 23-ward map, and tapping a ward pops up the boxes I hung
// from it. The ward shapes are public/geo/tokyo23.topo.json (nihon geo); names and my rank notes are places.json
// wards; the boxes are the ward boxes of my Tokyo mind map (matched by name), so nothing is written twice.
import { geoMercator, geoPath } from 'd3-geo';
import { select } from 'd3-selection';
import 'd3-transition';
import { zoom, zoomIdentity, type ZoomTransform } from 'd3-zoom';
import type { Feature, FeatureCollection, Geometry } from 'geojson';
import { feature } from 'topojson-client';
import type { GeometryCollection, Topology } from 'topojson-specification';
import { assetUrl } from '../asset-url';
import { landmarkSource, landmarks, notes, places, regionOf, prefBySlug } from '../data';
import { drawLandmark } from '../landmarks/art';
import type { LabelMode, NoteItem, Ward } from '../types';
import { clear, el } from './dom';
import { glossNote, photoSearch, renderTree } from './notes-render';

export const WARD_PREFECTURE = 'tokyo';
type WardFeature = Feature<Geometry, { ja: string }>;
const SVG = 'http://www.w3.org/2000/svg';

let shapes: Promise<WardFeature[]> | null = null;
function loadShapes(): Promise<WardFeature[]> {
  shapes ??= fetch(assetUrl('geo/tokyo23.topo.json'))
    .then((r) => {
      if (!r.ok) throw new Error(`tokyo23.topo.json ${r.status}`);
      return r.json() as Promise<Topology<{ wards: GeometryCollection<{ ja: string }> }>>;
    })
    .then((t) => (feature(t, t.objects.wards) as FeatureCollection<Geometry, { ja: string }>).features);
  return shapes;
}

/** My ward boxes (by ward name) and the other boxes that hang from the same list (多摩, the rankings…). */
function myWardBoxes(): { byWard: Map<string, NoteItem>; others: NoteItem[] } {
  const names = new Set(places.wards.map((w) => w.name.ja));
  const parentOf = (list: NoteItem[]): NoteItem | null => {
    for (const it of list) {
      if (it.children?.some((c) => names.has(c.t))) return it;
      const r = parentOf(it.children ?? []);
      if (r) return r;
    }
    return null;
  };
  const parent = parentOf(notes.prefectures[WARD_PREFECTURE]?.items ?? []);
  const byWard = new Map<string, NoteItem>();
  const others: NoteItem[] = [];
  for (const c of parent?.children ?? []) {
    if (names.has(c.t)) byWard.set(c.t, c);
    else others.push(c);
  }
  return { byWard, others };
}

function svg<K extends keyof SVGElementTagNameMap>(tag: K, attrs: Record<string, string | number> = {}): SVGElementTagNameMap[K] {
  const n = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, String(v));
  return n;
}

export function renderTokyo23(mode: LabelMode, focus?: string): HTMLElement {
  const pref = prefBySlug.get(WARD_PREFECTURE)!;
  const region = regionOf(pref);
  const style = { color: region.color, ink: region.ink };
  const { byWard, others } = myWardBoxes();
  const wardByJa = new Map(places.wards.map((w) => [w.name.ja, w]));

  const wrap = el('div', { class: 't23', style: `--c:${region.color};--ink-r:${region.ink}` });
  wrap.append(
    el('h2', {}, el('span', { lang: 'ja' }, '東京23区'), el('small', { lang: 'ja' }, 'とうきょうにじゅうさんく · 도쿄 23구')),
    el('p', { class: 'lead' }, `구를 누르면 그 구에 적어 둔 칸이 떠요 — 칸이 있는 구 ${byWard.size}곳은 진하게 · ＋ 로 확대하면 랜드마크가 나와요`),
  );
  // the ward map zooms (＋ −, pinch, drag): my landmark stickers come out once it is close (사용자: 「23구 확대했을 때만」)
  let zt: ZoomTransform = zoomIdentity;
  // the map, and beside it (below it on a narrow screen) the column where a ward's card pops out — never over the
  // map, as on my Canva page where the boxes hang outside the 23-ward map
  const stage = el('div', { class: 't23__stage' });
  const mapBox = el('div', { class: 't23__mapbox' }, el('p', { class: 't23__loading' }, '23区 지도를 펼치는 중…'));
  const hint = el('p', { class: 't23__hint' }, '← 구를 누르면 여기에 그 구의 칸이 떠요');
  const card = el('div', { class: 't23__card', role: 'dialog', 'aria-live': 'polite' });
  card.hidden = true;
  const side = el('div', { class: 't23__side' }, hint, card);
  stage.append(mapBox, side);
  wrap.append(stage);
  if (others.length) {
    wrap.append(el('section', { class: 't23__others' }, el('h3', {}, '그 밖에 적어 둔 것'), glossNote(others), renderTree(others, style)));
  }
  wrap.append(el('p', { class: 'meta-line' }, '地図: 地球地図日本（国土地理院）· 구 이름 · 순위 메모는 내 Canva 23区 지도에서'));

  let selected: SVGGElement | null = null;
  function closeCard() {
    card.hidden = true;
    hint.hidden = false;
    selected?.classList.remove('is-selected');
    selected = null;
  }

  function showCard(ja: string, g: SVGGElement, at: [number, number]) {
    const ward = wardByJa.get(ja);
    const box = byWard.get(ja);
    selected?.classList.remove('is-selected');
    selected = g;
    g.classList.add('is-selected');
    clear(card);
    const close = el('button', { type: 'button', class: 't23__close', 'aria-label': '닫기' }, '×');
    close.addEventListener('click', closeCard);
    // my own box first (its reading and Korean box are my words), the map data when I wrote nothing
    const kana = box?.sub ?? ward?.name.kana ?? '';
    const ko = box?.ko ?? ward?.name.ko ?? '';
    card.append(
      close,
      el('div', { class: 't23__head' },
        el('span', { class: 't23__name', lang: 'ja' }, el('small', {}, kana), ja),
        ko ? el('span', { class: 't23__ko' }, ko) : null,
        photoSearch(`${ja} 東京`)),
    );
    if (ward?.note) card.append(el('p', { class: 't23__note', lang: 'ja' }, ward.note));
    const kids = box?.children ?? [];
    const gn = kids.length ? glossNote(kids) : null;
    if (gn) card.append(gn);
    if (kids.length) card.append(renderTree(kids, style));
    else card.append(el('p', { class: 'empty' }, box ? '구 이름만 적어 둔 칸이에요' : '아직 적어 둔 칸이 없어요 ✿'));
    card.hidden = false;
    hint.hidden = true;
    card.style.animation = 'none';
    void card.offsetWidth; // pop again for every ward
    card.style.animation = '';
    // in the column beside the map, level with the tapped ward; below the map when there is no room beside it
    card.style.top = '';
    card.scrollTop = 0;
    if (getComputedStyle(card).position === 'absolute') {
      const svgEl = mapBox.querySelector('svg');
      const k = svgEl ? svgEl.getBoundingClientRect().width / (Number(svgEl.getAttribute('width')) || 1) : 1;
      const y = zt.apply(at)[1]; // where the ward is now, zoomed
      card.style.top = `${Math.max(0, Math.min(y * k - 30, side.clientHeight - card.offsetHeight))}px`;
    } else {
      card.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  loadShapes()
    .then((features) => {
      mapBox.querySelector('.t23__loading')?.remove();
      const W = Math.max(280, mapBox.clientWidth || 700);
      const H = Math.round(W * 0.8);
      const projection = geoMercator().fitExtent([[8, 8], [W - 8, H - 8]], { type: 'FeatureCollection', features });
      const path = geoPath(projection);
      const map = svg('svg', { class: 't23__map', viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: 'img', 'aria-label': '도쿄 23구 지도' });
      const shapesG = svg('g');
      const labelsG = svg('g', { class: 't23__labels' });
      // on a phone-sized map the central wards are tiny: short names only (the card has the reading)
      const small = W < 520;
      let focusAt: { g: SVGGElement; at: [number, number] } | null = null;
      const wardAt = new Map<string, { g: SVGGElement; at: [number, number] }>();
      for (const f of features) {
        const ja = f.properties.ja;
        const ward = wardByJa.get(ja);
        const g = svg('g', { class: `t23__ward${byWard.has(ja) ? ' has-notes' : ''}`, tabindex: 0, role: 'button', 'aria-label': ja });
        g.append(svg('path', { d: path(f) ?? '' }));
        const title = svg('title');
        title.textContent = `${ja}${ward ? ` (${ward.name.kana}) ${ward.name.ko}` : ''}`;
        g.append(title);
        shapesG.append(g);

        const [cx, cy] = path.centroid(f);
        const text = svg('text', { x: cx.toFixed(1), y: cy.toFixed(1), class: `t23__label${ward?.mark ? ' is-red' : ''}`, 'font-size': small ? 10 : 12 });
        const full = mode === 'kana' ? ward?.name.kana ?? ja : mode === 'ko' ? ward?.name.ko ?? ja : ja;
        const main = small ? full.replace(/(区|く|구)$/, '') : full;
        if (mode === 'furi' && ward && !small) {
          const furi = svg('tspan', { x: cx.toFixed(1), dy: '-1.15em', class: 't23__furi' });
          furi.textContent = ward.name.kana;
          text.append(furi);
        }
        const m = svg('tspan', { x: cx.toFixed(1), dy: mode === 'furi' && ward && !small ? '1.25em' : '0.35em', class: 't23__main' });
        m.textContent = main;
        text.append(m);
        // the rank notes (犯罪率↓ 3위 …) stay in the ward's card and the rankings below the map, not on it (사용자)
        labelsG.append(text);

        const open = () => showCard(ja, g, [cx, cy]);
        wardAt.set(ja, { g, at: [cx, cy] });
        if (ja === focus) focusAt = { g, at: [cx, cy] };
        g.addEventListener('click', (e) => { e.stopPropagation(); open(); });
        g.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
        });
      }
      // my Tokyo landmarks as the same stickers as on the map, where they are; a tap opens the ward they hang from
      const stickersG = svg('g', { class: 't23__landmarks' });
      const r = small ? 12 : 16;
      const stickers: { g: SVGGElement; base: string }[] = [];
      landmarks.filter((l) => l.pref === WARD_PREFECTURE).forEach((l, i) => {
        const p = projection(l.at);
        const ward = l.ward ? wardAt.get(l.ward) : undefined;
        if (!p || !ward) return;
        const base = `translate(${p[0].toFixed(1)},${p[1].toFixed(1)}) rotate(${((i * 7) % 11) - 5})`;
        const g = svg('g', { class: `landmark${landmarkSource(l) === 'supplement' ? ' is-sup' : ''}`, role: 'button', tabindex: 0, 'aria-label': l.name.ja, transform: base });
        stickers.push({ g, base });
        const art = svg('g', { class: 'landmark__art', transform: `scale(${((2 * r) / 100).toFixed(3)}) translate(-50,-50)` });
        drawLandmark(art, l.icon);
        g.append(art);
        const title = svg('title');
        title.textContent = `${l.name.ja} (${l.name.kana}) ${l.name.ko} — ${l.ward}`;
        g.append(title);
        // the ward's card opens and, inside it, this place's own box blinks (as on the map's panel)
        const open = () => {
          showCard(l.ward!, ward.g, ward.at);
          const chip = [...card.querySelectorAll<HTMLElement>('.nchip__t')].find((e) => e.textContent === l.box)?.closest<HTMLElement>('.nchip');
          if (!chip) return;
          chip.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
          chip.classList.remove('is-flash');
          void chip.offsetWidth;
          chip.classList.add('is-flash');
        };
        g.addEventListener('click', (e) => { e.stopPropagation(); open(); });
        g.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
        });
        stickersG.append(g);
      });
      // everything in one zoomed group; the names and stickers keep their size on screen as it grows
      const viewport = svg('g', { class: 't23__viewport' });
      viewport.append(shapesG, stickersG, labelsG); // the ward names stay readable over the stickers
      map.append(viewport);
      map.addEventListener('click', closeCard);
      const labelFs = small ? 10 : 12;
      const STICKERS_AT = 1.7;
      const zoomHint = el('p', { class: 't23__zoomhint' }, '🔍 ＋ 로 확대하면 랜드마크가 나와요');
      const plus = el('button', { type: 'button', 'aria-label': '확대' }, '+');
      const minus = el('button', { type: 'button', 'aria-label': '축소' }, '−');
      const apply = () => {
        viewport.setAttribute('transform', zt.toString());
        map.style.setProperty('--t23-k', String(zt.k));
        labelsG.querySelectorAll('text').forEach((t) => t.setAttribute('font-size', (labelFs / zt.k).toFixed(2)));
        for (const s of stickers) s.g.setAttribute('transform', `${s.base} scale(${(1 / zt.k).toFixed(4)})`);
        const on = zt.k >= STICKERS_AT;
        stickersG.style.display = on ? '' : 'none';
        zoomHint.hidden = on;
        minus.toggleAttribute('disabled', zt.k <= 1.01);
      };
      // buttons, pinch and drag; the wheel keeps scrolling the popup (never zooms it by surprise), no double-click zoom
      const zb = zoom<SVGSVGElement, unknown>().scaleExtent([1, 6]).translateExtent([[0, 0], [W, H]]).clickDistance(5)
        .filter((e: Event) => e.type !== 'wheel' && !(e as MouseEvent).button)
        .on('zoom', (e: { transform: ZoomTransform }) => { zt = e.transform; apply(); });
      const mapSel = select<SVGSVGElement, unknown>(map as SVGSVGElement).call(zb).on('dblclick.zoom', null);
      plus.addEventListener('click', () => mapSel.transition().duration(280).call(zb.scaleBy, 1.7));
      minus.addEventListener('click', () => mapSel.transition().duration(280).call(zb.scaleBy, 1 / 1.7));
      mapBox.append(map, zoomHint, el('div', { class: 't23__zoom', role: 'group', 'aria-label': '23区 지도 확대/축소' }, plus, minus));
      apply();
      const f = focusAt as { g: SVGGElement; at: [number, number] } | null;
      if (f && focus) showCard(focus, f.g, f.at);
    })
    .catch(() => {
      const l = mapBox.querySelector('.t23__loading');
      if (l) l.textContent = '23区 지도를 불러오지 못했어요 — 새로고침해 보세요';
    });
  return wrap;
}
