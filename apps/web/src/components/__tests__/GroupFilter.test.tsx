/** 그룹 · 소그룹 (ADR 0025).
 *
 *  여기서 고정하는 것은 규칙 하나다: **드롭다운에 적힌 수와 그것을 골랐을 때
 *  보이는 목록은 같아야 한다.**  셀은 소그룹에만 살기 때문에 상위 그룹으로만
 *  거르면 셀이 가득한 그룹이 비어 보이는데, 사람은 그것을 "데이터가 사라졌다"
 *  로 읽는다.
 */

import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { GroupFilterFields, useGroupChoice, groupPath } from '../GroupFilter'
import type { Group } from '../../lib/types'

afterEach(() => vi.unstubAllGlobals())

function group(id: number, name: string, parentId: number | null = null,
               samples = 0): Group {
  return {
    id, name, parent_id: parentId, parent_name: '', subgroup_count: 0,
    description: '', color: '', created_at: '2026-08-01T00:00:00',
    updated_at: '2026-08-01T00:00:00', sample_count: samples, run_count: 0,
  }
}

const GROUPS = [
  group(1, '건식 시리즈', null, 3),
  group(2, '80wt%', 1, 2),
  group(3, '70wt%', 1, 1),
  group(4, '삼성SDI', null, 5),
]

function installGroups(made: unknown[] = []) {
  vi.stubGlobal('fetch', vi.fn(async (url: string, init?: RequestInit) => {
    if (init?.method === 'POST') {
      made.push(JSON.parse(String(init.body)))
      return { ok: true, status: 201, statusText: 'Created',
               json: async () => group(9, '새 소그룹', 1) }
    }
    return { ok: true, status: 200, statusText: 'OK', json: async () => GROUPS }
  }))
}

/** 화면 없이 훅만 보는 상자.  `includes` 는 화면이 아니라 규칙이다. */
function Probe({ ids, creatable = false }: { ids: (number | null)[]; creatable?: boolean }) {
  const pick = useGroupChoice()
  return (
    <>
      <GroupFilterFields pick={pick} creatable={creatable} />
      <div data-testid="scope">{ids.filter((id) => pick.includes(id)).join(',')}</div>
      <div data-testid="effective">{String(pick.effective)}</div>
    </>
  )
}

describe('그룹 · 소그룹', () => {
  it('그룹 드롭다운에는 최상위만 — 소그룹은 옆칸의 몫이다', async () => {
    installGroups()
    render(<Probe ids={[]} />)

    const top = await screen.findByRole('combobox', { name: '그룹' })
    await waitFor(() =>
      expect([...top.querySelectorAll('option')].map((o) => o.textContent))
        .toEqual(['그룹 없음', '건식 시리즈 (3)', '삼성SDI (5)']))
  })

  it('그룹을 고르면 그 소그룹만 옆칸에 뜬다', async () => {
    installGroups()
    render(<Probe ids={[]} />)

    const sub = await screen.findByRole('combobox', { name: '소그룹' })
    expect(sub).toBeDisabled()   // 그룹을 안 골랐으면 고를 것이 없다

    await userEvent.selectOptions(
      await screen.findByRole('combobox', { name: '그룹' }), '1')
    await waitFor(() => expect(sub).not.toBeDisabled())
    expect([...sub.querySelectorAll('option')].map((o) => o.textContent))
      .toEqual(['소그룹 없음 (그룹 전체)', '80wt% (2)', '70wt% (1)'])
  })

  it('상위 그룹으로 거르면 소그룹의 셀도 든다', async () => {
    // 셀은 소그룹에만 산다.  상위 그룹만 보면 그 그룹은 비어 보인다.
    installGroups()
    render(<Probe ids={[1, 2, 3, 4]} />)
    await screen.findByRole('combobox', { name: '그룹' })

    await userEvent.selectOptions(screen.getByRole('combobox', { name: '그룹' }), '1')
    await waitFor(() =>
      expect(screen.getByTestId('scope').textContent).toBe('1,2,3'))
    // 서버에는 상위 그룹 id 하나만 보낸다 -- 펴는 일은 `group_scope` 가 한다.
    expect(screen.getByTestId('effective').textContent).toBe('1')
  })

  it('소그룹까지 고르면 그것 하나로 좁혀진다', async () => {
    installGroups()
    render(<Probe ids={[1, 2, 3, 4]} />)
    await screen.findByRole('combobox', { name: '그룹' })

    await userEvent.selectOptions(screen.getByRole('combobox', { name: '그룹' }), '1')
    await waitFor(() => expect(screen.getByTestId('scope').textContent).toBe('1,2,3'))
    await userEvent.selectOptions(screen.getByRole('combobox', { name: '소그룹' }), '2')

    await waitFor(() => expect(screen.getByTestId('scope').textContent).toBe('2'))
    expect(screen.getByTestId('effective').textContent).toBe('2')
  })

  it('그룹을 바꾸면 소그룹은 놓는다', async () => {
    // 옛 그룹의 자식이 골라진 채로 남으면, 화면에 없는 조건으로 걸러진 빈
    // 목록이 나온다.
    installGroups()
    render(<Probe ids={[1, 2, 3, 4]} />)
    await screen.findByRole('combobox', { name: '그룹' })

    await userEvent.selectOptions(screen.getByRole('combobox', { name: '그룹' }), '1')
    await waitFor(() => expect(screen.getByTestId('scope').textContent).toBe('1,2,3'))
    await userEvent.selectOptions(screen.getByRole('combobox', { name: '소그룹' }), '3')
    await waitFor(() => expect(screen.getByTestId('effective').textContent).toBe('3'))

    await userEvent.selectOptions(screen.getByRole('combobox', { name: '그룹' }), '4')
    await waitFor(() => expect(screen.getByTestId('effective').textContent).toBe('4'))
  })

  it('아무것도 안 고르면 전부 든다', async () => {
    installGroups()
    render(<Probe ids={[1, 2, 3, 4, null]} />)
    await screen.findByRole('combobox', { name: '그룹' })
    expect(screen.getByTestId('scope').textContent).toBe('1,2,3,4,')
  })

  it('그 자리에서 소그룹을 만든다 — 고른 그룹 밑으로', async () => {
    // 올리다 말고 라이브러리에 갔다 오게 하지 않는다.
    const made: unknown[] = []
    installGroups(made)
    render(<Probe ids={[]} creatable />)
    await screen.findByRole('combobox', { name: '그룹' })

    await userEvent.selectOptions(screen.getByRole('combobox', { name: '그룹' }), '1')
    await userEvent.selectOptions(screen.getByRole('combobox', { name: '소그룹' }), '__new__')
    await userEvent.type(screen.getByLabelText('새 소그룹 이름'), '재현')
    await userEvent.click(screen.getByRole('button', { name: '만들기' }))

    await waitFor(() => expect(made).toEqual([{ name: '재현', parent_id: 1 }]))
  })
})

describe('groupPath', () => {
  it('소그룹은 "부모 · 자식" — 자식 이름만으로는 어느 실험인지 모른다', () => {
    expect(groupPath('80wt%', '건식 시리즈')).toBe('건식 시리즈 · 80wt%')
  })

  it('최상위 그룹은 제 이름 그대로', () => {
    expect(groupPath('삼성SDI', '')).toBe('삼성SDI')
  })

  it('그룹이 없으면 빈 문자열 — 부르는 쪽이 대시를 고른다', () => {
    expect(groupPath(null, '')).toBe('')
  })
})
