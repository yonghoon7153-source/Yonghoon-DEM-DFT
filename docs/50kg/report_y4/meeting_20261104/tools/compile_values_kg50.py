"""50kg D1 · D2 · D3 값 대응표 — 이종기술 3세부 2차년도 중간 발표 (10-13 · 13–19쪽) 의 DEM 지표를 같은 정의로 (1저자 11-02 "여기에 들어간 모든 값이 필요해").

새 계산 없음 — 값 = draft2 metrics_<침대>.json · 끝 덱 (kg50_y4_sources.parse_deck) · values/szz_share/plane_load.json (szz_share_kg50.py) 의 옮김뿐.
usage: python3 -I compile_values_kg50.py <리포> → <리포>/docs/50kg/report_y4/meeting_20261104/values/values_D123.csv (+ 화면 표)
"""
import csv
import json
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(REPO / 'docs/50kg/report_y4'))
sys.path.insert(0, str(REPO / 'scripts'))
import kg50_y4_sources as src  # noqa: E402

OUT = REPO / 'docs/50kg/report_y4/meeting_20261104/values'
BEDS = [('D3', 'SE3um', '3 µm'), ('D2', 'SE2um', '2 µm'), ('D1', 'SE1um', '1 µm')]
SIGMA0_REPORT = 1.5          # mS/cm — 보고 기준 (1저자 10-12) · f × 1.5 = 절대 유효 이온전도도
M = {b: json.loads((REPO / f'docs/50kg/report_y4/draft2/data/{b}/metrics_{b}.json').read_text(encoding='utf-8')) for b, _, _ in BEDS}
PL = json.loads((OUT / 'szz_share/plane_load.json').read_text(encoding='utf-8'))
DK = {}
for bd in src.BEDS:
    for b, _, _ in BEDS:
        if bd['case'] == M[b]['case']:
            DK[b] = src.parse_deck((REPO / bd['deck']).read_text(encoding='utf-8'), bd['case'])

rows = []


def add(page, item, unit, fn, src_note, nd=None):
    vals = []
    for b, lab, _ in BEDS:
        try:
            v = fn(b, lab)
        except (KeyError, TypeError):
            v = None
        vals.append(v)
    rows.append(dict(page=page, item=item, unit=unit, vals=vals, src=src_note, nd=nd))


m = lambda b, k: M[b]['metrics'][k]
cp = lambda b, k: M[b]['compaction'][k]
lw = lambda b, ph, k: M[b]['aggregates']['love_weber']['by_phase_MPa'][ph]['nowall'][k]
plc = lambda lab: PL['cases'][lab] if PL['cases'][lab].get('status') in ('OK', 'CHECK') else None   # CHECK = 값은 내되 사유 (아래 상태 행)

