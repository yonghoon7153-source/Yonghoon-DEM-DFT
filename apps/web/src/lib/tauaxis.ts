/** DRT 가로축 — `log₁₀ τ (s)` 인가 `f (Hz)` 인가.
 *
 *  **왜 로그인가.**  이완 시간은 마이크로초에서 수백 초까지 여섯 자리를
 *  걸친다.  선형 축에 놓으면 봉우리 대부분이 왼쪽 한 점에 뭉치므로, 어느
 *  쪽으로 그리든 좌표는 로그다.
 *
 *  **왜 둘인가.**  같은 γ 를 문헌은 대개 `f (Hz)` 로 그리고 (봉우리에 F1·F2…
 *  라고 이름을 붙이는 그 그림), DRT 를 푸는 쪽은 τ 로 본다.  둘은 `τ = 1/(2πf)`
 *  로 이어져 있어 **같은 그림을 좌우로 뒤집은 것**이다 — 고주파가 τ 축에서는
 *  왼쪽, f 축에서는 오른쪽이다.  봉우리의 높이와 넓이는 안 바뀐다: γ 는
 *  `d ln τ` 위의 밀도이고 `d ln τ = −d ln f` 라, 로그 축이기만 하면 봉우리
 *  아래 넓이(= 그 과정의 저항)가 그대로다.  뜻이 같고 읽는 사람이 다르므로
 *  고르게 둔다.
 *
 *  **`ln τ` 는 뺐다.**  DRT 의 정의가 자연로그 위의 밀도라 한동안 기본이었는데,
 *  이 랩이 실제로 읽는 것은 `log₁₀` 다 (눈금이 곧 자릿수라 `−3` 이 1 ms 로 바로
 *  읽힌다).  히스토리에 갈래가 통째로 있다.
 *
 *  **f 축의 눈금은 좌표가 아니라 주파수다.**  좌표는 `log₁₀ f` 여야 자릿수가
 *  고르게 퍼지는데, 사람이 읽어야 하는 것은 `2` 가 아니라 `10²` 이다.  그래서
 *  `drtAxisTick` 이 따로 있고, `Plot` 의 `xTick`·`xSplits` 가 그것을 받는다.
 */

import { num } from './format'

export type DrtAxis = 'tau' | 'f'

export const DRT_AXES: readonly DrtAxis[] = ['tau', 'f']

/** 이 브라우저가 기억하는 열쇠.  DRT 를 그리는 화면 둘이 같은 것을 쓴다 —
 *  한쪽에서 τ 로 보다 다른 쪽에서 f 가 나오면 같은 봉우리가 반대쪽 끝에 있는
 *  것처럼 보인다. */
export const DRT_AXIS_KEY = 'bml.drtAxis'

export function validDrtAxis(value: unknown, fallback: DrtAxis = 'tau'): DrtAxis {
  return value === 'tau' || value === 'f' ? value : fallback
}

/** τ (초) → 가로축 좌표.  둘 다 로그이고, f 쪽은 부호가 뒤집힌다. */
export function drtAxisValue(axis: DrtAxis, tauSeconds: number): number {
  return axis === 'tau'
    ? Math.log10(tauSeconds)
    : Math.log10(1 / (2 * Math.PI * tauSeconds))
}

/** 좌표에서 τ 를 되돌린다 — 눈금 설명(`describeX`)이 이 왕복 위에 선다. */
export function tauFromAxis(axis: DrtAxis, value: number): number {
  return axis === 'tau' ? 10 ** value : 1 / (2 * Math.PI * 10 ** value)
}

/** 클립보드로 나가는 **날 것의** x — τ 는 초, f 는 Hz.  로그로 내보내면
 *  워크시트에서 되돌릴 수 없다. */
export function rawFromTau(axis: DrtAxis, tauSeconds: number): number {
  return axis === 'tau' ? tauSeconds : 1 / (2 * Math.PI * tauSeconds)
}

export function drtAxisLabel(axis: DrtAxis): string {
  return axis === 'tau' ? 'log₁₀ τ (s)' : 'f (Hz)'
}

/** 고르개와 클립보드 머리말처럼 좁은 자리에 적을 짧은 이름. */
export function drtAxisShort(axis: DrtAxis): string {
  return axis === 'tau' ? 'log₁₀ τ' : 'f (Hz)'
}

const SUPERSCRIPT: Record<string, string> = {
  '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
  '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻',
}

/** 눈금 한 칸의 글자.
 *
 *  `tau` 축은 좌표가 곧 눈금이다 (`−3` 이 그대로 읽힌다).  `f` 축은 좌표가
 *  `log₁₀ f` 라 그대로 두면 `3` 이 3 Hz 로 읽힌다 — 실제로는 1 kHz 다.
 *
 *  자리 눈금(정수)은 `10ⁿ` 으로, 그 사이(확대했을 때)는 **실제 주파수**로
 *  적는다.  `10^0.5` 를 지수로 적으면 아무도 3.2 Hz 를 못 읽는다.
 */
export function drtAxisTick(axis: DrtAxis, value: number): string {
  // τ 축은 그대로.  `num` 을 태우면 `-3` 이 `-3.00` 이 되는데, 자리 눈금에
  // 소수점 둘은 읽는 데 도움이 안 되고 칸만 넓힌다.
  if (axis === 'tau') return String(Number(value.toPrecision(6)))
  const whole = Math.round(value)
  if (Math.abs(value - whole) < 1e-9) {
    if (whole === 0) return '1'
    if (whole === 1) return '10'
    return `10${String(whole).split('').map((c) => SUPERSCRIPT[c] ?? c).join('')}`
  }
  return num(10 ** value, 3)
}

/** 자리(10ⁿ)에 눈금을 놓는다.
 *
 *  uPlot 이 알아서 고르게 두면 `0.7` 같은 자리에 눈금이 떨어지고, 그러면
 *  지수 표기를 쓸 수가 없다.  **확대해서 두 자리도 안 남았을 때**는 범위에
 *  맞춘 폭으로 쪼갠다 — 눈금이 하나뿐인 축은 어디를 보고 있는지 말해 주지
 *  않는다.
 */
export function decadeSplits(min: number, max: number): number[] {
  const whole: number[] = []
  for (let n = Math.ceil(min); n <= Math.floor(max); n += 1) whole.push(n)
  if (whole.length >= 3) return whole

  // 확대해서 두 자리도 안 남았다.  고정 폭으로 쪼개면 (0.5, 0.25 …) 아주 좁게
  // 확대했을 때 눈금이 하나만 남거나 아예 없어지는데, 눈금 없는 축은 어디를
  // 보고 있는지 말해 주지 않는다.  범위에 맞춰 1·2·5 × 10ᵏ 중에서 고른다.
  const span = max - min
  if (!(span > 0)) return whole
  const rough = span / 5
  const magnitude = 10 ** Math.floor(Math.log10(rough))
  const step = [1, 2, 5, 10].map((m) => m * magnitude).find((one) => one >= rough)
    ?? magnitude * 10
  const out: number[] = []
  for (let v = Math.ceil(min / step) * step; v <= max; v += step) {
    // 부동소수 누적 오차가 눈금 글자에 `2.9999999996` 로 새어 나온다.
    out.push(Number(v.toPrecision(12)))
  }
  return out
}
