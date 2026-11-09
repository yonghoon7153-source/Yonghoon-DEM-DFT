# -*- coding: utf-8 -*-
"""사전 공격 15 변이 — 새 가드 하나씩 (사본 pa15/mut/scripts/rint_r_chain.py · 원본 = pa15/tree) → `--only RR3,PA13,PA14,RR4` → 잡힘 (실패 검사 이름) · 생존.
   고친 사람의 변이 목록을 보지 않고 직접 고른 것."""
import json
import py_compile
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

PA15 = Path(__file__).resolve().parent.parent
SRC = PA15 / 'tree' / 'scripts' / 'rint_r_chain.py'
DST = PA15 / 'mut' / 'scripts' / 'rint_r_chain.py'
TEST = PA15 / 'mut' / 'scripts' / 'test_rint_r_chain.py'
ONLY = sys.argv[1] if len(sys.argv) > 1 else 'RR3,PA13,PA14,RR4'

M = [
    ('a_drop', "    if ent is not None:                                        # ⓐ 지킴", "    if False:                                        # ⓐ 지킴"),
    ('a_missing_ok', "    ent = ('attempt.json 없음 · 꼴 틀림', f'n {n}') if a is None else attempt_entry_diff(a, n, e)",
     "    ent = None if a is None else attempt_entry_diff(a, n, e)"),
    ('a_noentry_ok', "        return f'{RESUME_PROV} [ⓐ] {folder.name}: 원장 항목 {n!r} 이 없다'", "        return None"),
    ('entry_no_resume_of', "ATTEMPT_ENTRY_FIELDS = ('target', 'machine', 'resume_of')", "ATTEMPT_ENTRY_FIELDS = ('target', 'machine')"),
    ('entry_no_machine', "ATTEMPT_ENTRY_FIELDS = ('target', 'machine', 'resume_of')", "ATTEMPT_ENTRY_FIELDS = ('target', 'resume_of')"),
    ('b_drop', "    if bind is not None:                                       # ⓑ 지킴", "    if False:                                       # ⓑ 지킴"),
    ('b_eq_only_type', "    if not (type(frm) is int and frm == eff):", "    if not (type(frm) is int):"),
    ('b_newattempt_R_ok', "        return None if R is None else f'원장 항목 {n} = 새 시도", "        return None if True else f'원장 항목 {n} = 새 시도"),
    ('b_nondict_ok', "        return f'원장 항목 {n} = 재실행 (resume_of {e[\"resume_of\"]}) 인데 요약 resume 칸 = {type(R).__name__} (생산자 = 객체)'",
     "        return None"),
    ('src_failopen', "    if src is None:                                            # 원천 지킴 (fail-closed)",
     "    if src is None:\n        return None\n    if src is None:"),
    ('loc_count_ge1', "    if len(hit) != 1:", "    if len(hit) == 0:"),
    ('loc_symlink', "p.name == r['folder'] and not p.is_symlink() and p.is_dir()]", "p.name == r['folder'] and p.is_dir()]"),
    ('loc_attempt', "    if a is None or a['n'] != frm or a['target'] != e['target']:", "    if False:"),
    ('loc_digest', "    if folder_digest(p) != r['folder_sha256']:\n        return None, f'원천 {p.name} 요약 sha", "    if False:\n        return None, f'원천 {p.name} 요약 sha"),
    ('c_drop', "    if bnd is not None:                                        # ⓒ 지킴", "    if False:                                        # ⓒ 지킴"),
    ('c_after_new', "            if seen_new:\n                return f'복사 기록 런", "            if False:\n                return f'복사 기록 런"),
    ('c_cf_eq', "            if not (type(r['copied_from']) is int and r['copied_from'] == frm):", "            if False:"),
    ('c_cf_type', "            if not (type(r['copied_from']) is int and r['copied_from'] == frm):", "            if not (r['copied_from'] == frm):"),
    ('c_copy_srcdone', "            if not _src_run_done(src, nm, od):", "            if False:"),
    ('c_bytes', "                if st_m != 'ok' or st_t != 'ok' or mine != theirs:", "                if False:"),
    ('c_launch_only', "            for ext in ('launch.json', 'end.json'):", "            for ext in ('launch.json',):"),
    ('c_end_only', "            for ext in ('launch.json', 'end.json'):", "            for ext in ('end.json',):"),
    ('c_payload', "            if not same:", "            if False:"),
    ('c_first_new_done', "        if not seen_new and _src_run_done(src, nm, od):", "        if False:"),
    ('c_new_launch_same', "        if st_m != 'ok' or mine == theirs:", "        if False:"),
    ('c_new_launch_missing_ok', "        if st_m != 'ok' or mine == theirs:", "        if st_m == 'ok' and mine == theirs:"),
    ('srd_no_dir', "    return bool(bound and rc_success(er.get('rc')) and (Path(src) / od).is_dir())", "    return bool(bound and rc_success(er.get('rc')))"),
    ('srd_no_rc', "    return bool(bound and rc_success(er.get('rc')) and (Path(src) / od).is_dir())", "    return bool(bound and (Path(src) / od).is_dir())"),
    ('d_drop', "    if rcmp is not None:                                       # ⓓ 지킴", "    if False:                                       # ⓓ 지킴"),
    ('d_cmp', "    if R.get('compared') != want:", "    if False:"),
    ('d_name', "    if new[0].get('name') != rerun or not (isinstance(od, str) and RUN_DIR_RE.fullmatch(od)):",
     "    if not (isinstance(od, str) and RUN_DIR_RE.fullmatch(od)):"),
    ('new_attempt_no_early_return', "    if e['resume_of'] is None:\n        return None\n    R = s.get('resume') if isinstance(s.get('resume'), dict) else {}\n    src, swhy",
     "    R = s.get('resume') if isinstance(s.get('resume'), dict) else {}\n    src, swhy"),
    ('fields_keep_true', "    if why:\n        f['resume_ok'] = False\n    return f, why", "    return f, why"),
    ('recount_ignore_st', "    if st is None:\n        return result_fields(p, s, unreadable=(sst == 'unreadable')), None",
     "    if True:\n        return result_fields(p, s, unreadable=(sst == 'unreadable')), None"),
    ('write_old', "    f, why = result_fields_ledger(folder, s, st, n, unreadable=unreadable)\n    return _result_line(n, folder, f, by), why",
     "    return attempt_result_line(n, folder, s, by, unreadable=unreadable), None"),
    ('recover_old', "                res, pwhy = attempt_result(n, f, s, 'recover', st, unreadable=(sst == 'unreadable'))",
     "                res, pwhy = attempt_result_line(n, f, s, 'recover', unreadable=(sst == 'unreadable')), None"),
    ('close_old', "        res, pwhy = attempt_result(att.n, att.folder, s, 'chain', att.st)", "        res, pwhy = attempt_result_line(att.n, att.folder, s, 'chain'), None"),
    ('order_no_prov', "    why = resume_chain_provenance_problem(st, ad['chain'])", "    why = None"),
    ('chainprov_noprov', "        why = resume_provenance_problem(st, k, p, s if sst == 'ok' else None)", "        why = None"),
    ('chainprov_nodigest', "        if p.name != r.get('folder') or p.is_symlink() or not p.is_dir() or folder_digest(p) != r.get('folder_sha256'):",
     "        if p.name != r.get('folder') or not p.is_dir():"),
    ('chainprov_nostart_skip', "        if s0 is None:\n            return f'{RESUME_PROV} [원천]", "        if s0 is None:\n            continue\n            return f'{RESUME_PROV} [원천]"),
    ('chain_noprov', "            why = resume_provenance_problem(st, k, cand[0], s_k if sst == 'ok' else None, found=found)", "            why = None"),
    ('chain_recount_nost', "            why = result_line_problem(k, cand[0], r, st=st, found=found)", "            why = result_line_problem(k, cand[0], r)"),
    ('tlp_recount_nost', "        why = result_line_problem(k, p, r, st=st, found=found)  #", "        why = result_line_problem(k, p, r)  #"),
    ('lic_recount_nost', "        why = result_line_problem(n, d, r, st=st, found=found)   #", "        why = result_line_problem(n, d, r)   #"),
    ('M56_exists', "    if not src.is_dir():", "    if not src.exists():"),
]


