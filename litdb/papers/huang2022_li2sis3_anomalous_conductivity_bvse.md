# Anomalously High Ionic Conductivity of Li₂SiS₃-Type Conductors — Huang et al. (JACS 2022)

> slug `huang2022_li2sis3_anomalous_conductivity_bvse` · DOI `10.1021/jacs.1c13178` · type `exp (XRD·중성자 Rietveld·EIS·CV·full cell) + **BVSE**` ·
> *J. Am. Chem. Soc.* **2022**, 144, 11, 4989–4994 · 투고 2021-12-15 · **오픈액세스(CC BY)** ·
> 본문 6 pp + ESI 12 pp · digested 2026-07-28 · status ✅ (본문 + ESI 방법절 정독)
>
> **저자** Wenze Huang¹, Naoki Matsui¹, Satoshi Hori¹, Kota Suzuki¹, Masaaki Hirayama², Masao Yonemura³,
> Takashi Saito³'⁴, Takashi Kamiyama³, **Yuki Sasaki**⁵, **Yongsub Yoon**⁵'⁶, **Saheum Kim**⁶, **Ryoji Kanno**¹*
> ¹도쿄공업대 전고체전지연구센터 · ²도쿄공업대 화학과학공학 · ³'⁴KEK 중성자과학(J-PARC/SOKENDAI) ·
> ⁵**Hyundai Mobility Japan R&D Center** · ⁶**현대자동차 (화성)**
> CCDC 2128371 · 방사광 SPring-8 BL02B2 · 중성자 J-PARC SPICA
>
> 🔑 **이 논문이 우리 db 의 철회값을 판정한다** — `db/properties/external_benchmarks_symposium_2026.json`
> 의 `csp_metastable_conductivity` 에서 2026-07-28 철회했던 값 3개의 진짜 출처가 여기다.

---

## 1. 한 줄 요약

Li₂S–SiS₂–P₂S₅ 준3원계에서 **새 정방정 상 n-Li₂SiS₃**(P4₂2₁2, 실조성 **Li₁.₈₂SiP₀.₀₃₆S₃**)를 찾았고,
**고립 edge-sharing 사면체 이량체 (Si/P)₂S₆** 로 이뤄진 3D 골격이 기존 사방정 e-Li₂SiS₃
(**corner-shared 무한 SiS₄ 사슬**) 대비 **σ_RT 를 3자릿수 올린다**(2.4 mS/cm @ 298 K, Ea 0.28 eV).
기구는 **BVSE** 로 규명 — 부분점유 split Li 자리가 에너지 지형을 평탄화한다.

---

## 2. ★★ 우리 철회값 판정 (V5 후속)

`litdb/papers/kim2025_csp_metastable_edge_sharing_sse.md`(JACS 2025 CSP)는 σ 를 **보고하지 않는데**,
심포지엄 덱이 σ 값을 실어서 우리가 그대로 db 에 넣었다가 철회했었다. 그 값들의 출처가 이 논문이다
(JACS 2025 의 **ref 36**).

| 덱이 말한 것 | 이 논문 실물 | 판정 |
|---|---|---|
| edge-sharing σ = **2.4 mS/cm** | **2.4 × 10⁻³ S/cm = 2.4 mS/cm @ 298 K** (n-Li₂SiS₃) | ✅ **맞다 — 되살릴 수 있다** |
| corner-sharing σ = **1e-4 mS/cm** | 논문은 e-Li₂SiS₃ 의 σ 를 **수치로 안 준다**. "3 orders lower" 로부터 역산하면 **≈2.4 × 10⁻³ mS/cm** | ❌ **틀리다** (약 24배 차이) |
| 상승폭 **4자릿수** | 초록·본문·그래픽초록 모두 **"3 orders of magnitude" / "1000 times"** | ❌ **3자릿수가 맞다** |

