"""Codex 4차 탐침 — RGLR3 고친 트리 재실행 (10-06).  읽기 전용 · 캠페인 없음.

판정 묶음 (`docs/reviews/codex_rglr2_reverify_review_evidence_20261005/` — source 는 manifest 만 커밋됨) 을 OUT 으로 복사하고,
source/ 를 `git archive <REV>` 의 **같은 456 경로** 로 채운 뒤 run_probes.py (7 탐침) → 결함 단언만 뒤집은 new_probes 사본 → 원본 new_probes 를 돌린다.
원본 new_probes 는 결함이 **있음을** 단언하므로 고친 트리에서 AssertionError (rc 1) 가 정상이다.

    python3 docs/reviews/codex_rglr3_fix_probe_rerun_20261006/drive_fix_probe.py OUT_DIR [REV=HEAD]
"""
import json, shutil, subprocess, sys, time
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]
PKG = REPO / 'docs/reviews/codex_rglr2_reverify_review_evidence_20261005'
OLD40 = "assert tau[0]['accepted'] and tau[1]['accepted'] and tau[2]['accepted']"
NEW40 = "assert tau[0]['accepted'] and not tau[1]['accepted'] and not tau[2]['accepted']   # 고친 뒤: 띠 · σ₀ 사본 변조 = 거부 (RGLR3-02)"
OLD79 = "assert called and retry_rc==0 and retry_run['code_changed_during_run']==[] and retry_report['mixed_generation']==[]"
NEW79 = "assert not called and retry_rc==2 and retry_run is None   # 고친 뒤: 같은 HEAD dirty 재시도 = 워커 전 거부 · run_002 없음 (RGLR3-01)"


def main(out, rev='HEAD'):
    P = Path(out).resolve()
    if P.exists():
        raise SystemExit(f'{P} 가 이미 있다 — 새 폴더를 준다')
    shutil.copytree(PKG, P, ignore=shutil.ignore_patterns('evidence'))
    (P / 'evidence').mkdir()
    paths = [f['path'] for f in json.loads((PKG / 'source_manifest.json').read_text(encoding='utf8'))['files']]
    git = lambda *a: subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, check=True).stdout
    sha = git('rev-parse', rev).decode().strip()
    tracked = set(git('ls-tree', '-r', '-z', '--name-only', sha).decode().split('\0'))
    keep, missing = [p for p in paths if p in tracked], [p for p in paths if p not in tracked]
    (P / 'source').mkdir()
    subprocess.run(['tar', '-x', '-C', str(P / 'source')], input=git('archive', sha, '--', *keep), check=True)
    (P / 'source_rev.json').write_text(json.dumps(dict(rev=sha, n_paths=len(paths), n_kept=len(keep), missing_at_rev=missing), indent=1))
    lines = (P / 'probes/new_probes.py').read_text(encoding='utf8').split('\n')
    assert lines[39] == OLD40 and lines[78] == OLD79, '탐침 원본이 판정 묶음과 다르다'
    lines[39], lines[78] = NEW40, NEW79
    fixed = '\n'.join(lines).replace("save(E/'new_probes.json',res)", "save(E/'new_probes_after_fix.json',res)")
    assert fixed.count('new_probes_after_fix.json') == 1
    (P / 'probes/new_probes_after_fix.py').write_text(fixed, encoding='utf8')
    print('source', sha, len(keep), 'missing', missing, flush=True)
    rcs = {}
    for name, args in (('probes_all', ['run_probes.py']), ('new_probes_after_fix', ['probes/new_probes_after_fix.py']),
                       ('new_probes_original', ['probes/new_probes.py'])):
        t = time.monotonic()
        p = subprocess.run([sys.executable, *args], cwd=P, capture_output=True, text=True)
        (P / 'evidence' / f'driver_{name}.log').write_text(p.stdout + p.stderr, encoding='utf8')
        rcs[name] = p.returncode
        print(name, 'rc', p.returncode, f'{time.monotonic() - t:.0f}s', flush=True)
    ok = rcs == {'probes_all': 0, 'new_probes_after_fix': 0, 'new_probes_original': 1}
    print('기대 (0 · 0 · 1) =', ok)
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main(*sys.argv[1:]))
