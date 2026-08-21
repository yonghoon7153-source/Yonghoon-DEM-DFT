/** The mass / area / composition inputs that drive every normalised number.
 *
 * Editing here writes straight to the sample: the raw mAh in the database is
 * untouched, so every table and plot re-normalises on the next fetch without
 * re-reading the 20 MB original (ADR 0001).
 */

import { useEffect, useRef, useState } from 'react'

import { api } from '../lib/api'
import { massFromName, num } from '../lib/format'
import { ko } from '../lib/i18n'
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
  | 'reference_offset_v'

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
  // 문자열이라 숫자 draft 에 섞지 않는다.
  const [electrode, setElectrode] = useState(sample.reference_electrode ?? '')
  // 사람이 이 칸들을 건드렸는지.  `dirty` 로는 판단할 수 없다 — 남이 저장해서
  // sample 이 바뀌기만 해도 draft 와 달라지므로 dirty 가 참이 된다.  "내가
  // 쳤다" 와 "값이 달라졌다" 는 다른 질문이다.
  const [touched, setTouched] = useState(false)
  const shownId = useRef(sample.id)

  useEffect(() => {
    // 공유 서버라 이 화면은 남의 편집으로도 다시 읽힌다.  타이핑 중에 그것이
    // 들어오면, 반쯤 입력한 질량이 소리 없이 사라진다 — 저장한 줄 알고 넘어가면
    // 그 셀의 모든 mAh/g 가 옛 질량으로 남는다.
    if (touched && sample.id === shownId.current) return
    shownId.current = sample.id
    setTouched(false)
    setDraft(pick(sample))
    setElectrode(sample.reference_electrode ?? '')
  }, [sample, touched])

  const dirty =
    (Object.keys(draft) as SpecKey[]).some(
      (key) => (draft[key] ?? null) !== (sample[key] ?? null),
    ) || electrode !== (sample.reference_electrode ?? '')

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
      if (electrode !== (sample.reference_electrode ?? '')) {
        body.reference_electrode = electrode
      }
      if (clear.length) body.clear = clear
      const updated = await api.updateSample(sample.id, body)
      setTouched(false)
      onSaved(updated)
    } catch (cause) {
      setError(String(cause instanceof Error ? cause.message : cause))
    } finally {
      setSaving(false)
    }
  }

  const cell = sample.resolved_cell
  const set = (key: SpecKey) => (value: number | null) => {
    setTouched(true)
    setDraft((previous) => ({ ...previous, [key]: value }))
  }

  // 파일 이름이 질량을 들고 다닌다 (`..._4.6V_1_17.5mg`).  .wrd 는 그 값을
  // 모르므로 손으로 넣어야 하는데, 옆에 이름이 말하는 값을 적어 두면 오타가
  // 모든 mAh/g 를 조용히 바꾸기 전에 눈에 걸린다.
  const named = massFromName(sample.name)

  return (
    <div className="col">
      {error ? <Alert kind="error">{error}</Alert> : null}

      <div className="grid cols-2" style={{ gap: 9 }}>
        <NumberField
          label="전극 총 질량 (집전체 제외)"
          hint="mg · 이 값에 활물질 wt% 를 곱한다"
          note={named === null ? undefined : <span title="셀 이름에 적힌 값">#{named}mg</span>}
          value={draft.total_mass_mg}
          onChange={set('total_mass_mg')}
          min={0}
        />
        <NumberField
          label="활물질 함량 직접 입력"
          hint="wt% · 조성보다 우선"
          value={draft.active_wt_percent}
          onChange={set('active_wt_percent')}
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

      {/* 집전체 질량은 입력란에서 뺐다 — 이 랩은 "전극 총 질량" 을 이미 집전체를
          제외한 값으로 쓴다.  다만 예전에 값을 넣어 둔 셀이 있으면 그 차감이
          화면에 없는 채로 계속 살아 있게 되므로, 있을 때만 보여 주고 지울 수
          있게 한다.  보이지 않는 차감은 mAh/g 를 조용히 바꾼다. */}
      {sample.current_collector_mass_mg ? (
        <Alert kind="warn">
          이 셀에는 집전체 질량 {sample.current_collector_mass_mg} mg 이 남아 있어 총
          질량에서 빠지고 있습니다. 총 질량을 이미 집전체 제외로 넣었다면 지우세요.
          <button
            type="button"
            className="ghost tiny"
            style={{ marginLeft: 8 }}
            disabled={saving}
            onClick={async () => {
              setSaving(true)
              try {
                setError(null)
                onSaved(
                  await api.updateSample(sample.id, { clear: ['current_collector_mass_mg'] }),
                )
              } catch (cause) {
                setError(String(cause instanceof Error ? cause.message : cause))
              } finally {
                setSaving(false)
              }
            }}
          >
            지우기
          </button>
        </Alert>
      ) : null}

      {/* 기준전극.  황화물계 전고체는 Li-In 대극으로 만드는데, 계측기는 그
          기준으로 기록하고 논문은 vs Li/Li+ 로 쓴다 — 차이 0.62 V 는 4.40 V
          컷오프를 3.78 V 로 보이게 할 만큼 크고, 틀렸다고 알아채기 어려울 만큼
          그럴듯하다. 질량과 같은 방식으로 저장은 raw, 표시할 때 환산한다. */}
      <div className="grid cols-2" style={{ gap: 9, marginTop: 9 }}>
        <Field label="기준전극" hint="전압 표시 기준">
          <select
            value={electrode}
            onChange={(event) => {
              setTouched(true)
              setElectrode(event.target.value)
            }}
          >
            <option value="">기록 그대로 (환산 안 함)</option>
            <option value="Li">Li 금속 — vs Li/Li⁺</option>
            <option value="Li-In">Li-In 합금 (+0.62 V) — 황화물계 전고체</option>
            <option value="LTO">Li₄Ti₅O₁₂ (+1.55 V)</option>
          </select>
        </Field>
        <NumberField
          label="오프셋 직접 입력"
          hint="V · 위 선택보다 우선"
          value={draft.reference_offset_v}
          onChange={set('reference_offset_v')}
        />
      </div>

      <div className="row">
        <button type="button" className="primary" disabled={!dirty || saving} onClick={save}>
          {saving ? '저장 중…' : dirty ? '저장하고 다시 계산' : '저장됨'}
        </button>
        {dirty ? (
          <button
            type="button"
            className="ghost sm"
            onClick={() => {
              setTouched(false)
              setDraft(pick(sample))
              setElectrode(sample.reference_electrode ?? '')
            }}
          >
            되돌리기
          </button>
        ) : null}
      </div>

      <div className="sep" />

      <dl className="small" style={{ margin: 0, display: 'grid', gap: 4 }}>
        <Derived
          label="활물질 질량"
          value={cell.active_mass_g ? `${num(cell.active_mass_g * 1000)} mg` : null}
          note={cell.notes.active_mass && ko.cellNote(cell.notes.active_mass)}
        />
        <Derived
          label="면적"
          value={cell.area_cm2 ? `${num(cell.area_cm2)} cm²` : null}
          note={cell.notes.area && ko.cellNote(cell.notes.area)}
        />
        <Derived
          label="로딩"
          value={cell.loading_mg_cm2 ? `${num(cell.loading_mg_cm2, 3)} mg/cm²` : null}
        />
        <Derived
          label="공칭 용량"
          value={cell.nominal_capacity_mah ? `${num(cell.nominal_capacity_mah)} mAh` : null}
          note={cell.notes.nominal_capacity && ko.cellNote(cell.notes.nominal_capacity)}
        />
      </dl>

      {Object.keys(cell.unavailable).length ? (
        <div className="tiny faint">
          사용 불가 기준:{' '}
          {Object.entries(cell.unavailable)
            .map(([basis, reason]) => `${basis} — ${ko.basisReason(reason)}`)
            .join(' · ')}
        </div>
      ) : null}
      {Object.entries(cell.notes).length ? (
        <div className="tiny faint">
          {Object.entries(cell.notes)
            .map(([key, note]) => {
              // `composition` carries the blend's *problems*, joined by "; ",
              // and those live in a different rule table.  Sending them through
              // cellNote matched nothing, so the one note most likely to say
              // something is wrong was the one shown in English.
              const text =
                key === 'composition'
                  ? note
                      .split('; ')
                      .map(ko.compositionProblem)
                      .join(' · ')
                  : ko.cellNote(note)
              return `${NOTE_LABELS[key] ?? key}: ${text}`
            })
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
    reference_offset_v: sample.reference_offset_v ?? null,
  }
}

export { Field }
