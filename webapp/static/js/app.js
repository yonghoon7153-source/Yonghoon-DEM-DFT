/* app.js — 커맨드 팔레트(⌘K / Ctrl-K) + 목차 스크롤스파이.
 *
 * 왜 바닐라인가: CSP 가 `default-src 'self'` 라 CDN 이 막힌다. 그런데 여기 필요한
 * 것은 "목록을 걸러 보여주고 키로 고르기" 와 "지금 보이는 제목 표시" 둘뿐이라
 * 프레임워크가 있어도 줄어들 코드가 없다.
 *
 * ⚠ innerHTML 을 쓰지 않는다. 팔레트 항목의 제목·설명은 위키 파일에서 온 문자열이고,
 *   이 앱은 그 파일들을 100% 신뢰 대상으로 두지 않는다 (마크다운 렌더에서 raw HTML 을
 *   끈 것과 같은 이유). 전부 textContent 로 넣는다.
 */
(function () {
  "use strict";

  /* ═══ 커맨드 팔레트 ═══════════════════════════════════════════════════ */
  var box = document.getElementById("cmdk");
  var input = document.getElementById("cmdk-q");
  var list = document.getElementById("cmdk-list");
  var items = null;          // /api/palette.json 의 결과 (한 번만 가져온다)
  var shown = [];
  var cur = 0;
  var loading = false;

  var MAC = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent || "");

  function hint() {
    var k = document.getElementById("cmdkhint");
    if (k) k.textContent = MAC ? "⌘K" : "Ctrl K";
  }

  function load() {
    if (items || loading) return Promise.resolve();
    loading = true;
    return fetch("/api/palette.json")
      .then(function (r) { return r.ok ? r.json() : { items: [] }; })
      .then(function (d) { items = d.items || []; })
      .catch(function () { items = []; })      // 못 가져와도 팔레트는 검색으로 쓸 수 있다
      .then(function () { loading = false; });
  }

  /* 점수: 제목 앞부분 일치 > 제목 포함 > slug 포함 > 설명 포함.
     형태소 분석 같은 건 없다 — 목적지가 스무 개 남짓이라 필요가 없다. */
  function score(it, q) {
    var t = (it.t || "").toLowerCase();
    var s = (it.s || "").toLowerCase();
    var d = (it.d || "").toLowerCase();
    if (t.indexOf(q) === 0) return 100;
    if (t.indexOf(q) >= 0) return 70;
    if (s.indexOf(q) >= 0) return 50;
    if (d.indexOf(q) >= 0) return 20;
    return -1;
  }

  function row(it, i) {
    var li = document.createElement("li");
    li.className = "cmdk-i" + (i === cur ? " is-on" : "");
    li.setAttribute("role", "option");
    li.setAttribute("aria-selected", String(i === cur));
    li.dataset.url = it.u;

    var t = document.createElement("span");
    t.className = "cmdk-t";
    t.textContent = it.t;                      // ⚠ textContent — 위키에서 온 문자열이다
    var k = document.createElement("span");
    k.className = "cmdk-k";
    k.textContent = it.k || "";
    var d = document.createElement("span");
    d.className = "cmdk-d";
    d.textContent = it.d || "";

    li.appendChild(t); li.appendChild(k); li.appendChild(d);
    li.addEventListener("click", function () { go(it.u); });
    return li;
  }

  function paint() {
    var q = (input.value || "").trim().toLowerCase();
    var pool = items || [];
    if (!q) {
      shown = pool.slice(0, 12);
    } else {
      shown = pool
        .map(function (it) { return { it: it, sc: score(it, q) }; })
        .filter(function (x) { return x.sc >= 0; })
        .sort(function (a, b) { return b.sc - a.sc; })
        .slice(0, 20)
        .map(function (x) { return x.it; });
      // 이름으로 못 찾으면 전문 검색으로 넘어갈 길을 항상 하나 남긴다
      shown.push({ t: "전문 검색: " + input.value.trim(), k: "검색",
                   d: "본문까지 훑는다", u: "/search?q=" + encodeURIComponent(input.value.trim()) });
    }
    if (cur >= shown.length) cur = Math.max(0, shown.length - 1);

    list.textContent = "";
    if (!shown.length) {
      var e = document.createElement("li");
      e.className = "cmdk-empty";
      e.textContent = items === null ? "불러오는 중…" : "그런 이름의 페이지가 없다.";
      list.appendChild(e);
      return;
    }
    shown.forEach(function (it, i) { list.appendChild(row(it, i)); });
  }

  function move(step) {
    if (!shown.length) return;
    cur = (cur + step + shown.length) % shown.length;
    paint();
    var on = list.querySelector(".is-on");
    if (on && on.scrollIntoView) on.scrollIntoView({ block: "nearest" });
  }

  function go(url) { if (url) window.location.href = url; }

  function open() {
    if (!box) return;
    box.hidden = false;
    input.value = "";
    cur = 0;
    paint();
    input.focus();
    load().then(paint);
  }

  function close() { if (box) box.hidden = true; }

  if (box && input && list) {
    hint();
    var btn = document.getElementById("cmdkbtn");
    if (btn) btn.addEventListener("click", open);
    Array.prototype.forEach.call(box.querySelectorAll("[data-cmdk-close]"), function (el) {
      el.addEventListener("click", close);
    });
    input.addEventListener("input", function () { cur = 0; paint(); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") { e.preventDefault(); if (shown[cur]) go(shown[cur].u); }
      else if (e.key === "Escape") { e.preventDefault(); close(); }
    });

    document.addEventListener("keydown", function (e) {
      if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) {
        e.preventDefault();
        if (box.hidden) open(); else close();
        return;
      }
      if (e.key === "Escape" && !box.hidden) close();
      // `/` 로도 연다 — 단, 글자를 치고 있는 중이면 가로채지 않는다
      if (e.key === "/" && box.hidden) {
        var a = document.activeElement;
        var tag = a && a.tagName;
        if (tag === "INPUT" || tag === "TEXTAREA" || (a && a.isContentEditable)) return;
        e.preventDefault();
        open();
      }
    });
  }

  /* ═══ 목차 스크롤스파이 ═══════════════════════════════════════════════
     "지금 어디를 읽고 있는가" 를 목차에 표시한다. 6만 자 문서에서는 이게 없으면
     목차가 그냥 링크 목록이지 위치 감각을 주지 못한다.

     화면에 걸린 제목 중 **가장 위**의 것을 현재로 삼는다. 하나도 안 걸려 있으면
     (긴 절의 한가운데) 마지막으로 지나간 제목을 유지한다. */
  var links = document.querySelectorAll("[data-toc]");
  if (links.length && "IntersectionObserver" in window) {
    var byId = {};
    var targets = [];
    Array.prototype.forEach.call(links, function (a) {
      var id = a.getAttribute("data-toc");
      var el = document.getElementById(id);
      if (!el) return;
      byId[id] = a;
      targets.push(el);
    });

    var visible = Object.create(null);
    var last = null;

    function mark() {
      var ids = Object.keys(visible).filter(function (k) { return visible[k]; });
      var pick = last;
      if (ids.length) {
        // 문서 순서로 가장 앞선 것
        pick = ids.reduce(function (best, id) {
          if (!best) return id;
          var a = document.getElementById(id), b = document.getElementById(best);
          return (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING) ? id : best;
        }, null);
      }
      if (!pick || pick === last) return;
      if (last && byId[last]) byId[last].classList.remove("is-here");
      if (byId[pick]) byId[pick].classList.add("is-here");
      last = pick;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting; });
      mark();
    }, {
      // 위쪽 여백을 크게 잡아 "화면 상단을 막 지난 제목" 이 현재가 되게 한다
      rootMargin: "-8% 0px -72% 0px",
      threshold: 0
    });
    targets.forEach(function (el) { io.observe(el); });
  }
})();

