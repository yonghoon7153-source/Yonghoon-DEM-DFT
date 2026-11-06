"""압축 체크포인트에서 이어 돈 침대 (D0.7 · 11-03 재개) 의 로그 둘을 한 압밀 곡선으로 잇는다 — 읽기 전용 · 새 정의 없음.

쓰는 곳: run_draft2_metrics.py `--log B --log-stitch A:S` (1저자 11-05 "d0.7 관련해서 … parameter 추출들 진행해봐").
- A = 체크포인트 S 를 쓴 실행의 로그 — 정착 끝 PLATE HEIGHT 한 줄 · PHASE 3 머리 · 압축 run 들 (S 를 담은 run 은 끝까지 있어야 한다).
- B = 체크포인트 S 에서 이어 돈 실행의 로그 — PHASE 3 머리 · 첫 run = S → (A 에서 S 를 담은 run 의 끝 step) · 그 뒤 5000 step run ·
  PHASE 4 · 끝 줄 (재개 도구 Q3 (나) = 첫 판정이 원 판정 격자에 맞도록 `run 2` 같은 짧은 run).
- 이음 = A 의 압축 행 중 step ≤ S + B 의 압축 행.  S 뒤 A 행 = 취소된 실행의 나머지 → 버리고 개수 · 범위를 기록한다.
- 판정 줄 (Current Pressure) = A 에서 S 를 담은 run 앞 run 들의 판정 + B 의 판정 전부 (S 를 담은 run 의 판정 = B 의 첫 판정).
- 그 뒤 검사 · 행 계산 = make_fig_p2_aux.branches 와 같은 식 (판정 격자 5000 step · 목표 도달 · 예측 끝 판 높이 ↔ 끝 mesh ·
  이완 100,000 step · 끝 덤프 step) — 다른 점은 판정 수 = run 조각 수 − 1 (S 를 담은 run 이 A · B 두 조각) 하나뿐.
- 시험: `python3 -P docs/50kg/report_y4/draft2/log_stitch.py selftest` (실제 D2 · D3 로그로 같은 규칙 대조 + 합성 이음 양성 · 음성).
"""
import hashlib
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / 'figs'))
import kg50_y4_sources as src  # noqa: E402
import make_fig_p2_aux as P2  # noqa: E402

H3 = '====== PHASE 3: COMPRESSION (Speed 0.01) ======'
H4 = '====== PHASE 4: RELAXATION ======'
LOOP_STEPS = 5000
RELAX_STEPS = 100000
_PH = re.compile(r'^====== PLATE HEIGHT: ([0-9.eE+-]+) ======$', re.M)
_LOOP = re.compile(r'^Loop time of \S+ on \d+ procs for (\d+) steps')
_CP = re.compile(r'^Current Pressure: ([0-9.eE+-]+) MPa')


def events(seg):
    """구간 줄 → (run 들, 판정 값들).  run = setup step · 정규 행 [(step, pressMPa_sim)] · Loop 길이 · 앞선 판정 수.
    run · 행 규칙은 make_fig_p2_aux.parse_log 의 runs() 와 같다 (selftest ① 이 실제 로그로 대조)."""
    out, cur, in_run, cps = [], None, False, []
    for line in seg:
        if line.lstrip().startswith('Step') and 'pressMPa' in line:
            cur, in_run = dict(setup=None, rows=[], nsteps=None, cp_before=len(cps)), True
            out.append(cur)
            continue
        if line.startswith('Loop time of'):
            m = _LOOP.match(line)
            if in_run and m:
                cur['nsteps'] = int(m.group(1))
            in_run = False
            continue
        m = _CP.match(line)
        if m:
            cps.append(float(m.group(1)))
            continue
        mt = P2._THERMO.match(line) if in_run else None
        if mt:
            if cur['setup'] is None:
                cur['setup'] = int(mt.group(1))
            else:
                cur['rows'].append((int(mt.group(1)), float(mt.group(5))))
    return [r for r in out if r['rows']], cps


