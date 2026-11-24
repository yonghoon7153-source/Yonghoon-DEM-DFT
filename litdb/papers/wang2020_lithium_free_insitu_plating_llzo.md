<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = zuo2022_chlorination_cathode_interface.md · 꼴 참고 = liao2025_interfacial_adhesion_li_plating_carbon_interlayer.md (같은 박리 계열).
     2026-11-24 작성 (병렬 배치 · 공유 파일은 메인 세션이 합친다).
     원문 = 본문 9 pp (Nat. Commun. 11, 5201 · OA CC BY 4.0) + SI 12 pp (Supplementary Fig. 1–7 · Supplementary Methods (peel) · Supplementary Discussion (CCD)).
     값 표지: [인쇄] = 본문·SI·그림 안 글자로 적힌 값 · `figure-read ≈` = 그림에서 읽은 값 (래스터 픽셀 판독)
              · `figure-read ≈ (벡터)` = 본문 PDF 의 벡터 경로 좌표를 축 눈금에 맞춰 읽은 값 (Fig. 1b · 2a · 2b · 4g · 6b — 픽셀 판독보다 정밀)
              · [우리 산술] = 인쇄·판독 값으로 이 digest 가 계산한 값 (식 · 가정 병기) · [미확인] = 본문 + SI 어디에도 없음.
     크롭: 도구 13 장 중 4 장 (Fig. 2 · 3 · 5 · 6) 을 손으로 다시 잘랐다 (recrop 사유는 figures.json) + 식 크롭 4 장 손으로 (eq_*). 도구의 '놓친 번호' S8–S36 은 오탐 (본문 'Supplementary Fig. S6' + 위첨자 참고문헌 31–36). -->

# Enabling "lithium-free" manufacturing of pure lithium metal solid-state batteries through in situ plating — 무음극(Li-free) LLZO 셀에서 Li 를 **집전체(CC)/LLZO 계면에 그 자리 전기도금**: 5 mAh cm⁻² (≈25 µm) 도금·탈리 · 핵생성 과전압 수 mV · **CC/LLZO 박리 점착 1–10 J m⁻²** 를 넣은 고전 핵생성 모형 · NCA/PEO 풀셀 50 사이클 — Wang · Carmona · Gupta · Albertus · Sakamoto (*Nat. Commun.* 11, 5201 (2020))

> slug `wang2020_lithium_free_insitu_plating_llzo` · DOI `10.1038/s41467-020-19004-4` · type `exp (in situ Li 전기도금 · 갈바노스태틱 + EIS · FIB-SEM 단면 + EDS · CC 박리 후 ex situ SEM · 90° peel 점착 시험 + 박리 팔 소성 보정 · 해석식 핵생성 모형 — 원자단위 계산 0)` · PDF `litdb/inbox/wang2020_insitu_plating_main.pdf` (본문 9 pp) + `litdb/inbox/wang2020_insitu_plating_SI.pdf` (SI 12 pp · Fig. S1–S7 · Supplementary Eq. 1–2) · digested `2026-11-24` · status ✅
> elements: Li, La, Zr, Ta, O, Cu, Ni
> methods: adhesion

> **저자**: Michael J. Wang¹, Eric Carmona², Arushi Gupta³, Paul Albertus², **Jeff Sakamoto**¹²⁴\* (교신 · jeffsaka@umich.edu) — ¹Univ. of Michigan MSE · ²Univ. of Maryland Chem. & Biomol. Eng. · ³Univ. of Michigan Macromolecular Sci. & Eng. · ⁴Univ. of Michigan ME (소속 번호는 PDF 1 쪽 그대로)
> 투고 2020-03-20 · 수리 2020-09-22 · 온라인 2020-10-15 · **OA CC BY 4.0** · 자금 ARPA-E DE-AR0000653 · 이해상충: J.S. = Zakuro, Inc. 창업자 · 역할: M.J.W. 실험 · A.G. 고분자 복합양극 · **E.C. · P.A. 핵생성 이론·모형** · P.A. · J.S. 지도
> 계보: Neudecker 2000 (LiPON 박막 'Li-free' 원전, ref 15) → Motoyama 2015 (CC/LiPON 핵생성·성장 모형, ref 20) · Krauskopf 2019 (LLZO 위 Li 성장 동역학, ref 19) · Lee 2020 *Nat. Energy* (Ag–C 층, ref 23) → **본 논문** (LLZO 에서 인터레이어 없이 'Li-free') → 같은 그룹 후속 `lee2022_thin_insitu_li_void_rewetting_llzo` (얇은 in situ Li 의 공극·재젖음 · 같은 배치에서 정리됨).

