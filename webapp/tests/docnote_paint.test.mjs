/* 형광펜이 **실제 브라우저에서 칠해지는가** — 진짜 DOM 이 아니면 검증이 안 되는 것들.
 *
 * 왜 있나 (2026-08-27): 첫 판은 `wrapFirst`(한 텍스트 노드 안에 통째로 있을 때만
 * `surroundContents`)로 칠했다. digest 본문은 <b>·<sub>·<em> 이 촘촘해서 사람이 문장을
 * 드래그하면 거의 항상 노드를 가로지른다 — **저장은 되는데 안 칠해졌다.** 파이썬 테스트는
 * 서버만 보고 있어서 이걸 못 잡았고, 1저자가 화면을 보고 신고했다.
 *
 * 이 파일이 못 하는 것: 마우스 드래그(Selection)로 칠하는 경로는 안 본다 —
 * 여기서 보는 것은 **저장된 형광펜이 본문에 다시 붙는가** 하나다.
 *
 * 실행:  node webapp/tests/docnote_paint.test.mjs
 *        (playwright-core 와 /opt/pw-browsers 가 있어야 한다. 없으면 SKIP 으로 끝낸다.)
 */
import { readFileSync, existsSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";

const ROOT = path.resolve(new URL(".", import.meta.url).pathname, "../..");
const JS = path.join(ROOT, "webapp/static/js/docnote.js");
// ⛔ 2026-08-28 — docnote.js 는 이제 서식 함수(inline/autosize/wrapSel)를 **자기 사본으로
//   두지 않고** comments.js 의 window.noteFmt 를 부른다. base.html 이 모든 페이지에
//   comments.js 를 싣기 때문인데, 이 테스트는 docnote.js 만 싣고 있어서 메모 카드가
//   아예 안 그려졌다 (NF() 가 던진다 — 의도한 fail-closed 다).
//   ⇒ **실제 페이지와 같은 조합**으로 싣는다. 하나만 싣는 테스트는 실제를 안 시험한다.
const CJS = path.join(ROOT, "webapp/static/js/comments.js");
// ⚠ CSS 도 같이 물린다. 안 물리면 `.dn-card` 가 static 으로 놓여서 **자리·크기 검사가
//   아무것도 재지 않는다** — 통과해도 보증이 없다 (2026-08-27 자체 발견).
const CSS = path.join(ROOT, "webapp/static/css/style.css");

let chromium;
try {
  const req = createRequire(process.env.PW_CORE_FROM || `${ROOT}/package.json`);
  ({ chromium } = req("playwright-core"));
} catch {
  console.log("SKIP — playwright-core 가 없다 (npm i playwright-core)");
  process.exit(0);
}
const EXE = ["/opt/pw-browsers/chromium/chrome-linux/chrome",
             "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"].find(existsSync);
if (!EXE) { console.log("SKIP — chromium 실행파일을 못 찾았다"); process.exit(0); }

const HL = [
  // ① 한 텍스트 노드 안 (옛 판도 되던 경우)
  { id: "h1", text: "한 노드 안에 통째로", color: "yellow", at: "2026-08-27" },
  // ② <b> 경계를 가로지른다 ← 실제 신고 사례
  { id: "h2", text: "굵은 글자를 지나 이어지는 문장", color: "green", at: "2026-08-27" },
  // ③ 인라인 태그 여러 개 + 아래첨자
  { id: "h3", text: "Li6PS5Cl 과 LGPS 에 치환/도핑만 해 왔다", color: "pink", at: "2026-08-27" },
  // ④ 본문에 없는 글 → 자리를 못 찾아야 한다 (음성)
  { id: "h4", text: "본문에 없는 문장이다", color: "blue", at: "2026-08-27" },
  // ⑤ 문단을 가로지른다 → 못 찾아야 한다 (음성, 알려진 한계)
  { id: "h5", text: "첫 문단 끝 두 번째 문단 시작", color: "yellow", at: "2026-08-27" },
];

// 실제 모달과 같은 격자(본문 | 288px 여백칸)를 흉내 낸다 — 그래야 '왼쪽으로 넓어진다' 가
// 뜻을 갖는다. 클래스 이름은 style.css 의 것을 그대로 쓴다.
const PAGE = `
<div id="pmbox" class="dnote-on" style="max-width:1180px;margin:0 auto">
<div class="modal-head"></div>
<div id="host"><div id="body" class="doc">
  <p>여기 <em>기울임</em> 이 있고 <span>한 노드 안에 통째로</span> 들어 있는 문단이다. 첫 문단 끝</p>
  <p>두 번째 문단 시작 — <b>굵은 글자</b>를 지나 이어지는 문장 이 있다.</p>
  <ul><li>지금까지는 Li<sub>6</sub>PS<sub>5</sub>Cl 과 <b>LGPS</b> 에 <em>치환/도핑</em>만 해 왔다 → 끝</li></ul>
</div></div></div>`;

const b = await chromium.launch({ executablePath: EXE });
const pg = await b.newPage();
await pg.setContent(`<!doctype html><meta charset="utf-8">${PAGE}`);
const NOTE = {
  id: "n1", at: "2026-08-27 23:06", anchor: "한 노드 안에 통째로",
  /* ⚠ **줄바꿈 없는 긴 문단**이어야 한다 (2026-08-28). 첫 fixture 는 \n 이 박혀 있어서
   *   카드를 넓혀도 줄 수가 거의 안 줄었고, 그래서 "빈 여백" 시험이 **고치기 전에도
   *   통과했다** — 판별력이 0 이었다. 실제 메모는 이렇게 이어지는 문단이라 좁을 때
   *   10줄이던 게 넓히면 3줄로 접힌다. 거기서만 그 버그가 보인다. */
  text: "First, its symmetric molecular structure and **highly electron-deficient center** "
      + "allow it to readily undergo ring-opening polymerization initiated by nucleophilic "
      + "attack from S2- anions. Secondly, the resulting PS has strong antioxidant capacity, "
      + "and, as a surface modification layer, can effectively enhance the oxidation "
      + "stability of LPSC, which is exactly the point this fixture needs to reflow across "
      + "several lines when the card is narrow and far fewer when it widens.",
};
await pg.evaluate(({ hl, note }) => {
  window.__calls = [];
  window.fetch = function (url, opt) {
    window.__calls.push([url, opt && opt.method]);
    const hi = String(url).includes("/api/highlights/");
    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve({ items: hi ? hl : [note] }),
    });
  };
}, { hl: HL, note: NOTE });
await pg.addStyleTag({ path: CSS });
await pg.addScriptTag({ path: CJS });   // 서식의 집 — docnote.js 보다 **먼저**
await pg.addScriptTag({ path: JS });
await pg.evaluate(() =>
  window.mountDocNotes(document.getElementById("body"), "kb/x.md",
                       document.getElementById("pmbox")));
