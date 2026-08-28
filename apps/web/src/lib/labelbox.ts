/** 글자가 차지하는 자리 — 겹치는 축 글자를 빼기 위한 어림자.
 *
 *  3D 그림은 축 셋을 **한 화면 안에서 돌린다.**  돌리면 가로축의 끝과 깊이축의
 *  시작이 같은 모서리로 모이는 각도가 반드시 생기고, 거기서 두 축의 눈금
 *  글자가 포개진다 (실제로 `2.00` 이 스펙트럼 이름 위에 찍혔다).  2D 그림은
 *  uPlot 이 알아서 빼 주지만 이 그림은 우리가 그린다.
 *
 *  **왜 재지 않고 어림하는가.**  SVG 글자의 실제 폭은 `getComputedTextLength()`
 *  로 잴 수 있지만 그것은 **그린 뒤**에만 된다 — 그리기 전에 무엇을 뺄지
 *  정해야 하는 우리에게는 한 박자 늦다 (그리고 각도가 바뀔 때마다 다시 그려야
 *  하므로 매 프레임 레이아웃을 두 번 하게 된다).  그래서 글자 종류별 폭으로
 *  어림한다: 한글·한자는 한 칸을 다 쓰고, 라틴은 절반쯤이다.  Chromium 에서
 *  실측한 값에 맞춰 놓았다 (`스펙트럼` 44 px, `Dcell12_4_C06` 81 px, 11 px 글꼴).
 *
 *  어림이므로 **조금 넓게 잡는 쪽**이 안전하다 — 좁게 잡으면 겹친 것을 못
 *  보고 그대로 찍는다.  `overlaps` 의 `pad` 가 그 여유다.
 */

/** 글자 하나가 쓰는 폭 (글꼴 크기의 배수). */
function charEm(ch: string): number {
  const code = ch.codePointAt(0) ?? 0
  // 한글·한자·가나·전각 — 한 칸을 다 쓴다.
  if (code >= 0x1100 && code <= 0x115f) return 1
  if (code >= 0x2e80 && code <= 0xa4cf) return 1
  if (code >= 0xac00 && code <= 0xd7a3) return 1
  if (code >= 0xf900 && code <= 0xfaff) return 1
  if (code >= 0xfe30 && code <= 0xfe6f) return 1
  if (code >= 0xff00 && code <= 0xff60) return 1
  if ('.,:;\'`|!iltj'.includes(ch)) return 0.32
  if (ch === ' ' || ch === '-' || ch === '(' || ch === ')') return 0.33
  if (ch >= '0' && ch <= '9') return 0.62
  if (ch >= 'A' && ch <= 'Z') return 0.66
  return 0.55
}

/** 글자열의 폭 어림 (px). */
export function textWidth(text: string, size: number): number {
  let em = 0
  for (const ch of text) em += charEm(ch)
  return em * size
}

export interface LabelBox { x: number; y: number; w: number; h: number }

/** SVG `<text>` 하나가 덮는 네모.
 *
 *  `at.y` 는 **밑줄**(baseline)이다.  글자 상자는 그 위로 올라간다.
 */
export function labelBox(
  at: { x: number; y: number },
  text: string,
  size: number,
  anchor: 'start' | 'middle' | 'end' = 'middle',
): LabelBox {
  const w = textWidth(text, size)
  const x = anchor === 'middle' ? at.x - w / 2 : anchor === 'end' ? at.x - w : at.x
  return { x, y: at.y - size * 0.95, w, h: size * 1.2 }
}

/** 두 네모가 겹치는가.  `pad` 만큼 서로 부풀려서 본다 (닿기 직전도 겹침). */
export function overlaps(a: LabelBox, b: LabelBox, pad = 0): boolean {
  return !(a.x + a.w + pad <= b.x || b.x + b.w + pad <= a.x
    || a.y + a.h + pad <= b.y || b.y + b.h + pad <= a.y)
}

/** 자리를 다투는 글자들 중 **찍을 것**을 고른다.  먼저 온 것이 이긴다.
 *
 *  `keep` 인 것은 겹쳐도 안 뺀다 (축 이름).  대신 자리는 그대로 차지하므로,
 *  뒤에 오는 눈금이 그 자리를 피한다.
 *
 *  돌려주는 것은 **찍을 것들의 열쇠**다.  부르는 쪽이 그리면서 `has()` 로
 *  묻는다 — 눈금 **선**은 그대로 그리고 **글자만** 빼기 때문이다.  선까지
 *  빼면 그 자리에 눈금이 있었다는 것조차 사라진다.
 */
export function placeLabels(
  items: { key: string; box: LabelBox; keep?: boolean }[],
  pad = 3,
): Set<string> {
  const taken: LabelBox[] = []
  const out = new Set<string>()
  for (const one of items) {
    if (!one.keep && taken.some((box) => overlaps(box, one.box, pad))) continue
    taken.push(one.box)
    out.add(one.key)
  }
  return out
}
