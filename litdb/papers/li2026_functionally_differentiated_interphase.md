<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     서식 기준 = papers/nolan2021_garnet_cathode_coating.md (1저자 지정)
     2026-09-12 신규 작성 (litdb-curator):
       ① 서지가 요청서에 "미확인" 으로 왔으나 **본문 PDF 메타데이터에서 전량 확정**했다:
          *Journal of Energy Storage* **181** (2026) 124529 · DOI 10.1016/j.est.2026.124529 ·
          Elsevier · 수신 2026-06-10 / 수정 2026-08-07 / 수락 2026-08-26 / 온라인 2026-09-10.
          요청서의 저자·소속(Central South University)은 전부 맞았다.
       ② 크로핑 그림 **6장 전부(Fig. 1–6)를 실제로 봤다.** SI 는 `.docx` 라 추출기가 못 건드려
          그림 이미지는 없고, **본문은 zipfile→word/document.xml 파싱으로 206 문단 전수 확보**
          (Fig. S1–S12 캡션 · Table S1 · Table S2 13행 전부 · DFT 방법절 · 합성 레시피).
          `Fig. 1g`·`Fig. 1m` 은 4× 확대 재판독했다.
       ③ 본문↔그림/표 어긋남 **8건** 발견(§10). 그중 **§10-1(초록 수치)** 은 우리가 이 논문을
          인용하는 순간 바로 걸린다 — 초록의 `77.1 mAh/g over 1000 cycles` 는 1000번째 사이클
          용량이 아니라 **1C 첫 용량**이고, 진짜 1000번째는 ≈47 mAh/g 다 (Table S1 61.2 % 로 검산).
       ④ ★ 이 편의 우리 쪽 핵심은 성능이 아니라 **"Li₃P 를 피하려고 Li₃N 을 골랐는데, 저자 자신의
          `Fig. 1g` 가 Li₃N 을 다섯 코팅 중 가장 좁은 갭으로 그린다"** 는 자가당착이다 (§7c).
          우리 `sei_products.json` 분류(conductor < 2 eV)를 그대로 적용하면 Li₃N 도 `conductor-LEAK` 다.
       ⑤ 독립 재분석 2건(§12): **CCD 값 6개가 전부 0.199 mA cm⁻² 의 정수배** = 계단 분해능이
          곧 오차이고 4자리 유효숫자는 허수다 · **Fig. 5 y축 단위 V 는 mV 여야 한다**(ASR 검산).
       ⑥ ⛔ 공유 파일(INDEX.md · comparison_vs_ours.md)은 **건드리지 않았다** — 네 편이 동시에
          돌고 있다. 합칠 텍스트는 이 파일 맨 끝 `<!-- MERGE-BLOCK -->` 에 완성형으로 둔다. -->

# Functionally differentiated composite interphase enables stable sulfide-based all-solid-state lithium metal batteries — Xuebao Li, Zhuangzhi Wu, Dezhi Wang (*Journal of Energy Storage* **181** (2026) 124529)

> slug `li2026_functionally_differentiated_interphase` · DOI `10.1016/j.est.2026.124529` · type `실험 주도 + 얇은 DFT 스크리닝 (VASP/PBE 계면 슈퍼셀 11개 · DOS 7종 · CI-NEB 6종 — 전부 "성분 고르기" 용도. 자체 실험 = SEM/EDS·XPS·AFM·CCD·대칭셀·풀셀)` · PDF `litdb/inbox/115. Li_FunctionallyDifferentiatedCompositeInterphase_MAIN.pdf` (본문 11 pp, 그림 6장, 표 0장, refs 47) + `115. Sup) …_SI.docx` (Fig. S1–S12 · Table S1–S2 · 합성/전기화학/DFT 방법절) · digested `2026-09-12` · status ✅ · 태그 **[외부]**

> elements: Li, F, Cl, Br, N, O, P, S, Zr
> methods: DFT, NEB, DOS, XPS

> **저자**: **Xuebao Li**ᵃ, Chao Zhaoᵃ, Yueqing Pengᵃ, Kun Zengᵃ, Shijie Hanᵃ, Zekai Zhangᵃ, **Zhuangzhi Wu\***ᵃ, **Dezhi Wang\*\***^(a,b) — ᵃ School of Materials Science and Engineering, **Central South University** (中南大学), Changsha 410083 · ᵇ **State Key Laboratory of Powder Metallurgy**, 동 대학. 단일기관 7인. 교신 3인(lixuebao@ / zwu2012@ / dzwang@csu.edu.cn).
> **지원**: NSFC **52374407** · 계산자원 **Central South University HPC Center**. 데이터 *"available on request"*(공개 저장소 없음).
> **키워드(저자 지정)**: Sulfide solid electrolyte · All-solid-state lithium metal battery · **Density functional theory** · Interfacial engineering · Composite interphase · Lithium dendrites.

---

## 0. 이 digest 를 읽는 법 — 범위부터

### 0a. 1저자가 이 편에 물은 여섯 가지 — 답 먼저

| # | 물음 | 답 (근거 절) |
|---|---|---|
| **1** | 서지가 확정되나 | 🟢 **전량 확정.** *J. Energy Storage* **181**, 124529 (2026), DOI 10.1016/j.est.2026.124529. PDF 메타데이터(`subject` 필드) + 각 쪽 하단 러닝헤더 두 군데에서 독립 확인. "미확인" 으로 남길 것 없음 |
| **2** | 어떤 계면상을 만들고 무엇으로 "기능 분화" 를 주장하나 | **3성분 · 3역할**: **LiF** = 전자차단/부동태 · **LiCl/LiBr** = 계면 피복 연속성·균질화 · **Li₃N** = 빠른 Li⁺ 수송. 제작 순서가 곧 적층 순서라는 주장이고(Li 쪽부터 LiF→LiCl/LiBr→Li₃N), 도해는 `Fig. 5g`. ⛔ **다만 수직 분리는 증명되지 않았다 — 저자 자신이 본문에서 자인한다**(§3e·§10-3) |
| **3** | 우리 원장 산물(Li₃PO₄·Li₂SO₄·Li₂S·LiCl·Li₃P)이 관측되나 | 🔴 **다섯 중 관측 0건.** `LiCl` 은 나오지만 **분해산물이 아니라 THF 용액에서 *뿌린* 코팅**이다. `Li₂S`·`Li₃P` 는 **서론 한 문장의 인용**일 뿐 측정되지 않았고, `Li₃PO₄`·`Li₂SO₄` 는 등장조차 않는다. 결정적으로 **이 논문에는 S 2p · P 2p XPS 가 한 장도 없고, 순환 후(post-mortem) XPS 도 0 건**이다 (§7d) |
| **4** | Li₃P 를 어떻게 다루나 (우리 `conductor-LEAK` 판정과) | 🔴 **세 번째 입장이 나왔다.** 본문 등장 **1회**(서론), 실패 이유를 *"poor **ionic** transport capability"* 로 돌린다 — 우리(전자 누설) 와도, `[Xiao20Rev]`(부동태 산물) 와도 다르다. 그리고 **대체재로 고른 Li₃N 이 저자 자신의 `Fig. 1g` 에서 다섯 코팅 중 갭이 가장 좁다**(figure-read ≈1.1 eV) — 우리 기준(<2 eV = conductor)이면 **Li₃N 도 `conductor-LEAK`** 다 (§7c, §10-5) |
| **5** | 계산이 있나 | 🟡 **있다, 그러나 얇다.** VASP/PBE/PAW/ENCUT 520 eV, 계면 슈퍼셀 **11개**, DOS **7종**, CI-NEB **6종**. ⛔ **k-메시 0 · 슈퍼셀 크기 0 · 진공층 0 · vdW 0 · 스핀 0 · NEB 이미지 수 0 · 무질서 처리 0 · 밴드갭 숫자 0**. SI 가 정의한 계면에너지 γ(식 S1)는 **값이 본문·SI 어디에도 없다**(사장된 방법) (§4·§10-2) |
| **6** | 우리가 이식할 수 있는 것 | **수치는 0.** 이식 가능한 것은 **① 3역할 분할이라는 *서술 틀*** ② **Li₃N 딜레마라는 반례** ③ **CCD 계단 보고 규약의 반면교사**(§12a) 뿐 |

### 0b. 그림 판독 범위 (정직 고지)

- 크로핑 **6/6 장 전부 실제로 봤다**: `Fig. 1`·`Fig. 2`·`Fig. 3`·`Fig. 4`·`Fig. 5`·`Fig. 6`. 안 본 그림 **없음**.
- `Fig. 1g`(DOS 7패널)·`Fig. 1m`(LPSCl NEB)은 **4× 확대 재판독**했다 — 이 digest 의 갭·장벽 판독은 그 확대본 기준이다.
- **SI 그림(S1–S12)은 이미지로 보지 못했다** — SI 가 `.docx` 라 `extract_figures.py` 대상이 아니다. SI 는 **텍스트만** 전수 확보(캡션·Table S1·Table S2·방법절). 따라서 **S1–S12 에 대한 서술은 전부 "캡션 + 본문 인용" 이고 우리 판독이 아니다.**
- 그림에서만 읽은 값은 전부 **`figure-read ≈`** 로 표시했다. 본문 인쇄값과 섞지 않았다.

---

## 1. 한 줄 요약

**황화물(LPSCl)/Li 금속 계면의 실패는 한 가지 원인이 아니라 "전자 부동태 · 이온 수송 · 계면 균질성" 세 축의 불균형이므로, 한 물질에 셋을 다 맡기지 말고 LiF(전자차단)+LiCl/LiBr(피복 균질화)+Li₃N(빠른 Li⁺)을 순차 습식 처리로 겹쳐 쌓자** — 그 결과 대칭셀 CCD 가 0.398 → **3.581 mA cm⁻²**(9×), 0.398 mA cm⁻² 에서 **800 h** 안정, NCM‖LiZrClO–LPSCl‖코팅Li 풀셀이 0.1 C **215.0 mAh g⁻¹**(ICE 91.0 %)·1 C **1000 사이클**(⚠ 1000번째 용량은 초록이 말하는 77.1 이 아니라 **≈47 mAh g⁻¹**, §10-1).

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 저널·권·쪽 | *Journal of Energy Storage* **181** (2026) **124529** (Research Papers) |
| DOI | `10.1016/j.est.2026.124529` |
| 일정 | 수신 **2026-06-10** / 수정 **2026-08-07** / 수락 **2026-08-26** / 온라인 **2026-09-10** |
| 저작권 | © 2026 Published by **Elsevier Ltd.** (2352-152X) |
| 분량 | 본문 **11 pp**(참고문헌 2 pp 포함) · 그림 **6장** · 표 **0장** · refs **47** |
| SI | `.docx` — 실험절(합성·코팅·전기화학·물리분석) + **DFT 방법절 §1.4** + Fig. **S1–S12** + **Table S1**(풀셀 5샘플 × 4 rate) + **Table S2**(문헌 13편 성능비교) + SI refs 13 |
| 데이터 공개 | *"Data will be made available on request."* — 저장소·raw 없음 |
| 계 (계산) | **Li₆PS₅Cl (LPSCl)** (100) 면 + Li 금속 + 코팅 5종(LiF·LiCl·LiBr·Li₂O·Li₃N) |
| 계 (실험) | SE = **Li₆PS₅Cl**(자체 합성, 볼밀 300→400 rpm, 500 ℃ 8 h) · 촉매전해질 = **Li₁.₇₅ZrCl₄.₇₅O₀.₅ ("LiZrClO", 자체 합성)** · 양극 = **NCM811 : LiZrClO : VGCF = 70:27:3** · 음극 = Cu 박에 압연한 **Li 금속** |
| 셀 구성 | **이중층 전해질**: 양극쪽 할라이드 40 mg + 음극쪽 황화물 80 mg, 436.7 MPa 로 치밀화 → Li 부착 후 **10 MPa** 로 밀봉. **mold-type cell, 가압 상태** |
| 시험 조건 | 풀셀 **2.8–4.3 V**, 0.1→0.2→0.5 C 활성화 후 **4사이클째부터 1 C**. **1 C = 180 mAh g⁻¹** |

### 2a. 샘플 이름표 (이 논문을 읽는 데 반드시 필요)

