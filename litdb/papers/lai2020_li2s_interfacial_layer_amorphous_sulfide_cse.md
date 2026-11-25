# Stabilizing a Lithium Metal Battery by an In Situ Li₂S-modified Interfacial Layer via Amorphous-Sulfide Composite Solid Electrolyte — Lai et al. (*Nano Lett.* 2020)

> slug `lai2020_li2s_interfacial_layer_amorphous_sulfide_cse` · DOI `10.1021/acs.nanolett.0c03395` · type `exp 주 + DFT 보조` · PDF `litdb/inbox/85. Lai2020_…pdf` (본문 9 pp) + `85. Sup) …pdf` (SI 22 pp) · digested `2026-09-01` · status ✅
> elements: Li, S, P, F, O, Fe
> methods: DFT, NEB, XPS
> **저자**: Chen Lai¹², Chengyong Shu¹, Wei Li³, Liu Wang², Xiaowei Wang⁶, Tianran Zhang², Xuesong Yin⁵, Iqbal Ahmad¹, Mingtao Li¹, Xiaolu Tian¹, Pu Yang¹, **Wei Tang\***¹⁴, **Naihua Miao\***³, **Guangyuan Wesley Zheng\***²⁵ · *Nano Lett.* **2020**, 20(11), 8273−8281
> 🔗 **이 digest 의 존재 이유**: `papers/liu2024_pband_center_sbo_dual_interface.md` §6.4 가 *"Li₂S 0.22 eV · LiF 0.67 eV 는 ref [30b] 소환값"* 이라고 판정하며 지목한 **그 [30b] 원출처**다. 1저자 질문 = *"진짜로 NEB 를 했는지 봐라."* → **§0 · §6 · §11 이 답이다.**

---

## 0. ★★ 검증 임무 결론 요약 (먼저 읽는다)

| 물음 | 답 | 증거 |
|---|---|---|
| **(A) 서지 동일성** — 이게 정말 Lai, *Nano Lett.* 2020, 20, 8273 인가 | ✅ **동일하다.** 저자 14명 이름·순서·교신 3인까지 Liu 2024 ref [30b] 와 완전 일치 | 표지 `Cite This: Nano Lett. 2020, 20, 8273−8281` · DOI `10.1021/acs.nanolett.0c03395` · PDF 메타 Title `nl0c03395 1..9` · 워터마크 `article-pdf/20/11/8273/18456487/nl0c03395.pdf` |
| **(B) NEB 실재 여부** | ✅ **실재한다.** 자기 계산이다 — 소환값이 아니다 | ① SI 에 **DFT 계산 방법 절이 있다**(전문 §6.1) ② `CI-NEB` 명시 + Henkelman 2000 인용 ③ **`Fig. 3e`·`Fig. 3f` 에 MEP 곡선 실물**(각 7점 + 구조 인셋) ④ **`Fig. S11`** 에서 자기 값을 *"Present work"* 로 문헌값과 나란히 표시 |
| **(C) 0.22 eV 의 최종 귀속** | ✅ **이 논문의 자체 CI-NEB 계산.** 인용 사슬은 3단이 아니라 **2단에서 끝난다** (Liu 2024 → Lai 2020 = 원출처) | 본문 *"the **calculated** migration energy barrier of Li ions passing through LiF layer is 0.67 eV, while it is 0.22 eV for that in Li₂S layer"* + `Fig. S11` 의 **"Present work"** 라벨 |
| **(D) 우리 0.305 eV 와 비교 가능한가** | ⛔ **불가.** 다섯 축 중 **①셀 ②전하규약 ③홉정의 가 전부 어긋난다** | §11. 특히 ③ — 그들 것은 **여분 Li 한 개가 얇은 슬랩을 위→아래로 뚫는 6단 다중홉**이고, 우리 것은 **벌크 하전 공공의 최근접 c→c 단일홉** |

**★ 이 digest 가 새로 캔 것 (Liu 2024 digest 에는 없던 사실)**
1. **논문 스스로가 "Li₂S"(벌크, 문헌) 와 "Li₂S layer"(자기 계산) 를 분리해 그렸다** — `Fig. S11` 에서 문헌 벌크 Li₂S 는 **Cal. figure-read ≈0.45 eV / Exp. ≈0.74 eV** 이고, 자기 값 0.22 eV 는 **따로 "Li₂S layer — Present work"** 막대다. ⇒ **0.22 eV 는 애초에 벌크 Li₂S 물성으로 제시된 적이 없다.**
2. 그 벌크 Li₂S 계산의 출처는 SI ref [27] = **Moradabadi & Kaghazchi, *Appl. Phys. Lett.* 2016, 108, 213906, "Thermodynamics and kinetics of defects in Li₂S"** — **우리 `v2/li2s` 0.305 eV 가 겨눠야 할 진짜 문헌 짝이 이것이다** (Lai 의 0.22 가 아니다).
3. 본문이 *왜* 벌크가 아니라 층을 계산했는지 스스로 밝힌다: *"Though **bulk Li₂S shows low Li ion conductivity** at room temperature,[53] the **nanoscale Li₂S SEI exhibits high Li ion conductivity**.[54] **For these reasons**, DFT calculations were performed…"* ⇒ 벌크와 층이 다른 값이라는 걸 **알고** 층을 골랐다.
4. **0.67 : 0.22 의 3배 대비는 장벽 정의에 의존한다** (§10-①). 그림에서 읽으면 LiF 는 *"경로 최대점 − 직전 극소"* 로 0.67 이지만, *"최대점 − 초기상태"* 로 재면 **≈0.43 eV** 다. Li₂S 는 두 정의가 같은 값(극소가 전부 0)이라 **LiF 쪽만 늘어난다** ⇒ 대비가 3.0× → 2.0× 로 줄어든다.

---

## 1. 한 줄 요약

PVDF–LiTFSI 고분자 전해질에 **비정질 3Li₂S·2P₂S₅(LPS)** 를 채워 넣으면(SLCSE), 순환 중 Li 금속 표면에 **LiF 대신 Li₂S 가 in-situ 로 깔리고**(SMIL), 그 결과 (i) PVDF 의 탈불소화(분해)가 억제되고 (ii) 젖음성이 좋아져 Li 도금이 균일해진다 — 라는 것이 주장이다. 뒷받침으로 **CI-NEB 로 "Li 가 층을 통과하는" 장벽을 LiF 0.67 eV vs Li₂S 0.22 eV** 로 계산하고, **Li|Li₂S 계면 형성에너지가 Li|LiF 보다 4–5배 더 음수**(−0.29~−0.44 vs −0.078~−0.096 J/m²)임을 보인다. 성적은 σ **3.42 × 10⁻⁴ S/cm**, t_Li⁺ **0.44**, Li‖SLCSE‖LiFePO₄ 풀셀 **153 mAh/g @0.05 mA/cm²** · **150 cyc 99.5 %**(20 cyc 기준).

---

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 저널/년 | ***Nano Lett.* 2020**, 20(11), 8273−8281 (Letter) · DOI `10.1021/acs.nanolett.0c03395` |
| 접수/개정/게재 | Received **2020-08-20** · Revised **2020-10-19** · Published **2020-10-27** |
| 소속 | ¹西安交通大学 화공학원 · ²**NUS** 화학생물분자공학 · ³**北京航空航天大学 재료** (= Naihua Miao, **계산 담당 교신**) · ⁴上海空间电源研究所 · ⁵**IMRE A\*STAR** 싱가포르 · ⁶NUS Graduate School |
| 분량 | 본문 **9 pp**(Fig 1–5 + Table 1, refs 58) · SI **22 pp**(Fig S1–S13 + Table S1, refs 28) |
| 연구유형 | **exp 주 + DFT 보조** — DFT 는 본문 1개 문단(§5.6)과 SI 방법 1쪽이 전부 |
| 계 | `Li ‖ (S)LCSE ‖ LiFePO₄` 풀셀 · `Li‖SE‖Li` 대칭셀 · `Li‖SE‖Cu` 반대칭셀 · `SS‖SE‖SS` |
| **계보** | **[Liu24SbO]**(`papers/liu2024_pband_center_sbo_dual_interface.md`) 의 **ref [30b] 원출처**. Liu 2024 는 자기 LiSbS₂ 관통장벽 0.23 eV 를 *"Li₂S layer (0.22 eV) 와 비슷하고 LiF layer (0.67 eV) 보다 훨씬 낮다"* 로 위치시킬 때 **이 논문을 끌어왔다** |

