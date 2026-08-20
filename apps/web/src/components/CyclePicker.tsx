/** Choose which cycles to plot, and read the chosen cycle's numbers. */

import { useState } from 'react'

import { basisUnit, num, parseCycleSpec, pct, spread } from '../lib/format'
import type { Basis, Cycle } from '../lib/types'

export function CyclePicker({
  cycles,
  value,
  onChange,
  basis,
}: {
  cycles: Cycle[]
  value: number[]
  onChange: (cycles: number[]) => void
  basis: Basis
}) {
  const available = cycles.map((c) => c.cycle)
  const [spec, setSpec] = useState(value.join(','))
  const [invalid, setInvalid] = useState(false)

  function apply(text: string) {
    setSpec(text)
    const parsed = parseCycleSpec(text, available)
    setInvalid(text.trim() !== '' && parsed.length === 0)
    if (parsed.length) onChange(parsed.slice(0, 40))
  }

  function preset(picks: number[]) {
    setInvalid(false)
    setSpec(picks.join(','))
    onChange(picks)
  }

  const last = available.at(-1)
  const focus = cycles.find((c) => c.cycle === value.at(-1))

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
        <button type="button" className="sm" onClick={() => preset(available.slice(0, 1))}>
          첫 사이클
        </button>
        <button
          type="button"
          className="sm"
          disabled={!last}
          onClick={() => preset(last ? [last] : [])}
        >
          마지막
        </button>
        <button type="button" className="sm" onClick={() => preset(spread(available, 8))}>
          균등 8개
        </button>
        <button
          type="button"
          className="sm"
          onClick={() => preset(available.slice(0, 40))}
          title="최대 40개"
        >
          전체
        </button>
      </div>

      {invalid ? (
        <div className="tiny" style={{ color: 'var(--danger)' }}>
          선택된 사이클이 없습니다. 이 셀은 {available.at(0)}–{last}번을 가지고 있습니다.
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
