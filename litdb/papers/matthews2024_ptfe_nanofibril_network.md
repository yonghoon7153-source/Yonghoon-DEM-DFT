# 무용매(dry-process) NMC 전극의 PTFE 나노-피브릴 binder 망 — 계층 microstructure 와 형성기전을 고해상 SEM 으로 풀다 — Matthews (Front. Energy Res. 2024)

> slug `matthews2024_ptfe_nanofibril_network` · DOI `10.3389/fenrg.2023.1336344` · type `exp (SEM/EDX + 전기화학 + EIS; 시뮬레이션 0)` · PDF `18480bfb-fenrg111336344.pdf` · digested `2026-09-04` · status ✅

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 중요한가

건식(무용매) NMC622 + **1 wt% PTFE** 전극의 바인더가 **슬러리 PVDF 의 "이끼(moss)형" CBD 와
근본적으로 다른 계층(hierarchical) 피브릴 망**이라는 것을, 3 kV FEG-SEM 으로 **primary(Ø 수 µm ·
L 수백 µm) → secondary → "10s nm 이하"** 까지 계단을 따라 내려가며 보여주고, 그 계단이 만들어지는
**기전(NMC 표면 거칠기에 PTFE 결정자가 맞물림 → 전단으로 풀려나옴 unwinding → 이미 뽑힌 피브릴에서
다시 뽑힘)** 을 제시한 논문.

**우리에게 이 카드의 값어치는 딱 하나다 — `scripts/additives.py:38` 의
`PTFE_D, PTFE_L = 0.25, 40.0` 주석이 인용하는 두 출처 중 하나가 이 논문인데, 그 값이
이 논문에서 나오는지 한 번도 확인된 적이 없었다.**  판정은 아래 §3 · §13.1 에 있고 요약하면:

| 우리 상수 | 이 논문이 주는가 | 판정 |
|---|---|---|
| `branch to 10s nm` (주석) | ✅ **문자 그대로** ("down to diameters of 10s nm or below", 초록) | **앵커 확정** |
| `branch_frac` · `branch_n` (계층 분지) | ✅ Fig 4C + §3.1 (primary→secondary→"finer and finer") | **앵커 확정 (정성)** |
| `vol_conserve` (등체적 드로잉 d ∝ √(V/L)) | ✅ 기전이 crystallite **unwinding** = 등체적 인발 | **방향 앵커** |
| `--ptfe-am-bind` (AM 표면 핵생성) | ✅ **이 논문의 핵심 기전 자체** (NMC 거칠기 = anchor point) | **방향 앵커 (신규 획득)** |
| **`PTFE_D = 0.25 µm`** | ⛔ **없다** — 분포도·히스토그램·n·평균±sd **전무** | **미앵커** (구간 안이지만 값은 이 논문 것이 아님) → ★ **자매 논문 Lee 2025 의 rope Ø 0.248 µm 가 앵커한다**(§16) |
| **`PTFE_L = 40 µm`** | ⛔ **없다** — 논문은 primary 를 **"100s µm"**, Fig 2A 를 **">50 µm"** 라 함 | **미앵커 · 우리 값이 그 하한보다 짧다** (Lee 는 반대로 최장 14.3 µm — §16) |
| `AR ≈ 160` | 🔶 **간접 지지** — 논문 자신의 (수 µm, 100s µm) 쌍이 AR ≈ 33–500 | **계층 의존** — Lee 실측은 AR ≈ 27 (§16) |
| `PTFE_FIBRIL` 전단 의존 크기(0.45) | ⛔ 전단·온도 스윕 **미보고** ("in-house optimisation" 이라고만) | **§F1 유지** |

> ★★★ **한 줄 종합 (자매 카드 `lee2025_dual_fibrous_ptfe_dry_electrode` 와 겹친 결과 — §16):
> 우리 `(0.25, 40)` 은 키메라다.  지름은 Lee 의 가는 계층에서, 길이·AR 은 Matthews 의 굵은 계층에서
> 왔고, 두 논문의 절대 스케일은 8–10배 다르다.  한 쌍의 (Ø, L) 로는 원리적으로 둘 다 못 맞춘다.**

⚠ **소재계 게이트 — 액체계 LIB (1 M LiPF₆ EC/EMC 3:7 + 2 wt% VC), 황화물 ASSB 아님.**
이온상이 **반전**돼 있다(공극이 이온을 나른다).  ⇒ **형태·기전·공정은 전이, 성능 절대값은 전이 금지.**

---

## 0. 서지 정보 (SI 참고문헌 `[S7]` 용 — 확인한 그대로)

- **저자**: **G. A. B. Matthews**¹²\*, **S. Wheeler**¹², **J. Ramírez-González**¹², **P. S. Grant**¹²
  (인용 블록 표기: *Matthews GAB, Wheeler S, Ramírez-González J and Grant PS (2024)*)
- **소속**: ¹ Department of Materials, University of Oxford, Oxford, United Kingdom ·
  ² The Faraday Institution, Quad One, Harwell Science and Innovation Campus, Didcot, United Kingdom
- **교신**: G. A. B. Matthews (guillaume.matthews@materials.ox.ac.uk)
- **제목**: *Solvent-free NMC electrodes for Li-ion batteries: unravelling the microstructure and
  formation of the PTFE nano-fibril network*
- **저널 / 권 / 논문번호 / 연도**: **Frontiers in Energy Research, 11, 1336344 (2024)**
  · Frontiers 는 **페이지가 아니라 논문번호(article number)** 를 쓴다 — `11:1336344`
- **DOI**: `10.3389/fenrg.2023.1336344`  ⚠ DOI 문자열의 `2023` 은 **채택연도**이고 **발행연도는 2024**
  (Frontiers 관행).  인용에는 **2024** 를 쓰되 DOI 는 그대로 `…2023.1336344`.
- **유형 / 라이선스**: Original Research · **Open Access, CC BY**
- **일정**: Received 10 Nov 2023 · Accepted 13 Dec 2023 · **Published 11 January 2024**
- **편집/심사**: Editor Mona Faraji Niri (Warwick) · Reviewers Carl David Reynolds (Birmingham),
  Samuel Cooper (Imperial College London)
- **지원**: The Faraday Institution, *"Nextrode — next-generation electrodes"* (**FIRG015**, **FIRG066**)
- **분량 (★ 실측)**: **본문 PDF 10 쪽** (저널 자체 풋터 01–10) — 뷰어가 말한 254 쪽은 **오독**.
  Figure 1–8 · Table 1 · 참고문헌 ~2.5 쪽.  **SI(Table S1, S2, Figure S1) 는 이 파일에 없다**
  (온라인 Supplementary Material 별도).

**권장 인용 문자열 (`[S7]`)**
> G. A. B. Matthews, S. Wheeler, J. Ramírez-González, P. S. Grant,
> *Solvent-free NMC electrodes for Li-ion batteries: unravelling the microstructure and formation of
> the PTFE nano-fibril network*, **Front. Energy Res. 11, 1336344 (2024)**.
> DOI: 10.3389/fenrg.2023.1336344

---

## 1. 약어 · 핵심개념 (우리 맥락으로 번역)

| 논문 용어 | 뜻 | 우리 쪽 대응 |
|---|---|---|
| **solvent-free / dry-processed** | 용매(NMP) 없이 건식 혼합 + 전단 + 열압연 | 우리 SBE/DBE 침대의 공정 축 (Thinky/ballmill/handmix) |
| **PTFE fibrillation** | PTFE 분말이 압축+전단으로 **풀려 실이 되는** 것 | `additives.seed_fibres(vol_conserve=True)` = 등체적 인발 |
| **primary / secondary fibril** | 1차(굵고 김) / 그로부터 다시 뽑힌 2차(가늚) | `branch_frac`, `branch_n`, `branch_vol`, `branch_len` |
| **crystallite unwinding** | PTFE 입자 표면 결정자가 맞물렸다 풀리며 실이 됨 (Ariawan 2002) | 우리에게 **없는 기전** — 우리는 씨앗을 사후에 뿌린다 |
| **anchor point** | 피브릴이 NMC 표면 거칠기에 물린 자리 | `--ptfe-am-bind` (AM 표면 핵생성 분율, 기본 0.5) |
| **CBD (carbon binder domain)** | PVDF + C65 가 뭉친 이끼형 덩어리 (슬러리 전용) | 건식에는 **없다** — 그 자리를 CNF + PTFE 망이 대신 |
| **CNF (carbon nanofibre)** | 도전재.  Pyrograf, **Ø 150–200 nm**, L 수십 µm | 우리 `VGCF_D = 0.15 µm` 와 **같은 자릿수** |
| **obscuration / pore blockage** | 바인더가 AM 표면을 덮음 / 기공을 막음 | 우리 coverage · pore-τ 축 |
| **R_cont / R_CT / R_ion** | 집전체 접촉저항 / 전하이동 / 공극 내 이온확산 | 우리 R_collector / R_ct / R_tort 3-분해와 1:1 |

---

## 2. 배경 · 동기 (Introduction, §1)

논문이 세우는 문제의식은 셋이다.

1. **왜 건식인가 (경제·환경)** — 슬러리 캐스팅에서 **팩 총제조비의 약 1/4** 이 용매 관련 공정에서
   나오고(Liu 2021), **용매 제거(건조·회수·재생)가 전형적 LiB embodied energy 의 절반** 을
   차지한다.  NMP 는 독성·인화성이며, LCO/NMC622 는 수계 용매를 쓰면 **Li leaching** 이 생겨
   NMP 를 피하기 어렵다(Hawley 2020).  ⇒ 무용매가 답이 될 수 있다.
   (배경 예시로 Volvo C40 Recharge **26.4 t CO₂-eq** vs 내연 XC40 **15.7 t** 을 든다.)
2. **건식 3대 계열** — ① **dry painting**(정전 분무 후 열압/열압연으로 바인더 활성화)
   ② **powder extrusion moulding**(바인더 **40–50 vol%** → 압출 → 탈지 → **500–900 °C 소결**)
   ③ **PTFE-fibrillation**.  ③ 이 산업 관심(Tesla Battery Day 2020, Maxwell 2003 특허; Samsung·LG
   의 PTFE 기반 ASSB 논문)의 초점이다.  ③ 은 (i) 건식혼합 → (ii) **피브릴화** → (iii) 열압연.
