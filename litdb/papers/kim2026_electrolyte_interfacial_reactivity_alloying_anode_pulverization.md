<!-- digest 초판 2026-10-05 (논문 에이전트 · 대피 세션 `claude/evac-2026-10-02` — 커밋·INDEX·comparison 병합은 부모 세션이 한다).
     ① 그림: 본문 FIGURE 1–6 전부 실독. 확대 판독 = `Fig. 1b`(초기 사이클 3×) · `Fig. 3` F 1s 열 · `Fig. 5d,e`(원본 래스터를 `Fig. S26` 과 나란히) · `Fig. 6b`(2×).
        SI 26장 실독, 표는 `Table S1`·`Table S3` 만 이미지로 확인 (나머지 표는 PDF 텍스트). 안 본 SI 그림 8장은 머리말에 목록.
     ② 손 크롭 2: `Fig. S3`(SI p.3) · `Fig. S27`(SI p.24) — 도구가 '그래픽 없음' 으로 번호 공백 처리한 벡터 그림이다 (figures.json `manual_crop`).
     ③ 동영상 3개(Movie S1–S3) 는 직접 재생하지 못했다 — 정지 프레임 8장씩만 봤다.
     ④ 정량 검산 넷 (우리 산수): `Fig. S25` g(r) 디지타이즈 → Na–P 배위수 · `Table S1` 분할 정합 · `Table S3` 값으로 응력 상한 · AIMD/T3 관측창 (`tools/sei/collect_neb.py::hop_check`).
     ⑤ `kim2026_li_argyrodite_sei_reactive_md` ([KimSEI]) 와 다른 논문이다 — 접두 'kim2026' 만 같다. -->

# Electrolyte Interfacial Reactivity Regulates Alloying Anode Pulverization — Kim, Xu et al. (*Adv. Energy Mater.* 2026, e71596)

> slug `kim2026_electrolyte_interfacial_reactivity_alloying_anode_pulverization` · DOI `10.1002/aenm.71596` · type `exp 주 (Na 반쪽·완전셀 · SEM/3D-XRM · cryo-(S)TEM/EDS · APT · XPS · ToF-SIMS · in-situ XRD · 고정밀 누설전류) + 계산 보조 (GROMACS 고전 MD · NWChem B3LYP 환원전위 · VASP-PBE AIMD 5 ps · 자체 위상장)` · PDF `litdb/inbox/Kim 2026 - Electrolyte interfacial reactivity regulates alloying anode pulverization (Adv Energy Mater aenm.71596).pdf` (본문 19 pp) + `litdb/inbox/Kim 2026 - Sup) Electrolyte interfacial reactivity regulates alloying anode pulverization (Adv Energy Mater aenm.71596) SI.pdf` (SI 37 pp: Note S1–S2 · `Fig. S1`–`S35` · `Table S1`–`S7`) + 동영상 3 (`Sup2`–`Sup4 Movie` = Movie S1–S3) · digested `2026-10-05` · status ✅ · 태그 **[외부 · Na 계 · 액체 전해질 · 합금 음극]**

> elements: Na, Bi, Sn, C, O, F, P
> methods: DFT, AIMD, MD, XPS

> **저자**: **Namhyung Kim**¹†$ · **Yaobin Xu**²† · Bharat Gwalani³# · Won-Gwang Lim¹ · Matthew R. Fayette¹ · Guosheng Li¹ · Mark H. Engelhard¹ · Peiyuan Gao³ · Yulan Li³ · Shenyang Hu⁴ · Lili Liu¹ · Jiyu Cai⁵ · Zonghai Chen⁵ · Md Jasim Uddin⁶ · Bhuvaneswari M. Sivakumar¹ · Hsin-Mei Kao³ · Zihua Zhu² · Seoa Kim¹ · Fredrick Omenya¹ · David Reed¹ · **Chongmin Wang**²\* · **Xiaolin Li**¹\* (†공동 1저자) — ¹PNNL Energy & Environment Directorate ²PNNL EMSL ³PNNL Physical & Computational Sciences ⁴PNNL National Security Directorate ⁵Argonne Chemical Sciences & Engineering ⁶NC State MSE ($ 현 부경대 소재시스템공학과 · # 현 NC State) · 접수 2026-04-27 · 개정 08-17 · 수락 09-09 · **OA (CC BY)** · © Battelle / UChicago Argonne · 자금: DOE Office of Electricity, Energy Storage Division (PNNL DE-AC05-76RL01830) · EMSL 사용자 과제 51717·60577·51382 + ToF-SIMS 과제 · Kao = DOE BES award 10122 · 사사: Arnulf Latz · Timo Danner (HIU — `[Claus24Gar]` 의 저자들) · 데이터: "요청 시 제공"
>
> **분업** (Author Contributions 원문): 고전 MD·분자 DFT·AIMD = **Peiyuan Gao** · 위상장 = **Yulan Li · Shenyang Hu** · cryo-TEM = Yaobin Xu (C. Wang 지도) · 3D-XRM = Guosheng Li · APT = Gwalani (+Uddin) · XPS = Sivakumar·Engelhard · in-situ XRD = Omenya · ToF-SIMS = Kao·Zhu · 누설전류 = Cai·Chen (ANL) · 전극·전기화학 = N. Kim · 필름 전착 = Fayette.
>
> **선행 관측**: "글라임(에터) 전해질이 Bi·Sn 음극에 좋다" 는 것 자체는 이 논문이 인용한 선행이 있다 — ref 37 (Zhang/Tarascon 2016, 마이크로 Sn) · ref 40 (Wang 2017, 벌크 Bi) · ref 73 (Qin 2020, Sn). **이 논문의 몫은 관측이 아니라 기전 해석**이다.
>
> **관련 digest**: `kim2026_li_argyrodite_sei_reactive_md` ([KimSEI] — ⚠ **다른 논문**: Li‖아지로다이트 반응 MD) · `chaney2024_two_step_sei_growth_argyrodite_li_metal` ([Chaney24SEI] — SEI 시간축) · `li2026_mci_vs_sei_na3ps4_na_mlip_md` ([Li26MCI] — Na 계 SEI/MCI MLIP-MD) · `clausnitzer2024_degradation_mechanisms_cathode_llzo` ([Claus24Gar] — 사사의 Latz·Danner) · 고변형 음극 화학-기계 (DEM 쪽 · 읽기만): `kim2023_chemomech_failure_highstrain_anode` · `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review` ([Kang]) · Si 음극 ASSB: `jun2026_ppma_econductive_binder_si_lowpressure_assb` ([Jun26]) · Na 계 외부: `li2026_na_sulfide_halide_interface_review` · `gao2026_sib_electrolyte_ai_review`.

> **본 digest 에서 실제로 본 그림 (2026-10-05)** — 크롭 **48장**(본문 6 + SI 35 + 표 7, 손 크롭 2 포함) 중 **34장**:
> 본문 `Fig. 1`–`Fig. 6` **6/6** (확대: `Fig. 1b` · `Fig. 3` F 1s · `Fig. 5d,e` · `Fig. 6b`) · SI 26장 `Fig. S3` `S5` `S6` `S7` `S8` `S9` `S10` `S11` `S12` `S13` `S14` `S15` `S21` `S22` `S23` `S25` `S26` `S27` `S28` `S29` `S30` `S31` `S32` `S33` `S34` `S35` · 표 2장 `Table S1`·`Table S3` (이미지로 확인 — 값은 PDF 텍스트에서 옮겼다).
> **안 본 것**: `Fig. S1` · `S4` · `S16` · `S17` · `S18` · `S19` · `S20` · `S24` (캡션·본문 서술만) · `Fig. S2` 는 SI p.3 쪽 렌더(110 dpi)로만 · `Table S2`·`S4`–`S7` 은 텍스트로만.
> **그림이 본문과 어긋난 곳 (상세 §10)**: ① `Fig. 5d,e` 의 **NaBi(100)·Na₃Bi(100) 열 표지가 `Fig. S26` 과 뒤바뀐 것으로 보인다** ② `Fig. 5c` 세로축에 **눈금이 없다**(축 끊김 2) — 환원전위 숫자는 논문 어디에도 없다 ③ `Fig. S27a` — 본문 *"at all tested potentials … significantly lower"* 인데 0.01 V 에서 figure-read ≈−0.83 vs ≈−0.73 µA, 차이는 **합금 평탄 전위(0.5·0.7 V)에 몰려 있다** ④ `Fig. S5b` — 본문 *"<30 % … within ∼20 cycles"* 인데 20 사이클 figure-read ≈49 % ⑤ `Fig. 6b` TEGDME 탈나트륨화 평균선 figure-read ≈0.34 ↔ `Table S5` 0.26 ⑥ `Fig. 6d–f` 응력 색막대 10¹¹ Pa — `Table S3` 값으로 낼 수 있는 완전구속 상한(≈4×10¹⁰ Pa, 우리 산수)보다 크다 ⑦ `Fig. 3` F 1s — 본문 *"slightly higher"* 인데 NaₓPF_y:NaF 봉우리 높이비 figure-read ≈9 (EC/PC) vs ≈1 (TEGDME 10 사이클) ⑧ `Fig. S25b` g(r) 를 적분하면 EC/PC 의 Na–PF₆ 접촉이 `Fig. 5a`(15.8 %)보다 훨씬 많다 (우리 산수).
> 그림에서만 읽은 값은 **`figure-read ≈`**, 논문에 없는 우리 계산은 **(우리 산수)** 로 표시했다.

> **동영상 (Movie S1–S3, 각 5.0 s · 1920×1080 · 30 fps)** — ⚠ **직접 재생하지 못했다. 고르게 뽑은 정지 프레임 8장씩만 봤다** (부모 세션 제공 · 레포에 넣지 않음). SI 에 동영상 캡션은 **없다**. 본문 p.8 한 문장이 전부다: *"Movies S1–S3 show the overlaid 3D distribution of Bi and SEI components, including C, F, and P."* 프레임 제목으로 대응을 확인했다: `Sup2` = Movie S1 = **"EC/PC-10 cycles"** · `Sup3` = Movie S2 = **"TEGDME-10 cycles"** · `Sup4` = Movie S3 = **"TEGDME-100 cycles"**. 세 편 모두 APT 바늘 하나를 세로축 둘레로 돌리는 영상이고, 한 화면에 3 패널(Bi 30 at% + C 20 at% · Bi 30 at% + F 10 at% · Bi 30 at% + P 1 at% 등농도면)이다. `Fig. 4e,h`·`Fig. S21` 이 그 정지 화면이다. EC/PC-10·TEGDME-100 프레임에는 30 nm 축척 막대가 있고, **TEGDME-10 프레임에는 없다**(본 프레임 범위에서).

---

## 0. 이 digest 를 읽는 법 — 우리 축과의 관계 먼저

이 논문은 **액체 전해질 Na 이온 전지의 합금 음극(Bi, 검증용 Sn)** 논문이다. 우리 캠페인(황화물 고체전해질 LPSCl 계열 · DFT/MLIP-MD)과 **계도 다르고 양도 다르다** → **[외부]**, 물성 4축(A–D)에 수치로 넣지 않는다.

그래도 읽을 값이 있는 자리는 셋이다.

1. **SEI 를 '조성' 이 아니라 '반응 속도' 로 읽자는 주장.** 우리 음극 계면 자산은 0 K 산물표·갭(조성 쪽)뿐이고 시간축이 없다 (`comparison_vs_ours.md` §H 첫 행). 이 논문은 같은 공백을 액체 쪽에서 실측 지표(정전위 유지 누설전류)와 짧은 AIMD 로 메우려 했다 — 그 시도의 강점과 교락을 같이 본다.
2. **짧은 AIMD 의 '무반응' 판정.** 5 ps · 298 K 에서 분해가 안 보였다는 것을 "TEGDME 는 안정하다" 의 근거로 쓴다. 우리 T3(Li‖LPSCl 반응 MD, 350 K · ≥20 ns) 계획도 같은 함정에 걸릴 수 있다 → §5.5 관측창 검산.
3. **위상장으로 "SEI 두께 → 핵생성 밀도 → 입계 밀도 → 미분화" 를 보이는 방식** — DEM/연속체 쪽 관심사다. 단 이 모형은 SEI 를 고정된 층으로 넣고, 파괴 모형이 없고, 응력 크기가 물리적이지 않다 → 정성 그림으로만 쓴다.

| 논문 주장 | 무엇이 받쳐 주나 | 판정 (§6.8) |
|---|---|---|
| TEGDME 에서 Bi 는 오래 살고, EC/PC 에서는 10 사이클 안에 죽는다 | `Fig. 1b` · `Fig. S3b` · `Fig. S5` (필름·분말·완전셀) | ✅ 강하다 (세 형태에서 재현) |
| EC/PC 는 10–20 nm Bi + 두꺼운 SEI (치밀), TEGDME 는 µm Bi + 얇은 SEI (다공) | `Fig. 2` · `Fig. 4` · `Fig. S10`·`S13`·`S14` · `Fig. S22`·`S23` | ✅ 형태 대비는 분명 (시야 1–2 개 · 크기 통계 없음) |
| 그 차이의 '지배 요인' 은 SEI 조성이 아니라 **전해질 계면 반응성** | 누설전류 `Fig. S27` · 분자 DFT `Fig. 5c` · AIMD `Fig. 5d,e` | ⚠ **교락** — 전해질이 2 종뿐이라 반응성·용매화·유전율·SEI 두께·SEI 조성비가 한꺼번에 바뀐다. 누설전류에는 미분화 뒤 면적과 잔류 합금 전류가 섞인다 |
| 두꺼운 SEI → 균일 Na 유속 → 핵 많음 → 입계 많음 → 미분화 | 위상장 `Fig. 6` · `Table S5`–`S7` | ⚠ **가정이 결론을 만든다** — SEI 두께·균일도를 입력으로 넣고, 파괴·SEI 성장·반응성은 모형에 없다. 반쪽 사이클 둘을 서로 다른 초기 원판에서 따로 돌렸다 |
| Sn 에서도 같다 → 일반 원리 | `Fig. S33`–`S35` | △ 방향은 같다 · 25 사이클 · EC/PC 의 Sn 은 가역 용량이 이론의 ≈21 % 뿐 |

