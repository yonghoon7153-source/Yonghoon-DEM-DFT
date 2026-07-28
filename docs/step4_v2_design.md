# STEP4-v2 설계 — 시간적분 + 구형확산 + 비선형 BV (voxel-DFN, SSB) (2026-07-15 구현 현행판)

v1(저율 선형 BV·균일 SOC·RELATIVE 스냅샷, `step3_sigma.solve_reaction_current`) → v2 =
갈바노스타틱/CV **시간 전개**.  같은 복셀 미세구조 위에서 방전을 실제로 굴린다.
**구현 = `scripts/step4_dyn.py`** (2026-07-15, selftest 20/20, 물리·수치 2-agent 리뷰 반영,
커밋 448c8b1→388b2aa).  이 문서는 코드 기준으로 현행화됨 — 세부는 모듈 docstring이 우선.

## 0. 산출물 (왜 하는가)

- **V(t) 방전곡선** (half-cell vs Li counter), C-rate sweep → **capacity@cutoff vs rate**
- **입자별 SOC(t)** → 활용 불균일의 시간 전개 (v1 hot-spot 스냅샷의 동역학판)
- **분극 분해**: ohmic(전자/이온) vs kinetic(BV) vs diffusion(구형) — 시점별
- **SBE vs DBE 같은-침대 rate 비교** = SDCP의 rate-capability 가치 정량 (manuscript 다음 축;
  σ_SDCP 4점 곡선과 접합 — 브리지가 고율에서 언제 결정적이 되는가)
- **CV/CCCV 곡선** (`--cv-hold`: V-리밋 도달 후 전압 홀드, 충·방 양방향) · **발열 분해 [W]**
  (Q_ohm e/i 분리 · Q_ct · Q_film · Q_rint + Q_rev(dU/dT 훅)) · **에너지 수지 감사**(매 스텝
  기계정밀도 — P_ohm+ΣIη+ΣI²ASR/A+ΣIU+I·V=0; 오독 방지 축)

## 1. 물리 (SSB-특화 단순화 2개는 근사가 아니라 물리)

- **SE = 단일이온 전도체(t⁺≈1)** → 전해질 농도분극·염 확산 없음 → 이온망은 시종 옴익.
  액체 DFN 대비 "생략"이 아니라 황화물 SSB의 **정확한** 거동.
- **전위 준정적**: 전기장 이완시간 ≪ 확산시간 → 각 시점 (φ_e, φ_i) 정상상태 결합해.
- **입자 내부**: c_s(r,t) 구형 1D Fick — ∂c/∂t = D_s·(1/r²)∂/∂r(r²∂c/∂r).
  BC: 표면 flux = (그 입자의 BV 면전류 합)/(표면적), 중심 대칭.  입자별 독립(1271개).
- **BV 면** (v1과 같은 rasterized AM|ion 면): i = i0(c_surf)·[e^{0.5Fη/RT} − e^{−0.5Fη/RT}],
  η = φ_e − φ_i − U_ocp(c_surf).  SDCP는 v1처럼 자기-BV 없음(비인터칼레이션, 배달만).
- **갈바노스타틱**: I_tot = C-rate × (AM 질량 × 비용량) 고정.
  V(t) = φ_e(집전체) − φ_i(분리막) 기준 — Li counter/anode 과전압은 범위 밖 명시(half-cell).

## 2. 수치

- 시간 루프(adaptive Δt): 스텝마다 **Newton** on (φ_e, φ_i) — 면별 g_ct = ∂i/∂η만 갱신하면
  v1의 결합 SPD 조립을 그대로 재사용, CG(CuPy)는 이전 해 warm-start (스텝간 Δ 작음 → 수 iter).
- 구형확산: 입자별 tridiagonal **Crank–Nicolson**, (1271 입자)×(Nr≈20 셸) 벡터화 — 비용 무시급.
- 격자: 동역학 1차는 **vox 0.8µm**(dof ~1/8)로 개발/스윕, 결론 런만 0.4 확인.
- 성능 추정: ~50 steps × 2-3 Newton × warm CG ≈ V100에서 케이스당 십분~시간 단위 — 실행 가능.
- 저율 극한 회귀: C→0에서 v2 첫 스텝 ≡ v1 (선형화 일치) = 필수 selftest.

## 3. §F1 입력 3개 (앵커 — 사용자 확인 후 확정)

