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
import { readFileSync, existsSync, statSync } from "node:fs";
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
// ⚠ 2026-11-11 — 이 컨테이너는 `/opt/pw-browsers/chromium` 이 실행파일 (심볼릭 링크) 이라 옛 두 경로가 다 없어서
//   이 시험이 **SKIP** 으로 끝나고 있었다 (안 돈 시험). 파일일 때만 쓴다 — 다른 환경에선 그 이름이 폴더다.
const isFile = (p) => { try { return existsSync(p) && statSync(p).isFile(); } catch { return false; } };
const EXE = ["/opt/pw-browsers/chromium/chrome-linux/chrome",
             "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
             "/opt/pw-browsers/chromium"].find(isFile);
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

/* 여백은 **메모나 초안이 있을 때만** 열린다 (2026-10-28).
 * ⛔ 종전엔 mount 하자마자 여백을 열어서, 메모 0 건인 개념 페이지 15 쪽 전부에 빈 460px 여백이
 *   잡혔고 1920 화면에서 본문이 428px 로 눌렸다 (사용자 신고 · 실측). 음성 경로가 핵심이다. */
const gate = await pg.evaluate(async () => {
  window.fetch = function () {
    return Promise.resolve({ ok: true, json: () => Promise.resolve({ items: [] }) });
  };
  window.unmountDocNotes();
  const host = document.getElementById("pmbox");
  // 'dnote:toggle' (2026-11-17) — 여백이 열리고 닫힐 때만 host 에 온다 (iframe 높이를 그 자리에서 맞추는 쪽이 듣는다)
  const tog = [];
  const onTog = (e) => tog.push(e.detail.on);
  host.addEventListener("dnote:toggle", onTog);
  window.mountDocNotes(document.getElementById("body"), "kb/empty.md", host);
  await new Promise((r) => setTimeout(r, 300));
  const shown = () => { const g = host.querySelector(".dnote-gut");
                        return !!g && getComputedStyle(g).display !== "none"; };
  const empty = { on: host.classList.contains("dnote-on"), shown: shown(), tog: tog.join() };
  const p = document.querySelector("#body p");
  p.dispatchEvent(new MouseEvent("contextmenu", { bubbles: true, cancelable: true }));
  await new Promise((r) => setTimeout(r, 50));
  const draft = { on: host.classList.contains("dnote-on"), shown: shown(),
                  hasDraft: !!host.querySelector(".dn-draft"), tog: tog.join() };
  const x = host.querySelector(".dn-cancel");
  if (x) x.click();
  await new Promise((r) => setTimeout(r, 50));
  const back = { on: host.classList.contains("dnote-on"), shown: shown(), tog: tog.join() };
  host.removeEventListener("dnote:toggle", onTog);
  return { empty, draft, back };
});
chk(!gate.empty.on && !gate.empty.shown,
    `[여백 열기·음성] 메모 0 건이면 여백을 안 연다 (dnote-on=${gate.empty.on}, 보임=${gate.empty.shown})`);
chk(gate.draft.on && gate.draft.shown && gate.draft.hasDraft,
    `[여백 열기] 본문 오른쪽 클릭 초안이면 연다 (dnote-on=${gate.draft.on}, 보임=${gate.draft.shown}, 초안=${gate.draft.hasDraft})`);
chk(!gate.back.on && !gate.back.shown,
    `[여백 열기] 초안을 취소하면 다시 닫는다 (dnote-on=${gate.back.on}, 보임=${gate.back.shown})`);
chk(gate.empty.tog === "" && gate.draft.tog === "true" && gate.back.tog === "true,false",
    `[여백 열기·알림] host 에 'dnote:toggle' 은 열고 닫힐 때만 온다 — 메모 0 건으로 달 때는 안 온다 `
    + `(처음 "${gate.empty.tog}" → 초안 "${gate.draft.tog}" → 취소 "${gate.back.tog}")`);