def parse_stitched(text_a, text_b, case, S):
    """A · B 로그 글 → make_fig_p2_aux.parse_log 꼴 (plate_z0_sim · runs3 · runs4 · current_press) + 이음 기록."""
    need = src.need
    tag = case.upper()
    need(isinstance(S, int) and S > 0, f'이음 step S = {S!r} — 양의 정수여야 한다')
    need(f'====== Simulation Finished! ({tag}:' in text_b, f'log B: {case} 끝 줄이 없다 (다른 침대 · 덜 끝난 로그?)')
    need('Simulation Finished!' not in text_a, 'log A 가 끝까지 돈 로그다 — 이을 일이 없다')
    pa, pb = _PH.findall(text_a), _PH.findall(text_b)
    need(len(pa) == 1, f'log A: PLATE HEIGHT 출력 줄 {len(pa)} 개 (1 개여야)')
    need(len(pb) == 0, f'log B: PLATE HEIGHT 출력 줄 {len(pb)} 개 (압축 재개 로그에는 없어야)')
    la, lb = text_a.split('\n'), text_b.split('\n')
    need(la.count(H3) == 1 and H4 not in la, f'log A: PHASE 3 머리 {la.count(H3)} 개 · PHASE 4 머리 {la.count(H4)} 개 (1 · 0 이어야)')
    need(lb.count(H3) == 1 and lb.count(H4) == 1, f'log B: PHASE 3 · 4 머리 {lb.count(H3)} · {lb.count(H4)} 개 (1 · 1 이어야)')
    i3a, i3b, i4b = la.index(H3), lb.index(H3), lb.index(H4)
    need(i3b < i4b, 'log B: 단계 순서')
    ra, cpa = events(la[i3a:])
    rb, cpb = events(lb[i3b:i4b])
    r4, _ = events(lb[i4b:])
    need(ra and rb and r4, f'run 없음 (A {len(ra)} · B 압축 {len(rb)} · B 이완 {len(r4)})')
    hold = [k for k, r in enumerate(ra) if any(st == S for st, _ in r['rows'])]
    need(len(hold) == 1, f'log A: step {S} 행을 가진 압축 run {len(hold)} 개 (1 개여야)')
    k = hold[0]
    rk = ra[k]
    end_a = rk['rows'][-1][0]
    need(rk['setup'] < S < end_a, f'S {S} 가 run 안쪽이 아니다 (setup {rk["setup"]} · 끝 {end_a}) — run 경계 이음은 이 도구 범위 밖')
    need(rk['nsteps'] == end_a - rk['setup'] == LOOP_STEPS, f'log A: S 를 담은 run 이 끝까지 돈 {LOOP_STEPS} step run 이 아니다 '
         f'(Loop {rk["nsteps"]} · 행 {rk["setup"]} → {end_a})')
    for j in range(k + 1):
        need(ra[j]['nsteps'] == LOOP_STEPS and ra[j]['rows'][-1][0] - ra[j]['setup'] == LOOP_STEPS,
             f'log A: 압축 run {j} 길이 {ra[j]["nsteps"]} (≠ {LOOP_STEPS})')
        need(ra[j]['cp_before'] == j, f'log A: run {j} 앞 판정 수 {ra[j]["cp_before"]} (≠ {j}) — run · 판정 순서가 어긋남')
    # (판정 줄 수 ≥ k 는 위 cp_before == j (j ≤ k) 가 이미 보장 — 따로 검사하지 않는다)
    b0 = rb[0]
    need(b0['setup'] == S, f'log B: 첫 압축 run 시작 {b0["setup"]} ≠ 이음 step {S}')
    need(b0['rows'][-1][0] == end_a and b0['nsteps'] == end_a - S,
         f'log B: 첫 run 끝 {b0["rows"][-1][0]} (Loop {b0["nsteps"]}) ≠ A 판정 격자 {end_a} — 판정 격자가 다르다')
    need(b0['cp_before'] == 0, f'log B: 첫 압축 run 앞에 판정 줄 {b0["cp_before"]} 개')
    for j in range(1, len(rb)):
        need(rb[j]['nsteps'] == LOOP_STEPS and rb[j]['rows'][-1][0] - rb[j]['setup'] == LOOP_STEPS,
             f'log B: 압축 run {j} 길이 {rb[j]["nsteps"]} (≠ {LOOP_STEPS})')
        need(rb[j]['cp_before'] == j, f'log B: run {j} 앞 판정 수 {rb[j]["cp_before"]} (≠ {j})')
    need(len(cpb) == len(rb), f'log B: 판정 줄 {len(cpb)} 개 ≠ 압축 run {len(rb)} 개')
    kept = [(st, p) for st, p in rk['rows'] if st <= S]
    dropped = [(st, p) for st, p in rk['rows'] if st > S] + [x for r in ra[k + 1:] for x in r['rows']]
    p_a = {st: p for st, p in rk['rows']}
    runs3 = ra[:k] + [dict(setup=rk['setup'], rows=kept, nsteps=None, cp_before=k)] + rb
    splice = dict(S=S, run_index_a=k, run_setup_a=rk['setup'], run_end=end_a, a_rows_kept=sum(len(r['rows']) for r in ra[:k]) + len(kept),
                  a_rows_dropped=len(dropped), a_dropped_first_step=dropped[0][0] if dropped else None,
                  a_dropped_last_step=dropped[-1][0] if dropped else None, a_checks_kept=k, a_checks_total=len(cpa),
                  b_compress_runs=len(rb), b_checks=len(cpb), a_p_at_S=p_a[S], a_p_at_run_end=p_a[end_a], b_p_at_run_end=b0['rows'][-1][1])
    return dict(plate_z0_sim=float(pa[0]), runs3=runs3, runs4=r4, current_press=cpa[:k] + cpb, splice=splice)