| 라벨 | 처리 | 주 성분 |
|---|---|---|
| **LI** | 미처리 Li (Cu 박 압연) | 천연 Li₂O/LiOH/Li₂CO₃ 피막 |
| **LO** | 추가 산화시킨 Li | Li₂O·LiOH (불균일) — **설계에서 탈락**(§3b) |
| **LF-1 … LF-6** | **LiFSI@DME** 0.0025–0.03 M, 80 ℃ 1 h 침지 | **LiF-rich** (+ –SO₂F·NOₓ 잔류). 최적 = **LF-4**(0.01 M) |
| **LF-D** | LiF 를 DME 에 직접 녹여 적하 | 물리적 침적 LiF — **실패 대조군** |
| **BC-1 … BC-4** | **LiCl/LiBr(1:1)@THF** 0.0025–0.01 M, 200 μL 적하 | LiCl + LiBr. 최적 = **BC-3**(0.0075 M) |
| **LN-TMEDA** | **TMEDA**(테트라메틸에틸렌다이아민) 80 ℃ 20 min 침지 | **Li₃N** + –NR₃ 잔류 |
| **LN-NM** | **NM**(나이트로메탄) 80 ℃ 10 min 침지 | Li₃N + C–N/NOₓ 부산물 다량 — **탈락** |
| **3LFCBNL-1** | **LF-4 → BC-3 → TMEDA 붓칠** 3단 순차 | LiF + LiCl/LiBr + Li₃N. **주인공** |
| **3LFCBNL-2** | 3단인데 마지막을 **NM** 으로 | 동일 3성분, 품질 열위 |

---

## 3. 핵심 물성 (수치)

### 3a. DFT — Li⁺ 이동장벽 (CI-NEB, `Fig. 1h–m`) ★

> ⚠ **전부 본문 인쇄값**이다(그림 안 라벨과 일치 확인). 단위 eV.

| 상 | 장벽 (eV) | 그림 | 경로 길이 (figure-read ≈, Å) | 판독 메모 |
|---|---|---|---|---|
| **Li₃N** | **0.0103** | `Fig. 1j` | ≈1.33 | 🔴 마커 **4개**뿐 · 시작 0 → 끝 **−0.0082 eV**(끝점 비축퇴) · 장벽이 **자기 힘 수렴한계 안**(§10-4) |
| **Li₂O** | **0.2326** | `Fig. 1h` | ≈2.15 | 마커 6개, 대칭적 |
| **LiCl** | **0.4800** | `Fig. 1l` | ≈3.75 | 마커 6개, 대칭적 |
| **LiBr** | **0.5615** | `Fig. 1k` | ≈3.75 | 마커 7개, 대칭적 |
| **LiF** | **0.6367** | `Fig. 1i` | ≈3.05 | 마커 6개, 대칭적 |
| **LPSCl — inter-cage** | **0.2498** | `Fig. 1m` | 큰 봉우리 ≈5 Å 지점 | 🔴 전체 사슬 ≈14.5 Å · **시작 0 → 끝 −0.152 eV**(비축퇴) → **역방향 장벽은 ≈0.40 eV** |
| **LPSCl — intra-cage** | **0.0166** | `Fig. 1m` | 같은 사슬 ≈9.3→9.9 Å 구간 | 🔴 **CI 가 오르는 봉우리가 아니다** — 한 사슬 위의 *부차* 극대라 안장점이 수렴하지 않았다(§10-4) |

**본문이 이 표에서 끌어내는 결론**: *"LiF·LiCl·LiBr 은 전자절연이지만 Li⁺ 장벽이 높아 주 전도상이 될 수 없다. 따라서 **LiCl/LiBr 은 계면 균질화 성분으로 이해해야 하며 빠른 이온전도상이 아니다**."* — 이 문장은 논문 안에서 가장 정직한 대목이고, 흔한 "할라이드 SEI 가 Li⁺ 를 잘 통한다" 식 서술을 **저자 스스로 부인**한다.

### 3b. DFT — 전자구조 (DOS, `Fig. 1g`) ★ **전량 figure-read**

> 🔴 **이 논문은 밴드갭을 숫자로 한 번도 인쇄하지 않는다.** 아래는 전부 우리 픽셀 판독이고, **DOS 문턱 판독**이다 —
> 우리 집 규율상 DOS 문턱은 정본 갭이 아니다(CLAUDE.md: fixed-occ nscf 고유값만 인정). **인용 금지, 순위용.**

| 패널 | 가전자대 (eV) | 전도대 개시 (figure-read ≈) | 함의 |
|---|---|---|---|
| **Li**(금속) | −5 → +2 연속 | — (E_F 가로지름) | 금속 기준 패널 |
| **LiF** | −3.2 → 0 | **≈ +9.7** | 압도적 최광갭 → 전자차단 1순위 |
| **LiBr** | −2.8 → 0 | **≈ +7.0** | 광갭 |
| **LiCl** | −2.9 → 0 | **≈ +5.9** | 광갭 (우리 fixed-occ 6.2603 과 같은 자리) |
| **Li₂O** | −2.9 → 0 | **≈ +4.4** | 광갭 (우리 fixed-occ 4.986 과 같은 자리) |
| **Li₃N** | −2.7 → 0 | **≈ +1.1** | 🔴 **다섯 코팅 중 압도적 최협갭.** 반도체급 |
| **LPSCl** | −5 → 0 (−4.6 고립 스파이크 + −2.4~−1.4 + −0.8~0) | **≈ +3.2** (미약 시작) / **≈ +4.3** (본 개시) | ⚠ 우리 canonical comp1 **2.066 eV** 와 1 eV 이상 벌어진다 — **화해 불가**(§7b) |

**⛔ 이 그림의 치명적 한계 (우리 판독)**: 7패널이 **각자의 E_F 에 개별 정렬**돼 있다(절연체는 E_F=VBM). 즉 **공통 에너지 축이 아니다** → 이 그림으로는 **밴드 정렬(band alignment)** 을 읽을 수 없고, 계면에서 전자가 LPSCl 로 주입되는지는 **각 상의 갭이 아니라 정렬이 정한다**. 논문은 정렬을 계산하지 않았다 (§10-6).

### 3c. DFT — 차등전하밀도 (`Fig. 1a–f`)

- 모델 구성(우리 판독): **(a) LPSCl–Li 1개** + **(b)–(f) 각 코팅마다 `LPSCl–X`(위) 와 `X–Li`(아래) 2개** = **총 11개 계면 슈퍼셀**.
- 🔴 **3상 샌드위치(Li‖LiF‖LiCl/LiBr‖Li₃N‖LPSCl)는 한 번도 모델링되지 않았다.** 즉 논문의 주장인 **"기능 분화·시너지" 에는 직접 계산이 0건**이고, 성분별 개별 스크린을 **말로 합성**한 것이다 (§10-7).
- 등가면 값(isosurface, e Å⁻³) **미표기** · Bader 등 **적분값 0** · 평면평균 Δρ(z) **0**. 노랑/청록 덩어리의 "크다/보통이다" 비교는 **정량이 아니다**.
- 본문 주장 *"Li₂O·Li₃N 은 비교적 완만하고 균일한 전하 재분포"* ↔ 우리 판독: **(b)·(c) 의 LPSCl 쪽 계면 로브가 (d)·(e)·(f) 보다 오히려 크다**. 본문 서열과 그림 인상이 어긋난다 (§10-6).

### 3d. 실험 — CCD(임계전류밀도) & 대칭셀

| 샘플 | CCD (mA cm⁻²) | 0.398 mA cm⁻² 기준 배수 | 출처 |
|---|---|---|---|
| **LI (bare)** | **0.398** | 1.0× | `Fig. S8a` |
| **LF-D** (LiF 직접 적하) | **0.398** | 1.0× | `Fig. S8b` |
| **LO** (산화 Li) | **0.398** | 1.0× | `Fig. S8c` |
| **BC-3** (LiCl/LiBr) | **0.597** | 1.5× | `Fig. S10c` |
| **LN-TMEDA** / **LN-NM** (Li₃N) | **0.796** | 2.0× | `Fig. S11a,b` |
| **LF-4** (LiF-rich) | **1.393** | 3.5× | `Fig. S9d` |
| **3LFCBNL-2** | **2.188** | 5.5× | `Fig. S11d` |
| **3LFCBNL-1** | **3.581** | **9.0×** | `Fig. S11c` |

> ★ **§12a 에서 이 표를 독립 재분석한다 — 여덟 값 전부가 `0.199 mA cm⁻²` 의 정수배다.**

- **대칭셀 장기**(0.398 mA cm⁻², = bare Li 의 CCD): **LI** 는 초기 큰 이력 → **≈115 h 에 이력이 거의 소멸**(figure-read, `Fig. 5a`). 본문 표기 *"~110 h"*. ⭕ **저자가 이것을 "개선" 으로 읽지 말라고 명시**한다 — *"gradual formation of **soft-short pathways or localized electronic conduction channels**"* 가능성을 스스로 적었다. 문헌에서 흔한 "이력 감소 = 안정화" 오독을 막는 드문 정직함.
- **3LFCBNL-1**: **800 h** 동안 이력 거의 불변, 대칭적 (`Fig. 5b`). ⚠ y축 단위 문제는 §12b.

### 3e. 실험 — 표면 화학 (XPS, `Fig. 3` + `Fig. S4–S7`) ★ 우리 SEI 축 직결

> ⚠⚠ **전부 *순환 전* 시료다.** 이 논문에는 **순환 후(post-mortem) XPS 가 0건**이고, **S 2p·P 2p 스펙트럼도 0건**이다.

| 시료 | F | Br | Cl | N | 판정 |
|---|---|---|---|---|---|
| **pristine Li** (`Fig. S4`) | 무 | 무 | 무 | 무 | C 1s 284.8(C–C/C–H) + ~287.41(카보네이트) · O 1s **~531.20 LiOH** / **528.45 Li₂O** → 천연 Li₂O/LiOH/Li₂CO₃ 피막 |
| **LF-4** (`Fig. 3a`) | **684.8 = LiF** (주) + ~686.3 = –SO₂F | 무 | 무 | NOₓ-like + –SO₂–N–SO₂ | *"LiF-rich interphase **rather than a chemically pure LiF layer**"* (저자 자인) |
| **BC-3** (`Fig. 3b`) | 무 | **LiBr** (강) | **LiCl** (강) | 무 | 유기 부산물 없이 **순수 할라이드 피복** — 이 논문에서 가장 깨끗한 스펙트럼 |
| **LN-TMEDA** (`Fig. 3c`) | 무 | 무 | 무 | **~398.8 = Li₃N**(주) + ~401.8 = –NR₃ | *"Li₃N-**containing** interphase rather than a chemically pure Li₃N layer"* |
| **3LFCBNL-1** (`Fig. 3d`) | **LiF** (강·선명) | LiBr (**약·잡음 수준**) | LiCl (**약·잡음 수준**) | NOₓ + –NR₃ + **SO₂–N–SO₂** + Li₃N → **Li₃N 은 4성분 중 소수** (figure-read) | 4성분 공존은 맞으나 **세기가 심하게 불균등** |
| **LN-NM / 3LFCBNL-2** (`Fig. S7`) | — | — | — | Li₃N **+ C–N·NOₓ 불순물 다량** | NM 은 반응이 격해 *"chemically complex and structurally nonuniform nitrided layer"* → 탈락 |

**저자 자신의 결정적 유보 (본문 그대로)**: *"the present XPS results **neither establish that these components form chemically pure individual phases nor determine whether they are arranged as discrete vertically separated layers**."*
⇒ 즉 **제목의 "functionally differentiated"(= 기능별로 분화된 층) 은 설계 의도이지 증명된 구조가 아니다.** `Fig. 5g` 의 3층 도해는 가설 도해다.

### 3f. 실험 — 형상·나노역학 (SEM/EDS `Fig. 2`, AFM `Fig. 4`)

| 샘플 | RMS 거칠기 (nm) | 접착력 (nN) | **표면 겉보기 탄성률 (GPa)** |
|---|---|---|---|
| **LI** | **2.6** | **13.5** | **39.4** ⚠ |
| **LF-4** | 7.3 | 26.4 | 2.6 |
| **BC-3** | **33.0** (최대) | **48.9** (최대) | 3.7 |
| **LN-TMEDA** | 4.0 | 20.8 | 3.1 |
| **3LFCBNL-1** | 14.3 | 36.5 | 4.1 |

- ⭕ **저자가 39.4 GPa 를 스스로 부인**한다 — *"should be attributed to the **coupled effect** of the Li layer, native surface layer, and Cu substrate, **rather than to the intrinsic Young's modulus of pure Li metal**"* 이고, 나아가 *"the apparent modulus values … should be interpreted primarily as **comparative local surface responses rather than intrinsic material properties**"*. ⇒ **⛔ 이 5개 값은 우리 기계물성 축(E_VRH·B₀)과 같은 표에 절대 놓을 수 없다.**
- 코팅 총두께 **≈60 μm** (`Fig. S2` 단면 SEM). **개별 층 두께는 측정 불가** — 자인: 기계 절단 시 *"severe smearing and deformation of the soft Li substrate, together with **fracture of the comparatively brittle composite interphase**"*.
- 오차막대 **0개** (`Fig. 4f,g,h` 전부 단일 막대, n 미표기).

