#!/usr/bin/env python3
"""comsol_export.py — 케이스/킷 → comsol_pkg (스키마 v1.0, mph 생성기와의 계약).

킷 디렉터리(am_scaffold.csv · se_scaffold.csv · mpm_input.json · mpm_metrics.json ·
mpm_payload.json 중 있는 것)를 읽어 COMSOL 하이브리드 모델 입력 패키지를 쓴다:

  manifest.json / am_spheres.csv / am_am_contacts.csv / vgcf_fibres.csv /
  se_domain.json / electrochem.json / (ocp_*.csv 복사) / conventions.md / provenance.json

물리 결정 (2026-08-05 사용자 확정 — 변경 금지):
  · AM 구 = 해상 기하 (스피어 그대로) / SE = 연속체 κ_dom / VGCF = 1D Edge
    (단면 π·(0.075 µm)² 정확) / PTFE = 기하 금지 (차단 효과는 κ_dom·f_cov 몫)
  · AM-AM 넥 = DEM δ 의 Hertz 탄성 접촉 (NCM 140 GPa ≫ SE 1.35 → AM-AM 소성 미미;
    Stage-E 소성 면적은 TODO(trackb) 옵션으로만)
  · single-ion: LPSCl t⁺≈1 → 농도분극 없음.  일반 DFN 인터페이스 금지 (conventions.md §3)
  · provenance 필수: 산출물이 자기 실행조건·출처를 스스로 말한다 (SE 곡선 5점의
    sub/frames 를 되찾지 못해 곡선 전체를 폐기한 세션 교훈)

§F1 날조 금지: 킷에서 못 찾은 값은 null + provenance/reason.  미결 조각은
TODO(trackb) 주석으로 명시.

  python3 scripts/comsol_export.py --kit <킷 디렉터리> --out comsol_pkg_<case>
  python3 scripts/comsol_export.py --selftest
"""
import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np
from scipy.spatial import cKDTree

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)
# σ_e 클래스값은 step3_sigma 에서 import — 값을 여기 복붙하면 SDCP 150→250 류의
# 드리프트가 재발한다 (단일 출처 원칙).  VGCF 지름·phase 코드도 additives 가 정본.
from step3_sigma import SIGMA_DEFAULT, SIGMA_ION_SE_S_CM_25C     # noqa: E402
import se_material                                               # noqa: E402  (T_REF_C 규약)
from additives import PHASE as ADD_PHASE, VGCF_D                 # noqa: E402

SCHEMA_VERSION = '1.0'
TAU_CONVENTION = 'linear: sigma_eff = sigma_bulk*phi/tau'
# AM-AM 접촉 규약: gap ≤ 0.10 µm — step3_sigma.rasterize(tol_am_um=0.10)/econn 과 동일해야
# 복셀 σ 솔브가 잇는 접촉과 이 패키지의 접촉 목록이 같은 그래프가 된다 (규약 분기 금지).
TOL_AM_UM = 0.10
_UM_PER_LU = 1000.0            # LIGGGHTS box units(=mm) → µm (mpm_input_from_case 규약)


# ─────────────────────────── 공용 유틸 ───────────────────────────

def read_scaffold(path):
    """type,x,y,z,r ('#' 주석/헤더 허용) → (type[n], xyz_um[n,3], r_um[n]).

    좌표 단위: 킷 스캐폴드는 LIGGGHTS LU(1 LU = 1 mm; lateral 0..0.05 = 50 µm) → ×1000 µm.
    cycle_contact_ledger.load_atoms 와 동일한 median-radius 감지 (r 중앙값 < 0.05 → LU) —
    µm 스캐폴드를 실수로 다시 ×1000 하면 수축·접촉이 전부 무너지므로 맹목 변환 금지."""
    T, X, R = [], [], []
    with open(path, newline='') as f:
        for row in csv.reader(f):
            if not row or row[0].lstrip().startswith('#'):
                continue
            try:
                t = int(float(row[0]))
                x, y, z, r = (float(row[k]) for k in (1, 2, 3, 4))
            except (ValueError, IndexError):
                continue                                    # 헤더행 등 비수치 행 허용
            T.append(t); X.append((x, y, z)); R.append(r)
    T = np.asarray(T, int); X = np.asarray(X, float).reshape(-1, 3); R = np.asarray(R, float)
    if len(R) and float(np.median(R)) < 0.05:
        X, R = X * _UM_PER_LU, R * _UM_PER_LU
    return T, X, R


def holm_conductance_S(sigma_c_S_cm, a_um):
    """Holm 협착 저항 R = 1/(2·σ_c·a) 의 컨덕턴스 g = 2·σ_c·a [S].
    σ_c 는 S/cm, a 는 µm → cm 로 1e-4.  단위 검산: σ_c=1 S/cm, a=1 µm → g = 2e-4 S."""
    return 2.0 * float(sigma_c_S_cm) * (float(a_um) * 1e-4)


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def _git_commit():
    try:
        out = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=os.path.dirname(_THIS_DIR),
                             capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or None if out.returncode == 0 else None
    except Exception:
        return None                                         # §F1: 실패 시 null (추정 금지)


def _load_json(path):
    """없으면 None; 있는데 깨졌으면 즉시 중단 — 깨진 metrics 를 조용히 무시하면
    trackb 부재로 오진해 dem_stageE 폴백이 나간다 (침묵 다운그레이드 금지)."""
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        raise SystemExit(f'{path}: JSON 파싱 실패 ({type(e).__name__}: {e}) — '
                         f'킷 산출물 손상: 무시하지 않고 중단')


# ─────────────────────────── 킷 읽기 ───────────────────────────

def load_kit(kit):
    """킷 디렉터리에서 있는 것만 모은다.  반환 dict:
    am_(t,x,r) · metrics(dict|None) · payload(dict|None) · mpm_input(dict|None) · inputs(md5용 경로)."""
    k = {}
    amp = os.path.join(kit, 'am_scaffold.csv')
    if not os.path.exists(amp):
        raise SystemExit(f'{kit}: am_scaffold.csv 없음 — AM 해상 기하가 이 패키지의 최소 입력')
    k['am_t'], k['am_x'], k['am_r'] = read_scaffold(amp)
    if len(k['am_r']) == 0:
        raise SystemExit(f'{amp}: 스피어 0개 — export 대상 없음')
    bad = set(np.unique(k['am_t'])) - {1, 2}
    if bad:
        raise SystemExit(f'{amp}: 알 수 없는 type {sorted(bad)} — 스캐폴드 규약은 1=AM_P/2=AM_S '
                         f'(⚠ 복셀 sid 1=AM_S/2=AM_P 와 반대 — 추측 배정 금지)')
    k['inputs'] = {'am_scaffold.csv': amp}
    for name in ('se_scaffold.csv', 'run_mpm.sh'):
        p = os.path.join(kit, name)
        if os.path.exists(p):
            k['inputs'][name] = p
    k['mpm_input'] = _load_json(os.path.join(kit, 'mpm_input.json'))
    if k['mpm_input'] is not None:
        k['inputs']['mpm_input.json'] = os.path.join(kit, 'mpm_input.json')
    m = _load_json(os.path.join(kit, 'mpm_metrics.json'))
    if m is not None:
        k['inputs']['mpm_metrics.json'] = os.path.join(kit, 'mpm_metrics.json')
        if isinstance(m, dict) and 'mpm_metrics' in m:      # 래핑된 형태도 허용
            m = m['mpm_metrics']
    k['metrics'] = m
    pl = _load_json(os.path.join(kit, 'mpm_payload.json'))
    if pl is not None:
        k['inputs']['mpm_payload.json'] = os.path.join(kit, 'mpm_payload.json')
    k['payload'] = pl
    return k