3. **공백** — PTFE-fibrillation 연구는 **ASSB 복합양극·SE 분리막에 편중**돼 있고
   (Hippauf 2019: NMC + Li₆PS₅Cl + CNF + **0.1–1 wt% PTFE**, 가열 mortar 1 min → 열압연 ~100 µm ·
   Zhang 2021: Li₆PS₅Cl + **0.2 wt% PTFE** 볼밀 → 80 °C 열압연 → **30 µm** 분리막 ·
   Lee 2023: Li₆PS₅Cl + **0.2–5 wt% PTFE** mortar 전단 → 20–120 °C 압연 → **300 µm**),
   **LiB 쪽은 오히려 PTFE 를 많이 쓴다**(Zhang 2022 흑연 + 5 wt% CB + **5 wt% PTFE** jet-mill →
   160 °C → 80 µm · Tao 2023 NMC/흑연 + 3 wt% CB + **5 wt% PTFE** → 50 °C → 120–150 µm).
   그런데 **피브릴이 너무 미세해 완전한 특성화가 안 됐고, 미세구조 차이 ↔ 성능 차이의 연결도
   자세히 연구된 바 없다.**

⇒ 이 논문의 과제: **소량 PTFE 의 LiB 건식 전극에서 피브릴 망을 고해상으로 분해**하고,
**형성 기전의 정성 모델**을 세우고, **슬러리 대비 미세구조 차이가 전기화학에 어떻게 나타나는지**
연결하는 것.

> ★ 우리 눈으로: **Hippauf(0.1–1 wt%) · Zhang(0.2) · Lee(0.2–5) · 본편(1) 이 전부 sub-5 wt% 대역**이고
> 우리 **SBE 1.0 wt% / DBE 0.5 wt%** 가 바로 그 대역 한복판이다.  건식 LiB 쪽의 3–5 wt% 는 우리보다
> 훨씬 높다 — **PTFE 함량 축에서 우리는 "ASSB 계열"에 서 있다**는 것이 이 문단으로 확인된다.

---

## 3. ★★ 재료 · 제작 (Materials and Methods §2) — **PTFE 기하의 1차 자료가 여기 있다**

### 3.1 원료 (§2.1) — stated

| 물질 | 사양 (논문 명시) | 공급 |
|---|---|---|
| **CAM** | **LiNi₀.₆Mn₀.₂Co₀.₂O₂ (NMC622)**, **median 입경 10 µm**, 전형 방전용량 **175 mAh/g** (2.8–4.25 V) | Targray, Canada |
| **PTFE** | **분말 입경 100–200 µm** ← ★ **피브릴이 되기 전의 원료 크기** | 3M, Germany |
| **CNF** | **평균 Ø 150–200 nm**, 길이 **수십 µm (several tens of µm)** | Pyrograf, USA |
| PVDF | 슬러리용 바인더 분말 | Solvay, Belgium |
| C65 | 슬러리용 카본블랙 | Timcal, Belgium |
| LTO | 대극(풀셀), **median 5–10 µm** | MSE, USA |

> ★★ **CNF Ø 150–200 nm 는 우리 `VGCF_D = 0.15 µm` 의 독립 재확인**이다 (제품은 다르다 —
> 우리는 Showa Denko VGCF-H, 여기는 Pyrograf).  단 **길이는 다르다**: 우리 `VGCF_L = 10 µm` vs
> 여기 "수십 µm".  ⇒ 우리 VGCF 길이는 **이 논문 기준으로는 짧은 쪽**이지만, 제품이 다르므로
> 모순이 아니라 **밴드 확장**으로 기록한다.

### 3.2 건식 전극 제작 (§2.2) — ★ 공정 변수 전부

1. AM + 바인더 + CNF 를 **Thinky 유성혼합기, 6 min, 300 → 2000 rpm** 으로 건식 혼합
2. **agate mortar + pestle** 로 옮기고 **오븐 80 °C, 20 min** 예열 → **수동 혼합**
3. **5 min 후 단일 통짜 flake(single integral flake)** 획득
4. **SUMET CA3 열 캘린더**, **80 °C**, **라인압 50 N/mm** → **≈100 µm** 두께
   - 저자 주: "랩 규모지만 **산업 파일럿라인과 같은 핵심 단계 — 승온 전단혼합 + 캘린더 압축**"
   - ⚠ "**전단 온도 · 구성비 · 캘린더 조건을 바꿔가며 in-house 최적화한 결과**" 라고만 하고
     **그 스윕은 보고하지 않는다** (→ §12 n/a)

**조성 (★ 두 가지가 다르다 — 혼동 금지)**
- **전기화학용**: **NMC622 + 1 wt% PTFE + 3.5 wt% CNF**
- **미세구조 분석용**: **NMC622 + 1 wt% PTFE** — *CNF 를 일부러 빼서* PTFE 피브릴과 헷갈리지 않게 함
  (⇒ Fig 2A · Fig 3A,B 의 실 = **전부 PTFE**.  이 설계가 이 논문 SEM 의 신뢰도를 만든다.)

**슬러리 대조군**: C65 + PVDF/NMP 스톡(8 % PVDF) 5 min Thinky → AM + NMP 추가(고형분 60 wt%) →
10 min → doctor blade 로 **15 µm Al 박**에 캐스팅 → 80 °C 핫플레이트 건조 → 캘린더.
조성 **NMC622 + 2 wt% PVDF + 2 wt% C65**.

### 3.3 셀 (§2.3) — stated
- 14 mm 디스크, **120 °C 진공(Ar 플러시) 하룻밤 건조**
- 두께 **100–110 µm**, **면적로딩 30–32 mg/cm²** (양쪽 동일 — 공정한 비교를 위해)
- CR2032 반쪽셀(Li chip) / 풀셀(LTO), 유리섬유 분리막(Whatman)
- 전해질 **1 M LiPF₆ in EC/EMC 3:7 + 2 wt% VC** (Elyte), 반쪽 140 µL · 풀셀 180 µL
- 풀셀 N/P **면적·중량 용량비 ≈ 1:1.1**
- **EIS 는 코인셀이 아니라 El-Cell PAT 3전극**(Li 기준전극 + Li 대극)

### 3.4 전기화학 (§2.4) · 미세구조 (§2.5) — stated
- 반쪽셀 **2.5–4.2 V**, RT · 풀셀 **1–2.8 V**, **C/3**, RT
- 형성: **C/20 ×2 → C/10 ×2** · 충전 **CC-CV**(컷오프 전류 = CC 전류의 절반) → **CC 방전**
- 풀셀 전류는 **가정 이론용량 175 mAh/g** 기준
- **EIS**: **100 mHz – 1 kHz**, ac **10 mV**, Biologic VSP(±0.1 %), **ZView 4.0c** 등가회로 피팅
- **SEM/EDX**: **Zeiss Merlin FE-SEM, 가속전압 3 kV**, Oxford Instruments X-max EDX

---

## 4. ★★★ 결과 ① — 미세구조 (§3.1, Fig 2–4) — **이 카드의 심장**

### 4.1 저배율 대조 (Fig 2, 50 µm bar)

- **Fig 2A** (건식, NMC + 1 wt% PTFE, CNF 없음): **"매우 가늘고(< 1 µm in diameter) 길며(> 50 µm)
  NMC 입자 수십 개를 (적어도) 가로지르는 PTFE 피브릴"**.
- **Fig 2B** EDX (F+C = 초록): 그 실들이 **얇은 초록 선**으로 나타남 — 즉 PTFE 가 **선(線)** 으로만
  존재하고 표면을 덮지 않는다.
- **Fig 2C/D** (슬러리, PVDF+C65): PVDF 는 **"moss-like(이끼형)"** 형태(Almar 2019, Entwistle 2022)이고
  EDX 초록이 **면(面)으로 넓게 퍼져** AM 을 감싼다.

> ★ 우리 관점: **Fig 2B vs 2D 가 "선형 바인더 vs 면형 바인더" 의 교과서 그림**이다.
> 우리 복셀 규약에서 PTFE 를 **폴리라인(centerline path)** 으로 두는 선택(`POLYLINE_PHASES=(2,4,6)`)이
> 여기서 **형태론적으로 정당화**된다 — PVDF 였다면 폴리라인이 아니라 코팅(shell)이어야 한다.

### 4.2 고배율 — 계층이 드러난다 (Fig 3, 10 µm / 2 µm bar)

- **Fig 3A** (건식, 10 µm bar): 뚜렷한 **branch-like(가지형)** 형태.  **NMC 표면 가림(obscuration)이
  훨씬 적고, 기공 막힘(pore blockage)이 없다.**
- **Fig 3B** (건식, 2 µm bar): **"더 큰 피브릴이 다시 갈라져 수십 nm 이하(a few 10s of nm or less)의
  극세 피브릴이 되고, NMC 입자를 얽어매는 3D 피브릴 그물을 형성한다."**
  또 **"피브릴이 NMC 표면의 여러 지점에 'anchor' 되어 있다"** — 이것이 §4.3 기전의 관찰적 근거.
- **Fig 3C** (슬러리, 10 µm bar): **PVDF 패치가 NMC 표면의 상당 분율을 덮고, 전극 내부로 통하는
  기공을 부분적/완전히 막는다.**
- **Fig 3D** (슬러리, 2 µm bar): PVDF 안에 C65 미립자가 들어가 **CBD** 를 이룬다.
- 거시적으로 건식 전극은 **"유연하고 천 같은(fabric-like) 취급감"**.
- 저자는 슬러리 특유의 **건조 중 바인더 상부 이동(binder migration)** 을 지적하고
  (기공 막힘 악화·전해질 침투 제한·Li 이동 저해·수명 저하), **건식은 건조가 없으므로 원리적으로
  발생 불가**라고 정리한다.

### 4.3 ★ 형성 기전 3단계 (Fig 4A 모식도 + Fig 4B, 4C 실증)

논문이 제시하는 정성 모델 (본문 그대로의 논리 흐름):

1. **압착 + 맞물림** — 전단혼합 중 **10–20 µm NMC 입자가 100–200 µm PTFE 원료 입자에 눌린다.**
   **NMC 표면의 마이크로 거칠기가 PTFE 표면 결정자(crystallite)와 쉽게 맞물려 견고한 anchor
   지점을 만든다.**  (Fig 4A inset 화살표 · Fig 4B 화살표)
2. **1차 인발** — 계속되는 혼합·전단으로 NMC 입자들이 서로 스쳐 멀어지며
   **"비교적 큰(지름 최대 수 µm) primary fibril" 이 뽑혀 나오고, 먼 거리까지 뻗는다.**
   Fig 4B **inset** 이 **"더 작은 PTFE 가닥들의 다발(bundle of smaller PTFE strands)로 이루어진
   primary fibril"** 을 보여준다 — ★ **primary 는 속이 찬 원기둥이 아니라 다발이다.**
