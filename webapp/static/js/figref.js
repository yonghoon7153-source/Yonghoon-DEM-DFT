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

  /* 확대·축소 -----------------------------------------------------------
   * 가로로 긴 그림(Table S5 등)은 max-width:100% 때문에 팝업 폭에 맞춰 줄어들어
   * 글씨를 못 읽는다 (2026-08-06 1저자 신고: "확대시 옆에도 스크롤이 생기게").
   * '맞춤'을 벗어나면 이미지를 **원본 픽셀 기준**으로 키우고 max-width 를 풀어서
   * 컨테이너(.figpane-img, overflow:auto)에 가로·세로 스크롤이 생기게 한다.
   * 팝업·라이트박스가 같은 컨트롤을 쓴다 (host 만 다르다). */
  var ZSTEP = 1.25, ZMIN = 0.15, ZMAX = 8;

  function zoomBtns() {
    return '<span class="figzoom-ctl">' +
      '<button type="button" class="btn sm figz" data-z="-" title="축소 (Ctrl+휠)">−</button>' +
      '<button type="button" class="btn sm figz figz-lab" data-z="0"' +
      ' title="맞춤 ⇄ 원본 크기 (그림 더블클릭도 같음)">맞춤</button>' +
      '<button type="button" class="btn sm figz" data-z="+" title="확대 (Ctrl+휠)">+</button></span>';
  }

  function Zoom(host, onZoom) {
    var z = 0;                       // 0 = 맞춤(폭에 맞춤) · 그 외 = 원본 대비 배율
    function img() { return host.querySelector(".figpane-img img"); }
    function paint() {
      var lab = host.querySelector(".figz-lab");
      if (lab) lab.textContent = z ? Math.round(z * 100) + "%" : "맞춤";
      if (onZoom) onZoom(z);                         // 컨테이너 높이 고정 등 (팝업)
      host.classList.toggle("figzoom", !!z);
      var im = img();
      if (!im) return;
      if (!z) { im.style.width = ""; return; }
      im.style.width = im.naturalWidth
        ? Math.round(im.naturalWidth * z) + "px"     // 원본 해상도 기준
        : Math.round(z * 100) + "%";                 // 아직 안 불러왔으면 임시로
    }
    function set(v) { z = v ? Math.max(ZMIN, Math.min(ZMAX, v)) : 0; paint(); }
    function bump(dir) {                             // 맞춤에서 누르면 '지금 보이는 크기'부터
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
      e.preventDefault();
      bump(e.deltaY < 0 ? 1 : -1);
    }, { passive: false });
    return {
      bind: function (reset) {          // innerHTML 을 다시 그린 뒤 호출
        if (reset) z = 0;
        var im = img();
        if (im) im.addEventListener("load", paint);   // 원본 크기는 로드 뒤에야 안다
        paint();
      }
    };
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
    // 사용자가 직접 옮기거나 크기를 바꾸면 그 값을 기억하고 자동배치를 멈춘다 (1저자 요청)
    var userPos = null, userSize = null;
    el.addEventListener("mouseenter", function () { over = true; clearTimeout(hideT); });
    el.addEventListener("mouseleave", function () { over = false; if (!pinned) hide(80); });

    /* 여백이 넓으면 팝업도 넓게 — 380 px 고정이면 다패널 그림이 안 읽힌다(1저자 지적).
       오른쪽/왼쪽 중 넓은 쪽을 골라 그 폭에 맞춘다. 둘 다 좁으면 본문 위에 겹쳐 띄운다. */
    function clampIn(x, y, w, h) {          // 화면 밖으로 못 나가게 (제목줄은 항상 잡히게)
      return [Math.max(8 - w + 90, Math.min(x, window.innerWidth - 90)),
              Math.max(8, Math.min(y, window.innerHeight - 44))];
    }

    function place(anchor) {
      if (userSize) {
        // 사용자가 키운 크기는 max-height 상한(90vh)에 막히면 안 된다 — 상한을 푼다
        el.style.maxHeight = "none";
        el.style.width = userSize[0] + "px";
        el.style.height = userSize[1] + "px";
      }
      if (userPos) {                        // 사용자가 옮겨 놓은 자리를 지킨다
        var c = clampIn(userPos[0], userPos[1], el.offsetWidth, el.offsetHeight);
        el.style.left = c[0] + "px"; el.style.top = c[1] + "px";
        return;
      }
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

    /* 제목줄을 잡아 끌면 이동 — 끄는 순간 자동으로 고정(pin)된다.
       버튼(↗ 크게 · ⬇ · ✕) 위에서 시작한 건 무시. 제목줄 더블클릭 = 원래 자리로. */
    el.addEventListener("pointerdown", function (e) {
      var bar = e.target.closest && e.target.closest(".figpane-bar");
      if (!bar || (e.target.closest && e.target.closest("a,button"))) return;
      e.preventDefault();
      var r = el.getBoundingClientRect();
      var dx = e.clientX - r.left, dy = e.clientY - r.top;
      pinned = pinned || "__drag";          // 끌기 시작하면 사라지지 않게
      el.classList.add("figpane-dragging");
      // ⚠ 이동/종료는 **window** 에 건다. 바(bar)에만 걸면 포인터가 바 밖으로 나간 채
      //   놓였을 때 up 을 못 받아 figpane-dragging 이 남고, 그 클래스의 pointer-events:none
      //   때문에 그림이 스크롤조차 안 된다 (2026-08-06 1저자 신고).
      function mv(ev) {
        var c = clampIn(ev.clientX - dx, ev.clientY - dy, r.width, r.height);
        userPos = c;
        el.style.left = c[0] + "px"; el.style.top = c[1] + "px";
      }
      function up() {
        window.removeEventListener("pointermove", mv);
        window.removeEventListener("pointerup", up);
        window.removeEventListener("pointercancel", up);
        el.classList.remove("figpane-dragging");
      }
      window.addEventListener("pointermove", mv);
      window.addEventListener("pointerup", up);
      window.addEventListener("pointercancel", up);
    });
    el.addEventListener("dblclick", function (e) {
      if (!(e.target.closest && e.target.closest(".figpane-bar"))) return;
      userPos = userSize = null;            // 자동배치로 되돌리기
      el.style.height = ""; el.style.maxHeight = "";
      place(null);
    });
    // CSS resize 로 크기를 바꾸면 기억한다
    if (window.ResizeObserver) {
      new ResizeObserver(function () {
        if (el.style.display === "none") return;
        var r = el.getBoundingClientRect();
        if (userSize || el.style.height) userSize = [Math.round(r.width), Math.round(r.height)];
        // 내용이 뒤늦게 늘어(코멘트가 fetch 후에 그려진다) 화면 밖으로 나가면 위로 당긴다
        if (r.bottom > window.innerHeight - 8) {
          var t = Math.max(8, window.innerHeight - 8 - r.height);
          el.style.top = t + "px";
          if (userPos) userPos = [userPos[0], t];
        }
      }).observe(el);
      el.addEventListener("pointerup", function () {   // 리사이즈 핸들을 놓은 순간부터 기억
        var r = el.getBoundingClientRect();
        userSize = [Math.round(r.width), Math.round(r.height)];
      });
    }

    /* 확대하면 팝업 높이를 '지금 높이'로 못 박는다.
       .figpane-img 는 flex:1 1 auto 라 높이가 내용만큼 늘어나는데, 부모는 max-height 로
       잘리기만 해서(overflow:hidden) **세로 스크롤이 안 생기고 잘려 나갔다**.
       부모 높이가 확정되면 그 안에서 shrink → overflow:auto 가 살아난다.
       CSS resize 로 사용자가 이미 크기를 잡아 뒀으면(el.style.height) 건드리지 않는다. */
    var zoomHeld = false;
    var zoom = Zoom(el, function (z) {
      if (z && !el.style.height) {
        el.style.height = el.offsetHeight + "px";
        el.style.maxHeight = "none";
        zoomHeld = true;
      } else if (!z && zoomHeld) {
        el.style.height = ""; el.style.maxHeight = ""; zoomHeld = false;
      }
    });
    var lastKey = null;

    function show(rec, anchor, pin) {
      if (pinned && !pin && pinned !== rec.key) return;
      clearTimeout(hideT);
      // 같은 그림을 다시 누르면 닫는다. ⚠ 예전엔 pinned=null 로만 두고 hide() 를 불렀는데,
      //   마우스가 팝업 안에 있어 over=true 라 숨김이 취소돼 안 닫혔다 (✕ 도 같은 이유).
      if (pin) {
        if (pinned === rec.key) {
          // digest 를 앞으로 보내 팝업이 가려진 상태라면 '닫기'가 아니라 '앞으로'
          if (global.winIsTop && !global.winIsTop(el)) { global.winFocus(el); return; }
          close(); return;
        }
        pinned = rec.key;
      }
      el.innerHTML =
        '<div class="figpane-bar"><b>' + esc(rec.title) + '</b>' +
        '<span class="figpane-act">' + zoomBtns() +
        '<a class="btn sm" href="/api/file/' + encodeURI(rec.rel) + '" target="_blank" rel="noopener">↗</a>' +
        '<a class="btn sm" href="/api/file/' + encodeURI(rec.rel) + '?dl=1" download>⬇</a>' +
        (pinned ? '<button type="button" class="btn sm figpane-x">✕</button>' : '') +
        '</span></div>' +
        '<div class="figpane-img"><img src="/api/file/' + encodeURI(rec.rel) + '" alt="' + esc(rec.title) + '"></div>' +
        '<div class="figpane-cap">' + capHtml(rec) + noteHtml(rec, true) + '</div>' +
        // 코멘트는 고정했을 때만 — 스쳐 지나가는 미리보기마다 fetch 하지 않는다
        (pinned ? '<div class="figpane-cmt"></div>' : '') +
        '<div class="figpane-hint">' +
        (pinned ? '제목줄 끌면 이동 · 모서리로 크기조절 · +/− 또는 Ctrl+휠로 확대(스크롤)'
                : '클릭하면 고정 · 본문에서 드래그로도 열려요') + '</div>';
      var x = el.querySelector(".figpane-x");
      if (x) x.onclick = function (ev) { ev.preventDefault(); ev.stopPropagation(); close(); };
      // 고정된 팝업만 '창'으로 친다 — 스쳐 지나가는 미리보기까지 모달 배경막을 걷으면 깜빡인다
      el.classList.toggle("figpane-pinned", !!pinned);
      if (pinned && global.mountComments)
        global.mountComments(el.querySelector(".figpane-cmt"), rec.rel);
      zoom.bind(rec.key !== lastKey);        // 다른 그림으로 바뀌면 배율은 맞춤부터
      lastKey = rec.key;
      // ⚠ "block" 이면 CSS 의 display:flex 를 덮어써서 .figpane-img 의 flex 축소가 죽는다
      //   → 그림이 팬 밖으로 자라 세로 스크롤 없이 잘려 나갔다 (2026-08-06)
      el.style.display = "flex";
      place(anchor);
      // 창 순서: 방금 연 팝업이 앞 + 모달을 '창 모드'로 (dragmodal.js)
      if (pin && global.winFocus) global.winFocus(el); else if (global.winSync) global.winSync();
    }
    function hide(ms) {
      clearTimeout(hideT);
      hideT = setTimeout(function () {
        if (!over && !pinned) { el.style.display = "none"; if (global.winSync) global.winSync(); }
      }, ms == null ? 160 : ms);
    }
    function close() { pinned = null; over = false; userPos = userSize = null; lastKey = null;
                       zoomHeld = false;
                       el.style.height = ""; el.style.maxHeight = "";
                       el.classList.remove("figpane-dragging");   // 혹시 남았으면 정리
                       el.classList.remove("figpane-pinned");
                       el.style.display = "none";
                       el.style.zIndex = "";                      // 창 순서 초기화
                       if (global.winSync) global.winSync(); }
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
        '<span class="cmt-badge" data-cbadge="' + esc(f.rel) + '"' +
        (f.comments ? '' : ' style="display:none"') + '>💬 ' + (f.comments || 0) + '</span>' +
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
      '<span style="display:flex;gap:6px;align-items:center">' + zoomBtns() +
      '<a class="btn sm" href="/api/file/' + encodeURI(f.rel) + '?dl=1" download>⬇ 저장</a>' +
      '<button type="button" class="btn sm" data-x>✕ 닫기</button></span></div>' +
      '<div style="padding:14px">' +
      '<div class="figpane-img figlb-img"><img src="/api/file/' +
      encodeURI(f.rel) + '" alt="' + esc(f.title) + '"></div>' +
      '<div class="figtext">' + capHtml(f) + noteHtml(f, false) + '</div>' +
      '<div class="figlb-cmt"></div></div></div>';
    m.querySelector("[data-x]").onclick = function () { m.classList.remove("open"); };
    Zoom(m.querySelector(".modal-body")).bind(true);
    if (global.mountComments) global.mountComments(m.querySelector(".figlb-cmt"), f.rel);
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

  // /literature 검색이 "몇 장에서 걸렸나"를 세도록 키 접두 + 구분자로 저장한다
  global.FIGSEP = "\u00a6";

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
    if (global.winSync) global.winSync();     // 남은 모달의 배경막 되돌리기
  };
})(window);
