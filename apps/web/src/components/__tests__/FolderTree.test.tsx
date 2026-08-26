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
  it('최상위를 접으면 그 소그룹까지 같이 숨는다', async () => {
    render(<Harness />)
    expect(screen.getByText('셀 1')).toBeInTheDocument()

    await userEvent.click(screen.getByRole('button', { name: 'Mid_Ni 접기' }))
    // 자식 폴더 줄 자체가 사라진다 — 남으면 부모 없는 폴더가 떠 있게 된다.
    expect(screen.queryByText('4.4V')).toBeNull()
    expect(screen.queryByText('셀 1')).toBeNull()
    // 형제 폴더는 그대로.
    expect(screen.getByText('묶음 없음')).toBeInTheDocument()

    await userEvent.click(screen.getByRole('button', { name: 'Mid_Ni 펼치기' }))
    expect(screen.getByText('셀 1')).toBeInTheDocument()
  })

  it('접힘은 새로고침 뒤에도 남는다 — 화면 상태이지 데이터가 아니다', async () => {
    const first = render(<Harness />)
    await userEvent.click(screen.getByRole('button', { name: '4.4V 접기' }))
    first.unmount()

    render(<Harness />)
    expect(await screen.findByRole('button', { name: '4.4V 펼치기' })).toBeInTheDocument()
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
    const badges = screen.getAllByTitle(/지난번에 이 화면을 떠날 때/)
    expect(badges.map((node) => node.textContent)).toEqual(['+1', '−1', '+1', '−1'])
    //                            ↑ Mid_Ni 는 4.4V 것을 합쳐 세므로 같은 수가 두 벌
    expect(badges[0]!.className).toContain('more')
    expect(badges[1]!.className).toContain('less')
  })
})
