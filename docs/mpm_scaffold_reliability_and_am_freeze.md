# MPM scaffold — AM-freeze 근거 + porosity 신뢰성 regime map (절대값 · 트랜드)

**계기 (2026-06-26):** input_1mAh_100_15 (P:S 10:0, AM:SE 87:13, SE-poor) scaffold MPM이
porosity **0.00%** = 완전 비물리(DEM 32.84%)를 냈다.  SE가 바닥으로 흘러내리고 frozen AM만
위에 노출.  → "AM 고정인데 다른 MPM porosity는 믿을 수 있나? 근본이 흔들린다" + "porosity를
임의로 lock하면 그 수치 신뢰성 있나?" + "절대값도 트랜드도 중요하다" 라는 정당한 의문.
이 문서가 controlling 답변.  데이터: `docs/data/mpm_dem_porosity_reliability.csv` (104 cases).

---

## §0 TL;DR

1. **AM을 freeze하는 건 shortcut이 아니라 4가지 근거가 있는 의도된 설계**(§1).  AM에 물리를 주면
   (연속체라 rigid 접촉망 표현 불가 + over-shielding 반대 비물리 + CFL/OOM blow-up + 검증 골격 drift).
2. **scaffold MPM porosity는 104 중 80개(76%)에서 DEM과 cross-validated** (|gap| ≤ 4 %p) = **신뢰**.
   real_14 실험검증(MPM 16.7 ↔ DEM 15.6 ↔ exp, 512 수렴)이 이 중간 regime을 anchor.
3. **양 끝에서 각 모델이 *반대 방향*으로 실패** — 이게 근본을 흔드는 게 아니라 **frame[4]/[5]를
   더 깨끗하게 만든다**:
   - **SE-poor + mono-large-AM + thin(1–2mAh)** → **MPM 과압축**(frozen AM이 하중 못 받음) → **DEM 신뢰**.
   - **SE-rich (SE/solid ≳ 50%)** → **DEM ε_sphere 과압축**(overlap convention artifact) → **MPM 신뢰**.
   - **중간(production bimodal)** → 둘이 일치 → **상호 cross-validation**.
4. **트랜드도 regime-aware로 보면 robust**(§5): porosity-vs-조성 트랜드는 중간에서 견고; SE-poor/
   mono-large 끝은 **DEM 트랜드**(Furnas rebound), SE-rich 끝은 **MPM**.  ⚠ raw-MPM을 전 구간에 쓰면
   트랜드가 틀린다(특히 mono-large 끝의 Furnas rebound를 과압축이 지워버림).
5. **porosity를 임의 lock/clamp하면 신뢰성 0 (조작).**  정답은 clamp가 아니라 **regime-gate**(그 regime의
   옳은 모델을 쓰는 것 = frame[5]).  그리고 **DEM↔MPM 일치(|gap|≤4)가 곧 validity 증명서**다.

---

## §1 왜 AM을 freeze하나 (= AM에 물리를 주면 안 되는 이유, 4가지)

scaffold 방식: DEM dump의 **실측 300 MPa 압축 AM 좌표**를 grid obstacle로 **고정**(am_mask가 v=0 pin,
AM material point 없음); SE만 MPM 재료로 두고 소성 압축.  AM을 움직이게(=물리를 주면) 안 되는 이유:

**① frame[5] — 근본: AM load-bearing은 *rigid 접촉망* 현상 = DEM 영역**
강체 AM이 하중을 받는 것은 **점접촉(Hertzian, force concentration)으로 이뤄진 rigid 접촉 네트워크**
현상이다.  이건 Kirchhoff/Holm 접촉망을 가진 **DEM이 정확히 푸는 것**.  MPM은 **연속체**(material point +
배경 grid)라 도달 가능한 해상도(접촉폭 ≪ cell)에서 **rigid 점접촉을 제대로 표현 못 한다**.  따라서 AM
역학은 DEM에 맡기고(scaffold로 결과를 물려받음), MPM은 **SE 소성흐름만** 계산 — 분업의 핵심.

