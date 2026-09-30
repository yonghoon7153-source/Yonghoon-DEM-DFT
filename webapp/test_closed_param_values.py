#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""닫힌 파라미터 값 · 경로 회귀 — 웹앱 ② (LHS-24 (a)(b)(c)(d)(h) · DESC-01 · 1저자 비준 09-30 밤 · J20-l).

  python3 webapp/test_closed_param_values.py      # 종료코드 0 = PASS

합성 침대를 **웹앱과 같은 CLI** (`analyze_contacts_bimodal.py` · `analyze_contacts.py` — app.py 의 두 cmd) 로 돌려
full_metrics.json · contact_summary.csv · network_summary.csv 를 본다.  기대값은 설계한 입자 · 접촉에서 **손으로** 센다.

  [A] (a) full_metrics.json 에 숫자처럼 생긴 문자열 · 문자열 bool 이 없다 (numpy 값이 json `default=str` 로 문자열이 되던 것) ·
      am_am_n_contacts = int · 옛 케이스의 문자열 ('412') 도 그룹 선택기 · 그룹 그림이 숫자로 읽는다
  [B] (b) 두 상이 침대에 다 있는데 접촉이 0 인 쌍 = **측정된 0** (접촉 요약 행 · area_<쌍>_n · _total) · 평균 면적은 정의되지
      않는다 (키 없음 · CSV '—') · 상이 침대에 없으면 그 쌍은 없다 (N/A — 인계표 J20-h 와 같은 규칙)
  [C] (c) τ 가 없는 침대 (SE–SE 접촉 0 → 관통 없음) 도 phi_se · phi_am (구 부피 합 ÷ 판 간격 상자) 을 낸다 · σ_Bruggeman 은
      없다 (DESC-01 — τ 실패가 기하량까지 삼키던 것)
  [D] (d) 분석기가 porosity_union · overlap_fraction_pct · porosity_spheresum 을 **직접** 저장한다 (ε_sphere 와 같은 판 · 상자) —
      2e (recompute_porosity_dual) 가 없는 경로 (batch_rerun_physics · archive_reanalyze · stop_after contact/coverage) 에서도
      남는다 · 2e 를 돌려도 값이 같다 (2e 는 원 공극률에 고정해 ε_u = ε_s + 겹침·(1 − ε_s) 로 쓴다)
  [H] (h) 비정사각 상자 (0.012 × 0.010) → V_box = x · y · plate_z (ε_sphere · ε_union) · recompute_porosity_dual.compute_dual 도

