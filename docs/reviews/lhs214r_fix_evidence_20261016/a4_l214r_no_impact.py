"""L214R 수정 무영향 대조 (읽기 전용) — 기준 BASE (기본 6cb256956) ↔ 지금 트리.

기준 = 6cb256956 (L214R 수정 직전 본 가지 · 봉인 32 파일 바이트 = Codex 재검증 핀 9e3ef54ca 와 같다 · 대기 지문 acc7bfa3…).
침대 · 덤프 읽기 · 비교 도우미 · 웹앱 탐침은 L214 증거의 a4_no_impact.py 를 그대로 가져다 쓴다 (사본 없음 · 그 파일은 실행하지 않고 함수만 쓴다).
리포에 쓰지 않는다 (임시 폴더만 · BASE 판은 git show / git archive).

  N  생산자 (network_conductivity) — L214 A4 와 같은 침대 (합성 넷 · real_14 · case15 · 격자 둘) · 결과 JSON 전체 비트 대조
     (L214R 는 생산자 출력 키를 더하지 않는다 — 고친 곳은 증서 검사 · 기하 환산 넘침 사유뿐)
  T  τ 소비자 (tau_flux) — v1.2 τ 원천 194 (case_row: 옛 50 칸 비트 같음 · 새 표지 두 칸 = 값 집계) · 새 생산자 레코드 (ion_columns 옛 칸 · 세대 계약 · 0b ·
     증서 결합 같음 · 새 표지 값) · lhsx_054 진단 레코드 (옛 생산자 1087a9b2f)
  R  배포 빌더 (lhs_release_build) — v1.2 인계표 빈칸 뜻 · 관통 분류 · 상태 집계 같음 · 주 타깃 관문: v1.2 표 그대로 (표지 칸 없음) = 문제 하나 (의도 · fail-closed ·
     L214R-02) · 같은 표에 상태에서 유도한 표지 칸을 붙인 사본 = 문제 없음 (합성 · 관문 논리 확인용)
  W  웹앱 transform_network_summary_4col (새 표 · 기존 CSV 표) — 네 꼴 × 두 표 · BASE 트리 ↔ 지금 트리 따로 프로세스 · 전부 같아야
     (L214R-03 · WEB-09 는 최종 split 병합 단계 — 화면 전체 대조는 Codex display 탐침 고치기 전 · 뒤 재실행 = 증거 probe_rerun/)

실행:  python3 -B docs/reviews/lhs214r_fix_evidence_20261016/a4_l214r_no_impact.py [--base REF] [--json OUT] [--skip-case15]
"""
import argparse
import importlib.util
import io
import json
import os
import sys
import tarfile
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
A4_PATH = os.path.join(ROOT, 'docs', 'reviews', 'lhs214_fix_evidence_20261015', 'a4_no_impact.py')
_spec = importlib.util.spec_from_file_location('a4_l214', A4_PATH)
A4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A4)                                       # 정의만 (main 은 부르지 않는다) · sys.path 에 ROOT/scripts · ROOT/webapp
assert A4.ROOT == ROOT, (A4.ROOT, ROOT)


