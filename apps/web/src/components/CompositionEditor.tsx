/** Record what the electrode is made of, and derive the mAh/g denominator.
 *
 * Only the active material belongs in that denominator, so this panel is where
 * the most consequential number in the app is set.  It accepts the shorthand a
 * researcher types (`AM:SE:VGCF:PTFE = 80:17:3:0`), a saved preset, or
 * per-component editing — and keeps a 0 wt% entry, because "this batch had no
 * binder" is a record worth having.
 *
 * A preset carries more than the blend: cells from one build share a punch
 * diameter, a nominal specific capacity and a counter electrode, and typing
 * those four fields per cell is where they get typed wrong.  Never a mass —
 * that is measured per cell (ADR 0010).
 */

import { useEffect, useRef, useState } from 'react'

import { api } from '../lib/api'
import { useAsync } from '../lib/hooks'
import { ko } from '../lib/i18n'
import type {
  Component, ComponentRole, CompositionPreset, PresetSettings, Sample,
} from '../lib/types'
import { Alert, CompositionChips, Field } from './ui'

const ROLE_LABELS: Record<ComponentRole, string> = {
  active: '활물질',
  electrolyte: '전해질',
  conductive: '도전재',
  binder: '바인더',
  other: '기타',
}

/** Sending a composition clears any hand-typed wt%, so the blend drives the
 *  denominator again.  Passed explicitly at every call site: merging it in
 *  blindly once threw away the "조성 지우기" button's own clear list, and the
 *  button reported success while leaving the blend exactly where it was. */
const CLEARS_WT = 'active_wt_percent'

/** What a preset may carry, in the order the save dialog lists it.
 *
 * Masses are absent on purpose.  `total_mass_mg` and `active_mass_mg` are
 * weighed per cell; riding along in a preset they would land under another
 * cell's mAh/g with nothing on screen to say so. */
const SETTING_ROWS: { key: keyof PresetSettings; label: string; unit?: string }[] = [
  { key: 'diameter_mm', label: '전극 지름', unit: 'mm' },
  { key: 'area_cm2', label: '전극 면적', unit: 'cm²' },
  { key: 'thickness_um', label: '전극 두께', unit: 'µm' },
  { key: 'nominal_specific_capacity_mah_g', label: '공칭 비용량', unit: 'mAh/g' },
  { key: 'reference_electrode', label: '기준전극' },
  { key: 'reference_offset_v', label: '오프셋', unit: 'V' },
]

/** The number as it was entered, minus float noise.
 *
 * Not `num()`: that formats *measurements* to a fixed significance, and a
 * preset line is a record of what will be written.  205.9 mAh/g shown as
 * "206" is a different nominal capacity, and "13.0 mm" is a punch nobody
 * typed. */
function exact(value: number): string {
  return String(Number(value.toFixed(6)))
}

/** The settings this cell would hand to a preset saved right now. */
export function presetSettingsOf(sample: Sample): PresetSettings {
  return {
    area_cm2: sample.area_cm2,
    diameter_mm: sample.diameter_mm,
    thickness_um: sample.thickness_um,
    nominal_specific_capacity_mah_g: sample.nominal_specific_capacity_mah_g,
    reference_electrode: sample.reference_electrode || null,
    reference_offset_v: sample.reference_offset_v ?? null,
  }
}

/** `["전극 지름 13 mm", "기준전극 Li-In"]` — what a preset will change.
 *
 * Shown before saving and again after applying.  One click filling five fields
 * is the point of a preset and also its hazard: a silent bulk edit of the
 * inputs behind every mAh/g is exactly the kind of thing this repo refuses to
 * do quietly. */
export function describeSettings(settings: PresetSettings | undefined): string[] {
  if (!settings) return []
  const parts: string[] = []
  for (const row of SETTING_ROWS) {
    const value = settings[row.key]
    if (value === null || value === undefined || value === '') continue
    const shown = typeof value === 'number' ? exact(value) : value
    parts.push(`${row.label} ${shown}${row.unit ? ` ${row.unit}` : ''}`)
  }
  return parts
}

/** Only the settings actually carried, ready to merge into a PATCH. */
function filledSettings(settings: PresetSettings): Record<string, unknown> {
  const body: Record<string, unknown> = {}
  for (const [key, value] of Object.entries(settings)) {
    if (value !== null && value !== undefined && value !== '') body[key] = value
  }
  return body
}

