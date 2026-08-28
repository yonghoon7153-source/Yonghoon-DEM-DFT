/** 여럿을 골라 겹쳐 보는 화면들이 함께 쓰는 고르개.
 *
 *  충방전·임피던스·GITT 세 비교 화면이 하는 일은 같다: 그룹으로 좁히고,
 *  체크박스로 몇 개를 켜고, 겹쳐 그린다.  그런데 세 곳이 각자 다르게 생겨서
 *  (충방전은 체크박스 격자, 나머지는 칩 줄) 한 화면에서 익힌 손이 다른 화면에서
 *  통하지 않았다 — "모두 선택" 이 있는 곳과 없는 곳이 갈리고, 고른 수가 제목에
 *  나오는 곳과 안 나오는 곳이 갈렸다.
 *
 *  **상한을 여기서 지킨다.**  고를 수 있는 수는 서버가 정하거나(비교 30개) 그림이
 *  정하는데(겹쳐 그리기 8개), 예전에는 그 상한이 화면마다 다른 방식으로 걸려
 *  있었다: 한쪽은 켜는 것을 막고, 한쪽은 막지 않고 서버가 422 를 냈다.  둘 다
 *  같은 규칙으로 — 상한에 닿으면 **끌 수는 있고 켤 수는 없다**, 그리고 왜인지를
 *  적는다.
 *
 *  **한 파일이 여러 줄인 것은 접는다** (`PickItem.fold`).  SOC 스캔은 파일
 *  하나가 스윕 스물이고, 그 스물은 목록에서 서로 아무것도 구별해 주지 않는다 —
 *  이름도 대역도 회로도 같다.  접지 않으면 고르개가 그 파일 하나로 가득 차서
 *  다른 셀이 화면 밖으로 밀린다.  펴면 스윕을 하나씩 켤 수 있다: SOC 별
 *  나이퀴스트는 스윕마다 다른 곡선이고, 그중 셋만 겹쳐 보는 것이 이 화면의
 *  쓰임이다.
 */

import { type ReactNode, useMemo, useRef, useState } from 'react'

import { GroupFilterFields, type GroupChoice } from './GroupFilter'
import { Card, Empty } from './ui'
import { keepInPlace } from '../lib/anchor'

export interface PickItem {
  id: number
  /** 굵게 나오는 줄 — 무엇인지. */
  name: string
  /** 그 아래 회색 한 줄 — 조성·조건처럼 고를 때 보는 것. */
  note?: string
  /** 켜졌을 때 앞에 찍는 점.  그래프의 그 곡선 색과 같아야 뜻이 있다. */
  color?: string
  /** 이 항목이 **이미 다 된 것**인가 (EIS 라면 fitting 이 있는 것).
   *
   *  이름 앞에 체크를, 아래 회색 줄 앞에 무엇이 됐는지를 적는다.  고르기
   *  전에 알아야 하는 것이라 여기 있다 — 골라 놓고 그림에서 "이건 곡선이
   *  없네" 를 발견하면 다시 고르러 내려와야 한다. */
  done?: boolean
  /** 됐을 때 회색 줄 앞에 적을 말 (`fitting 완료`).  `done` 없이는 안 쓴다. */
  doneNote?: string
  /** 이 항목이 **한 파일의 여러 줄 중 하나**인가 (SOC 스캔의 스윕).
   *
   *  같은 `key` 를 가진 것들이 한 줄로 접히고, 그 줄을 펴야 하나씩 보인다.
   *  `key` 는 파일을 가리키는 것이라야 한다 (sha256) — 이름으로 묶으면 이름이
   *  같은 다른 파일이 한 줄로 합쳐진다. */
  fold?: { key: string; label: string; note?: string }
}

/** 목록을 그리는 단위.  접힌 파일 하나가 항목 여럿을 대신한다. */
type Block =
  | { kind: 'one'; item: PickItem }
  | { kind: 'fold'; key: string; label: string; note?: string; items: PickItem[] }

