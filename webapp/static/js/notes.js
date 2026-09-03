/* notes.js — 메모 모아보기
   ==========================================================================
   문서마다 흩어진 하이라이트·메모를 한 화면에 모은다.

   ⚠ 서버는 메모를 하나도 모른다. 저장소는 `localStorage` 의
     `bms.annot.<slug>` 키들이고, 서버가 준 것은 slug → 제목·URL 이름표뿐이다
     (`#note-docs`). 그래서 이 파일이 하는 일은 셋이다: **모으기 · 거르기 ·
     묶기.**

   설계 전제
   1. **이름표가 없어도 카드를 버리지 않는다.** 문서가 지워졌거나 이름이
      바뀌었으면 slug 를 그대로 보여 주고 "지금 위키에 없는 문서" 라고 적는다.
      메모는 사람이 쓴 것이라 조용히 사라지면 안 된다.
   2. **날짜로 묶는다.** `made` 는 "YYYY-MM-DD HH:MM" 이고 앞 10자가 날짜다.
      날짜가 없는 낡은 기록은 맨 뒤 `날짜 없음` 묶음으로 간다.
   3. **거르면 빈 날짜 묶음은 통째로 숨긴다.** 안 그러면 날짜 머리만 줄줄이
      남아 결과가 있는 것처럼 보인다.
   ========================================================================== */
