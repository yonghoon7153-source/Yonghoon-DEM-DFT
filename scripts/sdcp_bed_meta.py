#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MPM 킷 침대의 세대 · 시딩 기록을 읽기만 한다 — DBE 재압밀 명령을 옛 침대와 같은 세대로 맞추려고 (등록 v2 §3-B R0).

  python3 scripts/sdcp_bed_meta.py ~/sdcp/kit_SBE ~/sdcp/kit_DBE
  python3 scripts/sdcp_bed_meta.py --selftest

킷마다: run_mpm.sh 의 mpm3d_compaction 명령 (그 줄부터 `||` 앞까지) · latest_run 이 가리키는 폴더 · mpm_metrics.json 에서 이름에
세대 · 시딩 낱말이 든 키 (깊이 4 · 값 160 자까지).  아무것도 쓰지 않는다.
"""
import json
import os
import re
import sys
import tempfile
from pathlib import Path

WORDS = re.compile(r'(e_anchor|add_e|dens|mixing|rng|seed|n_grid|frames|platen|mach|protocol|git|code|sha|sdcp|agg|surface|clump|'
                   r'target_gpa|e_se|nu_se|lateral|version|generation|recipe|wt)', re.I)


def walk(o, path=(), depth=0, out=None):
    out = [] if out is None else out
    if depth > 4:
        return out
    if isinstance(o, dict):
        for k, v in o.items():
            p = path + (str(k),)
            if WORDS.search(str(k)) and not isinstance(v, (dict, list)):
                out.append(('.'.join(p), v))
            elif WORDS.search(str(k)) and isinstance(v, list) and len(v) <= 8 and all(not isinstance(x, (dict, list)) for x in v):
                out.append(('.'.join(p), v))
            walk(v, p, depth + 1, out)
    elif isinstance(o, list):
        for i, v in enumerate(o[:50]):
            walk(v, path + (f'[{i}]',), depth + 1, out)
    return out


def kit_report(kit):
    kit = Path(kit)
    lines = [f'== {kit}']
    rs = kit / 'run_mpm.sh'
    if rs.is_file():
        txt = rs.read_text(encoding='utf-8', errors='replace').split('\n')
        i = next((j for j, l in enumerate(txt) if 'mpm3d_compaction.py' in l and l.strip().startswith('python3')), None)
        if i is None:
            lines.append('  run_mpm.sh: mpm3d_compaction 호출 줄 없음')
        else:
            blk = []
            for l in txt[i:i + 12]:
                if l.strip().startswith('||'):
                    break
                blk.append(l.rstrip())
            lines.append('  run_mpm.sh mpm3d:')
            lines += ['    ' + l for l in blk]
    else:
        lines.append('  run_mpm.sh 없음')
    lr = kit / 'latest_run'
    run = None
    if lr.exists():
        run = lr.resolve()
        lines.append(f'  latest_run → {run}')
    else:
        cands = sorted(d for d in kit.glob('run_*') if (d / 'mpm_metrics.json').is_file())
        if cands:
            run = cands[-1]
            lines.append(f'  latest_run 없음 · 마지막 run_* = {run}')
    mj = (run / 'mpm_metrics.json') if run else None
    if mj and mj.is_file():
        try:
            d = json.loads(mj.read_text(encoding='utf-8'))
        except Exception as e:                                   # noqa: BLE001
            lines.append(f'  mpm_metrics.json 읽기 실패: {e}')
            return lines
        lines.append(f'  mpm_metrics.json ({mj.stat().st_size} B · 최상위 키 {len(d) if isinstance(d, dict) else "?"})')
        for k, v in walk(d):
            s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
            lines.append(f'    {k} = {s[:160]}')
    else:
        lines.append('  mpm_metrics.json 없음')
    return lines


def selftest():
    td = Path(tempfile.mkdtemp(prefix='bedmeta_'))
    kit = td / 'kit_X'
    (kit / 'run_1').mkdir(parents=True)
    (kit / 'run_mpm.sh').write_text('echo a\npython3 "$SCR/mpm3d_compaction.py" \\\n  --seed 7 --mixing ballmill \\\n  || { echo fail; }\n', encoding='utf-8')
    (kit / 'run_1' / 'mpm_metrics.json').write_text(json.dumps({'E_anchor': 'ADD_E_SET_X', 'additives': {'SDCP': {'agg_d_um': 1.0, 'n': 5}},
                                                                 'porosity': 0.1}), encoding='utf-8')
    os.symlink(kit / 'run_1', kit / 'latest_run')
    rep = '\n'.join(kit_report(kit))
    ok = ('--seed 7 --mixing ballmill' in rep and 'E_anchor = ADD_E_SET_X' in rep and 'additives.SDCP.agg_d_um = 1.0' in rep
          and 'porosity' not in rep and 'fail' not in rep)
    print(rep)
    print(f'\nsdcp_bed_meta selftest: {"1/1" if ok else "0/1"} PASS')
    return 0 if ok else 1


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('kits', nargs='*', help='킷 폴더 (run_mpm.sh 가 있는 곳)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.kits:
        ap.error('킷 폴더를 하나 이상')
    for k in a.kits:
        print('\n'.join(kit_report(k)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
