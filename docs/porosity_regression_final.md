# 전극 Porosity 관계식 (최종) — 문헌 기반 다차원 회귀

**SE plastic deformation을 포함한** 단일 생산용 porosity 관계식.
DEM(강체 packing) + MPM(소성 void-fill)을 regime-gate로 결합.

- 코드: `scripts/porosity_physics_regression.py` (항 정의 `features()`),
  `scripts/porosity_final_production.py` (fit + grid),
  `scripts/porosity_decompose.py` (성분 분해),
  `scripts/porosity_final_verify.py` (adversarial 검증).
- 데이터: `docs/data/case_3d_collection.csv` (DEM+MPM paired, n=110),
  예측표 `docs/data/porosity_production_final.csv`,
  성분분해 `docs/data/porosity_decomposition.csv`.

---

## 1. 타깃 — regime-gate된 "best" porosity (plastic 포함)

각 케이스의 **참 porosity**를 두 모델에서 고름:

```
gap = ε_DEM(ε_sphere) − ε_MPM(plastic)
gap > +4 %p  → ε_DEM   (mono-large 코너: MPM 연속체가 과압축 → 강체가 loose-truth)
그 외        → ε_MPM   (정상+SE-rich: 진짜 소성 void-fill = 물리값,
                        동시에 DEM ε_sphere의 overlap 과압축을 구제)
```

n=110 중 **104 = MPM(plastic)**, **6 = DEM(코너)**.
→ 기본은 plastic 값, MPM이 무너지는 mono-large 코너만 DEM.

근거(frame[5] 분업): DEM = 강체 접촉망/packing/Furnas-dip, MPM = 소성 형상변화/
void-fill. 둘은 **각각 실험(Minnmann pure-SE 10% @300MPa)에 독립 보정**, 서로
fit 안 함(frame[4]). |gap|≤4 = 교차검증 인증서.

---

## 2. 최종식

```
ε[%] = 31.92                              (const)
     − 51.06 · B          + 13.51 · B_sym      (McGeary/Furnas 비모달 dip)
     − 47.88 · S_λ        − 18.39 · φ_se        (Bazzoun SE size-ratio + 조성)
     +  3.06 · r_AM       −  3.71 · r_SE        (절대 크기)
     + 33.79 · (S_λ·a)    + 38.12 · (F_se·B)    (다차원 결합)
```

**성능 (n=110):** R²=0.696, **LOOCV R²=0.646**, RMSE 2.52 %p.
overfit 아님 (full−LOOCV gap = 0.05). k=9, n/k=12:1.

---

## 3. 각 항 설명 (정의 + 물리 + 문헌)

모든 입력은 **설계값**에서 계산 — DEM 출력 φ_am/φ_se(=1−porosity)는 **누수라서
절대 사용 안 함**.