# ── N. 생산자 (전체 비트 대조) ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def section_n(nc_new, nc_old, skip_case15):
    rows, beds = [], {}
    A, C = A4.se_am_bed()
    Acl, Ccl = A4.chain(clamp_at=10)
    Ant, Cnt = A4.nonthrough_bed()
    Abx, Cbx = A4.chain()
    synth = [('합성 SE + AM (이온 · 전자 · 열 · H12)', A, C, [1], [2], {1: 'SE', 2: 'AM_P'}, 1.0, 20.0, 10.0),
             ('합성 GEN2-01 사슬 (협착-only R_c = 0)', Acl, Ccl, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0),
             ('합성 진짜 비관통', Ant, Cnt, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0),
             ('합성 CF 모형 과전도 (상자 1 × 1)', Abx, Cbx, [1], [], {1: 'SE'}, 1.0, 20.0, 1.0)]
    real14 = os.path.join(ROOT, 'docs', 'data', 'real14_reference_20260928')
    Ar, Cr, _bx = A4.load_dump(real14, 'atom_2060000.liggghts.gz', 'contact_2060000.liggghts.gz')
    synth.append(('real_14 (세 채널 · 커밋된 기준 덤프)', Ar, Cr, [3], [1, 2], {1: 'AM_P', 2: 'AM_S', 3: 'SE'}, 1000.0, 0.0302845, 0.05))
    if not skip_case15:
        c15 = os.path.join(ROOT, 'docs', 'data', 'case15_corner_20261001')
        Ac, Cc, bxc = A4.load_dump(c15, 'atom_v4_1710000.liggghts.gz', 'contact_v4_1710000.liggghts.gz')
        synth.append(('case15 음성 대조 (실패 침대 · 띠 겹침 · 음수 면적)', Ac, Cc, [2], [1], {1: 'AM_P', 2: 'SE'}, 1000.0,
                      A4.stl_plate(os.path.join(c15, 'mesh_v4_1710000.stl')), bxc))
    for lab, A_, C_, se_, am_, tm_, sc_, pz_, box_ in synth:
        bx, by = (box_, box_) if not isinstance(box_, list) else box_
        for cm in ('hertzian', 'physics'):
            t0 = time.time()
            new_ = A4.run_or_err(nc_new._run_all_networks, A_, C_, se_, am_, tm_, sc_, pz_, bx, by, None, contact_mode=cm)
            old_ = A4.run_or_err(nc_old._run_all_networks, A_, C_, se_, am_, tm_, sc_, pz_, bx, by, None, contact_mode=cm)
            d = A4.first_diff(new_, old_)
            lv = A4.leaves(new_)
            rows.append(dict(section='N', case=lab, mode=cm, compared=f"수 {lv['num']} · 문자 {lv['str']} · null {lv['null']}",
                             identical=(d == ''), diff=d, sec=round(time.time() - t0, 1),
                             statuses={k: new_.get(k) for k in ('sigma_full_status', 'sigma_full_reason', 'ionic_status', 'electronic_status',
                                                                'thermal_status')}))
            beds[(lab, cm)] = new_
    for cm in ('hertzian', 'physics'):
        args = (Ar, Cr, [3], 1000.0, 0.0302845, 0.05, 0.05)
        kw = dict(type_map={1: 'AM_P', 2: 'AM_S', 3: 'SE'}, contact_mode=cm, mode='ionic')
        new_, old_ = A4.run_or_err(nc_new.run_decomposition, *args, **kw), A4.run_or_err(nc_old.run_decomposition, *args, **kw)
        d = A4.first_diff(new_, old_)
        lv = A4.leaves(new_)
        rows.append(dict(section='N', case='real_14 이온 run_decomposition', mode=cm, compared=f"수 {lv['num']} · 문자 {lv['str']} · null {lv['null']}",
                         identical=(d == ''), diff=d, sec=None, statuses={k: new_.get(k) for k in ('sigma_full_status', 'sigma_full_reason')}))
    for largs, lab in (((34, 34, 30, 7, 0.5, 2.0), '격자 34×34×30 (자유 노드 > 30,000 · cg)'), ((3, 3, 6, 20261006, 0.2, 5.0), '격자 3×3×6 (spsolve)')):
        ln_, lo_ = A4.lattice(*largs), A4.lattice(*largs)
        gn, go = A4.quiet(nc_new.solve_network, ln_), A4.quiet(nc_old.solve_network, lo_)
        d = A4.first_diff(A4.canon([gn[0], gn[1], ln_['solve_info']]), A4.canon([go[0], go[1], lo_['solve_info']]))
        rows.append(dict(section='N', case=lab, mode='solve_network', compared='G · q · solve_info 전체 (증서 · 단 기록)', identical=(d == ''), diff=d,
                         sec=None, statuses={'G': float(gn[0]).hex(), 'q': float(gn[1]).hex()}))
    return rows, beds


