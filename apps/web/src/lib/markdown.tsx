/** 아주 작은 마크다운 — 패치노트가 `docs/log.md` **그대로**라서 필요하다.
 *
 * 그 파일은 사람이 읽으라고 쓴 마크다운이고, 화면은 그것을 글자 그대로
 * 뿌리고 있었다.  그래서 강조하려고 적은 `**` 가 화면에서는 오히려 **읽는 것을
 * 방해하는 기호**가 됐다 — 제일 중요한 문장에만 붙어 있으니 하필 거기서.
 *
 * 라이브러리를 안 쓴다.  필요한 것이 넷뿐이고(굵게 · 기울임 · 코드 · 들여쓴
 * 블록), 마크다운 파서는 하나같이 HTML 을 뱉는다 -- 그걸 넣으려면
 * `dangerouslySetInnerHTML` 이 필요하고, 그 순간 이 화면은 `docs/log.md` 에
 * 적힌 것을 실행하는 화면이 된다.  여기서는 **React 노드만 만든다.**
 */

import type { ReactNode } from 'react'

type Marks = { bold?: boolean; italic?: boolean; code?: boolean }

/** 한 조각의 글자와 그 조각에 걸린 표시. */
export interface Segment extends Marks {
  text: string
}

/** 순서가 뜻이다.  코드가 먼저라서 `` `**x**` `` 안의 별표는 글자로 남는다 --
 *  이 저장소의 기록에는 `**` 를 그대로 보여 주는 자리가 실제로 있다. */
const RULES: { pattern: RegExp; mark: keyof Marks; recurse: boolean }[] = [
  { pattern: /`([^`\n]+)`/, mark: 'code', recurse: false },
  { pattern: /\*\*([^*\n]+)\*\*/, mark: 'bold', recurse: true },
  { pattern: /\*([^*\n]+)\*/, mark: 'italic', recurse: true },
]

/** 한 줄을 조각으로 나눈다.  못 알아본 것은 **글자 그대로 남긴다** — 지우면
 *  사람이 적은 것이 화면에서 사라진다. */
export function inlineSegments(text: string, marks: Marks = {}): Segment[] {
  let best: { at: number; length: number; inner: string; mark: keyof Marks; recurse: boolean } | null = null
  for (const rule of RULES) {
    const found = rule.pattern.exec(text)
    if (!found) continue
    if (best === null || found.index < best.at) {
      best = {
        at: found.index,
        length: found[0].length,
        inner: found[1] ?? '',
        mark: rule.mark,
        recurse: rule.recurse,
      }
    }
  }
  if (best === null) return text ? [{ text, ...marks }] : []

  const before = text.slice(0, best.at)
  const after = text.slice(best.at + best.length)
  const innerMarks = { ...marks, [best.mark]: true }
  return [
    ...(before ? [{ text: before, ...marks }] : []),
    ...(best.recurse ? inlineSegments(best.inner, innerMarks) : [{ text: best.inner, ...innerMarks }]),
    ...inlineSegments(after, marks),
  ]
}

export type Block =
  | { kind: 'para'; lines: string[] }
  | { kind: 'code'; lines: string[] }
  | { kind: 'list'; lines: string[] }

/** 본문을 덩어리로 나눈다.
 *
 *  들여쓴 블록을 따로 두는 이유가 이 저장소에서는 특별하다: 기록에 적히는 표와
 *  실측값이 전부 그 모양이다.  그것을 문단으로 흘려 보내면 자릿수가 어긋나서
 *  숫자를 비교할 수 없게 된다 -- 그 표를 적은 이유가 비교인데.
 */
export function blocks(body: string): Block[] {
  const out: Block[] = []
  let current: Block | null = null
  const flush = () => {
    if (current && current.lines.length) out.push(current)
    current = null
  }
  for (const raw of body.replace(/\r\n/g, '\n').split('\n')) {
    const line = raw.replace(/\s+$/, '')
    if (!line.trim()) {
      flush()
      continue
    }
    const indented = /^(?: {4}|\t)/.test(line)
    const bullet = /^\s*[-*·]\s+/.test(line)
    const kind: Block['kind'] = indented ? 'code' : bullet ? 'list' : 'para'
    if (!current || current.kind !== kind) {
      flush()
      current = { kind, lines: [] } as Block
    }
    current.lines.push(kind === 'code' ? line.replace(/^(?: {4}|\t)/, '') : line.trim())
  }
  flush()
  return out
}

function marked(segments: Segment[]): ReactNode[] {
  return segments.map((segment, index) => {
    if (segment.code) return <code key={index}>{segment.text}</code>
    let node: ReactNode = segment.text
    if (segment.italic) node = <em key={index}>{node}</em>
    if (segment.bold) node = <strong key={index}>{node}</strong>
    return <span key={index}>{node}</span>
  })
}

/** 한 줄을 그린다 (표시를 살려서). */
export function Inline({ text }: { text: string }) {
  return <>{marked(inlineSegments(text))}</>
}

/** 본문 전체를 그린다. */
export function Markdown({ body, className }: { body: string; className?: string }) {
  return (
    <div className={className}>
      {blocks(body).map((block, index) => {
        if (block.kind === 'code') {
          // 표와 실측값이다.  자릿수가 맞아야 하므로 고정폭에 줄바꿈 그대로.
          return <pre key={index} className="md-pre">{block.lines.join('\n')}</pre>
        }
        if (block.kind === 'list') {
          return (
            <ul key={index} className="md-list">
              {block.lines.map((line, i) => (
                <li key={i}>
                  <Inline text={line.replace(/^\s*[-*·]\s+/, '')} />
                </li>
              ))}
            </ul>
          )
        }
        // 문단 안의 줄바꿈은 붙인다.  `docs/log.md` 는 80칸에서 접혀 있을 뿐,
        // 거기서 줄을 바꾸려던 것이 아니다.
        return (
          <p key={index} className="md-p">
            <Inline text={block.lines.join(' ')} />
          </p>
        )
      })}
    </div>
  )
}