def merged_metrics(kit):
    """metrics json 우선, 없으면 payload 내장 mpm_metrics — 키 조회용 단일 뷰."""
    if kit['metrics'] is not None:
        return kit['metrics']
    if kit['payload'] is not None:
        return kit['payload'].get('mpm_metrics') or {}
    return {}


def find_trackb(kit):
    """step3.trackb 블록 (κ_dom 보정 + per-particle facewalk coverage) — metrics → payload 순."""
    for src, m in (('mpm_metrics.json', kit['metrics']),
                   ('mpm_payload.json', (kit['payload'] or {}).get('mpm_metrics'))):
        if isinstance(m, dict):
            tb = (m.get('step3') or {}).get('trackb') if isinstance(m.get('step3'), dict) else None
            if isinstance(tb, dict):
                return tb, src
    return None, None


# ─────────────────────────── am_spheres.csv ───────────────────────────

def _per_particle_cov(trackb, n_am):
    """trackb.per_particle → 입자별 (f_reaction, f_carbon, f_block).

    ★ 길이 ≠ 스피어 수면 즉시 중단 — SuperP `_fid.max()+1` 전역오프셋 버그 부류의 재발 방지:
    조용히 자르거나 재배열하면 모든 입자가 남의 coverage 를 뒤집어쓴다.  index 규약 =
    am_scaffold.csv 행 순서 (am_surface_patches 의 pid 와 동일해야 함)."""
    pp = trackb.get('per_particle')
    if pp is None:
        return None
    if not isinstance(pp, dict):
        raise SystemExit(f'trackb.per_particle 형식 오류: dict-of-arrays 여야 함 (got {type(pp).__name__})')
    out = {}
    for key in ('f_reaction', 'f_carbon', 'f_block'):
        v = pp.get(key)
        if v is None:
            raise SystemExit(f'trackb.per_particle 에 {key} 없음 — 계약 불충족 '
                             f'(있는 키: {sorted(pp)}); 절반짜리 facewalk 을 조용히 섞지 않는다')
        v = np.asarray(v, float)
        if len(v) != n_am:
            raise SystemExit(f'trackb.per_particle[{key}] 길이 {len(v)} ≠ am_scaffold 스피어 수 '
                             f'{n_am} — 조용한 재배열 금지(오프셋 버그 부류): trackb 생성 시점의 '
                             f'AM 순서와 am_scaffold.csv 일치 여부를 확인하고 재생성할 것')
        out[key] = v
    return out


def build_am_rows(kit, trackb, notes):
    """am_spheres.csv 행 + coverage 출처 라벨.  per_particle(facewalk) 있으면 입자별,
    없으면 클래스 평균 브로드캐스트 (metrics → mpm_input dem_* 순) — 행마다 f_cov_source 라벨."""
    t, x, r = kit['am_t'], kit['am_x'], kit['am_r']
    n = len(r)
    cls = np.where(t == 1, 'AM_P', 'AM_S')                  # 스캐폴드 type 1=AM_P / 2=AM_S
    sig = np.where(t == 1, SIGMA_DEFAULT['AM_P'], SIGMA_DEFAULT['AM_S'])
    pp = _per_particle_cov(trackb, n) if trackb else None
    if pp is not None:
        f_rx, f_cb, f_bk = pp['f_reaction'], pp['f_carbon'], pp['f_block']
        src = 'mpm_facewalk'
    else:
        m = merged_metrics(kit)
        mi = kit['mpm_input'] or {}
        # 클래스 평균 체인: MPM coverage(%) → DEM coverage(%) → 0.0(+경고 note).
        # f_cov_block 은 facewalk 없이는 미계측 → 0.0 하한으로 두되 PTFE 가 실재하면 경고.
        def cov_pct(cls_name):
            for key, tag in ((f'coverage_{cls_name}_mpm_pct', 'mpm class mean'),
                             (f'dem_coverage_{cls_name}_mean', 'dem class mean')):
                v = m.get(key) if key.startswith('coverage') else mi.get(key)
                if v is not None:
                    return float(v), tag
            return None, None
        vals = {}
        for c in ('AM_P', 'AM_S'):
            if (t == (1 if c == 'AM_P' else 2)).any():
                v, tag = cov_pct(c)
                if v is None:
                    v, tag = 0.0, 'ABSENT→0.0 placeholder'
                    notes.append(f'⚠ coverage 원천 부재({c}) — f_cov_reaction=0.0 은 placeholder '
                                 f'(§F1: 측정값 아님; MPM 재실행으로 facewalk 확보 권장)')
                vals[c] = v / 100.0
        add_pct = {c: m.get(f'coverage_{c}_add_mpm_pct') for c in ('AM_P', 'AM_S')}
        # 리뷰 minor: carbon 원천 부재도 침묵하지 않는다 — VGCF/SuperP 실재 킷에서
        # f_cov_carbon=0.0 이 무경고로 나가면 mph 생성기가 "탄소 접점 없음" 으로 오독
        for c in ('AM_P', 'AM_S'):
            if (t == (1 if c == 'AM_P' else 2)).any() and add_pct.get(c) is None \
                    and any((m.get('additive_counts') or {}).get(k) for k in
                            ('VGCF', 'SuperP', 'SWCNT')):
                notes.append(f'⚠ 탄소 첨가제 실재하나 coverage_{c}_add_mpm_pct 부재 — 해당 클래스 '
                             f'전 행 f_cov_carbon=0.0 은 placeholder (§F1: 측정값 아님)')
        f_rx = np.array([vals.get(c, 0.0) for c in cls])
        f_cb = np.array([(float(add_pct.get(c) or 0.0)) / 100.0 for c in cls])
        f_bk = np.zeros(n)
        _adds = (m.get('additive_counts') or {})
        if _adds.get('PTFE'):
            notes.append('⚠ PTFE 존재하나 per_particle facewalk 부재 — f_cov_block=0.0 은 하한 '
                         '(차단 미계측; κ_dom·f_cov 반영은 facewalk 필요)')
        src = 'class_mean_fallback'
    rows = []
    for i in range(n):
        rows.append([i, x[i, 0], x[i, 1], x[i, 2], r[i], cls[i], float(sig[i]),
                     float(f_rx[i]), float(f_cb[i]), float(f_bk[i]), src])
    return rows, src


def write_am_spheres(out, rows):
    p = os.path.join(out, 'am_spheres.csv')
    with open(p, 'w', newline='') as f:
        f.write('# comsol_pkg v1.0 am_spheres — cls ∈ {AM_P,AM_S} (스캐폴드 type 1=AM_P/2=AM_S; '
                '⚠ 복셀 sid 1=AM_S/2=AM_P 와 반대), f_cov_source ∈ {mpm_facewalk,class_mean_fallback}\n')
        f.write(f"# sigma_e_S_cm = step3_sigma.SIGMA_DEFAULT (AM_P {SIGMA_DEFAULT['AM_P']} / "
                f"AM_S {SIGMA_DEFAULT['AM_S']} S/cm, A1-locked Trevisanello 5/10 mS/cm)\n")
        f.write('# id = am_scaffold.csv 행 순서 (per_particle facewalk 의 index 규약과 동일)\n')
        w = csv.writer(f)
        w.writerow(['id', 'x_um', 'y_um', 'z_um', 'r_um', 'cls', 'sigma_e_S_cm',
                    'f_cov_reaction', 'f_cov_carbon', 'f_cov_block', 'f_cov_source'])
        for row in rows:
            w.writerow([row[0]] + [f'{v:.12g}' for v in row[1:5]] + [row[5], f'{row[6]:.12g}',
                        f'{row[7]:.12g}', f'{row[8]:.12g}', f'{row[9]:.12g}', row[10]])
    return p


