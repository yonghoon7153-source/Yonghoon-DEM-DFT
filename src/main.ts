import './styles/tokens.css';
import './styles/base.css';
import './styles/app.css';

import { prefBySlug, regionById, regions } from './data';
import { createMap, type MapApi } from './map/map';
import { el } from './ui/dom';
import { createEaster, createPetals } from './ui/easter';
import { createModal } from './ui/modal';
import { createPanel, renderGeneralMemo } from './ui/panel';
import { createSearch } from './ui/search';
import { createTooltip } from './ui/tooltip';
import type { Lang } from './types';

const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T;
const LABEL_KEY = 'nihonchizu.labelMode';
const isMobile = () => window.matchMedia('(max-width: 760px)').matches;

const state = {
  selected: null as string | null,
  region: null as string | null,
  labelMode: ((localStorage.getItem(LABEL_KEY) as Lang | null) ?? 'ja') as Lang,
};

async function init() {
  const stage = $('stage');
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
  });

  let hoverSlug: string | null = null;
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
        if (slug !== hoverSlug) {
          hoverSlug = slug;
          tooltip.show(prefBySlug.get(slug)!, ev);
        } else tooltip.move(ev);
      },
      onZoom: () => easter?.reposition(),
    },
    state.labelMode,
  );
  $('map-loading').remove();

  easter = createEaster({
    layer: $('mascot-layer'),
    stage,
    map,
    onCount: (n, total, isNew) => {
      $('collection-count').textContent = `${n}/${total}`;
      if (isNew) {
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
        if (opts.mascot) easter.revealMascot(opts.mascot);
        else easter.reveal(slug);
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

  // ---- label mode
  const seg = $('label-mode');
  function setLabelMode(mode: Lang) {
    state.labelMode = mode;
    localStorage.setItem(LABEL_KEY, mode);
    seg.querySelectorAll('button').forEach((b) => b.setAttribute('aria-checked', String(b.dataset.mode === mode)));
    map?.setLabelMode(mode);
  }
  seg.querySelectorAll('button').forEach((b) => b.addEventListener('click', () => setLabelMode(b.dataset.mode as Lang)));
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
    if (h.startsWith('region/')) showRegion(h.slice(7));
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
