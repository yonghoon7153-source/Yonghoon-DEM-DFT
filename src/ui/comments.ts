// 💬 comment — visitors write 「뭐뭐 넣어줘!」 and everyone sees the list. The server side is one Cloudflare Pages
// Function (functions/api/comments.ts, ADR 0007). Everything is plain text (el/textContent), never HTML.
import { prefBySlug, prefectures } from '../data';
import type { Prefecture } from '../types';
import { el } from './dom';

interface Comment { id: number; at: number; name: string; pref: string; body: string }
interface Reply { comments?: Comment[]; comment?: Comment; more?: boolean; admin?: boolean; error?: string }

const API = `${import.meta.env.BASE_URL}api/comments`;
const MAX = 400;
// an unsent comment and the manager's password live only while the page is open — nothing is saved (9차 요청)
const draft = { name: '', pref: '', body: '' };
let adminKey = '';

const SAY: Record<string, string> = {
  'not-configured': '게시판을 여는 중이에요 — 조금만 기다려 주세요 ✿',
  'no-server': '게시판은 올린 사이트(nihoncheese.bmlwork.kr)에서 열려요',
  'slow-down': '조금만 천천히요 — 잠시 뒤에 다시 써 주세요',
  busy: '오늘은 글이 너무 많이 왔어요 — 내일 또 써 주세요',
  empty: '하고 싶은 말을 적어 주세요',
  'too-long': `${MAX}자까지 쓸 수 있어요`,
  forbidden: '비밀번호가 달라요',
  network: '연결이 안 돼요 — 잠시 뒤에 다시 해 보세요',
};
const say = (code?: string) => SAY[code ?? 'network'] ?? SAY.network!;

const prefLabel = (p: Prefecture) => `${p.short.ja} · ${p.name.ko}`;