**동기**: CSE(composite solid electrolyte) 의 두 병목 — ① 덴드라이트는 CSE 의 무른 상(soft phase)·기공·입계를 타고 뚫고 들어온다 ② **PVDF 가 Li 금속과 만나 탈불소화(dehydrofluorination)** 되면서 전자를 흘려 Li⁺ 를 국소 환원 → 불균일 도금 가속. 저자들의 답 = *"기계적 강도로 덴드라이트를 억누르는 대신, Li 금속 위에 **잘 통하고 잘 젖는 SEI 를 in-situ 로 깔자**"* — 그 SEI 를 **LiF 가 아니라 Li₂S** 로 만든다.

---

## 3. 핵심 물성 (수치 총정리)

### 3.1 전해질 자체

| 물성 | **LCSE** (LiTFSI–PVDF) | **SLCSE** (+LPS) | 출처 |
|---|---|---|---|
| 두께 | — | **≈40 μm** | `Fig. 1c` 단면 SEM |
| σ_ion (25 °C) | **2.40 × 10⁻⁴ S/cm** | **3.42 × 10⁻⁴ S/cm** (**1.43×**) | 본문 · `Fig. S4` 등가회로 fit |
| **t_Li⁺** | **0.16** | **0.44** (**2.75×**) | 본문 · `Fig. 1d` (Bruce–Vincent, ΔV = 10 mV) |
| 크로노암페로메트리 I₀ → I_s | 12.2 → **6.0 μA** | 22.5 → **14.2 μA** | `Fig. 1d` |
| R₀ (Ohmic, 등가회로) | 16.64 Ω | **11.69 Ω** | `Table S1` |
| R₁ (계면) / C | 2.42 Ω / 8.01×10⁻⁸ F | **2.28 Ω** / 7.03×10⁻⁸ F | `Table S1` |
| L / CPE_T / CPE_P | 6.93×10⁻⁷ / 3.30×10⁻⁶ / 0.90 | 7.39×10⁻⁷ / 2.34×10⁻⁶ / **0.92** | `Table S1` |

### 3.2 대칭셀 / 도금

| 지표 | LCSE | SLCSE | 출처 |
|---|---|---|---|
| 분극전압 (0.04 mA/cm², 1 h/1 h) | **≈35 mV** | **≈15 mV** | 본문 · `Fig. 2a` (figure-read 반진폭 ≈0.035 / ≈0.013 V — 일치) |
| 200 h → 1000 h 분극 증가 | ≈8 mV | **≈4 mV** ("약 절반") | 본문 · `Fig. 2a` figure-read 확인 |
| 0.50 mA/cm² 과전압 | 본문 *"2배"* · **figure-read ≈±0.45 V** | **figure-read ≈±0.17 V** | `Fig. 2b` — figure-read 비 ≈**2.6×** (본문 "2배"보다 큼) |
| 핵생성 과전압 (tip−flat, on Cu) | **figure-read ≈0.08 V** (tip ≈−0.195, flat ≈−0.115 V) | **figure-read ≈0.023 V** (tip ≈−0.065, flat ≈−0.042 V) | `Fig. 2c` |
| 10 cyc 후 Li 표면 | 거칠고 균열 + **dead Li/SEI**(파란 원) | 미세하고 균일 | `Fig. 2e` / `Fig. 2f` |

### 3.3 풀셀 (Li‖SE‖LiFePO₄, 25 °C, 2.5–3.8 V, 로딩 2.0–2.5 mg/cm²)

| 지표 | LCSE | SLCSE |
|---|---|---|
| rate 0.05 / 0.10 / 0.25 / 0.50 mA cm⁻² | **138 / 123 / 102 / 47** mAh/g | **153 / 144 / 131 / 101** mAh/g |
| 수명 @0.05 mA/cm² | **95번째 cyc 에서 failed** | **>150 cyc**, 용량유지 **99.5 %** (20 cyc 기준) |
| 50th/80th 분극 (plateau gap) | figure-read **≈0.12 V** | figure-read **≈0.09 V** |

### 3.4 XPS 앵커 (우리 `xps_reference_sei.csv` 와 대조 가능)

| 종 | BE (eV) | 어디 |
|---|---|---|
| P 2p — **PS₄³⁻** | **134.0 / 134.8** | `Fig. 1e-1` 원시 SLCSE |
| S 2p — **Li₂S** | **162.2** (원시 SLCSE) · **162.3 / 163.5** (순환 후 Li-SLCSE) | `Fig. 1e-2` · `Fig. 3c-2` |
| S 2p — PS₄³⁻ | **163.8** | `Fig. 1e-2` |
| S 2p — **S=O** (TFSI⁻) | **169.5** (원시) · **169.4 / 170.5** (순환 후) | `Fig. 1e-2` · `Fig. 3c` |
| S 2p — **S–O–Li** (리튬화된 TFSI) | **167.3 / 168.5** | `Fig. 3c` |
| F 1s — **LiF** | **684.9** | `Fig. 3a-1` (Li-LCSE) · `Fig. 3b-2` (순환 후 LCSE) |
| F 1s — –CF₂ / –CF₃ | **687.8 / 688.9** | `Fig. 3a`, `Fig. 3b` |

### 3.5 ★ 계산값 (이 논문이 직접 계산한 것)

| 양 | 값 | 어디 |
|---|---|---|
| **CI-NEB: Li 가 LiF 층을 통과** | **0.67 eV** (본문 인쇄) | `Fig. 3e` · `Fig. S11` "LiF layer, Present work" |
| **CI-NEB: Li 가 Li₂S 층을 통과** | **0.22 eV** (본문 인쇄) | `Fig. 3f` · `Fig. S11` "Li₂S layer, Present work" |
| 표면 형성에너지 Li(100)/(110)/(211) | **0.47 / 0.50 / 0.55 J m⁻²** | `Table 1` |
| 계면 형성에너지 Li(hkl)\|**LiF** | **−0.084 / −0.078 / −0.096 J m⁻²** | `Table 1` |
| 계면 형성에너지 Li(hkl)\|**Li₂S** | **−0.39 / −0.29 / −0.44 J m⁻²** | `Table 1` |

**⇒ 계산 결론 두 줄**: (i) Li 는 **Li₂S 층을 LiF 층보다 3배 쉽게 통과**한다 (ii) **Li|Li₂S 계면이 Li|LiF 보다 4–5배 더 강하게 자발형성**된다 ⇒ Li₂S 가 젖음성도 좋고 덴드라이트 관통 저항도 크다.

### 3.6 ★★ `Fig. S11` — 논문 자신이 그린 문헌 대조표 (**전부 figure-read**)

> 캡션 원문: *"Figure S11 The migration energy barrier of Li ionic conductor obtained by DFT calculation and experiments [15-28]"*
> 막대는 주황(Cal.) 위에 파랑(Exp.) 이 얹힌 형태 — **파랑 꼭대기 = 실험값**으로 읽었다 (겹쳐그리기 해석; 저자가 축약 규칙을 적지 않아 **누적합 해석 가능성도 배제 못 한다**).

| 계 | Cal. (figure-read) | Exp. (figure-read) | SI ref |
|---|---|---|---|
| Li₃OCl | ≈0.37 | ≈0.59 | [15] Zhang PRB 2013 · [16] Lv Adv. Sci. 2016 |
| LiTi₂(PO₄)₃ | ≈0.245 | ≈0.47 | [17] Lu Nano Energy 2017 · [18] Chang JACerS 2005 |
| Li₁₀GeP₂S₁₂ | ≈0.14 | ≈0.25 | [19] Du JPCC 2014 · [20] Kamaya Nat. Mater. 2011 |
| Li₇P₃S₁₁ | ≈0.24 | ≈0.39 | [21] Xiong CMS 2014 · [22] Seino EES 2014 |
| Li₃PS₄ | ≈0.20 | ≈0.36 | [23] Lepley PRB 2013 · [24] Liu JACS 2013 |
| **LiF (벌크, 문헌)** | **≈0.73** | **≈0.85** | [25] **Chen, Ouyang, Song, Sun, *JPCC* 2011, 115, 7044** · [26] Li/Maier *AFM* 2011 |
| **LiF layer** | **≈0.67** | — | **Present work** |
| **Li₂S (벌크, 문헌)** | **≈0.45** | **≈0.74** | [27] **Moradabadi & Kaghazchi, *APL* 2016, 108, 213906** · [28] Lin/Dudney/Liang *ACS Nano* 2013 |
| **Li₂S layer** | **≈0.22** | — | **Present work** |

빨간 점선이 y ≈ 0.22 에 그어져 있어 자기 값을 전 계열에 겹쳐 보여 준다.

---

## 4. 재료 & 방법 (실험, SI 전문 요약)