### 3g. 실험 — 풀셀 (`Fig. 6` + `Table S1`)

| 샘플 | 0.1 C | 0.2 C | 0.5 C | 1 C | **1000사이클 후 유지율** | 실제 수명 (figure-read) |
|---|---|---|---|---|---|---|
| **LI** | 146.9 / 65.4 % | 101.5 / 40.7 % | — | — | — | **3 사이클에 사망** |
| **BC-3** | 188.8 / 87.8 % | 149.6 / 89.8 % | 87.0 / 78.9 % | 56.1 / 52.8 % | — | **5 사이클에 사망** |
| **LF-4** | 199.0 / 91.0 % | 180.9 / 97.0 % | 135.2 / 91.0 % | 74.8 / 81.4 % | — | ≈90–100 사이클에 급락 → 590 사이클까지 ≈5 mAh g⁻¹ 잔존. **CE 가 0–115 % 로 요동**(소프트쇼트 지문) |
| **LN-TMEDA** | 202.9 / 90.9 % | 169.7 / 95.2 % | 90.5 / 80.1 % | **33.6** / 67.0 % | **72.1 %** | 1000 사이클 완주, 1 C 용량이 너무 낮다 |
| **3LFCBNL-1** | **215.0 / 91.0 %** | 194.5 / 97.1 % | 141.8 / 89.9 % | **77.1** / 80.1 % | **61.2 %** | 1000 사이클 완주, **1000번째 ≈47 mAh g⁻¹** (§10-1) |

- Table S2(문헌 13편 비교)에서 이 논문의 셀프-포지셔닝: *"215.0 mAh g⁻¹ at 1st cycle at 0.1 C / 77.1 mAh g⁻¹ at 1000th cycle at 1 C"*. **이 표기가 §10-1 의 오류를 SI 에서도 반복한다.**

---

## 4. DFT/계산 방법 ★

> 출처는 **SI §1.4 「First-principle calculations」 단 3문단**이다. 본문에는 방법절이 없다.

| 항목 | 이 논문 | 우리 규약 | 판정 |
|---|---|---|---|
| 코드 | **VASP** | QE (pw.x) + LOBSTER + UMA-s-1p1 | 다름(비교는 가능) |
| 범함수 | **GGA-PBE** | PBE | ✅ 같음 |
| 의사퍼텐셜 | **PAW** | QE PAW/USPP | ✅ 같음 |
| 평면파 컷오프 | **520 eV** (≈38.2 Ry) | ecutwfc 60 Ry / ecutrho 480 Ry (sei 계열) | 🟡 VASP 520 eV 는 MP 표준값 — 무난 |
| **k-점 메시** | ⛔ **미기재** | 계마다 명시 | 🔴 **재현 불가** |
| **슈퍼셀 크기·원자 수** | ⛔ **미기재** ("supercell" 단어만 2회) | nat·cell 을 protocol_hash 에 박음 | 🔴 |
| **진공층 두께** | ⛔ **미기재** (슬랩 계산인데) | — | 🔴 |
| **vdW 보정** | ⛔ **미기재** (Li 금속/이온결정 계면인데) | — | 🔴 |
| **스핀 편극** | ⛔ **미기재** | 계마다 선언 | 🔴 |
| **DFT+U** | 언급 없음 (해당 없음: 3d 없음) | — | ○ |
| **완화 수렴 (구조·전자)** | **NEB 만** 명시: 총에너지 **10⁻⁵ eV**, 힘 **0.02 eV Å⁻¹**. 계면/DOS 계산의 기준은 **미기재** | — | 🔴 |
| **NEB 방식** | **CI-NEB**(climbing image) | QE CI-NEB (`neb.x`) | ✅ 같은 계열 |
| **NEB 이미지 수** | ⛔ **미기재** (그림 마커로 4–13개 추정) | `num_of_images` 를 결과에 동봉 | 🔴 |
| **NEB 결함 기구** | ⛔ **미기재** — 공공(vacancy)인지 침입형(interstitial)인지 안 밝힘 | `sei_neb.json` 은 *공공 매개*를 못 박고 절연체는 `tot_charge −1` + jellium | 🔴🔴 **LiF 의 장벽은 기구에 따라 배로 갈린다** — 이 미기재만으로 0.6367 eV 는 비교 불가 |
| **끝점 축퇴 검사** | ⛔ 없음 — `Fig. 1j`(Li₃N)·`Fig. 1m`(LPSCl) 둘 다 끝점이 비축퇴 | 우리 `sei_neb.json` 은 **`endpoints_symmetry_equivalent` 를 필드로 저장**하고 False 면 blocking | 🔴 **우리 게이트로는 두 값 다 탈락** |
| **★ 무질서 처리 (S²⁻/Cl⁻ 4a/4c 자리)** | ⛔ **한 글자도 없다.** SQS·enumerate·다배열 평균 **0** | comp2 실측: 배열에 따라 Ea 가 **0.275 ↔ 0.151 eV** (1.8배) | 🔴🔴 **아지로다이트에서 이건 치명적이다.** `Fig. 1m` 끝점이 −0.152 eV 인 것 자체가 **특정 단일 배열**을 썼다는 증거다 |
| AIMD / MD / MLIP | **없음** | UMA-s-1p1 MLIP-MD | — |
| **계면에너지 γ** | SI 식 (S1) `γ = [E_interface − E_A − E_B]/A` **정의는 있으나 값이 어디에도 없다** | — | 🔴 **사장된 방법**(§10-2) |
| 밴드 정렬 / 일함수 / Schottky 장벽 | **없음** | — | 🔴 전자차단 주장의 물리적 핵심이 빠졌다 |
| Bader / 전하 적분 | **없음** (색깔 등가면만) | Bader·ICOHP 상시 | 🔴 |

### 4a. 계산 물량 정리

- 계면 슈퍼셀 **11개**: `LPSCl–Li` 1 + `LPSCl–X` 5 + `X–Li` 5 (X = Li₂O, Li₃N, LiF, LiCl, LiBr).
- DOS **7개**: Li, Li₂O, Li₃N, LiF, LiBr, LiCl, LPSCl (⚠ 라벨상 **단일상**이다 — 계면 DOS 가 아니다, §10-6).
- CI-NEB **6개**: Li₂O, LiF, Li₃N, LiBr, LiCl, LPSCl(1개 사슬에 두 장벽).

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1a–f | **계면 원자구조 + 차등전하밀도** 11개. (a) `LPSCl–Li` 단독, (b)–(f) 는 각 코팅마다 위 `LPSCl–X` / 아래 `X–Li` 2단. 노랑=축적, 청록=고갈. 범례 Li 파랑/P 보라/S 주황/Cl 초록/O 빨강/F 분홍/N 흰색/Br 검정, 축 c↑·b→ | ⚠ **등가면 값 미표기 + 적분값 0** → 패널 간 "크다/작다" 비교 금지. 그리고 **3상 샌드위치가 없다** = 시너지 주장에 직접 계산이 없다. 우리가 계면 CDD 를 낼 때 **isovalue 를 반드시 적자**는 반면교사 |
| 1g | **DOS 7패널** (Li / Li₂O / Li₃N / LiF / LiBr / LiCl / LPSCl), x = −5 → +12 eV, E_F=0 파선 | 🔑 **이 편에서 우리 축에 가장 직접 닿는 그림.** figure-read 전도대 개시: LiF ≈+9.7 / LiBr ≈+7.0 / LiCl ≈+5.9 / Li₂O ≈+4.4 / **Li₃N ≈+1.1** / LPSCl ≈+3.2. ⛔ **패널이 각자 E_F 에 정렬**돼 공통축이 아니다 → 밴드정렬 못 읽음. **Li₃N 최협갭**이 §7c 논지의 근거 |
| 1h–l | **코팅 5종 CI-NEB**: Li₂O 0.2326 / LiF 0.6367 / Li₃N **0.0103** / LiBr 0.5615 / LiCl 0.4800 eV | 🔑 *"LiCl/LiBr 은 이온전도상이 아니다"* 를 저자가 **자기 계산으로 못박은** 지점 — 우리 `[Lu]` 의 "LiCl 장벽 0.05 eV" 와 **정면 충돌**(§7e). ⚠ Li₃N 패널은 마커 4개·끝점 비축퇴·장벽이 힘 허용오차 안 |
| 1m | **LPSCl 단일 NEB 사슬**(≈14.5 Å, 마커 13개). 큰 봉우리 **0.2498 eV**(≈5 Å) + 부차 극대 **0.0166 eV**(≈9.3→9.9 Å). 시작 0 → **끝 −0.152 eV** | 🔑 우리 Ea 와 **숫자만** 가깝다(0.2498 ↔ comp1 0.253). ⛔ **같은 양이 아니다**(정적 단일경로 vs MD 앙상블) + **끝점 비축퇴** → 역방향 ≈0.40 eV. §7a 에서 "우연급 일치" 로 격하 |
| 2a | **제작 공정 도해**: Li → LiFSI@DME 침지 → DME 세척 → 적하(coprecipitation) → TMEDA 붓칠 → 80 ℃ 건조, 전 과정 Ar | 🔴 **도해 라벨 오기**: 적하 용액이 **"LiF/LiBr@THF"** 로 인쇄됐는데 본문·SI 는 **LiCl/LiBr@THF** 다 (§10-8) |
| 2b–g | **FE-SEM + EDS 매핑 6종** (LI / LO / LF-4 / BC-3 / LN-TMEDA / 3LFCBNL-1), 각 6원소(C·O·F·Cl·Br·N) + 광학 인셋 | 🔴 **배율이 다르다**: (b)–(e) 는 **10 μm** 스케일바, (f)–(g) 는 **100 μm**. 즉 주인공 3LFCBNL-1 의 *"dense and continuous … markedly reduced surface defects"* 는 **단성분 시료보다 10× 낮은 배율**에서 내린 판정이다 (§10-8). figure-read: (e) BC-3 의 Br·Cl 이 가장 강하고, (g) 에서 **Br·N 이 가장 약하다** |
| 3a–d | **XPS F 1s / "Br 1s" / "Cl 1s" / N 1s** × 4시료 (LF-4 / BC-3 / LN-TMEDA / 3LFCBNL-1) | 🔑 우리 `xps_reference_sei.csv` 와 붙일 유일한 실험 앵커. 🔴 **그런데 core level 라벨이 틀렸다** — Al Kα(1486.6 eV)로는 Br 1s(≈1782)·Cl 1s(≈2822)를 **여기할 수 없다**. 실제로 x축은 **65–75 eV = Br 3d**, **190–210 eV = Cl 2p** 다 (§10-2). figure-read: (d) 에서 Br·Cl 은 잡음 수준, Li₃N 은 N 4성분 중 소수 |
| 4a–e | **AFM 맵** 5종. ⚠ 컬러바 단위가 전부 **nN** — 높이(nm)가 아니라 **힘/접착 맵**이다. 범위가 패널마다 제각각(1.5~−17.2 / 25.8~−36.1 / 141.4~−80.6 / −23.2~−36.4 / −68.3~−34.8 nN), (d)·(e) 는 부호 방향까지 반대 | ⛔ 패널 간 육안 비교 불가. 측면 스케일바도 없다(SI 에 2×2 μm 만) |
| 4f,g,h | **막대그래프 3종**: RMS 거칠기(nm) / 접착력(nN) / **표면 겉보기 탄성률(GPa)** | 값은 본문과 완전 일치. ⛔ **오차막대 0·n 미표기** · (h) 는 **축 절단**(LI 39.4 만 위쪽) · **저자 스스로 "고유 물성이 아니다" 라고 못박음** → 우리 E_VRH/B₀ 와 같은 표 금지 |
| 5a,b | **대칭셀 800 h**: (a) LI(150 h 축), (b) **3LFCBNL-1**(800 h 축), 둘 다 0.398 mA cm⁻². y축 *"Voltage (V)"* ±40 | 🔴 **캡션은 (b) 를 "3LFCBNL-2" 라 하는데 그림 안 라벨과 본문은 "3LFCBNL-1"** (§10-8). 🔴 **y축 단위가 V 일 수 없다** — ASR 검산으로 mV 여야 한다(§12b). figure-read: LI 는 **≈115 h** 에 이력 소멸(저자가 소프트쇼트 가능성 자인) |
| 5c–g | **Li 석출 거동 모식도 5종** (LI / LF-4 / BC-3 / LN-TMEDA / **3LFCBNL-1**). (g) 가 핵심: 아래부터 **Li → LiF(초록) → LiCl·LiBr 입자 단층(하늘/흰 구슬) → Li₃N(보라) → 전해질** | 🔑 **"기능 분화" 의 그림판 정의.** ⚠ 그런데 (e) 에서 LiCl/LiBr 이 **불연속 입자 단층**으로 그려지고 덴드라이트가 그 **틈으로 뚫고 나간다** — 본문의 *"coverage continuity"* 주장과 그림이 어긋난다. 그리고 (g) 에서도 덴드라이트는 **여전히 LiF 층 안에 형성**돼 있다(가둘 뿐 막지 못함) |
| 6a–e | **풀셀 1 C 사이클링 5종** (용량 좌축 / CE 우축) | 🔑 **초록 수치 오류의 증거.** figure-read: (e) 3LFCBNL-1 은 1 C 진입 ≈78 → **1000사이클 ≈48 mAh g⁻¹**. Table S1 의 유지율 61.2 % × 77.1 = **47.2** 와 일치 ⇒ 초록의 *"retains 77.1 over 1000 cycles"* 는 틀렸다(§10-1). (a) LI 3사이클·(c) BC-3 5사이클 사망 · (b) LF-4 는 CE 가 0–115 % 요동 |
| Table S1 | 풀셀 5샘플 × (0.1/0.2/0.5/1 C 용량·효율) + 1000사이클 유지율 | §3g 에 전 셀 복원 |
| Table S2 | 문헌 13편 황화물 ASSLMB 성능 비교 (조건·성능·ref) | ⚠ 자기 행에 §10-1 오류를 반복. ⛔ 우리 db 이식 금지(조건 제각각) |
| S1 | Cu 박에 압연한 Li 금속 광학 사진 | (미판독 — 캡션만) |
| S2 | **3LFCBNL-1 단면 SEM + EDS** → 총두께 **≈60 μm** | 🔑 두께의 유일 근거. **층별 두께는 못 냄**(절단 손상 자인) |
| S3 | LF-D / LN-NM / 3LFCBNL-2 표면 SEM+EDS | 공정 대조군 |
| S4 | pristine Li XPS 6창 (C/O/F/Br/Cl/N) | **기준선**: Li₂O 528.45 · LiOH 531.20 · 할로겐/질소 무 |
| S5 | LF-4/BC-3/LN-TMEDA/3LFCBNL-1 의 **C 1s·O 1s** | 유기 잔류 확인 |
| S6 | 산화 Li (LO) C 1s·O 1s | Li₂O/LiOH 우세 |
| S7 | LN-NM·3LFCBNL-2 의 6원소 XPS | NM 경로의 C–N·NOₓ 불순물 |
| S8–S11 | **CCD 계단시험 전량** (S8: LI/LF-D/LO · S9: LF-1~6 · S10: BC-1~4 · S11: LN-TMEDA/LN-NM/3LFCBNL-1/3LFCBNL-2) | §3d 표의 원자료. **§12a 의 0.199 계단 분해능 판정 근거** |
| S12 | 풀셀 5종 충방전 곡선 | LI·LF-4·BC-3 의 과충전/불완전충전 지문 |

