/** Number and unit formatting.
 *
 * Lab readings are compared by eye across rows, so significant figures matter
 * more than decimal places: 207.7 mAh/g and 5.2515 mAh should both read
 * cleanly without either being padded to the other's precision.
 */

export function num(value: number | null | undefined, digits = 4): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return '—'
  const magnitude = Math.abs(value)
  if (magnitude === 0) return '0'
  if (magnitude >= 1000) return value.toFixed(0)
  if (magnitude >= 100) return value.toFixed(Math.max(0, digits - 3))
  if (magnitude >= 10) return value.toFixed(Math.max(0, digits - 2))
  if (magnitude >= 1) return value.toFixed(Math.max(0, digits - 1))
  return value.toPrecision(Math.max(2, digits - 1))
}

/** 사람이 적은 그대로의 수 — 부동소수점 찌꺼기만 턴다.
 *
 * `num()` 과 다르다.  저쪽은 *측정값*을 일정한 유효숫자로 맞추는 것이고,
 * 여기는 "적힌 값을 그대로 보여 준다" 이다.  0.2C 를 "0.20C" 로, 205.9 mAh/g 를
 * "206" 으로 쓰면 사람이 넣지 않은 정밀도가 생기거나 값 자체가 달라진다.
 */
export function plain(value: number | null | undefined): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return '—'
  return String(Number(value.toFixed(6)))
}

export function pct(value: number | null | undefined, digits = 2): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return '—'
  return value.toFixed(digits)
}

export function cycleNumber(value: number | null | undefined): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return '—'
  return Number.isInteger(value) ? String(value) : value.toFixed(1)
}

export function bytes(value: number): string {
  if (value < 1024) return `${value} B`
  if (value < 1024 ** 2) return `${(value / 1024).toFixed(0)} KB`
  if (value < 1024 ** 3) return `${(value / 1024 ** 2).toFixed(1)} MB`
  return `${(value / 1024 ** 3).toFixed(2)} GB`
}

export function dateTime(value: string | null | undefined): string {
  if (!value) return '—'
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return value
  const pad = (n: number) => String(n).padStart(2, '0')
  return (
    `${parsed.getFullYear()}-${pad(parsed.getMonth() + 1)}-${pad(parsed.getDate())} ` +
    `${pad(parsed.getHours())}:${pad(parsed.getMinutes())}`
  )
}

export function duration(hours: number | null | undefined): string {
  if (hours === null || hours === undefined || !Number.isFinite(hours)) return '—'
  if (hours < 1) return `${(hours * 60).toFixed(0)}분`
  if (hours < 48) return `${hours.toFixed(1)}시간`
  return `${(hours / 24).toFixed(1)}일`
}

/** The axis title for a capacity basis, with proper superscripts. */
export function basisAxis(basis: string): string {
  switch (basis) {
    case 'mAh/g':
      return '비용량 (mAh g⁻¹)'
    case 'mAh/cm2':
      return '면적용량 (mAh cm⁻²)'
    case 'mAh/cm3':
      return '부피용량 (mAh cm⁻³)'
    case '%':
      return '용량 활용률 (%)'
    default:
      return '용량 (mAh)'
  }
}

export function basisUnit(basis: string): string {
  switch (basis) {
    case 'mAh/g':
      return 'mAh g⁻¹'
    case 'mAh/cm2':
      return 'mAh cm⁻²'
    case 'mAh/cm3':
      return 'mAh cm⁻³'
    case '%':
      return '%'
    default:
      return 'mAh'
  }
}

/** 이름이 mg 로 적은 질량.  **글자 하나 바꾸지 않았다** -- 이 규칙은 이 랩의
 *  파일 이름 수백 개를 이미 통과한 것이라, g 를 붙이면서 건드리지 않는다.
 *
 * 두께와 같은 이유로 `\b` 를 쓰지 않는다: `17.5mg_2` 의 `mg` 뒤는 밑줄이고,
 * 밑줄은 단어 문자라 경계가 아니다.
 * 앞 경계도 본다 (리뷰 #33): `17,5mg` 나 `1e-3mg` 처럼 지원하지 않는 표기의
 * **꼬리만** 떼어 5, 3 을 힌트로 보여 주면, 진짜 근거처럼 읽힌다.  숫자 토큰
 * 앞이 소수점·쉼표·지수·부호·숫자면 통째로 못 읽은 것이다.
 */
const MASS_MG = /(?<![\d.,eE+-])(\d+(?:\.\d+)?)\s*mg(?![a-z0-9])/gi

