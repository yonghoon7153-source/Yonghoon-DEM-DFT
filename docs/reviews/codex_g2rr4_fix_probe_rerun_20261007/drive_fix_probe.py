"""Codex 세대 2 재검증 4 탐침 — G2RR4-01 · 02 · 03 고친 트리 재실행 (10-07).  읽기 전용 · 194 생산 · DEM/MPM · 시뮬레이션 없음.

판정 묶음 `docs/reviews/codex_gen2_network_reverify4_evidence_20261007/` (source/ 는 manifest 만 · submitted/ 는 커밋된 사전 점검 tar) 을 OUT 에 다시 세운다:
  source/    = `git archive <REV>` 의 manifest 고유 경로 (446 · 중복 2 는 한 번)
  submitted/ = <REV> 의 `docs/reviews/codex_gen2_network_reverify4_precheck_20261007/*.tar.gz` 둘 (절대 경로 · `..` · 링크 · 장치 = 거부)
  probes/    = Codex 다섯 **무변경** + 이 폴더의 파생 탐침 둘 (release_gate_detailed · observation_cli_staged — 파일 머리에 무엇을 바꿨는지)
실행 = Codex README 순서 그대로 — `run_checks.py submitted_evidence scope194 case15_channels release_gate` → `observation_cli` → 파생 → 회귀 넷
(reread · publication · role · release).  각 run_checks 호출 = `python3 -I` · CWD = OUT 의 부모 (묶음 밖).

    python3 -I docs/reviews/codex_g2rr4_fix_probe_rerun_20261007/drive_fix_probe.py OUT_DIR [REV=HEAD]

기대 rc — 고친 트리 (REV ≠ 핀): 1 차 = 1 (submitted_evidence 탐침이 경로 번역 기준선에서 assert — 그 사본에 워커 케이스 기록 out/status.json 이 없어
'완료 시도의 실행 단계 기록이 없다' 3 · README §2) · observation_cli = 0 (탐침에 단언 없음 · 네 행 rc 는 JSON) · 파생 = 0 · 회귀 = 1 (test_lhs_release_v13 V16a —
git archive 사본에 .git 없음 · 나머지 셋 0).
핀 `87f0906a2` (전): 1 차 = 0 · observation_cli = 0 · 파생 = observation_cli_staged 만 0 (release_gate_detailed 는 고친 트리의 상세 픽스처 계약이라 건너뜀) · 회귀 = 1.
"""
import json, shutil, subprocess, sys, tarfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PKG = REPO / 'docs/reviews/codex_gen2_network_reverify4_evidence_20261007'
PRE = 'docs/reviews/codex_gen2_network_reverify4_precheck_20261007'
PIN = '87f0906a2674e7d4e8ec31ca98aed5b14babc293'
DERIVED = ('release_gate_detailed', 'observation_cli_staged')


def _safe_extract(tgz: Path, dest: Path):
    with tarfile.open(tgz) as t:
        for m in t.getmembers():
            parts = m.name.split('/')
            if m.name.startswith('/') or '..' in parts or not (m.isfile() or m.isdir()):
                raise SystemExit(f'tar 항목 거부: {tgz.name}: {m.name}')
            tgt = dest / m.name
            if m.isdir():
                tgt.mkdir(parents=True, exist_ok=True)
                continue
            tgt.parent.mkdir(parents=True, exist_ok=True)
            with t.extractfile(m) as s_, open(tgt, 'wb') as d_:
                shutil.copyfileobj(s_, d_)


def _load(p: Path):
    try:
        return json.loads(p.read_text(encoding='utf8'))
    except (OSError, ValueError):
        return None


def summarize(E: Path, rcs: dict, sha: str) -> dict:
    """증거 JSON 에서 판정 칸만 — 표 (README) 의 원천."""
    s = dict(rev=sha, batch_rc=rcs)
    rg = _load(E / 'release_gate.json')
    s['release_gate'] = [dict(label=c['label'], accepted=c['accepted'], error=(c.get('error') or '')[:240]) for c in (rg or {}).get('cases', [])]
    rgd = _load(E / 'release_gate_detailed.json')
    s['release_gate_detailed'] = [dict(label=c['label'], accepted=c['accepted'], check=c.get('check'), out_dir_exists=c.get('out_dir_exists'),
                                       fixture_shape=c.get('fixture_shape'), error=(c.get('error') or '')[:240]) for c in (rgd or {}).get('cases', [])]
    for name in ('observation_cli', 'observation_cli_staged'):
        rows = _load(E / f'{name}.json') or []
        s[name] = [dict(label=r['label'], rc=r['rc'], n_start=r.get('n_start'), n_final=r.get('n_final'), import_problems=r.get('import_problems'),
                        stage_binding={k: dict(executed=v.get('executed'), expected=v.get('expected'), observed=v.get('observed'))
                                       for k, v in (r.get('stage_binding') or {}).items()}) for r in rows]
    log = (E / 'submitted_evidence.log').read_text(encoding='utf8') if (E / 'submitted_evidence.log').exists() else ''
    s['submitted_evidence_baseline'] = [ln for ln in log.splitlines() if ln.startswith('PATH_TRANSLATED_BASELINE')]
    s['submitted_evidence_tail'] = log.splitlines()[-3:]
    c15 = _load(E / 'case15_channels.json') or {}
    s['case15'] = dict(plate_um=c15.get('plate_um'), atoms=c15.get('atoms'), contacts=c15.get('contacts'),
                       negative_rows=[(r['id1'], r['id2'], r['area_um2']) for r in c15.get('negative_area') or []],
                       channels={k: (v.get('value') if isinstance(v, dict) else v) for k, v in (c15.get('channels') or {}).items()})
    s['scope194'] = _load(E / 'scope194.json')
    runs = {}
    for p in sorted(E.glob('runs_*.json')):
        for row in _load(p) or []:
            runs[row['name']] = dict(rc=row['rc'], tail=row.get('tail'))
    s['runs'] = runs
    return s


