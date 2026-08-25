/** 그룹 · 소그룹 — 고르는 자리 하나로 모아 둔 것.
 *
 *  그룹은 한 단계만 겹친다 (ADR 0025): 그룹 안에 소그룹, 소그룹 안에는 셀.
 *  화면이 드롭다운 둘인 이유가 그것이고, 그래서 이 부품이 곧 그 규칙의
 *  표현이다 — 세 번째 드롭다운이 없으므로 3단을 만들 자리도 없다.
 *
 *  셀은 **한 자리에만** 산다.  소그룹에 든 셀의 `group_id` 는 소그룹을
 *  가리키므로, 상위 그룹으로 거를 때는 그 자식들까지 같이 봐야 한다.
 *  `includes()` 가 그 한 곳이다 (서버 쪽 짝은 `deps.group_scope`).
 */

import { useCallback, useMemo, useState } from 'react'

import { Field } from './ui'
import { api } from '../lib/api'
import { useAsync } from '../lib/hooks'
import type { Group } from '../lib/types'

export interface GroupChoice {
  groupId: number | null
  subGroupId: number | null
  setGroupId: (value: number | null) => void
  setSubGroupId: (value: number | null) => void
  /** 전부.  트리를 그려야 하는 화면(라이브러리)이 쓴다. */
  groups: Group[]
  /** 최상위 그룹만. */
  tops: Group[]
  /** 지금 고른 그룹의 소그룹들.  아무것도 안 골랐으면 빈 배열. */
  subs: Group[]
  /** 서버에 보낼 `group_id` — 소그룹이 골라졌으면 그것, 아니면 그룹. */
  effective: number | null
  /** 이 그룹 id 가 지금 고른 범위에 드는가.  안 골랐으면 전부 든다. */
  includes: (groupId: number | null | undefined) => boolean
  /** 그룹 목록이 도착했는가.  도착 전에 `setFromGroupId` 를 부르면 부모를
   *  찾을 수 없어 "그룹 없음" 으로 읽힌다 — 저장된 값을 화면에 앉히는 쪽은
   *  이것을 기다려야 한다. */
  loaded: boolean
  /** 저장된 `group_id` 하나로 두 드롭다운을 맞춘다.
   *
   *  셀은 한 노드만 가리키므로 (ADR 0025) 그것이 소그룹이면 위 칸에는 그
   *  **부모**가 와야 한다.  이 계산이 화면마다 흩어지면 어떤 화면은 소그룹에
   *  든 셀을 "그룹 없음" 으로 그린다. */
  setFromGroupId: (groupId: number | null) => void
  /** 방금 만든 그룹이 목록에 나오도록. */
  reload: () => void
  /** 그룹/소그룹을 그 자리에서 만든다.  만들고 나서 골라 둔다. */
  create: (name: string, parentId: number | null) => Promise<void>
}

export function useGroupChoice(reloadKey: unknown = 0): GroupChoice {
  const [groupId, setGroupIdRaw] = useState<number | null>(null)
  const [subGroupId, setSubGroupId] = useState<number | null>(null)
  const groups = useAsync(() => api.listGroups(), [reloadKey], { live: true })

  const all = useMemo(() => groups.data ?? [], [groups.data])
  const tops = useMemo(() => all.filter((group) => !group.parent_id), [all])
  const subs = useMemo(
    () => (groupId === null ? [] : all.filter((g) => g.parent_id === groupId)),
    [all, groupId])

  // 그룹을 바꾸면 소그룹은 놓는다.  옛 그룹의 자식이 골라진 채로 남으면
  // 화면에 없는 조건으로 걸러진 빈 목록이 나온다.
  const setGroupId = useCallback((value: number | null) => {
    setGroupIdRaw(value)
    setSubGroupId(null)
  }, [])

  const includes = useCallback((candidate: number | null | undefined) => {
    if (subGroupId !== null) return candidate === subGroupId
    if (groupId === null) return true
    if (candidate === groupId) return true
    return all.some((g) => g.id === candidate && g.parent_id === groupId)
  }, [all, groupId, subGroupId])

  const setFromGroupId = useCallback((id: number | null) => {
    const found = id === null ? undefined : all.find((group) => group.id === id)
    if (!found) {
      setGroupIdRaw(null)
      setSubGroupId(null)
      return
    }
    if (found.parent_id) {
      setGroupIdRaw(found.parent_id)
      setSubGroupId(found.id)
    } else {
      setGroupIdRaw(found.id)
      setSubGroupId(null)
    }
  }, [all])

  const create = useCallback(async (name: string, parentId: number | null) => {
    const made = await api.createGroup({
      name, ...(parentId === null ? {} : { parent_id: parentId }),
    })
    await groups.reload()
    if (parentId === null) setGroupId(made.id)
    else setSubGroupId(made.id)
  }, [groups, setGroupId])

  return {
    groupId, subGroupId, setGroupId, setSubGroupId,
    groups: all, tops, subs,
    effective: subGroupId ?? groupId,
    includes, loaded: groups.data !== null && groups.data !== undefined,
    setFromGroupId, reload: groups.reload, create,
  }
}

