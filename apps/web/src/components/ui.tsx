/** Small presentational pieces shared across pages. */

import type { ReactNode } from 'react'

import { basisUnit, num } from '../lib/format'
import type { Basis, CellState } from '../lib/types'

export function Card({
  title,
  actions,
  children,
  tight,
}: {
  title?: ReactNode
  actions?: ReactNode
  children: ReactNode
  tight?: boolean
}) {
  return (
    <section className="card">
      {(title || actions) && (
        <header>
          {title}
          <span className="spacer" />
          {actions}
        </header>
      )}
      <div className={tight ? 'body tight' : 'body'}>{children}</div>
    </section>
  )
}

export function Metric({
  label,
  value,
  unit,
  note,
  muted,
}: {
  label: string
  value: ReactNode
  unit?: string
  note?: ReactNode
  muted?: boolean
}) {
  return (
    <div className="metric">
      <div className="label">{label}</div>
      <div className={muted ? 'value muted' : 'value'}>
        {value}
        {unit ? <span className="unit">{unit}</span> : null}
      </div>
      {note ? <div className="note">{note}</div> : null}
    </div>
  )
}

export function CapacityMetric({
  label,
  value,
  basis,
  note,
}: {
  label: string
  value: number | null | undefined
  basis: Basis
  note?: ReactNode
}) {
  return (
    <Metric
      label={label}
      value={num(value)}
      unit={basisUnit(basis)}
      note={note}
      muted={value === null || value === undefined}
    />
  )
}

const STATE_TEXT: Record<CellState, string> = {
  running: '구동 중',
  finished: '사이클 종료',
  unknown: '상태 불명',
}

export function StateBadge({
  state,
  confidence,
  cycle,
}: {
  state: CellState
  confidence?: string
  cycle?: number | null
}) {
  return (
    <span className={`badge ${state}`} title={confidence ? `근거 신뢰도: ${confidence}` : undefined}>
      {state === 'running' ? <span className="pulse" /> : null}
      {STATE_TEXT[state]}
      {state === 'running' && cycle ? ` · ${cycle}번째 진행` : ''}
    </span>
  )
}

export function Spinner({ label }: { label?: string }) {
  return (
    <span className="row small dim">
      <span className="spinner" />
      {label ?? '불러오는 중'}
    </span>
  )
}

export function Alert({
  kind = 'info',
  children,
}: {
  kind?: 'info' | 'warn' | 'error'
  children: ReactNode
}) {
  return <div className={`alert ${kind}`}>{children}</div>
}

export function Empty({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div className="empty">
      <div className="big">{title}</div>
      {children}
    </div>
  )
}

export function Field({
  label,
  hint,
  children,
}: {
  label: string
  hint?: string
  children: ReactNode
}) {
  return (
    <label className="field">
      <span>
        {label}
        {hint ? <span className="hint"> · {hint}</span> : null}
      </span>
      {children}
    </label>
  )
}

export function NumberField({
  label,
  hint,
  value,
  onChange,
  step = 'any',
  min,
  placeholder,
}: {
  label: string
  hint?: string
  value: number | null | undefined
  onChange: (value: number | null) => void
  step?: string | number
  min?: number
  placeholder?: string
}) {
  return (
    <Field label={label} hint={hint}>
      <input
        type="number"
        step={step}
        min={min}
        placeholder={placeholder}
        value={value ?? ''}
        onChange={(event) => {
          const raw = event.target.value
          onChange(raw === '' ? null : Number(raw))
        }}
      />
    </Field>
  )
}