> ⚠⚠ **네 줄 경고 — 인용 전에 반드시.**
> ① **LLZO (산화물 가넷 Li₆.₅La₃Zr₁.₅Ta₀.₅O₁₂) 계다.** LPSCl 값으로 옮기지 않는다. 특히 *"LLZO 는 Li 와 안정하니 부반응이 없고 CE 가 원리상 100 %"* (p.7) 는 **Li 금속(0 V)에서 열역학적으로 환원되는 LPSCl 에는 성립하지 않는다** (우리 grand-potential 환원 경계가 0 V 보다 한참 위 — 값은 `../our_dft_baseline.md`).
> ② **점착 1–10 J m⁻² 는 박리 시험의 실용 점착 (G_c 부류) 이다** — 측정 박리력에서 박리 팔의 소성 일 Q 를 **모형으로 뺀** 값이고, 그 입력 (σ_Y · t · E) 이 논문에 없다. 저자 스스로 *"upper bound of the true values"* (SI p.10). **DFT W_ad 와 같은 줄 금지.** 같은 논문 본문은 한 곳에서 *"10 s of J m⁻²"* 라고도 쓴다 (p.6). 소성 보정 전 상한 P(1−cos φ) = **Cu ≈ 69 · Ni ≈ 32 J m⁻²** [우리 산술 · `Fig. S4` 판독 · §6-2].
> ③ **"CE ≈ 99 %" 는 1.8 V · 2 h 정전압 유지를 포함한 값이다** (p.4). 정전류만이면 **0.929–0.966** (`Fig. 2b` 벡터 판독 · 12 사이클) 이고 `Fig. 2a` 에서 정전류로 벗긴 몫은 ≈ **4.5 / 5.0 mAh cm⁻² (≈ 90 %)** 다. 풀셀의 "CE ≈ 100 %" 는 **Li 저장분 2.7 mAh cm⁻² 위에서 < 0.8 mAh cm⁻² 만 돌린** 값이라 무음극 가역성의 시험이 아니다.
> ④ **"50 사이클 ≈ 25 % 용량 감소" (p.7) 는 충전 용량 기준과 맞는다** (Q_charge 0.629 → 0.481) — **방전 용량은 0.787 → 0.494 (−37 %)** (`Fig. 6b` 벡터 판독). 인용하면 어느 용량인지 적는다.

> **본 digest 에서 실제로 본 그림 (2026-11-24)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` (본문 6 장 전부 · 크롭으로) · `Fig. S1` `Fig. S4` `Fig. S5` `Fig. S6` `Fig. S7` (크롭으로) · `Fig. S2` `Fig. S3` (**SI 쪽 렌더로만** — 크롭 파일은 열지 않았다) · 식 크롭 4 장 (eq_01 · eq_02_03 · eq_04 · eq_S1_S2) — 그림 13 장 전부 + 식 4 장.
> 그림에서만 읽은 값은 **`figure-read ≈`** 로, 벡터 경로에서 읽은 값은 **`figure-read ≈ (벡터)`** 로 표시했다.
> 본문 서술과 어긋난 그림 6 곳 → §10 (`Fig. 1b` 범위 · `Fig. 2b` 의 '> 99 %' · `Fig. 3a` '최소 간극' · `Fig. 3b` 33 µm · `Fig. 5b` 'micron range' · `Fig. 6b` 25 % · `Fig. S7b` 용량 축).

---

## 0. 이 digest 를 읽는 법 — 우리 읽기축

이 논문은 **우리 물질 (argyrodite) 논문이 아니다.** 그런데도 정리하는 까닭은 셋이다.

1. **W_ad 보고서 7 절 (Li 친화성 · 핵생성 · 점착과 공극) 의 실험 앵커** — 보고서 위치 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` §7 (Li 친화성 정량화 제안) · §2 (쌍별 W 값). **우리 W 값은 이 digest 에 싣지 않는다 — 위치만.**
   이 논문은 *"Li 가 CC/전해질 계면을 **열면서** 핵을 만든다 → 그 일 = 옛 계면 점착 − 새 계면 점착 (식 1)"* 이라는 틀을 처음 정량 실험과 묶었다. 우리 DFT 가 낼 수 있는 항 (W_adh,Li·CC · W_adh,Li·SE) 을 **논문은 0 으로 두었다** — 그 빈칸이 우리 몫이다 (§7a · §11).
