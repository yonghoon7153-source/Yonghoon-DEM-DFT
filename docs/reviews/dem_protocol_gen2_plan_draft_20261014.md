# DEM 압축 프로토콜 세대 2 계획서 (초안 · 런 없음 · 1저자 비준 전 · 2026-10-14)

> **지위**: 계획 초안 — 런 0 · 코드 변경 0 · 결과 0 건 · 봉인 32 (`CODE_FILES`) 무변경 · 기존 문서 무변경.  이 문서는 단계 정의 · 끝 조건 · 물성 · 보정 · 시험 · 표지의 **설계**만 적는다 — 숫자 문턱은 런 전 **등록 문서**에서 봉인한다 (이 초안은 등록이 아니다).
> **순서** (1저자 10-14 저녁 4): 이 초안 → 검토 → 1저자 비준 → Codex → 등록 · 시험 먼저 → 런.
> **근거 (리포)**: 원장 `DEMP-01` · `DEMP-02` · `MV-01`–`MV-09` (`docs/reviews/findings.json`) · Codex 모델 검증 판정문 `docs/reviews/codex_review_model_validation_20261008.md` (이하 **판정문**) · 감쇠 가지 실험 `docs/data/ps73_damping_branch_20261007/README.md` (이하 **분기 README** — §2 · §4 · §9 · §12-4) · 언로딩 등록 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` (이하 **언로딩 등록** — §12 · §13) · 키트 `docs/data/ps45_unload_20261009/README.md` · Codex 키트 재검토 `docs/reviews/codex_review_dem_unloading_kit_20261014.md` · 수정 계획 `docs/reviews/dem_unloading_kit_fix_plan_20261014.md` · 지배방정식 `docs/dem_governing_equations_background_20261011.md` (이하 **배경**) · `docs/dem_governing_equations_report_20261009.md` · E_SE 보정 이력 `docs/esse_calibration_2mAh_real_9.md` · 원장 `CL-94` (`docs/reviews/claims.json`) · 1저자 결정 = `docs/session_20260923_progress.md` 10-14 저녁 · 저녁 2 · 3 · 4 줄.
> **문헌**: litdb 정본 브랜치 `origin/claude/friendly-meitner-lldvar` 의 카드만 (이 초안이 읽은 판 = 커밋 `9dc235c38`) — 인용 꼴 = `litdb-canon:<slug>` + 카드가 적은 쪽 · 그림 · 표.  카드에 없는 서지 · 값은 채우지 않았다 (규율 ⑥) — 찾을 문헌 = §11.
> **표지**: [우리 산술] = 이 초안이 덱 · 문서 · 카드 값으로 계산 (식은 그 자리에) · [어림] = 단순 모형 (예: affine 저항) 의 크기 · [미확인] = 출처 없음 / 확인 전 · ⬜ = 1저자 결정 대기 (§8).

## 0. 지위 · 한정어

### 0-1. 1저자 결정 (2026-10-14)

| # | 때 · 출처 | 결정 (원문 낱말은 *기울임*) | 이 문서 |
|---|---|---|---|
| D1 | 10-14 저녁 ⑤ (진행 기록) · 분기 README §12-4 끝 | 가지 B 결과에 따라 E_SE · 정지 규칙을 처음부터 다시 세워도 된다 (*"쇄신 느낌으로 처음부터 … repo 에 기록은 잘 남겨 놓고 더 체계적으로"*) | 전체 |
| D2 | 10-14 저녁 2 ① | 단계 = **insertion → stabilization → compression → servo (정적 300 MPa 유지) → relaxation → plate remove → unloading** (*"이런 식이겠지"* — 정의 · 순서 확인은 이 초안에서) | §2 · Q1 · Q2 |
| D3 | 10-14 저녁 2 ① | 서보로 300 MPa 를 잡은 뒤 판을 빼고 언로딩까지 넣는다 ⇒ **지금의 언로딩 로직 (ps45 키트 · ULKR 수정 중) 을 확실히 잡는 것이 세대 2 의 선행** | §0-3 · §2-6 · §5 T12 |
| D4 | 10-14 저녁 2 ② | **SE 진밀도 1.64 g/cm³** (랩 · 세대 2) — 10-13 의 "2.0 고수" 는 세대 1 침대 한정 · "실제 진밀도 미확인" 한정어 유지 · NCM 4.8 ↔ 슬라이드 4.85 = ⬜ → **D10 으로 닫힘 (4.85)** | §3 · §4-3 · Q6 · Q7 |
| D5 | 10-14 저녁 2 ③ | 설계 점: 압축 감쇠 (가지 C1 · C2) · 정지 = 정적 서보 (MV-01 수렴 판정 고침) · 서보 전환 때 판 fix 재생성 안 함 (MV-02) · 보존 (MV-08) · 판 뚫음 (DEMP-02) · E_SE 재보정 (정적 프로토콜 · E 사다리 · 실험 앵커 = 소립 SE 펠릿 · 복합체 공극 · 결과 전 등록 · Codex) · 세대 1 = 지우지 않고 표지 | §2 · §4 · §6 |
| D6 | 10-14 저녁 3 | E_SE 보정 = **순수 SE 침대가 300 MPa 가압 + relaxation 끝에서 공극률 union 10–13 %** (랩 표준 · 측정법 미확인 · 소립 SE 펠릿 기하 공극률로 대조 가능) · 마찰 μ 등 접촉 계수 = 근거 있으면 고쳐도 된다 (압축 민감도는 작아도 언로딩 · 스프링백에 영향) → 계수 표 | §3 · §4 |
| D7 | 10-14 저녁 4 | 계획서는 **litdb 정본 카드 등 근거와 함께** (*"이 모든 과정을 litdb 등의 reference와 함께"*) | §10 · §11 |
| D8 | 10-14 (세션 전달) | 세대 2 에서 **거시 검증 세트를 새 프로토콜로 다시 한다** — 최소 순수 SE Heckel 다압력 (세대 1 = `heckel/` 의 100 · 200 · 300 · 400 MPa 덱 · 생성기 `scripts/make_heckel_inputs.py` · 같은 압축 감쇠 0.5 — `DEMP-01` note) · frame [3] 의 조성 (AM %) 공극 검사 (Heckel 선형 · Furnas dip) · E_SE 보정 침대 | §2-9 · §4-7 · §6 |
| D9 | 10-14 (세션 전달) | 공극 정의: **보정 표적 = ε_union 10–13 % 그대로** (순수 SE · 300 MPa + relaxation 끝) · **ε_sphere (질량 보존 — 실험 질량 / 기하 공극과 같은 연산자) 도 모든 기록에 함께 계산 · 보존** (*"내부적으로 sphere는 가지고 있으면 좋지"*) · MV-03 한정어를 붙인다 · 랩 펠릿 (질량 + 두께 · 진밀도 1.64 가정) 은 ε_sphere 로 대조 ⇒ **열린 질문이 아니라 기록된 결정** | §4-1 |
| D10 | 10-14 밤 (세션 전달) | 세대 2 입자 진밀도 = **NCM (PC · SC) 4.85 · SE 1.64 g/cm³** — 출처 = 1저자 2 년차 연구 보고 슬라이드 "2-1 / DEM 해석 조건" 표 (같은 표: 지름 PC 9 · SC 4 · SE 1 µm · NCM 80 wt% · 6 mAh/cm² · 300 MPa · 50 × 50 µm · 입자 159,000–163,000 개 · 영률 PC/SC 140 · SE 22 GPa = **재료 참고값 — DEM 입력 아님**) · 세대 1 침대 = 덱 값 4.8 · 2.0 그대로 (역사 · 다시 돌리지 않음) · 밀도의 랩 측정법은 리포에 기록이 없다 [미확인 — 출처 = 1저자 슬라이드] · 세대 2 E_SE 는 여전히 보정 유효값 (D6 · D9) | §2-1 · §3 · §4-3 · Q6 (닫힘) |

### 0-2. 한정어 (떼지 말 것)

1. 런 0 · 코드 0 — 숫자는 덱 · 리포 문서 · 정본 카드 값과 [우리 산술] · [어림] 뿐.  가지 B 값 (§1 #2) 은 **모델 내부 진단** (MV-01 · 02 · 08 검사 전) — "정적 300 MPa 값" 으로 쓰지 않는다.
2. §2-4 끝 조건 숫자 다수 = 판정문 §3 *"검토자가 제안하는 수치 오차 예산"* (실험 상수 아님) 을 옮긴 것 — 1저자 채택 · 등록 봉인 전.
3. 세대 2 는 **접촉 법칙 계열을 바꾸지 않는다** (`hooke/hysteresis` + 보정된 SE 유효 E) — 항복 캡 법칙은 세대 3 후보 (Q15).
4. 보정 표적 10–13 % 는 **1저자 랩 표준 (측정법 미확인)** — 외부 앵커로 부르지 않는다 (§4-2 · `CL-94`).
5. 세대 1 결과는 지우지 않는다 — "DEM 프로토콜 세대 1" 표지 + 한정어 (§6).
6. ps45 언로딩 시험은 **세대 1 침대 위**의 시험이다 — 세대 2 언로딩 단계는 그 **로직**을 쓴다 (값이 아니라).

### 0-3. 이름 · 선행

- 이름 = **"DEM 프로토콜 세대 1 / 2"** (키 제안 `dem_protocol_gen` = `P1` / `P2` · §6-3).  ⚠ 이미 있는 **"접촉망 세대 2"** (`ion_net_generation` = g2 — Physics ψ 곱 · 면적 g2 · 정확 Dirichlet 전극 · CLAUDE.md 10-06 저녁 줄) 와 **다른 축**이다.  "세대 2" 만 따로 쓰지 않는다.  v1.3 배포 행 = "DEM 프로토콜 세대 1 침대 × 접촉망 세대 2".
- 선행: ① 언로딩 키트 `ULKR-01`–`12` 수정 (1저자 10-14 Q1–Q9 권고대로 · 별도 작업 트리에서 진행 — 이 초안의 기준 커밋 `fdfd6e070` 에는 아직 없음 · 원장 open) → Codex 짧은 재확인 GO ② 이 계획 비준 ③ 세대 2 등록 (런 전) · 시험 먼저 (§5).

## 1. 세대 1 에서 틀린 것

| # | 무엇이 틀렸나 | 증거 (숫자 · 자리) | 원장 | 세대 2 (§) |
|---|---|---|---|---|
| 1 | **압축 단계 전역 감쇠** `fix damp all viscous 0.5` 가 판 힘의 큰 몫을 진다 — "300 MPa 도달" 에 저항이 들어 있다 | ps73 압축 중 저항 −0.5·Σv_z = 434.3 N = 목표 750 N 의 57.9 % · 이완 뒤 정적 165.3 MPa (분기 README §1) · affine 어림 저항 몫 ≈ N/300,000 (300 MPa · 분기 README §9) → **입자 수 N (두께) 에 비례** — 순수 SE Heckel 침대 (N 40,250) 13 % @300 · 40 % @100 MPa [우리 산술 — 저항 = γ·N·v/2 · 덱 0.0025 m²] | `DEMP-01` (P1) | §2-3 · §2-4 · §3 γ_g |
| 2 | **정지 = 처음 도달 + 판 고정 이완** → 정적 300 MPa 가 아니다 | 가지 B (ibb job 271368): 같은 멈춘 상태에서 서보 750 N 유지 → 105.842 µm (Δh −5.210 µm) · ε_sphere 14.953 → 10.769 % (−4.184 %p) · 판 압력 299.27 MPa (분기 README §12-4 · 모델 내부 진단) | `DEMP-01` | §2-4 |
| 3 | 가지 B 의 수렴 판정 (CONVERGED) ≠ 정적 평형 | KE 0.5 J (초기 참조 KE 의 29,483 배) 합성 입력이 10 번째 덩어리에서 CONVERGED (판정문 MV-01) | `MV-01` (P1) | §2-4 끝 조건 · §5 T3 |
| 4 | 서보 전환 때 판 · 벽 fix 를 지우고 다시 만든다 → 법선 소성 이력 (δ_max) 초기화 | 정규화 반례 법선력 0.16 → 0.40 (판정문 MV-02 · `docs/data/ps73_damping_branch_20261007/in.branch_B.liggghts` 214–242 행) | `MV-02` (P1) | §2-0 ① · §5 T1 · T2 |
| 5 | union 을 고르는 것으로 실험 질량 공극과의 불일치가 풀리지 않는다 · 쌍 렌즈 union ≠ 정확 union | 순수 SE 두 런 정의 차 12.42 · 11.41 %p · 세 구 반례 2.045 %p (판정문 MV-03) | `MV-03` (P1) | §4-1 |
| 6 | "기하 고정" E 민감도는 실제로 재평형 민감도 | 판정문 MV-04 · §5 표 (세 estimand) | `MV-04` | §4-5 |
| 7 | 중력 9.81 (자기 무게 10⁶ 배) · 정착 98.1 (10⁷ 배) — 보정 뒤 중력을 바꾸면 준비 이력 교란을 E 가 흡수 | 93 µm 창 자기 무게 2.97 MPa ↔ 물리 축척 2.97 Pa (판정문 §6) | `MV-05` (P1) | §2-2 · §4-9 |
| 8 | t0 (문법 시험) ≠ dt 자격 · 24 GPa = Li₂S–P₂S₅ 유리 값 | 판정문 MV-06 · `litdb-canon:sakuda2013_sulfide_mechanical_property` (75Li₂S·25P₂S₅ 유리 · E 18–25 GPa · ρ_glass 1.88) | `MV-06` (P2) | §3 dt · E 행 |
| 9 | 입자 수 가드 ≠ 보존 | 50 × 50 × 111.052 µm³ 에서 AM_P (r 4.5 µm) 1 개 = ε_sphere 0.137 %p · 50 개 = 6.87 %p (판정문 MV-08) | `MV-08` (P2) | §5 T4 |
| 10 | 입자가 판 메시를 뚫고 나간다 | ps73 판 위 입자 최대 11 · 이완 시작 원자 3 개 잃음 (`docs/data/ps73_compaction_curve_20261006/README.md` §7-1) | `DEMP-02` (P3) | §2-3 기록 · §5 T4 |
| 11 | 덱 밀도 (NCM 4.8 · SE 2.0) ↔ 1저자 보고 표 (4.85 · 1.64) — 같은 질량 처방인데 **SE 부피 몫이 다르다** (보고 표의 밀도가 세대 1 덱 입력과 달랐다) | 81.6 : 18.4 (질량) → SE 부피 몫 35.1 % (4.8 · 2.0) · 40.0 % (4.85 · 1.64) [우리 산술 §3-2] | (D4 · D10) | §3 |
| 12 | 접촉 계수 다수에 출처 기록이 없다 — 특히 언로딩을 정하는 k̂₂/k₁ · k_c/k₁ | 덱 m5–m9 (배경 §5.4 · §7) · k_c/k₁ 1e5–1e6 ↔ 문헌 예시 1 (`litdb-canon:luding2008_cohesive_frictional_contact_models` Table 1·2) | — | §3 |
| 13 | 순수 SE 보정 · Heckel 침대가 얇다 | 300 MPa 침대 두께 8.24 µm ≈ SE 지름 8 개 (`docs/data/heckel_pure_se_dem.csv` plate_z) — 위 · 아래 벽 띠가 높이의 큰 몫 [어림] | — | §4-4 |
| 14 | 보정 앵커의 지위 | "순수 SE 10 % · 300 MPa" 앵커 = **출처 철회** (우리 MPM 보정 수렴값) | `CL-94` (hold) | §4-2 |
| 15 | 순수 SE 침대 겹침이 강성 축소 불변 조건 밖 | ⟨δ⟩ 0.11 µm = SE 지름의 11 % (`docs/data/esse_calibration_2mAh_real_9.csv` SE_only 행) ↔ *"overlap remains smaller than 1 % of the particle diameter"* (`litdb-canon:paulick2015_elastic_particle_properties_dem_review` §4 p.75) → 연화는 결과 불변 장치가 아니라 **보정 프록시** | — | §3 E 행 · §4-5 |

- `MV-07` (LW 응력 검증) · `MV-09` (스냅숏 README 수치 서술) = 응력 관측 해석 · 문서 서술 — 세대 2 단계 설계와 독립 (응력은 보조 관측으로 기록만 · LW 검증은 별건).
- 문헌 쪽: 정본 전극 DEM 22 편 중 **압축 단계에 전역 점성 감쇠를 둔 건식 압축 연구는 찾지 못했다** (보고 · 미보고 구분 불가 — 배경 §10.3 ④).  배경 감쇠 (background friction · eq 22) 는 Luding 모델에도 있다 — 장파장 협동 모드 소산용이고 카드 표기는 "과댐핑 주의" (`luding2008…` §2.6 · 카드 요약 — 원문 문구 아님).

## 2. 단계별 프로토콜

### 2-0. 공통 원칙

| # | 원칙 | 왜 | 어떻게 (LIGGGHTS 골자) |
|---|---|---|---|
| ① | **판 하나 · 한 번만 만든다** — 안정화에서 만든 판 메시 · 판 벽 fix 를 분리까지 지우거나 다시 만들지 않는다 | MV-02 | `fix top_mesh all mesh/surface/stress …` + `fix zwall_top all wall/gran … mesh n_meshes 1 meshes top_mesh` 한 번 · 판 이동 = `fix … move/mesh mesh top_mesh linear 0 0 v` 를 덩어리마다 끊고 다시 건다 — 벽 · 메시 fix 는 그대로라 판 접촉 이력이 이어진다 (언로딩 등록 §4-1 — Codex Q1-d 확인 · 키트가 이미 쓰는 장치) · ⚠ move/mesh **반복 정의**는 아직 바이너리에서 지나가 보지 않았다 (키트 수정 계획 Q8 (가) — ibb 문법 fixture 대상) → §5 T2 · 대안 = 내장 서보 (Q3) |
| ② | **모든 단계 끝 = 정량 조건** · 예산 소진 = `NOT_CONVERGED` (예측 띠로 구제하지 않는다) | MV-01 | 덩어리 사이에서 읽고 제어 (분기 키트 §7 꼴) · 판정은 사후 판독기가 원 기록으로 다시 한다 (덱 판정 = 제어용) |
| ③ | **단계 경계마다 같은 열의 전체 기록** | MV-08 · MV-03 · 키트 C17 | 원자 (id type x y z radius vx vy vz ω fx fy fz c_strs) · 쌍 접촉 26 열 (`compute pair/gran/local`) · 판 벽 local (`compute wall/gran/local`) · 판 메시 STL · restart · 단계 요약 (key=value) |
| ④ | **run 사이 읽기 규칙** | 분기 t0 1 회 FAIL (`SELF-98`) | run 바로 뒤 값은 정의 다음 줄에서 즉시 치환으로 얼림 · `write_restart` 뒤 `ke` 금지 · `run 0` 뒤 판 힘 금지 · setup 줄 판 압력 금지 (분기 README §8 · §12-2 · 생성기 selftest ⑭a · ⑭b) |
| ⑤ | **중력 규약을 보정 전에 고정** | MV-05 | 준비 (삽입 · 정착) g_prep = 수치 장치 (기록) · 안정화부터 g_final = 9.81e-6 (축척 — 판정문 §6 권고) · 2×2 확인 (§4-9 ②) |
| ⑥ | **시간은 물리 시간 단위로 적는다** | MV-06 · ULR1-04 | 창 · 유지 · 예산을 dt₀ step 수가 아니라 물리 시간으로 적고 W(dt) = T_W/dt (언로딩 등록 §13-4 표 꼴) |
| ⑦ | **공극은 두 정의를 함께** | MV-03 · D9 | 모든 기록에 ε_union (정확 · MC 표본오차) 과 ε_sphere (고정 ID · 판 안 집합) 를 나란히 · 쌍 렌즈 union 은 세대 1 연속성 칸으로만 |

### 2-1. 삽입 (insertion)

| 칸 | 내용 |
|---|---|
| 목적 | 처방 (상별 질량분율 · 진밀도 · 반경) 대로 입자 목록을 겹침 없이 만든다 |
| LIGGGHTS 골자 | `fix particletemplate/sphere` (상별 `density constant` · `radius constant`) → `fix particledistribution/discrete` (**질량분율**) → `fix insert/pack … overlapcheck yes … volumefraction_region` → `run 1` · `processors * * 1` · 삽입은 NP ≤ 2 (세대 1 덱 주석 — 4 · 10 rank 에서 부분 삽입 · `PS-01`) → `write_restart` → 이후 NP 변경은 재개 절차 G1–G3 (`docs/resume_ckpt_procedure_20260927.md`) |
| 매개변수 · 출처 | ρ_SE 1640 · ρ_AM (PC · SC) 4850 (D4 · D10 — 1저자 보고 표 · 측정법 [미확인]) · 반경 = 침대 설계 · `volumefraction_region` 0.321 · 초기 속도 −0.5 (세대 1 값 · 준비 장치 · 출처 없음) · 짝 seed (E 사다리 · 압력 사다리) |
| 끝 조건 | 상별 개수 = 처방 (허용 = rank 별 템플릿 절삭 폭 — `SELF-70` 꼴 · 숫자는 등록) · 최소 간격 ≥ 0 · 원자 수 하한 (세대 1 덱의 99 % 바닥 꼴) |
| 기록 | seed · 상별 개수 · 구 부피 · 질량 · 삽입 영역 · 덱 sha256 · LIGGGHTS 바이너리 sha256 · NP |
| 관련 결함 | `PS-01` · `SELF-70` (믹서 — `insert/pack` rank 별 템플릿 절삭) · 밀도 변경에 따른 개수 변화 (§3-2) |

### 2-2. 안정화 (stabilization) — 정착 + 판 배치 + 정지

| 칸 | 내용 |
|---|---|
| 목적 | 중력 정착으로 느슨한 충전층을 만들고 그 위에 판을 둔 뒤 압축 직전 정지 상태를 만든다 |
| LIGGGHTS 골자 | `fix nve/sphere` · `fix gravity g_prep` · `fix viscous γ_prep` → 정착 → `compute reduce max z` → 판 STL (z_max + r_max + 여유 · 세대 1 꼴) → `fix top_mesh … mesh/surface/stress` · `fix zwall_top … wall/gran … mesh` (★ 여기서 한 번 — 원칙 ①) → `fix gravity g_final` 로 바꿈 · γ_rest → 정지 판정 |
| 매개변수 · 출처 | g_prep: 세대 1 98.1 (×10 · 수치 가속 — 준비 이력은 2×2 로 확인 · MV-05) · g_final 9.81e-6 (λ_g = λ_σ/(λ_ρ·λ_L) = 10⁻⁶ · 판정문 §6) · γ_prep · γ_rest 1e-5 (세대 1 정착 · 이완 값) · DEM 정착 = 충전 생성기로만 쓰는 선례 `litdb-canon:pycompact2025_dem_mpfem_workflow` (방법만 — 금속 분말 · 1400–2000 MPa) |
| 끝 조건 | 병진 + 회전 KE 창 평균 ≤ 기준 (등록) · 판 접촉 힘 ≤ 목표의 0.1 % · 원자 · 새어 나감 0 |
| 기록 | 정착 끝 · 판 배치 뒤 덤프 · restart · z_max · 판 높이 · KE |
| 관련 결함 | `MV-05` · `DEMP-02` (판 위치 · 판 위 입자) · 세대 1 PHASE 2 (중력 9.81 + 감쇠 0.5 로 200,000 step) 는 쓰지 않는다 |

### 2-3. 압축 (compression)

| 칸 | 내용 |
|---|---|
| 목적 | 판을 일정 속도로 내려 목표 판 힘 근처까지 누른다 |
| LIGGGHTS 골자 | **권고 (가) 덱 수준 서보**: 덩어리 (1,000–5,000 step · 등록) 마다 판 힘 F (`f_top_mesh[3]` · 정규 thermo 줄 · 원칙 ④) 를 읽어 v = −clip(k_p·v_max·(F_t − F)/F_t, ±v_max) 로 move/mesh 를 다시 건다 — 오차가 크면 포화 (= v_max 일정 하강 · 세대 1 과 같은 판 속도) · 벽 · 메시 fix 는 그대로.  **대안 (나)** = `fix mesh/surface/stress/servo` 를 안정화부터 설치 (판 하나 · 재생성 없음) — move/mesh 와 함께 못 쓴다 (분기 README §8) · run 사이 `fix_modify` 로 `servo/integrate stop|start` · `servo/target_val` (0 불가 · equal 변수 허용) · `servo/vel_max` · `servo/ctrlParam kp ki kd` 를 바꿀 수 있다 (세션 스크래치에 남은 LIGGGHTS 소스 사본 `mesh_module_stress_servo.cpp` `modify_param` · 문서 `mesh_module_servo` 판독 — 사본의 판 = 3d5c00f 인지 확인 전 · 리포 밖) → (나) 면 이완 = `integrate stop` · 언로딩 = **힘 계단** (target 사다리) 이라 변위 계단인 키트와 다른 프로토콜이 된다 (Q3) |
| 매개변수 · 출처 | v_max = 0.01 m/s (덱) = **plate velocity 0.01 mm/s** (1저자 10-12 · 배경 §9-1) · F_t = 750 N (덱 · 300 MPa × 0.001 × 0.0025 m²) · **γ_comp = 저항 몫 기준**: 목표 근처 −γΣv_z ≤ F_t 의 2 % [어림 · 문헌 기준 없음 — 등록 때 확정] · affine 어림 몫 ≈ (γ/0.5)·N/300,000 → ps45 (N 1.6 × 10⁵) 0.05 → 5.3 % · 0.01 → 1.1 % [우리 산술] · 후보 0.05 · 0.01 · 1e-5 를 작은 침대에서 시험 (가지 C1 · C2 설계 · 시간 척도 표 — 0.05 까지 침대 집단 모드 과감쇠 ζ 4.2 · 분기 README §2 · §9 · 1저자 기억 *"낮추면 터짐"* 을 가드로 확인) · 관성수 I = γ̇·d·√(ρ/P) ≈ 7×10⁻⁶ (SE) – 1×10⁻⁴ (AM_P) at 300 MPa (배경 §9-1 [산술]) ↔ 준정적 예 I < 10⁻⁴ (`litdb-canon:thakur2014_eepa_adhesive_elastoplastic_dem` §4) |
| 끝 조건 | 판 힘 창 평균 ≥ (1 − x)·F_t 첫 도달 → 서보 단계 (같은 장치 · 제어 상태 이름만 바뀐다 · x = 등록) · 가드 (원자 · 새어 나감 · KE · 판 힘 과도 — 분기 README §7 값) = TECH |
| 기록 | 5,000 step 마다 원자 · 메시 · 판 힘 · −γΣv_z · KE (병진 · 회전) · 판 위 / 바닥 아래 중심 수 · 원자 수 |
| 관련 결함 | `DEMP-01` · `DEMP-02` · `MV-02` |

### 2-4. 서보 (정적 300 MPa 유지)

| 칸 | 내용 |
|---|---|
| 목적 | 판 힘을 F_t 에 붙든 채 침대를 **정적 평형**까지 둔다 — 공극 · 두께가 "판 명목 정적 300 MPa" (판정문 Q1 정의: P_top = F_top/A) 의 값이 되게 |
| LIGGGHTS 골자 | 압축과 같은 고리 (비례 구간) · γ_hold 1e-5 (세대 1 이완 · 가지 B 서보 값) · 덩어리 5,000 step · 회전 KE = `compute erotate/sphere` |
| 매개변수 · 출처 | k_p 30 · v_max 0.01 (가지 B) — ⚠ τ ≈ F_t/(k_p·v_max·K_bed) (판정문 Q10: K = 47,000 N/m 이면 0.053 s · K 가 1/10 이면 0.53 s 덱) → 침대 · E 마다 짧은 제어 자격 먼저 (§5 T11 · §4-9 ②) · 예산 = 물리 시간 (등록) |
| 끝 조건 (MV-01 해제 증거 — 숫자 = 판정문 §3 초안 · 1저자 채택 · 봉인 전) | 초기 전환 뒤에만 모은 **연속 창** W ≥ max(0.05 덱 s, 지배 이완 주기 × 10) + 같은 길이 추가 창으로 drift 대조 · **힘**: 창 평균 오차 ≤ 0.5 % · 정규 표본 각각 ≤ 1 % · **운동**: 병진 + 회전 KE 와 잔류 힘 / 토크 (K/(P_deck·V_deck) ≤ 1e-6 = 후보 screen · 단독 합격선 아님) · **힘 수지**: 중력 · 저항 · 관성 포함 전역 · 절단면 잔차 ≤ F_t 의 1 % · 저항 · 관성 항 각각 ≤ 0.1 % · **관측량 안정**: 추가 유지 (매 침대) · dt/2 · v/2 대조 (자격 런 · §4-9 ②) 에서 ε ≤ 0.1 %p · h ≤ 0.1 µm · 하중 몫 ≤ 1 %p · **보존**: 같은 예산 · 설명 안 되는 AM 손실 = 실패 · 예산 소진 = `NOT_CONVERGED` |
| 문헌 대조 | 정압 유지 → 운동에너지 0 까지: *"Pressure was then held constant until the system reaches static equilibrium (i.e., the kinetic energy of the system decayed to zero)"* (`litdb-canon:shi2019_high_am_loading_particle_size_assb` p.2) · PID 일정 단축압 + 총 KE 0 수렴까지 유지 (`litdb-canon:bazzoun2025_dem_parameter_sensitivity_assb_cathode` §4 · `litdb-canon:bazzoun2026_dem_fem_rnm_ionic`) · PI / PID 상단벽 → 목표 몰드압 (`litdb-canon:so2021_dem_mold_pressure_assb_coldpress` §4 · `litdb-canon:so2022_dem_compaction_coated_particles_assb` §2.4) · KE/PE < 1 % (`litdb-canon:demirtas2021_mpfem_hollow_sphere_die_compaction` §4-5 — RD ≥ 0.6 에서만 강제 · MPFEM) |
| 기록 | 덩어리 궤적 (step · 판 z · F · KE 병진 · 회전 · −γΣv_z · 원자 · 새어 나감) · 창 끝 덤프 · restart 100,000 step |
| 관련 결함 | `MV-01` · `MV-02` · `DEMP-01` · 판정문 Q1 · Q10 |

### 2-5. 이완 (relaxation) — 제안 정의 R-a (⬜ Q2)

| 칸 | 내용 |
|---|---|
| 목적 | 서보를 멈추고 (판 고정) 침대가 정적임을 **다시 확인** — 판 압력이 떨어지면 서보 끝이 정적이 아니었다는 뜻 · **E_SE 보정 표적 (ε_union) 을 읽는 상태** (D6) · 언로딩 출발 상태 S0 |
| LIGGGHTS 골자 | (가) move fix 없음 (판 고정 = 세대 1 PHASE 4 꼴) · (나) `fix_modify … servo/integrate stop` (같은 서보 fix · §2-3 사본 판독) · γ 1e-5 · 같은 메시 · 벽 fix |
| 매개변수 | 길이 ≥ 서보 판정 창과 같은 물리 시간 (등록) |
| 끝 조건 | 판 압력 창 평균이 F_t 의 ±1 % 안 (이완 강하 ΔP_relax ≤ 1 % — 넘으면 그 침대 `NOT_CONVERGED` · 재시도 = 등록된 1 회 서보 연장만) · 키트 S1 (판 압력 표류) · S2 (KE) · S3 (총힘 잔차 — 키트 C1 · C2) |
| 기록 | 언로딩 S0 보존 대상 전부 (언로딩 등록 §3-1: ID · 종류 · 반경 · 위치 · 속도 · 질량 · 상별 개수 · 판 간격 · 판 압력 · 접촉 이력) · **ε_union (안쪽 · 전체)** · **ε_sphere (all · inside)** · 쌍 렌즈 union (세대 1 연속성) · AM–AM 기여 D (`scripts/plane_load_share.py`) · 접촉 수 |
| 주의 | 판이 고정이라 h · ε_sphere 는 그대로 (입자 출입이 없으면) — ε_union 은 겹침 재분배로 움직일 수 있다 (언로딩 등록 §12-9: 고정 h 에서 겹침 감소 → V_union 증가 → ε_union 감소) → 표적 = **이 단계 끝 프레임** |
| 관련 결함 | `MV-01` · `MV-03` · D6 · D9 |

### 2-6. 언로딩 (하중 제거)

| 칸 | 내용 |
|---|---|
| 목적 | 판을 계단으로 들어 올려 측정 압력 P_meas 에서의 두께 · 회복 ρ 를 재고 분리까지 간다 (실험의 "하중 제거") |
| LIGGGHTS 골자 | **ps45 언로딩 키트 장치 그대로** — 같은 `top_mesh` 를 move/mesh +z 계단 · 단마다 유지 · 창 · 판독기 · 관문 (언로딩 등록 §4-1 · §12 · §13 · `docs/data/ps45_unload_20261009/README.md`) · ⛔ `ULKR` 수정 + Codex 재확인 GO 판만 |
| 매개변수 · 출처 | 키트 표 `docs/data/ps45_unload_20261009/unload_params.json` 값 (P_meas 1 MPa · Δz_A 0.20 µm · Δz_B 0.05 µm · T_W = 5,000 step × dt₀ · S1–S4 · 분리 2 창 · 분리 뒤 4 창 · 들어 올림 상한 16 µm) — ⚠ 계단 · 상한은 **ps45 h₀ ≈ 117 µm 기준** → 두께가 다른 침대는 h₀ 비례 환산 (등록 때) · g = g_final (9.81e-6 이면 키트의 "실제 중력 팔" (언로딩 등록 §6-2 h) 이 주 경로가 되어 갈래가 필요 없다) |
| 끝 조건 | 키트 §13-1 · §13-2 · §13-3 그대로 (`primary_status` · `trajectory_status` · `SELECTION_UNRESOLVED` · 분리 = 둘째 0 창 끝) |
| 기록 | 키트 C17 (창 끝 원자 · 벽 local · 쌍 · 메시 · 단 끝 restart) |
| 문헌 | 다이 압축 → release · springback 관찰 (`so2021_dem_mold_pressure…` §4 · `litdb-canon:so2022_dem_contact_model_assb_compaction_sintering` Fig 2 · Fig 7a) · 목표 도달 뒤 같은 속도로 후퇴 · 실험 대조는 **제하 뒤** 공극만 (`litdb-canon:zhang2026_xct_dem_cathode_calendering_peel_calibration` §3.5: 200 MPa 하중 중 ≈0.152 → 제하 뒤 ≈0.319 · LIB 압연 DEM) · 순수 SE 회복 규모 (§4-2 표 B) |
| 관련 결함 | `ULKR-01`–`12` · `UL-01`–`10` · `ULR1-01` · `03` · `05` · `RB-01` · `RB-02` |

### 2-7. 판 제거 · 자유 표면 유지

| 칸 | 내용 |
|---|---|
| 목적 | 판이 떨어진 뒤 (유효 판 접촉 0) 판을 치우고 자유 표면 상태의 두께 지표 · 공극을 잰다 — 실험의 "꺼낸 뒤 두께" 에 가장 가까운 **모델** 상태 (p p f — 다이 벽 · 탈형 · 측방 팽창은 없다 · 언로딩 등록 §9-1) |
| LIGGGHTS 골자 | 분리 선언 (키트 §13-3) 뒤 판을 위로 치움 (선택: 메시 삭제 — 판 접촉이 0 이면 지울 이력이 없다 · 벽 local 접촉 수 0 으로 확인) · 4 창 유지 · 표면 관측자 h_surf (키트 C5) — 키트의 분리 뒤 단계와 같고 "판을 치운다" 한 줄만 더한다 |
| 끝 조건 | 키트 S4 (h_surf 창 간 ≤ 0.002 µm) · S2 (KE) |
| 기록 | **ε_sphere,inside** (고정 S0 ID · 표면 지표 높이 기준 — 랩 펠릿 대조 연산자 · D9) · ε_union (보조) · h_surf · p99.9 · 이탈 입자 |
| 문헌 | in-die (하중 중) ↔ out-of-die (영 압력 · 탄성 회복 포함) 정의: *"The "in-die" (at pressure) accounts for powder deformation upon applying pressure … The "out-of-die" (zero pressure) analysis … also accounts for its elastic recovery."* (`litdb-canon:faka2026_particle_size_consolidation_strain_lpscl` §4.2 p.10) · 같은 구분의 측정 절차 (`litdb-canon:heck2026_densification_sulfide_se_binder_scalable` p.13) · 실험 측정 연산자 = 질량 / 진밀도 / 면적 / 두께 (판정문 Q3 표 · `bazzoun2025…` eq 2–3) |
| 관련 결함 | `MV-03` · `RB-01` · 판정문 Q3 |

### 2-8. 1저자 순서와 이 초안의 대응 (⬜ Q1 · Q2)

| 1저자 낱말 (D2) | 이 초안 | 실험 대응 | 비고 |
|---|---|---|---|
| insertion | 2-1 | 분말 계량 · 다이 충전 | |
| stabilization | 2-2 정착 + 판 배치 + 정지 | 다이 안 분말 · 펀치 접촉 | 세대 1 의 정착 (98.1) + 안정화 (9.81 · 감쇠 0.5 · 200,000 step) 두 조각을 하나로 |
| compression | 2-3 | 가압 (램프) | |
| servo (정적 300 MPa 유지) | 2-4 | 유지 (dwell) | |
| relaxation | 2-5 판 고정 정적 재확인 (R-a) | (해당 없음 — 모델 확인 단계) | 대안 R-b = 서보 유지 연장 (Q2) |
| plate remove → unloading | **2-6 언로딩 → 2-7 판 제거** (순서 바꿈 제안) | 하중 제거 → 꺼냄 (탈형) → 두께 측정 | 판은 하중을 뺀 뒤에야 떨어진다 · 키트도 분리로 끝난다 · 다른 해석 = "plate remove" 가 서보 해제 (판 고정 전환) 라면 그 자리는 2-5 (Q1) |

### 2-9. 거시 검증 세트도 같은 단계로 (D8)

| 세트 | 침대 | 단계 | 읽는 상태 | 세대 1 |
|---|---|---|---|---|
| 순수 SE Heckel 다압력 | 보정 침대와 같은 설계 (§4-4) · 압력마다 새 침대 · 같은 seed (짝 — 세대 1 seed 78049 꼴) | 2-1 – 2-7 · F_t 만 100 · 200 · 300 · 400 MPa | in-die Heckel = 2-5 끝 (정적 P) · out-of-die 꼴 Heckel = 2-7 (자유 표면) — 같은 런에서 둘 다 | `heckel/` · 생성기 `scripts/make_heckel_inputs.py` (압축 감쇠 0.5 · 처음 도달 정지) · `docs/data/heckel_pure_se_dem.csv` |
| 조성 (AM wt%) 공극 — Furnas dip | 세대 1 dip 근거와 같은 침대 설계 계열 (크기비 · RVE) · AM wt% 6–8 점 × seed 2 (설계 = 등록 때) | 같음 · 300 MPa | 2-5 끝 (ε_sphere · ε_union) + 2-7 | `all_dem_porosity.csv` · `docs/porosity_regression_final.md` · `scripts/fit_porosity_v4_global.py` |
| E_SE 보정 침대 | §4-4 (순수 SE 30 µm 급) | 같음 | 2-5 끝 (표적) | `docs/esse_calibration_2mAh_real_9.md` (복합 표적 13.5 % · 순수 SE 두 침대) |
| 복합 연속성 침대 | 2mAh_real_9 설계 · E* | 같음 | 2-5 · 2-7 | 같은 문서 |
| ps45 다섯 침대 | `dem_scripts/ps_sweep_6mah_20260914/` 설계 (세대 2 밀도 4.85 · 1.64 면 같은 질량에서 SE 개수 ×1.22 · AM ×0.99 · §3-2) | 2-1 – 2-7 (언로딩 포함) | 2-5 · 2-6 (ρ) · 2-7 (랩 대조) | 같은 덱 (세대 1) |

## 3. 물성 · 접촉 계수

### 3-1. 계수 표 (세대 1 = ps45 덱 `dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts` · Heckel 생성기 `scripts/make_heckel_inputs.py`)

| 계수 (덱 이름) | 세대 1 | 세대 2 제안 | 출처 (정본 카드 · 원장 · [미확인]) | 압축 영향 | 언로딩 · 되튐 영향 |
|---|---|---|---|---|---|
| E_AM (`youngsModulus` type 1 · 2) | 140 GPa (덱 1.4e8) | 그대로 | 다결정 NMC811 나노압입 138 ± 24 GPa · n = 29 (`litdb-canon:sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` p.4) · 원장 `CL-90` | 작음 (SE 가 지배) | 작음 |
| E_SE (type 3) | 1.35 GPa (덱 0.135e7 · 2mAh_real_9 복합 13.5 % 표적 · 세대 1 프로토콜에서 보정) | **다시 보정** (§4-5) · 표지 "보정 입력 (재료 E 아님)" | 재료 참고 (표적 아님): 1저자 보고 표의 SE 22 GPa = 재료 참고값 · DEM 입력 아님 (D10) · DFT 22.1 (`litdb-canon:deng2016_elastic_superionic_electrolytes_dft` Table III) · 27.4 (`litdb-canon:torii2025_lpscl_mechanical_anisotropy_dft`) · 나노압입 27.6 (`litdb-canon:lee2025_heckel_argyrodite_powder_densification_nanoindentation` Table 2) · 13 % 다공 펠릿 굽힘 4.7 ± 1.1 (`litdb-canon:song2025_porous_argyrodite_modulus_fracture_toughness` — 다른 양) · 24 = 유리 (`sakuda2013…` · MV-06) · 연화 = 1 % 겹침 규칙 밖 (§1 #15) | 강함 — 구속 일축 압축은 입자 강성에만 민감 (`litdb-canon:coetzee2017_dem_calibration_review` §5.5 p.131) | 강함 (같은 하중에서 겹침 ∝ 1/k) |
| ν_SE | 0.30 | **0.37** (E 보정 전에 고정) | DFT 0.37 (`deng2016…` Table III · `torii2025…`) · 모델 입력 0.37 (`bazzoun2026…`) · 0.33 (0.29–0.37) (`bazzoun2025…` Table 3) · DFT 범위 0.23–0.34 (`litdb-canon:pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament`) | E* ×1.054 → k_n ×1.043 [우리 산술 · 배경 식 (10)] → E 보정이 흡수 · 민감도 최저군 (`bazzoun2025…` Fig 14) | 작음 |
| ν_AM | 0.25 | 그대로 [측정 출처 없음 — 문헌 값도 모델 입력] | 0.27 (0.24–0.3) (`bazzoun2025…`) · 0.30 (`bazzoun2026…`) · 0.3 (`shi2019…` SI Table 1 · NMC532) | 최저군 | 작음 |
| ρ_SE | 2000 kg/m³ | **1640** (D4 · D10 — 1저자 보고 표 · 측정법 [미확인] · 진밀도 미확인 한정어) | 1저자 슬라이드 · 카드 대조 §3-3 | 같은 질량 처방의 SE 부피 몫 35.1 → 40.0 % (ρ_AM 4.85 와 함께) · SE 개수 ×1.22 · k_n ×0.961 · γ_n ×0.888 · dt_R ×0.906 [우리 산술 §3-2] — **침대 자체가 바뀐다** | 같음 + 중력 하중 |
| ρ_AM (PC · SC) | 4800 | **4850** (D10 — 1저자 보고 표 · 측정법 [미확인]) | 1저자 슬라이드 · 카드 대조: NCM811 4.76 (`litdb-canon:bielefeld2020_effective_ionic_conductivity_binder` §3.3 사용값) · 4.8 (`litdb-canon:lee2026_lpscl_coating_thickness_ncm811` SI Fig. S4) · 4.77 (`bazzoun2025…` Table 2 · `bazzoun2026…`) · 4.85 = NMC532 (`shi2019…` SI Table 1) | 같은 AM 질량에서 AM 부피 · 개수 ×0.990 · 복합 실험 공극 재기준에 +0.5 %p 몫 [우리 산술] · DEM 동역학 영향 ≈ 0 | ≈ 0 |
| e (`coefficientRestitution`) | 0.3 (전 쌍) | 0.3 그대로 + 민감도 팔 (0.5) | 권장 0.4–0.8 · r < 0.4 = 인위적 과감쇠 (`luding2008…` §2.3.1) · 0.4 (0.2–0.6) · 민감도 최저 (`bazzoun2025…` Fig 14) · 0.5 (`so2021…` Table 1 · `so2022_dem_contact_model…` Table 1) · 0.25 (`litdb-canon:otani2025_dem_se_dispersion_aggregation_compression`) · 0.3 (`litdb-canon:frankenberg2024_dem_high_intensity_mixer_assb` Table 3 · 혼합기 · 조대화) — 이력 모델의 e 는 감쇠 계수를 정하는 매개변수 (배경 §8.1) | 정적 끝점에는 약할 것 (방향 어림 — 팔로 확인) | 회복 진동 감쇠 · 소산 → 창 수 |
| μ (`coefficientFriction`) | 0.5 (전 쌍 · 판 · 바닥 포함) | 0.5 그대로 + 민감도 팔 | LPSCl 측정값 [미확인] · 0.5 (`so2021…` · `so2022…` · `otani2025…`) · 0.4 (0.2–0.6) · **μ_CAM–SE 최강 민감** (`bazzoun2025…` Fig 14) · LLZO/LGPS 0.3 · NMC 0.2 (`litdb-canon:lee2024_multiphysics_dem_fem_initial_pressure_assb` — 모델 입력) | 복합: 강함 · 순수 SE 구속 압축: 약함 (`coetzee2017…` p.131) | 접선 고착 → 회복 억제 가능 (크기 미상) |
| μ_r (`coefficientRollingFriction` · CDT) | AM–AM 0.2 · SE 낀 쌍 0.1 | 그대로 [미확인] + 언로딩 팔 (0) | *"purely empirical parameter that cannot be determined by direct measurement"* (`coetzee2017…` p.106 · Benvenuti 인용) · 0.01 (`otani2025…`) · 0.2 (선형 스프링 구름 · DAOR 보정 · `frankenberg2024…`) · 0.001 (`thakur2014…`) | 중간 (값의 물리 근거 없음) | ⚠ CDT 토크 크기 = μ_r·k_n·δ·R* — 이력력이 아니라 적재 직선 값 (배경 §7) → 제하 · 인장 접촉에서도 토크 유지 = 회복 저항 가능 |
| k̂₂/k₁ (`coefficientMaxElasticStiffness`) | 1.5 · 3 · 5 (AM–AM · AM–SE · SE–SE) | 그대로 [미확인 — 출처 기록 없음] + 언로딩 팔 | 예시 k₁/k̂₂ = 0.5 (= 2) (`luding2008…` Table 1·2) | 작음 (처녀 적재 = k₁ · 포화 경계만) | ★ 강함 — 제하 강성을 정한다: 포화 접촉 (δ_max ≥ δ_lim · SE 낀 접촉 대부분 — 언로딩 등록 §9-4 판독) 은 기울기 k̂₂ 의 한 직선으로 돌아가 영구 겹침 δ₀ = (1 − k₁/k̂₂)·δ_lim 만 남긴다 → 회복 변위 ≈ F/k̂₂ (k̂₂/k₁ 가 클수록 작다) · 비포화 접촉의 회복 겹침 = (k₁/k₂)·δ_max ≥ (k₁/k̂₂)·δ_max (AM–AM ≥ 2/3) [배경 식 (12)–(14)] |
| k_c/k₁ (`coefficientAdhesionStiffness` · k₁ 의 배수) | 1e5 · 2e5 · 1e6 | 그대로 [미확인] + ★ 언로딩 팔 (0 · 1 · 세대 1) | 예시 k_c/k̂₂ = 0.5 → k_c/k₁ = 1 (`luding2008…` Table 1·2) · k_c → ∞ 극한의 최대 인력 −(k₂ − k₁)·δ_max (`luding2008…` 카드 §4 · eq 6 해설 — 비포화 꼴) | 적재 무관 (δ → 0 근처 가지) | ★★ 가장 클 수 있다 — k_c/k₁ ≫ 1 이면 δ₀ 아래로 제하된 접촉이 δ → 0 직전까지 인장을 버틴다 (배경 §5.4 δ_a 표 · k_c → ∞ 극한의 최대 인력 ≈ (k₂ − k₁)·min(δ_max, δ_lim) [우리 산술 · 배경 식 (12)–(15)]) → 접촉 개구 · 판 분리 · 표면 회복을 억제할 수 있다 (크기 미상 — 팔로 잰다) |
| φ_F (`coefficientPlasticityDepth`) | 0.05 · 0.01 · 0.005 | 그대로 [미확인] | 예시 0.05 (`luding2008…` Table 1·2) | 포화 경계 δ_lim ∝ φ_F (배경 식 (11) · §5.4 표) | 포화 여부 · 영구 겹침 δ₀ ∝ δ_lim |
| V (`characteristicVelocity`) | 2.0 (덱) | 그대로 — E 보정과 묶인다 [출처 없음 · 강성 입력] | k_n ∝ E*^0.8·V^0.4·m*^0.2·R*^0.4 (배경 식 (10)) | E 와 축퇴 — V 를 바꾸면 보정 E 의 뜻이 바뀐다 | 같음 |
| 전역 감쇠 γ_g (`fix viscous`) | 정착 1e-5 · 안정화 · 압축 **0.5** · 이완 1e-5 | 준비 γ_prep · 압축 = 저항 몫 기준 (≤ 2 % 어림 · §2-3) · 서보 · 이완 · 언로딩 1e-5 | background friction (eq 22 · 카드 요약 "과댐핑 주의" — `luding2008…` §2.6) · 건식 압축 연구에서 전역 감쇠 보고 없음 (배경 §10.3 ④) | ★ 세대 1 결함 원인 (`DEMP-01`) | 언로딩 1e-5 (키트) |
| 중력 | 정착 98.1 → 9.81 (덱 · 자기 무게 10⁶ 배) | 준비 g_prep (수치 장치 · 기록) → 안정화부터 9.81e-6 (축척) | 판정문 §6 · `MV-05` | 30 µm 순수 SE 침대 바닥 자기 무게 0.43 MPa (g 9.81 · 300 MPa 의 0.14 %) [우리 산술] | P_meas 1 MPa 근처에서 지배 가능 (93 µm 창 2.97 MPa — 판정문 §6) |
| dt | 1e-6 (덱) | 그대로 + `fix check/timestep/gran` + dt/2 자격 | Rayleigh 몫 SE 1.03 % (E 1.35 · ρ 1640 · ν 0.37) → 2.31 % (E 6.75) · AM_S 1.58 % [우리 산술 · 배경 식 (4)] · 관행 10–30 % (배경 §3.3) · 사용 예 (`litdb-canon:shenouda2020_dem_metal_powder_am_liggghts_tutorial`) | — | 키트 물리 창 (dt 바뀌면 step 수 환산) |
| 판 속도 | 0.01 m/s (덱) = 0.01 mm/s | 그대로 (압축 포화 · 언로딩 이동) + v/2 사다리 | 1저자 10-12 용어 (배경 §9-1) · I < 10⁻⁴ (`thakur2014…`) · 속도 사다리 선례 (`litdb-canon:ngandjong2021_dem_calendering_digital_twin` §4-B — ε 를 고정한 사다리라 ε(P) 의 재하율 불변은 시험 안 함) | 재하율 교란 (CLAUDE.md MPM 재하율 함정과 같은 부류) | 키트 v₀ · v₀/2 결정표 |
| 축척 규약 | r × 1000 · E × 0.001 · P × 0.001 · ρ × 1 | 그대로 (조대화 아님) | 조대화 사례 = 힘 f² 축척 (`frankenberg2024…`) · 길이 100 배 + 자료 없는 일치 주장 · 점착 상사 깨짐 (`otani2025…`) | 정적 상사 (σ/E · δ/r) 유지 · 덱 시계 31,600 배 느림 (배경 §9-1) | 같음 |
| 판 · 바닥 재질 | type 1 (AM_P 행 — 판–SE 접촉 = AM_P–SE 계수) | 그대로 · 표기 | 다이 · 펀치 마찰 [미확인] · DEM 벽 Y 70 GPa (`faka2026…` SI Table S5) | 벽 근처 공극 → 보정은 안쪽 영역 (§4-4) | 판 접촉 이력 = 언로딩 주 관측 |

- 세대 3 후보 (이 계획 밖): 항복 캡이 있는 법칙 — Thornton–Ning (`litdb-canon:thorntonning1998_adhesive_elastoplastic_contact`) · MDR (`litdb-canon:zunker2024_mdr_contact_model_partI` · `litdb-canon:zunker2025_dem_large_deformation_compaction`) · 경도 문턱 (`so2022_dem_contact_model…`) · 다접촉 (`litdb-canon:giannis2021_stress_based_multicontact_dem` · `litdb-canon:varkey2026_multicontact_elastoplastic_dem`).  SE 영률을 연화하지 않고 캡으로 압축 응답을 맞추는 접근이다 (배경 §10.3 ③ — 해석).

### 3-2. 진밀도 · 조성 환산 [우리 산술]

| ρ_AM · ρ_SE (g/cm³) | 81.6 : 18.4 질량 처방의 SE 부피 몫 (고체 중) | 같은 질량의 개수 (세대 1 덱 대비) | ps45 7:3 입자 수 (덱 계획 160,422) |
|---|---|---|---|
| 4.8 · 2.0 (세대 1 덱) | 35.11 % | ×1 | 160,422 |
| 4.85 · 1.86 (SE 결정학 — `lee2025_heckel…` 카드 §3-4 [우리 산술]) | 37.03 % | AM ×0.990 · SE ×1.075 | — |
| **4.85 · 1.64 (세대 2 · D10)** | **40.01 %** | **AM ×0.990 · SE ×1.220** | **≈ 195,300 (+21.7 %)** |

- 식: SE 부피 몫 = (w_SE/ρ_SE) ÷ (w_AM/ρ_AM + w_SE/ρ_SE).  NCM 4.8 → 4.85 하나만의 몫 = 고체 부피 ×0.994 (SE 1.64 에서).
- 같은 면적 용량 (AM 질량 / 면적 고정 · 6 mAh/cm²) 이면 고체 부피 ×1.070 → 두께 ≈ +7.0 % (같은 공극에서) — 세대 2 ps45 침대는 세대 1 보다 두껍고 입자가 많다 (비용 §7).
- ⚠ 1저자 보고 표 (D10) 가 적은 입자 수 159,000–163,000 개는 세대 1 덱 (4.8 · 2.0) 의 ps45 침대 값이다 — 같은 표의 밀도 4.85 · 1.64 로 돌린 침대가 아니다 (세대 1 침대 = 덱 값이 사실 · 역사).
- 질량 의존 동역학 (SE–SE · 2.0 → 1.64): k_n ∝ m*^0.2 → ×0.961 · γ_n ∝ (m*·k_n)^0.5 ∝ m*^0.6 → ×0.888 · Rayleigh dt_R ∝ ρ^0.5 → ×0.906 (배경 식 (4) · (9) · (10)) ⇒ 같은 E_SE 라도 세대 1 과 강성 · 감쇠가 같지 않다 — §4 에서 E 를 다시 잡는 이유 하나.

### 3-3. 진밀도 출처 대조 — 작업 지시의 카드 목록 정정

| 값 | 원문에 인쇄된 값 (카드 표지) | 카드에 있지만 원문 값이 아닌 것 |
|---|---|---|
| 1.64 | `bazzoun2025…` Table 2 (stated · ρ_CAM 4.77 함께) · `bazzoun2026…` (재료 파라미터) · `lee2025_heckel…` SI p.3 *"calculated"* TD (카드 §3-4: 결정학 1.860 보다 12 % 낮고 같은 논문 단면 공극 2.5 % 와 양립하지 않는다 → 오기 가능성 · 저자 확인 필요) · `lee2026_lpscl_coating_thickness_ncm811` SI Fig. S4 (ρ_NCM811 4.8 함께) | `litdb-canon:alabdali2023_cgmd_wet_manufacturing_ssb_cathode` — 카드: *"밀도는 논문에 없다 (우리가 문헌값 대입)"* · `litdb-canon:cho2024_conflicting_roles_conductive_additive` — 카드 §12 의 vol% 환산 지시 (우리 문장) |
| 1.86–1.88 | `litdb-canon:miss2026_insitu_conductivity_porosity_pressure_compaction` Table S1 1.87 (결정밀도 · Adeli 2019) · `faka2026…` SI Table S5 1.87 (DEM 입력) · `litdb-canon:minnmann2021_jes_charge_transport_bottlenecks` 재료 표 1.87 · `litdb-canon:ketter2025_resistor_network_models_predict_transport_properties` 1.86 (Deiseroth 2008) · `litdb-canon:doux2020_stack_pressure_assb` Table S2 TD 1.860 · `litdb-canon:thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` 본문의 문헌 TD 1.77–1.88 · (다른 재료) `sakuda2013…` 유리 1.88 · `shi2019…` LPS 유리 1.87 | `litdb-canon:kraft2017_lattice_polarizability_argyrodite_Li6PS5X` — 카드: *"Cl d≈1.86 … 우리 back-of-envelope 추정"* · `lee2025_heckel…` 카드의 결정학 1.860 = [우리 산술] (Adeli 2019 격자상수) |

⇒ 1.64 를 **인쇄한** 정본 카드는 넷 (Bazzoun 2025 · 2026 · Lee 2025 · Lee 2026) 이고 그 계산 근거를 적은 카드는 없다 [미확인].  1.86–1.88 은 결정밀도 계열 다섯 이상.  세대 2 = SE 1.64 · NCM 4.85 (D4 · D10 — 1저자 보고 표 · 랩 측정법 리포 미기록) · 한정어 = *"진밀도 미확인 — SE 는 결정학 1.86 과 12 % 차"*.  작업 지시의 "1.64 (Bazzoun · cho2024 · alabdali)" · "1.86–1.87 (Kraft · faka2026 · Minnmann)" 중 cho2024 · alabdali · Kraft 의 값은 원문 값이 아니다 (위 표 오른쪽 열).

## 4. 보정 설계

### 4-1. 결정 기록 — 공극 정의 (D9 · 열린 질문 아님)

| 칸 | 결정 |
|---|---|
| 보정 표적 (estimand) | **ε_union** (정확 union — 다중 겹침 · 판 · 바닥 절단 포함 · MC 표본 수 · seed · 표준오차 기록) · 순수 SE 보정 침대 · **2-5 이완 끝 프레임** · 창 **10–13 %** |
| 함께 보존 | **ε_sphere** (= 1 − Σ(4/3)πr³ ÷ (A·h) · 고정 ID 집합 · 판 안 집합 따로) — 모든 단계 기록 · 모든 침대 |
| 실험 대조 | 랩 펠릿 (질량 + 두께 · 진밀도 1.64 가정) ↔ **ε_sphere** (같은 연산자 — 판정문 Q3 표 첫 줄 · `bazzoun2025…` eq 2–3) · 상태 맞춤 = 랩이 두께를 잰 상태 (꺼낸 뒤면 2-7) — ⬜ Q9 |
| 연산자 명세 | 정확 union = `scripts/dem_analysis_core.py` `calc_porosity_union_exact` · `scripts/lhs_union_webapp.py` 꼴 (MC) · ⚠ 쌍 렌즈 union (`calc_porosity_dual` — 세대 1 순수 SE 10.08 · 11.64 % 의 연산자) 은 정확 union 이 아니다 (세 구 반례 2.045 %p · 판정문 MV-03) → 세대 1 과 잇는 **연속성 칸**으로만 함께 적는다 |
| 영역 | 안쪽 (위 · 아래 벽에서 SE 지름 2–4 개를 뺀 띠 — `bazzoun2025…` §4 의 ω = 0.7 꼴) 과 전체 높이 둘 다 — 표적 영역 = ⬜ Q11 (권고 안쪽) |
| ⛔ 한정어 (MV-03 · 떼지 말 것) | 세대 1 순수 SE 두 런에서 정의만 바꿔도 **12.42 · 11.41 %p** 움직였다 (ε_sphere −2.34 ↔ ε_union 10.08 % · 0.23 ↔ 11.64 %) — 같은 질량을 union 부피에 넣으려면 밀도 ×1.138 · ×1.129 가 필요하다 · **union 을 맞춘 것이 실험 질량 공극을 맞춘 것은 아니다** (판정문 MV-03) |

### 4-2. 표적의 지위 · 문헌 맥락

- 지위: 1저자 랩 표준 (D6 · 측정법 미확인 · 랩에 밀도 측정법이 없다 — 진행 기록 10-14 저녁 ③).  ⚠ 같은 숫자대의 옛 앵커 "순수 SE 10 % · 300 MPa" 는 출처 철회 (`CL-94` — 우리 MPM 보정 수렴값).  10–13 % 가 같은 계보라면 DEM E 를 MPM 값에 맞추는 frame [4] 교차 맞춤이 된다 → 출처 기록 = ⬜ Q8 · 독립 대조 = 랩 EIS 펠릿의 ε_sphere.

**표 A — 순수 SE 계열 펠릿 공극 (300 MPa 근처 · 보정 표적 아님 — 정의 · 상태 · 재료가 섞여 있다)**

| 정본 카드 | 재료 · 입경 | 상태 | 진밀도 기준 | 공극 | 표지 |
|---|---|---|---|---|---|
| `doux2020_stack_pressure_assb` | LPSCl (NEI) · 13 mm · 200 mg | 370 MPa · **다이 밖** | 1.860 | 4 개 평균 상대밀도 82.1 % → **≈18 %** (측정 밀도 1.522) · 같은 측정값을 1.64 로 쓰면 **7.2 %** [우리 산술] | Table S2 |
| `miss2026_insitu…` | µc-Li₅.₅PS₄.₅Cl₁.₅ | 다이 안 하중 중 / 놓은 뒤 (다이 안) | 1.87 (결정) | 7.1–7.6 % / 8.6 % | [재계산] Table S2 |
| `lee2025_heckel…` | 상용 LPSCl (POSCO JK) · 연속 가압 1 mm/min | 다이 안 하중 중 | 1.64 (인쇄 · 의심) | ≈15 % (1.86 이면 ≈25 %) | [판독] Fig 1d · 카드 §3-4 |
| `faka2026…` | AMG LPSCl D50 40 · 20 · 11 · 4 µm | 다이 안 · 0.3 GPa | 결정 (Rietveld) | 12.9 · 16.0 · 22.5 · 26.3 % | [판독] Fig S2 |
| `thompson2026…` | LPSCl (NEI · 입경 ≈5 µm 추정) | 준등방 · 하중 중 | 결정 1.861 | ≈16 % (331–334 MPa) | 카드 [우리 산술] |

⇒ 7–26 % 범위 — 진밀도 기준 · 입경 · 상태 (다이 안 · 밖) · 재료가 갈라 놓는다 → **어느 것도 이 모델의 보정 표적이 아니다** (맥락).  1 µm 랩 분말의 10–13 % 는 faka2026 의 "입경이 작을수록 같은 압력 공극 ↑" 경향과 긴장 관계 — 진밀도 기준 · 측정 상태 차이로 설명되는지는 미분리.

**표 B — 순수 SE 계열 하중 제거 회복 (두께)**

| 정본 카드 | 회복 | 조건 · 표지 |
|---|---|---|
| `miss2026_insitu…` | **1.62 %** (300 MPa → 놓음 · 다이 안) · 전 압력 −0.3 – +2.8 % · 400 MPa 뒤 다이 밖 +6.5 % | µc-Li₅.₅PS₄.₅Cl₁.₅ · [재계산] Table S2 · [판독] Fig 3a |
| `lee2025_heckel…` | 0.233 mm ≈ **4.7 %** (≈900 MPa → 0 · 다이 안) | 한 시료 · [판독] Fig 1c |
| `heck2026_densification…` | 1.5 → 0.01 GPa in-die 두께 **+6.9 %** (≈ 고체 탄성 팽창 크기) | β-Li₃PS₄ 분말 · [판독 · 카드 산술] Fig 10 |

⇒ 순수 SE 회복 1.6–7 % → 공극 +1.4 – +4 %p (ε 11.5 % 출발 · 같은 고체 부피: ε′ = 1 − (1 − ε)/(1 + r)) [우리 산술] — **표적 창 폭 (3 %p) 과 같은 크기** → 실험 대조는 상태를 맞춰야 한다 (Q9).

### 4-3. 진밀도의 무게 — 정의 차 (12 %p) 와 같은 크기 [우리 산술]

**랩 펠릿 (LPSCl 0.100 g · 지름 10.00 mm · ε = 1 − m/(ρ·A·t))**

| 두께 t (mm) | 겉보기 밀도 (g/cm³) | ε (TD 1.64) | ε (TD 1.86) |
|---|---|---|---|
| 0.750 | 1.698 | −3.5 % (불가능) | 8.7 % |
| 0.776 | 1.641 | 0 % (경계) | 11.8 % |
| 0.800 | 1.592 | 3.0 % | 14.4 % |
| 0.850 | 1.498 | 8.7 % | 19.5 % |
| 0.900 | 1.415 | 13.7 % | 23.9 % |

- TD 1.64 에서 ε 10–13 % 가 되려면 t ≈ 0.863–0.892 mm · 두께 0.01 mm ≈ 공극 1.2 %p · TD 1.64 ↔ 1.86 의 차 ≈ **11 %p** (MV-03 정의 차 12.42 · 11.41 %p 와 같은 크기).
- ⇒ **값싼 반증 시험**: 질량 0.100 g · 지름 10.00 mm 펠릿이 **0.776 mm 보다 얇으면 TD 1.64 는 물리적으로 불가능** (공극 < 0) — 질량 ±0.1 mg · 두께 ±0.01 mm 로 재면 판별된다 (Q7).
- 랩 EIS ① 펠릿 조건 (진행 기록 10-14 낮 ② · 오후 ② · 오후 3 ④ · 저녁 ③): LPSCl 0.1 g · 10 Φ · **300 MPa 성형** · 두께는 1저자가 잰다 (*"두께도 얼추 재볼게"*) · EIS 측정 지그 압력 **100–150 MPa** (한 값 고정) · 랩에 밀도 측정법 없음.  같은 기록의 어림 두께 0.75–0.85 mm 는 TD 1.64 경계 (0.776 mm) 를 끼고 있다 → 이 측정이 경계를 가른다.  ⚠ 두께를 재는 상태 (성형 다이 안 · 꺼낸 뒤 · 지그 안 100–150 MPa) 가 대조 상태를 정한다 (Q9).
- **ps45 실험 공극의 재기준** (1저자 10-09 값 = TD AM 4.8 · SE 2.0 · 질량비 81.6 : 18.4 · 같은 질량 · 두께): 10:0 26.18 → **20.98** · 7:3 22.24 → **16.77** · 5:5 24.54 → **19.23** · 3:7 25.64 → **20.41** · 0:10 29.75 → **24.81 %** (세대 2 TD = AM 4.85 · SE 1.64 · 차 −4.9 – −5.5 %p) · 식 (1 − ε′) = (1 − ε)·Σ(w/ρ)′/Σ(w/ρ) = (1 − ε) × 1.0704.  이 차는 언로딩 가설의 동기였던 "실험–DEM 차" (5.7–9.3 %p · `miss2026_insitu…` 카드 표) 와 같은 크기다 ⇒ **그 차를 해석하기 전에 진밀도 결정이 먼저**다 (언로딩 등록 §1-2 · `RB-01`).
- Doux 2020 (표 A) 도 같은 측정값이 TD 1.860 이면 18 % · 1.64 면 7.2 %.

### 4-4. 보정 침대

| 칸 | 제안 | 근거 |
|---|---|---|
| 재료 | 순수 SE · r 0.5 µm (단일 크기) | 랩 SE 소립 1 µm (진행 기록 10-14 저녁 ③) |
| 측방 | 50 × 50 µm 주기 (생산 RVE 와 같음) = SE 지름 50 개 | 세대 1 덱 |
| 두께 | 최종 ≈ 30 µm (SE 지름 30 개) → N ≈ 1.25–1.29 × 10⁵ (고체분율 0.87–0.90) [우리 산술] | 세대 1 300 MPa 침대 8.24 µm (지름 8 개) 는 벽 띠가 큰 몫 [어림] · 벽 2–4 지름 = bulk 아님 (`bazzoun2025…` §4 · box factor · ω) |
| 영역 | 안쪽 + 전체 둘 다 기록 | §4-1 · Q11 |
| seed | 사다리 = seed 1 (짝) · E* = seed 3 | 독립 실현 3 개 (`bazzoun2025…` §4 · `shi2019…` *"at least three"*) |
| 준비 | E 마다 삽입부터 새로 (짝 seed) — 한 정착 상태에서 E 만 갈라 내지 않는다 | 판정문 §5 V4 표 셋째 줄 (fresh 준비 / 압축 = 생산 일반화용 estimand) |
| 두께 수렴 | E* 에서 20 · 40 µm 한 쌍 (안쪽 ε_union 차 ≤ 0.5 %p — 숫자는 등록) | 벽 영향 크기 확인 |
| 중력 | g_final (§2-2) | `MV-05` |

### 4-5. E 사다리

- **estimand**: E_SE* = 다른 모든 입력 (ν_SE · ρ · V · k̂₂/k₁ · k_c/k₁ · φ_F · μ · μ_r · e · 중력 · 프로토콜) 을 고정했을 때 안쪽 ε_union (2-5 끝) 이 **11.5 %** (창 가운데) 를 지나는 E_SE 입력 + 창 10–13 % 에 대응하는 E 구간.  ⚠ `hooke/hysteresis` 의 k_n ∝ E*^0.8·V^0.4·m*^0.2·R*^0.4 (배경 식 (10)) — E_SE* 는 **보정된 접촉 강성 입력**이지 재료 영률이 아니다 (V · ρ · ν 와 함께 보고).
- **1 차**: E ∈ {1.35 · 2.0 · 3.0 · 4.5 · 6.75} GPa (×1.5 등비 · seed 1) → 표적을 끼는 두 점 → 그 안에 두 점 더 → **ln E 선형 보간** (등록) → E* 에서 seed 3.
- **단조성**: ε_union(E) 가 seed 산포보다 크게 단조를 깨면 보간하지 않고 보고 (미식별).
- **dt**: Rayleigh 몫 SE 1.03 % (E 1.35) → 2.31 % (E 6.75) [우리 산술] — `fix check/timestep/gran` 로 런 중 기록 · dt/2 는 자격 런에서 (§4-9 ②).
- **겹침 보고**: E* 의 ⟨δ⟩/d · 최대 — 1 % 규칙 (`paulick2015…`) 밖이면 "보정 프록시" 표지 그대로.
- **하지 않는 것**: 24 GPa 끝점 (유리 계보 · MV-06 — 필요하면 "고강성 시나리오" 이름으로 따로) · 복합 침대로 E 맞추기 · 같은 체크포인트 재평형 (V4 의 다른 estimand — 판정문 §5).
- 보정에 쓰지 않는 자료: Heckel 100 · 200 · 400 · out-of-die · 조성 사다리 · 복합 · ps45 · 랩 펠릿 = 전부 **검증** (§4-8).

### 4-6. 결과 전 기대 (등록 문서로 옮길 후보 · 판정 아님)

| # | 기대 | 반증 · 처리 | 근거 |
|---|---|---|---|
| X1 | 방향: **E_SE* > 1.35 GPa** | 세대 2 · E 1.35 의 안쪽 ε_union ≥ 10 % → E* ≤ 1.35 가능 → 보고 (억지 맞춤 없음) | 가지 B: 같은 E 에서 정적 서보가 ε_sphere −4.18 %p · X2 어림 · 두꺼운 침대는 벽 띠 몫이 작다 (방향) · ρ (k_n ×0.961) 와 ν (×1.043) 는 거의 상쇄 [우리 산술] |
| X2 | **다리 팔** (세대 1 Heckel 침대 · seed 78049 · ρ 2.0 · ν 0.30 · E 1.35 · 중력 세대 1 그대로 — **프로토콜만** 세대 2): Heckel 기울기 K = 0.007257 /MPa 의 ±20 % 안 · 각 압력의 ln(1/(1−D)) 증가 0.2–0.4 (affine 일정 저항 오프셋 40.25 MPa × K = 0.29) → 쌍 렌즈 union ≈ 23.1 · 14.2 · 7.5 · 2.5 % (100 · 200 · 300 · 400 MPa) [어림] | 어느 압력이든 증가 ≤ 0 · K 가 ±20 % 밖 · 증가가 압력에 크게 의존 (예: Δ(100) > 2·Δ(400)) → `DEMP-01` 저항 오프셋 모형 기각 (기전 다시) | 분기 README §9 (affine 저항 · N/300,000) · `docs/data/heckel_pure_se_dem.csv` (K · A · R²) |
| X3 | 검증 Heckel (E* · 세대 2 침대): 100–400 MPa 선형 R² ≥ 0.95 (세대 1 0.9653) · P_y 방향 > 137.8 MPa (E* > 1.35 → 같은 압력 증분당 치밀화 ↓ — 어림) · 크기 미등록 | R² < 0.95 → 곡률 보고 (E 재맞춤 없음) · P_y ≤ 137.8 → 보고 | 문헌 in-die P_y (기준 아님): 상용 LPSCl 294–344 MPa (`lee2025_heckel…` Table 1 K → [우리 산술 · 카드]) · AMG 280–700 (`faka2026…` Fig S2 · PSD · 카드 산술) · β-Li₃PS₄ ≈260 (`heck2026…` Fig 10 · 카드 산술) · in-die Heckel 단계 I–III 관행 (`lee2025_heckel…` · `litdb-canon:schneider2023_particle_size_pressure_transport`) |
| X4 | 같은 런의 out-of-die 꼴 (2-7) D < in-die (2-5) D — 모든 압력 | 반대면 언로딩 판독 점검 (TECH 의심) | in-die / out-of-die 정의 (`faka2026…` p.10 · `heck2026…` p.13) |
| X5 | 다리 팔 조성 셋 (SE 많음 · dip 근처 · AM 많음): Δε (세대 2 − 세대 1) 가 SE 많은 쪽에서 더 음수 (저항 몫 ∝ N · SE 가 많을수록 N ↑) | 순서가 반대 → 저항 몫 모형 재검토 | 분기 README §9 |
| X6 | 조성 사다리 (E*): 국소 최소 (dip) 위치 AM 70–90 wt% 안 | 최소 없음 · 범위 밖 → "dip = 기하 패킹" 해석 약화로 보고 | 세대 1 DEM/v4 AM 75–85 wt% (CLAUDE.md frame [3]) · 임계 크기비 ≥ 약 7 (`litdb-canon:mcgeary1961_bimodal_sphere_packing`) · 경질 + 연질 혼합 압밀 DEM (`litdb-canon:martinbouvard2003_dem_composite_cold_compaction`) |
| X7 | 언로딩: 모든 침대 ρ > 0 (키트 E1) · 순수 SE 회복 크기 = **미등록** (k̂₂/k₁ · k_c/k₁ 의존 미상) | 키트 규칙 | 문헌 규모 1.6–7 % (표 B) 는 맥락만 |

### 4-7. 거시 검증 세트 다시 하기 (D8) — E_SE 재보정과의 순서

| 단계 | 무엇 | 재보정과의 순서 | 결과 전 기대 |
|---|---|---|---|
| V0 | 언로딩 키트 수정 + Codex 재확인 GO | 선행 | — |
| V1 | 자격 런 (작은 침대 · §4-9 ②) | 보정 전 | — |
| V2 | **다리 팔** (E 1.35 · 프로토콜만 세대 2): Heckel 4 압력 + 조성 셋 | 보정과 병렬 가능 (E* 를 쓰지 않는다) | X2 · X5 |
| V3 | E 사다리 → **E* 커밋 (봉인)** | — | X1 |
| V4 | Heckel 100 · 200 · 400 MPa (+ 300 = 보정 점 재사용) · seed 2 · in-die + out-of-die 꼴 | E* 봉인 뒤 | X3 · X4 |
| V5 | 조성 사다리 (dip) · seed 2 | E* 봉인 뒤 | X6 |
| V6 | 복합 연속성 (2mAh_real_9 설계) | E* 봉인 뒤 | 외부 표적 없음 — 13.5 % 는 세대 1 모델 참조값 (판정문 V3) · 보고만 |
| V7 | ps45 다섯 침대 (언로딩 포함) | E* 봉인 뒤 | X7 · 랩 대조 = 탐색 (랩 값 = 추린 3 개 평균 · TD 1.64 재기준 §4-3 · 언로딩 등록 §1-2) |
| V8 | Codex (결과) → 생산 재실행 범위 (sentinel 짝 비교 — 판정문 Q2) | 마지막 | — |

- 역사가 되는 세대 1 숫자 = §6-2.

### 4-8. 보정 ↔ 검증 분리 · 판정식

- 보정 자료 = 순수 SE 300 MPa (2-5 끝) **하나**.  검증 = 나머지 전부 (Heckel 100 · 200 · 400 · out-of-die · 조성 · 복합 · ps45 · 랩 펠릿).  *"It is also important that the calibration experiment is different from the final experiment or application being modelled. If the final application is used to calibrate the parameter values, the exercise is nothing more than a parameter sensitivity study"* (`coetzee2017…` §2 p.106).
- 구속 일축 압축은 입자 강성에만 민감하다 (`coetzee2017…` §5.5 p.131) → 순수 SE 압축으로 E 를 잡는 것은 문헌 표준 경로 · 마찰은 이 시험으로 못 잡는다 (μ = §3 민감도 팔).
- 실험 대조 판정식 (판정문 Q4): d = ε_DEM − ε_lab (같은 상태 · 같은 연산자) · U_lab (반복 시료 · 질량 · 진밀도 · 면적 · 두께 — 공통 계통 항 보존) · U_seed · B_num (dt · 유지 · 제어 · 후처리 · 보존) · 실용 폭 δ_ε 는 결과 전에 1저자가 정하고 **전체 구간이 δ_ε 안일 때만 "동등"** · 걸치면 미판정.  펠릿 1 개로는 불확도가 없다 → 파일럿 ≥ 3 개 (판정문 Q4 *"분산을 보기 시작하는 파일럿 최소안"*).

### 4-9. 순서 (판정문 §8 순서 + 언로딩 선행)

① 측정량 정의 (§4-1) · 랩 자료 요청 (Q7 · Q8 · Q9) · 중력 · 준비 정책 (Q5)
② 수치 자격 (작은 침대 ≈ 6 × 10⁴ 입자 · 15 µm): 정적 평형 (MV-01) · 이력 연속 (MV-02) · 보존 (MV-08) · 중력 2×2 (준비 g 98.1 / 9.81e-6 × 최종 g 9.81 / 9.81e-6 — 판정문 §6 3 단계) · dt/2 · v/2 · γ_comp 후보 셋 · e 0.5 팔 · μ 팔 · 두께 쌍 · 언로딩 민감 계수 팔 (k̂₂/k₁ · k_c/k₁ · μ_r — 크기부터)
③ 다리 팔 (병렬) ④ E 사다리 → E* 봉인 ⑤ 검증 세트 ⑥ Codex — 각 단계 = 등록 (결과 전) → 런 → 기록 (결과를 본 뒤 띠 · 문턱을 옮기지 않는다).

## 5. 시험 먼저 (키트 H0–H5 꼴 — 반례를 먼저 시험으로 옮겨 고치기 전 실패를 본다)

| # | 시험 | 막는 것 | 고치기 전 (세대 1 덱 · 도구) 기대 | 통과 | 어디 |
|---|---|---|---|---|---|
| T0 | 덱 문법 · 부호 (Ut0 꼴 · 20 입자 fixture) | 문법 · 판 힘 부호 · 단위 | — | 모든 경로 지남 (판정 아님) | ibb · WSL |
| T1 | fix 재생성 lint — 안정화 → 분리 사이에 `top_mesh` · `zwall_top` 의 unfix · 재정의 0 | MV-02 | 가지 B 덱 = 위반 (214–242 행) | 세대 2 덱 0 곳 | 컨테이너 (생성기 selftest) |
| T2 | 판 접촉 이력 연속 — move/mesh 를 끊고 다시 걸어도 판–입자 δ_max · 접선 이력 같음 · 판 위치 = 덱 공식 (메시 덤프 대조) + 음성 대조 (벽 fix 재생성 → 달라짐) | MV-02 | 키트 이력 시험 (`docs/data/ps45_unload_20261009/history_test/make_history_decks.py` · H1 · H3–H4) 꼴 재사용 · 반복 정의 문법 = 키트 수정 계획 Q8 fixture 와 같은 묶음 | 같음 / 다름 둘 다 | ibb fixture |
| T3 | 정적 평형 판정기 — 판정문 반례 (KE 0.5 J · 초기 구간 뒤 KE 0.009 J) 거부 · 정적 양성 수용 · 예산 소진 = `NOT_CONVERGED` | MV-01 | 가지 B 수렴식 = 반례 수용 (10 · 14 번째 CONVERGED) | 반례 거부 · 양성 수용 | 컨테이너 (합성 궤적) |
| T4 | 보존 회계 — 상별 · ID 별 손실 · 판 위 · 바닥 아래 · 공극 기여 | MV-08 · DEMP-02 | 가지 B 수 가드 = AM 50 개 손실 허용 (6.87 %p) | 설명 안 되는 AM 손실 = FAIL · 허용 손실 ≤ 예산 | 컨테이너 (합성 덤프) |
| T5 | 공극 연산자 — ε_sphere (고정 ID · inside) · 정확 union (MC · 표본오차) · 안쪽 영역 · 쌍 렌즈 (연속성) | MV-03 | 쌍 렌즈를 정확이라 부르면 세 구 반례 2.045 %p | 해석해 (두 구 · 세 구 · 벽 절단 구) 와 MC 1σ 안 | 컨테이너 |
| T6 | 힘 수지 회계 — −γΣv_z · 중력 · 관성 · 판 · 바닥 | DEMP-01 · MV-01 | — | 평형 사슬 = 통과 · 불평형 = 실패 (키트 S3 꼴) | 컨테이너 |
| T7 | 중력 축척 — g 9.81e-6 fixture 의 자기 무게 수지 · g 전환 지점 | MV-05 | — | 수지 1e-3 안 | ibb fixture |
| T8 | run 사이 읽기 lint (write_restart 뒤 ke · run 0 뒤 판 힘 · 없는 fix) | `SELF-98` 꼴 | t0 1 회 덱 = 6 곳 (분기 README §12-2) | 0 곳 | 컨테이너 (분기 생성기 `docs/data/ps73_damping_branch_20261007/make_branch_decks.py` ⑭a · ⑭b 재사용) |
| T9 | 삽입 재고 — 상별 개수 · 구 부피 · 질량 = 처방 (ρ 1.64) · NP ≤ 2 삽입 · 템플릿 절삭 폭 | `PS-01` · `SELF-70` | 4 · 10 rank 부분 삽입 (덱 주석) | 허용 폭 안 | WSL · ibb fixture |
| T10 | dt 자격 — `check/timestep/gran` 로그 파서 · dt/2 같은 물리 시간 끝점 비교 | MV-06 | t0 만 (dt 자격 아님) | Rayleigh 몫 기록 · dt/2 차 ≤ 예산 | 컨테이너 (파서) · ibb (작은 침대) |
| T11 | 덱 수준 서보 고리 — 합성 판 힘 응답 (선형 강성 · 지연) 에서 포화 · 비례 · 부호 · 진동 감지 | 제어 | — | 목표 수렴 · 포화 = v_max · 발산 = 가드 | 컨테이너 (모의) |
| T12 | 언로딩 키트 접합 — 세대 2 의 2-5 끝 = S0 · 키트 판독기 · 관문 (ULKR 수정판) 이 세대 2 기록을 읽는다 | `ULKR-01`–`12` | 수정 전 키트 = Codex 반례 수용 | Codex 재확인 GO 판으로 통과 | 컨테이너 |
| T13 | 재개 — 세대 2 체크포인트 이름 · 재개 덱 · G1–G3 | 재개 사고 (`SELF-54`) | `scripts/resume_ckpt.sh` 는 세대 1 이름 (compress > after_settling > settling) 으로 모드를 고른다 → 세대 2 단계를 모른다 | 단계마다 재개 G1–G3 통과 (`docs/resume_ckpt_procedure_20260927.md` 기준 그대로) | ibb fixture |
| T14 | (Q3 (나) 를 고를 때만) 내장 서보 `fix_modify` — `servo/integrate stop` 동안 판 정지 · `target_val` 계단 · `ctrlParam` 이 run 사이에 먹는다 · 같은 fix 라 판 접촉 이력 유지 · 사본 판 = 설치 빌드 판 | MV-02 · 문법 | 세션 스크래치 소스 사본 판독뿐 (리포 밖 · 판 미확인) | 판 위치 · 힘 · 이력 = 기대대로 | ibb fixture |

## 6. 세대 1 결과 영향 · 표지

### 6-1. 세대 1 자료 (지우지 않는다)

| 자료 | 자리 | 세대 1 인 이유 | 한정어 (§6-3 번호) |
|---|---|---|---|
| LHS 194 (130 + 64) · 보충 20 · 후막 짝 8 DEM 침대 | WSL · ibb (리포에 덱 원본 없음 — 2-type 템플릿 = 같은 프로토콜 확인 · 3-type 미확인 · `DEMP-01` note) | 압축 감쇠 0.5 · 처음 도달 정지 | ① ② ③ ④ |
| 접촉망 194 · 보충 20 배치 (10-14 발사) · 배포 v1 · v1.1 · v1.2 · v1.3 | `docs/data/lhs_release_20261006_v12/README.md` · `docs/reviews/lhs_release_v13_plan_20261007.md` | 세대 1 침대 위의 접촉망 세대 2 | "DEM 프로토콜 세대 1 × 접촉망 세대 2" |
| ps45 다섯 침대 + 파생 (union · 단면 하중 · 압밀 곡선 · σ_e · 망 g2 · 언로딩 S0) | `dem_scripts/ps_sweep_6mah_20260914/` · `docs/data/ps45_r45_union_20260929/README.md` · `docs/data/ps45_plane_load_20261007/README.md` · `docs/data/ps73_compaction_curve_20261006/README.md` | 같음 | ① ② ③ ④ ⑤ + 언로딩 = "세대 1 침대의 언로딩 시험" |
| 가지 B (DEMP-01) | 분기 README §12-4 | 세대 1 압축 + 서보 유지 (fix 재생성 · MV-02) | "모델 내부 진단 · 세대 혼합" |
| 순수 SE Heckel 4 압력 | `heckel/` · `docs/data/heckel_pure_se_dem.csv` · `docs/data/heckel_reproduction_20260917/RESULT.md` | 같음 · 얇은 침대 (판 높이 7.1–12.0 µm · 400 → 100 MPa) · 쌍 렌즈 union | ① ② ③ ④ ⑥ |
| real_14 복합 다압력 Heckel | `docs/data/heckel_real14_composite_multiP.csv` | 같음 | ① ② |
| E_SE 보정 침대 | `docs/esse_calibration_2mAh_real_9.md` · `docs/data/esse_calibration_2mAh_real_9.csv` | 같음 · 표적 = 세대 1 복합 13.5 % | ① ② ③ ⑥ |
| DEM 공극 코퍼스 · dip · 스케일링 법칙 · 예측기 | `all_dem_porosity.csv` · `docs/porosity_regression_final.md` · `scripts/fit_porosity_v4_global.py` · σ_ionic T1 · σ_e Stage 22.5 · σ_thermal T1 (CLAUDE.md) | 세대 1 코퍼스로 적합 (덱 서명 확인 범위 = `DEMP-01` note 의 리포 덱 23 개 + Heckel 넷 — 코퍼스 전 침대의 덱 원본은 리포 밖 → 서명 미확인 침대는 `unknown`) | ① ② + "세대 1 코퍼스 적합" |
| DEM 덤프를 scaffold 로 쓴 MPM | `docs/data/real14_am_scaffold.csv` · `docs/data/real14_se_scaffold.csv` (real_14 atom_2060000) 등 | scaffold = 세대 1 침대 | "scaffold 출처 = DEM 프로토콜 세대 1" (MPM 쪽 물리 · 값 재계산 아님) |
| 믹서 캠페인 | `dem_scripts/mixer_20260921/` 등 | 압축 프로토콜이 아니다 (회전 드럼) | 표지 대상 아님 · 계수를 바꾸면 그때 따로 |

### 6-2. 역사가 되는 숫자 (세대 1 · 인용 때 표지)

| 숫자 | 자리 | 세대 2 에서 |
|---|---|---|
| 순수 SE Heckel: K 0.007257 /MPa · A 0.3132 · R² 0.9653 · **P_y 137.8 MPa** · **σ_y,eff ≈ 46 MPa** (쌍 렌즈 D_union · 4 점) | `docs/data/heckel_pure_se_dem.csv` 머리 · CLAUDE.md frame [3] | V4 로 새 값 · 옛 값 = "세대 1 · x 축 = 명목 압력 (저항 포함)" |
| real_14 복합 Heckel: K 0.007510 · R² 0.9603 · P_y 133 MPa [116, 156] · σ_y,eff ≈ 44 MPa | `docs/data/heckel_real14_composite_multiP.csv` | 다시 하지 않음 (검증 세트 밖 — Q13) · 표지만 |
| E_SE = 1.35 GPa (복합 2mAh_real_9 ε_sphere 13.47 % · 순수 SE ε_union 10.08 / 11.64 % · ε_sphere −2.34 / 0.23 %) | `docs/esse_calibration_2mAh_real_9.md` | V3 로 E* |
| DEM dip AM 75–85 wt% | CLAUDE.md frame [3] · `docs/porosity_regression_final.md` | V5 |
| "18 배 연화 (24 → 1.35 GPa)" 서술 | CLAUDE.md | 배수는 E* 로 바뀐다 · 24 = 유리 (MV-06) |
| 가지 B 서보 끝 105.842 µm · 10.769 % | 분기 README §12-4 | 모델 내부 진단 (세대 혼합) |

- ⚠ `docs/data/heckel_pure_se_dem.csv` 머리의 앵커 문장 (300 MPa ε_union 10.08 % 를 문헌 냉간압축 값과 같다고 적은 줄) 은 `CL-94` 출처 철회 대상이다 — 이 초안은 고치지 않는다 (기존 파일 무변경) · 표지 작업 때 정정 표지 한 줄 (후속).

### 6-3. 표지 (설계 · 비준 뒤 실행)

- 키: `dem_protocol_gen` = `P1` / `P2` / `unknown` — 기록 · 배포 표 · 웹앱 케이스 (접촉망 `ion_net_generation` 과 다른 칸).  P1 추론 = **덱 서명** (PHASE 3 `viscous 0.5` + 처음 도달 정지 + 판 고정 이완) — 날짜로 추론하지 않는다 · 모르면 `unknown` → 표에서 P1 · P2 섞기 거부 (접촉망 세대 계약 `G2R-02` 꼴) · 섞으려면 명시 opt-in + 한정어.
- 한정어 묶음 (P1):
  ① 정지 = 압축 감쇠 0.5 아래 처음 도달 — 명목 "300 MPa" 에 저항 포함 (어림 몫 N/300,000 · ps73 실측 57.9 %) · 이완 뒤 정적 판 압력은 더 낮다 (ps73 165 MPa)
  ② 저항 몫 ∝ N → 두께 · 입자 수가 다른 침대 사이 비교 = 프로토콜 교란 포함 (같은 침대 안 · 비슷한 N 비교는 대체로 공통)
  ③ ρ_AM 4.8 · ρ_SE 2.0 (1저자 보고 표의 4.85 · 1.64 와 다른 덱 값) · ν_SE 0.30 · E_SE 1.35 (세대 1 복합 표적 · 이 프로토콜에서 보정)
  ④ 중력 98.1 정착 · 9.81 (자기 무게 10⁶ 배)
  ⑤ 판 위 입자 (`DEMP-02`) · 입자 수 가드만 (`MV-08`)
  ⑥ union = 쌍 렌즈 (정확 아님) 인 옛 표
- 퍼뜨리는 자리 (CLAUDE.md "코드 → 웹앱 순차 반영"): 자료 README 머리 한 줄 · 배포 README (v1.3 = "DEM 프로토콜 세대 1 × 접촉망 세대 2") · 웹앱 (케이스 페이지 배지 · 그룹 비교 섞기 경고 · 보고서 머리 · 툴팁) · 원장 노트 · wiki 지도 항목 · CLAUDE.md 현재 상태 표 줄 — 전부 **비준 뒤** (이 초안은 기존 문서를 고치지 않는다 · 값 변경 없음).

### 6-4. 무엇이 남나

- 같은 세대 1 안 · 비슷한 N 의 상대 비교 (한정어 ①–⑥ 과 함께) · 계산 자체 (접촉망 g2 · τ · 협착 · 망 σ) 는 그 침대 위에서 맞다 · 가지 B 의 등록 예측 적중 (B1 같음 · B2 띠 안) 은 모델 내부 결과로 남는다.
- 판정문 Q2: 194 행을 165 MPa 로 바꾸지도 자동 폐기하지도 않는다 · 재실행 범위는 sentinel 짝 비교로 정한다.

## 7. 비용 · 일정 어림

가정: ibb 10 코어 · 160 k 입자 = **18.6 step/s** (가지 B 실측 — 641,200 step / 34,412 s · t0 포함) · 속도 ∝ 1/N · WSL 직렬 8.7 step/s (t0 실측) · 큐 대기 제외 · step 수 = 정착 0.2 M + 안정화 0.1 M + 압축 (스트로크 ÷ 0.01 µm/1,000 step) + 서보 ≤ 1.0 M (가지 B 0.61 M) + 이완 0.1 M + 언로딩 ≈ 0.5–1 M [어림].

| 묶음 | 침대 · 런 | 침대당 step | 침대당 시간 (10 코어) | 합 (10 코어 · 일) |
|---|---|---|---|---|
| 자격 런 | 작은 침대 (≈ 6 × 10⁴ · 15 µm) × ≈ 10 | ≈ 2 M | ≈ 0.5 일 | ≈ 5 |
| E 사다리 | 순수 SE 30 µm (≈ 1.27 × 10⁵) × (5 + 2 + 2) | ≈ 3.5 M | ≈ 1.7 일 | ≈ 16 |
| 다리 팔 (선택) | 세대 1 Heckel 침대 (4.0 × 10⁴) × 4 + 조성 셋 | ≈ 2–3 M | ≈ 0.3–1.5 일 | ≈ 5 |
| 검증 Heckel | 순수 SE 30 µm × 3 압력 × seed 2 | ≈ 3 M | ≈ 1.5 일 | ≈ 9 |
| 조성 사다리 | 6–8 조성 × seed 2 | 설계 의존 | ≈ 1–2 일 | ≈ 12–32 |
| 복합 연속성 | × 2 | ≈ 3 M | ≈ 1.5 일 | ≈ 3 |
| ps45 다섯 (언로딩 포함) | ≈ 1.95 × 10⁵ × 5 | ≈ 4.5–5 M | ≈ 3.4–3.8 일 | ≈ 17–19 |
| **합** | | | | **≈ 67–89** → ibb cpu-60 (10 코어 잡 6 개 동시) 에서 큐가 비면 ≈ 2–3 주 |

- 일정 (의존 사슬 · 어림 · 날짜 아님): 언로딩 수정 → Codex 재확인 (≈ 2–4 일) → 이 계획 비준 · 등록 · 시험 먼저 (≈ 3–5 일) → 자격 런 (≈ 1 주) → Codex → E 사다리 (≈ 1 주 · 6 병렬) → 검증 세트 (≈ 2 주) → Codex ⇒ **≈ 5–7 주** (HOLD 한 번마다 + 수 일).
- 경합: LHS 194 · 보충 20 (10-14 발사 · ibb) · ps45 언로딩 본 실행 (GO 뒤) · 다른 트랙 — 코어 순서 = Q16.

## 8. 1저자 결정

| Q | 무엇 | 선택지 | 권고 |
|---|---|---|---|
| Q1 | 단계 순서 — "plate remove → unloading" | (가) 이 초안: 이완 → 언로딩 (계단 · 분리까지) → 판 제거 · 자유 표면 (나) 글자 그대로 (판 제거 = 서보 해제 · 판 고정 전환 → 언로딩) | **(가)** — 판은 하중을 뺀 뒤에 떨어진다 · 키트 · 실험 순서 (하중 제거 → 꺼냄 → 측정) 와 같다 · (나) 의 "서보 해제" 는 이 초안의 2-5 가 맡는다 |
| Q2 | relaxation 정의 | (R-a) 판 고정 · 정적 재확인 (ΔP_relax ≤ 1 %) · 표적 = 끝 프레임 (R-b) 서보 유지 연장 | **(R-a)** — MV-01 의 독립 확인이 된다 · 세대 1 PHASE 4 와 같은 장치 |
| Q3 | 판 제어 장치 | (가) 덱 수준 서보 (move/mesh 를 덩어리마다 다시 · 판 fix 한 번 · 언로딩 = 키트 변위 계단 그대로) (나) 내장 `mesh/surface/stress/servo` 처음부터 (이완 = `fix_modify … servo/integrate stop` · 언로딩 = `servo/target_val` 힘 계단 — 소스 사본 판독 · 판 확인 전) | **(가)** — D3 (키트 로직이 선행) 과 맞고 이력 보존 장치가 키트에서 이미 쓰인다 · (나) 는 변위 계단 키트를 쓰려면 서보 메시를 지워야 해 (move/mesh 병용 불가 · 분기 README §8) 이력 초기화가 언로딩 출발점에서 다시 생기고, 힘 계단으로 가면 키트 판독 · 관문을 새로 검증해야 한다 (target 0 불가 → 분리 처리도 새로) · (가) 의 단점 (이산 제어 · move/mesh 반복 정의의 바이너리 미확인) 은 T2 · T11 · 키트 Q8 fixture 로 먼저 |
| Q4 | 압축 전역 감쇠 | (가) 저항 몫 기준 (목표 근처 ≤ 2 % · 후보 0.05 · 0.01 · 1e-5 작은 침대 시험) (나) 1e-5 고정 | **(가)** — "낮추면 터짐" 기억 (분기 README §9) 을 시험으로 확인 · 서보가 나머지를 지운다 |
| Q5 | 중력 · 준비 | (가) 준비 g (수치 · 기록) → 안정화부터 9.81e-6 · 2×2 확인 (나) 9.81 유지 | **(가)** — 판정문 §6 · MV-05 순서 (보정 전 고정) · P_meas 1 MPa 언로딩의 자기 무게 지배 문제도 같이 풀린다 |
| Q6 | NCM 진밀도 | (가) 4.8 (나) 4.85 | ✅ **닫힘 — 1저자 10-14 밤 (D10) = 4.85** (PC · SC · 세대 2) · 세대 1 침대 = 4.8 그대로 (역사) · 측정법 [미확인 — 1저자 보고 표] · 정본 카드 값 (4.76 · 4.8 · 4.77 · NMC532 4.85) 은 대조로만 (§3-1) |
| Q7 | 진밀도 1.64 검산 | EIS ① 펠릿 (LPSCl 0.100 g · 10.00 mm) 을 질량 ±0.1 mg · 두께 ±0.01 mm 로 · 3 개 | **예** — 0.776 mm 보다 얇으면 1.64 는 불가능 · 0.01 mm ≈ 1.2 %p (§4-3) · ps45 실험 공극은 세대 2 TD (4.85 · 1.64) 로 다시 적으면 −4.9 – −5.5 %p → 실험–DEM 차 해석 전에 이 결정이 먼저 |
| Q8 | "10–13 % 랩 표준" 의 출처 | 측정 기록 (시료 · 질량 · 두께 · 진밀도 · 하중 상태 · 시료 수) 을 적는다 | **예** — 우리 MPM 10 % (`CL-94`) 계보면 표적 이름을 "모델 표적" 으로 · 독립 대조는 EIS 펠릿 ε_sphere |
| Q9 | 실험 대조 상태 | 랩 펠릿 두께를 재는 상태 — 성형 다이 안 (하중 중 · 놓은 뒤) · 꺼낸 뒤 · EIS 지그 안 (100–150 MPa) | **확인 뒤 상태 맞춤** — 꺼낸 뒤면 2-7 의 ε_sphere,inside 와 · 다이 안이면 2-5 / 2-6 · 지그 안이면 언로딩 사다리의 100–150 MPa 단으로 근사 (실험은 제하 뒤 재적재라 이력이 다르다는 표지) — 순수 SE 회복 1.6–7 % = 공극 +1.4 – +4 %p 라 창 폭 (3 %p) 과 같은 크기 |
| Q10 | 계수 변경 | ν_SE 0.30 → 0.37 · 나머지 그대로 + 민감도 팔 (e 0.5 · μ · μ_r 0 · k̂₂/k₁ (Luding 예시 2) · k_c/k₁ (0 · 1 · 세대 1)) | **권고대로** — ν 만 근거 셋 (DFT 둘 + Bazzoun 2026 입력) · 다른 계수는 LPSCl 측정 출처가 없다 [미확인] · 언로딩 민감 계수는 작은 침대 언로딩 팔로 크기부터 |
| Q11 | 보정 표적 영역 | (가) 안쪽 (벽 2–4 지름 제외) (나) 전체 높이 | **(가)** (둘 다 기록) — 랩 펠릿 ≈ 0.8 mm = SE 지름 800 개 라 벽 띠가 무시된다 |
| Q12 | 다리 팔 | (가) 한다 (Heckel 4 + 조성 3 · E 1.35 · 프로토콜만) (나) 안 한다 | **(가)** — 프로토콜 효과와 E 효과를 가른다 · `DEMP-01` 저항 오프셋 모형의 두 번째 침대 시험 · 비용 ≈ 5 (10 코어 · 일) |
| Q13 | 검증 세트 범위 | 순수 SE Heckel · 조성 dip · 보정 침대 · 복합 연속성 · ps45 다섯 / real_14 복합 Heckel · LHS 194 = 지금 안 함 | **권고대로** — 생산 코퍼스 재실행은 검증 뒤 sentinel 로 (판정문 Q2) |
| Q14 | 표지 키 · 시점 | `dem_protocol_gen` P1/P2 · 비준 직후 문서 · 웹앱 배지 (값 변경 없음) | **예** |
| Q15 | 접촉 법칙 계열 | (가) `hooke/hysteresis` + 보정 E 유지 (나) 항복 캡 법칙으로 | **(가)** — 1저자 방향 (E_SE 재보정) · 캡 법칙 = 세대 3 후보 (§3-1 끝) |
| Q16 | ibb 코어 순서 | LHS 194 · 보충 20 (진행 중) · ps45 언로딩 본 실행 (GO 뒤) · 세대 2 자격 런 | **진행 중인 것 먼저 · 세대 2 자격 런은 빈 코어** — 다른 job 은 끄지 않는다 (1저자 10-08 Q1 (가) 규약) |

> ✅ **1저자 10-14 — Q1 · Q7 · Q8 권고대로**: Q1 = 이완 → 언로딩 (판을 천천히 올려 하중 해제) → 판 분리 · 자유 표면 · Q7 = EIS 용 SE 펠릿 두께로 진밀도 1.64 검사 (0.100 g · 지름 10 mm 펠릿이 0.776 mm 보다 얇으면 1.64 불가) · Q8 = "10–13 % 랩 표준" 의 측정 기록 (시료 · 질량 · 두께 · 진밀도 · 하중 상태 · 시료 수) 을 적는다 · 1저자 *"이 참에 reference 되는 논문을 확실하게 찾으면 안되나? SE pellet porosity 관련해서"* → 표 A 보강 문헌 탐색 (후보 · 정본 카드 필요 목록) 진행 중.
> ✅ **1저자 10-14 — Q10 (가) ν_SE = 0.37** (*"(가)로하자"* — 근거: Deng 2016 Table III DFT 0.37 · Torii 2025 DFT 0.37 · Bazzoun 2026 입력 0.37 · Bazzoun 2025 0.33 (0.29–0.37) · Pustorino 2025 DFT 0.23–0.34 · 우리 DFT (E_VRH 22.06 · B₀ 26.23) = 0.360 은 notes 병기 · E* 차 0.7 %) · 그 밖의 Q2–Q6 · Q9 · Q11–Q16 = 대기.

## 9. Codex 검토 요청 개요 (비준 뒤 · 발송 = 1저자)

- 핀: 이 초안의 비준판 커밋 · 범위 = **설계 검토 (런 없음)**.
- 묶음: 이 문서 · 원장 `DEMP-01` · `02` · `MV-01`–`09` · 판정문 10-08 · 분기 README · `docs/data/ps73_damping_branch_20261007/in.branch_B.liggghts` · 생성기 · 언로딩 등록 §12–§13 · 키트 README · 키트 재검토 판정 · 수정 계획 · 배경 · ps45 덱 · Heckel 생성기 · Heckel CSV · E_SE 보정 문서 · §10 정본 카드 목록.
- 물을 것:
  1. 단계 정의 · 끝 조건이 MV-01 해제 증거로 충분한가 (판정문 §3 예산 그대로 · 관측 창 정의)
  2. 덱 수준 서보 (move/mesh 반복) 가 MV-02 를 닫는가 · 이산 제어의 위험 (진동 · 과도) · 내장 서보와의 비교
  3. D9 공극 결정 + 상태 맞춤 (Q9) + 영역 (Q11) 이 MV-03 을 닫는가 · 진밀도 불확실성 (§4-3) 처리
  4. 중력 · 준비 순서 (MV-05) · 2×2 설계 충분성
  5. E 사다리 estimand (fresh · 짝 seed) · 보간 규칙 · 보정 ↔ 검증 분리
  6. 계수 표의 출처 대조 (규율 ⑥ — 카드 쪽 · 표) · 언로딩 민감 계수 (k̂₂/k₁ · k_c/k₁ · μ_r) 처리
  7. 결과 전 기대 X1–X7 의 반증 줄에 판별력이 있는가 (특히 X2 다리 팔)
  8. 표지 설계 (P1/P2 · 섞기 거부) · 세대 1 자료 목록 누락
  9. 언로딩 키트 → 세대 2 접합 (T12) 의 빈 곳
- 반례 탐침 제안: MV-01 합성 궤적 (KE 0.5 J · 0.009 J) 을 새 판정기 설계에 · MV-02 이력 연속 (move/mesh 반복 ↔ fix 재생성) · MV-08 보존 회계 (AM 1 · 50 개 손실) · 세 구 union.
- 하지 않는 것: 런 · 덱 실행 · 스케줄러 · 원장 수정.

## 10. 근거 목록 (정본 카드 · 이 계획에서 받치는 것)

| 정본 카드 (`litdb-canon:`) | 카드가 적은 자리 | 받치는 것 |
|---|---|---|
| `luding2008_cohesive_frictional_contact_models` | §2.3.1 (r 0.4–0.8) · §2.3.2 eq 6–8 · §2.6 eq 22 · Table 1·2 예시 | 우리 법선 법칙의 정의 · 예시 k₁/k̂₂ 0.5 · k_c/k̂₂ 0.5 · φ_f 0.05 · 배경 감쇠 (카드 요약: 과댐핑 주의) |
| `coetzee2017_dem_calibration_review` | §2 p.106 · §5.5 p.131 · p.106 (Benvenuti) · §1 p.105 | 보정 ≠ 검증 · 구속 압축 = 강성에만 민감 · 구름 마찰 = 측정 불가 경험 매개변수 · 출처 열 (measured / calibrated / assumed) |
| `paulick2015_elastic_particle_properties_dem_review` | §4 p.75 · §5 p.75 | 1 % 겹침 규칙 → 우리 연화 = 보정 프록시 |
| `thakur2014_eepa_adhesive_elastoplastic_dem` | §4 (I < 10⁻⁴ · density scaling · 재하 · 제하 · 몰드 제거 3 단계) | 준정적 기준 · 제하 절차 선례 · μ_r 0.001 |
| `demirtas2021_mpfem_hollow_sphere_die_compaction` | §4-5 | KE/PE < 1 % (RD ≥ 0.6) · mass scaling 의 재하율 교란 |
| `shi2019_high_am_loading_particle_size_assb` | p.2 · SI Table 1 | 정압 유지 → KE 0 · ρ 1.87 / 4.85 (LPS 유리 · NMC532) |
| `bazzoun2025_dem_parameter_sensitivity_assb_cathode` | §3 표 (Table 2 · 3) · §4 · Fig 14 · eq 2–3 | PID 서보 + KE 0 유지 · μ 0.4 (최강 민감) · COR 0.4 (최저) · ν_SE 0.33 · ρ 1.64 / 4.77 · 실험 공극 연산자 · ω 0.7 · 실현 3 개 |
| `bazzoun2026_dem_fem_rnm_ionic` | 재료 파라미터 줄 | PID 일정 압력 · μ · COR 0.4 · ν_SE 0.37 · ρ 1.64 / 4.77 · E_SE 22.1 |
| `so2021_dem_mold_pressure_assb_coldpress` | Table 1 · §4 | PI 상단벽 → release · springback · μ 0.5 · e 0.5 |
| `so2022_dem_compaction_coated_particles_assb` | §2.4 · 표 | PID 상단벽 · μ 0.5 · e 0.5 |
| `so2022_dem_contact_model_assb_compaction_sintering` | Table 1 · Fig 2 · Fig 7a | release 곡선 · 램프 후 release · 경도 문턱 (세대 3 후보) |
| `lee2025_heckel_argyrodite_powder_densification_nanoindentation` | SI p.3 · Table 1 · Table 2 · Fig 1c · 1d · 카드 §3-4 | in-die Heckel 관행 · TD 1.64 인쇄 (의심) · K → P_y · 300 MPa ≈15 % · 회복 ≈4.7 % · 나노압입 E 27.6 |
| `miss2026_insitu_conductivity_porosity_pressure_compaction` | p.32833 Eq 2 · Table S1 · S2 | in situ 공극 연산자 (피스톤 · 입자 탄성 보정) · ρ₀ 1.87 · 다이 안 7.1–7.6 % · 놓은 뒤 8.6 % · 회복 1.62 % |
| `faka2026_particle_size_consolidation_strain_lpscl` | §4.2 p.10 · Fig S2 · SI Table S5 | in-die / out-of-die 정의 · PSD 별 300 MPa 공극 · DEM ρ 1.87 · Y 18.5 · 벽 Y 70 |
| `heck2026_densification_sulfide_se_binder_scalable` | p.13 · Fig 10 · Fig 12 | in-die / out-of-die 절차 · in-die 감압 회복 ≈ 고체 탄성 · springback 범위 |
| `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` | p.6 · p.3 · SI Table S1 | 감압 격자 가역 · 선폭 비가역 · 문헌 TD 1.77–1.88 |
| `doux2020_stack_pressure_assb` | Table S2 | 다이 밖 LPSCl 펠릿 상대밀도 82.1 % (TD 1.860) · 측정 밀도 1.522 |
| `sakuda2013_sulfide_mechanical_property` | 본문 · Fig 2a | 24 GPa 계보 = 유리 · ρ_glass 1.88 (MV-06) |
| `deng2016_elastic_superionic_electrolytes_dft` | Table III | ν 0.37 · E 22.1 |
| `torii2025_lpscl_mechanical_anisotropy_dft` | p.17883 · 표 | E 27.4 · ν 0.37 |
| `pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament` | 표 | ν 0.23–0.34 |
| `song2025_porous_argyrodite_modulus_fracture_toughness` | §3.1 | 13 % 다공 펠릿 E 4.7 ± 1.1 GPa (다른 양 · 제하 강성 대조 후보) |
| `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` | p.4 | NMC811 E 138 ± 24 GPa → E_AM 140 |
| `lee2026_lpscl_coating_thickness_ncm811` | SI Fig. S4 | ρ 4.8 / 1.64 인쇄 |
| `bielefeld2020_effective_ionic_conductivity_binder` | §3.3 | NCM811 4.76 (C-rate 추정 사용값) |
| `minnmann2021_jes_charge_transport_bottlenecks` | 재료 표 | LPSCl 1.87 (`CL-94` 판정 근거 카드이기도) |
| `ketter2025_resistor_network_models_predict_transport_properties` | 소프트 밀링 절 | LPSCl 1.86 · NCM83 4.78 |
| `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` · `cho2024_conflicting_roles_conductive_additive` · `kraft2017_lattice_polarizability_argyrodite_Li6PS5X` | 카드 주석 | 밀도 값이 **원문 값이 아님** (§3-3 정정) |
| `otani2025_dem_se_dispersion_aggregation_compression` | 표 · §10-③ | COR 0.25 · μ 0.5 · μ_r 0.01 · 조대화 주장의 한계 |
| `frankenberg2024_dem_high_intensity_mixer_assb` | Table 3 | COR 0.3 · μ_s 0.44 · μ_r 0.2 (DAOR 보정) · 힘 f² 조대화 |
| `lee2024_multiphysics_dem_fem_initial_pressure_assb` | 표 | μ 0.1–0.3 (모델 입력) |
| `ngandjong2021_dem_calendering_digital_twin` | §4-B | 속도 사다리 선례 (한계 포함) |
| `zhang2026_xct_dem_cathode_calendering_peel_calibration` | §3.5 · p.4–5 | 하중 중 ↔ 제하 뒤 공극 · 실험 대조 = 제하 뒤 |
| `shenouda2020_dem_metal_powder_am_liggghts_tutorial` | 도메인 · 안정성 진단 | `fix check/timestep/gran` 사용 예 |
| `pycompact2025_dem_mpfem_workflow` | 요약 | DEM 정착 = 충전 생성기 선례 (방법만) |
| `mcgeary1961_bimodal_sphere_packing` | 요약 | 임계 크기비 ≥ 약 7 (dip 의 기하 기반) |
| `martinbouvard2003_dem_composite_cold_compaction` | 요약 | 경질 + 연질 복합 냉간 압밀 DEM |
| `schneider2023_particle_size_pressure_transport` | 표 | in-die Heckel P_y (t-Li₇SiPS₈) — 관행 맥락 |
| `thorntonning1998_adhesive_elastoplastic_contact` · `zunker2024_mdr_contact_model_partI` · `zunker2025_dem_large_deformation_compaction` · `giannis2021_stress_based_multicontact_dem` · `varkey2026_multicontact_elastoplastic_dem` | 요약 | 캡 · 다접촉 법칙 = 세대 3 후보 (이 계획 밖) |

- 리포 밖 근거 (카드 아님): 1저자 2 년차 연구 보고 슬라이드 "2-1 / DEM 해석 조건" 표 (세션 전달 10-14 밤 · D10 — 밀도 4.85 · 1.64 · 지름 9 · 4 · 1 µm · 영률 140 · 22 GPa = 재료 참고값 · 밀도 측정법 리포 미기록 [미확인]).
- 리포 근거 (카드 아님): 판정문 10-08 (MV-01–09 · §3 · §4 · §6 · §8) · 분기 README (§1 · §2 · §4 · §8 · §9 · §12) · 언로딩 등록 §3–§13 · 키트 README · 배경 (§3–§10) · `docs/esse_calibration_2mAh_real_9.md` · `docs/data/heckel_pure_se_dem.csv` · `docs/data/heckel_real14_composite_multiP.csv` · `dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts` · `scripts/make_heckel_inputs.py` · 판정문 증거 재현 `docs/reviews/codex_model_validation_review_evidence_20261008/_README_reproduction.md`.

## 11. 찾을 문헌 (정본 카드에 없음 — 검색어만 · 인용 아님)

| 무엇 | 검색어 |
|---|---|
| LPSCl 입자 마찰계수 측정 | "Li6PS5Cl friction coefficient" · "sulfide solid electrolyte powder shear cell" · "argyrodite powder flowability angle of repose" |
| 미분 · 점착 분말의 구름 마찰 보정 | "rolling friction calibration fine cohesive powder DEM" · "rolling resistance model assessment Ai 2011" |
| 순수 아지로다이트 펠릿의 다이 밖 두께 · 회복 (300 MPa 근처) | "argyrodite pellet springback ejection" · "Li6PS5Cl pellet relative density out-of-die" |
| LPSCl 진밀도 측정 (He 비중병) · 1.64 의 계산 근거 | "Li6PS5Cl helium pycnometry" · "argyrodite true density pycnometer" · "Li6PS5Cl density 1.64 g cm-3" |
| Heckel 원전 · in-die / out-of-die 관행 | "Heckel 1961 density pressure relationships powder compaction" · "Sun Grant 2001 in-die out-of-die Heckel" (heck2026 참고문헌 [58]) |
| DEM 전역 감쇠가 준정적 압축 끝점에 주는 영향 | "DEM global viscous damping quasi-static compaction error" · "Cundall local non-viscous damping uniaxial compression" |
| 서보 벽 · 정적 평형 판정 (DEM 다이 압축) | "servo-controlled wall DEM uniaxial compaction static equilibrium criterion" · "LIGGGHTS mesh/surface/stress/servo" |
| 점착 이력 모델 계수 (k_c · φ_f · k̂₂/k₁) 의 미분 · 황화물 값 | "Luding adhesive elasto-plastic contact parameters fine powder calibration" · "hysteretic linear spring plasticity depth calibration" |
| 연질 분말 제하 강성 · 탄성 회복의 DEM 검증 | "DEM unloading elastic recovery cold compaction validation" · "elastic springback discrete element powder compact" |
| 경질 + 연질 혼합 다압력 공극 실험 (조성 축) | "hard soft powder mixture compaction porosity composition experiment" |
