import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { blocks, inlineSegments, Markdown } from '../markdown'

describe('inlineSegments', () => {
  it('굵게를 알아본다', () => {
    expect(inlineSegments('앞 **가운데** 뒤')).toEqual([
      { text: '앞 ' },
      { text: '가운데', bold: true },
      { text: ' 뒤' },
    ])
  })

  it('코드 안의 별표는 글자 그대로 남는다', () => {
    // 이 저장소의 기록에는 `**` 를 그대로 보여 주는 자리가 실제로 있다.
    expect(inlineSegments('`**x**` 는 굵게가 아니다')).toEqual([
      { text: '**x**', code: true },
      { text: ' 는 굵게가 아니다' },
    ])
  })

  it('못 알아본 기호는 지우지 않는다', () => {
    // 지우면 사람이 적은 것이 화면에서 사라진다.
    expect(inlineSegments('2 * 3 = 6')).toEqual([{ text: '2 * 3 = 6' }])
  })

  it('굵게 안의 코드도 살린다', () => {
    expect(inlineSegments('**`bml` 을 치세요**')).toEqual([
      { text: 'bml', bold: true, code: true },
      { text: ' 을 치세요', bold: true },
    ])
  })
})

describe('blocks', () => {
  it('들여쓴 표는 따로 둔다', () => {
    // 자릿수가 어긋나면 숫자를 비교할 수 없다 -- 그 표를 적은 이유가 비교인데.
    const body = '앞 문단\n\n    1  2  3\n    4  5  6\n\n뒤 문단'
    expect(blocks(body)).toEqual([
      { kind: 'para', lines: ['앞 문단'] },
      { kind: 'code', lines: ['1  2  3', '4  5  6'] },
      { kind: 'para', lines: ['뒤 문단'] },
    ])
  })

  it('문단 안의 줄바꿈은 한 문단이다', () => {
    expect(blocks('여든 칸에서\n접혔을 뿐이다')).toEqual([
      { kind: 'para', lines: ['여든 칸에서', '접혔을 뿐이다'] },
    ])
  })
})

describe('Markdown', () => {
  it('별표가 화면에 안 보이고 굵게로 나온다', () => {
    render(<Markdown body="**방전 용량이 0.18 % 낮았다**" />)
    expect(screen.getByText('방전 용량이 0.18 % 낮았다').tagName).toBe('STRONG')
    expect(document.body.textContent).not.toContain('**')
  })

  it('표는 고정폭으로 그대로 나온다', () => {
    const { container } = render(<Markdown body={'앞\n\n    a  b\n    c  d'} />)
    expect(container.querySelector('pre')?.textContent).toBe('a  b\nc  d')
  })
})
