# scripts/step6_surrogate.py v1 설계·구현 기록 — MLIP식 전기화학 surrogate (STEP6)

작성 2026-07-27.  구현 `scripts/step6_surrogate.py` (~1,300줄, numpy-only 코어 + import-guard).
클라우드 selftest **8/8 PASS** (전문 §9).  모든 출력 첫 줄 = §F1 배너
`SURROGATE/UNCALIBRATED — 전개값은 STEP4-모델 상속 예측; 절대 신뢰는 앵커(실솔버) 상태만 (§F1)`.

## 0. 포지셔닝 (진단결과 1-5·기존 자산과의 관계)

**MLIP 대응표**: 원자 국소환경 서술자→(에너지·힘)+위원회 불확실성→MD 전진, 외삽 감지 시 DFT
앵커 호출·재학습 = 우리: (SOC·표면 stoich·η·유효저항 서술자 ‖ 설계벡터)→(다음 스텝 Δstate)+
위원회 밴드→시간 전개, σ>gate 시 STEP4 실솔버 앵커 호출·transition 버퍼 축적·(v2)온라인 재학습.
**파이프라인 정확도 상속 = MLIP 규약**(ml_cycle_surrogate.py 독스트링과 동일 문장) — 학습데이터
provenance 는 'model'(STEP4 산출)이므로 모든 출력은 SURROGATE/UNCALIBRATED (§F1).

**솔버 치료(R1-R5)와 직교**: R1/R2/R4/R5 = 솔브 1회 단가·조건수를 고치는 공급-측 치료.
STEP6 은 **수요-측** — (a) 비싼 스텝 자체를 surrogate 전개로 건너뛰고 앵커만 실솔브,
(b) 진단1[3-b]의 "스텝비용 = ev 2-4회 × nnAMG 솔브"에서 surrogate 의 V 예측을
`_bracket_illinois` 의 V_guess warm-start 로 줘 ev 횟수를 줄이는 (v2 훅) 보조 지렛대.
**정직 한계(고찰)**: 앵커 호출 시 깊은 보정해 목표(atol_cg ≈ 2.7e-13~2.7e-14, 진단1[2])가
Jacobi 자기바닥(~1.4e-12) 아래인 한 **nnAMG 의 정당한 필요는 잔존** — STEP6 은 호출 빈도를
줄일 뿐 단가를 못 고침(단가는 R1/R2/R4 몫).  "수렴 다 안 됐어도 확률 높으면 진행"의 공식화:
deep_weak escape 로 조기종료된 부분수렴 상태(resid 정직 보고, 진단1[1-b])를 위원회 밴드가
덮으면 앵커로 **명시 로그와 함께** 수용(이중 증거: 솔버 resid + surrogate 밴드) — 침묵 수용
금지 (v2, §8-2).

**기존 자산 재사용 계약** (구현에서 실제로 쓴 것):
- `ml_cycle_surrogate.py`: nan=결측(§F1 날조 0)·median-impute+전-결측 경고·import-guard 패턴·
  provenance 라벨 형식 차용.  **스케일 분업**: ml_cycle_surrogate = 사이클-N 축(R_int(N)·
  retention) ‖ step6 = 사이클-내 시간축(V(t) 전개).  step6 per-cycle 지표(delivered·Q_ohm 분담)
  가 ml_cycle_surrogate 타깃 공급원(v2 배선, §8-3).
- `ml_design_loop.py`: `scalarize`/`APP_OBJECTIVES` 를 rank_candidates 점수화에 import 재사용
  (missing='penalize' 규약 포함; **s6_ 네임스페이스**로 등록해 σ-앱 'balanced' 와 이름충돌 방지
  — 구현 중 실제로 충돌 발견·수정); `sobol_doe` 는 CLI `--sobol/--bounds` 후보 생성기.
- `eis_drt_ica.py`: 회로소자 유도식을 물리-basis 로 재사용 — 스텝별 유효저항
  r0_eff=(Q_ohm_e+Q_ohm_i)/I², r_ct_eff=Q_ct/I², r_film_eff=Q_film/I² (npz Q_*_W 열에서 직접,
  frame[4] 회로와 동일 분해), τ_w=r_p²/D_s.