/* 여백 접기 (2026-11-11 · 사용자 '메모 부분 접고 피는 버튼 상단에 있음 좋을듯').
 *   사용자 화면은 개념 페이지 (.concept-wrap = 목차 | 본문 | 메모 세 칸) 다 — 그 꼴로 잰다.
 *   (위 모달 조각 #pmbox 는 내용 폭으로 줄어드는 상자라 '본문이 넓어진다' 를 잴 수 없다 · 2026-11-11 실측.)
 *   localStorage 는 진짜 주소에서만 열린다 (setContent 의 about:blank 는 막힌다) — 가짜 http 주소로 띄운다.
 *   넓은 화면 (> 1280px) 이어야 '여백이 얇은 띠로 준다' 가 뜻을 갖는다 — 좁은 화면은 여백이 본문 아래로 쌓인다.
 *   ⛔ 음성: 접힌 채 오른쪽 클릭으로 새 메모를 열면 **숨은 초안**이 생기면 안 된다 (펴서 보인다). */
const pg2 = await b.newPage({ viewport: { width: 1600, height: 900 } });
await pg2.route("http://fold.test/**", (route) => route.fulfill({ contentType: "text/html; charset=utf-8", body:
  // ⚠ 실제 앱과 같은 틀 (body = flex · main.content = 남은 폭) 에 넣는다 — 틀 없이 .concept-wrap 만 두면
  //   flex 항목이 내용 폭으로 줄어서 '본문이 넓어진다' 를 잴 수 없다 (2026-11-11 실측 · 본문 414 → 414).
  `<!doctype html><meta charset="utf-8"><main class="content" id="main"><div class="concept-wrap"><nav class="concept-toc">목차</nav>
   <article class="doc concept" id="concept-body"><p>여기 한 노드 안에 통째로 들어 있는 문단이다. 첫 문단 끝</p>
   <p>두 번째 문단 시작 — 이어지는 문장이 있다.</p></article></div></main>` }));
await pg2.goto("http://fold.test/");
await pg2.addStyleTag({ path: CSS });
await pg2.addScriptTag({ path: CJS });
await pg2.addScriptTag({ path: JS });
const fold = await pg2.evaluate(async (note) => {
  window.fetch = function (url) {
    const hi = String(url).includes("/api/highlights/");
    return Promise.resolve({ ok: true, json: () => Promise.resolve({ items: hi ? [] : [note] }) });
  };
  localStorage.removeItem("dnote-folded");
  const host = document.querySelector(".concept-wrap");
  const body = document.getElementById("concept-body");
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const vis = (el) => !!el && getComputedStyle(el).display !== "none";
  const card = () => host.querySelector(".dn-card");
  const btn = () => host.querySelector(".dn-fold");
  const gutW = () => host.querySelector(".dnote-gut").getBoundingClientRect().width;
  window.mountDocNotes(body, "kb/fold.md", host);
  await wait(300);
  const s0 = { on: host.classList.contains("dnote-on"), folded: host.classList.contains("dnote-folded"),
               card: vis(card()), btn: vis(btn()), aria: btn() && btn().getAttribute("aria-expanded"),
               w: gutW(), bodyW: body.getBoundingClientRect().width };
  btn().click(); await wait(60);
  const s1 = { folded: host.classList.contains("dnote-folded"), card: vis(card()), btn: vis(btn()),
               aria: btn().getAttribute("aria-expanded"), stored: localStorage.getItem("dnote-folded"),
               w: gutW(), bodyW: body.getBoundingClientRect().width };
  window.unmountDocNotes();
  window.mountDocNotes(body, "kb/fold.md", host);
  await wait(300);
  const s2 = { folded: host.classList.contains("dnote-folded"), card: vis(card()) };
  body.querySelector("p").dispatchEvent(new MouseEvent("contextmenu", { bubbles: true, cancelable: true }));
  await wait(60);
  const s3 = { folded: host.classList.contains("dnote-folded"), draft: vis(host.querySelector(".dn-draft")),
               stored: localStorage.getItem("dnote-folded") };
  const x = host.querySelector(".dn-cancel"); if (x) x.click();
  await wait(60);
  const s4 = { folded: host.classList.contains("dnote-folded"), card: vis(card()) };
  btn().click(); await wait(60);
  const s5 = { folded: host.classList.contains("dnote-folded") };
  btn().click(); await wait(60);
  const s6 = { folded: host.classList.contains("dnote-folded"), card: vis(card()) };
  localStorage.removeItem("dnote-folded");
  return { s0, s1, s2, s3, s4, s5, s6 };
}, NOTE);
chk(fold.s0.on && !fold.s0.folded && fold.s0.card && fold.s0.btn && fold.s0.aria === "true",
    "[접기] 처음엔 펴져 있고 머리줄에 [접기] 버튼이 보인다");
