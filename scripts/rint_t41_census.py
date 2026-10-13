#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""①′ T4-1 `ledger_census` — 리포 안 AM-only scaffold 의 **raster 원장 조사** (보고 전용 · 솔브 없음 · 2026-10-13).

계약 = v2 §4 T4-1 (L414: 부류별 수 · support/true 분포 · 탄소 덮인 목 몫 · 3중 수 · 미실현 사유) · §3-6 (D4′ = T4-1 뒤) ·
v3 §7-1 T4-1 (L327: 정의된 census · **σ 를 보고 예외 법칙을 바꾸지 않는다** · a_lt_h · 탄소 가림 · 3중 수 추가) ·
v3.1 §1 N8b (동심 비동일 수를 census 에 넣는다).  판정 = docs/reviews/codex_review_rint_g2_v3_20261007.md (census 개발 GO).

⛔ 보고 전용 — σ 솔브 없음 · 예외 법칙 (D4′) 결정 아님 · ①′ 정량 채택 · 생산 HOLD · 웹앱 화면 없음 (기구 · 시험 전용).
침대 (리포 안 AM-only scaffold · 첨가제 점 집합이 리포에 없다 → 탄소 덮인 목 몫 = 0 은 **정의상** 0):
  real_14   docs/data/real14_am_scaffold.csv (+ 덤프 2,060,000 → 조인 · DEM 대조)
  case15    docs/data/case15_corner_20261001/case15_am_scaffold.csv (+ 덤프 1,710,000 → 조인 · DEM 대조)
  kit_ps_5_5 docs/data/kit_ps_scaffolds/kit_ps_5_5__am_scaffold.csv.gz (덤프 없음 → δ_bound = scaffold 자릿수 + 덤프 %g 6 **가정**)
격자 (생산 규약 둘):
  vox0.4_bridge1.2h   vox 0.4 µm · 브리지 기본 1.2·vox = 0.48 µm  — 킷 run_mpm.sh `--step3-vox 0.4` (브리지 인자 없음)
  vox0.15_bridge0.24  vox 0.15 µm · 브리지 0.24 µm 물리 고정      — Phase A · Lee STEP3 러너 (VOX=0.15 BRIDGE_UM=0.24 · CL-87 · CL-88)
틀 = LIGGGHTS 상자 × 1000 µm · lo = (0, 0, 0) (바닥 z 0 · 옆면 0) · hi = (L, L, max(z + r)) · 비주기 raster (생산 STEP3 와 같은 규약 —
생산 MPM 프레임과 원점 위상이 같은지는 확인 안 함 → 통계 대표성만 · 셀 단위 재현 주장 아님) · dilate_z 1 (킷 생산 run_mpm.sh 는
`--dilate-z 1.0214` — ①′ 은 N1 로 그 기하를 거부한다).

  python3 scripts/rint_t41_census.py --out docs/data/rint_t41_census_20261013      # 전부 (침대 × 격자 = 6 작업 · 작업마다 하위 프로세스)
  python3 scripts/rint_t41_census.py --selftest
