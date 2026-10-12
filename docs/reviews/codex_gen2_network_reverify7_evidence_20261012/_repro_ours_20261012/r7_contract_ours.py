#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Codex 재검증 7 (10-12) — r7_contract 의 우리 트리 판 (Codex 탐침은 윈도 경로 전용이라 그대로 못 돈다).

    python3 -I -B <이 파일> <리포 루트> <Codex 묶음 baseline_r6/evidence> <Codex r7_contract.json> <출력 json>

같은 질문을 우리 리포 (git) 에서 다시 묻는다 (Codex 탐침을 import 하지 않는다 · 솔버 · DEM 실행 없음):
  ① 봉인 32 code_fp = e8b2496b… · R6 핀 (a20fc1875) 대비 바뀐 봉인 파일 0
  ② 인계 도구 지문 (g2_network_reread · lhs_design_dataset) 핀 ↔ R6
  ③ case15 원자료 네 파일 전체 sha256 · 풀린 바이트 = 등록 (CASE15_NEGCTL) = README
  ④ 접촉 덤프를 Decimal 로 직접 읽어 음수 면적 행 = 등록 두 행
  ⑤ 수정 범위 (부모 821f0e151 ↔ 핀 3cedd40a5): 줄 수 · 바뀐 / 새 함수 · chk(...) AST 동일
  ⑥ 반입된 R6 입력 일곱 = Codex baseline 바이트 · 요청서 = 핀 바이트
