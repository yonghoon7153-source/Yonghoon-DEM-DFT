import './styles/tokens.css';
import './styles/base.css';
import './styles/app.css';

import { landmarkById, mountains, places, prefBySlug, regionById, regions, regionsInGroup, transit } from './data';
import { createMap, type MapApi } from './map/map';
import type { LayerId } from './map/layers';
import { artReady } from './mascots/visual';
import { el } from './ui/dom';
import { createCompass } from './ui/compass';
import { createEaster, createPetals } from './ui/easter';
import { createModal } from './ui/modal';
import { createPanel, renderGeneralMemo } from './ui/panel';
import { renderComments } from './ui/comments';
import { renderFestivals } from './ui/festivals';
import { createFx } from './ui/fx';
import { createSearch } from './ui/search';
import { createTooltip } from './ui/tooltip';
import { renderTokyo23, WARD_PREFECTURE } from './ui/tokyo23';
import type { LabelMode } from './types';

const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T;
const isMobile = () => window.matchMedia('(max-width: 760px)').matches;

// A reload starts from scratch (9차 요청): no stickers, 図鑑 0, ふりがな, default layers. Nothing is kept in the
// browser any more; what earlier versions stored is cleared once.
try {
  for (const k of ['nihonchizu.found.v1', 'nihonchizu.labelMode.v2', 'nihonchizu.labelMode.v1', 'nihonchizu.layers.v1']) localStorage.removeItem(k);
} catch {
  /* storage blocked: nothing to clear */
}

const state = {
  selected: null as string | null,
  region: null as string | null,
  layers: { cities: true, bridges: true, transit: false, mountains: false } as Record<LayerId, boolean>,
  range: { active: null as number | null, hide: false },
  transit: { active: null as string | null, hide: false },
  labelMode: 'furi' as LabelMode,
};