def rows_from(L, es, common, label, n_checks):
    """parse 결과 → (검사 통과 뒤) 가압 · 이완 행.  식 = make_fig_p2_aux.branches 그대로 (selftest ② 가 실제 로그로 대조)."""
    need = src.need
    v, dt = common['press_speed_sim'], common['dt']
    area_um2 = common['box_x_um'] * common['box_y_um']
    a = es['atoms']
    v_solid = float(np.sum(4.0 / 3.0 * np.pi * (a['r'] * src.LEN_SIM_TO_UM) ** 3))
    r3 = L['runs3']
    s0 = r3[0]['setup']
    s_end = r3[-1]['rows'][-1][0]
    cont = all(r3[i]['setup'] == r3[i - 1]['rows'][-1][0] for i in range(1, len(r3)))
    need(cont and s_end - s0 == LOOP_STEPS * n_checks, f'{label}: 압축 run 이음 · step 수 {s_end - s0} ≠ {LOOP_STEPS} × 판정 {n_checks}')
    tgt = common['target_MPa'] / src.P_SIM_TO_MPA
    cp = L['current_press']
    need(len(cp) == n_checks and cp[-1] >= tgt and all(c < tgt for c in cp[:-1]), f'{label}: Current Pressure 줄 ↔ 판정 수 · 목표 도달 대조 실패')
    z_end_pred = L['plate_z0_sim'] - v * dt * (s_end - s0)
    need(abs(z_end_pred - es['plate_z_sim']) <= 5e-7 * 1.0001, f'{label}: 예측 끝 판 높이 {z_end_pred} ↔ 끝 mesh {es["plate_z_sim"]}')
    r4 = L['runs4']
    need(r4 and r4[0]['setup'] == s_end, f'{label}: 이완 run 이 압축 끝 step 에서 시작하지 않는다')
    relax = [p for r in r4 for p in r['rows']]
    need(relax and relax[-1][0] == es['step'] and relax[-1][0] - s_end == RELAX_STEPS,
         f'{label}: 이완 끝 step {relax[-1][0] if relax else None} ↔ 끝 덤프 {es["step"]}')
    load = sorted({st: p for r in r3 for st, p in r['rows']}.items())
    need(len(load) == sum(len(r['rows']) for r in r3), f'{label}: 가압 행 step 이 겹친다 (이음 중복)')
    rows_load, rows_relax = [], []
    for st, p_sim in load:
        z_um = (L['plate_z0_sim'] - v * dt * (st - s0)) * src.LEN_SIM_TO_UM
        rows_load.append((st, p_sim * src.P_SIM_TO_MPA, z_um, 100.0 * (1.0 - v_solid / (area_um2 * z_um))))
    z_fix = es['plate_z_um']
    for st, p_sim in relax:
        rows_relax.append((st, p_sim * src.P_SIM_TO_MPA, z_fix, 100.0 * (1.0 - v_solid / (area_um2 * z_fix))))
    return dict(plate_z0_um=L['plate_z0_sim'] * src.LEN_SIM_TO_UM, s0=s0, s_end=s_end, n_runs=n_checks,
                z_end_pred_um=z_end_pred * src.LEN_SIM_TO_UM, z_end_mesh_um=es['plate_z_um'], v_solid_um3=v_solid,
                load=rows_load, relax=rows_relax, end_step=es['step'])


