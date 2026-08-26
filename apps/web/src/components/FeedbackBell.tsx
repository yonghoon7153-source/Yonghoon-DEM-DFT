/** 상단 막대 오른쪽의 F&Q 단추 — 그리고 알림 점.
 *
 * 점이 답하는 질문은 하나다: **내가 마지막으로 본 뒤에 뭔가 움직였나.**
 * 답글이 붙은 것도 움직인 것이라 `updated_at` 으로 재고 (서버가 답글에도 그
 * 값을 찍는다), 읽음은 브라우저에 적는다 — 사람을 구분할 방법이 없으므로
 * (ADR 0012), 서버에 두면 이름을 바꾼 순간 남의 읽음이 내 것이 된다.
 */

import { NavLink } from 'react-router-dom'

import { api } from '../lib/api'
import { useAsync } from '../lib/hooks'
import { countNewer, lastSeen } from '../lib/seen'

export function FeedbackBell() {
  // 이 단추는 모든 화면에 떠 있다.  자주 물으면 그만큼 서버를 두드리므로,
  // 편집 알림(live)에 얹고 2분에 한 번만 스스로 확인한다.
  const board = useAsync(() => api.listFeedback(), [], { live: true, refreshMs: 120_000 })
  const notes = board.data ?? []
  const since = lastSeen('feedback')
  const fresh = countNewer(notes.map((note) => note.updated_at), since)
  const open = notes.filter((note) => !note.resolved_at).length

  return (
    <NavLink
      to="/feedback"
      className="ghost sm bell"
      title={
        fresh
          ? `${fresh}건이 새로 올라왔거나 답이 붙었습니다`
          : open
            ? `열려 있는 것 ${open}건`
            : '쓰다가 걸린 것을 적어 두는 곳'
      }
    >
      F&amp;Q
      {fresh ? <span className="bell-dot" aria-label={`새 소식 ${fresh}건`} /> : null}
    </NavLink>
  )
}
