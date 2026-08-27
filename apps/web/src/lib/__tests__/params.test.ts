/** 파라미터 이름 → 사람 말, 그리고 무엇을 강조할지.
 *
 *  표의 '뜻' 칸이 열세 줄 중 두 줄만 채워져 있었다 — 읽는 사람에게는
 *  "모르는 것이 열한 개" 로 보인다.
 */

import { describe, expect, it } from 'vitest'

import { isHeadline, paramMeaning } from '../params'

describe('파라미터 뜻', () => {
  it('전송선 안쪽까지 이름이 있다 — 여기가 전부 비어 있었다', () => {
    expect(paramMeaning('TL1_Ri')).toContain('이온')
    expect(paramMeaning('TL1_Re')).toContain('전자')
    expect(paramMeaning('TL1_Rct')).toContain('전하이동')
    expect(paramMeaning('TL1_Wn')).toContain('확산')
    expect(paramMeaning('TL1_Wt')).toContain('시간')
  })

  it('접미사 규칙이라 원소 이름을 가리지 않는다', () => {
    // `Ws2_R` 도 `TL1_Wr` 도 같은 것을 뜻한다.
    expect(paramMeaning('Ws2_R')).toContain('확산 저항')
    expect(paramMeaning('TL1_Wr')).toContain('확산 저항')
    expect(paramMeaning('CPE1_n')).toContain('지수')
    expect(paramMeaning('CPE9_Q')).toContain('CPE')
    expect(paramMeaning('L1')).toContain('배선')
  })

  it('R0 는 아크가 아니라 절편이라 따로 말한다', () => {
    expect(paramMeaning('R0')).toContain('절편')
    expect(paramMeaning('R1')).toContain('반원')
  })

  it('모르는 이름에는 아무 말도 안 붙인다 — 지어내지 않는다', () => {
    expect(paramMeaning('Zed7_frobnicate')).toBe('')
  })
})

describe('무엇을 강조하는가', () => {
  it('보고서에 옮겨 적는 값은 저항이다', () => {
    expect(isHeadline('R0')).toBe(true)
    expect(isHeadline('R2')).toBe(true)
    expect(isHeadline('TL1_Rct')).toBe(true)
    expect(isHeadline('TL1_Ri')).toBe(true)
    expect(isHeadline('Ws1_R')).toBe(true)
  })

  it('모양을 정하는 값과 배선은 강조하지 않는다 — 전부 강조하면 강조가 아니다', () => {
    expect(isHeadline('CPE1_n')).toBe(false)
    expect(isHeadline('CPE1_Q')).toBe(false)
    expect(isHeadline('TL1_Wn')).toBe(false)
    expect(isHeadline('TL1_Wt')).toBe(false)
    expect(isHeadline('L1')).toBe(false)
  })
})

describe('면적으로 나눠도 되는 파라미터', () => {
  it('Ω 인 것만 — 나머지는 나누면 뜻 없는 수가 된다', async () => {
    const { isOhmParam } = await import('../params')
    for (const name of ['R0', 'R12', 'TL1_Rct', 'TL1_Ri', 'TL1_Re',
                        'TL1_Wr', 'Ws4_R']) {
      expect(isOhmParam(name)).toBe(true)
    }
    // `_Q` 는 S·sⁿ 이라 오히려 곱해야 하고, 지수는 무차원, `_tau`·`_Wt` 는 초다.
    for (const name of ['CPE1_Q', 'CPE1_n', 'TL1_Wn', 'TL1_Wt', 'Ws4_tau', 'L1']) {
      expect(isOhmParam(name)).toBe(false)
    }
  })
})
