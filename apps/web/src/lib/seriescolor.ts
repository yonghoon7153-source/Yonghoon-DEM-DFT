/** 곡선 색 하나를 **모든 그리는 곳이 같게** 읽는다.
 *
 *  전에는 이 규칙이 `Plot.tsx` 안에만 있었다.  그래서 화면 범례와 2D 곡선은
 *  테마 토큰(`--series-0`)을 쓰는데 `Plot3D` 의 곡선과 PNG 범례는 팔레트의
 *  원래 hex 를 그대로 썼고, 어두운 화면에서 같은 계열이 서로 다른 색으로
 *  나왔다 — 실측 대비 7.00:1 대 2.66:1 (Codex 그림 리뷰 #8).
 *
 *  캔버스에는 CSS 상속이 없다.  `var(--discharge)` 를 그대로 넘기면 선이
 *  **안 보이는 색**으로 그려지고 아무도 오류를 못 본다.  그래서 토큰을 여기서
 *  실제 색으로 푼다.
 */

import { SERIES_COLORS, seriesColor } from './format'

export function cssVar(name: string, fallback: string): string {
  if (typeof window === 'undefined') return fallback
  const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim()
  return value || fallback
}

/** `var(--토큰, 대체)` 를 실제 색으로.  토큰이 아니면 그대로 돌려준다. */
export function resolveColor(color: string | undefined, fallback: string): string {
  if (!color) return fallback
  const token = color.match(/^var\(\s*(--[\w-]+)\s*(?:,\s*(.+?))?\s*\)$/)
  if (!token) return color
  return cssVar(token[1]!, token[2]?.trim() ?? fallback)
}

/** 팔레트 색을 테마 토큰으로 바꿔 준다.
 *
 *  `SERIES_COLORS` 는 밝은 화면 전용 상수인데 부르는 쪽이 그 hex 를 그대로
 *  넘긴다.  어두운 바탕에서 회색과 짙은 파랑이 2.4:1 까지 떨어져 — 선이
 *  보이려면 3:1 이 필요하다 — 팔레트 자리를 되찾아 `var(--series-N, <hex>)`
 *  로 다시 쓴다.  팔레트가 아닌 색(부르는 쪽의 토큰이나 일회용)은 그대로 둔다.
 */
export function seriesToken(color: string | undefined, index: number): string {
  const slot = color
    ? SERIES_COLORS.indexOf(color.trim().toLowerCase())
    : index % SERIES_COLORS.length
  if (slot < 0) return color as string
  return `var(--series-${slot}, ${SERIES_COLORS[slot]})`
}

/** 그릴 때 쓸 최종 색 — 토큰까지 푼 것.  캔버스·SVG 가 이것을 받는다. */
export function paintColor(color: string | undefined, index: number): string {
  return resolveColor(seriesToken(color, index), seriesColor(index))
}
