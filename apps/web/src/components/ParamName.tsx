/** 파라미터 이름을 첨자로 — 표에서도, 문장 속에서도.
 *
 *  표는 이름 하나가 한 칸이라 쉽다.  어려운 것은 **문장**이다: "물리적 한계에
 *  붙은 파라미터: CPE1_n, TL1_Wn, TL1_Wt" 같은 줄은 서버가 만들고, 그 안에
 *  이름이 섞여 있다.  표만 첨자로 바꾸면 같은 것이 한 화면에서 두 모습으로
 *  나온다.
 *
 *  **정규식으로 이름처럼 생긴 것을 찾지 않는다.**  이 피팅이 실제로 가진
 *  이름 목록을 받아서 그것만 바꾼다 — 회로 문자열(`L1-R0-p(R1,CPE1)-TL1`)이
 *  같은 문장에 섞여 있을 때, 이름처럼 생긴 조각을 골라 자르면 사람이 회로
 *  칸에 그대로 쳐 넣어야 하는 글자를 망가뜨린다.
 */

import type { ReactNode } from 'react'

import { splitSubscript } from '../lib/params'

/** 이름 하나를 첨자로. */
export function ParamName({ name }: { name: string }) {
  const [base, index] = splitSubscript(name)
  return <>{base}{index ? <sub>{index}</sub> : null}</>
}

/** 문장 안의 **아는 이름**만 첨자로 바꿔 그린다. */
export function ParamText({
  text,
  names,
}: {
  text: string
  /** 이 피팅이 가진 파라미터 이름들.  이 목록에 있는 것만 바꾼다. */
  names: string[]
}) {
  if (!text) return null
  // 긴 이름부터 찾는다 -- `TL1_W` 와 `TL1_Wn` 이 함께 있으면 짧은 쪽이 먼저
  // 걸려 `TL1_W` + "n" 으로 쪼개진다.
  const wanted = [...new Set(names)].filter(Boolean).sort((a, b) => b.length - a.length)
  if (!wanted.length) return <>{text}</>

  const out: ReactNode[] = []
  let at = 0
  let key = 0
  while (at < text.length) {
    let hitAt = -1
    let hit = ''
    for (const name of wanted) {
      const found = text.indexOf(name, at)
      if (found < 0) continue
      if (hitAt < 0 || found < hitAt || (found === hitAt && name.length > hit.length)) {
        hitAt = found
        hit = name
      }
    }
    if (hitAt < 0) {
      out.push(text.slice(at))
      break
    }
    if (hitAt > at) out.push(text.slice(at, hitAt))
    out.push(<ParamName key={key += 1} name={hit} />)
    at = hitAt + hit.length
  }
  return <>{out}</>
}
