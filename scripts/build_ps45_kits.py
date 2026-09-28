#!/usr/bin/env python3
"""build_ps45_kits.py — 웹앱 케이스 → ps45 MPM 킷 5 개 (사전등록 `ps45_dh_transfer_prereg_20260926.md` §5-B 의 손 절차를 한 번에).

왜 (2026-09-28) — §5-B 는 케이스마다 `mpm_input_from_case.py` 를 손으로 부르고 lateral 을 눈으로 보라고 적었다.  다섯 침대의 웹앱
이름은 `input_6mAh_real_<N>_D9` (D9 = AM_P 지름 9 µm = r 4.5) 라 이름으로는 P:S 를 알 수 없고 (번호 N 은 사용자가 붙인 것),
업로드 덱 이름은 `input_ps_<P>_<S>_r45` 일 수도 아닐 수도 있다.  ⇒ **P:S 는 이름이 아니라 입자 수로** 정한다.

무엇
  고르기   uploads/<cid>/meta.json 의 업로드 파일에 `ps_<P>_<S>_r45` 덱이 있거나 이름이 `_D9` 로 끝나는 케이스
  만들기   results/<cid>/ (atoms.csv …) → `mpm_input_from_case.py --type-map 1:AM_P,2:AM_S,3:SE` (다섯 덱 모두 표준 번호 · §5-B ②)
  판정     am_scaffold 의 AM_P · AM_S 개수 ↔ README §2 예측 (가장 가까운 P:S · 각 ±max(3, 2 %)) · lateral |x − 0.05| ≤ 5e-5 (§5-B ③) ·
           덱 이름이 있으면 그 P:S 와 개수의 P:S 가 같아야 한다
  중복     같은 P:S 가 둘 이상이면 스캐폴드 **좌표** (머리 주석의 케이스 id 제외) 가 같을 때만 받는다 — 다르면 그 P:S 는 비우고 사람이 고른다
  산출     <out>/kit_ps_<P>_<S>_r45/ · <out>/ps45_kits.tgz (준비된 것만) — v100 `~/Yonghoon-DEM-DFT/se_curve/` 로 보낸다

⚠ 사전등록 §2 의 전제 하나는 이 도구가 못 본다: 업로드한 최종 atom 덤프가 **완주 궤적**의 것인지 (r2 · r3 재시작이 덤프를 덮었다).
  출력의 `덤프 atom_<step>` 을 각 `post_ps_*_r45` 로그의 마지막 step 과 대조한다.

    ~/Yonghoon-DEM-DFT/.venv/bin/python3 scripts/build_ps45_kits.py            # 웹앱 PC (WEBAPP_* 폴더 = ~/Yonghoon-DEM-DFT/webapp/*)
    python3 scripts/build_ps45_kits.py --selftest
"""
import argparse
import csv
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

PRED = {'10_0': (402, 0), '7_3': (282, 1375), '5_5': (201, 2292), '3_7': (121, 3209), '0_10': (0, 4584)}   # README §2 (AM_P, AM_S)
LATERAL, LAT_TOL = 0.05, 5e-5
TYPE_MAP = '1:AM_P,2:AM_S,3:SE'


def _sha(p):
    """좌표만 — 머리 주석 (`# … — case <id>`) 은 케이스마다 달라 같은 침대의 재업로드를 다르다고 오판한다."""
    return hashlib.sha256(b''.join(l for l in open(p, 'rb') if not l.startswith(b'#'))).hexdigest()


