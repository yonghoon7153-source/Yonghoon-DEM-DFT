#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② 끝-끝 E18 (11-03 · 실물 판정 → 다시 판정 · 1저자 11-03 밤 Q2) — 판정 · 다시 판정 가드를 하나씩 끄는 변이 → 새 시험 E18 이 옳은 이유로 실패하나.
PC7 고침 변이 틀 (`docs/reviews/rint2_rr_fix_evidence_20261023/pc7_fix/mutate_pc7fix.py`) 과 같은 꼴: 사본 트리 (scripts 복사 · docs · webapp = 링크) ·
변이마다 scripts/rint_r_chain.py 를 원본에서 다시 쓰고 옛 글 (정확히 한 번) 을 바꾼 뒤 `scripts/test_rint_r_chain_e2e.py --only E18` · rc ≠ 0 = 잡힘 ·
'BASE' = 변이 없음 · 'V0' = 판정 단계 없음 (새 시험이 판정 단계 없이 실패하는지 = 시험 먼저 증거).  값 · σ 를 화면에 내지 않는다 (시험 자신의 봉인 대조 그대로).

  python3 mutate_e18.py <원 트리> <사본 트리 바탕 (없으면 만든다)> <결과 json> <로그 폴더> [id,…]
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

#: (id, 끈 가드, 옛 글 (정확히 한 번), 새 글, 잡아야 할 검사 (기대 · 보고용))
MUTS = [
    ('V0', '판정 단계 없음 — stage_verdict = rc 0 · 아무것도 안 씀 (판정 · 다시 판정 둘 다)',
     'def stage_verdict(a, contract):\n    if a.reverify:', 'def stage_verdict(a, contract):\n    return 0\n    if a.reverify:', 'E18b'),
    ('V1', '다시 판정 없음 — reverify = rc 0 (다시 계산 · 바이트 대조 · 보고 없음)',
     '    vdir = Path(vdir)\n', '    return 0\n    vdir = Path(vdir)\n', 'E18c'),
    ('V2', '다시 판정 바이트 대조 끔 (늘 같음)',
     '    same = new_pub == old_pub and new_res == old_res\n', '    same = True\n', 'E18e'),
    ('V3', '다시 판정이 결과 JSON 을 대조하지 않음 (공개 JSON 만)',
     '    same = new_pub == old_pub and new_res == old_res\n', '    same = new_pub == old_pub\n', 'E18i'),
    ('V4', '판정의 킷 다시 해시 (bed_problem) 끔',
     "    pub['bed'] = bed_problem(s0r0, root, (SBE_KIT, DBE_KIT))\n", "    pub['bed'] = None\n", 'E18f'),
    ('V5', '판정의 원장 대조 (ledger_verdict_check) 끔',
     "        lpub = ledger_verdict_check(dirs, ledger['path'], ledger.get('attempt_dirs') or (), ledger['commit'])\n", '        lpub = None\n', 'E18g'),
    ('V6', '판정 기록에 등록 sha256 을 싣지 않음',
     "'sha256': reg_sha, 'plan_hash': plan_hash", "'sha256': None, 'plan_hash': plan_hash", 'E18h'),
    ('V7', '다시 판정 보고의 등급 다름 = 늘 False',
     "'original': g0, 'recomputed': g1, 'grade_differ': g0 != g1,", "'original': g0, 'recomputed': g1, 'grade_differ': False,", 'E18e'),
    ('V8', '판정 환경 옆 파일 (verdict_env.json) 안 씀',
     "    write_json(out / VERDICT_ENV_FILE, {'schema': VERDICT_ENV_SCHEMA, 'env': env_record(), 'utc': _utc()})\n", '    pass\n', 'E18b'),
    ('V9', '값 봉인 끔 — 판정이 --show-results 없이도 결과를 화면에',
     '    if a.show_results:\n', '    if True:\n', 'E18b'),
    ('V10', '다시 판정 보고의 다른 결과 칸 이름 = 늘 빈 목록',
     "'results_differ': (old_res is None) != (res is None) or (r0 != r1), 'results_keys_differ': rkeys,",
     "'results_differ': (old_res is None) != (res is None) or (r0 != r1), 'results_keys_differ': [],", 'E18i'),
]
FAIL_RE = re.compile(r'^\s*FAIL\s+(E18\w*)\s+(.*)$')


def make_tree(wt, base):
    tree = base / 'tree'
    if tree.exists():
        return tree
    tree.mkdir(parents=True)
    shutil.copytree(wt / 'scripts', tree / 'scripts', symlinks=True, ignore=shutil.ignore_patterns('__pycache__'))
    for nm in ('docs', 'webapp'):
        (tree / nm).symlink_to(wt / nm, target_is_directory=True)
    if (wt / '.gitignore').exists():
        shutil.copy2(wt / '.gitignore', tree / '.gitignore')
    return tree


def run_one(tree, mid, env, logd):
    t0 = time.time()
    p = subprocess.run(['nice', '-n', '10', sys.executable, str(tree / 'scripts' / 'test_rint_r_chain_e2e.py'), '--only', 'E18'],
                       capture_output=True, text=True, env=env, cwd=str(tree))
    (logd / f'{mid}.log').write_text(p.stdout + ('\n--- stderr ---\n' + p.stderr if p.stderr.strip() else ''), encoding='utf-8')
    tail = [ln for ln in p.stdout.splitlines() if ln.startswith('test_rint_r_chain_e2e:')]
    fails = [m.group(1) for m in (FAIL_RE.match(ln) for ln in p.stdout.splitlines()) if m]
    return p.returncode, (tail[-1] if tail else (p.stdout[-300:] + p.stderr[-300:])), fails, round(time.time() - t0, 1)


def main():
    wt, base, outp, logd = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]), Path(sys.argv[4])
    pick = set(sys.argv[5].split(',')) if len(sys.argv) > 5 else None
    logd.mkdir(parents=True, exist_ok=True)
    tree = make_tree(wt, base)
    src = (wt / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
    dst = tree / 'scripts' / 'rint_r_chain.py'
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    todo = [('BASE', '변이 없음', None, None, '')] + MUTS
    if pick:
        todo = [m for m in todo if m[0] in pick]
    res = json.loads(outp.read_text(encoding='utf-8')) if outp.exists() else []
    done = {r['id'] for r in res}
    try:
        for mid, why, old, new, want in todo:
            if mid in done:
                continue
            if old is None:
                dst.write_text(src, encoding='utf-8')
            else:
                n = src.count(old)
                if n != 1:
                    res.append({'id': mid, 'why': why, 'error': f'옛 글 {n} 번'})
                    outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
                    print(mid, 'ERROR', f'옛 글 {n} 번', flush=True)
                    continue
                mutated = src.replace(old, new, 1)
                compile(mutated, 'rint_r_chain.py', 'exec')
                dst.write_text(mutated, encoding='utf-8')
            rc, tail, fails, sec = run_one(tree, mid, env, logd)
            r = {'id': mid, 'why': why, 'rc': rc, 'killed': (rc != 0) if old is not None else None, 'want': want or None,
                 'want_hit': (want in fails) if want else None, 'tail': tail, 'fails': fails, 'seconds': sec}
            res.append(r)
            outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
            print(mid, 'rc', rc, tail, fails, f'{sec}s', flush=True)
    finally:
        dst.write_text(src, encoding='utf-8')


if __name__ == '__main__':
    main()
