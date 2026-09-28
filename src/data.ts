// Loads the JSON database and builds the lookups the UI needs.
import prefecturesJson from '../data/prefectures.json';
import regionsJson from '../data/regions.json';
import mascotsJson from '../data/mascots.json';
import notesJson from '../data/notes.json';
import placesJson from '../data/places.json';
import mountainsJson from '../data/mountains.json';
import supplementJson from '../data/supplement.json';
import transitJson from '../data/transit.json';
import festivalsJson from '../data/festivals.json';
import geoMeta from './generated/prefecture-geo.json';
import type { Airport, City, Festival, FestivalsDb, Mascot, MountainsDb, NoteExtra, NoteItem, NotesDb, PlacesDb, PrefGeoMeta, Prefecture, Region, RegionGroup, Station, SupplementDb, TransitDb } from './types';

export const prefectures = prefecturesJson.prefectures as Prefecture[];
export const regions = (regionsJson.regions as Region[]).slice().sort((a, b) => a.order - b.order);
/** Big regions that only group others (中部 › 北陸 · 甲信 · 東海) — ADR 0008. */
export const regionGroups = ((regionsJson as { groups?: RegionGroup[] }).groups ?? []) as RegionGroup[];
export const mascots = mascotsJson.mascots as Mascot[];
export const notes = notesJson as unknown as NotesDb;
export const prefGeo = geoMeta as unknown as Record<string, PrefGeoMeta>;
export const places = placesJson as unknown as PlacesDb;
export const mountains = mountainsJson as unknown as MountainsDb;
export const supplement = supplementJson as unknown as SupplementDb;
export const transit = transitJson as unknown as TransitDb;
export const festivals = (festivalsJson as unknown as FestivalsDb).festivals;

/** Where a festival is written: a box in my mind map, in Claude's 보충, or only in the calendar. */
export function festivalSource(f: Festival): 'notes' | 'supplement' | 'claude' {
  const p = prefBySlug.get(f.pref);
  if (!p) return 'claude';
  const name = f.box ?? f.ja;
  const named = (items: NoteItem[]): boolean => items.some((it) => it.t === name || named(it.children ?? []));
  if (named(notesFor(p).items)) return 'notes';
  if (named(supplementFor(p))) return 'supplement';
  return 'claude';
}

/** ✈ airports in a prefecture, hubs first. */
export function airportsOf(p: Prefecture): Airport[] {
  return transit.airports.filter((a) => a.pref === p.slug).sort((a, b) => Number(!!b.hub) - Number(!!a.hub));
}
/** 🚄 named shinkansen stations in a prefecture, with their lines (a station on two lines is listed once). */
export function stationsOf(p: Prefecture): { station: Station; lines: string[] }[] {
  const out = new Map<string, { station: Station; lines: string[] }>();
  for (const l of transit.shinkansen) {
    for (const s of l.stations) {
      if (!s.major || s.pref !== p.slug) continue;
      const e = out.get(s.ja) ?? { station: s, lines: [] };
      e.lines.push(l.name.ja);
      out.set(s.ja, e);
    }
  }
  return [...out.values()];
}

export const prefById = new Map<number, Prefecture>(prefectures.map((p) => [p.id, p]));
export const prefBySlug = new Map<string, Prefecture>(prefectures.map((p) => [p.slug, p]));
export const regionById = new Map<string, Region>(regions.map((r) => [r.id, r]));
export const regionGroupById = new Map<string, RegionGroup>(regionGroups.map((g) => [g.id, g]));
export const mascotById = new Map<string, Mascot>(mascots.map((m) => [m.id, m]));

export function regionOf(p: Prefecture): Region {
  const r = regionById.get(p.region);
  if (!r) throw new Error(`unknown region ${p.region}`);
  return r;
}

export function groupOf(r: Region): RegionGroup | undefined {
  return r.group ? regionGroupById.get(r.group) : undefined;
}

/** 「中部 › 北陸」 for a region inside a group, the plain name otherwise. */
export function regionTitle(r: Region, key: 'ja' | 'kana' | 'ko' = 'ja'): string {
  const g = groupOf(r);
  return g ? `${g.name[key]} › ${r.name[key]}` : r.name[key];
}

export function regionsInGroup(groupId: string): Region[] {
  return regions.filter((r) => r.group === groupId);
}

/** My memo pages for a region: its own, then the one I wrote for its big group (the 中部地方 box of my Canva). */
export function regionNotes(r: Region): { id: string; title: string; memo?: string; items: NoteItem[] }[] {
  const out: { id: string; title: string; memo?: string; items: NoteItem[] }[] = [];
  const own = notes.regions[r.id];
  if (own?.memo || own?.items?.length) out.push({ id: r.id, title: r.name.ja, memo: own.memo, items: own.items ?? [] });
  const g = groupOf(r);
  const gn = g && notes.regions[g.id];
  if (g && gn && (gn.memo || gn.items?.length)) out.push({ id: g.id, title: g.name.ja, memo: gn.memo, items: gn.items ?? [] });
  return out;
}