# ── T. τ 소비자 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def _split(new, old, newcols):
    """새 레코드 = 옛 키 전부 (같은 값) + newcols 만 더한 것인가 → (같은가, 차이 설명, 더한 칸 값)."""
    extra, missing = set(new) - set(old), set(old) - set(new)
    if missing or not extra <= set(newcols):
        return False, f'키 — 빠짐 {sorted(missing)[:4]} · 모르는 더함 {sorted(extra - set(newcols))[:4]}', {}
    d = A4.first_diff({k: new[k] for k in old}, old)
    return d == '', d, {k: new[k] for k in sorted(extra)}


def section_t(tf_new, tf_old, beds, tmp):
    rows = []
    newcols = tuple(tf_new.MODEL_LIMIT_FLAG_COL.values())
    tgz = os.path.join(ROOT, 'docs', 'data', 'lhs_network194_11fcf91e8', 'handover_v12_20261006', 'net194_tau_sources_20261006.tar.gz')
    d194 = os.path.join(tmp, 'tau194')
    with tarfile.open(tgz) as t:
        t.extractall(d194, filter='data')
    cases = sorted(os.listdir(os.path.join(d194, 'cases')))
    n_eq, n_cells, bad, flags = 0, 0, [], {}
    for c in cases:
        cd = os.path.join(d194, 'cases', c, 'work', 'results', c)
        rn, ro = A4.canon(tf_new.case_row(cd)), A4.canon(tf_old.case_row(cd))
        n_cells += len(ro)
        ok, d, add = _split(rn, ro, newcols)
        if ok and set(add) == set(newcols):
            n_eq += 1
        else:
            bad.append((c, d or f'더한 칸 {sorted(add)}'))
        for k, v in add.items():
            flags[f'{k}={v!r}'] = flags.get(f'{k}={v!r}', 0) + 1
    rows.append(dict(section='T', case=f'v1.2 τ 원천 {len(cases)} 케이스 (case_row 옛 칸 · 세대 1 inferred_legacy)', mode='옛 칸 비트 같음 + 표지 두 칸',
                     compared=f'옛 칸 {n_cells}', identical=(not bad and n_eq == len(cases)), diff=(bad[:2] or ''), statuses=flags))
    for lab in ('합성 SE + AM (이온 · 전자 · 열 · H12)', 'real_14 (세 채널 · 커밋된 기준 덤프)', '합성 진짜 비관통', '합성 CF 모형 과전도 (상자 1 × 1)'):
        dual = {'hertzian': beds[(lab, 'hertzian')], 'physics': beds[(lab, 'physics')]}
        pz = 20.0 if lab.startswith('합성') else 30.2845
        ledger = {'thickness_um': pz, 'thickness_mass_conserving_um': pz * 0.97, 'phi_se_mass_conserving': 0.5}
        perc = 0.0 if '비관통' in lab else 100.0

        def judge(tf):
            return {'contract': tf.network_generation_contract(dual),
                    'record_problem': {m: tf.ion_record_problem(tf.mode_record(dual, m)) for m in tf.MODES},
                    'binding': {m: tf.certificate_binding_problems(m, tf.mode_record(dual, m)) for m in tf.MODES}}
        icn, ico = A4.canon(tf_new.ion_columns(dual, ledger, perc)), A4.canon(tf_old.ion_columns(dual, ledger, perc))
        ok, d, add = _split(icn, ico, newcols)
        dj = A4.first_diff(A4.canon(judge(tf_new)), A4.canon(judge(tf_old)))
        rows.append(dict(section='T', case=f'{lab} — 새 생산자 레코드', mode='ion_columns 옛 칸 · 세대 계약 · 0b · 증서 결합',
                         compared=f'옛 칸 {len(ico)} + 판정 셋', identical=(ok and dj == '' and set(add) == set(newcols)), diff=(d or dj),
                         statuses=dict(add, **{m: (icn.get(f'ion_net_status_{m}'), icn.get(f'ion_net_status_reason_{m}')) for m in tf_new.MODES})))
    ev = os.path.join(ROOT, 'docs', 'reviews', 'codex_lhs214_failures_review_evidence_20261014', 'submitted', 'lhs214_run_evidence_1014_1520.tgz')
    with tarfile.open(ev) as t:
        rec = {cm: json.load(t.extractfile(f'lhs214_run_evidence_1014_1520/diag_lhsx054/network_conductivity_{cm}.json')) for cm in ('hertzian', 'physics')}
    dual = {'hertzian': rec['hertzian'], 'physics': rec['physics']}
    ledger = {'thickness_um': 20.0, 'thickness_mass_conserving_um': 19.0, 'phi_se_mass_conserving': 0.5}
    icn, ico = A4.canon(tf_new.ion_columns(dual, ledger, 100.0)), A4.canon(tf_old.ion_columns(dual, ledger, 100.0))
    ok, d, add = _split(icn, ico, newcols)
    jn = {'contract': tf_new.network_generation_contract(dual), 'record_problem': {m: tf_new.ion_record_problem(tf_new.mode_record(dual, m)) for m in tf_new.MODES}}
    jo = {'contract': tf_old.network_generation_contract(dual), 'record_problem': {m: tf_old.ion_record_problem(tf_old.mode_record(dual, m)) for m in tf_old.MODES}}
    dj = A4.first_diff(A4.canon(jn), A4.canon(jo))
    rows.append(dict(section='T', case='lhsx_054 진단 레코드 (옛 생산자 1087a9b2f · Codex 묶음)', mode='ion_columns 옛 칸 · 세대 계약 · 0b',
                     compared=f'옛 칸 {len(ico)} + 판정 둘', identical=(ok and dj == '' and set(add) == set(newcols)), diff=(d or dj),
                     statuses=dict(add, physics=(icn.get('ion_net_status_physics'), str(icn.get('ion_net_status_reason_physics'))[:60]),
                                   hertz=(icn.get('ion_net_status_hertz'), icn.get('ion_net_status_reason_hertz')))))
    return rows


