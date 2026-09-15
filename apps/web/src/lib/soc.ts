/** 사람이 한 줄에 적은 SOC 를 스윕 차례의 목록으로 (ADR 0038).
 *
 *  실험 노트에 적히는 모양 그대로 받는다: `SOC 0, 10, 20 …` · `0 10 20` ·
 *  `0%, 10%, 20%` · 줄바꿈으로 나눈 것.  적는 사람이 형식을 외우게 하지 않는
 *  것이 요점이다 — 형식이 틀렸다고 돌려보내면 다음부터는 엑셀에서 옮겨 온다.
 *
 *  **빈 자리는 `null`** 이다 ("그 스윕은 모른다").  `-` 와 `?` 도 같게 읽는다.
 *  적었던 것을 지우는 길이 있어야 하고, 모르는 스윕 하나 때문에 전부를 못 적게
 *  하면 안 된다 (§0.4).
 *
 *  **숫자가 아닌 것은 삼키지 않는다.**  `bad` 로 돌려주고 화면이 그것을 적는다.
 *  조용히 버리면 열둘을 적었는데 열하나가 저장되고, 그때 SOC 축은 한 칸씩
 *  밀린 채로 멀쩡해 보인다.
 */

export interface SocList {
  /** 적힌 차례 그대로.  스윕 수와 같아야 저장된다. */
  values: (number | null)[]
  /** 숫자로 못 읽은 토막들 — 화면이 그대로 보여 준다. */
  bad: string[]
}

/** 목록의 머리에 붙는 이름표.  `SOC 0, 10` 처럼 쓰는 사람이 많다. */
const LABEL = /^soc$|^soc:$|^%$/i

export function parseSocList(text: string): SocList {
  const values: (number | null)[] = []
  const bad: string[] = []
  // 쉼표·공백·줄바꿈·탭 아무것으로나 나눈다.  엑셀에서 세로로 복사해 오면
  // 줄바꿈이고, 손으로 치면 쉼표다.
  for (const raw of text.split(/[\s,;]+/)) {
    const token = raw.trim()
    if (!token) continue
    if (LABEL.test(token)) continue
    if (token === '-' || token === '?' || token === '—') {
      values.push(null)
      continue
    }
    // 끝의 % 는 단위지 값이 아니다.
    const number = Number(token.replace(/%$/, ''))
    if (!Number.isFinite(number)) {
      bad.push(token)
      continue
    }
    values.push(number)
  }
  return { values, bad }
}

/** 이 목록을 이 스캔에 적을 수 있는가.  못 적으면 **왜인지**를 돌려준다.
 *
 *  화면과 서버가 같은 규칙을 봐야 한다 — 서버는 어차피 422 로 막지만, 누르기
 *  전에 알려 주지 않으면 사람은 눌러 보고 나서야 안다.
 */
export function socProblem(list: SocList, sweeps: number): string {
  if (list.bad.length) {
    return `숫자로 읽을 수 없는 것이 있습니다: ${list.bad.slice(0, 5).join(' · ')}`
  }
  if (!list.values.length) return ''
  if (list.values.length !== sweeps) {
    return `스윕은 ${sweeps}개인데 ${list.values.length}개를 적었습니다 — `
      + '수가 같아야 어느 스윕의 SOC 인지 정해집니다'
  }
  const out = list.values.find(
    (one) => one !== null && !(one >= 0 && one <= 100))
  if (out !== undefined && out !== null) {
    return `SOC 는 0~100 사이여야 합니다: ${out}`
  }
  return ''
}

/** 적어 둔 SOC 를 화면에 적는 말.  없으면 빈 문자열이다. */
export function socLabel(value: number | null | undefined): string {
  return value === null || value === undefined ? '' : `SOC ${value}%`
}
