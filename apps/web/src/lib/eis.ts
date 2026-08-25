/** 임피던스 점 다루기 — 화면 여럿이 같은 규칙을 써야 하는 것들.
 *
 *  지금은 하나뿐이다: 실수축 **위**에 있는 점을 어떻게 볼 것인가.
 */

/** 유도성 점의 수 — 실수축 위(Z″ > 0)에 있는 것.
 *
 *  이 실험실의 파일은 실제로 유도성으로 시작한다: 7 MHz 부터 몇백 kHz 까지
 *  Z″ 가 양수다.  그것은 케이블과 셀 홀더이지 셀이 아니고, 어떤 셀 회로도
 *  재현하지 못한다 (`wrdkit/eis/guess.py: inductive_mask` 와 같은 규칙 —
 *  판정은 부호 하나다).
 */
export function inductiveCount(zIm: number[]): number {
  let n = 0
  for (const value of zIm) if (value > 0) n += 1
  return n
}

/** 유도성 점을 뺀 (Z′, −Z″).
 *
 *  나이퀴스트에서 이 점들은 −Z″ 가 음수라 아크 밑으로 수직선이 되어 꽂히고,
 *  세로 눈금을 통째로 늘려 아크를 납작하게 만든다.  `y ≥ 0` 단추는 **보이는
 *  범위**만 자르므로 그 수직선은 그대로 남는다 — 그래서 여기서 점 자체를 뺀다.
 *
 *  **조용히 빼지 않는다.**  뺀 수를 함께 돌려주고 화면이 그것을 적는다:
 *  직렬저항이 옴 단위로 달라지는데 이유를 아무도 모르는 것이 이 규칙이
 *  생긴 이유다 (ADR 0019).
 *
 *  부호 하나로만 자른다.  "고주파 몇 점" 처럼 세는 규칙을 넣으면 아크가
 *  실제로 유도성인 셀(리튬 도금 같은)에서 실측을 지우게 된다.
 */
export function nyquistXy(
  zRe: number[],
  zIm: number[],
  dropInductive: boolean,
  /** 면적 정규화 같은 눈금 바꾸기.  자르기를 **먼저** 하고 여기를 태운다 —
   *  Ω·cm² 로 바꿔도 부호는 그대로라 순서가 답을 바꾸지는 않지만, 판정이
   *  언제나 날 것의 Z″ 위에서 일어나는 편이 읽기 쉽다. */
  scale: (value: number) => number = (value) => value,
): { x: number[]; y: number[]; dropped: number } {
  const x: number[] = []
  const y: number[] = []
  let dropped = 0
  for (let i = 0; i < zRe.length; i += 1) {
    if (dropInductive && (zIm[i] ?? 0) > 0) {
      dropped += 1
      continue
    }
    x.push(scale(zRe[i]!))
    // 나이퀴스트 세로축은 −Z″ 다.
    y.push(scale(-(zIm[i] ?? 0)))
  }
  return { x, y, dropped }
}
