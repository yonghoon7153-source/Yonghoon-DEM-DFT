/** 이 브라우저가 마지막으로 고른 DRT 벌점 λ.
 *
 * 상세 화면과 비교 화면이 **같은 λ 를 봐야 한다.**  다르면 같은 스펙트럼의
 * γ 가 두 화면에서 다르게 생기고, 그 둘을 나란히 놓는 것이 비교 화면의 일이라
 * 거기서 곧바로 어긋난다.  그래서 값이 사는 자리를 한 군데로 둔다.
 *
 * 기본값을 하나로 못 박지 않는 이유는 그 값이 사람마다·시료마다 다르기
 * 때문이고, 기억하면 그 사람의 값이 곧 기본이 된다.  아직 아무것도 안
 * 골랐으면 1e-5 에서 시작한다 — 실측으로 이 랩이 쓰는 자리다.
 */

export const LAMBDA_KEY = 'bml.drt.lambda'
export const FIRST_LAMBDA = 1e-5

export function rememberedLambda(): number {
  try {
    const saved = Number(window.localStorage.getItem(LAMBDA_KEY))
    return Number.isFinite(saved) && saved > 0 ? saved : FIRST_LAMBDA
  } catch {
    // 사생활 보호 창에서는 읽는 것만으로 던진다.  기억을 못 하는 것은
    // 불편이지만, 그것 때문에 DRT 가 안 뜨면 고장이다.
    return FIRST_LAMBDA
  }
}

export function rememberLambda(value: number): void {
  try {
    window.localStorage.setItem(LAMBDA_KEY, String(value))
  } catch {
    /* 못 적어도 이번 화면은 그대로 돈다 */
  }
}

/** 적어 둔 λ 에 가장 가까운 자리.  로그 자로 잰다 — λ 는 10배씩 움직인다. */
export function nearestLambdaIndex(values: number[], want: number): number {
  let best = 0
  let gap = Infinity
  values.forEach((value, index) => {
    if (!(value > 0)) return
    const distance = Math.abs(Math.log10(value) - Math.log10(want))
    if (distance < gap) {
      gap = distance
      best = index
    }
  })
  return best
}
