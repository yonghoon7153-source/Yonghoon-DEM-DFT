/** 실수축 위의 점을 어떻게 다루는가.
 *
 *  판정은 부호 하나다.  "고주파 몇 점" 처럼 세는 규칙으로 바뀌면 아크가
 *  실제로 유도성인 셀(리튬 도금 같은)에서 실측을 지우게 된다 — 그래서
 *  여기서 부호 규칙을 못박는다.
 */

import { describe, expect, it } from 'vitest'

import {
  arcWindow, inductiveCount, inductiveRun, isScan, nyquistXy, scanFit, sweepAt,
} from '../eis'

/** 반원 하나 + 45° 확산 꼬리.  실제 전고체 풀셀의 모양이다. */
function arcThenTail(tailTop: number) {
  const x: number[] = []
  const y: number[] = []
  // 반원: 지름 20, 꼭대기 10.
  for (let t = 0; t <= 20; t += 1) {
    x.push(t)
    y.push(Math.sqrt(Math.max(0, 100 - (t - 10) ** 2)))
  }
  // 45° 꼬리: 골짜기(20, 0)에서 올라간다.
  for (let t = 1; t <= tailTop; t += 1) {
    x.push(20 + t)
    y.push(t)
  }
  return [{ x, y }]
}

describe('유도성 꼬리', () => {
  const frequency = [1e5, 1e4, 1e3, 1e2, 1e1]
  const zRe = [10, 8, 7, 9, 20]
  const zIm = [21.7, 7.4, -0.4, -2.1, -12]

  it('고주파에서 이어진 구간만 센다', () => {
    expect(inductiveCount(zIm, frequency)).toBe(2)
    expect(inductiveCount([-1, -2], [10, 1])).toBe(0)
  })

  /** 부호는 관측이지 "배선이다" 의 증명이 아니다.  배터리는 제 저주파 유도성
   *  고리를 갖는다 (화학적 인덕턴스·드리프트) — 그것은 셀의 측정값이다. */
  it('저주파의 양수는 안 뺀다 — 그것은 셀의 것일 수 있다', () => {
    const f = [1e5, 1e4, 1e3, 1e2, 1e1, 1e0]
    const im = [5, 3, -1, -2, 0.4, 0.9]
    expect(inductiveRun(im, f)).toEqual([true, true, false, false, false, false])
    expect(inductiveCount(im, f)).toBe(2)
  })

  it('가운데 한 점만 양수면 배선이 아니다 — 이어져 있지 않다', () => {
    const f = [1e4, 1e3, 1e2, 1e1, 1e0]
    expect(inductiveRun([10, -2, 3, -4, -5], f))
      .toEqual([true, false, false, false, false])
  })

  it('배열이 저주파부터 담겨 있어도 판정이 같다', () => {
    const f = [1e0, 1e1, 1e2, 1e3, 1e4]
    expect(inductiveRun([-5, -4, 3, -2, 10], f))
      .toEqual([false, false, false, false, true])
  })

  it('세로축은 −Z″ 다 — 부호를 뒤집는다', () => {
    const { x, y, dropped } = nyquistXy(zRe, zIm, false)
    expect(x).toEqual(zRe)
    expect(y).toEqual(zIm.map((one) => -one))
    expect(dropped).toBe(0)
  })

  it('빼면 몇 개를 뺐는지 함께 돌려준다 — 조용히 빼지 않는다', () => {
    const { x, y, dropped } = nyquistXy(zRe, zIm, true, undefined, frequency)
    expect(dropped).toBe(2)
    expect(x).toEqual([7, 9, 20])
    expect(y).toEqual([0.4, 2.1, 12])
  })

  it('눈금 바꾸기는 자른 뒤에 태운다 (Ω → Ω·cm²)', () => {
    const { x, y } = nyquistXy(zRe, zIm, true, (value) => value * 2, frequency)
    expect(x).toEqual([14, 18, 40])
    expect(y).toEqual([0.8, 4.2, 24])
  })
})

describe('아크가 사는 구간', () => {
  it('꼬리가 반원보다 높으면 반원까지만 남긴다', () => {
    const window = arcWindow(arcThenTail(40))
    expect(window).not.toBeNull()
    // 반원 꼭대기가 세로 눈금이 된다 — 꼬리 40 이 아니라.
    expect(window!.yMax).toBeCloseTo(10, 6)
    // 가로는 골짜기(20)에서 조금 더.  꼬리 끝(60)까지 가지 않는다.
    expect(window!.xMax).toBeGreaterThanOrEqual(20)
    expect(window!.xMax).toBeLessThan(25)
  })

  it('꼬리가 반원보다 낮으면 자르지 않는다 — 전부 보이는 편이 낫다', () => {
    expect(arcWindow(arcThenTail(4))).toBeNull()
  })

  it('꼬리가 아예 없으면 자르지 않는다', () => {
    const x: number[] = []
    const y: number[] = []
    for (let t = 0; t <= 20; t += 1) {
      x.push(t)
      y.push(Math.sqrt(Math.max(0, 100 - (t - 10) ** 2)))
    }
    expect(arcWindow([{ x, y }])).toBeNull()
  })

  it('반원이 둘이면 **둘 다** 남긴다 — 첫 골짜기에서 자르면 두 번째를 잘라먹는다',
     () => {
    const x: number[] = []
    const y: number[] = []
    for (let t = 0; t <= 20; t += 1) {          // 첫 반원 (꼭대기 5)
      x.push(t)
      y.push(0.5 * Math.sqrt(Math.max(0, 100 - (t - 10) ** 2)))
    }
    for (let t = 1; t <= 20; t += 1) {          // 둘째 반원 (꼭대기 10)
      x.push(20 + t)
      y.push(Math.sqrt(Math.max(0, 100 - (t - 10) ** 2)))
    }
    for (let t = 1; t <= 40; t += 1) {          // 꼬리
      x.push(40 + t)
      y.push(t)
    }
    const window = arcWindow([{ x, y }])
    expect(window).not.toBeNull()
    expect(window!.yMax).toBeCloseTo(10, 6)
    expect(window!.xMax).toBeGreaterThanOrEqual(40)
  })

  it('점이 너무 적으면 판단하지 않는다', () => {
    expect(arcWindow([{ x: [1, 2], y: [1, 2] }])).toBeNull()
    expect(arcWindow([])).toBeNull()
  })
})

