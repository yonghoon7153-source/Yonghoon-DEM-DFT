# db/structures — comp1/modelc V0 권위 구조 노트

## comp1 (Li₆PS₅Cl)
- ✅ **`comp1_V0_k444.cif` / `.xyz` = FINAL/AUTHORITATIVE V0**
  - 출처: container `comp1_v3/v3_post/k444_redo/relax_k444.out` (4×4×4 relax, k×L=40)
  - PS₄ intact (P-S 2.072±0.036 Å), V0=1016.62 Å³, a=10.0551 Å (cubic), E0=−13917.8916 eV
  - ordered: Cl ×4 + free-S²⁻ ×4가 서로 다른 자리 독점 (S/Cl mixing 없음)
  - **figure + 구조 분석 모두 이 파일 사용**
- `lpscl_F43m_24G_canonical.cif` — idealized F-43m (P 정확히 특수위치). figure용으로 깔끔하나
  V0 아님(a=10.249). 필요시 V0로 스케일해 사용 (paper_figures/comp1_V0_cubic.cif가 그 결과).
- ❌ `lpscl_relaxed_conv_52atoms.cif.BROKEN_PS4_dissociated` — **사용 금지**.
  conventional-cell 변환 사고로 PS₄ 해리 (각 P가 S 1~2개만 ≤2.5Å, 나머지 4.3Å). k-mesh 무관, CIF 변환 버그.

## modelc (Li₅.₄PS₄.₄Cl₁.₆)
- `modelC_DFT_EOS_V0.cif` — EOS v100 점(V=1204.22) 구조. V0(1216.44)로 스케일해 사용.
  rhombohedral 초격자, Cl-rich + Li 공공 (disordered). figure는 rhombohedral 그대로.
  ⚠ EOS 구조와 LOBSTER(k663) property 구조가 Cl 4a/4d 배치가 다를 수 있음 — per-site ICOHP는
  property 구조(bonds_modelc_k663.json) 기준.

마지막 갱신: 2026-06-05
