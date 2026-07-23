# STEP5 — 사이클 열화 (cycle degradation): "진짜 열화 전극" (정의 2026-07-23)

## 파이프라인 위치
```
STEP1  DEM 패킹 (LIGGGHTS)
STEP2  MPM 압밀 · payload (형상·void·응력)
STEP3  voxel Kirchhoff σ (σ_e / σ_ion / σ_thermal · current-focusing)
STEP4  electrochem 동역학 (galvano/CV · R_int · 방전곡선)
STEP5  ★사이클 열화 (R_int(N) · 용량 fade)  ← 여기
```

## 목표
pristine 전극(STEP1–4 산출)이 주어졌을 때 **N 사이클 후 어떻게 열화하는가**(R_int(N),
용량 유지율)를 예측.  = "충전상태 스냅샷"을 넘어 실제 사이클 fade로.

## ★ 정직한 모델 = frame[5] 4조각 분해
핵심 교훈(적대리뷰): **"MPM이 사이클을 다 돌린다"는 불가능** — 대신 각 물리를 제 도구에.

| 조각 | 물리 | 도구 | 총 fade 몫 | 상태 |
|---|---|---|---|---|
| **A-1** | 충전상태 형상변화 (SC 수축→접촉 gap) | MPM v1 `--cycle-deform` | 형상앵커(가역) | ✅ GPU검증 (SC coverage −19%) |
| **A-3** | 영구 접촉파단 | ledger (δcr CZM + `recontact=forbid`) | **~2%** | ✅ R_ct 1.09×@N100(포화) |
| **B-1** | 화학 계면상(CEI) 성장 | STEP4 interphase (i0(N)↓+필름옴성) | **~98% 지배** | ✅ N-전개 착지(b1_chem_fade): 총 R_int(N) 실험앵커, 화학 99.6~99.8% |
| **실험** | 크기·모양 앵커 | R_int(N)/retention(N) 곡선 | 검증 게이트 | ⛔ WSL PDF(#5) |

합산: **총 R_int(N) = R_contact(N)[A-1 검증 gap → A-3 ledger] + R_chem(N)[B-1] + R_collector(N)**.

## 여정 (기각된 것 = 정직화 과정, 적대리뷰가 오버클레임 차단)
- ❌ **v2 반복사이클 MPM** — 3렌즈 만장일치 기각(코딩 전): rigid pin-mask는 방전 스프링백 불가 ·
  isochoric J2는 영구 접촉손실 금지(부피보존=void 메꿈) · 재변형 sub-voxel(0.2셀=null mask) ·
  servo 자기-drift.  docs/a1_v2_cycle_ratchet_design.md.
- ❌ **reflow 캘리브** — metric 아티팩트로 철회(ledger Hertz-area 30% vs MPM voxel 19% = 지표차,
  재유동 아님; 같은 voxel 지표선 16.8%≈19.4% 이미 일치).  docs/a3_reflow_calibration.md.
- ✅ **살아남은 것** = 위 정직 4조각 분해.


## ★ 코팅 양극재 = 화학 몫 열어둠 (사용자 2026-07-23)
요즘 쓰는 양극재는 **nm 코팅(LNO 등)으로 CEI 억제** → 화학 열화 작음.  근거: kim2025 LNO R_ct
17~22 vs bare 290~450 Ω·cm²(~16~20× 낮음); 너 랩 pristine R_int 12~18 = **코팅 영역**(bare 아님).
⇒ 코팅 셀의 fade는 화학-CEI 아님 → **b1_chem_fade `--chem-x`로 화학 몫을 열어둠**(코팅=작게):
  - 화학(코팅 억제, 명시) + 접촉(ledger 하한, frozen-AM이라 골격재배열 빠짐) + **OTHER**(나머지 =
    골격재배열·SE 분해·Li쪽 = 현 모델 밖).  예: 코팅 SBE → 화학 6% / 접촉 0.2% / **OTHER 94%**.
⇒ STEP5 = **열린 분해 프레임워크**(하드코딩 fade 아님).  좋은 양극재면 우리 모델은 작은 접촉-기계 몫만
  정직히 잡고, 지배 OTHER는 실험값 들어오면 채움.  = 정직하고 방어 가능한 스탠스.

## 핵심 발견
**접촉-기계 열화(ledger)는 총 fade의 ~2%뿐 → 진짜 열화는 화학(B-1 CEI)이 지배(~98%).**
(ledger R_ct 1.09× vs 실험 총 R_int 3.8~6.1×@1000cyc; 너 랩 Fig6e SBE/DBE.)
→ **MPM/ledger = 방향·기전; 크기·모양 = 화학 + 실험.**  이게 "MPM이 다 해준다"를 대체하는 정직한 형태.


## ★ 문헌 앵커 (2026-07-23 리서치, provenance 라벨)
[A]=table-verified(litdb PDF digest) · [B]=text-stated(search snippet, PDF 미검증).
- **SHAPE 문헌-앵커 (ASSUMED → 문헌지지 승격)**: **Park 2023 AEM**(10.1002/aenm.202203861) —
  계면 R vs √t가 **코팅/첨가제 = 선형-√t**(확산제한 Wagner film, 기울기 25.73 Ω·h⁻⁰·⁵), **bare =
  파라볼릭(super-√t)**.  ⇒ **화학 CEI 채널 = √N**(우리 기본값 문헌지지) · **bare 초과분 = 접촉손실이
  화학 위에 얹힘** = 우리 [화학√N + 접촉] 분해와 정확히 일치. [B]
- **화학 크기 앵커**: **Yun 2023 EnSM**(우리 랩, TableS1 [A]) — bare SC-NMC LPSCl **R_ct 341.7→982.3
  = 2.87×@100cyc**, R_ion 1.24×(전송은 열화 덜).  **Kim 2025**(우리 랩, TableS4/S6 [A]) — LNO 코팅이
  R_ct **~13~20× 억제**(453→22).
- **코팅 = modest fade**: **Payandeh 2023**(admi.202201806 [B]) 코팅 SC-NMC **93%@200cyc** vs 비코팅
  ~79%.  **Nature Energy 2025**(s41560-025-01726-8 [B]) Ni≥85 = CAM/SE **이탈(접촉손실)** 지배(=OTHER).
- ⛔ **여전히 없음**: 코팅 sulfide ASSB의 깨끗한 ≥4-N-점 R_int(N) **곡선**(WebFetch 403 차단).  가장 근접 =
  Yun/Kim 2점 table-verified + Park √t 함수형.  다음 추적: Seok 2026 AEM(aenm.202506351)·ORNL DRT·Trevisanello.

## 현 위치 · 산출물
- ✅ **도구**: `cycle_contact_ledger.py`(fade), `plot_fade_trajectory.py`(정직-분해 그림),
  `plot_focusing_colorbar.py`(current-focusing joint 컬러바), `calibrate_ledger_reflow.py`(철회판),
  `metric_split_check.py`(지표 분해), `gen_a1_anchors.sh`/kit companion(MPM 앵커).
- ✅ **webapp**: viewer3d.js 용어집 "사이클 열화 fade(N)" 정직 항목.
- ⛔ **B-1 N-전개** (지배적 화학 몫) — 다음 핵심.
- ⛔ **실험 R_int(N) 곡선** (WSL PDF #5) — 모양·크기 검증.

## 다음
1. **B-1 N-전개**: `step4_dyn.py --cycle-n N --i0-cycle-mult ...`로 CEI R_chem(N) 산출 →
   ledger 접촉(1.1×) + B-1 화학 합산 = 총 R_int(N) → 실험(3.8~6.1×) 재현.  ★크기 맞추는 길.
2. **실험 곡선** 디지타이즈(WSL) → 모양(√N/선형/포화) 검증.
3. (이후) webapp 인터랙티브 fade(N) 패널.

## 매뉴스크립트 narrative (한 문단)
STEP5는 pristine 전극(STEP1–4)의 사이클 열화 R_int(N)을 **first-principles 분해**로 예측한다:
계면저항 성장은 (i) **화학 계면상(CEI)** — 확산제한 Wagner 성장으로 **√N**(Park 2023, 코팅 셀서 선형-√t
문헌확인) — 과 (ii) **기계적 접촉손실** — MPM 충전-상태 gap(A-1, SC coverage −19% GPU검증)을 ledger
이산-CZM(recontact-forbid)으로 전개 — 의 **합**이다.  bare SC-NMC LPSCl서 화학이 지배(R_ct 2.87×@100cyc,
Yun 2023)하고 접촉은 소수(ledger 하한 ~1.1×; frozen-AM이라 골격재배열 제외).  **nm-코팅 양극재는 CEI를
~13~20× 억제**(Kim 2025)해 화학 몫이 작아지고(coated 93%@200cyc, Payandeh) 잔여 열화는 골격재배열·
CAM/SE 이탈(Ni≥85, Nature Energy 2025) 등 **모델 밖(OTHER)** 으로 이동한다.  ⇒ STEP5의 기여 = 각 채널을
frame[5]로 **정직하게 분리**(MPM/ledger=기전·방향, 크기=실험앵커), 좋은 양극재엔 열린 프레임(--chem-x)으로
작은 접촉몫만 정직히 잡는다.  (반증: reflow 지표착시·v2 반복사이클 MPM은 적대리뷰로 코딩전 기각.)
