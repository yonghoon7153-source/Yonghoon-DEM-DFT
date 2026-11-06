#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 10 회차 (독립) 실경로 탐침 — 실제 git 원장 · --stage recover --ledger · --add --resume (시험 고정물 = scripts/test_rint_r_chain.py 의
도우미 그대로 · 시험 함수는 부르지 않는다 · 검사 하나만).

쓰는 법: python3 -I probe_ledger.py <scripts 폴더> <출력 json>
- PB-01 ①: 요약 없는 시도 · 사슬 끝 기록 (by chain · 미확인 · 원인 None · rc null · 로그 Traceback) → recover 가 chain_end 로 옮김 → 결과 줄 → --add --resume
  (대조 = 같은 끝 기록 rc 1 · 같은 끝 기록 rc null 인데 확인 True (by chain 길))
- PB-01 ②: 요약 있는 시도 (GROUP_UNCONFIRMED 멈춤 · 런 기록 rc null · group_cause null) → recover → 결과 줄 → --add --resume (대조 = rc 1)
"""
import json
import sys
import tempfile
from pathlib import Path

SCRIPTS, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, SCRIPTS)
import test_rint_r_chain as T  # noqa: E402
import rint_r_chain as RR  # noqa: E402

T.RR = RR
T.TD = tempfile.mkdtemp(prefix='pa10_ledger_')
T.fixtures()
TB = T.RC02_LOG


def summary(rc, gcause, code='GROUP_UNCONFIRMED'):
    def prep(f):
        s = {'tool': RR.TOOL, 'schema': RR.SCHEMA, 'stage': 'ladder', 'status': 'STOPPED',
             'stop': {'code': code, 'what': code, 'cause': 'x', 'run': 'L01_floor', 'reason': None},
             'runs': [{'name': 'L01_floor', 'outdir': 'L01_floor_arm1', 'rc': rc, 'group_cause': gcause}]}
        RR.write_summary(Path(f) / 'ladder_summary.json', s)
    return prep


rows = {}
base_end = {'by': 'chain', 'left': [999989]}
for nm, end, prep in (
        ('A_orphan_unconf_rcnull', {'cause': None, 'rc': None, 'confirmed': False}, None),
        ('A_orphan_unconf_rc1_ctl', {'cause': None, 'rc': 1, 'confirmed': False}, None),
        ('A_orphan_conf_rcnull_ctl', {'cause': None, 'rc': None, 'confirmed': True}, None),
        ('B_summary_gu_rcnull_gcnull', {'cause': None, 'rc': None, 'confirmed': False}, summary(None, None)),
        ('B_summary_gu_rc1_ctl', {'cause': None, 'rc': 1, 'confirmed': False}, summary(1, None)),
        ('B_summary_gu_rcnull_gctimeout_ctl', {'cause': 'timeout', 'rc': None, 'confirmed': False}, summary(None, 'timeout'))):
    r = T.rc_recover_resume(f'PA10_{nm}', dict(base_end, **end), TB, prep=prep)
    f = Path(T.TD) / 'runs' / f'PA10_{nm}' / 'attempt_1'
    er = json.loads((f / 'groups' / 'L01_floor.end.json').read_text(encoding='utf-8'))
    r['end_after_recover'] = {k: er.get(k) for k in ('by', 'rc', 'cause', 'confirmed', 'chain_end')}
    r['log_has_traceback'] = 'Traceback' in (f / 'logs' / 'L01_floor.log').read_text(encoding='utf-8')
    rows[nm] = r

Path(OUT).write_text(json.dumps({'td': T.TD, 'chain_module': RR.__file__, 'rows': rows}, ensure_ascii=False, indent=1, default=str),
                     encoding='utf-8')
for k, r in rows.items():
    print(k.ljust(36), 'orphan', r['orphan'], '| recover rc', r['recover_rc'], '| result', {x: r['result'].get(x) for x in ('cause', 'resume_ok')},
          '| --add --resume rc', r['resume_rc'], 'NOT_ALLOWED' if r['not_allowed'] else 'allowed', '| tb', r['log_has_traceback'])