chk(fold.s1.folded && !fold.s1.card && fold.s1.btn && fold.s1.aria === "false" && fold.s1.stored === "1",
    `[접기] 누르면 카드가 숨고 버튼은 남는다 · 브라우저에 기억 (localStorage ${fold.s1.stored})`);
chk(fold.s1.w < fold.s0.w / 3 && fold.s1.bodyW > fold.s0.bodyW + 200,
    `[접기] 여백이 얇은 띠로 줄고 본문이 넓어진다 (여백 ${Math.round(fold.s0.w)} → ${Math.round(fold.s1.w)} px · 본문 ${Math.round(fold.s0.bodyW)} → ${Math.round(fold.s1.bodyW)} px)`);
chk(fold.s2.folded && !fold.s2.card, "[접기] 다시 열어도 접힌 채다 (보는 사람 브라우저에 기억)");
chk(!fold.s3.folded && fold.s3.draft && fold.s3.stored === "0",
    "[접기·음성] 접힌 채 오른쪽 클릭하면 펴서 초안을 보인다 (숨은 초안 없음 · 편 상태를 기억)");
chk(!fold.s4.folded && fold.s4.card, "[접기] 초안을 닫아도 펴진 채 남고 카드가 보인다");
chk(fold.s5.folded && !fold.s6.folded && fold.s6.card, "[접기] 버튼으로 다시 접고 다시 편다 (오가기)");

/* 머리줄이 위에 붙는 목차 (#doctoc · 논문 페이지) 에 가리지 않는가 (2026-11-11 실측 — 굴리면 버튼이 목차 뒤로 숨었다).
 *   ⛔ 음성 대조: 목차가 없으면 0 으로 붙는다 (offset 이 늘 생기면 개념 페이지 머리줄이 괜히 내려간다). */
const toc = await pg2.evaluate(async () => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const host = document.querySelector(".concept-wrap");
  const gut = host.querySelector(".dnote-gut");
  const top0 = getComputedStyle(gut).getPropertyValue("--dn-h-top").trim();
  const nav = document.createElement("nav");
  nav.id = "doctoc";
  nav.style.cssText = "position:sticky;top:0;z-index:5;height:120px;background:#ddd";
  host.parentNode.insertBefore(nav, host);
  const filler = document.createElement("div"); filler.style.height = "3000px";
  document.getElementById("concept-body").appendChild(filler);
  window.dispatchEvent(new Event("resize"));
  await wait(200);
  window.scrollTo(0, 1500); await wait(200);
  const h = host.querySelector(".dn-h").getBoundingClientRect(), n = nav.getBoundingClientRect();
  return { top0, top1: getComputedStyle(gut).getPropertyValue("--dn-h-top").trim(), hTop: h.top, navBottom: n.bottom };
});
chk(toc.top0 === "0px", `[머리줄·음성 대조] 위에 붙는 목차가 없으면 0 으로 붙는다 (${toc.top0})`);
chk(toc.top1 === "124px" && toc.hTop >= toc.navBottom - 0.5,
    `[머리줄] 굴려도 [접기] 버튼이 위 목차 아래에 보인다 (--dn-h-top ${toc.top1} · 머리줄 위 ${Math.round(toc.hTop)} ≥ 목차 아래 ${Math.round(toc.navBottom)})`);

