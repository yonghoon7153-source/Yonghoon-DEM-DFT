"""L214 수정 A4 무영향 대조 — 정상 경우의 타깃 숫자는 비트 동일 · 메타 · 표시 변경은 따로 (수정 계획 docs/reviews/lhs214_fix_plan_20261014.md §3 A4).

기준 = 원격 본 가지 커밋 BASE (기본 0c557e72a — 이 수정 직전 · 봉인 CODE_FILES 32 code_fp e8b2496b… = 1087a9b2f 와 같은 봉인) 의 모듈 ↔ 지금 작업 트리.
읽기 전용 (리포에 쓰지 않는다 · 임시 폴더만 · git show / git archive 로 BASE 판을 읽는다).

  N  생산자 (scripts/network_conductivity.py) — 합성 침대 넷 × 두 모드 (`_run_all_networks` — 이온 · 전자 · 열 · H12) · real_14 (이온 run_decomposition ·
     세 채널 _run_all_networks) · case15 (음성 대조 — 실패 침대) · 격자 둘 (cg · spsolve) → 결과 JSON 전체가 L214 가 **더한** 기록 키 넷
     (electronic_ · thermal_ sigma_full_status · _reason) 만 빼면 같다 (float repr 왕복 = 비트 대조) · 더한 키는 따로 표
  T  τ 소비자 (scripts/tau_flux.py) — 커밋된 v1.2 τ 원천 194 케이스 (case_row 50 칸) · N 의 새 생산자 레코드 (ion_columns · 세대 계약 · 공용 기술 검사 ·
     증서 결합) · 옛 생산자 lhsx_054 진단 레코드 (Codex 묶음 — 사후 재분류 없음)
  R  배포 빌더 (scripts/lhs_release_build.py) — v1.2 인계표 130 + 64 행의 모든 칸 빈칸 뜻 · 관통 분류 · 상태 집계 · 주 타깃 관문
  W  웹앱 표 (webapp/app.py transform_network_summary_4col — 새 표 · 기존 CSV 표) — BASE 트리 ↔ 지금 트리를 따로 프로세스로: 정상 (두 모드 값 있음) ·
     비관통 = 같다 / Hertz 만 있는 옛 케이스 · 모형 한계 = L214-03 의도 변경 (따로 표)

실행:  python3 docs/reviews/lhs214_fix_evidence_20261015/a4_no_impact.py [--base REF] [--json OUT] [--skip-case15]
"""
import argparse
import contextlib
import gzip
import importlib.util
import io
import json
import math
import os
import subprocess
import sys
import tarfile
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SCRIPTS = os.path.join(ROOT, 'scripts')
WEBAPP = os.path.join(ROOT, 'webapp')
for _p in (SCRIPTS, WEBAPP):
    if _p not in sys.path:
        sys.path.insert(0, _p)
L214_ADDED = ('electronic_sigma_full_status', 'electronic_sigma_full_reason', 'thermal_sigma_full_status', 'thermal_sigma_full_reason')
GUARD_FIELDS = ('q_withheld', 'q_guard_max', 'guard_policy', 'sum_g')


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **kw)


def run_or_err(fn, *a, **kw):
    """결과 또는 예외 (실패 침대의 기대 거부도 기록 — BASE 와 같은 예외여야 한다)."""
    try:
        return canon(quiet(fn, *a, **kw))
    except Exception as e:                                       # noqa: BLE001
        return {'__error__': f'{type(e).__name__}: {e}'}


def git_bytes(*args):
    return subprocess.run(['git', '-C', ROOT] + list(args), capture_output=True, check=True, timeout=120).stdout


def load_base(base, rel, name, tmp):
    path = os.path.join(tmp, name + '.py')
    with open(path, 'wb') as fh:
        fh.write(git_bytes('show', f'{base}:{rel}'))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def canon(obj):
    return json.loads(json.dumps(obj, sort_keys=True, default=str))


def strip(obj, keys):
    o = canon(obj)

    def walk(x):
        if isinstance(x, dict):
            for k in keys:
                x.pop(k, None)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(o)
    return o