await pg.waitForFunction(() => document.querySelectorAll("mark.dn-pen").length > 0,
                         null, { timeout: 5000 }).catch(() => {});

const got = await pg.evaluate(() => {
  const by = {};
  document.querySelectorAll("mark.dn-pen").forEach((m) => {
    const k = m.dataset.hid || "?";
    (by[k] = by[k] || { text: "", cls: m.className, n: 0 });
    by[k].text += m.textContent;
    by[k].n += 1;
  });
  return by;
});

let ok = true;
const chk = (c, m) => { ok = ok && !!c; console.log(`  ${c ? "✓" : "✗"} ${m}`); };
const norm = (s) => String(s || "").replace(/\s+/g, " ").trim();

chk(got.h1 && norm(got.h1.text) === HL[0].text,
    `[형광·양성] 한 노드 안 (조각 ${got.h1 ? got.h1.n : 0}개)`);
chk(got.h2 && norm(got.h2.text) === HL[1].text,
    `[형광·양성·실측회귀] <b> 경계를 가로질러도 칠한다 (조각 ${got.h2 ? got.h2.n : 0}개) `
    + `— 옛 판이 여기서 조용히 실패했다`);
chk(got.h3 && norm(got.h3.text) === HL[2].text,
    `[형광·양성] 인라인 태그 여럿 + <sub> 를 가로질러도 (조각 ${got.h3 ? got.h3.n : 0}개)`);
