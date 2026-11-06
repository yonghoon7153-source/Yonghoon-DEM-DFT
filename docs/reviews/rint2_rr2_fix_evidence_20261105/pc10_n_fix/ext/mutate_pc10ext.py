"""PC10 확장 (P2-A · P2-B · P3-5) 새 가드 변이 — git 없는 사본 (리포 밖) 에서 가드 하나씩 약하게 · 깨고 고른 시험을 돌린다 (`../mutate_pc10.py` 꼴).

usage: python3 -I mutate_pc10ext.py <사본 나무> <out.json> [이름,…]
  사본 나무 = scripts/rint_r_chain.py · scripts/test_rint_r_chain.py (+ 고정물이 읽는 파일) 가 있는 폴더 (git 저장소 아님).
  한 변이 = 사슬 원문 한 자리 (정확히 한 번 나와야 · 아니면 SKIP) 바꿈 → 시험 → 원 바이트로 되돌림 · 끝에 사슬 · 시험 sha256 이 처음과 같은지 적는다.
  잡힘 = 시험 rc ≠ 0 + 잡아야 할 검사 하나 이상 FAIL (KILLED) · rc ≠ 0 인데 그 검사가 아닌 다른 검사만 = KILLED_OTHER · rc 0 = SURVIVED.
  종류 W = 가드를 약하게 (반례 행이 잡아야) · L = 생산자 꼴을 거부하게 (거짓 fail-closed — 대조 행이 잡아야).
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

MT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
SEL = set(sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] else None
RRF = 'scripts/rint_r_chain.py'
TST = 'scripts/test_rint_r_chain.py'
ONLY = 'CT,RN,RC0,PE03,PD13,PD02,LG,FF,CE,SU,AL19,RS02'

# (이름, 종류, 항목, 옛 글, 새 글, 잡아야 할 검사)
M = [
    # ── P2-A 거부 기록 (rejected_in_folder · rejected_form_problem · rejected_folder_problem)
    ('A01', 'W', 'rejected_in_folder: 칸 대조 뺌', 'why = rejected_form_problem(rec, read_attempt(folder)) or rejected_folder_problem(folder)',
     'why = rejected_folder_problem(folder)', ['CT05']),
    ('A02', 'W', 'rejected_in_folder: 폴더 대조 뺌', 'why = rejected_form_problem(rec, read_attempt(folder)) or rejected_folder_problem(folder)',
     'why = rejected_form_problem(rec, read_attempt(folder))', ['CT05']),
    ('A03', 'W', '폴더 대조: 남는 것 (흔적) 무시', '    if extra or miss:\n', '    if miss:\n', ['CT05']),
    ('A04', 'W', '폴더 대조: 링크 · 특수 파일 받음', "        if not stat.S_ISREG(m):\n            return f'{nm} = 일반 파일이 아니다",
     "        if False:\n            return f'{nm} = 일반 파일이 아니다", ['CT05']),
    ('A05', 'W', '칸 대조: 칸 더 있음 받음 (부분집합만)', '    if set(rec) != REJECTED_KEYS:\n', '    if not REJECTED_KEYS <= set(rec):\n', ['CT05']),
    ('A06', 'W', '칸 대조: n = bool 받음', "    if type(rec['n']) is not int or rec['n'] != att['n']:", "    if rec['n'] != att['n']:", ['CT05']),
    ('A07', 'W', '칸 대조: 시작 커밋 결합 → 40 hex 꼴만', "    if rec['ledger_commit'] != att['ledger_commit']:", "    if not _hex40(rec['ledger_commit']):",
     ['CT05']),
    ('A08', 'W', '칸 대조: code = 글이면 무엇이든', "    if not (type(rec['code']) is str and STOP_CODE_RE.fullmatch(rec['code'])):",
     "    if not isinstance(rec['code'], str):", ['CT05']),
    ('A09', 'W', '칸 대조: cause · utc 꼴 안 봄', "    if type(rec['cause']) is not str or type(rec['utc']) is not str:", '    if False:', ['CT05']),
    ('A10', 'W', '칸 대조: schema 안 봄', "    if rec['schema'] != REJECTED_SCHEMA:\n        return f'schema", "    if False:\n        return f'schema", ['CT05']),
    ('A11', 'W', 'recover_ledger = 옛 읽기 (rejected_record)', '                rec = rejected_in_folder(f, f.name)', '                rec = rejected_record(rj, f.name)',
     ['CT05']),
    ('A12', 'W', 'result_recount 폴더 = 옛 읽기 (rejected_record)', '        rec = rejected_in_folder(p, p.name)',
     '        rec = rejected_record(p / REJECTED_FILE, p.name)', ['CT05']),
    ('A13', 'W', 'attempt.json 없음 받음 (그 대조 건너뜀)', "    if att is None:\n        return 'attempt.json", "    if att is None:\n        return None and 'attempt.json",
     ['CT05']),
    # ── P2-B 멈춘 런 기록 안 대조 (stopped_record_problem · chain_confirmed)
    ('B01', 'W', '① runs 마지막 대조 뺌', '    if not (isinstance(runs, list) and runs and runs[-1] is rr):', '    if not isinstance(runs, list):', ['CT06']),
    ('B02', 'W', '② outdir 접두 (<런> · <런>_arm) 뺌', " and isinstance(run, str) and (od == run or od.startswith(run + '_arm'))):", '):', ['CT06']),
    ('B03', 'W', '② outdir RUN_DIR_RE 뺌', '    if not (isinstance(od, str) and RUN_DIR_RE.fullmatch(od) and isinstance(run, str)',
     '    if not (isinstance(od, str) and isinstance(run, str)', ['CT06']),
    ('B04', 'W', '③ arms_read 대조 뺌', '    if not (type(ar) is list and not ar):', '    if False:', ['CT06']),
    ('B05', 'L', '③ arms_read 칸 없음 = 틀림 (한정 행 · 칸 없는 고정물이 잡아야)', "    ar = rr.get('arms_read', [])", "    ar = rr.get('arms_read')", ['CT06']),
    ('B06', 'W', '④ GU 끝 기록 대조 뺌', "    if code == 'GROUP_UNCONFIRMED':\n        cf = chain_confirmed(folder, run)",
     "    if False:\n        cf = chain_confirmed(folder, run)", ['CT06']),
    ('B07', 'L', '④ GU = 확인 True 요구 (뒤집음 · 생산자 꼴 거부)', '        if cf is not None and cf is not False:', '        if cf is not None and cf is not True:',
     ['CT06']),
    ('B08', 'W', 'chain_confirmed: by recover = 못 읽음 (chain_end 안 봄)', "        v = ce.get('confirmed')", '        return None', ['CT06']),
    ('B09', 'W', 'chain_confirmed: by chain = 못 읽음', "    if by == 'chain':\n        v = er.get('confirmed')", "    if by == 'chain':\n        return None",
     ['CT06']),
    ('B10', 'W', "chain_confirmed: 꼴 틀린 값 = 못 읽음 ('bad' → None)", "    return v if type(v) is bool else 'bad'", '    return v if type(v) is bool else None',
     ['CT06']),
    ('B11', 'W', 'chain_confirmed: 모르는 by = 못 읽음', "    else:\n        return 'bad'\n    return v if type(v) is bool",
     "    else:\n        return None\n    return v if type(v) is bool", ['CT06']),
    ('B12', 'W', 'chain_confirmed: chain_end 객체 아님 = 못 읽음', "        if not isinstance(ce, dict):\n            return 'bad'",
     "        if not isinstance(ce, dict):\n            return None", ['CT06']),
    ('B13', 'W', 'stop_record_problem 이 기록 안 대조를 안 부름', '    why = stopped_record_problem(s, folder, code, run, rr)', '    why = None', ['CT06']),
    ('B14', 'W', '② 요청 칸 정확한 outdir 대조 뺌 (접두만)', '    if want is not None and od != want:', '    if False:', ['CT06']),
    ('B15', 'W', 'record_outdir: 꼴 틀린 요청 칸 = 대조 안 함 (None)', "        return ''\n    return name + run_outdir_suffix(n, al)",
     '        return None\n    return name + run_outdir_suffix(n, al)', ['CT06']),
    ('B16', 'W', 'record_outdir: arm_list 무시', '    return name + run_outdir_suffix(n, al)', '    return name + run_outdir_suffix(n, None)', ['CT06']),
    ('B17', 'L', 'record_outdir: 요청 칸 없는 기록 = 틀림 (한정 행 · 칸 없는 고정물이 잡아야)', "    if 'arms' not in rr:\n        return None",
     "    if 'arms' not in rr:\n        return ''", ['CT06']),
    ('B18', 'W', 'record_outdir: bool arms 받음', '    if not (isinstance(name, str) and type(n) is int and',
     '    if not (isinstance(name, str) and isinstance(n, int) and', ['CT06']),
    # ── P3-5 단계 요약 칸 꼴 (summary_shape_problem)
    ('C01', 'W', 'result_fields 가 칸 꼴 대조를 안 부름', '        why = summary_shape_problem(s)', '        why = None', ['CT07']),
    ('C02', 'W', 'stop 꼴 안 봄', '    if st is not None and not isinstance(st, dict):', '    if False:', ['CT07']),
    ('C03', 'W', 'runs 목록 꼴 안 봄 (원소 대조는 남음)', "    if not isinstance(runs, list):\n        return f'runs =", "    if False:\n        return f'runs =",
     ['CT07']),
    ('C04', 'W', 'runs 원소 객체 꼴 안 봄', "        if not isinstance(r, dict):\n            return f'runs[{i}]", "        if False:\n            return f'runs[{i}]",
     ['CT07']),
    ('C05', 'W', 'outdir 꼴 안 봄', '        if od is not None and not isinstance(od, str):', '        if False:', ['CT07']),
]


def sha(f):
    return hashlib.sha256((MT / f).read_bytes()).hexdigest()


def run(only):
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    t0 = time.time()
    p = subprocess.run([sys.executable, '-B', TST, '--only', only], cwd=str(MT), capture_output=True, text=True, env=env, timeout=3600)
    return p.returncode, p.stdout + p.stderr, time.time() - t0


if (MT / '.git').exists():
    sys.exit('사본 나무여야 한다 (git 저장소 아님)')
start = {f: sha(f) for f in (RRF, TST)}
res = {'_only': ONLY}
rc, out, dt = run(ONLY)
res['BASE'] = {'rc': rc, 'summary': (re.findall(r'test_rint_r_chain: .*', out) or [''])[-1], 'seconds': round(dt, 1)}
print('BASE', res['BASE'], flush=True)
for mid, kind, item, old, new, want in M:
    if SEL is not None and mid not in SEL:
        continue
    txt = (MT / RRF).read_bytes().decode('utf-8')
    if txt.count(old) != 1:
        res[mid] = {'kind': kind, 'item': item, 'status': 'SKIP', 'why': f'count {txt.count(old)}'}
        print(mid, 'SKIP', txt.count(old), flush=True)
        continue
    try:
        (MT / RRF).write_bytes(txt.replace(old, new).encode('utf-8'))
        rc, out, dt = run(ONLY)
    finally:
        (MT / RRF).write_bytes(txt.encode('utf-8'))
    failed = sorted(set(re.findall(r'^  FAIL  (\S+)', out, re.M)))
    st = 'SURVIVED' if rc == 0 else ('KILLED' if set(want) & set(failed) else 'KILLED_OTHER')
    res[mid] = {'kind': kind, 'item': item, 'status': st, 'want': want, 'failed': failed, 'seconds': round(dt, 1)}
    print(mid, kind, item, st, failed, f'{dt:.1f}s', flush=True)
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
end = {f: sha(f) for f in (RRF, TST)}
res['_tree'] = {'start_sha256': start, 'end_sha256': end, 'restored': start == end}
n = [k for k in res if not k.startswith('_') and k != 'BASE']
res['_count'] = {'total': len(n), 'killed': sum(res[k]['status'] == 'KILLED' for k in n),
                 'killed_other': [k for k in n if res[k]['status'] == 'KILLED_OTHER'],
                 'survived': [k for k in n if res[k]['status'] == 'SURVIVED'], 'skipped': [k for k in n if res[k]['status'] == 'SKIP']}
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('count', res['_count'], 'restored', res['_tree']['restored'])