# ─────────────────────────── am_am_contacts.csv ───────────────────────────

def build_contacts(kit):
    """AM-AM 접촉: gap ≤ TOL_AM_UM (rasterize tol_am_um 과 동일 규약).
    δ = max(0, ri+rj−d) → 근접-비겹침(0<gap≤tol) 쌍은 δ=0, a=0, g=0 으로 나열만 한다
    (STEP3 복셀 솔브는 그 쌍도 브리지로 잇는다 — 목록에서 빼면 그래프가 달라짐).
    탐색은 전역 query_pairs — 후보쌍 = 반경 2·r_max+tol 이내라 bimodal(대립 소수) /
    mono-소립(대량이지만 r_max 작음) 어느 쪽도 후보 폭발 없음 (ledger 식 분리탐색 불필요)."""
    x, r, t = kit['am_x'], kit['am_r'], kit['am_t']
    sig = np.where(t == 1, SIGMA_DEFAULT['AM_P'], SIGMA_DEFAULT['AM_S'])
    rows = []
    if len(r) >= 2:
        pairs = cKDTree(x).query_pairs(2.0 * float(r.max()) + TOL_AM_UM, output_type='ndarray')
        for i, j in sorted(map(tuple, pairs)):
            d = float(np.linalg.norm(x[i] - x[j]))
            if d > r[i] + r[j] + TOL_AM_UM:
                continue
            delta = max(0.0, float(r[i] + r[j] - d))
            rstar = float(r[i] * r[j] / (r[i] + r[j]))
            a = float(np.sqrt(rstar * delta))
            sc = 2.0 * sig[i] * sig[j] / (sig[i] + sig[j])   # 이종 접촉의 직렬(조화) σ [S/cm]
            rows.append([int(i), int(j), delta, a, holm_conductance_S(sc, a)])
    return rows


def write_contacts(out, rows):
    p = os.path.join(out, 'am_am_contacts.csv')
    with open(p, 'w', newline='') as f:
        f.write(f'# comsol_pkg v1.0 am_am_contacts — 접촉 규약: gap <= {TOL_AM_UM} um '
                f'(= step3_sigma.rasterize tol_am_um; econn 과 동일)\n')
        f.write('# R*=ri*rj/(ri+rj); a=sqrt(R**delta); sigma_c=2*si*sj/(si+sj) [S/cm]; '
                'g=2*sigma_c*(a_um*1e-4) [S] (Holm R=1/(2*sigma_c*a))\n')
        f.write('# Hertz 탄성 δ 그대로 (NCM 140 GPa ≫ SE 1.35 → AM-AM 소성 미미 = 하한이 물리값 근처)\n')
        # TODO(trackb): Stage-E 소성-면적 옵션 — network_conductivity 의 physics 모드(A_tabor/
        #   A_volume min-caps)를 연결해 a 를 상한 밴드로도 병기 (계약 v1.0 은 Hertz 단일).
        f.write('# TODO(trackb): Stage-E 소성-면적 옵션 (network_conductivity physics 모드 연결)\n')
        w = csv.writer(f)
        w.writerow(['i', 'j', 'delta_um', 'a_hertz_um', 'g_holm_S'])
        for i, j, d, a, g in rows:
            w.writerow([i, j, f'{d:.12g}', f'{a:.12g}', f'{g:.12g}'])
    return p


# ─────────────────────────── vgcf_fibres.csv ───────────────────────────

def write_vgcf(out, kit, notes):
    """payload additive_fibres(µm 폴리라인)에서 VGCF(phase 2)만 — PTFE(4)는 기하 금지 결정.
    데이터 없으면 헤더만 + manifest.notes 사유."""
    fibres = []
    for fb in ((kit['payload'] or {}).get('additive_fibres') or []):
        try:
            if int(fb.get('phase', -1)) == ADD_PHASE['VGCF'] and fb.get('pts'):
                fibres.append([(float(a), float(b), float(c)) for a, b, c in fb['pts']])
        except (TypeError, ValueError) as e:
            raise SystemExit(f'mpm_payload.json additive_fibres 형식 오류 ({e}) — 폴리라인은 '
                             f'{{phase, pts:[[x,y,z],…]}} µm 규약')
    # TODO(trackb): mpm3d --save-fibre npy 산출물 자동 인식 배선 (payload 없는 킷도 섬유 회수).
    p = os.path.join(out, 'vgcf_fibres.csv')
    with open(p, 'w', newline='') as f:
        f.write(f'# comsol_pkg v1.0 vgcf_fibres — diameter_um={VGCF_D}, '
                f"sigma_S_cm={SIGMA_DEFAULT['VGCF']}  (additives.VGCF_D / step3_sigma.SIGMA_DEFAULT)\n")
        f.write(f'# 1D Edge 규약: 단면 A = pi*({VGCF_D / 2.0} um)^2 정확 (물리 결정 2026-08-05); '
                f'좌표 µm (payload additive_fibres 프레임).  PTFE 는 기하 금지 → 미포함\n')
        w = csv.writer(f)
        w.writerow(['fibre_id', 'seq', 'x_um', 'y_um', 'z_um'])
        for fid, pts in enumerate(fibres):
            for seq, (xx, yy, zz) in enumerate(pts):
                w.writerow([fid, seq, f'{xx:.12g}', f'{yy:.12g}', f'{zz:.12g}'])
    if not fibres:
        notes.append('VGCF 점 데이터 부재 — 킷에 --save-fibre 산출물 없음 (payload additive_fibres '
                     '비었음/없음) → vgcf_fibres.csv 는 헤더만')
    return p, len(fibres)


# ─────────────────────────── se_domain.json ───────────────────────────

def _kdom_ratio_of(tb):
    """kdom_ratio — trackb 기록값 우선; 없으면 (φ_full/τ_full)/(φ_geo/τ_geo) 재계산.
    step3_sigma.kdom_calibration(같은 식) 이 있으면 그 정본을 쓴다 (이중 구현 드리프트 방지)."""
    kd = tb.get('kdom_ratio')
    if kd is not None:
        return float(kd), 'trackb.kdom_ratio'
    args = [tb.get(k) for k in ('phi_full', 'tau_full', 'phi_geo', 'tau_geo')]
    if any(v is None for v in args):
        return None, None
    try:
        import step3_sigma as _s3
        fn = getattr(_s3, 'kdom_calibration', None)
        if fn is not None:
            v = fn(*args)
            return (float(v), 'step3_sigma.kdom_calibration(phi/tau)') if v is not None else (None, None)
    except Exception:
        pass
    pf, tf, pg, tg = (float(v) for v in args)
    if tf <= 0 or tg <= 0 or pg <= 0:
        return None, None
    return (pf / tf) / (pg / tg), 'recomputed (phi_full/tau_full)/(phi_geo/tau_geo)'


