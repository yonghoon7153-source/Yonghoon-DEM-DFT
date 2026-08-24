/** 축 고정 — 사이클을 골라도 그래프가 같은 눈금 위에 남게 한다.
 *
 * 이것이 없을 때 실제로 일어난 일: dQ/dV 에서 전체 사이클을 보다가 1번 하나만
 * 누르면 y 축이 그 곡선에 맞춰 다시 잡히고, **같은 곡선이 훨씬 뚱뚱해 보인다.**
 * 봉우리가 커진 것처럼 읽히는데 숫자는 하나도 안 변했다. 프로파일의 x 축은
 * 이미 셀 전체 용량에 고정돼 있었지만(SampleDetail 의 capacityAxis), dQ/dV 의
 * y 축에는 그런 것이 없었다.
 *
 * 왜 자동으로 "전체 사이클 기준" 을 쓰지 않는가: 그 범위를 알려면 안 그릴
 * 사이클까지 전부 계산해야 한다. 400 사이클짜리 파일에서 아무도 안 보는 곡선
 * 800개를 미분하는 값은 없다. 그래서 **사람이 잠근다** — 지금 보이는 범위를
 * 그대로 얼려 두고, 숫자를 직접 고칠 수도 있게.
 *
 * 잠근 뒤에 단위가 바뀌면(mAh → mAh/g, 프로파일 → dQ/dV) 그 숫자는 다른 축의
 * 것이다. 그대로 두면 그래프가 빈 화면이 되므로 `resetKey` 가 바뀔 때 자동으로
 * 풀린다.
 */

import { useEffect, useMemo, useState } from 'react'

import type { PlotSeries } from './Plot'

export type AxisRange = [number | null, number | null]

export interface AxisLock {
  locked: boolean
  /** `Plot` 에 그대로 넘긴다. 안 잠갔으면 undefined — 자동 축이다. */
  range: AxisRange | undefined
  toggle: () => void
  setBound: (which: 0 | 1, value: string) => void
}

/** 지금 보이는 계열들의 y 범위. 숨긴 계열은 빼고, 여유를 조금 준다. */
export function visibleExtent(series: PlotSeries[], axis: 'x' | 'y'): AxisRange | null {
  let low = Number.POSITIVE_INFINITY
  let high = Number.NEGATIVE_INFINITY
  for (const item of series) {
    if (item.hidden) continue
    for (const value of axis === 'y' ? item.y : item.x) {
      if (!Number.isFinite(value)) continue
      if (value < low) low = value
      if (value > high) high = value
    }
  }
  if (!Number.isFinite(low) || !Number.isFinite(high)) return null
  if (low === high) {
    // 상수 곡선. 0 폭 축은 uPlot 이 그리지 못한다.
    const pad = Math.abs(low) * 0.05 || 1
    return [low - pad, high + pad]
  }
  // 여유 4 % — 봉우리 꼭대기가 축에 붙으면 잘린 것처럼 보인다.
  const pad = (high - low) * 0.04
  return [low - pad, high + pad]
}

/** 잠금 상태와 그 범위. `series` 는 잠그는 순간의 값을 읽는 데만 쓴다. */
export function useAxisLock(series: PlotSeries[], axis: 'x' | 'y',
                            resetKey: string): AxisLock {
  const [range, setRange] = useState<AxisRange | null>(null)

  // 단위가 바뀌면 잠근 숫자는 다른 축의 것이다.  풀지 않으면 빈 그래프가 되고,
  // 사람은 데이터가 없다고 생각한다.
  useEffect(() => {
    setRange(null)
  }, [resetKey])

  const toggle = () => {
    setRange((current) => (current ? null : visibleExtent(series, axis)))
  }

  const setBound = (which: 0 | 1, value: string) => {
    setRange((current) => {
      const base: AxisRange = current ?? visibleExtent(series, axis) ?? [null, null]
      const next: AxisRange = [base[0], base[1]]
      const parsed = Number(value)
      // 빈 칸은 "이쪽은 자동" 이라는 뜻이다.  0 은 유효한 경계이므로
      // falsy 검사로 걸러내면 안 된다.
      next[which] = value.trim() === '' || Number.isNaN(parsed) ? null : parsed
      return next
    })
  }

  return { locked: range !== null, range: range ?? undefined, toggle, setBound }
}

/** 잠금 버튼과 경계 두 칸. */
export function AxisLockControl({ lock, label = '축 고정', step = 'any' }: {
  lock: AxisLock
  label?: string
  step?: string
}) {
  const [low, high] = lock.range ?? [null, null]
  const text = useMemo(
    () => (value: number | null) => (value === null ? '' : String(round(value))),
    [],
  )
  return (
    <div className="row" style={{ gap: 6 }}>
      <button
        type="button"
        className={lock.locked ? 'sm on' : 'sm ghost'}
        aria-pressed={lock.locked}
        onClick={lock.toggle}
        title={
          lock.locked
            ? '축을 다시 자동으로 — 고른 사이클에 맞춰 눈금이 바뀝니다'
            : '지금 눈금을 고정 — 사이클을 바꿔도 곡선 크기를 그대로 비교할 수 있습니다'
        }
      >
        {lock.locked ? `🔒 ${label}` : `🔓 ${label}`}
      </button>
      {lock.locked ? (
        <>
          <input
            type="number"
            step={step}
            value={text(low)}
            onChange={(event) => lock.setBound(0, event.target.value)}
            style={{ width: 82 }}
            aria-label={`${label} 최소`}
            placeholder="자동"
          />
          <span className="tiny faint">~</span>
          <input
            type="number"
            step={step}
            value={text(high)}
            onChange={(event) => lock.setBound(1, event.target.value)}
            style={{ width: 82 }}
            aria-label={`${label} 최대`}
            placeholder="자동"
          />
        </>
      ) : null}
    </div>
  )
}

/** 칸에 넣을 만큼만 남긴다.  1e-9 짜리 dV/dQ 도 있으므로 자릿수로 자르지
 *  않고 유효숫자로 자른다. */
function round(value: number): number {
  if (value === 0) return 0
  const magnitude = Math.floor(Math.log10(Math.abs(value)))
  const digits = Math.max(0, Math.min(12, 4 - magnitude))
  return Number(value.toFixed(digits))
}
