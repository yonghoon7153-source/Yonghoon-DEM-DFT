/** 면적을 곱한 임피던스 — Ω 를 Ω·cm² 로.
 *
 *  **곱이지 몫이다가 아니다.**  저항은 면적에 반비례하므로 (`R = ρL/A`),
 *  크기를 지운 값은 `R·A = ρL` 이다.  화면 문구가 오래 "면적으로 나눈 값" 이라고
 *  적혀 있었는데 (코드는 처음부터 곱하고 있었다) 읽는 사람에게 거짓말이었다
 *  (Codex 그림 리뷰 #9).  **용량**은 반대다 — mAh/cm² 는 진짜로 나눈다.
 *
 *  같은 전극을 지름 10 mm 로 찍은 것과 16 mm 로 찍은 것은 저항이 2.5 배 다르다.
 *  재료가 같아도 그렇다.  그래서 셀끼리 비교하려면 면적을 곱한 값(면적비
 *  저항, ASR)이라야 한다 — 논문의 값도 대개 그것이다.
 *
 *  **면적을 모르면 손대지 않는다.**  추정한 면적을 곱한 수는 측정된 ASR 과
 *  똑같이 생겼고, 어느 쪽인지 알 방법이 없다 (§0.4).  그래서 화면은 면적이
 *  적혀 있을 때만 Ω·cm² 로 바뀌고, 그전에는 Ω 그대로 둔다.
 */

/** 파라미터 이름이 저항인가 — 면적으로 나눌 수 있는 것인가.
 *
 *  단위로 가린다: `Ω` 인 것만 나눈다.  CPE 의 `S·sⁿ`, 지수 `n`, 시간상수 `s`,
 *  인덕턴스 `H` 는 면적으로 나누는 양이 아니다 (CPE 는 오히려 **곱해야** 하고,
 *  그 규칙은 지수 n 에 따라 달라서 여기서 조용히 처리할 수 없다).
 */
export function scalesWithArea(unit: string): boolean {
  return unit.trim() === 'Ω'
}

/** 면적을 곱한 단위 이름.  곱할 수 없는 단위는 그대로 돌려준다. */
export function areaUnit(unit: string, area: number | null | undefined): string {
  if (!area || !scalesWithArea(unit)) return unit
  return 'Ω·cm²'
}

/** 값 하나.  면적이 없으면 그대로 둔다 — 그것이 이 함수의 요점이다.
 *
 *  이름이 `perArea` 인데 **곱한다**.  `Ω per cm²` 가 아니라 `Ω·cm²` 라는
 *  뜻으로 읽어야 한다 (면적당으로 규격화한 값). */
export function perArea(value: number, area: number | null | undefined): number {
  return area && area > 0 ? value * area : value
}
