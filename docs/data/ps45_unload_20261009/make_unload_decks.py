#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 언로딩 키트 K2 — 덱 생성기 (다섯 침대 · 모든 팔 · 10:0 이완 연장).  덱을 손으로 고치지 말 것.

    python3 make_unload_decks.py             # decks/ 다시 쓰기 + SHA256SUMS (seal_kit.py)
    python3 make_unload_decks.py --check     # 커밋본 = 생성 결과 · SHA256SUMS (다르면 rc 1)
    python3 make_unload_decks.py --selftest  # 구조 · G0 · 얼림 · 표 밖 상수 · 물리 창 재계산 · 멈춤 규칙 · 러너 짝

읽는 것 = unload_params.json 하나 (덱 안 숫자는 전부 표에서 · 표 밖 상수 lint) + 원 덱 글자 (리포 tgz r8 — 모델 머리 · 숫자를 다시 적지 않는다).
덱 (decks/<침대>/in.<종류>.liggghts):
  R       복원 시험 (S0 · 2,000 step · §3-2 · §12-1 ①②④): PRE_SETUP write_dump (바닥 이력 · 원자 omega) → run 0 (G1 · G2 · G2c · 판 이력 POST) →
          run 2000 (G3) → R_END 관측 → 보조 소거 (uncompute → unfix 두 벽 → 진단 restart un_diag.bin)
  UNread  보조 소거 읽기 (새 프로세스 — 진단 restart → 같은 머리 → PRE · POST 관측)
  UK      회전 KE 기준 (S0 무이동 3 창 · choice C4)
  UC      무이동 50,000 step × dt₀/dt (판 압력 표류 · 잡음 · KE)
  U_<팔>  언로딩 (UB · UVa · UVb · UT3 = 튜플 t1 · t2 · t4 · t3 · 전체 멈춤 규칙) — 상태 기계 (§4-2 · §5 · §12 · §13)
  G_<팔>  중력 팔 (R_M 에서 · 같은 머리 → run 0 → fix gravi 제자리 교체 g_aux · §6-2 h · §12-7 NO_BRACKET)
  (7:3) UT    dt₀/2 · 첫 교차 + 확인 두 단 → R_M 에서 멈춤 (§13-5 ③) · UTc = U_UT3 를 UT 의 R_M (상태 파일) 에서 재개 (같은 덱 블록)
  (7:3) Ut0   문법 (짧은 창 · 짧은 이동 · P_meas 크게 · 분리 문턱 크게 — 머리 → k = 0 → A 한 단 → B 단 → R_M → 분리 → 끝을 한 번씩 지나간다 · 판정 자료 아님)
  (10:0) EXT  3,600,000 에서 다시 읽어 60,000 (원 덱 출력 꼴 · 50,000 마다 restart → 3,650,000 · 끝 3,660,000 명시 write_restart)
  (10:0) EXT2 3,660,000 에서 50,000 (3,700,000 · 끝 3,710,000 명시)
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ul_gates  # noqa: E402
import ul_lib  # noqa: E402

DECK_DIR = 'decks'
SBATCH = 'run_unload_ibb.sbatch'
RUNNER = 'run_unload.sh'
BEDS = ('ps_0_10_r45', 'ps_3_7_r45', 'ps_5_5_r45', 'ps_7_3_r45', 'ps_10_0_r45')
PROD_ARMS = ('UB', 'UVa', 'UVb', 'UT3')


def deck_names():
    """→ {(침대, 종류): 상대 경로}."""
    out = {}
    for b in BEDS:
        kinds = ['R', 'UNread', 'UK', 'UC'] + [f'U_{a}' for a in PROD_ARMS] + [f'G_{a}' for a in PROD_ARMS]
        if b == 'ps_7_3_r45':
            kinds += ['UT', 'Ut0']
        if b == 'ps_10_0_r45':
            kinds += ['EXT', 'EXT2']
        for k in kinds:
            out[(b, k)] = os.path.join(DECK_DIR, b, f'in.{k}.liggghts')
    return out


# ── 구현 (아래 selftest 를 먼저 썼다) ─────────────────────────────────────────

LAZY_OK = {
    'pressMPa': 'r8 원 덱 머리의 thermo 변수 — run 중 thermo 가 부른다 (run 사이에 ${} 로 읽지 않는다)',
    'ul_Ps': '부호 있는 판 압력 — fix ul_av (ave/time) · thermo 가 run 중에 부른다 (run 사이에 ${} 로 읽지 않는다)',
    'ul_dnext': '덤프 주기 변수 (dump_modify every v_ul_dnext) — 덤프가 run 중에 부른다 · 창 끝 = 다음 W 배수 · 이동 중 = 멀리',
}
KINDS_DESC = {
    'R': '복원 시험 R (S0 · 2,000 step · PRE · POST · R_END · 보조 소거 진단 restart)',
    'UNread': '보조 소거 읽기 (R 의 진단 restart → 같은 머리 → PRE · POST 관측 · 진단 전용)',
    'UK': '회전 KE 기준 (S0 무이동 창 · choice C4)',
    'UC': '무이동 대조 UC (판 압력 표류 · 잡음 · KE)',
    'UT': '개발 팔 UT (dt₀/2 · 첫 교차 + 확인 두 단 → R_M 에서 멈춤 · §13-5 ③)',
    'Ut0': '문법 Ut0 (판정 자료 아님 · 짧은 창 · 짧은 이동 · 한 번씩 지나가기)',
    'EXT': '10:0 이완 연장 (3,600,000 에서 다시 읽어 60,000 · REG §10 Q11 (가) · §12-11)',
    'EXT2': '10:0 이완 연장 둘째 (3,660,000 에서 50,000 · S0′ 미달일 때만)',
}


def _fmt(x):
    """표 숫자 → 덱 글자 (정수면 정수 · 아니면 %.12g) — 렌더와 표 밖 상수 검사가 같은 함수를 쓴다."""
    if isinstance(x, bool):
        raise TypeError('bool 은 숫자가 아니다')
    if isinstance(x, int):
        return str(x)
    x = float(x)
    if x.is_integer() and abs(x) < 1e15:
        return str(int(x))
    return '%.12g' % x


def _int_of(x, what):
    r = round(x)
    if abs(x - r) > 1e-9 * max(1.0, abs(x)):
        raise SystemExit(f'⛔ {what} = {x} 가 정수가 아니다 (표 숫자 조합이 창 · 이동을 step 정수로 만들지 못한다)')
    return int(r)


def arm_numbers(arm, P=None):
    """팔 → 그 덱의 숫자 (전부 표에서 · §13-4 물리 창 W(dt) = T_W / dt)."""
    P = P or ul_lib.load_params()
    W0, pr = P['windows'], P['protocol']
    if arm == 'Ut0':
        u = P['ut0']
        return {'dt': None, 'v': pr['v0'], 'W': u['W'], 'nA': u['nA'], 'nB': u['nB'], 'k0min': u['k0_min'], 'k0max': u['k0_max'],
                'wmin': u['general_min'], 'wmax': u['budget_max'], 'sepreq': u['sep_declare'], 'postn': u['post_sep'],
                'ave_ne': u['ave_nevery'], 'ave_nr': u['ave_nrepeat'], 'thermo': u['thermo'], 'uc_steps': None, 'hf': 1}
    A = P['arms'][arm]
    f, hf = A['dt_factor'], A['hold_factor']
    dt = pr['dt0'] * f
    v = pr['v0'] * A['v_factor']
    out = {'dt': dt if f != 1.0 else None, 'v': v, 'W': _int_of(W0['W0'] / f, f'{arm} 창 W'), 'hf': hf,
           'k0min': W0['k0_min'], 'k0max': W0['budget_max'] * hf, 'wmin': W0['general_min'] * hf, 'wmax': W0['budget_max'] * hf,
           'sepreq': W0['sep_declare'], 'postn': W0['post_sep'], 'ave_ne': _int_of(W0['ave_nevery_dt0'] / f, f'{arm} ave nevery'),
           'ave_nr': W0['ave_nrepeat'], 'thermo': _int_of(W0['thermo_dt0'] / f, f'{arm} thermo'),
           'uc_steps': _int_of(W0['uc_steps_dt0'] / f, f'{arm} UC step')}
    out['nA'] = _int_of(pr['dz_A'] / (v * dt), f'{arm} A 이동 step') if v else 0
    out['nB'] = _int_of(pr['dz_B'] / (v * dt), f'{arm} B 이동 step') if v else 0
    if out['ave_ne'] * out['ave_nr'] != out['W']:
        raise SystemExit(f'⛔ {arm}: ave/time nevery × nrepeat ≠ W (창 전체 평균이 아니다)')
    for k in ('nA', 'nB'):
        if out[k] % out['W']:
            raise SystemExit(f'⛔ {arm}: {k} 가 W 의 배수가 아니다 (창 끝 ≠ run 끝)')
    return out


def _arm_of(kind):
    if kind.startswith(('U_', 'G_')):
        return kind.split('_', 1)[1]
    return {'UT': 'UT', 'Ut0': 'Ut0', 'UC': 'UC'}.get(kind, 'UB')


def _deck_nums(bed, kind, P):
    """이 덱이 쓸 수 있는 숫자 전부 (이름 → 표 값) — 렌더러는 숫자를 여기서만 꺼낸다."""
    B = P['beds'][bed]
    arm = _arm_of(kind)
    a = arm_numbers(arm, P)
    pr, st, W0, x = P['protocol'], P['steady'], P['windows'], P['ext_10_0']
    pm = P['P_meas_report_MPa'] / P['units']['report_MPa_per_Ps']
    n = {'W': a['W'], 'nA': a['nA'], 'nB': a['nB'], 'v': a['v'], 'k0min': a['k0min'], 'k0max': a['k0max'], 'wmin': a['wmin'],
         'wmax': a['wmax'], 'sepreq': a['sepreq'], 'postn': a['postn'], 'ave_ne': a['ave_ne'], 'ave_nr': a['ave_nr'], 'thermo': a['thermo'],
         'big': W0['big_every'], 'Pm': pm, 'PB': pr['B_switch_factor'] * pm, 'S1r': st['S1_rel'], 'S1a': st['S1_abs_factor_of_Pmeas'] * pm,
         'cap': pr['lift_cap'], 'conf': pr['confirm_steps'], 'glost': pr['guards']['atoms_lost'], 'gleak': pr['guards']['leak_increase'],
         'gke': pr['guards']['ke_trans_max'], 'sepnmax': P['separation']['sep_nmax'], 'atoms': B['atoms'], 'h0': B['h0'],
         'R_steps': W0['R_steps'], 'R_thermo': W0['R_thermo'], 'uk_windows': W0['uk_windows'], 'g_aux': P['g_aux'],
         'g_min': W0['gravity_hold_min'], 'g_max': W0['gravity_hold_max']}
    if a['dt'] is not None:
        n['dt'] = a['dt']
    if a['uc_steps'] is not None:
        n['uc_steps'] = a['uc_steps']
    if bed == 'ps_10_0_r45':
        n['s0'] = x['start_step'] if kind in ('R', 'UNread', 'EXT') else B['s0_candidates'][0]
        n.update(ext_start=x['start_step'], ext_run1=x['run1'], ext_end1=x['end1'], ext_run2=x['run2'], ext_restart=x['restart_every'],
                 ext_atom=x['atom_every'], ext_mesh=x['mesh_every'], ext_contact=x['contact_every'], ext_thermo=x['thermo'])
    else:
        n['s0'] = B['s0']
    if kind == 'Ut0':
        u = P['ut0']
        n.update(Pm=u['P_meas_deck'], PB=pr['B_switch_factor'] * u['P_meas_deck'], S1a=st['S1_abs_factor_of_Pmeas'] * u['P_meas_deck'],
                 sepnmax=u['sep_nmax'], S2max=u['S2max'])
    return n