/** 스캔의 한 스윕인가, 그리고 그 스윕은 어느 상태에서 잰 것인가.
 *
 *  라이브러리·비교·스캔 상세 세 화면이 같은 판정을 써야 한 화면에서 "스캔"
 *  인 것이 다른 화면에서 낱장 스무 개로 흩어지지 않는다.
 */
describe('SOC 스캔의 스윕', () => {
  it('스윕이 둘 이상이면 스캔이다 — 안 적힌 것은 낱장', () => {
    expect(isScan({ sweep_count: 11 })).toBe(true)
    expect(isScan({ sweep_count: 1 })).toBe(false)
    expect(isScan({ sweep_count: null })).toBe(false)
    expect(isScan({})).toBe(false)
  })

  it('용량이 있으면 용량, 없으면 전위', () => {
    expect(sweepAt({ capacity_mah: 1.234, potential_v: 3.85 })).toBe('1.23 mAh')
    expect(sweepAt({ capacity_mah: null, potential_v: 3.85 })).toBe('3.85 V')
  })

  it('만방전(0 mAh)은 "모름" 이 아니다', () => {
    expect(sweepAt({ capacity_mah: 0 })).toBe('0 mAh')
  })

  it('둘 다 없으면 빈 문자열 — 0 으로 적으면 만방전과 구분되지 않는다', () => {
    expect(sweepAt({ capacity_mah: null, potential_v: null })).toBe('')
    expect(sweepAt({})).toBe('')
  })
})

/** 접힌 스캔 한 줄의 fitting 상태.
 *
 *  이 함수가 있는 이유는 하나다: 접힌 줄에 **첫 스윕의** χ² 를 적으면 스물 중
 *  하나만 맞춘 파일이 맞춘 파일로 보인다.  그래서 시험도 그 자리를 본다 —
 *  "일부만 맞춘 것은 절대 완료라고 하지 않는다".
 */
describe('scanFit', () => {
  const sweep = (fits: number, chi: number | null = 0.002, circuit = 'R0-p(R1,CPE1)') => ({
    fit_count: fits,
    best_circuit: fits ? circuit : null,
    best_chi_squared: fits ? chi : null,
  })

  it('스윕 전부가 맞춰졌으면 완료라고 한다', () => {
    const state = scanFit([sweep(1), sweep(2), sweep(1)], 3)
    expect(state.done).toBe(true)
    expect(state.label).toBe('fitting 완료')
    expect(state.fitted).toBe(3)
    expect(state.sweeps).toBe(3)
  })

  it('하나라도 안 맞춰졌으면 완료가 아니라 센 것을 적는다', () => {
    const state = scanFit([sweep(1), sweep(0), sweep(1)], 3)
    expect(state.done).toBe(false)
    expect(state.label).toBe('fitting 2/3')
  })

  it('맞춘 적이 없으면 0/N 이 아니라 —', () => {
    const state = scanFit([sweep(0), sweep(0)], 2)
    expect(state.done).toBe(false)
    expect(state.label).toBe('—')
    expect(state.detail).toBe('')
  })

  //: 거르개가 스윕을 가려도 거짓 '완료' 는 나오지 않아야 한다.  분모는 파일이
  //  말하는 수이고, 안 보이는 스윕은 안 맞춘 것으로 센다.
  it('거르개에 가려진 스윕이 있으면 완료라고 하지 않는다', () => {
    const state = scanFit([sweep(1), sweep(1)], 11)
    expect(state.done).toBe(false)
    expect(state.label).toBe('fitting 2/11')
    expect(state.sweeps).toBe(11)
  })

  //: 평균이 아니라 **가장 나쁜** χ² 다.  하나가 크게 틀렸는데 나머지가 좋으면
  //  평균은 그것을 감춘다.
  it('χ² 는 가장 나쁜 스윕의 것을 적는다', () => {
    const state = scanFit([sweep(1, 0.002), sweep(1, 0.5), sweep(1, 0.01)], 3)
    expect(state.detail).toContain('χ²≤0.5')
    expect(state.detail).toContain('R0-p(R1,CPE1)')
  })

  it('회로가 섞여 있으면 하나를 대표로 적지 않는다', () => {
    const state = scanFit(
      [sweep(1, 0.002, 'R0-p(R1,CPE1)'), sweep(1, 0.003, 'R0-TL')], 2)
    expect(state.detail).toContain('회로 2종')
    expect(state.detail).not.toContain('R0-TL')
  })

  it('χ² 가 없는 맞춤도 셈에는 들어간다', () => {
    const state = scanFit([sweep(1, null), sweep(1, null)], 2)
    expect(state.label).toBe('fitting 완료')
    expect(state.detail).toBe('R0-p(R1,CPE1)')
  })

  it('빈 목록은 완료가 아니다', () => {
    expect(scanFit([], 0).done).toBe(false)
    expect(scanFit([], 0).label).toBe('—')
  })
})