def leaves(x, out=None):
    out = out if out is not None else {'num': 0, 'str': 0, 'null': 0}
    if isinstance(x, dict):
        for v in x.values():
            leaves(v, out)
    elif isinstance(x, list):
        for v in x:
            leaves(v, out)
    elif isinstance(x, bool) or isinstance(x, str):
        out['str'] += 1
    elif isinstance(x, (int, float)):
        out['num'] += 1
    else:
        out['null'] += 1
    return out


def first_diff(a, b, path='$'):
    if type(a) is not type(b):
        return f'{path}: {type(a).__name__} {a!r} ≠ {type(b).__name__} {b!r}'
    if isinstance(a, dict):
        if set(a) != set(b):
            return f'{path}: 키 {sorted(set(a) ^ set(b))[:6]}'
        for k in sorted(a):
            d = first_diff(a[k], b[k], f'{path}.{k}')
            if d:
                return d
        return ''
    if isinstance(a, list):
        if len(a) != len(b):
            return f'{path}: 길이 {len(a)} ≠ {len(b)}'
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, f'{path}[{i}]')
            if d:
                return d
        return ''
    if isinstance(a, float) and isinstance(b, float):
        return '' if a.hex() == b.hex() or (math.isnan(a) and math.isnan(b)) else f'{path}: {a!r} ≠ {b!r}'
    return '' if a == b else f'{path}: {a!r} ≠ {b!r}'


def find_keys(x, keys, path='$', out=None):
    out = out if out is not None else []
    if isinstance(x, dict):
        for k, v in x.items():
            if k in keys:
                out.append((f'{path}.{k}', v))
            find_keys(v, keys, f'{path}.{k}', out)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            find_keys(v, keys, f'{path}[{i}]', out)
    return out


# ── 침대 (scripts/test_network_solve_certificate.py 와 같은 만듦새 · 사본) ─────────────────────────────────────────────────────────────
def chain(n=21, r=1.0, area=0.1, delta=0.05, clamp_at=None):
    A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': r} for i, z in enumerate(range(n), 1)}
    C = [{'id1': i, 'id2': i + 1, 'contact_area': (math.pi * (1.02 * r) ** 2 if i == clamp_at else area), 'delta': delta} for i in range(1, n)]
    return A, C


def se_am_bed():
    A = {i: dict(type=1, x=0., y=0., z=float(z), radius=1.) for i, z in enumerate(range(21), 1)}
    A.update({100 + k: dict(type=2, x=5., y=0., z=float(z), radius=1.) for k, z in enumerate(range(21))})
    C = [dict(id1=i, id2=i + 1, contact_area=0.1, delta=0.05) for i in range(1, 21)]
    C += [dict(id1=100 + k, id2=101 + k, contact_area=0.1, delta=0.05) for k in range(20)]
    return A, C


def nonthrough_bed():
    A = {i: {'type': 1, 'x': 3.0 * i, 'y': 0.0, 'z': z, 'radius': 1.0} for i, z in ((1, 0.0), (2, 1.0), (3, 2.0))}
    A.update({10 + k: {'type': 1, 'x': 0.0, 'y': 5.0, 'z': float(z), 'radius': 1.0} for k, z in enumerate(range(10, 21))})
    C = [{'id1': 10 + k, 'id2': 11 + k, 'contact_area': 0.1, 'delta': 0.05} for k in range(10)]
    return A, C


def lattice(nx_, ny_, nz_, seed, lo, hi):
    import numpy as np
    rng = np.random.default_rng(seed)
    idx = {}
    for k in range(nz_):
        for j in range(ny_):
            for i in range(nx_):
                idx[(i, j, k)] = len(idx)
    edges = []
    for (i, j, k), u in idx.items():
        for di, dj, dk in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            v = idx.get((i + di, j + dj, k + dk))
            if v is not None:
                rb = float(rng.uniform(lo, hi))
                edges.append({'id1': u, 'id2': v, 'R_total': rb, 'R_bulk': rb, 'R_constriction': 0.0})
    bot = {u for (i, j, k), u in idx.items() if k == 0}
    top = {u for (i, j, k), u in idx.items() if k == nz_ - 1}
    nodes = sorted({e['id1'] for e in edges} | {e['id2'] for e in edges})
    return {'nodes': nodes, 'edges': edges, 'bottom': bot, 'top': top, 'scale': 1.0, 'plate_z': float(nz_), 'box_x': float(nx_), 'box_y': float(nx_)}