chk(got.h2 && got.h2.n >= 2, "[형광] 노드를 가로지르면 조각이 2개 이상 생긴다");
chk(got.h2 && /dn-pen-green/.test(got.h2.cls), "[형광] 색 클래스가 붙는다");
chk(!got.h4, "[형광·음성] 본문에 없는 글은 안 칠한다");
chk(!got.h5, "[형광·음성] 문단을 가로지른 선택은 안 칠한다 (알려진 한계)");

const btn = await pg.evaluate(() => {
  const el = document.createElement("button");
  el.id = "docpen"; document.body.appendChild(el);
  window.docnotePenToggle(); window.docnotePenToggle();   // paintPenBtn 을 태운다
  return { text: el.textContent, title: el.title };
});
chk(/⚠2/.test(btn.text), `[형광] 자리를 못 찾은 2개를 버튼에 알린다 ("${btn.text}")`);
chk(/자리를 못 찾았어요/.test(btn.title), "[형광] 왜 그런지 title 로 설명한다");

const dbl = await pg.evaluate(() => {
  window.__dnRerender = true;
  document.querySelectorAll("mark.dn-pen").forEach(() => {});
  return document.querySelectorAll("mark.dn-pen mark.dn-pen").length;
});
chk(dbl === 0, "[형광] 형광펜 안에 형광펜이 겹쳐 들어가지 않는다");

// ── 고치기 상자가 내용에 맞춰 커지는가 (1저자 2026-08-27 "수정할 때 창이 작아져서 불편해")
await pg.setViewportSize({ width: 1400, height: 900 });
const box = await pg.evaluate(() => {
  const card = document.querySelector(".dn-card");
  if (!card) return { err: "메모 카드가 없다" };
  const shown = card.querySelector(".dn-text").getBoundingClientRect().height;
  card.querySelector(".dn-edit").click();
  const ta = card.querySelector(".dn-in");
  if (!ta) return { err: "입력창이 안 열렸다" };
  const r = ta.getBoundingClientRect();
  const before = { h: r.height, w: r.width, scroll: ta.scrollHeight,
                   cardLeft: card.getBoundingClientRect().left, shown: shown };
  ta.value += "\n덧붙이는 줄 1\n덧붙이는 줄 2\n덧붙이는 줄 3";
  ta.dispatchEvent(new Event("input", { bubbles: true }));
  return Object.assign(before, { after: ta.getBoundingClientRect().height });
});
chk(!box.err, `[고치기] 입력창이 열린다 ${box.err || ""}`);
if (!box.err) {
  chk(box.h + 2 >= box.scroll,
      `[고치기·실측회귀] 상자가 **내용을 다 담는다** (높이 ${Math.round(box.h)} ≥ 내용 ${box.scroll})`);
  /* ⛔ 반대 방향도 본다 (1저자 2026-08-28: "저 흰색 여백을 안보게").
   *   전에는 **좁은 카드에서 높이를 재고** 그 뒤에 카드가 왼쪽으로 넓어져서,
   *   글은 3줄로 접혔는데 상자는 좁을 때 줄 수로 남아 아래가 통째로 비었다.
   *   "다 담는가" 만 보면 그 상태도 통과한다 — 한 방향만 보는 시험은 절반이다. */
  chk(box.h <= box.scroll + 10,
      `[고치기·실측회귀] 상자에 **빈 여백이 남지 않는다** (높이 ${Math.round(box.h)} ≈ 내용 ${box.scroll})`);
  chk(box.h > 60, `[고치기] rows=3 (약 46px) 보다 크다 (${Math.round(box.h)}px)`);
  chk(box.after > box.h + 20,
      `[고치기] 줄을 더 치면 더 커진다 (${Math.round(box.h)} → ${Math.round(box.after)}px)`);
  // 여백칸은 288px 이고 카드는 좌우 10px 안쪽이라 평소 입력창은 ~250px 다.
  //   고칠 때는 본문 위로 왼쪽으로 넓어져야 한다.
  chk(box.w > 400,
      `[고치기] 고칠 때 입력창이 여백칸(≈250px)보다 넓어진다 (${Math.round(box.w)}px, `
      + `카드 left ${Math.round(box.cardLeft)}px)`);
}

