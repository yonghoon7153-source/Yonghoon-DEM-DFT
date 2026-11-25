/* docnote.js — 보고서 본문에 **Word 식 여백 메모** + 형광펜 (DEM 웹앱 · 공유 보고서 보기 화면 /reports/<slug>).
 *
 * 1저자 11-25: *"이렇게 독립적인 우리 분야들 있잖아 이렇게 토글로 묶고 이렇게 안에서 html 나 웹페이지 등 킬 수 있게 해줘"* —
 * 참고 = DFT 웹앱의 docnote.js (보고서 보기 화면의 여백 메모 · 형광펜).  구조는 그대로 옮기고 **저장 자리만 바꿨다**:
 *
 *   mountDocNotes(bodyEl, rel, hostEl)   — 본문에 메모 기능을 단다 (본문이 같은 출처 iframe 안이어도 된다)
 *   unmountDocNotes()                    — 정리
 *
 * 저장은 **보는 사람 브라우저 (localStorage)** 에만 한다 — 이 웹앱에는 메모 창고 (서버) 가 없다.
 *   열쇠 = "dem-dnote:v1:notes:<rel>" · "dem-dnote:v1:pens:<rel>" (rel = 리포 기준 보고서 파일 경로).
 *   ⛔ 다른 기기 · 다른 브라우저 · 다른 사람과 나누지 않는다.  보고서 파일 · 새 탭 · 내려받기는 원본 바이트 그대로다.
 *   ⛔ 저장이 막힌 브라우저 (사생활 창 · 막힌 사이트 자료 · 칸이 참) 에서는 **이번 화면에서만** 기억하고 머리줄에 그렇게 적는다
 *     (조용히 버리지 않는다).  저장된 값을 못 읽으면 (깨진 JSON) 지우지 않고 사본 열쇠 (…:bak-<시각>) 로 옮긴 뒤 새로 쓴다.
 *   ⛔ 메모 글은 이 브라우저에서 그린다 — 먼저 이스케이프 (HTML 주입 없음) → **굵게** · ==형광== · `code` 만.  그림 붙여넣기는 없다.
 *
 * 자리를 **글로** 잡는다 (좌표 · 문단 번호가 아니라)
 *   보고서를 고치면 문단이 밀린다.  글 지문으로 잡으면 문단이 밀려도 따라가고, 글이 아예 지워지면 "자리를 잃은 메모"
 *   로 위에 모아 둔다 — **지우지 않는다**.  메모를 잃는 게 자리를 잃는 것보다 나쁘다.
 *
 * 이 파일이 **못 하는 것**
 *   · 여러 문단에 걸친 선택을 형광펜으로 못 칠한다 (블록 안일 때만) — 버튼에 '⚠ 자리 못 찾음 n' 을 적는다.
 *   · 같은 글이 문서에 여러 번 나오면 **첫 번째**에 붙는다 — 구분하지 못한다.
 *   · **붙인 자리(anchor)는 못 고친다.** 글만 고쳐진다 — 자리를 옮기려면 지우고 다시 단다.
 *   · 보고서가 새 날짜 판 (다른 파일 이름) 으로 바뀌면 메모는 옛 파일 이름 열쇠에 남는다.
 *
 * 고치기 — 글을 누르거나 ✎ 를 누르면 제자리에서 고친다.  옛 글은 **지우지 않고** item.history 에 쌓는다.
 * 접기 — 여백 머리줄의 [접기 ▸] 로 카드를 감추고 여백을 얇은 띠로 줄인다 (감출 뿐 지우지 않는다 · 상태도 이 브라우저에만).
 *
 * 본문이 iframe 안에 있을 때 (보기 화면 = 보고서 원본을 같은 출처 iframe 으로 띄운다 — 보고서는 자기 CSS 를 가진 완결 HTML)
 *   여백 (카드) 은 늘 hostEl 쪽 — 이 창 — 문서에 그리고, **본문 쪽 일만** 본문의 문서로 한다:
 *   글 찾기 · 칠하기 · 선택 · 오른쪽 클릭 · Esc.  카드 높이는 iframe 의 위치를 더해 맞춘다 (topOf).
 *   본문에 칠하는 표시 (형광펜 · 메모 자리 · 반짝임) 의 CSS 는 이 창 style.css 에서 골라 iframe 문서에 옮긴다 (shareBodyCss).
 *   ⛔ 못 하는 것: iframe 은 **한 겹만** · 같은 출처만 · iframe 이 안쪽으로 굴러가면 카드가 안 따라간다 —
 *     띄우는 쪽이 iframe 높이를 내용에 맞춰 안쪽 스크롤을 없앤다 · iframe 이 다른 문서로 가면 띄우는 쪽이 다시 단다.
 */
