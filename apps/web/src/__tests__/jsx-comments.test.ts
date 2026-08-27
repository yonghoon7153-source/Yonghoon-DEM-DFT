/** JSX 본문 자리에 `//` 주석을 두면 **글자가 되어 화면에 찍힌다.**
 *
 *  실제로 그랬다: 스캔 화면의 파라미터 드롭박스 위에
 *  `// **이름만으로는 무엇인지 모른다.** …` 다섯 줄이 그대로 카드에 박혀
 *  나왔다.  `{ … ? ( // 주석 <Field/> ) : null }` 이던 것을 `<div>` 로 감싸는
 *  순간 그 `//` 가 표현식 안이 아니라 **자식 노드**가 되기 때문이다.
 *
 *  타입 검사도 린트도 이것을 안 잡는다 — 문법으로는 멀쩡한 텍스트 노드다.
 *  그래서 여기서 소스를 훑는다.  화면을 그려 놓고 `//` 를 찾는 방법도 있지만,
 *  그러려면 모든 화면을 모든 상태로 그려야 한다.
 */

import { readFileSync, readdirSync, statSync } from 'node:fs'
import { join } from 'node:path'

import { describe, expect, it } from 'vitest'

function tsxFiles(root: string): string[] {
  const out: string[] = []
  for (const name of readdirSync(root)) {
    const path = join(root, name)
    if (statSync(path).isDirectory()) {
      out.push(...tsxFiles(path))
    } else if (name.endsWith('.tsx')) {
      out.push(path)
    }
  }
  return out
}

/** 앞이 닫는 태그(`>`)로 끝나고 뒤가 여는 태그(`<`)인 `//` 덩어리 — 그 자리의
 *  `//` 는 주석이 아니라 글자다.  `=>` 는 화살표 함수라 뺀다. */
function leaked(source: string): string[] {
  const lines = source.split('\n')
  const found: string[] = []
  for (let i = 0; i < lines.length; i += 1) {
    if (!/^\s*\/\//.test(lines[i]!)) continue
    if (i > 0 && /^\s*\/\//.test(lines[i - 1]!)) continue   // 덩어리의 첫 줄만
    let end = i
    while (end + 1 < lines.length && /^\s*\/\//.test(lines[end + 1]!)) end += 1
    const before = (lines[i - 1] ?? '').trimEnd()
    const after = (lines[end + 1] ?? '').trimStart()
    if (/[^=]>$/.test(before) && after.startsWith('<')) {
      found.push(`${i + 1}: ${lines[i]!.trim().slice(0, 60)}`)
    }
  }
  return found
}

describe('JSX 본문에 샌 주석', () => {
  it('화면 소스 어디에도 없다 — 있으면 그 글자가 카드에 찍힌다', () => {
    const offenders: string[] = []
    for (const path of tsxFiles(join(__dirname, '..'))) {
      const hits = leaked(readFileSync(path, 'utf8'))
      if (hits.length) offenders.push(`${path}\n  ${hits.join('\n  ')}`)
    }
    expect(offenders.join('\n')).toBe('')
  })

  it('무엇을 잡고 무엇을 넘기는지', () => {
    // 잡는다: 태그와 태그 사이의 `//`.
    expect(leaked('  </Field>\n  // 설명\n  <Field>')).toHaveLength(1)
    // 넘긴다: 표현식 안(`(` 뒤)의 `//` 는 진짜 주석이다.
    expect(leaked('  {list.length ? (\n    // 설명\n    <Field>')).toHaveLength(0)
    // 넘긴다: 화살표 함수 뒤.
    expect(leaked('  onClick={() =>\n    // 설명\n    <Field>')).toHaveLength(0)
    // 넘긴다: JSX 가 아닌 보통 코드.
    expect(leaked('  const a = 1\n  // 설명\n  const b = 2')).toHaveLength(0)
  })
})
