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
})();
