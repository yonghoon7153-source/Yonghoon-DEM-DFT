/** 대칭셀 이온전도도 파트가 공유하는 것들 (ADR 0039).
 *
 *  이 파트가 EIS 와 갈리는 이유는 **묻는 것이 달라서**다.  SOC 스캔은 "SOC 에
 *  따라 저항이 어떻게 변하나" 이고, 이쪽은 "이 전해질의 이온전도도와 활성화
 *  에너지가 얼마인가" 다.  축도(1000/T) 분모도(두께·면적) 마지막에 남는 수도
 *  다르다.
 */

import type { Scan, ScanConductivity } from './types'

/** 대칭셀 파트가 스캔을 모으는 목적 이름.  자유 입력이므로 **고정 목록이
 *  아니다** — 이것은 업로드 화면의 보기이자, 목록이 기본으로 거르는 말이다. */
export const CONDUCTIVITY_PURPOSE = '이온전도도 스윕'

/** 저항이 어디서 왔는지, 사람이 읽을 말로.
 *
 *  표에 늘 적는다.  손으로 읽은 저항과 맞춘 저항이 한 열에 섞인 채 슬라이드에
 *  붙으면 그 구분은 영영 사라지고, 실측에서 그 차이는 활성화에너지 13 % 였다.
 */
export function sourceLabel(source: string): string {
  if (source === 'typed') return '적음'
  if (source === 'fit') return 'fitting'
  return ''
}

/** 이 스캔이 대칭셀 파트의 것인가.
 *
 *  둘 중 하나면 된다: 목적에 `이온전도도` 가 적혀 있거나, 셀 구성이 대칭셀
 *  이거나.  **숨기지 않는 쪽으로 넉넉하게 잡는다** — 여기 안 보이는 파일은
 *  사람이 찾을 자리가 없고, 잘못 들어온 파일은 눈에 띄면 그만이다.
 */
export function isConductivityScan(scan: Scan): boolean {
  return scan.purpose.includes('이온전도도') || scan.cell_config === 'sym'
}

/** 표가 서려면 아직 무엇이 필요한가 — 서버가 준 목록을 한 문장으로. */
export function missingSentence(data: ScanConductivity): string {
  if (!data.missing.length) return ''
  return `${data.missing.join(' · ')} 이(가) 아직 없습니다 — 적으면 표가 채워집니다.`
}

/** 활성화에너지를 적는 말.  기준을 **늘 함께** 적는다.
 *
 *  같은 아홉 점에서 `ln σ` 는 0.329 eV, `ln(σT)` 는 0.354 eV 다 (실측).  둘 다
 *  맞는 수이고 뜻이 다르므로, 기준이 안 적힌 활성화에너지는 비교할 수 없다.
 */
export function basisLabel(basis: string): string {
  return basis === 'sigma_t' ? 'ln(σT) 대 1000/T' : 'ln σ 대 1000/T'
}
