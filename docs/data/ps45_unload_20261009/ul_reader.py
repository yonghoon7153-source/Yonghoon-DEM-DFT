#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 언로딩 키트 K4 — 읽는 쪽 (상태 기계 판독 · 선택 · 다음 제출 관문).  표준 라이브러리만 · 런 폴더를 읽기만 한다 (판정 JSON 만 쓴다).

    python3 ul_reader.py --selftest
    python3 ul_reader.py inputs  <root> <bed>            # in/ 원 파일 sha256 = 표 (rc 0 · 2)
    python3 ul_reader.py restore <root> <bed> [--hist <history_verdict.json>] [--job RJ|RJ2]
    python3 ul_reader.py kebase  <root> <bed>            # KE 기준 파일 <bed>/ul_base.in (S2 문턱 = 10 × (병진 + 회전))
    python3 ul_reader.py s0p     <root>                  # 10:0 이완 연장 S0′ / S0″ 결정 → ps_10_0_r45/s0_decision.json
    python3 ul_reader.py arm     <root> <bed> <job>      # 팔 판독 → <job>/arm_verdict.json
    python3 ul_reader.py select  <root>                  # 7:3 결정표 (§12-4 · §13-1) → ps_7_3_r45/selection.json
    python3 ul_reader.py gate    <root> <bed> <job>      # 그 잡을 지금 낼 수 있나 (rc 0 허용 · 2 거부 — 러너가 부른다)
    python3 ul_reader.py report  <root>                  # 다섯 침대 · 10 쌍 괄호 표 → report.json

폴더 (정본 이름 = README §0):  <root>/<침대>/in/ (원 파일) · RJ/ (Ut0 · R · UN · UK) · RJ2/ (10:0 S0′ 에서) · EXT/ · EXT2/ (10:0) ·
  <팔>/ (UB · UT · UC · UVa · UVb · UT3 · UTc · G_<팔>) · ul_base.in · s0_decision.json · selection.json.
판정 규칙 (등록 §12 · §13 · 권고 기본값 = docs/reviews/dem_unloading_kit_section13_appendix_draft_20261013.md):
  창 접촉 상태  CONTACT (벽 local 접촉 ≥ 1 · 창 평균 P > 0) · TENSION (≥ 1 · P ≤ 0) · ZERO (0) · OBS_MISSING (덤프 없음 · 깨짐 — 0 으로 세지 않는다)
  분리 선언    연속 두 ZERO 창의 둘째 창 끝 · 재접촉이면 계수 · 분리 뒤 창 · 표면 관측 초기화 (§13-3)
  상쇄 표지    교차 끝점 마지막 창의 인장 합 ≥ 0.5 · P_meas · A — 처분 = 진단값 (순위 · 10 쌍 표에서 미식별 · §13-3 Q2 (가))
  끝점 유효    덱 정상 (S1 ∧ S2 두 창) · S3 PASS · 유한 · (k* 는) NOISE_FLOOR 아님 · 접촉 (CONTACT · TENSION)
  교차         P̄ − P_meas 부호 바뀜 (> ↔ ≤) · 첫 교차 = 점 추정 (P 두 점 선형 보간) + 실제 괄호 · 비단조 = 모든 교차 괄호의 합집합 (§13-5 ①)
  상태 두 축   primary_status (주 측정 · 첫 교차 + 확인 두 단) ↔ trajectory_status (분리 · 표면 · 종료) — §13-2 TIMEOUT 세 경우
  선택         유효한 δ 두 개면 결정표 한 행 · 아니면 SELECTION_UNRESOLVED (NaN 은 ≤ 도 > 도 아니다 · §13-1)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ul_gates  # noqa: E402
import ul_lib  # noqa: E402
import ul_observers  # noqa: E402
import ul_s3  # noqa: E402

BEDS = ('ps_0_10_r45', 'ps_3_7_r45', 'ps_5_5_r45', 'ps_7_3_r45', 'ps_10_0_r45')
B73, B100 = 'ps_7_3_r45', 'ps_10_0_r45'
ARM_JOBS = ('UB', 'UT', 'UC', 'UVa', 'UVb', 'UT3', 'UTc', 'G_UB', 'G_UVa', 'G_UVb', 'G_UT3')
TUPLE_ARM = {'t1': 'UB', 't2': 'UVa', 't3': 'UT3', 't4': 'UVb'}
EPS_PP = 1e-9          # δ 경계 비교 — 부동소수 반올림 허용 (%p · choice C13)
WALL_U = ('mesh', 'tri', 'id', 'fnx', 'fny', 'fnz')                                         # compute wall/gran/local id force_normal
WALL_R = ('mesh', 'tri', 'id', 'fnx', 'fny', 'fnz', 'deltaMax', 'shearx', 'sheary', 'shearz')  # id history force_normal → 열 순서 = id · fn · history


# ── 구현 (아래 selftest 를 먼저 썼다) ─────────────────────────────────────────

_f = ul_lib.fnum


def _i(x):
    v = _f(x)
    return int(round(v)) if v is not None else None


def _csv(path, cols):
    """→ (행 dict 목록 · 문제 목록) — 머리 = 표 · 열 수 다른 줄은 버리지 않고 문제로 적는다."""
    if not os.path.exists(path):
        return None, [f'{os.path.basename(path)} 없음']
    lines = [ln for ln in open(path, encoding='utf-8', errors='replace').read().splitlines() if ln.strip()]
    pr = []
    if not lines or lines[0].split(',') != list(cols):
        pr.append(f'{os.path.basename(path)} 머리 ≠ 표')
        return [], pr
    out = []
    for n, ln in enumerate(lines[1:], 2):
        v = ln.split(',')
        if len(v) != len(cols):
            pr.append(f'{os.path.basename(path)}:{n} 열 수 {len(v)} ≠ {len(cols)}')
            continue
        out.append(dict(zip(cols, v)))
    return out, pr


def _supersede(rows):
    """이어 돌림: 실패한 시도가 이어 돌림 step 뒤에 남긴 줄 (같은 step 이 다시 나오기 전 줄) 을 버린다 → (남긴 줄 · 버린 수)."""
    kept, dropped = [], 0
    for r in rows:
        s = r.get('step')
        while s is not None and kept and kept[-1].get('step') is not None and kept[-1]['step'] >= s:
            kept.pop()
            dropped += 1
        kept.append(r)
    return kept, dropped


def read_run(d, P=None):
    P = P or ul_lib.load_params()
    R = P['records']
    out = {'dir': d, 'windows': [], 'steps': [], 'events': [], 'summary': None, 'problems': [], 'n_superseded_rows': 0, 'resume_steps': []}
    ev, pr = _csv(os.path.join(d, 'ul_events.csv'), R['events_cols'])
    out['problems'] += pr
    events = [{'event': r['event'], 'k': _i(r['k']), 'step': _i(r['step']), 'plate_z': _f(r['plate_z']), 'lift': _f(r['lift']),
               'detail': r['detail']} for r in (ev or [])]
    out['resume_steps'] = [e['step'] for e in events if e['event'] == 'RESUME']
    kept = []
    for e in events:   # RESUME 앞에 실패한 시도가 남긴 그 step 뒤 사건은 버린다
        if e['event'] == 'RESUME' and e['step'] is not None:
            kept = [x for x in kept if x['step'] is None or x['step'] <= e['step']]
        kept.append(e)
    out['events'] = kept
    for name, key, cols in (('ul_windows.csv', 'windows', R['windows_cols']), ('ul_steps.csv', 'steps', R['steps_cols'])):
        rows, pr = _csv(os.path.join(d, name), cols)
        out['problems'] += pr
        conv = []
        for r in rows or []:
            c = {}
            for k, v in r.items():
                c[k] = v if k in ('arm', 'bed', 'kind') else _f(v)
            for k in ('k', 'w', 'phase', 'step', 'n_windows', 'n_move', 'steady', 'modeB', 'n_contact_geo', 'n_contact_last', 'atoms', 'leak'):
                if k in c and c[k] is not None:
                    c[k] = int(round(c[k]))
            conv.append(c)
        conv, dropped = _supersede(conv)
        out[key] = conv
        out['n_superseded_rows'] += dropped
    sp = os.path.join(d, 'ul_summary.txt')
    out['summary'] = ul_lib.read_kv(sp) if os.path.exists(sp) else None
    return out


def window_states(windows, wall_by_step, P=None):
    """창마다 판 접촉 상태 — 벽 local 덤프 (창 끝) 의 접촉 수 · 창 평균 압력 (덱 → 보고 MPa) · 인장 합 (N · 판이 입자를 끌어올리는 쪽)."""
    P = P or ul_lib.load_params()
    sign = P['plate_fn_compressive_sign']
    scale = P['units']['report_MPa_per_Ps']
    out = []
    for w in windows:
        step = w.get('step')
        Pd = _f(w.get('Ps_avg'))
        Pr = Pd * scale if Pd is not None else None
        rows = wall_by_step.get(step)
        rec = {'step': step, 'P_MPa': Pr, 'n': None, 'tension_N': None, 'compress_N': None, 'n_geo': w.get('n_contact_geo')}
        if rows is None:
            rec['state'] = 'OBS_MISSING'
        else:
            fz = [_f(r.get('fnz')) for r in rows]
            if any(x is None for x in fz):
                rec['state'] = 'OBS_MISSING'
                out.append(rec)
                continue
            rec['n'] = len(rows)
            rec['tension_N'] = sum(abs(x) for x in fz if x * sign < 0)
            rec['compress_N'] = sum(abs(x) for x in fz if x * sign > 0)
            if not rows:
                rec['state'] = 'ZERO'
            elif Pr is None:
                rec['state'] = 'OBS_MISSING'
            else:
                rec['state'] = 'CONTACT' if Pr > 0 else 'TENSION'
        out.append(rec)
    return out


def separation(states, sepreq=2):
    """§13-3: 연속 sepreq 개 ZERO 창의 마지막 창 끝 = 분리 선언 · 그 창부터 분리 뒤 창 · 재접촉 (CONTACT · TENSION) 이면 계수 · 분리 뒤 창 초기화 ·
    OBS_MISSING 은 0 이 아니다 (연속을 끊는다 · 분리 뒤면 그 분리의 표면 관측도 끊긴다)."""
    out = {'declared_index': None, 'declared_step': None, 'recontact_index': [], 'missing_index': [], 'separated_final': False, 'post_windows': []}
    run, sep = 0, False
    for i, s in enumerate(states):
        st = s['state']
        if st == 'ZERO':
            run += 1
            if sep:
                out['post_windows'].append(i)
            elif run >= sepreq:
                sep = True
                out['declared_index'], out['declared_step'] = i, s['step']
                out['post_windows'] = [i]
            continue
        run = 0
        if st == 'OBS_MISSING':
            out['missing_index'].append(i)
        else:
            if sep:
                out['recontact_index'].append(i)
        if sep:
            sep = False
            out['post_windows'] = []
    out['separated_final'] = sep
    return out