/** 이름이 g 로 적은 질량 -- mg 규칙보다 **훨씬 좁다**.
 *
 * `g` 는 한 글자이고 이름 어디에나 있다.  `mg` 는 그 자체로 거의 질량이지만
 * `g` 는 `NCM811g`, `2x3g`, `avg` 의 g 일 수 있고, 힌트가 틀리면 있느니만
 * 못하다 (`cellConfigFromName` 의 `symmetry` 와 같은 자리다).  그래서 셋을
 * 함께 요구한다:
 *
 *  1. **숫자 앞이 구분자**여야 한다 (줄 시작 · 공백 · `_` · `-` · 괄호).
 *     `NCM811g` 는 숫자가 글자에 붙어 있으므로 통째로 이름의 일부다.
 *  2. **`g` 앞이 숫자나 공백**이어야 한다.  `mg` · `kg` · `µg` · `ug` 의 g 가
 *     여기서 걸러진다 -- 접두를 하나씩 나열하지 않아도 된다.
 *  3. 뒤에 글자·숫자가 오면 안 된다 (`5gr`, `3g2`).  밑줄과 끝은 허용한다.
 *
 * 그리고 **크기까지 본다** (`G_RANGE`).  위 셋을 통과해도 `811 g` 는 이
 * 저장소가 다루는 전극의 질량이 아니다.  거절이지 추정이 아니므로 §0.4 에
 * 어긋나지 않는다 -- 못 읽으면 힌트가 안 뜰 뿐이고, 사람이 칸에 적으면 된다.
 */
