/** Korean renderings of the explanations the API returns.
 *
 * The backend keeps its reasons in English: they are part of the API
 * contract, they appear in the CLI and in logs, and `wrdkit` has no business
 * knowing who is reading it.  Translation belongs here, at the point of
 * display, and falls through to the original text whenever a phrasing is not
 * recognised — an untranslated sentence is far better than a missing one.
 */

type Rule = [RegExp, (match: RegExpMatchArray) => string]

const KNEE_REASONS: Rule[] = [
  // 기준끼리 갈렸다는 꼬리표는 문장 뒤에 붙는다 — 앞부분을 먼저 번역하고
  // 꼬리표를 다시 붙인다.  이게 없으면 문장 전체가 어느 규칙에도 안 맞아
  // 통째로 영어로 나간다.
  [
    /^(.*); another criterion puts it at cycle ([\d.]+)$/,
    (m) => `${apply(KNEE_REASONS, m[1]!)} · 다른 기준은 ${m[2]}번을 짚습니다`,
  ],
  [
    /^retention crossed (\S+)% at cycle ([\d.]+)$/,
    (m) => `유지율이 ${m[2]}번 사이클에서 ${m[1]}% 를 통과했습니다`,
  ],
  [
    /^capacity never fell below (\S+)% \(lowest ([\d.]+)%\)$/,
    (m) => `유지율이 ${m[1]}% 아래로 내려간 적이 없습니다 (최저 ${m[2]}%)`,
  ],
  [
    /^fade rate steepens ([\d.]+)x at cycle ([\d.]+) \(([-\d.]+) -> ([-\d.]+) %\/cycle\)$/,
    (m) => `${m[2]}번 사이클에서 열화율이 ${m[1]}배로 급해집니다 (${m[3]} → ${m[4]} %/cycle)`,
  ],
  [
    /^fade rate reached (\S+)x the early-life rate \(([-\d.]+) vs ([-\d.]+) %\/cycle\) at cycle ([\d.]+)$/,
    (m) => `${m[4]}번 사이클에서 열화율이 초기의 ${m[1]}배에 도달했습니다 (${m[2]} vs ${m[3]} %/cycle)`,
  ],
  [
    /^fade rate never reached (\S+)x the early-life rate$/,
    (m) => `열화율이 초기의 ${m[1]}배에 도달한 적이 없습니다`,
  ],
  [
    /^fade rate never stayed at (\S+)x the early-life rate$/,
    (m) => `열화율이 초기의 ${m[1]}배를 넘은 채로 머무른 적이 없습니다`,
  ],
  [
    /^fade steepens at cycle ([\d.]+) \(([-+\d.]+) -> ([-+\d.]+) %\/cycle\) and eases off again from cycle ([\d.]+) \(([-+\d.]+) %\/cycle\)$/,
    (m) =>
      `${m[1]}번 사이클에서 열화가 급해졌다가 (${m[2]} → ${m[3]} %/cycle) ` +
      `${m[4]}번부터 다시 완만해집니다 (${m[5]} %/cycle)`,
  ],
  [
    /^fade begins at cycle ([\d.]+) \(([-+\d.]+) -> ([-+\d.]+) %\/cycle\)$/,
    (m) => `${m[1]}번 사이클에서 열화가 시작됩니다 (${m[2]} → ${m[3]} %/cycle)`,
  ],
  [
    /^only ([\d.]+)% is lost after cycle ([\d.]+) \(needs ([\d.]+)%\), and a line bent there fits no better than a straight one$/,
    (m) =>
      `${m[2]}번 이후로 잃는 것이 ${m[1]}% 뿐이고 (${m[3]}% 이상 필요), ` +
      `거기서 꺾은 선이 곧은 선보다 잘 맞지도 않습니다`,
  ],
  [
    /^only ([\d.]+)% is lost after cycle ([\d.]+) \(needs ([\d.]+)%\)$/,
    (m) => `${m[2]}번 이후로 잃는 것이 ${m[1]}% 뿐입니다 (${m[3]}% 이상이어야 knee 로 인정)`,
  ],
  [
    /^the rate does steepen, but only ([\d.]+)% is lost afterwards \(needs ([\d.]+)%\)$/,
    (m) => `열화율은 급해지지만 그 뒤로 잃는 것이 ${m[1]}% 뿐입니다 (${m[2]}% 이상 필요)`,
  ],
  [
    /^curvature peaks at cycle ([\d.]+) but only ([\d.]+)% is lost afterwards \(needs ([\d.]+)%\)$/,
    (m) => `${m[1]}번에서 곡률이 가장 크지만 그 뒤로 잃는 것이 ${m[2]}% 뿐입니다 (${m[3]}% 이상 필요)`,
  ],
  [
    /^a bent line fits no better than a straight one$/,
    () => '꺾은 선이 곧은 선보다 더 잘 맞지 않습니다 — 잡음일 가능성이 큽니다',
  ],
  [
    /^the rate steepens around cycle ([\d.]+), but a line bent there fits no better than a straight one$/,
    (m) => `${m[1]}번 부근에서 열화율이 급해지지만, 거기서 꺾은 선이 곧은 선보다 잘 맞지 않습니다`,
  ],
  [
    /^curvature peaks at cycle ([\d.]+), but a line bent there fits no better than a straight one$/,
    (m) => `${m[1]}번에서 곡률이 가장 크지만, 거기서 꺾은 선이 곧은 선보다 잘 맞지 않습니다`,
  ],
  [
    /^neither of the two best break points accelerates the fade$/,
    () => '가장 잘 맞는 두 절점 어디에서도 열화가 가속되지 않습니다',
  ],
  [
    /^a three-line fit needs at least (\d+) cycles, has (\d+)$/,
    (m) => `세 직선으로 보려면 사이클이 ${m[1]}개 이상이어야 합니다 (현재 ${m[2]}개)`,
  ],
  [/^no three-line break point fits$/, () => '세 직선으로도 맞는 절점이 없습니다'],
  [
    /^fade steepens at cycle ([\d.]+) \(([-+\d.]+) -> ([-+\d.]+) %\/cycle\)$/,
    (m) => `${m[1]}번 사이클에서 열화가 급해집니다 (${m[2]} → ${m[3]} %/cycle)`,
  ],
  [
    /^cycle ([\d.]+) bends, but only (\d+) cycles follow it and ([\d.]+)% has been lost so far -- at this rate the ([\d.]+)% that makes it a knee needs about (\d+)$/,
    (m) =>
      `${m[1]}번에서 꺾이지만 그 뒤가 ${m[2]} 사이클뿐이고 아직 ${m[3]}% 를 잃었습니다 — ` +
      `이 속도라면 knee 로 인정하는 ${m[4]}% 까지 ${m[5]} 사이클쯤 더 필요합니다`,
  ],
  [
    /^fell below (\S+)% at cycle ([\d.]+), the last cycle in the record -- nothing follows to confirm it$/,
    (m) => `기록의 마지막 사이클인 ${m[2]}번에서 ${m[1]}% 아래로 내려갔습니다 — 확인할 뒤가 없습니다`,
  ],
  [
    /^no usable cycle at or after cycle (\d+); the record ends at cycle (\d+)$/,
    (m) => `${m[1]}번 이후로 쓸 수 있는 사이클이 없습니다 (기록은 ${m[2]}번에서 끝납니다)`,
  ],
  [/^maximum curvature at cycle ([\d.]+)$/, (m) => `${m[1]}번 사이클에서 곡률이 가장 큽니다`],
  [
    /^curvature peaks at cycle ([\d.]+) but fade accelerates only ([\d.]+)x there \(needs ([\d.]+)x\)$/,
    (m) =>
      `${m[1]}번에서 곡률이 가장 크지만 거기서 가속이 ${m[2]}배뿐입니다 ` +
      `(${m[3]}배 이상이어야 knee 로 인정)`,
  ],
  [
    /^dipped below (\S+)% at cycle ([\d.]+) but recovered$/,
    (m) => `${m[2]}번 사이클에서 ${m[1]}% 아래로 내려갔다가 회복했습니다`,
  ],
  [
    /^fade accelerates only ([\d.]+)x \(needs ([\d.]+)x\)$/,
    (m) => `가속이 ${m[1]}배뿐입니다 (${m[2]}배 이상이어야 knee 로 인정)`,
  ],
  [
    /^fade does not accelerate after the best break point$/,
    () => '가장 잘 맞는 절점 이후로도 열화가 가속되지 않습니다',
  ],
  [/^capacity is not fading$/, () => '용량이 감소하지 않습니다'],
  [/^needs at least (\d+) cycles, has (\d+)$/, (m) => `사이클이 ${m[2]}개뿐입니다 (${m[1]}개 이상 필요)`],
  [/^series too short after edge trimming$/, () => '가장자리를 제외하면 데이터가 너무 짧습니다'],
  [/^no complete cycles$/, () => '완료된 사이클이 없습니다'],
]

