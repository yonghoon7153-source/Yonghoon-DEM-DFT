/** 셀 하나를 기록에서 지우는 버튼.
 *
 * 대시보드와 셀 라이브러리가 같은 것을 쓴다.  같은 동작을 두 화면에 따로 적으면
 * 반드시 한쪽만 고쳐지고, 하필 그것이 **무엇이 지워지는가** 를 설명하는 문구다 —
 * 한 화면은 "원본도 지워진다" 로 읽히고 다른 화면은 아니게 된다.
 *
 * 두 번 눌러야 지워진다.  표의 행 끝에 있는 버튼이라 스크롤하다 스치기 쉽고,
 * 되돌리기가 없다.
 *
 * 원본 `.wrd` 는 지우지 않는다 (저장소 불변 규칙 2).  파일은 `data/uploads/` 에
 * 남고, 다시 올리면 sha256 이 같아 그대로 살아난다 — 그래서 이 버튼은 "삭제"
 * 라기보다 "목록에서 내리기" 에 가깝고, 문구도 그렇게 적는다.
 */

import { useState } from 'react'

import { api } from '../lib/api'
import { TrashIcon } from './ui'

export function DeleteSampleButton({
  sampleId,
  sampleName,
  onDeleted,
  onError,
}: {
  sampleId: number
  sampleName: string
  onDeleted: () => void
  /** 실패를 어디에 그릴지는 표가 정한다 — 행 안에 끼우면 열이 밀린다. */
  onError: (message: string | null) => void
}) {
  const [confirming, setConfirming] = useState(false)
  const [busy, setBusy] = useState(false)

  if (!confirming) {
    return (
      <button
        className="ghost icon"
        aria-label={`${sampleName} 지우기`}
        title="이 셀을 기록에서 지웁니다 (원본 .wrd 는 남습니다)"
        onClick={() => {
          onError(null)
          setConfirming(true)
        }}
      >
        <TrashIcon />
      </button>
    )
  }

  return (
    <>
      <button
        className="danger tiny"
        disabled={busy}
        onClick={async () => {
          setBusy(true)
          try {
            onError(null)
            await api.deleteSample(sampleId, true)
            setConfirming(false)
            onDeleted()
          } catch (cause) {
            onError(cause instanceof Error ? cause.message : String(cause))
          } finally {
            setBusy(false)
          }
        }}
      >
        지웁니다
      </button>
      <button className="ghost tiny" disabled={busy} onClick={() => setConfirming(false)}>
        취소
      </button>
    </>
  )
}