- `cycling_data_ingest.py`: provenance_gate 규약 차용 — step6 은 chemistry 대신
  **provenance='model-surrogate'** 게이트: 절대 신뢰는 앵커(실솔버) 상태에만, 전개 구간은
  UNCALIBRATED 밴드.

## 1. 파일 구조 (단일 파일)

```
scripts/step6_surrogate.py
├─ § 스키마/상수      F1_LABEL / SCHEMA_VERSION / DESIGN_FEATURES / STATE_KEYS /
│                     BASIS_KEYS / DELTA_TARGETS_CC·CV / _CORE_KEEP / S6_OBJECTIVES
├─ § (1) 추출기       load_step4_npz / design_from_run / _design_vec / _physics_basis /
│                     _row / _run_states / _resolve_step3 / extract_transitions
├─ § (2) 위원회       RidgeCommittee (numpy) / SkCommittee (sklearn guard) /
│                     save_model·load_model (phase별 cc/cv + bank 를 한 npz) / train_from_corpus
├─ § (3) 전개         propagate (+멤버 누적경로 밴드, p_cut) / _state0_from_bank / make_anchor_fn_cli
├─ § (4) 랭킹         rank_candidates / pick_next_anchor
├─ § (5) 검증         _synthetic_rc_corpus / _synth_run / _synth_state_at / _selftest
└─ § (6) CLI          main (--train / --propagate / --rank / --selftest)
```

## 2. 스키마

```python
DESIGN_FEATURES = ['c_rate','thickness_um','r_int_ohm_cm2','d_s_m2s','i0_A_m2','asr_film',
                   'temp_k','areal_mAh_cm2','i_1c_A','bv_face_per_cm2','x0','x100','cv_hold',
                   'sigma_e_eff','sigma_ion_eff','log_tau_w']          # 16 (결측=nan, 날조 0)
STATE_KEYS      = ['x_mean','x_surf_p05','x_surf_p50','x_surf_p95','eta_kin_V','eta_diff_V',
                   'v_terminal','i_norm','r0_eff','r_ct_eff','r_film_eff','phase_cc']   # 12
BASIS_KEYS      = ['b_head_room','b_gap_surf_core','b_ir_scale','b_bv_asinh','b_log_dt',
                   'b_gap_relax','b_coul_step']                        # 7 (state/design만 = 누수 0)
X 행 = state(12) ‖ design(16) ‖ basis(7) ‖ dt_s(1) = 36 feature
DELTA_TARGETS_CC = [d_v_terminal, d_x_surf_p05/50/95, d_eta_kin_V, d_eta_diff_V]   # 6
DELTA_TARGETS_CV = CC + [d_i_norm]                                     # CV 는 전류가 상태
```

**★ 물리 하드코딩(잔차학습 — MLIP 의 '알려진 항은 학습 안 함')**:
`Δx̄ = ±(i_norm·dt/3600)·(x100−x0)` 쿨롱계수는 정확한 부기(질량보존; dead-AM 포함 부피가중
x̄ 에도 정확)이므로 **학습하지 않고 전개에서 정확 적용**.  추출기는 실 npz 에서 이 항등식을
검산(forward-Euler·사다리꼴 중 최소 상대오차; >1e-6 경고, >1e-3 런 제외 + excluded 목록 반환)
→ 추출기 자가검증.  표면 percentile·η만 학습 = 확산 지연·비선형 BV 라는 '모르는 절반'에
모델 용량 집중.

**설계서 대비 구현 편차 (전부 정직 기록)**:
1. **basis 확장 2항**: `b_gap_relax = (표면-코어 갭)·dt/τ_w` (확산 완화 스텝의 이산화),
   `b_coul_step = i_norm·dt/3600·(x100−x0)` (쿨롱 구동 스텝).  설계서 5항의 물리-유도 확장 —
   d_x_surf 의 두 구동항을 직접 서술(frame[5] payoff: "why" 있는 feature).  전부 state/design
   에서 계산 = 누수 없음.
