#!/usr/bin/env python3
"""LHS214 B7 발사 기록 — 등록 §5 판정 중 **받은 묶음 (records) 만으로** 할 수 있는 칸 (읽기 전용).

입력 = 받은 묶음을 빈 폴더에 푼 두 배치 뿌리 사본 (manifest · runs · progress · seal_audit · reread · merged · cases/*/worker.json · log.txt).
판정 함수 = 리포의 것 그대로 (사본 금지 · 규율 ①):
  - ⓪ · ⓪b 배치 관문 = scripts/lhs_release_build.py `v13_batch_gate_problems` (build · 단계 A · check 가 같은 함수)
  - τ 상태 집계 = `_v13_status_counts` · 주 타깃 모형 한계 = `v13_primary_model_limit_problems` · 모형 한계 사실 = `v13_model_limit`
  - 등록 §4 덧붙임의 완료 확인 스니펫 (등록 문서의 글자 그대로 옮김)
쓰는 것 = --out 폴더의 s5_summary.json · tau_status_by_case.tsv (값 없음 · 상태 · 사유 · 표지 · 띠 규칙).

사용: python3 -I s5_records_judge.py --repo <리포> --root194 <풀어 둔 194 뿌리> --rootsupp <풀어 둔 보충 뿌리> --out <새 폴더>
"""
import argparse
import collections
import csv
import hashlib
import json
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True)
ap.add_argument('--root194', required=True)
ap.add_argument('--rootsupp', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()
sys.path.insert(0, os.path.join(a.repo, 'scripts'))
import lhs_release_build as L  # noqa: E402

BATCHES = (('production194', a.root194), ('supp20', a.rootsupp))
MODES = ('hertz', 'physics', 'hertz_h12')
summ = {'schema': 's5_records_judge/v1', 'batches': {}}
tsv_rows = []


def sha256(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def jl(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


for eset, root in BATCHES:
    B = summ['batches'][eset] = {}
    man = jl(os.path.join(root, 'manifest.json'))
    man_sha = sha256(os.path.join(root, 'manifest.json'))
    vcs = man.get('git') or {}
    B['manifest'] = dict(sha256=man_sha, launch_sha=vcs.get('sha'), launch_sha_len=len(vcs.get('sha') or ''), dirty=vcs.get('dirty'),
                         code_fp=(man.get('seal') or {}).get('code_fp'), expected_generation=man.get('expected_network_generation'),
                         observe_imports=man.get('observe_imports'), argv=man.get('argv'), input_digest=man.get('input_digest'),
                         cohorts=[c.get('name') for c in (man.get('plan') or {}).get('cohorts', [])], n_queue=len((man.get('plan') or {}).get('queue', [])))
    # ── §5-1 케이스 판정 (done / failed + failure_kind) ── merged status.json · parallel_cases.tsv · progress.tsv · worker.json · runs
    st_counts, fk, attempts, ok_null = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    cases_by_ds = {}
    for ds in sorted(os.listdir(os.path.join(root, 'merged'))):
        if not os.path.isdir(os.path.join(root, 'merged', ds)):
            continue
        st = jl(os.path.join(root, 'merged', ds, 'status.json'))
        cases_by_ds[ds] = sorted(st['cases'])
        for c, v in st['cases'].items():
            st_counts[(ds, v.get('status'))] += 1
            if v.get('status') != 'done':
                fk[(ds, v.get('failure_kind'), tuple(v.get('failed_stages') or []))] += 1
            #  단계 실패 = ok 가 False 이거나 rc 가 0 이 아닌 것 (웹앱 'Network Merge' 줄은 ok 칸 없이 rc 0 만 적는다 — app._network_merge_log ·
            #  v1.2 기록도 130 × (rc 0 · ok null) — 실패로 세지 않는다)
            bad_stage = [s for s in (v.get('stages') or []) if s.get('ok') is False or s.get('rc') not in (0, None)]
            for s in (v.get('stages') or []):
                if s.get('ok') is None:
                    ok_null[(ds, s.get('step'), s.get('rc'))] += 1
            if bad_stage:
                fk[(ds, 'stage_not_ok', tuple(s.get('step') for s in bad_stage))] += 1
        with open(os.path.join(root, 'merged', ds, 'parallel_cases.tsv'), encoding='utf-8') as f:
            pc = list(csv.DictReader(f, delimiter='\t'))
        for r in pc:
            attempts[(ds, r.get('attempts'), r.get('seal'))] += 1
    with open(os.path.join(root, 'progress.tsv'), encoding='utf-8') as f:
        pr = list(csv.DictReader(f, delimiter='\t'))
    runs = sorted(x for x in os.listdir(os.path.join(root, 'runs')) if x.endswith('.json'))
    run_kinds = [(x, jl(os.path.join(root, 'runs', x)).get('kind'), jl(os.path.join(root, 'runs', x)).get('outcomes'),
                  jl(os.path.join(root, 'runs', x)).get('code_changed_during_run'), jl(os.path.join(root, 'runs', x)).get('git_sha_end')) for x in runs]
    w_att = collections.Counter()
    for c in os.listdir(os.path.join(root, 'cases')):
        w = jl(os.path.join(root, 'cases', c, 'worker.json'))
        at = w.get('attempts') or []
        w_att[(len(at), (at[-1] if at else {}).get('outcome'), (at[-1] if at else {}).get('rc'))] += 1
    mr = jl(os.path.join(root, 'merged', 'merge_report.json'))
    B['s5_1'] = dict(status={f'{k[0]}:{k[1]}': v for k, v in sorted(st_counts.items())},
                     failures={f'{k[0]}:{k[1]}:{"|".join(k[2])}': v for k, v in fk.items()},
                     stages_ok_null={f'{k[0]}:{k[1]}:rc={k[2]}': v for k, v in sorted(ok_null.items(), key=str)},
                     parallel_cases_attempts_seal={f'{k[0]}:attempts={k[1]}:seal={k[2]}': v for k, v in sorted(attempts.items())},
                     progress_rows=len(pr), progress_outcomes=dict(collections.Counter(r['outcome'] for r in pr)),
                     progress_attempt_values=dict(collections.Counter(r['attempt'] for r in pr)),
                     runs=run_kinds, worker_attempts=[(f'n_attempts={k[0]} outcome={k[1]} rc={k[2]}', v) for k, v in w_att.items()],
                     merge_report=dict(counts={k: v['counts'] for k, v in mr['cohorts'].items()}, failures=mr.get('failures'), anomalies=mr.get('anomalies'),
                                       structural=mr.get('structural'), mixed_generation=mr.get('mixed_generation'),
                                       code_changed_since_launch=mr.get('code_changed_since_launch'), eligibility=mr.get('eligibility'),
                                       seal_verdicts=(mr.get('seal') or {}).get('verdicts')))
    # ── §5-2 감사 — 등록 §4 덧붙임 스니펫 그대로 (194 등록 263–275 줄) ──
    sa = jl(os.path.join(root, 'seal_audit.json'))
    o = sa['import_observation']
    sb = o['stage_binding']['attempts']
    comp = {'|'.join(map(str, k)) for k in o['completed_attempts']}
    B['s5_2_registered_snippet'] = {
        '케이스': len(sa['cases']), '판정': sa['verdicts'],
        '결합 = 완료 시도': [set(sb) == comp, len(sb), len(comp)],
        'expected ≠ observed': [k for k, r in sb.items() if r.get('expected') != r.get('observed')][:5],
        '감사 문제': sa['import_observation_problems'][:5],
        '완료 아닌 시도의 미최종 영수증 (정보 · Q2)': len(o['unfinalized_noncompleted']),
        '시작 · 끝맺음 (재시도 없으면 같다)': [o['n_started'], o['n_finalized']],
    }
    B['s5_2_fields'] = dict(schema=sa.get('schema'), eligibility=sa.get('eligibility'), merged=sa.get('merged'),
                            generation_declared=sa.get('generation_declared'), expected_network_generation=sa.get('expected_network_generation'),
                            generation_problems=sa.get('generation_problems'), input_problems=sa.get('input_problems'),
                            code_root_changed_now=sa.get('code_root_changed_now'), recorded_root=sa.get('root'), seal_fp=sa.get('seal_fp'),
                            launch_sha=sa.get('launch_sha'), case_generations=dict(collections.Counter(r.get('generation') for r in sa['cases'])),
                            obs_outside=o.get('outside'), obs_problems=o.get('problems'), obs_tmp_leftover=o.get('tmp_leftover'),
                            n_processes=o.get('n_processes'))
    # ── §5-3 다시 읽기 기록 ──
    rr = jl(os.path.join(root, 'reread.json'))
    case_fail = [(c['case'], [k['name'][:3] for k in c['checks'] if not k.get('ok')]) for c in rr['cases'] if not all(k.get('ok') for k in c['checks'])]
    B['s5_3_fields'] = dict(schema=rr.get('schema'), n_fail=rr.get('n_fail'), expected_set=rr.get('expected_set'), expected_n=rr.get('expected_n'),
                            read_n=rr.get('read_n'), set_equal=rr.get('set_equal'), missing=rr.get('missing'), extra=rr.get('extra'),
                            meta_all_ok=all(m.get('ok') for m in rr['meta']), meta_names=[m['name'][:40] for m in rr['meta']],
                            n_cases=len(rr['cases']), cases_with_failed_checks=case_fail,
                            check_ids_per_case=sorted({k['name'][:2] for c in rr['cases'] for k in c['checks']}),
                            recorded_launcher_root=rr.get('launcher_root'),
                            manifest_sha256_eq_bundle_manifest=(rr.get('manifest_sha256') == man_sha),
                            seal_fp_eq_manifest=(rr.get('seal_fp') == (man.get('seal') or {}).get('code_fp')),
                            launch_sha_eq_manifest=(rr.get('launch_sha') == vcs.get('sha')),
                            generations=dict(collections.Counter(c.get('generation') for c in rr['cases'])))
    # ── ⓪ · ⓪b 배포 관문 같은 함수 (경로 결합 두 칸은 사본 위치라 다를 수밖에 없다) ──
    rec, probs = L.v13_batch_gate_problems(root, eset)
    path_only = [p for p in probs if (p.startswith('seal_audit.json — root ') or p.startswith('reread.json — launcher_root ')) and '≠ 이 배치 뿌리' in p]
    B['gate_same_function'] = dict(n_problems=len(probs), path_binding_only=len(path_only), other_problems=[p for p in probs if p not in path_only],
                                   files={k: (None if v is None else {kk: vv for kk, vv in v.items() if kk in ('sha256', 'read')}) for k, v in rec.items()})
    # ── τ 상태 (§5-4 · §9-8 ④⑤⑥) — 다시 읽기 H1 의 load_tau_results 칸 (row_cells) ──
    rows_by_ds = collections.defaultdict(list)
    branch = collections.Counter()
    for c in rr['cases']:
        r = dict(c['row_cells'])
        r[L.KEY] = c['case']
        rows_by_ds[c['cohort']].append(r)
        for mode, t in (c.get('table') or {}).items():
            for br, v in t.items():
                branch[(c['cohort'], mode, br, v.get('status'), v.get('reason'))] += 1
        tsv_rows.append(dict(dataset=c['cohort'], case_id=c['case'],
                             **{f'ion_net_status_{m}': r.get(f'ion_net_status_{m}', '') for m in MODES},
                             **{f'ion_net_status_reason_{m}': r.get(f'ion_net_status_reason_{m}', '') for m in MODES},
                             full_model_limit_hertz=r.get('full_model_limit_hertz', ''), full_model_limit_physics=r.get('full_model_limit_physics', ''),
                             ion_net_band_rule_hertz=r.get('ion_net_band_rule_hertz', ''), ion_net_basis_check_hertz=r.get('ion_net_basis_check_hertz', ''),
                             ion_net_generation=r.get('ion_net_generation', '')))
    T = B['tau'] = {}
    for ds, rows in sorted(rows_by_ds.items()):
        d = T[ds] = {'n': len(rows)}
        for m in MODES:
            d[f'status_{m}'] = L._v13_status_counts(rows, f'ion_net_status_{m}')
            d[f'reason_{m}'] = dict(collections.Counter(r.get(f'ion_net_status_reason_{m}', '') for r in rows))
        d['model_limit_fact_hertz'] = sorted(r[L.KEY] for r in rows if L.v13_model_limit(r, 'hertz'))
        d['model_limit_fact_physics_n'] = sum(1 for r in rows if L.v13_model_limit(r, 'physics'))
        d['model_limit_status_h12_n'] = sum(1 for r in rows if L._v13_is_model_limit(r, 'hertz_h12'))
        d['primary_model_limit_problems'] = L.v13_primary_model_limit_problems(rows)
        d['flag_values'] = {f: dict(collections.Counter(r.get(f, 'ABSENT') for r in rows)) for f in ('full_model_limit_hertz', 'full_model_limit_physics')}
        d['band_rule'] = {m: dict(collections.Counter(r.get(f'ion_net_band_rule_{m}', '') for r in rows)) for m in MODES}
        d['basis_check'] = {m: dict(collections.Counter(r.get(f'ion_net_basis_check_{m}', '') for r in rows)) for m in MODES}
        d['const'] = {k: dict(collections.Counter(r.get(k, '') for r in rows)) for k in ('ion_sigma0_mScm', 'ion_sigma0_T_C', 'phi_basis', 'L_basis', 'ion_net_generation')}
        d['hertz_target_available_value_status'] = sum(1 for r in rows if r.get('ion_net_status_hertz') in L._V13_VALUE_STATUSES and r.get('f_ion_hertz', '') != '')
        d['hertz_nonperc_f_zero'] = sum(1 for r in rows if r.get('ion_net_status_hertz') == 'NOT_PERCOLATING' and r.get('f_ion_hertz', '') not in ('',))
        d['hertz_f_blank'] = sorted(r[L.KEY] for r in rows if r.get('f_ion_hertz', '') == '')
        d['mbcb_cases'] = {m: sorted(r[L.KEY] for r in rows if r.get(f'ion_net_status_{m}') == 'MODEL_BELOW_CONTINUUM_BOUND') for m in MODES}
    B['branch_table'] = {f'{k[0]}|{k[1]}|{k[2]}|{k[3]}|{k[4]}': v for k, v in sorted(branch.items(), key=lambda kv: tuple(str(x) for x in kv[0]))}
    # 레코드 수준 채널 (metrics_flat — 전자 · 열 FULL 상태도 §9-8 ① 범주 · 값 칸이 아닌 상태 · 사유 기록)
    ch = {}
    for ds in sorted(cases_by_ds):
        with open(os.path.join(root, 'merged', ds, 'metrics_flat.csv'), encoding='utf-8', newline='') as f:
            mf = list(csv.DictReader(f))
        cols = ('ionic_channel_verdict', 'electronic_channel_verdict', 'thermal_channel_verdict', 'network_solver_status', 'failed_channels',
                'network_dual.hertzian.sigma_full_status', 'network_dual.hertzian.sigma_full_reason',
                'network_dual.physics.sigma_full_status', 'network_dual.physics.sigma_full_reason',
                'network_dual.hertzian.electronic_sigma_full_status', 'network_dual.hertzian.electronic_sigma_full_reason',
                'network_dual.physics.electronic_sigma_full_status', 'network_dual.physics.electronic_sigma_full_reason',
                'network_dual.hertzian.thermal_sigma_full_status', 'network_dual.hertzian.thermal_sigma_full_reason',
                'network_dual.physics.thermal_sigma_full_status', 'network_dual.physics.thermal_sigma_full_reason')
        ch[ds] = {c_: dict(collections.Counter(r.get(c_, 'ABSENT') for r in mf)) for c_ in cols}
        ch[ds]['n_rows'] = len(mf)
        ch[ds]['electronic_model_limit_cases'] = {
            m: sorted(r['case'] for r in mf if r.get(f'network_dual.{m}.electronic_sigma_full_reason') == 'full_over_conduction')
            for m in ('hertzian', 'physics')}
    B['metrics_flat_channels'] = ch

os.makedirs(a.out, exist_ok=True)
with open(os.path.join(a.out, 's5_summary.json'), 'w', encoding='utf-8') as f:
    json.dump(summ, f, ensure_ascii=False, indent=1, default=list)
cols = list(tsv_rows[0])
with open(os.path.join(a.out, 'tau_status_by_case.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter='\t', lineterminator='\n')
    w.writeheader()
    for r in sorted(tsv_rows, key=lambda r: (r['dataset'], r['case_id'])):
        w.writerow(r)
print('ok', os.path.join(a.out, 's5_summary.json'), len(tsv_rows))
