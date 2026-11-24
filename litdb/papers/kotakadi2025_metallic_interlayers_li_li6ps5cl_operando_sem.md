<!-- digest 표준 양식 (paper-level STANDALONE). 2026-11-25 (KST) 첫 작성 — 병렬 큐레이터 배치 2026-11-25 #1 (litdb/_curation/batch_2026_11_25).
     ① 크롭 29장 (본문 그림 6 + 표 1 · SI 그림 17 + 표 5) 중 그림 23장을 다 봤다 — 원해상도 16장 (본문 6장 전부 + SI S2 · S7 · S8 · S9 · S10 · S11 · S12 · S15 · S16 · S17)
        + 축소 접촉 시트 7장 (S1 Nyquist · S3–S6 문헌 상평형도 · S13 · S14 셀 부품 · 조립 도식 — 백지 크롭이 아닌지 · 내용 확인용). 표 6장은 PDF 글자층으로 읽었다.
     ② 숫자를 읽은 곳: Fig. 5A · Fig. 6A,B · Fig. S9 는 색으로 곡선을 픽셀 판독 · Fig. S2 위 · 아래 축 눈금은 픽셀로 쟀다 · Fig. 3 · Fig. 4 축척 막대는 픽셀.
        Data S1 (VAMAS .vms 셋) 은 CasaXPS 맞춤 성분 줄을 글자로 읽었다 (§3g · §17). 영상 (Videos S1–S7) 은 안 왔다.
     ③ 이 논문은 원자단위 계산을 하지 않는다 (부피 = Materials Project 구조 · ΔG = 핸드북). 기법 태그는 XPS 하나.
     ④ 우리 점착 (W) 값은 싣지 않는다 — 위치만 (§7 · §11). -->

# Impact of metallic interlayers at the lithium-Li6PS5Cl solid electrolyte interface — Kotakadi et al. (*Joule* **2025**, 9, 102175)

> slug `kotakadi2025_metallic_interlayers_li_li6ps5cl_operando_sem` · DOI `10.1016/j.joule.2025.102175` · type `exp 전용 (operando SEM (BSE · SE) · 3 전극 EIS · 정전류 · CTTA · in situ XPS (가상 전극 도금) — 원자단위 계산 0 · 부피는 Materials Project 구조 · ΔG 는 핸드북)` · PDF `litdb/inbox/kotakadi2025_metallic_interlayers_main.pdf` (본문 16 pp = 그림 초록 1 + 저널 쪽 1–15) + `litdb/inbox/kotakadi2025_metallic_interlayers_SI.pdf` (SI 16 pp · Fig. S1–S17 · Table S1–S5) + 원자료 `litdb/inbox/kotakadi2025_metallic_interlayers_dataS1_xps/{Mg,Ag,In}_XPS.vms` (Data S1) · digested `2026-11-25` · status ✅ · 태그 **[외부]**

> elements: Li, P, S, Cl, Bi, In, Ag, Mg
> methods: XPS

> **저자**: **Souhardh Kotakadi** (Oxford 재료과) · Jack Aspinall (Oxford) · Matthew Burton (Oxford + Faraday Institution) · Yi Liang (Oxford) · Yuichi Aihara (Nissan Research Centre, Nissan Motor) · **Mauro Pasta\*** (Oxford + Faraday Institution · 교신 · lead contact `mauro.pasta@materials.ox.ac.uk`). Jeff Sakamoto 는 저자가 아니다 (refs 23 · 29 로 인용만).
>
> **서지**: 투고 2025-04-18 · 수정 2025-08-18 · 수락 2025-09-29 · 온라인 2025-10-28 · 권호 2025-11-19 · *Joule* **9**, 102175 · OA (CC BY 4.0) · 자금 Nissan Motor (S.K. · J.A. · M.P.) · Faraday Institution FIRG056 (M.B. · M.P.) · Henry Royce Institute (EPSRC EP/R010145/1) · **이해 상충: S.K. · J.A. · M.B. · M.P. 가 이 내용의 특허 출원을 준비 중** (p.13) · 참고문헌 본문 57 + SI 12 · 미심사 판 ChemRxiv `10.26434/chemrxiv-2025-bfts2` (같은 저자 6 명 · Crossref 확인) · 랩 표준 표기 *Joule*, 9, 102175 (2025).
>
> **계보**: [Aktekin23] (*Nat. Commun.* 14, 6946 · CTTA 원전 · ref 12) · [Narayanan22] (*Nat. Commun.* 13, 7237 · 가상 전극 in situ XPS · ref 13) · [Burton25] (*Nat. Commun.* 16, 9304 · 아지로다이트 SEI 의 P · ref 14) · [Aspinall24Mg] (*Nat. Commun.* 15, 4511 · Li–Mg 합금 음극 · ref 37) · [Aspinall24In] (*ACS Energy Lett.* · Li–In 미세구조 · ref 41) · [Lee20AgC] (*Nat. Energy* 5, 299 · Ag–C · ref 30 · `lee2020_silver_carbon_composite_anode_all_solid_state_li_metal.md`) · [Haslam25] (ref 23 · `haslam2025_alloying_interlayers_li_morphology_microstructure_anode_free.md`) · [Sandoval23] (*Joule* 7, 2054 · ref 28 · 같은 배치 다른 에이전트) → **본 논문** (같은 Li₆PS₅Cl 위에서 Bi · In · Ag · Mg 100 nm 층을 **operando SEM 으로 위에서 보며** 리튬화 · 도금 · SEI 를 한 줄로 잇는다).
>
> **본 digest 에서 실제로 본 그림 (2026-11-25)**: 그림 23장 **전부** — 원해상도 **16장** (본문 6장 전부 `Fig. 1`–`Fig. 6` + SI `Fig. S2` · `S7` · `S8` · `S9` · `S10` · `S11` · `S12` · `S15` · `S16` · `S17`) + **축소 접촉 시트로 7장** (`Fig. S1` Nyquist · `S3`–`S6` 문헌 상평형도 재수록 · `S13` · `S14` 셀 부품 사진 · 조립 도식 — 백지 크롭이 아닌지와 내용만 확인 · 숫자는 안 읽었다). 표 6장 (`Table 1` · `Table S1`–`S5`) 은 PDF 글자층으로 읽었다. 영상 (도금 Videos S1–S7 · 번호 없는 리튬화 영상) 은 **안 왔다** — `Fig. 3` · `Fig. 4` 스냅숏으로만 읽었다.
> 그림에서만 읽은 값은 **`figure-read ≈`**, 논문 값으로 우리가 계산한 값은 **`우리 산수`**, Data S1 원자료에서 읽은 값은 **`Data S1`** 로 표시했다. 쪽은 저널 쪽 (p.1–15 · PDF 쪽 − 1) · SI 는 SI PDF 쪽 (SI p.N).
>
> 🎤 talk 역링크: `litdb/talks/` 의 인입 대기열 (그 표가 있는 유일한 파일 `lee2026_skku_mlip_materials_design.md`) 에 이 논문은 없다 (2026-11-25 grep).

---

## 0. 이 digest 를 읽는 법

**우리 계 그대로다** — SE 는 상용 Li₆PS₅Cl (MSE Supplies · D50 ≈10 µm · 우리 comp1 조성) 이고, 그 위에 Bi · In · Ag · Mg 를 **100 nm** 올렸다 (Bi · Ag · Mg = RF 마그네트론 스퍼터 · In = 열증착). 같은 층을 다섯 종류 셀에 넣었다.

| 셀 | 구성 | 압력 · 조건 | 무엇을 봤나 |
|---|---|---|---|
| ① operando SEM 셀 | (층) \| LPSCl 90 mg \| InLi 분말 50 mg \| In 박 + SUS 10 µm · 윗면 = Cu 망 + SUS 고리 | **적층압 ≈0** (*"effectively no pressure"*) · 0.2 mA cm⁻² · 10 h = 2 mAh cm⁻² · 상대극 InLi (+0.622 V 보정) | 층 리튬화 (BSE · `Fig. 3`) → Li 도금 형태 (SE · `Fig. 4` · `Fig. 5`) |
| ② 3 전극 셀 (EIS · 주기 리튬화) | (층) \| LPSCl 150 mg (가운데 InLi 망 기준극) \| Li 박 200 µm | 압력 미기재 · 9.61 µA cm⁻² × 30 min 펄스 + PEIS | 접촉 면적 (`Table 1` · `Fig. 2C`) · operando 전위 곡선 대조 (`Fig. S7`) |
| ③ 사이클 반쪽 셀 | (층) \| LPSCl \| InLi–In (3 전극) | **5 MPa** · 0.1 mA cm⁻² · 1.5 mAh cm⁻² · 박리 0.1 V 끝 | 핵 과전압 (`Fig. S8`) · 전압 · CE (`Fig. S16` · `S17`) |
| ④ CTTA 셀 | (층) \| LPSCl \| Li 박 200 µm | 압력 미기재 · 15.56 µA cm⁻² × 6 min (1.56 µAh cm⁻²) 펄스 → 50 mV 까지 OCV | SEI 의 Li 소모 (`Fig. 6A,B` · `Fig. S9`) |
| ⑤ in situ XPS | Cu 망 \| LPSCl 5 mm \| Li 박 \| Cu 박 · 금속은 **XPS 안에서 Ar 이온빔 스퍼터 (목표 ≈10 nm)** | 진공 10⁻⁷ Pa · 전자 중화기 빔으로 '가상 도금' | 금속\|SE 반응 산물 · 도금 뒤 변화 (`Fig. 6E–H` · `Fig. S10`–`S12` · Data S1) |

저자 메시지는 넷이다. **(1)** 층을 SE 위에 증착하면 CC 위에 증착한 것보다 이중층 용량 (CPE Q) 이 **35 배** = 전기화학 접촉 면적이 35 배 (p.3 · `Table 1`). **(2)** 고용체를 만드는 Ag · Mg 는 고르게 리튬화되고 멀쩡하며, 금속간 화합물을 만드는 Bi 는 LiBi → Li₃Bi **61 %** 팽창으로 들려 깨진다. In 은 금속간 화합물인데도 멀쩡하다 (52 % · 무른 In · 증착 방울 꼴). 낮은 D 상 → 높은 D 상 전이에서 리튬화가 불균일해진다 (p.4–6). **(3)** In · Ag · Mg 위에서 Li 는 고르게 둥근 방울로 자라고, Ag 가 가장 잘게 (1.5 mAh cm⁻² 에서 481 개) 자란다 (p.8 · `Fig. 5`). **(4)** 전자가 통하는 층은 접촉이 넓어 **SEI 를 더 키운다** (CTTA) — Mg 는 예외로 느리고, XPS 로 보면 In · Ag 의 금속 황화물은 Li 가 오면 Li₂S 로 바뀌지만 MgS 는 남아 부동태를 만든다 (p.9–10).

> ⚠⚠ **operando 셀은 무가압이고 윗면만 본다.** 형태 (방울 · 덮임 · 크기 분포) 는 0 MPa · 열린 표면의 결과다 (저자도 p.8 에 적음). 층 **아래** (층\|SE 사이) 에서 자라는 Li 는 Bi 처럼 층이 깨져 들리지 않으면 안 보인다 — 저자: *"planar growth through the thickness of the interlayer would not be visible in this imaging mode"* (p.8).

> ⚠⚠ **조건당 셀 하나** (n = 1) · 반복 · 오차 막대가 없다. In 만 증착법 (열증착 · ≈1 µm 방울) 이 달라 '금속' 과 '막 꼴' 이 같이 바뀐다 (저자 p.6). XPS 막 (≈10 nm · 이온빔 · Bi 없음) 은 셀 막 (100 nm · RF) 과 다르다.

> ⚠⚠ **CTTA 의 'Mg 는 SEI 가 느리다' 는 정규화에 달려 있고, 그 정규화가 SI 로 재현되지 않는다** (§10-①). 원자료 `Fig. S9` 에서 Mg 셀은 모든 시각에 **가장 많이 · 가장 빨리** Li 를 잃는다. 이 digest 에서 가장 중요한 경고다.

---

## 1. 한 줄 요약

Li₆PS₅Cl 위 100 nm 금속 층은 상도가 고용체냐 (Ag · Mg) 금속간 화합물이냐 (Bi · In) 에 따라 리튬화 꼴이 갈린다 — Bi 는 LiBi → Li₃Bi (61 %) 에서 들려 깨지고 Li 가 층 **밑**에서 기둥으로 자라며 첫 사이클 뒤 단락하고, In · Ag · Mg 는 멀쩡하고 Li 가 **위**에 고르게 방울로 자란다 (0 MPa operando SEM · 핵 과전압 none 17.8 → Bi 10.8 · In 4.6 · Ag 2.0 · Mg 0 mV `figure-read ≈`). 층을 SE 위에 두면 CC 위보다 접촉이 35 배 (CPE Q) 넓어 전류는 고르게 퍼지지만 **SEI 도 커진다** (CTTA 180 h ≈0.09 대 층 없음 ≈0.034 mAh cm⁻² `figure-read ≈`). 저자는 Mg 가 MgS · 인화물로 부동태 SEI 를 만들어 이 손실을 줄인다고 보지만, 그 근거 (CTTA 정규화 · XPS 0.2 eV 차) 는 이 digest 가 다시 읽어 보면 약하다 (§10).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 계 | 상용 Li₆PS₅Cl 냉간 압착 펠릿 (10 mm · 430 MPa) 위 Bi · In · Ag · Mg 100 nm (AFM 으로 두께 확인) · 비교: 같은 Bi 를 SUS 박 (CC) 위에 증착 (*functionalized CC*) · 층 없음 |
| 왜 | 무음극 (저자 용어 *anode-less* · *lithium-less*) 셀은 첫 도금 효율 · 형태가 수명을 정한다. 합금 층이 도금을 고르게 한다는 보고는 많지만 대부분 산화물 SE 이거나 사후 · 간접 관찰이라 **황화물에서 합금 상 생성 · Li 확산 · 층의 기계 건전성이 어떻게 도금과 SEI 를 정하는지** 모른다 (p.2) |
| 질문 | ① 층을 어디 (SE 위 · CC 위) 두느냐가 접촉 면적을 얼마나 바꾸나 ② 상도 꼴 (고용체 · 금속간) 이 리튬화 균일성 · 파괴 · 도금 형태를 어떻게 정하나 ③ 전자가 통하는 층이 SEI 성장을 키우나 · 층 화학이 SEI 를 바꾸나 |
| 고른 금속 | Mg — α-Mg (≤15 % Li) · β-Li (≥31 % Li) 고용체 둘 (`Fig. S6`) · Ag — α-Ag 에 Li ≤45 % 고용 · β-Li 에 Ag ≤1 % · 그 사이 금속간 화합물은 결정 구조가 비슷하고 1–5 % 고용 범위 (`Fig. S5`) · Bi — 금속간 화합물 둘 (LiBi · Li₃Bi) (`Fig. S3`) · In — 금속간 화합물 최대 8 개 (`Fig. S4`) · Li₃Bi 와 InLi 는 빠른 Li 이온 전도 상 (p.2) |
| 연구 유형 | 실험 전용 — operando SEM · 3 전극 EIS · 정전류 · CTTA · in situ XPS. 계산은 없다 (MP 결정 구조로 부피 · 핸드북 ΔG_f 로 치환 반응 ΔG) |
| 셀 수 | 조건당 하나 (반복 · 오차 막대 없음) |
| 데이터 | *"All data used in this study are included as supplemental data"* (p.13) — Data S1 (XPS 원자료) 은 받았다 · 'Sup2' 엑셀 (40 MB · 이름 미상) 과 영상은 안 왔다 |

---

## 3. 핵심 수치 총정리 ★

### 3a. 재료 · 셀 (p.11–13)

