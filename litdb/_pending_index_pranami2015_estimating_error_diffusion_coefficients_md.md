# 인입 대기 — `pranami2015_estimating_error_diffusion_coefficients_md`
> ⚠ **2026-09-13 확인: 이 파일의 ① 은 INDEX 행이 아니라 `comparison_vs_ours.md` 방법 원전 표다 — INDEX.md 에 넣을 행이 없다.** 큐레이터가 INDEX 행을 따로 써야 한다. 미병합.

> 생성 2026-09-09 · litdb-curator. **동시 실행 충돌 회피**로 `INDEX.md` · `comparison_vs_ours.md` 를 직접
> 건드리지 않았다. 아래 두 조각을 사람(또는 다음 큐레이터)이 옮겨 붙인다.
> digest 본문: `litdb/papers/pranami2015_estimating_error_diffusion_coefficients_md.md`
> 그림: `litdb/figures/pranami2015_estimating_error_diffusion_coefficients_md/` (16장)

---

## ① `INDEX.md` 에 추가할 행

```
| pranami2015_estimating_error_diffusion_coefficients_md | Estimating Error in Diffusion Coefficients Derived from Molecular Dynamics Simulations | Pranami & Lamm | J. Chem. Theory Comput. 11, 4586–4592 (2015) | 10.1021/acs.jctc.5b00574 | methods (통계·MD 방법론 원전) | ✅ | 시드/독립궤적(MIS) · δ≥τ 다중 시간원점 · MSD 회귀 오차 무효 · 유한크기 D vs 1/L. ⛔ 물성값 없음 — 4축 표 제외, 🔧 방법 원전 |
```

- 🎤 talk 역링크: **해당 없음** — `litdb/talks/lee2026_skku_mlip_materials_design.md` §99-10 인입 대기열(6건)에
  이 논문은 **없다** (`grep` 확인). 다른 talk 에도 매칭 없음.

---

## ② `comparison_vs_ours.md` 에 추가할 블록

⛔ **물성 4축(A 이온전도 / B 산화안정 / C 기계 / D 전자구조) 표에 넣지 않는다** — 이 논문에는 σ·Ea·ESW·gap 이
하나도 없다 (계가 Lennard-Jones 유체다). 값 없는 행을 4축 표에 넣으면 표가 무의미해진다.
**`🔧 방법 원전` 블록에만** 넣는다.

```markdown
### 🔧 방법 원전 — 시드 · 독립궤적 · MSD 오차 추정

**`pranami2015_estimating_error_diffusion_coefficients_md`** (JCTC 2015) — LJ 유체 + 프랙탈 응집체, 물성값 없음.

| 이 논문이 요구하는 것 | 우리 현행 | 판정 |
|---|---|---|
| δ 를 R_SD(τ,δ) 로 측정, **δ ≥ τ** (겹치지 않는 시간원점) | δ = 저장간격 **0.1 ps** 고정, τ ≤ 50 ps → **겹침 500배** | ❌ 미준수 |
| MSD~τ 회귀가 뱉는 D 오차는 **무효** (정규성 W=0.87 p<1e-4 · 등분산 위반) | 오차막대를 **시드**에서 낸다 (600 K 3-시드) | ✅ 준수 |
| 오차는 **MIS(다중 독립 시뮬레이션)** 의 D 표본에서 t-CI | 시드 3 | ⚠ 목적별 (아래) |
| D 표본의 **정규성 검정** 후 t-CI | 한 적 없음 (3점으론 불가) | ❌ 불가 |
| 등분산 깨지면 **WLS** | MSD 창 2–50 ps **등가중 OLS** | ❌ 미준수 |
| 유한크기 **D vs 1/L** 외삽 | 셀 크기 **1개** → 보정 불가 | ❌ 불가 |

**시드 산포 비교** (CV = σ/μ):
| 계 | CV | 출처 |
|---|---|---|
| LJ 유체 N=1000 (100 시드) | **0.11 %** | 논문 SI §2 (소환값) |
| LJ 유체 N=125 (100 시드) | **0.20 %** | 논문 SI §2 (소환값) |
| 프랙탈 응집체 1개 (10 시드) | **2.7–4.1 %** | Table 3 역산 *(digest 계산)* |
| **우리 MLIP-MD (Li in argyrodite)** | **≈ 22 %** | 3-seed×3-T 재시드 *(digest 계산)* |

**🔴 우리 시드 3개 판정** *(digest 계산 — 이 논문의 Step 5 식 + 우리 실측 CV 22.1 %)*:
- 단일 D 의 3시드 95 % CI 반폭 = **±63 %** (LPSCl1.6 600 K 실측)
- 비(ratio)의 3시드 95 % CI = **×[0.61, 1.65]** (폭 2.7배)
- ⇒ **R ≥ 2 (자릿수·2배급) 주장 → 3시드로 충분**
- ⇒ **R ≈ 1.33 급 주장 → 계당 6–8 시드 필요**
- ⇒ **"동등하다" 주장 → 수십 개 필요** ⇒ 반드시 **"구별되지 않는다(not distinguished)"** 로 표현
- ⇒ 철회된 **단일시드 1.33× 는 0.91 σ** (= 순수 시드 잡음). 2026-07-09 철회가 **사전에 계산 가능했다.**
- ⛔ 이 논문은 **비(ratio)의 오차를 다루지 않는다** — 위 비 계산은 우리가 붙인 로그공간 전파다.
- ⛔ 유한크기 보정식은 **hydrodynamic** 기원이라 고체 전해질 Li 홉핑에 **이식 금지**.
```

---

## ③ (선택) `kb/` 후속 제안 — 이 digest 가 만든 실행 항목

옮기는 사람이 판단해서 `kb/open_items.md` ⏭ 절이나 큐에 넣을 것. **여기서는 kb 를 건드리지 않았다.**

1. **R_SD(τ,δ) 를 우리 저장 궤적으로 한 번 그린다** — 새 MD 불필요. 우리 MTO 의 실효 표본 수가 확정된다.
2. **`n_origins` 로 오차막대를 만들지 않는다** 를 규약 문장으로 명시 (지금 코드엔 그 경로가 없지만 명시도 없다).
3. **`tools/modelc_v3/disorder_ensemble_diffusion.py:110` docstring 의 "(weakly correlated) origins" 표현 정정** —
   Pranami Fig. 2 는 δ = τ/4 에서 R_SD ≈ 0.85 (강한 상관)를 보인다.
4. **보고량 카드(`kb/templates/estimand_card.md`)에 "주장하려는 최소 효과 크기 R" 칸 추가** →
   `M = f(CV, R)` 을 결과 보기 전에 계산 (정지 규칙 선언과 맞물림).
5. **MSD 창 2–50 ps 에 WLS 를 한 번 시험** — 등가중 OLS 대비 D 이동량을 재고 근거를 남긴다.
