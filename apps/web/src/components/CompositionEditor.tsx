/** Record what the electrode is made of, and derive the mAh/g denominator.
 *
 * Only the active material belongs in that denominator, so this panel is where
 * the most consequential number in the app is set.  It accepts the shorthand a
 * researcher types (`AM:SE:VGCF:PTFE = 80:17:3:0`), a preset, or per-component
 * editing — and keeps a 0 wt% entry, because "this batch had no binder" is a
 * record worth having.
 */

import { useEffect, useState } from 'react'

import { api } from '../lib/api'
import { useAsync } from '../lib/hooks'
import { ko } from '../lib/i18n'
import type { Component, ComponentRole, Sample } from '../lib/types'
import { Alert, CompositionChips, Field } from './ui'

const ROLE_LABELS: Record<ComponentRole, string> = {
  active: '활물질',
  electrolyte: '전해질',
  conductive: '도전재',
  binder: '바인더',
  other: '기타',
}

export function CompositionEditor({
  sample,
  onSaved,
}: {
  sample: Sample
  onSaved: (sample: Sample) => void
}) {
  const meta = useAsync(() => api.meta(), [])
  const [components, setComponents] = useState<Component[]>(sample.composition)
  const [text, setText] = useState('')
  const [expanded, setExpanded] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setComponents(sample.composition)
    setText('')
  }, [sample.composition, sample.updated_at])

  const total = components.reduce((sum, c) => sum + (c.wt_percent || 0), 0)
  const activePercent = components
    .filter((c) => c.role === 'active')
    .reduce((sum, c) => sum + (c.wt_percent || 0), 0)
  const dirty =
    JSON.stringify(components) !== JSON.stringify(sample.composition) || text.trim() !== ''

  async function save(body: Record<string, unknown>) {
    setSaving(true)
    setError(null)
    try {
      // Sending a composition clears any hand-typed wt% so the blend drives
      // the denominator again -- but merge, never overwrite: the "조성 지우기"
      // button asks to clear `composition`, and a blanket
      // `clear: ['active_wt_percent']` threw that request away, so the button
      // reported success and left the blend exactly where it was.
      const clear = [
        ...new Set([...((body.clear as string[] | undefined) ?? []), 'active_wt_percent']),
      ]
      onSaved(await api.updateSample(sample.id, { ...body, clear }))
      setText('')
    } catch (cause) {
      setError(String(cause instanceof Error ? cause.message : cause))
    } finally {
      setSaving(false)
    }
  }

  const problems = sample.resolved_cell.composition_problems

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
            onChange={(event) => setText(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter' && text.trim()) void save({ composition_text: text })
            }}
          />
          <button
            type="button"
            className="primary"
            disabled={!text.trim() || saving}
            onClick={() => save({ composition_text: text })}
          >
            적용
          </button>
        </div>
      </Field>

      <Field label="자주 쓰는 조성">
        <select
          value=""
          disabled={saving}
          onChange={(event) => {
            if (event.target.value) void save({ composition_text: event.target.value })
          }}
        >
          <option value="">프리셋 선택…</option>
          {meta.data?.composition_presets.map((preset) => (
            <option key={preset.text} value={preset.text}>
              {preset.label}
            </option>
          ))}
        </select>
      </Field>

      <details open={expanded} onToggle={(e) => setExpanded((e.target as HTMLDetailsElement).open)}>
        <summary>성분별로 편집 {components.length ? `(${components.length}개)` : ''}</summary>
        <div className="col" style={{ gap: 6, marginTop: 8 }}>
          {components.map((component, index) => (
            <div key={index} className="row" style={{ gap: 5, flexWrap: 'nowrap' }}>
              <input
                type="text"
                value={component.name}
                aria-label={`성분 ${index + 1} 이름`}
                onChange={(event) =>
                  setComponents((current) =>
                    current.map((c, i) =>
                      i === index ? { ...c, name: event.target.value } : c,
                    ),
                  )
                }
                style={{ flex: 2 }}
              />
              <input
                type="number"
                step="any"
                min={0}
                value={component.wt_percent}
                aria-label={`성분 ${index + 1} wt%`}
                onChange={(event) =>
                  setComponents((current) =>
                    current.map((c, i) =>
                      i === index ? { ...c, wt_percent: Number(event.target.value) } : c,
                    ),
                  )
                }
                style={{ flex: 1, minWidth: 62 }}
              />
              <select
                value={component.role}
                aria-label={`성분 ${index + 1} 역할`}
                onChange={(event) =>
                  setComponents((current) =>
                    current.map((c, i) =>
                      i === index
                        ? { ...c, role: event.target.value as ComponentRole }
                        : c,
                    ),
                  )
                }
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
                onClick={() =>
                  setComponents((current) => current.filter((_, i) => i !== index))
                }
              >
                ✕
              </button>
            </div>
          ))}

          <div className="row">
            <button
              type="button"
              className="sm"
              onClick={() =>
                setComponents((current) => [
                  ...current,
                  { name: '', wt_percent: 0, role: 'other' },
                ])
              }
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
                save({ composition: components.filter((c) => c.name.trim()) })
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
                onClick={() => save({ clear: ['composition'] })}
              >
                조성 지우기
              </button>
            ) : null}
          </div>
        </div>
      </details>
    </div>
  )
}