---

## 6. Post-processing ★

- **무엇을 했나**
  ① **차등전하밀도(differential charge density)** — 계면 11개. 시각적 판정만.
  ② **DOS** — 7상. E_F 근방 상태 유무로 "전자절연" 판정. **수치 갭 보고 없음.**
  ③ **CI-NEB** — 6상. 장벽 수치가 이 논문 계산 파트의 **유일한 정량 산출물**.
  ④ (SI 에 정의만 존재) **계면에너지 γ** — 값 없음.
- **도구**: VASP 외 **일절 미기재**. VESTA/pymatgen/LOBSTER 류 언급 0. 시각화 도구도 미기재(그림 양식상 VESTA 계열로 보이나 근거 없음).
- **수치화·플롯·기록 방식**
  - NEB 는 **에너지 vs "Reaction Coordinate (Å)"** — 이미지 번호가 아니라 **실제 거리**를 x축에 썼다. ⭕ 이건 좋은 관행이다(경로 길이가 보인다). 우리도 `sei_neb_mep_origin.csv` 에서 같은 축을 쓸 수 있다.
  - 장벽 숫자는 **그림 안 텍스트로만** 적혀 있고 표가 없다. 본문 재인쇄값과 대조해 일치 확인함.
  - DOS 는 y축이 **"a.u." 이고 눈금이 없다** → 상태밀도 크기 비교 불가, 문턱 판독만 가능.
  - **원자료 공개 0** (POSCAR/CONTCAR/OUTCAR/궤적 없음, "on request").

---

## 7. 우리 DFT 대비 (comp1 / modelc) → `our_dft_baseline.md`

### 7a. 🟡 LPSCl Li⁺ 장벽 — **숫자는 가깝고 양은 다르다**

| | 값 | 방법 | 정의 |
|---|---|---|---|
| **[Li26FDI]** | **0.2498 eV** (inter-cage) | VASP CI-NEB, 정적, **단일 경로·단일 배열** | 한 사슬 위 최고 안장점(0 K, 완화된 격자) |
| **우리 comp1** | **0.253 eV** | **MLIP-MD**(UMA-s-1p1, omat), 600/800/1000 K 3점 아레니우스, MSD 2–50 ps | **유효 활성화에너지**(모든 경로·모든 방향의 앙상블 평균) |
| **우리 modelc** | **0.224 eV** (단일궤적) / **0.197 ± 0.032 eV** (600 K 3-seed) | 동일 | 동일 |

**판정 — ⛔ "우리 Ea 가 문헌 NEB 로 검증됐다" 로 쓰면 안 된다.** 세 가지 이유:
1. **양이 다르다.** 정적 CI-NEB 안장점 ≠ MD 아레니우스 Ea. 후자는 다중 경로·상관 이동·격자 진동을 포함한다 (우리 `our_dft_baseline.md` 의 방법 라벨 주의와 같은 함정).
2. **그들 경로는 끝점이 비축퇴다** (figure-read 시작 0 → 끝 **−0.152 eV**). 정방향 0.2498 / 역방향 ≈0.40 eV 로 **방향 의존**이다. 방향 평균이 필요한 MD Ea 와 직접 대응하지 않는다.
3. **무질서 처리가 0이다.** 우리 comp2 실측으로 배열에 따라 Ea 가 **0.275 ↔ 0.151 eV**(1.8배) 흔들린다 — 0.2498 과 0.253 의 0.004 eV 차이는 **그 흔들림 안에 완전히 잠긴다**. 일치는 **우연급**이다.
   ⇒ 인용한다면 **"같은 결(0.2–0.3 eV대)"** 까지만.
4. ⛔ **우리 쪽 NEB 와는 아예 비교할 수 없다** — `db/properties/sei_neb.json` 은 **`retracted: true`, `n_citable: 0`** 이다. 우리에게 인용 가능한 NEB 값이 없다.

**⭕ 반대로 우리 게이트가 이 논문을 잡는다**: 우리 `sei_neb.json` 은 결과마다 **`endpoints_symmetry_equivalent`** 를 기록하고 False 면 blocking 처리한다. `Fig. 1j`(Li₃N)·`Fig. 1m`(LPSCl) 둘 다 **False** 다. 우리 규약이 남의 논문보다 엄격한 드문 지점이고, 이건 우리 방법론 카드에 쓸 만하다.

### 7b. 🔴 LPSCl 밴드갭 — **화해 불가, 비교 금지**

| | 값 | 방법 |
|---|---|---|
| **[Li26FDI]** | **figure-read ≈ 3.2 eV** (미약 개시) / ≈4.3 eV (본 개시) | `Fig. 1g` **DOS 문턱** — 논문은 숫자를 인쇄하지 않음 |
| **우리 comp1** | **2.066 eV** | PBE **fixed-occ nscf VBM/CBM 고유값** (canonical) |
| **우리 modelc** | **2.099 eV** | 동일 (⚠ 레지스트리 `method_integrity_flag` = *"⛔ 방법 불일치 의심"* — 실행본 미해소) |

**판정 — 🔴 이 격차는 판정할 수 없다.** 이유: ① 논문이 **숫자를 안 냈다** ② **DOS 문턱 판독은 우리 규율상 정본이 아니다**(CLAUDE.md: ~0.3 eV 과소) — 그런데 여기선 오히려 **크게 나왔다**, 즉 과소 보정으로도 설명이 안 된다 ③ **벌크인지 (100) 슬랩인지 라벨이 말해주지 않는다** ④ **k-메시·셀·무질서 배열이 전부 미기재**다.
⇒ **양쪽 다 "wide-gap insulator" 수준까지만 같다고 말하고, 절대값은 나란히 적지 않는다.** (우리 기존 규율: 문헌과 절대 갭 직접 비교 금지 — 그대로 적용.)

### 7c. 🔴🔴 **핵심 충돌 — Li₃P 를 피하려고 고른 Li₃N 이 같은 함정이다**

> ⚠ 이 절이 이 digest 의 가장 중요한 산출물이다. 요청서가 지시한 대로
> `papers/xiao2020_interface_stability_ssb_review.md` 의 같은 충돌과 **나란히** 적는다.

**Li₃P 를 둘러싼 세 입장 (이제 3파전이다)**

| 출처 | Li₃P 를 무엇으로 보나 | 근거 |
|---|---|---|
| **우리 원장** (`db/properties/sei_products.json` + `sei_electronic.json`) | **`conductor-LEAK`** — gap **0.70 eV**(MP) / 우리 fixed-occ nscf **0.7092 eV**(`li3p_mp-736`, verdict *"좁은 갭"*). 무도핑 음극 누설 산물이고, O 도입으로 **Li₂O(4.986 eV) 로 갈아치우는 것**이 처방 | 계산 (전자구조) |
| **[Xiao20Rev]** (Xiao/Ceder, *Nat Rev Mater* 2020) | **부동태 산물** — Li₃PO₄/Li 계면에서 *"Li₃P 와 Li₂O … **These reaction products are passivating**"*, LiPON/Li 에서도 *"block electron conduction but … permit Li-ion diffusion"* | 문헌 종합 + XPS(ref 222) |
| **[Li26FDI]** (이 논문) | **"이온 수송이 나쁜" 산물** — 서론 유일 등장: *"The resulting interphase products, including Li₂S, Li₃P, and LiCl … their **poor ionic transport capability** and continuous structural evolution … induce persistent interfacial impedance growth"* | ⛔ **근거 없음** — 인용(refs 13–15)만 있고 자체 측정·계산 0 |

🔴 **세 번째 입장은 문헌적으로 약하다.** Li₃P 는 통상 **이온전도는 준수하고 전자적으로 새는** 상으로 다뤄진다 — `[Xiao20Rev]` 가 인용하는 LiPON 사례가 정확히 *"이온은 통과, 전자는 차단"* 이고, 우리 계산도 **좁은 갭(전자 문제)** 을 가리킨다. **[Li26FDI] 는 문제 축을 전자→이온으로 옮겨 놓았고, 그 이동에 아무 근거가 없다.**

🔴🔴 **그리고 그 잘못된 진단이 대체재 선택을 오염시킨다.**
- 이 논문의 논리: *"Li₃P 는 이온을 못 통한다 → 그러니 **이온을 잘 통하는** 상(Li₃N, 0.0103 eV)을 넣자."*
- 그런데 **저자 자신의 `Fig. 1g` 가 Li₃N 을 다섯 코팅 중 갭이 가장 좁은 상으로 그린다** — figure-read **≈1.1 eV**, LiF(≈9.7)·LiBr(≈7.0)·LiCl(≈5.9)·Li₂O(≈4.4) 에 한참 못 미친다.
- **우리 `sei_products.json` 분류 기준**(`insulator ≥ 4 eV / marginal 2–4 / **conductor < 2 = e⁻ leak**`)을 그대로 적용하면 → **Li₃N 도 `conductor-LEAK` 다.** Li₃P(0.70) 와 같은 칸이다.
- 저자도 이 구멍을 **알고는 있다**. 본문에 심사 대응으로 보이는 유보가 박혀 있다: *"the DOS result of Li₃N **only indicates the absence of significant interfacial electronic states near the Fermi level**, whereas **its role as a fast Li⁺-transport phase cannot be inferred from DOS analysis alone**."* — 그러나 **"Li₃N 이 전자를 막느냐" 는 물음 자체는 끝내 답하지 않는다.**

