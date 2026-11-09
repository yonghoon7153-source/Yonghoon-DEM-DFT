"""s_min 준비 자료 숫자 (읽기 전용) — 입력: 리포 kit JSON · NPZ_SHA256.txt · SHA256SUMS · 스크래치 npz 둘.
실행: python3 -I tools/smin_numbers.py <repo> <npz_dir> <out.json>
σ 값은 읽지 않는다 (단계 1 = census 뿐)."""
import hashlib, json, math, sys
import numpy as np

repo, npz_dir, out = sys.argv[1], sys.argv[2], sys.argv[3]
data = repo + '/docs/data/rint2_s0_sbe_20261108'
kit_rel = 'docs/data/rint2_s0_sbe_20261108/files/sdcp/ca1_s0_sbe_20261106_memfix/s0_stage1_kit_SBE_vgcf100.json'
kit = repo + '/' + kit_rel


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


import os
res = {'what': 's_min 개발 단계 준비 숫자 (11-09 · 읽기 전용 · σ 없음 · 결정 아님)'}
# ── 자료 신원 ──
sums = {}
for line in open(data + '/SHA256SUMS'):
    h, p = line.split(None, 1)
    sums[p.strip()] = h
npzsums = {}
for line in open(data + '/NPZ_SHA256.txt'):
    h, n, p = line.split()
    npzsums[os.path.basename(p)] = (h, int(n))
kit_sha = sha(kit)
ident = {'kit_json_repo_path': kit_rel, 'kit_json_sha256': kit_sha, 'kit_json_bytes': os.path.getsize(kit),
         'kit_json_sha256_in_SHA256SUMS': sums.get('files/sdcp/ca1_s0_sbe_20261106_memfix/s0_stage1_kit_SBE_vgcf100.json'),
         'kit_json_kgy_path': '/home/kgy/sdcp/ca1_s0_sbe_20261106_memfix/s0_stage1_kit_SBE_vgcf100.json (run.log 의 출력 폴더)',
         'npz': {}}
ident['kit_json_sha_match'] = ident['kit_json_sha256'] == ident['kit_json_sha256_in_SHA256SUMS']
for nm in ('s0_junctions_kit_SBE_vgcf100.npz', 's0_instances_kit_SBE_vgcf100.npz'):
    p = npz_dir + '/' + nm
    got = sha(p)
    ident['npz'][nm] = {'sha256': got, 'bytes': os.path.getsize(p), 'expected_sha256': npzsums[nm][0],
                        'expected_bytes': npzsums[nm][1], 'match': got == npzsums[nm][0] and os.path.getsize(p) == npzsums[nm][1]}
res['identity'] = ident
if not (ident['kit_json_sha_match'] and all(v['match'] for v in ident['npz'].values())):
    raise SystemExit('sha 불일치 — 멈춤')

d = json.load(open(kit))
J = d['junction_census']
C = J['census']
res['identity'].update({'schema': d['schema'], 'stage': d['stage'], 'tool': d['tool'], 'kit_name': d['kit']['name'],
                        'plan_sha256': d['plan']['sha256'], 'plan_source': d['plan']['source'],
                        'code_git_head': d['code']['git_head'], 'code_git_dirty': d['code']['git_dirty'],
                        'python': d['code']['python'], 'numpy': d['code']['numpy'], 'scipy': d['code']['scipy'],
                        'elapsed_s': d['elapsed_s'],
                        'source_tgz_sha256': 'd48f55c1b6884a75f011e9517d3f592c25aecf8a73d7a02ebbbee86eaede0a13 (README.md · ADOPTION_CHECK.md)',
                        'repo_import_commit': '4d76378b9'})
# ── 문턱 · 기하 상수 ──
th = J['thresholds']
r_f, tol_ff, L_par = th['r_f_um'], th['tol_ff_um'], th['L_par_um']
D = 2.0 * r_f + tol_ff
ti = d['threshold_inputs']
res['thresholds'] = {'r_f_um': r_f, 'tol_ff_um': tol_ff, 'u_um': ti['u_um'], 'L_par_um': L_par, 'r_port_um': th['r_port_um'],
                     'gap_tol': th['gap_tol'], 's_min_um_in_stage1': th['s_min_um'], 'vox_um': d['raster']['convention']['vox_um'],
                     'spacing_median_um': ti['spacing_median_um'], 'spacing_p10_um': ti['spacing_p10_um'],
                     'spacing_p90_um': ti['spacing_p90_um'], 'spacing_max_um': ti['spacing_max_um'], 'n_spacings': ti['n_spacings'],
                     'D_um (= 2 r_f + tol_ff · 탐지 거리 · 바닥의 s > D)': D,
                     'halfpi_D_um (= (π/2)·D · B0 미리보기 자기 접촉 호 하한)': 0.5 * math.pi * D,
                     'halfpi_2rf_um (= (π/2)·2r_f · 닿는 두 다리 반원 호)': 0.5 * math.pi * 2.0 * r_f,
                     'floor_vertex_angle_deg (= 2·asin(2/π) · `_self_floor` docstring 의 79°)': math.degrees(2.0 * math.asin(2.0 / math.pi)),
                     'fibre_diameter_um': 2.0 * r_f}