2. **_CORE_KEEP 확장**: 설계서의 (x_surf_p50, i_norm, dt) + 위 basis 2항 — 물리 구동항을
   subset 에서 떨어뜨리면 위원회 평균이 퇴화하기 때문(같은 '퇴화 방지' 취지).
3. **phase 추론**: npz 에 phase 배열이 없음 → `|I| ≥ 0.995·|I[0]|` = CC (CC 전류 상수·CV 감쇠).
4. **밴드 기본 'member'** (설계서 기본 RSS 에서 변경 — selftest 실증 근거): §5 참조.
5. **state0**: OCP 없이 V(x_init) 를 만들 수 없음 → bank(코퍼스 각 런 첫 스텝 state) 회귀
   (n_runs≥8; 미만 최근접) + 'state0-보간(UNCALIBRATED)' 라벨.  x0/x100 은 bank 로도 안 채움
   (쿨롱창 = §F1 필수 입력 — 없으면 명시 에러).
6. **r0/r_ct/r_film 상태는 v1 전개에서 상수**(Δ 타깃에 없음) — 저율·CC 에서 근사적 상수;
   v2 학습 후보.
7. v1 은 **방전 전용** (charge=True → NotImplementedError; §8).

## 3. (1) 추출기

- `load_step4_npz(경로|dict)` — step4_dyn np.savez 규약(t, V_terminal, I, x_mean, x_surf_p05/50/95,
  eta_kin_mean, eta_diff_mean, Q_ohm_e/i_W, Q_ct_W, Q_film_W, newton_resid, kcl_rel,
  energy_balance_rel, I_1C_A, q_frac_at_cutoff, viz_z_um, params_json) 로드.  합성(dict) 공유.
  필수 키 누락 → 런 스킵 + excluded 기록 (크래시 금지).
- `design_from_run` — params_json + npz + 선택 STEP3 join → 설계 dict.  per-particle d_s/i0
  (dict형 {min,max}) 는 log-mean(√(min·max)).  areal/bv_face 는 area_cm2 있을 때만(실 step4
  params 엔 없음 → nan 정직).  STEP3 join: ① CLI `--step3-json case=path`(경로 부분일치)
  ② 케이스 폴더 sibling `mpm_payload.json` 자동 탐색 → `step3.sigma_*_eff_S_cm` — 실패 시 nan.
- `extract_transitions` — 스텝 k→k+1 전이쌍, dt 를 feature 로(적응 dt 지원).  phase 경계
  (cc↔cv) 쌍은 양쪽 모두 제외(라벨 오염 방지).  quality_gate: newton_resid > 4·median 스텝
  → weight 0.25 태그(포함하되 정직 다운웨이트 = 부분수렴 데이터도 '라벨과 함께' 쓰는 STEP6
  취지; 배수는 ASSUMED).  반환에 X_cc/Y_cc/w_cc/run_cc(LOCO용) ‖ X_cv/… ‖ bank(state0) ‖
  meta/quality/excluded ‖ F1 라벨.

## 4. (2) 위원회

`RidgeCommittee(n_members=24, lam=1e-3, feat_frac=0.7, boot_frac=0.8, seed)` — numpy 폐형해:
bootstrap(행) × random feature-subset(열; _CORE_KEEP 상시 유지) ridge (표준화 μ/σ 저장,
절편 무벌점).  평균=예측, 멤버 std=인식적 불확실성 프록시(휴리스틱 ASSUMED).  fit 잔차
가중-RMSE = `sres` (aleatoric 프록시 — 밴드에 사용).  전-결측 feature → ml_cycle_surrogate
규약 경고.
- `loco_score` — ★**leave-one-curve-out(런 단위) R²** 만 보고(시계열 자기상관 누수 차단;
  random-split R² 는 보고 금지 — repo LOOCV 규율의 시계열판).  selftest 에서 random-split 을
  '계산만' 하여 규율 데모.
- 저장: `save_model/load_model` — phase 별 2 위원회(cc_/cv_ prefix) + bank_design/bank_state +
  meta_json(F1_LABEL·SCHEMA_VERSION·코퍼스 경로+md5·LOCO)을 **한 npz** 에.  SCHEMA_VERSION
  불일치 → 명시 ValueError.  왕복 bitwise (selftest ⑦).