⚠ (a)(b)(c)(d)(h) 는 파이프라인 (analyze_contacts · dem_analysis_core) 을 바꾼다 — WSL 5번 봉인 (1e09f661d) 이후 세대.
"""
import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')

_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f' — {extra}' if extra else ''))
    return bool(cond)


def same(a, b, tol=1e-9):
    try:
        return abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b)))
    except (TypeError, ValueError):
        return False


# ── 합성 침대 (sim 단위 · scale 1000 → µm) ─────────────────────────────────────────
R_SE, SP, PLATE_Z = 0.002, 0.0038, 0.03          # SE 반지름 2 µm · 사슬 간격 3.8 µm (이웃 δ = 0.2 µm) · 판 30 µm
AM = {1: ('AM_P', 0.003, (0.003, 0.003, 0.010)), 2: ('AM_P', 0.003, (0.0088, 0.003, 0.010)),
      3: ('AM_S', 0.0015, (0.0088, 0.003, 0.0144)), 4: ('AM_S', 0.0015, (0.003, 0.003, 0.020))}
AM_AM = [(1, 2, 0.0002), (2, 3, 0.0001)]           # AM_P–AM_P 1 · AM_P–AM_S 1 · AM_S–AM_S **0** (3 · 4 는 안 닿는다)
N_SAT = {1: 2, 2: 1, 3: 2, 4: 1}                    # AM 마다 닿는 SE 위성 수 → AM_P–SE 3 · AM_S–SE 3
NUM_RE = re.compile(r'\s*[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?\s*')


def sphere_v(r):
    return 4.0 / 3.0 * math.pi * r ** 3


def lens_v(r1, r2, delta):
    d = r1 + r2 - delta
    return math.pi * delta ** 2 / (12 * d) * (d ** 2 + 2 * d * (r1 + r2) - 3 * (r1 - r2) ** 2)


def make_bed(d, kind='bimodal', se_se=True, box=None, am_ids=(1, 2, 3, 4)):
    """d 에 atoms.csv · contacts.csv · out/mesh_info.json (+ input_params.json) 를 쓴다.  기대값 dict 를 돌려준다."""
    out = os.path.join(d, 'out')
    os.makedirs(out)
    if kind == 'bimodal':
        tid, tmap = {'AM_P': 1, 'AM_S': 2, 'SE': 3}, '1:AM_P,2:AM_S,3:SE'
    else:                                          # mono — 웹앱은 AM 한 종류를 반지름 이름 (r 1.5 µm → AM_S) 으로 부른다
        tid, tmap = {'AM_S': 1, 'SE': 2}, '1:AM_S,2:SE'
    atoms, cons = [], []
    sid = 101
    for cx in (0.002, 0.006, 0.010):               # SE 사슬 3 × 8 알 (z 2 → 28.6 µm) — 바닥 · 판 띠에 닿아 관통
        prev = None
        for k in range(8):
            atoms.append((sid, tid['SE'], cx, 0.009, R_SE + SP * k, R_SE))
            if prev is not None and se_se:
                cons.append((prev, sid, 2 * R_SE - SP))
            prev, sid = sid, sid + 1
    sat = 201
    for a in am_ids:
        ph, r, (x, y, z) = AM[a]
        atoms.append((a, tid[ph], x, y, z, r))
        for j in range(N_SAT[a]):
            atoms.append((sat, tid['SE'], x, y - (r + R_SE - 1e-5), z + 0.0041 * j, R_SE))
            cons.append((a, sat, 1e-5))
            sat += 1
    cons += [(i, j, dl) for i, j, dl in AM_AM if i in am_ids and j in am_ids]
    with open(os.path.join(d, 'atoms.csv'), 'w') as fh:
        fh.write('id,type,x,y,z,radius\n')
        fh.writelines(f'{a},{t},{x!r},{y!r},{z!r},{r!r}\n' for a, t, x, y, z, r in atoms)
    with open(os.path.join(d, 'contacts.csv'), 'w') as fh:
        fh.write('id1,id2,fn_x,fn_y,fn_z,ft_x,ft_y,ft_z,contact_area,delta\n')
        fh.writelines(f'{i},{j},0,0,0.001,0,0,0,1e-08,{dl!r}\n' for i, j, dl in cons)
    with open(os.path.join(out, 'mesh_info.json'), 'w') as fh:
        json.dump({'plate_z': PLATE_Z}, fh)
    bx, by = box or (0.012, 0.012)
    with open(os.path.join(out, 'input_params.json'), 'w') as fh:
        json.dump({'box_x': bx, 'box_y': by}, fh)
    rad = {a: r for a, _t, _x, _y, _z, r in atoms}
    v_s = sum(sphere_v(r) for r in rad.values())
    v_se = sum(sphere_v(r) for a, t, _x, _y, _z, r in atoms if t == tid['SE'])
    v_lens = sum(lens_v(rad[i], rad[j], dl) for i, j, dl in cons)
    v_box = bx * by * PLATE_Z
    return dict(dir=d, out=out, tmap=tmap, script=('analyze_contacts_bimodal.py' if kind == 'bimodal' else 'analyze_contacts.py'),
                eps_s=(1 - v_s / v_box) * 100, eps_u=(1 - (v_s - v_lens) / v_box) * 100, ov=v_lens / v_s * 100,
                phi_se=v_se / v_box, phi_am=(v_s - v_se) / v_box)


def run_bed(bed):
    pr = subprocess.run([sys.executable, os.path.join(SCRIPTS, bed['script']), os.path.join(bed['dir'], 'atoms.csv'),
                         os.path.join(bed['dir'], 'contacts.csv'), '-o', bed['out'], '-t', bed['tmap'], '-s', '1000'],
                        capture_output=True, text=True, timeout=600)
    met = {}
    p = os.path.join(bed['out'], 'full_metrics.json')
    if os.path.exists(p):
        with open(p) as fh:
            met = json.load(fh)
    return pr, met


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as fh:
        return list(csv.reader(fh))


def stringy(obj, path=''):
    """숫자처럼 생긴 문자열 · 문자열 bool (numpy 값이 default=str 로 새던 흔적) 의 위치."""
    bad = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            bad += stringy(v, f'{path}.{k}' if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            bad += stringy(v, f'{path}[{i}]')
    elif isinstance(obj, str) and (NUM_RE.fullmatch(obj) or obj in ('True', 'False', 'nan', 'inf', '-inf')):
        bad.append(f'{path}={obj!r}')
    return bad


def main():
    tmp = tempfile.mkdtemp(prefix='closed_values_')
    try:
        beds = {
            'A': make_bed(os.path.join(tmp, 'A_bimodal')),
            'B': make_bed(os.path.join(tmp, 'B_no_se_se'), se_se=False),
            'C': make_bed(os.path.join(tmp, 'C_rect'), box=(0.012, 0.010)),
            'D': make_bed(os.path.join(tmp, 'D_no_am_s'), am_ids=(1, 2)),
            'E': make_bed(os.path.join(tmp, 'E_mono'), kind='mono', am_ids=(3, 4)),
        }
        runs = {k: run_bed(b) for k, b in beds.items()}
        for k, (pr, met) in runs.items():
            chk(f'0{k} 침대 {k} — {beds[k]["script"]} rc 0 · full_metrics.json',
                pr.returncode == 0 and bool(met), (pr.stderr or pr.stdout or '')[-600:])
        mA, mB, mC, mD, mE = (runs[k][1] for k in 'ABCDE')

        print('[A] (a) 숫자는 숫자로')
        bad = [f'{k}:{b}' for k in 'ABCDE' for b in stringy(runs[k][1])]
        chk('A1 full_metrics.json 다섯 침대에 숫자처럼 생긴 문자열 · 문자열 bool 0 개', not bad, ', '.join(bad[:12]))
        v = mA.get('am_am_n_contacts')
        chk('A2 am_am_n_contacts = int 2 (AM_P–AM_P 1 + AM_P–AM_S 1) · mono = int 0',
            isinstance(v, int) and not isinstance(v, bool) and v == 2
            and isinstance(mE.get('am_am_n_contacts'), int) and mE.get('am_am_n_contacts') == 0,
            f'{v!r} · {mE.get("am_am_n_contacts")!r}')
        chk('A3 am_am_cn 평균 1.0 · 모집단 std √0.5 (AM 4 개의 CN 1 · 2 · 1 · 0)',
            same(mA.get('am_am_cn'), 1.0) and same(mA.get('am_am_cn_std'), math.sqrt(0.5)),
            f'{mA.get("am_am_cn")} · {mA.get("am_am_cn_std")}')

        print('[B] (b) 접촉 0 인 쌍 = 0 · 없는 상 = N/A')
        want_n = {'AM_P_AM_P': 1, 'AM_P_AM_S': 1, 'AM_S_AM_S': 0, 'AM_P_SE': 3, 'AM_S_SE': 3, 'SE_SE': 21, 'AM전체_SE': 6}
        got_n = {p: mA.get(f'area_{p}_n') for p in want_n}
        chk('B1 area_<쌍>_n — AM_S–AM_S 는 측정된 0 (두 상 다 있음) · 나머지는 설계한 개수',
            got_n == want_n and all(isinstance(x, int) for x in got_n.values()), str(got_n))
        chk('B2 area_AM_S_AM_S_total = 0.0 · _mean 은 정의 안 됨 (키 없음)',
            mA.get('area_AM_S_AM_S_total') == 0 and 'area_AM_S_AM_S_mean' not in mA,
            f"{mA.get('area_AM_S_AM_S_total')!r} · mean {'있음' if 'area_AM_S_AM_S_mean' in mA else '없음'}")
        rows = read_csv(os.path.join(beds['A']['out'], 'contact_summary.csv'))
        zr = [r for r in rows if r and r[0] == 'AM_S-AM_S']
        allr = [r for r in rows if r and r[0] == 'All']
        chk("B3 접촉 요약 CSV 에 'AM_S-AM_S' 행 = 접촉수 0 · 평균 '—' · 합 0 · 'All' 접촉수 = 29 (21+3+3+1+1+0 · AM전체-SE 는 빼고)",
            len(zr) == 1 and zr[0][1] == '0' and zr[0][2] == '—' and float(zr[0][3]) == 0.0
            and len(allr) == 1 and allr[0][1] == '29', str(rows))
        chk('B4 없는 상은 N/A — AM_S 가 선언만 된 침대 (10:0 꼴) 에 area_AM_S_* 키 · 요약 행 없음',
            not any(k.startswith('area_AM_S_') for k in mD) and mD.get('area_AM_P_AM_P_n') == 1
            and not any(r and r[0].startswith('AM_S') for r in read_csv(os.path.join(beds['D']['out'], 'contact_summary.csv'))),
            str(sorted(k for k in mD if k.startswith('area_') and k.endswith('_n'))))
        chk('B5 mono (1:AM_S,2:SE) — AM_S–AM_S = 0 (AM 2 개 · 서로 안 닿음) · AM_S–SE 3 · SE–SE 21',
            mE.get('area_AM_S_AM_S_n') == 0 and mE.get('area_AM_S_SE_n') == 3 and mE.get('area_SE_SE_n') == 21,
            str({k: mE.get(k) for k in sorted(mE) if k.startswith('area_') and k.endswith('_n')}))

        print('[C] (c) τ 가 없어도 φ')
        chk('C1 침대 B (SE–SE 접촉 0) — 관통 없음 · τ 없음 (전제)',
            mB.get('percolation_pct') == 0 and mB.get('tortuosity_mean') in (None, 0),
            f"{mB.get('percolation_pct')} · {mB.get('tortuosity_mean')}")
        chk('C2 phi_se = V_SE / (x·y·판) · phi_am = V_AM / (x·y·판) — τ 와 무관한 기하량',
            same(mB.get('phi_se'), beds['B']['phi_se']) and same(mB.get('phi_am'), beds['B']['phi_am']),
            f"{mB.get('phi_se')} vs {beds['B']['phi_se']} · {mB.get('phi_am')} vs {beds['B']['phi_am']}")
        chk('C3 τ 가 없으면 σ_Bruggeman (sigma_ratio) 은 없다 — 숫자를 지어내지 않는다',
            mB.get('sigma_ratio') is None, repr(mB.get('sigma_ratio')))
        nb = {r[0]: r[1] for r in read_csv(os.path.join(beds['B']['out'], 'network_summary.csv')) if len(r) >= 2}
        chk("C4 네트워크 표에 'SE Volume Fraction' 행 · σ_Bruggeman 행은 없음",
            same(nb.get('SE Volume Fraction'), round(beds['B']['phi_se'], 3), 1e-12)
            and not any(k.startswith('σ_Bruggeman') for k in nb), str(nb)[:400])
        chk('C5 τ 있는 침대 A 는 그대로 — phi_se · sigma_ratio 둘 다',
            same(mA.get('phi_se'), beds['A']['phi_se']) and isinstance(mA.get('sigma_ratio'), float),
            f"{mA.get('phi_se')} · {mA.get('sigma_ratio')!r}")

        print('[D] (d) 분석기가 union 을 직접')
        chk('D1 porosity_spheresum = porosity = ε_sphere 식 · porosity_union = 쌍 렌즈 식 · overlap_fraction_pct = V_lens/V_구',
            same(mA.get('porosity_spheresum'), beds['A']['eps_s']) and same(mA.get('porosity'), beds['A']['eps_s'])
            and same(mA.get('porosity_union'), beds['A']['eps_u']) and same(mA.get('overlap_fraction_pct'), beds['A']['ov']),
            f"{mA.get('porosity_spheresum')} · {mA.get('porosity_union')} · {mA.get('overlap_fraction_pct')} vs "
            f"{beds['A']['eps_s']} · {beds['A']['eps_u']} · {beds['A']['ov']}")
        u0 = mA.get('porosity_union')
        pr2 = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'recompute_porosity_dual.py'), '--dir', beds['A']['out'],
                              '--csv-out', os.path.join(tmp, 'dual.csv')], capture_output=True, text=True, timeout=300)
        with open(os.path.join(beds['A']['out'], 'full_metrics.json')) as fh:
            m2 = json.load(fh)
        chk('D2 2e (recompute_porosity_dual --dir) 뒤에도 같은 값 — 분석기 값 ↔ 2e 값 1e-9 안 (원 공극률 고정식)',
            pr2.returncode == 0 and u0 is not None and same(m2.get('porosity_union'), u0)
            and same(m2.get('overlap_fraction_pct'), mA.get('overlap_fraction_pct')),
            f"rc {pr2.returncode} · {u0} → {m2.get('porosity_union')} · {(pr2.stderr or '')[-200:]}")
        with open(os.path.join(HERE, 'app.py'), encoding='utf-8') as fh:
            src = fh.read()

        def body(fn):
            m = re.search(rf'\ndef {fn}\(.*?(?=\n@app\.route|\ndef )', src, re.S)
            return m.group(0) if m else ''
        chk('D3 2e 가 없는 재분석 경로 (batch_rerun_physics · archive_reanalyze) 도 같은 분석기를 부른다 → union 이 남는다',
            all("analyze_contacts_bimodal.py' if mode == 'bimodal' else 'analyze_contacts.py'" in body(f)
                and 'recompute_porosity_dual' not in body(f) for f in ('batch_rerun_physics', 'archive_reanalyze')),
            'body 대조 실패')

        print('[H] (h) 비정사각 상자')
        chk('H1 상자 0.012 × 0.010 — ε_sphere · ε_union = x·y·판 상자 (옛 코드 = x² 로 계산)',
            same(mC.get('porosity'), beds['C']['eps_s']) and same(mC.get('porosity_union'), beds['C']['eps_u']),
            f"{mC.get('porosity')} vs {beds['C']['eps_s']} · {mC.get('porosity_union')} vs {beds['C']['eps_u']}")
        chk('H2 φ_SE 도 같은 상자 (이미 x·y 였다 — 두 식이 한 상자를 쓴다)',
            same(mC.get('phi_se'), beds['C']['phi_se']), f"{mC.get('phi_se')} vs {beds['C']['phi_se']}")
        try:
            sys.path.insert(0, SCRIPTS)
            import recompute_porosity_dual as RPD
            at = {1: {'x': 0, 'y': 0, 'z': 0, 'radius': 0.001, 'type': 1}}
            es, eu, ov = RPD.compute_dual(at, [], 0.01, box_xy=0.012, box_y=0.010)
            ok_h3 = same(es, (1 - sphere_v(0.001) / (0.012 * 0.010 * 0.01)) * 100)
            ex = ''
        except Exception as e:                      # noqa: BLE001 — 옛 시그니처 (box_y 없음) 는 TypeError
            ok_h3, ex = False, repr(e)
        chk('H3 recompute_porosity_dual.compute_dual(box_xy, box_y) — 비정사각 상자', ok_h3, ex)

        print('[W] 웹앱 — 옛 케이스의 숫자 문자열도 숫자로')
        for k, v in (('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_UPLOAD_FOLDER', 'uploads'),
                     ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
            os.environ[k] = os.path.join(tmp, v)
        sys.path.insert(0, HERE)
        import generate_comparison_plots as G
        mp = G._merged_params({'am_am_n_contacts': '412', 'ps_ratio': '7:3', 'x': 1.5, 'flag': True,
                               'sflag': 'True', 'snan': 'nan', 'plate_z_source': 'mesh'})
        chk("W1 그룹 그림 _merged_params — '412' → 412.0 · '7:3' · bool · 'True' · 'nan' · 'mesh' 는 빠진다",
            mp.get('am_am_n_contacts') == 412.0 and mp.get('x') == 1.5
            and not ({'ps_ratio', 'flag', 'sflag', 'snan', 'plate_z_source'} & set(mp)), str(mp))
        import app as A
        cdir = os.path.join(os.environ['WEBAPP_RESULTS_FOLDER'], 'legacy_case')
        os.makedirs(cdir, exist_ok=True)
        with open(os.path.join(cdir, 'full_metrics.json'), 'w') as fh:
            json.dump({'am_am_n_contacts': '412', 'porosity': 15.6, 'ps_ratio': '7:3', 'tortuosity_use_median': 'False'}, fh)
        r = A.app.test_client().post('/group/param-options', data={'cases': ['legacy_case']})
        params = (r.get_json() or {}).get('params', []) if r.status_code == 200 else []
        chk("W2 그룹 선택기 /group/param-options — 옛 문자열 '412' 인 am_am_n_contacts 도 고를 수 있다 · 'False' · '7:3' 은 아니다",
            'am_am_n_contacts' in params and 'porosity' in params
            and 'ps_ratio' not in params and 'tortuosity_use_median' not in params, f'{r.status_code} · {params}')
        tables, met, _ip = A._load_case_tables(beds['A']['out'], {'id': 'A', 'name': 'A'})
        cs = tables.get('contact_summary', {})
        zrow = [x for x in cs.get('data', []) if x and x[0] == 'AM_S-AM_S']
        chk('W3 케이스 페이지 접촉 요약 표 (_load_case_tables) 에 AM_S-AM_S 0 행이 보인다',
            len(zrow) == 1 and str(zrow[0][1]) == '0', str(cs.get('data'))[:400])
        tB, _mB, _ = A._load_case_tables(beds['B']['out'], {'id': 'B', 'name': 'B'})
        labels = [str(x[0]) for x in tB.get('network_summary', {}).get('data', [])]
        chk('W4 τ 없는 침대의 케이스 페이지 네트워크 표에 φ_SE 행 (① 라벨 그대로)',
            any(lb.startswith('SE volume fraction φ_SE') for lb in labels), str(labels)[:400])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    n = _ok + len(_fail)
    print(f'\n{_ok}/{n}  ' + ('✓ 전부 통과' if not _fail else f'✗ {len(_fail)} 건 실패'))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