⇒ **우리 결론**: 이 설계가 작동한다면 그 이유는 *"Li₃N 이 전자를 막아서"* 가 **아니라**, **LiF 가 Li 금속과 Li₃N 사이에 끼어 있어서**다(`Fig. 5g` 의 적층 순서가 정확히 그렇다). 즉 **이 논문의 구조는 "빠른 이온전도상은 전자적으로 샌다" 는 우리 판정을 반박하는 게 아니라, 그것을 전제로 우회한 설계다.** 논문 스스로는 그렇게 말하지 않는다. **← 이것이 우리가 이 편에서 얻는 가장 큰 것.**

### 7d. 🔴 우리 SEI 산물 5종 대조 — **관측 0/5**

| 우리 산물 (`sei_products.json` / `interface_reactivity_results.json`) | 이 논문에 나오나 | 어떤 증거로 |
|---|---|---|
| **LiCl** (gap 6.65 MP / **6.2603 우리 fixed-occ**, `insulator`) | 🟡 **나온다 — 그러나 분해산물이 아니다.** THF 용액에서 **인위적으로 뿌린 코팅**이다 | XPS **Cl 2p** ≈198.5 eV (`Fig. 3b,d`) — ⚠ 논문 라벨은 "Cl 1s"(오기) |
| **Li₂S** (3.90 MP / **3.4379 우리**, `marginal`) | 🔴 **서론 1문장 인용뿐.** 측정 0 | — (**S 2p 스펙트럼이 논문에 없다**) |
| **Li₃P** (0.70 MP / **0.7092 우리**, `conductor-LEAK`) | 🔴 **서론 1문장 인용뿐.** 측정 0 | — (**P 2p 스펙트럼이 논문에 없다**) |
| **Li₃PO₄** (5.73 MP / **5.9121 우리**, `insulator`) | 🔴 **등장 0회** | — |
| **Li₂SO₄** (양극쪽 산물) | 🔴 **등장 0회** | — |

**⇒ 판정: 이 논문은 우리 산물 목록을 *검증하지도 반박하지도* 않는다.** 이유는 단순하다 — **전해질 쪽 원소(P·S)를 한 번도 측정하지 않았다.** XPS 는 코팅 원소(F·Br·Cl·N·C·O)만 보고, 그마저 **전부 순환 전** 시료다.
🔴 이는 우리 §E 표의 동급 논문들(`[Li25]`·`[Wu26]`·`[WangYO]`·`[Xu26NdO]`·`[Liu]` — 전부 **순환 후 XPS** 로 Li₂S·Li₃P·LiCl 를 직접 잡았다)과 비교해 **명확한 열위**다. 자기가 "parasitic reaction 을 억제했다" 고 주장하면서 **그 reaction 의 산물을 측정하지 않았다.**

또 하나: 논문이 쓰는 **LiBr 은 우리 산물 목록에 없다** (우리 계에 Br 이 없다). 우리 `[Wu26]` 행이 순환 후 XPS 에서 **LiBr(69 eV)** 를 잡은 적이 있어 대응은 되지만, **우리 db 로 이식할 값은 없다.**

### 7e. 🔴 LiCl 이동장벽 — **우리 §E 표 안의 기존 문헌과 정면 충돌**

| 출처 | LiCl Li⁺ 장벽 | 성격 |
|---|---|---|
| **[Lu]** (우리 §E 기존 행) | **0.05 eV** — *"전자절연(gap 6.22) + **저 Li⁺ 장벽(0.05)** + 연성 → 좋은 buffer"* | 계산 |
| **[Li26FDI]** (이 논문) | **0.4800 eV** — *"LiCl/LiBr 은 **주 Li⁺ 수송상이 될 수 없다**"* | 계산 (CI-NEB) |

**≈10배 차이다.** 어느 쪽도 결함 기구(공공 vs 침입형)를 명시하지 않아 **원인을 특정할 수 없다** — 이온결정에서 공공 매개와 침입형 장벽은 통상 수 배 갈린다. ⚠ **우리 §E 의 `[Lu]` 행 "LiCl = 저장벽 buffer" 서술은 이제 무조건 문헌 충돌을 병기해야 한다.** (우리 자신의 `v3/licl` NEB 는 미완 = `Ea_forward_eV: None` 이라 심판을 못 본다.)

### 7f. ⚪ 기계물성 — **비교 자체가 성립하지 않는다**

- 이 논문: **AFM 표면 겉보기 탄성률 2.6–4.1 GPa** (코팅), 39.4 GPa (bare LI). **저자가 스스로 "고유 물성이 아니다" 라고 못박음.**
- 우리: **E_VRH 22.06 (comp1) / 27.66 GPa (modelc)** — DFT 탄성텐서(relaxed-ion), **LPSCl 벌크**.
⇒ **대상(코팅 vs 전해질) · 방법(AFM 나노압입 vs DFT C_ij) · 정의(겉보기 국소 응답 vs Voigt-Reuss-Hill)** 셋 다 다르다. **⛔ 같은 표 금지.** 우리 축 C 에 행을 만들지 않는다.

### 7g. ⚪ 산화안정성(축 B) — **해당 없음**

이 논문은 **음극(환원) 쪽만** 다룬다. ESW·grand-potential·산화 onset 계산 **0건**. 우리 **2.256 V(S²⁻-limited)** 와 대조할 대상이 없다.
(⚠ 다만 셀은 **이중층 전해질**로 양극쪽에 할라이드 **Li₁.₇₅ZrCl₄.₇₅O₀.₅** 를 깔아 **황화물이 고전압을 보지 않게** 했다 — 이건 "Cl-rich 산화안정" 축과 다른, **셀 설계로 회피** 하는 방법이다. 우리 축 B 에는 값이 아니라 **설계 선례**로만 남는다.)

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

1. **★★★ "빠른 이온전도상 = 전자적으로 새는 상" 이라는 우리 판정의 외부 사례가 하나 더 생겼다 — 그것도 저자가 의도치 않게.**
   우리 원장은 Li₃P(0.70 eV)를 `conductor-LEAK` 로 판정하고 O 도입 → Li₂O(4.986) 로 대체하는 서사를 쓴다. 이 논문은 **Li₃N(figure-read ≈1.1 eV, 장벽 0.0103 eV)** 을 골랐고, 그것만으로는 안 되니 **LiF 를 Li 쪽에 깔았다**. 즉 *"이온 빠른 상은 갭이 좁다 → 전자차단은 다른 상이 맡아야 한다"* 를 **실험적으로 반복**한 것이다. **우리 Nd/O 서사의 '층 분업' 논거로 인용 가능**하다 — 단 §7c 의 단서(저자는 그렇게 말하지 않는다)를 붙여서.
2. **★★ 우리 `sei_products.json` 갭 사다리에 LiF·Li₃N 칸이 비어 있다** — 이 논문이 그 두 칸을 (숫자 없이, 순위로만) 채워 준다: **LiF ≫ LiBr > LiCl > Li₂O ≫ Li₃N**. 우리 fixed-occ nscf 로 **LiF·Li₃N·LiBr 세 상을 추가 계산할 근거**가 생겼다 (`tools/sei/` 체인에 상만 추가하면 된다). 특히 **Li₃N 은 우리 원장에 "UMA 사용 금지"(2026-06 결정론적 편향 판정) 표지가 이미 붙어 있는 상**이라 — **MLIP 이 아니라 DFT 로** 가야 한다는 것까지 이미 정해져 있다.
3. **★★ CCD 보고 규약을 우리 것으로 만들자.** §12a 에서 보듯 이 논문의 CCD 8값은 전부 **0.199 mA cm⁻² 의 정수배**다 = **계단 분해능이 곧 불확실도**인데 4자리로 인쇄했다. 우리가 CCD 를 낼 일이 생기면 **계단 크기·마지막 통과 계단·실패 계단을 같이 보고**한다. (`kb/templates/estimand_card.md` 의 "보고량 정의" 에 넣을 만한 항목.)
4. **★ 계면 CDD 를 그릴 때 isovalue 를 반드시 적는다.** 이 논문 `Fig. 1a–f` 는 등가면 값이 없어 패널 비교가 무의미해졌다. 우리 CDD 그림(하우스 스타일)에 **isovalue + 적분 전하(Bader)** 를 같이 싣는 관행을 못박자 — `[Luo22]` 가 Bader 로 전해질 순전하를 정량화한 것이 바른 예다.
5. **★ 밴드 정렬이 빠진 "전자차단" 주장의 표본.** 계면 전자주입은 **각 상의 갭이 아니라 정렬**이 정한다. 우리가 SEI 전자차단을 주장할 때는 **갭 사다리 + 정렬(또는 최소한 슬랩 일함수)** 을 같이 대야 한다는 반면교사.
6. **⚪ 이식 금지 목록**: 성능 수치(CCD·용량·사이클) 전량 · AFM 탄성률 전량 · 장벽 5종 절대값(결함 기구 미기재) · figure-read 갭 전량.

---

## 9. 인용 가능 문장 (deck/paper용)

> ⚠ 전부 **문헌 소환값**이다. 우리 db 절대값과 같은 표에 놓지 않는다. 인용 시 조건(가압 mold cell, 60 μm 코팅)을 반드시 병기.

- *"Li₆PS₅Cl 은 Li 금속과 접촉하면 Li₂S·Li₃P·LiCl 를 만들고, 이 산물들은 초기에는 일부 부동태화하지만 계속 진화해 계면 임피던스를 키운다"* — [Li26FDI] 서론 (⚠ **이 논문의 자체 근거는 없다**, refs 13–15 재인용).
- *"LiF·LiCl·LiBr 은 전자절연이지만 **Li⁺ 이동장벽이 높아(0.64 / 0.48 / 0.56 eV) 주된 빠른 이온 전도 경로가 될 수 없다**. 따라서 LiCl/LiBr 은 빠른 이온전도상이 아니라 **계면 균질화 성분**으로 이해해야 한다"* — [Li26FDI] §2 + `Fig. 1h–l`. **← 이 편에서 가장 인용가치 높은 문장.**
- *"한 물질이 전자절연·빠른 Li⁺ 수송·계면 균질성·기계적 견고성·전기화학 안정성을 동시에 만족하기는 본질적으로 어렵다 — 전자 누설 억제, 국소 환경 균질화, 빠른 Li⁺ 수송에 필요한 성질이 한 재료 안에 모이는 일은 드물다"* — [Li26FDI] 서론. **우리 "층 분업" 논거의 문헌 표현.**
- *"XPS 결과는 이 성분들이 화학적으로 순수한 개별 상을 이룬다는 것도, 수직으로 분리된 층으로 배열돼 있다는 것도 입증하지 못한다"* — [Li26FDI] §2 (**저자 자인**). ⭕ 이 논문을 인용할 때 **반드시 같이 인용**한다.
- ⛔ **인용 금지**: *"retains 77.1 mAh g⁻¹ over 1000 cycles at 1 C"* (초록·결론·Table S2) — **틀렸다**. 1000번째 사이클 용량은 **≈47 mAh g⁻¹** 이다 (§10-1).

---

## 10. 주의/한계 (over-claim 방지) — **본문↔그림/표 어긋남 8건 포함**

### 10-1. 🔴🔴 **초록 수치 오류 — 1000사이클 용량이 아니다** (우리가 인용하면 바로 걸린다)

초록·본문·결론·Table S2 가 모두 *"retains **77.1 mAh g⁻¹ over 1000 cycles** at 1C"* 라고 쓴다. 그러나 **Table S1** 의 같은 행을 보면 `1 C` 칸이 **77.1 / 80.1 %** 이고, 별도 칸 *"The capacity retention rate after 1000 cycles"* 가 **61.2 %** 다.
⇒ **77.1 은 1 C 진입 시(4사이클째) 용량**이고, 1000번째 용량은 **77.1 × 0.612 = 47.2 mAh g⁻¹** 이다.
**figure-read 로 독립 확인**: `Fig. 6e` 의 용량 곡선은 1 C 진입 ≈78 에서 시작해 **1000사이클에서 ≈48 mAh g⁻¹** 에 닿는다. 계산값과 일치한다.
같은 구조가 **LN-TMEDA** 에도 있다(1 C 33.6, 유지율 72.1 % → 1000번째 ≈24.2; figure-read ≈22–24 ✓).
**⇒ 이 논문의 헤드라인 성능은 인쇄된 것보다 낮다.** NCM811 기준 1 C 47 mAh g⁻¹ 는 **1 C 공칭 180 mAh g⁻¹ 의 26 %** 다.

### 10-2. 🔴 **XPS core-level 라벨이 틀렸다 — 우리 `xps_reference_sei.csv` 와 붙이기 전에 고쳐야 한다**

