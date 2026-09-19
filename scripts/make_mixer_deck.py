#!/usr/bin/env python3
"""믹싱 드럼 덱 생성기 — 조성에서 치수·개수·섬유파일을 **유도**한다.

왜 생성기인가
  치수가 조성에서 유도된다 (부피분율 → 개수비 → 드럼 크기).  손으로 적으면
  조성을 바꿀 때마다 틀린다.  `docs/reviews/mixing_model_design_20260919.md` §11 의
  계산을 그대로 코드로 옮긴 것이다.

⚠⚠ 생산 압축 덱의 `scale=1000` 규약을 **쓰지 않는다**.
  그 규약은 `E_sim = E_real/scale` · `R_sim = R_real×scale` 이라 접촉력은 `scale¹`,
  중력은 `scale³` 로 스케일된다 ⇒ 중력/접촉 비가 `scale²` 만큼 틀어진다.
  압축 덱은 **플래튼 구동**이라 중력이 무시돼 무해했지만 **드럼은 중력 구동**이다.
  ⇒ 대신 문헌 방식(`lischka`·`hare`)을 쓴다: **coarse-graining(CGF) + 중력 실제값 유지**,
  점착은 무차원수 보존으로 재보정(⬜ `D11`, 지수 미측정).

⚠ 전단탄성률을 낮춘다 — `lischka` 가 *"계산비용 때문에 G=1e8 로 낮췄다, 물성이 아니다"*
  라고 명시한 것과 같은 조작이고, 튜토리얼 `Mixer` 도 `E=1e7` 을 쓴다.
  ⇒ **탄성 물성으로 인용 금지.**

usage
  python3 scripts/make_mixer_deck.py --out dem_scripts/mixer_20260919 --n-total 50000
  python3 scripts/make_mixer_deck.py --selftest
"""
import argparse
import math
import os
import sys

#: 밀도 (g/cm³) — `scripts/additives.py` 정본과 같은 값.  여기서 다시 적는 이유는
#  이 생성기가 리포 밖(1저자 WSL)에서도 단독으로 돌 수 있어야 하기 때문이다.
DENS = {'AM': 4.80, 'SE': 2.00, 'VGCF': 2.00, 'PTFE': 2.20}
#: 1저자 지시 조성 (2026-09-19) — 에너지밀도 최대 조합
WT = {'AM': 80.0, 'SE': 18.0, 'VGCF': 1.0, 'PTFE': 1.0}
PS = (7.0, 3.0)                       # P:S (wt%)
#: 실제 지름 (µm).  AM_P 12 = 생산 규약 · VGCF 0.15 · PTFE 0.25 는 `CL-66` 앵커
D_REAL_UM = {'AM_P': 12.0, 'AM_S': 4.0, 'SE': 1.0}
L_FIB_UM = 10.0                       # ⚠ VGCF 길이.  PTFE 길이는 출처 없음 (`CL-67`)


def volume_fractions():
    wt = {'AM_P': WT['AM'] * PS[0] / sum(PS), 'AM_S': WT['AM'] * PS[1] / sum(PS),
          'SE': WT['SE'], 'VGCF': WT['VGCF'], 'PTFE': WT['PTFE']}
    rho = {'AM_P': DENS['AM'], 'AM_S': DENS['AM'], 'SE': DENS['SE'],
           'VGCF': DENS['VGCF'], 'PTFE': DENS['PTFE']}
    v = {k: wt[k] / rho[k] for k in wt}
    tot = sum(v.values())
    return {k: v[k] / tot for k in v}, wt


