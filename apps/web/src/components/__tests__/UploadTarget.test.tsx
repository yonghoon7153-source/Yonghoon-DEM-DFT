/** 세 업로드 화면이 함께 쓰는 부품.
 *
 *  한 곳에 모은 이유가 "같은 일" 이므로, 그 같은 일이 실제로 같은지는 여기서
 *  한 번만 고정한다 — 화면마다 다시 적으면 셋이 갈라져도 테스트가 통과한다.
 */

import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { useState } from 'react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import {
  DropZone, UploadTargetFields, cellNameFor, useUploadTarget,
} from '../UploadTarget'

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


describe('파일 이름으로 셀 만들기는 충방전만', () => {
  /** 훅과 화면을 같이 세우는 탐침.  `planFor` 가 무엇을 돌려주는지가
   *  이 테스트의 본체라 버튼 하나로 눌러서 꺼낸다. */
  function Probe({ perFileCell }: { perFileCell: boolean }) {
    const pick = useUploadTarget(0, perFileCell)
    const [got, setGot] = useState<string>('')
    return (
      <>
        <UploadTargetFields pick={pick} />
        <button
          type="button"
          onClick={async () => {
            const plan = await pick.planFor([new File(['x'], 'cellA_01_C01.mpr')])
            setGot(JSON.stringify(plan))
          }}
        >
          계획
        </button>
        <output>{got}</output>
      </>
    )
  }

  function installFetch(made: unknown[]) {
    vi.stubGlobal('fetch', vi.fn(async (_url: string, init?: RequestInit) => {
      if (init?.method === 'POST') {
        made.push(JSON.parse(String(init.body)))
        return new Response(JSON.stringify({ id: 99, name: 'x' }),
                            { headers: { 'content-type': 'application/json' } })
      }
      return new Response('[]', { headers: { 'content-type': 'application/json' } })
    }))
  }

  it('충방전에는 체크박스가 있다', async () => {
    installFetch([])
    render(<Probe perFileCell />)
    expect(await screen.findByLabelText('파일 이름을 셀 이름으로')).toBeInTheDocument()
  })

  it('EIS·GITT 에는 체크박스가 없고, 대신 나중에 붙이라고 말한다', async () => {
    installFetch([])
    render(<Probe perFileCell={false} />)
    await screen.findByLabelText('새 셀 이름')
    expect(screen.queryByLabelText('파일 이름을 셀 이름으로')).toBeNull()
    expect(screen.getByText(/나중에 아래 색인에서 붙일 수 있습니다/)).toBeInTheDocument()
  })

  it('길을 안 열면 셀을 만들지 않는다 — 체크박스만 숨기는 것으로는 부족하다', async () => {
    // 여기가 실제로 샜던 자리다.  EIS 업로드가 `.mpr` 이름으로 충방전 셀을
    // 만들어서, EC-Lab 채널 번호까지 붙은 (`..._01_C01`) 파일 0개짜리 셀이
    // 셀 목록·대시보드·관계셀 고르개에 쌓였다.
    const made: unknown[] = []
    installFetch(made)
    render(<Probe perFileCell={false} />)
    await screen.findByLabelText('새 셀 이름')
    await userEvent.click(screen.getByRole('button', { name: '계획' }))
    await waitFor(() => expect(screen.getByRole('status').textContent).toBe('[null]'))
    expect(made).toEqual([])
  })
})
