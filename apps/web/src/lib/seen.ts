/** 마지막으로 본 때 — 알림 점의 전부다.
 *
 * 서버에 "누가 어디까지 읽었나" 를 저장하지 않는다.  그러려면 사람을 구분해야
 * 하는데 이 앱에는 로그인이 없고 (ADR 0012), 상단 막대의 이름은 아무나 적을 수
 * 있는 표시일 뿐이라 그것으로 읽음을 관리하면 이름을 바꾼 순간 남의 읽음이
 * 내 것이 된다.  **읽음은 브라우저의 것**이다 — 그 판단이 맞는 이유는, 점이
 * 답하려는 질문이 "이 화면 앞에 앉은 내가 저걸 봤나" 이기 때문이다.
 */

const PREFIX = 'bml.seen.'

/** 저장소를 못 쓰는 창(사생활 보호)에서는 **읽은 적 없음**으로 둔다.
 *  점이 계속 떠 있는 것이, 새 글이 있는데 안 뜨는 것보다 낫다. */
export function lastSeen(key: string): number {
  try {
    const saved = Number(window.localStorage.getItem(PREFIX + key))
    return Number.isFinite(saved) ? saved : 0
  } catch {
    return 0
  }
}

export function markSeen(key: string, at: number = Date.now()): void {
  try {
    window.localStorage.setItem(PREFIX + key, String(at))
  } catch {
    /* 못 적어도 화면은 그대로 돈다 */
  }
}

/** 마지막으로 본 뒤에 움직인 것이 몇 개인가.
 *
 * 밀리초를 그대로 비교하지 않고 1초를 봐준다.  서버 시각과 브라우저 시각이
 * 몇백 ms 어긋나 있으면, 방금 내가 쓴 글이 곧바로 "안 읽음" 으로 돌아온다 --
 * 그 점은 아무에게도 쓸모가 없다.
 */
export function countNewer(times: (string | null | undefined)[], since: number): number {
  if (!since) return times.filter(Boolean).length
  return times.filter((iso) => {
    if (!iso) return false
    const at = Date.parse(iso.endsWith('Z') ? iso : `${iso}Z`)
    return Number.isFinite(at) && at > since + 1000
  }).length
}