- **LPS 합성 (용액법)**: `138 mg Li₂S`(3.00 mmol) + `444.5 mg P₂S₅`(2.00 mmol) → **3:2 몰비 = 3Li₂S·2P₂S₅ ✔** 를 `4 g THF` 에 완전용해까지 교반 → **80 °C 12 h + 160 °C 4 h** 용매 제거 → 마노유발 30 min 분쇄. 전 공정 Ar 글로브박스 (O₂·H₂O < 0.1 ppm).
- **SLCSE**: `100 mg LPS + 120 mg LiTFSI + 180 mg PVDF` (= **25 : 30 : 45 wt%**) in `1.90 g NMP`, RT **100 h** 교반(Ar) → **300 μm 닥터블레이드** → Ar 자연건조 **8 h** → Ø12 mm 펀칭. 최종 **≈40 μm**.
- **LCSE**: LPS 만 뺀 동일 공정, 단 **건조 4 h** (⚠ 두 시료의 건조시간이 다르다 — §10-⑤).
- **LiFePO₄ 양극**: `280 LFP : 40 acetylene black : 40 LiTFSI : 40 PVDF` (= **70:10:10:10 wt%**), DMF 슬러리, Al 박 위 300 μm, 80 °C 진공 하룻밤. 로딩 **2.0–2.5 mg/cm²**.
- **분석**: XRD Bruker D8 Advance (Cu Kα λ = 1.54056 Å) · SEM JEOL JSM-6700F · **XPS Kratos AXIS Ultra DLD, Al Kα hν = 1486.71 eV, < 1×10⁻⁸ torr**.
- **전기화학**: NEWARE, **2.5–3.8 V** 정전류 · EIS Autolab PGSTAT204A, **1 MHz–10 Hz**, 진폭 10 mV · t_Li⁺ 는 Bruce–Vincent 식 (SI eq 1) `t = I_s(ΔV − I₀R_i₀)/[I₀(ΔV − I_sR_is)]` 형태 — **분극 전/후 Nyquist 로 R_b·R_i 를 각각 취함**.

---

## 5. 결과 — 섹션별 상세

### 5.1 LPS 와 필름 (Fig. 1a–c, Fig. S1–S3)
용액법 LPS 는 수십~수백 nm 입자(`Fig. S1`), XRD 상 **주로 비정질 + 미량 Li₃PS₄·Li₂S 결정상**(`Fig. S2`). SLCSE 필름은 유연하고(`Fig. 1b`) 단면 **≈40 μm**(`Fig. 1c`), 표면이 LCSE 보다 평탄해(`Fig. S3`) Li 금속과 밀착하기 좋다고 주장.

### 5.2 전도·수송 (Fig. 1d, Fig. S4, Table S1)
`Fig. 1d` 크로노암페로메트리(10 mV): SLCSE 22.5 → 14.2 μA, LCSE 12.2 → 6.0 μA. **t_Li⁺ 0.44 vs 0.16.** 삽입 Nyquist 는 분극 전/후 모두 SLCSE 가 더 작은 반원(Z′ ≲ 800 Ω 스케일). σ 는 SS‖CSE‖SS 로 2.40 → **3.42 × 10⁻⁴ S/cm**. 저자 해석: LPS 가 **세라믹|고분자 계면과 세라믹 내부** 두 경로를 추가로 열어 t_Li⁺·σ 를 동시에 올린다 (refs 37–39).

### 5.3 원시 SLCSE 의 화학종 (Fig. 1e)
LPS 가 비정질이라 XPS 로 종을 정한다. **P 2p 는 PS₄³⁻ 이중선(134.0/134.8) 하나뿐** ⇒ 인은 전부 PS₄ 형태. **S 2p 는 세 성분** — Li₂S(162.2) · PS₄³⁻(163.8) · S=O(169.5, TFSI⁻ 유래). ⇒ *"LPS 는 주로 비정질 **Li₂S + Li₃PS₄**"*. (figure-read: Li₂S 성분의 면적은 작다 — 미량이다.)

### 5.4 대칭셀·도금 거동 (Fig. 2)
- `Fig. 2a` 1000 h @0.04 mA cm⁻²: SLCSE 는 좁고 평평한 밴드(≈±0.013 V), LCSE 는 넓고 서서히 벌어지는 밴드(≈±0.035 → ±0.041 V). 190–210 / 490–510 / 980–1000 h 확대 삽도 3개.
- `Fig. 2b` rate 사다리 **0.05 → 0.10 → 0.20 → 0.50 → 0.05 mA cm⁻²** (⚠ 대칭셀은 0.20, 풀셀은 0.25 — 사다리가 다르다). 0.50 에서 LCSE 가 크게 벌어진다.
- `Fig. 2c` Cu 위 첫 도금: **tip potential**(핵생성) 과 **flat potential**(확산지배) 을 라벨로 분리. LCSE 는 둘 다 훨씬 깊다 ⇒ 젖음성 나쁨.
- `Fig. 2d–f` SEM: 원시 Li(평탄, 미세 피트) → LCSE 10 cyc 후 **거칠고 dead Li/SEI**(파란 원) → SLCSE 10 cyc 후 **균일 미세**. `Fig. S6` 는 풀셀(0.50 mA cm⁻²)에서 같은 대비.

### 5.5 계면층의 정체 — XPS/CV (Fig. 3a–d, Fig. S7–S10)
논증이 4단이다.
1. **`Fig. 3a`** — 순환 후 Li 표면: Li-LCSE 에는 **LiF(684.9) 가 있고**, Li-SLCSE 에는 **LiF 가 없다**.
2. **`Fig. 3b`** — 그 LiF 의 F 는 어디서 왔나? 원시 LCSE vs 20 cyc LCSE 에서 **–CF₂ 상대강도가 크게 변한다** ⇒ **PVDF 분해가 주범**(LiTFSI 아님). `Fig. S7` 은 SLCSE 의 –CF₂/–CF₃ 비가 거의 안 변함을 보여 **탈불소화 억제**를 뒷받침.
3. **`Fig. 3c`** — Li-SLCSE 에만 **162.3/163.5 eV = in-situ Li₂S** 이중선이 새로 뜬다. 그리고 **PS₄³⁻ 의 S 2p 는 Li-SLCSE 표면에 없다** ⇒ 표면층은 SLCSE 자체가 아니라 **SEI**. `Fig. S8`(S 2p 비교)·`Fig. S9`(P 2p, PS₄³⁻ 안정)·`Fig. S10`(Li 1s) 로 교차.
4. **`Fig. 3d`** — CV 1st–4th. SLCSE 셀에만 **≈2.75 V 부근 추가 산화·환원 쌍**이 나타나고, 이를 **SMIL 형성 반응**으로 귀속. ⇒ Li₂S 는 (a) SLCSE 로부터의 화학확산 + (b) 전기화학 반응 **둘 다**로 생긴다 (ref 48).
   ⚠ 본문 문장이 *"…in the CV curves of the **Li‖LCSE‖LiFePO₄** cell (Figure 3d-2)"* 라고 적었는데 `Fig. 3d-2` 는 **SLCSE** 패널이다 — **본문 오기**(§10-④).

### 5.6 ★★ DFT — 이 논문의 계산 문단 (본문 p.8278 좌단)
> **원문 그대로**: *"Though bulk Li₂S shows low Li ion conductivity at room temperature,⁵³ the nanoscale Li₂S SEI exhibits high Li ion conductivity.⁵⁴ For these reasons, density functional theory (DFT) calculations were performed to understand the migration behavior of Li when passing through LiF and Li₂S layers. As illustrated in **Figure 3e and 3f**, the calculated migration energy barrier of Li ions passing through **LiF layer is 0.67 eV**, while it is **0.22 eV for that in Li₂S layer**. Obviously, this means that the Li ion conductivity of SMIL is much higher than that of FMIL… The migration energy barriers of Li in Li ionic conductors reported by DFT calculations and experiments are collected in **Figure S11**. It can be seen that the calculated migration energy barrier of Li in the Li₂S layer (0.22 eV) is close to that previously reported of Li in bulk **β-Li₃PS₄ (∼0.20 eV)** and **Li₇P₃S₁₁ (0.24 eV)**,⁵⁵'⁵⁶ verifying the high Li ion conductivity of the Li₂S layer."*

즉 **0.22 eV 는 이 논문이 계산했고, 그 값을 "β-Li₃PS₄·Li₇P₃S₁₁ 만큼 빠르다"는 문헌 두 편에 맞대어 정당화**한다. (ref [55] Lepley PRB 2013 · [56] Xiong CMS 2014.)