# p14 — 해석 조건
add('14 조건', '복합양극 크기 (L × W)', 'µm', lambda b, l: f"{DK[b]['box_x_um']:g} × {DK[b]['box_y_um']:g}", '끝 덱')
add('14 조건', '면적당 용량 (설계)', 'mAh/cm²', lambda b, l: 6.5, 'docs/50kg/dem_plan_20261026.md §0 (덱 manifest 예상 6.50)')
add('14 조건', '가압 압력', 'MPa', lambda b, l: DK[b]['target_MPa'], '끝 덱')
add('14 조건', 'NCM 입경', 'µm', lambda b, l: DK[b]['d_am_um'], '끝 덱 (단일 입경)')
add('14 조건', '고체전해질 입경 (D50)', 'µm', lambda b, l: DK[b]['d50_se_um'], '끝 덱 (단일 입경)')
add('14 조건', 'NCM 함량', 'wt%', lambda b, l: 100 * DK[b]['w_am'], '끝 덱')
add('14 조건', '입자 수 (NCM + SE)', '개', lambda b, l: M[b]['inventory']['n_am'] + M[b]['inventory']['n_se'], 'atom_end')
add('14 조건', '  NCM 입자 수', '개', lambda b, l: M[b]['inventory']['n_am'], 'atom_end')
add('14 조건', '  SE 입자 수', '개', lambda b, l: M[b]['inventory']['n_se'], 'atom_end')
add('14 조건', '진밀도 NCM / SE', 'g/cm³', lambda b, l: f"{DK[b]['rho_am_gcc']:g} / {DK[b]['rho_se_gcc']:g}", '끝 덱')
add('14 조건', '영률 NCM / SE (해석 입력)', 'GPa', lambda b, l: f"{DK[b]['E_am_GPa']:g} / {DK[b]['E_se_GPa']:g}", '끝 덱 — SE 1.35 = 유효 영률 (재료값 22 의 연화 대리)')
add('14 조건', '푸아송비 NCM / SE', '—', lambda b, l: f"{DK[b]['nu'][0]:g} / {DK[b]['nu'][2]:g}", '끝 덱')
# p15 — 가압 · 두께
add('15 가압', '가압 시작 판 높이', 'µm', lambda b, l: cp(b, 'plate_z0_um'), 'compaction (로그)', 2)
add('15 가압', '판 정지 높이 (= 이완 끝)', 'µm', lambda b, l: cp(b, 'z_end_mesh_um'), 'mesh_end', 2)
add('15 가압', '두께 감소율 (가압 시작 대비)', '%', lambda b, l: 100 * (1 - cp(b, 'z_end_mesh_um') / cp(b, 'plate_z0_um')), '위 두 값', 1)
add('15 가압', '판 정지 직전 압력', 'MPa', lambda b, l: cp(b, 'p_t0minus_MPa'), '로그 thermo', 1)
add('15 가압', '이완 첫 출력 압력', 'MPa', lambda b, l: cp(b, 'p_relax_first_MPa'), '로그 thermo', 1)
add('15 가압', '이완 끝 판 압력', 'MPa', lambda b, l: cp(b, 'p_end_MPa'), '로그 thermo (1 µm 156 — 아래 주의)', 1)
add('15 가압', '질량 보존 두께', 'µm', lambda b, l: m(b, 'thickness_mass_conserving_um'), 'metrics', 2)
# p16 — 응력 분포
add('16 응력', 'NCM von Mises 응력 중앙값 (벽 접촉 제외)', 'MPa', lambda b, l: lw(b, 'AM', 'median'), 'Love–Weber 입자 응력', 0)
add('16 응력', 'SE von Mises 응력 중앙값 (벽 접촉 제외)', 'MPa', lambda b, l: lw(b, 'SE', 'median'), 'Love–Weber 입자 응력', 0)
add('16 응력', 'NCM von Mises p10 – p90', 'MPa', lambda b, l: f"{lw(b, 'AM', 'p10'):.0f} – {lw(b, 'AM', 'p90'):.0f}", 'Love–Weber')
add('16 응력', 'SE von Mises p10 – p90', 'MPa', lambda b, l: f"{lw(b, 'SE', 'p10'):.0f} – {lw(b, 'SE', 'p90'):.0f}", 'Love–Weber')
add('16 응력', '입자 응력 변동계수 (전체)', '%', lambda b, l: m(b, 'lw_cv_pct'), 'Love–Weber', 1)
# p17 — 미세구조
add('17 미세구조', '기공도 (정확 합집합)', '%', lambda b, l: m(b, 'eps_union_exact_pct'), 'calc_porosity_union_exact', 1)
add('17 미세구조', 'AM coverage', '%', lambda b, l: m(b, 'coverage_physics_union_pct'), 'union_coverage_bed (덱 값)', 1)
add('17 미세구조', '수송 tortuosity', '—', lambda b, l: m(b, 'tau2_ion_hertz'), 'φ_SE·σ₀/σ_eff (제곱근 아님)', 2)
add('17 미세구조', '기하 tortuosity (최단 경로 / 두께)', '—', lambda b, l: m(b, 'tau_geo_all'), 'calc_tortuosity_all', 3)
add('17 미세구조', 'SE 부피 분율 (질량 보존)', '—', lambda b, l: m(b, 'phi_se_mass_conserving'), 'metrics', 4)
add('17 미세구조', 'NCM 부피 분율 (질량 보존)', '—', lambda b, l: m(b, 'phi_am_mass_conserving'), 'metrics', 4)
# p18 — 접촉 · 응력 분담
add('18 접촉·응력', 'CN AM–SE (NCM 1개당 SE 접촉 수)', '개', lambda b, l: m(b, 'am_se_cn_mean'), 'calc_am_isolation_risk', 1)
add('18 접촉·응력', 'CN SE–SE (SE 1개당)', '개', lambda b, l: m(b, 'se_se_cn_mean'), 'calc_se_se_cn', 2)
add('18 접촉·응력', 'CN AM–AM (NCM 1개당)', '개', lambda b, l: m(b, 'am_am_cn_mean'), 'metrics', 2)
add('18 접촉·응력', 'AM–SE 접촉 1개 면적 (평균)', 'µm²', lambda b, l: m(b, 'area_am_se_per_contact_mean_um2'), 'c_cpl[22]', 3)
add('18 접촉·응력', 'NCM 1개당 AM–SE 접촉 면적 (평균)', 'µm²', lambda b, l: m(b, 'area_am_se_per_am_mean_um2'), 'c_cpl[22]', 1)
for g in ('AM–AM', 'AM–SE', 'SE–SE'):
    add('18 접촉·응력', f'σzz 기여 {g}', '%', lambda b, l, g=g: plc(l)['contribution_sigma_zz_pct'][g], 'plane_load_share (21 단면)', 1)
