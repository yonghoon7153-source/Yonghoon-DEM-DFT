# Cowork 프롬프트 — 안용훈 연구 프로필 (Claude Code 2차 판정, 2026-09-04)

> 이걸 그대로 Cowork 세션에 붙여 넣고 메모리에 옮긴다.
> Cowork 는 repo 를 못 읽으므로 **이 문서가 유일한 근거**다. 전문은 repo 의
> `REPORT_TO_COWORK.md`(1105행) · `research-agent/config/research_profile.md` 에 있다.

---

## ⛔ 먼저 — 이전에 준 프로필 중 버려야 할 것

1. **"DFT→MLIP→DEM→FEM 하나의 multi-scale 파이프라인"** — 틀렸다. 두 축은 별개다.
2. **"MPM/voxelization 은 문헌 단계"** — 틀렸다. MPM 은 production 이고 최근 90일 커밋에서
   **가장 많이 언급된 주제(283회)** 다. (이건 Claude Code 의 1차 보고 오류이기도 하다.)
3. **"두 litdb 를 통합할지 결정 필요"** — 틀렸다. 이미 2026-07-16 에 정해졌다.

---

## 안용훈은 누구인가

**한 사람이 황화물계 전고체전지(ASSB)를 두 스케일에서 따로 공격한다.**
두 축은 git 상 **공통 조상이 없는 별개 브랜치**이고 코드를 공유하지 않는다.
소속: Division of Materials Science & Engineering, **Hanyang University**.
영문 표기는 **Yonghoon An** (Kim·Ahn 은 오기).

### 축 A — DEM / MPM / voxelization (브랜치 `claude/stoic-knuth-NObVQ`, 2652커밋)

황화물 복합양극을 **DEM(LIGGGHTS)과 MPM(Taichi GPU, J2 소성) 두 독립 모델**로 압밀하고,
**접촉망 Kirchhoff σ**(Holm 협착)와 **복셀 유한체적 σ**(∇·σ∇φ=0) 두 개의 독립 수송 해를 구한 뒤
전기화학(비선형 BV + 구형확산)까지 밀어 ASR·율특성을 낸다. 마지막에 전부를 **물리로 구조화된
회귀**로 압축한다.

- 파이프라인(축 A **내부**): STEP1 DEM → STEP2 MPM → STEP3 복셀 σ → STEP4 전기화학 → STEP6 surrogate
- **최종 목표(사용자 원문)**: *"설계 수치 입력 → ML 이 전 물성 예측 → 그 수치에 맞는 2D 미세구조를
  그리고 → 서로 다른 구성을 한 복합양극 안의 층으로 쌓는다"*
- 계: NCM811 bimodal(AM_P poly / AM_S single-crystal, 문턱 3.5 µm) · Li₆PS₅Cl · 첨가제 VGCF·SuperP·
  PTFE·**SDCP**(σ 250 mS/cm) · P:S 0:10~10:0 · 100–400 MPa · SBE/DBE
- 확보값: porosity 15–19.7 % · σ_ionic 0.117–0.173 · σ_e 3.18–4.63 · σ_th 3.42–4.33 mS/cm ·
  percolation 92–99.7 % · τ_Lap 1.21–4.39 · CN(AM–AM) 2.73–3.86
- 스케일링 법칙 3종 FINALIZED: **σ_ionic LOOCV 0.9752**(n=90/k=5) · σ_e Stage 22.5 **0.9531** ·
  σ_thermal T1 **0.9028**(Ridge α=0.05, 14 feature)
- 보정: MPM E_eff 1.53 GPa·σ_y 0.15 GPa(Minnmann 앵커) · DEM E_SE 24→**1.35 GPa(18× 연화)** ·
  Heckel R² 0.965·P_y 138 MPa · Furnas dip AM 75–85 wt%(DEM 전용)
- 원고: `docs/paper/main.tex` — *Stage E fracture-aware network solver…* 전 섹션 초안, 편집 중

> ★★ **이 축의 통제 인식론 — frame[4]**: **DEM 과 MPM 을 서로 보정하지 않는다.** 각자 실험에만
> 독립 보정하고 비교한다. 일치 = 교차검증, 불일치 = 정량화된 모형 한계(정보이지 실패가 아니다).
> 강제 일치는 순환논증. ⇒ **"DEM 과 FEM/MPM 을 서로 캘리브레이션했다" 는 논문은 무관이 아니라
> 반례다** — 관련도는 높게 주되 frame[4] 위반을 비판 포인트에 반드시 적는다.

### 축 B — DFT / MLIP (브랜치 `claude/friendly-meitner-lldvar`)

