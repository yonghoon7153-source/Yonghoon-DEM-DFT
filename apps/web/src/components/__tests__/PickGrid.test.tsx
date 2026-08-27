/** 고르개 — 한 파일이 여러 줄인 것(SOC 스캔)을 접는 자리.
 *
 *  이 부품이 지켜야 할 것 셋:
 *   1. 접힌 파일은 목록에서 **한 줄**이다.  펴기 전에는 스윕이 안 보인다 —
 *      스물이 그대로 깔리면 고르개가 그 파일 하나로 가득 찬다.
 *   2. 펴면 스윕을 **하나씩** 켤 수 있다.  SOC 별 나이퀴스트는 스윕마다 다른
 *      곡선이고, 그중 셋만 겹쳐 보는 것이 이 화면의 쓰임이다.
 *   3. 스윕이 하나뿐인 파일은 **예전 그대로**다.  접을 것이 없는데 펴는 단추만
 *      하나 더 있으면 손만 늘어난다.
 */

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { useState } from 'react'
import { describe, expect, it } from 'vitest'

import { PickGrid, foldItems, type PickItem } from '../PickGrid'

/** 스캔 한 파일의 스윕들.  `fold.key` 는 파일(sha256)이다. */
function sweeps(sha: string, label: string, count: number, from = 1): PickItem[] {
  return Array.from({ length: count }, (_, i) => ({
    id: from + i,
    name: `#${i + 1}`,
    note: `${(i * 0.5).toFixed(3)} mAh`,
    fold: { key: sha, label, note: '전고체 · SOC 스캔' },
  }))
}

const single: PickItem = { id: 90, name: 'B_bare', note: '액체' }

/** 페이지가 실제로 쓰는 모양: 고른 것은 밖에서 들고 있다. */
function Controlled({ items, limit }: { items: PickItem[]; limit?: number }) {
  const [picked, setPicked] = useState<number[]>([])
  return (
    <PickGrid title="스펙트럼 선택" items={items} picked={picked}
              onChange={setPicked} limit={limit} />
  )
}

const foldBox = () => document.querySelector('.pick-fold') as HTMLElement
const checks = (scope: HTMLElement | Document = document) =>
  [...scope.querySelectorAll<HTMLInputElement>('.pick-item input[type="checkbox"]')]

describe('PickGrid — SOC 스캔 접기', () => {
  it('스윕 여럿인 파일은 한 줄로 접히고, 스윕은 펴야 보인다', async () => {
    render(<Controlled items={[...sweeps('sha-a', 'A_scan', 11), single]} />)

    // 접힌 상태: 파일 한 줄 + 낱장 한 줄 = 체크박스 둘.
    expect(checks()).toHaveLength(2)
    expect(screen.getByText('A_scan')).toBeTruthy()
    expect(screen.getByText(/스윕 11개/)).toBeTruthy()
    expect(screen.queryByText('#7')).toBeNull()

    await userEvent.click(screen.getByRole('button', { name: '스윕 고르기' }))
    expect(screen.getByText('#7')).toBeTruthy()
    // 파일 줄 하나 + 스윕 열하나 + 낱장 하나.
    expect(checks()).toHaveLength(13)
  })

  it('펴서 스윕 하나만 켠다 — 파일 전체가 켜지지 않는다', async () => {
    render(<Controlled items={sweeps('sha-a', 'A_scan', 5)} />)
    await userEvent.click(screen.getByRole('button', { name: '스윕 고르기' }))

    const body = document.querySelector('.pick-fold-body') as HTMLElement
    await userEvent.click(checks(body)[2]!)

    expect(checks(body).filter((box) => box.checked)).toHaveLength(1)
    expect(screen.getByText(/스펙트럼 선택 · 1개/)).toBeTruthy()
    // 파일 줄은 "일부만" 이다 — 켜짐도 꺼짐도 아니다.  세모가 없으면 다섯 중
    // 하나가 다섯 전부로 보인다.
    const head = checks(foldBox())[0]!
    expect(head.checked).toBe(true)
    expect(head.indeterminate).toBe(true)
  })

  it('파일 줄은 스윕 전부를 켜고, 다시 누르면 전부 끈다', async () => {
    render(<Controlled items={sweeps('sha-a', 'A_scan', 5)} />)
    const head = () => checks(foldBox())[0]!

    await userEvent.click(head())
    expect(screen.getByText(/스펙트럼 선택 · 5개/)).toBeTruthy()
    expect(head().indeterminate).toBe(false)

    await userEvent.click(head())
    expect(screen.getByText(/스펙트럼 선택 · 0개/)).toBeTruthy()
  })

  it('상한을 넘겨 켜지 않는다 — 남은 자리만큼만', async () => {
    render(<Controlled items={sweeps('sha-a', 'A_scan', 11)} limit={4} />)

    await userEvent.click(checks(foldBox())[0]!)
    expect(screen.getByText(/스펙트럼 선택 · 4개/)).toBeTruthy()
    expect(screen.getByText('4 / 4')).toBeTruthy()
  })

  it('스윕이 하나뿐인 파일은 접지 않는다 — 펴는 단추가 손만 늘린다', () => {
    render(<Controlled items={[...sweeps('sha-a', 'A_one', 1), single]} />)

    expect(screen.queryByRole('button', { name: '스윕 고르기' })).toBeNull()
    expect(screen.getByText('#1')).toBeTruthy()
    expect(checks()).toHaveLength(2)
  })
})

describe('foldItems', () => {
  it('첫 등장 자리를 지킨다 — 스캔을 목록 끝으로 몰지 않는다', () => {
    const blocks = foldItems([
      ...sweeps('sha-a', 'A_scan', 2, 1),
      single,
      ...sweeps('sha-b', 'B_scan', 2, 50),
    ])
    expect(blocks.map((block) => (block.kind === 'fold' ? block.key : block.item.name)))
      .toEqual(['sha-a', 'B_bare', 'sha-b'])
  })

  it('같은 파일의 스윕이 떨어져 있어도 한 덩어리다', () => {
    const [a1, a2] = sweeps('sha-a', 'A_scan', 2, 1)
    const blocks = foldItems([a1!, single, a2!])
    expect(blocks).toHaveLength(2)
    expect(blocks[0]!.kind === 'fold' && blocks[0]!.items.map((one) => one.id))
      .toEqual([1, 2])
  })
})