def build_se_domain(kit, trackb, notes):
    m = merged_metrics(kit)
    mi = kit['mpm_input'] or {}
    box = (kit['payload'] or {}).get('box') or {}
    # 두께/박스: metrics(MPM press-plane) → payload box → mpm_input(DEM) → 스캐폴드 외피(최후)
    thick = m.get('thickness_mpm_um') or m.get('thickness_um') or box.get('z_max') \
        or mi.get('dem_thickness_um')
    lat_x = box.get('x_max') or (float(mi['lateral_box']) * _UM_PER_LU if mi.get('lateral_box') else None)
    lat_y = box.get('y_max') or lat_x
    if thick is None:
        thick = float((kit['am_x'][:, 2] + kit['am_r']).max())
        notes.append('⚠ thickness 원천 부재 → am_scaffold z-외피로 대체 (press-plane 아님 — 근사 라벨)')
    if lat_x is None:
        lat_x = lat_y = float((kit['am_x'][:, :2] + kit['am_r'][:, None]).max())
        notes.append('⚠ lateral box 원천 부재 → am_scaffold x/y-외피로 대체 (근사 라벨)')
    # porosity: 관례 문자열 필수 — mpm=union / dem=eps_sphere.  서로 다른 관례를 짝짓지 않는다.
    por, por_conv = None, None
    if m.get('porosity_mpm_pct') is not None or m.get('porosity_settled_pct') is not None:
        por = float(m.get('porosity_mpm_pct') if m.get('porosity_mpm_pct') is not None
                    else m.get('porosity_settled_pct'))
        por_conv = 'union'
    elif mi.get('dem_porosity_pct') is not None:
        por, por_conv = float(mi['dem_porosity_pct']), 'eps_sphere'
    d = {'sigma_bulk_ion_S_cm': None, 'kappa_dom_S_cm': None, 'kappa_dom_S_m': None,
         'kdom_ratio': None, 'tau_full': None, 'tau_geo': None, 'phi_full': None, 'phi_geo': None,
         'tau_convention': TAU_CONVENTION, 'porosity_pct': por, 'porosity_convention': por_conv,
         'thickness_um': float(thick), 'box_um': [float(lat_x), float(lat_y), float(thick)],
         'mixed_phase': None, 'source': 'dem_stageE', 'reason': None}
    if trackb is None:
        d['reason'] = ('step3.trackb 부재 (mpm_metrics/mpm_payload 에 없음) — κ_dom/τ/φ 는 null; '
                       'MPM payload 를 trackb 헬퍼(step3_sigma)와 함께 재실행해 채울 것 (§F1)')
        notes.append('se_domain: trackb 부재 → κ_dom null + source=dem_stageE')
        return d
    d['source'] = 'mpm'
    # ★ trackb 부분실패 표면화 (리뷰 minor): writer 계약은 "부분결과 + error 키" —
    #   익스포터가 그걸 가리면 provenance 원칙(산출물이 자기 상태를 말한다)이 깨진다
    if trackb.get('error'):
        notes.append(f"⚠ trackb 부분실패: {trackb['error']} — 아래 값들은 실패 이전 계산분")
        d['reason'] = f"trackb 부분실패({trackb['error']})의 생존 필드만 전달"
    sb = trackb.get('sigma_bulk_ion_S_cm')
    if sb is None:
        # ★ §F1 (리뷰 critical): 키가 **실재하는 None** 은 writer 의 의도적 null 이다 —
        #   mixed 이온상(SDCP+SE)에서 "단일 σ_bulk 기반 τ 정의 불가" 를 명시 기록한 것.
        #   상수로 덮으면 같은 파일의 mixed_phase.reason 과 자기모순 패키지가 되고, mph
        #   생성기가 SE-도메인 σ 로 조용히 틀린 물리를 받는다.  상수 폴백은 키 자체가
        #   없는 구세대 trackb 에만 허용하고 출처 라벨을 필드로 남긴다.
        if 'sigma_bulk_ion_S_cm' in trackb:
            d['sigma_bulk_ion_S_cm'] = None
            _mx = (trackb.get('mixed_phase') or {}).get('reason') if isinstance(
                trackb.get('mixed_phase'), dict) else None
            d['reason'] = ('sigma_bulk_ion: writer 가 의도적으로 null 기록 — '
                           + (_mx or 'trackb 사유 미기재') + ' (§F1: 상수 대입 금지)')
            notes.append('se_domain: sigma_bulk_ion null 유지 (writer 의도 존중, §F1)')
        else:
            d['sigma_bulk_ion_S_cm'] = float(SIGMA_ION_SE_S_CM_25C)
            d['sigma_bulk_source'] = 'default_25C_const'    # manifest note 에만 의존하지 않게
            notes.append('se_domain: 구세대 trackb (sigma_bulk_ion 키 부재) → '
                         f'SIGMA_ION_SE_S_CM_25C ({SIGMA_ION_SE_S_CM_25C} S/cm) 폴백')
    else:
        d['sigma_bulk_ion_S_cm'] = float(sb)
    for k in ('tau_full', 'tau_geo', 'phi_full', 'phi_geo'):
        d[k] = float(trackb[k]) if trackb.get(k) is not None else None
    kd, kd_src = _kdom_ratio_of(trackb)
    d['kdom_ratio'] = kd
    if kd is not None:
        if kd > 1.0:
            # 이중계상 가드: 하이브리드는 AM 을 기하로 해상 → κ_dom 이 σ_bulk 를 넘으면
            # τ 규약(선형 vs √)이 섞였거나 φ_geo 해가 잘못된 것.
            notes.append(f'⚠ kdom_ratio={kd:.4g} > 1 — 규약 불일치 경고 (kdom_calibration 가드): '
                         f'τ 선형/√ 혼동 또는 φ_geo 해 확인')
        if d['sigma_bulk_ion_S_cm'] is not None:
            d['kappa_dom_S_cm'] = kd * d['sigma_bulk_ion_S_cm']
            d['kappa_dom_S_m'] = d['kappa_dom_S_cm'] * 100.0   # 1 S/cm = 100 S/m (병기 규약)
        # sigma_bulk null(mixed 의도적) 이면 κ_dom 도 null 유지 — 비 kd 만으로 절대 σ 날조 금지
    else:
        # 리뷰 지적: 옛 문구는 (phi,tau) 4종 부재까지 단정했는데 mixed 경로는 tau_full 만
        # 의도적 None 이고 나머지는 실재한다 — 실제 부재 항목만 말한다
        _miss = [k for k in ('kdom_ratio', 'tau_full', 'tau_geo', 'phi_full', 'phi_geo')
                 if trackb.get(k) is None]
        d['reason'] = (d.get('reason') or '') + (
            f" | κ_dom 산출 불가 — 부재/None 항목: {', '.join(_miss)} (§F1: null)")
    d['mixed_phase'] = trackb.get('mixed_phase')
    if kd_src:
        notes.append(f'se_domain: kdom_ratio 출처 = {kd_src}')
    return d


# ─────────────────────────── electrochem.json ───────────────────────────

def _find_analysis_pack(kit_dir):
    """킷 안(1단 하위 포함)의 ocp_*.csv + params_*.json 쌍 — run_mpm.sh 의 anchor_params/ 규약.
    (킷 밖 ../anchor_params 는 export 결정성을 위해 뒤지지 않는다 — provenance 가 킷 내부만 보증.)"""
    cands = []
    for base, _dirs, files in os.walk(kit_dir):
        rel = os.path.relpath(base, kit_dir)
        if rel != '.' and os.sep in rel:                    # 킷 루트 + 1단 하위만 (anchor_params/)
            continue
        for fn in sorted(files):
            if fn.startswith('ocp_') and fn.endswith('.csv'):
                cands.append((os.path.join(base, fn), base))
    for ocp, base in cands:
        for fn in sorted(os.listdir(base)):
            if fn.startswith('params_') and fn.endswith('.json'):
                return ocp, os.path.join(base, fn)
    return (cands[0][0], None) if cands else (None, None)