export function CompositionEditor({
  sample,
  onSaved,
}: {
  sample: Sample
  onSaved: (sample: Sample) => void
}) {
  // 남이 저장한 프리셋도 여기 나타난다 — 한 서버를 같이 보고 있으니
  // 저장한 순간 모두의 목록이다.
  const presets = useAsync(() => api.listPresets(), [], { live: true })
  const [components, setComponents] = useState<Component[]>(sample.composition)
  const [text, setText] = useState('')
  const [expanded, setExpanded] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [naming, setNaming] = useState(false)
  // 사람이 이 칸들을 건드렸는지.  `dirty` 로는 판단할 수 없다 — 남이 저장해서
  // sample 이 바뀌기만 해도 components 와 달라지므로 dirty 가 참이 된다.
  const [touched, setTouched] = useState(false)
  const shownId = useRef(sample.id)
  // Stamped with the sample revision it describes, so the note about what a
  // preset just changed disappears by itself on the next edit instead of
  // hanging around describing a state that is gone.
  const [applied, setApplied] = useState<{ at: string; parts: string[] } | null>(null)

  useEffect(() => {
    // 공유 서버라 이 화면은 남의 편집으로도 다시 읽힌다.  성분을 고치는 도중에
    // 그것이 들어오면 반쯤 고친 조성이 소리 없이 사라지고, 그 조성이 mAh/g
    // 분모를 정한다.
    if (touched && sample.id === shownId.current) return
    shownId.current = sample.id
    setTouched(false)
    setComponents(sample.composition)
    setText('')
  }, [sample.id, sample.composition, sample.updated_at, touched])

  const total = components.reduce((sum, c) => sum + (c.wt_percent || 0), 0)
  const activePercent = components
    .filter((c) => c.role === 'active')
    .reduce((sum, c) => sum + (c.wt_percent || 0), 0)
  const dirty =
    JSON.stringify(components) !== JSON.stringify(sample.composition) || text.trim() !== ''

  async function save(body: Record<string, unknown>): Promise<Sample | null> {
    setSaving(true)
    setError(null)
    try {
      const updated = await api.updateSample(sample.id, body)
      setTouched(false)
      onSaved(updated)
      setText('')
      return updated
    } catch (cause) {
      setError(String(cause instanceof Error ? cause.message : cause))
      return null
    } finally {
      setSaving(false)
    }
  }

  /** One preset, every field it carries, one request. */
  async function applyPreset(preset: CompositionPreset) {
    const body: Record<string, unknown> = filledSettings(preset.settings)
    if (preset.composition.length) {
      body.composition = preset.composition
      // Only then: a settings-only preset has no blend to drive the
      // denominator, so wiping a hand-typed wt% would just lose it.
      body.clear = [CLEARS_WT]
    }
    const updated = await save(body)
    if (updated) {
      setApplied({ at: updated.updated_at, parts: describeSettings(preset.settings) })
    }
  }

  const problems = sample.resolved_cell.composition_problems
  const showApplied = applied && applied.at === sample.updated_at && applied.parts.length > 0

  return (
    <div className="col" style={{ gap: 10 }}>
      {error ? <Alert kind="error">{error}</Alert> : null}

      <CompositionChips components={sample.composition} />

      {problems.length ? (
        <Alert kind="warn">{problems.map(ko.compositionProblem).join(' · ')}</Alert>
      ) : null}

      {sample.resolved_cell.active_wt_percent !== null ? (
        <div className="tiny faint">
          활물질 {sample.resolved_cell.active_wt_percent} wt% 가 mAh/g 분모에 들어갑니다
          {sample.active_wt_percent !== null && sample.composition.length
            ? ' (직접 입력값이 조성보다 우선)'
            : ''}
        </div>
      ) : null}

      <Field label="조성 입력" hint="AM:SE:VGCF:PTFE = 80:17:3:0">
        <div className="row" style={{ gap: 6, flexWrap: 'nowrap' }}>
          <input
            type="text"
            value={text}
            placeholder={sample.composition_label || 'AM:SE:VGCF = 80:17:3'}
            onChange={(event) => {
              setTouched(true)
              setText(event.target.value)
            }}
            onKeyDown={(event) => {
              if (event.key === 'Enter' && text.trim()) {
                void save({ composition_text: text, clear: [CLEARS_WT] })
              }
            }}
          />
          <button
            type="button"
            className="primary"
            disabled={!text.trim() || saving}
            onClick={() => save({ composition_text: text, clear: [CLEARS_WT] })}
          >
            적용
          </button>
        </div>
      </Field>

      <Field
        label="프리셋"
        hint="조성 · 지름 · 비용량 · 기준전극을 한 번에"
      >
        <select
          value=""
          disabled={saving || !presets.data?.length}
          aria-label="프리셋 선택"
          onChange={(event) => {
            const preset = presets.data?.find((p) => String(p.id) === event.target.value)
            if (preset) void applyPreset(preset)
          }}
        >
          <option value="">
            {presets.data?.length ? '프리셋 선택…' : '저장된 프리셋이 없습니다'}
          </option>
          {presets.data?.map((preset) => (
            <option key={preset.id} value={preset.id}>
              {preset.label}
            </option>
          ))}
        </select>
      </Field>

      {showApplied ? (
        <div className="tiny faint">프리셋이 채운 값: {applied!.parts.join(' · ')}</div>
      ) : null}

      <details open={expanded} onToggle={(e) => setExpanded((e.target as HTMLDetailsElement).open)}>
        <summary>
          성분별로 편집 {components.length ? `(${components.length}개)` : ''}
          <span className="spacer" />
          <button
            type="button"
            className="sm"
            // A click inside <summary> toggles the <details>; this button is
            // not a disclosure control, so it cancels that default.
            onClick={(event) => {
              event.preventDefault()
              event.stopPropagation()
              setNaming(true)
            }}
          >
            프리셋 저장
          </button>
        </summary>
        <div className="col" style={{ gap: 6, marginTop: 8 }}>
          {components.map((component, index) => (
            <div key={index} className="row" style={{ gap: 5, flexWrap: 'nowrap' }}>
              <input
                type="text"
                value={component.name}
                aria-label={`성분 ${index + 1} 이름`}
                onChange={(event) => {
                  setTouched(true)
                  setComponents((current) =>
                    current.map((c, i) =>
                      i === index ? { ...c, name: event.target.value } : c,
                    ),
                  )
                }}
                style={{ flex: 2 }}
              />
              <input
                type="number"
                step="any"
                min={0}
                value={component.wt_percent}
                aria-label={`성분 ${index + 1} wt%`}
                onChange={(event) => {
                  setTouched(true)
                  setComponents((current) =>
                    current.map((c, i) =>
                      i === index ? { ...c, wt_percent: Number(event.target.value) } : c,
                    ),
                  )
                }}
                style={{ flex: 1, minWidth: 62 }}
              />
              <select
                value={component.role}
                aria-label={`성분 ${index + 1} 역할`}
                onChange={(event) => {
                  setTouched(true)
                  setComponents((current) =>
                    current.map((c, i) =>
                      i === index
                        ? { ...c, role: event.target.value as ComponentRole }
                        : c,
                    ),
                  )
                }}
                style={{ flex: 1.4, minWidth: 84 }}
              >
                {(Object.keys(ROLE_LABELS) as ComponentRole[]).map((role) => (
                  <option key={role} value={role}>
                    {ROLE_LABELS[role]}
                  </option>
                ))}
              </select>
              <button
                type="button"
                className="ghost sm"
                title="성분 제거"
                onClick={() => {
                  setTouched(true)
                  setComponents((current) => current.filter((_, i) => i !== index))
                }}
              >
                ✕
              </button>
            </div>
          ))}

          <div className="row">
            <button
              type="button"
              className="sm"
              onClick={() => {
                setTouched(true)
                setComponents((current) => [
                  ...current,
                  { name: '', wt_percent: 0, role: 'other' },
                ])
              }}
            >
              성분 추가
            </button>
            <span className="spacer" />
            <span
              className="tiny mono"
              style={{ color: Math.abs(total - 100) > 0.5 ? 'var(--warn)' : 'var(--ink-3)' }}
            >
              합계 {total.toFixed(total % 1 ? 1 : 0)} wt% · 활물질 {activePercent || 0} wt%
            </span>
          </div>

          <div className="row">
            <button
              type="button"
              className="primary sm"
              disabled={!dirty || saving}
              onClick={() =>
                save({
                  composition: components.filter((c) => c.name.trim()),
                  clear: [CLEARS_WT],
                })
              }
            >
              {saving ? '저장 중…' : '조성 저장'}
            </button>
            {total > 0 && Math.abs(total - 100) > 0.5 ? (
              <button
                type="button"
                className="sm"
                disabled={saving}
                title="합계를 100 wt% 로 다시 계산합니다"
                onClick={() =>
                  save({
                    composition: components
                      .filter((c) => c.name.trim())
                      .map((c) => ({ ...c, wt_percent: (c.wt_percent * 100) / total })),
                    clear: [CLEARS_WT],
                  })
                }
              >
                100%로 환산
              </button>
            ) : null}
            {sample.composition.length ? (
              <button
                type="button"
                className="ghost sm"
                disabled={saving}
                onClick={() => save({ clear: ['composition', CLEARS_WT] })}
              >
                조성 지우기
              </button>
            ) : null}
          </div>
        </div>
      </details>

      {naming ? (
        <PresetDialog
          components={components.filter((c) => c.name.trim())}
          settings={presetSettingsOf(sample)}
          presets={presets.data ?? []}
          onDone={() => presets.reload()}
          onClose={() => setNaming(false)}
        />
      ) : null}
    </div>
  )
}