def table_numbers(bed, kind, P=None):
    P = P or ul_lib.load_params()
    return {_fmt(v) for v in _deck_nums(bed, kind, P).values()}


# ── 원 덱 머리 (r8 글자 · 숫자를 다시 적지 않는다) ─────────────────────────────

def _r8_head(P):
    L = ul_lib.logical_lines(ul_lib.r8_text(P))
    cmd = {}

    def take(key, pred, last=False):
        hits = [ln for ln in L if pred(ln)]
        if not hits or (not last and len(hits) != 1):
            raise SystemExit(f'⛔ r8 에서 {key} 가 {len(hits)} 번')
        cmd[key] = hits[-1]

    for k in ('atom_style', 'atom_modify', 'boundary', 'newton', 'soft_particles', 'communicate', 'units', 'processors', 'neighbor',
              'neigh_modify', 'pair_style', 'pair_coeff', 'timestep'):
        take(k, lambda ln, k=k: ln.split()[0] == k)
    for v in ('r_AM_P', 'r_AM_S', 'r_SE', 'dt'):
        take(v, lambda ln, v=v: ln.split()[:2] == ['variable', v])
    for m in range(1, 10):
        take(f'm{m}', lambda ln, m=m: ln.split()[:2] == ['fix', f'm{m}'])
    for c in ('strs', 'ke', 'cpl'):
        take(c, lambda ln, c=c: ln.split()[:2] == ['compute', c])
    for f in ('zwall_bot', 'integr', 'gravi', 'top_mesh', 'zwall_top'):
        take(f, lambda ln, f=f: ln.split()[:2] == ['fix', f])
    last_run = max(i for i, ln in enumerate(L) if ln.split()[0] == 'run')
    damps = [ln for ln in L[:last_run] if ln.split()[:2] == ['fix', 'damp']]
    cmd['damp'] = damps[-1]
    take('energy', lambda ln: ln == 'fix_modify zwall_top energy yes')
    take('pressMPa', lambda ln: ln.split()[:2] == ['variable', 'pressMPa'])
    tw = cmd['top_mesh'].split()
    tw[tw.index('file') + 1] = '${plate_stl}'
    cmd['top_mesh'] = ' '.join(tw)
    return cmd


def _head(P, arm_dt=None):
    c = _r8_head(P)
    L = ['# >>> block head — 원 마지막 조각 덱 (r8 꼴) 이 S0 에 켜 둔 정의 그대로 · 순서 = 원 PHASE 4 (zwall_bot → integr → gravi → top_mesh → zwall_top → damp)',
         '#     (r8 글자에서 뽑았다 · 판 STL 경로만 ${plate_stl} — 메시 자료는 restart 에서 · 압축 감쇠 0.5 · 판 이동 fix 는 S0 에 없다)']
    L += [c[k] for k in ('atom_style', 'atom_modify', 'boundary', 'newton', 'soft_particles', 'communicate', 'units')]
    L += ['', c['r_AM_P'], c['r_AM_S'], c['r_SE'], c['dt'], c['timestep'], c['processors'], '', 'read_restart ${ckpt}', '',
          c['neighbor'], c['neigh_modify'], '']
    L += [c[f'm{m}'] for m in range(1, 10)]
    L += ['', c['pair_style'], c['pair_coeff'], '', c['strs'], c['ke'], c['cpl'], '', c['zwall_bot'], '',
          c['integr'], c['gravi'], c['top_mesh'], c['zwall_top'], c['damp'], c['energy'], '', c['pressMPa'], '# <<< block head', '']
    if arm_dt is not None:
        L += ['# >>> block arm_dt — 등록된 팔 dt (read_restart 뒤 — restart 파일이 dt 를 되살리는 규약 · REG §4-3)',
              f'variable dt equal {_fmt(arm_dt)}', 'timestep ${dt}', '# <<< block arm_dt', '']
    return L


def _banner(bed, kind, P):
    arm = _arm_of(kind)
    desc = KINDS_DESC.get(kind) or (f'언로딩 팔 {arm} (튜플 {next((t for t, v in P["tuples"].items() if v["arm"] == arm), "—")} · 전체 멈춤 규칙)'
                                    if kind.startswith('U_') else f'중력 팔 {arm} (R_M 에서 · g_aux · §6-2 h · §12-7)')
    return ['# ============================================================',
            f'# DEM 언로딩 키트 — {bed} · {kind} — {desc}',
            '#   생성: make_unload_decks.py (손으로 고치지 말 것 — 생성기를 고치고 다시 만든다 · SHA256SUMS)',
            '#   정본: docs/data/ps45_unload_20261009/README.md · 등록 docs/reviews/dem_unloading_ps45_prereg_20261009.md §12 · §13',
            '#   변수 (run_unload.sh 가 -var 로 준다): out (이 런 폴더) · plate_stl (판 STL · 자료는 restart 에서) · ckpt (읽을 restart) ·',
            '#     ul_base (KE 기준 파일 · S2) · ul_state (상태 파일 · 이어 돌림 · 중력 팔) · ul_resume (1 = 이어 돌림) · ul_s0 (10:0 S0′ 결정)',
            '#   모델 머리 = 원 덱 글자 · 언로딩 블록 숫자 = unload_params.json (덱 안 상수로 다시 적지 않는다 · 생성기 selftest 가 검사)',
            '# ============================================================', '']


def _params(bed, kind, n, extra=()):
    L = ['# >>> block ul_params — 표 (unload_params.json) 에서 온 숫자 · 이름 (덱 생성기가 적는다)',
         f'variable ul_arm string {kind}', f'variable ul_bed string {bed}', f'variable ul_s0 index {_fmt(n["s0"])}',
         f'variable ul_atoms0 equal {_fmt(n["atoms"])}', f'variable ul_h0 equal {_fmt(n["h0"])}',
         f'variable ul_v equal {_fmt(n["v"])}', f'variable ul_W equal {_fmt(n["W"])}', f'variable ul_nA equal {_fmt(n["nA"])}',
         f'variable ul_nB equal {_fmt(n["nB"])}']
    L += [f'variable ul_k0min equal {_fmt(n["k0min"])}', f'variable ul_k0max equal {_fmt(n["k0max"])}',
          f'variable ul_wmin0 equal {_fmt(n["wmin"])}', f'variable ul_wmax0 equal {_fmt(n["wmax"])}',
          f'variable ul_sepreq equal {_fmt(n["sepreq"])}', f'variable ul_sepnmax equal {_fmt(n["sepnmax"])}',
          f'variable ul_postn equal {_fmt(n["postn"])}', f'variable ul_ave_ne equal {_fmt(n["ave_ne"])}',
          f'variable ul_ave_nr equal {_fmt(n["ave_nr"])}', f'variable ul_thermo equal {_fmt(n["thermo"])}',
          f'variable ul_big equal {_fmt(n["big"])}', f'variable ul_Pm equal {_fmt(n["Pm"])}', f'variable ul_PB equal {_fmt(n["PB"])}',
          f'variable ul_S1r equal {_fmt(n["S1r"])}', f'variable ul_S1a equal {_fmt(n["S1a"])}', f'variable ul_cap equal {_fmt(n["cap"])}',
          f'variable ul_conf equal {_fmt(n["conf"])}', f'variable ul_glost equal {_fmt(n["glost"])}',
          f'variable ul_gleak equal {_fmt(n["gleak"])}', f'variable ul_gke equal {_fmt(n["gke"])}']
    L += list(extra)
    L += ['variable ul_resume index 0', 'variable ul_dzA equal ${ul_v}*${dt}*${ul_nA}', 'variable ul_dzB equal ${ul_v}*${dt}*${ul_nB}',
          'variable ul_amin equal ${ul_atoms0}-${ul_glost}']
    if kind == 'Ut0':
        L.append(f'variable ul_S2max equal {_fmt(n["S2max"])}')
    elif kind != 'UK':
        L.append('include ${ul_base}')
    L += ['# <<< block ul_params', '']
    return L


def _obs(P, dumps=True, contact=True, first=False):
    sign = '' if P['Ps_sign'] == 1 else '-'
    L = ['# >>> block ul_obs — 관측 (ul_ 접두 · 동역학 없음 · 판 압력 부호 있음 = Ps · 보고 MPa = 1000 · Ps)',
         'compute ul_ke all ke', 'compute ul_erot all erotate/sphere', 'compute ul_wh all wall/gran/local id force_normal',
         f'variable ul_Ps equal {sign}f_top_mesh[3]/0.0025/1000000',
         'fix ul_av all ave/time ${ul_ave_ne} ${ul_ave_nr} ${ul_W} v_ul_Ps c_ul_ke c_ul_erot',
         'group ul_t1 type 1', 'group ul_t2 type 2', 'group ul_t3 type 3',
         'region ul_bel block INF INF INF INF INF 0.0 units box']
    L += _regions('${ul_h0}', create=True)
    L += ['thermo_style custom ' + P['records']['thermo_style'], 'thermo ${ul_thermo}', 'variable ul_dnext equal step+${ul_big}']
    if dumps:
        fa = '%d %d ' + ' '.join([P['dumps']['atom_format_float']] * 15)
        L += ['dump ul_da all custom ${ul_W} ${out}/dump/atom_*.dump id type x y z radius mass vx vy vz omegax omegay omegaz fx fy fz',
              f'dump_modify ul_da every v_ul_dnext format "{fa}"' + (' first yes' if first else ''),
              'dump ul_dw all local ${ul_W} ${out}/dump/wall_*.dump ' + ' '.join(f'c_ul_wh[{i}]' for i in range(1, 7)),
              'dump_modify ul_dw every v_ul_dnext format "' + ' '.join([P['dumps']['atom_format_float']] * 6) + '"' + (' first yes' if first else '')]
        if contact:
            L += ['dump ul_dc all local ${ul_W} ${out}/dump/contact_*.dump ' + ' '.join(f'c_cpl[{i}]' for i in range(1, 27)),
                  'dump_modify ul_dc every v_ul_dnext' + (' first yes' if first else '')]
        L += ['dump ul_dm all mesh/stl ${ul_W} ${out}/dump/mesh_*.stl top_mesh']
    L += ['# <<< block ul_obs', '']
    return L