| 항목 | 값 |
|---|---|
| SE | Li₆PS₅Cl (MSE Supplies · D50 ≈10 µm) |
| 층 | Bi · Ag · Mg RF 스퍼터 (MBraun MB EVAP · Ar 글러브박스 · 50 mm 표적 · Bi 28 W · Ag 58 W · Mg 30 W · 기저 5 × 10⁻⁵ mbar · Ar 10 sccm · 예비 스퍼터 ≥2 min · 기판 33 rpm) · In 열증착 (Mo 보트 · 6 Å s⁻¹ · 녹는점 156 °C 라 상온 스퍼터 막이 거칠어서) · **전부 100 nm** (AFM) |
| operando 셀 펠릿 | LPSCl 90 mg · PEEK 10 mm · 430 MPa 1 min → InLi 볼밀 분말 50 mg · 같은 압력 5 min → In 박 0.127 mm + SUS 10 µm · 80 MPa 10 s · 층 증착 때 PEEK 를 Kapton 으로 가림 |
| 전기화학 셀 펠릿 | LPSCl 75 mg · Macor 10 mm · 430 MPa 5 min → 같은 스퍼터 |
| 3 전극 | Riegger 형 망 기준극 (InLi 입힌 망) · 둘로 자른 PEEK 몸통 · 위에 LPSCl 75 mg 더 (370 MPa 5 min · 합계 150 mg) · Li 박 200 µm (10 mm · 80 MPa 10 s) · OCV 10 h (주기 EIS) · 주기 리튬화 12.25 µA (본문 9.61 µA cm⁻²) × 30 min (4.81 µAh cm⁻²) + OCV 10 min + PEIS (10 mV · 1 MHz–50 mHz) |
| 사이클 셀 | 상대극 InLi 분말 80 mg (370 MPa 5 min) + In 박 (80 MPa 10 s) · 0.1 mA cm⁻² × 15 h = 1.5 mAh cm⁻² 도금 → 같은 전류로 0.1 V (vs Li⁺/Li) 까지 박리 · **5 MPa** (p.8) |
| operando SEM | Tescan Mira3 FEG-SEM (MBraun 글러브박스로 열림) · Biologic SP150 · KF40 어댑터 + 4 핀 단자 · 0.2 mA cm⁻² × 10 h = 2 mAh cm⁻² · 밝기 · 대비 고정 · 매크로로 일정 간격 · 빔 ≤5 pA (최고 배율 66 × 66 µm 에서 ≈0.1 µA cm⁻² · 인가 전류의 ≤0.05 %) · 10 kV (`Fig. S15` 데이터 막대) |
| 영상 분석 | Fiji (ImageJ) + Meta Segment Anything Model (refs 54 · 55) |
| CTTA | Aktekin 2023 방식 · 15.56 µA cm⁻² × 6 min = 1.56 µAh cm⁻² 펄스 → OCV 를 **50 mV** 까지 (= 도금 Li 가 다 소모) → 반복 · Li 박 200 µm 상대극 · 정규화 = 0 V 에 닿기 전 전하 (합금) 를 뺀다 (`Table S3`) |
| in situ XPS | PHI VersaProbe III · Al Kα 1486.6 eV (25 W · 15 kV) · 10⁻⁷ Pa · 통과 에너지 224 (전체) / 55 eV (고분해) · 펠릿 LPSCl 30 mg (5 mm · Cu 망과 500 MPa 5 min) · 반대쪽 Li 박 (4.7 mm · 500 µm 압연) + Cu 박 (60 MPa) · 금속 = XPS 안 Ar 이온빔 (4 kV · 3 × 3 mm) 으로 표적 (In 박 · Ag 박 · Mg 조각) 을 스퍼터 · **목표 ≈10 nm** · 스퍼터와 측정 번갈아 · 가상 도금 = BaO 중화기 전자빔 (5 mm) · CasaXPS · Shirley / offset Shirley 배경 · 비대칭 LA 선꼴 (In 3d5/2 · Ag 3d5/2 비대칭 · Mg 1s 대칭) · **Cl 2p3/2 = 198.5 eV 로 전하 보정** |

### 3b. 접촉 면적 — 증착 자리 (p.3–4 · `Table 1` · `Fig. 2C`)

| 배치 | SE 벌크 저항 (Ω) | 이중층 CPE Q (µF s^(α−1)) | α |
|---|---|---|---|
| Bi on CC (*functionalized CC*) | 34.34 | **4.637** | 0.7899 |
| Bi on SE (*interlayer*) | 33.56 | **163.9** | 0.7675 |

- 등가 회로 = R_bulk + CPE 직렬 (막힌 전극 · `Fig. 2C` 삽입) · 10 mm 펠릿 · 3 전극. Q 비 **35.3** → *"suggesting the contact area is 35 times greater in the interlayer case"* (p.3).
- `Fig. 2C` Bode (실독): 고주파 평탄 log|Z| ≈1.53 (≈34 Ω · 둘 같음) · 가장 낮은 주파수 (≈0.05 Hz) 에서 log|Z| ≈5.7 (CC) 대 ≈4.1 (SE) `figure-read ≈` → |Z| 비 ≈40.
- `우리 산수` (Brug 식 · 막힌 전극 C = Q^(1/α) R^((1−α)/α)): C_eff ≈0.45 µF (CC) 대 ≈34 µF (SE) → **비 ≈75**. α 가 달라 Q 비 ≠ 용량 비다 (§10-④). 기하 면적 (0.785 cm²) 으로 나누면 ≈0.58 대 ≈43 µF cm⁻².

### 3c. 리튬화 — operando BSE (`Fig. 3` · `Fig. S2` · `Fig. S7` · `Table S2` · p.4–6)

| 층 | 전위 곡선 (operando · +0.622 V 보정 · `figure-read ≈`) | BSE 영상 | 저자 해석 |
|---|---|---|---|
| **Bi** | 시작 1.4 V (본문 · `Fig. 3A` 축 위 끝) / ≈1.7 V (`Fig. S2a`) → **0.78 V** 평탄 (≈0.011–0.032 mAh cm⁻²) → **0.74 V** 아래 평탄 (≈0.033–0.07) → 0 V (h ≈0.097–0.100) | E→F 고르게 어두워짐 · G 몇 곳에서 Li₃Bi 불균일 핵 + 가운데서 균열 · H 균열이 전체로 · 들려 깨짐 | Bi → LiBi 는 고르게 (0.78 V 2 상) · LiBi → Li₃Bi 는 높은 D 상 (Li₃Bi D ≈10⁻⁴ · 단위 오기) 이 먼저 자라 불균일 · **61 % 팽창 → 박리 · 위로 휨 · 파괴** · 층이 다 리튬화되기 전에는 Li 도금 없음 |
| **In** | 1.0 V → ≈0.55–0.47 V 어깨 → j ≈0.011 (≈0.3 V) → **0 V ≈0.023** → k ≈0.040 · l ≈0.079 · 뚜렷한 평탄 없음 | I ≈1 µm In 방울 (증착 꼴) · J · K 점점 Li 많은 상 · K 에서 Li 핵 · L 큰 검은 Li 덩어리 | InLi (D 5.5 × 10⁻⁷ cm² s⁻¹) 가 먼저 불균일하게 생기고 바로 Li 많은 상 · 다 리튬화되기 전에 Li 전위 · Li 핵 · 리튬화와 도금이 나란히 · 멀쩡 (최대 단계 팽창 In → InLi 52 % · 무른 In) |
| **Ag** | 0.40 V → 급강하 → **≈0.055 V** 작은 평탄 (≈0.02–0.045) → **≈0.015 V** (≈0.06–0.085) → ≈0 V (≈0.10–0.125) → o ≈0.123 · p ≈0.236 | M→O 점진적 · 고른 밝기 변화 · P 고른 Li 방울 | 상이 바뀔 때마다 층 전체가 고르게 (결정 구조 비슷 · D 차 작음) · O 에서 γ 고용체 (Li ≥ 9 Ag) · Li 플럭스가 고용 속도를 넘어 P 에서 도금 · 파괴 · 박리 없음 · Li 는 층 **위**에 · 리튬화 용량 **0.22 (Ag) 대 0.1 mAh cm⁻² (In)** · ⚠ 본문은 평탄을 *"ordered α-Ag at 0.56 V and LiAg at 0.2 V"* 라 적었다 (§10-⑦) |
| **Mg** | 0.22 V → 급강하 (α-Mg 희석 · ≈0.002) → 0 V 를 살짝 밑돌며 ≈ −0.003 → −0.015 V 로 천천히 → r ≈0.038 · s ≈0.071 · t ≈0.084 | Q→R 고르게 · R→S β 상 불균일 핵 · 자람 · S→T 점점 어두워짐 + 도금 시작 | α-Mg (D 낮음) → β-Li (D 가 Li 따라 커짐 → 양의 되먹임 · ref 37) · 상 변화 하나 · 둘 다 고용체 → 부피가 천천히 · 파괴 없음 |

- 시야 (축척 막대 픽셀): `Fig. 3` 패널 ≈54 µm · `Fig. 4` 패널 ≈36 µm `figure-read ≈` (방법의 '최고 배율 66 × 66 µm' 보다 좁다 — 잘라 낸 패널로 보인다).
- 부피 (`Table S2` · MP 결정 구조 · 원자당 cm³ mol⁻¹): Bi 21.31 → BiLi 28.67 (+35 %) → BiLi₃ 46.05 (처음 대비 +116 % · 단계 +61 %) · In 15.71 → InLi 23.83 (+52 %) → In₄Li₅ 26.00 (+9 %) → In₂Li₃ 28.40 (+9 %) → InLi₂ 33.26 (+17 %) → InLi₃ 43.06 (+29 %) → In₃Li₁₃ 57.96 (+35 % · **처음 대비 +269 %**).
- `Fig. S2` (캡션 · SI p.3): 위 가로축에 '층 평균 Li 원자 %' 를 달고, *"Li₃Bi should start to nucleate beyond 50 at % Li. However, we see the Li₃Bi/LiBi potential plateau much earlier at ∼25 at % Li"* · In 은 *"highly lithiated phases are formed at very low average compositions"* 로 불균일성을 주장한다. ⚠ 그 위 축은 네 금속 모두 **같은 환산 (Li/M = 1 ↔ 0.100 mAh cm⁻²)** 을 쓴다 (눈금 픽셀 측정 · §10-②).
- `Fig. S7` (3 전극 주기 리튬화 · 실독 · `figure-read ≈` · 펄스 주기 ≈1 h 가정): Bi 2.25 V 시작 → ≈0.8 V 평탄 하나 (≈4.3–13.5 h · ≈9 펄스 ≈0.043 mAh cm⁻²) → ≈14 h 에 0 V · In 1.75 V → **≈0.6 V 평탄** (≈1.6–4 h · ≈2–3 펄스) → ≈9 h 에 0 V · Ag 2.0 V → ≈10 h 에 ≈0.1 V → ≈20 h 에 ≈0 V · Mg 1.25 V → ≈1.5 h 에 ≈0.1 V → ≈4.5 h 에 ≈0 V. 저자: *"confirming consistent potential profiles"* (p.4).

### 3d. 도금 형태 — operando SE (`Fig. 4` · `Fig. 5` · p.6–8)

- 찍은 시점: 도금 0.5 · 1 · 1.5 mAh cm⁻² (`Fig. 4` · 같은 자리 추적 — 패널마다 같은 표지 입자가 보인다).
- **Bi** (`Fig. 4A–C`): 층 밑에서 두꺼운 Li 기둥이 자라 층을 들어 올리고 깨뜨린다 · 층 위에는 Li 핵이 없다 (p.6–8). 실독: 깨진 판 (밝은 점이 박힌) 이 들리고 오른쪽 절반을 매끈한 어두운 덩어리가 채운다 (B · C).
- **In · Ag · Mg** (`Fig. 4D–L`): 표면 전체에 고르게 핵 → 둥근 방울로 자람 · 첫 핵생성 뒤 새 핵은 적다 (p.8). 실독: In 방울 ≈3–6 µm (1.5) · Ag 0.5 에서 이미 빽빽한 작은 덩어리 → 1.5 에서 ≈3–5 µm 가 거의 다 덮음 · Mg 방울 ≈2–5 µm · 표면이 거칠고 잡음이 많다.
- 덮임 (`Fig. 5A` · 픽셀 판독 `figure-read ≈`):

| 도금량 (mAh cm⁻²) | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.8 | 1.0 | 1.5 |
|---|---|---|---|---|---|---|---|---|---|
| In (%) | ≈3 | ≈18 | ≈37 | ≈53 | ≈65 | ≈74 | ≈86 | ≈92 | ≈96.5 |
| Ag (%) | ≈1 | ≈1 | ≈4 | ≈26 | ≈45 | ≈58 | ≈77 | ≈84 | ≈94.6 |
| Mg (%) | ≈1 | ≈3 | ≈11 | ≈21 | ≈32 | ≈41 | ≈59 | ≈64 | ≈77.6 |

  본문: 도금 시작 In ≈0.05 · Ag ≈0.25 · Mg ≈0.1 mAh cm⁻² (p.8) · 시작 뒤 덮는 속도는 Ag > In (가장 가파른 기울기 `figure-read ≈`230 대 ≈210 % per mAh cm⁻² — 10 % 남짓 차) · Mg 는 같은 덮임에 더 많은 전하가 든다 (α/β D 차 · β 고용 범위).

- 크기 분포 (`Fig. 5B` · 1.5 mAh cm⁻²): 입자 수 **Ag 481 · In 444 · Mg 321** · Ag · Mg 대부분 1–3 µm · In 대부분 3–4 µm (p.8) · 실독: 봉우리 Mg ≈20.5 % @ ≈1.7 µm · Ag ≈17 % @ ≈1.7–2.3 µm · In ≈19.5 % @ ≈3.1 µm · 꼬리 ≈10–12 µm `figure-read ≈`. 계수한 면적 · 분할 문턱은 미기재.
- 저자 해석 (p.8): Ag · Mg 의 잘고 고른 분포 = Li\|고용체 합금 계면 에너지가 낮다 (격자 불일치 작음) · In 은 InLi 가 먼저 도금을 시작하고 층에 들어가는 Li 가 적어 같은 용량에 방울이 크다.
- 고용체의 대가 (p.8): Ag · Mg 는 합금 금속이 Li 쪽으로 퍼져 평평한 층이 안 남고, 박리 뒤 처음 층을 다시 못 만들 수 있다 · In 은 마지막 금속간 상이 Li 와 평형이라 조성이 안 바뀐다 → *"intermetallic-forming interlayers may offer improved long-term stability if the lithium-rich phases do not hinder lithium transport"*.
- 압력 (p.8): 형태는 0 MPa 값 · Li 경도 ≈2 MPa (ref 46) · 크리프는 그 아래 → 가압 셀이면 방울이 눌려 평평한 막.

### 3e. 전기화학 — 핵 과전압 · 사이클 (`Fig. S8` · `Fig. S16` · `Fig. S17` · p.8–9)

- 핵 과전압 (`Fig. S8` · 3 전극 · `figure-read ≈`): **none ≈17.8 · Bi ≈10.8 · In ≈4.6 · Ag ≈2.0 · Mg 0 mV** (캡션: Bi 10 mV · Mg 는 서서히 내려갈 뿐 스파이크 없음 · In · Ag · Mg 는 스파이크가 없다고 적었다).
- 사이클 (5 MPa · 0.1 mA cm⁻² · 1.5 mAh cm⁻² · InLi–In 상대극): Bi 는 첫 사이클 뒤 실패 (2 째 도금 ≈8.3 h 에 단락 · `Fig. S17b`) · 층 없음은 3 째 도금 ≈3.6 h 에 단락 (`Fig. S17c`) · 캡션: 무층 셀은 보통 1–2 사이클에 단락.
- 쿨롱 효율 (`Fig. S16f` · `figure-read ≈`):

| 사이클 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| none | ≈95 | ≈87 | (단락) | — | — |
| Bi | ≈81 | (단락) | — | — | — |
| In | ≈83 | ≈84 | ≈80 | ≈73 | ≈65 |
| Ag | ≈85 | ≈92 | ≈91 | ≈86 | ≈72 |
| Mg | ≈93 | ≈86 | ≈82 | ≈69 | ≈61 |

  `Fig. S17a` 박리 끝 시각 (≈17.3 h 시작 · `figure-read ≈`): Bi ≈29.5 · In ≈29.9 · Ag ≈30.2 · Mg ≈31.3 · none ≈31.5 h → 박리량 ≈1.22 · 1.26 · 1.29 · 1.39 · 1.42 mAh cm⁻² (`우리 산수`) = `Fig. S16f` 첫 CE 와 같다.
  본문 (p.8–9): *"The use of silver and magnesium interlayers … results in improved Coulombic efficiencies when compared with the non-interlayer cells"* — ⚠ 첫 사이클은 **층 없음이 가장 높다** (§10-⑧). 캡션 (SI p.13): 첫 CE 손실은 0.1 V 끝에서 합금에 남은 Li 몫 · In · Mg 는 사이클마다 CE 가 내려간다 (박리 문제) · Ag 는 처음 오르다 3 사이클 뒤 같이 떨어진다.

