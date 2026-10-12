#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""반입한 재검증 7 폴더 + 리포 git 으로 Codex 묶음을 다시 세운다 (slim 에서 뺀 것 = git 에서 복원).

    python3 -I -B <이 파일> <리포 루트> <새 빈 폴더>

넣는 것: 반입 폴더 그대로 + source/ 573 (핀 3cedd40a5 · source_manifest 의 blob SHA-1 · SHA-256 · 크기 대조) +
parent/scripts/ 2 (부모 821f0e151) + baseline_r6/{evidence 일곱 · source_manifest.json} (10-11 재검증 6 반입본) +
submitted/request.md (핀의 요청서).  그다음 그 폴더에서 Codex 실행기를 무변경으로:
    python3 -I <폴더>/run_checks.py reread r7_cli ; … r7_parent_cli ; … r7_predicates test_quality_probe ; … r7_final_qa
(r7_contract = 윈도 경로 전용 → 우리 판 r7_contract_ours.py)
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

PIN = '3cedd40a5911d0606bf33ed2085d5cb93c4db2e0'
PARENT = '821f0e15180bdd3472f9ce203a7a7815a1f27eb9'
HERE = Path(__file__).resolve().parents[1]                     # 반입 폴더
R6 = 'docs/reviews/codex_gen2_network_reverify6_evidence_20261011'


def blob(repo, rev, path):
    return subprocess.run(['git', '-C', str(repo), 'show', f'{rev}:{path}'], capture_output=True, check=True).stdout


def main(repo: Path, dst: Path) -> int:
    if dst.exists() and any(dst.iterdir()):
        sys.exit(f'{dst} 가 비어 있지 않다')
    shutil.copytree(HERE, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns('_repro_ours_*'))
    man = json.loads((HERE / 'source_manifest.json').read_text(encoding='utf-8-sig'))
    assert man['pin'] == PIN
    for e in man['files']:
        data = blob(repo, PIN, e['path'])
        h1 = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert h1 == e['sha'] and hashlib.sha256(data).hexdigest() == e['sha256'] and len(data) == e['bytes'], e['path']
        p = dst / 'source' / e['path']
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    for rel in ('scripts/g2_network_reread.py', 'scripts/wsl_network_smoke.py'):
        p = dst / 'parent' / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(blob(repo, PARENT, rel))
    (dst / 'baseline_r6/evidence').mkdir(parents=True, exist_ok=True)
    for f in sorted((repo / R6 / 'evidence').glob('r6_s0b_*.input.json')):
        shutil.copy2(f, dst / 'baseline_r6/evidence' / f.name)
    shutil.copy2(repo / R6 / 'source_manifest.json', dst / 'baseline_r6/source_manifest.json')
    (dst / 'submitted').mkdir(exist_ok=True)
    (dst / 'submitted/request.md').write_bytes(blob(repo, PIN, 'docs/reviews/codex_gen2_network_reverify7_request_20261011.md'))
    print(json.dumps({'bundle': str(dst), 'source_files': len(man['files'])}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()))
