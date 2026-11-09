# -*- coding: utf-8 -*-
"""P10 — 정직 꼴 더 (보장 4):
  H6 원천 원 시도의 끝난 런 L01 의 런 폴더가 없음 (결과 줄 전부터) → 생산자 `_src_done` False → 재실행 2 가 L01 부터 새로 (남은 payload 없음 = assumed) · L02 rc 1 (자원)
  H7 원천 L02 = 그룹 미확인 뒤 recover 가 끝 기록을 다시 씀 (by recover · chain_end) 꼴은 고정물 밖이라 뺌 — 대신 원천 L02 = 시간 초과 (killed:timeout · 끝 기록 cause
     timeout · rc null) → 재실행 2 = L01 복사 · L02 새로 (대조 같음) · L03 런 전 TIME_LIMIT
각 꼴 → 세 자리 기대 = 자격 True · 통과."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402
import p4_honest as P4  # noqa: E402  (resume3 · first_custom 재사용 — 모듈 실행부가 같이 돈다)

T, RR = h.T, h.RR


def H6(tag):
    base = Path(T.TD) / 'rr4' / tag
    a1 = T.rr4_first(base)
    shutil.rmtree(Path(a1[0]) / RR.record_outdir(T.rr4_req(1)))      # 끝난 런 L01 의 런 폴더 없음 (원 시도 결과 줄 전)
    a2 = P4.resume3(a1[0], base / 'attempt_2', 2, 1, {1: ('floor', 0), 2: ('again', 1)})
    return [a1, a2]


def H7(tag):
    base = Path(T.TD) / 'rr4' / tag
    f1 = T.rr4_att(base / 'attempt_1', 1, None)
    r1 = T.rr4_files(f1, 1, 'floor')
    r2 = T.rr4_files(f1, 2, 'source-ceiling', rc=0)
    nm = r2['name']
    end = json.loads((f1 / 'groups' / f'{nm}.end.json').read_text(encoding='utf-8'))
    end.update(cause='timeout', rc=None)
    (f1 / 'groups' / f'{nm}.end.json').write_bytes(RR.canon_bytes(end))
    r2.update(rc=None, group_cause='timeout', arms_read=[])
    a1 = (f1, T.rr4_put(f1, T.rr4_summ('TIME_LIMIT', nm, [r1, r2])))
    a2 = T.rr4_resume(f1, base / 'attempt_2', 2, 1, 'source-ceiling')
    return [a1, a2]


res = {}
for nm, mk in (('H6_src_run_folder_missing', H6), ('H7_src_timeout', H7)):
    o = h.three(nm, mk)
    o['accepted_all_three'] = h.accepted(o)
    sm = mk(nm + '_shape')
    o['first_result'] = RR.result_fields(sm[0][0], sm[0][1])
    o['last_shape'] = {'stop': sm[-1][1]['stop'], 'resume': sm[-1][1]['resume'], 'runs': [(r['name'], r.get('copied_from'), r.get('rc')) for r in sm[-1][1]['runs']]}
    res[nm] = o
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p10_honest_more.json', res)
for k, v in res.items():
    print(k, 'ACCEPTED' if v['accepted_all_three'] else 'rejected', v['writer'], v['places'], v['cli'], '| src', v['first_result']['resume_ok'], v['first_result']['cause'],
          '| last', v['last_shape']['stop'], v['last_shape']['resume'] and (v['last_shape']['resume']['copied'], v['last_shape']['resume']['rerun'], v['last_shape']['resume']['determinism']))