def _x_window_from_run_script(kit_dir, notes):
    """run_mpm.sh 에 구워진 --x0/--x100 (킷이 실제로 실행하는 창) — 여러 값이 섞이면 채택 안 함."""
    p = os.path.join(kit_dir, 'run_mpm.sh')
    if not os.path.exists(p):
        return None, None
    txt = open(p).read()
    out = []
    for flag in ('--x0', '--x100'):
        vals = {v for v in re.findall(re.escape(flag) + r'[= ]+([0-9.eE+-]+)', txt)}
        if len(vals) == 1:
            out.append(float(next(iter(vals))))
        else:
            if len(vals) > 1:
                notes.append(f'⚠ run_mpm.sh 에 {flag} 값이 여러 개({sorted(vals)}) — 모호해 채택 안 함')
            out.append(None)
    return out[0], out[1]


def build_electrochem(kit, kit_dir, out_dir, notes):
    mi = kit['mpm_input'] or {}
    d = {k: None for k in ('i0_A_m2', 'alpha_a', 'alpha_c', 'D_s_m2_s', 'c_max_mol_m3',
                           'x0', 'x100', 'asr_film_ohm_m2', 'r_int_ohm_cm2', 'T_C', 'ocp_csv')}
    prov = {'analysis_pack': None, 'source': {}, 'reason': {}, 'notes': []}
    ocp_p, par_p = _find_analysis_pack(kit_dir)
    copied = None
    if ocp_p:
        copied = os.path.basename(ocp_p)
        shutil.copy2(ocp_p, os.path.join(out_dir, copied))
        d['ocp_csv'] = copied
        prov['source']['ocp_csv'] = os.path.relpath(ocp_p, kit_dir)
        kit['inputs'][os.path.relpath(ocp_p, kit_dir)] = ocp_p        # 읽은 입력 → provenance md5
    else:
        prov['reason']['ocp_csv'] = 'ocp_*.csv 없음 — GPU 박스에서 step4_pybamm_anchor --export-params 로 생성'
    if par_p:
        pj = _load_json(par_p)
        prov['analysis_pack'] = {'params_json': os.path.relpath(par_p, kit_dir),
                                 'provenance': pj.get('provenance')}
        kit['inputs'][os.path.relpath(par_p, kit_dir)] = par_p        # 읽은 입력 → provenance md5
        for field, key in (('c_max_mol_m3', 'c_max_mol_m3'), ('x0', 'x_at_charged'),
                           ('x100', 'x_at_discharged')):
            if pj.get(key) is not None:
                d[field] = float(pj[key])
                prov['source'][field] = f'{os.path.basename(par_p)}:{key}'
    else:
        for f2 in ('c_max_mol_m3', 'x0', 'x100'):
            prov['reason'][f2] = 'params_*.json 없음 (analysis pack 부재)'
    # 킷이 실제 실행하는 stoich 창 (run_mpm.sh 가 --x100 0.9084 를 굽는다) — params json 을 덮는 정본
    x0_rs, x100_rs = _x_window_from_run_script(kit_dir, notes)
    if x0_rs is not None:
        d['x0'] = x0_rs; prov['source']['x0'] = 'run_mpm.sh --x0 (킷 실행창 override)'
    if x100_rs is not None:
        d['x100'] = x100_rs; prov['source']['x100'] = 'run_mpm.sh --x100 (킷 실행창 override)'
    # collector 직렬 R_int — 킷 명시값만 (None = 전극-내부 R_int=0 규약, 날조 금지)
    if mi.get('step4_r_int_ohm_cm2') is not None:
        d['r_int_ohm_cm2'] = float(mi['step4_r_int_ohm_cm2'])
        prov['source']['r_int_ohm_cm2'] = 'mpm_input.json step4_r_int_ohm_cm2 (rint_eis_anchors 선택값)'
    else:
        prov['reason']['r_int_ohm_cm2'] = '킷 미지정 — 전극-내부 R_int=0 규약 (직렬항 없음)'
    # D_s: 킷이 명시한 경우만 (mono_scalar 단일값).  bimodal 분리는 단일 필드에 못 넣는다 —
    # 임의로 한쪽을 고르면 §F1 위반 → null + provenance 에 분리 dict 통째로.
    es = mi.get('step4_am_electro_split')
    if isinstance(es, dict):
        if es.get('mode') == 'mono_scalar' and es.get('d_s') is not None:
            d['D_s_m2_s'] = float(es['d_s'])
            prov['source']['D_s_m2_s'] = f"mpm_input step4_am_electro_split mono_scalar (class={es.get('class')})"
        else:
            prov['reason']['D_s_m2_s'] = ('bimodal poly/SC 분리 — 단일 D_s 필드에 넣지 않음 '
                                          '(어느 쪽인지 임의 선택 금지); 분리값은 provenance 참조')
            prov['step4_am_electro_split'] = es
    else:
        prov['reason']['D_s_m2_s'] = ('킷 명시값 없음 — step4_dyn 기본 3e-14 (Kang&Shin 2025 FEM 체인값, '
                                      '측정 아님)는 §F1 상 여기 못 적음; COMSOL 에서 명시 선택할 것')
    # i0/α/ASR: analysis pack 에 없음 → null + 규약 안내만 (step4_dyn v1 은 i0=2 A/m² 훅,
    # α=0.5/0.5 대칭 BV, ASR=0 — 훅/규약이지 앵커가 아니라서 값 필드에 적지 않는다)
    prov['reason']['i0_A_m2'] = 'i0 앵커 부재 (step4_dyn v1 훅 2 A/m² = 훅, 측정 아님 — §F1 null)'
    prov['reason']['alpha_a'] = prov['reason']['alpha_c'] = \
        'α 명시 없음 (step4_dyn 규약 = 0.5/0.5 대칭 BV — 규약이지 측정 아님)'
    prov['reason']['asr_film_ohm_m2'] = 'ASR_film 앵커 부재 (step4_dyn 기본 0)'
    # T_C: 온도 주입 킷이면 그 값, 아니면 σ 테이블 선언온도(25 °C 규약, se_material.T_REF_C)
    tp = mi.get('temperature_provenance') or ((kit['payload'] or {}).get('temperature_provenance'))
    if isinstance(tp, dict) and tp.get('T_C') is not None:
        d['T_C'] = float(tp['T_C'])
        prov['source']['T_C'] = 'temperature_provenance (킷 운전온도 주입)'
    else:
        d['T_C'] = float(se_material.T_REF_C)
        prov['source']['T_C'] = ('se_material.T_REF_C 선언온도 — 운전온도 미주입 킷의 σ 는 25 °C 규약값 '
                                 '(측정 조건 아님)')
    d['provenance'] = prov
    return d, copied


# ─────────────────────────── conventions.md ───────────────────────────