/** 접힌 파일 한 줄이 말해야 하는 '다 된' 상태 — 스윕 전부인가, 몇 개인가.
 *
 *  머리말 줄만 보고 고르는 사람이 많다 (펴는 것이 한 번 더 누르는 일이라).
 *  그래서 **그 줄이 파일 전체를 말해야** 한다: 스윕 열하나 중 셋만 맞춰진
 *  파일에 체크가 붙으면, 골라 놓고 그림에서 곡선 여덟 개가 비는 것을 본다.
 *  반대로 전부 맞춰진 파일에 아무 표시가 없으면 펴서 열하나를 세어야 안다.
 */
export function foldDone(
  items: PickItem[],
): { done: number; total: number; all: boolean } {
  const done = items.filter((one) => one.done).length
  return { done, total: items.length, all: items.length > 0 && done === items.length }
}

/** 평평한 목록을 접힌 덩어리로.  **첫 등장 자리**를 지킨다 — 스캔을 목록
 *  끝으로 몰면 방금 올린 파일이 맨 밑에 가 있다. */
export function foldItems(items: PickItem[]): Block[] {
  const blocks: Block[] = []
  const at = new Map<string, Extract<Block, { kind: 'fold' }>>()
  for (const item of items) {
    if (!item.fold) {
      blocks.push({ kind: 'one', item })
      continue
    }
    const seen = at.get(item.fold.key)
    if (seen) {
      seen.items.push(item)
      continue
    }
    const block: Extract<Block, { kind: 'fold' }> = {
      kind: 'fold',
      key: item.fold.key,
      label: item.fold.label,
      note: item.fold.note,
      items: [item],
    }
    at.set(item.fold.key, block)
    blocks.push(block)
  }
  // 스윕이 하나뿐인 파일은 접을 것이 없다 — 접힌 줄과 안 접힌 줄이 같은 수를
  // 대신하면 펴는 단추만 하나 더 있는 셈이다.
  return blocks.map((block) =>
    block.kind === 'fold' && block.items.length === 1
      ? { kind: 'one' as const, item: block.items[0]! }
      : block)
}

