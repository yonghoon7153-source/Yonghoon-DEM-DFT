#!/usr/bin/env python3
"""CYCLE-STEP 3 — R_int(N) 합성: 접촉-몫(모델) + 화학-몫(측정) 분해.  (R_int 프로젝트 Phase 3)

A10 접촉-원장(cycle_contact_ledger.py)이 주는 **기계적 접촉-손실 몫**(R_ct 프록시 배율
rct_proxy_rel(N) = A0/A_N, CAM-SE 반응면 면적손실)을, 측정된 **총 R_int(N) 성장**(문헌 앵커,
CAM-SE 계면)과 겹쳐 성장의 기계 vs 화학 몫을 분해한다.  = R_geom 스플릿(bare-vs-wetted →
기하 몫)의 **사이클판**(mechanical-vs-total → 화학 몫).

물리 (rint_reference_growthlaw_design §3 additive):
    R_int(N) = R_contact(N) + R_chem(N)
    R_contact(N) = R_contact(0)·rct_proxy_rel(N)      ← A10 원장 (접촉 면적손실; 모델 출력)
    R_chem(N)    = interphase 성장 (Koerver 첫충전 점프 + g(N))  ← 측정/문헌 (모델 밖)
    R_contact(0) = f0·R_int(0)                        ← pristine 접촉 몫 (미지 → 스윕)

성장의 기계 몫 (f0 무관 상대비로도 유효):
    s_mech(N) = ΔR_mech(N)/ΔR_meas(N) = f0·(rct_rel(N)−1) / (R_rel_meas(N)−1)

⚠ §F1 정직:
  • 우리 원장 = LPSCl+NMC811 (Yun 2023이 동일 재료군 CAM-SE 총 R_int 앵커 = 최우선 대조).
    Kang&Shin = NCA (재료 다름) → mono/bimodal *아키텍처* 방향 대조에만 (절대 이식 금지).
  • rct_proxy_rel = 면적비 상대 프록시 (절대 Ω·cm² 아님).  f0 = pristine 접촉 몫 미지 →
    스윕(0.1–1.0) + 명목값 보고.  s_mech는 f0=1에서 상한.
  • collector R_int(SBE/DBE 110/46)은 *집전체* 계면(rint_cycle_traj 소관) — 여기 CAM-SE와 별개.

사용:
  python3 scripts/cycle_rint_synthesis.py --ledger cycle_bimodal.json --arch bimodal
  python3 scripts/cycle_rint_synthesis.py --ledger cycle_mono.json --ledger2 cycle_bimodal.json \\
          --measured yun --out rint_decomp        # 두 아키텍처 나란히
selftest:  python3 scripts/cycle_rint_synthesis.py --selftest
"""
import argparse
import csv
import json
import os

import numpy as np

# ── 측정 앵커 (CAM-SE 계면 총 R_int, N=100 규약; 전부 출판값 §F1) ──
#   value = R_int(N)/R_int(0) 성장 배율 궤적 {cycle: factor}, R0 = pristine Ω·cm² (있으면).
MEASURED = {
    'yun': dict(  # Yun 2023 ESM, NCM+LPSCl (우리 재료군!) — 0.33C 100cyc 2.5-4.3V
        material='NCM+LPSCl', arch='(unspec)', R0_ohm_cm2=341.7,
        traj={0: 1.0, 100: 982.3 / 341.7},  # +187% = 2.874×
        source='Yun 2023 ESM 59:102787 (R_int 341.7→982.3, +187%)', pdf='pdf_local'),
    'kang_bnca': dict(  # Kang&Shin 2025 ACS AMI, bimodal NCA(3+10µm) — 0.5C 100cyc
        material='NCA', arch='bimodal', R0_ohm_cm2=113.5,
        traj={1: 1.0, 25: 275.6 / 113.5, 50: 332.2 / 113.5, 75: 335.7 / 113.5, 100: 501.8 / 113.5},
        source='Kang&Shin 2025 ACS AMI TableS2 (113.5→501.8, 4.42×)', pdf='pdf_local'),
    'kang_unca': dict(  # 같은 논문, unimodal 3µm NCA
        material='NCA', arch='unimodal', R0_ohm_cm2=56.0,
        traj={1: 1.0, 100: 84.5 / 56.0},  # 1.51×
        source='Kang&Shin 2025 ACS AMI TableS3 (56.0→84.5, 1.51×)', pdf='pdf_local'),
}