/** What the map knows about a city: the capital, a place with a box in my notes or 보충 (something to see), or a name only. */
export function cityTier(c: City): 'capital' | 'spot' | 'note' {
  if (c.capital) return 'capital';
  const p = prefBySlug.get(c.pref);
  if (!p) return 'note';
  const named = (items: NoteItem[]): boolean => items.some((it) => it.t === c.name.ja || named(it.children ?? []));
  return named(notesFor(p).items) || named(supplementFor(p)) ? 'spot' : 'note';
}

export function mascotsOf(p: Prefecture): Mascot[] {
  return mascots.filter((m) => m.prefecture === p.slug).sort((a, b) => (a.kind === b.kind ? 0 : a.kind === 'official' ? -1 : 1));
}

/** The hidden friend revealed by tapping this mascot three times, if any. */
export function secretFor(m: Mascot): Mascot | undefined {
  return mascots.find((x) => x.secret === m.id);
}

/** Google search for the character's official page, for mascots without a verified url. */
export function mascotSearchUrl(m: Mascot): string {
  return `https://www.google.com/search?q=${encodeURIComponent(`${m.name.ja} ${m.org} 公式`)}`;
}

export function prefecturesIn(regionId: string): Prefecture[] {
  return prefectures.filter((p) => p.region === regionId).sort((a, b) => a.id - b.id);
}

/** Boxes the user wrote for a prefecture (may be empty). */
/** Claude's supplementary boxes — only while I have written nothing for that prefecture. */
export function supplementFor(p: Prefecture): NoteItem[] {
  if (notes.prefectures[p.slug]?.items?.length) return [];
  return supplement.prefectures[p.slug]?.items ?? [];
}

export function notesFor(p: Prefecture): { star: boolean; items: NoteItem[] } {
  const n = notes.prefectures[p.slug];
  return { star: !!n?.star, items: n?.items ?? [] };
}

export function extrasFor(p: Prefecture): NoteExtra[] {
  return notes.extras.filter((e) => e.targets?.prefectures?.includes(p.slug));
}

export function extrasForRegion(regionId: string): NoteExtra[] {
  const group = regionById.get(regionId)?.group;
  return notes.extras.filter((e) => e.targets?.regions?.includes(regionId) || (!!group && e.targets?.regions?.includes(group)));
}

/** Extras that are not tied to any place (47都道府県, table manners, …) — what the map already draws is not repeated here. */
export function generalExtras(): NoteExtra[] {
  return notes.extras.filter((e) => !e.targets?.prefectures?.length && !e.targets?.regions?.length);
}

export function countBoxes(items: NoteItem[]): number {
  let n = 0;
  for (const it of items) n += 1 + countBoxes(it.children ?? []);
  return n;
}

// ---- search ---------------------------------------------------------------

const HIRA_TO_KATA = 0x60;
function normalize(s: string): string {
  return s
    .toLowerCase()
    .normalize('NFKC')
    .replace(/[ァ-ヶ]/g, (ch) => String.fromCharCode(ch.charCodeAt(0) - HIRA_TO_KATA)) // katakana -> hiragana
    .replace(/[\s\-ー・･。、,.()（）]/g, '')
    .replace(/[āáà]/g, 'a').replace(/[ōóò]/g, 'o').replace(/[ūúù]/g, 'u').replace(/[īíì]/g, 'i').replace(/[ēéè]/g, 'e');
}

interface SearchEntry { p: Prefecture; keys: string[] }
const searchIndex: SearchEntry[] = prefectures.map((p) => ({
  p,
  keys: [p.name.ja, p.short.ja, p.name.kana, p.short.kana, p.name.ko, p.name.ko.replace(/(현|도|부)$/, ''), p.name.en, p.name.romaji, p.slug, p.capital.ja, p.capital.kana ?? '', p.capital.ko ?? '']
    .filter(Boolean)
    .map(normalize),
}));

export function searchPrefectures(query: string, limit = 8): Prefecture[] {
  const q = normalize(query);
  if (!q) return [];
  const scored: { p: Prefecture; score: number }[] = [];
  for (const e of searchIndex) {
    let best = 0;
    for (const k of e.keys) {
      if (k === q) best = Math.max(best, 3);
      else if (k.startsWith(q)) best = Math.max(best, 2);
      else if (k.includes(q)) best = Math.max(best, 1);
    }
    if (best) scored.push({ p: e.p, score: best });
  }
  return scored.sort((a, b) => b.score - a.score || a.p.id - b.p.id).slice(0, limit).map((s) => s.p);
}