- `SkCommittee(RidgeCommittee)` — sklearn GBR 위원회(비선형; WSL).  클라우드에선 fit 이
  `{'ready': False, 'status': …}` 반환(크래시 금지) → `train_from_corpus` 가 RidgeCommittee 로
  graceful 폴백.  predict 인터페이스 동일 → propagate/rank 는 모델 종류 무관.  저장은 v2
  (joblib; v1 은 npz=Ridge 만).

CC 위원회 필수·CV 는 전이쌍 ≥30 이면 학습(코퍼스에 CCCV 완주런 존재: 2026-07-21 3.18 mAh
SBE/DBE).

## 5. (3) propagate — 불확실성-게이트 전개

자기회귀: X=[s_t‖design‖basis‖dt] → 위원회 Δ → s_{t+1}=s_t+Δ, 단 Δx̄=쿨롱 정확항.
CV phase 진입 시 V 를 v_cut 에 핀, d_i_norm 으로 전류 감쇠, i_cut_frac 종료.

**밴드 (전부 UNCALIBRATED)** — 3모드, 기본 `'member'`:
- `'member'`(기본) = √(std(멤버별 누적 V경로)² + Σs_res²).  각 멤버의 스텝-편향이 경로를 따라
  지속 누적되는 것을 그대로 반영(독립가정 없음; MLIP 위원회-궤적 스프레드).  p_cut draw 와
  동일한 cumV_m 을 공유 = 내부 일관.
- `'rss'` = √(Σstd² + Σs_res²) — 독립가정 (설계서 원안 기본).
- `'sum'` = Σstd + √Σs_res² — 최보수 상한.
★ **기본값 변경 근거(실증)**: selftest ③ held-out 전곡선에서 rss 커버리지 **31%** vs member
**80%** — 자기회귀 상관에서 RSS 과소(설계서 스스로 ★ASSUMED 로 경고한 그 실패)를 합성
진실로 실증 → v1 기본 = member.  캘리브레이션(실 STEP4 대조) 전까지 어느 모드든 UNCALIBRATED.

**σ_gate**: 스텝 std(d_v) > sigma_gate_mv →
- anchor_fn 있음: state = anchor_fn(state, design) 실측 교체 + 불확실성 리셋 + **transition
  버퍼 축적**(반환 `transitions_new` — v2 온라인 재학습 입력).
- anchor_fn 없음: anchors[] 에 'ANCHOR-NEEDED'(t, state, std) 마킹; force=False(기본) 전개
  정지 = **확신 없는 곡선 날조 금지**; force=True 는 밴드 팽창 유지한 채 계속(스윕/정성 전용).
- anchor_every=N: N스텝마다 강제 앵커(드리프트 상한; v2 라이브 훅 기본).

**컷오프(확률적 진행 = "확률 높으면 진행"의 구현)**: 멤버 누적경로 + aleatoric noise 로
V-draw n_draw개 → p_cut = P(V<v_cut).  p>0.5 종료; p 가 0.1/0.9 를 지나는 [t_lo, t_hi] =
'불확실 종료창' → delivered_frac = (mean, lo, hi) — 끊긴 시점의 불확실성을 숫자로.

`make_anchor_fn_cli(cmd_template)` — v1 앵커 어댑터(프로세스 경계, 느슨한 결합): 템플릿을
state/design 으로 format → 실행 → **stdout 마지막 JSON 줄 = 갱신 state** 규약.  v2 에서
step4_dyn `on_step` 라이브 훅으로 대체.

## 6. (4) rank — 픽·확률·최적 경로

`rank_candidates`: 후보마다 propagate(force=True; 랭킹은 정성 허용) → metric
{delivered, v_mean, q_ohm_frac, anchor_need_frac} (v_mean 은 (v̄−v_cut)/(V0−v_cut) 정규화;
q_ohm_frac = r0/(r0+r_ct+r_film) state0 기준) → `scalarize`(ml_design_loop 재사용,
missing='penalize', 앱 = s6_balanced/s6_fast_charge/s6_explore).  **p_pick** = Thompson식:
후보별 점수 draw(delivered 는 종료창 반폭·v_mean 은 밴드로 가우스 근사 샘플 — ASSUMED)
n_draw개 → argmax 빈도/n_draw = '이 후보가 최선일 확률'.  Σp_pick=1.

