#!/usr/bin/env python3
"""PRE-D3V2 탐침 14 — R11 "시험 덱의 물성 블록 (fix m1–m5 · mC · pair_style · wall/gran) = 등록한 ρ 팔 블록과 바이트 같음"
↔ R05 "보정 곡선 (C1) 의 벽 = γ_W/γ_SE 0 (벽 점착 끔)".

생성기 사실: (i) mC (cohesionEnergyDensity peratomtypepair) 행렬의 마지막 행 · 열 = 벽 (deck() · ced_matrix_geomean)
            (ii) gm_arm 은 γ_W/γ_SE = 0 을 거부한다 (_gm_num: 유한한 양수만)
⇒ 벽 점착 0 의 시험 덱은 어떤 등록 ρ 팔 (벽 = 0.0256·ρ_비코팅 > 0) 의 mC 블록과도 바이트 같을 수 없다 · 끝 감도 0.0256 은 ρ_비코팅 1 팔과만 같다.
덱 텍스트만 만든다 (파일 쓰기 0 · 런 0).

재실행: python3 -I p14_r11_r05.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
m = c.m
LAB = 'lab20261014'
p = m.plan(100000, cgf=151.4, dens_gen=LAB)
rpm = m.rpm_for_fr(m.FR_ANCHOR, p['R'])
out = {}
try:
    m.gm_arm({'AM_P': 1.0, 'AM_S': 1.0, 'SE': 1.0}, gamma_wall=0.0, bo_se=21.244)
    out['gm_arm_wall0'] = 'accepted'
except SystemExit as e:
    out['gm_arm_wall0'] = f'SystemExit: {e}'


def mc_block(name, rho_unc):
    a = m.gm_arm({'AM_P': rho_unc, 'AM_S': rho_unc, 'SE': 1.0}, gamma_wall=m.gm_wall_from_ncm(rho_unc), bo_se=21.244,
                 rho_uncoated_ncm=rho_unc)
    if name not in m.ARMS:
        m.register_arm(name, a)
    txt = m.deck(p, rpm, 2.0, seed=32452843, arm=name)
    lines = txt.split('\n')
    i0 = next(i for i, l in enumerate(lines) if l.startswith('fix mC '))
    return lines[i0:i0 + 1 + len(m.TYPES) + 1]


b03 = mc_block('PRED3VrhoA', 0.3)
b10 = mc_block('PRED3VrhoB', 1.0)
out['mC_rho_uncoated_0.3'] = b03
out['mC_rho_uncoated_1.0'] = b10
out['rows_differ'] = [i for i, (x, y) in enumerate(zip(b03, b10)) if x != y]
pcommon.dump('p14_r11_r05.json', out)
print('gm_arm(γ_W/γ_SE = 0):', out['gm_arm_wall0'])
print('mC (ρ_비코팅 0.3):'); print('\n'.join(b03))
print('mC (ρ_비코팅 1.0):'); print('\n'.join(b10))
print('다른 행 (0 = 머리):', out['rows_differ'])
