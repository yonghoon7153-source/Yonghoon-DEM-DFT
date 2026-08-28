/* comments.js — 파일·그림·문헌에 코멘트 (Notion 식 💬N).
 *
 * 1저자 요청(2026-08-06): "files나 figure 사진 확대하면 comment 적어놓을 수 있게".
 * 그림을 보다가 든 판단("이 줄무늬는 아티팩트 의심", "이 축은 log")을 그 파일 옆에
 * 붙여 둔다. 서버가 db/file_comments.json 에 저장하므로 세션·머신이 바뀌어도 남는다.
 *
 *   mountComments(el, rel)  — el 안에 코멘트 패널을 그린다 (미리보기 모달·라이트박스용)
 *   paintBadge(rel, n)      — 카드의 💬 배지 숫자 갱신
 *   window.noteFmt          — 메모·코멘트가 **함께 쓰는** 글 서식 (아래 참조)
 *
 * ⛔⛔ 2026-08-28 — 서식 함수(inline/autosize/wrapSel)를 **여기로 옮겼다.**
 *   원래 docnote.js(본문 여백 메모)에만 있어서, 문헌 코멘트는 `**87.2%**` 가
 *   별표째 보였다(1저자 신고). 각자 사본을 두면 오늘 이미 두 번 겪은 "같은 규약의
 *   두 경로"가 된다 — 이 파일은 base.html 이 **모든 페이지**에 싣고 docnote.js 는
 *   일부 페이지에만 실리므로, **여기가 유일한 집**이고 docnote.js 가 가져다 쓴다.
 */
