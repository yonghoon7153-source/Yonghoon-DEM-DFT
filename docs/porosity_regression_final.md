# 전극 공극률(Porosity) 회귀식 — 문헌 기반 다차원 모델

> ## ✅ CLOSED (stage2 종료, 2026-06-30) — n_collection=153
> 데이터 수집 종료, 식 확정.  **production form = regime-gated(plastic 포함) target**:
> | target | LOOCV | R² | RMSE | n |
> |---|---|---|---|---|
> | **gated best (plastic 포함, 생산형)** | **0.583** | 0.637 | 2.32 %p | 129 |
> | rigid ε_sphere (DEM native) | 0.769 | 0.830 | 2.45 %p | 129 |
>
> rigid가 더 높은 건 ε_sphere가 *매끄러운* 양이라 그렇고(단 SE-rich 과압축 artifact를
> fit), **물리적으로 옳은 건 gated(plastic) 0.583**.  잔차 ±2.3%p의 **절반(~1.5)은 환원
> 불가 seed 노이즈** → 식은 정보 한계.  **R²를 더 못 올리는 이유 = 데이터 다양성(thin↔thick,
> SE-poor↔rich, 전 P:S)이지 form 결함 아님.**
>
> **★ 코너는 *포함*** (mono-large·thin-SE-poor, gap>4 → gate가 DEM 사용).  out-of-envelope
> 지만 porosity 범위를 넓혀 R²에 *기여*한다 — 빼면 R²가 *오히려* 떨어짐(in-envelope-only
> 0.52 < 코너포함 0.58).  사용자 지시(2026-06-30): "코너도 추가".
>
> **Outlier 제외 = 물성(영률 등)-다른 것만 (`scripts/porosity_close.py`):**
> - **영률(E_SE)-다른**: E-변종 particulate_9_E05(0.68)/E15(2.02 GPa) — 표준 1.35와 다른
>   재료강성 → 제외(E-축은 별도, +2.3%p/E배).
> - **그 외 물성/레짐-다른**: sub-µm SE(particulate_1 r0.25, Cronau 비정질) · particulate
>   (mono-AM_S r3 separator) · S-series(r_AM_S=4) — `load_pairs(exclude_particulate)` +
>   tracking CSV로 분리(frame[5] 별 레짐).
> - **broken-sim**(물성 아닌 *무효 데이터*): `1mAh_100_*` (CLAUDE.md plate_z 메타버그 →
>   음수/이상 porosity) — 필터 영구.
>
> 별도 발견(닫음): regime-gate · thin SE-poor 코너 경계(SE≲15% **且** thin, 두께-탈출) ·
> SE-size U(조성-의존, particulate) · E_SE 단조(+2.3%p/E배) · λ-scaling(r_AM_S=4 미완,
> r_SE=1.33 1점 필요) — `docs/porosity_subum_se_investigation.md`.
> 후속(통합/E축)은 `scripts/porosity_unified.py` + post-porosity 로드맵.



전고체 양극(LPSCl 고체전해질 + 단결정 NCM)의 **공극률을 설계 변수에서 예측**하는
관계식. **SE 소성 변형을 포함한** DEM(강체 패킹)·MPM(소성 void-fill) 결합 모델.

---

## 1. 타깃 정의 — regime-gate된 "best" 공극률

각 케이스의 참 공극률을 두 모델 출력에서 선택한다. DEM은 강체 구 + 탄성 overlap의
ε_sphere를, MPM은 진짜 소성 void-fill의 공극률을 준다.

```
gap = ε_DEM(ε_sphere) − ε_MPM(plastic)

gap > +4 %p  →  ε_DEM    (mono-large 코너: 연속체 MPM이 과압축 → 강체가 loose-truth)
그 외        →  ε_MPM    (정상 + SE-rich: 소성 void-fill = 물리값;
                          동시에 DEM ε_sphere의 overlap 과압축을 보정)
```

n=129 중 **123 = MPM(plastic), 6 = DEM(코너)**. 즉 기본은 소성값, MPM이 무너지는
큰-AM 단일 코너만 강체값.