# ── R. 배포 빌더 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def section_r(lrb_new, lrb_old):
    import csv
    rows = []
    hd = os.path.join(ROOT, 'docs', 'data', 'lhs_network194_11fcf91e8', 'handover_v12_20261006')
    col = lrb_new.V13_MODEL_LIMIT_FLAG['hertz']
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
        rows.append(dict(section='R', case=f'v1.2 인계표 {ds} ({len(rr)} 행 × {len(cols)} 열)', mode='빈칸 뜻 · 관통 분류 · 상태 집계',
                         compared=f'칸 {n} · 행 {len(rr)} · 상태 열 {len(sc)}', identical=(not bad and not cb and not scb),
                         diff=(bad[:2] or cb[:2] or scb or ''), statuses={k: v[0] for k, v in sc.items()}))
        g_old, g_new = lrb_old.v13_primary_model_limit_problems(rr), lrb_new.v13_primary_model_limit_problems(rr)
        exp = (g_old == [] and len(g_new) == 1 and col in g_new[0] and f'칸이 없는 행 {len(rr)}' in g_new[0])
        rows.append(dict(section='R', case=f'v1.2 인계표 {ds} — 주 타깃 관문 (표 그대로)', mode='의도 변경 (L214R-02 · 표지 칸 없음 = 문제 · fail-closed)',
                         compared=f'BASE 문제 {len(g_old)} · 지금 문제 {len(g_new)}', identical=exp, intended=True,
                         diff=('' if exp else f'BASE {g_old} · 지금 {g_new}'), statuses={'지금': [p[:110] for p in g_new]}))
        aug = [dict(r, **{col: (lrb_new.V13_FLAG_TRUE if lrb_new._v13_is_model_limit(r, 'hertz') else lrb_new.V13_FLAG_FALSE)}) for r in rr]
        g_aug = lrb_new.v13_primary_model_limit_problems(aug)
        rows.append(dict(section='R', case=f'v1.2 인계표 {ds} — 상태에서 유도한 표지 칸을 붙인 사본 (합성 · 관문 논리)', mode='문제 없어야',
                         compared=f'행 {len(aug)} · 표지 True {sum(1 for r in aug if r[col] == lrb_new.V13_FLAG_TRUE)}', identical=(g_aug == []),
                         diff=('' if g_aug == [] else g_aug), statuses={}))
    return rows