⇒ **가져갈 것**: ① 관측창 한 줄 (짧은 MD 의 '무반응' 은 장벽 상한일 뿐이다) ② 반응 속도를 재는 실험 지표(정전위 유지 누설전류)와 그 교락 목록 ③ 그림·표 정합 검산의 반례 묶음 (§10). **가져가지 않을 것**: 용량·저항·두께·조성·응력 숫자 전부 (Na 액체 계).

---

## 1. 한 줄 요약

1 M NaPF₆ 를 **EC/PC(1:1 vol)** 와 **TEGDME** 에 녹인 두 전해질에서, ~10 µm 전착 Bi 필름과 상용 Bi 분말 전극(~3.6 mAh cm⁻²)은 TEGDME 에서 **>99 % 유지(필름 >150 · 분말 250 사이클)**, EC/PC 에서 **10 사이클 안에 <20 %** 로 무너진다. 저자들은 SEM·3D-XRM·cryo-TEM·APT·XPS·ToF-SIMS 로 EC/PC 쪽이 **10–20 nm Bi 가 두꺼운 SEI 에 박힌 치밀 전극**, TEGDME 쪽이 **µm Bi 에 얇은 SEI 가 덮인 다공 전극**임을 보인다. 고전 MD·분자 DFT·5 ps AIMD·누설전류로 **EC/PC 가 Bi·NaBi·Na₃Bi 위에서 더 반응적**이라고 판단하고, 위상장으로 "두꺼운 SEI → 핵 많음 → 입계 많음 → 미분화" 를 그려 **"전해질 계면 반응성이 합금 음극 미분화를 지배한다"** 고 결론한다. Sn 에서 같은 경향을 확인했다.

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 동기 | 합금 음극은 부피 변화로 금이 가고 새 표면에 SEI 가 계속 자란다. 지금까지의 해법은 "얇고 단단한 NaF/LiF-rich SEI" 를 만드는 전해질 설계였다. 그런데 SEI 는 *"only kinetically stable"* 하고 첨가제가 떨어지면 기능을 잃는다 → *"As with survivorship bias, it is therefore imprudent to focus solely on SEI composition or structure"* (p.2) |
| 질문 | ① 전해질 분해 경로가 다르면 결정립 미세화·입자 균열(핵 크기·응력)이 어떻게 달라지나 ② 전해질–전극 상호작용이 균열과 함께 전극 형태를 어떻게 바꿔 성능 열화로 이어지나 |
| 모형계 | **Bi** (Bi → NaBi(≈0.7 V) → Na₃Bi(≈0.5 V) vs Na/Na⁺ · 부피 변화 *"∼360 %"*) · 검증 **Sn** (0.2–0.5 V · NaSn·Na₉Sn₄·Na₁₅Sn₄) |
| 대조 설계 | **같은 염·같은 농도**(1.0 M NaPF₆), 용매만 EC/PC(1/1 vol%) ↔ TEGDME — **전해질 2 종** |
| 연구유형 | 실험 주 + 계산 보조 (MD · 분자 DFT · AIMD · 위상장) |
| 본문 구성 | §2 전기화학(`Fig. 1`) → §3 구조(`Fig. 2`) → §4 SEI 조성·분포(`Fig. 3`·`Fig. 4`) → §5 계면 반응성(`Fig. 5`) → §6 위상장(`Fig. 6`) → §7 Sn → §8 Discussion → §9 Methods |
| 편집 흔적 | SI Note S1 이 전해질을 두 번 **"LiPF₆-EC-PC · LiPF₆-tetraglyme"** 로 적는다 (본문·`Table S2` 는 NaPF₆ — 복붙 흔적) · `Figure S12` 캡션 "XRD images" (실제 XRM) · `Figure S3` 캡션 "Bi power electrodes" (powder) · `Table S5` 제목 "Na₃Bi grain size during … desodiation" (탈나트륨화 열은 Bi 결정립) · 본문 p.12 *"maximium, minium, average, and mean"* |

---

## Figure set

> ⓘ 이 표를 §3 앞에 둔 이유: 웹 화면의 그림 주석은 파일 **순서대로 그림당 3 개까지만** 모은다 (`webapp/data.py::paper_figure_notes`). 그림을 인용하는 소제목이 표보다 앞에 오면 이 표의 행이 밀려난다.

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a,b | 필름 1·2 사이클 곡선 (0.1 C; 1회차 단일 평탄 figure-read ≈0.51 V(TEGDME)/≈0.46 V(EC/PC), 2회차 ≈0.7·≈0.5 V 두 평탄) · 사이클 (0.3 C, 그림 끝 ≈148 사이클): TEGDME figure-read ≈335–345 mAh g⁻¹ 유지 / EC/PC ≈321 → ≈359 → … → ≈75 (10회) · CE EC/PC figure-read ≈83 → ≈92 → ≈60 (3회) → ≈78 % (10회), TEGDME ≈97 → ≈100 % | 실패 속도 대비의 원자료. ⚠ 본문 ">150 cycles" ↔ 그림 끝 ≈148 · "<20 % within 10" ↔ 10회 figure-read ≈21–23 % |
| 1c,d | 5회차 정규화 방전곡선 (EC/PC 평탄 셋 figure-read ≈0.68/≈0.49/≈0.41 V + 끝 기울기 = '고용체 유사' · TEGDME 평탄 둘 + 수직 끝 = 2상) · dQ/dV (EC/PC Na₃Bi 봉우리 ≈0.48 → ≈0.41 V, NaBi 봉우리 소멸 · TEGDME 100회까지 ≈0.50/≈0.70 V 고정) | 곡선 모양(2상 vs 고용체 유사)으로 입자 크기를 읽는 전기화학 진단 |
| 1e–h | 상별 용량 기여 파이·추이. EC/PC (2·5·7·10회): NaBi 27.5 → 12.3 → 0 → 0 % · Na₃Bi 72.5 → 69.8 → 55.1 → 30 % · 손실 0 → 17.9 → 44.9 → 70 %. TEGDME: NaBi 32.1–32.6 % · Na₃Bi 67.9 → 65.2 % · 손실 ≤2.2 % (100회) | 이론 33.3/66.7 % 대비 — '죽은 NaₓBi' 누적의 정량 표현 |
| 2a–d | 10회 뒤 SEM (EC/PC 매끈하고 둥근 덩어리 / TEGDME figure-read 0.3–1 µm 해면 망) · 3D-XRM (EC/PC 치밀층에 가는 균열 / TEGDME 입자·기공) | 다공 vs 치밀 — DEM 쪽 '전극 구조 진화' 정성 그림 |
| 2e–h | cryo-TEM: EC/PC ≈10–20 nm Bi (SAED 고리 110·012) 가 저대비 껍질 안 / TEGDME 큰 결정 Bi (d₀₁₂ 0.328 nm · [42-1] 점무늬) | 미분화 크기의 직접 증거 — 시야 1–2 개, 크기 분포 없음 |
| 3 | XPS C 1s·F 1s·P 2p (EC/PC 10 · TEGDME 10 · TEGDME 100). C 1s CO₃ ≈290.1 · COO ≈289 · C–O ≈286.8 · C–H ≈285 eV · F 1s NaₓPF_y ≈687.1 · NaF ≈683.8 · P 2p ≈137.7 eV (본문). 봉우리 높이비 NaₓPF_y:NaF figure-read ≈9 / ≈1 / ≈2.5 · C–O:C–H ≈0.7 / ≈0.34 / ≈0.47 | ⚠ 세로축 눈금 없음 → 시료 간 '양' 비교 불가. 본문 "slightly" 는 그림보다 작게 말한다 |
| 4a–d | cryo-STEM + EDS (P·Na·F·O·C 겹침 + Bi·C 맵, 축척 200 nm): EC/PC 는 Bi 가 넓은 C 영역 안에 흩어짐 / TEGDME 는 큰 Bi 입자(figure-read ≈0.5×0.9 µm) 위에 SEI 가 겹침 | SEI 공간분포의 2D 증거 |
| 4e–j | APT 바늘 (높이 figure-read ≈130–180 nm): 등농도면 Bi >30 at%(보라) · <30 at%(회색) · F >10 · C >20 at%. 평균조성 EC/PC Bi-rich Bi 42.1 / C 53.3 / F 3.7 · SEI-rich 33.7 / 60.8 / 4.4 at% ("continuum-like") · TEGDME Bi-rich 84.7 / 8.3 / 7.0 · SEI-rich 23.1 / 59.7 / 17.2 at% ("discrete") | 🔴 `Table S1` EC/PC 행 내부 모순 (§3f) · Na·O·H 미보고 · 조건당 바늘 1 개 |
| 5a,b | 고전 MD 용매화 분포: EC/PC SSIP 84.2 · CIP 12.5 · AGG 3.3 % / TEGDME 92.5 · 7.1 · 0.4 % | 🔴 `Fig. S25b` g(r) 적분과 안 맞는다 (EC/PC Na–P 배위수 ≈0.6–0.8, 우리 산수) |
| 5c | 분자 DFT 환원전위 서열 (위에서부터 Na⁺-3EC3PC ≈ NaPF₆-3EC2PC > EC > Na⁺-6EC > PC ≫ Na⁺-TEGDME ≫ TEGDME) | 🔴 **세로축 눈금 0 · 축 끊김 2** — 값이 없다. 인용 불가 |
| 5d,e | AIMD 5 ps 뒤 스냅샷 — Bi(100)·NaBi(100)·Na₃Bi(100) × EC/PC·TEGDME | 🔴 NaBi·Na₃Bi 열 표지가 `Fig. S26` 과 뒤바뀐 것으로 보인다 · 분해 정량(끊긴 결합 수·전하 이동) 없음 |
| 6a–c | 위상장 핵생성 (입자 가장자리 고리) · 결정립 지름 상자그림 (R 정규화) · 상대 입계 수 밀도 (EC/PC figure-read ≈1.6 나트륨화 · ≈2.7 탈나트륨화, TEGDME = 1) | 정성 그림. ⚠ `Fig. 6b` 와 `Table S5` 불일치 2 곳 · 입계 '밀도' 정의 없음 |
| 6d–f | '압력'·σ 분포 (색막대 7.9×10³ … −2.0×10¹¹ Pa · 0 … 1.0×10¹¹ Pa · σ₁ 0 … 2.0×10¹¹ Pa) | 🔴 크기는 해석 불가 (§10-5) · 캡션 σx ↔ 색막대 σ₁ |
| 6g | 반응성 → SEI 두께 → 입계 밀도 → 미분화 도식 | 결론 도식 — 모형이 실제로 계산한 범위보다 넓다 |
| S1 | 전착 Bi 필름 SEM (안 봄 — 캡션) | — |
| S2 | 전착 Bi 필름 3D-XRM (~10 µm) (쪽 렌더 저해상으로만 봄) | 초기 두께 기준 |
| S3 | **분말** 전극 1·2회 곡선 + ~0.3 C 사이클: TEGDME figure-read ≈365 mAh g⁻¹ · ≈255 사이클 평탄 / EC/PC ≈355 → ≈45 (≈12회). 1회 방전 EC/PC ≈447 · TEGDME ≈415 mAh g⁻¹ (손 크롭) | 초록 "250 cycles" 의 원자료 |
| S4 | PBA 반쪽셀 두 전해질 (안 봄) | 양극 쪽 대조 |
| S5 | PBA‖Bi 완전셀: 첫 충전 figure-read ≈1.78 mAh cm⁻² · 방전 EC/PC ≈1.15 · TEGDME ≈1.36 · 유지율 TEGDME ≈93 % @100 / EC/PC ≈49 % @20 · ≈27 % @30 · ≈5 % @67 | Na 대극 효과 배제 대조 · ⚠ 본문 "<30 % within ∼20 cycles" · ">91 % over 120 cycles" 와 그림(축 100 사이클) 불일치 |
| S6 | in-situ XRD (EC/PC 만) 완전 탈나트륨 상태 1·3·5회: 1회차에 Bi(012) ≈27° + NaBi·Na₃Bi, 3·5회차엔 Bi 봉우리 없음 | '죽은 NaₓBi' 의 구조 증거 · ⚠ Methods 2θ 15–30° ↔ 그림 ≈16–47° · TEGDME 대조 없음 |
| S7 | Na‖Bi EIS (인쇄값): EC/PC 1회 R_SEI 33.9 · R_ct 102 Ω → 10회 180.0 (b) / 180.8 (e) · 765 Ω / TEGDME 1회 2.3 · 8.9 → 10회 3.2 · 10.6 Ω | 비 ≈15 → ≈56 배 (R_SEI, 우리 산수) · Ω 미정규화 (전극 면적 미기재) |
| S8 | Na‖Na 대칭셀 EIS: 두 전해질 모두 반원 figure-read ≈4 Ω | Na 대극 기여는 작다 |
| S9 | 1회 뒤 SEM: EC/PC 매끈 + 드문 기공 / TEGDME 갈라진 덩어리 + µm 기공 | — |
| S10 | 10회 뒤 SEM + 단면: EC/PC ≈67 µm (그 위 figure-read ≈100 µm 층은 설명 없음 — 분리막 섬유가 보인다) / TEGDME ≈25 µm | 두께가 SEM ↔ XRM 에서 다르다 (§3d) |
| S11 | 첫 나트륨화 뒤 XRM: 두 전해질 모두 ≈30 µm (≈3×) | "부피 팽창은 전해질과 무관" 의 근거 |
| S12 | 1회 뒤 XRM ("XRD" 는 오기): EC/PC ≈50 µm 성긴 다공 / TEGDME ≈30 µm | — |
| S13 | 10회 뒤 XRM EC/PC: 치밀 ≈50 µm (단면 셋 figure-read 35–57 µm) | — |
| S14 | 10회 뒤 XRM TEGDME: 다공 ≈44 µm (다공부 figure-read ≈47 µm) | — |
| S15 | 100회 뒤 XRM TEGDME: 위 치밀 · 아래 다공 (본문 ≈50 µm · 단면 figure-read ≈40 µm, 경계 불확실) | 장기에는 TEGDME 도 치밀해진다 |
| S16 | 100회 뒤 cryo-TEM TEGDME (안 봄) | — |
| S17, S18, S19 | cryo-TEM + EDS 전 원소 맵 (EC/PC 10 · TEGDME 10 · TEGDME 100) (안 봄 — 본문 서술만) | — |
| S20 | APT 10회 전 이온 재구성 (안 봄) | — |
| S21 | APT TEGDME 100회: P(>1 at%)·F·C 와 Bi 의 섞임 · Bi-rich / SEI-rich (높이 figure-read ≈170 nm) | 장기 SEI 성장의 3D 그림 · 바늘 1 개 |
| S22 | XPS 깊이 분석 0/40/210 s: TEGDME 는 0 s 부터 Bi⁰ 가 보이고 40 s 에 P·F 소멸 / EC/PC 는 210 s 까지 P·F 남음 | 두께 차의 앙상블 증거 · 세로 눈금 없음 · nm 환산 없음 |
| S23 | ToF-SIMS 깊이: Bi⁺ 는 TEGDME 가 높음 / P⁻·NaF₂⁻ 는 EC/PC 가 250 s 내내 높고 TEGDME 는 처음부터 ≈0 | EC/PC SEI 는 250 s 안에 안 뚫렸다 — '두께' 값은 없다 |
| S24 | 고전 MD 스냅샷 (안 봄) | — |
| S25 | 용매·착물 구조 + g(r): Na–O 첫 봉우리 figure-read ≈0.24 nm (EC ≈13.8 · PC ≈15.3 · TEGDME ≈16) · Na–P EC/PC ≈0.34 nm (g ≈9.4) / TEGDME ≈0.35 nm (g ≈0.6) + ≈0.74 nm (g ≈4.0) | 🔴 EC/PC Na–P 배위수 ≈0.6–0.8 (우리 산수) ↔ `Fig. 5a` CIP+AGG 15.8 % · TEGDME 는 정합 (≈0.06 ↔ 7.5 %) |
| S26 | AIMD 초기 구조 6개 (Bi · Na₃Bi · NaBi × 두 전해질) | `Fig. 5d,e` 표지 대조의 기준 |
| S27 | 누설전류 (손 크롭). 정상상태 figure-read (µA, 0.01/0.05/0.1/0.2/0.3/0.4/0.5/0.6/0.7/0.8 V): EC/PC −0.83 · −1.0 · −1.4 · −2.0 · −2.9 · −6.9 · −12.0 · −0.9 · −5.6 · −1.6 / TEGDME −0.73 · −0.5 · −0.4 · −0.5 · −0.9 · −1.6 · −2.5 · −0.3 · −0.8 · +0.17. 원자료 30 h 유지: EC/PC 0.4 V 최저 ≈−250 µA @≈2 h · TEGDME 0.5 V ≈−770 µA @≈0.3 h | 🔴 차이가 0.5·0.7 V (합금 평탄)에 몰림 · 0.01 V 에선 거의 같다 · 면적 미정규화 |
| S28 | 위상장 셀 (원기둥 Bi + 두께 고르지 않은 SEI + 전해질) | 입력 기하 |
| S29, S30 | 나트륨화 스냅샷: 두꺼운 SEI (작은 결정립 고리) / 얇은 SEI (적고 긴 결정립) — 둘 다 **가장자리 고리만** 변태 | 초기 단계만 계산됐다 |
| S31, S32 | 탈나트륨화 스냅샷 — **새 Na₃Bi 원판에서 시작** (나트륨화 결과를 잇지 않음) | 본문 "after a full sodiation–desodiation cycle" 과 어긋남 |
| S33 | Sn: 첫 방전/충전 figure-read EC/PC ≈270/≈175 · TEGDME ≈750/≈665 mAh g⁻¹ · TEGDME 25 사이클 유지, EC/PC ≈22 사이클에 ≈0 | 일반화 시도 — 짧다 |
| S34 | Sn cryo-TEM: EC/PC figure-read ≈150–250 nm 입자 다수 / TEGDME ≈1 µm 덩어리 · FFT Sn 200·10-1 | — |
| S35 | Sn EDS: EC/PC 작은 Sn 반점 + Na·O·C 가 전 시야 / TEGDME 한 덩어리에 SEI 원소가 겹침 | Bi 와 같은 그림 |
| Table S1 | APT 영역별 조성 (Bi/C/P/F at%) — 전사 §3f | 🔴 EC/PC 행의 '전체' 값이 두 영역 값 사이에 없다 (네 원소 모두) |
| Table S2 | 고전 MD 계: 밀도 1.339 / 1.112 g cm⁻³ · 몰비 NaPF₆:EC:PC 50:330:285 / NaPF₆:TEGDME 50:210 | (우리 산수) 7,405 / 8,170 원자 · 상자 ≈4.35 nm · ≈1.01 M |
| Table S3 | 위상장 물성: C₁₁/C₁₂/C₄₄ = Bi 300/100/100 · Na₃Bi 300/100/100 · SEI 30/10/10 · 전해질 0.9/0.3/0.3 GPa · e_c 0.01/0.01/0.01/0 · e₀ 0/0.05/0/0 · ε 1000/100/50/10 · L* 10/10/0/0 | ⛔ 추정 입력값 — 우리 탄성과 비교 금지 |
| Table S4 | 무차원 매개변수: ξ_σ 0.8 · ξ_SEI 0.9 · ω̇₀* 0.01 · ω̇₁* 0.2 · ω̇₂* 0.2 · M_Na*⁰ 1.0 · M_Na⁺*⁰ 0.6 · l₀ 50 nm · D_Na⁺ 7.0×10⁻¹² m² s⁻¹ · V_mol 21.3×10⁻⁶ m³ mol⁻¹ · T 300 K | (우리 산수) t₀ = l₀²/D ≈ 0.36 ms · R²/D ≈ 2.9 s |
| Table S5 | 결정립 Dmax/Dmin/Dave (÷R, R = 90 l₀): 나트륨화 얇은 1.0/0.22/0.61 · 두꺼운 0.44/0.20/0.31 · 탈나트륨화 얇은 0.83/0.097/0.26 · 두꺼운 0.29/0.05/0.17 | 물리 단위로 2.7 vs 1.4 µm · 1.2 vs 0.77 µm (우리 산수) |
| Table S6, Table S7 | 입자 크기 (R = 30/50/70/90 l₀) 별 탈나트륨화 Bi 결정립 Dave/R — 얇은 SEI 0.170/0.156/0.175/0.26 · 두꺼운 SEI 0.140/0.153/0.171/0.171 | R = 50·70 l₀ 에서 얇은/두꺼운 차 ≤2 % — 효과가 크기에 견고하지 않다 |