황화물 SE 의 전자구조·탄성·결합·이온수송을 제일원리와 MLIP-MD 로 정량하고, LiNiO₂ 계면 위
바인더 흡착 대비와 SEI 상의 Li 이동장벽을 낸다. **정체성은 물리보다 절차에 있다.**

- 도구: VASP(외주 번들 생성기 1.37 MB/21k줄) · QE CI-NEB · UMA MLIP-MD · ORCA r2SCAN-3c · LOBSTER · BVSE
- 계: Li₆PS₅Cl 계열(comp1–5 · modelc=LPSCl1.6 · +B₂O₃ · LPSOCl · Nd 치환) · LiNiO₂(104)×바인더
  조각(**SDCP vs PTFE**) · SEI 상(Li metal·Li₂S·Li₃N–Nd·Li₂O·Li₃P·Li₃PO₄·LiCl) · Li₃N(001)·LiC₆(0001)
- 확보값(정본 39항목): 밴드갭 **2.066/2.099/1.9671/2.2309 eV**(fixed-occ nscf) · B₀ 21.7–26.2 GPa ·
  탄성 20.0–35.0 GPa · MD Ea 0.15–0.29 eV · ICOHP −5.91~−6.04 eV ·
  NEB Li metal **0.0806** / LiNdO₂ **0.229** / Li₂S **0.305** eV (전부 provisional, 인용 불가)
- **C-12 ΔE_ads(SDCP vs PTFE)는 아직 값이 없다** — 외주 VASP 16잡 발송 전

> ★★ **이 축의 통제 규율**: *"admissible state 가 여럿인데 선택·집계 규칙이 없으면 스칼라
> 보고량은 정의되지 않는다."* 배경 — **SDCP 흡착에너지를 여덟 번 계산했고 여덟 번 반려됐다.**
> 받은 리뷰는 전부 "제대로 돌렸나" 였고 전부 통과했으며, "맞는 양을 재고 있나" 는 여덟 번째에야
> 물었고 즉시 P0 가 나왔다. ⇒ 논문을 볼 때 **"이 논문은 무엇을 보고량으로 정의했는가"** 가
> 비판 포인트 1순위다.

**데이터 규율 (어기면 값이 무효 — 문헌에서도 이 위반을 잡는다)**
- 밴드갭은 **fixed-occupations nscf 고유값만**. DOS-threshold 판독 금지(~0.3 eV 과소)
- **UMA 를 Li₃N 에 금지**(결정론적 편향). LPSCl MD 에는 검증된 표준
- MLIP-MD: MSD 창 **2–50 ps 고정** · 아레니우스 600/800/1000 K · **σ 절대값 인용 금지,
  비율도 멀티시드 판정만**(단일시드 1.33× 철회 사례)
- BVSE 정량은 원본 주기셀 값만
- NEB 전하 규약이 상의 electronic_class 로 갈린다(부도체 V_Li⁻+jellium / 금속 중성공공).
  jellium 은 유한셀 근사 ⇒ **셀 수렴 전엔 상 사이 비교 전용**. BVSE 와 같은 표 금지

### 축 C — 실험 협업 (`이종기술`, 한양대 이종원 그룹) ★ 새로 확인됨

폴더가 아니라 **독립 실험 라인**이다 (README: *"Separate experimental line from SDCP"*).
- AM:SE:VGCF:PTFE = **80:18:1:1** · 소립 4 µm single-crystal NCM(No.1/No.2) · poly:small 5:5
- 대칭셀(SUS∣복합양극∣SUS, 이온 차단 → σ_e) · 풀셀(SUS∣Li-In∣SE∣복합양극∣primer-SUS)
- **BioLogic VSP-300** EIS 원자료 + CNLS 등가회로 fit(R_s/R_int/R_w/R_ion)
- 비용량(5:5) No.1 202.95 · No.2 206.5 mAh g⁻¹ · 면적용량 3 mAh cm⁻² · Li-In · 60 °C
- **풀셀 EIS → R_int 이 STEP4 의 실측 앵커** (V_term = V − I·R_int)
⇒ **EIS·대칭셀·율특성·Li-In·SUS 집전체 실험 논문은 무관이 아니다. 축 C 로 채점한다.**

---

## 두 축의 접점 — 넷이고 전부 "번호 하나" 단위다

한쪽 출력이 다른 쪽 입력으로 **흘러가지 않는다.** 사람이 값 하나를 골라 옮겨 적는다.
이게 파이프라인이 아닌 이유다.

1. **탄성 상수** — 축 B 의 DFT(E_VRH 22.06/27.66 GPa · B₀ 26.23 · ν 0.360 · μ 8.11)가 축 A 물성
   카드에 **인용**돼 있다. ⚠ 축 A 는 그대로 안 쓴다 — DEM 은 18× 연화한 1.35 GPa 를 쓰고,
   DFT 값은 "실-bulk 축" 참조로만 분리해 둔다.