def main(out, rev='HEAD'):
    P = Path(out).resolve()
    if P.exists():
        raise SystemExit(f'{P} 가 이미 있다 — 새 폴더를 준다')
    if REPO == P or REPO in P.parents:
        raise SystemExit(f'{P} 는 리포 안이다 — 리포 밖 폴더를 준다')
    git = lambda *a: subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, check=True).stdout
    sha = git('rev-parse', rev).decode().strip()
    is_pin = sha == PIN
    shutil.copytree(PKG, P, ignore=shutil.ignore_patterns('evidence', '_README_import.md', 'bundle_inventory.json'))
    E = P / 'evidence'
    E.mkdir()
    man = json.loads((PKG / 'source_manifest.json').read_text(encoding='utf8'))
    paths = sorted({f['path'] for f in (man['files'] if isinstance(man, dict) else man)})
    tracked = set(git('ls-tree', '-r', '-z', '--name-only', sha).decode().split('\0'))
    keep, missing = [p for p in paths if p in tracked], [p for p in paths if p not in tracked]
    S = P / ('sour' + 'ce')
    S.mkdir()
    subprocess.run(['tar', '-x', '-C', str(S)], input=git('archive', sha, '--', *keep), check=True)
    for tgz in sorted((S / PRE).glob('*.tar.gz')):
        dest = P / 'submitted' / tgz.name[:-len('.tar.gz')]
        dest.mkdir(parents=True)
        _safe_extract(tgz, dest)
    derived = [d for d in DERIVED if not (is_pin and d == 'release_gate_detailed')]
    for name in derived:
        shutil.copyfile(HERE / f'{name}.py', P / 'probes' / f'{name}.py')
    (P / 'source_rev.json').write_text(json.dumps(dict(rev=sha, is_pin=is_pin, n_paths=len(paths), n_kept=len(keep), missing_at_rev=missing,
                                                       derived=derived), indent=1), encoding='utf8')
    print('source', sha, 'pin' if is_pin else 'fixed', len(keep), 'missing', missing, flush=True)
    batches = (('first', ['submitted_evidence', 'scope194', 'case15_channels', 'release_gate']), ('observation', ['observation_cli']),
               ('derived', derived), ('regression', ['reread', 'publication', 'role', 'release']))
    expect = {'first': 0 if is_pin else 1, 'observation': 0, 'derived': 0, 'regression': 1}
    rcs = {}
    for tag, names in batches:
        if tag == 'observation' and not (E / 'submitted_evidence.json').exists():
            #  고친 트리의 submitted_evidence 탐침은 assert 로 JSON 을 쓰지 못한다 — observation_cli 는 그 파일을 읽기만 한다 (값은 안 쓴다) → Codex 원본 사본을 둔다
            shutil.copyfile(PKG / 'evidence/submitted_evidence.json', E / 'submitted_evidence.json')
            (E / 'submitted_evidence.json.FROM_CODEX.txt').write_text(
                'evidence/submitted_evidence.json = Codex 원본 사본 (observation_cli 탐침이 읽기만 한다) — 이 재실행의 submitted_evidence 탐침은 assert 로 쓰지 못했다\n',
                encoding='utf8')
        t = time.monotonic()
        p = subprocess.run([sys.executable, '-I', str(P / 'run_checks.py'), *names], cwd=str(P.parent), capture_output=True, text=True,
                           encoding='utf8', errors='replace')
        (E / f'driver_{tag}.log').write_text(p.stdout + p.stderr, encoding='utf8')
        rcs[tag] = p.returncode
        print(tag, names, 'rc', p.returncode, f'{time.monotonic() - t:.0f}s', flush=True)
    summary = summarize(E, rcs, sha)
    summary['expect'] = expect
    summary['ok'] = rcs == expect
    (E / 'probe_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding='utf8')
    print('기대', expect, '=', summary['ok'])
    return 0 if summary['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main(*sys.argv[1:]))