def write_conventions(out, case):
    txt = f"""# comsol_pkg 규약 (schema v{SCHEMA_VERSION}) — {case}

## 1. 단위표 (S/cm ↔ S/m)

| 항목 | 패키지 단위 | COMSOL SI | 환산 |
|---|---|---|---|
| σ_e (am_spheres.sigma_e_S_cm), σ_bulk_ion, κ_dom_S_cm | S/cm | S/m | ×100 (1 S/cm = 100 S/m) |
| κ_dom_S_m (병기) | S/m | S/m | 그대로 |
| g_holm_S (am_am_contacts) | S | S | 절대 컨덕턴스 — 환산 불필요 |
| 좌표·반지름·a_hertz·delta | µm | m | ×1e-6 |

Holm 식 g = 2·σ_c[S/cm]·(a_um·1e-4 cm) 는 cm 기반 — SI 로 다시 쓰면 g = 2·σ_c[S/m]·a[m]
(같은 수).  검산: σ_c = 1 S/cm, a = 1 µm → g = 2e-4 S.

## 2. τ 관례 — 선형 (√ 함정 주의)

이 패키지의 τ 는 전부 **선형** 관례다:

    sigma_eff = sigma_bulk · phi / tau   ⇒   tau = phi · sigma_bulk / sigma_eff

수치 예: φ = 0.5, σ_bulk = 1, σ_eff = 0.125 → 선형 τ = 0.5·1/0.125 = **4**.
같은 해를 √ 관례(σ_eff = σ_bulk·φ/τ², build_tau_regime_db 의 규약)로 읽으면 τ = √4 = **2**.
**같은 물리가 τ = 4 ↔ 2 로 갈린다** — COMSOL Effective transport parameter 에 넣기 전에
그 인터페이스의 τ 정의(1승/2승)를 반드시 확인할 것.

κ_dom 이중계상 가드: 하이브리드 모델은 AM 구를 기하로 해상하므로 AM-장애물 굴곡도는 모델이
스스로 만든다.  κ_dom/σ_bulk = (φ_full/τ_full)/(φ_geo/τ_geo) = kdom_ratio 이고, φ_geo/τ_geo 는
"AM 여집합을 꽉 찬 SE 로 이상화"한 같은 복셀 Laplace 해다.  kdom_ratio > 1 이면 규약 불일치
경고 (manifest.notes 확인).

## 3. single-ion 경고 (LPSCl t⁺ ≈ 1)

LPSCl 은 single-ion conductor (t⁺ ≈ 1) → **전해질 농도구배·농도분극이 물리적으로 없다.**
COMSOL 의 일반 리튬이온 배터리(DFN, tertiary current distribution, concentrated electrolyte)
인터페이스를 쓰면 **가짜 확산분극**이 생긴다 — 전류분포(Primary/Secondary Current
Distribution) 인터페이스 + 이 패키지의 κ_dom 만 사용할 것.

## 4. a_s 밴드 — Hertz(탄성 하한) / Tabor(소성 상한)

am_am_contacts 의 a_hertz 는 DEM δ 의 **탄성 Hertz** 접촉반경 (a = √(R*·δ)).  NCM 140 GPa ≫
SE 1.35 GPa 라 AM-AM 접촉의 소성은 미미 → Hertz 하한이 물리값에 가깝다.  Stage-E
(Tabor F/H + volume V/h) 소성-면적은 상한 밴드 — TODO(trackb): network_conductivity physics
모드 연결 옵션 (v1.0 계약은 Hertz 단일).  coverage 거리 밴드 규약: Hertz 0.13 µm /
Tabor 0.26 µm (payload coverage_* 키).

## 5. 파라미터는 제작압 P 에 갇힘 (+ porosity 관례)

이 패키지의 기하·접촉·σ·coverage 는 전부 **제작압**(예: 300 MPa) 압밀 상태의 값이다.
구동 스택압이 다르면(예: 90 MPa) 접촉/기공이 달라진다 — P 를 바꾼 예측에 재사용 금지,
해당 P 로 STEP1/2 를 재실행한 킷에서 재-export 할 것 (mpm_input.json 의
a1_pressure_provenance 확인).  porosity 관례: **mpm = union / dem = eps_sphere** — 관례가
다른 porosity 를 한 표에서 짝지어 비교 금지 (se_domain.porosity_convention 이 라벨).

## 6. I_1C 규약 — TODO

TODO(trackb): I_1C(면적용량 × rate → 전류) 규약 문서화 미결 — x100 창을 넓히면 I_1C 재계산
(전류 ~9%↑) 이슈 포함 (docs/step4_assb_window_review.md).  COMSOL 갈바노 BC 의 전류값은
이 규약 확정 후 electrochem.json 에 추가된다.
"""
    p = os.path.join(out, 'conventions.md')
    with open(p, 'w') as f:
        f.write(txt)
    return p


# ─────────────────────────── export 본체 ───────────────────────────

