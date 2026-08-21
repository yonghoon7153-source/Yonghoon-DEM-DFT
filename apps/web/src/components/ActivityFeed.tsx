/** 최근에 누가 무엇을 했는지.
 *
 * 한 서버를 여럿이 쓰면 제일 먼저 생기는 질문이 "이거 누가 올렸지", "이 질량
 * 누가 바꿨지" 다.  기록은 서버가 자동으로 남기고(ADR 0012), 여기는 읽기만
 * 한다.
 */

import { Link } from 'react-router-dom'

import { useAsync } from '../lib/hooks'
import { api } from '../lib/api'
import type { Activity } from '../lib/types'
import { ago } from './WhoAmI'

const ENTITY: Record<Activity['entity'], string> = {
  sample: '셀',
  group: '그룹',
  preset: '프리셋',
  run: '파일',
}

const ACTION: Record<Activity['action'], string> = {
  create: '추가',
  update: '수정',
  delete: '삭제',
}

/** 무엇을 고쳤는지, 사람이 쓰는 말로.  모르는 필드는 이름 그대로 둔다 —
 *  틀린 번역보다 낯선 영어가 낫다. */
const FIELD_NAMES: Record<string, string> = {
  total_mass_mg: '질량',
  active_mass_mg: '활물질 질량',
  active_wt_percent: '활물질 wt%',
  composition_json: '조성',
  diameter_mm: '지름',
  area_cm2: '면적',
  thickness_um: '두께',
  nominal_specific_capacity_mah_g: '공칭 비용량',
  reference_electrode: '기준전극',
  reference_offset_v: '전압 오프셋',
  reference_cycle: '기준 사이클',
  declared_state: '상태',
  group_id: '그룹',
  name: '이름',
  notes: '메모',
  cycle_offset: '사이클 오프셋',
  temperature_c: '온도',
  c_rate: 'C-rate',
}

function fieldList(fields: string[]): string {
  if (!fields.length) return ''
  const shown = fields.slice(0, 3).map((field) => FIELD_NAMES[field] ?? field)
  return shown.join(', ') + (fields.length > 3 ? ` 외 ${fields.length - 3}` : '')
}

export function ActivityFeed({ limit = 12 }: { limit?: number }) {
  const feed = useAsync(() => api.activity({ limit }), [limit], { live: true })
  const rows = feed.data ?? []

  if (feed.error) return <div className="tiny faint">활동 기록을 읽지 못했습니다.</div>
  if (!rows.length) {
    return <div className="tiny faint">아직 기록이 없습니다.</div>
  }

  return (
    <ul className="feed">
      {rows.map((entry) => (
        <li key={entry.id}>
          <span className={`tag ${entry.action}`}>{ACTION[entry.action] ?? entry.action}</span>
          <span className="what truncate">
            {/* 셀만 링크로 건다 — 그룹·프리셋·파일은 각자의 화면이 없다. */}
            {entry.entity === 'sample' && entry.entity_id !== null && entry.action !== 'delete' ? (
              <Link to={`/samples/${entry.entity_id}`}>{entry.label || `셀 ${entry.entity_id}`}</Link>
            ) : (
              <span>{entry.label || `${ENTITY[entry.entity] ?? entry.entity} ${entry.entity_id ?? ''}`}</span>
            )}
            {entry.fields.length ? (
              <span className="faint"> · {fieldList(entry.fields)}</span>
            ) : null}
          </span>
          <span className="spacer" />
          <span className="tiny faint nowrap" title={entry.at}>
            {entry.actor || '이름 없음'} · {ago(entry.at)}
          </span>
        </li>
      ))}
    </ul>
  )
}