def crossings(steps, Pm):
    """연속 두 단 (둘 다 유한 P) 의 P − P_meas 부호 바뀜 (> ↔ ≤) → [(i, j)]."""
    out = []
    for i in range(len(steps) - 1):
        a, b = steps[i]['P'], steps[i + 1]['P']
        if a is None or b is None:
            continue
        if (a > Pm) != (b > Pm):
            out.append((i, i + 1))
    return out


def interp_rho(a, b, Pm, h0_um):
    """두 단 (lift_um · P) 사이 P_meas 의 선형 보간 → (ρ %, 괄호 µm, 괄호 %) · 분모 0 · 비유한 = (None, …)."""
    la, lb, pa, pb = a['lift_um'], b['lift_um'], a['P'], b['P']
    br = [min(la, lb), max(la, lb)] if la is not None and lb is not None else None
    brp = [100.0 * x / h0_um for x in br] if br else None
    if None in (la, lb, pa, pb) or pa == pb:
        return None, br, brp
    hc = la + (pa - Pm) / (pa - pb) * (lb - la)
    return 100.0 * hc / h0_um, br, brp


def _wall_rows(path, cols=WALL_U):
    """창 끝 벽 local 덤프 → 접촉 목록 · 없음 · 깨짐 (머리 · 열 · 행 수 · 비유한) = None (OBS_MISSING — 0 으로 세지 않는다)."""
    if not os.path.exists(path):
        return None
    d = ul_lib.read_dump(path, 'local', [f'c_ul_wh[{c}]' for c in range(1, len(cols) + 1)])
    if not d['ok']:
        return None
    return [{n: r[f'c_ul_wh[{c}]'] for c, n in enumerate(cols, 1)} for r in d['rows']]


def _s0_frame(root, bed, P):
    """S0 원자 (in/atom_<S0>.liggghts — 10:0 은 s0_decision 의 S0′ 프레임) → (id 집합, 원자 목록, step)."""
    s0 = _bed_s0(root, bed, P)
    if s0 is None:
        return None, None, None
    cand = [os.path.join(root, bed, 'in', f'atom_{s0}.liggghts'), os.path.join(root, bed, 'EXT', 'post', f'atom_{s0}.liggghts'),
            os.path.join(root, bed, 'EXT2', 'post', f'atom_{s0}.liggghts')]
    for p in cand:
        if os.path.exists(p):
            d = ul_lib.read_dump(p, 'custom')
            if d['rows']:
                return {int(r['id']) for r in d['rows']}, d['rows'], s0
    return None, None, s0


def _bed_s0(root, bed, P):
    B = P['beds'][bed]
    if B['s0'] is not None:
        return B['s0']
    dec = _readjson(os.path.join(root, B100, 's0_decision.json')) if root else None
    return dec.get('s0') if dec and dec.get('status') == 'PASS' else None


def _readjson(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError):
        return None


def _s3_at(d, step, plate_z, s0_ids):
    ap, cp = os.path.join(d, 'dump', f'atom_{step}.dump'), os.path.join(d, 'dump', f'contact_{step}.dump')
    if s0_ids is None or not (os.path.exists(ap) and os.path.exists(cp)):
        return {'status': 'NOT_COMPUTED', 'why': ['S3 입력 덤프 · S0 집합 없음']}
    A = ul_lib.read_dump(ap, 'custom')
    C = ul_lib.read_dump(cp, 'local', [f'c_cpl[{c}]' for c in range(1, 27)])
    if not (A['rows'] and C['ok']):
        return {'status': 'NOT_COMPUTED', 'why': A['problems'][:2] + C['problems'][:2]}
    con = [{'id1': r['c_cpl[7]'], 'id2': r['c_cpl[8]'], 'fx': r['c_cpl[10]'], 'fy': r['c_cpl[11]'], 'fz': r['c_cpl[12]']} for r in C['rows']]
    return ul_s3.s3_residual(A['rows'], con, s0_ids, plate_z, atom_step=A['step'], contact_step=C['step'])


def _thermo(d):
    txt = ''
    for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if re.fullmatch(r'screen(_a\d+)?\.txt', name):
            txt += open(os.path.join(d, name), encoding='utf-8', errors='replace').read() + '\n'
    return ul_lib.parse_thermo(txt)


def deck_windows(deck_text):
    """생성된 덱 → 창 W (step) · dt (마지막 숫자 정의) · T_W = W · dt (ULR1-04 — 덱이 증거)."""
    var = {}
    for ln in ul_lib.logical_lines(deck_text):
        w = ln.split()
        if w[:1] == ['variable'] and len(w) >= 4 and w[2] in ('equal', 'index') and re.fullmatch(r'[-+0-9.eE]+', w[3]):
            var[w[1]] = float(w[3])
    W, dt = var.get('ul_W'), var.get('dt')
    return {'W': int(W) if W else None, 'dt': dt, 'T_W': W * dt if W and dt else None}


def arm_verdict(d, bed, job, P=None, root=None):
    """팔 런 폴더 → 판정 (§12-3 · §13-1 · §13-2 · §13-3 · §13-5) — 덱의 단 기록 + 창 끝 덤프 (벽 · 원자 · 쌍) + thermo."""
    P = P or ul_lib.load_params()
    root = root or os.path.dirname(os.path.dirname(d))
    run = read_run(d, P)
    Pm = P['P_meas_report_MPa']
    scale = P['units']['report_MPa_per_Ps']
    um = P['units']['um_per_deck_m']
    conf = P['protocol']['confirm_steps']
    h0_um = P['beds'][bed]['h0'] * um
    N_per_MPa = 0.0025 * 1e6 / scale   # 1 보고 MPa = 0.001 덱 MPa → 0.001 × 0.0025 m² × 1e6 = 2.5 N (덱 Ps 식의 A · 1e6)
    s0_ids, s0_atoms, _ = _s0_frame(root, bed, P)
    v = {'job': job, 'bed': bed, 'dir': d, 'problems': list(run['problems']), 'n_superseded_rows': run['n_superseded_rows'],
         'primary_status': None, 'rho_pct': None, 'bracket_um': None, 'bracket_pct': None, 'union_bracket_um': None, 'union_bracket_pct': None,
         'lower_bound_pct': None, 'nonmonotone': False, 'cancellation': None, 'disposition': None, 'rank_eligible': False,
         'endpoint_states': [], 'sigma_P': None, 'trajectory_status': None, 'separation': None, 's4_status': 'NOT_COMPUTED', 'why': []}
    gravity = job.startswith('G_')
    summ = run['summary']
    res = (summ or {}).get('result')
    v['trajectory_status'] = {'DONE': 'DONE', 'LIFT_CAP': 'LIFT_CAP', 'GUARD': 'GUARD', 'TECH': 'TECH', 'RM_STOP': 'RM_STOP'}.get(res, 'TIMEOUT')
    wins = run['windows']
    walls = {w['step']: _wall_rows(os.path.join(d, 'dump', f'wall_{w["step"]}.dump')) for w in wins if w.get('step') is not None}
    states = window_states(wins, walls, P)
    for st, w in zip(states, wins):
        st['k'] = w.get('k')
    steps = []
    for s in run['steps']:
        Pb = s.get('Pbar')
        steps.append({'k': s.get('k'), 'kind': s.get('kind'), 'step': s.get('step'), 'lift_um': (s['lift'] * um) if s.get('lift') is not None else None,
                      'plate_z': s.get('plate_z'), 'P': Pb * scale if Pb is not None else None, 'steady': s.get('steady') == 1,
                      'phase': s.get('phase')})
    last_state = {}
    for st in states:
        last_state[st['k']] = st

    def endpoint(i):
        s = steps[i]
        why = []
        if s['P'] is None or s['lift_um'] is None:
            why.append(f'단 {s["k"]} P̄ · 높이 비유한')
        if not s['steady']:
            why.append(f'단 {s["k"]} UNSTEADY (S1 ∧ S2 두 창 없음)')
        s3 = _s3_at(d, s['step'], s['plate_z'], s0_ids)
        s['s3'] = s3['status']
        if s3['status'] != 'PASS':
            why.append(f'단 {s["k"]} S3 {s3["status"]}')
        st = last_state.get(s['k'], {}).get('state')
        s['state'] = st
        if st not in ('CONTACT', 'TENSION'):
            why.append(f'단 {s["k"]} 판 접촉 {st}')
        return why

    # 첫 교차 (k ≥ 1 의 사다리 · 비유한 단을 사이에 둔 교차 = 끝점 무효)
    first, gap = None, False
    for j in range(1, len(steps)):
        pj = steps[j]['P']
        if pj is None:
            gap = True
            continue
        if pj <= Pm:
            pi = steps[j - 1]['P']
            first = ('gap', j) if (gap or pi is None) else ((j - 1, j) if pi > Pm else ('below', j))
            break
        gap = False
    nb = [e for e in run['events'] if e['event'] == 'NO_BRACKET']
    if gravity and nb:
        v['primary_status'] = 'NO_BRACKET'
        v['why'].append(f'중력 팔 재평형 뒤 P̄ ≤ P_meas · 분리 · 비정상 ({nb[0]["detail"]}) — 압력 · 높이 · 표면만 (§12-7)')
        first = None
    elif first and first[0] == 'gap':
        v['primary_status'] = 'UNIDENTIFIED'
        v['why'].append(f'교차 끝점 비유한 (단 {steps[first[1] - 1]["k"]} — NaN 은 ≤ 도 > 도 아니다)')
    elif first and first[0] == 'below':
        v['primary_status'] = 'UNIDENTIFIED'
        v['why'].append('출발 (k = 0 · 중력 팔 첫 유지) 부터 P̄ ≤ P_meas — 교차 없음')
    elif first:
        i, j = first
        why = endpoint(i) + endpoint(j)
        v['endpoint_states'] = [steps[i].get('state'), steps[j].get('state')]
        rho, br, brp = interp_rho(steps[i], steps[j], Pm, h0_um)
        v['rho_pct'], v['bracket_um'], v['bracket_pct'] = rho, br, brp
        # k* 의 σ_P — 그 단 마지막 두 창의 thermo 정규 줄 (창 범위 = 창 기록의 step)
        ws = sorted(w['step'] for w in wins if w.get('k') == steps[j]['k'] and w.get('step') is not None)
        if len(ws) >= 2:
            lo = ws[-2] - (ws[-1] - ws[-2])
            sg = ul_observers.sigma_P(_thermo(d)['regular'], [(lo, ws[-1])], ddof=P['noise_floor']['ddof'], min_n=P['noise_floor']['min_n'],
                                      col=P['records']['thermo_cols'][4], scale=scale)
            v['sigma_P'] = sg['sigma']
            nf = ul_observers.noise_floor(sg['sigma'], Pm, P['noise_floor']['factor'])
        else:
            nf = 'OBS_MISSING'
        if rho is None:
            why.append('보간 불가 (분모 0 · 비유한)')
        n_after = len(steps) - 1 - j
        if why:
            v['primary_status'] = 'UNIDENTIFIED'
            v['why'] += why
            v['rho_pct'] = None
        elif nf == 'NOISE_FLOOR':
            v['primary_status'] = 'NOISE_FLOOR'
            v['why'].append(f'P_meas < {P["noise_floor"]["factor"]} σ_P ({v["sigma_P"]})')
        elif nf != 'OK':
            v['primary_status'] = 'UNIDENTIFIED'
            v['why'].append(f'σ_P {nf}')
            v['rho_pct'] = None
        elif n_after < conf:
            v['primary_status'] = 'UNIDENTIFIED'
            v['why'].append(f'확인 단 {n_after} < {conf} (주 측정 미완료 · 하한 자동 발행 없음)')
            v['rho_pct'] = None
        else:
            v['primary_status'] = 'OK'
        # 비단조 — 모든 교차 괄호의 합집합 (§13-5 ① · b 판정 없음)
        cr = crossings(steps[1:], Pm)
        cr = [(a + 1, b + 1) for a, b in cr]
        v['nonmonotone'] = len(cr) > 1
        if cr:
            lifts = [steps[x]['lift_um'] for pair in cr for x in pair]
            v['union_bracket_um'] = [min(lifts), max(lifts)]
            v['union_bracket_pct'] = [100.0 * x / h0_um for x in v['union_bracket_um']]
        # 상쇄 — 교차 끝점 마지막 창의 인장 합 ≥ 0.5 · P_meas · A (힘)
        tens = [last_state.get(steps[x]['k'], {}).get('tension_N') for x in (i, j)]
        thr = 0.5 * Pm * N_per_MPa
        v['cancellation'] = any(t is not None and t >= thr for t in tens)
        v['cancellation_detail'] = {'tension_N': tens, 'threshold_N': thr}
    elif v['primary_status'] is None:
        # 교차 없음 — §13-2 ② · ③
        if v['trajectory_status'] in ('DONE',):
            v['primary_status'] = 'NO_CROSSING'
            v['why'].append('끝났는데 교차 없음')
        else:
            why = []
            ks = list(range(1, len(steps)))
            for x in ks:
                why += endpoint(x)
            mono = all(steps[x]['P'] is not None and steps[x - 1]['P'] is not None and steps[x]['P'] <= steps[x - 1]['P'] for x in ks)
            if not ks:
                why.append('정상 단 없음')
            if not mono:
                why.append('비단조 (교차 전) — 하한 전제 불충족')
            if why:
                v['primary_status'] = 'UNIDENTIFIED'
                v['why'] += why
            else:
                v['primary_status'] = 'LOWER_BOUND'
                v['lower_bound_pct'] = 100.0 * steps[ks[-1]]['lift_um'] / h0_um
    if steps and steps[0]['k'] == 0 and not steps[0]['steady'] and not gravity:
        v['primary_status'] = 'TECH'
        v['why'].append('k = 0 출발 비정상 (§7-1 TECH)')
    if res == 'TECH':
        v['primary_status'] = 'TECH'
    v['disposition'] = 'DIAGNOSTIC' if v['cancellation'] else ('VALUE' if v['primary_status'] == 'OK' else 'NONE')
    v['rank_eligible'] = v['primary_status'] == 'OK' and not v['cancellation']
    # 분리 · 분리 뒤 표면 (§13-3) · S4 (창 = 덱 물리 창 — 창 끝 프레임 사이)
    sep = separation(states, P['windows']['sep_declare'])
    v['separation'] = {k: sep[k] for k in ('declared_step', 'separated_final', 'recontact_index', 'missing_index')}
    v['separation']['n_post'] = len(sep['post_windows'])
    if sep['separated_final'] and sep['post_windows']:
        excl = ul_observers.s0_exclusion(s0_atoms, P['beds'][bed]['h0']) if s0_atoms else set()
        hs = []
        for idx in sep['post_windows'][:P['windows']['post_sep']]:
            stp = states[idx]['step']
            ad = ul_lib.read_dump(os.path.join(d, 'dump', f'atom_{stp}.dump'), 'custom')
            box = ((0.0, 0.05), (0.0, 0.05)) if not ad['box'] else (ad['box'][0], ad['box'][1])
            si = ul_observers.surface_index(ad['rows'], excl, box, grid=P['surface']['grid'], q=P['surface']['quantile'],
                                            method=P['surface']['quantile_method'], um=um) if ad['rows'] else {'status': 'NOT_COMPUTED', 'mean_um': None}
            hs.append(si['mean_um'])
        v['surface_um'] = hs
        s4 = [ul_observers.s4_check(a, b, P['steady']['S4_um_per_window']) for a, b in zip(hs, hs[1:])]
        v['s4_status'] = 'FAIL' if 'FAIL' in s4 else ('PASS' if s4 and all(x == 'PASS' for x in s4) else 'NOT_COMPUTED')
    if v['trajectory_status'] == 'DONE' and not (sep['separated_final'] and len(sep['post_windows']) >= P['windows']['post_sep']):
        v['why'].append('끝 = DONE 인데 판독기 분리 · 분리 뒤 창이 모자란다 (덱 기하 개수 ↔ 벽 덤프)')
    return v