---

## 3. 핵심 수치 총정리 ★

> 전위는 전부 **vs Na/Na⁺**. 셀은 따로 적지 않으면 CR2032 반쪽셀 · Na 금속 대극 · 0.01–1.0 V · C/3 · 실온 · 전해질 ~80 µL.

### 3a. 전기화학 (`Fig. 1`, `Fig. S3`, `Fig. S5`)

| 전극 / 셀 | 조건 | TEGDME | EC/PC | 출처 |
|---|---|---|---|---|
| Bi 필름 (전착 ~10 µm on Cu) | 1·2회 0.1 C (`Fig. 1a` 표기) · 이후 0.3 C | 탈나트륨 **~370 mAh g⁻¹** · **>99 % @ >150 사이클** (그림 끝 ≈148) | 가역 **~321 mAh g⁻¹** · **<20 % within 10** (figure-read 10회 ≈75 mAh g⁻¹ = 1회 321 의 ≈23 %) | p.3 · `Fig. 1a,b` |
| Bi 분말 (45 µm · Super P/CMC/SBR 90:5:2.5:2.5 · Al 박 · ~10 mg cm⁻²) | ~0.3 C | **~350 mAh g⁻¹** · **>99 % over 250 사이클** | **~357 mAh g⁻¹** · **<20 % within 10** (figure-read ≈12회에 ≈45) | p.3 · `Fig. S3` |
| 면적 용량 | — | 본문 **~3.6 mAh cm⁻²** · `Fig. 1` 캡션 ">3.0" · 서론 "~3" · Methods 목표 "2–3" | 〃 | — |
| PBA‖Bi 완전셀 | 1.6–3.2 V | 본문 **>91 % over 120** · figure-read ≈93 % @100 (축 끝) | 본문 **<30 % within ∼20** · figure-read ≈49 % @20 · ≈27 % @30 | p.3 · `Fig. S5` |
| PBA 반쪽셀 | 2.0–4.0 V | "comparable performance in both" | 〃 | `Fig. S4` (안 봄) |
| 1회 방전 평탄 | 0.1 C | 단일 평탄 figure-read ≈0.51 V | 단일 평탄 ≈0.46 V (더 큰 분극) | `Fig. 1a` |
| CE | 0.3 C | figure-read ≈97 → ≈100 % | figure-read ≈83 → ≈92 (2회) → ≈60 (3회) → ≈78 % (10회) | `Fig. 1b` (±2 %p 판독) |

- 분말 1회 방전 figure-read EC/PC ≈447 · TEGDME ≈415 mAh g⁻¹ — Bi → Na₃Bi 이론 385 mAh g⁻¹ (본문 미기재, 일반값) 을 넘는 몫은 첫 SEI 형성으로 보인다 (우리 해석).
- ⚠ CE 는 본문에 숫자가 없다 — 위 값은 전부 그림 판독.

### 3b. 상 기여 — 죽은 NaₓBi 의 누적 (`Fig. 1d–h`)

| 사이클 | EC/PC NaBi / Na₃Bi / 손실 (%) | TEGDME NaBi / Na₃Bi / 손실 (%) |
|---|---|---|
| 2 | **27.5 / 72.5 / 0** (비 1:2.6, 이론 1:2) | 32.1 / 67.9 / 0 |
| 5 | 12.3 / 69.8 / 17.9 | 32.4 / 66.6 / 1.0 |
| 7 | 0 / **55.1** / **44.9** | 32.6 / 66.3 / 1.1 |
| 10 | 0 / 30 / 70 | 32.6 / 66.2 / 1.2 |
| 100 | — | 32.6 / 65.2 / 2.2 |

- 이론 기여 Bi→NaBi **33.3 %** · NaBi→Na₃Bi **66.7 %**. 본문은 TEGDME 를 *"∼32.6 % and ∼66.4 %"* 로 적는데 66.4 는 어느 파이에도 없다 (경미).
- dQ/dV: EC/PC 는 5회차부터 NaBi 봉우리가 사라지고 Na₃Bi 봉우리가 figure-read ≈0.48 → ≈0.41 V 로 내려간다 (분극 증가). TEGDME 는 100회까지 ≈0.50 · ≈0.70 V 그대로.
- in-situ XRD (`Fig. S6`, EC/PC): 완전 탈나트륨(1.0 V) 상태인데도 1회차에 NaBi(주)·Na₃Bi(소) 가 남고, 3·5회차에는 **Bi(012) 봉우리 자체가 없다** → 본문: NaBi 봉우리의 '소멸' 은 NaₓBi 가 없어서가 아니라 *"diminishing Bi-to-NaBi phase transition"* 때문.

### 3c. 임피던스 (`Fig. S7`, `Fig. S8` — 인쇄값, Ω, 면적 미정규화)

| 셀 | R_s | R_SEI | R_ct |
|---|---|---|---|
| Na‖Bi EC/PC 1회 | 4.8 | **33.9** | **102** |
| Na‖Bi EC/PC 10회 | 5.3 | **180.0** (`Fig. S7b`) / **180.8** (`Fig. S7e`) | **765** |
| Na‖Bi TEGDME 1회 | 7.6 | **2.3** | **8.9** |
| Na‖Bi TEGDME 10회 | 6.2 | **3.2** | **10.6** |
| Na‖Na (둘 다) | — | 반원 figure-read ≈4 Ω (1·10회 비슷) | — |

- 비 (우리 산수): 1회 R_SEI ≈15× · R_ct ≈11× → 10회 R_SEI ≈56× · R_ct ≈72×. 본문 *"> 10 times higher"* (1회) ✓.
- 등가회로: R_s + (CPE_SEI‖R_SEI) + (CPE_ct‖R_ct + Z_W). 주파수 0.01–10⁵ Hz.

### 3d. 형태 · 두께 (`Fig. 2`, `Fig. S9`–`S16`)

| 상태 | EC/PC | TEGDME | 기법 |
|---|---|---|---|
| 전착 직후 | ~10 µm 치밀 다결정 Bi | 〃 | SEM · XRM |
| 첫 나트륨화 뒤 | ~30 µm (≈3×) · 치밀·주름 | ~30 µm | XRM (`Fig. S11`) |
| 1회 뒤 (탈나트륨) | ~50 µm · 성긴 작은 입자 + SEI 가 빈틈 채움 | ~30 µm · 큰 입자 조밀 + 얇은 SEI | XRM · SEM (`Fig. S9`·`S12`) |
| 10회 뒤 | **~67 µm** (SEM 단면) ↔ **~50 µm** (XRM) · 기공 없음 | **~25 µm** (SEM 단면) ↔ **~44 µm** (XRM) · 다공 | `Fig. S10` ↔ `Fig. S13`·`S14` |
| 100회 뒤 | — | ~50 µm (본문) · 위 치밀 / 아래 큰 덩어리·기공 (단면 figure-read ≈40 µm) | XRM `Fig. S15` |
| 입자 크기 (10회) | **10–20 nm** 다결정 Bi (SAED 고리) · Discussion 은 "∼10 nm" | "micro-sized" 결정 Bi · `Fig. 4c` 입자 figure-read ≈0.5×0.9 µm · SEM 망 굵기 figure-read ≈0.3–1 µm | cryo-TEM · STEM · SEM |

