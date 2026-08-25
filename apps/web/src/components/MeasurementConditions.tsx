/** 이 측정의 조건 — 셀에 안 붙어 있어도 (ADR 0027).
 *
 *  EIS 만 보려고 잰 것, 셀을 만들기 전에 올린 것, 남의 셀에서 떼어 온 것.
 *  그런 측정이 많은데 "언제, 무엇을, 어떤 공정으로, 몇 도에서" 를 적을 데가
 *  셀밖에 없었다 — 셀이 없으면 그 사실도 없어지는 셈이었다.
 *
 *  붙어 있으면 **비어 있는 칸만** 셀에서 가져온다.  물려받은 칸은 힌트에
 *  "셀에서: …" 를 적는다: 그냥 값만 보이면 셀을 고쳤을 때 왜 이 측정의 표시가
 *  따라 바뀌는지 알 수 없다 (§0.4).  적어 넣으면 그것이 이긴다 — 같은 셀의
 *  임피던스를 다른 온도에서 재는 일이 실제로 있다.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { GroupFilterFields, useGroupChoice } from './GroupFilter'
import { Alert, Field } from './ui'

/** 화면이 다루는 칸들.  이름은 셀 쪽과 같다 — 물려받기가 한 줄로 끝난다. */
export interface Conditions {
  group_id?: number | null
  test_date?: string
  cathode_type?: string
  process?: string
  temperature_c?: number | null
  group_id_effective?: number | null
  group_label?: string
  test_date_effective?: string
  cathode_type_effective?: string
  process_effective?: string
  temperature_c_effective?: number | null
  inherited?: string[]
}

const CATHODE_TYPES = ['High-Ni', 'Mid-Ni', 'LFP', 'LMO', 'LCO', 'Li-rich']
const PROCESSES = ['dry', 'wet', 'semi-dry']

type TextKey = 'test_date' | 'cathode_type' | 'process'

const TEXT_KEYS: TextKey[] = ['test_date', 'cathode_type', 'process']

function pickText(record: Conditions): Record<TextKey, string> {
  return {
    test_date: record.test_date ?? '',
    cathode_type: record.cathode_type ?? '',
    process: record.process ?? '',
  }
}

function temperatureText(record: Conditions): string {
  const value = record.temperature_c
  return value === null || value === undefined ? '' : String(value)
}

