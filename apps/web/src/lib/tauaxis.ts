/** DRT 가로축 — `ln τ` 와 `log₁₀ τ`.
 *
 *  **τ 자체는 축으로 못 쓴다.**  이완 시간은 마이크로초에서 수백 초까지
 *  여섯 자리를 걸치고, 선형 축에 놓으면 봉우리 대부분이 왼쪽 한 점에 뭉친다.
 *  그래서 로그를 취하는데, **어느 로그인지가 랩마다 다르다.**
 *
 *  DRT 문헌과 이 랩이 실제로 쓰는 것은 `ln τ` 다 — γ(ln τ) 의 정의 자체가
 *  자연로그 위의 밀도이고 (`Z = ∫ γ(ln τ)/(1+jωτ) d ln τ`), 봉우리 아래 넓이가
 *  곧 저항이 되는 것도 그 축에서다.  `log₁₀` 는 눈금을 읽기 쉬워서 쓴다
 *  (−3 이 곧 1 ms).  둘은 **같은 그림을 2.303 배로 늘인 것**이라 봉우리 자리와
 *  높이의 뜻이 달라지지 않지만, 폭을 자로 재서 적는 사람에게는 다른 수가 된다.
 *
 *  그래서 고르게 두고 기본은 `ln` 이다.  고른 것은 이 브라우저에 남는다.
 */

export type TauAxis = 'ln' | 'log10'

export const TAU_AXES: readonly TauAxis[] = ['ln', 'log10']

/** 이 브라우저가 기억하는 열쇠.  DRT 를 그리는 화면 둘이 같은 것을 쓴다 --
 *  한쪽에서 `ln` 으로 보다 다른 쪽에서 `log₁₀` 이 나오면 같은 봉우리가 다른
 *  자리에 있는 것처럼 보인다. */
export const TAU_AXIS_KEY = 'bml.drtTauAxis'

export function tauAxisValue(axis: TauAxis, tauSeconds: number): number {
  return axis === 'ln' ? Math.log(tauSeconds) : Math.log10(tauSeconds)
}

/** 축의 값에서 τ 를 되돌린다 — 눈금 설명(`describeX`)이 쓴다. */
export function tauFromAxis(axis: TauAxis, value: number): number {
  return axis === 'ln' ? Math.exp(value) : 10 ** value
}

export function tauAxisLabel(axis: TauAxis): string {
  return axis === 'ln' ? 'ln τ (τ in s)' : 'log₁₀ τ (s)'
}

/** 고르개에 적을 짧은 이름. */
export function tauAxisShort(axis: TauAxis): string {
  return axis === 'ln' ? 'ln τ' : 'log₁₀ τ'
}

/** 저장된 값이 우리가 아는 둘 중 하나인가.  아니면 기본(`ln`). */
export function validTauAxis(value: unknown): TauAxis {
  return value === 'log10' ? 'log10' : 'ln'
}
