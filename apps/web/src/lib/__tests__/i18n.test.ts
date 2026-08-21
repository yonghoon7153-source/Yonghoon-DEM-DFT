import { describe, expect, it } from 'vitest'

import { ko } from '../i18n'

describe('knee reasons', () => {
  it('translates a detected segmented knee, keeping the numbers', () => {
    expect(
      ko.kneeReason('fade rate steepens 6.90x at cycle 22 (-0.179 -> -1.233 %/cycle)'),
    ).toBe('22번 사이클에서 열화율이 6.90배로 급해집니다 (-0.179 → -1.233 %/cycle)')
  })

  it('translates a threshold crossing', () => {
    expect(ko.kneeReason('retention crossed 80% at cycle 36.1')).toBe(
      '유지율이 36.1번 사이클에서 80% 를 통과했습니다',
    )
  })

  it('translates the slope-ratio criterion', () => {
    expect(
      ko.kneeReason(
        'fade rate reached 2x the early-life rate (-0.216 vs -0.081 %/cycle) at cycle 13',
      ),
    ).toContain('13번 사이클에서 열화율이 초기의 2배에 도달')
  })

  it('translates a non-detection', () => {
    expect(ko.kneeReason('capacity is not fading')).toBe('용량이 감소하지 않습니다')
    expect(ko.kneeReason('needs at least 9 cycles, has 5')).toBe(
      '사이클이 5개뿐입니다 (9개 이상 필요)',
    )
  })

  // knee.py 가 실제로 내보내는 문장들.  아래 목록은 원형 곡선 12종과 직선 열화
  // 200개를 돌려 나온 이유를 모아 숫자만 다른 것을 하나로 합친 것이다.
  // knee.py 의 문구를 바꾸면 여기가 먼저 빨개진다 — 화면이 영어로 나가기 전에.
  const REASONS = [
    'a bent line fits no better than a straight one',
    'capacity is not fading',
    'capacity never fell below 80% (lowest 100.0%)',
    'curvature peaks at cycle 10 but fade accelerates only 0.02x there (needs 1.5x)',
    'curvature peaks at cycle 105, but a line bent there fits no better than a straight one',
    'curvature peaks at cycle 115 but only 0.3% is lost afterwards (needs 2%)',
    'dipped below 80% at cycle 164 but recovered',
    'fade accelerates only 1.00x (needs 1.5x)',
    'fade begins at cycle 20 (+0.337 -> -0.894 %/cycle)',
    'fade does not accelerate after the best break point',
    'fade rate never stayed at 2x the early-life rate',
    'fade rate reached 2x the early-life rate (-0.228 vs -0.044 %/cycle) at cycle 76',
    'fade rate steepens 11.77x at cycle 40 (-0.119 -> -1.401 %/cycle)',
    'fade steepens at cycle 22 (-0.088 -> -4.277 %/cycle) and eases off again from cycle 34 (-0.541 %/cycle)',
    'maximum curvature at cycle 11',
    'needs at least 7 cycles, has 3',
    'neither of the two best break points accelerates the fade',
    'no complete cycles',
    'no three-line break point fits',
    'only 0.4% is lost after cycle 86 (needs 2%)',
    'retention crossed 80% at cycle 102.6',
    'series too short after edge trimming',
    'a three-line fit needs at least 13 cycles, has 10',
    'the rate does steepen, but only 0.1% is lost afterwards (needs 2%)',
    'the rate steepens around cycle 124, but a line bent there fits no better than a straight one',
    'no usable cycle at or after cycle 50; the record ends at cycle 5',
    'fell below 80% at cycle 12, the last cycle in the record -- nothing follows to confirm it',
    'cycle 12 bends, but only 5 cycles follow it and 1.8% has been lost so far -- at this rate the 2% that makes it a knee needs about 6',
    'fade steepens at cycle 88 (-0.020 -> -0.900 %/cycle)',
    'fade rate steepens 11.67x at cycle 12 (-0.030 -> -0.350 %/cycle); another criterion puts it at cycle 51',
    // API 가 허용하는 경계 파라미터.  Python 의 :g 가 지수 표기를 만든다.
    'capacity never fell below 1e-05% (lowest 99.0%)',
    'fade rate never stayed at 1e+06x the early-life rate',
  ]

  it('translates every reason knee.py can produce', () => {
    const english: string[] = []
    for (const reason of REASONS) {
      const translated = ko.kneeReason(reason)
      if (translated === reason) english.push(reason)
    }
    expect(english).toEqual([])
  })

  it('keeps the cycle numbers of every reason it translates', () => {
    for (const reason of REASONS) {
      const numbers = reason.match(/\d+\.?\d*/g) ?? []
      const translated = ko.kneeReason(reason)
      for (const value of numbers) {
        expect(translated, reason).toContain(value)
      }
    }
  })

  it('passes an unrecognised sentence through rather than dropping it', () => {
    expect(ko.kneeReason('some future criterion said no')).toBe(
      'some future criterion said no',
    )
  })

  it('records the passthrough, so a new backend wording is not silently English', () => {
    ko.kneeReason('a wording nobody has translated yet')
    ko.basisReason('some future basis is missing')
    expect(ko.untranslated()).toContain('a wording nobody has translated yet')
    expect(ko.untranslated()).toContain('some future basis is missing')
    // a phrase with a rule must not be reported as missing
    ko.basisReason('active mass not set')
    expect(ko.untranslated()).not.toContain('active mass not set')
  })
})