def plan(n_total, d_se_over_am=0.25, d_fib_over_am=0.25, cgf=200.0,
         fill=0.30, pack=0.60, drum_r_over_l=2.5, shear_mod=3.85e6, nu=0.25):
    """조성 → 개수 · 드럼 치수 · 시간스텝.  **순수 함수**라 시험 가능하다."""
    phi, wt = volume_fractions()
    dP = D_REAL_UM['AM_P'] * 1e-6 * cgf                      # m
    d = {'AM_P': dP, 'AM_S': dP / 3.0, 'SE': dP * d_se_over_am,
         'VGCF': dP * d_fib_over_am, 'PTFE': dP * d_fib_over_am}
    #  ⚠⚠ LIGGGHTS `particledistribution/discrete` 는 분율을 **mass%** 로 읽는다
    #    (실행으로 확인: 로그가 "distribution based on mass%" 를 먼저 찍고 number% 를 유도한다).
    #    초판은 개수분율을 넣어 AM_P 가 744 → **6개**로 들어갔다.
    #    ⇒ 우리 조성이 이미 wt% 이므로 **그대로 넣는다**.
    #  섬유 — 구 개수는 종횡비가 정한다 (길이는 CGF 로 같이 늘어난다)
    L_fib = L_FIB_UM * 1e-6 * cgf
    nsph = max(2, int(round(L_fib / d['VGCF'])))
    NSPH = {'AM_P': 1, 'AM_S': 1, 'SE': 1, 'VGCF': nsph, 'PTFE': nsph}
    rho_i = {'AM_P': DENS['AM'], 'AM_S': DENS['AM'], 'SE': DENS['SE'],
             'VGCF': DENS['VGCF'], 'PTFE': DENS['PTFE']}
    #  템플릿 1개의 질량 (섬유는 구 nsph 개)
    #  ★ 섬유는 구가 겹쳐 있어 nsph 개 합보다 가볍다 — 기하로 보정한다 (실측 +3.8 % 편향 제거)
    fac = {k: (chain_volume_factor(NSPH[k]) if NSPH[k] > 1 else 1.0) for k in d}
    m_tpl = {k: NSPH[k] * fac[k] * rho_i[k] * 1000.0 * (math.pi / 6) * d[k] ** 3 for k in d}
    massfrac = {k: wt[k] / 100.0 for k in wt}
    #  템플릿 개수비 = 질량분율 / 템플릿질량
    c = {k: massfrac[k] / m_tpl[k] for k in d}
    per = sum(c.values())
    #  `particles_in_region` 은 **템플릿** 수다.  목표는 원자 수로 준다.
    atoms_per_tpl = sum(c[k] / per * NSPH[k] for k in d)
    n_tpl_total = int(round(n_total / atoms_per_tpl))
    n_tpl = {k: int(round(n_tpl_total * c[k] / per)) for k in d}
    n = {k: n_tpl[k] * NSPH[k] for k in d}                    # 원자 수
    n_fib = {k: n_tpl[k] for k in ('VGCF', 'PTFE')}
    #  드럼 — 고체 부피에서 역산
    v_solid = n['AM_P'] * (math.pi / 6) * d['AM_P'] ** 3 / phi['AM_P']
    v_drum = v_solid / (fill * pack)
    R = (drum_r_over_l * v_drum / math.pi) ** (1 / 3.0)
    L = R / drum_r_over_l
    #  시간스텝 — Rayleigh 의 20 %, 가장 작은 입자·SE 밀도 기준
    d_small = min(d.values())
    rho_si = DENS['SE'] * 1000.0
    dt = 0.2 * math.pi * (d_small / 2) * math.sqrt(rho_si / shear_mod) \
        / (0.1631 * nu + 0.8766)
    rpm_crit = 60 / (2 * math.pi) * math.sqrt(9.81 / R)
    return dict(phi=phi, wt=wt, d=d, n=n, n_tpl=n_tpl, n_tpl_total=n_tpl_total,
                massfrac=massfrac, n_fib=n_fib, nsph=nsph, L_fib=L_fib,
                v_solid=v_solid, v_drum=v_drum, R=R, L=L, dt=dt,
                rpm_crit=rpm_crit, cgf=cgf, stl_scale=R / 0.5, n_total=sum(n.values()))


def chain_volume_factor(nsph, spacing_over_d=0.8):
    """겹친 구 사슬의 부피 / (구 부피 × nsph).

    ⚠ 이 보정이 없으면 섬유 질량을 **과대**평가해 LIGGGHTS 가 1 wt% 를 맞추려고
      가닥을 더 넣는다 (실측 +3.8 %).  등반경 렌즈 부피는 해석적이다:
        d = s·D,  δ = D − d,  V_lens = π δ²(d + 2D)/12
    """
    if nsph < 2:
        return 1.0
    D = 1.0
    d = spacing_over_d * D
    delta = D - d
    v_sph = (math.pi / 6) * D ** 3
    v_lens = math.pi * delta ** 2 * (d + 2 * D) / 12.0
    return (nsph * v_sph - (nsph - 1) * v_lens) / (nsph * v_sph)


def fibre_file(nsph, d_sph):
    """multisphere 구 파일 — `x y z radius` 한 줄씩 (튜토리얼 `stone1.multisphere` 형식).

    ⚠ 겹치게 둔다 (중심간 거리 = 0.8·d).  떨어뜨리면 강체가 아니라 염주가 된다.
    """
    step = 0.8 * d_sph
    x0 = -0.5 * step * (nsph - 1)
    return ''.join(f'{x0 + i*step:.8g} 0 0 {d_sph/2:.8g}\n' for i in range(nsph))