/* ── 본문이 iframe 안에 있을 때 (2026-11-17 · /interface-thermo · 사용자 '여기서도 메모랑 하이라이트' → '기존 포멧 가져와') ──
 *   그 화면의 보고서는 자기 CSS (변수 --bg 등이 웹앱과 겹친다) 를 가진 완결 HTML 이라 같은 출처 iframe 으로 띄우고,
 *   여백 (카드) 은 바깥 화면에 둔다. 아래 틀도 그렇게 짠다 — iframe 을 위에서 300 + 40px 밀어 둔다 (좌표 보정이 없으면 카드가 그만큼 어긋난다).
 *   본 것: ① 형광펜 · 메모 자리가 **iframe 문서 안**에 칠해지고 색이 보인다 (표시 CSS 가 iframe 으로만 옮겨졌다)
 *          ② 카드가 iframe 안 자기 줄 높이에 놓인다 (Playwright 가 따로 잰 상자끼리 비교)
 *          ③ ⛔음성: 자리 원소를 '문서에서 떨어졌다' 로 오인해 다시 그리기를 되풀이하지 않는다 (이 창 document 로 재면 그렇게 된다)
 *          ④ iframe 안 글을 골라 오른쪽 클릭 → 바깥 여백에 초안 · 고른 글이 인용된다 · ⑤ 펜을 켜고 iframe 안에서 고르면 칠하기 요청
 *          ⑥ ⛔음성: 떼고 나면 iframe 오른쪽 클릭이 초안을 안 만들고 브라우저 메뉴도 안 막는다 · 다시 달아도 CSS 는 한 벌
 *   못 보는 것: 진짜 마우스 드래그 (선택은 스크립트로 만든다) · 서버 저장 (fetch 가짜) — 실제 앱 화면 확인은 따로 한다. */
const FRAME_DOC = `<!doctype html><html><head><meta charset="utf-8"><style>
:root{--bg:#fffbeb;--accent:#0d9488}
body{margin:0;background:var(--bg);font:16px/1.75 sans-serif}
main{max-width:48rem;margin:0 auto;padding:2.5rem 16px 4rem}
</style></head><body><main>
<h1>보고서 제목</h1>
${Array.from({ length: 8 }, (_, i) => `<p>채움 문단 ${i + 1} — 자리를 아래로 내리는 글이다. 같은 말을 여러 번 되풀이해 줄을 채운다.</p>`).join("\n")}
<p id="ta">요약 — <b>LPSCl 은 Li 금속과</b> 닿으면 분해된다 는 문장이 여기 있다.</p>
<p id="tc">오른쪽 클릭으로 메모를 달 문단이다 — 앞머리 열두 글자를 고른다.</p>
<p id="td">형광펜으로 칠할 문단이다 — 앞머리 열 글자를 고른다.</p>
${Array.from({ length: 4 }, (_, i) => `<p>채움 문단 ${i + 9} — 조금 더 아래로.</p>`).join("\n")}
<p id="tb">Ag₂S 는 1.91 V 보다 높은 전위에서만 안정하다.</p>
</main></body></html>`;
const OUTER = `<!doctype html><meta charset="utf-8"><main class="content" id="main">
<div style="height:300px">머리 (iframe 을 아래로 민다)</div>
<div class="dn-host" id="fhost"><div style="min-width:0"><div style="height:40px">머리줄</div>
<iframe id="fr" src="/report" style="width:100%;height:1500px;border:1px solid #ccc;display:block"></iframe>
</div></div></main>`;
const FNOTE = { id: "f1", at: "2026-11-17 10:00", anchor: "Ag₂S 는 1.91 V 보다 높은 전위에서만 안정하다.",
                text: "iframe 안 문장에 붙인 메모" };
const FHL = [{ id: "fh1", text: "LPSCl 은 Li 금속과 닿으면 분해된다", color: "yellow", at: "2026-11-17" }];
const pg3 = await b.newPage({ viewport: { width: 1600, height: 900 } });
await pg3.route("http://frame.test/**", (route) => route.fulfill({
  contentType: "text/html; charset=utf-8",
  body: route.request().url().endsWith("/report") ? FRAME_DOC : OUTER }));