2. **연속체 · DEM 모형 입력** — 적층압 ≈ 4 MPa · Li 항복 < 1 MPa · 압력 과전압 V̄p/F (4 MPa → 0.5 mV) · 핵 밀도 (≈ 10 mm⁻²) · 핵 지름 (≈ 100 µm @ 30 µAh cm⁻²) · 피복률 시계열 (15 % → ≈ 50 % → 합체 ≈ 1 mAh cm⁻²) · 벗긴 뒤 공극 5–10 µm · 계면 저항 < 10 Ω cm². 전부 **LLZO · 2 mm 펠릿 · 25 °C · 0.05 mA cm⁻²** 조건값이다 (§3 · §11).
3. **G_c 대 W_ad 의 간극을 보여 주는 또 하나의 사례** — 박리 상한 30–70 J m⁻² (우리 산술) 대 원자 규모 계면 에너지 (< 1 J m⁻², 저자 표현). 같은 박리 계열 `liao2025_interfacial_adhesion_li_plating_carbon_interlayer` (탄소/LPSCl Γ 9–41 J m⁻² · 문턱 ≈ 10 J m⁻²) 와 같은 자릿수다 (§7 · §10).

**이 논문이 한 것**: (i) Li 원(foil) | 2 mm LLZTO | 적층(laminated) Cu 또는 Ni 박 셀에서 0.05 mA cm⁻² 로 5 mAh cm⁻² 까지 Li 를 CC 쪽에 도금 → EIS 로 '차단 → 비차단' 전이와 무변화 확인, (ii) 도금·탈리 가역성 (CE · EIS), (iii) FIB 단면 + CC 를 떼어낸 LLZO 면의 시간별 SEM 으로 핵 → 옆성장 → 합체 → 수직성장, (iv) 90° 박리로 CC/LLZO 점착, (v) 고전 핵생성 식 (구형 핵 · 표면항 = 계면 여는 일) 과 성장 과전압 식 (식 4), (vi) NCA/PEO 복합양극 풀셀 (60 °C · 50 사이클).
**안 한 것**: 원자단위 계산 0 · 핵생성 장벽 ΔG* 계산 없음 · Li–CC · Li–LLZO 점착 측정·계산 없음 (0 으로 가정) · 박리 소성 보정 입력값 미기재 · 통계 (셀 수 · 오차막대) 거의 없음 · 황화물 SE 없음.

---

## 1. 한 줄 요약

LLZO 펠릿에 Cu·Ni 박을 900–1100 °C 에서 **확산 접합**하고 0.05 mA cm⁻² 로 Li 를 그 계면에 그 자리 도금하면 **5 mAh cm⁻² (≈ 25 µm) 까지 LLZO 손상 없이 쌓이고 거의 되돌릴 수 있다** (정전압 유지 포함 ≈ 99 %). Li 는 균일 막이 아니라 **소수의 핵 (≈ 10 mm⁻²) 이 옆으로 자라 ≈ 1 mAh cm⁻² 에서 합체**하는 식으로 자라며, 저자는 그 전위 곡선의 작은 골 (핵생성 과전압 ≈ 수 mV) 을 **CC/LLZO 계면을 여는 일 (박리 점착 1–10 J m⁻²)** 로 해석하는 고전 핵생성 틀을 냈다. 단점: 형성 전류 상한이 0.09 mA cm⁻² (그 이상 단락) 라 **5 mAh 에 100 h**, in situ Li 의 CCD 는 0.3 mA cm⁻² 로 Li 박 (≈ 1) 보다 낮다.

---

## 2. 메타 / 동기 / 질문

| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| M. J. Wang · E. Carmona · A. Gupta · P. Albertus · Jeff Sakamoto\* (Michigan · Maryland) | *Nat. Commun.* 11, 5201 (2020) | 10.1038/s41467-020-19004-4 | Li₆.₅La₃Zr₁.₅Ta₀.₅O₁₂ (LLZTO, 열간 유도 가압) · CC = Cu 10 µm / Ni 35 µm 박 · 양극 NCA + PEO-LiTFSI | exp + 해석식 모형 (원자단위 계산 0) |

