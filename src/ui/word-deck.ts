export type StudyLanguage = 'ja' | 'en';
export interface WordCard {
  id: string;
  ja: string;
  reading: string;
  ko: string;
  en: string;
  jaExample: string;
  enExample: string;
  koExample: string;
  category: string;
  exampleOrigin?: string;
  notionUrl?: string;
}
export interface WordDeck {
  schemaVersion: 1;
  deckId: string;
  title: string;
  cards: WordCard[];
  today?: Record<StudyLanguage, Record<string, string[]>>;
}

function parseToday(value: unknown, cards: WordCard[]): NonNullable<WordDeck['today']> {
  const invalid = () => new Error('단어장의 날짜별 복습 목록을 확인해 주세요.');
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw invalid();
  const byId = new Map(cards.map((card) => [card.id, card]));
  const today: NonNullable<WordDeck['today']> = { ja: {}, en: {} };
  for (const language of ['ja', 'en'] as const) {
    const days = (value as Record<string, unknown>)[language];
    if (!days || typeof days !== 'object' || Array.isArray(days)) throw invalid();
    for (const [day, ids] of Object.entries(days)) {
      if (!/^(?:[1-9]|[12]\d|3[01])$/.test(day) || !Array.isArray(ids) || ids.length > cards.length) throw invalid();
      const members = new Set<string>();
      for (const id of ids) {
        if (typeof id !== 'string' || !byId.get(id)?.[language] || members.has(id)) throw invalid();
        members.add(id);
      }
      today[language][day] = [...members];
    }
  }
  return today;
}

/** Imported files are data. Render their strings with textContent, never HTML. */
export function parseDeck(value: unknown): WordDeck {
  if (!value || typeof value !== 'object') throw new Error('단어장 형식을 확인해 주세요.');
  const d = value as Record<string, unknown>;
  if (d.schemaVersion !== 1 || !Array.isArray(d.cards) || !d.cards.length || d.cards.length > 5000) {
    throw new Error('카드 1~5,000개가 들어 있는 단어장 파일을 선택해 주세요.');
  }
  function str(v: unknown, max = 8000): string {
    if (typeof v !== 'string' || v.length > max) throw new Error('단어장에 읽을 수 없는 항목이 있어요.');
    return v.trim();
  }
  const ids = new Set<string>();
  const cards = d.cards.map((row): WordCard => {
    if (!row || typeof row !== 'object') throw new Error('카드 내용을 확인해 주세요.');
    const c = row as Record<string, unknown>;
    const id = str(c.id, 160), ja = str(c.ja ?? ''), en = str(c.en ?? ''), ko = str(c.ko);
    if (!id || ids.has(id) || !ko || (!ja && !en)) throw new Error('카드 번호가 겹치거나 표현·뜻이 비어 있어요.');
    ids.add(id);
    let notionUrl: string | undefined;
    if (typeof c.notionUrl === 'string') {
      try {
        const u = new URL(c.notionUrl);
        if (u.protocol === 'https:' && ['app.notion.com', 'www.notion.so', 'notion.so'].includes(u.hostname)) notionUrl = u.href;
      } catch { /* An invalid source link does not prevent learning the expression. */ }
    }
    return { id, ja, en, ko, reading: str(c.reading ?? ''), jaExample: str(c.jaExample ?? ''),
      enExample: str(c.enExample ?? ''), koExample: str(c.koExample ?? ''),
      category: str(c.category || '생활 회화', 100), exampleOrigin: str(c.exampleOrigin ?? '', 100), notionUrl };
  });
  const deckId = str(d.deckId, 160), title = str(d.title, 160);
  if (!deckId || !title) throw new Error('단어장 이름을 확인해 주세요.');
  const deck: WordDeck = { schemaVersion: 1, deckId, title, cards };
  if (d.today !== undefined) deck.today = parseToday(d.today, cards);
  return deck;
}

const DAY_MS = 24 * 60 * 60 * 1000;
const KST_OFFSET_MS = 9 * 60 * 60 * 1000;

/** KST midnight occurs at 15:00 UTC, regardless of the browser's local time zone. */
export function seoulStudyDay(now = Date.now()) {
  const local = new Date(now + KST_OFFSET_MS);
  const ordinal = Math.floor(local.getTime() / DAY_MS);
  return {
    key: local.toISOString().slice(0, 10),
    dayOfMonth: local.getUTCDate(),
    ordinal,
    nextMidnight: (ordinal + 1) * DAY_MS - KST_OFFSET_MS,
  };
}

export function dailyCards(deck: WordDeck, language: StudyLanguage, day: ReturnType<typeof seoulStudyDay>, publicSample: boolean): WordCard[] {
  if (publicSample) {
    // Six of the eighteen paired examples per day. A stride of seven gives
    // consecutive days disjoint selections and visits every starting position.
    const count = deck.cards.length;
    const first = ((day.ordinal * 7) % count + count) % count;
    return Array.from({ length: Math.min(6, count) }, (_, i) => deck.cards[(first + i) % count]!)
      .filter((card) => card[language]);
  }
  const ids = deck.today?.[language][String(day.dayOfMonth)] ?? [];
  const byId = new Map(deck.cards.map((card) => [card.id, card]));
  return ids.map((id) => byId.get(id)!);
}

export function matchesCard(card: WordCard, query: string): boolean {
  const normalize = (s: string) => s.normalize('NFKC').toLocaleLowerCase();
  const haystack = normalize([card.ja, card.en, card.ko, card.reading, card.category].join(' '));
  return normalize(query).trim().split(/\s+/).every((word) => haystack.includes(word));
}

export function shuffled<T>(items: readonly T[]): T[] {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j]!, result[i]!];
  }
  return result;
}