await pg3.goto("http://frame.test/");
await pg3.addStyleTag({ path: CSS });
await pg3.addScriptTag({ path: CJS });
await pg3.addScriptTag({ path: JS });
await pg3.waitForFunction(() => {
  const d = document.getElementById("fr").contentDocument;
  return !!(d && d.readyState === "complete" && d.getElementById("tb"));
}, null, { timeout: 5000 });
const fr = await pg3.evaluate(async ({ note, hl }) => {
  window.__calls = [];
  window.fetch = function (url, opt) {
    window.__calls.push([String(url), opt && opt.method, opt && opt.body]);
    const hi = String(url).includes("/api/highlights/");
    return Promise.resolve({ ok: true, json: () => Promise.resolve({ items: hi ? hl : [note] }) });
  };
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const fd = document.getElementById("fr").contentDocument;
  const host = document.getElementById("fhost");
  window.mountDocNotes(fd.querySelector("main"), "docs/x.html", host);
  await wait(400);
  const pens = [...fd.querySelectorAll("mark.dn-pen")];
  const m1 = fd.querySelector("mark.dn-hl");
  await wait(300);                                   // ③ — 그사이 다시 그렸으면 자리 원소가 바뀐다
  const st = fd.getElementById("dn-body-css");
  return {
    penN: pens.length, penText: pens.map((m) => m.textContent).join(""),
    penBg: pens.length ? fd.defaultView.getComputedStyle(pens[0]).backgroundColor : "",
    cssIn: !!st, cssRules: st ? (st.textContent.match(/\{/g) || []).length : 0,
    cssOut: !!document.getElementById("dn-body-css"),
    hl: !!m1, sameHl: !!m1 && m1 === fd.querySelector("mark.dn-hl") && m1.isConnected,
    card: !!host.querySelector(".dn-card"), cardInFrame: !!fd.querySelector(".dn-card"),
    on: host.classList.contains("dnote-on"),
  };
}, { note: FNOTE, hl: FHL });
chk(fr.penN >= 2 && norm(fr.penText) === FHL[0].text,
    `[iframe·형광] iframe 문서 안에 칠한다 — <b> 를 가로질러도 (조각 ${fr.penN}개)`);
chk(fr.cssIn && fr.cssRules >= 5 && /^rgb/.test(fr.penBg) && fr.penBg !== "rgba(0, 0, 0, 0)",
    `[iframe·CSS] 칠한 곳에 색이 보인다 — 본문 쪽 표시 규칙 ${fr.cssRules}개가 iframe 으로 옮겨졌다 (${fr.penBg})`);
chk(!fr.cssOut, "[iframe·CSS·음성] 옮긴 규칙은 iframe 에만 넣는다 — 바깥 문서에 사본이 안 생긴다");
chk(fr.hl && fr.card && !fr.cardInFrame && fr.on,
    "[iframe·메모] 메모 자리 표시는 iframe 안 · 카드는 바깥 여백에 (여백이 열린다)");
chk(fr.sameHl,
    "[iframe·음성] 자리 원소를 '떨어졌다' 로 오인해 다시 그리기를 되풀이하지 않는다 (300 ms 뒤에도 같은 원소)");
const fbox = await pg3.frameLocator("#fr").locator("mark.dn-hl").first().boundingBox();
const cbox = await pg3.locator("#fhost .dn-card").first().boundingBox();
chk(fbox && cbox && Math.abs(cbox.y - fbox.y) <= 4,
    `[iframe·자리·실측회귀] 카드가 iframe 안 자기 줄 높이에 놓인다 (카드 y ${cbox && Math.round(cbox.y)} · 자리 y ${fbox && Math.round(fbox.y)} · iframe 은 340px 밀려 있다)`);

const fctx = await pg3.evaluate(async () => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const f = document.getElementById("fr"), fd = f.contentDocument, fw = f.contentWindow;
  const host = document.getElementById("fhost");
  const p = fd.getElementById("tc"), r = fd.createRange();
  r.setStart(p.firstChild, 0); r.setEnd(p.firstChild, 12);
  const s = fw.getSelection(); s.removeAllRanges(); s.addRange(r);
  const picked = s.toString();
  const ev = new fw.MouseEvent("contextmenu", { bubbles: true, cancelable: true });
  p.dispatchEvent(ev);
  await wait(60);
  const d = host.querySelector(".dn-draft"), q = d && d.querySelector(".dn-quote");
  const res = { draft: !!d, quote: q ? q.textContent : "", picked, prevented: ev.defaultPrevented,
                live: p.classList.contains("dn-anch-live"),
                typing: !!(document.activeElement && document.activeElement.classList.contains("dn-in")) };
  const x = host.querySelector(".dn-cancel"); if (x) x.click();
  await wait(40);
  res.gone = !host.querySelector(".dn-draft") && !p.classList.contains("dn-anch-live");
  return res;
});
chk(fctx.draft && fctx.prevented && fctx.quote === fctx.picked.replace(/\s+/g, " ").trim(),
    `[iframe·오른쪽 클릭] iframe 안에서 고른 글로 바깥 여백에 초안이 열린다 ("${fctx.quote}")`);