3. **2차 인발(= 분지)** — 갓 만들어진 primary 피브릴 자신이 움직이는 NMC 입자에 다시 붙어,
   **primary 로부터 더 작은 다발이 뽑혀(unwinding) secondary fibril 이 된다** (Fig 4C 흰 화살표
   3개, 3 µm bar).  **"이 과정이 반복되어 점점 더 가는 피브릴이 되며, 끊어지지 않고(without
   breakage), 계층적 PTFE 피브릴 web 이 된다."**  부산물로 **occasional nodules(간헐적 혹)** 이 생긴다.

**문헌 근거**: Ariawan 2002 (PTFE fine-powder paste 압출: 표면 결정자가 맞물렸다가 입자가 서로
미끄러지며 **"unwound"** 되어 긴 피브릴이 됨) · Ardakani 2013 (**압축과 전단의 조합**이 필요).
저자는 "우리는 압출이 아니라 전단혼합이고 PTFE 도 소량이지만, **같은 crystallite interlocking →
unwinding 기전**이 일어나는 것으로 미세구조가 시사한다"고 명시한다.

### 4.4 ★★★ 그래서 **피브릴 지름 값**은 정확히 무엇인가 — 논문 전수 조사

**논문 전체에서 피브릴 치수를 말하는 문장은 아래 4 개가 전부다** (초록·§3.1·결론):

| 위치 | 원문 그대로 | 지름 | 길이 |
|---|---|---|---|
| 초록 | "primary fibrils of **a few µm in diameter** and **100's µm in length** that branched into secondary and then ever finer fibrils, **down to diameters of 10s nm or below**" | 수 µm → **10s nm 이하** | 수백 µm |
| §3.1 Fig 2A | "very fine (**< 1 μm in diameter**) and long (**> 50 μm**) PTFE fibrils spanning (at least) tens of NMC particles" | **< 1 µm** | **> 50 µm** |
| §3.1 Fig 3B | "larger fibrils again branched into extremely fine fibrils of **a few 10s of nm or less**" | **수십 nm 이하** | — |
| §3.1 기전 | "the first, relatively large (**up to a few μm in diameter**) primary fibrils, which can **extend over large distances**" | **최대 수 µm** | "먼 거리" |
| 결론 | "Large primary fibrils of **a few microns in diameter** and **hundreds of microns in length** branched into finer secondary and ever finer fibrils **down to diameters of tens of nanometers**" | 수 µm → **수십 nm** | **수백 µm** |

⛔ **분포는 없다.**  히스토그램·확률밀도·평균±표준편차·중앙값·**측정 개수 n·이미지 해석 절차**가
**하나도 없다.**  방법(§2.5)에는 SEM 조건(3 kV Merlin)만 있고 **정량 이미지 분석 서술이 전혀 없다.**
⇒ **정량 지름 분포를 이 논문에서 인용할 수 없다.**  줄 수 있는 것은 **구간(bracket)** 뿐이다:

> **PTFE 피브릴 지름 = [수십 nm, 수 µm] ≈ 두 자릿수(≈100×) 스팬 · 계층적 · 분포 미보고**
> **길이: primary 수백 µm (Fig 2A 는 >50 µm)**

### 4.5 우리가 그림에서 직접 잰 값 — 📉 **digitized · TREND only · 상한**

논문이 분포를 안 주므로 **우리가 그림을 디지타이즈**했다.  ⚠ **인쇄 래스터 한계를 먼저 적는다** —
PDF 내장 이미지가 **전부 300 dpi** 라, 각 패널의 **네이티브 픽셀 = 물리 크기**가 정해져 있다:

| 패널 | 스케일바 | **네이티브 1 px** | 잰 값 (반치폭 능선 스캔) | 판정 |
|---|---|---|---|---|
| **Fig 3B** | 2 µm | **≈ 8.2 nm** | 가닥 폭 중앙 **≈ 34 nm**, p10–p90 **≈ 18–58 nm**, **최대 ≈ 95 nm** | **논문의 "a few 10s of nm" 를 재현.** 이 프레임에 250 nm 는 **하나도 없다** |
| **Fig 3A** | 10 µm | ≈ 32.7 nm | 중앙 ≈ 112 nm (= 3.4 네이티브 px) | ⚠ **해상도 바닥에 붙음 → 상한**, 참값은 더 작다 |
| **Fig 2A** | 50 µm | ≈ 163 nm | 중앙 ≈ 0.57 µm (= 3.5 네이티브 px) | ⚠ **완전한 해상도 한계 + AM 입자 모서리 오염 → 인용 부적합** |
| **Fig 4B inset** | 2 µm (318 px @900 dpi) | ≈ 18.9 nm | primary 다발 폭 **≈ 1–2 µm** | 논문의 "up to a few µm" 와 **일치** |

★ **가장 방어 가능한 한 줄 — Fig 6A 의 내부 자(ruler)**:
Fig 6A(사이클 후, 2 µm bar)는 **초록 화살표 = PTFE 피브릴**, **주황 화살표 = CNF** 로 둘을 나란히
찍어 놓았고, **CNF 는 방법(§2.1)에 Ø 150–200 nm 로 명시**돼 있다.  같은 프레임에서
**CNF(주황) 로드가 PTFE(초록) 가닥보다 눈에 띄게 3–5 배 굵다.**
⇒ **DERIVED(ours): 그 프레임의 PTFE 피브릴 Ø ≈ 30–70 nm** (150–200 nm ÷ 3–5).
이것은 절대 픽셀 측정이 아니라 **같은 이미지 안의 stated 자와의 비율**이라 래스터 한계에 훨씬 강하다.

**⇒ 종합 판정 (§13.1 로 이어짐)**
> **개수(number) 기준으로 PTFE 피브릴 인구의 대부분은 수십 nm 대에 있고, 부피(volume) 기준으로는
> 수 µm primary 가 압도한다.**  논문은 **어느 쪽 분포도 주지 않으므로 그 배분은 `n/a`** 다.
> **우리 `PTFE_D = 0.25 µm` 는 두 인구의 사이(gap)에 있다** — 어느 쪽도 아니다.

---

## 5. 결과 ② — 전기화학 (§3.2, Fig 5·7, Table 1)

### 5.1 첫 사이클 C/20 (Fig 5) — stated
- 충·방전 프로파일 **거의 동일**, 공급사 사양과 일치
- 방전용량 **건식 169 mAh/g vs 슬러리 163 mAh/g**
- 첫 충전 **CE 91.1 % (건식) vs 91.3 % (슬러리)** — CEI 형성에 의한 비가역, 사실상 동일
- 저자 주: **형성 프로토콜을 양쪽 동일하게 썼으나, 건식 미세구조에는 재최적화 여지가 있다**

### 5.2 ★ 율특성 (Fig 7A, 반쪽셀 vs Li) — stated + 📉digitized

| C-rate | **건식 개선율 (stated)** | 📉 절대 용량 (digitized, ±3 mAh/g) |
|---|---|---|
| 0.1C | **+4.5 %** | ≈ 163 vs 156 |
| 0.2C | **+6 %** | ≈ 157 vs 148 |
| 0.5C | **+10 %** | ≈ 143 vs 130 |
| 1C | **+27 %** | ≈ 125 vs 99 |
| **2C** | **+146 %** | **≈ 56 vs 23** |
| 0.1C 복귀 | — | ≈ 162 vs 153 (양쪽 회복) |

초록·결론은 이 **+146 %** 를 **"up to 150 % at 2C"** 로 반올림한다.

⚠⚠ **헤드라인 "2C 에서 150 %" 의 조건을 반드시 붙일 것** (요청 항목 ⑥):
- **조건**: **반쪽셀 vs Li 금속** · **2.5–4.2 V** · RT · 두께 100–110 µm · 면적로딩 30–32 mg/cm² ·
  0.1C→2C→0.1C **30 사이클 율 시험** 안의 한 구간 · 액체전해질 1 M LiPF₆ EC/EMC 3:7 + 2 wt% VC
- **"용량이 150 %" 가 아니라 "150 % *증가*"** = **약 2.5배**.
- ★★ **그러나 그 2C 지점은 두 전극 모두 붕괴한 자리다** — **56 / 23 mAh/g** 은 각각 0.1C 대비
  **34 % / 15 %** 에 불과하다.  즉 **큰 배수는 분모가 작아서** 나온다.  **실용 구간(≤1C)의
  이득은 +4.5 ~ +27 %** 이고 이쪽을 함께 적지 않으면 과대 인용이 된다.
- 저자 자신도 **"최저율에서의 5–10 % 개선은 (이온이동이 아니라) 약간 낮은 전하이동저항에서
  왔을 가능성이 크다"** 고 구분해 적는다.

### 5.3 장기 사이클 (Fig 7B, 풀셀 NMC–LTO, C/3, 200 cyc) — stated
- 평균 용량유지율 **건식 96 % vs 슬러리 93 %**
- 열화율 **0.02 %/cycle vs 0.035 %/cycle** ⇒ 초록의 **"40 % 더 느리게 열화"**
  (⚠ 산술로는 1 − 0.02/0.035 = **43 %** — 저자가 40 % 로 반올림)
- CE 는 양쪽 모두 ~100 % 로 겹침 (Fig 7B 오른축)

### 5.4 ★ 사이클 후 미세구조 (Fig 6) — **PTFE 안정성 논쟁의 결론**
- 시험: **0.1C → 2C → 0.1C, 30 사이클** 후 해체
- **Fig 6A** (건식, 1 wt% PTFE + 3.5 wt% CNF, 2 µm bar): **피브릴이 그대로 관찰됨** ⇒
  **셀 조립/해체 + 30 사이클을 견딤.**  CNF 도 PTFE 망에 **얽혀(enmeshed)** 있음.
  초록 화살표 = PTFE, 주황 = CNF.
- **Fig 6B** (슬러리, 5 µm bar): PVDF+C65 CBD 가 **pristine(Fig 3C)과 같은 형태**로 남음
  (EDX 확인은 Supplementary Fig S1 — 이 파일에 없음)
