# 기상성장 탄소섬유(VGCF) — 단섬유 4단자 저항률 · 압착분말 부피저항률(HTT·충전밀도 의존) · 인장물성 · 납축/Li-ion 전극 첨가 효과 — Endo et al. (Carbon 2001, Review article · Shinshu Univ. + Showa Denko + MIT)

> slug `endo2001_vgcf_basic_properties_battery_applications` · DOI `10.1016/S0008-6223(00)00295-5` · type `experiment + review (single-fibre 4-point resistivity · compressed-powder volume resistivity vs HTT & packing density · micro-tensile · lead–acid / Li-ion electrode additive)` · PDF `37d2ae22-1-s2.0-S0008622300002955-main.pdf` · digested `2026-09-25` · status ✅

> 본문 11 pp = Carbon **39** (2001) **1287–1297**, 첫 쪽 머리표 *"Review article"* (접수 2000-06-20 · 승인 2000-10-27). SI 없음.
> **이 카드의 "p." 는 저널 쪽** (PDF 쪽 n = 저널 p. 1286 + n).
> 그림 15 + Table 1 = **16장 전부** `litdb/figures/endo2001_vgcf_basic_properties_battery_applications/` — **16장 모두 손으로 다시 잘랐다**
> (자동 크로퍼는 9장만 잡았고 나란히 놓인 그림을 두 장씩 합쳐 잘랐다 · Table 1 은 쪽 전체를 잡았다 — §6 끝 크롭 메모).
>
> **계기**: 원고 SI Table S2 의 VGCF 전자전도도 행 각주 (원장 `SELF-51` · 작업 브랜치 `docs/reviews/si_table_response_20260925.md` §8 각주 ᵈ)
> 그리고 원장 `R20-04` 권고 ⓒ *"83 의 압력·밀도·측정법을 원장에 반입"*.  리포는 2026-08-18 부터 *"단섬유 1e-4 Ω·cm · 분말 0.012 Ω·cm"* 를
> 써 왔지만 **원문으로 확인한 적이 없었다**.  이 카드가 그 확인이다.
> ⚠ **이 논문은 "VGCF-H" 라는 이름을 한 번도 쓰지 않는다** (§3-5).  ⚠ **"0.012" 라는 숫자는 본문에 없고 그림의 한 점이다** (§3-2).

