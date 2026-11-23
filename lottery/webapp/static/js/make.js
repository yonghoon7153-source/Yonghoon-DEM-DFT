/* make.js — 번호 생성기 (로또 6/45 · 연금복권720+).
 *
 * 추첨은 브라우저의 암호 난수(crypto.getRandomValues)로 하고, 거절 표본추출로 치우침을 없앤다.
 * 고른 번호는 어디에도 저장하거나 보내지 않는다 (서버는 읽기 전용이고 이 파일은 fetch 를 한 번,
 * 인기도 계수를 받으려고만 한다).
 *
 * ⚠ innerHTML 을 쓰지 않는다 (본체 app.js 와 같은 규칙) — 전부 createElement + textContent.
 * ⚠ 인기도 계산은 아래 <core> 구간에만 있다. tests/test_site_js.py 가 이 구간을 잘라 node 로
 *   돌리고 파이썬 popularity.score_combos 와 같은 값인지 대조한다.
 */
// <core>
function patternFeatures(c, latest) {
  var s = c.slice().sort(function (a, b) { return a - b; });
  var consec = 0, overlap = 0, i;
  for (i = 1; i < s.length; i++) if (s[i] - s[i - 1] === 1) consec++;
  for (i = 0; i < s.length; i++) if (latest.indexOf(s[i]) >= 0) overlap++;
  var col = [0, 0, 0, 0, 0, 0, 0], row = [0, 0, 0, 0, 0, 0, 0];
  for (i = 0; i < s.length; i++) { col[(s[i] - 1) % 7]++; row[Math.floor((s[i] - 1) / 7)]++; }
  return [consec, overlap, Math.max.apply(null, col), Math.max.apply(null, row)];
}
function percentileOf(eta, S) {
  var q = S.eta_percentiles, p = S.pct;
  if (eta <= q[0]) return p[0];
  if (eta >= q[q.length - 1]) return p[p.length - 1];
  var lo = 0, hi = q.length - 1;
  while (hi - lo > 1) { var mid = (lo + hi) >> 1; if (q[mid] <= eta) lo = mid; else hi = mid; }
  var span = q[hi] - q[lo];
  return span > 0 ? p[lo] + (eta - q[lo]) / span * (p[hi] - p[lo]) : p[lo];
}
function popularity(c, S) {
  var s = 0, i;
  for (i = 0; i < c.length; i++) s += S.beta[c[i] - 1];
  var f = patternFeatures(c, S.latest_numbers);
  for (i = 0; i < f.length; i++) s += f[i] * S.theta[i];
  var eta = S.gamma0 + S.gamma1 * (s - S.center);
  var mu = S.mu_avg * Math.exp(eta);
  return { eta: eta, mu: mu, share: (1 - Math.exp(-mu)) / mu, pct: percentileOf(eta, S) };
}
function comboShape(c) {
  var s = c.slice().sort(function (a, b) { return a - b; });
  var d = [], i, run = 1, maxRun = 1;
  for (i = 1; i < s.length; i++) d.push(s[i] - s[i - 1]);
  for (i = 0; i < d.length; i++) { run = d[i] === 1 ? run + 1 : 1; if (run > maxRun) maxRun = run; }
  return { arithmetic: d.every(function (x) { return x === d[0]; }), maxRun: maxRun };
}
// 세후 금액 — 동행복권 당첨자 가이드의 원천징수 세율. 200만 원 이하는 과세최저한(비과세),
// 넘으면 (당첨금 − 구입비 1,000원) 에 3억까지 22%, 3억 초과분 33%.
function afterTax(prize) {
  if (prize <= 2000000) return { tax: 0, net: prize };
  var income = prize - 1000;
  var tax = Math.floor(Math.min(income, 3e8) * 0.22 + Math.max(0, income - 3e8) * 0.33);
  return { tax: tax, net: prize - tax };
}
// 백테스트 — rounds: [회차, 번호 6개, 보너스, 1~5등 1인당 당첨금, 게임 가격].
// 같은 조합을 1회부터 매 회 1게임씩 샀다면. 'expected' 는 평균적인(무작위) 번호의 기대값이다.
var TIER_P = [1, 6, 228, 11115, 182780].map(function (k) { return k / 8145060; });
function simulate(c, rounds) {
  var out = { counts: [0, 0, 0, 0, 0], won: 0, spent: 0, expectedWon: 0, unknownFirst: 0, n: rounds.length };
  for (var r = 0; r < rounds.length; r++) {
    var d = rounds[r], m = 0, k;
    for (k = 1; k <= 6; k++) if (c.indexOf(d[k]) >= 0) m++;
    var bonus = c.indexOf(d[7]) >= 0;
    var tier = m === 6 ? 1 : m === 5 ? (bonus ? 2 : 3) : m === 4 ? 4 : m === 3 ? 5 : 0;
    if (tier) {
      out.counts[tier - 1]++;
      if (tier === 1 && d[8] === 0) out.unknownFirst++;   // 1등 없던(이월) 회차 — 금액 미기재
      else out.won += d[7 + tier];
    }
    out.spent += d[13];
    for (k = 0; k < 5; k++) out.expectedWon += TIER_P[k] * d[8 + k];
  }
  return out;
}
// </core>

