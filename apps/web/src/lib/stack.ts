/** 곡선을 위로 비껴 쌓는다 — 논문이 SOC 스캔을 한 장에 싣는 그 방법.
 *
 *  스윕 열한 개를 같은 축에 겹치면 가장 큰 것 하나가 화면을 다 쓰고 나머지는
 *  그 안에서 납작해진다.  SOC 를 따라 아크가 어떻게 움직이는지가 이 화면을
 *  여는 이유인데, 정작 그것이 안 보인다.  그래서 곡선마다 일정한 양만큼
 *  **올려서** 그린다.
 *
 *  **세로 눈금은 그 순간 값이 아니게 된다.**  그것이 이 그림의 값이자 대가다 —
 *  모양은 또렷해지고 값은 못 읽는다.  그래서 여기서 올린 양(`step`)을 함께
 *  돌려주고, 화면과 클립보드가 그 수를 그대로 적는다.  적지 않으면 나중에
 *  누군가 이 그림에서 저항을 읽는다.
 *
 *  **올릴 양은 '가운데 곡선의 높이' 로 정한다** (최댓값이 아니라).  스캔 하나
 *  안에 유난히 큰 스윕이 하나 있는 것이 보통인데 (마지막 SOC 의 확산 꼬리),
 *  그 최댓값으로 간격을 잡으면 나머지 열 곡선이 서로 아주 멀리 떨어져 각자
 *  납작한 선이 된다.  중앙값이면 대부분의 곡선이 제 높이의 절반쯤 만큼
 *  떨어지고, 큰 곡선 하나만 이웃을 살짝 넘는다.
 */

export interface Stackable {
  y: number[]
  hidden?: boolean
}

/** 곡선 하나가 이웃보다 제 높이의 몇 배만큼 위에 앉을까. */
export const STACK_GAP = 0.6

/** 올릴 양 한 칸.  그릴 것이 없거나 전부 평평하면 0 (그러면 겹쳐 그린 것과
 *  같고, 그것이 맞다 — 없는 간격을 지어내지 않는다). */
export function stackStep(series: Stackable[], gap = STACK_GAP): number {
  const heights: number[] = []
  for (const one of series) {
    if (one.hidden) continue
    let low = Infinity
    let high = -Infinity
    for (const value of one.y) {
      if (!Number.isFinite(value)) continue
      if (value < low) low = value
      if (value > high) high = value
    }
    if (Number.isFinite(low) && high > low) heights.push(high - low)
  }
  if (!heights.length) return 0
  heights.sort((a, b) => a - b)
  const middle = heights.length % 2
    ? heights[(heights.length - 1) / 2]!
    : (heights[heights.length / 2 - 1]! + heights[heights.length / 2]!) / 2
  return middle * gap
}

/** 몇 번째 칸에 앉는가 — **보이는 것들 사이에서의 차례**다.
 *
 *  꺼 둔 스윕이 제 칸을 지키게 하면 그림 가운데에 빈 띠가 남고, 그 빈 띠는
 *  "여기 측정이 없다" 로 읽힌다.  꺼면 접히고 켜면 도로 자리가 난다.
 */
export function stackOffsets(series: Stackable[], step: number): number[] {
  let slot = 0
  return series.map((one) => (one.hidden ? Number.NaN : step * slot++))
}
