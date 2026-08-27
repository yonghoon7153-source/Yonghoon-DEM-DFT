/** 임피던스 점 다루기 — 화면 여럿이 같은 규칙을 써야 하는 것들.
 *
 *  둘이다: 실수축 **위**에 있는 점을 어떻게 볼 것인가, 그리고 한 파일의 스윕
 *  여럿(SOC 스캔)을 어떻게 부를 것인가.
 */

import { num } from './format'

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

/** 이 줄이 SOC 스캔의 한 스윕인가.
 *
 *  파일이 말하는 것이지 사람이 붙인 꼬리표가 아니다 — 한 줄은 `(sha256,
 *  sweep_index)` 이고 (ADR 0022), 스윕이 둘 이상이면 그 파일은 스캔이다.
 *  라이브러리·비교·스캔 상세 세 화면이 같은 판정을 써야 한 화면에서 "스캔"
 *  인 것이 다른 화면에서 낱장 스무 개로 흩어지지 않는다.
 */
export function isScan(item: { sweep_count?: number | null }): boolean {
  return (item.sweep_count ?? 1) > 1
}

/** 이 스윕을 **어느 상태에서** 잰 것인가 — SOC 스캔에서 스윕을 구별하는 값.
 *
 *  용량이 있으면 용량, 없으면 전위.  `#3` 만으로는 순서밖에 모르는데, 사람이
 *  고를 때 보는 것은 순서가 아니라 그 SOC 다.
 *
 *  둘 다 없으면 **빈 문자열**이다.  `0 mAh` 로 적으면 만방전과 구분되지 않는다
 *  (§0.4: 모르면 모른다고 적는다).
 */
export function sweepAt(
  item: { capacity_mah?: number | null; potential_v?: number | null },
  digits = 3,
): string {
  if (item.capacity_mah !== null && item.capacity_mah !== undefined) {
    return `${num(item.capacity_mah, digits)} mAh`
  }
  if (item.potential_v !== null && item.potential_v !== undefined) {
    return `${num(item.potential_v, digits)} V`
  }
  return ''
}

/** 아크가 사는 구간 — 나이퀴스트에서 **반원들만** 남기는 창.
 *
 *  `y ≥ 0` 은 실수축 위(유도성 꼬리)를 빼 준다.  그것으로 안 되는 경우가 하나
 *  더 있다: **확산 꼬리**.  전고체 풀셀의 45° 직선이나 전송선의 저주파 갈래는
 *  −Z″ 를 반원 높이의 몇 배까지 끌어올리고, 세로 눈금은 하나라서 정작 회로를
 *  고를 때 보는 반원이 바닥에 눌린다 (`equalAspect` 때문에 가로도 함께 늘어난다).
 *
 *  **어디까지가 아크인가.**  아크는 올라갔다 내려오고, 꼬리는 올라가서 안
 *  내려온다.  그래서 마지막 **골짜기**(내려왔다 다시 올라가기 시작하는 자리)가
 *  경계다.  마지막이라야 하는 이유: 아크가 둘이면 그 사이에도 골짜기가 있고,
 *  첫 골짜기에서 자르면 두 번째 반원을 잘라 버린다.
 *
 *  **자를지 말지.**  골짜기 뒤가 아크보다 낮으면 자르지 않는다 — 꼬리가 작으면
 *  전부 보이는 편이 낫고, 그때 `y ≥ 0` 은 예전 그대로 동작한다.  꼬리가 아크만큼
 *  높아졌을 때만 자른다 ("반원 크기보다 확산이 훨씬 클 때").
 *
 *  잡음으로 생긴 오르내림을 골짜기로 세지 않으려고 전체 높이의 2 % 를 문턱으로
 *  둔다.  못 찾으면 `null` 이고, 부르는 쪽은 예전 규칙(`y ≥ 0`)을 쓴다.
 */
export function arcWindow(
  points: { x: number[]; y: number[] }[],
): { xMax: number; yMax: number } | null {
  //: x 오름차순으로 모은다.  계열이 여럿이면 (스윕 겹쳐보기) 한 곡선처럼 본다 —
  //  창은 화면 하나에 하나고, 어느 스윕의 아크든 다 들어와야 한다.
  const all: { x: number; y: number }[] = []
  for (const item of points) {
    for (let i = 0; i < item.x.length; i += 1) {
      const x = item.x[i]
      const y = item.y[i]
      if (x === undefined || y === undefined) continue
      if (!Number.isFinite(x) || !Number.isFinite(y) || y < 0) continue
      all.push({ x, y })
    }
  }
  if (all.length < 5) return null
  all.sort((a, b) => a.x - b.x)

  const peak = Math.max(...all.map((one) => one.y))
  if (!(peak > 0)) return null
  const tol = peak * 0.02

  // 오르내림을 세면서 **마지막 골짜기**를 찾는다.
  //
  // 자리(index)로 센다.  값으로 찾으면 반원의 양 끝이 둘 다 y=0 이라 골짜기를
  // 첫 점에서 찾아 버리고, 그러면 아크가 통째로 잘린다.
  let cut = -1
  let rising = true
  let mark = all[0]!.y
  let markAt = 0
  for (let i = 0; i < all.length; i += 1) {
    const value = all[i]!.y
    if (rising) {
      if (value > mark) { mark = value; markAt = i }
      else if (mark - value > tol) { rising = false; mark = value; markAt = i }
      continue
    }
    if (value < mark) { mark = value; markAt = i }
    else if (value - mark > tol) {
      // 여기서 다시 오르기 시작했다 — 방금 지나온 바닥이 골짜기다.
      cut = markAt
      rising = true
      mark = value
      markAt = i
    }
  }
  if (cut <= 0) return null
  const arcs = all.slice(0, cut + 1)
  const tail = all.slice(cut + 1)
  if (!tail.length) return null

  const arcTop = Math.max(...arcs.map((one) => one.y))
  const tailTop = Math.max(...tail.map((one) => one.y))
  // 꼬리가 아크보다 낮으면 자를 이유가 없다.  전부 보이는 편이 낫다.
  if (tailTop < arcTop) return null

  // 골짜기에 딱 붙여 자르면 마지막 점이 테두리에 걸린다.  아크 폭의 10 % 만 더.
  const span = arcs[arcs.length - 1]!.x - arcs[0]!.x
  return { xMax: arcs[arcs.length - 1]!.x + span * 0.1, yMax: arcTop }
}
