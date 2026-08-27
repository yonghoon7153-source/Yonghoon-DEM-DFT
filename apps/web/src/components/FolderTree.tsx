/** 폴더 — 표 안에서 접었다 펴는 묶음 줄 (ADR 0035).
 *
 *  대시보드와 라이브러리가 같은 것을 쓴다.  두 표는 열이 서로 다르지만 묶는
 *  규칙은 하나여야 한다 — 한쪽에서 익힌 손이 다른 쪽에서 통해야 하고, 무엇보다
 *  `+2 −1` 의 기준이 화면마다 다르면 그 수는 아무 뜻이 없다.
 */

import { useEffect, useMemo, useRef } from 'react'

import { useStickyState } from '../lib/hooks'
import {
  type Folder, type FolderDelta, type FolderSnapshot, type Placed,
  buildFolders, folderDelta,
} from '../lib/folders'

const SNAPSHOT_PREFIX = 'bml.folders.'
//: 손으로 **바꾼 것만** 적어 둔다 (열쇠 → 폈나).  기본이 깊이마다 다르므로
//: (아래 `useFolders`) 목록 하나로는 "안 건드림" 과 "일부러 접음" 을 가를 수가
//: 없다 — 최상위를 일부러 접어 둔 것과 아직 아무것도 안 한 것이 같아진다.
//:
//: 열쇠 이름이 세 번째다.  담는 모양이 바뀔 때마다 새 이름을 쓴다: 옛 값을
//: 새 뜻으로 읽으면 정확히 반대로 접힌다.  한 번 쓰고 버리는 값이라 옛 열쇠는
//: 그냥 안 읽는다.
const OPEN_PREFIX = 'bml.folders.open2.'

function readSnapshot(key: string): FolderSnapshot | null {
  try {
    const stored = window.localStorage.getItem(SNAPSHOT_PREFIX + key)
    return stored === null ? null : (JSON.parse(stored) as FolderSnapshot)
  } catch {
    // 저장소를 못 쓰는 창(사생활 보호)에서는 **기억 없음**이다.  없는 기억을
    // 빈 기억으로 두면 모든 셀이 새 것으로 보인다 (§0.4).
    return null
  }
}

function writeSnapshot(key: string, snapshot: FolderSnapshot): void {
  try {
    window.localStorage.setItem(SNAPSHOT_PREFIX + key, JSON.stringify(snapshot))
  } catch {
    /* 못 적어도 화면은 그대로 돈다 — 다음에 열면 표시가 없을 뿐이다 */
  }
}

export interface FolderView<T> {
  folders: Folder<T>[]
  /** 이 폴더가 접혀 있는가. */
  isFolded: (key: string) => boolean
  /** 이 폴더의 줄을 지금 그려야 하는가 (제 폴더도 부모도 안 접혀 있는가). */
  isVisible: (folder: Folder<T>) => boolean
  toggle: (folder: Folder<T>) => void
  /** 지난번과 견준 것.  둘 다 0 이면 아무것도 안 바뀌었다는 뜻이다. */
  change: (folder: Folder<T>) => FolderDelta
}

/** 폴더를 만들고, 접힘과 "지난번" 을 브라우저에 기억해 둔다.
 *
 *  기준선은 **화면을 연 순간에 얼려 둔다** (`baseline` 이 ref 인 이유).  보는
 *  동안 상대가 올린 셀은 그 자리에서 `+1` 로 뜨고, 목록이 바뀔 때마다 "지금"
 *  을 저장하므로 다음에 열면 그것이 기준이 된다.
 */