### 5.7 표면·계면 형성에너지 (Fig. 4, Table 1)
`Fig. 4` 는 **Li(100)/(110)/(211) 위에 LiF(200)** (a–c) 과 **Li₂S(111)** (d–f) 을 얹은 6개 계면 모델. figure-read: Li 금속 기판은 **5–6 원자층**, LiF 층은 **약 2 (200) 면**, Li₂S 층은 **매우 얇다(대략 한 겹 삼중층)**. 분홍 점선이 계면을 표시.
- Li 표면 γ 가 전부 **양수** (0.47–0.55 J m⁻²) ⇒ 새 표면을 만들려면 에너지가 든다. **γ 가 낮은 면에 Li 이 자란다** ⇒ 원시 Li 위 덴드라이트 성장 (ref 58).
- **Li|LiF·Li|Li₂S 계면 γ 는 전부 음수** ⇒ LiF·Li₂S 가 존재하면 계면은 **자발 형성**.
- **Li|Li₂S 가 훨씬 더 음수** (−0.29 ~ −0.44 vs −0.078 ~ −0.096) ⇒ 둘이 동시에 있으면 **Li|Li₂S 가 우선 형성**되고, 젖음성이 더 좋고, 덴드라이트가 뚫으려면 더 큰 에너지를 이겨야 한다.
- 저자 자체검증: Li 표면 γ 0.47/0.50/0.55 가 ref 57(Zhang, *Mater. Today* 2020) 과 가까워 *"indicating the reliability of our calculation method"*.

### 5.8 풀셀 (Fig. 5, Fig. S12–S13)
`Fig. 5a` — LCSE 는 **≈97 cyc 에서 급락("failed")**, SLCSE 는 150 cyc 까지 완만(figure-read 20 cyc ≈149 → 150 cyc ≈148 mAh/g). `Fig. 5b` 50th/80th 프로파일에서 SLCSE 의 plateau 간극이 좁다. `Fig. 5c,d` rate. `Fig. S12` — 순환에 따른 계면저항: **SLCSE 는 100 cyc 후 크게 감소**(SMIL 형성), LCSE 는 50 cyc 에 감소했다가 100 cyc 에 **다시 증가**(PVDF 분해). `Fig. S13` 단면 SEM 은 SLCSE|Li 접촉이 더 밀착.

---

## 6. ★★ DFT / 계산 방법 — 전수 확인 (1저자 질의 (B))

### 6.1 SI "DFT calculation methods" 전문 (SI p.4–5) — **본문에는 계산 방법 절이 아예 없다**

> *"Density functional theory (DFT) calculations were performed using the **Vienna ab initio Simulation Package (VASP)** code based on the **pseudopotential and plane wave** methods.⁷ The exchange correlation energy was described by **generalized gradient approximation (GGA)** with **Perdew-Burke-Ernzerhof (PBE)** parametrization. The **cutoff energy for the planewave basis set was set at 520 eV** and a **k-point density of 4/Å** was adopted.¹⁰ The convergence criteria for total energy and ionic force were **10⁻⁵ eV** and **10⁻² eV/Å**, respectively. **The thickness of the vacuum layer was set as 20 Å.**"*
> …
> *"The migration barrier energies of Li passing through LiF and Li₂S layers are calculated by using the **climbing-image under elastic band (CI-NEB) method**.¹² The calculations will be finished when the **total energy difference is no higher than 1.0 × 10⁻⁵ eV for per atom** and **maximum forces on each atom are within 0.05 eV/Å**. The value of the migration energy barrier can be obtained by following equation: **E_m = E_h − E_i, (h > i)** of which the E_m is the migration energy barrier determined by the **maximum value of difference between E_h and E_i**. E_h and E_i are the relative energies of transition states (h>i) referring to the **initial state (seen as reference state with 0 eV in total energy)**."*

수식 두 개도 SI 에 있다:
- 표면에너지 `γ_se = ΔE / (2S)` (ref 11 Fu, *Appl. Surf. Sci.* 2010)
- 계면 형성에너지 `γ_ie = [E_Li|cl − (E_Li + E_cl)] / S`

관련 인용: ref [7] Kresse & Joubert PAW 1999 · [8] PBE 1996 · [10] Monkhorst–Pack 1976 · **[12] Henkelman, *J. Chem. Phys.* 2000, 113, 9901 — 정확한 CI-NEB 원전**.

### 6.2 문자열 전수 카운트 (`pdftotext -layout` 기준)

| 문자열 | 본문 (9 pp) | SI (22 pp) |
|---|---|---|
| `NEB` | **0** | **1** (본문 방법절 `(CI-NEB) method`) |
| `nudged` | 0 | **1** (ref 12 제목 안에서만) |
| `elastic band` | 0 | **2** (방법절 1 + ref 12 제목 1) |
| `climbing` | 0 | **2** (방법절 1 + ref 12 제목 1) |
| `CI-NEB` | 0 | **1** |
| `VASP` / `PBE` / `GGA` | **0 / 0 / 0** | 1 / 1 / 2 |
| `cutoff` / `k-point` / `pseudopotential` | 0 / 0 / 0 | 1 / 1 / 2 |
| `Computational` (절 제목) | **0** | **0** — 절 제목은 `DFT calculation methods:` |
| `migration` | 9 | 4 |
| `energy barrier` | 5 | 3 |
| **`0.67`** | **1** (p.8278) | **0** (그림 라벨로만) |
| **`0.22`** | **2** (p.8278 ×2) | **0** (그림 라벨로만) |

⇒ **계산 방법 절은 SI 에만 있고, 실체가 있다.** "인용문 한 줄만 있고 계산 절이 없는" 경우가 **아니다**.

### 6.3 ★ NEB 전수 표 (Liu 2024 digest §6.4 와 같은 양식)

| # | 계 | 값 | 출처 | 경로 (어디→어디) | 셀 / 슈퍼셀 | 이미지 수 | CI | 전하 규약 | code/범함수/컷오프 | 수렴 임계 |
|---|---|---|---|---|---|---|---|---|---|---|
| **L1** | **LiF 층 관통** | **0.67 eV**(정방향)<br>figure-read 역방향 ≈**0.83 eV** | **이 논문 자체 계산** (`Fig. 3e`) | 여분 Li 한 개가 얇은 **LiF 슬랩의 윗면 → 아랫면**. **6단 다중홉**, 중간 극소 2개(RC2 ≈−0.24, RC4 ≈−0.40 eV). RC4 부근에서 **격자 Li 한 개가 슬랩 아래로 밀려난다**(figure-read) — 단순 홉이 아니라 **국소 재배열 동반** | **명시 없음.** 진공 20 Å ⇒ 슬랩. figure-read: LiF **≈2 (200) 면 두께**, 인셋 원자 수 ~20개 | **명시 없음** — `Fig. 3e` 의 "Cal." 마커 **figure-read 7개**(RC 0–6, 끝점 포함) | SI 에 `CI-NEB` 명시 ✔ (단 *"climbing-image under elastic band"* 로 오기) | ⛔ **명시 없음.** NELECT·배경전하·jellium·공공/침입형 어느 것도 한 줄 없다. figure-read 로는 **여분 Li 원자 1개 = 침입형**, 기본값이면 **중성 셀** | VASP / PAW / **GGA-PBE** / **520 eV** / k-density **4/Å** | 전자 1e−5 eV; **NEB 힘 0.05 eV/Å** (일반 이완 0.01 eV/Å 보다 **5배 느슨**) |
| **L2** | **Li₂S 층 관통** | **0.22 eV** (양방향 대칭, figure-read 역방향도 ≈0.215) | **이 논문 자체 계산** (`Fig. 3f`) | 여분 Li 한 개가 **Li₂S 슬랩의 윗면 → 아랫면**. **6단 다중홉**, 중간 극소가 **전부 0 eV 근처**(RC0=RC3=RC6≈0) = 사실상 **주기적 관통 경로** | **명시 없음.** figure-read: Li₂S 슬랩이 **매우 얇다**(대략 한 겹 삼중층), 인셋 원자 수 ~20개 | **명시 없음** — figure-read **7개** | 〃 | ⛔ **명시 없음** (동일) | 〃 | 〃 |

**`Fig. 3e` figure-read 좌표** (Energy eV vs Reaction Coordinate 0–6):
`0.00 → +0.08 → −0.24 → +0.43 → −0.40 → +0.13 → +0.01`
자홍색 화살표가 **RC2 점선(−0.24) → RC3 점선(+0.43)** 을 잇는다 ⇒ **0.67 = E(3) − E(2) = 경로상 최대 상승단**.