# ── 같은 가닥 (자기) 후보 ──
with np.load(npz_dir + '/s0_junctions_kit_SBE_vgcf100.npz', allow_pickle=False) as z:
    is_self = z['is_self']; s = z['s']; dk = z['self_dk_min']; nrv = z['self_n_revisit']; n_rows = int(len(is_self))
with np.load(npz_dir + '/s0_instances_kit_SBE_vgcf100.npz', allow_pickle=False) as z:
    prev_self = int(np.sum(z['is_self'])); prev_rows = int(len(z['is_self']))
longc = J['long_contacts']
kinds = {}
for x in longc:
    kinds[x['kind']] = kinds.get(x['kind'], 0) + 1
s_self = s[is_self]
s_fin = s_self[np.isfinite(s_self)]
qs = [1, 5, 10, 25, 50, 75, 90, 95, 99]
res['self_candidates'] = {
    'json.census.n_self_candidates': C['n_self_candidates'], 'json.census.n_self_kept': C['n_self_kept'],
    'json.census.n_self_filtered': C['n_self_filtered'], 'json.census.self_s_um': C['self_s_um'],
    'json.census.self_filter': C['self_filter'], 'json.census.n_instances_self': C['n_instances_self'],
    'json.census.n_cut_self_faces': C['n_cut_self_faces'], 'json.census.self_dk_min': C['self_dk_min'],
    'json.self_candidates_len': len(J['self_candidates']), 'json.self_s_um': J['self_s_um'],
    'json.n_long_self': J['n_long_self'], 'json.Lc_self_um': J['Lc_self_um'],
    'json.rejection_codes': J['rejection_codes'], 'json.s_min_status': J['s_min_status'],
    'npz_junctions.rows': n_rows, 'npz_junctions.is_self_true': int(np.sum(is_self)),
    'npz_junctions.s_finite': int(np.sum(np.isfinite(s))), 'npz_junctions.self_dk_min_ne_-1': int(np.sum(dk != -1)),
    'npz_junctions.self_n_revisit_sum': int(np.sum(nrv)),
    'npz_instances(B0 미리보기).rows': prev_rows, 'npz_instances(B0 미리보기).is_self_true': prev_self,
    'json.census_preview.vv.n_self': d['census_preview']['vv']['n_self'],
    'json.long_contacts_kind_counts': kinds,
    'json.long_contacts_s_um_non_null': int(sum(1 for x in longc if x['s_um'] is not None)),
    'n_used_for_quantiles': int(len(s_fin)),
    'quantiles_um': {f'p{q}': (float(np.percentile(s_fin, q)) if len(s_fin) else None) for q in qs},
    'min_um': (float(s_fin.min()) if len(s_fin) else None), 'max_um': (float(s_fin.max()) if len(s_fin) else None)}
# 로그 칸 (자기 후보 s) — 0 건이라 칸마다 0
edges = [0.0] + [10.0 ** (k / 4.0) for k in range(-8, 5)] + [math.inf]   # 0 · 0.01 … 10 µm (10^(1/4) 간격) · ∞
res['self_s_hist_um'] = [{'lo': lo, 'hi': (hi if math.isfinite(hi) else 'inf'), 'n': int(np.sum((s_fin >= lo) & (s_fin < hi)))}
                         for lo, hi in zip(edges[:-1], edges[1:])]
res['threshold_table'] = [{'s_min_um': v, 'label': lb, 'SBE_self_junctions': int(np.sum(s_fin >= v)) if len(s_fin) else 0,
                            'SBE_self_candidates_total': int(len(s_fin)), 'equivalent_to_floor_only': v <= D}
                           for v, lb in ((0.0, '0'), (J['revisit']['s_um']['max'], '재방문 s 최대 (쌍별 호 간격 · 정의 다름)'), (D, 'D'), (0.5 * math.pi * 2.0 * r_f, '(π/2)·2r_f'),
                                         (L_par, 'L_par'), (0.5 * math.pi * D, '(π/2)·D'), (0.5, '0.5'), (1.0, '1.0'))
                           if v is not None] 