export function useFolders<T>(
  scope: string, items: T[], place: (item: T) => Placed,
): FolderView<T> {
  //: **기본은 깊이가 정한다: 최상위는 펴고, 소그룹은 접는다.**
  //:
  //: 다 접으면 첫 화면이 묶음 이름 두 줄이라 무엇이 있는지 안 보이고, 다 펴면
  //: 예전의 평평한 목록과 똑같아 폴더가 있으나 마나다.  가운데가 파일
  //: 탐색기의 모양이고, 그것이 이 제안의 시작이었다 (ADR 0035) — 큰 칸은
  //: 보이고 그 안은 눌러서 연다.
  //:
  //: 그리고 이 배치라야 `+2 −1` 이 쓸모가 있다: 최상위는 제 아래 전부를 합쳐
  //: 세므로 (`subtree`) 펴 놓은 그 줄에 바뀐 수가 이미 적혀 있고, 어느 소그룹
  //: 인지는 그때 열어 보면 된다.
  const [open, setOpen] = useStickyState<Record<string, boolean>>(
    OPEN_PREFIX + scope, {})
  // 처음 한 번만 읽는다.  매 렌더마다 읽으면 아래에서 저장한 것을 도로 읽어
  // 기준선이 "지금" 이 되고, 그러면 아무것도 안 바뀐 것으로 보인다.
  const baseline = useRef<FolderSnapshot | null>(null)
  const loaded = useRef(false)
  if (!loaded.current) {
    baseline.current = readSnapshot(scope)
    loaded.current = true
  }

  const folders = useMemo(() => buildFolders(items, place), [items, place])

  const snapshot = useMemo(() => {
    const out: FolderSnapshot = {}
    // `items` 가 아니라 `subtree` 다 — 최상위 폴더에 직접 든 셀이 없으면
    // `items` 로 센 수는 밑에서 무슨 일이 나든 영원히 0 이다.
    for (const folder of folders) {
      out[folder.key] = folder.subtree.map((item) => place(item).id)
    }
    return out
  }, [folders, place])

  useEffect(() => {
    // 목록이 아직 안 왔을 때 저장하면 그 빈 목록이 다음번 기준이 되고, 다음에
    // 열면 있는 셀 전부가 `+n` 으로 뜬다.
    if (!folders.length) return
    writeSnapshot(scope, snapshot)
  }, [scope, snapshot, folders.length])

  // 열쇠만 받으므로 깊이를 여기서 찾는다 -- 부르는 쪽 전부가 폴더를 들고
  // 있지는 않다 (`isVisible` 은 부모의 열쇠만 안다).
  const depthOf = new Map(folders.map((folder) => [folder.key, folder.depth]))
  const isFolded = (key: string) =>
    !(open[key] ?? (depthOf.get(key) ?? 0) === 0)
  return {
    folders,
    isFolded,
    isVisible: (folder) =>
      folder.depth === 0
      || !folders.some((top) => top.children.includes(folder.key) && isFolded(top.key)),
    toggle: (folder) => setOpen({ ...open, [folder.key]: isFolded(folder.key) }),
    change: (folder) => folderDelta(
      snapshot[folder.key] ?? [],
      baseline.current?.[folder.key],
      baseline.current !== null),
  }
}

/** 표 안의 폴더 줄 — `<tbody>` 하나의 머리로 쓴다. */
export function FolderRow<T>({
  folder,
  view,
  columns,
}: {
  folder: Folder<T>
  view: FolderView<T>
  /** 표의 열 수 — 폴더 줄은 표 전체 폭이다. */
  columns: number
}) {
  const open = !view.isFolded(folder.key)
  const change = view.change(folder)
  // 기준이 무엇인지 적어 둔다.  브라우저마다 다른 수라, 적어 두지 않으면
  // "서버가 세어 준 수" 로 읽힌다 (ADR 0035 의 대가).
  const since = '이 브라우저에서 지난번에 이 화면을 떠날 때와 견준 것입니다'
  return (
    <tr className="section">
      <th colSpan={columns}>
        {/* 가로 스크롤에 붙는 것은 이 span 이다 — 칸 자체는 표 전체 폭이라
            붙잡을 여지가 없다 (app.css 의 .section-label). */}
        <span
          className="section-label"
          // 소그룹은 한 단계 안으로.  `.section-label` 이 이미 좌우 여백을
          // 갖고 있으므로 **더한다** — 덮어쓰면 들여쓴 티가 안 난다.
          style={folder.depth
            ? { paddingLeft: 'calc(var(--s4) + 22px)' } : undefined}
        >
          <button
            type="button"
            className="fold"
            aria-expanded={open}
            aria-label={`${folder.name} ${open ? '접기' : '펼치기'}`}
            onClick={() => view.toggle(folder)}
          >
            {open ? '▾' : '▸'}
          </button>
          {/* **이름만 칠한다.**  줄 전체를 강조색으로 두면 `· 26개` 와
              `+2 −1` 까지 같이 파래져서 이름과 수가 다시 한 덩어리가 된다 —
              가르려고 칠하는 것이므로 가를 것만 칠한다. */}
          <span className={folder.depth ? 'folder-name sub' : 'folder-name'}>
            {folder.name}
          </span>
          <span className="faint"> · {folder.total}개</span>
          {/* 들어온 것과 나간 것은 **색이 다르다.**  훑을 때 부호 하나로
              가르는 것보다 빠르고, `+2 −1` 이 한 덩어리로 읽히지 않는다. */}
          {change.added ? (
            <span className="folder-change more" title={since}>+{change.added}</span>
          ) : null}
          {change.removed ? (
            <span className="folder-change less" title={since}>−{change.removed}</span>
          ) : null}
        </span>
      </th>
    </tr>
  )
}