def build(root, out, builder=None, py=sys.executable, log=print):
    """→ (준비된 킷 이름 목록, 케이스별 행 목록).  행 = dict(cid, name, ps, n, lateral, deck, dump, ok, why)."""
    up, rs = os.path.join(root, 'webapp', 'uploads'), os.path.join(root, 'webapp', 'results')
    H = os.path.expanduser('~')
    bld = builder or next((p for p in (os.path.join(H, 'dem-web', 'scripts', 'mpm_input_from_case.py'),
                                       os.path.join(root, 'scripts', 'mpm_input_from_case.py')) if os.path.isfile(p)), None)
    log(f'uploads {up}\nresults {rs}\nbuilder {bld}\npython  {py}')
    if not bld:
        raise SystemExit('⛔ mpm_input_from_case.py 없음')
    os.makedirs(out, exist_ok=True)
    got, rows = {}, []
    for mp in sorted(glob.glob(os.path.join(up, '*', 'meta.json'))):
        cid = os.path.basename(os.path.dirname(mp))
        try:
            m = json.load(open(mp, encoding='utf-8'))
        except (OSError, ValueError):
            continue
        files = [str(f) for f in (m.get('files') or [])]
        deck = next((f for f in files if re.search(r'ps_\d+_\d+_r45', f)), '')
        name = str(m.get('name', ''))
        if not (deck or name.endswith('_D9')):
            continue
        dump = next((f for f in files if re.match(r'atom_\d+', f)), '')
        r = os.path.join(rs, cid)
        row = dict(cid=cid, name=name, deck=deck, dump=dump, ps=None, n=None, lateral=None, ok=False, why='')
        rows.append(row)
        if not os.path.isfile(os.path.join(r, 'atoms.csv')):
            row['why'] = 'results/atoms.csv 없음 (분석 안 끝남)'
            log(f'  SKIP {name} ({cid}) — {row["why"]}')
            continue
        tmp = os.path.join(out, f'_tmp_{cid}')
        shutil.rmtree(tmp, ignore_errors=True)
        with open(os.path.join(out, f'{cid}.log'), 'w') as lf:
            rc = subprocess.run([py, bld, '--results', r, '--case', cid, '--out', tmp, '--type-map', TYPE_MAP],
                                stdout=lf, stderr=subprocess.STDOUT).returncode
        if rc or not os.path.isfile(os.path.join(tmp, 'am_scaffold.csv')):
            row['why'] = f'킷 생성 rc={rc} · {out}/{cid}.log'
            log(f'  FAIL {name} ({cid}) — {row["why"]}')
            continue
        ty = [c[0].split('.')[0] for c in csv.reader(open(os.path.join(tmp, 'am_scaffold.csv'))) if c and c[0][:1].isdigit()]
        n = (ty.count('1'), ty.count('2'))
        ps = min(PRED, key=lambda k: abs(PRED[k][0] - n[0]) + abs(PRED[k][1] - n[1]))
        ok_n = all(abs(a - b) <= max(3, 0.02 * b) for a, b in zip(n, PRED[ps]))
        lat = json.load(open(os.path.join(tmp, 'mpm_input.json'))).get('lateral_box')
        ok_l = isinstance(lat, (int, float)) and abs(lat - LATERAL) <= LAT_TOL
        ok_d = (not deck) or (f'ps_{ps}_r45' in deck)
        h = _sha(os.path.join(tmp, 'am_scaffold.csv'))[:12] + '/' + _sha(os.path.join(tmp, 'se_scaffold.csv'))[:12]
        row.update(ps=ps, n=n, lateral=lat, ok=ok_n and ok_l and ok_d,
                   why='; '.join(w for w, c in (('개수', ok_n), ('lateral', ok_l), ('덱 이름 ≠ 개수', ok_d)) if not c))
        log(f'  {"OK  " if row["ok"] else "FAIL"} ps_{ps}_r45 ← {name} ({cid}) · AM_P/AM_S {n[0]}/{n[1]} (예측 {PRED[ps][0]}/{PRED[ps][1]}) · '
            f'lateral {lat} · 덱 {deck or "—"} · 덤프 {dump or "—"} · sha {h}' + (f' · ✗ {row["why"]}' if row['why'] else ''))
        if row['ok']:
            got.setdefault(ps, []).append((cid, tmp, h))
    log('──')
    ready = []
    for ps in PRED:
        c = got.get(ps, [])
        if not c:
            log(f'  ✗ ps_{ps}_r45 — 케이스 없음')
            continue
        if len({x[2] for x in c}) > 1:
            log(f'  ✗ ps_{ps}_r45 — 서로 다른 스캐폴드 {len(c)} 개 ({", ".join(x[0] for x in c)}) — 사람이 고른다')
            continue
        k = os.path.join(out, f'kit_ps_{ps}_r45')
        shutil.rmtree(k, ignore_errors=True)
        shutil.copytree(c[0][1], k)
        ready.append(f'kit_ps_{ps}_r45')
        log(f'  ✓ kit_ps_{ps}_r45 ← {c[0][0]}' + (f' (같은 스캐폴드 {len(c)} 개)' if len(c) > 1 else ''))
    for t in glob.glob(os.path.join(out, '_tmp_*')):
        shutil.rmtree(t, ignore_errors=True)
    log(f'준비 {len(ready)}/5 — {" ".join(ready)}')
    if ready:
        subprocess.run(['tar', 'czf', os.path.join(out, 'ps45_kits.tgz'), '-C', out] + ready, check=True)
        log(f'→ {os.path.join(out, "ps45_kits.tgz")}')
    return ready, rows


