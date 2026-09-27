// 💬 コメント — the one small server piece of にほんちず (ADR 0007): visitors leave 「뭐뭐 넣어줘!」 and everyone
// sees the list. A Cloudflare Pages Function at /api/comments, kept in D1 (binding `DB`); deleting needs the
// `ADMIN_KEY` secret. No login. The IP is never stored — only a salted hash, to slow down flooding.
//   GET    /api/comments[?before=<id>]   newest first, 30 at a time (+ `admin: true` when X-Admin-Key is right)
//   POST   /api/comments                 { name?, pref?, body, website? }   website = a trap field people never see
//   DELETE /api/comments?id=<id>         X-Admin-Key: <ADMIN_KEY>

// the part of the D1 API used here (no @cloudflare/workers-types needed)
interface D1Result<T = unknown> { results?: T[]; meta?: { last_row_id?: number } }
interface D1PreparedStatement {
  bind(...values: unknown[]): D1PreparedStatement;
  first<T = unknown>(): Promise<T | null>;
  all<T = unknown>(): Promise<D1Result<T>>;
  run(): Promise<D1Result>;
}
interface D1Database {
  prepare(sql: string): D1PreparedStatement;
  batch(statements: D1PreparedStatement[]): Promise<D1Result[]>;
}
export interface Env { DB?: D1Database; ADMIN_KEY?: string }
interface Ctx { request: Request; env: Env }
interface Row { id: number; created_at: number; name: string; pref: string; body: string }

const PAGE = 30;
const MAX_BODY = 400;
const MAX_NAME = 20;
const PER_PERSON_10_MIN = 5;
const PER_DAY = 300;

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });

// the table makes itself on first use, so the only setup is creating the database and binding it
let ready: Promise<unknown> | null = null;
function schema(db: D1Database): Promise<unknown> {
  ready ??= db
    .batch([
      db.prepare("CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at INTEGER NOT NULL, name TEXT NOT NULL DEFAULT '', pref TEXT NOT NULL DEFAULT '', body TEXT NOT NULL, ip_hash TEXT NOT NULL DEFAULT '')"),
      db.prepare('CREATE INDEX IF NOT EXISTS comments_by_person ON comments (ip_hash, created_at)'),
      db.prepare('CREATE INDEX IF NOT EXISTS comments_by_time ON comments (created_at)'),
    ])
    .catch((e: unknown) => {
      ready = null;
      throw e;
    });
  return ready;
}

// control characters, zero-width and direction marks never belong in a comment (they can disguise text)
const HIDDEN = /[\u0000-\u0008\u000B-\u001F\u007F-\u009F​-‏‪-‮⁠-⁤⁦-⁩﻿]/g;
/** The text as it will be stored, or null when it is too long. */
function clean(value: unknown, max: number, multiline: boolean): string | null {
  let t = typeof value === 'string' ? value : '';
  t = t.replace(/\r\n?/g, '\n').replace(/\t/g, ' ').replace(HIDDEN, '');
  t = multiline ? t.replace(/\n{3,}/g, '\n\n') : t.replace(/\n/g, ' ');
  t = t.trim();
  return [...t].length > max ? null : t;
}

async function personHash(request: Request, env: Env): Promise<string> {
  const ip = request.headers.get('cf-connecting-ip') ?? '';
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(`${ip}|${env.ADMIN_KEY ?? 'nihoncheese'}`));
  return [...new Uint8Array(digest).slice(0, 12)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function isAdmin(request: Request, env: Env): boolean {
  const want = env.ADMIN_KEY ?? '';
  const got = request.headers.get('x-admin-key') ?? '';
  if (!want || got.length !== want.length) return false;
  let diff = 0;
  for (let i = 0; i < want.length; i++) diff |= want.charCodeAt(i) ^ got.charCodeAt(i);
  return diff === 0;
}

const shape = (r: Row) => ({ id: r.id, at: r.created_at, name: r.name, pref: r.pref, body: r.body });

async function guarded(fn: () => Promise<Response>): Promise<Response> {
  try {
    return await fn();
  } catch (e) {
    console.error('comments:', e);
    return json({ error: 'server' }, 500);
  }
}

export const onRequestGet = ({ request, env }: Ctx) =>
  guarded(async () => {
    const db = env.DB;
    if (!db) return json({ error: 'not-configured' }, 503);
    await schema(db);
    const before = Number(new URL(request.url).searchParams.get('before'));
    const q = Number.isInteger(before) && before > 0
      ? db.prepare('SELECT id, created_at, name, pref, body FROM comments WHERE id < ? ORDER BY id DESC LIMIT ?').bind(before, PAGE + 1)
      : db.prepare('SELECT id, created_at, name, pref, body FROM comments ORDER BY id DESC LIMIT ?').bind(PAGE + 1);
    const rows = (await q.all<Row>()).results ?? [];
    return json({ comments: rows.slice(0, PAGE).map(shape), more: rows.length > PAGE, ...(isAdmin(request, env) ? { admin: true } : {}) });
  });

export const onRequestPost = ({ request, env }: Ctx) =>
  guarded(async () => {
    const db = env.DB;
    if (!db) return json({ error: 'not-configured' }, 503);
    if (Number(request.headers.get('content-length') ?? 0) > 8192) return json({ error: 'too-long' }, 413);
    let input: unknown;
    try {
      input = await request.json();
    } catch {
      return json({ error: 'bad-request' }, 400);
    }
    if (!input || typeof input !== 'object') return json({ error: 'bad-request' }, 400);
    const f = input as Record<string, unknown>;
    // people never see the trap field; a bot that fills it is told "thanks" and nothing is kept
    if (typeof f.website === 'string' && f.website.trim()) return json({ ok: true }, 201);
    const body = clean(f.body, MAX_BODY, true);
    const name = clean(f.name, MAX_NAME, false);
    const pref = typeof f.pref === 'string' && /^[a-z]{2,12}$/.test(f.pref) ? f.pref : '';
    if (body === null || name === null) return json({ error: 'too-long' }, 400);
    if (!body) return json({ error: 'empty' }, 400);
    await schema(db);
    const now = Date.now();
    const who = await personHash(request, env);
    const mine = await db.prepare('SELECT COUNT(*) AS n FROM comments WHERE ip_hash = ? AND created_at > ?').bind(who, now - 10 * 60_000).first<{ n: number }>();
    if ((mine?.n ?? 0) >= PER_PERSON_10_MIN) return json({ error: 'slow-down' }, 429);
    const today = await db.prepare('SELECT COUNT(*) AS n FROM comments WHERE created_at > ?').bind(now - 86_400_000).first<{ n: number }>();
    if ((today?.n ?? 0) >= PER_DAY) return json({ error: 'busy' }, 429);
    const r = await db.prepare('INSERT INTO comments (created_at, name, pref, body, ip_hash) VALUES (?, ?, ?, ?, ?)').bind(now, name, pref, body, who).run();
    return json({ comment: { id: Number(r.meta?.last_row_id ?? 0), at: now, name, pref, body } }, 201);
  });

export const onRequestDelete = ({ request, env }: Ctx) =>
  guarded(async () => {
    const db = env.DB;
    if (!db) return json({ error: 'not-configured' }, 503);
    if (!isAdmin(request, env)) return json({ error: 'forbidden' }, 403);
    const id = Number(new URL(request.url).searchParams.get('id'));
    if (!Number.isInteger(id) || id <= 0) return json({ error: 'bad-request' }, 400);
    await schema(db);
    await db.prepare('DELETE FROM comments WHERE id = ?').bind(id).run();
    return json({ ok: true });
  });