const EVIDENCE: Rule[] = [
  [/^state was set by hand on the sample$/, () => '셀에 상태를 직접 지정했습니다'],
  [
    /^the record reaches the step after the cycling loop$/,
    () => '기록이 사이클 루프 다음 스텝까지 도달했습니다',
  ],
  [
    /^(\d+) of (\d+) planned cycles completed$/,
    (m) => `계획 ${m[2]} 사이클 중 ${m[1]} 사이클을 마쳤습니다`,
  ],
  [
    /^only (\d+) of (\d+) planned cycles are present$/,
    (m) => `계획 ${m[2]} 사이클 중 ${m[1]} 사이클만 있습니다`,
  ],
  [/^cycle (\d+) is cut off mid-step$/, (m) => `${m[1]}번 사이클이 스텝 도중에 잘렸습니다`],
  [
    /^last sample is (.+?) old, under (.+)$/,
    (m) => `마지막 샘플이 ${duration(m[1]!)} 전입니다 (${window_(m[2]!)} 이내)`,
  ],
  [
    /^nothing logged for (.+?) even though the record ends mid-cycle - the test stopped, or it continued in a file that is not here$/,
    (m) =>
      `기록이 사이클 도중에 끝났는데도 ${duration(m[1]!)} 동안 아무것도 기록되지 않았습니다 — ` +
      `실험이 멈췄거나, 여기 없는 파일로 이어졌습니다`,
  ],
  [/^nothing logged for (.+)$/, (m) => `${duration(m[1]!)} 동안 아무것도 기록되지 않았습니다`],
  [
    /^the file carries no schedule and no partial cycle to judge by$/,
    () => '판단할 스케줄도, 잘린 사이클도 없습니다',
  ],
]