function ago(t: number): string {
  const s = Math.max(0, (Date.now() - t) / 1000);
  if (s < 60) return '방금';
  if (s < 3600) return `${Math.floor(s / 60)}분 전`;
  if (s < 86400) return `${Math.floor(s / 3600)}시간 전`;
  if (s < 86400 * 7) return `${Math.floor(s / 86400)}일 전`;
  const d = new Date(t);
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`;
}

async function call(url: string, init: RequestInit = {}): Promise<{ ok: boolean; data: Reply }> {
  try {
    const r = await fetch(url, init);
    // no Pages Function behind the page (vite dev, GitHub Pages): the answer is not our JSON
    const data = (await r.json().catch(() => ({ error: 'no-server' }))) as Reply;
    return { ok: r.ok && !data.error, data: r.ok ? data : { error: data.error ?? 'network' } };
  } catch {
    return { ok: false, data: { error: 'network' } };
  }
}

/** The comment board; `current` (the open prefecture) is picked in the 県 box to begin with. */
export function renderComments(current?: string | null): HTMLElement {
  const wrap = el('div', { class: 'cmt' });
  wrap.append(
    el('h2', {}, el('span', { class: 'cmt__title' }, '💬 comment'), el('small', {}, '「뭐뭐 넣어줘!」 — 누구나 쓰고, 모두가 봐요')),
    el('p', { class: 'lead' }, '넣었으면 하는 県 · 명소 · 음식 · 단어, 틀린 곳도 좋아요. 로그인 없이, 이름은 안 써도 돼요.'),
  );

  // ---- writing
  const name = el('input', { type: 'text', class: 'cmt__field cmt__name', maxlength: '20', placeholder: '이름 (안 써도 돼요)', autocomplete: 'nickname', 'aria-label': '이름' });
  const pref = el('select', { class: 'cmt__field cmt__pref', 'aria-label': '어느 県 이야기인지' },
    el('option', { value: '' }, '県 (안 골라도 돼요)'),
    ...prefectures.map((p) => el('option', { value: p.slug }, prefLabel(p))));
  const body = el('textarea', { class: 'cmt__field cmt__body', maxlength: String(MAX), rows: '3', placeholder: '예) 교토에 말차 파르페도 넣어줘!', 'aria-label': '하고 싶은 말' });
  // people never see this field; a bot fills it and its comment is dropped (the server checks it)
  const trap = el('input', { type: 'text', class: 'cmt__trap', name: 'website', tabindex: '-1', autocomplete: 'off', 'aria-hidden': 'true' });
  const status = el('p', { class: 'cmt__status', role: 'status' });
  const count = el('span', { class: 'cmt__count' });
  const send = el('button', { type: 'submit', class: 'cmt__send' }, '보내기');
  const form = el('form', { class: 'cmt__form' }, el('div', { class: 'cmt__row' }, name, pref), body, trap, el('div', { class: 'cmt__foot' }, status, count, send));
  name.value = draft.name;
  pref.value = draft.pref || (current && prefBySlug.has(current) ? current : '');
  body.value = draft.body;
  const recount = () => {
    count.textContent = `${[...body.value].length}/${MAX}`;
  };
  recount();
  name.addEventListener('input', () => { draft.name = name.value; });
  pref.addEventListener('change', () => { draft.pref = pref.value; });
  body.addEventListener('input', () => { draft.body = body.value; recount(); });
  body.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); form.requestSubmit(); }
  });

  // ---- reading
  const list = el('ul', { class: 'cmt__list' });
  const note = el('p', { class: 'cmt__note' }, '불러오는 중…');
  const more = el('button', { type: 'button', class: 'cmt__more' }, '더 보기');
  more.hidden = true;
  let oldest = 0;
  let admin = false;

  function item(c: Comment): HTMLElement {
    const p = prefBySlug.get(c.pref);
    const meta = el('div', { class: 'cmt__meta' },
      el('b', {}, c.name || '익명'),
      p ? el('span', { class: 'cmt__tag' }, prefLabel(p)) : null,
      el('time', { datetime: new Date(c.at).toISOString(), title: new Date(c.at).toLocaleString('ko-KR') }, ago(c.at)));
    const li = el('li', { class: 'cmt__item' }, meta, el('p', { class: 'cmt__text' }, c.body));
    if (admin) {
      const del = el('button', { type: 'button', class: 'cmt__del', 'aria-label': '이 글 지우기', title: '지우기' }, '🗑');
      del.addEventListener('click', async () => {
        if (!window.confirm('이 글을 지울까요?')) return;
        const r = await call(`${API}?id=${c.id}`, { method: 'DELETE', headers: { 'x-admin-key': adminKey } });
        if (r.ok) li.remove();
        else window.alert(say(r.data.error));
        showEmpty();
      });
      meta.append(del);
    }
    return li;
  }
  function showEmpty() {
    if (!list.childElementCount && note.dataset.state !== 'closed') {
      note.textContent = '아직 글이 없어요 — 첫 번째 「뭐뭐 넣어줘!」 를 남겨 주세요 ✿';
      note.hidden = false;
    }
  }

  async function load(before = 0): Promise<boolean> {
    const r = await call(before ? `${API}?before=${before}` : API, adminKey ? { headers: { 'x-admin-key': adminKey } } : {});
    if (!r.ok || !Array.isArray(r.data.comments)) {
      note.textContent = say(r.data.error ?? 'no-server');
      note.dataset.state = 'closed';
      note.hidden = false;
      more.hidden = true;
      // nowhere to send to yet: keep what was typed, but don't pretend it can go
      if (r.data.error === 'not-configured' || r.data.error === 'no-server') send.disabled = true;
      return false;
    }
    admin = !!r.data.admin;
    note.hidden = true;
    delete note.dataset.state;
    for (const c of r.data.comments) list.append(item(c));
    oldest = r.data.comments.at(-1)?.id ?? oldest;
    more.hidden = !r.data.more;
    showEmpty();
    return true;
  }
  more.addEventListener('click', async () => {
    more.disabled = true;
    await load(oldest);
    more.disabled = false;
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!body.value.trim()) {
      status.textContent = say('empty');
      body.focus();
      return;
    }
    send.disabled = true;
    status.textContent = '보내는 중…';
    const r = await call(API, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ name: name.value, pref: pref.value, body: body.value, website: trap.value }),
    });
    send.disabled = false;
    if (!r.ok) {
      status.textContent = say(r.data.error);
      return;
    }
    if (r.data.comment) {
      list.prepend(item(r.data.comment));
      note.hidden = true;
    }
    body.value = draft.body = '';
    recount();
    status.textContent = '보냈어요! 고마워요 ✿';
  });

  // ---- the owner: the password (ADMIN_KEY in Cloudflare) shows 🗑 on every comment, until the page reloads
  const adminBtn = el('button', { type: 'button', class: 'cmt__admin' }, '관리');
  adminBtn.addEventListener('click', () => {
    const key = el('input', { type: 'password', class: 'cmt__field cmt__key', placeholder: '관리 비밀번호', autocomplete: 'current-password', 'aria-label': '관리 비밀번호' });
    const ok = el('button', { type: 'button', class: 'cmt__admin' }, '확인');
    const msg = el('span', { class: 'cmt__adminmsg', role: 'status' });
    const box = el('div', { class: 'cmt__adminbox' }, key, ok, msg);
    adminBtn.replaceWith(box);
    key.focus();
    const tryKey = async () => {
      adminKey = key.value;
      list.replaceChildren();
      await load();
      if (admin) box.replaceWith(el('p', { class: 'cmt__adminmsg' }, '관리 중 — 🗑 로 지워요 (새로고침하면 끝)'));
      else {
        adminKey = '';
        msg.textContent = say('forbidden');
      }
    };
    ok.addEventListener('click', tryKey);
    key.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); void tryKey(); }
    });
  });

  wrap.append(form, note, list, more, el('div', { class: 'cmt__end' }, adminBtn));
  void load();
  return wrap;
}