def run_one(mid, old, new):
    txt = SRC.read_text(encoding='utf-8')
    k = txt.count(old)
    if k != 1:
        return {'id': mid, 'status': f'NOT_UNIQUE {k}'}
    DST.write_text(txt.replace(old, new), encoding='utf-8')
    try:
        py_compile.compile(str(DST), doraise=True)
    except py_compile.PyCompileError as e:
        return {'id': mid, 'status': 'COMPILE_ERROR', 'err': str(e)[:200]}
    t0 = time.time()
    p = subprocess.run([sys.executable, str(TEST), '--only', ONLY], capture_output=True, text=True, cwd=str(PA15 / 'mut'), timeout=1200)
    last = [x for x in p.stdout.splitlines() if x.startswith('test_rint_r_chain:')]
    fails = re.findall(r"FAILED: \[(.*)\]", last[-1]) if last else []
    fl = [x.strip().strip("'") for x in fails[0].split(',')] if fails else []
    return {'id': mid, 'status': 'KILLED' if fl else ('SURVIVED' if p.returncode == 0 else f'rc{p.returncode}'), 'fails': fl,
            'summary': last[-1] if last else p.stdout[-300:] + p.stderr[-300:], 's': round(time.time() - t0, 1)}


out = []
sel = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None
for mid, old, new in M:
    if sel and mid not in sel:
        continue
    r = run_one(mid, old, new)
    out.append(r)
    print(r['id'], r['status'], r.get('fails'), r.get('summary', '')[-90:], flush=True)
shutil.copy2(SRC, DST)
tag = (sys.argv[3] if len(sys.argv) > 3 else 'mutation15')
(PA15 / 'out' / f'{tag}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
k = sum(1 for r in out if r['status'] == 'KILLED')
print(f'total {len(out)} killed {k} survived {[r["id"] for r in out if r["status"] != "KILLED"]}')
