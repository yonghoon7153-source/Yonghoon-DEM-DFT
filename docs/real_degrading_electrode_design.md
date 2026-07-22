# 진짜 열화하는 전극(real degrading electrode) — 하이브리드 사이클 chemo-mech 설계

2026-07-22, 사용자 지시: "난 진짜 전극을 만들고 싶어" + (A) A10 심화 + (B) STEP4 계면상.
사이클 열화를 **voxel 지오메트리에 실제 반영**하되, 매 사이클 전체 파이프라인을 돌리지
않는 **하이브리드**(ledger 빠른 경로 + MPM 진짜 재변형 앵커).  A10 설계문서
(`a10_cycle_chemomech_design.md`)의 옵션 A/B를 **결합·확정**한 상위 설계.

## 0. 핵심 결정 (사용자 승인 2026-07-22)
- **깊이 = 하이브리드**: ledger(전 N, 빠름) + MPM 재변형(적응 앵커 N∈{0,5,10,25,50,100},
  초기 촘촘 §2.5, 진짜 지오메트리)로 ledger 규칙을 **캘리브+검증**.  → ledger가 "진짜 지오메트리
  열화"에 정합된 빠른 **기전모델**(외삽 아님, §2.5).  정확도 부족 시 앵커 증설 → 풀MPM 수렴.
- **frame[5] 분업 엄수**: MPM = 기계 재변형(지오메트리·응력·SE morphology·crack) · DEM/ledger =
  접촉망·percolation·transport 부기 · STEP4 = 화학 계면상(SEI/CEI).  겹치지 않게.

## 1. 현 상태 (출발점)
- **Pristine 지오메트리 = 이미 진짜**: MPM 300MPa 소성압밀 결과(se_dump = 실제 변형 SE 형상).
- **A10 v1 (옵션 A ledger)**: AM 수축을 **gap 계산 안에서만** 반영(강체구), Griffith/Bucci CZM →
  f_broken/A_rel/R_ct/σ_rel/Γ* → Kirchhoff 재솔브.  **voxel 지오메트리는 안 바뀜.**
- **한계(정직)**: 입자내부 균열·소성 재배열·τ 스파이크 과소평가.  ← MPM 재변형 앵커가 메움.

## 2. 하이브리드 아키텍처

```
 사이클 N ─┬─ [빠른 경로] ledger(전 N):  AM수축→gap→CZM→f_broken→Kirchhoff → σ(N),R_contact(N)
           │        ▲ 캘리브(G_c·δcr·re-contact f)
           └─ [진짜 앵커] MPM 재변형(N=0/50/100):
                 AM 반경 수축(ΔV/SOC) → MPM 재평형(SE 소성 재유동, void 생성)
                 → 응력장 → crack 판정(SE cohesive + AM Auerbach) → ★재복셀화★
                 → STEP3/4 재솔브 → σ(N)·coverage(N)·두께(N) [진짜 지오메트리]
```
- **캘리브 루프**: ledger의 자유 노브(G_c 2.8±1.8, δcr 100nm, re-contact f, ΔV 앵커)를
  MPM 앵커의 σ(N)/coverage(N)에 최소자승 맞춤 → ledger가 앵커 사이를 **진짜처럼** 보간.
- **검증 대조군(옵션 C)**: 측정 R_int(N) 밴드(A11-② rint_cycle_traj) 안에 드는가.

## 2.5. ★ "외삽 아니냐" 우려의 해소 — 정확도 빌드 전략 (사용자 지적 2026-07-22)
우려: ledger가 MPM 앵커 사이를 채우면 **외삽 아닌가 → 부정확**.  답 = **ledger를 curve-fit이
아니라 MECHANISTIC(기전-기반)으로 짓고, MPM 앵커는 "숫자 맞춤"이 아니라 "물리 주입+검증"으로
쓴다.**  그러면 앵커 사이는 외삽이 아니라 **검증된 물리 예측(interpolation of a physics model)**.

1. **ledger = 결정론적 per-cycle 기전 규칙** (curve-fit ❌): 매 사이클 AM수축(ΔV)→접촉gap(계산)→
   Griffith 파단(계산)→영구/재접촉(규칙).  주어진 지오메트리+규칙이면 궤적은 **예측**되지 외삽 아님.
   MPM 앵커는 규칙의 **미지 물리상수(G_c·δcr)만** 고정 + 기전 자체를 **검증**.
2. **강체구 ledger가 놓치는 물리를 MPM 앵커가 "주입"**: rigid-sphere는 (a) SE 소성 재유동(gap 재습윤),
   (b) crack→void→**τ 스파이크**(So 2021 균열지배)를 못 만듦.  MPM 앵커가 이 응답을 드러내면 →
   ledger에 **물리 항으로 흡수**(SE-재유동 응답·τ-스파이크 항, MPM 앵커서 보정).  즉 ledger가
   "MPM-informed 물리 모델"이 됨 → 앵커 사이도 그 물리를 **운반**.  ← 정확도의 근원.
3. **적응적 앵커 밀도**: 손실이 빠르고 비선형인 **초기(N=0/5/10/25)에 촘촘**, 포화 후기(50/100)는 성김
   (So 2021 "첫사이클 최대손실" → 초기 곡률이 관건).  외삽 구간(N>100)은 앵커로 **닫음**(마지막 앵커).