| 입력 | 계획 | 상태 |
|---|---|---|
| U_ocp(SOC)·c_max·stoich창 NMC811 | pybamm 내장 Chen2020에서 기계 export (provenance 명시, 날조 0) — `step4_pybamm_anchor.py --export-params` (양극 y 위치기반 추출 + sanity assert) | ✅ 승인(2026-07-15 "다 gpu로 진행하자") · export 구현 |
| D_s (NCM811) | 문헌 범위 1e-14–1e-13 m²/s → `--d-s` 입력 노출(기본 3e-14 = Kang&Shin FEM 값 인용) | ✅ 승인 · 구현 |
| i0 | v1 훅 유지(2 A/m², ⚠F1) + `--i0` 스윕; i0(x) 농도의존 명시형 | ✅ 유지 · 구현 |
| dU/dT(x) (엔트로피) | `--dudt-csv` 있을 때만 Q_rev 출력 (없으면 NaN — 날조 없음) | 훅 구현 (데이터 대기) |

## 4. pybamm 앵커 (frame[4] — 독립 참조와 대조, cross-fit 금지)

- **균질 트윈**: pybamm DFN(/SPMe)에 우리 STEP3 산출 σ_e_eff·σ_ion_eff·ε·두께 + 동일
  OCP/D_s/i0/대표입경 입력 → V(t)·분극 대조.
- 프로토콜: (a) **균일-구조 극한**(합성 uniform 침대)에서 voxel-v2 ≈ pybamm 수 % 이내 = 솔버
  검증; (b) 실제 침대의 편차 = **미세구조 효과의 정량**(이게 부가가치 — 균질모델이 못 보는 것).
- 실행 위치: pybamm은 WSL/V100 (cloud 컨테이너 미설치).

## 5. 구현 순서 (각 단계 selftest + 물리 2-agent 리뷰) — 진행 현황 2026-07-15

1. ✅ 구형확산 코어 (질량보존 2.7e-12 · 평형 유지 1.6e-15 · √t 2.9% — √t가 계수버그 실검출)
2. ✅ 비선형 BV Newton (CSR 위치맵 brute-force 대조 1e-16 · 평형 V=OCV 7e-14 · 저율 직렬-R
   1e-4 · v1 회귀 2.2e-5 · 에너지 수지 2e-12 · ASR/비대칭α/CV 해석해)
3. ✅ 갈바노/CCCV 시간 루프 + 출력 (쿨롱 적산 9e-9 · 전스텝 KCL/E-bal 감사 · R_int · SOC-창
   클램프 · V-컷오프 보간)
