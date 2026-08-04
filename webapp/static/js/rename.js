/* rename.js — 첨부 카드의 ✏ 로 파일 이름 바꾸기 (개념 문서 · /files 공용).
 *
 * 1저자 요청(2026-08-06): 업로드한 한글 파일이 `pmf______.pdf` 처럼 뭉개져 있어서
 * 화면에서 바로 고치고 싶다. (뭉개진 원인 자체 — 업로드 시 [A-Za-z0-9._-] 강제 —
 * 은 data.safe_filename 에서 고쳤다. 이건 이미 들어와 있는 것들 정리용.)
 *
 * 서버(/api/file-rename)가 파일을 옮기고 **문서에 적힌 경로도 같이** 고친다.
 * `docs/uploads/` 밖은 서버가 거절한다 — repo 산출물은 도구가 같은 이름으로 다시
 * 만들어 두 벌이 되기 때문. 그래서 버튼 자체도 업로드 파일에만 붙는다.
 */
(function () {
  "use strict";

  function ask(card, btn) {
    var cur = card.dataset.name || "";
    var dot = cur.lastIndexOf(".");
    var stem = dot > 0 ? cur.slice(0, dot) : cur;      // 확장자는 빼고 물어본다
    var next = window.prompt("새 이름 (확장자는 빼도 돼요)", stem);
    if (next === null) return;
    next = next.trim();
    if (!next || next === stem || next === cur) return;

    var old = btn.textContent;
    btn.disabled = true;
    btn.textContent = "…";
    fetch("/api/file-rename", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rel: card.dataset.rel, name: next })
    })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (x) {
        if (!x.ok) throw new Error(x.d.error || "실패");
        location.reload();          // 목록은 본문/디스크에서 다시 수집한다
      })
      .catch(function (e) {
        alert("⛔ " + (e.message || "통신 실패"));
        btn.disabled = false;
        btn.textContent = old;
      });
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest(".att-rn");
    if (!btn) return;
    var card = btn.closest(".att-card");
    if (!card) return;
    e.stopPropagation();            // 카드 클릭(미리보기 열기)과 겹치지 않게
    e.preventDefault();
    ask(card, btn);
  }, true);                         // ⚠ 캡처 단계 — 카드의 click 리스너보다 먼저 잡는다
})();