### 3f. SEI — CTTA (`Fig. 6A,B` · `Fig. S9` · `Table S3` · `Table S5` · p.9–10)

| 셀 | `Fig. 6` (정규화) @≈178 h `figure-read ≈` | `Fig. S9` (원자료) @178–180 h `figure-read ≈` | `Table S3` 뺀 전하 (mAh cm⁻²) |
|---|---|---|---|
| none | 0.0345 | 0.0346 | 0 |
| Bi (SE 위) | 0.089 | 0.142 | 0.041 |
| Bi CC | 0.062 (`Fig. 6A`) | 0.089 | 0.053 |
| In | 0.090 | 0.131 | 0.018 |
| Ag | 0.092 | 0.114 | 0.155 |
| Mg | **0.050** | **0.285** (모든 시각에 가장 높다) | 0.024 |

- 본문 (p.9): Bi on SE > Bi CC > none — *"enhanced electronic contact area at the interface promotes greater SEI formation"* · Bi · In · Ag 는 비슷하고 none 보다 훨씬 높다 · Mg 도 늘지만 훨씬 느리다 · CTTA 의 한계: 도금 Li 의 면 분포를 모른다.
- `Fig. S9` 원자료 (실독 · 픽셀): Mg 가 10 h 에 ≈0.15 · 12 h 에 ≈0.17 까지 가파르게 오르고 그 뒤 200 h ≈0.29 · 다른 셀은 처음 몇 h 의 합금 몫 뒤 완만하다.
- ⚠ **`Table S3` 로 `Fig. S9` 를 빼면 `Fig. 6B` 가 안 나온다** (§10-①).
- SEI 크기 (`Table S5` · 정의 그대로): 잃은 용량 **0.09 mAh cm⁻² (180 h)** → 두께 **810 nm** (Aktekin: 1 µAh cm⁻² 당 9 nm) → 저항 **604 Ω cm²** (Alt 2024 SEI 전도도 134 nS cm⁻¹ · 전자 전도 무시) · 본문: Alt 등은 SEI 저항을 10 Ω cm² 아래로 두어야 한다고 본다 (본문은 Ω cm⁻² 로 오기).

### 3g. XPS — 반응 산물 (`Fig. 6E–H` · `Fig. S10`–`S12` · `Table S4` · Data S1 · p.9)

- 본문: 스퍼터하면 금속 황화물이 생긴다 (S 2p 'S–금속' 봉우리가 커진다 · S–PS₄ 감소는 막 두께 탓) · In · Mg 는 Li₂S 와 금속 황화물의 S²⁻ 결합 에너지가 다르다 · In 은 Li 가 In 을 밀어내 Li₂S (원래 Li₂S 자리로 되돌아감) · Ag 는 봉우리가 겹쳐 못 가른다 (같은 기전일 것) · **Mg 는 바로 되돌아가지 않는다** · Mg 는 인화물 (`Fig. 6H`) 과 산화물 (`Fig. S12`) 이 더 많다.
- `Table S4` (핸드북 ΔG_f · kJ mol⁻¹): Li₂S −434 · Bi₂S₃ −140 · In₂S₃ −337 · Ag₂S −40 · MgS −341 → Li 치환 ΔG (금속 황화물 화학식 1 개당): Bi₂S₃ **−1162** · In₂S₃ **−965** · Ag₂S **−394** · MgS **−93** (본문은 이 값을 'ΔG_f' 라 부른다). `우리 산수` S 1 개당: Bi −387 · In −322 · **Ag −394** · Mg −93.
- Data S1 맞춤 성분 (CasaXPS · BE = 1486.6 − KE · Cl 2p3/2 = 198.5 eV 보정 · `Data S1`):

| 시료 · 단계 | S 2p3/2 PS₄³⁻ (eV) | S 2p3/2 '160 eV 성분' (eV · 파일 성분 이름) | 금속 준위 (eV) | 기타 |
|---|---|---|---|---|
| In · 처음 | 161.44 | 160.00 (S 2p2 = Li₂S) | — | Li 1s 55.4 (면적 538) |
| In · 5 / 10 / **40** min | 161.40 / 161.45 / 161.50 | **160.45 / 160.48 / 160.46** (S–In) | In 3d5/2 442.75 / 442.71 / 442.69 (+ In³⁺ 443.5–443.6 · 5 min 15 % → 10 min 6 % → 40 min 0) | P 2p 환원 성분 130.04 · 128.31 (5 min 만 · 22 %) · Li 1s 면적 161 → 115 |
| In · 리튬화 뒤 | 161.40 | **159.90** (Li₂S 로 되돌아감) | In 3d5/2 **441.56** (−1.13) | Li 1s 53.45 + 54.2 (면적 506 + 229) · O 1s 새 성분 527.81 |
| Ag · 처음 | 161.46 | 160.00 ('li2s') | — | — |
| Ag · 5 / 10 / **50** min | 161.42 / 161.41 / 161.41 | **160.03 / 160.03 / 159.96** ('li2s' · 따로 된 S–Ag 성분 없음) | Ag 3d5/2 367.33 / 367.31 / 367.16 | P 2p 맞춤 없음 |
| Ag · 리튬화 뒤 (Eneut-5min) | 161.45 | 160.01 | Ag 3d5/2 **366.17** (−0.99) | — |
| Mg · 처음 | 161.43 | 160.06 (Li₂S) | — | P 2p 131.80 + 129.84 (7 %) |
| Mg · 5 / 10 / 30 min | 161.40 / 161.40 / 161.40 | **160.27 / 160.25 / 160.25** (S–Mg) | Mg 1s 1303.45 / 1303.16 / 1303.03 | P 2p 환원 성분 129.8 · 127.8 → 129.4 · 126.8 → 129.5 · 126.7 (P 2p 면적의 **48 · 57 · 56 %**) · Li 1s (30 min) 54.67 (면적 51) |
| Mg · 리튬화 뒤 | 161.38 | **160.20** (−0.05 만) | Mg 1s 1302.75 (−0.28) | Li 1s 54.68 + 53.91 (면적 35 + 11 = 46 · 30 min 과 같은 수준) · P 2p 신호 없음 |

  ⇒ S–금속 대 Li₂S 위치 차: **In ≈0.45–0.58 eV · Mg ≈0.19–0.21 eV · Ag ≈0.03 eV** (`Data S1`). 세 번째 스퍼터 단계는 Data S1 · `Fig. S10` · `Fig. S11` 이 **40 min (In) · 50 min (Ag)** 인데 `Fig. 6E,F` 는 둘 다 *"30 min sputtering"* 이라 적었다 (Mg 만 30 min · §10-⑨).

### 3h. 우리 산수 (가정 명시 · 논문에 없는 값)

- **100 nm 막의 이론 리튬화 전하** (`Table S1` 질량 Bi 0.098 · In 0.073 · Ag 0.105 · Mg 0.017 mg cm⁻² · 26.80 Ah mol⁻¹): Li/M = 1 당 Bi **0.0126** · In **0.0170** · Ag **0.0261** · Mg **0.0187** mAh cm⁻² → Li₃Bi **0.0377** · InLi 0.0170 · In₃Li₁₃ **0.0738** · Li₉Ag **0.235** · Mg 15 % Li 0.0033 · 31 % Li 0.0084 · Li/Mg = 9 **0.169** mAh cm⁻².
- **`Fig. S2` 위 축의 환산**: 네 패널 모두 10 · 20 · 30 · 40 · 50 at% 눈금이 Q = 0.100 × x/(1−x) mAh cm⁻² 자리에 있다 (픽셀 · 오차 ≤ 2 px) → 쓴 Li/M = 1 ↔ **0.100 mAh cm⁻²** = 금속 3.73 µmol cm⁻² = 100 nm 막의 **Bi 8.0 · In 5.9 · Ag 3.8 · Mg 5.3 배**.
- **operando Bi 의 전하 과잉**: 0 V 까지 ≈0.097 mAh cm⁻² = 100 nm Li₃Bi 의 **≈2.6 배** · 두 평탄 길이 ≈0.021 · ≈0.04–0.05 = 화학량 (0.0126 · 0.025) 의 ≈1.7 · ≈1.6–2 배 (비는 1 : 2 에 가깝다). 3 전극 셀 (`Fig. S7a`) 의 0.8 V 평탄 ≈0.043 은 화학량 (0.038) 에 가깝고 평탄 앞 (2.25 → 0.8 V) 에 ≈0.015–0.02 mAh cm⁻² 가 더 들었다 (`figure-read` · 펄스 주기 ≈1 h 가정).
- **Ag 의 0.22 mAh cm⁻²** ≈ Li₉Ag 화학량 (0.235) — 본문의 'γ (Li ≥ 9 Ag) 뒤 도금' 과 100 nm 환산이 맞는다 (`Fig. S2c` 위 축으로는 o · p 가 ≈56 · ≈70 at% 라 안 맞는다).
- **Brug 유효 용량** (§3b): ≈0.45 대 ≈34 µF → 비 ≈75 (Q 비 35).
- **치환 ΔG 를 S 1 개당으로** (§3g): Ag₂S −394 ≈ Bi₂S₃ −387 > In₂S₃ −322 ≫ MgS −93 kJ (mol S)⁻¹.
- **SEI 몫**: 0.09 중 층 없음 몫 ≈0.034 를 빼면 층 때문에 더 잃은 것 ≈0.056 mAh cm⁻² → 같은 환산으로 ≈500 nm · ≈375 Ω cm².
- **접촉 35 배 ↔ SEI 1.4 배**: Bi on SE / Bi CC = 0.089 / 0.062 ≈1.4 (`figure-read`) — SEI 가 접촉 면적에 비례하지 않는다.
- **Li 두께**: 1 mAh cm⁻² ≈4.85 µm (조밀 Li) → 1.5 mAh cm⁻² ≈7.3 µm · 2 mAh cm⁻² ≈9.7 µm.
- **전류 · 면적**: 12.25 µA ÷ 9.61 µA cm⁻² = 1.275 cm² (지름 12.7 mm) — 10 mm 펠릿 (0.785 cm²) 이면 15.6 µA cm⁻² 다 (= CTTA 의 15.56 µA cm⁻²). 빔 5 pA ÷ (66 µm)² ≈0.11 µA cm⁻² (본문 ≈0.1 · ≈0.06 % of 0.2 mA cm⁻²).

---

## 4. 재료 & 방법 — 같은 실험을 흉내 낼 때 필요한 조건 전부 ★

### 4a. 재료 (p.11)
Li₆PS₅Cl (MSE Supplies LLC · D50 ≈10 µm) · Li 리본 (Sigma-Aldrich 99.9 %) · In 박 0.127 mm (Thermo Fisher) · SUS 박 10 µm (Advent) · 스퍼터 표적 Bi (50 mm × 6 mm · 99.97 %) · Ag (99.99 %) · Mg (99.9 %) (Goodfellow) · 증착용 In 알갱이 (Alfa Aesar 99.99 %). XPS 표적: In 박 (Thermo 100 µm · 99.99 %) · Ag 박 (Sigma 500 µm · 99.95 % · 4000 방 사포 연마) · Mg 조각 (Alfa −4 mesh · 99.98 %).

### 4b. 층 증착 (p.11)
§3a 표 그대로 — RF 출력 Bi 28 · Ag 58 · Mg 30 W · In 열증착 6 Å s⁻¹ · 전부 100 nm (AFM). '같은 제조 방식' 을 맞추려 In 을 증착했다고 적었지만 (p.11) 결과는 In 만 방울 꼴이다 (`Fig. 3I`).

### 4c. 셀 (p.11–12)
operando 셀 · 3 전극 · 사이클 셀 · CTTA 셀 — §0 · §3a 표. operando 셀은 위 SUS 고리 + Cu 망 (전자 접촉 면적을 늘리려고) · 아래 SUS 피스톤 · *"Once assembled, the cell operates under effectively no pressure"* (p.12). 사이클 셀만 5 MPa 가 적혀 있다 (p.8).

### 4d. 전기화학 (p.11–13)
EIS (PEIS 10 mV · 1 MHz–50 mHz · 등가 회로 R + CPE) · 주기 리튬화 (CP 30 min · OCV 10 min · PEIS) · 사이클 (0.1 mA cm⁻² · 15 h · 0.1 V 끝) · operando (0.2 mA cm⁻² · 10 h) · CTTA (15.56 µA cm⁻² · 6 min · 50 mV 문턱 · `Table S3` 정규화).

### 4e. 현미경 · 영상 분석 (p.12–13)
Tescan Mira3 · BSE (상 대비) + SE (형태) · EDS 검출기 있음 (결과는 안 보임) · 밝기 · 대비 고정 · 일정 간격 매크로 · Fiji + SAM 으로 분할 → 덮임 % · 입자 지름 분포.

### 4f. XPS (p.13)
§3a 표 · 금속 막은 ≈10 nm 목표 · 스퍼터와 측정 번갈아 · 가상 도금 = 중화기 전자빔이 시편 윗면 전체를 덮게 두고 노출 뒤 측정.

### 4g. ⚠ 논문이 적지 않은 것 (재현 · 해석에 필요한데 없다)
- **적층압** — 3 전극 EIS · 주기 리튬화 · CTTA 셀의 운전 압력 · 'functionalized CC' 를 펠릿에 붙인 압력.
- **EIS 맞춤 소프트웨어 · 오차** · `Table 1` 의 반복 (셀 하나).
- **CTTA 정규화의 실제 절차** — `Table S3` 값 · 시간 원점을 옮겼는지 (§10-①).
- **덮임 · 크기 분포의 분할 문턱 · 계수 면적 · 몇 장을 썼는지** (`Fig. 5`).
- **가상 도금의 전자빔 전류 · 노출 시간 · 시료별 Li 공급량** (Ag 파일만 'Eneut-5min' 이 남았다).
- **XPS 막 두께 확인** (≈10 nm 는 '목표') · Bi XPS 없음.
- **`Fig. S2` 위 축 환산식** (§3h · §10-②).
- 영상 (Videos S1–S7 · 리튬화 영상) 의 시간 간격 · 길이.
- 'Sup2' 보충 엑셀의 이름 · 내용 (본문은 Data S1 과 영상만 이름을 부른다).

---

## 5. 결과 — 절별 상세 (그림 실독 포함)

### 5.1 층을 어디 두나 — SE 위 대 CC 위 — `Fig. 1` · `Fig. 2` · `Table 1` (p.3–4)
`Fig. 1B,C` 도식이 전부를 말한다: CC 위 층 (파란 직선) 은 SE 입자 꼭대기에만 닿고, SE 위 층 (파란 물결) 은 입자 표면을 따라 감싼다. `Fig. 2B` 단면 BSE 에서 층은 SE 윗면의 밝은 띠다 (실독: 띠가 공칭 100 nm 보다 두꺼워 보인다 `figure-read ≈`0.3–0.5 µm — 단면 경사 · 거칠기 · BSE 상호작용 부피 탓일 수 있고, 두께는 AFM 으로 잰 값이 본문이다). 두 배치 모두 Bi 가 막힌 전극처럼 거동해 (처음 상태 · 저주파에서 |Z| 가 축전기처럼 계속 커진다) 이중층 CPE 하나로 맞췄고, Q 가 35 배라 접촉 면적이 35 배라고 읽었다. 저자는 이를 *"previously unquantified effect of deposition location on electrochemical contact area"* 라 부른다 (p.3). 그 결과 유효 전류 밀도가 크게 줄어 덴드라이트 · SEI Li 소모를 줄인다는 논리 (p.4).

