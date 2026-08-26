/** 폴더로 접는 규칙 (ADR 0035). */

import { describe, expect, it } from 'vitest'

import { UNGROUPED, buildFolders, folderDelta } from '../folders'

interface Row { id: number; group_id: number | null; group_name: string
                group_parent_name: string }

const place = (row: Row) => ({
  id: row.id,
  groupId: row.group_id,
  groupName: row.group_name,
  groupParentName: row.group_parent_name,
})

const cell = (id: number, groupId: number | null, name = '', parent = ''): Row =>
  ({ id, group_id: groupId, group_name: name, group_parent_name: parent })

describe('buildFolders', () => {
  it('소그룹은 제 부모 밑에 들어간다 — 셀은 한 자리에만 산다 (ADR 0025)', () => {
    const folders = buildFolders([
      cell(1, 11, '4.4V', 'Mid_Ni'),
      cell(2, 12, '4.2V', 'Mid_Ni'),
      cell(3, 11, '4.4V', 'Mid_Ni'),
      cell(4, 10, 'Mid_Ni'),          // 최상위 바로 밑
    ], place)

    expect(folders.map((f) => [f.name, f.depth, f.items.length, f.total]))
      .toEqual([
        ['Mid_Ni', 0, 1, 4],   // 직접 하나, 자식까지 합쳐 넷
        ['4.2V', 1, 1, 1],
        ['4.4V', 1, 2, 2],
      ])
    // 달라진 수를 세는 것은 `subtree` 다.  최상위에 직접 든 셀이 없는 폴더가
    // 흔한데, `items` 로 세면 그런 폴더는 밑에서 무슨 일이 나도 0 이다.
    expect(folders[0]!.subtree.map((row) => row.id).sort()).toEqual([1, 2, 3, 4])
    // 최상위를 접으면 자식 폴더도 같이 숨어야 한다.
    expect(folders[0]!.children).toEqual([folders[1]!.key, folders[2]!.key])
  })

  it('접힘의 열쇠는 그룹 id 다 — 이름을 고쳐도 접힌 채로 남는다', () => {
    const before = buildFolders([cell(1, 11, '4.4V', 'Mid_Ni')], place)
    const after = buildFolders([cell(1, 11, '4.40 V', 'Mid_Ni')], place)
    expect(after[1]!.key).toBe(before[1]!.key)
  })

  it('묶음 없는 것은 맨 아래 한 폴더로', () => {
    const folders = buildFolders([
      cell(1, null),
      cell(2, 10, 'Mid_Ni'),
      cell(3, null),
    ], place)
    expect(folders.map((f) => f.name)).toEqual(['Mid_Ni', '묶음 없음'])
    expect(folders[1]!.key).toBe(UNGROUPED)
    expect(folders[1]!.items.map((row) => row.id)).toEqual([1, 3])
  })

  it('묶음 없는 것이 없으면 그 폴더도 없다 — 빈 폴더는 안 그린다', () => {
    expect(buildFolders([cell(1, 10, 'Mid_Ni')], place).map((f) => f.name))
      .toEqual(['Mid_Ni'])
  })

  it('차례는 이름순 — 올린 시각순이면 파일 하나에 폴더가 자리를 옮긴다', () => {
    const folders = buildFolders([
      cell(1, 20, 'Ni-rich'),
      cell(2, 10, 'Mid_Ni'),
      cell(3, 12, '4.2V', 'Mid_Ni'),
      cell(4, 11, '4.4V', 'Mid_Ni'),
    ], place)
    expect(folders.map((f) => f.name)).toEqual(['Mid_Ni', '4.2V', '4.4V', 'Ni-rich'])
  })
})

describe('folderDelta', () => {
  it('개수가 아니라 집합을 센다 — 하나 들어오고 하나 나간 날이 보여야 한다', () => {
    // 개수만 셌으면 0 이라 아무 일도 없던 것처럼 보였을 자리다.
    expect(folderDelta([1, 2, 3], [1, 2, 9], true)).toEqual({ added: 1, removed: 1 })
  })

  it('기억이 없으면 아무것도 안 센다 — 모르는 것을 새 것이라 하지 않는다', () => {
    expect(folderDelta([1, 2, 3], undefined, false)).toEqual({ added: 0, removed: 0 })
  })

  it('기억은 있는데 그 폴더가 없으면 진짜 새 폴더다', () => {
    expect(folderDelta([1, 2], undefined, true)).toEqual({ added: 2, removed: 0 })
  })

  it('차례가 달라도 같은 집합이면 안 바뀐 것이다 — 늘 붙어 있는 꼬리표는 아무도 안 본다', () => {
    expect(folderDelta([1, 2], [2, 1], true)).toEqual({ added: 0, removed: 0 })
  })
})
