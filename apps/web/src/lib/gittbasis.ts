/** GITT 의 용량 축 — mAh · mAh/g · mAh/cm².
 *
 *  상세와 비교가 **같은 규칙을 봐야 한다.**  다르면 같은 기록의 가로축이 두
 *  화면에서 다르게 생기고, 나란히 놓는 것이 비교 화면의 일이라 거기서 곧바로
 *  어긋난다.
 *
 *  전고체에서는 같은 mAh/g 도 면적이 다르면 다른 전류밀도로 잰 것이 된다.
 *  그래서 랩이 실제로 쓰는 축은 mAh/cm² 다.
 */

import type { GittRun } from './types'

export type GittBasis = 'mAh' | 'mAh/g' | 'mAh/cm2'

export const GITT_BASIS_LABEL: Record<GittBasis, string> = {
  mAh: 'mAh',
  'mAh/g': 'mAh/g',
  'mAh/cm2': 'mAh/cm²',
}

export const GITT_AXIS_LABEL: Record<GittBasis, string> = {
  mAh: '용량 (mAh)',
  'mAh/g': '비용량 (mAh g⁻¹)',
  'mAh/cm2': '면적용량 (mAh cm⁻²)',
}

/** 그 기준으로 나누는 수 — 없으면 `null` 이고, 그러면 그 기준을 못 쓴다.
 *
 *  나눌 수가 없을 때 1 로 나누지 않는다: mAh 를 mAh/cm² 라고 부르기만 한
 *  숫자가 되고, 그것은 측정한 면적용량과 화면에서 구별되지 않는다 (§0.4).
 */
export function gittDivisor(record: GittRun, basis: GittBasis): number | null {
  if (basis === 'mAh/g') return record.active_mass_g_effective || null
  if (basis === 'mAh/cm2') return record.area_cm2_effective || null
  return 1
}

/** 여러 기록을 한 그림에 얹을 때, 그 기준을 **못 쓰는 것**은 어느 것인가.
 *
 *  겹쳐 그리는 자리에서는 하나만 못 나눠도 그림이 거짓말을 한다: mAh 곡선과
 *  mAh/cm² 곡선이 같은 가로눈금에 서면, 둘의 길이 차이가 용량 차이인지 단위
 *  차이인지 볼 방법이 없다.  빼고 **이름을 적는다** (§0.4).
 */
export function splitByBasis(
  records: GittRun[], basis: GittBasis,
): { kept: GittRun[]; dropped: GittRun[] } {
  const kept: GittRun[] = []
  const dropped: GittRun[] = []
  for (const record of records) {
    (gittDivisor(record, basis) ? kept : dropped).push(record)
  }
  return { kept, dropped }
}