/* ── 2열 배치 (1저자 2026-08-28: "중복된 층에서는 1열, 2열 느낌으로 나눠서") ──
 * 예전에는 자리가 겹치면 **무조건 아래로 밀었다** — 본문 그 줄과 나란히 있어야 할
 * 카드가 한참 내려가 어느 줄 메모인지 알 수 없었다. 이제 옆 열로 간다.
 * 그리고 폭은 **겹칠 때만** 반이다 — 혼자 있는 메모는 통폭을 다 쓴다. */
/* ⚠ 위 시험들은 메모 **하나**로 돌았다. 겹침 배치는 그걸로 못 본다 —
 *   서로 가까운 자리에 붙은 메모 셋으로 다시 올린다. */
await pg.evaluate(() => {
  const mk = (id, anchor, text) => ({ id, at: "2026-08-28 13:17", anchor, text });
  const many = [
    mk("m1", "한 노드 안에 통째로", "첫 메모. 여기에 **굵게** 와 여러 줄이 들어간다.\n둘째 줄\n셋째 줄"),
    mk("m2", "굵은 글자", "둘째 메모 — 바로 아래 문단이라 첫 메모와 자리가 겹친다."),
    mk("m3", "치환/도핑", "셋째 메모. 목록 항목에 붙는다."),
  ];
  window.fetch = function (url) {
    const hi = String(url).includes("/api/highlights/");
    return Promise.resolve({ ok: true, json: () => Promise.resolve({ items: hi ? [] : many }) });
  };
  window.unmountDocNotes();
  window.mountDocNotes(document.getElementById("body"), "kb/x.md",
                       document.getElementById("pmbox"));
});
await pg.waitForFunction(() => document.querySelectorAll(".dn-card").length >= 3,
                         null, { timeout: 5000 }).catch(() => {});

const cols = await pg.evaluate(() => {
  const g = document.querySelector(".dnote-gut");
  if (!g) return { err: "여백칸이 없다" };
  const cards = [...g.querySelectorAll(".dn-card")];
  if (cards.length < 2) return { err: `카드가 ${cards.length}개뿐이다` };
  const gr = g.getBoundingClientRect();
  const r = cards.map((c) => {
    const b = c.getBoundingClientRect();
    return { left: Math.round(b.left - gr.left), w: Math.round(b.width),
             top: Math.round(b.top - gr.top), h: Math.round(b.height),
             half: c.classList.contains("dn-half") };
  });
  return { gutW: Math.round(gr.width), cards: r };
});
chk(!cols.err, `[배치] 카드가 여럿 있다 ${cols.err || ""}`);
if (!cols.err) {
  chk(cols.gutW >= 380,
      `[배치·실측] 여백칸이 넓어졌다 (${cols.gutW}px, 예전 288px)`);
  // 겹치는 카드는 서로 다른 left 를 갖는다 = 2열로 갈렸다
  const halves = cols.cards.filter((c) => c.half);
  const lefts = new Set(cols.cards.map((c) => c.left));
  chk(lefts.size >= (halves.length ? 2 : 1),
      `[배치] 겹친 카드는 **다른 열**에 놓인다 (열 시작점 ${[...lefts].join("/")}px, `
      + `반폭 ${halves.length}장)`);
  // ⛔ 음성: 어느 카드도 여백칸 밖으로 삐져나가지 않는다 (고치는 중인 카드는 제외)
  const over = cols.cards.filter((c) => c.left < -1 || c.left + c.w > cols.gutW + 1);
  chk(over.length === 0,
      `[배치·음성] 카드가 여백칸을 벗어나지 않는다 (${over.length}장 벗어남)`);
  // ⛔ 음성: 같은 열에서 세로로 겹치지 않는다 — 겹치면 글이 가려진다
  const bad = [];
  for (let i = 0; i < cols.cards.length; i++) {
    for (let j = i + 1; j < cols.cards.length; j++) {
      const a = cols.cards[i], c = cols.cards[j];
      const xo = a.left < c.left + c.w && c.left < a.left + a.w;
      const yo = a.top < c.top + c.h && c.top < a.top + a.h;
      if (xo && yo) bad.push([i, j]);
    }
  }
  chk(bad.length === 0, `[배치·음성] 카드끼리 겹치지 않는다 (${bad.length}쌍 겹침)`);
}

