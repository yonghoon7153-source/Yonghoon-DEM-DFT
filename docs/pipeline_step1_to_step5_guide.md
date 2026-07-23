# 황화물 전고체전지 양극 통합 시뮬레이션 — STEP1 → STEP5 설명서
### (처음 보시는 분을 위한 자립형 안내서, 2026-07-23)

> **한 문단 요약.** 우리는 황화물 고체전해질(LPSCl) + 단결정/코팅 NCM 양극을 **냉간압축(≈300 MPa)**
> 한 복합 양극을, 입자 하나하나의 수준에서 **디지털로 재현**하고 그로부터 **성능(전도도·용량·분극)**
> 과 **수명(사이클 열화)**을 예측한다.  다섯 단계로 흐른다: **① 입자를 쌓고(DEM) → ② 눌러서
> 압밀시키고(MPM) → ③ 그 미세구조에서 전자·이온·열 전도를 푼 뒤(복셀 Kirchhoff) → ④ 충·방전
> 전기화학을 돌리고(STEP4) → ⑤ 사이클이 지나며 어떻게 열화하는지(R_int(N))를 분해한다.**  핵심
> 원칙은 **"각 물리를 그 물리에 맞는 도구로만"** 풀고(frame[5] 상보 분업), 각 도구를 **DEM↔MPM끼리가
> 아니라 실험에 독립적으로 보정**하는 것이다.  일치하면 교차검증, 어긋나면 그 차이가 곧 정량화된
> 모델 한계 — 둘 다 결과이지 실패가 아니다.

---

## 0. 왜 이걸 만드나 (문제 정의)

**전고체전지(ASSB)**의 양극은 액체 전해질이 없다.  대신 **고체전해질(SE) 분말**과 **활물질(AM,
여기선 NCM 양극재)** 분말을 섞어 **눌러 굳힌** 복합체다.  성능을 가르는 것은 화학식이 아니라
**미세구조** — 입자들이 얼마나 조밀하게 쌓였는지, 어디서 서로 닿았는지, 그 접촉을 통해 이온·전자가
어떻게 흐르는지다.  실험만으로는 이 내부를 직접 못 본다(SEM은 단면 한 장, EIS는 전체 저항 한 숫자).

→ 그래서 **입자 해상도 시뮬레이션**으로 내부를 복원한다.  입력은 설계 숫자(조성비, 입경, 압력),
출력은 실험이 못 주는 것들: **접촉망, 전도 경로, 응력장, 소성 변형, 그리고 이들이 사이클과 함께
어떻게 무너지는가.**

---

## 1. 핵심 철학 — frame[5] 상보 모델 분업 (이걸 먼저 이해해야 나머지가 보임)

이 프로젝트에서 가장 중요한 개념 하나만 꼽으면 **"모델을 서로 맞추지 않는다"**이다.

- **DEM**(이산요소법)은 입자를 **영원히 단단한 구(rigid sphere)**로 본다.  잘하는 것: **접촉망,
  재배열, 패킹(쌓임), 전도 경로**.  못하는 것: 입자가 **눌려 찌그러지는 소성 변형**(강체라 모양이 안 변함).
- **MPM**(물질점법)은 재료를 **연속체**로 본다.  잘하는 것: **소성 변형, 형상 변화, 빈틈 메움 흐름,
  응력·변형장**.  못하는 것: **이산 접촉망**(연속체라 "이 입자와 저 입자가 점에서 닿았다"를 표현 못 함).

두 모델은 **현실의 서로 다른 절반**을 본다.  그래서 —

> **DEM과 MPM을 서로 보정하면 안 된다(순환논리).  각각을 실험에 독립적으로 맞춘 뒤 비교한다.
> 일치 = 교차검증 증거.  불일치 = 정량화된 모델 한계(정보, 실패가 아님).**

| 물리 | 담당 도구 | 이유 |
|---|---|---|
| 접촉망, 전도(σ_ion/σ_e/σ_thermal), 퍼콜레이션, 힘사슬, Furnas 패킹 dip | **DEM** | 이산 접촉 = 강체구의 강점 |
| 소성 형상변화(SEM 모폴로지), 빈틈-메움 흐름, 응력·변형장, 사이클 형상변화 | **MPM** | 연속체 소성 = 유일 표현 |
| 다공도, 두께, 기계적 coverage, 조성→다공도 트렌드 | **둘 다**(독립 교차검증) | 겹치는 영역 = 신뢰도 측정자 |

