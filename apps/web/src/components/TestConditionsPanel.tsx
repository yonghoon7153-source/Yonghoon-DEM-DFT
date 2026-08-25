/** 시험 조건 — 셀 라이브러리에서 비교의 축이 되는 값들.
 *
 * 이 칸들은 계산에 들어가지 않는다.  질량이나 조성과 달리 틀려도 mAh/g 가
 * 바뀌지 않는다.  대신 라이브러리에서 무엇과 무엇을 나란히 놓을지를 정하므로,
 * 비어 있으면 셀이 서른 개 쌓인 뒤에 "그때 그 60도 건은 어느 거였지" 가 된다.
 *
 * C-rate 는 계측기가 아는 값이다.  `.wrd` 안의 스케줄에서 파싱해 채워 넣고,
 * 여기 타이핑한 것은 **덮어쓰기**로만 취급한다 (CLAUDE.md §0.3).  스케줄이 뭐라
 * 했는지는 칸 옆에 그대로 적어 둔다 — 덮어쓴 사람이 무엇을 덮었는지 볼 수
 * 있어야 하고, 스케줄이 추론에 실패했을 때(형성/본 사이클 비가 애매한 경우)도
 * 그 사실이 보여야 한다.
 */

import { useEffect, useMemo, useRef, useState } from 'react'

import { GroupFilterFields, useGroupChoice } from './GroupFilter'
import { api } from '../lib/api'
import { plain } from '../lib/format'
import type { Sample, Schedule } from '../lib/types'
import { Alert, Field, NumberField } from './ui'

/** 이 랩이 실제로 쓰는 값들.  목록에 없는 것도 그냥 칠 수 있다 — datalist 는
 *  제안이지 제한이 아니다. */
const CATHODE_TYPES = ['High-Ni', 'Mid-Ni', 'LFP', 'LMO', 'LCO', 'Li-rich']
const PROCESSES = ['dry', 'wet', 'semi-dry']

type TextKey = 'test_date' | 'cathode_type' | 'cathode_detail' | 'process'
type NumberKey = 'c_rate' | 'c_rate_formation' | 'temperature_c'

const TEXT_KEYS: TextKey[] = ['test_date', 'cathode_type', 'cathode_detail', 'process']
const NUMBER_KEYS: NumberKey[] = ['c_rate', 'c_rate_formation', 'temperature_c']

function pickText(sample: Sample): Record<TextKey, string> {
  return {
    test_date: sample.test_date ?? '',
    cathode_type: sample.cathode_type ?? '',
    cathode_detail: sample.cathode_detail ?? '',
    process: sample.process ?? '',
  }
}

function pickNumbers(sample: Sample): Record<NumberKey, number | null> {
  return {
    c_rate: sample.c_rate,
    c_rate_formation: sample.c_rate_formation,
    temperature_c: sample.temperature_c,
  }
}

