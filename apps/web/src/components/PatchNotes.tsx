/** 패치노트 — 무엇이 바뀌었나.
 *
 * 바로 아래 "최근 활동" 과 짝이지만 다른 질문에 답한다.  저쪽은 *데이터* 가
 * 어떻게 바뀌었는지(누가 무슨 셀을 올렸나)이고, 여기는 *워크벤치* 가 어떻게
 * 바뀌었는지다.  두 사람이 각자 고치고 `bml` 이 조용히 pull 하므로, 어제와
 * 다른 화면을 보면서도 무엇이 달라졌는지 알 길이 없었다 — `git log` 를 열어야
 * 했고, 그건 이 화면을 쓰는 사람이 할 일이 아니다.
 *
 * 내용은 `docs/log.md` 를 그대로 읽는다.  화면용 목록을 따로 두면 반드시
 * 한쪽만 갱신되고, 그때 사람이 보는 쪽이 틀린 쪽이 된다.
 */

import { useState } from 'react'

import { api } from '../lib/api'
import { useAsync } from '../lib/hooks'
import type { ChangeNote } from '../lib/types'

/** 아는 action 만 색을 준다.  파일에는 문서가 적어 둔 일곱 개 말고도 `feat`
 *  `docs` 가 들어와 있고, 앞으로 또 생길 수 있다 — 모르는 것은 중립으로 그리고
 *  이름은 그대로 보여 준다. */
const ACTION: Record<string, { label: string; tone: string }> = {
  feat: { label: '새 기능', tone: 'create' },
  create: { label: '새로', tone: 'create' },
  fix: { label: '고침', tone: 'fix' },
  update: { label: '바뀜', tone: '' },
  ingest: { label: '읽기', tone: '' },
  verify: { label: '검증', tone: '' },
  lint: { label: '정리', tone: '' },
  docs: { label: '문서', tone: '' },
  start: { label: '시작', tone: '' },
}

/** `2026-08-24` → `8월 24일`.  같은 해면 연도를 뺀다 — 스무 줄에 `2026` 이
 *  스무 번 적히면 정작 다른 부분인 날짜가 안 읽힌다. */
export function noteDate(iso: string, today = new Date()): string {
  const parts = iso.split('-')
  if (parts.length !== 3) return iso
  const [year, month, day] = parts
  const short = `${Number(month)}월 ${Number(day)}일`
  return Number(year) === today.getFullYear() ? short : `${year}. ${short}`
}

/** 본문 첫 문단만.  나머지는 펼쳤을 때 나온다.
 *
 * 문단으로 자르지 문장으로 자르지 않는다.  이 기록의 첫 문단은 대개 "무엇이
 * 잘못돼 있었는가" 한 덩어리이고, 거기서 첫 문장만 떼면 증상만 남고 이유가
 * 잘린다. */
export function firstParagraph(body: string): string {
  const paragraph = body.trim().split(/\n\s*\n/)[0] ?? ''
  return paragraph.replace(/\s*\n\s*/g, ' ').trim()
}

export function PatchNotes({ limit = 8 }: { limit?: number }) {
  const notes = useAsync(() => api.changelog({ limit }), [limit])
  const [open, setOpen] = useState<string | null>(null)
  const rows = notes.data ?? []

  if (notes.error) return <div className="tiny faint">패치노트를 읽지 못했습니다.</div>
  if (notes.loading && !rows.length) return <div className="tiny faint">읽는 중…</div>
  if (!rows.length) return <div className="tiny faint">아직 기록이 없습니다.</div>

  return (
    <ul className="feed patch-notes">
      {rows.map((note) => (
        <Note
          key={`${note.date}|${note.subject}`}
          note={note}
          open={open === `${note.date}|${note.subject}`}
          onToggle={() =>
            setOpen((current) => {
              const key = `${note.date}|${note.subject}`
              return current === key ? null : key
            })
          }
        />
      ))}
    </ul>
  )
}

function Note({
  note,
  open,
  onToggle,
}: {
  note: ChangeNote
  open: boolean
  onToggle: () => void
}) {
  const kind = ACTION[note.action]
  const summary = firstParagraph(note.body)
  return (
    <li className="col" style={{ alignItems: 'stretch', gap: 3 }}>
      <div className="row" style={{ alignItems: 'baseline', gap: 8 }}>
        <span className={`tag ${kind?.tone ?? ''}`}>{kind?.label ?? note.action}</span>
        <span className="what truncate" style={{ flex: 1 }}>
          {note.subject}
        </span>
        <span className="tiny faint nowrap">{noteDate(note.date)}</span>
      </div>
      {summary ? (
        <>
          {/* 접혀 있을 때 한 줄이 보이는 것이 요점이다 -- 제목만 스무 개면
              무엇이 바뀌었는지가 아니라 "뭔가 바뀌었다" 만 읽힌다. */}
          <div className={open ? 'tiny note-body' : 'tiny note-body truncate'}>
            {open ? note.body : summary}
          </div>
          <button
            type="button"
            className="link-btn tiny"
            style={{ alignSelf: 'flex-start' }}
            aria-expanded={open}
            onClick={onToggle}
          >
            {open ? '접기' : '자세히'}
          </button>
        </>
      ) : null}
    </li>
  )
}