/** Name what is on screen, and manage the list while you are here.
 *
 * Deleting lives in this dialog rather than beside the dropdown because this
 * is where a duplicate becomes visible: you come to save "건식 80", see the
 * "건식 80" from March, and decide which one survives. */
function PresetDialog({
  components,
  settings,
  presets,
  onDone,
  onClose,
}: {
  components: Component[]
  settings: PresetSettings
  presets: CompositionPreset[]
  onDone: () => void
  onClose: () => void
}) {
  const [name, setName] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [clash, setClash] = useState(false)

  const carried = describeSettings(settings)
  const blend = components.length
    ? `${components.map((c) => c.name).join(':')} = ${components
        .map((c) => exact(c.wt_percent))
        .join(':')}`
    : ''
  const empty = !components.length && !carried.length

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  async function submit(overwrite: boolean) {
    if (!name.trim() || busy) return
    setBusy(true)
    setError(null)
    try {
      await api.savePreset({
        name: name.trim(),
        composition: components,
        settings: filledSettings(settings),
        overwrite,
      })
      onDone()
      onClose()
    } catch (cause) {
      const message = String(cause instanceof Error ? cause.message : cause)
      setError(message)
      // 409: the name is taken.  Offer the replacement rather than making
      // somebody invent "건식 80 (2)".
      setClash(message.includes('이미 있습니다'))
    } finally {
      setBusy(false)
    }
  }

  async function remove(preset: CompositionPreset) {
    setBusy(true)
    setError(null)
    try {
      await api.deletePreset(preset.id)
      onDone()
    } catch (cause) {
      setError(String(cause instanceof Error ? cause.message : cause))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div
      className="modal-backdrop"
      role="presentation"
      onClick={(event) => {
        if (event.target === event.currentTarget) onClose()
      }}
    >
      <div className="modal" role="dialog" aria-modal="true" aria-label="프리셋 저장">
        <h3>프리셋 저장</h3>

        {error ? <Alert kind="error">{error}</Alert> : null}

        <Field label="이름" hint="드롭박스에 이름과 조성 비율로 보입니다">
          <input
            type="text"
            value={name}
            autoFocus
            aria-label="프리셋 이름"
            placeholder="예: 건식 ASSB 80:17:3"
            onChange={(event) => {
              setName(event.target.value)
              setClash(false)
            }}
            onKeyDown={(event) => {
              if (event.key === 'Enter') void submit(clash)
            }}
          />
        </Field>

        {/* 무엇이 저장되는지 먼저 보여 준다.  프리셋 하나가 칸 다섯을 바꾸는데
            그 목록이 보이지 않으면, 나중에 적용했을 때 어디서 온 값인지 알 수
            없다. */}
        <div className="preset-carry">
          <div className="tiny dim">저장되는 값</div>
          {blend ? <div className="mono tiny">{blend}</div> : null}
          {carried.length ? (
            <div className="mono tiny">{carried.join(' · ')}</div>
          ) : null}
          {empty ? (
            <div className="tiny faint">
              담을 것이 없습니다. 조성이나 지름·비용량·기준전극을 먼저 채우세요.
            </div>
          ) : (
            <div className="tiny faint">질량은 셀마다 다르므로 담지 않습니다.</div>
          )}
        </div>

        <div className="row">
          <button
            type="button"
            className="primary"
            disabled={!name.trim() || busy || empty}
            onClick={() => submit(clash)}
          >
            {clash ? '덮어쓰기' : busy ? '저장 중…' : '저장'}
          </button>
          <button type="button" className="ghost" onClick={onClose}>
            닫기
          </button>
        </div>

        {presets.length ? (
          <>
            <div className="sep" />
            <div className="tiny dim">저장된 프리셋 {presets.length}개</div>
            <div className="col" style={{ gap: 0 }}>
              {presets.map((preset) => (
                <div key={preset.id} className="preset-row">
                  <span className="col" style={{ gap: 1, minWidth: 0 }}>
                    <span className="small truncate">{preset.name}</span>
                    <span className="tiny faint mono truncate">
                      {[preset.text, ...describeSettings(preset.settings)]
                        .filter(Boolean)
                        .join(' · ')}
                    </span>
                    {/* 목록이 공용이므로, 지우기 전에 누구 것인지 보여 준다. */}
                    {preset.created_by ? (
                      <span className="tiny faint">{preset.created_by}</span>
                    ) : null}
                  </span>
                  <span className="spacer" />
                  <button
                    type="button"
                    className="ghost sm"
                    disabled={busy}
                    aria-label={`"${preset.name}" 삭제`}
                    title={`"${preset.name}" 삭제`}
                    onClick={() => remove(preset)}
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </>
        ) : null}
      </div>
    </div>
  )
}