(function (global) {
  "use strict";

  var BLOCKS = "p,li,h1,h2,h3,h4,h5,h6,blockquote,pre,td,th,figcaption";
  var cur = null;          // {body, rel, host, gut, notes, map, draft}

  /* 여백 접기 상태 — 보는 사람 브라우저에만 (localStorage). 읽기 · 쓰기가 막혀 있으면 이번 화면에서만 기억한다. */
  var FOLD_KEY = "dnote-folded";
  var foldMem = null;
  function folded() {
    if (foldMem !== null) return foldMem;
    try { foldMem = global.localStorage.getItem(FOLD_KEY) === "1"; } catch (e) { foldMem = false; }
    return foldMem;
  }
  function setFolded(v) {
    foldMem = !!v;
    try { global.localStorage.setItem(FOLD_KEY, foldMem ? "1" : "0"); } catch (e) { /* 이번 화면에서만 */ }
  }

  /* 글 서식 — 참고 판은 comments.js 의 서식 묶음 (서버가 그린 html) 을 불렀다.  이 웹앱에는 그 파일 · 메모 서버가 없어서
   * 같은 규약을 이 파일 안에 둔다 (집 = 여기 하나).  ⚠ inline 은 **esc 뒤에** 돈다 — 순서가 뒤집히면 HTML 주입이다.
   * 못 하는 것: 블록 문법 (목록 · 표 · 제목) · 그림 · 링크는 없다 — 여기는 메모지 문서가 아니다. */
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function inline(s) {
    return esc(s)
      .replace(/`([^`\n]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*\n]+)\*\*/g, "<b>$1</b>")
      .replace(/==([^=\n]+)==/g, '<mark class="dn-penmk">$1</mark>');
  }
  function disp(x) { return inline((x && x.text) || ""); }
  /* 입력창을 내용에 맞춰 늘린다 — 화면 높이의 55 % 를 넘지는 않는다 (그 위로는 상자 안에서 굴린다).
   * ⚠ 여백 메모에서는 높이가 바뀌면 배치가 어긋나므로 **호출한 쪽이 layout() 을 같이 부른다.** */
  function autosize(ta) {
    if (!ta) return;
    ta.style.height = "auto";
    var max = Math.round((global.innerHeight || 800) * 0.55);
    ta.style.height = Math.min(ta.scrollHeight + 2, max) + "px";
  }
  /* textarea 선택 영역을 표시로 감싼다 / 벗긴다 (Ctrl+B · Ctrl+H) */
  function wrapSel(ta, mk) {
    var a = ta.selectionStart, b = ta.selectionEnd, v = ta.value, sel = v.slice(a, b), n = mk.length;
    if (sel && v.slice(a - n, a) === mk && v.slice(b, b + n) === mk) {
      ta.value = v.slice(0, a - n) + sel + v.slice(b + n);
      ta.setSelectionRange(a - n, b - n);
    } else if (sel.length > 2 * n && sel.slice(0, n) === mk && sel.slice(-n) === mk) {
      ta.value = v.slice(0, a) + sel.slice(n, -n) + v.slice(b);
      ta.setSelectionRange(a, b - 2 * n);
    } else {
      ta.value = v.slice(0, a) + mk + sel + mk + v.slice(b);
      if (sel) ta.setSelectionRange(a + n, b + n); else ta.setSelectionRange(a + n, a + n);
    }
  }

  /* ── 저장 — 보는 사람 브라우저 (localStorage) ────────────────────────────
   * 참고 판의 서버 창고 (메모 · 형광펜 두 창고) 자리.  항목 꼴은 같다:
   *   메모 {id, at, anchor, text, edited_at?, history?[{at, text}]} · 형광펜 {id, at, text, color}.
   * mode = "local" (이 브라우저에 남는다) · "memory" (저장이 막혀 이번 화면에서만).  깨진 값은 지우지 않고 사본으로 옮긴다. */
  var STORE_PREFIX = "dem-dnote:v1:";
  var memStore = {};
  function storeKey(kind, rel) { return STORE_PREFIX + kind + ":" + rel; }
  function isItem(x) { return x && typeof x === "object" && typeof x.id === "string" && typeof x.text === "string"; }
  function storeRead(kind, rel) {
    var k = storeKey(kind, rel), raw;
    try { raw = global.localStorage.getItem(k); }
    catch (e) { return { items: (memStore[k] || []).slice(), mode: "memory" }; }
    if (memStore[k]) return { items: memStore[k].slice(), mode: "memory" };   // 앞서 쓰기가 막혔다 — 이번 화면 값이 최신
    if (raw == null) return { items: [], mode: "local" };
    var v = parseList(raw);
    if (v && v.every(isItem)) return { items: v, mode: "local" };
    return { items: v ? v.filter(isItem) : [], mode: "local", corrupt: raw };   // 깨졌거나 꼴이 다른 항목 — 쓸 때 사본으로 옮긴다
  }
  function parseList(raw) { try { var v = JSON.parse(raw); return Array.isArray(v) ? v : null; } catch (e) { return null; } }
  function storeWrite(kind, rel, items) {
    var k = storeKey(kind, rel);
    try {
      var old = global.localStorage.getItem(k), ov = old == null ? [] : parseList(old);
      if (old != null && !(ov && ov.every(isItem))) {
        global.localStorage.setItem(k + ":bak-" + Date.now(), old);   // 못 읽는 옛 값은 지우지 않고 사본 열쇠로 옮긴다
      }
      global.localStorage.setItem(k, JSON.stringify(items));
      delete memStore[k];
      return "local";
    } catch (e) {
      memStore[k] = items.slice();
      return "memory";
    }
  }
  function newId(p) { return p + Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }
  function nowStr() {
    var d = new Date(), z = function (n) { return (n < 10 ? "0" : "") + n; };
    return d.getFullYear() + "-" + z(d.getMonth() + 1) + "-" + z(d.getDate()) + " " + z(d.getHours()) + ":" + z(d.getMinutes());
  }
  function noteWrite(items) { cur.notesMode = storeWrite("notes", cur.rel, items); }
  function penWrite(items) { cur.pensMode = storeWrite("pens", cur.rel, items); }
  function norm(s) { return String(s == null ? "" : s).replace(/\s+/g, " ").trim(); }

  /* ── 본문의 문서 · 창 (iframe 이면 그쪽 · 머리 주석 '본문이 iframe 안에 있을 때') ── */

  function bwin(d) { return (d && d.defaultView) || global; }

  /* 본문 원소의 위쪽 좌표를 **이 창 (여백) 기준**으로. 같은 문서면 getBoundingClientRect 그대로다.
   * iframe 안이면 그 iframe 의 내용 상자 위치 (테두리 · 안쪽 여백 포함) 를 더한다 — 한 겹만. */
  function topOf(el) {
    var t = el.getBoundingClientRect().top;
    var w = el.ownerDocument && el.ownerDocument.defaultView;
    var f = w && w !== global ? w.frameElement : null;
    if (f) {
      t += f.getBoundingClientRect().top + f.clientTop
         + (parseFloat(global.getComputedStyle(f).paddingTop) || 0);
    }
    return t;
  }

  /* 본문 쪽 표시 규칙만 iframe 문서에 옮긴다 — 형광펜 (mark.dn-pen*) · 메모 자리 (mark.dn-hl · .dn-anch*) ·
   * 반짝임 (.dn-flash · @keyframes dnflash) · 펜 켬 커서 (body.dn-pen-on). 다크 모드 @media 도 그대로 따라간다.
   * 왜 고르나: style.css 를 통째로 넣으면 보고서 자기 CSS 와 변수 이름 (--bg 등) · 원소 규칙이 겹쳐 둘 다 깨진다.
   * 왜 사본 파일이 아닌가: 집은 style.css 하나다 — 두 벌이면 한쪽만 고쳐진다 (이 파일 위 ⛔⛔ 2026-08-28 과 같은 병).
   * ⛔ 못 하는 것: 다른 출처 스타일시트 (글꼴 CDN) 는 브라우저가 못 읽게 막아 건너뛴다 · 고른 규칙이 0 개면
   *   칠은 되지만 브라우저 기본 <mark> 노랑으로만 보인다 (색 구분 · 메모 자리 막대 · 반짝임 없음 — 2026-11-17 일부러 빼 보고 실측)
   *   → 콘솔에 알리고 개수를 cur.bodyCssN 에 남긴다 (시험은 iframe 문서에 옮겨진 규칙 수와 칠한 색을 본다). */
  var BODY_CSS = /mark\.dn-|\.dn-anch|\.dn-flash|dn-pen-on/;
  function bodyRules(list, out) {
    [].forEach.call(list || [], function (r) {
      if (r.type === 1) {                                  // CSSStyleRule
        if (BODY_CSS.test(r.selectorText || "")) out.push(r.cssText);
      } else if (r.type === 4) {                           // CSSMediaRule — 안쪽만 골라 같은 조건으로 감싼다
        var inner = bodyRules(r.cssRules, []);
        if (inner.length) out.push("@media " + (r.conditionText || r.media.mediaText) + "{" + inner.join("\n") + "}");
      } else if (r.type === 7 && /^dn/.test(r.name || "")) {   // CSSKeyframesRule (dnflash)
        out.push(r.cssText);
      }
    });
    return out;
  }
  function shareBodyCss(d) {
    var old = d.getElementById("dn-body-css");
    if (old) return old._dnN || 0;
    var out = [];
    [].forEach.call(document.styleSheets, function (ss) {
      var rules;
      try { rules = ss.cssRules; } catch (_) { return; }  // 다른 출처 — 못 읽는다
      bodyRules(rules, out);
    });
    var st = d.createElement("style");
    st.id = "dn-body-css";
    st.textContent = out.join("\n");
    st._dnN = out.length;
    (d.head || d.documentElement).appendChild(st);
    if (!out.length && global.console) {
      global.console.warn("docnote: 본문 쪽 표시 규칙을 이 창 CSS 에서 못 찾았다 — iframe 안 형광펜 · 메모 자리가 기본 <mark> 모양으로만 보인다");
    }
    return out.length;
  }

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
    var od = block.ownerDocument || document;     // 본문의 문서 (iframe 이면 그쪽)
    var w = od.createTreeWalker(block, NodeFilter.SHOW_TEXT, null), n;
    while ((n = w.nextNode())) {
      if (n.parentNode && n.parentNode.closest &&
          n.parentNode.closest("mark.dn-hl,mark.dn-pen")) continue;
      var i = n.nodeValue.indexOf(needle);
      if (i < 0) continue;
      var r = od.createRange();
      r.setStart(n, i); r.setEnd(n, i + needle.length);
      var mk = od.createElement("mark");
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
      '<button type="button" class="dn-expand" title="넓게 보기 (다시 누르면 되돌림)">⤢</button>' +
      '<button type="button" class="dn-edit" title="고치기">✎</button>' +
      '<button type="button" class="dn-del" title="지우기">✕</button></div>' +
      (nt.anchor ? '<div class="dn-quote">' + esc(nt.anchor) + "</div>" : "") +
      '<div class="dn-text" title="눌러서 고치기">' + disp(nt) + "</div></div>";
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
      '<div class="dn-act"><button type="button" class="btn btn-sm btn-secondary dn-editcancel">취소</button>' +
      '<button type="button" class="btn btn-sm btn-primary dn-save">저장</button></div>';
    var ta = box.querySelector(".dn-in");
    ta.value = nt ? nt.text : "";
    // ⚠ autosize 를 여기서 부르지 않는다 — 아직 카드가 **안 넓어졌다.**
    //   layout() 이 폭을 정한 뒤 스스로 맞춘다 (위 주석 참조).
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
    if (!norm(text) || !cur) return;
    var items = storeRead("notes", cur.rel).items, hit = false;
    items.forEach(function (n) {
      if (n.id !== nid || n.text === text) return;
      (n.history = n.history || []).push({ at: n.edited_at || n.at, text: n.text });   // 옛 글은 지우지 않는다
      n.text = text; n.edited_at = nowStr(); hit = true;
    });
    if (hit) noteWrite(items);
    load();
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
      '<div class="dn-h"><span class="dn-ttl">📝 메모 <span class="muted">' + cur.notes.length + "</span></span>" +
      '<span class="dn-hint">본문에서 오른쪽 클릭</span>' +
      '<button type="button" class="dn-fold" aria-expanded="true">접기 ▸</button></div>' +
      lost.map(function (n) { return cardHtml(n, true); }).join("") +
      ok.map(function (n) { return cardHtml(n, false); }).join("");
    paintBadge();
    syncOn();
    layout();
  }

  /* 여백은 **메모나 쓰는 중인 초안이 있을 때만** 편다 (2026-10-28).
   * ⛔ 종전엔 mount 하자마자 dnote-on 을 붙여서 메모 0 건인 개념 페이지 15 쪽 전부에
   *   빈 460px 여백이 잡혔다 — 1920 화면에서 본문이 428px 로 눌렸다 (사용자 신고 · 실측).
   *   메모를 다는 길은 그대로다: 본문 오른쪽 클릭 → openDraft 가 여백을 연다. */
  function syncOn() {
    if (!cur || !cur.host) return;
    var was = [cur.host.classList.contains("dnote-on"), cur.host.classList.contains("dnote-folded")].join();
    var on = cur.notes.length > 0 || !!cur.draftEl;
    cur.host.classList.toggle("dnote-on", on);
    // 접기 — 초안이 열려 있으면 접지 않는다 (숨은 초안 금지 · openDraft 가 펴 둔다)
    var f = on && folded() && !cur.draftEl;
    cur.host.classList.toggle("dnote-folded", f);
    var b = cur.gut && cur.gut.querySelector(".dn-fold");
    if (b) {
      b.setAttribute("aria-expanded", f ? "false" : "true");
      b.textContent = f ? "◂ 펴기" : "접기 ▸";
      b.title = f ? "메모 여백 펴기 (메모 " + cur.notes.length + " 개)" : "메모 여백 접기 — 본문이 넓어진다 (메모는 그대로)";
    }
    /* 여백이 열리거나 접히면 본문 칸 폭이 바뀐다 — host 에 **그 자리에서** 알린다 (2026-11-17 · /interface-thermo).
     * 띄우는 쪽이 폭에 딸린 것 (iframe 높이) 을 카드 배치 · ?note= 굴리기 **전에** 다시 맞추게 한다. 다음 그림 차례
     * (ResizeObserver) 까지 기다리면 그사이 딥링크 굴리기가 아직 짧은 iframe 의 안쪽을 굴려서, 높이를 맞추는 순간
     * 자리가 밀렸다 (1440px 창 실측 — 메모 자리가 화면 가운데가 아니라 아래 끝 873/900). 듣는 쪽이 없으면 아무 일도 없다. */
    if ([on, f].join() !== was && global.CustomEvent) {
      cur.host.dispatchEvent(new CustomEvent("dnote:toggle", { detail: { on: on, folded: f } }));
    }
  }

  /* 머리줄 ([접기 ▸] 버튼) 이 위에 붙는 상자에 가리지 않게 그 높이만큼 내려 붙인다 (2026-11-11 실측) —
   * 논문 페이지는 #doctoc (목차 · sticky top 0 · z 5) 가, 논문 창은 .modal-head (sticky · z 3) 가 위를 덮어서
   * 굴리면 머리줄 (z 2) 이 그 뒤로 숨었다. 여백과 가로로 겹치는 붙은 상자만 센다 (겹치는 것 중 가장 큰 높이). */
  function headTop() {
    if (!cur || !cur.gut) return;
    var t = 0, g = cur.gut.getBoundingClientRect();
    [document.getElementById("doctoc"), cur.host && cur.host.querySelector(".modal-head")].forEach(function (el) {
      if (!el || cur.gut.contains(el)) return;
      var pos = getComputedStyle(el).position;
      if (pos !== "sticky" && pos !== "fixed") return;
      var a = el.getBoundingClientRect();
      if (a.right > g.left && a.left < g.right && a.height > 0) t = Math.max(t, Math.ceil(a.height) + 4);
    });
    cur.gut.style.setProperty("--dn-h-top", t + "px");
  }

  function toggleFold() {
    if (!cur) return;
    setFolded(!folded());
    syncOn();
    if (!folded()) setTimeout(function () { if (cur) layout(); }, 0);   // 편 뒤에 카드 자리를 다시 잰다
  }

  /* 카드를 자기 자리 높이에 맞춰 세로로 놓는다. 겹치면 아래로 민다 (Word 와 같다).
   * ⚠ 카드는 gut 안에서 absolute — gut 과 본문이 **같은 스크롤 상자** 안에 있어야
   *   rect 차이가 스크롤과 무관해진다. .modal-body 가 그 상자다. */
  function layout() {
    if (!cur || !cur.gut) return;
    headTop();
    var head = cur.gut.querySelector(".dn-h");
    var gr = cur.gut.getBoundingClientRect();
    var cards = [].slice.call(cur.gut.querySelectorAll(".dn-card,.dn-draft"));
    /* ⚠ katex·mermaid·figref 는 mount 뒤에도 본문 조각을 **갈아끼운다**. 그러면 우리가
     *   잡아 둔 자리 원소가 문서에서 떨어져 나가고, 카드가 전부 맨 위로 몰린다
     *   (붙인 자리를 잃은 것처럼 보인다). 떨어진 걸 발견하면 자리를 다시 찾는다. */
    var stale = false;
    var rows = cards.map(function (c) {
      var el = c.dataset.nid ? cur.map[c.dataset.nid] : cur.draftEl;
      // ⚠ 자기 문서에 아직 있나를 본다 — 본문이 iframe 이면 이 창 document 가 아니다 (2026-11-17).
      if (el && !(el.ownerDocument || document).contains(el)) { stale = true; el = null; }
      var t = el ? topOf(el) - gr.top : 0;      // topOf = 이 창 기준 (iframe 위치 포함)
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

    /* 폭을 통째로 쓰는 카드 = 고치는 중 · 새 메모 초안 · **사용자가 ⤢ 로 편 것**.
     * 세 경우를 한 이름으로 묶는다 — 규칙이 갈라지면 한쪽만 고쳐진다(오늘 세 번 겪음). */
    function isEd(c) {
      return c.classList.contains("dn-editing") || c.classList.contains("dn-draft")
          || c.classList.contains("dn-wide");
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
    /* ⛔⛔ 2026-08-28 실측 — **고치는 중인 카드는 절대 반폭이 아니다.**
     *   고치면 카드가 길어져 옆 카드와 겹치므로 위 규칙이 half=true 로 만들고,
     *   그러면 아래 ③ 이 left 를 열 위치(11px)로 덮어썼다. 폭은 넓힌 그대로(739px)라
     *   카드가 여백칸(460px)을 **오른쪽으로 290px 삐져나갔다** — 왼쪽으로 넓어져야 하는데
     *   오른쪽으로 밀려난 것이다 (1저자: "이쪽 말고 왼쪽으로 확장되게"). */
    rows.forEach(function (r, i) { if (isEd(r.c)) half[i] = false; });

    // ② 정해진 폭을 입히고 **다시 잰다**
    rows.forEach(function (r, i) {
      if (isEd(r.c) && nCol > 1) setW(r.c, fullW + OVER, PAD - OVER);
      else setW(r.c, half[i] ? colW : fullW, PAD);
      r.c.classList.toggle("dn-half", half[i] && !isEd(r.c));
    });
    /* ⛔⛔ 2026-08-28 (1저자: "저 흰색 여백을 안보게") — 입력창 높이를 **폭이 정해진 뒤에**
     *   다시 맞춘다. openEdit() 이 좁은 카드에서 autosize 를 부르고 그 다음에 카드가
     *   왼쪽으로 넓어졌기 때문에, 글은 3줄로 접혔는데 상자는 좁을 때 줄 수(10줄)로
     *   남아 **아래가 통째로 흰 여백**이었다. 배치 버그와 같은 병이다 — 재는 순서.
     *   여기서 하는 이유: 폭을 정하는 곳이 여기뿐이라 순서가 어긋날 수 없다. */
    rows.forEach(function (r) {
      var ta = r.c.querySelector(".dn-in");
      if (ta) autosize(ta);
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
        if (!isEd(r.c)) r.c.style.left = (PAD + k * (colW + GAP)) + "px";   // ②가 정한 자리를 지킨다
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
    var card = null;
    try {       // 주소 (?note=) 에서 온 값 — 선택자가 깨지면 그냥 못 찾은 것으로 (화면을 멈추지 않는다)
      card = cur.gut.querySelector('.dn-card[data-nid="' + (global.CSS && global.CSS.escape ? global.CSS.escape(nid) : nid.replace(/"/g, '\\"')) + '"]');
    } catch (e) { card = null; }
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
    // 여백은 메모가 있을 때만 열리므로 (syncOn), 0 건일 때는 **다는 법**을 글자로 보인다
    var mem = cur && (cur.notesMode === "memory" || cur.pensMode === "memory");
    var bad = cur && (cur.notesCorrupt != null || cur.pensCorrupt != null);
    b.textContent = (n ? "📝 메모 " + n : "📝 메모 0 · 본문 오른쪽 클릭으로 추가")
      + (mem ? " · ⚠ 이 브라우저가 저장을 막았다 (새로 고치면 사라진다)" : "")
      + (bad ? " · ⚠ 저장된 메모를 못 읽었다 (지우지 않고 사본으로 둔다)" : "");
    b.title = (n ? n + "건 — 본문 오른쪽 클릭으로 더 답니다"
                 : "본문을 오른쪽 클릭하면 메모를 답니다 (여백은 메모가 생기면 열린다)")
              + " · 저장 = 이 브라우저에만 (다른 기기 · 다른 사람과 나누지 않는다)";
    b.classList.toggle("dn-warn", !!(mem || bad));
  }

  /* ── 서버 ──────────────────────────────────────────────────────────────── */

  function load() {
    if (!cur) return;
    var r = storeRead("notes", cur.rel);
    cur.notes = r.items;
    cur.notesMode = r.mode;
    cur.notesCorrupt = r.corrupt != null ? r.corrupt : null;
    render();
    focusFromUrl();
  }

  /* ── 형광펜 (2026-08-27) ────────────────────────────────────────────────
   * 메모와 **열쇠가 다르다** (…:pens:<rel>). 자리 잡는 방식은 같다 — 글 지문.
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
    var od = block.ownerDocument || document;     // 본문의 문서 (iframe 이면 그쪽)
    var w = od.createTreeWalker(block, NodeFilter.SHOW_TEXT, null), n;
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
      var mk = od.createElement("mark");
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
    var r = storeRead("pens", cur.rel);
    cur.pens = r.items;
    cur.pensMode = r.mode;
    cur.pensCorrupt = r.corrupt != null ? r.corrupt : null;
    render();
    paintPenBtn();
  }

  function addPen(text) {
    if (!cur) return;
    var items = storeRead("pens", cur.rel).items;
    items.push({ id: newId("h"), at: nowStr(), text: text, color: cur.penColor || "yellow" });
    penWrite(items);
    loadPens();
  }

  function delPen(hid) {
    if (!cur) return;
    penWrite(storeRead("pens", cur.rel).items.filter(function (h) { return h.id !== hid; }));
    loadPens();
  }

  function paintPenBtn() {
    paintBadge();
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
    // 본문이 iframe 이면 그 문서 body 에도 — 칠한 곳 커서 · 점선 (body.dn-pen-on mark.dn-pen) 은 그쪽 CSS 가 본다
    var fb = cur && cur.frameDoc && cur.frameDoc.body;
    if (fb) fb.classList.toggle("dn-pen-on", on);
  }

  global.docnotePenToggle = function () {
    if (!cur) return;
    cur.penOn = !cur.penOn;
    paintPenBtn();
  };

  function save(text, anchor) {
    if (!norm(text) || !cur) return;
    var items = storeRead("notes", cur.rel).items;
    items.push({ id: newId("n"), at: nowStr(), anchor: anchor || "", text: text });
    noteWrite(items);
    load();
  }

  /* ── 새 메모 초안 ──────────────────────────────────────────────────────── */

  function killDraft() {
    if (!cur) return;
    var d = cur.gut && cur.gut.querySelector(".dn-draft");
    if (d) d.parentNode.removeChild(d);
    if (cur.draftEl && cur.draftEl.classList) cur.draftEl.classList.remove("dn-anch-live");
    cur.draftEl = null; cur.draftAnchor = "";
    syncOn();
    layout();
  }

  function openDraft(block, anchor) {
    killDraft();
    if (folded()) setFolded(false);   // 접힌 여백에 초안을 쓸 수 없다 — 새 메모를 쓰면 편다 (그대로 펴 둔다)
    cur.draftEl = block;
    cur.draftAnchor = anchor;
    syncOn();                  // 여백을 먼저 펴야 초안 카드 자리를 잴 수 있다
    block.classList.add("dn-anch-live");
    var d = document.createElement("div");
    d.className = "dn-draft";
    d.innerHTML =
      '<div class="dn-meta">새 메모<button type="button" class="dn-cancel" title="취소 (Esc)">✕</button></div>' +
      (anchor ? '<div class="dn-quote">' + esc(anchor) + "</div>" : "") +
      '<textarea class="dn-in" rows="3" placeholder="메모… (Ctrl+Enter 저장 · Esc 취소 · Ctrl+B 굵게 · Ctrl+H 형광 · Shift+Enter 줄바꿈)"></textarea>' +
      '<div class="dn-act"><button type="button" class="btn btn-sm btn-primary dn-save">저장</button></div>';
    cur.gut.appendChild(d);
    layout();
    var ta = d.querySelector(".dn-in");
    autosize(ta);
    ta.focus();
    d.scrollIntoView({ block: "nearest" });
  }

  /* 오른쪽 클릭한 자리 → (고른 글 있으면 그 글, 없으면 문단 앞머리) */
  function anchorFor(block) {
    var bw = bwin(block.ownerDocument);          // 고른 글은 **본문의 창** 선택이다 (iframe 이면 그쪽)
    var s = bw.getSelection && bw.getSelection();
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
    hostEl.classList.remove("dnote-on");    // 메모를 읽은 뒤 render() 의 syncOn 이 정한다
    hostEl.classList.remove("dnote-folded");
    if (!gut._dnFold) {                     // 머리줄 [접기 ▸ / ◂ 펴기] — gut 하나에 한 번만 단다
      gut._dnFold = true;
      gut.addEventListener("click", function (e) {
        var b = e.target && e.target.closest && e.target.closest(".dn-fold");
        if (!b) return;
        e.preventDefault(); e.stopPropagation();
        toggleFold();
      });
    }
    cur = { body: bodyEl, rel: rel, host: hostEl, gut: gut,
            notes: [], map: {}, draftEl: null, draftAnchor: "",
            pens: [], penOn: false, penColor: "yellow",
            notesMode: "local", pensMode: "local", notesCorrupt: null, pensCorrupt: null };
    /* 본문이 iframe 안이면 (머리 주석) — 오른쪽 클릭 · Esc 는 그 문서에서 나고, 칠할 표시의 CSS 는 그 문서에 있어야 한다.
     * ⚠ CSS 를 먼저 옮긴다: 아래 load() 가 그리는 형광펜이 처음부터 보이게. */
    var bd = bodyEl.ownerDocument;
    if (bd && bd !== document) {
      cur.frameDoc = bd;
      cur.bodyCssN = shareBodyCss(bd);
      bd.addEventListener("contextmenu", onContext);
      bd.addEventListener("keydown", onEsc, true);
    }
    gut.innerHTML = '<div class="dn-h">📝 메모</div>';
    load();
    loadPens();
    paintPenBtn();
    // 형광펜: 켜져 있을 때만 드래그가 칠한다. 꺼져 있으면 평소처럼 글이 선택될 뿐이다
    //   — 읽다가 실수로 칠하는 사고를 막으려고 **기본은 꺼짐**이다.
    bodyEl.addEventListener("mouseup", function () {
      if (!cur || !cur.penOn) return;
      var sel = bwin(bodyEl.ownerDocument).getSelection();   // 본문의 창 선택 (iframe 이면 그쪽)
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
    //   ⚠ 관찰자는 **본문의 창** 것을 쓴다 — iframe 안 원소는 그 문서의 렌더 갱신에서 잰다 (같은 문서면 이 창 것이다).
    var RO = bwin(bd).ResizeObserver || global.ResizeObserver;
    if (RO) {
      cur.ro = new RO(function () { layout(); });
      cur.ro.observe(bodyEl);
    }
  };

  global.unmountDocNotes = function () {
    if (!cur) return;
    if (cur.ro) cur.ro.disconnect();
    clearHl();
    if (cur.frameDoc) {                     // iframe 문서에 건 것을 거둔다 (옮긴 CSS 는 남긴다 — 다시 달면 그대로 쓴다)
      cur.frameDoc.removeEventListener("contextmenu", onContext);
      cur.frameDoc.removeEventListener("keydown", onEsc, true);
      if (cur.frameDoc.body) cur.frameDoc.body.classList.remove("dn-pen-on");
    }
    if (cur.host) { cur.host.classList.remove("dnote-on"); cur.host.classList.remove("dnote-folded"); }
    if (cur.gut && cur.gut.parentNode) cur.gut.parentNode.removeChild(cur.gut);
    cur = null;
    document.body.classList.remove("dn-pen-on");
    var pb = document.getElementById("docpen");
    if (pb) { pb.classList.remove("on"); pb.textContent = "🖍 형광"; }
  };

  global.docNoteLayout = layout;

  /* ── 이벤트 (문서에 한 번만) ───────────────────────────────────────────── */

  /* 오른쪽 클릭 · Esc 는 이름 붙인 함수다 — 본문이 iframe 이면 mount 가 그 문서에도 같은 함수를 걸고
   * unmount 가 거둔다 (이 창 document 에는 늘 한 번 걸려 있다). */
  function onContext(e) {
    if (!cur) return;
    if (!cur.body.contains(e.target)) return;
    var block = e.target.closest && e.target.closest(BLOCKS);
    if (!block || !cur.body.contains(block)) return;
    if (block.closest(".figstrip") || block.closest(".figpane")) return;  // 그림은 💬 담당
    e.preventDefault();
    openDraft(block, anchorFor(block));
  }
  document.addEventListener("contextmenu", onContext);

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
    /* ⤢ — 카드를 **자리는 그대로 둔 채** 넓게 편다 (1저자 2026-08-28: "확장시킬 수 있거나").
     * 자리를 옮기지 않는 이유: 카드의 세로 위치가 곧 "본문 어느 줄 메모인가" 다.
     * 옮기면 그 뜻이 사라진다 — 넓히는 건 그 뜻을 안 건드리고 읽기만 해결한다. */
    if (e.target.closest(".dn-expand")) {
      var wc = e.target.closest(".dn-card");
      wc.classList.toggle("dn-wide");
      layout();
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
      noteWrite(storeRead("notes", cur.rel).items.filter(function (n) { return n.id !== nid; }));
      load();
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
  function onEsc(e) {
    if (!cur || e.key !== "Escape") return;
    if (cur.gut && cur.gut.querySelector(".dn-draft")) {
      e.stopPropagation(); e.preventDefault(); killDraft(); return;
    }
    if (editing()) { e.stopPropagation(); e.preventDefault(); closeEdit(); }
  }
  document.addEventListener("keydown", onEsc, true);

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
