/** 폴더 줄 — 접히는가, 그리고 `+2 −1` 이 무엇을 기준으로 세는가 (ADR 0035). */

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'

import { FolderRow, useFolders } from '../FolderTree'

interface Row { id: number; group: number | null; name: string; parent: string }

const place = (row: Row) => ({
  id: row.id,
  groupId: row.group,
  groupName: row.name,
  groupParentName: row.parent,
})

const CELLS: Row[] = [
  { id: 1, group: 11, name: '4.4V', parent: 'Mid_Ni' },
  { id: 2, group: 12, name: '4.2V', parent: 'Mid_Ni' },
  { id: 3, group: null, name: '', parent: '' },
]

function Harness({ rows = CELLS }: { rows?: Row[] }) {
  const view = useFolders('test', rows, place)
  return (
    <table>
      <tbody>
        {view.folders.filter(view.isVisible).map((folder) => (
          <tr key={folder.key}>
            <td>
              <table>
                <tbody>
                  <FolderRow folder={folder} view={view} columns={1} />
                  {view.isFolded(folder.key) ? null : folder.items.map((row) => (
                    <tr key={row.id}><td>셀 {row.id}</td></tr>
                  ))}
                </tbody>
              </table>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

beforeEach(() => window.localStorage.clear())
afterEach(() => window.localStorage.clear())

describe('폴더 줄', () => {
  it('처음에는 다 접혀 있다 — 그래야 첫 화면이 곧 요약이다', () => {
    render(<Harness />)
    // 최상위 폴더 이름과 수만 보인다.
    expect(screen.getByText('Mid_Ni')).toBeInTheDocument()
    expect(screen.getByText('묶음 없음')).toBeInTheDocument()
    // 소그룹도 셀도 아직 없다 — 펴야 나온다.
    expect(screen.queryByText('4.4V')).toBeNull()
    expect(screen.queryByText('셀 1')).toBeNull()
    expect(screen.queryByText('셀 3')).toBeNull()
  })

  it('최상위를 펴면 소그룹이 나오고, 다시 접으면 같이 숨는다', async () => {
    render(<Harness />)
    await userEvent.click(screen.getByRole('button', { name: 'Mid_Ni 펼치기' }))
    // 소그룹 줄은 나오지만 그 안의 셀은 아직 접혀 있다 — 한 단계씩 편다.
    expect(screen.getByText('4.4V')).toBeInTheDocument()
    expect(screen.queryByText('셀 1')).toBeNull()

    await userEvent.click(screen.getByRole('button', { name: '4.4V 펼치기' }))
    expect(screen.getByText('셀 1')).toBeInTheDocument()

    await userEvent.click(screen.getByRole('button', { name: 'Mid_Ni 접기' }))
    // 자식 폴더 줄 자체가 사라진다 — 남으면 부모 없는 폴더가 떠 있게 된다.
    expect(screen.queryByText('4.4V')).toBeNull()
    expect(screen.queryByText('셀 1')).toBeNull()
    // 형제 폴더는 그대로.
    expect(screen.getByText('묶음 없음')).toBeInTheDocument()
  })

  it('펴 둔 것은 새로고침 뒤에도 펴져 있다 — 화면 상태이지 데이터가 아니다', async () => {
    const first = render(<Harness />)
    await userEvent.click(screen.getByRole('button', { name: 'Mid_Ni 펼치기' }))
    await userEvent.click(screen.getByRole('button', { name: '4.4V 펼치기' }))
    first.unmount()

    render(<Harness />)
    expect(await screen.findByRole('button', { name: '4.4V 접기' })).toBeInTheDocument()
    expect(screen.getByText('셀 1')).toBeInTheDocument()
  })

  it('처음 보는 사람에게는 표시가 없다 — 기억이 없는 것은 새 것이 아니다', () => {
    render(<Harness />)
    expect(screen.queryByTitle(/지난번에 이 화면을 떠날 때/)).toBeNull()
  })

  it('지난번에 없던 셀은 `+1`, 있던 셀이 빠지면 `−1`', () => {
    const first = render(<Harness rows={CELLS} />)
    first.unmount()

    // 하나 들어오고 하나 나갔다.  개수만 셌으면 0 이라 아무 일도 없던 것처럼
    // 보였을 자리다.
    render(<Harness rows={[
      { id: 4, group: 11, name: '4.4V', parent: 'Mid_Ni' },
      { id: 2, group: 12, name: '4.2V', parent: 'Mid_Ni' },
      { id: 3, group: null, name: '', parent: '' },
    ]} />)
    // 들어온 것과 나간 것은 따로 그린다 — 색이 다르므로 조각도 둘이다.
    // **접힌 채로도 보여야 한다.**  그것이 `subtree` 로 세는 이유다 — 첫
    // 화면에서 어느 묶음이 움직였는지 훑는 것이 이 수의 용도다.
    const badges = screen.getAllByTitle(/지난번에 이 화면을 떠날 때/)
    expect(badges.map((node) => node.textContent)).toEqual(['+1', '−1'])
    expect(badges[0]!.className).toContain('more')
    expect(badges[1]!.className).toContain('less')
    expect(screen.queryByText('4.4V')).toBeNull()
  })
})