def _valid_rho(vd):
    return vd is not None and vd.get('primary_status') == 'OK' and isinstance(vd.get('rho_pct'), float) and math.isfinite(vd['rho_pct'])


def _le(a, b):
    return a <= b + EPS_PP


def selection(v_ub, v_ut, v_uv=None, P=None):
    """§12-4 결정표 · §13-1 끝점 유효성 — 유효한 δ 둘이면 행 하나 · 아니면 SELECTION_UNRESOLVED (다음 팔 · 본 런 없음)."""
    P = P or ul_lib.load_params()
    lim = P['selection']['delta_max_pp']
    out = {'stage': None, 'delta_dt': None, 'delta_v': None, 'dt_star': None, 'tuple': None, 'arm': None, 'next': [], 'why': []}
    if v_ub is None or v_ut is None:
        out.update(stage='need_UB_UT', why=['UB · UT 판독 전'])
        return out
    if not (_valid_rho(v_ub) and _valid_rho(v_ut)):
        out['stage'] = 'SELECTION_UNRESOLVED'
        out['why'].append(f'끝점 무효 — UB {v_ub.get("primary_status")} · UT {v_ut.get("primary_status")} (δ_dt 없음)')
        return out
    d_dt = abs(v_ut['rho_pct'] - v_ub['rho_pct'])
    out['delta_dt'] = d_dt
    if not math.isfinite(d_dt):
        out.update(stage='SELECTION_UNRESOLVED', why=['δ_dt 비유한'])
        return out
    half = not _le(d_dt, lim)
    out['dt_star'] = 'dt0/2' if half else 'dt0'
    uvjob = 'UVb' if half else 'UVa'
    if v_uv is None:
        out.update(stage='need_UV', next=[uvjob])
        return out
    if v_uv.get('job') not in (None, uvjob):
        out.update(stage='SELECTION_UNRESOLVED', why=[f'UV 팔 {v_uv.get("job")} ≠ dt* 의 팔 {uvjob}'])
        return out
    ref = v_ut if half else v_ub
    if not _valid_rho(v_uv):
        out['stage'] = 'SELECTION_UNRESOLVED'
        out['why'].append(f'끝점 무효 — {uvjob} {v_uv.get("primary_status")} (δ_v 없음)')
        return out
    d_v = abs(v_uv['rho_pct'] - ref['rho_pct'])
    out['delta_v'] = d_v
    if not math.isfinite(d_v):
        out.update(stage='SELECTION_UNRESOLVED', why=['δ_v 비유한'])
        return out
    slow = not _le(d_v, lim)
    tup = {(False, False): 't1', (False, True): 't2', (True, False): 't3', (True, True): 't4'}[(half, slow)]
    out.update(stage='resolved', tuple=tup, arm=TUPLE_ARM[tup])
    return out


def _arm_v(root, bed, job, P):
    d = os.path.join(root, bed, job)
    if not os.path.isdir(d):
        return None
    try:
        return arm_verdict(d, bed, job, P, root=root)
    except Exception as e:  # noqa: BLE001 — 판독 실패 = 무효 끝점 (조용히 넘기지 않는다)
        return {'job': job, 'primary_status': 'UNIDENTIFIED', 'why': [f'판독 실패 {type(e).__name__}: {e}']}


def selection_state(root, P=None):
    P = P or ul_lib.load_params()
    ub, ut = _arm_v(root, B73, 'UB', P), _arm_v(root, B73, 'UT', P)
    s = selection(ub, ut, None, P)
    if s['stage'] == 'need_UV':
        uv = _arm_v(root, B73, s['next'][0], P)
        if uv is not None:
            s = selection(ub, ut, uv, P)
    return s


def _restored(root, bed, P):
    job = 'RJ2' if bed == B100 else 'RJ'
    r = _readjson(os.path.join(root, bed, job, 'restore_verdict.json'))
    return r is not None and r.get('status') == 'RESTORED', job


def _has_event(root, bed, job, name):
    run = read_run(os.path.join(root, bed, job))
    return any(e['event'] == name for e in run['events'])


def gate(root, bed, job, P=None):
    """다음 제출 관문 (§13-1 · §13-5 ② ③) → (허용?, 이유)."""
    P = P or ul_lib.load_params()
    if bed not in BEDS:
        return False, f'모르는 침대 {bed}'
    if job == 'RJ':
        return True, '복원 시험 (원 체크포인트 · 결과 0 건)'
    if job == 'EXT':
        if bed != B100:
            return False, 'EXT = 10:0 전용'
        r = _readjson(os.path.join(root, bed, 'RJ', 'restore_verdict.json'))
        return (bool(r and r.get('status') == 'RESTORED'), '10:0 이완 연장 = 3,600,000 복원 관문 통과 뒤 (§12-11)')
    if job == 'RJ2':
        if bed != B100:
            return False, 'RJ2 = 10:0 전용 (S0′ 복원 · UK)'
        dec = _readjson(os.path.join(root, bed, 's0_decision.json'))
        return (bool(dec and dec.get('status') == 'PASS'), 'S0′ 결정 PASS 뒤 (§12-11 · F3 이면 없음)')
    ok, rj = _restored(root, bed, P)
    if not ok:
        return False, f'{rj} 복원 판정 RESTORED 전 (§12-1 ⑤ — 미확인 · 실패면 U 없음)'
    if not os.path.exists(os.path.join(root, bed, 'ul_base.in')):
        return False, 'KE 기준 파일 ul_base.in 없음 (kebase · UK 뒤)'
    if job == 'UC':
        return True, '무이동 대조 (dt₀ · 서로 독립)'
    if bed == B73:
        if job in ('UB', 'UT'):
            return True, '7:3 개발 팔 (UB · UT · UC 먼저 · 서로 독립 · §13-5 ②)'
        s = selection_state(root, P)
        if job in ('UVa', 'UVb'):
            if s['stage'] == 'need_UV' and s['next'] == [job]:
                return True, f'δ_dt {s["delta_dt"]} → dt* {s["dt_star"]} → {job}'
            return False, f'선택 단계 {s["stage"]} · 다음 {s["next"]} ({" · ".join(s["why"])}) — UV 는 UB · UT 끝점 판독 뒤 dt* 의 팔 하나만'
        if s['stage'] != 'resolved':
            return False, f'최종 튜플 없음 ({s["stage"]} · {" · ".join(s["why"])})'
        if job == 'UTc':
            ok = s['tuple'] == 't3' and _has_event(root, bed, 'UT', 'RM')
            return ok, f'튜플 {s["tuple"]} — UTc 는 결정표 3 행 (UT 채택) 일 때 UT 의 R_M 에서만 (§13-5 ③)'
        if job == 'UT3':
            return False, '7:3 의 t3 본 값 = UT + UTc (S0 에서 새 UT3 를 돌리지 않는다)'
        if job.startswith('G_'):
            src = 'UT' if s['tuple'] == 't3' else s['arm']
            ok = job == f'G_{s["arm"]}' and _has_event(root, bed, src, 'RM')
            return ok, f'중력 팔 = 최종 팔 {s["arm"]} 의 R_M (출처 {src}) 에서'
        return False, f'7:3 {job} — 개발 팔 순서 밖'
    s = selection_state(root, P)
    if s['stage'] != 'resolved':
        return False, f'7:3 최종 튜플 없음 ({s["stage"]}) — 나머지 넷 U 없음 (§13-1)'
    if job == s['arm']:
        return True, f'본 런 = 최종 튜플 {s["tuple"]} 의 팔 {job}'
    if job == f'G_{s["arm"]}':
        ok = _has_event(root, bed, s['arm'], 'RM')
        return ok, f'중력 팔 = {s["arm"]} 의 R_M 에서'
    return False, f'{bed} 는 최종 튜플 {s["tuple"]} 의 팔 {s["arm"]} 만 (민감도 미측정 · §12-5)'