**근거(frame[5] 분업)**: DEM = 강체 접촉망·패킹·Furnas dip 담당, MPM = 소성 형상
변화·void-fill 담당. 두 모델은 **각각 실험(Minnmann pure-SE 10% @300MPa)에 독립
보정**되며 서로 fit하지 않는다(frame[4]). |gap| ≤ 4는 두 독립 모델의 교차검증
인증서로 해석한다.

---

## 2. 회귀식

```
ε[%] = β0
     + β1·B    + β2·B_sym         (McGeary/Furnas 비모달 dip)
     + β3·S_λ  + β4·φ_se          (Bazzoun SE 채움 + 조성)
     + β5·r_AM + β6·r_SE          (절대 크기)
     + β7·(S_λ·a) + β8·(F_se·B)   (다차원 결합)
```

현 corpus(n=129, **CLOSED**) fit 계수:

| 항 | 계수 | 항 | 계수 |
|---|---|---|---|
| β0 (const) | +34.90 | β4 (φ_se) | −25.15 |
| β1 (B) | −58.88 | β5 (r_AM) | +2.81 |
| β2 (B_sym) | +14.72 | β6 (r_SE) | −3.41 |
| β3 (S_λ) | −36.66 | β7 (S_λ·a) | +19.94 |
| | | β8 (F_se·B) | +70.50 |

**계수 대입 — 복사용 최종식** (단위 %p, 변수 정의는 §3):

```
ε[%] = 34.90
     − 58.88·B   + 14.72·B_sym      (① McGeary/Furnas 비모달 dip)
     − 36.66·S_λ − 25.15·φ_se       (② Bazzoun SE 채움 + 조성)
     +  2.81·r_AM −  3.41·r_SE       (③ 절대 크기, µm)
     + 19.94·(S_λ·a) + 70.50·(F_se·B)   (④ 다차원 결합)
```

**성능**: R² = 0.637, **LOOCV R² = 0.583**, RMSE = 2.32 %p, n=129, k=9 (n/k=14.3).
full−LOOCV gap = 0.054 → 과적합 아님.  (rigid ε_sphere native target은 LOOCV 0.769
— 더 매끄럽지만 SE-rich overlap 과압축 artifact를 fit; 물리적으로 옳은 생산형은 gated 0.583.)

---

## 3. 변수·항 정의

모든 입력은 **설계값**에서 계산한다. DEM 출력 부피분율 φ_am, φ_se는
φ_am+φ_se = 1−ε로 타깃을 직접 누설하므로 **feature로 사용하지 않는다**.

### 3.1 기본 변수
- `P` — AM_P(큰 AM) 분율. (0:10→0, 3:7→0.3, …, 10:0→1.0)
- `a` = AM_wt / 100 — 무게 기준 활물질 비율.
- `φ_se` (se_of_solid) — SE의 **고체 부피분율** (공극률과 독립):

  φ_se = [(100−AM_wt)/ρ_SE] / [AM_wt/ρ_AM + (100−AM_wt)/ρ_SE],  ρ_AM=4.8, ρ_SE=2.0 g/cm³

  (예: AM_wt=82 → φ_se=0.345 = sim 보고치 ~0.32–0.33과 정합)
- `r_AM` (rAM_eff) — 조성가중 AM 반지름. 비모달: P·r_AMP+(1−P)·r_AMS; 단일: 해당 반지름.
- `λ_AM` = r_AMP/r_AMS (비모달 크기비), `λ_SE` = r_AM/r_SE.
- `sat(λ)` = min(λ/7, 1) — **McGeary 7:1 임계비** 게이트. 작은 입자가 큰 입자 void에
  들어가려면 크기비 ≥ 7(= 0.154·d_c) 필요; 미만이면 부분 채움.

### 3.2 항별 의미 + 문헌

**(①) McGeary/Furnas 비모달 dip — β1·B + β2·B_sym**
- B = max(1 − ((P−0.64)/0.64)², 0) · sat(λ_AM)
  - 포물선 peak가 P_OPT = 0.64 (= RCP 골격 고체분율 0.64). 큰 AM 골격(void≈0.36)을
    작은 AM이 채울 때 최밀이 되는 조성. sat(λ_AM)로 크기비 게이팅.