def _interp_factor(traj, N):
    xs = sorted(traj)
    return float(np.interp(N, xs, [traj[x] for x in xs]))


def load_ledger(path):
    d = json.load(open(path))
    tr = d.get('trajectory')
    if not tr:                                                # 리뷰 #6/#8: 빈 궤적 명시 거부
        raise SystemExit(f'❌ {path}: trajectory 비었음 (cycle_contact_ledger 재실행 필요)')
    for k in ('cycle', 'rct_proxy_rel', 'f_broken_amse'):     # 리뷰 #7: 구버전 json 하드가드
        if k not in tr[0]:
            raise SystemExit(f'❌ {path}: 원장 키 "{k}" 없음 — 최신 cycle_contact_ledger.py로 재생성 필요')
    N = np.array([r['cycle'] for r in tr], float)
    holm = np.array([r['rct_proxy_rel'] for r in tr], float)  # Holm 구속 배율 (area^−0.5, 하한)
    # 전하이동(면적) 배율 (area^−1, 상한) — 구버전 json엔 없을 수 있어 fallback=holm
    ct = np.array([r.get('rct_ct_area_rel', r['rct_proxy_rel']) for r in tr], float)
    fbrk = np.array([r['f_broken_amse'] for r in tr], float)
    return dict(N=N, rct_holm=holm, rct_ct=ct, f_broken=fbrk, gamma=d.get('gamma_star', {}).get('value'),
                atoms=d.get('atoms', path), n_amse=d.get('n_contacts', {}).get('am_se'))


def synth(led, meas_key, f0_nom, f0_sweep):
    """성장의 기계 몫 밴드 = (저항규약 Holm↔CT) × (f0 스윕) 2D envelope.  측정 R_int 감소셀도 처리."""
    m = MEASURED[meas_key]
    rows = []
    for i, N in enumerate(led['N']):
        Rmeas = _interp_factor(m['traj'], N)
        d_meas = Rmeas - 1.0
        # 저항규약 두 끝 × f0 두 끝 = 4 조합의 기계 몫 → envelope (리뷰 #1: Holm 하한 / CT 상한)
        rcts = {'holm': led['rct_holm'][i], 'ct': led['rct_ct'][i]}
        shares = {}
        for rk, rct in rcts.items():
            for f0 in (f0_nom, *f0_sweep):
                # d_meas<0(측정 R 감소, LZO 등) 또는 ~0이면 성장 분해 불능 → None (리뷰 #2)
                shares[(rk, f0)] = (f0 * (rct - 1.0) / d_meas) if abs(d_meas) > 1e-6 and d_meas > 0 else None
        vals = [v for v in shares.values() if v is not None]
        s_nom = shares[('ct', f0_nom)] if shares.get(('ct', f0_nom)) is not None else None  # CT+명목 = 대표(측정 CT지배)
        s_nom_holm = shares.get(('holm', f0_nom))
        s_lo = min(vals) if vals else None
        s_hi = max(vals) if vals else None
        # additive 재구성 (대표=CT+명목 f0; R_chem 음수면 경고 플래그 — 리뷰 #4, clamp 대신 노출)
        rct_rep = rcts['ct']
        R_mech_rel = 1.0 + f0_nom * (rct_rep - 1.0)
        R_chem_rel = Rmeas - R_mech_rel
        chem_neg = R_chem_rel < -1e-9                          # 모델 기계가 측정 총 초과 = 규약 불일치 신호
        rows.append(dict(cycle=int(N), rct_holm_rel=round(rcts['holm'], 4), rct_ct_rel=round(rcts['ct'], 4),
                         R_int_rel_meas=round(Rmeas, 4),
                         mech_share_ct_nom=None if s_nom is None else round(s_nom, 4),
                         mech_share_holm_nom=None if s_nom_holm is None else round(s_nom_holm, 4),
                         mech_share_lo=None if s_lo is None else round(s_lo, 4),
                         mech_share_hi=None if s_hi is None else round(s_hi, 4),
                         R_mech_rel=round(R_mech_rel, 4), R_chem_rel=round(R_chem_rel, 4),
                         chem_negative_flag=bool(chem_neg),
                         R_int_ohm_cm2=round(m['R0_ohm_cm2'] * Rmeas, 1) if m.get('R0_ohm_cm2') else None))
    return rows, m