def pair_table(verdicts):
    """10 쌍 — 유효 · 순위 자격 (상쇄 진단값 아님) 둘 다일 때만 괄호 (합집합) 비교 · 겹침 = 미구분 (동률 아님) · 아니면 UNIDENTIFIED."""
    out = []
    for i, a in enumerate(BEDS):
        for b in BEDS[i + 1:]:
            va, vb = verdicts.get(a) or {}, verdicts.get(b) or {}
            ok = all(x.get('primary_status') == 'OK' and x.get('rank_eligible') and x.get('union_bracket_pct') for x in (va, vb))
            if not ok:
                rel = 'UNIDENTIFIED'
            else:
                (a0, a1), (b0, b1) = sorted(va['union_bracket_pct']), sorted(vb['union_bracket_pct'])
                rel = 'OVERLAP' if (a0 <= b1 and b0 <= a1) else 'SEPARATED'
            out.append({'a': a, 'b': b, 'relation': rel})
    return out


def _screen_info(path):
    info = {'banner': False, 'git': False, 'errors': [], 'loops': [], 'resets': set(), 'markers': []}
    if not os.path.exists(path):
        info['errors'].append('화면 없음')
        return info
    for ln in open(path, encoding='utf-8', errors='replace').read().splitlines():
        if 'LIGGGHTS-PUBLIC 3.8.0' in ln:
            info['banner'] = True
            info['git'] = info['git'] or '3d5c00f' in ln
        if ln.startswith('ERROR') or 'Segmentation fault' in ln or 'MPI_ABORT' in ln:
            info['errors'].append(ln.strip())
        m = re.search(r'Loop time of [0-9.eE+-]+ on (\d+) procs', ln)
        if m:
            info['loops'].append(int(m.group(1)))
        m = re.match(r'Resetting (global|per-atom) state of Fix (\S+) Style (\S+) from restart file info', ln.strip())
        if m:
            info['resets'].add((m.group(2), m.group(3), m.group(1)))
        if ln.startswith('UL_'):
            info['markers'].append(ln.strip())
    return info


EXPECTED_RESETS = (('history_zwall_bot', 'property/atom', ('global', 'per-atom')), ('top_mesh', 'mesh/surface/stress', ('global',)),
                   ('n_neighs_mesh_top_mesh', 'property/atom', ('global', 'per-atom')),
                   ('tracker_top_mesh', 'contacthistory/mesh', ('global', 'per-atom')), ('contacthistory', 'contacthistory', ('global', 'per-atom')))


def restore_verdict(root, bed, job='RJ', hist=None, P=None):
    """§12-1 복원 판정 — G0 (러너가 실행 전 원 덱으로 남긴 g0.json) · reset 로그 · G1 · G2 · G2c · 판 mesh md5 · G3 · PRE = POST (바닥 이력) ·
    보조 소거 진단 (R_END ↔ UN) · 작은 침대 이력 시험 (H0–H5) → RESTORED · UNCONFIRMED · SYNTAX_FAIL · VALUE_MISMATCH."""
    P = P or ul_lib.load_params()
    B = P['beds'][bed]
    J = os.path.join(root, bed, job)
    R, UN = os.path.join(J, 'R'), os.path.join(J, 'UN')
    s0 = B['s0'] if bed != B100 else (P['ext_10_0']['start_step'] if job == 'RJ' else _bed_s0(root, bed, P))
    out = {'bed': bed, 'job': job, 's0': s0, 'checks': {}, 'status': None}
    si = _screen_info(os.path.join(R, 'screen.txt'))
    syntax = si['banner'] and si['git'] and not si['errors'] and si['loops'] and all(n == 6 for n in si['loops']) \
        and any(m.startswith('UL_R_DONE') for m in si['markers'])
    out['checks']['syntax'] = {'ok': bool(syntax), 'loops': si['loops'], 'errors': si['errors'][:3]}
    miss = [(f, s, k) for f, s, ks in EXPECTED_RESETS for k in ks if (f, s, k) not in si['resets']]
    out['checks']['reset_log'] = {'ok': not miss, 'missing': miss}
    g0 = _readjson(os.path.join(J, 'g0.json'))
    out['checks']['g0'] = {'ok': bool(g0 and g0.get('status') == 'PASS'), 'violations': (g0 or {}).get('violations')}
    scr = open(os.path.join(R, 'screen.txt'), encoding='utf-8', errors='replace').read() if os.path.exists(os.path.join(R, 'screen.txt')) else ''
    ref_g1 = B['g1'] if (bed != B100 or job == 'RJ') else None
    if ref_g1 is None and bed == B100:
        T = ul_lib.parse_thermo(_ext_log_text(root))
        row = T['regular'].get(s0)
        ref_g1 = f'{s0} {int(row["Atoms"])} {row["KinEng"]} 0 0' if row else None
    out['checks']['G1'] = ul_gates.g1_check(scr, ref_g1, s0) if ref_g1 else {'status': 'NOT_COMPUTED'}
    orig_atom = _orig_frame(root, bed, job, s0, 'atom', P)
    orig_con = _orig_frame(root, bed, job, s0, 'contact', P)
    orig_mesh = _orig_frame(root, bed, job, s0, 'mesh', P)
    g2a = os.path.join(R, 'g2', f'atom_{s0}.liggghts')
    g2c = os.path.join(R, 'g2', f'contact_{s0}.liggghts')
    g2m = os.path.join(R, 'g2', f'mesh_{s0}.stl')
    out['checks']['G2'] = ul_gates.g2_compare(g2a, orig_atom) if orig_atom and os.path.exists(g2a) else {'status': 'NOT_COMPUTED'}
    out['checks']['G2c'] = ul_gates.g2c_compare(g2c, orig_con) if orig_con and os.path.exists(g2c) else {'status': 'NOT_COMPUTED'}
    out['checks']['mesh_md5'] = {'status': 'PASS' if orig_mesh and os.path.exists(g2m) and ul_gates.mesh_md5_equal(g2m, orig_mesh) else 'FAIL'}
    log = _orig_log_text(root, bed, job, P)
    out['checks']['G3'] = ul_gates.g3_check(scr, log, s0) if log else {'status': 'NOT_COMPUTED'}
    pre = ul_lib.read_dump(os.path.join(R, 'obs', 'pre_bot.dump'), 'custom')
    posts = sorted(x for x in os.listdir(os.path.join(R, 'obs')) if x.startswith('post_atom_')) if os.path.isdir(os.path.join(R, 'obs')) else []
    post = ul_lib.read_dump(os.path.join(R, 'obs', posts[0]), 'custom') if posts else {'rows': []}
    out['checks']['pre_post'] = {'ok': _hist_equal(pre['rows'], post['rows'])}
    end = ul_lib.read_dump(os.path.join(R, 'obs', 'end_pre_bot.dump'), 'custom')
    un = ul_lib.read_dump(os.path.join(UN, 'obs', 'un_pre_bot.dump'), 'custom')
    seen = _erasure_seen(end['rows'], un['rows'])
    out['checks']['un_erasure'] = {'seen': seen}
    h = _readjson(hist) if hist else None
    hpass = None if h is None else (h.get('expected_all') is True or h.get('verdict') == 'PASS' or h.get('rc') == 0)
    out['checks']['history_test'] = {'pass': hpass, 'source': hist}
    prepost = all(out['checks'][k].get('status') == 'PASS' for k in ('G1', 'G2', 'G2c', 'mesh_md5', 'G3')) and out['checks']['pre_post']['ok']
    out['status'] = ul_gates.restoration_verdict(out['checks']['reset_log']['ok'], out['checks']['g0']['ok'], bool(syntax), prepost, hpass, seen)
    return out


def _orig_frame(root, bed, job, s0, kind, P):
    name = {'atom': f'atom_{s0}.liggghts', 'contact': f'contact_{s0}.liggghts', 'mesh': f'mesh_{s0}.stl'}[kind]
    for p in (os.path.join(root, bed, 'in', name), os.path.join(root, bed, 'EXT', 'post', name), os.path.join(root, bed, 'EXT2', 'post', name)):
        if os.path.exists(p):
            return p
    return None


def _orig_log_text(root, bed, job, P):
    if bed == B100 and job == 'RJ2':
        return _ext_log_text(root)
    p = os.path.join(root, bed, 'in', P['beds'][bed]['orig_log'])
    if os.path.exists(p):
        return open(p, encoding='utf-8', errors='replace').read()
    if bed == B73:
        return ul_lib.tgz_member(P['head_source']['r8_log_suffix'], None, P).decode('utf-8', 'replace')
    return None


def _ext_log_text(root):
    txt = ''
    for j in ('EXT', 'EXT2'):
        p = os.path.join(root, B100, j, 'screen.txt')
        if os.path.exists(p):
            txt += open(p, encoding='utf-8', errors='replace').read() + '\n'
    return txt


def _hist_cols(rows):
    return {int(r['id']): tuple(r.get(f'f_history_zwall_bot[{c}]') for c in range(1, 5)) for r in rows}


def _hist_equal(pre, post, rel=1e-12, floor=1e-18):
    """바닥 primitive 이력 PRE_SETUP = POST_SETUP (이력 시험과 같은 허용 — 상대 1e-12 · 절대 1e-18 덱 m)."""
    if not pre or not post:
        return False
    a, b = _hist_cols(pre), _hist_cols(post)
    if set(a) != set(b):
        return False
    for i in a:
        for x, y in zip(a[i], b[i]):
            if x is None or y is None or abs(x - y) > max(rel * abs(x), floor):
                return False
    return True


