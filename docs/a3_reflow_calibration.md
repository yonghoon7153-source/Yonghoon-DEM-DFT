# A-3 ledger reflow 캘리브 — MPM 앵커로 SE-재유동 DOF 회귀 (2026-07-22)

real_degrading_electrode_design §3 A-3 (ledger 캘리브)의 첫 착지.  A-1 MPM 앵커(real_14, GPU)로
빠른 ledger의 **ε(가역 변형) DOF = SE plastic 재유동 회복**을 회귀했다.

## 발견 (fast vs accurate 불일치의 정체)
- **빠른 근사 (cycle_contact_ledger, 강체구+기하)**: SC(AM_S 2µm) 수축 −5.1% → 표면 34nm 이동 →
  접촉면적(Hertz A∝R·ov) 기하 손실 **30.0%** (−5.9%면 33.7%).
- **정확한 MPM (A-1 --cycle-deform, plastic SE)**: SC coverage 손실 **19.4%** (−5.9%면 22.7%).
- **갭 = plastic 재유동**: 말랑 SE가 벌어진 접촉에 흘러들어 손실의 ~34%를 회복 — frame[5]에서 MPM만
  하는 일, 강체구 ledger엔 없음.  (⚠ MPM voxel-coverage ↔ ledger Hertz-area 지표차이도 일부 혼입 =
  순수 재유동 아님, ASSUMED-FORM.)

## 캘리브 결과
| ΔV(SC) | MPM 손실% | ledger 기하% | reflow=1−MPM/led |
|---|---|---|---|
| −5.1% | 19.4 | 30.0 | 0.352 |
| −5.9% | 22.7 | 33.7 | 0.327 |

- **reflow-recover = 0.34** (SE 재유동이 기하 접촉손실의 34% 회복).
- **일반화**: 두 ΔV의 reflow 산포 0.024 (<0.05) → 단일 계수가 서로 다른 충전깊이에 통함.
- **LOAO(정직, out-of-sample)**: 한 앵커로 fit → 나머지 blind 예측 오차 **0.9~2.1%p** (in-sample 아님).
- 적용 후: `--reflow-recover 0.34` → ledger 21/24% ≈ MPM 19/23% (|Δ|<2%p).

## 구현
- `cycle_contact_ledger.py --reflow-recover R` [0,1]: 개구(SC 수축, 양수 이동)만 (1−R)배로 회복,
  폐합(poly 팽창)은 무관.  기본 0.0 = 순수기하(현행 byte 불변).  selftest8.
- `calibrate_ledger_reflow.py`: MPM 앵커(N0+충전들) + atoms(또는 --from-scaffold) → reflow 회귀 +
  일반화/LOAO 리포트.  selftest PASS.  재현: `--from-scaffold docs/data/real14 --pristine m_N0.json
  --charged m_charged.json m_charged_deep.json`.

## 정직한 한계 (다음)
- ★**ε(가역) DOF만 캘리브** — 영구 열화 DOF(δcr, rewet_frac)는 **반복사이클 MPM(v2)** 필요.  현 단일-
  충전 앵커는 가역 변형 진폭만 준다(N6-a).
- ★**앵커 2점** → LOAO는 최소한의 out-of-sample(1-held-out).  ΔV 스윕 촘촘히 + poly ΔV 스윕 = 더 강한 검증.
- ★지표 혼입(voxel↔Hertz)을 분리하려면 MPM coverage를 Hertz-area 정의로 재산출 or ledger를 voxel로.
- σ_e/σ_ion 절대 궤적으로의 전파는 poly_internal_void→σ_e 결합(앵커 대기) 착지 후.