### 5.2 Bi — 고른 LiBi · 불균일 Li₃Bi · 들려 깨짐 — `Fig. 3A,E–H` · `Fig. S2a` · `Fig. S3` (p.4)
1.4 V (처음) → 0.78 V 평탄 동안 영상이 고르게 어두워진다 (E → F · 실독으로는 미세한 변화). LiBi 가 다 되면 몇 곳에서 Li₃Bi 가 불균일하게 핵을 만들고 (G · 실독: 얼룩진 어두운 회색 영역 + 왼쪽 아래 균열) 그 가운데서 균열이 나 Li₃Bi 를 따라 번진다. 0.74 V 바로 아래가 LiBi–Li₃Bi 2 상 평탄이다. 계속 리튬화하면 균열이 표면 전체로 퍼지고 고르게 어두워지며 0 V 로 간다 (H · 실독: 검은 구멍 · 들린 판 가장자리). 저자: 금속간 화합물은 질서 결정이라 소성이 작고 점착이 낮다 (ref 41) · LiBi → Li₃Bi 61 % 팽창으로 층이 SE 에서 떨어져 위로 휘고 깨진다 · 층이 다 리튬화된 뒤에야 Li 도금.

### 5.3 In — 불균일하지만 멀쩡 — `Fig. 3B,I–L` · `Fig. S2b` · `Fig. S4` (p.4–6)
In 만 ≈1 µm 방울 꼴 (I · 실독: 촘촘한 알갱이 무늬) — 증착 탓. Li 를 넣자 전위가 바로 Li 도금 전위로 떨어지고 (`Fig. 3B` · 실독: 1.0 V → ≈0.5 V 어깨 → ≈0.023 mAh cm⁻² 에서 0 V) Li 가 많은 상이 차례로 핵을 만든다 (J · K · 작은 검은 점). InLi 의 높은 D 가 불균일을 만들고 InLi 가 보이자마자 다음 상이 생겨 평탄이 없다. 다 리튬화된 영역에서 Li 핵 (K) → 층이 다 리튬화되기 전에 Li 전위에 닿는 이유 (ref 45) · '합금 영역에서 Li 도금 장벽이 다음 In 상을 만드는 장벽보다 낮다' (p.4). K → L 은 리튬화와 도금이 나란히 (L · 실독: 2–6 µm 검은 덩어리가 시야의 상당 부분). 박리 · 파괴 없음 — 가장 큰 팽창 (52 %) 이 첫 단계에서 무른 In 이 받기 때문 (p.6).

### 5.4 Ag — 층 전체가 차례로 — `Fig. 3C,M–P` · `Fig. S2c` · `Fig. S5` (p.6)
M → O 가 점진적 · 고른 밝기 변화 (실독: O 는 균일한 회색). 전위는 처음 급강하 (Ag 희석) 뒤 β 상과 다음 금속간 화합물이 작은 평탄으로 나온다 — 본문은 *"likely an ordered α-Ag at 0.56 V and LiAg at 0.2 V"* 라 적었는데 그림의 작은 평탄은 ≈0.055 V · ≈0.015 V 다 (`figure-read ≈` · §10-⑦). 결정 구조가 비슷해 상이 바뀔 때마다 층 전체가 고르게 넘어간다 (D 차가 작다). O 에서 γ 고용체 (Li ≥ 9 Ag) 를 지나 P 에서 Li 가 층 위로 도금된다 — 평형이면 Li 많은 고용체라 0 V 에 안 닿지만, 이 전류에서는 Li 플럭스가 고용 속도를 넘는다. 고른 방울 · 파괴 없음 · Li 는 늘 층 **위** (p.6).

### 5.5 Mg — 고르게 희석 · 불균일한 β · 양의 되먹임 — `Fig. 3D,Q–T` · `Fig. S2d` · `Fig. S6` (p.6)
α-Mg 가 포화할 때까지 고르게 희석 (Q → R · 전위 급강하) → β 상이 불균일하게 핵을 만들고 자란다 (R → S · 실독: 얼룩무늬가 짙어짐) → 점점 어두워지며 나머지 층 리튬화와 도금 시작이 겹친다 (T). β 의 D 가 Li 따라 커져 이미 β 인 곳으로 Li 가 더 몰린다 (ref 37 · 저자 그룹 앞 논문). 상 변화가 하나이고 둘 다 고용체라 부피가 천천히 변해 응력이 작다 · 파괴 없음.

### 5.6 리튬화 정리 — 무엇이 층의 운명을 정하나 (p.6)
금속간 화합물은 단단하고 부서지기 쉬워 큰 변형을 못 받고 깨진다 · 고용체는 무르고 연성이라 천천히 팽창해 멀쩡하다. In 은 팽창이 비슷한데도 (≈52 대 ≈61 %) 멀쩡하다 → (i) 상 사이 팽창의 **임계값** 이 있을 수 있다 (ii) 증착 방울 꼴이 파괴를 견딜 수 있다 (iii) **층과 이웃 재료 사이 점착 일 (work of adhesion) 이 받아 줄 수 있는 부피 변화를 정할 수 있다** (ref 24 · 값 없음). 낮은 D → 높은 D 상 전이에서 리튬화가 불균일해지고 그것이 전위 곡선에 드러난다. 결론: 팽창의 크기와 분포 · 기계 물성 (특히 경도) · 생기는 상의 Li 수송.

### 5.7 도금 형태 — `Fig. 4` · `Fig. 5` (p.6–8)
§3d. Bi 는 Li 기둥이 층 밑에서 자라 층을 깨뜨리고, 리튬화가 끝난 뒤 Bi 층은 고른 도금에 거의 기여하지 않는다 (p.8). In · Ag · Mg 는 고르게 핵 · 방울 성장 · 새 핵 적음. 셋의 비슷한 형태는 합금 금속이 전하를 고르게 퍼뜨리고 Li 합금이 도금 과전압을 낮추기 때문 (p.8). 덮임 속도 · 크기 분포 차이는 §3d · 해석은 계면 에너지 (격자 불일치) · 고용 Li 양 · D 차.

### 5.8 사이클 — `Fig. S8` · `Fig. S16` · `Fig. S17` (p.8–9)
5 MPa · 0.1 mA cm⁻² · 1.5 mAh cm⁻²: 접촉 면적이 넓어 유효 전류가 낮아지고 층 없는 셀보다 사이클이 낫다 · 모든 층에서 핵 · 도금 과전압이 낮고 사이클 내내 유지 · Bi 는 첫 사이클 뒤 실패 (operando 와 같은 파괴 → 2 째 사이클 단락) · Ag · Mg 는 CE 가 좋아졌다고 적었다 (§10-⑧ 그림과 어긋남). 실독 (`Fig. S17`): 첫 도금 평탄 none ≈ −17 mV · 층 ≈ −5 ~ −13 mV · 박리 평탄 none ≈ +17 · 층 ≈ +7 ~ +12 mV `figure-read ≈`.

### 5.9 SEI — CTTA — `Fig. 6A–D` · `Fig. S9` · `Table S3` (p.9)
CTTA = 조금 도금 → 개회로로 두어 도금 Li 가 SEI 로 다 소모 (50 mV 까지 오름) → 반복 · 쌓이는 전하가 빠를수록 SEI 가 빨리 자란다. Bi on SE > Bi CC > none (`Fig. 6A`) — 전자 접촉 면적이 SEI 를 키운다 (`Fig. 6C,D` 도식 · ref 48 = 적층압이 CTTA 를 바꾼다는 Sivavec 2025). Bi · In · Ag 비슷 · Mg 는 훨씬 느리다 (`Fig. 6B` · 정규화 = `Table S3` 를 뺀 값). 실독 (`Fig. 6`): 계단 곡선 (계단 하나 = 1.56 µAh cm⁻²) · 층 셀은 √t 에 가까운 꼴 (Bi 30 → 180 h 비 ≈2.0 대 √6 = 2.45) · 층 없는 셀과 Mg 는 그보다 더 빨리 꺾인다 (`figure-read` · 저자 언급 없음).

### 5.10 SEI — XPS — `Fig. 6E–H` · `Fig. S10`–`S12` · `Table S4` · Data S1 (p.9)
§3g. 저자 논리: ① 스퍼터 중 금속 황화물 생성 ② Li 가 오면 Li₂S 가 더 안정해 금속 황화물을 밀어낸다 (In 확인 · Ag 추정) ③ MgS 는 구동력이 작아 (−93 kJ mol⁻¹) 바로 안 바뀌고 CTTA 의 느린 SEI 는 느린 반응 속도 탓일 수 있다 ④ Mg 는 인화물 · 산화물도 더 많아 Li 소모를 늦출 수 있다 (ref 14) ⑤ 그래서 Mg 층은 계면에 남는 부동태 SEI 를 만들고, 다른 층의 SEI 는 Li 도금과 함께 곧 바뀐다. 실독 (`Fig. S10`–`S12`): In 3d5/2 · Ag 3d5/2 가 리튬화 뒤 ≈1 eV 낮은 쪽으로 옮겨 가고 (Data S1 −1.13 · −0.99 eV · 본문 언급 없음 — Li 합금 생성 신호로 읽힌다 · 우리 해석) · Mg 1s 의 Mg⁰ 성분이 리튬화 뒤 거의 사라진다 · In · Ag 리튬화 뒤 O 1s ≈528 eV 새 봉우리 (Li₂O 류 · Data S1 In 527.81).

### 5.11 전자 화학 퍼텐셜 논증 · SEI 크기 (p.9–10)
전자가 통하는 층은 Li 가 도금된 뒤 SE 쪽 층의 전자 화학 퍼텐셜이 Li 금속과 같아진다 (ref 14) → 층이 SEI 화학을 바꾸지 않는 한 (Mg 처럼) 층에서 SE 가 환원되는 것은 Li 금속에서와 같다. 고른 도금은 필요하지만 넓어진 접촉이 SE 열화를 키운다 — 0.09 mAh cm⁻² (180 h) → ≈800 nm SEI → ≈600 Ω cm² (`Table S5`) · Alt 등의 10 Ω cm² 목표 대비 크다. 자기 부동태 층 (ref 14) 처럼 Mg 같은 부동태 SEI 를 만드는 층이 Li SEI 를 억제하면서 접촉은 지킬 수 있다 (p.10).

### 5.12 결론 (p.10–11)
성능은 합금 열역학만이 아니라 상 변화의 균일성 · Li D · 부피 변화가 정한다 · 고용체 층 (Ag · Mg) 은 고르게 리튬화하고 멀쩡 · Bi 는 61 % 로 깨짐 · In 은 무름 · 작은 상간 팽창으로 멀쩡 · 넓은 조성에서 D 가 비슷한 층 (Ag) 이 최선 · 모든 층이 핵 과전압을 낮추고 안 깨지면 고른 방울 도금 (Ag 가 가장 잘다) · SE 위 증착은 활성 면적을 늘려 균일성은 좋지만 SEI 를 빠르게 한다 · Mg 는 고른 도금 + 부동태 SEI 로 유망 · 부동태 층 + 전도성 층 조합을 제안.

---

## 6. 메커니즘 종합

**저자 사슬** (p.10–11): 상도 꼴 (고용체 · 금속간) → 상 변화가 고른가 (D 차 · 결정 구조 유사성) + 부피 변화의 크기 · 분포 + 연성 → 층이 멀쩡한가 · 리튬화가 고른가 → (멀쩡하면) 낮은 핵 과전압 + 고른 전하 분배 → 고른 방울 도금 · (깨지면) 층 밑 Li 기둥 · 단락. 따로: 전자가 통하는 층의 접촉 면적 → SEI 면적 ↑ → Li 손실 ↑ · 층 금속 황화물의 Li 치환 구동력 (Mg 작음) → SEI 가 계면에 남나.

**이 digest 가 갈라 읽은 층위** (§10 의 검산 결과를 반영):

| 주장 | 받치는 것 | 이 digest 판정 |
|---|---|---|
| SE 위 증착이 접촉 면적을 크게 늘린다 | `Table 1` · `Fig. 2C` (셀 하나) | **방향은 단단** (Bode 저주파 \|Z\| 비 ≈40 `figure-read`) · '35 배' 라는 숫자는 맞춤 방식 의존 (Brug 로는 ≈75 · `우리 산수`) |
| Bi 는 61 % 팽창으로 박리 · 파괴 · 첫 사이클 뒤 단락 | `Fig. 3G,H` · `Fig. 4A–C` · `Fig. S17b` | **단단** (영상 · 단락 둘 다) — 다만 61 % 가 원인이라는 것은 In (52 % · 전체 269 %) 과의 대조뿐이고 In 은 막 꼴도 다르다 |
| 고용체 (Ag) 는 층 전체가 고르게 리튬화 | `Fig. 3M–P` (BSE 대비 변화) | **영상과 맞다** · 정량 (분할 · 세기 분포) 은 없다 |
| 낮은 D → 높은 D 전이가 불균일을 만든다 · 그것이 전위 곡선에 드러난다 | 영상 (Bi · In · Mg) + `Fig. S2` 의 at% 축 | 영상 쪽은 맞다 · **at% 축 논증은 그 축의 환산이 공칭 막 두께와 안 맞아 (§10-②) 그대로는 못 쓴다** |
| 층이 핵 과전압을 낮춘다 (none > Bi > In > Ag > Mg) | `Fig. S8` (셀 하나씩) | 순서로는 쓸 만하다 · 크기는 그림 판독 |
| 층이 CE 를 높인다 | 본문 p.8–9 | **그림과 어긋난다** — 첫 사이클 CE 는 층 없는 셀이 가장 높다 (`Fig. S16f`) · 층의 이득은 '단락 없이 더 간다' 다 (§10-⑧) |
| 전자 전도 층은 SEI 를 키운다 | `Fig. 6A` (Bi on SE > Bi CC > none) | **방향은 단단** · 크기는 접촉 면적에 비례하지 않는다 (35 배 접촉 ↔ 1.4 배 SEI · `우리 산수`) |
| Mg 는 SEI 가 느리다 (부동태) | `Fig. 6B` (정규화) + XPS (MgS 유지 · 인화물) | **약하다** — `Fig. S9` 원자료에서 Mg 가 가장 많이 잃고 `Table S3` 로 `Fig. 6B` 가 재현되지 않는다 (§10-①) · XPS 차 0.2 eV · Li 공급량 미확인 (§10-③) |

---

## 7. 우리 계산과의 대조 ★ (`../our_dft_baseline.md` · W_ad 보고서 · DEM)

### 7a. 이 논문이 우리 어느 축에 걸리나 (먼저 판정)

- **물성 4축 (A 이온 · B 산화 · C 기계 · D 전자) — 수치가 없다.** LPSCl 의 σ · Ea · 탄성 · 띠틈 어느 것도 이 논문에 없다 (SE 저항 33–34 Ω 은 셀 하나의 펠릿 저항일 뿐 두께 · σ 환산이 없다) → `comparison_vs_ours.md` 물성 표에 넣지 않는다.
- **E 축 (환원 / Li 금속 계면) — 같은 계 (Li₆PS₅Cl) 의 실험.** 걸리는 곳 셋: ① 네 층의 합금 전위가 전부 우리 **환원 가장자리 1.717 V** 아래다 ② XPS 반응 산물 (Li₂S · 환원 P) 이 우리 0 V 끝 산물과 같은 방향이다 ③ CTTA 는 그 환원의 속도를 잰다 (우리는 열역학까지).
- **W_ad 보고서 7 절 (Li 친화성 · 합금 구동력) · 8 절 (계면의 상태 · Li 가 쌓이는 자리 · 공극 · 부피) — 실험 대조 여러 줄** (§11). 7 절 ① · ② (흡착 · 젖음 · 점착) 는 재지 않았다 — 저자가 '점착 일이 받아 줄 수 있는 부피 변화를 정할 수 있다' 고 **말만** 한다 (p.6).
- **DEM · 연속체 — 접촉 분율 대조 표적 하나 (`Table 1`) + 정성 입력 몇 개** (§11).