**`Fig. 3f` figure-read 좌표**:
`0.00 → +0.13 → +0.18 → ≈0.00 → +0.155 → +0.215 → 0.00`
화살표가 **RC5 점선(≈0.215) ↔ RC6 점선(0.00)** 사이. 극소가 전부 0 이라 **0.22 = 최대점 − 극소 = 최대점 − 초기상태** (두 정의가 일치).

**⇒ 이것이 §10-① 의 핵심**: `E_m = max(E_h − E_i)` 정의는 **LiF 에서만** 값을 부풀린다.
- "최대점 − 초기상태" 로 재면: LiF **≈0.43**, Li₂S **0.22** ⇒ 대비 **3.0× → 2.0×**
- 역방향(6→0)으로 재면: LiF **≈0.83**(=E(3)−E(4)), Li₂S **≈0.215** ⇒ 대비 **3.9×**
논문은 이 방향 의존성을 언급하지 않는다.

### 6.4 그림 인셋이 말해 주는 것 (본문·SI 에 글로는 없는 것) — 전부 `figure-read`

- **NEB 셀에 Li 금속 기판이 없다.** `Fig. 4` 에서는 Li 금속을 파란 구로 명확히 그렸는데, `Fig. 3e/3f` 인셋에는 **기판이 없다** ⇒ NEB 는 **자립(free-standing) 슬랩**에서 돌린 것으로 보인다. ⚠ 본문·SI 에 명시가 없어 **추정**이다 — 이 점을 인용할 때 반드시 붙일 것.
- **이동종은 여분의 Li 원자 1개**다 (LiF 는 빨간 구, Li₂S 는 파란 구로 표시). **공공(vacancy) 이 아니다.**
- LiF 색: 자홍 = F, 초록 = Li. Li₂S 색: 주황 = S, 노랑 = Li. (`Fig. 4` 와 같은 팔레트.)
- `Fig. 3f` 의 RC3 확대원(돋보기)은 이동 Li 이 격자 S·Li 과 맞닿은 중간 극소 배치를 보여 준다.
- **본문은 "Li **ions**"(이온), SI 는 "**Li** passing through"(원자) 로 표현이 갈린다** — 하전 규약이 없으니 어느 쪽인지 문헌만으로는 정할 수 없다.

### 6.5 명시 없음 목록 (전수 grep 확인 — 추정 금지 항목)

`supercell` · 원자 수 · NEB 이미지 수 · **전하 상태 / NELECT / 배경전하 / jellium** · **공공 vs 침입형** · 슬랩 두께 / 층 수 · NEB 셀의 표면 지수 · 고정층(frozen layer) 여부 · **Monkhorst–Pack 메시 실수치**(오직 *"k-point density of 4/Å"*) · 스핀편극 · smearing · dipole correction · NEB 전용 k-mesh · NEB 구현체(VTST 등) · 이동 Li 의 출처 · **DFT-D/vdW 보정** — **전부 논문에 없다.**

---

## 7. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1a–c | 닥터블레이드 공정도 · 필름 실물 · 단면 SEM 40 μm | CSE 필름 규격. 우리 축과 직접 관계 없음 |
| **1d** | 크로노암페로메트리(10 mV) + Nyquist 삽도, **t_Li⁺ 0.16 → 0.44** | **Bruce–Vincent 표기의 표준 포맷**. 분극 전/후 Nyquist 를 같이 실은 점이 좋다 |
| **1e** | 원시 SLCSE **P 2p / S 2p** 디컨볼루션 | ★ **우리 XPS 앵커 대조군**: PS₄³⁻ 134.0/134.8 · Li₂S **162.2** · S=O 169.5 eV |
| 2a | 대칭셀 1000 h @0.04 mA cm⁻² + 확대 삽도 3개 | figure-read 반진폭이 본문 15/35 mV 와 **일치** — 드물게 정직한 그림 |
| 2b | rate 사다리 0.05→0.50 mA cm⁻² | 본문 *"2배"* ↔ figure-read **≈2.6×** (§10-②) |
| **2c** | Cu 위 첫 도금: **tip / flat potential 분리 라벨** | ★ **핵생성 과전압을 확산지배 평탄부와 분리해 읽는 법** — 우리가 Li 젖음성 서술할 때 그대로 쓸 수 있는 어휘 |
| 2d–f | 원시 Li / LCSE 10 cyc / SLCSE 10 cyc SEM | dead Li·SEI 를 원으로 표시하는 관례. **정량 없음** |
| **3a,b** | F 1s — Li 표면의 LiF 유무 + **PVDF vs LiTFSI 어느 쪽이 F 원인인가** | ★ **"분해 주범 특정" 논증 포맷**: 전해질 쪽 –CF₂ 상대강도 변화로 고분자 분해를 지목 |
| **3c** | S 2p — Li-SLCSE 에만 **in-situ Li₂S (162.3/163.5)**, PS₄³⁻ 부재 | ★ *"표면층은 SE 가 아니라 SEI 다"* 를 **음이온 종의 부재**로 증명하는 논법 |
| 3d | CV 1st–4th, **≈2.75 V 추가 산화환원 쌍 = SMIL 형성** | ⚠ 본문이 패널을 **LCSE 로 오기**(§10-④). 값은 그림에서만 |
| **3e** | ★★ **CI-NEB — Li 가 LiF 층 관통, 0.67 eV** | ★★ §6.3 · §11. **7점 다중홉 · 중간 극소 −0.40 eV · 정의 의존성**을 반드시 같이 인용 |
| **3f** | ★★ **CI-NEB — Li 가 Li₂S 층 관통, 0.22 eV** | ★★ **1저자 질문의 답이 여기 있다.** 벌크 홉이 아니라 **얇은 슬랩 관통** — 우리 0.305 와 다른 양 |
| **4a–f** | **Li(100)/(110)/(211) \| LiF(200)** 및 **\| Li₂S(111)** 계면 최적화 구조 | ★ 우리 `interface_reactivity` 슬랩 모델의 외부 대조. figure-read: **Li 기판 5–6층, LiF 2면, Li₂S 극히 얇음** ⇒ 슬랩 수렴 미검증 |
| **Table 1** | 표면 γ (0.47/0.50/0.55) + 계면 γ (Li\|LiF −0.078~−0.096 / Li\|Li₂S −0.29~−0.44 J m⁻²) | ★ **SEI 상 선택성을 "계면 형성에너지 부호·크기" 로 말하는 틀**. 우리 `sei_formation_voltage` 와 **다른 양**이니 섞지 말 것 |
| 5a–d | 풀셀 사이클(LCSE 97 cyc 실패) · 50/80th 프로파일 · rate · rate 프로파일 | figure-read 0.10 mA cm⁻² SLCSE **≈150** vs 본문 **144** (§10-③) |
| S1–S3 | LPS 분쇄 전/후 형상 · XRD · 필름 표면/단면 | LPS 가 비정질 + 미량 Li₃PS₄/Li₂S |
| S4 / Table S1 | EIS 실측·fit + 등가회로 성분값 | R₀·R₁·CPE 표기 관례 |
| S5–S10 | 누적 용량손실 · 풀셀 후 Li SEM · F1s/S2p/P2p/Li1s XPS | `Fig. S9` = PS₄³⁻ 가 순환 후에도 SLCSE 안에 남는다(안정) |
| **S11** | ★★ **문헌 장벽 9개 막대 비교 — "Li₂S"(벌크) vs "Li₂S layer"(자기값) 분리** | ★★★ **이 digest 의 최대 수확** (§3.6 · §11). **벌크 Li₂S Cal. ≈0.45 eV** 가 우리 0.305 의 진짜 문헌 짝 후보 |
| S12 | 순환수별 대칭셀 EIS | SLCSE 는 100 cyc 후 계면저항 ↓, LCSE 는 50 → 100 cyc 에 ↑ |
| S13 | SLCSE\|Li · LCSE\|Li 단면 SEM | 밀착도 대비 (정량 없음) |

**내가 실제로 본 그림 / 안 본 그림 (정직 목록)**
- 🔍 **고해상 실물 판독(확대 포함)**: `Fig. 3` 전체 + **`3e`·`3f` 를 zoom 9× 로 따로 렌더해 마커 좌표까지 판독** + `3f` 인셋을 zoom 22–24× 로 재렌더(슬랩 두께·이동종 색 확인) · `Fig. 4` 전체 · **`Fig. S11`**(자동 크로핑이 놓쳐 손으로 렌더해 추가) · `Fig. 1` 전체 · `Fig. 2` 전체 · `Fig. 5` 전체.
- ⛔ **안 본 것**: SI `Fig. S1`·`S2`·`S4`(자동 크로핑됨, 열지 않음) 및 `S3`·`S5`–`S10`·`S12`·`S13`(크로핑 자체가 안 됨). 형상 SEM·XRD·반복 XPS·EIS 라 우리 축(NEB 검증)에 새 정보가 없다고 판단했다.
- 📄 **표(`tab_1.png`·`tab_S1.png`)는 이미지로 안 봤다** — PDF 텍스트가 더 정확해 그쪽에서 옮겼다.
- **본문 서술과 어긋난 그림 3건** → §10-②③④.