이 원칙이 STEP2(MPM)와 STEP3(DEM 전도)가 **왜 분리돼 있는지**, STEP5에서 **왜 "MPM이 사이클을
다 돌린다"가 불가능한지**를 설명한다.

---

## 2. 파이프라인 한눈에

```mermaid
flowchart TD
    A["설계 입력<br/>(조성 AM:SE, 입경 P/S, 압력, 두께)"] --> S1
    S1["STEP1 · DEM 패킹<br/>LIGGGHTS · 강체구 + hooke/hysteresis<br/>→ 압밀 베드 atoms.csv"] --> S2
    S1 -.전도.-> S3
    S2["STEP2 · MPM 압밀 / payload<br/>MLS-MPM · von Mises J2 소성<br/>→ 형상·void·응력, se_dump"] --> S3
    S3["STEP3 · 복셀 전도<br/>Kirchhoff + Holm + Stage-E<br/>→ σ_e / σ_ion / σ_thermal + current-focusing"] --> S4
    S3 --> ML["ML 예측기<br/>설계→σ triad<br/>(LOOCV 0.90~0.98)"]
    S4["STEP4 · 전기화학 동역학<br/>BV + 구형확산 · OCP · R_int<br/>→ 충·방전곡선, 분극, 반응분포"] --> S5
    S5["STEP5 · 사이클 열화<br/>R_int(N) = 접촉(ledger) + 화학(CEI √N) + OTHER<br/>→ 용량 fade 예측"]
    EXP["실험 앵커<br/>Minnmann · Cronau · Yun · Kim · Park"] -.독립 보정.-> S1 & S2 & S3 & S4 & S5
```

각 STEP은 **앞 단계의 출력을 입력으로** 받고, **실험에 독립적으로 보정**된다(점선).

---

## 3. STEP1 — DEM 패킹 (입자를 쌓는다)

**한 줄**: 설계 숫자대로 AM·SE 분말을 가상 용기에 붓고 **300 MPa로 눌러** 실제와 같은 다공도의
**압밀 베드**를 만든다.

- **도구/물리**: LIGGGHTS(오픈소스 DEM).  입자는 **강체구**, 접촉은 **hooke/hysteresis**(선형-Hertz
  근사) 스프링.  압력판이 위에서 눌러 목표 압력까지 압밀.
- **핵심 트릭 — 18× 연화(softening)**: SE의 실제 탄성계수는 E≈24 GPa인데, 시뮬레이션에선
  **E_eff=1.35 GPa로 18배 물렁하게** 쓴다.  왜? 강체구 DEM은 입자가 안 찌그러지므로(소성 없음),
  실제 분말의 **재배열·입계 미끄러짐·미세파쇄** 같은 "빠진 치밀화 기전"을 **연화된 탄성계수 하나로
  뭉뚱그려** 넣는다.  이 18×는 자의적이지 않다 — 순수-SE에서 **Cronau 중첩 11~12%**, 독립적인
  MPM 치밀화, 셋이 모두 같은 연화를 요구한다(삼중 교차검증).
- **입력**: 조성(AM:SE 무게비, 예 82:18), P:S 비(대입자 poly : 소입자 SC), 입경(12:4:1 등), 압력, 두께.
- **출력**: 압밀 베드 `atoms.csv`(id, type, x, y, z, radius) — 모든 후속 단계의 골격.
- **핵심 수식(검증)**: **Heckel** ln(1/(1−D)) = K·P + A, 우리 DEM은 R²=0.965, 항복압 **P_y=138 MPa**.
- **실험 앵커**: 다공도 ≈13~16% @300 MPa(Minnmann 냉간압축), 순수-SE Cronau 중첩 11~12%.
- **한계**: 입자 모양은 절대 안 변한다(강체).  "치밀화"는 재배열+중첩이지 형상 소성이 아니다 →
  형상은 STEP2(MPM)가 담당.

---

## 4. STEP2 — MPM 압밀 / payload (눌러서 찌그러뜨린다)

**한 줄**: STEP1의 **실제 AM 골격을 고정**한 채, 그 사이의 **SE만 연속체 소성으로 눌러** 실제
형상변화·빈틈메움·응력장을 계산한다.

- **도구/물리**: MLS-MPM(Taichi GPU), **von Mises J2 소성**(부피보존 소성 흐름 = 실제 분말 치밀화).
- **생산 파라미터(3D)**: E_SE=1.53 GPa, **ν_SE=0.49**(벌크는 실제처럼 단단, 전단만 물렁 = 부피보존
  입상 흐름), σ_y=0.30 GPa, 목표 0.30 GPa, **readout = wallP**(압력판 반력 = 해상도-불변, 진짜 경계조건).
