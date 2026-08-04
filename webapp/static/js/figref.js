/* figref.js — digest 본문의 "Fig. 5e" 를 크로핑된 그림과 잇는다.
 *
 * 1저자 요청(2026-08-06): "논문 에이전트에서 fig.x 관련 언급이 있고 드래그를 그쪽 위에 하면
 *   옆에 팝업으로 보이게 / 밑에 파일로 쫙 있고 글이랑 링크해서 드래그하면 옆 여백에 figure 뜨게"
 *
 * 그림은 tools/litdb/extract_figures.py 가 PDF 캡션을 앵커로 잘라 litdb/figures/<slug>/ 에
 * 넣어둔 것. /api/paper/<pid> 응답의 figures 배열로 온다.
 *
 * 하는 일
 *   ① 본문 텍스트 노드를 훑어 Fig/Table/Scheme 참조를 <a class="figref"> 로 감싼다
 *      (코드·수식·기존 링크 안은 건드리지 않는다 — 파일명 `fig_3.png` 오염 방지)
 *   ② 마우스 올리기 / **드래그 선택** 둘 다에서 오른쪽 여백에 그림 팝업
 *   ③ 본문 끝에 그림 카드 목록 + 클릭하면 큰 창
 */
(function (global) {
  "use strict";

  // Fig. 5e / Figure 5(e) / Figs 2-3 / Table S3 / Scheme 1
  var RE = /\b(Fig(?:ures?|s)?\.?|FIGS?\.?|Tables?|Schemes?)\s*\.?\s*\(?(S?\d{1,3})\)?([a-z](?:\s*[–—,\-]\s*[a-z])*)?(?![\w.])/g;
  var SKIP = { CODE: 1, PRE: 1, A: 1, SCRIPT: 1, STYLE: 1, TEXTAREA: 1, BUTTON: 1 };
  var PANE_MIN = 340, PANE_MAX = 680;   // 여백 크기에 맞춰 이 사이에서 정해진다

  function keyOf(word, num) {
    var c = word.toLowerCase().charAt(0);
    return (c === "t" ? "t" : c === "s" ? "s" : "f") + num.toUpperCase();
  }

  var SRCLAB = { set: "Figure set", sec: "본문 절" };
  var BODY = null;                 // 링크화한 digest 본문 (점프 대상)

  /* 옵시디언식 점프 — 주석을 누르면 본문의 그 줄로 스크롤 + 잠깐 하이라이트.
   * 마크다운이 HTML 로 바뀌면 `**`·백틱이 사라지므로 서버가 평문 실마리(find)를 같이 준다.
   * 표는 칸마다 <td> 로 쪼개지므로 실마리도 한 칸 안에서만 떼어 왔다. */
  function norm(t) { return (t || "").replace(/[`*_~\s]+/g, " ").trim(); }

  function jumpTo(find, src) {
    if (!BODY || !find) return false;
    var needle = norm(find);
    if (needle.length < 4) return false;
    var pool = src === "sec"
      ? BODY.querySelectorAll("h1,h2,h3,h4,h5,h6")
      : BODY.querySelectorAll("td,th,li,p,h1,h2,h3,h4,h5,h6");
    var hit = null;
    for (var i = 0; i < pool.length && !hit; i++)
      if (norm(pool[i].textContent).indexOf(needle) !== -1) hit = pool[i];
    if (!hit) {                    // 실마리가 잘렸을 수 있으니 앞 20자로 한 번 더
      var short = needle.slice(0, 20);
      for (var j = 0; j < pool.length && !hit; j++)
        if (norm(pool[j].textContent).indexOf(short) !== -1) hit = pool[j];
    }
    if (!hit) return false;
    var row = hit.closest("tr") || hit;          // 표는 행 전체를 강조
    row.scrollIntoView({ behavior: "smooth", block: "center" });
    row.classList.remove("figjump");
    void row.offsetWidth;                        // 재생을 위해 리플로 강제
    row.classList.add("figjump");
    setTimeout(function () { row.classList.remove("figjump"); }, 2600);
    return true;
  }

  /* digest 주석 블록 — 논문 원문 캡션과 **구분해서** 보여준다 */
  function noteHtml(rec, compact) {
    if (!rec.notes || !rec.notes.length) return "";
    var list = compact ? rec.notes.slice(0, 1) : rec.notes;
    return '<div class="fignote"><div class="fignote-h">📝 우리 digest 정리</div>' +
      list.map(function (n, i) {
        var can = !!n.find;
        return '<div class="fignote-i' + (can ? " fignote-go" : "") + '"' +
          (can ? ' role="button" tabindex="0" title="본문의 이 줄로 이동"' +
                 ' data-find="' + esc(n.find) + '" data-src="' + esc(n.src) + '"' : "") +
          '><span class="fignote-src">' + esc(SRCLAB[n.src] || n.src) + "</span>" +
          esc(n.text) + (can ? ' <span class="fignote-jump">↩ 본문</span>' : "") + "</div>";
      }).join("") +
      (compact && rec.notes.length > 1
        ? '<div class="fignote-more">+' + (rec.notes.length - 1) + " 더 (클릭)</div>" : "") +
      "</div>";
  }

  function capHtml(rec) {
    if (!rec.caption) return "";
    return '<div class="figcap"><div class="figcap-h">📄 논문 캡션 (원문)</div>' +
      esc(rec.caption) + "</div>";
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  /* ① 본문 링크화 ------------------------------------------------------- */
  function linkify(root, index) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue || n.nodeValue.length < 4) return NodeFilter.FILTER_REJECT;
        for (var p = n.parentNode; p && p !== root; p = p.parentNode)
          if (SKIP[p.nodeName]) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var todo = [], n;
    while ((n = walker.nextNode())) if (RE.test(n.nodeValue)) { RE.lastIndex = 0; todo.push(n); }
    RE.lastIndex = 0;
    var hits = 0;
    todo.forEach(function (node) {
      var s = node.nodeValue, out = document.createDocumentFragment(), last = 0, m;
      RE.lastIndex = 0;
      while ((m = RE.exec(s))) {
        var k = keyOf(m[1], m[2]);
        if (!index[k]) continue;                      // 없는 그림은 링크 안 함
        if (m.index > last) out.appendChild(document.createTextNode(s.slice(last, m.index)));
        var a = document.createElement("a");
        a.className = "figref";
        a.setAttribute("data-fig", k);
        a.setAttribute("role", "button");
        a.setAttribute("tabindex", "0");
        a.textContent = m[0];
        out.appendChild(a);
        last = m.index + m[0].length;
        hits++;
      }
      if (!hits && last === 0) return;
      if (last === 0) return;
      if (last < s.length) out.appendChild(document.createTextNode(s.slice(last)));
      node.parentNode.replaceChild(out, node);
    });
    return hits;
  }

  /* ② 오른쪽 여백 팝업 --------------------------------------------------- */
  function Pane(container) {
    var el = document.createElement("div");
    el.className = "figpane";
    el.style.display = "none";
    document.body.appendChild(el);
    var pinned = null, hideT = null, over = false;
    el.addEventListener("mouseenter", function () { over = true; clearTimeout(hideT); });
    el.addEventListener("mouseleave", function () { over = false; if (!pinned) hide(80); });

    /* 여백이 넓으면 팝업도 넓게 — 380 px 고정이면 다패널 그림이 안 읽힌다(1저자 지적).
       오른쪽/왼쪽 중 넓은 쪽을 골라 그 폭에 맞춘다. 둘 다 좁으면 본문 위에 겹쳐 띄운다. */
    function place(anchor) {
      var box = container.getBoundingClientRect();
      var gapR = window.innerWidth - box.right - 26;
      var gapL = box.left - 26;
      var w = Math.max(PANE_MIN, Math.min(PANE_MAX, Math.max(gapR, gapL)));
      var left;
      if (gapR >= w) left = box.right + 14;              // 오른쪽 여백
      else if (gapL >= w) left = box.left - w - 14;       // 왼쪽 여백
      else {                                             // 둘 다 좁다 → 겹쳐서
        w = Math.max(PANE_MIN, Math.min(PANE_MAX, window.innerWidth - 40));
        left = Math.max(12, (window.innerWidth - w) / 2);
      }
      el.style.width = w + "px";
      el.style.left = left + "px";
      var ar = anchor ? anchor.getBoundingClientRect() : box;
      var h = el.offsetHeight || 400;
      el.style.top = Math.max(12, Math.min(ar.top - 40, window.innerHeight - h - 12)) + "px";
    }
    window.addEventListener("resize", function () {
      if (el.style.display !== "none") place(null);
    });

    function show(rec, anchor, pin) {
      if (pinned && !pin && pinned !== rec.key) return;
      clearTimeout(hideT);
      if (pin) pinned = pinned === rec.key ? null : rec.key;
      el.innerHTML =
        '<div class="figpane-bar"><b>' + esc(rec.title) + '</b>' +
        '<span class="figpane-act">' +
        '<a class="btn sm" href="/api/file/' + encodeURI(rec.rel) + '" target="_blank" rel="noopener">↗ 크게</a>' +
        '<a class="btn sm" href="/api/file/' + encodeURI(rec.rel) + '?dl=1" download>⬇</a>' +
        (pinned ? '<button type="button" class="btn sm figpane-x">✕</button>' : '') +
        '</span></div>' +
        '<div class="figpane-img"><img src="/api/file/' + encodeURI(rec.rel) + '" alt="' + esc(rec.title) + '"></div>' +
        '<div class="figpane-cap">' + capHtml(rec) + noteHtml(rec, true) + '</div>' +
        (pinned ? '' : '<div class="figpane-hint">클릭하면 고정 · 드래그로도 열려요</div>');
      var x = el.querySelector(".figpane-x");
      if (x) x.onclick = function () { pinned = null; hide(0); };
      el.style.display = "block";
      place(anchor);
    }
    function hide(ms) {
      clearTimeout(hideT);
      hideT = setTimeout(function () {
        if (!over && !pinned) el.style.display = "none";
      }, ms == null ? 160 : ms);
    }
    function close() { pinned = null; over = false; el.style.display = "none"; }
    return { show: show, hide: hide, close: close, el: el };
  }

  /* ③ 하단 그림 카드 ---------------------------------------------------- */
  function strip(figs, onOpen) {
    var wrap = document.createElement("div");
    wrap.className = "figstrip";
    var head = document.createElement("div");
    head.className = "figstrip-head";
    head.innerHTML = '📎 논문 그림 <span class="muted">' + figs.length +
      '개 · PDF 캡션 기준 자동 크로핑 · 본문의 Fig 언급에 마우스를 올리면 옆에 떠요</span>';
    wrap.appendChild(head);
    var grid = document.createElement("div");
    grid.className = "figstrip-grid";
    figs.forEach(function (f) {
      var c = document.createElement("button");
      c.type = "button";
      c.className = "figcard";
      c.setAttribute("data-fig", f.key);
      c.innerHTML =
        '<span class="figcard-thumb"><img loading="lazy" src="/api/file/' +
        encodeURI(f.rel) + '" alt="' + esc(f.title) + '"></span>' +
        '<span class="figcard-lab">' + esc(f.title) +
        (f.page ? ' <span class="muted">p' + f.page + '</span>' : '') + '</span>';
      c.onclick = function () { onOpen(f); };
      grid.appendChild(c);
    });
    wrap.appendChild(grid);
    return wrap;
  }

  /* 큰 창 (라이트박스) */
  function lightbox(f) {
    var m = document.getElementById("figlb");
    if (!m) {
      m = document.createElement("div");
      m.id = "figlb";
      m.className = "modal";
      m.onclick = function (e) { if (e.target === m) m.classList.remove("open"); };
      document.body.appendChild(m);
    }
    m.innerHTML =
      '<div class="modal-body" style="max-width:min(1100px,94vw)">' +
      '<div class="modal-head"><h3 style="font-size:.9rem;margin:0">' + esc(f.title) +
      (f.page ? ' <span class="muted">· p' + f.page + '</span>' : '') + '</h3>' +
      '<span style="display:flex;gap:6px">' +
      '<a class="btn sm" href="/api/file/' + encodeURI(f.rel) + '?dl=1" download>⬇ 저장</a>' +
      '<button type="button" class="btn sm" data-x>✕ 닫기</button></span></div>' +
      '<div style="padding:14px"><img style="max-width:100%;height:auto" src="/api/file/' +
      encodeURI(f.rel) + '" alt="' + esc(f.title) + '">' +
      '<div class="figtext">' + capHtml(f) + noteHtml(f, false) + '</div></div></div>';
    m.querySelector("[data-x]").onclick = function () { m.classList.remove("open"); };
    m.classList.add("open");
  }

  /* 조립 ---------------------------------------------------------------- */
  /* 주석 클릭 → 본문 점프 (팝업·라이트박스 어디서든) */
  document.addEventListener("click", function (e) {
    var g = e.target.closest && e.target.closest(".fignote-go");
    if (!g) return;
    e.preventDefault();
    e.stopPropagation();
    var lb = document.getElementById("figlb");
    var ok = jumpTo(g.dataset.find, g.dataset.src);
    if (ok && lb) lb.classList.remove("open");     // 큰 창은 닫아야 본문이 보인다
    if (!ok) g.classList.add("fignote-miss");
  }, true);
  document.addEventListener("keydown", function (e) {
    var g = e.target.closest && e.target.closest(".fignote-go");
    if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); g.click(); }
  });

  global.figrefAttach = function (bodyEl, figs, container) {
    BODY = bodyEl;
    if (!bodyEl) return 0;
    var old = document.querySelector(".figpane");
    if (old) old.remove();
    if (!figs || !figs.length) return 0;

    var index = {};
    figs.forEach(function (f) {
      f.title = (f.kind === "table" ? "Table " : f.kind === "scheme" ? "Scheme " : "Fig. ") + f.label;
      index[f.key] = f;
    });
    var n = linkify(bodyEl, index);
    var pane = Pane(container || bodyEl);

    bodyEl.addEventListener("mouseover", function (e) {
      var a = e.target.closest ? e.target.closest(".figref") : null;
      if (a && index[a.dataset.fig]) pane.show(index[a.dataset.fig], a, false);
    });
    bodyEl.addEventListener("mouseout", function (e) {
      if (e.target.closest && e.target.closest(".figref")) pane.hide();
    });
    bodyEl.addEventListener("click", function (e) {
      var a = e.target.closest ? e.target.closest(".figref") : null;
      if (a && index[a.dataset.fig]) { e.preventDefault(); pane.show(index[a.dataset.fig], a, true); }
    });
    bodyEl.addEventListener("keydown", function (e) {
      var a = e.target.closest ? e.target.closest(".figref") : null;
      if (a && index[a.dataset.fig] && (e.key === "Enter" || e.key === " ")) {
        e.preventDefault(); pane.show(index[a.dataset.fig], a, true);
      }
    });
    // 드래그(선택)로도 — 선택한 글자 안에 Fig 참조가 있으면 그 그림을 띄운다
    bodyEl.addEventListener("mouseup", function () {
      var sel = window.getSelection();
      if (!sel || sel.isCollapsed) return;
      var t = String(sel).slice(0, 120);
      RE.lastIndex = 0;
      var m = RE.exec(t);
      if (!m) return;
      var rec = index[keyOf(m[1], m[2])];
      if (!rec) return;
      var r = sel.getRangeAt(0);
      pane.show(rec, { getBoundingClientRect: function () { return r.getBoundingClientRect(); } }, true);
    });

    bodyEl.appendChild(strip(figs, lightbox));
    return n;
  };
  global.figrefClose = function () {
    var p = document.querySelector(".figpane");
    if (p) p.remove();
    var m = document.getElementById("figlb");
    if (m) m.classList.remove("open");
  };
})(window);