> **결론**: `2.4 mS/cm` 는 **Huang 2022 의 실험값**으로 출처를 붙여 되살린다.
> `1e-4` 와 `4자릿수` 는 **철회 유지**. 그리고 이 수치는 **JACS 2025 계산 논문의 결과가 아니라
> Huang 2022 실험값의 소환**임을 반드시 병기해야 한다 — 덱이 남의 실험값을 자기 계산값처럼 옮겼다.

⚠ 추가 주의: 이 논문의 e-Li₂SiS₃ 비교 대상은 **ref 16 (Ahn & Huggins 1990)** 의 보고값이지
같은 연구에서 새로 측정한 것이 아니다. 즉 "3자릿수"도 **자기 측정 vs 문헌값 비교**다.

---

## 3. 물질과 구조

**합성**: Li₂S + P₂S₅ + SiS₂ 볼밀 **40 h @ 380 rpm**(Zr 포트 45 mL, 10 mm 볼 18개, Ar) → 펠릿 →
탄소 도가니 → 석영관 밀봉 → **T ≤ 823 K, 8 h**.

**n-Li₂SiS₃** (신상)
- 공간군 **P4₂2₁2 (94)**, 정방정, **a = 6.44743(3) Å, c = 11.50292(12) Å**
- 소광규칙 h00 h=2n · 0k0 k=2n · 00l l=2n
- 골격: **고립 edge-shared (Si/P)₂S₆ 이량체** (4f 사면체 자리, Si/P = **0.97 : 0.03** 고정) + LiS₄ 사면체
- **Li 자리 2개, 부분점유**: **Li1 4d 점유 0.866(8)** · **Li2 8g 점유 0.552(4)**
  → 논문: *"characteristic of superionic conductors"*
- 중성자 Rietveld R_wp = **3.06** (n-Li₂SiS₃ 99.17 % + Si 0.83 %)

**e-Li₂SiS₃** (기존, 비교군): 사방정 **Cmc2₁**, **corner-shared 무한 SiS₄ 사슬**, Li 8b
**m-Li₂SiS₃** (중간상): n 과 e 가 섞인 것 (P4₂2₁2 + Cmc2₁)

**상전이**: 온도를 올리면 **n → m → e** (Fig 3). 즉 **n 이 저온상**이고, 이량체가 열리며 사슬이 된다.
> ⚠ **JACS 2025 CSP 논문의 "준안정 edge-sharing" 서사와 방향이 다르다.** 여기서 edge-sharing(n)은
> **저온에서 얻어지는 상**이지 고온 준안정상이 아니다. 두 논문을 같이 인용할 때 이 점을 뭉개지 말 것.

---

## 4. 전기화학 (Fig 4)

| 물질 | σ @ 298 K | Ea |
|---|---|---|
| **n-Li₂SiS₃** | **2.4 × 10⁻³ S/cm** | **0.28 eV** |
| m-Li₂SiS₃ | (플롯) | ~0.5 eV |
| e-Li₂SiS₃ | n 대비 **3자릿수 낮음**(ref 16) | ~0.5 eV |

- **EIS**: 10 mV, **1 Hz – 7 MHz**, Solartron 1260, **228–383 K**. σT = A exp(−Ea/k_BT)
- 298 K Nyquist 에 **반원이 없다**(1 MHz 까지 sharp peak 만) — 228 K 아래에서야 반원이 보인다.
  → 논문 해석: **입계 저항이 작다**. 펠릿을 90 MPa 성형 후 **180 MPa · 673 K · 2 h** 만 눌렀는데
  상대밀도 **~85 %** 로 낮은데도 그렇다 = **분말이 무르고 성형성이 좋다**(soft, moldable).
  > 🔑 이건 산화물계(LLZO 등)가 >1173 K 소결을 요구하는 것과 대비되는 **황화물의 장점** 서사이고,
  > 우리 역학 축(E·G/B)과 개념적으로 이어진다.
- **CV**: −0.5 ~ 5.0 V vs Li/Li⁺, 1 mV/s. ~0 V 에서 Li 석출/용해만, **유의한 부반응 전류 없음**.
  ⚠ 논문 스스로 *"kinetically widening"* 이라고 쓴다 — **열역학적 창이 아니라 부동태화에 의한 동역학적 창**.
  (우리 ESW 규율의 "CV 넓은 창 = kinetic" 경고와 정확히 같은 문법)