- **DEM→MPM 스캐폴드 결합**(핵심 아이디어): AM 패킹은 DEM의 강점, SE 형상은 MPM의 강점 →
  **DEM의 실제 AM 위치를 격자에 고정(frozen)**하고 **SE만 MPM 재료**로 채워 소성 압밀.  AM을 왜
  안 풀어주나: ① 이산 강체 하중분담은 연속체가 표현 못 함, ② 움직이면 힘사슬 과-차폐(36~41% 비물리),
  ③ AM-as-material은 CFL/OOM 폭발, ④ DEM AM은 이미 검증된 300 MPa 평형 골격.
- **입력**: STEP1 스캐폴드 CSV(am_scaffold, se_scaffold), 압력, 격자 해상도.
- **출력**: 압밀된 SE 형상(se_dump), 누적 소성변형장, 응력장, `mpm_payload.json`(웹뷰어용).
- **실험 앵커**: 순수-SE **Minnmann 10% @300 MPa**(σ_y 스윕 0.30→10.0% 재현), SEM 모폴로지(코어보존+
  경계평탄), 복합체 다공도 **16.7% vs LIGGGHTS 15.6%**(두 독립모델 ±1%p 일치 = frame[4] 교차검증).
- **한계**: 연속체라 **이산 접촉망·Furnas dip은 못 만든다**(그건 STEP3/DEM 소유).  MPM이 소유하는 것 =
  **형상·다공도 증분·응력장**.

---

## 5. STEP3 — 복셀 전도 (전자·이온·열이 어떻게 흐르나)

**한 줄**: 압밀된 미세구조를 **복셀(3D 픽셀)**로 만들고, 접촉망 위에서 **Kirchhoff 회로**를 풀어
**전자·이온·열 전도도 3종**과 **전류 집중**을 낸다.

- **도구/물리**: `network_conductivity.py`, `step3_sigma.py`.  각 입자=노드, 접촉=저항.
  **Holm 1967 수축저항** R = 1/(2σ·r_c)(접촉 반경 r_c로 좁아지는 목), Kirchhoff Σ(φ_i−φ_j)/R = 0.
- **Stage-E 소성 접촉면적 보정**: 강체구의 탄성 중첩(πR·δ)은 소성 접촉을 과대평가 → **Tabor(F/H)·
  부피 재유도**로 실제 소성 접촉면적을 다시 구한다(5-영역 분해, 과압축은 min(caps) 천장으로 차단).
- **3종 전도도(triad)**:
  - **σ_ion**(이온): SE 골격을 타고. 앵커 = Cronau 단결정 3.0 mS/cm × Cronau(r_SE) 결정립 보정.
  - **σ_e**(전자): AM(NCM) 골격을 타고. 단결정/다결정 입계로 나뉨(Trevisanello 방향).
  - **σ_thermal**(열): AM-AM/AM-SE/SE-SE 다경로 병렬.
- **current-focusing**(전류 집중): 좁은 목에서 전류밀도가 평균의 수십 배로 치솟는 지점(p99.8 상위
  0.2%) — 열화·발열의 씨앗.  공동 컬러바는 **케이스-최대(안 잘림)** 천장으로 표시.
- **coverage**(피복률): AM 표면 중 SE가 덮은 비율. Hertz(접촉) ~18% vs **Tabor(소성 퍼짐) ~52%**.
- **입력**: STEP2 payload / STEP1 베드.  **출력**: σ_e/σ_ion/σ_thermal(mS/cm), τ(굴곡도),
  퍼콜레이션 분율, current-focusing 맵, coverage.
- **실험 앵커**: **Bazzoun 2026**(같은 LPSCl+NCM+LIGGGHTS+RNM) σ_eff,ion EIS 0.065~0.137 mS/cm,
  압력-의존 σ-vs-P(400 MPa 포화).
- **한계**: 접촉망은 있으나 시간전개(충방전)는 없음 → STEP4로.

---

## 6. STEP4 — 전기화학 동역학 (충·방전을 돌린다)

**한 줄**: STEP3의 전도망 위에서 **실제 충·방전(정전류/CV, 사이클)**을 시간전개해 **전압곡선·분극·
반응 분포**를 낸다.

