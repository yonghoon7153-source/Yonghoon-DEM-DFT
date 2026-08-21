/** 이 브라우저를 쓰는 사람의 이름.
 *
 * 검증하지 않는다 — 로그인이 아니다 (ADR 0012). 한 실험실에서 실제로 하는
 * 질문은 "이 셀 질량 누가 바꿨어" 이지 "네가 너임을 증명해라" 가 아니고,
 * 아무도 필요로 하지 않는 로그인은 공유되는 로그인, 포스트잇에 적힌 로그인,
 * 셀이 도는 새벽 두 시에 잠기는 로그인이 된다.
 *
 * 이름은 이 브라우저에만 남는다. 기계마다 한 번씩 물어보는 것이 맞다 —
 * 실험실 공용 PC 와 자기 노트북은 다른 사람이 쓸 수 있다.
 */

const KEY = 'workbench.who'

/** 표에 그려지고 헤더로 오간다.  서버의 MAX_ACTOR 와 같게 유지한다. */
export const MAX_NAME = 40

export function cleanName(raw: string): string {
  // 제어문자는 버린다.  이 값은 헤더로도 나가는데, 거기 줄바꿈이 하나 들어가면
  // 요청 자체가 깨진다.
  return [...raw]
    .filter((character) => character >= ' ' && character !== '')
    .join('')
    .trim()
    .slice(0, MAX_NAME)
}

export function readName(): string {
  try {
    return cleanName(window.localStorage.getItem(KEY) ?? '')
  } catch {
    return '' // 시크릿 모드 등 — 이름 없이도 다 돌아간다
  }
}

export function writeName(raw: string): string {
  const name = cleanName(raw)
  try {
    if (name) window.localStorage.setItem(KEY, name)
    else window.localStorage.removeItem(KEY)
  } catch {
    /* 저장이 안 되면 이번 세션에만 쓰인다 */
  }
  return name
}

/** 요청에 실을 헤더.  이름이 없으면 아무것도 싣지 않는다.
 *
 * HTTP 헤더 값은 ASCII 범위의 바이트만 담을 수 있다. 한글 이름을 그대로
 * 넣으면 요청이 브라우저를 떠나기도 전에 거절되므로, 서버가 되돌리는 방식
 * 그대로 퍼센트 인코딩해서 보낸다.
 */
export function actorHeader(): Record<string, string> {
  const name = readName()
  return name ? { 'X-Workbench-User': encodeURIComponent(name) } : {}
}