4. **정직한 오차 막대**: 각 앵커에서 **ledger-예측 vs MPM-실측 불일치**를 그대로 리포트 = 모델
   신뢰구간.  타이트하면 사이 신뢰, 벌어지면 **앵커 추가 or 물리 항 보강**(적응).  → 외삽 위험을
   숨기지 않고 **정량 노출**.
5. **과적합 방지**: 앵커 점수 ≥ 자유노브 수 + 정칙화.  노브를 4→2(G_c·δcr)로 줄이고 나머지는 문헌 고정.
6. **최대정확 상한 = 풀 MPM**은 언제나 가능(비용만) — 하이브리드가 앵커에서 풀MPM과 만나므로,
   "얼마나 촘촘히 앵커하느냐"로 **정확도↔비용을 연속 조절**.  기본 6앵커→불충분하면 증설.

⇒ 결론: 하이브리드는 "fit+외삽"이 아니라 **"기전모델 + 앵커에서 물리주입·검증 + 적응증설"**.
외삽 위험은 오차막대로 노출하고 앵커로 닫는다.  정확도가 부족하면 앵커만 늘리면 풀MPM에 수렴.

## 3. 조각 (구현 단위 — 각 3각 적대리뷰)

### (A) 기계 열화
- **A-1. MPM 사이클 재변형 모듈** (`mpm3d_compaction.py --cycle-deform`): am_scaffold 반경을
  ΔV(SOC)로 수축(SC 격자 −5.1% / poly Parks 분기) → 고정AM 갱신 → SE MPM 재평형(기존 servo/hold)
  → se_dump' 재변형 형상.  ★GPU (체크포인트만).  frame[5]=MPM 소관.
- **A-2. 응력·crack 커플**: MPM 응력장(σ_vm)에서 SE cohesive 임계(G_c) 넘는 셀 = crack →
  국소 σ 절단(void).  AM 파단은 기존 DEM Auerbach(f_intact)와 **중복 없이** 결합(AM내부=참고,
  접촉면=ledger).  → τ 스파이크(So 2021 균열지배) 포착.
- **A-3. ledger 캘리브·보간**: `cycle_contact_ledger.py`에 `--mpm-anchor N=path` 훅 →
  MPM 앵커로 노브 fit → 전 N 빠른 전개.  출력 coverage(N)·σ_e/σ_ion(N)·R_contact(N).
- **A-4. percolation(N)**: 재복셀/ledger 후 연결성분(econn·f_perc) → 끊김 궤적.

### (B) 화학 열화
- **B-1. STEP4 계면상 성장** (`step4_dyn.py`): 지금 ASR_film=0 슬롯을 **ASR_film(N)** 성장으로:
  Koerver 첫사이클 점프 + √N(SC, 확산제한 CEI) / 선형(poly) — R_int(N) 설계문서 §3.1 형태 재사용.
  → R_chem(N) 직접 산출.  방전곡선(N) = 계면상↑ → 분극↑.
- **B-2. R_int(N) 통합**: R_int(N)=R_contact(N)[A, ledger+MPM] + R_chem(N)[B, STEP4] +
  R_collector(N)[기존].  → 이종기술 cycled(150)를 **assumed-form에서 모델-산출로 승격**.

## 4. 출력·검증 (진짜 전극의 증거)
- 궤적: σ_e/σ_ion(N)·coverage(N)·두께(N)·R_contact/chem/int(N)·용량(N)·방전곡선(N)·Γ*(N)
- 앵커 검증: ① Kang&Shin R_int(N) 4.4×(B-NCA)/1.5×(U-NCA) 모양 ② So 첫사이클 최대손실
  ③ Yun R_ion +23%(τ 완만↑) ④ Jung SC/PC retention 부호 ⑤ 측정 R_int(N) 밴드 내(옵션 C)
- **진짜 지오메트리 증거**: MPM 앵커의 재변형 se_dump'(void 생성·SE 재유동·crack) 시각화(viz_mpm).

## 5. 구현 순서 (GPU 상황 반영)
- **지금(GPU 0.2C 점유 중, CPU 가능)**: B-1(STEP4 계면상, selftest 검증) → A-3 ledger 캘리브 훅
  (MPM 앵커 없이도 형태 구현) → A-2 crack 판정 로직.
- **GPU 여유 시**: A-1 MPM 재변형 앵커 3점 실행 → 캘리브 → 통합 궤적.
- 각 조각 = **코드·전기화학·물리 3각 적대리뷰** 후 커밋.

## 6. 미결 (구현 중 논의)
1. ΔV 앵커: SC −5.1%(Kondrakov) vs 5.9%(Yun/Kang) — 스윕축.
2. crack 임계 G_c 2.8±1.8: 중앙 고정 vs 스윕.
3. MPM 재변형서 SE 재유동 프로토콜: servo(정압) vs hold(변위) — 재습윤 물리와 연결.
4. 캘리브 노브 과적합 방지: 앵커 3점에 노브 4개 → 정칙화 or 노브 축소.
5. B-1 계면상 성장 형태(√N/선형) poly/SC 분기 = D_s/i0 분리축과 동일 규약.
