/** 폴더 줄 — 접히는가, 그리고 `+2 −1` 이 무엇을 기준으로 세는가 (ADR 0035). */

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'

import { FolderRow, useFolders } from '../FolderTree'

interface Row { id: number | string; group: number | null; name: string; parent: string }

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
  it('최상위는 펴져 있고 소그룹은 접혀 있다 — 파일 탐색기의 모양', () => {
    render(<Harness />)
    // 최상위는 펴져 있으므로 그 아래 소그룹 줄이 보인다.
    expect(screen.getByText('Mid_Ni')).toBeInTheDocument()
    expect(screen.getByText('4.4V')).toBeInTheDocument()
    // 그런데 소그룹은 접혀 있어 그 안의 셀은 아직 없다.
    expect(screen.queryByText('셀 1')).toBeNull()
    // 그룹 없는 것은 최상위라 (깊이 0) 곧바로 보인다.
    expect(screen.getByText('그룹 없음')).toBeInTheDocument()
    expect(screen.getByText('셀 3')).toBeInTheDocument()
  })

  it('소그룹을 펴면 그 안이 나온다', async () => {
    render(<Harness />)
    await userEvent.click(screen.getByRole('button', { name: '4.4V 펼치기' }))
    expect(screen.getByText('셀 1')).toBeInTheDocument()
  })

  it('최상위를 접으면 그 소그룹까지 같이 숨는다', async () => {
    render(<Harness />)
    await userEvent.click(screen.getByRole('button', { name: 'Mid_Ni 접기' }))
    // 자식 폴더 줄 자체가 사라진다 — 남으면 부모 없는 폴더가 떠 있게 된다.
    expect(screen.queryByText('4.4V')).toBeNull()
    // 형제 폴더는 그대로.
    expect(screen.getByText('그룹 없음')).toBeInTheDocument()
  })

  it('손으로 바꾼 것은 새로고침 뒤에도 그대로 — 기본과 갈라져야 한다', async () => {
    const first = render(<Harness />)
    // 기본과 **반대로** 둘 다 바꾼다: 최상위는 접고 소그룹은 편다.
    await userEvent.click(screen.getByRole('button', { name: '4.4V 펼치기' }))
    await userEvent.click(screen.getByRole('button', { name: '그룹 없음 접기' }))
    first.unmount()

    render(<Harness />)
    expect(await screen.findByRole('button', { name: '4.4V 접기' })).toBeInTheDocument()
    expect(screen.getByText('셀 1')).toBeInTheDocument()
    // 일부러 접은 최상위가 기본(펴짐)으로 되돌아가면 안 된다 — 목록 하나로는
    // "안 건드림" 과 "일부러 접음" 이 같아져서 그렇게 됐다.
    expect(screen.getByRole('button', { name: '그룹 없음 펼치기' })).toBeInTheDocument()
    expect(screen.queryByText('셀 3')).toBeNull()
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
    // **접힌 소그룹의 것도 최상위가 대신 말해 준다.**  그것이 `subtree` 로
    // 세는 이유다 — 첫 화면에서 어느 묶음이 움직였는지 훑는 것이 용도다.
    const badges = screen.getAllByTitle(/지난번에 이 화면을 떠날 때/)
    // Mid_Ni(최상위) 와 4.4V(소그룹) 가 같은 수를 말한다.
    expect(badges.map((node) => node.textContent)).toEqual(['+1', '−1', '+1', '−1'])
    expect(badges[0]!.className).toContain('more')
    expect(badges[1]!.className).toContain('less')
    // 그러면서 소그룹은 여전히 접혀 있다 — 셀은 안 보인다.
    expect(screen.queryByText('셀 4')).toBeNull()
  })

  it('묶음 이름만 강조색이다 — 수까지 같이 칠하면 도로 한 덩어리다', () => {
    render(<Harness />)
    const name = screen.getByText('Mid_Ni')
    expect(name.className).toContain('folder-name')
    // 소그룹은 `.sub` 다 — **원래 색**으로 돌아가고 한 눈금 작다.  둘 다
    // 파랗게 두면 층이 사라진다 (색 규칙은 `stylesheet.test.ts` 가 잡는다).
    expect(screen.getByText('4.4V').className).toContain('sub')
    expect(name.className).not.toContain('sub')
    // `· 3개` 는 이름 밖에 남아야 한다 -- 안에 들어가면 같이 칠해진다.
    expect(name.textContent).toBe('Mid_Ni')
  })

  it('셀에 안 붙은 줄도 센다 — 열쇠가 숫자가 아니어도', () => {
    // EIS·GITT 대시보드에는 `sample_id` 가 없는 줄이 있다.  전부 같은 값으로
    // 두면 서로 구별이 안 되어 **하나 들어오고 하나 나간 날이 0 으로 보인다.**
    const loose = (name: string): Row =>
      ({ id: `f:${name}`, group: null, name: '', parent: '' })
    const first = render(<Harness rows={[loose('a.mpr'), loose('b.mpr')]} />)
    first.unmount()

    render(<Harness rows={[loose('a.mpr'), loose('c.mpr')]} />)
    const badges = screen.getAllByTitle(/지난번에 이 화면을 떠날 때/)
    expect(badges.map((node) => node.textContent)).toEqual(['+1', '−1'])
  })
})