(function () {
  "use strict";
  var root = document.getElementById("maker");
  if (!root) return;

  var S = null, POOL = [], PAST = {}, PPAST = {}, LATEST = 0, ROUNDS = [];
  var ui = { mode: "unpopular", maxPct: 20, count: 5, inc: [], exc: [] };
  var lastLotto = [], lastPension = [];
  var HELP = {
    unpopular: "전체 8,145,060개 조합 중 사람들이 덜 고르는 쪽에서 무작위로 고른다. 과거 1등 조합, 같은 간격 수열, 4개 이상 연속 번호처럼 따라 사는 사람이 많은 모양은 뺀다. 당첨 확률은 다른 조합과 같다.",
    random: "모든 조합을 똑같은 확률로 고른다. 판매점 자동과 같은 방식이다.",
    ddpm: "과거 당첨번호로 학습한 확산 모델(DDPM)이 미리 만든 번호 중에서 고른다. 실험용이다 — 검증 결과 적중 실력은 무작위와 같고, 특정 번호를 지나치게 많이 쓰는 치우침이 있다(머신러닝 대결 화면)."
  };

  function $(id) { return document.getElementById(id); }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function randInt(n) {            // 0..n-1 균등 — 거절 표본추출로 나머지 치우침이 없다
    var lim = Math.floor(0x100000000 / n) * n, buf = new Uint32Array(1);
    for (;;) { crypto.getRandomValues(buf); if (buf[0] < lim) return buf[0] % n; }
  }
  function pickK(pool, k) {         // 부분 피셔-예이츠
    var a = pool.slice();
    for (var i = 0; i < k; i++) { var j = i + randInt(a.length - i), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a.slice(0, k);
  }
  function won(x) {
    if (x >= 1e8) return (x / 1e8).toFixed(1) + "억";
    if (x >= 1e4) return Math.round(x / 1e4).toLocaleString("ko-KR") + "만";
    return Math.round(x).toLocaleString("ko-KR");
  }
  function ballCls(n) { return n <= 10 ? "b1" : n <= 20 ? "b2" : n <= 30 ? "b3" : n <= 40 ? "b4" : "b5"; }
  function key(c) { return c.join("-"); }
  function msg(t) { $("lotto-msg").textContent = t || ""; }

  function backtest(c) {
    var r = simulate(c, ROUNDS), wrap = el("div", "backtest");
    var first = ROUNDS[0][0], last = ROUNDS[ROUNDS.length - 1][0];
    wrap.appendChild(el("p", "pnote", first + "회~" + last + "회 매주 이 번호 1게임: 쓴 돈 " + r.spent.toLocaleString("ko-KR") +
      "원 · 받은 돈 " + r.won.toLocaleString("ko-KR") + "원 (회수율 " + Math.round(r.won / r.spent * 100) + "%). 평균적인 번호라면 약 " +
      Math.round(r.expectedWon).toLocaleString("ko-KR") + "원 (" + Math.round(r.expectedWon / r.spent * 100) + "%)." +
      (r.unknownFirst ? " 1등이 없어 이월된 회차의 1등 " + r.unknownFirst + "번은 금액을 알 수 없어 빼고 셌다." : "") +
      " 과거 성적은 운이고, 다음 회 확률과는 무관하다."));
    var tw = el("div", "tablewrap full"), tb = el("table", "data"), th = el("thead"), hr = el("tr");
    ["", "1등", "2등", "3등", "4등", "5등"].forEach(function (h) { hr.appendChild(el("th", null, h)); });
    th.appendChild(hr); tb.appendChild(th);
    var body = el("tbody");
    [["이 번호", r.counts.map(String)], ["평균적인 번호 (기대)", TIER_P.map(function (p) { var x = p * r.n; return x < 0.01 ? x.toFixed(4) : x.toFixed(2); })]]
      .forEach(function (row) {
        var tr = el("tr"); tr.appendChild(el("td", "rowh", row[0]));
        row[1].forEach(function (v) { tr.appendChild(el("td", "num", v)); }); body.appendChild(tr);
      });
    tb.appendChild(body); tw.appendChild(tb); wrap.appendChild(tw);
    return wrap;
  }

  function ticket(label, c, detail) {
    var pop = popularity(c, S), sh = comboShape(c), low = pop.pct <= 50;
    var row = el("div", "ticket");
    row.appendChild(el("span", "tk-l", label));
    var balls = el("span", "balls");
    c.forEach(function (n) { balls.appendChild(el("span", "ball " + ballCls(n), String(n))); });
    row.appendChild(balls);
    var info = el("div", "tk-info");
    var p = low ? pop.pct : 100 - pop.pct;
    info.appendChild(el("span", "tk-chip " + (low ? "tk-low" : "tk-high"),
      (low ? "▼ 인기 하위 " : "▲ 인기 상위 ") + Math.max(0.5, p).toFixed(p < 10 ? 1 : 0) + "%"));
    var gross = S.pool1_recent_mean * pop.share;
    info.appendChild(el("span", "tk-chip", "1등 시 기대 " + won(gross) + "원 · 세후 " + won(afterTax(gross).net) + "원 (평균의 " + (pop.share / S.share_avg).toFixed(2) + "배)"));
    if (PAST[key(c)]) info.appendChild(el("span", "tk-chip tk-flag", "⚑ 과거 1등 조합 (" + PAST[key(c)] + "회)"));
    if (sh.arithmetic) info.appendChild(el("span", "tk-chip tk-flag", "⚑ 같은 간격 수열"));
    if (sh.maxRun >= 4) info.appendChild(el("span", "tk-chip tk-flag", "⚑ " + sh.maxRun + "개 연속"));
    if (detail) {
      var best = 0, rounds = [];
      Object.keys(PAST).forEach(function (k) {
        var d = k.split("-").map(Number), ov = c.filter(function (x) { return d.indexOf(x) >= 0; }).length;
        if (ov > best) { best = ov; rounds = [PAST[k]]; } else if (ov === best) rounds.push(PAST[k]);
      });
      rounds.sort(function (a, b) { return a - b; });
      info.appendChild(el("span", "tk-chip", "과거 최대 " + best + "개 일치 (" + rounds.length + "회: " + rounds.slice(-3).join("·") + (rounds.length > 3 ? "…" : "") + ")"));
      info.appendChild(el("span", "tk-chip", LATEST + "회 번호와 " + c.filter(function (x) { return S.latest_numbers.indexOf(x) >= 0; }).length + "개 겹침"));
    }
    row.appendChild(info);
    return row;
  }

  function makeLotto() {
    msg("");
    var allowed = [], n;
    for (n = 1; n <= 45; n++) if (ui.inc.indexOf(n) < 0 && ui.exc.indexOf(n) < 0) allowed.push(n);
    var need = 6 - ui.inc.length;
    if (allowed.length < need) { msg("제외한 번호가 너무 많아 고를 번호가 모자랍니다."); return; }
    var out = [], seen = {}, missed = 0;
    for (var k = 0; k < ui.count; k++) {
      var c = null;
      if (ui.mode === "ddpm") {
        var pool = POOL.filter(function (p) {
          return ui.inc.every(function (x) { return p.indexOf(x) >= 0; }) &&
                 !p.some(function (x) { return ui.exc.indexOf(x) >= 0; }) && !seen[key(p)];
        });
        if (!pool.length) { msg("고정·제외 조건에 맞는 확산 모델 번호가 더 없습니다. 조건을 줄여 주세요."); break; }
        c = pool[randInt(pool.length)];
      } else {
        var best = null, bestPct = 101;
        for (var t = 0; t < 30000; t++) {
          var cand = ui.inc.concat(pickK(allowed, need)).sort(function (a, b) { return a - b; });
          if (seen[key(cand)]) continue;
          if (ui.mode === "random") { c = cand; break; }
          var sh = comboShape(cand);
          if (PAST[key(cand)] || sh.arithmetic || sh.maxRun >= 4) continue;
          var pc = popularity(cand, S).pct;
          if (pc <= ui.maxPct) { c = cand; break; }
          if (pc < bestPct) { best = cand; bestPct = pc; }
        }
        if (!c) { c = best; missed++; }
      }
      if (!c) break;
      seen[key(c)] = 1;
      out.push(c);
    }
    if (missed) msg("고정한 번호 때문에 인기 하위 " + ui.maxPct + "% 조합을 " + missed + "게임에서 찾지 못해, 찾은 것 중 가장 덜 인기 있는 조합을 넣었습니다.");
    lastLotto = out;
    var box = $("lotto-out");
    box.textContent = "";
    out.forEach(function (c, i) { box.appendChild(ticket("ABCDE".charAt(i), c)); });
  }

  function makePension() {
    var g = $("pension-group").value, cnt = +$("pension-count").value, rows = [];
    function digits() { var s = ""; for (var i = 0; i < 6; i++) s += String(randInt(10)); return s; }
    if (g === "all") { var d = digits(); for (var k = 1; k <= 5; k++) rows.push({ g: k, d: d }); }
    else for (var i = 0; i < cnt; i++) rows.push({ g: g === "rand" ? 1 + randInt(5) : +g, d: digits() });
    lastPension = rows;
    var box = $("pension-out");
    box.textContent = "";
    rows.forEach(function (r, i) {
      var row = el("div", "ticket");
      row.appendChild(el("span", "tk-l", "ABCDE".charAt(i)));
      var dg = el("span", "pdigits");
      dg.appendChild(el("span", "pgroup", r.g + "조"));
      r.d.split("").forEach(function (x) { dg.appendChild(el("span", "pd", x)); });
      row.appendChild(dg);
      if (PPAST[r.d]) { var info = el("div", "tk-info"); info.appendChild(el("span", "tk-chip", PPAST[r.d] + "회 1등 번호와 같은 6자리")); row.appendChild(info); }
      box.appendChild(row);
    });
  }

  function copy(text, btn) {
    function done() { var o = btn.textContent; btn.textContent = "복사했습니다"; setTimeout(function () { btn.textContent = o; }, 1400); }
    function fallback() {
      var ta = el("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.left = "-9999px";
      document.body.appendChild(ta); ta.select();
      try { if (document.execCommand("copy")) done(); } catch (e) { /* 선택된 상태로 둔다 */ }
      ta.remove();
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fallback);
    else fallback();
  }

  function segment(container, attr, onPick) {
    container.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("button[data-" + attr + "]");
      if (!b) return;
      Array.prototype.forEach.call(container.querySelectorAll("button"), function (x) {
        var on = x === b; x.classList.toggle("is-on", on); x.setAttribute("aria-pressed", String(on));
      });
      onPick(b.getAttribute("data-" + attr));
    });
  }

  function wire() {
    segment(root.querySelector(".mk-game"), "game", function (g) {
      $("lotto-panel").hidden = g !== "lotto"; $("pension-panel").hidden = g !== "pension";
    });
    segment($("mode-seg"), "mode", function (m) {
      ui.mode = m; $("mode-help").textContent = HELP[m]; $("pct-ctl").hidden = m !== "unpopular";
    });
    $("pct-sel").addEventListener("change", function () { ui.maxPct = +this.value; });
    $("lotto-count").addEventListener("change", function () { ui.count = +this.value; });
    $("numgrid").addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("button[data-n]");
      if (!b) return;
      var n = +b.getAttribute("data-n"), s = b.getAttribute("data-s");
      var next = s === "none" ? "in" : s === "in" ? "out" : "none";
      if (next === "in" && ui.inc.length >= 5) { msg("고정 번호는 5개까지입니다 — 제외로 넘어갑니다."); next = "out"; }
      ui.inc = ui.inc.filter(function (x) { return x !== n; });
      ui.exc = ui.exc.filter(function (x) { return x !== n; });
      if (next === "in") ui.inc.push(n);
      if (next === "out") ui.exc.push(n);
      b.setAttribute("data-s", next);
      b.setAttribute("aria-label", n + "번 (" + (next === "in" ? "꼭 포함" : next === "out" ? "제외" : "기본") + ")");
    });
    $("lotto-go").addEventListener("click", makeLotto);
    $("lotto-copy").addEventListener("click", function () {
      copy(lastLotto.map(function (c) { return c.map(function (x) { return (x < 10 ? "0" : "") + x; }).join(" "); }).join("\n"), this);
    });
    $("lotto-reset").addEventListener("click", function () {
      ui.inc = []; ui.exc = []; msg("");
      Array.prototype.forEach.call($("numgrid").querySelectorAll("button"), function (b) {
        b.setAttribute("data-s", "none"); b.setAttribute("aria-label", b.getAttribute("data-n") + "번 (기본)");
      });
    });
    $("check-go").addEventListener("click", function () {
      var nums = ($("my-numbers").value.match(/\d+/g) || []).map(Number), uniq = [];
      nums.forEach(function (x) { if (uniq.indexOf(x) < 0) uniq.push(x); });
      var box = $("check-out");
      box.textContent = "";
      if (uniq.length !== 6 || uniq.some(function (x) { return x < 1 || x > 45; })) {
        box.appendChild(el("p", "empty", "1~45 사이 서로 다른 번호 6개를 입력하세요.")); return;
      }
      var c = uniq.sort(function (a, b) { return a - b; });
      box.appendChild(ticket("검", c, true));
      box.appendChild(backtest(c));
    });
    $("my-numbers").addEventListener("keydown", function (e) { if (e.key === "Enter") $("check-go").click(); });
    $("tax-go").addEventListener("click", function () {
      var v = +($("tax-in").value.replace(/[^0-9]/g, "") || 0), t = afterTax(v);
      $("tax-out").textContent = v ? ("세금 " + t.tax.toLocaleString("ko-KR") + "원 → 실수령 " + t.net.toLocaleString("ko-KR") + "원 (" + won(t.net) + "원)") : "금액을 원 단위 숫자로 넣어 주세요.";
    });
    $("tax-in").addEventListener("keydown", function (e) { if (e.key === "Enter") $("tax-go").click(); });
    $("pension-go").addEventListener("click", makePension);
    $("pension-group").addEventListener("change", function () { $("pension-count").disabled = this.value === "all"; });
    $("pension-copy").addEventListener("click", function () {
      copy(lastPension.map(function (r) { return r.g + "조 " + r.d; }).join("\n"), this);
    });
  }

  fetch(root.getAttribute("data-score-url"))
    .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
    .then(function (d) {
      S = d.score; POOL = d.ddpm_pool; LATEST = d.latest_round; ROUNDS = d.rounds;
      d.rounds.forEach(function (r) { PAST[r.slice(1, 7).join("-")] = r[0]; });
      d.pension_past.forEach(function (r) { PPAST[r[1]] = r[0]; });
      wire();
      makeLotto();      // 처음 열었을 때도 결과가 보이게 한 번 뽑아 둔다 (새로고침마다 바뀐다)
      makePension();
    })
    .catch(function (e) {
      $("lotto-out").appendChild(el("p", "empty", "인기도 계수를 불러오지 못했습니다: " + e.message));
    });
})();
