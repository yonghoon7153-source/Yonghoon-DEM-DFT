# Design of multicomponent argyrodite based on a mixed oxidation state as promising solid-state electrolyte using moment tensor potentials — Ji Won Lee (J. Mater. Chem. A 2024)

> slug `lee2024_multicomponent_argyrodite_mixed_oxidation_mtp` · DOI `10.1039/d4ta00361f` · type `MLIP(MTP) + DFT` ·
> *J. Mater. Chem. A* **2024, 12, 7272–7278** · 투고 2024-01-16 / 수리 2024-02-16 / 게재 2024-02-19 ·
> 본문 7 pp + ESI 29 pp · digested 2026-07-28 · status ✅ (본문 + ESI 핵심 전수)
>
> **저자** Ji Won Lee¹, Ji Hoon Kim¹, Ji Seon Kim¹, Yong Jun Jang², Sun Ho Choi², Seong Hyeon Choi²,
> Sung Man Cho², Yong-Gu Kim², **Sang Uck Lee**¹* — ¹성균관대 화학공학 · **²현대자동차 (Hwaseong)**
> 과제: NRF 2021R1A2B5B01002879 · MOTIE P0022336 · **Hyundai Motor Company**
>
> 🔑 **덱에 없던 논문** — 서지 검색 중 발견해 우선순위 2위로 승격했던 그것.
> **우리 co-doping 캠페인과 정면으로 같은 문제설정**(다성분 치환 + 교호작용 + 합성가능성 필터).

---

## 1. 한 줄 요약

argyrodite의 P 자리를 **혼합 산화수 조합** Li₅₊₂ₓ₊ᵧ[A]ₓ⁴⁺[B]ᵧ⁵⁺[C]₁₋ₓ₋ᵧ⁶⁺S₅[D] 로 열어
([A]=Si/Ge/Sn, [B]=P/Sb, [C]=W/Mo, [D]=I→Cl/Br), **84개 구조를 MTP-MD로 전수**해
**[A]⁴⁺–[C]⁶⁺ 조합이 최고**임을 찾고, 그 이유를 **[C]⁶⁺의 solid-electrolyte inductive effect**(S 전하를
빼앗아 S–Li 상호작용을 약화)와 **[A]⁴⁺의 dynamic lattice effect**(셀 팽창 → Li 경로 확장)의
**시너지**로 설명한다. 여기에 **할로겐 혼합·과잉**을 얹어 σ_RT를 더 올린다.

---

## 2. 설계 공간 (Fig 1b) — 4개 군

**모체**: 완전질서 **Li₆PS₅I** (I⁻는 크기가 커서 4a 100% 점유를 선호 → 질서 모델이 타당)

| 군 | 조합 | 변수 | σ_RT 결과 |
|---|---|---|---|
| **(1)** | [B]⁵⁺–[C]⁶⁺ | y = 0.25, 0.5, 0.75 | **σ_RT ≈ 0** |
| **(2)** | **[A]⁴⁺–[C]⁶⁺** | x = 0.25, 0.5, 0.75 | **σ_RT > 27** ★ |
| **(3)** | [A]⁴⁺–[B]⁵⁺–[C]⁶⁺ | x, y = 0.25, 0.5 | σ_RT > 10 |
| **(4-1)** | (1)–(3)에 **Cl 또는 Br 치환** | | σ_RT > 10 |
| **(4-2)** | **할로겐 혼합 + 과잉** (Cl₁.₀Br₀.₅, Cl₀.₅Br₁.₀) | D₁.₅ | **38 < σ_RT < 82** ★★ |
| **(4-3)** | 할로겐 더 과잉 (Cl₁.₂₅Br₀.₅) | D₁.₇₅ | **σ_RT < 10** (역전!) |

**성능 순서 (본문 결론)**:
```
[A]⁴⁺–[C]⁶⁺  >  [A]⁴⁺–[B]⁵⁺–[C]⁶⁺  >  [A]⁴⁺–[B]⁵⁺  >  [B]⁵⁺–[C]⁶⁺
```
**원소 내 순서**: [A]에서 **Si⁴⁺ > Ge⁴⁺ > Sn⁴⁺** · [C]에서 **W⁶⁺ > Mo⁶⁺**

