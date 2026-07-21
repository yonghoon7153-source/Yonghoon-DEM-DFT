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
    tr = d['trajectory']
    N = np.array([r['cycle'] for r in tr], float)
    rct = np.array([r['rct_proxy_rel'] for r in tr], float)   # A0/A_N = 접촉저항 배율(면적손실)
    fbrk = np.array([r['f_broken_amse'] for r in tr], float)
    return dict(N=N, rct_rel=rct, f_broken=fbrk, gamma=d.get('gamma_star', {}).get('value'),
                atoms=d.get('atoms', path), n_amse=d.get('n_contacts', {}).get('am_se'))


def synth(led, meas_key, f0_nom, f0_sweep):
    m = MEASURED[meas_key]
    rows = []
    for i, N in enumerate(led['N']):
        rct = led['rct_rel'][i]                               # 모델: 접촉저항 배율
        Rmeas = _interp_factor(m['traj'], N)                  # 측정: 총 R_int 배율
        d_mech_unit = rct - 1.0                               # ΔR_mech / (f0·R0)
        d_meas = Rmeas - 1.0                                  # ΔR_meas / R0
        # 성장의 기계 몫 (f0 명목 + 스윕 밴드)
        s_nom = (f0_nom * d_mech_unit / d_meas) if d_meas > 1e-9 else 0.0
        s_lo = (min(f0_sweep) * d_mech_unit / d_meas) if d_meas > 1e-9 else 0.0
        s_hi = (max(f0_sweep) * d_mech_unit / d_meas) if d_meas > 1e-9 else 0.0
        # additive 재구성 (명목 f0; R_chem = 잔차 = 측정 − 기계)
        R_int_rel = Rmeas                                     # 총 (측정 = 참값 규약)
        R_mech_rel = 1.0 + f0_nom * d_mech_unit               # 기계 몫 (모델)
        R_chem_rel = R_int_rel - R_mech_rel                   # 화학 잔차 (모델 밖)
        rows.append(dict(cycle=int(N), rct_proxy_rel=round(rct, 4), R_int_rel_meas=round(Rmeas, 4),
                         mech_share_nom=round(s_nom, 4), mech_share_lo=round(min(s_lo, s_hi), 4),
                         mech_share_hi=round(max(s_lo, s_hi), 4),
                         R_mech_rel=round(R_mech_rel, 4), R_chem_rel=round(max(R_chem_rel, 0), 4),
                         R_int_ohm_cm2=round(m['R0_ohm_cm2'] * Rmeas, 1) if m.get('R0_ohm_cm2') else None))
    return rows, m


