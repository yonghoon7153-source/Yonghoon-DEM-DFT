/** DRT 가로축 — `log₁₀ τ`.
 *
 *  **τ 자체는 축으로 못 쓴다.**  이완 시간은 마이크로초에서 수백 초까지
 *  여섯 자리를 걸치고, 선형 축에 놓으면 봉우리 대부분이 왼쪽 한 점에 뭉친다.
 *  그래서 로그를 취한다.
 *
 *  **`ln τ` 를 골라 쓸 수 있게 뒀다가 뺐다.**  DRT 문헌의 정의는 자연로그 위의
 *  밀도이고 (`Z = ∫ γ(ln τ)/(1+jωτ) d ln τ`) 봉우리 아래 넓이가 저항이 되는
 *  것도 그 축에서라, 한동안 `ln` 이 기본이었다.  그런데 이 랩이 실제로 읽는
 *  것은 `log₁₀` 다 — 눈금이 곧 자릿수라 `−3` 이 1 ms 로 바로 읽힌다.  둘은
 *  같은 그림을 2.303 배로 늘인 것이라 봉우리 자리와 높이의 뜻은 같지만, 폭을
 *  자로 재서 적는 사람에게는 다른 수가 된다.  **쓰지 않는 축을 골라 둘 수
 *  있게 두면 두 화면이 다른 축으로 그려지는 길만 남는다.**  하나로 줄인다.
 *
 *  되돌릴 일이 있으면 이 파일의 히스토리에 `ln` 갈래가 통째로 있다.
 */

/** τ (초) → 가로축 값. */
export function tauAxisValue(tauSeconds: number): number {
  return Math.log10(tauSeconds)
}

/** 축의 값에서 τ 를 되돌린다 — 눈금 설명(`describeX`)이 쓴다. */
export function tauFromAxis(value: number): number {
  return 10 ** value
}

export const TAU_AXIS_LABEL = 'log₁₀ τ (s)'

/** 클립보드 머리말처럼 좁은 자리에 적을 짧은 이름. */
export const TAU_AXIS_SHORT = 'log₁₀ τ'
