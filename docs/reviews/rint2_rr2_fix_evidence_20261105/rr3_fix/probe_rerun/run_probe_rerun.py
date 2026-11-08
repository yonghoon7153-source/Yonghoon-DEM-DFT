#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Codex 회차 ③ 탐침 `pc12_attack/probe_pc12_independent.py` 다시 (RR3-01 고친 작업 트리) — 탐침 = 반입 증거 원본 바이트 (sha256 = EVIDENCE_MANIFEST 7f335c75…)
를 리포 밖 스크래치로 복사해 `python3 -I -B -X utf8` · cwd = 리포 밖 빈 폴더 · RINT_REVIEW_REPO = 작업 트리.
  ① 원본 그대로 — 기대 = RR3-01 존재 assert (원장 다음 항목 None · 편집 뒤 resume_ok True) 에서 AssertionError · rc 1 (기대한 뒤집힘 · REPRODUCE.md "현 반례
     존재 assert 를 조용히 PASS 로 바꾸지 않는다")
  ② 거부 oracle 사본 — 그 assert 두 줄만 거부 oracle 로 (원장 다음 항목 = RESUME_NOT_ALLOWED · 편집 뒤 resume_ok False · stop_record_problem 사유 있음) · 그 밖 바이트
     그대로 (차이 = oracle.diff) → 끝까지 돌아 results.json → 우리 고치기 전 재현 (`_repro_ours_20261108/pc12_attack/results.json` · 같은 기계 · 같은 탐침) 과 잎 대조.

  python3 -I -B run_probe_rerun.py <작업 트리> <스크래치 폴더> <출력 폴더>
"""
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO, SCR, OUT = (Path(x).resolve() for x in sys.argv[1:4])
EV = REPO / 'docs' / 'reviews' / 'codex_rint2_rr_round3_evidence_20261108'
PROBE = EV / 'pc12_attack' / 'probe_pc12_independent.py'
PROBE_SHA = '7f335c758c036c6de5ab10ef5b9ab3d35d6eb10ab3f0182694bdea03914b74d7'
BEFORE = EV / '_repro_ours_20261108' / 'pc12_attack'
ORACLE = [
    ("    assert ledger_rows[1]['attempt_order_problem'] is None\n",
     "    assert ledger_rows[1]['attempt_order_problem'][0]=='RESUME_NOT_ALLOWED'   # RR3-01 고침 뒤 거부 oracle (원 = is None)\n"),
    ("    assert before['resume_ok'] is False and after['resume_ok'] is True and problem is None\n",
     "    assert before['resume_ok'] is False and after['resume_ok'] is False and problem is not None   # RR3-01 고침 뒤 거부 oracle (원 = True · None)\n"),
]


def run(script, tag):
    cwd = SCR / f'cwd_{tag}'
    cwd.mkdir(parents=True)
    env = dict(os.environ, RINT_REVIEW_REPO=str(REPO))
    p = subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8', str(script)], cwd=str(cwd), env=env, capture_output=True, text=True)
    (OUT / f'{tag}.stdout.log').write_text(p.stdout, encoding='utf-8')
    (OUT / f'{tag}.stderr.log').write_text(p.stderr, encoding='utf-8')
    (OUT / f'{tag}.rc.json').write_text(json.dumps({'rc': p.returncode, 'python': sys.version, 'cmd': f'RINT_REVIEW_REPO=<작업 트리> {sys.executable} -I -B -X utf8 '
                                                     f'<스크래치>/{tag}/pc12_attack/{script.name}'}, ensure_ascii=False), encoding='utf-8')
    return p.returncode, p.stderr


def leaves(x, path=''):
    if isinstance(x, dict):
        for k in sorted(x):
            yield from leaves(x[k], f'{path}/{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, f'{path}[{i}]')
    else:
        yield path, x


def main():
    raw = PROBE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PROBE_SHA, '탐침 바이트가 반입 원본이 아니다'
    OUT.mkdir(parents=True, exist_ok=True)
    rep = {'probe_sha256': PROBE_SHA, 'repo': '<작업 트리>', 'chain_sha256': hashlib.sha256((REPO / 'scripts' / 'rint_r_chain.py').read_bytes()).hexdigest()}
    d1 = SCR / 'orig' / 'pc12_attack'
    d1.mkdir(parents=True)
    (d1 / PROBE.name).write_bytes(raw)
    rc1, err1 = run(d1 / PROBE.name, 'orig')
    last = [ln for ln in err1.strip().splitlines()[-3:]]
    rep['orig'] = {'rc': rc1, 'stderr_tail': last, 'copy_sha256_same': hashlib.sha256((d1 / PROBE.name).read_bytes()).hexdigest() == PROBE_SHA}
    txt = raw.decode('utf-8')
    for old, new in ORACLE:
        assert txt.count(old) == 1, old
        txt = txt.replace(old, new)
    d2 = SCR / 'oracle' / 'pc12_attack'
    d2.mkdir(parents=True)
    (d2 / 'probe_rr3_oracle.py').write_text(txt, encoding='utf-8')
    diff = ''.join(difflib.unified_diff(raw.decode('utf-8').splitlines(True), txt.splitlines(True), 'probe_pc12_independent.py (원본)', 'probe_rr3_oracle.py'))
    (OUT / 'oracle.diff').write_text(diff, encoding='utf-8')
    rc2, err2 = run(d2 / 'probe_rr3_oracle.py', 'oracle')
    rep['oracle'] = {'rc': rc2, 'stderr_tail': err2.strip().splitlines()[-3:] if err2.strip() else []}
    for nm in ('results.json', 'chain_side_rows.json', 'counterexample_original_summary.json', 'counterexample_edited_summary.json',
               'counterexample_original_ledger.jsonl', 'counterexample_edited_ledger.jsonl'):
        if (d2 / nm).is_file():
            shutil.copy2(d2 / nm, OUT / nm)
    after = json.loads((d2 / 'results.json').read_text(encoding='utf-8')) if (d2 / 'results.json').is_file() else None
    before = json.loads((BEFORE / 'results.json').read_text(encoding='utf-8'))
    diffs = []
    if after is not None:
        a, b = dict(leaves(after)), dict(leaves(before))
        for k in sorted(set(a) | set(b)):
            if a.get(k, '<없음>') != b.get(k, '<없음>'):
                diffs.append({'leaf': k, 'before': b.get(k, '<없음>'), 'after': a.get(k, '<없음>')})
        rep['leaves'] = {'before': len(b), 'after': len(a), 'differ': len(diffs)}
        cs_b = json.loads((BEFORE / 'chain_side_rows.json').read_text(encoding='utf-8'))
        cs_a = json.loads((d2 / 'chain_side_rows.json').read_text(encoding='utf-8'))
        rep['chain_side_rows_same'] = cs_a == cs_b
        rep['chain_side_rows_n'] = [len(cs_b), len(cs_a)]
        t = after['tests']['prior_read_failure_promoted']
        rep['prior_read_failure_promoted'] = {
            'original_failure_code': t['original_failure']['code'],
            'original_result': [t['original_result']['cause'], t['original_result']['resume_ok']],
            'edited_result': [t['edited_result']['cause'], t['edited_result']['resume_ok']],
            'stop_record_problem_set': t['stop_record_problem'] is not None,
            'ledger_attempt_order': [(r['label'], r['parsed_result_resume_ok'], (r['attempt_order_problem'] or [None])[0], r['result_line_problem'])
                                     for r in t['ledger_policy']],
            'source_done': t['source_done'], 'copy_read': (t['actual_copy_read_result'] or {}).get('code'),
            'producer_arms_read_keys': sorted(t['producer_records'][0]['arms_read'][0])}
    (OUT / 'leaf_diff.json').write_text(json.dumps(diffs, ensure_ascii=False, indent=1, default=repr), encoding='utf-8')
    (OUT / 'rerun_report.json').write_text(json.dumps(rep, ensure_ascii=False, indent=1, default=repr), encoding='utf-8')
    print(json.dumps(rep, ensure_ascii=False, indent=1, default=repr))
    return 0


if __name__ == '__main__':
    sys.exit(main())