- **도구/물리**: `step4_dyn.py`.  **Butler-Volmer 반응 kinetics** + **구형 입자 확산**(고체 내 Li 확산)
  + STEP3 전도망(옴 강하).  OCP(열역학 전압) = **NMC811 Chen 2020** 실측 테이블.
- **핵심 파라미터**: 방전창 x0=0.264 ~ **x100=0.9084**(NMC811 vs-Li GITT 실측), R_int 직렬(풀셀 축),
  SC/poly 크기-의존 확산계수 D_s.
- **수치 안정화(near-null-B AMG)**: 저율(0.1C/0.2C)에서 계가 near-singular → 일반 풀개가 실패.
  **near-null 벡터 기반 대수다중격자 전처리기**가 유일하게 수렴(8.3e-14, 100 it).
- **대표 결과**: 2C CCCV 충전 완주(CC끝 81.5→CV후 89.6%), ΔV 분해(옴 4.5 + kinetics 4.8 mV) —
  방전(7.9 mV)과 대칭 = 수송-기원 양방향 확인.  σ_e ↑(SDCP)이 rate-capability를 개선.
- **입력**: STEP3 전도 그리드(step4_grid.npz), OCP/파라미터 앵커.  **출력**: 전압-시간 곡선, 과전압
  분해, 반응전류 분포, 겉보기 R_int.
- **실험 앵커**: NMC811 OCP(Chen 2020), PyBaMM/COMSOL 방정식-수준 패리티(수치 패리티 런 대기).
- **한계**: v1은 저율 선형/독립 스텝.  시간축 완화·사이클 chaining은 STEP5 방향.

---

## 7. STEP5 — 사이클 열화 (수명: R_int이 사이클과 함께 어떻게 자라나)

**한 줄**: pristine 전극(STEP1–4)이 **N 사이클 후 계면저항 R_int(N)**이 얼마나 자라는지를,
**"어느 물리가 얼마나"** 정직하게 **분해**해 예측한다.

가장 중요한 교훈: **"MPM이 사이클을 다 돌린다"는 물리적으로 불가능**(아래 ⚠).  대신 각 열화 기전을
제 도구에 맡기고 **합산**한다 —

> **총 R_int(N) = R_접촉(N) + R_화학(N) + R_OTHER(N)**

| 조각 | 물리 | 도구 | 총 fade 몫 | 앵커 |
|---|---|---|---|---|
| **A-1** | 충전상태 형상변화(SC 수축 −5.1% Kondrakov, poly 팽창) | MPM `--cycle-deform` | 형상 앵커(가역) | GPU 검증(coverage −19%) |
| **A-3** | 영구 접촉파단 | ledger(Bucci δcr CZM, recontact=forbid) | **~2%**(하한) | mono 1.05× vs bimodal 1.51× |
| **B-1** | 화학 계면상(CEI) 성장 | STEP4 interphase / `b1_chem_fade` | **~98% 지배**(bare) | √N Park2023 · 크기 Yun/Kim |
| **OTHER** | 골격재배열·SE 분해·Li쪽 | (모델 밖) | 코팅셀서 지배 | 실험값 대기 |

- **핵심 발견**: 접촉-기계 열화(ledger)는 총 fade의 **~2%뿐**.  진짜 열화는 **화학 CEI(B-1)가 지배**.
  (ledger R_ct 1.1× vs 실험 총 R_int 3.8~6.1×@1000cyc.)  → **MPM/ledger = 방향·기전, 크기·모양 =
  화학 + 실험.**
- **정직한 shape**: CEI 성장은 **√N**(확산제한 Wagner) — **Park 2023**이 코팅셀서 "계면 R vs √t 선형"을
  확인(문헌앵커).  ★단, **magnitude(크기)는 실험 끝점에 앵커**하고 **shape(모양)는 ASSUMED** — 끝점
  하나론 √N/선형 구별 불가.  그래서 `fit_rint_curve.py`로 **실험 곡선(≥4 N점)이 들어오면 shape을
  확증/기각**한다(검증 게이트).
- **코팅 인식**(요즘 양극재): nm 코팅(LNO 등)은 CEI를 **13~20× 억제**(Kim 2025) → 화학 몫이 작아지고
  잔여는 **OTHER(모델 밖)**로 이동 → `b1_chem_fade --chem-x`로 **화학 몫을 열어둠**(하드코딩 아님).
