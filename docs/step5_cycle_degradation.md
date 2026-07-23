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
| **B-1** | 화학 계면상(CEI) 성장 | STEP4 interphase (i0(N)↓+필름옴성) | **~98% 지배** | 🔶 훅 있음, N-전개 미실행 |
| **실험** | 크기·모양 앵커 | R_int(N)/retention(N) 곡선 | 검증 게이트 | ⛔ WSL PDF(#5) |

합산: **총 R_int(N) = R_contact(N)[A-1 검증 gap → A-3 ledger] + R_chem(N)[B-1] + R_collector(N)**.

## 여정 (기각된 것 = 정직화 과정, 적대리뷰가 오버클레임 차단)
- ❌ **v2 반복사이클 MPM** — 3렌즈 만장일치 기각(코딩 전): rigid pin-mask는 방전 스프링백 불가 ·
  isochoric J2는 영구 접촉손실 금지(부피보존=void 메꿈) · 재변형 sub-voxel(0.2셀=null mask) ·
  servo 자기-drift.  docs/a1_v2_cycle_ratchet_design.md.
- ❌ **reflow 캘리브** — metric 아티팩트로 철회(ledger Hertz-area 30% vs MPM voxel 19% = 지표차,
  재유동 아님; 같은 voxel 지표선 16.8%≈19.4% 이미 일치).  docs/a3_reflow_calibration.md.
- ✅ **살아남은 것** = 위 정직 4조각 분해.

## 핵심 발견
**접촉-기계 열화(ledger)는 총 fade의 ~2%뿐 → 진짜 열화는 화학(B-1 CEI)이 지배(~98%).**
(ledger R_ct 1.09× vs 실험 총 R_int 3.8~6.1×@1000cyc; 너 랩 Fig6e SBE/DBE.)
→ **MPM/ledger = 방향·기전; 크기·모양 = 화학 + 실험.**  이게 "MPM이 다 해준다"를 대체하는 정직한 형태.

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
