/** 의견 게시판 — 적고, 답하고, 정리하고, 지운다 (ADR 0033). */

import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { FeedbackBell } from '../../components/FeedbackBell'
import { Feedback, wrapSelection } from '../Feedback'
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

describe('F&Q 게시판', () => {
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
      note({ id: 2, body: '이미 고쳤음', resolved_at: '2026-08-26T10:00:00',
             resolved_by: '안용훈' }),
    ]
    render(<MemoryRouter><Feedback /></MemoryRouter>)
    expect(await screen.findByText('아직 열려 있음')).toBeInTheDocument()
    expect(screen.getByText('이미 고쳤음')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: '열려 있는 것' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: '정리된 것' })).toBeInTheDocument()
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
    await screen.findByRole('heading', { name: '열려 있는 것' })
    await waitFor(() => expect(window.localStorage.getItem('bml.seen.feedback')).toBeTruthy())
    board.unmount()

    render(<MemoryRouter><FeedbackBell /></MemoryRouter>)
    await screen.findByText('F&Q')
    expect(screen.queryByLabelText(/새 소식/)).not.toBeInTheDocument()
  })
})

describe('Ctrl+B 로 감싸기', () => {
  it('고른 글자를 감싼다', () => {
    // `**굵게**` 를 손으로 치라고 안내하는 칸은 안 쓰인다.
    expect(wrapSelection('앞가운데뒤', 1, 4, '**')).toEqual({
      value: '앞**가운데**뒤', start: 3, end: 6,
    })
  })

  it('고른 것이 없으면 표시만 넣고 그 사이에 커서를 둔다', () => {
    // 그래야 바로 이어서 칠 수 있다.
    expect(wrapSelection('앞뒤', 1, 1, '`')).toEqual({
      value: '앞``뒤', start: 2, end: 2,
    })
  })

  it('이미 감싸여 있으면 벗긴다', () => {
    // 누르면 켜지고 다시 누르면 꺼진다.
    expect(wrapSelection('앞**가운데**뒤', 3, 6, '**')).toEqual({
      value: '앞가운데뒤', start: 1, end: 4,
    })
  })
})
