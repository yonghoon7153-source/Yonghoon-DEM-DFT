# SDCP 매뉴스크립트 앵커 (Figures_v7, 2026-07-09 추출) — 모델 재배선 근거

사용자 매뉴스크립트 figure(15p: main 7 + SI S1-S22)에서 추출한 **실측 앵커**.  이전 웹서치 proxy
(conformal 필름·E 2 GPa·σ 315-1089 S/cm)는 전부 폐기/교체.

## 시스템
**Dry-processed ASSB cathode** (hot-rolling): NCM + LPSCl + PTFE + SDCP.
- **SBE** = Standard(PTFE-only) Binder Electrode / **DBE** = Dual(PTFE+SDCP) Binder Electrode
- +@C-SUS = SDCP/graphene 200nm 코팅 집전체(S14: 코팅 후 전도도 불변 1.3e4 S/cm; Fig5 접착 693→1029 aJ)
- wt% 조성은 methods 텍스트(미제공) — **TODO: 사용자 확인**

## SDCP 물성 (모델 입력)
| 항목 | 값 | 출처 | 모델 반영 |
|---|---|---|---|
| **형상** | as-made ~3µm 입자(S2) → 전극 내 **0.2-0.5µm 분산 입자**(S3, 노란원) | SEM | ★ kind='particle', SDCP_D=0.30µm; surface_frac=AM-앵커 몫(0.5 hook) + bulk 분산 |
| **E** | **23.6 GPa** (PTFE 5.6; long-tail~100) | AFM 모듈러스맵 Fig2d/S6 | ★ E=23.6 앵커 (LPSCl급 → rigid-proxy σ_y=1.0 §F1) |
| σ_ion (LPSCl+X pellet) | 3.57→**2.86** mS/cm (×0.80) vs PTFE 0.97 (×0.27) | Fig2f | STEP3: SDCP는 이온 저차단 |
| σ_e (LPSCl+X pellet) | 0.30→**1.53** e-7 S/cm (×5.1) vs PTFE 0.12 (×0.4) | Fig2g/S10 | STEP3: e-부스팅; econn 도체 유지 ✓ |
| 합성 | EDOT-MeOH+sultone→Na염 monomer→산화중합→이온교환 SO₃H | Fig2a/S4-5 | DFT monomer와 동일 ✓ |
| 열/구조 | XRD 무변화(S8), Raman/FTIR PEDOT+SO₃H(2b/S7) | | |

## 전극-수준 발견 (모델이 겨냥할 것)
- **S12: SDCP 단독 = dough 형성 불가** → PTFE fibrillation web이 필수 → **비교셋 = SBE(PTFE) vs DBE(PTFE+SDCP)**, SDCP-단독 런은 비물리
- **Fig3a: DBE에서 PTFE 분산 균일화** (SBE F-map 응집 → DBE 균일) — SDCP가 PTFE 뭉침을 억제 = 우리 fibrillation/분산 축과 연결 후보
- Fig3c-d: elastic recovery 0.69→0.82 / Fig4: R_ele 59.7→48.5 Ωcm², c-AFM 저저항 면적↑ / Fig6-7: 1000cyc@2C 안정, 저압(5MPa)서 격차 최대
- **Fig4(e) 'Electrochemical modeling' 빈 패널 + Fig7(c,d) placeholder** — 우리 3D 구조+연결성(econn) 시각화의 목표 슬롯

## 모델 반영 상태 (2026-07-09)
- additives.py: SDCP_D=0.30, v_obj=구부피, process rows regime='particle'+surface_frac(0.5/0.5/0.3 hook)
- mpm3d: kind='particle' 시딩(AM-앵커 몫 seed_coat(shell=반지름) + bulk 균일 in-pore), E=23.6 앵커,
  σ_y=1.0 rigid-proxy(§F1), **CFL dt 가드**(additive E가 SE 스택 초과 시 dt 캡 — VGCF 10도 소급 커버),
  metadata morphology/E_anchor/variant/INTERIM
- 유지: doped/neutral variant(coh·econn 처리), E_bind INTERIM(−4.8/−3.0 MLIP, DFT U-ramp 대기), ρ1.3 proxy(methods 대기)
