#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""피복 단계 CLI 가 실행 위치 기준 추적 파일을 덮어쓰지 않는다 — 원장 LHS-27.

  python3 scripts/test_coverage_cli_no_tracked_write.py      # 종료코드 0 = PASS

결함 (LHS-27 · 09-30 5번 배치 193/194 dirty): `coverage_physics_vs_hertzian.py <case_id>` 가 끝에서 요약 CSV 를
`Path('docs/figures/physics_regime')/coverage_hertz_vs_physics_summary.csv` (**실행 위치 기준** · 리포에서는 추적 파일) 에 매번 덮어썼다 —
리포 루트에서 도는 웹앱 파이프라인 · LHS 배치가 그 파일을 바꿔 run 의 dirty = true 를 만들었다 (코드가 바뀌지 않았는데 '깨끗한 봉인 커밋에서
돌았다' 는 증명이 무너진다) · 케이스를 여럿 돌면 마지막 케이스 요약만 남았다.
처방: 요약 CSV 는 **명시적 `--summary-out PATH`** 일 때만 쓴다 (기본 = 아무 파일도 안 쓴다 · 화면 출력은 그대로).  배치 쪽 dirty 판정에서 이 파일만
예외로 두는 것은 하지 않는다 (가림 — 원장 note).

★ 시험 먼저 — 옛 코드 (a0a24c538): ① 실행 위치의 추적 파일 자리가 덮인다 ② 새 파일 (docs/figures/…) 이 생긴다 ③ `--summary-out` 을 모른다 (rc 2).
  C1 rc 0 · C2 추적 파일 자리 바이트 그대로 · C3 실행 위치에 아무것도 새로 생기지 않는다 · C4 `--summary-out` = 그 경로에만 · 행 = 케이스 × 상 ·
  C5 `--all` 도 기본은 안 쓴다 · C6 케이스의 피복 값 (full_metrics) 은 그대로 쓴다 (이 수정은 출력 경로만 바꾼다)
"""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPT = os.path.join(HERE, 'coverage_physics_vs_hertzian.py')
TRACKED = os.path.join('docs', 'figures', 'physics_regime', 'coverage_hertz_vs_physics_summary.csv')
_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}' + (f'   {extra}' if extra else ''))
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {extra}' if extra else ''))
    return bool(cond)


def _tree(root):
    return sorted(str(p.relative_to(root)) for p in Path(root).rglob('*'))


def main():
    sys.path.insert(0, HERE)
    import coverage_physics_vs_hertzian as CV
    tmp = Path(tempfile.mkdtemp(prefix='lhs27_'))
    try:
        data = tmp / 'data'
        res, up = data / 'results', data / 'uploads'
        cids = ('lhs27_a', 'lhs27_b')
        for cid in cids:
            cd, _tm, _sc = CV._selftest_fixture(res / cid)
            (up / cid).mkdir(parents=True, exist_ok=True)
            shutil.copy2(cd / 'meta.json', up / cid / 'meta.json')
        cwd = tmp / 'repo_like'                                   # 리포 루트처럼 — 추적 파일 자리에 표지 내용을 둔다
        (cwd / os.path.dirname(TRACKED)).mkdir(parents=True)
        sentinel = b'case_id,name,am_type\nTRACKED,do-not-touch,AM_P\n'
        (cwd / TRACKED).write_bytes(sentinel)
        before = _tree(cwd)
        env = dict(os.environ, WEBAPP_RESULTS_FOLDER=str(res), WEBAPP_UPLOAD_FOLDER=str(up),
                   WEBAPP_ARCHIVE_FOLDER=str(data / 'archive'), PYTHONDONTWRITEBYTECODE='1')

        def run(*args):
            return subprocess.run([sys.executable, SCRIPT, *args], cwd=str(cwd), env=env, capture_output=True, text=True,
                                  timeout=600)

        p = run(*cids)
        chk('C1 기본 실행 rc 0 (케이스 둘)', p.returncode == 0, (p.stderr or '')[-300:])
        chk('C2 ★ 실행 위치의 추적 파일 자리 (docs/figures/physics_regime/…summary.csv) 바이트 그대로',
            (cwd / TRACKED).read_bytes() == sentinel, (cwd / TRACKED).read_bytes()[:120])
        after = _tree(cwd)
        chk('C3 ★ 실행 위치에 새 파일 · 폴더가 생기지 않는다', after == before, f'새로 생김 {sorted(set(after) - set(before))}')
        empty = tmp / 'empty_cwd'
        empty.mkdir()
        pe = subprocess.run([sys.executable, SCRIPT, cids[0]], cwd=str(empty), env=env, capture_output=True, text=True,
                            timeout=600)
        chk('C3b ★ 빈 실행 위치에서도 아무것도 만들지 않는다 (옛 코드는 docs/figures/physics_regime/ 를 새로 만들었다)',
            pe.returncode == 0 and _tree(empty) == [], f'rc={pe.returncode} · 생김 {_tree(empty)}')
        fm = json.loads((res / cids[0] / 'full_metrics.json').read_text())
        chk('C6 케이스 피복 값은 그대로 쓴다 (legacy physics · v2 · 합집합 상태)',
            isinstance(fm.get('coverage_AM_P_mean_physics'), float) and fm.get('coverage_status_physics_v2') == 'ok'
            and 'coverage_status_physics_union' in fm, repr({k: fm.get(k) for k in ('coverage_AM_P_mean_physics',
                                                                                      'coverage_status_physics_v2')}))
        out = tmp / 'elsewhere' / 'summary.csv'
        p2 = run(*cids, '--summary-out', str(out))
        rows = list(csv.DictReader(open(out))) if out.exists() else []
        chk('C4 ★ --summary-out PATH = 그 경로에만 쓴다 (케이스 둘 × 상 둘 = 4 행) · 추적 파일 자리는 그대로',
            p2.returncode == 0 and len(rows) == 4 and {r['case_id'] for r in rows} == set(cids)
            and (cwd / TRACKED).read_bytes() == sentinel and _tree(cwd) == before,
            f'rc={p2.returncode} · 행 {len(rows)} · {(p2.stderr or "")[-200:]}')
        p3 = run('--all')
        chk('C5 --all 도 기본은 요약 파일을 안 쓴다 (rc 0 · 실행 위치 그대로)',
            p3.returncode == 0 and (cwd / TRACKED).read_bytes() == sentinel and _tree(cwd) == before,
            f'rc={p3.returncode} · {(p3.stderr or "")[-200:]}')
        src = open(SCRIPT, encoding='utf-8').read()
        chk('C7 소스에 실행 위치 기준 docs/figures 쓰기가 없다 (Path(\'docs/figures/physics_regime\') 옛 줄)',
            "Path('docs/figures/physics_regime')" not in src)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for f in _fail:
            print('  -', f)
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