**동기 (p.1–3).**
- SOA 양극 (NMC · NCA · LFP) 은 **완전 리튬화 상태로 만든다** → 미리 붙인 Li 금속은 부피·무게만 늘린다. 흑연 → Li 금속 교체로 에너지 밀도 40–50 % 증가 (refs 1–5 인용) [인쇄].
- 목표치 인용: > 1000 Wh L⁻¹ · > 1000 사이클 (≤ 80 % 용량 감소 — 원문 표현 그대로) · < $100 kWh⁻¹ (refs 6, 7).
- 실험실 Li 금속 셀은 > 200 µm 박을 쓴다 · 얇게는 ≈ 20 µm 까지 만들었지만 취급·비용 때문에 자립 박은 비현실적 (ref 8).
- 액체계 'anode-free' 는 Li 와 전해질 반응으로 CE 가 낮다 (refs 9, 10, 12–14). LiPON 박막은 'Li-free' 를 이미 보였지만 (Neudecker 2000, ref 15) 대형 제조가 어렵다.
- LLZO 는 Li 와 안정하지만 조건에 따라 Li 필라멘트가 뚫는다 (refs 16–18). 스퍼터 CC/LiPON · LLZO 위 핵생성 연구 (refs 19–22) 는 **도금이 CC 를 깨뜨려 '죽은 Li' · 낮은 CE · (LLZO 에선) 단락**을 보였다.
- Lee 2020 (*Nat. Energy*, ref 23): Ag–C (≈ 10 µm) 층이 **핵생성 에너지를 낮춘다는 가설** — *"While reduction in nucleation energy was not quantified"* (p.2).

**질문 셋.**
- **Q1** 상용급 용량 (≥ 3 mAh cm⁻²) 을 인터레이어 없이 LLZO/CC 계면에 그 자리 도금·탈리할 수 있나 — LLZO 를 망가뜨리지 않고?
- **Q2** 도금 전위 곡선 (특히 시작의 골) 을 계면 역학 (점착) 과 어떻게 잇나?
- **Q3** 그렇게 만든 Li 가 대칭셀 · 실제 양극 풀셀에서 음극으로 작동하나?

**답 (저자).** Q1 예 (5 mAh cm⁻² · 0.05 mA cm⁻² · 4 MPa · 25 °C) · Q2 식 (1)–(4) 의 '계면을 여는 일' 틀 (정량 검증은 아님 — 저자 스스로 "initial framework") · Q3 예 (NCA/PEO 풀셀 50 사이클 · 퇴화는 양극 쪽 PEO 계면 탓, Cu/LLZO/Li 박 대조셀로 확인).

---

## 3. 핵심 수치 총정리 ★

### 3a. 셀 · 조건 (Methods p.8)

| 항목 | 값 | 출처 | 비고 |
|---|---|---|---|
| 전해질 | Li₆.₅La₃Zr₁.₅Ta₀.₅O₁₂ · 고상합성 → 급속 유도 열간가압 (Taylor 2018, ref 39) · 다이아몬드 톱으로 ≈ 2 mm 펠릿 | p.8 [인쇄] | 상대밀도 · 입도 · σ [미확인] |
| CC | Cu 10 µm · Ni 35 µm (Targray 전지급 박) | p.8 [인쇄] | 표면 거칠기 [미확인] |
| CC 적층 (lamination) | LLZO 한 면 1200 grit 연마 → 박 올림 → **3–6 MPa · 900–1100 °C · 5 분** (금속에 따라) | p.8 [인쇄] | 금속별 정확한 T [미확인] |
| 반대면 | 연마 → 0.1 µm 다이아몬드 페이스트 → **400 °C Ar 열처리** (저항성 표면층 제거) → **750 µm Li 박** 을 고온에서 압착 (ref 18) | p.8 [인쇄] | Li 원 = Li 박 (양극 계면 인공물 배제가 이유) |
| 적층압 (운전) | **≈ 4 MPa** | p.8 · p.5 [인쇄] | 풀셀 PEO 함침은 4.2 MPa · 80 °C 수 시간 |
| 온도 | 도금·탈리 실험 전부 **25 °C** · 풀셀 형성 80 °C · 순환 60 °C (± 3 °C) | p.8 · p.7 [인쇄] | |
| EIS | 진폭 5 mV · 500 mHz–7 MHz (Bio-Logic VMP-300) | p.8 [인쇄] | 풀셀 EIS 줄은 *"between 500 and 7 MHz"* — 단위 누락 오기 |
| 도금 전류 | **0.05–0.1 mA cm⁻²** | p.8 [인쇄] | ≥ 0.09 에서 단락 (p.4) |
| 탈리 전류 | 0.05–0.3 mA cm⁻² | p.8 [인쇄] | |
| 두께 환산 | 5 mAh cm⁻² ≈ 25 µm · 2.7 ≈ 13.5 µm (균일 가정) | p.3 · p.7 [인쇄] | = 5 µm / (mAh cm⁻²) 반올림 · 정확값 4.85 µm [우리 산술, V̄_Li 13.0 cm³ mol⁻¹] |