chk(fctx.live && fctx.typing, "[iframe·오른쪽 클릭] 다는 자리 (iframe 문단) 가 표시되고 바깥 입력창에 바로 쓴다");
chk(fctx.gone, "[iframe] 초안을 취소하면 iframe 안 표시도 걷힌다");

const fpen = await pg3.evaluate(async () => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const f = document.getElementById("fr"), fd = f.contentDocument, fw = f.contentWindow;
  if (!document.getElementById("docpen")) {
    const el = document.createElement("button"); el.id = "docpen"; document.body.appendChild(el);
  }
  window.docnotePenToggle();                          // 켠다
  const bodyOn = fd.body.classList.contains("dn-pen-on");
  const p = fd.getElementById("td"), r = fd.createRange();
  r.setStart(p.firstChild, 0); r.setEnd(p.firstChild, 10);
  const s = fw.getSelection(); s.removeAllRanges(); s.addRange(r);
  const picked = s.toString();
  window.__calls = [];
  fd.querySelector("main").dispatchEvent(new fw.MouseEvent("mouseup", { bubbles: true }));
  await wait(60);
  const post = window.__calls.find((c) => c[1] === "POST" && c[0].includes("/api/highlights/"));
  window.docnotePenToggle();                          // 끈다
  return { bodyOn, bodyOff: !fd.body.classList.contains("dn-pen-on"), picked,
           sent: post ? JSON.parse(post[2]).text : null };
});
chk(fpen.sent === fpen.picked.replace(/\s+/g, " ").trim(),
    `[iframe·형광] 펜을 켜고 iframe 안에서 고르면 그 글로 칠하기 요청이 간다 ("${fpen.sent}")`);
chk(fpen.bodyOn && fpen.bodyOff, "[iframe·형광] 펜을 켜고 끄면 iframe body 에도 dn-pen-on 이 따라간다 (칠한 곳 커서)");

/* ⚠ '건 것을 거뒀다' 는 동작으로는 못 가른다 — 떼면 cur 가 없어서 남은 처리기도 아무 일을 안 한다
 *   (2026-11-17 일부러 거두기를 빼 봤더니 동작 시험은 그대로 초록이었다). 그래서 iframe 문서에 **걸려 있는 처리기 수**를
 *   DevTools 프로토콜로 직접 센다 (보고서 iframe 에는 자기 스크립트가 없어서 기준이 0 이다). */
/*   ⚠ 바깥 창에서 `contentDocument` 를 evaluate 한 객체로 물으면 늘 0 개다 (2026-11-17 실측 — 처리기는 문서의 세계 기준으로 센다).
 *     DOM 트리에서 iframe 의 문서 노드를 찾아 **그 문서 쪽 객체**로 풀어서 묻는다. */
const cdp = await pg3.context().newCDPSession(pg3);
const frameListeners = async () => {
  const { root } = await cdp.send("DOM.getDocument", { depth: -1, pierce: true });
  const find = (n) => n.nodeName === "IFRAME" ? n
    : (n.children || []).reduce((hit, c) => hit || find(c), null);
  const { object } = await cdp.send("DOM.resolveNode", { nodeId: find(root).contentDocument.nodeId });
  const { listeners } = await cdp.send("DOMDebugger.getEventListeners", { objectId: object.objectId });
  return listeners.filter((l) => l.type === "contextmenu" || l.type === "keydown").length;
};
const nOn = await frameListeners();
const foff = await pg3.evaluate(async () => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const f = document.getElementById("fr"), fd = f.contentDocument, fw = f.contentWindow;
  const host = document.getElementById("fhost");
  window.unmountDocNotes();
  const p = fd.getElementById("tc");
  const ev = new fw.MouseEvent("contextmenu", { bubbles: true, cancelable: true });
  p.dispatchEvent(ev);
  await wait(40);
  return { draft: !!host.querySelector(".dn-draft"), prevented: ev.defaultPrevented,
           marks: fd.querySelectorAll("mark.dn-pen,mark.dn-hl").length };
});
const nOff = await frameListeners();
const fagain = await pg3.evaluate(async () => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const fd = document.getElementById("fr").contentDocument;
  window.mountDocNotes(fd.querySelector("main"), "docs/x.html", document.getElementById("fhost"));   // 다시 단다
  await wait(300);
  return { cssN: fd.querySelectorAll("#dn-body-css").length, pens: fd.querySelectorAll("mark.dn-pen").length };
});
const nAgain = await frameListeners();
await pg3.evaluate(() => window.unmountDocNotes());
chk(!foff.draft && !foff.prevented,
    "[iframe·음성] 떼고 나면 iframe 오른쪽 클릭이 초안을 안 만들고 브라우저 메뉴도 안 막는다");
