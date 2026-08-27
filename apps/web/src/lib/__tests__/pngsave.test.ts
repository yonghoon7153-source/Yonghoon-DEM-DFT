import { describe, expect, it, vi } from 'vitest'

import {
  AXIS_PX, axisPx, downloadCanvas, PNG_TICK_ROOM, safeFileName, scaleFont,
} from '../pngsave'

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

describe('저장할 때 눈금이 촘촘해지지 않는다', () => {
  it('축 간격도 같은 배로 — 눈금 수는 배수와 무관하다', () => {
    // uPlot 은 눈금 수를 `그림 폭 / space` 로 정한다 (space 는 눈금 사이 최소
    // 픽셀).  그림만 세 배로 키우고 space 를 그대로 두면 눈금이 세 배가 되고,
    // 글꼴도 세 배라 그것들이 서로 겹친다 — GITT 그림의 가로 눈금이
    // `0.0250.050.075…` 로 붙어 나온 것이 그 자국이다.
    const ticks = (plotPx: number, scale: number) =>
      (plotPx * scale) / axisPx(scale).xSpace
    expect(ticks(600, 3)).toBeCloseTo(ticks(600, 1), 10)
    expect(ticks(600, 1)).toBeCloseTo(12, 10)

    const yTicks = (plotPx: number, scale: number) =>
      (plotPx * scale) / axisPx(scale).ySpace
    expect(yTicks(320, 4)).toBeCloseTo(yTicks(320, 1), 10)
  })

  it('배수가 1 이면 화면 값 그대로 — 저장을 붙였다고 화면이 바뀌면 안 된다', () => {
    expect(axisPx(1)).toEqual(AXIS_PX)
  })

  it('저장은 한 번 더 성기게 — 가로를 세로보다 더', () => {
    // 가로 글자는 나란히 누워 부딪히고 세로 글자는 쌓여서 안 부딪힌다.
    expect(PNG_TICK_ROOM.x).toBeGreaterThan(PNG_TICK_ROOM.y)
    const px = axisPx(3, PNG_TICK_ROOM)
    expect(px.xSpace).toBe(AXIS_PX.xSpace * 3 * PNG_TICK_ROOM.x)
    expect(px.ySpace).toBe(AXIS_PX.ySpace * 3 * PNG_TICK_ROOM.y)
    // 글자 띠는 **안** 성기게 한다 — 글자가 앉는 자리라 글꼴 배수만 따라간다.
    expect(px.xSize).toBe(AXIS_PX.xSize * 3)
    expect(px.ySize).toBe(AXIS_PX.ySize * 3)
  })

  it('눈금 글자 띠도 같이 커진다 — 33 px 글자가 50 px 띠에 안 들어간다', () => {
    expect(axisPx(3).xSize).toBe(AXIS_PX.xSize * 3)
    expect(axisPx(3).ySize).toBe(AXIS_PX.ySize * 3)
  })
})

describe('내려받기가 실패하면 말한다', () => {
  it('`toBlob` 이 null 을 주면 부르는 쪽에 알린다', () => {
    // 브라우저가 캔버스를 PNG 로 못 굽는 경우 (대개 너무 커서다).  `toBlob` 은
    // **비동기**라 throw 로는 못 알린다 — 부르는 쪽의 try 는 이미 끝나 있다.
    const canvas = {
      toBlob: (done: (blob: Blob | null) => void) => done(null),
    } as unknown as HTMLCanvasElement
    const said: string[] = []
    downloadCanvas(canvas, '그림', (why) => said.push(why))
    expect(said).toHaveLength(1)
    expect(said[0]).toContain('만들지 못했습니다')
  })

  it('성공하면 아무 말도 안 한다 — 그리고 파일 이름을 붙인다', () => {
    // jsdom 에는 `URL.createObjectURL` 이 없다 (Blob URL 을 만들 곳이 없다).
    const urls = URL as unknown as Record<string, unknown>
    urls.createObjectURL = () => 'blob:x'
    urls.revokeObjectURL = () => {}
    const clicked: string[] = []
    const canvas = {
      toBlob: (done: (blob: Blob | null) => void) => done(new Blob(['x'])),
    } as unknown as HTMLCanvasElement
    const realCreate = document.createElement.bind(document)
    const spy = vi.spyOn(document, 'createElement').mockImplementation(((tag: string) => {
      const node = realCreate(tag)
      if (tag === 'a') {
        Object.defineProperty(node, 'click', {
          value: () => clicked.push((node as HTMLAnchorElement).download),
        })
      }
      return node
    }) as typeof document.createElement)
    const said: string[] = []
    downloadCanvas(canvas, 'LPSCl 셀 #3', (why) => said.push(why))
    spy.mockRestore()
    delete urls.createObjectURL
    delete urls.revokeObjectURL
    expect(said).toEqual([])
    expect(clicked).toEqual(['LPSCl 셀 #3.png'])
  })
})
