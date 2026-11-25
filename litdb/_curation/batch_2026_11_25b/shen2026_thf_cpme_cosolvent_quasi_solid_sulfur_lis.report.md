# 끝 보고 — shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis (2026-11-25 · litdb-curator · 배치 2026-11-25b #1 · 이어 하기)

쓴 파일은 셋이에요 (앞 세션이 컨테이너 재시작으로 멈춘 자리에서 이어 썼어요).
- digest `litdb/papers/shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis.md` (492 줄 · 표 11 개 · 칸 수 어긋난 줄 0 · 목록 앞 빈 줄 확인 · Python-Markdown 렌더 표 11 · 문단 속 깨진 표 0)
- 그림 `litdb/figures/shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis/` — 크롭은 **손대지 않았고** (`--clean` 안 돌림), figures.json 에 이번 세션의 열람 기록 키 `note_session2` 하나만 **보탰어요** (다른 키 · 값은 그대로 — 전후 비교 확인)
- 이 보고 파일

공유 파일 · git 은 안 건드렸어요. 넣을 줄은 아래 (a) · (b) · (h) 에 있어요.

---

## 사용자 설명

**한 줄로**: 액체 전해질 Li–S 전지에서, 폴리설파이드를 거의 안 녹이는 용매 (CPME) 에 조금 더 잘 녹이는 용매 (THF) 를 22:3 으로 섞었더니 셔틀은 안 생기면서 반응은 빨라졌다는 논문이에요. 우리 계 (LPSCl 고체전해질) 와는 다른 계라서 물성 숫자는 비교 안 하고, 계산 방법이랑 개념만 맞대 봤어요.

**배경을 한 단계씩**:
1. Li–S 전지는 방전할 때 S₈ 가 Li₂S 로 가는 길에 **폴리설파이드 (Li₂Sₓ, LiPS)** 라는 중간체를 거쳐요. 보통 에테르 전해질은 이걸 잘 녹여서, 녹은 LiPS 가 음극까지 갔다 오는 **셔틀** 이 생기고 용량이 빠져요.
2. 그래서 LiPS 를 거의 안 녹이는 **약용매화 전해질 (SSE)** 을 쓰면, 반응이 녹지 않은 채로 고체 쪽에서 진행해요 — 이걸 **준고체 황 반응 (QSSSR)** 이라고 불러요. 셔틀은 막히는데, 대신 입자 **표면에서 전하 이동이 느려서** 반응이 굼떠요.
3. 이 논문의 아이디어는 "**벌크는 안 녹이게 두고, 반응 표면에서만 살짝 녹이자**" 예요. CPME 가 벌크를 맡고, THF 가 Li⁺ 의 첫 용매화 껍질에 조금 들어가서 표면에서 생기는 LiPS 를 그때그때 녹여 준다는 해석이에요. 바깥쪽 THF 는 CPME 와 '쌍극자 결합' 으로 묶여 있어서 벌크에선 LiPS 를 안 녹인다고 해요.

**실측으로 받쳐지는 것**: Li₂S₆ 용해도 ≈50 → ≈80 mM[S] (THF 를 반반 넣으면 ≈600) · 이온전도도 0.3 → 1.2 mS cm⁻¹ · Li⁺ 수송수 0.40 → 0.56 · PITT 로 본 Li₂S 석출 피크가 4.27 → 2.88 h 로 빨라짐 · 두꺼운 전극 (5 mg cm⁻² · 3 µL mg⁻¹) 율 성능 0.1 C 5.4 / 2 C 2.1 mAh cm⁻² · 2.44 Ah 파우치 434 Wh kg⁻¹ (포장 제외 · 첫 사이클). 셔틀이 없다는 것도 GITT · 셔틀 전류로 직접 쟀어요.