const RETENTION_NOTES: Rule[] = [
  [/^cycle (\d+) vs cycle (\d+)$/, (m) => `${m[1]}번 사이클 vs 기준 ${m[2]}번 사이클`],
  [
    /^cycle (\d+) vs cycle (\d+) - cycle (\d+) is not in this record, so retention is measured from the earliest cycle available$/,
    (m) =>
      `${m[1]}번 사이클 vs ${m[2]}번 사이클 — ${m[3]}번 사이클이 이 기록에 없어 ` +
      `가장 이른 사이클을 기준으로 계산했습니다`,
  ],
]

const CELL_NOTES: Rule[] = [
  [/^entered directly$/, () => '직접 입력'],
  [
    /^current collector mass exceeds total mass$/,
    () => '집전체 질량이 총 질량보다 큽니다',
  ],
  [/^π x \((.+) mm \/ 2\)²$/, (m) => `π × (${m[1]} mm / 2)²`],
  [
    /^([\d.]+) mg x ([\d.]+) mAh\/g$/,
    (m) => `${m[1]} mg × ${m[2]} mAh/g`,
  ],
  [
    /^([\d.]+) mg \(after ([\d.]+) mg collector\) x ([\d.]+) wt%(?: from (.+))?$/,
    (m) =>
      `${m[1]} mg (집전체 ${m[2]} mg 제외) × ${m[3]} wt%` + (m[4] ? ` — ${m[4]}` : ''),
  ],
  [
    /^([\d.]+) mg x ([\d.]+) wt%(?: from (.+))?$/,
    (m) => `${m[1]} mg × ${m[2]} wt%` + (m[3] ? ` — ${m[3]}` : ''),
  ],
  [
    /^([\d.]+) mg x 100 wt% \(no composition given - assuming the whole electrode is active material\)$/,
    (m) => `${m[1]} mg × 100 wt% — 조성이 없어 전극 전체를 활물질로 가정했습니다`,
  ],
  // 집전체를 뺀 뒤 조성이 없는 조합.  위 두 규칙 어느 쪽에도 맞지 않아
  // 영어 그대로 나가고 있었다 — 흔한 입력인데도.
  [
    /^([\d.]+) mg \(after ([\d.]+) mg collector\) x 100 wt% \(no composition given - assuming the whole electrode is active material\)$/,
    (m) =>
      `${m[1]} mg (집전체 ${m[2]} mg 제외) × 100 wt% — 조성이 없어 전극 전체를 활물질로 가정했습니다`,
  ],
  [
    /^the composition names no active material(?: - none of (.+) is a known active material)?; enter the active wt% to use mAh\/g$/,
    (m) =>
      '조성에 활물질이 없습니다' +
      (m[1] ? ` — ${m[1]} 를 활물질로 알아보지 못했습니다` : '') +
      '. mAh/g 를 쓰려면 활물질 wt% 를 입력하세요',
  ],
  [
    /^directly entered active mass is not positive - ignored$/,
    () => '직접 입력한 활물질 질량이 0 이하라 무시했습니다',
  ],
  [/^([\d.]+) cm² x ([\d.]+) µm$/, (m) => `${m[1]} cm² × ${m[2]} µm`],
]