- ⚠ 같은 상태의 두께가 **기법·시료마다 1.5–1.8 배** 다르다 (EC/PC 67 vs 50 · TEGDME 25 vs 44 µm). 통계(여러 시료·여러 위치) 없음.

### 3e. SEI 화학 — XPS (`Fig. 3`, `Fig. S22`)

| 성분 | 결합에너지 (본문) | EC/PC 10 | TEGDME 10 | TEGDME 100 |
|---|---|---|---|---|
| CO₃ (알킬 카보네이트) | ∼290.1 eV | 있음 | 없음 | 없음 |
| O–C=O (폴리에스터) | ∼289 eV | 있음 | 있음 | 있음 |
| C–O (폴리에터) | ∼286.8 eV | 큼 | 작음 | 중간 |
| C–H | ∼285 eV | 있음 | 큼 | 큼 |
| F 1s NaₓPF_y / NaF | ∼687.1 / ∼683.8 eV | 높이비 figure-read ≈9 | ≈1 | ≈2.5 |
| C–O : C–H (성분 높이) | — | figure-read ≈0.7 | ≈0.34 | ≈0.47 |
| P 2p NaₓPF_y | ∼137.7 eV | 뚜렷 | 약함 (기준선 잡음 큼) | 뚜렷 |

- 기준: C 1s 284.8 eV · CasaXPS Shirley. 깊이 분석 (`Fig. S22`): 500 eV Ar⁺ · 2×2 mm² · 0/40/210 s (Methods 는 "총 ~300 s"). TEGDME 는 0 s 부터 Bi⁰ 가 보이고 40 s 에 P·F 가 사라진다. EC/PC 는 210 s 에도 P·F 가 남고 Bi 신호가 약하다.
- ⚠ 세로축 눈금이 어느 패널에도 없다 → 시료 사이 '양' 비교 불가. 위 비율은 한 스펙트럼 안의 성분 높이비(면적 아님)다.

### 3f. APT 영역 조성 (`Table S1` 전사 · at%, Bi+C+P+F 로 정규화 · 등농도면 Bi 30 at% 로 분할)

| 전해질 | 영역 | Bi | C | P | F |
|---|---|---|---|---|---|
| TEGDME 10회 | 전체 | 73.2 | 16.9 | 0.0 | 9.9 |
| 〃 | Bi-rich | **84.7** | 8.3 | 0.0 | 7.0 |
| 〃 | SEI-rich | 23.1 | 59.7 | 0.0 | 17.2 |
| EC/PC 10회 | 전체 | **66.80** | **30.9** | **0.4** | **1.8** |
| 〃 | Bi-rich | 42.1 | 53.3 | 0.9 | 3.7 |
| 〃 | SEI-rich | 33.7 | 60.8 | 1.0 | 4.4 |
| TEGDME 100회 | 전체 | 53.4 | 39.5 | 0.0 | **7.1** |
| 〃 | Bi-rich | 54.7 | 30.4 | 0.0 | 14.9 |
| 〃 | SEI-rich | 22.8 | 60.8 | 0.4 | 15.9 |

- 🔴 **분할 정합 검산 (우리 산수)**: 두 영역이 Bi 30 at% 문턱으로 바늘 전 부피를 나눈다면 '전체' 는 두 영역 값 **사이**에 있어야 한다. TEGDME 10회는 네 원소 모두 ✓. **EC/PC 10회는 네 원소 모두 ✗** (Bi 66.8 > 42.1·33.7 · C 30.9 < 53.3·60.8 · P 0.4 < 0.9·1.0 · F 1.8 < 3.7·4.4). TEGDME 100회는 F 가 ✗ (7.1 < 14.9·15.9). 또 EC/PC 'SEI-rich' 의 Bi **33.7 at% 는 그 영역을 정의한 문턱(<30 at%)보다 높다**. 영역 조성을 부피 평균이 아니라 경계 근처 profile(proxigram) 등으로 냈다면 가능한 일이지만 **방법이 적혀 있지 않다** → EC/PC 행 숫자를 "continuum-like" 의 정량 근거로 쓸 수 없다.
- 본문 서술 (p.8–9): EC/PC 는 Bi-rich/SEI-rich 차가 작아 *"continuum-like microstructure"*, TEGDME 는 *"discrete phase separation"*. 10 → 100회 TEGDME 에서 Bi-rich 의 Bi 84.7 → 54.7 · C 8.3 → 30.4 at% → *"SEI grows gradually while Bi particles progressively break down"*.
- ⚠ **Na · O · H 를 보고하지 않는다** (SEI 주성분 NaF·Na 알킬카보네이트의 Na·O 가 빠짐 — 이유 미기재).

### 3g. 누설전류 (`Fig. S27` — 전부 figure-read ≈, µA, 면적 미정규화 · 셀 1 개)

| 전위 (V) | 0.01 | 0.05 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 |
|---|---|---|---|---|---|---|---|---|---|---|
| EC/PC | −0.83 | −1.0 | −1.4 | −2.0 | −2.9 | −6.9 | **−12.0** | −0.9 | **−5.6** | −1.6 |
| TEGDME | −0.73 | −0.5 | −0.4 | −0.5 | −0.9 | −1.6 | −2.5 | −0.3 | −0.8 | +0.17 |
| 비 (우리 산수) | ≈1.1 | ≈2 | ≈3.4 | ≈4 | ≈3 | ≈4.3 | ≈4.8 | ≈3 | ≈7 | — |

- 방법: 형성 3회 (C/10) → C/10 으로 목표 전위까지 방전 → **30 h 정전위 유지** → *y = A·exp(−x/t) + y₀* 맞춤의 **y₀** = 정상상태 누설전류 (Keithley 2401 자체 장치 'HpLC', ANL).
- 원자료 (`Fig. S27b,c`): EC/PC 0.4 V 의 과도전류가 figure-read ≈2 h 에 ≈−250 µA 최저 후 ≈15 h 에 걸쳐 감쇠 · TEGDME 0.5 V ≈−770 µA (≈0.3 h) · 0.7 V ≈−640 µA 가 ≈5 h 안에 감쇠.
- 🔴 **차이가 0.5 V(NaBi→Na₃Bi)·0.7 V(Bi→NaBi) 평탄 전위에 몰려 있다**. Na₃Bi 영역(0.01–0.3 V)에서는 비가 1.1–4 이고 **0.01 V 에서는 거의 같다**. TEGDME 0.8 V 값은 부호가 반대(+0.17) → 측정 바닥이 대략 ±0.2–0.5 µA (우리 해석). `Fig. S27a` 에는 0.01 V 점이 있는데 원자료 범례(0.05–0.8 V)에는 없다.

### 3h. 고전 MD — 용매화 (`Fig. 5a,b`, `Fig. S25`, `Table S2`)

| 전해질 | SSIP | CIP | AGG | Na–O 첫 봉우리 | Na–P |
|---|---|---|---|---|---|
| NaPF₆-EC/PC | **84.2 %** (본문 ∼84) | **12.5 %** | **3.3 %** (본문 ∼3.33) | figure-read ≈0.24 nm (EC g ≈13.8 · PC ≈15.3) | ≈0.34 nm 날카로운 봉우리 g ≈9.4 |
| NaPF₆-TEGDME | **92.5 %** (본문 ">92.5") | **7.1 %** | **0.4 %** | ≈0.24 nm g ≈16 | ≈0.35 nm g ≈0.6 + ≈0.74 nm g ≈4.0 |

- 🔴 **g(r) 적분 검산 (우리 산수)**: `Fig. S25` 의 Na–P 곡선을 픽셀로 디지타이즈해 CN = 4πρ_P∫g r² dr 로 적분했다 (ρ_P = 50 / 상자 부피 · 상자 부피 82.5 nm³ = `Table S2` 밀도·몰비에서). **EC/PC: CN ≈0.62 (r_c 0.40 nm) – 0.79 (0.45) – 0.82 (0.50)** — Na⁺ 의 과반이 PF₆⁻ 와 맞닿아야 하는 값인데 `Fig. 5a` 는 CIP+AGG **15.8 %**. **TEGDME: CN ≈0.06** ↔ 7.5 % — **정합**. 같은 방법으로 한쪽만 3–5 배 어긋난다. 분류 기준(절단 거리·판정 원자)이 미기재라 원인은 모른다 — `Fig. 5a` 의 EC/PC 분율은 인용하지 않는다.
- (우리 산수) `Table S2` 로 계 크기: EC/PC **7,405 원자** · TEGDME **8,170 원자** · 정육면체 환산 한 변 ≈**4.35 nm** (둘 다) · 염 농도 ≈**1.01 M** ✓.

### 3i. 분자 DFT · AIMD (`Fig. 5c–e`, `Fig. S26`)

- 분자 DFT 환원전위: **숫자 0 개**. `Fig. 5c` 는 눈금 없는 세로축에 축 끊김 2 개로 서열만 그렸다 — 위에서부터 Na⁺-3EC3PC ≈ NaPF₆-3EC2PC > EC > Na⁺-6EC > PC ≫ Na⁺-TEGDME ≫ TEGDME. 본문: *"species in EC/PC are significantly more prone to reduction than those in TEGDME"*.
- AIMD: 숫자 0 개 (분해된 분자 수·전하 이동·결합 차수 시계열 없음). 서술: Bi(100) 위에서는 둘 다 눈에 띄는 분해 없음 · EC/PC 는 NaBi 에서 시작해 Na₃Bi 에서 *"very severe"* · TEGDME 는 NaBi·Na₃Bi 위에서 반응이 적지만 *"Na dealloying is observed, particularly in the case of Na₃Bi"*.

### 3j. 위상장 (`Table S5`–`S7`, `Fig. 6b,c`)

| 결정립 (÷R, R = 90 l₀ = 4.5 µm) | 나트륨화 얇은 SEI (TEGDME) | 나트륨화 두꺼운 SEI (EC/PC) | 탈나트륨화 얇은 | 탈나트륨화 두꺼운 |
|---|---|---|---|---|
| Dmax/R | 1.0 | 0.44 | 0.83 | 0.29 |
| Dmin/R | 0.22 | 0.20 | 0.097 | 0.05 |
| Dave/R | **0.61** | **0.31** | **0.26** | **0.17** |
| Dave 물리 단위 (우리 산수) | ≈2.7 µm | ≈1.4 µm | ≈1.2 µm | ≈0.77 µm |
| `Fig. 6b` figure-read | 평균선 ≈0.61 ✓ · 최소 ≈0.22 ✓ | 평균 ≈0.32 ✓ · **최소 ≈0.15** ✗ (표 0.20) | **평균선 ≈0.34** ✗ (표 0.26) · 최대 0.83 ✓ | 평균 ≈0.17 ✓ |

| `Table S6`·`S7` 탈나트륨화 Dave/R | R = 30 l₀ | 50 | 70 | 90 |
|---|---|---|---|---|
| 얇은 SEI | 0.170 | 0.156 | 0.175 | 0.26 |
| 두꺼운 SEI | 0.140 | 0.153 | 0.171 | 0.171 |
| 차 (우리 산수) | 21 % | **2 %** | **2 %** | 52 % |

- 상대 입계 수 밀도 (`Fig. 6c`, TEGDME = 1): EC/PC figure-read **≈1.6** (나트륨화) · **≈2.7** (탈나트륨화). 정의(개수·길이·면적)는 없다.
- 결정립 크기 대비: 모형 1.5–2 배 (얇은/두꺼운) vs 실험 µm vs 10–20 nm (≈10² 배) — 방향만 맞는다.

### 3k. Sn (`Fig. S33`–`S35`)

- 첫 가역 용량: EC/PC **∼175 mAh g⁻¹** · TEGDME **∼667 mAh g⁻¹** (= Na₁₅Sn₄ 이론 **847 mAh g⁻¹** 의 **∼79 %**). EC/PC 의 가역 용량은 이론의 ≈21 % (우리 산수 · 첫 방전 figure-read ≈270 mAh g⁻¹ 도 ≈32 %).
- 사이클: TEGDME 25 사이클 figure-read ≈665–690 유지 · EC/PC 2회 ≈192 → ≈22회 ≈0.
- cryo-TEM 10회: EC/PC *"nanorod-shaped"* Sn (그림에서는 ≈150–250 nm 둥근 입자가 주로 보인다, figure-read) · TEGDME µm 입자 유지. EDS: EC/PC 는 작은 Sn 반점 위로 Na·O·C 가 전 시야를 덮고, TEGDME 는 한 덩어리에 얇게 겹친다.

---

## 4. 실험 방법 — 원문 요약 (§9.1–9.3)

