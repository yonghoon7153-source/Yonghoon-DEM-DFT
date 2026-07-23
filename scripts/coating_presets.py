#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""이종기술 코팅 프리셋 (webapp v3, #33) — CAM 표면 이종층을 하나의 셀렉터로 통합.

CLAUDE.md frame[5]: 코팅 = **화학 CEI 축**(Stage-E 기계 coverage와 별개).  litdb 적용표(B-2위):
코팅이 현재 3경로(화학CEI STEP5 --chem-x · 계면전도 Han2025 t/σ_b · 구조seeding SDCP/SWCNT)로
흩어져 있어 → 통합 프리셋 {cei_suppress, r_ct_factor, σ_ion_mod, σ_e_mod, seed_morph}.

★정직 규약: **크기(magnitude)는 앵커, shape(√N)는 ASSUMED** (fit_rint_curve.py가 ≥4 N점 실측으로
게이트).  앵커 없는 항목은 값 미지정(스윕 전용).  cei_suppress = bare 대비 화학성장 증분 억제배수
(LNO 13–20× = Kim2025 R_ct 20×·CEI 13–20×; Payandeh 93%@200cyc; Kang LZO 6–8nm).

`coated_chem_x(coating, bare_chem_x)`: bare 화학성장 × → 코팅 적용 후 억제된 화학성장 × 반환
  = 1 + (bare_chem_x − 1) / cei_suppress   (증분만 억제, 앵커 끝점 규약과 정합).
