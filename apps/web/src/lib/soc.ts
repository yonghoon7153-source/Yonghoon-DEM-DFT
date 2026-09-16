/** 사람이 한 줄에 적은 SOC 를 스윕 차례의 목록으로 (ADR 0038).
 *
 *  읽는 일 자체는 `valuelist.ts` 가 한다 — 온도(ADR 0039)와 같은 입력이고,
 *  둘 다 계측기가 모르는 값을 스윕 차례대로 적는 일이다.  여기 남는 것은 SOC
 *  만의 두 가지다: 머리의 `SOC` 이름표와 끝의 `%`, 그리고 0~100 이라는 범위.
 *
 *  등간격 축약 `(0, 100, 11)` 도 그대로 쓸 수 있다 — 같은 파서라서 공짜다.
 */

import {
  type ValueList, listProblem, parseValueList,
} from './valuelist'

export type SocList = ValueList

/** 목록의 머리에 붙는 이름표.  `SOC 0, 10` 처럼 쓰는 사람이 많다. */
const LABEL = /^soc$|^soc:$|^%$/i
/** 끝의 % 는 단위지 값이 아니다. */
const UNIT = /%$/

export function parseSocList(text: string): SocList {
  return parseValueList(text, { label: LABEL, unit: UNIT })
}

/** 이 목록을 이 스캔에 적을 수 있는가.  못 적으면 **왜인지**를 돌려준다. */
export function socProblem(list: SocList, sweeps: number): string {
  return listProblem(list, sweeps, 'SOC', { low: 0, high: 100, unit: '%' })
}

/** 적어 둔 SOC 를 화면에 적는 말.  없으면 빈 문자열이다. */
export function socLabel(value: number | null | undefined): string {
  return value === null || value === undefined ? '' : `SOC ${value}%`
}