"""
import argparse
import datetime
import json
import os
import platform
import resource
import subprocess
import sys
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

TOL_AM_UM = 0.10                 # 브리지 쌍 규칙 (econn · rasterize 기본 · 생산 그대로)
CONFIGS = {
    'vox0.4_bridge1.2h': {'vox': 0.4, 'bridge_um': None,
                          'basis': '킷 run_mpm.sh --step3-vox 0.4 · --step3-bridge-um 없음 (기본 1.2·vox)'},
    'vox0.15_bridge0.24': {'vox': 0.15, 'bridge_um': 0.24,
                           'basis': 'Phase A · Lee STEP3 러너 VOX=0.15 BRIDGE_UM=0.24 (CL-87 · CL-88 물리 고정)'},
}
BEDS = {
    'real_14': {'scaffold': 'docs/data/real14_am_scaffold.csv',
                'atom': 'docs/data/real14_reference_20260928/atom_2060000.liggghts.gz',
                'contact': 'docs/data/real14_reference_20260928/contact_2060000.liggghts.gz',
                'type_map': {1: 'AM_P', 2: 'AM_S', 3: 'SE'}, 'box_lateral_sim': None},
    'case15': {'scaffold': 'docs/data/case15_corner_20261001/case15_am_scaffold.csv',
               'atom': 'docs/data/case15_corner_20261001/atom_v4_1710000.liggghts.gz',
               'contact': 'docs/data/case15_corner_20261001/contact_v4_1710000.liggghts.gz',
               'type_map': {1: 'AM_P', 2: 'SE'}, 'box_lateral_sim': None},
    'kit_ps_5_5': {'scaffold': 'docs/data/kit_ps_scaffolds/kit_ps_5_5__am_scaffold.csv.gz', 'atom': None, 'contact': None,
                   'type_map': None, 'box_lateral_sim': 'docs/data/kit_ps_scaffolds/kit_ps_5_5__mpm_input.json'},
}
CARBON_NOTE = ('0 — 리포에 첨가제 (VGCF · SDCP · SuperP) 점 집합이 없다 · AM-only raster 라 덮인 목이 정의상 없다 '
               '(N_c^surv = N_c^0) · 실침대의 탄소 가림 몫은 첨가제 점 집합이 있는 기계에서 (원장 RINT-08 · v3 §2-2)')


def _quant(x):
    x = np.asarray(x, np.float64)
    if x.size == 0:
        return None
    q = np.percentile(x, [0, 10, 50, 90, 100])
    return {'n': int(x.size), 'p0': float(q[0]), 'p10': float(q[1]), 'p50': float(q[2]), 'p90': float(q[3]), 'p100': float(q[4])}


def _git(*args):
    try:
        return subprocess.run(['git', '-C', ROOT, *args], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:                                  # noqa: BLE001
        return None


def _seam_pairs(c, r, L_um, tol):
    """옆면 주기 (x · y) 에서만 닿는 AM 쌍 — 최소 영상 거리 ≤ r_i + r_j + tol 인데 raw 거리는 아니다 (비주기 raster 가 표현 못 함 ·
    seam_unrepresented).  → (닿음 δ > 0 수, 브리지 쌍 규칙 (gap ≤ tol) 수)."""
    from scipy.spatial import cKDTree
    n = len(c)
    if n < 2:
        return 0, 0
    box = np.array([L_um, L_um, 1e9])
    cw = np.mod(c, box)
    tree = cKDTree(cw, boxsize=box)
    touch, bridge = 0, 0
    for i, j in tree.query_pairs(2.0 * float(r.max()) + tol):
        draw = float(np.linalg.norm(c[i] - c[j]))
        d = c[i] - c[j]
        d[:2] -= L_um * np.round(d[:2] / L_um)
        dmi = float(np.linalg.norm(d))
        if dmi + 1e-9 < draw:
            if dmi < r[i] + r[j]:
                touch += 1
            if dmi <= r[i] + r[j] + tol:
                bridge += 1
    return touch, bridge


def _contact_point(c, r, a, b):
    v = c[b] - c[a]
    d = float(np.linalg.norm(v))
    x = (d * d + r[a] ** 2 - r[b] ** 2) / (2 * d) if d > 0 else 0.0
    return c[a] + v * (x / d if d > 0 else 0.0)


def census_job(bed_name, cfg_name, *, scaffold=None, box_lateral_um=None, join=None, delta_bound_um=None, delta_bound_source=None):
    """한 침대 × 한 격자 — raster + 원장 (솔브 없음) → census dict."""
    import step3_sigma as S3
    import rint_iface_join as J
    cfg = CONFIGS[cfg_name]
    vox, bridge = cfg['vox'], cfg['bridge_um']
    sc = J.read_scaffold_csv(scaffold)
    c, r, t = sc['xyz'] * 1000.0, sc['r'] * 1000.0, sc['t']
    if join is not None:
        c, r, t = join['particles']['c_um'], join['particles']['r_um'], join['particles']['t']
    L = float(box_lateral_um)
    lo, hi = (0.0, 0.0, 0.0), (L, L, float((c[:, 2] + r).max()))
    t0 = time.time()
    sid, _pid = S3.rasterize(c, r, t, None, None, lo, hi, vox, bridge_um=bridge, tol_am_um=TOL_AM_UM)
    t1 = time.time()
    led = S3.am_iface_ledger(c, r, t, sid, sid, lo, vox, delta_bound_um=float(delta_bound_um), tol_am_um=TOL_AM_UM, bridge_um=bridge)
    t2 = time.time()
    out = {'bed': bed_name, 'config': cfg_name, 'vox_um': vox, 'bridge_um_effective': led['bridge_um'],
           'bridge_um_requested': bridge, 'tol_am_um': TOL_AM_UM, 'box_um': [list(lo), list(hi)],
           'grid': list(sid.shape), 'n_cells': int(sid.size), 'n_M': led['n_M'],
           'delta_bound_um': float(delta_bound_um), 'delta_bound_source': delta_bound_source,
           'n_particles': {'AM_P': int((t == 1).sum()), 'AM_S': int((t == 2).sum())},
           'rejections': [{'code': x['code'], 'n': x.get('n')} for x in led['rejections']],
           'n8_exact_duplicate': int(sum(x.get('n', 0) for x in led['rejections'] if x['code'] == 'exact_duplicate')),
           'n8b_concentric_nonidentical': int(sum(x.get('n', 0) for x in led['rejections'] if x['code'] == 'concentric_nonidentical')),
           'time_s': {'rasterize': round(t1 - t0, 2), 'ledger': round(t2 - t1, 2)}}
    if led['owner'] is None:
        out['note'] = '원장이 owner 를 만들지 않았다 (N8 · N8b 거부) — 나머지 census 없음'
        return out
    C, F = led['contacts'], led['faces']
    cls = C['cls']; nC = len(cls); h2 = vox * vox
    names = S3.IFACE_CONTACT_CLASSES
    out['n_registered_pairs'] = int(nC)
    out['classes'] = {nm: int((cls == k).sum()) for k, nm in enumerate(names)}
    tk = np.asarray(C['type_key']).astype(str)
    out['classes_by_type'] = {key: {nm: int(((cls == k) & (tk == key)).sum()) for k, nm in enumerate(names)}
                              for key in S3.IFACE_TYPE_KEYS}
    c0 = cls == 0
    sup = c0 & (C['n0'] > 0) & (C['A_true'] > 0)
    out['support_over_true_contact'] = _quant(C['n0'][sup] * h2 / C['A_true'][sup])
    amb = (cls == 1) & (C['n0'] > 0) & (C['A_hi'] > 0)
    out['support_over_true_ambiguous_a_hi'] = _quant(C['n0'][amb] * h2 / C['A_hi'][amb])
    out['support_faces_contact'] = _quant(C['n0'][c0])
    out['a_um_contact'] = _quant(C['a_um'][c0])
    out['a_lt_h'] = {'contact': int((c0 & C['a_lt_h']).sum()), 'contact_of': int(c0.sum()),
                     'ambiguous_a_hi': int(((cls == 1) & C['a_lt_h']).sum()), 'ambiguous_of': int((cls == 1).sum()),
                     'meaning': 'a < h — CNC 편향 미인증 범위 (RRM 없음 · v3 §2-1) · RRM 기준이면 unresolved_subgrid'}
    reg = F['cid'] >= 0
    out['triple'] = {'n_contacts_with_triple_face': int((C['n_triple'] > 0).sum()), 'n_triple_faces_registered': int((F['triple'] & reg).sum()),
                     'n_faces_registered': int(reg.sum()), 'n_cells_multi_claim_ge3': led['n_cells_multi_claim'],
                     'meaning': '면 양쪽 셀 중 하나가 둘 이상의 다른 주인과 닿음 (짝 + 셋째) · 다중 청구 = 청구자 3 이상 셀'}
    out['eps_band_gt1_cells'] = led['n_cells_band_gt1']
    #  미실현 (막을 질 contact 부류인데 S_c^surv 면 0)
    unre = c0 & (C['nsurv'] == 0)
    P = led['particles']
    box_clip = 0
    for q in np.flatnonzero(unre & (C['n0'] == 0)).tolist():
        p = _contact_point(P['c'], P['r'], int(C['a'][q]), int(C['b'][q]))
        if np.any(p < np.asarray(lo)) or np.any(p >= np.asarray(hi)):
            box_clip += 1
    out['unrealized'] = {'n': int(unre.sum()), 'carbon': int((unre & (C['n0'] > 0)).sum()),
                         'box_clip': int(box_clip), 'no_support': int((unre & (C['n0'] == 0)).sum()) - int(box_clip),
                         'meaning': ('contact 부류인데 owner 쌍 면 0 — box_clip = 접촉점이 raster 상자 밖 (옆면 · 바닥 잘림) · '
                                     'no_support = 상자 안인데 면 없음 · carbon = 첨가제가 목을 덮음 (여기서는 정의상 0)')}
    out['unregistered'] = {'n_faces': int((~reg).sum()), 'n_faces_surv': int(((~reg) & F['surv']).sum()),
                           'n_pairs': int(len(np.unique(F['pair'][~reg]))),
                           'meaning': '등록 쌍 (gap ≤ tol) 이 아닌데 두 주인이 면을 공유 — 양자화 융합 · 브리지가 셋째를 찌름 (v2 §3-6)'}
    out['carbon_covered_neck_share'] = 0.0
    out['carbon_covered_neck_share_note'] = CARBON_NOTE
    st, sb = _seam_pairs(c, r, L, TOL_AM_UM)
    out['seam_scaffold'] = {'n_touch': st, 'n_bridge_rule': sb,
                            'meaning': '옆면 주기 영상으로만 닿는 AM 쌍 (scaffold 기하) — 비주기 raster 가 표현 못 함 (seam_unrepresented · v2 §3-6)'}
    if join is not None:
        out['dem_crosscheck'] = S3._iface_join_crosscheck(led, join)
    out['fp_sid'] = led['fp_sid']
    out['peak_rss_mb'] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0, 1)
    return out


def bed_setup(bed_name):
    """침대 → (scaffold 경로, 옆면 L µm, 조인 기록 또는 None, δ_bound µm, 출처 문구)."""
    import rint_iface_join as J
    B = BEDS[bed_name]
    scaf = os.path.join(ROOT, B['scaffold'])
    if B['atom']:
        jn = J.am_iface_join(scaf, os.path.join(ROOT, B['atom']), os.path.join(ROOT, B['contact']), type_map=B['type_map'])
        if jn['status'] != 'PASS':
            raise SystemExit(f'{bed_name}: 조인 관문 실패 {[x["code"] for x in jn["rejections"]]} — census 중단 (fail-closed)')
        A = J.read_atom_dump_frame(os.path.join(ROOT, B['atom']))
        L = float(A['box_hi'][0] - A['box_lo'][0]) * 1000.0
        if abs(float(A['box_hi'][1] - A['box_lo'][1]) * 1000.0 - L) > 1e-9:
            raise SystemExit(f'{bed_name}: 옆면이 정사각이 아니다')
        return scaf, L, jn, float(jn['g_geo']['delta_bound_um']), 'rint_iface_join g_geo.delta_bound_um (scaffold 자릿수 + 덤프 실측 반폭)'
    with open(os.path.join(ROOT, B['box_lateral_sim']), encoding='utf-8') as fh:
        L = float(json.load(fh)['lateral_box']) * 1000.0
    sc = J.read_scaffold_csv(scaf)
    hs = sc['half']
    #  덤프가 리포에 없다 → 덤프 %g 6 유효숫자를 **가정** (real_14 · case15 덤프 실측 S = 6 과 같은 형식이라는 가정 · 확인 안 됨)
    hd = np.array([J.half_ulp_tokens(np.array([format(float(np.abs(sc['xyz'][:, k]).max()), '.6g')]), 6)[0] for k in range(3)])
    hr = float(J.half_ulp_tokens(np.array([format(float(sc['r'].max()), '.6g')]), 6)[0])
    db = 1000.0 * float(np.sqrt(((2.0 * (hs + hd)) ** 2).sum()) + 2.0 * (hs + hr))
    return scaf, L, None, db, 'scaffold 자릿수 + 덤프 %g 6 유효숫자 **가정** (덤프 리포에 없음 · 확인 안 됨)'


def _child(bed, cfg, out_json):
    scaf, L, jn, db, src = bed_setup(bed)
    res = census_job(bed, cfg, scaffold=scaf, box_lateral_um=L, join=jn, delta_bound_um=db, delta_bound_source=src)
    if jn is not None:
        res['join'] = {'status': jn['status'], 'fp_join': jn['fp_join'], 'files': jn['files'], 'steps': jn['steps'],
                       'scaffold_frame_claim': jn['scaffold_frame_claim'],
                       'g_geo': {k: v for k, v in jn['g_geo'].items() if k not in ('rule', 'delta_bound_rule')},
                       'g_frame': {k: v for k, v in jn['g_frame'].items() if k != 'rule'}}
    with open(out_json, 'w', encoding='utf-8') as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)


def run_all(out_dir, beds, cfgs):
    os.makedirs(out_dir, exist_ok=True)
    parts = []
    for bed in beds:
        for cfg in cfgs:
            pj = os.path.join(out_dir, f'_part_{bed}__{cfg}.json')
            t0 = time.time()
            p = subprocess.run([sys.executable, os.path.abspath(__file__), '--child', bed, cfg, pj], capture_output=True, text=True)
            el = time.time() - t0
            if p.returncode != 0 or not os.path.exists(pj):
                parts.append({'bed': bed, 'config': cfg, 'status': 'FAILED', 'rc': p.returncode, 'stderr_tail': p.stderr[-2000:],
                              'wall_s': round(el, 1)})
                print(f'  {bed} × {cfg}: FAILED rc {p.returncode}', flush=True)
                continue
            with open(pj, encoding='utf-8') as fh:
                res = json.load(fh)
            os.remove(pj)
            res['status'] = 'OK'; res['wall_s'] = round(el, 1)
            parts.append(res)
            print(f"  {bed} × {cfg}: OK {el:.0f} s · grid {res['grid']} · pairs {res.get('n_registered_pairs')} · "
                  f"classes {res.get('classes')} · peak {res.get('peak_rss_mb')} MB", flush=True)
    import numpy as _np, scipy as _sp
    blobs = {f: _git('hash-object', f) for f in ('scripts/step3_sigma.py', 'scripts/rint_iface_join.py', 'scripts/rint_t41_census.py')}
    doc = {'kind': 'rint_t41_census', 'version': 'v1', 'date_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
           'status': ('보고 전용 — σ 솔브 없음 · 예외 법칙 (D4′) 결정 아님 · 결과를 보고 법칙을 바꾸지 않는다 (v3 §7-1 T4-1) · '
                      '①′ 정량 채택 · 생산 HOLD · 웹앱 화면 없음'),
           'git_head': _git('rev-parse', 'HEAD'), 'code_blobs': blobs,
           'environment': {'python': platform.python_version(), 'numpy': _np.__version__, 'scipy': _sp.__version__,
                           'machine': platform.machine(), 'cpu_count': os.cpu_count()},
           'configs': CONFIGS, 'beds': {k: {kk: vv for kk, vv in v.items() if kk != 'type_map'} | {'type_map': v['type_map']}
                                        for k, v in BEDS.items() if k in beds},
           'frame': 'LIGGGHTS 상자 × 1000 µm · lo (0, 0, 0) · hi (L, L, max(z + r)) · 비주기 raster · dilate_z 1 · AM-only (첨가제 · SE 없음)',
           'carbon_note': CARBON_NOTE, 'jobs': parts}
    with open(os.path.join(out_dir, 'census.json'), 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
        fh.write('\n')
    return doc


# ═════════════════════════ selftest ═════════════════════════
def selftest():
    import tempfile
    fails = []

    def chk(name, cond, extra=''):
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        if not cond:
            fails.append(name)
    with tempfile.TemporaryDirectory() as td:
        #  합성 침대: AM_S 두 구 접촉 (z 정렬) + AM_P 두 구 간극 브리지 + 옆면 주기로만 닿는 AM_S 쌍 (x 경계)
        rows = ['# type,x,y,z,r  # selftest scaffold (AM_P=1,AM_S=2)',
                '2,0.003000,0.003000,0.002000,0.001000', '2,0.003000,0.003000,0.003980,0.001000',
                '1,0.007000,0.006500,0.002000,0.001500', '1,0.010040,0.006500,0.002000,0.001500',
                '2,0.000500,0.010000,0.002000,0.001000', '2,0.011480,0.010000,0.002000,0.001000']
        p = os.path.join(td, 's.csv')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(rows) + '\n')
        CONFIGS['_self'] = {'vox': 0.2, 'bridge_um': 0.24, 'basis': 'selftest'}
        try:
            res = census_job('self', '_self', scaffold=p, box_lateral_um=12.0, delta_bound_um=0.0029, delta_bound_source='selftest')
        finally:
            CONFIGS.pop('_self', None)
        cl = res['classes']
        chk('① 부류 합 = 등록 쌍 (contact 1 · gap_bridged 1)', sum(cl.values()) == res['n_registered_pairs'] == 2
            and cl['contact'] == 1 and cl['gap_bridged'] == 1, repr(cl))
        chk('② support/true 표본 = contact 중 면 있는 것 · 미실현 0 · 탄소 = 0 (정의상)', res['support_over_true_contact']['n'] == 1
            and res['unrealized']['n'] == 0 and res['carbon_covered_neck_share'] == 0.0, repr(res['support_over_true_contact']))
        chk('③ 옆면 주기로만 닿는 쌍 = seam 1 (닿음 · 브리지 규칙 둘 다)', res['seam_scaffold']['n_touch'] == 1
            and res['seam_scaffold']['n_bridge_rule'] == 1, repr(res['seam_scaffold']))
        chk('④ 거부 없음 · N8 · N8b 0 · a_lt_h 정의 (contact_of = 1)', res['rejections'] == [] and res['n8_exact_duplicate'] == 0
            and res['n8b_concentric_nonidentical'] == 0 and res['a_lt_h']['contact_of'] == 1, repr(res['rejections']))
    print('SELFTEST', 'PASS' if not fails else f'FAIL {fails}')
    return 0 if not fails else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default='')
    ap.add_argument('--beds', default=','.join(BEDS))
    ap.add_argument('--configs', default=','.join(CONFIGS))
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--child', nargs=3, metavar=('BED', 'CONFIG', 'OUT_JSON'), help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.child:
        _child(*a.child)
        return 0
    if not a.out:
        ap.error('--out 이 필요하다')
    run_all(a.out, a.beds.split(','), a.configs.split(','))
    return 0


if __name__ == '__main__':
    sys.exit(main())
