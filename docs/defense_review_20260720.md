# Defense-grade 초정밀 리뷰 — 2026-07-20 (오늘 작업 전체)

5-에이전트 적대검증(코드·물리·숫자·정직·**COMSOL-대체**) + 즉시 수정 기록.
대상 커밋 `ca4e75c..HEAD` (branch `claude/stoic-knuth-NObVQ`).  ⚠ 검증 후 CONFIRMED 결함은
당일 전부 수정·커밋됨(§3).  이 문서 = 방어 요지 정본.

---

## ★ 1. 핵심 질문 — 전기화학 시스템(STEP4-v2)이 COMSOL을 대체하나?

**답: 범위별 YES/NO. curve-fit이 아니라 legitimate 물리 시스템이다.**

### 실제로 푸는 것 (marketing 아님 — 코드 정독 + selftest 19/19 통과)
STEP4-v2 (`scripts/step4_dyn.py`) = **복셀-해상 SSB-특화 DFN**:
- 전하보존 2망(φ_e·φ_i) FV `∇·(σ∇φ)=0`, 조화평균 face 전도(`:374`), Dirichlet 집전체/분리막(`:385-402`).
- **완전 비선형 Butler-Volmer** (선형화 아님) `I=i0·A·[exp(α_a fη)−exp(−α_c fη)]`(`:299-304`), i0(x), 필름 ASR per-face Newton.
- **입자별 구형 고체확산** (~1271개 각자 자기 구, Crank-Nicolson, Thomas; `:184-242`) — COMSOL size-bin보다 세밀.
- 갈바노/CV/CCCV, 충·방전, 직렬 R_int; 매스텝 KCL + 기계정밀 에너지밸런스 감사.
STEP3 (`network_conductivity.py`) = 정당한 Kirchhoff 전도 solver (그래프 Laplacian + Holm/Mikic 수축) = COMSOL 전도 모듈과 같은 PDE, 볼륨메시 대신 접촉그래프.

### ✅ 대체 가능
1. **σ 삼중(이온/전자/열) — 실제 DEM/MPM 침대.** ★ **Bazzoun 2026 독립 입증**: 같은 재료·코드·접촉물리를 실측 EIS + COMSOL FEM에 검증(RNM≈FEM≈실험, 32-98× 빠름). 우리는 같은 급 + e/열 삼중.
2. **미세구조-해상 전류/SOC/핫스팟 필드** — COMSOL은 이미지 메시 필요, 우리는 DEM/MPM에서 바로. **최대 우위.**
3. **반쪽셀 V(t) (단일이온 sulfide)** — 빠진 항(전해질 NP·이중층)은 t⁺≈1 SE에서 물리적으로 없는 것, 근사 아님.
- 수치 신뢰 selftest 19/19: 질량보존 2.7e-12, Cottrell 2.9%, 직렬-R 1.2e-4, KCL 7e-9, 에너지밸런스 4e-13, STEP3 회귀 2.2e-5.

### ❌ 대체 불가 (COMSOL 필요)
액체/혼성 전해질(NP 없음) · 고-CAM 절대 σ(수축-only, FEM 대비 ~2× 과소, bracket) · 커플드 멀티피직스(등온·stress→반응 A10 미완) · 음극/풀셀 · 수렴 보장·재료 라이브러리·적응메시 · 고율 과도(미검증).

### 심사자 3대 질문
- **Q1 "외부 solver/실험과 정량 일치 하나"**: STEP3=YES(Bazzoun). **STEP4=NO 완료된 외부 패리티 없음** (PyBaMM 트윈 인프라만 있고 ΔV-RMS 숫자 없음). ← **최우선 갭.**
- **Q2 "수축-only 절대 σ"**: "트렌드 검증·절대 bracket"로 생존 (고-CAM ~2× 편향 정직 인정).
- **Q3 "1e-4 KCL 노이즈플로어 + deep_weak 휴리스틱"**: **최약점** — FEM식 수렴보장 없음; 안전망(KCL+에너지 감사)이 gross 에러는 잡음.

### "COMSOL-패리티" 정직성
**방정식/기능 패리티 = 진짜 + 내부 검증됨. 수치 검증으로 읽으면 과장.** → backlog/CLAUDE의 한 줄 "COMSOL-패리티" 라벨을 **"방정식-수준 패리티, 내부 검증; 수치 패리티 대기"**로 명시 권고(미수정, §4).

### Bullet-proof 최소작업
1. **★ PyBaMM 패리티 1회** (`step4_pybamm_anchor.py`, 균일 침대 → ΔV-RMS mV). **<10-20mV면 Q1의 STEP4 갭 닫힘 = V100 하루.**
2. Bazzoun 실측 EIS를 STEP3 절대 검증점 채택. 3. 고율(≥2-3C) 확산-knee 1개. 4. production 스케일 수렴곡선(vox·tol 스윕).

---