"""
from __future__ import annotations

import ast
import decimal
import difflib
import gzip
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PIN = '3cedd40a5911d0606bf33ed2085d5cb93c4db2e0'
PARENT = '821f0e15180bdd3472f9ce203a7a7815a1f27eb9'
R6PIN = 'a20fc1875'
FP_EXPECTED = 'e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71'


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def show(repo: Path, rev: str, path: str) -> bytes:
    return subprocess.run(['git', '-C', str(repo), 'show', f'{rev}:{path}'], capture_output=True, check=True).stdout


def assignment(text: str, name: str):
    tree = ast.parse(text)
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    # 리터럴 등록 할당만 (튜플 · dict(...)) — 모듈 import 없음 (Codex 탐침과 같은 제한 eval)
    return eval(compile(ast.Expression(node.value), name, 'eval'), {'__builtins__': {}, 'dict': dict})


def funcs(text: str) -> dict:
    return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(text).body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def chks(text: str) -> list:
    return [ast.dump(n, include_attributes=False) for n in ast.walk(ast.parse(text))
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'chk']


def main(repo: Path, baseline_ev: Path, codex_json: Path, out: Path) -> int:
    res: dict = {'pin': PIN}
    runner = show(repo, PIN, 'scripts/run_network_194_parallel.py').decode()
    sealed = assignment(runner, 'CODE_FILES')
    handover = assignment(runner, 'HANDOVER_FILES')
    h_pin = {p: sha(show(repo, PIN, p)) for p in sealed}
    h_r6 = {p: sha(show(repo, R6PIN, p)) for p in sealed}
    fp = sha(json.dumps(sorted(h_pin.items()), separators=(',', ':')).encode())
    res['sealed32'] = {'files': len(sealed), 'code_fp': fp, 'expected_code_fp_match': fp == FP_EXPECTED,
                       'changed_from_r6': [p for p in sealed if h_pin[p] != h_r6[p]], 'hashes': h_pin}
    res['handover'] = {p: {'current': sha(show(repo, PIN, p)), 'r6': sha(show(repo, R6PIN, p))} for p in handover}

    reread_pin = show(repo, PIN, 'scripts/g2_network_reread.py').decode()
    reg = assignment(reread_pin, 'CASE15_NEGCTL')
    case_dir = repo / 'docs/data/case15_corner_20261001'
    readme = {}
    for line in (case_dir / 'README.md').read_text(encoding='utf-8').splitlines():
        m = re.match(r'^([0-9a-f]{64})\s+([\d,]+) B\s+(\S+)', line)
        if m:
            readme[m[3]] = {'sha256': m[1], 'bytes': int(m[2].replace(',', ''))}
    raw = {}
    for fn, expected in reg['raw_sha256'].items():
        p = case_dir / fn
        packed = not p.is_file()
        if packed:
            p = p.with_suffix(p.suffix + '.gz')
        h, n = hashlib.sha256(), 0
        with (gzip.open(p, 'rb') if packed else p.open('rb')) as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b''):
                n += len(chunk)
                h.update(chunk)
        raw[fn] = {'path': str(p.relative_to(repo)), 'uncompressed_bytes': n, 'actual_sha256': h.hexdigest(),
                   'registry_sha256': expected, 'readme': readme.get(fn),
                   'match': h.hexdigest() == expected == readme[fn]['sha256'] and n == readme[fn]['bytes']}
    res['raw_case15'] = raw

    D = decimal.Decimal
    rows, neg = 0, []
    with gzip.open(case_dir / 'contact_v4_1710000.liggghts.gz', 'rt', encoding='utf-8') as fh:
        for line in fh:
            if line.startswith('ITEM: ENTRIES'):
                cols = line[len('ITEM: ENTRIES'):].split()
                break
        idx = [cols.index(k) for k in ('c_cpl[7]', 'c_cpl[8]', 'c_cpl[22]', 'c_cpl[23]')]
        for line in fh:
            if not line.strip() or line.startswith('ITEM'):
                continue
            rows += 1
            f = line.split()
            a, b, area, delta = (f[i] for i in idx)
            if D(area) < 0:
                neg.append([int(D(a)), int(D(b)), float((D(area) * 1000000).quantize(D('0.000001'))),
                            float((D(delta) * 1000).quantize(D('0.000001')))])
    res['negative_rows'] = {'source_contact_rows': rows, 'independent_decimal_rows': neg,
                            'registry_rows': [list(r) for r in reg['negative_rows_ref']],
                            'matches_registration': sorted(neg) == sorted(map(list, reg['negative_rows_ref']))}

    patches = {}
    for rel in ('scripts/g2_network_reread.py', 'scripts/wsl_network_smoke.py'):
        a, b = show(repo, PARENT, rel).decode(), show(repo, PIN, rel).decode()
        fa, fb = funcs(a), funcs(b)
        diff = list(difflib.unified_diff(a.splitlines(), b.splitlines()))
        patches[rel] = {'added_lines': sum(l.startswith('+') and not l.startswith('+++') for l in diff),
                        'deleted_lines': sum(l.startswith('-') and not l.startswith('---') for l in diff),
                        'changed_functions': sorted(k for k in fa.keys() & fb.keys() if fa[k] != fb[k]),
                        'added_functions': sorted(fb.keys() - fa.keys()),
                        'removed_functions': sorted(fa.keys() - fb.keys()),
                        'chk_count_parent': len(chks(a)), 'chk_count_pin': len(chks(b)),
                        'all_chk_asts_identical': chks(a) == chks(b)}
    res['patches'] = patches

    imp = []
    idir = 'docs/reviews/codex_gen2_network_reverify6_evidence_20261011/evidence'
    names = subprocess.run(['git', '-C', str(repo), 'ls-tree', '--name-only', f'{PIN}:{idir}'],
                           capture_output=True, text=True, check=True).stdout.split()
    for nm in sorted(n for n in names if re.fullmatch(r'r6_s0b_.*\.input\.json', n)):
        data = show(repo, PIN, f'{idir}/{nm}')
        old = baseline_ev / nm
        imp.append({'name': nm, 'sha256': sha(data), 'equals_codex_baseline_bytes': old.is_file() and old.read_bytes() == data})
    res['imported_regressions'] = imp
    res['request_equals_pin_bytes'] = sha(show(repo, PIN, 'docs/reviews/codex_gen2_network_reverify7_request_20261011.md'))

    # Codex 증거와 같은 칸 대조
    cx = json.loads(codex_json.read_text(encoding='utf-8-sig'))
    same = {
        'sealed32': res['sealed32']['code_fp'] == cx['sealed32']['code_fp'] and res['sealed32']['changed_from_r6'] == cx['sealed32']['changed_from_r6']
                    and res['sealed32']['hashes'] == cx['sealed32']['hashes'],
        'handover': res['handover'] == cx['handover'],
        'raw_case15': all(raw[k]['actual_sha256'] == cx['raw_case15'][k]['actual_sha256']
                          and raw[k]['uncompressed_bytes'] == cx['raw_case15'][k]['uncompressed_bytes'] for k in raw),
        'negative_rows': res['negative_rows']['independent_decimal_rows'] == cx['negative_rows']['independent_decimal_rows']
                         and rows == cx['negative_rows']['source_contact_rows'],
        'patches': all(all(patches[r][k] == cx['scope']['patches'][r][k] for k in patches[r]) for r in patches),
        'imported_regressions': [(x['name'], x['sha256']) for x in imp] == [(x['name'], x['sha256']) for x in cx['imported_regressions']],
    }
    res['codex_same'] = same
    res['all_ok'] = (res['sealed32']['expected_code_fp_match'] and not res['sealed32']['changed_from_r6']
                     and all(x['match'] for x in raw.values()) and res['negative_rows']['matches_registration']
                     and all(x['equals_codex_baseline_bytes'] for x in imp) and all(same.values()))
    out.write_text(json.dumps(res, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'all_ok': res['all_ok'], 'codex_same': same, 'code_fp': fp[:12],
                      'reread_pin': res['handover'].get('scripts/g2_network_reread.py', {}).get('current', '')[:12],
                      'negative': neg, 'patches': {k: (v['added_lines'], v['deleted_lines']) for k, v in patches.items()}},
                     ensure_ascii=False))
    return 0 if res['all_ok'] else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])))
