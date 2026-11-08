"""변이 시험 (사전 공격 14 고침) — 새 조건을 하나씩 지우거나 약하게 한 rint_r_chain.py (고친 판) 로 만든 뿌리 (scripts = 작업 트리 링크 + 변이 사슬 + 고친 시험 사본 ·
docs 링크) 에서 `test_rint_r_chain.py --only PA14,PA13` → 잡힘 (실패 ≥ 1) / 놓침.  M00 = 변이 없음 (8/8 통과여야).  P3-f 넷 = 사전 공격 14 의 생존 변이 (같은 바꿈
· `../preattack14/probes/mutate.py` M14 · M18 · M47 · M54) 를 고친 판에 다시.  동치 (뜻이 같아 어떤 입력도 못 가름) = 목록 밖 · 보고에 적는다.
쓰임: python3 mutate_pa14.py <작업 트리> <결과 폴더> [일꾼 수]"""
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

WT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
WORKERS = int(sys.argv[3]) if len(sys.argv) > 3 else 2
ORIG = (WT / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
TEST = WT / 'scripts' / 'test_rint_r_chain.py'
SEL = 'PA14,PA13'

MUTS = [
    #  ── P3-a (arm_public_value_problem · conv_ok 앞 _num · 사유 _show) ──
    ('A01_num_guard_drop', "        if not _num(r):                                   # ★ 11-09 사전 공격 14 P3-a",
     "        if False:                                   # ★ 11-09 사전 공격 14 P3-a"),
    ('A02_show_iters_repr', "            return f'{k} {_show(v)} (= null · 0 이상 int)'", "            return f'{k} {v!r} (= null · 0 이상 int)'"),
    ('A03_show_cginfo_repr', "return f'cg_info {_show(a.get(\"cg_info\"))} · cg_resid", "return f'cg_info {a.get(\"cg_info\")!r} · cg_resid"),
    ('A04_show_guard_repr', "            return f'cg_resid {_show(r)} (positive = 유한 수", "            return f'cg_resid {r!r} (positive = 유한 수"),
    #  ── P3-d (생산자 값 꼴) ──
    ('D01_pid_prefix_only', "    if not (type(pid) is str and ARM_PID_RE.fullmatch(pid)):", "    if not (type(pid) is str and pid.startswith(RC.CA_EXT_PREFIX + '-')):"),
    ('D02_pid_match_not_full', "    if not (type(pid) is str and ARM_PID_RE.fullmatch(pid)):", "    if not (type(pid) is str and ARM_PID_RE.match(pid)):"),
    ('D03_pid_upper_ok', "ARM_PID_RE = re.compile(re.escape(RC.CA_EXT_PREFIX) + r'-[0-9a-f]{16}')",
     "ARM_PID_RE = re.compile(re.escape(RC.CA_EXT_PREFIX) + r'-[0-9a-fA-F]{16}')"),
    ('D04_pid_len_loose', "ARM_PID_RE = re.compile(re.escape(RC.CA_EXT_PREFIX) + r'-[0-9a-f]{16}')",
     "ARM_PID_RE = re.compile(re.escape(RC.CA_EXT_PREFIX) + r'-[0-9a-f]{1,}')"),
    ('D05_sid_nonempty_only', "    if not (type(sid) is str and ARM_SID_RE.fullmatch(sid)):", "    if not (type(sid) is str and sid):"),
    ('D06_sid_match_not_full', "    if not (type(sid) is str and ARM_SID_RE.fullmatch(sid)):", "    if not (type(sid) is str and ARM_SID_RE.match(sid)):"),
    ('D07_sid_upper_ok', "ARM_SID_RE = re.compile(r'[0-9a-f]{32}')", "ARM_SID_RE = re.compile(r'[0-9a-fA-F]{32}')"),
    ('D08_sid_len16_ok', "ARM_SID_RE = re.compile(r'[0-9a-f]{32}')", "ARM_SID_RE = re.compile(r'[0-9a-f]{16,32}')"),
    ('D09_err_tau_drop', "    if e > SVCF.CERT_TARGET_TOL:\n", "    if False:\n"),
    ('D10_err_tau_ge', "    if e > SVCF.CERT_TARGET_TOL:\n", "    if e >= SVCF.CERT_TARGET_TOL:\n"),
    ('D11_err_tau_x10', "    if e > SVCF.CERT_TARGET_TOL:\n", "    if e > 10 * SVCF.CERT_TARGET_TOL:\n"),
    #  ── P3-e (resume_rerun_problem · 칸 집합) ──
    ('E01_keyset_drop', "    if set(R) != set(RESUME_KEYS):", "    if False:"),
    ('E02_keyset_allow_extra', "    if set(R) != set(RESUME_KEYS):", "    if not set(RESUME_KEYS) <= set(R):"),
    ('E03_keyset_allow_missing', "    if set(R) != set(RESUME_KEYS):", "    if not set(R) <= set(RESUME_KEYS):"),
    ('E04_keys_no_det', "RESUME_KEYS = ('from', 'copied', 'rerun', 'compared', 'determinism')", "RESUME_KEYS = ('from', 'copied', 'rerun', 'compared')"),
    #  ── P3-f (사전 공격 14 생존 넷 · 같은 바꿈) ──
    ('M14_copiedfrom_type', "type(r['copied_from']) is int and r['copied_from'] == frm", "r['copied_from'] == frm"),
    ('M18_rr_det_only', "if cmp_ != [] or det is not None:", "if det is not None:"),
    ('M47_mm_elem_type', "if not (type(x) is dict and x.get('same') is True)]", "if not (x.get('same') is True)]"),
    ('M54_lo_one', "lo = ro if ro is not None else 1", "lo = 1"),
]


def run_one(item):
    nm, old, new = item
    if old is None:
        text = ORIG
    else:
        n = ORIG.count(old)
        if n != 1:
            return nm, 'SKIP', f'old occurs {n}', []
        text = ORIG.replace(old, new)
    root = OUT / 'roots' / nm
    src = OUT / 'srcs' / f'{nm}.py'
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(text, encoding='utf-8')
    make_tree(WT, root, src, TEST)
    tmp = OUT / 'tmp' / nm
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(tmp))
    r = subprocess.run([sys.executable, str(root / 'scripts' / 'test_rint_r_chain.py'), '--only', SEL], cwd=str(tmp), env=env,
                       capture_output=True, text=True, timeout=1800)
    fails = re.findall(r'^  FAIL  (\S+)', r.stdout, re.M)
    summ = [ln for ln in r.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
    shutil.rmtree(root, ignore_errors=True)
    shutil.rmtree(tmp, ignore_errors=True)
    verdict = ('PASS_ALL' if not fails and r.returncode == 0 else 'FAILS') if old is None else ('CAUGHT' if fails else 'MISSED')
    return nm, verdict, summ[-1] if summ else (r.stdout[-300:] + r.stderr[-300:]), fails


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = {}
    first = run_one(('M00_identity', None, None))
    res[first[0]] = first[1:]
    print(*first, flush=True)
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for nm, verdict, summ, fails in ex.map(run_one, MUTS):
            res[nm] = (verdict, summ, fails)
            print(nm, verdict, fails, summ, flush=True)
    n = len(MUTS)
    caught = sum(1 for k, v in res.items() if k != 'M00_identity' and v[0] == 'CAUGHT')
    skipped = sum(1 for k, v in res.items() if v[0] == 'SKIP')
    print(f'\n변이 {n} · 잡힘 {caught} · 놓침 {n - caught - skipped} · 건너뜀 {skipped} · 변이 없음 {res["M00_identity"][0]}', flush=True)
    (OUT / 'mutation_results.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
