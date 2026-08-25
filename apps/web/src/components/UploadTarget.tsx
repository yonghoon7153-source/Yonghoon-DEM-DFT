/** 세 업로드 화면이 함께 쓰는 "어느 셀에 붙일까" 와 "여기에 끌어다 놓으세요".
 *
 *  충방전 업로드에만 있던 모양을 EIS·GITT 로 옮기면서 한 곳으로 모았다.  같은
 *  일을 세 번 적어 두면 한 번 고칠 때 두 곳이 남는데, 이 화면들이 하는 일은
 *  실제로 똑같다: **그룹을 정하고 → 셀을 정하고 → 파일을 던진다.**
 *
 *  그룹을 먼저 고르는 순서에는 이유가 있다.  아래 "기존 셀" 목록이 그 그룹으로
 *  좁혀지고 새로 만드는 셀은 그 그룹에 들어가므로, 한 실험 묶음을 통째로 올릴
 *  때 나중에 하나씩 붙이지 않아도 된다.
 */

import { useCallback, useMemo, useRef, useState, type ReactNode } from 'react'

import { Field } from './ui'
import { api } from '../lib/api'
import { useAsync } from '../lib/hooks'
import type { Group, Sample } from '../lib/types'

/** 파일 이름에서 셀 이름을 뽑는다 — 끝의 파일 순번(`_011`)만 뗀다.
 *
 *  Smart Interface 가 긴 실험을 `..._011.wrd`, `..._012.wrd` 로 쪼개므로 그
 *  둘은 **한 셀**이다.  나머지는 손대지 않는다: 이름 안의 질량과 조건은
 *  사람이 적은 것이고, 규칙을 더 넣을수록 틀릴 자리가 는다.
 */
export function cellNameFor(fileName: string): string {
  const stem = fileName.replace(/\.[^.]+$/, '')
  return stem.replace(/_\d{2,4}$/, '') || stem
}

export interface UploadTarget {
  groupId: number | null
  setGroupId: (value: number | null) => void
  newName: string
  setNewName: (value: string) => void
  target: number | null
  setTarget: (value: number | null) => void
  query: string
  setQuery: (value: string) => void
  nameFromFile: boolean
  setNameFromFile: (value: boolean) => void
  groups: Group[]
  samples: Sample[]
  matches: Sample[]
  /** 파일마다 어느 셀에 붙일지.  필요하면 셀을 만든다.
   *
   *  파일 하나가 셀 하나인 실험이 많아서 (컷오프만 바꾼 열네 개짜리 묶음
   *  같은) 이름을 열네 번 타이핑하게 두지 않는다 — 그때는 파일 이름이
   *  셀 이름이 되고, 같은 이름은 한 번만 만든다.
   */
  planFor: (files: File[]) => Promise<(number | null)[]>
}

export function useUploadTarget(reloadKey: unknown = 0): UploadTarget {
  const [groupId, setGroupId] = useState<number | null>(null)
  const [newName, setNewName] = useState('')
  const [target, setTarget] = useState<number | null>(null)
  const [query, setQuery] = useState('')
  const [nameFromFile, setNameFromFile] = useState(false)

  const samples = useAsync(() => api.listSamples(), [reloadKey], { live: true })
  const groups = useAsync(() => api.listGroups(), [reloadKey], { live: true })

  const matches = useMemo(() => {
    const all = samples.data ?? []
    const needle = query.trim().toLowerCase()
    const inGroup = groupId === null ? all : all.filter((s) => s.group_id === groupId)
    if (!needle) return inGroup
    return inGroup.filter((s) => s.name.toLowerCase().includes(needle))
  }, [samples.data, query, groupId])

  const planFor = useCallback(async (files: File[]) => {
    if (target !== null) return files.map(() => target)

    if (newName.trim()) {
      const created = await api.createSample({
        name: newName.trim(),
        ...(groupId === null ? {} : { group_id: groupId }),
      })
      // 다음 드롭이 같은 이름으로 또 만들지 않도록 고른 셀로 옮겨 둔다.
      setTarget(created.id)
      setNewName('')
      return files.map(() => created.id)
    }

    if (!nameFromFile) return files.map(() => null)

    // 같은 이름을 두 번 만들지 않도록 이번 드롭에서 만든 것을 기억한다.
    const madeHere = new Map<string, number>()
    const out: (number | null)[] = []
    for (const file of files) {
      const wanted = cellNameFor(file.name)
      const known = madeHere.get(wanted)
        ?? (samples.data ?? []).find((s) => s.name === wanted)?.id
      if (known) {
        out.push(known)
        continue
      }
      const created = await api.createSample({
        name: wanted,
        ...(groupId === null ? {} : { group_id: groupId }),
      })
      madeHere.set(wanted, created.id)
      out.push(created.id)
    }
    return out
  }, [target, newName, groupId, nameFromFile, samples.data])

  return {
    groupId, setGroupId, newName, setNewName, target, setTarget,
    query, setQuery, nameFromFile, setNameFromFile,
    groups: groups.data ?? [], samples: samples.data ?? [], matches,
    planFor,
  }
}