## 2. 강점 (defense에서 리드할 것)
- **★ hot-side가 σ비율 따라 뒤집힘** (base=집전체/전자제한 ↔ SBE/DBE=분리막/이온제한) — Dirichlet-pin 인공물이면 방향 안 뒤집힘 = **가장 견고한 물리 주장.**
- **mech↔reaction 정직 레이어** (`c06e78a`): raw +0.95 옆에 z-통제 +0.46/within-slice +0.61, strain=co-location 라벨 — 어디서도 과장 안 함(그림·CSV·모달 일관).
- **kim2025 앵커 충실** — 453/290/382·22/18/17·T-sweep 전부 litdb 카드와 일치, 유일한 pdf_verified; 나머지 전부 confirmed_snippet 태그.
- **σ_apparent MIX flag = 강점** (fresh 벌크+aged R_int 시간축 혼합을 자기 규명; 헤드라인은 R_int 무관).
- **over-transfer 7+3 캐비엇**, **g(N) assumed-form 라벨**, **"clamp=조작" 자기비판** — 정직성이 defense 자산.

---

## 3. CONFIRMED 결함 → 오늘 전부 수정 (커밋)
| # | 결함 | 심각 | 발견 | 수정 커밋 |
|---|---|---|---|---|
| 1 | **R_geom 가드 NameError** — 축퇴 코너서 크래시 → STEP3+STEP4 전체(σ_ion·pore-τ·jrxn) 무음 드롭 | HIGH | 코드+정직 (독립 2인) | `589cbf2` (_sw/_sb 클램프를 가드 위로) |
| 2 | **σ_SDCP=250 전파 누락 12곳** — 영문 paper draft가 abstract와 모순(10%/+45% vs +52%), EMT 11.6×↔+52.0% 자기모순, BV 503,922 | MED | 숫자 | `a6603d9` (10→7.3·+45→+52·150→250·11.6×→13.3×·503,922→503,915) |
| 3 | **Holm 지수 −1을 "Holm"으로** — Holm 수축=−0.5(우리 σ_ionic cov^½), −1은 전하전달 = 자기모순 | HIGH(물리) | 물리 | `9a09612` (옴성 −0.5 + 전하전달 −1 분리) |
| 4 | **R_tort에 pore/void τ** — 코드 '수송 폼 대입 금지' 가드 위반 | MED-HIGH | 물리 | `9a09612` (SE-상 이온 τ로) |
| 5 | **anchor-db seed-list 593.8** — §2b서 폐기한 오귀속 숫자를 §5서 여전히 seed 지시 | MED | 정직 | `9a09612` (strike + kim2025로 교체) |
| 6 | **code hardening** — mech-reaction fig 누수(에러경로)·CSV compute 2회 bins 불일치·bins 미검증(0→ZeroDiv) | LOW-MED | 코드 | `4fdb58c` (try/finally·1회 compute·_mech_bins) |
| 7 | **§F1 측정→계산** — σ_e/R_geom/BV(모델 OUTPUT)를 "측정한/실측/잰"이라 표기 | LOW(정직) | 정직 | `4497...` (모델이 산출한/계산값; 진짜 랩측정 72.5µm은 보존) |

---

## 4. 남은 항목 (미수정 — 우선순위·근거)
1. **★ STEP4 외부 패리티 런 (Q1)** — 최우선. PyBaMM 인프라 있음, V100 하루. defensible→bullet-proof의 유일한 조각.
2. **CLAUDE.md/backlog "COMSOL-패리티" 라벨** → "방정식 패리티, 수치 대기"로 상세화 (한 줄이 검증된 것처럼 읽힘).
3. **coverage↔reaction "CAUSAL"** — 반-tautology(jrxn=BV 면적 총합). within-slice +0.61이 진짜 근거. **intensive(면적당 i/ī) vs coverage로 재검**하면 비자명 확정. (현 모듈은 "OBSERVATIONAL/co-location" 라벨은 정직하나 "genuine/causal" 표현 톤 조정 여지.)
4. **72.5µm 두께 "실측" TO-VERIFY** — 진짜 caliper/SEM 값인지 확인(모델 출력 relabel이면 순환). 배영진 전극이라 실측 가능성 높음.
5. **저-우선 코드**: porosity CSV regime-gate 경계 반올림(CSV는 gap 반올림 후 임계, 리스트뷰는 raw — [4.0,4.05) 경계 불일치, cosmetic); mech-reaction 모달 Esc·중복 스택(UX).
6. **절대 σ CAM-rich** — field-spreading 교차검증 or bracket 명시 (Q2).

---

## 5. 한 줄 결론
오늘 작업은 **전기화학 시스템이 σ-삼중 전송(Bazzoun 입증) + 미세구조-해상 전류/SOC 필드에서 COMSOL을 진짜
대체**함을 방어 가능하게 정리했고, 적대검증이 찾은 **CONFIRMED 결함 7종을 당일 전부 수정**했다.
"defensible"과 "bullet-proof" 사이의 **단 하나의 빠진 조각 = STEP4 매치드-조건 패리티 런 1회**(이미 있는
인프라, V100 하루).  액체전해질·커플드 열/역학·풀셀·보장수렴 고율은 COMSOL 영역으로 정직히 남긴다.