def _regions(pz, create=False):
    """판 접촉 기하 영역 (중심이 [판 − r, 판] = z + r > 판 · 판 위 중심 제외) · 새어 나감 (판 위 중심)."""
    L = [] if create else ['region ul_c1 delete', 'region ul_c2 delete', 'region ul_c3 delete', 'region ul_abv delete']
    for i, r in ((1, 'r_AM_P'), (2, 'r_AM_S'), (3, 'r_SE')):
        L += [f'variable ul_lo{i} equal {pz}-${{{r}}}', f'region ul_c{i} block INF INF INF INF ${{ul_lo{i}}} {pz} units box']
    L += [f'region ul_abv block INF INF INF INF {pz} INF units box']
    return L


def _records_head(P):
    R = P['records']
    return [f'print "{",".join(R["windows_cols"])}" file ${{out}}/ul_windows.csv screen no',
            f'print "{",".join(R["steps_cols"])}" file ${{out}}/ul_steps.csv screen no',
            f'print "{",".join(R["events_cols"])}" file ${{out}}/ul_events.csv screen no']


def _ev(name, detail):
    return f'print "{name},${{ul_k}},${{ul_step}},${{ul_pz}},${{ul_lift}},{detail}" append ${{out}}/ul_events.csv screen no'


def _freeze(name, expr):
    return [f'variable {name} equal {expr}', f'variable {name} equal ${{{name}}}']


def _window_read(s2=True):
    """run 바로 뒤 읽기 — 정의 다음 줄에서 즉시 치환으로 얼린다 (⑭b) · write_restart 전 (⑭a)."""
    L = _freeze('ul_step', 'step') + _freeze('ul_P', 'f_ul_av[1]') + _freeze('ul_Kt', 'f_ul_av[2]') + _freeze('ul_Kr', 'f_ul_av[3]')
    L += _freeze('ul_Kti', 'ke') + _freeze('ul_na', 'atoms') + _freeze('ul_nc', 'count(ul_t1,ul_c1)+count(ul_t2,ul_c2)+count(ul_t3,ul_c3)')
    L += _freeze('ul_lk', 'count(all,ul_bel)+count(all,ul_abv)')
    L += ['variable ul_lkd equal ${ul_lk}-${ul_lk0}', 'variable ul_w equal ${ul_w}+1', 'variable ul_K equal ${ul_Kt}+${ul_Kr}',
          'variable ul_S1 equal (${ul_w}>1)&&((abs(${ul_P}-${ul_Pprev})<=${ul_S1r}*abs(${ul_P}))||(abs(${ul_P}-${ul_Pprev})<=${ul_S1a}))']
    if s2:
        L += ['variable ul_S2 equal ${ul_K}<=${ul_S2max}', 'variable ul_ok equal ${ul_S1}&&${ul_S2}']
    else:
        L += ['variable ul_S2 equal -1', 'variable ul_ok equal -1']
    L += ['variable ul_Pbar2 equal (${ul_P}+${ul_Pprev})/2', 'variable ul_Pprev equal ${ul_P}',
          'if "${ul_ok} == 1" then "variable ul_okn equal ${ul_okn}+1" else "variable ul_okn equal 0"',
          'if "${ul_nc} <= ${ul_sepnmax}" then "variable ul_sepn equal ${ul_sepn}+1" else "variable ul_sepn equal 0"',
          'print "${ul_arm},${ul_bed},${ul_k},${ul_w},${ul_phase},${ul_step},${ul_pz},${ul_lift},${ul_P},${ul_Kt},${ul_Kr},${ul_K},'
          '${ul_S1},${ul_S2},${ul_ok},${ul_nc},${ul_na},${ul_lk},${ul_Kti}" append ${out}/ul_windows.csv screen no',
          'if "${ul_na} < ${ul_amin}" then "variable ul_why string atoms_lost" "jump SELF ul_guard"',
          'if "${ul_lkd} > ${ul_gleak}" then "variable ul_why string leak" "jump SELF ul_guard"',
          'if "${ul_Kt} > ${ul_gke}" then "variable ul_why string ke_trans_avg" "jump SELF ul_guard"',
          'if "${ul_Kti} > ${ul_gke}" then "variable ul_why string ke_trans_inst" "jump SELF ul_guard"']
    return L


def _state(fname):
    keys = ('ul_k', 'ul_phase', 'ul_modeB', 'ul_pz', 'ul_lift', 'ul_ncross', 'ul_xk', 'ul_lk0', 'ul_Pbar')
    path = '${out}/restart/' + fname + '_${ul_step}.in'
    L = [f'print "variable ul_rstep equal ${{ul_step}}" file {path} screen no']
    L += [f'print "variable {k} equal ${{{k}}}" append {path} screen no' for k in keys]
    L += [f'print "variable ul_kind string ${{ul_kind}}" append {path} screen no']
    return L


def _summary_block():
    keys = ('result', 'arm', 'bed', 'step', 'k', 'phase', 'modeB', 'pz', 'lift', 'xk', 'ncross', 'why')
    L = ['label ul_summary', 'print "result=${ul_result}" file ${out}/ul_summary.txt screen no']
    L += [f'print "{k}=${{ul_{k}}}" append ${{out}}/ul_summary.txt screen no' for k in keys[1:]]
    L += ['print "UL_SUMMARY arm=${ul_arm} bed=${ul_bed} result=${ul_result} step=${ul_step} k=${ul_k} plate_z=${ul_pz} lift=${ul_lift} why=${ul_why}"',
          'jump SELF ul_end']
    return L


def _start_checks():
    L = _freeze('ul_step', 'step') + _freeze('ul_na', 'atoms')
    L += ['if "${ul_step} != ${ul_s0}" then "print \'UL_ABORT reason=start_step step=${ul_step} expect=${ul_s0}\'" "quit"',
          'if "${ul_na} != ${ul_atoms0}" then "print \'UL_ABORT reason=start_atoms atoms=${ul_na} expect=${ul_atoms0}\'" "quit"']
    return L


def _init_state():
    return ['variable ul_k equal 0', 'variable ul_phase equal 4', 'variable ul_modeB equal 0', 'variable ul_pz equal ${ul_h0}',
            'variable ul_lift equal 0', 'variable ul_ncross equal 0', 'variable ul_xk equal -1', 'variable ul_Pbar equal 0',
            'variable ul_kind string 0', 'variable ul_why string none', 'variable ul_result string RUNNING', 'variable ul_postw equal 0',
            'variable ul_steady equal 0']


