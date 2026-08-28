/* docnote.js — digest 본문에 **Word 식 여백 메모**.
 *
 * 1저자 요청(2026-08-17): "글 쪽 화면 오른쪽클릭하면 word에서 메모 남기는 것처럼
 * 옆에 적는게 생기게". 논문 digest 를 읽다가 든 판단("이건 우리 §20.3 오타 얘기",
 * "이 수치는 우리 db 랑 방법이 다름")을 **읽던 그 줄 옆에** 붙인다.
 *
 *   mountDocNotes(bodyEl, rel, hostEl)   — 본문에 메모 기능을 단다
 *   unmountDocNotes()                    — 모달 닫을 때 정리
 *
 * 저장은 **코멘트와 같은 창고**다 (/api/comments/<rel> → db/file_comments.json).
 * 새 저장소를 만들지 않는 이유: 검색 색인(paper_comment_search)·백업·락이 이미 거기
 * 붙어 있다. 여백 메모는 그 항목에 `anchor`(붙인 자리의 글) 가 있는 것뿐이다.
 *
 * 자리를 **글로** 잡는다 (좌표·문단번호가 아니라)
 *   digest 는 열 때마다 서버가 다시 렌더하고, 문서를 고치면 문단이 밀린다.
 *   글 지문으로 잡으면 문단이 밀려도 따라가고, 글이 아예 지워지면 "자리를 잃은 메모"
 *   로 위에 모아 둔다 — **지우지 않는다**. 메모를 잃는 게 자리를 잃는 것보다 나쁘다.
 *
 * 이 파일이 **못 하는 것**
 *   · 여러 문단에 걸친 선택을 형광펜으로 못 칠한다 (한 텍스트 노드 안일 때만).
 *     그 경우 문단 전체를 옅게 표시하고 메모에 고른 글을 인용해 둔다.
 *   · 같은 글이 문서에 여러 번 나오면 **첫 번째**에 붙는다 — 구분하지 못한다.
 *   · 그림에는 안 붙는다 (그림은 comments.js 의 💬 가 담당 — 두 벌로 갈리면 안 된다).
 *   · **붙인 자리(anchor)는 못 고친다.** 글만 고쳐진다 — 자리를 옮기려면 지우고 다시 단다.
 *     (자리를 고치면 딥링크·검색 색인이 가리키던 곳과 어긋난다.)
 *
 * 고치기 (2026-08-17 추가)
 *   글을 누르거나 ✎ 를 누르면 제자리에서 고친다. 옛 글은 **지우지 않고**
 *   서버가 item.history 에 쌓는다 — 이 글들은 판단 기록이라 "그때 뭐라고 봤더라" 가
 *   나중에 질문이 된다.
 */
