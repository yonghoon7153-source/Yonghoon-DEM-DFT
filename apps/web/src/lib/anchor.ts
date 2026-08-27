/** 누른 자리를 화면에 붙잡아 둔다.
 *
 *  비교 화면의 고르개는 **그림 밑**에 있다 (ADR 0023: 고르개가 위에 있으면
 *  스펙트럼이 늘수록 그림이 화면 밖으로 밀린다).  그 대신 값을 치르는 것이
 *  이것이다 — 체크를 하나 누르면 위쪽이 다시 그려지면서 높이가 변하고
 *  (범례가 한 줄 늘거나 줄고, 경고가 뜨거나 사라지고, '고른 것' 표에 줄이
 *  하나 붙는다), 고르개 전체가 그만큼 위아래로 움직인다.  **다음에 누르려던
 *  칸이 커서 밑에서 사라진다.**  다섯 개를 고르려면 다섯 번 스크롤을 다시
 *  맞춰야 했다.
 *
 *  그래서 누르는 순간 그 요소가 화면에서 있던 자리를 적어 두고, 다시 그려진
 *  뒤에 그 자리로 되돌린다.  높이가 **나중에** (요청이 돌아온 뒤에) 바뀌는
 *  경우가 대부분이라 한 번 고쳐서는 안 되고, 잠깐 동안 계속 지켜본다.
 */

/** 사람이 직접 굴리는 방법들.  `scrollBy` 는 이 중 무엇도 일으키지 않으므로,
 *  이것이 오면 우리가 손을 떼야 한다는 뜻이다 — 안 그러면 붙잡는 동안 사람의
 *  스크롤을 되돌려 버린다. */
const HANDS_OFF = ['wheel', 'touchmove', 'keydown'] as const

/**
 *  @param element 화면에서 제자리에 있어야 할 것 (고르개 상자).
 *  @param forMs  얼마나 지켜볼지.  응답이 돌아와 높이가 바뀌는 데까지가
 *                보통 몇백 ms 라, 1.2초면 넉넉하고 사람이 답답할 만큼 길지 않다.
 */
export function keepInPlace(element: HTMLElement | null, forMs = 1200): void {
  if (!element || typeof window === 'undefined') return
  if (typeof element.getBoundingClientRect !== 'function') return
  const want = element.getBoundingClientRect().top
  const deadline = Date.now() + forMs
  let frame = 0
  // 취소한 프레임이 **안 오는 것은 아니다.**  이미 예약된 콜백은 그대로
  // 실행될 수 있으므로, 그만두었다는 사실을 우리가 들고 있어야 한다.
  let stopped = false

  const stop = () => {
    stopped = true
    if (frame) window.cancelAnimationFrame(frame)
    for (const kind of HANDS_OFF) window.removeEventListener(kind, stop)
  }

  const tick = () => {
    if (stopped) return
    if (Date.now() > deadline) return stop()
    const drift = element.getBoundingClientRect().top - want
    // 반 픽셀 아래는 무시한다.  소수점 흔들림까지 좇으면 매 프레임 스크롤을
    // 건드리게 되고, 그 자체가 떨림으로 보인다.
    if (Math.abs(drift) > 0.5) window.scrollBy(0, drift)
    frame = window.requestAnimationFrame(tick)
  }

  for (const kind of HANDS_OFF) window.addEventListener(kind, stop, { passive: true })
  frame = window.requestAnimationFrame(tick)
}