def _erasure_seen(end_rows, un_rows):
    """보조 소거 진단 — R_END 의 바닥 이력에 0 아닌 값이 있고 UN (소거 뒤 새 프로세스) 에서는 전부 0 이면 참."""
    if not end_rows or not un_rows:
        return None
    a, b = _hist_cols(end_rows), _hist_cols(un_rows)
    nz_end = any(any(x not in (None, 0.0) for x in v) for v in a.values())
    zero_un = all(all(x == 0.0 for x in v) for v in b.values())
    return bool(nz_end and zero_un)


def kebase(root, bed, P=None, write=True):
    """KE 기준 (choice C4): 병진 = 표 (원 로그 이완 끝 · 10:0 = EXT 로그 S0′) · 회전 = UK 창 평균의 중앙값 → S2 문턱 = 10 × 합 · 기준 파일."""
    P = P or ul_lib.load_params()
    B = P['beds'][bed]
    job = 'RJ2' if bed == B100 else 'RJ'
    trans = B['ke_base_trans']
    if bed == B100:
        dec = _readjson(os.path.join(root, B100, 's0_decision.json'))
        trans = dec.get('ke_trans') if dec else None
    rows, pr = _csv(os.path.join(root, bed, job, 'UK', 'ul_windows.csv'), P['records']['windows_cols'])
    rot = [_f(r['ke_rot_avg']) for r in rows or []]
    k = ul_observers.ke_base(trans, [x for x in rot] if rot and all(x is not None for x in rot) else [], P['steady']['S2_factor'])
    k['problems'] = pr
    if k['s2_limit'] is None:
        k['text'] = None
        return k
    k['text'] = (f'# KE 기준 (ul_reader.py kebase) — {bed} · 병진 {trans!r} J ({"EXT 로그 S0′" if bed == B100 else "표 · 원 로그 이완 끝"}) · '
                 f'회전 {k["rot"]!r} J (UK 창 평균 {len(rot)} 의 중앙값) · S2 문턱 = {P["steady"]["S2_factor"]} × 합\n'
                 f'variable ul_KEbase equal {k["base"]!r}\nvariable ul_S2max equal {k["s2_limit"]!r}\n')
    if write:
        with open(os.path.join(root, bed, 'ul_base.in'), 'w', encoding='utf-8') as f:
            f.write(k['text'])
    return k