4. 🔶 pybamm 앵커: export 구현(리뷰 blocker#2 수정 — 양극 stoich 위치기반) · compare =
   EXPERIMENTAL(첫 V100 스모크에서 파라미터명 다듬기).  pybamm은 V100/WSL에만 있음.
5. ⛔ V100 스모크(진행): DBE payload `--save-step4-grid` → 0.5C 기계 스모크 → 0.1C/0.5C/1C
   본 곡선 → SBE 재압밀 rate 비교 셋.
리뷰 기록: 물리 리뷰 blocker 2(AM 반경 box단위, stoich 혼합) + 수치 리뷰(가드-BV 유령접지,
CSR 순열방향, 성능 판정 "곡선당 ~1-1.5h V100") — 전부 반영 커밋 388b2aa.

## 6. 범위 밖 (정직 선언)

열 **커플** 없음(등온 T 파라미터; 발열 Q_*는 출력 전용) · 부피변화/열화 커플 없음(A10) ·
anode 없음(half-cell; pybamm 트윈은 Li-counter 분극 제거로 정합) · SE 농도분극 없음(단일이온
t⁺≈1 — 물리적으로 부재) · 이중층 C_dl 없음(시간상수 ms ≪ 방전 dt; COMSOL도 방전 sim 통상
off) · D_s(c) 농도의존 없음(Chen2020 양극도 상수) · 입자균열 진행 없음(Auerbach는 압밀
스냅샷) · 입자 표면 SOC는 입자당 1D(면별 국소 SOC 없음 — 부분피복은 전면적 균질화).
v2는 **transport→kinetics→diffusion** 3층까지.

## 7. v2 chaining — 연속 사이클 (2026-07-28)

스케줄(--step4-sched)의 v1 실행은 각 스텝 독립 초기상태(= 모든 Rest 가 사실상 ∞ 극한, Loop
반복 = 동일 복제)였다.  v2 chaining 은 **셸-SOC 상태 rad.x [n_am, nr] 를 런 사이로 전달**해
스케줄을 진짜 연속 사이클로 실행한다.

- CLI: `--save-state s.npz`(런 끝 저장; newton_fail 도 저장하되 로더가 거부) /
  `--init-state s.npz`(같은 베드·같은 --nr·같은 c_max 강제, 입자반경 allclose 대조,
  newton_fail 상태 거부 — 강제 MPM_S4_CHAIN_FORCE=1) / `--rest --t-rest-min M`(Rest 실물리).
- 상태 = 농도장뿐.  rad.J 리셋(런 전환 = 전류 불연속 — 새 프로토콜의 첫 솔브가 새 J 결정),
  φ 재초기화(U0 = U(x̄_loaded) 균일; Newton 2-3회 수렴).  체인 시작 시 노이즈바닥 자가교정은
  **균일-x̄ 참조평형**으로 잰다 (로드 필드는 비평형 → 진짜 BV 전류가 잔차에 실려 바닥이
  과대교정되고 경고선·목표가 물러지는 것 방지).
- Rest = **REST-LOCAL v2.0**: 입자별 zero-flux CN 확산 완화 (질량 정확 보존 — drift 검산 출력).
  입자간 전하 재분배(I_tot=0 망솔브 = 혼합전위 평활)는 미모델 — **v2.1 훅**.  mono-물성
  베드에선 입자 상태가 근사 동일해 재분배 ≈ 0.  V 트레이스 = 용량가중 평균 OCP(x_surf)
  (I=0 표식용 근사, meta 에 명기 §F1).
- 부기: x_ini = 로드 필드의 부피가중 x̄ → delivered % 는 "전체 창 대비, 실제 시작 기준".
  run npz 에 x_shell_final [n_am,nr] 상시 포함(감사 + 수동 체인).  meta.chain =
  {init_state, prev_end, save_state}; viz JSON 에 x_init/chained.
- 킷(`--step4-chain`, 스케줄 전용, 기본 OFF = v1 방출 **bitwise 불변** 검증): 스텝별
  s4state_XXnY.npz 체인, Rest 는 실제 --rest 런, 실패 스텝 뒤는 존재가드 SKIP(침묵
  평형-재시작 오염 금지 — step4_only.sh 로 재개).  **Loop 경계를 넘어 상태 누적** →
  cyc2 는 cyc1 끝에서 시작 = 진짜 반복 사이클.
- webapp: 스케줄 옆 "⛓ 연속 사이클(v2)" 체크(기본 ON) → &s4chain=1 → zip `_chain` 태그.
  (같이 정정: 클라이언트 _addTag 의 _ppds/_cap 순서가 서버와 어긋나던 기존 버그 —
  cap+ppds 동시 킷의 자동 등록훅 예측명 불일치 원인 — 서버 순서 _sched[_chain]_cap_ppds 로 미러.)
- 문법 확장: 방전 스텝에 i → 방전-CCCV(CV@v_min, |I|<i·1C 종지) · 스텝에 t(분) → --t-max
  (GITT 펄스열 구성 가능해짐: 짧은 펄스 + rest 반복 — chaining 이 전제).
- 검증: selftest chain(1-4)=rest 보존·평탄화 / save-load bitwise+가드 3종 / simulate 연속성 /
  x_field=None bitwise · CLI e2e(충전 19.8% 전달 → rest ΔV_ocp −21 mV·surf-mean gap
  0.031→0.009·drift 9e-16 → 방전이 충전끝 x̄ 0.731 에서 시작) · 킷 chain-OFF = 구세대
  byte-identical · chain-ON bash -n · env_db selftest.
- v1 독립런의 자리(폐기 아님): rate-capability 스크리닝(각 율 완전이완 시작 규약)은 여전히
  v1 이 정본 — chaining 은 연속 사이클/프로토콜 충실 재현용.  비교 시 실행규약(_chain 태그)
  병기 필수.  잔여 훅: v2.1 rest 입자간 재분배(I_tot=0 망솔브) · 조건-루프(용량<X% until —
  in-run 열화 모델 필요) · B-1 per-cycle 자동배선(N→배수 법칙 앵커 대기).

### §7-리뷰 반영 (2026-07-28, 3렌즈 적대 리뷰 — 코드/전기화학/수치물리 에이전트)
- **[MED·수정] V_cutoff 상태-부기 정합**: 저장 체인 상태를 컷오프 보간 교차점으로 롤백 — 매
  V_cutoff 사이클마다 다음 충전이 보고 q 보다 마지막-dt 만큼 깊게 시작하던 dt-의존 전량장부
  오프셋(dx_max=0.02 서 창의 ~0.3-1%/사이클) 제거.  selftest chain(5): 상태 q ≡ 보고 q (Δ=0.0).
- **[MED·수정] 로더 가드 통일(세탁 봉쇄)**: isfinite(NaN 은 min/max 비교 침묵통과) + 솔버밴드
  [-0.01, 1.01] 범위 + `soc_overrun` 종료 거부 — rest 경로가 오염 상태를 클립-세탁해 'rest_end'
  로 재발급하던 구멍 폐쇄.  rest 는 클립-포함 총드리프트 감사 + NaN-안전 부정형 경고.
- **[MED·수정] simulate x_field 수용밴드**를 솔버 자체밴드로 확장 — 정상 종료한 심방전 상태
  (셸 x∈(1,1.01] 합법)를 "손상"으로 오인 거부하던 비대칭 제거 + 클립 이동 감사 출력.
- **[MED·수정] J(표면유속) 상태 탑재** — 표면농도 연속성: 체인 첫 U_f 재구성과 rest t=0 점에만
  사용(첫 전진에서 새 J 로 대체).  미탑재시 한 점이 OCP 쪽으로 U′·Δx_surf 편향 (D_s=4e-15 poly
  에서 수십 mV; GITT 순간강하 과대).  e2e 재실측: rest ΔV_ocp −21.5→−27.6 mV (첫 점 정확화).
- **[MED·수정] rest V-트레이스 가중**: 부피(R³)→ **i0(x_surf)·R² 혼합전위 선형화** (부피가중은
  Σi0·A·sinh=0 의 해가 아니라 바이모달·i0-분리서 수십 mV 편향) + **dead 입자 상태 탑재·제외**.
- **[MED·수정] 킷 체인블록 시작 `rm -f s4state_*.npz`** — step4_only.sh 재실행 시 이전 시도
  잔재가 SKIP 가드를 무력화하고 env-override 바뀐 설정을 침묵 혼합하던 구멍 폐쇄.
- **[수정]** Rannacher 스타트업(BE 반스텝×2, θ-스킴 일반화 — CN 기본 bitwise) = 급경사 초기장
  CN 링잉 제거 · newton_fail exit 3 (킷 FAILED 로그 한-스텝 지연 제거) · 체크포인트 세그먼트
  페이싱(부분 세그먼트 viz 희소화 해소) · dx_mean_signed/q_frac_segment 병기(전체-창 q 와 혼동
  방지) · chain 가드 파싱직후 이동 + prov step4_chain 정확화(grid-only=false) · rest t≤7일 ·
  webapp: **s4cap 단독 선택 다운로드 500(기존버그)** / grid-only 태그 미러(기존) / 명령카드
  스케줄·체인 표시+STEP4 fetch 라인(기존) / **_addTag _cap·_ppds 순서(기존버그 — cap+ppds 킷
  자동등록 예측명 불일치)**.
- **[검증 확인]** 체인 첫 Newton 강건(U_f 스프레드 446 mV 도 2 it, 프레시런과 동일) · 질량장부
  float64 정합(충→rest→방 체인 총오차 정확 0) · 균일-참조 노이즈바닥 = 필수이자 정확(로드-필드
  참조는 9.4e5× 부풂=가비지 수용) · 로드 클립 실무 불활성(현행 창서 headroom 0.15+) · v1
  bitwise 불변 3중 재확인(selftest chain4 + 킷 구세대 byte-diff + 전기화학 렌즈).
- **[잔여 훅 확정]** v2.1 rest I_tot=0 망솔브 — bimodal D_s/i0 분리 베드를 rest 로 체인할 때
  1차항(2.5C 충전끝 U_f 스프레드 157 mV 실측) → 그 조합 사용 전 우선 구현 대상.
