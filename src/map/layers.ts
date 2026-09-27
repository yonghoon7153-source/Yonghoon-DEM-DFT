// Layers drawn over the prefectures, restoring the detail of the Canva map:
//   cities   — ◎ prefectural capitals and ● the cities I wrote on my map, Tokyo's 23 wards, the four main-island
//              names (in the sea, with a leader line, as on my map) and other places I noted (隠岐諸島)
//   bridges  — the three Honshu–Shikoku routes
//   mountains — the worksheet 「高い山脈・山地・高地」: green ridges with their numbers, plus my two notes
// Data lives in data/places.json and data/mountains.json. Lines are drawn in map space (they zoom with the land);
// dots, numbers and names are drawn in screen space and placed so they do not cover the prefecture names.
import { geoCircle, geoPath, type GeoProjection } from 'd3-geo';
import type { Selection } from 'd3-selection';
import type { ZoomTransform } from 'd3-zoom';
import { mountains, places } from '../data';
import type { LabelMode, LonLat, PlaceName } from '../types';

export type LayerId = 'cities' | 'bridges' | 'mountains';
export interface Rect { x: number; y: number; w: number; h: number }
type G = Selection<SVGGElement, unknown, null, undefined>;

export interface LayerContext {
  geo: G; // inside the zoomed viewport
  marks: G; // screen space, under the prefecture names
  text: G; // screen space, over the prefecture names
  projection: GeoProjection;
  okinawaShift: LonLat;
  onRange(no: number): void;
}

export interface LayerFrame {
  t: ZoomTransform;
  placed: Rect[]; // prefecture names already on screen — new labels must not cover them
  W: number;
  H: number;
  mode: LabelMode;
  selected: string | null;
  region: string | null;
}

/** Zoom levels at which names appear. */
const CITY_NAMES_AT = 2.1;
const WARDS_AT = 9;
const ISLANDS_UNTIL = 1.7;
const BRIDGE_NAMES_AT = 2.2;
const OKI_AT = 1.8;
/** 「山↑」-style notes belong to the whole-country / region view. */
const MAP_NOTES_UNTIL = 5;

function parts(n: PlaceName, mode: LabelMode): { main: string; furi: string } {
  if (mode === 'kana') return { main: n.kana, furi: '' };
  if (mode === 'ko') return { main: n.ko, furi: '' };
  return { main: n.ja, furi: mode === 'furi' ? n.kana : '' };
}

/** Rough text width: CJK / kana / hangul are square, the rest narrower. */
function textW(s: string, fs: number): number {
  let w = 0;
  for (const ch of s) w += /[　-鿿가-힯＀-￯]/.test(ch) ? fs : fs * 0.58;
  return w;
}

const hit = (a: Rect, list: Rect[]) => list.some((r) => r.x < a.x + a.w && r.x + r.w > a.x && r.y < a.y + a.h && r.y + r.h > a.y);

interface Pt { px: [number, number] }
interface LabelItem extends Pt { id: string; name: PlaceName; note?: string; mark?: string; red?: boolean; area?: boolean; cls: string; fs: number; prio: number; pref?: string }

/** Where the segment from the centre of `r` towards `p` leaves the rectangle (null when `p` is inside). */
function edgeToward(r: Rect, p: [number, number], gap: number): [number, number] | null {
  const cx = r.x + r.w / 2, cy = r.y + r.h / 2;
  const dx = p[0] - cx, dy = p[1] - cy;
  const s = Math.min(dx ? (r.w / 2 + gap) / Math.abs(dx) : Infinity, dy ? (r.h / 2 + gap) / Math.abs(dy) : Infinity);
  return s >= 1 ? null : [cx + dx * s, cy + dy * s];
}

