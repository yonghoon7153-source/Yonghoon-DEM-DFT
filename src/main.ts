import './styles/tokens.css';
import './styles/base.css';
import './styles/app.css';

import { mountains, places, prefBySlug, regionById, regions } from './data';
import { createMap, type MapApi } from './map/map';
import type { LayerId } from './map/layers';
import { artReady } from './mascots/visual';
import { el } from './ui/dom';
import { createCompass } from './ui/compass';
import { createEaster, createPetals } from './ui/easter';
import { createModal } from './ui/modal';
import { createPanel, renderGeneralMemo } from './ui/panel';
import { createSearch } from './ui/search';
import { createTooltip } from './ui/tooltip';
import type { LabelMode } from './types';

const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T;
const LABEL_KEY = 'nihonchizu.labelMode.v2'; // v2: ふりがな became the default
const isMobile = () => window.matchMedia('(max-width: 760px)').matches;
function readLabelMode(): LabelMode | null {
  try {
    const v = localStorage.getItem(LABEL_KEY);
    return v === 'furi' || v === 'ja' || v === 'kana' || v === 'ko' ? v : null;
  } catch {
    return null;
  }
}

const LAYER_KEY = 'nihonchizu.layers.v1';
function readLayers(): Partial<Record<LayerId, boolean>> {
  try {
    const v = JSON.parse(localStorage.getItem(LAYER_KEY) ?? '{}') as Record<string, unknown>;
    return { ...(typeof v.cities === 'boolean' ? { cities: v.cities } : {}), ...(typeof v.bridges === 'boolean' ? { bridges: v.bridges } : {}) };
  } catch {
    return {};
  }
}

const state = {
  selected: null as string | null,
  region: null as string | null,
  layers: { cities: true, bridges: true, mountains: false, ...readLayers() } as Record<LayerId, boolean>,
  range: { active: null as number | null, hide: false },
  labelMode: (readLabelMode() ?? 'furi') as LabelMode,
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
    rangeState: () => state.range,
    onRange: (no) => pickRange(no),
    onHideRangeNames: (hide) => {
      state.range.hide = hide;
      map?.setHideRangeNames(hide);
      panel.refresh();
    },
    onMountainsOff: () => mountainsOff(),
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

  function select(slug: string, opts: { animate?: boolean; mascot?: string } = {}) {
    if (!map || !easter || !prefBySlug.has(slug)) return;
    state.selected = slug;
    state.region = null;
    setLegendActive(null);
    map.highlightRegion(null);
    applyInset(true);
    map.selectPrefecture(slug, { animate: opts.animate });
    panel.showPrefecture(slug);
    easter.dismiss(true);
    setHash(slug);
    window.setTimeout(() => {
      if (state.selected === slug && easter) {
        easter.reveal(slug, opts.mascot);
        panel.refresh();
      }
    }, opts.animate === false ? 50 : 760);
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
    try {
      localStorage.setItem(LAYER_KEY, JSON.stringify({ cities: state.layers.cities, bridges: state.layers.bridges }));
    } catch {
      /* not remembered */
    }
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
  // a layer without data yet keeps its button out of sight
  const hasData: Record<LayerId, boolean> = { cities: places.cities.length > 0, bridges: places.bridges.length > 0, mountains: mountains.ranges.length > 0 };
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
      } else setLayer(id, !state.layers[id]);
    }),
  );
  for (const id of ['cities', 'bridges'] as const) setLayer(id, state.layers[id]);

  // ---- label mode
  const seg = $('label-mode');
  const compass = createCompass(stage, $('map-loading'));
  function setLabelMode(mode: LabelMode) {
    state.labelMode = mode;
    try {
      localStorage.setItem(LABEL_KEY, mode);
    } catch {
      /* private mode: the choice just is not remembered */
    }
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
  $('brand').addEventListener('click', () => {
    const on = petals.toggle();
    $('brand').title = on ? '벚꽃 그만 🌸' : '벚꽃 🌸';
  });

  createSearch($('search'), (slug) => select(slug));

  // ---- keyboard
  window.addEventListener('keydown', (e) => {
    const typing = (e.target as HTMLElement | null)?.tagName === 'INPUT';
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
    else if (h.startsWith('region/')) showRegion(h.slice(7));
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
