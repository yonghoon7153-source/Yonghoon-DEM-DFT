/** 목록을 폴더로 — 그룹 → 소그룹 → 셀 (ADR 0035).
 *
 *  셀은 이미 두 단계로 묶여 있다 (ADR 0025): 최상위 그룹 아래에 소그룹, 그
 *  아래에 셀.  셀은 **한 자리에만** 살아서 `group_id` 가 소그룹을 가리키면
 *  그 셀은 소그룹 것이고, 최상위를 가리키면 그 그룹 바로 밑에 있다.
 *
 *  여기 있는 것은 그 구조를 **화면이 접었다 펼 수 있는 모양**으로 다시 펴는
 *  일뿐이다.  서버는 그대로다 — 새 표도 새 라우터도 없다.
 */

/** 폴더로 묶을 수 있는 것.  대시보드 줄이든 셀이든 이 셋만 있으면 된다. */
export interface Placed {
  /** 셀의 id — 달라진 것을 세는 열쇠다 (`folderDelta`). */
  id: number
  groupId: number | null
  groupName: string
  /** 그 그룹이 소그룹이면 그 위 그룹의 이름.  최상위면 빈 문자열. */
  groupParentName: string
}

export interface Folder<T> {
  /** 접힘을 기억하는 열쇠.  그룹 id 를 쓰면 이름을 고쳐도 접힌 채로 남는다. */
  key: string
  name: string
  /** 0 = 최상위 그룹, 1 = 소그룹.  화면의 들여쓰기가 이것을 따라간다. */
  depth: number
  /** 이 폴더에 **직접** 든 것들.  자식 폴더의 것은 안 센다 — 그려지는 줄이다. */
  items: T[]
  /** 이 폴더와 그 자식들을 합친 것.
   *
   *  달라진 수를 세는 것은 **이쪽**이다.  최상위 폴더에 직접 든 셀이 하나도
   *  없는 것은 흔한데, `items` 로 세면 그런 폴더는 밑에서 무슨 일이 나든
   *  영원히 `0` 이다 — 접어 둔 폴더가 바로 그 경우라, 접었을 때 아무 표시도
   *  안 뜨면 폴더를 접어 두는 이유 자체가 없어진다. */
  subtree: T[]
  /** 접었을 때 보여 주는 수 = `subtree.length`. */
  total: number
  /** 접으면 같이 숨는 폴더들의 `key`.  최상위 폴더만 채워진다. */
  children: string[]
}

/** 묶음이 없는 셀들이 가는 곳.  마지막에 온다. */
export const UNGROUPED = 'ungrouped'

/** 목록을 폴더 차례로 편다 — 최상위, 그 소그룹들, … 그리고 묶음 없음.
 *
 *  **빈 폴더는 만들지 않는다.**  필터로 셀이 다 빠진 그룹까지 그리면 화면의
 *  절반이 "0개" 가 되고, 그 목록은 무엇이 걸러졌는지가 아니라 어떤 그룹이
 *  있는지를 말하게 된다 — 그건 그룹 관리 화면이 할 일이다 (ADR 0035).
 *
 *  차례는 **이름순**이다.  올린 시각순으로 두면 파일 하나가 들어올 때마다
 *  폴더가 자리를 옮기고, 접어 둔 것을 다시 찾아야 한다.
 */
export function buildFolders<T>(
  items: T[], place: (item: T) => Placed,
): Folder<T>[] {
  /** 최상위 이름 → (소그룹 이름 | '' → 것들) */
  const tree = new Map<string, Map<string, T[]>>()
  const keyOf = new Map<string, string>()
  const loose: T[] = []

  for (const item of items) {
    const at = place(item)
    if (at.groupId === null || !at.groupName) {
      loose.push(item)
      continue
    }
    // 부모 이름이 있으면 그 셀은 소그룹에 산다.  없으면 최상위 바로 밑이다.
    const top = at.groupParentName || at.groupName
    const sub = at.groupParentName ? at.groupName : ''
    const branch = tree.get(top) ?? new Map<string, T[]>()
    tree.set(top, branch)
    branch.set(sub, [...(branch.get(sub) ?? []), item])
    // 접힘의 열쇠는 id 다 — 이름을 고쳐도 접힌 채로 남는다.  최상위의 id 는
    // 그 밑의 셀이 소그룹에 살면 알 수 없으므로 이름을 쓴다.
    if (sub) keyOf.set(`${top}/${sub}`, String(at.groupId))
  }

  const out: Folder<T>[] = []
  for (const top of [...tree.keys()].sort((a, b) => a.localeCompare(b, 'ko'))) {
    const branch = tree.get(top)!
    const subs = [...branch.keys()].filter(Boolean)
      .sort((a, b) => a.localeCompare(b, 'ko'))
    const children = subs.map((sub) => keyOf.get(`${top}/${sub}`) ?? `${top}/${sub}`)
    const direct = branch.get('') ?? []
    const subtree = [...branch.values()].flat()
    out.push({
      key: `top:${top}`,
      name: top,
      depth: 0,
      items: direct,
      subtree,
      total: subtree.length,
      children,
    })
    for (const [index, sub] of subs.entries()) {
      const list = branch.get(sub) ?? []
      out.push({
        key: children[index]!,
        name: sub,
        depth: 1,
        items: list,
        subtree: list,
        total: list.length,
        children: [],
      })
    }
  }

  // 묶음 없음은 맨 아래.  "아직 안 넣었다" 는 조건이 아니라 미완이라, 위에
  // 두면 실제 묶음들을 매번 밀어낸다.
  if (loose.length) {
    out.push({ key: UNGROUPED, name: '묶음 없음', depth: 0,
               items: loose, subtree: loose, total: loose.length, children: [] })
  }
  return out
}

// --- 지난번과 달라진 것 (ADR 0035) ------------------------------------------

/** 폴더 열쇠 → 그때 그 폴더에 있던 셀 id 들. */
export type FolderSnapshot = Record<string, number[]>

export interface FolderDelta {
  added: number
  removed: number
}

/** 지금과 그때를 견준다.
 *
 *  **개수가 아니라 집합이다.**  하나가 들어오고 하나가 나간 날 개수만 세면
 *  0 이 되어 아무 일도 없던 것처럼 보이는데, 그날이야말로 봐야 하는 날이다.
 *
 *  `before` 가 `undefined` 면 처음 보는 폴더다.  기억 자체가 없는 경우
 *  (`hasMemory === false`) 에는 아무것도 세지 않는다 — 모든 셀이 새 것으로
 *  보이지만 그건 사실이 아니라 기억이 없다는 뜻이다 (§0.4).
 */
export function folderDelta(
  now: number[], before: number[] | undefined, hasMemory: boolean,
): FolderDelta {
  if (!hasMemory) return { added: 0, removed: 0 }
  const then = new Set(before ?? [])
  const here = new Set(now)
  let added = 0
  for (const id of here) if (!then.has(id)) added += 1
  let removed = 0
  for (const id of then) if (!here.has(id)) removed += 1
  return { added, removed }
}
