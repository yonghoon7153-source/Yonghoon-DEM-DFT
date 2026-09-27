// Loads the JSON database and builds the lookups the UI needs.
import prefecturesJson from '../data/prefectures.json';
import regionsJson from '../data/regions.json';
import mascotsJson from '../data/mascots.json';
import notesJson from '../data/notes.json';
import placesJson from '../data/places.json';
import mountainsJson from '../data/mountains.json';
import supplementJson from '../data/supplement.json';
import geoMeta from './generated/prefecture-geo.json';
import type { Mascot, MountainsDb, NoteExtra, NoteItem, NotesDb, PlacesDb, PrefGeoMeta, Prefecture, Region, SupplementDb } from './types';

export const prefectures = prefecturesJson.prefectures as Prefecture[];
export const regions = (regionsJson.regions as Region[]).slice().sort((a, b) => a.order - b.order);
export const mascots = mascotsJson.mascots as Mascot[];
export const notes = notesJson as unknown as NotesDb;
export const prefGeo = geoMeta as unknown as Record<string, PrefGeoMeta>;
export const places = placesJson as unknown as PlacesDb;
export const mountains = mountainsJson as unknown as MountainsDb;
export const supplement = supplementJson as unknown as SupplementDb;

export const prefById = new Map<number, Prefecture>(prefectures.map((p) => [p.id, p]));
export const prefBySlug = new Map<string, Prefecture>(prefectures.map((p) => [p.slug, p]));
export const regionById = new Map<string, Region>(regions.map((r) => [r.id, r]));
export const mascotById = new Map<string, Mascot>(mascots.map((m) => [m.id, m]));

export function regionOf(p: Prefecture): Region {
  const r = regionById.get(p.region);
  if (!r) throw new Error(`unknown region ${p.region}`);
  return r;
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
  return notes.extras.filter((e) => e.targets?.regions?.includes(regionId));
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