>
> ✅ **원고 사용 기록 (2026-09-26, 사용자 결정 — 작업 브랜치 `docs/reviews/si_table_response_20260925.md` §9-1 #13)**: SDCP 원고 SI 표 S2 *VGCF electronic conductivity (effective, fibre network) 1.0 × 10² S cm⁻¹* 의 출처 칸 = `Ref. [S(Endo)] (compressed powder)` — 근거는 §3-2 Fig. 8 압착분말 곡선 (100 S cm⁻¹ ≈ 0.92 g cm⁻³ 자리, 그림 판독).
> ⛔ *"100 = 83 반올림"* · *VGCF-H* 이름으로 인용 금지는 그대로.  E_VGCF 10 GPa 의 출처로는 쓰지 않는다 (Fig. 6 ≈110–310 GPa — 작업 브랜치 원장 `CL-93`).
---

## 0. ★ 원고 각주용 확인값 — 이것부터 (2026-09-25 PDF 원문 대조)

| 질문 | 확인값 | 근거 (쪽 · 그림 · 표) | 등급 |
|---|---|---|---|
| **단섬유 저항률 — 흑연화** | **1 × 10⁻⁴ Ω cm → σ = 1 × 10⁴ S cm⁻¹** | p. 1289 §3 본문 (인용문 = 이 카드 §3-1) · 흑연화 = **HTT 2800 °C** (Table 1 각주 b) | **stated** |
| **단섬유 저항률 — 탄화** | **1 × 10⁻³ Ω cm → σ = 1 × 10³ S cm⁻¹** | 같은 문장 · 탄화 = **HTT 1200 °C** (Table 1 각주 a) | **stated** |
| **단섬유 측정법** | *"longitudinal resistivity … measured using a **four-point method**"*, 섬유 직경은 **SEM 관찰** | p. 1289 §3 | stated.  ⚠ 섬유 개수 · 측정 섬유별 직경 · 온도 · 오차 · 중공(hollow) 단면 처리 **미기재** |
| **단섬유 직경** | Table 1 **0.2 µm** (SEM) · 서론 *"narrow diameter distribution (from 0.1 to 0.2 µm)"* | p. 1289 Table 1 · p. 1287 §1 | stated |
| **"0.012 Ω·cm" 가 이 논문에 있나** | **본문·표에는 없다** (문자열 0 건).  **Fig. 7 의 한 점**이다: 흑연화(≈2800 °C) s-VGCF, **부피밀도(volume density) 0.8 g/cm³ 고정** → **≈ 0.012 Ω cm** (픽셀 판독 **0.0119**) | Fig. 7 (p. 1292) + 본문 p. 1292 *"when the volume density is constant at 0.8 g/cm³"* | **조건 = stated · 값 = figure-read ≈** |
| 교차 확인 | Fig. 8 (흑연화, 밀도 스윕) 을 0.8 g/cm³ 에서 보간 → **≈ 0.0125 Ω cm** | Fig. 8 (p. 1292) | figure-read ≈ — **두 그림이 5 % 안에서 일치** |
| σ 환산 | 1/0.0119 ≈ **84** · 1/0.0125 ≈ **80** S cm⁻¹ (1/0.012 = 83.3) | — | DERIVED.  ⇒ 원고에는 **"≈ 80 S cm⁻¹" (≈ 0.012 Ω cm)** 로 — "83" 은 판독 정밀도보다 자릿수가 많다 |
| **압력 조건** | **없다.**  밀도만 준다 (가한 압력의 크기 · 압력↔밀도 관계 **미보고**) | p. 1292 §4 | 확인 |
| **분말 측정법** | 특수 시험셀에 시료를 넣고 **위에서 가압**, 부피저항률을 **가압 방향에 수직으로** 측정 | p. 1292 §4 (인용문 = 이 카드 §3-2) | stated.  ⚠ 단자 수(2/4) · 셀 치수 · 온도 · 반복 **미기재** |
| 분말값의 밀도 의존 | **≈ 1 Ω cm (0.13 g/cm³) → ≈ 0.0034 Ω cm (2.0 g/cm³)** = σ **≈ 1 → ≈ 300 S cm⁻¹ (≈ 300 배)** | Fig. 8 | figure-read ≈ ⇒ **"압착 분말값" 은 밀도를 붙이지 않으면 한 숫자가 아니다** |
| 분말 HTT 의존 (0.8 g/cm³) | ≈1200 °C **0.0296** · ≈2000 °C **0.0153** · ≈2800 °C **0.0119** Ω cm | Fig. 7 | figure-read ≈ |
| **영률 (탄성계수)** | **본문에 수치 없음.**  Fig. 6 (인장강도–인장탄성률 지도)에서 *"Carbonized s-VGCF and graphitized s-VGCFs"* 사각형 = **인장탄성률 ≈ 110–310 GPa · 인장강도 ≈ 1.2–3.0 GPa** | Fig. 6 (p. 1291), 탄소섬유 분류 배경 = Ref. [12] | figure-read ≈ · **측정점이 아니라 개략 영역** (측정법·개수 미기재) |
| 인장강도 | 흑연화 s-VGCF 21 점: 직경 ≈ 0.11–0.84 µm 에서 ≈ 54–214 kg/mm² = **≈ 0.53–2.1 GPa** · 가늘수록 강함 | Fig. 5 (p. 1291), 출처 Ref. [11] (Sudoh 1990 학회) | figure-read ≈ |
| **열전도도** | **n/a** — 서론의 정성 서술 *"very high electrical and thermal conductivity"* (일반 VGCF, Ref. [4,5]) 뿐 | p. 1287 | 확인 |
| "5 × 10⁻⁵ Ω cm (고흑연화 굵은 VGCF)" | **이 논문에 없다.**  *"s-VGCFs have … lower values [of conductivity] than normal VGCFs"* 라는 **정성** 문장(Ref. [10] 근거)뿐 | p. 1289 | 확인 — 리포 기록(CL-47 사용자 검증 메모)의 그 값은 **다른 출처**다 |
| **"VGCF-H" 인가** | **이름이 한 번도 안 나온다** (전수 0).  Showa Denko 공저자(K. Nishimura) · 회분 측정법 표기 "**SDK**" · Ref. [15] = *"Showa denko's catalog, Fine Carbon, V.G.C.F, 1997"* | p. 1287 · Table 1 · p. 1297 | 확인 — **VGCF-H 와 같은 등급인지 이 논문으로 판정 불가** (§3-5) |
| **우리 σ_VGCF = 100 S cm⁻¹** | 흑연화 단섬유의 **1/100** · 탄화 단섬유의 **1/10** · 0.8 g/cm³ 압착분말(≈ 80–84)의 **1.19–1.25 배** · Fig. 8 곡선에서는 **≈ 0.92 g/cm³ 자리** | §3-6 | DERIVED.  ⛔ **"100 = 83 반올림" 이라 쓰지 말 것** (100 은 83 감사보다 먼저 들어왔다 — `R20-04`) |
| **우리 E_VGCF = 10 GPa** | Fig. 6 영역(≈ 110–310 GPa)의 **1/11–1/31**.  우리 민감도 시험 범위(1–100 GPa)는 이 영역 **전부 아래** | §3-6 | DERIVED |

---

## 1. 한 줄 요약

**Showa Denko 공저**의 부동촉매(floating reactant)법 **서브마이크론 VGCF(s-VGCF, 직경 0.1–0.2 µm, 길이 10–20 µm)** 를
**탄화(1200 °C)** 와 **흑연화(2800 °C)** 두 상태로 놓고 ① 구조(XRD C₀ · Raman I_D/I_G · TEM) ② **단섬유 물성**(4단자 저항률 **1×10⁻³ → 1×10⁻⁴ Ω cm** · 인장강도 · 인장탄성률)
③ **압분체(bulk) 물성**(부피저항률의 HTT·**충전밀도** 의존 · 복원율 resiliency) ④ **전지 첨가 효과**(납축전지 양극판 저항 · 음극판 수명 · Li-ion 음극 자체 용량 · 흑연 음극 첨가 효과)를
한 편에 모은 **총설형 논문**이다.  ★ 우리에게 값진 것은 **단섬유 1×10⁻⁴ Ω cm (stated)** 와 **압착분말 ≈0.012 Ω cm @ 0.8 g/cm³ (Fig. 7 판독)** 가 **같은 섬유 · 같은 논문**에서
나온다는 것 — 두 값 사이 **≈ 120 배**가 섬유–섬유 접촉 · 충전 · 배향이 만든 손실이고, 그 분말값 자체도 밀도에 따라 **≈ 300 배** 움직인다 (Fig. 8).
⚠ 영률은 본문에 없고 Fig. 6 의 **개략 사각형**(≈ 110–310 GPa)뿐이다.  ⚠ 전지 결과는 **납축전지 · 액체 Li-ion 흑연 음극**이라 황화물 ASSB 양극으로 값이 옮겨지지 않는다.

---

## 2. 메타

| 저자 | 소속 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|---|
| **M. Endo**ᵃ\* · Y.A. Kimᵃ · T. Hayashiᵃ · **K. Nishimura**ᵇ · T. Matusitaᵃ · K. Miyashitaᵃ · **M.S. Dresselhaus**ᶜ | ᵃ Faculty of Engineering, **Shinshu University** (Nagano) · ᵇ **Showa denko company** (Tokyo) · ᶜ **MIT** | Carbon **39** (2001) **1287–1297** (Review article) | 10.1016/S0008-6223(00)00295-5 (PII S0008-6223(00)00295-5) | **submicron VGCF (s-VGCF)**, 부동촉매법 — **탄화(HTT 1200 °C) / 흑연화(HTT 2800 °C)**.  대조: "normal VGCF"(직경 10–20 µm, Fig. 2 는 10 µm) · 기존 탄소섬유(PAN · isotropic pitch) · SiC/SiN whisker | **실험 + 총설** — XRD/Raman/TEM · 단섬유 4단자 저항률 · 미세 인장 · 압분체 부피저항률 · 복원율 · 납축전지/Li-ion 전극 |

- 저자 철자: 제1쪽 **"T. Matusita"**, 참고문헌 [16] 은 **"Matushita T"** — 논문 안에서 철자가 다르다 (원문 그대로 둔다).
- 자금: JSPS "Research for the Future Program" Nano-carbon (Endo) · NSF-DMR 98-04734 · INT 98-15744 (Dresselhaus).
- ★ **데이터 출처가 그림마다 다르다** (총설이라서) — 인용할 때 반드시 확인:
  | 그림/표 | 출처 표기 |
  |---|---|
  | Table 1 · Fig. 1–3 · Fig. 7–9 · Fig. 12–14 | 인용 표기 없음 (저자 측 자료로 읽힌다) |
  | 단섬유 저항률 (본문 p. 1289) | 인용 표기 없음 — 비교 문장만 Ref. [10] |
  | Fig. 4 (장치) · Fig. 5 (인장강도) | **Ref. [11]** Sudoh, Daioh, Morimoto, Int. Symp. on Carbon 8B09 (1990) p. 518 |
  | Fig. 6 (강도–탄성률 지도) | **Ref. [12]** Dresselhaus et al., *Graphite fibers and filaments* (Springer 1988) p. 122 (본문은 [11,12]) |
  | Fig. 10–11 (납축전지) | **Ref. [14]** Hojo et al., YUASA-JIHO Tech. Rev. 72 (1992) 23 |
  | Fig. 15 (흑연 음극 + s-VGCF) | **Ref. [15,16]** Showa Denko 카탈로그 (1997) · Nishimura et al., J. Mater. Res. 15 (2000) 1303 |
- ⚠ **어느 그림에도 오차막대가 없고 반복 측정 수도 없다.**

---

## 3. ★★★ 확인값 상세 — 사용자 질문 1–5

### 3-1. 단섬유 전기저항률 — **stated** (p. 1289, §3 "Electrical conductivity and mechanical strength of single s-VGCFs")

원문 (p. 1289 오른쪽 단, 400 dpi 렌더로 기호 확인 — 텍스트 추출은 `×`·`Ω`·지수가 깨져 "1310 23 V cm" 로 나온다):
> *"The longitudinal resistivity of the s-VGCFs was measured using a four-point method and the fiber diameter was observed by a scanning electron microscope.
> Carbonized s-VGCFs show an electrical resistivity of **1×10⁻³ Ω cm**, whereas graphitized s-VGCFs show a value of **1×10⁻⁴ Ω cm**.
> Based on data in Ref. [10], s-VGCFs have higher electrical conductivity than conventional carbon fibers, and lower values than normal VGCFs due to the lower crystallinity of s-VGCFs as shown in Fig. 1."*

| 상태 | HTT (Table 1 각주) | ρ (Ω cm) | σ (S cm⁻¹) | 등급 |
|---|---|---|---|---|
| 탄화 s-VGCF | **1200 °C** | **1 × 10⁻³** | 1 × 10³ | stated |
| 흑연화 s-VGCF | **2800 °C** | **1 × 10⁻⁴** | **1 × 10⁴** | stated |

- 방향: **longitudinal** (섬유 축 방향).  섬유 직경: SEM 관찰 — Table 1 의 공칭값은 **0.2 µm**.
- ⚠ **안 적힌 것**: 측정한 섬유 수 · 각 섬유의 실제 직경 · 탐침 간격 · 온도 · 산포 · **중공 단면을 뺐는지**(Fig. 3a 가 중공 튜브를 보인다).
  두 값이 **정확히 한 자릿수 차이의 "1 ×"** 로만 적혀 있어 **자릿수 대표값**으로 읽는 것이 안전하다.
- ⚠ 마지막 문장의 *"as shown in Fig. 1"* 은 **Fig. 2** 여야 한다 (Fig. 1 은 SEM, 결정성은 Fig. 2 의 XRD/Raman) — §8 내부 불일치 목록.
- ★ **"고흑연화 굵은 VGCF 5–6 × 10⁻⁵ Ω cm"** 는 이 논문에 **없다**.  s-VGCF 가 normal VGCF 보다 덜 전도적이라는 **방향**만 있다 (Ref. [10] 근거).
  리포 CL-47 의 사용자 검증 메모가 *"Endo 본질 비저항 5e-5"* 라고 적은 값은 **다른 Endo 논문**(이 논문 Ref. [1,2] Koyama & Endo 1974 등이 후보, **미확인**)에서 왔을 것이다.

### 3-2. 압착분말(bulk) 부피저항률 — **조건 stated · 값 figure-read** (p. 1291–1292, §4 "Volume resistivity and resiliency in the bulk state")

**측정법** (p. 1292, 원문):
> *"A special apparatus to which was attached a testing cell was set up to evaluate the volume resistivity of the bulky samples, because it is not easy to test such samples by
> conventional methods under stable conditions due to their extremely low volume density in the range from 0.02 to 0.07 g/cm³.  That is, some portion of the sample is inserted
> into the testing cell, and pressure is applied to the cell from the upper part, and **the volume resistivity vertical to the direction of the applied pressure is measured**."*

**Fig. 7 의 조건과 저자 해석** (p. 1292, 원문):
> *"Fig. 7 shows the relation between the volume resistivity and HTT **when the volume density is constant at 0.8 g/cm³**.  The decrease in resistivity with increasing HTT is mainly
> attributed to the increased crystallinity with increasing HTT, such as decreased inter-layer spacing and increased crystallite size **if we assume that the contact resistance is
> the same for all samples**.  The electrical resistance of a sample of packed carbon fibers is **a sensitive function of the contact resistance between the fibers**, as indicated by
> the decrease in volume resistivity as a function of volume density; that is, the value of applied pressure is strongly related to the decreased contact resistance, as shown in Fig. 8."*

**Fig. 7 — 부피밀도 0.8 g/cm³ 고정, HTT 3점** (픽셀 판독: 프레임 x 1000→3000 °C, y 0→0.035 Ω cm, 마커 무게중심; 판독 오차 ≈ ±0.0001–0.0002 Ω cm — §5-4):

| HTT (판독) | ρ_V (Ω cm) | σ (S cm⁻¹) | 비고 |
|---|---|---|---|
| ≈ 1207 °C (탄화 1200) | **≈ 0.0296** | ≈ 34 | |
| ≈ 2009 °C | **≈ 0.0153** | ≈ 65 | 단섬유 값 **없음** (본문은 1200·2800 만) |
| ≈ 2802 °C (흑연화 2800) | **≈ 0.0119** | **≈ 84** | ★ **"0.012 Ω·cm" 의 출처 후보** |

**Fig. 8 — 흑연화 s-VGCF, 부피밀도 스윕** (y 로그 0.001–1 Ω cm · x 선형 0–2.5 g/cm³; 스캔 래스터가 ±5 px 불균일해 **가까운 눈금 사이 구간 보간**으로 보정; 마커 ≈ 28 개 — 0.55–1.0 g/cm³ 에서 겹쳐 ±2 개 불확실):

| 부피밀도 (g/cm³) | 고체분율 (÷ 진밀도 2.1) | ρ_V (Ω cm) | σ (S cm⁻¹) |
|---|---|---|---|
| ≈ 0.13 (첫 점, 위 틀선 위) | 0.06 | ≈ 1.0 | ≈ 1 |
| 0.2 | 0.10 | ≈ 0.29 | ≈ 3.4 |
| 0.3 | 0.14 | ≈ 0.10 | ≈ 10 |
| 0.4 | 0.19 | ≈ 0.053 | ≈ 19 |
| 0.5 | 0.24 | ≈ 0.031 | ≈ 32 |
| 0.6 | 0.29 | ≈ 0.021 | ≈ 47 |
| **0.8** | **0.38** | **≈ 0.0125** | **≈ 80** |
| 1.0 | 0.48 | ≈ 0.0087 | ≈ 115 |
| 1.2 | 0.57 | ≈ 0.0065 | ≈ 154 |
| 1.5 | 0.71 | ≈ 0.0046 | ≈ 215 |
| ≈ 1.98 (마지막 점) | 0.94 | ≈ 0.0034 | ≈ 296 |

- 🧮 **DERIVED — 곡선의 모양** (log ρ_V – log 밀도 기울기): **−2.8** (0.13–0.3) → **−2.3** (0.3–0.6) → **−1.7** (0.6–1.0) → **−1.3** (1.0–2.0 g/cm³).
  저밀도 쪽이 가파르다 = **접촉이 막 생기는(퍼콜레이션 문턱 근처) 영역**의 모양, 고밀도 쪽은 완만.
- 🧮 **DERIVED — 거의 치밀해도 단섬유에 못 미친다**: ≈ 2.0 g/cm³(진밀도의 94 %)에서도 ρ_V ≈ 0.0034 = 단섬유(1e-4)의 **≈ 34 배**.
  ⇒ 접촉저항만이 아니라 **배향 · 섬유 반경방향(c축) 전도** 도 남는다 (논문은 이 점을 논하지 않는다 — 우리 해석).
- ★ **"0.012 Ω·cm = 83 S/cm" 의 조건이 여기서 처음 붙는다**: 흑연화(2800 °C) s-VGCF(공칭 0.2 µm) 압분체, **부피밀도 0.8 g/cm³(≈ 38 vol% 섬유)**, 가압 방향에 **수직** 측정.
  Fig. 7(0.0119)과 Fig. 8 보간(0.0125)이 5 % 안에서 맞는다.  **압력값은 없다.**
- ⚠ 리포 원장 `R20-04` 가 기록한 **공급사(Resonac, 구 Showa Denko) 사양 0.017 Ω cm @ 0.8 g/cm³ (= 58.8 S cm⁻¹)** 는 **이 카드가 확인한 값이 아니다**
  (원장 스스로 *"두 건의 검색 스니펫 · PDF 사양서 미확보"* 라 적었다).  같은 0.8 g/cm³ 조건이 둘 다에 나오는 것은 공급사 시험 규약이 이 논문의 셀과 **같은 계보일 가능성**을
  시사하지만 **추정**이다.  🧮 참고로 Endo Fig. 8 곡선에서 σ = 58.8 은 **≈ 0.68 g/cm³** 자리다 — 두 "0.8 g/cm³" 값의 1.4 배 차이는 이 곡선 위에서 **밀도 ≈ 15 % 차이** 크기다.

### 3-3. 섬유 기하 · 밀도 · 표면적 · 산화 — **Table 1 (p. 1289), stated**

| 항목 | 탄화 s-VGCF (1200 °C) | 흑연화 s-VGCF (2800 °C) | 단위 | 방법 |
|---|---|---|---|---|
| 격자상수 C₀ | 6.900 | 6.775 | Å | XRD |
| 섬유 직경 | 0.2 | 0.2 | µm | SEM |
| 섬유 길이 | 10–20 | 10–20 | µm | SEM |
| 부피(겉보기)밀도 | 0.02–0.07 | 0.02–0.07 | g/cm³ | Tapping |
| 진밀도 | 1.9 | 2.1 | g/cm³ | Pycnometer |
| 비표면적 (BET) | 37 | 15 | m²/g | "N₂ absorption" (원문 그대로) |
| 회분 | 1.5 | 0.03 | % | SDK |
| pH | 5 | 7 | – | JIS-K6221 |
| 산화 개시온도 | 550 | 650 | °C | TGA |

- 본문 (p. 1289): *"high aspect ratio (>10²) and extremely low volume density in the range 0.02–0.07 g/cm³"*.
  🧮 Table 1 로 역산한 종횡비는 **L/d = 50–100** 이라 본문의 ">10²" 와 맞지 않는다 (직경 분포 0.1 µm 쪽이면 100–200) — §8.
- 🧮 **DERIVED — 비표면적 대 기하**: 속찬 원기둥 SSA = 4/(ρd) → d = 0.2 µm · ρ = 2.1 이면 **9.5 m²/g**, 실측 15 m²/g 는 **등가 직경 0.127 µm** 에 해당
  (0.1–0.2 µm 분포 · 열린 중공 등으로 설명 가능).  탄화 37 m²/g 는 등가 직경 0.057 µm = **기하만으로 설명 안 됨** (미세기공·거칠기 — 흑연화에서 사라짐).
- 🧮 d₀₀₂ = C₀/2: 탄화 **3.450 Å** → 흑연화 **3.388 Å** (normal VGCF 2800 °C ≈ 3.358 Å, Fig. 2a) — s-VGCF 는 2800 °C 에서도 normal VGCF 보다 **덜 흑연화**(저자: 작은 직경·곡률 탓).
- 흑연화 표면의 **~5 nm 비정질 "contaminated carbon"** (공업 흑연화 공정 중 생성, Fig. 3c) — 저자는 CFRP 기지와의 결합에 유리할 수 있다고 적는다 (p. 1289).

### 3-4. 기계적 성질 — Fig. 4–6 (p. 1290–1291)

- **측정 장치 (Fig. 4, Ref. [11])**: 유압 미세조작기(A) · 현미경(B) · 마이크로피펫(C) 두 개 사이에 섬유(E)를 접착제(D: "Binder" — **전극 바인더 아님**)로 고정 · 힘 변환기(F) → 증폭기(G) → 기록계(H) · 레버(I) · 모터(J) · 컴퓨터(K) · 비디오카메라(L)/녹화기(M).
  본문은 *"a micromanipulator, a high-speed video camera and a scanning electron microscope etc."* 라 적는다 (그림의 B 는 "Microscope" — 광학/전자 여부 불명).
- **Fig. 5 — 인장강도 vs 직경 (흑연화 s-VGCF · SiC · SiN whisker)**: 흑연화 s-VGCF 21 점 (픽셀 판독, 1 kgf/mm² = 9.807 MPa):

  | 직경 (µm) | 인장강도 (kg/mm²) | (GPa) |
  |---|---|---|
  | 0.11 | ≈ 214 | ≈ 2.10 |
  | 0.25 | ≈ 207 · ≈ 174 | ≈ 2.03 · 1.71 |
  | 0.29–0.49 | ≈ 79–150 | ≈ 0.77–1.47 |
  | 0.54–0.84 | ≈ 54–133 | ≈ 0.53–1.30 |

  저자 (p. 1290): *"The tensile strengths of all samples show a strong dependence on diameter, which is especially severe for the case of s-VGCFs … graphitized s-VGCFs have
  tensile strengths comparable to those of conventional whiskers."*  ⚠ 인장 시험 섬유의 직경(0.11–0.84 µm)이 공칭 0.2 µm 보다 **대부분 굵다**.
- **Fig. 6 — 인장강도 vs 인장탄성률 지도 (Ref. [12] 의 탄소섬유 분류 위에 s-VGCF 사각형)** (픽셀 판독, 축 0–700 GPa · 0–7000 MPa):

  | 영역 | 인장탄성률 (GPa) | 인장강도 (MPa) |
  |---|---|---|
  | **"Carbonized s-VGCF and graphitized s-VGCFs"** (격자무늬 큰 사각형) | **≈ 110–310** | **≈ 1210–2990** |
  | General grade (isotropic pitch) | ≈ 60–107 | ≈ 470–1170 |
  | High strength / Intermediate modulus / High modulus / Ultra-high modulus / High performance / High strain ultra-high strength | ≈ 200–250 / 285–335 / 300–400 / 450–700 / 490–650 / 200–250 | ≈ 3000–4500 / 3000–5500 / 2000–2500 / 2000–2500 / 2500–3300 / 4900–6100 |

  저자 (p. 1290): *"Carbonized and graphitized s-VGCFs show relatively higher values of tensile strength and modulus as compared to those of general grade (isotropic pitch) carbon fibers."*
  ⚠⚠ **이 사각형은 측정점이 아니다** — 탄화와 흑연화를 **한 상자로 묶었고**, 탄성률을 어떻게 쟀는지(힘–변위 곡선? 몇 개?) **본문에 없다**.
  ⚠ Fig. 5 의 강도 범위(≈ 0.5–2.1 GPa)와 Fig. 6 상자의 강도 범위(≈ 1.2–3.0 GPa)가 **어긋난다** (§8).
- **영률의 한 줄 판정**: *"서브마이크론 VGCF 단섬유 인장탄성률 ≈ 10² GPa (Fig. 6 개략 영역 ≈ 110–310 GPa)"* 까지만 쓸 수 있다.  **수치 하나를 고르면 가짜 정밀도.**
- **열전도도: n/a.**  (Fig. 6 의 사선 0.5/1/1.5/2 % 는 파단 변형률 = 강도/탄성률 등고선이다.)

### 3-5. ★ "VGCF-H" 와 이 논문 VGCF 의 관계

- **이 논문은 "VGCF-H" 를 한 번도 쓰지 않는다** (본문·표·캡션·그림 라벨 전수 — 텍스트 grep 0 건, 그림은 16장 육안).
  "VGCF" 를 **일반명사**로 쓴다 — "normal VGCFs (10–20 µm)" 와 "submicron VGCFs (s-VGCFs)" 를 모두 VGCF 라 부른다.
- **Showa Denko 연결 고리는 셋**: 공저자 K. Nishimura 의 소속(Showa denko company) · Table 1 회분 측정법 "**SDK**"(Showa Denko K.K. 약칭으로 읽힌다) ·
  Ref. [15] *"Showa denko's catalog, Fine Carbon, V.G.C.F, 1997"*(Fig. 15 출처).  ⇒ 이 s-VGCF 는 **Showa Denko 의 2000 년 전후 VGCF 제품군**으로 보인다 — **논문이 등급명을 적지 않는다.**
- **우리 리포의 "VGCF-H" 와 다른 점** (리포 기록 — `scripts/additives.py` `VGCF_D, VGCF_L = 0.15, 10.0  # Showa Denko VGCF-H; aspect ~67`, 우리 그룹 실험 카드 `kim2025` = Showa Denko, ~150 nm · ~10 µm):

  | | 이 논문 s-VGCF (흑연화) | 리포 "VGCF-H" (공급사 주석, **원본 데이터시트 파일 없음**) |
  |---|---|---|
  | 직경 | **0.2 µm** (분포 0.1–0.2) | **0.15 µm** |
  | 길이 | 10–20 µm | 10 µm |
  | 진밀도 | 2.1 g/cm³ | 2.0 (`DENS`) · `R20-04` 기록 2.0 |
  | 압착분말 @ 0.8 g/cm³ | ≈ 0.012 Ω cm (그림 판독) | 0.017 Ω cm (`R20-04`, 스니펫 2건 · 미확인) |

- ⇒ **원고 각주에서 "VGCF-H" 값으로 이 논문을 인용하면 틀린다.**  이 논문으로 인용하려면 **"graphitized submicron VGCF (≈ 0.2 µm)"** 로 적어야 한다.
  VGCF-H 이름을 쓰려면 **공급사 데이터시트 원본**이 따로 필요하다 (작업 브랜치 si_table_response §8 이 이미 *"데이터시트 파일 확보 뒤"* 로 보류해 둔 그 파일).

### 3-6. ★ 우리 값 대비 (질문 5) — **DERIVED**

| 우리 입력 | 값 | 이 논문 대비 | 판정 |
|---|---|---|---|
| σ_VGCF (STEP3 복셀, `SIGMA_DEFAULT['VGCF']`) | **100 S cm⁻¹** — *frozen, uncalibrated legacy voxel-network coefficient* (h = 0.15 µm 에서 직경보존 환산 78.5) | 흑연화 단섬유 1e4 의 **1/100** · 탄화 단섬유 1e3 의 **1/10** · 0.8 g/cm³ 압착분말 ≈ 80–84 의 **1.19–1.25 배** · Fig. 8 곡선의 **≈ 0.92 g/cm³ (≈ 44 vol%) 자리** | **[분말(0.8 g/cm³) ≈ 80 ↔ 단섬유 1e4] 밴드의 아래 끝, 분말값 바로 위.**  ⛔ **83 에서 유도된 값이 아니다** (`R20-04`: 도입 커밋 `087d1a07` 의 order-of-magnitude hook) — 이 논문은 **참조점**을 줄 뿐 **유도 근거가 아니다** |
| 복셀 표현의 섬유–섬유 접촉 | **저항 0** (닿은 섬유를 공유 셀로 융합 = `CONTACT_FREE` 가지, CL-81) | 이 논문: 같은 섬유가 **압분체가 되면 ≈ 120 배**(0.8 g/cm³) 저항해지고 그 값이 밀도로 ≈ 300 배 움직인다; 저자는 *"sensitive function of the contact resistance"* | 우리가 **지운 항이 실물에서 지배적**임을 보인다.  ⚠ 그러나 *"전부 접촉저항"* 은 이 논문도 말하지 않는다 (§5-3 · 2.0 g/cm³ 에서도 34 배) |
| 섬유 직경 | 0.15 µm | 0.2 µm | 등급 차 가능 — 이 논문으로 0.15 를 방어할 수 없다 (SEM 원자료 대기 = si_table_response §3) |
| 섬유 길이 · 종횡비 | 10 µm · 67 | 10–20 µm · 50–100 (Table 1 역산) | 같은 자릿수 |
| 진밀도 (wt → vol 환산) | 2.00 g/cm³ | 흑연화 2.1 · 탄화 1.9 | VGCF vol% 가 흑연화 값 대비 **+5 %** 크게 잡힌다 — 무시 가능 |
| **E_VGCF (MPM 섬유 재료점)** | **10 GPa** (`Assumed`, CL-42 `ADD_E_SET`; 1/10/100 GPa 민감도 = **h0**: Δε 0.18 %p · Δσ_e ≤ 0.25 %) | Fig. 6 영역 ≈ 110–310 GPa 의 **1/11–1/31** | `Assumed` 라벨이 맞다.  문헌 단섬유값을 각주에 넣으면 **"above the tested range"** 를 붙여야 한다 (시험 1–100 GPa, 이 영역은 110 부터) — 1→10 GPa +0.14 %p · 10→100 GPa +0.04 %p 로 **체감**하지만 **>100 GPa 는 미시험 외삽** |
| 열전도 (STEP3 thermal) | — | **n/a** | 이 카드는 VGCF 열전도 앵커를 못 준다 |

---

## 4. 실험 방법 ★ (각 값이 "어떤 종류의 값" 인지 가르는 자리)

### 4-1. 시료 (p. 1287–1289)
- **합성**: 탄화수소(benzene · methane) 를 전이금속 촉매 입자로 **1000–1300 °C** 에서 분해 [1–9].  **부동촉매(floating reactant)법** [6–8] =
  유기금속(ferrocene 등) 열분해로 생긴 촉매 입자와 탄화수소를 반응실 안에 **3차원 분산** → 고수율 · 균일 직경 → **양산 · 저가**의 유망 경로.
- s-VGCF 는 직경 분포가 좁고(0.1–0.2 µm) normal VGCF(10–20 µm, 중심 필라멘트 + 열분해탄소 외피의 나이테 구조 [4])와 **형태가 거의 같다**.
- 두 열처리 상태: **탄화 1200 °C** / **흑연화 2800 °C** (Table 1 각주).  구조 스윕(Fig. 2)은 1000–3000 °C.

### 4-2. 구조 (p. 1289–1290, Table 1 · Fig. 1–3)
- **FE-SEM (Fig. 1)**: 무작위 배향 · 수십 가닥씩 뭉침 · **반구형 끝(semispherical tip)** · 균일 직경 — *"very favorable when this fiber is applied as filler to improve electrical conductivity."*
- **XRD C₀ (Fig. 2a)** · **Raman R = I_D/I_G (Fig. 2b)** vs HTT, s-VGCF 와 normal VGCF(10 µm) 비교.  저자 해석: s-VGCF 는 C₀ 가 훨씬 크지만(덜 흑연화) R 은 비슷 →
  Raman 이 보는 **표층(광학 침투깊이 ≈ 400 nm)** 은 둘이 비슷하고 **벌크 결정성**은 s-VGCF 가 낮다 (작은 직경 · 표면 곡률).
- **TEM (Fig. 3)**: (a) as-grown — 중공 튜브, 튜브 지름이 촉매 입자보다 약간 작고 곧다; (b) as-grown 표층 — 무질서한 판(turbostratic), 넓은 회절점;
  (c) 흑연화 — 표면 ~5 nm 비정질 "contaminated carbon" 아래 **곧고 규칙적인 (002) 판**, 날카로운 (00l) 회절점 = **AB 층간 상관(3D 질서) 개시**.

### 4-3. 단섬유 저항률 (p. 1289) — §3-1
- **4단자, 섬유 축 방향(longitudinal)**, 직경은 SEM.  그 외 조건 미기재.

### 4-4. 미세 인장 (p. 1289–1290, Fig. 4–6, Ref. [11])
- 마이크로피펫 두 개 사이 섬유 고정 → 모터·레버로 인장 → 힘 변환기로 하중, 현미경 + 비디오로 관찰.  탄성률 산출법 **미기재**.

### 4-5. 압분체 부피저항률 (p. 1291–1292, Fig. 7–8) — §3-2
- 시험셀에 분말을 넣고 **위에서 가압**, **가압 방향에 수직으로** 저항률.  제어변수 = **부피밀도**(압력 아님).
- 저자가 꼽는 변수 (p. 1291–1292): *"the length and diameter of the fiber, its contact resistance, and the concentration of additives."*

### 4-6. 복원율 resiliency (p. 1292–1293, Fig. 9)
- 시료를 넣은 부피 V₀ → 일정 압력 P 하 부피 V₁ → 압력 제거 후 V₂.  ⚠⚠ **정의식이 본문과 캡션에서 서로 역수다** (§8-1).
- x 축 = *"Log(pressure/volume density, cm)"* (압력/밀도 = 길이 단위).

### 4-7. 납축전지 (p. 1292–1293, Fig. 10–11, Ref. [14])
- **양극판**: 활물질(평균 입경 2–5 µm; 원문은 *"active anode material … of the positive electrode"* — 용어 혼동, 활물질 조성 미기재) 에 흑연화 s-VGCF 를 wt% 로 첨가 → 경화(cured) 양극판
  (폭 10 mm · 두께 3.35 mm) 의 저항률.  Fig. 10 인셋: 양 끝 전원 + 안쪽 전압 단자 = **4단자 배치** (그림 판독).
- **음극판**: 0.5–1 wt% 첨가, **밀폐형(seal-type) 4 Ah 납축전지** 수명 — 방전 0.57 A → 1.70 V/cell, 충전 7.35 V (최대 1.5 A) 6 h.

### 4-8. Li-ion (p. 1293–1296, Fig. 12–15)
- **흑연화 s-VGCF 자체를 음극으로** (Fig. 12–13): 0–1.5 V, 0.2 mA/cm².  전해질·바인더·극판 조성 **미기재**.
- **상용 셀 음극 시트** SEM (Fig. 14): 인조흑연 + s-VGCF.
- **인조흑연(HTT 2900 °C) + s-VGCF 0/1/5/10 wt%** (Fig. 15, Ref. [15,16]): 0–1.5 V, 0.2 mA/cm².

---

## 5. 핵심 수치 ★ (stated / figure-read / DERIVED 구분)

### 5-1. 구조 (Fig. 2, figure-read ≈ — 격자 0.05 Å · 300 °C 로 눈금 판독)
| HTT (°C) | s-VGCF C₀ (Å) | normal VGCF C₀ (Å) | s-VGCF R = I_D/I_G | normal VGCF R |
|---|---|---|---|---|
| ≈ 1100 | — | — | — | ≈ 0.91 |
| ≈ 1300 | — | — | ≈ 0.81 | — |
| 1500 | — | ≈ 6.899 | — | ≈ 0.74 |
| 1600 | ≈ 6.917 | — | ≈ 0.70 | — |
| 1800 | ≈ 6.906 | ≈ 6.863 | — | — |
| 2000 | ≈ 6.874 | ≈ 6.853 | ≈ 0.33 | ≈ 0.20 |
| 2200 | ≈ 6.866 | — | — | — |
| 2400 | ≈ 6.826 | — | — | — |
| 2500 | — | ≈ 6.737 | — | ≈ 0.07 |
| 2600 | ≈ 6.796 | — | ≈ 0.08 | — |
| 2800 | ≈ 6.781 | ≈ 6.715 | — | — |
| 2900–3000 | ≈ 6.775 | — | ≈ 0.01 (3000) | ≈ 0.01 (3000, 겹침) |

⚠ Table 1 의 탄화(1200 °C) C₀ **6.900 Å** 가 Fig. 2a 의 1600 °C 값(≈ 6.917)보다 **작다** — HTT 에 대해 단조감소해야 하므로 **서로 맞지 않는다** (다른 로트? 논문 설명 없음, §8).

### 5-2. 전지 결과 (figure-read ≈, stated 는 표기)
| 항목 | 값 | 근거 |
|---|---|---|
| 납축 양극판 저항률 vs 흑연화 s-VGCF | **≈ 0.7 wt% → ≈ 8 × 10⁶ · 1.0 wt% → ≈ 4 × 10³ · 1.5 wt% → ≈ 1.3 × 10² Ω cm** (0.7→1.5 wt% 에서 ≈ 4.8 자릿수) | Fig. 10 (로그축 10⁰–10⁹ 픽셀 판독) · 본문 *"lowered for the case of 1.5 %"* (stated).  ⚠ 점 3개 · 0 wt% 없음 |
| 납축 음극판 (0.5–1 wt%) 수명 | 방전용량 70 % 도달: **무첨가 ≈ 410 → 첨가 ≈ 800 사이클 (≈ 2 배)**; 1000 사이클에 ≈ 48 % | Fig. 11 |
| 흑연화 s-VGCF 음극 첫 사이클 | 삽입 **364 mAh/g** · 탈리 **283 mAh/g** · 쿨롱효율 **77.7 %** (캡션) / *"about 77 %"* (본문) · 0.8 V 로 즉시 강하 · **0.7 V 어깨는 첫 방전에만** | Fig. 12 · p. 1293 (**stated**) |
| 2 µm VGCF 대비 | s-VGCF 가 *"relatively higher capacity due to their high surface area"* | p. 1294 · Ref. [13] (stated, 수치 없음) |
| 흑연화 s-VGCF 음극 사이클 | ≈ 305 → ≈ 258 mAh/g (≈ 240 사이클, ≈ 85 %) — *"fairly good cyclic efficiency … up to above 200 cycles"* | Fig. 13 |
| 인조흑연 + s-VGCF "cyclic efficiency" | 40–43 사이클에서 **0 % ≈ 90.5 · 1 % ≈ 92 · 5 % ≈ 94.6 · 10 % ≈ 100** (10 % 는 초기 ≈ 101 % 까지 오름) · 본문 *"almost 100 % up to 50 cycles"* (10 wt%) | Fig. 15 · p. 1294 |

### 5-3. 🧮 DERIVED — Fig. 7 두 점 + 단섬유 두 값으로 본 "HTT 에 안 따르는 몫"
- **관찰**: HTT 1200 → 2800 °C 에서 **단섬유는 10 배**(1e-3 → 1e-4) 좋아지는데 **압분체(0.8 g/cm³)는 2.5 배**(0.0296 → 0.0119)만 좋아진다.
- **저자 자신의 가정**(*"contact resistance is the same for all samples"*)을 그대로 두고 ρ_bulk = a·ρ_fiber + b 로 풀면 (미지수 2 · 점 2 — **검증 없는 정확해**):
  a ≈ 19.7, **b ≈ 0.0099 Ω cm** ⇒ 2800 °C 에서 **HTT 무관 항이 ≈ 83 %**, 섬유 고유 항 ≈ 17 % · 1200 °C 에서는 섬유 고유 항 ≈ 66 %.
- 읽는 법: 흑연화 압분체의 저항은 **대부분 섬유 자체가 아닌 곳**(접촉 · 경로)에서 온다 — 저자의 *"sensitive function of the contact resistance"* 와 같은 방향.
- ⚠⚠ **이 분해로 "전부 접촉저항" 이라 쓰면 안 된다**: ① 점 2개 정확해 ② 접촉저항도 HTT 에 따라 변할 수 있다(흑연화 표면의 5 nm 비정질층, Fig. 3c) ③ 2000 °C 는 단섬유 값이 없어 검증 못 한다
  ④ 리포 규약(methods v7 · `R20-04`)이 이미 *"one of several contributions"* 로 적고 있다 — 이 카드도 그 한정어를 바꾸지 않는다.

### 5-4. 디지타이즈 절차 (재현용)
- PyMuPDF 로 해당 쪽을 **400 dpi** 렌더 → 그레이 < 100~110 을 "검정" → **프레임 선**(가장 긴 수직/수평 검정 열·행)과 **점선 격자**(회색 < 200 이 폭의 35 % 넘는 행·열)로 축 보정.
- 마커: 연결성분(면적 창) 무게중심; 겹친 마커는 **거리변환 봉우리**로 분리 (Fig. 8 사슬 구간은 여전히 ±2 개 불확실).  Fig. 8 · Fig. 10 은 로그축이라 **눈금 사이 구간 보간**.
- 판독 불확도: 마커 중심 ±2 px ≈ Fig. 7 에서 ±0.0001 Ω cm, Fig. 8 에서 ±1.5 %.  **개략 사각형(Fig. 6)은 테두리 선 두께(≈ 2 GPa) 만큼.**

---

## 6. Figure set ★ (본문 15 + Table 1 = 16, **전부 크롭 · 육안 확인 2026-09-25**)

| Fig | 내용 | **우리가 재사용할 것** |
|---|---|---|
| **1** | FE-SEM 두 배율 — (a) 10 µm: 무작위 배향 섬유망, 수십 가닥 뭉침 (b) 500 nm: **반구형 끝** · 균일 직경 | 섬유 형태 정성 (직선에 가까움 · 끝이 둥글다) |
| **Table 1** | 탄화/흑연화 s-VGCF 기본 물성 9 행 (§3-3) | ★ 직경 0.2 · 길이 10–20 · 탭밀도 0.02–0.07 · **진밀도 2.1** · BET 15 · 회분 0.03 % · 산화개시 650 °C |
| **2** | (a) C₀ vs HTT 1500–3000 °C (b) I_D/I_G vs HTT 1000–3000 °C — s-VGCF vs normal VGCF(10 µm) | 흑연화 정도 = 단섬유 σ 의 뿌리 (§5-1).  ⚠ 캡션 "crystallite size (C₀)" = 실제로는 **격자상수** |
| **3** | TEM (a) as-grown 중공 튜브 100 nm (b) as-grown 표층 격자상 5 nm + SAED (c) 흑연화 표층 5 nm + SAED — **~5 nm 비정질 피복** | 표면 상태 = 섬유–섬유 · 섬유–SE 접촉의 실제 계면 (정성) |
| **4** | 미세 인장 장치 개략도 A–M (Ref. [11]) | 인장강도 측정법 — 탄성률 산출법은 안 보인다 |
| **5** | 인장강도(kg/mm²) vs log 직경 — 흑연화 s-VGCF · SiC · SiN whisker (Ref. [11]) | 강도 ≈ 0.5–2.1 GPa · **직경 의존** (§3-4) |
| **6** | 인장강도(MPa) vs 인장탄성률(GPa) 지도 — 탄소섬유 등급 + **s-VGCF 사각형** + 파단변형률 등고선 0.5–2 % | ★★ **영률의 유일한 근거** ≈ 110–310 GPa — **개략 영역** |
| **7** | 부피저항률 vs HTT, **부피밀도 0.8 g/cm³** — 3점 | ★★★ **"0.012 Ω·cm" 의 출처** (2800 °C 점 ≈ 0.0119) |
| **8** | 흑연화 s-VGCF 부피저항률(로그) vs 부피밀도 0.13–2.0 g/cm³ | ★★★ **분말값의 밀도 의존 ≈ 300 배** · closure 보정 표적 후보 (§10 ③) |
| **9** | (a) 복원율 측정 개략 V₀ → V₁(가압) → V₂(제거) (b) 복원율(vol %) vs log(압력/밀도) — 흑연화 s-VGCF(2800 °C) ≈ 104–178 % · s-VGCF(○) ≈ 85–119 % · Crackerchop C-107F ≈ 29–59 % · PAN MLD-100… (Toray) ≈ 40–51 % · "Fnakabo S-241" ≈ 19–40 % | 섬유 매트의 **스프링백** 서열 (흑연화 > 탄화 ≫ 기존 탄소섬유).  ⚠ 정의식 불일치 — **서열만** (§8-1) |
| **10** | 납축 양극판 저항률(로그 10⁰–10⁹) vs 흑연화 s-VGCF wt% 0.7/1.0/1.5 + 측정 인셋 | 첨가량에 따른 **퍼콜레이션형 급락** (정성) — 납축 양극 경화판이라 값 이식 불가 |
| **11** | 밀폐형 4 Ah 납축전지 방전용량(%) vs 사이클 — 무첨가 vs 음극판 첨가 | 70 % 수명 ≈ 2 배 |
| **12** | 흑연화 s-VGCF 음극 첫 사이클 충방전 곡선 (364 / 283 mAh/g) | 섬유 자체의 Li 삽입 용량 — 우리 모델에 없음 (VGCF 는 전자상만) |
| **13** | 흑연화 s-VGCF 음극 용량 vs 사이클 0–240 | — |
| **14** | 상용 셀 탄소 음극 시트 단면 SEM (a) Cu 박 위 5 µm (b) 확대 3 µm — 흑연 플레이크 사이 섬유망 | 섬유가 입자 사이를 **다리 놓는** 실사진 (정성) |
| **15** | 인조흑연(2900 °C) 음극 "cyclic efficiency" vs 사이클, s-VGCF 0/1/5/10 wt% | wt% ↑ → 유지 ↑ 의 단조 서열 (액체계) |

⚠ **오차막대 없음** (모든 그림).

**크롭 메모** (재추출 시 필독, `litdb/pdf_map.tsv` 에도 적었다): 이 PDF 의 그림은 전부 **가는 래스터 띠의 모자이크**(그림당 125–542 조각 · 쪽당 최대 881)이고, 두 단에 **그림이 나란히** 놓인 쪽이 많다.
`extract_figures.py` 자동 크롭은 **16개 중 9개**만 잡고, **Fig. 2+3 · 5+6 · 10+12 · 11+13 을 한 장씩으로 합쳤으며**, Table 1 은 **쪽 전체**(y 34.7–667.9)를 잡았다
→ 16장 전부 **그림 영역 안 래스터 조각의 합집합 + 백색 여백 제거**(흰색 = 세 채널 > 244, 여백 8 px @ 300 dpi) 로 다시 잘랐다 (`figures.json` 의 `recrop` / `manual_crop`, 전부 `viewed: true`).
⛔ `--slug endo2001_vgcf_basic_properties_battery_applications --clean` 을 다시 돌리면 **이 16장이 사라지고 합쳐진 9장이 돌아온다.**

---

## 7. 논지 흐름 · 저자 기전 (Post-processing)

1. **왜 탄소인가** (p. 1287): 전지 탄소재의 두 이유 = **높은 전기전도도 + 여러 전해질에서의 내식성**.  VGCF 는 흑연 기저면이 섬유 축에 평행한 **나이테(annular) 조직** →
   뛰어난 역학 · 매우 높은 전기·열 전도 · 높은 흑연화성.  부동촉매법이 **양산·저가** 경로.
2. **구조** (§2): s-VGCF 는 normal VGCF 보다 벌크 결정성이 낮지만 표층은 비슷하다 (XRD vs Raman 깊이 차이).  흑연화하면 3D 질서가 생긴다 (TEM).
3. **단섬유** (§3): 탄화 1e-3 → 흑연화 1e-4 Ω cm; 기존 탄소섬유보다 전도적, normal VGCF 보다 덜 전도적(결정성).  강도는 whisker 급, 탄성률·강도는 범용(isotropic pitch) 탄소섬유보다 높다.
   ⇒ *"very promising as a filler for electrodes in batteries."*
4. **벌크** (§4): 전극 충전재로 쓰려면 섬유 자체만이 아니라 **충전 상태(bulky state)** 를 봐야 한다 — 부피저항률은 HTT(결정성)와 **밀도(접촉저항)** 로 떨어진다.
   극히 낮은 탭밀도 · 가는 직경 · 강도 때문에 **눌러도 치밀해지기 어렵고 풀면 되돌아온다** = **resiliency** — 흑연화 > 탄화 ≫ 기존 탄소섬유 (*"intertwined entanglements"*).
   ⇒ Li-ion 음극의 부피변화 응력을 흡수하고 **물리적 바인더** 구실을 할 것이라는 **기대** (§4 에는 데이터 없음).
5. **납축전지** (§5): 양극판 저항률 ↓ (1.5 %), 음극판 수명 ↑ — 기전 주장 = 물리적 바인더(탈락·붕괴 억제) · 동심 결정 배향의 **내산화성** · 망 형성에 의한 **활물질 이용률 ↑**.
6. **Li-ion** (§6): 섬유 자체가 283 mAh/g 가역(2 µm VGCF 보다 큼 = 표면적), 200 사이클 이상 양호; 흑연 음극에 첨가하면 wt% ↑ → 사이클 유지 ↑ (10 wt% 에서 50 사이클 ≈ 100 %),
   *"At higher concentrations, the s-VGCF carbon fibers interconnect between graphite powder particles to form a continuous conductive network."*
   부수 효과 = 전해액 흡수·보유 · 전극의 복원성·압축성.
7. **결론 (a)–(g)** (p. 1296): (a) 가는 직경 → 얇은 전극에 균일 분산 + 넓은 반응 면적 (b) 전극 전도도 향상 = **섬유 자체 고전도 + 흑연 입자와 fiber-mat 망 형성**
   (c) whisker 대비 섬유의 삽입능이 용량을 깎지 않음 (d) fiber-mat 망 → 전극 유연성 (e) 삽입 응력 흡수 → 내구성 (f) 전해액 침투 개선 (g) **카본블랙 대비** 장기 사이클 개선.
   ⚠ (c)·(g) 는 **이 논문 안에 대응 데이터가 없다** (카본블랙 비교 그림 0).

---

## 8. ★★ 비판적 검토 — 내부 불일치 · 인용 전 확인 목록

### 8-1. 복원율 정의식이 본문과 캡션에서 **서로 역수**다
- 본문 p. 1292: **R_V = (V₀ − V₁)/(V₀ − V₂)** · 캡션 Fig. 9 (p. 1293): **R_v = (V₀ − V₂)/(V₀ − V₁) × 100 %** (두 곳 모두 400 dpi 로 확인).
- 물리적으로 V₀ > V₂ ≥ V₁ 이면 본문식은 **≥ 100 %**, 캡션식은 **≤ 100 %** 다.  그런데 Fig. 9b 는 **≈ 19 %(기존 섬유) 부터 ≈ 178 %(흑연화 s-VGCF) 까지** 한 축에 놓는다
  ⇒ **어느 식도 그림 전체를 설명하지 못한다** (다른 정의 — 예: 압축 부피 대비 팽창 — 였을 가능성, 논문 설명 없음).  ⇒ **Fig. 9b 는 서열만 인용한다.**
### 8-2. 그 밖의 불일치 (원고 인용 전 확인용)
| # | 불일치 | 위치 | 영향 |
|---|---|---|---|
| 1 | 결정성 근거를 *"as shown in Fig. 1"* 로 적음 — 실제는 **Fig. 2** | p. 1289 | 없음 (참조 오기) |
| 2 | Fig. 2 캡션 *"crystallite size (C₀)"* vs 축·Table 1 *"lattice constant"* vs 본문 *"interlayer distance C₀"* | p. 1289–1290 | C₀ = c 축 격자상수(= 2 d₀₀₂) 로 읽는다 |
| 3 | Table 1 탄화(1200 °C) C₀ 6.900 Å < Fig. 2a 1600 °C ≈ 6.917 Å | p. 1289–1290 | 로트 차이 가능 — 구조값을 HTT 연속함수로 섞어 쓰지 말 것 |
| 4 | 본문 종횡비 *">10²"* vs Table 1 역산 50–100 | p. 1289 | 자릿수 표현 |
| 5 | 인장 시험 섬유 직경 0.11–0.84 µm (Fig. 5) vs 공칭 0.2 µm | p. 1291 | 강도·탄성률이 **공칭 섬유의 값인지** 불명 |
| 6 | Fig. 5 강도 ≈ 0.5–2.1 GPa vs Fig. 6 상자 ≈ 1.2–3.0 GPa | p. 1291 | Fig. 6 은 개략 — **Fig. 5 가 측정점** |
| 7 | *"active anode material … of the positive electrode"* | p. 1292 | 납축 **양극** 활물질로 읽는다 (조성 미기재) |
| 8 | "discharge capacity 283 mAh/g" = 탈리(가역) 용량, 첫 삽입은 364 | p. 1293 / Fig. 12 | 반쪽셀 방전·충전 호칭 관례 차이 |
| 9 | Fig. 15 "cyclic efficiency" 가 **100 % 를 넘는다** (≈ 101 %) | Fig. 15 | 쿨롱효율이 아니라 **1사이클 대비 용량유지율**로 보인다 — 정의 없음 |
| 10 | 결론 (g) "카본블랙 대비 개선" | p. 1296 | **대응 데이터 없음** |
| 11 | 저자 철자 Matusita (1쪽) vs Matushita (Ref. [16]) | p. 1287 / 1297 | 서지 입력 시 1쪽 표기 |
| 12 | Ref. [1] *"Jpn J Appl Phys 1974;3(7):1175–6"* — 같은 해 Ref. [2] 는 13(12) | p. 1296 | 권호 오기 가능 (1974 JJAP 는 13 권대) — 인용 전 확인 |

### 8-3. 값의 성격 (반드시 붙일 한정어)
- 단섬유 두 값은 **"1 ×" 한 자리 대표값** — 산포·개수 없음.  ⇒ *"≈ 10⁴ S cm⁻¹"* 형으로.
- 압착분말 값은 **그림 판독** 이고 **밀도 0.8 g/cm³ 에서만** 의미가 있다.  압력값 없음.  **순수 섬유 압분체**다 (바인더·활물질·전해질 없음).
- 영률은 **개략 영역**이다.

---

## 9. 우리 DEM+MPM 대비 (frame[4] · frame[5])

> ⚠ **이 논문에는 DEM·MPM·미세구조 모델이 하나도 없다.**  frame[4] 교차검증 상대가 **아니라 상(phase) 입력 앵커**다.
> frame[5] 로는 **양쪽에 한 칸씩** 걸린다: **전달 쪽** = STEP3 복셀 σ_e 의 VGCF 상 계수 (DEM 접촉망 σ_e 는 AM 골격 — VGCF 상이 없다) · **역학 쪽** = MPM 섬유 재료점의 E_VGCF.
> 이 논문이 가진 반쪽 = **상 물성(단섬유 · 압분체)**, 없는 반쪽 = **전극 속 섬유망** (바인더·SE·AM 과 섞인 상태의 전도·역학).

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| VGCF 상 σ_e | 단섬유 1e4 (흑연화, stated) · 압분체 ≈ 80 @ 0.8 g/cm³ (figure-read) | 100 S cm⁻¹ frozen legacy coefficient (→ 78.5 @ h 0.15) | §3-6: 밴드 아래 끝.  **100 은 이 값들에서 유도되지 않았다** |
| 섬유–섬유 접촉 | 압분체 저항이 밀도로 ≈ 300 배 · 저자 *"sensitive function of the contact resistance"* | 복셀 융합 = **0** (CL-81 `CONTACT_FREE`) | 실물에서 지배적인 항을 우리가 지웠다 — **σ 계수로 뭉뚱그린 보상**이 CL-47 의 인식론 (DEM E_eff 18 배 연화와 같은 부류) |
| 측정 방향 | **가압 방향에 수직** (면내) | STEP3 σ_e 는 **두께 방향** (가압 방향) | 가압하면 섬유가 면내로 눕는 경향 → 방향 의존 가능 (논문 미논의) — 값 대조 시 한정어 |
| 섬유 함량 | 압분체 = **≈ 38 vol% 섬유** (0.8/2.1) | 전극 고체 중 VGCF **≈ 1.9 vol%** (80:18:1:1) · **≈ 5.6 vol%** (Lee 80:17:3:0.5) — `DENS` 로 환산 | **7–20 배 희박** · 기지가 SE/AM.  ⇒ **압분체 곡선을 전극 섬유망으로 옮기지 말 것** |
| 직경 · 길이 | 0.2 µm · 10–20 µm | 0.15 µm · 10 µm | 등급 차 가능 (§3-5) |
| E_VGCF | ≈ 110–310 GPa (Fig. 6 영역) | 10 GPa `Assumed` (h0 민감도 1–100) | 1/11–1/31 · 시험 범위 밖 |
| 섬유 파단 | 강도 ≈ 0.5–2.1 GPa, 직경 의존 | 섬유 파단 모델 없음 | 건식 혼합·압연 중 섬유 절단은 우리 축 밖 (§H 혼합 공정 축과 연결) |
| 열전도 | n/a | STEP3 thermal 채널 | 앵커 없음 |
| 표면 | 흑연화 표면 ~5 nm 비정질 탄소 | 없음 (#30 carbon-SE 분해 훅은 **면적만** 센다) | 탄소–황화물 계면 반응성을 볼 때 **표면 상태가 등급마다 다를 수 있다** (훅 후보, 값 없음) |

### ★ 반드시 붙일 통제 경고
1. **순수 섬유 압분체 ≠ 전극 속 섬유망** — 함량(38 vs 2–6 vol%) · 기지 · 가압 이력 · 측정 방향이 다 다르다.  압분체 값은 **자릿수 참조점**이다.
2. **그림 판독값**을 stated 로 격상하지 말 것 — "0.012" 이상 자릿수 금지, "83" 대신 "≈ 80".
3. **VGCF-H 이름으로 이 논문을 인용하지 말 것** (§3-5).
4. **100 의 유도 근거로 쓰지 말 것** (`R20-04`) — *"coincides with"* 까지.
5. 영률은 **개략 영역** — *"of order 10² GPa"* 까지.

---

## 10. 적용 인사이트 — 우리 연구에 어떻게

- ① **SI Table S2 각주 ᵈ 의 비어 있던 출처를 채운다** — 단 문구를 이 논문이 말하는 대상으로 맞춘다 (§13 초안): "VGCF-H" → **"graphitized submicron VGCF (≈ 0.2 µm)"**,
  "~83 S cm⁻¹" → **"≈ 80 S cm⁻¹ (≈ 0.012 Ω cm) at a packing density of 0.8 g cm⁻³"**.  methods v7 초안의 두 곳(단섬유 문장 · "compressed-powder (≈ 83 S cm⁻¹) measurements of VGCF-H")도 같은 수정이 필요하다.
- ② **원장 `R20-04` 권고 ⓒ 의 절반이 닫힌다** — "83" 의 **밀도(0.8 g/cm³) · HTT(2800 °C) · 측정 방향(가압에 수직) · 측정 셀 형식**이 원문에 있다; **압력은 원문에도 없다**.
  (원장 갱신은 작업 브랜치 몫 — 이 카드는 근거만 둔다.)
- ③ ★ **closure 보정 표적 제안 (제안만 · 사전등록 전)**: Fig. 8 은 **같은 섬유의 σ(충전밀도) 곡선**이다.  STEP3 로 **순수 섬유 RVE** 를 몇 개 밀도(예: 0.3–1.2 g/cm³)에서 만들고
  σ_fiber = 1e4 (이 논문 stated) 로 풀면 "융합 복셀 = 접촉 0" 상한이 나온다 → **실측/상한 비 = 밀도별 접촉 손실 인자**.
  이것이 `R20-04` 권고 ⓓ *"RVE 측정으로 국소 closure 를 보정"* 의 **조성이 안 맞는 첫 표적**이다.
  ⚠ 걸림돌: 0.2 µm 섬유 vs 0.15 µm 복셀(d/h ≈ 1.3) · 측정 방향(면내) · 가압 시 섬유 배향 · 섬유 곡률 미지 · 38 vol% 순수 섬유 압분체를 만드는 경로(겹침·압밀)는 미검토.
- ④ **E_VGCF 각주 ᵇ 에 문헌 자릿수를 붙일 수 있다** — Ozkan 2010 PDF(미확보) 없이도 이 논문 Fig. 6 으로 *"of order 10² GPa, above the tested range"* 까지.
- ⑤ **CL-48 (σ_VGCF_OVERRIDE = 7854 = 1e4 · π/4) 의 "1e4" 가 원문으로 앵커된다** (흑연화 2800 °C · 4단자 · 0.2 µm 섬유).  단 CL-47 이 정리했듯 그 팔은 **이중 완전화 = 탄소망 상한 프로브**다.
- ⑥ 탄화 등급(1e3)과 흑연화 등급(1e4)의 **10 배 차이**는 공급사 등급 선택만으로 섬유 고유 σ 가 한 자릿수 움직일 수 있다는 뜻 — 우리 규약은 섬유 고유 σ 보다 **접촉**에 민감하다는
  CL-47 판정과 합치면, 등급 차이가 전극 σ_e 에 주는 영향은 **1 자릿수보다 훨씬 작을 것**이다 (§5-3: 흑연화 압분체에서 HTT 가 2.5 배만 움직인다) — **정량은 미측정**.

---

## 11. 한계

### 11-1. 저자가 밝힌 것
- 압분체 해석에서 **"접촉저항이 모든 시료에서 같다고 가정하면"** 이라는 조건을 스스로 붙였다 (p. 1292).
- s-VGCF 의 벌크 결정성이 normal VGCF 보다 낮다 — 전도도도 그만큼 낮다 (p. 1289).
### 11-2. 우리가 추가하는 것 (논문이 말하지 않은 것)
- **압력값 0** · 압분 셀의 단자 수·치수 · 온도 · 반복 0 · 오차막대 0.
- **탄성률 측정법 0** — Fig. 6 은 분류 지도 위 개략 사각형.
- **총설** — 여러 그림이 인용 출처(학회 초록 · 사내 기술지 · 카탈로그)에서 왔다 (§2 표).
- 전지 결과는 **납축전지 · 액체 Li-ion 흑연 음극** — 황화물 ASSB 양극·건식 공정과 무관.
- 섬유 **열전도도 수치 0**.
- 섬유 **등급명 없음** — VGCF-H 와의 동일성 판정 불가.

---

## 12. 기법 미니 용어집

| 용어 | 뜻 (이 카드에서) |
|---|---|
| **VGCF** | vapor-grown carbon fiber — 탄화수소를 금속 촉매 위에서 기상 분해해 키운 탄소섬유.  이 논문은 일반명사로 쓴다 |
| **s-VGCF** | submicron VGCF (직경 0.1–0.2 µm) — 부동촉매법 산물 |
| **normal VGCF** | 직경 10–20 µm 의 고전적 VGCF (기판 성장 + 열분해탄소 외피) |
| **부동촉매(floating reactant)법** | 촉매 전구체(ferrocene 등)와 탄화수소를 반응로 안에 떠 있는 상태로 공급 — 연속 양산형 |
| **HTT** | heat treatment temperature — 탄화 ~1000–1500 °C, 흑연화 ~2500–3000 °C |
| **C₀** | 흑연 c 축 격자상수 = 2 d₀₀₂ (흑연화될수록 작아짐) |
| **I_D/I_G (R)** | Raman D 밴드(무질서) / G 밴드(흑연) 세기비 — 작을수록 흑연화 |
| **4단자(four-point)법** | 전류 단자와 전압 단자를 나눠 접촉저항을 빼고 시료 저항만 재는 법 |
| **volume density (부피밀도)** | 분말 질량 / 차지한 부피 = 겉보기(충전)밀도.  탭밀도는 두드려 채운 값 |
| **volume resistivity (부피저항률)** | 압분체 시편의 유효 저항률 (섬유 + 접촉 + 공극 전부 포함) |
| **resiliency (복원율)** | 가압 후 제거 시 부피가 되돌아오는 정도 — 정의식은 §8-1 |
| **turbostratic** | 흑연 판이 쌓였지만 층간 상관(AB 적층)이 없는 상태 |
| **contaminated carbon** | 공업 흑연화 중 섬유 표면에 쌓인 ~5 nm 비정질 탄소 (Fig. 3c) |
| **CONTACT_FREE 가지 (우리)** | 접촉 협착 저항을 뺀 전달 계산 — 복셀 FV 가 여기에 있다 (CL-81) |

---

## 13. 인용 가능 문장 (deck / 원고용)

**(A) SI Table S2 각주 ᵈ — 권장안** (작업 브랜치 `si_table_response_20260925.md` §8 초안의 마지막 문장을 교체):
> ᵈ Effective conductivity assigned to the VGCF phase in the voxel model; not calibrated.  Because the voxel model merges touching fibres, this value represents the fibre network
> including fibre–fibre contact losses rather than a single fibre.  For reference, Endo et al. report a longitudinal (four-point) resistivity of 1 × 10⁻⁴ Ω cm (≈ 10⁴ S cm⁻¹)
> for single submicron vapour-grown carbon fibres graphitized at 2800 °C, and a volume resistivity of ≈ 0.012 Ω cm (≈ 80 S cm⁻¹) for the same fibres compressed to a packing
> density of 0.8 g cm⁻³ (Ref. Sx, read from Fig. 7).

**(A′) 요청 서식 그대로 채운 판**:
> … single graphitized submicron VGCF filaments ~1 × 10⁴ S cm⁻¹ (1 × 10⁻⁴ Ω cm, four-point) and compressed powder of the same fibres ~80 S cm⁻¹ (≈ 0.012 Ω cm) at a packing density of 0.8 g cm⁻³ (Ref. Sx).

**(A″) 밀도 의존을 한 줄 덧붙일 때** (선택):
> …; the compressed-powder value itself falls from ≈ 1 to ≈ 0.003 Ω cm as the packing density rises from ≈ 0.1 to 2.0 g cm⁻³ (Ref. Sx, Fig. 8).

**(B) Methods v7 수정안** (현재 *"VGCF-H having a single-filament resistivity of 1 × 10⁻⁴ Ω cm"* · *"compressed-powder (≈ 83 S cm⁻¹) measurements of VGCF-H"*):
> … graphitized submicron VGCF having a single-filament resistivity of 1 × 10⁻⁴ Ω cm [Endo 2001] … separating single-filament (≈ 10⁴ S cm⁻¹) from compressed-powder
> (≈ 80 S cm⁻¹ at a packing density of 0.8 g cm⁻³) measurements of graphitized submicron VGCF [Endo 2001] …

**(C) E_VGCF 각주 ᵇ 에 덧붙일 때**:
> … The tensile modulus of single submicron VGCFs is of order 10² GPa (≈ 100–300 GPa; Ref. Sx, Fig. 6), above the tested range.

**(D) 한국어 한 줄 (발표용)**: *"같은 흑연화 VGCF 가 단섬유로는 10⁴ S/cm 인데 0.8 g/cm³ 로 눌러 담으면 ≈ 80 S/cm — 두 자릿수가 섬유 사이에서 사라진다 (Endo 2001).
우리 복셀은 그 접촉을 융합해 버리므로 VGCF 계수 100 은 재료상수가 아니라 섬유망 유효값이다."*

⛔ **쓰면 안 되는 문장**: *"100 S/cm was rounded from 83 S/cm"* · *"VGCF-H powder 83 S/cm (Endo 2001)"* · *"the difference is entirely fibre–fibre contact resistance"* ·
*"the Young's modulus of VGCF is 200 GPa (Endo 2001)"* (영역을 한 수로) · *"VGCF thermal conductivity (Endo 2001)"* (없음).

---

## 14. 관련 카드 (litdb 내부 교차참조)

- `lawrence2008_single_vgcnf_elastic_modulus_morphology` — (2026-09-26 추가) **E_VGCF 짝 카드**: 개별 VGCNF (Pyrograf III) 17 가닥의 **굽힘** 탄성률 **6–207 GPa** (AFM 3점 굽힘 · 형태와 1:1).  이 카드의 Fig. 6 영역(인장, 개략)과 합쳐 E_VGCF 각주의 문헌 위치가 두 줄로 선다.  판정: *"10 GPa · Ref. [Lawrence]"* 출처 칸 **불가**, `Assumed` + 범위 참조 각주 **조건부** (그 카드 §0).
- `kim2025_conductive_agent_se_coating_cathode` — **우리 그룹** 실험 VGCF (Showa Denko, ~150 nm · ~10 µm) vs Super P · SE 코팅 복합양극 σ_e.
- `lee2025_corolling_dryprocess_lpscl_ptfe` — LPSCl + NCM811 + **VGCF 3 wt%** + PTFE: 복합체 σ_e ≈ 34 mS/cm · PTFE 0.5 → 5 wt% 에서 ≈ 3,000 배 붕괴 (우리 Lee 대조 A 의 상대).
- `lee2025_dual_fibrous_ptfe_dry_electrode` · `matthews2024_ptfe_nanofibril_network` · `zhang2026_dryprocess_electrode_architecture_cell_level` — 건식 전극의 VGCF–PTFE 섬유망 형태.
- `cho2024_conflicting_roles_conductive_additive` · `kim2024_carbon_volumetric_occupation_se_domain` · `reisacher2023_percolation_sulfide_carbon_matrix` — 탄소 상의 부피 점유 · 퍼콜레이션 양면성.
- `koo2026_swcnt_sheath_thick_electrode` · `kim2026_charge_engineered_cnf_binder` — 다른 1D 탄소 (SWCNT · CNF).
- `patil1987_self_doped_conducting_polymers` — 같은 INDEX 절(첨가제/바인더 상 앵커)의 SDCP σ 짝 카드: **VGCF 는 [분말 ↔ 단섬유] 밴드가 이 논문으로 원문 확인됐고, SDCP 는 밴드 자체가 없다** (CL-61).
- `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` · `aminchiang2016_nmc_electronic_ionic_transport_vs_li` — 다른 상(AM)의 σ_e 입력 앵커.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
