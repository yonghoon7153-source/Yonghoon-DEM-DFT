/** 사람이 한 줄에 적은 수들을 스윕 차례의 목록으로.
 *
 *  SOC (ADR 0038) 와 온도 (ADR 0039) 가 같은 입력을 쓴다.  둘 다 계측기가
 *  모르는 값이고, 둘 다 "스윕 차례대로 하나씩" 이라는 규칙이 같다.
 *
 *  실험 노트에 적히는 모양 그대로 받는다: `60, 50, 40 …` · `60 50 40` ·
 *  줄바꿈으로 나눈 것 · 엑셀에서 세로로 복사해 온 것.  적는 사람이 형식을
 *  외우게 하지 않는 것이 요점이다 — 형식이 틀렸다고 돌려보내면 다음부터는
 *  엑셀에서 옮겨 온다.
 *
 *  **등간격은 `(처음, 끝, 개수)` 로 줄여 쓸 수 있다.**  `(60, -20, 9)` 는
 *  60 부터 -20 까지 아홉 개, 곧 `60 50 40 30 20 10 0 -10 -20` 이다.  온도
 *  스윕이 대개 등간격이라 아홉 번 치는 일이 잦다.
 *
 *  괄호를 **요구한다**.  `60, 50, 40` 은 세 개짜리 목록이고 `(60, 40, 3)` 은
 *  범위다 — 괄호가 없으면 둘을 가를 방법이 없고, 잘못 갈리면 60·50·40 을
 *  적었는데 60·40 사이 세 점이 들어간다.
 *
 *  **빈 자리는 `null`** 이다 ("그 스윕은 모른다").  `-` 와 `?` 도 같게 읽는다.
 *  적었던 것을 지우는 길이 있어야 하고, 모르는 스윕 하나 때문에 전부를 못 적게
 *  하면 안 된다 (§0.4).
 *
 *  **숫자가 아닌 것은 삼키지 않는다.**  `bad` 로 돌려주고 화면이 그것을 적는다.
 *  조용히 버리면 열둘을 적었는데 열하나가 저장되고, 그때 축은 한 칸씩 밀린
 *  채로 멀쩡해 보인다.
 */

export interface ValueList {
  /** 적힌 차례 그대로.  스윕 수와 같아야 저장된다. */
  values: (number | null)[]
  /** 숫자로 못 읽은 토막들 — 화면이 그대로 보여 준다. */
  bad: string[]
  /** 범위 축약을 펼쳤으면 그 사실.  화면이 **되읽어 준다** — 아홉 개를 적었다고
   *  믿었는데 여덟 개가 들어가는 일이 이 축약에서 제일 생기기 쉽다. */
  expanded: boolean
}

export interface ParseOptions {
  /** 목록 머리의 이름표 — `SOC 0, 10` 처럼 쓰는 사람이 많다. */
  label?: RegExp
  /** 끝에 붙는 단위 — 단위지 값이 아니다 (`10%`, `60C`, `60°C`). */
  unit?: RegExp
}

/** `(처음, 끝, 개수)` — 앞뒤 공백은 봐주고, 안쪽은 쉼표나 공백으로 나눈다. */
const RANGE = /^\(\s*(-?[\d.eE+]+)\s*[,\s]\s*(-?[\d.eE+]+)\s*[,\s]\s*(\d+)\s*\)$/

const BLANK = new Set(['-', '?', '—', '–'])

export function parseValueList(text: string, options: ParseOptions = {}): ValueList {
  const range = text.trim().match(RANGE)
  if (range) return expandRange(range)

  const values: (number | null)[] = []
  const bad: string[] = []
  // 쉼표·공백·줄바꿈·탭·세미콜론 아무것으로나 나눈다.  엑셀에서 세로로 복사해
  // 오면 줄바꿈이고, 손으로 치면 쉼표다.
  for (const raw of text.split(/[\s,;]+/)) {
    const token = raw.trim()
    if (!token) continue
    if (options.label?.test(token)) continue
    if (BLANK.has(token)) {
      values.push(null)
      continue
    }
    const stripped = options.unit ? token.replace(options.unit, '') : token
    const number = Number(stripped)
    if (!stripped || !Number.isFinite(number)) {
      bad.push(token)
      continue
    }
    values.push(number)
  }
  return { values, bad, expanded: false }
}

function expandRange(match: RegExpMatchArray): ValueList {
  const first = Number(match[1])
  const last = Number(match[2])
  const count = Number(match[3])
  if (!Number.isFinite(first) || !Number.isFinite(last)) {
    return { values: [], bad: [match[0]], expanded: false }
  }
  if (count < 1) {
    return { values: [], bad: [match[0]], expanded: false }
  }
  if (count === 1) return { values: [first], bad: [], expanded: true }
  const step = (last - first) / (count - 1)
  const values: (number | null)[] = []
  for (let i = 0; i < count; i += 1) {
    // 12 자리로 자른다.  `(0, 0.3, 4)` 가 0.09999999999999999 을 내는 것을
    // 막을 뿐이고, 어떤 실측 온도·SOC 도 이 자리 아래에 있지 않다.
    values.push(Number((first + step * i).toPrecision(12)))
  }
  return { values, bad: [], expanded: true }
}

/** 펼친 결과를 사람이 읽을 한 줄로 — 되읽어 주는 데 쓴다. */
export function describeValues(values: (number | null)[], unit = ''): string {
  const shown = values.map((one) => (one === null ? '—' : String(one)))
  const tail = unit ? ` ${unit}` : ''
  if (shown.length <= 12) return shown.join(', ') + tail
  return `${shown.slice(0, 9).join(', ')} … ${shown[shown.length - 1]}${tail}`
    + ` (${values.length}개)`
}

/** 이 목록을 이 스캔에 적을 수 있는가.  못 적으면 **왜인지**를 돌려준다.
 *
 *  화면과 서버가 같은 규칙을 봐야 한다 — 서버는 어차피 422 로 막지만, 누르기
 *  전에 알려 주지 않으면 사람은 눌러 보고 나서야 안다.
 */
export function listProblem(list: ValueList, sweeps: number, what: string,
                            range?: { low: number; high: number; unit: string }): string {
  if (list.bad.length) {
    return `숫자로 읽을 수 없는 것이 있습니다: ${list.bad.slice(0, 5).join(' · ')}`
  }
  if (!list.values.length) return ''
  if (list.values.length !== sweeps) {
    return `스윕은 ${sweeps}개인데 ${list.values.length}개를 적었습니다 — `
      + `수가 같아야 어느 스윕의 ${what} 인지 정해집니다`
  }
  if (range) {
    const out = list.values.find(
      (one) => one !== null && !(one >= range.low && one <= range.high))
    if (out !== undefined && out !== null) {
      return `${what} 는 ${range.low}~${range.high}${range.unit} 사이여야 합니다: ${out}`
    }
  }
  return ''
}