(function (global) {
  "use strict";

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  /* 붙여넣은 그림만 <img> 로 편다. **우리가 저장한 이름 규격**(해시 32자 + 확장자)만
   * 허용한다 — 임의 URL 을 허용하면 메모 한 줄로 외부 요청을 만들 수 있다. */
  var IMG_SRC = /^\/api\/note-image\/[0-9a-f]{32}\.(?:png|jpg|gif|webp)$/;

  /* 메모·코멘트의 아주 작은 인라인 서식. **esc 뒤에** 돌린다 — 순서가 뒤집히면 HTML 주입이다.
   * `code` 를 먼저 처리해 그 안의 별표가 굵게 먹지 않게 한다.
   * ⛔ 못 하는 것: 블록 문법(목록·표·제목)은 없다. 여기는 메모지 문서가 아니다. */
  function inline(s) {
    return esc(s)
      .replace(/`([^`\n]+)`/g, "<code>$1</code>")
      .replace(/!\[([^\]\n]*)\]\(([^)\s]+)\)/g, function (m, alt, src) {
        if (!IMG_SRC.test(src)) return m;      // 규격 밖 URL 은 **글자 그대로** 둔다
        return '<img class="note-img" src="' + src + '" alt="' + alt + '" loading="lazy">';
      })
      .replace(/\*\*([^*\n]+)\*\*/g, "<b>$1</b>")
      .replace(/==([^=\n]+)==/g, '<mark class="dn-penmk">$1</mark>');
  }

  /* 입력창을 내용에 맞춰 늘린다 (1저자 2026-08-27: "수정할 때 창이 작아져서 불편해").
   * 카드에 보이던 글이 rows=3 상자로 눌려서, 고치려고 열면 오히려 **덜 보였다** —
   * 읽을 때보다 고칠 때 더 안 보이는 건 거꾸로다.
   * 화면 높이의 55 % 를 넘지는 않는다 (그 위로는 상자 안에서 스크롤한다).
   * ⚠ 여백 메모에서는 높이가 바뀌면 배치가 어긋나므로 **호출한 쪽이 layout() 을 같이 부른다.** */
  function autosize(ta) {
    if (!ta) return;
    ta.style.height = "auto";
    var max = Math.round((global.innerHeight || 800) * 0.55);
    ta.style.height = Math.min(ta.scrollHeight + 2, max) + "px";
  }

  /* textarea 선택 영역을 표시로 감싼다/벗긴다 (Ctrl+B). 선택이 없으면 커서 자리에
   * 빈 표시를 넣고 그 안으로 커서를 옮긴다 — 워드에서 굵게를 먼저 켜는 것과 같다. */
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

  /* 커서 자리에 글을 끼워 넣는다 (그림 붙여넣기용) */
  function insertAt(ta, txt) {
    var a = ta.selectionStart, b = ta.selectionEnd;
    ta.value = ta.value.slice(0, a) + txt + ta.value.slice(b);
    ta.setSelectionRange(a + txt.length, a + txt.length);
    autosize(ta);
  }

  /* 클립보드·드래그의 그림을 올리고 `![](url)` 을 커서 자리에 넣는다.
   * ⛔ 못 하는 것: 여러 장을 병렬로 올리지 않는다(순서가 섞이면 어느 그림인지 모른다). */
  function uploadImage(file, ta, done) {
    var fd = new FormData();
    fd.append("file", file);
    ta.disabled = true;
    fetch("/api/note-image", { method: "POST", body: fd })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (x) {
        ta.disabled = false;
        if (!x.ok) { alert("⛔ " + (x.d.error || "그림 업로드 실패")); return; }
        insertAt(ta, "![](" + x.d.url + ")\n");
        ta.focus();
        if (done) done();
      })
      .catch(function () { ta.disabled = false; alert("⛔ 그림 업로드 통신 실패"); });
  }

  /* 붙여넣기·드롭 이벤트에서 그림 파일을 꺼낸다. 없으면 null (그러면 기본 동작에 맡긴다). */
  function imageFrom(e) {
    var dt = e.clipboardData || e.dataTransfer;
    if (!dt) return null;
    var items = dt.items || [];
    for (var i = 0; i < items.length; i++) {
      if (items[i].kind === "file" && /^image\//.test(items[i].type)) {
        var f = items[i].getAsFile();
        if (f) return f;
      }
    }
    var fs = dt.files || [];
    for (var j = 0; j < fs.length; j++) {
      if (/^image\//.test(fs[j].type)) return fs[j];
    }
    return null;
  }

  /* 붙여넣은 그림을 눌러 크게 본다 (1저자 2026-08-28: "사진 눌러도 zoom 안 된다").
   * 카드 안에서는 폭·높이를 잘라 두기 때문에(다른 메모를 밀어내지 않으려고) **원본을 볼
   * 길이 따로 있어야 한다.** 기존 `.modal`/`.modal-body` 규약을 그대로 쓴다 — 새 껍데기를
   * 만들면 닫기·배경막·z-index 규칙이 두 벌이 된다.
   * ⛔ 못 하는 것: 확대·축소 단계가 없다. 원본 크기로 한 번 보여줄 뿐이다
   *   (그림 팝업의 figref Zoom 과 달리 여기 그림은 캡처라 대개 그걸로 충분하다). */
  function openImage(src, alt) {
    var m = document.getElementById("noteimg-lb");
    if (!m) {
      m = document.createElement("div");
      m.id = "noteimg-lb";
      m.className = "modal";
      m.innerHTML = '<div class="modal-body"><img alt=""></div>';
      document.body.appendChild(m);
      m.addEventListener("click", function (e) {
        // 그림 자체를 누른 게 아니면 닫는다 (배경막 어디를 눌러도 닫히게)
        if (!e.target.closest("img")) m.classList.remove("open");
      });
    }
    var img = m.querySelector("img");
    img.src = src;
    img.alt = alt || "";
    m.classList.add("open");
  }
  document.addEventListener("click", function (e) {
    var im = e.target.closest && e.target.closest(".note-img");
    if (!im) return;
    e.preventDefault();
    e.stopPropagation();          // ⚠ 메모 카드의 "눌러서 고치기" 가 같이 열리면 안 된다
    openImage(im.getAttribute("src"), im.getAttribute("alt"));
  }, true);
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var m = document.getElementById("noteimg-lb");
    if (m && m.classList.contains("open")) { m.classList.remove("open"); e.stopPropagation(); }
  }, true);

  /* ⚠ 이 묶음이 **정본**이다. docnote.js 는 자기 사본을 두지 않고 여기를 부른다. */
  global.noteFmt = {
    esc: esc, inline: inline, autosize: autosize, wrapSel: wrapSel,
    insertAt: insertAt, uploadImage: uploadImage, imageFrom: imageFrom,
    IMG_SRC: IMG_SRC
  };

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
        '<button type="button" class="cmt-edit" title="수정">✎</button>' +
        '<button type="button" class="cmt-del" title="삭제">✕</button></div>' +
        // ⚠ 원문을 data-raw 에 함께 실어둔다 — 수정 상자를 열 때 **서버를 다시 안 부른다**.
        //   (다시 부르면 방금 쓴 글이 아직 안 보이는 순간이 생긴다)
        '<div class="cmt-t" data-raw="' + esc(c.text) + '">' + inline(c.text) + "</div></div>";
    }).join("");
    box.innerHTML =
      '<div class="cmt-h">💬 코멘트 <span class="muted">' + items.length + "</span></div>" +
      '<div class="cmt-list">' + (list ||
        '<div class="muted" style="font-size:.76rem">아직 없어요 — 이 파일을 보다가 든 판단을 남겨두면 다음에 열 때 같이 보여요.</div>') +
      "</div>" +
      '<div class="cmt-new"><textarea class="cmt-in" rows="2" ' +
      'placeholder="코멘트… **굵게** Ctrl+B · 그림은 붙여넣기(Ctrl+V) · Ctrl+Enter 로 등록"></textarea>' +
      '<button type="button" class="btn sm cmt-add">등록</button></div>';
    paintBadge(rel, items.length);
  }

  /* /literature 카드의 검색 색인(data-cmt)을 방금 단 코멘트로 갱신.
   * 그 값은 페이지가 그려질 때 서버가 구워 넣은 것이라, 새로고침 전엔 방금 쓴 글로
   * 검색해도 💬 배지가 안 떴다 (1저자 신고 2026-08-06). 서버가 최신 색인을 같이 준다.
   *
   * ⚠ docnote.js(본문 여백 메모)도 **이 함수를 쓴다** — window.syncPaperCmtIndex 로
   *   내보낸다. 색인 갱신 규칙이 두 벌이 되면 한쪽만 고쳐져 검색이 어긋난다. */
  function syncPaperIndex(d) {
    if (!d || !d.paper || !d.paper.slug) return;
    var sel = window.CSS && CSS.escape ? CSS.escape(d.paper.slug)
                                       : d.paper.slug.replace(/"/g, '\\"');
    var card = document.querySelector('.paper[data-id="' + sel + '"]');
    if (!card) return;
    if (d.paper.cmt) card.setAttribute("data-cmt", d.paper.cmt);
    else card.removeAttribute("data-cmt");
    // 검색 중이면 배지가 바로 뜨게 다시 거른다 (/literature 에만 있는 함수)
    if (document.getElementById("plist") && typeof window.apply === "function") window.apply();
  }

  function load(box, rel) {
    fetch("/api/comments/" + encodeURI(rel))
      .then(function (r) { return r.json(); })
      .then(function (d) { render(box, rel, d.items || []); syncPaperIndex(d); })
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

  /* 수정 저장 — PATCH. 서버(edit_file_comment)가 이미 있었는데 UI 가 없었다. */
  function patch(box, rel, cid, text) {
    fetch("/api/comments/" + encodeURI(rel), {
      method: "PATCH", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: cid, text: text })
    }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (x) {
        if (!x.ok) { alert("⛔ " + (x.d.error || "수정 실패")); return; }
        load(box, rel);
      })
      .catch(function () { alert("⛔ 통신 실패"); });
  }

  /* 코멘트 하나를 수정 상자로 바꾼다. 원문은 data-raw 에 이미 있다. */
  function openEdit(item) {
    if (item.querySelector(".cmt-ed")) return;
    var t = item.querySelector(".cmt-t");
    var raw = t.getAttribute("data-raw") || "";
    var ed = document.createElement("div");
    ed.className = "cmt-ed";
    ed.innerHTML = '<textarea class="cmt-in cmt-edin"></textarea>' +
      '<div class="cmt-edbtns"><button type="button" class="btn sm cmt-save">저장</button>' +
      '<button type="button" class="btn sm ghost cmt-cancel">취소</button></div>';
    t.style.display = "none";
    item.appendChild(ed);
    var ta = ed.querySelector("textarea");
    ta.value = raw;
    autosize(ta);                       // 열자마자 글이 다 보이게 (2026-08-27 교훈)
    ta.focus();
    ta.setSelectionRange(raw.length, raw.length);
  }

  function closeEdit(item) {
    var ed = item.querySelector(".cmt-ed");
    if (ed) ed.remove();
    var t = item.querySelector(".cmt-t");
    if (t) t.style.display = "";
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
  global.syncPaperCmtIndex = syncPaperIndex;   // docnote.js 와 **같은** 색인 갱신을 쓴다

  /* 이벤트는 문서에 한 번만 — 패널이 다시 그려져도 계속 먹는다 */
  document.addEventListener("click", function (e) {
    var box = e.target.closest && e.target.closest(".cmt");
    if (!box) return;
    var rel = box.dataset.rel;
    if (e.target.closest(".cmt-add")) {
      var ta = box.querySelector(".cmt-new .cmt-in");
      post(box, rel, ta.value); ta.value = ""; autosize(ta);
      return;
    }
    var item = e.target.closest(".cmt-i");
    if (e.target.closest(".cmt-edit")) { openEdit(item); return; }
    if (e.target.closest(".cmt-cancel")) { closeEdit(item); return; }
    if (e.target.closest(".cmt-save")) {
      patch(box, rel, item.dataset.cid, item.querySelector(".cmt-edin").value);
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
    var ta = e.target.closest && e.target.closest(".cmt-in");
    if (!ta) return;
    // Ctrl+B — 굵게 (여백 메모와 같은 조작. 두 곳이 다르면 손이 헷갈린다)
    if ((e.ctrlKey || e.metaKey) && (e.key === "b" || e.key === "B")) {
      e.preventDefault();
      wrapSel(ta, "**");
      return;
    }
    if (!(e.ctrlKey || e.metaKey) || e.key !== "Enter") return;
    e.preventDefault();
    var box = ta.closest(".cmt");
    var item = ta.closest(".cmt-i");
    if (item) {                          // 수정 중이면 저장
      patch(box, box.dataset.rel, item.dataset.cid, ta.value);
      return;
    }
    post(box, box.dataset.rel, ta.value); ta.value = ""; autosize(ta);
  });

  /* 입력 중 상자가 따라 늘어난다 */
  document.addEventListener("input", function (e) {
    var ta = e.target.closest && e.target.closest(".cmt-in");
    if (ta) autosize(ta);      // .dn-in 은 docnote.js 가 layout() 과 함께 처리한다
  });

  /* 그림 붙여넣기(Ctrl+V) · 끌어놓기 — 캡처를 코멘트/메모에 바로 붙인다.
   * ⚠ **코멘트(.cmt-in)와 여백 메모(.dn-in) 둘 다** 받는다. 한쪽만 되면 손이 헷갈린다.
   *   메모 쪽은 상자가 늘어나면 여백 카드 배치가 어긋나므로 layout() 을 같이 부른다. */
  var NOTE_TA = ".cmt-in, .dn-in";

  function afterGrow() {
    if (typeof global.docNoteLayout === "function") global.docNoteLayout();
  }

  function onImage(e) {
    var ta = e.target.closest && e.target.closest(NOTE_TA);
    if (!ta) return;
    var f = imageFrom(e);
    if (!f) return;                      // 그림이 아니면 기본 동작(글 붙여넣기)에 맡긴다
    e.preventDefault();
    uploadImage(f, ta, afterGrow);
  }
  document.addEventListener("paste", onImage);
  document.addEventListener("drop", onImage);
  document.addEventListener("dragover", function (e) {
    if (e.target.closest && e.target.closest(NOTE_TA)) e.preventDefault();
  });
})(window);