### 7b. 항목별 대조

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| SE 환원의 문턱 | 층이 0.78 V (Bi) · ≲0.6 V (In) · ≲0.06 V (Ag) · ≲0.22 V (Mg) 에서 리튬화 · 저자는 'Li 가 도금된 뒤 층의 전자 화학 퍼텐셜이 Li 금속과 같아져 SE 가 환원된다' 고 쓴다 (p.9) | grand-potential **환원 가장자리 1.717 V** (Li 교환 0 · comp1 = modelc) → 1.242 V (5 Li₂S + LiCl + P) → 0 V 끝 Li₂S + Li₃P + LiCl (`../our_dft_baseline.md` · `../comparison_vs_ours.md` §E) | **같은 방향 · 우리 쪽이 더 이르다** — 우리 열역학으로는 층\|LPSCl 계면이 **도금 전 합금 단계에서 이미** 환원 영역에 있다 (Bi 0.78 V 도 1.717 V 아래). 저자의 '도금 뒤' 틀보다 이른 SEI 를 예측한다 (속도는 계산 밖) · CTTA 정규화 (0 V 전 전하를 전부 '합금' 으로 뺀다) 는 그 몫의 SEI 를 같이 지운다 — Bi · In 처럼 높은 전위 합금일수록 더 (우리 해석) |
| 환원 산물 | XPS 리튬화 뒤 S 2p 159.90–160.01 (Li₂S) · P 2p 환원 성분 126.7–130.0 eV (Mg 스퍼터 중 · In 5 min) · Cl 2p 는 보정 기준이라 LiCl 을 못 본다 (`Data S1`) | 0 V 끝 Li₂S + Li₃P + LiCl | **같다** (Li₂S · 환원 P) · Mg₃P₂ 인지 Li₃P 인지 · 금속 인화물인지는 BE 만으로 못 가른다 |
| 층 금속 황화물의 Li 치환 | ΔG Bi₂S₃ −1162 · In₂S₃ −965 · Ag₂S −394 · MgS −93 kJ mol⁻¹ (화학식당 · 핸드북) · S 당 −387 · −322 · −394 · −93 (`우리 산수`) | 금속 황화물 계산 없음 · Ag\|LPSCl 은 W_ad 보고서 2-3 의 반응 없는 날카로운 계면 가정 | 대조 불가 (우리 값 없음) · **S 당으로 보면 Ag₂S 치환이 In₂S₃ 보다 유리** — 본문의 In ≫ Ag 비교는 화학량 탓이다 (§10-⑤) · 순서 대조는 MP 볼록 껍질로 싸게 낼 수 있다 (계산 후보) |
| SEI 성장 속도 | CTTA 180 h: none ≈0.034 · Bi/In/Ag ≈0.09 · Mg ≈0.05 (정규화) mAh cm⁻² `figure-read ≈` · √t 에 가까운 꼴 | 계산 없음 (우리는 '환원된다' 까지) | n/a — 대조 표적도 아니다 (정규화 재현 안 됨 · §10-①) |
| 합금 전위 (구동력) | Bi 0.78 · 0.74 V · In (3 전극) ≈0.6 V · Ag ≈0.055 · ≈0.015 V · Mg ≲0.22 V 에서 급강하 `figure-read ≈` | W_ad 보고서 7 절 ③ 제안 단계 (상평형 계산 · 아직 안 함) | **대조 표적 (순서 Bi ≫ In > Ag ≈ Mg)** — 셀 분극 · 0 MPa · 0.2 mA cm⁻² 가 섞인 값이라 절대값은 맞추지 않는다 · 같은 순서를 becker2026 (LPSCl · 적정 OCV) 이 준다 |
| 부피 변화 | MP 결정 구조 (PBE) 의 원자당 부피 비 (`Table S2`) | 우리 DFT 이완은 고정셀 + EOS (argyrodite 만) · 금속간 화합물 계산 없음 | 같은 출처 (MP) 라 **비는 우리가 다시 내도 거의 같다** · 절대 부피는 PBE 과대 (흔히 1–3 %) |
| Li 젖음 · 점착 | **재지 않았다** · 저자: 점착 일이 받아 줄 부피 변화를 정할 수 있다 (p.6 · ref 24) | W_ad 보고서 §7 ① · ② 제안 단계 · 우리 W 쌍 (Ag–C · C–C · LPSCl\|Ag(111) · LPSCl\|흑연) 값은 보고서 §2 · `db/properties/adhesion.json` (**여기 옮기지 않는다**) | 이 논문을 젖음 · 점착의 실측으로 인용하지 않는다 · 'W 가 층 박리 (부피 변화 수용) 의 변수' 라는 **가설** 의 출처로만 |
| 접촉 면적 | 증착 자리에 따라 CPE Q 35 배 (Brug ≈75 · `우리 산수`) | DEM 접촉 분율 (`../comparison_vs_ours_DEM.md` §I · 우리 값은 그쪽 원장) | **DEM 대조 표적** — '눌러 붙인 박 대 등각 막' 의 전기화학 접촉 비 · 압력 미기재 · 비정전용량 같다고 가정 (§11 #1) |
| SE 기계 물성 | 없음 | LPSCl E_VRH 22.06 / 27.66 GPa · B₀ 26.23 / 21.71 GPa (comp1 / modelc) | n/a |
| 이온 수송 · 전자구조 | 합금 상의 Li D 는 인용값 (Li₃Bi ≈10⁻⁴ · InLi 5.5 × 10⁻⁷ cm² s⁻¹) | LPSCl MLIP-MD (상대차만) · gap 2.066 / 2.099 eV (fixed-occ nscf) | n/a — 다른 물질 · 다른 양 |

### 7c. litdb 안 이웃 카드와 맞나 · 어긋나나 (11-24b 묶음)

| 이웃 카드 | 같은 것 | 다른 것 · 갈림 |
|---|---|---|
| `becker2026_electrodeposited_li_microstructure_metal_interlayers_anode_free` (LPSCl · Au · Ag · Bi 160 nm · **15 MPa** · 사후 단면) | Bi 두 평탄 800 · 760 mV ↔ 여기 0.78 · 0.74 V (같다) · Ag 는 Li 에 녹고 Bi 는 Li₃Bi 로 남는다 (같은 꼴) · 구동력 순서 Bi ≫ Ag | **Li 가 쌓이는 자리가 둘 다 반대다.** becker: Bi → Li₃Bi 층이 LPSCl 쪽에 남고 Li 는 **CC 쪽** · Ag → Li 가 **SE 쪽** (합금\|LPSCl 사이). 여기 (0 MPa · 위에서 봄): Bi → Li 기둥이 층 **밑** (SE 쪽) 에서 자라 깨진 Li₃Bi 를 들어 올림 · Ag → Li 가 층 **위** (CC 쪽). 갈리는 변수 후보: 압력 (0 대 15 MPa) · 층이 깨졌나 (여기 Bi 는 도금 전에 박리) · 관찰법 (윗면 영상은 층 밑 Li 를 못 본다) · 막 두께 (100 대 160 nm) · Bi 리튬화 전하는 becker 가 공칭보다 **적고** (150 · 100 µA cm⁻² 에서 ≈78 · ≈58 % · 그 digest 판독) 여기는 **많다** (≈2.6 배) — 면적 기준 · 양이 두 논문 모두 불확실 |
| `ko2025_metal_interlayer_anode_less_li_plating_stripping_mechanism` (가넷 · 200 nm · **0 MPa operando SEM**) | Ag → 층이 Li–Ag 합금이 되고 Li 는 SE 반대쪽 (위) 에 · 이 논문 Ag · In · Mg 와 같은 쪽 · 둘 다 0 MPa 열린 윗면 | ko 의 Au · Cu 는 층 밑에 쌓여 층을 들었다 — 여기서는 **Bi** 가 그 꼴 (Li₃Bi 박리 뒤) · 첫 CE 순서 Ag > Zn > Au > Cu (ko) 대 여기 첫 CE none > Mg > Ag > In > Bi (`Fig. S16f` · 5 MPa) |
| `haslam2025_alloying_interlayers_li_morphology_microstructure_anode_free` (LLZO · Au · Ag 100 nm · 2.5 MPa) | 고용체 형성 금속 (Ag) 은 Li 에 녹고 · 금속간 형성 금속 (Au) 은 상으로 남는다 → 여기 Ag · Mg (녹음) 대 In · Bi (남음) 와 같은 갈래 · 합금 층이 핵 과전압 골을 없앤다 | haslam 은 LLZO (SEI 없음) · 여기는 SEI 가 주제 · Ag 평탄 ≈0.054 V (haslam `Fig. S1` 0.01 mA cm⁻²) ↔ 여기 ≈0.055 V (`figure-read` · 같다) |
| `chu2026_solubility_guided_interlayer_li_plating_stripping_garnet` (LLZO · 고용도 지표) | 고용도가 큰 Ag 는 박리 쪽 문제 (공극 · 분극) — 여기 Ag 의 CE 가 3 사이클 뒤 떨어지고 (`Fig. S16f`) 저자가 '박리 뒤 층을 다시 못 만든다' 고 쓴 것과 같은 방향 | chu 는 LLZO · 0.520 MPa · 접촉각 · CCD — 여기는 CCD · 접촉각 없음 |
| `choi2025_silver_exsolution_argyrodite_anode_free` (Ag 넣은 아지로다이트) | 운전 중 (≈0 V) 계면 = LPSCl \| SEI \| Li–Ag 합금 (choi) ↔ 여기 Ag 리튬화 뒤 Li₂S + Ag 3d −1 eV (`Data S1` · 우리 해석) — 같은 그림 | choi 의 Ag 3d 367.9 eV (Ag–S 귀속) 와 여기 367.2–367.3 eV 는 보정 기준이 다를 수 있어 절대값으로 견주지 않는다 · 여기 S 2p 로는 Ag–S 가 안 갈린다 (§3g) |
| `baer2026_li_metal_argyrodite_interface_stability_transport` · `kim2026_li_argyrodite_sei_reactive_md` (계산 · Li\|LPSCl 반응) | Li 가 닿으면 계면이 곧 Li₂S 류 (antifluorite) 로 바뀐다 ↔ 여기 In · Ag 리튬화 뒤 Li₂S 가 S 2p 를 차지 (곧 바뀐다) | Mg 의 'MgS 유지' 는 계산 카드에 짝이 없다 · 그 실측도 약하다 (§10-③) |
| `kasemchainan2019_critical_stripping_current_dendrite_on_plating` · `sandoval2025_operando_xray_tomography_li_growth_stripping_anode_free` (LPSCl · 가압) | 박리 쪽이 먼저 문제 · Li 로 찬 균열 — 여기 사이클의 CE 하락 (박리 문제) 과 같은 방향 | 여기는 0 MPa 도금 영상과 5 MPa 사이클만 · 공극 · 균열 영상 없음 |
| `lee2020_silver_carbon_composite_anode_all_solid_state_li_metal` · `metzler2026_sputtered_ag_carbon_interlayers_anode_free` (Ag–C 층) | Ag 가 Li 에 녹아 옮겨 간다 (여기 '합금 금속이 Li 쪽으로 퍼진다') | Ag–C 는 Li 가 CC 쪽 (탄소가 있어서) · 여기 순수 Ag 막은 0 MPa 에서 위 (CC 쪽) — '탄소가 Li 를 CC 쪽으로 보낸다' 는 비교에 이 논문을 그대로 쓰지 않는다 (0 MPa · 열린 윗면) |

### 7d. 🔑 층위를 갈라 쓴 결론 (보고서 · 발표용)

① **같은 LPSCl 에서도 'Li 가 층의 어느 쪽에 쌓이나' 는 금속만으로 안 정해진다.** 0 MPa operando (이 논문) 와 15 MPa 사후 단면 (becker2026) 이 Bi · Ag 둘 다 반대로 나왔다. W_ad 보고서 8-3 의 '계 · 압력에 따라 다르다' 를 **같은 SE 안에서도** 압력 · 층 파괴 · 관찰법에 따라 다르다로 넓혀 쓸 근거다. 우리 W 쌍이 어느 계면을 대표하는지 (층\|SE · Li\|층 · Li\|SE) 를 적을 때 '어떤 압력 · 어떤 단계' 를 같이 적는다.

② **'합금 층\|LPSCl' 은 증착 순간부터 반응한 계면이다** — In · Mg 는 스퍼터 중 S–금속 성분이 생기고 (BE 차 0.45–0.58 · 0.19–0.21 eV · `Data S1`) Mg 는 P 도 환원된다 (P 2p 의 ≈50 %). Ag 는 S 2p 로 안 갈린다. 리튬화 뒤에는 In · Ag 쪽이 Li₂S 다. ⇒ 보고서 8-5 '계면의 상태' 에 **세 단계** (증착 직후 = 금속 황화물 + 금속 · 리튬화 중 = 합금 + SE 환원 시작 · 도금 뒤 = Li₂S 류 SEI + Li 합금) 를 적을 실험 근거.

③ **CTTA 는 고용체 층에 저장된 Li 와 SEI 로 잃은 Li 를 못 가른다.** 고용체 (Ag γ · Mg β) 의 평형 전위가 CTTA 의 50 mV 문턱보다 낮아, 개회로 동안 Li 가 합금 속으로 퍼지는 것도 '소모' 로 센다. 그래서 정규화 (0 V 전 전하 빼기) 가 결과를 정하고, 그 정규화가 이 논문 안에서 재현되지 않는다 (§10-①). 보고서 8-1 · 8-5 의 '합금 · 반응 층이면 W 와 별도로 층에 저장되는 Li 양을 따로 본다' 와 정확히 같은 함정의 실측 예다.

④ **부피 변화는 '얼마나' 보다 '어느 단계에서 · 무른 상이 받나' 가 갈랐다.** Bi 전체 +116 % 는 깨지고 In 전체 +269 % 는 멀쩡했다 — 첫 단계 (In → InLi 52 %) 를 무른 In 이 받았고 막이 방울 꼴이었다. 층\|SE 점착 (W) 이 이 수용 한계에 들어간다는 저자 가설 (p.6) 은 우리 W 계산이 채울 수 있는 빈칸이지만, **이 논문은 그 값도 순서도 주지 않는다.**

---

## 8. DFT/계산 방법 ★

**없다.** code · functional · pseudo · k-point · supercell · DFT+U · AIMD · MLIP · 무질서 처리 전부 **n/a**. 계산처럼 보이는 것 둘은 데이터베이스 · 핸드북 조회다:

- 부피 팽창 (`Table S2`) — Materials Project 결정 구조의 원자당 부피 (ref S6 · PBE 계열 이완값 · 저자 계산 아님).
- Li 치환 ΔG (`Table S4`) — 핸드북 ΔG_f (refs S7–S10: Glushko · Park/Koh/Siegel 2015 (Li₂S) · Patnaik · Lange) 를 반응식으로 더했다. 화학식당 값이다 (S 당 정규화 안 함).

### 8b. 후처리 (post-processing) — 무엇을 어떻게 숫자로 만들었나

| 무엇 | 어떻게 | 도구 | 산출 |
|---|---|---|---|
| 접촉 면적 | PEIS 스펙트럼을 R + CPE 직렬로 맞춤 → CPE Q 비 | 미기재 | `Table 1` · `Fig. 2C` · `Fig. S1` |
| 리튬화 상 | BSE 세기 = 원자번호 → 어두울수록 Li 많음 · 더 안 바뀌는 시점을 '가장 리튬화된 상태' 로 | 육안 (영상) | `Fig. 3` · 영상 |
| 덮임 · 크기 | SE 영상 분할 → 덮인 면적 % · 입자 지름 분포 | Fiji + Meta SAM | `Fig. 5A,B` |
| 핵 과전압 | 3 전극 곡선의 핵 스파이크 최저점 | — | `Fig. S8` |
| SEI | CTTA 누적 전하 − 0 V 전 전하 (`Table S3`) → 9 nm/µAh cm⁻² (Aktekin) → σ_SEI 134 nS cm⁻¹ (Alt) 로 저항 | — | `Fig. 6A,B` · `Table S5` |
| XPS | Shirley / offset Shirley 배경 · LA 선꼴 · Cl 2p3/2 = 198.5 eV 보정 · 성분 위치로 종 귀속 | CasaXPS 2.3.25 | `Fig. 6E–H` · `Fig. S10`–`S12` · Data S1 |
| 평균 조성 | 전하 → 층 평균 Li at% (위 축) | 환산식 미기재 | `Fig. S2` |

⇒ 관계는 **우리 계산이 이 논문의 빈칸을 채우는 쪽** 이다: 층 금속 황화물 · 금속 인화물의 LPSCl 대비 안정성 (볼록 껍질 · Li 화학 퍼텐셜 따라) · Li–M 볼록 껍질 전압 (Bi ≫ In > Ag ≈ Mg 순서 대조) · Li 속 M 의 고용 에너지 (녹나 · 남나) · 층\|SE · Li\|층 W (보고서 7 절 ② 의 틀). 이 논문에서 계산 수치를 가져올 것은 없다.

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 셀 도식 — (A) operando SEM 셀 (SEM 기둥 · 층 위 Li 방울 · SE · InLi/In 상대극 · 전위계) · (B) CC 위 층 (파란 직선이 SE 입자 꼭대기만 닿음) · (C) SE 위 층 (입자를 따라 감싸는 파란 물결) · (D) 3 전극 셀 (층 · SE 가운데 망 기준극 · Li) | '증착 자리 = 접촉 면적' 을 한눈에 — DEM 접촉 분율 설명 그림 · operando 셀이 무가압 · 열린 윗면이라는 것 |
| 2 | (A) RF 스퍼터 도식 · (B) Bi 층 단면 BSE (5 µm 막대 · SE 윗면 밝은 띠 · 실독 ≈0.3–0.5 µm 로 공칭보다 두꺼워 보임) · (C) Bode \|Z\| — 고주파 ≈34 Ω 같음 · 0.05 Hz 에서 CC ≈10^5.7 대 SE ≈10^4.1 Ω (`figure-read`) · 삽입 R_bulk–CPE | 접촉 면적 차의 원 데이터 — Q 비 35 · Brug ≈75 (`우리 산수`) · DEM 대조 표적 |
| 3 | 리튬화 전위 곡선 넷 (A Bi · B In · C Ag · D Mg · 상 창 점선 · 영상 시점 점 e–t) + BSE 영상 16 장 (E–H Bi · I–L In · M–P Ag · Q–T Mg · 10 µm 막대 · 시야 ≈54 µm) · 전위 +0.622 V 보정 | 금속별 리튬화 꼴 · Bi 파괴 · In 방울 막 · Ag 균일 · Mg 불균일 β — 보고서 7 절 ③ (합금 구동력) 의 순서 대조 (Bi ≫ In > Ag ≈ Mg) · ⚠ 본문 Ag 평탄 0.56 · 0.2 V 는 그림 ≈0.055 · ≈0.015 V |
| 4 | 도금 SE 영상 12 장 (A–C Bi · D–F In · G–I Ag · J–L Mg · 0.5 / 1 / 1.5 mAh cm⁻² · 같은 자리 · 10 µm 막대 · 시야 ≈36 µm) | Bi = 층 밑 Li 기둥 · 깨진 층 들림 / 나머지 = 위로 둥근 방울 — 보고서 8-3 'Li 가 쌓이는 자리' 의 LPSCl · 0 MPa 판 (becker2026 15 MPa 와 반대) |
| 5 | (A) 덮임 % 대 도금량 (In · Ag · Mg · 0–1.5 mAh cm⁻²) · (B) 1.5 mAh cm⁻² 지름 분포 (0–12 µm · 입자 % · 봉우리 Mg ≈1.7 · Ag ≈2 · In ≈3.1 µm) | 핵 밀도 · 덮임 속도의 실측 (LPSCl · 0 MPa) — DEM · 연속체 도금 모형의 정성 표적 · ⚠ 시야 하나 · 분할 문턱 미기재 |
| 6 | (A) CTTA Bi on SE · Bi CC · none · (B) Bi · In · Ag · Mg · none (정규화) · (C,D) SEI 도식 (등각 층 대 CC 접점) · (E–G) S 2p (In · Ag · Mg · 처음 → 스퍼터 3 단계 → 리튬화 뒤 · 점선 = Li₂S · S–금속 자리) · (H) Mg P 2p | 전자 전도 층이 SEI 를 키운다 (방향) · 반응 산물 (Li₂S · S–M · 환원 P) — 보고서 8-5 '계면의 상태' · ⚠ 6B 의 Mg 곡선은 `Fig. S9` + `Table S3` 로 재현 안 됨 · 6E,F 의 '30 min' 은 데이터상 40 · 50 min |
| S1 | (축소 시트로 봄) Bi 층 Nyquist — (a) CC 위 (−Im 수백 kΩ 까지) (b) SE 위 (≈13 kΩ 까지) · 맞춤은 직선 (CPE) 이고 원 데이터는 저주파 쪽에서 그 직선에서 벗어난다 | `Table 1` 맞춤의 원 스펙트럼 — CPE 하나가 전 범위를 다 못 맞춘다는 것 (§10-④ 의 보탬) |
| S2 | 리튬화 전위 곡선 넷 (확대판) + 위 가로축 '층 평균 Li at%' · 상 이름 · 영상 시점 | ⚠ 위 축은 네 금속 모두 Li/M = 1 ↔ 0.100 mAh cm⁻² (픽셀 측정) — 100 nm 막 (0.013–0.026) 과 안 맞아 캡션의 '25 at% 에서 이른 Li₃Bi' 논증을 그대로 쓰지 않는다 |
| S3 | (축소 시트로 봄) Bi–Li 상평형도 (Sangster & Pelton · ref S1) — α/β BiLi (50 at%) · BiLi₃ (≈75 at%) 두 화합물 · Bi · Li 쪽 고용 거의 없음 | 상 이름 확인용 · 7 절 ③ 볼록 껍질 계산의 상 목록 |
| S4 | (축소 시트로 봄) In–Li 상평형도 (ref S2) — 넓은 InLi (≈50 at% 둘레) · In₄Li₅ · In₂Li₃ · InLi₂ · InLi₃ · In₃Li₁₃ (≈81 at%) | 상 이름 확인용 |
| S5 | (축소 시트로 봄) Ag–Li 상평형도 (Pelton · ref S3) — (Ag) 고용체가 ≈47 at% Li 까지 · β · γ₃ · γ₂ · γ₁ · (βLi) | 상 이름 확인용 · 7-1 표 Ag 행 'Li-풍부 Li–Ag 합금' 후보 목록 |
| S6 | (축소 시트로 봄) Mg–Li 상평형도 (ref S4) — (Mg) ≈15–17 at% Li 까지 · (Li) ≈30 at% 부터 · 그 사이 2 상 | 상 이름 확인용 |
| S7 | 3 전극 주기 리튬화 넷 (a Bi · b Ag · c In · d Mg · 색 = 펄스 · 회색 = OCV · i–iv 점) | Bi 0.8 V 평탄 하나 (≈0.043 mAh cm⁻² · 화학량에 가까움) · **In ≈0.6 V 평탄이 operando (`Fig. 3B`) 엔 없다** — '같은 전위 곡선' 주장의 반례 · 평탄 앞 Bi 2.25 → 0.8 V 의 ≈0.015–0.02 mAh cm⁻² = SE 환원 후보 (우리 1.717 V 가장자리 아래 · 우리 해석) |
| S8 | Li 핵 과전압 막대 (none ≈17.8 · Bi ≈10.8 · In ≈4.6 · Ag ≈2.0 · Mg 0 mV · `figure-read`) | 보고서 8-5 '핵생성 과전압의 순서' 에 LPSCl 판 한 줄 (순서 none > Bi > In > Ag > Mg) |
| S9 | CTTA 원자료 (정규화 전 · 0–210 h · Mg 가 12 h 에 ≈0.17 · 200 h ≈0.29 로 가장 높음) | ⚠ **Mg 가 원자료에서 가장 많이 잃는다** — 6B 의 'Mg 느림' 은 정규화의 결과 (§10-①) · 고용체 층의 Li 저장 ↔ SEI 를 CTTA 가 못 가른다는 실측 예 |
| S10 | In 시료 XPS 전부 (In 3d5/2 · S 2p · P 2p · Cl 2p · Li 1s · O 1s · 처음 / 5 · 10 · **40 min** / 리튬화 뒤) | In–S → Li₂S 되돌아감의 원 그림 · In 3d −1.1 eV (Li–In 합금 신호 · 우리 해석) · 3 째 단계가 40 min |
| S11 | Ag 시료 XPS 전부 (Ag 3d5/2 · S 2p · P 2p · Cl 2p · Li 1s/Ag 4p · O 1s · 처음 / 5 · 10 · **50 min** / 리튬화 뒤) | S 2p 에 S–Ag 성분이 따로 없다 (Li₂S 색 · 160.0 eV) — `Fig. 6F` 의 'S-Metal' 은 같은 성분의 다른 이름 · Ag 3d −1.0 eV (Li–Ag 합금 신호 · 우리 해석) |
| S12 | Mg 시료 XPS 전부 (Mg 1s (Mg²⁺ · Mg⁰) · S 2p · P 2p · Cl 2p · Li 1s/Mg 2p · O 1s) | Mg 는 스퍼터 중에도 대부분 Mg²⁺ (MgS · 인화물 · 산화물) · Mg⁰ 는 리튬화 뒤 거의 사라짐 · P 환원이 크다 — 보고서 8-5 '반응 뒤 표면' 후보 (MgS · Mg₃P₂ 류) |
| S13 | (축소 시트로 봄) operando 셀 부품 사진 — 금속 바닥 전극 · 검은 절연 몸통 · 링 · 윗 전극 막대 | 무가압 셀의 실물 — 누르는 부품이 없다는 것 |
| S14 | (축소 시트로 봄) operando 셀 조립 분해도 — Top electrode · Insulating body · PEEK ring/cell holder · Bottom electrode · Insulating base | 같은 용도 |
| S15 | operando 셀 넓은 시야 (Cu 망 · SUS 고리 · 2.77 mm 시야 · 10 kV · 125 배 · SE · BSE · 2024-05 데이터 막대) | '리튬화 · 도금이 셀 전체에서 일어난다' 의 근거 — 시야 대표성 점검 (정량 아님) |
| S16 | 반쪽 셀 도금 · 박리 곡선 (a none · b Bi · c In · d Ag · e Mg · 5 MPa) + (f) CE 5 사이클 | ⚠ 첫 CE 는 none ≈95 % 가 가장 높다 — '층이 CE 를 높인다' 대신 '층이면 단락 없이 더 간다' 로 쓴다 |
| S17 | 1 · 2 · 3 사이클 곡선을 겹쳐 그림 (도금 0–15 h · 박리 ≈17–31 h) · Bi 2 째 · none 3 째 사이클 단락 | 도금 · 박리 과전압 순서 (층 < none) · 단락 시점 |
| Table 1 | SE 저항 · CPE Q · α (CC 위 · SE 위) | §3b — Q 비 35 · Brug ≈75 |
| Table S1 | 에너지 밀도 — Li 24.26 µm (2061 mAh cm⁻³ · 3860 mAh g⁻¹) · Ag–C 층 (Ag 0.8 + C 9.2 µm → 1459.5 mAh cm⁻³ · 1258 mAh g⁻¹) · 100 nm 층 (2052.8 mAh cm⁻³ · 3570.8–3808.9 mAh g⁻¹) · 층 질량 Bi 0.098 · In 0.073 · Ag 0.105 · Mg 0.017 mg cm⁻² | 100 nm 막의 이론 리튬화 전하 환산의 근거 (§3h) · 얇은 금속 층의 무게 손해가 작다는 숫자 |
| Table S2 | Bi · In 금속간 상의 원자당 부피 · 팽창 (MP) | §3c — Bi 단계 +61 % · In 첫 단계 +52 % · In 전체 +269 % |
| Table S3 | CTTA 에서 뺀 전하 (none 0 · Bi 0.041 · Bi CC 0.053 · In 0.018 · Ag 0.155 · Mg 0.024 mAh cm⁻²) | ⚠ 이 값으로 `Fig. S9` → `Fig. 6` 이 재현되지 않는다 (§10-①) |
| Table S4 | Li₂S · 금속 황화물 ΔG_f 와 Li 치환 ΔG (화학식당) | S 당으로 다시 내면 Ag₂S ≈ Bi₂S₃ > In₂S₃ ≫ MgS (§10-⑤) · 볼록 껍질 계산의 순서 대조 표적 |
| Table S5 | SEI 두께 810 nm · 저항 604 Ω cm² (0.09 mAh cm⁻² · 9 nm/µAh · 134 nS cm⁻¹) | 환산 사슬 그대로 — 층 없음 몫을 빼면 ≈500 nm · ≈375 Ω cm² (`우리 산수`) |

---

## 10. 비판 — 이 논문의 약한 곳 ★

① **CTTA 정규화가 SI 로 재현되지 않는다 — 'Mg 가 SEI 를 늦춘다' 의 정량 근거가 흔들린다.** 본문 · 방법의 정의는 '0 V 에 닿기 전 전하를 뺀다' (`Table S3`) 다. 그런데 `Fig. S9` (원자료) 와 `Fig. 6` (정규화) 를 픽셀로 맞대면 (`figure-read` · §3f 표):

- 층 없음은 그대로 같다 (뺀 값 0 · 맞다).
- Bi 는 상수 0.053 만큼 내려갔다 (100 h · 178 h 둘 다) — `Table S3` 의 Bi 값 0.041 이 아니라 **Bi CC 값 0.053** 이다. Bi CC 는 0.027 만큼 내려갔다 (표에는 0.053).
- Ag 는 ≈0.022–0.025 만큼 내려갔다 (표 0.155 를 빼면 음수가 된다 — 표의 **Mg 값 0.024** 와 비슷).
- **In · Mg 는 기울기 자체가 다르다** (100 → 178 h 증가: In S9 ≈0.011 대 6B ≈0.018 (30 h 부터 보면 0.027 대 0.045) · Mg S9 **≈0.025 대 6B ≈0.008** — 3 배). 상수를 빼거나 시간 원점을 몇 h 옮겨서는 기울기가 안 바뀐다.
- 원자료에서 Mg 는 10 h 에 ≈0.15 · 12 h 에 ≈0.17 까지 가파르게 오르는데, 100 nm Mg 를 Li/Mg ≈ 9 (90 at% Li) 로 만드는 데 드는 전하가 0.169 mAh cm⁻² 다 (`우리 산수`). 즉 그 꺾임까지는 β 고용체로의 **합금** 으로 보는 것이 자연스럽고, 그만큼을 빼면 Mg 의 180 h 값은 ≈0.11 로 Bi · In · Ag (≈0.09) 보다 **높다** — 늦은 시간 기울기도 Mg 가 가장 크다 (S9 · 100 → 178 h ≈0.025).

⇒ 고용체 층 (Ag γ · Mg β) 은 평형 전위가 50 mV 문턱보다 낮아 **개회로 중 합금 속으로 퍼지는 Li 도 '소모' 로 센다.** 이 논문의 CTTA 로는 Mg 의 SEI 를 다른 층과 같은 잣대로 순위 매길 수 없다. 표 · 그림의 짝이 바뀌었을 가능성 (오기) 과 정규화 절차 미기재를 같이 적는다 — 원자료 (Sup2 엑셀로 짐작) 가 있으면 가를 수 있다.

② **`Fig. S2` 위 축 (층 평균 Li at%) 이 공칭 막 두께와 안 맞는다.** 네 패널 모두 at% 눈금이 Li/M = 1 ↔ **0.100 mAh cm⁻²** 로 놓여 있다 (픽셀 측정 · 네 금속이 같은 값). 저자 자신의 `Table S1` 질량 (100 nm) 으로는 Li/M = 1 이 Bi 0.0126 · In 0.0170 · Ag 0.0261 · Mg 0.0187 mAh cm⁻² 다 — 축은 금속을 **3.8–8.0 배** 많게 잡았다. 그래서

- 캡션의 *"Li₃Bi/LiBi potential plateau much earlier at ∼25 at % Li"* 는 그 축 위에서만 성립한다. 100 nm 환산이면 그 평탄은 Li/Bi ≈ 2.5 (≈71 at%) 에서 시작해 '이르지' 않다.
- 거꾸로 100 nm 환산이면 Bi 는 0 V 까지 **화학량의 ≈2.6 배** 전하를 먹었다 (평탄 두 개의 비는 1 : 2 에 가깝다) — 남는 전하가 어디로 갔는지가 질문이 된다. 우리 열역학으로는 층\|LPSCl 계면이 0.78 V 에서 이미 환원 영역이라 (가장자리 1.717 V) **SE 환원이 1 순위 후보** 다 (우리 해석 · 논문에 없음). 3 전극 셀 (`Fig. S7a`) 도 0.8 V 평탄 앞 (2.25 → 0.8 V) 에 ≈0.015–0.02 mAh cm⁻² 가 더 들었다 (`figure-read`).
- Ag 는 거꾸로 100 nm 환산이 본문과 맞는다 (0.22 mAh cm⁻² ≈ Li₉Ag 0.235 · 'O 에서 γ (Li ≥ 9 Ag)') — 위 축으로는 o · p 가 ≈56 · ≈70 at% 라 본문과 어긋난다.

⇒ 'D 차 → 불균일 → 전위 곡선이 상도와 어긋난다' 는 **영상으로는 맞지만, at% 축으로 한 정량 논증은 쓰지 않는다.**

③ **Mg 의 'MgS 가 남는다' (XPS) 는 차이가 작고 Li 공급이 같은지 모른다.**

- S–Mg 와 Li₂S 의 위치 차가 **0.19–0.21 eV** 다 (`Data S1` · In 은 0.45–0.58). 한 성분 (S 2p2) 의 위치만 움직여 맞췄으므로 MgS 와 Li₂S 가 섞인 상태는 그 사이 어디로 나온다. 리튬화 뒤 이동 0.05 eV 를 '되돌아가지 않았다' 로 읽는 것은 맞춤 정밀도 근처다.
- Mg 시료는 리튬화 뒤 Li 1s 면적이 30 min 스퍼터 때와 같다 (≈46 대 ≈51 · `Data S1`) — In 시료는 같은 단계에서 ≈115 → ≈735 로 6 배 늘었다. Mg 쪽에는 **Li 가 표면 깊이 (수 nm) 까지 거의 안 왔거나 Mg 속으로 녹았다.** 가상 도금의 전자빔 조건이 시료마다 안 적혀 있어, 'MgS 가 안정해서' 와 'Li 를 덜 받아서' 를 못 가른다. Mg 1s 가 −0.28 eV 옮겨 간 것은 Li–Mg 합금으로 읽힐 수 있다 (우리 해석).
- '인화물이 더 많다' 는 In 대비로는 Data S1 이 받친다 (P 2p 환원 성분 Mg 48–57 % 대 In 22 % (5 min 만)) · Ag 는 P 2p 맞춤이 없어 견줄 수 없다.

④ **'접촉 면적 35 배' 는 CPE Q 의 비다.** α 가 다르면 (0.79 대 0.77) Q 단위가 달라 Q 비는 용량 비가 아니다. Brug 식으로 바꾸면 ≈75 배다 (`우리 산수`). 방향 (SE 위가 훨씬 넓다) 은 Bode 저주파 |Z| 비 (≈40 · `figure-read`) 로도 단단하지만 숫자는 맞춤 · 변환 방식 의존이다. `Fig. S1` (축소 시트로 봄) 에서도 CPE 직선이 저주파 쪽 원 데이터에서 벗어난다 — 한 CPE 로 전 범위를 맞춘 값이다. 셀 하나 · CC 를 붙인 압력 미기재 · 두 계면의 비정전용량이 같다는 가정이 같이 들어 있다.

⑤ **치환 ΔG 비교가 화학량에 묶여 있다.** `Table S4` 의 ΔG 는 금속 황화물 화학식 1 개당이라 S 3 개짜리 (Bi₂S₃ · In₂S₃) 가 커 보인다. S 당으로 내면 Ag₂S (−394) ≈ Bi₂S₃ (−387) > In₂S₃ (−322) ≫ MgS (−93) 다 (`우리 산수`) — 본문의 In (−965) 대 Ag (−394) 대비는 2.5 배 차가 아니라 Ag 쪽이 오히려 크다. Mg 결론 (구동력이 가장 작다) 은 그대로다. 또 이 ΔG 는 a_Li = 1 (Li 금속) 기준이고 SE 자체의 환원 (우리 1.717 V 가장자리) 과의 경쟁은 안 본다. 본문은 이 값을 'ΔG_f' 로 부른다 (생성 에너지가 아니라 치환 반응 에너지).

⑥ **Bi 대 In 의 '부피 문턱' 논증은 변수가 여럿 같이 바뀐다.** In 은 증착 (≈1 µm 방울 · 막이 연속이 아니다) · Bi 는 스퍼터 (연속막) 다. 전체 팽창은 In 이 훨씬 크다 (+269 % 대 +116 %). 저자도 문턱 · 막 꼴 · 점착 셋을 후보로만 든다 (p.6). 이 논문으로 '임계 팽창값' 을 말할 수 없다.

⑦ **숫자 · 표기가 어긋나는 곳.**

- (a) Ag 평탄 *"ordered α-Ag at 0.56 V and LiAg at 0.2 V"* (p.6) ↔ `Fig. 3C` · `Fig. S2c` 의 작은 평탄은 ≈0.055 · ≈0.015 V (`figure-read`) · 축 최대가 0.4 V 라 0.56 V 는 그림에 없다 — 자릿수 오기로 보인다 (haslam2025 의 Ag 0.054 V 와 같은 자리).
- (b) Li₃Bi D *"∼10⁻⁴ cm⁻² s⁻¹"* (단위 오기 · cm² s⁻¹) · *"10 Ω cm⁻²"* (Ω cm²) · SI 캡션의 *"0.1 mAh cm⁻²"* 전류 (mA cm⁻²) · *"Bimsuth CC"* (`Table S3`).
- (c) 주기 리튬화 *"12.25 µA (9.61 µA cm⁻²)"* 는 1.275 cm² (12.7 mm) 면적이다 — 10 mm 펠릿이면 15.6 µA cm⁻² (§3h).
- (d) Bi 처음 전위 1.4 V (본문 · `Fig. 3A` 축 위 끝에 걸림) ↔ `Fig. S2a` ≈1.7 V.
- (e) Li₃Bi D ≈10⁻⁴ cm² s⁻¹ 의 출처 (ref 44 · Weppner & Huggins 1977) 는 우리 기억으로 용융염 셀 고온 측정이다 — '298 K' 값인지 원문 확인 필요 (우리 기억 · 미확인).

⑧ **'층이 CE 를 높인다' 는 그림과 어긋난다.** 본문 (p.8–9) 은 Ag · Mg 가 층 없는 셀보다 CE 가 좋다고 쓰지만, `Fig. S16f` 첫 사이클은 **none ≈95 % > Mg ≈93 > Ag ≈85 > In ≈83 > Bi ≈81 %** 이고 둘째 사이클도 none ≈87 ≈ Mg ≈86 이다 (Ag 만 ≈92). 층 없는 셀은 3 째 사이클에 단락했으니 비교할 다음 사이클이 없다. 저자 캡션의 설명 (0.1 V 끝에서 합금에 남는 Li) 은 첫 CE 차를 설명하지만, 그렇다면 결론은 '층이면 **단락 없이** 더 간다' 다. 조건당 셀 하나.

⑨ **XPS 그림 표기가 원자료와 다르다.**

- `Fig. 6E` (In) · `Fig. 6F` (Ag) 의 셋째 단계 *"30 min sputtering"* ↔ Data S1 · `Fig. S10` · `Fig. S11` 은 **40 min · 50 min** (Mg 만 30 min).
- `Fig. 6F` 는 Ag 스퍼터 단계의 160.0 eV 성분을 'S-Metal' (청록) 로 칠했는데 같은 스펙트럼의 `Fig. S11` 은 Li₂S (노랑) 로 칠했고 Data S1 의 성분 이름도 'li2s' 다 · 위치는 160.00 → 160.03 → 159.96 → 160.01 eV 로 안 움직인다. 즉 Ag₂S 생성 · 치환은 **분광 근거 없이** 열역학 (`Table S4`) 으로만 붙었다 (저자도 *"difficult to resolve"* 라 적음).
- Bi 는 XPS 를 안 했다 · XPS 막 (≈10 nm · Ar 이온빔 · XPS 안) 과 셀 막 (100 nm · RF) 의 제조 · 두께가 다르다.

⑩ **0 MPa · 윗면 · 셀 하나.** 형태 숫자 (덮임 · 입자 수 · 크기) 는 열린 윗면 · 무가압 · 시야 하나 (≈36–66 µm) 의 값이다. 분할 문턱 · 계수 면적이 없다 (481 개는 `Fig. 4I` 패널 시야로는 다 안 들어가 더 넓은 면적에서 센 것으로 보인다). 'Ag 가 덮임 속도가 빠르다' 는 가장 가파른 기울기 10 % 남짓 차다 (`figure-read`). 층 **아래** 로 자라는 Li 는 안 보인다 — Ag · In · Mg 의 'Li 는 층 위' 도 '위에서 보이는 Li' 다.

⑪ **'S7 이 operando 전위 곡선과 같다' 는 일부만 맞다.** In 은 3 전극 셀 (`Fig. S7c`) 에서 ≈0.6 V (In/InLi) 평탄이 보이는데 operando (`Fig. 3B`) 에서는 없다 — 저자는 평탄이 없는 것을 불균일 리튬화로 설명했지만, 20 배 큰 전류 (0.2 대 ≈0.01 mA cm⁻²) · 무가압의 분극으로도 설명된다. Bi 도 3 전극은 평탄 하나 (≈0.8 V) · operando 는 둘 (0.78 · 0.74 V) 이다.

⑫ **이해 상충.** 저자 넷이 이 내용의 특허 출원을 준비 중이다 (p.13). 결론 (Mg · 부동태 층 + 전도 층 조합) 이 그 방향과 맞물린다.

---

## 11. W_ad 보고서 · DEM 입력으로 쓸 것 ★★ (보고서 7 절 · 7-1 표 · 8 절)

⛔ 전부 **Li₆PS₅Cl · 상온 · 조건당 셀 하나** 다. operando 형태는 **0 MPa**, 사이클은 **5 MPa** 다. 값은 차수 · 순서로만 쓴다. 우리 W 값은 여기 옮기지 않는다 (보고서 §2 · `db/properties/adhesion.json`).

| # | 무엇 | 값 · 관찰 | 어디 (봤나) | 쓰는 곳 · 한정 |
|---|---|---|---|---|
| 1 | 증착 자리 ↔ 전기화학 접촉 면적 | SE 위 등각 막 대 CC 위 막 = CPE Q 35 배 (Brug ≈75 · `우리 산수`) → CC 쪽 접촉 ≈1/35–1/75 | p.3–4 · `Table 1` (글자층) · `Fig. 2C` (봤다) | **DEM 접촉 분율의 대조 표적** (8-4 '국부 전류 = 전체 / 접촉 분율') — 압착 압력 미기재 · 비정전용량 같다고 가정 · 셀 하나 |
| 2 | 접촉 ↔ SEI | CTTA 180 h: Bi on SE ≈0.089 · Bi CC ≈0.062 · none ≈0.034 mAh cm⁻² → 접촉 35 배에 SEI 1.4 배 | p.9 · `Fig. 6A` (봤다 · 픽셀) | 8-4 '계면상이 생기면 부피가 준다' 옆에 — 전도 층이 SEI 면적을 키우지만 접촉에 비례하지 않는다 · 정량 인용 금지 (§10-①) |
| 3 | 층\|SE 반응 산물 (증착 직후) | In · Mg → S–금속 (BE +0.45–0.58 · +0.19–0.21 eV vs Li₂S) · Mg → P 환원 (P 2p 의 ≈50 %) · Ag → S 2p 로 안 갈림 | p.9 · `Fig. 6E–H` · `Fig. S10`–`S12` (봤다) · Data S1 | 8-2 · 8-5 '계면의 상태' — LPSCl\|금속은 증착 순간부터 반응한 계면 · 2-3 의 LPSCl\|Ag(111) (반응 없는 날카로운 계면) 은 '첫 충전 전 · Ag 는 분광으로 반응이 안 보인다' 로 한정 |
| 4 | 층\|SE (도금 뒤) | In · Ag → Li₂S (S 2p 159.90–160.01) · In 3d · Ag 3d −1.1 · −1.0 eV (Li 합금 · 우리 해석) · Mg → S–Mg 유지 (−0.05 eV · 약함) | `Fig. 6E–G` · `Fig. S10`–`S12` (봤다) · Data S1 | 8-3 끝 '운전 중 계면 = SE \| 분해 산물 \| Li–M 합금' 의 LPSCl · 실측 판 (choi2025 와 같은 그림) |
| 5 | 부피 변화 · 파괴 | Bi → LiBi +35 % · LiBi → Li₃Bi +61 % (전체 +116 %) → 박리 · 파괴 · 단락 / In → InLi +52 % (전체 +269 %) 멀쩡 / Ag · Mg 고용체 멀쩡 | p.4–6 · `Fig. 3E–H` · `Fig. 4A–C` · `Table S2` (봤다 · 표는 글자층) | 8-4 균열 · 접촉 손실에 '층의 부피 변화' 한 줄 — 얼마나보다 '어느 단계 · 무른 상' (In) · 막 꼴 교락 |
| 6 | 고용체 대 금속간 화합물 | Ag · Mg: 고른 리튬화 · 잘고 고른 Li (481 · 321 개) · 핵 과전압 2 · 0 mV · 그러나 금속이 Li 로 퍼짐 / In: 마지막 금속간 상이 Li 와 평형 (조성 고정) | p.6–8 · `Fig. 3` · `Fig. 5` · `Fig. S8` (봤다) | 7 절 ③ 을 '생기나 · 녹나 · 남나' 로 쪼갤 근거 (haslam2025 · becker2026 와 같은 갈래) · 7-1 표 Ag 행 'Li 속 묽은 고용체' 와 맞다 |
| 7 | Li 가 쌓이는 자리 (LPSCl · 0 MPa) | Ag · In · Mg → 층 **위** (보이는 것만) · Bi → 층 **밑** 기둥 (깨진 Li₃Bi 를 들어 올림) | p.6–8 · `Fig. 4` (봤다) | 8-3 — becker2026 (15 MPa · 사후) 과 Bi · Ag 둘 다 반대 → '계 · 압력에 따라' 를 '같은 SE 에서도 압력 · 층 파괴 · 관찰법에 따라' 로 |
| 8 | Li 핵 과전압 순서 | none ≈17.8 > Bi ≈10.8 > In ≈4.6 > Ag ≈2.0 > Mg 0 mV | SI p.6 · `Fig. S8` (봤다 · figure-read) | 8-5 '실험과 견줄 것' 의 핵 과전압 순서에 LPSCl 판 한 줄 (대조 표적 · 순서만) |
| 9 | 합금 전위 순서 | Bi 0.78 · 0.74 V > In ≈0.6 V (3 전극) > Mg ≲0.22 V · Ag ≈0.055 · ≈0.015 V | `Fig. 3A–D` · `Fig. S2` · `Fig. S7` (봤다 · figure-read) | 7 절 ③ 볼록 껍질 전압의 순서 대조 (Bi ≫ In > Ag ≈ Mg) · becker2026 의 Bi ≫ Au > Ag 와 이어 붙일 수 있다 · 분극 섞임 |
| 10 | CTTA 의 한계 | 고용체 층 (Ag γ · Mg β) 은 평형 전위 < 50 mV → 합금 속 Li 확산과 SEI 소모가 안 갈림 · 정규화가 재현 안 됨 | `Fig. S9` · `Fig. 6B` · `Table S3` (봤다 · 픽셀) | 8-1 · 8-5 '합금 · 반응 층이면 층에 저장되는 Li 양을 따로 본다' 의 실측 함정 예 |
| 11 | 점착 일 가설 | '층과 이웃 재료 사이 점착 일이 받아 줄 수 있는 부피 변화를 정할 수 있다' (ref 24) — 값 없음 | p.6 (본문) | W(층\|SE) · W(Li–M\|SE) 가 들어갈 자리의 문헌 가설 · 이 논문은 값도 순서도 안 준다 |
| 12 | 도금 형태의 압력 문장 | 0 MPa 방울 → 가압 (Li 경도 ≈2 MPa · 크리프 그 아래) 이면 눌려 평평한 막 | p.8 (본문) | 8-4 '압력은 세 단계' 옆 — operando 무가압 형태를 셀 조건으로 옮기지 않는다는 저자 자신의 단서 |

---

## 12. 적용 인사이트 ★

- ① **W 표의 '계면 상태' 칸을 셋으로 나눈다** — 증착 직후 (금속 황화물 · 인화물 + 금속) · 리튬화 중 (합금 + SE 환원 시작 · 우리 1.717 V 가장자리 아래) · 도금 뒤 (Li₂S 류 SEI + Li 합금). LPSCl\|Ag(111) 처럼 반응 없는 날카로운 계면은 첫 단계의 **이상화** 라고 이름을 붙여 낸다.
- ② **싼 계산 하나 — 금속 황화물 · 인화물의 LPSCl 대비 안정성.** MP 볼록 껍질에서 MS_x + Li → Li₂S + M 의 S 당 반응 에너지 (Ag₂S ≈ Bi₂S₃ > In₂S₃ ≫ MgS 순서가 대조 표적) 와 LPSCl + M 의 반응 생성물을 Li 화학 퍼텐셜에 따라 보면, '층이 SEI 화학을 바꾸나' 를 우리 grand-potential 틀로 바로 답할 수 있다 (새 DFT 없이 · 계산 후보 — 카드부터).
- ③ **DEM 접촉 분율의 실험 짝으로 `Table 1` 을 적어 둔다** — '눌러 붙인 박 대 등각 막' 의 전기화학 접촉 비 1/35–1/75. 다만 압력이 없으니 '그 압력에서 DEM 이 같은 차수를 내나' 의 대조로만.
- ④ **CTTA 숫자를 W · SEI 논의에 끌어올 때 고용체 층은 빼거나 따로 단다.** 이 논문의 Mg 결과는 정규화가 정한다 — 'Mg 가 부동태 SEI 로 Li 손실을 줄인다' 를 우리 보고서에 근거로 싣지 않는다.
- ⑤ **'Li 가 어디 쌓이나' 를 계산 쪽에서 묻는 질문은 압력을 같이 둔다.** 같은 LPSCl 에서 0 MPa (여기) 와 15 MPa (becker2026) 가 반대로 나왔다 — W 순위 하나로 Li 자리를 예측하지 않는다 (보고서 8-3 의 Metzler 2025 결론과 같은 방향).

---

## 13. 인용 가능 문장 (영문 초안)

- "Depositing a 100 nm Bi layer directly on a cold-pressed Li₆PS₅Cl pellet, rather than on the stainless-steel current collector, increased the fitted double-layer CPE coefficient by a factor of ~35 (4.6 to 164 µF s^(α−1)), indicating a much larger electrochemically active contact area [*Joule*, 9, 102175 (2025)]."
- "In operando SEM at negligible stack pressure, Bi interlayers delaminated and fractured during the LiBi-to-Li₃Bi transformation (61% volume expansion), and Li then grew as pillars beneath the fractured layer, whereas In, Ag and Mg interlayers remained intact and Li nucleated uniformly on top as globules."
- "Electronically conducting interlayers increased Li consumption measured by coulometric titration time analysis (Bi on the electrolyte > Bi on the current collector > no interlayer)."
- "In situ XPS showed In–S and Mg–S species forming during metal deposition on Li₆PS₅Cl; after virtual Li plating, the In-derived sulfide signal shifted back to the Li₂S position, while the Mg-derived signal shifted by only ~0.05 eV."
- ⚠ 원고에 쓸 때 'Mg interlayers suppress SEI growth' · 'interlayers improve Coulombic efficiency' 단독 서술은 쓰지 않는다 (§10-① · §10-⑧). 'contact area increased 35-fold' 는 'CPE coefficient increased ~35-fold' 로 쓴다 (§10-④).

---

## 14. 주의 / 한계 (인용 규율)

- ⛔ **operando 형태 숫자 (덮임 · 입자 수 · 크기 · Li 자리) 를 가압 셀 조건으로 옮기지 않는다** — 0 MPa · 열린 윗면 · 시야 하나 · 셀 하나.
- ⛔ **CTTA 의 Mg 순위 · 정규화 값을 정량으로 인용하지 않는다** — `Fig. S9` · `Table S3` · `Fig. 6B` 가 서로 안 맞는다 (§10-①). 인용한다면 방향 (전도 층 > 층 없음 · SE 위 > CC 위) 만.
- ⛔ **`Fig. S2` 의 at% 축 · 그것으로 한 '이른 핵생성' 논증을 인용하지 않는다** (§10-②).
- ⛔ **젖음 · 점착의 측정으로 인용하지 않는다** — 접촉각 · 박리 시험 · 흡착 에너지가 없다. 점착 일은 저자 가설 (ref 24) 일 뿐이다.
- ⛔ **우리 W (보고서 §2 · `db/properties/adhesion.json`) 와 같은 표에 놓지 않는다** — 이 논문에는 W 도 G_c 도 없다.
- '접촉 면적 35 배' 는 'CPE Q 35 배' 로 쓴다 (Brug 로는 ≈75) · 'CE 향상' 은 '단락 없이 더 간다' 로 쓴다 (§10-④ · ⑧).
- XPS BE 차 (In 0.45–0.58 · Mg 0.19–0.21 · Ag ≈0.03 eV) 는 Data S1 맞춤값이다 — 맞춤 성분 하나의 위치라 혼합 상태를 못 가른다 · Cl 2p 보정이라 LiCl 생성은 못 본다.
- 핵 과전압 · CE · 덮임 · CTTA 곡선 값은 그림 판독이다 (본문 숫자는 Bi 10 mV · 0.09 mAh cm⁻² · 481/444/321 개 · 0.05/0.25/0.1 mAh cm⁻² 정도) — `figure-read ≈` 를 떼지 않는다.
- 부피 · ΔG 는 데이터베이스 · 핸드북 값이다 (저자 계산 아님) · ΔG 는 화학식당.

---

## 15. 기법 용어 미니사전

| 용어 | 뜻 (이 논문에서) |
|---|---|
| anode-less / lithium-less (무음극) | Li 박 없이 첫 충전에서 Li 를 그 자리에서 도금하는 셀. 이 논문 반쪽 셀의 Li 원은 상대극 (Li 박 · InLi–In) 이다 |
| functionalized CC | 금속 층을 SE 가 아니라 집전체 (SUS 박) 위에 증착한 배치. SE 입자 꼭대기에만 닿는다 |
| RF 마그네트론 스퍼터 · 열증착 | 플라스마로 표적을 때려 원자를 날려 쌓는 법 · 금속을 녹여 증발시켜 쌓는 법. In 은 녹는점이 낮아 증착했고 그래서 방울 꼴이 됐다 |
| BSE · SE 영상 | 후방산란 전자 (세기 ∝ 원자번호 → 상 대비 · Li 가 많을수록 어둡다) · 이차 전자 (표면 형태) |
| CPE (상수 위상 요소) | 이상 축전기 대신 쓰는 임피던스 요소 Z = 1/[Q(jω)^α]. α = 1 이면 축전기 · α < 1 이면 거칠거나 고르지 않은 계면. Q 의 단위가 α 에 따라 달라 α 가 다르면 Q 를 그대로 견줄 수 없다 |
| Brug 식 | CPE 의 Q · α 와 직렬 저항으로 유효 용량을 내는 식 (막힌 전극: C = Q^(1/α) R^((1−α)/α)) — §3b · §10-④ 의 우리 산수 |
| 막힌 전극 (blocking electrode) | 전하 이동 반응이 없어 이중층 충전만 하는 전극. 저주파에서 임피던스가 축전기처럼 계속 커진다 |
| 3 전극 · 망 기준극 | SE 가운데 InLi 를 입힌 망을 기준극으로 넣어 작업극 전위만 따로 재는 셀 (Riegger 2023 방식) |
| 2 상 평탄 | 두 상이 공존하는 동안 Li 화학 퍼텐셜이 고정돼 전위가 평평한 구간 (예: LiBi + Li₃Bi) |
| 고용체 (solid solution) · 금속간 화합물 (intermetallic) | 조성이 연속으로 바뀌는 한 상 (Ag–Li · Mg–Li) · 정해진 조성 · 질서 결정의 화합물 (LiBi · Li₃Bi · InLi …) |
| D (Li 확산계수) · 화학 확산계수 | Li 가 상 속을 퍼지는 빠르기. 전기화학으로 잰 화학 확산계수는 열역학 증폭 인자가 곱해져 매우 클 수 있다 (Li₃Bi 의 ≈10⁻⁴ cm² s⁻¹) |
| 핵 과전압 (nucleation overpotential) | Li 도금 시작에 전위가 평탄보다 더 내려갔다 올라오는 골 · 새 Li 핵을 만드는 추가 구동력 |
| CTTA (전량 적정 시간 분석) | 조금 도금 → 개회로로 두어 Li 가 SEI 로 다 소모될 때 (50 mV) 까지 기다림 → 반복. 누적 전하 = SEI 로 잃은 Li (Aktekin 2023) |
| 가상 전극 도금 (virtual electrode plating) | XPS 안에서 전자빔 (중화기) 으로 시편 윗면에 전자를 주어 아래 Li 박의 Li⁺ 를 SE 를 지나 윗면으로 끌어와 도금하는 법 (Narayanan 2022 · Wenzel 2015) |
| Shirley · offset Shirley 배경 · LA 선꼴 | XPS 배경 빼는 법 · CasaXPS 의 비대칭 Lorentzian 선꼴 (금속의 높은 BE 쪽 꼬리) |
| 전하 보정 (charge calibration) | 시편 대전으로 밀린 BE 를 기준 봉우리 (여기 Cl 2p3/2 = 198.5 eV) 로 맞추는 것 — 그 봉우리의 화학이 안 바뀐다고 가정한다 |
| S–PS₄ · S_bri · S–M | 아지로다이트 PS₄³⁻ 의 S · 다리 S (P–S–P 류) · 금속 황화물의 S²⁻ (이 논문 그림 범례) |
| P_red | 환원된 P (인화물 · P–P) — P 2p 가 PS₄³⁻ (≈132 eV) 보다 낮은 BE (≈130 · ≈127 eV) |
| 전자 화학 퍼텐셜 논증 | 전자가 통하는 층이 Li 와 닿으면 층의 전자 화학 퍼텐셜이 Li 금속과 같아져, 층에 닿은 SE 는 Li 금속에 닿은 것과 같은 환원 구동력을 받는다 (ref 14) |
| Segment Anything Model (SAM) | 영상에서 물체 경계를 자동으로 따는 학습 모형 (Meta) — 여기서는 Li 방울 분할 |
| 양의 되먹임 (positive feedback) | β-Li 의 D 가 Li 함량에 따라 커져, 이미 β 인 곳으로 Li 가 더 몰리는 것 (Mg) |

---

## 16. 이웃 digest · 참고문헌 지도

| 무엇 | 어디 |
|---|---|
| 같은 LPSCl 무음극 금속 층 | `becker2026_electrodeposited_li_microstructure_metal_interlayers_anode_free.md` (Au · Ag · Bi 160 nm · 15 MPa · EBSD — Li 자리 반대 · §7c) · `sandoval2025_operando_xray_tomography_li_growth_stripping_anode_free.md` (Au · Ag 100 nm/Cu · operando μCT) · 같은 배치 `sandoval2023_alloy_interlayers_structural_electrochemical_evolution_anode_free` (ref 28 · 진행 중) |
| 가넷 위 금속 층 (operando · 0 MPa) | `ko2025_metal_interlayer_anode_less_li_plating_stripping_mechanism.md` (Cu · Au · Ag · Zn) · `haslam2025_alloying_interlayers_li_morphology_microstructure_anode_free.md` (ref 23 · Au · Ag) · `chu2026_solubility_guided_interlayer_li_plating_stripping_garnet.md` (고용도 지표) |
| Li\|LPSCl 반응 · SEI (계산) | `baer2026_li_metal_argyrodite_interface_stability_transport.md` · `kim2026_li_argyrodite_sei_reactive_md.md` · `lepley2015_modeling_interfaces_between_solids_li_battery_materials.md` |
| Ag 와 아지로다이트 | `choi2025_silver_exsolution_argyrodite_anode_free.md` (운전 중 계면 = LPSCl \| SEI \| Li–Ag) · `lu2026_li_ag_interface_thermodynamics_kinetics.md` (Li\|Ag W_ad) |
| Ag–C 층 | `lee2020_silver_carbon_composite_anode_all_solid_state_li_metal.md` (ref 30) · `metzler2026_sputtered_ag_carbon_interlayers_anode_free.md` · `metzler2025_ag_particle_distribution_carbon_interlayer_anode_free.md` · `xie2024_agc_buffer_layer_lithiation_delithiation_mechanism.md` |
| 박리 · 적층압 (LPSCl) | `kasemchainan2019_critical_stripping_current_dendrite_on_plating.md` |
| litdb 에 없는 참고문헌 중 중요한 것 | ref 12 Aktekin 2023 *Nat. Commun.* 14, 6946 (CTTA) · ref 13 Narayanan 2022 *Nat. Commun.* 13, 7237 (가상 전극 XPS) · ref 14 Burton 2025 *Nat. Commun.* 16, 9304 (SEI 의 P) · ref 37 Aspinall 2024 *Nat. Commun.* 15, 4511 (Li–Mg) · ref 39 Thomas 2024 *Chem. Mater.* 36, 8936 (Li–Ag) · ref 41 Aspinall 2024 *ACS Energy Lett.* (Li–In) · ref 48 Sivavec 2025 *Commun. Chem.* 8, 96 (CTTA 적층압) · ref 49 Alt 2024 *Joule* 8, 2755 (다상 SEI) · ref 31 Jeong 2024 *ACS Energy Lett.* 9, 2554 (원소 합금 음극) · ref 24 Kim 2023 *Nat. Commun.* 14, 782 (인터레이어 · 점착) |

---

## 17. 이 digest 의 재현 메모 (원자료 · 판독)

- **Data S1** (`litdb/inbox/kotakadi2025_metallic_interlayers_dataS1_xps/*.vms` · VAMAS · CasaXPS 2.3.25 정보 포함 · 파일당 36 블록 = 전체 + 핵심 준위 × 5 단계): 블록마다 `Casa Info Follows` 뒤 `Calib M = … A = 198.5 BE ADD` (Cl 2p3/2 보정) · `CASA comp (*이름*) … Position <KE>` 줄을 읽어 BE = 1486.6 − KE 로 바꿨다 (보정된 틀 · Cl 2p 성분이 정확히 198.5 eV 로 나온다). 이중선은 연결 안 된 (link −1) 성분만 표에 올렸다. 단계 이름은 파일 그대로 — In `Pristine · 4kV-5min · 4kV-10min · 4kV-40min · after lithiation` · Ag `Pristine · 4kV-5min · 4kV-10min · 4kV-50min · Eneut-5min` · Mg `Initial · 4kV-5minMg · 4kV-10minMg · 4kV-30minMg · after lithiation`. 측정일은 파일 머리 기준 Mg 2022-06 · In 2022-09 · Ag 2022-10 이다 (투고 2025-04 보다 2.5–3 년 앞선다). 획득 조건 (스캔 수) 은 블록마다 확인하지 않았다 — 면적은 같은 파일 안에서만 견줬다.
- **곡선 판독** (`Fig. 5A` · `Fig. 6A,B` · `Fig. S9`): 테두리 · 눈금 픽셀로 축을 맞추고 곡선 색 (±45–70 RGB 합) 으로 시각마다 세로 위치의 중앙값을 냈다. 겹친 곡선 (Bi · In @ 100 h) 은 판독값을 비웠다.
- **`Fig. S2` 위 축**: 네 패널 위 · 아래 눈금을 픽셀로 찾아 10–70 at% 눈금을 mAh cm⁻² 로 바꿨다 → 모두 Q = 0.100 x/(1−x) 와 ≤2 px 안에서 맞는다.
- **축척 막대**: `Fig. 3E` 10 µm = 78 px · 패널 폭 ≈419 px → ≈54 µm · `Fig. 4A` 10 µm = 146 px · 패널 ≈525 px → ≈36 µm.
- 판독 스크립트 · 중간 파일은 scratchpad (세션 임시) 에만 두었다 — 다시 내려면 위 절차를 따른다.
