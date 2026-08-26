/** 표의 이름 앞에 붙는 이름표 — 그룹과 올린 사람.
 *
 *  대시보드가 먼저 쓰던 모양을 한 자리로 모은 것이다.  열로 따로 두면 이름과
 *  "누구의 어느 묶음인가" 가 표 폭만큼 떨어져 한 줄을 읽는 데 눈이 세 번
 *  움직이고, 화면마다 각자 그리면 같은 표가 화면마다 다르게 생긴다.
 *
 *  **없으면 아무것도 그리지 않는다.**  그룹이 안 붙은 측정은 정상이고 (§0.4),
 *  빈 이름표는 "그룹이 있는데 이름이 없다" 로 읽힌다.
 */

/** 그룹 이름표.  `path` 는 마우스를 올렸을 때 보이는 "부모 · 자식" 전체다. */
export function GroupTag({ name, path }: { name?: string | null; path?: string }) {
  if (!name) return null
  return (
    <span className="group-tag" title={`그룹: ${path || name}`}>{name}</span>
  )
}

/** 올린 사람 이름표. */
export function OwnerTag({ owner, label = '올린 사람' }: {
  owner?: string | null
  label?: string
}) {
  if (!owner) return null
  return <span className="owner-tag" title={`${label}: ${owner}`}>{owner}</span>
}

/** 서버가 "부모 · 자식" 한 줄(`group_label`)로만 줄 때 잎 이름만 떼어 낸다.
 *
 *  이름표에는 잎만 적고 전체 길은 title 로 돌린다 — 12ch 로 잘리는 칩에
 *  부모까지 넣으면 정작 구별에 쓰이는 잎이 잘려 나간다.
 */
export function leafOf(label?: string | null): string {
  if (!label) return ''
  const parts = label.split(' · ')
  return parts[parts.length - 1] ?? ''
}
