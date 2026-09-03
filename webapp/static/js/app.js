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