- **풀셀**: n-Li₂SiS₃ 분리막 SE + **LNO 코팅 LiCoO₂ / LGPS 7:3** 복합양극 + **In–Li** 음극,
  1.9–3.6 V vs In–Li (≈0.62 V vs Li/Li⁺), **0.2 C, 298 K → ~120 mAh/g 가역**

---

## 5. ★★ BVSE — 우리와 같은 방법 (ESI + Fig 5)

**방법 (ESI p.3)**:
- **SoftBV 프로그램**, **Morse-type softBV force field** (transferable)
- **격자 해상도 0.1 Å**
- Rietveld 정련 구조를 입력 → Li site energy 계산 → 낮은 BVSE 영역 = 이동 경로
- **VESTA** 로 등가면 시각화

> 🔑🔑 **우리 `tools/comp1_v3/` 와 같은 계열이다.** 우리도 softBV(Li–X R0 = S 2.105 / Cl 2.249 /
> O 1.466, b = 0.37), BVSE = (BVS−1)², VESTA 배포.
> **차이는 격자 해상도**: 그들 **0.1 Å** vs 우리 **~0.25 Å**. 우리가 더 성기다.
> → 우리 채널% 정량의 해상도 민감도를 한 번 확인할 근거가 생겼다 (후속 항목).

**이동 장벽 (Fig 5a4 / 5b4)**

| n-Li₂SiS₃ (edge, 2D+1D) | e-Li₂SiS₃ (corner, 1D→2D→3D) |
|---|---|
| [Li2–i1–Li1–i2–Li2] **ab 평면 2D** 최적경로: 0.168 / 0.068 / 0.085 / 0.165 eV | [Li1–i1–i3–Li1] **[001] 1D** 최적: 0.338 / 0.387 / 0.046 eV |
| [Li2–i1–i1–i2–Li2] 로 상호연결 → **3D 퍼콜레이션, 유효장벽 0.228 eV** | [Li1–i1–Li1] 로 **bc 2D**, [100] 연결에 **0.367 eV** 필요 → 3D 는 여기서 막힘 |

> 🔑 **차원성 논증이 우리 `li_percolation` F* 프레임과 정확히 같다.**
> "1D → 2D → 3D 로 올라가는 데 필요한 유효장벽"으로 물질을 가르는 것이고,
> `kim2025_li3ycl6_new_crystal_structure` 의 **1D 퍼콜레이션 p_c = 1** 논증과도 같은 계열이다.
> **BVSE 유효장벽(0.228 vs 0.367 eV)이 실험 Ea 차이(0.28 vs ~0.5 eV)와 방향·크기가 맞는다**고
> 논문이 명시 — BVSE 가 정성 프록시로 작동한 사례.

**기구 결론**: 부분점유 split Li 자리(Li1 4d + Li2 8g)가 **에너지 지형을 평탄화**하고,
Li1 간극 이온과 이웃 Li2 가 **협동 확산(concerted diffusion)** 을 하게 한다.
split 자리는 **SiS₄ 무한 corner-shared 사슬 → edge-shared 이량체** 재배열로 저온에서 유도된다.

---

## 6. 우리 대비 / 채택

| 항목 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| BVSE 프로그램·force field | SoftBV, Morse-type | **동일 계열** | ✓ |
| BVSE 격자 해상도 | **0.1 Å** | ~0.25 Å | ⚠ **우리가 성기다** — 채널% 해상도 민감도 확인 필요 |
| BVSE 용도 | 이동경로 + **차원성별 유효장벽** | 채널% + blocking + F* | 같은 문법, 우리가 스크리닝 쪽으로 확장 |
| BVSE ↔ 실험 Ea | 0.228/0.367 eV ↔ 0.28/~0.5 eV **방향·크기 일치** | 대조 사례 없음 | **우리 BVSE 정당화에 인용 가능한 외부 사례** |
| Li 부분점유 | Rietveld 로 0.866 / 0.552 실측 | disorder ensemble(계산) | 실험 대조군 |
| CV 창 해석 | 스스로 **"kinetically widening"** 명시 | 같은 경고 규율 | ✓ 규율 일치 |
| 성형성 | 85 % 밀도로도 입계저항 작음 | 역학 축(E, G/B) | 개념 연결 |