/* ── 접힌 안쪽으로 가는 앵커 ──────────────────────────────────────────────
   `/results` 는 노트·CSV 를 <details> 로 접는다. 접힌 안의 제목으로 가는
   링크는 브라우저가 열어 주지 않는 경우가 있어, 눌러도 아무 일이 없는 것처럼
   보인다. 조상 <details> 를 전부 열고 나서 스크롤한다. */
function openToHash(hash) {
  var id = (hash || "").replace(/^#/, "");
  if (!id) return;
  var t = document.getElementById(id);
  if (!t) return;
  var d = t.closest("details");
  var opened = false;
  while (d) {
    if (!d.open) { d.open = true; opened = true; }
    d = d.parentElement ? d.parentElement.closest("details") : null;
  }
  // 방금 편 것이 있으면 배치가 끝난 **다음 프레임**에 스크롤한다. 같은 프레임에
  // 부르면 아직 접힌 높이로 계산해 엉뚱한 곳에 선다 (실측: top 1727px).
  if (opened) requestAnimationFrame(function () { t.scrollIntoView({ block: "start" }); });
  else t.scrollIntoView({ block: "start" });
}
window.addEventListener("hashchange", function () { openToHash(location.hash); });
document.addEventListener("click", function (e) {
  var a = e.target.closest && e.target.closest('a[href^="#"]');
  if (!a) return;
  var h = a.getAttribute("href");
  if (h && h.length > 1 && document.getElementById(h.slice(1))) {
    e.preventDefault();
    if (location.hash !== h) history.pushState(null, "", h);
    openToHash(h);
  }
});
if (location.hash) openToHash(location.hash);

/* ══ 메모 · 하이라이트 ════════════════════════════════════════════════════
   ⚠ 이 앱은 저장소에 **아무것도 쓰지 않는다**. 메모와 하이라이트는 읽는 사람의
     주석이지 위키의 내용이 아니므로 브라우저 안(localStorage)에만 남는다.
     그래서 "화면의 정본은 저장소 파일" 이라는 약속이 문자 그대로 유지된다.

   저장 좌표를 **문자열 offset 이 아니라 (제목 id, 그 절 안의 문자 위치)** 로
   잡는다. 문서가 갱신돼 앞부분이 길어져도 절 안에서 다시 찾을 수 있어야 하고,
   못 찾으면 **조용히 엉뚱한 곳에 칠하지 않고** 고아로 표시한다 — 잘못된 자리에
   칠한 하이라이트는 없는 것보다 나쁘다. */
(function () {
  var reader = document.querySelector(".reader[data-annot]");
  if (!reader) return;
  var body = document.getElementById("digest-body");
  var rail = document.getElementById("annot-list");
  var bar = document.getElementById("sel-bar");
  if (!body || !rail || !bar) return;

  var KEY = "bms.annot." + reader.getAttribute("data-annot");
  var HUES = { y: "노랑", g: "초록", p: "보라", r: "빨강" };

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "[]"); }
    catch (e) { return []; }            // 사설창·저장 차단 — 기능만 죽고 화면은 산다
  }
  function save(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); }
    catch (e) { /* 저장이 막힌 브라우저 — 이번 세션에만 남는다 */ }
  }

  /* 선택 구간을 (절 id, 절 안 문자 offset, 길이, 원문) 으로 적는다 */
  function sectionOf(node) {
    var el = node.nodeType === 3 ? node.parentElement : node;
    while (el && el !== body) {
      var prev = el.previousElementSibling;
      while (prev) {
        if (/^H[1-6]$/.test(prev.tagName) && prev.id) return prev.id;
        prev = prev.previousElementSibling;
      }
      el = el.parentElement;
    }
    return "";
  }
  function sectionRoot(id) {
    var h = id && document.getElementById(id);
    return h ? h.parentElement : body;
  }
  function textOf(root, stopAtId) {
    // 절 텍스트: 제목 다음부터 다음 같은 수준 제목 전까지
    var h = stopAtId && document.getElementById(stopAtId);
    if (!h) return body.textContent;
    var out = "", n = h.nextElementSibling;
    while (n && !/^H[1-6]$/.test(n.tagName)) { out += n.textContent; n = n.nextElementSibling; }
    return out;
  }

  function capture() {
    var sel = window.getSelection();
    if (!sel || sel.isCollapsed) return null;
    var text = String(sel).trim();
    if (!text || text.length < 2) return null;
    var r = sel.getRangeAt(0);
    if (!body.contains(r.commonAncestorContainer)) return null;
    var sid = sectionOf(r.startContainer);
    var hay = textOf(body, sid);
    var at = hay.indexOf(text);
    return { sec: sid, at: at, len: text.length, text: text,
             at_kind: at < 0 ? "unfound" : "found" };
  }

  function add(hue, note) {
    var c = capture();
    if (!c) return;
    var list = load();
    list.push({ id: "a" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
                hue: hue || "y", note: note || "", sec: c.sec, at: c.at,
                len: c.len, text: c.text, at_kind: c.at_kind,
                made: new Date().toISOString().slice(0, 16).replace("T", " ") });
    save(list);
    window.getSelection().removeAllRanges();
    render();
  }

  /* ── 그리기 ─────────────────────────────────────────────────────────── */
  function clearMarks() {
    body.querySelectorAll("mark.hl").forEach(function (m) {
      var t = document.createTextNode(m.textContent);
      m.parentNode.replaceChild(t, m);
    });
    body.normalize();
  }

  function paint(a) {
    // 절 안에서 원문을 다시 찾는다. 못 찾으면 칠하지 않고 고아로 둔다.
    var h = a.sec && document.getElementById(a.sec);
    var start = h ? h.nextElementSibling : body.firstElementChild;
    var walkRoot = [];
    var n = start;
    while (n && !(h && /^H[1-6]$/.test(n.tagName))) { walkRoot.push(n); n = n.nextElementSibling; }
    if (!walkRoot.length) walkRoot = [body];
    for (var i = 0; i < walkRoot.length; i++) {
      var w = document.createTreeWalker(walkRoot[i], NodeFilter.SHOW_TEXT);
      var tn;
      while ((tn = w.nextNode())) {
        var k = tn.nodeValue.indexOf(a.text);
        if (k < 0) continue;
        var rg = document.createRange();
        rg.setStart(tn, k); rg.setEnd(tn, k + a.text.length);
        var m = document.createElement("mark");
        m.className = "hl hl-" + (a.hue || "y");
        m.setAttribute("data-annot-id", a.id);
        if (a.note) m.setAttribute("data-has-note", "1");
        try { rg.surroundContents(m); return true; } catch (e) { return false; }
      }
    }
    return false;
  }

  function render() {
    var list = load();
    clearMarks();
    var orphan = 0;
    list.forEach(function (a) { if (!paint(a)) { a.stale = true; orphan++; } else { a.stale = false; } });

    rail.textContent = "";
    var nNotes = 0;
    list.forEach(function (a) {
      if (a.note) nNotes++;
      var li = document.createElement("li");
      li.className = "rail-i hl-" + (a.hue || "y") + (a.stale ? " is-stale" : "");
      li.setAttribute("data-annot-id", a.id);

      var q = document.createElement("blockquote");
      q.className = "rail-q";
      q.textContent = a.text.length > 180 ? a.text.slice(0, 180) + "…" : a.text;
      li.appendChild(q);

      if (a.stale) {
        var w = document.createElement("p");
        w.className = "rail-stale";
        w.textContent = "본문에서 이 구절을 찾지 못했다 — 문서가 바뀐 것 같다. "
                      + "엉뚱한 곳에 칠하지 않으려고 표시만 남긴다.";
        li.appendChild(w);
      }

      var ta = document.createElement("textarea");
      ta.className = "rail-note";
      ta.rows = a.note ? 3 : 1;
      ta.placeholder = "메모…";
      ta.value = a.note || "";
      ta.addEventListener("input", function () {
        var l = load(), t = l.find(function (x) { return x.id === a.id; });
        if (t) { t.note = ta.value; save(l); }
        document.getElementById("note-n").textContent =
          String(l.filter(function (x) { return x.note; }).length);
      });
      li.appendChild(ta);

      var foot = document.createElement("div");
      foot.className = "rail-foot";
      var when = document.createElement("span");
      when.className = "rail-when"; when.textContent = a.made || "";
      foot.appendChild(when);
      var del = document.createElement("button");
      del.type = "button"; del.className = "btn btn-xs btn-ghost";
      del.textContent = "지움";
      del.addEventListener("click", function () {
        save(load().filter(function (x) { return x.id !== a.id; }));
        render();
      });
      foot.appendChild(del);
      li.appendChild(foot);

      li.addEventListener("click", function (e) {
        if (e.target.tagName === "TEXTAREA" || e.target.tagName === "BUTTON") return;
        var m = body.querySelector('mark[data-annot-id="' + a.id + '"]');
        if (m) m.scrollIntoView({ block: "center" });
      });
      rail.appendChild(li);
    });

    document.getElementById("note-n").textContent = String(nNotes);
    var hint = document.getElementById("annot-hint");
    if (hint) hint.hidden = list.length > 0;
  }

  /* ── 선택 도구막대 ──────────────────────────────────────────────────── */
  function placeBar() {
    var sel = window.getSelection();
    if (!sel || sel.isCollapsed || !body.contains(sel.anchorNode)) { bar.hidden = true; return; }
    var r = sel.getRangeAt(0).getBoundingClientRect();
    if (!r.width && !r.height) { bar.hidden = true; return; }
    bar.hidden = false;
    bar.style.top = (window.scrollY + r.top - bar.offsetHeight - 8) + "px";
    bar.style.left = (window.scrollX + r.left) + "px";
  }
  document.addEventListener("selectionchange", function () { window.setTimeout(placeBar, 0); });
  document.addEventListener("scroll", function () { if (!bar.hidden) placeBar(); }, true);

  bar.addEventListener("mousedown", function (e) { e.preventDefault(); });
  bar.addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    if (b.dataset.hl) add(b.dataset.hl, "");
    else if (b.dataset.act === "note") add("y", "");
    bar.hidden = true;
    if (b.dataset.act === "note") {
      var last = rail.lastElementChild;
      if (last) { var t = last.querySelector("textarea"); if (t) { t.rows = 3; t.focus(); } }
    }
  });

  /* ── 내보내기 — 브라우저에 갇히지 않게 ──────────────────────────────── */
  var exp = document.getElementById("annot-export");
  if (exp) exp.addEventListener("click", function () {
    var list = load();
    if (!list.length) { alert("이 문서에는 아직 메모·하이라이트가 없다."); return; }
    var slug = reader.getAttribute("data-annot");
    var out = ["# 메모 · 하이라이트 — " + slug, "",
               "이 파일은 **브라우저에 있던 개인 주석**을 내보낸 것이다. 위키의 내용이",
               "아니며, 인용의 근거가 아니다. 정본은 언제나 저장소의 원문이다.", ""];
    list.forEach(function (a, i) {
      out.push("## " + (i + 1) + ". " + (HUES[a.hue] || a.hue)
               + (a.sec ? "  (절: `#" + a.sec + "`)" : "")
               + (a.stale ? "  ⚠ 본문에서 못 찾음" : ""));
      out.push("");
      a.text.split("\n").forEach(function (l) { out.push("> " + l); });
      out.push("");
      if (a.note) { out.push(a.note, ""); }
      out.push("— " + (a.made || ""), "");
    });
    var blob = new Blob([out.join("\n")], { type: "text/markdown;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url; a.download = slug + ".notes.md";
    document.body.appendChild(a); a.click(); a.remove();
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  });

  /* ── 메모 모아보기에서 넘어온 경우 — `?note=<id>` 로 그 자리를 연다 ────
     모아보기 카드가 "적어 둔 그 자리로 간다" 고 약속하므로 여기서 지켜야 한다.
     하이라이트가 본문에서 안 찾아진 고아면 **오른쪽 목록 쪽으로** 데려간다 —
     아무 데도 안 가고 조용히 실패하면 링크가 깨진 것처럼 보인다. */
  function focusRequested() {
    var m = /[?&]note=([^&#]+)/.exec(location.search);
    if (!m) return;
    var id;
    try { id = decodeURIComponent(m[1]); } catch (e) { id = m[1]; }
    var el = body.querySelector('mark[data-annot-id="' + id + '"]')
          || rail.querySelector('[data-annot-id="' + id + '"]');
    if (!el) return;
    el.scrollIntoView({ block: "center" });
    el.classList.add("is-focus");
    window.setTimeout(function () { el.classList.remove("is-focus"); }, 2600);
  }

  render();
  focusRequested();
})();

/* ══ 사이드바 배지 — 어느 화면에서든 "메모가 몇 건인지" ════════════════
   메모 화면에 들어가야만 개수를 아는 것은 불편하다. 0이면 숨긴다 (0을 띄우면
   눈에 걸리기만 한다). 저장 접근이 막힌 브라우저면 조용히 아무것도 안 한다. */
(function () {
  var badge = document.getElementById("nav-note-n");
  if (!badge) return;
  var n = 0;
  try {
    for (var i = 0; i < localStorage.length; i++) {
      var k = localStorage.key(i);
      if (!k || k.indexOf("bms.annot.") !== 0) continue;
      var l = JSON.parse(localStorage.getItem(k) || "[]");
      if (Array.isArray(l)) n += l.length;
    }
  } catch (e) { return; }
  if (n > 0) { badge.textContent = String(n); badge.hidden = false; }
})();