# ── W. 웹앱 표 (따로 프로세스 — BASE 트리 ↔ 지금 트리 · 전부 같아야) ─────────────────────────────────────────────────────────────────
def section_w(base, tmp):
    tree_old = os.path.join(tmp, 'base_tree')
    os.makedirs(tree_old)
    with tarfile.open(fileobj=io.BytesIO(A4.git_bytes('archive', '--format=tar', base, 'webapp', 'scripts'))) as t:
        t.extractall(tree_old, filter='data')
    o_old, o_new = A4.run_probe(tree_old), A4.run_probe(ROOT)
    rows = []
    for name in A4.W_FIX:
        for tag in ('새 표', '기존 CSV 표'):
            k = f'{name} | {tag}'
            a, b = o_new.get(k) or [], o_old.get(k) or []
            d = A4.first_diff(a, b)
            rows.append(dict(section='W', case=k, mode='같아야', compared=f'행 {len(a)}', identical=(d == ''), diff=d, statuses={}))
    return rows


def main():
    ap = argparse.ArgumentParser(description='L214R 수정 무영향 대조 (읽기 전용)')
    ap.add_argument('--base', default='6cb256956', help='기준 커밋 (L214R 수정 직전 본 가지)')
    ap.add_argument('--json', help='결과 JSON 경로 (리포 밖 권장)')
    ap.add_argument('--skip-case15', action='store_true', help='case15 (큰 침대) 생략')
    a = ap.parse_args()
    t0 = time.time()
    changed = A4.git_bytes('diff', '--name-only', a.base, '--', 'scripts', 'webapp').decode().split()
    with tempfile.TemporaryDirectory(prefix='a4_l214r_') as tmp:
        import network_conductivity as nc_new
        import tau_flux as tf_new
        import lhs_release_build as lrb_new
        nc_old = A4.load_base(a.base, 'scripts/network_conductivity.py', 'nc_base', tmp)
        tf_old = A4.load_base(a.base, 'scripts/tau_flux.py', 'tf_base', tmp)
        tf_old._nc_mod = lambda: nc_old                      # 옛 τ 소비자 = 옛 생산자 상수 · 판정 (같은 BASE 판끼리)
        lrb_old = A4.load_base(a.base, 'scripts/lhs_release_build.py', 'lrb_base', tmp)
        rows_n, beds = section_n(nc_new, nc_old, a.skip_case15)
        rows_t = section_t(tf_new, tf_old, beds, tmp)
        rows_r = section_r(lrb_new, lrb_old)
        rows_w = section_w(a.base, tmp)
    rows = rows_n + rows_t + rows_r + rows_w
    ok = all(r['identical'] for r in rows)
    rep = dict(base=a.base, changed_files=changed, rows=rows, ok=ok, sec=round(time.time() - t0, 1))
    print(f'L214R 무영향 대조 — 기준 {a.base} ↔ 지금 트리 · 바뀐 파일 {changed}')
    print('  (= 같음 · ~ 등록한 의도 변경이 기대대로 · ≠ 실패)')
    for r in rows:
        mark = ('~' if r.get('intended') else '=') if r['identical'] else '≠'
        print(f"  {mark} [{r['section']}] {r['case']} · {r['mode']} · {r['compared']}" + (f"   ⟵ {r['diff']}" if r['diff'] else '')
              + (f"   {json.dumps(r['statuses'], ensure_ascii=False)[:240]}" if r['statuses'] and r['section'] in ('T', 'R') else ''))
    print(f"L214R A4 {'PASS' if ok else 'FAIL'} — 대조 {sum(1 for r in rows if r['identical'])}/{len(rows)} · {rep['sec']} s")
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            json.dump(rep, f, ensure_ascii=False, indent=1, default=str)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
