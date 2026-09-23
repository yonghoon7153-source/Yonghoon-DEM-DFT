---
title: "리뷰 BW 프롬프트 — W_ad: 클러스터 없이(단일 노드 48 GB) 무엇을 검증할 수 있나 · MLIP+D3 본계산 + 작은 모델 DFT 검증으로 바꿔도 되는가"
date: 2026-09-23
updated: 2026-09-23
tags: [review, codex, adhesion, wad, interface, lpscl, silver, graphite, uma, d3, dft-verification, compute-limits]
status: 발송됨 · 회신 수령 (NO-GO · 제한 파일럿 조건부 GO) → codex_BW_reply_wad_validation_without_cluster_2026_09_23.md
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 BW — W_ad: 클러스터 없이 무엇을 검증할 수 있나

> 앞 리뷰: **BV (NO-GO)** — `kb/reviews/codex_BV_reply_wad_lpscl_ag_c_vgcf_2026_09_23.md`. 그 재개 조건 5묶음 중 무엇을 했고,
> **새로 생긴 제약 하나**(클러스터 접근 종료) 때문에 BV 의 검증 설계를 어떻게 바꾸려는지 묻는다.
> 트랙 = 우리 DFT → 1저자 = 사용자. 정본 브랜치 `claude/friendly-meitner-lldvar`.

## §0. BV 뒤에 한 것 (전부 결과 0 — 계산은 아직 한 건도 안 돌았다)

| BV 조건·지적 | 한 것 | 근거 |
|---|---|---|
| ② SE 단순 절단이 PS₄ 8/48 을 끊는다 | PS₄ 보존 창의 Li 2\|6 틈에서 자른 **대칭 슬랩 두 장** 빌더·검증기 | `tools/wad/se_sym_slab.py` (selftest 50 · 음성: 순진 절단·극성 절단·비대칭·이름표 뒤바뀜·PS₄/자유 S 자리바꿈·러너 LiNiO₂ 0배위 · 돌연변이 전부 빨간불) |
| (구조) | S 바깥 Li₇₆P₁₂S₆₂Cl₁₂ **162원자** · Li·PS₄ 바깥 Li₆₈P₁₂S₅₈Cl₁₂ **150원자** = Pustorino 2025 의 6층 조성 · 양면 동일 = **x 축 C2**(편차 9×10⁻⁵ Å) | `db/structures/wad_se_slabs_2026_09_23/` |
| (발견) | comp1_V0_k444 에는 **−4 축이 없다** (Li 정렬이 입방 대칭을 깬다) — z 를 뒤집는 대칭은 C2x 하나 | 계획 §0′ 정정 |
| 분산 표기 | QE 기본 `dftd3_threebody=.true.` 확인 → W_ad 는 **D3(BJ) 2체**, ATM 은 따로 | 결정 `D-2026-09-23-wad-d3-twobody-atm-separate` |
| SE\|SE 대조 | 이완 PBE W_cleave 경보 운영값 **0.3–0.7 J/m²** · >1 이면 PS₄ 절단 먼저 점검 · 무이완 ≥ 이완 — **결과 전 봉인**, 합격선 아님 | 결정 `D-2026-09-23-wad-sese-alarm-band` |
| ⑤ DEM 입력법칙 | DEM 회신: JKR pull-off 의 **w = W** · 헤드라인 = **고정기하 W_sep** · DFT@UMA 값도 받아 G_c **띠** | `kb/projects/wad_dem_reply_draft_2026_09_23.md` §받은 회신 |
| (범위) | DEM 요청으로 **P2 LPSCl\|graphite(0001) 를 P1 과 같은 우선순위로** (Ag 5.7 vol% — LPSCl 이 닿는 면 대부분이 탄소) | 결정 `D-2026-09-23-wad-p2-lpscl-graphite-scope` |

**격자 정합 후보** (정방 SE 단면 10.055 Å 위 직사각 초격자 · |ε| < 3 % · 흡착층을 SE 에 맞출 때):

| 계면 | SE 측면 | 흡착층 셀 | 흡착층 변형률 | 원자 수 (6층 SE) |
|---|---|---|---|---|
| P1 LPSCl\|Ag(111) | 1×2 (10.06 × 20.11 Å) | 10.01 × 20.22 Å (x = 2·√3a_s · y = 7·a_s) | +0.46 / −0.57 % (a 4.086) · −1.32 / −2.33 % (a 4.16 PBE) | ≈ 436 (Ag 4층 가정) |
| P2 LPSCl\|graphite | 1×3 (10.06 × 30.17 Å) | 9.84 × 29.83 Å (x = 4a · y = 7·√3a) | +2.19 / +1.14 % | ≈ 820 (흑연 3층 가정) |