def _gz_items(path, tag):
    with gzip.open(path, 'rt') as fh:
        lines = fh.read().splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith(tag):
            head = ln.replace(tag, '').split()
            return lines, head, [ln_.split() for ln_ in lines[i + 1:] if ln_ and not ln_.startswith('ITEM')]
    raise ValueError(path)


def load_dump(folder, atom, contact):
    lines, ha, ra = _gz_items(os.path.join(folder, atom), 'ITEM: ATOMS')
    ia = {k: ha.index(k) for k in ('id', 'type', 'x', 'y', 'z', 'radius')}
    A = {int(r[ia['id']]): {'type': int(r[ia['type']]), 'x': float(r[ia['x']]), 'y': float(r[ia['y']]), 'z': float(r[ia['z']]),
                            'radius': float(r[ia['radius']])} for r in ra}
    b = next(i for i, ln in enumerate(lines) if ln.startswith('ITEM: BOX BOUNDS'))
    bounds = [[float(x) for x in lines[b + 1 + k].split()[:2]] for k in range(3)]
    _l, hc, rc = _gz_items(os.path.join(folder, contact), 'ITEM: ENTRIES')
    j1, j2, jA, jD = (hc.index('c_cpl[7]'), hc.index('c_cpl[8]'), hc.index('c_cpl[22]'), hc.index('c_cpl[23]'))
    C = [{'id1': int(float(r[j1])), 'id2': int(float(r[j2])), 'contact_area': float(r[jA]), 'delta': float(r[jD])} for r in rc]
    return A, C, [bb[1] - bb[0] for bb in bounds[:2]]


def stl_plate(path):
    zs = [float(s.split()[3]) for s in open(path, encoding='utf-8').read().splitlines() if s.strip().startswith('vertex')]
    return sum(zs) / len(zs)