def _machine(kind, gravity=False, stop_rm=False):
    """언로딩 상태 기계 (§4-2 · §5 · §12 · §13): 창 고리 · 유지 끝 (S1 ∧ S2 두 창 · 최소 · 최대) · 단 끝 (교차 · 확인 · R_M · 분리) · 다음 이동."""
    L = ['# >>> block machine — 상태 기계 (단계 ul_phase: 4 HOLD0 · 0 SEARCH · 1 CONFIRM · 2 SEPARATE · 3 POST)',
         'label ul_hold_start', 'variable ul_w equal 0', 'variable ul_okn equal 0', 'variable ul_sepn equal 0', 'variable ul_Pprev equal 0',
         'variable ul_Pbar2 equal 0', 'variable ul_rc equal 0',
         'if "${ul_phase} == 4" then "variable ul_wmin equal ${ul_k0min}" "variable ul_wmax equal ${ul_k0max}" '
         'else "variable ul_wmin equal ${ul_wmin0}" "variable ul_wmax equal ${ul_wmax0}"',
         'variable ul_dnext equal (floor(step/${ul_W})+1)*${ul_W}',
         'label ul_win', 'run ${ul_W}']
    L += _window_read()
    L += ['if "${ul_phase} == 3" then "jump SELF ul_win_post"', 'if "${ul_phase} == 2" then "jump SELF ul_win_sep"',
          'label ul_win_gen',
          'if "(${ul_w} >= ${ul_wmin}) && (${ul_okn} >= 2)" then "variable ul_steady equal 1" "jump SELF ul_hold_end"',
          'if "${ul_w} >= ${ul_wmax}" then "variable ul_steady equal 0" "jump SELF ul_hold_end"', 'jump SELF ul_win',
          '# 분리 (개정 3 §14-7 · Q6): 선언 = 유지 예산 안 · 분리 뒤 4 창 = 예산과 따로 · 재접촉 = 같은 높이 · 남은 예산 (k + 1 로 옮기지 않는다) · 예산 끝 = SEP_INCOMPLETE',
          'label ul_win_sep', 'if "${ul_sepn} >= ${ul_sepreq}" then "jump SELF ul_declare_sep"', 'if "${ul_rc} == 1" then "jump SELF ul_win_rc"',
          'jump SELF ul_win_gen',
          'label ul_declare_sep', 'variable ul_phase equal 3', 'variable ul_postw equal 1', _ev('SEPARATED', 'w${ul_w}'),
          'if "${ul_postw} >= ${ul_postn}" then "jump SELF ul_finish_ok"', 'jump SELF ul_win',
          'label ul_win_post', 'if "${ul_nc} > ${ul_sepnmax}" then "jump SELF ul_recontact"', 'variable ul_postw equal ${ul_postw}+1',
          'if "${ul_postw} >= ${ul_postn}" then "jump SELF ul_finish_ok"', 'jump SELF ul_win',
          'label ul_recontact', 'variable ul_phase equal 2', 'variable ul_postw equal 0', 'variable ul_rc equal 1', _ev('RECONTACT', 'n${ul_nc}'),
          'label ul_win_rc', 'if "${ul_w} >= ${ul_wmax}" then "jump SELF ul_sep_incomplete"', 'jump SELF ul_win',
          '# 단 끝 — P̄_k = 마지막 두 창 평균 · 단 줄 기록 뒤 단계 전이',
          'label ul_hold_end', 'variable ul_Pbar equal ${ul_Pbar2}',
          'print "${ul_arm},${ul_bed},${ul_k},${ul_kind},${ul_dz},${ul_n},${ul_step},${ul_pz},${ul_lift},${ul_Pbar},${ul_w},${ul_steady},'
          '${ul_phase},${ul_modeB},${ul_nc}" append ${out}/ul_steps.csv screen no',
          'if "${ul_phase} == 4" then "jump SELF ul_end_hold0"', 'if "${ul_phase} == 0" then "jump SELF ul_end_search"',
          'if "${ul_phase} == 1" then "jump SELF ul_end_confirm"', 'jump SELF ul_step_done']
    if gravity:
        L += ['# 중력 팔 첫 유지 끝 (§12-7): 정상 · P̄ > P_meas 일 때만 B 단 교차 · 아니면 NO_BRACKET (재압축 없음 · 분리 · 표면만)',
              'label ul_end_hold0', _ev('GRAVITY_HOLD_DONE', 'steady${ul_steady}'),
              'if "${ul_steady} == 0" then "variable ul_why string unsteady" "jump SELF ul_nobracket"',
              'if "${ul_sepn} >= ${ul_sepreq}" then "variable ul_why string separated" "jump SELF ul_nobracket"',
              'if "${ul_Pbar} <= ${ul_Pm}" then "variable ul_why string le_Pmeas" "jump SELF ul_nobracket"',
              'variable ul_phase equal 0', 'variable ul_modeB equal 1', 'jump SELF ul_step_done',
              'label ul_nobracket', _ev('NO_BRACKET', '${ul_why}'), 'variable ul_phase equal 2', 'variable ul_modeB equal 1',
              'jump SELF ul_step_done']
    else:
        L += ['label ul_end_hold0', 'if "${ul_steady} == 0" then "variable ul_why string k0_unsteady" "jump SELF ul_tech"',
              'variable ul_phase equal 0', _ev('HOLD0_DONE', 'Pbar0'), 'jump SELF ul_step_done']
    L += ['label ul_end_search', 'if "${ul_Pbar} <= ${ul_Pm}" then "jump SELF ul_cross"',
          'if "(${ul_modeB} == 0) && (${ul_Pbar} <= ${ul_PB})" then "jump SELF ul_modeb"', 'jump SELF ul_step_done',
          'label ul_modeb', 'variable ul_modeB equal 1', _ev('MODE_B', 'next'), 'jump SELF ul_step_done',
          'label ul_cross', 'variable ul_phase equal 1', 'variable ul_modeB equal 1', 'variable ul_ncross equal 0',
          'variable ul_xk equal ${ul_k}', _ev('CROSS', 'first'), 'jump SELF ul_step_done',
          'label ul_end_confirm', 'variable ul_ncross equal ${ul_ncross}+1', 'if "${ul_ncross} >= ${ul_conf}" then "jump SELF ul_rm"',
          'jump SELF ul_step_done',
          'label ul_rm', 'variable ul_phase equal 2']
    if gravity:
        L += [_ev('CONFIRMED', 'ncross${ul_ncross}'), 'jump SELF ul_step_done']
    else:
        L += [_ev('RM', 'ncross${ul_ncross}'), 'write_restart ${out}/restart/restart_RM_${ul_step}.bin'] + _state('state_RM')
        L += ['jump SELF ul_rmstop' if stop_rm else 'jump SELF ul_step_done']
        if stop_rm:
            L += ['# UT 멈춤 (§13-5 ③) — 같은 궤적의 분리 · 중력 분기는 결정표 3 행일 때 UTc (U_UT3 덱을 이 R_M 상태에서 이어 돌림)',
                  'label ul_rmstop', _ev('RM_STOP', 'UT'), 'variable ul_result string RM_STOP', 'jump SELF ul_summary']
    L += ['# 단 끝 restart + 이어 돌릴 상태 (다음 이동 결정 뒤의 단계 · 방식)', 'label ul_step_done',
          'write_restart ${out}/restart/restart_unload_${ul_step}.bin'] + _state('state_unload') + ['jump SELF ul_next']
    L += ['# 다음 이동 — A (Δz_A) · B (Δz_B · P̄ ≤ 3 P_meas 다음 단부터 · 교차 뒤 확인 · 분리) · 들어 올림 상한 (같은 Δz_B 배수 규칙)',
          'label ul_next', 'variable ul_n equal ${ul_nA}', 'variable ul_dz equal ${ul_dzA}', 'variable ul_kind string A',
          'if "${ul_modeB} == 1" then "variable ul_n equal ${ul_nB}" "variable ul_dz equal ${ul_dzB}" "variable ul_kind string B"',
          'variable ul_capx equal (${ul_lift}+${ul_dz})>(${ul_cap}+${ul_dzB}/2)',
          'if "${ul_capx} == 1" then "jump SELF ul_cap_stop"', 'variable ul_k equal ${ul_k}+1', 'variable ul_dnext equal step+${ul_big}',
          'fix ul_mv all move/mesh mesh top_mesh linear 0.0 0.0 ${ul_v}', 'run ${ul_n}', 'unfix ul_mv',
          'variable ul_pz equal ${ul_pz}+${ul_dz}', 'variable ul_lift equal ${ul_pz}-${ul_h0}']
    L += _regions('${ul_pz}') + ['jump SELF ul_hold_start']
    L += ['label ul_cap_stop', _ev('LIFT_CAP', 'cap'), 'variable ul_result string LIFT_CAP', 'jump SELF ul_summary',
          'label ul_sep_incomplete', _ev('SEP_INCOMPLETE', 'w${ul_w}'), 'variable ul_result string SEP_INCOMPLETE', 'jump SELF ul_summary',
          'label ul_finish_ok', _ev('POST_DONE', 'w${ul_w}'), 'variable ul_result string DONE',
          'write_restart ${out}/restart/restart_final_${ul_step}.bin', 'jump SELF ul_summary',
          'label ul_guard', _ev('GUARD', '${ul_why}'), 'variable ul_result string GUARD',
          'write_restart ${out}/restart/restart_guard_${ul_step}.bin', 'jump SELF ul_summary',
          'label ul_tech', _ev('TECH', '${ul_why}'), 'variable ul_result string TECH', 'jump SELF ul_summary']
    L += _summary_block() + ['# <<< block machine', '', 'label ul_end', 'print "UL_SCRIPT_END arm=${ul_arm} bed=${ul_bed} result=${ul_result}"']
    return L


def _render_U(bed, kind, P):
    """U_<팔> · UT · Ut0 · G_<팔>."""
    n = _deck_nums(bed, kind, P)
    gravity = kind.startswith('G_')
    L = _banner(bed, kind, P) + _head(P, n.get('dt'))
    extra = [f'variable ul_gmin equal {_fmt(n["g_min"])}', f'variable ul_gmax equal {_fmt(n["g_max"])}'] if gravity else []
    L += _params(bed, kind, n, extra)
    if gravity:
        L += ['variable ul_k0min equal ${ul_gmin}', 'variable ul_k0max equal ${ul_gmax}', '']
    L += _obs(P, first=gravity)
    if gravity:
        L += ['# >>> block g_start — 팔의 R_M (restart + 상태 파일) 에서 · 같은 머리 → run 0 (G1 · G2 · G2c) → 중력 제자리 교체 (같은 ID = 같은 자리)',
              'include ${ul_state}'] + _freeze('ul_step', 'step')
        L += ['if "${ul_step} != ${ul_rstep}" then "print \'UL_ABORT reason=start_step step=${ul_step} expect=${ul_rstep}\'" "quit"',
              'variable ul_why string none', 'variable ul_result string RUNNING', 'variable ul_postw equal 0', 'variable ul_steady equal 0']
        L += _regions('${ul_pz}') + _records_head(P) + [_ev('START', 'RM_branch'), 'run 0',
                                                         f'fix gravi all gravity {_fmt(n["g_aux"])} vector 0.0 0.0 -1.0',
                                                         'variable ul_k equal 0', 'variable ul_phase equal 4', 'variable ul_modeB equal 1',
                                                         'variable ul_ncross equal 0', 'variable ul_xk equal -1', 'variable ul_kind string 0',
                                                         'variable ul_dz equal 0', 'variable ul_n equal 0', _ev('GRAVITY_ON', 'g_aux'),
                                                         'jump SELF ul_hold_start', '# <<< block g_start', '']
    else:
        L += ['# >>> block start — 처음 (S0) 또는 이어 돌림 (단 끝 restart + 상태 파일 · 같은 덱)',
              '#   상태 파일은 늘 맨 바깥에서 include (if 안 include = 3d5c00f input.cpp 845 ERROR) — 처음이면 러너가 빈 파일 (주석뿐) 을 준다',
              'include ${ul_state}', 'if "${ul_resume} == 1" then "jump SELF ul_resumed"']
        L += _start_checks() + _init_state() + ['variable ul_dz equal 0', 'variable ul_n equal 0']
        L += _freeze('ul_lk0', 'count(all,ul_bel)+count(all,ul_abv)') + _records_head(P) + [_ev('START', 's0')]
        L += ['print "UL_START arm=${ul_arm} bed=${ul_bed} step=${ul_step} atoms=${ul_na} leak0=${ul_lk0} plate_z=${ul_pz}"',
              'jump SELF ul_hold_start', 'label ul_resumed'] + _freeze('ul_step', 'step')
        L += ['if "${ul_step} != ${ul_rstep}" then "print \'UL_ABORT reason=resume_step step=${ul_step} expect=${ul_rstep}\'" "quit"',
              'variable ul_why string none', 'variable ul_result string RUNNING', 'variable ul_postw equal 0', 'variable ul_steady equal 0',
              'variable ul_dz equal 0', 'variable ul_n equal 0']
        L += _regions('${ul_pz}') + [_ev('RESUME', 'state'), 'print "UL_RESUME arm=${ul_arm} bed=${ul_bed} step=${ul_step} k=${ul_k} phase=${ul_phase}"',
                                     'jump SELF ul_next', '# <<< block start', '']
    L += _machine(kind, gravity=gravity, stop_rm=(kind == 'UT'))
    return '\n'.join(L) + '\n'