| 항목 | 내용 |
|---|---|
| Bi 필름 | 정전류 전착 10 mA cm⁻² · 0.2 M Bi₂O₃ + 2.5 M 메테인설폰산 · 실온 · 500 rpm · Cu 박(0.025 mm)을 10 % H₂SO₄ 10 min 세정 · 목표 2–3 mAh cm⁻² (12–18 min) |
| Sn 필름 | 15 mA cm⁻² · 0.15 M Sn₂P₂O₇ + 0.8 M K₄P₂O₇ + 0.25 M H₃BO₃ + 젤라틴 1 g L⁻¹ · 50 °C · 1000 rpm · 8–12 min |
| 분말 전극 | Bi·Sn 분말 45 µm (325 mesh) : Super P : CMC : SBR = 90:5:2.5:2.5 · 물 · **Al 박** · 120 °C 진공 · ~10 mg cm⁻² |
| PB 양극 | PB 분말(Altris) : Super P : CMC : SBR = 90:3:3:4 · Al 박 · 140 °C (로딩 미기재) |
| 셀 | CR2032 · Ar 글러브박스 O₂·H₂O <1 ppm · Na 금속 99.5 % · **1.0 M NaPF₆ in TEGDME** / **1.0 M NaPF₆ in EC/PC (1/1 vol%)** (둘 다 Gotion) · **~80 µL** · 분리막 PP Celgard 2500 + 유리섬유 · Arbin · **C/3** · Bi·Sn 0.01–1.0 V · PB 2.0–4.0 V · PB‖Bi 1.6–3.2 V (N/P 미기재) |
| EIS | Biologic VSP · 0.01–10⁵ Hz · Na‖Na 0.7 mA cm⁻² · ~3 mAh cm⁻² (반쪽셀과 방전 깊이 맞춤) |
| 누설전류 | §3g |
| SEM | Helios NanoLab 600i · 탄소 5 nm 코팅 |
| 3D-XRM | Zeiss Versa 610 · 360° 3201 투영 · 20× (70 kV · 8.5 W · 4 s) / 40× (8 s) · 흡수대비 |
| XPS | Nexsa · Al Kα 1486.6 eV · 72 W · 통과 50 eV · 200 µm · 5×10⁻⁹ Torr · C 1s 284.8 eV · CasaXPS Shirley · 깊이: 500 eV Ar⁺ · 2×2 mm² · Ta₂O₅ 식각률 보정 · 총 ~300 s · ⚠ 시료 세척 조건 미기재 |
| in-situ XRD | Empyrean · Cu Kα · GaliPIX3D · MTI 분리형 Be 창 셀 · Bi 필름 on **Cu 메시** · **EC/PC 만** · 0.05–1.0 V · 0.2 C · *"2θ range of 15–30°"* · 3 min/스캔 |
| cryo-(S)TEM | FEI Titan 300 kV (프로브 수차보정) · 용매로 살짝 세척 → lacey C Cu 그리드 → Ar 봉투 → 액체질소 → Gatan Elsa 냉각 홀더 · ~100 K · 저선량 ~1 (저배율) / ~100 e Å⁻² s⁻¹ (HRTEM) · EDS 체류 0.01–0.1 ms · ~40 pA |
| APT | LEAP 4000XHR · 레이저 100 pJ · 125 kHz · 40 K · 검출률 0.3 % · Helios Hydra UX PFIB lift-out · IVAS 3.8 |
| ToF-SIMS | ToF-SIMS V · 양이온: 2.0 keV O₂⁺ ~400 nA 500×500 µm² 스퍼터 + 25 keV Bi⁺ ~1.87 pA 분석 100×100 µm² · 음이온: 1.0 keV Cs⁺ ~137.1 nA 300×300 µm² · 전하보상 10 eV · SurfaceLab 7.2 · 음이온 강도는 ¹⁸O⁻ 로 정규화 |

---

## 5. 계산 방법 ★ (Note S1·S2 원문 · 없는 것은 "미기재")

### 5.1 고전 MD — 용매화 (GROMACS · P. Gao)

| 항목 | 값 |
|---|---|
| 코드 | GROMACS (판 미기재) · 그림 VMD |
| 힘장 | **OPLS-AA** · 편극 효과 대신 **이온 전하 ×0.75** (Na⁺ +0.75 · PF₆⁻ −0.75) |
| 계 | `Table S2`: NaPF₆:EC:PC = **50:330:285** · 1.339 g cm⁻³ / NaPF₆:TEGDME = **50:210** · 1.112 g cm⁻³ (초기 밀도·몰비 = 실험값) · (우리 산수) 7,405 / 8,170 원자 · 한 변 ≈4.35 nm |
| 평형 | **NPT 298 K · 10 ns** · v-rescale (τ 0.2) + Berendsen (τ 2) — τ 단위 미기재 |
| 생산 | **NPT 298 K · 100 ns** · Nosé–Hoover (τ 0.2) + Parrinello–Rahman (τ 2) |
| 상호작용 | vdW 절단 1.2 nm + 장거리 분산 보정 · PME (실공간 1.2 nm) |
| 적분 | dt **1 fs** · 1000 스텝(1 ps)마다 저장 |
| 미기재 | SSIP/CIP/AGG 판정 기준(절단 거리·판정 원자) · 독립 궤적 수 · 힘장 검증(밀도·점도·전도도 대조) · Na⁺·PF₆⁻ LJ 매개변수 출처 · 상자 크기 |
| ⚠ 오기 | SI 문장이 계를 *"LiPF₆-EC-PC and LiPF₆-tetraglyme"* 로 적는다 (본문·표는 NaPF₆) |

### 5.2 분자 DFT — 환원전위 (NWChem · P. Gao)

| 항목 | 값 |
|---|---|
| 코드 · 범함수 | NWChem (판 미기재) · **B3LYP** + **DFT-D3** |
| 기저 | 구조 6-31G** (음이온 6-31++G**) · 단일점 **6-311++G(d,p)** |
| 열역학 | 진동수 → 영점·열 보정 → **298.15 K Gibbs** |
| 용매 | **COSMO** · ε = **7.78** (테트라글라임) / **77.48** (EC-PC 평균) |
| 환원전위 | **E_red = [G(M) − G(M⁻)]/F − 1.73 V** (vs Na/Na⁺; 1.73 V = 절대 Na/Na⁺ 전위, Trasatti 1986 인용) |
| 대상 | EC · PC · TEGDME · Na⁺-6EC · Na⁺-3EC3PC · NaPF₆-3EC2PC · Na⁺-TEGDME (`Fig. S25a`) |
| 결과 | **수치 미보고** (`Fig. 5c` 눈금 없음) |
| 미기재 | 형태(conformer) 탐색 · 환원체 스핀 · 환원 후 결합 개열 여부(단열 vs 수직) · PF₆⁻ 환원 |

### 5.3 AIMD — 계면 반응성 (VASP · P. Gao)

| 항목 | 값 |
|---|---|
| 코드 | VASP (판 미기재) · 그림 VMD |
| 범함수 · 전위 | **PBE** · PAW · ENCUT **400 eV** · Gaussian **0.05 eV** · 전자 수렴 **10⁻⁵ eV** |
| 계 | 6 개 = 전해질 2 × 고체 3 (**Bi · NaBi · Na₃Bi**, MP id 를 *"mp-27838, mp-22924 and mp-23152"* 로 나열 — 상↔id 1:1 대응은 명시 안 됨) · 면 **(100)** (Bi 필름 XRD 주봉 중 하나라는 이유 + 저지수면 안정 — Bi 필름 XRD 는 논문에 없다) |
| 슬랩 | **8 원자층 · 가운데 2 층 고정** |
| 전해질 | 밀도·몰비는 고전 MD 와 같게 · 무작위 배치 → OPLS-AA 고전 MD **100 ps** 사전평형 |
| 앙상블 | **NVT** · Nosé (질량 매개변수 0.1) · **298 K** · dt **1 fs** · **5 ps** · 궤적 1 개/계 |
| 전하 | *"All systems were modeled in neutral states to minimize reactivity"* — 전위 제어 없음 |
| 미기재 | k 점 · 셀 크기 · 원자·분자 수 · 슬랩 종단 · 전해질 층 두께 · 쌍극자 보정 · vdW (AIMD 쪽) · 스핀 · H 질량 · 반복 궤적 · 분해 판정 기준 |
| ⚠ 오기 | 여기서도 *"LiPF₆-EC-PC and LiPF₆-tetraglyme"* |

### 5.4 위상장 — 결정립 핵생성·미분화 (Y. Li · S. Hu · Note S2)

- **상 4 개**: Bi (η₁) · Na₃Bi 다결정 (η₂…η_{n−2}, 방위별) · SEI (η_{n−1}) · 전해질 (η_n). 보존장 c_Na (중성 Na) · c_Na⁺ (Na 이온). Bi 를 기준 격자로 c_Bi = 1, 평형 c_Na = 0 (Bi) / 3 (Na₃Bi), SEI·전해질은 용해도 한계로.
- **자유에너지**: F = ∫[f_intf(η) + f_bulk(η,c) + f_elct(η,c)] dV · f_elct = ρφ · ρ = F_c z c_Na⁺ / V_mol · Poisson ∇·(ε(r)∇φ) + ρ = 0 · μ_Na⁺ 에 F_c z φ / V_mol 항.
- **탄성**: e*_ij = δ_ij Σ_p h_p(η)[e₀⁽ᵖ⁾ + e_c⁽ᵖ⁾(c_Na + c_Na⁺)] (등방 팽창 고유변형) · σ = C(r)(e − e*) · ∇·σ = 0 · **미소변형**.
- **동역학**: Allen–Cahn ∂η/∂t = −L δF/δη · Cahn–Hilliard ∂c_Na/∂t = ∇·(M_Na∇μ) + ω̇ · ∂c_Na⁺/∂t = ∇·(M_Na⁺∇μ) − ω̇ · 이동도 혼합법칙 · **M_Na⁺ = M⁰[1.05 − η₁][1.05 − h][1 − ξ_SEI η_{n−1}][1 − η_n][1 + ξ_σ σ_h/σ_h,max]** (식 12 — 전해질에서 0 · 인장에서 증가) · 반응속도 ω̇ 는 SEI·전해질 안에서 0, 그 밖에서 c_Na⁺{ω̇₀ + ω̇₁·S(η₁) + ω̇₂·S(h)} (S = 0.5 에서 꺾이는 시그모이드 · 식 13) — ω̇₀ = Bi·Na₃Bi 상 안 · ω̇₁ = SEI 와 Bi/Na₃Bi 의 계면 · ω̇₂ = Na₃Bi 입계의 반응속도 상수 (원문 정의) · h = Σ η_p² (Na₃Bi 안 1).
- **핵생성**: 고전 핵생성 이론 3 단계 (후보 자리 탐색 → 확률 → 삽입).
- **수치**: FFT 스펙트럴 · 반암시 시간적분 (Chen & Shen 1998) · 강한 탄성 불균질은 반복법 (Hu & Chen 2001) · 셀 **256 l₀ × 256 l₀ × 4 l₀** (l₀ = 50 nm → 12.8 × 12.8 × 0.2 µm) · 원기둥 Bi **R = 90 l₀ = 4.5 µm** · 3 방향 주기 · Bi 안 φ = 0 · T = 300 K.
- **매개변수**: `Table S3`·`Table S4` (Figure set 행에 전사). 저자 스스로: SEI·전해질 탄성은 문헌에 없고 Na 확산도 직접 측정이 드물어 *"estimated based on available literature values"*.
- **가정** (본문 p.12): ① TEGDME SEI 가 EC/PC 보다 *"thinner, denser, and less homogeneous"* ② SEI–전해질 계면 거칠기는 같다 ③ 나트륨화·탈나트륨화는 확산 지배(전해질 수송·계면 반응은 빠름). 그리고 *"These simulations are intended to illustrate the relative effects of the two SEI scenarios on nucleation density and grain refinement, rather than to provide a fully parameterized predictive model."*
- **미기재**: f_intf·f_bulk 함수형 · 검증 (*"will be provided in our forthcoming simulation study"*, ref 33 = 원고 준비 중) · 코드 이름 · **두 SEI 의 두께 수치** (그림으로만) · 구동력(전류밀도·C-rate·경계 Na⁺ 농도) · 핵생성 매개변수 · 실현(시드) 수 · 스냅샷의 시각 · 파괴 기준 · '입계 밀도' 정의 · ΔQ (D_Na⁺ = D₀exp(−ΔQ/k_BT) 의 활성화 에너지).

### 5.5 관측창 · 시간척도 검산 (`D-2026-09-27-barrier-hop-count` 산식 · ν₀ 10¹³ s⁻¹ **가정**)

이 논문은 **장벽(Ea) 값을 하나도 인용하지 않는다** (위상장의 ΔQ 도 미기재) → 결정의 의무 줄은 해당이 없다. 대신 같은 산식으로 **"이 시간 창에서 한 번이라도 일어날 수 있는 반응의 장벽 상한"** 을 낸다: Ea_max = kT·ln(ν₀·t) (한 반응 자리 · N = 1 기준). 값은 `tools/sei/collect_neb.py::hop_check` 로 냈다.

| 시간 창 | T | Ea_max (N = 1) | 의미 |
|---|---|---|---|
| **AIMD 5 ps** (이 논문) | 298 K | **≈0.10 eV** | 홉 수 검산 (ν₀ 10¹³ s⁻¹ 가정 · 298 K): 0.10 eV → Γ ≈ 2.0×10¹¹ s⁻¹ · 1/Γ ≈ 4.9 ps · 5 ps 동안 N ≈ 1 회 / 0.50 eV → Γ ≈ 3.5×10⁴ s⁻¹ · 1/Γ ≈ 29 µs · 5 ps 동안 N ≈ 1.7×10⁻⁷ 회 |
| 반쪽 사이클 (C/3 ≈ 3 h) | 298 K | ≈1.01 eV | 1.0 eV → Γ ≈ 1.2×10⁻⁴ s⁻¹ · 1/Γ ≈ 8.2×10³ s (≈2.3 h) |
| 누설전류 유지 30 h | 298 K | ≈1.07 eV | 1.0 eV → 30 h 동안 N ≈ 13 회 |
| 고전 MD 100 ns | 298 K | ≈0.36 eV | (반응 없는 힘장 — 참고용) |
| 우리 T3 계획 20 ns | 350 K | ≈0.37 eV | 50 ns 면 ≈0.40 eV |