const MASS_G = /(?:^|[\s_\-([])(\d+(?:\.\d+)?)\s*g(?![a-z0-9])/gi

/** g 로 적힌 값이 전극 질량으로 말이 되는 범위 (g).  0.1 mg ~ 5 g.
 *
 * 이 랩이 실제로 쓰는 값은 0.3 mg ~ 176 mg 이다.  넉넉하게 잡되 `811g` 나
 * `2024g` 같은 이름 조각은 확실히 떨어지는 자리에 뒀다. */
const G_RANGE = { min: 0.0001, max: 5 } as const

/** 이름이 말하는 질량 -- mg 로 환산한 값과, 이름에 **적힌 그대로**.
 *
 * 이 랩은 파일 이름 끝에 전극 질량을 적는다 (`..._4.6V_1_17.5mg`, 그리고
 * 사람에 따라 `..._0.0175g`).  그 숫자는 `.wrd` 가 모르는 유일한 값이라
 * (ADR 0003) 손으로 넣어야 하는데, 옆에 이름이 말하는 값을 적어 두면 오타가
 * 모든 mAh/g 를 조용히 바꾸기 전에 눈에 걸린다.
 *
 * 적힌 그대로를 함께 내는 이유는 **환산이 보이지 않으면 힌트가 거짓말처럼
 * 보이기 때문**이다: 이름에 `0.0175g` 라고 썼는데 화면이 `17.5mg` 만 보여
 * 주면, 어디서 온 수인지 모르는 사람은 그것을 다른 값으로 읽는다.
 *
 * 마지막 것이 이긴다 -- 이름이 질량을 둘 말하면 전극 자신의 것이 뒤에 온다.
 * mg 와 g 를 함께 훑고 **위치로** 고르므로, 어느 단위로 적었든 규칙이 같다.
 */
export function massHintFromName(
  name: string | null | undefined,
): { mg: number; wrote: string } | null {
  if (!name) return null
  const hits: { mg: number; wrote: string; at: number }[] = []
  const take = (mg: number, wrote: string, at: number) => {
    if (Number.isFinite(mg) && mg > 0) hits.push({ mg, wrote, at })
  }
  for (const match of name.matchAll(MASS_MG)) {
    take(Number(match[1]), `${match[1]} mg`, match.index ?? 0)
  }
  for (const match of name.matchAll(MASS_G)) {
    const grams = Number(match[1])
    if (!(grams >= G_RANGE.min && grams <= G_RANGE.max)) continue
    // 0.0175 * 1000 이 17.499999999999996 로 나오는 자리다.  힌트가 오타를
    // 잡으라고 있는 것인데 힌트 자신이 지저분하면 그 일을 못 한다.
    take(Number((grams * 1000).toPrecision(12)), `${match[1]} g`, match.index ?? 0)
  }
  if (!hits.length) return null
  // 두 단위를 따로 훑었으므로 **위치로** 고른다 -- 훑은 순서로 고르면 g 로
  // 적은 값이 늘 이기고, "마지막 것이 이긴다" 가 단위마다 달라진다.
  const last = hits.reduce((best, hit) => (hit.at >= best.at ? hit : best))
  return { mg: last.mg, wrote: last.wrote }
}

/** The mass written into a cell's name, in mg.  `massHintFromName` 의 숫자만. */
export function massFromName(name: string | null | undefined): number | null {
  return massHintFromName(name)?.mg ?? null
}

/** Thickness the file name mentions, in micrometres.
 *
 * Same bargain as `massFromName`: the instrument does not record how thick the
 * pellet was, so somebody types it -- and this lab already writes it into the
 * name (`260719_No1_55_70um_sym_01`).  Shown beside the field as a reference,
 * never filled in silently: a name is what somebody meant to call the file,
 * and a conductivity computed from a typo looks exactly like a measured one.
 *
 * The last match wins, as with mass: a name that mentions two thicknesses puts
 * the one being measured last. */
export function thicknessFromName(name: string | null | undefined): number | null {
  if (!name) return null
  let found: number | null = null
  // `\b` 가 아니라 `(?![a-z0-9])` 다.  밑줄은 JS 정규식에서 **단어 문자**라
  // `70um_sym` 의 `um` 뒤에는 단어 경계가 없다 — 이 랩의 이름이 거의 다 그
  // 모양이므로, `\b` 로 쓰면 힌트가 거의 안 뜬다.
  for (const match of name.matchAll(/(?<![\d.,eE+-])(\d+(?:\.\d+)?)\s*(um|µm|μm)(?![a-z0-9])/gi)) {
    const value = Number(match[1])
    if (Number.isFinite(value) && value > 0) found = value
  }
  return found
}

/** Cell configuration the file name mentions.
 *
 * `sym` for a symmetric cell, `full` for a full cell, `half` for a half cell.
 * `null` when the name does not say -- which is most names, and is why this is
 * a hint next to a control rather than the control's value.
 *
 * Word boundaries matter: `symmetry` is not `sym`, and a cell called
 * `LiFull_01` should not be read as a full cell because of a capital F. */
export function cellConfigFromName(
  name: string | null | undefined,
): 'sym' | 'full' | 'half' | null {
  if (!name) return null
  const text = name.toLowerCase()
  const has = (pattern: RegExp) => pattern.test(text)
  if (has(/(^|[^a-z])sym(m|metric|metrical)?([^a-z]|$)/)) return 'sym'
  if (has(/(^|[^a-z])half([^a-z]|$)/)) return 'half'
  if (has(/(^|[^a-z])full(cell)?([^a-z]|$)/)) return 'full'
  return null
}

/** The part of a cell name shared by its replicates.
 *
 * This lab names cells for what the experiment was, then adds which replicate
 * and how much it weighed: `4.6V_1_17.5mg`, `4.6V_2_18.1mg`.  Those two are
 * the same condition run twice, and grouping them is the question people
 * actually ask of the library — without having to create an experiment group
 * for every condition first.
 *
 * So trailing tokens that identify the *individual cell* come off, and
 * everything that identifies the *condition* stays:
 *
 *     4.6V_1_17.5mg            -> 4.6V
 *     4.0V_post_formation_18.9mg -> 4.0V_post_formation
 *     No_1_dry_011             -> No_1_dry
 *
 * Only trailing tokens are stripped.  `No_1_dry` keeps its `_1` because the
 * `dry` after it says the number is part of the name, not a replicate index —
 * and a rule that reached into the middle would merge `No_1_dry` with
 * `No_2_wet`.
 *
 * A name that strips away to nothing keeps its full self.  Returning "" would
 * put every all-numeric name in one nameless heap.
 */
export function nameFamily(name: string | null | undefined): string {
  if (!name) return ''
  let stem = name.trim()
  // `17.5mg` is the mass, `011` is the file sequence or the replicate index.
  const droppable = /[\s_-]+(?:\d+(?:\.\d+)?\s*mg|\d+)$/i
  while (droppable.test(stem)) {
    stem = stem.replace(droppable, '')
  }
  return stem || name.trim()
}

/** Qualitative palette, ordered so adjacent series stay distinguishable and
 *  no pair collides under the common forms of colour blindness. */
export const SERIES_COLORS = [
  '#1d4ed8', '#ea580c', '#059669', '#7c3aed', '#db2777',
  '#0891b2', '#ca8a04', '#4b5563', '#2563eb', '#e11d48',
  '#15803d', '#b45309', '#6d28d9', '#0e7490', '#9f1239',
]

export function seriesColor(index: number): string {
  return SERIES_COLORS[index % SERIES_COLORS.length] as string
}

/** A cycle-number spec like `1,3,10-20` expanded to numbers. */
export function parseCycleSpec(spec: string, available: number[]): number[] {
  const trimmed = spec.trim().toLowerCase()
  if (!trimmed || trimmed === 'all' || trimmed === '전체') return available
  const wanted = new Set<number>()
  for (const part of trimmed.split(',')) {
    const piece = part.trim()
    if (!piece) continue
    if (piece.includes('-')) {
      const [from, to] = piece.split('-', 2).map((v) => Number.parseInt(v, 10))
      if (Number.isFinite(from) && Number.isFinite(to)) {
        for (let n = Math.min(from!, to!); n <= Math.max(from!, to!); n += 1) wanted.add(n)
      }
    } else {
      const value = Number.parseInt(piece, 10)
      if (Number.isFinite(value)) wanted.add(value)
    }
  }
  return available.filter((n) => wanted.has(n))
}

/** Evenly spaced picks from a list — "show me 8 cycles across the run". */
export function spread(values: number[], count: number): number[] {
  if (values.length <= count) return values
  const picks: number[] = []
  for (let i = 0; i < count; i += 1) {
    const index = Math.round((i * (values.length - 1)) / (count - 1))
    const value = values[index]
    if (value !== undefined && !picks.includes(value)) picks.push(value)
  }
  return picks
}
