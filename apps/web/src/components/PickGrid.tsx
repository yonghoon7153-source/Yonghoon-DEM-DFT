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

import type { ReactNode } from 'react'

import { GroupFilterFields, type GroupChoice } from './GroupFilter'
import { Card, Empty } from './ui'

export interface PickItem {
  id: number
  /** 굵게 나오는 줄 — 무엇인지. */
  name: string
  /** 그 아래 회색 한 줄 — 조성·조건처럼 고를 때 보는 것. */
  note?: string
  /** 켜졌을 때 앞에 찍는 점.  그래프의 그 곡선 색과 같아야 뜻이 있다. */
  color?: string
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
      <div className="col" style={{ gap: 10 }}>
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
              onChange(limit === undefined ? all : all.slice(0, limit))
            }}
          >
            모두 선택
          </button>
          <button type="button" className="sm ghost" onClick={() => onChange([])}>
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
                      {item.name}
                    </span>
                    {item.note ? (
                      <span className="tiny faint truncate" style={{ display: 'block' }}>
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