**계산이 실제로 한 일 — 그리고 약한 곳**:
- **AIMD** (VASP · PBE-D3 · 50 ps · 298 K): 상자 안 Li⁺ 주변에 무엇이 몇 개 붙는지 (배위수) 를 냈어요. 그런데 논문이 분자 수를 안 적어서 원자 수 355 · 369 와 상자 크기로 거꾸로 풀어 보니 **Li⁺ 가 상자마다 2 개**예요 (그림 스냅숏에도 초록 구가 둘씩 보여요). 그래서 'THF 0.5 개' 는 사실상 THF 한 분자가 붙어 있었다는 크기예요. 우리 관측창 규칙으로 보면 (298 K · 50 ps · 기회 2) 기대 사건 1 개에 해당하는 장벽이 ≈0.18 eV 라, 껍질 교환이 그보다 어려우면 이 숫자는 처음 배치의 기억일 수 있어요.
- **분자 DFT** (Gaussian · B3LYP-D3(BJ)): THF–CPME 한 쌍 0.21 eV 를 '강한 쌍극자 결합' 의 근거로 쓰는데, THF–THF · CPME–CPME 쌍을 안 계산해서 "특별히 더 끌린다" 는 비교가 없어요. Li₂S₆ 에 용매가 붙는 에너지 (`Fig. S8`) 는 **왼쪽 두 막대 위 분자 그림이 라벨과 뒤바뀌어** 있어요 (다섯 값을 더해 보는 가산성 검산으로는 x 축 라벨이 맞아요).
- **β-S₈ 면 흡착**: THF 가 (−221) 면에 제일 세게 붙어서 그 면이 드러난다는 그림인데, **계산 방법이 한 줄도 없어요**. 게다가 더 큰 분자인 CPME 가 THF 보다 4–9 배 약하게 붙고, 면 사이 차이가 0.05–0.10 eV (실온 열에너지의 2–4 배) 라서 근거로 쓰기 어려워요.

**그림과 본문이 어긋난 곳 (중요한 것만)**:
- `Fig. 5e` 의 '800 mAh g⁻¹ 로 200 사이클 안정' 은 그래프가 흩어짐 없는 일직선이고, 같은 조건 첫 사이클 (`Fig. S19`) 방전이 1.2 V 가 아니라 ≈2.0 V 에서 끝나요 → **용량을 800 에서 끊는 사이클**로 보여요 (논문은 안 밝혀요). 그러면 유지율 근거가 아니에요.
- 얇은 전극 율 시험 (`Fig. S18`) 은 0.5–3 C 에서 **오히려 CPME 셀이 더 높아요**. "CPME 보다 낫다" 는 4–5 C 에서만 맞아요.
- S₈ 재석출 피크 시간을 본문은 2.28 h 라고 쓰는데 그림에 찍힌 값은 1.8 h 예요 (2.28 은 그 계단의 전압 V 예요).
- 그 밖에 이온전도도 막대 · 셔틀 전류 · operando XRD 소비율 · 분극 '12 vs 70 mV' 도 본문 숫자가 그림과 달라요 (digest §10 에 25 개 정리).

**우리 계산과 닿는 곳**:
- MD 방법: 그쪽은 DFT 힘으로 돌린 AIMD, 우리는 UMA MLIP-MD 라서 힘 축이 달라요. 보고량도 그쪽은 배위수 (구조), 우리는 MSD → D (수송) 라서 숫자 비교는 없어요. 대신 "이온 몇 개 × 몇 ps × 시드 몇 개" 를 같이 적어야 배위수를 정량으로 말할 수 있다는 걸 반면교사로 가져왔어요.
- 분자 DFT: 우리 ORCA r2SCAN-3c 는 BSSE 기하 보정 (gCP) · D4 가 들어 있는 묶음이라, 이런 작은 결합에너지에서 차이가 날 수 있어요. 그리고 SDCP 때 배운 "상태 (배좌 · 스핀) 선택 규칙이 없으면 스칼라 하나가 정의 안 된다" 는 규율의 외부 사례예요.
- 개념: 전고체 Li–S 에는 '표면에서 잠깐 녹는 중간체' 가 아예 없어서, 그 역할을 혼합 전도체나 **반응에 끼는 고체전해질 자체**가 해요. 우리 산화 개시 (층① · S²⁻ 한계) 가 Li–S 충전 평탄 근처라서, LPSCl 을 쓰는 전고체 Li–S 에선 SE 산화가 열역학적으로 허용되는 창에서 셀이 돌아요 — 그 실측 쪽은 cronk2026 카드가 정본이에요.
- ⛔ 이 논문으로 li2s 쪽 새 카드 · 트랙 · 런은 제안하지 않았어요 (11-16 닫힘). 우리 SEI 트랙의 Li₂S 결정 NEB 와는 질문이 달라서 옆에 두지 않았어요.