export function TestConditionsPanel({
  sample,
  schedule,
  onSaved,
}: {
  sample: Sample
  /** 이 셀의 파일이 들고 온 스케줄.  없으면 안내만 달라진다. */
  schedule?: Schedule
  onSaved: (sample: Sample) => void
}) {
  const [text, setText] = useState(() => pickText(sample))
  const [numbers, setNumbers] = useState(() => pickNumbers(sample))
  // 그룹은 여기서도 고친다.  라이브러리에서만 붙일 수 있으면, 셀을 열어 조건을
  // 적다가 "이건 그 시리즈였지" 를 깨달았을 때 화면을 나갔다 와야 한다.
  const group = useGroupChoice()
  const { setFromGroupId, loaded: groupsLoaded } = group
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  // 남의 편집으로도 이 화면이 다시 읽히므로, 치는 중이면 덮지 않는다 (ADR 0012).
  const [touched, setTouched] = useState(false)
  const shownId = useRef(sample.id)

  useEffect(() => {
    if (touched && sample.id === shownId.current) return
    shownId.current = sample.id
    setTouched(false)
    setText(pickText(sample))
    setNumbers(pickNumbers(sample))
    // 저장된 값이 화면에 앉으려면 그룹 목록이 먼저 와야 한다: 소그룹의 부모를
    // 그 목록에서 찾기 때문이다.  안 기다리면 소그룹에 든 셀이 잠깐 "그룹
    // 없음" 으로 보이고, 그 상태로 저장을 누르면 정말로 떨어져 나간다.
    if (groupsLoaded) setFromGroupId(sample.group_id)
  }, [sample, touched, groupsLoaded, setFromGroupId])

  const groupChanged = groupsLoaded && group.effective !== (sample.group_id ?? null)
  const dirty =
    groupChanged ||
    TEXT_KEYS.some((key) => text[key] !== (sample[key] ?? '')) ||
    NUMBER_KEYS.some((key) => (numbers[key] ?? null) !== (sample[key] ?? null))

  async function save() {
    setSaving(true)
    setError(null)
    try {
      const body: Record<string, unknown> = {}
      const clear: string[] = []
      for (const key of TEXT_KEYS) {
        if (text[key] !== (sample[key] ?? '')) body[key] = text[key]
      }
      for (const key of NUMBER_KEYS) {
        const value = numbers[key]
        if (value === null) {
          if (sample[key] !== null) clear.push(key)
        } else if (value !== sample[key]) {
          body[key] = value
        }
      }
      if (groupChanged) {
        // 그룹에서 빼는 것은 `group_id: null` 이 아니라 clear 다 -- PATCH 에서
        // null 은 "안 보냄" 과 구별되지 않는다.
        if (group.effective === null) clear.push('group_id')
        else body.group_id = group.effective
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

  // 드롭다운을 만지는 것도 편집이다.  안 그러면 남의 편집으로 이 화면이 다시
  // 읽힐 때 방금 고른 그룹이 저장된 값으로 되돌아간다 (ADR 0012).
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

  const setWord = (key: TextKey) => (value: string) => {
    setTouched(true)
    setText((current) => ({ ...current, [key]: value }))
  }
  const setNumber = (key: NumberKey) => (value: number | null) => {
    setTouched(true)
    setNumbers((current) => ({ ...current, [key]: value }))
  }

  // 스케줄이 말한 C-rate.  본 사이클은 그대로 있고, 형성은 전류 비로 환산한다.
  const scheduleRate = schedule?.c_rate ?? null
  const formationRate =
    scheduleRate && schedule?.cycling_current_a && schedule?.formation_current_a
      ? (scheduleRate * schedule.formation_current_a) / schedule.cycling_current_a
      : null

  return (
    <div className="col" style={{ gap: 10 }}>
      {error ? <Alert kind="error">{error}</Alert> : null}

      <div className="grid cols-3" style={{ gap: 9 }}>
        {/* 그룹이 맨 앞이다 -- 나머지 칸이 "이 셀은 무엇인가" 라면 이것은
            "무엇과 나란히 놓을 것인가" 이고, 라이브러리에서 셋을 고를 때
            제일 먼저 쓰는 축이다 (ADR 0025). */}
        <GroupFilterFields pick={groupPick} hint="비교 묶음 · 라이브러리의 축" creatable />
        <Field label="시험일" hint="YYYY-MM-DD">
          <input
            type="date"
            value={text.test_date}
            onChange={(event) => setWord('test_date')(event.target.value)}
          />
        </Field>
        <Field label="양극재" hint="비교의 축">
          <input
            type="text"
            list="cathode-types"
            placeholder="High-Ni"
            value={text.cathode_type}
            onChange={(event) => setWord('cathode_type')(event.target.value)}
          />
          <datalist id="cathode-types">
            {CATHODE_TYPES.map((value) => (
              <option key={value} value={value} />
            ))}
          </datalist>
        </Field>
        <Field label="양극재 상세" hint="NCM811, NCM622 …">
          <input
            type="text"
            placeholder="NCM811"
            value={text.cathode_detail}
            onChange={(event) => setWord('cathode_detail')(event.target.value)}
          />
        </Field>
        <Field label="공정" hint="건식 / 습식">
          <input
            type="text"
            list="processes"
            placeholder="dry"
            value={text.process}
            onChange={(event) => setWord('process')(event.target.value)}
          />
          <datalist id="processes">
            {PROCESSES.map((value) => (
              <option key={value} value={value} />
            ))}
          </datalist>
        </Field>
        {/* 형성이 먼저다 — 셀이 실제로 거치는 순서이고, 사이클 표도 1번부터
            읽는다.  본 사이클을 왼쪽에 두면 화면의 순서와 실험의 순서가
            어긋나서, 두 칸 중 어느 것이 무엇인지 매번 라벨을 다시 읽어야
            한다 (Library 의 'C-rate (형성/본)' 열도 이 순서다). */}
        <NumberField
          label="C-rate · 형성"
          hint="formation"
          note={
            formationRate ? (
              <span title="스케줄의 형성/본 사이클 전류 비로 환산한 값">
                {plain(formationRate)}C
              </span>
            ) : undefined
          }
          value={numbers.c_rate_formation}
          onChange={setNumber('c_rate_formation')}
          min={0}
        />
        <NumberField
          label="C-rate · 본 사이클"
          hint="0.2 = 0.2C"
          note={scheduleRate ? <span title="스케줄에서 읽은 값">{plain(scheduleRate)}C</span> : undefined}
          value={numbers.c_rate}
          onChange={setNumber('c_rate')}
          min={0}
        />
        <NumberField
          label="온도"
          hint="°C"
          value={numbers.temperature_c}
          onChange={setNumber('temperature_c')}
        />
      </div>

      <div className="row">
        <button type="button" className="primary sm" disabled={!dirty || saving} onClick={save}>
          {saving ? '저장 중…' : dirty ? '저장' : '저장됨'}
        </button>
        {dirty ? (
          <button
            type="button"
            className="ghost sm"
            onClick={() => {
              setTouched(false)
              setText(pickText(sample))
              setNumbers(pickNumbers(sample))
              setFromGroupId(sample.group_id)
            }}
          >
            되돌리기
          </button>
        ) : null}
        <span className="spacer" />
        <span className="tiny faint">
          {schedule?.c_rate
            ? '옆의 값은 파일의 스케줄에서 읽은 것입니다 — 입력하면 그쪽이 이깁니다'
            : '계산에는 쓰이지 않고, 라이브러리에서 셀을 찾고 묶는 데 씁니다'}
        </span>
      </div>
    </div>
  )
}
