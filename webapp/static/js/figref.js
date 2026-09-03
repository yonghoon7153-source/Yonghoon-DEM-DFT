/* figref.js — digest 본문의 "Fig. 3" · "Table S1" 을 크로핑된 그림과 잇는다.
 *
 * 원본: 다른 브랜치(argyrodite DFT) webapp/static/js/figref.js 의 이식판.
 * 우리 digest 도 `[인쇄]`/`[도표]` 표기를 쓰면서 본문에서 Fig. N 을 그대로 부르므로
 * 이 패턴은 도메인을 갈아도 그대로 유효하다.
 *
 * 가져온 것
 *   ① 본문 텍스트 노드를 훑어 Fig/Table/Scheme 참조를 <a class="figref"> 로 감싼다.
 *      코드·기존 링크 안은 건드리지 않는다 — 파일명 `fig_3.png` 오염 방지.
 *   ② 마우스 올리기 / 드래그 선택 둘 다에서 옆 여백에 그림 팝업, 클릭하면 고정.
 *   ③ 본문 끝 그림 카드 목록 + 클릭하면 큰 창(라이트박스).
 *   ④ 확대/축소 — 가로로 긴 표 그림은 폭에 맞추면 글씨를 못 읽는다.
 * 버린 것 (우리 쪽에 대응물이 없거나 읽기 전용 원칙에 어긋난다)
 *   · 그림 코멘트 저장(mountComments) — 쓰기다. 이 앱은 아무것도 저장하지 않는다.
 *   · digest 주석 → 본문 점프(fignote/jumpTo) — 우리 figures.json 에는 주석 필드가 없다.
 *   · 팝업 드래그 이동/창 순서(dragmodal 연동) — 창이 하나뿐이라 필요가 없다.
 */
