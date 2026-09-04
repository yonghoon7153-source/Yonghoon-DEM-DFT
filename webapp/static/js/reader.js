/* reader.js — 전체화면 리더 (긴 digest 를 본문만 남기고 읽는 모드)
 *
 * ★ 왜 DOM 을 복제하지 않는가
 *   이 페이지의 하이라이트·메모(app.js)와 그림 팝업(figref.js)은 **본문의 실제
 *   DOM 노드**에 걸려 있다. 모달을 따로 만들어 본문을 복제하면 같은 문단이 두
 *   벌 생기고, localStorage 에 저장된 주석 좌표가 어느 쪽을 가리키는지 모호해진다
 *   (그리고 한쪽에 칠한 하이라이트가 다른 쪽에 안 뜬다).
 *   그래서 이 리더는 **같은 노드를 CSS 로 전체화면에 놓는 모드**다 —
 *   `<body class="rd-on">` 하나로 레이아웃만 바뀌고 본문 노드는 그대로다.
 *   그 덕에 메모·하이라이트·그림 팝업이 리더 안에서도 **그냥 된다**.
 *
 * ⚠ CSP: 인라인 <script> 금지. 이 파일은 base.html 에서 defer 로 불린다.
 * ⚠ 이 앱은 저장소에 아무것도 쓰지 않는다. 여기서 저장하는 것은 **읽기 취향**
 *   (글자 크기·본문 폭·목차/메모 접힘)뿐이고 전부 이 브라우저 localStorage 다.
 */