본문·캡션·SI 가 일관되게 **"Br 1s"**·**"Cl 1s"** 라고 쓴다. 그런데 SI 장비 기재는 **PHI VersaProbe 4, Al target** = Al Kα **1486.6 eV** 다.
- **Br 1s = 약 1782 eV**, **Cl 1s = 약 2822 eV** → **Al Kα 로는 여기 자체가 불가능하다.**
- `Fig. 3` 의 실제 x축: **65–75 eV**(= **Br 3d**, LiBr 3d₅/₂ ≈68–69 eV) · **190–210 eV**(= **Cl 2p**, LiCl 2p₃/₂ ≈198.5 eV).
⇒ **실물은 Br 3d 와 Cl 2p 다.** 우리 `xps_reference_sei.csv` 의 Cl 2p 앵커와 **비교 가능하다** — 단 **논문 라벨을 그대로 옮기면 우리 원장이 오염된다.**
추가: Cl 2p 는 스핀-궤도 이중선(Δ≈1.60 eV)인데 **단일 성분으로 피팅**돼 있다.

### 10-3. 🔴 **"functionally differentiated"(층 분화) 는 증명되지 않았다 — 저자 자인 + 우리 보강**

저자 자인(§3e 인용)에 더해, **우리 판독이 그 자인을 정량으로 뒷받침한다**:
- XPS 정보심도는 **≈10 nm**, 코팅 총두께는 **≈60 μm** → **1.7 × 10⁻⁴ (0.017 %)** 만 본 것이다.
- 게다가 **적층 순서와 XPS 세기가 어긋난다**: 공정 순서상 LiF 가 **가장 아래(Li 쪽)** 이고 Li₃N 이 **가장 위**인데, `Fig. 3d` 에서 **F 1s 가 가장 강하고 선명**하며 Br·Cl 은 잡음 수준, Li₃N 은 N 4성분 중 소수다. **깨끗한 수직 3층이라면 XPS 는 거의 Li₃N 만 봐야 한다.**
⇒ 실제 구조는 **혼합된 복합층**일 가능성이 높다. `Fig. 5g` 의 3층 도해는 **모식도이지 데이터가 아니다.**

### 10-4. 🔴 **Li₃N 0.0103 eV 와 LPSCl intra-cage 0.0166 eV 는 자기 수렴한계 안에 있다**

SI 가 밝힌 NEB 힘 수렴은 **0.02 eV Å⁻¹** 이다.
- **Li₃N**(`Fig. 1j`): 전 경로 ≈1.33 Å 에 마커 **4개** → 이미지 간격 ≈0.44 Å. 잔류힘 0.02 eV Å⁻¹ × 0.44 Å ≈ **0.009 eV** ≈ 보고된 **0.0103 eV**. **장벽과 오차가 같은 크기다.**
- **LPSCl intra-cage**(`Fig. 1m`): ≈9.3 → 9.9 Å 두 인접 이미지의 에너지차(≈0.016 eV)를 장벽으로 읽었다. 간격 ≈0.6 Å × 0.02 = **0.012 eV**. 역시 같은 크기.
- 더 근본적으로, **CI-NEB 는 사슬 위 *하나의* 이미지만 안장점으로 끌어올린다**(여기선 0.2498 eV 봉우리). **부차 극대인 0.0166 eV 는 수렴된 안장점이 아니다.**
⇒ **두 값은 "0 에 가깝다" 이상으로 읽으면 안 된다.** 특히 *"Li₃N 이 Li₂O 보다 23배 빠르다"* 식 비율 인용 금지.

### 10-5. 🔴 **Li₃P 진단이 근거 없이 바뀌었고, 그 진단이 대체재 선택을 오염시켰다** → §7c 전문 참조

### 10-6. 🔴 **DOS 논증이 계면 논증이 아니다 (+ 본문↔그림 서열 어긋남 2건)**

- **(a)** 본문: *"the DOS of the **Li/LPSCl interfacial model** exhibits finite electronic states near the Fermi level (`Fig. 1g`)"*. 그러나 `Fig. 1g` 의 패널 라벨은 **`Li`·`Li₂O`·`Li₃N`·`LiF`·`LiBr`·`LiCl`·`LPSCl`** 로 **단일상**이고, 캡션도 *"DOS of different inorganic coatings and LPSCl"* 다. **계면 DOS 라는 증거가 없다.**
  ⇒ 그렇다면 이 그림이 말하는 것은 *"LiF 는 절연체다"* 뿐이고, 그건 계산이 필요 없는 상식이다. **계면 전자차단을 보이려면 밴드정렬/일함수/계면 PDOS 가 필요한데 전부 없다.**
- **(b)** 7패널이 **각자의 E_F 기준**으로 그려져 있어(절연체는 E_F = VBM) **공통 에너지축이 아니다** — 이 그림으로 밴드정렬을 읽으려는 시도 자체가 성립하지 않는다.
- **(c)** 본문: *"LiF 계면은 F 주위에 **뚜렷한 전자 국재화**"* / *"Li₂O·Li₃N 계면은 **비교적 완만하고 균일한** 전하 재분포"*. 우리 `Fig. 1b–f` 판독은 **반대** — (b)Li₂O·(c)Li₃N 의 LPSCl 쪽 계면 로브가 (d)LiF 보다 **크고 넓다**. 등가면 값이 없어 확정은 못 하지만, **본문 서열이 그림 인상과 맞지 않는다.**

### 10-7. 🔴 **"시너지" 에 직접 계산이 0건이다**

계산된 것은 **2상 계면 11개**(`LPSCl–X` 5 + `X–Li` 5 + `LPSCl–Li` 1)뿐이다. **Li‖LiF‖LiCl/LiBr‖Li₃N‖LPSCl 다층 모델은 없고, LiF|LiCl 같은 코팅-코팅 계면도 없다.** 논문의 중심 주장(기능 분화·협동)은 **성분별 개별 스크린을 산문으로 합친 것**이다.
같은 결로, **SI 식 (S1) 의 계면에너지 γ 는 정의만 있고 값이 본문·SI 어디에도 없다** — 어느 코팅이 LPSCl/Li 와 열역학적으로 더 잘 붙는지는 **결국 답하지 않았다**. 성분 선택의 열역학 근거가 통째로 비어 있다.
(부수: SI 물리분석절에 **XRD** 가 들어 있으나 **XRD 데이터가 논문 어디에도 없다** — Fig. S1–S12 에 XRD 없음. γ 와 함께 **사장된 방법 2건**.)

### 10-8. 🟡 **라벨/캡션 오기 3건 + 배율 불공정 1건**

| # | 위치 | 내용 |
|---|---|---|
| (i) | `Fig. 5` **캡션** | *"(b) **3LFCBNL-2**"* ↔ **그림 안 라벨과 본문은 "3LFCBNL-1"**. 800 h 데이터의 주인이 누구인지 캡션만 다르다 |
| (ii) | `Fig. 2a` **도해** | 적하 용액이 **"LiF/LiBr@THF"** 로 인쇄 ↔ 본문·SI 는 **LiCl/LiBr@THF** |
| (iii) | `Fig. 3` 전체 | **"Br 1s"·"Cl 1s"** → 실제 **Br 3d·Cl 2p** (§10-2) |
| (iv) | `Fig. 2b–g` | **(b)–(e) 10 μm vs (f)–(g) 100 μm** — 주인공(g)을 **10× 낮은 배율**에서 *"dense and continuous, markedly reduced surface defects"* 로 판정했다. **동일 배율 비교가 아니다** |

### 10-9. 🟡 **저자 스스로 적은 한계 (⭕ 이 논문의 미덕)**

이 논문은 과장이 많지만 유보도 유난히 많다. 인용할 때 **함께** 옮긴다.
- *"mold-type cells under an externally applied stack pressure … **should not be directly extrapolated to practical coin-cell or pouch-cell configurations operated under reduced pressure**"*
- 60 μm 두께에 대해: *"**should not be regarded as an optimized thickness**"* + *"may introduce **additional ionic resistance, an energy-density penalty, and scalability challenges**"*
- 대칭셀 이력 소멸에 대해: *"should **not** be interpreted as definitive evidence of improved interfacial stability"* (소프트쇼트 가능성)
- AFM 탄성률에 대해: *"should **not** be directly interpreted as evidence that the interphase can completely resist cracking or delamination"*
- LF-4 조성에 대해: *"more appropriately described as a **LiF-rich interphase rather than a chemically pure LiF layer**"*

### 10-10. 🟡 측정의 공백 목록

**σ(이온전도도) 0건 · EIS/임피던스 0건 · XRD 데이터 0건 · S 2p·P 2p XPS 0건 · 순환 후 XPS 0건 · ToF-SIMS 0건 · 단면 TEM 0건 · 반복수/오차막대 0건 · 원자료 공개 0건.**

---

## 11. 용어 미니사전 (이 편을 읽는 데 필요한 것만)

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **CCD** (critical current density) | 대칭셀 전류를 계단식으로 올리다가 전압이 붕괴(= 덴드라이트 관통/단락)하는 직전 전류밀도 | 이 논문의 대표 지표. **계단 분해능 0.199 mA cm⁻²**(§12a) |
| **ICE** (initial Coulombic efficiency) | 첫 사이클의 방전/충전 용량 비 | 3LFCBNL-1 **91.0 %** |
| **CI-NEB** | climbing-image nudged elastic band. 사슬 위 **최고 이미지 하나만** 안장점으로 끌어올려 장벽을 정확히 잡는 NEB 변형 | **부차 극대(0.0166 eV)는 이 보정을 못 받는다** — §10-4 의 핵심 |
| **차등전하밀도** (differential/deformation charge density) | Δρ = ρ(계면) − ρ(A) − ρ(B). 접촉으로 전자가 어디로 몰리고 빠졌는지 | 등가면 값을 안 적으면 **패널 간 비교 불가** |
| **intra-cage / inter-cage** | 아지로다이트 Li 는 PS₄ 사이 "cage"(48h 고리) 안을 빠르게 돌고(intra), 장거리 수송은 cage↔cage 뜀(inter)이 율속 | 본문 0.0166 / 0.2498 eV. **intra 값은 신뢰 못 함**(§10-4) |
| **LiFSI** | lithium bis(fluorosulfonyl)imide, LiN(SO₂F)₂. Li 금속과 반응해 **LiF-rich** 막을 만든다 | LF 계열 전구체. 잔류 **–SO₂F·SO₂–N–SO₂·NOₓ** 가 XPS 에 남는다 |
| **TMEDA** | N,N,N′,N′-tetramethylethylenediamine. Li 와 온건하게 반응해 **Li₃N** 생성 | LN-TMEDA. **NM(나이트로메탄)보다 깨끗**하다는 것이 이 논문의 공정 주장 |
| **NM** | nitromethane, CH₃NO₂. Li 와 격렬 반응 → Li₃N + C–N/NOₓ 부산물 + 가스 | LN-NM·3LFCBNL-2. 품질 열위 |
| **LiZrClO** | **Li₁.₇₅ZrCl₄.₇₅O₀.₅**, 자체 합성 할라이드 전해질 | **양극쪽 층** — 황화물이 고전압을 직접 안 보게 하는 이중층 설계 |
| **soft short** | 덴드라이트가 부분 관통해 국소 전자전도 경로가 생긴 상태. **전압 이력이 오히려 줄어든다** | `Fig. 5a` 의 LI 가 **≈115 h 에 이력 소멸** — 저자가 이 가능성을 자인 |
| **표면 겉보기 탄성률** | AFM 힘-거리 곡선에서 얻는 국소 접촉 강성. **기판·피막·탐침이 다 섞인 값** | 39.4 GPa(LI) 가 Li 의 탄성률이 아닌 이유 |

---

## 12. ★ 본 digest 의 독립 재분석 — **논문에 인쇄돼 있지 않은 것**

### 12a. 🔑 **CCD 8값이 전부 `0.199 mA cm⁻²` 의 정수배다 — 유효숫자 4자리는 허수다**

논문이 보고한 CCD 를 **0.199 mA cm⁻² 로 나눠 보면**:

| 샘플 | 보고 CCD | ÷ 0.199 | 계단 번호 n |
|---|---|---|---|
| LI / LF-D / LO | 0.398 | 2.000 | **2** |
| BC-3 | 0.597 | 3.000 | **3** |
| LN-TMEDA / LN-NM | 0.796 | 4.000 | **4** |
| LF-4 | 1.393 | 7.000 | **7** |
| 3LFCBNL-2 | 2.188 | 10.995 | **11** (11×0.199 = 2.189) |
| 3LFCBNL-1 | 3.581 | 17.995 | **18** (18×0.199 = 3.582) |

