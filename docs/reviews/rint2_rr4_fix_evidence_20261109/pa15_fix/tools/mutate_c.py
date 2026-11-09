# -*- coding: utf-8 -*-
"""고침 C (사전 공격 15 처분) 변이 — 사본 트리 MUT (scripts = 고친 판 사본 · 그 밖 = 바탕 트리 링크) 의 scripts/rint_r_chain.py 에 변이 하나씩 → 상주 시험
`--only RR3,PA13,PA14,RR4,RR5` → 잡힘 (실패 검사 이름) · 생존.  목록 = (1) 사전 공격 15 의 probes/mutate15.py M (바이트 그대로 읽음 · 고친 판에서 글자가 바뀐 다섯 =
같은 뜻으로 옮김 · 지운 가드 = 적용 안 됨 기록) (2) 고침 C 의 새 가드마다.  인자: mutate15.py 경로 · 고친 판 사슬 경로 · MUT 트리 · 출력 JSON · [고를 id 쉼표]."""
import json
import py_compile
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

M15 = Path(sys.argv[1])
SRC = Path(sys.argv[2])
MUT = Path(sys.argv[3]).absolute()
OUT = Path(sys.argv[4])
SEL = set(sys.argv[5].split(',')) if len(sys.argv) > 5 and sys.argv[5] else None
ONLY = 'RR3,PA13,PA14,RR4,RR5'
DST = MUT / 'scripts' / 'rint_r_chain.py'
TEST = MUT / 'scripts' / 'test_rint_r_chain.py'

ns = {}
t15 = M15.read_text(encoding='utf-8')
exec(t15[t15.index('M = ['):t15.index('\n]\n', t15.index('M = [')) + 3], ns)
M15_LIST = ns['M']

#: 고친 판에서 글자가 바뀐 사전 공격 15 변이 → 같은 뜻 (None = 그 가드를 지웠다 · 적용 안 됨)
ADAPT = {
    'b_drop': ("        if bind is not None:                                   # ⓑ 지킴", "        if False:                                   # ⓑ 지킴"),
    'c_first_new_done': ("        if not seen_new and nm != rerun:", "        if False:"),
    'd_name': None,
    'new_attempt_no_early_return': ("    if e['resume_of'] is None:\n        return None\n    if isinstance(s, dict):\n        frm = (",
                                    "    if isinstance(s, dict):\n        frm = ("),
    'write_old': ("    f, why = result_fields_ledger(folder, s, st, n, unreadable=unreadable)\n    if resume_prov_unconfirmed(why):",
                  "    f, why = result_fields(folder, s, unreadable=unreadable), None\n    if resume_prov_unconfirmed(why):"),
}

