# A-3 reflow "캘리브" — ★부분 철회 / 정직 재작성 (2026-07-22, 3렌즈 적대리뷰 후)

## ⚠ 헤드라인 정정 (RETRACTION)
초판(commit 31470f9)은 "빠른 ledger와 정확한 MPM의 SC 접촉손실 갭(30%→19%) = **SE plastic 재유동**,
`--reflow-recover 0.34`로 캘리브"라 했다.  **코드·전기화학·물리 3렌즈 적대리뷰 + metric 분해 실측 결과
이 인과 귀속은 틀렸다.**  갭은 대부분 **지표/법칙 아티팩트**이지 재유동이 아니다.

## metric 분해 (반증, 재현: `scripts/metric_split_check.py`)
같은 real_14 강체 기하를 **두 지표로** 재면:
| 측정 | SC 손실 | 정체 |
|---|---|---|
| ledger **Hertz-area** (Σ R·ov, 연속, elastic) | 30.0% | ledger 규약 |
| ledger **RIGID voxel** (MPM식 인접, 강체) | **16.8%** | ★재유동 없음, MPM과 같은 지표 |
| **MPM voxel** (재평형, 앵커 실측) | 19.4% | 진짜 |

- **지표+area법칙 (Hertz→voxel, 강체): +13.2%p ← 지배, 재유동 아님**
- **재평형/재유동 (voxel, 강체→MPM): −2.6%p ← 미미, 게다가 부호 반대**(MPM이 오히려 살짝 더 잃음)

⇒ **같은 voxel 지표로 재면 ledger 강체(16.8%) ≈ MPM(19.4%), Δ2.6%p — reflow 필요 없음.**
초판의 30%(Hertz)를 19%(voxel)와 비교한 게 **애플-오렌지**였고, reflow=0.34는 그 지표차를 메운 것.

## 왜 지표차가 지배하나 (리뷰가 준 물리)
1. **sub-voxel 후퇴**: SC 표면 34nm 이동 = MPM voxel(0.13µm)의 ¼ 미만 → 이진 voxel-coverage는 거의
   불감(voxel 하나가 SE 마주 보면 34nm 후퇴해도 계속 마주 봄).  Hertz-area는 ov에 선형 → 크게 감소.
   → 두 지표가 34nm 이동에 ~4× 다르게 반응 = 갭의 기원.
2. **elastic 법칙 오용 (물리 F4)**: SC-SE ov0 평균 92nm = SE 반경(0.5µm)의 **18%** = 깊은 소성 접촉.
   elastic Hertz `A∝R·δ`는 이 영역서 무효 — 소성 평탄접촉은 δ 34nm 줄어도 면적 거의 불변인데 πRδ는
   선형 감소로 **과대**.  production은 이래서 Stage-E **5-regime capped area**를 씀(`network_
   conductivity.py:240-264`).  ledger의 30%는 틀린 area 법칙 탓도 있음.  → reflow는 이 오차도 흡수.
3. **repo 자체 데이터와 상충 (물리 F3)**: `docs/data/mpm_coverage_plastic_vs_rigid.csv` = 같은 real_14
   plastic vs rigid coverage 증분 **+3~6%p** only (AM-rich = SE load-shielded).  "재유동 34% 회복"은
   우리 자신의 측정(재유동은 이 침대서 작다)과 모순.

## 통계·방법 결함 (리뷰 F2/F3/F4)
- **n=2 LOAO = 대수적으로 그냥 산포** (`blind_err = ledger_geom·spread`), out-of-sample 아님.
- 두 앵커는 **같은 스캐폴드·같은 poly ΔV, SC ΔV만 5.1↔5.9%(16%)** = 유사복제; 공통-모드 bias 상쇄돼
  안 보임.  "generalizes/일반화 ✅"는 좁은 ΔV 범위가 만든 tautology.
- **frame[4]/§2.5-6 위반**: reflow는 ledger를 MPM에 회귀(cross-fit) — "MPM-vs-ledger 일치를 *독립* 검증
  이라 부르지 말 것"(§2.5-6).  MPM의 charge-state coverage는 실험 앵커 없음(frame[1] LIMIT) → 진리로
  격상 금지.  §2.5-4b/F17의 blind-mid-N 게이트 미충족.
- **타깃≠산출 (F5)**: area-loss로 fit해 binary δcr 게이트에 적용; "|Δ|<2%p"는 in-sample fit 잔차.
- **provenance**: 앵커 JSON(19.4/22.7%)이 repo에 없음.  ★실제로는 v100 GPU 런(servo/hold 재평형) 산출
  (사용자 콘솔: coverage_AM_S 30.9→24.9→23.9) = 리뷰의 "CPU-only/재유동 없음"은 사실오류 — 앵커엔
  재평형 있음.  단 JSON 미커밋 = 감사 불가 지적은 유효 → 앵커 metrics 커밋/기록 필요.

## 정직한 실제 결론 (초판 대체)
- ★**같은 지표로 재면 빠른 ledger(16.8%)와 정확한 MPM(19.4%)는 이미 일치**(Δ2.6%p) — reflow 조작 없이.
  이게 원래 얻고 싶던 것(교차검증)이고, 초판의 "34% 재유동"보다 낫다.  단 §2.5-6대로 "**독립** 검증"
  아님 = MPM-앵커 self-consistency.
- **reflow=0.34 는 물리 상수가 아님** → production에 전파 안 함.  `--reflow-recover`는 노브로 유지
  (기본 0.0 = 무해·byte 불변), 라벨을 "**경험적 metric/law 정합 계수 (재유동 아님)**"로 정정.  실 앵커는
  nonzero 를 재유동으로 정당화하지 못함.

## 코드 수정 (리뷰 반영)
- ledger `--reflow-recover` help/provenance 재라벨(재유동 → metric/law 정합); `%%`→`%` 누출 수정.
- ledger selftest8 → **진짜 run() 테스트**(초판은 공식=공식 tautology, code MAJOR).
- calibrate reflow **[0,1] 클램프 + calibrated≠applied 경고**(음수 reflow 침묵 폐기 방지, F6);
  SC-fit 계수를 全 opening 접촉에 적용하는 scope 명기(F8); 산출 라벨 metric/law 정합.
- `metric_split_check.py` 신설 = 분해 재현(F1 reproducibility).

## 남은 진짜 과제 (초판이 "✅"로 건너뛴 것)
1. **like-for-like 지표**: ledger를 voxel로 재거나 MPM를 Hertz-area(+Stage-E capped)로 재서 **같은
   지표**로 비교 (§2.5-N5).  그래야 재유동 몫을 진짜 분리.
2. **영구 열화**: 반복사이클 MPM(v2) — δcr/rewet DOF.
3. **독립 검증**: 다른 스캐폴드/조성 + 실험(Kang&Shin/Yun) — MPM-self-consistency 아닌 진짜 검증.
4. **plastic area 법칙**: ledger의 Hertz πRδ → Stage-E capped area로 교체(소성 접촉 정확도).
