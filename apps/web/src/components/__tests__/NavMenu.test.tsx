/** 상단 메뉴 — 섹션이 셋이 되면서 한 줄에 늘어놓을 수 없게 된 것. */

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { describe, expect, it } from 'vitest'

import { NavMenu, isUnder, type NavSection } from '../NavMenu'

const CYCLING: NavSection = {
  label: '충방전 프로파일 · 사이클',
  links: [
    { to: '/dashboard', label: '대시보드' },
    { to: '/samples', label: '셀 라이브러리' },
    { to: '/compare', label: '비교' },
    { to: '/upload', label: '업로드' },
  ],
}

const GITT: NavSection = {
  label: 'GITT',
  links: [{ to: '/gitt', label: '확산계수 · pseudo-OCV', soon: true }],
}

function renderMenu(section: NavSection, at = '/dashboard') {
  return render(
    <MemoryRouter initialEntries={[at]}>
      <Routes>
        <Route path="*" element={<NavMenu section={section} />} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('상단 메뉴', () => {
  it('접혀 있다가 눌러야 펴진다', async () => {
    renderMenu(CYCLING)
    expect(screen.queryByRole('menuitem', { name: '대시보드' })).toBeNull()

    await userEvent.click(screen.getByRole('button', { name: /충방전/ }))
    for (const label of ['대시보드', '셀 라이브러리', '비교', '업로드']) {
      expect(screen.getByRole('menuitem', { name: label })).toBeInTheDocument()
    }
  })

  it('링크를 고르면 닫힌다 — 안 닫으면 새 화면의 절반을 가린다', async () => {
    renderMenu(CYCLING)
    await userEvent.click(screen.getByRole('button', { name: /충방전/ }))
    await userEvent.click(screen.getByRole('menuitem', { name: '비교' }))
    expect(screen.queryByRole('menuitem', { name: '비교' })).toBeNull()
  })

  it('Escape 로 닫힌다', async () => {
    renderMenu(CYCLING)
    await userEvent.click(screen.getByRole('button', { name: /충방전/ }))
    await userEvent.keyboard('{Escape}')
    expect(screen.queryByRole('menuitem', { name: '대시보드' })).toBeNull()
  })

  it('지금 있는 화면의 섹션이 표시된다 — 접혀 있어도 어디인지 보인다', () => {
    renderMenu(CYCLING, '/samples/12')
    expect(screen.getByRole('button', { name: /충방전/ })).toHaveClass('active')
  })

  it('아직 없는 화면은 눌리지 않되 보인다', async () => {
    renderMenu(GITT, '/dashboard')
    await userEvent.click(screen.getByRole('button', { name: 'GITT' }))
    const item = screen.getByRole('menuitem', { name: /확산계수/ })
    expect(item).toHaveAttribute('aria-disabled', 'true')
    expect(item.tagName).not.toBe('A')
  })
})

describe('isUnder', () => {
  it('상세 화면도 그 섹션 안이다', () => {
    expect(isUnder('/eis/12', '/eis')).toBe(true)
    expect(isUnder('/eis', '/eis')).toBe(true)
  })

  it('앞부분만 같은 다른 경로는 아니다', () => {
    // `/sample` 이 `/samples` 를 삼키면 엉뚱한 섹션이 켜진 것처럼 보인다.
    expect(isUnder('/samples', '/sample')).toBe(false)
  })
})
