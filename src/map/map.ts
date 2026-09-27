// Interactive SVG map: projection, zoom/pan, labels in screen space, selection & hover.
import { geoMercator, geoPath, type GeoProjection } from 'd3-geo';
import { select, type Selection } from 'd3-selection';
import { zoom, zoomIdentity, type ZoomBehavior, type ZoomTransform } from 'd3-zoom';
import 'd3-transition';
import { feature, merge, mesh } from 'topojson-client';
import type { GeometryCollection, MultiPolygon as TopoMultiPolygon, Polygon as TopoPolygon, Topology } from 'topojson-specification';
import type { Feature, FeatureCollection, MultiPolygon } from 'geojson';
import { prefById, prefGeo, prefectures, prefecturesIn, regionOf, regions } from '../data';
import type { LabelMode, LonLat, Prefecture } from '../types';
import { createLayers, type LayerId } from './layers';

export interface MapCallbacks {
  onSelect(slug: string): void;
  onHover(slug: string | null, event?: MouseEvent): void;
  onZoom?(k: number): void;
  onRange?(no: number): void;
}

export interface MapApi {
  container: HTMLElement;
  selectPrefecture(slug: string | null, opts?: { animate?: boolean; zoom?: boolean }): void;
  focusRegion(regionId: string): void;
  highlightRegion(regionId: string | null): void;
  setLabelMode(mode: LabelMode): void;
  zoomBy(factor: number): void;
  reset(animate?: boolean): void;
  setInset(inset: Partial<Inset>): void;
  anchorScreen(slug: string): { x: number; y: number } | null;
  addSticker(slug: string, visual: { image?: string; svg?: string }): void;
  currentScale(): number;
  setLayer(id: LayerId, on: boolean): void;
  setActiveRange(no: number | null): void;
  setHideRangeNames(hide: boolean): void;
  focusRange(no: number): void;
}

interface Inset { top: number; right: number; bottom: number; left: number }
type PrefFeature = Feature<MultiPolygon, { id: number; ja: string }>;
interface JapanTopology extends Topology { objects: { japan: GeometryCollection<{ id: number; ja: string }> } }

/** Manual nudges (lon, lat degrees) for labels whose centroid sits awkwardly. */
const LABEL_NUDGE: Record<string, [number, number]> = {
  hokkaido: [0.35, -0.15],
  nagasaki: [-0.1, 0.1],
  kagoshima: [0.05, 0.35],
  hyogo: [0, 0.05],
  tokyo: [0.1, 0.02],
  okinawa: [0.15, -0.05],
};

export function shortLabel(p: Prefecture, mode: LabelMode): string {
  if (mode === 'ja' || mode === 'furi') return p.short.ja;
  if (mode === 'kana') return p.short.kana;
  if (p.slug === 'hokkaido') return p.name.ko;
  return p.name.ko.replace(/(현|도|부)$/, '');
}