**제일 날카로운 세 가지**:
1. **'수송' 과 '표면 용매화' 가 안 갈렸어요** — CPME/THF 는 전도도가 4–5 배라 분극 · 율 개선 대부분이 수송만으로도 설명돼요. 논문 `Table S1` 에 같은 전도도의 대조군 (CPME 2.5 M 0.83 ≈ CPME/THF 24:1 0.85 mS cm⁻¹) 이 있는데 셀에 안 넣었어요.
2. **분자 기전 근거가 얇아요** — Li⁺ 2 개 · 50 ps AIMD, 기준 없는 이량체 하나, 방법 없는 슬랩 흡착이 기전의 전부예요. 실측 결과 (셔틀 억제 + 빨라짐) 는 서는데 '왜' 는 안 서요.
3. **문헌 읽기 체크로 쓸 만한 판별법** 두 개를 얻었어요 — 용량 제한 사이클 판별 (흩어짐 0 평탄선 + 방전 끝 전압 + CE ≥ 100 %), Scharifker–Hills 판정 감사 (축 꼴 · 피크 전 무판별 · 유한 반응물 고갈).

궁금한 데 있으면 물어봐 주세요 — 예를 들어 AIMD 상자 역산이나 용량 제한 판별 근거를 그림으로 같이 볼 수 있어요.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## ⚡🔩 Li–S 전환형(conversion) 양극 × LPSCl 촉매전해질 — 확률적 기하 + FEM (2026-09-03 신설)` 의 표 (`| slug | 논문 | 축 |`) — `papers/guan2026_feco_vs_in2s3_li2s_electrocrystallization.md` 행 **바로 뒤** (같은 액체 Li–S · 같은 Scharifker–Hills 판정). 분류기는 **[dft]** (`build_index.py --check` 가 그렇게 찍어요). Jeff Sakamoto 아님 → 🏷 배지 없음. talk 대기열에 없음 → 🎤 꼬리 없음.

```
| `papers/shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis.md` **(본문 11 pp + SI 25 pp · 크롭 31 장 (본문 그림 5 + Scheme 1 + TOC · SI 그림 20 · SI 표 2 · 식 블록 2 · 손 크롭 6 · 다시 자름 2) 중 24 장 원해상도 + 4 장 축소 시트로 봄 · 확대 판독 10 패널 · 표는 PDF 글자층 · 2026-11-25)** | **[외부·⚠ 액체 (sparingly solvating) 전해질 Li–S (SE 아님) — 물성 4축 수치 비교 제외 · 🔧 AIMD 용매화 표본 · 분자 결합에너지 기준 · 방법 없는 슬랩 흡착 · 성능 주장 감사]** ✅ **Chunli Shen**#/**Lujun Zhu**#/Mengxue He/Wencong Feng/Xufeng Hong/Yuanrui Li/**Yatao Liu\***/Chenyan Ma/Lei Zheng/**Quanquan Pang\*** (北京大 · 北京化工大 · IHEP CAS), "**Interacting Cosolvents-Regulated Solvation for Rapid Quasi-Solid-State Sulfur Reactions in Li–S Batteries**" (*ACS Nano* 2026 ASAP, DOI 10.1021/acsnano.6c12314). 1 M LiTFSI CPME/THF (22:3 v/v) · Li₂S₆ 용해도 ≈50 → ≈80 mM[S] (1:1 ≈600) · σ 0.3 → 1.2 mS cm⁻¹ (`Fig. 1a` 막대 ≈0.22 / ≈1.11) · t₊ 0.40 → 0.56 · PITT Li₂S t_m 4.27 → 2.88 h · 두꺼운 전극 (5 mg cm⁻² · 3 µL mg⁻¹) 5.4 / 2.1 mAh cm⁻² (0.1 / 2 C) · 파우치 2.44 Ah · 434 Wh kg⁻¹ (포장 제외 · 40 cyc ≈61 % figure-read). 계산 = VASP PBE-D3 AIMD 50 ps (상자 역산 **Li⁺ 2 개**) · Gaussian B3LYP-D3(BJ) 이량체 0.21 eV (기준 이량체 없음) · Li₂S₆ 착물 (`Fig. S8` 왼쪽 두 그림 라벨과 뒤바뀜) · β-S₈ 면 흡착 (방법 전무 · CPME 가 THF 보다 ≈4–9 배 약함). 🔴 **우리 감사**: `Fig. 5e` 800 mAh g⁻¹ × 200 cyc = 용량 제한 사이클로 보임 (`Fig. S19` 방전 ≈2.0 V 끝) · `Fig. S18` 0.5–3 C 는 CPME 가 더 높음 · S₈ t_m 본문 2.28 h ↔ 그림 1.8 h · 같은 σ 대조군 (2.5 M CPME ≈ 24:1) 미시험 → 수송–표면 용매화 교락. | **액체 Li–S 전해질 (SSE · 준고체 반응) · AIMD/분자 DFT 보고 규약 감사 · 문헌 성능 주장 판별법 (용량 제한 · S–H)** — 🔧 §J-96 · ⛔ 우리 SEI 트랙 Li₂S 결정 NEB 옆에 두지 않는다 |
```

