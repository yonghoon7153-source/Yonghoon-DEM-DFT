#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""변이마다 "옳은 이유로 잡혔나" — 변이를 사본 트리에 쓰고 새 프로세스에서 시험 함수를 직접 불러 (화면 600 자 자름 없이) 틀린 칸을 기대 칸과 대조.

  python3 -I mut_reasons.py <원 트리> <사본 트리> <결과 json>

변이 정의 = mutate_pc6_13.py (같은 폴더) 의 PC613 · LIB.  판정 = 떨어진 시험 집합 = 기대 · PD13 · PD02c = 틀린 칸 수 (bad_n) = 기대 칸 수 · 보인 칸 (앞 12) ⊆ 기대
칸 · PD02c 표 칸 · PD13o · PD13g = 틀린 칸 집합 = 기대 · 실경로 셋 = 그 변이가 바꾸는 칸 값.  끝에 사본 트리의 사슬을 원본으로 되돌린다.  값 · σ 없음.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mutate_pc6_13 as M  # noqa: E402

DRV = r'''
import json, shutil, sys, tempfile
sys.path.insert(0, sys.argv[1])
import test_rint_r_chain as T
import rint_r_chain as R
T.RR = R
T.TD = tempfile.mkdtemp(prefix='mutr_')
try:
    T.fixtures()
    out = {}
    for name in sys.argv[2].split(','):
        try:
            res, why = getattr(T, 't_' + name)()
        except Exception as e:
            res, why = False, repr(e)
        out[name] = {'pass': bool(res), 'why': why}
    print('MUTR ' + json.dumps(out, ensure_ascii=False, default=repr))
finally:
    shutil.rmtree(T.TD, ignore_errors=True)
'''
FAILRC = ['1', '2', '-9', '137', 'True', 'False', '0.0', "'0'"]
FAIL_ROWS = [f'None/{r}' for r in FAILRC]
NONE_ROWS = ['None/None', 'timeout/None', 'signal/None', 'signal_after/None']
G4 = ['plain', 'python_bug', 'oom_cupy', 'disk_full']
ALL_PATHS = ['rc1', 'rc_timeout', 'rc_signal', 'rc_signal_after', 'time_limit', 'group_unconfirmed', 'orphan_recover', 'orphan_timeout', 'orphan_signal',
             'orphan_signal_after', 'orphan_rc1']
RE_PATHS = [p for p in ALL_PATHS if p not in ('rc1', 'orphan_rc1')]
TESTS = {'G': 'PD13,PD13o,PD13g,PD13r,PD13d', 'L': 'PD02c,PD02cr'}


def k(nms, rows):
    return {f'{n}/{r}' for n in nms for r in rows}


#: id → {시험: 기대} — 기대 = None (통과) · set (틀린 칸 집합 · PD13 · PD02c 는 bad_n + 부분집합) · callable (실경로 detail → bool) · ('tab', set, cuda9)
EXP = {
    'G13a': {'PD13': k(G4, FAIL_ROWS), 'PD13r': lambda w: w['bug'][5]['cause'] == 'group_unconfirmed' and w['oom'][5]['cause'] == 'group_unconfirmed'},
    'G13b': {'PD13': k(['plain', 'python_bug'], FAIL_ROWS), 'PD13r': lambda w: w['bug'][5]['cause'] == 'group_unconfirmed' and w['oom'][5]['cause'] == 'resource'},
    'G13c': {'PD13': k(G4, ['None/False', 'None/0.0'])},
    'G13d': {'PD13': k(G4, FAIL_ROWS), 'PD13o': {'ce1_plain', 'ce1_python', 'ce_neg9_plain'},
             'PD13r': lambda w: w['bug'][5]['cause'] == 'group_unconfirmed',
             'PD13d': lambda w: w['bug'][6] == [1, None, False] and w['bug'][7]['cause'] == 'parent_dead'},
    'G13e': {'PD13': k(G4, NONE_ROWS), 'PD13o': {'ce_none_rc'}},
    'G13f': {'PD13o': {'ce1_plain', 'ce1_python', 'ce_neg9_plain'},
             'PD13d': lambda w: w['bug'][6] == [1, None, False] and w['bug'][7]['cause'] == 'parent_dead'},
    'G13g': {'PD13o': {'ce_timeout', 'ce_signal'}},
    'G13h': {'PD13g': {'chain_rc1', 'chain_timeout'}, 'PD13d': lambda w: w['bug'][6] == [None, None, None] and w['bug'][7]['cause'] == 'parent_dead'},
    'G13i': {'PD13g': {'recover_carry'}},
    'G13j': {'PD13g': {'chain_rc1', 'chain_timeout', 'recover_carry'},
             'PD13d': lambda w: w['bug'][6] == [None, None, None] and w['bug'][7]['cause'] == 'parent_dead'},
    'G13k': {'PD13g': {'chain_rc1', 'chain_timeout', 'recover_carry'},
             'PD13d': lambda w: w['bug'][5] == ['recover', 1, 'parent_dead', True] and w['bug'][6] == [None, None, None]},
    'G13l': {'PD13r': lambda w: w['bug'][1] is False and w['oom'][1] is False and w['bug'][5]['cause'] == 'runner_rc'},
    'L02a': {'PD02c': ('tab', k(['cublas'], RE_PATHS), False)},
    'L02b': {'PD02c': ('tab', k(['cusolver'], RE_PATHS), False)},
    'L02c': {'PD02c': ('tab', k(['cusparse'], RE_PATHS), False), 'PD02cr': lambda w: w[2]['cause'] == 'parent_dead' and w[3] == 0},
    'L02d': {'PD02c': ('tab', k(['cufft'], RE_PATHS), False)},
    'L02e': {'PD02c': ('tab', k(['cuda_error_assert', 'cuda_error_illegal'], RE_PATHS), False)},
    'L02f': {'PD02c': ('tab', k(['cublas_alloc_and_oom', 'cuda_error_oom_drvcode'], ALL_PATHS), True)},
    'L02g': {'PD02c': ('tab', k(['cuda_error_assert', 'cuda_error_illegal'], RE_PATHS), False)},
}


