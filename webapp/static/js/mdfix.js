/* mdfix.js — 한국어 마크다운의 볼드/취소선이 CommonMark 에서 안 닫히는 문제 보정.
 *
 * 왜 필요한가 (2026-08-05, 1저자 발견):
 *   `**평균 potential(Mean Field)**로` 처럼 "닫는 ** 앞이 구두점이고 뒤가 한글"이면
 *   CommonMark 의 right-flanking 규칙상 강조가 닫히지 않아 `**` 가 그대로 보인다.
 *   한국어는 조사가 바로 붙는 언어라 이 형태가 흔하다 — kb 전체에 610건.
 *   서버(Python-Markdown)는 규칙이 느슨해 정상 렌더되는데 브라우저(marked.js)만 실패했다.
 *
 * 방침: 소스를 고치지 않고(자연스러운 표기다) 렌더 직전에 <strong>/<em>/<del> 로 바꾼다.
 *   코드펜스·인라인코드·수식($…$, $$…$$)은 자리표시자로 빼두고 건드리지 않는다
 *   (파일 글로브 `*.png`, KaTeX `$x^*$` 오염 방지).
 */
(function (global) {
  function protect(src, store) {
    function put(m) { store.push(m); return "MDX" + (store.length - 1) + ""; }
    return src
      .replace(/```[\s\S]*?```/g, put)      // 코드펜스
      .replace(/~~~[\s\S]*?~~~/g, put)
      .replace(/\$\$[\s\S]*?\$\$/g, put)    // 블록 수식
      .replace(/`[^`\n]*`/g, put)           // 인라인 코드
      .replace(/\$[^$\n]*\$/g, put);        // 인라인 수식
  }

  function restore(src, store) {
    return src.replace(/MDX(\d+)/g, function (_, k) { return store[+k]; });
  }

  /* 마크다운 강조를 HTML 로 미리 변환 (flanking 규칙을 우회) */
  global.mdFixEmphasis = function (src) {
    if (!src) return src;
    var store = [];
    var s = protect(src, store);
    s = s.replace(/\*\*([^\n*][^\n]*?)\*\*/g, "<strong>$1</strong>");   // **볼드**
    s = s.replace(/~~([^\n~][^\n]*?)~~/g, "<del>$1</del>");             // ~~취소선~~
    // *기울임* — 앞뒤가 공백이 아닌 경우만 (글로브·곱셈기호 오탐 방지)
    s = s.replace(/(^|[^\w*\\])\*([^\s*][^\n*]*?[^\s*])\*(?![\w*])/g, "$1<em>$2</em>");
    return restore(s, store);
  };
})(window);
