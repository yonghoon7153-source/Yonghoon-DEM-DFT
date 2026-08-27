/** 임피던스를 어느 단위로 볼까 — `Ω` 인가 `Ω·cm²` 인가.
 *
 *  **왜 고르게 두는가.**  같은 전극을 지름 10 mm 로 찍은 것과 16 mm 로 찍은
 *  것은 저항이 2.5 배 다르다.  셀끼리 견주려면 면적을 곱한 값(ASR)이라야
 *  하고 논문의 값도 대개 그것이다 — 그런데 **계측기가 준 수는 Ω 다.**  ZView
 *  결과와 대조하거나, 이 셀 하나의 사이클 간 변화만 보거나, 랩 노트의 예전
 *  수와 맞춰 볼 때는 나누지 않은 쪽이 맞다.  둘 다 필요하므로 단추로 둔다.
 *
 *  **왜 열쇠를 함께 쓰는가.**  상세 화면은 면적이 적혀 있으면 늘 Ω·cm² 로
 *  그렸고 비교 화면은 Ω 로 그렸다.  같은 스펙트럼의 R₀ 가 한 화면에서 15.6,
 *  다른 화면에서 12.3 으로 나오는데 두 수가 다른 단위라는 말은 축 이름에만
 *  있었다 — 눈이 축까지 안 간다.  한 브라우저에 하나의 선택으로 푼다.
 *
 *  **면적을 모르면 손대지 않는다.**  추정 면적을 곱한 수는 실측 ASR 과
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

/** 이 브라우저가 단위를 **골라 본 적이 있는가.**
 *
 *  없으면 화면이 데이터를 보고 정할 수 있다 — 면적을 아는 스캔은 Ω·cm² 로
 *  여는 것이 맞고, 그것이 이 랩이 논문에 적는 값이다.  한 번이라도 골랐으면
 *  그 선택이 이긴다: 사람이 Ω 로 바꿔 놓은 화면이 새로고침마다 Ω·cm² 로
 *  돌아가면 그 단추는 고장 난 것으로 읽힌다.
 */
export function hasStoredZUnit(): boolean {
  try {
    return window.localStorage.getItem(Z_UNIT_KEY) !== null
  } catch {
    // 사생활 보호 모드에서는 읽기 자체가 던진다.  그때는 "고른 적 없다" 로 본다.
    return false
  }
}