흑연은 SE 1×3 미만에 안 들어간다 (1×2 는 y 방향 +5.9 %).

## §1. 새 제약 — 클러스터가 없다 (실측)

- **KISTI 접근은 2026-09-15 에 종료됐다.** 우리 기계는 전부 **단일 노드**다: gabia A6000 **48 GB** (가장 크다) / kgy 3090 24 GB (공유) / V100 32 GB.
- ⭐ **1저자 (2026-09-23): 이런 큰 계산은 GPU 로.** 큰 잡을 CPU(host RAM 62 GB)로 돌리지 않는다 ⇒ 큰 잡의 메모리 상한 = **GPU 한 장 48 GB**.
  아래 추정치는 GPU 가 b2o3 MD 와 공유 중이라 **CPU pw.x 1랭크로 추정치만 읽고 수 초 안에 PID 로 죽인** 값이다 (계산 없음 · 1저자 허용).
- QE `Estimated max dynamical RAM` (gabia CPU 1랭크 스크래치 프로브 · 2026-09-23 · GBRV USPP + P rrkjus · 52/520 Ry · gaussian 0.005 · D3):

| 잡 | 원자 | k 점 | 추정 |
|---|---|---|---|
| comp1 벌크 SCF | 52 | 30 | 6.7 GB |
| S 바깥 6층 슬랩 SCF (진공 20 Å) | 162 | 9 | **55.8 GB** |
| Li·PS₄ 바깥 6층 슬랩 SCF | 150 | 9 | **50.2 GB** |
| (다른 계) Li₂S 4×4×4 공공 SCF · 60/480 | 191 | 2×2×2 | 45.15 GB — kgy 실측 **15 s 만에 VRAM ≥ 21.1 GB** (가드 중단 · 하한) |

- ⇒ **P1(~436) · P2(~820원자) 전체 계면의 평면파 DFT 는 우리 기계로 불가.** BV 의 *"검증 표본 = 실제 계면에서 사전 고정 5개 · 표본마다 |W^PBE − W^UMA| ≤ 0.10 J/m²"* 를 **그대로는 못 한다.**
- 같은 벽을 li2s 트랙이 먼저 맞았다: 400원자 G1 이 QE 추정 110 GB 로 막히자 **120원자로 질문을 바꿔** UMA 를 DFT 에 검증했다 (F_RMSE 0.039 eV/Å · 상대 E MAE 0.55 meV/atom — `db/properties/li2s_track_ladder_2026_09_18.json`).
- MLIP 쪽 사정: 이 repo 에 **"MLIP 절대값을 인용하지 않는다 (σ · W_ad)"** 규칙이 있다 (`webapp/fairchem.py` `OUR_BANS`). 근거 중 하나 — LPSCl|NCM 가족에서 UMA W_ad 가 실험 순위와 **R = −0.76** 로 뒤집혔고 같은 구조에 MACE 는 +0.957 였다 (`db/properties/adhesion.json`; 당시 NCM 빌더에도 문제가 있어 원인이 섞였을 수 있다). UMA(omat)는 **분산이 없는 PBE(+U)** 를 배웠고, MoLE 전문가 가중치가 **계 전체 조성**에 따라 정해진다.

## §2. 제안하는 설계 변경 (검토 대상)

**(A) 본계산 = UMA+D3(BJ, 2체) · 검증 = gabia 에 들어가는 작은 모델에서 DFT(PBE+D3)** ← 제안자 선호
- 전체 계면(P1·P2 · 20 registry · 균일 xy)은 UMA+D3 로 이완 → 강체 분리 W_sep. 분리 참조는 **같은 셀에서 멀리 뗀 것**(조성 동일 → MoLE 가중치 동일).
- DFT 검증 표본 (전부 gabia 48 GB 안 — 추정은 부피 × 밴드 수 비례, 던지기 전에 CPU 추정으로 확인):
  - V1 **SE\|SE 대조 4층** (110 / 98원자 · 진공 15 Å · k 3×3×1 · 6층 대비 0.48 / 0.40 ≈ 22–27 GB): 확장 계면 그 자체. Pustorino 자신의 두께 시험이 3층 0.22 vs 6층 0.20 J/m².
  - V2 **Ag\|흑연 작은 셀** (그래핀 2×2 / Ag(111) √3 등 수십 원자): DFT 로 값 자체를 낸다 — MLIP 불필요. UMA+D3 검증도 겸한다.
  - V3 **LPSCl\|Ag 대리 모델**: 얇은 SE(1 관용셀 두께) 위 Ag 조각(~70원자, 추정 ~20 GB) — Ag–S/Ag–Li/Ag–Cl 결합 환경. ⚠ 확장 계면이 아니다.
  - V4 **LPSCl\|흑연 대리 모델**: 같은 SE 위 그래핀 조각.
