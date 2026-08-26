/** 스타일시트가 지켜야 할 것 — 그림으로만 드러나는 종류의 사고를 막는다.
 *
 *  실제로 난 사고: `.dim { opacity: 0.45 }` 가 파일 뒤쪽(F&Q 구역)에 하나 더
 *  생겼다. `.dim` 은 표에서 회색 칸에 쓰는 글자색 유틸리티라 관계셀 칸이
 *  `<td class="text dim">` 이었고, `opacity < 1` 은 **쌓임 맥락(stacking
 *  context)** 을 만든다. 그래서 그 칸 안에서 뜬 셀 고르기 창이
 *
 *    1. 반투명해져 밑의 표가 비쳐 보이고,
 *    2. `z-index: 60` 인데도 `z-index: 1` 인 붙박이 표 머리 **아래**로 깔렸다.
 *       — 60 은 그 `<td>` 안에서만 세는 수라서 표 머리를 못 이긴다.
 *
 *  둘 다 "겹쳐 보인다" 로만 보이고, CSS 어디를 봐야 하는지는 화면이 말해 주지
 *  않는다. 그래서 여기서 센다.
 */

import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'

import { describe, expect, it } from 'vitest'

// vitest 는 `apps/web` 에서 돈다 (vite root).
const css = readFileSync(resolve(process.cwd(), 'src/styles/app.css'), 'utf-8')

/** 주석을 뺀 본문 — 주석 속의 예시가 규칙으로 세어지지 않게. */
const body = css.replace(/\/\*[\s\S]*?\*\//g, '')

/** `.dim` 처럼 표 칸에 그대로 붙는 글자 유틸리티들.
 *
 *  이들은 **글자만** 바꿔야 한다. 어느 것이든 조상이 될 수 있고, 조상이
 *  쌓임 맥락을 만들면 그 안에서 뜬 창이 화면 맨 위로 못 올라간다.
 */
const TEXT_UTILITIES = ['dim', 'faint', 'small', 'tiny', 'nowrap', 'mono', 'text']

/** 쌓임 맥락을 만들거나 잘라 내는 속성들. */
const DANGEROUS = /(^|[;{\s])(opacity|transform|filter|backdrop-filter|perspective|contain|isolation|will-change|mix-blend-mode|position)\s*:/

describe('app.css', () => {
  it.each(TEXT_UTILITIES)('.%s 는 글자만 바꾼다 — 쌓임 맥락을 만들지 않는다', (name) => {
    // 이 클래스를 **달고 있는 요소**에 걸리는 규칙 전부.  `.dim` 도 `td.dim`
    // 도 `tbody td.text` 도 같은 요소에 붙으므로 다 센다 -- 좁은 선택자로
    // 우회해서 붙이는 것을 놓치지 않으려는 것이다.
    const blocks = [...body.matchAll(/([^{}]+)\{([^{}]*)\}/g)]
      .filter(([, selectors]) => (selectors ?? '').split(',')
        .some((one) => one.trim().endsWith(`.${name}`)))
      .map(([, , rules]) => rules ?? '')

    expect(blocks.length).toBeGreaterThan(0)
    for (const rules of blocks) {
      expect(rules, `.${name} 에 위험한 속성이 붙었습니다`).not.toMatch(DANGEROUS)
    }
  })

  it('창은 표 머리보다 위에 있다 — z-index 를 눈으로 대조한다', () => {
    const zOf = (selector: string) => {
      const found = body.match(
        new RegExp(`${selector}\\s*\\{[^{}]*z-index:\\s*(\\d+)`))
      return found ? Number(found[1]) : null
    }
    const backdrop = zOf('\\.modal-backdrop')
    expect(backdrop).not.toBeNull()
    // 표 머리(붙박이)와 고정 열, 상단 막대보다 위여야 한다.
    expect(backdrop!).toBeGreaterThan(zOf('thead th')!)
    expect(backdrop!).toBeGreaterThan(zOf('\\.topbar')!)
  })
})