/* ── 고칠 때 **왼쪽으로** 넓어진다 (1저자 2026-08-28: "이쪽 말고 왼쪽으로 확장되게") ──
 * ⛔ 실측 회귀: 고치면 카드가 길어져 옆 카드와 겹치고, 그러면 배치가 half=true 로 보고
 *   left 를 열 위치(11px)로 덮어썼다. 폭은 넓힌 그대로라 카드가 여백칸을 **오른쪽으로
 *   290px 삐져나갔다** — 왼쪽으로 넓어져야 하는데 오른쪽으로 밀린 것이다.
 * ⚠ 앞의 "고치기" 시험은 **통폭 카드**를 고쳐서 이걸 못 봤다. 반폭이던 카드를 고쳐야 보인다. */
const edw = await pg.evaluate(() => {
  const g = document.querySelector(".dnote-gut");
  const cards = [...g.querySelectorAll(".dn-card")];
  const t = cards.find((c) => c.classList.contains("dn-half")) || cards[0];
  if (!t) return { err: "카드가 없다" };
  const wasHalf = t.classList.contains("dn-half");
  const btn = t.querySelector(".dn-edit");
  if (!btn) return { err: "✎ 가 없다" };
  btn.click();
  const gr = g.getBoundingClientRect(), b = t.getBoundingClientRect();
  const ta = t.querySelector(".dn-in");
  return { wasHalf, gutW: Math.round(gr.width), w: Math.round(b.width),
           left: Math.round(b.left - gr.left), right: Math.round(b.right - gr.left),
           h: ta ? Math.round(ta.getBoundingClientRect().height) : 0,
           scroll: ta ? ta.scrollHeight : 0 };
});
chk(!edw.err, `[고치기·왼쪽] 카드를 고칠 수 있다 ${edw.err || ""}`);
if (!edw.err) {
  chk(edw.wasHalf, `[고치기·왼쪽] **반폭이던** 카드를 고른다 (통폭만 보면 이 버그가 안 보인다)`);
  chk(edw.left < 0,
      `[고치기·왼쪽·실측회귀] **왼쪽으로** 넓어진다 (left ${edw.left}px < 0)`);
  chk(edw.right <= edw.gutW + 1,
      `[고치기·왼쪽·음성] 오른쪽으로 삐져나가지 않는다 (오른끝 ${edw.right} ≤ 여백칸 ${edw.gutW})`);
  chk(edw.w > edw.gutW,
      `[고치기·왼쪽] 여백칸보다 넓어진다 (${edw.w} > ${edw.gutW}px)`);
  chk(edw.h <= edw.scroll + 10 && edw.h + 2 >= edw.scroll,
      `[고치기·왼쪽] 상자 높이가 글에 딱 맞는다 (${edw.h} ≈ ${edw.scroll})`);
}