- DEM 전달값 = *"작은 모델 DFT 로 검증한 UMA+D3"* 이름표 · **검증 통과 시에만** — MLIP 금지 규칙의 **조건부 예외**가 필요하다.

**(B) 가우스 기저 DFT (CP2K GPW · PBE-D3 · DZVP/TZV2P-MOLOPT)** — 진공에 비용을 안 내서 전체 계면 DFT 를 지키는 길이다.
⚠ **"큰 계산은 GPU" 제약에서 약해졌다**: 처음 판단은 *"800원자가 host 62 GB 에 들어간다"* 였는데 그건 CPU 전제다. GPU 판 CP2K 는 설치·메모리 모형·검증이 전부 새로 필요하다.
그 위에 새 코드 · 기저 수렴 · **BSSE(counterpoise)** · 우리 QE 기준선과 교차검증(SE\|SE 로)이 필요하다.

## §3. 질문

1. **클러스터 없이 · GPU 한 장(48 GB)으로 (A) 가 DEM 목표(자릿수 · 저 ≲ 0.3 / 고 ≳ 1 J/m² 구간)에 방어 가능한가**, 아니면 (B)(GPU 판 CP2K)가 필요한가? (A) 라면 최소 검증 집합은?
2. **V3 설계** — 조각-위-슬랩, 변형된 단층 흡착층, 얇은 확장 계면 중 어느 것이 확장 계면 W 와 **같은 물리**를 재는가? 조각이면 무엇으로 정규화하고(접촉 원자당 · 투영 면적당) 합격선은 무엇인가 (BV 의 0.10 J/m² 가 옮겨지나)?
3. **MoLE·가산성** — 같은 셀 원거리 분리 참조로 충분한가? 가산성 시험 E(A+B, far) vs E(A)+E(B) 를 보고량 단위(J/m²)로 어떻게 걸까?
4. **UMA + D3(BJ, PBE 계수)** — omat 이 분산 없는 PBE 라 이중계산은 없다고 보는데 맞나? 같은 D3 를 양쪽에 더하면 검증은 **PBE 몫만** 시험하게 된다 — 흑연 계면(분산 지배)에서 그걸로 충분한가? d_eq 는 UMA 반발이 정하는데?
5. **SE\|SE 4층** (110 / 98원자 · 진공 15 Å · k 3×3×1) 이 6층 대신 경보 대조로 충분한가?
6. **정합 규칙** — 흡착층을 SE 에 맞춘다(SE 기하를 P1·P2·SE\|SE 에서 하나로 고정 · 흑연 +2.2 %). 면적당 W 는 변형된 셀 면적으로. 괜찮은가?
7. **지금 DEM 에 무엇을 약속해도 되나** — 아래 부록의 두 판(전체 초안 · 확정분만 담은 중간 회신) 중 무엇이 맞나? 전체 초안의 4번(*헤드라인 = W_sep(DFT · 고정기하)*)은 (A) 와 **모순**이다 (제안자 자기발견).
8. (작은 것) gabia GPU ↔ UMA 예외(`D-2026-09-23-gabia-gpu-exception-sese`)는 슬랩이 48 GB 를 넘어 **한 번도 발동하지 않은 채** 끝나는데, 닫는 것 말고 남길 것이 있나?

## §4. 받고 싶은 것
- GO / NO-GO 와 **재개 조건** (BV 처럼 묶음으로).
- (A) 로 간다면 V1–V4 중 필수·선택 · 각 표본의 **합격선과 정규화** · 사전 고정 방식.
- DEM 에 지금 보낼 수 있는 문장의 **허용 서술 범위**.

## 부록 — DEM 회신 초안 두 판
- 전체 초안(3·4번 포함): `kb/projects/wad_dem_reply_draft_2026_09_23.md` §회신 2
- 확정분만 담은 중간 회신: 같은 파일 §회신 2′ (중간)