## (b) 비교 문서에 넣을 줄 (`litdb/comparison_vs_ours.md`)

⛔ A–D 물성 4축 표에는 **행을 만들지 않아요** (방법 원전 · 액체 전해질). 두 군데만:

**① `## 📑 Reference key` 표** — `[Guan26FeCo]` · `[Luo26Sep]` 행 근처 (같은 Li–S 묶음):

```
| **[Shen26CoSol]** 🔧🔴 **방법 원전 (AIMD 용매화 표본 · 분자 결합에너지 기준 · 방법 없는 β-S₈ 면 흡착 · 성능 주장 감사)** · ⛔ **액체 (SSE) 전해질 Li–S — A–D 물성 4축 진입 금지** | **Chunli Shen**#/**Lujun Zhu**#/…/**Yatao Liu\***/…/**Quanquan Pang\*** (北京大 · 北京化工大 · IHEP CAS) 2026 ***ACS Nano* ASAP** (DOI 10.1021/acsnano.6c12314) — "Interacting Cosolvents-Regulated Solvation for Rapid Quasi-Solid-State Sulfur Reactions in Li–S Batteries" | ✅ `papers/shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis.md` — 판정 §J-96 | exp 주 + 계산 보조 (VASP PBE-D3 AIMD 50 ps · Gaussian B3LYP-D3(BJ) · 슬랩 방법 미기재) |
```

**② §J 끝에 새 블록** — `### J-95.` 블록의 ⛔ 줄 뒤 · `---` / `## K.` 앞 (번호는 합칠 때 다음 빈 번호로):

```
---

### J-96. 🔧🔴 **방법 원전 — [Shen26CoSol] 액체 Li–S 공용매 (CPME/THF) 전해질 (*ACS Nano* 2026 ASAP): Li⁺ 2 개 · 50 ps AIMD 의 배위수 · 기준 없는 이량체 결합에너지 · 방법 없는 β-S₈ 면 흡착 · 용량 제한 사이클** (2026-11-25 신설)

> 📎 출처: `papers/shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis.md` (크롭 31 장 중 24 장 원해상도 + 4 장 축소 시트 · 확대 판독 10 패널). ⛔ 액체 (sparingly solvating) 전해질 Li–S — A–D 물성 4축에 행을 만들지 않는다. 트랙: 우리 DFT 기준선 (사용자 1저자) — 방법 감사만.

| 계산 · 서술 | 논문 값 | 우리 규율로 다시 읽으면 | 판정 |
|---|---|---|---|
| AIMD 첫 껍질 CN (`Fig. 1d–f`) | CPME 2 + TFSI⁻ 2 · CPME/THF: CPME ≈1.5 + TFSI⁻ ≈2 + THF ≈0.5 | 조성 미기재 → 원자 수 역산 CPME 17 + LiTFSI 2 · CPME 15 + THF 4 + LiTFSI 2 = **Li⁺ 2 개** · 50 ps · 298 K · 궤적 1. 관측창 (298 K · 50 ps · 기회 2 · ν₀ 10¹³ s⁻¹ 가정 · 정상성 가정): 기대 사건 1 ≈0.18 eV (검출 63 %) · 95 % 검출 ≈0.15 eV (`collect_neb.py --obs_window`) | ⚠ CN 0.5 = THF 한 분자 크기 — 정량 아님 (우리 멀티시드 규율로는 관측 1 회) |
| CPME–THF '쌍극자 결합' (`Fig. S4`) | ΔE 0.21 eV (B3LYP-D3(BJ)/6-311+G(d,p)) · O···H 2.49 Å / AIMD 2.59–2.90 Å | 기준 이량체 (THF–THF · CPME–CPME) 없음 → 섞임 에너지 미산출 · BSSE 없음 · O···H 는 반데르발스 접촉 거리 | 🔴 '특별한 짝' 근거 아님 |
| Li₂S₆–용매 결합 (`Fig. S8`) | figure-read CPME −0.76 · THF −1.02 · 2THF −1.96 · THF–CPME −1.73 · 2CPME −1.51 eV | 기상 맨 Li 자리 포화 에너지 · 배좌 · 상태 선택 규칙 없음 (회신 N) · **왼쪽 두 분자 그림이 x 축 라벨과 뒤바뀜** (가산성은 라벨 지지) · \|E\| < 2 eV (배위수 규칙 문턱 아래) | 🔴 용액 용매화 세기로 쓰지 않는다 |
| β-S₈ 면 흡착 (`Fig. 4e` · `Fig. S15`) | THF (−221) ≈ −0.27 · (130) ≈ −0.22 · (300) ≈ −0.17 · CPME ≈ −0.048 · −0.056 · −0.018 eV (figure-read) | 슬랩 방법 전무 · CPME (19 원자) 가 THF (13 원자) 보다 ≈4–9 배 약함 · 면 차 0.01–0.10 eV (≈0.3–4 kT) · CPME 우세 면 본문 (300) ↔ SI · 그림 (130) | 🔴 면 선택성 · 집합조직 근거 아님 |
| 성능 (`Fig. 5e` · `Fig. S18`–`S20` · `Fig. 5h`) | 800 mAh g⁻¹ × 200 cyc · 고율 우위 · 5.2 mAh cm⁻² × 50 cyc · 2.44 Ah × 40 cyc | 흩어짐 0 평탄선 + `Fig. S19` 방전 ≈2.0 V 끝 → **용량 제한** · 0.5–3 C 는 CPME 가 높다 · 50 cyc ≈3.5 mAh cm⁻² · 파우치 40 cyc ≈61 % · 포장 제외 · 함의 평균 전압 ≈1.82 V (우리 산수) | ⚠🔴 문헌 성능 주장 판별법의 실례 |

⛔ 인용 금지 — AIMD CN ≈0.5 를 정량으로 · 0.21 eV 를 '강한 특이 상호작용' 으로 · `Fig. S8` 결합에너지를 용액 용매화 세기로 · β-S₈ 흡착값을 면 선택성으로 · `Fig. 5e` 를 유지율로 · 이 논문의 Li₂S (액체 셀 방전 산물 · Scherrer ≈4.5–7.5 nm) 를 우리 SEI 트랙 Li₂S 결정 NEB (CONDITIONAL · `HZ-sei-neb-li2s-cc-cellconv`) 옆에.
```