### 3b. in situ 도금 첫 응답 (`Fig. 1` · Ni CC · 0.05 mA cm⁻² · 25 °C)

| 양 | 값 | 출처 |
|---|---|---|
| 개회로 전압 (Li 원 vs Ni CC) | ≈ 1.8 V | p.3 [인쇄] |
| 전위 최소 (골) | ≈ 25 mV (−) · 처음 몇 분 · ≈ 3 µAh cm⁻² | p.3 [인쇄] |
| 　 같은 골 — 그림 | **−0.0259 V @ 0.0046 mAh cm⁻²** (≈ 5.5 분) | `figure-read ≈ (벡터)` |
| 정상 도금 전위 | ≈ 20 mV (−) · 1 시간 안 | p.3 [인쇄] |
| 　 그림 | −0.0240 (0.01) · −0.0224 (0.02) · −0.0219 (0.03) · **−0.0213 V (0.04–0.05 mAh cm⁻²)** | `figure-read ≈ (벡터)` |
| E_nucleation (골 − 정상) | 그림의 빨간 화살표 ≈ **4.3 mV** · 곡선으로는 ≈ 4.6 mV | `figure-read ≈ (벡터)` (본문은 숫자로 안 적음) |
| 전체 이온 임피던스 | ≈ 350 Ω cm² → 0.05 mA cm⁻² 에서 DC 분극 ≈ 17.5 mV | p.3 [인쇄] |
| Z_bulk 표지 · Z_int 표지 | 3.8 MHz · 0.8 Hz | `Fig. 1c` [인쇄] |
| 도금 후 계면 저항 (Li/LLZO) | **< 10 Ω cm²** (저주파 0.5–5 Hz 반원 지름) | p.3 [인쇄] |
| 5 mAh cm⁻² 뒤 EIS 변화 | 없음 → *"no Li filaments have nucleated"* | p.4 [인쇄] |
| 도금 시간 · 양 | ≈ 100 h · ≈ 5 mAh cm⁻² ≈ 25 µm | p.3 [인쇄] |
| 다른 CC 금속 | *"Identical tests … with similar results"* (금속·수치 [미확인]) | p.3 [인쇄] |
| 형성 중 단락 문턱 | **≥ 0.09 mA cm⁻² 에서 일관되게 단락** · 대칭 Li/LLZO/Li CCD 의 ≈ 1/10 | p.4 [인쇄] |
| LLZO 이온전도 함의 | ≈ 6 × 10⁻⁴ S cm⁻¹ (2 mm ÷ 350 Ω cm² — 전체 저항을 LLZO 로 볼 때) | [우리 산술] |

### 3c. 가역성 (`Fig. 2` · `Fig. S1` · Cu CC · 25 °C)

| 양 | 값 | 출처 |
|---|---|---|
| 1 회 도금 / 탈리 | 4.98 / 4.95 mAh cm⁻² (그림 표지) → ≈ 99 % · **1.8 V 2 h 정전압 유지 포함** | `Fig. 2a` · p.4 [인쇄] |
| 도금 / 탈리 평탄 전위 | **−0.0169 / +0.0137 V** (중앙값) | `figure-read ≈ (벡터)` |
| 정전류 탈리가 끝나는 곳 (전위 폭주) | 누적 ≈ 9.51 mAh cm⁻² → 정전류 몫 ≈ **4.5 mAh cm⁻² (≈ 90 %)** · 0.2 V 넘는 곳 ≈ 9.59 · 곡선 끝 ≈ 9.79 | `figure-read ≈ (벡터)` |
| 순환 CE (12 사이클 · 매번 3 mAh cm⁻² · 도금 0.05 · 탈리 0.05/0.1/0.2/0.3 mA cm⁻² 각 3 사이클) — 정전류만 | 0.953 · 0.946 · 0.966 · 0.954 · 0.950 · 0.966 · 0.946 · 0.949 · 0.951 · **0.933 · 0.929 · 0.933** | `Fig. 2b` `figure-read ≈ (벡터)` |
| 　 정전류 + 정전압 | 0.995 · 0.995 · **0.976 · 0.975 · 0.983** · 0.993 · 0.995 · 0.997 · 0.997 · 0.995 · 0.999 · 1.001 (평균 0.992) | `Fig. 2b` `figure-read ≈ (벡터)` |
| 저자 문장 | *"relatively stable above 99 % over the 12 cycles"* | p.4 [인쇄] — 3·4·5 사이클은 99 % 아래 (§10) |
| 잃는 1 % 의 원인 (저자) | 액체계의 부동태·죽은 Li 가 아니라 **LLZO 또는 CC 와의 접촉 손실** | p.4 [인쇄] (직접 증거는 EIS · 단면) |
| 탈리 분극 (전류별) | +0.012 (0.05) · +0.029 (0.1) · +0.06 (0.2) · +0.09–0.10 V (0.3 mA cm⁻²) → ≈ 240–300 Ω cm² | `Fig. S1` figure-read ≈ |
| 정전류 탈리 끝 (3 mAh 중) | ≈ 2.89 (사이클 1) · 2.86 (4) · 2.75 (7) · 2.69 mAh cm⁻² (10) | `Fig. S1` figure-read ≈ |
| 탈리 뒤 EIS | 저주파 비차단 → 차단 · **고주파 (LLZO 옴) 호가 크게 증가** (≈ 250 → ≈ 430 Ω cm² 끝점) · 재도금 → 원래 모양 회복 | p.4 [인쇄] · 끝점은 `Fig. 2c` figure-read ≈ |

