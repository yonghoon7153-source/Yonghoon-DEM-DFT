// Shapes of the JSON database in /data (see data/schema/*.schema.json).

export type Lang = 'ja' | 'kana' | 'ko';

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
  children?: NoteItem[];
}

export interface NotesDb {
  meta: { source: string; canva?: string; updated: string; status: string; note?: string };
  regions: Record<string, { memo?: string; items?: NoteItem[] }>;
  prefectures: Record<string, { star?: boolean; items: NoteItem[] }>;
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
