# τ (굴곡도) 정의 닫기 — 판단 메모 v2 (2026-10-03 · 적대 리뷰 셋 반영)

- **무엇이 바뀌었나**: v1 (`docs/reviews/tau_conventions_judgment_v1_20261003.md`, 그대로 둠) 을 리뷰 셋으로 고쳤다.
  - 코드 리뷰 `tau_review_code_20261003.md` — 49 행: 확인 37 · 부분 10 · 틀림 1 · 검증 불가 1, 그리고 놓친 결함 M1–M9.
  - 문헌 리뷰 `tau_review_lit_20261003.md` — 54 주장: 일치 41 · 부분 10 · 틀림 3.  틀림 셋은 전부 COMSOL 쪽 번호다.
  - 물리 리뷰 `tau_review_physics_20261003.md` — 32 행: 타당 9 · 조건부 17 · 틀림 5 · 검증 불가 1.  계산은 `tau_review_phys_calc.py` (v2 작성 중 재실행 — 수치 일치).
  - 부분 · 틀림 · 조건부 · 검증 불가 행은 전부 본문을 고쳤다.  고친 자리는 §R 원장에 있다.
- **근거**: τ 목록 (`tau_inventory_20261003.md`, 27 변형 · 불일치 I-01~I-22) · litdb 정본 카드 7 편 + `comparison_vs_ours_DEM.md` §J · COMSOL 5.6 Battery Design Module User's Guide (`comsol/BDM_UG.txt`) · 리포 `claude/stoic-knuth-NObVQ` HEAD `1afd37a9a` (**읽기만**, 쓰기 0).
  - COMSOL 쪽은 **인쇄 머리말 쪽**이다.  v1 은 `\f` 로 자른 0-기준 색인을 쪽으로 써서 전부 1 작았다.  책 자신의 색인 ("tortuosity factors 450") 으로도 확인했다.
  - v2 가 새로 계산한 수는 §3-3 의 띠별 φ_mc/φ_구합 하나뿐이다 (커밋 `docs/data/case_master.csv` 읽기 · 쌍 렌즈 union).
- **비준된 전제 — 다시 열지 않음**: D1 열 셋 f = σ_eff/σ₀ · T = φ/f · τ = √T (키 `tau2` 권고) · D2 면적 모드 Hertz · physics 둘 다 + 무거운 게이트 · D3 φ = 질량 보존 φ · D4 이온 → 전자 → 열 · LHS-25 · LHS-26 은 LHS (130 + 64) · ps45 재계산 **전에** 닫는다.
- **표기**: (유도) = case_master n = 157 (25 °C) 로 소비처 식을 다시 계산 · (우리 산술) = 원문 · 코드 수치로 계산한 것 (측정 아님) · [미확인] = 근거 없음 · 리뷰 꼬리표 = 코드 #n · 코드 Mn · 문헌 Xn · 물리 xn (해당 리뷰의 행) · `TAU-xx` · `CL-94` = 원장 미등재 제안 · **1세대** = S3 판정 전의 협착식 (v1 의 "세대 1" 과 같은 뜻).
- `claims.json` `quotation_ban` 37 패턴과 겹치는 문자열이 없음을 작성 뒤 대조했다.

---

## §0. 결론 → 1저자 결정 → P1 결함

### 0-1. 결론