- B_sym = 4P(1−P) — 대칭 혼합량(보조항).
- 문헌: McGeary 1961(이성분 구 패킹 0.625→0.86, 임계비 7:1), de Larrard CPM.
- 효과: P↑일수록 dip 심화, 10:0에서 작은 AM 소멸 → 반등.
- 검증: ablation에서 둘 다 필수(제거 시 LOOCV −0.15 / −0.13).

**(②) Bazzoun SE 채움 + 조성 — β3·S_λ + β4·φ_se**
- S_λ = sat(λ_SE) — SE 크기비 채움 효율.
- φ_se — SE 고체분율(조성). SE↑ → AM 틈 채움 → ε↓.
- 문헌: Bazzoun 2025(작은 SE → CAM void 채움 → ε↓, 크기비 λ=D_CAM/D_SE).
- crossover: S_λ와 결합항이 φ_se에 따라 SE-크기 효과의 부호를 반전(SE-rich엔 큰 SE
  조밀 / AM-rich엔 작은 SE가 더 잘 채움 — 프로젝트 size-effect 관측과 일치).
- 검증: φ_se 필수(−0.064).

**(③) 절대 크기 — β5·r_AM + β6·r_SE**
- r_AM — 큰 AM일수록 골격·wall-scale↑ → ε↑. **ablation에서 최강 항(제거 −0.46)**:
  크기 scale 자체가 사라짐.
- r_SE — SE 반지름 원시값. 큰 SE = 적고 큰 SE 입자 → 성긴 패킹. λ_SE의 sat()
  **포화(λ_SE>7→1)가 못 잡는** 직접 효과. *r_SE=1.5µm 케이스가 corpus에 늘며
  드러남, 추가 시 LOOCV +0.084.* 음(−) 계수는 결합항과의 상쇄이지 단독 물리 부호
  아님(아래 collinearity).
- 검증: 둘 다 필수.

**(④) 다차원 결합 — β7·(S_λ·a) + β8·(F_se·B)**  ※ F_se = φ_se·sat(λ_SE)
- S_λ·a = sat(λ_SE)·(AM_wt/100) — **SE 채움 효율 × AM 골격량**. Bazzoun 채움은 채울
  AM 골격이 있어야 의미 → 크기비와 조성의 결합.
- F_se·B = [φ_se·sat(λ_SE)]·B — **SE 채움 × 비모달 void**. SE가 McGeary/de Larrard
  비모달 패킹이 만든 void에 들어앉음(2-class 결합). (F_se 단독항은 r_SE 추가 후
  중복이라 제거; 결합항만 유지.)
- 검증: S_λ·a 제거 −0.012; F_se·B 유지가 우세. 두 결합이 단독항보다 LOOCV 기여 큼.

---

## 4. 성분 분해

조건별 각 그룹의 기여(= β·feature, 합하면 ε). AM_wt=82, r=6/2/0.5 (n=129 CLOSED 계수):

| P:S | const | dip(①) | SE(②) | size(③) | 결합(④) | **= ε%** |
|---|---|---|---|---|---|---|
| 0:10 | +34.9 | +0.0 | −29.6 | +3.9 | +9.3 | **18.5** |
| 3:7 | +34.9 | −5.7 | −42.2 | +7.3 | +21.8 | **16.1** |
| 5:5 | +34.9 | −9.3 | −45.3 | +9.5 | +26.3 | **16.1** |
| 7:3 | +34.9 | −12.6 | −45.3 | +11.8 | +26.7 | **15.4** |
| 9:1 | +34.9 | −15.8 | −45.3 | +14.0 | +25.1 | **12.9** |
| 10:0 | +34.9 | −5.7 | −45.3 | +15.2 | +18.7 | **17.7** |

