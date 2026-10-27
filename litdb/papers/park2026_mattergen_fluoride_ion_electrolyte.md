<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-10-27 신규 작성 — 논문 에이전트 병렬 9 편 중 1 편 (사용자 목록 #3).
     그림: 추출기가 본문 PDF 에서 캡션 후보를 0 개 잡았다 (Research Square 레이아웃 = 'Figure N' 이 단독 줄 + 캡션 문단이 래스터 아래).
           본문 Fig. 1–7 은 손 크롭 (figures.json `manual_crop`) · SI Fig. S1 · Table S1–S9 는 자동.
           번호 공백 탐지기는 f7 하나만 올렸다 — 본문 그림이 0 장이면 공백을 잴 기준점이 없다 (도구 맹점 · 이번엔 고치지 않음).
     읽기축: 우리 1단계 스크리닝 깔때기 (조성 후보 → MLIP 완화 → 문턱) 의 검증 사다리 + 생성형 역설계 로드맵. -->

# Generative Inverse Design of Solid-State Fluoride-Ion Electrolyte Candidates in Data-Sparse Chemical Space — Park, Choi, Heo, Jeong (Research Square preprint 2026)

> slug `park2026_mattergen_fluoride_ion_electrolyte` · DOI `10.21203/rs.3.rs-11026639/v1` · type `DFT + ML (확산 생성모형 MatterGen · MLIP 사전선별 MatterSim · GNN 갭 예측 ALIGNN)` · PDF `a8a0ec62-3._Generative_Inverse_Design_of_Solid-State_Fluoride-Ion_Electrolyte_Candidates_in_Data-Sparse_Chemical_Space.pdf` (22 pp = 표지 · 원고 · 참고문헌 45 편 · 그림 7 장 p.17–22) + `a7a43323-3._Sup_Generative_….pdf` (SI 11 pp · `Fig. S1` + `Table S1`–`Table S9`) · digested `2026-10-27` · status ✅ · 태그 **[외부 · 불화물 이온 (F⁻) 전지 고체전해질 · ⛔ Li 황화물 아님 → 물성 4축 수치 비교 제외 · 🔧 깔때기 · MLIP 사전선별 검증의 방법 원전]**

> elements: F, Ni, Li, Na, K, Cs, Bi, Fe, Cu, Sn, Pb, Ce
> methods: DFT, MLIP, elastic

> **저자**: Joohyeon Park† · Seonwoo Choi† (가천대 전자공학과) · Myeongjae Heo (서강대 기계공학과) · **Heonjae Jeong\*** (서강대 기계공학과 + 스마트설계·제조기술연구소) · †공동 1저자 · 게시 **2026-10-09 (v1)** · **CC BY 4.0** · 서강대 교내연구비 202510019.01 · KISTI Nurion·Neuron · 코드 · 최종 구조 · 그림 원자료 `github.com/Jeong-Research-Group/FIB`
> ⚠ **미심사 preprint** (Research Square 표지: *"preliminary reports that have not undergone peer review"*). SI 파일명 `SMnpjComputMaterJeong.docx` → *npj Comput. Mater.* 투고본으로 보인다 (추정 · 본문에 명시 없음).
> 🎤 관련 발표: 없음 (talk 인입 대기열 확인 2026-10-27).

---

## 0. 이 digest 를 읽는 법

**왜 먹었나 — 셋.**
1. 우리 1단계 스크리닝 깔때기 (조성 후보 → UMA 완화 → 문턱; `kb/methodology/dopant_screening_funnel_2026_06_13.md` 의 342 배열 → UMA → 1 · cascade Stage 00–12 `comparison_vs_ours.md` §J-10) 와 **같은 꼴** — *MLIP 사전선별 → DFT 검증 → 물성 문턱* — 을 생성형 모형 뒤에 붙인 litdb 첫 **1차** 사례다. MatterGen 은 지금까지 `jain2026_ml_pipelines_solid_state_electrolyte_design` 리뷰의 2차 인용으로만 있었다.
2. 생성형 역설계는 우리 로드맵에 **미착수**로 있다 (`kb/projects/digital_twin_roadmap.md` 의 "Inverse design (generative model)" · `kb/fairchem/05_papers_and_insight_workflow.md` 7 번).
3. 계가 F⁻ 전도체 후보 (Ni 불화물) 라 **물성값은 하나도 우리 표로 오지 않는다.** 가져오는 것은 **검증 사다리의 설계와, 그 사다리가 어디서 미끄러지나**다.

**결론부터**
- ✅ **가져올 것**: 두 팔 (일반 모형 · 불화물 전용 모형) 의 **단별 생존수 전부 공개** (`Fig. 1`) · 사후 중복 분석과 그 설정 공개 · 대칭 허용오차 견고성 표 (`Table S4`, `Table S6`–`Table S9`) · 저자 스스로 그은 한계 문장 셋 (*"prioritized computational leads, not validated solid electrolytes"* · 띠 정렬은 *"not a complete … stability window"* · 28 배는 *"largely definitional"*).
- ⛔ **가져오면 안 되는 것**: ① 후보 에너지 (VASP PBE · **비스핀 · U 없음 · 보정 없음**) 를 Materials Project hull 에 **그대로** 댄 Ehull — Ni–F 계 MP 엔트리는 GGA+U 다 ② 고스핀 Ni²⁺ (자기모멘트 1.82–1.92 μB, `Table S2`) 계의 **비스핀** HSE06 갭 · 탄성 · 띠 끝 · 계면 반응에너지 ③ **문턱을 통과한 것만** 그린 parity 로 *"MLIP 가 관대하니 위음성이 최소"* 라고 말하는 것 (`Fig. 4` — y 0.10 위로 점이 0 개) ④ **결과 지표 (가장 유리한 띠 정렬) 로 슬랩 종단을 고르는 것** (`Fig. 6`).
- ⚠ **빠진 단**: **이온 수송이 깔때기에 없다** (이동 장벽 · MD · BVSE · 결함 계산 0) — 저자도 인정한다. 제목의 *"electrolyte candidates"* 를 받치는 단이 없다.

> **본 digest 에서 실제로 본 그림 (2026-10-27)**: `Fig. 1` · `Fig. 2` (원 래스터 확대로 (a)·(b) 칸 숫자 판독) · `Fig. 3` (네 패널 막대를 픽셀로 적분) · `Fig. 4` · `Fig. 5` · `Fig. 6` · `Fig. 7` · `Fig. S1` (막대 30 개 픽셀 판독) — **그림 크롭 8 장 전부**.
> 이미지로 안 본 것: `Table S1`–`Table S9` 크롭 9 장 — 표는 PDF 텍스트로 읽고 텍스트 추출로 숫자를 대조했다.
> 본문 서술과 어긋난 그림: `Fig. 2a` (캡션 ↔ 내용) · `Fig. 2b` (F 칸 ↔ 13,235) · `Fig. 3d` (적분 ↔ 13,235) · `Fig. 4b` (*"consistent offset"* ↔ 넓은 산포) · `Fig. 6` (PbSnF₄ 기준도 창을 둘러싼다 — 본문 언급 없음) · `Fig. 1` (*"SUN screening"* 라벨 ↔ Methods 'U·N 으로는 안 지웠다'). 상세 §5 · §10.
> 그림에서만 읽은 값은 **`figure-read ≈`**, 우리가 계산한 값은 **우리 산수**로 표시했다.

---

## 1. 한 줄 요약

MatterGen (확산 생성모형) 에 **Ehull 하나만 조건**으로 걸어 일반 모형 (Alex-MP-20) 에서 108,000 · 불화물 전용 모형 (MP-F) 에서 21,600 구조를 뽑고, MatterSim (Ehull ≤ 0.1) → ALIGNN (Eg ≥ 3.5 eV) → 조성 · 산화수 → DFT (Ehull ≤ 0.02 · O/H 제외 · HSE06 Eg ≥ 3.5) → Born 탄성 깔때기로 **Ni 불화물 5 종** (LiNi₂F₅ · CsNaNi₂F₆ · NiF₂ 다형 · KNi₂F₅ · NaNi₂F₅) 을 남겼다. 불화물 전용 학습은 표본당 안정 불화물 수율을 **≈28 배** (218 → 6,127 / 10⁴ 표본) 올렸지만 저자 스스로 "대부분 정의상" 이라 하고, 안정 불화물에서 최종까지의 생존율은 **0.042 % vs 0.030 %** 로 같다. KNi₂F₅ · NaNi₂F₅ 가 띠 정렬 · 계면 반응으로 1 순위 (KNi₂F₅ 는 강성도 최대), CsNaNi₂F₆ 가 2 순위다.

⚠ 단 셋: ① **이온전도 단이 없다** ② 선별 단계의 에너지 · 갭 · 탄성 · 띠 끝 · 반응에너지가 전부 **비스핀 · U 없음** 이고 MP 기준과 **보정 없이** 섞였다 (Ni²⁺ 는 고스핀 자성) ③ 5 종이 전부 Ni 인 이유를 저자는 *"학습 말뭉치에 Ni 불화물이 흔해서"* 라고 하지만, 불화물 전용 모형의 생성 분포 (`Fig. 2b`) 에서 Ni 는 V · Mn 보다 5–7 배 드물다 (figure-read) — **선별 프로토콜이 Ni 를 골랐을 가능성**을 논문이 배제하지 못한다 (§10-③).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 대상 | 고체 **불화물 이온 전지 (FIB)** 전해질 — 운반자가 F⁻. 서론: 이론 체적 에너지밀도 **~5000 Wh L⁻¹** (ref 9 인용) · 불연성 무기 고체와 궁합이 좋다 |
| 문헌 갭 | 빠른 F⁻ 전도체가 드물고, 연구가 **LaF₃ (tysonite) · PbSnF₄ (fluorite 계)** 의 좁은 이원 · 고용체 계에 몰려 있다. DFT · HT · 진화 탐색은 정해 둔 조성 · 원형 안에서만 돈다 |
| 질문 ① | 양이온 · 화학량 · 공간군 · 모체 구조를 **안 정하고**, 안정도만 조건으로 건 생성형 모형이 데이터 희소 영역의 후보를 내나 |
| 질문 ② | 학습 데이터 분포 (조성 일반 vs 불화물 전용) 가 생성 효율을 어떻게 바꾸나 |
| 두 팔 | **Alex-MP-20**: 공개 MatterGen (Alexandria + MP · 607,683 학습 / 67,521 검증 · ≤20 원자/셀 · Ehull < 0.1) → Ehull 조건 미세조정 · **MP-F**: MP v2022.10.28 중 F 함유 **13,414** (방사성 · 비활성기체 제외 · 원자수 · Ehull 제한 **없음**) 로 사전학습 → Ehull 조건 미세조정 |
| 표본 | 2,160 구조/런 (216 × 10 배치) — Alex **50 런 = 108,000** · MP-F **10 런 = 21,600** (5 배 차) |
| 저자 주장 | (i) 생성 분포는 학습 말뭉치의 조성 사전분포가 지배한다 (ii) 도메인 정렬 = 안정 불화물 수율 ≈28 배, 단 효과는 불화물 보존 단에 몰려 있고 정의상이다 (iii) Ni 계 5 종 — **KNi₂F₅ · NaNi₂F₅ 우선**, **CsNaNi₂F₆ 2 순위** (iv) 무제약 생성 + 물리 기반 선별이 미개척 영역을 연다 (*"principal advance"*) |
| 스스로 둔 한계 | 이온전도 미확인 (결함 · 장벽 · MD · 임피던스가 다음 단) · 비스핀 선별값은 근사 · 띠 정렬 ≠ 안정창 · 0 K 반응에너지는 순위만 · Ni 자체가 공급 제약 원소 |

---

## 3. 핵심 수치 총정리 ★

### 3a. 생성 설정

| 항목 | Alex-MP-20 팔 | MP-F 팔 |
|---|---|---|
| 학습 말뭉치 | Alexandria + MP, 607,683 학습 / 67,521 검증 · ≤20 원자/셀 · Ehull < 0.1 eV/atom | MP v2022.10.28 F 함유 13,414 · 방사성 · 비활성기체 제외 · 원자수 · Ehull 제한 없음 |
| 학습 경로 | 공개 사전학습 모형 → Ehull 조건 미세조정 | MP-F 로 사전학습 → Ehull 조건 미세조정 |
| 조건 · 샘플링 | Ehull 목표 **0.05 eV/atom** · guidance factor **2.0** · 확산 **1,000 스텝** | 같음 |
| 런 | 2,160/런 × **50** = **108,000** | × **10** = **21,600** |
| 사후 중복 (StructureMatcher) | **1,628 (1.5 %)** | **7,020 (32.5 %)** |
| 중복 제거 | 안 함 — 본문의 모든 수는 중복 포함 | 같음 |
| 신규성 (N) · 유일성 (U) 비율 | 평가는 했다고 쓰지만 **수치 미보고** (n/a) | 같음 |

### 3b. 깔때기 단별 생존 (`Fig. 1` + 본문 p.4) ★

| 단 | 기준 | Alex-MP-20 | 단 통과율 (우리 산수) | MP-F | 단 통과율 (우리 산수) |
|---|---|---|---|---|---|
| 0 | 생성 | 108,000 | — | 21,600 | — |
| 1 | MatterSim Ehull ≤ 0.1 eV/atom (`Fig. 1` 라벨 "SUN screening" — 실제 제거는 S 만) | 76,344 | 70.7 % | 13,235 | 61.3 % |
| 2 | F 함유 (`Fig. 1` 라벨 "Fluoride-only") | 2,356 | 3.09 % | 13,235 | 100 % (구성상) |
| 3 | ALIGNN Eg ≥ 3.5 eV | 672 | 28.5 % | 1,259 | **9.5 %** |
| 4 | 비활성기체 · 방사성 · Hg 제외 | 670 | 99.7 % | 1,227 | 97.5 % |
| 5 | 형식 산화수 전하중성 | 438 | 65.4 % | 877 | 71.5 % |
| 6 | DFT 수렴 | 404 | 92.2 % | 801 | 91.3 % |
| 7 | **DFT Ehull ≤ 0.02 eV/atom** | **14** | **3.5 %** | **57** | **7.1 %** |
| 8 | O · H 함유 제외 | 8 | 57.1 % | 28 | 49.1 % |
| 9 | HSE06 Eg ≥ 3.5 eV (두 팔 합 36 → 18) | 5 | 62.5 % | 13 | 46.4 % |
| 10 | Born 탄성 안정 (두 팔 합 18 → 5, *"excluded thirteen"*) | **1** | 20 % | **4** | 30.8 % |

> 🔑 **세 단이 깔때기를 정한다** — ⑦ DFT Ehull (3.5 % / 7.1 % 통과) · ⑨ HSE06 갭 (두 팔 합 **절반 탈락**) · ⑩ Born (두 팔 합 **72 % 탈락**). ⑧ O/H 제외는 **조성 규칙인데 DFT 뒤**에 있어서 DFT 생존자의 43–51 % 를 버린다 (§10-⑫).

### 3c. 수율 · 비율

| 양 | Alex-MP-20 | MP-F | 비고 |
|---|---|---|---|
| 안정 비율 (MatterSim) | 70.7 % | 61.3 % | 일반 모형이 높다 — *"modest cost in stability conditioning"* |
| 안정 구조 중 F 함유 | 3.09 % (2,356) | 100 % | MP-F 는 구성상 (단 `Fig. 2b` 판독은 §5.2) |
| 표본 10⁴ 당 안정 불화물 | **218** | **6,127** | 비 **28.1×** (우리 산수, 본문 "≈28") |
| 안정 불화물 → 최종 | 1/2,356 = **0.042 %** | 4/13,235 = **0.030 %** | 저자: *"similar observed final-candidate retention"* · n = 1 대 4 |
| `Fig. 3a` · `Fig. 3b` 첫 칸 (MatterSim Ehull 0–0.025) | `figure-read ≈` 25,170 (안정의 ≈33 %) | `figure-read ≈` 7,130 (안정의 **≈54 %**) | 네 칸 합 ≈76,190 · ≈13,080 → 라벨과 맞아 판독 검증됨 |

### 3d. MatterSim vs DFT Ehull (`Fig. 4`)

| 양 | Alex-MP-20 | MP-F |
|---|---|---|
| RMSE / MAE | **0.06 / 0.06 eV/atom** | **0.07 / 0.07 eV/atom** |
| 방향 | MatterSim 이 계통적으로 **낮다** (저자) | 같음 (저자) |
| 표본 | MatterSim ≤ 0.1 + 이후 필터 통과 + DFT 수렴 = 404 | 801 |
| `figure-read` | 띠 모양 상관 · 띠 중심 오프셋 ≈0.06 · **y 0.10 위로 점 0 개** | 상관 약함 · **y = 0 줄** (MatterSim 0, DFT 0.02–0.20) + **x = 0 열** (DFT 0, MatterSim 0–0.09) · y 0.10 위로 점 0 개 |

### 3e. 최종 5 종 — 구조 (`Table S1` · symprec 은 Methods)

| 후보 | 팔 | 공간군 (채택 symprec) | 원자/셀 | a, b, c (Å) | α, β, γ (°) | V (Å³) | V/원자 (우리 산수) |
|---|---|---|---|---|---|---|---|
| LiNi₂F₅ | Alex | *P*1 (0.001 Å) | 8 | 4.0, 5.4, 5.2 | 74.3, 67.3, 68.2 | 94.5 | 11.8 |
| CsNaNi₂F₆ | MP-F | *P*4/*mmm* (0.1) | 10 | 5.8, 4.0, 5.8 | 90.0, 89.9, 90.0 | 135.1 | 13.5 |
| NiF₂ | MP-F | *P*-1 (0.01) | 9 | 3.1, 4.7, 7.5 | 94.7, 102.1, 89.9 | 106.0 | 11.8 |
| KNi₂F₅ | MP-F | *C*2 (0.01) | 8 | 4.1, 3.9, 6.6 | 90.1, 71.7, 90.0 | 99.9 | 12.5 |
| NaNi₂F₅ | MP-F | *Pm* (0.02) | 8 | 3.9, 4.0, 6.5 | 72.1, 89.9, 89.9 | 95.6 | 12.0 |

- 전하 균형: A⁺ + 2 Ni²⁺ = 5 F⁻ (ANi₂F₅) · Cs⁺ + Na⁺ + 2 Ni²⁺ = 6 F⁻ — **전부 Ni²⁺**.
- NiF₂ 는 MP 의 정방 (*P*4₂/*mnm*) · 사방 (*Pnnm*) 과 **다른 다형** — symprec 0.10 → 0.001 Å 어디서도 그 둘로 안 간다 (`Table S4`).
- ⚠ 구조는 전부 **비스핀 PBE 이완** 결과다 (`Table S1` 캡션).

### 3f. 자성 (`Table S2` · `Table S3`) ★

| 후보 | μ_Ni FM / AFM (μB) | E_NM / E_FM / E_AFM (eV/f.u., PBE+U) | 바닥 | E_FM − E_AFM | **NM − 바닥** (eV/f.u.) | NM − 바닥 (eV/Ni · eV/atom, 우리 산수) | 0.02 eV/atom 문턱의 몇 배 (우리 산수) |
|---|---|---|---|---|---|---|---|
| LiNi₂F₅ | 1.87 / 1.87 | −28.28 / −34.11 / −34.10 | FM (0.01 차) | −0.01 | **5.83** | 2.91 · **0.729** | **36×** |
| CsNaNi₂F₆ | 1.89 / 1.85 | −35.79 / −39.63 / −39.82 | AFM | +0.19 | 4.03 | 2.02 · 0.403 | 20× |
| NiF₂ | 1.82 / 1.82 | −10.74 / −11.38 / −11.57 | AFM | +0.19 | 0.83 | 0.83 · 0.277 | 14× |
| KNi₂F₅ | 1.92 / 1.91 | −29.97 / −32.31 / −32.35 | AFM | +0.04 | 2.38 | 1.19 · 0.298 | 15× |
| NaNi₂F₅ | 1.92 / 1.92 | −29.79 / −32.01 / −32.06 | AFM | +0.05 | 2.27 | 1.14 · 0.284 | 14× |

- PBE+U (Dudarev, U_eff = 6.2 eV, Ni 3d — MP 관례) · NiF₂ 는 Ni 3 개 셀이라 짝수 Ni 슈퍼셀.
- 본문: FM–AFM 은 LiNi₂F₅ · KNi₂F₅ · NaNi₂F₅ 에서 0.05 eV/f.u. 안 (거의 축퇴), CsNaNi₂F₆ · NiF₂ 는 AFM 이 0.19 eV/f.u. 우위 ✓ (표와 일치).
- 모멘트 1.82–1.92 μB = **고스핀 Ni²⁺ (S = 1)** 이 공유결합으로 조금 줄어든 크기 (해석 · 우리).
- ⚠ 여기 NM 은 **PBE+U 비스핀**이라 선별 단계 (**PBE · U 없음** · 비스핀) 의 비스핀 벌점 자체는 아니다 (그 값은 n/a). 그래도 **스핀 처리 하나로 0.28–0.73 eV/atom 이 움직인다**는 규모는 Ehull 문턱 (0.02) 옆에 놓고 볼 만하다.
- ⚠ **LiNi₂F₅ 의 NM 벌점이 Ni 당 2.91 eV** 로, 같은 ANi₂F₅ 꼴의 K (1.19) · Na (1.14) 의 2.5 배다 — 논문 설명 없음 (§10-⑬).

### 3g. 탄성 (`Table S5`, 비스핀 PBE) + 우리 산수

| 후보 | B V / R / **H** (GPa) | E V / R / **H** | G V / R / **H** | ΔB (V−R) | A^U (우리) | B_H/G_H (우리) | ν (우리) |
|---|---|---|---|---|---|---|---|
| LiNi₂F₅ | 65.74 / 53.35 / **59.54** | 74.62 / 61.19 / **67.90** | 28.46 / 23.37 / **25.92** | 12.39 | 1.32 | 2.30 | 0.310 |
| CsNaNi₂F₆ | 72.02 / 71.87 / **71.94** | 81.54 / 76.94 / **79.25** | 31.10 / 29.11 / **30.10** | **0.15** | **0.34** | 2.39 | 0.316 |
| NiF₂ | 83.65 / 66.84 / **75.24** | 71.38 / 62.46 / **66.94** | 26.29 / 23.23 / **24.76** | 16.81 | 0.91 | 3.04 | 0.352 |
| KNi₂F₅ | 86.12 / 84.22 / **85.17** | 99.63 / 87.87 / **93.78** | 38.11 / 33.13 / **35.62** | 1.90 | 0.77 | 2.39 | 0.316 |
| NaNi₂F₅ | 84.27 / 66.50 / **75.38** | 81.80 / 52.61 / **67.28** | 30.56 / 19.23 / **24.90** | **17.77** | **3.21** | 3.03 | 0.351 |

- 검산: B_H · G_H = (V+R)/2 ✓ · **E_H = 9B_H·G_H/(3B_H+G_H)** 로 표의 E_H 가 ±0.01 GPa 재현된다 (우리 산수 — E 는 V·R 평균이 아니라 B_H·G_H 에서 유도).
- A^U = 5G_V/G_R + B_V/B_R − 6 (Ranganathan–Ostoja-Starzewski 보편 이방성 지수, 0 = 등방) · ν = (3B−2G)/(2(3B+G)).
- 본문 서술 검산: KNi₂F₅ 가 가장 단단 (B_H 85.2 · E_H 93.8) ✓ · NaNi₂F₅ V–R 폭 최대 (B 17.8 · E 29.2) ✓ · CsNaNi₂F₆ B 의 V–R 차 0.15 GPa ✓ · NiF₂ E · G 최저 ✓ (G 는 NaNi₂F₅ 24.90 과 0.14 차).

### 3h. 띠 끝 — 슬랩 · 진공 기준 (`Fig. 6` 인쇄 라벨 · 본문에는 숫자 없음)

| 계 | 종단 | CBM (eV) | VBM (eV) | 갭 (우리 산수) | CBM − anode (−3.33) | F₂/F⁻ (−7.33) − VBM | 창을 둘러싸나 |
|---|---|---|---|---|---|---|---|
| LiNi₂F₅ | F | −4.56 | −8.99 | 4.43 | −1.23 | +1.66 | ✗ (CBM 이 창 안) |
| CsNaNi₂F₆ | Cs | −3.90 | −7.74 | 3.84 | −0.57 | +0.41 | ✗ (CBM) |
| NiF₂ | Ni | −2.47 | −6.04 | 3.57 | +0.86 | −1.29 | ✗ (VBM 이 창 안) |
| **KNi₂F₅** | K | −3.03 | −7.78 | 4.75 | +0.30 | +0.45 | ✓ |
| **NaNi₂F₅** | Na | −2.93 | −7.55 | 4.62 | +0.40 | +0.22 | ✓ |
| PbSnF₄ (기준) | n/a | −3.26 | −8.35 | 5.09 | **+0.07** | +1.02 | ✓ (**본문 언급 없음**) |

- 창 = **F₂/F⁻ −7.33 eV** (Bratsch 표준전위 + Trasatti 절대전위 · 환산 상수는 본문에 없음) ~ **"가상 4 V anode" −3.33 eV** (= F₂/F⁻ + 4.00 V).
- 갭은 **슬랩 · 비스핀 HSE06** 값이다. 벌크 HSE06 갭은 후보별로 안 나온다 (≥ 3.5 라고만).

### 3i. 계면 반응에너지 (`Fig. S1` 막대 · `figure-read ≈` 픽셀 판독 ±0.02 eV/atom)

| 전해질 \ 전극 | FeF₃ | BiF₃ | CuF₂ | Sn | Pb | Ce |
|---|---|---|---|---|---|---|
| LiNi₂F₅ | −1.13 | −0.84 | −0.88 | −0.90 | −1.09 | −1.59 |
| CsNaNi₂F₆ | −1.10 | **−0.74** | −0.78 | −0.84 | −0.95 | −1.25 |
| NiF₂ | −1.20 | −0.99 | −1.05 | −1.07 | −1.27 | **−1.89** |
| KNi₂F₅ | −1.15 | −0.81 | −0.84 | −0.88 | −1.01 | −1.54 |
| NaNi₂F₅ | −1.15 | −0.82 | −0.86 | −0.90 | −1.05 | −1.54 |

- 본문에 나온 숫자는 *"모든 쌍이 ≈ −0.7 eV/atom 보다 음수"* 하나뿐이다. 표 값은 전부 그림 판독.
- **여섯 열 모두에서 순서가 같다**: CsNaNi₂F₆ (가장 덜 음수) < ANi₂F₅ 셋 < NiF₂ (가장 음수) — 전극 종류와 무관 (§10-⑥).

### 3j. 논문에 **없는** 값 (n/a)

후보별 DFT Ehull 숫자 (≤ 0.02 라고만) · 후보별 벌크 HSE06 갭 · 신규성 · 유일성 비율 · C_ij 성분 (평균만) · 포논 · **이온전도도 · 이동 장벽 · 결함 형성에너지 · MD** · 계면 반응 최소점의 x 와 생성물 · MatterSim 판 · ALIGNN 판 (어느 범함수의 갭을 예측하나) · HSE06 · 슬랩 k-격자 · 탄성 계산법 (변형 집합 · relaxed-ion 여부) · PbSnF₄ 기준 계산 조건 · hull 에 쓴 MP 엔트리 판.

---

## 4. DFT/계산 방법 ★

### 4a. 생성 — MatterGen (ref 19 · Zeni *et al.*, *Nature* 639, 624 (2025))
- 확산 생성모형 · 기본 ≤20 원자/원시셀 · **Ehull 하나만 조건** (목표 0.05 eV/atom · ref 30 Sun 2016 준안정 척도) · guidance factor 2.0 · 확산 1,000 스텝 · 2,160 구조/런 (216 × 10 배치).
- 샘플링 단계에서 양이온 집합 · 화학계 · 화학량 · 공간군 · 원형 **전부 미지정**. 불화물 관련성은 (i) MP-F 학습 말뭉치 또는 (ii) Alex 팔의 사후 F 필터로만 들어간다.
- 런을 독립 반복 → 같은 구조가 여러 번 나올 수 있다 (중복은 사후 집계만, 제거 안 함).

### 4b. 사전선별
- **안정**: MatterGen 평가 파이프라인 SUN 기준 중 S — **MatterSim** (ref 31, Yang 2024 arXiv 2405.04967 · MLFF) Ehull ≤ 0.1 eV/atom. MatterSim 판 · hull 기준 엔트리 미명시.
- **유일 · 신규**: pymatgen StructureMatcher — 생성 집합 안 (유일) · Alex-MP 기준 845,997 DFT 엔트리 대비 (신규). 설정 `ltol 0.2 · stol 0.3 · angle_tol 5°` · 원시셀 환원 · 부피 스케일 켬. **통계만 내고 제거 안 함.**
- **전자 절연**: **ALIGNN** (ref 32) Eg ≥ 3.5 eV (*"consistent with the band gaps of established fluoride-ion solid electrolytes"*, ref 33 PbSnF₄). 모형 판 · 학습 대상 미명시.
- **조성**: 비활성기체 · 방사성 · Hg 제외 (ref 34).
- **산화수**: 합리적 산화수 조합 하나로라도 형식 전하가 0 이면 통과 (전이금속 가변 원자가 허용).

### 4c. DFT 검증 — VASP
- VASP (refs 35, 36) · PAW (37) · **PBE** (38) · ENCUT **520 eV** · MP 격자 역공간 밀도 **2π × 0.03 Å⁻¹** (39) · **격자 + 원자 전체 이완**, 힘 < **0.01 eV/Å**.
- 이완 구조에서 탄성상수 → VRH. 갭은 **HSE06** (40), Eg < 3.5 eV 탈락.
- ⛔ **선별 단계 전부 (이완 · Ehull · 탄성 · HSE06 띠 끝) 비스핀 · U 없음.** Ehull 은 **MP hull 엔트리 대비, GGA/GGA+U 호환 보정 없이** 계산 (본문 그대로).
- Ehull ≤ **0.02 eV/atom** · 그 뒤 **O · H 함유 제외** (산화물 · 수산화물 이차상이 금속–O 결합을 키우고 F⁻ 이동도를 낮춘다는 논리, ref 11).

### 4d. 자성 재평가 (최종 5 종만)
- 스핀편극 **PBE+U_eff** (Dudarev, ref 45) · **U_eff = 6.2 eV (Ni 3d, MP 관례)** · NM / FM / AFM 비교 · NiF₂ 는 짝수 Ni 슈퍼셀.
- *"these calculations establish the preferred magnetic ordering and were **not propagated** to the screening-stage descriptors"* — 띠 끝 · 탄성 · 계면 서술자는 비스핀값 그대로. 스핀편극 상태에서 재이완했는지 n/a.

### 4e. 탄성 · 대칭
- **Born 기준** (ref 42 Mouhat–Coudert — C_ij 양의 정부호) 위반 탈락 · Hill 평균 = Voigt · Reuss 산술평균 (ref 41).
- 공간군: spglib (ref 44) via pymatgen (ref 43). **적응형 symprec** — 0.10 Å 에서 0.01 Å 간격으로 낮춰 최소 0.001 Å; *"대칭 일관 셀이 이완 격자 계량을 재현하는 가장 큰 symprec"* 을 채택 (재현 판정 수치는 없음). 각도 허용 5°. 채택값: LiNi₂F₅ 0.001 · CsNaNi₂F₆ 0.1 · NiF₂ 0.01 · KNi₂F₅ 0.01 · NaNi₂F₅ 0.02 Å.

### 4f. 띠 정렬 — 슬랩
- 이완 벌크에서 **3 층 (001) 슬랩** · z 방향 진공 **15 Å**.
- 종단: **F₂/F⁻ 준위에 대해 가장 유리한 띠 정렬을 보인 종단을 고름** → F (LiNi₂F₅) · Cs (CsNaNi₂F₆) · Ni (NiF₂) · K (KNi₂F₅) · Na (NaNi₂F₅).
- 평면 평균 정전 퍼텐셜로 HSE06 띠 끝을 진공 기준에 맞춤. **쌍극자 보정 없음** (*"비직교 슬랩 격자가 표면 법선 쌍극자 보정 방식과 맞지 않아서"*).
- F₂/F⁻ = −7.33 eV (refs 27 Bratsch · 28 Trasatti) · 가상 4 V anode = −3.33 eV · PbSnF₄ 기준 계산 조건 n/a.

### 4g. 계면 반응성
- 전극–전해질 쌍마다 결합 화학계의 **MP 엔트리로 pymatgen 기준 hull** 구성.
- 의사이원: **C(x) = xA + (1−x)B, 0 ≤ x ≤ 1** (A = 전해질, B = 전극).
- 반응에너지 = C(x) 와 그 조성의 기준 상도 평형상 사이 에너지 차 · 혼합물 원자당 · **x 를 훑은 최솟값** = 계면 반응성 · **0 K**.
- 전극: 양극 BiF₃ · FeF₃ · CuF₂ / 음극 Sn · Pb · Ce (refs 8, 29).
- 후보 (A) 에너지의 출처 = 본문 서술상 자기 DFT 값 (*"the band-edge, elastic, and interfacial descriptors were obtained from the non-spin-polarized screening-stage calculations"*). pymatgen 클래스명 · hull 에너지 대체 옵션 · 보정 적용 여부 미명시.

### 4h. 하지 않은 것
무질서 처리 (정렬 소셀 하나씩) · AIMD · MLIP-MD · NEB · BVSE · 결함 계산 · 포논 · 스핀편극 재선별 — **전부 0**.

### 4i. 재현에 필요한데 없는 것
§3j + ISMEAR · EDIFF · HSE06 혼합 · 차폐 파라미터 · 슬랩 진공 판독 위치 · MP 엔트리 내려받은 시점. ⚠ mp_api 기본 thermo type 이 `GGA_GGA+U` → `GGA_GGA+U_R2SCAN` 혼합으로 바뀐 것을 우리가 2026-10-23 에 실측했다 (`tools/doping/convex_hull_ehull.py` 주석) — 어느 판을 받았느냐가 hull 을 바꿀 수 있다.

---

## 5. 결과 — 절별 상세 (그림 실독 포함) ★

### 5.1 워크플로 (`Fig. 1`)
- 깔때기 그림: 위 "Generation" (분홍) → "High throughput screening" 6 층 → DFT 괄호 4 단 (14/57 → 8/28 → 5/13 → 1/4). 숫자는 §3b.
- 빨간 점선 상자 "Fluoride-only 2,356" 은 Alex 팔에만 걸린 F 필터. 라벨은 "Fluoride-only" 지만 실제 기준은 **"F 함유"** — O 함유 옥시불화물은 DFT 뒤 ⑧ 단에서야 빠진다.
- ⚠ 1 단 라벨 *"Ehull ≤ 0.1 eV atom⁻¹ and SUN screening from MatterSim"* ↔ Methods *"structures were not additionally removed on the basis of uniqueness or novelty"* — 그림은 SUN 으로 걸렀다고 읽히지만 실제로는 S 만 걸렀다.

### 5.2 원소 지형 (`Fig. 2`) — ⚠ 캡션과 내용이 어긋난다
- 형식: 주기율표 히트맵. (a) 색막대 0–7,000 · (b) 0–4,000 (F 칸은 검정 = 범위 밖). 칸마다 작은 숫자.
- `figure-read ≈` (원 래스터 859×1009 px 확대 판독):
  - **(a)** Tl ≈6,709 · Ag ≈6,403 · Hg ≈6,248 · **Li ≈6,206** · In ≈6,054 · Cd ≈5,972 · Au ≈5,465 · Zn ≈5,390 · Ga ≈5,228 · Cu ≈5,219 · Sm ≈5,118 · La ≈5,099 · … · Ni ≈2,863 · **F ≈2,682** · O ≈2,557 · Mn ≈1,643 · V ≈958.
  - **(b)** **F ≈11,77x** (검정 칸 · 끝자리 불확실) · Li ≈3,368 · **V ≈2,246** · O ≈2,168 · **Mn ≈1,639** · K ≈1,165 · Rb ≈1,133 · Na ≈865 · Ag ≈841 · Cs ≈814 · Fe ≈754 · Cu ≈745 · Tl ≈491 · **Ni ≈321** · Co ≈311.
- 본문 서술 (b 가 Li · O · V · F · Mn 에 몰림) ✓.
- ⚠ **어긋남 ① — (a) 는 'F 함유 안정 구조' 일 수 없다.** 캡션은 두 패널 다 *"stable (Ehull ≤ 0.1) fluoride-containing structures"* 라고 하지만, (a) 에서 F (≈2,682) 가 최댓값이 아니고 Li 등이 **F 함유 안정 구조 총수 2,356 을 넘는다.** 구조 수로 세면 F 칸 = 부분집합 크기 = 최댓값이어야 하고, 원자 수로 세면 F 가 2,356 보다 훨씬 커야 한다 — **어느 셈법으로도 성립하지 않는다.** 칸 합 ≈214,000 (우리 산수) ÷ 76,344 ≈ 구조당 2.8 원소라 (a) = **안정 Alex 출력 전체**로 읽는 게 자연스럽다 (본문 *"generated candidates that satisfy the thermodynamic stability criterion"* 과는 맞는다). ⇒ (a) 와 (b) 는 **같은 모집단의 비교가 아니다** (전체 안정 vs 불화물).
- ⚠ **어긋남 ② — (b) 의 F 칸 ≈11,77x < 13,235.** 구조 수로 셌다면 안정 MP-F 출력의 ≈1,460 개에 F 가 없다는 뜻이고 (*"generates fluorides by construction"* 과 충돌), 아니면 (b) 가 다른 부분집합이다. 판별 불가.
- 🔑 **Ni 는 생성 분포에서 소수다**: (b) 에서 Ni ≈321 은 V (≈2,246) 의 1/7, Mn (≈1,639) 의 1/5, Fe · Cu (≈750) 의 절반 아래. 그런데 최종 5 종은 **100 % Ni**. Discussion 의 설명 *"reflects the prevalence of Ni-containing fluorides in the training corpora"* 는 학습 말뭉치의 원소 통계가 안 나와 직접 검증은 못 하지만, 학습 분포를 따라가야 할 생성 분포에서 Ni 가 드물다 ⇒ **Ni 농축은 깔때기 하류에서 일어났다** (§10-③).

### 5.3 Ehull · 갭 분포 (`Fig. 3`)
- (a)(b) MatterSim Ehull 히스토그램, 0–0.5 eV/atom · 칸 0.025 · 빨간 점선 0.1. 라벨 *"Stable: 76344 / Unstable: 31656"* · *"Stable: 13235 / Unstable: 8365"* ✓. 음수 칸 없음.
  - 첫 칸 (0–0.025) `figure-read ≈`: (a) ≈25,170 (안정의 33 %) · (b) ≈7,130 (**54 %**). MP-F 는 Ehull ≈ 0 에 훨씬 몰린다 — 중복 32.5 % 와 함께 **학습 구조 재생성과 양립**하는 모양 (신규성 미보고라 확인 불가).
- (c)(d) ALIGNN 갭 히스토그램, 0–8 eV · 칸 0.5 · 빨간 점선 3.5 eV.
  - 픽셀 적분 (우리 산수): **(c) 합 ≈2,317 · ≥3.5 ≈656** — 본문 2,356 · 672 와 맞는다 (판독법 검증).
  - **(d) 합 ≈5,960 · ≥3.5 ≈1,184** — ≥3.5 꼬리는 깔때기 1,259 와 비슷한데 **합이 13,235 의 45 %** 다. ⚠ **어긋남 ③** — (d) 는 캡션의 *"stable fluoride-containing structures from the MP-F model"* 전체가 아니다. 중복 제거본이라면 (13,235 − 7,020 = 6,215 에 가깝다) 가설로 맞지만 본문은 *"duplicates were not removed"* 라고 한다.
  - ⚠ **어긋남 ④** — 본문 *"The normalized Eg distributions … show comparable profiles"*. 결정적인 ≥3.5 꼬리 비율은 Alex **28.5 %** (672/2,356) 대 MP-F **9.5 %** (1,259/13,235) — `Fig. 3d` 자체 적분으로도 ≈19.9 % — 비슷하지 않다.
  - 우리 가설 산수: (d) 의 ≈5,960 이 유일 구조 수라면 표본당 수율 비는 28× 가 아니라 **≈13×** 다 (5,960/21,600 ÷ 2,356/108,000). 저자 스스로 *"any concentration of duplicates among stable fluorides would instead make the 28-fold ratio an upper bound"* 라고 썼다 — 그림이 그 상한 쪽 신호를 준다.

### 5.4 MatterSim vs DFT (`Fig. 4`) ★ — 절단된 parity
- 두 패널 x = DFT Ehull · y = MatterSim Ehull, 0–0.20 eV/atom, 점선 y = x.
- (a) 404 점: 대각선과 평행한 띠, 오프셋 ≈0.06 (RMSE · MAE 가 둘 다 0.06 인 것과 맞다 — 오차가 거의 상수 편향).
- (b) 801 점: 넓은 산포. **y = 0 줄** (MatterSim 이 hull 위로 본 구조가 DFT 로는 0.02–0.20) 과 **x = 0 열** (DFT 가 hull 위로 본 구조가 MatterSim 으론 0–0.09) 이 같이 있다 — *"a consistent offset"* 이라는 요약은 (a) 에는 맞고 (b) 에는 과하다.
- 🔑 **두 패널 모두 y 0.10–0.20 이 비어 있다** — 표본이 MatterSim ≤ 0.1 문턱을 통과한 것뿐이라서다. 그래서
  ① 지워진 점은 전부 y > 0.1 이고, x < 0.1 인 곳에서 지워진 점은 **전부 대각선 위** (MatterSim 이 DFT 보다 높게 본 것 = **위음성**) 였다. 절단 자체가 그림을 "MatterSim 이 낮다" 쪽으로 민다.
  ② 저자 결론 *"permissive pre-filter that minimizes false negatives"* 는 **이 표본으로 검증할 수 없다** — 위음성 (MatterSim > 0.1 인데 DFT ≤ 0.02) 은 DFT 를 한 번도 안 돌렸다.
  ③ 다른 설명도 열려 있다: DFT 쪽이 **비스핀** 이라 자성 계의 DFT 에너지가 올라가면 DFT Ehull 이 커진다 → "MatterSim 이 낮다" 처럼 보인다. 자성 / 비자성 조성으로 나눠 그리면 갈리는데 논문은 안 나눴다.
- (a) 의 x < 0.1 구간에서도 점이 대각선 아래라 **편향 일부는 진짜**일 수 있다 — 절단이 전부를 만든 건 아니다.

### 5.5 최종 5 종 · 자성 (`Fig. 5`, `Table S1`, `Table S2`, `Table S3`)
- `Fig. 5`: 5 개 구조 렌더 (원소 색: Li 초록 · Ni 회색 · F 연파랑 · Cs/K 보라 · Na 노랑, 다면체 표시) + 공간군 라벨 (*P*1 · *P*4/*mmm* · *P*-1 · *C*2 · *Pm*) — `Table S1` 과 일치.
- 래스터 해상도로는 **Ni 배위 (팔면체 vs 평면사각) 판독 불가**. 논문도 결합 길이 · 배위수를 안 준다 — 비스핀 이완에서 Ni²⁺ 가 어떤 기하로 갔는지 확인할 길이 없다 (§10-②).
- 자성은 §3f. 저자 해석: 모든 후보가 스핀편극에서 더 안정 → 자기 질서가 에너지상 의미 있다 · 선별값은 근사 · 비스핀은 Ni²⁺ 에너지를 과대평가하므로 Ehull 문턱은 **남긴 후보에게는 보수적**, 버린 후보 중엔 **위음성이 있을 수 있다** · 스핀편극 + U 재선별이 자연스러운 다음 단.
- ⚠ 저자의 "보수적" 논리는 **hull 이 같은 수준 (비스핀 PBE) 일 때만** 선다. 실제 hull 은 MP 엔트리 (Ni–F 계는 GGA+U · 스핀편극) 이고 보정 없이 섞었다 → 비스핀 벌점 (Ehull ↑) 과 GGA 대 GGA+U 기준 차 (부호 미정, Ni 당 eV 규모 가능) 가 **같이** 들어간다 (§10-①).

### 5.6 대칭 견고성 (`Table S4`, `Table S6`–`Table S9`)

| 후보 | 0.10 → 0.02 Å | 0.01 Å | 0.001 Å | 채택 → 보고 |
|---|---|---|---|---|
| NiF₂ (`Table S4`) | *C*2/*m* | *P*-1 | *P*1 | 0.01 → *P*-1 |
| LiNi₂F₅ (`Table S6`) | *Cm* | *Cm* | *P*1 | **0.001 → *P*1** |
| CsNaNi₂F₆ (`Table S7`) | *P*4/*mmm* | *Pm* | *P*1 | 0.1 → *P*4/*mmm* |
| KNi₂F₅ (`Table S8`) | *Cmmm* | *C*2 | *P*1 | 0.01 → *C*2 |
| NaNi₂F₅ (`Table S9`) | *Cmmm* (0.10–0.03) · *Pm* (0.02) | *P*1 | *P*1 | 0.02 → *Pm* |

- 저자: 5 종이 삼사 · 단사 · 정방에 걸쳐 있고 허용오차 전 범위에서 구별된다 → *"meaningful structural diversity"*.
- ⚠ 보고 저대칭 (*P*1 · *P*-1) 은 **0.01 Å 이하에서만** 나온다. 0.03 Å 로 통일하면 *Cm* · *P*4/*mmm* · *C*2/*m* · *Cmmm* · *Cmmm* — **삼사정계가 사라진다.** "이완 격자 계량을 재현" 의 판정 수치가 없어서, 대칭 선택이 생성 구조 (대칭화 없이 이완한 *P*1 출발점) 의 잔여 잡음인지 자성 · 전자 뒤틀림인지 갈리지 않는다 (§10-⑩).
- ✅ 그래도 NiF₂ 가 MP 두 다형 어느 쪽으로도 안 간다는 결론은 표 전 범위에서 성립한다.

### 5.7 띠 정렬 (`Fig. 6`)
- 막대 그림: 주황 = CBM (위 막대), 파랑 = VBM (아래 막대), 빗금 띠 = 창 (−3.33 ~ −7.33 eV), 0 eV 진공 점선. 숫자는 §3h.
- 저자: KNi₂F₅ · NaNi₂F₅ 의 띠 끝이 창을 **둘러싼다** → 전기화학 · 수송 검증 우선 대상. *"does not include thermodynamic decomposition potentials or interphase formation and therefore should not be interpreted as a complete electrochemical stability window"*.
- figure-read 로 본 것:
  - LiNi₂F₅ · CsNaNi₂F₆ 는 **CBM 이 창 안** (anode 보다 1.23 · 0.57 eV 아래 — 환원 쪽 위험), NiF₂ 는 **VBM 이 창 안** (F₂/F⁻ 보다 1.29 eV 위 — 산화 쪽 위험).
  - 기준 **PbSnF₄ 도 창을 둘러싼다** (CBM 이 anode 보다 0.07 eV 위) — 이 서술자가 '알려진 전도체' 와 후보를 가르는 힘이 얼마인지 논문은 말하지 않는다.
  - NiF₂ 의 슬랩 갭 3.57 eV 는 3.5 문턱을 0.07 eV 넘는다.
- 방법 약점 (§10-⑦): 종단을 **결과 (가장 유리한 정렬)** 로 고름 · 쌍극자 보정 없음 · 3 층 · 삼사 · 단사 셀의 (001) 은 셀 선택에 달린 면 · 비스핀 HSE06 · "anode" 는 F₂/F⁻ 에서 4 V 를 잰 가상 준위라 `Fig. 7` 의 Sn · Pb · Ce 와 연결이 없다.

### 5.8 계면 반응성 (`Fig. 7`, `Fig. S1`)
- `Fig. 7`: 5 × 6 히트맵, 색막대 **0 (파랑) — −1.0 (흰색) — −2.0 (빨강)** eV/atom. ⚠ **흰색 중심이 −1.0** 이라 −0.74 ~ −0.99 칸이 '파랗게 = 안전해' 보인다 — 절대 크기로는 전부 큰 구동력이다. 캡션의 전극 순서 (BiF₃, FeF₃, …) 와 그림 축 순서 (FeF₃, BiF₃, …) 가 다르다 (사소).
- `Fig. S1`: 같은 값의 막대 (y 0 ~ −1.75 eV/atom, 격자선 0.25). 값은 §3i.
- 본문 서술 검산 ✓: BiF₃ 가 FeF₃ 보다 0 에 가깝다 · Sn · Pb 는 중간 · Ce 는 거의 전부 강한 음수 · NiF₂ 가 BiF₃ · Sn 에 가장 음수라 나머지 넷이 '유리' · CsNaNi₂F₆ 가 **여섯 전극 전부에서** 가장 덜 음수 · 전 쌍 < ≈ −0.7.
- ⚠ 우리 판독 (§10-⑥):
  - **불활성 짝의 크기가 화학적으로 설명되지 않는다.** Ni²⁺ 불화물과 FeF₃ · BiF₃ · CuF₂ 는 양이온이 다 평소 산화수다 — 삼원 불화물이 생겨도 보통 수십 meV/atom 규모 (일반 지식 · 이 논문 값 아님) 인데 여기는 −0.74 ~ −1.20.
  - **논문 안에서도 맞지 않는다.** 의사이원 최솟값이 x → 1 (순수 후보) 쪽이면 그 값은 후보 자신의 −Ehull 이고, 후보는 Ehull ≤ 0.02 를 통과했다 → 같은 에너지 기준이라면 불활성 짝에서 −0.7 바닥이 나올 수 없다. ⇒ 두 분석의 기준 (보정 · 스핀 · 엔트리 판) 이 다르거나, 어느 한쪽에 오프셋이 있다.
  - **순위가 전극이 아니라 Ni 함량을 따른다** — 여섯 열 모두 CsNaNi₂F₆ (Ni 원자분율 0.20) < ANi₂F₅ (0.25) < NiF₂ (0.33). 금속 음극 (Ce · Pb · Sn) 에선 환원될 Ni²⁺ 가 많을수록 더 음수인 게 진짜 화학일 수 있지만, 불화물 양극 열에서도 같은 순서면 **조성 비례 오프셋**과 구별이 안 된다 ⇒ 저자가 *"the ranking, rather than the absolute magnitude, is the relevant output"* 이라 한 **순위도** 기준 확인이 먼저다.
  - 최소점의 x · 생성물을 안 줘서, 값이 진짜 계면 반응인지 한쪽 끝점의 자기 분해인지 가를 수 없다 (우리 `tools/oxidation/interface_reactivity_v2.py::is_endpoint` 가 2026-09-16 에 잡은 함정과 같은 모양 — §7).

### 5.9 탄성 (`Table S5`)
- §3g. 저자 해석: KNi₂F₅ 가장 단단 · NaNi₂F₅ V–R 폭 최대 = 탄성 이방성 강함 → 띠 정렬 · 계면으로 우선순위, 등방성으로는 아님 · CsNaNi₂F₆ 는 *"nearly isotropic elastic response (a Voigt-Reuss difference of 0.15 GPa in bulk modulus)"* · NiF₂ 는 E · G 최저라 후순위.
- ⚠ **B 의 V–R 차는 등방성 지표가 아니다** — 입방정은 이방성이 아무리 커도 B_V = B_R 이다. 지표는 G 쪽 (A^U) 이다. 계산해 보면 CsNaNi₂F₆ A^U = **0.34** 로 여전히 가장 작아 결론은 살지만 근거 지표가 틀렸다. NaNi₂F₅ A^U = **3.21** 로 이방성 최대 ✓.
- ⚠ Born 기준 (장파장 음향 안정) 만 봤다 — 포논 (광학 모드 불안정) 은 안 봤다. **Ehull ≤ 0.02 안에 든 이완 구조 18 개 중 13 개 (72 %) 가 Born 위반** — 이완 구조가 이 비율로 안장점이면 비스핀 이완이 자성 뒤틀림을 못 담고 멈췄거나 hull 단의 기준이 느슨하다는 신호일 수 있다. 논문은 이 탈락률을 논의하지 않는다.
- ⚠ 비스핀 PBE 탄성 — 고스핀 바닥 상태의 탄성은 아니다.

### 5.10 저자 스스로 그은 한계 (Discussion)
- 28 배 = 불화물 보존 단에 몰린 **정의상** 효과 · 표본 예산 · 말뭉치 · 사전학습 크기 (607,683 vs 13,414) · 중복률이 달라 **두 모형의 보편 순위가 아니다**.
- 선별값은 비스핀 + MP hull 보정 없음 → **근사**. 완전 스핀편극 + U 재선별이 다음 단.
- 5 종 = **검증된 전해질이 아니라 우선순위 계산 후보**. 결함 형성 · 이동 장벽 · MD · 임피던스가 남았다.
- 전부 Ni = 말뭉치 탓 (저자 해석) · Ni 공급 제약 → 원소 풍부도 · 위험도를 깔때기에 넣는 게 자연스러운 확장 · LiNi₂F₅ 는 Li 함유라 자원 다변화 관점에서 불리 · Ce 금속은 이 Ni 불화물 계열과 맞지 않는다.
- *"principal advance"* = 화합물 몇 개가 아니라, 원소 조합 · 화학량 · 원형을 안 정해도 그럴듯한 후보가 나온다는 시연.

---

## 6. Post-processing ★ + 논증 흐름

### 6a. 후처리
- **무엇**: Ehull (convex hull) · StructureMatcher 중복 · 신규 · ALIGNN Eg · 형식 산화수 열거 · VRH 평균 + Born · spglib symprec 훑기 · 평면 평균 정전 퍼텐셜 진공 정렬 · pymatgen 의사이원 계면 반응 · NM/FM/AFM 에너지 비교.
- **도구**: MatterGen (+ 평가 파이프라인) · MatterSim · ALIGNN · pymatgen (StructureMatcher · PhaseDiagram · spglib) · VASP. 구조 그림 (`Fig. 5`) 도구 미명시 (VESTA 풍).
- **기록 · 플롯**: 스크립트 · 설정 · 최종 구조 · 그림 원자료를 GitHub 공개 (`Jeong-Research-Group/FIB`). 히스토그램 · parity · 주기율표 히트맵 · 막대 / 히트맵.

### 6b. 저자의 논증 사슬 — 그리고 약한 고리

| # | 주장 | 근거 | 약한 고리 |
|---|---|---|---|
| ① | 고체 F⁻ 전도체 희소 + DB 좁음 | 서론 문헌 | — |
| ② | 조성 · 원형 미지정 + Ehull 조건 생성 | MatterGen | "데이터 희소" 는 **기능 (전도)** 쪽인데 조건은 **안정도**뿐 → 실제로 훑는 곳은 데이터 많은 '안정 불화물' 공간 (§10-⑧) |
| ③ | 학습 분포가 생성 분포를 지배 | `Fig. 2` | (a) 는 F 부분집합이 아니다 (§5.2) |
| ④ | 도메인 정렬 = 28 배 | 수 세기 | 정의상 · 중복 · `Fig. 3d` 적분 (§5.3) |
| ⑤ | MatterSim = 관대한 사전선별 | `Fig. 4` | 절단 표본 (§5.4) |
| ⑥ | Ni 5 종이 열 · 전자 · 기계 기준 통과 | DFT 깔때기 | 비스핀 · U 없음 · MP 혼합 (§10-①②) |
| ⑦ | KNi₂F₅ · NaNi₂F₅ 우선 | `Fig. 6` · `Fig. 7` · `Table S5` | 종단 선택 · 기준 오프셋 · 수송 0 (§10-⑥⑦⑧) |
| ⑧ | 무제약 생성이 미개척 영역을 연다 | ①–⑦ | 결과가 **전부 Ni** — '무제약' 출력을 프로토콜이 한 원소로 모았을 가능성 (§10-③) |

---

## 7. 우리 DFT 대비 ★★ (`../our_dft_baseline.md` · `db/properties/`)

### 7a. 값은 나란히 놓지 않는다 — 이유 먼저
- 계가 다르다: **Ni 불화물 (F⁻ 운반 후보 · 정렬 소셀 8–10 원자)** vs **Li argyrodite (Li⁺ · 무질서 배열 · 52 원자 이상)**.
- 범함수 · 스핀 · 정의가 다르다: 그들 갭 = **슬랩 · 비스핀 HSE06 · 종단 선택** · 우리 갭 = **PBE fixed-occ nscf 고유값** (comp1 **2.066** · modelc **2.099 eV**, canonical `gap-fixedocc-eigenvalue-v1`).
- ⇒ 물성 4축 (A 이온 · B 산화 · C 기계 · D 전자) 표에 **넣을 행이 없다.** 대조는 **방법 축**만.

### 7b. 방법 축 대조

| 항목 | 이 논문 | 우리 | 같은가 · 왜 |
|---|---|---|---|
| 후보 생성 | MatterGen 확산 생성 (조성 · 원형 미지정) | 자리 열거 (`enumerate_track1.py` 342 배열 · `kb/methodology/dopant_screening_funnel_2026_06_13.md`) · cascade 설계 순위 | **다름** — 그들은 조성 공간을, 우리는 정해진 호스트의 배열 공간을 훑는다 |
| MLIP 사전선별 | MatterSim Ehull ≤ 0.1 | UMA-s-1p1 (omat) 일괄 완화 → 순위 → 상위만 DFT+U (깔때기 4 단 top-5 계획) | **같은 꼴** — 둘 다 MLIP 문턱 뒤만 DFT 로 본다 |
| MLIP 검증 | 통과자 parity (RMSE 0.06–0.07 eV/atom) | 외부 데이터 힘 벤치 (`db/properties/mlip_bench_li3ps4_uma.json` — 힘 MAE 30.0 meV/Å) · Li₃N 사용 금지 판정 (`HZ-uma-li3n-banned`, BLOCKED) | **둘 다 위음성률을 직접 안 잰다** — 그들은 절단 parity, 우리는 문턱 아래 감사 표본이 없다 |
| 에너지 기준 (hull) | 자기 VASP 에너지 (비스핀 · U 없음) 를 MP hull 에 **보정 없이** | `tools/doping/convex_hull_ehull.py` — `--mode uma` 는 우리 구조 + MP 경쟁상을 **전부 UMA 로 다시 계산**해 자기일관 · `--mode mp` 는 생성물만 (절대 Ehull 안 줌) · `tools/doping/dft_decomp_check.py` — 공통 분해상 기저를 같은 QE 설정으로 · thermo type `GGA_GGA+U` 명시 (2026-10-23) | **다름 — 우리 규칙이 이 논문의 함정을 막는 쪽.** 근거 문구: *"MP 엔트리는 VASP PAW PBE(+보정)이고 우리는 QE USPP 다. 섞으면 hull 이 틀린다."* (`dft_decomp_check.py` docstring) · *"OMat/UMA total energies are not directly compatible with Materials Project total energies or MP2020 corrections."* (`tools/fairchem_kb/curated_knowledge.json`) |
| 스핀 · U | 선별 단계 비스핀 · U 없음 (Ni²⁺ 고스핀인데) → 최종 5 종만 PBE+U 자성 비교 (서술자에 미반영) | Nd 4f: DFT+U · ISPIN=2 (깔때기 4 단) | **다름 — 우리 쪽이 맞다** |
| 이완 정책 | 격자 + 원자 전체 이완 (정렬 소셀) | argyrodite = **고정셀 + EOS (BM3) → V₀ 에서 이온만** (CLAUDE.md 2026-10-15) | 다름 — 정렬 소셀이면 전체 이완이 보통이라 그들 선택이 틀린 건 아니다 |
| 띠 틈 | 슬랩 비스핀 HSE06 · 종단을 결과로 선택 · 쌍극자 보정 없음 | 벌크 PBE fixed-occ nscf 고유값 (DOS 문턱 판독 금지) | 다름 — 값 비교 금지 · 'wide-gap' 수준만 |
| 산화 안정 | 띠 정렬 서술자 (저자: ESW 아님) · grand-potential 창 **없음** | B① grand-potential onset **2.256 V** (S²⁻-limited, comp1 · modelc 동일) | **축 분리 규율은 같은 방향** — 그들도 '띠 정렬 ≠ 열역학 창' 을 명시. 단 그들에겐 ①축 값 자체가 없다 |
| 계면 반응 | pymatgen 의사이원 · 후보 자기 에너지 · MP 혼합 · 최소점 x · 산물 미보고 | `tools/oxidation/interface_reactivity_v2.py` — `InterfacialReactivity(use_hull_energy=True)` (닫힌계: 반응물을 hull 에너지로 → 자기 오프셋이 반응에너지로 안 샌다) · 끝점 최소 깃발 `is_endpoint` · 기록 `db/properties/interface_reactivity_results.json` 은 **모든 kink 의 x · 에너지 · 반응식**을 남긴다 (예: comp1‖LiCoO₂ 최소 @ x = 0.5302) | **다름** — 우리가 늘 남기는 x · 산물 · 끝점 판정을 그들은 안 준다. ⚠ 단 `use_hull_energy=True` 는 두 반응물이 **다 MP 엔트리**일 때 깔끔하다 — MP 에 없는 새 후보라면 같은 기준 (스핀편극 GGA+U + MP2020 보정) 으로 계산한 엔트리를 상도에 넣어야 한다 |
| 탄성 | VRH Hill · Born 만 · 계산법 미명시 · 비스핀 | relaxed-ion C_ij → E_VRH (comp1 **22.06** · modelc **27.66 GPa**) · B₀ BM3 (**26.23** · **21.71 GPa**) · 조성 간 비교는 `HZ-elastic-cross-composition` (CONDITIONAL) | 값은 다른 계라 나란히 안 놓는다 · 방법은 VRH 로 같다 |
| 수송 단 | **없음** | 호스트 계 (comp1 · modelc · lpsocl) MLIP-MD (UMA) — 절대값 인용 금지 · 상대차만. ⚠ cascade (도핑 스크리닝) 의 D_rel 파일럿은 **2026-10-01 닫힘** — *"사전 정의한 보고량 D_rel(P1/P2) 은 이 프로토콜에서 정의되지 않았고, 보고하지 않는다"* (`db/properties/cascade_d_rel_closed_2026_10_01.json`) | ⚠ **'수송 단 없는 스크리닝 깔때기' 는 지금 우리 cascade 에도 해당한다** — 남의 흠으로만 쓰지 않는다 |
| 무질서 | 정렬 소셀 하나 | 무질서 배열 앙상블 | 다름 |
| 깔때기 회계 | 두 팔 단별 생존 전부 공개 | `kb/reviews/litdb_dopant_sota_2026_09_09.md` §3.2 (91 → 45 → 36 → 13) | **같은 형식** — 문헌에서 드문 형식 (§J-10-b #1: 13 캠페인 중 2 건) 을 이 논문은 갖췄다 |

### 7c. 진짜 차이 vs 방법 인공물
- 값 비교가 없으니 '물성 차이' 는 없다. 대신 **이 논문의 결론 중 방법 인공물일 수 있는 것**을 우리 규율로 표시한다:
  - *"MatterSim 은 계통적으로 낮다 → 관대한 사전선별"* → **절단 표본 + DFT 쪽 비스핀** 이 섞여 있다 (방법 의존).
  - *"5 종 모두 Ni = 말뭉치 탓"* → **비스핀 HSE06 갭 문턱 · GGA 대 GGA+U 기준 혼합** 이 Ni 를 고를 수 있다 (방법 의존 · 가설).
  - *"모든 전극과 계면상 형성 (< −0.7 eV/atom)"* · 그 순위 → **에너지 기준 일관성** 미확인 (방법 의존).
  - *"KNi₂F₅ · NaNi₂F₅ 가 창을 둘러싼다"* → **종단 선택 · 쌍극자 보정 없음 · 비스핀** (방법 의존).
- 방법과 무관하게 서는 것: 깔때기 각 단의 **생존수** (정의대로 센 값) · NiF₂ 다형이 MP 두 상과 다르다는 대칭 판정 · 28× 라는 산수 자체 (해석은 정의상).

---

## 8. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | 생성 → 고처리량 선별 깔때기. 두 팔 (Alex-MP-20 / MP-F) 단별 생존 108,000/21,600 → 76,344/13,235 → (F 함유 2,356) → 672/1,259 → 670/1,227 → 438/877 → 404/801 → DFT 4 단 14/57 · 8/28 · 5/13 · 1/4 | 단별 회계 보고 형식의 본보기. ⚠ "SUN screening" 라벨은 실제로 S 만 · O/H 조성 필터가 DFT 뒤에 있다 |
| 2a,b | 안정 생성 구조의 원소 출현 히트맵 (a 0–7,000 · b 0–4,000). (b) 는 Li · O · V · F · Mn 에 몰림 | ⚠ (a) 는 캡션과 달리 F 부분집합이 아님 (F ≈2,682 < Li ≈6,206) · (b) F ≈11,77x < 13,235 · (b) 에서 Ni ≈321 ≪ V ≈2,246 → 최종 100 % Ni 는 하류 농축 (figure-read) |
| 3a,b | MatterSim Ehull 히스토그램 (0–0.5, 칸 0.025, 문턱 0.1) — Stable 76,344 / 13,235 | MP-F 안정의 ≈54 % 가 첫 칸 (Alex ≈33 %) — 재생성 의심 신호 (figure-read) |
| 3c,d | ALIGNN 갭 히스토그램 (0–8 eV, 칸 0.5, 문턱 3.5) | (c) 적분 ≈2,317 ✓ · (d) 적분 ≈5,960 ≠ 13,235 · ≥3.5 꼬리 비율 28.5 % 대 9.5 % — "비슷한 분포" 가 아니다 (우리 픽셀 적분) |
| 4a,b | MatterSim vs DFT Ehull parity, RMSE · MAE 0.06 (a) · 0.07 (b) | ★ **통과자만 그린 parity 는 위음성을 못 잰다** — y 0.10 위가 비어 있다. 우리 UMA 문턱에도 문턱 아래 감사 표본이 필요 |
| 5 | 최종 5 종 구조 (*P*1 · *P*4/*mmm* · *P*-1 · *C*2 · *Pm*) | 해상도로 Ni 배위 판독 불가 — 비스핀 이완 기하 확인 불가 |
| 6 | 슬랩 HSE06 띠 끝 (진공 기준) vs F₂/F⁻ −7.33 · 가상 anode −3.33 eV · PbSnF₄ 기준 | KNi₂F₅ · NaNi₂F₅ 만 창을 둘러쌈 — 단 PbSnF₄ 도 둘러쌈 · 종단을 결과로 고름 · 쌍극자 보정 없음 → 서술자 설계의 반면교사 |
| 7 | 5 × 6 계면 반응에너지 히트맵 (흰색 중심 −1.0 eV/atom) | 색 중심이 −1.0 이라 '파랑 = 안전' 착시 · 순위가 Ni 함량 순 · 우리는 x · 산물 · 끝점 판정을 같이 보고한다 |
| S1 | `Fig. 7` 값의 막대 (y 0 ~ −1.75 eV/atom) | 픽셀 판독 표 (§3i) · 불활성 불화물 짝도 −0.74 ~ −1.20 — 에너지 기준 확인 필요 |
| Table S1 | 5 종 격자 · 공간군 · 부피 (비스핀 PBE 이완) | 구조 ID 용 |
| Table S2 | FM / AFM Ni 평균 자기모멘트 1.82–1.92 μB | 고스핀 Ni²⁺ — 비스핀 선별의 전제가 무너지는 지점 |
| Table S3 | NM / FM / AFM 총에너지 (PBE+U) | 우리 산수: NM 이 0.28–0.73 eV/atom 높다 = Ehull 문턱의 14–36 배 · LiNi₂F₅ 이상치 |
| Table S4 | NiF₂ symprec 0.10–0.001 Å → *C*2/*m* · *P*-1 · *P*1 | MP 두 다형과 다름 — 허용오차 훑기 표는 우리 구조 보고에도 쓸 만한 형식 |
| Table S5 | 탄성 V / R / H (B · E · G) | E_H = 9BG/(3B+G) 재현 · A^U 로 보면 CsNaNi₂F₆ 0.34 · NaNi₂F₅ 3.21 (우리 산수) |
| Table S6 | LiNi₂F₅ symprec 훑기 (0.01 까지 *Cm*) | *P*1 보고는 0.001 Å 에서만 |
| Table S7 | CsNaNi₂F₆ symprec 훑기 (0.02 까지 *P*4/*mmm*) | — |
| Table S8 | KNi₂F₅ symprec 훑기 (0.02 까지 *Cmmm*) | *C*2 는 0.01 Å 에서만 |
| Table S9 | NaNi₂F₅ symprec 훑기 (0.03 까지 *Cmmm*) | *Pm* 은 0.02 Å 에서만 |

---

## 9. 적용 인사이트 ★ + 인용 가능 문장

### 9a. 우리 1단계 깔때기에 주는 것
1. **문턱 아래 감사 표본** — MLIP 문턱에서 떨어진 것 중 무작위 n 개를 DFT 로 돌려 위음성률을 직접 잰다. 통과자 parity 로는 원리적으로 못 잰다 (`Fig. 4` 의 빈 y 0.10–0.20). 우리 UMA 일괄 완화 순위 (342 → 1) 에도 그대로 걸린다 — 상위 몇 개만 DFT 로 보면 (깔때기 4 단은 top-5 계획) "UMA 가 떨어뜨린 것 중에 진짜가 있었나" 는 답이 안 나온다.
2. **에너지 기준 한 줄 선언** — hull · 반응에너지 행마다 *후보 에너지 출처 · 경쟁상 출처 · 스핀 · U · 보정* 을 적는다. 우리 도구는 이미 혼합을 막게 짜여 있다 (`convex_hull_ehull.py` · `dft_decomp_check.py`) — 남은 일은 **보고 칸**을 박는 것.
3. **싼 필터 먼저** — 이 논문은 조성 규칙 (O/H 제외) 을 DFT 뒤에 둬서 DFT 생존자의 43–51 % 를 조성 규칙으로 버렸다. §J-10 의 '싼 것 먼저' 원칙이 깨지면 어떻게 되는지의 실측 사례.
4. **"왜 전부 X 인가" 를 단별로 추적** — 생성 분포 (`Fig. 2b`: Ni 소수) 와 최종 (Ni 100 %) 사이 어느 단에서 농축됐는지, 단마다 원소 분포를 남기면 프로토콜 인공물인지 바로 갈린다. 우리 cascade 순위에서도 '도펀트 원소 × 단' 표를 남길 이유.
5. **생성형을 로드맵에 올린다면** — 조건이 안정도뿐이면 '데이터 희소한 기능' (이온전도) 을 겨누지 못한다. 수송 서술자를 조건이나 단으로 넣어야 하고, 그 단의 **보고량 카드를 먼저** 쓴다 (`kb/templates/estimand_card.md`). 우리 cascade 수송 단 (D_rel) 이 닫힌 이유 (보고량 미정의) 가 바로 그 카드 단계다.
6. **띠 정렬 서술자를 쓸 때** — 종단은 표면에너지로 고르거나 전 종단의 범위를 보고 · 쌍극자 보정 (c 를 표면 법선으로 셀 재설정) · 층수 수렴 · 알려진 기준 (여기선 PbSnF₄) 이 그 서술자를 통과하는지부터 본다.

### 9b. 인용 가능 문장 (영문 · preprint 임을 명시)
- *"Conditioning a diffusion generative model on thermodynamic stability alone and training it on a fluoride-only corpus raised the per-sample yield of stable fluoride candidates by roughly 28-fold, an advantage the authors describe as largely definitional (Research Square preprint, 2026, DOI 10.21203/rs.3.rs-11026639/v1)."*
- *"The same study reported the stage-wise retention of both model arms in full (108,000 to 1 and 21,600 to 4 structures), which remains uncommon among screening studies."*
- (우리 서술 — 논문 주장 아님) *"A parity plot restricted to candidates that passed a machine-learned stability gate cannot establish a low false-negative rate, because candidates rejected by the gate are never evaluated with DFT."*
- 랩 표기 (발표): *Research Square*, rs.3.rs-11026639/v1 (2026) — 저널 미게재 preprint.

---

## 10. 비판 — 이 논문의 약한 곳 ★

> 등급: 🔴 결론을 흔듦 · 🟠 서술 · 그림 신뢰를 깎음 · 🟡 보완 필요.

1. 🔴 **에너지 기준 혼합 (Ehull).** 후보는 VASP PBE · **비스핀 · U 없음 · 보정 없음**, hull 은 **MP 엔트리** 그대로. MP 규약에서 +U 는 O · F 를 포함한 계의 Co · Cr · Fe · Mn · Mo · Ni · V · W 에 걸린다 (논문 밖 지식 · pymatgen MP 입력셋 기본값 — 논문도 U_eff 6.2 를 "MP 관례" 라 부른다) → **Ni–F 경쟁상은 GGA+U · 스핀편극, 후보는 GGA · 비스핀**. 두 오차가 섞인다: 비스핀 벌점 (후보 에너지 ↑ → Ehull ↑) 과 GGA 대 GGA+U 기준 차 (부호 미정, Ni 당 eV 규모 가능). 저자의 "보수적" 논리는 앞의 것만 본다. 규모 감: 같은 후보에서 스핀 처리 하나로 **0.28–0.73 eV/atom** (`Table S3`, PBE+U) — 문턱 0.02 의 **14–36 배**. VASP · PAW · PBE · 520 eV 는 MP 와 같은 계열이라 '코드 혼합' 은 아니고, 남는 건 **+U · 스핀 · 보정** 세 겹이다.
2. 🔴 **고스핀 Ni²⁺ 에 비스핀 서술자.** `Table S2` 모멘트 1.82–1.92 μB = S = 1. 팔면체 d⁸ 은 e_g 두 오비탈에 전자 둘 — 비스핀에서는 e_g 를 둘로 쪼개 한쪽만 채우는 **저스핀 꼴**로만 갭이 열린다 (뒤틀림, 또는 혼성 범함수의 오비탈 편극). 그러면 HSE06 갭 · 띠 끝 · 탄성 · 반응에너지가 **바닥 상태가 아닌 전자 상태**의 값이 된다 (우리 해석 · 결정장 전자 세기). 구조도 비스핀으로 이완됐다 (`Table S1`). 배위 · 결합 길이 미보고라 확인할 길이 없다.
3. 🔴 **"전부 Ni" 가 프로토콜 인공물일 가능성 — 논문이 배제하지 않는다.** (i) 생성 분포에서 Ni 는 소수 (`Fig. 2b`: Ni ≈321 vs V ≈2,246 · Mn ≈1,639, figure-read) (ii) HSE06 단에서 **36 → 18 (절반)** 탈락 — ALIGNN ≥ 3.5 를 이미 통과한 구조들인데, ALIGNN 이 PBE 급 갭을 예측한다면 HSE06 갭은 더 커야 하므로 절반 탈락은 이상하다. 비스핀 HSE06 은 d 껍질이 반쯤 찬 Mn²⁺ · Fe³⁺ (d⁵) · Co²⁺ (d⁷) · Cr³⁺ (d³) · Cu²⁺ (d⁹) 류를 금속 (또는 작은 갭) 으로 만들고, d⁰ · d¹⁰ · 저스핀 d⁶ · d⁸ (Ni²⁺) 만 통과시키는 **d 전자수 필터**처럼 굴 수 있다 (가설). d⁸ 이 특별한 이유: 비어야 할 쪽이 **리간드를 정면으로 향하는 e_g (σ*)** 라 평면사각 꼴 뒤틀림 하나로 크게 갈린다 — 저스핀 평면사각 d⁸ (Ni²⁺ · Pd²⁺ · Pt²⁺ 착물) 이 흔한 이유와 같다. t₂g 안에서만 갈려야 하는 d² (V³⁺) 등은 갈림 폭이 작아 3.5 eV 급 갭이 나오기 어렵다 (iii) ① 의 U 원소 기준 혼합도 전이금속 계에만 걸린다. 검증법: HSE06 단 36 후보의 원소 · d 전자수 목록 공개 + 스핀편극 GGA+U · MP2020 보정으로 ⑦–⑩ 단 재실행. ALIGNN 판 · 학습 대상 (어느 범함수의 갭) 미명시라 (ii) 의 강도도 확정 못 한다.
4. 🔴 **절단 parity (`Fig. 4`).** 표본 = MatterSim ≤ 0.1 통과자 → 위음성은 DFT 를 한 번도 안 돌렸다 → *"minimizes false negatives"* 는 검증 불가. 절단은 x < 0.1 에서 대각선 위 점만 지우므로 '계통적으로 낮다' 쪽으로 그림을 민다. 대안 설명 (DFT 쪽 비스핀) 도 열려 있다. (b) 는 *"consistent offset"* 이 아니라 넓은 산포 (y = 0 줄 · x = 0 열).
5. 🟠 **그림–본문 불일치 다섯.** ① `Fig. 2a` 는 F 부분집합이 아님 (어느 셈법으로도) ② `Fig. 2b` F ≈11,77x < 13,235 ③ `Fig. 3d` 적분 ≈5,960 ≠ 13,235 (≥3.5 꼬리는 1,259 와 맞음) ④ *"comparable Eg profiles"* ↔ 꼬리 28.5 % 대 9.5 % ⑤ `Fig. 1` "SUN screening" ↔ Methods U · N 미적용. 어느 것도 28× 산수 자체를 깨지는 않지만, **그림이 어떤 모집단을 그렸는지** 독자가 알 수 없다.
6. 🟠 **계면 반응에너지 (`Fig. 7`, `Fig. S1`).** 불활성 불화물 짝 (FeF₃ · BiF₃ · CuF₂) 도 −0.74 ~ −1.20 eV/atom — 화학적으로 설명되지 않는 크기 · 후보 Ehull ≤ 0.02 와 같은 기준에서 동시에 성립하기 어렵다 · 여섯 열 모두 순위가 Ni 원자분율 순 (0.20 < 0.25 < 0.33) → **순위까지** 오프셋에 오염됐을 수 있다 · 최소점 x · 산물 미보고. 흰색 중심 −1.0 색막대는 '파랑 = 안전' 착시를 만든다.
7. 🟠 **띠 정렬 (`Fig. 6`).** 종단을 **결과로** 고름 (가장 유리한 정렬 = 낙관 상한) · 쌍극자 보정 없음 (비대칭 · 극성 슬랩이면 진공 준위가 기울어 기준이 흔들린다 — c 를 표면 법선으로 셀을 다시 잡으면 되는 문제를 "호환 안 됨" 으로 넘겼다) · 3 층 (두께 수렴 없음) · 삼사 · 단사 셀의 (001) 은 셀 선택에 달린 면 · 비스핀 HSE06 · "anode" = F₂/F⁻ + 4 V 의 가상 준위 · 기준 PbSnF₄ 도 통과.
8. 🟠 **수송 단 0 · "데이터 희소" 의 과녁.** 제목은 전해질 후보지만 이동 장벽 · MD · BVSE · 결함이 없다 (저자 인정). 또 데이터가 희소한 것은 **빠른 F⁻ 전도체 (기능 라벨)** 인데 생성 조건은 **Ehull** 뿐이라, 실제로 훑은 곳은 학습 데이터만 13,414 개인 '안정 불화물' 공간이다.
9. 🟡 **탄성.** Born 만 (포논 없음) · Ehull ≤ 0.02 이완 구조의 **72 % 가 Born 위반** — 논의 없음 · B 의 V–R 차를 등방성 지표로 씀 (입방정은 이방성과 무관하게 0 — A^U 로 바꿔도 CsNaNi₂F₆ 최소라 결론은 산다) · 계산법 (변형 집합 · relaxed-ion) 미명시 · 비스핀.
10. 🟡 **대칭.** 보고 저대칭은 ≤0.01 Å 에서만 · "격자 계량 재현" 판정 수치 없음 · 0.03 Å 로 통일하면 삼사정계가 사라진다.
11. 🟡 **신규성 미보고 · 재생성 의심.** SUN 중 N · U 비율을 안 준다 · MP-F 중복 32.5 % · MP-F 안정의 ≈54 % 가 Ehull 첫 칸 (figure-read) — 학습 구조 재생성과 양립한다. 최종 4 종 (A–Ni–F) 이 ICSD 에 있는지도 안 따졌다 (NiF₂ 다형만 MP 와 대조).
12. 🟡 **깔때기 순서 · 통계.** O/H 조성 필터가 DFT 뒤 (DFT 생존자 43–51 % 를 버림 — DFT 전 집합에서도 비슷한 비율이었다면 DFT 예산 절반 가까이가 조성 규칙으로 버릴 구조에 쓰였다, 우리 추정) · 최종 1 대 4 의 생존율 비교 (0.042 % vs 0.030 %) 는 n = 1 · 4 — 포아송으로 ±100 % · ±50 %.
13. 🟡 **LiNi₂F₅ NM 벌점 이상치** — Ni 당 2.91 eV vs K · Na 동형 1.19 · 1.14 eV (`Table S3`, 우리 산수). 다른 해 (비수렴 · 다른 기하) 가능성 · 설명 없음.
14. 🟡 **미심사 preprint v1** · 공동 1저자 둘이 계산 · 소프트웨어 · 검증 · 그림 · 초고를 다 맡았다 (Author Contributions) — 내부 교차검증 층이 얇다.

**✅ 공정하게 — 잘한 것**: 두 팔 단별 생존 전량 공개 · 중복 분석과 설정 공개 · 28× 의 정의상 성격과 중복 상한을 스스로 명시 · 띠 정렬 ≠ 안정창 · 0 K 반응에너지는 순위만 · "검증된 전해질 아님" · 대칭 허용오차 전 범위 표 · 코드 · 구조 공개.

---

## 11. 주의 / 한계 (인용 규율)
- ✅ 써도 되는 것: 깔때기 **형식**과 단별 생존수 (출처: preprint) · 28× **+ 단서** (정의상 · 중복 상한 · 표본 예산 5 배 차) · *"MLIP 사전선별 + DFT 검증 + 수송 단 없음"* 이라는 구조 서술 · NiF₂ 다형의 대칭 판정.
- ⛔ 쓰지 말 것:
  - 5 종의 갭 · 탄성 · 띠 끝 · 반응에너지를 **물성값으로** 인용 (비스핀 · U 없음 · 기준 혼합) — 특히 우리 값과 **같은 표 금지**.
  - *"KNi₂F₅ · NaNi₂F₅ 는 F⁻ 고체전해질"* — 수송 0.
  - *"MatterSim 은 불화물에서 관대하다 (위음성 적음)"* — 절단 표본.
  - *"모든 전극과 계면상이 생긴다 (< −0.7 eV/atom)"* 를 화학적 사실로 — 기준 일관성 미확인.
- figure-read 값 (`Fig. 2` 칸 숫자 · `Fig. 3` 적분 · `Fig. S1` 막대) 은 판독값으로만, 본문 명시값과 섞지 않는다.
- preprint 판이 바뀌면 (v2 · 저널 게재) 수치를 다시 대조한다.

---

## 12. 우리 기록 매핑

| 이 논문 요소 | 우리 쪽 기록 | 관계 |
|---|---|---|
| 깔때기 단별 생존 | `kb/reviews/litdb_dopant_sota_2026_09_09.md` §3.2 · `comparison_vs_ours.md` §J-10 | 같은 회계 형식 — 외부 1차 사례 1 건 추가 |
| 깔때기 판정 계약 | `comparison_vs_ours.md` §J-12 (`[Basu26MFB]` — 아무도 안 떨어뜨리는 깔때기) | 대조: 이 논문은 **매 단이 실제로 자른다** |
| MLIP 사전선별 | `kb/methodology/dopant_screening_funnel_2026_06_13.md` (342 → UMA → 1) · `db/properties/mlip_bench_li3ps4_uma.json` | 통과자만 DFT — 위음성 미측정 위험을 같이 진다 |
| MLIP 계 의존 편향 | `db/properties/citation_hazards.json` `HZ-uma-li3n-banned` (BLOCKED) | MLIP 편향의 부호 · 크기는 계마다 따로 잰다 |
| 에너지 기준 | `tools/doping/convex_hull_ehull.py` · `tools/doping/dft_decomp_check.py` · `tools/fairchem_kb/curated_knowledge.json` | 우리는 혼합 금지 규칙 보유 — 이 논문이 반례 |
| 계면 반응 | `tools/oxidation/interface_reactivity_v2.py` (`use_hull_energy=True` · `is_endpoint`) · `db/properties/interface_reactivity_results.json` | 우리는 x · 산물 · 끝점 판정 보고 |
| 띠 틈 | `db/properties/canonical_registry.json` (`gap-fixedocc-eigenvalue-v1`: 2.066 · 2.099 eV) | 값 비교 금지 |
| 탄성 | `canonical_registry.json` (`elastic-dft-relaxedion-*` · `b0-dft-bm3-v1`) · `HZ-elastic-cross-composition` | 값 비교 금지 |
| 수송 단 | `db/properties/cascade_d_rel_closed_2026_10_01.json` | 우리 cascade 도 지금 수송 결과 없음 |
| 생성형 역설계 | `kb/projects/digital_twin_roadmap.md` (Inverse design 미착수) · `kb/fairchem/05_papers_and_insight_workflow.md` | 착수 시 §9a-5 · §10 을 체크리스트로 |
| MatterGen 2차 인용 | `papers/jain2026_ml_pipelines_solid_state_electrolyte_design.md` | 이 편으로 1차 사례 확보 |

---

## 13. 기법 용어 미니사전
- **FIB (fluoride-ion battery)**: F⁻ 가 양 · 음극 사이를 오가는 전지. 금속 불화물 ↔ 금속 전환 반응.
- **tysonite · fluorite**: F⁻ 전도체의 두 대표 원형 — LaF₃ 형 (삼방/육방) · CaF₂ 형 (입방). PbSnF₄ 는 fluorite 계 층상 유도체.
- **MatterGen**: 원자 종류 · 좌표 · 격자를 함께 잡음에서 되살리는 **확산 생성모형**. 조건 (여기선 Ehull) 을 걸어 원하는 성질 쪽으로 샘플을 민다.
- **guidance factor**: 조건을 얼마나 세게 따를지의 배율 (classifier-free guidance). 크면 조건에 충실 · 다양성은 준다.
- **SUN (Stable · Unique · Novel)**: MatterGen 평가 지표 — hull 근처 · 생성 집합 안에서 유일 · 기준 DB 에 없음.
- **StructureMatcher (`ltol` · `stol` · `angle_tol`)**: pymatgen 의 결정 동일성 판정 — 격자 길이 · 원자 위치 · 각도 허용오차.
- **Ehull (energy above hull)**: 같은 조성에서 가장 안정한 상 조합 (convex hull) 보다 원자당 얼마나 높은가. 0 = hull 위.
- **MP 호환 보정 (GGA/GGA+U 혼합 · MP2020)**: GGA 와 GGA+U 총에너지는 기준이 달라 그대로 못 뺀다. MP 는 원소 · 음이온별 에너지 보정으로 둘을 한 hull 에 놓는다. 보정 없이 섞으면 Ehull 이 틀린다.
- **Dudarev U_eff**: d (또는 f) 전자 국재화를 보정하는 DFT+U 의 단일 파라미터 (U − J). Ni 6.2 eV 는 MP 값.
- **NM · FM · AFM**: 비스핀 (자성 없음) · 강자성 · 반강자성 배열.
- **고스핀 Ni²⁺ (d⁸, S = 1)**: 팔면체 Ni²⁺ 는 e_g 두 오비탈에 홀전자 둘 — 모멘트 ≈2 μB (공유결합으로 조금 줄어 1.8–1.9).
- **MatterSim**: 대규모 제1원리 데이터로 학습한 범용 MLIP (MLFF) — `wu2026_ml_driven_electrolyte_interface_design_review` Table 3 기준 MP + Alexandria + 자체 생성 ~17 M. 여기선 Ehull 사전선별에만 썼다.
- **ALIGNN**: 결합각까지 그래프에 넣은 GNN 물성 예측기. 여기선 구조 → 갭.
- **HSE06**: 단거리 정확 교환을 섞은 혼성 범함수 — PBE 의 갭 과소평가를 줄인다.
- **Voigt · Reuss · Hill**: 단결정 C_ij 에서 다결정 탄성률의 상한 (균일 변형) · 하한 (균일 응력) · 그 평균.
- **Born 기준**: C_ij 가 양의 정부호 = 장파장 변형에 안정. 포논 (모든 파장) 안정과는 다르다.
- **A^U (보편 이방성 지수)**: 5G_V/G_R + B_V/B_R − 6. 0 이면 등방. B 의 V–R 차만으로는 등방성을 못 잰다.
- **Pugh 비 (B/G) · ν (푸아송 비)**: 연성 · 취성의 경험 지표 (B/G > 1.75 · ν > 0.26 이면 '연성 쪽').
- **symprec (spglib)**: 대칭 판정 위치 허용오차 (Å). 크면 높은 대칭, 작으면 낮은 대칭이 나온다.
- **슬랩 진공 정렬 · 평면 평균 퍼텐셜**: 표면 모형에서 정전 퍼텐셜을 면 평균해 진공 평탄부를 0 으로 잡고 띠 끝을 절대 눈금에 놓는 법.
- **쌍극자 보정**: 위아래 표면이 다른 슬랩의 인공 전기장을 상쇄하는 보정. 없으면 진공 평탄부가 기울어 기준이 흔들린다.
- **절대 전극 전위 (Trasatti)**: 표준전위 (vs SHE) 를 진공 기준 에너지로 옮기는 환산. 여기서 F₂/F⁻ → −7.33 eV.
- **의사이원 계면 반응성**: 두 상을 x : (1−x) 로 섞은 가상 조성의 hull 에너지와 반응물 에너지 차의 최솟값. 0 K · 열역학 구동력만 (속도 · 부동태 없음).
- **절단 (truncation) · 선택 편향**: 문턱을 통과한 표본만 보면 문턱이 지운 영역의 정보가 원리적으로 없다 — parity 의 편향 · 위음성률을 그 표본으로는 못 잰다.