def s0p_decision(root, P=None, write=True):
    """10:0 이완 연장 (REG §10 Q11 (가) · §12-11): S0′ = 3,650,000 조건 (EXT 로그) → 미달이면 S0″ = 3,700,000 (EXT2) → 그래도 미달 = F3."""
    P = P or ul_lib.load_params()
    x = P['ext_10_0']
    out = {'status': 'NOT_COMPUTED', 's0': None, 'tried': [], 'ke_trans': None}
    for job, s, end in (('EXT', x['s0p'], x['end1']), ('EXT2', x['s0pp'], x['end2'])):
        p = os.path.join(root, B100, job, 'screen.txt')
        if not os.path.exists(p):
            break
        c = ul_gates.s0p_condition(open(p, encoding='utf-8', errors='replace').read(), s, window=x['cond_window'], frac=x['cond_frac'],
                                   tail=x['tail_lines'])
        ck = os.path.exists(os.path.join(root, B100, job, 'restart', f'restart_ext_{s}.bin'))
        endck = os.path.exists(os.path.join(root, B100, job, 'restart', f'restart_ext_{end}.bin'))
        out['tried'].append({'job': job, 's0': s, 'condition': c['status'], 'max_rel': c.get('max_rel'), 'ckpt': ck, 'end_ckpt': endck})
        if c['status'] == 'PASS' and ck:
            out.update(status='PASS', s0=s, ke_trans=c['ke_base'])
            break
        out['status'] = 'FAIL'
    if out['status'] == 'FAIL' and len(out['tried']) == 2:
        out['status'] = 'F3'
    if write:
        with open(os.path.join(root, B100, 's0_decision.json'), 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
    return out


def inputs_check(root, bed, P=None):
    """in/ 원 파일 (체크포인트 · atom · contact · mesh) sha256 = 표 · 원 로그 · 원 마지막 조각 덱 있음."""
    P = P or ul_lib.load_params()
    B = P['beds'][bed]
    out = {'ok': True, 'files': {}}
    for key, rec in B['in_files'].items():
        p = os.path.join(root, bed, 'in', rec['file'])
        if not os.path.exists(p):
            out['files'][key] = 'missing'
            out['ok'] = False
            continue
        sh = ul_lib.sha256_file(p)
        out['files'][key] = 'ok' if sh == rec['sha256'] else f'sha256 {sh} ≠ 표'
        out['ok'] = out['ok'] and sh == rec['sha256']
    for key in ('orig_log', 'last_deck'):
        p = os.path.join(root, bed, 'in', B[key])
        out['files'][key] = 'ok (sha256 기록)' if os.path.exists(p) else 'missing'
        out['ok'] = out['ok'] and os.path.exists(p)
    return out


def report(root, P=None):
    P = P or ul_lib.load_params()
    s = selection_state(root, P)
    vs = {}
    for bed in BEDS:
        job = ('UTc' if s.get('tuple') == 't3' else s.get('arm')) if bed == B73 else s.get('arm')
        if job:
            vs[bed] = _arm_v(root, bed, job, P)
    return {'selection': s, 'beds': vs, 'pairs': pair_table({b: v for b, v in vs.items() if v})}


# ── 합성 런 폴더 (덱이 쓰는 꼴 그대로 · 시험 전용) ─────────────────────────────

def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def _chain_atoms(ids, plate_z, bad=False, m=1e-6, g=9.81):
    """S3 합성 — 총힘 0 인 원자 (bad = 무게의 10 % 알짜힘)."""
    rows = []
    for k, i in enumerate(ids):
        rows.append({'id': i, 'type': 3, 'x': 0.001 + 0.0005 * k, 'y': 0.002, 'z': min(plate_z * 0.5, 0.01) + 0.001 * k, 'radius': 0.0005,
                     'mass': m, 'vx': 0.0, 'vy': 0.0, 'vz': 0.0, 'omegax': 0.0, 'omegay': 0.0, 'omegaz': 0.0, 'fx': 0.0, 'fy': 0.0,
                     'fz': (0.1 * m * g if bad else 0.0)})
    return rows


def _chain_contacts(ids, m=1e-6, g=9.81):
    out = []
    for k in range(len(ids) - 1):
        f = m * g * (len(ids) - 1 - k)
        v = [0.0] * 26
        v[6], v[7] = float(ids[k]), float(ids[k + 1])
        v[9], v[10], v[11] = 0.0, 0.0, -f
        out.append({f'c_cpl[{c + 1}]': v[c] for c in range(26)})
    return out


ATOM_COLS = ['id', 'type', 'x', 'y', 'z', 'radius', 'mass', 'vx', 'vy', 'vz', 'omegax', 'omegay', 'omegaz', 'fx', 'fy', 'fz']


def _mk_arm(root, bed, job, spec, P):
    """spec = {'W', 'dt', 'steps': [{'lift_um', 'P', 'steady', 'nw', 'kind', 'phase', 'modeB', 'wall' (창마다 [fn_z N …] 또는 None) ,
    's3': 'ok' | 'bad', 'sigma': 보고 MPa}], 'summary': 결과 | None, 'events': [(이름, 단 번호, 설명)], 'post_surface': [(h_um …)] | None}."""
    d = os.path.join(root, bed, job)
    R = P['records']
    B = P['beds'][bed]
    h0 = B['h0']
    W, dt = spec['W'], spec['dt']
    s0 = spec.get('s0', B['s0'] or B.get('s0_candidates', [0])[0])
    th = spec.get('thermo', round(5e-4 / dt))
    step = s0
    wl, sl, el = [','.join(R['windows_cols'])], [','.join(R['steps_cols'])], [','.join(R['events_cols'])]
    head = '    Step    Atoms         KinEng        ul_erot          ul_Ps       pressMPa            CPU '
    thermo = []
    os.makedirs(os.path.join(d, 'dump'), exist_ok=True)
    el.append(f'START,0,{s0},{h0},0,s0')
    ids = [1, 2, 3, 4, 5]
    surf_i = 0

    def run_block(step0, n, Pd, sig):
        """LIGGGHTS run 하나의 화면 — 머리 · setup 줄 (step0) · thermo 주기 정규 줄 · Loop time."""
        thermo.append(head)
        thermo.append(f' {step0} 160417 1e-07 1e-08 {Pd:.12g} {abs(Pd):.12g} 0')
        for t in range(1, n // th + 1):
            noise = (sig / 1000.0) * (1 if t % 2 else -1)
            thermo.append(f' {step0 + t * th} 160417 1e-07 1e-08 {Pd + noise:.12g} {abs(Pd + noise):.12g} 0')
        thermo.append(f'Loop time of 1.0 on 6 procs for {n} steps with 160417 atoms')

    for k, st in enumerate(spec['steps']):
        lift = st['lift_um'] / 1000.0
        pz = h0 + lift
        n_move = st.get('n_move', 0 if k == 0 else (round(spec.get('dzA', 2e-4) / (spec.get('v', 0.01) * dt)) if st.get('kind') == 'A'
                                                       else round(spec.get('dzB', 5e-5) / (spec.get('v', 0.01) * dt))))
        Pd = st['P'] / 1000.0
        sig = st.get('sigma', 0.001)
        if n_move:
            run_block(step, n_move, Pd, 0.0)
        step += n_move
        for w in range(1, st['nw'] + 1):
            step0, step = step, step + W
            run_block(step0, W, Pd, sig)
            okw = 1 if (st['steady'] and w >= st['nw'] - 1) else 0
            walls = st.get('wall')
            wv = walls[w - 1] if isinstance(walls, list) and w - 1 < len(walls) else ('default' if walls is None else walls)
            if wv == 'missing':
                pass
            else:
                fns = [-(st['P'] * 2.5)] if wv == 'default' else wv
                rows = [{f'c_ul_wh[{c}]': v for c, v in zip(range(1, 7), (0.0, float(j % 2), float(100 + j), 0.0, 0.0, fz))} for j, fz in enumerate(fns)]
                ul_lib.write_local(os.path.join(d, 'dump', f'wall_{step}.dump'), step, [f'c_ul_wh[{c}]' for c in range(1, 7)], rows)
            nc = 0 if wv == 'missing' else (1 if wv == 'default' else len(wv))
            wl.append(f'U,{bed},{k},{w},{st.get("phase", 0)},{step},{pz},{lift},{Pd},1e-07,1e-08,1.1e-07,{okw},{okw},{okw},{nc},160417,11,1e-07')
            if st.get('surface') is not None:
                hs = st['surface'][surf_i] if isinstance(st['surface'], list) else st['surface']
                surf_i += 1
                atoms = []
                for ix in range(10):
                    for iy in range(10):
                        atoms.append({'id': 1000 + ix * 10 + iy, 'type': 3, 'x': 0.0025 + 0.005 * ix, 'y': 0.0025 + 0.005 * iy,
                                      'z': hs / 1000.0 - 0.0005, 'radius': 0.0005, 'mass': 1e-6, 'vx': 0.0, 'vy': 0.0, 'vz': 0.0, 'omegax': 0.0,
                                      'omegay': 0.0, 'omegaz': 0.0, 'fx': 0.0, 'fy': 0.0, 'fz': 0.0})
                ul_lib.write_custom(os.path.join(d, 'dump', f'atom_{step}.dump'), step, ATOM_COLS, atoms)
        steady = 1 if st['steady'] else 0
        Pbar = Pd if st.get('Pbar') is None else st['Pbar']
        sl.append(f'U,{bed},{k},{st.get("kind", "0")},{lift},{n_move},{step},{pz},{lift},{Pbar},{st["nw"]},{steady},{st.get("phase", 0)},'
                  f'{st.get("modeB", 0)},1')
        if st.get('surface') is None:
            ul_lib.write_custom(os.path.join(d, 'dump', f'atom_{step}.dump'), step, ATOM_COLS, _chain_atoms(ids, pz, bad=(st.get('s3') == 'bad')))
        ul_lib.write_local(os.path.join(d, 'dump', f'contact_{step}.dump'), step, [f'c_cpl[{c}]' for c in range(1, 27)], _chain_contacts(ids))
        for name, kk, det in spec.get('events', []):
            if kk == k:
                el.append(f'{name},{k},{step},{pz},{lift},{det}')
    _w(os.path.join(d, 'ul_windows.csv'), '\n'.join(wl) + '\n')
    _w(os.path.join(d, 'ul_steps.csv'), '\n'.join(sl) + '\n')
    _w(os.path.join(d, 'ul_events.csv'), '\n'.join(el) + '\n')
    _w(os.path.join(d, 'screen.txt'), 'LIGGGHTS-PUBLIC 3.8.0 (git 3d5c00f)\n' + '\n'.join(thermo) + '\n')
    if spec.get('summary'):
        _w(os.path.join(d, 'ul_summary.txt'), f'result={spec["summary"]}\narm={job}\nbed={bed}\n')
    if spec.get('deck'):
        _w(os.path.join(d, 'deck.liggghts'), spec['deck'])
    os.makedirs(os.path.join(root, bed, 'in'), exist_ok=True)
    s0f = os.path.join(root, bed, 'in', f'atom_{s0}.liggghts')
    if not os.path.exists(s0f):
        surf = [{'id': 1000 + i, 'type': 3, 'x': 0.0025, 'y': 0.0025, 'z': 0.05, 'radius': 0.0005, 'vx': 0.0, 'vy': 0.0, 'vz': 0.0} for i in range(100)]
        ul_lib.write_custom(s0f, s0, ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz'],
                            [{k2: a[k2] for k2 in ('id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz')} for a in _chain_atoms(ids, h0)] + surf)
    return d


def _ladder(lifts, Ps, steady=True, nw=4, **kw):
    """사다리 단 (k = 0 은 출발 P̄ 160) + 주어진 단들 (B 단)."""
    steps = [{'lift_um': 0.0, 'P': 160.0, 'steady': True, 'nw': 3, 'kind': '0', 'phase': 4}]
    for lift, p in zip(lifts, Ps):
        steps.append(dict({'lift_um': lift, 'P': p, 'steady': steady, 'nw': nw, 'kind': 'B', 'phase': 0, 'modeB': 1, 'n_move': 0}, **kw))
    return steps


def selftest() -> int:
    import tempfile
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
    import make_unload_decks as mk  # noqa: E402 — 생성된 덱에서 물리 창을 다시 읽는다 (ULR1-04)
    decks = {k: mk.render(B73, k, P) for k in ('U_UB', 'UT', 'U_UVa', 'U_UVb', 'U_UT3')}
    h0um = P['beds'][B73]['h0'] * 1000.0
    with tempfile.TemporaryDirectory() as root:
        # ── ULR1-02 측정 뒤 TIMEOUT (Codex state.json post_measurement_timeout) ──
        sp = {'W': 5000, 'dt': 1e-6, 'deck': decks['U_UB'],
              'steps': _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]),
              'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'summary': None}
        _mk_arm(root, B73, 'UB', sp, P)
        v = None
        try:
            v = arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root)
        except Exception:  # noqa: BLE001
            v = None
        chk('R1 ULR1-02 측정 뒤 TIMEOUT — 사다리 0.2 · 0.25 · 0.3 · 0.35 µm / 1.2 · 0.8 · 0.6 · 0.4 MPa · +2 확인 끝 · 분리 전 시간 끝 → '
            'primary OK · ρ = 0.2026077873428664 % · 실제 괄호 [0.2, 0.25] µm · trajectory TIMEOUT (옛 "ρ > 0.315 %" 하한 아님)',
            lambda: v['primary_status'] == 'OK' and abs(v['rho_pct'] - 0.2026077873428664) < 1e-12
            and abs(v['bracket_um'][0] - 0.2) < 1e-12 and abs(v['bracket_um'][1] - 0.25) < 1e-12 and v['trajectory_status'] == 'TIMEOUT')
        sp2 = dict(sp, steps=_ladder([0.2, 0.25, 0.3], [1.9, 1.6, 1.3]), events=[])
        _mk_arm(root, B73, 'UT', sp2, P)
        chk('R1 ULR1-02 교차 전 TIMEOUT · 마지막 정상 단까지 정상 · 접촉 · 단조 → LOWER_BOUND (ρ > ρ(0.3 µm)) · 점 추정 없음',
            lambda: (lambda u: u['primary_status'] == 'LOWER_BOUND' and u['rho_pct'] is None
                     and abs(u['lower_bound_pct'] - 100 * 0.3 / h0um) < 1e-12)(arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root)))
        sp3 = dict(sp, steps=_ladder([0.2, 0.25, 0.3], [1.9, 2.1, 1.3]), events=[])
        _mk_arm(root, B73, 'UVa', sp3, P)
        chk('R1 ULR1-02 교차 전 TIMEOUT 인데 비단조 (1.9 → 2.1) → 하한 자동 발행 안 함 = UNIDENTIFIED (사유 기록)',
            lambda: (lambda u: u['primary_status'] == 'UNIDENTIFIED' and u['lower_bound_pct'] is None and u['why'])(
                arm_verdict(os.path.join(root, B73, 'UVa'), B73, 'UVa', P, root=root)))
    with tempfile.TemporaryDirectory() as root:
        # ── ULR1-01 끝점 유효성 → 선택 → 다음 제출 (종단) ──
        def arm(job, lifts, Ps, **kw):
            sp = {'W': 5000 if job in ('UB', 'UVa') else 10000, 'dt': 1e-6 if job in ('UB', 'UVa') else 5e-7,
                  'steps': _ladder(lifts, Ps), 'events': [('CROSS', 1, 'first'), ('RM', 3, 'ncross2')], 'summary': 'DONE'}
            sp.update(kw)
            return _mk_arm(root, B73, job, sp, P)

        def rho_lifts(r):   # 교차를 원하는 ρ 로 놓는 사다리 (P 1.2 → 0.8 · 보간 = 두 단 가운데)
            mid = r / 100.0 * h0um
            return [mid - 0.025, mid + 0.025, mid + 0.075, mid + 0.125]

        Ps4 = [1.2, 0.8, 0.6, 0.4]
        cases = [('t1', 1.0, 1.04, 1.03, 'UB'), ('t2', 1.0, 1.04, 1.2, 'UVa'), ('t3', 1.0, 1.2, 1.22, 'UT3'), ('t4', 1.0, 1.2, 1.4, 'UVb')]
        for tup, rub, rut, ruv, want in cases:
            for j in ('UB', 'UT', 'UVa', 'UVb'):
                shutil.rmtree(os.path.join(root, B73, j), ignore_errors=True)
            arm('UB', rho_lifts(rub), Ps4)
            arm('UT', rho_lifts(rut), Ps4)
            s1 = None
            try:
                s1 = selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                               arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root), None, P)
            except Exception:  # noqa: BLE001
                s1 = None
            uvjob = 'UVa' if abs(rut - rub) <= 0.1 else 'UVb'
            base = rub if uvjob == 'UVa' else rut
            arm(uvjob, rho_lifts(ruv), Ps4, W=5000 if uvjob == 'UVa' else 10000, dt=1e-6 if uvjob == 'UVa' else 5e-7)
            s2 = None
            try:
                s2 = selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                               arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root),
                               arm_verdict(os.path.join(root, B73, uvjob), B73, uvjob, P, root=root), P)
            except Exception:  # noqa: BLE001
                s2 = None
            chk(f'R2 ULR1-01 결정표 {tup}: ρ_UB {rub} · ρ_UT {rut} → δ_dt {abs(rut - rub):.2f} → 다음 = {uvjob} (UB · UT 끝 뒤에만) · '
                f'ρ_UV {ruv} (기준 {base}) → 튜플 {tup} · 7:3 최종 팔 {want}',
                lambda s1=s1, s2=s2, uvjob=uvjob, tup=tup: s1['stage'] == 'need_UV' and s1['next'] == [uvjob]
                and s2['stage'] == 'resolved' and s2['tuple'] == tup)
        for j in ('UB', 'UT', 'UVa', 'UVb'):
            shutil.rmtree(os.path.join(root, B73, j), ignore_errors=True)
        arm('UB', rho_lifts(1.0), Ps4)
        arm('UT', rho_lifts(1.1), Ps4)
        arm('UVa', rho_lifts(1.1), Ps4)
        chk('R2 ULR1-01 경계 δ = 0.10 정확히 (ρ 1.0 ↔ 1.1 · 부동소수 0.10000000000000009) = ≤ 쪽 → dt* = dt₀ · δ_v 0.10 → t1 (UB)',
            lambda: selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                              arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root),
                              arm_verdict(os.path.join(root, B73, 'UVa'), B73, 'UVa', P, root=root), P)['tuple'] == 't1')
        # 무효 끝점 셋 — UT UNSTEADY · UT NaN · UV 무교차
        shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
        arm('UT', rho_lifts(1.04), Ps4, steps=_ladder(rho_lifts(1.04), Ps4, steady=False))
        chk('R3 ULR1-01 UT 끝점 UNSTEADY → δ_dt 없음 → SELECTION_UNRESOLVED · 다음 제출 없음 (UV 안 냄)',
            lambda: (lambda s: s['stage'] == 'SELECTION_UNRESOLVED' and s['next'] == [] and s['tuple'] is None)(
                selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                          arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root), None, P)))
        shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
        nan_steps = _ladder(rho_lifts(1.04), Ps4)
        nan_steps[2]['Pbar'] = 'nan'
        arm('UT', rho_lifts(1.04), Ps4, steps=nan_steps)
        chk('R3 ULR1-01 UT 끝점 P̄ = NaN (CSV "nan") → else 로 흘리지 않는다 → SELECTION_UNRESOLVED',
            lambda: selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                              arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root), None, P)['stage'] == 'SELECTION_UNRESOLVED')
        shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
        arm('UT', rho_lifts(1.04), Ps4)
        shutil.rmtree(os.path.join(root, B73, 'UVa'), ignore_errors=True)
        arm('UVa', [0.2, 0.25, 0.3, 0.35], [1.9, 1.8, 1.7, 1.6], events=[], summary='LIFT_CAP')
        chk('R3 ULR1-01 UV 무교차 (상한) → δ_v 없음 → SELECTION_UNRESOLVED (최종 튜플 없음 · 나머지 네 침대 U 없음)',
            lambda: (lambda s: s['stage'] == 'SELECTION_UNRESOLVED' and s['tuple'] is None)(
                selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                          arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root),
                          arm_verdict(os.path.join(root, B73, 'UVa'), B73, 'UVa', P, root=root), P)))
        chk('R3 NO_BRACKET 이름은 개발 팔 판정에 쓰지 않는다 (§13-1 — 중력 팔 전용)',
            lambda: 'NO_BRACKET' not in json.dumps(arm_verdict(os.path.join(root, B73, 'UVa'), B73, 'UVa', P, root=root)))
        # ── S3 · NOISE_FLOOR 가 끝점을 무효로 ──
        shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
        st = _ladder(rho_lifts(1.04), Ps4)
        st[2]['s3'] = 'bad'
        arm('UT', rho_lifts(1.04), Ps4, steps=st)
        chk('R4 교차 끝점 S3 FAIL (총힘 잔차 > 1e-3) → 끝점 무효 → primary UNIDENTIFIED (S3 사유) · 선택 UNRESOLVED',
            lambda: (lambda u: u['primary_status'] == 'UNIDENTIFIED' and 'S3' in ' '.join(u['why']))(
                arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root)))
        shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
        st = _ladder(rho_lifts(1.04), Ps4)
        st[2]['sigma'] = 0.5
        arm('UT', rho_lifts(1.04), Ps4, steps=st)
        chk('R4 k* 의 마지막 두 창 thermo σ_P 0.5 MPa (> P_meas / 3) → NOISE_FLOOR (주 값 아님 · 선택 UNRESOLVED)',
            lambda: (lambda u: u['primary_status'] == 'NOISE_FLOOR' and u['sigma_P'] > 0.4)(
                arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root)))
        # ── ULR1-05 결정표 3 행 → UTc 후속 산출물 · 다음 제출 관문 ──
        for j in ('UB', 'UT', 'UVa', 'UVb'):
            shutil.rmtree(os.path.join(root, B73, j), ignore_errors=True)
        _w(os.path.join(root, B73, 'RJ', 'restore_verdict.json'), json.dumps({'status': 'RESTORED'}))
        _w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
        arm('UB', rho_lifts(1.0), Ps4)
        chk('R5 관문: UB · UT 판독 전 UVa · UVb 거부 (동시 UV 제출 없음 · §13-5 ②)', lambda: not gate(root, B73, 'UVa', P)[0] and not gate(root, B73, 'UVb', P)[0])
        arm('UT', rho_lifts(1.2), Ps4)
        chk('R5 관문: δ_dt 0.2 → dt* = dt₀/2 → UVb 만 허용 · UVa 거부', lambda: gate(root, B73, 'UVb', P)[0] and not gate(root, B73, 'UVa', P)[0])
        arm('UVb', rho_lifts(1.22), Ps4, W=10000, dt=5e-7)
        chk('R5 ULR1-05 결정표 3 행 (UT 채택) → UTc (UT 의 R_M 에서 이어 돌림) 허용 · UT3 를 S0 에서 새로 (7:3) 거부 · G_UT3 허용 (R_M = UT)',
            lambda: gate(root, B73, 'UTc', P)[0] and not gate(root, B73, 'UT3', P)[0] and gate(root, B73, 'G_UT3', P)[0])
        chk('R5 다른 침대: 복원 전 거부 · 복원 뒤에는 최종 튜플의 팔 (UT3) 만 허용 · UB · UVa 거부',
            lambda: (not gate(root, 'ps_3_7_r45', 'UT3', P)[0]) and (_w(os.path.join(root, 'ps_3_7_r45', 'RJ', 'restore_verdict.json'), json.dumps({'status': 'RESTORED'})) or True)
            and (_w(os.path.join(root, 'ps_3_7_r45', 'ul_base.in'), 'x\n') or True)
            and gate(root, 'ps_3_7_r45', 'UT3', P)[0] and not gate(root, 'ps_3_7_r45', 'UB', P)[0] and not gate(root, 'ps_3_7_r45', 'UVa', P)[0])
        chk('R5 10:0: 이완 연장 결정 (S0′) 전 RJ2 · U 거부', lambda: not gate(root, B100, 'RJ2', P)[0] and not gate(root, B100, 'UT3', P)[0])
    with tempfile.TemporaryDirectory() as root:
        # ── ULR1-03 접촉 상태 · 상쇄 · 분리 · 창 결손 ──
        def wins(counts, pressures):
            return [{'step': 100 + i, 'Ps_avg': p / 1000.0, 'n_contact_geo': c} for i, (c, p) in enumerate(zip(counts, pressures))]

        def walls(counts):
            return {100 + i: (None if c == 'M' else [{'fnz': -1.0}] * c) for i, c in enumerate(counts)}

        s = None
        try:
            st = window_states(wins([2, 0, 0], [0.4, 0, 0]), walls([2, 0, 0]), P)
            s = separation(st, 2)
        except Exception:  # noqa: BLE001
            s = None
        chk('R6 ULR1-03 [2, 0, 0] (P 0.4 · 0 · 0) → CONTACT → (첫 0 창 = 대기) → 둘째 0 창 끝에 SEPARATED · TENSION 을 거치지 않는다',
            lambda: [x['state'] for x in st] == ['CONTACT', 'ZERO', 'ZERO'] and s['declared_index'] == 2 and s['declared_step'] == 102)
        chk('R6 ULR1-03 [0, 0, 1, 1] (P 0 · 0 · 0.2 · 0.2) → 둘째 창에 분리 → 셋째 창 재접촉 → 분리 계수 · 분리 뒤 창 · 표면 관측 초기화 (분리 미완료)',
            lambda: (lambda s2: s2['declared_index'] == 1 and s2['recontact_index'] == [2] and s2['separated_final'] is False
                     and s2['post_windows'] == [])(separation(window_states(wins([0, 0, 1, 1], [0, 0, 0.2, 0.2]), walls([0, 0, 1, 1]), P), 2)))
        chk('R6 ULR1-03 [0, 결손, 0] → OBS_MISSING 은 0 이 아니다 → 분리 선언 없음',
            lambda: (lambda st3: [x['state'] for x in st3] == ['ZERO', 'OBS_MISSING', 'ZERO'] and separation(st3, 2)['declared_index'] is None)(
                window_states(wins([0, 0, 0], [0, 0, 0]), walls([0, 'M', 0]), P)))
        chk('R6 ULR1-03 P ≤ 0 만으로 분리 아님 — 접촉 2 (+0.25 · −0.25 순힘 0) · P 0 → TENSION (분리 아님)',
            lambda: window_states(wins([2], [0.0]), {100: [{'fnz': -0.625}, {'fnz': 0.625}]}, P)[0]['state'] == 'TENSION')
        # 상쇄 +1.6 / −0.6 (Codex state.json pressure_positive_cancellation) — 종단: 런 폴더 → 판독
        Ps4 = [1.2, 1.0, 0.6, 0.4]
        canc = [-1.6 * 2.5, 0.6 * 2.5]
        st = _ladder([0.2, 0.25, 0.3, 0.35], Ps4)
        st[2]['wall'] = [canc] * 4
        st[2]['P'] = 1.0
        _mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': st, 'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'summary': 'DONE'}, P)
        chk('R7 ULR1-03 상쇄: 교차 끝점 압축 1.6 · 인장 0.6 MPa (순 1.0) → 접촉 상태 CONTACT · 상쇄 표지 참 (0.6 ≥ 0.5 · P_meas) · '
            '처분 = 진단값 (순위 밖) · 주 측정 자격은 따로 (세 칸)',
            lambda: (lambda u: u['endpoint_states'][-1] == 'CONTACT' and u['cancellation'] is True and u['rank_eligible'] is False
                     and u['disposition'] == 'DIAGNOSTIC')(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root)))
        # 비단조 (Codex live_nonmonotone_b_reference) — 첫 교차 점 추정 + 합집합 괄호 · b 없음
        _mk_arm(root, B73, 'UC', {'W': 5000, 'dt': 1e-6, 'steps': _ladder([1.0, 1.05, 1.1, 1.15], [1.2, 0.8, 1.3, 0.7]),
                                  'events': [('CROSS', 2, 'first')], 'summary': 'DONE'}, P)
        chk('R8 ULR1-05 ① 비단조 1.2 · 0.8 · 1.3 · 0.7 MPa → 첫 교차 ρ 0.9229910312286136 % · 비단조 표지 · 보고 괄호 = 교차 괄호 합집합 [1.0, 1.15] µm · b 판정 없음',
            lambda: (lambda u: abs(u['rho_pct'] - 0.9229910312286136) < 1e-12 and u['nonmonotone'] is True
                     and abs(u['union_bracket_um'][0] - 1.0) < 1e-12 and abs(u['union_bracket_um'][1] - 1.15) < 1e-12
                     and 'band_b' not in u and 'b_pp' not in u)(arm_verdict(os.path.join(root, B73, 'UC'), B73, 'UC', P, root=root)))
        # A 단 교차 = A 괄호 그대로 (되돌려 B 로 대체하지 않는다)
        stA = [{'lift_um': 0.0, 'P': 160.0, 'steady': True, 'nw': 3, 'kind': '0', 'phase': 4},
               {'lift_um': 0.2, 'P': 1.4, 'steady': True, 'nw': 4, 'kind': 'A', 'phase': 0, 'n_move': 0},
               {'lift_um': 0.4, 'P': 0.6, 'steady': True, 'nw': 4, 'kind': 'A', 'phase': 0, 'n_move': 0}]
        _mk_arm(root, B73, 'UVb', {'W': 10000, 'dt': 5e-7, 'steps': stA, 'events': [], 'summary': None}, P)
        chk('R8 A 단 교차 → 실제 괄호 = A 괄호 [0.2, 0.4] µm 그대로 (예정 Δz_B 아님 · §12-3)',
            lambda: (lambda u: abs(u['bracket_um'][0] - 0.2) < 1e-12 and abs(u['bracket_um'][1] - 0.4) < 1e-12)(
                arm_verdict(os.path.join(root, B73, 'UVb'), B73, 'UVb', P, root=root)))
    with tempfile.TemporaryDirectory() as root:
        # ── ULR1-04 물리 창 — 생성된 덱에서 다시 계산 · S4 반례 (표면 0.6 µm / 덱 s) ──
        dw = {}
        try:
            dw = {k: deck_windows(t) for k, t in decks.items()}
        except Exception:  # noqa: BLE001
            dw = {}
        chk('R9 ULR1-04 생성된 덱에서 창 물리 시간 다시 계산: UB 5,000 × 1e-6 · UT · U_UT3 · U_UVb 10,000 × 5e-7 = 0.005 덱 s (모두 같다)',
            lambda: all(abs(dw[k]['T_W'] - 0.005) < 1e-15 for k in decks) and dw['UT']['W'] == 10000 and dw['U_UVb']['W'] == 10000 and dw['U_UB']['W'] == 5000)

        def s4_case(deck_text, job):
            ww = deck_windows(deck_text)
            u = 0.6   # µm / 덱 s
            hs = [120.0 + u * ww['T_W'] * i for i in range(5)]   # 창 끝마다 · 창 시간 = 그 덱의 W × dt
            st = _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4])
            st.append({'lift_um': 0.4, 'P': 0.0, 'steady': True, 'nw': 5, 'kind': 'B', 'phase': 2, 'modeB': 1, 'n_move': 0,
                       'wall': [[]] * 5, 'surface': hs})   # 둘째 0 창에 분리 선언 → 분리 뒤 4 창 (선언 창 포함)
            _mk_arm(root, B73, job, {'W': ww['W'], 'dt': ww['dt'], 'steps': st, 'deck': deck_text,
                                     'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'summary': 'DONE'}, P)
            return arm_verdict(os.path.join(root, B73, job), B73, job, P, root=root)

        chk('R9 ULR1-04 S4 반례 — 생성된 U_UT3 덱 (창 10,000 step = 0.005 s) 에서 표면 0.6 µm/s = 0.003 µm/창 → S4 FAIL',
            lambda: s4_case(decks['U_UT3'], 'UT3')['s4_status'] == 'FAIL')
        bad_deck = decks['U_UT3'].replace('variable ul_W equal 10000', 'variable ul_W equal 5000')
        chk('R9 ULR1-04 판별력 — 옛 규약 (dt₀/2 에서도 5,000 step = 0.0025 s) 덱이면 0.0015 µm/창 → PASS 로 바뀐다 (그래서 덱에서 다시 계산한다)',
            lambda: s4_case(bad_deck, 'UVb')['s4_status'] == 'PASS')
    with tempfile.TemporaryDirectory() as root:
        # ── 이어 돌림 · 10 쌍 표 · KE 기준 · S0′ ──
        sp = {'W': 5000, 'dt': 1e-6, 'steps': _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]),
              'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'summary': 'DONE'}
        d = _mk_arm(root, B73, 'UB', sp, P)
        wpath = os.path.join(d, 'ul_windows.csv')
        L = open(wpath).read().splitlines()
        stale = [ln.split(',') for ln in L[1:] if ln.split(',')[2] == '2']
        resume_step = int([ln.split(',') for ln in L[1:] if ln.split(',')[2] == '1'][-1][5])
        extra = [','.join(r[:5] + [str(int(r[5]))] + r[6:8] + ['9.999'] + r[9:]) for r in stale[:2]]
        _w(wpath, '\n'.join(L[:1] + [ln for ln in L[1:] if int(ln.split(',')[5]) <= resume_step] + extra + L[1:][len([1 for ln in L[1:] if int(ln.split(',')[5]) <= resume_step]):]) + '\n')
        open(os.path.join(d, 'ul_events.csv'), 'a').write(f'RESUME,1,{resume_step},0.111252,0.0002,state\n')
        chk('R10 이어 돌림: 실패한 시도가 남긴 이어 돌림 step 뒤 창 줄 (P 9.999) 은 버리고 새 시도 줄만 쓴다 — 판독 같음 (ρ 0.2026…)',
            lambda: (lambda u: abs(u['rho_pct'] - 0.2026077873428664) < 1e-12 and u['n_superseded_rows'] == 2)(
                arm_verdict(d, B73, 'UB', P, root=root)))
        vs = {'ps_0_10_r45': {'primary_status': 'OK', 'union_bracket_pct': [1.0, 1.2], 'rank_eligible': True},
              'ps_3_7_r45': {'primary_status': 'OK', 'union_bracket_pct': [1.1, 1.3], 'rank_eligible': True},
              'ps_5_5_r45': {'primary_status': 'OK', 'union_bracket_pct': [1.4, 1.5], 'rank_eligible': True},
              'ps_7_3_r45': {'primary_status': 'OK', 'union_bracket_pct': [0.5, 0.6], 'rank_eligible': False},
              'ps_10_0_r45': {'primary_status': 'NOISE_FLOOR', 'union_bracket_pct': None, 'rank_eligible': False}}
        chk('R11 10 쌍 표: 괄호 겹침 = 미구분 (0:10 ↔ 3:7) · 분리 = 구분 (3:7 ↔ 5:5) · 상쇄 진단값 · 무효 침대 = 미식별 · 10 쌍 전부',
            lambda: (lambda t: len(t) == 10 and {(r['a'], r['b']): r['relation'] for r in t}[('ps_0_10_r45', 'ps_3_7_r45')] == 'OVERLAP'
                     and {(r['a'], r['b']): r['relation'] for r in t}[('ps_3_7_r45', 'ps_5_5_r45')] == 'SEPARATED'
                     and {(r['a'], r['b']): r['relation'] for r in t}[('ps_3_7_r45', 'ps_7_3_r45')] == 'UNIDENTIFIED'
                     and {(r['a'], r['b']): r['relation'] for r in t}[('ps_0_10_r45', 'ps_10_0_r45')] == 'UNIDENTIFIED')(pair_table(vs)))
        uk = os.path.join(root, B73, 'RJ', 'UK')
        _w(os.path.join(uk, 'ul_windows.csv'), ','.join(P['records']['windows_cols']) + '\n' + '\n'.join(
            f'UK,{B73},0,{w},4,{3200000 + 5000 * w},0.111052,0,0.16,2e-07,{r},0,-1,-1,-1,400,160417,11,2e-07' for w, r in ((1, 3e-8), (2, 1e-8), (3, 2e-8))) + '\n')
        chk('R12 KE 기준: 병진 = 표 (7:3 2.04e-07) · 회전 = UK 창 평균 셋의 중앙값 (2e-08) · S2 문턱 = 10 × 합 = 2.24e-06 · 기준 파일',
            lambda: (lambda k: abs(k['rot'] - 2e-8) < 1e-20 and abs(k['s2_limit'] - 2.24e-6) < 1e-18 and 'ul_S2max' in k['text'])(kebase(root, B73, P, write=False)))
        ext = os.path.join(root, B100, 'EXT')
        lines = ['    Step    Atoms         KinEng        ul_erot          ul_Ps       pressMPa            CPU ', ' 3600000 159152 3.5e-06 1e-07 0.3 0.3 0']
        lines += [f' {3600000 + 1000 * k} 159152 {1e-7 * (1 + (k % 5))} 1e-08 0.174 0.174 {k}' for k in range(1, 61)]
        lines.append('Loop time of 1 on 6 procs for 60000 steps with 159152 atoms')
        _w(os.path.join(ext, 'screen.txt'), '\n'.join(lines) + '\n')
        _w(os.path.join(ext, 'restart', 'restart_ext_3650000.bin'), 'x')
        _w(os.path.join(ext, 'restart', 'restart_ext_3660000.bin'), 'x')
        chk('R13 10:0 S0′: EXT 로그 ± 5,000 · 마지막 25 줄 1 % 안 → S0′ = 3,650,000 · KE 병진 기준 = 5 줄 창 평균 다섯의 중앙값 · 체크포인트 실재',
            lambda: (lambda s: s['status'] == 'PASS' and s['s0'] == 3650000 and abs(s['ke_trans'] - 3e-7) < 1e-18)(s0p_decision(root, P, write=False)))
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='DEM 언로딩 키트 K4 읽는 쪽')
    ap.add_argument('cmd', nargs='?', choices=['inputs', 'restore', 'kebase', 's0p', 'arm', 'select', 'gate', 'report'])
    ap.add_argument('args', nargs='*')
    ap.add_argument('--hist')
    ap.add_argument('--job', default='RJ')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.cmd:
        ap.error('명령 (또는 --selftest)')
    P = ul_lib.load_params()
    need = {'inputs': 2, 'restore': 2, 'kebase': 2, 's0p': 1, 'arm': 3, 'select': 1, 'gate': 3, 'report': 1}[a.cmd]
    if len(a.args) != need:
        ap.error(f'{a.cmd}: 인자 {need} 개')
    root = os.path.abspath(a.args[0])

    def dump(obj, path=None):
        txt = json.dumps(obj, ensure_ascii=False, indent=1, default=lambda o: sorted(o) if isinstance(o, set) else str(o))
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(txt + '\n')
        return txt

    if a.cmd == 'inputs':
        r = inputs_check(root, a.args[1], P)
        print(dump(r))
        return 0 if r['ok'] else 2
    if a.cmd == 'restore':
        r = restore_verdict(root, a.args[1], a.job, a.hist, P)
        dump(r, os.path.join(root, a.args[1], a.job, 'restore_verdict.json'))
        print(f'RESTORE_VERDICT bed={a.args[1]} job={a.job} status={r["status"]} ' +
              ' '.join(f'{k}={(v.get("status") or v.get("ok") or v.get("seen") or v.get("pass"))}' for k, v in r['checks'].items()))
        return 0 if r['status'] == 'RESTORED' else 2
    if a.cmd == 'kebase':
        k = kebase(root, a.args[1], P)
        print(f'KE_BASE bed={a.args[1]} trans={k["trans"]} rot={k["rot"]} s2_limit={k["s2_limit"]}')
        return 0 if k['s2_limit'] is not None else 2
    if a.cmd == 's0p':
        r = s0p_decision(root, P)
        print(f'S0P status={r["status"]} s0={r["s0"]} tried={r["tried"]}')
        return 0 if r['status'] == 'PASS' else 2
    if a.cmd == 'arm':
        bed, job = a.args[1], a.args[2]
        r = arm_verdict(os.path.join(root, bed, job), bed, job, P, root=root)
        dump(r, os.path.join(root, bed, job, 'arm_verdict.json'))
        print(f'ARM_VERDICT bed={bed} job={job} primary={r["primary_status"]} rho_pct={r["rho_pct"]} bracket_pct={r["bracket_pct"]} '
              f'trajectory={r["trajectory_status"]} cancellation={r["cancellation"]} nonmonotone={r["nonmonotone"]} why={" · ".join(r["why"])}')
        return 0
    if a.cmd == 'select':
        s = selection_state(root, P)
        dump(s, os.path.join(root, B73, 'selection.json'))
        print(f'SELECTION stage={s["stage"]} delta_dt={s["delta_dt"]} delta_v={s["delta_v"]} dt_star={s["dt_star"]} tuple={s["tuple"]} '
              f'arm={s["arm"]} next={s["next"]} why={" · ".join(s["why"])}')
        return 0
    if a.cmd == 'gate':
        ok, why = gate(root, a.args[1], a.args[2], P)
        print(f'GATE bed={a.args[1]} job={a.args[2]} {"ALLOW" if ok else "REFUSE"} — {why}')
        return 0 if ok else 2
    r = report(root, P)
    dump(r, os.path.join(root, 'report.json'))
    print(f'REPORT selection={r["selection"]["stage"]} tuple={r["selection"]["tuple"]} pairs={[(x["a"], x["b"], x["relation"]) for x in r["pairs"]]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