# ── N. 생산자 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def section_n(nc_new, nc_old, skip_case15):
    rows, added, beds = [], [], {}
    A, C = se_am_bed()
    Acl, Ccl = chain(clamp_at=10)
    Ant, Cnt = nonthrough_bed()
    Abx, Cbx = chain()
    synth = [('합성 SE + AM (이온 · 전자 · 열 · H12)', A, C, [1], [2], {1: 'SE', 2: 'AM_P'}, 1.0, 20.0, 10.0),
             ('합성 GEN2-01 사슬 (협착-only R_c = 0)', Acl, Ccl, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0),
             ('합성 진짜 비관통', Ant, Cnt, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0),
             ('합성 CF 모형 과전도 (상자 1 × 1)', Abx, Cbx, [1], [], {1: 'SE'}, 1.0, 20.0, 1.0)]
    real14 = os.path.join(ROOT, 'docs', 'data', 'real14_reference_20260928')
    Ar, Cr, _bx = load_dump(real14, 'atom_2060000.liggghts.gz', 'contact_2060000.liggghts.gz')
    synth.append(('real_14 (세 채널 · 커밋된 기준 덤프)', Ar, Cr, [3], [1, 2], {1: 'AM_P', 2: 'AM_S', 3: 'SE'}, 1000.0, 0.0302845, 0.05))
    if not skip_case15:
        c15 = os.path.join(ROOT, 'docs', 'data', 'case15_corner_20261001')
        Ac, Cc, bxc = load_dump(c15, 'atom_v4_1710000.liggghts.gz', 'contact_v4_1710000.liggghts.gz')
        synth.append(('case15 음성 대조 (실패 침대 · 띠 겹침 · 음수 면적)', Ac, Cc, [2], [1], {1: 'AM_P', 2: 'SE'}, 1000.0,
                      stl_plate(os.path.join(c15, 'mesh_v4_1710000.stl')), bxc))
    for lab, A_, C_, se_, am_, tm_, sc_, pz_, box_ in synth:
        bx, by = (box_, box_) if not isinstance(box_, list) else box_
        for cm in ('hertzian', 'physics'):
            t0 = time.time()
            new_ = run_or_err(nc_new._run_all_networks, A_, C_, se_, am_, tm_, sc_, pz_, bx, by, None, contact_mode=cm)
            old_ = run_or_err(nc_old._run_all_networks, A_, C_, se_, am_, tm_, sc_, pz_, bx, by, None, contact_mode=cm)
            d = first_diff(strip(new_, L214_ADDED), strip(old_, L214_ADDED))
            g = find_keys(new_, GUARD_FIELDS)
            lv = leaves(strip(new_, L214_ADDED))
            rows.append(dict(section='N', case=lab, mode=cm, compared=f"수 {lv['num']} · 문자 {lv['str']} · null {lv['null']} (더한 기록 키 넷 뺀 뒤)",
                             identical=(d == ''), diff=d, guard_fields=len(g), sec=round(time.time() - t0, 1),
                             statuses={k: new_.get(k) for k in ('sigma_full_status', 'sigma_full_reason', 'ionic_status', 'electronic_status',
                                                                'thermal_status')}))
            added.append(dict(case=lab, mode=cm, keys={k: new_.get(k, '(키 없음)') for k in L214_ADDED},
                              base_has=[k for k in L214_ADDED if k in old_]))
            beds[(lab, cm)] = new_
    if True:
        A_r, C_r = Ar, Cr
        for cm in ('hertzian', 'physics'):
            new_ = run_or_err(nc_new.run_decomposition, A_r, C_r, [3], 1000.0, 0.0302845, 0.05, 0.05,
                              type_map={1: 'AM_P', 2: 'AM_S', 3: 'SE'}, contact_mode=cm, mode='ionic')
            old_ = run_or_err(nc_old.run_decomposition, A_r, C_r, [3], 1000.0, 0.0302845, 0.05, 0.05,
                              type_map={1: 'AM_P', 2: 'AM_S', 3: 'SE'}, contact_mode=cm, mode='ionic')
            d = first_diff(new_, old_)
            lv = leaves(new_)
            rows.append(dict(section='N', case='real_14 이온 run_decomposition', mode=cm, compared=f"수 {lv['num']} · 문자 {lv['str']} · null {lv['null']}",
                             identical=(d == ''), diff=d, guard_fields=len(find_keys(new_, GUARD_FIELDS)), sec=None,
                             statuses={k: new_.get(k) for k in ('sigma_full_status', 'sigma_full_reason')}))
    for largs, lab in (((34, 34, 30, 7, 0.5, 2.0), '격자 34×34×30 (자유 노드 > 30,000 · cg)'), ((3, 3, 6, 20261006, 0.2, 5.0), '격자 3×3×6 (spsolve)')):
        ln_, lo_ = lattice(*largs), lattice(*largs)
        gn, go = quiet(nc_new.solve_network, ln_), quiet(nc_old.solve_network, lo_)
        d = first_diff(canon([gn[0], gn[1], ln_['solve_info']['full']]), canon([go[0], go[1], lo_['solve_info']['full']]))
        rows.append(dict(section='N', case=lab, mode='solve_network full', compared='G · q · solve_info (증서 수치 · 단 기록)', identical=(d == ''), diff=d,
                         guard_fields=len(find_keys(canon(ln_['solve_info']), GUARD_FIELDS)), sec=None,
                         statuses={'G': float(gn[0]).hex(), 'q': float(gn[1]).hex()}))
    return rows, added, beds