> 🔑 **(4-2) → (4-3) 역전이 핵심 소견 중 하나** — 할로겐 과잉이 단조 증가가 아니라 **최적점이 있다**.
> D₁.₅에서 최고, D₁.₇₅에서 급락. **우리 modelc(LPSCl1.6)가 D₁.₆으로 정확히 그 최적 구간에 있다.**
> ⚠ 단 그들 계는 I 기반 다성분이고 우리는 Cl 단일이라 직접 이식 금지 — "최적점 존재"라는
> **형태만** 공유한다.

---

## 3. 기구 두 가지 (Fig 3) ★★ 우리 언어로 번역 가능

### 3a. Solid-electrolyte inductive effect — [C]⁶⁺ (Fig 3d)
고산화수 양이온이 S의 전자를 끌어당겨 **S–Li 상호작용을 약화** → Li 이동 촉진.

| 중심 양이온 | S 전하 | Li⁺ 확산 |
|---|---:|---|
| **Si⁴⁺** | **−1.48 e⁻** | Strong S–Li → **억제** |
| **W⁶⁺** | **−0.84 e⁻** | Weak S–Li → **촉진** |

> 🔑🔑 **이건 우리 Bader/ICOHP 축과 같은 물리다.** 우리 cascade가 이미 쓰는
> "고산화수 도핑 → S 전하↓ → σ↑" 처방(kim2024 GB 논문의 결론이기도 함)이 **여기서 정량화**돼 있다.
> 우리 db의 Bader 전하를 이 −1.48 / −0.84 축에 얹을 수 있다.

**단, trade-off가 있다**: [C]⁶⁺ 도입은 전하중성 때문에 **Li 농도를 낮춘다**.
→ *"the [C]⁶⁺ incorporation ratio must be small enough to maintain the advantage of the
solid-electrolyte inductive effect over the effect of reducing Li-ion concentration."*
그래서 최적이 x=0.75 [A] / 0.25 [C] 쪽에 있다.

### 3b. Dynamic lattice effect — [A]⁴⁺
Si⁴⁺/Ge⁴⁺가 P⁵⁺보다 커서 **격자를 팽창**시키고 Li 확산 경로를 넓힌다. 동시에 Li 농도를 **올린다**
(Li₅₊₂ₓ₊ᵧ — [A]⁴⁺ 하나당 Li 2개 추가).

### 3c. 확산 양상 (Fig 3a–c, e)
- **군(1)** Li₅.₇₅P₀.₇₅W₀.₂₅S₅I: Li 궤적이 **4c-cage 안에 국소화** → cage 간 확산 거의 없음 → σ 낮음
- **군(2)** Li₆.₅Si₀.₇₅W₀.₂₅S₅I: **inter-cage diffusion**(4a-cage 경유) 발생 → σ 높음
- **van Hove 상관함수**: 군(1)·군(3) Li₅.₇₅Si₀.₂₅Sb₀.₂₅W₀.₅S₅I는 500 ps 동안 **~4 Å에 강한 피크**
  (= cage 안 갇힘). 군(2)·(3) 고전도체는 **전 거리에 분산** (= 수 ps 내 다중 이온 동시 hopping)

> 🔑 **van Hove 상관함수는 우리 MSD 파이프라인에 없는 진단이다.** "갇힘 vs 자유"를
> MSD 기울기가 아니라 **거리-시간 지도**로 판별한다 — 우리 disorder_ensemble의
> "ordered frozen" 판정을 훨씬 선명하게 만들 도구.

---

## 4. 최고 후보 (Table 1)

