// Shapes of the JSON database in /data (see data/schema/*.schema.json).

export type Lang = 'ja' | 'kana' | 'ko';
/** Map label style: furi = 漢字 with small かな above (like the Canva map), otherwise one script. */
export type LabelMode = 'furi' | Lang;

export interface Names { ja: string; kana: string; romaji: string; ko: string; en: string }
export interface Term { ja: string; kana?: string; ko?: string }

export interface Prefecture {
  id: number;
  slug: string;
  region: string;
  name: Names;
  short: { ja: string; kana: string };
  capital: Term;
  meibutsu: Term[];
  spots: Term[];
  hitokoto: { ja: string; ko: string };
  mascot?: string;
}

export interface Region {
  id: string;
  order: number;
  /** The big region this one belongs to (中部 › 北陸) — only for the page titles and my 中部 memo. */
  group?: string;
  name: { ja: string; kana: string; ko: string; en: string };
  color: string;
  ink: string;
}
/** A big region that only groups others (中部): not drawn, not in the legend. */
export interface RegionGroup {
  id: string;
  name: { ja: string; kana: string; ko: string; en: string };
  color: string;
  ink: string;
}

export interface Mascot {
  id: string;
  prefecture: string;
  kind: 'official' | 'extra';
  name: { ja: string; kana: string; ko: string };
  org: string;
  about: { ja: string; ko: string };
  line: { ja: string; ko: string };
  /** What it says while being tapped — the hint before its hidden friend appears (みきゃん: 「날 너무 누르면 안돼!!」). */
  poke?: { ja: string; ko: string };
  /** likeness = our drawing · official = official art · standin = a picture the user chose instead (credit = its source) */
  art: 'likeness' | 'official' | 'standin';
  url?: string;
  credit?: string;
  /** Official image under public/ (e.g. "mascots/kumamon.png"). Replaces the drawn likeness when present. */
  image?: string;
  /** Hidden friend: appears when the mascot with this id is tapped three times (easter egg). */
  secret?: string;
}

/** One box of the mind map. Boxes joined by a line are children. */
export interface NoteItem {
  t: string;
  sub?: string;
  cap?: string;
  ko?: string;
  url?: string;
  star?: boolean;
  kind?: 'photo';
  /** The Canva box had a photo next to it — shown as 📷 that opens an image search (string = the search words). */
  photo?: boolean | string;
  /** Korean for a box I wrote only in Japanese — added by Claude, not my words (shown as a gray line). */
  gloss?: string;
  children?: NoteItem[];
}

export interface SupplementDb { prefectures: Record<string, { items: NoteItem[] }> }

export interface NotesDb {
  meta: { source: string; canva?: string; updated: string; status: string; note?: string };
  regions: Record<string, { memo?: string; items?: NoteItem[] }>;
  /** `root` — how I wrote the prefecture's own boxes, only where it differs from the standard name (니이가타, かがわ県). */
  prefectures: Record<string, { star?: boolean; root?: { ja?: string; ko?: string }; items: NoteItem[] }>;
  extras: NoteExtra[];
}

export interface NoteExtra {
  id: string;
  title: string;
  sub?: string;
  targets?: { regions?: string[]; prefectures?: string[] };
  items: NoteItem[];
}

export interface PrefGeoMeta {
  id: number;
  nameJa: string;
  anchor: [number, number];
  bbox: [number, number, number, number];
  coreBbox: [number, number, number, number];
  areaSr: number;
  polygons: number;
}

// ---- map layers (data/places.json, data/mountains.json) — coordinates are [longitude, latitude]
export type LonLat = [number, number];
/** `official` — the official spelling when I wrote the name differently on my map (津軽市 → つがる市). */
export interface PlaceName { ja: string; kana: string; ko: string; official?: string }
export interface City { id: string; pref: string; name: PlaceName; at: LonLat; capital: boolean; fromUser: boolean }
/** `note` — what I wrote next to the ward on my map (ranks); `mark` — I wrote its reading in red. */
export interface Ward { id: string; name: PlaceName; at: LonLat; note?: string; mark?: boolean }
/** `label` sits in the sea; a leader line runs from it to `at` on the island's coast. */
export interface Island { id: string; name: PlaceName; at: LonLat; label: LonLat }
/** `mark` — the part of `note` I wrote in red; `radiusKm` — I circled an area (根釧台地) rather than a point. */
export interface ExtraPlace { id: string; name: PlaceName; note?: string; mark?: string; pref?: string; at: LonLat; radiusKm?: number }
/** A few words written straight on the map (「山↑」 on the 中央高地). */
export interface MapNote { id: string; t: string; pref?: string; at: LonLat }
/** `kind` — tunnel (青函トンネル, drawn dashed) or plan (津軽海峡大橋: studied, never built — faint dotted); a bridge otherwise. */
export interface Bridge { id: string; kind?: 'tunnel' | 'plan'; name: PlaceName; route: { ja: string; kana: string }; line: LonLat[]; color: string; ko?: string }
export interface CompassWord { ja: string; kana: string; ko: string }
/** A direction word pinned to an edge of the map (north-up, so it never moves). */
export interface Compass { id: string; side: 'top' | 'right' | 'bottom' | 'left'; words: CompassWord[] }
/** A lake drawn on the map (its shape is objects.lakes of japan.topo.json); the name sits at `at`. */
export interface Lake { id: string; name: PlaceName; pref: string; at: LonLat; note?: string }
export interface PlacesDb { cities: City[]; wards: Ward[]; islands: Island[]; lakes?: Lake[]; extraPlaces: ExtraPlace[]; mapNotes: MapNote[]; compass: Compass[]; bridges: Bridge[] }
export interface MountainRange { no: number; id: string; kind: '山脈' | '山地' | '高地'; name: PlaceName; line: LonLat[]; ko?: string }
export interface MountainNote { id: string; t: string; sub?: string; ko?: string; at: LonLat; arrow?: LonLat[] }
export interface MountainsDb { ranges: MountainRange[]; notes: MountainNote[] }

/** 🚄 가는 법 layer (ADR 0009). `hub` — an international gateway, shown even on the whole-country view. */
export interface Airport { id: string; iata: string; name: PlaceName; pref: string; at: LonLat; hub?: boolean }
/** A station on a line; only a `major` one carries a name on the map (then kana, ko and pref are set). */
export interface Station { ja: string; kana?: string; ko?: string; pref?: string; at: LonLat; major?: boolean }
/** `kind` — mini (山形 · 秋田, conventional-gauge) or plan (under construction, dotted). The map joins stations with straight lines. */
export interface ShinkansenLine { id: string; kind?: 'mini' | 'plan'; name: PlaceName; color: string; stations: Station[] }
export interface TransitDb { airports: Airport[]; shinkansen: ShinkansenLine[] }

/** 🎆 축제 달력 entry. `box` — the note box that mentions it (default: ja); `approx` — the dates move a little every year. */
export interface Festival { id: string; kind?: 'season'; ja: string; kana: string; ko: string; pref: string; box?: string; fx: 'fireworks' | 'snow' | 'sakura' | 'momiji' | 'lanterns' | 'drums' | 'streamers'; start: string; end?: string; approx?: boolean; note?: string }
export interface FestivalsDb { festivals: Festival[] }

/** A place box of my mind map (or 보충) as a look-alike sticker on the map when zoomed in (ADR 0011). */
export interface Landmark { id: string; box: string; name: PlaceName; pref: string; ward?: string; at: LonLat; icon: string }
export interface LandmarksDb { landmarks: Landmark[] }
