/** Origin 으로 옮기는 버튼 한 줄.
 *
 *  절차서의 마지막 단계가 "Copy to clipboard → 엑셀 → Origin" 이다.  충방전
 *  화면에는 있었고 EIS·GITT 에는 없었다 — 화면에서 읽을 수는 있는데 밖으로
 *  나갈 수가 없으면 그 자리에서 절차가 끊긴다.
 *
 *  복사할 것이 없을 때 조용히 성공한 척하지 않는다.  빈 클립보드는 붙여
 *  넣기 전까지 티가 안 나고, 그때는 이 화면을 이미 떠난 뒤다.
 */

import { useState } from 'react'

import { Alert } from './ui'
import { copyText } from '../lib/origin'

export interface CopyItem {
  label: string
  /** 누를 때 만든다 — 화면에 있는 것을 그대로 복사하기 위해. */
  build: () => string
  title?: string
  disabled?: boolean
  /** 몇 개를 뺐는지.  조용히 빼면 점 수가 다른 것을 못 본다. */
  skipped?: number
  skippedNote?: (skipped: number) => string
}

export function CopyBar({ items }: { items: CopyItem[] }) {
  const [copied, setCopied] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [note, setNote] = useState<string | null>(null)

  async function run(item: CopyItem) {
    setError(null)
    setNote(null)
    const text = item.build()
    if (!text) {
      setError(`복사할 ${item.label} 데이터가 없습니다`)
      return
    }
    try {
      await copyText(text)
      setCopied(item.label)
      if (item.skipped && item.skippedNote) setNote(item.skippedNote(item.skipped))
      window.setTimeout(
        () => setCopied((current) => (current === item.label ? null : current)), 1800)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    }
  }

  return (
    <div className="col copy-bar" style={{ gap: 6 }}>
      {/* `align-items: center` 가 없으면 `.row` 의 기본 정렬(stretch)이 작은
          글자를 단추 높이만큼 늘려, 'Origin 으로' 가 단추 위쪽에 걸린다. */}
      <div className="row" style={{ gap: 6, flexWrap: 'wrap', alignItems: 'center' }}>
        <span className="tiny faint">Origin 으로</span>
        {items.map((item) => (
          <button
            key={item.label}
            type="button"
            disabled={item.disabled}
            title={item.title}
            aria-label={copied === item.label
              ? `${item.label} 복사됨` : `${item.label} 복사`}
            onClick={() => void run(item)}
          >
            {copied === item.label ? '복사됨 ✓' : item.label}
          </button>
        ))}
      </div>
      {error ? <Alert kind="error">{error}</Alert> : null}
      {note ? <Alert kind="warn">{note}</Alert> : null}
    </div>
  )
}