---

## 8. Post-processing ★

| 무엇 | 어떻게 | 수치화·기록 방식 |
|---|---|---|
| **CI-NEB** | VASP + CI-NEB (Henkelman 2000). **E_m = max(E_h − E_i), h>i, 초기상태 = 0 eV 기준** | `Fig. 3e/3f` 에 **"Cal." 산점 + "Fitted" 스플라인**을 겹쳐 그리고, 자홍 화살표로 E_m 을 표시. **표·수치목록은 없다** — 값은 본문 문장과 그림 라벨뿐 |
| **표면에너지** | `γ_se = ΔE/(2S)` (양면 절단) | `Table 1` 1열, J m⁻² |
| **계면 형성에너지** | `γ_ie = [E_Li\|cl − (E_Li + E_cl)]/S` (한 면) | `Table 1` 2·3열, J m⁻² |
| **구조 시각화** | 미기재 (VESTA/VMD 추정 — 논문에 도구명 없음) | `Fig. 4` 6패널 + `Fig. 3e/3f` 인셋 7개씩 |
| **문헌 벤치마크** | 문헌 DFT·실험 장벽 14편(SI ref 15–28) 을 자기 값과 한 막대그래프에 | `Fig. S11`, **누적/겹침 규칙 미기재** ⇒ 판독 모호 |
| **XPS 디컨볼루션** | Kratos AXIS Ultra DLD. 배경/피팅 함수·스핀궤도 분리 구속 **미기재** | Fig. 1e·3a–c·S7–S10 |
| ⛔ **하지 않은 것** | Bader/전하밀도차/DOS/COHP/ELF/AIMD/포논 **전부 없음**. 슬랩 두께·k-mesh·셀 수렴 시험 **없음**. **오차막대 0** | — |

---

## 9. 전체 논증 흐름

`PVDF 는 Li 금속과 만나면 탈불소화한다` → `그러면 표면에 LiF 가 깔린다(Fig. 3a,b)` → `LiF 는 Li 가 잘 못 지나간다(CI-NEB 0.67 eV, Fig. 3e)` + `Li|LiF 계면은 약하게만 자발형성된다(γ −0.08 J m⁻², Table 1)` → `⇒ 도금이 불균일해지고 덴드라이트가 난다(Fig. 2e)` ‖ `LPS 를 넣으면 표면에 Li₂S 가 깔린다(Fig. 3c, CV 2.75 V)` → `Li₂S 는 Li 가 잘 지나간다(0.22 eV, Fig. 3f)` + `Li|Li₂S 계면이 훨씬 강하게 자발형성된다(γ −0.29~−0.44)` → `⇒ 젖음성 ↑ · 균일 도금(Fig. 2f) · PVDF 분해 억제(Fig. 3a-2 에 LiF 없음)` → `⇒ 대칭셀 분극 15 mV · 풀셀 150 cyc 99.5 %`.

**논증의 약한 고리 두 개**:
① *"Li₂S 는 Li 가 잘 지나간다"* 의 근거가 **얇은 자립 슬랩 관통 장벽 하나**다. 논문 자신이 `Fig. S11` 에서 **벌크 Li₂S 는 Cal. ≈0.45 / Exp. ≈0.74 eV** 라고 그려 놓았다 — 즉 *"층이라서 빠르다"* 가 논지인데, **왜 층이면 빠른지**(두께·표면 완화·계면 배위)는 계산으로 분해되지 않는다.
② SEI 는 실제로 **Li₂S 단독이 아니다**. XPS 는 Li-SLCSE 표면에 **S=O(169.4/170.5) 와 S–O–Li(167.3/168.5) 도** 잡는다 — 즉 TFSI 분해물이 공존한다. 그런데 계산은 **순수 Li₂S 층**만 다룬다.

---

## 10. 주의 / 한계 (over-claim 방지) — 비판적으로

① **★★ 0.67 : 0.22 의 3배 대비는 장벽 정의에 의존한다.** SI 정의 `E_m = max(E_h − E_i), h>i` 는 *에너지 스팬(energy span)* 이라 다단 경로에서 정당한 선택이긴 하다. 하지만 `Fig. 3e` figure-read 로 보면 **LiF 경로에는 −0.24, −0.40 eV 의 깊은 중간 극소가 있고 Li₂S 경로에는 없다**. 그래서 같은 정의가 **LiF 만 부풀린다**: "최대점 − 초기상태" 기준이면 **0.43 vs 0.22 (2.0×)**, 역방향이면 **0.83 vs 0.215 (3.9×)**. **논문은 방향 의존성을 언급하지 않는다.** ⇒ *"LiF 가 Li₂S 보다 3배 어렵다"* 를 인용할 땐 **정의를 같이 적어야 한다**.

② **`Fig. 2b` — 본문 "2배" ↔ figure-read ≈2.6×.** 0.50 mA cm⁻² 에서 LCSE 과전압 ≈±0.45 V, SLCSE ≈±0.17 V. 보수적으로 반올림한 것이라 방향은 맞지만, 그림 쪽이 더 극적이다.

③ **`Fig. 5c` — 본문 SLCSE 0.10 mA cm⁻² 값 144 mAh/g ↔ figure-read ≈150.** LCSE 쪽 4개 값(138/124/103/47)은 figure-read 와 정확히 맞는다. SLCSE 0.10 만 어긋난다 (figure-read 정밀도 ±3 을 감안해도 경계).

④ **본문 오기 — CV 패널 지정.** *"an extra pair of reduction−oxidation peaks … were observed in the CV curves of the **Li‖LCSE‖LiFePO₄** cell (**Figure 3d-2**)"* — `Fig. 3d-2` 는 **SLCSE** 패널이고, 문맥(SMIL 형성) 상 SLCSE 가 맞다. 편집 오류.

⑤ **대조군 통제 결함 — 건조시간이 다르다.** SLCSE 는 Ar 건조 **8 h**, LCSE 는 **4 h**(SI 명시). 잔류 NMP 량이 다르면 σ·t_Li⁺·계면저항이 전부 달라진다. **LPS 의 효과와 건조도의 효과가 분리되지 않는다.**

⑥ **DFT 사양이 재현 불가 수준이다.** §6.5 목록 — **슈퍼셀·원자수·이미지 수·전하규약·슬랩 두께·k-mesh 실수치가 전부 없다.** 특히 **전하 규약 부재**는 절연체 NEB 에서 결정적이다: 중성 셀에 여분 Li 원자를 넣으면 전자가 전도대(또는 폴라론)로 들어가고, 이는 **하전 Li⁺ 이동과 다른 물리**다. 논문이 본문에서는 *"Li **ions**"*, SI 에서는 *"**Li** passing through"* 로 갈리는 것 자체가 이 모호함의 징후다.

⑦ **NEB 힘 임계가 일반 이완보다 느슨하다** (0.05 vs 0.01 eV/Å). 0.22 eV 수준 장벽에서 5배 느슨한 임계는 **수십 meV 오차**를 남길 수 있다. 오차막대는 어디에도 없다.

⑧ **슬랩 두께 수렴 시험 없음.** figure-read 로 Li₂S 층은 **거의 한 겹**이다. 한 겹짜리 "층"의 관통 장벽은 사실상 **표면 흡착·탈착 에너지에 가깝고**, 두께를 늘리면 벌크 값(≈0.45 eV, ref 27)으로 수렴할 가능성이 크다. **이것이 0.22 를 벌크 물성으로 오독하면 안 되는 물리적 이유다.**

⑨ **계면 형성에너지의 부호 해석이 느슨하다.** γ_ie < 0 은 *"LiF·Li₂S 가 이미 존재할 때"* 계면이 자발 형성된다는 뜻이지, **그 상이 생기는 반응이 자발적이라는 뜻이 아니다**. 논문은 이 구분을 하지 않고 *"can be spontaneously formed when LiF or Li₂S is present"* 로 조건을 달았다가, 이후 문장에서는 조건 없이 우열을 말한다.

⑩ **`Fig. S11` 막대 규칙 미기재.** Cal.(주황) 위에 Exp.(파랑) 이 겹친 것인지 누적된 것인지 캡션·본문 어디에도 없다. 겹침으로 읽으면 벌크 Li₂S Exp ≈0.74 eV, 누적으로 읽으면 ≈0.29 eV — **두 배 이상 차이난다.** 우리는 겹침으로 읽었고(다른 계들의 Cal.<Exp. 관계가 물리적으로 자연스럽다), **이 판독은 잠정**이다.