export async function createMap(container: HTMLElement, cb: MapCallbacks, initialMode: LabelMode): Promise<MapApi> {
  const url = `${import.meta.env.BASE_URL}geo/japan.topo.json`;
  const topo = (await fetch(url).then((r) => {
    if (!r.ok) throw new Error(`geo ${r.status}`);
    return r.json();
  })) as JapanTopology;

  const fc = feature(topo, topo.objects.japan) as unknown as FeatureCollection<MultiPolygon, { id: number; ja: string }>;
  const features = fc.features as PrefFeature[];
  const union = merge(topo, topo.objects.japan.geometries as (TopoPolygon | TopoMultiPolygon)[]);
  const innerBorders = mesh(topo, topo.objects.japan, (a, b) => a !== b);
  const coast = mesh(topo, topo.objects.japan, (a, b) => a === b);
  const bySlug = new Map<string, PrefFeature>();
  for (const f of features) {
    const p = prefById.get(f.properties.id);
    if (p) bySlug.set(p.slug, f);
  }

  let W = Math.max(320, container.clientWidth);
  let H = Math.max(320, container.clientHeight);
  let inset: Inset = { top: 70, right: 0, bottom: 70, left: 0 };
  let transform: ZoomTransform = zoomIdentity;
  let labelMode: LabelMode = initialMode;
  let selected: string | null = null;
  let hovered: string | null = null;
  let highlightedRegion: string | null = null;

  const projection: GeoProjection = geoMercator();
  const path = geoPath(projection);

  const svg = select(container).append('svg').attr('class', 'map-svg').attr('role', 'presentation');
  const viewport = svg.append('g').attr('class', 'viewport');
  const gWash = viewport.append('g').attr('class', 'wash');
  const gLand = viewport.append('g').attr('class', 'land');
  const gLines = viewport.append('g').attr('class', 'lines');
  const gGeoLayers = viewport.append('g').attr('class', 'geo-layers');
  const gInset = viewport.append('g').attr('class', 'inset');
  const gScreen = svg.append('g').attr('class', 'screen');
  const gMarks = gScreen.append('g').attr('class', 'marks');
  const gStickers = gScreen.append('g').attr('class', 'stickers');
  const gLabels = gScreen.append('g').attr('class', 'labels');
  const gLayerText = gScreen.append('g').attr('class', 'layer-text');
  const okinawaShift = ((topo as unknown as { meta?: { okinawaShift?: LonLat } }).meta?.okinawaShift ?? [-0.6, 5.4]) as LonLat;
  const layers = createLayers({ geo: gGeoLayers, marks: gMarks, text: gLayerText, projection, okinawaShift, onRange: (no) => cb.onRange?.(no) });

  gWash.append('path').attr('class', 'sea-halo sea-halo--wide');
  gWash.append('path').attr('class', 'sea-halo');
  gWash.append('path').attr('class', 'land-shadow');
  gWash.append('path').attr('class', 'sticker-halo');

  const prefPaths: Selection<SVGPathElement, PrefFeature, SVGGElement, unknown> = gLand
    .selectAll<SVGPathElement, PrefFeature>('path')
    .data(features, (d) => String(d.properties.id))
    .join('path')
    .attr('class', 'pref')
    .attr('data-slug', (d) => prefById.get(d.properties.id)?.slug ?? '')
    .attr('tabindex', 0)
    .attr('role', 'button')
    .attr('aria-label', (d) => {
      const p = prefById.get(d.properties.id)!;
      return `${p.name.ja} ${p.name.kana} ${p.name.ko}`;
    })
    .style('fill', (d) => regionOf(prefById.get(d.properties.id)!).color)
    .style('--hover-fill', (d) => `color-mix(in oklab, ${regionOf(prefById.get(d.properties.id)!).color} 80%, white)`);

  gLines.append('path').attr('class', 'border-inner');
  gLines.append('path').attr('class', 'coast');
  gInset.append('rect').attr('class', 'inset-frame').attr('rx', 10);

  // ---- events on prefectures
  prefPaths
    .on('mouseenter', function (event: MouseEvent, d) {
      const slug = prefById.get(d.properties.id)!.slug;
      setHover(slug);
      cb.onHover(slug, event);
    })
    .on('mousemove', (event: MouseEvent, d) => cb.onHover(prefById.get(d.properties.id)!.slug, event))
    .on('mouseleave', () => {
      setHover(null);
      cb.onHover(null);
    })
    .on('click', (event: MouseEvent, d) => {
      event.stopPropagation();
      cb.onSelect(prefById.get(d.properties.id)!.slug);
    })
    .on('keydown', (event: KeyboardEvent, d) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        cb.onSelect(prefById.get(d.properties.id)!.slug);
      }
    });

  // ---- labels (screen space)
  interface LabelDatum { p: Prefecture; kind: 'pref' }
  interface RegionLabelDatum { id: string; ja: string; kana: string; ko: string; ink: string; anchor: [number, number] }
  const regionLabelData: RegionLabelDatum[] = regions.map((r) => {
    const members = prefecturesIn(r.id);
    const pts = members.map((p) => prefGeo[String(p.id)]!.anchor);
    const anchor: [number, number] = [pts.reduce((s, a) => s + a[0], 0) / pts.length, pts.reduce((s, a) => s + a[1], 0) / pts.length];
    return { id: r.id, ja: r.name.ja, kana: r.name.kana, ko: r.name.ko, ink: r.ink, anchor };
  });
  // nudge a few region labels into open water so they do not cover prefecture names
  const REGION_NUDGE: Record<string, [number, number]> = {
    hokkaido: [0.5, 2.3], tohoku: [2.4, 0.2], kanto: [2.0, -1.0], chubu: [-1.0, 1.4], kinki: [0.5, -1.8],
    chugoku: [-0.2, 1.1], shikoku: [0.2, -1.2], kyushu: [1.8, -0.9], okinawa: [0, 1.9],
  };
  for (const r of regionLabelData) {
    const n = REGION_NUDGE[r.id];
    if (n) r.anchor = [r.anchor[0] + n[0], r.anchor[1] + n[1]];
  }

  const regionLabels = gLabels
    .selectAll<SVGTextElement, RegionLabelDatum>('text.label--region')
    .data(regionLabelData, (d) => d.id)
    .join('text')
    .attr('class', 'label label--region')
    .attr('lang', 'ja')
    .style('--label-ink', (d) => d.ink);
  regionLabels.append('tspan').attr('class', 'label__furi').attr('x', 0).attr('y', '-1.55em');
  regionLabels.append('tspan').attr('class', 'label__main').attr('x', 0).attr('y', 0);

  const prefLabels = gLabels
    .selectAll<SVGTextElement, LabelDatum>('text.label--pref')
    .data(prefectures.map((p) => ({ p, kind: 'pref' as const })), (d) => d.p.slug)
    .join('text')
    .attr('class', 'label label--pref')
    .attr('data-slug', (d) => d.p.slug)
    .style('--label-ink', (d) => regionOf(d.p).ink);
  // ふりがな: the reading sits above the name in a smaller size (em = its own size, so it follows is-active)
  prefLabels.append('tspan').attr('class', 'label__furi').attr('x', 0).attr('y', '-1.45em');
  prefLabels.append('tspan').attr('class', 'label__main').attr('x', 0).attr('y', 0);
  function writeLabels() {
    const furi = labelMode === 'furi';
    prefLabels.select('.label__main').text((d) => shortLabel(d.p, labelMode));
    prefLabels.select('.label__furi').text((d) => (furi ? d.p.short.kana : ''));
    regionLabels.select('.label__main').text((d) => (labelMode === 'ko' ? `${d.ko} 지방` : labelMode === 'kana' ? `${d.kana}ちほう` : `${d.ja}地方`));
    regionLabels.select('.label__furi').text((d) => (furi ? `${d.kana}ちほう` : ''));
  }
  writeLabels();

  const insetNote = gLabels.append('text').attr('class', 'label label--note').text('↙ 沖縄はほんとはもっと南西 (인셋)');

  // ---- projection fit & drawing
  const okinawa = bySlug.get('okinawa')!;
  let okinawaBox: [[number, number], [number, number]] = [[0, 0], [0, 0]];

  function fitProjection() {
    projection.fitExtent([[24, 24], [W - 24, H - 24]], fc);
    prefPaths.attr('d', (d) => path(d) ?? '');
    const unionD = path(union) ?? '';
    gWash.selectAll('path').attr('d', unionD);
    gLines.select('.border-inner').attr('d', path(innerBorders) ?? '');
    gLines.select('.coast').attr('d', path(coast) ?? '');
    okinawaBox = path.bounds(okinawa);
    gInset
      .select('rect')
      .attr('x', okinawaBox[0][0] - 14)
      .attr('y', okinawaBox[0][1] - 14)
      .attr('width', okinawaBox[1][0] - okinawaBox[0][0] + 28)
      .attr('height', okinawaBox[1][1] - okinawaBox[0][1] + 28);
    layers.refit();
  }

  // projected anchors (cached per fit)
  const anchorPx = new Map<string, [number, number]>();
  const boxPx = new Map<string, [number, number]>(); // core bbox size in px at k=1
  function cacheAnchors() {
    for (const p of prefectures) {
      const g = prefGeo[String(p.id)]!;
      const n = LABEL_NUDGE[p.slug] ?? [0, 0];
      const pt = projection([g.anchor[0] + n[0], g.anchor[1] + n[1]]);
      if (pt) anchorPx.set(p.slug, [pt[0], pt[1]]);
      const a = projection([g.coreBbox[0], g.coreBbox[3]]);
      const b = projection([g.coreBbox[2], g.coreBbox[1]]);
      if (a && b) boxPx.set(p.slug, [Math.abs(b[0] - a[0]), Math.abs(b[1] - a[1])]);
    }
  }

  // ---- zoom
  const zoomBehavior: ZoomBehavior<SVGSVGElement, unknown> = zoom<SVGSVGElement, unknown>()
    .scaleExtent([0.8, 16])
    .clickDistance(5)
    .on('zoom', (event) => {
      transform = event.transform as ZoomTransform;
      viewport.attr('transform', transform.toString());
      updateScreenSpace();
      cb.onZoom?.(transform.k);
    });
  svg.call(zoomBehavior).on('dblclick.zoom', null);
  svg.on('click', () => {
    /* clicking the sea keeps the selection; nothing to do */
  });

  // ---- screen-space update (labels & stickers)
  function updateScreenSpace() {
    const k = transform.k;
    const placed: { x: number; y: number; w: number; h: number }[] = [];
    regionLabels.classed('is-hidden', (d) => d.id !== highlightedRegion || k > 3).attr('transform', (d) => {
      const pt = projection(d.anchor)!;
      const [x, y] = transform.apply([pt[0], pt[1]]);
      return `translate(${x.toFixed(1)},${y.toFixed(1)})`;
    });

    const order = prefectures
      .map((p) => ({ p, box: boxPx.get(p.slug) ?? [0, 0] }))
      .sort((a, b) => {
        const pa = a.p.slug === selected || a.p.slug === hovered ? 1 : 0;
        const pb = b.p.slug === selected || b.p.slug === hovered ? 1 : 0;
        return pb - pa || b.box[0] * b.box[1] - a.box[0] * a.box[1];
      });
    const visible = new Set<string>();
    for (const { p, box } of order) {
      const a = anchorPx.get(p.slug);
      if (!a) continue;
      const [x, y] = transform.apply(a);
      const text = shortLabel(p, labelMode);
      const fs = p.slug === selected || p.slug === hovered ? 14 : 12;
      const furi = labelMode === 'furi';
      const w = Math.max(text.length * fs * 1.02, furi ? p.short.kana.length * fs * 0.68 * 1.02 : 0) + 6;
      const top = furi ? fs * 1.33 : fs / 2; // the reading line adds height above the name
      const h = top + fs / 2 + 6;
      const force = p.slug === selected || p.slug === hovered;
      const fits = box[1] * k >= (furi ? 22 : 16) && box[0] * k >= w * 0.45;
      const rect = { x: x - w / 2, y: y - top - 3, w, h };
      const collides = placed.some((r) => r.x < rect.x + rect.w && r.x + r.w > rect.x && r.y < rect.y + rect.h && r.y + r.h > rect.y);
      const onScreen = x > -40 && x < W + 40 && y > -20 && y < H + 20;
      if (onScreen && (force || (fits && !collides))) {
        visible.add(p.slug);
        placed.push(rect);
      }
    }
    prefLabels
      .classed('is-hidden', (d) => !visible.has(d.p.slug))
      .classed('is-active', (d) => d.p.slug === selected || d.p.slug === hovered)
      .attr('transform', (d) => {
        const a = anchorPx.get(d.p.slug)!;
        const [x, y] = transform.apply(a);
        return `translate(${x.toFixed(1)},${y.toFixed(1)})`;
      });

    layers.update({ t: transform, placed, W, H, mode: labelMode, selected, region: highlightedRegion });

    const [ix, iy] = transform.apply([okinawaBox[0][0] - 14, okinawaBox[1][1] + 14]);
    insetNote.attr('transform', `translate(${ix.toFixed(1)},${(iy + 11).toFixed(1)})`).classed('is-hidden', k > 2.2);

    gStickers.selectAll<SVGGElement, string>('g.sticker').attr('transform', function () {
      const slug = this.dataset.slug!;
      const a = anchorPx.get(slug)!;
      const [x, y] = transform.apply(a);
      return `translate(${(x + 14).toFixed(1)},${(y - 16).toFixed(1)})`;
    });
  }

  function setHover(slug: string | null) {
    hovered = slug;
    prefPaths.classed('is-hover', (d) => prefById.get(d.properties.id)!.slug === slug);
    updateScreenSpace();
  }

  // ---- fitting helpers
  function visibleExtent(): [[number, number], [number, number]] {
    return [[inset.left, inset.top], [W - inset.right, H - inset.bottom]];
  }

  function transformFor(bounds: [[number, number], [number, number]], padding: number, maxK = 16): ZoomTransform {
    const [[x0, y0], [x1, y1]] = bounds;
    const [[vx0, vy0], [vx1, vy1]] = visibleExtent();
    const vw = Math.max(80, vx1 - vx0 - padding * 2);
    const vh = Math.max(80, vy1 - vy0 - padding * 2);
    const k = Math.min(maxK, Math.max(0.8, Math.min(vw / Math.max(1, x1 - x0), vh / Math.max(1, y1 - y0))));
    const cx = (x0 + x1) / 2;
    const cy = (y0 + y1) / 2;
    const tx = (vx0 + vx1) / 2 - cx * k;
    const ty = (vy0 + vy1) / 2 - cy * k;
    return zoomIdentity.translate(tx, ty).scale(k);
  }

  function applyTransform(t: ZoomTransform, animate: boolean, duration = 700) {
    if (animate) svg.transition().duration(duration).call(zoomBehavior.transform, t);
    else svg.call(zoomBehavior.transform, t);
  }

  function boundsOf(slug: string, core = true): [[number, number], [number, number]] {
    const p = prefById.get(prefectures.find((q) => q.slug === slug)!.id)!;
    const g = prefGeo[String(p.id)]!;
    const bb = core ? g.coreBbox : g.bbox;
    const a = projection([bb[0], bb[3]])!;
    const b = projection([bb[2], bb[1]])!;
    return [[Math.min(a[0], b[0]), Math.min(a[1], b[1])], [Math.max(a[0], b[0]), Math.max(a[1], b[1])]];
  }

  /** Union of the prefectures' core boxes: far-flung islands do not shrink the initial view. */
  function fullBounds(): [[number, number], [number, number]] {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const p of prefectures) {
      const b = boundsOf(p.slug);
      x0 = Math.min(x0, b[0][0]); y0 = Math.min(y0, b[0][1]);
      x1 = Math.max(x1, b[1][0]); y1 = Math.max(y1, b[1][1]);
    }
    return [[x0, y0], [x1, y1]];
  }

  // ---- public api
  function selectPrefecture(slug: string | null, opts: { animate?: boolean; zoom?: boolean } = {}) {
    selected = slug;
    prefPaths.classed('is-selected', (d) => prefById.get(d.properties.id)!.slug === slug);
    if (slug) {
      // raise the selected path so its accent stroke is not hidden by neighbours
      const node = gLand.select<SVGPathElement>(`path[data-slug="${slug}"]`).node();
      node?.parentNode?.appendChild(node);
      if (opts.zoom !== false) {
        const b = boundsOf(slug);
        const wide = b[1][0] - b[0][0] > 40 || b[1][1] - b[0][1] > 40;
        let t = transformFor(b, wide ? 60 : 90, 7.5);
        // keep the label anchor (where the mascot pops out) well inside the visible area
        const a = anchorPx.get(slug);
        if (a) {
          const [, ay] = t.apply(a);
          const [[, vy0], [, vy1]] = visibleExtent();
          const phone = W <= 760; // on phones the bubble is a strip above the sheet, so keep the anchor above it
          const minY = vy0 + (phone ? 100 : 150), maxY = vy1 - (phone ? 120 : 40);
          if (ay < minY) t = zoomIdentity.translate(t.x, t.y + (minY - ay)).scale(t.k);
          else if (ay > maxY) t = zoomIdentity.translate(t.x, t.y - (ay - maxY)).scale(t.k);
        }
        applyTransform(t, opts.animate !== false);
      }
    }
    updateScreenSpace();
  }

  function focusRegion(regionId: string) {
    const members = prefecturesIn(regionId);
    let bx0 = Infinity, by0 = Infinity, bx1 = -Infinity, by1 = -Infinity;
    for (const p of members) {
      const b = boundsOf(p.slug);
      bx0 = Math.min(bx0, b[0][0]); by0 = Math.min(by0, b[0][1]);
      bx1 = Math.max(bx1, b[1][0]); by1 = Math.max(by1, b[1][1]);
    }
    applyTransform(transformFor([[bx0, by0], [bx1, by1]], 50, 6), true);
  }

  function highlightRegion(regionId: string | null) {
    highlightedRegion = regionId;
    prefPaths.classed('is-dim', (d) => !!regionId && prefById.get(d.properties.id)!.region !== regionId);
    updateScreenSpace();
  }

  function setLabelMode(mode: LabelMode) {
    labelMode = mode;
    writeLabels();
    updateScreenSpace();
  }

  function zoomBy(factor: number) {
    svg.transition().duration(300).call(zoomBehavior.scaleBy, factor);
  }

  function reset(animate = true) {
    applyTransform(transformFor(fullBounds(), 14, 16), animate, 800);
  }

  function setInset(next: Partial<Inset>) {
    inset = { ...inset, ...next };
  }

  function anchorScreen(slug: string) {
    const a = anchorPx.get(slug);
    if (!a) return null;
    const [x, y] = transform.apply(a);
    return { x, y };
  }

  function addSticker(slug: string, visual: { image?: string; svg?: string }) {
    if (!gStickers.select(`g.sticker[data-slug="${slug}"]`).empty()) return;
    if (!visual.image && !visual.svg) return;
    const g = gStickers.append('g').attr('class', 'sticker').attr('data-slug', slug);
    const inner = g.append('g').attr('transform', `scale(0.3) rotate(${(slug.length % 3) * 6 - 6}) translate(-50,-50)`);
    if (visual.image) {
      inner.append('image').attr('href', visual.image).attr('width', 100).attr('height', 100).attr('preserveAspectRatio', 'xMidYMid meet');
    } else if (visual.svg) {
      // Copy the art's children (not the outer <svg>): a nested <svg> sizes itself unpredictably.
      const doc = new DOMParser().parseFromString(visual.svg, 'image/svg+xml');
      const target = inner.node()!;
      for (const child of Array.from(doc.documentElement.childNodes)) target.appendChild(document.importNode(child, true));
    }
    updateScreenSpace();
  }

  // ---- resize
  const ro = new ResizeObserver(() => {
    const w = Math.max(320, container.clientWidth);
    const h = Math.max(320, container.clientHeight);
    if (w === W && h === H) return;
    W = w; H = h;
    svg.attr('viewBox', `0 0 ${W} ${H}`);
    fitProjection();
    cacheAnchors();
    if (selected) selectPrefecture(selected, { animate: false });
    else reset(false);
  });

  svg.attr('viewBox', `0 0 ${W} ${H}`);
  fitProjection();
  cacheAnchors();
  reset(false);
  ro.observe(container);
  highlightRegion(highlightedRegion);

  return {
    container,
    selectPrefecture,
    focusRegion,
    highlightRegion,
    setLabelMode,
    zoomBy,
    reset,
    setInset,
    anchorScreen,
    addSticker,
    currentScale: () => transform.k,
    setLayer(id: LayerId, value: boolean) {
      layers.set(id, value);
      svg.classed('is-terrain', layers.isOn('mountains'));
      updateScreenSpace();
    },
    setActiveRange(no: number | null) {
      layers.setActiveRange(no);
      updateScreenSpace();
    },
    setHideRangeNames(hide: boolean) {
      layers.setHideRangeNames(hide);
      updateScreenSpace();
    },
    focusRange(no: number) {
      const b = layers.rangeBounds(no);
      if (!b) return;
      // phones have a short strip of map above the sheet: keep the margin in proportion to it
      const [[vx0, vy0], [vx1, vy1]] = visibleExtent();
      const pad = Math.max(16, Math.min(90, Math.round(Math.min(vx1 - vx0, vy1 - vy0) * 0.12)));
      applyTransform(transformFor(b, pad, 5), true);
    },
  };
}
