/** 셀 고르기 창 — **어디에 그려지는가**.
 *
 *  이 창은 표 칸(`<td>`) 안에서 열린다.  `position: fixed` 는 화면 기준처럼
 *  보이지만, 조상 중에 `transform`·`filter`·`opacity < 1` 이 하나라도 있으면
 *  그 조상이 기준이 되고 쌓임 순서도 그 안에 갇힌다.
 *
 *  실제로 그렇게 됐다: `.dim` 에 `opacity: 0.45` 가 들어가 있었고 관계셀 칸이
 *  `<td class="text dim">` 이라, 창이 반투명해진 채 붙박이 표 머리 **아래**로
 *  깔렸다.  그 규칙은 지웠지만 (`stylesheet.test.ts` 가 다시 못 들어오게
 *  막는다), 창이 남의 DOM 안에 있는 한 같은 사고는 언제든 다시 난다.
 *
 *  그래서 창은 `document.body` 로 옮겨 그린다.  조상이 아예 없으면 조상이
 *  기준이 될 수도 없다.
 */

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { CellPicker } from '../CellPicker'
import type { Sample } from '../../lib/types'

function sample(id: number, name: string): Sample {
  return {
    id,
    name,
    group_id: null,
    group_name: '',
    group_parent_name: '',
    cathode_type: '',
    cathode_detail: '',
    created_at: '2026-08-26T10:00:00',
    updated_at: '2026-08-26T10:00:00',
    run_count: 1,
  } as Sample
}

function renderInACell() {
  return render(
    <MemoryRouter>
      <table>
        <tbody>
          <tr>
            {/* 진짜 화면과 같은 자리.  `dim` 이 문제였던 그 칸이다. */}
            <td className="text dim">
              <CellPicker
                value={null}
                samples={[sample(1, '4.4V_cell29'), sample(2, '4.2V_cell33')]}
                label="Dcell39 관계셀"
                onPick={() => {}}
              />
            </td>
          </tr>
        </tbody>
      </table>
    </MemoryRouter>,
  )
}

afterEach(() => vi.restoreAllMocks())

describe('셀 고르기 창', () => {
  it('표 칸이 아니라 body 에 그려진다 — 조상이 있으면 화면 맨 위로 못 올라간다',
     async () => {
    renderInACell()
    await userEvent.click(screen.getByRole('button', { name: 'Dcell39 관계셀' }))

    const dialog = await screen.findByRole('dialog', { name: 'Dcell39 관계셀 고르기' })
    const backdrop = dialog.parentElement!
    expect(backdrop.className).toBe('modal-backdrop')
    expect(backdrop.parentElement).toBe(document.body)
    // 표 안에는 아무것도 안 남는다 -- 반쯤 남으면 그것이 곧 옛 사고다.
    expect(document.querySelector('td .modal-backdrop')).toBeNull()
  })

  it('창 밖을 누르면 닫히고, 안을 누르면 안 닫힌다', async () => {
    renderInACell()
    await userEvent.click(screen.getByRole('button', { name: 'Dcell39 관계셀' }))

    const dialog = await screen.findByRole('dialog', { name: 'Dcell39 관계셀 고르기' })
    // 목록을 훑다 여백을 스치는 것이 창을 닫는 동작이 되면 고른 것을 잃는다.
    await userEvent.click(dialog)
    expect(screen.queryByRole('dialog')).not.toBeNull()

    await userEvent.click(dialog.parentElement!)
    expect(screen.queryByRole('dialog')).toBeNull()
  })
})
