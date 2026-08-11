#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""보존된 킷 스캐폴드(flat·gz) → 킷 디렉토리 배치로 되돌린다.

V100 반납 전에 `docs/data/kit_ps_scaffolds/` 로 옮길 때 **평평한 이름**으로 눌러
담았다 (`kit_ps_0_10__am_scaffold.csv.gz`).  그런데 `fit_dh_collapse.py` 와
`plan_se_curve_targets.bed_volumes()` 는 **킷 디렉토리** 배치를 기대한다:

    <kit>/am_scaffold.csv · <kit>/se_scaffold.csv · <kit>/mpm_input.json

즉 데이터는 보존됐지만 **그대로는 d_h 판정을 재현할 수 없었다**.  이 스크립트가
그 한 칸을 잇는다 — 보존본을 풀어 킷 배치로 만들고, 그 위에서 적합을 다시 돌리면
판정이 바이트로 재현된다.

★ 원본을 고치지 않는다.  `fit_dh_collapse.py` 는 selftest 19 개로 고정돼 있으므로
  거기에 아카이브 경로 해석을 끼워 넣는 대신, 배치를 맞춰 주는 쪽을 택했다.

사용:
    python3 scripts/unpack_kit_scaffolds.py --out ~/se_curve_repro
    python3 scripts/fit_dh_collapse.py --dir ~/se_curve_repro --mach 0.03 --n-grid 288
