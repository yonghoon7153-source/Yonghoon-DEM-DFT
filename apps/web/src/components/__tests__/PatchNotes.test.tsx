/** 패치노트 — 무엇이 바뀌었나.
 *
 * 두 사람이 각자 고치고 `bml` 이 조용히 pull 하므로, 화면이 어제와 달라도
 * 무엇이 달라졌는지 알 길이 없었다.  그 답을 `docs/log.md` 에서 그대로 가져온다.
 *
 * 여기서 틀릴 수 있는 방식: 접혀 있을 때 아무 내용도 안 보여 "뭔가 바뀌었다"
 * 스무 줄이 되거나, 모르는 action 이 화면에서 사라지거나, 펼쳤을 때 문단이
 * 뭉개지거나.
 */

import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { firstParagraph, noteDate, PatchNotes } from '../PatchNotes'
import type { ChangeNote } from '../../lib/types'

function note(overrides: Partial<ChangeNote> = {}): ChangeNote {
  return {
    date: '2026-08-24',
    action: 'fix',
    subject: '포트 주인을 밝힌다',
    body: '증상은 이랬다.\n\n그래서 이렇게 고쳤다.',
    ...overrides,
  }
}

function installFetch(rows: ChangeNote[] | Error) {
  vi.stubGlobal(
    'fetch',
    vi.fn(async () => {
      if (rows instanceof Error) {
        return { ok: false, status: 500, statusText: 'Error', json: async () => ({ detail: 'x' }) }
      }
      return { ok: true, status: 200, statusText: 'OK', json: async () => rows }
    }),
  )
}

afterEach(() => vi.unstubAllGlobals())

describe('noteDate', () => {
  const today = new Date('2026-08-24T00:00:00Z')

  it('같은 해면 연도를 뺀다', () => {
    // 스무 줄에 2026 이 스무 번 적히면 정작 다른 부분인 날짜가 안 읽힌다.
    expect(noteDate('2026-08-24', today)).toBe('8월 24일')
  })

  it('다른 해면 연도를 붙인다 — 그때는 그것이 다른 부분이다', () => {
    expect(noteDate('2025-12-01', today)).toBe('2025. 12월 1일')
  })

  it('모양이 다르면 그대로 둔다 — 날짜를 지어내지 않는다', () => {
    expect(noteDate('언젠가', today)).toBe('언젠가')
  })
})

describe('firstParagraph', () => {
  it('문단으로 자른다, 문장으로 자르지 않는다', () => {
    // 이 기록의 첫 문단은 대개 "무엇이 잘못돼 있었는가" 한 덩어리다.  첫 문장만
    // 떼면 증상만 남고 이유가 잘린다.
    expect(firstParagraph('증상이 이랬다. 원인은 이것이었다.\n\n그래서 고쳤다.')).toBe(
      '증상이 이랬다. 원인은 이것이었다.',
    )
  })

  it('문단 안의 줄바꿈은 한 줄로 편다', () => {
    expect(firstParagraph('한 문단이\n두 줄로 적혀 있다.\n\n다음.')).toBe(
      '한 문단이 두 줄로 적혀 있다.',
    )
  })

  it('본문이 없으면 빈 문자열', () => {
    expect(firstParagraph('')).toBe('')
  })
})

describe('패치노트', () => {
  it('제목과 요약 한 줄을 함께 보여 준다', async () => {
    // 제목만 스무 개면 무엇이 바뀌었는지가 아니라 "뭔가 바뀌었다" 만 읽힌다.
    installFetch([note()])
    render(<PatchNotes />)
    expect(await screen.findByText('포트 주인을 밝힌다')).toBeInTheDocument()
    expect(screen.getByText('증상은 이랬다.')).toBeInTheDocument()
  })

  it('자세히를 누르면 본문 전체가 나온다', async () => {
    installFetch([note()])
    render(<PatchNotes />)
    await userEvent.click(await screen.findByRole('button', { name: '자세히' }))
    expect(screen.getByText(/그래서 이렇게 고쳤다\./)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: '접기' })).toBeInTheDocument()
  })

  it('모르는 action 도 이름 그대로 나온다 — 항목이 사라지지 않는다', async () => {
    // docs/SCHEMA.md 는 일곱 개를 적어 뒀는데 파일에는 feat 도 docs 도 있다.
    // 아는 것만 그리면 그 커밋만 패치노트에서 조용히 빠진다.
    installFetch([note({ action: 'refactor', subject: '이름을 바꿨다' })])
    render(<PatchNotes />)
    expect(await screen.findByText('이름을 바꿨다')).toBeInTheDocument()
    expect(screen.getByText('refactor')).toBeInTheDocument()
  })

  it('아는 action 은 우리말 이름표를 단다', async () => {
    installFetch([note({ action: 'feat' })])
    render(<PatchNotes />)
    expect(await screen.findByText('새 기능')).toBeInTheDocument()
  })

  it('본문이 없는 항목에는 자세히 버튼이 없다', async () => {
    // 눌러도 아무것도 안 나오는 버튼은 고장 난 것으로 읽힌다.
    installFetch([note({ body: '' })])
    render(<PatchNotes />)
    expect(await screen.findByText('포트 주인을 밝힌다')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: '자세히' })).toBeNull()
  })

  it('읽지 못하면 그렇게 말한다 — 빈 목록인 척하지 않는다', async () => {
    installFetch(new Error('nope'))
    render(<PatchNotes />)
    expect(await screen.findByText('패치노트를 읽지 못했습니다.')).toBeInTheDocument()
  })

  it('기록이 없으면 없다고 한다', async () => {
    installFetch([])
    render(<PatchNotes />)
    await waitFor(() => expect(screen.getByText('아직 기록이 없습니다.')).toBeInTheDocument())
  })

  it('한 항목을 펼치면 다른 항목은 접힌다', async () => {
    installFetch([note({ subject: '첫째' }), note({ subject: '둘째' })])
    render(<PatchNotes />)
    const buttons = await screen.findAllByRole('button', { name: '자세히' })
    await userEvent.click(buttons[0]!)
    expect(screen.getAllByRole('button', { name: '자세히' })).toHaveLength(1)
    await userEvent.click(screen.getByRole('button', { name: '자세히' }))
    expect(screen.getAllByRole('button', { name: '자세히' })).toHaveLength(1)
  })
})
