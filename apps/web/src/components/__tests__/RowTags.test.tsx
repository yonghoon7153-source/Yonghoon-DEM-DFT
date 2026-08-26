import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { GroupTag, OwnerTag, leafOf } from '../RowTags'

describe('leafOf', () => {
  it('"부모 · 자식" 에서 잎만 — 칩은 12ch 라 부모를 넣으면 잎이 잘린다', () => {
    expect(leafOf('건식전극 · 50kg 1um')).toBe('50kg 1um')
  })

  it('부모가 없으면 그대로', () => {
    expect(leafOf('건식전극')).toBe('건식전극')
  })

  it('없으면 빈 문자열 — 빈 이름표를 그리지 않게', () => {
    expect(leafOf('')).toBe('')
    expect(leafOf(undefined)).toBe('')
    expect(leafOf(null)).toBe('')
  })
})

describe('GroupTag · OwnerTag', () => {
  it('그룹이 없으면 아무것도 안 그린다 — 빈 칩은 "이름 없는 그룹" 으로 읽힌다', () => {
    const { container } = render(<><GroupTag name="" /><OwnerTag owner="" /></>)
    expect(container.querySelector('.group-tag')).toBeNull()
    expect(container.querySelector('.owner-tag')).toBeNull()
  })

  it('전체 길은 마우스로 돌린다 — 칩에는 잎만 적는다', () => {
    render(<GroupTag name="50kg 1um" path="건식전극 · 50kg 1um" />)
    const tag = screen.getByText('50kg 1um')
    expect(tag.getAttribute('title')).toBe('그룹: 건식전극 · 50kg 1um')
  })

  it('경로를 안 주면 이름이 곧 경로다', () => {
    render(<GroupTag name="건식전극" />)
    expect(screen.getByText('건식전극').getAttribute('title')).toBe('그룹: 건식전극')
  })

  it('올린 사람은 테두리만 있는 이름표', () => {
    render(<OwnerTag owner="안용훈" />)
    const tag = screen.getByText('안용훈')
    expect(tag.className).toBe('owner-tag')
    expect(tag.getAttribute('title')).toBe('올린 사람: 안용훈')
  })
})