(물성 4축이 아니라 `comparison_vs_ours_DEM.md` 쪽도 해당 없음 — DEM · 미세구조 내용이 없어요.)

## (c) `litdb/pdf_map.tsv` 줄

**필요 없어요** — `extract_figures.py --inbox --only shen2026 --dry` 가 본문 · SI 를 **제목 100 %** 로 자동 짝지어요 (inbox 파일명이 slug 로 시작). 굳이 고정하고 싶으면:

```
shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis	shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis_
```

## (d) 추가로 먹일 논문 (≤ 8 · 최근 2 년 먼저 · 전부 litdb 에 없음 · 전부 Crossref 로 서지 확인)

발견 검색은 Crossref REST 만 썼어요 (일반 UA · 개인 정보 없음) — 주제어 12 번 (앞 세션 6 + 이번 4 · 2025 이후 필터 대부분) + 제목 확인 2 번 + DOI 확인 17 건. litdb 에 있는지는 DOI · 제목 조각으로 `rg` (digest · json · tsv) 해서 0 건 확인.

| # | 논문 | 왜 | litdb |
|---|---|---|---|
| 1 | Mistry, Kundu, Yang, Wang, Stockham, Spencer … **"Solid–liquid electrolyte interphases in quasi-solid-state lithium–sulfur batteries with argyrodite-type solid electrolyte separators"** — *Faraday Discuss.*, 269, 369 (2026). DOI 10.1039/d6fd00058d | ★★ **argyrodite SE 분리막 + 준고체 Li–S** — 이 논문 (액체 SSE) 과 우리 계 (argyrodite) 를 직접 잇는다 · SE\|액체 계면상 | 없음 |
| 2 | Yu, Singh, Yu, Nazar **"Suppressing argyrodite oxidation by tuning the host structure for high-areal-capacity all-solid-state lithium–sulfur batteries"** — *Nat. Mater.*, 24, 1082 (2025). DOI 10.1038/s41563-025-02238-2 | ★★ 우리 **축 B (argyrodite 산화)** 를 전고체 Li–S 에서 다룬다 · cronk2026 의 LPSCl 분해와 짝 | 없음 |
| 3 | Zhang et al. **"Synergistic Electrolyte Solvation and Mediation Engineering for Quasi-Solid-State Sulfur Electrochemistry"** — *ACS Nano*, 20, 21459 (2026). DOI 10.1021/acsnano.6c10639 | 같은 하위 분야 (준고체 S 전기화학 · 용매화 + 매개) 최신 — 이 논문 주장의 재현 · 대안 | 없음 |
| 4 | Lai, Liao, Manthiram **"Modulating Li⁺ and Polysulfide Solvation with Low-Density Moderately Solvating Electrolytes …"** — *Angew. Chem. Int. Ed.*, 65, e22940 (2026). DOI 10.1002/anie.202522940 | 중간 용매화 · 저밀도 전해질 — THF 역할의 다른 해석 | 없음 |
| 5 | Peng et al. **"Rational Electrolyte Solvent Screening for Practical Lithium–Sulfur Batteries"** — *ACS Energy Lett.*, 11, 4125 (2026). DOI 10.1021/acsenergylett.6c00790 | 용매 선별 기준 (계산 · 실험) — 방법 쪽 | 없음 |
| 6 | Liu, An, Fang, … Pang **"Surface-localized phase mediation accelerates quasi-solid-state reaction kinetics in sulfur batteries"** — *Nat. Chem.*, 17, 614 (2025). DOI 10.1038/s41557-025-01735-w | 같은 그룹 전작 (이 논문 ref 26) — '표면 국소 용액 영역' 개념의 원전 | 없음 |
| 7 | Gadea, Soria-Fernández, Santiago, Carriazo, Castillo **"Design strategies and future directions of sparingly solvating electrolytes for lithium-sulfur batteries"** — *Commun. Mater.*, 7, 9 (Crossref 발행 2025). DOI 10.1038/s43246-025-01026-4 | SSE 설계 리뷰 — 분야 지도 | 없음 |
| 8 | Shao, Pang, Bird, Robinson, Shearing **"Contemporary Trends in Lithium-Sulfur Battery Design: A Comparative Review of Liquid, Quasi-Solid, and All-Solid-State Architectures and Mechanisms"** — *Adv. Energy Mater.*, 16, e03239 (2026 · Crossref 발행 2025). DOI 10.1002/aenm.202503239 | 액체 → 준고체 → 전고체 Li–S 사다리 (이 논문 ref 7) — 우리 전고체 Li–S 카드 묶음의 지도 | 없음 |

