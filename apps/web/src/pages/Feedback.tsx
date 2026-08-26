/** 의견 — 쓰다가 걸린 것을 겪은 자리에 적는 칸 (ADR 0033).
 *
 * 이 저장소에서 제일 잘 사라지는 것이 **쓰는 사람의 말**이다.  카톡으로 오면
 * 스크롤에 묻히고, 말로 하면 그 자리에서 끝난다.  `docs/log.md` 는 고친 사람의
 * 기록이지 겪은 사람의 기록이 아니다.
 *
 * 정리된 항목을 목록에서 빼지 않는다 — 같은 불편이 두 달 뒤에 다시 올라올 때
 * "그때 이렇게 정리했다" 가 보여야 한다.  대신 아래로 내린다.
 */

import { useEffect, useMemo, useRef, useState } from 'react'

import { Alert, Card, Empty, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime } from '../lib/format'
import { useAsync } from '../lib/hooks'
import { Markdown } from '../lib/markdown'
import { markSeen } from '../lib/seen'
import type { FeedbackKind, FeedbackNote } from '../lib/types'

/** Ctrl+B · Ctrl+I · Ctrl+` — 고른 글자를 표시로 감싼다.
 *
 *  `**굵게**` 를 손으로 치라고 안내하는 것보다 낫다.  안내를 읽어야 하는 칸은
 *  안 쓰이고, 그 안내를 화면에 적으면 별표가 그대로 보여서 **마크다운이 안
 *  된다는 증거처럼** 읽힌다.
 *
 *  고른 것이 없으면 표시만 넣고 그 사이에 커서를 둔다 — 그래야 바로 이어서
 *  칠 수 있다.  이미 감싸여 있으면 벗긴다 (누르면 켜지고 다시 누르면 꺼진다).
 */
export function wrapSelection(
  value: string, start: number, end: number, mark: string,
): { value: string; start: number; end: number } {
  const before = value.slice(0, start)
  const picked = value.slice(start, end)
  const after = value.slice(end)
  const wrapped = before.endsWith(mark) && after.startsWith(mark)
  if (wrapped) {
    return {
      value: before.slice(0, -mark.length) + picked + after.slice(mark.length),
      start: start - mark.length,
      end: end - mark.length,
    }
  }
  return {
    value: `${before}${mark}${picked}${mark}${after}`,
    start: start + mark.length,
    end: end + mark.length,
  }
}

const MARKS: Record<string, string> = { b: '**', i: '*', e: '`' }

const KINDS: { value: FeedbackKind; label: string; hint: string }[] = [
  { value: 'issue', label: '불편', hint: '쓰다가 막히거나 틀린 것' },
  { value: 'question', label: '질문', hint: '이건 어떻게 되나요' },
  { value: 'idea', label: '제안', hint: '이러면 좋겠습니다' },
]

function kindOf(kind: string) {
  return KINDS.find((k) => k.value === kind) ?? KINDS[0]!
}