def run(a):
    leds = [('primary', load_ledger(a.ledger))]
    if a.ledger2:
        leds.append(('secondary', load_ledger(a.ledger2)))
    f0_sweep = [float(x) for x in a.f0_sweep.split(',')]
    m0 = MEASURED[a.measured]
    interp_note = ('측정 앵커가 N=0,100 2점뿐 → 중간 체크포인트 R_meas는 선형보간(실측 아님)'
                   if len(m0['traj']) <= 2 else '측정 궤적 다점')
    out = dict(model='CYCLE-STEP3 R_int synthesis', measured_key=a.measured,
               measured=m0, f0_nominal=a.f0_nom, f0_sweep=f0_sweep,
               caveats=[
                   '기계 몫 밴드 = 저항규약(Holm 1/√A 하한 ↔ 전하이동 R_ct 1/A 상한) × f0(pristine 접촉몫) 스윕. '
                   '측정 CAM-SE R_int는 전하이동 지배(Yun "계면반응 지배") → CT(area^−1)가 대표규약 (리뷰 #1).',
                   'f0=R_contact(0)/R_int(0) 이상화: pristine R_int(0)에 이미 CEI interphase 포함 → f0는 접촉몫 '
                   '상한구조. mech+chem 가법성은 독립 가정(설계 §4-9는 접촉면 손실↔화학이 물리적 결합 경고) (리뷰 #3).',
                   f'{interp_note} (리뷰 #5).',
                   'Yun=NCM+LPSCl 동일재료·아키텍처 미상 → mono/bimodal 절대 몫의 분모가 같음(아키텍처 미상). '
                   '단 mono↔bimodal 대비(contrast)는 분모 상쇄돼 100% 모델-구동(=접촉배율 비, 분모 무관) (리뷰 #2).',
                   'Kang=NCA 아키텍처 방향만(재료 다름); collector축(SBE/DBE)은 별개(rint_cycle_traj).',
               ],
               arch_label=a.arch, results={})
    print(f'측정 앵커: {m0["source"]}  (R0={m0.get("R0_ohm_cm2")} Ω·cm²)  [{interp_note}]')
    print(f'f0(pristine 접촉몫) 명목 {a.f0_nom}, 스윕 {f0_sweep};  대표규약=전하이동 CT(area^−1)\n')
    all_rows = []
    for tag, led in leds:
        rows, m = synth(led, a.measured, a.f0_nom, f0_sweep)
        out['results'][tag] = dict(atoms=led['atoms'], gamma_star=led['gamma'], rows=rows)
        last = rows[-1]
        _pc = lambda v: 'n/a' if v is None else f'{v * 100:.0f}%'
        print(f'[{tag}] {os.path.basename(str(led["atoms"]))}  '
              f'Γ*={led["gamma"]}  (AM-SE 접촉 {led["n_amse"]})')
        print(f'  N=100: 접촉배율 Holm {last["rct_holm_rel"]:.2f}× / CT {last["rct_ct_rel"]:.2f}× '
              f'· 측정 총 {last["R_int_rel_meas"]:.2f}×')
        print(f'    → 기계 몫 대표(CT+f0={a.f0_nom}) {_pc(last["mech_share_ct_nom"])}, '
              f'밴드 [{_pc(last["mech_share_lo"])}–{_pc(last["mech_share_hi"])}] '
              f'(규약×f0), Holm+명목 {_pc(last["mech_share_holm_nom"])}')
        if last.get('chem_negative_flag'):
            print(f'    ⚠ 화학 잔차 음수 (R_mech {last["R_mech_rel"]:.2f} > 측정 {last["R_int_rel_meas"]:.2f}) '
                  f'— f0/규약이 측정 총을 초과 = 규약 불일치 신호 (clamp 안 함)')
        for r in rows:
            all_rows.append(dict(arch=tag, **r))
    # 아키텍처 방향 대조 (둘 다 있을 때; 분모-무관 = 모델 접촉배율 비)
    if len(leds) == 2:
        r1, r2 = out['results']['primary']['rows'][-1], out['results']['secondary']['rows'][-1]
        ratio_holm = r2['rct_holm_rel'] / max(r1['rct_holm_rel'], 1e-9)
        ratio_ct = r2['rct_ct_rel'] / max(r1['rct_ct_rel'], 1e-9)
        print(f'\n아키텍처 방향 (분모-무관, 모델 접촉배율 비): Holm {ratio_holm:.2f}× / CT {ratio_ct:.2f}×')
        print(f'  (Kang&Shin 측정 B/U-NCA = 4.42/1.51 = 2.93× — 기계가 방향 일부, 나머지=화학이 bimodal 증폭)')
        out['arch_direction'] = dict(model_ratio_holm=round(ratio_holm, 3), model_ratio_ct=round(ratio_ct, 3),
                                     kang_measured_ratio=round(4.42 / 1.51, 3),
                                     note='분모 상쇄 → 대비는 100% 모델-구동 (리뷰 #2 검증)')
    with open(a.out + '.json', 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    with open(a.out + '.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        w.writeheader(); w.writerows(all_rows)
    print(f'\nsaved {a.out}.json / .csv')


# ---------------------------------------------------------------- selftest
def _selftest():
    ok = True
    # 1) _interp_factor 양끝·중간
    tj = {0: 1.0, 100: 4.0}
    e1 = abs(_interp_factor(tj, 0) - 1.0) + abs(_interp_factor(tj, 100) - 4.0) + abs(_interp_factor(tj, 50) - 2.5)
    ok1 = e1 < 1e-9; ok &= ok1
    print(f'selftest1 interp 양끝/중간: {"OK" if ok1 else "FAIL"}')
    # 2) 기계 몫 (CT+f0=1): rct_ct=1.5, 측정=4.0 → (1.5−1)/(4−1)=0.1667
    led = dict(N=np.array([100.0]), rct_holm=np.array([1.5]), rct_ct=np.array([1.5]),
               f_broken=np.array([0.5]), gamma=1.0, atoms='t', n_amse=1)
    MEASURED['_t'] = dict(material='t', arch='t', R0_ohm_cm2=100.0, traj={0: 1.0, 100: 4.0}, source='t', pdf='t')
    rows, _ = synth(led, '_t', 1.0, [0.2, 1.0])
    ok2 = abs(rows[0]['mech_share_ct_nom'] - 0.5 / 3.0) < 1e-3
    ok &= ok2
    print(f'selftest2 기계몫 CT f0=1 (1.5×/4×→16.7%): {rows[0]["mech_share_ct_nom"]:.4f}  {"OK" if ok2 else "FAIL"}')
    # 3) f0 스케일: f0=0.5 → 절반
    rows2, _ = synth(led, '_t', 0.5, [0.5, 0.5])
    ok3 = abs(rows2[0]['mech_share_ct_nom'] - 0.5 * (0.5 / 3.0)) < 1e-3
    ok &= ok3
    print(f'selftest3 f0=0.5 절반: {rows2[0]["mech_share_ct_nom"]:.4f}  {"OK" if ok3 else "FAIL"}')
    # 4) additive: R_mech + R_chem = 측정 총 (f0 명목)
    ok4 = abs((rows[0]['R_mech_rel'] + rows[0]['R_chem_rel']) - rows[0]['R_int_rel_meas']) < 1e-3
    ok &= ok4
    print(f'selftest4 R_mech+R_chem=총: {"OK" if ok4 else "FAIL"}')
    # 5) 무열화(rct=1) → 기계 몫 0
    led0 = dict(N=np.array([100.0]), rct_holm=np.array([1.0]), rct_ct=np.array([1.0]),
                f_broken=np.array([0.0]), gamma=1.0, atoms='t', n_amse=1)
    rows0, _ = synth(led0, '_t', 1.0, [0.2, 1.0])
    ok5 = abs(rows0[0]['mech_share_ct_nom']) < 1e-9
    ok &= ok5
    print(f'selftest5 무열화 기계몫 0: {rows0[0]["mech_share_ct_nom"]:.4f}  {"OK" if ok5 else "FAIL"}')
    # 6) Holm≤CT 밴드 (큰접촉 우선 파단 시 CT가 크다) + 측정 감소셀 None (리뷰 #1/#2)
    ledb = dict(N=np.array([100.0]), rct_holm=np.array([1.2]), rct_ct=np.array([1.5]),
                f_broken=np.array([0.3]), gamma=1.0, atoms='t', n_amse=1)
    rowsb, _ = synth(ledb, '_t', 1.0, [1.0])
    ok6 = rowsb[0]['mech_share_holm_nom'] < rowsb[0]['mech_share_ct_nom']  # Holm 하한 < CT 상한
    MEASURED['_d'] = dict(material='t', arch='t', R0_ohm_cm2=100.0, traj={0: 1.0, 100: 0.8}, source='t', pdf='t')
    rowsd, _ = synth(ledb, '_d', 1.0, [1.0])                    # 측정 감소 → 성장분해 불능 None
    ok6 &= rowsd[0]['mech_share_ct_nom'] is None
    ok &= ok6
    print(f'selftest6 Holm<CT 밴드 + 측정감소 None: {"OK" if ok6 else "FAIL"}')
    del MEASURED['_t'], MEASURED['_d']
    print('RINT-SYNTH SELFTEST', 'PASS' if ok else 'FAIL')
    return ok


def main():
    ap = argparse.ArgumentParser(description='CYCLE-STEP3 R_int(N) 합성/분해')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--ledger', help='cycle_contact_ledger .json (primary)')
    ap.add_argument('--ledger2', default=None, help='두번째 원장 (아키텍처 대조)')
    ap.add_argument('--measured', default='yun', choices=list(MEASURED),
                    help='측정 앵커: yun(NCM+LPSCl 동일재료·기본) / kang_bnca / kang_unca (NCA 방향)')
    ap.add_argument('--arch', default='', help='아키텍처 라벨 (mono/bimodal, 보고용)')
    ap.add_argument('--f0-nom', type=float, default=0.5, help='pristine 접촉 몫 명목 (미지 → 스윕도 병기)')
    ap.add_argument('--f0-sweep', default='0.1,0.3,0.5,1.0', help='f0 스윕 (밴드)')
    ap.add_argument('--out', default='cycle_rint_synth')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(0 if _selftest() else 1)
    if not a.ledger:
        ap.error('--ledger required (or --selftest)')
    if not (0 < a.f0_nom <= 1):
        ap.error('--f0-nom must be in (0,1]')
    run(a)


if __name__ == '__main__':
    main()