/* ── ⤢ 넓게 보기 · 그림 확대 (1저자 2026-08-28) ─────────────────────────── */
const wide = await pg.evaluate(() => {
  const g = document.querySelector(".dnote-gut");
  const cards = [...g.querySelectorAll(".dn-card")];
  const t = cards.find((c) => c.classList.contains("dn-half")) || cards[0];
  if (!t) return { err: "카드가 없다" };
  const btn = t.querySelector(".dn-expand");
  if (!btn) return { err: "⤢ 가 없다" };
  const gr = g.getBoundingClientRect();
  const w0 = Math.round(t.getBoundingClientRect().width);
  const top0 = Math.round(t.getBoundingClientRect().top - gr.top);
  btn.click();
  const b1 = t.getBoundingClientRect();
  const on = { w: Math.round(b1.width), left: Math.round(b1.left - gr.left),
               right: Math.round(b1.right - gr.left),
               top: Math.round(b1.top - gr.top),
               editing: t.classList.contains("dn-editing"),
               hasTa: !!t.querySelector(".dn-in") };
  btn.click();                                   // 다시 눌러 되돌린다
  const w2 = Math.round(t.getBoundingClientRect().width);
  return { w0, top0, on, w2, gutW: Math.round(gr.width) };
});
chk(!wide.err, `[⤢] 버튼이 있다 ${wide.err || ""}`);
if (!wide.err) {
  chk(wide.on.w > wide.w0,
      `[⤢] 누르면 넓어진다 (${wide.w0} → ${wide.on.w}px)`);
  chk(wide.on.left < 0 && wide.on.right <= wide.gutW + 1,
      `[⤢] **왼쪽으로** 넓어지고 여백칸을 안 벗어난다 (left ${wide.on.left}, 오른끝 ${wide.on.right})`);
  // ⛔ 핵심: 넓게 보기는 **고치기가 아니다.** 입력창이 열리면 안 된다 —
  //   읽으려고 눌렀는데 편집이 시작되면 잘못 고칠 수 있다.
  chk(!wide.on.editing && !wide.on.hasTa,
      `[⤢·음성] 넓게 보기가 **고치기를 열지 않는다** (editing=${wide.on.editing}, 입력창=${wide.on.hasTa})`);
  chk(wide.w2 === wide.w0,
      `[⤢] 다시 누르면 되돌아온다 (${wide.on.w} → ${wide.w2}px, 원래 ${wide.w0})`);
}

/* 붙여넣은 그림을 누르면 확대창이 열린다 (카드 안에서는 잘라 두므로 원본 볼 길이 필요) */
const zoom = await pg.evaluate(() => {
  // ⚠ 앞 시험이 카드 하나를 **고치기 상태로 열어 둔 채** 끝난다. 그걸 집으면
  //   "그림을 눌러서 열렸다" 와 "원래 열려 있었다" 를 구분 못 한다 — 안 열린 카드를 고르고,
  //   절대 상태가 아니라 **전/후 변화**로 잰다.
  const card = [...document.querySelectorAll(".dn-card")]
    .find((c) => !c.classList.contains("dn-editing"));
  if (!card) return { err: "고치기 아닌 카드가 없다" };
  const wasEditing = card.classList.contains("dn-editing");
  const box = card.querySelector(".dn-text");
  box.innerHTML = window.noteFmt.inline(
    "![](/api/note-image/" + "a".repeat(32) + ".png)");
  const im = box.querySelector(".note-img");
  if (!im) return { err: "note-img 가 안 생겼다" };
  im.click();
  const m = document.getElementById("noteimg-lb");
  const openNow = !!(m && m.classList.contains("open"));
  const src = m ? m.querySelector("img").getAttribute("src") : null;
  const alsoEditing = card.classList.contains("dn-editing") && !wasEditing;
  // Esc 로 닫힌다
  document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
  return { openNow, src, alsoEditing,
           closed: !!(m && !m.classList.contains("open")) };
});
chk(!zoom.err, `[그림확대] 붙여넣은 그림이 렌더된다 ${zoom.err || ""}`);
if (!zoom.err) {
  chk(zoom.openNow, "[그림확대·실측회귀] 그림을 누르면 확대창이 열린다");
  chk(/note-image/.test(zoom.src || ""), `[그림확대] 원본 src 를 띄운다 (${zoom.src})`);
  // ⛔ 음성: 그림을 눌렀는데 "눌러서 고치기" 가 같이 열리면 안 된다
  chk(!zoom.alsoEditing,
      "[그림확대·음성] 그림을 눌러도 **고치기가 같이 열리지 않는다**");
  chk(zoom.closed, "[그림확대] Esc 로 닫힌다");
}

await b.close();
console.log(ok ? "docnote paint PASS" : "docnote paint FAIL");
process.exit(ok ? 0 : 1);