def judge(mid, out):
    exp = EXP[mid]
    names = TESTS['G' if mid.startswith('G') else 'L'].split(',')
    notes, ok = {}, True
    for t in names:
        r = out.get(t) or {}
        e = exp.get(t)
        if e is None:
            good = r.get('pass') is True
            notes[t] = 'pass' if good else f'뜻밖 실패 {str(r.get("why"))[:200]}'
        elif r.get('pass') is not False:
            good, notes[t] = False, '통과 (기대 = 실패)'
        elif callable(e):
            try:
                good = bool(e(r['why']))
            except Exception as ex:                                  # noqa: BLE001
                good = False
                notes[t] = f'detail 꼴 {type(ex).__name__}: {ex}'
            notes.setdefault(t, 'fail · 기대 칸 값' if good else f'fail · 칸 값 다름 {str(r.get("why"))[:300]}')
        else:
            w = r['why']
            if isinstance(e, tuple):
                _tag, want, cuda9 = e
                got = set((w.get('bad') or {}).keys())
                good = w.get('bad_n') == len(want) and got <= want and (w.get('tab') or {}).get('cuda9') is cuda9
                notes[t] = f'bad_n {w.get("bad_n")} / 기대 {len(want)} · 보인 칸 ⊆ 기대 {got <= want} · cuda9 {(w.get("tab") or {}).get("cuda9")}'
            elif t in ('PD13',):
                got = set((w.get('bad') or {}).keys())
                good = w.get('bad_n') == len(e) and got <= e
                notes[t] = f'bad_n {w.get("bad_n")} / 기대 {len(e)} · 보인 칸 ⊆ 기대 {got <= e}'
            else:
                got = set((w.get('bad') or {}).keys())
                good = got == e
                notes[t] = f'틀린 칸 {sorted(got)} / 기대 {sorted(e)}'
        ok = ok and good
    return ok, notes


def main():
    wt, tree, outp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    src = (wt / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
    dst = tree / 'scripts' / 'rint_r_chain.py'
    drv = tree / '_mutr_driver.py'
    drv.write_text(DRV, encoding='utf-8')
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    res = []
    try:
        for mid, why, old, new, _only, _exp in M.PC613 + M.LIB:
            assert src.count(old) == 1, (mid, src.count(old))
            dst.write_text(src.replace(old, new, 1), encoding='utf-8')
            p = subprocess.run(['nice', '-n', '10', sys.executable, str(drv), str(tree / 'scripts'), TESTS['G' if mid.startswith('G') else 'L']],
                               capture_output=True, text=True, env=env, cwd=str(tree))
            line = [ln for ln in p.stdout.splitlines() if ln.startswith('MUTR ')]
            out = json.loads(line[-1][5:]) if line else {}
            ok, notes = judge(mid, out) if out else (False, {'driver': (p.stdout[-400:] + p.stderr[-400:])})
            res.append({'id': mid, 'why': why, 'right_reason': ok, 'notes': notes})
            print(mid, 'right_reason' if ok else 'CHECK', json.dumps(notes, ensure_ascii=False)[:600], flush=True)
    finally:
        dst.write_text(src, encoding='utf-8')
        drv.unlink()
    outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print('right_reason', sum(r['right_reason'] for r in res), '/', len(res))


if __name__ == '__main__':
    main()