# ── T. τ 소비자 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def section_t(tf_new, tf_old, beds, tmp):
    rows = []
    tgz = os.path.join(ROOT, 'docs', 'data', 'lhs_network194_11fcf91e8', 'handover_v12_20261006', 'net194_tau_sources_20261006.tar.gz')
    d194 = os.path.join(tmp, 'tau194')
    with tarfile.open(tgz) as t:
        t.extractall(d194)
    cases = sorted(os.listdir(os.path.join(d194, 'cases')))
    n_eq, n_cells, bad, statuses = 0, 0, [], {}
    for c in cases:
        cd = os.path.join(d194, 'cases', c, 'work', 'results', c)
        rn, ro = canon(tf_new.case_row(cd)), canon(tf_old.case_row(cd))
        n_cells += len(rn)
        d = first_diff(rn, ro)
        if d:
            bad.append((c, d))
        else:
            n_eq += 1
        for m in ('hertz', 'physics', 'hertz_h12'):
            k = (m, rn.get(f'ion_net_status_{m}'), tf_new.reason_code(rn.get(f'ion_net_status_reason_{m}')))
            statuses[str(k)] = statuses.get(str(k), 0) + 1
    rows.append(dict(section='T', case=f'v1.2 τ 원천 {len(cases)} 케이스 (case_row · 50 칸)', mode='세대 1 (inferred_legacy)',
                     compared=f'칸 {n_cells}', identical=(not bad and n_eq == len(cases)), diff=(bad[:2] or ''), statuses=statuses))
    lab0 = '합성 SE + AM (이온 · 전자 · 열 · H12)'
    for lab in (lab0, 'real_14 (세 채널 · 커밋된 기준 덤프)', '합성 진짜 비관통', '합성 CF 모형 과전도 (상자 1 × 1)'):
        dual = {'hertzian': beds[(lab, 'hertzian')], 'physics': beds[(lab, 'physics')]}
        pz = 20.0 if lab.startswith('합성') else 30.2845
        ledger = {'thickness_um': pz, 'thickness_mass_conserving_um': pz * 0.97, 'phi_se_mass_conserving': 0.5}
        perc = 0.0 if '비관통' in lab else 100.0
        out_n = {'ion_columns': tf_new.ion_columns(dual, ledger, perc), 'contract': tf_new.network_generation_contract(dual),
                 'record_problem': {m: tf_new.ion_record_problem(tf_new.mode_record(dual, m)) for m in tf_new.MODES},
                 'binding': {m: tf_new.certificate_binding_problems(m, tf_new.mode_record(dual, m)) for m in tf_new.MODES}}
        out_o = {'ion_columns': tf_old.ion_columns(dual, ledger, perc), 'contract': tf_old.network_generation_contract(dual),
                 'record_problem': {m: tf_old.ion_record_problem(tf_old.mode_record(dual, m)) for m in tf_old.MODES},
                 'binding': {m: tf_old.certificate_binding_problems(m, tf_old.mode_record(dual, m)) for m in tf_old.MODES}}
        d = first_diff(canon(out_n), canon(out_o))
        ic = out_n['ion_columns']
        rows.append(dict(section='T', case=f'{lab} — 새 생산자 레코드', mode='ion_columns · 세대 계약 · 0b · 증서 결합',
                         compared=f"칸 {len(ic)} + 판정 셋", identical=(d == ''), diff=d,
                         statuses={m: (ic.get(f'ion_net_status_{m}'), ic.get(f'ion_net_status_reason_{m}')) for m in tf_new.MODES}))
    ev = os.path.join(ROOT, 'docs', 'reviews', 'codex_lhs214_failures_review_evidence_20261014', 'submitted', 'lhs214_run_evidence_1014_1520.tgz')
    with tarfile.open(ev) as t:
        rec = {cm: json.load(t.extractfile(f'lhs214_run_evidence_1014_1520/diag_lhsx054/network_conductivity_{cm}.json')) for cm in ('hertzian', 'physics')}
    dual = {'hertzian': rec['hertzian'], 'physics': rec['physics']}
    ledger = {'thickness_um': 20.0, 'thickness_mass_conserving_um': 19.0, 'phi_se_mass_conserving': 0.5}
    out_n = {'ion_columns': tf_new.ion_columns(dual, ledger, 100.0), 'contract': tf_new.network_generation_contract(dual),
             'record_problem': {m: tf_new.ion_record_problem(tf_new.mode_record(dual, m)) for m in tf_new.MODES}}
    out_o = {'ion_columns': tf_old.ion_columns(dual, ledger, 100.0), 'contract': tf_old.network_generation_contract(dual),
             'record_problem': {m: tf_old.ion_record_problem(tf_old.mode_record(dual, m)) for m in tf_old.MODES}}
    d = first_diff(canon(out_n), canon(out_o))
    ic = out_n['ion_columns']
    rows.append(dict(section='T', case='lhsx_054 진단 레코드 (옛 생산자 1087a9b2f · Codex 묶음)', mode='ion_columns · 세대 계약 · 0b',
                     compared=f'칸 {len(ic)} + 판정 둘', identical=(d == ''), diff=d,
                     statuses={'physics': (ic.get('ion_net_status_physics'), str(ic.get('ion_net_status_reason_physics'))[:40]),
                               'hertz': (ic.get('ion_net_status_hertz'), ic.get('ion_net_status_reason_hertz')),
                               'physics 0b': str(out_n['record_problem'].get('physics'))[:60]}))
    return rows


