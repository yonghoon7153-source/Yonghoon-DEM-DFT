/** 한 줄에 적은 수들을 스윕 차례로 — 그리고 `(처음, 끝, 개수)` 축약. */

import { describe, expect, it } from 'vitest'

import { describeValues, listProblem, parseValueList } from '../valuelist'

describe('목록 읽기', () => {
  it('쉼표·공백·줄바꿈 아무것으로나 나눈다', () => {
    expect(parseValueList('60, 50, 40').values).toEqual([60, 50, 40])
    expect(parseValueList('60 50 40').values).toEqual([60, 50, 40])
    expect(parseValueList('60\n50\n40').values).toEqual([60, 50, 40])
    expect(parseValueList(' 60;50 ;40 ').values).toEqual([60, 50, 40])
  })

  it('음수와 소수를 읽는다 — 온도는 영하로 간다', () => {
    expect(parseValueList('60, 0, -20, -0.5').values).toEqual([60, 0, -20, -0.5])
  })

  it('빈 자리는 null 이다 — 모르는 스윕 하나가 전부를 막지 않는다', () => {
    expect(parseValueList('60, -, 40, ?').values).toEqual([60, null, 40, null])
  })

  it('숫자가 아닌 것은 삼키지 않고 돌려준다', () => {
    const list = parseValueList('60, 어제, 40')
    expect(list.values).toEqual([60, 40])
    expect(list.bad).toEqual(['어제'])
  })

  it('이름표와 단위는 값이 아니다', () => {
    const list = parseValueList('SOC 0, 50%, 100%',
                               { label: /^soc$/i, unit: /%$/ })
    expect(list.values).toEqual([0, 50, 100])
    expect(list.bad).toEqual([])
  })
})

describe('(처음, 끝, 개수) 축약', () => {
  it('내려가는 온도 아홉 점을 펼친다', () => {
    const list = parseValueList('(60, -20, 9)')
    expect(list.values).toEqual([60, 50, 40, 30, 20, 10, 0, -10, -20])
    expect(list.expanded).toBe(true)
  })

  it('쓴 방향을 지킨다 — 올라가게 쓰면 올라간다', () => {
    expect(parseValueList('(-20, 60, 9)').values)
      .toEqual([-20, -10, 0, 10, 20, 30, 40, 50, 60])
  })

  it('공백으로 나눠 써도 되고 괄호 안 공백도 봐준다', () => {
    expect(parseValueList('( 60 -20 9 )').values)
      .toEqual([60, 50, 40, 30, 20, 10, 0, -10, -20])
  })

  //: 이것이 괄호를 요구하는 이유다.  `60, 40, 3` 을 범위로 읽으면 세 값을
  //  적은 사람이 60·50·40 을 얻는다 — 우연히 그럴듯해서 더 나쁘다.
  it('괄호가 없으면 그냥 목록이다', () => {
    expect(parseValueList('60, 40, 3').values).toEqual([60, 40, 3])
    expect(parseValueList('60, 40, 3').expanded).toBe(false)
  })

  it('부동소수점 찌꺼기를 남기지 않는다', () => {
    expect(parseValueList('(0, 0.3, 4)').values).toEqual([0, 0.1, 0.2, 0.3])
  })

  it('개수가 1 이면 한 점, 0 이면 읽을 수 없다', () => {
    expect(parseValueList('(60, -20, 1)').values).toEqual([60])
    expect(parseValueList('(60, -20, 0)').bad).toEqual(['(60, -20, 0)'])
  })
})

describe('적을 수 있는가', () => {
  const list = (text: string) => parseValueList(text)

  it('개수가 다르면 두 수를 함께 말한다', () => {
    const problem = listProblem(list('60, 40'), 9, '온도')
    expect(problem).toContain('9')
    expect(problem).toContain('2')
  })

  it('빈 입력은 문제가 아니다 — 아직 안 적은 것이다', () => {
    expect(listProblem(list(''), 9, '온도')).toBe('')
  })

  it('범위를 주면 벗어난 값을 짚는다', () => {
    const problem = listProblem(list('0, 50, 120'), 3, 'SOC',
                                { low: 0, high: 100, unit: '%' })
    expect(problem).toContain('120')
  })

  it('숫자로 못 읽은 것이 있으면 그것부터 말한다', () => {
    expect(listProblem(list('60, 어제, 40'), 3, '온도')).toContain('어제')
  })
})

describe('되읽어 주기', () => {
  it('짧으면 그대로, 길면 줄여서 개수를 적는다', () => {
    expect(describeValues([60, 50, 40], '°C')).toBe('60, 50, 40 °C')
    expect(describeValues([60, null, 40], '°C')).toBe('60, —, 40 °C')
    const many = Array.from({ length: 20 }, (_, i) => i)
    expect(describeValues(many)).toContain('(20개)')
  })
})
