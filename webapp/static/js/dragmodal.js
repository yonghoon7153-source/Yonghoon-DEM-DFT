/* dragmodal.js — 모달 창을 제목줄로 끌어 옮긴다 (모든 .modal 공통).
 *
 * 1저자 요청(2026-08-06): digest 창 옆에 그림 팝업을 띄워 놓고 보는데, 창이 화면
 * 한가운데 고정이라 둘이 겹친다. 제목줄을 잡아 옮길 수 있으면 나란히 놓고 읽힌다.
 *
 * .modal 은 flex 로 가운데 정렬돼 있으므로 .modal-body 에 relative 오프셋만 준다
 * (좌표계를 갈아엎지 않아 기존 레이아웃·반응형이 그대로 산다).
 * 그림 팝업은 컨테이너의 getBoundingClientRect() 를 보고 자리를 잡으므로 따라온다.
 */
(function () {
  "use strict";

  function bodyOf(el) { return el.closest ? el.closest(".modal-body") : null; }

  document.addEventListener("pointerdown", function (e) {
    var head = e.target.closest && e.target.closest(".modal-head");
    if (!head) return;
    if (e.target.closest("a,button,input,select,textarea")) return;   // 닫기 버튼 등은 제외
    var box = bodyOf(head);
    if (!box) return;
    e.preventDefault();

    var startX = e.clientX, startY = e.clientY;
    var ox = parseFloat(box.dataset.dx || 0), oy = parseFloat(box.dataset.dy || 0);
    box.classList.add("modal-dragging");

    function mv(ev) {
      var dx = ox + ev.clientX - startX, dy = oy + ev.clientY - startY;
      // 제목줄이 항상 화면 안에 남게 — 놓쳐서 못 잡는 일이 없도록
      var r = box.getBoundingClientRect();
      var maxX = window.innerWidth / 2 + r.width / 2 - 80;
      var maxY = window.innerHeight / 2 + r.height / 2 - 40;
      dx = Math.max(-maxX, Math.min(dx, maxX));
      dy = Math.max(-(window.innerHeight / 2 - r.height / 2 + 8), Math.min(dy, maxY));
      box.dataset.dx = dx; box.dataset.dy = dy;
      box.style.position = "relative";
      box.style.left = dx + "px";
      box.style.top = dy + "px";
    }
    function up() {
      window.removeEventListener("pointermove", mv);
      window.removeEventListener("pointerup", up);
      window.removeEventListener("pointercancel", up);
      box.classList.remove("modal-dragging");
    }
    // ⚠ window 에 건다 — 제목줄 밖에서 놓으면 pointerup 을 못 받아 끌기 상태가 남는다
    window.addEventListener("pointermove", mv);
    window.addEventListener("pointerup", up);
    window.addEventListener("pointercancel", up);
  }, true);

  // 제목줄 더블클릭 = 가운데로 복귀
  document.addEventListener("dblclick", function (e) {
    var head = e.target.closest && e.target.closest(".modal-head");
    if (!head) return;
    var box = bodyOf(head);
    if (!box) return;
    box.style.left = box.style.top = box.style.position = "";
    delete box.dataset.dx; delete box.dataset.dy;
  });

  // 창을 닫으면 다음에 열 때 가운데에서 시작
  document.addEventListener("click", function (e) {
    var m = e.target.closest && e.target.closest(".modal");
    if (!m || e.target !== m) return;                 // 배경 클릭 = 닫기
    m.querySelectorAll(".modal-body").forEach(function (b) {
      b.style.left = b.style.top = b.style.position = "";
      delete b.dataset.dx; delete b.dataset.dy;
    });
  });

  /* ── 창 앞뒤 순서 (윈도우식) ────────────────────────────────────────
   * 1저자 요청(2026-08-06): "digest 쪽 누르면 digest가 맨앞, fig 누르면 fig가 맨앞".
   * 기본 z 는 modal 80 < figpane 95 로 고정이라 그림 팝업이 늘 위였다.
   * 누른 창에 100 부터 올라가는 z 를 인라인으로 물려 순서를 바꾼다.
   *
   * ⚠ 모달은 화면 전체를 덮는 반투명 배경막이라, 그냥 위로 올리면 그 막이 그림
   *   팝업을 가려 다시 못 누른다. 그래서 **그림 팝업이 떠 있는 동안만** 모달을
   *   '창 모드'(.modal-win: 막 투명 + pointer-events 해제)로 바꾼다 — 두 창이
   *   나란히 살아 있고, 팝업을 닫으면 원래의 어두운 모달로 돌아온다. */
  var ZTOP = 100;

  function paneOpen() {                    // 고정(pinned)된 팝업만 '창'으로 친다
    var p = document.querySelector(".figpane.figpane-pinned");
    // ⚠ offsetParent 로 판정하면 안 된다 — position:fixed 는 항상 null 이라 늘 '닫힘'이 된다
    return !!(p && p.getClientRects().length);
  }
  function sync() {
    var on = paneOpen();
    document.querySelectorAll(".modal.open").forEach(function (m) {
      m.classList.toggle("modal-win", on);
      if (!on) m.style.zIndex = "";        // 팝업이 없으면 기본 층으로 되돌린다
    });
  }
  function focusWin(el) {
    if (!el) return;
    if (+el.style.zIndex === ZTOP) return;             // 이미 맨 앞
    el.style.zIndex = ++ZTOP;
    sync();
  }

  document.addEventListener("pointerdown", function (e) {
    if (!e.target.closest) return;
    var pane = e.target.closest(".figpane");
    if (pane) { focusWin(pane); return; }
    var body = e.target.closest(".modal-body");
    if (body) focusWin(body.closest(".modal"));
  }, true);

  /* 이 창이 맨 앞인가 — 그림 팝업이 digest 뒤에 완전히 가려졌을 때
     Fig 링크를 다시 누르면 '닫기'가 아니라 '앞으로'가 되게 하려고 쓴다 */
  function isTop(el) {
    var z = +(el.style.zIndex || 0), top = true;
    document.querySelectorAll(".modal.open").forEach(function (m) {
      if (+(m.style.zIndex || 0) > z) top = false;
    });
    return top;
  }

  window.winFocus = focusWin;
  window.winSync = sync;
  window.winIsTop = isTop;
})();
