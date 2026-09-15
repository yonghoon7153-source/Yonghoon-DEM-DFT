/** 이격 간격 — **사람이 정한다.**
 *
 *  한동안 이 수는 자동이었다 (보이는 곡선 높이의 중앙값 × 0.6).  데이터가
 *  정하는 수라 스캔마다 달라졌고, 그래서 두 스캔을 나란히 놓으면 **같은 그림이
 *  다른 자로 그려졌다** — 이격이 6.79 인 그림과 31.2 인 그림을 옆에 붙여 놓고
 *  "이쪽이 더 벌어져 있다" 를 말할 수 없다.  논문에 실을 때 손으로 맞추는 수가
 *  바로 이것이기도 하다.
 *
 *  그래서 자동을 버리고 **입력칸**을 둔다.  기본은 20 이고, 원하는 만큼 쓴다.
 *
 *  **단위는 지금 보고 있는 세로축의 단위**다 (Ω 또는 Ω·cm²).  단위를 바꾸면
 *  같은 20 이 다른 크기가 되는데, 그것이 맞다 — 이 수는 값이 아니라 **화면에서
 *  얼마나 떼어 놓을지**이고, 떼어 놓는 거리는 그 축의 자로 재는 것이다.
 *
 *  비워 두거나 0 이하를 쓰면 **0** 이다: 겹쳐 그린 것과 같아지고, 화면이 그렇게
 *  적는다.  없는 간격을 지어내지 않는다 (§0.4).
 */

import { useStickyState } from '../lib/hooks'

/** 처음 보는 값.  자동이던 시절의 수(스캔마다 4~30)를 대신할 하나가 필요한데,
 *  Ω·cm² 로 재는 이 랩의 아크가 대개 수십이라 20 이면 한 칸이 눈에 보인다. */
export const STACK_GAP_DEFAULT = 20

export interface StackGap {
  /** 실제로 올릴 양.  못 읽으면 0 이다. */
  value: number
  /** 입력칸에 그대로 들어 있는 글자 (지우는 중일 수도 있다). */
  text: string
  set: (text: string) => void
}

/** 이격 간격 한 자리.  나이퀴스트 화면과 비교 화면이 **같은 열쇠**를 쓴다 —
 *  한쪽에서 정한 간격이 다른 쪽에서 딴 수가 되면 두 그림을 못 견준다. */
export function useStackGap(key = 'bml.stackGap'): StackGap {
  const [text, set] = useStickyState(key, String(STACK_GAP_DEFAULT))
  const parsed = Number(text)
  return {
    value: Number.isFinite(parsed) && parsed > 0 ? parsed : 0,
    text,
    set,
  }
}

/** 그 입력칸.  단위를 라벨에 적는다 — 20 이 Ω 인지 Ω·cm² 인지가 그림의 뜻을
 *  바꾸고, 단위 단추는 이 칸에서 멀리 떨어져 있다. */
export function StackGapField({ gap, unit }: { gap: StackGap; unit: string }) {
  return (
    <label className="row small" style={{ gap: 6, alignItems: 'center' }}>
      <span className="dim">이격 간격</span>
      <input
        type="number"
        min={0}
        step="any"
        value={gap.text}
        onChange={(event) => gap.set(event.target.value)}
        aria-label="이격 간격"
        title={`곡선 하나를 이웃보다 얼마나 올릴지 (${unit}) — 비우면 겹쳐 그립니다`}
        style={{ width: 92, borderColor: gap.value ? undefined : 'var(--danger)' }}
      />
      <span className="dim">{unit}</span>
    </label>
  )
}