(function () {
  "use strict";

  // Fig. 5e / Figure 5(e) / Figs 2-3 / Table S3 / Scheme 1
  var RE = /\b(Fig(?:ures?|s)?\.?|FIGS?\.?|Tables?|Schemes?)\s*\.?\s*\(?(S?\d{1,3})\)?([a-z](?:\s*[–—,\-]\s*[a-z])*)?(?![\w.])/g;
  var SKIP = { CODE: 1, PRE: 1, A: 1, SCRIPT: 1, STYLE: 1, TEXTAREA: 1, BUTTON: 1 };
  var PANE_MIN = 340, PANE_MAX = 680;

  function keyOf(word, num) {
    var c = word.toLowerCase().charAt(0);
    return (c === "t" ? "t" : c === "s" ? "s" : "f") + num.toUpperCase();
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function url(rel, dl) { return "/api/file/" + encodeURI(rel) + (dl ? "?dl=1" : ""); }

  function capHtml(rec) {
    if (!rec.caption) return "";
    return '<div class="figcap"><div class="figcap-h">원문 캡션</div>' + esc(rec.caption) + "</div>";
  }

  /* 확대·축소 — '맞춤'을 벗어나면 **원본 픽셀 기준**으로 키우고 max-width 를 풀어서
     컨테이너(overflow:auto)에 스크롤이 생기게 한다. 표 그림은 이게 없으면 못 읽는다. */
  var ZSTEP = 1.25, ZMIN = 0.15, ZMAX = 8;

  function zoomBtns() {
    return '<span class="figzoom-ctl">' +
      '<button type="button" class="btn sm figz" data-z="-" title="축소 (Ctrl+휠)">−</button>' +
      '<button type="button" class="btn sm figz figz-lab" data-z="0" title="맞춤 ⇄ 원본 (더블클릭도 같음)">맞춤</button>' +
      '<button type="button" class="btn sm figz" data-z="+" title="확대 (Ctrl+휠)">+</button></span>';
  }

  function Zoom(host, onZoom) {
    var z = 0;
    function img() { return host.querySelector(".figpane-img img"); }
    function paint() {
      var lab = host.querySelector(".figz-lab");
      if (lab) lab.textContent = z ? Math.round(z * 100) + "%" : "맞춤";
      if (onZoom) onZoom(z);
      host.classList.toggle("figzoom", !!z);
      var im = img();
      if (!im) return;
      if (!z) { im.style.width = ""; return; }
      im.style.width = im.naturalWidth ? Math.round(im.naturalWidth * z) + "px"
                                       : Math.round(z * 100) + "%";
    }
    function set(v) { z = v ? Math.max(ZMIN, Math.min(ZMAX, v)) : 0; paint(); }
    function bump(dir) {
      var im = img();
      var cur = z || (im && im.naturalWidth ? im.clientWidth / im.naturalWidth : 1);
      set(cur * (dir > 0 ? ZSTEP : 1 / ZSTEP));
    }
    host.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest(".figz");
      if (!b) return;
      e.preventDefault(); e.stopPropagation();
      var d = b.getAttribute("data-z");
      if (d === "+") bump(1); else if (d === "-") bump(-1); else set(z ? 0 : 1);
    });
    host.addEventListener("dblclick", function (e) {
      if (!(e.target.closest && e.target.closest(".figpane-img"))) return;
      e.preventDefault(); set(z ? 0 : 1);
    });
    host.addEventListener("wheel", function (e) {
      if (!(e.ctrlKey || e.metaKey)) return;
      if (!(e.target.closest && e.target.closest(".figpane-img"))) return;
      e.preventDefault(); bump(e.deltaY < 0 ? 1 : -1);
    }, { passive: false });
    return {
      bind: function (reset) {
        if (reset) z = 0;
        var im = img();
        if (im) im.addEventListener("load", paint);   // 원본 크기는 로드 뒤에야 안다
        paint();
      }
    };
  }

  /* ① 본문 링크화 */
  function linkify(root, index) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue || n.nodeValue.length < 4) return NodeFilter.FILTER_REJECT;
        for (var p = n.parentNode; p && p !== root; p = p.parentNode)
          if (SKIP[p.nodeName]) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var todo = [], n, hits = 0;
    while ((n = walker.nextNode())) if (RE.test(n.nodeValue)) { RE.lastIndex = 0; todo.push(n); }
    RE.lastIndex = 0;
    todo.forEach(function (node) {
      var s = node.nodeValue, out = document.createDocumentFragment(), last = 0, m;
      RE.lastIndex = 0;
      while ((m = RE.exec(s))) {
        var k = keyOf(m[1], m[2]);
        if (!index[k]) continue;                       // 없는 그림은 링크하지 않는다
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
      if (last === 0) return;
      if (last < s.length) out.appendChild(document.createTextNode(s.slice(last)));
      node.parentNode.replaceChild(out, node);
    });
    return hits;
  }

  /* ② 옆 여백 팝업 */
  function Pane(container) {
    var el = document.createElement("div");
    el.className = "figpane";
    el.style.display = "none";
    document.body.appendChild(el);
    var pinned = null, hideT = null, over = false, lastKey = null;
    el.addEventListener("mouseenter", function () { over = true; clearTimeout(hideT); });
    el.addEventListener("mouseleave", function () { over = false; if (!pinned) hide(80); });

    /* 여백이 넓으면 팝업도 넓게 — 고정 폭이면 다패널 그림이 안 읽힌다.
       오른쪽/왼쪽 중 넓은 쪽에 붙이고, 둘 다 좁으면 본문 위에 겹쳐 띄운다. */
    function place(anchor) {
      var box = container.getBoundingClientRect();
      var gapR = window.innerWidth - box.right - 26, gapL = box.left - 26;
      var w = Math.max(PANE_MIN, Math.min(PANE_MAX, Math.max(gapR, gapL))), left;
      if (gapR >= w) left = box.right + 14;
      else if (gapL >= w) left = box.left - w - 14;
      else { w = Math.max(PANE_MIN, Math.min(PANE_MAX, window.innerWidth - 40));
             left = Math.max(12, (window.innerWidth - w) / 2); }
      el.style.width = w + "px";
      el.style.left = left + "px";
      var ar = anchor ? anchor.getBoundingClientRect() : box;
      var h = el.offsetHeight || 400;
      el.style.top = Math.max(12, Math.min(ar.top - 40, window.innerHeight - h - 12)) + "px";
    }
    window.addEventListener("resize", function () { if (el.style.display !== "none") place(null); });

    /* 확대하면 팬 높이를 '지금 높이'로 못 박는다 — 안 그러면 .figpane-img 가 내용만큼
       자라서 세로 스크롤 없이 잘려 나간다 (원본에서 실측된 버그). */
    var held = false;
    var zoom = Zoom(el, function (z) {
      if (z && !el.style.height) { el.style.height = el.offsetHeight + "px"; el.style.maxHeight = "none"; held = true; }
      else if (!z && held) { el.style.height = ""; el.style.maxHeight = ""; held = false; }
    });

    function show(rec, anchor, pin) {
      if (pinned && !pin && pinned !== rec.key) return;
      clearTimeout(hideT);
      if (pin) {
        if (pinned === rec.key) { close(); return; }   // 같은 그림을 또 누르면 닫는다
        pinned = rec.key;
      }
      el.innerHTML =
        '<div class="figpane-bar"><b>' + esc(rec.title) + "</b>" +
        '<span class="figpane-act">' + zoomBtns() +
        '<a class="btn sm" href="' + url(rec.rel) + '" target="_blank" rel="noopener" title="새 탭">↗</a>' +
        (pinned ? '<button type="button" class="btn sm figpane-x" title="닫기">✕</button>' : "") +
        "</span></div>" +
        '<div class="figpane-img"><img src="' + url(rec.rel) + '" alt="' + esc(rec.title) + '"></div>' +
        '<div class="figpane-cap">' + capHtml(rec) +
        (rec.page ? '<div class="figpage">원문 p.' + esc(rec.page) + "</div>" : "") + "</div>" +
        (pinned ? "" : '<div class="figpane-hint">클릭하면 고정 · 본문에서 드래그로도 열려요</div>');
      var x = el.querySelector(".figpane-x");
      if (x) x.onclick = function (ev) { ev.preventDefault(); ev.stopPropagation(); close(); };
      el.classList.toggle("figpane-pinned", !!pinned);
      zoom.bind(rec.key !== lastKey);
      lastKey = rec.key;
      // ⚠ "block" 이면 CSS 의 display:flex 를 덮어써서 그림이 팬 밖으로 자란다
      el.style.display = "flex";
      place(anchor);
    }
    function hide(ms) {
      clearTimeout(hideT);
      hideT = setTimeout(function () {
        if (!over && !pinned) el.style.display = "none";
      }, ms == null ? 160 : ms);
    }
    function close() {
      pinned = null; over = false; lastKey = null; held = false;
      el.style.height = ""; el.style.maxHeight = "";
      el.classList.remove("figpane-pinned");
      el.style.display = "none";
    }
    return { show: show, hide: hide, close: close, el: el };
  }

  /* ③ 하단 그림 카드 */
  function strip(figs, onOpen) {
    var wrap = document.createElement("div");
    wrap.className = "figstrip";
    var head = document.createElement("div");
    head.className = "figstrip-head";
    head.innerHTML = "그림 · 표 <span class=\"muted\">" + figs.length +
      "장 · PDF 캡션을 앵커로 자동 크로핑 · 본문의 Fig 언급에 마우스를 올리면 옆에 떠요</span>";
    wrap.appendChild(head);
    var grid = document.createElement("div");
    grid.className = "figstrip-grid";
    figs.forEach(function (f) {
      var c = document.createElement("button");
      c.type = "button";
      c.className = "figcard";
      c.setAttribute("data-fig", f.key);
      c.innerHTML = '<span class="figcard-thumb"><img loading="lazy" src="' + url(f.rel) +
        '" alt="' + esc(f.title) + '"></span><span class="figcard-lab">' + esc(f.title) +
        (f.page ? ' <span class="muted">p' + esc(f.page) + "</span>" : "") + "</span>";
      c.onclick = function () { onOpen(f); };
      grid.appendChild(c);
    });
    wrap.appendChild(grid);
    return wrap;
  }

  /* 큰 창 */
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
      '<div class="modal-body">' +
      '<div class="modal-head"><h3>' + esc(f.title) +
      (f.page ? ' <span class="muted">· p' + esc(f.page) + "</span>" : "") + "</h3>" +
      '<span class="modal-act">' + zoomBtns() +
      '<a class="btn sm" href="' + url(f.rel, 1) + '" download>⬇ 저장</a>' +
      '<button type="button" class="btn sm" data-x>✕ 닫기</button></span></div>' +
      '<div class="modal-in"><div class="figpane-img figlb-img"><img src="' + url(f.rel) +
      '" alt="' + esc(f.title) + '"></div><div class="figtext">' + capHtml(f) + "</div></div></div>";
    m.querySelector("[data-x]").onclick = function () { m.classList.remove("open"); };
    Zoom(m.querySelector(".modal-body")).bind(true);
    m.classList.add("open");
  }

  /* 조립 */
  function attach(bodyEl, figs) {
    if (!bodyEl || !figs || !figs.length) return 0;
    var index = {};
    figs.forEach(function (f) { index[f.key] = f; });
    var n = linkify(bodyEl, index);
    var pane = Pane(bodyEl);

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
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      var lb = document.getElementById("figlb");
      if (lb && lb.classList.contains("open")) { lb.classList.remove("open"); return; }
      pane.close();
    });

    bodyEl.appendChild(strip(figs, lightbox));
    return n;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var host = document.getElementById("figdata");
    var body = document.getElementById("digest-body");
    if (!host || !body) return;
    var slug = host.getAttribute("data-slug");
    if (!slug) return;
    fetch("/api/figures/" + encodeURIComponent(slug) + ".json")
      .then(function (r) { return r.ok ? r.json() : { figures: [] }; })
      .then(function (d) { attach(body, d.figures || []); })
      .catch(function () { /* 그림이 없어도 digest 본문은 그대로 읽힌다 */ });
  });
})();