- **입력**: ledger 접촉 궤적 + 실험 총 R_int 끝점(×@N).  **출력**: 총 R_int(N) 분해 곡선.
- **실험 앵커**: **Yun 2023**(우리 랩, bare SC-NMC R_ct 341.7→982.3 = 2.87×@100), **Kim 2025**(LNO
  13~20× 억제), **Payandeh 2023**(코팅 93%@200cyc).
- **⚠ 기각된 것(정직화 과정, 적대리뷰가 코딩 전 차단)**:
  - **v2 반복사이클 MPM**: rigid 핀-마스크는 방전 스프링백 불가 · 부피보존 J2는 영구 접촉손실 금지
    (void를 도로 메움) · 재변형이 sub-voxel → **물리적으로 불가능**.
  - **reflow=0.34 캘리브**: 지표 착시(ledger Hertz-면적 30% vs MPM 복셀-coverage 19% = 정의 차이지
    재유동 아님)로 **철회**.
- **실행 도구**: `cycle_contact_ledger.py`(접촉 fade) · `b1_chem_fade.py`(화학 N-전개) ·
  **`fit_rint_curve.py`(실험 shape 검증)** · **webapp `/step5`(인터랙티브 fade(N) 패널)**.

---

## 8. 검증·실험 앵커 총괄표

| 단계 | 무엇을 검증 | 실험/문헌 앵커 | 우리 값 |
|---|---|---|---|
| STEP1 | 다공도, 압밀곡선 | Minnmann 냉간압축 10% @300 · Heckel | 13~16%, P_y=138 MPa, R²0.965 |
| STEP1 | 순수-SE 소성 floor | Cronau 중첩 5~10% | 11~12% |
| STEP2 | 순수-SE 다공도 | Minnmann 10% @300 | σ_y0.30→10.0% |
| STEP2 | 복합 다공도·두께 | LIGGGHTS(DEM 독립) | 16.7 vs 15.6%(±1%p) |
| STEP2 | 모폴로지 | SEM(코어보존+경계평탄) | 정성 일치 |
| STEP3 | σ_ion 절대값·압력의존 | Bazzoun 2026 EIS · Varkey 2026 | 0.065~0.137 mS/cm 범위 |
| STEP3 | σ_grain 결정립 | Cronau 2022 단결정 3.0 | Cronau(r_SE) 보정 |
| STEP4 | OCP·rate | Chen 2020 NMC811 · PyBaMM | 패리티 런 대기 |
| STEP5 | 열화 크기 | Yun 2023 R_ct 2.87×@100 | 실험 끝점 앵커 |
| STEP5 | 열화 모양 | Park 2023 √t 선형(코팅) | √N 기본(fit_rint_curve 검증) |
| STEP5 | 코팅 억제 | Kim 2025 LNO 13~20× | --chem-x 열어둠 |

ML 예측기(설계→σ triad): **σ_ionic LOOCV 0.975 · σ_e 0.953 · σ_thermal 0.90**.

---

## 9. 무엇을 믿고, 무엇을 안 믿나 (정직한 한계)

**믿을 수 있다(실험 교차검증됨)**: 다공도·두께(DEM↔MPM ±1%p), 순수-SE 소성 floor(Cronau/Minnmann),
σ_ion 트렌드·압력의존(Bazzoun), 형상 모폴로지(SEM), Heckel 압밀곡선.

**방향·기전은 믿고, 절대 크기는 실험 앵커에 맡긴다**: STEP5 열화(접촉-기계 몫 ~2%는 하한, 화학·OTHER
크기는 실험), current-focusing 상대비교, 복합 다공도 절대값(패킹-한계, de Larrard/DEM에 맡김).

**모델 밖(OTHER)**: 골격 재배열의 이산 성분, SE 화학분해, Li 음극쪽 — 실험값이 들어오면 채움.

**절대 안 하는 것**: DEM↔MPM 상호보정(순환논리), ASSUMED를 검증된 것으로 표기, 문헌값 날조.
provenance 라벨(measured / assumed / ASSUMED-FORM / literature-anchored)을 항상 붙인다.

---

## 10. 어디서 실행하나 (실무 지도)

