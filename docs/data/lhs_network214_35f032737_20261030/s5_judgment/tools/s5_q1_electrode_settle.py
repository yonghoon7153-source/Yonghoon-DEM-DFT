#!/usr/bin/env python3
"""Q1 확정 도구 — 한 침대: B7 실행 자신의 입력으로 B7 코드가 H0 이온 망을 다시 짓고, **같은 망**을 두 전극 모형으로 푼다 (읽기 전용).

  · 입력 (읽기만): --case-dir = B7 실행의 results/<case> (atoms.csv · contacts.csv · mesh_info.json · input_params.json ·
    network_provenance.json · network_conductivity_dual.json) · --v12-dual = v1.2 τ 원천의 같은 케이스 network_conductivity_dual.json ·
    (선택) --v12-prov = 그 network_provenance.json.  쓰기는 --out (새 빈 폴더) 에만.
  · 망 = B7 CLI 와 같은 적재 (type map · plate_z = mesh_info.json · 상자 = input_params.json) 로 `_run_all_networks(contact_mode='hertzian')` 를
    안에서 부른다.  `solve_network` 를 감싸 H0 이온 망 (hertz_arm H0 · 열 아님 · 간선 상 = SE) 의 세 가지 (full · bulk_only · constriction_only)
    풀이마다 같은 망 · 같은 간선 저항으로 둘을 더 푼다 (설계 기록 재구현 `docs/data/gen2_design_20261006/c1/netsolve.py`):
      옛 전극 = netsolve.solve_adaptive (가상 전원 · 싱크 g_b = max(100·Σg/n_el, 10·g_max, 1e-6) · 직접해 — 옛 모듈과의 차 real_14 −3.1e-9 ·
               case15 −1.3e-7 (net_beds_*.json module_check))
      새 전극 = B7 solve_network 가 돌려준 값 그대로 + netsolve.solve_dirichlet (교차 확인)
판정 (값 칸은 소수 8 자리 저장 — 저장 반폭 = 0.5e-8):
  A0 = atoms.csv · contacts.csv 의 지문 (sha256 앞 16) = B7 provenance 의 input_digests
  A  = 안에서 부른 B7 값 ↔ B7 기록 (세 가지) 이 저장 반폭 안
  B  = 같은 망 옛 전극 값 ↔ v1.2 기록 (v1.2 에 있는 가지 · FULL 필수) 이 저장 반폭 안
  → A0 ∧ A ∧ B = INCLUDE 근거 (rc 0): v1.2 → B7 차이는 전극 모형뿐 — 정확한 Δ = σ_dirichlet/σ_adaptive − 1 을 적는다
  → 하나라도 거짓 = HOLD (rc 3): 입력 · 절차가 B7 기록과 이어지지 않거나 (A0 · A) 전극 밖의 차이가 있다 (B)
  → v1.2 가 CG 경로 (관통 N + 2 > 30000 · scipy ≥ 1.14 에서 옛 `tol=` → `atol=1e-8` · 기본 rtol 1e-5) 면 B 를 판정하지 않는다 = INCONCLUSIVE (rc 4)
  → 입력 오류 = rc 2
  (--assume-v12-direct = 검증 픽스처 전용 · WSL 확정 명령에는 쓰지 않는다)
  (선택) A_code = --b7-manifest: 불러온 리포 모듈 sha256 = 봉인 code_hashes · A_run = --b7-reread: provenance run id = reread run id ∧ reread 표 값 = dual 기록
        — 주면 INCLUDE 의 조건에 들어간다 (WSL 확정 명령은 둘 다 준다)
사용: python3 -I s5_q1_electrode_settle.py --repo <B7 체크아웃> --case-dir <B7 results/<case>> --v12-dual <dual JSON> [--v12-prov <JSON>] \\
        [--b7-manifest <manifest.json>] [--b7-reread <reread.json>] --case <이름> --out <새 폴더>
"""
import argparse
import hashlib
import json
import math
import os
import sys

HALF = 0.5e-8
BRANCHES = (('full', 'sigma_full'), ('bulk_only', 'sigma_bulk_net'), ('constriction_only', 'sigma_constr_net'))
OLD_CG_N = 30000


def die(msg):
    print('⛔ ' + msg, file=sys.stderr)
    sys.exit(2)


