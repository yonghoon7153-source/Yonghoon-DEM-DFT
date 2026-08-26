/** 제목 자리에서 그대로 고치는 이름.
 *
 *  셀에서 먼저 만들었고 (`SampleDetail` 의 `CellName`), 임피던스·GITT 상세도
 *  같은 것을 필요로 했다 — 거기서는 제목이 그냥 글자라 눌러도 아무 일이 없었고,
 *  이름을 고치려면 목록으로 돌아가야 했다.  같은 부품을 세 번 쓰기로 하고
 *  옮겼다: 여섯 가지 가드를 세 번 다시 쓰는 것이 이 종류의 사고가 나는 자리다.
 *
 *  지키는 것:
 *
 *  1. **빈 이름으로 저장하지 않는다.**  서버도 422 로 막지만, 화면이 먼저
 *     말해 줘야 왕복 한 번을 아낀다.
 *  2. **실패하면 편집을 닫지 않는다.**  닫으면 방금 친 이름이 사라지고,
 *     화면에는 옛 이름이 남아 저장된 것처럼 보인다.
 *  3. **안 친 편집기는 남의 수정을 덮지 않는다** (#31).  A 가 focus 만 한
 *     사이 B 가 이름을 바꾸면, draft(옛것)와 live(새것)가 달라 "고쳤다" 로
 *     읽혔다 — `touched` 와 `base` 가 그 둘을 가른다.
 *
 *  적용은 Enter 와 포커스 이탈, 취소는 Esc.
 */

import { useEffect, useState } from 'react'

import { Alert } from './ui'

export function EditableName({
  name,
  label,
  onSave,
}: {
  /** 지금 서버에 있는 이름.  편집 중에 바뀌면 그것도 여기로 들어온다. */
  name: string
  /** 편집기의 접근성 이름 — "셀 이름", "스펙트럼 이름" 처럼. */
  label: string
  onSave: (name: string) => Promise<void>
}) {
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState(name)
  const [base, setBase] = useState(name)
  const [touched, setTouched] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  // 다른 사람이 이름을 고쳤을 수 있다.  안 친 편집기는 따라가고, 치고 있는
  // 글자는 덮지 않는다 — 지워지면 무엇을 잃었는지도 모른다.
  useEffect(() => {
    if (!editing) {
      setDraft(name)
      return
    }
    if (!touched) {
      setDraft(name)
      setBase(name)
    }
  }, [name, editing, touched])

  const commit = async () => {
    if (busy) return
    const next = draft.trim()
    if (!next) {
      setError('이름은 비울 수 없습니다.')
      return
    }
    if (!touched || next === name) {
      setEditing(false)
      setError(null)
      return
    }
    if (name !== base) {
      // 편집하는 사이 다른 곳에서 이름이 바뀌었다.  조용히 덮지 않고 묻는다;
      // 기준을 지금 값으로 옮겨 두므로, 보고도 저장하면 그때는 진짜 의도다.
      setError(
        `편집하는 사이 이름이 '${name}' 으로 바뀌었습니다 — ` +
          '덮어쓰려면 다시 저장하세요.',
      )
      setBase(name)
      return
    }
    setBusy(true)
    try {
      await onSave(next)
      setEditing(false)
      setError(null)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
    }
  }

  if (!editing) {
    return (
      <h1 className="truncate">
        <button
          type="button"
          className="title-edit"
          title="눌러서 이름 고치기"
          onClick={() => {
            setDraft(name)
            setBase(name)
            setTouched(false)
            setError(null)
            setEditing(true)
          }}
        >
          {/* 이름이 길면 잘려야 한다 — 자르기는 글자를 들고 있는 칸에
              걸어야 하고, inline-flex 인 버튼에 걸면 듣지 않는다. */}
          <span className="truncate">{name}</span>
          <span className="pencil" aria-hidden="true">✎</span>
        </button>
      </h1>
    )
  }

  return (
    <div className="col" style={{ gap: 4 }}>
      <input
        className="title-input"
        aria-label={label}
        autoFocus
        value={draft}
        disabled={busy}
        onChange={(event) => {
          setDraft(event.target.value)
          setTouched(true)
        }}
        onBlur={() => void commit()}
        onKeyDown={(event) => {
          if (event.key === 'Enter') {
            event.preventDefault()
            void commit()
          }
          if (event.key === 'Escape') {
            setDraft(name)
            setError(null)
            setEditing(false)
          }
        }}
      />
      {error ? <Alert kind="error">{error}</Alert> : null}
    </div>
  )
}