| # | 결론 | 절 |
|---|---|---|
| ① | 우리 **T = φ·σ₀/σ_eff** (= 웹앱 τ_Lap,eff²) 는 문헌 τ 양과 **같은 정의식**이다 (전체 단면 · 관통 방향 · 전 SE 부피 정규화).  원문 이름은 서로 다르다: Tjaden "tortuosity factor" κ = τ² · Landesfeind "effective tortuosity" τ (Eq 5 — 전극 측정 Eq 13 은 Nguyen 이 τ_e 계열 eSCM 으로 분류) · Nguyen "tortuosity factor" τ (conventional) · Park "tortuosity" τ_e · Minnmann "tortuosity factor" τ² · TauFactor "Tortuosity Factor" τ · COMSOL "fluid tortuosity factor" τ_F.  **물리 기준 상태는 다르다**: 우리 T 는 간선 재료 σ₀ (펠릿값, `CL-91`) 위에 SE–SE Holm 을 직렬로 더하고, 원기둥 bulk · 반공간 협착식 · 띠 끝 단락을 거친 **접촉망 모델 T** 다 (물리 a1 · 문헌 A0) | §1 · §3 |
| ② | 리포의 "COMSOL/EIS input" 은 **√T** 에 붙어 있다.  COMSOL 종 수송 인터페이스의 Eq 6-6 f_e = ε_p/τ_F (p.376) 에서 τ_F 는 T 꼴이다.  √T 를 그 칸에 넣으면 σ_eff 가 √T 배 (코퍼스 중앙 2.5×, physics 3.2× — 유도) 과대다.  배터리 인터페이스 (Porous Electrode, p.266–267) 는 식을 인쇄하지 않는다 → **강하게 시사 (strongly implied) — 인쇄 근거 없음**.  보강 문장 (4 장 Porous Electrode 노드, p.144 · p.156) 은 Bruggeman · Tortuosity 선택지에서 전극 부피분율이 유효 전도도 계산에 **쓰인다**는 것만 말한다 — 물리 리뷰의 읽기로 σ/τ 꼴은 배제되고 ε/τ ↔ ε/τ² 는 미결이다.  T 가 σ_full 을 재현하려면 **COMSOL σ₀ 칸 = 우리 3.0** 이어야 한다.  √T 를 τ_F 칸에 **배선하는 코드는 없다** — 틀린 것은 라벨 · 내보내기 표기 · README 검산식 · 커밋 열 사전 TSV 6 개 (이미 전달된 배포 v1 · v1.1 포함) 다 (코드 #5 · #6 · 물리 c1) | §1 · TAU-01 |
| ③ | Minnmann 대조에 **"일치" 는 없다** (v1 "SE 많은 쪽 정합 범위" 철회).  우리 T(φ_SE) 곡선은 Minnmann 곡선을 φ_SE 로 **≈ 0.06–0.09 왼쪽으로 옮긴 꼴**이다.  SE 쪽은 곡선이 평평해 그 어긋남이 세로로 보이지 않았을 뿐이다.  일치처럼 보이던 띠 중 위 두 띠 (φ_SE 0.61 · 0.54) 는 **과압축 침대**다 (ε_sphere 2.95–6.6 % · SE/고체 0.59–0.61).  기준 상태를 Minnmann 관례 (순수 SE 펠릿 = 1) 로 맞추면 우리 T 는 **× 0.5–0.7** 로 내려간다 — 코퍼스 외삽 **T_pure,ours ≈ 1.4–2.0** (hertz) 기준.  ⇒ **순수 SE 런 = 모든 절대 대조의 게이트** (물리 a3 · b3) | §3-2 · §3-3 |
| ④ | SE 적은 쪽 "3–10 배 낮음" 은 **모델 오차 배수가 아니다**.  입경비 (우리 r_SE/r_AM 중앙 ≈ 0.13 ↔ Minnmann ≳ 1) 와 퍼콜 문턱까지의 거리차가 지배하는 **다른 미세구조의 비교**다.  바인더 · CBD 후보는 Minnmann 에 해당하지 않는다 (전도도 시료 = 건식 NCM + LPSCl).  **springback** (380 MPa 압밀 → ≈ 40 MPa 측정) 이 후보에서 빠져 있었다 (물리 b4) | §3-8 |
| ⑤ | **Hertz T 도 1세대** 협착식이다.  반공간 Maxwell R_c = 1/(2σa) 는 평균 a/r_SE 0.30–0.44 에서 리포 자신의 flux-tube 기준해 (곱 배치 ψ) 대비 R_c 를 **1.7–2.4 배** 과대하게 둔다.  곱 배치로 바꾸면 T_H 가 직렬 근사로 ≈ 30–40 % 내려가고, 그 과대는 SE 많은 쪽에서 가장 크다.  physics T 는 다른 결함을 가진다 — ψ 분모 (`L2-01`) + 접촉별 면적이 상한값 (`LHS-25`) + ψ 절벽 (물리 a4 · b8) | §3 · §5 · TAU-13 |
| ⑥ | CF 가지의 T < 1 (26/157) 은 **원기둥 bulk 모델의 성질**이지 솔버 이상이 아니다 → SOLVER_ANOMALY 표지를 쓰지 않는다.  FULL 도 같은 bulk 를 쓰므로 τ_FULL/τ_CF "협착 배수" 는 **T 로 ≈ 1.2–1.4 배 (√ 로 1.1–1.2 배) 과대**다.  L0 띠 끝 단락은 T 를 **최대 ≈ 4r_SE/L 만큼 낮춘다** — 코퍼스 중앙 6 % · p90 12 % · 최대 17 % (상한 추정).  L1 폴백은 곧은 사슬에서 21–29 % 로 더 크다 (물리 f1–f4 · 코드 M5 · #27) | §3-6 |
| ⑦ | LHS-25 의 뿌리는 합보다 앞에 있다.  **접촉별 추정량 F_real/H 가 느슨한 상한값**을 그대로 돌려준다 (부피 보존 소성 면적의 ≈ 1.5–3 배).  v1 의 κ ≈ 15–30 · 포화 문턱 30–60 MPa · "0.1–0.2 × 원판" 은 **철회**한다 — 생산 DEM 은 hooke/hysteresis 이고, 힘 평형상 κ ≈ 2–9 다.  Arzt 는 안 B (라게르 면 상한) 의 근거이지 안 A 의 근거가 아니다 (물리 e2–e6 · 문헌 C3 · C5) | §6 |
| ⑧ | "τ_e 공백이 인계를 막지 않는다" 는 **ML 기술자 문장으로만** 선다.  P2D/COMSOL 입력으로는 부호 불정이다.  위상 dead-end p90 = **2.86 %** 이고, flux dead-end 는 기존 FULL 장으로 셀 수 있다 (물리 d1) | §7 |

### 0-2. 1저자가 정할 것 — 권고 · 이유

> ✅ **비준 10-03 (1저자 · 서브 세션)** — 아래 권고대로.  단 결정 3 은 서브 세션 설명 판 **"hertz 먼저 · physics 는 LHS-25 뒤"** (coverage 인계 J20-m 과 같은 c_cpl[22] 면적) · 결정 4 = 기존 순수 SE 4 침대로 망만 (새 DEM 없음) · 결정 9 = 절차만 (c² 두 끝 1.27 · 1.40 · 라게르 구현 범위 별도).  실행은 추가 문헌 10 편 (§8-1) 흡수 · 인사이트 보고 뒤 — 기록 `docs/session_20260923_progress.md` (10-03).

| # | 정할 것 | 권고 | 이유 (절 · 리뷰) |
|---|---|---|---|
| 1 | f 의 정규화 상자 (D3 의 짝) | **(ii)** f_mc = f_gap·L_gap/L_mc · T = φ_mc/f_mc.  이름표 "판 간격 해의 질량보존 두께 재척도 (해 아님)".  풀린 f_gap 은 메타 열로 두고 φ_mc 와 짝짓지 않는다 | T 가 현행 솔버 T 와 **정의상** 같은 수다 (부피 보존 z-신장 자기상사 가정).  (i) φ_mc ÷ f_gap 은 T 를 L_gap/L_mc 배 낮춘다 (LHS 0.898–0.985 · lhsx 0.867–0.931) → 금지.  (iii) 은 표의 φ (D3) 로 T 를 재현할 수 없다 (§3-7 · 물리 g3) |
| 2 | 비관통 규칙 | **f = 0 + `NOT_PERCOLATING`**.  판정은 `percolating_fraction == 0` ∧ `calc_percolation` `percolation_pct == 0` (같은 L0 띠) 로 한다 — `sigma_full_status` 로는 판정하지 않는다.  T · τ 는 빈칸 (= ∞).  한정어 "문턱 근처의 관통 여부는 상자 크기의 실현값 — 재료 성질 아님" | conventional τ = ∞ (Nguyen p5).  비관통이면 솔버가 (None, None) 을 돌려 상태가 'not_computed' 가 된다 — 'valid_zero' 는 도달 불가 (코드 M2 · 물리 h1 · §5-2 G2 · G3) |
| 3 | 두 면적 모드의 게이트 (D2) | hertz · physics **둘 다** 싣는다.  둘 다 협착식 1세대 메타를 단다 (`ion_net_constriction` = `maxwell_halfspace` / `mikic_psi_divide`).  둘 다 **"ML 기술자 전용 · 실험 절대 대조 HOLD"**.  ⛔ 실험에 더 가깝다는 이유로 모드를 고르지 않는다 | 두 모드 모두 1세대이고 결함 방향이 반대다 (hertz 는 R_c 과대 · physics 는 ψ 분모 + 상한값 면적 + 절벽).  어느 쪽도 물리 개선판이 아니다 (§3-8 · 물리 a4 · b7 · b8) |
| 4 | 순수 SE 게이트 런 | 순수 SE 침대 망 1 회 (hertz · physics · CF 세 가지) 를 **모든 절대 T 대조의 선행조건으로 등록**한다.  결과는 원 T 와 정규화 T (÷ T_pure,ours) 를 **둘 다** 보고하고, 정규화 뒤 대조의 판정선은 런 전에 등록한다.  그 전에는 "일치 · 정합 · 검증" 낱말을 쓰지 않는다.  기존 순수 SE 덤프 유무 [미확인] — 없으면 DEM 1 런 | 외삽 T_pure,ours ≈ 1.4–2.0 (hertz) → × 0.5–0.7.  이 방향이 결론을 바꾼다: SE 많은 쪽 "정합" 이 사라지고 SE 적은 쪽 격차는 커진다.  정규화는 Minnmann 의 정의 (순수 펠릿 τ² ≡ 1) 를 맞추는 것이지 값을 맞추는 것이 아니다 (§3-2 · 물리 a3) |
| 5 | "COMSOL/EIS input" 정정 · 전달된 배포 | √T 행 · 열에서 COMSOL · EIS 낱말을 **지금** 뺀다.  T 행 · T 내보내기 열을 새로 둔다 (숫자 불변).  T 에 "COMSOL 입력" 표지는 사용 버전 **GUI Equation 보기 캡처 뒤**에 단다.  σ₀ 짝을 명기한다.  전달본 v1 · v1.1 은 **정오표를 즉시** 낸다 (열 사전 한 문장, 값 불변).  v1.2 (f/T/τ 를 실을 때) 에서 열 사전을 교체한다 | 전달된 문구가 √T 를 COMSOL 에 넣으라고 읽힌다 (√T 배 과대).  값이 안 바뀌므로 수치 재발행은 필요 없다.  배터리 인터페이스는 인쇄 근거가 없다 (§1 · TAU-01 · 코드 #6 · 물리 c1) |
| 6 | 등급 · COMSOL 2D 의 τ 축 | 한 도우미 (모드 명시) 로 통일한다.  Stage-E σ 로 만든 값에서 "τ" 이름을 뗀다.  문턱 (√ 척도 1.8–6.0) 에는 **"내부 등급선"** 표지를 단다 (Famprikis 카드에 없음 · Tippens 2019 [미확인]).  T 축으로 옮기면 문턱을 제곱한다 | 등급 / 웹앱 H 0.852–1.584 편차의 주원인은 **모드 불일치 (156/157)** 다.  재료 인자 (Cronau · 파괴) 차는 1/157 (particulate_1) 뿐이다 (TAU-03 · 코드 #10 · 물리 a5) |
| 7 | 프레임 [1] "pure-SE ≈ 10 % @ 300 MPa (Minnmann)" | **`CL-94` (제안) 등재 + 한 커밋 정정**.  문안: "Minnmann 2021 본문 · SI 에 순수 SE 기공값도 300 MPa 도 없다 (380 MPa 복합 양극 기공 7.6–17 %, 평균 14 % 만 있다).  카드 계보상 우리 MPM 보정 수렴값이다 (순환 앵커 의심 — Sakuda 2013 은 다른 재료의 유리, Minnmann 2024 는 복합 기공으로 다른 양)".  MPM σ_y 0.30 에 "외부 앵커 없음" 표지.  정정 뒤 정확한 문자열을 `quotation_ban` 에 올린다 | frame[4] "각 모델을 실험에 독립 보정" 이 이 매개변수에서는 성립하지 않는다 (TAU-10 · 문헌 B1 · B2 · 물리 h2) |
| 8 | `single.html:1847` "1.4 % 일치 — parameter-free external validation" | **수치 없이 철회**.  대체 문장: "단일 케이스 대조는 기준 상태 보정 (결정 4) 전에는 판정 불가" | 한 점 일치를 다른 한 점 일치 (v1 의 "T 4.41 vs 4.27") 로 바꾸지 않는다.  같은 φ 띠에서 T_H 2.36–4.87 이고, hertz 협착식 과대와 기준 상태 미보정이 겹쳐 있다 (TAU-02 · 물리 g4) |
| 9 | LHS-25 처방 — **사전등록 결정** | ① 접촉별 추정량을 **역학 전제로 C0/C1 전에 등록**한다.  E2 = 부피 보존 c²·A_overlap (전제: DEM 겹침이 소성 변형의 대리 · c² 는 Arzt 압밀 한계 1.27–1.40 또는 Storåkers ≈ 1.4 에서 런 전에 고정).  E3 = F_DEM/H (전제: DEM 힘이 평형 하중 · 면적 하한).  **둘 다** 계산한다.  F_real/H (현행) 는 "physics (상한값)" 표지로만 둔다.  결론은 E2 · E3 가 같은 쪽일 때만 쓰고, 갈리면 사유와 함께 1저자가 판정한다.  ② 합 상한은 안 B (라게르 면, Arzt 근거).  안 A 는 강체 AM 난간 (β_AM 1 · 구관 회계) 으로만 쓴다.  β_SE {1.0, 1.10} 은 철회한다 (SE 에 쓰려면 물리 유도 또는 1.0–2.0 감도 사전등록).  ③ 채택 기준은 물리 검사뿐이다 (구성상 ≤ 100 % · `budget_below_lower` · 부피 보존 면적 대비).  C1 은 진단 전용, C2 추세 항목은 보고 전용 | v1 의 "C1 을 보고 F 를 정한다" 는 관측을 재현하는 규약 고르기다.  F_real/H 와 F_DEM/H 는 둘 다 추정치가 아니라 경계다 (§6 · 물리 e2–e6 · g1 · g2) |
| 10 | LHS-26 처방 | 설계 상 (`block`) 에서 모양 인자를 정한다.  반지름 규칙은 덱이 총칭 변수일 때의 진단으로만 쓴다.  rough 는 1.40/1.10 출처가 생기기 전까지 인계 제외를 유지한다 | 반지름 규칙이 mono_AM_P 9 침대를 AM_S 로 부른다 (코드 #39 확인 · §6-8) |
| 11 | CF 가지 · "협착 배수" 의 지위 (CL-81 읽기) | CF 의 이름표를 **"모델 내부 기준선 (부피 비보존 bulk)"** 으로 한다 — 물리적 "이상 접촉 극한" 이 아니다.  FULL/CF 는 "모델 내부 협착 비 (원기둥 bulk 기준)" 로 개명한다.  복셀 ÷ 접촉망 대조 계획에 CF 과전도 (× 1/(0.6–0.8)) 를 **사전등록**한다.  CL-81 의 구조 결론 (복셀 FV 는 Holm 항 0) 은 그대로 둔다 | 연속체는 Wiener f ≤ φ (T ≥ 1) 를 지켜야 하는데 CF 는 26/157 이 어긴다.  협착 비는 T 로 1.2–1.4 배 과대이고, 침대 간 비교에 배위수 Z 가 섞인다 (§3-6 · TAU-07 · TAU-08 · 물리 f1 · f2) |
| 12 | TAU-05 (비관통 유한 τ_Dij 삭제) 의 σ_e 파급 | σ_e Stage 22.5 계수를 **동결**한다.  6 침대의 τ 가 폴백값이었다고 기록한다.  재적합은 TAU-06 (σ_e 의 C(τ) 가 어느 τ 를 쓸지) 결정 뒤 **별도로 등록**한다 | 6 침대 (input_2mAh_real_16 · a9_p00/02/06/08/10) 가 σ_e 22.5 필터를 전부 통과한다 → 비트 불변이 깨지는 것이 확정이다.  재적합을 두 번 하지 않으려는 것이다.  σ_thermal T1 은 이미 빠져 있어 무영향이다 (코드 #34) |
| 13 | τ_e | "인계 비차단" 은 ML 기술자 문장으로만 쓴다.  P2D/COMSOL 입력 열은 보류한다 (한정어 "부호 불정").  먼저 FULL 장 flux dead-end (2 % 문턱) · z 단면별 SE 컨덕턴스 · AM–SE 면적 분포를 진단한다 | 위상 dead-end 는 flux dead-end 의 하한이다.  p90 2.86 % · τ_e = T 는 z 균질도 요구 · sink 가중이 LHS-25 면적에 의존한다 (§7 · 물리 d1) |
| 14 | 전자 · 열 T (D4 다음) | 전자: 단일 σ₀ (σ_AM,input) 기준으로 f · T 를 정의하고 GB 인자를 T 에 흡수한다고 명시한다 — 또는 f 만 싣는다.  열: φ = 전 고체 · k₀ 정의를 정한 뒤 세대 표지를 단다 (`CL-12`) | 전자 σ₀ 가 입자마다 다르다 (`sigma_AM_relative`).  σ_AM 50 = 모델 기준값 (`CL-92`).  열 k_weight 가지 미실행 이력 (§5-4) |
| 15 | 키 이름 · 메타 | `f_ion_<mode>` · `tau2_ion_<mode>` · `tau_ion_<mode>` (mode = `hertz` · `physics`) + 메타 `f_ion_<mode>_gap` · `ion_net_status` · `ion_net_area_mode` · `ion_net_constriction` · `ion_net_psi` · `ion_net_band_rule` · `ion_net_band_frac` · `ion_sigma0_mScm` · `ion_sigma0_T_C` · `phi_basis` · `L_basis` | D1 의 `tau2` (T 는 두께 · 온도, κ 는 열전도와 충돌 — tjaden 카드 권고).  세대 · 띠 · σ₀ 짝을 열 안에서 읽게 한다 (§5-1) |
| 16 | S3 봉인 모듈 | f/T/τ 는 **봉인 밖 새 도우미** (예: `scripts/tau_flux.py`) 에서 계산한다.  봉인 모듈 문구 (docstring 'valid_zero' · "formation factor" · `active_fraction`) 정정은 다음 재봉인에 묶는다 | 봉인은 수정 금지가 아니라 **재봉인 강제**다 (`run_s3_psi.py:243–278`).  09-17 봉인은 이미 어긋나 있다 (plastic_coverage 09-29 3 커밋 · network_conductivity 09-28).  그래도 수치 변경은 S3 기준선을 바꾼다 (§4 머리 · 코드 #25 · #26) |

### 0-3. P1 결함 (전체 표는 §4)

| ID | 결함 | 왜 P1 |
|---|---|---|
| TAU-01 | √T 에 "COMSOL/EIS input" — 웹앱 · 등급 · COMSOL 2D 표기 · README 검산식 (φ 자리 반대) · **커밋 TSV 6 개 (전달본 v1 · v1.1 포함)** | 전달된 산출물이 √T 를 COMSOL 에 넣으라고 읽힌다 → σ_eff √T 배 과대 |
| TAU-02 | `single.html:1847` "1.4 % 일치 — parameter-free external validation" | 한 케이스 · hertz 1세대 · 기준 상태 미보정 값을 외부 검증이라 표시한다 |
| TAU-03 | "τ_Laplace,eff" 한 이름에 최소 다섯 변형 (편차 0.852–1.584, 주원인 = 모드 불일치) | 같은 이름의 수가 소비처마다 다르다 |
| TAU-10 | 프레임 [1] 앵커가 Minnmann 2021 에 없다 (순환 의심) | 정본 파일 (CLAUDE.md) 의 MPM 보정 앵커가 출처 없이 인용된다 |
| TAU-13 | 두 면적 모드 모두 1세대 협착식 (hertz 반공간 · physics ψ 분모 + 상한값 면적 + 절벽) | 게이트 없이 인계하면 물리 타깃으로 오독된다 |

---

## §1. 문헌 명명 대조표 — 양 하나에 한 줄

쪽 표기: COMSOL = 인쇄 쪽 · Minnmann = PDF 쪽 (IOP 표지 = p.1; 논문 자체에는 쪽 번호가 없다) · Park SI = PDF 쪽 · 나머지 = 인쇄 쪽.

| 양 | 우리 기호 · 정의 | Tjaden 2018 (`tjaden2018_…`) | Landesfeind 2016 (`landesfeind2016_…`) | Nguyen 2020 (`nguyen2020_…`) | Minnmann 2021 (`minnmann2021_…`) | Park 2020 (`park2020_…`) | TauFactor (`taufactor_…`) | COMSOL 5.6 BDM UG |
|---|---|---|---|---|---|---|---|---|
| **f** | f = σ_eff/σ₀ (= φ/T) · 솔버 무차원 `sigma_full` (`network_conductivity.py:857` · 1156) | "ε/τ² 'diffusibility' / 'effective relative diffusivity'" (p.47 기호표 · p.49) | 1/N_M (이름 없음, Eq 1 A1373) · ⚠ Eq 7 의 **f = 비례인자** (다른 양) | 1/N_M (Eq 1, p1) | σ_i,eff/σ_i,0 (Eq 4 성분, 이름 없음, PDF p.5) | εσ/τ 의 무차원부 (이름 없음) — 본문이 "Equation S1 and S2 in Figure S9" 로 부르는 식 (그림 안 라벨 [1] · [2], SI p.6) | D_eff/D (TauFactor.m:3490–3496) | **"effective transport factor" f_e = ε_p/τ_F** (Eq 6-6, **p.376**) |
| **T** | T = φ·σ₀/σ_eff · (유도) T_H 중앙 6.21 | **κ = τ² "tortuosity factor"** (Eq 2, p.48) · D_eff = (ε/κ)D_bulk "also valid for ionic and electronic conductivities" (Eq 3) | **τ "effective tortuosity"** N_M = τ/ε (Eq 5, A1374) · Eq 8 (A1375) · "τ in Eq. 5 appears often as τ²" (A1374) | **τ "tortuosity factor"** (conventional) τ/ε = κ₀/κ_eff (Eq 1, p1) — 관통 Dirichlet | **τ_i² "tortuosity factor"** (Eq 4, PDF p.5) — ⚠ 인쇄식 (σ_eff/σ₀)·φ 는 역수 오식, 보고값 = φσ₀/σ_eff (SI Table S2 전 행 재현 — 카드 §4.3 · 문헌 A9) | **τ_e · τ_s "tortuosity of electrolyte / active material"** (SI p.13) — 낱말은 **"tortuosity"** ("factor" 없음) · 값 미보고 | **τ "Tortuosity Factor (D:D)"** τ = D·VolFrac/D_eff (TauFactor.m:3495) | **τ_F "fluid tortuosity factor"** (Eq 6-6 문장, p.376) · "For the Tortuosity model, specify the tortuosity factor is τF." (p.377) · "tortuosity τF,i" (p.343) · τF, τL, τG "corresponding tortuosity factors" (p.450) · 배터리 "Electrolyte tortuosity τl" (p.267, 식 없음) |
| **√T** | τ = √T = 웹앱 τ_Lap,eff (`app.py:2610`) | "τ" (식 3 의 τ; flux τ = √κ — 표 4 (flux, τ² · τ 열) p.61 · 표 5 (기하, 같은 τ 기호) p.62) | "τ² 관례의 τ" (A1374 문장) | — | τ_i (원문은 √ 를 보고하지 않는다 — "2.07" 은 카드 산술) | — | — (Duquesnoy 는 CSV = τ, 그림 = √ — 카드 역링크) | — (입력 칸 없음) |
| **τ_geo** | τ_Dij · τ_Dij,all · 벽 τ = 경로 길이 / 쌍의 \|Δz\| (`dem_analysis_core.py:569–651` · 654–736 · `lhs_descriptor_harvest.py:1361–1416`) | **τ = Δl/Δx "tortuosity" (geometric)** (Eq 1, p.48) · τ_geo (Holzer, p.48) | **τ_path** (Eq 3, A1373) · τ_geo · τ̄_geo — "strictly distinguish" (A1374) | "geometrical tortuosities" (p2 · p7, 식 없음) | **τ_i = l_i/l_0 "geometric tortuosity"** (Eq 3, PDF p.5) — 정의만, 측정 없음 | — | — (모드 1–3 은 flux) | — |
| **τ_e** | — (리포에 없음) | — | Eq 13 τ = R_Ion·A·κ·ε/(2d) (A1382, 차단 대칭셀 TLM) — Nguyen 은 이 방식을 eSCM (τ_e 계열) 로 분류한다 (p.2) | **τ_e "electrode tortuosity factor"** τ_e/ε = R_ion·A_CC·κ₀/L (Eq 2, p8) | EIS-TLM 이지만 셀이 전자 차단 + 양단 Li-In → 관통형에 가깝다 [판독 — nguyen 카드 ⑤] | — | mode 6 "Electrode Tortuosity" (TauFactor.m:3681–3685 · 계수 3 유도 [미확인]) | — |
| **N_M** | 1/f = T/φ (열 없음) · `R_bruggeman_over_full` = N_M/N_M(B) (`network_conductivity.py:1185`) | **N_M = σ_bulk/σ_eff = τ²/ε "MacMullin number"** (Eq 5, p.49) | **N_M = κ/κ_eff** (Eq 1) = τ/ε (Eq 5) · Archie N_M = ε^−m (Eq 2, A1373) | N_M = κ₀/κ_eff (Eq 1) ("McMullin" · "Mullin" 오기) | — (이름 없음) | — | — | — (= 1/f_e) |
| **Bruggeman** | `sigma_bruggeman` = φ^1.5 (`network_conductivity.py:1125`) ⇒ T_B = φ^−½ · √T_B = φ^−¼ | τ² = ε^(1−α), α = 1.5 (Eq 6, p.49) · γ 붙인 Eq 8 | τ = ε^(1−m) = ε^−α, **α = 0.5** (Eq 6, A1374) · N_M(B) = ε^−1.5 | — | — ("Bruggeman" 낱말 없음) | — ("Bruggeman" 0 회) | — | **τ_F = ε_p^(−1/2)** (p.377) · τ_L = ε_p^(−1/2) (p.451) · Electrophoretic "multiplies the diffusivity and mobility values by the porosity to the power of 1.5" (p.415) |

- ⚠ **같은 기호 다른 양** (이름표에 꼬리표 필수):
  - ① Park **τ_e** (전해질 = 우리 T) ≠ Nguyen **τ_e** (전극 tortuosity factor) ≠ 우리 `_e` (전자).  전자 꼬리표는 `_el_` (tjaden 카드 권고).
  - ② Landesfeind **f** (Eq 7 비례인자) ≠ 우리 f.
  - ③ "formation factor": 우리 docstring `F_e = σ_eff/σ_AM,input` (`network_conductivity.py:13–15`, ≤ 1) 는 Archie (Landesfeind Eq 2 의 N_M = ε^−m, ≥ 1) 의 **역수**다.
  - ④ "geo/geom" 셋 (`I-08`): τ_Lap,geom (flux · CF) · Track-B `tau_geo` (flux · AM 여집합) · COMSOL 2D 파라미터 `tau_geo` (= Dijkstra, 기하).
  - ⑤ Bruggeman α: Tjaden/COMSOL 1.5 (f 지수) ↔ Landesfeind 0.5 (T 지수) ↔ √T 관례 0.25.

**COMSOL Tortuosity 칸 = T 인가 — 인터페이스별 강도** (BDM_UG.txt 인쇄 쪽 · 원문 대조 완료):

| 인터페이스 · 자리 | 인쇄 근거 (원문 문장) | 강도 |
|---|---|---|
| Transport of Concentrated Species (다공 매질 확산) | Eq 6-6 "the effective transport factor, fe, is defined from the porosity and the fluid tortuosity factor in the manner of: fe = εp/τF" (p.376) · "For the Tortuosity model, specify the tortuosity factor is τF." (p.377) · "For the Bruggeman model, the effective transport factor is τF = εp^(–1/2)" (p.377) | **확정** (인쇄 식) |
| Transport of Diluted Species (Theory) | "De = (εp/τL) DL — Saturated Porous Media" · "τF, τL, and τG are the corresponding tortuosity factors (dimensionless)" (p.450) · "for the Bruggeman model the tortuosity is defined as τL = εp^(–1/2)" (p.451) | **확정** |
| Electrophoretic Transport | "The default correction model is Bruggeman, which multiplies the diffusivity and mobility values by the porosity to the power of 1.5" (p.415) | 같은 관례 (ε^1.5) |
| 4 장 Electrochemistry — Porous Electrode 노드 | "The Electrode volume fraction is used to calculate the effective electrical conductivity of the porous matrix when the correction factor is set to Bruggeman or Tortuosity." — p.144 (Primary and Secondary Current Distribution) · p.156 (Tertiary Current Distribution, Nernst–Planck).  물리 리뷰 표기 p.143 · p.155 는 0-기준 색인이다 (인쇄 +1) | 보강만 — Tortuosity 선택지에서 부피분율이 계산에 쓰인다 (물리 리뷰 읽기: ε 가 곱해짐 → σ/τ 꼴 배제 · ε/τ ↔ ε/τ² 미결) · 전극 (전자) 상 문장이고 배터리 인터페이스가 아니다 |
| **배터리 인터페이스** — Porous Electrode 노드 (p.266 머리) | "the Electrode tortuosity τs and Electrolyte tortuosity τl parameters may also be used by the Effective Transport Parameter Correction (next section)" (p.267) — 식 없음 | **강하게 시사 (strongly implied) — 인쇄 근거 없음** → 사용 버전 GUI Equation 보기 캡처 1 장으로 닫는다 (미실행) |
| 외부 | Landesfeind A1374 "(e.g., Comsol Multiphysics), where it is expressed terms of ε/τ = ε^1.5" | 같은 관례 |
| **배터리 모듈 앱 예제** — *Homogenizing a Heterogeneous Electrode Model* (Application Library · 첫 줄 "Model created in COMSOL Multiphysics 6.4" · 1저자 업로드 PDF 10-04) | 식 (1) "The effective flux parameter will depend on both the volume fraction, ε, and the tortuosity, τ, of the porous conductive binder domain according to" **f_eff = ε/τ** (p.2) · 식 (2)–(5) 3D 라플라스 (확산계수 1 · u = 0/1) 경계 플럭스 평균 × 두께 → f_eff 0.55 (p.4) · 0.554 (p.11) · 1D 균질 모델 Porous Electrode: "Effective Transport Parameter Correction … From the Electrolyte conductivity list, choose User defined.  In the fl text field, type f_eff*(eps_l_b^1.5)" · "From the Electric conductivity list, choose User defined.  In the fs text field, type f_eff" (p.14) | **같은 관례 (배터리 모듈 문서의 인쇄 식)** — 단 그 예제는 Tortuosity 선택지를 쓰지 않고 f 를 **User defined** 로 직접 넣는다 → 노드 Tortuosity 선택지의 식은 여전히 미인쇄 (위 행 그대로) |

- 쓸 때의 조건 (물리 c1):
  - T 로 COMSOL 이 σ_full 을 재현하려면 COMSOL σ₀ 칸이 **같은 3.0 (우리 간선 재료값)** 이어야 한다.  측정 펠릿값 (예: Minnmann 1.6) 이나 결정립값과 짝지으면 다른 σ_eff 가 나온다.
  - P2D 매개변수로는 Nguyen 이 τ_e 를 권한다 — "should be preferred" (p5 · p8) · "should be used" (p7).
  - √T 에서 "COMSOL" 을 빼는 것은 지금 해도 된다.  T 에 "COMSOL 입력" 표지를 다는 것은 GUI 확인 뒤에 한다.
- ✅ **10-04 D1 (1저자 비준 "권고에 맞게 진행") — COMSOL 인계 경로**:
  - COMSOL 에는 **`f_ion` 을 Porous Electrode 보정 User defined (fl) 칸**으로 넘긴다 — 위 앱 예제와 같은 방식이라 τ 관례가 끼지 않는다.  예제 구성상 fl 은 부피분율을 포함한 σ 배수다 (fl = f_eff·eps_l_b^1.5 — 두 인자 모두 부피분율 포함 → σ_eff = fl·σ) = 우리 f 정의 (σ_eff/σ₀).
  - 같은 틀로 짝짓는다: 두께 L_mc · εl = φ_mc · `f_ion` (판 간격 틀이면 L_gap · φ_구합 · `f_ion_<mode>_gap` — 두 틀을 섞지 않는다).
  - Tortuosity 칸을 쓴다면 `tau2` — "COMSOL 입력" 표지는 GUI Equation 확인 뒤 (결정 5 그대로).
  - 이름 함정: 그 예제는 f_eff 를 "sometimes referred to as the McMullin number (Ref. 2)" 라 부른다 — Landesfeind 등의 N_M = τ/ε = **1/f (역수)** 와 반대다.  우리 표의 f 행 (= 1/N_M) 그대로 두고 "McMullin" 낱말로 열 이름을 만들지 않는다.
  - PDF 는 COMSOL 라이선스 문서라 리포에 넣지 않는다 (쪽 · 식 번호 인용만).  웹앱 반영 = tau2 툴팁 · COMSOL 2D 내보내기 `f_ion` 행 · README (`webapp/test_tau_labels.py` J1–J4).
- COMSOL 자체 표기도 흔들린다.  같은 양을 "fluid tortuosity factor" (p.376) · "tortuosity" (p.343 · p.348) · "tortuosity factors" (p.450) 로 부른다.  p.377 은 "the effective transport factor is τ_F = ε_p^−1/3 (Millington–Quirk)" 처럼 이름을 바꿔 적는다.  **⇒ COMSOL 의 "tortuosity" 낱말 = tortuosity factor = T.**
- 에이전트 기록의 "Diluted Species 375쪽" 은 두 번 틀렸다: Eq 6-6 은 Transport of Concentrated Species 절에 있고 인쇄 p.376 이다.
- Arzt 1982 는 τ 를 다루지 않는다 (§6 접촉면적 전용).

---

## §2. 우리 27 변형 — 판정표

문헌 비교값 약어 (ASSB 복합양극 · 조건 포함):
- **[M]** Minnmann 이온 T 2.40 · 3.23 · 4.27 · 15.3 · 130.  φ_NCM 25/33/42/53/61 vol% · φ_SE 0.613–0.248 (SI 식 S9 재계산값) · 380 MPa 압밀 · ≈ 40 MPa 측정 · σ₀ = 순수 SE 펠릿 1.6 mS/cm @25 °C · 순수 τ² ≡ 1 · SI Table S2 = 카드 §5.0.  fine SE 61 vol% 33.8 — **σ₀ 1.6 (밀링 전) 기준**이고, 밀링 SE 자신의 1.2 mS/cm 기준이면 ≈ 25 다 (문헌 D6, 우리 산술).
- **[M√]** 같은 값의 √ 1.55–11.4.
- **[P]** Park 측정 σ_eff 역산 T ≈ **4.4 / 11 / 19** — Park 자기 σ₀ (SI Table S1 조성식 3.08 / 2.84 / 2.64 mS/cm, 30 °C).  σ₀ 3.0 환산판은 4.3 / 11 / 21 (v1 값).  NCM 60/70/80 wt% · ε_e 0.477/0.347/0.217 (본문 Fig 1a) · 추세 전용 (문헌 D9).  √ 2.1 / 3.3 / 4.4.
- **[G]** ASSB SE 상 기하 τ: 이 7 카드에 값 없음 [미확인].  참고만 — 액체 LIB **기공**상 FMM · pore centroid 1.01–1.26 (Tjaden Table 5, p.62).
- **[E]** ASSB τ_e: 없음.

판정 5 단계: **타당** · **조건부** (조건 · 한정어 붙여 사용) · **이름 틀림** (양은 맞음) · **정의 결함** (계산이 문헌 정의와 어긋남) · **쓰지 말 것**.

| ID | 이름 · 키 | 필드 양 (§1) | 정의 file:line | 입력 φ · σ₀ · 면적 | 우리 값 (n · 출처) | 문헌 비교 | 판정 | 필요한 수정 |
|---|---|---|---|---|---|---|---|---|
| **A. 기하 (τ_geo)** | | | | | | | | |
| T01 | τ_Dij 표본판 `tortuosity_mean/median/std/recommended` | τ_geo | `dem_analysis_core.py:569–651` (쌍 200 · seed 42 :611–615 · [1, 20) :629 · 폴백 :598–605) | — · — · SE 접촉 그래프 (중심 거리) | case_master n=163 1.149–17.49 (1.484) · LHS 웹앱 117/130 1.281–8.101 (1.518) · lhsx 64 1.260–1.594 | [G] | **조건부** — 비관통 침대에 유한값 (`DESC-02W`: case_master 6/163 · LHS 11/130) 만 정의 결함 | 폴백 삭제 → None + 상태 (`TAU-05` — σ_e 22.5 파급은 결정 12) · 라벨 "기하 · 쌍 Δz" |
| T02 | τ_Dij,all `tortuosity_all_*` | τ_geo (FMM 형) | `dem_analysis_core.py:654–736` | — · — · 같은 그래프 | 커밋 표 없음 · ps45 5 건 1.194–1.235 (서술, `session_20260923_progress.md:833`) | [G] | **타당** | 툴팁 "τ_Dij 와 같거나 작다" 철회 (보장 아님 `I-17`, `single.html:1835`) |
| T03 | 수확기 옛 τ `tortuosity_dijkstra_SE` (solid_zrange) | τ_geo | `lhs_descriptor_harvest.py:1249–1358` · `_tau_sample` :1361–1416 | — · — · 원자 기하 그래프 | 14/130 1.318–2.040 · lhsx 31/64 1.271–1.541 | [G] | **쓰지 말 것** (T04 로 대체 · `LHS-08`) | 없음 (보류 유지 `lhs_design_dataset.py:739–742`) |
| T04 | 벽 τ `tortuosity_SE_wall(_median)` | τ_geo | 같은 함수, 벽 띠 :1334–1350 · 규약 :229 | — · — · 같은 그래프 | 130: 106 OK 1.292–4.151 (1.494) · 64/64 1.262–1.600 (1.365) · ps45 1.239–1.289 · 절단 0 | [G] | **타당** ("Tortuosity (기하학적)") | README 문구 "수송 τ (tortuosity factor) 가 아니다" → "flux τ 도, 그 제곱 (tortuosity factor) 도 아니다" · 덱 분모 "두께" (`LREL-05`) |
| T05 | 뷰어 경로 τ `paths[].tortuosity` | τ_geo (경로별) | `analyze_contacts.py:628–718` | — | 커밋 없음 | — | **조건부** (시각화 전용) | 라벨 "시각화 경로 · 통계 아님" |
| T06 | legacy 경로 τ `tortuosity_paths.json` | τ_geo | `analyze_contacts.py:808–841` (i ↔ i 짝 최대 5) | — | 커밋 없음 | — | **조건부** (시각화 전용) | 같음 |
| T07 | τ_Dij_R · v59 proxy | 혼종 (R 가중으로 고른 경로의 유클리드 길이) | `physics_fit_v60_tau_R_real.py:78–199` · `v59_tau_3way.py:76–82` | — · — · physics | 커밋 없음 | — | **쓰지 말 것** (개선 없음 CLAUDE.md:1783) | 보관 표지 |
| **B. flux T 형 (선형) — τ_F = φσ₀/σ** | | | | | | | | |
| T14 | STEP3 pore-τ `step3.pore.tau` | T (기공 확산) | `step3_sigma.py:1591–1672` (τ = ε/D_rel :1663) | ε 전 기공 (닫힌 기공 포함) · D₀ = 1 · 복셀 | 커밋 4 건 전부 None (비관통) · 서술 1,415 → 4.97e9 (`DR3-07`) | TauFactor 정의와 같음 (Li⁺ 아님) | **조건부** (구조 지표로만 — Li⁺ 수송 τ 아님) | 키 `tau2_pore_void_vox` 권고 · `TAU-04` |
| T15 | Track-B `tau_full` | T (이온 · 복셀 · CF 계열 `CL-81`) | `step3_sigma.py:3286–3296` · `mpm_webapp_payload.py:2481–2506` | φ = 전도상 복셀 분율 · 단일 σ 가드 · 복셀 | 커밋 없음 | [M] (정의 같음 · 접촉 저항 항 0) | **타당** (규약 문자열 `linear` 명시) | 꼬리표 `vox_cf` |
| T16 | Track-B `tau_geo` | T (AM 여집합 flux) | `mpm_webapp_payload.py:2507–2520` | φ_geo = 1 − AM 분율 · D = 1 | 커밋 없음 | — | **이름 틀림** ('geo' 인데 flux) | `tau2_flux_amcomp_vox` |
| T17 | τ²_Lap 계열 `tau_sq_Lap_eff` · `tau_eff2` · SI 그림 τ²_Lap,eff | **T** | `build_tau_regime_db.py:137` · `tau_all_backfill.py:134` · `plot_tau_regime_si.py:98–100` | T08 과 같음 | (유도) H 1.945–3646 (6.212) · P 1.436–4401 (10.07) | [M] · [P] | **타당** (= D1 의 T) — **1세대 협착식 (두 모드)** · 게이트 조건 | 인계 `tau2` 의 원형 (§5) |
| T18 | 문헌 앵커 CSV `tau_ion_sq` · `tau_el_sq` | T (문헌) | `docs/data/minnmann2021_sigma_tau_porosity.csv` | — | tau_ion_sq 1–34 · tau_el_sq 1–120 | [M] | **조건부** — 61 vol% 거친 SE 행에 fine-SE 값 34 (SI S2 거친 SE = 130) · 25 vol% σ_ion "~1.4" (S2 0.408 mS/cm) · 42 vol% wt 73 (S1 = 70) · :2 에 인쇄식 Eq 4 | `TAU-12` (SI Table S2 로 교체) |
| **C. flux √T 형 — τ = √(φσ₀/σ)** | | | | | | | | |
| T08 H | τ_Lap,eff Hertz 열 | √T (FULL) | `webapp/app.py:2610` · :2744 | φ 구합 · σ₀ = `_sigma_grain_context` (T 짝, :7495) · **c_cpl[22] 기하 교차 원판** (`L1-04`, "Hertz" 는 이름만) · 협착 = 반공간 Maxwell | (유도) 157: 1.395–60.39 (2.492) | [M√] · [P] √ | **이름 틀림 · 조건부** — 양은 √T 가 맞다.  "COMSOL/EIS input" · "GB 포함" 라벨이 틀렸다.  협착식은 1세대 (반공간 Holm, a/r 0.30–0.44 에서 R_c 1.7–2.4 배 과대) | `TAU-01` · `TAU-13` · 인계는 T 로 (§5) |
| T08 P | τ_Lap,eff physics 열 | √T (FULL) | `app.py:2611–2612` · :2745–2746 | 같음 · physics v1 면적 (`plastic_coverage.py:393–395`) | (유도) 1.198–66.34 (3.173) | 같음 | **조건부** — ψ 분모 (`L2-01`) 1세대 · `L1-01/03` · `LHS-25` (접촉별 상한값 면적) · ψ 절벽 · 화면에서는 physics σ 가 없으면 Hertz 값이 조용히 들어간다 (`TAU-21`) | `TAU-13` 게이트 · `TAU-21` |
| T09 | τ_Lap,geom = τ_Laplace,bulk | √T (CF = 협착 0) | `app.py:2613–2614` · :2747–2748 | 같음 · 면적 무관 (H↔P 차 ≤ 0.19 %) | (유도) 0.789–20.80 (1.206) · **< 1 이 26/157** | 대응 없음 (Minnmann "true geometrical" 은 개념만) | **정의 결함 (모델 성질)** — 부피 비보존 원기둥 R_bulk 로 T < 1 가능 · 솔버 이상 아님 (§3-6) · 'geom' ≠ τ_geo · **모델 내부 기준선 전용** | `TAU-07` · 인계 안 함 |
| T10 | 등급 `__tau_lap_eff` | √T + 재료 인자 | `grade_engine.py:927–935` (σ 선택 :775–784) | φ 구합 · **3.0 고정** · Stage-E physics 우선 (Cronau(r_SE) · 파괴 인자 포함) | (유도) 1.198–66.34 (3.173) · 웹앱 H 대비 0.852–1.584 (1.227) | — | **정의 결함** — 웹앱 H 대비 편차의 주원인은 **모드 불일치** (physics 우선 ↔ 웹앱 H, 156/157).  재료 인자 (Stage-E ≠ physics) 는 1/157 (particulate_1, r_SE 0.25 µm) 뿐 · 온도 불변성 깨짐 (`L4-04`) | `TAU-03` |
| T11 | 등급 `__tau_lap_bulk` | √T_CF | `grade_engine.py:937–945` | 3.0 고정 · CF | = T09 | — | **정의 결함** (T09 + "Bruggeman φ^−0.5 ≈ 1.85" 지수 틀림 — √ 관례면 φ^−0.25, :180) | `TAU-07` |
| T12 | COMSOL 2D `tau_Laplace_eff` (→ `tau_eff`) · `tau_Laplace_bulk` (→ `tau_bulk`) | √T | `export_comsol_2d.py:67–79` · 표 :104–107 · README :658–660 | 3.0 상수 (:48) · stage_e_physics → physics → raw (**stage_e 단계 없음** — 등급과 사슬 한 칸 다름) | 산출물 없음 | — | **정의 결함 (표기)** — 파라미터 표에 √T 를 "COMSOL/EIS input" 으로 적는다.  **자동 배선은 없다** (README 는 SE 도메인에 `sigma_i` 를 직접 넣고 tau_eff 는 "검산용").  README 검산식은 φ 자리가 반대다 (:660 "σ_eff = σ_grain / (φ·tau_eff²)") | `TAU-01` |
| T13 | 오프라인 재계산 계열 (`tau_Lap_eff` · `tau_L_*` · `tau_lap_*` …) | √T (혼합) | `build_tau_regime_db.py:93–95` · `compare_laplace_dijkstra.py:55–67` · `tau_all_backfill.py:125–134` 외 | 스크립트마다 σ 모드 다름 | `docs/db/section7_10case_sweep.csv` n=10 1.21–5.16 (σ 모드 미기록) | — | **조건부** (보관 · SI 진단) | 거듭제곱 · σ 원천 표지 |
| **D. 파생 · 재표지 · 유령** | | | | | | | | |
| T19 | C(τ) logpoly2 | τ_geo 의 회귀 함수 | `generate_comparison_plots.py:4789` · :6066–6069 · `predictor_engine.py:110–156` | T01 recommended → mean | — | — | **타당** (적합 특징 — 수송 τ 주장 아님) | 문서에 "C(τ_geo)" 명기 (CLAUDE.md:2076 "Laplace" 서술 `I-21`) |
| T20 | σ_brug 비 `sigma_ratio` = φ·f_perc/τ_geo² | Bruggeman 꼴 + 기하 τ | `dem_analysis_core.py:1112–1154` (:1147) · 행 ×3.0 리터럴 `analyze_contacts.py:276–278` | φ 구합 · 3.0 리터럴 | n=163 0–0.491 (0.128) | — | **조건부** (어림식 · 기하 τ ≤ flux τ 라 σ 과대 방향) | 'σ_Bruggeman' 행 이름 충돌 (`I-07`) 정리 |
| T21 | 망 Bruggeman `sigma_bruggeman` = φ^1.5 | Bruggeman (암묵 T = φ^−½) | `network_conductivity.py:1119–1125` · :1167–1168 · :1183–1185 | φ = 망 노드 (전 SE) 구합 | n=163 0.043–0.580 | [M] 대비 1.9–65× 벗어남 (Minnmann §16-3) | **타당** (기준선 · 구형 · 균질 한정 — Tjaden R2) | α 관례 표기 (1.5 형) |
| T22 | 비율 "Constriction overhead" — 웹앱 τ_Lap,eff/τ_Dij · 등급 τ_eff/τ_bulk | flux ÷ 기하 · (Stage-E) ÷ CF | `app.py:2626–2631` · :2760–2765 · 라벨 :2142–2143 · `grade_engine.py:183–190` · :947–953 | 섞임 | 웹앱 0.508–20.29 (1.711) · 등급 1.504–3.689 (2.588) · √(CF/FULL) H 1.76–3.50 (2.01) | Tjaden 같은 시료 flux/기하 **1.24–1.59** (접촉 저항 없이) | **정의 결함** (협착 배수가 아님).  같은 망 FULL/CF 도 "순수 협착" 이 아니다 — 원기둥 bulk 때문에 T 로 ≈ 1.2–1.4 배 과대 (§3-6) | `TAU-08` |
| T23 | ML `tau_se` | **T14 재표지** (기공) | `ml_cycle_surrogate.py:28` · :86 · selftest `train_cycle_surrogate.py:223` | — | — | — | **쓰지 말 것** (STEP3 자신이 금지 `step3_sigma.py:1623–1625`) | `TAU-04` |
| T24 | 예측기 · ML `tau` | τ_geo (T01 mean) | `predictor_engine.py:279–285` · `design_performance_corpus.csv` · `ml_design_structure.py:65` | — | n=291 1.149–4.324 · structure nested R² 0.921 | [G] | **조건부** (τ > 8 행 삭제 = 코호트 선별 `L5-01` · 비관통 유한값 `DESC-02W`) | 상태 열로 거르기 |
| T25 | PyBaMM `Bruggeman coefficient` ← τ | 자리 틀림 (지수 b 자리) | `webapp/pybamm_predictor.py:72` (porosity = 공극 :70) | ε = 공극 (ASSB 전해질상 = SE 여야) | 호출자 없음 | — | **쓰지 말 것** | `TAU-15` |
| T26 | 유령 키 `tortuosity_electronic_*` · `tortuosity_lap_eff` · `tau_lap_eff` · `tau_dij(_R)` (+ `constriction_pct` · `constriction_fraction_pct`) | 없음 | 소비자만 (`generate_comparison_plots.py:6067–6069` · 6480 · `electronic_nested_cv.py:190` · `generate_fitting_report.py:675` · `app.py:2893` · 2903 · 2910 · `refresh_warnings.py:76` · 86 · 92) — 생산자 0 (git grep · 접두 결합 · f-문자열도 0) | — | 커밋 자료 0 | — | **정의 결함** (σ_e C(τ) 가 조용히 SE 이온 τ · 경고 영영 안 뜸) | `TAU-06` · `TAU-23` |
| T27 | "formation factor" F_e = σ_eff/σ_input | **f** | `network_conductivity.py:13–15` (docstring) · CLAUDE.md:150 | — | (유도) f_H 3.5e-5–0.356 (0.0467) | Minnmann f_ion 0.255 → 0.00191 (카드 §5.0) | **이름 틀림** (Archie 이름은 1/f) | 문서 · `TAU-17` |

- 목록 대조: 코드 리뷰가 §2 의 file:line 49 행을 전부 다시 열었다 — 확인 37 · 부분 10 · 틀림 1 · 검증 불가 1 (§R).  v1 이 적은 잔차 셋 (`active_fractions` ±2 줄 · Arzt 카드 L-1 의 면적식 자리 = 실제 `plastic_coverage.py:266–404` · COMSOL 쪽) 중 COMSOL 쪽은 v1 에서 전부 1 작았고 (문헌 A13–A15) v2 에서 인쇄 쪽으로 고쳤다.

---

## §3. 값의 합리성 — 필드와 맞대기

### 3-1. σ₀ 는 우리 T 에서 약분된다 — 실험 T 에서는 아니다
- 망은 ρ = 1 로 풀고 출력에서 σ_bulk 를 곱한다: `sigma_full_mScm = σ_ratio × σ_bulk × 1000` (`network_conductivity.py:1156`).  이온 σ_bulk = `se_material.sigma_grain_S_cm(T)` (:1226).
- 이온 모드는 σ_rel = 1 · k_weight = 1 (:359–400) 이다.  R_bulk · R_Maxwell · R_constriction · 경계 g 가 전부 1/σ 에 비례한다 (:401–452 · :661–664).  웹앱은 같은 출처 · 같은 온도의 σ₀ 로 나눈다 (`app.py:2601` → `_sigma_grain_context` :7495).  ⇒ **T = φ/σ_ratio, f = σ_ratio — σ₀ 값 (3.0 이든 1.6 이든) 이 사라진다** (물리 a2 · 코드 #13).
- 예외: 등급 · COMSOL 2D 는 3.0 상수 + Stage-E σ 를 쓴다 (`L4-04` · `TAU-03`).  그러나 이 코퍼스에서 Stage-E physics ≠ physics 인 행은 1/157 뿐이다.
- ⚠ **비대칭** (물리 a2): 실험 T = φσ₀/σ_meas 는 **가정한 σ₀ 에 정비례**한다.  Park 역산값은 σ₀ 를 무엇으로 두느냐에 달려 있다 (Park 자기 σ₀ 판 4.4 / 11 / 19 ↔ 3.0 판 4.3 / 11 / 21).  Minnmann 은 자기 펠릿 1.6 을 쓴다.  ⇒ 우리 쪽 약분이 대조를 공짜로 만들어 주지 않는다.
- 절대 σ_eff 끼리는 직접 비교하지 않는다 — 같은 미세구조면 우리 σ_eff 는 3.0/1.6 = 1.875 배로 나온다 (minnmann 카드 §11).

### 3-2. 기준 상태 — 방향은 정해져 있다 (v1 "방향도 미정" 철회)

| 항목 | 값 | 출처 |
|---|---|---|
| Minnmann 의 기준 | 순수 SE 펠릿 τ² ≡ 1 (SI p.4 §3 "the tortuosity factor of the pure materials has been set to unity") · σ₀ 1.6 mS/cm @25 °C | 문헌 A10 |
| 우리의 기준 | 간선 재료 σ₀ (펠릿값 3.0, `CL-91`) + SE–SE Holm 직렬 (부분 이중계상, CLAUDE.md CL-81 절 → T↑) · 원기둥 bulk (T↓) · 띠 끝 단락 (T↓) | 코드 |
| SE 가장 많은 침대 (a5 계열 6 침대, φ_SE 0.689–0.696 · φ_AM 0.29 · ε_sphere 1.0–2.4 %) | T_H 1.95–2.47 · T_P 1.44–1.91 · T_CF 0.62–0.79 | 물리 a3 (유도 · v2 재실행 일치) |
| SE 많은 띠의 T_H/T_CF 중앙 | ≈ 3.2 (곧은 사슬 시험 T_FULL/T_CF ≈ 2.9, d/r 1.78) | 물리 a3 · 코드 #15 |
| 외삽 T_pure,ours (φ ≈ 0.88 = 순수 SE, 기공 ≈ 12 %) | **hertz ≈ 1.4–2.0 · physics ≈ 1.0–1.5** | 물리 a3 — a5/a6 한 계열의 SE 쪽 기울기 (ln T vs φ: −0.4 ~ −2.4 /φ) 외삽 · **측정 아님** |
| 함의 | 펠릿 σ₀ 위 Holm 이중계상이 원기둥 과전도보다 크다 → T_pure,ours > 1 → Minnmann 관례로 맞추면 우리 T 는 **× 0.5–0.7** (hertz) | 우리 산술 (1/2.0 … 1/1.4) |
| 처방 | 순수 SE 침대 망 1 회 = 모든 절대 대조의 게이트 (결정 4) · 원 T 와 정규화 T 를 둘 다 보고 | — |

### 3-3. 우리 T vs Minnmann 2021 (SI Table S2) — 판정 없이 숫자만

짝짓기 규약:
- 띠 중심 = Minnmann φ_SE (SI 식 S9 재계산값 0.6133 · 0.5364 · 0.4437 · 0.3297 · 0.2478, 공통 평균 기공 14 % 로 계산된 값) ± 0.04.
- 우리 φ = 구합 φ (`phi_se`) · FULL 해 · (유도).
- ⚠ 53 vol% 띠 중심을 0.330 으로 반올림하면 n 56 · T_P 8.75 가 된다 (코드 #35).

| φ_NCM (vol%) | Minnmann φ_SE | Minnmann 시료 기공 (SI Table S1) | Minnmann T_ion | 우리 n | 우리 ε_sphere 중앙 | 우리 φ_mc/φ_구합 중앙 | 우리 r_SE/r_AM 중앙 | T Hertz-geom 중앙 [범위] | T physics 중앙 [범위] | T_H / T_M | 띠 표지 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 0.613 | 7.6 % | 2.40 | 6 | 4.7 % | 0.907 | — (p_frac 결측) | 2.65 [2.21–3.24] | 2.28 [1.93–2.95] | 1.10 | **과압축 영역** (a6 계열) · σ_P > σ_H (ψ 절벽) |
| 33 | 0.536 | 13 % | 3.23 | 2 | 6.1 % | 0.917 | — | 2.73 [2.59–2.86] | 2.51 [2.49–2.53] | 0.85 | **과압축 영역** (particulate_7/10) · σ_P > σ_H |
| 42 | 0.444 | 17 % | 4.27 | 12 | 9.8 % | 0.940 | — | 3.20 [2.36–4.87] | 4.15 [3.04–5.66] | 0.75 | a/r_SE ≈ 0.41 (hertz 협착 과대 큰 쪽) |
| 53 | 0.330 | 17 % | 15.3 | 57 | 15.8 % | 0.978 | 0.133 [0.104–0.469] | 5.40 [3.89–18.6] | 8.77 [6.28–39] | 0.35 | 입경비 영역 밖 |
| 61 | 0.248 | 15 % | 130 (fine SE 33.8 — σ₀ 1.6 기준) | 46 | 18.7 % | 0.982 | 0.125 [0.104–0.469] | 13.5 [6.21–26.6] | 19.7 [9.64–66.8] | 0.10 (fine 대비 0.40 · 밀링 SE σ₀ 1.2 기준이면 0.53) | 문턱 근접 (φ − 0.20 중앙 0.038) |

- ε_sphere · r_SE/r_AM · φ − 0.20 = 물리 리뷰 계산 (v2 재실행 일치).  φ_mc/φ_구합 = (1 − ε_union)/(1 − ε_sphere) = v2 새 계산 (case_master 의 쌍 렌즈 union).  쌍 렌즈 union 은 정확 union 보다 낮게 잡히므로 (`SELF-72`) 실제 이동은 이보다 크다.  Minnmann 시료 기공 순서는 카드 §3 (7.6 · 13 · 17 · 17 · 15 %).
- **φ 관례 감도** (물리 b2): 두 감도 모두 SE 많은 쪽의 가로 어긋남을 키우고, 둘 다 띠 폭 0.04 보다 크다.
  - ① D3 의 φ_mc 로 짝지으면 SE 많은 띠의 우리 점이 0.05–0.06 왼쪽으로 간다 (위 표 0.907 · 0.917).
  - ② Minnmann 은 공통 기공 14 % 로 φ 를 계산했다.  25 vol% 시료의 실측 기공 7.6 % 를 쓰면 그 점의 φ_SE 는 0.613 → 0.659 로 오른쪽으로 간다 (카드 §3).
- **곡선 이동** (물리 b3 ⑤): 우리 3.20 @0.444 ≈ Minnmann 3.23 @0.536 이고, 우리 13.5 @0.248 ≈ Minnmann 15.3 @0.330 이다.  ⇒ 우리 곡선 ≈ Minnmann 곡선을 φ_SE 로 0.06–0.09 왼쪽으로 옮긴 꼴이다.  "SE 많은 쪽 정합" 과 "SE 적은 쪽 3–10 배" 는 같은 어긋남의 두 얼굴이다.
- **기공을 맞추지 않았다**: SE 많은 띠는 우리 ε_sphere 3–6 % ↔ Minnmann 7.6–13 %, SE 적은 띠는 16–19 % ↔ 15–17 % (근접) 다.  같은 φ_SE 에서 우리 SE 많은 침대는 기공 자리에 AM 이 0.12 더 있다 (φ_AM 0.37 ↔ 0.25).
- 위 두 띠는 CLAUDE.md 신뢰성 지도가 "SE/고체 ≳ 50 % → DEM ε_sphere 과압축 (겹침 인공물)" 로 표시한 영역이다 (ε_union 11.9–15.3 %).

### 3-4. 우리 T vs Park 2020 역산 — 추세 전용

| NCM wt% | ε_e | Park T (Park σ₀) | Park T (σ₀ 3.0 판) | 우리 n | T_H 중앙 [범위] | T_P 중앙 | T_H / T_Park (Park σ₀) |
|---|---|---|---|---|---|---|---|
| 60 | 0.477 | 4.4 | 4.3 | 9 | 3.11 [2.78–4.87] | 4.45 | 0.71 |
| 70 | 0.347 | 11 | 11 | 28 | 4.79 [2.73–11.7] | 7.58 | 0.44 |
| 80 | 0.217 | 19 | 21 | 36 | 15.1 [7.0–552] | 20.2 | 0.79 |

- Fig 2b 판독 불확실성 ±0.03 dex (T 로 ±7 %, 문헌 리뷰 F 절) 은 결론을 바꾸지 않는다.
- 한정어 (물리 b5):
  - T_Park 는 가정 σ₀ 에 비례한다.  Park 의 σ₀ 는 측정 펠릿이 아니라 조성 의존 모형 입력이다 (SI Table S1 식 · 30 °C).
  - NBR 바인더 2 wt% 가 있다 (이온 차단 → 실험 T↑).  슬러리 공정이고 두께 ≈ 39 µm 다.
  - NCM · LPSCl 이 둘 다 ≈ 8–10 µm 이다 (입경비 ≈ 1 — Minnmann 과 같은 입경비 교란).
  - Park τ 값 · 산출법은 원문에 보고되지 않았다.
- ⛔ Minnmann 비율과 Park 비율을 한 문장의 "너무 낮다" 로 합치지 않는다.

### 3-5. Bruggeman 배수 · flux ÷ 기하

| 비 | 우리 (유도, n = 157) | 문헌 |
|---|---|---|
| T / φ^−½ (Bruggeman 배수) | H 중앙 3.40 (IQR 2.54–6.71) · P 5.42 (3.94–9.62) — 1세대 협착식 포함 | Minnmann 1.9–65× (42 vol% 2.8×) · **Park 실험 3.0–9.8×** (σ₀ 3.0 판; Park σ₀ 판 3.0–8.8×) · Park 모형 5-seed 밴드 1.8–24× (**시뮬** — 실측 칸과 섞지 않음, 문헌 D10) · 액체 전극 ≈ 1.5–3× (Landesfeind A1386) |
| √T_FULL / τ_Dij | H 1.711 (IQR 1.37–2.10) · P 2.09 (1.53–2.62) | Tjaden 같은 시료 기공상 **1.24–1.59** (Table 4 p.61 ↔ Table 5 p.62 의 쌍 셋, 우리 산술 · 접촉 저항 없음) |
| √T_CF / τ_Dij | **0.80** (IQR 0.69–1.03) | Tjaden "flux ≥ 기하" (p.60 식 22 문장 — 근거는 [63, 85] 부분체적의 경험식, 문헌 D2) — 우리 CF 는 **반대 방향** (원기둥 bulk, §3-6) |

- ⇒ 웹앱 "Constriction overhead" (τ_Lap,eff/τ_Dij ≈ 1.7) 는 협착으로 읽을 수 없다 — 접촉 저항이 없는 연속 기공상도 1.24–1.59 를 낸다.
- 같은 망의 FULL/CF (√ 중앙 2.01 · T 중앙 ≈ 4) 도 "순수 협착 배수" 가 아니다.  이름은 "모델 내부 협착 비 (원기둥 bulk 기준)" 이고, T 로 ≈ 1.2–1.4 배 과대다 (§3-6).

### 3-6. CF 가지의 T < 1 — 모델 성질 (솔버 이상 아님)

| 항목 | 내용 | 출처 |
|---|---|---|
| 곧은 사슬 유도 | N 개 · 반지름 r · 중심 간격 d · 상자 단면 A (사슬 하나) · 판 간격 L = (N−1)d + 2r.  CF 간선 R = d/(σπr²) (`network_conductivity.py:401–403` — 반쪽마다 **입자 단면 전체 πr² 의 원기둥**) · φ = N·(4/3)πr³/(A·L) (구합, :1120–1123) ⇒ **T_CF = (4/3)·r·d·N(N−1)/L² → (4/3)(r/d)**.  d = 2r → 2/3 · d = 1.78r → 0.75 · T_CF < 1 ⇔ d > 4r/3 | 우리 유도 · 코드 #14 |
| 연속체 하한 | 부피분율 φ 인 연속 전도상은 Wiener 평행 상한 σ_eff ≤ φσ₀ 를 지킨다 ⇒ T ≥ 1.  1D 가변 단면 T = ⟨A⟩⟨1/A⟩ ≥ 1 · TauFactor 관통 모드 "τ ≥ 1" · 곧은 관통 기공 τ = 1 (Nguyen Fig 3) | 표준 결과 · 물리 a1 |
| 원인 | 구의 지름 방향 평균 단면은 (2/3)πr² 인데 원기둥은 πr² → 곧은 사슬에서 1.5 배 과전도.  3D 에서는 결합마다 같은 부피를 다시 쓴다 — affine 근사 T_CF ≈ 8r/(Zd) (d = 2r 이면 4/Z).  코퍼스 T_CF/(4/Z) 중앙 1.87 (IQR 1.62–2.64) · φ_SE ≥ 0.44 쪽 (n 23) 은 중앙끼리의 비 1.38 (T_CF 0.808 ÷ 4/Z 0.585).  ⚠ v1 의 "도체 부피 ≈ 0.75·Z 배" 는 부피 진술로만 맞다 — 전도에는 z 성분 결합만 기여한다 | 물리 f1 (우리 산술 · v2 재실행 일치) |
| 솔버 실측 | 평행 사슬 4 개 (띠마다 ≥ 3 입자): N 30 · d/r 1.9998 → 0.6445 (= 식) · N 30 · 1.78 → 0.7182 · N 120 · 1.78 → 0.7413 · N 120 · 1.9998 → 0.6612 · T_FULL (c_cpl[22] 원판, d/r 1.78) 2.108 / 2.176 | scratchpad `tau_chain_check2.py` · 코드 #15 재실행 |
| 코퍼스 26/157 | 전부 `plate_z_source = mesh` (판 높이 과대라는 L2 원인 배제) · 전부 SE 많음 (φ 0.36–0.69 · overlap_mean 9–23 %) | 코드 #16 · #17 |
| **분류** | **원기둥 bulk 모델의 예정된 성질** — 솔버 이상이 아니다 → SOLVER_ANOMALY 표지 폐기 (§5-2 G5).  CF 는 이 모델의 σ 상한 (모델 내부 기준선) 이지, Wiener 를 지켜야 하는 물리적 "이상 접촉 극한" 이 아니다.  ⇒ CL-81 의 복셀 ÷ 접촉망 대조를 크기로 읽으면 CF 과전도 (× 1/(0.6–0.8)) 가 섞인다 → 사전등록 (결정 11) | 물리 f1 |
| FULL 의 T ≥ 1 (157/157) | Holm 이 원기둥 과전도를 가린 결과이지 물리 정합의 증거가 아니다.  physics 절벽 간선 (R_c = 0) 이 늘면 FULL 도 모델 안에서 T < 1 이 될 수 있다 (a5 계열 T_P 이미 1.44–1.91) | 물리 f3 |
| 협착 비 FULL/CF | 직렬 근사: (m_model − 1) = (m_phys − 1)/b, b ≈ CF 의 bulk 과전도 인자 0.6–0.8.  T 배수 중앙 ≈ 4 는 부피 일관 bulk 라면 ≈ 2.8–3.4 다 → **T 로 ≈ 1.2–1.4 배 · √ 로 ≈ 1.1–1.2 배 과대**.  b 가 Z 에 따라 변해 (T_CF/(4/Z) IQR 1.62–2.64) 침대 간 비교에 Z 가 섞인다.  physics 모드는 절벽 간선 비율까지 섞인다 (SE 많은 띠 접촉의 ≥ 15.8 %) | 물리 f2 (우리 산술) |
| 띠 끝 단락 (L0) | 띠 안 SE 를 g_boundary ≫ g_bulk 로 전극에 묶는데 (`:225–249` · `:620–666`) σ 는 판 간격 전체로 정규화한다 (`:853–857`) → 양 끝 ≈ 2r 씩이 저항 0.  **T 하향 ≤ 4r_SE/L** · 코퍼스 4r_SE/L 중앙 0.062 · p90 0.12 · 최대 0.17 (상한 추정).  곧은 사슬 4 개 (L0) 에서 T_CF/극한 0.967 @ 2r/L 0.033.  r_SE/L 에 따라 달라 입경군 간 대조를 비튼다 (a5 계열 0.083) | 물리 f4 · 코드 M5 |
| 띠 폴백 (L1) | 사슬 **하나** (띠 입자 < 3) 면 L1 (판 간격 15/85 %, `:230–235`) 이 조용히 켜진다.  T_CF 0.5113 · 0.5697 · 0.5295 = 네 사슬 대비 0.793 · 0.793 · 0.714 (21–29 % 낮음 · σ 26–40 % 과대).  ⇒ `LHS-17` 의 무기록 폴백은 σ · T 값도 바꾼다 (원장 영향 열에 σ 없음 → 새 증거).  LHS 130/130 은 L0.  역사 코퍼스의 L1 빈도는 [미확인] (case_master 에 띠 열 없음) — L2 판 높이 원인만 `plate_z_source = mesh` 157/157 로 배제 | 코드 #27–#30 |

### 3-7. φ 상자 (D3) 가 T 에 주는 영향
- 질량 보존 장부 (`dem_analysis_core.py:1274–1283`): L_mc = L_gap·(1−ε_구합)/(1−ε_union) · φ_SE,mc = (1−ε_union)·V_SE/ΣV ⇒ **φ_SE,mc·L_mc = φ_구합·L_gap** (우리 유도 · 코드 #37 대수 확인).
- 부피 보존 z-신장 (단면 1/s · 길이 s 배, s = L_mc/L_gap) 이면 G → G/s², σ_eff → σ_eff/s, φ → φ/s ⇒ **T 불변**, f 만 1/s 배.  ⇒ 일관된 두 상자 어디서든 **T = φ_구합·σ₀/σ_full (= 현행 웹앱 T)**.
- ⚠ 이 불변은 **자기상사 가정**이다 (물리 g3).  실제 겹침 해소는 균일 신장이 아니라 접촉을 줄인다 (Holm ∝ 1/a, a ∝ √δ).  그러면 G 는 1/s² 보다 빨리 떨어질 것이다.  ⇒ f_mc 는 풀린 양이 아니라 **재척도한 양**이고, T(ii) = T(솔버) 는 정의에 의한 등식이다 → 이름표 "재척도 (해 아님)" · 풀린 f_gap 병기 (결정 1).
- 섞은 짝 (φ_mc ÷ 판 간격 f) 만 T 를 s⁻¹ 배 낮춘다: 배포 v1.1 L_gap/L_mc = LHS 0.898–0.985 (중앙 0.959) · lhsx 0.867–0.931 (0.894) (`docs/data/lhs_release_20261001_v11/*.csv` 의 `thickness_wall_gap_um` ÷ `thickness_mass_conserving_um`).

### 3-8. 어디서 높고 낮은가 — 가설 (미검정)

| 구간 | 우리 위치 (숫자만) | 판정 | 원인 후보 (방향) |
|---|---|---|---|
| SE 많음 (φ_SE ≥ 0.44) | Minnmann 대비 H 0.75–1.10 · P 0.78–0.97 · Park 60 wt% H 0.71 | **판정 불가** (v1 "정합 범위" 철회 — 물리 b3) | 기준 상태 미보정 (× 0.5–0.7 추정, §3-2) · hertz 반공간 Holm 과대가 가장 큰 영역 (a/r_SE 0.41–0.44 → R_c 2.2–2.4 배) · 위 두 띠 과압축 영역 · φ 관례 감도 > 띠 폭 (§3-3) · σ_P > σ_H 역전 14/14 = ψ 절벽 (아래 행) |
| SE 적음 (φ_SE ≤ 0.35) | Minnmann 대비 H 0.10–0.35 · P 0.15–0.57 · Park 70 · 80 wt% H 0.44 · 0.79 | **다른 미세구조의 비교** — 모델 오차 배수가 아니다 (물리 b4) | 아래 ①–⑦ |
| physics vs hertz | 143/157 σ_P < σ_H (중앙 비 0.664) · 14/157 σ_P > σ_H — 전부 φ_SE ≥ 0.554 | — | 143 침대: ψ 분모 배치 R_c = 1/(2σaψ) (`network_conductivity.py:444`, `L2-01`) — 커밋 자료와 정합한다: 탄성 가지 몫 ≤ 0.9 % (중앙 0.1) · 협착만 망 σ_P/σ_H 0.21–0.89 (중앙 0.39, n 43, `network_dual.ratio_physics_over_hertzian.sigma_constr_net`) · CF 모드 무관 (≤ 0.19 %).  곱 배치에서 반전될지는 [미검증].  14 침대: ψ 절벽 (ψ < 1e-4 → R_c = 0, `:445–452`) + a_eff 클램프 (`:425` — 2πR_min² 캡에 걸린 접촉은 a = √2·r_min → ψ = 0).  그 띠의 geom 캡 결합 15.8 % → physics T 가 CF 쪽 (T < 1 가능) 으로 끌린다 (코드 #18 · #19 · 물리 b8).  ⛔ 실험에 더 가깝다고 physics 를 고르지 않는다 |
| CF | T_CF 0.62–433 (1.454) · < 1 이 26/157 | 모델 내부 기준선 전용 | §3-6 — 절대값 비교 금지, 같은 망 안의 FULL/CF 분해에만 (그것도 "모델 내부 협착 비") |

SE 적은 쪽 원인 후보 (물리 b4 · b6):
- ① **입경비**: 우리 r_SE/r_AM 중앙 0.133 · 0.125 (범위 0.10–0.47) ↔ Minnmann SE D50 3.45 · D90 20 µm 대 NCM ~3 µm (비 ≥ 1, SI Table S5 · 본문 PDF p.3) ↔ Park 둘 다 ≈ 8–10 µm.
  - 코퍼스 안 검정: φ 0.31–0.35 에서 r_SE ≥ 1.0 (n 4) T_H 중앙 6.87 ↔ r_SE 0.5 (n 6) 5.18 · ln-선형 적합 T(0.33) 8.3 ↔ 5.3 · 53 vol% 띠 ρ(T_H, r_SE/r_AM) = +0.63 (n 25).
  - 방향은 가설을 지지한다.  그러나 우리 최대 입경비 0.47 로는 15.3 에 닿지 못한다 → 영역 밖 대조다.
- ② **퍼콜 문턱 거리**: Minnmann ln T 기울기 −3.9 → −3.0 → −11 → −26 /φ (61 vol% 쪽에서 발산) ↔ 우리 −0.4 → −1.7 → −4.6 → −11.
  - 우리 61 vol% 띠 침대는 모델 φ_c (0.195–0.200) 위 0.04 (중앙 0.038) 뿐이고, T_H 가 φ (ρ −0.50) · 기공 (+0.68) 을 따른다.
  - 세로 배수는 두 문턱의 거리차가 지배한다.  Minnmann 자신도 PSD 만 바꿔 같은 φ 에서 130 → 33.8 (× 3.8) 이다.
- ③ **springback** (v1 에 없던 후보): DEM 망은 최대 압밀 기하 (판 고정 완화) 인데, 실험은 380 MPa 뒤 하중을 풀고 ≈ 40 MPa 에서 EIS 를 했다.  springback 은 실험 T 를 올린다 (우리가 낮게 보이는 방향).  [스냅샷 단계는 덱별 확인 필요]
- ④ 원기둥 bulk 과전도 (T↓, §3-6) · ⑤ 띠 끝 단락 (T↓, ≤ 4r/L).
- ⑥ 연화 E 의 큰 겹침 — **부호 미정 (검증 불가)**: 배위수↑ · a↑ → Holm↓ (T↓) ↔ 반공간 Maxwell 과대가 a/r 와 함께 커짐 (T↑, §0 ⑤).  반사실 (실제 E) 망이 있어야 가린다.
- ⑦ 펠릿 σ₀ 위 Holm 이중계상 (T↑): 기준 상태를 맞추면 우리 T 가 더 내려가 이 구간의 격차는 오히려 커진다.
- ⛔ **바인더 · CBD 차단 후보는 Minnmann 대조에서 뺀다** — 전도도 시료는 NCM + LPSCl 건식 혼합뿐이다 (바인더 · 탄소 없음, VGCF 는 별도 비교군).  Park 에는 해당한다 (NBR 2 wt%).
- v1 의 후보 ④ "c_cpl[22] 면적 (탄성 Hertz 의 ≈ 2 배)" 는 따로 떨어진 원인으로 세지 않는다.  그것은 "Hertz" 열이 이름만 Hertz 라는 사실 (`L1-04`) 이고, 그 면적이 협착에 주는 효과는 ⑥ (큰 a · 반공간 Maxwell) 에 들어 있다.

---

## §4. 고칠 결함 — 우선순위 (제안 ID · 원장 미등재)

⛔ **공통 제약 — S3 봉인** (코드 #24–#26 반영):
- 봉인 대상: `seal_s3_prerun.py:99–100` `NUMERIC_MODULES` = `network_conductivity` · `plastic_coverage` · `audit_constriction_deleted` · `extract_se_network_diagnostics` (넷).
- 수정은 **금지가 아니라 재봉인 강제**다.  `run_s3_psi.verify_code_bundle` (`run_s3_psi.py:243–278`) 이 봉인 파일의 모듈 sha256 ≠ 지금 트리면 그 봉인을 거부한다.  게이트 selftest (`check_all.sh:234` → ⑫d) 는 커밋 안 된 수정만 잡는다.
- 봉인 창은 `SEAL_DEADLINE 2026-09-17 23:59 KST` (:40–51) 였다.  그 뒤 `plastic_coverage.py` 가 09-29 에 세 번 바뀌었고 (`114f5514d` · `00cc8461b` · `d64dd9cdf`) `network_conductivity.py` 는 09-28 `c0c2d4f44` 에 바뀌었다.  리포에 봉인 파일이 없다 (`docs/data/s3_prerun_seal.json` 부재).  ⇒ 09-17 봉인이 있었다면 이미 거부 상태다.
- 그래도 수치 변경은 S3 기준선을 바꾼다 → **f/T/τ 는 봉인 밖 새 도우미** (예: `scripts/tau_flux.py`) 에서 계산하고, 봉인 모듈 문구 수정은 다음 재봉인에 묶는다 (결정 16).
- 규칙 J20-l: 코드 → 웹앱 → 게이트 → 커밋 한 묶음.

### P1
| ID | 결함 | file:line | 시험 먼저 → 최소 수정 | 웹앱 짝 |
|---|---|---|---|---|
| TAU-01 | **√T 에 "COMSOL/EIS input"**.  COMSOL 종 수송 τ_F = T (§1) · 배터리 인터페이스는 강하게 시사 · EIS-TLM 은 τ_e 계열일 수 있다.  √T 를 COMSOL τ_F 칸에 **배선하는 코드는 없다** — 표기 · README 검산식 · 열 사전이 사람을 그 칸으로 보낸다 (넣으면 σ_eff √T 배 과대) | `app.py:1947` · 2050–2051 · 2140–2141 · 2606 · 2615 · 2623 · 2740 · 2757 · 9543–9544 · `single.html:1823` · 1841 · 1843–1847 · 1852 · `grade_engine.py:14` · 164–167 · 925 · `export_comsol_2d.py:72` · 104–105 (표 표기) · **658–660 (README — `sigma_i` 직접 · tau_eff 는 "검산용" · 검산식 φ 자리 반대 :660)** · `lhs_design_dataset.py:884` → **커밋 TSV 6 개**: `docs/data/lhs_handover_20261001_columns.tsv` · `lhsx_handover_20261001_columns.tsv` · `lhs_release_20261001/{lhs,lhsx}_release_20261001_columns.tsv` (배포 v1) · `lhs_release_20261001_v11/{lhs,lhsx}_release_20261001_v11_columns.tsv` (배포 v1.1) — v1 · v1.1 은 **이미 전달됐다** (Codex GO 10-01) · selftest `:3222–3223` (낱말 'COMSOL' · 'τ_Laplace' 존재만 강제; :3192 는 주석) · `plot_section7_design_rules.py:106` · `docs/bruggeman_tortuosity_network_20261002.md:32` · `docs/stage4_electrochem_research.md:44` (PyBaMM "tortuosity factor" 칸 문서 코드) · CLAUDE.md:25 | ① 웹앱 τ 블록 렌더: √T 행에 "COMSOL" · "EIS" 없음 · T 행 있음 (지금 실패) ② `export_comsol_2d.numerical_parameters` 합성 입력 → `tau2` 행 == φσ₀/σ_full · README 검산식 σ_full = φσ₀/τ² (지금 실패) ③ 열 사전: 새 문구가 'COMSOL' · 'τ_Laplace' 를 둘 다 유지하면 ㉓b 는 수정 없이 통과한다 — 하나라도 빼면 ㉓b 를 먼저 바꾼다 → 라벨 · README · T 열 (숫자 불변) · 전달본은 결정 5 (정오표 + v1.2) | 케이스 τ 블록 · 툴팁 · 등급 툴팁 · 배포 README · 열 사전 |
| TAU-02 | **"Minnmann 2.07 vs 우리 2.10 — 1.4 % 일치 · parameter-free external validation"** — 한 케이스 (particulate_11 Hertz; physics √T 2.369) · 같은 φ 띠 n = 12 에서 T_H 2.36–4.87 · σ₀ 기준 다름 (§3-1 · §3-2) · hertz 1세대 · "42 vol% CAM ↔ 42.7 vol% SE" 혼용 · σ₀ 라벨 "LPSCl bulk MLIP-MD value" (`CL-91` = 펠릿값) | `single.html:1845` · 1847 | 툴팁 문자열 시험 → **수치 없이 철회** (결정 8) | 같은 파일 |
| TAU-03 | **"τ_Laplace,eff" 한 이름에 최소 다섯 변형**: 웹앱 H · 웹앱 P (raw + T 짝 σ₀) · 등급 (stage_e_physics → physics → stage_e → raw + 3.0) · COMSOL 2D (stage_e_physics → physics → raw — stage_e 없음 + 3.0) · regime DB (raw H + 3.0).  등급 / 웹앱 H 0.852–1.584 (1.227) 의 주원인은 **모드 불일치 (156/157)** 다 · 재료 인자는 1/157.  `grade_engine.py:925` "same formula as webapp/app.py:2026" 은 낡은 줄 번호이고 :169 "같은 공식이 아니다" 와 모순이다 | `app.py:2599–2612` · `_sigma_grain_context` :7495 · `grade_engine.py:775–784` · :925 · :932 · `export_comsol_2d.py:48` · 69–70 · `build_tau_regime_db.py:28` · 90 · 95 | 같은 metrics → 등급 값 == 웹앱 값 (모드별) · σ_grain ×4 → T 불변 (등급 툴팁의 L4-04 예) → 한 도우미 · Stage-E 판에서 "τ" 이름 제거 | 등급 표 · 그룹 비교 `grade:` 파라미터 |
| TAU-10 | **프레임 [1] "pure-SE porosity ≈ 10 % @ 300 MPa (Minnmann et al.)"** — Minnmann 2021 본문 · SI 에 순수 시료 기공값도 "300 MPa" 도 없다.  있는 것은 380 MPa 복합 양극 기공 7.6–17 % (평균 14 %) 뿐이다 (문헌 B1).  카드 계보 (`minnmann2022_…` 카드): 우리 MPM/DEM 보정 표적 · 수렴값 (Minnmann 2021 복합 + Sakuda 2013 유리 거동 위) → **순환 앵커 의심** (문헌 B2 · 물리 h2) | CLAUDE.md:464 · 1101 · 1123 · 1143 · 1259 · 1310 · 1322 · 1325 · 1356 · 1392 · `mpm3d_compaction.py:19` · 618 (help) · `docs/mpm3d_calibration.md` (9 곳) · minnmann2022 카드 :429 (정본 브랜치) | 원장 **`CL-94` (제안)**: "MPM σ_y 0.30 보정 앵커 '순수 SE 10 % @300 MPa' 의 출처 [미확인] — Minnmann 2021 (본문 + SI) 에 없음 · 카드 계보상 우리 보정 수렴값 (순환)" · status hold → 같은 커밋에서 문구를 "출처 [미확인] (Minnmann 2021 아님) · 외부 앵커 없음" 으로 → 정정 뒤 정확 문자열을 `quotation_ban` 에 | 웹앱 해당 화면 없음 (보고) |
| TAU-13 | **두 면적 모드 모두 1세대 협착식** — 게이트 없이 인계하면 "더 정교한 면적" 이나 물리값으로 오독된다.  hertz: R_c = 1/(2σa) 반공간 Maxwell (`network_conductivity.py:406–408` 주석 "Exact for point-contact-on-halfspace geometry" · :421 · :453–454).  평균 a/r_SE 0.44 · 0.41 · 0.33 · 0.30 (φ 띠 높음 → 낮음) 에서 리포 기준해 대비 R_c × ≈ 0.41–0.58 → **1.7–2.4 배 과대** — 기준해 = 곱 배치 ψ = (1 − a/r)^1.5, 축대칭 flux-tube 유한체적 `scripts/constriction_reference.py` (`:428–442` 주석 · `AREA-09`).  physics: ψ 분모 (`:444`, `L2-01`) · 접촉별 상한값 면적 (`plastic_coverage.py:374–395`, `LHS-25`) · ψ 절벽 (`:445–452`) · a_eff 클램프 (`:425`) (물리 a4 · b8) | (봉인) `network_conductivity.py:406–454` · `plastic_coverage.py:374–395` | 코드 수정 없음 — 인계 메타 `ion_net_constriction` (`maxwell_halfspace` / `mikic_psi_divide`) · `ion_net_psi = legacy_divide` · **두 모드 모두 물리 타깃 HOLD** · S3 판정 + 순수 SE 게이트 뒤 재계산 | hertz · physics 열 머리에 "1세대 (반공간 Holm / ψ 분모)" |

### P2
| ID | 결함 | file:line | 시험 먼저 → 최소 수정 | 웹앱 짝 |
|---|---|---|---|---|
| TAU-04 | 기공 τ 가 ML `tau_se` 로 | `ml_cycle_surrogate.py:28` · 86 · `train_cycle_surrogate.py:223` | `build_matrix` 시험: pore.tau None · trackb tau_full X → `tau2_ion_vox` = X → 특징 이름 교체 (`tau2_pore_void_vox` 는 구조 축으로 따로) | 웹앱 화면 없음 (보고) |
| TAU-05 | 비관통 침대에 유한 τ_Dij (`DESC-02W`).  **파급 확정** (코드 #34): 비관통-SE 6 침대 (input_2mAh_real_16 · a9_p00/02/06/08/10) 가 σ_e Stage 22.5 필터를 전부 통과한다 — σ_e 타깃 `electronic_sigma_full_mScm_stage_e` 0.46–10.7 · `_EXCLUDED_NAMES_EL` 밖 · φ_AM 0.567–0.608 · τ > 0 (유령 키 → SE τ, a9_p10 17.49).  ⇒ 고치면 σ_e 생 적합의 **비트 불변이 깨진다**.  σ_thermal T1 은 `R_brug_over_full_physics` · `asr_ionic` 결측으로 이미 빠져 무영향 | `dem_analysis_core.py:573` · 586 · 598–605 · `generate_comparison_plots.py:6060–6083` · 6939–6970 | 합성: 위 띠만 닿는 성분 → None (지금 유한) · σ_ionic T1 LOOCV 비트 불변 확인 (T1 은 f_p > 0 행만) → 폴백 삭제 + 상태 · σ_e 는 **결정 12 (동결)** | τ 블록 "— (미관통)" · 예측기 None 처리 |
| TAU-06 | 유령 `tortuosity_electronic_*` · `tau_lap_eff` (σ_e 의 C(τ) 가 조용히 SE 이온 τ · 경고 영영 안 뜸) | `generate_comparison_plots.py:6067–6069` · 6480 · `generate_fitting_report.py:675` · `app.py:2892–2915` · `refresh_warnings.py:76–95` · `electronic_nested_cv.py:187–191` | Stage 22.5 계수 비트 불변 시험 → 죽은 키 제거 · 보고서 문구 "σ_e 의 C(τ) 는 SE 이온 기하 τ" · 경고는 계산된 T 로 (또는 삭제).  `TAU-23` 과 한 묶음 | 경고 배지 |
| TAU-07 | τ_Lap,geom ('geom' 오명 · T < 1 가능) + **CF 의 지위**: "CONTACT_FREE — upper bound, ideal contact limit" 은 이 모델의 σ 상한일 뿐 물리적 이상 접촉 극한이 아니다 (물리 f1) | `app.py:1946` · 2138–2139 · 2613 · 9545 · `single.html:1837–1841` ("τ_Dij 의 0.8배 · GB") · `grade_engine.py:176–181` (φ^−0.5 — √ 관례면 φ^−0.25) · `export_comsol_2d.py:106–107` · `docs/literature_review_dem_mpm_assb.md:106` · taufactor 카드 §(2) · CLAUDE.md CL-81 절 | 곧은 사슬 시험 T_CF = (4/3)r d N(N−1)/L² (기록용) → 이름 "τ (flux · 접촉 저항 0 · 모델 내부 기준선 — 부피 비보존 bulk)" · 인계 안 함 · 복셀 ÷ 접촉망 대조 계획에 CF 과전도 (× 1/(0.6–0.8)) 사전등록 (결정 11) | 같은 묶음 |
| TAU-08 | "Constriction overhead" 섞인 비 · 같은 망 FULL/CF 도 원기둥 bulk 때문에 "순수 협착" 이 아니다 (T 로 ≈ 1.2–1.4 배 과대) | `app.py:2142–2143` · `single.html:1849–1853` (낡은 "n=56 · 1.76×") · `grade_engine.py:183–190` · 947–953 (분자 Stage-E physics ÷ 분모 raw CF) | 등급 overhead == √(σ_CF/σ_full) 같은 모드 시험 → 협착 비 = 같은 망 τ_FULL/τ_CF, 이름 "모델 내부 협착 비 (원기둥 bulk 기준)" · T_CF · 절벽 간선 비율과 같이 보고 · 물리 협착 배수로 인용 금지 · 웹앱 행 이름 "flux ÷ 기하" | 같은 묶음 |
| TAU-12 | Minnmann 앵커 CSV 낡은 행 | `docs/data/minnmann2021_sigma_tau_porosity.csv:2` · 8–12 | SI Table S2 값으로 교체 (61 vol% 거친 SE 130 · fine 33.8 별행 + "σ₀ 1.6 기준" · σ 전 행) · 인쇄식 Eq 4 문구 정정 | SI 그림은 42 vol% 한 점만 하드코딩 (`plot_tau_regime_si.py:134–136`) — 영향 없음 |
| TAU-14 | 띠 폴백 L1 이 σ · T 값을 바꾼다 (`LHS-17` 증거 추가) | (봉인) `network_conductivity.py:230–247` · `dem_analysis_core.py:505–523` | 인계 게이트: 띠 규칙 L0 일 때만 값 (§5-2 G1) · `ion_net_band_rule` 열 | 웹앱 표에 띠 규칙 표시 |
| TAU-21 (코드 M1) | **웹앱 physics τ 칸이 physics σ 가 없으면 조용히 Hertz 값을 쓴다** (비율 행 `ratio_p` 도) — physics 를 빈칸으로 둔 침대가 화면에서는 physics 값처럼 보인다 (§5-2 G6 과 충돌) | `app.py:2611–2612` · 2745–2746 (`… if sig_full_p and sig_full_p > 0 else tau_lap_eff_h`) | 시험: physics 키 없는 metrics → physics 칸 "—" (지금 Hertz 값) → 대체 분기 삭제 | 같은 파일 (J20-l) |
| TAU-22 (코드 M2) | **비관통이면 `sigma_full_status` 가 'valid_zero' 가 아니라 'not_computed'** — `solve_network` 가 관통 성분이 없으면 (None, None) 을 돌려준다.  docstring 의 "'valid_zero' = 퍼콜 경로 없음" 은 도달 불가 → 상태로 NOT_PERCOLATING 을 판별할 수 없다 | (봉인) `network_conductivity.py:540–576` ↔ `:94–112` · 결과 dict :1164 | 인계 도우미 시험: 위 띠만 닿는 합성 → f = 0 · `NOT_PERCOLATING` (`percolating_fraction == 0` ∧ `calc_percolation`) · sentinel 결함 자체는 원장 등재 후보 — 수정은 다음 재봉인 | 없음 (보고) |
| TAU-24 (코드 M5) | **L0 띠도 띠 노드를 등전위로 묶고 정규화는 판 간격** — 실효 길이가 L 보다 짧아 T 를 ≤ 4r_SE/L 낮춘다 (L1 폴백과 같은 기전, 크기만 작다; 중앙 6 % · p90 12 % · 최대 17 %, 상한 추정) · r_SE/L 에 따라 달라 입경군 간 대조를 비튼다 | (봉인) `network_conductivity.py:225–249` · 620–666 · 853–857 | 메타 `ion_net_band_frac` (= 4r_SE/L) + 한정어 · (선택) L_eff 보정판 병기 — 보정식은 런 전 등록 | 웹앱 표에 띠 두께/L |

### P3
| ID | 결함 | file:line | 수정 | 웹앱 짝 |
|---|---|---|---|---|
| TAU-09 | 망 `active_fraction` (바닥 = 집전체 기준) ↔ `ionic_active_pct` (위 = 분리막 기준) | (봉인) `network_conductivity.py:999–1021` ↔ `dem_analysis_core.py:741–768` | 이온 접근성은 분리막 기준 (Nguyen 방향 논리) — 이온 `active_fraction` 은 소비처 없음 (`NET_MERGE_KEYS` `pipeline_service.py:83–97` 에 전자만) → 열 사전 규칙만 · 이름 정정은 다음 재봉인 | 없음 (보고) |
| TAU-11 | 카드가 Minnmann Eq 4 를 보고값 꼴로만 적음 (인쇄 역수 오식 미표기) · Arzt 카드 L-3 영문 "the per-particle form of Arzt's Eqs. (19)–(21)" 은 과장 (문헌 C5) | 정본 litdb: `bielefeld2020_…:136` · 505 · `interfacial_impedance_formulation_…:173` · `taufactor_…:146` · `arzt1982_…` L-3 / 반대 방향 (인쇄식을 맞는 식처럼): 리포 `docs/lit_minnmann2021_…:147` · CSV :2 | 한 줄 한정어 "(보고값 꼴 · 인쇄 Eq 4 는 σ 비 역수 — minnmann2021 카드 §4.3 · §17 #1)" · Arzt L-3 → "reduces to Arzt's mean-field (isostatic, monosize) Eqs. (19)–(21)" — 카드는 정본 브랜치 커밋 (이번 작업은 COMSOL 쪽 번호만 고쳤다) | — |
| TAU-15 | PyBaMM 휴면 코드: τ → Bruggeman 지수 자리 · porosity = 공극 · 문서 처방 충돌 (`I-11`) | `pybamm_predictor.py:70–72` · `docs/stage4_…:44` ↔ `docs/stage2_…:55` | 삭제 또는 "tortuosity factor" 옵션 + T + φ_SE 로 재작성 · 문서를 T 로 통일 | 호출자 없음 |
| TAU-16 | 등급 문턱 출처 "Tippens 2019, Famprikis 2019" — **Famprikis 카드에 없음** (감사 D #97 은 Famprikis 카드만 대조) · **Tippens 2019 는 미감사 [미확인]** · √ 척도 | `grade_engine.py:14` · 165–167 | "내부 등급선" 표지 · Tippens 원문 확인 전 인용 금지 · T 축 전환 시 문턱 제곱 | 등급 툴팁 |
| TAU-17 | "formation factor" = f (Archie 와 역수) | (봉인) `network_conductivity.py:13–15` · CLAUDE.md:150 | 문서 정정 · docstring 은 다음 재봉인 | — |
| TAU-18 | 덱 τ_wall 분모 "두께" (`LREL-05` 열림) | `docs/report_20261021/build_deck_v2.py:316` · 325 | 원장대로 | — |
| TAU-19 | "τ_Dij,all ≤ τ_Dij" 보장 문구 (`I-17`) | `single.html:1835` · `docs/bruggeman_…:30` | 문구 삭제 (ps45 실측 3.5–4.3 % 작음은 예시로만) | 같은 파일 |
| TAU-20 | σ₀ 출처 라벨 제각각 (`I-15`) | `single.html:1845` · `export_comsol_2d.py:48` · 94–95 | "펠릿값 (Cronau 2021 SI 그림 S2c 하단 · CL-91)" 로 통일 | 같은 묶음 |
| TAU-23 (코드 M4) | **`constriction_dominant` 경고도 죽어 있다** — `constriction_pct` · `constriction_fraction_pct` 생산자 0 (비슷한 `_constriction_pct` 는 그룹 표 전용 지역 키) | `app.py:2903` · `refresh_warnings.py:86` ↔ `app.py:6832` | `TAU-06` 묶음 (협착 서사의 같은 경고) — 키 삭제 또는 같은 망 FULL/CF 로 다시 정의 (TAU-08 이름) | 경고 배지 |
| TAU-25 (코드 M9) | `sigma_full_mScm` 은 소수 6 자리 반올림 — φσ₀/σ_full_mScm 와 φ/`sigma_full` 이 코퍼스에서 최대 0.11 % 다르다 | (봉인) `network_conductivity.py:1156` | 인계 T 는 무차원 `sigma_full` (8 자리) 로 계산 · G4 "비트 동일" 시험 대상 | — |

---

## §5. 망 인계 열 사전 초안 — 이온 먼저 (D4)

### 5-1. 열 (모드 = `hertz` · `physics`, 같은 정의 · 면적과 협착식만 다름)
| 열 | 식 (정확히) | 이름 · 한정어 |
|---|---|---|
| `f_ion_<mode>` | f_mc = σ_ratio × (L_gap/L_mc).  σ_ratio = G_FULL·L_gap/(box_x·box_y) (솔버 무차원 `sigma_full`, 8 자리 — `TAU-25`) · L_gap = 판 간격 · L_mc = 질량 보존 두께 (결정 1) | "유효 전도도 비 (diffusibility · COMSOL f_e · 1/N_M) — **판 간격 해의 질량보존 두께 재척도 (해 아님)**" · σ₀ 수치에 무관 (§3-1) · COMSOL 에는 이 값을 Porous Electrode 보정 **User defined (fl)** 로 (같은 틀 L_mc · φ_mc · 10-04 D1) |
| `f_ion_<mode>_gap` (메타) | σ_ratio 그대로 | "판 간격 기준으로 풀린 값 — φ_mc 와 짝짓지 말 것 (T 를 L_gap/L_mc 배 낮춘다)" |
| `tau2_ion_<mode>` | T = φ_SE,mc / f_ion (= φ_구합·σ₀/σ_full — 현행 웹앱 T 와 **정의상** 같은 수) | "**접촉망 모델 T** (간선 재료 σ₀ 기준 · Holm 협착 포함 (1세대) · 원기둥 bulk · z 관통 conventional) — 문헌 tortuosity factor 와 같은 정의식, 물리 기준 상태는 다름".  COMSOL: "종 수송 인터페이스 Eq 6-6 (p.376) 의 τ_F 와 같은 꼴.  배터리 인터페이스는 **강하게 시사 (strongly implied) — 인쇄 근거 없음** → 사용 버전 GUI Equation 보기 확인 전에는 'COMSOL 입력' 이라 쓰지 않는다.  σ_full 재현은 COMSOL σ₀ = `ion_sigma0_mScm` 일 때만" |
| `tau_ion_<mode>` | τ = √T | "τ² 관례의 τ (Minnmann √τ²) — **COMSOL 입력 아님**" |
| `ion_net_status` | `OK` · `NOT_PERCOLATING` · `BAND_FALLBACK` · `MODEL_BELOW_CONTINUUM_BOUND` · `NOT_COMPUTED` (+ 사유: `solver_guard` · `missing_input` · `temperature_mismatch` · `percolation_disagree`) | 값 규칙 5-2.  ⛔ `SOLVER_ANOMALY` 는 쓰지 않는다 |
| `ion_net_area_mode` | `hertz` = LIGGGHTS c_cpl[22] 기하 교차 원판 π(rδ − δ²/4) (같은 반지름 r · 겹침 δ; `L1-04` — 탄성 πR*δ 의 **(2 − δ/(2r))** 배, "Hertz" 는 이름만) · `physics` = v1 Tabor · 부피 · 기하 cap (`plastic_coverage.py:266–404` — 접촉별 **상한값**, `LHS-25`) | — |
| `ion_net_constriction` | `maxwell_halfspace` (hertz: R_c = 1/(2σa), ψ 없음 — a/r_SE 0.30–0.44 에서 R_c 1.7–2.4 배 과대) · `mikic_psi_divide` (physics: ψ 분모 `L2-01` · ψ < 1e-4 → R_c = 0 절벽) | 두 모드 모두 **1세대** |
| `ion_net_psi` | `legacy_divide` | physics 에만 의미 (`L2-01`) |
| `ion_net_band_rule` · `ion_net_band_frac` | L0 / L1 / L2 · 4r_SE/L (띠 끝 단락에 의한 T 하향의 상한) | L_eff 보정판을 원하면 런 전 등록 |
| `ion_sigma0_mScm` · `ion_sigma0_T_C` | 3.0 · 25 (온도 런이면 `se_material` Arrhenius 값과 그 T) | "σ₀ = 간선 재료 σ = 펠릿값 (Cronau 2021 SI 그림 S2c µC-Li₆PS₅Cl 평탄 하단, `CL-91`) — f 의 기준 · COMSOL σ₀ 칸의 짝" |
| `phi_basis` · `L_basis` | `mass_conserving` · `L_mc` | D3 |

### 5-2. 값 규칙 · 게이트
| 게이트 | 내용 | 실패 시 |
|---|---|---|
| G1 띠 | 솔버 띠 = L0 (입자 자기 반지름 2 배 · 양 끝 ≥ 3).  L1 폴백은 곧은 사슬에서 T 를 21–29 % 낮춘다 (σ 26–40 % 과대, §3-6).  ⚠ L0 자체도 T 를 ≤ 4r_SE/L (중앙 6 % · 최대 17 %) 낮춘다 → 게이트가 아니라 메타 `ion_net_band_frac` + 한정어 (`TAU-24`) | `BAND_FALLBACK` · 셋 다 빈칸 |
| G2 관통 | 솔버 관통 성분 유무 (`percolating_fraction > 0`) == `calc_percolation` `percolation_pct > 0` (같은 띠).  ⛔ `sigma_full_status` 로 판정하지 않는다 — 비관통도 'not_computed' 다 (`TAU-22`) | 불일치 → `NOT_COMPUTED (percolation_disagree)` · 셋 다 빈칸 |
| G3 비관통 | G1 · G2 통과 + 관통 성분 없음 | **f = 0 · T · τ 빈칸 (= ∞)**.  한정어: "이온적으로 죽은 전극으로 읽지 말 것 (`ionic_active_pct` 는 유한, J20-p) · 문턱 근처의 관통 여부는 상자 크기의 실현값 — 재료 성질 아님" |
| G4 온도 짝 | σ₀ 와 σ_full 이 같은 T.  시험: σ_grain 두 값 → T 비트 동일 (landesfeind 카드 §11-③) · 무차원 `sigma_full` 로 계산 (`TAU-25`) | `NOT_COMPUTED (temperature_mismatch)` · 빈칸 |
| G5 연속체 하한 | f > φ (T < 1) → **`MODEL_BELOW_CONTINUUM_BOUND` — 값 유지 + 표지**.  원기둥 bulk · physics 절벽이라는 모델 성질이지 수치 실패가 아니다.  빈칸으로 거르면 코퍼스를 T ≥ 1 쪽으로 선별하게 된다.  수치 관문은 솔버 자신의 것이다: `G_eff > 1.1·Σg` → CG 재시도 → None (`network_conductivity.py:778–818`) · 단상 `sigma_ratio > 1.5` 거부 (`:870–878`).  ⚠ v1 이 인용한 `:846` 은 `NETWORK_DEBUG` 안의 출력뿐이다.  "2·Σg" 를 쓰려면 새 도우미의 **새 규칙**으로 등록한다 (코드 #38 · 물리 f3) | 솔버 관문이 거부하면 `NOT_COMPUTED (solver_guard)` |
| G6 협착 세대 | 두 모드 모두 `ion_net_constriction` 메타.  physics 추가 표지: cap_conflict 비율 (`L1-01`) · 탄성 가지 비율 · ψ 절벽 접촉 수 (a_eff/r_min ≥ s*, R_c → 0) · LHS-25 Λ_i > 1 입자 수 | 값은 싣되 **두 모드 모두 물리 타깃 (실험 절대 대조) HOLD** — 해제 조건 = 결정 4 게이트 + S3 판정 |

### 5-3. 붙일 한정어 (열 사전 문구)
- "flux 기반 · 관통 (두 평행 띠 Dirichlet) **conventional tortuosity factor** (Nguyen Eq 1) — **electrode tortuosity factor τ_e (Nguyen Eq 2) 가 아니다** · 차단 대칭셀 EIS-TLM 의 τ (Landesfeind Eq 13 형 — Nguyen 이 eSCM 으로 분류) 와 **한정어 없이 비교하지 않는다**."
- "COMSOL: 종 수송 인터페이스 Eq 6-6 (p.376) · Tortuosity model 문장 (p.377) 의 τ_F 와 같은 꼴 — 배터리 인터페이스 (Porous Electrode, p.266–267) 는 식이 인쇄돼 있지 않다: **강하게 시사 (strongly implied)** · GUI Equation 보기로 확인 전에는 'COMSOL 입력' 이라 쓰지 않는다 · COMSOL σ₀ 칸 = 3.0 (`ion_sigma0_mScm`) 과 짝일 때만 σ_full 재현.  COMSOL 에 넣을 때는 `f_ion` 을 Porous Electrode 보정 User defined (fl) 칸으로 (배터리 모듈 앱 예제 *Homogenizing a Heterogeneous Electrode Model* 과 같은 방식 · 같은 틀 L_mc · φ_mc) — 이 경로는 τ 관례와 무관."
- "**1세대 협착식** (hertz = 반공간 Maxwell, a/r 0.30–0.44 에서 R_c 과대 · physics = ψ 분모 + 접촉별 상한값 면적 + 절벽) — ML 기술자 전용 · **실험 절대 대조 금지** (순수 SE 게이트 · S3 판정 전)."
- "z 한 축 (Tjaden 식 21 τ_C 와 직접 비교 금지) · 형상 · CBD 차단 없음 · σ₀ 펠릿값 위 Holm 접촉 저항 = 부분 이중계상 (방향 T↑ — 순수 SE 게이트로 크기 확인)."
- "띠 끝 단락 → T 하향 ≤ 4r_SE/L (`ion_net_band_frac`)."
- "φ = 전 SE (비관통 · 고립 포함) — dead 부피가 T 를 키운다 (Nguyen Fig 2: 같은 N_M 에서 −35 %) → **1차 수송량은 f** (재척도 이름표와 함께)."
- 문헌 T 와 맞댈 때: "Minnmann 은 순수 SE 펠릿 τ² ≡ 1 기준 (σ₀ 1.6 mS/cm @25 °C) — 우리 T 는 간선 재료 기준 · 기준을 맞추면 × 0.5–0.7 (외삽 추정, 게이트 전)."
- 인계하지 않는 것: CF 가지 (모델 내부 기준선 · T < 1 가능) · Stage-E σ 로 만든 τ · 기하 τ (이미 `tortuosity_SE_wall` 로 따로 있음).

### 5-4. 전자 · 열 (D4 다음 — 정의 결정 먼저)
| 채널 | 막는 것 | 권고 |
|---|---|---|
| 전자 | σ₀ 가 입자마다 다르다 (`sigma_AM_relative` GB 인자, AM_P < 1) — Track-B 도 같은 경우 τ 를 None 으로 둔다 (`mpm_webapp_payload.py:2488–2505`) · σ_AM 50 mS/cm 는 모델 기준값 (`CL-92`) | 단일 σ₀ = σ_AM,input 기준 f · T 를 정의하고 GB 인자를 T 에 흡수한다고 명시 — 또는 f 만 |
| 열 | 다상 (AM–AM · AM–SE · SE–SE) · k_weight 가지가 옛 코퍼스에서 실행 안 됨 (`CL-12`) | φ = 전 고체 · k₀ 정의 결정 뒤, 세대 표지 |

---

## §6. LHS-25 · LHS-26 닫기 설계 (v1 §6 전면 개정)

### 6-1. "기하 원판의 약 3 배" 의 기준 — 겹침 (교차) 원
- 그 "기하 원판" = LIGGGHTS `c_cpl[22]` = 두 구의 **기하 교차 원판** (같은 반지름이면 π(rδ − δ²/4)) — `parse_liggghts.py:51–56`.
  - `L1-04`: A_LIGG/A_Hertz = **2 − δ/(2r)** (δ = 겹침).  r 0.5 µm · δ/R* 0.05 에서 1.9875 배.
  - ⚠ v1 은 "2 − d/(2r)" 로 적었다.  §3-6 의 d (중심 간격) 로 읽으면 1.0125 다 — 코드 #22 틀림, `parse_liggghts.py:53` 주석의 d (겹침 뜻) 를 그대로 옮긴 것이다.  v2 는 겹침을 δ 로만 쓴다.
  - 망의 "Hertz" 모드도 이 면적을 쓴다 (`network_conductivity.py:303` · 353).
- "≈ 3 배" 의 출처 = 비포화 LHS 침대의 physics v1 ÷ Hertz-geom 피복률 비 — **침대 합의 비**이지 접촉별 비가 아니다.  AM_P 2.364–3.373 (중앙 2.958) · AM_S 2.459–3.974 (3.203) (`docs/reviews/lhs_coverage_reasonableness_20261001.md:189` · :246).
- Arzt 대조 (우리 산술 · 단분산 · 방향 참고):
  - 압밀 한계 초기 접촉은 겹침 원의 1.27–1.40 배 (D 0.84–0.90, 식 (3) · (8) · (A7) — 문헌 C7).
  - 근거리 (소결) 극한 a(r=1) = 11(1 − 1/R′) 은 겹침 원의 1.85 · 1.87 배 (D 0.90 · 0.95) 다.  각주: (A9) 의 1/R′² 정규화 판 겹침 원 π(1 − 1/R′²) 기준이고, 정규화 없이 π(R′² − 1) 기준이면 1.47 · 1.43 이다 (문헌 C8).
  - Arzt 는 이것을 "upper bound for the contact areas" (p.1886) 라 부른다.  그러나 그것은 **두 재분배 극한 사이 · 단분산 모형 안**의 상한이다 (문헌 C6).
  - Tabor 3 배는 그 상한도 ≈ 1.6 배 넘는다.

### 6-2. 접촉별 진단 — 뿌리는 합보다 앞에 있다 (물리 e3)
| 항목 | 내용 | 출처 |
|---|---|---|
| 추정량 구조 | A_physics = max(하한, min(F_real/H, V/h_min, 2πR_min²)) (`plastic_coverage.py:374–395`) — 상한들이 하한보다 크면 **상한값 자체**를 돌려준다 | 코드 · 물리 e3 |
| F_real/H 의 지위 | F_real = (4/3)·E*_real·√R*·δ^1.5, E* 22.415 GPa (AM–SE 값, SE–SE 에도 씀 — `L1-03`) · H 0.85 GPa · δ = 연화 E (SE 1.35 GPa) 로 생긴 DEM 겹침 (`:35–46` · 349–352).  완전소성 영역에서만 정당한 **느슨한 상한**이다 (같은 간섭에서 탄소성 힘 ≤ 탄성 힘, p_m ≈ H) — 추정치가 아니다.  코드 자신의 항복 개시 δ/R* 0.0011 (`plastic_coverage.py:58`) 의 수십–수백 배 간섭이다 | 코드 #20 · 물리 e3 · g1 |
| 크기 | A_tabor/A_overlap = (2/(3π))(E*/H)√(δ/R*) ≈ **5.6√(δ/R*)** → δ/R* > 0.032 이면 겹침 원을 넘는다.  부피 보존 소성 면적 (Arzt 압밀 한계 1.27–1.40 × 겹침 원 · `storakers1997_…` 카드 ≈ 1.4 ×) 과 비교하면, 연화 DEM 의 전형 겹침 δ/R* 0.15–0.45 에서 **≈ 1.5–3 배** | 물리 e3 (우리 산술) |
| cap 결합 | 부피 캡 결합 **0 %** (모든 φ 띠) → 사실상 "Tabor 를 2πR_min² 로 자른 것".  결합 비율 중앙: φ ≥ 0.55 geom 15.8 · tabor 80.8 % (AM–SE geom 26.4 %) · φ 0.29–0.37 geom 4.8 · tabor 84.6 % (AM–SE 18.0 %) | 물리 재계산 기록 (`A_binding_share_*`) |
| 함의 | 포화하지 않은 입자도 접촉별 면적이 이미 부풀어 있다 → 합 예산 (안 A) 은 **상한들의 합을 다시 자를 뿐**이다 | 물리 e3 |

### 6-3. 합 단계 진단 — v1 수치 철회 (물리 e2 · 코드 #23 · 문헌 C5)
- **Love–Weber 항등식** Σ_j F_ij = 4πR_i²·p̄_i (가지 길이 ≈ R_i) 은 F 가 **평형 접촉력**일 때만 선다 (보정 셋: 가지 길이 R − δ/2 · 접선력 · LIGGGHTS 원자 응력의 비리얼 반분 — arzt 카드 L-3).
  - Arzt (19)–(21) 은 이 항등식의 **등방 · 단분산 평균장 판**일 뿐이다: (19) f/a = 3σ_f + (21) ⇒ Z·a = 4πR²(p/D)/(3σ_f) (R = 1).
  - **입자별 판은 Arzt 에서 나오지 않고 Love–Weber 가 필요하다.**  (20) 자체가 Molerus 의 등방 평균장 결과이고, die 압밀에는 국소압으로 바꾸라는 단서가 붙어 있다.
  - 평균장 Σ A_tabor/(4πR²) ≈ 0.3/(0.85·D) = 0.35–0.42 (D 0.84–1.0, 문헌 C5 확인).
- 코드의 F 는 평형 힘이 아니라 **실제 E 로 다시 만든 힘**이다 → Σ_j A_tabor,ij/(4πR_i²) = κ_i·p̄_i,DEM/H, κ_i = ΣF_real/ΣF_DEM.
- ⛔ **v1 수치 철회**: "κ ≈ E*_real/E*_DEM ≈ 15 (AM–SE) · 30 (SE–SE) ⇒ 포화 문턱 30–60 MPa ⇒ SE 많은 침대에서 일반적이어야" 와 곁가지 "F_DEM 이면 A_tabor ≈ 0.1–0.2 × 원판 → 원판으로 접힌다".  이유는 셋이다.
  - ① 생산 접촉법칙은 Hertz 가 아니라 **hooke/hysteresis** 다 (`pair_style … hooke/hysteresis` 40 덱 · `dem_perturbation.py:62`).  F_DEM = k_n·δ (선형) 이라 κ ∝ √δ/k_n 은 **δ 의존**이고 E* 비가 아니다.  덱 `youngsModulus peratomtype 1.4e8 1.4e8 0.135e7` (14 덱) ⇒ AM 140 GPa · SE 1.35 GPa (덱 단위) — v1 의 "AM 모듈러스 [미확인]" 은 풀렸다 (코드 #23).
  - ② 힘 평형 산술: SE–SE (R 0.5 µm · Z 6.5 · p̄ 0.2–0.36 GPa · δ/R 0.15–0.30) 에서 **κ ≈ 2–9** · A(F_eq)/원판 ≈ 0.5–1.8 (물리 e2 · 일회성 산술).
  - ③ κ 가 15–30 이면 전형 접촉에서 A_tabor 가 2πR_min² 캡을 1.5–2.6 배 넘어 대부분 geom 캡에 걸려야 한다.  그러나 코퍼스 geom 결합은 5–16 % (전체) · 16–26 % (AM–SE), tabor 결합은 68–85 % 다.
- ⇒ 포화 문턱 p̄ ≈ H/κ ≈ 0.1–0.5 GPa — 입자 평균 응력과 같은 자릿수다.  **H0 (응력 꼬리) 와 H1 (κ) 은 미리 가를 수 없고**, C1 실측으로만 보인다.  F_DEM 판도 원판으로 "접히지" 않는다.

### 6-4. 처방 후보 — 사전등록 결정으로 (권고는 절차만, 결정 9)
**(가) 접촉별 추정량** — C0/C1 전에 역학 전제로 등록한다 (물리 e3 · g1):

| 판 | 식 | 전제 | 지위 |
|---|---|---|---|
| E1 (현행) | F_real/H | 실제 E 로 다시 만든 탄성 힘 · 완전소성 p_m ≈ H | **느슨한 상한** — "physics (상한값)" 표지로만 |
| E2 | c²·A_overlap (부피 보존) | DEM 겹침 = 소성 변형의 대리 (frame[2] 연화 인식론) | 추정치.  c² 는 런 전에 고정한다 (Arzt 압밀 한계 1.27–1.40 at D 0.84–0.90 · Storåkers ≈ 1.4 — 출처 선택 자체가 결정) |
| E3 | F_DEM/H | DEM 힘 = 평형 하중 · 겹침은 연화 인공물 | **하한** (단일 접촉 p_m ≤ H 이므로 A ≥ F/H).  ⚠ 다중접촉 정수압 구속에서는 접촉압이 H 를 넘을 수 있다 (물리 e4) — 그 영역에서는 하한이 아니다 |

- 권고 (절차): E2 · E3 를 **둘 다** 계산하고 E1 은 상한으로 병기한다.
- 결론은 E2 · E3 가 같은 쪽일 때만 쓴다.  갈리면 사유를 적고 1저자가 판정한다.
- ⛔ 기대 추세를 재현하는 판을 고르지 않는다.

**(나) 합 단계 상한**:

| | 안 B — 라게르 면 상한 | 안 A — 입자별 표면 예산 |
|---|---|---|
| 규칙 | A_ij ≤ A_face,ij (radical plane 면 다각형) · 강한 판 = 원판 ∩ 다각형 | Λ_i = Σ_j A_ij^raw/(β_i·4πR_i²) · s_i = min(1, 1/Λ_i) · A_ij ← A_ij^raw·min(s_i, s_j) |
| 근거 | **Arzt p.1885 각주** ("the faces of the Voronoi polyhedra contain all the contact areas") · Fig. 5 ▲ (TKD 평균 접촉면) · impingement = 접촉면끼리의 충돌 → 이 기전.  다분산 일반화는 우리 가정 | **Nisar 2024 식 (22)–(25) 의 수치 장치** (평균장 난간, arzt 카드 경유) — 소성 접촉역학이 아니다.  Arzt 식 (7) · (A4)–(A6) 은 재분배용 **자유표면 회계**이지 접촉면 상한이 아니다 (D = 1 에서도 S/4πR′² = 0.41 → Arzt 안에서 한 번도 걸리지 않음).  "근거" 가 아니라 "유추" (문헌 C3 · 물리 e4) |
| 쓰임 (권고) | 합 상한의 기본 | **강체 AM 의 안전 난간으로만**: β_AM = 1 (강체 표면은 늘지 않아 정확) — 원판이 아니라 **구관 면적으로 회계** (식 A4–A5 꼴, 물리 e5).  조각 겹침은 안 B 에서 |
| β_SE | — | **{1.0, 1.10} 철회** (물리 e6).  1.10 (같은 부피 TKD) · 1.034–1.054 (Arzt 전밀도 합) 은 단분산 · 등축 셀 · 전밀도 값이다.  12:4:1 의 작은 연질 SE 가 막처럼 납작해지면 표면이 1.1 배를 쉽게 넘는다 (종횡비 1:3 원판 ≈ 2 배, 우리 산술).  SE 에 쓰려면 물리 유도 (예: MPM real_14 변형 SE 표면/구 표면 분포) 또는 **1.0–2.0 감도를 런 전 등록**한다 — 1.10 을 "물리 상한" 이라 부르지 않는다 |
| 약점 | 재배열 큰 저밀도에서 느슨 · 리포에 라게르 도구 없음 (`git grep` 0 · pyvoro 미설치, 코드 #40) | F 를 둔 채 A 만 s_i 배로 줄이면 implied 압력 F/A = H/s_i > H → Tabor 조건 자체가 깨진다 → **implied 압력 기록 필수** |

### 6-5. 사전등록 검사 (결과 보기 전 등록 · 판정선 수치는 1저자 비준 뒤)
| 검사 | 무엇 | 쓰임 |
|---|---|---|
| C0 | 130 + 64 + ps45 의 접촉 덤프로 A_physics (E1 · E2 · E3 세 판) 재계산 → 상별 Λ_i 분포 · Λ > 1 입자 비율 · "침대 포화 ⇔ AM Λ > 1" | 진단 — 포화 침대 전부가 Λ > 1 입자를 가져야 한다 (아니면 다른 원인) |
| C1 | AM 마다 κ_i = ΣF_real/ΣF_DEM · p̄_i,DEM = ΣF_DEM/(4πR_i²) · 항등식 Λ_i(tabor) = κ_i·p̄_i/H 의 수치 확인.  원자 응력 말고 접촉 목록을 쓴다 (비리얼 반분 주의).  c_cpl[13–15] 힘을 덱 단위계로 일관 환산한다 (`DESC-03` 길이 · 두께 혼용).  가지 길이 보정 크기 δ̄/2R 를 병기한다 (물리 e1) | **진단 전용** — H0 (p̄_i > H) vs H1 (κ_i·p̄_i > H) 중 포화를 설명하는 쪽을 보고만 한다.  ⛔ 힘 정의 (E1/E2/E3) 선택에 쓰지 않는다 |
| C2 | 합 상한 적용 판 (B, 또는 AM 의 A 난간): AM 피복률 ≤ 100 % 구성상 (194/194 assert) · `budget_below_lower` 수 · 부피 보존 면적 대비 비 · implied 압력 F/A (A 난간이면) · Λ ≤ 1 만 있는 침대 비트 불변 | **채택 기준 = 이 물리 검사뿐**.  v2 분모 붕괴 18 침대 회복 · ρ(피복률, SE/고체) 부호 = **보고 전용** (물리 g2) |
| C3 | 망 physics σ (전/후) — ψ 배치 고정 (legacy) | 보고만 (`L2-01` 과 얽힘: 면적을 줄이면 ψ 벌점이 줄어 σ 가 **오를** 수 있다) |
| C4 | E2 ↔ E3 판이 침대 순위를 바꾸는지 (순위 상관 문턱은 런 전 등록) | 바뀌는 침대는 결론 보류 + 1저자 판정 |

### 6-6. 코드 자리
| 자리 | 봉인 | 할 일 |
|---|---|---|
| `scripts/coverage_physics_vs_hertzian.py` (AM–SE physics 누적 ≈ :480–560) | 아님 | E2 · E3 판 + 안 B/A 패스 (새 함수 · 시험 먼저) |
| `scripts/plastic_coverage.py:266–404` (접촉별 면적) | **봉인** (수정 = 재봉인 강제) | 건드리지 않음 — 새 판은 봉인 밖 래퍼에서 |
| `scripts/network_conductivity.py:303–353` (간선 면적) | **봉인** | 봉인 밖 래퍼에서 간선 사후 패스, 또는 다음 재봉인 |
| 웹앱 physics 피복률 · 망 physics 열 · 툴팁 | — | 같은 정의 · 이름 ("physics (상한값)") (J20-l) |

### 6-7. 1저자 결정으로 남기는 것
- ① 접촉별 추정량 전제 (E2 · E3 · c² 출처).
- ② 합 상한 (B · A 난간의 범위).
- ③ β_SE (A 를 SE 에 쓸 때만 — 유도 또는 1.0–2.0 감도).
- ④ C4 문턱.
- ⑤ "physics (상한값)" 개명 시점 (숫자 불변이라 즉시 가능).
- ⑥ `LHS-25` 원장 문구 정정 (아래).
- 원장 문구 정정 제안 (`LHS-25`, 1저자 비준 뒤 원장 수정):
  - 현 문구: "접촉마다 추정한 소성 면적 (Tabor F/H · SE 경도 0.85 GPa — 기하 원판의 약 3 배) 을 표면 한도 없이 더한다".
  - 제안: "접촉마다 **상한값** (F_real/H — 실제 E 로 다시 만든 힘, 부피 보존 소성 면적의 ≈ 1.5–3 배) 을 추정치로 쓰고, 그 합에 표면 한도가 없다".

### 6-8. LHS-26 — 모양 인자를 설계 상에서 (v1 그대로 · 코드 #39 확인)
- 지금은 rough 피복률 `sf = SHAPE_FACTOR.get(lbl)` (`coverage_physics_vs_hertzian.py:534`; AM_P 1.40 · AM_S 1.10 `dem_analysis_core.py:26–30`) 의 lbl 이 `type_map_resolve.py:134` 의 반지름 규칙에서 온다.
  - 규칙: 총칭 `${r_AM}` → r > 0.004 sim (`AM_P_RADIUS_CUT_SIM`, :48) → AM_P.
  - 결과: mono_AM_P 인데 r ≤ 4 µm 인 9 침대가 1.10 을 받는다 — lhs00_118 (3.0) · 121 (4.0) · 124 (3.0) · 125 (3.5) · 126 (2.5) · lhsx_003 (3.17) · 017 (2.80) · 048 (2.72) · 062 (3.80) µm.
- 수정: 설계 CSV 의 `block` (mono_AM_P / mono_AM_S / bimodal — `lhs_design_dataset.py:365`) 을 상 이름의 정본으로 넘기는 명시 덮어쓰기 (`phase_override`) 를 둔다.  반지름 규칙은 덱이 총칭 변수일 때의 진단으로만 쓴다.
  - 시험 먼저: 위 9 침대 → 1.40 (지금 1.10).
  - ps45 는 r_AM_P 4.5 · r_AM_S 2.0 µm 라 규칙과 설계가 같다 (`ps45_handover.csv`).
- 남는 것: 1.40 / 1.10 값 자체의 출처 (B3) 는 이 카드들에 없다 [미확인] → rough 는 인계 제외 유지 (J20-m).

---

## §7. τ_e 공백 (v1 §7 개정 — 물리 d1)

| 항목 | 내용 |
|---|---|
| 리포 상태 | **electrode tortuosity factor 경로가 없다**: 접촉망은 양 끝 띠 Dirichlet 관통형 (`network_conductivity.py:225–249` · 590–593) · STEP3 도 관통형 (`step3_sigma.py:835–840`) · TauFactor mode 6 대응 없음 (nguyen 카드 판정) |
| 인계에 문제인가 | **ML 구조 기술자로서는 아니다** — T 는 conventional τ 로 정의가 닫혀 있고 한정어로 충분하다 (§5-3).  **P2D/COMSOL 매개변수로는 문제다** — Nguyen: "the electrode tortuosity factor τe should be preferred over the conventional tortuosity factor τ during the parametrization step" (p5) · "τe should be used in conventional P2D Newman models instead of τ" (p7) · "eSCM should be preferred over eRDM" (p8).  ⇒ "인계 비차단" 은 ML 기술자 문장으로만 쓰고, P2D 입력 열에는 "부호 불정" 한정어를 단다 |
| 위상 dead-end (배포 v1.1 `top_reachable_pct − percolation_pct`) | LHS 106 관통 침대: 중앙 0.03 % · **p90 2.86 %** · 최대 10.98 % · lhsx 64: ≤ 0.044 %.  상위 10 % 는 Nguyen 구 충전 A 의 dead-end 4 % 수준이다 (Fig 5: 4 · 8 % → τ_e/τ +0.8 · +3.9 %) |
| 0.03 % 를 근거로 쓰지 않는 이유 | ① 위상 dead-end 는 flux dead-end (최대 flux 의 2 % 문턱, Nguyen p4 · Fig 5) 의 **느슨한 하한**이다 — Holm 이 지배하는 망 (T_FULL/T_CF 중앙 ≈ 4 · 접촉 반경이 자릿수로 퍼짐) 에서는 위상상 관통이어도 flux 가 2 % 미만인 가지가 많을 수 있다 ② τ_e = T 에는 dead-end 가 없을 뿐 아니라 **z 방향 균질 (TLM 균질화)** 도 필요하다 — 침대 두께 ÷ 가장 큰 AM 지름 중앙 4.7 (최소 1.3 · 최대 39 · L 15–184 µm, case_master) · 벽 · 판 근처 층 · A7 구배.  Nguyen 자신도 5 µm 구 침대의 TLM 이탈을 대표성 부족 신호로 읽었다 ③ ASSB 의 sink 는 AM–SE 접촉면이다 → LHS-25 로 부푼 physics 면적에 의존한다 ④ ASSB 경계조건 (이중층 = AM–SE 접촉만) 이 액체와 다르다 (nguyen 카드 ⑥) |
| 관통 침대의 비관통 SE 몫 (100 − percolation_pct) | 중앙 0.27 % · p90 10.2 % (하위 분위 규약; 보간 규약이면 0.283 · 10.72 — 코드 #41) · 최대 56.8 % — 그만큼 φ 가 T 를 부풀린다 (f 는 무관) |
| 차이가 큰 집합 | 비관통 24 침대 (T = ∞ 인데 τ_e 는 유한) |
| **추가 솔브 없이 할 수 있는 진단** | flux 기준 dead-end: FULL 해의 전위 · 간선 전류는 이미 나온다 — `solve_network(…, return_field=True)` (`network_conductivity.py:516`) · `dump_raw_dir` 가 쓰는 필드 (`:1104–1107`).  Nguyen 문턱 (최대 flux 의 2 %) 로 세면 된다.  같은 묶음에서 z 단면별 SE 컨덕턴스 · AM–SE 면적 분포를 낸다 |
| 최소안 (후속 · 미구현 · 미검증) | SE 망 + AM–SE 접촉을 축전 sink 로 (ω → 0 극한 = 접촉 면적 비례 균일 sink) · AM 등전위 (σ_e ≫ σ_ion 가정 — 저 CAM 에서 깨짐, Minnmann τ_el² 120 @25 vol%) · 분리막 쪽 띠 Dirichlet · 집전체 쪽 차단 → 희소 솔브 1 회 → R_eff → R_ion = 3·R_eff (Nguyen Eq 5) → τ_e = ε·R_ion·A·σ₀/L.  sink 가중이 접촉 면적이므로 **LHS-25 가 먼저** 닫혀야 한다.  실험 앵커도 둘로 갈린다: Bazzoun (완전 차단 대칭셀 → eSCM 형) ↔ Minnmann (전자 차단 + 양단 Li-In → 관통형) [판독] |

---

## §8. 더 볼 문헌 — 최종 요청 목록 (중복 제거 · 상위 10 먼저)

- 서지는 **원 참고문헌 목록의 문자열 그대로**다.  문헌 리뷰가 목록 원문과 글자 그대로임을 확인했다 (E1–E9).  [35] Ender 2011 은 Landesfeind PDF 참고문헌 목록에서 v2 가 다시 확인했다.
- **OA**: 7 카드 어디에도 요청 서지의 OA 여부가 적혀 있지 않다 → 전 행 "카드 기록 없음".  카드에 OA 가 적힌 것은 카드 자신의 논문뿐이다 (Arzt CC BY-NC-ND · Landesfeind CC BY-NC-ND 4.0 · Minnmann CC BY 4.0 · Nguyen CC BY 4.0 · TauFactor CC BY · Tjaden CC BY 4.0) — 요청 목록에는 없다.
- 정본 카드 유무: 아래 서지는 정본 `litdb/papers/` 에 카드가 없다 (파일 목록 대조).

### 8-1. 상위 10
| 순위 | 서지 (원 목록 그대로) | 출처 목록 | 왜 필요한가 | 닫는 열린 항목 | OA |
|---|---|---|---|---|---|
| 1 | H. F. Fischmeister, E. Arzt and L. R. Olsson, Powder Metall. 21, 179 (1978). | arzt [3] | 압분 bronze 의 배위수 · 접촉면적 **실측** (impingement 구간 D ≈ 0.97 까지, Arzt Fig 4 ● · Fig 5 □).  [8] "H. F. Fischmeister and E. Arzt, Powder Metall. To be published." 의 가장 가까운 대체다 ([8] 출판 서지 [미확인] — 찾으면 1순위).  ⚠ 금속 분말 → 황화물 이전에는 한정어 | 결정 9 · §6-4: E2 의 c² · 안 B 면 상한의 실측 대조 | 카드 기록 없음 |
| 2 | [13] Holzer L, Wiedenmann D, Münch B, et al. The influence of constrictivity on the effective transport properties of porous layers in electrolysis and fuel cells. J Mater Sci. 2013;48(7):2934–2952. | tjaden [13] (= landesfeind [6]) | τ_eff ↔ τ_geo 엄격 구분 + 협착 β — FULL / CF / 기하 분해의 문헌 틀 | 결정 11 · TAU-07 · TAU-08 (협착 비의 이름 · 정의) · §3-5 | 카드 기록 없음 |
| 3 | c) L. Froboese, J. F. v. d. Sichel, T. Loellhoeffel, L. Helmers, A. Kwade, J. Electrochem. Soc. 2019, 166, A318 | park [18c] | ASSB 전극 미세구조 ↔ 이온전도도 실측 (famprikis2019 카드 ref 75 가 같은 논문을 "tortuosity/미세구조↔σ 실측 원전" 으로 적음) — 입경비 가설의 실험 쪽 검정.  Park σ₀ 조성식 (Table S1 각주 b "literature[18a-c]") 출처의 **후보 중 하나** (특정 아님, 문헌 E6) | 결론 ④ · §3-8 ① · §3-4 (Park σ₀) | 카드 기록 없음 |
| 4 | Landesfeind, J., Ebner, M., Eldiven, A., Wood, V. & Gasteiger, H. A. Tortuosity of battery electrodes: validation of impedance-derived values and critical comparison with 3D tomography. J. Electrochem. Soc. 165, A469–A476 (2018). | nguyen ref 29 (= minnmann [61] · landesfeind §14) | 같은 전극의 임피던스 τ ↔ 단층촬영 τ — 정의 · 방법 차이의 실측 크기.  Minnmann 의 "LIB tortuosity factor 는 한 자릿수 낮다" (p.9) 근거 — τ² 척도인지 τ 척도인지 확인 | 결정 13 · §7 (τ_e ↔ conventional) | 카드 기록 없음 |
| 5 | [12] a) J. Park, D. Kim, W. A. Appiah, J. Song, K. T. Bae, K. T. Lee, J. Oh, J. Y. Kim, Y.-G. Lee, M.-H. Ryou, Y. M. Lee, Energy Storage Mater. 2019, 19, 124; b) J. Park, J. Y. Kim, D. O. Shin, J. Oh, J. Kim, M. J. Lee, Y.-G. Lee, M.-H. Ryou, Y. M. Lee, Chem. Eng. J. 2020, 391, 123528. | park [12] | Park Fig S9 식 · 경계조건의 인용원 — ASSB 디지털트윈 τ 의 산출법 · σ₀ 규약 (역산 대신 원값) | §3-4 (Park T 의 σ₀ 의존 · 추세 전용 한정어) | 카드 기록 없음 |
| 6 | [43] D. Hlushkou, A. E. Reising, N. Kaiser, S. Spannenberger, S. Schlabach, Y. Kato, B. Roling, and U. Tallarek, J. Power Sources, 396, 363 (2018). | minnmann [43] | Minnmann 이 ASSB tortuosity (PDF p.5) · 기공 13–17 % 비교 문헌 (p.9) 으로 인용 — 미세구조 기반 ASSB τ 의 두 번째 절대 앵커 후보 (내용 [미확인]) | 결정 4 뒤의 절대 대조 | 카드 기록 없음 |
| 7 | [32] Z. Siroma, N. Fujiwara, S. Yamazaki, M. Asahi, T. Nagai, and T. Ioroi, Electrochim. Acta, 160, 313 (2015). | minnmann [32] | Minnmann TLM 식 [1] 의 원전 — Minnmann 의 R_ion 이 무엇을 포함하는지 (입계 · 접촉) 확인 → 기준 상태 대응 | 결정 4 · §3-2 | 카드 기록 없음 |
| 8 | [25] N. Kaiser, S. Spannenberger, M. Schmitt, M. Cronau, Y. Kato, and B. Roling, J. Power Sources, 396, 175 (2018). | minnmann [25] | 임피던스 → ASSB 유효 이온전도도 · tortuosity 선행 — 같은 축의 두 번째 실험 경로 | §3 절대 대조 (게이트 뒤) | 카드 기록 없음 |
| 9 | 35. M. Ender, J. Joos, T. Carraro, and E. Ivers-Tiffée, Electrochem. commun., 13, 166 (2011). | landesfeind ref 35 (PDF 목록 — 카드 표에 없음) | Landesfeind 가 "numerical simulation of the Laplace equation as discussed, e.g., in Ender et al." 로 인용하는 자리 (A1374) — 복셀 Laplace N_M (STEP3 계열).  ⚠ v1 의 [34] (JES 159 A972, 2012) 는 FIB-SEM 재구성 인용 (A1375) 이다 (문헌 E7) | 결정 11 (CL-81 복셀 ÷ 접촉망 대조의 선례) | 카드 기록 없음 |
| 10 | Pouraghajan, F. et al. Quantifying tortuosity of porous Li-ion battery electrodes: comparing polarization-interrupt and blocking-electrolyte methods. J. Electrochem. Soc. 165, 2644–2653 (2018). | nguyen ref 20 | eRDM vs eSCM **실측** 비교 + 접촉저항 · R_ct 를 넣은 일반 TLM | 결정 13 · §7 최소안 | 카드 기록 없음 |

### 8-2. 2순위 (중복 제거)
| 서지 (원 목록 그대로) | 출처 | 왜 | 닫는 항목 |
|---|---|---|---|
| Malifarge, S., Delobel, B. & Delacourt, C. Determination of tortuosity using impedance spectra analysis of symmetric cell. J. Electrochem. Soc. 164, E3329–E3334 (2017). | nguyen ref 18 | 전자 저항 임의값 대칭셀 TLM — ASSB 에서 r_el ≪ r_ion 이 안 설 때 | §7 |
| Cooper, S. J., Bertei, A., Finegan, D. P. & Brandon, N. P. Simulated impedance of diffusion in porous media. Electrochim. Acta 251, 681–689 (2017). | nguyen ref 42 | 망 임피던스 (τ_e) 구현 참고 | §7 최소안 |
| [14] Wiedenmann D, Keller L, Holzer L, et al. Three-dimensional pore structure and ion conductivity of porous ceramic diaphragms. AIChE J. 2013;59(5):1446–1457. | tjaden [14] (= landesfeind [10]) | Landesfeind Eq 4 (N_M ≡ τ̄_geo/(εβ)) 원식 — τ_geo 지수 [미확인] 닫기 | §3-5 |
| [63] Cooper SJ, Eastwood DS, Gelb J, et al. Image based modelling of microstructural heterogeneity in LiFePO4 electrodes for Li-ion batteries. J Power Sour. 2014;247:1033–1039. | tjaden [63] (= landesfeind [12]) | 같은 시료 κ_geo vs κ_flux (Tjaden 식 21–22 원출처) | §3-5 한정어 |
| O. Molerus, Powder Technol. 12, 259 (1975). | arzt [14] | 힘 ↔ 외부압 f = 4πp/(ZD) — Arzt (20) 평균장의 원전 | §6-3 · C1 |
| A. K. Kakar and A. C. D. Chaklader, J. appl. Phys. 38, 3223 (1967). · P. J. James, Powder Metall. 20, 199 (1977). | arzt [18] · [19] | 압분 (Pb · Cu · Zn · Al) 접촉면적 실측 — 1 순위의 보조 | 결정 9 · E2 c² |
| [33] Y. Kato, S. Shiotani, K. Morita, K. Suzuki, M. Hirayama, and R. Kanno, The journal of physical chemistry letters, 9, 607 (2018). | minnmann [33] | EIS 와 독립인 사이클 기반 τ | 절대 대조 교차 |
| [34] M. Ender, J. Joos, T. Carraro, and E. Ivers-Tiffee, J. Electrochem. Soc., 159, A972 (2012). | landesfeind [34] | FIB-SEM 재구성 (A1375) — 영상 기반 N_M 의 데이터 쪽 | 결정 11 보조 |
| [27] T. Asano, S. Yubuchi, A. Sakuda, A. Hayashi, and M. Tatsumisago, J. Electrochem. Soc., 164, A3960 (2017). | minnmann [27] | NCM111–Li₃PS₄ CAM 적재 ↔ 수송 스윕 — 같은 실험 축의 두 번째 점 | §3-3 |
| [11] Epstein N. On tortuosity and the tortuosity factor in flow and diffusion through porous media. Chem Eng Sci. 1989;44(3):777–779. | tjaden [11] | κ = τ² 명명 원전 | §1 (이름 근거) |
| [18] I. V. Thorat, D. E. Stephenson, N. A. Zacharias, K. Zaghib, J. N. Harb, and D. R. Wheeler, J. Power Sources, 188, 592 (2009). | landesfeind [18] (= tjaden [47] · nguyen ref 16) | eRDM 원조 · α 관례 | §1 Bruggeman 행 |
| [61] Stephenson DE, Hartman EM, Harb JN, et al. Modeling of particle-particle interactions in porous cathodes for lithium-ion batteries. J Electrochem Soc. 2007;154(12):A1146. | tjaden [61] | 리뷰 목록에서 접촉망에 가장 가까운 모형 | §3-6 비교 |
| Morasch, R., Landesfeind, J., Suthar, B. & Gasteiger, H. A. Detection of binder gradients using impedance spectroscopy and their influence on the tortuosity of Li-ion battery graphite electrodes. J. Electrochem. Soc. 165, A3459 (2018). | nguyen ref 33 | 구배 전극의 방향 의존 τ — graded-z | §7 ② (z 균질) |

- 낮음 (서지는 카드 표 참조): Usseglio-Viretta 2018 (nguyen ref 28) · Lu 2020 (ref 34) · Zahn 2017 (ref 12) · Clennell 1997 · Djian 2007 · Ebner 2014 (landesfeind [13] [14] [32]) · van Brakel & Heertjes 1974 · Chung 2013 · Zhang 2015 · Tjaden 2016 (tjaden [12] [56] [64] [27]) · Ross 1982 · Arzt, Ashby & Easterling (미출판 [미확인]) (arzt [2] [15]) · Ito 2017 · Nam 2018 · Jung 2019 · Neumann 2020 · Danner 2016 (park [11] [15d] [18b] [14] [19c]).

### 8-3. 목록 밖 (출처 탐색 자체가 필요)
| 항목 | 상태 |
|---|---|
| 등급 문턱 "Tippens 2019" | 서지 문자열이 7 카드 어디에도 없다 [미확인] — 원문 확인 전 인용 금지 (TAU-16) |
| LPSCl 복합양극 springback 크기 (380 → ≈ 40 MPa) | 7 카드 참고문헌 목록에 해당 서지 없음 [미확인] (§3-8 ③) |
| 프레임 [1] "순수 SE ≈ 10 % @ 300 MPa" | 문헌 요청이 아니라 정정 거리다 — 카드 계보 (`minnmann2022_…` 카드) 상 우리 MPM 보정 수렴값.  관련 카드는 이미 있다: `sakuda2013_sulfide_mechanical_property` (75Li₂S–25P₂S₅ 유리 · 300 MPa 는 Fig 2a 판독 추세값) · `minnmann2024_microstructure_porosity_visualization` (복합 기공) (TAU-10 · 결정 7) |
| COMSOL 배터리 인터페이스의 보정 식 | 문헌이 아니라 사용 버전 GUI Equation 보기 캡처로 닫는다 (§1 · 결정 5) |

---

## §R. 리뷰 반영 원장

집계: 코드 49 행 (확인 37 · 부분 10 · 틀림 1 · 검증 불가 1) + 놓친 결함 M1–M9 · 문헌 54 (일치 41 · 부분 10 · 틀림 3) · 물리 32 (타당 9 · 조건부 17 · 틀림 5 · 검증 불가 1).  확인 · 일치 · 타당 행 중 고칠 것이 없던 행은 나열을 생략했다.  아래는 v1 문장이 바뀐 행 전부다.

| 리뷰 · 항목 | 판정 | v1 문장 | v2 문장 (자리) |
|---|---|---|---|
| 코드 #5 | 부분 | T12 "COMSOL τ_F 칸에 √T" | 파라미터 표에 √T 를 "COMSOL/EIS input" 으로 표기 · 자동 배선 없음 · README 검산식 φ 반대 (§2 T12 · TAU-01) |
| 코드 #6 (= M6) | 부분 | TAU-01 범위 `lhs_design_dataset.py:884` (→ TSV) | 커밋 TSV 6 개 (전달본 v1 · v1.1 포함) 명시 → 정오표 결정 (결정 5) |
| 코드 #7 | 부분 | "3192 · 3222 (selftest 가 옛 문구를 강제)" | :3192 는 주석 · :3222–3223 은 'COMSOL' · 'τ_Laplace' 낱말 존재만 강제 (TAU-01) |
| 코드 #9 | 부분 | "COMSOL 2D 같음" (등급과) | 사슬 한 칸 다름 (stage_e 없음) · 변형 최소 다섯 (TAU-03) |
| 코드 #10 | 확인 + 정밀화 | 등급 / 웹앱 H 0.852–1.584 를 재료 인자로 읽히게 둠 | 편차의 주원인 = 모드 불일치 (156/157) · Stage-E ≠ physics 1/157 (결정 6 · T10 · TAU-03) |
| 코드 #11 | 확인 + 추가 | — | `grade_engine.py:925` 의 낡은 줄 번호 `app.py:2026` 도 고칠 대상 (TAU-03) |
| 코드 #17 | 확인 + 추가 | T < 1 원인 = 원기둥 R_bulk | + 띠 끝 효과 (L0) 같은 방향 · 26 건 전부 `plate_z_source = mesh` (§3-6) |
| 코드 #19 | 확인 + 보강 | ψ 분모 = "주원인 후보" | 커밋 자료와 정합 (탄성 몫 ≤ 0.9 % · 협착만 비 0.39 · CF 동일) · 곱 배치 반전은 [미검증] (§3-8) |
| 코드 #22 | **틀림** | "A_LIGG/A_Hertz = 2 − d/(2r)" | "2 − δ/(2r) (δ = 겹침)" · 같은 문서 안 d 두 뜻 제거 (§6-1 · §5-1) |
| 코드 #23 (= M7) | 부분 | κ ≈ E*_real/E*_DEM "Hertz 근사" · "AM 모듈러스 [미확인]" | 생산 DEM = hooke/hysteresis → κ 는 δ 의존, E* 비 아님 · AM 140 GPa (덱) · C1 실측만 · 덱 단위계 환산 명시 (§6-3 · C1) |
| 코드 #24 | 확인 + 추가 | 봉인 모듈 "두 파일" | `NUMERIC_MODULES` 넷 (§4 머리) |
| 코드 #25 | 부분 | "주석 한 줄도 … 건드리지 않는다" (금지) | 수정 = 재봉인 강제 · 게이트는 미커밋만 잡음 · 봉인 밖 도우미 권고 유지 (§4 머리 · 결정 16) |
| 코드 #26 | 부분 | "c0c2d4f44 → 현재 봉인 상태 [미확인]" | + plastic_coverage 09-29 3 커밋 → 09-17 봉인은 있었다면 이미 거부 상태 (§4 머리) |
| 코드 #30 | 검증 불가 | 역사 코퍼스 폴백 빈도 [미확인] | 그대로 [미확인] + L2 판 높이 원인은 `plate_z_source = mesh` 157/157 로 배제 (§3-6) |
| 코드 #34 (= M8) | 부분 | 6 침대 σ_e · κ 적합 포함 "가능성 [미확인]" | σ_e 22.5 필터 전부 통과 → 비트 불변 깨짐 확정 · σ_thermal 무영향 → 결정 12 (TAU-05) |
| 코드 #35 | 확인 + 추가 | 띠 중심 미명기 | 띠 중심 = SI 식 S9 재계산값 명기 · 0.330 반올림이면 n 56 · T_P 8.75 (§3-3) |
| 코드 #38 (= M3) | 부분 | G5 "G_eff ≤ 2·Σg (`:846`)" | :846 = `NETWORK_DEBUG` 출력 · 실제 관문 :778–818 · :870–878 · 2·Σg 는 새 규칙으로만 (§5-2 G5) |
| 코드 #41 | 확인 + 추가 | 0.27 · 10.2 (규약 미표기) | 하위 분위 규약 명기 (보간이면 0.283 · 10.72) (§7) |
| 코드 #47 | 부분 | "Tippens 2019, Famprikis 2019 출처 없음 (감사 D #97)" | Famprikis 카드에 없음 · Tippens 2019 미감사 [미확인] (TAU-16 · 결정 6) |
| 코드 M1 | 놓침 | — | TAU-21 (P2): physics τ 칸이 조용히 Hertz 값 |
| 코드 M2 | 놓침 | G2 · G3 가 `sigma_full_status` 로 판정 가능하다고 전제 | TAU-22 (P2): 비관통 = 'not_computed' → `percolating_fraction == 0` ∧ `calc_percolation` (결정 2 · G2) |
| 코드 M4 | 놓침 | — | TAU-23 (P3): `constriction_dominant` 경고 죽음 · TAU-06 묶음 |
| 코드 M5 | 놓침 | G1 "L0 이면 값을 싣는다" | TAU-24 (P2): L0 띠 단락 T ≤ 4r_SE/L 하향 → 메타 · 한정어 (§3-6 · G1) |
| 코드 M9 | 놓침 | — | TAU-25 (P3): 6 자리 반올림 → 무차원 `sigma_full` 로 T 계산 (G4) |
| 문헌 A0 | 부분 | §0 "문헌의 'tortuosity factor' (… Landesfeind τ · Park τ_e …)" | 원문 이름 병기: Landesfeind "effective tortuosity" (Eq 13 은 τ_e 계열) · Park "tortuosity" (결론 ①) |
| 문헌 A2 | 일치 + 수정 | Tjaden flux/기하 같은 기호 "p.61" | p.61–62 (§1) |
| 문헌 A7 | 일치 + 수정 | Park "SI p.6 Eq S1·S2" | 본문 명칭 Eq S1·S2 · 그림 라벨 [1]·[2] 병기 (§1) |
| 문헌 A9 | 일치 + 수정 | Minnmann 쪽 표기 미설명 | "PDF 쪽 (IOP 표지 = p.1)" 명기 (§1 머리) |
| 문헌 A13 | **틀림** | Eq 6-6 "p.375" (§1 2 곳 · 글머리 2 곳 · §5-3) | **p.376** (전 자리) |
| 문헌 A14 | **틀림** | Bruggeman τ_F "p.376 · p.450" | **p.377 · p.451** |
| 문헌 A15 | **틀림** | p.342 · p.347 · p.449 · p.449–450 · p.266 · p.414 · MQ p.376 | p.343 · p.348 · p.450 · p.450–451 · p.267 (노드 머리 p.266) · p.415 · p.377.  정본 카드의 같은 오차 1 건도 고침 (작업 2) |
| 문헌 B1 | 일치 + 수정 | CL-94 문안 "본문 · SI 어디에도 없다" | + "380 MPa 복합 기공 7.6–17 % (평균 14 %) 는 있으나 순수 SE 값 · 300 MPa 는 없다" (결정 7 · TAU-10) |
| 문헌 B2 | 부분 | "출처 [미확인] · 에이전트 제안 0 건" | 카드 계보 병기 (Sakuda 2013 · Minnmann 2024 · 우리 MPM 수렴값 — 순환 의심) · [미확인] 유지 (TAU-10 · §8-3) |
| 문헌 C2 | 부분 | "Arzt 1982 는 impingement 이후 규칙을 주지 않는다" | 접촉면적 성장 · 조각 겹침 공제 규칙은 없다 ([8] 로 미룸) · 배위수에는 압밀 한계 Z (식 11) 처방이 있다 (p.1887) — §6 은 면적 쪽만 인용 |
| 문헌 C3 | 부분 | 안 A 근거 = "Arzt 식 (7) · (A4)–(A6)" | 자유표면 회계에서의 **유추** (Arzt 는 상한으로 쓰지 않음) · 안 A 근거 = Nisar 형 평균장 난간 (§6-4) |
| 문헌 C5 | 부분 | Σ A_tabor = 4πR²p̄/H "(Love–Weber) → 카드 L-3" | Arzt (19)–(21) = 등방 · 단분산 평균장 판만 · 입자별은 Love–Weber (§6-3 · TAU-11 카드 문구) |
| 문헌 C6 | 일치 + 한정어 | "upper bound for the contact areas" | + "두 재분배 극한 사이 · 단분산 모형 안" (§6-1) |
| 문헌 C8 | 일치 + 각주 | 1.85 · 1.87 배 | + (A9) 정규화 각주 (없으면 1.47 · 1.43) (§6-1) |
| 문헌 D2 | 일치 + 한정어 | "flux ≥ 기하가 늘 성립 (p.60 식 22)" | + 근거는 [63, 85] 부분체적 경험식 (§3-5) |
| 문헌 D5 | 일치 + 표기 | Minnmann φ_SE 0.613 … 0.248 | "SI 식 S9 재계산" 표기 (§3-3 · §2 [M]) |
| 문헌 D6 | 부분 | fine SE 33.8 · "fine 대비 0.40" | σ₀ 1.6 (밀링 전) 기준 · 밀링 SE 1.2 기준이면 ≈ 25 · 비 0.53 병기 (§2 [M] · §3-3) |
| 문헌 D9 | 부분 | Park T ≈ 4.3 / 11 / 21 (σ₀ 3.0) · 비 0.72 / 0.44 / 0.72 | Park 자기 σ₀ 판 4.4 / 11 / 19 주값 · 3.0 판 괄호 · 비 0.71 / 0.44 / 0.79 (§3-4 · §2 [P]) |
| 문헌 D10 | 부분 | Bruggeman 배수 "Park 2–24×" | 실험 3.0–9.8× · 모형 5-seed 밴드 1.8–24× (시뮬) 분리 (§3-5) |
| 문헌 D16 | 부분 | Nguyen "recommended" | "should be preferred" (p5 · p8) · "should be used" (p7) (§1 · §7) |
| 문헌 E6 | 일치 + 수정 | Froboese "σ₀ 식 출처" | Table S1 각주 b "literature[18a-c]" 중 후보 (§8-1 #3) |
| 문헌 E7 | 부분 | "[34] Ender … JES 159, A972 (2012) — 복셀 Laplace N_M" | Laplace N_M 인용은 [35] Electrochem. commun. 13, 166 (2011) · [34] = FIB-SEM (§8-1 #9 · §8-2) |
| 물리 a1 | 조건부 | §0 "식 · 정규화가 **같은 양**" | "같은 정의식 — 물리 기준 상태는 다름" · 열 이름표 "접촉망 모델 T" (결론 ① · §5-1) |
| 물리 a2 | 타당 + 추가 | — | "실험 T ∝ 가정 σ₀ — 약분은 우리 쪽만" (§3-1) |
| 물리 a3 | 조건부 | "T_pure,ours [미확인] · 방향도 미정" | 외삽 > 1 (hertz 1.4–2.0) → × 0.5–0.7 · 순수 SE 런 = 게이트 (결론 ③ · §3-2 · 결정 4) |
| 물리 a4 | 조건부 | hertz 열은 "Holm 협착 포함" T 로 그대로 · 세대 표지는 physics 만 | hertz 도 1세대 (반공간 Holm, a/r 0.30–0.44 → R_c 1.7–2.4×) · 메타 `ion_net_constriction` (결론 ⑤ · TAU-13) |
| 물리 a5 | 조건부 | TAU-03 편차를 재료 인자로 읽히게 둠 | 모드 불일치 156/157 · 재료 인자는 r_SE < 0.5 µm 행만 (결정 6) |
| 물리 b2 | 조건부 | φ 짝짓기 "우리 점이 ≈ 2 % 이상 왼쪽" (코퍼스 중앙 0.980) | 띠별 φ_mc/φ_구합 0.907–0.982 · Minnmann 시료별 기공 · 기공 미정합 · 과압축 표지 (§3-3) |
| 물리 b3 | **틀림** | "SE 많은 쪽 (φ_SE ≥ 0.44) Minnmann 대비 −25 … +10 % = 정합 범위" | **판정 불가** — 곡선 Δφ_SE ≈ 0.06–0.09 이동 · 과압축 침대 · 기준 상태 · 협착식 (결론 ③ · §3-8) |
| 물리 b4 | 조건부 | "SE 적은 쪽 실험보다 3–10 배 낮게" · 후보 ② CBD · 바인더 | 다른 미세구조의 비교 (입경비 · 문턱 거리) · 바인더는 Minnmann 에 해당 없음 · springback 추가 · 입경비 하위집합 수치 (결론 ④ · §3-8) |
| 물리 b5 | 조건부 | Park "추세 전용" | + σ₀ · NBR 바인더 · 입경비 ≈ 1 한정어 · Minnmann 과 합치지 않음 (§3-4) |
| 물리 b6 | 검증 불가 | ⑤ "연화 E 로 큰 겹침 = 높은 배위수" (T↓ 후보) | 가설 유지 + 반대 방향 항 (반공간 Maxwell 과대 T↑) 같은 행 — 부호 미정 (§3-8 ⑥) |
| 물리 b8 | 조건부 | physics > hertz T 의 주원인 = ψ 분모 | + SE 많은 쪽 14 침대 역전 = ψ 절벽 · a_eff 클램프 (§3-8) |
| 물리 c1 | 조건부 | §0 · §5-1 "COMSOL Tortuosity 입력 = T" 단정 | 종 수송 기준 · 배터리 = 강하게 시사 · σ₀ 짝 · T 에 "COMSOL 입력" 은 GUI 확인 뒤 · 보강 문장 추가 — 물리 리뷰 표기 p.143 · p.155 (0-기준 색인) 를 원문 대조해 인쇄 p.144 · p.156 으로 (결론 ② · §1 · §5) |
| 물리 d1 | 조건부 | "τ_e 인계 비차단 · 위상 dead-end 0.03 %" | ML 기술자 한정 · p90 2.86 % · flux dead-end 는 FULL 장 · z 균질 · LHS-25 선행 (결론 ⑧ · §7 · 결정 13) |
| 물리 e1 | 타당 + 추가 | C1 | + 가지 길이 보정 크기 δ̄/2R 병기 (§6-5) |
| 물리 e2 | **틀림** | κ ≈ 15–30 · 문턱 30–60 MPa · "0.1–0.2 × 원판" · "SE 많은 침대에서 일반적이어야" | 철회 · κ ≈ 2–9 (힘 평형) · C1 실측으로만 (§6-3) |
| 물리 e3 | 조건부 | "입자별 합에 표면 한도가 없어 포화" → 안 A/B | 뿌리 = 접촉별 추정량이 상한값 (부피 보존의 ≈ 1.5–3 배) → 추정량 사전등록 · "physics (상한값)" (결론 ⑦ · §6-2 · 결정 9) |
| 물리 e4 | 조건부 | 안 A 근거 = Arzt (7) · nisar · zunker | 안 A = Nisar 형 평균장 난간 · Arzt 는 안 B 근거 · implied 압력 기록 (§6-4) |
| 물리 e5 | 타당 + 추가 | β_AM = 1 (정확) | + 원판이 아니라 구관 면적으로 회계 (§6-4) |
| 물리 e6 | **틀림** | β_SE {1.0, 1.10} | 철회 · 물리 유도 또는 1.0–2.0 감도 사전등록 (§6-4 · 결정 9) |
| 물리 f1 | 타당 + 수정 | CF "정의 결함" · "도체 부피 ≈ 0.75·Z 배" | 모델 내부 기준선 (부피 비보존 bulk) · affine T_CF ≈ 4/Z + 코퍼스 대조 · CL-81 대조에 CF 과전도 사전등록 (§3-6 · 결정 11) |
| 물리 f2 | 조건부 | "우리 안의 순수 협착 배수 = FULL/CF" | "모델 내부 협착 비 (원기둥 bulk 기준)" · T 로 ≈ 1.2–1.4 배 과대 (§3-5 · §3-6 · TAU-08) |
| 물리 f3 | **틀림** | G5 "f ≤ φ (T ≥ 1) 실패 시 SOLVER_ANOMALY" | `MODEL_BELOW_CONTINUUM_BOUND` (값 유지 + 표지) · SOLVER_ANOMALY 상태 폐기 · 수치 실패는 솔버 관문 → `NOT_COMPUTED (solver_guard)` (§5-2 G5) |
| 물리 f4 | 조건부 | G1 "L0 이면 값을 싣는다 (L1 만 T 를 낮춘다)" | L0 도 T ≤ 4r_SE/L 하향 (중앙 6 % · 최대 17 %) → 메타 `ion_net_band_frac` · 한정어 (§3-6 · G1) |
| 물리 g1 | **틀림** | Tabor F 정의는 "C1 을 본 뒤 정한다" | C1 **전에** 역학으로 등록 · C1 은 진단 전용 (§6-4 · §6-5 · 결정 9) |
| 물리 g2 | 조건부 | C2 "18 침대 회복 · ρ 부호" (판정/보고 미정) | 보고 전용 · 채택 기준은 물리 검사만 (§6-5 C2) |
| 물리 g3 | 조건부 | f_mc "T 가 현행 솔버 T 와 같은 값" | 자기상사 가정 · "재척도 (해 아님)" 이름표 · 풀린 f_gap 메타 (§3-7 · 결정 1 · §5-1) |
| 물리 g4 | 조건부 | TAU-02 대체 문구 "T 4.41 vs 4.27 (단일 케이스 · 모드 의존)" | 수치 없이 철회 (결정 8) |
| 물리 h1 | 타당 + 추가 | 비관통 = f 0 · T · τ 빈칸 | + "문턱 근처 관통 여부는 상자 크기 실현값 — 재료 성질 아님" (결정 2 · G3) |
| 물리 h2 | 타당 + 추가 | CL-94 (제안) | + "순환 앵커" · MPM σ_y 0.30 "외부 앵커 없음" (결정 7) |