### 3d. 단면 · 형태 · 핵 (`Fig. 3` · `Fig. 4` · `Fig. S2` · `Fig. S3`)

| 양 | 값 | 출처 |
|---|---|---|
| 5 mAh cm⁻² 도금 뒤 Li 층 | 관찰 **33 µm** (균일 가정 25 µm 보다 두꺼움 → 비균일) | p.4 [인쇄] |
| 　 `Fig. 3b` 패널에서 | 어두운 띠 ≈ 20–21 µm (가로 눈금 기준 · 기울기 보정 전) → 52° 보정 가정 시 ≈ 25–27 µm | figure-read ≈ (픽셀) · 33 µm 를 이 패널에서 재현 못 함 (§10) |
| 벗긴 뒤 간극 | **5–10 µm** · 적층압 아래선 덜 두드러질 것 · 다른 곳은 접촉 유지 (`Fig. S2d`) | p.4 [인쇄] |
| 　 `Fig. 3c` 패널에서 | 4.5–8.2 µm (보정 전) | figure-read ≈ (픽셀) |
| 적층 직후 계면 (`Fig. 3a`) | 저자 *"minimal gaps"* — 그림에는 **길이 ≈ 7–9 µm · 열림 ≈ 1 µm 의 렌즈형 공극**이 줄지어 있고 가장 짙은 행에서 계면 길이의 **≈ 47 %** 가 공극 | figure-read ≈ (픽셀 · 보정 전) |
| 박리 SEM 시점 | 4 · 30 · 200 · 620 · 1000 · 1600 µAh cm⁻² (= 5 분 · 36–38 분 · 4 h · 12.4 h · 20 h · 32 h @ 0.05 mA cm⁻²) | p.4 [인쇄] · 시간 환산 [우리 산술] (본문은 30 µAh = 38 분) |
| 4 µAh cm⁻² | Li 식별 어려움 | p.4 [인쇄] |
| 30 µAh cm⁻² | **≈ 100 µm 지름 패치 · LLZO 면의 ≈ 15 %** · 자라지 않은 작은 핵도 보임 | p.4 [인쇄] |
| 　 `Fig. 4b` 판독 | 패치 지름 ≈ 100–250 µm · 패널 (≈ 2.0 × 1.65 mm) 에 ≈ 12–15 개 → ≈ 4–5 mm⁻² | figure-read ≈ |
| 핵 밀도 (저자) | **≈ 10 nucleates per mm²** · *"~100 µm by 1 h"* | p.6 [인쇄] |
| 200 µAh cm⁻² | 패치 수 증가 + 옆으로 성장 | p.4 [인쇄] |
| 620 µAh cm⁻² (≈ 12 h) | 피복 ≈ 50 % · 맨 LLZO 가 아직 남음 · 평균 높이 ≈ 6 µm (그래서 간극이 생길 만하다) | p.4 [인쇄] · 6.0 µm 재현 [우리 산술: 0.62 × 4.85 / 0.5] |
| 1000 µAh cm⁻² | 거의 균일 막으로 **합체** | p.4 [인쇄] |
| 1.6 mAh cm⁻² | 합체 뒤 **수직 성장** · 높이 · 지형 증가 | p.4 [인쇄] |
| 30 µAh 의 평균 패치 높이 | ≈ 1 µm (0.03 × 4.85 / 0.15) | [우리 산술] |
| `Fig. 4g` 전위 | 골 ≈ −0.030 V (≈ 0 mAh) → −0.021 (0.02–0.04) → −0.019 (0.18) → −0.018 (0.45–0.59) → −0.017 (0.8–0.9) → **−0.015 V (1.0–1.14 mAh cm⁻²)** | `figure-read ≈ (벡터)` |
| 세 구간 경계 (`Fig. 4g` 색) | 핵생성 (빨강) ≈ 0 → 0.03 · 옆성장 (노랑) 0.03 → ≈ 1.03 · 합체 + 수직 (초록) > 1.03 mAh cm⁻² | figure-read ≈ |