#: 고침 C 의 새 가드 (PC15-01 – 05)
NEW = [
    ('N_rerun_eq', "    if rerun is not None and R.get('rerun') != rerun:", "    if False:"),
    ('N_first_new', "        if not seen_new and nm != rerun:", "        if False:"),
    ('N_bind', "        if not bound:                                              # ★ 11-09 사전 공격 15 PC15-02",
     "        if False:                                              # ★ 11-09 사전 공격 15 PC15-02"),
    ('N_dirs_subset', "        if any(d != od for d in dirs):", "        if False:"),
    ('N_prior_done', "        if r is not last and not (run_end_ok(folder, nm) and od in dirs):", "        if False:"),
    ('N_prior_od', "and not (run_end_ok(folder, nm) and od in dirs):", "and not (run_end_ok(folder, nm)):"),
    ('N_prior_end', "and not (run_end_ok(folder, nm) and od in dirs):", "and not (od in dirs):"),
    ('N_last_def', "    last = runs[-1] if runs and runs[-1].get('name') == stop_run else None", "    last = runs[-1] if runs else None"),
    ('N_name_form', "                return None, f'{base.name}/{GROUPS_DIR}/{fn} = 런 이름 꼴 밖",
     "                continue\n                return None, f'{base.name}/{GROUPS_DIR}/{fn} = 런 이름 꼴 밖"),
    ('N_order_rev', "    for run in sorted(names, key=lambda x: (int(RUN_ORDER_RE.fullmatch(x).group(2)), x)):",
     "    for run in sorted(names, key=lambda x: (int(RUN_ORDER_RE.fullmatch(x).group(2)), x), reverse=True):"),
    ('N_order_str', "    for run in sorted(names, key=lambda x: (int(RUN_ORDER_RE.fullmatch(x).group(2)), x)):", "    for run in sorted(names):"),
    ('N_src_names_only', "    for base in (Path(src), Path(folder)):\n        g = base / GROUPS_DIR", "    for base in (Path(src),):\n        g = base / GROUPS_DIR"),
    ('N_d_all_same', "    if bad:\n        return (f'디스크상 첫 미완료 런 {rerun} 이 이 시도에서 끝났는데",
     "    if False:\n        return (f'디스크상 첫 미완료 런 {rerun} 이 이 시도에서 끝났는데"),
    ('N_d_post_not_done', "        if post:\n            return (f'요약 = resume.rerun", "        if False:\n            return (f'요약 = resume.rerun"),
    ('N_d_post_def', "    post = R is not None and (s.get('stop') or {}).get('run') != R.get('rerun')", "    post = False"),
    ('N_d_done_end', "        done = rerun is not None and run_end_ok(folder, rerun) and bool(run_dirs(folder, rerun))",
     "        done = rerun is not None and bool(run_dirs(folder, rerun))"),
    ('N_d_done_dirs', "        done = rerun is not None and run_end_ok(folder, rerun) and bool(run_dirs(folder, rerun))",
     "        done = rerun is not None and run_end_ok(folder, rerun)"),
    ('N_end_ok_confirmed', "    return bool(bound and rc_success(er.get('rc')) and er.get('confirmed') is True)",
     "    return bool(bound and rc_success(er.get('rc')))"),
    ('N_5_old_outdir', "        want = resume_recompare_run(src, folder, rerun)\n    except OSError as e:",
     "        want = resume_recompare(src / od, folder / od)\n    except OSError as e:"),
    ('N_summaryless_skip', "    if e['resume_of'] is None:\n        return None\n    if isinstance(s, dict):\n        frm = (",
     "    if e['resume_of'] is None or not isinstance(s, dict):\n        return None\n    if isinstance(s, dict):\n        frm = ("),
    ('N_summaryless_effnone', "        if frm is None:\n            return (f'{RESUME_PROV} [ⓑ] {folder.name}: 요약 없는 재실행 시도",
     "        if False:\n            return (f'{RESUME_PROV} [ⓑ] {folder.name}: 요약 없는 재실행 시도"),
    ('N_held', "    if resume_prov_unconfirmed(why):", "    if False:"),
    ('N_held_close', "    except ResultHeld as e:                                # ★ 11-09 사전 공격 15 PC15-03",
     "    except ZeroDivisionError as e:                                # ★ 11-09 사전 공격 15 PC15-03"),
    ('N_entry_type', "    diff = [f for f in ATTEMPT_ENTRY_FIELDS if not (type(a[f]) is type(e[f]) and a[f] == e[f])]",
     "    diff = [f for f in ATTEMPT_ENTRY_FIELDS if a[f] != e[f]]"),
    ('N_shape', "        if shape is not None:                                  # ★ 11-09 사전 공격 15 PC15-05",
     "        if False:                                  # ★ 11-09 사전 공격 15 PC15-05"),
]


def run_one(mid, old, new, txt):
    if old is None:
        return {'id': mid, 'status': 'NOT_APPLICABLE (가드를 지웠다 · 고친 판)'}
    k = txt.count(old) if old else 0
    if old and k != 1:
        return {'id': mid, 'status': f'NOT_UNIQUE {k}'}
    DST.write_text(txt.replace(old, new) if old else txt, encoding='utf-8')
    try:
        py_compile.compile(str(DST), doraise=True)
    except py_compile.PyCompileError as e:
        return {'id': mid, 'status': 'COMPILE_ERROR', 'err': str(e)[:200]}
    t0 = time.time()
    p = subprocess.run([sys.executable, str(TEST), '--only', ONLY], capture_output=True, text=True, cwd=str(MUT), timeout=1800)
    last = [x for x in p.stdout.splitlines() if x.startswith('test_rint_r_chain:')]
    fails = re.findall(r"FAILED: \[(.*)\]", last[-1]) if last else []
    fl = [x.strip().strip("'") for x in fails[0].split(',')] if fails else []
    return {'id': mid, 'status': 'KILLED' if fl else ('SURVIVED' if p.returncode == 0 else f'rc{p.returncode}'), 'fails': fl,
            'summary': last[-1] if last else (p.stdout[-300:] + p.stderr[-300:]), 's': round(time.time() - t0, 1)}


src_txt = SRC.read_text(encoding='utf-8')
plan = [('NOMUT', '', '')]
for mid, old, new in M15_LIST:
    if mid in ADAPT:
        a = ADAPT[mid]
        plan.append((f'm15:{mid}', None if a is None else a[0], None if a is None else a[1]))
    else:
        plan.append((f'm15:{mid}', old, new))
plan += [(f'new:{a}', b, c) for a, b, c in NEW]
out = []
try:
    for mid, old, new in plan:
        if SEL and mid not in SEL and mid.split(':')[-1] not in SEL:
            continue
        r = run_one(mid, old, new, src_txt)
        r['adapted'] = mid.split(':')[-1] in ADAPT
        out.append(r)
        print(r['id'], r['status'], r.get('fails'), (r.get('summary') or '')[-80:], flush=True)
finally:
    DST.write_text(src_txt, encoding='utf-8')
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
mut = [r for r in out if r['id'] != 'NOMUT']
k = [r['id'] for r in mut if r['status'] == 'KILLED']
print(f'total {len(mut)} killed {len(k)} other {[(r["id"], r["status"]) for r in mut if r["status"] != "KILLED"]}')
