"""변이 시험 (Codex 회차 ④ PC14-02 · 03 · RR4-01 고침) — 고친 rint_r_chain.py 의 새 지킴을 하나씩 끈 (또는 RR4-01 의 M56) 사슬로 만든 뿌리 (scripts = 작업 트리 링크
+ 변이 사슬 + 고친 시험 사본 · docs 링크 · `mktree.py`) 에서 ① `test_rint_r_chain.py --only RR4` (잡힘 = 실패 ≥ 1) ② `rows_dump.py RR4` (행 상태 = RR4A 의 accepted /
rejected<표지> · RR4C · RR4D 값) → JSON.  M00 = 변이 없음 (5/5 통과여야).  지킴 하나 ↔ 검사 하나: ⓐ → N3a · ⓑ → N4 · Z4 · ⓒ → N1 · N2 · Z1 · Z2 가 accepted 로
뒤집혀야 · M56 → RR4C 실패.
쓰임: python3 mutate_rr4.py <작업 트리> <결과 폴더> [일꾼 수]"""
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mktree import make_tree  # noqa: E402

WT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
WORKERS = int(sys.argv[3]) if len(sys.argv) > 3 else 2
ORIG = (WT / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
TEST = WT / 'scripts' / 'test_rint_r_chain.py'
SEL = 'RR4'

G_A = "    if ent is not None:                                        # ⓐ 지킴\n"
G_B = "    if bind is not None:                                       # ⓑ 지킴\n"
G_C = "    if bnd is not None:                                        # ⓒ 지킴\n"
G_D = "    if rcmp is not None:                                       # ⓓ 지킴\n"
G_S = "        return f'{RESUME_PROV} [원천] {folder.name}: {swhy} (확인할 수 없는 원천 = 재개 허용 안 함 · fail-closed · ★ 11-09 Codex 회차 ④)'\n"
OFF = "    if False:\n"

MUTS = [
    #  ── 공통 검증 지킴 (resume_provenance_problem) ──
    ('MA_entry_off', [(G_A, OFF)]),
    ('MB_from_off', [(G_B, OFF)]),
    ('MC_boundary_off', [(G_C, OFF)]),
    ('MD_recompare_off', [(G_D, OFF)]),
    ('MS_source_failclosed_off', [(G_S, "        return None\n")]),
    ('MAB_entry_from_off', [(G_A, OFF), (G_B, OFF)]),
    #  ── 부르는 자리 (같은 함수 규칙) ──
    ('W1_order_call_off', [("    why = resume_chain_provenance_problem(st, ad['chain'])     # ★ 11-09 Codex 회차 ④ PC14-02 · 03 — 사슬 끝 결과 줄 resume_ok 만 믿지 않는다\n",
                            "    why = None\n")]),
    ('W2_presolve_call_off', [("        if r['resume_ok'] is True and cand[0].is_dir():           # ★ 11-09 Codex 회차 ④ — 사슬 시도마다 재개 출처 공통 검증\n",
                               "        if False:\n")]),
    ('W3_fields_ledger_off', [("    why = resume_provenance_problem(st, n, folder, s, found=found)\n    if why:\n        f['resume_ok'] = False\n",
                               "    why = None\n")]),
    ('W4_write_folder_only', [("    f, why = result_fields_ledger(folder, s, st, n, unreadable=unreadable)\n    return _result_line(n, folder, f, by), why\n",
                               "    return _result_line(n, folder, result_fields(folder, s, unreadable=unreadable), by), None\n")]),
    ('W5_recount_folder_only', [("    return result_fields_ledger(p, s, st, n, unreadable=(sst == 'unreadable'), found=found)\n",
                                 "    return result_fields(p, s, unreadable=(sst == 'unreadable')), None\n")]),
    #  ── RR4-01 (사전 공격 14 M56 = 같은 바꿈) ──
    ('M56_isdir_to_exists', [("    if not src.is_dir():\n", "    if not src.exists():\n")]),
]


def apply(text, reps):
    for old, new in reps:
        n = text.count(old)
        if n != 1:
            return None, f'old occurs {n}: {old[:60]!r}'
        text = text.replace(old, new)
    return text, None


def run_one(item):
    nm, reps = item
    if reps is None:
        text, err = ORIG, None
    else:
        text, err = apply(ORIG, reps)
    if err:
        return nm, {'verdict': 'SKIP', 'why': err}
    root = OUT / 'roots' / nm
    src = OUT / 'srcs' / f'{nm}.py'
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(text, encoding='utf-8')
    make_tree(WT, root, src, TEST)
    tmp = OUT / 'tmp' / nm
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(tmp), RR4FIX_SCRIPTS=str(root / 'scripts'))
    r = subprocess.run([sys.executable, str(root / 'scripts' / 'test_rint_r_chain.py'), '--only', SEL], cwd=str(tmp), env=env,
                       capture_output=True, text=True, timeout=1800)
    fails = re.findall(r'^  FAIL  (\S+)', r.stdout, re.M)
    summ = [ln for ln in r.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
    d = subprocess.run([sys.executable, str(HERE / 'rows_dump.py'), SEL], cwd=str(tmp), env=env, capture_output=True, text=True, timeout=1800)
    try:
        rows = json.loads(d.stdout)
    except ValueError:
        rows = {'_dump_error': (d.stdout[-300:] + d.stderr[-300:])}
    a = ((rows.get('RR4A') or {}).get('detail') or {})
    states = a.get('states') if isinstance(a, dict) else None
    #  자리별 (결과 줄 쓰기 CLI 자격 · 다음 순서 멈춤 · 풀기 전 사슬 멈춤 · 다시 셈 사유 있음) — 부르는 자리 변이 (W1 · W2) 가 어느 자리를 뒤집는지
    places = {}
    for k, v in ((a.get('rows') or {}) if isinstance(a, dict) else {}).items():
        if isinstance(v, dict):
            pl = v.get('places') or [None, None, None]
            cl = v.get('cli') or [None, None, None, None]
            places[k] = {'write_resume_ok': cl[1], 'write_tags': cl[2], 'order': (pl[1] or [None])[0], 'chain': (pl[2] or [None])[0],
                         'recount_reason': cl[3] is not None}
        else:
            places[k] = v
    dd = ((rows.get('RR4D') or {}).get('detail') or {})
    shutil.rmtree(root, ignore_errors=True)
    shutil.rmtree(tmp, ignore_errors=True)
    verdict = ('PASS_ALL' if not fails and r.returncode == 0 else 'FAILS') if reps is None else ('CAUGHT' if fails else 'MISSED')
    return nm, {'verdict': verdict, 'summary': summ[-1] if summ else (r.stdout[-300:] + r.stderr[-300:]), 'fails': fails,
                'rr4a_states': states, 'rr4a_places': places, 'rr4c_detail': (rows.get('RR4C') or {}).get('detail'),
                'rr4d_rows': dd.get('rows') if isinstance(dd, dict) else dd,
                'rr4b_bad': ((rows.get('RR4B') or {}).get('detail') or {}).get('bad_names')}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = {}
    first = run_one(('M00_identity', None))
    res[first[0]] = first[1]
    print(first[0], first[1]['verdict'], first[1].get('summary'), flush=True)
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for nm, v in ex.map(run_one, MUTS):
            res[nm] = v
            print(nm, v['verdict'], v.get('summary'), v.get('fails'), flush=True)
    (OUT / 'mutation_results.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    caught = [k for k, v in res.items() if v['verdict'] == 'CAUGHT']
    missed = [k for k, v in res.items() if v['verdict'] == 'MISSED']
    print(f'잡힘 {len(caught)}/{len(MUTS)} · 놓침 {missed} · 무변이 {res["M00_identity"]["verdict"]}')


if __name__ == '__main__':
    main()
