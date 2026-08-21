/** 이름 — 이 브라우저에서 저장한 것들에 붙는다.
 *
 * 로그인이 아니다.  아무도 검증하지 않고, 실패할 방법도 없다 (ADR 0012).
 * 처음 온 사람에게 한 번 묻고, 그다음부터는 상단 막대의 이름을 눌러 바꾼다.
 *
 * 이름이 없어도 전부 동작한다 — 기록이 "이름 없음" 으로 남을 뿐이다.  올릴
 * 파일이 20 MB 짜리인데 이름을 안 적었다고 막는 것은 도움이 아니다.
 */

import { useEffect, useRef, useState } from 'react'

import { MAX_NAME, readName, writeName } from '../lib/who'

export function WhoAmI() {
  const [name, setName] = useState(readName)
  // 이름이 없는 채로 시작하면 한 번 묻는다.  물어보는 시점이 여기인 이유는,
  // 저장하려는 순간에 묻는 창이 뜨면 하려던 일이 끊기기 때문이다.
  const [open, setOpen] = useState(() => !readName())
  const [draft, setDraft] = useState(name)
  const field = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (open) {
      setDraft(readName())
      field.current?.focus()
    }
  }, [open])

  function commit() {
    setName(writeName(draft))
    setOpen(false)
  }

  return (
    <>
      <button
        type="button"
        className={`ghost sm who${name ? '' : ' unnamed'}`}
        onClick={() => setOpen(true)}
        title={name ? '이름 바꾸기' : '이름을 적으면 저장한 것에 이름이 붙습니다'}
      >
        {name || '이름 없음'}
      </button>

      {open ? (
        <div
          className="modal-backdrop"
          role="presentation"
          onClick={(event) => {
            if (event.target === event.currentTarget) setOpen(false)
          }}
        >
          <div className="modal" role="dialog" aria-modal="true" aria-label="이름">
            <h3>이름을 적어 주세요</h3>
            <p className="small dim" style={{ margin: 0 }}>
              올린 파일과 고친 값에 이 이름이 붙습니다. 이 브라우저에만 저장되고,
              비밀번호는 없습니다.
            </p>
            <input
              ref={field}
              type="text"
              value={draft}
              maxLength={MAX_NAME}
              aria-label="이름"
              placeholder="예: 안용훈"
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') commit()
                if (event.key === 'Escape') setOpen(false)
              }}
            />
            <div className="row">
              <button type="button" className="primary" onClick={commit}>
                저장
              </button>
              {/* 이름 없이도 다 된다.  적기 싫은 사람을 붙잡아 두지 않는다. */}
              <button type="button" className="ghost" onClick={() => setOpen(false)}>
                나중에
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </>
  )
}

/** `용훈 · 3시간 전` — 누가 언제.  이름이 없으면 시간만. */
export function By({ who, at, verb }: { who?: string; at?: string; verb?: string }) {
  const parts = [who || null, at ? ago(at) : null].filter(Boolean)
  if (!parts.length) return null
  return (
    <span className="tiny faint nowrap">
      {verb ? `${verb} ` : ''}
      {parts.join(' · ')}
    </span>
  )
}

/** 사람이 실제로 쓰는 단위로 — 정확한 시각은 title 에 있으면 된다. */
export function ago(iso: string): string {
  // 서버는 UTC 를 시간대 표시 없이 보낸다.  Z 를 붙이지 않으면 브라우저가
  // 현지시로 읽어서, 한국에서는 모든 것이 9시간 미래에 일어난 일이 된다.
  const stamp = /[Z+]|-\d\d:\d\d$/.test(iso) ? iso : `${iso}Z`
  const minutes = Math.round((Date.now() - new Date(stamp).getTime()) / 60_000)
  if (!Number.isFinite(minutes)) return ''
  if (minutes < 1) return '방금'
  if (minutes < 60) return `${minutes}분 전`
  const hours = Math.round(minutes / 60)
  if (hours < 24) return `${hours}시간 전`
  const days = Math.round(hours / 24)
  if (days < 7) return `${days}일 전`
  return new Date(stamp).toLocaleDateString('ko-KR', { month: 'numeric', day: 'numeric' })
}