def deck(p, rpm, revolutions, seed=32452843):
    n, d = p['n'], p['d']
    period = 60.0 / rpm
    steps_fill = 20000
    steps_run = int(round(revolutions * period / p['dt']))
    dump_every = max(1000, steps_run // 200)
    box = p['R'] * 1.15
    return f"""# 믹싱 드럼 — 표면에너지 스윕  (생성: scripts/make_mixer_deck.py)
# ⚠ 손으로 고치지 말 것 — 치수가 조성에서 유도된다.  조성을 바꾸면 생성기를 다시 돌린다.
#
# 조성 AM:SE:VGCF:PTFE = {WT['AM']:.0f}:{WT['SE']:.0f}:{WT['VGCF']:.0f}:{WT['PTFE']:.0f} (wt%) · P:S = {PS[0]:.0f}:{PS[1]:.0f}
# CGF = {p['cgf']:.0f}  (실제 AM_P {D_REAL_UM['AM_P']:.0f} µm → 사물 {d['AM_P']*1e3:.2f} mm)
# ⛔ 생산 scale=1000 규약을 쓰지 않는다 — 드럼은 중력 구동이라 중력/접촉 비가 깨진다.
# ⚠ 전단탄성률을 계산비용 때문에 낮췄다 (lischka 와 같은 조작) — 물성으로 인용 금지.

atom_style      granular
atom_modify     map array sort 0 0
boundary        f f f
newton          off
communicate     single vel yes
units           si
processors      1 1 1            # PUBLIC 판 multisphere 는 직렬만 지원

region          reg block -{box:.6g} {box:.6g} -{box:.6g} {box:.6g} -{box:.6g} {box:.6g} units box
create_box      5 reg
neighbor        {d['VGCF']*0.5:.6g} bin
neigh_modify    delay 0

# --- 물성 (1:AM_P 2:AM_S 3:SE 4:VGCF 5:PTFE) ---
# ⚠ 영률은 계산비용용 연화값이다.  생산 압축 덱의 값(AM 140 GPa · SE 1.35 GPa)이 아니다.
fix m1 all property/global youngsModulus peratomtype 1.e7 1.e7 1.e7 1.e7 1.e7
fix m2 all property/global poissonsRatio peratomtype 0.25 0.25 0.30 0.30 0.30
fix m3 all property/global coefficientRestitution peratomtypepair 5 &
{_mat(5, 0.3)}
fix m4 all property/global coefficientFriction peratomtypepair 5 &
{_mat(5, 0.5)}
fix m5 all property/global coefficientRollingFriction peratomtypepair 5 &
{_mat(5, 0.2)}
# ★ 스윕 축 — 표면에너지 대리 (SJKR, J/m³).  팔마다 이 블록만 바꾼다.
fix mC all property/global cohesionEnergyDensity peratomtypepair 5 &
{_mat(5, 3.0e5)}
fix m9 all property/global characteristicVelocity scalar 2.0

# ⚠ cohesion 은 tangential 뒤 · rolling_friction 앞 (순서가 실재하는 제약)
pair_style      gran model hertz tangential history cohesion sjkr rolling_friction cdt
pair_coeff      * *
timestep        {p['dt']:.4g}
fix             gravi all gravity 9.81 vector 0.0 0.0 -1.0

# --- 기구 (STL 은 튜토리얼 Mixer 원본을 scale 로 줄여 쓴다) ---
fix Drum  all mesh/surface file Drum.stl  type 2 scale {p['stl_scale']:.6g}
fix Front all mesh/surface file Front.stl type 2 scale {p['stl_scale']:.6g}
fix Back  all mesh/surface file Back.stl  type 2 scale {p['stl_scale']:.6g}
fix walls all wall/gran model hertz tangential history cohesion sjkr rolling_friction cdt &
    mesh n_meshes 3 meshes Drum Front Back

# --- 입자 ---
fix pt1 all particletemplate/sphere 10487 atom_type 1 density constant {DENS['AM']*1000:.0f} radius constant {d['AM_P']/2:.6g}
fix pt2 all particletemplate/sphere 11887 atom_type 2 density constant {DENS['AM']*1000:.0f} radius constant {d['AM_S']/2:.6g}
fix pt3 all particletemplate/sphere 13901 atom_type 3 density constant {DENS['SE']*1000:.0f} radius constant {d['SE']/2:.6g}
# ★ 섬유는 multisphere 강체 사슬 — 구 하나로 접지 않는다 (sun2026: 접으면 σ_e 순위가 뒤집힌다)
# ⚠ 끝의 `type` 은 **원자 타입이 아니라 multisphere 템플릿 번호**이고 **1 부터 연속**이어야 한다
#   (실행으로 확인: ERROR: multisphere template types have to be consecutive starting from 1)
fix pt4 all particletemplate/multisphere 15101 atom_type 4 density constant {DENS['VGCF']*1000:.0f} &
    nspheres {p['nsph']} ntry 1000000 spheres file data/vgcf.multisphere scale 1.0 type 1
fix pt5 all particletemplate/multisphere 17093 atom_type 5 density constant {DENS['PTFE']*1000:.0f} &
    nspheres {p['nsph']} ntry 1000000 spheres file data/ptfe.multisphere scale 1.0 type 2

# ⚠ 분율은 **mass%** 다 (LIGGGHTS 규약 — 실행으로 확인).  우리 조성이 wt% 라 그대로 넣는다.
fix pdd all particledistribution/discrete 32452867 5 &
    pt1 {p['massfrac']['AM_P']:.6f} pt2 {p['massfrac']['AM_S']:.6f} pt3 {p['massfrac']['SE']:.6f} &
    pt4 {p['massfrac']['VGCF']:.6f} pt5 {p['massfrac']['PTFE']:.6f}

region ins_reg cylinder x 0.0 0.0 {p['R']*0.9:.6g} -{p['L']*0.45:.6g} {p['L']*0.45:.6g} units box
fix ins all insert/pack seed {seed} distributiontemplate pdd &
    maxattempt 200 insert_every once overlapcheck yes all_in yes vel constant 0. 0. -0.2 &
    region ins_reg particles_in_region {p['n_tpl_total']} ntry_mc 20000   # 템플릿 수 (섬유 1가닥 = 1)

fix integr all multisphere        # multisphere 가 있으면 nve/sphere 대신 이것

compute rke all erotate/sphere
thermo_style custom step atoms ke c_rke vol
thermo 5000
thermo_modify lost ignore norm no

shell mkdir post
run 1
dump dmp all custom {dump_every} post/mix_*.liggghts id type mol x y z vx vy vz fx fy fz radius

# ① 채우고 정착 — ⚠ KE 가 떨어진 뒤에 회전을 시작한다 (정착 전에 돌리면 지표가 뒤집힌다)
run {steps_fill}
unfix ins
run {steps_fill}

# ② 회전 {revolutions} 바퀴 @ {rpm:.0f} rpm  (임계 {p['rpm_crit']:.0f} rpm · Fr {(2*math.pi/period)**2*p['R']/9.81:.3f})
fix mvD all move/mesh mesh Drum  rotate origin 0 0 0 axis 1. 0. 0. period {period:.6g}
fix mvF all move/mesh mesh Front rotate origin 0 0 0 axis 1. 0. 0. period {period:.6g}
fix mvB all move/mesh mesh Back  rotate origin 0 0 0 axis 1. 0. 0. period {period:.6g}
run {steps_run}
"""


def _mat(n, val):
    """peratomtypepair n×n 행렬 — 전부 같은 값 (팔에서 이 블록만 바꾼다)."""
    rows = []
    for i in range(n):
        rows.append('    ' + ' '.join(f'{val:g}' for _ in range(n)))
    return ' &\n'.join(rows)


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    phi, wt = volume_fractions()
    chk('① 부피분율 합 = 1', abs(sum(phi.values()) - 1) < 1e-12)
    chk('② wt 합 = 100', abs(sum(wt.values()) - 100) < 1e-9)
    chk('③ AM_P:AM_S wt 비 = 7:3', abs(wt['AM_P'] / wt['AM_S'] - 7 / 3) < 1e-9)
    p = plan(50000)
    chk(f'④ 개수 합이 목표에 맞는다 ({p["n_total"]})', abs(p['n_total'] - 50000) / 50000 < 0.01)
    chk('⑤ SE 가 개수로 최다', max(p['n'], key=p['n'].get) == 'SE')
    #  ★ 변이 대조 — CGF 를 2배 하면 드럼 반경이 2배여야 한다 (부피 ∝ d³ · 개수 고정)
    p2 = plan(50000, cgf=400.0)
    chk('⑥ 변이: CGF ×2 → 드럼 R ×2', abs(p2['R'] / p['R'] - 2) < 0.02)
    chk('⑦ 변이: CGF ×2 → dt ×2', abs(p2['dt'] / p['dt'] - 2) < 0.02)
    #  ★ 섬유 파일 — 강체가 되도록 겹쳐야 한다
    txt = fibre_file(5, 1e-3)
    xs = [float(l.split()[0]) for l in txt.strip().split('\n')]
    gap = xs[1] - xs[0]
    chk('⑧ 섬유 구가 겹친다 (중심간 < 지름)', gap < 1e-3)
    chk('⑨ 섬유가 원점 대칭', abs(xs[0] + xs[-1]) < 1e-12)
    dk = deck(p, rpm=60, revolutions=5)
    chk('⑩ 덱에 cohesion 이 tangential 뒤·rolling 앞',
        'tangential history cohesion sjkr rolling_friction' in dk)
    chk('⑪ multisphere 적분기를 쓴다', 'fix integr all multisphere' in dk)
    chk('⑫ 생산 scale=1000 규약을 안 쓴다', 'scale 1000' not in dk)
    #  ★ 실행으로 배운 제약 — multisphere 템플릿 번호는 1 부터 연속이어야 한다
    import re as _re
    _t = [int(m) for m in _re.findall(r'\.multisphere scale [\d.]+ type (\d+)', dk)]
    chk(f'⑬ multisphere 템플릿 번호가 1 부터 연속 ({_t})',
        _t == list(range(1, len(_t) + 1)))
    #  변이 대조 — atom_type 은 그대로 4·5 여야 한다 (둘을 헷갈리면 상이 섞인다)
    #  ★ 겹침 보정 — 3구 사슬은 구 3개 합의 약 0.963 배여야 한다 (해석값)
    f3 = chain_volume_factor(3)
    chk(f'⑮ 3구 사슬 부피계수 {f3:.4f} ≈ 0.9627 (해석)', abs(f3 - 0.9627) < 5e-3)
    chk('⑯ 변이: nsph=1 이면 보정 없음', chain_volume_factor(1) == 1.0)
    chk('⑰ 변이: 사슬이 길수록 계수가 준다', chain_volume_factor(5) < f3)
    chk('⑭ 변이: atom_type 은 4·5 로 남아 있다',
        'atom_type 4' in dk and 'atom_type 5' in dk)
    print(f'\nmake_mixer_deck selftest: {ok}/{ok+len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='', help='덱을 쓸 디렉터리')
    ap.add_argument('--n-total', type=int, default=50000)
    ap.add_argument('--cgf', type=float, default=200.0)
    ap.add_argument('--rpm', type=float, default=60.0)
    ap.add_argument('--revolutions', type=int, default=5)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    p = plan(a.n_total, cgf=a.cgf)
    print(f'조성 → 개수 (N={p["n_total"]:,})')
    for k in ('AM_P', 'AM_S', 'SE', 'VGCF', 'PTFE'):
        print(f'   {k:5s} φ {p["phi"][k]:.4f} · d {p["d"][k]*1e3:6.3f} mm · n {p["n"][k]:8,d}'
              + (f'  ({p["n_fib"][k]:,} 가닥 × {p["nsph"]} 구)' if k in p['n_fib'] else ''))
    print(f'\n드럼  R {p["R"]*1e3:.1f} mm (지름 {2*p["R"]*1e3:.0f} mm) · L {p["L"]*1e3:.1f} mm'
          f' · 부피 {p["v_drum"]*1e6:.0f} mL · STL scale {p["stl_scale"]:.4f}')
    print(f'시간  dt {p["dt"]:.3g} s · 임계 {p["rpm_crit"]:.0f} rpm'
          f' · {a.rpm:.0f} rpm 에서 Fr {(2*math.pi*a.rpm/60)**2*p["R"]/9.81:.3f}')
    steps = int(round(a.revolutions * (60/a.rpm) / p['dt']))
    print(f'비용  {a.revolutions} 바퀴 = {steps:,} step · 직렬 추정 '
          f'{p["n_total"]*steps/2.99e6/3600:.1f} h  (실측 처리율 2.99e6 p·step/s)')
    if a.out:
        os.makedirs(os.path.join(a.out, 'data'), exist_ok=True)
        with open(os.path.join(a.out, 'data', 'vgcf.multisphere'), 'w') as f:
            f.write(fibre_file(p['nsph'], p['d']['VGCF']))
        with open(os.path.join(a.out, 'data', 'ptfe.multisphere'), 'w') as f:
            f.write(fibre_file(p['nsph'], p['d']['PTFE']))
        with open(os.path.join(a.out, 'in.mixer'), 'w') as f:
            f.write(deck(p, a.rpm, a.revolutions))
        print(f'\n→ {a.out}/in.mixer  +  data/{{vgcf,ptfe}}.multisphere')
        print('⬜ STL 3개(Drum·Front·Back)를 같은 디렉터리에 두어야 한다')