| Idx | 조성 | Ea (eV) | σ_RT (mS/cm) | **E_hull (meV/atom)** |
|---|---|---:|---:|---:|
| 27 | Li₆.₅Ge₀.₇₅Mo₀.₂₅S₅I | 0.16 | 27.14 | 43 |
| 28 | Li₆.₅Ge₀.₇₅W₀.₂₅S₅I | 0.15 | 51.98 | 35 |
| 29 | Li₆.₅Si₀.₇₅Mo₀.₂₅S₅I | 0.15 | 52.14 | **3** |
| **30** | **Li₆.₅Si₀.₇₅W₀.₂₅S₅I** | **0.14** | **62.93** | **2** |
| 45 | Li₆.₂₅Ge₀.₅Sb₀.₂₅W₀.₂₅S₅I | 0.17 | 14.93 | 30 |
| 46 | Li₆.₂₅Ge₀.₅Sb₀.₂₅Mo₀.₂₅S₅I | 0.17 | 16.35 | 37 |
| 47 | Li₆.₂₅Si₀.₅Sb₀.₂₅Mo₀.₂₅S₅I | 0.15 | 33.05 | 10 |
| 48 | Li₆.₂₅Si₀.₅Sb₀.₂₅W₀.₂₅S₅I | 0.16 | 33.74 | 5 |

**합성가능성 기술자: E_hull < 50 meV/atom** (참고문헌 59–61 근거).
> 🔑 우리 cascade에는 **hull 기반 합성가능성 필터가 없다**(Δe = host 대비 상대 형성E만).
> 이건 명확한 공백이고, `cascade_screening_funnel.json` 의 "G1이 vacuous"라는 진단과도 맞물린다 —
> 우리 G1은 hull이 아니라 host 상대값이라 아무도 못 떨어뜨린다.

---

## 5. 방법 (ESI Note S2·S3·S5)

- **DFT** VASP 5.4.4 · **MTP는 optB88-vdW 수준에서 학습** (kim2024가 판정한 그 functional)
- **MLIP** MTP (Shapeev), **MAML** python 패키지로 학습, pymatgen으로 스냅샷 추출,
  잡 관리 **CCpy** (`github.com/91bsjun/CCpy`) — 오픈소스
- **MD** LAMMPS. **MSD → D → Arrhenius 350–500 K → 300 K 외삽** (Fig S4)
  → **Nernst–Einstein** (Haven 보정 없음, eq S3)
- **에르고딕성**: *"we repeated MD simulations twice for the same structure"* → **2-시드**
- **무질서 처리 (Note S5)**: 3×3×3 슈퍼셀(27 unit cell, >1,000 원자).
  6개 특성 배열을 **열역학 안정성 가중**으로 랜덤 배분 (eq S5: `N_i = P_i(E)·n_s / ΣP_i(E)`,
  합이 27 아니면 최안정 배열 ±1 보정) — **kim2024와 동일한 random supercell 기법**.
  **I 기반 모델은 배열 1개(질서)만** 사용 (I⁻가 커서 4a 100% 선호).
- **계면·대기 안정성 (Note S6)**: **pseudo-binary** (eq S8–S10), pymatgen.
  - 계면: SSE ‖ {**LNO(LiNbO₃) 코팅**, **NCM811 양극**, **Li 음극**} 3종
  - 대기: SSE + H₂O pseudo-binary → **ΔE_H₂S**

---

## 6. ★★ ESI Table S1 — AIMD가 실험 대비 얼마나 틀리는가

| 조성 | **AIMD** | **MTP_optB88** | **실험** | AIMD 오차 |
|---|---:|---:|---:|---|
| Li₆PS₅I | 0.84 | **0.001** | **0.001** | **840×** |
| **Li₆PS₅Cl** | 4.6 | **2.46** | **2.3–2.5** | 1.9× |
| Li₆PS₅Br | 3.12 | 1.59 | 1.0 | 3.1× |
| Li₆.₅Si₀.₅Sb₀.₅S₅I | 9.0 | 13.6 | 11.6 | — |
| Li₆.₇₅Si₀.₇₅Sb₀.₂₅S₅I | **37.9** | **14.8** | **13.1** | **2.9×** |
| Li₃YCl₆ | 14 | 0.56 | 0.51 | **27×** |
| Li₇P₃S₁₁ | 57 | 6.5 | 4–17 | ~5× |