(function () {
  "use strict";

  var reader = document.querySelector(".reader");
  var art = reader && reader.querySelector(".doc-body");
  if (!reader || !art) return;                 // 리더가 있는 문서에서만 뜬다

  var PREF = "bms.read.pref";
  var FS_MIN = 0.85, FS_MAX = 1.45, FS_STEP = 0.05;
  var MEASURES = ["78ch", "92ch", "64ch"];     // 기본 → 넓게 → 좁게

  var pref = { fs: 1, m: 0, toc: 1, rail: 1 };
  try {
    var raw = localStorage.getItem(PREF);
    if (raw) {
      var got = JSON.parse(raw);
      if (got && typeof got === "object") {
        if (typeof got.fs === "number") pref.fs = Math.min(FS_MAX, Math.max(FS_MIN, got.fs));
        if (typeof got.m === "number") pref.m = ((got.m % MEASURES.length) + MEASURES.length) % MEASURES.length;
        if (typeof got.toc === "number") pref.toc = got.toc ? 1 : 0;
        if (typeof got.rail === "number") pref.rail = got.rail ? 1 : 0;
      }
    }
  } catch (e) { /* 저장 접근이 막힌 브라우저 — 기본값으로 간다 */ }

  function save() {
    try { localStorage.setItem(PREF, JSON.stringify(pref)); } catch (e) { /* 무시 */ }
  }

  /* ── 진입 버튼 — 본문 바로 위에 둔다 ─────────────────────────────────── */
  var cta = document.createElement("div");
  cta.className = "rd-cta";
  var open = document.createElement("button");
  open.type = "button";
  open.className = "btn rd-open";
  open.appendChild(document.createTextNode("전체화면으로 읽기"));
  var kb = document.createElement("kbd");
  kb.className = "kbd";
  kb.textContent = "F";
  open.appendChild(kb);
  var note = document.createElement("span");
  note.className = "rd-cta-n";
  note.textContent = "사이드바·머리글을 접고 본문만 남긴다. 메모·하이라이트·그림 팝업은 그대로 된다.";
  cta.appendChild(open);
  cta.appendChild(note);
  reader.parentNode.insertBefore(cta, reader);

  /* ── 위 막대 ─────────────────────────────────────────────────────────── */
  var bar = document.createElement("div");
  bar.className = "rd-bar";
  bar.hidden = true;

  var prog = document.createElement("div");
  prog.className = "rd-prog";
  var progIn = document.createElement("i");
  prog.appendChild(progIn);
  bar.appendChild(prog);

  var row = document.createElement("div");
  row.className = "rd-row";
  bar.appendChild(row);

  var titleEl = document.createElement("span");
  titleEl.className = "rd-title";
  var h1 = document.querySelector(".phead h1");
  titleEl.textContent = h1 ? h1.textContent : document.title;
  row.appendChild(titleEl);

  var pct = document.createElement("span");
  pct.className = "rd-pct";
  pct.textContent = "0%";
  row.appendChild(pct);

  function mkBtn(act, label, title, cls) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "rd-b" + (cls ? " " + cls : "");
    b.setAttribute("data-rd", act);
    b.title = title;
    b.textContent = label;
    row.appendChild(b);
    return b;
  }

  var grp = document.createElement("span");
  grp.className = "rd-grp";
  row.appendChild(grp);
  function mkGrpBtn(act, label, title) {
    var b = mkBtn(act, label, title);
    grp.appendChild(b);                        // row 끝에 붙은 것을 묶음으로 옮긴다
    return b;
  }
  mkGrpBtn("fs-", "A−", "글자 작게");
  var fsNow = document.createElement("span");
  fsNow.className = "rd-fsn";
  grp.appendChild(fsNow);
  mkGrpBtn("fs+", "A＋", "글자 크게");

  mkBtn("m", "폭", "본문 폭 바꾸기 (기본 → 넓게 → 좁게)");
  var bToc = mkBtn("toc", "목차", "목차 칸 접기/펴기", "rd-wide-only");
  var bRail = mkBtn("rail", "메모", "메모 칸 접기/펴기", "rd-wide-only");
  if (!reader.classList.contains("reader-3")) bRail.hidden = true;
  var bClose = mkBtn("close", "닫기", "리더 닫기 (Esc)", "rd-close");
  var kb2 = document.createElement("kbd");
  kb2.className = "kbd";
  kb2.textContent = "esc";
  bClose.appendChild(kb2);

  document.body.appendChild(bar);

  /* ── 상태 반영 ───────────────────────────────────────────────────────── */
  function applyPref() {
    fsNow.textContent = Math.round(pref.fs * 100) + "%";
    reader.style.setProperty("--measure", on ? MEASURES[pref.m] : "");
    // 모드가 꺼져 있을 때는 흔적을 남기지 않는다 — 보통 화면의 레이아웃은 그대로여야 한다
    document.body.classList.toggle("rd-no-toc", on && !pref.toc);
    document.body.classList.toggle("rd-no-rail", on && !pref.rail);
    bToc.setAttribute("aria-pressed", pref.toc ? "true" : "false");
    bRail.setAttribute("aria-pressed", pref.rail ? "true" : "false");
    // rem 토큰 전체가 따라오도록 루트 글자 크기를 움직인다 (제목·표까지 같이 큰다)
    document.documentElement.style.fontSize = on ? (16 * pref.fs) + "px" : "";
  }

  /* ── 진행률 ──────────────────────────────────────────────────────────── */
  function tick() {
    var max = art.scrollHeight - art.clientHeight;
    var r = max > 4 ? art.scrollTop / max : 0;
    r = Math.min(1, Math.max(0, r));
    progIn.style.width = (r * 100).toFixed(2) + "%";
    pct.textContent = Math.round(r * 100) + "%";
  }

  /* ── 모드 전환 — 읽던 자리를 지킨다 ───────────────────────────────────
     너비가 바뀌면 픽셀 오프셋은 의미를 잃는다. 그래서 **화면 맨 위에 걸린
     제목**을 기억했다가 전환 뒤 그 제목으로 되돌아간다. */
  function topHeading() {
    var hs = art.querySelectorAll("h1, h2, h3, h4");
    var last = null;
    for (var i = 0; i < hs.length; i++) {
      var t = hs[i].getBoundingClientRect().top;
      if (t >= -4) return hs[i];
      last = hs[i];
    }
    return last;
  }

  var on = false;
  function setMode(next) {
    if (next === on) return;
    var anchor = topHeading();
    on = next;
    document.body.classList.toggle("rd-on", on);
    bar.hidden = !on;
    open.setAttribute("aria-expanded", on ? "true" : "false");
    applyPref();
    // 배치가 두 번 바뀐다 (모드 클래스 → 루트 글자 크기). 한 프레임만 기다리면
    // 아직 옛 높이로 계산해 엉뚱한 자리에 선다 — 두 프레임 뒤에 옮긴다.
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        if (anchor) anchor.scrollIntoView({ block: "start" });
        else if (on) art.scrollTop = 0;
        tick();
      });
    });
    if (on) art.focus({ preventScroll: true });
  }

  art.setAttribute("tabindex", "-1");          // 키보드 스크롤이 바로 먹게
  art.addEventListener("scroll", tick, { passive: true });
  window.addEventListener("resize", tick);

  open.addEventListener("click", function () { setMode(true); });

  bar.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("[data-rd]") : null;
    if (!b) return;
    var a = b.getAttribute("data-rd");
    if (a === "close") { setMode(false); return; }
    if (a === "fs+") pref.fs = Math.min(FS_MAX, Math.round((pref.fs + FS_STEP) * 100) / 100);
    else if (a === "fs-") pref.fs = Math.max(FS_MIN, Math.round((pref.fs - FS_STEP) * 100) / 100);
    else if (a === "m") pref.m = (pref.m + 1) % MEASURES.length;
    else if (a === "toc") pref.toc = pref.toc ? 0 : 1;
    else if (a === "rail") pref.rail = pref.rail ? 0 : 1;
    applyPref();
    save();
    requestAnimationFrame(tick);
  });

  /* ── 자판 ────────────────────────────────────────────────────────────
     `f` 로 들어가고 `esc` 로 나온다. 입력칸(메모 textarea 포함) 안에서는
     아무것도 하지 않는다 — 메모를 쓰다 f 를 누르면 화면이 뒤집히면 안 된다. */
  document.addEventListener("keydown", function (e) {
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName || ""))) return;
    if (e.key === "Escape" && on) {
      var cmdk = document.getElementById("cmdk");
      if (cmdk && !cmdk.hidden) return;        // 팔레트가 열려 있으면 그쪽이 먼저다
      e.preventDefault();
      setMode(false);
      return;
    }
    if ((e.key === "f" || e.key === "F") && !on) { e.preventDefault(); setMode(true); }
  });

  applyPref();
  tick();
})();
