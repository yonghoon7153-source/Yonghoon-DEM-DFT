/** 글자 자리 어림 — 3D 축 글자가 겹치는 것을 그리기 전에 알아내는 자.
 *
 *  어림이므로 **실측에 묶어 둔다.**  아래 폭은 Chromium 에서 실제로 잰 값이다
 *  (11 px, system-ui, 같은 문자열).  어림이 실측보다 좁아지면 겹친 것을 못 보고
 *  그대로 찍으므로, 그 방향으로 틀어지는 변경을 여기서 잡는다.
 */

import { describe, expect, it } from 'vitest'

import { labelBox, overlaps, placeLabels, textWidth } from '../labelbox'

/** Chromium 실측 (font: 11px system-ui). */
const MEASURED: [string, number][] = [
  ['-6.00', 28.5],
  ['0', 7],
  ['50.0', 24.5],
  ['100', 21],
  ['Dcell12_4_C06', 81.1],
  ['Dcell12_4_4V_after_cycle_long_name', 205.5],
  ['Dcell12_4_3V', 74.4],
  ['스펙트럼', 44],
]

describe('textWidth', () => {
  it.each(MEASURED)('%s 는 실측 %d px 언저리', (text, real) => {
    const guess = textWidth(text, 11)
    expect(guess).toBeGreaterThan(real * 0.85)
    expect(guess).toBeLessThan(real * 1.2)
  })

  it('한글은 한 칸을 다 쓴다', () => {
    expect(textWidth('스펙트럼', 11)).toBe(44)
    expect(textWidth('전위', 10)).toBe(20)
  })

  it('빈 글자는 폭이 0', () => {
    expect(textWidth('', 11)).toBe(0)
  })
})

describe('labelBox', () => {
  //: `y` 는 밑줄이다.  상자를 밑줄 아래로 잡으면 눈금 글자가 실제로는 위에
  //  있는데 아래를 비교하게 되어, 겹침 판정이 통째로 어긋난다.
  it('밑줄 위로 상자를 세운다', () => {
    const box = labelBox({ x: 100, y: 200 }, '0', 11)
    expect(box.y).toBeLessThan(200)
    expect(box.y + box.h).toBeGreaterThan(200)
  })

  it('가운데 맞춤은 좌우로 반씩', () => {
    const box = labelBox({ x: 100, y: 50 }, '100', 11, 'middle')
    expect(box.x + box.w / 2).toBeCloseTo(100, 6)
  })

  it('오른쪽 맞춤은 왼쪽으로만 뻗는다 (세로축 눈금)', () => {
    const box = labelBox({ x: 100, y: 50 }, '100', 11, 'end')
    expect(box.x + box.w).toBeCloseTo(100, 6)
  })

  it('왼쪽 맞춤은 오른쪽으로만', () => {
    expect(labelBox({ x: 100, y: 50 }, '100', 11, 'start').x).toBe(100)
  })
})

describe('overlaps', () => {
  const at = (x: number, y: number) => ({ x, y, w: 10, h: 10 })

  it('떨어져 있으면 안 겹친다', () => {
    expect(overlaps(at(0, 0), at(20, 0))).toBe(false)
    expect(overlaps(at(0, 0), at(0, 20))).toBe(false)
  })

  it('맞닿은 것은 겹친 것이 아니다', () => {
    expect(overlaps(at(0, 0), at(10, 0))).toBe(false)
  })

  it('여유(pad)를 주면 닿기 직전도 겹친 것으로 본다', () => {
    expect(overlaps(at(0, 0), at(12, 0), 3)).toBe(true)
    expect(overlaps(at(0, 0), at(20, 0), 3)).toBe(false)
  })

  it('한 귀퉁이만 걸쳐도 겹침', () => {
    expect(overlaps(at(0, 0), at(9, 9))).toBe(true)
  })
})

describe('placeLabels', () => {
  const box = (x: number) => ({ x, y: 0, w: 10, h: 10 })

  it('먼저 온 것이 자리를 갖고, 겹친 뒤엣것은 빠진다', () => {
    const kept = placeLabels([
      { key: 'a', box: box(0) },
      { key: 'b', box: box(5) },
      { key: 'c', box: box(40) },
    ])
    expect([...kept]).toEqual(['a', 'c'])
  })

  //: 축 이름은 빠지면 그 축이 무엇인지 화면 어디에도 없다.
  it('keep 인 것은 겹쳐도 안 뺀다', () => {
    const kept = placeLabels([
      { key: 'tick', box: box(0) },
      { key: 'title', box: box(5), keep: true },
    ])
    expect(kept.has('title')).toBe(true)
  })

  //: keep 이 자리를 안 차지하면 뒤에 오는 눈금이 축 이름 위에 그대로 찍힌다.
  it('keep 도 자리는 차지한다 — 뒤에 오는 눈금이 그것을 피한다', () => {
    const kept = placeLabels([
      { key: 'title', box: box(0), keep: true },
      { key: 'tick', box: box(5) },
    ])
    expect([...kept]).toEqual(['title'])
  })

  it('빈 목록은 빈 결과', () => {
    expect(placeLabels([]).size).toBe(0)
  })
})
