/** SOC 스캔을 비껴 쌓아 한눈에 — 논문의 그 3D 그림.
 *
 *  **왜 필요한가.**  스윕 열하나를 같은 축에 겹쳐 그리면 반원들이 서로를 덮는다.
 *  SOC 를 따라 아크가 커지는지 작아지는지가 이 스캔을 여는 이유인데, 겹쳐 놓으면
 *  가장 큰 것 하나만 보이고 나머지는 그 안에 숨는다.  논문이 이럴 때 쓰는 것이
 *  깊이 축이다: SOC 가 올라갈수록 곡선을 조금씩 밀어 계단처럼 세운다.
 *
 *  **진짜 3D 가 아니라 비껴 쌓기다.**  회전도 원근도 없다 — 깊이만큼 오른쪽·위로
 *  민 것이고, MATLAB 의 3D 뷰를 정면에서 본 그림이 실제로 그 모양이다.  회전이
 *  없으니 마우스로 돌릴 수도 없고, 그것이 이 그림의 한계다.
 *
 *  **그래서 값이 옮겨진다.**  민 곡선의 `Z′` 는 더 이상 그 스윕의 `Z′` 가
 *  아니다.  부르는 쪽이 축 이름과 설명에 그렇게 적어야 한다 (§0.4) — 이 그림은
 *  **모양을 보는 것**이지 값을 읽는 것이 아니다.  값은 2D 로 돌아가서 읽는다.
 *
 *  **깊이는 전위(V) 다.**  우리 파일은 SOC 를 % 로 말해 주지 않는다 (계측기가
 *  아는 것은 그때의 전위와 용량이다).  그래서 논문의 `SOC 0 % · 50 % · 100 %`
 *  자리에 실제 전위가 들어간다 — 지어내지 않는다.
 */

/** 얼마나 밀까 — 그림 폭·높이에 대한 비율.
 *
 *  가로보다 세로를 크게 잡는다.  나이퀴스트에서 곡선은 옆으로 길고 위로 얕아서,
 *  같은 비율로 밀면 계단이 아니라 한 줄로 이어져 보인다.
 */
const SHEAR_X = 0.42
const SHEAR_Y = 0.62

export interface Stackable {
  x: number[]
  y: number[]
}

export interface Stacked<T> {
  series: T[]
  /** 계열마다 얼마나 밀렸나 — 깊이 축(안내선)을 그리는 데 쓴다. */
  offsets: { dx: number; dy: number; depth: number | null }[]
  /** 깊이로 실제로 쓴 값의 범위.  못 쓰면 `null` (그때는 차례로 민다). */
  span: { low: number; high: number } | null
}

/** 계열들을 깊이 순서로 비껴 쌓는다.
 *
 *  `depths[i]` 가 그 계열의 깊이(전위 V)다.  `null` 이 섞여 있으면 **차례**로
 *  민다 — 어떤 스윕만 전위를 아는 스캔에서 아는 것만 밀면 모르는 것들이 한
 *  자리에 겹쳐 쌓여, 그 겹침이 물리로 읽힌다.
 */
export function stack<T extends Stackable>(
  series: T[],
  depths: (number | null)[],
): Stacked<T> {
  if (!series.length) return { series, offsets: [], span: null }

  let low = Infinity
  let high = -Infinity
  for (const value of depths) {
    if (value === null || !Number.isFinite(value)) continue
    if (value < low) low = value
    if (value > high) high = value
  }
  // 깊이를 하나라도 모르면 차례로 민다.  아는 것만 밀면 모르는 것들이 한
  // 자리에 겹치고, 그 겹침을 사람이 "같은 상태" 로 읽는다.
  const usable = depths.length === series.length
    && depths.every((value) => value !== null && Number.isFinite(value))
    && high > low
  const fraction = (index: number) => {
    if (!usable) return series.length > 1 ? index / (series.length - 1) : 0
    return ((depths[index] as number) - low) / (high - low)
  }

  // 밀 거리는 **그림 자신의 크기**에 맞춘다.  고정 픽셀로 밀면 저항이 작은
  // 셀에서는 계단이 산더미가 되고 큰 셀에서는 안 보인다.
  let xLow = Infinity
  let xHigh = -Infinity
  let yLow = Infinity
  let yHigh = -Infinity
  for (const item of series) {
    for (const value of item.x) {
      if (!Number.isFinite(value)) continue
      if (value < xLow) xLow = value
      if (value > xHigh) xHigh = value
    }
    for (const value of item.y) {
      if (!Number.isFinite(value)) continue
      if (value < yLow) yLow = value
      if (value > yHigh) yHigh = value
    }
  }
  const xSpan = Number.isFinite(xHigh - xLow) && xHigh > xLow ? xHigh - xLow : 1
  const ySpan = Number.isFinite(yHigh - yLow) && yHigh > yLow ? yHigh - yLow : 1

  const offsets = series.map((_, index) => {
    const t = fraction(index)
    return {
      dx: t * xSpan * SHEAR_X,
      dy: t * ySpan * SHEAR_Y,
      depth: usable ? (depths[index] as number) : null,
    }
  })

  return {
    series: series.map((item, index) => ({
      ...item,
      x: item.x.map((value) => value + offsets[index]!.dx),
      y: item.y.map((value) => value + offsets[index]!.dy),
    })),
    offsets,
    span: usable ? { low, high } : null,
  }
}

/** 깊이 축 안내선 — 밀린 원점들을 잇는 선.
 *
 *  이 선이 없으면 계단이 그냥 흩어진 곡선 열하나로 보인다.  선 하나가 "이
 *  방향이 깊이" 라고 말해 주고, 그 끝의 두 숫자(가장 낮은 전위와 가장 높은
 *  전위)가 눈금 노릇을 한다.
 */
export function depthGuide(
  offsets: { dx: number; dy: number }[],
  origin: { x: number; y: number },
): { x: number[]; y: number[] } {
  return {
    x: offsets.map((one) => origin.x + one.dx),
    y: offsets.map((one) => origin.y + one.dy),
  }
}