const BASIS_REASONS: Record<string, string> = {
  'active mass not set': '활물질 질량이 없습니다',
  'electrode area not set': '전극 면적이 없습니다',
  'electrode area and thickness not set': '전극 면적과 두께가 없습니다',
  'active mass and nominal specific capacity not set': '활물질 질량과 공칭 비용량이 없습니다',
  unavailable: '사용할 수 없습니다',
}

const COMPOSITION_PROBLEMS: Rule[] = [
  [/^weight percentages add up to ([\d.]+), not 100$/, (m) => `wt% 합이 ${m[1]} 입니다 (100 이 아님)`],
  [/^a component has a negative weight percent$/, () => '음수 wt% 가 있습니다'],
  [/^no component is marked as the active material$/, () => '활물질로 지정된 성분이 없습니다'],
  [/^the active material is 0 wt%$/, () => '활물질이 0 wt% 입니다'],
  [/^a component name is repeated$/, () => '성분 이름이 중복됩니다'],
]

function duration(text: string): string {
  return text
    .replace(/^([\d.]+) h$/, '$1시간')
    .replace(/^([\d.]+) days$/, '$1일')
    .replace(/^([\d.]+) months$/, '$1개월')
}

function window_(text: string): string {
  return text
    .replace(/^two cycle times \(([\d.]+) h\)$/, '사이클 2회분($1시간)')
    .replace(/^([\d.]+) h$/, '$1시간')
}

/** Phrases no rule matched.
 *
 * Falling through is deliberate — a sentence in English beats a missing one —
 * but a silent fallthrough is how an English sentence ends up shipped in a
 * Korean panel for months.  Every unmatched phrase is recorded, and announced
 * once while developing, so a new backend wording is noticed the first time it
 * appears rather than the first time somebody complains. */
const untranslated = new Set<string>()

function passThrough(text: string): string {
  if (!untranslated.has(text)) {
    untranslated.add(text)
    if (typeof process !== 'undefined' && process.env['NODE_ENV'] === 'development') {
      console.warn(`[i18n] 번역 규칙이 없습니다: ${JSON.stringify(text)}`)
    }
  }
  return text
}

function apply(rules: Rule[], text: string): string {
  for (const [pattern, render] of rules) {
    const match = text.match(pattern)
    if (match) return render(match)
  }
  return passThrough(text)
}

export const ko = {
  kneeReason: (text: string) => apply(KNEE_REASONS, text),
  retentionNote: (text: string) => apply(RETENTION_NOTES, text),
  evidence: (text: string) => apply(EVIDENCE, text),
  cellNote: (text: string) => apply(CELL_NOTES, text),
  compositionProblem: (text: string) => apply(COMPOSITION_PROBLEMS, text),
  basisReason: (text: string) => BASIS_REASONS[text] ?? passThrough(text),
  /** Phrases that fell through untranslated, for tests and for the console. */
  untranslated: () => [...untranslated],
  stateTarget: (text: string) =>
    ({ running: '구동 중', finished: '종료', unknown: '불명' })[text] ?? text,
  signal: (text: string) =>
    ({
      manual: '수동',
      schedule: '스케줄',
      'cycle count': '사이클 수',
      'partial cycle': '잘린 사이클',
      recency: '최신성',
      none: '근거 없음',
    })[text] ?? text,
}