def _render_noMove(bed, kind, P):
    """UK (회전 KE 기준 · 창 n 개) · UC (무이동 50,000 step × dt₀/dt)."""
    n = _deck_nums(bed, kind, P)
    L = _banner(bed, kind, P) + _head(P, n.get('dt'))
    extra = [f'variable ul_uc_steps equal {_fmt(n["uc_steps"])}'] if kind == 'UC' else [f'variable ul_ukw equal {_fmt(n["uk_windows"])}']
    L += _params(bed, kind, n, extra)
    L += _obs(P, dumps=(kind == 'UC'), contact=False)
    L += ['# >>> block nomove — S0 에서 판 고정 · 창마다 기록 (단계 4 · k = 0)'] + _start_checks() + _init_state()
    L += ['variable ul_dz equal 0', 'variable ul_n equal 0'] + _freeze('ul_lk0', 'count(all,ul_bel)+count(all,ul_abv)') + _records_head(P)
    L += [_ev('START', 's0'), 'variable ul_nwin equal ' + ('${ul_uc_steps}/${ul_W}' if kind == 'UC' else '${ul_ukw}'),
          'variable ul_w equal 0', 'variable ul_okn equal 0', 'variable ul_sepn equal 0', 'variable ul_Pprev equal 0',
          'variable ul_Pbar2 equal 0', 'variable ul_dnext equal (floor(step/${ul_W})+1)*${ul_W}', 'label ul_win', 'run ${ul_W}']
    L += _window_read(s2=(kind == 'UC'))
    L += ['if "${ul_w} < ${ul_nwin}" then "jump SELF ul_win"', 'variable ul_Pbar equal ${ul_Pbar2}', _ev('NOMOVE_DONE', 'w${ul_w}'),
          'variable ul_result string DONE', 'jump SELF ul_summary',
          'label ul_guard', _ev('GUARD', '${ul_why}'), 'variable ul_result string GUARD', 'jump SELF ul_summary']
    L += _summary_block() + ['# <<< block nomove', '', 'label ul_end', 'print "UL_SCRIPT_END arm=${ul_arm} bed=${ul_bed} result=${ul_result}"']
    return '\n'.join(L) + '\n'


def _hist_dump_cols(forces=True):
    """바닥 primitive 이력 관측 열 — PRE_SETUP (write_dump · setup 전) 은 힘을 빼고 (아직 계산 전) · POST 는 총힘 포함 (이력 시험 관측자와 같은 꼴)."""
    return ('id type x y z radius mass vx vy vz omegax omegay omegaz ' + ('fx fy fz ' if forces else '')
            + 'f_history_zwall_bot[1] f_history_zwall_bot[2] f_history_zwall_bot[3] f_history_zwall_bot[4]')


def _render_R(bed, kind, P):
    n = _deck_nums(bed, kind, P)
    L = _banner(bed, kind, P) + _head(P)
    L += ['# >>> block r_params — 표에서 온 숫자', f'variable ul_bed string {bed}', f'variable ul_s0 index {_fmt(n["s0"])}',
          f'variable ul_atoms0 equal {_fmt(n["atoms"])}', f'variable ul_big equal {_fmt(n["big"])}', '# <<< block r_params', '',
          '# >>> block r_obs — 복원 관측 (ul_ 접두 · 동역학 없음) · 벽 local = mesh 판만 (3d5c00f compute_pair_gran_local.cpp 247–269 행)',
          'compute ul_erot all erotate/sphere', 'compute ul_wh all wall/gran/local id history force_normal',
          f'variable ul_Ps equal {"" if P["Ps_sign"] == 1 else "-"}f_top_mesh[3]/0.0025/1000000',
          'thermo_style custom ' + P['records']['thermo_style'], f'thermo {_fmt(n["R_thermo"])}', '# <<< block r_obs', '']
    wfmt = ' '.join(['%.17g'] * 10)
    afmt = '%d %d ' + ' '.join(['%.17g'] * 18)
    pfmt = '%d %d ' + ' '.join(['%.17g'] * 15)
    hcols, pcols = _hist_dump_cols(), _hist_dump_cols(forces=False)
    if kind == 'R':
        L += ['# >>> block r_start — S0 · G1 (setup 줄) · PRE_SETUP (바닥 primitive 배열 그대로 · write_dump = 덤프 init → write · system setup 없음)']
        L += _freeze('ul_step', 'step') + _freeze('ul_na', 'atoms')
        L += ['if "${ul_step} != ${ul_s0}" then "print \'UL_ABORT reason=start_step step=${ul_step} expect=${ul_s0}\'" "quit"',
              'if "${ul_na} != ${ul_atoms0}" then "print \'UL_ABORT reason=start_atoms atoms=${ul_na} expect=${ul_atoms0}\'" "quit"',
              'print "UL_R_START bed=${ul_bed} step=${ul_step} atoms=${ul_na}"',
              f'write_dump all custom ${{out}}/obs/pre_bot.dump {pcols} modify format "{pfmt}"',
              '# POST_SETUP (run 0) — G2 (원 형식 atom · 기본 형식 · 글자 대조) · G2c (원 형식 쌍 접촉 26 열) · 판 mesh md5 · 판 · 바닥 이력 · omega (새 출력)',
              'dump ul_g2a all custom ${ul_big} ${out}/g2/atom_*.liggghts id type x y z radius vx vy vz c_strs[1] c_strs[2] c_strs[3] c_ke',
              'dump_modify ul_g2a first yes',
              'dump ul_g2c all local ${ul_big} ${out}/g2/contact_*.liggghts ' + ' '.join(f'c_cpl[{i}]' for i in range(1, 27)),
              'dump_modify ul_g2c first yes', 'dump ul_g2m all mesh/stl ${ul_big} ${out}/g2/mesh_*.stl top_mesh', 'dump_modify ul_g2m first yes',
              'dump ul_ow all local ${ul_big} ${out}/obs/post_wall_*.dump ' + ' '.join(f'c_ul_wh[{i}]' for i in range(1, 11)),
              f'dump_modify ul_ow first yes format "{wfmt}"', f'dump ul_oa all custom ${{ul_big}} ${{out}}/obs/post_atom_*.dump {hcols}',
              f'dump_modify ul_oa first yes format "{afmt}"', 'run 0',
              'undump ul_g2a', 'undump ul_g2c', 'undump ul_g2m', 'undump ul_ow', 'undump ul_oa', 'print "UL_R_SETUP_DONE step=${ul_step}"',
              '# G3 — 2,000 step (판 고정 = 원 PHASE 4 그대로 · 첫 정규 줄 = 원 로그 같은 step)', f'run {_fmt(n["R_steps"])}']
        L += _freeze('ul_step', 'step')
        L += ['print "UL_R_END step=${ul_step}"', '# R_END 관측 (보조 소거 진단의 대조 · 같은 관측 경로)',
              f'write_dump all custom ${{out}}/obs/end_pre_bot.dump {pcols} modify format "{pfmt}"',
              'dump ul_ew all local ${ul_big} ${out}/obs/end_post_wall_*.dump ' + ' '.join(f'c_ul_wh[{i}]' for i in range(1, 11)),
              f'dump_modify ul_ew first yes format "{wfmt}"', f'dump ul_ea all custom ${{ul_big}} ${{out}}/obs/end_post_atom_*.dump {hcols}',
              f'dump_modify ul_ea first yes format "{afmt}"', 'run 0', 'undump ul_ew', 'undump ul_ea',
              '# 보조 소거 (진단 · S0 복원 증명 아님 · §12-1 ④): 활성 compute 를 먼저 지운다 → 두 벽 unfix (판 · 바닥 이력 소거) → 진단 restart (UNread 가 새 프로세스로 읽는다)',
              'uncompute ul_wh', 'unfix zwall_top', 'unfix zwall_bot', 'write_restart ${out}/un_diag.bin',
              'print "UL_R_DONE bed=${ul_bed} end_step=${ul_step}"', '# <<< block r_start']
    else:
        L += ['# >>> block un_start — 보조 소거 진단 restart 를 새 프로세스로 · 같은 머리 (벽 다시 정의 = 이력 0 에서) · PRE · POST 관측 (진단 전용)']
        L += _freeze('ul_step', 'step') + _freeze('ul_na', 'atoms')
        L += ['print "UL_UN_START bed=${ul_bed} step=${ul_step} atoms=${ul_na}"',
              f'write_dump all custom ${{out}}/obs/un_pre_bot.dump {pcols} modify format "{pfmt}"',
              'dump ul_uw all local ${ul_big} ${out}/obs/un_post_wall_*.dump ' + ' '.join(f'c_ul_wh[{i}]' for i in range(1, 11)),
              f'dump_modify ul_uw first yes format "{wfmt}"', f'dump ul_ua all custom ${{ul_big}} ${{out}}/obs/un_post_atom_*.dump {hcols}',
              f'dump_modify ul_ua first yes format "{afmt}"', 'run 0', 'undump ul_uw', 'undump ul_ua',
              'print "UL_UN_DONE bed=${ul_bed} step=${ul_step}"', '# <<< block un_start']
    return '\n'.join(L) + '\n'


def _render_EXT(bed, kind, P):
    n = _deck_nums(bed, kind, P)
    start, run = (n['ext_start'], n['ext_run1']) if kind == 'EXT' else (n['ext_end1'], n['ext_run2'])
    L = _banner(bed, kind, P) + _head(P)
    L += ['# >>> block ext — 원 덱 출력 꼴 (atom · mesh · contact · restart 주기 = 원 PHASE 4) + 새 관측 (omega · 총힘)',
          f'variable ul_bed string {bed}', f'variable ul_atoms0 equal {_fmt(n["atoms"])}', 'compute ul_erot all erotate/sphere',
          f'variable ul_Ps equal {"" if P["Ps_sign"] == 1 else "-"}f_top_mesh[3]/0.0025/1000000',
          'thermo_style custom ' + P['records']['thermo_style'], f'thermo {_fmt(n["ext_thermo"])}']
    L += _freeze('ul_step', 'step') + _freeze('ul_na', 'atoms')
    L += [f'if "${{ul_step}} != {_fmt(start)}" then "print \'UL_ABORT reason=start_step step=${{ul_step}}\'" "quit"',
          'if "${ul_na} != ${ul_atoms0}" then "print \'UL_ABORT reason=start_atoms atoms=${ul_na} expect=${ul_atoms0}\'" "quit"',
          f'dump ul_xa all custom {_fmt(n["ext_atom"])} ${{out}}/post/atom_*.liggghts id type x y z radius vx vy vz c_strs[1] c_strs[2] c_strs[3] c_ke',
          f'dump ul_xm all mesh/stl {_fmt(n["ext_mesh"])} ${{out}}/post/mesh_*.stl top_mesh',
          f'dump ul_xc all local {_fmt(n["ext_contact"])} ${{out}}/post/contact_*.liggghts ' + ' '.join(f'c_cpl[{i}]' for i in range(1, 27)),
          f'dump ul_xo all custom {_fmt(n["ext_atom"])} ${{out}}/post/obs_*.dump id type x y z radius mass vx vy vz omegax omegay omegaz fx fy fz',
          'dump_modify ul_xo format "%d %d ' + ' '.join([P['dumps']['atom_format_float']] * 15) + '"',
          f'restart {_fmt(n["ext_restart"])} ${{out}}/restart/restart_ext_*.bin',
          'print "UL_EXT_START bed=${ul_bed} step=${ul_step} atoms=${ul_na}"', f'run {_fmt(run)}']
    L += _freeze('ul_step', 'step')
    L += ['# 끝 = 명시 write_restart (run 끝 자동 쓰기에 기대지 않는다 · 이력 시험 정보 ⓐ · CX2 §6)',
          'write_restart ${out}/restart/restart_ext_${ul_step}.bin', 'print "UL_EXT_DONE bed=${ul_bed} end_step=${ul_step}"', '# <<< block ext']
    return '\n'.join(L) + '\n'