export function Feedback() {
  const board = useAsync(() => api.listFeedback(), [], { live: true, refreshMs: 60_000 })
  const notes = useMemo(() => board.data ?? [], [board.data])
  const [kind, setKind] = useState<FeedbackKind>('issue')
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const box = useRef<HTMLTextAreaElement>(null)

  // 이 화면을 연 것이 곧 읽은 것이다.  목록이 도착한 **뒤에** 찍는다 — 먼저
  // 찍으면 읽는 동안 올라온 글까지 읽은 것이 된다.
  useEffect(() => {
    if (board.data) markSeen('feedback')
  }, [board.data])

  const open = notes.filter((note) => !note.resolved_at)
  const done = notes.filter((note) => note.resolved_at)

  async function submit() {
    const body = draft.trim()
    if (!body || busy) return
    setBusy(true)
    setError(null)
    try {
      await api.createFeedback({ kind, body })
      setDraft('')
      board.reload()
    } catch (problem) {
      setError(problem instanceof Error ? problem.message : String(problem))
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>F&amp;Q</h1>
          <p className="sub">
            쓰다가 걸린 것을 여기 적어 두세요 — 불편한 점, 궁금한 것, 이러면
            좋겠다 싶은 것. 정리되면 접히지만 사라지지는 않습니다.
          </p>
        </div>
      </div>

      <Card
        title={<h2>새로 적기</h2>}
        actions={<span className="tiny faint">{kindOf(kind).hint}</span>}
      >
        <div className="col" style={{ gap: 10 }}>
          <div className="segmented" role="group" aria-label="종류">
            {KINDS.map((choice) => (
              <button
                key={choice.value}
                type="button"
                className={kind === choice.value ? 'on' : ''}
                onClick={() => setKind(choice.value)}
              >
                {choice.label}
              </button>
            ))}
          </div>
          <textarea
            ref={box}
            aria-label="내용"
            rows={3}
            value={draft}
            placeholder="예: 사이클 클립보드가 고른 것만 안 나오고 전체가 나옵니다"
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={(event) => {
              // 짧은 한 줄이 대부분이라 Ctrl+Enter 로 끝낼 수 있게 한다.
              if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
                void submit()
                return
              }
              if (!(event.ctrlKey || event.metaKey)) return
              const mark = MARKS[event.key.toLowerCase()]
              if (!mark) return
              event.preventDefault()
              const field = event.currentTarget
              const next = wrapSelection(
                field.value, field.selectionStart, field.selectionEnd, mark)
              setDraft(next.value)
              // 상태가 반영된 **뒤에** 커서를 놓는다.  지금 놓으면 React 가
              // value 를 다시 그리면서 커서를 끝으로 보낸다.
              window.requestAnimationFrame(() => {
                box.current?.setSelectionRange(next.start, next.end)
                box.current?.focus()
              })
            }}
          />
          <div className="row" style={{ gap: 10, alignItems: 'center' }}>
            <button type="button" className="primary" disabled={!draft.trim() || busy}
                    onClick={submit}>
              {busy ? '올리는 중…' : '올리기'}
            </button>
            {/* 무엇을 칠지가 아니라 **무엇을 누를지**를 적는다.  치라고
                안내하는 칸은 안 쓰이고, 그 안내에 적힌 별표는 마크다운이 안
                된다는 증거처럼 읽힌다. */}
            <span className="tiny faint">
              Ctrl+<kbd>B</kbd> <strong>굵게</strong>
              <span className="dim"> · </span>
              Ctrl+<kbd>I</kbd> <em>기울임</em>
              <span className="dim"> · </span>
              Ctrl+<kbd>E</kbd> <code>코드</code>
              <span className="dim"> · </span>
              Ctrl+<kbd>Enter</kbd> 올리기
            </span>
          </div>
          {error ? <Alert kind="warn">{error}</Alert> : null}
        </div>
      </Card>

      {board.error ? <Alert kind="warn">F&amp;Q 를 읽지 못했습니다.</Alert> : null}

      <Card title={<h2>열려 있는 것</h2>}
            actions={<span className="tiny faint">{open.length}개</span>}>
        {open.length ? (
          <div className="col" style={{ gap: 10 }}>
            {open.map((note) => (
              <NoteCard key={note.id} note={note} onChanged={() => board.reload()} />
            ))}
          </div>
        ) : board.loading ? (
          <Spinner label="읽는 중" />
        ) : (
          <Empty title="열려 있는 것이 없습니다">
            <span className="tiny faint">
              쓰다가 걸리는 것이 있으면 위에 한 줄 적어 두세요.
            </span>
          </Empty>
        )}
      </Card>

      {done.length ? (
        <Card
          title={<h2>정리된 것</h2>}
          actions={
            <span className="tiny faint">{done.length}개 · 지우지 않고 남겨 둡니다</span>
          }
        >
          <div className="col" style={{ gap: 10 }}>
            {done.map((note) => (
              <NoteCard key={note.id} note={note} onChanged={() => board.reload()} />
            ))}
          </div>
        </Card>
      ) : null}
    </main>
  )
}

