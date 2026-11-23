/* boot.js — 테마 초기화 + 사이드바 토글.
 *
 * ⚠ 인라인 <script> 를 쓰지 않는다: 이 앱의 CSP 는 script-src 'self' 라 인라인이 막힌다.
 *   테마는 <head> 에서 **동기로** 불러 페인트 전에 data-theme 을 정한다 (FOUC 방지).
 *   그래서 이 파일은 defer 가 아니고, 여기 있는 코드는 짧아야 한다 — 팔레트·스크롤스파이
 *   같은 나머지는 app.js 가 defer 로 가져간다.
 *
 *   테마 선택은 이 브라우저에만 둔다(localStorage). 서버는 아무것도 저장하지 않는다.
 */
(function () {
  "use strict";

  try {
    var t = localStorage.getItem("theme");
    if (t === "dark" || t === "light") document.documentElement.setAttribute("data-theme", t);
  } catch (e) { /* localStorage 가 막힌 브라우저 — 기본(시스템) 테마로 둔다 */ }

  function eff() {
    var e = document.documentElement.getAttribute("data-theme");
    if (e) return e;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function sync() {
    var dark = eff() === "dark";
    var use = document.getElementById("tt-use");
    var lab = document.querySelector(".tt-label");
    // 아이콘은 스프라이트의 symbol 을 갈아 끼운다 (아이콘 폰트도 CDN 도 못 쓴다)
    if (use) use.setAttribute("href", dark ? "#i-sun" : "#i-moon");
    if (lab) lab.textContent = dark ? "라이트 모드" : "다크 모드";
  }

  function nav(open) {
    var btn = document.getElementById("menubtn");
    var veil = document.getElementById("navveil");
    document.body.classList.toggle("nav-open", open);
    if (btn) btn.setAttribute("aria-expanded", String(open));
    if (veil) veil.hidden = !open;
  }

  document.addEventListener("DOMContentLoaded", function () {
    sync();

    var tb = document.getElementById("themebtn");
    if (tb) tb.addEventListener("click", function () {
      var n = eff() === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", n);
      try { localStorage.setItem("theme", n); } catch (e) {}
      sync();
    });

    var mb = document.getElementById("menubtn");
    if (mb) mb.addEventListener("click", function () {
      nav(!document.body.classList.contains("nav-open"));
    });
    var veil = document.getElementById("navveil");
    if (veil) veil.addEventListener("click", function () { nav(false); });

    // 좁은 화면에서 메뉴로 이동하면 서랍을 닫는다 (안 닫으면 도착한 화면이 가려진다)
    var side = document.getElementById("sidebar");
    if (side) side.addEventListener("click", function (e) {
      if (e.target.closest && e.target.closest("a")) nav(false);
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") nav(false);
  });
})();