`pick_next_anchor`: p_pick 상위권(≥max(0.1, 0.5·max)) 중 anchor_need_frac 최대 = **실솔버
1런의 정보이득 최대 지점**(MLIP on-the-fly 의 DFT-호출 선택 대응).  step4_dyn 실행 커맨드
힌트 동봉.

폐루프: `sobol_doe`(CLI --sobol/--bounds) → rank_candidates → pick_next_anchor → 실솔버 런 →
extract_transitions 증분 → 재학습 = 사용자 비전 "여러 후보군 중 다음 현상 예측해 픽·확률·
최적 경로가 바로 나오게".

## 7. selftest (합성 RC-방전 ODE — TEST-ONLY §F1) + CLI

합성 2-상태 ODE (물리값 아님): dsoc̄/dt=i/3600 (정확 쿨롱); dsoc_s/dt=(soc̄−soc_s)/τ +
k_c·i/3600 (표면 지연, k_c=1.6 = 방전 시 표면 선행 — x-증가 규약이라 설계서의 −k·I 를 +로);
V = 4.2 − 0.9·soc_s − R·i·areal·1e-3 − 0.03·asinh(i/i0) (옴+BV꼴).  설계축 (R, τ→d_s, areal,
i0, c_rate) 랜덤 샘플 24런(6런 CCCV), 적응 dt(20/35/50s)·V-noise 0.2 mV·컷오프 — 실 npz 와
같은 필드명 dict → 추출기 완전 공유.  τ_w=r_p²/D_s=τ 로 매핑해 basis 정합.

체크 8종: ① 추출 스키마·쿨롱 검산·phase 경계 제외 ② LOCO R²(d_v)>0.9 (random-split 은
계산만) ③ held-out 전곡선 밴드 커버리지 ≥68% (member) + rss 과소 실증 ④ OOD(R×5 + τ×8
다축) std 팽창 >2× → gate 발동 + force=False 정지 ⑤ 모의 실솔버(ODE 재적분) 앵커 → 오차
감소 + 버퍼 축적 + CLI 어댑터 JSON 규약 ⑥ rank 방향·p_pick·Σ=1·next-anchor ⑦ §F1 라벨 전
반환 + save/load bitwise + 스키마 가드 ⑧ SkCommittee import-guard graceful.

CLI: `--selftest` / `--train 'glob' [--step3-json case=path]* --out M.npz [--sklearn]
[--no-loco]` / `--propagate --model M --design d.json [--sigma-gate-mv --force --anchor-cmd
--anchor-every --band-mode]` / `--rank --model M (--candidates c.json | --sobol N --bounds
b.json) [--app]`.  전 모드 첫 줄 = F1 배너.  CLI 3모드 스모크(합성 npz 24파일 → train →
propagate → rank) 클라우드 검증 완료 (bank-회귀 state0 로 delivered 78.3% vs 진실 80.8%;
rank R=20/35/50 → delivered 86/80/74% 저-R 선두).

## 8. v2 로드맵 (v1 코드에 훅 자리만)

1. **step4_dyn 라이브 훅**: simulate() 루프 `on_step(state_dict)` 콜백 kwarg(기본 None=바이트
   불변) — 전이 실시간 축적 + surrogate 의 다음 V 예측을 `V_prev` 대신 `_bracket_illinois`
   warm-start 로 공급(진단1[3-b]: ev 횟수↓ = 스텝비용 직접 절감, 해 불변·저위험 1차 배선).
   2차 skip 모드 — surrogate M스텝 전진 후 실솔버 앵커, |V_sur−V_anchor|>gate 면 **앵커로
   롤백**+해당 구간 재학습(MLIP on-the-fly).  롤백 구현 전 skip 모드 금지.
2. **부분수렴 앵커 수용**: deep_weak 조기종료 상태(resid 정직 보고)를 밴드가 덮으면 앵커
   수용 — resid·밴드 동시 로그(침묵 금지).  nnAMG 깊은 솔브의 정당 필요는 잔존(§0).
