/** 의견 게시판 — 적고, 답하고, 정리하고, 지운다 (ADR 0033). */

import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { FeedbackBell } from '../../components/FeedbackBell'
import { Feedback } from '../Feedback'
import type { FeedbackNote } from '../../lib/types'

function note(over: Partial<FeedbackNote> = {}): FeedbackNote {
  return {
    id: 1,
    created_at: '2026-08-26T09:00:00',
    updated_at: '2026-08-26T09:00:00',
    created_by: '안혁주',
    kind: 'issue',
    body: '클립보드가 **전체**를 복사합니다',
    resolved_at: null,
    resolved_by: '',
    replies: [],
    ...over,
  }
}

let served: FeedbackNote[] = []
const calls: { url: string; init?: RequestInit }[] = []

function installFetch() {
  vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input)
    calls.push({ url, init })
    if (init?.method && init.method !== 'GET') {
      return new Response(null, { status: 204 })
    }
    return new Response(JSON.stringify(served), {
      status: 200, headers: { 'Content-Type': 'application/json' },
    })
  }))
}

beforeEach(() => {
  served = []
  calls.length = 0
  window.localStorage.clear()
  installFetch()
})
afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('의견 게시판', () => {
  it('본문의 마크다운을 그대로 그린다', async () => {
    served = [note()]
    render(<MemoryRouter><Feedback /></MemoryRouter>)
    expect((await screen.findByText('전체')).tagName).toBe('STRONG')
    expect(document.body.textContent).not.toContain('**전체**')
  })

  it('정리된 것도 목록에 남는다 — 아래로 내려갈 뿐', async () => {
    // 같은 불편이 두 달 뒤에 다시 올라올 때 "그때 이렇게 정리했다" 가 보여야 한다.
    served = [
      note({ id: 1, body: '아직 열려 있음' }),
      note({ id: 2, body: '정리된 것', resolved_at: '2026-08-26T10:00:00',
             resolved_by: '안용훈' }),
    ]
    render(<MemoryRouter><Feedback /></MemoryRouter>)
    expect(await screen.findByText('아직 열려 있음')).toBeInTheDocument()
    expect(screen.getByText('정리된 것')).toBeInTheDocument()
    expect(screen.getByText(/열려 있는 것 · 1개/)).toBeInTheDocument()
    expect(screen.getByText(/정리된 것 · 1개/)).toBeInTheDocument()
  })

  it('정리된 항목은 다시 열 수 있다', async () => {
    // 되돌릴 수 없는 버튼은 아무도 안 누른다.
    served = [note({ resolved_at: '2026-08-26T10:00:00' })]
    render(<MemoryRouter><Feedback /></MemoryRouter>)
    await userEvent.click(await screen.findByRole('button', { name: '다시 열기' }))
    const patch = calls.find((c) => c.init?.method === 'PATCH')
    expect(JSON.parse(String(patch?.init?.body))).toEqual({ resolved: false })
  })

  it('댓글만 따로 지운다 — 항목은 남는다', async () => {
    served = [note({
      replies: [{ id: 7, note_id: 1, created_at: '2026-08-26T09:30:00',
                  created_by: '안용훈', body: '고쳤습니다' }],
    })]
    render(<MemoryRouter><Feedback /></MemoryRouter>)
    await userEvent.click(await screen.findByRole('button', { name: '답글 지우기' }))
    const gone = calls.find((c) => c.init?.method === 'DELETE')
    expect(gone?.url).toContain('/api/feedback/1/replies/7')
  })

  it('빈 내용은 올릴 수 없다', async () => {
    render(<MemoryRouter><Feedback /></MemoryRouter>)
    expect(await screen.findByRole('button', { name: '올리기' })).toBeDisabled()
  })
})

describe('상단 막대의 점', () => {
  it('본 적이 없으면 켜진다', async () => {
    served = [note()]
    render(<MemoryRouter><FeedbackBell /></MemoryRouter>)
    expect(await screen.findByLabelText('새 소식 1건')).toBeInTheDocument()
  })

  it('열어 본 뒤에는 꺼진다', async () => {
    served = [note()]
    const board = render(<MemoryRouter><Feedback /></MemoryRouter>)
    // 목록이 도착한 뒤에 읽음이 찍힌다 — 먼저 찍으면 읽는 동안 올라온 것까지
    // 읽은 것이 된다.
    await screen.findByText(/열려 있는 것/)
    await waitFor(() => expect(window.localStorage.getItem('bml.seen.feedback')).toBeTruthy())
    board.unmount()

    render(<MemoryRouter><FeedbackBell /></MemoryRouter>)
    await screen.findByText('의견')
    expect(screen.queryByLabelText(/새 소식/)).not.toBeInTheDocument()
  })
})