(빼 둔 후보: Chen 2025 *Energy Storage Mater.* 83, 104502 (약용매화 Li–S 동역학) · Jin 2025 *Angew.* e202504898 (약용매화 율 성능) · Jarrold & Manthiram 2025 *Commun. Mater.* 6, 240 (전고체 Li–S 전해질 전략) · Kim 2024 *Nat. Commun.* 15 (용매화–물성 관계 · 2 년 밖).)

## (e) W_ad · DEM-DFT 공유 보고서 (`docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html`) 에 쓸 거리

**없음** — 그 보고서는 점착 일 W (C–C · Ag–C · LPSCl\|Ag · LPSCl\|흑연) 와 Li 금속 계면 (lithiophilicity · 공극 · 적층압) 축인데, 이 논문에는 점착 · 접촉 역학 · Li 친화도 정량이 없어요. 가까운 것 (β-S₈ 면 흡착 0.02–0.27 eV) 은 액체 용매 분자의 물리흡착이고 방법이 없어서 8-2 '계산 선례의 함정' 에도 넣을 값이 아니에요. Li‖Cu 는 SEM (`Fig. S16`) 만 있고 CE 숫자가 없어요.

## (f) 그림 크롭 요약 (본 것 / 안 본 것)

- **크롭 31 장** = 본문 그림 5 + Scheme 1 + TOC · SI 그림 20 · SI 표 2 · 식 블록 2. 앞 세션 손작업: 손 크롭 6 (`Fig. S5` · `S7` · `S19` — 추출기가 '그래픽 없음' 으로 버린 벡터 그림 · TOC · 식 (1)–(2) · (3)–(6)) · 다시 자름 2 (`Fig. S11` 위 절반 · `Fig. S18` x 축 제목). `missing_labels` [] · 번호 공백 0.
- **이번 세션에 원해상도로 본 것 24 장**: `Scheme 1` · `Fig. 1`–`5` · `Fig. S1` · `S3` · `S4` · `S8` · `S9` · `S10` · `S11` · `S12` · `S13` · `S14` · `S15` · `S16` · `S17` · `S18` · `S19` · `S20` · 식 블록 2.
- **확대 판독 10 패널**: `Fig. 1a` · `2d` · `2e` (새로) · `3b` (새로) · `3c` · `4c` · `4e` · `5b,c` · `5e` (새로) · `5h` (새로) + `Fig. S8` 원래 래스터 (분자 그림 확인). 확대 PNG 는 scratchpad 에만 (repo 에 안 넣음).
- **축소 접촉 시트로만 본 것 4 장**: `Fig. S2` · `S5` · `S6` · `S7` (내용 · 인쇄 숫자만).
- **안 본 것 3 장**: `fig_toc.png` (캡션상 `Scheme 1` 가운데 원화와 같음) · `Table S1` · `Table S2` (PDF 글자층으로 읽음).
- **본문 서술과 어긋난 그림**: `Fig. 1a` (σ 막대 ≈0.22 / ≈1.11 ↔ 본문 0.3 / 1.2) · `Fig. 2d` (셔틀 '20/213 µA at 2.3 V' ↔ 2.35 · 2.40 V · 213 은 neat THF) · `Fig. 2e` · `Fig. 5b,c` ('12 vs 70 mV' 재현 안 됨) · `Fig. 3c` (t_m 1.8 h ↔ 본문 2.28 h) · `Fig. 4c` ('~80 % at ~20 % DOD' ↔ ≈50 % · SI 'Li₂S 소비 비슷' ↔ ≈48 vs ≈76 % SOC) · `Fig. 4d` · `Fig. S13` (CPME 우세 (130) ↔ 본문 (300)) · `Fig. S8` (왼쪽 두 분자 그림 뒤바뀜) · `Fig. S18` (0.5–3 C CPME 우위 ↔ 'surpassing') · `Fig. 5e` + `Fig. S19` (용량 제한) · `Fig. S20` ('5.2 over 50 cycles' ↔ 50 cyc ≈3.5) · `Fig. 5h` ('stable' ↔ ≈61 %) · `Fig. S1` (I_ss × R > ΔV) · `Fig. S10` (1:1 '충전 중 증가' 의심) · `Fig. S12c` (섬보다 구멍) · `Fig. S14` (세기 ≈0 구간 크기 점) · `Fig. S17` (20 ↔ 10 사이클). 전부 digest §10.
- figures.json: `note_session2` 키 하나 보탬 (이번 세션 열람 목록 · 그림이 digest 를 바꾼 지점 넷).

