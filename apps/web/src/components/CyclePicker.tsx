/** Choose which cycles to plot, and read the chosen cycle's numbers. */

import { useEffect, useRef, useState } from 'react'

import { basisUnit, num, parseCycleSpec, pct, spread } from '../lib/format'
import { ko } from '../lib/i18n'
import type { Basis, Cycle, PartialCycle } from '../lib/types'

/** As many cycles as the API will draw in one response.  Keep in step with
 *  `_PROFILE_CYCLE_LIMIT` in apps/api/app/routers/analysis.py. */
export const MAX_DRAWN_CYCLES = 400

export function CyclePicker({
  cycles,
  value,
  onChange,
  basis,
  partial = [],
}: {
  cycles: Cycle[]
  value: number[]
  onChange: (cycles: number[]) => void
  basis: Basis
  /** 숫자는 없지만 곡선은 그릴 수 있는 사이클들.  비어 있으면 없는 것과 같다 --
   *  고를 수 없는 번호를 목록에 넣으면 `전체` 가 그릴 수 없는 것을 고른다. */
  partial?: PartialCycle[]
}) {
  const available = [...cycles.map((c) => c.cycle), ...partial.map((p) => p.cycle)].sort(
    (a, b) => a - b,
  )
  const [spec, setSpec] = useState(() => value.join(','))
  const [invalid, setInvalid] = useState(false)
  // What this box last handed upward.  The selection also changes from
  // elsewhere -- clicking a row in the cycle table, the table's own 초기화 --
  // and without somewhere to compare against, the text and the plot drift
  // apart: the graph shows four curves and the box still says what was typed
  // ten clicks ago.
  const emitted = useRef(value.join(','))
  const incoming = value.join(',')

  useEffect(() => {
    if (incoming === emitted.current) return
    emitted.current = incoming
    setSpec(incoming)
    setInvalid(false)
  }, [incoming])

  function send(picks: number[]) {
    emitted.current = picks.join(',')
    onChange(picks)
  }

  function apply(text: string) {
    setSpec(text)
    const parsed = parseCycleSpec(text, available)
    setInvalid(text.trim() !== '' && parsed.length === 0)
    // An emptied box means an empty selection, not "keep the last one".
    if (text.trim() === '') send([])
    else if (parsed.length) send(parsed.slice(0, MAX_DRAWN_CYCLES))
  }

  function preset(picks: number[]) {
    setInvalid(false)
    setSpec(picks.join(','))
    send(picks)
  }

  /** 이 사이클 **하나만** 남긴다.
   *
   *  한동안 이 둘은 토글이었다 (선택에 더하고 빼기).  "처음과 지금을 나란히"
   *  를 손으로 안 치고 보게 하려던 것이었는데, 쓰는 사람에게는 **누른 것이
   *  안 먹는 것**으로 읽혔다: 이미 열 곡선이 그려져 있으면 거기에 한 줄이
   *  더해질 뿐이라 어느 것이 1번인지 안 보이고, 한 번 더 누르면 사라진다 —
   *  "나타났다가 사라졌다가 한다" (F&Q, 2026-08-30).
   *
   *  같은 줄의 다른 단추는 전부 **갈아치운다** (초기화 · 균등 8개 · 전체).
   *  이 둘만 달랐고, 그래서 이 둘만 예측이 안 됐다.
   *
   *  **더하는 자리는 그대로 있다**: 사이클 표의 행은 여전히 토글이다
   *  ("행을 누르면 프로파일에 추가·제거됩니다").  처음과 지금을 나란히
   *  보려면 `첫 사이클` 을 누르고 표에서 마지막 행을 누른다. */
  function only(cycle: number | undefined) {
    if (cycle === undefined) return
    preset([cycle])
  }

  /** 지금 보고 있는 것이 **딱 이것 하나**인가.
   *
   *  `includes` 로 두면 1·5·9 를 보고 있을 때도 `첫 사이클` 이 켜져 보이는데,
   *  그 단추를 누르면 화면이 바뀐다 — 켜진 단추는 누를 것이 없어야 한다. */
  const onlyOne = (cycle: number | undefined) =>
    cycle !== undefined && value.length === 1 && value[0] === cycle

  const first = available.at(0)
  const last = available.at(-1)
  const focus = cycles.find((c) => c.cycle === value.at(-1))
  // 고른 것이 숫자 없는 사이클이면 그렇게 말한다.  숫자 줄이 그냥 사라지면
  // 방금 누른 것이 안 먹은 것으로 읽힌다.
  const focusPartial = focus
    ? undefined
    : partial.find((item) => item.cycle === value.at(-1))
  const capped = available.length > MAX_DRAWN_CYCLES

  return (
    <div className="col" style={{ gap: 8 }}>
      <div className="row">
        <input
          type="text"
          value={spec}
          onChange={(event) => apply(event.target.value)}
          placeholder="예: 1,3,10-20 또는 all"
          style={{ maxWidth: 220, borderColor: invalid ? 'var(--danger)' : undefined }}
          aria-label="사이클 선택"
        />
        <button
          type="button"
          className="sm"
          disabled={!value.length}
          onClick={() => preset([])}
          title="선택을 모두 지웁니다"
        >
          초기화
        </button>
        <button
          type="button"
          className={`sm${onlyOne(first) ? ' on' : ''}`}
          disabled={first === undefined}
          onClick={() => only(first)}
          title="첫 사이클만 남깁니다 — 더하려면 사이클 표의 행을 누르세요"
        >
          첫 사이클
        </button>
        <button
          type="button"
          className={`sm${onlyOne(last) ? ' on' : ''}`}
          disabled={last === undefined}
          onClick={() => only(last)}
          title="마지막 사이클만 남깁니다 — 더하려면 사이클 표의 행을 누르세요"
        >
          마지막
        </button>
        <button type="button" className="sm" onClick={() => preset(spread(available, 8))}>
          균등 8개
        </button>
        <button
          type="button"
          className="sm"
          onClick={() => preset(available.slice(0, MAX_DRAWN_CYCLES))}
          title={capped ? `최대 ${MAX_DRAWN_CYCLES}개` : `${available.length}개 전부`}
        >
          전체
        </button>
      </div>

      {invalid ? (
        <div className="tiny" style={{ color: 'var(--danger)' }}>
          선택된 사이클이 없습니다. 이 셀은 {available.at(0)}–{last}번을 가지고 있습니다.
        </div>
      ) : null}

      {focusPartial ? (
        <div className="row small" style={{ gap: 14 }}>
          <span className="dim">{focusPartial.cycle}번</span>
          <span className="faint">
            {ko.partialReason(focusPartial.reason)} — 곡선은 그리지만 사이클 용량은
            없습니다
          </span>
        </div>
      ) : null}

      {focus ? (
        <div className="row small" style={{ gap: 14 }}>
          <span className="dim">{focus.cycle}번</span>
          <span className="mono">
            방전 {num(focus.discharge_capacity)} {basisUnit(basis)}
          </span>
          <span className="mono">
            충전 {num(focus.charge_capacity)} {basisUnit(basis)}
          </span>
          <span className="mono">CE {pct(focus.coulombic_efficiency)}%</span>
          {focus.retention_pct !== null ? (
            <span className="mono">유지율 {pct(focus.retention_pct, 1)}%</span>
          ) : null}
          {focus.voltage_hysteresis !== null ? (
            <span className="mono">ΔV {num(focus.voltage_hysteresis, 3)} V</span>
          ) : null}
        </div>
      ) : null}
    </div>
  )
}