⑪ **용량유지 99.5 % 의 기준점이 20번째 사이클이다.** `Fig. 5a` figure-read 로 용량은 **20 cyc 이후에도 계속 올라 50–70 cyc 에서 ≈153 으로 정점**을 찍고 내려온다. **정점 대비로 재면 ≈96–97 %** 다. 기준 사이클 선택이 유리한 쪽이다.

⑫ **로딩이 낮다** (LFP 2.0–2.5 mg cm⁻²) 그리고 전류밀도도 낮다 (0.05 mA cm⁻² ≈ 0.03 C 급). 실용 셀 성적으로 확장 인용 금지.

---

## 11. ★★ 우리 DFT 대비 → `../our_dft_baseline.md` · `db/properties/sei_neb.json`

### 11.1 우리 값의 지위 (먼저 못 박는다)

`db/properties/sei_neb.json` → `results["v2/li2s"]`:
**0.305 eV** · QE CI-NEB(neb.x) · 반형석 **3×3×3**(λ₁ 12.1 Å) · **7 images** · **V_Li⁻ 하전 공공 + jellium (tot_charge −1)** · ecutwfc 60 / ecutrho 480 Ry · **c→c 최근접 홉 d = 2.8526 Å** · 끝점 대칭등가 · converged.
- `citable: false` · `absolute_citable: false` · `scientific_status: provisional_single_cell` · `cell_convergence_status: untested`
- ⛔ `forbidden_statement`: *"0.305 eV 를 수렴된 Li₂S 고유 물성으로 인용하거나 **실험·문헌 값과 나란히 놓는 것**"*
- ✅ **허용된 유일한 문장 (그대로만)**: *"For the Li2S antifluorite 3x3x3 model, the charged-vacancy (V_Li-, jellium) nearest-neighbour c->c CI-NEB barrier is 0.305 eV under this finite-cell protocol."*

### 11.2 다섯 축 판정 — **값 대 값 표를 만들지 않는다**

| 축 | **Lai 2020 (L2: Li₂S 층)** | **우리 `v2/li2s`** | 판정 |
|---|---|---|---|
| **① 셀 / 슈퍼셀 · 원자수** | **명시 없음.** 진공 20 Å 슬랩. figure-read: 극히 얇은 층(≈한 겹), 인셋 원자 ~20개 | 벌크 주기 **3×3×3 반형석**, λ₁ 12.1 Å (⚠ **원자수는 우리 레코드에도 미기록**. λ₁ = 12.1 Å ≈ 3 × 4.03 Å ⇒ **원시 fcc 셀의 3×3×3 = 81 원자**, 공공 1개 빼면 80 — **우리 쪽 유도값**이지 기록값이 아니다) | ⛔ **불일치.** 슬랩(2D, 표면 2개) vs 벌크(3D 주기). 애초에 다른 계 |
| **② 전하 규약** | **⛔ 명시 없음.** NELECT·배경전하·jellium 언급 0. figure-read 로 **여분 Li 원자 1개(침입형)**, 기본값이면 중성 셀 | **V_Li⁻ 하전 공공 + jellium**, tot_charge = −1, gaussian smearing | ⛔ **불일치이자 비교 불가.** 침입형(추정) vs 공공, 중성(추정) vs q=−1 |
| **③ 홉 정의** | **여분 Li 이 슬랩 윗면→아랫면 관통.** **6단 다중홉**, 중간 극소 존재, LiF 쪽은 **격자 Li 밀려남 동반**(figure-read). 자리 지정·홉 거리 **명시 없음** | **단일 최근접 홉** 8c → 8c, **d = 2.8526 Å**, 끝점 대칭등가, n_path_steps = 1 | ⛔ **완전히 다른 양.** 하나는 *막을 뚫는 투과 장벽*, 하나는 *격자 내 전도 홉* |
| **④ CI · 이미지 수 · 힘 임계** | CI-NEB **선언 ✔**. 이미지 수 **명시 없음**(figure-read 7점). 힘 **0.05 eV/Å** | CI auto, **7 images**, QE 기본 임계 | ⚠ **부분 일치.** CI 는 양쪽 다. 이미지 수는 우연히 같아 보이나 그들은 미기재. **힘 임계는 그들이 5× 느슨** |
| **⑤ 코드 / 범함수 / 컷오프** | **VASP / PAW / GGA-PBE / 520 eV / k-density 4/Å** | **QE / PBE / ecutwfc 60 Ry(≈816 eV) · ecutrho 480 Ry** | ⚠ **부분 일치.** 범함수(PBE)만 같다. 코드·기저·PP·k-mesh 규약이 다르다 |

**⇒ 종합 판정: 다섯 축 중 ①②③ 이 어긋난다 ⇒ `0.22 eV` 와 `0.305 eV` 는 같은 양이 아니다.**
**두 값을 나란히 놓지 않는다. 비율도 계산하지 않는다.** 이 논문은 우리 `v2/li2s` 에 대해 **반증도 지지도 아니다.**

### 11.3 ★ 그런데 이 논문이 **진짜 비교 대상을 가리켜 준다**

`Fig. S11` 이 **"Li₂S"(벌크, 문헌) 막대를 자기 "Li₂S layer" 막대와 분리**해 그렸다:

| | 값 | 출처 | 우리와의 관계 |
|---|---|---|---|
| **Li₂S (벌크) Cal.** | **figure-read ≈0.45 eV** | SI ref **[27] Moradabadi & Kaghazchi, *Appl. Phys. Lett.* 2016, 108, 213906 — "Thermodynamics and kinetics of defects in Li₂S"** | ★★ **우리 0.305 eV 가 겨눠야 할 문헌 짝은 여기다.** 제목이 *defects in Li₂S* 이므로 **결함 매개 홉**일 가능성이 높다 = 우리와 **같은 종류의 양**일 수 있다 |
| Li₂S (벌크) Exp. | figure-read ≈0.74 eV | SI ref [28] Lin/Dudney/Liang *ACS Nano* 2013 | 실험 전도도 Arrhenius Ea (전도도 측정 ≠ 단일 홉 장벽) |
| **Li₂S layer** | 0.22 eV | 이 논문 | ⛔ 우리와 비교 불가 (§11.2) |

⛔ **단, ≈0.45 는 figure-read 이고 [27] 원문을 우리가 아직 안 봤다.** 그 논문도 **전하 규약(중성 vs 하전 공공)·셀 크기**를 확인하기 전에는 우리 0.305 와 나란히 놓을 수 없다. **다음 할 일 = [27] 확보 후 다섯 축 재대조.**

### 11.4 LiF — 우리 SEI 사다리의 빈 칸에 대한 소득

`comparison_vs_ours.md` §E 가 이미 *"우리 SEI gap 사다리의 맨 위 칸이 비어 있다 — LiF"* 를 걸어 두었고, `sei_neb`·`sei_electronic`·`sei_formation_voltage` 에 LiF 를 넣는 것이 할 일 #1 이다.
- 이 논문은 **LiF 층 0.67 eV**(자기값, 층) 를 준다 — ⛔ **우리 벌크 LiF 계산의 목표값으로 쓰면 안 된다** (같은 ①②③ 불일치).
- 대신 **벌크 LiF 의 문헌 출처를 가리켜 준다**: `Fig. S11` ref **[25] Chen, Ouyang, Song, Sun, *J. Phys. Chem. C* 2011, 115(14), 7044–7049 — "Electrical and lithium ion dynamics in three main components of solid electrolyte interphase from density functional theory study"** (figure-read Cal. ≈0.73 eV). **SEI 3성분(LiF·Li₂O·Li₂CO₃)을 한 논문에서 DFT 로 다룬 편**이므로, 우리 `sei_electronic`·`sei_neb` 를 채울 때 **한 번에 여러 칸을 대조할 수 있는 후보**다.

### 11.5 우리에게 옮겨도 되는 것 / 안 되는 것