## (g) Jeff Sakamoto 저자 여부

**아니에요** — 저자 10 명 (Shen · Zhu · He · Feng · Hong · Y. Li · Y. Liu\* · Ma · Zheng · Pang\*) 중 없음. INDEX 행에 🏷 배지 안 달았고, 웹앱 `_paper_pis` = [] 확인.

## (h) 다른 Li–S digest 에 덧붙일 줄 (각 digest 머리 blockquote 의 '🔗 관련' 줄 근처 · 내가 고치지 않았어요)

- `papers/cronk2026_lis_cathode_interphase_chemistry.md`
  `> 🔗 **관련 (2026-11-25)**: `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` — 액체 SSE (CPME/THF) Li–S · '반응하는 전해질' 이 없는 액체 쪽 끝점 (이 카드의 S 표면 Li₃PS₄₊ₙ · LPSCl 분해와 대조) · 준고체 반응 정의 · Li₂S 2D/3D 성장 판독 감사.`
- `papers/cronk2026_lis_positive_electrode_geometry_fem.md`
  `> 🔗 **관련 (2026-11-25)**: `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` — 액체 Li–S 의 Li₂S 2D 막 (부동태) ↔ 3D 섬 (표면 유지) 판독 (PITT · SEM) — 이 카드 '활성 표면' 개념의 액체판 · ⛔ 기하 · 응력 수치 비교 없음.`
- `papers/lin2026_p_doped_compounds_li_s_review.md`
  `> 🔗 **관련 (2026-11-25)**: `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` — 이 리뷰 범위 밖의 전해질 쪽 전략 (약용매화 SSE + 공용매) 1차 논문 · 흡착 · 결합에너지 보고 규약 반례 (슬랩 방법 미기재) 가 같은 결.`
- `papers/luo2026_lis_separator_crystal_engineering_review.md`
  `> 🔗 **관련 (2026-11-25)**: `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` — '작동 상태 ≠ 초기 상태' 의 구체 사례 (초기 α-S₈ → 재충전 β-S₈) · 방법 미기재 면 흡착 (0.02–0.27 eV) 의 보고 규약 반례.`
- `papers/wang2025_miec_tis2_lps_three_phase_interface_lis_assb.md`
  `> 🔗 **관련 (2026-11-25)**: `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` — 액체 SSE 쪽 '표면 국소 용매화' (전고체에선 불가능 → MIEC 가 대신) · VASP AIMD 보고 항목 비교 (이쪽 액체 50 ps · Li⁺ 2 개).`
