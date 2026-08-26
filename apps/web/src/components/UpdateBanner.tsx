/** 워크벤치가 갱신되면 화면 위에 한 줄 — "새로고침하세요".
 *
 * 두 사람이 각자 고치고 `bml` 이 조용히 pull 한다.  그래서 서버는 새 코드로
 * 갈아탔는데 **열려 있는 탭은 옛 화면 그대로** 인 상태가 생긴다.  그 상태가
 * 위험한 이유는 조용해서다: 화면은 멀쩡하고, 방금 고친 것이 안 보일 뿐이라
 * 사람은 고쳐지지 않았다고 읽는다 (실측 — 용량을 고친 뒤 그대로 겪었다).
 *
 * 판정은 `served_commit` 하나로 한다.  **저장소의 HEAD 가 아니라 떠 있는
 * 서버의 것**이다 — 사람이 보는 화면을 정하는 것은 떠 있는 쪽이다.
 */

import { useEffect, useState } from 'react'

import { api } from '../lib/api'
import { useLiveRevision } from '../lib/hooks'

export function UpdateBanner() {
  // 처음 본 값이 기준이다.  이 탭이 언제 열렸든 "그때와 다른가" 만 묻는다.
  const [loaded, setLoaded] = useState<string | null>(null)
  const [now, setNow] = useState<string | null>(null)
  // 남이 뭔가 바꾸면 바로 한 번 더 본다 -- 갱신 직후가 제일 자주 바뀌는 때다.
  const revision = useLiveRevision(true)

  useEffect(() => {
    let alive = true
    async function look() {
      try {
        const at = await api.revision()
        if (!alive) return
        const commit = at.served_commit ?? ''
        if (!commit) return          // 모르면 아무 말도 안 한다
        setLoaded((first) => first ?? commit)
        setNow(commit)
      } catch {
        /* 서버가 잠깐 내려간 것뿐일 수 있다 — 그때 띠를 띄우면 거짓말이다 */
      }
    }
    void look()
    // 1분에 한 번.  더 자주 물어봐야 할 이유가 없다: 갱신은 사람이 하는
    // 일이고, 1분 늦게 아는 것이 문제가 된 적은 없다.
    const timer = window.setInterval(look, 60_000)
    return () => {
      alive = false
      window.clearInterval(timer)
    }
  }, [revision])

  if (!loaded || !now || loaded === now) return null

  return (
    <div className="update-banner" role="status">
      <span>
        <strong>워크벤치가 갱신됐습니다.</strong> 지금 보고 계신 화면은 갱신 전
        것입니다 — 새로고침하면 새 화면이 됩니다.
      </span>
      <button type="button" className="primary sm" onClick={() => window.location.reload()}>
        새로고침
      </button>
      {/* 자기 컴퓨터에서 띄운 사람은 새로고침만으로는 안 된다.  그 사람의
          서버는 여전히 옛 코드이고, 이 띠는 그 서버가 보낸 값으로 떠 있으므로
          애초에 안 뜬다 -- 하지만 **중추 서버를 보다가 자기 것으로 옮긴** 경우가
          있어서 한 줄 남긴다. */}
      <span className="tiny faint nowrap">자기 컴퓨터에서 띄우셨다면 <code>bml</code></span>
    </div>
  )
}
