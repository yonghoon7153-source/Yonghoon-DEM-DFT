/** 셀 고르기 — 드롭다운이 아니라 창.
 *
 *  셀은 계속 는다.  이름이 `cell39_CONT_3.6V_176.4mg_mid_Ni_건식전극_0.1C_...`
 *  처럼 길고 서로 앞부분이 같아서, 드롭다운으로는 두 가지가 동시에 깨진다:
 *  목록이 화면 밖으로 넘치고, 이름이 잘려 어느 것인지 구분되지 않는다.  게다가
 *  `<select>` 는 제 가장 긴 선택지만큼 넓어져 표의 옆 칸을 덮는다.
 *
 *  그래서 **버튼 + 창**이다.  창 안에서 그룹·소그룹으로 좁히고, 남은 것을
 *  **최근에 고친 순서**로 쭉 편다 — 방금 만든 셀에 방금 올린 파일을 붙이는
 *  것이 이 화면에서 가장 흔한 일이라, 그 순서가 곧 사람이 찾는 순서다.
 */

import { useEffect, useMemo, useState } from 'react'

import { GroupFilterFields, groupPath, useGroupChoice } from './GroupFilter'
import { Empty } from './ui'
import { dateTime } from '../lib/format'
import type { Sample } from '../lib/types'

/** 고른 셀을 보여 주는 버튼.  누르면 창이 뜬다. */
export function CellPicker({
  value,
  samples,
  label,
  disabled = false,
  emptyLabel = '— 안 붙임',
  onPick,
}: {
  value: number | null | undefined
  samples: Sample[]
  /** 스크린리더가 읽을 이름.  표 안에서는 줄마다 달라야 한다. */
  label: string
  disabled?: boolean
  emptyLabel?: string
  onPick: (sampleId: number | null) => void
}) {
  const [open, setOpen] = useState(false)
  const chosen = value ? samples.find((sample) => sample.id === value) : undefined

  return (
    <>
      <button
        type="button"
        className="cell-pick"
        aria-label={label}
        aria-haspopup="dialog"
        disabled={disabled}
        title={chosen ? chosen.name : emptyLabel}
        onClick={() => setOpen(true)}
      >
        <span className="truncate">
          {chosen ? chosen.name : <span className="faint">{emptyLabel}</span>}
        </span>
        <span className="faint" aria-hidden>▾</span>
      </button>
      {open ? (
        <CellPickerDialog
          title={label}
          value={value ?? null}
          samples={samples}
          emptyLabel={emptyLabel}
          onClose={() => setOpen(false)}
          onPick={(picked) => {
            setOpen(false)
            onPick(picked)
          }}
        />
      ) : null}
    </>
  )
}

function CellPickerDialog({
  title,
  value,
  samples,
  emptyLabel,
  onClose,
  onPick,
}: {
  title: string
  value: number | null
  samples: Sample[]
  emptyLabel: string
  onClose: () => void
  onPick: (sampleId: number | null) => void
}) {
  const [search, setSearch] = useState('')
  const group = useGroupChoice()
  const inGroup = group.includes

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  const rows = useMemo(() => {
    const needle = search.trim().toLowerCase()
    const matched = samples.filter((sample) => {
      if (!inGroup(sample.group_id)) return false
      if (!needle) return true
      return sample.name.toLowerCase().includes(needle)
        || (sample.group_name ?? '').toLowerCase().includes(needle)
        || (sample.cathode_detail ?? '').toLowerCase().includes(needle)
    })
    // 최근에 고친 것이 위로.  방금 만든 셀에 방금 올린 파일을 붙이는 것이
    // 가장 흔한 일이다.
    return [...matched].sort((a, b) =>
      (b.updated_at ?? '').localeCompare(a.updated_at ?? ''))
  }, [samples, search, inGroup])

  return (
    <div
      className="modal-backdrop"
      role="presentation"
      onClick={(event) => {
        if (event.target === event.currentTarget) onClose()
      }}
    >
      <div className="modal cell-picker" role="dialog" aria-modal="true"
           aria-label={`${title} 고르기`}>
        <h3>{title}</h3>

        <div className="grid cols-2" style={{ gap: 10 }}>
          <GroupFilterFields pick={group} hint="묶음으로 좁히기" />
        </div>
        <input
          type="text"
          autoFocus
          aria-label="셀 검색"
          placeholder="이름 · 그룹 · 양극재로 좁히기…"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />

        <div className="tiny faint">
          {rows.length}개 · 최근에 고친 순서
        </div>

        <div className="cell-list">
          <button
            type="button"
            className={`cell-row${value === null ? ' on' : ''}`}
            onClick={() => onPick(null)}
          >
            <span className="faint">{emptyLabel}</span>
          </button>
          {rows.map((sample) => (
            <button
              key={sample.id}
              type="button"
              className={`cell-row${value === sample.id ? ' on' : ''}`}
              onClick={() => onPick(sample.id)}
            >
              <span className="name truncate">{sample.name}</span>
              <span className="tiny faint truncate">
                {[groupPath(sample.group_name, sample.group_parent_name),
                  sample.cathode_detail || sample.cathode_type,
                  sample.run_count ? `파일 ${sample.run_count}개` : null]
                  .filter(Boolean).join(' · ') || '조건 미입력'}
              </span>
              <span className="tiny faint when">{dateTime(sample.updated_at)}</span>
            </button>
          ))}
          {!rows.length ? (
            <Empty title="조건에 맞는 셀이 없습니다">
              그룹을 넓히거나 검색어를 지워 보세요.
            </Empty>
          ) : null}
        </div>

        <div className="row">
          <span className="spacer" />
          <button type="button" className="ghost sm" onClick={onClose}>닫기</button>
        </div>
      </div>
    </div>
  )
}