(function () {
  var groupsEl = document.getElementById("nh-groups");
  if (!groupsEl) return;                       // 이 화면이 아니다

  var barEl = document.getElementById("nh-bar");
  var emptyEl = document.getElementById("nh-empty");
  var noneEl = document.getElementById("nh-none");
  var qEl = document.getElementById("nh-q");

  var PREFIX = "bms.annot.";
  var HUES = { y: "노랑", g: "초록", p: "보라", r: "빨강" };
  var DOCS = (function () {
    var s = document.getElementById("note-docs");
    try { return JSON.parse(s ? s.textContent : "{}") || {}; }
    catch (e) { return {}; }
  })();

  /* ── 모으기 ───────────────────────────────────────────────────────────
     localStorage 를 훑어 우리 접두사를 가진 키만 편다. 사설 창·저장 차단이면
     접근 자체가 던지므로 통째로 감싼다 (기능만 죽고 화면은 산다). */
  function collect() {
    var out = [];
    var keys = [];
    try {
      for (var i = 0; i < localStorage.length; i++) {
        var k = localStorage.key(i);
        if (k && k.indexOf(PREFIX) === 0) keys.push(k);
      }
    } catch (e) { return out; }

    keys.forEach(function (k) {
      var slug = k.slice(PREFIX.length);
      var list;
      try { list = JSON.parse(localStorage.getItem(k) || "[]"); }
      catch (e) { return; }                    // 깨진 항목 하나가 전체를 막지 않는다
      if (!Array.isArray(list)) return;
      var doc = DOCS[slug];
      list.forEach(function (a) {
        if (!a || !a.text) return;
        out.push({
          slug: slug,
          title: doc ? doc.t : slug,
          url: doc ? doc.u : null,             // null = 지금 위키에 없는 문서
          id: a.id, hue: a.hue || "y", note: a.note || "",
          text: String(a.text), sec: a.sec || "",
          made: a.made || ""
        });
      });
    });

    // 최신순. 날짜 없는 것은 뒤로 (빈 문자열이 가장 작다)
    out.sort(function (x, y) { return x.made < y.made ? 1 : x.made > y.made ? -1 : 0; });
    return out;
  }

  /* ── 그리기 ─────────────────────────────────────────────────────────── */
  function card(a) {
    // 문서가 없으면 링크가 아니라 <div> 다 — 갈 곳 없는 링크를 주지 않는다
    var el = document.createElement(a.url ? "a" : "div");
    el.className = "nh-card hl-" + a.hue + (a.note ? " has-note" : "") +
                   (a.url ? "" : " is-orphan");
    if (a.url) el.href = a.url + "?note=" + encodeURIComponent(a.id);
    el.setAttribute("data-hue", a.hue);
    el.setAttribute("data-has-note", a.note ? "1" : "");
    el.setAttribute("data-s",
      (a.text + " " + a.note + " " + a.title + " " + a.slug).toLowerCase());

    var head = document.createElement("div");
    head.className = "nh-head";
    var doc = document.createElement("span");
    doc.className = "nh-doc";
    doc.textContent = a.title;
    head.appendChild(doc);
    if (!a.url) {
      var warn = document.createElement("span");
      warn.className = "nh-orphan";
      warn.textContent = "지금 위키에 없는 문서";
      head.appendChild(warn);
    }
    var when = document.createElement("time");
    when.className = "nh-when";
    when.textContent = a.made || "";
    head.appendChild(when);
    el.appendChild(head);

    var q = document.createElement("blockquote");
    q.className = "nh-quote";
    q.textContent = a.text.length > 260 ? a.text.slice(0, 260) + "…" : a.text;
    el.appendChild(q);

    if (a.note) {
      var p = document.createElement("p");
      p.className = "nh-note-t";
      p.textContent = a.note;
      el.appendChild(p);
    }

    if (a.sec) {
      var s = document.createElement("span");
      s.className = "nh-sec mono";
      s.textContent = "#" + a.sec;
      el.appendChild(s);
    }
    return el;
  }

  function render(items) {
    groupsEl.textContent = "";
    var order = [], byDay = {};
    items.forEach(function (a) {
      var d = a.made ? a.made.slice(0, 10) : "";
      if (!byDay[d]) { byDay[d] = []; order.push(d); }
      byDay[d].push(a);
    });
    order.forEach(function (d) {
      var sec = document.createElement("section");
      sec.className = "nh-day";
      var h = document.createElement("div");
      h.className = "nh-day-h";
      var dd = document.createElement("span");
      dd.className = "nh-day-d";
      dd.textContent = d || "날짜 없음";
      var nn = document.createElement("span");
      nn.className = "nh-day-n";
      nn.textContent = byDay[d].length + "건";
      var line = document.createElement("span");
      line.className = "nh-day-line";
      h.appendChild(dd); h.appendChild(nn); h.appendChild(line);
      sec.appendChild(h);
      var wrap = document.createElement("div");
      wrap.className = "nh-list";
      byDay[d].forEach(function (a) { wrap.appendChild(card(a)); });
      sec.appendChild(wrap);
      groupsEl.appendChild(sec);
    });
  }

  /* ── 거르기 — 카드는 DOM 에 두고 숨긴다 (다시 그리면 스크롤이 튄다) ─── */
  var fKind = "all", fHue = "";

  function apply() {
    var q = (qEl && qEl.value || "").toLowerCase().trim();
    var shown = 0;
    Array.prototype.forEach.call(groupsEl.querySelectorAll(".nh-day"), function (g) {
      var seen = 0;
      Array.prototype.forEach.call(g.querySelectorAll(".nh-card"), function (c) {
        var ok = (!q || c.getAttribute("data-s").indexOf(q) >= 0)
              && (fKind !== "note" || c.getAttribute("data-has-note"))
              && (!fHue || c.getAttribute("data-hue") === fHue);
        c.hidden = !ok;
        if (ok) seen++;
      });
      g.hidden = seen === 0;                  // 빈 날짜 머리를 남기지 않는다
      shown += seen;
    });
    if (noneEl) noneEl.hidden = shown > 0;
  }

  /* ── 내보내기 — 브라우저에 갇히지 않게 ──────────────────────────────── */
  function exportAll(items) {
    var out = ["# 메모 · 하이라이트 — 전체", "",
               "이 파일은 **브라우저에 있던 개인 주석**을 내보낸 것이다. 위키의 내용이",
               "아니며 인용의 근거가 아니다. 정본은 언제나 저장소의 원문이다.", "",
               "총 " + items.length + "건 · 내보낸 때 " +
               new Date().toISOString().slice(0, 16).replace("T", " "), ""];
    var cur = null;
    items.forEach(function (a) {
      if (a.slug !== cur) {
        cur = a.slug;
        out.push("", "## " + a.title, "", "`" + a.slug + "`" +
                 (a.url ? "" : "  ⚠ 지금 위키에 없는 문서"), "");
      }
      out.push("- **" + (HUES[a.hue] || a.hue) + "**" +
               (a.sec ? "  (절 `#" + a.sec + "`)" : "") +
               (a.made ? "  — " + a.made : ""));
      a.text.split("\n").forEach(function (l) { out.push("  > " + l); });
      if (a.note) out.push("", "  " + a.note.replace(/\n/g, "\n  "));
      out.push("");
    });
    var blob = new Blob([out.join("\n")], { type: "text/markdown;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var el = document.createElement("a");
    el.href = url;
    el.download = "bms-notes-" + new Date().toISOString().slice(0, 10) + ".md";
    document.body.appendChild(el); el.click(); el.remove();
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  /* ── 시작 ─────────────────────────────────────────────────────────────── */
  var items = collect();

  if (!items.length) {
    if (emptyEl) emptyEl.hidden = false;
    return;
  }
  if (barEl) barEl.hidden = false;
  render(items);

  document.getElementById("nh-n-all").textContent = String(items.length);
  document.getElementById("nh-n-note").textContent =
    String(items.filter(function (a) { return a.note; }).length);
  Object.keys(HUES).forEach(function (h) {
    var b = document.querySelector('[data-hn="' + h + '"]');
    if (b) b.textContent = String(items.filter(function (a) { return a.hue === h; }).length);
  });

  if (qEl) qEl.addEventListener("input", apply);

  Array.prototype.forEach.call(document.querySelectorAll(".nh-f"), function (b) {
    b.addEventListener("click", function () {
      fKind = b.getAttribute("data-f");
      Array.prototype.forEach.call(document.querySelectorAll(".nh-f"), function (x) {
        x.classList.toggle("is-on", x === b);
      });
      apply();
    });
  });

  // 색 칩은 **토글**이다 — 같은 것을 다시 누르면 색 조건이 풀린다
  Array.prototype.forEach.call(document.querySelectorAll(".nh-h"), function (b) {
    b.addEventListener("click", function () {
      var h = b.getAttribute("data-hue");
      fHue = (fHue === h) ? "" : h;
      Array.prototype.forEach.call(document.querySelectorAll(".nh-h"), function (x) {
        x.classList.toggle("is-on", x.getAttribute("data-hue") === fHue);
      });
      apply();
    });
  });

  var exp = document.getElementById("nh-export");
  if (exp) exp.addEventListener("click", function () { exportAll(items); });
})();