| | 항목 |
|---|---|
| ✅ **옮겨도 됨 (방법·어휘)** | ① `γ_ie = [E_A\|B − (E_A + E_B)]/S` **계면 형성에너지로 SEI 상 선택성을 말하는 틀** ② `Fig. 2c` 의 **tip / flat potential 분리 어휘** ③ XPS BE 앵커 (§3.4) — 우리 `xps_reference_sei.csv` 와 대조 가능 ④ `Fig. S11` 식 **"우리 값 ± 문헌 Cal./Exp. 를 한 막대에" 표기법**(단 누적/겹침 규칙을 반드시 캡션에 명시할 것 — 이 논문의 실패를 반복하지 말 것) |
| ⛔ **옮기면 안 됨** | ① **0.22 / 0.67 eV 를 우리 NEB 값과 같은 표·같은 축에** ② 0.22 를 **"Li₂S 의 이동장벽"** 으로 (논문 자신이 "layer" 라고 한정했다) ③ **≈0.45 / ≈0.73 / ≈0.74 / ≈0.85 eV** 를 원문(ref 25/27/28) 확인 없이 (전부 figure-read + 막대 규칙 모호) ④ `Table 1` 의 J m⁻² 값을 우리 eV 단위 형성에너지와 |

---

## 12. 적용 인사이트 (우리 연구에 어떻게)

1. **★★ 인용 사슬은 여기서 끝난다 — 그리고 끝점이 "층" 이었다.** Liu 2024 → Lai 2020 이 전부이고, Lai 는 **자기 계산**을 했다. 다만 그 계산의 대상이 **벌크 Li₂S 가 아니라 나노 두께 층**이었고, **논문 자신이 그 구분을 `Fig. S11` 에 그려 놓았다**. ⇒ 우리가 앞으로 *"문헌 Li₂S 장벽은 0.22 eV"* 라고 쓰면 **논문의 자기 구분마저 무시하는 것**이 된다. 정확한 문장은 *"Lai 2020 이 CI-NEB 로 계산한 **나노 Li₂S 층 관통** 장벽이 0.22 eV 이고, 같은 논문이 인용한 **벌크 Li₂S 계산값은 그보다 두 배 크다**"*.
2. **★ 우리 `v2/li2s` 를 승격시키려면 필요한 것이 명확해졌다.** 셀 수렴 시험(3×3×3 → 4×4×4)에 더해, **문헌 짝을 [27] Moradabadi & Kaghazchi 2016 로 고정**하고 다섯 축(특히 **전하 규약**)을 대조해야 한다. Lai 를 짝으로 삼는 시도는 여기서 종결한다.
3. **★ LiF 칸 채우기의 출발점이 생겼다.** [25] Chen *JPCC* 2011 은 **LiF·Li₂O·Li₂CO₃ 를 한 편에서** DFT 로 다룬다 ⇒ 우리 `sei_electronic`(현재 LiCl 6.26 > Li₂O 4.99 > Li₂S 3.44 > Li₃P 0.71 eV, **LiF 없음**) 과 `sei_neb` 를 **동시에** 대조할 수 있는 단일 문헌 후보다.
4. **"층이라서 빠르다" 는 가설은 우리가 검증할 수 있는 것이다.** 우리는 이미 Li₂S 벌크 NEB 인프라(`tools/`, `sei_neb.json`)를 가지고 있다. **같은 프로토콜로 Li₂S 슬랩(두께 1·2·3 삼중층)의 관통 장벽을 재면**, Lai 의 0.22 가 두께 수렴 곡선의 어디에 있는지 판정할 수 있다. ⚠ 단 이건 **estimand 카드부터** 채워야 한다(CLAUDE.md 2026-08-28) — *"관통 장벽" 이 이 계에서 잘 정의되는 스칼라인가* 가 첫 질문이고, `Fig. 3e` 에서 격자 Li 이 밀려나는 걸 보면 **admissible state 가 여럿**일 위험이 크다.
5. **계면 형성에너지 부호 논법을 우리 축 E 에 이식할 수 있다.** *"두 SEI 상이 동시에 가능할 때 어느 쪽이 먼저 깔리나"* 를 **γ_ie 크기 비교**로 답하는 방식은 우리 `interface_reactivity` 예측을 **정량 서열**로 바꾸는 값싼 경로다. (단 §10-⑨ 의 조건 — "그 상이 이미 존재할 때" — 을 반드시 붙일 것.)

---

## 13. 인용 가능 문장 (deck/paper 용)

- *"Lai et al. (Nano Lett. 2020, 20, 8273) computed, with VASP/PBE CI-NEB, that Li migrating **through a thin Li₂S layer** faces a 0.22 eV barrier versus 0.67 eV **through a LiF layer**."* — ✅ (반드시 **"through a … layer"** 를 유지)
- *"In the same work's own literature compilation (Fig. S11), **bulk** Li₂S is plotted separately with a calculated barrier roughly twice that of their layer value."* — ✅ (**figure-read** 임을 밝힐 것)
- *"The Li|Li₂S interface formation energy (−0.29 to −0.44 J m⁻²) is 4–5× more negative than Li|LiF (−0.078 to −0.096 J m⁻²), while bare Li surfaces are positive (0.47–0.55 J m⁻²)."* — ✅ (`Table 1` 인쇄값)
- *"The composite electrolyte reaches σ = 3.42 × 10⁻⁴ S cm⁻¹ and t_Li⁺ = 0.44 at RT, versus 2.40 × 10⁻⁴ S cm⁻¹ and 0.16 without the sulfide filler."* — ✅
- ⛔ **금지**: *"문헌 Li₂S 이동장벽 0.22 eV 대비 우리 0.305 eV"* — 다섯 축 중 셋이 어긋난다 (§11.2).
- ⛔ **금지**: 0.67/0.22 를 **정의 명시 없이** "3배" 로 (§10-①).
- ⛔ **금지**: `Fig. S11` 의 ≈0.45/≈0.73/≈0.74/≈0.85 를 원문 확인 없이 (figure-read + 규칙 모호).

---

## 14. 기법 용어 미니사전

- **CI-NEB (climbing-image nudged elastic band)** — 두 끝점 사이에 이미지(중간 구조) 여러 개를 스프링으로 엮어 최소에너지경로를 찾고, 그중 **가장 높은 이미지만 스프링을 끄고 힘의 부호를 뒤집어** 안장점으로 밀어 올리는 방법. 안장점 에너지를 정확히 잡는 것이 목적. 원전 = Henkelman, *J. Chem. Phys.* **2000**, 113, 9901. ⚠ 이 논문 SI 는 *"climbing-image **under** elastic band"* 라고 오기했다(정확히는 *nudged*).
- **에너지 스팬 vs 최대점−초기상태** — 다단 경로에서 "장벽"을 정하는 두 규약. 전자는 `max over h>i (E_h − E_i)` = 가장 큰 오르막 한 구간, 후자는 `max(E) − E(초기)`. 중간 극소가 깊으면 **전자가 훨씬 크다**. 이 논문은 전자를 쓴다 (§10-①).
- **jellium 배경전하** — 하전 결함(예: V_Li⁻)을 주기셀에 넣으면 전체가 발산하므로 균일한 반대부호 배경을 깔아 중성화하는 근사. **유한셀 오차가 남아** 셀 수렴 시험이 필수. 우리 `v2/li2s` 가 여기에 해당하고, **Lai 는 이 규약을 아예 언급하지 않는다**.
- **침입형(interstitial) vs 공공(vacancy) 매개 홉** — Li 전도의 두 기구. 침입형은 **여분 Li 이 격자 틈으로** 움직이고, 공공은 **빈 자리로 이웃 Li 이 뛴다**. 장벽 크기·전하 규약·농도 의존성이 전부 다르다. Lai 의 인셋은 **여분 Li**(침입형)으로 보이고, 우리 것은 **공공**이다.
- **Bruce–Vincent 이동수 t_Li⁺** — 대칭셀에 작은 직류 분극(여기 10 mV)을 걸고 **초기/정상상태 전류 + 분극 전후 계면저항**으로 양이온 수송분율을 뽑는 표준법. 저항 보정을 하지 않으면(단순 I_s/I₀) 과대평가된다 — 이 논문은 22.5→14.2 (비 0.63) 에서 보정 후 **0.44** 를 얻는다.
- **γ_se = ΔE/(2S)** 의 2 — 벌크를 자르면 **표면이 두 개** 생기므로 나눈다. 반대로 계면 형성에너지 γ_ie 는 **계면이 하나**라 2 가 없다.
- **SMIL / FMIL** — 이 논문의 조어. **S**ulfide(Li₂S)-**M**odified **I**nterfacial **L**ayer / **F**luoride(LiF)-**M**odified. 우리 문서에서 쓸 땐 반드시 풀어 쓸 것.
- **탈불소화(dehydrofluorination)** — PVDF `–(CH₂–CF₂)–` 가 염기·환원 조건에서 HF 를 잃고 이중결합화하는 반응. Li 금속과 만나면 진행되며 **LiF + 전자전도성 탄소질**을 남긴다 — 이 논문이 막으려는 것.
