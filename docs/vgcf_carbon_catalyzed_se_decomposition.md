# VGCF carbon-촉매 SE 분해 → STEP5 화학열화 (#30)

**기전:** 탄소(VGCF/SuperP) 표면이 NCM–SE–carbon **3상 계면**에서 sulfide SE(LPSCl)의
전기화학적 **산화 분해**를 촉매 → 분해산물(P₂Sₓ, Li₂Sₙ, POₓ, P-O-P)이 저항성 → R_ion·R_int
성장 + SE 소모.  SE-poor(고-AM) 레짐에서 최악(적은 SE가 우선 공격).

## 문헌 앵커 (litdb — 정량, 우리 최고-앵커 채널)
- **kim2024** (우리 랩): 비가역용량 26.3→42.9 mAh/g (carbon 0→3 wt% @90 wt% AM = **+63%**);
  O 1s XPS 분해산물; **Fig 3b line-EDS: 3상 계면이 SE 분해 촉매** (기전 핵심).
- **cho2024** (사이클 앵커): with-CA 고-f_AM서 **R_ion 402→781 (~2×@100cyc)**, **R_int 278→591
  (~2.1×@100cyc)**; CV/XPS = LPSCl→P₂Sₓ+Li₂Sₙ+POₓ.  halide 치환 시 signature 소멸.
- **yun2023**: bare SC-NMC R_ct 341.7→982.3 = **2.87×@100cyc**.
- **reisacher2023**: carbon 전자-percolation 문턱 p_c≈4 wt% (설계 최소-carbon 경계).

## 구현 (기본 OFF)

**STEP3 read-out** (`step3_sigma.carbon_se_contact_area(sid, vox)`): carbon(sid 3/4/8)↔SE(6)
복셀-면 접촉 면적 µm² = 촉매 반응면.  payload가 `step3['carbon_se_area_um2']`로 기록 (carbon
있을 때만).  검증: 10×10 계면 @vox0.4 = 16.0 µm² 정확, no-carbon=0.

**STEP5 화학 채널 분해** (`b1_chem_fade._assemble` + trajectory/trajectory_scalar):
화학 채널을 **carbon-촉매몫 + baseline-CEI몫**으로 분해.
```
dR_chem_carbon = min(dR_chem, k_cat_carbon · carbon_se_area · vgcf_wt)   # 앵커 초과 방지 min()
dR_chem_base   = dR_chem − dR_chem_carbon
```
출력: `chem_carbon_share_pct`, `chem_base_share_pct`, `chem_carbon_frac`.

## ★ 이중계산 가드 (핵심)
cho2024/yun2023 끝점은 **with-carbon 셀** 측정 = 실험 앵커(`rint_exp_x`)에 carbon 효과가 **이미
포함**.  따라서 carbon몫을 화학 위에 **더하면(ADD) 이중계상** → 대신 화학 채널을 **쪼갠다(SPLIT)**:
`carbon + baseline = chem_total`, **총 R_int(N) 궤적 불변**.  selftest가 이를 고정:
- `k_cat_carbon=0` → carbon몫 0, chem 불변 (기본 무영향).
- ON → chem 불변, carbon+base=chem, **R_int 행별 궤적 bitwise 불변** (SPLIT 확인).
- kim2024 carbon-**부피점유**(SE 변위 → σ_ionic) 효과는 STEP3 **구조**축(A4) — STEP5 **화학**항과
  분리(부피변위 vs 표면촉매 혼동 금지).

## 잔여
- `k_cat_carbon` rate 값 = cho2024 ΔR_int-attributable-to-CA 또는 kim2024 +63%/3wt%로 캘리브 필요
  (현재 스윕 파라미터, 기본 0).  webapp `/step5` 패널 배선(carbon_se_area·k·vgcf_wt 슬라이더)은 후속.
- 3렌즈 적대리뷰 진행.