| 하고 싶은 것 | 도구 / 위치 |
|---|---|
| STEP1 DEM 패킹 | LIGGGHTS 입력 → 압밀 베드 atoms.csv |
| STEP2 MPM 압밀(GPU) | `scripts/mpm3d_compaction.py`(킷: `mpm_input_from_case.py` → run_mpm.sh) |
| STEP3 전도 σ triad | `scripts/network_conductivity.py`, `step3_sigma.py`(payload에 자동) |
| STEP4 충·방전 | `scripts/step4_dyn.py`(킷: step4_only.sh) |
| STEP5 접촉 fade | `scripts/cycle_contact_ledger.py` |
| STEP5 화학 N-전개 | `scripts/b1_chem_fade.py`(--chem-x 코팅) |
| STEP5 실험 shape 검증 | `scripts/fit_rint_curve.py --csv/--points` |
| STEP5 인터랙티브 패널 | **webapp `/step5`** (슬라이더 + 실시간 분해도) |
| MPM 3D 뷰어 | webapp `/mpm-lab` |
| 설계→σ ML 예측 | webapp `/predictor` |

킷 = 웹앱이 케이스별로 zip 산출(스캐폴드 CSV + run_mpm.sh + step4 + A-1 앵커) → GPU(v100)에서 실행.

---

## 11. 용어집 (처음 보는 분용)

- **DEM (이산요소법)**: 입자 하나하나를 강체구로 두고 접촉힘으로 운동을 푸는 방법.
- **MPM (물질점법)**: 재료를 연속체로 두되 "물질점"이 격자 위를 움직이며 소성 변형을 푸는 방법.
- **AM / SE**: 활물질(양극재, NCM) / 고체전해질(LPSCl).  P/S = 대입자(poly, 다결정) / 소입자(SC, 단결정).
- **다공도(porosity)**: 빈 공간 비율.  낮을수록 조밀.  냉간압축 목표 ~10~16%.
- **Heckel / P_y**: 압밀 압력-밀도 관계식.  P_y = 항복압(재배열→소성 전이).
- **Kirchhoff / Holm 수축저항**: 접촉망을 전기회로로 풀 때의 회로법칙 / 좁은 접촉목의 저항 이론(1967).
- **퍼콜레이션(percolation)**: 접촉이 한쪽 끝에서 반대쪽 끝까지 **연결**되어 전류가 통하는가.
- **굴곡도(tortuosity, τ)**: 이온이 돌아가는 정도.  σ_eff = σ_grain·φ/τ².
- **coverage(피복률)**: AM 표면이 SE로 덮인 비율(전자-이온 경계).
- **current-focusing(전류 집중)**: 좁은 목에서 전류밀도가 평균의 수십 배 → 열화 씨앗.
- **Butler-Volmer**: 전극 반응속도-과전압 관계식(전기화학 kinetics).
- **OCP**: 개회로전압(열역학 평형 전압, SOC의 함수).
- **R_int / R_ct**: 계면 총저항 / 전하이동 저항.  EIS로 측정.  단위 Ω·cm²(면적기준).
- **CEI**: 양극-전해질 계면상(cathode-electrolyte interphase) — 사이클마다 자라 저항 증가.
- **√N Wagner 성장**: 확산제한 계면상 두께가 √시간(∝√사이클)로 자란다 → 저항 ∝ √N.
- **frame[5]**: 이 프로젝트의 상보 모델 분업 철학(§1).
- **ledger**: 사이클마다 접촉 개폐를 장부처럼 추적하는 후처리 도구(A-3).
- **provenance 라벨**: 값의 출처 표기(measured/assumed/ASSUMED-FORM/literature-anchored).

---

## 12. 한 페이지 정리 (외워둘 것)

1. **입자→압밀→전도→전기화학→열화**, 다섯 단계가 순차로 흐른다.
2. **DEM = 전도(transport), MPM = 역학(mechanics)** — **서로 안 맞추고 각각 실험에 맞춘다**.
3. STEP2의 18× 연화·MPM 스캐폴드는 **자의적이 아니라 삼중 교차검증**된 물리 대리.
4. STEP5 열화는 **접촉(~2%) + 화학 CEI(~98%, √N) + OTHER**로 **정직 분해** — 크기는 실험 앵커,
   모양은 실험 곡선으로 검증(fit_rint_curve).
5. **일치=교차검증, 불일치=정량화된 한계.**  ASSUMED를 검증된 것으로 위장하지 않는다.

*(상세 근거·수치는 각 단계 전용 문서: `docs/mpm3d_calibration.md`, `docs/step4_assb_window_review.md`,
`docs/step5_cycle_degradation.md`, `docs/manuscript_sdcp_sigma_e_mechanism.md`,
`docs/lit_bazzoun2026_dem_fem_rnm.md`, `docs/defense_review_20260720.md`.)*