function NoteCard({ note, onChanged }: { note: FeedbackNote; onChanged: () => void }) {
  const [reply, setReply] = useState('')
  const [busy, setBusy] = useState(false)
  const kind = kindOf(note.kind)
  const resolved = Boolean(note.resolved_at)

  async function run(work: () => Promise<unknown>) {
    if (busy) return
    setBusy(true)
    try {
      await work()
      onChanged()
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className={`note-card${resolved ? ' resolved' : ''}`}>
      <div className="row" style={{ alignItems: 'baseline', gap: 8 }}>
        <span className={`tag ${note.kind}`}>{kind.label}</span>
        <span className="tiny faint">{note.created_by || '이름 없음'}</span>
        <span className="tiny faint">{dateTime(note.created_at)}</span>
        <span className="spacer" style={{ flex: 1 }} />
        {resolved ? (
          <span className="tiny faint nowrap">
            {note.resolved_by || '누군가'} 정리 · {dateTime(note.resolved_at)}
          </span>
        ) : null}
      </div>

      <Markdown body={note.body} className="note-body" />

      {note.replies.length ? (
        <ul className="note-replies">
          {note.replies.map((item) => (
            <li key={item.id}>
              <div className="row" style={{ alignItems: 'baseline', gap: 6 }}>
                <span className="tiny faint">{item.created_by || '이름 없음'}</span>
                <span className="tiny faint">{dateTime(item.created_at)}</span>
                <span style={{ flex: 1 }} />
                {/* 해결하면 그 댓글만 지운다 — 항목은 기록으로 남는다. */}
                <button
                  type="button"
                  className="link-btn tiny"
                  // 한 카드에 '지우기' 가 둘이다 (답글 · 항목).  글자는 같아도
                  // 무엇이 지워지는지는 달라야 한다.
                  aria-label="답글 지우기"
                  disabled={busy}
                  onClick={() => run(() => api.deleteFeedbackReply(note.id, item.id))}
                >
                  지우기
                </button>
              </div>
              <Markdown body={item.body} className="tiny" />
            </li>
          ))}
        </ul>
      ) : null}

      <div className="row" style={{ gap: 6, marginTop: 6 }}>
        <input
          aria-label={`${note.id}번에 답글`}
          value={reply}
          placeholder="답글"
          onChange={(event) => setReply(event.target.value)}
          onKeyDown={(event) => {
            if (event.key !== 'Enter' || !reply.trim()) return
            void run(async () => {
              await api.replyToFeedback(note.id, { body: reply.trim() })
              setReply('')
            })
          }}
          style={{ flex: 1 }}
        />
        <button
          type="button"
          className="ghost sm"
          disabled={busy || !reply.trim()}
          onClick={() =>
            run(async () => {
              await api.replyToFeedback(note.id, { body: reply.trim() })
              setReply('')
            })
          }
        >
          답글
        </button>
        {/* 되돌릴 수 없는 버튼은 아무도 안 누른다 — 그래서 다시 열 수 있다. */}
        <button
          type="button"
          className="ghost sm"
          disabled={busy}
          onClick={() => run(() => api.updateFeedback(note.id, { resolved: !resolved }))}
        >
          {resolved ? '다시 열기' : '정리됨'}
        </button>
        <button
          type="button"
          className="ghost sm danger"
          aria-label="항목 지우기"
          disabled={busy}
          onClick={() => {
            if (!window.confirm('이 항목과 답글을 모두 지울까요?')) return
            void run(() => api.deleteFeedback(note.id))
          }}
        >
          지우기
        </button>
      </div>
    </div>
  )
}