def _selftest():
    import random
    import tempfile
    here = os.path.dirname(os.path.abspath(__file__))
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    def mock(root, beds):
        for cid, (nm, deck, np_, ns, seed, box) in beds.items():
            u, r = (os.path.join(root, 'webapp', d, cid) for d in ('uploads', 'results'))
            os.makedirs(u)
            json.dump(dict(name=nm, files=[deck, 'atom_3640000.liggghts']), open(os.path.join(u, 'meta.json'), 'w'))
            if np_ is None:
                continue                                  # 분석 안 끝난 케이스 (results 없음)
            os.makedirs(r)
            g = random.Random(seed)
            rows, k = ['id,type,x,y,z,radius'], 0
            for t, n, rad in ((1, np_, 0.0045), (2, ns, 0.002), (3, 200, 0.0005)):
                for _ in range(n):
                    k += 1
                    rows.append(f'{k},{t},{g.uniform(0, 0.05):.6f},{g.uniform(0, 0.05):.6f},{g.uniform(0, 0.11):.6f},{rad}')
            open(os.path.join(r, 'atoms.csv'), 'w').write('\n'.join(rows) + '\n')
            json.dump(dict(box_x=box), open(os.path.join(r, 'input_params.json'), 'w'))

    bld = os.path.join(here, 'mpm_input_from_case.py')
    base = {'c010': ('input_6mAh_real_1_D9', 'input_ps_0_10_r45.liggghts', 0, 4588, 1, 0.05),
            'c37': ('input_6mAh_real_2_D9', 'input_ps_3_7_r45.liggghts', 121, 3209, 2, 0.05),
            'c55': ('input_6mAh_real_3_D9', 'in.real_3.liggghts', 201, 2292, 3, 0.05),          # 덱 이름에 P:S 없음 → 개수로
            'c73': ('input_6mAh_real_4_D9', 'input_ps_7_3_r45.liggghts', 282, 1375, 4, 0.05),
            'c73b': ('input_6mAh_real_4_D9', 'input_ps_7_3_r45.liggghts', 282, 1375, 4, 0.05),   # 같은 침대 재업로드 (같은 좌표)
            'c100': ('input_6mAh_real_5_D9', 'input_ps_10_0_r45.liggghts', 402, 0, 5, 0.05),
            'cX': ('other_case', 'input_foo.liggghts', 50, 50, 6, 0.05),                          # 무관
            'cN': ('input_6mAh_real_9_D9', 'input_ps_5_5_r45.liggghts', None, None, 0, 0.05)}     # 분석 안 끝남
    with tempfile.TemporaryDirectory() as td:
        mock(td, base)
        ready, rows = build(td, os.path.join(td, 'out'), builder=bld, log=lambda *_: None)
        by = {r['cid']: r for r in rows}
        chk('① 다섯 침대 → 킷 5/5 (P:S 를 개수로) · 무관 케이스는 고르지 않는다',
            sorted(ready) == sorted(f'kit_ps_{k}_r45' for k in PRED) and 'cX' not in by)
        chk('② 덱 이름에 P:S 가 없어도 개수로 5:5', by['c55']['ps'] == '5_5' and by['c55']['ok'])
        chk('③ 같은 침대 재업로드 (좌표 같음 · 머리 주석만 다름) → 받는다', 'kit_ps_7_3_r45' in ready)
        chk('④ 분석 안 끝난 케이스 → SKIP (다른 킷은 영향 없음)', by['cN']['why'].startswith('results/atoms.csv 없음'))
        chk('⑤ tar 에 준비된 킷만', os.path.isfile(os.path.join(td, 'out', 'ps45_kits.tgz')))
    bad = dict(base)
    bad['c73b'] = ('input_6mAh_real_4_D9', 'input_ps_7_3_r45.liggghts', 282, 1375, 44, 0.05)          # 같은 P:S · 다른 좌표
    bad['c37'] = ('input_6mAh_real_2_D9', 'input_ps_3_7_r45.liggghts', 121, 3000, 2, 0.05)            # 개수 어긋남 (−6.5 %)
    bad['c010'] = ('input_6mAh_real_1_D9', 'input_ps_0_10_r45.liggghts', 0, 4588, 1, 0.06)            # lateral 0.06
    bad['c55'] = ('input_6mAh_real_3_D9', 'input_ps_3_7_r45.liggghts', 201, 2292, 3, 0.05)            # 덱 이름 3_7 · 개수 5_5
    with tempfile.TemporaryDirectory() as td:
        mock(td, bad)
        ready, rows = build(td, os.path.join(td, 'out'), builder=bld, log=lambda *_: None)
        by = {r['cid']: r for r in rows}
        chk('⑥ 같은 P:S 인데 좌표가 다른 두 케이스 → 그 P:S 는 비운다 (사람이 고른다)', 'kit_ps_7_3_r45' not in ready)
        chk('⑦ 개수가 예측과 ±2 % 넘게 어긋남 → 킷 안 만듦', not by['c37']['ok'] and 'kit_ps_3_7_r45' not in ready)
        chk('⑧ lateral 0.06 (≠ 0.05 ± 5e-5) → 킷 안 만듦', not by['c010']['ok'] and 'lateral' in by['c010']['why'])
        chk('⑨ 덱 이름 (3_7) 과 개수 (5_5) 가 다르면 → 킷 안 만듦', not by['c55']['ok'] and '덱' in by['c55']['why'])
        chk('⑩ 멀쩡한 것 (10_0) 은 그대로 준비', ready == ['kit_ps_10_0_r45'])
    print(f'\nbuild_ps45_kits selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description='웹앱 케이스 → ps45 MPM 킷 5 개 (ps45 사전등록 §5-B)')
    ap.add_argument('--root', default=os.path.expanduser('~/Yonghoon-DEM-DFT'), help='데이터 루트 (webapp/uploads · webapp/results 가 그 밑)')
    ap.add_argument('--out', default=os.path.expanduser('~/ps45_kits'), help='킷을 쓸 곳')
    ap.add_argument('--builder', default=None, help='mpm_input_from_case.py 경로 (기본: ~/dem-web → <root>/scripts)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    ready, _ = build(a.root, a.out, builder=a.builder)
    raise SystemExit(0 if len(ready) == 5 else 1)


if __name__ == '__main__':
    main()
