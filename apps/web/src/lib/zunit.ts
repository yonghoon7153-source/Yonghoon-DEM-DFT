/** 임피던스를 어느 단위로 볼까 — `Ω` 인가 `Ω·cm²` 인가.
 *
 *  **왜 고르게 두는가.**  같은 전극을 지름 10 mm 로 찍은 것과 16 mm 로 찍은
 *  것은 저항이 2.5 배 다르다.  셀끼리 견주려면 면적으로 나눈 값(ASR)이라야
 *  하고 논문의 값도 대개 그것이다 — 그런데 **계측기가 준 수는 Ω 다.**  ZView
 *  결과와 대조하거나, 이 셀 하나의 사이클 간 변화만 보거나, 랩 노트의 예전
 *  수와 맞춰 볼 때는 나누지 않은 쪽이 맞다.  둘 다 필요하므로 단추로 둔다.
 *
 *  **왜 열쇠를 함께 쓰는가.**  상세 화면은 면적이 적혀 있으면 늘 Ω·cm² 로
 *  그렸고 비교 화면은 Ω 로 그렸다.  같은 스펙트럼의 R₀ 가 한 화면에서 15.6,
 *  다른 화면에서 12.3 으로 나오는데 두 수가 다른 단위라는 말은 축 이름에만
 *  있었다 — 눈이 축까지 안 간다.  `TAU_AXIS_KEY` 가 DRT 가로축에서 이미 푼
 *  것과 같은 문제이고, 같은 방법으로 푼다: 한 브라우저에 하나의 선택.
 *
 *  **면적을 모르면 나누지 않는다.**  추정 면적으로 나눈 수는 실측 ASR 과
 *  똑같이 생겼고 어느 쪽인지 알 방법이 없다 (§0.4).  그래서 `areaFor` 는
 *  `null` 을 돌려주고, 화면은 Ω 로 그리면서 **왜 못 바꾸는지를 적는다.**
 */

export type ZUnit = 'ohm' | 'ohmcm2'

export const Z_UNITS: readonly ZUnit[] = ['ohm', 'ohmcm2']

/** 이 브라우저가 기억하는 열쇠.  스펙트럼 상세와 EIS 비교가 같은 것을 쓴다. */
export const Z_UNIT_KEY = 'bml.zUnit'

export function validZUnit(value: unknown, fallback: ZUnit = 'ohm'): ZUnit {
  return value === 'ohm' || value === 'ohmcm2' ? value : fallback
}

/** 축과 표에 적을 이름. */
export function zUnitLabel(unit: ZUnit): string {
  return unit === 'ohm' ? 'Ω' : 'Ω·cm²'
}

/** 이 화면이 실제로 나눌 면적.
 *
 *  `Ω` 를 골랐거나 면적을 모르면 `null` 이고, `perArea(value, null)` 은 값을
 *  그대로 둔다 — 화면 곳곳에서 `if` 를 되풀이하지 않으려고 여기 한 곳에서
 *  판정한다.  단위 이름도 이 결과로 정해야 **그림과 이름이 어긋나지 않는다**:
 *  면적이 없는데 `Ω·cm²` 라고 적히는 것이 이 함수가 막는 사고다.
 */
export function areaFor(unit: ZUnit, area: number | null | undefined): number | null {
  if (unit !== 'ohmcm2') return null
  return area && area > 0 ? area : null
}