def branches_stitched(es, case, path_a, path_b, S, common, label='D0.7'):
    """make_fig_p2_aux.branches(...)[label] 와 같은 꼴 + log_a · splice."""
    raw_a, raw_b = Path(path_a).read_bytes(), Path(path_b).read_bytes()
    L = parse_stitched(raw_a.decode('utf-8', errors='strict'), raw_b.decode('utf-8', errors='strict'), case, S)
    need = src.need
    need(len(L['runs3']) == len(L['current_press']) + 1, f'{label}: 이음 run 조각 수 ≠ 판정 수 + 1')
    out = rows_from(L, es, common, label, len(L['current_press']))
    out.update(case=case, log=str(path_b), log_sha256=hashlib.sha256(raw_b).hexdigest(), log_bytes=len(raw_b),
               log_a=str(path_a), log_a_sha256=hashlib.sha256(raw_a).hexdigest(), log_a_bytes=len(raw_a), splice=L['splice'])
    return out


# ───────────────────────────── 시험 ─────────────────────────────

def _thermo(step, press, atoms=1000, ke=1e-8, cpu=1.0):
    return f'{step:>8d} {atoms:>8d} {ke:>14.7g} {cpu:>14.7g} {press:>14.8g} '


def _run(setup, end, press_of, nsteps=None, loop=True):
    out = ['    Step    Atoms         KinEng            CPU       pressMPa ', _thermo(setup, 0.0, cpu=0)]
    st = (setup // 1000 + 1) * 1000
    while st < end:
        out.append(_thermo(st, press_of(st)))
        st += 1000
    out.append(_thermo(end, press_of(end)))
    if loop:
        out.append(f'Loop time of 1.0 on 4 procs for {nsteps if nsteps is not None else end - setup} steps with 1000 atoms')
    return out


def _synth(S=410000, s0=400002, s_stop=420002, target=0.3, tag='KG50_TEST_B50', pz=0.15, a_tail=1, b_first_end=None,
           a_ph=1, b_ph=0, a_phase4=False, drop_b_cp=False, early_target=False, relax=RELAX_STEPS, b_setup=None, a_loop_k=True):
    def p(st):                                   # 판 압력 (덱 단위 0.3 = 300 MPa) — 정지 판정에서만 목표 도달
        return min(0.29, 0.29 * max(st - s0, 0) / max(s_stop - s0, 1))
    a = ['header'] + ['====== PLATE HEIGHT: %r ======' % pz] * a_ph + [H3]
    runs_a = []
    st = s0
    while st < S + LOOP_STEPS * a_tail:
        e = st + LOOP_STEPS
        runs_a.append((st, e))
        st = e
    for i, (st, e) in enumerate(runs_a):
        lp = (a_loop_k or not (st < S < e))
        a += _run(st, e, p, loop=lp)
        a.append('Current Pressure: %r MPa (Target: %r)' % (p(e), target))
    if a_phase4:
        a.append(H4)
    b = ['header'] + ['====== PLATE HEIGHT: %r ======' % pz] * b_ph + [H3]
    e0 = next(e for st, e in runs_a if st < S < e) if b_first_end is None else b_first_end
    bs = S if b_setup is None else b_setup
    b += _run(bs, e0, p)
    cps = []
    st = e0
    runs_b = [(bs, e0)]
    while st < s_stop:
        runs_b.append((st, st + LOOP_STEPS))
        st += LOOP_STEPS
    for i, (st, e) in enumerate(runs_b):
        if i > 0:
            b += _run(st, e, p)
        val = target + 0.0004 if e >= s_stop else (target + 0.001 if (early_target and i == 1) else p(e))
        cps.append(val)
        if not (drop_b_cp and i == 1):
            b.append('Current Pressure: %r MPa (Target: %r)' % (val, target))
    b.append(H4)
    b += _run(s_stop, s_stop + relax, lambda s: 0.05)
    b.append(f'====== Simulation Finished! ({tag}: test) ======')
    return '\n'.join(a) + '\n', '\n'.join(b) + '\n', dict(S=S, s0=s0, s_stop=s_stop, pz=pz)


def selftest():
    fails = []

    def check(name, cond, extra=''):
        print(('  ✓ ' if cond else '  ✗ ') + name + (f' — {extra}' if extra and not cond else ''))
        if not cond:
            fails.append(name)

    def refused(name, fn, frag):
        """거부 + 거부 이유 (frag) 까지 맞아야 통과 — 다른 검사가 대신 막은 것은 실패 (변이 시험이 잡도록)."""
        try:
            fn()
        except Exception as e:                   # src.need → SourceError — 거부면 이유를 본다
            check(name, frag in str(e), f'이유가 다르다: {e}')
            return str(e)
        check(name, False, '거부되지 않았다')
        return None

    # ① 실제 완주 로그 (D2 · D3) — events() 의 run · 행 · 판정 = make_fig_p2_aux.parse_log
    repo = HERE.parents[3]
    for bed, rel, case in (('D2', 'docs/data/kg50_d2_end_20261030/kg50_d2_b50_log.liggghts', 'kg50_d2_b50'),
                           ('D3', 'docs/data/kg50_d3_cell_verdict_20261027/kg50_d3_b50_s1_log.liggghts', 'kg50_d3_b50_s1')):
        text = (repo / rel).read_text(encoding='utf-8')
        L0 = P2.parse_log(text, case)
        lines = text.split('\n')
        i3, i4 = lines.index(H3), lines.index(H4)
        r3, cp3 = events(lines[i3:i4])
        r4, _ = events(lines[i4:])
        same3 = [(r['setup'], r['rows']) for r in r3] == [(r['setup'], r['rows']) for r in L0['runs3']]
        same4 = [(r['setup'], r['rows']) for r in r4] == [(r['setup'], r['rows']) for r in L0['runs4']]
        check(f'① {bed} 실제 로그: 압축 run {len(r3)} · 이완 run {len(r4)} · 판정 {len(cp3)} = parse_log', same3 and same4 and cp3 == L0['current_press'])
        # ② 같은 parse 결과 → rows_from = make_fig_p2_aux.branches (가짜 끝 상태 = 로그가 예측한 끝 판 · 끝 step)
        n = len(L0['runs3'])
        common = dict(press_speed_sim=0.01, dt=1e-6, box_x_um=50.0, box_y_um=50.0, target_MPa=300.0)
        s0, s_end = L0['runs3'][0]['setup'], L0['runs3'][-1]['rows'][-1][0]
        zp = L0['plate_z0_sim'] - 0.01 * 1e-6 * (s_end - s0)
        atoms = dict(r=np.array([0.003, 0.0005, 0.00035]))
        es = dict(atoms=atoms, plate_z_sim=zp, plate_z_um=zp * src.LEN_SIM_TO_UM, step=L0['runs4'][-1]['rows'][-1][0])
        mine = rows_from(L0, es, common, bed, n)
        tmp = Path(__import__('tempfile').mkdtemp()) / 'log.liggghts'
        tmp.write_text(text, encoding='utf-8')
        ref = P2.branches({bed: dict(case=case, endstate=es)}, {bed: str(tmp)}, common)[bed]
        same = all(mine[k] == ref[k] for k in ('load', 'relax', 's0', 's_end', 'n_runs', 'plate_z0_um', 'z_end_pred_um', 'v_solid_um3'))
        check(f'② {bed} 같은 식: rows_from = make_fig_p2_aux.branches (가압 {len(ref["load"])} · 이완 {len(ref["relax"])} 행 · 비트 같음)', same)

    # ③ 합성 이음 — 양성
    common = dict(press_speed_sim=0.01, dt=1e-6, box_x_um=50.0, box_y_um=50.0, target_MPa=300.0)
    atoms = dict(r=np.array([0.003, 0.0005]))

    def es_for(meta, relax=RELAX_STEPS):
        zp = meta['pz'] - 0.01 * 1e-6 * (meta['s_stop'] - meta['s0'])
        return dict(atoms=atoms, plate_z_sim=zp, plate_z_um=zp * src.LEN_SIM_TO_UM, step=meta['s_stop'] + relax)

    def go(ta, tb, meta, es=None, S=None):
        La = parse_stitched(ta, tb, 'kg50_test_b50', meta['S'] if S is None else S)
        return La, rows_from(La, es or es_for(meta), common, 'T', len(La['current_press']))

    ta, tb, meta = _synth()
    La, out = go(ta, tb, meta)
    sp = La['splice']
    check('③ 합성 이음 통과: s0 400002 · 정지 420002 · 판정 4 · 조각 5', out['s0'] == 400002 and out['s_end'] == 420002 and out['n_runs'] == 4
          and len(La['runs3']) == 5, f'{out["s0"]} {out["s_end"]} {out["n_runs"]} {len(La["runs3"])}')
    check('③ A 의 S 뒤 행은 버림 (410002 – 415002 · 7 행) · 판정 A 1 + B 3', sp['a_rows_dropped'] == 7 and sp['a_dropped_first_step'] == 410002
          and sp['a_dropped_last_step'] == 415002 and sp['a_checks_kept'] == 1 and sp['b_checks'] == 3, repr(sp))
    steps = [r[0] for r in out['load']]
    check('③ 가압 행 = 400002 다음 – 420002 · 이음 자리 410000 → 410002 · 중복 없음', steps[0] == 401000 and steps[-1] == 420002
          and 410000 in steps and 410002 in steps and len(steps) == len(set(steps)))
    check('③ 이완 행 = 끝 step 520002 · ε 고정', out['relax'][-1][0] == 520002 and len({r[3] for r in out['relax']}) == 1)

    # ④ 음성 — 하나씩 어긋나게 · 거부 이유까지 대조 (검사 하나 = 시험 하나)
    import copy
    cp_line = re.compile(r'^Current Pressure: .*$', re.M)

    def drop_cp(text, which):                    # which = 0 (첫) · -1 (마지막) 판정 줄 지우기
        ms = list(cp_line.finditer(text))
        m = ms[which]
        return text[:m.start()] + text[m.end() + 1:]

    fin = '====== Simulation Finished! (KG50_TEST_B50: test) ======'
    refused('④ S 가 정수가 아님 (문자열)', lambda: go(ta, tb, meta, S='410000'), '양의 정수')
    refused('④ B 가 끝 줄 없는 로그', lambda: go(ta, tb.replace('Simulation Finished!', 'Simulation Stopped'), meta), '끝 줄이 없다')
    refused('④ 다른 침대 끝 줄', lambda: go(ta, tb.replace('KG50_TEST_B50', 'KG50_D1_B50'), meta), '끝 줄이 없다')
    refused('④ A 가 끝까지 돈 로그', lambda: go(ta + fin + '\n', tb, meta), 'log A 가 끝까지 돈')
    refused('④ A PLATE HEIGHT 2 줄', lambda: go(*_synth(a_ph=2)), 'log A: PLATE HEIGHT')
    refused('④ B 에 PLATE HEIGHT', lambda: go(*_synth(b_ph=1)), 'log B: PLATE HEIGHT')
    refused('④ A 에 PHASE 4 머리', lambda: go(*_synth(a_phase4=True)), 'log A: PHASE 3 머리')
    refused('④ B 에 PHASE 3 머리 둘', lambda: go(ta, tb.replace(H3, H3 + '\n' + H3, 1), meta), 'log B: PHASE 3 · 4 머리')
    tb_sw = tb.replace(H3, '@@3@@').replace(H4, H3).replace('@@3@@', H4)
    refused('④ B 단계 순서 뒤집힘', lambda: go(ta, tb_sw, meta), 'log B: 단계 순서')
    refused('④ B 이완 run 없음', lambda: go(ta, tb.split(H4)[0] + H4 + '\n' + fin + '\n', meta), 'run 없음')
    refused('④ S 가 A 행에 없음 (S = 410500)', lambda: go(ta, tb, meta, S=410500), '행을 가진 압축 run')
    refused('④ S = run 경계 (405002) — 범위 밖', lambda: go(ta, tb, meta, S=405002), '안쪽이 아니다')
    refused('④ A 에서 S 를 담은 run 이 덜 끝남 (Loop 줄 없음)', lambda: go(*_synth(a_loop_k=False)), 'S 를 담은 run 이 끝까지 돈')
    refused('④ A 첫 run 길이 4999', lambda: go(ta.replace('for 5000 steps', 'for 4999 steps', 1), tb, meta), 'log A: 압축 run 0 길이')
    refused('④ A 첫 판정 줄 빠짐', lambda: go(drop_cp(ta, 0), tb, meta), 'log A: run 1 앞 판정 수')
    refused('④ B 첫 run 시작 ≠ S', lambda: go(*_synth(b_setup=409000)), '첫 압축 run 시작')
    refused('④ B 첫 run 끝 ≠ A 판정 격자', lambda: go(*_synth(b_first_end=411002)), '판정 격자가 다르다')
    refused('④ B 첫 run 앞에 판정 줄', lambda: go(ta, tb.replace(H3, H3 + '\nCurrent Pressure: 0.0 MPa (Target: 0.3)', 1), meta),
            '첫 압축 run 앞에 판정 줄')
    refused('④ B 둘째 run 길이 4999', lambda: go(ta, tb.replace('for 5000 steps', 'for 4999 steps', 1), meta), 'log B: 압축 run 1 길이')
    refused('④ B 가운데 판정 줄 빠짐', lambda: go(*_synth(drop_b_cp=True)), 'log B: run 2 앞 판정 수')
    refused('④ B 마지막 판정 줄 빠짐', lambda: go(ta, drop_cp(tb, -1), meta), 'log B: 판정 줄')
    L_gap = copy.deepcopy(La)
    del L_gap['runs3'][2]
    refused('④ 가압 조각 하나 빠짐 (rows_from 직접)', lambda: rows_from(L_gap, es_for(meta), common, 'T', len(L_gap['current_press'])),
            '압축 run 이음')
    refused('④ 목표가 정지 전에 도달', lambda: go(*_synth(early_target=True)), 'Current Pressure 줄')
    es_bad = es_for(meta)
    es_bad = dict(es_bad, plate_z_sim=es_bad['plate_z_sim'] + 1e-6)
    refused('④ 예측 끝 판 높이 ≠ 끝 mesh', lambda: go(ta, tb, meta, es=es_bad), '예측 끝 판 높이')
    L_r4 = copy.deepcopy(La)
    L_r4['runs4'][0]['setup'] += 1
    refused('④ 이완 run 시작 ≠ 압축 끝 (rows_from 직접)', lambda: rows_from(L_r4, es_for(meta), common, 'T', len(L_r4['current_press'])),
            '이완 run 이 압축 끝')
    ta2, tb2, m2 = _synth(relax=90000)
    refused('④ 이완 길이 ≠ 100,000', lambda: go(ta2, tb2, m2, es=es_for(m2, relax=90000)), '이완 끝 step')
    refused('④ 끝 덤프 step ≠ 이완 끝', lambda: go(ta, tb, meta, es=dict(es_for(meta), step=520001)), '이완 끝 step')
    tb_dup = tb.replace(_thermo(412000, 0.29 * (412000 - 400002) / 20000), _thermo(412000, 0.29 * (412000 - 400002) / 20000) + '\n'
                        + _thermo(412000, 0.29 * (412000 - 400002) / 20000), 1)
    refused('④ B 에 같은 step 행 두 번', lambda: go(ta, tb_dup, meta), '가압 행 step 이 겹친다')
    print(f'log_stitch selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 0 if not fails else 1


if __name__ == '__main__':
    if sys.argv[1:] == ['selftest']:
        sys.exit(selftest())
    print(__doc__)