async function init() {
  const stage = $('stage');
  // Safari < 16 has no `overflow: clip`; undo any scroll the browser does on focus.
  const app = $('app');
  app.addEventListener('scroll', () => {
    if (app.scrollLeft || app.scrollTop) app.scrollTo(0, 0);
  });
  const tooltip = createTooltip($('tooltip'), stage);
  const modal = createModal($('modal'));
  const petals = createPetals($('petals'));
  const fx = createFx($('fx'));
  let map: MapApi | null = null;
  let easter: ReturnType<typeof createEaster> | null = null;

  const panel = createPanel($('panel'), {
    onClose: () => deselect(),
    onSelectPrefecture: (slug) => select(slug),
    onSelectRegion: (id) => showRegion(id),
    onRevealMascot: (id) => {
      if (!easter) return;
      easter.revealMascot(id);
      panel.refresh();
    },
    isMascotFound: (id) => easter?.isFound(id) ?? false,
    hasWardMap: (slug) => slug === WARD_PREFECTURE,
    onWardMap: (focus) => openWards(focus),
    rangeState: () => state.range,
    onRange: (no) => pickRange(no),
    onHideRangeNames: (hide) => {
      state.range.hide = hide;
      map?.setHideRangeNames(hide);
      panel.refresh();
    },
    onMountainsOff: () => mountainsOff(),
    transitState: () => state.transit,
    onLine: (id) => pickLine(id),
    onHideLineNames: (hide) => {
      state.transit.hide = hide;
      map?.setHideLineNames(hide);
      panel.refresh();
    },
    onTransitOff: () => transitOff(),
  });

  let hoverSlug: string | null = null;
  // While the map moves (zoom transitions, drags) the browser fires hover events for whatever slides
  // under a still cursor. Keep the tooltip hidden until the map has settled and the pointer moves.
  let lastZoomAt = 0;
  map = await createMap(
    $('map'),
    {
      onSelect: (slug) => select(slug),
      onHover: (slug, ev) => {
        if (!slug || !ev) {
          hoverSlug = null;
          tooltip.hide();
          return;
        }
        if (performance.now() - lastZoomAt < 250) return;
        if (slug !== hoverSlug) {
          hoverSlug = slug;
          tooltip.show(prefBySlug.get(slug)!, ev);
        } else tooltip.move(ev);
      },
      onZoom: () => {
        lastZoomAt = performance.now();
        if (hoverSlug) {
          hoverSlug = null;
          tooltip.hide();
        }
        easter?.reposition();
      },
      onRange: (no) => pickRange(no),
      onLine: (id) => pickLine(id),
      onLandmark: (id) => openLandmark(id),
    },
    state.labelMode,
  );
  await artReady; // fetched alongside the map; already settled when every mascot has a picture
  $('map-loading').remove();

  easter = createEaster({
    layer: $('mascot-layer'),
    stage,
    map,
    onCount: (n, total, isNew) => {
      $('collection-count').textContent = `${n}/${total}`;
      if (isNew) {
        panel.refresh();
        const b = $('collection-btn');
        b.classList.remove('is-celebrate');
        void b.offsetWidth;
        b.classList.add('is-celebrate');
      }
    },
  });

  // ---- layout: keep the selection visible next to the panel
  function applyInset(panelOpen: boolean) {
    document.getElementById('app')?.classList.toggle('has-panel', panelOpen);
    if (!map) return;
    if (!panelOpen) map.setInset({ right: 0, bottom: isMobile() ? 110 : 70, top: isMobile() ? 110 : 70 });
    else if (isMobile()) map.setInset({ right: 0, bottom: Math.round(stage.clientHeight * 0.58), top: 110 });
    else {
      const w = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--panel-w'), 10) || 420;
      map.setInset({ right: w + 28, bottom: 0, top: 70 });
    }
  }

  /** `quiet` — from a landmark sticker: the map stays as it is (no zooming out to the whole 県) and no mascot pops out. */
  function select(slug: string, opts: { animate?: boolean; mascot?: string; quiet?: boolean } = {}) {
    if (!map || !easter || !prefBySlug.has(slug)) return;
    state.selected = slug;
    state.region = null;
    setLegendActive(null);
    map.highlightRegion(null);
    applyInset(true);
    map.selectPrefecture(slug, { animate: opts.animate, zoom: !opts.quiet });
    panel.showPrefecture(slug);
    easter.dismiss(true);
    setHash(slug);
    if (opts.quiet) return;
    window.setTimeout(() => {
      if (state.selected === slug && easter) {
        easter.reveal(slug, opts.mascot);
        panel.refresh();
      }
    }, opts.animate === false ? 50 : 760);
    // Tokyo: the 23区 popup of my Canva page follows the zoom and the mascot (not on a page load from a link)
    if (slug === WARD_PREFECTURE && opts.animate !== false) {
      window.setTimeout(() => {
        if (state.selected === slug && !modal.isOpen()) openWards();
      }, 1400);
    }
  }
  function openWards(focus?: string) {
    modal.open(renderTokyo23(state.labelMode, focus), { wide: true });
  }
  /**
   * A landmark sticker was tapped: its prefecture's page opens and its box blinks (a 기본 정보 spot: its 観光 word in the
   * 図鑑); in 東京, the 23区 popup opens on its ward. The map stays where it is — no zooming out, no mascot (사용자:
   * 「지도 축소되면서 캐릭터 나오고 그거 안 해도 돼, 오히려 방해」) — and only slides if the panel would cover the sticker.
   */
  function openLandmark(id: string) {
    const l = landmarkById.get(id);
    if (!l) return;
    if (state.selected !== l.pref) select(l.pref, { quiet: true });
    if (modal.isOpen()) modal.close();
    map?.keepInView(l.at, l.pref);
    if (l.pref === WARD_PREFECTURE && l.ward) {
      openWards(l.ward);
      return;
    }
    window.setTimeout(() => panel.flashBox(l.box ?? l.spot ?? '', l.box === undefined), 250);
  }

  function deselect() {
    if (!map) return;
    state.selected = null;
    state.region = null;
    setLegendActive(null);
    map.highlightRegion(null);
    map.selectPrefecture(null, { zoom: false });
    easter?.dismiss();
    panel.close();
    applyInset(false);
    setHash('');
  }

  function showRegion(id: string) {
    if (!map || !regionById.has(id)) return;
    state.selected = null;
    state.region = id;
    easter?.dismiss(true);
    map.selectPrefecture(null, { zoom: false });
    applyInset(true);
    map.highlightRegion(id);
    map.focusRegion(id);
    panel.showRegion(id);
    setLegendActive(id);
    setHash(`region/${id}`);
  }

  // ---- legend
  const legend = $('legend');
  for (const r of regions) {
    const b = el('button', { type: 'button', 'data-region': r.id, style: `--c:${r.color}` }, el('span', { class: 'dot', 'aria-hidden': 'true' }), el('span', { class: 'ja', lang: 'ja' }, r.name.ja), el('span', { class: 'ko' }, r.name.ko));
    b.addEventListener('mouseenter', () => map?.highlightRegion(r.id));
    b.addEventListener('mouseleave', () => map?.highlightRegion(state.region));
    b.addEventListener('click', () => showRegion(r.id));
    legend.append(b);
  }
  function setLegendActive(id: string | null) {
    legend.querySelectorAll('button').forEach((b) => b.classList.toggle('is-active', b.dataset.region === id));
  }

  // ---- map layers: cities / bridges / mountain mode
  const layerBtns = $('layers').querySelectorAll<HTMLButtonElement>('button[data-layer]');
  function setLayer(id: LayerId, on: boolean) {
    state.layers[id] = on;
    map?.setLayer(id, on);
    layerBtns.forEach((b) => {
      if (b.dataset.layer === id) b.setAttribute('aria-pressed', String(on));
    });
  }
  function showMountains() {
    if (!map) return;
    setLayer('mountains', true);
    state.selected = null;
    state.region = null;
    easter?.dismiss(true);
    map.selectPrefecture(null, { zoom: false });
    map.highlightRegion(null);
    setLegendActive(null);
    applyInset(true);
    panel.showMountains();
    setHash('sanmyaku');
  }
  function mountainsOff() {
    setLayer('mountains', false);
    state.range.active = null;
    map?.setActiveRange(null);
    if (panel.current()?.type === 'mountains') {
      panel.close();
      applyInset(false);
      setHash('');
    }
  }
  function pickRange(no: number) {
    if (!map) return;
    if (!state.layers.mountains) setLayer('mountains', true);
    state.range.active = no;
    map.setActiveRange(no);
    if (panel.current()?.type !== 'mountains') showMountains();
    else panel.refresh();
    map.focusRange(no);
  }
  // 🚄 route mode — the same shape as the mountain mode: the button turns it on and off
  function showTransit() {
    if (!map) return;
    setLayer('transit', true);
    state.selected = null;
    state.region = null;
    easter?.dismiss(true);
    map.selectPrefecture(null, { zoom: false });
    map.highlightRegion(null);
    setLegendActive(null);
    applyInset(true);
    panel.showTransit();
    setHash('shinkansen');
  }
  function transitOff() {
    setLayer('transit', false);
    state.transit.active = null;
    map?.setActiveLine(null);
    if (panel.current()?.type === 'transit') {
      panel.close();
      applyInset(false);
      setHash('');
    }
  }
  function pickLine(id: string) {
    if (!map) return;
    if (!state.layers.transit) setLayer('transit', true);
    state.transit.active = id;
    map.setActiveLine(id);
    if (panel.current()?.type !== 'transit') showTransit();
    else panel.refresh();
    map.focusLine(id);
  }
  // a layer without data yet keeps its button out of sight
  const hasData: Record<LayerId, boolean> = { cities: places.cities.length > 0, bridges: places.bridges.length > 0, transit: transit.airports.length + transit.shinkansen.length > 0, mountains: mountains.ranges.length > 0 };
  layerBtns.forEach((b) => (b.hidden = !hasData[b.dataset.layer as LayerId]));
  $('layers').hidden = !Object.values(hasData).some(Boolean);
  layerBtns.forEach((b) =>
    b.addEventListener('click', () => {
      const id = b.dataset.layer as LayerId;
      if (id === 'mountains') {
        if (state.layers.mountains) mountainsOff();
        else {
          showMountains();
          map?.reset();
        }
      } else if (id === 'transit') {
        if (state.layers.transit) transitOff();
        else {
          showTransit();
          map?.reset();
        }
      } else setLayer(id, !state.layers[id]);
    }),
  );
  for (const id of ['cities', 'bridges', 'transit'] as const) setLayer(id, state.layers[id]);

  // ---- label mode
  const seg = $('label-mode');
  const compass = createCompass(stage, $('map-loading'));
  function setLabelMode(mode: LabelMode) {
    state.labelMode = mode;
    seg.querySelectorAll('button').forEach((b) => b.setAttribute('aria-checked', String(b.dataset.mode === mode)));
    map?.setLabelMode(mode);
    compass.setMode(mode);
  }
  seg.querySelectorAll('button').forEach((b) => b.addEventListener('click', () => setLabelMode(b.dataset.mode as LabelMode)));
  setLabelMode(state.labelMode);

  // ---- controls
  $('zoom-in').addEventListener('click', () => map?.zoomBy(1.6));
  $('zoom-out').addEventListener('click', () => map?.zoomBy(1 / 1.6));
  $('zoom-reset').addEventListener('click', () => {
    if (state.selected || state.region) deselect();
    map?.reset();
  });
  $('collection-btn').addEventListener('click', () => {
    if (!easter) return;
    const view = easter.collectionView();
    view.querySelectorAll<HTMLButtonElement>('.zukan__card').forEach((card) =>
      card.addEventListener('click', () => {
        modal.close();
        const id = card.dataset.mascot!;
        select(card.dataset.slug!, { mascot: id });
      }),
    );
    modal.open(view);
  });
  $('memo-btn').addEventListener('click', () => modal.open(renderGeneralMemo()));
  function openFestivals() {
    modal.open(renderFestivals({
      onPick: (f) => {
        modal.close();
        select(f.pref);
        // the burst lands once the map has flown to the prefecture
        window.setTimeout(() => {
          if (state.selected !== f.pref || !map) return;
          const at = map.anchorScreen(f.pref) ?? { x: stage.clientWidth / 2, y: stage.clientHeight / 2 };
          fx.play(f.fx, at);
        }, 820);
      },
    }));
  }
  $('matsuri-btn').addEventListener('click', openFestivals);
  $('comment-btn').addEventListener('click', () => modal.open(renderComments(state.selected)));
  $('brand').addEventListener('click', () => {
    const on = petals.toggle();
    $('brand').title = on ? '벚꽃 그만 🌸' : '벚꽃 🌸';
  });

  createSearch($('search'), (slug) => select(slug));

  // ---- keyboard
  window.addEventListener('keydown', (e) => {
    // writing somewhere (the search, a comment) — the one-key shortcuts must not steal the letters
    const t = e.target as HTMLElement | null;
    const typing = !!t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable);
    if (e.key === 'Escape') {
      if (modal.isOpen()) modal.close();
      else if (panel.isOpen()) deselect();
    } else if (e.key === '/' && !typing) {
      e.preventDefault();
      $('search-input').focus();
    } else if ((e.key === '+' || e.key === '=') && !typing) map?.zoomBy(1.4);
    else if (e.key === '-' && !typing) map?.zoomBy(1 / 1.4);
  });

  // ---- hash routing (#kyoto, #region/kinki)
  function setHash(h: string) {
    const next = h ? `#${h}` : ' ';
    if (h) history.replaceState(null, '', next);
    else history.replaceState(null, '', location.pathname + location.search);
  }
  function readHash() {
    const h = decodeURIComponent(location.hash.replace(/^#\/?/, ''));
    if (!h) return;
    if (h === 'sanmyaku' && mountains.ranges.length) showMountains();
    else if (h === 'shinkansen' && transit.shinkansen.length) showTransit();
    else if (h === 'matsuri') openFestivals();
    else if (h.startsWith('region/')) {
      // an old link to a big region (#region/chubu) opens its first travel region
      const id = h.slice(7);
      showRegion(regionById.has(id) ? id : regionsInGroup(id)[0]?.id ?? id);
    }
    else if (prefBySlug.has(h)) select(h, { animate: false });
  }
  window.addEventListener('hashchange', readHash);
  readHash();

  // keep inset sane when the viewport changes size class
  window.matchMedia('(max-width: 760px)').addEventListener('change', () => {
    applyInset(panel.isOpen());
    if (state.selected && map) map.selectPrefecture(state.selected, { animate: false });
  });
}

init().catch((err) => {
  console.error(err);
  const l = document.getElementById('map-loading');
  if (l) l.textContent = '지도를 불러오지 못했어요 … 새로고침 해주세요';
});