- 저자는 문헌의 **불일치**를 정면으로 정리한다:
  - **Hippauf 2019**: NMC–Li₆PS₅Cl 복합양극 **압축 중 피브릴이 끊어질 것**, 셀 조립 후 PTFE 는
    기계적 무결성에 기여 안 함
  - **Lee 2023**: Li₆PS₅Cl 분리막에서 **과도한 캘린더링 후에도 조밀한 피브릴 망 관찰**,
    PTFE 가 기계적 안정성에 결정적
  - **Zhang 2022**: PTFE–흑연 음극에서 **사이클 후 피브릴 관찰 불가** → 음극 전위에서 불안정,
    첫 리튬화 때 **carbyne 으로 환원**
  - **Manev 1995 / Novák 1997**: PTFE 바인더 흑연 음극도 **안정적으로 사이클**
  - **본편의 기여**: **양극 전위(2.5–4.2 V vs Li)에서는 30 사이클 후에도 살아있다** —
    ⚠ 음극 쪽 논쟁에는 답하지 않는다.

### 5.5 ★★ EIS 3전극 (Fig 8, Table 1) — stated

**Fig 8A** Nyquist(방전 상태, 축 **Z′ 0–100 Ω · −Z″ 0–100 Ω**).  본문은 "넓은 arc + 저주파 굽은
꼬리"라 쓰지만 **그림은 눌린 반원 2개 + 상승 꼬리**로 보인다 (🔍 figure-read).
건식(파랑)은 1st arc 정점이 **−Z″ ≈ 21 Ω @ Z′ ≈ 25**, 슬러리(주황)는 **≈15 Ω @ Z′ ≈ 27**;
저주파에서 **주황이 Z′ ≈ 75 부근에서 가파르게 프레임 밖으로 상승**하고 파랑은 **Z′ ≈ 93 안에서
2nd arc 를 닫는다** — Table 1 의 총합(SF 104 Ω vs SC 159.5 Ω)과 정합.

★ **inset 등가회로 (🔍 figure-read — 본문에 회로식이 없어 그림에서 읽음)**:
**직렬 3블록 사다리**
> **(R_cont ∥ C_cont) — (R_ct ∥ C_dl) — (R_ion ∥ CPE_ion)**

⇒ **Randles 가 아니다** (Warburg 대신 **CPE_ion**, 그리고 **접촉 블록이 앞에 하나 더** 있다).
우리 `eis_drt_ica.py` 의 Randles(R0 + R_ct∥C_dl + Wo) 와 **위상이 다르다** — 대조할 때 반드시 명시.

**Fig 8B** spectroscopic capacitance (**log C′/F, −2 … −6** vs **log f/Hz, −1 … 3** = 0.1 Hz–1 kHz ✓
본문 측정범위와 일치).  곡선 위에 **CPE_ion**(저주파, 좌상) · **C_dl**(중간) · **C_cont**(고주파, 우하)
가 직접 라벨돼 있어 **세 시간상수의 귀속이 그림에 박혀 있다**.  슬러리(주황)가 전 구간에서 건식(파랑)
**위**에 있다.  ⚠ 본문은 "세 평탄역(plateaux)"이라 하지만 **실제로는 단조 감소에 어깨(shoulder) 세 개**에
가깝다 (🔍 figure-read) — "평탄역"을 문자 그대로 인용하지 말 것.
귀속 근거는 Atebamba 2010, 식별자는 **τ = RC**.

**Table 1 — 등가회로 최적적합 저항 (괄호 = 마지막 자리 불확도)**

| 양극 | **R_cont [Ω]** | **R_CT [Ω]** | **R_ion [Ω]** |
|---|---|---|---|
| **Solvent-free** | **36 (1)** | **18 (1)** | **50 (4)** |
| **Slurry cast** | **24.6 (7)** | **20.9 (9)** | **114 (28)** |

해석 (저자):
- **R_cont 는 건식이 더 크다 (36 vs 25)** — **"건식 전극이 집전체 위에 형성된 것이 아니기(자립막)
  때문일 것"**.  ⇒ ★ 이건 **결함이 아니라 자립막 구조의 대가**.
- **R_CT 는 비슷** (18 vs 21) — 다만 건식이 약간 낮고, 이것이 **저율 5–10 % 이득**의 원인 후보.
- **R_ion 은 건식이 절반 이하 (50 vs 114, −56 %)** — 슬러리는 CBD 가 NMC 표면을 크게 덮고
  기공 일부를 막는데(Fig 3C), 건식은 **기공 막힘 0 · 표면 가림 최소**(Fig 3A) ⇒
  **기공을 통한 이온 이동이 개선**되고, **이것이 고율 용량을 지배한다**(Besnard 2017).

> ★★ **이 표가 이 논문에서 우리 축으로 가장 강하게 전이되는 정량 자료다.**
> 우리 `R_int` 3-분해(**R_contact[Holm + R_ct] + R_tort[SE 이온-τ] + R_collector**)와
> **항 대 항으로 1:1 대응**한다 (`docs/project_rint_fullcell_cycling.md`).
> ⚠ 단 **Ω 단위 그대로이고 면적 정규화가 없다** — EIS 는 코인셀이 아니라 **El-Cell PAT** 에서
> 쟀는데 **PAT 전극 지름이 논문에 없다** ⇒ **Ω·cm² 로 환산 불가** (§12 n/a).

---

## 6. 그림 한 장씩 — 무엇을 보이고 우리가 무엇을 쓰나

| Fig | 내용 | ★ 우리가 쓸 것 |
|---|---|---|
| **1** | 🔍 3단계 공정 모식도 — **1. Mixing**(2축 회전 유성혼합기, 회색 AM + **초록 PTFE 구**) → **2. Fibrillation**(**mortar & pestle**, 초록 PTFE 가 **하나의 물결치는 실**로 뽑혀 회색 입자들을 꿰뚫음) → **3. Calendering**(2-롤) | ★ 우리 `ADDITIVE_PROCESS['PTFE']` mixing 프리셋이 **어느 단계를 대리하는지** 그림으로 확인.  ★★ **②·③ 에서 PTFE 가 "입자를 꿰는 한 가닥 곡선"으로 그려진다** = 우리 **폴리라인 표현**의 도해적 정당화.  ⚠ 우리는 ②를 **모사하지 않고 결과만 씨앗한다** |
| **2A/B** | 건식 표면 SEM + EDX(F,C 초록) — **가늘고(<1 µm) 긴(>50 µm) 선형 PTFE**, NMC 수십 개 span | ★ **선형(폴리라인) 바인더의 형태론적 근거** · Ø<1 µm · L>50 µm 상한/하한 |
| **2C/D** | 슬러리 표면 + EDX — **moss-like PVDF 가 면으로 덮음** | 우리가 PVDF/CBD 를 모델링할 일이 생기면 **shell/coat 규약**이지 폴리라인이 아니다 |
| **3A** | 건식 10 µm bar — 가지형 web, **표면 가림 적음 · 기공 막힘 없음** | ★ 우리 **coverage · pore-τ** 축의 정성 기준선.  📉 실 폭 상한 ≈112 nm(해상도 바닥) |
| **3B** | 건식 2 µm bar — **10s nm 극세 피브릴 + AM 표면 다지점 anchor** | ★★ **`branch to 10s nm` 주석의 실제 출처** · 📉 가닥 폭 중앙 ≈34 nm |
| **3C** | 슬러리 10 µm bar — **PVDF 패치가 표면 덮고 기공 막음** | 슬러리의 R_ion 114 Ω 의 그림 증거 |
| **3D** | 슬러리 2 µm bar — PVDF 안의 C65 = **CBD** | CBD 개념의 원형 그림 |
| **4A** | **형성 기전 3단계 모식도** (①압착·맞물림 ②primary 인발 ③secondary 인발) | ★★ **우리 `vol_conserve` 등체적 인발 + `branch_frac` 의 물리적 스토리보드** |
| **4B** | primary 형성 실사 (20 µm bar) + **inset(2 µm)**: **작은 가닥들의 다발** | ★★ **primary = 다발(bundle)** — 우리 단일 실린더 표현의 한계를 규정.  📉 다발 폭 ≈1–2 µm |
| **4C** | **secondary 인발 실사** (3 µm bar, 화살표 3개) + **nodules** | ★★ **`branch_n` 의 직접 증거** (한 primary 에서 **2개** 가지가 화살표로 지시됨) |
| **5** | 첫 C/20 충·방전 곡선 (169 vs 163 mAh/g) | 미세구조 차이가 **열역학 용량이 아님** = 우리 SDCP 서사와 동일 논법 |
| **6A** | **사이클 후** 건식 (2 µm bar) — **초록=PTFE, 주황=CNF** 병기 | ★★★ **내부 자(ruler)**: CNF(stated 150–200 nm)가 PTFE 보다 3–5× 굵다 ⇒ **PTFE ≈ 30–70 nm** |
| **6B** | 사이클 후 슬러리 (5 µm bar) — CBD 형태 유지 | 대조군 |
| **7A** | 율특성 반쪽셀 0.1C→2C→0.1C | ★ **+4.5/+6/+10/+27/+146 %** 사다리.  ⚠ 2C 절대값이 56/23 이라는 것과 **함께** 인용 |
| **7B** | 풀셀 NMC–LTO 200 cyc C/3 + CE | 96 vs 93 % · 0.02 vs 0.035 %/cyc |
| **8A** | 🔍 3전극 Nyquist (Z′/−Z″ 0–100 Ω, 반원 2개+꼬리) + **등가회로 inset = (R_cont∥C_cont)—(R_ct∥C_dl)—(R_ion∥CPE_ion) 직렬 3블록** | ★★ **회로 위상이 Randles 가 아니다** (Warburg 대신 CPE, 앞에 접촉 블록) — 우리 `eis_drt_ica.py` 와 대조할 때 **반드시 명시** |
| **8B** | 🔍 spectroscopic capacitance (log C′/F −2…−6 vs log f/Hz −1…3) — 곡선에 **CPE_ion / C_dl / C_cont** 직접 라벨 | ★ **τ=RC 로 접촉/전하이동/기공확산을 분리**하는 방법 — 우리 DRT 와 같은 목적, 다른 도구.  ⚠ 본문 "평탄역"은 실제로는 **어깨** |

---

## 7. Post-processing — 그들이 실제로 쓴 방법

