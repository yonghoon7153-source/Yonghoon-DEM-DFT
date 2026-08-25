/** 관계셀 — 이 측정이 어느 충방전 셀의 것인가, 그리고 그것을 여기서 바꾼다.
 *
 *  EIS·GITT 는 저마다 독자 섹션이지만 (ADR 0024) 셀 하나가 셋을 잇는다.  그
 *  이음을 **거는 자리**가 화면마다 다르면, 파일을 스무 개 올려 놓고 어디서
 *  붙이는지를 매번 다시 찾게 된다.  그래서 고르는 드롭다운, 지우는 버튼,
 *  그리고 "무엇이 어디에 붙어 있나" 를 훑는 창을 한 곳에 둔다.
 *
 *  **붙이지 않아도 된다.**  파일부터 올려 두고 셀은 나중에 만드는 순서가 흔해서
 *  `sample_id` 는 비어 있는 것이 정상이고, 이 창은 그 상태를 고쳐야 할 잘못이
 *  아니라 **아직 안 한 일**로 보여 준다 (§0.4).
 */

import { useMemo, useState, type ReactNode } from 'react'
import { Link } from 'react-router-dom'

import { TrashIcon } from './ui'
import type { Sample } from '../lib/types'

/** 관계셀 하나를 고르는 드롭다운.  빈 값은 "떼어내기" 다. */
export function RelatedCellSelect({
  value,
  samples,
  label,
  disabled = false,
  onPick,
}: {
  value: number | null | undefined
  samples: Sample[]
  /** 스크린리더가 읽을 이름.  표 안에서는 줄마다 달라야 한다. */
  label: string
  disabled?: boolean
  onPick: (sampleId: number | null) => void
}) {
  return (
    <select
      aria-label={label}
      value={value ? String(value) : ''}
      disabled={disabled}
      onChange={(event) =>
        onPick(event.target.value ? Number(event.target.value) : null)}
    >
      <option value="">— 안 붙임</option>
      {samples.map((sample) => (
        <option key={sample.id} value={sample.id}>{sample.name}</option>
      ))}
    </select>
  )
}

/** 측정 하나를 기록에서 지운다.  **붙어 있어도 지울 수 있다.**
 *
 *  두 번 눌러야 지워진다: 표의 행 끝이라 스크롤하다 스치기 쉽고 되돌리기가
 *  없다.  원본 파일은 남는다 (불변 규칙 2) — 같은 바이트를 다시 올리면
 *  sha256 이 같아 되살아나므로, 이 버튼은 "삭제" 보다 "목록에서 내리기" 다.
 */
export function DeleteMeasurementButton({
  name,
  onDelete,
  onError,
}: {
  name: string
  onDelete: () => Promise<void>
  onError: (message: string | null) => void
}) {
  const [confirming, setConfirming] = useState(false)
  const [busy, setBusy] = useState(false)

  if (!confirming) {
    return (
      <button
        type="button"
        className="ghost icon"
        aria-label={`${name} 지우기`}
        title="이 측정을 기록에서 지웁니다 (원본 파일은 남습니다). 셀에 붙어 있어도 지울 수 있습니다."
        onClick={() => {
          onError(null)
          setConfirming(true)
        }}
      >
        <TrashIcon size={13} />
      </button>
    )
  }
  return (
    <>
      <button
        type="button"
        className="danger tiny"
        disabled={busy}
        onClick={async () => {
          setBusy(true)
          try {
            onError(null)
            await onDelete()
            setConfirming(false)
          } catch (cause) {
            onError(cause instanceof Error ? cause.message : String(cause))
          } finally {
            setBusy(false)
          }
        }}
      >
        지웁니다
      </button>
      <button type="button" className="ghost tiny" disabled={busy}
              onClick={() => setConfirming(false)}>
        취소
      </button>
    </>
  )
}

export interface IndexEntry {
  id: number
  name: string
  sampleId: number | null
  sampleName: string | null
  /** 한 줄 밑에 붙는 작은 글씨 — 점 수, 펄스 수 같은 것. */
  detail: ReactNode
  /** 이 측정의 상세로 가는 길. */
  href: string
}

/** 관계셀 색인 — 무엇이 어느 셀에 붙어 있고 무엇이 아직 안 붙었나.
 *
 *  안 붙은 것이 먼저 온다.  그것이 이 창에서 할 일이기 때문이다.  붙은 것도
 *  같이 보여 주는 이유는 **옮기는 일**이 실제로 있어서다 — 파일을 잘못된 셀에
 *  붙였다는 것은 대개 다른 셀을 만들고 나서 안다.
 */
export function RelatedCellIndex({
  entries,
  samples,
  onAttach,
  onDelete,
  emptyLabel = '올린 것이 없습니다',
}: {
  entries: IndexEntry[]
  samples: Sample[]
  onAttach: (id: number, sampleId: number | null) => Promise<void>
  onDelete: (id: number) => Promise<void>
  emptyLabel?: string
}) {
  const [search, setSearch] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState<number | null>(null)

  const rows = useMemo(() => {
    const needle = search.trim().toLowerCase()
    const matched = entries.filter((entry) => !needle
      || entry.name.toLowerCase().includes(needle)
      || (entry.sampleName ?? '').toLowerCase().includes(needle))
    // 안 붙은 것 먼저, 그 다음 셀 이름순.
    return [...matched].sort((a, b) => {
      if (!a.sampleId !== !b.sampleId) return a.sampleId ? 1 : -1
      return (a.sampleName ?? '').localeCompare(b.sampleName ?? '', 'ko')
        || a.name.localeCompare(b.name, 'ko')
    })
  }, [entries, search])

  const loose = entries.filter((entry) => !entry.sampleId).length

  return (
    <div className="col" style={{ gap: 10 }}>
      <input
        type="text"
        aria-label="색인 검색"
        placeholder="이름 또는 관계셀로 좁히기…"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
      />
      <div className="tiny faint">
        {loose
          ? `${loose}개가 아직 셀에 안 붙어 있습니다 — 붙이지 않아도 분석은 됩니다.`
          : '모두 관계셀이 정해져 있습니다.'}
      </div>
      {error ? <div className="tiny warn">{error}</div> : null}
      {rows.length ? (
        <div className="col" style={{ gap: 8, maxHeight: 420, overflow: 'auto' }}>
          {rows.map((entry) => (
            <div key={entry.id} className="col" style={{ gap: 4 }}>
              <div className="row" style={{ gap: 8, justifyContent: 'space-between' }}>
                <Link to={entry.href} className="truncate">{entry.name}</Link>
                <DeleteMeasurementButton
                  name={entry.name}
                  onError={setError}
                  onDelete={() => onDelete(entry.id)}
                />
              </div>
              <div className="row" style={{ gap: 8 }}>
                <RelatedCellSelect
                  value={entry.sampleId}
                  samples={samples}
                  label={`${entry.name} 관계셀`}
                  disabled={busy === entry.id}
                  onPick={async (sampleId) => {
                    setBusy(entry.id)
                    try {
                      setError(null)
                      await onAttach(entry.id, sampleId)
                    } catch (cause) {
                      setError(cause instanceof Error ? cause.message : String(cause))
                    } finally {
                      setBusy(null)
                    }
                  }}
                />
                <span className="tiny dim">{entry.detail}</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="tiny faint">{emptyLabel}</div>
      )}
    </div>
  )
}