def run(a):
    leds = [('primary', load_ledger(a.ledger))]
    if a.ledger2:
        leds.append(('secondary', load_ledger(a.ledger2)))
    f0_sweep = [float(x) for x in a.f0_sweep.split(',')]
    out = dict(model='CYCLE-STEP3 R_int synthesis', measured_key=a.measured,
               measured=MEASURED[a.measured], f0_nominal=a.f0_nom, f0_sweep=f0_sweep,
               caveat='rct_rel=면적비 상대프록시; f0=pristine 접촉몫 미지(스윕); Yun=동일재료군 최우선, '
                      'Kang=NCA 아키텍처 방향만; collector축(SBE/DBE)은 별개(rint_cycle_traj)',
               arch_label=a.arch, results={})
    print(f'측정 앵커: {MEASURED[a.measured]["source"]}  (R0={MEASURED[a.measured].get("R0_ohm_cm2")} Ω·cm²)')
    print(f'f0(pristine 접촉몫) 명목 {a.f0_nom}, 스윕 {f0_sweep}\n')
    all_rows = []
    for tag, led in leds:
        rows, m = synth(led, a.measured, a.f0_nom, f0_sweep)
        out['results'][tag] = dict(atoms=led['atoms'], gamma_star=led['gamma'], rows=rows)
        last = rows[-1]
        print(f'[{tag}] {os.path.basename(str(led["atoms"]))}  '
              f'Γ*={led["gamma"]}  (AM-SE 접촉 {led["n_amse"]})')
        print(f'  N=100: 모델 접촉배율 {last["rct_proxy_rel"]:.2f}× / 측정 총 {last["R_int_rel_meas"]:.2f}× '
              f'→ 기계 몫 {last["mech_share_nom"] * 100:.0f}% '
              f'[{last["mech_share_lo"] * 100:.0f}–{last["mech_share_hi"] * 100:.0f}%], '
              f'화학 몫 {(1 - last["mech_share_nom"]) * 100:.0f}%')
        for r in rows:
            all_rows.append(dict(arch=tag, **r))
    # 아키텍처 방향 대조 (둘 다 있을 때)
    if len(leds) == 2:
        r1, r2 = out['results']['primary']['rows'][-1], out['results']['secondary']['rows'][-1]
        ratio_model = r2['rct_proxy_rel'] / max(r1['rct_proxy_rel'], 1e-9) if r2['rct_proxy_rel'] else 0
        print(f'\n아키텍처 방향: 모델 접촉배율 비 secondary/primary = {ratio_model:.2f}×')
        print(f'  (Kang&Shin 측정 B/U-NCA = 4.42/1.51 = 2.93× — 기계가 방향 일부 설명, 나머지=화학이 bimodal 증폭)')
        out['arch_direction'] = dict(model_ratio=round(ratio_model, 3),
                                     kang_measured_ratio=round(4.42 / 1.51, 3))
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
    # 2) 기계 몫: rct_rel=1.5, 측정=4.0, f0=1 → (1.5−1)/(4−1)=0.5/3=0.1667
    led = dict(N=np.array([100.0]), rct_rel=np.array([1.5]), f_broken=np.array([0.5]),
               gamma=1.0, atoms='t', n_amse=1)
    MEASURED['_t'] = dict(material='t', arch='t', R0_ohm_cm2=100.0, traj={0: 1.0, 100: 4.0}, source='t', pdf='t')
    rows, _ = synth(led, '_t', 1.0, [0.2, 1.0])
    ok2 = abs(rows[0]['mech_share_nom'] - 0.5 / 3.0) < 1e-3
    ok &= ok2
    print(f'selftest2 기계몫 f0=1 (1.5×/4×→16.7%): {rows[0]["mech_share_nom"]:.4f}  {"OK" if ok2 else "FAIL"}')
    # 3) f0 스케일: f0=0.5 → 절반
    rows2, _ = synth(led, '_t', 0.5, [0.5, 0.5])
    ok3 = abs(rows2[0]['mech_share_nom'] - 0.5 * (0.5 / 3.0)) < 1e-3
    ok &= ok3
    print(f'selftest3 f0=0.5 절반: {rows2[0]["mech_share_nom"]:.4f}  {"OK" if ok3 else "FAIL"}')
    # 4) additive: R_mech + R_chem = 측정 총 (f0 명목)
    ok4 = abs((rows[0]['R_mech_rel'] + rows[0]['R_chem_rel']) - rows[0]['R_int_rel_meas']) < 1e-3
    ok &= ok4
    print(f'selftest4 R_mech+R_chem=총: {"OK" if ok4 else "FAIL"}')
    # 5) 무열화(rct=1) → 기계 몫 0
    led0 = dict(N=np.array([100.0]), rct_rel=np.array([1.0]), f_broken=np.array([0.0]),
                gamma=1.0, atoms='t', n_amse=1)
    rows0, _ = synth(led0, '_t', 1.0, [0.2, 1.0])
    ok5 = abs(rows0[0]['mech_share_nom']) < 1e-9
    ok &= ok5
    print(f'selftest5 무열화 기계몫 0: {rows0[0]["mech_share_nom"]:.4f}  {"OK" if ok5 else "FAIL"}')
    del MEASURED['_t']
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