**⇒ CCD 시험은 `0.199 mA cm⁻²` 단위의 전류 계단으로 돌렸고, 보고값은 "마지막으로 통과한 계단" 이다.**
따라서:
- **실질 불확실도는 ±0.199 mA cm⁻²** (= 계단 하나)다. `3.581` 의 소수 셋째 자리는 **의미가 없다** — 물리적으로는 **"3.58 ± 0.20"**, 더 정직하게는 **"18번째 계단 통과, 19번째 실패"** 다.
- **BC-3(3계단) vs LN-TMEDA(4계단)** 의 차이는 **한 계단**이다. "Li₃N 이 LiCl/LiBr 보다 낫다" 는 **1 계단 차이 · n=1** 로 주장된 것이다.
- 반면 **3LFCBNL-1(18) vs LF-4(7)** 는 **11계단 차이**라 계단 노이즈로 설명되지 않는다 — **복합 코팅의 우위 자체는 견고하다.**
- 0.199 mA cm⁻² 라는 값은 **고정 전류 ÷ 전극 면적**의 흔적이다(예: ⌀10 mm = 0.785 cm² 에 0.156 mA, 또는 1.005 cm² 에 0.200 mA). 논문은 **전극 면적을 밝히지 않는다** — 그래서 어느 쪽인지 특정할 수 없다.

**우리 규율로 옮기면**: CCD 류 계단시험 보고량은 **① 계단 크기 ② 마지막 통과 계단 ③ 실패 계단 ④ 전극 면적**을 같이 적어야 한다. 지금처럼 "3.581" 만 적으면 **재현도 비교도 안 된다.**

### 12b. 🔑 **`Fig. 5a,b` 의 y축 단위 "V" 는 mV 여야 한다 (ASR 검산)**

`Fig. 5a,b` 의 y축은 **"Voltage (V)", 범위 ±40** 이고 정상상태 진폭은 figure-read **≈±7**(3LFCBNL-1), 초기 스파이크 **≈±18**(LI)이다. 전류는 **0.398 mA cm⁻²**.
- **단위가 V 라면** → 면적비저항 **ASR = 7 V ÷ 0.398 mA cm⁻² ≈ 1.76 × 10⁴ Ω cm²**. 이 정도면 셀이 800 h 동안 안정적으로 돌 수 없고, ±7 V 는 **어떤 고체전해질의 전기화학창도 한참 벗어난다**(모든 성분이 분해된다).
- **단위가 mV 라면** → **ASR ≈ 17.6 Ω cm²** — 가압 mold 형 황화물 대칭셀로 **완전히 정상적인 값**이다.
⇒ **y축 라벨이 `V` 로 잘못 인쇄됐다고 판단한다.** (우리 §E 표에 이미 같은 유형의 선례가 있다 — `[Deng26PS]` 의 *"y축 라벨 오류"* 행.)
**⛔ 그러므로 `Fig. 5` 에서 과전압 수치를 읽어 우리 표에 옮기지 않는다.** 800 h 안정성이라는 **정성적 사실만** 가져온다.

### 12c. 🔑 **XPS 가 본 부피 = 코팅의 0.017 %**

XPS 정보심도 **≈10 nm** ÷ 코팅 두께 **≈60 μm** = **1.7 × 10⁻⁴**.
`Fig. 3`·`Fig. S5`·`Fig. S7` 의 모든 조성 주장은 **코팅 최외곽 만분의 1.7** 에 대한 것이다. 깊이 프로파일(Ar 스퍼터링)도, 단면 분석(TEM/EELS)도 없다.
⇒ **"복합 계면상의 조성" 이라는 서술은 실제로는 "복합 계면상 표면의 조성" 이다.** §10-3 의 층 구조 미증명과 같은 뿌리다.

### 12d. 🔑 **rate capability 를 재계산하면 "고율" 주장이 약해진다**

`Table S1` 에서 **1 C 용량 ÷ 0.1 C 용량**:

| 샘플 | 0.1 C | 1 C | **비율** |
|---|---|---|---|
| LF-4 | 199.0 | 74.8 | **37.6 %** |
| BC-3 | 188.8 | 56.1 | **29.7 %** |
| LN-TMEDA | 202.9 | 33.6 | **16.6 %** |
| **3LFCBNL-1** | **215.0** | **77.1** | **35.9 %** |

⇒ **3LFCBNL-1 의 율특성(35.9 %)은 LF-4(37.6 %)보다 오히려 낮다.** 즉 복합 코팅의 이점은 **율특성이 아니라 수명**이다(LF-4 는 ≈90–100 사이클에 죽고 3LFCBNL-1 은 1000 사이클을 완주한다). 본문이 *"insufficient Li⁺ transport under high-rate conditions"* 를 LF-4 의 약점으로 지목하지만, **0.1 C→1 C 유지율로는 둘이 사실상 같다.** Li₃N 의 "빠른 이온수송" 기여는 이 표에서 보이지 않는다 — LN-TMEDA 단독이 **율특성 꼴찌(16.6 %)** 인 것이 특히 그렇다.
**⇒ 이 논문의 성능 이득은 "이온수송 개선" 보다 "부반응·단락 억제(수명)" 로 설명하는 편이 데이터에 더 맞는다.** (저자 서사와 다르다.)

---

## 13. 한 줄 결론

**성능 데이터는 견고하고(CCD 9× · 800 h · 1000 사이클) 저자의 자기 유보도 드물게 정직하지만, "기능 분화" 라는 제목의 주장은 계산(2상 계면 11개, 3상 모델 0개)으로도 측정(XPS 최외곽 0.017 %, 순환 후 분석 0건)으로도 증명되지 않았다 — 그리고 우리에게 진짜 값진 것은 그 주장이 아니라, 저자가 Li₃P 를 피하려고 고른 Li₃N 이 자기 `Fig. 1g` 에서 다섯 코팅 중 갭이 가장 좁아(figure-read ≈1.1 eV) 우리 `conductor-LEAK` 칸에 그대로 들어간다는 사실, 즉 "빠른 이온전도상은 전자적으로 샌다 → 전자차단은 다른 층이 맡아야 한다" 는 우리 층-분업 서사를 이 논문이 의도치 않게 한 번 더 실증했다는 점이다.**

---