# ── R. 배포 빌더 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def section_r(lrb_new, lrb_old):
    import csv
    rows = []
    hd = os.path.join(ROOT, 'docs', 'data', 'lhs_network194_11fcf91e8', 'handover_v12_20261006')
    for ds in ('lhs', 'lhsx'):
        with open(os.path.join(hd, f'{ds}_handover_v12_20261006.csv'), encoding='utf-8', newline='') as f:
            rr = list(csv.DictReader(f))
        cols = list(rr[0].keys())
        n, bad = 0, []
        for r in rr:
            for c in cols:
                def one(mod):
                    try:
                        return ('v', mod.v13_blank_reason(r, c))
                    except Exception as e:                       # noqa: BLE001
                        return ('e', f'{type(e).__name__}: {e}')
                a, b = one(lrb_new), one(lrb_old)
                n += 1
                if a != b:
                    bad.append((r.get('case_id'), c, a, b))

        def cls(mod, r):
            try:
                return ('v', mod._v13_class(r))
            except Exception as e:                               # noqa: BLE001
                return ('e', f'{type(e).__name__}: {e}')
        cb = [(r.get('case_id'), cls(lrb_new, r), cls(lrb_old, r)) for r in rr if cls(lrb_new, r) != cls(lrb_old, r)]
        sc = {c_: (lrb_new._v13_status_counts(rr, c_), lrb_old._v13_status_counts(rr, c_)) for c_ in cols if c_.startswith('ion_net_status_')
              and not c_.startswith('ion_net_status_reason')}
        scb = {k: v for k, v in sc.items() if v[0] != v[1]}
        gate = lrb_new.v13_primary_model_limit_problems(rr)
        rows.append(dict(section='R', case=f'v1.2 인계표 {ds} ({len(rr)} 행 × {len(cols)} 열)', mode='빈칸 뜻 · 관통 분류 · 상태 집계 · 주 타깃 관문',
                         compared=f'칸 {n} · 행 {len(rr)} · 상태 열 {len(sc)}', identical=(not bad and not cb and not scb and gate == []),
                         diff=(bad[:2] or cb[:2] or scb or gate or ''), statuses={k: v[0] for k, v in sc.items()}))
    return rows