/** 두 드롭다운.  소그룹은 그룹을 고른 뒤에만 뜻이 있으므로 그때만 켜진다. */
export function GroupFilterFields({
  pick,
  groupLabel = '그룹',
  subLabel = '소그룹',
  hint,
  creatable = false,
  compact = false,
}: {
  pick: GroupChoice
  /** 눈에 보이는 라벨.  ①② 같은 번호는 여기에 붙인다 -- 스크린리더가 읽는
   *  이름(`aria-label`)은 번호와 무관하게 '그룹'·'소그룹' 으로 고정한다. */
  groupLabel?: string
  subLabel?: string
  hint?: string
  /** 그 자리에서 새 그룹·소그룹을 만들 수 있게 (업로드 화면에서 쓴다). */
  creatable?: boolean
  /** 라벨 없이 드롭다운 둘만 -- 페이지 머리처럼 세로가 없는 자리에서. */
  compact?: boolean
}) {
  if (compact) {
    return (
      <div className="row" style={{ gap: 6 }}>
        <GroupSelect
          aria-label="그룹 필터"
          value={pick.groupId}
          options={pick.tops}
          empty="모든 그룹"
          width={170}
          onChange={pick.setGroupId}
        />
        {/* 소그룹이 없는 그룹에서는 자리를 차지하지 않는다 -- 대부분의 그룹이
            그렇고, 늘 떠 있으면 머리줄이 쓰지도 않는 칸으로 넓어진다. */}
        {pick.subs.length ? (
          <GroupSelect
            aria-label="소그룹 필터"
            value={pick.subGroupId}
            options={pick.subs}
            empty="소그룹 전체"
            width={160}
            onChange={pick.setSubGroupId}
          />
        ) : null}
      </div>
    )
  }

  // 감싸지 않는다.  부르는 쪽의 격자(라이브러리의 `cols-4`, 업로드의 `cols-2`)가
  // 다른 칸들과 같은 폭으로 눕히게 두면, 세 섹션의 거르기 줄이 저절로 같은
  // 모양이 된다 -- 여기서 한 겹 감싸면 두 칸이 한 칸 안에 눌려 들어간다.
  return (
    <>
      <Field label={groupLabel} hint={hint}>
        <GroupSelect
          aria-label="그룹"
          value={pick.groupId}
          options={pick.tops}
          empty="그룹 없음"
          onChange={pick.setGroupId}
          onCreate={creatable ? (name) => pick.create(name, null) : undefined}
        />
      </Field>
      <Field
        label={subLabel}
        hint={pick.groupId === null
          ? '그룹을 먼저 고르세요'
          : pick.subs.length
            ? `${pick.subs.length}개`
            : '이 그룹에는 아직 없습니다'}
      >
        <GroupSelect
          aria-label="소그룹"
          value={pick.subGroupId}
          options={pick.subs}
          empty="소그룹 없음 (그룹 전체)"
          disabled={pick.groupId === null}
          onChange={pick.setSubGroupId}
          onCreate={creatable && pick.groupId !== null
            ? (name) => pick.create(name, pick.groupId)
            : undefined}
        />
      </Field>
    </>
  )
}

/** 하나짜리 드롭다운.  `onCreate` 를 주면 "+ 새로 만들기" 가 붙는다. */
function GroupSelect({
  value,
  options,
  empty,
  disabled = false,
  width,
  onChange,
  onCreate,
  'aria-label': ariaLabel,
}: {
  value: number | null
  options: Group[]
  empty: string
  disabled?: boolean
  width?: number
  onChange: (value: number | null) => void
  onCreate?: (name: string) => Promise<void>
  'aria-label': string
}) {
  const [making, setMaking] = useState(false)
  const [name, setName] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function submit() {
    const wanted = name.trim()
    if (!wanted || busy) return
    setBusy(true)
    try {
      await onCreate?.(wanted)
      setMaking(false)
      setName('')
      setError('')
    } catch (cause) {
      // 서버가 3단을 거절하는 등, 이유가 있는 거절이다.  삼키면 아무 일도
      // 안 일어난 것처럼 보인다.
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
    }
  }

  return (
    <>
      <select
        aria-label={ariaLabel}
        value={value ?? ''}
        disabled={disabled}
        style={width ? { width } : undefined}
        onChange={(event) => {
          if (event.target.value === '__new__') {
            setMaking(true)
            return
          }
          onChange(event.target.value ? Number(event.target.value) : null)
        }}
      >
        <option value="">{empty}</option>
        {options.map((group) => (
          <option key={group.id} value={group.id}>
            {group.name}
            {group.sample_count ? ` (${group.sample_count})` : ''}
          </option>
        ))}
        {onCreate ? <option value="__new__">+ 새로 만들기…</option> : null}
      </select>
      {making && onCreate ? (
        <div className="row" style={{ gap: 6, marginTop: 6 }}>
          <input
            type="text"
            autoFocus
            value={name}
            aria-label={`새 ${ariaLabel} 이름`}
            placeholder="이름"
            onChange={(event) => setName(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                event.preventDefault()
                void submit()
              }
              if (event.key === 'Escape') setMaking(false)
            }}
          />
          <button type="button" disabled={busy || !name.trim()}
                  onClick={() => void submit()}>
            만들기
          </button>
          <button type="button" onClick={() => { setMaking(false); setError('') }}>
            취소
          </button>
        </div>
      ) : null}
      {error ? <div className="tiny warn">{error}</div> : null}
    </>
  )
}

/** 트리를 한 줄로: "부모 · 자식".  표의 한 칸과 묶음 제목이 같은 말을 쓰도록. */
export function groupPath(name: string | null | undefined,
                          parentName: string | undefined): string {
  if (!name) return ''
  return parentName ? `${parentName} · ${name}` : name
}