3. torch/GPU 학습(대코퍼스)·온라인 재학습 버퍼 소비·ml_cycle_surrogate 타깃 배선(step6
   per-cycle 지표 → R_int(N) 학습행)·충전(charge) 전개·r0/r_ct/r_film 상태의 Δ 학습·
   SkCommittee 저장(joblib)·밴드 캘리브레이션(실 STEP4 대조 후 계수화).

## 9. selftest 전문 (2026-07-27, 클라우드 numpy-only, 결정론 확인 — 동일 해시 2회)

```
SURROGATE/UNCALIBRATED — 전개값은 STEP4-모델 상속 예측; 절대 신뢰는 앵커(실솔버) 상태만 (§F1)
=== step6_surrogate selftest (합성 RC-방전 ODE — TEST-ONLY §F1) ===
① 추출기: CC 2466 + CV 303 전이쌍, phase 경계 6쌍 제외, 쿨롱 검산 통과(제외 0)  OK
  ⚠ 전-결측 feature 1개 → median=0 impute(무정보): ['bv_face_per_cm2']
  ⚠ 전-결측 feature 1개 → median=0 impute(무정보): ['bv_face_per_cm2']
② 위원회: LOCO R²(d_v)=0.9854 (>0.9), d_x_surf_p50=0.9876 · random-split=0.9892=계산만(보고 금지 규율)  OK
③ 전개(held-out): 97스텝, |V_err| 중앙 6.08 mV, 밴드 커버리지 member 80% (≥68) vs rss 31% (독립가정 과소 실증) · delivered sur 0.800 vs 진실 0.808 · 종료 V_cutoff(p>0.5)  OK
④ σ_gate: std in-dist 0.574 → OOD 2.254 mV (3.9×) → gate 1.414 mV 발동 · force=False 정지(anchor_needed_stop)  OK
⑤ 앵커: mean|V_err| force 9.68 → anchor 1.80 mV (26회 교체, 버퍼 26쌍) · CLI 어댑터 OK
⑥ rank: R=20/35/50 → score 0.448/0.390/0.343, p_pick=[1.0, 0.0, 0.0] (Σ=1, 저-R 선두) · next-anchor 추천 1건  OK
⑦ §F1 라벨 전 반환 확인 + save/load bitwise 왕복 + 스키마 가드 + 로드-전개 동일  OK
⑧ [cloud] sklearn 부재 → import-guard graceful ✓ (sklearn 부재 (WSL 전용) — RidgeCommitt…)
selftest OK (8/8)
```

해석 메모: ③ |V_err| 중앙 6 mV = 자기회귀 드리프트(스텝당 ~0.06 mV 편향 누적) — 위원회
평균의 한계이며 member 밴드가 이를 80% 덮음(정합).  ④ OOD 팽창 3.9× 는 다축(R×5+τ×8)
기준 — 단축 OOD 는 위원회 민감도가 축에 따라 다름(계수-무관 축은 팽창 약함) → 실전 gate 는
in-dist std 측정 후 상대 설정 권장.  ⑥ p_pick 이 1/0/0 으로 결정적인 건 후보 간 점수차가
draw 노이즈보다 크기 때문(동률·근접 후보에선 분산됨).

## 10. 규약 준수 체크리스트

- [x] sklearn/torch 하드 의존 금지 — import-guard, numpy-only 폴백이 기본 동작
- [x] selftest 합성 ODE 로 클라우드 실제 PASS (`python3 scripts/step6_surrogate.py --selftest`)
- [x] §F1: 모든 반환 dict/CLI 배너에 SURROGATE/UNCALIBRATED 라벨, 날조 앵커 0
      (결측=nan, x0/x100 미지정 시 명시 에러, state0-보간·Thompson-근사·다운웨이트 전부
      ASSUMED/UNCALIBRATED 라벨)
- [x] ml_cycle_surrogate / ml_design_loop / eis_drt_ica / cycling_data_ingest 규약 재사용 명시
- [x] LOCO(런 단위) 보고 — random-split 보고 금지
- [x] 모델명 없음 · 한국어 압축 주석 · git 커밋은 메인 세션
