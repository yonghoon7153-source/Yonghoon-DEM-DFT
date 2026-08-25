/** Origin 으로 옮기는 버튼 — 빈 클립보드로 성공한 척하지 않는가. */

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { CopyBar } from '../CopyBar'

function stubClipboard() {
  const written: string[] = []
  vi.stubGlobal('navigator', {
    ...navigator,
    clipboard: { writeText: async (text: string) => { written.push(text) } },
  })
  vi.stubGlobal('isSecureContext', true)
  Object.defineProperty(window, 'isSecureContext', { value: true, configurable: true })
  return written
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('CopyBar', () => {
  it('누른 것을 복사하고 눌렀다고 표시한다', async () => {
    const written = stubClipboard()
    render(<CopyBar items={[{ label: '나이퀴스트', build: () => '1\t2' }]} />)

    await userEvent.click(screen.getByRole('button', { name: '나이퀴스트 복사' }))
    expect(written).toEqual(['1\t2'])
    expect(await screen.findByText('복사됨 ✓')).toBeInTheDocument()
  })

  it('복사할 것이 없으면 말한다 — 빈 클립보드는 붙여 넣기 전까지 티가 안 난다', async () => {
    stubClipboard()
    render(<CopyBar items={[{ label: 'pOCV', build: () => '' }]} />)

    await userEvent.click(screen.getByRole('button', { name: 'pOCV 복사' }))
    expect(await screen.findByText('복사할 pOCV 데이터가 없습니다')).toBeInTheDocument()
  })

  it('뺀 점이 있으면 몇 개인지 말한다', async () => {
    stubClipboard()
    render(<CopyBar items={[{
      label: '확산계수',
      build: () => '0.5\t1e-6',
      skipped: 3,
      skippedNote: (n) => `가정을 통과하지 못한 펄스 ${n}개는 뺐습니다`,
    }]} />)

    await userEvent.click(screen.getByRole('button', { name: '확산계수 복사' }))
    expect(await screen.findByText(/펄스 3개는 뺐습니다/)).toBeInTheDocument()
  })

  it('누를 수 없는 버튼은 눌리지 않는다', async () => {
    stubClipboard()
    render(<CopyBar items={[{ label: '보드', build: () => 'x', disabled: true }]} />)
    expect(screen.getByRole('button', { name: '보드 복사' })).toBeDisabled()
  })
})
