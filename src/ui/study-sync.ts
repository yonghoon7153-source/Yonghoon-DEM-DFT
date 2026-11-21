import { parseDeck, type WordDeck } from './word-deck';

const FEED_URL = '/study-feed/my-deck.v1.enc.json';
const MAX_RESPONSE_BYTES = 16 * 1024 * 1024;
const CONNECTION_ERROR = '단어장 연결 파일을 확인해 주세요.';
const SYNC_ERROR = '단어장을 새로 가져오지 못했어요. 연결 파일과 인터넷 연결을 확인한 뒤 다시 시도해 주세요.';
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export interface StudyConnection {
  schemaVersion: 1;
  kind: 'nihonchizu-study-connection';
  feedId: string;
  deckId: string;
  url: typeof FEED_URL;
  /** Local decryption key. Never include it in a request, URL, or log. */
  key: string;
}

function object(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(CONNECTION_ERROR);
  return value as Record<string, unknown>;
}

function base64url(value: unknown, expectedBytes?: number): Uint8Array<ArrayBuffer> {
  if (typeof value !== 'string' || !value || value.length > MAX_RESPONSE_BYTES
    || !/^[A-Za-z0-9_-]+$/.test(value) || value.length % 4 === 1
    || (expectedBytes !== undefined && value.length !== Math.ceil(expectedBytes * 4 / 3))) {
    throw new Error(CONNECTION_ERROR);
  }
  const binary = atob(value.replace(/-/g, '+').replace(/_/g, '/'));
  if ((expectedBytes !== undefined && binary.length !== expectedBytes)
    || btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '') !== value) {
    throw new Error(CONNECTION_ERROR);
  }
  return Uint8Array.from(binary, (char) => char.charCodeAt(0));
}

export function parseConnection(value: unknown): StudyConnection {
  try {
    const data = object(value);
    if (data.schemaVersion !== 1 || data.kind !== 'nihonchizu-study-connection'
      || typeof data.feedId !== 'string' || !UUID.test(data.feedId)
      || typeof data.deckId !== 'string' || !data.deckId.trim() || data.deckId.length > 160
      || data.deckId !== data.deckId.trim() || /[\u0000-\u001f\u007f]/.test(data.deckId)
      || data.url !== FEED_URL || typeof data.key !== 'string') throw new Error(CONNECTION_ERROR);
    base64url(data.key, 32);
    return { schemaVersion: 1, kind: 'nihonchizu-study-connection', feedId: data.feedId,
      deckId: data.deckId, url: FEED_URL, key: data.key };
  } catch { throw new Error(CONNECTION_ERROR); }
}

function validTimestamp(value: unknown): value is string {
  if (typeof value !== 'string' || value.length > 40) return false;
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,9})?(?:Z|([+-])(\d{2}):(\d{2}))$/.exec(value);
  if (!match || !Number.isFinite(Date.parse(value))) return false;
  const year = Number(match[1]), month = Number(match[2]), day = Number(match[3]);
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  return month >= 1 && month <= 12 && day >= 1 && day <= days[month - 1]!
    && Number(match[4]) <= 23 && Number(match[5]) <= 59 && Number(match[6]) <= 59
    && (!match[7] || (Number(match[8]) <= 23 && Number(match[9]) <= 59));
}

function checkAbort(signal?: AbortSignal) {
  if (signal?.aborted) throw new DOMException('단어장 새로고침을 취소했어요.', 'AbortError');
}

async function readLimited(response: Response, signal?: AbortSignal): Promise<Uint8Array<ArrayBuffer>> {
  const length = response.headers.get('content-length');
  if (!response.ok || !response.body || response.redirected
    || (length !== null && /^\d+$/.test(length) && Number(length) > MAX_RESPONSE_BYTES)) {
    void response.body?.cancel().catch(() => undefined);
    throw new Error(SYNC_ERROR);
  }
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let size = 0, complete = false;
  try {
    while (true) {
      checkAbort(signal);
      const { done, value } = await reader.read();
      checkAbort(signal);
      if (done) { complete = true; break; }
      size += value.byteLength;
      if (size > MAX_RESPONSE_BYTES) throw new Error(SYNC_ERROR);
      chunks.push(value);
    }
    const result = new Uint8Array(size);
    let offset = 0;
    for (const chunk of chunks) { result.set(chunk, offset); offset += chunk.byteLength; }
    return result;
  } finally {
    if (!complete) void reader.cancel().catch(() => undefined);
    reader.releaseLock();
  }
}

/** Fetches only encrypted bytes. The key is used locally by Web Crypto. */
export async function fetchStudyDeck(connection: StudyConnection, signal?: AbortSignal): Promise<{
  deck: WordDeck;
  revision: string;
  /** Display metadata only: updatedAt is not part of the authenticated AAD. */
  updatedAt: string;
}> {
  try {
    const profile = parseConnection(connection);
    checkAbort(signal);
    if (!globalThis.crypto?.subtle) throw new Error(SYNC_ERROR);
    const response = await fetch(profile.url, {
      method: 'GET', mode: 'same-origin', credentials: 'omit', cache: 'no-store',
      redirect: 'error', referrerPolicy: 'no-referrer', signal,
    });
    const envelope = object(JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(await readLimited(response, signal))));
    if (envelope.schemaVersion !== 1 || envelope.kind !== 'nihonchizu-encrypted-deck'
      || envelope.feedId !== profile.feedId || typeof envelope.revision !== 'string'
      || !/^[0-9a-f]{64}$/.test(envelope.revision) || !validTimestamp(envelope.updatedAt)) throw new Error(SYNC_ERROR);
    const iv = base64url(envelope.iv, 12), ciphertext = base64url(envelope.ciphertext);
    if (ciphertext.byteLength < 16) throw new Error(SYNC_ERROR);
    const keyBytes = base64url(profile.key, 32);
    let key: CryptoKey;
    try { key = await crypto.subtle.importKey('raw', keyBytes, { name: 'AES-GCM' }, false, ['decrypt']); }
    finally { keyBytes.fill(0); }
    checkAbort(signal);
    const additionalData = new TextEncoder().encode(`nihonchizu-encrypted-deck:1:${profile.feedId}:${envelope.revision}`);
    const plaintext = await crypto.subtle.decrypt({ name: 'AES-GCM', iv, additionalData, tagLength: 128 }, key, ciphertext);
    checkAbort(signal);
    const hash = new Uint8Array(await crypto.subtle.digest('SHA-256', plaintext));
    const revision = Array.from(hash, (byte) => byte.toString(16).padStart(2, '0')).join('');
    if (revision !== envelope.revision) throw new Error(SYNC_ERROR);
    const deck = parseDeck(JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(plaintext)));
    if (deck.deckId !== profile.deckId) throw new Error(SYNC_ERROR);
    checkAbort(signal);
    return { deck, revision, updatedAt: envelope.updatedAt };
  } catch {
    checkAbort(signal);
    throw new Error(SYNC_ERROR);
  }
}