> **Collinearity 주의**: 개별 항·그룹 값이 최종 ε보다 크고 서로 상쇄한다(②≈−45,
> ④≈+26). feature 상관으로 **개별 계수는 단독 식별되지 않고 선형결합만 식별된다**
> (Ridge가 LOOCV를 크게 깎는 것으로 확인). 따라서 **검증된 것은 합(예측값)**이며,
> 분해는 한 가지 유효한 대수적 분할이다. 개별 계수의 부호·크기를 단독 물리로
> 해석하지 말 것.

---

## 5. 불확실성 — regime 오차밴드

regime 혼합은 필터링이 아니라 **잔차 오차로 표현**한다.

| regime | n | bias | ±밴드(LOOCV RMSE) |
|---|---|---|---|
| 정상 (MPM/plastic) | 111 | −0.2 | **±2.4 %p** |
| SE-rich (MPM) | 12 | +0.4 | ±1.1 %p |
| mono-large 코너 (DEM) | 6 | +3.1 | ±4.9 %p |

seed-noise floor ≈ ±1.5 %p (동일 설계의 seed 간 흩어짐) → 잔차의 절반은 DEM 확률적
패킹에서 오며 **어떤 모델로도 환원 불가**. 즉 form은 정보 한계 부근이다. 활용 시:
조성 순위·설계 중심값엔 충분; downstream(σ_ionic/ASR) 입력 시 **±밴드째 전파**.

---

## 6. 적용 한계

정확도 위계:
1. **실험** (Minnmann 10% @300MPa) — 유일 절대 anchor.
2. **개별 시뮬** (gated DEM/MPM) — 특정 조건 ground truth (±1.5 seed + 모델 gap).
3. **본 회귀식** — 미시뮬 조건용 ±2.5 %p 보간 사상.

- 본 식은 ③. 특정 점의 "궁극값"이 아니라 설계 공간을 매끄럽게 이은 추정.
- **데이터 anchor된 P:S는 5개(0:10·3:7·5:5·7:3·10:0)**뿐; 1:9·2:8·4:6·6:4·8:2·9:1은
  보간.
- ⚠ **8:2·9:1이 7:3보다 낮게 예측되는 것은 form이 dip을 과하게 연장한 artifact**다.
  실제로는 작은 AM이 과소해지면 void 미충전으로 재성김(McGeary 반등). **데이터로
  확인된 dip 바닥은 7:3 근처**; 8:2·9:1 확정엔 직접 시뮬 필요.

---

## 7. 검증 요약 (이 식이 최종인 근거)

- **Ablation**: 9항 중 8항 필수(제거 시 LOOCV −0.01~−0.46). 단독 se_fill만 잉여 →
  제거(r_SE 추가 후 중복; 상호작용 F_se·B는 유지).
- **Addition 스크리닝**: r_SE 추가 +0.084(채택). 그 외 후보(se_solid², B×φ_se, P, P²,
  φ_se×a, 1/λ_SE, B²)는 ΔLOOCV ≤ 0 또는 노이즈 → 기각.
- **타깃 비교**: gated 0.583 vs pure-MPM 0.399 vs pure-DEM(rigid ε_sphere) 0.769.
  pure-DEM이 수치상 높으나 **소성 미포함 + ε_sphere 과압축 artifact 잔존** → 물리적으로
  부적합. gated가 옳은 타깃(소성 포함 요구 충족).
- **과적합/정칙화**: full−LOOCV gap 0.054(작음). Ridge는 LOOCV 악화(강한 collinearity)
  → OLS 유지, 단 계수는 합으로만 해석.
- **코너 포함이 R²를 올린다**: in-envelope-only(n≈95) LOOCV 0.52 < 코너 포함(n=129) 0.58.
  코너(mono-large·thin-SE-poor)는 porosity 범위를 넓혀 *기여* → 제외 안 함.

**결론**: r_SE 추가 + se_fill 제거 + broken-sim(1mAh_100) 제거로 corpus 정리, gated
LOOCV 0.583. 추가/삭제할 항 없음 → 현 corpus의 **최종식(CLOSED)**.

---

*기준 조건: 압력 300 MPa, AM 12µm·4µm(반지름 6·2) / SE 1µm(반지름 0.5), ρ_AM=4.8 /
ρ_SE=2.0 g/cm³, n=129 (CLOSED, 2026-06-30).*