| 무엇 | 도구 / 절차 | 수치화 여부 |
|---|---|---|
| 피브릴 형태 | **Zeiss Merlin FE-SEM, 3 kV** (저전압 = 표면 민감, 코팅 없이 폴리머 관찰) | ⛔ **정성만** — 이미지 분석·측정 n·분포 **없음** |
| 상 분포 | **EDX(Oxford X-max)**, Ni+O → AM(파랑), F+C → 바인더(초록) | 정성 맵 (정량 wt% 없음) |
| 형성 기전 | **다수 관찰 기반의 정성 모델** + 문헌(Ariawan 2002, Ardakani 2013) | ⛔ 모델링·시뮬레이션 **0** |
| 사이클 후 안정성 | 해체 후 SEM, 화살표 라벨(PTFE/CNF) | 정성 |
| 율특성 | Arbin, CC-CV/CC, 형성 후 30 사이클 rate ladder | **개선율 %** stated |
| 임피던스 | **3전극 El-Cell PAT** + **ZView 4.0c 등가회로 피팅** + **spectroscopic capacitance** 표현.  회로 = 🔍 **(R_cont∥C_cont)—(R_ct∥C_dl)—(R_ion∥CPE_ion) 직렬 3블록** (Fig 8A inset 에서 읽음 — 본문에 회로식 없음) | **Table 1** stated (Ω, 불확도 포함).  ⚠ **C·CPE 값은 미보고** |
| 시간상수 분리 | **τ = RC** 로 세 과정 귀속 (Atebamba 2010 준거) | 정성 귀속 (**τ 수치 미보고**) |

> **🔍 그림 판독 공개 (무엇을 실제로 봤나)**: `fig_1`(공정 모식도) · `fig_2`(저배율 SEM+EDX) ·
> `fig_3`(고배율 SEM) · `fig_4`(기전 모식도+실증) · `fig_5`(첫 사이클) · `fig_6`(사이클 후 SEM) ·
> `fig_7`(율/사이클) · `fig_8`(EIS) **전부 이미지로 확인**했다.  `Table 1` 은 **이미지가 아니라 PDF
> 텍스트**로 읽었다(더 정확).  🔍 표시가 붙은 서술은 **그림에서만 얻은 것**이고, 📉 는 **픽셀 측정
> (추세용)** 이다.

> ★ **DRT 를 쓰지 않았다** — spectroscopic capacitance 로 평탄역을 세는 고전적 방법이다.
> 우리 `eis_drt_ica.py`(Tikhonov DRT)는 **같은 분리를 더 세게** 한다 ⇒ 이 논문 데이터에
> 우리 도구를 얹으면 R_ion/R_CT 분해가 재현되는지 **방법 대조**가 가능하다 (§16 백로그).

---

## 8. 수치 총괄표 — stated / digitized / DERIVED(ours) / n/a

### ✅ stated (본문 명시)
| 항목 | 값 |
|---|---|
| PTFE 함량 | **1 wt%** (미세구조 전용 시료도 1 wt%) |
| CNF 함량 | **3.5 wt%** (전기화학용), 미세구조 시료는 **0** |
| 슬러리 대조 | **2 wt% PVDF + 2 wt% C65** |
| NMC622 | median **10 µm**, 175 mAh/g (2.8–4.25 V) |
| PTFE 원료분말 | **100–200 µm** |
| CNF | **Ø 150–200 nm**, L 수십 µm |
| LTO | **5–10 µm** |
| primary 피브릴 | Ø **최대 수 µm** · L **수백 µm** |
| Fig 2A 피브릴 | Ø **< 1 µm** · L **> 50 µm** |
| 최종 분지 | Ø **수십 nm 이하 (10s nm or below)** |
| 전극 두께 | **100–110 µm** (양쪽) |
| 면적로딩 | **30–32 mg/cm²** (양쪽) |
| 캘린더 | **80 °C · 50 N/mm 라인압** (SUMET CA3) |
| 혼합 | Thinky **6 min, 300→2000 rpm** · mortar **80 °C 20 min + 수동 5 min** |
| 첫 방전 C/20 | **169 vs 163 mAh/g** · CE **91.1 vs 91.3 %** |
| 율 개선 | **+4.5 / +6 / +10 / +27 / +146 %** (0.1/0.2/0.5/1/2C) |
| 사이클 | **96 vs 93 %** @200 cyc C/3 (풀셀) · **0.02 vs 0.035 %/cyc** |
| **EIS** | **R_cont 36(1) vs 24.6(7) Ω · R_CT 18(1) vs 20.9(9) Ω · R_ion 50(4) vs 114(28) Ω** |
| EIS 조건 | 100 mHz–1 kHz · 10 mV ac · 3전극 El-Cell PAT · 방전상태 |

### 📉 digitized (우리가 그림에서 읽음 — **추세용 · ±**)
| 항목 | 값 | 주의 |
|---|---|---|
| Fig 3B 가닥 폭 | 중앙 **≈34 nm**, p10–p90 **≈18–58 nm**, 최대 **≈95 nm** | 네이티브 1 px ≈ 8.2 nm → **하한 절단**, AM 결정자 모서리 오염 있음 |
| Fig 3A 실 폭 | 중앙 **≈112 nm** | = 3.4 네이티브 px = **해상도 바닥 → 상한** |
| Fig 2A 실 폭 | 중앙 **≈0.57 µm** | **해상도 한계 + 입자 모서리 오염 → 인용 부적합** |
| Fig 4B inset primary | 폭 **≈1–2 µm** | "up to a few µm" 와 일치 |
| Fig 7A 절대용량 | 0.1C 163/156 · 1C 125/99 · **2C 56/23** mAh/g | ±3 |

### 🧮 DERIVED (ours — 논문에 없음, 가정 명시)
| 항목 | 값 | 가정 |
|---|---|---|
| **Fig 6A PTFE 피브릴 Ø** | **≈30–70 nm** | 같은 프레임의 **stated CNF Ø 150–200 nm** 를 자로 삼고, 육안 굵기비 3–5× |
| primary AR | **≈33–500** (중심 100–200) | Ø 1–3 µm × L 100–500 µm |
| Fig 2A AR | **> 50** | Ø<1 µm, L>50 µm |
| 열화율 비 | **43 % 느림** | 0.02/0.035 (논문 표기 "40 %" 는 반올림) |
| 2C 이득의 분모 | 0.1C 대비 **34 % / 15 %** | 56/163, 23/156 |
| R_ion 개선 | **−56 %** | 50 vs 114 |

### ⛔ n/a — 논문 미보고 (우리 요청 축과 직결되는 것 우선)
- **피브릴 지름 분포 / 히스토그램 / n / 평균±sd / 이미지 분석 절차** ← ★ 요청 ①의 직접 답
- **피브릴 길이 분포**, **primary : secondary : tertiary 의 개수·부피 배분**
- **porosity · 밀도 · tortuosity** — 한 번도 나오지 않는다 (우리 축 A 대조 불가)
- **PTFE 함량 스윕** (1 wt% 한 점) — 함량↔미세구조·성능 곡선 없음 ⇒ **요청 ⑤는 이 논문으로 못 채움**
- **전단·온도·시간 스윕** — "in-house 최적화"라고만, 데이터 없음 ⇒ **무엇이 굵기를 정하는지 정량 불가**
- **σ_e / σ_ion 절대값** — EIS 는 **Ω**, PAT 셀 전극 면적 미기재 ⇒ **Ω·cm² 환산 불가**
- **기계 물성** (인장강도·접착력·모듈러스) — "flexible/fabric-like/cloth-like" 정성 표현뿐
- **분지 차수(generation) 수 · 분지각 · 분지 간격**
- **PTFE 탈불소화·carbyne 화 여부** (Zhang 2022 를 인용만 하고 자기 데이터 없음)
- SI: Table S1(로딩), Table S2, Figure S1(사이클 후 슬러리 EDX) — **제공 PDF 에 없음**

---

## 9. 논문 내부 불일치 · 오식 (인용 시 반드시 교정)

1. **결론의 단위 오식** — "areal loading (**30–32 mAh/cm²**)" 은 **mg/cm²** 여야 한다 (§2.3 이 맞다).
2. **입경 불일치** — §2.1 "median particle size of **10 µm**" vs §3.1 기전 "The **10–20 µm** NMC particles".
3. **반올림 미끄러짐** — 결과 **+146 %** ↔ 초록·결론 **"150 %"**; 열화율 비 **43 %** ↔ 초록 **"40 %"**.
4. **"increased by 150 %"** 는 **2.5배**를 뜻한다 — "용량이 150 %" 로 읽으면 **오독**.
5. 오탈자: "Furthemore" · "**crysallites**" · §3 의 "**polyvinyldifluoroethylene**"
   (§2.1 은 올바르게 *polyvinylidene fluoride*) · "**Novfik**"(→ Novák) · "aerial loading"(→ areal) ·
   §1 "Figure 1 number of process variants have evolved" (문장 조각 누락, ". A" 탈자).
6. **Fig 8 캡션의 "in the discharged state"** 는 본문에 조건이 더 없다 — SOC·사이클수 미기재.
7. 🔍 **본문 "a broad arc with a curved tail at low frequency"** 는 Fig 8A 와 정확히 맞지 않는다 —
   그림은 **눌린 반원 2개 + 상승 꼬리**이고, 저자 자신의 회로도 **RC 블록 3개**다.
   ⇒ "하나의 넓은 arc" 로 인용하지 말 것.
8. 🔍 **본문 "three plateaux"** 도 Fig 8B 에서는 **단조 감소의 어깨(shoulder) 3개**에 가깝다.
9. **등가회로 식이 본문에 없다** — 회로는 **Fig 8A inset 그림에만** 있고, **C_cont·C_dl·CPE_ion 의
   피팅값과 CPE 지수 n 은 아예 미보고**다.  Table 1 은 **R 세 개만** 준다.

---

## 10. ★ 우리 DEM+MPM 대비 → `our_dem_baseline.md` · `comparison_vs_ours_DEM.md`

### 10.0 침대 대조표

| 축 | Matthews 2024 | 우리 (SBE / DBE) | 전이 가능? |
|---|---|---|---|
| 전해질 | **액체 1 M LiPF₆ EC/EMC 3:7 + 2 wt% VC** | **고체 Li₆PS₅Cl** | ⛔ **이온상 반전 — 값 전이 금지** |
| CAM | NMC**622**, **poly, median 10 µm** | NMC811 (AM_P/AM_S bimodal) | 🔶 형태 유사, 조성 다름 |
| **PTFE** | **1 wt%** | **SBE 1.0 / DBE 0.5 wt%** | ✅ **같은 대역 — 조성 축은 직접 대조 가능** |
| 탄소 | **CNF 3.5 wt%, Ø 150–200 nm** | **VGCF 3 wt%, Ø 150 nm** | ✅ **거의 동일** |
| 두께 | 100–110 µm | 우리 침대 ~30–115 µm | 🔶 |
| 압력 | 캘린더 **50 N/mm 라인압** (면압 미환산) | 성형 **300 MPa** | ⛔ 규약 다름 — 직접 비교 불가 |
| porosity | **n/a** | ε_sphere 규약으로 보고 | ⛔ |
| 시뮬레이션 | **0** | DEM + MPM + STEP3 복셀 FV | — |