export function createLayers(ctx: LayerContext) {
  const path = geoPath(ctx.projection);
  const on: Record<LayerId, boolean> = { cities: true, bridges: true, mountains: false };
  let hideRangeNames = false;
  let activeRange: number | null = null;

  const shift = (at: LonLat, pref?: string): LonLat => (pref === 'okinawa' ? [at[0] + ctx.okinawaShift[0], at[1] + ctx.okinawaShift[1]] : at);
  const project = (at: LonLat): [number, number] => {
    const p = ctx.projection(at);
    return p ? [p[0], p[1]] : [NaN, NaN];
  };

  // ---------------------------------------------------------------- data in screen-space order
  const cities: LabelItem[] = places.cities.map((c) => ({
    id: c.id, name: c.name, pref: c.pref, px: [0, 0], fs: c.capital ? 10.5 : 10,
    cls: `city${c.capital ? ' city--capital' : ''}${c.fromUser ? ' city--mine' : ''}`,
    prio: (c.fromUser ? 2 : 0) + (c.capital ? 1 : 0),
  }));
  const cityAt = new Map(places.cities.map((c) => [c.id, shift(c.at, c.pref)]));
  const wards: LabelItem[] = places.wards.map((w) => ({ id: w.id, name: w.name, note: w.note, red: w.mark, px: [0, 0], fs: 9, cls: 'ward', prio: 0 }));
  const wardAt = new Map(places.wards.map((w) => [w.id, w.at]));
  const islands: LabelItem[] = places.islands.map((i) => ({ id: i.id, name: i.name, px: [0, 0], fs: 15, cls: 'island', prio: 0 }));
  const islandLabelAt = new Map(places.islands.map((i) => [i.id, i.label]));
  const islandCoastAt = new Map(places.islands.map((i) => [i.id, i.at]));
  const islandCoast = new Map<string, [number, number]>();
  const extras: LabelItem[] = places.extraPlaces.map((e) => ({ id: e.id, name: e.name, note: e.note, mark: e.mark, area: !!e.radiusKm, pref: e.pref, px: [0, 0], fs: 10, cls: `extra-place${e.radiusKm ? ' extra-place--area' : ''}`, prio: 0 }));
  // a map note is just text: its "name" carries the same words in every label mode
  const mapNotes: LabelItem[] = (places.mapNotes ?? []).map((m) => ({ id: m.id, name: { ja: m.t, kana: m.t, ko: m.t }, pref: m.pref, px: [0, 0], fs: 12, cls: 'map-note', prio: 0 }));
  const mapNoteAt = new Map((places.mapNotes ?? []).map((m) => [m.id, shift(m.at, m.pref)]));
  /** A capital that is also one of the 23 wards (都庁 in 新宿区) leaves its name to the ward when wards show. */
  const wardNamesJa = new Set(places.wards.map((w) => w.name.ja));
  const extraAt = new Map(places.extraPlaces.map((e) => [e.id, shift(e.at, e.pref)]));

  // ---------------------------------------------------------------- map-space lines
  const gAreas = ctx.geo.append('g').attr('class', 'layer layer--areas');
  const areaSel = gAreas.selectAll<SVGPathElement, (typeof places.extraPlaces)[number]>('path.place-area')
    .data(places.extraPlaces.filter((e) => e.radiusKm), (d) => d.id)
    .join('path')
    .attr('class', 'place-area');
  const gBridges = ctx.geo.append('g').attr('class', 'layer layer--bridges');
  const bridgeSel = gBridges.selectAll<SVGGElement, (typeof places.bridges)[number]>('g.bridge')
    .data(places.bridges, (d) => d.id)
    .join((enter) => {
      const g = enter.append('g').attr('class', 'bridge').style('--bridge', (d) => d.color);
      g.append('path').attr('class', 'bridge__casing');
      g.append('path').attr('class', 'bridge__line');
      g.append('title').text((d) => `${d.name.ja} (${d.name.kana}) · ${d.route.ja}${d.ko ? ` — ${d.ko}` : ''}`);
      return g;
    });
  const bridgeMid = new Map<string, [number, number]>();

  const gRanges = ctx.geo.append('g').attr('class', 'layer layer--ranges');
  const rangeSel = gRanges.selectAll<SVGPathElement, (typeof mountains.ranges)[number]>('path.range')
    .data(mountains.ranges, (d) => d.id)
    .join('path')
    .attr('class', 'range');
  const rangeMid = new Map<number, [number, number]>();
  const rangeBox = new Map<number, [[number, number], [number, number]]>();

  const defs = ctx.geo.append('defs');
  defs.append('marker').attr('id', 'note-arrow').attr('viewBox', '0 0 10 10').attr('refX', 8).attr('refY', 5)
    .attr('markerWidth', 7).attr('markerHeight', 7).attr('orient', 'auto-start-reverse')
    .append('path').attr('d', 'M0,0 L10,5 L0,10 z').attr('class', 'note-arrow__head');
  const gArrows = ctx.geo.append('g').attr('class', 'layer layer--notes');
  const arrowSel = gArrows.selectAll<SVGPathElement, (typeof mountains.notes)[number]>('path.note-arrow')
    .data(mountains.notes.filter((n) => n.arrow && n.arrow.length >= 2), (d) => d.id)
    .join('path')
    .attr('class', 'note-arrow')
    .attr('marker-end', 'url(#note-arrow)');

  // ---------------------------------------------------------------- screen-space marks & names
  const gCityMarks = ctx.marks.append('g').attr('class', 'layer layer--cities');
  const leaderSel = gCityMarks.selectAll<SVGLineElement, LabelItem>('line.island-leader')
    .data(islands, (d) => d.id)
    .join('line')
    .attr('class', 'island-leader');
  const dot = (sel: G, data: LabelItem[], kind: string) =>
    sel.selectAll<SVGGElement, LabelItem>(`g.${kind}`)
      .data(data, (d) => d.id)
      .join((enter) => {
        const g = enter.append('g').attr('class', (d) => d.cls);
        const capital = (d: LabelItem) => d.cls.includes('city--capital');
        g.append('circle').attr('class', 'mark__ring').attr('r', (d) => (capital(d) ? 4.3 : kind === 'city' ? 3.2 : kind === 'ward' ? 2.2 : 3));
        g.append('circle').attr('class', 'mark__dot').attr('r', (d) => (capital(d) ? 1.7 : 0));
        g.append('title').text((d) => `${d.name.ja} (${d.name.kana}) ${d.name.ko}${d.name.official ? ` · 공식 표기 ${d.name.official}` : ''}${d.note ? ` — ${d.note}` : ''}`);
        return g;
      });
  const cityDots = dot(gCityMarks, cities, 'city');
  const wardDots = dot(gCityMarks, wards, 'ward');
  const extraDots = dot(gCityMarks, extras.filter((e) => !e.area), 'extra-place');

  const gRangeMarks = ctx.marks.append('g').attr('class', 'layer layer--ranges');
  const rangeNos = gRangeMarks.selectAll<SVGGElement, (typeof mountains.ranges)[number]>('g.range-no')
    .data(mountains.ranges, (d) => d.id)
    .join((enter) => {
      const g = enter.append('g').attr('class', 'range-no').attr('role', 'button').attr('tabindex', 0);
      g.append('circle').attr('r', 9);
      g.append('text').text((d) => String(d.no));
      g.on('click', (event: MouseEvent, d) => { event.stopPropagation(); ctx.onRange(d.no); });
      g.on('keydown', (event: KeyboardEvent, d) => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); ctx.onRange(d.no); }
      });
      return g;
    });

  const textOf = (sel: G, data: LabelItem[], cls: string) =>
    sel.selectAll<SVGTextElement, LabelItem>(`text.${cls}`)
      .data(data, (d) => d.id)
      .join((enter) => {
        const t = enter.append('text').attr('class', `label label--place ${cls}`).attr('lang', 'ja').style('font-size', (d) => `${d.fs}px`);
        t.append('tspan').attr('class', 'label__furi');
        t.append('tspan').attr('class', 'label__main');
        t.append('tspan').attr('class', 'label__note');
        return t;
      });
  const cityNames = textOf(ctx.text, cities, 'city-name');
  const wardNames = textOf(ctx.text, wards, 'ward-name');
  const islandNames = textOf(ctx.text, islands, 'island-name');
  const extraNames = textOf(ctx.text, extras, 'extra-name');
  const mapNoteNames = textOf(ctx.text, mapNotes, 'map-note');
  wardNames.classed('is-red', (d) => !!d.red);
  const bridgeItems: LabelItem[] = places.bridges.map((b) => ({ id: b.id, name: b.name, px: [0, 0], fs: 10.5, cls: 'bridge-name', prio: 0 }));
  const bridgeNames = textOf(ctx.text, bridgeItems, 'bridge-name');
  const rangeTag = ctx.text.append('text').attr('class', 'label label--place range-tag').attr('lang', 'ja');
  rangeTag.append('tspan').attr('class', 'label__furi');
  rangeTag.append('tspan').attr('class', 'label__main');
  const noteSel = ctx.text.selectAll<SVGGElement, (typeof mountains.notes)[number]>('g.range-note')
    .data(mountains.notes, (d) => d.id)
    .join((enter) => {
      const g = enter.append('g').attr('class', 'range-note');
      g.append('rect').attr('rx', 6);
      const t = g.append('text').attr('lang', 'ja');
      t.append('tspan').attr('class', 'range-note__t').text((d) => d.t);
      t.append('tspan').attr('class', 'range-note__sub').text((d) => (d.sub ? ` ${d.sub}` : ''));
      g.append('title').text((d) => d.ko ?? '');
      return g;
    });

  // ---------------------------------------------------------------- geometry (per projection fit)
  /** The point halfway along a projected polyline (where its number or name goes). */
  function midpoint(pts: [number, number][]): [number, number] {
    const segs: { a: [number, number]; b: [number, number]; len: number }[] = [];
    for (let i = 1; i < pts.length; i++) {
      const a = pts[i - 1]!, b = pts[i]!;
      segs.push({ a, b, len: Math.hypot(b[0] - a[0], b[1] - a[1]) });
    }
    let left = segs.reduce((s, g) => s + g.len, 0) / 2;
    for (const { a, b, len } of segs) {
      if (left <= len && len > 0) return [a[0] + (b[0] - a[0]) * (left / len), a[1] + (b[1] - a[1]) * (left / len)];
      left -= len;
    }
    return pts[0] ?? [0, 0];
  }

  function refit() {
    for (const c of cities) c.px = project(cityAt.get(c.id)!);
    for (const w of wards) w.px = project(wardAt.get(w.id)!);
    for (const i of islands) {
      i.px = project(islandLabelAt.get(i.id)!);
      islandCoast.set(i.id, project(islandCoastAt.get(i.id)!));
    }
    for (const e of extras) e.px = project(extraAt.get(e.id)!);
    for (const m of mapNotes) m.px = project(mapNoteAt.get(m.id)!);
    areaSel.attr('d', (d) => path(geoCircle().center(d.at).radius(d.radiusKm! / 111.2)()) ?? '');
    bridgeSel.selectAll<SVGPathElement, (typeof places.bridges)[number]>('path').attr('d', (d) => path({ type: 'LineString', coordinates: d.line }) ?? '');
    for (const b of places.bridges) bridgeMid.set(b.id, midpoint(b.line.map(project)));
    for (const b of bridgeItems) b.px = bridgeMid.get(b.id) ?? [0, 0];
    rangeSel.attr('d', (d) => path({ type: 'LineString', coordinates: d.line }) ?? '');
    for (const r of mountains.ranges) {
      const pts = r.line.map(project);
      rangeMid.set(r.no, midpoint(pts));
      const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
      rangeBox.set(r.no, [[Math.min(...xs), Math.min(...ys)], [Math.max(...xs), Math.max(...ys)]]);
    }
    arrowSel.attr('d', (d) => path({ type: 'LineString', coordinates: d.arrow! }) ?? '');
  }

  // ---------------------------------------------------------------- per frame
  /** Place a name next to its dot (right, left, above, below); returns its box, or null when every side collides. */
  function placeName(sel: Selection<SVGTextElement, LabelItem, SVGGElement, unknown>, d: LabelItem, x: number, y: number, f: LayerFrame, gap: number, sides: ('r' | 'l' | 'u' | 'd' | 'c')[]): Rect | null {
    const { main, furi } = parts(d.name, f.mode);
    const fs = d.fs;
    const note = d.note ?? '';
    const w = Math.max(textW(main, fs), furi ? textW(furi, fs * 0.68) : 0, note ? textW(note, fs * 0.82) : 0) + 4;
    const up = furi ? fs * 1.33 : fs / 2;
    const down = fs / 2 + (note ? fs * 1.05 : 0);
    const h = up + down + 4;
    for (const side of sides) {
      let ax = x, ay = y, anchor: 'start' | 'end' | 'middle' = 'middle';
      if (side === 'r') { ax = x + gap; anchor = 'start'; }
      else if (side === 'l') { ax = x - gap; anchor = 'end'; }
      else if (side === 'u') { ay = y - gap - down; }
      else if (side === 'd') { ay = y + gap + up; }
      const rx = anchor === 'start' ? ax : anchor === 'end' ? ax - w : ax - w / 2;
      const rect = { x: rx - 2, y: ay - up - 2, w, h };
      if (rect.x < 0 || rect.y < 0 || rect.x + rect.w > f.W || rect.y + rect.h > f.H) continue;
      if (hit(rect, f.placed)) continue;
      f.placed.push(rect);
      const t = sel.filter((q) => q === d);
      // inline style: the .label rule's text-anchor: middle would beat a presentation attribute
      t.attr('transform', `translate(${ax.toFixed(1)},${ay.toFixed(1)})`).style('text-anchor', anchor).classed('is-hidden', false);
      t.select('.label__main').attr('x', 0).attr('y', 0).text(main);
      t.select('.label__furi').attr('x', 0).attr('y', '-1.45em').text(furi);
      const noteT = t.select('.label__note').attr('x', 0).attr('y', '1.35em').text('');
      const at = d.mark ? note.indexOf(d.mark) : -1;
      if (at < 0) noteT.text(note);
      else {
        noteT.append('tspan').text(note.slice(0, at));
        noteT.append('tspan').attr('class', 'label__mark').text(d.mark!);
        noteT.append('tspan').text(note.slice(at + d.mark!.length));
      }
      return rect;
    }
    return null;
  }

  function update(f: LayerFrame) {
    const { t } = f;
    const k = t.k;
    const onScreen = (x: number, y: number, m = 20) => x > -m && x < f.W + m && y > -m && y < f.H + m;

    // bridges (lines always when on; names when zoomed in)
    gBridges.classed('is-off', !on.bridges);
    for (const b of bridgeItems) {
      const [x, y] = t.apply(b.px);
      const show = on.bridges && k >= BRIDGE_NAMES_AT && onScreen(x, y) && placeName(bridgeNames, b, x, y, f, 10, ['u', 'd', 'r', 'l']);
      if (!show) bridgeNames.filter((q) => q === b).classed('is-hidden', true);
    }

    // mountain mode
    gRanges.classed('is-off', !on.mountains);
    gArrows.classed('is-off', !on.mountains);
    gRangeMarks.classed('is-off', !on.mountains);
    rangeSel.classed('is-active', (d) => d.no === activeRange);
    rangeNos.classed('is-active', (d) => d.no === activeRange).attr('transform', (d) => {
      const [x, y] = t.apply(rangeMid.get(d.no) ?? [0, 0]);
      if (on.mountains) f.placed.push({ x: x - 10, y: y - 10, w: 20, h: 20 });
      return `translate(${x.toFixed(1)},${y.toFixed(1)})`;
    });
    const active = mountains.ranges.find((r) => r.no === activeRange);
    if (on.mountains && active && !hideRangeNames) {
      const [x, y] = t.apply(rangeMid.get(active.no) ?? [0, 0]);
      const { main, furi } = parts(active.name, f.mode);
      rangeTag.classed('is-hidden', false).attr('transform', `translate(${(x + 13).toFixed(1)},${y.toFixed(1)})`).style('text-anchor', 'start');
      rangeTag.select('.label__main').attr('x', 0).attr('y', 0).text(main);
      rangeTag.select('.label__furi').attr('x', 0).attr('y', '-1.45em').text(furi);
    } else rangeTag.classed('is-hidden', true);
    noteSel.classed('is-hidden', !on.mountains).attr('transform', (d) => {
      const [x, y] = t.apply(project(d.at));
      return `translate(${x.toFixed(1)},${y.toFixed(1)})`;
    });
    noteSel.each(function () {
      const g = this as SVGGElement;
      const txt = g.querySelector('text')!;
      const bb = txt.getBBox();
      const r = g.querySelector('rect')!;
      r.setAttribute('x', String(bb.x - 6)); r.setAttribute('y', String(bb.y - 3));
      r.setAttribute('width', String(bb.width + 12)); r.setAttribute('height', String(bb.height + 6));
    });

    // cities, wards, islands, other places
    gCityMarks.classed('is-off', !on.cities);
    const wardsOn = on.cities && k >= WARDS_AT;
    const order = [...cities].sort((a, b) => (b.pref === f.selected ? 10 : 0) + b.prio - ((a.pref === f.selected ? 10 : 0) + a.prio));
    const shownDot = new Set<string>();
    for (const c of order) {
      const [x, y] = t.apply(c.px);
      const vis = on.cities && onScreen(x, y);
      if (vis) shownDot.add(c.id);
      const leaveToWard = wardsOn && c.pref === 'tokyo' && wardNamesJa.has(c.name.ja);
      const named = vis && !leaveToWard && (k >= CITY_NAMES_AT || c.pref === f.selected) && placeName(cityNames, c, x, y, f, 7, ['r', 'l', 'u', 'd']);
      if (!named) cityNames.filter((q) => q === c).classed('is-hidden', true);
    }
    cityDots.classed('is-hidden', (d) => !shownDot.has(d.id)).attr('transform', (d) => {
      const [x, y] = t.apply(d.px);
      return `translate(${x.toFixed(1)},${y.toFixed(1)})`;
    });

    const shownWard = new Set<string>();
    for (const w of wards) {
      const [x, y] = t.apply(w.px);
      const vis = wardsOn && onScreen(x, y);
      if (vis) shownWard.add(w.id);
      const named = vis && placeName(wardNames, w, x, y, f, 5, ['r', 'l', 'u', 'd']);
      if (!named) wardNames.filter((q) => q === w).classed('is-hidden', true);
    }
    wardDots.classed('is-hidden', (d) => !shownWard.has(d.id)).attr('transform', (d) => {
      const [x, y] = t.apply(d.px);
      return `translate(${x.toFixed(1)},${y.toFixed(1)})`;
    });

    const islandsOn = on.cities && k <= ISLANDS_UNTIL && !f.selected && !f.region;
    const leaders = new Map<string, [number, number, number, number]>();
    for (const i of islands) {
      const [x, y] = t.apply(i.px);
      const box = islandsOn && onScreen(x, y) ? placeName(islandNames, i, x, y, f, 0, ['c']) : null;
      if (!box) { islandNames.filter((q) => q === i).classed('is-hidden', true); continue; }
      const coast = t.apply(islandCoast.get(i.id) ?? i.px);
      const from = edgeToward(box, coast, 2);
      if (from) leaders.set(i.id, [from[0], from[1], coast[0], coast[1]]);
    }
    leaderSel.classed('is-hidden', (d) => !leaders.has(d.id)).each(function (d) {
      const l = leaders.get(d.id);
      if (!l) return;
      this.setAttribute('x1', l[0].toFixed(1)); this.setAttribute('y1', l[1].toFixed(1));
      this.setAttribute('x2', l[2].toFixed(1)); this.setAttribute('y2', l[3].toFixed(1));
    });

    gAreas.classed('is-off', !on.cities);
    const shownExtra = new Set<string>();
    for (const e of extras) {
      const [x, y] = t.apply(e.px);
      const vis = on.cities && k >= OKI_AT && onScreen(x, y);
      if (vis) shownExtra.add(e.id);
      // an area (根釧台地) carries its name inside the circle, a point (隠岐) beside its dot
      const named = vis && placeName(extraNames, e, x, y, f, e.area ? 0 : 7, e.area ? ['c', 'd'] : ['l', 'r', 'u', 'd']);
      if (!named) extraNames.filter((q) => q === e).classed('is-hidden', true);
    }
    for (const m of mapNotes) {
      const [x, y] = t.apply(m.px);
      const named = on.cities && k < MAP_NOTES_UNTIL && onScreen(x, y) && placeName(mapNoteNames, m, x, y, f, 6, ['c', 'u', 'd', 'r', 'l']);
      if (!named) mapNoteNames.filter((q) => q === m).classed('is-hidden', true);
    }
    extraDots.classed('is-hidden', (d) => !shownExtra.has(d.id)).attr('transform', (d) => {
      const [x, y] = t.apply(d.px);
      return `translate(${x.toFixed(1)},${y.toFixed(1)})`;
    });
  }

  return {
    refit,
    update,
    set(id: LayerId, value: boolean) { on[id] = value; },
    isOn: (id: LayerId) => on[id],
    setActiveRange(no: number | null) { activeRange = no; },
    setHideRangeNames(v: boolean) { hideRangeNames = v; },
    rangeBounds: (no: number) => rangeBox.get(no) ?? null,
  };
}

export type Layers = ReturnType<typeof createLayers>;