> 🔑🔑🔑 **우리 규율을 다시 다듬어야 한다 — 그리고 더 날카로워진다.**
>
> 지금까지 우리는 "MLIP σ 절대값 인용 금지"를 kim2024(**functional에 따라 8배**)를 근거로 세웠다.
> 이 논문은 **반대 방향의 데이터**를 준다: **optB88로 학습한 MTP는 8개 계에서 실험과 잘 맞는다.**
> 틀린 건 MLIP가 아니라 **AIMD**다(고온·짧은 시간·작은 셀 → Li₆PS₅I에서 840배).
>
> 두 논문을 합치면 정확한 명제는 이렇다:
> **"MLIP σ 절대값은 (a) 훈련 functional이 그 계에 맞고 (b) 같은 물질군에서 실험 검증을 거친
> 경우에만 신뢰할 수 있다."**
>
> **우리 UMA는 둘 다 만족하지 않는다** — OMat24(PBE 계열) 학습이라 optB88이 아니고,
> 우리 계에 대한 실험 대조 검증을 한 적이 없다. **따라서 우리 인용 금지 규율은 유지된다.
> 다만 이유가 "MLIP는 원래 못 믿는다"가 아니라 "우리 특정 설정이 검증되지 않았다"로 바뀐다.**
> 이건 규율을 약화시키는 게 아니라 **정확하게 만드는 것**이고, 동시에
> **T1(UMA 외삽/검증 대리지표)의 필요성을 한층 강하게 만든다.**

---

## 7. 계면·대기 안정성 (Fig S9·S10, Table S3·S4)

**모체 Li₆PS₅I 앵커** (Table S3, meV):

| vs LNO (LiNbO₃) | vs NCM811 | vs Li 음극 |
|---:|---:|---:|
| **−107.55** | **−424.46** | **−539.24** |

**결론**: *"regardless of [C]⁶⁺, **Sb⁵⁺ in [B] and Sn⁴⁺ and Ge⁴⁺ in [A]** provide significantly improved
electrochemical stability, electrode interfacial stability, and air stability."*

> 🔑 **정면 trade-off가 여기 있다**:
> - **전도도**: Si⁴⁺ > Ge⁴⁺ > **Sn⁴⁺** (Sn이 꼴찌)
> - **안정성(계면·대기)**: **Sn⁴⁺·Ge⁴⁺·Sb⁵⁺** 가 유리
>
> 즉 **Sn은 전도도를 깎고 안정성을 산다.** 그리고 이것이 이상욱 랩 가수분해 논문의
> **Sn 치환이 H₂S를 억제**한다는 결과와, 문장혁 랩 GNN이 예측한 **HSAB soft-acid(Sn/Sb/As)**와,
> 우리 db의 실험 앵커 **Taklu CuCl(H₂S 1.07→0.49)**과 **전부 같은 방향**이다.
> **독립 경로 5개가 Sn/Sb 계열 soft-acid 치환에서 만난다.**
>
> ⚠ 단 우리 cascade의 `air_hsab` 축은 정성 tier이고, 이 논문은 **pseudo-binary ΔE_H₂S**(eq S9–S10)
> 라는 **우리가 지금 당장 계산할 수 있는 정량 지표**를 쓴다 — M6와 같은 기계다.

---

## 8. 우리 대비 / 채택

| 항목 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| 문제설정 | P 자리 **다중 양이온 혼합 산화수** + 할로겐 혼합/과잉 | 코팅·첨가 화합물 47종 + 할로겐-rich(modelc) | **인접하지만 다름** — 그들은 골격 치환, 우리는 코팅/첨가 |
| 조합 수 | **84 구조** 전수 MTP-MD | codoping 1081쌍 (ML 대리) | 그들 전수 계산 / 우리 대리모델 |
| 교호작용 | inductive × dynamic lattice **시너지를 기구로 설명** | ML 교호작용 항 (LODO 누수 −0.255 실측) | **그들 우위** — 우리는 통계, 그들은 기구 |
| 합성가능성 | **E_hull < 50 meV/atom** | 없음(host 상대 Δe만) | **우리 공백 → T10** |
| 대기안정 | **pseudo-binary ΔE_H₂S 정량** | `air_hsab` 정성 tier | **우리 공백 → T2 대안** |
| 계면 상대 | 코팅 LNO + 양극 NCM811 + **Li 음극** 3종 | 양극만(→ SE 추가 중) | **우리 축이 좁다 → T9 확장** |
| 시드 | **2회 반복** | 3-시드 | ○ 우리가 약간 우위 |
| Arrhenius 창 | **350–500 K** | 600/800/1000 K | 그들이 저온 = 외삽 거리가 짧음 |
| 무질서 | 6배열 열역학 가중 random supercell | disorder ensemble + **배열간 분산 오차막대** | 우리 우위(오차막대) — 단 §9 주의 |
| σ 절대값 | 실험 대조 검증 후 인용 | 인용 금지 | **§6 — 우리 규율의 근거를 재정의해야** |

