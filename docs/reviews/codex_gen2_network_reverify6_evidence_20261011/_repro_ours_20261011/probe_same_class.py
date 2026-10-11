"""G2RR6-01 같은 부류 자기 점검 — 공용 판정 case15_negctl_s0b_problems 에 추가 변이 (순수 함수 · 읽기 전용).

사용: python3 -I -B probe_same_class.py <tree> <evidence_dir> <out_json>
기대 = 거부 (문제 ≥ 1).  rc 0 처럼 문제 0 이면 '통과 (오수용)'.
"""
import copy
import json
import math
import sys
from pathlib import Path

tree, evd, out = (Path(a).resolve() for a in sys.argv[1:4])
sys.path[:0] = [str(tree / 'scripts')]
import g2_network_reread as RR  # noqa: E402

doc = json.loads((evd / 'r6_s0b_positive.input.json').read_text(encoding='utf-8'))
CID = 'case15_network'


def run(fn):
    d = copy.deepcopy(doc)
    fn(d['reports'][CID], d)
    return RR.case15_negctl_s0b_problems(CID, d['reports'][CID], d['checks'], (d.get('timings') or {}).get(CID))


def setk(path, v):
    def f(r, _d):
        o = r
        for k in path[:-1]:
            o = o[k]
        o[path[-1]] = v
    return f


def na(rows):
    return setk(('negctl', 'negative_area'), rows)


A1, A2 = [31, 29241, -0.186036, 1.05114], [38, 29241, -0.186264, 1.0512]
M = {
    # ── raw_sha (Codex 둘 + 같은 부류)
    'raw_sha_empty_dict': setk(('raw_sha',), {}),
    'raw_sha_one_key_dropped': lambda r, d: r['raw_sha'].pop('mesh_v4_1710000.stl'),
    'raw_sha_extra_key': lambda r, d: r['raw_sha'].update({'extra.bin': ['abcdefabcdef', 'abcdefabcdef']}),
    'raw_sha_expected_changed_both': lambda r, d: r['raw_sha'].update({'atom_v4_1710000.liggghts': ['000000000000', '000000000000']}),
    'raw_sha_not_hex': lambda r, d: r['raw_sha'].update({'atom_v4_1710000.liggghts': ['zzzzzzzzzzzz', 'zzzzzzzzzzzz']}),
    'raw_sha_empty_strings': lambda r, d: r['raw_sha'].update({'atom_v4_1710000.liggghts': ['', '']}),
    'raw_sha_value_triple': lambda r, d: r['raw_sha'].update({'atom_v4_1710000.liggghts': ['f40f69eccd79', 'f40f69eccd79', 'x']}),
    'raw_sha_none': setk(('raw_sha',), None),
    # ── negative_area (Codex 둘 + 같은 부류)
    'na_positive_areas': na([[31, 29241, 0.186036], [38, 29241, 0.186264]]),
    'na_area_missing': na([[31, 29241], [38, 29241]]),
    'na_area_zero': na([[31, 29241, 0.0, 1.05114], [38, 29241, 0.0, 1.0512]]),
    'na_area_nan': na([[31, 29241, math.nan, 1.05114], [38, 29241, math.nan, 1.0512]]),
    'na_area_bool': na([[31, 29241, True, 1.05114], [38, 29241, True, 1.0512]]),
    'na_area_string': na([[31, 29241, '-0.186036', 1.05114], [38, 29241, '-0.186264', 1.0512]]),
    'na_extra_junk_row': na([A1, A2, 'junk']),
    'na_extra_short_row': na([A1, A2, [7]]),
    'na_ids_as_strings': na([['31', '29241', -0.186036, 1.05114], ['38', '29241', -0.186264, 1.0512]]),
    'na_ids_as_floats_trunc': na([[31.9, 29241.2, -0.186036, 1.05114], [38.7, 29241.9, -0.186264, 1.0512]]),
    'na_area_changed_value': na([[31, 29241, -5.0, 1.05114], [38, 29241, -5.0, 1.0512]]),
    'na_not_list': na('31,29241'),
    # ── nc1 같은 부류 (요약 · 상세 모순)
    'failed_stages_extra': lambda r, d: r.update(failed_stages=list(r.get('failed_stages') or []) + ['Parse']),
    # ── nc2 같은 부류 (등록 밖 τ 숫자 키)
    'tau_numeric_other_key': lambda r, d: r['tau'].update({'tau2_flux_ion_net_full': 3.21}),
    # ── nc3 거부 문자열 (부분 문자열만)
    'refuse_text_padded': lambda r, d: r['negctl']['channels']['thermal_physics'].update(
        error='junk ' + str(r['negctl']['channels']['thermal_physics'].get('error')) + ' junk'),
}
rows = []
for k, fn in M.items():
    try:
        p = run(fn)
        rows.append(dict(mutation=k, n_problems=len(p), passes=(len(p) == 0), first=(p[0][:240] if p else '')))
    except Exception as e:  # noqa: BLE001
        rows.append(dict(mutation=k, n_problems=None, passes=None, first=f'예외 {type(e).__name__}: {e}'[:240]))
base = RR.case15_negctl_s0b_problems(CID, doc['reports'][CID], doc['checks'], doc['timings'][CID])
res = dict(tree_head=(tree / 'HEAD_SHA').read_text().strip(), positive_problems=base, rows=rows,
           failed_stages_positive=doc['reports'][CID].get('failed_stages'))
out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print('positive problems', base, '· failed_stages', res['failed_stages_positive'])
for r in rows:
    print(f"{r['mutation']:30s} {'통과(오수용)' if r['passes'] else ('거부' if r['passes'] is False else '예외')} · {r['first'][:110]}")