### 10.1 ★★ 축 ①: **PTFE 기하 앵커** — 이 카드의 본론

**(a) 우리 상수의 출처 판정**

`scripts/additives.py:38` 의 주석은 두 출처(`RSC D5EE03240G`; `Front. Energy 2023.1336344`)를
`0.25 µm / 40 µm / AR≈160` 에 붙여 놓았다.  **이 논문 전수 조사 결과:**

- **`branch to 10s nm`** → ✅ **이 논문의 문장 그대로다** (초록 "down to diameters of **10s nm** or
  below"; §3.1 "a few **10s of nm** or less"; 결론 "**tens of nanometers**").
  ⇒ **주석의 이 조각은 정확히 이 논문에서 왔다.  앵커 확정.**
- **`spanning tens of NMC`** → ✅ **Fig 2A 문장 그대로** ("spanning (at least) **tens of NMC particles**").
  ⇒ **앵커 확정.**
- **`PTFE_D = 0.25 µm`** → ⛔ **이 논문에 없다.**  논문이 주는 것은 `<1 µm`(Fig 2A) · `수 µm`(primary) ·
  `수십 nm 이하`(finest) 이고, **0.25 µm 는 그 어느 문장에도 나오지 않는다.**
  ⇒ **미앵커.  "구간 안"이지만 "이 논문 값"이 아니다.**
- **`PTFE_L = 40 µm`** → ⛔ **없을 뿐 아니라 방향이 어긋난다.**  논문은 primary 를 **"100's µm"**,
  Fig 2A 를 **"> 50 µm"** 라 한다.  **40 µm 는 그 하한(50)보다도 짧다.**
  ⇒ **미앵커 · 우리 값이 짧은 쪽으로 벗어남.**
- **`AR ≈ 160`** → 🔶 **간접 지지.**  논문 자신의 (Ø 1–3 µm, L 100–500 µm) 쌍은 **AR ≈ 33–500**,
  중심 100–200.  Fig 2A 는 **AR > 50**.  ⇒ **AR 160 은 방어 가능한 유일한 조각**이다.
  **역설**: 우리 (0.25, 40) 과 논문의 (2, 300) 은 **AR 은 거의 같은데(160 vs 150) Ø 는 8배, L 은
  7.5배 다르다** — 즉 **AR 만 맞추고 절대 크기를 놓친 표현**이다.

> ★★★ **자릿수 판정 (요청 ①의 직접 답)**
> 제목은 **nano**-fibril 이지만 그것은 **계층의 아래 끝**을 가리키는 말이다.
> **위 끝은 수 µm 로 마이크로 스케일**이다.  우리 **0.25 µm = 250 nm** 는
> **위 끝보다 ~10배 작고, 아래 끝(수십 nm)보다 ~8배 크다** — **두 인구의 사이 골짜기**에 있다.
> 자릿수가 "틀렸다"기보다 **두 자릿수 분포를 한 점으로 접은 값**이고,
> 하필 **관측 인구가 가장 희박한 중간**에 놓였다.

**(b) 🧮 DERIVED — 그 선택이 우리 침대에서 무엇을 뜻하나**

우리 생산 레시피 `AM:SE:VGCF:PTFE = 80:18:1:1`, RVE 50×50×33 µm (solid 71,775 µm³)
→ PTFE **1.7 vol% = 1,226 µm³** (`scripts/additives.py` 실행값).
이 부피를 **어느 기하로 그리느냐**에 따라:

| 표현 | 객체 1개 부피 | **객체 수 n** | 우리 vox 0.15 µm 대비 |
|---|---|---|---|
| **Matthews primary** (Ø 2 µm × L 300 µm) | 942 µm³ | **≈ 1.3 개** | 13.3 vox 두께 = **해상됨** |
| **우리 현행** (Ø 0.25 × L 40) | 1.963 µm³ | **624 개** | 1.67 vox = **경계** |
| **Matthews finest** (Ø 30 nm × L 5 µm) | 3.53×10⁻³ µm³ | **≈ 347,000 개** | **0.2 vox = 5× 미해상** |

★ 세 가지가 동시에 드러난다:
1. **객체 수가 5.4 자릿수(1.3 → 347,000) 를 스팬한다** — 우리 624 는 그 **로그 중앙**
   (log₁₀: 0.11 / **2.80** / 5.54; 양 끝 중점 2.82).  즉 우리 값은 **"두 자릿수 분포의 기하평균"**
   이라는 뜻이고, **어느 쪽 물리도 표현하지 않는다**는 뜻이기도 하다.
2. ★★ **Matthews 의 primary 는 우리 RVE 에 들어가지 않는다.**  길이 **100s µm** 가 우리 상자
   **50 µm** 를 **2–10배** 넘고, **한 가닥이 1 wt% PTFE 부피를 통째로 소진**한다(n≈1.3).
   ⇒ **우리 침대는 primary 피브릴 하나의 span 안쪽에 있는 부분체적**이다.  주기경계에서 primary 는
   "인구"가 아니라 **관통하는 한 가닥**으로 표현돼야 하고, 우리 624개 짧은 실은 물리적으로
   **secondary/tertiary web 의 조각 표본**으로 읽는 것이 정직하다.
3. ★★ **finest 를 그리면 표현부피가 폭발한다.**  Ø 30 nm 섬유를 vox 0.15 µm 격자에 **1셀 폭
   centerline 스탬프**하면 단위길이당 단면이 **(0.15)²/(π·0.015²) ≈ 32배** (점간격 0.7·dx 규약이면
   **≈45배**) 부풀어, 1.7 vol% PTFE 가 **침대의 절반 이상**을 차지하게 된다.
   ⇒ **CL-25(SDCP 표현부피 4.31 → 0.238, 18배 변동) 와 정확히 같은 병리**이고, 이것이
   `step3_sigma.py` 가 **생산에서 PTFE 를 전도 격자에 아예 스탬프하지 않는** 이유의 사후 정당화다.
   ⚠ 반대로 **우리 0.25 µm** 를 1셀 폭으로 찍으면 **0.46배 = 2.2배 과소** — **부호가 반대다**.
   **표현부피 오차의 부호가 지름에 따라 뒤집힌다**는 것이 CL-25 의 PTFE 판이다.

### 10.2 ★★ 축 ②: **격자로 닫히지 않는다** — Koo sheath 판정과 같은 부류 (요청의 마지막 항)

우리 생산 복셀 = **0.15 µm** (수렴 스윕 0.15 / 0.125 / 0.115 — CL-41, **격자 수렴 미확인**).
`step3_sigma.py` 의 **구-스탬프 게이트는 `d/vox ≥ 2`** 다.

| 대상 | 필요한 vox | 그때 RAM (🧮 dof ∝ vox⁻³ 외삽; 리포 실측 0.115 → 35.6 GB, 투영 0.10 → 54 GB) |
|---|---|---|
| 우리 PTFE 0.25 µm | **≤ 0.125 µm** | **≈ 22 GB** — **가능** (이미 CL-41 에서 돌았다) |
| Matthews Fig 3B 중앙 ≈34 nm | **≤ 0.017 µm** | **≈ 11 TB** |
| Matthews finest 30 nm | **≤ 0.015 µm** | **≈ 16 TB** |

> ★★★ **판정: PTFE 웹의 미세 절반은 원리적으로 미해상이고, 격자로 닫히지 않는다.**
> 필요한 RAM 이 **TB 급**이라 "더 조이면 된다"가 답이 아니다.
> 이것은 오늘 **Koo(A14) SWCNT sheath 에 내린 판정과 같은 부류** — *"표현(representation) 문제이지
> 격자(resolution) 문제가 아니다"* — 이고, 처방도 같다: **부피를 pin 하고(add_pvs),
> 이득을 격자 불변량으로 재정의하고, 절대 표현부피를 근거로 삼지 않는다.**
> ⚠ 차이 하나: sheath 는 **표면 스킨**이라 면적으로 pin 할 수 있는데, PTFE 웹은 **부피상**이라
> pin 대상이 다르다.  같은 결론, 다른 손잡이.

### 10.3 축 ③: **기전 앵커 — 우리가 새로 얻은 것**

| 우리 코드 | 이 논문이 주는 것 | 등급 |
|---|---|---|
| `seed_fibres(vol_conserve=True)` — 등체적 인발, d ∝ √(V/L) | **crystallite unwinding** 기전 = 등체적 인발.  Fig 4B inset 이 **"작은 가닥 다발"** 임을 보임 | ✅ **방향 앵커** (분포 파라미터는 여전히 미앵커) |
| `vol_cv = 0.6` (초기 노드 부피 CV) | **PTFE 원료 100–200 µm 분말** = 2배 크기 스팬 | 🔶 **간접** — 원료 CV ≈ 0.2–0.3 을 시사, 우리 0.6 은 **더 넓다** |
| `branch_frac = 0.5`, `branch_n = 2` | Fig 4C 에서 **한 primary 에 화살표 2개** = 2차 분지 2가닥.  §3.1 "process can repeat" | ✅ **`branch_n=2` 는 그림과 정합** |
| `branch_vol = 0.3`, `branch_len = 0.5` | ⛔ **자식/부모 부피비·길이비 수치 없음** | ⛔ **미앵커** |
| `--ptfe-am-bind` (기본 0.5, §F1) | ★★ **이 논문의 핵심 기전 자체** — PTFE 는 **NMC 표면 거칠기**에 anchor 된다.  Fig 3B "anchored to the NMC surface at numerous points" | ✅ **방향 앵커 신규 획득** — 더 이상 순수 §F1 이 아니다 |
| `nucleate` = **탄소** 유인점 (CBD 공존) | 🔶 **기전상 1차 anchor 는 AM 표면이지 탄소가 아니다.**  다만 Fig 6A 는 CNF 가 PTFE 망에 **얽혀 있음**을 보임 | ⚠ **우선순위 재고 근거** — AM 몫을 낮게 잡을 근거가 약해졌다 |
| `curl ≈ 0.40` (엉킨 웹) | 🔶 Fig 3A 의 실은 anchor 사이에서 **팽팽하고 곧다**.  "tangled" 보다 "taut span" 에 가깝다 | ⚠ **curl 0.4 는 이 그림 기준 다소 높다** (다만 압력 의존 규약이라 단정 금지) |
| `PTFE_FIBRIL = {ballmill 1.0, thinky 1.0, handmix 0.45}` | ⛔ **전단 스윕 없음.**  단 기전이 **"전단이 반복될수록 더 가늘어진다"** 이므로 **단조 방향은 지지** | ⛔ **크기 §F1 유지 · 방향만 강화** |

### 10.4 축 ④: **PTFE 가 전자망을 어떻게 막는가** — 우리 CL-49 와의 대조

- 우리 실측(CL-49, arm 0): **PTFE 를 절연체로 스탬프하면 σ_e(SBE) 73.0 → 54.6 mS/cm (−25 %)**,
  σ_e 비 **1.1263 → 1.3092**.  "문헌의 3,000배 붕괴는 **표면 코팅** 효과라 복셀이 못 본다"고 적었다.
- **이 논문이 그 서술을 형태론적으로 뒷받침한다**: 건식 PTFE 는 **선(線)** 이고 **AM 표면을 거의
  덮지 않으며(minimal obscuration) 기공을 막지 않는다**(Fig 3A).  덮는 것은 **슬러리 PVDF**(Fig 3C).
  ⇒ **1 wt% 급 건식 PTFE 에서 "표면 코팅형 차단"은 형태론적으로 일어나지 않는다.**
  ⇒ 우리 **−25 %(부피 점유형 차단)** 가 **1 wt% 대역에서는 오히려 옳은 그림**일 가능성이 커진다.
  ⚠ 단 Lee 2025 의 3,000배 붕괴는 **PTFE 0.5 → 5 wt%** 구간이다 — **함량이 다르면 형태도 다르다**
  (본편도 LiB 문헌이 5 wt% 를 쓴다고 지적).  ⇒ **밴드로 기록**: *1 wt% = 선형, 저차단 · 5 wt% = 미지,
  코팅형 차단 가능* — **이 논문은 함량 스윕이 없어 그 전이를 못 봉한다**(§8 n/a).
- ⚠ **소재계 경고**: 여기는 액체계라 PTFE 가 막는 것은 **전자망**뿐이고 **이온은 공극의 액체**가
  나른다.  우리 황화물 침대에서는 PTFE 가 **양 망을 다 막는다** — R_ion 50 vs 114 Ω 을
  우리 σ_ion 으로 옮기면 **부호가 뒤집힌다.** **절대 전이 금지.**

### 10.5 축 ⑤: frame[4] / frame[5] 판정

- **frame[5] (분업)**: 이 논문은 **실험 전용, 시뮬레이션 0**.  ⇒ 경쟁자가 아니라 **앵커**다.
  **자기가 소유한 반쪽 = 형태(morphology) + 기전(mechanism)** — 우리 **MPM 반쪽**의 검증 상대.
  **못 가진 반쪽 = 정량 분포 · 수송 절대값 · porosity** — 그건 **우리 DEM/STEP3 반쪽**이고,
  **이 논문은 그 자리를 비워 둔 채로 끝난다.**  ⇒ **frame[5] 의 6번째 독립 확증**
  (Varkey · Bazzoun · Duquesnoy · Nam · Luan 에 이어).
- **frame[4] (교차검증)**: 우리 PTFE 표현을 **이 논문에 맞춰 튜닝하면 안 된다.**
  ⇒ 올바른 사용은 **"우리 (0.25, 40) 이 논문의 [10s nm, 수 µm] × [>50 µm, 100s µm] 구간
  **어디에 놓이는지 라벨**하는 것"** 이고, 그 라벨이 §10.1(b)/§10.2 다.
  **일치를 만들려고 값을 바꾸는 것은 순환**이다.

---

## 11. 인용 가능 문장 (deck / manuscript / SI)

- "건식 NMC 전극의 PTFE 바인더는 **지름 수 µm · 길이 수백 µm 의 primary 피브릴이 반복 인발되어
  수십 nm 이하까지 갈라지는 계층 망**을 이루며, 이 계층은 슬러리 PVDF 의 이끼형 CBD 와
  형태적으로 구분된다 [S7]."
- "PTFE 피브릴화는 **NMC 표면 거칠기에 PTFE 표면 결정자가 맞물려 anchor 되고, 이어지는 전단에서
  결정자가 풀려나오며(unwinding) 실이 뽑히는** 과정으로 설명된다 [S7]; 이 anchor–draw 기전은
  본 연구가 PTFE 씨앗을 **AM 표면에서 핵생성**시키는 규약의 근거다."
- "고해상 SEM 은 건식 전극에서 **활물질 표면 가림이 최소이고 기공 막힘이 없음**을 보이며,
  이는 3전극 EIS 의 **이온확산 저항 감소(114 → 50 Ω)** 와 정합한다 [S7]."
- "PTFE 피브릴은 **양극 전위(2.5–4.2 V vs Li)에서 30 사이클 후에도 관찰**되어 셀 조립·사이클을
  견딘다 [S7]" (⚠ 음극 전위 안정성은 이 논문 밖 — Zhang 2022 의 carbyne 환원 주장은 미해결).
- ⚠ **조건 붙여서만**: "건식 전극은 율이 올라갈수록 이득이 커져 **2C 에서 슬러리 대비 방전용량이
  약 150 % 증가**했다 (반쪽셀 vs Li, 2.5–4.2 V, 100–110 µm, 30–32 mg cm⁻²) [S7].
  **단 그 지점의 절대 용량은 56 vs 23 mAh g⁻¹ 로 두 전극 모두 0.1C 대비 34 % / 15 % 수준이며,
  ≤1C 의 이득은 +4.5 ~ +27 % 다.**"
- ⛔ **쓰면 안 되는 문장**: "Matthews 가 PTFE 피브릴 지름을 0.25 µm 로 보고했다" —
  **그런 값은 이 논문에 없다.**

---

## 12. ⚠ 주의 / 한계 (over-claim 방지)

1. **소재계 게이트 — 액체 LIB.**  이온상이 반전(공극 = 이온 경로).  **σ·R·용량 절대값 전이 금지.**
   전이 가능한 것은 **형태 · 기전 · 공정 · 방법론**뿐.
2. **정량 형태 데이터가 없다.**  분포·n·측정법이 전무하므로 **이 논문은 우리 `PTFE_D` 를
   좁히지 못한다.**  좁히는 것은 **구간뿐**: [수십 nm, 수 µm].
   ⇒ **요청 ①의 답은 "구간은 준다, 값은 안 준다"** 이고, 이것은 실망이 아니라 **정직한 경계**다.
3. **우리 디지타이즈는 상한이다.**  300 dpi 래스터가 네이티브 8–163 nm/px 를 강제해
   **하한이 절단**된다.  Fig 3B 중앙 34 nm 도 **4 네이티브 px** 에 불과하다.
   **어떤 디지타이즈 값도 물리 상수로 인용 금지.**
4. **PTFE 함량 1 wt% 한 점.**  함량↔형태 곡선이 없어 **우리 SBE 1.0 ↔ DBE 0.5 대조를
   이 논문으로 설명할 수 없다** (요청 ⑤ → **불가**).  그 자리는 Lee 2025(0.2–5 wt% 스윕) 몫이다.
5. **primary 는 다발(bundle)이다** (Fig 4B inset).  우리 단일 실린더 표현은 **속을 채운 원기둥**을
   가정하므로 **같은 겉지름에서 부피를 과대**할 수 있다.  다발 충전율은 **미보고 → n/a**.
6. **"without breakage"** 는 이 논문의 **관찰 기반 주장**이지 측정이 아니다.  Hippauf 2019 는
   압축 중 파단을 주장한다 — **두 주장이 공존**하고, 조건(황화물 복합양극 고압 vs LiB 캘린더)이 다르다.
7. **RAM 외삽(TB급)** 은 `dof ∝ vox⁻³` 가정의 **DERIVED** 값이다.  실측이 아니다.
8. **EIS 를 Ω·cm² 로 바꾸지 말 것** — PAT 셀 전극 면적 미기재.  코인셀 14 mm(1.539 cm²)를
   대입하는 것은 **셀이 달라 오류**다.
9. **캘린더 라인압 50 N/mm 를 MPa 로 환산하지 말 것** — 접촉폭(nip width) 미기재.
10. 논문 내부 오식(§9)을 그대로 옮기지 말 것 — 특히 **mAh/cm² ↔ mg/cm²**.

---

## 13. 실행 항목 (우리 백로그로)

| # | 항목 | 근거 | 상태 |
|---|---|---|---|
| M-1 | **`additives.py:38` 주석 정정** — `0.25 / 40.0` 옆에 **"두 출처 어느 쪽도 이 값을 보고하지 않음; Matthews 는 [10s nm, 수 µm]×[>50 µm, 100s µm] 구간만 제공"** 을 명시하고, 앵커된 조각(`branch to 10s nm`, `spanning tens of NMC`)과 미앵커 조각(Ø, L)을 **분리 표기** | §10.1(a) | ⬜ 제안 (코드 변경은 사용자 승인 후) |
| M-2 | **`PTFE_L = 40 µm` 재검토** — 논문 하한(>50 µm)보다 짧다.  RVE 50 µm 와 같은 크기라 **길이를 늘리면 주기경계 관통 표현**이 필요 | §10.1(b)-2 | ⬜ 논의 필요 (RVE 크기와 결합된 결정) |
| M-3 | **`--ptfe-am-bind` 를 §F1 에서 "방향 앵커됨"으로 승격** — 기전 자체가 AM-표면 anchor 다.  크기(0.5)는 여전히 미앵커 | §10.3 | ⬜ 문서 갱신 |
| M-4 | **PTFE 표현부피 원장** — SDCP CL-25 와 같은 방식으로 `PTFE 표현부피/참부피` 를 vox 0.15/0.125/0.115 에서 실측 (rasterize-only CPU).  **부호가 뒤집히는 구간**(d ≈ vox)을 실측으로 확인 | §10.1(b)-3 | ⬜ 저비용, 권장 |
| M-5 | **CL-49 후속 — 함량 밴드 라벨** "1 wt% = 선형·저차단(Matthews 형태 지지) / 5 wt% = 코팅형 차단 가능(Lee 2025)" 를 `comparison_vs_ours_DEM.md` §B 에 등재 | §10.4 | ⬜ |
| M-6 | **`curl = 0.40` 재검토** — Fig 3A 는 anchor 간 **팽팽한 span**.  다만 압력의존 규약이라 단독 판단 금지 | §10.3 | 🔶 관찰만 |
| M-7 | 이 논문 Fig 8 데이터에 우리 **DRT(`eis_drt_ica.py`)** 를 얹어 R_cont/R_CT/R_ion 3분해가 재현되는지 **방법 대조** | §7 | ⬜ (데이터 디지타이즈 필요) |

---

## 14. ★ 가장 날카로운 인사이트 3

1. ★★★ **우리 PTFE 지름은 "값"이 아니라 "두 자릿수 분포를 한 점으로 접은 기하평균"이다.**
   Matthews 는 [수십 nm, 수 µm] = **≈100×** 스팬을 보고하는데 우리는 0.25 µm 한 점(등체적 인발로
   실효 CV ≈ 0.36 → 약 4× 스팬)을 쓴다.  **이 논문은 그 점을 좁혀 주지 않고 대신 우리가 무엇을
   접고 있었는지를 정확히 알려 준다.**  가장 값진 부산물: **AR ≈ 160 만이 방어 가능**하고
   **(Ø, L) 쌍은 아니다** — 같은 AR 에서 논문의 (2 µm, 300 µm) 과 우리 (0.25, 40) 은 8배 다르다.

2. ★★★ **미세 절반은 격자로 닫히지 않는다 — TB 급이다.**  finest(30 nm)를 구-스탬프 게이트
   (`d/vox ≥ 2`)로 해상하려면 vox ≤ 0.015 µm, 곧 **≈16 TB**(dof ∝ vox⁻³ 외삽).
   ⇒ **Koo sheath 판정과 같은 부류: 표현 문제, 격자로 안 닫힘.**  그리고 그 반대편에
   **CL-25 의 부호 반전**이 붙는다 — 30 nm 를 1셀로 찍으면 **32–45× 과대**, 우리 0.25 µm 를
   1셀로 찍으면 **2.2× 과소**.  **표현부피 오차의 부호가 지름에 따라 뒤집힌다.**

3. ★★ **형태론이 우리 CL-49 를 지지한다 — 그러나 함량 밴드 안에서만.**
   건식 1 wt% PTFE 는 **선(線)** 이고 표면을 안 덮고 기공을 안 막는다(Fig 3A).
   ⇒ **부피 점유형 차단(−25 %)** 이 그 대역에서 옳은 그림일 가능성이 커졌고, Lee 2025 의
   3,000배 붕괴는 **다른 함량(5 wt%)의 다른 형태** 로 분리해 라벨해야 한다.
   ⚠ 그리고 **RVE 안에 primary 가 한 가닥도 온전히 안 들어간다** (L 100s µm > box 50 µm) —
   우리 침대의 PTFE 인구는 물리적으로 **secondary/tertiary 조각 표본**이라고 읽어야 한다.

---

## 15. 같은 서랍 안 관련 카드 (교차참조)

| 카드 | 관계 |
|---|---|
| **`lee2025_dual_fibrous_ptfe_dry_electrode`** — Kwon-Hyung Lee / Tae-Hee Kim / **Gyujin Song**, *Energy Environ. Sci.* **2025, 18, 8446–8461** (DOI `10.1039/D5EE03240G`, KIER 울산) | ★★★ **자매 카드 — `additives.py:38` 이 인용하는 다른 한 출처.  같은 날(2026-09-04) 별도 digest.  §16 이 둘을 겹친 종합 판정이다.  반드시 함께 읽을 것.** |
| `lee2025_corolling_dryprocess_lpscl_ptfe` | **황화물** LPSCl + PTFE 건식, **0.2–5 wt% 스윕** — 이 논문이 못 주는 **함량 축**을 소유.  §10.4 밴드의 반대편 |
| `liu2025_dry_processing_high_energy_li_batteries_review` | 건식공정 총설.  **본편을 ref [64] 로 인용**("AM 거친 표면이 먼저 바인더를 anchor, 그 다음 상호 전단력으로 PTFE 가 fibrous structure 로 fibrillate") ⇒ 우리가 총설에서 간접 인용하던 기전의 **1차 출처가 이 카드** |
| `nam2026_dpe_microstructure_review` | DPE 미세구조 리뷰.  **본편을 ref 122 로 인용**(PTFE 점탄성 3-regime) + Fig 4e ref 88 에 **dual-fibrous(자매 논문)** 언급 |
| `koo2026_swcnt_sheath_thick_electrode` (A14) | ★ **같은 판정 유형** — sub-voxel 나노상은 **표현 문제이지 격자 문제가 아니다**.  §10.2 의 논거 형제 |
| `zhang2026_dryprocess_electrode_architecture_cell_level` | 건식 **VGCF–PTFE 전단 커플링** CGMD.  **전단을 실제로 시뮬레이션**하는 유일한 이웃 — 본편의 기전을 계산으로 옮기려면 그 카드의 방법이 출발점 |
| `wang2026_dryprocess_thick_cathode_failure_ncm94` | 건식 후막 **황화물** 실패기전 + DRT.  본편의 EIS 3분해와 **같은 목적, 다른 도구**(DRT vs spectroscopic capacitance) |
| `mun2025_dry_electrode_technology_assb_review` · `zhang2026_dryprocess_electrode_architecture_cell_level` | 건식 공정 축의 상위 지도 |

---

## 16. ★★★ 자매 카드와 겹친 **종합 판정** — 두 논문을 합쳐야 감사가 닫힌다

`lee2025_dual_fibrous_ptfe_dry_electrode` (EES 2025, 18, 8446) 는 **Fig S2c 에 N=100 이미지 분석
치수표**를 싣는다 — **이 논문에 없는 바로 그 정량 분포**다.  둘을 겹치면:

| 우리 상수 | **Lee 2025** (D5EE03240G, N=100 정량) | **이 카드** (1336344, 구간 서술만) | 종합 |
|---|---|---|---|
| `PTFE_D = 0.25 µm` | ✅ **rope 평균 Ø 0.248 µm** (0.8 % 차) | ⛔ 값 없음 (구간 `10s nm ~ 수 µm` 안) | ✅ **Lee 가 앵커한다** |
| `PTFE_L = 40 µm` | ❌ rope 평균 **6.689 µm**, 최장 **14.257 µm** → **6.0 / 2.8배 과대** | ⛔ 값 없음 · **방향도 반대** (primary "100s µm", Fig 2A ">50 µm" ⇒ 40 은 그 **하한보다 짧다**) | ❌ **어느 쪽도 앵커 못 하고, 두 논문이 서로 반대편으로 어긋난다** |
| `AR ≈ 160` | ❌ 실측 **26.96 / 26.97** → **5.9배 과대** | 🔶 간접 지지 (자기 쌍이 AR 33–500) | ⚠ **계층(tier) 의존 — 어느 층을 보느냐로 갈린다** |
| (단일 굵기) | **두 집단**: fibre **Ø 0.048** / rope **Ø 0.248** (5.17배) | **계층 연속체**: 수십 nm → 수 µm (≈100배) | ⚠ 우리 단일 개체군이 못 담는 축 |

★★★ **진단 — 우리 `(0.25, 40)` 은 키메라다.**
**지름은 Lee 의 가는 계층(rope 0.248 µm)에서, 길이·AR 은 Matthews 의 굵은 계층(100s µm)에서 왔다.**
두 논문은 **같은 PTFE 망의 서로 다른 층**을 보고 있고 절대 스케일이 **8–10배** 다르다.
**한 쌍의 (Ø, L) 로는 원리적으로 둘 다 못 맞춘다.**

⚠ **두 논문의 한계가 정확히 거울상이라는 점을 함께 적을 것** (어느 쪽도 "틀린" 게 아니다):
- **이 카드(Matthews)** 는 **지름이 인쇄 래스터에 절단**된다 (300 dpi → 네이티브 8–163 nm/px, §4.5)
  — 그래서 **지름 분포를 못 준다**.  대신 **저배율 시야가 넓어 길이(100s µm)를 본다.**
- **Lee 2025** 는 **고배율 시야에서 N=100 을 재** 지름을 정밀하게 주지만, **시야가 길이를 절단**한다
  (최장 14.257 µm = 프레임 크기 급).  ⇒ **길이 통계는 시야 상한에 걸려 있다.**
⇒ **정직한 종합**: **Ø 는 Lee, L 은 Matthews 를 쓰되 "다른 계층의 값을 섞고 있다"는 라벨을 붙인다.**
그리고 진짜 해법은 값 하나를 고르는 것이 아니라 **2-계층(또는 분포) 표현으로 가는 것**이다 (§13 M-2).

---

## 🗨️ Q&A 로그

**Q (2026-09-04, 사용자). `additives.py` 의 `PTFE_D=0.25 µm` 가 이 논문에서 나오나?**
**A. 아니다.**  이 논문이 주는 피브릴 지름 진술은 4개뿐이고(§4.4 표) 전부 **구간**이다 —
`수 µm`(primary) · `<1 µm`(Fig 2A) · `수십 nm 이하`(finest).  **0.25 µm 라는 값은 본문·초록·결론·
캡션 어디에도 없다.**  분포도·히스토그램·n·평균±sd·이미지 분석 절차도 **전무**하다.
반면 주석의 **`branch to 10s nm`** 과 **`spanning tens of NMC`** 는 **이 논문의 문장 그대로**이므로,
주석은 "형태 서술은 이 논문, 숫자는 우리 선택" 으로 **분리 표기**하는 것이 맞다 (M-1).

**Q. 자릿수는 맞나 — nano-fibril 인데 우리는 250 nm 다.**
**A. 제목의 "nano" 는 계층의 아래 끝만 가리킨다.**  위 끝은 **수 µm**(마이크로)다.
우리 250 nm 는 **위 끝의 1/10, 아래 끝의 8배** — 두 인구 사이의 골짜기다.
Fig 6A 의 내부 자(stated CNF Ø 150–200 nm)로 재면 그 프레임의 PTFE 는 **≈30–70 nm** 로
**CNF 보다 가늘다** ⇒ **개수 기준으로 우리 값은 위쪽으로 벗어나 있다.**
다만 **부피 기준으로는 primary 가 압도**하므로 우리 값은 **아래쪽으로도 벗어나 있다.**
**논문이 그 배분을 안 주므로 어느 쪽으로 옮길지 결정할 근거가 없다** — 그래서 현행 값을
"두 자릿수 분포의 기하평균" 이라고 **라벨**하는 것이 지금 할 수 있는 가장 정직한 조치다.

**Q. 길이 40 µm 는?**
**A. 논문 진술보다 짧다.**  Fig 2A 가 **>50 µm**, primary 가 **100s µm** 다.
게다가 **primary 길이가 우리 RVE(50 µm)를 2–10배 넘어** RVE 안에 한 가닥도 온전히 안 들어간다.
⇒ 길이를 올리는 것은 **RVE 크기·주기경계 규약과 묶인 결정**이라 단독으로 못 바꾼다 (M-2).
