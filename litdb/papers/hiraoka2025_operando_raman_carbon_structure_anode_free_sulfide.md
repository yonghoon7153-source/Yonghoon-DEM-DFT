<!-- digest 표준 양식 (paper-level STANDALONE) · 깊이 본 = zuo2022_chlorination_cathode_interface.md · 같은 계열 꼴 = metzler2026_sputtered_ag_carbon_interlayers_anode_free.md · metzler2025_ag_particle_distribution_carbon_interlayer_anode_free.md
     작성 2026-11-24 — 병렬 세션 (배치 2026-11-24b #6 · 이 파일 · litdb/figures/<slug>/ · 끝 보고만 쓴다 · INDEX · comparison 은 메인 세션이 합친다 · git 안 씀).
     원문 = 본문 11 쪽 (PDF 1 쪽 = 이 호 (13 권 34 호) 표지 · PDF 2–11 쪽 = 인쇄 27960–27969) + SI 14 쪽 (그림 S1–S8 · 표 S1–S3) — 글자 층 전부 읽음 + 그림 16 장 전부 Read 로 렌더해 실독 (Fig. 1 은 손 크롭).
     쪽 표기 = "p.27961" 처럼 인쇄 쪽 · "SI S-N" = SI 인쇄 쪽 (= SI PDF N 쪽).  figures.json 의 page 는 PDF 쪽 (본문 PDF 쪽 = 인쇄 쪽 − 27958).
     단위 주의: 글자 층의 "10 mm · 18 mm · 100 mm · 70, 100 and 10 mm · ∼1 mm · ±5 mm · B 34 mm" 는 기호 폰트의 µ · ϕ 가 빠진 것이다 (폰트로 확인 · Fig. 1b 의 "10 µm · 100 µm · 70 µm" 와 일치). ex situ 의 "every 2 mm" 만 진짜 mm 다 (본문 폰트).
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 글자 · figure-read ≈ = 그림에서 읽은 값 (축 · 픽셀 · 디지털 판독) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산 (식 병기) ·
     [가정] = 원문에 없는 상수 · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = litdb 다른 카드의 값 (slug 병기) · [일반 지식] = 이 논문 밖 교과서 수준 지식 (출처 미확인 — 인용 전 원전 확인) · [미확인] = 본문 + SI 전수에 없음.
     우리 점착 (W) 값은 이 카드에 싣지 않는다 — 위치만.  이 논문에 DFT · MD · 연속체 모델은 없다 (실험 전용). -->

# Ag/카본블랙 층 (10 µm) 의 단면을 operando Raman 으로 보니 충전 중 카본블랙의 D · G 띠가 바뀌었다가 방전 뒤 대부분 돌아왔다 (G 1583 → ≈1540–1560 → 1575 cm⁻¹) — 저자는 '비정질 탄소에도 Li 가 들어간다' 로 읽는다 · Li 금속은 Ag/C 와 SUS 집전체 사이에 쌓인다 · 5 h 휴지 뒤 (ex situ) 변화는 작다 — Hiraoka · Sakabe · Suzuki · Seki (*J. Mater. Chem. A* 13, 27960 (2025))

> slug `hiraoka2025_operando_raman_carbon_structure_anode_free_sulfide` · DOI `10.1039/D5TA02406D` · type `exp (무음극 Li₆PS₅Cl 적층 파우치 셀 · LZO 코팅 NCM90 양극 · Ag/카본블랙 층 on SUS · 단면 operando 현미 Raman (532 nm) + ex situ Raman + 광학 단면 — 원자단위 계산 · 모델 0)` · PDF `litdb/inbox/hiraoka2025_operando_raman_carbon_anode_free_main.pdf` (본문 11 pp · 1 쪽은 표지) + SI `litdb/inbox/hiraoka2025_operando_raman_carbon_anode_free_SI.pdf` (14 pp · 그림 S1–S8 · 표 S1–S3) · digested `2026-11-24` · status ✅
> elements: Li, C, Ag, P, S, Cl
> methods: Raman

> **저자 (원문 순서)**: **Koji Hiraoka** (1저자 · a) · Junichi Sakabe (b) · **Naoki Suzuki\*** (교신 · b) · **Shiro Seki\*** (교신 · a) — a = Graduate School of Applied Chemistry and Chemical Engineering, School of Advanced Engineering, Kogakuin University (Hachioji, Tokyo) · b = Samsung Device Solutions R&D Japan, Samsung Japan Co. (Minoh, Osaka).
> **서지**: *J. Mater. Chem. A* **2025**, **13**, **27960–27969** (13 권 34 호 · 2025-09-14 호 · 이 PDF 1 쪽이 그 호 표지 = 표지 논문) · 받음 2025-03-25 · 승인 2025-06-11 · 온라인 2025-06-12 · 라이선스 표기 없음 (RSC 'Licence and permissions' 링크만) · 연구비 문장 없음 · 이해 상충 없음 · 자료 = ESI 에 포함.
> **기여 (p.27968)**: K.H. operando Raman · 전기화학 측정 · 초고 / N.S. + J.S. 무음극 셀 제작 · 평가 지원 / S.S. 지도.  감사: Yuna Sato (Kogakuin) — 측정 지원.
> **계보**: Lee 2020 *Nat. Energy* 5, 299 (ref 29 · Ag–C 층 원조 · 같은 셀 꼴) → Suzuki 2021 *Adv. Energy Sustain. Res.* 2, 2100066 (ref 30 · 같은 교신 · '과포화 카본블랙에서 Li 가 석출' 가설) → [`spencerjolly2023_ag_graphite_interlayer_operando_xrd`](spencerjolly2023_ag_graphite_interlayer_operando_xrd.md) (ref 31 · 흑연 Ag/C 의 operando XRD) → **본 논문** (원래의 카본블랙 Ag/C 를 operando Raman 으로).
> **이웃 카드 (링크만)**: [`metzler2026_sputtered_ag_carbon_interlayers_anode_free`](metzler2026_sputtered_ag_carbon_interlayers_anode_free.md) (상용 탄소 Raman 높이비 ≈1.3–1.4 · 결함 탄소 판정) · [`metzler2025_ag_particle_distribution_carbon_interlayer_anode_free`](metzler2025_ag_particle_distribution_carbon_interlayer_anode_free.md) (카본블랙 F-200GS · 도금 전 저장량) · [`kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode`](kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode.md) (같은 배합의 Ag–C 층 · §0-1) · [`baer2026_li_metal_argyrodite_interface_stability_transport`](baer2026_li_metal_argyrodite_interface_stability_transport.md) (Li \| LPSCl 반응 · §10-⑪).

> **실제로 본 그림 (2026-11-24 · Read 로 렌더)**: `Fig. 1` (손 크롭) `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` `Fig. 7` `Fig. 8` + `Fig. S1`–`Fig. S8` = **16 장 전부**.
> 확대해서 다시 본 것 (scratchpad 사본 · 저장소에 안 남김): `Fig. 2a` (첫 충전 앞부분) · `Fig. 2c` · `Fig. 3` (1087 · 1854 띠 · 3648 띠) · `Fig. 4a` · `4b` · `4d` · `Fig. S7` (2 h 격자 덧씌움) · `Fig. S8` (초기 · 100 %).
> **디지털 판독** (표지점 색 · 축 맞춤 · scratchpad): `Fig. 4` 전 패널 (점 1 충전값으로 축을 맞추면 표와 0.2–0.9 px 안에서 일치 → 점 2 를 같은 축으로 읽음) · `Fig. 7` · `Fig. S1a` (전류 적분) · `Fig. 2a` (첫 충전).
> 안 본 것: 표 크롭 `Table S1`–`Table S3` 이미지 (표는 PDF 글자로 옮겼다 — 글자가 정확하다).  크롭 = 도구 18 개 + 손 1 개 (`Fig. 1`) · 번호 공백 둘 (`Fig. 1` = 손 크롭으로 해결 · `Table S4` = SI 에 없음 · 본문 참조 오류).
> 그림에서만 읽은 값은 **`figure-read ≈`** 로 표시했다.  그림 판독이 본문 · 표와 어긋난 곳은 §10 에 모았다.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 카본블랙 (CB · D50 38 nm) 12 g + Ag (D50 60 nm) 4 g + PVDF 로 만든 10 µm Ag/C 층을 SUS 박 위에 깐 무음극 Li₆PS₅Cl 적층 셀을 **잘라서 단면을 열고** 532 nm 현미 Raman 으로 충방전 중에 보니 (실온 · 0.11 mV s⁻¹ 전위 주사 · 점 2 개), CB 의 **G 띠가 3.3–3.9 V 충전에서 1583 → ≈1559–1566 cm⁻¹ 로 내려가고 방전 초기 ≈1540 까지 갔다가 2.1 V 방전에서 1575 cm⁻¹ 로 돌아왔다** (점 1 · `Table S1`).  D 띠는 반대로 1355 → ≈1369 (충전) → ≈1382 (방전 3.3 V) → 1362 cm⁻¹.  저자는 이것을 *"Li intercalation into carbon even though it exhibited an amorphous structure"* 로 읽고 (초록), 흑연 Li-GIC 의 단계 전이와 *"similar trends"* 라고 본다 (p.27965).  그러나 Li 양 (mAh) · 화학량은 재지 않았고, 가장 큰 변화는 **단면 셀이 ≈3.85 V 에서 단락된 뒤**의 스펙트럼이며 (셋 다 단락 · `Fig. S1`), 각 SOC 에서 5 h 쉬게 한 ex situ 에서는 띠 변화가 작고 G 는 오히려 **위로** (+5–9 cm⁻¹) 갔다 (`Fig. 7` · `Table S3`).

| 우리 질문 | 이 논문의 답 | 근거 · 표지 | 직접 봤나 |
|---|---|---|---|
| ★ Q1 탄소 — 상품명 · 입경 · 비표면적 · 흑연화도 · I_D/I_G | **카본블랙 (CB)** · 상품명 [미확인] · **D50 38 nm** · BET · XRD (d₀₀₂ · L_a) · TEM · XPS [미확인] · Raman (532 nm): CB 분말 **D 1349 · G 1589 cm⁻¹** · 폭이 넓고 세기가 비슷 → 저자 *"disordered carbon with partially ordered graphene layers (low crystallinity)"* · 날카로운 2D 띠 없음 (2600–3000 cm⁻¹ 넓은 둔덕만 · figure-read) · 2 대역 pseudo-Voigt 맞춤 높이비 **R = I_D/I_G 초기 1.25 (점 1) · 1.13 (점 2)** · ex situ 초기 세 스펙트럼 **1.14–1.20 (평균 1.17)** [카드 산술 · `Table S1`–`S3`] · 원 높이비 (CB 분말 · 1000–1850 cm⁻¹ 직선 바탕) figure-read ≈**1.0** · FWHM **D ≈158 · G ≈66–67 cm⁻¹** (초기 맞춤 · [인쇄 · 표]) | [인쇄] p.27961 · p.27962–27963 · `Fig. 2c` · `Table S1`–`S3` | ✅ `Fig. 2c` (확대) · 표는 글자층 |
| ★ Q1 SE · 셀 조건 (압력 · 온도 · 전류) | **Li₆PS₅Cl** (argyrodite · RT ∼2 mS cm⁻¹ [인쇄 · 측정 자료 없음]) 슬러리 시트 (아크릴 결합제 1 wt% · 부직포 · ≈100 µm) · 양극 LZO 코팅 **NCM90** : SE : CNF : PTFE = 85 : 15 : 3 : 1.5 (≈70 µm · ≈3 cm² · Al 18 µm) · Ag/C ≈10 µm on **SUS 10 µm** · 적층 진공 파우치 → **WIP 490 MPa · 353 K · 30 min** · 설계 ≈18 mAh (C/10) / **사이클**: CCCV **5 mA (C/4 ≈1.7 mA cm⁻² [카드 산술])** · 4.2–2.5 V + 4.2 V CV 2 h · **318 K** · 구속 셀 **≈2 MPa** / **operando**: 잘라 낸 단면 셀 · 석영 창 · ≈2 MPa · Ar 상자 · **실온** · 전위 주사 **0.11 mV s⁻¹** / **ex situ**: 단면 셀 · **0.5 mA × 4 h (≈2 mAh) · 318 K** + 5 h 휴지 → 실온 Raman | [인쇄] p.27961–27962 · `Fig. 1` | ✅ `Fig. 1` (손 크롭) |
| ★ Q2 D · G 띠 (위치 · 폭 · 세기비) 변화 — operando | 점 1: **G 1582.9 → 1565.9 (3.3 V) → 1558.8 (3.6 V) → 1559.6 (3.9 V 충전) → 1540.5 (3.6 V 방전) → 1556.3 (2.7 V) → 1575.0 (2.1 V 방전)** · **D 1355.1 → 1368.8 (3.6 V 충전) → 1381.7 (3.3 V 방전) → 1362.4 (2.1 V)** · **R 1.25 → 1.04 (3.6 V 충전) → 3.70 (3.6 V 방전) → 1.25 (2.1 V)** [카드 산술 · 표] · 폭: D 106–163 · G 45–74 cm⁻¹ (뚜렷한 넓어짐 없음) · 점 2 충전도 같은 꼴 (G 1579.5 → 1555.5 · D 1349.5 → 1375.6) · **3.0 V 충전 ~ 2.7 V 방전에서 D · G 가 배경 위로 거의 사라지고** (`Fig. 3` · `Fig. S2`) 낮은 파수 형광이 커지며 D–G 사이에 새 띠 (figure-read ≈1380–1470 cm⁻¹ · `Fig. S4`) | [인쇄] p.27963–27965 · `Fig. 3` · `Fig. 4` · `Fig. S2`–`S5` · `Table S1` · `S2` | ✅ 전부 (`Fig. 4` 디지털 판독) |
| Q2 해석 — 삽입 · 흡착 · 도금 전후 | 저자: 모양 · R · 위치 변화 = **CB 안 소량 Li⁺ 삽입 + 표면 흡착** · 형광 = Li 석출로 탄소가 *"metallic-like state"* · 1087 · 1854 · 3648 cm⁻¹ 새 봉우리 = *"associated with Ag–Li alloying"* (배정 못 함) · ex situ 는 변화가 작다 → operando 는 비평형 (과포화) 상태 · 모형 (`Fig. 8`): 저 SOC 에서 Li 가 Ag/C 를 지나 **Ag/C \| SUS 사이**에 석출 + Ag–Li 합금 + CB 삽입 · 흡착 → 중 SOC 층 두꺼워짐 → 고 SOC Li–Ag 상 전이 연속 · ⚠ 띠 변화가 시작된 3.3 V 측정점은 셀 전류가 오르기 시작한 곳 (`Fig. S1a` figure-read ≈0.7 mA) 이라 '도금 전 삽입' 과 '도금과 함께' 를 이 자료로 못 가른다 [카드 해석] | p.27964–27967 · `Fig. 8` · `Fig. S1` | ✅ |
| ★ Q2 몇 mAh cm⁻² 까지 탄소가 Li 를 받나 | **이 논문은 재지 않았다** (mAh 와 Raman 을 잇는 숫자 없음).  대리 값 넷: ① 설계 — Ag/C 용량 ≈ 양극의 10 % → ≈1.8 mAh ≈ **0.6 mAh cm⁻²** (Ag + C 합 · [카드 산술 · 3 cm²]) ② `Fig. 2a` 첫 충전에서 ≈3.67 V 평탄 전 **figure-read ≈1.2 mAh ≈ 0.4 mAh cm⁻²** (Ag 합금 + 탄소 + 부반응 합) ③ operando G 이동이 보이기 시작한 3.3 V 측정점까지 흐른 전하 **figure-read ≈0.6 mAh** (`Fig. S1a` 적분 · 단면 셀 면적 미상) ④ CB 를 LiC₆ 까지 채운 상한 **≈0.3 mAh cm⁻²** [카드 산술 §3-8 · 밀도는 [다른 카드] 가정] — 전부 첫 충전 ≈6 mAh cm⁻² 의 **수 %–10 %** | [인쇄] p.27961 · `Fig. 2a` · `Fig. S1` · §3-8 | ✅ (`Fig. 2a` · `S1a` 디지털 판독) |
| ★ Q3 W_ad 보고서 7-1 표의 어느 행 | **'결함 · 작용기가 많은 탄소 (카본블랙 …)' 행** → 빈자리 결함 기저면 · O/N 작용기 면.  저자 모식 (`Fig. 8` 확대 그림) 이 CB 를 **'국소 정렬 층 (삽입 자리) + 작용기 (흡착 자리)'** 둘로 그린다 → 정렬 부분의 끝 상태로 '흑연 기저면 LiC₆' 는 **이상화된 끝**으로만 같이 둔다 [카드 해석] · 작용기 양은 XPS 가 없어 못 정한다 · 이 배합은 [우리 그룹] Ag–C 층 (`kang2026_…` · CB D50 35 nm · Ag 60 nm · 1 : 3 · PVDF 8 wt% · 10 µm SUS) 과 거의 같다 [다른 카드] | `Fig. 8` · p.27961 · §0-1 | ✅ |
| ★ Q3 8-3 '리튬화된 탄소 면에서 W 를 낸다' 의 근거가 되나 | **정성으로는 된다 · LiC₆ 로는 안 된다.** 충전 중 CB 의 띠가 두 점에서 같은 방향으로 바뀌고 방전 뒤 대부분 돌아온다 → '충전 중 Li 금속이 닿는 탄소는 맨 탄소가 아니다' 를 받친다.  그러나 ① Li 양 · 단계 (stage) 를 재지 않았고 ② 가장 큰 변화는 **단락 뒤** 스펙트럼이며 ③ 2 대역 맞춤에서 셋째 띠가 빠졌고 (`Fig. S4`) ④ 휴지 뒤 변화는 작고 G 가 **반대 방향**이다 — 'LiC₆ 기저면' 모형의 근거로는 쓰지 않는다 | §3-5 · §3-7 · §10 | ✅ |
| ★ Q4 한계 (침투 깊이 · 국소성 · 레이저 가열) | Raman 은 **드러난 단면 표면의 수십 nm** 만 본다 ([일반 지식] · 논문 언급 없음) · operando **점 2 개** (셀 1 개) · ex situ 10 점 중 **형광 적은 3 점을 골라** 평균 · 레이저 **3.2 mW · ≈1 µm → ≈4 mW µm⁻²** [카드 산술] · 가열 · 세기 의존 점검 **없음** · 같은 자리를 19 번 (≈76 min) 쬠 [카드 산술] · 단면은 구속이 없어 **셀 셋 다 단락** · 세기 정규화 불가 (저자 인정) · 기준 전극 없음 (셀 전압 축) | [인쇄] p.27962–27964 · `Fig. S1` · `Fig. 5` | ✅ |

⛔ **한정어 (떼지 말 것)**: ① **단면 셀이다** — 잘라서 연 면 (구속 없음 · Ar 상자 노출) 을 본다.  operando 셀은 셋 다 ≈3.85–3.9 V 에서 단면으로 단락됐고, 그 뒤 스펙트럼 (3.9 V 충전 · 방전 전부) 에 가장 큰 변화가 있다 ② **Li 양을 재지 않았다** — Raman 변화와 mAh 를 잇는 자료가 없다 ③ **상 동정 (XRD · TEM · XPS) 이 없다** — 'Li 삽입' · 'Ag–Li 합금' 은 해석이거나 인용이다 ④ **2 대역 맞춤 · 세기 비정규화** — 'aspect ratio' 는 모양이 아니라 세기 지표다 (§10-③) ⑤ operando = **실온 · 0.11 mV s⁻¹** · 사이클 · ex situ 충전 = **318 K** — 온도가 다르다.

---

## 0-1. ★ 표면 모형 고르기용 표 — 단계별 층 순서 · 탄소 상태 · 접촉 쌍

> 용도: 우리 Li 친화성 계산 (W_ad 보고서 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` **§7 · §7-1 · §8-3** — 값은 그 보고서에서만) 에서 **어느 표면 · 계면 모형을 고를지** 정하는 근거.  '대응 모형' 칸은 그 보고서 §7-1 표의 행 이름을 따랐다.  이 논문은 표면 방위 · 결함 밀도 · 작용기를 **재지 않았다** — 모형 칸은 전부 [카드 해석] 이다.

| 단계 (그림 · 조건) | 층 순서 (위 = 집전체) | 탄소 상태 (Raman) | Ag | 운전 중 계면 | 7-1 대응 모형 [카드 해석] | 근거 |
|---|---|---|---|---|---|---|
| ① 조립 직후 · 휴지 (pristine) | SUS 10 µm / **Ag/C ≈10 µm** / LPSCl ≈100 µm / PE ≈70 µm / Al | D 1355 · G 1583 · R 1.25 (점 1) · 1.13 (점 2) · 2D 없음 → 결함 많은 터보스트래틱 CB · 탐침 자리에 SE 신호 (≈420–440 cm⁻¹ 둔덕 · figure-read) 가 섞인다 | D50 60 nm 입자 · 분포 사진 없음 | SUS \| Ag/C · Ag/C \| LPSCl (= CB \| LPSCl + Ag \| LPSCl) · CB–Ag | 탄소 = **'결함 · 작용기가 많은 탄소'** 행 · Ag = Ag(111) · 집전체 = **SUS (7-1 표에 없음 — Cu 행만 있다)** | `Fig. 1b` · `Fig. 2c` · p.27961 |
| ② 충전 앞부분 (operando 0.45–3.0 V · 흐른 전하 ≲0.3 mAh figure-read) | 같음 (Li 금속 층 아직 없음 [카드 해석]) | 모양 거의 그대로 (G 1575–1584 · D 1358–1362) · 1087 cm⁻¹ 작은 봉우리 (≈0.9–2.4 V · 점 1) · 낮은 파수 형광 시작 | — | 같음 + SE 환원 (탄소 · Ag 가 SE 와 닿은 면 · 논문은 다루지 않음) | 맨 결함 탄소 (흡착 자리) | `Fig. 3` · `Fig. S1b` · `Fig. S3` |
| ③ 충전 (operando 3.3–3.9 V · ≈0.6 → 3–3.5 mAh figure-read) | SUS / **Li 금속** / Ag/C / LPSCl (모식 · ex situ 단면으로 확인) | **G ≈1559–1566 · D ≈1366–1376** · R 점마다 다름 (점 1 1.04–1.29 · 점 2 1.21–1.35) · 형광 큼 · D–G 사이 새 띠 · 1854 cm⁻¹ 봉우리 | Li–Ag 합금 (저자 · 인용 근거 · 직접 증거 없음) | **Li \| SUS** · **Li \| Ag/C 아랫면** (Li \| 리튬화 CB · Li \| Li–Ag) · Ag/C \| LPSCl · 단면에서는 SE 안 금속광 석출물 · 균열 (`Fig. 5a`) | 탄소 = **리튬화된 결함 탄소 (LiₓC · x 미정)** — 7-1 표에 없는 행 · LiC₆ 기저면은 이상화된 끝 · 합금 = Li–Ag 면 | `Fig. 3` · `Fig. 4` · `Fig. S4` · `Fig. 8` · `Fig. S8` |
| ④ 방전 (operando 3.6 → 2.1 V · 단락 뒤) | Li 층이 얇아짐 [카드 해석 · 방전 단면은 2.1 V 한 장] | 3.6–2.7 V: 띠가 배경 위로 거의 사라짐 (G 높이 24–87 · R 2.3–3.7 · 점 1) → 2.4–2.1 V: 다시 나타나 초기 쪽으로 (G 1572 → 1575 · R 1.43 → 1.25) · 1854 남음 | — | Li 가 빠지며 Li \| C 가 C \| SUS (또는 공극) 쪽으로 [카드 해석] | 탈리튬 결함 탄소 (≈ 맨 탄소) | `Fig. 3` · `Fig. 4` · `Fig. 5` · `Table S1` |
| ⑤ 각 SOC 에서 5 h 휴지 뒤 (ex situ) | SUS / **Li 층 (100 % 주석 ≈50 µm)** / Ag/C / LPSCl | 변화 작음: R 1.17 → 1.08–1.13 (29–100 %) → 1.52 (방전 0 %) · **G +5–9 cm⁻¹ (위로)** · 3650 cm⁻¹ 만 나타났다 사라짐 | — | Li \| SUS · Li \| Ag/C 아랫면 | '약하게 리튬화된 결함 탄소' — Raman 으로는 맨 탄소와 잘 안 갈린다 | `Fig. 6` · `Fig. 7` · `Fig. S7` · `Fig. S8` · `Table S3` |

이 표로 보고서에 더할 것 (§8 · 끝 보고 (e) 와 같은 내용):
- **Li \| C 쌍의 탄소 쪽은 두 끝으로 낸다** — 맨 결함 탄소 (① · ④ · 방전 끝) 와 리튬화된 결함 탄소 (③).  카본블랙에서 'LiC₆ 기저면' 은 정렬된 일부의 이상화된 끝이지 운전 조건의 대표가 아니다 (Li 양 미정 · 휴지 뒤 변화 작음).
- **집전체는 SUS 다** — 이 셀 · Lee 2020 계열 · [우리 그룹] `kang2026_…` 도 SUS 박 · 막대 [다른 카드].  W_ad 보고서 7-1 의 집전체 행은 Cu(111) 뿐이다.  SUS 의 맨 면은 Cr 이 많은 산화막이라 Li 와 반응한 뒤의 면이 운전 조건에 가깝다 [일반 지식 · 이 논문은 다루지 않음].
- Li 는 **Ag/C 와 집전체 사이**에 쌓인다 (ex situ 단면 · `Fig. S8`) — [`metzler2026_…`] (Cu \| C 사이) · [`metzler2025_…`] (구조화 층) 와 같은 방향이다 [다른 카드].  그래서 운전 중 Li 금속이 닿는 탄소는 **Ag/C 층의 집전체 쪽 면**이다.

---

## 1. 한 줄 요약

카본블랙 기반 Ag/C 층 (CB 38 nm + Ag 60 nm · 1 : 3 · PVDF · 10 µm · SUS 위) 을 깐 무음극 Li₆PS₅Cl | NCM90 적층 셀의 **단면**을 532 nm 현미 Raman 으로 충방전 중에 본 첫 보고다.  operando (실온 · 0.11 mV s⁻¹) 에서 CB 의 G 띠는 충전 3.3–3.9 V 에 **≈20–25 cm⁻¹ 내려갔다가** (1583 → 1559) 방전 끝 2.1 V 에서 1575 로 돌아왔고, D 띠는 거꾸로 올랐다가 돌아왔다.  저자는 이를 **비정질 CB 에도 Li⁺ 가 일부 삽입 · 흡착된다**는 증거로 읽고, 1087 · 1854 · 3648 cm⁻¹ 새 봉우리를 Ag–Li 합금화와 '관련' 있다고만 한다.  각 SOC 에서 5 h 쉰 뒤 (ex situ) 의 변화는 작았다 — 저자는 operando 가 비평형 (과포화) 상태를 잡는다고 결론짓는다 (p.27967–27968).

⚠ 단 ① Li 양을 재지 않았고 ② 가장 큰 변화는 단면 단락 (≈3.85 V) 뒤의 스펙트럼이며 ③ 'aspect ratio' 는 정규화 안 된 높이로 만든 세기 지표이고 ④ `Fig. 4` 점 2 방전 계열은 `Table S2` 와 맞지 않는다 (§10).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 계 | 무음극 (anode-free) 황화물 전고체 Li 이온 셀 (AF-ASSB) — **Li₆PS₅Cl** SE · LZO 코팅 **LiNi₀.₉Co₀.₀₅Mn₀.₀₅O₂** (NCM90) 양극 · **Ag/카본블랙 층** · SUS 음극 집전체 · 적층 (laminate) 파우치 · WIP |
| 던지는 질문 | 충방전 중 Ag/C 층의 **카본블랙 구조**가 어떻게 바뀌나 — Li 석출이 집전체 쪽에서 일어나는 이유 (Suzuki 2021 의 '과포화 CB 에서 Li 석출' 설명) 를 실험으로 받칠 수 있나 |
| 문헌 갭 (p.27961) | Suzuki 2021 (ref 30): Li 석출 과전압 때문에 0 V 아래로 내려가도 바로 석출되지 않고 *"The CB layer continuously accumulates Li atoms and becomes oversaturated. Li precipitates from the CB particles as a result of phase separation of the oversaturated CB (not formed directly from the reduction of Li⁺ in the SE layer)"* — *"This explanation, however, has not been supported by experimental results"* · Spencer-Jolly 2023 (ref 31) 은 operando XRD 를 **흑연** Ag/C 로 했다 — *"the reported Ag/C anode consisted of CB, and it is desirable to observe a CB-based Ag/C anode"* |
| 방법 선택 | 단면 현미 Raman — *"to identify slight morphological changes and metastable structural states on the Ag/C layer surface under dynamic conditions"* (p.27961) |
| 서론의 셀 주장 (p.27961) | AF 가 ASSB 에 유리한 이유로 *"SE does not generate solid electrolyte interphase (SEI) and exhaustion of electrolyte …does not occur"* — ⚠ LPSCl 은 Li 전위에서 환원된다 (§10-⑪) |
| 글의 꼴 | 서론 → 실험 (셀 제작 · operando · ex situ) → 결과 (전기화학 · operando · ex situ 비교 · 모형 `Fig. 8`) → 결론 · 본문 그림 8 · 표 0 · 참고문헌 52 / SI: 그림 S1–S8 · 'D · G 띠 해설' 1 쪽 (S-7–S-8 · 참고문헌 S1–S4) · 표 S1–S3 |
| 이 논문이 하지 않은 것 | 상 동정 (XRD · TEM · XPS) · 기준 전극 · Li 양 정량 · 레이저 세기 · 가열 대조 · Ag 없는 CB 층 대조 · 맨 탄소 · 흑연 기준 시료 · 반복 셀 통계 · 결함 · 작용기 정량 · 점착 · 압력 측정 |

---

## 3. 핵심 수치 총정리 ★

### 3-1. 제작 · 셀 (p.27961–27962 · `Fig. 1`)

| 부품 | 값 | 표지 |
|---|---|---|
| SE | **Li₆PS₅Cl** argyrodite · *"ionic conductivity is ∼2 mS cm⁻¹ at room temperature"* (측정 자료 · 공급처 없음) · 분말 + **아크릴 결합제 1 wt%** · 자일렌 + 다이에틸벤젠 슬러리 · **부직포** 위 블레이드 도포 · 313 K 공기 건조 · 시트 **≈100 µm** · 313 K 진공 12 h · 2.2 cm 정사각 | [인쇄] p.27961 |
| 양극 | **LiNi₀.₉Co₀.₀₅Mn₀.₀₅O₂** (고 Ni NCM) · **LZO (Li₂O–ZrO₂)** 졸–겔 코팅 (2-프로판올 : Li 메톡사이드 : Zr(IV) 테트라프로폭사이드 = 200 : 2 : 1 몰) · 회전 유동 코팅기 (SFD-01, Powrex) 분무 · 623 K 1 h 공기 · NCM : SE : CNF : PTFE = **85 : 15 : 3 : 1.5** (wt) 시트 · 1.7 cm 정사각 (**≈3 cm²**) · Al 18 µm 위 · ≈70 µm | [인쇄] p.27961 · `Fig. 1a` (3 cm² 점선) |
| ★ Ag/C 층 | **CB 12 g (D50 = 38 nm) + Ag 4 g (D50 = 60 nm)** 를 **PVDF 8 wt% 포함 NMP 용액 14 g** 에 넣고 저으며 NMP 50 g 을 천천히 더해 슬러리 → **SUS 박 10 µm** 위 블레이드 도포 → 353 K 공기 20 min → 373 K 진공 12 h (건조실) · 2 cm 정사각 · 로딩은 *"capacity of the Ag/C layer is ∼10% that of the PE layer"* · 두께 **≈10 µm** · [카드 산술] 건조 조성 CB : Ag : PVDF = 12 : 4 : 1.12 g = **70.1 : 23.4 : 6.5 wt%** (Ag : CB = 1 : 3) | [인쇄] p.27961–27962 · `Fig. 1b` |
| 조립 | PE · SE · Ag/C 를 이 순서로 쌓아 진공 적층 필름에 봉함 (건조실 · 이슬점 ≈223 K) → **WIP 490 MPa · 353 K · 30 min** · 설계 용량 **≈18 mAh (C/10)** · 두께 PE ≈70 · SE ≈100 · Ag/C ≈10 µm | [인쇄] p.27962 |
| 겉모양 | 적층 셀 **4 cm × 4 cm** · 활성 3 cm² · 단면 사진: SUS / Ag/C (10 µm) / SE (100 µm) / PE (70 µm) / Al · **측정점 1 · 2 = Ag/C 층 안** | `Fig. 1a,b` (그림 글자) |

### 3-2. 전기화학 (p.27962–27963 · `Fig. 2a,b` · `Fig. S1` · `Fig. S7`)

| 실험 | 값 | 표지 |
|---|---|---|
| 사이클 (자르지 않은 셀) | CCCV **5 mA (C/4)** · 4.2–2.5 V · 4.2 V CV 2 h · **318 K** · 구속 셀 **≈2 MPa** · 첫 방전 본문 *"about 16 mA h"* — figure-read **≈15.0 mAh** (첫 충전 CC 4.2 V 도달 ≈16.1 · CV 끝 ≈18.4 mAh) · CE **81 % (1) · 95 % (2) · >99.98 % (300 까지)** · 유지율 figure-read ≈91 % (2 회) → **≈71 % (300 회)** · 300 회 방전 figure-read ≈10.6 mAh | [인쇄] p.27962 · figure-read `Fig. 2a,b` |
| 첫 충전 앞부분 (디지털 판독) | 전압이 0.4 mAh 에서 ≈3.44 V · 0.5 mAh ≈3.47 V (어깨) · 1.0 mAh ≈3.63 V · **≈1.2 mAh 에서 ≈3.67 V 평탄으로 꺾임** · 그 뒤 3.69 (1.6) · 3.72 V (2.9 mAh) · 5 회 이후 곡선은 처음부터 ≈3.65–3.7 V (낮은 전압 구간이 없다) | figure-read `Fig. 2a` |
| operando 셀 (전위 주사) | 잘라 낸 적층 셀 · 석영 관찰창 셀 · ≈2 MPa · Ar 상자 (이슬점 ≈185 K) · 포텐쇼스탯 HZ-7000 (Meiden Hokuto) · **0.11 mV s⁻¹** · 본문 *"within an open-circuit voltage range from 4.0 to 2.1 V"* — 실제 그림은 **OCV figure-read ≈0.45 V 에서 시작**해 위로 → 단락 → 2.1 V 까지 아래로 · 측정점 = 0.3 V 마다 (충전 13 · 방전 6) | [인쇄] p.27962 · `Fig. S1a` |
| `Fig. S1` 전류 | 3.0 V 아래 µA 수준 (`Fig. S1b`: ≈0.58 V 에서 시작 · **≈0.68 V 에 ≈1.8 µA 작은 꼭지** · 1.55 V 에서 0.010 mA) · figure-read 3.0 V ≈0.25 · 3.3 V ≈0.7 · 3.57 V ≈0.9 mA → 3.6–3.85 V 가파르게 · **≈3.85 V 마지막 측정점 ≈6.5 mA → 그 직후 ≈15.5 mA 스파이크 = 단락** · 본문: *"The main current peak around 3.7 V"* (NCM 탈리 ↔ SUS 위 Li 석출) · **단락은 다른 operando 측정 (n = 3) 에서도** → *"most likely occurred through the cross-sectional surface rather than inside the cell"* · 단락 뒤 OCV ≈3.7 V 안정 · 2.1 V 까지 방전 (본문 꼭지 *"around 3.6 V"* — figure-read **≈3.3–3.4 V · ≈ −1.1 mA**) | [인쇄] p.27963 · figure-read `Fig. S1` |
| ex situ 셀 | 단면 셀을 같은 관찰창 셀에 · **0.5 mA × 4 h (≈2 mAh) · 318 K** 정전류 → 5 h 휴지 → 실온 Raman · 본문 *"capacities during the constant-current period were confirmed to be approximately 10 mA h, corresponding to 56% of the theoretical value"* · 휴지 5 h 로 *"sufficient relaxing states"* · SOC 표지 충전 15 · 29 · 44 · 59 · 73 · 100 % / 방전 58 · 15 · 0 % (SOC 정의 없음 — §3-8 ⑧) · 15 % 휴지 전압이 ±0.15 V 로 출렁이고 44 % 충전에 4.05 V 스파이크 (figure-read) | [인쇄] p.27962 · p.27966 · `Fig. S7` |

### 3-3. Raman 측정 조건 (p.27962 · SI S-7)

| 항목 | operando | ex situ |
|---|---|---|
| 장치 | 현미 Raman **NRS-4500 (Jasco)** · 셀째 현미경 안 | 같은 셀 · 같은 조건 |
| 들뜸 · 출력 | **532.0 nm · 3.2 mW** · 대물 **50×** · 핀홀 ϕ 34 µm · 회절격자 900 mm⁻¹ · 레이저 크기 **∼1 µm** · 광학 분해능 ≈4.7 cm⁻¹ | 같음 |
| 노출 | **60 s × 4 회 적산** · 바탕 보정 없이 원 스펙트럼으로 실음 (`Fig. 3`) | 같음 |
| 자리 | Ag/C 층 안 **점 2 개** (`Fig. 1b`) · 셀 부피 변화 단면에서 **±5 µm** → x–y 대로 자리 유지 | Ag/C 층 **10 점** (폭 방향 ≈2 mm 간격) → **형광이 적은 3 개를 골라** 맞춤 변수 평균 |
| 보정 | 폴리프로필렌 띠 위치로 파수 보정 | 같음 |
| 온도 | **실온** (값 미기재) | 충방전 318 K · Raman 실온 |
| 하지 않은 것 | 레이저 세기 바꾸기 · 가열 점검 · 같은 자리 레이저만 쬔 대조 (OCV) · 맨 CB 층 대조 · 침투 깊이 논의 | 같음 |

### 3-4. 초기 탄소 — 띠 위치 · 폭 · R (p.27962–27963 · `Fig. 2c` · SI S-7–S-8 · `Table S1`–`S3`)

| 시료 | D (cm⁻¹ · FWHM) | G (cm⁻¹ · FWHM) | R = H_D / H_G | 표지 |
|---|---|---|---|---|
| CB 분말 (밀봉 셀) | **1349** | **1589** | 원 높이 figure-read ≈**1.0** (1000–1850 직선 바탕) | [인쇄] p.27962 · figure-read `Fig. 2c` |
| Ag/C 층 단면 (operando 셀 · 초기) | 1349–1355 (본문 *"same positions as those of the CB powder"*) | — | — | [인쇄] p.27963 |
| 맞춤 · 점 1 초기 | 1355.1 · 158.4 | 1582.9 · 66.4 | **1.25** | [카드 산술] `Table S1` |
| 맞춤 · 점 2 초기 | 1349.5 · 157.7 | 1579.5 · 67.2 | **1.13** | [카드 산술] `Table S2` |
| 맞춤 · ex situ 초기 3 스펙트럼 | 1350.0–1355.8 · 168.9–180.1 | 1575.9–1580.9 · 63.5–65.0 | 1.14 · 1.20 · 1.14 (평균 **1.17**) | [카드 산술] `Table S3` |

- 저자 판정: *"These D-(A1g) and G-(E2g) bands agree with the characteristics of the disordered carbon materials because of their wide peak widths and similar intensities. Such broad peaks … are known to be characteristic of disordered carbon with partially ordered graphene layers (low crystallinity)"* (p.27962–27963 · refs 41–44).  Ag/C 단면의 띠 위치가 분말과 같으므로 *"no structural change or disintegration has occurred during the cell fabrication process"* (p.27963).
- SI 해설 (S-7–S-8): D2 (≈1620) · D3 (≈1500 · 비정질) · D4 (≈1200) 는 *"often quite weak … hidden in the intense and broad D-band"* · 이 측정은 S/N 이 낮고 단면 Ag/C 가 다공이라 *"the D2-, D3-, and D4-band was not clear observed, even though the use of the amorphously CB with much defects"* → **2 대역 맞춤**.  R 은 *"reported to corelate on the crystallite size (La) … this may increase with decreasing the La"* (SI S-7).
- [카드 해석] 높이비 ≈1.1–1.25 · G 폭 ≈66 cm⁻¹ · 날카로운 2D 없음 = **결함 · 무질서가 많은 나노결정 ~ 비정질 경계의 탄소** — [`metzler2026_…`] 의 MTI 상용 탄소 (높이비 ≈1.3–1.4 · 2D 2689 있음) 보다 질서가 조금 낮거나 비슷하고, [`kang2026_…`] 의 LC CNF (0.99) · HC CNF (0.19) 와는 측정 · 맞춤 조건이 달라 숫자를 바로 견주지 않는다 [다른 카드].  ⚠ 높이비는 맞춤 방식에 따라 달라진다 — 같은 스펙트럼의 원 높이비 ≈1.0 대 2 대역 맞춤 ≈1.1–1.25 (D 가 넓어 G 자리의 원 높이에 D 꼬리가 섞인다).

### 3-5. ★ operando D · G 변화 (p.27963–27965 · `Fig. 3` · `Fig. 4` · `Fig. S2`–`S5` · `Table S1` · `S2`)

**스펙트럼 모습 (실독 · `Fig. 3` 점 1 · `Fig. S2` 점 2)**
- 0.6–2.7 V 충전: D · G 가 또렷하고 모양이 초기와 비슷하다 · 낮은 파수 (≲800 cm⁻¹) 에서 형광 기울기가 커지기 시작 · 점 1 의 1087 cm⁻¹ 작은 날카로운 봉우리가 ≈0.9–2.4 V 에 보인다 (figure-read · 확대).
- 3.0–3.9 V 충전: D · G 가 작아지고 G 가 낮은 파수 쪽 어깨처럼 바뀐다 · 형광 기울기가 가장 크다 · 1854 cm⁻¹ 봉우리가 ≈2.4 V 부터 또렷해진다 (figure-read).
- 3.6–3.0 V 방전: **D · G 가 배경 위로 거의 사라진다** (점 1 · 점 2) · 1854 는 남는다.
- 2.7 → 2.1 V 방전: D · G 가 다시 나타나 2.1 V 에서 초기보다 높은 세기 · 1854 는 2.1 V 까지 남는다 · 2.1 V 스펙트럼은 2600–3000 cm⁻¹ 넓은 띠도 초기보다 크다.
- 바탕 보정한 `Fig. S4`: 3.9 V 충전 · 3.6 V 방전에서 **D 와 G 사이 ≈1380–1470 cm⁻¹ 에 새 띠** ('Appeared band') — 3.6 V 방전 스펙트럼은 그 띠가 가장 큰 넓은 둔덕이다 (figure-read) · 3.9 V 충전 점 1 의 G 꼭대기는 figure-read **≈1555 cm⁻¹** (원 스펙트럼에서도 내려갔다).

**맞춤 변수 (2 대역 pseudo-Voigt · `Table S1` 점 1 · R · AR 은 [카드 산술])**

| 측정점 | D 위치 · 폭 | G 위치 · 폭 | H_D · H_G (a.u.) | R | AR = ΣH/ΣW |
|---|---|---|---|---|---|
| 초기 (≈0.48 V) | 1355.1 · 158.4 | 1582.9 · 66.4 | 379.3 · 303.2 | 1.25 | 3.04 |
| 0.6 V 충전 | 1358.1 · 144.4 | 1583.9 · 70.4 | 184.2 · 150.2 | 1.23 | 1.56 |
| 2.1 V 충전 | 1359.2 · 151.2 | 1579.3 · 66.0 | 627.7 · 494.0 | 1.27 | 5.16 |
| 2.7 V 충전 | 1360.3 · 156.2 | 1577.2 · 60.8 | 710.6 · 575.8 | 1.23 | **5.93** |
| 3.0 V 충전 | 1362.2 · 141.7 | 1575.4 · 61.2 | 444.1 · 362.5 | 1.23 | 3.98 |
| 3.3 V 충전 | 1365.9 · 126.3 | **1565.9** · 64.8 | 262.4 · 235.5 | 1.11 | 2.61 |
| 3.6 V 충전 | 1368.8 · 106.1 | **1558.8** · 73.5 | 114.7 · 109.8 | **1.04** | 1.25 |
| 3.9 V 충전 (단락 직전) | 1368.5 · 157.3 | 1559.6 · 59.4 | 202.6 · 157.1 | 1.29 | 1.66 |
| 3.6 V 방전 | 1379.8 · 152.3 | **1540.5** · 45.5 | 90.7 · **24.5** | **3.70** | 0.58 |
| 3.3 V 방전 | **1381.7** · 141.1 | 1541.9 · 58.8 | 115.9 · 36.7 | 3.16 | 0.76 |
| 3.0 V 방전 | 1379.9 · 150.0 | 1547.8 · 59.2 | 173.5 · 52.0 | 3.34 | 1.08 |
| 2.7 V 방전 | 1375.5 · 138.6 | 1556.3 · 60.8 | 195.7 · 86.9 | 2.25 | 1.42 |
| 2.4 V 방전 | 1365.2 · 152.9 | 1572.0 · 62.2 | 550.6 · 385.9 | 1.43 | 4.35 |
| 2.1 V 방전 | 1362.4 · 163.0 | **1575.0** · 60.6 | 686.8 · 550.3 | **1.25** | 5.53 |

- 점 2 (`Table S2`): 초기 D 1349.5 · G 1579.5 · R 1.13 → 1.2–1.8 V 충전 D 1361–1362 · G 1586–1587 (G 가 조금 **올라간다**) → 3.3 V G 1572.1 → **3.6 V G 1556.6 · D 1375.7 → 3.9 V G 1555.5 · D 1375.6 · R 1.35** · 방전 (표): 3.6 V D 1385.3 · G 1544.3 · R 2.71 / 3.3 V 1385.8 · 1541.6 · 3.61 / 3.0 V 1361.1 · 1540.4 · **6.65 (G 높이 9.4)** / 2.7 V 1365.8 · 1550.0 · 1.84 / 2.4 V 1358.7 · 1569.4 · 1.77 / 2.1 V 1357.2 · 1575.7 · 1.35 [카드 산술].  ⚠ 이 방전 행들은 `Fig. 4` 의 점 2 방전 계열과 맞지 않는다 (§10-⑧).
- 저자 서술 (p.27964–27965): aspect ratio 최대는 *"around 2.1–2.4 V at both measurement points"* (표로는 충전 최대 = 2.7 V · 방전 최대 = 2.1 V) · R 은 *"trends … were different for each measurement point in the charge process, these values decreased during the discharge process in all voltage ranges"* · D 위치는 *"increased up to approximately 1.5 V, then slightly decreased up to approximately 2.4 V, and finally increased further during the charge process, while the position increased continuously during the discharge process"* (⚠ 시간 순으로는 방전 중 1380 → 1362 로 **내려간다** — 전압 축으로 읽은 서술) · G 위치는 *"slightly decreased continuously below approximately 3.0 V and then decreased considerably at a higher voltage during the charge process, whereas a substantial increase in all voltage regions was observed during the discharge process"* · *"The gradual changes (especially for the G-band position) should correspond to the partial intercalation/deintercalation reaction of Li⁺"*.
- 저자의 흑연 비유 (p.27965 · refs 44, 48–51): 액체 전해질 흑연에서 stage 4 (LiC₃₆) → stage 1 로 갈 때 *"the G-band begins to shift to a lower wavenumber and split of peak shapes, and then to a broader shape"* — *"as similar trends were observed, CB was also expected to intercalate Li"* (⚠ §10-⑤).
- 맞춤 형태 변수: D 의 Lorentz 비가 충전 중 0–0.44 에서 **방전 3.6–2.7 V 에 0.81–1 (점 1) · 1 (점 2)** 로 튄다 — 띠가 약해지면 맞춤 모양이 흔들린다 [카드 해석].

### 3-6. 새 봉우리 · 석출물 (p.27965–27966 · `Fig. 3` · `Fig. 5` · `Fig. S4`)

| 관찰 | 값 · 서술 | 표지 |
|---|---|---|
| operando 새 봉우리 | **≈1087 · 1854 · 3648 cm⁻¹** 가 충전 중 나타남 · 1854 는 방전 뒤에도 남음 (`Fig. 3` 초록 띠) · figure-read: 1087 은 점 1 에서 ≈0.9–2.4 V 충전에만 · 1854 는 ≈2.4 V 충전부터 2.1 V 방전까지 · 3648 은 넓은 둔덕 위 아주 작은 꺾임 (점 2 `Fig. S2` 에서 더 또렷) | [인쇄] p.27965 · figure-read |
| 저자 해석 | Ag/C 층의 Ag–Li 합금화는 *"a previous report, transmission electron microscope and electron diffraction pattern observations … in the Ag/C layer of an AF-ASSB system with the same cell configuration"* (ref 27 — §10-⑩) → *"This charging mechanism may affect the obtained Raman spectra, such as the observed additional peaks"* · *"the precise assignment of these additional peaks remains difficult"* | [인쇄] p.27965–27966 |
| 단면 사진 (`Fig. 5a`) | 3.9 V (단락 뒤): SE 층의 Ag/C 가까이에 **선 모양 균열 · 금속광 작은 석출물** (석출물 1 · 2) · 방전 뒤에도 대부분 남음 · 양극도 단락 뒤 약한 금속광 · *"these cracks and precipitates induced the short-circuit in the case with the cross-section"* | [인쇄] p.27965 · `Fig. 5a` |
| 석출물 Raman (`Fig. 5b`) | 석출물 1 · 2 = **≈1848 cm⁻¹ 봉우리 · D · G 없음** · 낮은 파수 형광 + ≈420–480 · ≈800 cm⁻¹ 둔덕 (figure-read) · 3.9 V 점 1 · 2 = D · G (G 가 ≈1555 쪽) + 1848 | `Fig. 5b` |
| 저자의 배제 | 측정점이 금속광이라 LPSCl 분해 산물이 아니다 · LPSCl 환원 산물 Li₂S 는 **383 cm⁻¹** (ref 52) 라 1848 · D · G 와 떨어져 있다 · *"this formed compound could diffuse physically into the SE layer owing to insufficient pressure at the cross-section"* | [인쇄] p.27966 |

### 3-7. ex situ (p.27966–27967 · `Fig. 6` · `Fig. 7` · `Fig. S7` · `Fig. S8` · `Table S3`)

| 관찰 | 값 | 표지 |
|---|---|---|
| Li 층 위치 | 모든 SOC 에서 **Ag/C 층과 SUS 집전체 사이**에 또렷한 Li 층 · 100 % 그림 주석 **"Deposited Li · 50 µm"** · 저자: *"Li⁺ may deposit onto the SUS current collector because it has more space there than between the SE and Ag/C layers"* | [인쇄] p.27966 · `Fig. S8` |
| 스펙트럼 (`Fig. 6` · 대표 1 장씩) | 형광이 *"in the lower wavenumber region was observed with higher SOC"* (본문 · ⚠ 그림에서는 15–44 % 의 바탕 기울기가 더 크다 · 대표 1 장이라 약한 판독) · 2600–2800 · 3500 cm⁻¹ 넓은 둔덕 · 새 봉우리는 **3650 cm⁻¹ 하나만** (충전 중 · 방전에서 사라짐) · 1087 · 1854 는 **안 나옴** | [인쇄] p.27966 · `Fig. 6` |
| 맞춤 (3 점 평균 · `Fig. 7`) | AR 충전 중 *"slightly continuous increasing"* → 방전 감소 (변화 폭 operando 보다 작음) · R *"continuous decrease/increase trend in the charge and discharge processes"* · 위치는 *"did not show clear trends"* | [인쇄] p.27966–27967 |
| figure-read `Fig. 7` (디지털 판독) | R: 초기 ≈1.19 → 15 % ≈1.34 → 29 % 1.10 · 44 % 1.13 · 59 % 1.09 · 73 % 1.12 · 100 % ≈1.13 → 방전 58 % 1.15 · 15 % 1.30 · 0 % ≈1.52 / D (충전) 1352–1357 · (방전) 1358–1368 / G 초기 1579.6 → 충전 1582.6–1587.1 · 방전 1586–1591 / AR 초기 ≈1.1 → 44 % 2.73 · 100 % ≈2.9 · 오차 막대가 크다 (정의 없음) | figure-read `Fig. 7` |
| `Table S3` 평균 [카드 산술] | R 1.17 → 1.38 (15 %) → 1.08 · 1.12 · 1.09 · 1.12 · 1.12 (29–100 %) → 1.10 · 1.37 · 1.52 (방전 58 · 15 · 0 %) / G 1579.1 → 1583.5–1587.7 → 1585.5–1591.8 / D 1353.7 → 100 % **1347.7** → 방전 15 % 1372.9 | [카드 산술] `Table S3` |
| 저자 결론 | *"the morphological and structural changes in the Ag/C layer are slight compared with the operando measurement, even though metallic Li deposition occurs"* · operando 는 *"insufficiently reached a steady-state"* · *"relatively high scan rate of potential sweep and room temperature and may have partially formed an over-saturated state in the Ag/C layer"* → *"ex situ Raman spectroscopy basically supports the results of the operando measurement, and different behaviors can be explained by the kinetic changes"* | [인쇄] p.27966–27967 |

### 3-8. 카드 산술 모음 (원문에 없는 값 — 식 · 가정 병기)

| 양 | 값 | 식 · 가정 |
|---|---|---|
| ① Ag/C 건조 조성 | CB 70.1 · Ag 23.4 · PVDF 6.5 wt% (Ag : CB = 1 : 3) | 12 : 4 : (14 × 0.08 = 1.12) g · 용매는 증발 |
| ② 사이클 전류 밀도 | **≈1.7 mA cm⁻²** (C/4) | 5 mA / ≈3 cm² (양극 면적 · `Fig. 1a`) |
| ③ 면적 용량 · Li 두께 | 설계 ≈6 mAh cm⁻² · 첫 충전 figure-read ≈18.4 mAh → ≈6.1 mAh cm⁻² → 치밀 Li **≈30 µm** | 1 mAh cm⁻² ≈ 4.85 µm Li (몰부피 13.0 cm³ mol⁻¹ · 3.6 C mAh⁻¹) |
| ④ Ag/C 설계 용량 | ≈1.8 mAh ≈ **0.6 mAh cm⁻²** (Ag + C 합) | 18 mAh × 10 % / 3 cm² · '용량' 을 Li 저장 용량으로 읽음 [카드 해석] |
| ⑤ CB 의 LiC₆ 상한 · Ag 몫 | CB **≈0.33 mAh cm⁻²** · Ag → Li₁₀Ag₃ ≈0.24 · LiAg ≈0.07 mAh cm⁻² · 합 ≈0.4–0.57 | 층 10 µm × 겉보기 밀도 **1.25 g cm⁻³ [다른 카드 가정 — `kang2026_…` 같은 배합 7.8 µm 층의 값]** = 1.25 mg cm⁻² · CB 0.70 × 372 mAh g⁻¹ (LiC₆ · 비정질 CB 가 실제로 이만큼 받는지는 모른다) · Ag 0.23 × 828 (Li₁₀Ag₃) · 248 (LiAg) mAh g⁻¹ — ④ 의 0.6 과 같은 자릿수 |
| ⑥ 탄소 몫 | LiC₆ 상한으로도 첫 충전의 **≈5 %** | 0.33 / 6.1 |
| ⑦ operando 흐른 전하 (`Fig. S1a` 적분) | 3.0 V 까지 ≈0.3 · **3.3 V 까지 ≈0.6** · 3.6 V 까지 ≈1.0 · **단락 직전 (≈3.85 V) ≈3–3.5 mAh** · 방전 (3.6 → 2.1 V) ≈1.9 mAh | Q = ∫ I dV / (0.11 mV s⁻¹) · 디지털 판독 · 2–3 V 구간은 선이 겹쳐 대략 (±30 %) · 단면 셀 면적 미상 (3 cm² 면 ≈0.2 / 0.33 / 1.0–1.2 mAh cm⁻²) |
| ⑧ ex situ 전하 (`Fig. S7`) | 충전 CC 구간 figure-read ≈4 h × 5 + **≈7 h (100 %)** → **≈13.5 mAh** · 방전 ≈3.7 + 4 + **1.4 h (2.0 V 에서 멈춤)** → **≈4.5 mAh** · SOC 표지가 '누적 ÷ 그 방향 합' 과 맞는다 (2 / 4 / 6 / 8 / 10 / 13.5 → 15 / 29 / 44 / 59 / 73 / 100 % · 방전 2.7 / 0.7 ÷ 4.5 → 59 / 15 %) | 0.5 mA 가정 · 2 h 격자 덧씌워 읽음 · ⚠ 본문 '≈10 mAh (56 %)' 와 안 맞는다 (§10-⑨) |
| ⑨ ex situ 100 % Li 두께 | 주석 ≈50 µm 대 치밀 환산 **≈22 µm** (≈2.3 배) | ≈13.5 mAh / 3 cm² × 4.85 µm · 면적 3 cm² 가정 · 단면 (구속 없음) 의 Li 가 성기거나 면적 가정이 틀렸다 [카드 해석] |
| ⑩ operando 부피 변화 검산 | ±5 µm (본문) 대 ≈3–3.5 mAh → ≈1.0–1.2 mAh cm⁻² → 치밀 Li **≈5–6 µm** | 3 cm² 가정 · 자릿수가 맞는다 |
| ⑪ operando 시간 | 충전 주사 ≈8.6 h · 방전 ≈4.4 h · 측정점 간격 ≈45 min · 스펙트럼 1 장 (240 s) = **≈26 mV** 주사 · 같은 자리 19 장 = **≈76 min** 레이저 | 0.3 V / 0.11 mV s⁻¹ = 2727 s · 3.4 V · 1.75 V 주사 |
| ⑫ 레이저 출력 밀도 | **≈4 mW µm⁻² (≈4 × 10⁵ W cm⁻²)** | 3.2 mW / π (0.5 µm)² · '레이저 크기 ∼1 µm' 를 지름으로 [가정] |
| ⑬ 'aspect ratio' 가 세기 지표라는 증거 | 같은 물질 초기값 점 1 **3.04** 대 점 2 **1.81** (1.7 배) · 폭 합은 225 대 225 cm⁻¹ 로 같고 높이 합만 683 대 407 | `Table S1` · `S2` 초기 행 |

---

## 4. 계산 방법 ★ — 이 논문에는 없다 (실험 방법을 대신 적는다)

- **DFT · AIMD · MLIP · 무질서 처리 · 연속체**: 없음 (원자단위 · 연속체 모델 0).
- **전기화학**: 적층 파우치 (WIP 490 MPa · 353 K) · 구속 셀 ≈2 MPa · CCCV 5 mA · 318 K / 단면 셀 전위 주사 0.11 mV s⁻¹ (HZ-7000) / 단면 셀 정전류 0.5 mA × 4 h + 5 h 휴지 (318 K).  기준 전극 없음 (셀 전압).
- **분광**: 현미 Raman NRS-4500 (Jasco) · 532.0 nm · 3.2 mW · 50× · 핀홀 ϕ 34 µm · 900 mm⁻¹ · ∼1 µm · ≈4.7 cm⁻¹ · 60 s × 4 · 폴리프로필렌 파수 보정 · 석영 관찰창 셀 · Ar 상자 (이슬점 ≈185 K).
- **현미경**: 단면 광학 사진 (장치 미기재) — 균열 · 석출물 · Li 층 (`Fig. 5a` · `Fig. S8`).
- **특이사항**: 단면 셀은 가장자리 구속 · 적층압이 없다 — 저자도 단락 · 석출물 확산을 *"insufficient pressure at the cross-section"* 로 설명한다.

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나 — 실독) | 우리 활용 |
|---|---|---|
| 1a,b | (a) 적층 파우치 4 × 4 cm · 활성 3 cm² 점선 · 탭 둘 (b) 단면 광학 사진: SUS / Ag/C 10 µm / SE 100 µm / PE 70 µm / Al · 측정점 1 · 2 (빨간 원) 가 Ag/C 띠 위 | 층 두께 · 순서의 원문 그림 · 탐침이 10 µm 층 안의 ∼1 µm 점이라는 것 (§0 Q4) |
| 2a | 자르지 않은 셀 1 · 5 · 10 · 20 · 30 · 40 · 50 · 100 · 200 · 300 회 충방전 (0–20 mAh · 2.0–4.5 V) — 첫 충전은 ≈3.67 V 평탄 전에 figure-read ≈1.2 mAh 의 낮은 전압 구간 · 첫 방전 figure-read ≈15.0 mAh · 5 회부터 곡선은 처음부터 ≈3.7 V | ★ 도금 전 저장량의 대리 값 (§3-8 · Q2) · 본문 '16 mAh' 와 어긋남 (§10-⑨) |
| 2b | 300 회 유지율 (figure-read ≈71 %) · CE (81 · 95 · ≈100 %) | 셀 성능 맥락만 (물성 아님) |
| 2c | Raman: Ag/C 층 (빨강) · CB 분말 (검정) · SE 층 (초록 × 0.05) — D ≈1349 · G ≈1589 점선 · D ≈ G 높이 · 2600–3000 넓은 둔덕 · SE 426 cm⁻¹ PS₄³⁻ · Ag/C 스펙트럼에도 ≈420–440 둔덕 | ★ 탄소 모형 = 결함 많은 CB (§3-4 · 7-1 행) · 탐침 자리에 SE 가 섞인다 |
| 3 | operando 점 1 원 스펙트럼 (바탕 보정 없음 · 100–4000 cm⁻¹) — 충전 0.6–3.9 V · 방전 3.6–2.1 V · 형광 · D · G 소실 · 1087 · 1854 · 3648 초록 띠 | ★ 띠가 사라지는 구간 (3.0 V 충전 ~ 2.7 V 방전) 이 맞춤 신뢰도의 경계 (§10-②) |
| 4a | aspect ratio vs 전압 (점 1 · 2 · 충전 실선 · 방전 빈 표지) — 점 1 충전 최대 2.7 V 5.93 · 방전 2.1 V 5.53 · 점 2 충전 계열은 0.6–2.4 V 가 한 칸 왼쪽 (디지털 판독) | ⛔ 세기 지표라 모양 해석에 쓰지 않는다 (§3-8 ⑬ · §10-③) |
| 4b | R vs 전압 (충전 왼쪽 축 0.9–1.6 · 방전 오른쪽 축 0–5) — 점 1 방전 3.70 → 1.25 · 방전 점이 x = 2.00–3.43 V 에 찍힘 · 점 2 방전 0.98–1.83 (`Table S2` 1.35–6.65 와 다름) | R 의 오르내림은 방향 해석이 모호 (§10-④) · 그림–표 불일치 (§10-⑧) |
| 4c,d | D · G 위치 vs 전압 (점 1 · 점 2) — G 충전 3.3–3.9 V 에 ≈20–25 cm⁻¹ 아래로 · 방전 초기 ≈1540 · 2.1 V ≈1575 · D 는 반대 · (d) 방전 D 는 점 1 값과 거의 같다 | ★ 가장 튼튼한 신호 = G 의 하향 이동 (원 스펙트럼 꼭대기로도 보임) · 단 단락 뒤 값은 띠가 약하다 |
| 5a | 단면 사진 초기 · 3.9 V (단락 뒤) · 2.1 V 방전 — SE 의 Ag/C 쪽에 균열 화살표 · 금속광 석출물 1 (빨강) · 2 (노랑) | DEM: 구속 없는 면으로 Li 가 새어 SE 균열 · 단락 (§8 ⑤) |
| 5b | 석출물 1 · 2 와 3.9 V 점 1 · 2 의 Raman — 석출물은 D · G 없이 ≈1848 봉우리 · 낮은 파수 형광 · ≈420–480 · 800 둔덕 | ★ 1848 은 탄소 격자 신호가 아니다 (§10-⑦) |
| 6 | ex situ 대표 스펙트럼 (초기 · 15–100 % 충전 · 58 · 15 · 0 % 방전) — D · G 늘 보임 · 2700 · 3500 넓은 둔덕 · 3650 작은 봉우리 (초록) | 휴지 뒤 탄소는 Raman 으로 맨 탄소와 크게 안 다르다 (§0-1 ⑤) |
| 7a–c | ex situ 3 점 평균 AR · R · D · G 위치 vs SOC (오차 막대) — R 15 % 에서 오른 뒤 ≈1.1 평탄 · 방전 끝 1.52 · G 는 충전 중 **위로** | ★ operando 와 G 방향이 반대 (§10-⑤) · `Table S3` 평균과 어긋남 (§10-⑧) |
| 8 | 반응 모형: 초기 → 저 SOC (SUS \| Li \| Ag/C · Ag–Li 합금 점 · SE 로 응력 화살표) → 중 SOC (Li 층 두꺼워짐 · SE 작은 균열) → 고 SOC · 확대: CB 입자 = 동심 · 터보스트래틱 조각 · '국소 정렬 층 = 삽입' · '작용기 = 흡착' · 'Partial Li⁺' | ★ 7-1 카본블랙 행 = 결함 · 작용기 + 정렬 부분 (LiC₆ 끝) 두 자리 모형의 저자 그림 (§0 Q3) · 작용기는 측정 안 됨 |
| S1 | (a) operando 전위 주사 전류 (−5 – 20 mA) · 측정점 원 · ≈3.85 V 뒤 단락 스파이크 (b) 0–2.0 V 확대 (0–0.010 mA) · ≈0.68 V 작은 꼭지 | ★ 측정점마다 흐른 전하 (§3-8 ⑦) · 방전 꼭지 ≈3.3–3.4 V (본문 3.6 V 와 다름) |
| S2 | operando 점 2 원 스펙트럼 — 점 1 과 같은 꼴 · 3648 작은 봉우리가 0.9–2.7 V 에 또렷 | 두 점 재현성 (충전 쪽) |
| S3 | 점 1 200–1800 cm⁻¹ · 형광 구간 (주황) 200–700 · 충전 중 ≈250 cm⁻¹ 날카로운 봉우리 · 380–480 둔덕 · 1087 | 형광이 3.3–3.9 V 충전에서 가장 크다 |
| S4 | 바탕 보정 600–2100 cm⁻¹ (초기 · 2.4 · 3.9 V 충전 · 3.6 · 2.1 V 방전 · 점 1 · 2) — 'Appeared band' ≈1380–1470 · 'Appeared peak' ≈1060–1120 · ≈1800–1920 | ★ 셋째 띠가 있는데 2 대역으로 맞췄다 (§10-②) |
| S5 | 맞춤 예 (초기 · 3.9 V 충전 · 2.1 V 방전 · 점 1) — 2 점 직선 바탕 (≈900–930 · ≈1790–1800 cm⁻¹ figure-read) · 3.9 V 는 가파른 바탕 위 작은 D · G · 1850 봉우리는 바탕점 바로 옆 · D 꼭대기 · 골에서 맞춤이 체계적으로 어긋남 | 맞춤 품질 판단의 원본 |
| S6 | 정의 모식: aspect ratio = (H_D + H_G)/(W_D + W_G) · R = H_D/H_G | 지표 정의 (§6) |
| S7 | ex situ 충방전 (시간 축 0–80 h) — 충전 15–100 % (검정) · 방전 58 · 15 · 0 % (빨강 · 같은 시간 축에 겹쳐 그림) · 15 % 휴지 전압 출렁임 · 44 % 스파이크 · 100 % CC 구간 ≈7 h · 0 % 방전은 ≈1.4 h 에 2.0 V | §3-8 ⑧ 과 본문 '10 mAh' 의 어긋남 (§10-⑨) |
| S8 | ex situ 단면 사진 (초기 · 29 · 44 · 59 · 73 · 100 %) — Ag/C 와 SUS 사이 Li 층이 커짐 · 100 % 주석 "Deposited Li 50 µm" | ★ Li 가 쌓이는 곳 = Ag/C \| 집전체 사이 (§0-1) · 두께 검산 (§3-8 ⑨) |
| Table S1 | operando 점 1 맞춤 변수 (높이 · 위치 · 폭 · Lorentz 비 × D · G · 19 측정점) | §3-5 표의 원자료 · R · AR 재계산 |
| Table S2 | operando 점 2 맞춤 변수 (같은 꼴) | 방전 행이 `Fig. 4` 와 다르다 (§10-⑧) |
| Table S3 | ex situ '대표 3 개' 맞춤 변수 (SOC 10 개 × 3) | `Fig. 7` 평균과 맞지 않는다 · 본문이 함께 가리킨 Table S4 는 SI 에 없다 |

---

## 6. Post-processing ★

- **무엇**: 원 스펙트럼 (바탕 보정 없이 그림) → 600/700–1850/1950 cm⁻¹ 구간 **2 점 직선 바탕** (`Fig. S5` 의 'Baseline point') → **pseudo-Voigt 2 대역** (D · G · Lorentz 비 자유) 맞춤 → 높이 · 위치 · 폭 → **R = H_D/H_G** · **aspect ratio = (H_D + H_G)/(W_D + W_G)** (`Fig. S6`) · ex situ 는 10 점 중 **형광이 적은 3 점** 평균 (± 막대 · 정의 없음).  새 봉우리는 위치만 (세기 · 면적 없음).  전기화학: 셀 전류 · 전압 곡선만 (용량 분해 · 미분 용량 없음).
- **도구**: 맞춤 소프트웨어 [미기재] · 현미경 · 분광 장치는 §3-3.
- **수치화 · 기록 방식**: 표 S1–S3 에 맞춤 변수 전부 (재계산 가능 — 이 카드의 R · AR 은 거기서 다시 냈다) · 원 스펙트럼 수치는 '자료는 ESI 에' 라고 했지만 ESI 에는 그림 · 표만 있다 [카드 해석] · 세기는 *"lack of peaks for y-axis correction and normalization"* 로 정규화 못 함 (p.27964).
- **우리가 가져올 꼴 · 피할 꼴**: ① 높이비 (R) 를 쓸 때 **맞춤 대역 수 · 바탕 처리 · 높이 / 면적 중 어느 것인지 · 들뜸 파장**을 숫자 옆에 적는다 (같은 스펙트럼에서 원 높이비 ≈1.0 대 맞춤 ≈1.25) ② 정규화 안 된 높이로 '모양' 지표를 만들지 않는다 (§3-8 ⑬) ③ 띠가 바탕에 묻힌 스펙트럼의 맞춤 위치는 따로 표시한다 (방전 3.6–2.7 V) ④ 운전 중 Raman 을 받을 때는 **레이저 세기를 두 단계 이상** · **OCV 에서 같은 시간 쬔 대조**를 요구한다.

---

## 7. 우리 DFT 대비 (comp1 / modelc · DEM 점착 트랙)  →  `our_dft_baseline.md`

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| A 이온전도 | LPSCl *"∼2 mS cm⁻¹ at room temperature"* (자료 없음) | MLIP-MD (UMA) σ · Ea — 절대값 비인용 (`our_dft_baseline.md` A 행) | n/a — 측정 없음 · 방법 다름 |
| B 산화 · C 기계 · D 전자구조 | 없음 | comp1 · modelc 기준값 | n/a |
| SE Raman | PS₄³⁻ 426 cm⁻¹ (SE 층) | Raman 계산 없음 | n/a — 식별용 |
| E 환원 · 음극 계면 | 서론: 무음극에서 *"SE does not generate solid electrolyte interphase"* · 석출물이 LPSCl 분해 산물이 아니라는 근거는 Li₂S 383 cm⁻¹ 부재뿐 | grand-potential 환원 쪽 경계 (`our_dft_baseline.md` 환원 행 · ⚠ 라벨 주의 `HZ-esw-reduction-limit-label`) — Li 금속 전위 (0 V) 는 그 경계보다 한참 아래 → Li · 리튬화 CB 와 닿는 LPSCl 은 **열역학적으로 환원된다** · [`baer2026_…`] · `chaney2024_…` 의 MLIP-MD 도 Li \| LPSCl 반응 [다른 카드] | 🔴 서론 주장이 틀렸다 (§10-⑪) · 이 논문의 자료는 SEI 를 묻지 않았다 — 반증도 아니다 |
| ★ 점착 트랙 — Li \| C 쌍 | CB 가 충전 중 Raman 으로 바뀐다 (삽입 · 흡착 해석) · Li 금속은 Ag/C \| SUS 사이 | W_ad 보고서 §2 의 탄소 쌍은 C–C · Ag–C · LPSCl \| 흑연 (맨 흑연 기저면) · **Li \| C (리튬화) 미계산** — 값은 그 보고서와 `db/properties/adhesion.json` 에서만 | 🟡 **계산 대상 목록만 이식**: Li \| 맨 결함 탄소 · Li \| 리튬화 결함 탄소 (LiₓC · x 미정) 두 끝 · LiC₆ 기저면은 이상화된 끝 · ⛔ G 이동 · R 을 Li 양 · stage 로 옮기지 않는다 |
| 점착 트랙 — 집전체 | **SUS 10 µm** | 7-1 표 집전체 행 = Cu(111) 만 | 🟡 SUS 면 (산화막 → Li 와 반응 뒤) 을 후보로 [카드 해석] |
| DEM | WIP 490 MPa (제조) · ≈2 MPa (운전) · Ag/C 10 µm · Li 층 (ex situ 100 %) ≈50 µm · 단면 ±5 µm | DEM 압력 단계 · 층 두께 입력 | 🟡 압력 단계 · 두께 비의 실험 예 (조건 붙여서만) · ⛔ 단면 (구속 없음) 의 Li 두께를 셀 안 두께로 옮기지 않는다 |

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

- ① **7-1 표 카본블랙 행의 '같이 볼 것' 칸에 '충전 중 리튬화된 결함 탄소' 를 더한다** — 이 논문은 Ag/C 층의 비정질 CB 도 충전 중 Raman 이 가역으로 바뀐다는 것을 보였다 (정성).  Li \| C 의 W 는 **맨 결함 탄소 ↔ 리튬화 결함 탄소** 두 끝을 범위로 낸다 ([`metzler2025_…`] digest 의 '기저면 ↔ 결함 면 범위' 제안과 같은 결) [다른 카드].  LiC₆ 기저면은 흑연 행의 끝 상태이고 카본블랙에서는 정렬된 일부의 이상화된 끝이다.
- ② **8-3 문장의 'Li\|C (리튬화된 탄소 · LiC₆)' 를 'Li\|C (리튬화된 탄소 — 흑연이면 LiC₆ · 카본블랙은 Li 양 미정)' 꼴로** — 이 논문은 '리튬화' 의 정성 근거는 되지만 LiC₆ 의 근거는 아니다.
- ③ **집전체 SUS 행** — 이 셀 · [우리 그룹] Ag–C 층 (`kang2026_…`) 은 SUS 박 위에서 만든다 [다른 카드].  Cu(111) 만으로는 이 계열의 Li \| 집전체 쌍을 못 덮는다.
- ④ **탄소가 받는 Li 는 충전량의 ≲5–10 %** (§3-8 ④–⑥) — Li 금속 층이 주연이고, 리튬화 탄소는 계면의 **막 조건**이다.  W 계산에서는 탄소 쪽 표면 상태 하나 (맨 / 리튬화) 를 정하는 문제이지 탄소 덩어리의 부피 변화 문제가 아니다.  DEM 에서도 Ag/C 층 (10 µm) 보다 Li 층 (수십 µm) 의 두께 변화가 지배한다 [카드 해석].
- ⑤ **DEM 경계조건 — 구속 없는 면** — 단면을 연 셀은 셋 다 그 면으로 단락됐고, SE 안 금속광 석출물 · 균열이 Ag/C 가까이에 생겼다 (`Fig. 5a`).  적층압이 없는 자유면이 생기면 Li 가 그리로 새는 꼴 — DEM 에서 옆면 · 모서리 경계를 자유면으로 두면 같은 인공물이 생길 수 있다 [카드 해석].
- ⑥ **우리 쪽에서 탄소 Raman 을 받을 때 요구할 사양** (7-1 행을 정하는 입력): 들뜸 파장 · 출력 밀도 · 맞춤 대역 수 (4–5 대역 [일반 지식] · 저자도 인용한 Sadezky 2005) · 높이 / 면적 비 구분 · 바탕 처리 · 같은 조건의 기준 탄소 (HOPG · 흑연 · 이 CB 분말) · 가능하면 XRD d₀₀₂ · L_a 와 XPS O/N.  이 논문 하나로는 이 CB 가 Ferrari–Robertson 의 어느 단계인지도 안 정해진다 (§10-④).

---

## 9. 인용 가능 문장 (deck / paper 용 — 조건을 떼지 않는다)

- "In an anode-free Li₆PS₅Cl cell with a 10 µm Ag/carbon-black interlayer, operando Raman spectroscopy on a cut cross-section showed that the carbon-black G band shifted down by about 20–25 cm⁻¹ during charge (3.3–3.9 V) and largely recovered after discharge to 2.1 V; the authors attributed this to partial Li insertion into the disordered carbon, but the amount of Li in the carbon was not quantified (*J. Mater. Chem. A*, 13, 27960 (2025))."
- "After 5 h of relaxation at each state of charge, the D/G-band changes were small, and plated Li was observed between the Ag/C layer and the stainless-steel current collector (*J. Mater. Chem. A*, 13, 27960 (2025))."
- (보고서용 한국어) *카본블랙과 Ag 나노입자로 만든 층도 충전 중 Raman 의 D · G 띠가 바뀌었다가 방전 뒤 대부분 돌아왔다 — 운전 중 Li 금속이 닿는 탄소는 맨 탄소가 아니라 Li 를 받은 탄소로 본다. 그 탄소에 든 Li 의 양 (LiC₆ 인지) 은 정해지지 않았다 (J. Mater. Chem. A, 13, 27960 (2025)).*
- ⛔ 쓰지 않는 문장: 'CB 가 LiC₆ 가 된다' · '1854 cm⁻¹ 은 Ag–Li 합금 신호' · '무음극 황화물 셀에는 SEI 가 없다' · 'aspect ratio 가 커졌으니 탄소 질서가 올랐다' · 'R 이 1.04 로 떨어졌으니 결함이 줄었다'.

---

## 10. 주의 / 한계 · 비판 ★ (over-claim 방지)

- ① **가장 큰 변화는 단락 뒤 · 구속 없는 단면이다.**  operando 셀은 셋 다 ≈3.85–3.9 V 에서 단면으로 단락됐다 (`Fig. S1a` 스파이크 ≈15.5 mA figure-read · n = 3).  G ≈1540–1548 · R 2.3–3.7 (점 1) 같은 극단값은 단락 뒤 방전 3.6–2.7 V 스펙트럼이다.  저자는 단락 뒤 OCV ≈3.7 V 와 방전 꼭지로 *"the effect of the short-circuit was considerably small"* 라고 하지만 단락 전하 · 국소 전위를 따지지 않았다.  충전 쪽 G 하향 (3.3–3.6 V · 1566 → 1559) 은 단락 전이라 이쪽이 더 튼튼하다.
- ② **2 대역 맞춤 + 셋째 띠.**  `Fig. S4` 에 D–G 사이 새 띠 (≈1380–1470 cm⁻¹) 가 3.9 V 충전 · 3.6 V 방전에서 또렷한데 맞춤은 D · G 둘뿐이다.  빠진 띠가 D 중심을 위로, G 중심을 아래로 끌 수 있다 — 방전 3.6–3.0 V 의 'D 1380 · G 1540' 은 맞춤 인공물과 못 가른다 (G 높이 9–52 a.u. · D Lorentz 비 0.81–1 로 튐).  다만 3.9 V 충전 점 1 의 원 스펙트럼 G 꼭대기도 figure-read ≈1555 라 **충전 쪽 G 하향 자체는 실제**다.  `Fig. S5` 에서는 초기 스펙트럼부터 D 꼭대기 · D–G 골에서 맞춤이 체계적으로 어긋난다.
- ③ **'aspect ratio' 는 모양이 아니라 세기다.**  정의 (ΣH/ΣW) 의 H 가 정규화 안 된 높이인데 (저자 스스로 *"lack of peaks for y-axis correction and normalization"*), 폭 합은 늘 ≈180–240 cm⁻¹ 로 비슷하다.  그래서 AR 은 신호 세기를 따라간다 — 같은 물질 초기값이 점 1 3.04 · 점 2 1.81 이다 (§3-8 ⑬).  AR 의 최대 · 최소를 '모양 변화' 로 읽지 않는다 (초점 · 형광 · 금속 덮임이 다 바꾼다).
- ④ **R 의 오르내림은 방향이 모호하다.**  SI 는 'R 은 L_a 가 작을수록 커진다' (Tuinstra–Koenig 꼴) 만 쓰는데, 저자가 인용한 Ferrari–Robertson (ref 43) 의 무질서 탄소 단계 (L_a ≲ 2 nm) 에서는 R 이 L_a² 에 비례해 반대로 간다 [일반 지식].  이 CB (G 폭 ≈66 cm⁻¹ · D ≈ G · 2D 없음) 가 어느 단계인지 정하지 않았으므로 'R 이 줄었다 = 질서 ↑ / 결함 ↓' 로 못 바꾼다.  게다가 방전 R 의 큰 값은 G 높이가 바닥으로 간 데서 온다 (분모 효과).
- ⑤ **흑연 Li-GIC 와 '비슷한 경향' 은 확인이 필요하다.**  흑연의 초기 (묽은) 단계는 G 가 위쪽 경계층 띠 (≈1600 cm⁻¹ · E₂g(b)) 로 갈라지는 쪽이고 stage 1 에서는 띠가 약해지며 넓어진다 [일반 지식 · refs 48–51 원문 미확인].  이 논문의 operando 는 G 가 **아래로** (−20–40 cm⁻¹), ex situ 는 **위로** (+5–9 cm⁻¹) 갔다 — 방향이 둘로 갈렸는데 같은 '삽입' 으로 묶었다.  아래로 가는 쪽은 전자 도핑 · 격자 팽창 · 가열 · 변형 · 맞춤 인공물 모두와 같은 방향이다.
- ⑥ **레이저 가열 · 광화학 점검이 없다.**  3.2 mW 를 ∼1 µm 에 · 스펙트럼당 240 s · 같은 자리 19 장 (≈76 min) [카드 산술 §3-8 ⑪–⑫].  금속 Li · 합금이 생기면 흡수가 커져 국소 온도가 오를 수 있다.  G 하향은 가열과 같은 방향이다 — 크기 (20–40 cm⁻¹) 를 가열만으로 설명하기는 어렵다고 보지만 [일반 지식], 세기를 바꾼 대조가 없어 몫을 못 가른다.
- ⑦ **새 봉우리 배정.**  금속 · 합금은 Raman 활성 진동이 없다 (저자도 *"metals and alloys hardly exhibit Raman scattering"*).  1087 · 1854 · 3648 cm⁻¹ 의 날카로운 봉우리는 분자 · 이온성 화학종의 진동이라야 한다.  위치가 **Li₂CO₃ (≈1090) · 아세틸라이드 Li₂C₂ (C≡C ≈1850–1870) · LiOH (O–H ≈3660–3680)** 와 가깝다 [일반 지식 · 기억값 · 원전 미확인] → 드러난 단면의 Li 가 상자 안 미량 CO₂ · H₂O · O₂ (또는 결합제 · 용매 잔여) 와 반응한 산물일 수 있다.  특히 1848 은 **D · G 가 없는 석출물에서 가장 세다** (`Fig. 5b`) — 탄소 격자 신호가 아니다.  저자의 'Ag–Li 합금과 관련' 은 근거가 없고, 후보 배정은 이 카드의 가설이다 (기준 시료 대조 필요).
- ⑧ **그림–표 어긋남 (디지털 판독 · 점 1 충전값으로 축을 맞추면 0.2–0.9 px 안에서 표와 일치하는 축으로 점 2 를 읽었다).**
  - `Fig. 4a,b` 점 2 충전: 0.6–2.4 V 값이 **한 칸 (0.3 V) 왼쪽**에 찍혔다 — x ≈0.30 V 에 0.6 V 값 (R 1.10 · AR 1.58) · 0.6 V 자리에 0.9 V 값 … 2.1 V 자리에 2.4 V 값 · 2.4 V 에 같은 값 한 번 더.  `Fig. 4d` (위치) 는 표와 맞게 찍혔다.
  - `Fig. 4b` 방전 점 (두 점 다): x = 2.00 · 2.29 · 2.57 · 2.86 · 3.14 · 3.43 V 에 찍혔다 (2.1–3.6 V 가 아니다) · 점 1 값 자체는 `Table S1` 과 맞다.
  - **`Fig. 4a,b,d` 점 2 방전 계열 ≠ `Table S2`**: R 그림 0.98–1.83 대 표 1.35–**6.65** · D 그림 ≈1363–1380 (시간 순으로 매끈하게 감소) 대 표 1357–1386 (3.0 V 에 1361 로 꺼짐) · 그림 D 는 **점 1 표값과 ≤1.7 cm⁻¹** · G 그림 ≈1546–1572 대 표 1540–1576.  어느 쪽이 맞는지 원문으로 못 가린다 — 점 2 방전으로 '두 점 재현' 을 말하지 않는다.
  - `Fig. 7` 평균 ≠ `Table S3` 세 스펙트럼 평균: D 최대 ≈5 cm⁻¹ (100 %: 그림 1352.5 대 표 1347.7 · 59 %: 1353.9 대 1358.7) · AR 29 %: 그림 1.43 대 표 1.02 · R 은 ±0.07 안.  본문이 함께 가리킨 **`Table S4` 는 SI 에 없다** — 어느 세 점을 평균했는지 확인 불가.
- ⑨ **본문 서술 대 그림.**  첫 방전 *"about 16 mA h"* 대 figure-read ≈15.0 (CE 81 % × 18.4 와도 맞음) · 단락 뒤 방전 꼭지 *"around 3.6 V"* 대 figure-read ≈3.3–3.4 V · aspect ratio 최대 *"2.1–2.4 V"* 대 표 충전 최대 2.7 V · '방전 중 D 위치 계속 증가' 대 시간 순 감소 (1380 → 1362) · ex situ 'R 충전 중 계속 감소' 대 15 % 에서 오름 (1.17 → 1.34–1.38) 뒤 평탄 · ex situ 'SOC 가 높을수록 형광' 대 그림에서 15–44 % 의 바탕 기울기가 더 큼 (대표 1 장) · ex situ CC 용량 *"approximately 10 mA h"* 대 `Fig. S7` 의 CC 구간으로 읽은 충전 ≈13.5 · 방전 ≈4.5 mAh (0.5 mA 가정 · §3-8 ⑧) · operando *"from 4.0 to 2.1 V"* 대 실제 ≈0.45 V 에서 시작.
- ⑩ **인용 · 표기 오류.**  ref 27 (Park · Jung · Sohn, *Electrochem. Solid-State Lett.* 2009) 은 '같은 셀 구성 무음극 전고체의 TEM · 전자회절 Ag–Li 합금' 의 출처가 될 수 없다 (2009 · 그런 셀 이전) — ref 29 (Lee 2020) 를 뜻한 듯 [카드 해석] · ref 33 의 저널 'Nature' 는 DOI (10.1038/s41467-…) 로 보면 *Nat. Commun.* · SI S-8 'Fig. S5 에서 정의' 는 `Fig. S6` · `Fig. S1` 캡션에 (b) 표지가 빠졌다 · SI 제목은 'Li Battery' (본문은 'Li-ion batteries').
- ⑪ **'무음극이면 SE 가 SEI 를 만들지 않는다' (서론) 는 틀렸다.**  LPSCl 은 Li 금속 전위에서 열역학적으로 환원된다 (§7 E 행 · [`baer2026_…`] · `chaney2024_…`) [다른 카드].  이 논문의 '석출물은 SE 분해 산물이 아니다' 근거도 Li₂S 383 cm⁻¹ 부재 하나다 — Li₃P · LiCl 은 Raman 으로 잘 안 보이거나 비활성이라 [일반 지식] 그 부재로 SEI 없음을 말할 수 없다.
- ⑫ **통계 · 선택.**  operando 그림은 셀 1 개 · 점 2 개 (n = 3 은 단락이 났다는 말에만) · ex situ 는 10 점 중 **형광이 적은 3 점을 골랐다** (선택 편향 — 형광이 큰 자리가 Li · 합금이 가장 많은 자리일 수 있다) · 오차 막대 정의 없음.
- ⑬ **셀 전압 축만 있다** (기준 전극 없음).  흑연 Li-GIC 단계는 Li/Li⁺ 기준 음극 전위로 정의되는데 이 논문은 음극 전위를 모른다.  3.3 V 셀 전압의 음극 전위는 양극 전위에 따라 달라진다.
- ⑭ **온도 · 속도가 다르다.**  operando = 실온 · 0.11 mV s⁻¹ (측정점 사이 ≈45 min) · 사이클 · ex situ 충전 = 318 K · 정전류 — 저자 스스로 '실온 · 빠른 주사' 가 과포화를 만들었을 수 있다고 한다.  같은 셀 상태를 두 방법으로 본 비교가 아니다.
- ⑮ **침투 깊이 · 국소성.**  532 nm 빛은 흑연질 탄소에 수십 nm 만 들어간다 [일반 지식] — CB 1 차 입자 (38 nm) 한두 겹 · 그것도 **잘라서 드러난 면**이다.  층 속 (Li 금속과 맞닿은 Ag/C 아랫면) 의 탄소를 직접 본 것이 아니다.  점 크기 ∼1 µm 에 10 µm 층 · 점 2 개 → 층 전체의 대표성은 모른다.

---

## 11. 용어 미니 사전

- **D 띠 · G 띠 · 2D** — G (≈1580 cm⁻¹) = 흑연 면 안 C–C 진동 (E₂g) · D (≈1350) = 결함 · 가장자리가 있어야 켜지는 띠 (A₁g 호흡 모드) · 2D (≈2700) = D 의 2 차 (층 쌓임 정보).  결함 탄소의 부띠 D2 (≈1620) · D3 (≈1500 · 비정질) · D4 (≈1200) 는 SI 해설 (S-7) 그대로.
- **R (= I_D/I_G)** — 이 논문은 맞춤 **높이**비.  면적비 · 원 높이비와 값이 다르다.  들뜸 파장에 따라 달라진다.
- **Tuinstra–Koenig · Ferrari–Robertson** — 나노결정 흑연 (L_a 큼) 에서는 R ∝ 1/L_a · 더 무질서한 탄소 (L_a ≲ 2 nm) 에서는 R ∝ L_a² (Ferrari–Robertson 세 단계 모형 · ref 43) [일반 지식].  어느 단계인지 정해야 R 의 오르내림을 읽을 수 있다.
- **pseudo-Voigt · Lorentz 비** — 가우스와 로렌츠를 섞은 띠 꼴 · 섞는 비율 (0 = 가우스 · 1 = 로렌츠).
- **aspect ratio (이 논문 정의)** — (H_D + H_G)/(W_D + W_G).  정규화 안 된 높이를 쓰므로 세기 지표다 (§10-③).
- **형광 바탕** — Raman 위에 깔리는 넓은 발광 · 이 논문은 '금속 같은 상태' 로 해석한다.
- **Li-GIC · stage** — 흑연 층간 Li 화합물 · stage n = Li 층 사이에 흑연 n 층 (stage 1 = LiC₆ · stage 2 = LiC₁₂ · 묽은 stage 4 ≈ LiC₃₆).
- **operando · ex situ** — 운전 중 그 자리에서 재기 · 멈추고 (여기서는 5 h 휴지) 재기.
- **AF-ASSB** — anode-free all-solid-state battery (무음극 전고체 전지) · 첫 충전에 집전체 위에 Li 를 만든다.
- **WIP** — warm isostatic pressing (가온 정수압 성형 · 여기서 490 MPa · 353 K).
- **CCCV · SOC · C/4** — 정전류–정전압 충전 · 충전 상태 · 4 시간에 다 채우는 전류.
- **카본블랙 (CB) · 터보스트래틱** — 수십 nm 구형 1 차 입자가 사슬로 엉긴 탄소 · 흑연 조각이 어긋나게 겹친 (방위가 어긋난) 층 구조.

---

## 12. 다음에 먹일 논문 (이 논문 참고문헌 + 최근 2 년 발견 검색 · 최근 것 먼저 · 2026-11-24 litdb · 목록 대조)

> 대조: `litdb/papers` 파일 이름 + digest 본문 grep · `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md` grep.  최근 편은 Crossref 주제어 검색 (제목 없이 · 2025 이후) 6 번 + 저자 검색 1 번 + DOI 확인 5 번으로 찾았다 (제목 · 저널 · 권 · 쪽 · DOI 는 Crossref 메타 · 본문은 안 엶).

| # | 문헌 | 왜 (우리 축) | litdb | 목록 |
|---|---|---|---|---|
| 1 | Liu, Lu, Clemens · *Electrochim. Acta* 574, 149375 (2026) — "Effect of carbon interlayer preconditioning on in-situ plated lithium metal stability in anode-free solid-state batteries" · DOI 10.1016/j.electacta.2026.149375 | 탄소 층을 미리 '조건화' (리튬화?) 하면 석출 Li 가 어떻게 되나 — Li \| 맨 탄소 대 Li \| 리튬화 탄소 (§8 ①) 의 실험 짝 (제목만 확인) | 없음 | 없음 |
| 2 | Lee, Choi, Lee · *J. Power Sources* 670, 239539 (2026) — "Unveiling the high lithiophilicity of lithiated hard carbon for lithium metal battery anodes" · DOI 10.1016/j.jpowsour.2026.239539 | '리튬화된 무질서 탄소는 친Li' — 7-1 카본블랙 행의 리튬화 끝 모형에 바로 걸린다 (계 · 방법은 원문 확인) | 없음 | 없음 |
| 3 | Hiraoka, Sato, Seki, Yamamoto · *ACS Appl. Energy Mater.* 9, 818 (2026) — "Multimodal Analysis of Short- and Medium-Term Degradation in Multilayered All-Solid-State Batteries" · DOI 10.1021/acsaem.5c03001 | 같은 1저자 · 교신의 후속 (다층 ASSB 열화 다중 분석) — Raman 방법 · 단면 셀 문제를 고쳤는지 볼 곳 (제목만) | 없음 | 없음 |
| 4 | Ko, Kim, Park, Kim, Kim · *ACS Nano* 19, 16957 (2025) — "Correlation between the Microstructure of the Carbon Protective Layer and Cycle Performance of Anode-Free All-Solid-State Lithium-Ion Batteries" · DOI 10.1021/acsnano.5c02926 | **탄소 미세구조 ↔ 무음극 전고체 성능** — '어느 탄소가 어느 모형' (7-1) 의 실험 축을 정면으로 | 없음 | 없음 |
| 5 | Yuan, Guo, Gurgan, Siddique, Li, Jang, Noh, Kim · *Carbon* 238, 120214 (2025) — "Raman spectroscopy analysis of disordered and amorphous carbon materials: A review of empirical correlations" · DOI 10.1016/j.carbon.2025.120214 | I_D/I_G · 폭 → L_a · sp³ · 단계 판정의 경험식 정리 — §8 ⑥ (Raman 으로 7-1 행 고르기) 의 방법 원전 | 없음 | 없음 |
| 6 | Xie, Diallo, Kim, Tu, Ceder · *Adv. Energy Mater.* 14, 2302960 (2024) — "The microscopic mechanism of lithiation and delithiation in the Ag/C buffer layer for anode-free solid-state batteries" · DOI 10.1002/aenm.202302960 | Ag/C 층 리튬화 미시 기전 — 이 논문의 '삽입 + 합금' 해석을 계산 · 분광으로 받칠 짝 | 없음 | **목록에 있음** (표 2 #3) |
| 7 | Suzuki, Yashiro, Fujiki, Omoda, Shiratsuchi, Watanabe, Aihara · *Adv. Energy Sustain. Res.* 2, 2100066 (2021) — "Highly Cyclable All-Solid-State Battery with Deposition-Type Lithium Metal Anode Based on Thin Carbon Black Layer" · DOI 10.1002/aesr.202100066 (ref 30) | 이 논문이 시험한 **'과포화 CB → Li 석출' 가설의 원전** · 같은 교신 · 카본블랙 층 | 없음 (`sandoval2025_…` 에 인용만) | 없음 |
| 8 | Lee Y.-G. 외 · *Nat. Energy* 5, 299 (2020) — "High-energy long-cycling all-solid-state lithium metal batteries enabled by silver–carbon composite anodes" · DOI 10.1038/s41560-020-0575-z (ref 29) | Ag–C 층 원조 · 이 셀 꼴의 출처 · Ag–Li 합금 TEM (ref 27 오기 확인처 · §10-⑩) | 없음 | **목록에 있음** (표 2 #1 · ⚠ 목록의 'Ag : 카본블랙 3 : 1' 은 이 논문 배합 (CB 12 g : Ag 4 g = Ag : CB 1 : 3) · `kang2026_…` (1 : 3) 과 반대 — 원전 확인 필요) |

다음 순번: Chacón-Torres, Wirtz, Pichler *ACS Nano* 7, 9249 (2013) (ref 48 · Li-GIC Raman · §10-⑤ 확인처) · Zhou, Doerrer, Kasemchainan, Bruce, Pasta, Hardwick *Batter. Supercaps* 3, 647 (2020) (ref 52 · Li₂S 383 cm⁻¹ · Li \| LPSCl Raman) · Sadezky 외 *Carbon* 43, 1731 (2005) (SI S3 · 5 대역 맞춤) · Mukofukasawa 외 *RSC Adv.* 15, 24117 (2025) (operando Raman · Li 석출 · 미세전극 — 새 봉우리 배정 대조) · Yuan 외 *Energy Storage Mater.* 76, 104110 (2025) (황화물 ASSB operando Raman 리뷰) · Hiraoka 외 *APL Energy* 3, 021502 (2025) (같은 1저자 Raman 리뷰) · Oh 외 *Batteries & Supercaps* 9, e70514 (2026) (저적층압 황화물 음극 계면 · DEM 압력) · Park 외 *Inorg. Chem. Front.* 12, 5449 (2025) (LPSCl \| Li 온도별 계면 반응).