- ⇒ **5 ps AIMD 의 '무반응' 은 "장벽 ≲0.1 eV 짜리 분해 경로가 없다" 까지만 말한다.** 셀이 실제로 보는 시간(시간–수십 시간)에는 장벽 ≈1 eV 까지의 반응이 일어난다. 0.1–1 eV 사이의 반응은 AIMD 에서 안 보이지만 셀에서는 일어난다 → TEGDME '안정' 의 근거로는 약하고, 실측 누설전류가 더 맞는 증거다 (그것도 §10-2 의 교락이 있다).
- 반응 자리가 n 개면 문턱이 kT·ln n 만큼 오른다 (n = 10 → +0.06 eV @298 K · n = 100 → +0.14 eV @350 K, 우리 산수) — 차수는 그대로다.
- **위상장 시간척**: D_Na⁺ = 7.0×10⁻¹² m² s⁻¹ 로 t₀ = l₀²/D ≈ **0.36 ms**, 입자 반경을 가로지르는 확산 시간 R²/D ≈ **2.9 s** (우리 산수; 고체 안 이동도 감쇠 인자 0.05 를 넣어도 ≈1 분). C/3 반쪽 사이클(≈3 h)보다 10³–10⁴ 배 짧다 → 실험 조건에서 나트륨화가 정말 '확산 지배' 인지(가정 ③)는 이 매개변수로는 성립하지 않는다. 모사의 구동력·시각이 C-rate 와 연결돼 있지 않다.
- ⛔ 차수 검산이지 확산계수·반응속도 상수가 아니다.

---

## 6. 결과 — 절별 상세 (그림 실독)

### 6.1 §2 전기화학 — 같은 Bi, 다른 수명 (`Fig. 1`, `Fig. S3`–`S8`)

- 필름과 분말이 거의 같은 곡선·용량을 낸다 → 전극 구성 요소의 간섭이 작은 모형계라는 근거.
- 1회차는 큰 입자라 0.5 V 근처 **단일 평탄**, 2회차부터 입자가 작아져 0.7·0.5 V **두 평탄** (refs 40·54).
- EC/PC 는 1회차부터 분극이 크다 (방전 평탄이 낮고 충전 평탄이 높다) → 저자: 새로 드러난 Bi 표면과 EC/PC 의 기생반응.
- `Fig. 1c`: 5회차 EC/PC 곡선 끝이 비스듬함 = *"solid-solution-like behavior, which is commonly observed in nano-sized battery materials"* · TEGDME 는 수직 = 2상 반응 (큰 입자). 곡선 모양으로 미분화를 읽는다.
- `Fig. 1e–h`: EC/PC 2회차 비 1:2.6 (이론 1:2) — 비가역이 초기에 시작 · 7회차에 절반 손실 · NaBi 기여 0. TEGDME 는 100회까지 이론비 그대로.
- `Fig. S6`: 탈나트륨 상태에서도 NaₓBi 가 남고 쌓인다 → *"sodium trapped within electrochemically 'dead' NaₓBi accumulates with cycling as pulverized domains lose electrical contact"*.
- `Fig. S7`·`S8`: R_SEI·R_ct 차이는 Bi 전극 쪽에서 온다 (Na‖Na 는 둘 다 ≈4 Ω).
- **핵심 논증 (p.5)**: 두 전해질의 첫 용량이 같고 TEGDME 가 이후 더 큰 용량(= 더 큰 누적 팽창)을 내는데도 더 안정하다 → *"volume change and particle cracking alone cannot explain the electrolyte-dependent behavior"*. 그리고 *"The TEGDME electrolyte contains the same NaPF₆ salt at the same concentration … and does not form a substantially different SEI. By excluding the effects of electrode structural engineering and SEI chemistry, these results indicate that electrolyte interfacial reactivity is the dominant factor"* (§6.8 ③ 에서 판정).

### 6.2 §3 구조 진화 — 다공 vs 치밀 (`Fig. 2`, `Fig. S9`–`S16`)

- 1회 뒤 EC/PC 는 이미 두꺼운 SEI 로 덮여 매끈하고 기공이 드물다. TEGDME 는 큰 덩어리로 갈라지고 µm 기공이 많다 (`Fig. S9`).
- 첫 나트륨화 뒤 두 전해질 모두 ≈30 µm (`Fig. S11`) → *"morphological differences … are not due to volume expansion, which is similar in both cases, but rather to electrolyte decomposition processes"*.
- 10회 뒤: EC/PC 는 기공 없는 치밀층 · XRM 이 입자를 못 가를 만큼 작아짐 (`Fig. 2b`·`S13`) · cryo-TEM 10–20 nm Bi + 두꺼운 저대비 껍질 + SAED 고리 (`Fig. 2e,f`). TEGDME 는 µm 입자 + 기공 + 얇은 SEI + 단결정 HRTEM (`Fig. 2g,h`).
- 100회 뒤 TEGDME 도 표면부가 치밀해진다 — 바닥(집전체 쪽)은 큰 덩어리·기공 유지 (`Fig. S15`).
- 저자 요약 (p.7): EC/PC = *"rapid pulverization, a dramatic increase in electrode thickness … dense morphology"* · TEGDME = *"slow pulverization rate, a gradual increase in electrode thickness, and the progressive solidification of a porous structure"*.

### 6.3 §4 SEI 조성 · 공간분포 (`Fig. 3`, `Fig. 4`, `Fig. S17`–`S23`, Table S1, Movies S1–S3)

- XPS: 두 SEI 의 **주성분은 같다** (폴리에스터·폴리에터·NaₓPF_y·NaF; EC/PC 만 알킬카보네이트 추가). EC/PC 는 C–O·COO·CO₃ 비중이 높고 NaₓPF_y/NaF 가 높다 (figure-read ≈9 vs ≈1) → 저자: EC/PC SEI 가 음이온 분해를 *"slightly less"* 겪는다 — 에터가 카보네이트보다 환원 안정이라 예상대로.
- TEGDME 10 → 100회: C–O/C–H · NaₓPF_y/NaF 둘 다 증가 → 저자: 장기 SEI 는 용매 유래 유기물 비중이 커진다 (⚠ NaₓPF_y 는 **염** 유래 — §10-7).
- cryo-EDS: EC/PC 는 Bi 나노입자 덩어리가 넓은 SEI(C) 영역에 묻힘 · 원소 분포는 거시적으로 균일 (`Fig. S17`, 안 봄). TEGDME 는 SEI 가 Bi 표면에 붙어 있고 원소별로 불균일 (`Fig. S18`, 안 봄) · 100회에 C·O 영역 증가 (`Fig. S19`, 안 봄).
- APT (`Fig. 4e–j`, Table S1, Movies): EC/PC 는 미세한 Bi-rich 영역이 많고 SEI 와 촘촘히 섞임 → *"continuum-like"* · TEGDME 는 Bi-rich 와 SEI-rich 가 뚜렷이 갈림 → *"discrete phase separation"*. 정지 프레임으로 본 동영상도 같은 그림이다 — EC/PC-10 바늘은 위아래로 보라(Bi)와 노랑(C)·빨강(F)이 촘촘히 번갈아 나오고, TEGDME-10 바늘은 아래쪽 넓은 보라 덩어리 위에 SEI 원소가 얹혀 있다. TEGDME-100 바늘은 C 가 바늘 전체로 퍼진다.
- XPS 깊이 (`Fig. S22`) · ToF-SIMS (`Fig. S23`): TEGDME 는 얕은 스퍼터에서 Bi 가 드러나고 SEI 신호가 빨리 사라진다 → **EC/PC SEI 가 훨씬 두껍다** (nm 환산은 없다).

### 6.4 §5 계면 반응성 (`Fig. 5`, `Fig. S24`–`S27`)

- 저자의 세 결론 (p.10): ① 균열·SEI 성장은 어느 문턱을 넘지 않으면 가역성을 해치지 않는다 ② SEI·전해질 성질이 미분화 정도를 바꾼다 ③ SEI 조성·구조·성장속도는 전해질 분해 반응(반응성)이 정한다.
- 고전 MD: 두 전해질 모두 SSIP 가 다수 (`Fig. 5a,b`). EC/PC 는 EC·PC·음이온이 모두 Na⁺ 에 배위, TEGDME 는 Na⁺ 가 주로 용매(한 분자가 감쌈)에 배위 (`Fig. S25`).
- 분자 DFT: EC/PC 쪽 종이 더 쉽게 환원된다 (`Fig. 5c` — 값 없음).
- AIMD (`Fig. 5d,e` + `Fig. S26`): 🔎 **표지 대조** — `Fig. S26` 캡션은 (b) EC/PC on **Na₃Bi** · (c) EC/PC on **NaBi** · (e) TEGDME on **Na₃Bi** · (f) TEGDME on **NaBi** 이고, 그림의 b·e 는 **넓은 셀 · Bi 3 원자 묶음 + Na 가 많은 층**(Na:Bi ≈3), c·f 는 **좁은 셀 · Bi 4 원자 줄과 Na 줄이 번갈아**(≈1:1) 다. 그런데 `Fig. 5d,e` 에서 **"NaBi(100)" 열이 넓고 Na 가 많은 셀, "Na₃Bi(100)" 열이 좁고 1:1 줄무늬 셀**이다 (원본 래스터 확대 · 나란히 대조 · figure-read). 원자 수는 보존되므로 5 ps 동안 슬랩이 바뀔 수 없다 → **`Fig. 5d,e` 의 두 열 표지가 뒤바뀐 것으로 보인다**. 본문 서술(*"very severe at the Na₃Bi surface"* · TEGDME *"Na dealloying … particularly in the case of Na₃Bi"*)은 `Fig. S26` 의 정체와 맞는다 → 오류는 그림 표지 쪽으로 읽힌다. 또 넓은(Na₃Bi 로 보이는) 슬랩은 **두 전해질 모두에서** 원자 배열이 크게 흐트러지고 Na 가 전해질 쪽으로 퍼진다 — 전해질과 무관한 슬랩 자체의 불안정일 수 있다.
- 누설전류 (`Fig. S27`): 본문 *"the overall steady-state leakage currents in the TEGDME electrolyte at all tested potentials are significantly lower"* · *"it is reasonable to assume that the Faradaic current, arising from alloying and dealloying of the Bi electrodes, was fully eliminated"* → 정상상태 전류를 *"a quantitative descriptor of parasitic reactions"* 로 쓴다 (판정은 §10-2).

### 6.5 §6 위상장 — 두꺼운 SEI 가 결정립을 잘게 만든다 (`Fig. 6`, `Fig. S28`–`S32`, Table S3–S7)

- 결과 (p.12): 두꺼운 SEI(EC/PC) 입자에서 NaₓBi·Bi 결정립이 더 작고 고르다 → 얇고 두께가 들쭉날쭉한 SEI(TEGDME) 는 Na 유속이 불균일해 핵이 적고 크기 분포가 넓다 · 두껍고 고른 SEI 는 유속이 고르게 퍼져 핵이 많다.
- 입계 밀도 (`Fig. 6c`): EC/PC 가 나트륨화 ≈1.6 · 탈나트륨화 ≈2.7 배 (figure-read).
- 응력 (`Fig. 6d–f`): 나트륨화 때 Na₃Bi 결정립은 큰 음의 '압력'(압축), SEI 는 양(인장) → *"while particle cracking is unlikely during sodiation, the SEI may be susceptible to cracking"* · 탈나트륨화 때 Bi 결정립은 큰 양의 '압력'(인장) · σx 는 입계에 수직. *"Interestingly, the magnitude of tensile stress is comparable between particles cycled with a thick SEI … and a thin SEI"* → 균열 위험의 차이는 **응력이 아니라 입계 밀도** 에서 온다는 논리.
- 🔎 스냅샷 실독 (`Fig. S29`–`S32`): 나트륨화는 두 경우 모두 **입자 가장자리의 얇은 고리만** 변태한 시점까지다 (내부는 Bi). 탈나트륨화는 **Na₃Bi 단일 원판에서 새로 시작**한다 (`Fig. S31a`·`S32a` — 나트륨화 결과를 잇지 않음). '압력' 의 부호 규약은 일반(+ = 압축)과 반대다 — 본문이 음의 압력을 압축으로 읽는다 (사실상 평균수직응력 σ_h 를 그린 것).
- 저자 단서: *"intended to illustrate the relative effects … rather than to provide a fully parameterized predictive model"*.

### 6.6 §7 Sn 검증 (`Fig. S33`–`S35`)

- EC/PC 에서 Sn 은 ∼175 mAh g⁻¹ 만 내고(분극 큼), TEGDME 는 ∼667 (Na₁₅Sn₄ 이론의 79 %). 더 큰 부피 변화를 겪는 TEGDME 쪽이 더 안정 → *"electrolyte interfacial reactivity, rather than volume change or particle cracking, plays a dominant role"*.
- cryo-TEM·EDS: EC/PC 는 잘게 쪼개진 Sn 이 두꺼운 SEI 에 싸이고, TEGDME 는 µm 입자 + 얇은 SEI → Bi 와 같은 그림.

### 6.7 §8 Discussion

- SEI 는 *"a product of electrolyte decomposition reactions deposited on the anode surface, rather than the intrinsic driver of interfacial stability"*.
- *"electrolytes with low interfacial reactivity are essential … However, electrolytes that produce a resilient SEI alone, without inherently suppressing interfacial reactivity, are insufficient"* · 희생 첨가제는 고갈되면 효과가 사라진다 (저로딩·과량 전해질에서 과대평가) · 많은 고급 전해질은 용매 분해 억제 + 강한 SEI 두 경로로 '실효' 반응성을 낮춘다.

### 6.8 논증 사슬 판정

