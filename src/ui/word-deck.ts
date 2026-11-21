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
  return { schemaVersion: 1, deckId, title, cards };
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
