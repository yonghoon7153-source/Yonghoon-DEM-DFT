/* boot.js — 테마 초기화 + 사이드바 토글.
 *
 * ⚠ 인라인 <script> 를 쓰지 않는다: 이 앱의 CSP 는 script-src 'self' 라 인라인이 막힌다.
 *   테마는 <head> 에서 동기로 불러 **페인트 전에** data-theme 을 정한다 (FOUC 방지).
 *   테마 선택은 이 브라우저에만 둔다(localStorage) — 서버는 아무것도 저장하지 않는다.
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
    var d = eff() === "dark";
    var i = document.querySelector(".tt-icon"), l = document.querySelector(".tt-label");
    if (i) i.textContent = d ? "☀️" : "🌙";
    if (l) l.textContent = d ? "라이트 모드" : "다크 모드";
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
      var o = document.body.classList.toggle("nav-open");
      mb.setAttribute("aria-expanded", String(o));
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") document.body.classList.remove("nav-open");
  });
})();
