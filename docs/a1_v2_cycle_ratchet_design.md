# A-1 v2 — 반복사이클 MPM: 소성 ratcheting 영구(비가역) 열화 설계 (2026-07-23)

## 목표 (v1 대비)
- **v1 (`--cycle-deform`)**: 충전상태 **1점**(가역 SOC breathing) — 방전하면 되돌아옴.
- **v2 (`--cycle-repeat N`)**: 충전↔방전 **N회 반복** → SE 소성 재유동이 방전 시 완전히 안 되돌아옴
  (J2 소성 = 비가역) → **영구 접촉 변화 누적(ratchet)** → **fade(N) 궤적을 first-principles로**.

## 기전 (frame[5] = MPM 소관: 소성 비가역)
```
초기 압밀(pristine) → 사이클 루프 N회:
  ┌ 충전 반각: SC 반경 −ΔV/3 수축 → am_mask 갱신 → SE 소성 재평형(servo 정압)
  │            → SE가 열린 gap에 흘러듦(소성 항복)
  └ 방전 반각: SC 반경 복원 → am_mask 갱신 → SE 재평형
               → 흘러든 SE의 탄성분만 회복, ★소성분은 잔류(ratchet)
  → SE 상태(x, F, dg, v) 사이클 간 PERSIST (리셋 안 함) → 소성 누적
  → 방전-말 coverage/porosity 측정 = 영구(비가역) 상태 → fade(N)
```
핵심: J2 소성에서 항복 후 하중제거 시 **탄성 스프링백만 회복, 소성변형 잔류** → 반복 시 단조 누적.
이게 v1(가역)이 못 주는 **영구 열화**이고, ledger의 ASSUMED-FORM Miner 보간을 **기전-궤적으로 교체**.

## ★ 정직 가드레일 (reflow 철회 교훈 = 오버클레임 금지)
1. **접촉-기계 열화만**: v2 fade(N) = SE-AM 접촉 기하의 영구변화.  화학 CEI(=B-1)·취성 crack(=FEM)
   별개 — 합산 금지, 각 채널 명기.
2. **magnitude는 앵커 대기**: v2는 궤적 **SHAPE**(√N? 선형? 포화?)를 first-principles로 산출.  절대크기·
   실 fade%는 **실험 앵커(Kang&Shin R_int(N) 4.4×/1.5×) 회귀** 후 확정.  v2 단독으로 "실 fade" 주장 금지.
3. **1 스캐폴드(real_14)**: 독립 케이스(다른 조성) 검증 별개 = §2.5 F17.
4. **지표 like-for-like**: v1 교훈 — fade를 **같은 voxel-coverage**로 재고 ledger와 비교(Hertz-area 혼입 금지).
5. **BC**: `--protocol servo`(정압=스택압 일정=실셀).  hold(변위)는 사이클서 체적변화 못 따라가 부적합.
6. **비가역 증명(N4 수치위생)**: 방전-말 상태가 진짜 pristine서 벗어났는지 = **누적 소성변형 Σdg(N)
   vs 탄성회복 분리** 리포트.  Σdg가 단조↑ = ratchet 진짜; 안 늘면 = 가역(v2 무의미) 자기진단.
7. **그리드-불변(N4)**: am_mask는 매 반각 갱신하되 dx·원점·nz·FLOOR·lateral_box 전 사이클 고정.
8. **수렴 가드**: 매 반각 servo 미수렴 시 하드-실패(조용한 쓰레기 누적 방지).

## 비용
사이클당 2 servo(충전+방전).  N=10 = 20 run(~20분/384).  fade(N)를 몇 N점(1/2/5/10/25/50)서 산출
= 비쌈 → ledger가 그 사이 보간(ASSUMED-FORM Miner → **v2 기전-궤적 앵커**로 교체·캘리브).

## 출력
- per-cycle 방전-말: coverage_AM_S/P(N), porosity(N), Σdg(N), thickness(N) → fade(N) 궤적 CSV/JSON.
- ledger 캘리브: v2 fade(N)로 **δcr·rewet_frac 회귀**(reflow 아님 — 진짜 영구 DOF; G_c 여전히 제외).
- viz: pristine vs N-cycled se_dump' 재변형 형상.

## webapp UI 반영 (사용자 지시)
- 뷰어: **가역(v1 charged) / 비가역(v2 discharged) 토글** + cycle-N 슬라이더 + fade(N) 궤적 플롯.
- 지표설명(help): "v2 = 반복사이클 소성 ratchet 영구열화; magnitude 앵커대기; 접촉-기계만".
- 비교모달: pristine↔N-cycled coverage/porosity Δ + Σdg 단조성(비가역 증명) 표시.

## 구현 순서 (reflow 교훈: 설계 리뷰 먼저)
(i) 이 설계 3렌즈 적대리뷰 → (ii) mpm3d `--cycle-repeat` 루프(SE state persist, am_mask 재갱신, CPU
기하검증) → (iii) 코드 3렌즈 리뷰 → (iv) GPU 실행(너) → (v) ledger v2-앵커 캘리브 → (vi) webapp UI.