2. **SDCP** — 같은 물질. 축 B 는 LiNiO₂ 위 흡착에너지(C-12), 축 A 는 전극 안 전도성 첨가제.
   축 A 의 SDCP 원고가 **`잔여 = E_bind DFT`** 로 축 B 의 값을 앵커 대기 큐에서 기다린다.
3. **litdb** — 정본은 **`claude/friendly-meitner-lldvar` 의 `litdb/` 하나뿐**(2026-07-16 결정,
   카드 208장). `stoic-knuth` 것(64장)은 **동결 스냅샷, 추가·수정 금지**.
4. 공저자용 Methods .docx 를 양쪽이 각각 낸다 (v7 / v8). 같은 원고인지는 **unknown**.

---

## 관련도 채점

| 점수 | 기준 |
|---|---|
| 0.9–1.0 | 세 축 중 하나의 **내 시스템·내 방법**에 직접 해당 |
| 0.7–0.85 | 같은 방법·다른 시스템, 또는 같은 시스템·다른 방법 |
| 0.5–0.65 | 황화물 ASSB 일반 실험·리뷰 (배경 인용용) |
| 0.35–0.45 | 배터리이나 세 축 어느 쪽과도 연결 약함 |
| <0.35 | rejected (DB 에는 기록) |

**한 축만 맞아도 높은 점수.** 두 축을 억지로 잇는 서술로 점수를 올리지 않는다.

**0.9 이상 조건** — 다음 중 하나: ① DEM 으로 만든 복합양극 미세구조에서 수송 물성(σ, τ,
percolation) ② 저항망/Kirchhoff/Bruggeman 으로 ASSB 양극 풀이 ③ Li₆PS₅Cl 계열의 밴드갭·탄성·
ICOHP·MLIP 확산 ④ LiNiO₂/NCM 계면 위 바인더·분자 흡착 DFT ⑤ SEI 상의 Li 이동장벽 NEB
⑥ 황화물 ASSB 복합양극의 EIS 등가회로 분해

**저자 신호** — Cronau · Trevisanello · Wang · Lawn · Auerbach · Holm · Duquesnoy · Bielefeld ·
Ngandjong · **Zeier** 를 인용하거나 그 값을 쓰면 축 A 에서 0.8 이상.

**감점**: supercapacitor · zinc/sodium-ion · fuel cell · photocatalysis · perovskite solar ·
redox flow · thermoelectric · hydrogen storage · CALPHAD · BMS/SOC 추정

---

## 비판 포인트 (심층 분석에서 반드시 확인)

이 사람의 규율을 위반한 논문은 **무관이 아니라 값어치 있는 비판 대상**이다.
1. 보고량 정의가 있는가 · **상태 선택 규칙**이 있는가 (열린 껍질·자성 기판·산화환원 활성)
2. **수렴을 보였는가** (격자·셀·k-point). 축 A 자신이 격자 미수렴으로 헤드라인을 철회했다
3. **DEM↔MPM/FEM 을 서로 보정했는가** (frame[4] 위반)
4. **DOS-threshold 로 밴드갭**을 읽었는가
5. **단일 시드 MD 로 σ 비**를 주장했는가
6. NEB 를 **셀 수렴 없이 절대값**으로 인용했는가

---

## 하지 말 것

- 두 축을 하나의 multi-scale 파이프라인으로 서술 (사용자가 명시적으로 금지)
- 문헌 수치를 우리 db 절대값과 **같은 표에** 놓기 (방법 명시 없이 이식 금지)
- `stoic-knuth` 브랜치 litdb 에 카드 추가 (동결)
- 설명 없는 LLM 관련도 점수 — 이 사람의 규율("확인 못 한 것은 통과가 아니다")과 정면 충돌한다.
  `rule_relevance` 의 hits 를 항상 같이 보일 것
- 두 브랜치 merge · Scholar alert 자동 등록 · vault 폴더 구조 변경

---

## 지금 제일 위험한 것 (선점 경보 대상)

- 축 A: `main.tex` 가 초안 완성 단계인데 **격자 수렴이 미해결**이라 헤드라인이 비어 있다.
  porosity 예측 · 저항망 σ · Stage E 파괴 보정 주제의 신규 논문은 **경보**로 올릴 것.
- 축 B: **C-12 가 아직 계산도 안 됐다**(발송 전). 바인더 흡착 DFT · PTFE/폴리머 계면 ·
  NCM 표면 흡착 주제는 **경보**.