def jload(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def sha256(p, n=None):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()[:n] if n else h.hexdigest()


def snapshot(d):
    out = {}
    for nm in sorted(os.listdir(d)):
        p = os.path.join(d, nm)
        if os.path.isfile(p):
            st = os.stat(p)
            out[nm] = (st.st_size, st.st_mtime_ns)
    return out


def within(x, rec):
    if not (isinstance(x, (int, float)) and isinstance(rec, (int, float))) or not (math.isfinite(x) and math.isfinite(rec)):
        return None
    return bool(abs(x - rec) <= HALF + 1e-12 * max(1.0, abs(x)))


def _jsonable(o):
    """numpy 스칼라 · 집합 등 — 기록용으로만 바꾼다 (판정에 쓰지 않는다)."""
    if hasattr(o, 'item'):
        return o.item()
    if isinstance(o, (set, frozenset, tuple)):
        return sorted(o, key=str)
    return repr(o)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--case-dir', required=True)
    ap.add_argument('--v12-dual', required=True)
    ap.add_argument('--v12-prov', default='')
    ap.add_argument('--case', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--b7-manifest', default='', help='B7 manifest.json — 불러온 리포 모듈 sha256 ↔ code_hashes (A_code)')
    ap.add_argument('--b7-reread', default='', help='B7 reread.json — run id ↔ provenance · 표 값 ↔ dual 기록 (A_run)')
    ap.add_argument('--assume-v12-direct', action='store_true',
                    help='검증 픽스처 전용 — v1.2 기록이 직접해로 만든 것이라고 가정한다 (WSL 확정 명령에는 쓰지 않는다 · 출력에 표지)')
    a = ap.parse_args(argv)
    cd = os.path.abspath(a.case_dir)
    if os.path.exists(a.out) and os.listdir(a.out):
        die(f'--out 가 비어 있지 않다: {a.out}')
    need = ('atoms.csv', 'contacts.csv', 'network_provenance.json', 'network_conductivity_dual.json')
    miss = [n for n in need if not os.path.isfile(os.path.join(cd, n))]
    if miss:
        die(f'case-dir 에 없음: {miss}')
    os.makedirs(os.path.join(a.out, 'work'), exist_ok=True)
    snap0 = snapshot(cd)
    prov = jload(os.path.join(cd, 'network_provenance.json'))
    argvp = prov.get('argv') or {}
    tmap_s, scale = argvp.get('type_map'), argvp.get('scale')
    if not (isinstance(tmap_s, str) and isinstance(scale, int)):
        die(f'provenance argv 결손: {argvp!r}')
    dig = {n: sha256(os.path.join(cd, n), 16) for n in ('atoms.csv', 'contacts.csv')}
    a0 = dig == (prov.get('input_digests') or {})
    v12prov = jload(a.v12_prov) if a.v12_prov else None
    a0v = (dig == (v12prov.get('input_digests') or {})) if v12prov else None
    rec_b7 = jload(os.path.join(cd, 'network_conductivity_dual.json'))['hertzian']
    rec_v12 = jload(a.v12_dual)['hertzian']

    sys.path.insert(0, os.path.join(a.repo, 'scripts'))
    sys.path.insert(0, os.path.join(a.repo, 'docs', 'data', 'gen2_design_20261006', 'c1'))
    import network_conductivity as nc        # noqa: E402  (B7 봉인 코드)
    import netsolve                          # noqa: E402  (설계 재구현)
    from analyze_contacts import load_atoms_raw, load_contacts_raw   # noqa: E402
    code = {n: sha256(p) for n, p in (('network_conductivity.py', nc.__file__), ('netsolve.py', netsolve.__file__),
                                       ('analyze_contacts.py', sys.modules['analyze_contacts'].__file__))}
    # A_run — 기록 사슬: provenance 의 run id = reread 의 run id · reread 표 값 = dual 기록 (세 가지)
    a_run, run_detail = None, {}
    if a.b7_reread:
        ent = [c for c in jload(a.b7_reread).get('cases') or [] if c.get('case') == a.case]
        if len(ent) != 1:
            a_run, run_detail = False, {'why': f'reread 에 {a.case} 항목 {len(ent)} 개'}
        else:
            e0 = ent[0]
            tb = ((e0.get('table') or {}).get('hertz') or {})
            same_vals = {br: (tb.get(br) or {}).get('value') == rec_b7.get(key) for br, key in BRANCHES}
            a_run = (prov.get('network_run_id') == e0.get('run_id')) and all(same_vals.values())
            run_detail = {'prov_run_id': prov.get('network_run_id'), 'reread_run_id': e0.get('run_id'), 'table_equals_dual': same_vals}

    type_map = {}
    for pair in tmap_s.split(','):                       # CLI main 과 같은 해석
        k, v = pair.split(':')
        type_map[int(k)] = v.strip()
    target_types = [k for k, v in type_map.items() if v == 'SE']
    am_types = [k for k, v in type_map.items() if 'AM' in v]
    atoms_raw, _ = load_atoms_raw(os.path.join(cd, 'atoms.csv'))
    contacts_raw, _ = load_contacts_raw(os.path.join(cd, 'contacts.csv'))
    mf = os.path.join(cd, 'mesh_info.json')
    plate_z = jload(mf)['plate_z'] if os.path.isfile(mf) else max(x['z'] for x in atoms_raw.values())
    box_x, box_y = 0.05, 0.05
    ipf = os.path.join(cd, 'input_params.json')
    if os.path.isfile(ipf):
        ip = jload(ipf)
        box_x, box_y = ip.get('box_x', 0.05), ip.get('box_y', 0.05)

    orig = nc.solve_network
    cap = []
    tset = set(target_types)

    def edge_R(e, mode):
        if mode == 'full':
            return e['R_total']
        if mode == 'bulk_only':
            return e['R_bulk'] if e['R_bulk'] > 0 else 1e-12
        if mode == 'constriction_only':
            return e['R_constriction']
        return e['R_total']

    def wrapped(network_data, mode='full', return_field=False):
        out = orig(network_data, mode=mode, return_field=return_field)
        nd = network_data if isinstance(network_data, dict) else {}
        if not (nd.get('contact_mode') == 'hertzian' and nd.get('hertz_arm') == 'H0' and not nd.get('is_thermal')
                and nd.get('edges') and all(e.get('type1') in tset and e.get('type2') in tset for e in nd['edges'])):
            return out
        sb_ = out[1] if out else None
        r = dict(mode=mode, sigma_b7_raw=(float(sb_) if sb_ is not None else None), solve_info=(nd.get('solve_info') or {}).get(mode))
        try:
            R = [edge_R(e, mode) for e in nd['edges']]
            perc = netsolve.perc_component(nd)
            _ga, sa, xa = netsolve.solve_adaptive(nd, R, perc)
            _gd, sd, _xd = netsolve.solve_dirichlet(nd, R, perc)
            r.update(sigma_adaptive=(float(sa) if sa is not None else None), sigma_dirichlet_ns=(float(sd) if sd is not None else None),
                     n_perc=len(perc), g_boundary=xa.get('g_boundary'), sum_g=xa.get('sum_g'), g_max=xa.get('g_max'),
                     n_bot=xa.get('n_bot'), n_top=xa.get('n_top'))
        except Exception as e:                            # noqa: BLE001 — 기록하고 판정에서 거짓
            r['error'] = f'{type(e).__name__}: {e}'
        cap.append(r)
        return out

    nc.solve_network = wrapped
    try:
        res = nc._run_all_networks(atoms_raw, contacts_raw, target_types, am_types, type_map, scale, plate_z, box_x, box_y,
                                   os.path.join(a.out, 'work'), contact_mode='hertzian', dump_raw_dir=None, temp_c=None, ea_ion_ev=None)
    finally:
        nc.solve_network = orig
    snap1 = snapshot(cd)
    # A_code — 이 실행에서 불러온 리포 모듈 (scripts · webapp) 의 sha256 ↔ B7 manifest code_hashes (목록에 있는 것만 · 목록 밖은 적기만)
    a_code, code_detail = None, {}
    loaded = {}
    repo_abs = os.path.abspath(a.repo)
    for mn, mod in list(sys.modules.items()):
        f_ = getattr(mod, '__file__', None)
        if f_ and os.path.abspath(f_).startswith(repo_abs + os.sep):
            loaded[os.path.relpath(os.path.abspath(f_), repo_abs).replace(os.sep, '/')] = sha256(f_)
    if a.b7_manifest:
        ch = jload(a.b7_manifest).get('code_hashes') or {}
        code_detail = {'checked': {r_: (h_ == ch[r_]) for r_, h_ in sorted(loaded.items()) if r_ in ch},
                       'not_in_seal': sorted(r_ for r_ in loaded if r_ not in ch)}
        a_code = bool(code_detail['checked']) and all(code_detail['checked'].values()) \
            and 'scripts/network_conductivity.py' in code_detail['checked']

    by = {}
    for r in cap:
        by.setdefault(r['mode'], []).append(r)
    rows, A, B, inconclusive = {}, True, True, False
    n_perc_full = None
    for br, key in BRANCHES:
        rs = by.get(br) or []
        r = rs[0] if rs else {}
        same_rep = all((x.get('sigma_b7_raw'), x.get('sigma_adaptive')) == (r.get('sigma_b7_raw'), r.get('sigma_adaptive')) for x in rs)
        sb, sa, sdn = r.get('sigma_b7_raw'), r.get('sigma_adaptive'), r.get('sigma_dirichlet_ns')
        recb, recv = rec_b7.get(key), rec_v12.get(key)
        a_ok = within(sb, recb) if recb is not None else (sb is None)
        a_res = (res or {}).get(key) == recb
        b_ok = within(sa, recv) if recv is not None else None
        rows[br] = dict(n_calls=len(rs), repeat_calls_identical=same_rep, sigma_b7_inprocess=sb, record_b7=recb, A=a_ok,
                        result_dict_equals_record=a_res, sigma_adaptive=sa, record_v12=recv, B=b_ok,
                        sigma_dirichlet_netsolve=sdn,
                        dirichlet_netsolve_vs_b7_rel=((sdn / sb - 1) if (sb and sdn) else None),
                        d_electrode=((sb / sa - 1) if (sb and sa) else None),
                        d_records=(((recb - recv) / max(abs(recb), abs(recv))) if (recb and recv) else None),
                        g_boundary=r.get('g_boundary'), sum_g=r.get('sum_g'), g_max=r.get('g_max'), n_perc=r.get('n_perc'),
                        n_bot=r.get('n_bot'), n_top=r.get('n_top'), b7_method=(r.get('solve_info') or {}).get('method'),
                        error=r.get('error'))
        if br == 'full':
            n_perc_full = r.get('n_perc')
        A = A and bool(a_ok) and bool(a_res) and same_rep and not r.get('error')
        if recv is not None or br == 'full':
            B = B and bool(b_ok) and not r.get('error')
    v12_n_perc = (rec_v12.get('n_nodes') or 0) * (rec_v12.get('percolating_fraction') or 0)
    v12_path = 'cg_rtol1e-5' if v12_n_perc + 2 > OLD_CG_N else 'spsolve'
    if a.assume_v12_direct:
        v12_path = f'assumed_direct (검증 픽스처 · 기록상 {v12_path})'
    elif v12_path != 'spsolve':
        inconclusive = True
    untouched = snap0 == snap1
    if not (a0 and A and untouched and a_code is not False and a_run is not False):
        verdict, rc = 'HOLD', 3
        why = '입력 · 절차 · 코드가 B7 기록과 이어지지 않는다 (A0 · A · A_code · A_run · case-dir 불변 중 거짓)'
    elif inconclusive:
        verdict, rc = 'INCONCLUSIVE', 4
        why = 'v1.2 가 CG 경로 (옛 반복해 오차) — B 를 판정하지 않는다'
    elif B:
        verdict, rc = 'INCLUDE', 0
        why = 'v1.2 → B7 차이 = 전극 모형뿐 (같은 입력 · 같은 망) — 정확한 Δ 는 rows.*.d_electrode'
    else:
        verdict, rc = 'HOLD', 3
        why = '같은 망의 옛 전극 값이 v1.2 기록과 다르다 — 전극 밖의 차이가 있다'
    out = dict(schema='s5_q1_electrode_settle/v1', case=a.case, verdict=verdict, why=why,
               checks=dict(A0_inputs_equal_b7_provenance=a0, A0v_inputs_equal_v12_provenance=a0v, A_b7_reproduced=A,
                           B_v12_reproduced_by_old_electrode=(None if inconclusive else B), case_dir_untouched=untouched,
                           A_code_equals_b7_seal=a_code, A_run_record_chain=a_run,
                           v12_solver_path=v12_path, v12_n_perc_approx=round(v12_n_perc), n_perc_rebuilt=n_perc_full),
               rows=rows, digests=dig, code_sha256=code, code_seal_detail=code_detail, run_detail=run_detail,
               argv=dict(type_map=tmap_s, scale=scale),
               geometry=dict(plate_z=plate_z, box_x=box_x, box_y=box_y), half_unit=HALF,
               d_full_within_1p5e4=(rows['full']['d_electrode'] is not None and abs(rows['full']['d_electrode']) <= 1.5e-4))
    with open(os.path.join(a.out, f'settle_{a.case}.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=_jsonable)
    rf = rows['full']
    print(f'{a.case}: {verdict} — {why}')
    print(f'  A0 {a0} · A {A} · A_code {a_code} · A_run {a_run} · B {None if inconclusive else B} · case-dir 불변 {untouched} · v1.2 경로 {v12_path}')
    for br, _ in BRANCHES:
        x = rows[br]
        de = x['d_electrode']
        print(f'  {br:17s} B7 {x["sigma_b7_inprocess"]!r} (기록 {x["record_b7"]!r}) · 옛 전극 {x["sigma_adaptive"]!r} (v1.2 기록 {x["record_v12"]!r})'
              f' · Δ_전극 {de:.6e}' if de is not None else f'  {br:17s} Δ 없음 ({x.get("error")})')
    print(f'  FULL Δ_전극 ≤ 1.5e-4: {out["d_full_within_1p5e4"]} (Δ = {rf["d_electrode"]!r})')
    return rc


if __name__ == '__main__':
    sys.exit(main())