"""
from __future__ import annotations

import argparse
import gzip
import os
import shutil
import sys

#: 보존본 위치 (리포 상대).  `<ARCHIVE>/<kit>__<file>` 규약.
ARCHIVE_DEFAULT = os.path.join('docs', 'data', 'kit_ps_scaffolds')

#: 지표(metrics) json 보존본 — 적합은 이 둘이 **같은 디렉토리**에 있어야 돈다.
METRICS_DEFAULT = os.path.join('docs', 'data', 'se_curve_metrics')

#: 킷 하나가 갖춰야 하는 파일.  mpm_input.json 은 lateral_box(면적) 를 준다.
MEMBERS = ('am_scaffold.csv', 'se_scaffold.csv', 'mpm_input.json',
           # ↓ 2026-08-11 추가.  첫 보존은 am/se+input 만 담았는데, 원본 킷에는
           #   fracture_scaffold(취성→MPM crack-void, opt-in MPM_FRACTURE 입력)와
           #   킷별로 **서로 다른** 러너 3종이 더 있었다 (5킷 해시 전부 다름 =
           #   한 벌만 두면 안 된다).  am/se 보존본은 tar 원본과 10/10 바이트 일치 확인됨.
           'fracture_scaffold.csv', 'run_mpm.sh', 'harvest.sh', 'run_a1_anchors.sh')

#: 없어도 정상인 멤버 — 있으면 풀고, 없어도 '빠짐' 으로 보고하지 않는다.
OPTIONAL = frozenset({'fracture_scaffold.csv', 'run_mpm.sh', 'harvest.sh', 'run_a1_anchors.sh'})

_SEP = '__'


def discover(archive):
    """아카이브 → {kit: {member: path}}.  `.gz` 는 확장자를 벗겨 키로 쓴다."""
    kits = {}
    if not os.path.isdir(archive):
        return kits
    for name in sorted(os.listdir(archive)):
        if _SEP not in name:
            continue
        kit, member = name.split(_SEP, 1)
        if member.endswith('.gz'):
            member = member[:-3]
        if member in MEMBERS:
            kits.setdefault(kit, {})[member] = os.path.join(archive, name)
    return kits


def _copy(src, dst):
    """gz 면 풀어서, 아니면 그대로 복사한다."""
    if src.endswith('.gz'):
        with gzip.open(src, 'rb') as f_in, open(dst, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    else:
        shutil.copyfile(src, dst)


def unpack(archive, out, metrics=None, link_metrics=True):
    """아카이브를 킷 배치로 푼다.  (풀린 킷 수, 빠진 파일 목록) 을 돌려준다."""
    kits, missing = discover(archive), []
    os.makedirs(out, exist_ok=True)
    for kit, members in sorted(kits.items()):
        kit_dir = os.path.join(out, kit)
        os.makedirs(kit_dir, exist_ok=True)
        for member in MEMBERS:
            src = members.get(member)
            if src is None:
                if member not in OPTIONAL:
                    missing.append(f'{kit}/{member}')
                continue
            dst = os.path.join(kit_dir, member)
            _copy(src, dst)
            if member.endswith('.sh'):
                os.chmod(dst, 0o755)          # 러너는 실행권한이 있어야 쓸 수 있다
    if link_metrics and metrics and os.path.isdir(metrics):
        # ★ 접두어로 거르지 않는다.  xfer_* 만 옮기면 d_h 적합의 **g192 기울기 보정**과
        #   jam/loose/wallp/se_e 소비처(summarize_jam_sweep 등)가 조용히 굶는다.
        for name in sorted(os.listdir(metrics)):
            if name.endswith('.json'):
                shutil.copyfile(os.path.join(metrics, name), os.path.join(out, name))
    return len(kits), missing


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument('--archive', default=os.path.join(here, ARCHIVE_DEFAULT))
    ap.add_argument('--metrics', default=os.path.join(here, METRICS_DEFAULT))
    ap.add_argument('--out', default=os.path.expanduser('~/se_curve_repro'))
    ap.add_argument('--no-metrics', action='store_true',
                    help='metrics json 을 복사하지 않는다 (스캐폴드만 필요할 때)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()

    n, missing = unpack(a.archive, a.out, a.metrics, link_metrics=not a.no_metrics)
    if not n:
        sys.exit(f'{a.archive} 에 `<kit>{_SEP}<member>` 파일이 없다 — 경로를 확인하세요.')
    n_json = len([f for f in os.listdir(a.out) if f.endswith('.json')])
    print(f'킷 {n} 개 · metrics json {n_json} 개 → {a.out}')
    # ★ 아카이브가 푼 킷과 **원래 있던 디렉토리**를 구분해 찍는다.  옛 출력은 out 밑의
    #   모든 디렉토리를 같은 표에 넣어, 복구된 볼륨에 남아 있던 킷(예: kit_real14)이
    #   "2/7 — 뭔가 빠졌다" 처럼 보였다.  아카이브에 없는 것은 결손이 아니다.
    from_archive = set(discover(a.archive))
    for kit in sorted(os.listdir(a.out)):
        d = os.path.join(a.out, kit)
        if not os.path.isdir(d):
            continue
        have = [m for m in MEMBERS if os.path.exists(os.path.join(d, m))]
        if kit in from_archive:
            print(f'  {kit:<16} {len(have)}/{len(MEMBERS)}  ' + ' '.join(have))
        else:
            print(f'  {kit:<16} (아카이브 밖 — 원래 있던 디렉토리, 건드리지 않음)  '
                  + ' '.join(have))
    if missing:
        print('\n⚠ 빠진 파일: ' + ', '.join(missing))
    print('\n재현:  python3 scripts/fit_dh_collapse.py --dir '
          f'{a.out} --mach 0.03 --n-grid 288')
    return 1 if missing else 0


def _selftest():
    import json
    import tempfile
    n = [0, 0]

    def ok(name, cond):
        n[1] += 1
        n[0] += bool(cond)
        print(f'  {"PASS" if cond else "FAIL"}  {name}')

    src = tempfile.mkdtemp(prefix='kitarc_')
    dst = tempfile.mkdtemp(prefix='kitout_')
    met = tempfile.mkdtemp(prefix='kitmet_')
    try:
        body = b'x,y,z,r\n0,0,0,0.5\n1,1,1,0.5\n'
        for kit in ('kit_ps_0_10', 'kit_ps_10_0'):
            for member in ('am_scaffold.csv', 'se_scaffold.csv'):
                with gzip.open(os.path.join(src, f'{kit}{_SEP}{member}.gz'), 'wb') as f:
                    f.write(body)
            json.dump({'lateral_box': 100.0},
                      open(os.path.join(src, f'{kit}{_SEP}mpm_input.json'), 'w'))
        json.dump({'phi': 0.72}, open(os.path.join(met, 'xfer_res_kit_ps_0_10_g288_e1.json'), 'w'))
        json.dump({'thickness_um': 27.7}, open(os.path.join(met, 'jam_P300_q95.json'), 'w'))

        REQUIRED = [m for m in MEMBERS if m not in OPTIONAL]
        found = discover(src)
        ok('1) 평평한 이름에서 (킷, 멤버) 를 뽑는다',
           set(found) == {'kit_ps_0_10', 'kit_ps_10_0'}
           and set(found['kit_ps_0_10']) == set(REQUIRED))

        cnt, missing = unpack(src, dst, met)
        ok('2) 킷 두 개를 풀었고 빠진 파일이 없다', cnt == 2 and not missing)
        p = os.path.join(dst, 'kit_ps_0_10', 'am_scaffold.csv')
        ok('3) ★ gz 가 풀려 평문 CSV 로 놓인다', os.path.exists(p) and open(p, 'rb').read() == body)
        ok('4) 킷 디렉토리 배치 = bed_volumes 가 기대하는 모양',
           all(os.path.exists(os.path.join(dst, 'kit_ps_10_0', m)) for m in REQUIRED))
        ok('4b) ★ 선택 멤버가 없어도 missing 으로 보고하지 않는다 (필수만 요구)',
           not missing and set(OPTIONAL) & set(MEMBERS) == set(OPTIONAL))
        ok('5) mpm_input.json 은 gz 가 아니라 그대로 복사된다',
           json.load(open(os.path.join(dst, 'kit_ps_10_0', 'mpm_input.json')))['lateral_box'] == 100.0)
        ok('6) xfer json 이 같은 루트로 따라온다',
           os.path.exists(os.path.join(dst, 'xfer_res_kit_ps_0_10_g288_e1.json')))
        ok('6b) ★ xfer_ 가 아닌 json 도 따라온다 (g192 보정·jam 요약이 굶지 않게)',
           os.path.exists(os.path.join(dst, 'jam_P300_q95.json')))

        # 빠진 멤버 보고
        src2 = tempfile.mkdtemp(prefix='kitarc2_')
        dst2 = tempfile.mkdtemp(prefix='kitout2_')
        try:
            with gzip.open(os.path.join(src2, f'kit_x{_SEP}am_scaffold.csv.gz'), 'wb') as f:
                f.write(body)
            _cnt, miss2 = unpack(src2, dst2, None)
            ok('7) ★ 빠진 멤버를 조용히 넘기지 않고 보고한다',
               sorted(miss2) == ['kit_x/mpm_input.json', 'kit_x/se_scaffold.csv'])
        finally:
            shutil.rmtree(src2, ignore_errors=True)
            shutil.rmtree(dst2, ignore_errors=True)

        ok('8) 아카이브가 없으면 빈 dict (예외 아님)', discover('/nonexistent/xyz') == {})
        ok('9) 관계없는 파일은 무시한다',
           'README' not in discover(src) and len(discover(src)) == 2)

        # ★ 선택 멤버가 **있으면** 풀리고, .sh 는 실행권한이 붙는다
        src3 = tempfile.mkdtemp(prefix='kitarc3_')
        dst3 = tempfile.mkdtemp(prefix='kitout3_')
        try:
            for m in ('am_scaffold.csv', 'se_scaffold.csv'):
                with gzip.open(os.path.join(src3, f'kit_z{_SEP}{m}.gz'), 'wb') as f:
                    f.write(body)
            json.dump({}, open(os.path.join(src3, f'kit_z{_SEP}mpm_input.json'), 'w'))
            with gzip.open(os.path.join(src3, f'kit_z{_SEP}fracture_scaffold.csv.gz'), 'wb') as f:
                f.write(b'id,x\n1,0\n')
            open(os.path.join(src3, f'kit_z{_SEP}run_mpm.sh'), 'w').write('#!/bin/sh\necho hi\n')
            _c3, miss3 = unpack(src3, dst3, None)
            fr = os.path.join(dst3, 'kit_z', 'fracture_scaffold.csv')
            sh = os.path.join(dst3, 'kit_z', 'run_mpm.sh')
            ok('10) ★ fracture_scaffold 가 있으면 풀린다 (취성→MPM 입력)',
               not miss3 and os.path.exists(fr) and open(fr).read().startswith('id,x'))
            ok('11) ★ 러너 .sh 는 실행권한이 붙는다 (안 붙으면 못 돌린다)',
               os.path.exists(sh) and (os.stat(sh).st_mode & 0o111))
        finally:
            shutil.rmtree(src3, ignore_errors=True)
            shutil.rmtree(dst3, ignore_errors=True)
    finally:
        for d in (src, dst, met):
            shutil.rmtree(d, ignore_errors=True)

    print(f'\nunpack_kit_scaffolds selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    raise SystemExit(main())