# ── W. 웹앱 표 (따로 프로세스 — BASE 트리 ↔ 지금 트리) ───────────────────────────────────────────────────────────────────────────────
W_PROBE = r'''
import contextlib, io, json, os, sys
root = sys.argv[1]
for p in (os.path.join(root, 'scripts'), os.path.join(root, 'webapp')):
    sys.path.insert(0, p)
with contextlib.redirect_stdout(io.StringIO()):
    import app
FIX = json.loads(sys.argv[2])
OLD_CSV = [['── Network Solver (Hertzian DEM-native) ──', ''], ['σ_ionic (mS/cm)', 0.6], ['R_brug (과대추정 배수)', '2.0×'],
           ['Constriction 비율(%)', 40.0], ['σ_electronic (mS/cm)', 2.0], ['σ_thermal (mS/cm equiv)', 0.3], ['SE Volume Fraction', 0.5]]
out = {}
for name, mx in FIX.items():
    for tag, data in (('새 표', []), ('기존 CSV 표', OLD_CSV)):
        tbl = {'network_summary': {'data': json.loads(json.dumps(data))}}
        with contextlib.redirect_stdout(io.StringIO()):
            app.transform_network_summary_4col(tbl, dict(mx), {})
        out[name + ' | ' + tag] = (tbl.get('network_summary') or {}).get('data')
print('@@JSON@@' + json.dumps(out, ensure_ascii=False, sort_keys=True, default=str))
'''
W_FIX = {
    '정상 (두 모드 · 세 채널 값)': {'sigma_full_mScm': 0.6, 'sigma_full_mScm_physics': 0.9, 'sigma_full_status': 'computed', 'sigma_full_status_physics': 'computed',
                             'network_solver_status': 'success', 'sigma_ratio': 0.4, 'phi_se': 0.5, 'sigma_bulk_net_mScm': 1.0, 'sigma_bulk_net_mScm_physics': 1.0,
                             'R_brug_over_full': 2.0, 'R_brug_over_full_physics': 1.4, 'bulk_resistance_fraction': 0.6, 'bulk_resistance_fraction_physics': 0.8,
                             'electronic_sigma_full_mScm': 2.0, 'electronic_sigma_full_mScm_physics': 3.0,
                             'thermal_sigma_full_mScm': 0.3, 'thermal_sigma_full_mScm_physics': 0.45, 'tortuosity_mean': 1.2},
    '비관통 (두 모드 valid_zero)': {'sigma_full_mScm': None, 'sigma_full_mScm_physics': None, 'sigma_full_status': 'valid_zero', 'sigma_full_status_physics': 'valid_zero',
                              'sigma_full_reason': 'no_through_path', 'sigma_full_reason_physics': 'no_through_path', 'network_solver_status': 'success',
                              'sigma_ratio': 0.4, 'phi_se': 0.3},
    'Hertz 만 있는 옛 케이스 (physics 키 없음)': {'sigma_full_mScm': 0.6, 'sigma_full_status': 'computed', 'network_solver_status': 'success', 'sigma_ratio': 0.4,
                                         'phi_se': 0.5, 'sigma_bulk_net_mScm': 1.0, 'R_brug_over_full': 2.0, 'bulk_resistance_fraction': 0.6,
                                         'electronic_sigma_full_mScm': 2.0, 'thermal_sigma_full_mScm': 0.3},
    '모형 한계 (Codex 합성 — physics None · full_over_conduction)': {'sigma_full_mScm': 0.6, 'sigma_full_mScm_physics': None, 'sigma_full_status': 'computed',
                                                         'sigma_full_status_physics': 'not_computed', 'sigma_full_reason_physics': 'full_over_conduction',
                                                         'network_solver_status': 'success', 'sigma_ratio': 0.4, 'phi_se': 0.5, 'sigma_bulk_net_mScm': 1.0,
                                                         'electronic_sigma_full_mScm': 2.0, 'electronic_sigma_full_mScm_physics': None},
}
#: 같아야 하는 쌍 = 새 표 (full_metrics 에서 세우는 망 절) 의 정상 · 비관통.  기존 CSV 표 (analyze_contacts 의 Hertz 한 열 망 절) 는 BASE 가 **값이 있어도**
#:   Physics = Hertz 복사 · Δ 0 % 로 넓혔다 (Codex L214-03 "Existing two-column CSV rows are expanded by copying values too") → 지금은 metrics 의 Physics 값 ·
#:   없으면 '—' (+ 사유) = 의도 변경.  모든 쌍에서 행 순서 · 지표 이름 · Hertz 칸은 같아야 한다 (바뀌는 것은 Physics · Δ 칸뿐).
W_EXPECT_SAME = (('정상 (두 모드 · 세 채널 값)', '새 표'), ('비관통 (두 모드 valid_zero)', '새 표'))


def run_probe(tree):
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    r = subprocess.run([sys.executable, '-c', W_PROBE, tree, json.dumps(W_FIX, ensure_ascii=False)], capture_output=True, text=True, timeout=600, env=env,
                       cwd=tree)
    line = next((ln for ln in r.stdout.splitlines() if ln.startswith('@@JSON@@')), None)
    if line is None:
        raise RuntimeError(f'probe rc {r.returncode}: {(r.stderr or r.stdout)[-800:]}')
    return json.loads(line[len('@@JSON@@'):])


def section_w(base, tmp):
    tree_old = os.path.join(tmp, 'base_tree')
    os.makedirs(tree_old)
    with tarfile.open(fileobj=io.BytesIO(git_bytes('archive', '--format=tar', base, 'webapp', 'scripts'))) as t:
        t.extractall(tree_old)
    o_old, o_new = run_probe(tree_old), run_probe(ROOT)
    rows, changes = [], []
    for name in W_FIX:
        for tag in ('새 표', '기존 CSV 표'):
            k = f'{name} | {tag}'
            a, b = o_new.get(k) or [], o_old.get(k) or []
            same = (a == b)
            #  불변식 — 행 수 · 순서 · 지표 이름 · Hertz 칸 (index 1) 이 같다 (바뀌는 것은 Physics · Δ 칸뿐)
            h_inv = len(a) == len(b) and all(isinstance(x, list) and isinstance(y, list) and x[:2] == y[:2] for x, y in zip(a, b))
            ch = [(str(y[0]), y, x) for x, y in zip(a, b) if x != y] if len(a) == len(b) else [('(행 수 다름)', len(b), len(a))]
            changes += [(k,) + c for c in ch]
            exp_same = (name, tag) in W_EXPECT_SAME
            rows.append(dict(section='W', case=k, mode=('같아야' if exp_same else 'L214-03 의도 변경 (Physics · Δ 칸만)'),
                             compared=f'행 {len(a)} · Hertz 칸 · 이름 · 순서 불변 {h_inv}',
                             identical=(same if exp_same else h_inv), diff=('' if same else f'{len(ch)} 행의 Physics · Δ 칸 다름'), statuses={},
                             hertz_cells_unchanged=h_inv, exact_same=same))
    return rows, changes