| # | 고리 | 근거 | 판정 |
|---|---|---|---|
| ① | 두 전해질에서 성능이 극단적으로 다르다 | 필름·분말·완전셀 | ✅ |
| ② | 첫 나트륨화 팽창·용량은 같다 → 부피 변화가 원인이 아니다 | `Fig. 1a` · `Fig. S11` | △ 첫 사이클만 · 이후 "TEGDME 누적 팽창이 더 크다" 는 EC/PC 가 이미 죽어서 생긴 차라 순환에 가깝다 |
| ③ | 같은 염·농도이고 SEI 가 *"not substantially different"* → SEI 화학을 배제 | XPS 주성분 | ✗ **배제 못 했다** — 자기 데이터가 SEI 두께(XPS 깊이·ToF-SIMS·cryo-EDS)·조성비(F 1s ≈9 vs ≈1)·분포(APT)의 차이를 보인다. TEGDME SEI 는 '얇고 NaF 비중이 높은' — 저자가 넘어서려는 기존 'SEI 품질' 설명과 같은 그림이다 |
| ④ | EC/PC 가 더 반응적이다 | 분자 DFT · AIMD · 누설전류 | △ 방향은 셋이 같다 · 정량은 누설전류뿐 (DFT 값 0 · AIMD 정량 0 · 관측창 0.1 eV) · 누설전류는 면적·잔류 합금 전류와 교락 |
| ⑤ | 반응성 → 두꺼운 SEI | ③④ | △ 상관 (n = 2 전해질) |
| ⑥ | 두꺼운 SEI → 핵 많음 → 입계 많음 | 위상장 | △ 모형 안에서는 성립 — 단 SEI 두께는 **입력**이고, 결정립 차는 1.5–2 배 · R 에 견고하지 않음 · 실현 1 개 |
| ⑦ | 입계 많음 → 미분화 → 새 표면 → SEI 성장 (되먹임) | 위상장 (파괴 없음) + 실험 형태 | ✗ 모형에 파괴가 없어 '미분화' 는 추론 · 되먹임 고리는 계산되지 않았다 |
| ⑧ | Sn 도 같다 → 일반 원리 | `Fig. S33`–`S35` | △ 방향 일치 · 25 사이클 · EC/PC Sn 은 나트륨화 깊이가 달라 같은 조건 비교가 아니다 |

⇒ **허용 서술 범위**: *"1 M NaPF₆ 에서 EC/PC 와 TEGDME 를 비교하면, 계면 반응성이 높은 쪽(EC/PC)에서 Bi 의 미분화·SEI 두께·전극 치밀화·용량 손실이 모두 컸다. 위상장 모형은 두꺼운 SEI 가 핵생성 밀도를 높여 결정립을 잘게 만들 수 있음을 정성적으로 보인다."* "반응성이 미분화를 **지배**한다" 는 인과는 이 데이터로 갈리지 않는다.

---

## 7. 우리 DFT/MLIP 대비 (`../our_dft_baseline.md` · EXTERNAL — 수치 대조 없음)

| 항목 | 이 논문 | 우리 | 같은가 / 다른가 · 이유 |
|---|---|---|---|
| 계 | Na · 액체(EC/PC, TEGDME) · Bi/Sn 합금 음극 | Li · 황화물 고체(LPSCl 계) · 벌크 SE | **다른 계** — 숫자를 같은 축에 놓지 않는다 |
| SEI 판독의 양 | 반응 **속도** (정상상태 누설전류) + 형태 (두께·분포) | 0 K grand-potential 산물·갭 (`db/properties/anode_interface_b2o3.json` · `sei_products.json`) | **다른 양** — 우리 쪽은 "무엇이 생기나", 이 논문은 "얼마나 빨리" (§H 첫 행 '시간축 공백' 의 액체판) |
| 반응 MD | AIMD 5 ps · 298 K · 중성 셀 · 1 궤적 · 정량 없음 | T3 계획 (UMA 반응 MD · Li‖LPSCl · 350 K · ≥20 ns · **미실행**) · 외부 `[KimSEI]` MTP 반응 MD 350 K 20–50 ns | 관측창 ≈0.10 eV vs ≈0.37–0.40 eV (§5.5) — **둘 다 셀 시간척(≈1 eV)에 못 미친다** |
| 고전 MD | OPLS-AA (전하 ×0.75) · NPT 100 ns · 용매화 분포 | 해당 없음 (우리 MD 는 고체 Li 확산 · UMA MLIP) | 비교 대상 없음 — 보고 규율(분류 기준 미기재 · g(r) 와 분율 불일치)만 가져온다 |
| 분자 DFT | B3LYP/COSMO 환원전위 (값 미공개) | 해당 없음 (우리는 주기 QE-PBE) | 비교 대상 없음 |
| 기계 (C) | 위상장 입력 C₁₁ = 300 GPa 등 (추정 입력값) | 우리 E_VRH (DFT 0 K) | ⛔ **비교 금지** — 모형 입력이지 물성이 아니다 |
| 전자 (D) | 없음 | PBE 갭 | 해당 없음 |
| DEM / 연속체 | 위상장 (SEI 고정층 · 파괴 없음 · 미소변형) | DEM/MPM 압밀·파괴 (Auerbach 접촉 판정) — `our_dem_baseline.md` 는 자리표시자(값 0) | 수치 대조 불가 · "입계 밀도 = 균열 개시 자리 수" 는 정성 가설로만 |

- ⚠ **트랙**: SEI·음극 계면 서술은 우리 DFT 기준선 트랙(사용자 1저자)이다. 이 편은 그 트랙에 **수치를 하나도** 넘기지 않는다.

---

## 8. 적용 인사이트 ★

1. **짧은 MD 의 '무반응·안정' 서술에 관측창 한 줄을 붙인다** (제안 · 결정 아님). Ea_max = kT·ln(ν₀·t) — 5 ps/298 K ≈0.10 eV, 우리 T3 20 ns/350 K ≈0.37 eV. 장벽 인용에 홉 수 검산을 붙이는 `D-2026-09-27` 의 거울상이다 (장벽이 없을 때 "이 창은 어디까지 보나"). T3 를 돌리면 "20 ns 동안 X 가 안 생겼다" 는 문장마다 이 줄이 필요하다.
2. **"조성 vs 속도" 프레임** — 우리 음극 서사는 조성(산물·갭)만 말한다. 이 논문은 같은 염·다른 용매로 '속도' 가 수명을 갈랐다고 주장한다. 고체 쪽 대응물은 **SE 환원 반응의 속도**(합금 음극 표면에서의 LPSCl 분해율)다. 실험 협업에 '정전위 유지 누설전류' 를 요청할 수 있는 지표로 기록해 둔다 — 단 §10-2 교락 목록(면적 정규화 · 합금 평탄 전위 회피 · 여러 셀)을 같이 보낸다.
3. **그림·표 정합 검산 체크리스트의 반례 묶음** (원고·리뷰 점검용): ① 세로축 눈금 없는 계산 그림 (`Fig. 5c`) ② 초기 구조와 결과 스냅샷의 표지 대조 (`Fig. 5d,e` ↔ `Fig. S26`) ③ 분할 영역 평균의 '전체' 가 두 값 사이에 있나 (`Table S1`) ④ g(r) 적분 ↔ 보고된 배위 분율 (`Fig. S25` ↔ `Fig. 5a`) ⑤ 응력 색막대 ↔ 입력 탄성·고유변형 상한 (`Fig. 6d–f` ↔ `Table S3`) ⑥ "full cycle" 이 정말 이어진 계산인가 (`Fig. S29`–`S32`). 우리 원고에도 그대로 쓸 수 있다.
4. **DEM/연속체 쪽** (부모 세션 판단): "SEI 두께 → 핵 밀도 → 입계 밀도 → 균열 자리" 는 고변형 음극(Si·합금)이 황화물 SE 와 만나는 고체 셀에서도 물을 만한 가설이다. 이 편은 파괴 매개변수·응력 크기를 주지 않으므로 **보정값으로는 못 쓴다**. 고체 쪽 대응 실험의 입구는 이 논문이 인용한 **ref 47 Tan et al. *Science* 373, 1494 (2021)** "Carbon-Free High-Loading Silicon Anodes Enabled by Sulfide Solid Electrolytes" (제목만 확인 · litdb 없음 → 인입 후보).
5. **보고 규율 대조** — 우리 MLIP-MD 카드는 앙상블·온도·시간·시드·창을 결과 전에 선언한다. 이 편의 AIMD·위상장은 궤적 1 개·실현 1 개·시각 미표기다. 우리 쪽이 지키는 것을 외부 반례로 확인하는 용도.

---

## 9. Post-processing

- **실험**: dQ/dV 봉우리 → 평탄별 용량 기여 (파이) · EIS 등가회로 맞춤 (R_s · CPE‖R_SEI · CPE‖R_ct + Z_W) · 누설전류 지수감쇠 맞춤 (y₀) · XPS CasaXPS Shirley 피팅 · APT IVAS 3.8 등농도면 (Bi 30 · F 10 · C 20 · P 1 at%) + 영역 평균조성 · ToF-SIMS SurfaceLab (¹⁸O⁻ 정규화) · XRM CT 재구성·분할 (도구 미기재).
- **계산**: 고전 MD → 용매화 분류 (SSIP/CIP/AGG, 기준 미기재) + g(r) · 분자 DFT → Gibbs 차 → E_red · AIMD → **스냅샷만** (VMD) · 위상장 → 결정립 지름 통계 (상자그림 · Dmax/Dmin/Dave) · 입계 수 밀도 · 응력장 색지도.
- **기록**: 원자료·구조 파일·입력 파일 비공개 ("요청 시"). 위상장 함수형은 "후속 논문".

---

## 10. 비판 — 이 논문의 약한 곳 ★

