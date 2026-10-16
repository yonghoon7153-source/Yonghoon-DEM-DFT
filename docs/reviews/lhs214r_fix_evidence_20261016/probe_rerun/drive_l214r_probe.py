"""Codex 재검증 탐침 (LHS214 · 핀 9e3ef54ca) 을 다른 트리에서 무변경으로 다시 돈다 — L214R-01–04 수정 전 · 후 대조 (읽기 전용).

  리포 밖 새 폴더 OUT 에 Codex 묶음과 같은 꼴을 세운다:
    OUT/source = REV 의 파일 (Codex source_manifest 의 경로 ∩ REV 트리) ∪ (REV 의 scripts/*.py · webapp/**.py|js|html · Codex prepare_source 와 같은 규칙)
    OUT/base   = BASE (기본 0c557e72a = Codex 기준) 의 파일 (Codex base_manifest 의 경로 ∩ BASE 트리)
    OUT/probes = 리포에 반입된 Codex 탐침 다섯 (바이트 그대로 · sha256 = Codex package_manifest 대조)
  그 뒤 Codex README 순서대로 돈다 (python3 -E -X utf8 -B · 탐침 무변경 · -I 는 사용자 site 를 빼서 웹앱 import 가 안 된다):
    l214_numeric.py · l214_numeric.py --selftests · l214_consumers.py · --negative · --release ·
    l214_display.py --tree source --producers · l214_display.py --tree base · receipt_identity.py
  receipt_identity.py 는 결함의 존재를 assert 로 적어 두었다 (minimal_activate_section3 = {R0, D1}) — 고친 트리에서는 그 줄에서 멈추는 것이 고쳐짐의 표지다.
  변이 값을 적어 두려고 파생 탐침 receipt_identity_noassert.py (같은 변이 · 결함 · 결과를 적은 assert 일곱 줄만 뺌 · 머리에 표지) 도 돈다.
  l214_a4.py 는 Codex 핀 manifest 에 묶여 있어 돌리지 않는다 (무영향 대조는 리포의 a4 스크립트로 따로).

실행:  python3 -I drive_l214r_probe.py OUT REV [--base 0c557e72a]
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get('L214R_REPO') or '/home/user/Yonghoon-DEM-DFT'
BUNDLE = 'docs/reviews/codex_lhs214_fix_reverify_evidence_20261015'
PROBES = ('l214_numeric.py', 'l214_consumers.py', 'l214_display.py', 'receipt_identity.py', 'l214_a4.py')
RUNS = (
    ('numeric', ['probes/l214_numeric.py']),
    ('numeric_selftests', ['probes/l214_numeric.py', '--selftests']),
    ('consumers', ['probes/l214_consumers.py']),
    ('consumers_negative', ['probes/l214_consumers.py', '--negative']),
    ('consumers_release', ['probes/l214_consumers.py', '--release']),
    ('display_source', ['probes/l214_display.py', '--tree', 'source', '--producers']),
    ('display_base', ['probes/l214_display.py', '--tree', 'base']),
    ('receipt_identity', ['probes/receipt_identity.py']),
    ('receipt_identity_noassert', ['probes/receipt_identity_noassert.py']),
)


def git(*args, binary=False):
    p = subprocess.run(['git', '-C', REPO, *args], capture_output=True, check=True, timeout=600)
    return p.stdout if binary else p.stdout.decode('utf-8')


def tree_paths(rev):
    return set(git('ls-tree', '-r', '--name-only', '-z', rev).split('\0')) - {''}


def rule_paths(paths):
    out = set()
    for p in paths:
        if p.startswith('scripts/') and p.endswith('.py') and p.count('/') == 1:
            out.add(p)
        elif p.startswith('webapp/') and p.endswith(('.py', '.js', '.html')):
            out.add(p)
    return out


def extract(rev, paths, dest):
    paths = sorted(paths)
    os.makedirs(dest, exist_ok=False)
    # 경로 수가 많아 묶음으로 나눈다 (git archive 는 경로마다 tar 항목 하나 · 같은 rev).
    n = 0
    for i in range(0, len(paths), 400):
        chunk = paths[i:i + 400]
        data = git('archive', '--format=tar', rev, '--', *chunk, binary=True)
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            for m in tf.getmembers():
                if not (m.isfile() or m.isdir()):
                    raise SystemExit(f'⛔ archive member type {m.name}')
                if m.name.startswith('/') or '..' in m.name.split('/'):
                    raise SystemExit(f'⛔ archive member path {m.name}')
            tf.extractall(dest, filter='data')
            n += sum(1 for m in tf.getmembers() if m.isfile())
    return n


def sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def make_noassert(src, dst):
    text = open(src, encoding='utf-8').read()
    lines = text.splitlines(keepends=True)
    keep, dropped = [], []
    for ln in lines:
        if ln.startswith('assert ') and ("out['current_receipt']" in ln or "out['variants']" in ln or ln.strip() == 'assert rc==0'):
            dropped.append(ln.rstrip('\n'))
            continue
        keep.append(ln)
    head = ('# 파생 탐침 (메인 세션 · L214R 재실행) — Codex receipt_identity.py 와 같은 변이 · 같은 출력 파일 · '
            'assert 만 뺐다 (결함의 존재를 적은 줄이라 고친 트리에서 결과를 남기지 못한다):\n')
    head += ''.join(f'#   뺀 줄: {d}\n' for d in dropped)
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(head + ''.join(keep))
    return dropped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('rev')
    ap.add_argument('--base', default='0c557e72a')
    ap.add_argument('--prepare-only', action='store_true', help='꼴만 세우고 탐침은 돌리지 않는다')
    ap.add_argument('--run-only', action='store_true', help='이미 세운 OUT 에서 탐침만 돈다 (driver_summary.json 의 rev 와 같아야)')
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    if a.run_only:
        return run_probes(out, git('rev-parse', a.rev).strip())
    if os.path.exists(out):
        raise SystemExit(f'⛔ {out} 이미 있다 (새 빈 폴더만)')
    if os.path.commonpath([out, REPO]) == REPO:
        raise SystemExit('⛔ OUT 은 리포 밖이어야 한다')
    rev = git('rev-parse', a.rev).strip()
    base = git('rev-parse', a.base).strip()
    man_s = json.loads(git('show', f'{rev}:{BUNDLE}/source_manifest.json'))
    man_b = json.loads(git('show', f'{rev}:{BUNDLE}/base_manifest.json'))
    pkg = json.loads(git('show', f'{rev}:{BUNDLE}/package_manifest.json'))
    t_rev, t_base = tree_paths(rev), tree_paths(base)
    want_s = {r['path'] for r in man_s['files']}
    src_paths = (want_s & t_rev) | rule_paths(t_rev)
    missing_s = sorted(want_s - t_rev)
    want_b = {r['path'] for r in man_b['files']}
    base_paths = want_b & t_base
    os.makedirs(out)
    info = dict(rev=rev, base=base, repo_head=git('rev-parse', 'HEAD').strip(),
                source_files=extract(rev, src_paths, os.path.join(out, 'source')),
                base_files=extract(base, base_paths, os.path.join(out, 'base')),
                codex_source_paths_missing_at_rev=missing_s,
                codex_base_paths_missing_at_base=sorted(want_b - t_base))
    for d in ('probes', 'evidence', 'tmp', 'notes'):
        os.makedirs(os.path.join(out, d), exist_ok=True)
    pk = {}
    for row in pkg.get('files', pkg if isinstance(pkg, list) else []):
        if isinstance(row, dict) and 'path' in row:
            pk[row['path'].replace('\\', '/')] = row
    probe_sha = {}
    for name in PROBES:
        data = git('show', f'{rev}:{BUNDLE}/probes/{name}', binary=True)
        dst = os.path.join(out, 'probes', name)
        with open(dst, 'wb') as f:
            f.write(data)
        s = hashlib.sha256(data).hexdigest()
        ref = (pk.get(f'probes/{name}') or {}).get('sha256')
        probe_sha[name] = dict(sha256=s, codex_package_sha256=ref, same=(ref == s) if ref else None)
    info['probes'] = probe_sha
    info['noassert_dropped'] = make_noassert(os.path.join(out, 'probes', 'receipt_identity.py'),
                                             os.path.join(out, 'probes', 'receipt_identity_noassert.py'))
    with open(os.path.join(out, 'driver_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: info[k] for k in ('rev', 'base', 'source_files', 'base_files', 'probes', 'noassert_dropped',
                                            'codex_source_paths_missing_at_rev')}, ensure_ascii=False, indent=1))
    if a.prepare_only:
        return 0
    return run_probes(out, rev)


def run_probes(out, rev):
    with open(os.path.join(out, 'driver_summary.json'), encoding='utf-8') as f:
        info = json.load(f)
    if info['rev'] != rev:
        raise SystemExit(f"⛔ OUT 의 rev {info['rev'][:9]} ≠ {rev[:9]}")
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    rows = []
    for label, argv in RUNS:
        t0 = time.monotonic()
        # -E (PYTHON* 환경변수 무시) · -I 는 쓰지 않는다 — 사용자 site 의 requests 가 웹앱 import 에 필요하다 (-I 는 사용자 site 를 뺀다) ·
        # sys.path[0] = OUT/probes (우리가 복사한 Codex 탐침 다섯 + 파생 하나뿐) · cwd = 빈 OUT/tmp
        cmd = [sys.executable, '-E', '-X', 'utf8', '-B', os.path.join(out, argv[0]), *argv[1:]]
        p = subprocess.run(cmd, cwd=os.path.join(out, 'tmp'),
                           env=env, capture_output=True, timeout=5400)
        log = os.path.join(out, 'evidence', f'_driver_{label}.log')
        with open(log, 'wb') as f:
            f.write(p.stdout + b'\n--- stderr ---\n' + p.stderr)
        tail = (p.stdout + p.stderr).decode('utf-8', 'replace').strip().splitlines()[-3:]
        row = dict(label=label, argv=argv, rc=p.returncode, seconds=round(time.monotonic() - t0, 1), log=os.path.relpath(log, out), tail=tail)
        rows.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
    info['runs'] = rows
    with open(os.path.join(out, 'driver_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print(json.dumps({'rev': info['rev'], 'runs': [(r['label'], r['rc']) for r in rows]}, ensure_ascii=False))
    # rc 2 = 파이썬이 탐침을 열지 못함 · 인자 오류 (드라이버 결함) — 탐침 자신의 실패 (rc 1 · assert) 와 구별한다
    return 2 if any(r['rc'] == 2 for r in rows) else 0


if __name__ == '__main__':
    sys.exit(main())