def main():
    ap = argparse.ArgumentParser(description='L214 수정 A4 무영향 대조 (읽기 전용)')
    ap.add_argument('--base', default='0c557e72a', help='기준 커밋 (원격 본 가지 · 수정 직전)')
    ap.add_argument('--json', help='결과 JSON 경로 (리포 밖 권장)')
    ap.add_argument('--skip-case15', action='store_true', help='case15 (큰 침대) 생략')
    a = ap.parse_args()
    t0 = time.time()
    changed = git_bytes('diff', '--name-only', a.base, '--', 'scripts', 'webapp').decode().split()
    with tempfile.TemporaryDirectory(prefix='a4_l214_') as tmp:
        import network_conductivity as nc_new
        import tau_flux as tf_new
        import lhs_release_build as lrb_new
        nc_old = load_base(a.base, 'scripts/network_conductivity.py', 'nc_base', tmp)
        tf_old = load_base(a.base, 'scripts/tau_flux.py', 'tf_base', tmp)
        tf_old._nc_mod = lambda: nc_old                      # 옛 τ 소비자 = 옛 생산자 상수 · 판정 (같은 BASE 판끼리)
        lrb_old = load_base(a.base, 'scripts/lhs_release_build.py', 'lrb_base', tmp)
        rows_n, added, beds = section_n(nc_new, nc_old, a.skip_case15)
        rows_t = section_t(tf_new, tf_old, beds, tmp)
        rows_r = section_r(lrb_new, lrb_old)
        rows_w, w_changes = section_w(a.base, tmp)
    rows = rows_n + rows_t + rows_r + rows_w
    want_same = rows                                         # N · T · R · W(같아야) = 비트 같음 · W(의도 변경) = Hertz 칸 · 행 불변
    ok = all(r['identical'] for r in want_same) and all(not any(k in x['base_has'] for k in L214_ADDED) for x in added) \
        and all(r['guard_fields'] == 0 for r in rows_n)
    rep = dict(base=a.base, changed_files=changed, rows=rows, added_keys=added, w_changes=w_changes, ok=ok, sec=round(time.time() - t0, 1))
    print(f'A4 무영향 대조 — 기준 {a.base} ↔ 지금 트리 · 바뀐 파일 {changed}')
    print('  (= 비트 같음 · ~ 의도 변경 = Physics · Δ 칸만 다르고 행 · 이름 · Hertz 칸 같음 · ≠ 실패)')
    for r in rows:
        mark = '=' if r.get('exact_same', r['identical']) else ('~' if r['identical'] else '≠')
        print(f"  {mark} [{r['section']}] {r['case']} · {r['mode']} · {r['compared']}" + (f"   ⟵ {r['diff']}" if r['diff'] else ''))
    print('  더한 기록 키 (N · L214_ADDED — BASE 결과에는 없음):')
    for x in added:
        print(f"    {x['case']} · {x['mode']}: {x['keys']}" + (f"  (BASE 에도 있음: {x['base_has']})" if x['base_has'] else ''))
    print(f'  W 의도 변경 ({len(w_changes)} 행 — L214-03 strict missing):')
    for k, lab, old_r, new_r in w_changes:
        print(f'    {k} · {lab}: BASE {old_r} → 지금 {new_r}')
    print(f"A4 {'PASS' if ok else 'FAIL'} — 대조 {sum(1 for r in want_same if r['identical'])}/{len(want_same)} 통과 (N · T · R · W 같아야 = 비트 같음 · "
          f"W 의도 변경 = 행 · 이름 · Hertz 칸 불변) · 증서 진단 키 (q_withheld …) 0 · BASE 결과에 더한 키 없음 · {rep['sec']} s")
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            json.dump(rep, f, ensure_ascii=False, indent=1, default=str)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