/** ① 그룹 · ② 새 셀 만들기 / 기존 셀에 연결. */
export function UploadTargetFields({ pick }: { pick: UploadTarget }) {
  return (
    <>
      <Field label="① 그룹" hint="새 셀이 들어갈 곳 · 아래 목록도 좁혀집니다">
        <select
          value={pick.groupId ?? ''}
          aria-label="그룹"
          onChange={(event) => {
            pick.setGroupId(event.target.value ? Number(event.target.value) : null)
            // 좁힌 목록에 없는 셀이 골라진 채로 남으면, 화면에는 안 보이는
            // 셀에 파일이 붙는다.
            pick.setTarget(null)
          }}
        >
          <option value="">그룹 없음</option>
          {pick.groups.map((group) => (
            <option key={group.id} value={group.id}>{group.name}</option>
          ))}
        </select>
      </Field>

      <div className="grid cols-2" style={{ gap: 10, margin: '10px 0 12px' }}>
        <Field label="② 새 셀 만들기"
               hint={pick.nameFromFile ? '파일마다 셀 하나' : '이름만 입력'}>
          <input
            type="text"
            value={pick.newName}
            placeholder="No_1_dry_0.0316g"
            aria-label="새 셀 이름"
            disabled={pick.target !== null || pick.nameFromFile}
            onChange={(event) => pick.setNewName(event.target.value)}
          />
          <label className="tiny" style={{ display: 'block', marginTop: 6 }}>
            <input
              type="checkbox"
              checked={pick.nameFromFile}
              onChange={(event) => {
                pick.setNameFromFile(event.target.checked)
                if (event.target.checked) {
                  pick.setNewName('')
                  pick.setTarget(null)
                }
              }}
              style={{ marginRight: 6 }}
            />
            파일 이름을 셀 이름으로
          </label>
        </Field>
        <Field
          label="② 또는 기존 셀에 연결"
          hint={pick.matches.length && pick.query.trim()
            ? `${pick.matches.length}개 일치`
            : '이름을 쳐서 좁힐 수 있습니다'}
        >
          {/* 라벨은 Field 안의 첫 폼 요소에 붙는다.  검색칸이 먼저 오므로
              select 는 자기 라벨을 따로 들어야 이름 없는 컨트롤이 되지 않는다. */}
          <input
            type="text"
            value={pick.query}
            placeholder="이름 일부…"
            aria-label="셀 이름으로 찾기"
            disabled={pick.newName.trim() !== ''}
            onChange={(event) => {
              pick.setQuery(event.target.value)
              pick.setTarget(null)
            }}
            style={{ marginBottom: 6 }}
          />
          <select
            value={pick.target ?? ''}
            aria-label="기존 셀에 연결"
            disabled={pick.newName.trim() !== ''}
            onChange={(event) =>
              pick.setTarget(event.target.value ? Number(event.target.value) : null)}
          >
            <option value="">연결 안 함 (나중에 지정)</option>
            {pick.matches.map((sample) => (
              <option key={sample.id} value={sample.id}>{sample.name}</option>
            ))}
          </select>
        </Field>
      </div>
    </>
  )
}

/** 끌어다 놓는 자리.  누르면 파일 고르기도 된다. */
export function DropZone({
  accept,
  label,
  hint,
  onFiles,
  children,
}: {
  /** `input[accept]` 에 그대로 — `.wrd`, `.mpr,.mpt,.mps`. */
  accept: string
  label: string
  hint?: ReactNode
  onFiles: (files: FileList | File[]) => void
  children?: ReactNode
}) {
  const [over, setOver] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  return (
    <div
      className={`dropzone${over ? ' over' : ''}`}
      onDragOver={(event) => {
        event.preventDefault()
        setOver(true)
      }}
      onDragLeave={() => setOver(false)}
      onDrop={(event) => {
        event.preventDefault()
        setOver(false)
        onFiles(event.dataTransfer.files)
      }}
      onClick={() => inputRef.current?.click()}
      role="button"
      tabIndex={0}
      onKeyDown={(event) => event.key === 'Enter' && inputRef.current?.click()}
    >
      <div className="big">{label}</div>
      <div className="small">{hint ?? '또는 눌러서 선택 · 여러 개 한 번에 가능'}</div>
      {children}
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        multiple
        hidden
        aria-label={label}
        onChange={(event) => {
          if (event.target.files) onFiles(event.target.files)
          event.target.value = ''
        }}
      />
    </div>
  )
}