**채택 항목** (`kb/open_items.md` T9–T12로 등록):
- **T9** 계면 반응성 축을 **{양극, SE, Li 음극, 기존 코팅(LNO)}** 4종으로 확장 (이미 SE는 추가)
- **T10** **E_hull 기반 합성가능성 필터** 도입 — 우리 G1이 vacuous한 근본 원인
- **T11** **pseudo-binary ΔE_H₂S** 계산 — `air_hsab` 정성 tier를 정량으로 (M6 기계 재사용, 비용 거의 0)
- **T12** **van Hove 상관함수** 를 MSD 파이프라인에 추가 — "갇힘 vs 자유" 판별

---

## 9. 주의 / 한계

1. **σ_RT 38–82 mS/cm (군 4-2)** 는 **실험 argyrodite 최고치를 크게 상회**한다. Table S1의 검증은
   0.001–13 mS/cm 범위에서만 이뤄졌고, **82 mS/cm 영역에 대한 실험 대조는 없다** — 외삽이다.
   ⛔ **이 수치를 우리 자료에 절대값으로 옮기지 말 것.**
2. **Arrhenius 350–500 K, 300 K 외삽** — 창이 좁아(150 K) Ea 오차가 σ에 크게 증폭된다.
   Ea 오차막대가 본문·ESI에 **없다**.
3. **2-시드**로 에르고딕성 주장. 배열간 분산은 random supercell 하나로 흡수돼 **오차막대 없음**
   — kim2024와 같은 한계. (우리 config-variance 오차막대 신규성은 이 논문 범위에서도 유지된다.)
4. **E_hull 3–43 meV/atom** 인데 최고 전도체 일부는 35–43으로 컷(50) 가까이 있다. "합성 가능"이
   아니라 "합성 가능성 있음"이다. 실제 합성 보고는 없다.
5. **I 기반 모체**는 실험 σ가 0.001 mS/cm로 사실상 부도체다. 거기서 출발해 만든 개선폭은
   **Cl/Br 기반에서 같은 폭이 나온다는 보장이 없다** — 실제로 군(4)에서 Cl/Br 치환이 별도로 필요했다.
6. **W·Mo는 무겁고 비싸다.** 비용·경량 축 논의가 전혀 없다 — 우리 cascade의 `cost_tier`·경량 테마가
   그들에게 없는 것.
7. Fig 2·4의 y축은 σ_RT인데 **오차막대가 없다**(2-시드인데도).

---

## 10. 인용 가능 문장

- "고산화수 양이온([C]⁶⁺)은 S의 전자를 끌어당겨 S–Li 상호작용을 약화시키고(inductive effect),
  큰 4가 양이온([A]⁴⁺)은 격자를 팽창시켜 확산 경로를 넓힌다(dynamic lattice effect) — 둘의 시너지가
  다성분 argyrodite의 전도도를 지배한다[Lee 2024]."
- "AIMD는 고온·짧은 시간·작은 셀 때문에 실온 이온전도도를 크게 빗나갈 수 있으며,
  Li₆PS₅I에서는 실험 대비 세 자릿수 차이가 보고됐다[Lee 2024 Table S1]."
- "할로겐 과잉은 단조 개선이 아니라 최적점을 가진다 — D₁.₅에서 최고, D₁.₇₅에서 급락[Lee 2024]."
  (⚠ I 기반 다성분계 결과, 우리 Cl 단일계에 이식 금지)
- "Sn⁴⁺·Ge⁴⁺·Sb⁵⁺ 치환은 전도도를 다소 희생하는 대신 전기화학·계면·대기 안정성을 모두 개선한다[Lee 2024]."