chk(nOn === 2 && nOff === 0 && nAgain === 2,
    `[iframe·음성] 떼면 iframe 문서에 건 오른쪽 클릭 · Esc 처리기를 거두고, 다시 달아도 한 벌이다 (단 동안 ${nOn} → 뗀 뒤 ${nOff} → 다시 ${nAgain})`);
chk(foff.marks === 0, "[iframe] 떼면 iframe 안 칠한 표시가 걷힌다");
chk(fagain.cssN === 1 && fagain.pens >= 2,
    `[iframe] 다시 달면 다시 칠하고 옮긴 CSS 는 한 벌이다 (${fagain.cssN}벌)`);

/* ?note= 딥링크 — host 가 '여백이 열렸다' 를 **굴리기 전에** 들어야 한다 (2026-11-17 1440px 실측).
 *   여백이 열리면 iframe 칸이 좁아져 보고서가 길어진다. 띄우는 쪽은 그 알림 (dnote:toggle) 에서 iframe 높이를 맞추는데,
 *   알림이 굴리기보다 늦으면 굴리기가 아직 짧은 iframe 의 안쪽을 굴리고, 높이를 맞추는 순간 자리가 밀린다 (873/900 — 가운데가 아니라 아래 끝).
 *   그래서 **순서**를 본다: 알림 → 그 메모 자리 굴리기. (iframe 안 원소의 scrollIntoView 는 iframe 세계의 것을 감싼다.) */
const fdeep = await pg3.evaluate(async () => {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const fd = document.getElementById("fr").contentDocument;
  const host = document.getElementById("fhost");
  const seq = [];
  const onTog = (e) => seq.push("toggle:" + e.detail.on);
  host.addEventListener("dnote:toggle", onTog);
  const P = fd.defaultView.Element.prototype, orig = P.scrollIntoView;
  P.scrollIntoView = function () { seq.push("scroll:" + this.tagName); return orig.apply(this, arguments); };
  history.replaceState(null, "", "/?note=f1");
  try {
    window.mountDocNotes(fd.querySelector("main"), "docs/x.html", host);
    await wait(500);
  } finally {
    P.scrollIntoView = orig;
    history.replaceState(null, "", "/");
    host.removeEventListener("dnote:toggle", onTog);
  }
  // ⚠ 카드의 dn-focus 표시로는 안 본다 — 형광펜 응답이 뒤따라 여백을 다시 그리면 그 표시가 지워진다 (기존 동작 · 여기 일이 아니다).
  //   iframe 세계의 MARK 굴리기 = focusNote 가 그 메모 자리로 데려간 것이다 (다른 굴리기는 바깥 문서 원소다).
  window.unmountDocNotes();
  return { seq };
});
const iTog = fdeep.seq.indexOf("toggle:true"), iScroll = fdeep.seq.indexOf("scroll:MARK");
chk(iTog >= 0 && iScroll > iTog,
    `[iframe·딥링크·실측회귀] 여백이 열렸다는 알림이 그 메모 자리 굴리기보다 먼저 온다 (${fdeep.seq.join(" → ")})`);

await b.close();
console.log(ok ? "docnote paint PASS" : "docnote paint FAIL");
process.exit(ok ? 0 : 1);