export function PickGrid({
  title,
  items,
  picked,
  onChange,
  group,
  groupHint = '소그룹까지 골라 좁힐 수 있습니다',
  limit,
  limitNote,
  extra,
  empty,
}: {
  /** 제목 앞머리.  뒤에 "· N개" 가 붙는다 — 몇 개를 골랐는지가 제목에 있어야
   *  스크롤을 내린 상태에서도 보인다. */
  title: string
  items: PickItem[]
  picked: number[]
  onChange: (ids: number[]) => void
  /** 그룹·소그룹으로 좁히기.  없으면 그 줄을 안 그린다. */
  group?: GroupChoice
  groupHint?: string
  /** 한 번에 고를 수 있는 최대.  없으면 제한 없음. */
  limit?: number
  /** 상한에 닿았을 때 적을 말.  왜 더 못 켜는지는 화면마다 다르다. */
  limitNote?: string
  /** 그 화면만의 추가 필터 (목적·전해질·검색 …). */
  extra?: ReactNode
  empty?: ReactNode
}) {
  const full = limit !== undefined && picked.length >= limit
  const blocks = useMemo(() => foldItems(items), [items])
  // 펴 놓은 파일.  **접힌 것이 기본**이다 — 스캔 하나가 스무 줄이면 그 파일
  // 하나로 고르개가 가득 찬다.  편 것은 열어 둔 채로 두어야 스윕 셋을 차례로
  // 켜는 동안 다시 펴지 않는다.
  const [open, setOpen] = useState<string[]>([])
  // 고르개는 그림 **밑**에 있다.  체크를 하나 누르면 위쪽이 다시 그려지면서
  // 높이가 변하고 (범례가 한 줄 늘거나 줄고, 경고가 뜨거나 사라지고, '고른 것'
  // 표에 줄이 하나 붙는다), 고르개가 그만큼 위아래로 움직인다 — 다음에
  // 누르려던 칸이 커서 밑에서 사라진다.  다섯 개를 고르려면 스크롤을 다섯 번
  // 다시 맞춰야 했다.  누른 순간의 자리를 붙잡아 둔다 (`lib/anchor`).
  const box = useRef<HTMLDivElement>(null)
  const toggle = (id: number) => {
    if (picked.includes(id)) {
      onChange(picked.filter((value) => value !== id))
      return
    }
    // 상한에서는 **켜는 것만** 막는다.  끄는 것까지 막으면 자리를 비울 수가
    // 없어서, 다른 것을 보려면 화면을 새로 고치는 수밖에 없다.
    if (full) return
    onChange([...picked, id])
  }

  /** 접힌 줄의 체크박스.  하나라도 켜져 있으면 **끄기**다 — 스무 개를 켠 뒤
   *  다시 누를 때 원하는 것은 언제나 비우기이고, 그 반대(이미 켠 것 위에 더
   *  얹기)는 상한 때문에 아무 일도 안 일어나는 클릭이 된다. */
  const toggleFold = (block: Extract<Block, { kind: 'fold' }>) => {
    const ids = block.items.map((item) => item.id)
    const on = ids.filter((id) => picked.includes(id))
    if (on.length) {
      onChange(picked.filter((id) => !ids.includes(id)))
      return
    }
    // 남은 자리만큼만.  상한을 넘겨 켜면 서버가 422 를 내거나 그림이 조용히
    // 몇 개를 버린다 — 어느 쪽이든 화면의 칩과 곡선이 어긋난다.
    const room = limit === undefined ? ids.length : Math.max(0, limit - picked.length)
    onChange([...picked, ...ids.slice(0, room)])
  }

  const item = (one: PickItem, inFold = false) => {
    const on = picked.includes(one.id)
    return (
      <label
        key={one.id}
        className="pick-item small"
        // 접힌 파일 안에서는 이름이 `#3` 뿐이다 — 어느 파일의 3번인지는
        // 머리말 줄에만 있어서, 스크롤이 그 줄을 지나면 사라진다.
        title={[inFold ? one.fold?.label : null, one.name, one.note]
          .filter(Boolean).join('\n')}
        style={{
          // 더 못 켜는 것은 흐리게.  누를 수는 있게 두면 아무 일도
          // 안 일어나는 클릭이 되고, 그것이 고장으로 읽힌다.
          cursor: !on && full ? 'default' : 'pointer',
          opacity: !on && full ? 0.45 : 1,
        }}
      >
        <input
          type="checkbox"
          checked={on}
          disabled={!on && full}
          onChange={() => toggle(one.id)}
        />
        <span style={{ minWidth: 0 }}>
          <span className="truncate" style={{ display: 'block' }}>
            {one.color ? (
              <span
                className="swatch"
                style={{ background: on ? one.color : 'var(--line-strong)' }}
              />
            ) : null}
            {/* 다 된 것은 이름 앞에 체크.  색이 아니라 글자인 이유는
                정적 캡처와 색맹에서 색만으로는 안 보이기 때문이다. */}
            {one.done ? <span className="done-mark" aria-hidden>✓</span> : null}
            {one.name}
          </span>
          {one.note || (one.done && one.doneNote) ? (
            <span className="tiny faint truncate" style={{ display: 'block' }}>
              {/* 무엇이 됐는지를 **회색으로** 적는다.  체크만 있으면
                  무엇이 됐다는 뜻인지 화면 어디에도 없다. */}
              {one.done && one.doneNote ? (
                <>
                  <span className="done-note">{one.doneNote}</span>
                  {one.note ? ' · ' : ''}
                </>
              ) : null}
              {one.note}
            </span>
          ) : null}
        </span>
      </label>
    )
  }

  return (
    <Card title={`${title} · ${picked.length}개`}>
      {/* **한 자리에서 붙잡는다.**  체크만이 아니라 그룹·소그룹·검색도 목록의
          길이를 바꾸고, 그때마다 고르개가 위아래로 달아난다 — 소그룹을 골랐더니
          화면이 위로 튀어 다음에 누를 칸을 다시 찾아야 했다.  `change` 는
          거품처럼 올라오므로 (select · checkbox · input 전부) 상자 하나에
          걸어 두면 그 안의 무엇을 건드려도 자리가 유지된다. */}
      <div className="col" style={{ gap: 10 }} ref={box}
           onChange={() => keepInPlace(box.current)}>
        {group ? (
          <div className="grid cols-2" style={{ gap: 10 }}>
            <GroupFilterFields pick={group} hint={groupHint} />
          </div>
        ) : null}

        {extra ? <div className="pick-extra">{extra}</div> : null}

        <div className="row">
          <button
            type="button"
            className="sm"
            onClick={() => {
              const all = items.map((one) => one.id)
              // 여기가 높이를 가장 크게 바꾼다 — 한 번에 열두 줄이 붙는다.
              keepInPlace(box.current)
              onChange(limit === undefined ? all : all.slice(0, limit))
            }}
          >
            모두 선택
          </button>
          <button
            type="button"
            className="sm ghost"
            onClick={() => { keepInPlace(box.current); onChange([]) }}
          >
            해제
          </button>
          <span className="spacer" />
          {limit !== undefined ? (
            <span className={full ? 'tiny warn' : 'tiny faint'}>
              {picked.length} / {limit}
            </span>
          ) : null}
        </div>

        {full && limitNote ? <div className="tiny warn">{limitNote}</div> : null}

        {items.length ? (
          <div className="pick-grid">
            {blocks.map((block) => {
              if (block.kind === 'one') return item(block.item)

              const ids = block.items.map((one) => one.id)
              const on = ids.filter((id) => picked.includes(id)).length
              const shown = open.includes(block.key)
              // 접힌 줄의 '다 된' 상태 — 스윕 하나가 아니라 파일 전체 (`foldDone`).
              const mark = foldDone(block.items)
              const doneWord = block.items.find((one) => one.doneNote)?.doneNote
              const doneLine = doneWord && mark.done
                ? (mark.all ? doneWord : `${mark.done}개 ${doneWord}`)
                : ''
              return (
                <div className="pick-fold" key={`fold:${block.key}`}>
                  <div className="pick-fold-head">
                    <label
                      className="pick-item small"
                      title={[`${block.label}`, `스윕 ${ids.length}개`,
                              doneLine ? `${mark.done}/${mark.total} ${doneWord}` : null]
                        .filter(Boolean).join('\n')}
                      style={{
                        cursor: !on && full ? 'default' : 'pointer',
                        opacity: !on && full ? 0.45 : 1,
                      }}
                    >
                      <input
                        type="checkbox"
                        checked={on > 0}
                        // 일부만 켜진 것은 켜짐도 꺼짐도 아니다.  세모 표시가
                        // 없으면 "스무 개 중 셋" 이 "스무 개 전부" 로 보인다.
                        ref={(node) => { if (node) node.indeterminate = on > 0 && on < ids.length }}
                        disabled={!on && full}
                        onChange={() => toggleFold(block)}
                      />
                      <span style={{ minWidth: 0 }}>
                        <span className="truncate" style={{ display: 'block' }}>
                          {/* 스윕 **전부**가 됐을 때만 체크다.  일부에 체크가
                              붙으면 접힌 줄을 믿고 골랐다가 빈 곡선을 본다. */}
                          {mark.all ? <span className="done-mark" aria-hidden>✓</span> : null}
                          {block.label}
                        </span>
                        <span className="tiny faint truncate" style={{ display: 'block' }}>
                          스윕 {ids.length}개{on ? ` · ${on}개 켬` : ''}
                          {doneLine ? (
                            <>
                              {' · '}
                              <span className="done-note">{doneLine}</span>
                            </>
                          ) : null}
                          {block.note ? ` · ${block.note}` : ''}
                        </span>
                      </span>
                    </label>
                    <button
                      type="button"
                      className="sm ghost pick-fold-toggle"
                      aria-expanded={shown}
                      onClick={() => {
                        // 펴면 스무 줄이 한꺼번에 붙는다 — 단추를 누른 자리가
                        // 그만큼 밀린다.  단추 클릭은 `change` 가 아니라서
                        // 상자에 걸어 둔 걸쇠가 안 잡는다.
                        keepInPlace(box.current)
                        setOpen((was) => was.includes(block.key)
                          ? was.filter((key) => key !== block.key)
                          : [...was, block.key])
                      }}
                    >
                      {shown ? '접기' : '스윕 고르기'}
                    </button>
                  </div>
                  {shown ? (
                    <div className="pick-fold-body">
                      {block.items.map((one) => item(one, true))}
                    </div>
                  ) : null}
                </div>
              )
            })}
          </div>
        ) : (
          empty ?? <Empty title="고를 것이 없습니다" icon="⌕" />
        )}
      </div>
    </Card>
  )
}
