/** 세 업로드 화면이 함께 쓰는 부품.
 *
 *  한 곳에 모은 이유가 "같은 일" 이므로, 그 같은 일이 실제로 같은지는 여기서
 *  한 번만 고정한다 — 화면마다 다시 적으면 셋이 갈라져도 테스트가 통과한다.
 */

import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { DropZone, cellNameFor } from '../UploadTarget'

afterEach(() => vi.unstubAllGlobals())

describe('cellNameFor', () => {
  it('끝의 파일 순번만 뗀다 — 쪼개진 두 파일은 한 셀이다', () => {
    // Smart Interface 가 긴 실험을 `_011`, `_012` 로 쪼갠다 (§3).
    expect(cellNameFor('No_1_dry_0.0316g_011.wrd')).toBe('No_1_dry_0.0316g')
    expect(cellNameFor('No_1_dry_0.0316g_012.wrd')).toBe('No_1_dry_0.0316g')
  })

  it('확장자를 가리지 않는다 — .mpr 도 셀 이름이 나와야 한다', () => {
    expect(cellNameFor('cell29_half_01.mpr')).toBe('cell29_half')
  })

  it('이름 안의 질량과 조건은 건드리지 않는다', () => {
    // 규칙을 더 넣을수록 틀릴 자리가 는다.  사람이 적은 것은 그대로 둔다.
    expect(cellNameFor('260612_Gr_Fe_0.3mg_26.8.wrd')).toBe('260612_Gr_Fe_0.3mg_26.8')
  })

  it('뗄 것만 남으면 원래 이름을 지킨다 — 빈 셀 이름을 만들지 않는다', () => {
    expect(cellNameFor('011.wrd')).toBe('011')
  })
})

describe('DropZone', () => {
  function drop(files: File[]) {
    const seen: File[][] = []
    render(
      <DropZone accept=".wrd" label="여기에 .wrd 파일을 끌어다 놓으세요"
                onFiles={(list) => seen.push([...list])} />,
    )
    const zone = screen.getByRole('button')
    // jsdom 은 DataTransfer 를 만들어 주지 않으므로 event 에 직접 실어 준다.
    fireEvent.drop(zone, { dataTransfer: { files } })
    return seen
  }

  it('끌어다 놓으면 그 파일들이 그대로 간다', () => {
    const files = [new File(['a'], 'a.wrd'), new File(['b'], 'b.wrd')]
    expect(drop(files)[0]?.map((f) => f.name)).toEqual(['a.wrd', 'b.wrd'])
  })

  it('눌러서 고르는 길도 같은 자리로 간다', async () => {
    const seen: File[][] = []
    render(
      <DropZone accept=".wrd" label="여기에 .wrd 파일을 끌어다 놓으세요"
                onFiles={(list) => seen.push([...list])} />,
    )
    // 라벨이 곧 그 자리의 이름이다 — 숨은 input 이 이름 없는 컨트롤이 되면
    // 키보드로도 스크린리더로도 못 쓴다.
    const input = screen.getByLabelText('여기에 .wrd 파일을 끌어다 놓으세요')
    await userEvent.upload(input, new File(['x'], 'x.wrd'))
    await waitFor(() => expect(seen).toHaveLength(1))
    expect(seen[0]?.[0]?.name).toBe('x.wrd')
  })

  it('끄는 동안 표시가 붙고, 나가면 떨어진다', () => {
    render(
      <DropZone accept=".wrd" label="끌어다 놓으세요" onFiles={() => {}} />,
    )
    const zone = screen.getByRole('button')
    expect(zone.className).not.toContain('over')

    fireEvent.dragOver(zone)
    expect(zone.className).toContain('over')

    fireEvent.dragLeave(zone)
    expect(zone.className).not.toContain('over')
  })
})