describe('state evidence', () => {
  it('translates a truncated final cycle', () => {
    expect(ko.evidence('cycle 45 is cut off mid-step')).toBe(
      '45번 사이클이 스텝 도중에 잘렸습니다',
    )
  })

  it('translates a stale record that ends mid-cycle', () => {
    const text = ko.evidence(
      'nothing logged for 5.5 months even though the record ends mid-cycle - ' +
        'the test stopped, or it continued in a file that is not here',
    )
    expect(text).toContain('5.5개월')
    expect(text).toContain('여기 없는 파일')
  })

  it('translates a fresh record', () => {
    expect(ko.evidence('last sample is 2.1 h old, under two cycle times (7.4 h)')).toBe(
      '마지막 샘플이 2.1시간 전입니다 (사이클 2회분(7.4시간) 이내)',
    )
  })

  it('translates the signal and target labels', () => {
    expect(ko.signal('partial cycle')).toBe('잘린 사이클')
    expect(ko.stateTarget('running')).toBe('구동 중')
  })
})

describe('cell notes', () => {
  it('translates a composition-derived mass, keeping the blend label', () => {
    expect(ko.cellNote('31.6 mg x 80 wt% from AM:SE:VGCF = 80:17:3')).toBe(
      '31.6 mg × 80 wt% — AM:SE:VGCF = 80:17:3',
    )
  })

  it('translates the assumption made when no composition is given', () => {
    expect(
      ko.cellNote(
        '31.6 mg x 100 wt% (no composition given - assuming the whole electrode is active material)',
      ),
    ).toContain('전극 전체를 활물질로 가정')
  })

  it('translates a collector subtraction', () => {
    expect(ko.cellNote('31.6 mg (after 8.4 mg collector) x 80 wt%')).toBe(
      '31.6 mg (집전체 8.4 mg 제외) × 80 wt%',
    )
  })
})

describe('basis and composition problems', () => {
  it('explains why a basis is unavailable', () => {
    expect(ko.basisReason('active mass not set')).toBe('활물질 질량이 없습니다')
  })

  it('translates composition problems', () => {
    expect(ko.compositionProblem('weight percentages add up to 102, not 100')).toBe(
      'wt% 합이 102 입니다 (100 이 아님)',
    )
    expect(ko.compositionProblem('the active material is 0 wt%')).toBe(
      '활물질이 0 wt% 입니다',
    )
  })
})

// --- 백엔드가 실제로 내는 문구가 전부 번역되는가 ------------------------------
//
// 규칙표를 손으로 관리하면 백엔드가 새 문구를 내놓을 때마다 조용히 영어가 샌다.
// 아래 목록은 wrdkit 의 normalize.resolve() 와 composition.problems() 가
// 만들어 내는 실제 문자열이다 — 새 사유를 추가하면 여기도 늘려야 한다.
describe('백엔드 문구 커버리지', () => {
  const CELL_NOTES = [
    'entered directly',
    'current collector mass exceeds total mass',
    'directly entered active mass is not positive - ignored',
    '31.6 mg x 80 wt%',
    '31.6 mg x 80 wt% from AM 80 : SE 20',
    '26.6 mg (after 5 mg collector) x 80 wt%',
    '31.6 mg x 100 wt% (no composition given - assuming the whole electrode is active material)',
    '26.6 mg (after 5 mg collector) x 100 wt% (no composition given - assuming the whole electrode is active material)',
    'the composition names no active material - none of Zzz, Qqq is a known active material; enter the active wt% to use mAh/g',
    'the composition names no active material; enter the active wt% to use mAh/g',
    'π x (13 mm / 2)²',
    '1.3273 cm² x 60 µm',
    '25.28 mg x 200 mAh/g',
  ]

  it.each(CELL_NOTES)('cellNote 가 번역한다: %s', (note) => {
    const before = ko.untranslated().length
    const out = ko.cellNote(note)
    expect(ko.untranslated().length).toBe(before)
    expect(out).not.toBe(note)
  })

  const COMPOSITION_PROBLEMS = [
    'weight percentages add up to 95, not 100',
    'a component has a negative weight percent',
    'no component is marked as the active material',
    'the active material is 0 wt%',
    'a component name is repeated',
  ]

  it.each(COMPOSITION_PROBLEMS)('compositionProblem 이 번역한다: %s', (problem) => {
    const before = ko.untranslated().length
    expect(ko.compositionProblem(problem)).not.toBe(problem)
    expect(ko.untranslated().length).toBe(before)
  })
})