**② 실제로 mobile-rigid AM을 넣으면 *반대로* 비물리 — over-shielding 36–41% 문제**
AM을 mobile-rigid로 MPM 연속체에 넣으면, 큰 강체 AM들이 **force chain을 형성해 하중을 독점 → SE를
shield** → SE가 안 눌려서 **porosity가 36–41%에 갇힌다**(실제 ~16%, +20%p 과다공).  즉 SE-poor의
0%(과압축)와 **정반대 방향**의 비물리.  frozen AM + plastic SE로 둬야 SE가 하중을 강제로 받아 16%까지
densify (real_14 검증).  ⇒ **AM에 물리 부여 = SE-poor 0%를 고치는 게 아니라 더 흔한 over-shielding 에러로
바꿔치기.** (CLAUDE.md "mobile rigid-AM re-introduces over-shielding".  단 그 force-chain의 일부는 SE BULK
연화 부작용이었고 --nu-se 0.49로 완화됨 — 그래도 AM-mobile 자체는 아래 ③④ 때문에 기각.)

**③ 계산상 blow-up — CFL/OOM**
AM을 material point로 넣으면: 140 GPa(stiff)라 CFL 조건 `dt ∝ 1/√(E/ρ)`이 **극소 timestep**을 요구 +
큰 2차입자라 point 수 폭증(OOM) → **n_grid ≥ 384에서 MPM blow-up**(CLAUDE.md "AM-as-material preset blew
up at n_grid≥384").  반면 frozen mask는 v=0 한 줄이라 OOM/CFL 부담 0 + 기하 정확.

**④ 중복 + drift — DEM AM이 이미 검증된 정답**
dump의 AM 좌표는 **이미 실측 300 MPa 평형 골격**(Furnas dip 등 DEM이 #266 실험과 1:1 검증).  AM을
움직이게 하면 그 **검증된 skeleton에서 벗어나고(drift)**, DEM이 잘하는 걸 MPM에서 **더 나쁘게 재시뮬**하는
꼴.  scaffold의 목적은 **DEM의 검증된 AM packing을 그대로 물려받는 것**.

---

## §2 두 모델의 *반대편* 실패 regime (의외로 깨끗한 cross-validation)

각 모델의 porosity가 **반대 끝에서 반대 방향으로** 무너진다.  이건 frame[4](독립 보정 후 비교)/[5](분업)을
약화시키는 게 아니라 **강화**한다 — 중간에서 둘이 만나 cross-validate하고, 끝에서는 무너지는 모델을
*다른* 모델이 받쳐준다.

### §2.1 SE-poor + mono-large-AM + thin → MPM 과압축 (frozen AM이 하중을 못 받음)
- 메커니즘: 평판이 300 MPa(target)를 찾아 내려오는데, **frozen AM은 v=0이라 wallP 반력에 기여 0**
  (반력은 움직이는 SE point만 평판에 부딪혀 만듦).  SE가 적고(SE/solid ≲ 28%) sparse-large-AM이면 평판이
  **얼어붙은 AM을 지나쳐** 무른 SE를 으깬다 → SE가 저항 대신 바닥으로 흘러내려 pooling, AM은 위에 노출,
  porosity가 0%까지 붕괴.  실제로는 강체 AM 골격이 300 MPa를 받지만(1mAh_100_15 DEM: 119 AM-AM 접촉,
  F/P_c 10.8, **48% 파괴** = AM이 하중 독점) **frozen scaffold는 그 load-bearing을 전달 못 함**.
- ⚠ **깨끗한 SE/solid threshold는 없다** — 진짜 판별자는 **"frozen AM이 평판을 막을 만큼 두껍고 촘촘하냐"**:
  - 8mAh_real_15 (10:0, SE/sol **16%**): gap **−0.1** ✓ (두꺼운 8mAh, AM 다층 → 평판 막힘 → 정상)
  - 2mAh_real_20 (10:0, SE/sol **16%**): gap **+19.6** ✗ (얇은 2mAh, sparse AM → 평판 통과 → 과압축)
  - **같은 SE/sol 16%인데 8mAh는 OK, 2mAh는 과압축** → 두께(AM-obstruction 완전성)가 핵심.
  - ⇒ 실패 조건 = **mono-large-AM(10:0) AND thin(1–2mAh)**.  8mAh mono-large는 SE-poor라도 정상.
- ★ **두 단계로 나뉜다 (input_1mAh_100_10 vs _15가 결정적):**
  - **(a) COLLAPSE (1mAh_100_15):** 평판이 300 MPa에 *도달 못 하고* SE를 0%까지 으깸 → **MPM 완전 무효 → DEM.**
  - **(b) BRACKET (1mAh_100_10, 등):** 평판이 300 MPa에 *도달은 함*(wallP 0.32 @frame45, servo 정상)
    그런데도 **MPM 15.9% vs DEM 28.3% (gap +12.4)**.  여기선 MPM이 "고장"이 아니라 **bracket의 아래끝**:
    DEM 28%(rigid 골격, mono-large가 헐겁게 packing, SE가 큰 void를 다 못 채움 = UPPER) ↔ MPM 16%(소성 SE가
    그 void로 흘러들어가 채움, 단 frozen-AM 과소부담으로 다소 over-fill = LOWER).  **진실은 그 사이(~20–24%),
    실험 anchor 없음**(real_14는 bimodal) → frame[4] "divergence = 정량화된 모델한계".
  - 판별 보강: gap이 큰 건 **DEM porosity가 비정상적으로 높을 때(⚠ insufficient-compaction 28–33%)** 거나
    **MPM이 SE-poor로 과압축할 때** — 둘 다 thin-mono-large corner.  **8mAh mono-large는 DEM이 정상
    compaction(16–19%)이라 둘이 일치**(real_15 gap −0.1, real_10 gap 0.0).  즉 "reliability가 확 떨어지는" 건
    *thin mono-large corner 한정*이지 전역 붕괴가 아님.
- ⚠ **protocol("servo 전에 더 작업")로는 bracket이 안 닫힌다:** _10은 servo가 *정상 작동*(target 도달).
  16 vs 28 gap은 protocol 버그가 아니라 **constitutive 분기**(rigid packing DEM vs plastic-SE+frozen-AM MPM).
  porosity-floor guard는 (a) COLLAPSE만 막고 (b) BRACKET은 모델차라 안 닫힘.

### §2.2 SE-rich → DEM ε_sphere 과압축 (overlap convention artifact)
- 메커니즘: DEM porosity는 `ε_sphere = 1 − ΣV_sphere/V_box`.  SE-rich(SE/solid ≳ 50%)로 dense하면 SE 구들이
  깊게 overlap → ΣV_sphere가 V_box를 넘어 **ε_sphere가 0/음수로 과소** (CLAUDE.md "dense SE-only gives
  NEGATIVE/near-zero ε_sphere").  반면 **MPM은 부피보존 소성**이라 over-densify 안 함 → 더 물리적.
  - a5 sweep (SE/sol **68%**): DEM 1–2% (artifact) vs MPM 11–13% (물리) → gap −9 ~ −11, **MPM 신뢰**.
  - a6 (59%): DEM ~5% vs MPM ~14% → gap ~−9.5.   a7 (48%): DEM ~9% vs MPM ~15% → gap ~−6 (mild).
- 이 끝에서는 **DEM ε_union/Stage-E area min-cap이 보정**(CLAUDE.md)하지만, **절대 porosity는 MPM이 정답**.

### §2.3 중간 (production bimodal, SE/solid ~30–50%) → 둘이 일치 → 상호 검증
- real_14 (φ_SE 0.27): MPM 16.7 ↔ DEM 15.6 ↔ **실험, 512 수렴** = anchor.  생산 케이스(AM 70–85 wt%)는
  대부분 여기 → MPM·DEM 둘 다 신뢰 (gap |≤4|, 평균적으로 MPM이 DEM보다 ~1–3 %p 높음 = real_14의
  수렴된 1.2 %p 모델차 패턴).

---

## §3 데이터 — 104 케이스 분류 (`mpm_dem_porosity_reliability.csv`)

판별: **|gap| = |DEM − MPM| ≤ 4 %p → cross-validated(둘 다 신뢰)**.  gap > 4 또는 < −4면 regime으로
어느 모델이 무너졌는지 진단.

| trust | n | 조건 | 의미 |
|---|---|---|---|
| **both (cross-validated)** | **80 (76%)** | \|gap\| ≤ 4 | DEM↔MPM 일치 → 둘 다 신뢰 ★ |
| **MPM** (DEM ε-과압축) | 12 | gap < −4, SE/solid ≥ 55% | SE-rich → DEM overlap artifact → MPM 신뢰 |
| **bracket** (mono-large 분기) | 6 | gap > 4, mono-large + thin, MPM>3 | [MPM 아래끝 / DEM 위끝], anchor 없음 |
| **review** (lean MPM) | 6 | −6.7 ~ −5, SE/solid ~48% (a7) | 중간 SE-rich, DEM 약한 ε-과압축 → MPM 쪽 |
| **DEM** (MPM COLLAPSE) | 1 | gap≫0, MPM<3 (crushed to ~0) | MPM 완전 무효 → DEM (1mAh_100_15) |

**FLAGGED — mono-large(10:0) 분기, 전부 thin(1–2mAh):**
| case | P:S | SE/sol | DEM | MPM | gap | 판정 |
|---|---|---|---|---|---|---|
| input_1mAh_100_15 | 10:0 | 25% | 32.8 | **0.0** | +32.8 | COLLAPSE → DEM |
| input_2mAh_real_20 | 10:0 | 16% | 29.3 | 9.7 | +19.6 | bracket |
| input_2mAh_a9_p10 | 10:0 | 19% | 26.4 | 10.9 | +15.5 | bracket |
| input_1mAh_100_10 | 10:0 | 32% | 28.3 | 15.9 | +12.4 | bracket (servo OK, target 도달) |
| input_2mAh_a9_50_p10 | 10:0 | 19% | 18.4 | 9.3 | +9.1 | bracket |
| input_1mAh_8_AMP_S5 | 10:0 | 28% | 21.9 | 15.0 | +6.8 | bracket |
| input_1mAh_8_AMP_S2 | 10:0 | 28% | 23.6 | 17.3 | +6.3 | bracket |

★ **대조 (같은 SE/sol인데 두께가 가른다):** SE/sol 25%서 8mAh_real_10 gap **0.0(both)** vs 1mAh_100_15
**+32.8(collapse)**; SE/sol 32%서 8mAh_real_5/2mAh_real_10 gap **~0(both)** vs 1mAh_100_10 **+12.4(bracket)**.
→ 8mAh(두꺼움, AM 다층 → 평판 막힘 + DEM 정상 compaction)는 일치, thin(1–2mAh, DEM-loose ⚠)만 분기.

**FLAGGED — DEM ε-과압축(→MPM 사용), SE-rich:** a5 (SE/sol 68%, gap −9.3~−10.8), a6 (59%, gap −7~−9.6)
= 12 cases.  **review(lean MPM):** a7 (48%, gap −5.2~−6.7) = 6 cases.

⇒ **다른 MPM값들은 문제없다 (질문 직답):** mono-large(10:0) 7개 + SE-rich(a5/a6/a7) 18개를 빼면
**나머지 80개(76%)는 DEM과 cross-validated = 신뢰.**  실패는 **무작위가 아니라 식별 가능한 두 corner**에
국한 — 근본은 흔들리지 않는다.

---

## §4 신뢰성 판정 — 절대값

**규칙 (gap-sign 진단):**
- **|gap| ≤ 4 %p** → DEM↔MPM **cross-validated → 둘 다 신뢰** (DEM↔MPM 일치 = validity 증명서).
- **gap > 4 (DEM ≫ MPM), mono-large + thin:**
  - MPM < 3% (300 MPa 도달 실패, crushed) → **COLLAPSE → MPM 무효 → DEM 사용.**
  - MPM ≥ 3% (target 도달) → **BRACKET [MPM 아래끝, DEM 위끝]** → **DEM을 primary**(packing = DEM 영역,
    frame[5]), MPM은 plastic 하한, gap = 정량화된 모델 불확실성.  단일 "정답" 숫자 주장 금지.
- **gap < −4 (MPM ≫ DEM)** + SE-rich(SE/sol ≳ 50%) → **DEM ε-과압축 → MPM porosity 사용.**

**⚠ porosity lock/clamp는 신뢰성 0 (질문 직답):** MPM porosity를 DEM값(또는 floor)으로 **임의 clamp하면
그건 독립 측정이 아니라 DEM 숫자 복사 = 조작**.  그 수치엔 신뢰성이 없다.  **올바른 길은 clamp가 아니라
regime-gate** — 그 regime의 **옳은 모델**을 보고(frame[5]), 무너진 모델은 "이 regime 밖"이라 명시.
이건 숫자를 지어내는 게 아니라 *모델 선택*이다.  그리고 **두 모델이 일치하는 곳에서는 clamp가 애초에
필요 없다**(이미 검증됨).

---

## §5 신뢰성 판정 — 트랜드 (사용자 강조: "트랜드값도 중요")

porosity-vs-조성 **트랜드**도 regime-aware로 읽으면 robust하지만, **raw-MPM을 전 구간에 쓰면 틀린다**:

- **중간(production bimodal, SE/sol 30–50%)**: DEM·MPM 트랜드 **일치 → robust**.  조성·P:S 따라가는
  porosity 변화는 둘 다 신뢰.
- **SE-poor / mono-large 끝**: **DEM 트랜드가 진실**(Furnas dip + rebound).  MPM은 과압축으로 트랜드가
  **깨진다/뒤집힌다**.
  - ★ a9_50 sweep 재해석(중요 정정): DEM 17.9→12.7(dip)→**18.5(rebound)**, MPM 16.8→10.4→**9.3(rebound 없음)**.
    이전엔 "MPM no-rebound = 소성 SE가 큰 AM void를 채워 dip을 지움(frame[3])"으로만 해석.  그러나 p10은
    **SE-poor mono-large = MPM 과압축 regime**(gap +9.1) → **9.3%는 plastic void-fill(실물리) + over-compression
    (artifact)의 CONFOUND**.  깨끗이 분리 불가.  ⇒ **Furnas rebound의 진실은 DEM(18.5%)**, MPM의 "no-rebound"는
    과대 해석 금지.  `docs/a9_50_ps_sweep_vs_bimodal266.md` §발견3에 이 caveat 추가됨.
  - ✅ **frame[3] "plastic이 dip을 부분 erase"의 *깨끗한* 증거는 standalone 2D champion**(mpm2d_jamming
    `--e-se/--yield-se`, scaffold 아님 → 과압축 없음)**이지 scaffold a9_50 p10이 아니다.**  standalone에서
    dip 약화·768 수렴은 진짜 소성효과; scaffold mono-large는 과압축 confound.
- **SE-rich 끝**: **MPM 트랜드가 진실**.  DEM은 ε_sphere artifact로 porosity가 1–2%로 깔려 트랜드가 압축됨.

**트랜드 사용 가이드:** 한 sweep을 그릴 때 **한 모델로 전 구간을 긋지 말 것.**  중간은 둘 다, SE-poor/
mono-large 끝은 DEM, SE-rich 끝은 MPM.  또는 **|gap|≤4 케이스만으로 트랜드를 긋고** 두 corner는 해당
모델로 따로 표시.  (실용: porosity·dip·Furnas 트랜드는 **DEM이 owner** — frame[5] — 이므로 트랜드는 DEM을
기본으로, MPM은 SE-rich 절대값·소성 morphology에서 보강.)

---

## §6 고치는 법 (구현 옵션)

1. **regime-gate (추천)** — case의 (P:S, mAh, SE/solid)로 실패 corner를 감지하면 MPM porosity를 **flag +
   DEM값으로 대체 보고**(= 옳은 모델 선택, frame[5]).  자동으로 0% 같은 비물리 제거.  조작 아님.
2. **|gap| validity check (자동)** — 모든 케이스에 DEM↔MPM gap을 계산해 |gap|>4면 "regime-edge: trust
   {DEM|MPM}" 배지.  cross-validation을 production 지표로 노출.
3. **porosity-floor clamp** — ✗ **하지 말 것** (§4: 조작, 신뢰성 0).
4. **elastic-AM scaffold** — ✗ §1-②③④로 기각 (over-shielding + blow-up + drift).
5. (장기) servo descend guard: 평판이 DEM porosity 밑으로 내려가거나 wallP가 안 오르면 정지 → mono-large
   과압축 완화.  단 근본(frozen AM이 하중 못 받음)은 안 사라짐 → 1)/2)가 1차 방어.

---

## §7 재현 / 데이터
- 분류 데이터: `docs/data/mpm_dem_porosity_reliability.csv` (104 cases: case, P:S, SE/solid%, DEM/MPM porosity,
  gap, trust, verdict).  생성 로직 = 이 문서 §3 규칙.
- anchor 검증: real_14 (MPM 16.7 ↔ DEM 15.6 ↔ exp, 512 수렴) = `docs/mpm3d_calibration.md`.
- 트랜드 정정: `docs/a9_50_ps_sweep_vs_bimodal266.md` §발견3 (a9_50 p10 over-compression confound).

## §8 ★ wallP-조건부 재실행 cross-capacity 결과 + OUTLIER 분류 (2026-06-26, 진행중)
mono-large/SE-poor 코너 13개를 wallP 조건부(skeleton-spring, §6)로 재실행하며, **같은 조성의 다른 면용량
(areal capacity) 형제**와 비교해 어느 값을 믿을지 판정.  ★ **방법 = 같은 조성에서 DEM=MPM 으로 *일치하는*
고-면용량 형제(두껍고 입자 많아 통계 좋음)를 trusted anchor 로 잡고, 얇은 케이스를 그에 비춰 본다.**
(면용량↑ = 전극 두꺼움 = 입자 多.  DEM은 *얇을수록 느슨*(edge/통계) → thin-DEM은 보통 상단 outlier.)

| case | P:S | am_wt | SE/sol% | r_SE | DEM | MPM(재실행) | 같은-조성 bulk anchor (trusted) | 판정 |
|---|---|---|---|---|---|---|---|---|
| 1mAh_100_15 | 10:0 | 87 | 25 | 0.5 | 32.8 | **20.2** | ~20 (8mAh_real_10 19.0, 2mAh_real_15 21.3) | ✅ **MPM 신뢰** (thin-DEM 32.8이 outlier) |
| 1mAh_100_10 | 10:0 | 82 | 32 | 0.5 | 28.3 | **21.78** | ~17 (2mAh_real_10 17.9, 8mAh_real_5 16.8) | 🟡 **mid-bracket OK** [bulk17, thinDEM28.3], 과압축 아님 |
| 2mAh_real_20 | 10:0 | 92 | **16** | 0.5 | 29.3 | **22.2** | ~27 (8mAh_real_15 27.4=DEM27.3) | ⚠ **MPM 잔여 과압축** → DEM/8mAh(~27) 신뢰 |
| 2mAh_a9_p10 | 10:0 | 90 | 19 | **1.5** | 26.4 | **15.44** | 없음 (am_wt90+rSE1.5 = 2mAh만) | ⛔ **DEGENERATE** (perc 0%, RVE 작음) → 둘 다 불신 |
| 2mAh_a9_50_p10 | 10:0 | 90 | 19 | 0.5 | 18.4 | **11.95** | 없음 (a9 series 2mAh-only) | ⚠ **over-compress confound** (a9_50_ps §발견3) → MPM 하한, DEM/mid 신뢰; 단 구조 OK(perc 99.4%, ≠a9_p10 degenerate) |

### OUTLIER 3-regime (확정 규칙 — production/trend 사용 시 적용)
1. **SE 충분 (SE/solid ≳ 25 %) → MPM 신뢰.**  조건부가 잘 작동, MPM이 같은-조성 고-면용량 형제(DEM=MPM)와
   수렴.  이때 **thin 1mAh 의 DEM 이 outlier**(thin-loose, +10 %p 이상) — DEM 아닌 MPM/bulk 사용.
   예: 1mAh_100_15(20.2), 1mAh_100_10(21.78).
2. **SE 극빈 (SE/solid ≈ 16 %) → MPM 잔여 과압축.**  SE가 너무 희박해 frozen-AM scaffold에서 SE가 더 흘러
   조건부가 *완전히* 못 잡음.  같은-조성 고-면용량 형제(8mAh, DEM=MPM)가 진실을 가리킴 → **DEM/8mAh 쪽
   (상단) 신뢰, MPM은 하한.**  예: 2mAh_real_20 (MPM 22.2 ≪ bulk 27).
3. **DEGENERATE (r_SE=1.5 mono-large 또는 SE percolation 0 % 또는 RVE 과소) → 둘 다 불신, trend 제외.**
   SE망이 끊겨 이온적으로 죽은 구조 + 통계 부족 → DEM·MPM 모두 low-confidence.  cross-capacity 형제도 없음.
   예: 2mAh_a9_p10 (perc 0 %, SE 629개, RVE 40×40µm).  **degenerate-flag, scaling/trend 코퍼스에서 제외.**

⇒ **단일 케이스의 porosity 신뢰도는 SE/solid 와 degeneracy 로 결정**:  SE≥25 % MPM·SE≈16 % DEM/anchor·
degenerate 제외.  thin-DEM 의 "insufficient compaction(>25 %)" 경고는 *얇은 전극의 loose-packing artifact*
일 수 있으니 같은-조성 고-면용량 형제로 교차확인할 것.  (나머지 9개 재실행 진행중 — 같은 표/규칙으로 누적.)

---

## ★ 1.6× 표본 재확인 — 169 케이스에서 80% (2026-08-03)

위 신뢰성 수치(104 중 80개 = 76%)는 표본이 작아 "이 비율 자체가 우연 아니냐"가 열린 질문이었다.
통합 데이터층(`scripts/design_performance_dataset.py`)이 코퍼스 전체를 한 번에 조인하면서
**같은 판정을 169 케이스에서** 돌릴 수 있게 됐다:

| | 표본 | \|gap\| ≤ 4 %p | 비율 |
|---|---|---|---|
| 원 기록 (2026-06-26) | 104 | 80 | **76 %** |
| **재확인 (2026-08-03)** | **169** | **136** | **80 %** |

⇒ 표본을 1.6× 로 늘려도 비율이 **유지·소폭 개선**된다.  76 % 는 소표본 아티팩트가 아니었고,
DEM↔MPM 교차검증 밴드(±4 %p)는 코퍼스 규모에서 재현된다 (frame[4]).

측정 경로 (재현):
```bash
D=~/Yonghoon-DEM-DFT/webapp
python3 scripts/design_performance_dataset.py \
    --results $D/results --archive $D/archive --mpm-lab $D/mpm_lab \
    --out docs/data/design_performance_corpus.csv
# → 케이스 291 · DEM 291 · MPM 169 · STEP4 0
#   ★frame[4] porosity 교차검증: 136/169 가 |gap| ≤ 4 %p (80%)
```

⚠ **주의 (스키마)**: 코퍼스의 `mpm_metrics.json` 은 **webapp payload writer** 산출이라
`mpm3d_compaction --save-metrics` 와 키가 다르다.  porosity 키는 `porosity_mpm_pct`
(← `porosity_settled_pct` 아님), 두께는 `thickness_mpm_um`.  처음 배선이 이걸 틀려서
gap 이 **한 건도 계산되지 않았고** 그 사실이 "MPM 169 조인됨" 뒤에 숨었다 — 조인 건수와
**파생 지표 산출 건수를 따로 인쇄**해야 이런 침묵이 드러난다.

⚠ **금지 키**: 같은 스키마에 `coverage_AM_*_mpm_pct`(복셀-인접, ~26 %)가 들어 있다.
위 §"coverage PLASTIC vs RIGID" 가 **보고 금지**로 판정한 그 값이며, 이름이 그럴듯해
자동수집에 섞이기 쉽다.  데이터층은 `MPM_FORBIDDEN` 으로 명시 차단하고 selftest 가 부재를
확인한다 (ML feature 로 들어가면 격자 해상도를 물리로 학습하게 된다).

### 남은 것 — 33건이 문서의 두 corner 에 들어맞는가
실패 33건이 §"실패는 양 끝 두 corner 에 국한, 반대 방향" 예측대로
(a) mono-large(10:0)+thin → MPM 과압축 / (b) SE-rich(SE/sol ≳ 50 %) → DEM ε_sphere 과압축
에 떨어지는지는 **아직 안 봤다**.  gap 의 **부호**가 그 판별자다 (a 는 음, b 는 양).
CSV 가 이미 `porosity_gap_pp` 를 담고 있으므로 한 번의 집계로 확인 가능 — 맞으면 regime map
이 코퍼스 규모에서 입증되는 것이고, 안 맞으면 새 corner 를 찾은 것이다.