add('18 접촉·응력', '단면 수직응력 σzz (21 단면 평균)', 'MPa', lambda b, l: plc(l)['sigma_zz_planes_mean_mpa'], 'plane_load_share', 1)
add('18 접촉·응력', 'σzz 계산 상태 (단면 하중 보존 최대÷최소)', '—', lambda b, l: f"{plc(l)['status']} ({plc(l)['conservation_max_over_min']:.4f})", 'plane_load_share — 보존 허용 1.02 · 1 µm = 이완 끝 판 압력 156 MPa 상태')
add('18 접촉·응력', '응력 감소 계수 α NCM / SE', '—', lambda b, l: f"{plc(l)['alpha']['alpha_zz']['AM']:.3f} / {plc(l)['alpha']['alpha_zz']['SE']:.3f}", 'plane_load_share α')
# p19 — 전하 수송
add('19 이온 수송', '정규화 유효 이온전도도 σ_eff/σ₀', '—', lambda b, l: m(b, 'f_ion_hertz'), 'f_mc (Hertz)', 5)
add('19 이온 수송', '  3 µm 대비', '배', lambda b, l: m(b, 'f_ion_hertz') / M['D3']['metrics']['f_ion_hertz'], '위 값의 비', 2)
add('19 이온 수송', f'유효 이온전도도 σ_Li+ (σ₀ = {SIGMA0_REPORT} mS/cm)', 'mS/cm', lambda b, l: SIGMA0_REPORT * m(b, 'f_ion_hertz'), 'f × 1.5 (보고 기준 · 전해질 물성 동일 가정)', 4)
add('19 이온 수송', '협착 (SE–SE 접촉부) 저항 몫', '%', lambda b, l: 100 * m(b, 'constriction_power_share_ion_hertz'), 'constriction_power_share_ion_hertz', 1)
add('19 이온 수송', 'SE 망 관통 (위·아래 연결) 입자 비율', '%', lambda b, l: m(b, 'percolation_pct'), 'calc_percolation', 1)
add('19 이온 수송', 'SE 망과 연결된 NCM', '%', lambda b, l: m(b, 'se_connected_am_pct'), 'calc_ionic_active_am', 0)
add('19 이온 수송', 'pellet 이온전도도 (3차년도 실측)', 'mS/cm', lambda b, l: {'D3': 5.1, 'D2': None, 'D1': 2.3}[b], 'dem_plan §0 (킥오프 · 측정 조건 미기록)')


def fmt(v, nd):
    if v is None:
        return '—'
    if isinstance(v, str):
        return v
    if nd is None:
        return f'{v:g}' if isinstance(v, float) else str(v)
    return f'{v:.{nd}f}'


with open(OUT / 'values_D123.csv', 'w', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh, lineterminator='\n')
    w.writerow(['이종기술 쪽', '항목', '단위', '3 µm (D3)', '2 µm (D2)', '1 µm (D1)', '출처'])
    for r in rows:
        w.writerow([r['page'], r['item'], r['unit']] + [fmt(v, r['nd']) for v in r['vals']] + [r['src']])
page = None
for r in rows:
    if r['page'] != page:
        page = r['page']
        print(f'\n### {page}\n| 항목 | 단위 | 3 µm | 2 µm | 1 µm |\n|---|---|---:|---:|---:|')
    print(f"| {r['item']} | {r['unit']} | " + ' | '.join(fmt(v, r['nd']) for v in r['vals']) + ' |')
