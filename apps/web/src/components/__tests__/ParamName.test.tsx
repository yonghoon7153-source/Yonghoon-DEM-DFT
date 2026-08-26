/** 문장 속 파라미터 이름도 표와 같은 모습이어야 한다.
 *
 *  표만 첨자로 바꾸면 같은 것이 한 화면에서 두 모습으로 나오고, 읽는 사람은
 *  그것을 다른 것으로 본다.
 */

import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { ParamName, ParamText } from '../ParamName'

const NAMES = ['L1', 'R0', 'CPE1_n', 'TL1_W', 'TL1_Wn', 'TL1_Wt', 'TL1_Ri', 'TL1_Re']

describe('ParamName', () => {
  it('번호와 접미사가 첨자로 간다', () => {
    const { container } = render(<ParamName name="CPE1_Q" />)
    expect(container.textContent).toBe('CPE1,Q')
    expect(container.querySelector('sub')?.textContent).toBe('1,Q')
  })

  it('쪼갤 것이 없으면 그대로 둔다', () => {
    const { container } = render(<ParamName name="Rct" />)
    expect(container.querySelector('sub')).toBeNull()
  })
})

describe('ParamText', () => {
  it('문장 속의 아는 이름만 바꾼다', () => {
    const { container } = render(
      <ParamText names={NAMES}
                 text="물리적 한계에 붙은 파라미터: CPE1_n, TL1_Wn, TL1_Wt" />,
    )
    // 글자는 그대로 읽히고 (첨자는 모양일 뿐),
    expect(container.textContent)
      .toBe('물리적 한계에 붙은 파라미터: CPE1,n, TL1,Wn, TL1,Wt')
    // 셋 다 첨자가 붙었다.
    expect(container.querySelectorAll('sub')).toHaveLength(3)
  })

  it('긴 이름이 먼저다 — TL1_W 가 TL1_Wn 을 잘라먹지 않는다', () => {
    const { container } = render(<ParamText names={NAMES} text="TL1_Wn 을 보세요" />)
    expect(container.querySelectorAll('sub')).toHaveLength(1)
    expect(container.querySelector('sub')?.textContent).toBe('1,Wn')
  })

  it('모르는 이름은 안 건드린다 — 회로 문자열을 망가뜨리지 않는다', () => {
    // 같은 문장에 `L1-R0-p(R1,CPE1)-TL1` 이 섞여 있다.  이름처럼 생긴 조각을
    // 정규식으로 고르면 사람이 회로 칸에 쳐 넣어야 하는 글자가 잘린다.
    render(<ParamText names={['Rct']} text="회로 L1-R0-p(R1,CPE1)-TL1 을 씁니다" />)
    expect(screen.getByText('회로 L1-R0-p(R1,CPE1)-TL1 을 씁니다')).toBeInTheDocument()
  })

  it('이름 목록이 비면 문장을 그대로 낸다', () => {
    render(<ParamText names={[]} text="아무 일도 없습니다" />)
    expect(screen.getByText('아무 일도 없습니다')).toBeInTheDocument()
  })
})