def render(bed, kind, P=None):
    P = P or ul_lib.load_params()
    if (bed, kind) not in deck_names():
        raise SystemExit(f'⛔ 등록되지 않은 덱 {bed}/{kind}')
    if kind in ('R', 'UNread'):
        return _render_R(bed, kind, P)
    if kind in ('UK', 'UC'):
        return _render_noMove(bed, kind, P)
    if kind in ('EXT', 'EXT2'):
        return _render_EXT(bed, kind, P)
    return _render_U(bed, kind, P)


KIT_FILES = ('unload_params.json', 'ul_lib.py', 'ul_s3.py', 'ul_observers.py', 'ul_gates.py', 'make_unload_decks.py', 'ul_reader.py',
             'seal_kit.py', 'run_unload.sh', 'run_unload_ibb.sbatch')


def generated_files(P=None):
    """→ {상대 경로: 글자} (덱 64)."""
    P = P or ul_lib.load_params()
    return {path: render(b, k, P) for (b, k), path in deck_names().items()}


def write_all():
    P = ul_lib.load_params()
    files = generated_files(P)
    for path, text in files.items():
        full = os.path.join(HERE, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
    print(f'✓ 덱 {len(files)} 개 — {DECK_DIR}/')
    seal = os.path.join(HERE, 'seal_kit.py')
    if os.path.exists(seal):
        subprocess.run([sys.executable, '-I', seal, '--write'], check=True)


def check():
    P = ul_lib.load_params()
    bad = []
    for path, text in generated_files(P).items():
        full = os.path.join(HERE, path)
        if not os.path.exists(full) or open(full, encoding='utf-8').read() != text:
            bad.append(path)
    if bad:
        print(f'⛔ 커밋본 덱이 생성 결과와 다르다 ({len(bad)}): {bad[:5]}')
        return 1
    seal = os.path.join(HERE, 'seal_kit.py')
    rc = subprocess.run([sys.executable, '-I', seal, '--check'], capture_output=True, text=True) if os.path.exists(seal) else None
    if rc is None or rc.returncode != 0:
        print('⛔ SHA256SUMS 대조 실패' + (f'\n{rc.stdout}{rc.stderr}' if rc else ' (seal_kit.py 없음)'))
        return 1
    print(f'✓ check — 덱 {len(deck_names())} 개 = 생성 결과 · {rc.stdout.strip().splitlines()[-1]}')
    return 0


# ── selftest ─────────────────────────────────────────────────────────────────

def _lines(text):
    try:
        return ul_lib.logical_lines(text)
    except Exception:  # noqa: BLE001
        return []


def _idx(L, prefix, start=0):
    for i in range(start, len(L)):
        if L[i].startswith(prefix):
            return i
    return 10 ** 9


def _runs(L):
    return [x for x in L if x.split()[0] == 'run']


def physical(text):
    """덱 글자에서 물리 시간을 다시 계산한다 (ULR1-04 — 생성된 덱이 증거): dt · 창 W · 창 시간 · 이동 (A · B) · 유지 (최소 · 최대) · 표본 · thermo."""
    L = _lines(text)
    var = {}
    for x in L:
        w = x.split()
        if w[:1] == ['variable'] and len(w) >= 4 and w[2] in ('equal', 'index') and re.fullmatch(r'[-+0-9.eE]+', w[3]):
            var[w[1]] = float(w[3])
    dt = var.get('dt')
    out = {'dt': dt}
    for k in ('ul_W', 'ul_nA', 'ul_nB', 'ul_v', 'ul_k0min', 'ul_k0max', 'ul_wmin0', 'ul_wmax0', 'ul_postn', 'ul_sepreq', 'ul_ave_ne', 'ul_thermo',
              'ul_uc_steps'):
        out[k] = var.get(k)
    if dt and out['ul_W']:
        out['T_W'] = out['ul_W'] * dt
        out['dz_A'] = (out['ul_v'] or 0) * dt * (out['ul_nA'] or 0)
        out['dz_B'] = (out['ul_v'] or 0) * dt * (out['ul_nB'] or 0)
        out['hold'] = (out['ul_wmin0'] * out['T_W'] if out['ul_wmin0'] else None, out['ul_wmax0'] * out['T_W'] if out['ul_wmax0'] else None)
        out['ave_dt'] = out['ul_ave_ne'] * dt if out['ul_ave_ne'] else None
        out['thermo_dt'] = out['ul_thermo'] * dt if out['ul_thermo'] else None
    return out


def deck_sim(text, obs_fn, start_step, state=None, S2max=1e-5, cli=None, max_cmds=400000):
    """덱 제어문만 해석하는 작은 모의기 (입자 계산 없음 · 시험 전용 · ULKR-07 · 10 — 실제 생성 덱의 분기를 다시 검증한다).
    variable (equal = 공식 · ${} 는 정의 때 치환 · 꺼낼 때 %.15g) · string · index (먼저 정의되면 그대로) · if/then/elif/else · jump SELF · label · run · quit ·
    include (${ul_state} = state 줄 · ${ul_base} = S2 문턱) · fix ul_mv move/mesh (이동 중) · print (사건 · 단 · 창 기록 줄 수집) · write_restart (수집).
    창 run (이동 아님 · n > 0) 마다 obs_fn(k, w, phase, step) = {'P' (덱 MPa), 'Kt', 'Kr', 'Kti', 'nc', 'na', 'lk'} 를 꺼낸다.
    → {'events': [[...]], 'steps': [[...]], 'windows': [[...]], 'restarts': [step], 'moves': [(k, step)], 'result', 'aborted', 'n_cmds'}."""
    import math as _m
    L = ul_lib.logical_lines(text)
    Wd = [ul_lib.words(x) for x in L]
    labels = {w[1]: i for i, w in enumerate(Wd) if w[:1] == ['label']}
    var = {k: ('index', str(v)) for k, v in (cli or {}).items()}
    sim = {'step': start_step, 'moving': False, 'obs': obs_fn(None, 0, None, start_step), 'events': [], 'steps': [], 'windows': [], 'restarts': [],
           'moves': [], 'result': None, 'aborted': None, 'n_cmds': 0}

    def num(x):
        return '%.15g' % x

    def ev(expr):
        o = sim['obs']
        e = expr.replace('&&', ' and ').replace('||', ' or ')
        e = re.sub(r'f_ul_av\[(\d)\]', lambda mm: repr(float(o[('P', 'Kt', 'Kr')[int(mm.group(1)) - 1]])), e)
        e = e.replace('count(ul_t1,ul_c1)+count(ul_t2,ul_c2)+count(ul_t3,ul_c3)', repr(float(o['nc'])))
        e = e.replace('count(all,ul_bel)+count(all,ul_abv)', repr(float(o['lk'])))
        e = re.sub(r'\bstep\b', str(sim['step']), e)
        e = re.sub(r'\bke\b', repr(float(o['Kti'])), e)
        e = re.sub(r'\batoms\b', str(int(o['na'])), e)
        return float(eval(e, {'__builtins__': {}}, {'abs': abs, 'floor': _m.floor}))   # noqa: S307 — 생성 덱의 숫자 식 (시험 전용)

    def get(name):
        st, v = var[name]
        return num(ev(v)) if st == 'equal' else v

    def sub(s):
        return re.sub(r'\$\{(\w+)\}', lambda mm: get(mm.group(1)), s)

    def do(w):
        """명령 하나 → None (다음 줄) · ('jump', 줄) · ('quit',)."""
        c = w[0]
        if c == 'variable' and len(w) >= 4:
            if w[2] == 'equal':
                var[w[1]] = ('equal', sub(' '.join(w[3:])))
            elif w[2] == 'string':
                var[w[1]] = ('string', sub(' '.join(w[3:])))
            elif w[2] == 'index' and w[1] not in var:
                var[w[1]] = ('index', sub(w[3]))
        elif c == 'include':
            if w[1] == '${ul_state}':
                for k2, v2 in (state or {}).items():
                    var[k2] = ('string', str(v2)) if isinstance(v2, str) else ('equal', num(float(v2)))
            elif w[1] == '${ul_base}':
                var['ul_S2max'] = ('equal', num(S2max))
        elif c == 'if':
            branches, cur, conds, k = [], [], [w[1]], 3
            while k < len(w):
                if w[k] == 'elif':
                    branches.append(cur)
                    cur = []
                    conds.append(w[k + 1])
                    k += 2
                    continue
                if w[k] == 'else':
                    branches.append(cur)
                    cur = []
                    conds.append('1')
                else:
                    cur.append(w[k])
                k += 1
            branches.append(cur)
            for cond, br in zip(conds, branches):
                if ev(sub(cond)):
                    for cmd in br:
                        r = do(ul_lib.words(cmd))
                        if r is not None:
                            return r
                    break
        elif c == 'jump' and len(w) >= 3 and w[1] == 'SELF':
            return ('jump', labels[w[2]])
        elif c == 'quit':
            return ('quit',)
        elif c == 'fix' and len(w) >= 4 and w[3] == 'move/mesh':
            sim['moving'] = True
        elif c == 'unfix' and w[1] == 'ul_mv':
            sim['moving'] = False
        elif c == 'run':
            n = int(float(sub(w[1])))
            if n > 0:
                sim['step'] += n
                if sim['moving']:
                    sim['moves'].append((int(float(get('ul_k'))), sim['step']))
                else:
                    sim['obs'] = obs_fn(int(float(get('ul_k'))), int(float(get('ul_w'))) + 1, int(float(get('ul_phase'))), sim['step'])
        elif c == 'write_restart':
            sim['restarts'].append(sim['step'])
        elif c == 'print' and len(w) >= 4 and w[2] == 'append':
            row = sub(w[1]).split(',')
            for key, nm in (('events', 'ul_events.csv'), ('steps', 'ul_steps.csv'), ('windows', 'ul_windows.csv')):
                if w[3].endswith(nm):
                    sim[key].append(row)
        elif c == 'print' and 'UL_ABORT' in w[1]:
            sim['aborted'] = sub(w[1])
        return None

    pc = 0
    while pc < len(Wd) and sim['n_cmds'] < max_cmds:
        sim['n_cmds'] += 1
        r = do(Wd[pc])
        if r is None:
            pc += 1
        elif r[0] == 'jump':
            pc = r[1] + 1
        else:
            break
    sim['result'] = var.get('ul_result', ('string', None))[1]
    return sim


def selftest() -> int:
    fails = []

    def chk(name, cond, detail=''):
        try:
            ok = bool(cond() if callable(cond) else cond)
        except Exception as e:  # noqa: BLE001 — 빈 구현 · 예외도 실패
            ok, detail = False, f'{type(e).__name__}: {e}'
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)

    P = ul_lib.load_params()
    names = deck_names()
    D = {}
    for key in names:
        try:
            D[key] = render(*key, P=P)
        except Exception:  # noqa: BLE001
            D[key] = ''
    chk(f'GD1 덱 {len(names)} 개가 만들어진다 (침대 다섯 × 12 + 7:3 UT · Ut0 + 10:0 EXT · EXT2)', lambda: len(names) == 64 and all(D.values()))
    r8, r2 = ul_lib.r8_text(P), ul_lib.r2_text(P)
    for key, text in D.items():
        b, k = key
        tag = f'{b}/{k}'
        chk(f'GD2 {tag}: 채우지 않은 @…@ · 탭 · `$` 꼴 · 주소 / 사용자 이름 없음',
            lambda text=text: text and not re.search(r'@[A-Z0-9_]+@', text) and '\t' not in text and not re.search(r'\$(?!\{)', text)
            and not re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|lustre|/home/|yonghoon|ibb-master', text))
        chk(f'GD3 {tag}: run 사이 위험한 읽기 없음 (⑭a) · 얼림 (⑭b) · if 조건 숫자뿐',
            lambda text=text: text and ul_lib.scan_between_runs(text) == [] and ul_lib.unfrozen_lazy(text, LAZY_OK) == [] and ul_lib.bad_if_conditions(text) == [])
        chk(f'GD4 {tag}: 덱 숫자 = 표 (또는 r8 원 글자 · 구조 상수) — 표 밖 상수 없음', lambda b=b, k=k, text=text: text and _stray_numbers(b, k, text, P) == [])
        orig = r2 if b == 'ps_10_0_r45' else r8
        arm = k.split('_', 1)[1] if k.startswith(('U_', 'G_')) else ('UT' if k == 'UT' else None)
        arm_dt = P['protocol']['dt0'] * P['arms'][arm]['dt_factor'] if arm and P['arms'][arm]['dt_factor'] != 1.0 else None
        chk(f'GD5 {tag}: G0 (원 {"r2" if b == "ps_10_0_r45" else "r8"} 꼴의 S0 정의 ↔ 이 덱 머리) = PASS',
            lambda text=text, orig=orig, arm_dt=arm_dt: text and ul_gates.g0_compare(orig, text, arm_dt=arm_dt)['status'] == 'PASS')
    # 물리 창 (ULR1-04 · §13-4) — 생성된 UB · UT · UVa · UVb · UT3 덱에서 다시 계산
    b73 = 'ps_7_3_r45'
    ph = {a: physical(D[(b73, f'U_{a}')]) for a in PROD_ARMS}
    ph['UT'] = physical(D[(b73, 'UT')])
    T_W = P['protocol']['dt0'] * P['windows']['W0']
    for a, f in ph.items():
        hf = P['arms'][a]['hold_factor']
        chk(f'GD6 {a}: 창 물리 시간 = T_W ({T_W}) · W = T_W / dt ({f.get("ul_W")}) · Δz_A 2e-4 · Δz_B 5e-5 · 유지 {4 * hf}–{12 * hf} 창 · 표본 1e-4 s · thermo 5e-4 s',
            lambda f=f, hf=hf: abs(f['T_W'] - T_W) < 1e-15 and abs(f['dz_A'] - P['protocol']['dz_A']) < 1e-15 and abs(f['dz_B'] - P['protocol']['dz_B']) < 1e-15
            and abs(f['hold'][0] - 4 * hf * T_W) < 1e-15 and abs(f['hold'][1] - 12 * hf * T_W) < 1e-15
            and abs(f['ave_dt'] - 1e-4) < 1e-15 and abs(f['thermo_dt'] - 5e-4) < 1e-15)
    chk('GD6 UT · UVb (dt₀/2) 의 창 = 10,000 step (옛 "모든 dt 에 5,000" 이면 창 시간이 반 — S4 가 거짓 PASS · ULR1-04)',
        lambda: ph['UT']['ul_W'] == 10000 and ph['UVb']['ul_W'] == 10000 and ph['UB']['ul_W'] == 5000)
    uc = physical(D[(b73, 'UC')])
    chk('GD6 UC = 50,000 step × dt₀/dt (0.05 덱 s)', lambda: abs(uc['ul_uc_steps'] * uc['dt'] - 0.05) < 1e-15)
    # 멈춤 규칙 · 이어 돌림 (ULR1-05 ③ · §13-5)
    ut, ub = _lines(D[(b73, 'UT')]), _lines(D[(b73, 'U_UB')])
    chk('GD7 UT = R_M 에서 멈춤 (RM_STOP) · UB = R_M 뒤 분리 단계로 이어감', lambda: any('RM_STOP' in x for x in ut) and not any('RM_STOP' in x for x in ub)
        and any('variable ul_phase equal 2' in x for x in ub))
    u3 = _lines(D[(b73, 'U_UT3')])
    chk('GD7 R_M 에서 restart + 이어 돌릴 상태 파일 (단계 2 · k+1) 을 쓴다 — UTc = U_UT3 + 이 상태 (같은 팔의 후속 관측) · '
        'U 덱은 상태 파일을 맨 바깥에서 include (if 안 include = 3d5c00f input.cpp 845 ERROR) 하고 ul_resume 으로 갈린다',
        lambda: any(x.startswith('write_restart ${out}/restart/restart_RM_') for x in ut) and any('state_RM_' in x for x in ut)
        and 'include ${ul_state}' in u3 and 'if "${ul_resume} == 1" then "jump SELF ul_resumed"' in u3
        and u3.index('include ${ul_state}') < u3.index('if "${ul_resume} == 1" then "jump SELF ul_resumed"'))
    chk('GD3b 어느 덱에도 if 안 include 가 없다 (3d5c00f input.cpp 845–846 "Cannot use include command within an if command")',
        lambda: all(not any(x.startswith('if ') and re.search(r'"\s*include\s', x) for x in _lines(t)) for t in D.values()))
    g = _lines(D[(b73, 'G_UB')])
    chk('GD7 중력 팔: 첫 run 은 run 0 (같은 머리 · G1) · 그 뒤 fix gravi 제자리 교체 g_aux 9.81e-6 · NO_BRACKET 사건',
        lambda: _runs(g)[0] == 'run 0' and _idx(g, 'fix gravi all gravity 9.81e-06 vector 0.0 0.0 -1.0') > _idx(g, 'run 0')
        and any('NO_BRACKET' in x for x in g))
    # ── ULKR-07 (Q6 · 개정 3 §14-7) — 실제 생성 덱의 분리 · 재접촉 분기를 모의기로 실행 (Codex deck_control 반례 · 입자 계산 없음) ──
    def sim_u(deck, contacts5, ke5=(1e-8, 1e-8)):
        Pk = {0: 0.16, 1: 0.0025, 2: 0.0008, 3: 0.0006, 4: 0.0004}

        def obs(k, w, phase, step):
            if k is None:
                return {'P': 0.16, 'Kt': 1e-8, 'Kr': 1e-8, 'Kti': 1e-8, 'nc': 1, 'na': P['beds'][b73]['atoms'], 'lk': 11}
            nc = 1 if k <= 4 else (contacts5[w - 1] if (k == 5 and w <= len(contacts5)) else 0)
            kt, kr = ke5 if k == 5 else (1e-8, 1e-8)
            return {'P': Pk.get(k, 1e-8 if nc else 0.0), 'Kt': kt, 'Kr': kr, 'Kti': kt, 'nc': nc, 'na': P['beds'][b73]['atoms'], 'lk': 11}
        return deck_sim(deck, obs, P['beds'][b73]['s0'], S2max=1e-5)

    def evs(s, name):
        return [(int(e[1]), e[5]) for e in s['events'] if e[0] == name]
    ub_deck = D[(b73, 'U_UB')]
    s_norm = sim_u(ub_deck, [])
    chk('GD15 모의기 대조: 정상 경로 — 교차 k 2 · 확인 k 3 · 4 → R_M · k 5 에서 둘째 0 창에 분리 선언 · 분리 뒤 4 창 (선언 창부터) → DONE · 이동 k 1–5',
        lambda: s_norm['result'] == 'DONE' and evs(s_norm, 'CROSS') == [(2, 'first')] and evs(s_norm, 'RM') == [(4, 'ncross2')]
        and evs(s_norm, 'SEPARATED') == [(5, 'w2')] and evs(s_norm, 'POST_DONE') == [(5, 'w5')] and [k for k, _ in s_norm['moves']] == [1, 2, 3, 4, 5])
    s_rc = sim_u(ub_deck, [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    chk('GD15 ULKR-07 재접촉 (정상 유지 · Codex recontact_steady): w 2 분리 → w 4 재접촉 → 같은 높이 (k 5) 남은 예산에서 w 6 재분리 → 분리 뒤 4 창 → DONE (w 9) · k 6 으로 옮기지 않는다',
        lambda: s_rc['result'] == 'DONE' and evs(s_rc, 'SEPARATED') == [(5, 'w2'), (5, 'w6')] and evs(s_rc, 'RECONTACT') == [(5, 'n1')]
        and evs(s_rc, 'POST_DONE') == [(5, 'w9')] and max(k for k, _ in s_rc['moves']) == 5)
    s_ex = sim_u(ub_deck, [0, 0] + [1] * 20, ke5=(2e-5, 1e-8))
    chk('GD15 ULKR-07 재접촉 뒤 예산 (12 창) 안에 다시 못 섬 → 같은 높이에서 끝 SEP_INCOMPLETE (분리 미완료) · k 6 으로 옮기지 않는다 (옛 덱 = 다음 단 이동)',
        lambda: s_ex['result'] == 'SEP_INCOMPLETE' and max(k for k, _ in s_ex['moves']) == 5 and evs(s_ex, 'SEP_INCOMPLETE') == [(5, 'w12')])
    s_post = sim_u(ub_deck, [1] * 10 + [0, 0, 1, 0, 0, 0, 0, 0], ke5=(2e-5, 1e-8))
    chk('GD15 ULKR-07 예산 끝 (w 12) 선언 뒤 분리 뒤 창에서 재접촉 (w 13 · 예산 밖) → SEP_INCOMPLETE · 이동 없음',
        lambda: s_post['result'] == 'SEP_INCOMPLETE' and evs(s_post, 'SEPARATED') == [(5, 'w12')] and evs(s_post, 'RECONTACT') == [(5, 'n1')]
        and max(k for k, _ in s_post['moves']) == 5)
    s_q6 = sim_u(ub_deck, [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], ke5=(2e-5, 1e-8))
    chk('GD15 Q6 (가) 선언은 예산 안 (w 2 · 6 · 12 ≤ 12) · 분리 뒤 4 창은 예산 밖 별도 관측 (Codex post_budget — w 15 DONE 은 개정 3 에서 정상) · 이동 없음',
        lambda: s_q6['result'] == 'DONE' and evs(s_q6, 'SEPARATED') == [(5, 'w2'), (5, 'w6'), (5, 'w12')] and evs(s_q6, 'POST_DONE') == [(5, 'w15')]
        and len(evs(s_q6, 'RECONTACT')) == 2 and max(k for k, _ in s_q6['moves']) == 5)
    # ── ULKR-10 A (Q4 · 개정 3 §14-5) — 중력 팔: 첫 재평형 유지만 4–12 · 그 뒤 B 단 = 출처 팔 튜플 (덱별 표 · 모의기 실행) ──
    gtab = []
    for b in BEDS:
        for a in PROD_ARMS:
            hf = P['arms'][a]['hold_factor']
            deck = D[(b, f'G_{a}')]
            Bd = P['beds'][b]
            rstep = (Bd['s0'] or Bd['s0_candidates'][0]) + 300000
            st = {'ul_rstep': rstep, 'ul_k': 4, 'ul_phase': 2, 'ul_modeB': 1, 'ul_pz': Bd['h0'] + 0.00035, 'ul_lift': 0.00035, 'ul_ncross': 2,
                  'ul_xk': 2, 'ul_lk0': 11, 'ul_Pbar': 0.0004, 'ul_kind': 'B'}
            Pg = {0: 0.0015, 1: 0.0012, 2: 0.0008, 3: 0.0006, 4: 0.0004}

            def obs(k, w, phase, step, b=b):
                nc = 1 if (k is None or k <= 4) else 0
                return {'P': Pg.get(k, 0.0) if k is not None else 0.0015, 'Kt': 1e-8, 'Kr': 1e-8, 'Kti': 1e-8, 'nc': nc, 'na': P['beds'][b]['atoms'], 'lk': 11}
            s = deck_sim(deck, obs, rstep, state=st, cli={'ul_s0': rstep - 300000})
            nw = {int(r[2]): int(r[10]) for r in s['steps']}
            gtab.append((b, a, hf, nw.get(0), nw.get(1), 'fix gravi all gravity 9.81e-06 vector 0.0 0.0 -1.0' in _lines(deck), s['result']))
    chk('GD16 ULKR-10 A 중력 팔 덱별 표 (다섯 침대 × G_UB · G_UVa · G_UVb · G_UT3 = 20 덱 · 모의기): 중력 교체 뒤 첫 유지 (k 0) = 4 창 (4–12 · × 2 없음) · '
        '그 뒤 B 단 (k 1) = 출처 팔 튜플 (G_UB · G_UT3 = 4 · G_UVa · G_UVb = 8) · 중력 = g_aux 9.81e-6',
        lambda: len(gtab) == 20 and all(n0 == 4 and n1 == 4 * hf and gok and res == 'DONE' for _, _, hf, n0, n1, gok, res in gtab), detail=str(gtab[:4]))
    e1, e2 = _lines(D[('ps_10_0_r45', 'EXT')]), _lines(D[('ps_10_0_r45', 'EXT2')])
    chk('GD8 10:0 EXT: run 60000 · restart 50000 (3,650,000) · 끝 명시 write_restart (3,660,000 — 자동 쓰기에 기대지 않는다) · 시작 step 검사 3,600,000',
        lambda: 'run 60000' in e1 and any(x.startswith('restart 50000 ') for x in e1) and _idx(e1, 'write_restart ${out}/restart/restart_ext_') > _idx(e1, 'run 60000')
        and any('!= 3600000' in x for x in e1))
    chk('GD8 10:0 EXT2: 시작 step 검사 3,660,000 · run 50000 · 끝 명시 write_restart', lambda: any('!= 3660000' in x for x in e2) and 'run 50000' in e2
        and _idx(e2, 'write_restart ${out}/restart/restart_ext_') > _idx(e2, 'run 50000'))
    R = _lines(D[(b73, 'R')])
    chk('GD9 R: PRE write_dump (바닥 이력) 가 첫 run 앞 · run 0 → run 2000 · R_END 관측 · uncompute → unfix 두 벽 → un_diag.bin',
        lambda: _idx(R, 'write_dump all custom ${out}/obs/pre_bot.dump') < _idx(R, 'run ') and _runs(R)[:2] == ['run 0', 'run 2000']
        and _idx(R, 'uncompute ul_wh') < _idx(R, 'unfix zwall_top') < _idx(R, 'unfix zwall_bot') < _idx(R, 'write_restart ${out}/un_diag.bin'))
    chk('GD9 R: G2 원 형식 덤프 (atom · contact · mesh) = 기본 형식 (dump_modify format 없음 — 글자 대조)',
        lambda: all(not any(x.startswith(f'dump_modify {d} ') and 'format' in x for x in R) for d in ('ul_g2a', 'ul_g2c', 'ul_g2m')))
    # 기록 머리 = 표 · print 열 수
    for col, fname in (('windows_cols', 'ul_windows.csv'), ('steps_cols', 'ul_steps.csv'), ('events_cols', 'ul_events.csv')):
        chk(f'GD10 기록 {fname}: 머리 = 표 · 쓰는 print 마다 열 수 같음', lambda col=col, fname=fname: _records_ok(D[(b73, 'U_UB')], P['records'][col], fname))
    # thermo 머리 이름 = 표 (읽는 쪽이 이 이름만 쓴다 · LIGGGHTS thermo.cpp — c_ · v_ 는 ID 앞 8 글자)
    for k in ('R', 'U_UB', 'UC', 'G_UVb', 'UT'):
        chk(f'GD13 {k}: 덱 thermo_style 의 머리 이름 = 표 thermo_cols {P["records"].get("thermo_cols")}',
            lambda k=k: _thermo_header(D[(b73, k)]) == P['records']['thermo_cols'])
    # 옛 b · 동시 UV 제출 (ULR1-05 ① ②) — 덱 · 러너에 없다 (K8 이 전 키트를 다시 본다)
    chk('GD11 덱 어디에도 옛 띠 b (2 δ_num + r_int) 판정이 없다', lambda: not any(re.search(r'δ_num|r_int|\bband_b\b|ul_bband', t) for t in D.values()))
    rb = _read(os.path.join(HERE, RUNNER))
    sb = _read(os.path.join(HERE, SBATCH))
    chk('GD12 러너 · 래퍼: #SBATCH -n 6 ↔ "$MPIRUN" $MPIRUN_FLAGS -np "$NP" (기본 --oversubscribe --bind-to none · NP 6)',
        lambda: [x for x in sb.splitlines() if x.startswith('#SBATCH -n ')] == ['#SBATCH -n 6'] and 'NP=6' in sb
        and '"$MPIRUN" $MPIRUN_FLAGS -np "$NP" "$LMP"' in rb and 'MPIRUN_FLAGS=${MPIRUN_FLAGS:---oversubscribe --bind-to none}' in rb)
    chk('GD12 러너: 동시 UV 제출 줄이 없다 (for A in UB UV UT UC) · UV = 선택 판독 뒤', lambda: rb and not re.search(r'for\s+\w+\s+in\s+UB\s+UV', rb + sb))
    for p in (os.path.join(HERE, SBATCH), os.path.join(HERE, RUNNER)):
        chk(f'GD12 bash -n {os.path.basename(p)}', lambda p=p: os.path.exists(p) and subprocess.run(['bash', '-n', p], capture_output=True).returncode == 0)
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


def _read(p):
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''


_THERMO_KW = {'step': 'Step', 'atoms': 'Atoms', 'ke': 'KinEng', 'cpu': 'CPU', 'dt': 'Dt', 'time': 'Time', 'erotate': 'RotEng'}


def _thermo_header(text):
    """덱의 마지막 thermo_style custom → LIGGGHTS 가 찍을 머리 이름 (thermo.cpp: 내장 = 고정 이름 · c_ / f_ / v_ = ID 앞 8 글자)."""
    ts = [x for x in _lines(text) if x.startswith('thermo_style custom ')]
    if not ts:
        return None
    out = []
    for w in ts[-1].split()[2:]:
        out.append(w[2:][:8] if w[:2] in ('c_', 'f_', 'v_') else _THERMO_KW.get(w, '?' + w))
    return out


STRUCTURAL = {'0', '1', '2', '3', '4', '-1', '0.0', '1.0', '-1.0', '1000000', '0.0025', '26', '1e9', '1.0e9'}


def _stray_numbers(bed, kind, text, P):
    """덱의 숫자 낱말 중 표 · r8 원 글자 · 구조 상수 어디에도 없는 것 (주석 · 따옴표 안 글은 뺀다)."""
    allowed = set(STRUCTURAL) | set(table_numbers(bed, kind, P)) | _r8_numbers(P)
    bad = []
    for ln in ul_lib.logical_lines(text):
        if ln.startswith('print ') or ln.startswith('if '):
            body = re.sub(r"'[^']*'", '', ln)
        else:
            body = ln
        body = re.sub(r'\$\{\w+\}', '', body)
        body = re.sub(r'\b[cfv]_\w+\[\d+\]', '', body)
        for tok in re.findall(r'(?<![\w.\[])[-+]?\d+\.?\d*(?:[eE][-+]?\d+)?(?![\w\]])', body):
            if tok not in allowed and _norm(tok) not in {_norm(a) for a in allowed}:
                bad.append((ln[:80], tok))
    return bad


def _norm(tok):
    try:
        return repr(float(tok))
    except ValueError:
        return tok


_R8N = None


def _r8_numbers(P):
    global _R8N
    if _R8N is None:
        _R8N = set(re.findall(r'(?<![\w.])[-+]?\d+\.?\d*(?:[eE][-+]?\d+)?', ul_lib.r8_text(P)))
    return _R8N


def _records_ok(text, cols, fname):
    L = _lines(text)
    head = [x for x in L if x.startswith('print "' + ','.join(cols) + '" file ${out}/' + fname)]
    rows = [x for x in L if x.startswith('print ') and f'append ${{out}}/{fname}' in x]
    if len(head) != 1 or not rows:
        return False
    for x in rows:
        body = ul_lib.words(x)[1]
        if len(body.split(',')) != len(cols):
            return False
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description='DEM 언로딩 키트 K2 덱 생성기')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--check', action='store_true')
    g.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.check:
        return check()
    if a.selftest:
        return selftest()
    write_all()
    return 0


if __name__ == '__main__':
    sys.exit(main())