<!-- MERGE-BLOCK — ⚠ 공유 파일 충돌 방지를 위해 이 digest 안에만 둔다. 사람이 나중에 합친다.
     (2026-09-12, litdb-curator. 네 편이 동시에 돌고 있어 litdb/INDEX.md · litdb/comparison_vs_ours.md ·
      kb/syntheses/* 는 **건드리지 않았다**. 아래 세 블록은 목적지 표의 열 수에 맞춰 완성해 두었다.)

     ※ 🎤 talk 역링크: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` →
       `litdb/talks/lee2026_skku_mlip_materials_design.md` 하나뿐인데, 그 대기열에
       이 논문(Functionally Differentiated / 3LFCBNL / TMEDA / Xuebao Li)은 **없다**.
       → talk 역링크 작업 **해당 없음**.

═══════════════════════════════════════════════════════════════════════════
(a) litdb/INDEX.md — "## ✅ Digest 완료 (paper-level)" 표에 넣을 행 1줄  [3열: slug | 논문 | 축]
═══════════════════════════════════════════════════════════════════════════

| `papers/li2026_functionally_differentiated_interphase.md` **(본문 11 pp + SI(.docx) 통합)** | **[외부·⭐ 황화물/Li 금속 *인공* 계면상 설계 — ★ 우리 `sei_products.json` 의 `Li₃P = conductor-LEAK` 판정과 *세 번째로 다른 입장*이 나온 편 · 🔑 저자가 Li₃P 대체재로 고른 **Li₃N 이 자기 `Fig. 1g` 에서 최협갭**(figure-read ≈1.1 eV)이라 우리 기준으론 같은 `conductor-LEAK` 칸이다]** ✅ **Xuebao Li**/Chao Zhao/Yueqing Peng/Kun Zeng/Shijie Han/Zekai Zhang/**Zhuangzhi Wu\***/**Dezhi Wang\*\*** (Central South University MSE + 분말야금 국가중점실험실, 단일기관 7인), "**Functionally differentiated composite interphase enables stable sulfide-based all-solid-state lithium metal batteries**" (***J. Energy Storage* 181, 124529 (2026)**, DOI 10.1016/j.est.2026.124529; NSFC 52374407; inbox #115 본문 11 pp · SI `.docx` · refs 47 · 그림 **6장**·표 0장). **설계 = LiF(전자차단) + LiCl/LiBr(피복 균질화) + Li₃N(빠른 Li⁺) 3성분 순차 습식코팅(LF-4→BC-3→TMEDA) = 3LFCBNL-1, 총두께 ≈60 μm.** 성적: CCD **0.398→3.581 mA cm⁻²**(9×) · 대칭셀 **800 h**@0.398 · 풀셀(NCM811‖LiZrClO–LPSCl‖coated Li) 0.1 C **215.0 mAh g⁻¹**/ICE **91.0 %** · 1 C **1000 사이클**. **계산 = VASP/PBE/PAW/520 eV, 계면 슈퍼셀 11개 + DOS 7종 + CI-NEB 6종**(Li₃N **0.0103** / Li₂O 0.2326 / LiCl 0.4800 / LiBr 0.5615 / LiF 0.6367 / LPSCl inter-cage **0.2498** · intra-cage 0.0166 eV). ⛔⛔ **k-메시·셀크기·진공·vdW·스핀·NEB 이미지수·결함기구·무질서처리 전부 미기재 · 밴드갭 숫자 0 · SI 식(S1) 계면에너지 γ 는 정의만 있고 값 없음 · XRD 도 방법에만 있고 데이터 없음.** 🔴 **본문↔그림/표 어긋남 8건**(digest §10): ① **초록의 `77.1 mAh g⁻¹ over 1000 cycles` 는 1 C *첫* 용량이고 1000번째는 ≈47**(Table S1 유지율 61.2 % 로 검산 + `Fig. 6e` figure-read ≈48) ② **XPS "Br 1s"·"Cl 1s" 는 Al Kα(1486.6 eV)로 여기 불가 — 실제 Br 3d·Cl 2p** ③ 층 분리 미증명(**저자 자인** + XPS 심도 10 nm ÷ 60 μm = **0.017 %**) ④ 0.0103·0.0166 eV 가 자기 힘수렴(0.02 eV Å⁻¹) 안 ⑤ `Fig. 1g` 는 **계면 DOS 가 아니라 단일상 DOS**(각자 E_F 정렬 = 밴드정렬 못 읽음) ⑥ 3상 샌드위치 모델 **0개**(시너지에 직접 계산 없음) ⑦ `Fig. 5` 캡션 "3LFCBNL-2"↔본문/그림 "3LFCBNL-1" · `Fig. 2a` 도해 "LiF/LiBr@THF"↔본문 "LiCl/LiBr@THF" ⑧ `Fig. 2` 배율 불공정(단성분 10 μm vs 주인공 100 μm). **본 digest 독립 재분석 4건**(§12): **CCD 8값 전부 `0.199 mA cm⁻²` 정수배**(n=2/3/4/7/11/18 → 유효숫자 4자리는 허수, 실질 ±0.199) · **`Fig. 5` y축 `V` 는 mV 여야**(ASR 검산 17.6 Ω cm² vs 1.76×10⁴) · XPS 가 본 부피 0.017 % · **율특성 재계산 시 3LFCBNL-1(35.9 %) < LF-4(37.6 %)** = 이득의 실체는 율특성이 아니라 수명. 그림 **6/6 실독**(SI 는 `.docx` 라 이미지 없음, 텍스트 206문단 전수). | **E 환원/음극(Li 금속) 계면** (+ 방법 원전 소량) |

═══════════════════════════════════════════════════════════════════════════
(b) litdb/comparison_vs_ours.md — 넣을 곳 2군데
═══════════════════════════════════════════════════════════════════════════

--- (b-1) "## E. 환원 / 음극(Li 금속) 계면" 표에 넣을 행 3개  [4열: | 주장 | 출처 | 우리 | 일치 |] ---

| **🔴🔴 Li₃P 논쟁에 *세 번째 입장*이 들어왔고, 그 오진이 대체재 선택을 오염시켰다** — 이 편은 Li₃P 를 *"**poor ionic transport capability**"* 로 규정한다(서론 유일 등장 1회, refs 13–15 재인용, **자체 측정·계산 0**). 우리(전자 누설)와도 `[Xiao20Rev]`(부동태 산물)와도 다르다. 그리고 그 진단을 따라 *"이온이 빠른 상"* 으로 **Li₃N**(CI-NEB **0.0103 eV**)을 골랐는데, **저자 자신의 `Fig. 1g` 가 Li₃N 을 다섯 코팅 중 최협갭으로 그린다** (figure-read 전도대 개시 ≈**1.1 eV** ‖ LiF ≈9.7 · LiBr ≈7.0 · LiCl ≈5.9 · Li₂O ≈4.4) | **[Li26FDI]** `Fig. 1g`·`Fig. 1h–l` + 서론 (⚠ 갭은 **논문 미인쇄**, 우리 DOS-문턱 figure-read — 우리 규율상 정본 아님) | `sei_products.json` 분류 **`insulator ≥4 / marginal 2–4 / conductor <2 eV = e⁻ leak`** · `sei_electronic.json` fixed-occ nscf: **Li₃P 0.7092**(*"좁은 갭"*) · Li₂S 3.4379 · Li₂O 4.986 · LiCl 6.2603 · Li₃PO₄ 5.9121 | 🔴 **우리 기준을 그대로 대면 Li₃N 도 `conductor-LEAK` 다** — Li₃P(0.70)와 같은 칸. ⇒ 이 설계가 도는 이유는 *"Li₃N 이 전자를 막아서"* 가 아니라 **LiF 가 Li 와 Li₃N 사이에 끼어서**(`Fig. 5g` 적층 순서)다. **즉 이 논문은 우리 "층 분업" 판정을 반박한 게 아니라 *전제로 깔고 우회*했다** — 정작 저자는 그렇게 말하지 않는다. ⭕ 저자도 구멍은 안다: *"the DOS result of Li₃N **only indicates the absence of significant interfacial electronic states** … whereas its role as a fast Li⁺-transport phase **cannot be inferred from DOS analysis alone**"* |
| **🔴 LiCl 이동장벽이 우리 표 안의 `[Lu]` 와 ≈10배 갈린다 — 우리 "LiCl = 저장벽 buffer" 행에 충돌 표기가 필요하다** — 이 편의 CI-NEB: **LiCl 0.4800 · LiBr 0.5615 · LiF 0.6367 eV** 이고, 본문이 명시적으로 못박는다 — *"LiCl/LiBr should be understood primarily as **interfacial homogenization components rather than rapid ion-conduction phases**"* | **[Li26FDI]** `Fig. 1i,k,l` (VASP CI-NEB, 10⁻⁵ eV / **0.02 eV Å⁻¹**) ↔ **[Lu]** `Fig. 6` (LiCl **0.05 eV**) | 우리 `sei_neb.json` = **`retracted: true`, `n_citable: 0`** (`v3/licl` 은 `Ea_forward_eV: None` 미완) → **우리는 심판을 못 본다** | 🔴 **두 문헌이 10배 갈리고 원인을 특정할 수 없다** — 양쪽 다 **결함 기구(공공 vs 침입형)를 안 밝혔다**(이온결정에서 이 둘은 통상 수 배 차이). ⚠ 앞으로 `[Lu]` 의 "LiCl 저장벽" 을 인용할 때 **이 충돌을 병기**한다. ⭕ 부수 소득: **"할라이드 SEI 가 Li⁺ 를 잘 통한다" 는 통념을 저자가 자기 계산으로 부인**한 드문 활자 |
| **LiF/LiCl–LiBr/Li₃N 3성분 인공 계면상 → CCD 0.398→3.581 mA cm⁻²(9×) · 대칭셀 800 h@0.398 · 풀셀 1 C 1000 사이클** (LiFSI@DME → LiCl/LiBr@THF → TMEDA 3단 습식, 총두께 **≈60 μm**) — 단성분: LiF-rich 1.393(3.5×) · Li₃N 0.796(2×) · LiCl/LiBr 0.597(1.5×) | **[Li26FDI]** `Fig. S8`–`S11` · `Fig. 5b` · `Fig. 6e` · `Table S1` | comp1/modelc 0 V 분해식 **Li₃P + 5 Li₂S + LiCl**(grand-potential) · `sei_products.json` 음극쪽 처방(O 도입 → Li₂O 로 Li₃P 대체) | 🟡 **방향은 같다**(전자차단 상을 Li 쪽에 깔면 CCD 가 오른다 — §E 진영 `[Li25]`·`[Wu26]`·`[LiInF]`·`[WangYO]`·`[Xu26NdO]` 와 동형). ⛔ **그러나 우리 산물 5종(Li₃PO₄·Li₂SO₄·Li₂S·LiCl·Li₃P) 관측은 0/5 다** — 이 논문엔 **S 2p·P 2p XPS 가 한 장도 없고 순환 후 XPS 도 0건**이며, 등장하는 LiCl 은 *분해산물이 아니라 뿌린 코팅*이다. 같은 축의 `[Li25]`·`[Wu26]`·`[WangYO]` 가 순환 후 XPS 로 Li₂S/Li₃P/LiCl 를 직접 잡은 것과 비교해 **명확한 열위**. 🔴 성능 인용 시 **초록의 `77.1 over 1000 cycles` 를 그대로 옮기면 틀린다** — 1000번째는 **≈47 mAh g⁻¹**(Table S1 유지율 61.2 % 검산 + `Fig. 6e` figure-read ≈48) |

--- (b-2) "### J-7. 🔧 방법 원전 — *물성값이 없어서 표에 못 넣는 편*" 블록에 추가할 소절 ---
    (⚠ 이 논문은 §E 에 이미 행 3개가 있다. 여기는 **값이 아니라 규약**만 따로 둔 것이다.)

**[Li26FDI] `li2026_functionally_differentiated_interphase` — ① CCD 계단 보고 규약(반면교사) ② NEB 끝점 축퇴 게이트 ③ 계면 CDD 의 isovalue 규약**

| 항목 | [Li26FDI] | 우리 | 판정 |
|---|---|---|---|
| **★★ CCD 보고 규약** | 보고값 8개가 **전부 `0.199 mA cm⁻²` 의 정수배**(n = 2/3/4/7/11/18). 즉 "마지막 통과 계단" 인데 **4자리 유효숫자**(3.581)로 인쇄 | 우리는 CCD 실험이 없다 | 🔴 **반면교사.** 계단시험 보고량은 **①계단 크기 ②마지막 통과 ③실패 계단 ④전극 면적** 을 같이 적어야 한다. 이 논문은 **전극 면적을 안 밝혀** 0.199 의 출처(전류÷면적)조차 특정 불가. `kb/templates/estimand_card.md` 의 "보고량 정의" 항목 후보 |
| **★★ NEB 끝점 축퇴** | `Fig. 1j`(Li₃N 0→**−0.0082**) · `Fig. 1m`(LPSCl 0→**−0.152 eV**) **둘 다 끝점 비축퇴** — 그런데 정방향 장벽만 보고. LPSCl 역방향은 ≈**0.40 eV** | `db/properties/sei_neb.json` 은 결과마다 **`endpoints_symmetry_equivalent`** 를 저장하고 False 면 blocking | ⭕⭕ **우리 게이트가 더 엄격하다.** 우리 NEB 캠페인은 `retracted`(n_citable 0)이지만 **이 게이트만은 살아 있다** — 방법론 카드에 쓸 만한 자산 |
| **★ NEB 수렴 하한** | 힘 허용 **0.02 eV Å⁻¹** 로 **0.0103 eV**(Li₃N, 이미지 간격 ≈0.44 Å → 허용오차 ≈0.009 eV)·**0.0166 eV**(LPSCl intra-cage, 간격 ≈0.6 Å → ≈0.012 eV)를 보고 | — | 🔴 **장벽 ≈ 오차.** 게다가 CI-NEB 는 사슬당 **한 이미지만** 안장점으로 올리므로 부차 극대(0.0166)는 수렴 안장점이 아니다. ⛔ *"Li₃N 이 Li₂O 보다 23배 빠르다"* 식 비율 인용 금지 |
| **★ 계면 CDD 규약** | 차등전하밀도 11패널에 **isovalue 미표기 · 적분(Bader) 0 · 평면평균 Δρ(z) 0** → 패널 간 "뚜렷/완만" 비교가 정량이 아니고, 실제로 **본문 서열이 그림 인상과 어긋난다**(우리 판독: Li₂O·Li₃N 로브가 LiF 보다 크다) | 우리 CDD 그림(하우스 스타일) | ⭕ **우리 규약으로 못박자**: CDD 에는 **isovalue + Bader 적분 전하**를 항상 병기. 바른 예는 `[Luo22]` (Bader 로 전해질 순전하 정량) |
| **★ 전자차단 주장의 필요조건** | "전자차단" 을 **각 상의 단일상 DOS** 로만 논증. **밴드정렬·일함수·Schottky 장벽·계면 PDOS 전부 없음**. 게다가 7패널이 **각자 E_F 에 정렬**돼 공통축이 아니다 | 우리 `sei_products.json` 갭 사다리도 **정렬이 아니라 갭**이다 | 🟡 **우리에게도 같은 구멍이 있다.** 계면 전자주입은 갭이 아니라 **정렬**이 정한다 → 우리 SEI 전자차단 주장에 **슬랩 일함수라도 붙이는** 것이 다음 숙제 |
| **⛔ 미기재 전수** | k-메시 · 슈퍼셀 크기/원자수 · 진공층 · vdW · 스핀 · NEB 이미지 수 · **결함 기구(공공/침입형)** · **S²⁻/Cl⁻ 무질서 처리** · 계면/DOS 계산의 수렴기준 · 시각화 도구 | 우리는 `protocol_hash`/`protocol_payload` 에 전량 박는다 | 🔴 **재현 불가.** 특히 **아지로다이트 무질서 미처리**가 치명적이다 — 우리 comp2 실측으로 배열에 따라 Ea 가 **0.275 ↔ 0.151 eV**(1.8배). `Fig. 1m` 끝점이 −0.152 eV 인 것 자체가 **특정 단일 배열**의 증거 |
| **사장된 방법 2건** | SI 식 **(S1) 계면에너지 γ** 정의만 있고 **값이 어디에도 없음** · SI 물리분석절의 **XRD** 도 **데이터 0장** | — | ⚠ 성분 선택의 **열역학 근거가 통째로 비어 있다**. 우리가 이 편을 "계면에너지로 코팅을 골랐다" 로 인용하면 **틀린다** |

═══════════════════════════════════════════════════════════════════════════
(c) litdb/comparison_vs_ours.md — "## 📑 Reference key (출처 약칭)" 표에 넣을 행 1줄
    [4열: | 약칭 | 논문 (저자·년·저널) | digest/status | 유형 |]
═══════════════════════════════════════════════════════════════════════════

| **[Li26FDI]** ⭐ 황화물/Li 금속 **인공 3성분 계면상** · ★ **`Li₃P = conductor-LEAK` 논쟁의 세 번째 입장**(우리 "전자 누설" ↔ `[Xiao20Rev]` "부동태" ↔ 이 편 "이온수송 불량") · 🔑 저자가 고른 대체재 **Li₃N 이 자기 `Fig. 1g` 최협갭**(figure-read ≈1.1 eV) = 우리 기준 같은 `conductor-LEAK` 칸 | **Xuebao Li**/Chao Zhao/Yueqing Peng/Kun Zeng/Shijie Han/Zekai Zhang/**Zhuangzhi Wu\***/**Dezhi Wang\*\*** (Central South University MSE + State Key Lab of Powder Metallurgy, 단일기관 7인) 2026 ***J. Energy Storage* 181, 124529** (DOI 10.1016/j.est.2026.124529; 수신 2026-06-10 / 수락 2026-08-26 / 온라인 2026-09-10; NSFC 52374407; inbox #115 본문 11 pp · **SI `.docx`** · refs 47 · 그림 6장 · 표 0장) — "**Functionally differentiated composite interphase enables stable sulfide-based all-solid-state lithium metal batteries**" | `papers/li2026_functionally_differentiated_interphase.md` (2026-09-12, 그림 **6/6 실독** · SI 는 `.docx` 라 이미지 없음 → **텍스트 206문단 전수 파싱**) | 실험 주도(SEM/EDS·XPS·AFM·CCD·대칭셀·풀셀) + **얇은 DFT**(VASP/PBE/PAW/520 eV; 계면 슈퍼셀 11 · DOS 7 · CI-NEB 6) · ⛔ **k-메시/셀/진공/vdW/스핀/이미지수/결함기구/무질서 전부 미기재 · 밴드갭 숫자 0 · 계면에너지 γ 정의만 있고 값 없음 · S 2p·P 2p XPS 0 · 순환 후 XPS 0 · σ·EIS·XRD 데이터 0** · 🔴 **초록 수치 오류 1건**(`77.1 over 1000 cycles` → 실제 ≈47) |

-->
