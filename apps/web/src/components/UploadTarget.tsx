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

import { CellPicker } from './CellPicker'
import { GroupFilterFields, useGroupChoice, type GroupChoice } from './GroupFilter'
import { Field } from './ui'
import { api } from '../lib/api'
import { useAsync } from '../lib/hooks'
import type { Sample } from '../lib/types'

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
  /** 파일 이름으로 셀을 만드는 길을 열어 둘지.  충방전만 참 — 이유는
   *  `UploadTargetFields` 머리말에 있다. */
  perFileCell: boolean
  /** 그룹 · 소그룹.  새 셀이 들어갈 자리이자 아래 목록을 좁히는 조건이다. */
  group: GroupChoice
  newName: string
  setNewName: (value: string) => void
  target: number | null
  setTarget: (value: number | null) => void
  query: string
  setQuery: (value: string) => void
  nameFromFile: boolean
  setNameFromFile: (value: boolean) => void
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

export function useUploadTarget(reloadKey: unknown = 0,
                                perFileCell = true): UploadTarget {
  const [newName, setNewName] = useState('')
  const [target, setTarget] = useState<number | null>(null)
  const [query, setQuery] = useState('')
  const [nameFromFile, setNameFromFile] = useState(false)

  const samples = useAsync(() => api.listSamples(), [reloadKey], { live: true })
  const group = useGroupChoice(reloadKey)
  const { includes, effective } = group

  const matches = useMemo(() => {
    const all = samples.data ?? []
    const needle = query.trim().toLowerCase()
    // 상위 그룹을 고르면 그 소그룹의 셀도 후보다 -- 서버의 `group_scope` 와
    // 같은 규칙이고, 여기서만 다르면 목록의 수가 드롭다운의 수와 어긋난다.
    const inGroup = all.filter((s) => includes(s.group_id))
    if (!needle) return inGroup
    return inGroup.filter((s) => s.name.toLowerCase().includes(needle))
  }, [samples.data, query, includes])

  const planFor = useCallback(async (files: File[]) => {
    if (target !== null) return files.map(() => target)

    if (newName.trim()) {
      const created = await api.createSample({
        name: newName.trim(),
        ...(effective === null ? {} : { group_id: effective }),
      })
      // 다음 드롭이 같은 이름으로 또 만들지 않도록 고른 셀로 옮겨 둔다.
      setTarget(created.id)
      setNewName('')
      return files.map(() => created.id)
    }

    // 화면이 그 길을 안 열어 두면 여기서도 안 만든다.  체크박스만 숨기면
    // 남아 있는 state 로 셀이 조용히 만들어질 수 있다.
    if (!perFileCell || !nameFromFile) return files.map(() => null)

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
        ...(effective === null ? {} : { group_id: effective }),
      })
      madeHere.set(wanted, created.id)
      out.push(created.id)
    }
    return out
  }, [target, newName, effective, nameFromFile, perFileCell, samples.data])

  return {
    perFileCell,
    group, newName, setNewName, target, setTarget,
    query, setQuery, nameFromFile, setNameFromFile,
    samples: samples.data ?? [], matches,
    planFor,
  }
}

/** ① 그룹 · ② 소그룹 · ③ 새 셀 만들기 / 기존 셀에 연결.
 *
 *  `perFileCell` 은 "파일 이름을 셀 이름으로" 를 낼지다.  충방전에서만 켠다:
 *  거기서는 파일 하나가 셀 하나인 묶음이 흔해서 (컷오프만 바꾼 열네 개짜리
 *  같은) 이름을 열네 번 타이핑하지 않게 해 준다.
 *
 *  EIS·GITT 에서는 낸 적이 있었고, 그것이 틀렸다.  거기서 파일은 셀이 아니라
 *  **셀의 측정**이다 — 같은 셀을 SOC 별로 다섯 번 재면 `.mpr` 이 다섯 개고
 *  셀은 하나다.  게다가 EC-Lab 이 채널 번호를 이름에 붙이므로
 *  (`..._#02_1_C01`) 만들어진 셀 이름은 그 셀의 `.wrd` 이름과 영영 안 맞는다.
 *  결과는 파일 0개짜리 충방전 셀이 셀 목록·대시보드·관계셀 고르개에 쌓이는
 *  것이었다.
 */
export function UploadTargetFields({ pick }: { pick: UploadTarget }) {
  const perFileCell = pick.perFileCell
  // 좁힌 목록에 없는 셀이 골라진 채로 남으면, 화면에는 안 보이는 셀에 파일이
  // 붙는다.  그래서 그룹이 바뀌면 고른 셀을 놓는다.
  const group: GroupChoice = useMemo(() => ({
    ...pick.group,
    setGroupId: (value: number | null) => {
      pick.group.setGroupId(value)
      pick.setTarget(null)
    },
    setSubGroupId: (value: number | null) => {
      pick.group.setSubGroupId(value)
      pick.setTarget(null)
    },
  }), [pick])

  return (
    <>
      <div className="grid cols-2" style={{ gap: 10 }}>
        <GroupFilterFields
          pick={group}
          groupLabel="① 그룹"
          subLabel="② 소그룹"
          hint="새 셀이 들어갈 곳 · 아래 목록도 좁혀집니다"
          creatable
        />
      </div>

      <div className="grid cols-2" style={{ gap: 10, margin: '10px 0 12px' }}>
        <Field label="③ 새 셀 만들기"
               hint={perFileCell && pick.nameFromFile ? '파일마다 셀 하나' : '이름만 입력'}>
          <input
            type="text"
            value={pick.newName}
            placeholder="No_1_dry_0.0316g"
            aria-label="새 셀 이름"
            disabled={pick.target !== null || pick.nameFromFile}
            onChange={(event) => pick.setNewName(event.target.value)}
          />
          {perFileCell ? (
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
          ) : (
            <span className="tiny faint" style={{ display: 'block', marginTop: 6 }}>
              안 정해도 됩니다 — 나중에 아래 색인에서 붙일 수 있습니다.
            </span>
          )}
        </Field>
        <Field
          label="③ 또는 기존 셀에 연결"
          hint={`고를 수 있는 셀 ${pick.matches.length}개`}
        >
          {/* 드롭다운이 아니라 창이다.  셀이 늘면 목록이 화면 밖으로 넘치고,
              길고 앞부분이 같은 이름들은 잘려서 구분되지 않는다.  창 안에서
              그룹·소그룹과 검색으로 좁히고 최근에 고친 순서로 편다. */}
          <CellPicker
            value={pick.target}
            samples={pick.matches}
            label="기존 셀에 연결"
            emptyLabel="연결 안 함 (나중에 지정)"
            disabled={pick.newName.trim() !== ''}
            onPick={(sampleId) => pick.setTarget(sampleId)}
          />
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
