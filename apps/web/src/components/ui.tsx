/** Small presentational pieces shared across pages. */

import type { ReactNode } from 'react'

import { basisUnit, num } from '../lib/format'
import type { Basis, CellState, Component } from '../lib/types'

export function Card({
  title,
  actions,
  children,
  tight,
  padSmall,
}: {
  title?: ReactNode
  actions?: ReactNode
  children: ReactNode
  tight?: boolean
  padSmall?: boolean
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
      <div className={tight ? 'body tight' : padSmall ? 'body pad-sm' : 'body'}>{children}</div>
    </section>
  )
}

/** Hairline-separated readout. Use for the numbers that answer the question. */
export function MetricBand({ children }: { children: ReactNode }) {
  return <div className="metric-band">{children}</div>
}

export function Metric({
  label,
  value,
  unit,
  note,
  muted,
  accent,
}: {
  label: string
  value: ReactNode
  unit?: string
  note?: ReactNode
  muted?: boolean
  accent?: boolean
}) {
  const className = ['value', muted ? 'muted' : '', accent ? 'accent' : '']
    .filter(Boolean)
    .join(' ')
  return (
    <div className="metric">
      <div className="label" title={label}>
        {label}
      </div>
      <div className={className}>
        <span>{value}</span>
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
  accent,
}: {
  label: string
  value: number | null | undefined
  basis: Basis
  note?: ReactNode
  accent?: boolean
}) {
  const missing = value === null || value === undefined
  return (
    <Metric
      label={label}
      value={num(value)}
      unit={missing ? undefined : basisUnit(basis)}
      note={note}
      muted={missing}
      accent={accent}
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
    <span
      className={`badge ${state}`}
      title={confidence ? `근거 신뢰도: ${confidence}` : undefined}
    >
      {state === 'running' ? <span className="pulse" /> : null}
      {STATE_TEXT[state]}
      {state === 'running' && cycle ? ` · ${cycle}번째 진행` : ''}
    </span>
  )
}

const ROLE_COLORS: Record<string, string> = {
  active: 'var(--accent)',
  electrolyte: 'var(--pos)',
  conductive: 'var(--ink-3)',
  binder: 'var(--warn)',
  other: 'var(--ink-4)',
}

/** The electrode blend, one chip per component. Zeros stay, dimmed. */
export function CompositionChips({
  components,
  showZero = true,
}: {
  components: Component[]
  showZero?: boolean
}) {
  const shown = showZero ? components : components.filter((c) => c.wt_percent > 0)
  if (!shown.length) return <span className="faint tiny">조성 미입력</span>
  return (
    <div className="chip-row">
      {shown.map((component, index) => (
        <span
          key={`${component.name}-${index}`}
          className={[
            'chip',
            component.wt_percent <= 0 ? 'zero' : '',
            component.role === 'active' ? 'active' : '',
          ]
            .filter(Boolean)
            .join(' ')}
          title={component.role}
        >
          <span className="dot" style={{ background: ROLE_COLORS[component.role] ?? 'var(--ink-4)' }} />
          {component.name}
          <span className="pct">{component.wt_percent}</span>
        </span>
      ))}
    </div>
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

/** Placeholder rows that keep the layout from jumping while data loads. */
export function TableSkeleton({ rows = 5, columns = 6 }: { rows?: number; columns?: number }) {
  return (
    <div style={{ padding: '12px 16px' }}>
      {Array.from({ length: rows }, (_, row) => (
        <div key={row} className="row" style={{ gap: 12, marginBottom: 9 }}>
          {Array.from({ length: columns }, (_, column) => (
            <div
              key={column}
              className="skeleton"
              style={{
                height: 12,
                flex: column === 0 ? 2 : 1,
                opacity: 1 - row * 0.13,
              }}
            />
          ))}
        </div>
      ))}
    </div>
  )
}

export function Alert({
  kind = 'info',
  children,
}: {
  kind?: 'info' | 'warn' | 'error'
  children: ReactNode
}) {
  return (
    <div className={`alert ${kind}`}>
      <span aria-hidden="true">{kind === 'error' ? '✕' : kind === 'warn' ? '!' : 'i'}</span>
      <span>{children}</span>
    </div>
  )
}

export function Empty({
  title,
  icon,
  children,
}: {
  title: string
  icon?: string
  children?: ReactNode
}) {
  return (
    <div className="empty">
      {icon ? <div className="icon">{icon}</div> : null}
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

/** Key/value list for dense metadata panels. */
export function KeyValues({ rows }: { rows: [string, ReactNode][] }) {
  return (
    <dl className="kv">
      {rows.map(([key, value]) => (
        <div key={key}>
          <span className="k">{key}</span>
          <span className="v">{value}</span>
        </div>
      ))}
    </dl>
  )
}

/** 휴지통.  currentColor 를 쓰므로 버튼의 색(위험이면 빨강)을 그대로 따른다. */
export function TrashIcon({ size = 15 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.4"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
    >
      <path d="M2.5 4h11" />
      <path d="M6 4V2.8c0-.44.36-.8.8-.8h2.4c.44 0 .8.36.8.8V4" />
      <path d="M12.4 4l-.5 8.4c-.04.62-.55 1.1-1.17 1.1H5.27c-.62 0-1.13-.48-1.17-1.1L3.6 4" />
      <path d="M6.6 6.9v3.7M9.4 6.9v3.7" />
    </svg>
  )
}