- (선택) `papers/guan2026_feco_vs_in2s3_li2s_electrocrystallization.md`
  `> 🔗 **관련 (2026-11-25)**: `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` — 같은 Scharifker–Hills 네 식 · 이론 곡선 축은 바르게 그렸지만 피크 전 무판별 · 유한 반응물 고갈 대안은 같다 (S–H 감사 짝).`
- (선택) `papers/wei2026_data_driven_hea_mediator_lis.md`
  `> 🔗 **관련 (2026-11-25)**: `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` — 같은 *ACS Nano* 2026 ASAP Li–S · PITT/GITT/in situ EIS · 흡착 DFT 보고 규약 대비 (이쪽은 슬랩 방법 전무).`

---

## 부록 1 · 점검 기록

- inbox 두 파일 sha256 = batch.json 일치 (본문 `391c8669…a484a` · SI `97267702…8ee8f4`).
- `build_index.py --check` (rc 1) → 이 slug 는 두 곳에만 떠요: '어느 인덱스에도 없음 **[dft]**' · 'comparison_vs_ours.md 미편입'. 위 (a) · (b) 를 넣으면 풀려요. 쓰기 전 기준선은 rc 0 이었어요.
- 웹앱 (Flask test client): `/paper/<slug>` 200 · 렌더 표 11 · `/api/paper/<slug>` 그림 31 중 주석 28 (TOC · 식 블록 2 는 번호 참조가 없어 주석 없음 — 정상) · 원소 태그 Li · S · O · C · N · F 여섯 원소 쪽 목록에 다 잡힘 · `_paper_pis` = []. ⚠ **화면 캡처 (데스크톱 · 폰 폭) 는 안 했어요** — 브라우저 렌더는 확인 못 한 것으로 적어요.
- talk 인입 대기열: 대기열이 있는 talk 은 `lee2026_skku_mlip_materials_design.md` 하나 · 이 논문 행 없음.
- 우리 점착 W 값: digest 에 J m⁻² 숫자 0 (위치 `db/properties/adhesion.json` 만). 우리 Li₂S 값: 0 (위치 `citation_hazards.json` `HZ-sei-neb-li2s-cc-cellconv` 만). li2s 새 카드 · 트랙 · 런 제안 0. ESW 는 '층① · S²⁻ 한계' 로 축을 이름 붙여 한 번 (`our_dft_baseline.md` 값 · 문헌 표와 안 섞음).
- 규칙 적용: 관측창 한 줄 (§5.2 · `collect_neb.py --obs_window 298 50e-12 2` → 0.18 / 0.15 eV · 기회 8 이면 0.21 / 0.18) · 홉 수 검산은 장벽 인용이 없어 해당 없음 · 배위수 규칙은 \|E\| < 2 eV 라 문턱 아래지만 `Fig. S8` 자리 (기상 저배위 Li) 를 적었어요.
- 산수 검산 (digest 에 '우리 산수' 로 표시): AIMD 상자 조성 역산 · 몰비 (22:3 v/v → THF/CPME 0.20) · σ 셀 상수 · 파우치 S 질량 · 이용률 · 함의 평균 전압 · 포장 포함 Wh kg⁻¹ · N/P 두 셈법 · Li₂S₆ 합성비 (8:3 → Li₂S₅.₃) · `Fig. S8` 가산성 · S–H 이론 곡선 값 · t₊ 옴 법칙 · Boltzmann 인자.
- git: add · commit · push · checkout · reset · stash 안 했어요. `extract_figures.py` 는 `--inbox --only shen2026 --dry` (쓰기 없음) 만. inbox 를 읽은 python 은 `-I` 로 돌렸어요. 임시 파일은 전부 scratchpad `shen2026_lis/` 아래 (`shen2026_` 접두어).

## 부록 2 · 영문 인용 문장 기준표 (digest §12 · 사용자 채점용 · 각 10 점)

| 항목 | 보는 것 | 점수 |
|---|---|---|
| 논지 | 문장이 논문이 실제로 받친 범위 (실측) 와 해석 (기전) 을 갈라 쓰나 | _/10 |
| 시제 | 남의 실험 · 계산 행위 = 과거 · 일반 사실 = 현재 (BML 가이드) | _/10 |
| 출처 | 랩 표기 *ACS Nano*, ASAP (2026) · DOI · figure-read 값 표시 | _/10 |
| 영어 | 관사 · 병렬 · 직렬 쉼표 · 'cell' 이중 의미 (simulation cell 로 명시) | _/10 |

— 끝 (2026-11-25 · 이 보고가 이 배치 #1 의 마지막 쓰기다 · digest · figures.json 마지막 손질 뒤에 다시 썼다)