(function (global) {
  "use strict";

  var BLOCKS = "p,li,h1,h2,h3,h4,h5,h6,blockquote,pre,td,th,figcaption";
  var cur = null;          // {body, rel, host, gut, notes, map, draft}

  /* ⛔⛔ 2026-08-28 — 글 서식(esc/inline/autosize/wrapSel)의 **집을 comments.js 로 옮겼다.**
   *   여기에만 있어서 문헌 코멘트는 `**87.2%**` 가 별표째 보였다(1저자 신고).
   *   comments.js 는 base.html 이 **모든 페이지**에 싣고 이 파일은 일부 페이지에만
   *   실리므로, 공용 규약은 저쪽이 집이다. 여기서는 **호출 시점에** 가져다 쓴다 —
   *   불러오는 순서를 가정하지 않으려고 (호출은 항상 DOM 준비 뒤다).
   *   ⚠ 사본을 다시 만들지 마라. 오늘만 "같은 규약의 두 경로" 를 세 번 고쳤다. */
  function NF() {
    if (!global.noteFmt) throw new Error("noteFmt 가 없다 — comments.js 가 안 실렸다");
    return global.noteFmt;
  }
  function esc(s) { return NF().esc(s); }
  function inline(s) { return NF().inline(s); }
  function autosize(ta) { return NF().autosize(ta); }
  function wrapSel(ta, mk) { return NF().wrapSel(ta, mk); }
  function norm(s) { return String(s == null ? "" : s).replace(/\s+/g, " ").trim(); }

  /* ── 본문 쪽: 형광펜 ───────────────────────────────────────────────────── */

  function blockList() {
    return [].slice.call(cur.body.querySelectorAll(BLOCKS)).filter(function (b) {
      // 그림 영역(figref)은 제외 — 거기는 💬 코멘트가 담당한다
      return !b.closest(".figstrip") && !b.closest(".figpane");
    });
  }

  /* 한 텍스트 노드 안에 통째로 들어 있을 때만 <mark> 로 감싼다.
   * ⚠ 노드를 걸치면 surroundContents 가 던진다 — 그때는 조용히 포기하고
   *   호출부가 문단 표시로 넘어간다 (예외를 삼키지 말고 null 로 알린다). */
  function wrapFirst(block, needle, cls, minLen) {
    if (!needle || needle.length < (minLen == null ? 4 : minLen)) return null;
    var w = document.createTreeWalker(block, NodeFilter.SHOW_TEXT, null), n;
    while ((n = w.nextNode())) {
      if (n.parentNode && n.parentNode.closest &&
          n.parentNode.closest("mark.dn-hl,mark.dn-pen")) continue;
      var i = n.nodeValue.indexOf(needle);
      if (i < 0) continue;
      var r = document.createRange();
      r.setStart(n, i); r.setEnd(n, i + needle.length);
      var mk = document.createElement("mark");
      mk.className = cls || "dn-hl";
      try { r.surroundContents(mk); } catch (_) { return null; }
      return mk;
    }
    return null;
  }

  function clearHl() {
    if (!cur) return;
    cur.body.querySelectorAll("mark.dn-hl,mark.dn-pen").forEach(function (m) {
      var p = m.parentNode;
      while (m.firstChild) p.insertBefore(m.firstChild, m);
      p.removeChild(m);
      if (p.normalize) p.normalize();
    });
    cur.body.querySelectorAll(".dn-anch").forEach(function (b) {
      b.classList.remove("dn-anch");
    });
  }

  /* 메모 하나의 자리를 찾는다 — ① 글 그대로 → ② 문단 앞머리 → ③ 문단 어디든 */
  function findAnchor(a) {
    if (!a) return null;
    var blocks = blockList(), i;
    for (i = 0; i < blocks.length; i++) {
      var mk = wrapFirst(blocks[i], a);
      if (mk) return mk;
    }
    for (i = 0; i < blocks.length; i++) {
      if (norm(blocks[i].textContent).indexOf(a) === 0) {
        blocks[i].classList.add("dn-anch"); return blocks[i];
      }
    }
    for (i = 0; i < blocks.length; i++) {
      if (norm(blocks[i].textContent).indexOf(a) >= 0) {
        blocks[i].classList.add("dn-anch"); return blocks[i];
      }
    }
    return null;
  }

  /* ── 여백 쪽: 카드 ─────────────────────────────────────────────────────── */

  function cardHtml(nt, lost) {
    var nh = (nt.history || []).length;
    return '<div class="dn-card' + (lost ? " dn-lost" : "") + '" data-nid="' + esc(nt.id) + '">' +
      '<div class="dn-meta">' + (lost ? '<span class="dn-lostmark" title="붙여 둔 글을 본문에서 못 찾았어요 — 문서가 바뀐 듯해요">⚠ 자리 잃음</span> ' : "") +
      esc(nt.at) + (nt.who ? " · " + esc(nt.who) : "") +
      (nt.edited_at ? ' <span class="dn-edited" title="' + esc(nt.edited_at) + ' 에 고침'
        + (nh ? " · 옛 글 " + nh + "판 보관" : "") + '">✎ 수정됨</span>' : "") +
      '<button type="button" class="dn-edit" title="고치기">✎</button>' +
      '<button type="button" class="dn-del" title="지우기">✕</button></div>' +
      (nt.anchor ? '<div class="dn-quote">' + esc(nt.anchor) + "</div>" : "") +
      '<div class="dn-text" title="눌러서 고치기">' + inline(nt.text) + "</div></div>";
  }

  /* ── 고치기 (제자리) ───────────────────────────────────────────────────── */

  function editing() { return cur && cur.gut && cur.gut.querySelector(".dn-card.dn-editing"); }

  function openEdit(card) {
    if (!card || card.classList.contains("dn-editing")) return;
    closeEdit();
    var box = card.querySelector(".dn-text");
    if (!box) return;
    card.classList.add("dn-editing");
    card._old = box.innerHTML;
    var nt = (cur.notes || []).filter(function (n) { return n.id === card.dataset.nid; })[0];
    box.innerHTML = '<textarea class="dn-in" rows="3"></textarea>' +
      '<div class="dn-act"><button type="button" class="btn sm dn-editcancel">취소</button>' +
      '<button type="button" class="btn sm dn-save">저장</button></div>';
    var ta = box.querySelector(".dn-in");
    ta.value = nt ? nt.text : "";
    autosize(ta);
    layout();
    ta.focus();
    ta.setSelectionRange(ta.value.length, ta.value.length);
  }

  function closeEdit() {
    var card = editing();
    if (!card) return;
    var box = card.querySelector(".dn-text");
    if (box && card._old != null) box.innerHTML = card._old;
    card.classList.remove("dn-editing");
    card._old = null;
    layout();
  }

  function patch(nid, text) {
    if (!norm(text)) return;
    fetch("/api/comments/" + encodeURI(cur.rel), {
      method: "PATCH", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: nid, text: text })
    }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (x) {
        if (!x.ok) { alert("⛔ " + (x.d.error || "저장 실패")); return; }
        if (global.syncPaperCmtIndex) global.syncPaperCmtIndex(x.d);
        load();
      })
      .catch(function () { alert("⛔ 통신 실패"); });
  }

  function render() {
    var lost = [], ok = [];
    clearHl();                 // ⚠ 형광펜도 같이 벗겨진다 — 바로 아래에서 다시 칠한다
    paintPens();
    cur.map = {};
    cur.notes.forEach(function (nt) {
      var el = findAnchor(nt.anchor || "");
      if (el) { cur.map[nt.id] = el; ok.push(nt); } else { lost.push(nt); }
    });
    cur.gut.innerHTML =
      '<div class="dn-h">📝 메모 <span class="muted">' + cur.notes.length + "</span>" +
      '<span class="dn-hint">본문에서 오른쪽 클릭</span></div>' +
      lost.map(function (n) { return cardHtml(n, true); }).join("") +
      ok.map(function (n) { return cardHtml(n, false); }).join("");
    paintBadge();
    layout();
  }

  /* 카드를 자기 자리 높이에 맞춰 세로로 놓는다. 겹치면 아래로 민다 (Word 와 같다).
   * ⚠ 카드는 gut 안에서 absolute — gut 과 본문이 **같은 스크롤 상자** 안에 있어야
   *   rect 차이가 스크롤과 무관해진다. .modal-body 가 그 상자다. */
  function layout() {
    if (!cur || !cur.gut) return;
    var head = cur.gut.querySelector(".dn-h");
    var gr = cur.gut.getBoundingClientRect();
    var cards = [].slice.call(cur.gut.querySelectorAll(".dn-card,.dn-draft"));
    /* ⚠ katex·mermaid·figref 는 mount 뒤에도 본문 조각을 **갈아끼운다**. 그러면 우리가
     *   잡아 둔 자리 원소가 문서에서 떨어져 나가고, 카드가 전부 맨 위로 몰린다
     *   (붙인 자리를 잃은 것처럼 보인다). 떨어진 걸 발견하면 자리를 다시 찾는다. */
    var stale = false;
    var rows = cards.map(function (c) {
      var el = c.dataset.nid ? cur.map[c.dataset.nid] : cur.draftEl;
      if (el && !document.contains(el)) { stale = true; el = null; }
      var t = el ? el.getBoundingClientRect().top - gr.top : 0;
      return { c: c, t: t };
    });
    // ⚠ 고치는 중에는 다시 그리지 않는다 — render() 가 여백을 통째로 새로 그려서
    //   쓰던 글이 날아간다. 자리 찾기는 저장/취소 뒤로 미룬다.
    if (stale && !cur._refind && !editing()) {   // render() → layout() 되돌이 빗장
      cur._refind = true;
      setTimeout(function () { if (cur) { cur._refind = false; render(); } }, 0);
      return;
    }
    rows.sort(function (a, b) { return a.t - b.t; });

    /* ⛔ 2026-08-28 (1저자: "중복된 층에서는 1열, 2열 느낌으로 나눠서") —
     *   예전에는 카드가 겹치면 **무조건 아래로 밀었다.** 그러면 본문의 그 줄과
     *   나란히 있어야 할 카드가 한참 아래로 내려가 **어느 줄 메모인지 알 수 없어졌다.**
     *   이제 자기 자리에 못 놓으면 **옆 열로** 간다. 아래로 미는 건 두 열이 다 찼을 때만.
     *
     *   그리고 폭은 **필요할 때만** 반으로 준다: 옆 열 카드와 세로로 겹치는 카드만
     *   좁아지고, 혼자 있는 메모는 여백 통폭을 다 쓴다 (그림 첨부가 답답하지 않게).
     *
     * ⛔ 못 하는 것
     *   · 3열 이상은 안 만든다. 여백이 그만큼 넓지 않고, 열이 늘수록 "어느 줄 메모인가"가
     *     오히려 흐려진다.
     *   · 좁은 화면(폭 < MIN_2COL)에서는 그냥 1열로 민다 — 반으로 가르면 글이 안 읽힌다.
     */
    var PAD = 10, GAP = 8, MIN_2COL = 360, OVER = 300;   // OVER = 고칠 때 본문 위로 넘는 폭
    var W = cur.gut.clientWidth || 0;
    var nCol = W >= MIN_2COL ? 2 : 1;
    var fullW = W - PAD * 2;
    var colW = Math.floor((fullW - GAP * (nCol - 1)) / nCol);
    var top0 = head ? head.offsetHeight + 6 : 0;

    function isEd(c) {
      return c.classList.contains("dn-editing") || c.classList.contains("dn-draft");
    }
    function setW(c, w, left) {
      c.style.right = "auto";
      c.style.left = left + "px";
      c.style.width = w + "px";
    }

    /* ⛔⛔ 순서가 중요하다 (2026-08-28 브라우저 테스트가 잡았다) — 폭을 바꾸면 글이
     *   접혀 **높이가 달라진다.** 첫 판은 통폭에서 잰 높이로 배치해 놓고 반폭을 입혀서
     *   카드 두 쌍이 겹쳤다. ⇒ ① 폭을 정하고 ② 다시 재고 ③ 그 다음 자리를 잡는다. */

    // ① 반폭으로 한 번 재서 "이 카드가 다음 카드와 부딪히나" 를 본다
    if (nCol > 1) {
      rows.forEach(function (r) { if (!isEd(r.c)) setW(r.c, colW, PAD); });
    }
    var hHalf = rows.map(function (r) { return r.c.offsetHeight; });
    var half = rows.map(function () { return false; });
    if (nCol > 1) {
      for (var i = 0; i < rows.length - 1; i++) {
        if (rows[i + 1].t < rows[i].t + hHalf[i] + GAP) { half[i] = true; half[i + 1] = true; }
      }
    }

    // ② 정해진 폭을 입히고 **다시 잰다**
    rows.forEach(function (r, i) {
      if (isEd(r.c) && nCol > 1) setW(r.c, fullW + OVER, PAD - OVER);
      else setW(r.c, half[i] ? colW : fullW, PAD);
      r.c.classList.toggle("dn-half", half[i] && !isEd(r.c));
    });
    var hh = rows.map(function (r) { return r.c.offsetHeight; });

    // ③ 자리 잡기. **통폭 카드는 두 열을 다 막는다** — 안 그러면 옆 열 카드가 겹친다.
    var bottom = [];
    for (var z0 = 0; z0 < nCol; z0++) bottom.push(top0);
    rows.forEach(function (r, i) {
      var t, k = 0;
      if (!half[i]) {                       // 통폭 — 모든 열이 비어야 놓는다
        t = r.t;
        for (var q = 0; q < nCol; q++) if (bottom[q] > t) t = bottom[q];
        for (var q2 = 0; q2 < nCol; q2++) bottom[q2] = t + hh[i] + GAP;
      } else {
        k = -1;
        for (var j = 0; j < nCol; j++) if (r.t >= bottom[j]) { k = j; break; }
        if (k < 0) {                        // 두 열 다 찼다 → 먼저 비는 열로 민다
          k = 0;
          for (var m = 1; m < nCol; m++) if (bottom[m] < bottom[k]) k = m;
        }
        t = Math.max(r.t, bottom[k]);
        bottom[k] = t + hh[i] + GAP;
        r.c.style.left = (PAD + k * (colW + GAP)) + "px";
      }
      r.c.style.top = t + "px";
    });

    var deep = top0;
    for (var z = 0; z < bottom.length; z++) if (bottom[z] > deep) deep = bottom[z];
    cur.gut.style.minHeight = (deep + 24) + "px";
  }

  /* 카드·본문 자리로 데려가고 잠깐 반짝인다. /notes 목록에서 넘어올 때 쓴다. */
  function focusNote(nid) {
    if (!cur) return false;
    var card = cur.gut.querySelector('.dn-card[data-nid="' + nid.replace(/"/g, '\\"') + '"]');
    if (!card) return false;
    card.classList.add("dn-focus");
    var el = cur.map[nid];
    (el || card).scrollIntoView({ block: "center", behavior: "smooth" });
    if (el) {
      el.classList.add("dn-flash");
      setTimeout(function () { el.classList.remove("dn-flash"); }, 2000);
    }
    setTimeout(function () { card.classList.remove("dn-focus"); }, 3000);
    return true;
  }

  /* ?note=<id> 로 들어오면 그 메모로. **한 번만** 먹는다 — 메모를 새로 달아
   * load() 가 다시 돌 때마다 화면이 끌려가면 글을 못 쓴다. */
  function focusFromUrl() {
    if (!cur || cur._urlDone) return;
    var nid = new URLSearchParams(location.search).get("note");
    if (!nid) { cur._urlDone = true; return; }
    if (focusNote(nid)) cur._urlDone = true;
  }

  global.focusDocNote = focusNote;

  function paintBadge() {
    var b = document.getElementById("pnotebadge");
    if (!b) return;
    var n = cur ? cur.notes.length : 0;
    b.textContent = n ? "📝 메모 " + n : "";
    b.title = n ? n + "건 — 본문 오른쪽 클릭으로 더 답니다" : "";
  }

  /* ── 서버 ──────────────────────────────────────────────────────────────── */

  function load() {
    fetch("/api/comments/" + encodeURI(cur.rel))
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!cur) return;
        cur.notes = (d.items || []);
        render();
        if (global.syncPaperCmtIndex) global.syncPaperCmtIndex(d);
        focusFromUrl();
      })
      .catch(function () {
        if (cur) cur.gut.innerHTML = '<div class="dn-h">📝 메모</div>' +
          '<div class="muted" style="font-size:.74rem;padding:0 10px">못 불러왔어요</div>';
      });
  }

  /* ── 형광펜 (2026-08-27) ────────────────────────────────────────────────
   * 메모와 **저장소가 다르다**(/api/highlights). 자리 잡는 방식은 같다 — 글 지문.
   * ⛔ 못 하는 것: 한 문단에 같은 글이 여러 번이면 첫 번째만 · 문단을 가로지르는
   *   선택은 저장은 되나 다시 못 찾을 수 있다 · 색은 4종 고정. */
  /* 글자 하나를 여러 텍스트 노드에 걸쳐서도 칠한다.
   *
   * ⛔ 2026-08-27 실측 — 첫 판은 `wrapFirst` 를 그대로 썼고, 그건 **한 텍스트 노드 안에
   *   통째로 들어 있을 때만** 감싼다(`surroundContents` 가 원소 경계를 걸치면 던진다).
   *   digest 본문은 <b>·<em>·<sub>·<code> 가 촘촘해서 사람이 문장 하나를 드래그하면
   *   거의 항상 노드를 가로지른다 — **저장은 되는데 안 칠해졌다.** 1저자 신고로 드러났다.
   *   → 블록의 텍스트를 정규화해 이어 붙여 찾고, **걸치는 노드마다 조각을 따로 감싼다.**
   *     조각별로 감싸면 surroundContents 의 제약이 사라지고 화면에는 이어져 보인다.
   *
   * 못 하는 것: **문단(블록)을 가로지르는 선택**은 못 찾는다 — 블록 단위로 찾기 때문이다.
   *   그 경우 호출부가 "자리를 못 찾음" 으로 세고 사용자에게 알린다. */
  function paintText(block, needle, cls, hid, at) {
    if (!needle || needle.length < 2) return false;
    var nodes = [], full = "", map = [];
    var w = document.createTreeWalker(block, NodeFilter.SHOW_TEXT, null), n;
    while ((n = w.nextNode())) {
      if (n.parentNode && n.parentNode.closest &&
          n.parentNode.closest("mark.dn-hl,mark.dn-pen")) continue;
      nodes.push(n);
      var v = n.nodeValue;
      for (var i = 0; i < v.length; i++) {
        if (/\s/.test(v[i])) {
          if (full.length && full[full.length - 1] === " ") continue;
          full += " "; map.push({ n: n, o: i });
        } else { full += v[i]; map.push({ n: n, o: i }); }
      }
    }
    var p = full.indexOf(needle);
    if (p < 0) return false;
    // 걸치는 노드별로 [시작,끝) 구간을 모은다
    var groups = [], k;
    for (k = p; k < p + needle.length; k++) {
      var m = map[k];
      var g = groups[groups.length - 1];
      if (g && g.n === m.n) g.e = m.o + 1;
      else groups.push({ n: m.n, s: m.o, e: m.o + 1 });
    }
    groups.forEach(function (g) {
      var t = g.n;
      if (g.e < t.nodeValue.length) t.splitText(g.e);
      if (g.s > 0) t = t.splitText(g.s);
      var mk = document.createElement("mark");
      mk.className = cls;
      if (hid) mk.dataset.hid = hid;
      mk.title = "형광펜 " + (at || "") + " — 펜 켜고 누르면 지워요";
      t.parentNode.replaceChild(mk, t);
      mk.appendChild(t);
    });
    return true;
  }

  function paintPens() {
    if (!cur || !cur.pens) return;
    var blocks = blockList(), miss = 0;
    cur.pens.forEach(function (h) {
      var done = false;
      for (var i = 0; i < blocks.length && !done; i++) {
        done = paintText(blocks[i], h.text,
                         "dn-pen dn-pen-" + (h.color || "yellow"), h.id, h.at);
      }
      if (!done) miss++;
    });
    cur.penMiss = miss;
  }

  function loadPens() {
    if (!cur) return;
    fetch("/api/highlights/" + encodeURI(cur.rel))
      .then(function (r) { return r.json(); })
      .then(function (d) { if (cur) { cur.pens = d.items || []; render(); paintPenBtn(); } })
      .catch(function () { if (cur) cur.pens = []; });
  }

  function addPen(text) {
    if (!cur) return;
    fetch("/api/highlights/" + encodeURI(cur.rel), {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text, color: cur.penColor || "yellow" })
    }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (x) { if (!x.ok) { alert("⛔ " + (x.d.error || "실패")); return; } loadPens(); })
      .catch(function () { alert("⛔ 통신 실패"); });
  }

  function delPen(hid) {
    if (!cur) return;
    fetch("/api/highlights/" + encodeURI(cur.rel), {
      method: "DELETE", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: hid })
    }).then(function () { loadPens(); }).catch(function () { alert("⛔ 통신 실패"); });
  }

  function paintPenBtn() {
    var b = document.getElementById("docpen");
    if (!b) return;
    var on = !!(cur && cur.penOn), n = (cur && cur.pens ? cur.pens.length : 0);
    var miss = (cur && cur.penMiss) || 0;
    b.classList.toggle("on", on);
    b.textContent = (on ? "🖍 형광 켬" : "🖍 형광") + (n ? " " + n : "")
                    + (miss ? " ⚠" + miss : "");
    b.title = (on ? "글을 드래그하면 칠해요 · 칠한 곳을 누르면 지워요 (다시 눌러 끄기)"
                  : "형광펜을 켜요 — 켜면 드래그로 칠할 수 있어요")
              + (miss ? "\n⚠ " + miss + "개는 본문에서 자리를 못 찾았어요 "
                        + "(문단을 가로질러 고르면 그래요 — 한 문단 안에서 다시 칠해 주세요)" : "");
    document.body.classList.toggle("dn-pen-on", on);
  }

  global.docnotePenToggle = function () {
    if (!cur) return;
    cur.penOn = !cur.penOn;
    paintPenBtn();
  };

  function save(text, anchor) {
    if (!norm(text)) return;
    fetch("/api/comments/" + encodeURI(cur.rel), {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text, anchor: anchor || "" })
    }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (x) {
        if (!x.ok) { alert("⛔ " + (x.d.error || "저장 실패")); return; }
        if (global.syncPaperCmtIndex) global.syncPaperCmtIndex(x.d);
        load();
      })
      .catch(function () { alert("⛔ 통신 실패"); });
  }

  /* ── 새 메모 초안 ──────────────────────────────────────────────────────── */

  function killDraft() {
    if (!cur) return;
    var d = cur.gut && cur.gut.querySelector(".dn-draft");
    if (d) d.parentNode.removeChild(d);
    if (cur.draftEl && cur.draftEl.classList) cur.draftEl.classList.remove("dn-anch-live");
    cur.draftEl = null; cur.draftAnchor = "";
    layout();
  }

  function openDraft(block, anchor) {
    killDraft();
    cur.draftEl = block;
    cur.draftAnchor = anchor;
    block.classList.add("dn-anch-live");
    var d = document.createElement("div");
    d.className = "dn-draft";
    d.innerHTML =
      '<div class="dn-meta">새 메모<button type="button" class="dn-cancel" title="취소 (Esc)">✕</button></div>' +
      (anchor ? '<div class="dn-quote">' + esc(anchor) + "</div>" : "") +
      '<textarea class="dn-in" rows="3" placeholder="메모… (Ctrl+Enter 저장 · Esc 취소 · Ctrl+B 굵게 · Ctrl+H 형광 · Shift+Enter 줄바꿈 · 그림은 붙여넣기)"></textarea>' +
      '<div class="dn-act"><button type="button" class="btn sm dn-save">저장</button></div>';
    cur.gut.appendChild(d);
    layout();
    var ta = d.querySelector(".dn-in");
    autosize(ta);
    ta.focus();
    d.scrollIntoView({ block: "nearest" });
  }

  /* 오른쪽 클릭한 자리 → (고른 글 있으면 그 글, 없으면 문단 앞머리) */
  function anchorFor(block) {
    var s = global.getSelection && global.getSelection();
    if (s && !s.isCollapsed && s.rangeCount) {
      var t = norm(s.toString());
      // 고른 글이 이 문단 안에 있을 때만 인정 — 딴 데 남은 선택을 끌어오지 않는다
      if (t && t.length >= 2 && block.contains(s.getRangeAt(0).commonAncestorContainer
            .nodeType === 1 ? s.getRangeAt(0).commonAncestorContainer
                            : s.getRangeAt(0).commonAncestorContainer.parentNode)) {
        return t.slice(0, 160);
      }
    }
    return norm(block.textContent).slice(0, 160);
  }

  /* ── mount / unmount ───────────────────────────────────────────────────── */

  global.mountDocNotes = function (bodyEl, rel, hostEl) {
    if (!bodyEl || !rel || !hostEl) return;
    global.unmountDocNotes();
    var gut = hostEl.querySelector(".dnote-gut");
    if (!gut) {
      gut = document.createElement("aside");
      gut.className = "dnote-gut";
      hostEl.appendChild(gut);
    }
    hostEl.classList.add("dnote-on");
    cur = { body: bodyEl, rel: rel, host: hostEl, gut: gut,
            notes: [], map: {}, draftEl: null, draftAnchor: "",
            pens: [], penOn: false, penColor: "yellow" };
    gut.innerHTML = '<div class="dn-h">📝 메모</div>';
    load();
    loadPens();
    paintPenBtn();
    // 형광펜: 켜져 있을 때만 드래그가 칠한다. 꺼져 있으면 평소처럼 글이 선택될 뿐이다
    //   — 읽다가 실수로 칠하는 사고를 막으려고 **기본은 꺼짐**이다.
    bodyEl.addEventListener("mouseup", function () {
      if (!cur || !cur.penOn) return;
      var sel = global.getSelection();
      if (!sel || sel.isCollapsed) return;
      var t = norm(String(sel));
      if (t.length < 2) return;
      if (!bodyEl.contains(sel.anchorNode)) return;
      sel.removeAllRanges();
      addPen(t.slice(0, 400));
    });
    // 칠한 곳을 누르면 지운다 (펜이 켜져 있을 때만 — 꺼져 있으면 그냥 글이다)
    bodyEl.addEventListener("click", function (e) {
      if (!cur || !cur.penOn) return;
      var m = e.target.closest && e.target.closest("mark.dn-pen");
      if (!m || !m.dataset.hid) return;
      e.preventDefault(); e.stopPropagation();
      delPen(m.dataset.hid);
    }, true);
    // 본문 높이가 바뀌면(그림 로딩·표 접힘) 카드 자리도 따라가야 한다
    if (global.ResizeObserver) {
      cur.ro = new ResizeObserver(function () { layout(); });
      cur.ro.observe(bodyEl);
    }
  };

  global.unmountDocNotes = function () {
    if (!cur) return;
    if (cur.ro) cur.ro.disconnect();
    clearHl();
    if (cur.host) cur.host.classList.remove("dnote-on");
    if (cur.gut && cur.gut.parentNode) cur.gut.parentNode.removeChild(cur.gut);
    cur = null;
    document.body.classList.remove("dn-pen-on");
    var pb = document.getElementById("docpen");
    if (pb) { pb.classList.remove("on"); pb.textContent = "🖍 형광"; }
  };

  global.docNoteLayout = layout;

  /* ── 이벤트 (문서에 한 번만) ───────────────────────────────────────────── */

  document.addEventListener("contextmenu", function (e) {
    if (!cur) return;
    if (!cur.body.contains(e.target)) return;
    var block = e.target.closest && e.target.closest(BLOCKS);
    if (!block || !cur.body.contains(block)) return;
    if (block.closest(".figstrip") || block.closest(".figpane")) return;  // 그림은 💬 담당
    e.preventDefault();
    openDraft(block, anchorFor(block));
  });

  document.addEventListener("click", function (e) {
    if (!cur) return;
    if (e.target.closest(".dn-cancel")) { killDraft(); return; }
    if (e.target.closest(".dn-editcancel")) { closeEdit(); return; }
    if (e.target.closest(".dn-save")) {
      // 저장 버튼은 새 메모(.dn-draft)와 고치기(.dn-card.dn-editing)가 같이 쓴다
      var ec = e.target.closest(".dn-card");
      if (ec) { patch(ec.dataset.nid, ec.querySelector(".dn-in").value); closeEdit(); return; }
      var d = e.target.closest(".dn-draft");
      save(d.querySelector(".dn-in").value, cur.draftAnchor);
      killDraft();
      return;
    }
    if (e.target.closest(".dn-edit")) {
      openEdit(e.target.closest(".dn-card")); return;
    }
    // 글을 누르면 바로 고치기 (1저자 요청 2026-08-17 "메모 다시 누르면 수정도")
    if (e.target.closest(".dn-text") && !e.target.closest(".dn-in")) {
      openEdit(e.target.closest(".dn-card")); return;
    }
    if (e.target.closest(".dn-card.dn-editing")) return;   // 고치는 중엔 점프 금지
    var del = e.target.closest(".dn-del");
    if (del) {
      var nid = del.closest(".dn-card").dataset.nid;
      if (!confirm("이 메모를 지울까요?")) return;
      fetch("/api/comments/" + encodeURI(cur.rel) + "?id=" + encodeURIComponent(nid),
            { method: "DELETE" })
        .then(function () { load(); })
        .catch(function () { alert("⛔ 통신 실패"); });
      return;
    }
    // 카드를 누르면 붙어 있는 자리로 데려간다 (Word 에서 메모 클릭과 같다)
    var card = e.target.closest(".dn-card");
    if (card && cur.map[card.dataset.nid]) {
      var el = cur.map[card.dataset.nid];
      el.scrollIntoView({ block: "center", behavior: "smooth" });
      el.classList.add("dn-flash");
      setTimeout(function () { el.classList.remove("dn-flash"); }, 1200);
    }
  });

  /* Esc 는 **모달보다 먼저** 잡는다 — 초안을 쓰다 Esc 를 누르면 모달이 닫혀 글이
   * 통째로 날아갔다. capture 단계에서 초안만 접고 전파를 끊는다. */
  document.addEventListener("keydown", function (e) {
    if (!cur || e.key !== "Escape") return;
    if (cur.gut && cur.gut.querySelector(".dn-draft")) {
      e.stopPropagation(); e.preventDefault(); killDraft(); return;
    }
    if (editing()) { e.stopPropagation(); e.preventDefault(); closeEdit(); }
  }, true);

  document.addEventListener("input", function (e) {
    if (!cur) return;
    var ta = e.target.closest && e.target.closest(".dn-in");
    if (ta) { autosize(ta); layout(); }
  });

  document.addEventListener("keydown", function (e) {
    if (!cur) return;
    var ta = e.target.closest && e.target.closest(".dn-in");
    if (!ta) return;
    // Ctrl/⌘+B = 굵게. 워드에서 하던 손이 여기서도 먹어야 한다 (1저자 요청 2026-08-27).
    //   브라우저 기본 Ctrl+B(사이드바/북마크)를 막아야 하므로 preventDefault 가 필수다.
    if ((e.ctrlKey || e.metaKey) && (e.key === "b" || e.key === "B")) {
      e.preventDefault(); wrapSel(ta, "**"); return;
    }
    if ((e.ctrlKey || e.metaKey) && (e.key === "h" || e.key === "H")) {
      e.preventDefault(); wrapSel(ta, "=="); return;      // 메모 안 형광펜
    }
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      var card = ta.closest(".dn-card");
      if (card) { patch(card.dataset.nid, ta.value); closeEdit(); }
      else { save(ta.value, cur.draftAnchor); killDraft(); }
    }
  });

  global.addEventListener("resize", function () { layout(); });
})(window);