### 3e. CC/LLZO 점착 (`Fig. S4` · Supplementary Methods p.9–10)

| 양 | 값 | 출처 |
|---|---|---|
| 시험 | TA.XTplus · 90° peel rig · ASTM D6862-11(2016) 변형 · 박 폭 4 mm × 길이 12 mm · **10 mm min⁻¹** · 완전 박리까지 | SI p.9 [인쇄] |
| 실제 박리각 | **Ni 45° · Cu 81°** (90° 지그인데도) | SI p.9 [인쇄] |
| 평균 박리력 (정상 구간 ≈ 0.4–1.0 peel strain · 시편 3 개씩 평균) | **Cu ≈ 81 N m⁻¹ · Ni ≈ 108 N m⁻¹** (점선) | `Fig. S4` figure-read ≈ (픽셀) |
| Ni 초기 봉우리 | ≈ 230 N m⁻¹ (strain ≈ 0.1–0.15) | `Fig. S4` figure-read ≈ |
| 식 | Γ = P(1 − cos φ) − Q (S1) · Q = 박리 팔 소성 일 (S2, σ_Y · t · E · φ′=φ 가정) | SI p.9 [인쇄] · `eq_S1_S2` 크롭 |
| 저자 값 | **W_adh,CC·LLZO ≈ 1–10 J m⁻²** (Cu · Ni) · *"upper bound of the true values"* | 본문 p.5 · SI p.5 · p.10 [인쇄] |
| 소성 보정 전 상한 G = P(1−cos φ) | **Cu ≈ 69 · Ni ≈ 32 J m⁻²** | [우리 산술 · §6-2] |
| 비교 기준 (저자) | 원자 규모 계면 (표면 에너지 추정 ref 24) **< 1 J m⁻²** | p.5–6 [인쇄] |

### 3f. 모형 산출 (`Fig. 5b` · 식 (2)–(4))

| 양 | 값 | 출처 |
|---|---|---|
| r0 곡선 | W = 1 · 10 · 100 J m⁻² × η_nuc 0–5 mV | `Fig. 5b` [인쇄] |
| "Approximate experimental region" 상자 | η_nuc ≈ **2.4–4.5 mV** · r0 ≈ 1–6 × 10⁻⁷ m (1 과 10 J m⁻² 곡선 사이) | `Fig. 5b` figure-read ≈ |
| 곡선 재현 | V̄_Li = 13.0 cm³ mol⁻¹ 로 식 (3) 을 풀면 세 곡선이 그림과 맞는다 (예: 10 J m⁻² · 1 mV → 2.7 µm) | [우리 산술] |
| 저자 문장 | *"assuming ~1 J m⁻² … critical radii are in the micron range for several mV"* | p.6 [인쇄] — 1 J m⁻² 면 2–5 mV 에서 **54–135 nm** (§10) |
| 압력 과전압 | η ≈ V̄_Li p / F · 4 MPa → **≈ 0.5 mV** | p.6 [인쇄] · 0.54 mV 재현 [우리 산술] |
| Li 항복강도 | **< 1 MPa** (Masias 2019, ref 28 인용) | p.4 [인쇄] |

### 3g. 임계 전류밀도 (`Fig. S5` · SI p.11 · 25 °C)