"""
from __future__ import annotations

# 각 프리셋: cei_suppress(화학성장 증분 억제배수, ≥1)·r_ct_factor(계면 R_ct 배수, <1=개선)·
#            sigma_ion_mod·sigma_e_mod(계면/벌크 σ 배수)·seed_morph·anchor(출처)·shape(항상 ASSUMED).
# ★값 = magnitude 앵커.  None = 앵커 없음(스윕 전용, 날조 금지).
COATING_PRESETS = {
    'none': {
        'label': 'bare NCM (무코팅)', 'cei_suppress': 1.0, 'r_ct_factor': 1.0,
        'sigma_ion_mod': 1.0, 'sigma_e_mod': 1.0, 'seed_morph': None,
        'anchor': 'baseline — 화학 CEI 전량(억제 없음)', 'shape': 'ASSUMED (√N)'},
    'LNO': {                                              # LiNbO3 — 가장 흔한 sulfide-ASSB CAM 코팅
        'label': 'LiNbO₃ (LNO)', 'cei_suppress': 15.0, 'r_ct_factor': 1.0 / 20.0,
        'sigma_ion_mod': 1.0, 'sigma_e_mod': 1.0, 'seed_morph': 'shell',
        'anchor': 'Kim2025: R_ct 20× 억제·CEI 13–20× / Payandeh 93%@200cyc (크기 앵커)',
        'shape': 'ASSUMED (√N; ≥4 N점 실측 필요)'},
    'LZO': {                                              # Li2ZrO3
        'label': 'Li₂ZrO₃ (LZO) 6–8nm', 'cei_suppress': 8.0, 'r_ct_factor': 1.0 / 6.0,
        'sigma_ion_mod': 1.0, 'sigma_e_mod': 1.0, 'seed_morph': 'shell',
        'anchor': 'Kang&Shin LZO 6–8nm CEI 억제 (크기 앵커, 배수는 LNO 하한 보수 추정)',
        'shape': 'ASSUMED (√N)'},
    'Li3PO4': {
        'label': 'Li₃PO₄', 'cei_suppress': None, 'r_ct_factor': None,
        'sigma_ion_mod': 1.0, 'sigma_e_mod': 1.0, 'seed_morph': 'shell',
        'anchor': '⛔ 정량 앵커 미확보 → 스윕 전용(날조 금지)', 'shape': 'ASSUMED'},
    'carbon': {                                           # 전도성 코팅 (탄소)
        'label': 'carbon-coat (전도성)', 'cei_suppress': 1.0, 'r_ct_factor': None,
        'sigma_ion_mod': 1.0, 'sigma_e_mod': None, 'seed_morph': 'shell',
        'anchor': 'Reisacher p_c≈4wt%(정확 LPSCl+C65)·So2022 core-shell — σ_e↑(값=A4 GPU), '
                  'CEI 억제 아님(오히려 탄소-촉매 SE분해=#30 별도 축)',
        'shape': 'N/A (화학열화는 #30 carbon-촉매로)'},
    'SDCP': {                                             # 자기도핑 전도성 바인더 (우리 A4′)
        'label': 'SDCP (S-PEDOT 자기도핑)', 'cei_suppress': None, 'r_ct_factor': None,
        'sigma_ion_mod': 0.80, 'sigma_e_mod': 5.1, 'seed_morph': 'coat',
        'anchor': 'A4′ 완비: σ_e×5.1·σ_ion×0.80·E23.6GPa (manuscript); E_bind DFT 잔여',
        'shape': 'N/A (전도 이종상, 화학 CEI 아님)'},
    'SWCNT': {                                            # 연속 SWCNT sheath (우리 A14)
        'label': 'SWCNT sheath', 'cei_suppress': None, 'r_ct_factor': None,
        'sigma_ion_mod': 1.0, 'sigma_e_mod': None, 'seed_morph': 'sheath',
        'anchor': 'A14 완비: seed_sheath geodesic vein, sid8 (Koo2026); σ_e=--sigma-swcnt',
        'shape': 'N/A (전도 이종상)'},
}


def get_preset(coating: str) -> dict:
    """코팅 이름 → 프리셋 dict (대소문자 무관).  미지원 → 'none'."""
    if not coating:
        return COATING_PRESETS['none']
    key = str(coating).strip()
    for k in COATING_PRESETS:
        if k.lower() == key.lower():
            return COATING_PRESETS[k]
    return COATING_PRESETS['none']


def coated_chem_x(coating: str, bare_chem_x: float) -> float:
    """bare 화학성장 ×(>1) → 코팅 CEI 억제 후 화학성장 ×.  증분만 억제(끝점 규약 정합):
    chem_x_coated = 1 + (bare_chem_x − 1) / cei_suppress.  cei_suppress None(앵커없음)/≤1 → bare 유지.
    ★크기만 앵커 — shape(√N)는 b1_chem_fade가 ASSUMED-FORM 라벨로 처리."""
    p = get_preset(coating)
    s = p.get('cei_suppress')
    b = float(bare_chem_x)
    if s is None or s <= 1.0:
        return b
    return 1.0 + (b - 1.0) / float(s)


def preset_summary() -> str:
    """프리셋 표 텍스트 (webapp/CLI 표기용)."""
    rows = ['coating        cei_suppress  r_ct×   σ_ion×  σ_e×   morph   anchor']
    for k, p in COATING_PRESETS.items():
        rows.append(f"{k:14s} {str(p['cei_suppress']):>11s}  {str(p['r_ct_factor'])[:6]:>6s}  "
                    f"{str(p['sigma_ion_mod']):>5s}  {str(p['sigma_e_mod']):>5s}  "
                    f"{str(p['seed_morph'] or '-'):>6s}  {p['anchor'][:40]}")
    return '\n'.join(rows)


# ─────────────────────────── self-test ───────────────────────────
def _selftest() -> int:
    fails = []
    # none = bare 불변
    assert abs(coated_chem_x('none', 1.30) - 1.30) < 1e-12
    assert abs(coated_chem_x('', 1.30) - 1.30) < 1e-12
    # LNO 15× 억제: 1.30 → 1 + 0.30/15 = 1.02
    assert abs(coated_chem_x('LNO', 1.30) - 1.02) < 1e-9, coated_chem_x('LNO', 1.30)
    assert abs(coated_chem_x('lno', 1.30) - 1.02) < 1e-9    # 대소문자 무관
    # LZO 8× : 1.30 → 1 + 0.30/8 = 1.0375
    assert abs(coated_chem_x('LZO', 1.30) - 1.0375) < 1e-9
    # 앵커 없는 프리셋(Li3PO4/SDCP/SWCNT) → bare 유지 (날조 금지 = 억제 미적용)
    for c in ('Li3PO4', 'SDCP', 'SWCNT', 'carbon'):
        if abs(coated_chem_x(c, 1.30) - 1.30) > 1e-9:
            fails.append(f'{c} 앵커없음인데 chem_x 변경')
    # 미지원 코팅 → none
    assert get_preset('unknown_xyz')['label'] == COATING_PRESETS['none']['label']
    # 억제는 단조 (suppress 클수록 chem_x 작음): LNO(15) < LZO(8) 억제 후
    assert coated_chem_x('LNO', 1.5) < coated_chem_x('LZO', 1.5) < 1.5
    # 억제 후에도 ≥1 (성장은 음수 안 됨)
    assert coated_chem_x('LNO', 1.30) >= 1.0
    print('selftest OK' if not fails else 'selftest FAIL: ' + '; '.join(fails))
    print(preset_summary())
    return 1 if fails else 0


if __name__ == '__main__':
    import sys
    raise SystemExit(_selftest() if (len(sys.argv) > 1 and sys.argv[1] == '--selftest') else _selftest())
