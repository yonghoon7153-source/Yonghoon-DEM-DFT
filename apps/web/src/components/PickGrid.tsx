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
 */

import { type ReactNode, useRef } from 'react'

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
              const all = items.map((item) => item.id)
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
            {items.map((item) => {
              const on = picked.includes(item.id)
              return (
                <label
                  key={item.id}
                  className="pick-item small"
                  title={item.note ? `${item.name}\n${item.note}` : item.name}
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
                    onChange={() => toggle(item.id)}
                  />
                  <span style={{ minWidth: 0 }}>
                    <span className="truncate" style={{ display: 'block' }}>
                      {item.color ? (
                        <span
                          className="swatch"
                          style={{ background: on ? item.color : 'var(--line-strong)' }}
                        />
                      ) : null}
                      {/* 다 된 것은 이름 앞에 체크.  색이 아니라 글자인 이유는
                          정적 캡처와 색맹에서 색만으로는 안 보이기 때문이다. */}
                      {item.done ? (
                        <span className="done-mark" aria-hidden>✓</span>
                      ) : null}
                      {item.name}
                    </span>
                    {item.note || (item.done && item.doneNote) ? (
                      <span className="tiny faint truncate" style={{ display: 'block' }}>
                        {/* 무엇이 됐는지를 **회색으로** 적는다.  체크만 있으면
                            무엇이 됐다는 뜻인지 화면 어디에도 없다. */}
                        {item.done && item.doneNote ? (
                          <>
                            <span className="done-note">{item.doneNote}</span>
                            {item.note ? ' · ' : ''}
                          </>
                        ) : null}
                        {item.note}
                      </span>
                    ) : null}
                  </span>
                </label>
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