| 양 | 값 | 출처 |
|---|---|---|
| 방식 | 25 µm (5 mAh cm⁻²) in situ Li 를 먼저 만든 뒤 반주기 0.25 mAh cm⁻² (≈ 1 µm) · **in situ Li 쪽에 도금할 때만** 전류 증가 · Li 원 쪽 도금은 0.05 고정 | SI p.11 [인쇄] |
| 전류 계단 (in situ Li 쪽) | 0.05 → 0.1 → 0.2 → **0.3 mA cm⁻² 에서 단락** (≈ 29.5 h) | `Fig. S5` figure-read ≈ · SI p.11 [인쇄] |
| 단계별 전위 | ≈ −0.021 (0.05) · −0.032 ~ −0.035 (0.1) · −0.071 V (0.2) → 0.3 에서 −0.113 V 찍고 붕괴 | `Fig. S5` figure-read ≈ |
| in situ Li CCD | **0.3 mA cm⁻²** vs 같은 조건 > 100 µm Li 박 대칭셀 **≈ 1 mA cm⁻²** | SI p.11 · 본문 p.7 [인쇄] |
| 저자 가설 두 개 | ① CC/LLZO 계면이 Li/LLZO 보다 거칠다 → 응력·이온 흐름 집중 ② 25 µm Li 의 종횡비 → 크기 의존 Li 역학 (refs S9–S11) | SI p.11 [인쇄] |

### 3h. 풀셀 (`Fig. 6` · `Fig. S6` · `Fig. S7`)

| 양 | 값 | 출처 |
|---|---|---|
| 구성 | Cu (10 µm) 적층 LLZO (700 °C Ar 열처리) · 상용 주조 NCA 전극 (≈ 3 mAh cm⁻² · 기공 ≈ 35 %) 에 PEO-LiTFSI 함침 (4.2 MPa · 80 °C · 수 시간) | p.8 [인쇄] |
| PEO-LiTFSI | 상온 ≈ 1 × 10⁻⁶ S cm⁻¹ → 60 °C 운전 · PEO/LLZO 계면 < 200 Ω cm² (상온, ref 30) | p.7 [인쇄] |
| 형성 | NCA 의 Li 를 Cu 위에 0.05 mA cm⁻² 로 도금 (Methods: **80 °C**) · 가용 3 mAh cm⁻² 중 **2.7 mAh cm⁻² (≈ 13.5 µm)** | p.7 · p.8 [인쇄] |
| 순환 | 60 °C (± 3 °C) · C/10 = **0.27 mA cm⁻²** · 4.2–3.0 V · CC-CV (4.2 V 1 h) · EIS 10 사이클마다 | p.7 · p.8 [인쇄] |
| 첫 방전 | 0.75 mAh cm⁻² (본문) · `Fig. 6a` 곡선 끝 ≈ 0.745 · `Fig. 6b` 첫 점 0.787 | p.7 [인쇄] · figure-read ≈ (벡터) |
| 방전 용량 추이 | 0.787 (1) · 0.768 (10) · 0.727 (20) · 0.632 (30) · 0.510 (40) · **0.494 (50)** — 최대 0.856 (13) | `Fig. 6b` `figure-read ≈ (벡터)` |
| 충전 용량 | 0.629 (1) → 0.481 (50) = −23.5 % | `Fig. 6b` `figure-read ≈ (벡터)` |
| 저자 '≈ 25 % 감소' | 충전 용량 기준과 맞다 · 방전 기준은 −37 % | p.7 [인쇄] vs 판독 (§10) |
| CE | 125.7 % (1) · 110.3 (2) · 105.7 (3) · 107.4 (4) · 104.0 (5) · 6–50 사이클 평균 **101.2 %** (91.9–104.3 · 45 중 10 개 < 100 %) | `Fig. 6b` `figure-read ≈ (벡터)` |
| 50 사이클 누적 (방전 − 충전) | ≈ 0.55 mAh cm⁻² ≈ Li 저장분 2.7 의 ≈ 20 % | [우리 산술 · 벡터 판독 합] |
| 셀 임피던스 | ≈ 90 (1 사이클) → ≈ 200 Ω cm² (50) · 저주파에서만 → 내부 계면 (PEO/LLZO 또는 PEO/NCA) | p.7 [인쇄] |
| 80 °C · 0.05 mA cm⁻² (`Fig. S6`) | 본문 *"~2.4 mAh cm⁻²"* · 판독: 형성 ≈ 2.8 · 방전 ≈ 2.29 → 2.22 → 2.13 (3 사이클) | p.7 [인쇄] · figure-read ≈ |
| 대조 Cu/LLZO/Li 박 셀 (`Fig. S7`) | in situ 2.7 mAh cm⁻² 형성 · 0.85 mAh cm⁻² 를 60 °C C/10 로 50 사이클 · 분극 ≈ ± 0.011 V · 임피던스 ≈ 21–40 Ω cm² 불변 · CE 100 % · 무퇴화 | SI p.8 [인쇄] · figure-read ≈ |
| PEO 산화 가설 | ≈ 3.8–4.0 V 이상 PEO 분해 → 임피던스 증가 · 용량 감소 (refs 31–36) | p.7 [인쇄] |