1. 🔴 **전해질 2 종 → 교락.** 반응성·용매화(SSIP 84 vs 92.5 %)·유전율(77.5 vs 7.8)·SEI 두께·SEI 조성비가 한꺼번에 바뀐다. 저자 스스로 TEGDME SEI 가 얇고 NaF 비중이 높다고 쓴다 — 이는 그들이 넘어서려는 "얇고 NaF-rich 한 SEI 가 좋다" 는 기존 설명과 **같은 그림**이다 → 데이터는 두 설명을 가르지 못한다. 가를 실험(같은 용매에서 첨가제로 반응성만 바꾸기 · 반응성 3 단계 이상의 전해질 · SEI 를 미리 만들어 옮기기)이 없다. 위상장도 '반응성' 이 아니라 'SEI 두께' 를 원인 변수로 넣는다.
2. 🔴 **누설전류 = 본질 반응성?** (a) 형성 3 회 **뒤**에 잰다 → 이미 미분화된 표면적이 곱해진 값이다 (µA · 면적·질량 정규화 없음) — 저자 기전(반응성 → 미분화 → 면적↑)이 측정값 안에 이미 들어 있다 (b) 차이가 **합금 평탄 전위(0.5·0.7 V)** 에 몰린다. 저자 스스로 EC/PC 의 '죽은' NaₓBi 는 *"can only be accessed by overcoming high resistance and large overpotentials"* 라고 쓴다 — 그 느린 합금 전류가 30 h 지수 맞춤의 y₀ 에 남을 수 있다 (`Fig. S27b` EC/PC 과도전류가 ≈15 h 에 걸쳐 감쇠) (c) Na₃Bi 영역 0.01 V 에서는 거의 같다 (≈−0.83 vs ≈−0.73 µA) — 본문 *"at all tested potentials"* 와 어긋나고, AIMD 의 *"very severe at Na₃Bi"* 와도 어긋난다 (d) 셀 1 개 · 오차막대 없음 · TEGDME 0.8 V 가 +0.17 µA.
3. 🔴 **AIMD** — 5 ps · 궤적 1 개 · 중성 셀 · 분해 정량 0 · k 점·셀·원자 수·vdW 미기재 · **열 표지 뒤바뀜 의심** (§6.4) · 관측창 ≲0.1 eV (§5.5) → '무반응' 은 안정의 근거가 아니다 · Na₃Bi 로 보이는 슬랩이 두 전해질 모두에서 흐트러진다.
4. 🔴 **분자 DFT 의 숫자가 0 개** — `Fig. 5c` 는 눈금 없는 축에 축 끊김 2 개. 그리고 두 전해질의 COSMO ε 가 10 배(77.48 vs 7.78) 달라, 서열 차의 일부가 분자 정체가 아니라 연속체 유전율에서 온다 (분리 안 됨).
5. 🔴 **위상장** (a) SEI 는 **고정된 입력층** (L* = 0 → 자라지 않는다) — 전해질 반응성은 모형에 없다 (b) **파괴 모형이 없다** — '미분화' 는 입계 밀도에서 추론 (c) 나트륨화·탈나트륨화를 **서로 다른 단일상 원판**에서 따로 돌렸다 (`Fig. S31a`·`S32a`) — 본문 *"after a full sodiation-desodiation cycle"* 과 어긋난다 (d) 둘 다 **가장자리 고리만** 변태한 초기 단계 (e) **실현 1 개** · 시드 반복 없음 · R = 50·70 l₀ 에서 얇은/두꺼운 차 ≤2 % (`Table S6`·`S7`) (f) **응력 크기가 비물리적** — 완전구속 상한 \|σ_h\| ≤ 3K·e* = 3 × 166.7 GPa × 0.08 ≈ **40 GPa** (우리 산수: K = (C₁₁ + 2C₁₂)/3 · e* = e₀ + e_c·c = 0.05 + 0.01×3) 인데 색막대는 **100–200 GPa** · 반대로 나트륨화 색막대의 양의 끝은 **+7.9×10³ Pa** — 본문의 *"SEI may be susceptible to cracking due to the buildup of tensile stress"* 를 그림 숫자가 받치지 못한다 (g) Bi 와 Na₃Bi 의 탄성상수가 **같은 둥근 값** (300/100/100 GPa) · 등방 고유변형 e* ≤ 0.08 = 부피 ≈24 % (우리 산수) vs 본문 *"∼360 %"* — 미소변형 선형탄성으로는 이 변형을 못 담는다 (h) f_intf·f_bulk·검증이 *"forthcoming"* → **재현 불가** (i) R²/D ≈ 2.9 s — 모사 시간척이 C/3 실험과 연결 안 됨 · 가정 ③ '확산 지배' 와 긴장 (j) 가정 ③ *"fast ion transport in the electrolyte"* ↔ 식 (12) 는 **전해질 안에서 M_Na⁺ = 0** (k) 결정립 대비 모형 1.5–2 배 vs 실험 ~10² 배 (l) `Fig. 6b` ↔ `Table S5` 불일치 2 곳 · `Fig. 6c` 정의 없음 · 캡션 σx ↔ 색막대 σ₁ · 'pressure' 부호 규약 반대 · (참고, 논문 밖 상식 · 미검증) Bi 는 무른 반금속이라 C₁₁ = 300 GPa 는 상식선보다 크다 — 저자가 인용한 ref 26 (Kammer 1972) 실측값과 대조가 필요하다.
6. 🔴 **APT** — `Table S1` EC/PC 행이 분할 산술과 네 원소 모두 모순 · TEGDME 100회 F 모순 · EC/PC 'SEI-rich' Bi 33.7 > 30 at% 문턱 (§3f) · **Na·O·H 미보고** · 조건당 바늘 1 개 (높이 figure-read ≈130–180 nm) → µm 이질성의 표본이 못 된다. (일반 주의, 논문 언급 없음) 금속 Bi 와 유기 SEI 처럼 증발장이 크게 다른 혼합 바늘은 경계에서 국소 배율 효과로 조성이 섞여 보인다 — 10–20 nm 입자가 촘촘한 EC/PC 에서 'continuum-like' 를 키울 수 있다.
7. ⚠ **XPS** — 세로축 눈금 없음 · *"slightly"* 는 그림(≈9 vs ≈1)보다 작게 말한다 · NaₓPF_y 봉우리와 세척 뒤 남은 NaPF₆ 를 가를 수 없다 (XPS 시료 세척 조건 미기재) · TEGDME 10 → 100회의 NaₓPF_y/NaF 증가를 *"higher proportion of polyether-based organic components derived from electrolyte solvent decomposition, compared to inorganic NaF originating from salt decomposition"* 의 근거로 쓰는데 NaₓPF_y 자체가 **염 유래**다 — 논리 미끄러짐.
8. ⚠ **고전 MD** — `Fig. S25b` g(r) 적분 CN ≈0.6–0.8 ↔ `Fig. 5a` CIP+AGG 15.8 % (TEGDME 는 정합 · §3h) · 분류 기준 미기재 · 힘장 검증 미보고 · SI 'LiPF₆' 오기 두 번.
9. ⚠ **두께** — 같은 상태가 기법·시료마다 1.5–1.8 배 다르다 (EC/PC 67 vs 50 · TEGDME 25 vs 44 µm) · `Fig. S10b` 윗층(≈100 µm) 설명 없음 · 통계 없음.
10. ⚠ **in-situ XRD** — EC/PC 만 (TEGDME 대조 없음) · Methods 2θ 15–30° ↔ 그림 ≈16–47° · 이 셀의 용량 곡선 미제시 (코인셀과 다른 형식 · 0.05 V 하한) · 기준선에 없는 봉우리 figure-read ≈41.5° · ≈43.4° 무해설 (≈43.3° 는 Cu 메시의 Cu(111) 로 보인다 — 우리 추정).
11. ⚠ **숫자 서술 ↔ 그림** — ">150 cycles" ↔ 그림 끝 ≈148 · 필름 "<20 % within 10" ↔ figure-read ≈21–23 % · 완전셀 *"<30 % … within ∼20 cycles"* ↔ ≈49 % @20 · *">91 % … over 120 cycles"* ↔ 축 100 사이클 · 분말 유지율을 *"as shown in Figure 1b"* 로 인용 (실제 `Fig. S3b`) · 로딩 2–3 / >3.0 / ~3 / ~3.6 mAh cm⁻² · TEGDME 기여 "66.4 %" 가 파이에 없음.
12. ⚠ **Sn** — EC/PC 에서는 가역 용량이 이론의 ≈21 % (첫 방전도 ≈32 %) → 상·부피 변화가 달라 미분화 비교가 같은 조건이 아니다 · 25 사이클 · 'nanorod' 가 `Fig. S34a` 에서 뚜렷하지 않다 (figure-read).
13. ⚠ **셀 조건** — 전해질 ~80 µL (과량) · 완전셀 N/P·PBA 로딩 미기재 · 반쪽셀 Na 대극 (Na‖Na·완전셀로 일부 보완).
14. ⚠ **②번 고리의 순환** — "TEGDME 가 이후 더 큰 용량 = 더 큰 누적 팽창인데도 안정" 은 EC/PC 가 이미 죽어서 생긴 차다. 깨끗한 근거는 첫 나트륨화(≈30 µm · 같은 용량) 하나뿐.
15. 경미 — SI 캡션 오기 (XRD↔XRM · "power") · `Table S5` 제목 · *"maximium, minium, average, and mean"* · R_SEI 180.0 ↔ 180.8 Ω · `Fig. S27a` 0.01 V 점의 원자료 없음 · 동영상 캡션 없음 · TEGDME-10 동영상 프레임에 축척 막대 없음 · MP id ↔ 상 대응 미명시.

**잘한 점** — 같은 염·같은 농도로 용매만 바꾼 깔끔한 대비 · 필름·분말·완전셀 세 형태 재현 · cryo-TEM·APT·XRM·XPS 깊이·ToF-SIMS 로 nm–µm 다중 척도 · Na‖Na EIS 와 PBA 완전셀로 Na 대극 효과 점검 · 누설전류라는 실측 속도 지표 · Sn 교차 확인 · AIMD 가 짧고 위상장이 정성용이라는 단서를 본문에 명시 · OA.

---

## 11. 인용 가능 문장 (영문 초안 — 방어 가능한 것만)

- "In 1 M NaPF₆, high-loading bulk Bi anodes retained ∼99% of their capacity over 250 cycles in TEGDME but faded to ∼20% within 10 cycles in EC/PC (Kim et al., *Adv. Energy Mater.* 2026, e71596)."
- "After 10 cycles in EC/PC, cryo-TEM showed ∼10–20 nm polycrystalline Bi embedded in a thick interphase, whereas Bi cycled in TEGDME remained as crystalline micrometre-scale particles covered by a thin interphase."
- (방법 주의로) "A 5 ps AIMD trajectory at 298 K only probes reactions with barriers of ≲0.1 eV (ν₀ = 10¹³ s⁻¹ assumed); the absence of decomposition on that timescale does not establish interfacial stability over hours of cycling."

---

## 12. 주의 / 한계 (인용 규율)

**⛔ 인용 금지**
- Na 계 수치(용량·저항·두께·조성·누설전류)를 우리 Li/LPSCl 축에 · 우리 db 값과 같은 줄에.
- `Fig. 5c` 의 '환원전위' — 숫자가 없다. "EC/PC 가 X V 더 쉽게 환원된다" 류 문장 전부.
- AIMD 스냅샷을 "TEGDME 는 NaₓBi 위에서 분해하지 않는다" 로 (관측창 ≲0.1 eV) · `Fig. 5d,e` 의 열 표지를 그대로 (`Fig. S26` 과 대조).
- 위상장 응력값 (10¹¹ Pa) · 결정립 절대 크기 · "SEI 가 인장으로 깨진다" · `Table S3` 탄성상수를 Bi/Na₃Bi 물성으로.
- `Table S1` EC/PC 행 숫자를 '연속체 같은 미세구조' 의 정량 근거로.
- `Fig. 5a` 의 EC/PC 용매화 분율 (`Fig. S25` 와 불일치).
- "전해질 반응성이 미분화를 **지배**한다" 를 입증된 인과로 — 허용 서술은 §6.8 끝.
- 누설전류를 면적·잔류 합금 전류와 분리된 '본질 반응성' 으로.

**⚠ 조건부**
- 성능·형태 수치 — **Na 액체 계 소환값**으로, 계 이름(1 M NaPF₆ · EC/PC vs TEGDME · Bi)을 붙여서만.
- "글라임 전해질이 Bi·Sn 에 좋다" — 선행 refs 37·40·73 과 함께.
- 위상장 결과 — "두꺼운 SEI 가 핵 밀도를 높일 수 있다" 는 **정성 가설**로만.

---

## 13. 기법 미니사전

- **합금 음극 미분화 (pulverization)**: 충방전 때 큰 부피 변화(Bi → Na₃Bi)로 입자가 갈라지고 잘게 부서지는 것. 새 표면이 드러나 SEI 가 다시 자란다.
- **2상 반응 vs 고용체 유사**: 큰 입자는 두 상의 경계가 움직이며 전위가 평탄하고 끝이 수직으로 떨어진다. 나노 입자는 평탄이 짧고 끝이 비스듬하다 — 곡선 모양으로 입자 크기를 읽는 근거.
- **dQ/dV**: 용량을 전위로 미분한 곡선. 상전이가 일어나는 전위에서 봉우리가 선다.
- **R_SEI / R_ct**: 임피던스 반원 둘 — 고주파 쪽이 SEI 를 지나는 저항, 중주파 쪽이 전하이동 저항.
- **3D-XRM (X선 현미경 CT)**: 시료를 360° 돌리며 투과 영상을 모아 3D 로 재구성. 흡수 대비로 Bi 와 SEI·기공을 가른다 (µm 해상).
- **cryo-(S)TEM / SAED**: 저온(~100 K)·저선량으로 빔 손상을 줄인 전자현미경. SAED 의 **고리**는 무작위 방위의 다결정(나노 입자), **점**은 단결정.
- **APT (원자 탐침 단층촬영)**: 뾰족한 바늘 시료 끝에서 원자를 한 층씩 전계 증발시켜 비행시간 질량분석으로 3D 원자 지도를 만든다. **등농도면**은 "Bi 30 at%" 처럼 농도 문턱으로 그린 경계면.
- **ToF-SIMS 깊이 분석**: 이온빔으로 깎으면서 튀어나온 이차이온 조각을 질량분석. 깎는 시간 축이지 nm 축이 아니다 (식각률 보정이 있어야 깊이).
- **누설전류 (정전위 유지)**: 전극을 한 전위에 오래 묶어 두면 합금 전류는 사라지고 전해질 분해 같은 기생전류만 남는다는 가정으로 재는 정상상태 전류. 면적·잔류 반응이 섞이기 쉽다.
- **SSIP / CIP / AGG**: 용매 분리 이온쌍 (Na⁺ 와 음이온 사이에 용매) / 접촉 이온쌍 (직접 맞닿음) / 응집체 (음이온이 Na⁺ 여럿에 걸침).
- **RDF g(r) · 배위수**: 한 원자 주위 r 거리에 다른 원자가 있을 상대 확률. CN = 4πρ∫g r² dr 로 첫 껍질 안의 이웃 수를 낸다.
- **OPLS-AA · 전하 축소**: 유기 액체용 고전 힘장. 편극을 흉내 내려고 이온 전하를 0.75 배로 줄이는 관행.
- **COSMO**: 분자 주위를 유전율 ε 연속체로 감싸 용매 효과를 근사하는 암시적 용매 모형.
- **환원전위 계산**: E_red = −ΔG_red/F 를 절대전위로 낸 뒤 절대 Na/Na⁺ 전위(1.73 V)를 빼 vs Na/Na⁺ 로 바꾼다.
- **AIMD 중성 셀**: 전자를 더하거나 빼지 않은 셀 — 전극 전위를 제어하지 않는다. 금속 슬랩의 페르미 준위가 '환원력' 을 정한다.
- **관측창 (Ea_max = kT·ln(ν₀t))**: 시간 t 동안 한 번이라도 일어날 수 있는 반응의 장벽 상한. 홉 수 검산과 같은 식을 반대로 쓴 것.
- **위상장 (phase-field)**: 상·결정립을 연속 변수(order parameter η)로 나타내 경계를 자동으로 그리는 방법. **Allen–Cahn** = 보존 안 되는 η 의 이완식, **Cahn–Hilliard** = 보존되는 농도의 확산식.
- **고유변형 (eigenstrain) e***: 상변태·조성 변화로 생기는 '응력 없는' 변형. 실제 변형과의 차가 탄성변형 → 응력.
- **고전 핵생성 이론 삽입**: 후보 자리마다 핵생성 확률을 계산해 확률적으로 핵을 심는 방식 — 같은 입력이라도 실현마다 결과가 다르다 (시드 반복이 필요한 이유).
- **PBA (Prussian blue analogue)**: Na 이온 전지 양극. 여기서는 Na 대극을 빼고 완전셀을 만들려고 썼다.

---

## 14. 그림 크롭 · 동영상 기록 (`litdb/figures/kim2026_electrolyte_interfacial_reactivity_alloying_anode_pulverization/figures.json`)

- **manual_crop 2**: `Fig. S3` (SI p.3 — S2 캡션과 S3 캡션 사이의 벡터 2 패널 · 클립 [103.8, 463.6, 506.5, 624.2] pt) · `Fig. S27` (SI p.24 — 캡션 위 벡터 3 패널 · 그리기 경로 16,467 개 · 클립 [121.4, 69.8, 488.9, 380.5] pt). 둘 다 도구가 *"그래픽 없음(img0/draw0)"* 으로 번호 공백 처리했다. 300 dpi · 도구의 `blank_ratio`·`_shrink` 를 그대로 썼다. `missing_labels` 두 항목에 `resolved` 를 달았다.
- **viewed**: 실제로 본 34 장 (그림 32 + 표 2) 에 `"viewed": true`.
- 다른 크롭은 손대지 않았다 (`--clean` 재실행 없음).
- **동영상**: `litdb/inbox/Kim 2026 - Sup2|Sup3|Sup4 Movie (Adv Energy Mater aenm.71596).mp4` = Movie S1 (EC/PC-10) · S2 (TEGDME-10) · S3 (TEGDME-100). 레포에는 프레임을 넣지 않았다. 직접 재생 판독은 하지 않았다 — 정지 프레임 8 장씩(1100×619 축소본)만 봤다.