export function MeasurementConditions({
  record,
  onSave,
}: {
  record: Conditions
  /** PATCH 를 보내고 화면을 다시 읽는 쪽.  EIS 와 GITT 가 다른 엔드포인트를
   *  쓰므로 여기서 부르지 않는다. */
  onSave: (body: Record<string, unknown>) => Promise<void>
}) {
  const [text, setText] = useState(() => pickText(record))
  const [temperature, setTemperature] = useState(() => temperatureText(record))
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [touched, setTouched] = useState(false)

  const group = useGroupChoice()
  const { setFromGroupId, loaded: groupsLoaded } = group
  // 칸에 앉히는 것은 **자기 것**이다.  물려받은 그룹을 앉히면 아무것도 안 바꾸고
  // 저장을 눌러도 그 값이 이 측정에 복사되고, 그러면 셀을 고쳐도 이쪽은 따라오지
  // 않는다 -- 물려받기가 조용히 끊긴다.
  const ownGroupId = record.group_id ?? null
  const seeded = useRef(false)

  useEffect(() => {
    if (touched || !groupsLoaded || seeded.current) return
    seeded.current = true
    setFromGroupId(ownGroupId)
  }, [touched, groupsLoaded, ownGroupId, setFromGroupId])

  const inherited = useMemo(() => new Set(record.inherited ?? []), [record.inherited])

  const groupChanged = groupsLoaded && seeded.current && group.effective !== ownGroupId
  const dirty =
    groupChanged ||
    TEXT_KEYS.some((key) => text[key] !== (record[key] ?? '')) ||
    temperature !== temperatureText(record)

  const save = useCallback(async () => {
    setSaving(true)
    setError(null)
    try {
      const body: Record<string, unknown> = {}
      const clear: string[] = []
      for (const key of TEXT_KEYS) {
        // 문자열 칸은 빈 문자열이 곧 "안 적음" 이라 clear 가 필요 없다.
        if (text[key] !== (record[key] ?? '')) body[key] = text[key]
      }
      const now = record.temperature_c ?? null
      if (temperature.trim() === '') {
        if (now !== null) clear.push('temperature_c')
      } else if (Number(temperature) !== now) {
        body.temperature_c = Number(temperature)
      }
      if (groupChanged) {
        if (group.effective === null) clear.push('group_id')
        else body.group_id = group.effective
      }
      if (clear.length) body.clear = clear
      await onSave(body)
      setTouched(false)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setSaving(false)
    }
  }, [text, temperature, record, groupChanged, group.effective, onSave])

  const groupPick = useMemo(() => ({
    ...group,
    setGroupId: (value: number | null) => {
      setTouched(true)
      group.setGroupId(value)
    },
    setSubGroupId: (value: number | null) => {
      setTouched(true)
      group.setSubGroupId(value)
    },
    create: async (name: string, parentId: number | null) => {
      setTouched(true)
      await group.create(name, parentId)
    },
  }), [group])

  /** 물려받은 칸의 안내 — 무엇이 어디서 왔는지. */
  const from = (key: TextKey, shown: string | undefined) =>
    (inherited.has(key) && shown ? `셀에서: ${shown}` : undefined)

  return (
    <div className="col" style={{ gap: 10 }}>
      {error ? <Alert kind="error">{error}</Alert> : null}

      <div className="grid cols-3" style={{ gap: 9 }}>
        <GroupFilterFields
          pick={groupPick}
          hint={inherited.has('group_id') && record.group_label
            ? `셀에서: ${record.group_label}`
            : '이 측정의 묶음 · 셀 없이도 됩니다'}
          creatable
        />
        <Field label="시험일"
               hint={from('test_date', record.test_date_effective) ?? 'YYYY-MM-DD'}>
          <input
            type="date"
            aria-label="시험일"
            value={text.test_date}
            onChange={(event) => {
              setTouched(true)
              setText((now) => ({ ...now, test_date: event.target.value }))
            }}
          />
        </Field>
        <Field label="양극재"
               hint={from('cathode_type', record.cathode_type_effective) ?? '비교의 축'}>
          <input
            type="text"
            aria-label="양극재"
            list="measurement-cathodes"
            placeholder={record.cathode_type_effective || 'High-Ni'}
            value={text.cathode_type}
            onChange={(event) => {
              setTouched(true)
              setText((now) => ({ ...now, cathode_type: event.target.value }))
            }}
          />
          <datalist id="measurement-cathodes">
            {CATHODE_TYPES.map((value) => <option key={value} value={value} />)}
          </datalist>
        </Field>
        <Field label="공정"
               hint={from('process', record.process_effective) ?? '건식 / 습식'}>
          <input
            type="text"
            aria-label="공정"
            list="measurement-processes"
            placeholder={record.process_effective || 'dry'}
            value={text.process}
            onChange={(event) => {
              setTouched(true)
              setText((now) => ({ ...now, process: event.target.value }))
            }}
          />
          <datalist id="measurement-processes">
            {PROCESSES.map((value) => <option key={value} value={value} />)}
          </datalist>
        </Field>
        <Field label="온도"
               hint={inherited.has('temperature_c')
                 && record.temperature_c_effective !== null
                 && record.temperature_c_effective !== undefined
                 ? `셀에서: ${record.temperature_c_effective} °C`
                 : '°C'}>
          <input
            type="number"
            aria-label="온도"
            value={temperature}
            placeholder={record.temperature_c_effective === null
              || record.temperature_c_effective === undefined
              ? '' : String(record.temperature_c_effective)}
            onChange={(event) => {
              setTouched(true)
              setTemperature(event.target.value)
            }}
          />
        </Field>
      </div>

      <div className="row">
        <button type="button" className="primary sm" disabled={!dirty || saving}
                onClick={() => void save()}>
          {saving ? '저장 중…' : dirty ? '저장' : '저장됨'}
        </button>
        {dirty ? (
          <button
            type="button"
            className="ghost sm"
            onClick={() => {
              setTouched(false)
              setText(pickText(record))
              setTemperature(temperatureText(record))
              setFromGroupId(ownGroupId)
            }}
          >
            되돌리기
          </button>
        ) : null}
        <span className="spacer" />
        <span className="tiny faint">
          {inherited.size
            ? '"셀에서:" 가 붙은 칸은 관계셀에서 온 값입니다 — 적어 넣으면 이 측정의 값이 이깁니다'
            : '셀에 붙이지 않아도 됩니다 — 이 측정만의 조건입니다'}
        </span>
      </div>
    </div>
  )
}
