/** The mass / area / composition inputs that drive every normalised number.
 *
 * Editing here writes straight to the sample: the raw mAh in the database is
 * untouched, so every table and plot re-normalises on the next fetch without
 * re-reading the 20 MB original (ADR 0001).
 */

import { useEffect, useState } from 'react'

import { api } from '../lib/api'
import { num } from '../lib/format'
import type { Sample } from '../lib/types'
import { Alert, Field, NumberField } from './ui'

type SpecKey =
  | 'total_mass_mg'
  | 'current_collector_mass_mg'
  | 'active_wt_percent'
  | 'active_mass_mg'
  | 'area_cm2'
  | 'diameter_mm'
  | 'thickness_um'
  | 'nominal_specific_capacity_mah_g'

const NOTE_LABELS: Record<string, string> = {
  active_mass: '활물질 질량',
  area: '면적',
  volume: '부피',
  nominal_capacity: '공칭 용량',
}

export function CellSpecPanel({
  sample,
  onSaved,
}: {
  sample: Sample
  onSaved: (sample: Sample) => void
}) {
  const [draft, setDraft] = useState<Record<SpecKey, number | null>>(() => pick(sample))
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => setDraft(pick(sample)), [sample])

  const dirty = (Object.keys(draft) as SpecKey[]).some(
    (key) => (draft[key] ?? null) !== (sample[key] ?? null),
  )

  async function save() {
    setSaving(true)
    setError(null)
    try {
      const body: Record<string, unknown> = {}
      const clear: string[] = []
      for (const key of Object.keys(draft) as SpecKey[]) {
        const value = draft[key]
        if (value === null) {
          if (sample[key] !== null) clear.push(key)
        } else if (value !== sample[key]) {
          body[key] = value
        }
      }
      if (clear.length) body.clear = clear
      onSaved(await api.updateSample(sample.id, body))
    } catch (cause) {
      setError(String(cause instanceof Error ? cause.message : cause))
    } finally {
      setSaving(false)
    }
  }

  const cell = sample.resolved_cell
  const set = (key: SpecKey) => (value: number | null) =>
    setDraft((previous) => ({ ...previous, [key]: value }))

  return (
    <div className="col">
      {error ? <Alert kind="error">{error}</Alert> : null}

      <div className="grid cols-2" style={{ gap: 10 }}>
        <NumberField
          label="전극 총 질량"
          hint="mg"
          value={draft.total_mass_mg}
          onChange={set('total_mass_mg')}
          min={0}
        />
        <NumberField
          label="활물질 함량"
          hint="wt%"
          value={draft.active_wt_percent}
          onChange={set('active_wt_percent')}
          min={0}
        />
        <NumberField
          label="집전체 질량"
          hint="mg · 빼고 계산"
          value={draft.current_collector_mass_mg}
          onChange={set('current_collector_mass_mg')}
          min={0}
        />
        <NumberField
          label="활물질 질량 직접 입력"
          hint="mg · 위 값보다 우선"
          value={draft.active_mass_mg}
          onChange={set('active_mass_mg')}
          min={0}
        />
        <NumberField
          label="전극 지름"
          hint="mm · 13pi = 13"
          value={draft.diameter_mm}
          onChange={set('diameter_mm')}
          min={0}
        />
        <NumberField
          label="전극 면적 직접 입력"
          hint="cm² · 지름보다 우선"
          value={draft.area_cm2}
          onChange={set('area_cm2')}
          min={0}
        />
        <NumberField
          label="전극 두께"
          hint="µm · mAh/cm³ 용"
          value={draft.thickness_um}
          onChange={set('thickness_um')}
          min={0}
        />
        <NumberField
          label="공칭 비용량"
          hint="mAh/g · C-rate 기준"
          value={draft.nominal_specific_capacity_mah_g}
          onChange={set('nominal_specific_capacity_mah_g')}
          min={0}
        />
      </div>

      <div className="row">
        <button type="button" className="primary" disabled={!dirty || saving} onClick={save}>
          {saving ? '저장 중…' : dirty ? '저장하고 다시 계산' : '저장됨'}
        </button>
        {dirty ? (
          <button type="button" className="ghost sm" onClick={() => setDraft(pick(sample))}>
            되돌리기
          </button>
        ) : null}
      </div>

      <div className="sep" />

      <dl className="small" style={{ margin: 0, display: 'grid', gap: 4 }}>
        <Derived
          label="활물질 질량"
          value={cell.active_mass_g ? `${num(cell.active_mass_g * 1000)} mg` : null}
          note={cell.notes.active_mass}
        />
        <Derived
          label="면적"
          value={cell.area_cm2 ? `${num(cell.area_cm2)} cm²` : null}
          note={cell.notes.area}
        />
        <Derived
          label="로딩"
          value={cell.loading_mg_cm2 ? `${num(cell.loading_mg_cm2, 3)} mg/cm²` : null}
        />
        <Derived
          label="공칭 용량"
          value={cell.nominal_capacity_mah ? `${num(cell.nominal_capacity_mah)} mAh` : null}
          note={cell.notes.nominal_capacity}
        />
      </dl>

      {Object.keys(cell.unavailable).length ? (
        <div className="tiny faint">
          사용 불가 기준:{' '}
          {Object.entries(cell.unavailable)
            .map(([basis, reason]) => `${basis} (${reason})`)
            .join(' · ')}
        </div>
      ) : null}
      {Object.entries(cell.notes).length ? (
        <div className="tiny faint">
          {Object.entries(cell.notes)
            .map(([key, note]) => `${NOTE_LABELS[key] ?? key}: ${note}`)
            .join(' · ')}
        </div>
      ) : null}
    </div>
  )
}

function Derived({
  label,
  value,
  note,
}: {
  label: string
  value: string | null
  note?: string
}) {
  return (
    <div className="row" style={{ justifyContent: 'space-between', gap: 12 }}>
      <span className="dim">{label}</span>
      <span className="mono" title={note}>
        {value ?? <span className="faint">—</span>}
      </span>
    </div>
  )
}

function pick(sample: Sample): Record<SpecKey, number | null> {
  return {
    total_mass_mg: sample.total_mass_mg,
    current_collector_mass_mg: sample.current_collector_mass_mg,
    active_wt_percent: sample.active_wt_percent,
    active_mass_mg: sample.active_mass_mg,
    area_cm2: sample.area_cm2,
    diameter_mm: sample.diameter_mm,
    thickness_um: sample.thickness_um,
    nominal_specific_capacity_mah_g: sample.nominal_specific_capacity_mah_g,
  }
}

export { Field }
