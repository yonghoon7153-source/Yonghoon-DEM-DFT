/** 사람이 한 줄에 적은 SOC 를 읽는 자리 (ADR 0038).
 *
 *  이 파서가 조용히 틀리면 SOC 축이 한 칸씩 밀린 채로 그림이 멀쩡해 보인다 —
 *  그래서 "못 읽은 것" 을 삼키지 않는 것이 여기서 제일 중요한 성질이다.
 */

import { describe, expect, it } from 'vitest'

import { parseSocList, socLabel, socProblem } from '../soc'

describe('parseSocList', () => {
  it('노트에 적는 모양 그대로 읽는다', () => {
    expect(parseSocList('SOC 0, 10, 20').values).toEqual([0, 10, 20])
    expect(parseSocList('0 10 20').values).toEqual([0, 10, 20])
    expect(parseSocList('0%, 10%, 20%').values).toEqual([0, 10, 20])
    // 엑셀에서 세로로 복사해 오면 줄바꿈이다.
    expect(parseSocList('0\n10\n20\n').values).toEqual([0, 10, 20])
  })

  it('소수점과 음수 표기도 그대로 읽는다 (판정은 따로 한다)', () => {
    expect(parseSocList('2.5, 97.5').values).toEqual([2.5, 97.5])
    expect(parseSocList('-5').values).toEqual([-5])
  })

  //: 모르는 스윕 하나 때문에 전부를 못 적게 하면 안 된다.
  it('빈 자리는 null — 지우는 길이자 모른다고 적는 길이다', () => {
    expect(parseSocList('0, -, 20').values).toEqual([0, null, 20])
    expect(parseSocList('0, ?, 20').values).toEqual([0, null, 20])
  })

  //: 여기가 이 파일의 이유다.  조용히 버리면 열둘을 적었는데 열하나가
  //  저장되고, 그 SOC 축은 한 칸 밀린 채로 멀쩡해 보인다.
  it('숫자가 아닌 것은 삼키지 않고 돌려준다', () => {
    const list = parseSocList('0, 열, 20')
    expect(list.values).toEqual([0, 20])
    expect(list.bad).toEqual(['열'])
  })

  it('빈 글은 빈 목록', () => {
    expect(parseSocList('').values).toEqual([])
    expect(parseSocList('   \n  ').values).toEqual([])
  })
})

describe('socProblem', () => {
  it('수가 맞고 범위 안이면 아무 말도 안 한다', () => {
    expect(socProblem(parseSocList('0, 50, 100'), 3)).toBe('')
  })

  it('수가 다르면 두 수를 함께 적는다', () => {
    const said = socProblem(parseSocList('0, 50'), 12)
    expect(said).toContain('12')
    expect(said).toContain('2')
  })

  it('못 읽은 것이 있으면 그것부터 말한다', () => {
    expect(socProblem(parseSocList('0, 열, 20'), 3)).toContain('열')
  })

  it('0~100 밖은 막는다', () => {
    expect(socProblem(parseSocList('0, 50, 120'), 3)).toContain('120')
    expect(socProblem(parseSocList('-1, 50, 100'), 3)).toContain('-1')
  })

  //: 빈 칸은 잘못이 아니다 — 아직 안 적은 것이다.
  it('빈 목록은 잘못이 아니다', () => {
    expect(socProblem(parseSocList(''), 12)).toBe('')
  })

  it('null 이 섞여 있어도 수만 맞으면 된다', () => {
    expect(socProblem(parseSocList('0, -, 100'), 3)).toBe('')
  })
})

describe('socLabel', () => {
  it('없으면 빈 문자열 — 0% 로 적지 않는다', () => {
    expect(socLabel(null)).toBe('')
    expect(socLabel(undefined)).toBe('')
  })

  it('0 은 값이다', () => {
    expect(socLabel(0)).toBe('SOC 0%')
  })
})
