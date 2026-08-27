/** 표의 왼쪽 몇 열을 붙여 둔다 — 오른쪽으로 밀어도 "누구의 줄인가" 가 남게.
 *
 *  셀 라이브러리는 첫 열만 붙이면 됐고, 그것은 CSS 한 줄로 끝난다
 *  (`.table-wrap.pin-first`, `left: 0`).  스캔의 스윕 표는 다르다: 붙여야 할
 *  것이 아홉 열(`#` 부터 `점` 까지)이고, 두 번째 열부터는 `left` 가 **앞선
 *  열들의 폭 합**이라야 한다.  그 폭은 이름 길이와 글꼴에 따라 매번 다르므로
 *  CSS 에 적을 수가 없다 — 상수로 적어 두면 이름이 긴 파일에서 열이 서로
 *  겹쳐 글자가 두 겹이 된다.
 *
 *  그래서 그린 뒤에 재서 붙인다.  머리 줄의 칸들이 실제로 어디에 있는지
 *  (`offsetLeft`) 읽어 그 값을 그 열의 모든 칸에 넣는다.
 *
 *  **재는 시점이 `useLayoutEffect` 인 이유**: `useEffect` 로 두면 한 프레임
 *  동안 `left` 가 0 인 채로 그려져 아홉 열이 왼쪽 끝에 겹쳐 보였다가 제자리를
 *  찾는다 — 표가 열릴 때마다 한 번씩 깜빡인다.
 */

import { useLayoutEffect } from 'react'

/** 붙인 칸에 붙는 표시.  실제 `left` 는 여기서 넣고, 배경·경계선은 CSS 가 한다. */
const PINNED = 'pin-col'
const EDGE = 'pin-edge'

/** 왼쪽 `count` 열을 붙인다.
 *
 *  `deps` 가 바뀌면 다시 잰다 — 열의 수나 내용이 바뀌면 폭도 바뀌기 때문이다.
 *  창 크기도 본다: 표가 좁아지면 칸 폭이 줄어 붙여 둔 자리가 어긋난다.
 */
export function usePinnedColumns(
  box: { current: HTMLElement | null },
  count: number,
  deps: unknown[] = [],
): void {
  useLayoutEffect(() => {
    const node = box.current
    if (!node) return
    const table = node.querySelector('table')
    if (!table) return

    const apply = () => {
      const head = table.querySelector('thead tr')
      if (!head) return
      const heads = [...head.children] as HTMLElement[]
      // 실제로 붙일 수 있는 만큼만.  열이 count 보다 적을 수 있다.
      const wanted = Math.min(count, heads.length)
      // **폭을 더해서 자리를 낸다 — `offsetLeft` 를 읽으면 안 된다.**
      //
      // 처음엔 `offsetLeft` 로 쟀는데, 한 번 `position: sticky` 를 걸고 나면
      // 그 값이 **붙어 있는 자리**를 돌려준다.  `ResizeObserver` 가 다시 잴
      // 때마다 그 값이 다음 `left` 로 들어가서, 두어 번 만에 앞 열들이 표
      // 한가운데로 기어들어갔다 (실제로 `#`·`이름` 이 `R₀` 옆에 가 있었다).
      // 칸의 **폭**은 붙어 있든 아니든 같으므로 그것만 더한다.
      let at = 0
      const lefts = heads.slice(0, wanted).map((cell) => {
        const here = at
        at += cell.getBoundingClientRect().width
        return here
      })
      for (const row of table.querySelectorAll('tr')) {
        const cells = [...row.children] as HTMLElement[]
        cells.forEach((cell, index) => {
          if (index < wanted) {
            cell.classList.add(PINNED)
            cell.classList.toggle(EDGE, index === wanted - 1)
            cell.style.left = `${lefts[index] ?? 0}px`
            return
          }
          // 열이 줄었을 때 옛 표시가 남으면 가운데 열이 왼쪽에 붙어 있는다.
          cell.classList.remove(PINNED, EDGE)
          cell.style.left = ''
        })
      }
    }

    // 붙은 구간의 경계선은 **밀었을 때만** 긋는다.  안 민 상태에서도 그으면
    // 표가 두 덩어리로 갈린 것처럼 보이는데, 그때는 갈릴 이유가 없다.
    const edge = () => node.classList.toggle('pin-scrolled', node.scrollLeft > 0)
    edge()
    node.addEventListener('scroll', edge, { passive: true })

    apply()
    // 표가 좁아지면 칸 폭이 줄어 붙여 둔 자리가 어긋난다.  `ResizeObserver` 가
    // 없는 환경(오래된 jsdom)에서는 한 번 재고 만다 — 붙긴 붙는다.
    if (typeof ResizeObserver === 'undefined') {
      return () => node.removeEventListener('scroll', edge)
    }
    const watch = new ResizeObserver(() => apply())
    watch.observe(table)
    return () => {
      node.removeEventListener('scroll', edge)
      watch.disconnect()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [box, count, ...deps])
}