**채택 항목**
1. **[즉시·인용] 철회값 부분 복원** — `2.4 mS/cm (Huang 2022, 실험)` 로 출처 붙여 되살리고,
   `1e-4`·`4자릿수` 는 철회 유지. **JACS 2025 계산값이 아니라 Huang 2022 실험값의 소환**임을 병기.
2. **[즉시·인용] BVSE 정당화** — "BVSE 유효장벽이 실험 Ea 와 방향·크기가 맞은 외부 사례"로
   우리 BVSE 축 서술에 인용.
3. **[후속·저비용] 격자 해상도 민감도** — 우리 0.25 Å 채널%를 0.1 Å 로 다시 뽑아 차이를 본다.
   차이가 크면 우리 채널% 정량의 신뢰구간이 바뀐다.
4. **[개념] 차원성 프레임 강화** — Huang(2D+1D vs 1D) + Kim Li₃YCl₆(1D p_c=1) 두 사례로
   `li_percolation` F* 의 문헌 근거가 두 개가 된다.

---

## 7. 주의 / 한계

1. **조성이 순수 Li₂SiS₃ 가 아니다** — 실제는 **Li₁.₈₂SiP₀.₀₃₆S₃** (Si/P = 0.97:0.03). P 가 소량 들어간다.
   "Li₂SiS₃ 가 2.4 mS/cm" 라고 쓰면 부정확하다.
2. **e-Li₂SiS₃ 의 σ 를 이 논문이 측정하지 않았다** — ref 16(Ahn & Huggins 1990) 소환값과 비교한 것이다.
   "3자릿수"는 **자기 측정 vs 문헌값**.
3. **CV 창은 동역학적**이다 (논문 자인). 열역학 ESW 로 인용 금지.
4. **σ 는 bulk + 입계 합산**이고 펠릿 밀도 **85 %** 다. 진밀도 보정 없음.
5. **BVSE 는 정전 프록시**다 — 전자구조·격자동역학·상관운동을 안 본다. 논문도 경로 식별용으로만 쓴다.
6. **n → m → e 가 승온 전이**라 n 이 **저온상**이다. JACS 2025 CSP 의 "준안정 edge-sharing" 서사와
   방향이 다르니 두 논문을 같이 인용할 때 뭉개지 말 것.
7. Ea 0.28 eV 는 **228–383 K** 창의 값. 우리 MD Ea(600–1000 K 외삽)와 창이 다르다 — 직접 비교 금지.

---

## 8. 인용 가능 문장

- "동일 조성 Li₂SiS₃ 에서도 SiS₄ 사면체의 연결방식이 corner-shared 무한사슬에서 고립 edge-shared
  이량체로 바뀌면 실온 이온전도도가 **3자릿수** 달라진다 (2.4 mS/cm vs ~10⁻³ mS/cm)[Huang 2022]."
- "BVSE 로 얻은 3D 퍼콜레이션 유효장벽(0.228 vs 0.367 eV)이 실험 활성화에너지 차이(0.28 vs ~0.5 eV)와
  방향·크기 모두 일치한다 — BVSE 가 이동 경로의 정성 프록시로 작동함을 보인 사례[Huang 2022]."
- "부분점유된 split Li 자리는 이동 에너지 지형을 평탄화하며, 이는 초이온전도체의 공통 특징이다[Huang 2022]."
- "황화물 전해질은 85 % 상대밀도에서도 입계 저항이 작아 고온 소결 없이 쓸 수 있다 — 산화물계가
  >1173 K 소결을 요구하는 것과 대비된다[Huang 2022]."