def export(kit_dir, out_dir):
    kit = load_kit(kit_dir)
    os.makedirs(out_dir, exist_ok=True)
    notes = []
    case = (kit['mpm_input'] or {}).get('case') or os.path.basename(os.path.normpath(kit_dir))
    trackb, tb_src = find_trackb(kit)
    if tb_src:
        notes.append(f'trackb 출처: {tb_src}')

    am_rows, cov_src = build_am_rows(kit, trackb, notes)
    files = [os.path.basename(write_am_spheres(out_dir, am_rows))]
    contacts = build_contacts(kit)
    files.append(os.path.basename(write_contacts(out_dir, contacts)))
    vp, n_fib = write_vgcf(out_dir, kit, notes)
    files.append(os.path.basename(vp))

    se = build_se_domain(kit, trackb, notes)
    with open(os.path.join(out_dir, 'se_domain.json'), 'w') as f:
        json.dump(se, f, indent=2, ensure_ascii=False)
    files.append('se_domain.json')

    ec, ocp_copied = build_electrochem(kit, kit_dir, out_dir, notes)
    with open(os.path.join(out_dir, 'electrochem.json'), 'w') as f:
        json.dump(ec, f, indent=2, ensure_ascii=False)
    files.append('electrochem.json')
    if ocp_copied:
        files.append(ocp_copied)

    files.append(os.path.basename(write_conventions(out_dir, case)))

    commit = _git_commit()
    prov = {'case': case, 'git_commit': commit,
            'inputs': {name: _md5(p) for name, p in sorted(kit['inputs'].items())},
            'created_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'generator': 'comsol_export.py'}
    with open(os.path.join(out_dir, 'provenance.json'), 'w') as f:
        json.dump(prov, f, indent=2, ensure_ascii=False)
    files.append('provenance.json')

    # source: MPM 산출물(metrics/payload)이 있으면 mpm, 스캐폴드-only 킷이면 dem_stageE
    source = 'mpm' if (kit['metrics'] is not None or kit['payload'] is not None) else 'dem_stageE'
    manifest = {'schema_version': SCHEMA_VERSION, 'case': case, 'source': source,
                'tau_convention': TAU_CONVENTION, 'files': files + ['manifest.json'],
                'git_commit': commit, 'notes': notes}
    with open(os.path.join(out_dir, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return {'case': case, 'source': source, 'n_spheres': len(am_rows),
            'n_contacts': len(contacts), 'n_fibres': n_fib, 'cov_source': cov_src,
            'kappa_dom_S_cm': se['kappa_dom_S_cm'], 'out': out_dir, 'notes': notes}


# ─────────────────────────── selftest ───────────────────────────

def _write_scaffold_lu(path, rows):
    with open(path, 'w', newline='') as f:
        f.write('# type,x,y,z,r  # LIGGGHTS box units — selftest 합성 킷\n')
        w = csv.writer(f)
        for r in rows:
            w.writerow(r)


def _read_pkg_csv(path):
    with open(path) as f:
        lines = [ln for ln in f if not ln.startswith('#')]
    return list(csv.DictReader(lines))


def _selftest():
    import math
    import tempfile
    n_ok, n_bad = [0], [0]

    def chk(name, cond, extra=''):
        (n_ok if cond else n_bad)[0] += 1
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f'  ({extra})' if extra and not cond else ''))

    with tempfile.TemporaryDirectory() as td:
        # ── 킷 A: LU 스캐폴드 4개 (P-P 겹침 δ=0.5µm 알려짐) + trackb metrics + payload 섬유 + anchor ──
        kitA = os.path.join(td, 'kitA'); os.makedirs(kitA)
        _write_scaffold_lu(os.path.join(kitA, 'am_scaffold.csv'), [
            [1, 0.010, 0.010, 0.0060, 0.006],               # P1 (µm: 10,10,6  r6)
            [1, 0.010, 0.010, 0.0175, 0.006],               # P2 — d=11.5, δ=0.5, R*=3, a=√1.5
            [2, 0.030, 0.030, 0.0020, 0.002],               # S3 (비접촉)
            [2, 0.040, 0.040, 0.0020, 0.002]])              # S4 (비접촉)
        _write_scaffold_lu(os.path.join(kitA, 'se_scaffold.csv'), [[3, 0.02, 0.02, 0.004, 0.0005]])
        ppA = {'f_reaction': [0.5, 0.4, 0.3, 0.2], 'f_carbon': [0.1, 0.1, 0.0, 0.0],
               'f_block': [0.0, 0.05, 0.0, 0.0], 'f_void': [0.4, 0.45, 0.7, 0.8]}
        tbA = {'kdom_ratio': 0.25, 'tau_full': 4.0, 'tau_geo': 2.0, 'phi_full': 0.3,
               'phi_geo': 0.6, 'sigma_bulk_ion_S_cm': 0.003, 'per_particle': ppA}
        json.dump({'porosity_mpm_pct': 15.9, 'thickness_mpm_um': 30.0,
                   'step3': {'sigma_e_eff_S_cm': 2.0, 'trackb': tbA}},
                  open(os.path.join(kitA, 'mpm_metrics.json'), 'w'))
        json.dump({'box': {'x_min': 0, 'x_max': 50.0, 'y_min': 0, 'y_max': 50.0,
                           'z_min': 0, 'z_max': 30.0},
                   'additive_fibres': [
                       {'phase': ADD_PHASE['VGCF'], 'pts': [[1.0, 1.0, 1.0], [3.0, 1.0, 1.0], [5.0, 1.0, 1.0]]},
                       {'phase': ADD_PHASE['PTFE'], 'pts': [[0.0, 2.0, 0.0], [1.0, 2.0, 0.0]]}],
                   'mpm_metrics': {'porosity_mpm_pct': 15.9}},
                  open(os.path.join(kitA, 'mpm_payload.json'), 'w'))
        json.dump({'case': 'synthetic_a', 'lateral_box': 0.05, 'step4_r_int_ohm_cm2': 30.0},
                  open(os.path.join(kitA, 'mpm_input.json'), 'w'))
        ancA = os.path.join(kitA, 'anchor_params'); os.makedirs(ancA)
        with open(os.path.join(ancA, 'ocp_nmc811_chen2020.csv'), 'w') as f:
            f.write('x_stoich,U_V\n0.3,4.1\n0.6,3.8\n0.9,3.4\n')
        json.dump({'c_max_mol_m3': 63104.0, 'x_at_charged': 0.2638, 'x_at_discharged': 0.9084,
                   'provenance': 'selftest synthetic'},
                  open(os.path.join(ancA, 'params_nmc811_chen2020.json'), 'w'))

        outA = os.path.join(td, 'pkgA')
        resA = export(kitA, outA)

        need = ['manifest.json', 'am_spheres.csv', 'am_am_contacts.csv', 'vgcf_fibres.csv',
                'se_domain.json', 'electrochem.json', 'conventions.md', 'provenance.json',
                'ocp_nmc811_chen2020.csv']
        chk('파일 전부 존재', all(os.path.exists(os.path.join(outA, f)) for f in need),
            str([f for f in need if not os.path.exists(os.path.join(outA, f))]))
        man = json.load(open(os.path.join(outA, 'manifest.json')))
        chk("manifest schema_version == '1.0'", man['schema_version'] == '1.0')
        chk("manifest source == 'mpm' (metrics 있는 킷)", man['source'] == 'mpm')
        chk('manifest tau_convention (선형)', man['tau_convention'] == TAU_CONVENTION)

        sph = _read_pkg_csv(os.path.join(outA, 'am_spheres.csv'))
        chk('스피어 수 4', len(sph) == 4, f'got {len(sph)}')
        chk('LU→µm ×1000 (P1 r=6µm, z=6µm)',
            abs(float(sph[0]['r_um']) - 6.0) < 1e-9 and abs(float(sph[0]['z_um']) - 6.0) < 1e-9)
        chk('cls/σ_e 배정 (type1→AM_P 0.005 / type2→AM_S 0.010)',
            sph[0]['cls'] == 'AM_P' and abs(float(sph[0]['sigma_e_S_cm']) - SIGMA_DEFAULT['AM_P']) < 1e-12
            and sph[2]['cls'] == 'AM_S' and abs(float(sph[2]['sigma_e_S_cm']) - SIGMA_DEFAULT['AM_S']) < 1e-12)
        chk('facewalk per-particle coverage (행별 값+라벨)',
            all(s['f_cov_source'] == 'mpm_facewalk' for s in sph)
            and abs(float(sph[0]['f_cov_reaction']) - 0.5) < 1e-9
            and abs(float(sph[1]['f_cov_block']) - 0.05) < 1e-9)

        con = _read_pkg_csv(os.path.join(outA, 'am_am_contacts.csv'))
        chk('접촉 1쌍 (P1-P2)', len(con) == 1 and con[0]['i'] == '0' and con[0]['j'] == '1',
            f'got {len(con)}')
        a_hand = math.sqrt((6.0 * 6.0 / 12.0) * 0.5)        # R*=3, δ=0.5 → a=√1.5 손계산
        chk('a_hertz = √(R*·δ) 손계산 1e-9 일치',
            abs(float(con[0]['a_hertz_um']) - a_hand) < 1e-9,
            f"{con[0]['a_hertz_um']} vs {a_hand}")
        g_hand = 2.0 * SIGMA_DEFAULT['AM_P'] * (a_hand * 1e-4)   # P-P: σ_c = σ_P
        chk('g_holm 행 일치 (P-P σ_c=σ_P)', abs(float(con[0]['g_holm_S']) - g_hand) < 1e-15)
        chk('g_holm 단위 (σ=1 S/cm, a=1µm → 2e-4 S)',
            abs(holm_conductance_S(1.0, 1.0) - 2e-4) < 1e-18)

        sed = json.load(open(os.path.join(outA, 'se_domain.json')))
        chk('κ_dom = kdom_ratio × σ_bulk', abs(sed['kappa_dom_S_cm'] - 0.25 * 0.003) < 1e-15)
        chk('S/m = 100 × S/cm', abs(sed['kappa_dom_S_m'] - 100.0 * sed['kappa_dom_S_cm']) < 1e-15)
        chk('se_domain source/관례 (mpm + union + 선형 τ)',
            sed['source'] == 'mpm' and sed['porosity_convention'] == 'union'
            and sed['tau_convention'] == TAU_CONVENTION and abs(sed['porosity_pct'] - 15.9) < 1e-9)
        chk('box/thickness (payload box 50×50×30 µm)',
            abs(sed['thickness_um'] - 30.0) < 1e-9 and abs(sed['box_um'][0] - 50.0) < 1e-9)

        ecj = json.load(open(os.path.join(outA, 'electrochem.json')))
        chk('electrochem: analysis pack 채움 (c_max/x0/x100/ocp 복사)',
            abs(ecj['c_max_mol_m3'] - 63104.0) < 1e-9 and abs(ecj['x0'] - 0.2638) < 1e-12
            and abs(ecj['x100'] - 0.9084) < 1e-12 and ecj['ocp_csv'] == 'ocp_nmc811_chen2020.csv')
        chk('electrochem: r_int 킷값 / i0 는 §F1 null+reason',
            abs(ecj['r_int_ohm_cm2'] - 30.0) < 1e-12 and ecj['i0_A_m2'] is None
            and bool(ecj['provenance']['reason'].get('i0_A_m2')))
        chk('electrochem: T_C = 25 규약 (미주입 킷)', abs(ecj['T_C'] - 25.0) < 1e-9)

        fib = _read_pkg_csv(os.path.join(outA, 'vgcf_fibres.csv'))
        chk('VGCF 폴리라인 3점 / PTFE(기하 금지) 제외',
            len(fib) == 3 and all(r['fibre_id'] == '0' for r in fib)
            and abs(float(fib[2]['x_um']) - 5.0) < 1e-12, f'got {len(fib)}')

        prv = json.load(open(os.path.join(outA, 'provenance.json')))
        chk('provenance inputs md5 (am_scaffold 포함)',
            'am_scaffold.csv' in prv['inputs'] and len(prv['inputs']['am_scaffold.csv']) == 32
            and prv['generator'] == 'comsol_export.py')
        conv = open(os.path.join(outA, 'conventions.md')).read()
        chk('conventions.md 6개 절 실제 본문 (τ=4↔2 · DFN 가짜 확산분극 포함)',
            all(s in conv for s in ('## 1.', '## 2.', '## 3.', '## 4.', '## 5.', '## 6.'))
            and 'τ = 4 ↔ 2' in conv.replace('**', '')
            and '가짜 확산분극' in conv and '0.125' in conv)
        chk('provenance: 읽은 analysis pack 도 md5 (ocp+params)',
            any(k.endswith('ocp_nmc811_chen2020.csv') for k in prv['inputs'])
            and any(k.endswith('params_nmc811_chen2020.json') for k in prv['inputs']))

        # ── 킷 B: trackb/metrics/payload 없음 → class_mean_fallback + se_domain null+reason ──
        kitB = os.path.join(td, 'kitB'); os.makedirs(kitB)
        _write_scaffold_lu(os.path.join(kitB, 'am_scaffold.csv'), [
            [1, 0.010, 0.010, 0.0060, 0.006], [2, 0.030, 0.030, 0.0020, 0.002]])
        json.dump({'case': 'synthetic_b', 'lateral_box': 0.05, 'dem_porosity_pct': 15.6,
                   'dem_thickness_um': 30.28, 'dem_coverage_AM_P_mean': 48.3,
                   'dem_coverage_AM_S_mean': 51.8},
                  open(os.path.join(kitB, 'mpm_input.json'), 'w'))
        outB = os.path.join(td, 'pkgB')
        resB = export(kitB, outB)
        manB = json.load(open(os.path.join(outB, 'manifest.json')))
        sphB = _read_pkg_csv(os.path.join(outB, 'am_spheres.csv'))
        sedB = json.load(open(os.path.join(outB, 'se_domain.json')))
        chk('trackb 없는 킷: class_mean_fallback (DEM 평균 48.3% → 0.483)',
            all(s['f_cov_source'] == 'class_mean_fallback' for s in sphB)
            and abs(float(sphB[0]['f_cov_reaction']) - 0.483) < 1e-9
            and abs(float(sphB[1]['f_cov_reaction']) - 0.518) < 1e-9)
        chk('trackb 없는 킷: se_domain null + reason + dem_stageE',
            sedB['kappa_dom_S_cm'] is None and sedB['kdom_ratio'] is None
            and sedB['source'] == 'dem_stageE' and bool(sedB['reason']))
        chk('trackb 없는 킷: porosity = DEM eps_sphere 관례',
            abs(sedB['porosity_pct'] - 15.6) < 1e-9 and sedB['porosity_convention'] == 'eps_sphere')
        chk("manifest source == 'dem_stageE' + VGCF 부재 note",
            manB['source'] == 'dem_stageE' and any('--save-fibre' in n for n in manB['notes']))
        chk('B: 접촉 0쌍 / 헤더만 vgcf', resB['n_contacts'] == 0 and resB['n_fibres'] == 0)

        # ── 킷 C: per_particle 길이 3 ≠ 스피어 4 → SystemExit (조용한 재배열 금지) ──
        kitC = os.path.join(td, 'kitC'); os.makedirs(kitC)
        shutil.copy2(os.path.join(kitA, 'am_scaffold.csv'), os.path.join(kitC, 'am_scaffold.csv'))
        tbC = dict(tbA); tbC['per_particle'] = {k: v[:3] for k, v in ppA.items()}
        json.dump({'step3': {'trackb': tbC}}, open(os.path.join(kitC, 'mpm_metrics.json'), 'w'))
        try:
            export(kitC, os.path.join(td, 'pkgC'))
            chk('per_particle 길이 불일치 → SystemExit', False, '에러 없이 통과함')
        except SystemExit as e:
            chk('per_particle 길이 불일치 → SystemExit', '재배열 금지' in str(e), str(e))

    print(f'\nselftest: {n_ok[0]} PASS / {n_bad[0]} FAIL')
    return 0 if n_bad[0] == 0 else 1


# ─────────────────────────── CLI ───────────────────────────

def main():
    ap = argparse.ArgumentParser(description='킷 → comsol_pkg (스키마 v1.0) 익스포터')
    ap.add_argument('--kit', help='킷 디렉터리 (am_scaffold.csv 필수; se_scaffold/mpm_input/'
                                  'mpm_metrics/mpm_payload 는 있는 것 사용)')
    ap.add_argument('--out', help='출력 디렉터리 (= comsol_pkg_<case> 로 이름 짓기를 권장)')
    ap.add_argument('--selftest', action='store_true', help='합성 킷 왕복 검증')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(_selftest())
    if not a.kit or not a.out:
        ap.error('--kit 과 --out 필요 (또는 --selftest)')
    r = export(a.kit, a.out)
    print(f"comsol_pkg 작성 완료 → {r['out']}")
    print(f"  case {r['case']} · source {r['source']} · 스피어 {r['n_spheres']} · "
          f"접촉 {r['n_contacts']} · VGCF 섬유 {r['n_fibres']} · coverage={r['cov_source']}")
    if r['kappa_dom_S_cm'] is not None:
        print(f"  κ_dom = {r['kappa_dom_S_cm']:.6g} S/cm ({r['kappa_dom_S_cm'] * 100.0:.6g} S/m)")
    for n in r['notes']:
        print(f'  note: {n}')


if __name__ == '__main__':
    main()