# ── 같은 셀 비연속 재방문 (census 요약만 · 쌍별 값 = 보고에 없음) ──
rv = J['revisit']
rvs = rv['s_um']
res['revisit'] = {'n_pairs': rv['n_pairs'], 'n_cells': rv['n_cells'], 'n_fibres': rv['n_fibres'], 'n_path_only': rv['n_path_only'],
                  'n_path_broken': C['n_self_revisits_path_broken'], 's_um_summary': rvs,
                  'quantiles_available': {'p0': rvs['min'], 'p50': rvs['median'], 'p100': rvs['max']},
                  'quantiles_not_in_report': [f'p{q}' for q in qs if q != 50],
                  'max_lt_D': rvs['max'] < D, 'max_over_D': rvs['max'] / D,
                  'partial_hist': {'n_le_median (짝수 n → 중앙값 = 437 · 438 번째 평균 → 437 개 이하 쪽 · 437 개 이상 쪽)': 437,
                                   'n_ge_median': 437, 'all_in_um': [rvs['min'], rvs['max']],
                                   'n_ge_D': 0, 'fibre_share': rv['n_fibres'] / C['n_vgcf_fibres']},
                  'rule': rv['rule'], 's_definition': '`_pos_pair_sd` (carbon_junction.py:1420–1433) — 두 위치의 셀 조각 사이 최소 호 간격 '
                                                     '(≠ 자기 쌍 s = 최근접점 사이 호 · `CJUNC_SELF_S_RULE`)'}
# ── 면 ──
res['faces'] = {'n_self_fused_faces (같은 조각 · 축방향 아님 · 바닥 밖 = 연속 · s_min 무관)': C['n_self_fused_faces'],
                'n_cut_self_faces': C['n_cut_self_faces'], 'n_unreg_faces (다른 조각 미등록 + 같은 조각 바닥 통과 면 · 보고가 가르지 않음)': C['n_unreg_faces'],
                'n_cut_site_faces': C['n_cut_site_faces']}
# ── 침대 규모 ──
res['bed'] = {k: C[k] for k in ('n_vgcf_fibres', 'n_pieces', 'n_segments', 'n_positions', 'n_instances', 'n_instances_distinct',
                                'n_instances_self', 'n_piece_cell_meets', 'n_instances_same_fid_pieces', 'n_ring_pieces',
                                'n_closed_paths_joined', 'n_seam_alias', 'n_long_distinct', 'n_long_self')}
res['bed']['n_long'] = J['n_long']
# ── 후보 규칙 ──
r_prime = 56.58842421   # Ω/µm · 설계 §4-1 (VGCF 1e4 S/cm · Ø0.15 µm · = 복셀 7,853.98 S/cm × vox²)
cands = [
    ('A0', '바닥만 (추가 거르기 없음) — 0', 0.0),
    ('A1', '바닥만 — 표기를 D 로 (동작 = A0)', D),
    ('A2', '재방문 s 최대 위 (동작 = A0 · 최대 0.190 < D)', rvs['max']),
    ('B', 'L_par (= 2(r_fi + r_fj) · 등록 고정 0.30)', L_par),
    ('C', '(π/2)·D (검출 거리 반원 · B0 미리보기 정의)', 0.5 * math.pi * D),
]
rows = []
for cid, name, v in cands:
    eff = 'floor_only (s_min ≤ D ≡ 0)' if v <= D else 'extra_filter (D < s < s_min 인 바닥 쌍 = 연속)'
    adm = int(np.sum(s_fin >= v)) if len(s_fin) else 0
    rows.append({'id': cid, 'rule': name, 's_min_um': v, 'effective_class': eff, 'SBE_self_junctions_admitted': adm,
                 'SBE_self_candidates_excluded': int(len(s_fin)) - adm, 'r_prime_times_s_ohm': r_prime * v})
res['candidates'] = rows
res['r_prime_ohm_per_um (설계 §4-1 · 추정 해석용)'] = r_prime
res['notes'] = ['자기 후보 0 건 → 어느 s_min 에서도 SBE 자기 접합 0 (받아들임 0 · 거름 0)',
                's_min ≤ D 는 모두 같은 동작 (바닥이 s > D 를 이미 요구 · carbon_junction.py:200–207 · 1387–1393 · 1460–1465)',
                '재방문 쌍별 s 값 · 같은 조각 바닥 통과 면 수 = S0 보고에 없음 (원 킷 입력으로 다시 세어야 · σ 없음)']
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k: res[k] for k in ('identity',)}, ensure_ascii=False, indent=1)[:1500])
print('D', D, 'halfpi_D', 0.5 * math.pi * D)
print(json.dumps(res['self_candidates'], ensure_ascii=False)[:1500])
print(json.dumps(res['candidates'], ensure_ascii=False, indent=0))
