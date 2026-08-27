import { describe, expect, it } from 'vitest'

import { safeFileName, scaleFont } from '../pngsave'

describe('그림 저장 — 파일 이름과 글꼴 배수', () => {
  it('파일 이름에 못 쓰는 글자만 걷어내고 한글은 남긴다', () => {
    // 셀 이름이 한글이라, 라틴만 남기면 파일 이름이 전부 같아진다.
    expect(safeFileName('LPSCl 셀 #3')).toBe('LPSCl 셀 #3')
    expect(safeFileName('a/b:c*d?e"f<g>h|i')).toBe('a b c d e f g h i')
    expect(safeFileName('   ')).toBe('plot')
    expect(safeFileName('')).toBe('plot')
    expect(safeFileName('x'.repeat(200)).length).toBe(80)
  })

  it('글꼴 크기만 배로 — 가족·굵기는 그대로', () => {
    expect(scaleFont('11px Pretendard, system-ui', 3)).toBe('33px Pretendard, system-ui')
    expect(scaleFont('600 11px Pretendard', 3)).toBe('600 33px Pretendard')
    // 배가 1 이면 아무것도 안 바뀌어야 한다 — 화면용 옵션이 그 길로 온다.
    expect(scaleFont('600 11px Pretendard', 1)).toBe('600 11px Pretendard')
    // 소수 배수에서 자리수가 폭발하지 않게.
    expect(scaleFont('11px x', 1.5)).toBe('16.5px x')
  })
})
