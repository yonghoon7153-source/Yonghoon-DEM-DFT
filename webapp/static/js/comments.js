/* comments.js — 파일·그림에 코멘트 (Notion 식 💬N).
 *
 * 1저자 요청(2026-08-06): "files나 figure 사진 확대하면 comment 적어놓을 수 있게".
 * 그림을 보다가 든 판단("이 줄무늬는 아티팩트 의심", "이 축은 log")을 그 파일 옆에
 * 붙여 둔다. 서버가 db/file_comments.json 에 저장하므로 세션·머신이 바뀌어도 남는다.
 *
 *   mountComments(el, rel)  — el 안에 코멘트 패널을 그린다 (미리보기 모달·라이트박스용)
 *   paintBadge(rel, n)      — 카드의 💬 배지 숫자 갱신
 */
(function (global) {
  "use strict";

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  /* 카드에 붙은 배지들을 갱신 — 목록을 다시 안 그려도 숫자가 맞는다 */
  function paintBadge(rel, n) {
    document.querySelectorAll('[data-cbadge="' + (window.CSS && CSS.escape
      ? CSS.escape(rel) : rel.replace(/"/g, '\\"')) + '"]').forEach(function (b) {
      b.textContent = "💬 " + n;
      b.style.display = n ? "" : "none";
    });
  }

  function render(box, rel, items) {
    var list = items.map(function (c) {
      return '<div class="cmt-i" data-cid="' + esc(c.id) + '">' +
        '<div class="cmt-meta">' + esc(c.at) + (c.who ? " · " + esc(c.who) : "") +
        '<button type="button" class="cmt-del" title="삭제">✕</button></div>' +
        '<div class="cmt-t">' + esc(c.text) + "</div></div>";
    }).join("");
    box.innerHTML =
      '<div class="cmt-h">💬 코멘트 <span class="muted">' + items.length + "</span></div>" +
      '<div class="cmt-list">' + (list ||
        '<div class="muted" style="font-size:.76rem">아직 없어요 — 이 파일을 보다가 든 판단을 남겨두면 다음에 열 때 같이 보여요.</div>') +
      "</div>" +
      '<div class="cmt-new"><textarea class="cmt-in" rows="2" ' +
      'placeholder="코멘트… (Ctrl+Enter 로 등록)"></textarea>' +
      '<button type="button" class="btn sm cmt-add">등록</button></div>';
    paintBadge(rel, items.length);
  }

  function load(box, rel) {
    fetch("/api/comments/" + encodeURI(rel))
      .then(function (r) { return r.json(); })
      .then(function (d) { render(box, rel, d.items || []); })
      .catch(function () {
        box.innerHTML = '<div class="muted" style="font-size:.76rem">코멘트를 못 불러왔어요</div>';
      });
  }

  function post(box, rel, text) {
    if (!text.trim()) return;
    fetch("/api/comments/" + encodeURI(rel), {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text })
    }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (x) {
        if (!x.ok) { alert("⛔ " + (x.d.error || "실패")); return; }
        load(box, rel);
      })
      .catch(function () { alert("⛔ 통신 실패"); });
  }

  global.mountComments = function (el, rel) {
    if (!el || !rel) return;
    var box = el.querySelector(".cmt");
    if (!box) {
      box = document.createElement("div");
      box.className = "cmt";
      el.appendChild(box);
    }
    box.dataset.rel = rel;
    box.innerHTML = '<div class="muted" style="font-size:.76rem">불러오는 중…</div>';
    load(box, rel);
  };
  global.paintCommentBadge = paintBadge;

  /* 이벤트는 문서에 한 번만 — 패널이 다시 그려져도 계속 먹는다 */
  document.addEventListener("click", function (e) {
    var box = e.target.closest && e.target.closest(".cmt");
    if (!box) return;
    var rel = box.dataset.rel;
    if (e.target.closest(".cmt-add")) {
      var ta = box.querySelector(".cmt-in");
      post(box, rel, ta.value); ta.value = "";
      return;
    }
    var del = e.target.closest(".cmt-del");
    if (del) {
      var cid = del.closest(".cmt-i").dataset.cid;
      if (!confirm("이 코멘트를 지울까요?")) return;
      fetch("/api/comments/" + encodeURI(rel) + "?id=" + encodeURIComponent(cid),
            { method: "DELETE" })
        .then(function () { load(box, rel); })
        .catch(function () { alert("⛔ 통신 실패"); });
    }
  });

  document.addEventListener("keydown", function (e) {
    if (!(e.ctrlKey || e.metaKey) || e.key !== "Enter") return;
    var ta = e.target.closest && e.target.closest(".cmt-in");
    if (!ta) return;
    e.preventDefault();
    var box = ta.closest(".cmt");
    post(box, box.dataset.rel, ta.value); ta.value = "";
  });
})(window);
