/** 라이브러리 세 곳이 함께 쓰는 **묶기**.
 *
 *  셀·임피던스·GITT 라이브러리가 하는 일은 같다: 표를 무엇으로 묶어 볼지
 *  고르고, 그 묶음마다 구분 줄을 하나 얹는다.  세 곳이 각자 갖고 있으면
 *  어휘가 갈리고 (한쪽에만 '작성자' 가 있고), 무엇보다 폴더가 한 곳에만
 *  생긴다 — 한 화면에서 익힌 손이 다른 화면에서 안 통한다.
 *
 *  **그룹만 폴더다.**  그룹은 사람이 만든 *자리*라 위아래가 있고 (그룹 →
 *  소그룹, ADR 0025) 접었다 펼 것이 있다.  나머지(작성자·양극재·공정·온도)는
 *  *값*이라 평평하다 — 접을 트리가 없는데 폴더 모양을 흉내 내면 그룹 트리와
 *  헷갈리기만 한다.
 */

export type GroupKey = 'none' | 'group' | 'owner' | 'cathode' | 'process' | 'temperature'

/** 무엇으로 묶을 수 있는가.
 *
 *  그룹은 사람이 만들어 붙이는 것이고, 나머지는 이미 기록에 적혀 있는 것이다.
 *  그룹을 만들기 전에도 "같은 조건 세 번 돌린 것" 을 나란히 보고 싶은 것이
 *  실제 요구라서, 값으로 묶는 길을 열어 둔다.
 */
export const GROUP_KEYS: [GroupKey, string][] = [
  ['none', '없음'],
  ['group', '그룹'],
  // 누가 올린 것인가.  한 서버를 여럿이 쓰면 표에서 남의 것과 내 것이 섞이고,
  // 이름만 보고는 알 수 없다 (ADR 0012 — 이름은 기록이지 신원 확인이 아니다).
  ['owner', '작성자'],
  ['cathode', '양극재'],
  ['process', '공정'],
  ['temperature', '온도'],
]

/** 저장된 값이 우리가 아는 것인가.  모르는 값이면 '없음' 으로 떨어뜨린다 —
 *  옛 브라우저에 남은 문자열 하나가 표를 통째로 비게 만들면 안 된다. */
export function validGroupKey(value: unknown): GroupKey {
  return GROUP_KEYS.some(([key]) => key === value) ? (value as GroupKey) : 'none'
}

export function GroupByControl({
  value,
  onChange,
}: {
  value: GroupKey
  onChange: (value: GroupKey) => void
}) {
  return (
    <div className="row" style={{ gap: 6 }}>
      <span className="tiny faint">묶기</span>
      <div className="segmented" role="group" aria-label="묶기">
        {GROUP_KEYS.map(([key, label]) => (
          <button
            key={key}
            type="button"
            className={value === key ? 'on' : ''}
            onClick={() => onChange(key)}
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  )
}

/** 값으로 묶는다 — 그룹이 아닌 묶기 전부.
 *
 *  값이 없는 묶음은 맨 아래.  나머지는 이름순 — 새로 올린 것이 목록을 흔들지
 *  않으려면 순서가 내용에만 달려 있어야 한다.  `null` 이면 안 묶는다.
 */
export function bucketize<T>(
  items: T[], key: GroupKey, labelOf: (item: T, key: GroupKey) => string,
): [string, T[]][] | null {
  if (key === 'none' || key === 'group') return null
  const buckets = new Map<string, T[]>()
  for (const item of items) {
    const label = labelOf(item, key)
    const bucket = buckets.get(label)
    if (bucket) bucket.push(item)
    else buckets.set(label, [item])
  }
  return [...buckets.entries()].sort(([a], [b]) => {
    if (!a) return 1
    if (!b) return -1
    return a.localeCompare(b, 'ko')
  })
}

/** 값 묶음의 구분 줄.  폴더가 아니므로 접는 삼각형이 없다. */
export function BucketRow({
  label,
  count,
  columns,
}: {
  label: string
  count: number
  columns: number
}) {
  return (
    <tr className="section">
      <th colSpan={columns}>
        {/* 가로 스크롤에 붙는 것은 이 span 이다 — 칸 자체는 표 전체 폭이라
            붙잡을 여지가 없다 (app.css 의 .section-label). */}
        <span className="section-label">
          {/* 폴더 줄과 같은 강조 (FolderTree 의 `.folder-name`).  묶는 방법이
              달라도 **묶음 줄은 같아 보여야** 한다 — 한쪽에서 익힌 눈이 다른
              쪽에서 그대로 통해야 하므로.
              '미입력' 은 값이 아니라 **없다는 말**이라 안 칠한다.  칠하면
              빈 칸이 이름처럼 읽힌다 (§0.4). */}
          {label
            ? <span className="folder-name">{label}</span>
            : <span className="faint">미입력</span>}
          <span className="faint"> · {count}개</span>
        </span>
      </th>
    </tr>
  )
}