### 공통 정의
- `P` = AM_P(큰 AM) 분율. 0:10→0, 3:7→0.3, …, 10:0→1.0.
- `a` = AM_wt / 100 (무게 기준 AM 비율).
- `φ_se` = se_of_solid = SE의 고체부피분율
  = `[(100−AM_wt)/ρ_SE] / [AM_wt/ρ_AM + (100−AM_wt)/ρ_SE]`,
  **ρ_AM=4.8, ρ_SE=2.0 g/cm³** (프로젝트 convention; sim의 "SE 비율(of solid)
  ~32-33% @AM82"와 일치 — AM82→34.5%).  *porosity 무관*.
- `r_AM` = rAM_eff = bimodal: `P·r_AMP+(1−P)·r_AMS`, mono: 해당 반지름.
- `λ_AM` = r_AMP/r_AMS (비모달 크기비), `λ_SE` = r_AM/r_SE.
- `sat(λ)` = `min(λ/7, 1)` — **McGeary 7:1 임계비** (작은 입자가 큰 입자 void에
  들어가려면 ≤1/7, 0.154·d_c). 7 이상이면 채움효율 포화.

### (a) McGeary/Furnas 비모달 dip — `−51.06·B + 13.51·B_sym`
- **`B`** = `max(1 − ((P−0.64)/0.64)², 0) · sat(λ_AM)`
  - 포물선 peak가 **P_OPT=0.64**(= RCP 골격 고체분율). 큰 AM 골격(void~0.36)을
    작은 AM이 채울 때 가장 조밀해지는 조성.
  - `sat(λ_AM)`로 게이팅: 크기비가 7:1 못 미치면 부분 채움.
- **`B_sym`** = `4·P·(1−P)` — 대칭 혼합량(보조항).
- **문헌**: McGeary 1961(이성분 구 packing 62.5→86%, 임계비 7:1),
  de Larrard CPM(Furnas dip).
- **효과**: P 커질수록 dip 깊어짐 → 10:0에서 작은 AM 사라져 **반등**
  (분해표: 9:1 −13.4 → 10:0 −5.0).
- **검증**: ablation에서 둘 다 NEEDED (빼면 −0.15 / −0.13).

### (b) Bazzoun SE 채움 + 조성 — `−47.88·S_λ − 18.39·φ_se`
- **`S_λ`** = `sat(λ_SE)` — SE 크기비 채움효율.
- **`φ_se`** = SE 고체분율(조성). SE 많을수록 AM 틈을 더 채움 → ε↓.
- **문헌**: Bazzoun 2025(작은 SE → CAM void 채움 → ε↓, λ=D_CAM/D_SE).
- **crossover**: `{S_λ, …}` 짝이 φ_se에 따라 SE-크기 효과 부호를 뒤집음
  (SE-rich엔 큰 SE 조밀 / AM-rich엔 작은 SE가 더 잘 채움 — 프로젝트 size-effect
  note).
- **검증**: φ_se NEEDED (−0.064). S_λ 단독은 약하지만 결합항과 함께 유지.

### (c) 절대 크기 — `+3.06·r_AM − 3.71·r_SE`
- **`r_AM`** = rAM_eff. 큰 AM일수록 골격 크고 wall-scale 큼 → ε↑.
  ablation에서 **가장 강함** (빼면 −0.46! 크기 scale 자체가 사라짐).
- **`r_SE`** = SE 반지름(원시값). 큰 SE = 적고 큰 SE 입자 → 성긴 pack → ε에 직접
  영향. λ_SE의 **포화(sat)가 못 잡는** 부분.
  - ★ **이 항이 이번 adversarial 재검증에서 추가됨 (+0.084 LOOCV)**. r_SE=1.5
    케이스(real_6/7, a-sweep)가 corpus에 늘며 직접 효과가 드러남. 음(−) 계수는
    "이 corpus에서 큰 SE가 더 조밀"이 아니라 결합항과의 상쇄(아래 collinearity 주의).
- **검증**: r_AM, r_SE 둘 다 NEEDED.

### (d) 다차원 결합 (파라미터끼리 연결) — `+33.79·(S_λ·a) + 38.12·(F_se·B)`
사용자 요청 "문헌 보고 파라미터끼리 어떻게 연결되는지":
- **`S_λ·a`** = `sat(λ_SE)·(AM_wt/100)` — **SE 채움효율 × AM 골격량**. Bazzoun
  채움은 채울 AM 골격이 있어야 의미 → 크기비와 조성의 결합.
- **`F_se·B`** = `[φ_se·sat(λ_SE)]·B` — **SE 채움 × 비모달 void**. SE가 McGeary/
  de Larrard 비모달 packing이 만든 void에 들어앉음 (2-class 결합).
- **검증**: 둘 다 유지 (S_λ·a 빼면 −0.012; F_se·B marginal이나 유지가 나음).
  forward screen에서 이 결합들이 단독항보다 LOOCV 기여 큼.

---

## 4. 성분 분해 (값은 더하면 porosity, @AM82·r=6/2/0.5)

| P:S | const | McGeary dip | Bazzoun SE | size | couplings | **= ε%** |
|---|---|---|---|---|---|---|
| 0:10 | +31.9 | +0.0 | −33.7 | +4.3 | +15.8 | **18.3** |
| 3:7 | +31.9 | −4.4 | −50.1 | +7.9 | +29.0 | **14.4** |
| 5:5 | +31.9 | −7.3 | −54.2 | +10.4 | +33.1 | **13.8** |
| 7:3 | +31.9 | −10.3 | −54.2 | +12.8 | +33.3 | **13.5** |
| 9:1 | +31.9 | −13.4 | −54.2 | +15.3 | +32.4 | **12.0** |
| 10:0 | +31.9 | −5.0 | −54.2 | +16.5 | +29.0 | **18.2** |

전체 77행: `docs/data/porosity_decomposition.csv`.

> ⚠ **Collinearity 주의**: 개별 항/그룹 값이 최종 porosity보다 훨씬 큼(Bazzoun SE
> −54, couplings +33 등이 상쇄). feature들이 상관돼서 **개별 계수는 단독으로
> 정해지지 않고 조합만 정해짐**(Ridge가 LOOCV를 크게 깎는 것으로 확인). →
> **신뢰할 건 SUM(LOOCV 검증)**, 분해는 한 가지 유효한 대수적 분할일 뿐. 개별
> 계수의 부호/크기를 물리로 과해석 금지. 조건에 따른 **합의 변화**를 보라.

---

## 5. 불확실성 = regime 오차밴드 (필터링 아님, 오차로 표현)

| regime | n | bias | ±밴드 |
|---|---|---|---|
| 정상 (MPM/plastic) | 92 | −0.2 | **±2.5 %p** |
| SE-rich (MPM) | 12 | +0.6 | ±1.8 %p |
| mono-large 코너 (DEM) | 6 | +3.0 | ±5.7 %p |

- seed-noise floor ≈ **±1.5 %p** (같은 설계 seed 흩어짐) → 잔차의 절반은 DEM
  확률적 packing, **어떤 모델도 못 줄임**. form은 거의 정보 한계.

---

## 6. 한계 — "궁극의 값" 아님 (정직)

진실 위계 3층:
1. **실험**(Minnmann 10% @300MPa) = 유일 절대 anchor.
2. **per-case 시뮬**(gated DEM/MPM) = 특정 조건 ground truth (±1.5 seed + 모델 gap).
3. **회귀식**(이 문서) = 안 돌린 조건용 **±2.5 매끄러운 지도**.

- **데이터 anchor된 P:S는 5개만** (0:10/3:7/5:5/7:3/10:0). **1:9·2:8·4:6·6:4·8:2·9:1은
  보간**.
- ⚠ **8:2·9:1이 7:3보다 낮게 나오는 건 McGeary 반등(작은 AM 부족→재성김)을 데이터가
  못 잡은 것** → 하한/불확실. 실측 dip 바닥은 **7:3 근처**. 확정하려면 그 두 P:S를
  직접 시뮬.
- downstream(σ_ionic/ASR)으로 먹일 땐 **±밴드째로 전파**.

---

## 7. Adversarial 검증 로그 (이 식이 최종인 근거)

`scripts/porosity_final_verify.py`:
- **(A) ablation**: 9항 중 8항 NEEDED(빼면 −0.01~−0.46), se_fill 단독은 DEAD →
  **제거**(rSE 추가 후 중복; 상호작용 F_se·B는 유지).
- **(B) addition**: rSE +0.084 → **추가**. 그 외 후보(se_solid², bim×se, P, P²,
  ses×amwt, 1/λ_SE, bim²) 전부 ΔLOOCV ≤ 0 또는 노이즈 → 기각.
- **(C) target**: gated 0.646 vs pure-MPM 0.443 vs pure-DEM 0.798. pure-DEM이
  수치상 높지만 **plastic 미포함 + ε_sphere 과압축 artifact** → 기각. gated가
  물리적으로 옳은 타깃(사용자 요구 = plastic 포함).
- **(D) overfit**: gap 0.05(작음). Ridge는 LOOCV 깎음(collinear) → OLS 유지.

**결론**: rSE 추가 + se_fill 제거 후 **LOOCV 0.550→0.646**. 더 뺄/더할 항 없음 →
이 9항이 현 corpus의 최종식.

---

*최종 갱신: 밀도 ρ_AM=4.8/ρ_SE=2.0, rSE 항 추가, se_fill 제거, n=110.*
