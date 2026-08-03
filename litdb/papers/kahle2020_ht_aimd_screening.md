# High-throughput computational screening for solid-state Li-ion conductors — Kahle/Marcolongo/Marzari (Energy Environ. Sci. 2020)

> slug `kahle2020_ht_aimd_screening` · DOI `10.1039/c9ee02457c` · type `DFT + pinball-MD(HT surrogate) + FPMD(BOMD) 스크리닝 (자체 실험 0)` · PDF `888fc044-41.…pdf`(본문 21 pp) + `8e473f28-41._Sup…pdf`(SI 35 pp: §1–6·Fig S1–S121·Table S1–S5) (inbox #41→#46) · digested `2026-07-28` · status ✅
> elements: Li, S, P, Cl, Br, I, F, O, N, Se, Ge, Ta, Ga, Cs, Re, Ti
> methods: DFT, AIMD, MD
> **저자**: Leonid Kahle*, Aris Marcolongo(‡현 IBM Research-Zurich), **Nicola Marzari** (EPFL THEOS·NCCR MARVEL) · EES 2020, **13**, 928–948 · Received 2019-07-31 / Accepted 2020-01-08 / Published 2020-01-10 · **첫 페이지 실물 확인 완료**(과제 메모 서지와 일치) · 데이터: Materials Cloud Archive **DOI 10.24435/materialscloud:2019.0077/v1** · 도구: AiiDA·SAMOS(github lekah/samos)·supercellor(github lekah/supercellor)

---

## 0. 이 digest를 읽는 법 (우리 캠페인에서의 위치) ★★
**"실험 구조 저장소(ICSD+COD) 전수를 MD로 스크리닝한다"는 문제를 *방법 규율*로 푼 원전**이다. 두 겹으로 읽는다:
1. **깔때기 논문으로**: [Sendek17](`sendek2017_ml_screening_12k_conductors.md`, ML 분류기)·[Xiao2019](`xiao2019_cathode_coating_screening.md`, 열역학 게이트)와 나란한 **3대 HT 스크리닝 계보의 "물리 시뮬레이션(MD)" 축** — 서술자/ML/정적 게이트가 아니라 **동역학 자체(확산계수)를 스크리닝 변수로** 쓴 유일한 대규모 사례(pinball 7.6 μs + FPMD 45 ns).
2. **MD 통계 규율 논문으로 (우리 대조 핵심)**: MSD 창을 **데이터로 검증**(5/10/20/30 vs 40 ps)·블록 분산 오차·**자동 수렴 워크플로**(err(D)<1e-8 cm²/s or <5%)·1/T-등간격 4온도·**Bayesian Ea 오차 전파**·검출 하한(1e-8) 명문화 — 우리 MLIP-MD 규율(MSD 2–50 ps 고정·3-T·멀티시드·절대 σ 비인용)과 항목별 정면 대조가 가능한 거의 유일한 문헌 (§5·§10).
3. **경고 사례로**: pinball(host 동결 surrogate)은 **정량 D 재현에 실패**(Fig 15 산포)했으나 **랭킹 분류기로는 유효**(top-quartile 71%) — "surrogate는 깔때기용, 물성값은 상위 이론으로"의 정직한 자기 검증. 우리 UMA(전 원자 MLIP)와 근사 철학이 정반대다(§4·§10).
⚠ argyrodite 블라인드 스팟: **부분점유(partial occupancy) 구조를 입구에서 전부 제외** → Li₆PS₅Cl/Br(4a/4d 무질서=부분점유로 기록)는 깔때기에 **아예 못 들어왔고**, 질서 배열인 Li₆PS₅I만 살아남아 "못 푼 잠재 후보"로 남았다(§6c·§10). 우리 disorder-ensemble 파이프라인이 정확히 이 공백을 메운다.

## 0.5 처음 읽는 사람을 위한 배경 (이 논문이 전제하는 것들)

**pinball model 이 뭔가 — 이름이 전부다**
격자(호스트)를 **통째로 얼려 놓고** Li 만 튕겨 다니게 하는 값싼 MD 다. 핀볼 기계처럼
공(Li)만 움직이고 판(골격)은 고정이다. 호스트 자유도를 없애니 계산이 수십 배 빨라진다.
대신 **골격이 Li 를 따라 숨쉬는 효과(격자 이완)를 잃는다** — 그게 아래 한계의 원인이다.

**"실패했는데 성공한" 결과를 읽는 법 ★**
pinball 은 **확산계수 D 의 절대값 재현에 실패했다**(Fig 15 산포가 크다). 그런데도 이 논문의
깔때기는 작동했다 — 상위 사분위를 71% 맞췄기 때문이다.
> **surrogate 는 정량이 아니라 순위를 맞히면 된다.**
> 깔때기 1단의 임무는 "정확한 값" 이 아니라 "버릴 것을 안 버리기" 다.
이 구분을 못 하면 "MLIP 로 D 를 계산했다" 같은 문장을 쓰게 된다. 우리 규율
("MLIP 절대 전도도 인용 금지, 비율만 다중시드 판정") 의 외부 근거가 바로 이것이다.

**MSD 창(fit window)이 왜 논문거리가 되나**
MSD(평균제곱변위)를 시간에 대해 직선 맞춤해서 D 를 얻는데, **어느 구간을 맞추느냐**로 값이
몇 배씩 달라진다. 짧은 시간엔 Li 가 우리(cage) 안에서 진동만 하고(sub-diffusive), 충분히
길어야 진짜 확산 구간이 나온다. 이 논문은 그 창을 감으로 고르지 않고 **데이터로 검증**
(5/10/20/30 vs 40 ps)하고, 블록 분산으로 오차막대를 붙이고, 수렴 기준을 자동화했다.
→ 우리 확산영역 게이트(`tools/ionic/msd_diffusive_check.py`, β = d log MSD / d log t)가
   같은 문제에 대한 우리 쪽 답이다.

**ICSD/COD 가 뭔가**
실험으로 구조가 결정된 결정들을 모아 둔 데이터베이스다. "실제로 존재가 확인된 물질" 만
대상으로 한다는 뜻이라, 계산으로 만들어낸 가상 구조를 다루는 CSP 논문
([Kim2025](`kim2025_csp_metastable_edge_sharing_sse.md`))과 출발점이 정반대다.

---

## 1. 한 줄 요약
ICSD+COD의 Li-함유 실험 구조 전수(유효 7,472 → 유니크 4,963)를 원소/결합 필터(1,362) → PBE 절연체 판정(1,016) → vc-relax(971) → **pinball model**(DFT 힘으로 피팅한 Li-only frozen-host surrogate, DFT 대비 ~4자릿수 저렴)로 1000 K 확산계수 스크리닝(796종 완주, 총 7.6 μs) → 상위 200에서 기지 전도체·불안정 구조를 제외한 **132종을 FPMD**(BOMD, 총 45 ns, 1000→750/600/500 K)로 정밀 판정하여 — **신규 fast-ion conductor 5종**(Li₅Cl₃O, Li₂CsI₃, LiGaI₄, LiGaBr₃, Li₇TaO₆; Ea 0.19–0.35 eV, LGPS 0.14 급) + **잠재 후보 40종** + **비전도 70종**(정직한 음성) + 기지 전도체 39종 재발견(검증)을 보고한다.

## 2. 메타
| 항목 | 내용 |
|---|---|
| 저자/기관 | Kahle·Marcolongo·Marzari — EPFL THEOS / NCCR MARVEL (스위스; Marcolongo는 게재 시점 IBM Zurich) |
| 저널 | Energy Environ. Sci. 2020, 13, 928–948 (2020-01-10 online) |
| DOI | 10.1039/c9ee02457c |
| 유형 | 순수 계산 HT 스크리닝: DFT(QE) 절연체 판정 + vc-relax + **pinball-MD**(자체 개발 surrogate, 원 논문 = Kahle/Marcolongo/Marzari PRM 2018, 2, 065405 [ref 107]) + **FPMD**(BOMD). 자체 실험 0 |
| 풀 | **ICSD 8,627 + COD 7,228 entries**(Li-함유 전수, 2019 스냅샷) |
| 산출 | 그룹 A(fast-ion) 5종+LGPS / B(potential) 40종 / C(non-diffusive) 70종 / D(pinball-only) 15종 + 기지 39종 |
| 인프라 | **AiiDA**(전 계산 DAG provenance, Fig 2) · SAMOS(MSD/밀도 분석) · supercellor(최소 슈퍼셀) · Materials Cloud 공개 |
| 핵심 질문 | "서술자도 force-field도 못 믿고 FPMD는 너무 비싸다 — **DFT 정확도에 근접하면서 수천 종을 돌릴 수 있는 MD 스크리닝**이 가능한가?" |
| 방법 스코프 결정(명문) | ESW(전기화학 창)는 **의도적으로 계산 안 함** — "LGPS도 interphase로 안정화되어 쓰인다 → 창 폭은 필요조건 아님"(p929). 기계 modulus 기준도 **채택 안 함** — "dendrite 억제는 결함 지배, 스크리닝 기준으로 이해 안 됨"(p930). → 깔때기 = 절연성 + 이온 확산 2축만 |

## 3. 깔때기 (Fig 1 + §3) — 전체 수치 ★★★
```
ICSD 8,627 + COD 7,228 (Li-함유 전수)                     15,855 entries
 └─ 부분점유 없음 + attached-H 없음                        3,956 + 3,777 = 7,733
 └─ CIF 파싱 성공(pymatgen; 261 실패)                      7,472 valid
 └─ 중복 제거(pymatgen StructureMatcher + CMPZ)            4,963 unique
[조성·기하 필터, Appendix A.2–A.3]
 └─ 음이온 {N,O,F,P,S,Cl,Se,Br,I}만·H 제외·3d TM(V–Cu) 제외·
    희귀/방사성/Z>Hg 제외·전하균형(Li가 전자 받을 음이온 존재)·
    결합거리 필터(분자성 할로겐·시아나이드·과산화물 등)        1,362
[전자구조 게이트, A.4]
 └─ PBE 절연체(전도대 최저준위 점유 < 1e-3 e)              1,016  (≈ abstract "~900"의 모집단)
[기하 이완, A.5]
 └─ vc-relax 수렴 성공                                       971  (부피 히스토그램 피크 +4%, Fig 3)
[pinball 피팅, A.7]
 └─ α₁·α₂·β₁ 회귀 성공 916 → r² 판정 통과                    903
[pinball-MD 확산 워크플로, §2.5·A.8]
 └─ D(1000 K) 수렴 완주 (총 7.6 μs)                          796  (12% 실패: 등에너지 드리프트·D 미수렴)
[FPMD 선별]
 └─ pinball-D 상위 200 − 기지 전도체 39 − 실험문헌상 불안정   132  → FPMD (총 45 ns)
[판정]
 └─ A: fast-ion (1000 K & 500 K 확산)                          5종 + LGPS(레퍼런스; supercell 7개)
 └─ B: potential (고온만 확산 or 저온 미해상)                 40종 (multi-T 19 + 1000 K-only 21)
 └─ C: non-diffusive (1000 K에서도 무확산)                    70종
 └─ D: FPMD 실패(SCF 발산 등) — pinball만 확산 확인           15종
```
- 산술 검증: A(5)+B(40) = **FPMD가 찾은 이온전도체 45종**; 45+기지 39 = 84종/796 후보. Abstract의 "~1400 unique materials / ~900 insulators / ~130 FPMD"는 각각 1,362/1,016(또는 903)/132의 라운딩.
- **⚠ 입구 필터의 대가**: "부분점유 제외"로 **무질서 argyrodite(LPSCl/LPSBr)·큐빅 가넷 LLZO(Li 부분점유)** 등이 구조적으로 배제됨 — 저자도 §3.5에서 "Li 자리만 부분점유인 구조가 추가로 645개(비-유니크) 있다"고 명시. 질서 구조인 Li₅La₃Ta₂O₁₂(ICSD 68252)·Li₆PS₅I만 통과.
- H 제외 이유가 흥미로움(A.2): "H는 Li보다 가벼워 Li 이동에 **끌려 움직일 것** → frozen-host 가정과 비양립"(pinball 미검증 영역).

## 3.5 대리모형(surrogate)이 무엇을 포기하는가

값싼 모형은 **무언가를 포기해서** 싸진다. 무엇을 포기했는지가 그 모형의 유효 범위를 정한다.
- **pinball** = 호스트 격자를 동결 → 포기한 것: **격자 이완**(Li 가 지나갈 때 골격이 벌어지는 효과).
  격자가 유연한 계에서는 확산을 과소평가하게 된다.
- **고전 force field** = 전자를 안 봄 → 포기한 것: 결합 재배열·산화상태 변화.
- **MLIP** = DFT 를 학습으로 흉내 → 포기한 것: **학습 영역 밖 외삽**. 밖에서는 조용히 틀린다.
읽을 때 질문 하나면 된다 — **"이 근사가 지운 물리가 내 계에서 중요한가?"**

---

## 4. Pinball model 정밀 해부 ★★★ (이 논문의 심장)

### 4a. 정의 — "Li만 움직이는, DFT 힘으로 보정한 정전+국소포텐셜 모델"
해밀토니언(eq 1):
```
H_P = Σ_p ½ M_p Ṙ_p² + α₁·E_N^{P–P} + α₂·E_N^{H–P} + β₁·Σ_p ∫ n_{R_H0}(r)·V_p^LOC(r) dr
```
- **pinball = Li 이온**(위치 R_p). E_N^{P–P} = pinball–pinball 유사핵(pseudopotential core) 정전기, E_N^{H–P} = pinball–host 정전기, 마지막 항 = **동결 전하밀도 n_{R_H0}(r)**(host 바닥상태에서 1회 계산)와 Li 국소 pseudopotential의 상호작용.
- 자유 파라미터는 **α₁, α₂, β₁ 단 3개** — 구조마다 DFT 힘에 선형 회귀로 피팅. (ML 포텐셜이 아니라 **물리항 3개짜리 보정 모델**임에 주의 — 우리 UMA 같은 학습 포텐셜과 범주가 다르다.)
- 이 논문은 **local pinball**: 원 모델(PRM 2018)의 비국소(core–동결파동함수) 항을 버림 — 정확도 약간↓, 대신 스케일링 **입방→제곱**.

### 4b. 두 가지 물리 근사 (감수한 오차)
1. **전하밀도 동결**: "Li는 이온성 계의 가전자 전하밀도를 거의 교란하지 않는다" → 밀도가 Li 순간 위치에 무의존.
2. **host 격자 동결**: Li 외 전 원자를 바닥상태 위치에 고정 — "강성(stiff) 계일수록 영향 작다"는 가정.
→ 결과적으로 **비용 ~4자릿수 절감**(Fig 17: 이온 스텝당 node-time pinball ~0.1–1 s vs DFT ~10²–10⁴ s). 절감분을 **통계에 재투자**(전 구조 D 수렴, 물질·온도당 1.5–18.4 ns)해서 총비용은 FPMD와 비슷해짐 — "같은 수를 FPMD로 돌리는 건 오늘날 컴퓨터로 불가능"(Appendix B).

### 4c. 피팅 절차 (A.7)
- 목표 **힘 성분 5,000개**: 예) LGPS Li₂₀Ge₂P₄S₂₄ = Li 20개 → 5000/(3·20) = **84 스냅샷**.
- 스냅샷 = BOMD가 아니라(그러면 스크리닝 의미 상실) **평형 위치에서 Li만 정규분포 σ=0.1 Å 변위** → 각 구성에 pinball 1회 + DFT 1회 → 힘만으로 α₁·α₂·β₁ 회귀. r² 나쁘면 탈락(916→903).
- 슈퍼셀 ≤500원자(초과분 탈락), d_inner = 8 Å.

### 4d. 검증 — 정량 실패, 랭킹 성공 (Fig 15 + p940) ★★
- **정량**: D_FPMD vs D_PB(1000 K) 산점(음이온별 색: S/Se·N/P·할로겐·O) — **"The diffusion coefficient from FPMD is not well reproduced by the pinball model"**(원문). 상관 빈약, 수 자릿수 산포.
- **랭킹(분류기)**: FPMD 대상 후보를 pinball-D 4분위로 나눠 "FPMD에서 D(1000 K)>1e-7 cm²/s일 확률"(success rate) 측정 → **top 71% / 2분위 36% / 3분위 33% / 4분위 21%** — 단조 감소 = "pinball 확산이 높을수록 FPMD에서 전도체일 확률이 체계적으로 높다". 기지 전도체를 빼고 계산했으므로 **하한**.
- **스크리닝 예측률**: (|A|+|B|+|E|)/(|A|+|B|+|C|+|E|) = (45+39)/(45+70+39) ≈ **54%** (E=39: pinball이 찾아낸 기지 전도체). 놓친 비율의 상한 = 4분위 21%(단조 가정 시 비스크리닝 구조가 전도체일 확률 <21%).
- **[Sendek] 교차 검증(p940)**: Sendek et al.(2019 Chem. Mater., ref 106)은 무작위 21종 중 3종(≈14%±~8%)이 전도체 → 만약 14%가 참 발생률이면 796 후보 중 진짜 전도체 ~111종 — Kahle이 찾은 84종과 "오차 내 정합", 놓친 건 ~27종 규모로 추정. (⚠ ref 45 = Sendek 2017 EES 스크리닝 본편, ref 106 = 2019 검증편 — 인용 시 구분.)
- **실패 원인 4중 자인(p939)**: ① local pinball 자체 부정확(비국소항 제거) ② 무작위 변위 스냅샷 피팅이 동역학 중 힘을 못 맞출 가능성 ③ **전하밀도 동결이 원형 전도체보다 큰 영향일 가능성** ④ **host 동결이 예상보다 큰 영향일 가능성** — "다음 스크리닝, 특히 조성 가변 스크리닝 전에 각각을 개별 검증해야".

### 4e. 우리 UMA와의 근사 계층 대조 (요약; 상세 §10)
| | pinball (Kahle) | UMA-s-1p1 (우리) |
|---|---|---|
| 움직이는 원자 | **Li만** (host 동결) | **전 원자** (PS₄ 회전·host 이완 포함) |
| 힘의 근원 | 물리항 3개 + 구조별 DFT-힘 회귀 | 범용 ML 포텐셜(omat 사전학습) |
| 오차의 성격 | 물리 근사(밀도·host 동결) — 계통적, 구조 의존 | 학습 오차 — PES 각인([KimMTP] functional 각인과 같은 결) |
| 검증 방식 | FPMD 대비 산점/분위(Fig 15) | EOS·Ea·실험 trend 대조(절대 σ 비인용) |
| 용도 판정 | **랭킹만 유효, 정량 무효**(저자 자인) | Ea·비율 신뢰, 절대 σ 비인용(우리 규율) |

## 4.5 MD 에서 D 를 뽑는 절차 (이 절의 전제)

1. **MSD** (평균제곱변위) = 시간 t 뒤에 이온이 평균적으로 얼마나 멀어졌나, 제곱으로 잰다.
2. 확산 중이면 MSD 가 시간에 **비례**한다 → 기울기/6 = 확산계수 D (3차원).
3. 그런데 **짧은 시간에는 비례하지 않는다** — 이온이 자기 자리(cage) 안에서 진동만 한다.
   그래서 **어느 구간을 직선 맞춤하느냐**가 D 를 몇 배씩 바꾼다. 이게 이 절 전체의 주제다.
4. **블록 평균** — 궤적을 여러 토막으로 잘라 각각 D 를 구하고 그 산포로 오차막대를 만든다.
   MD 는 통계라 값 하나만 내면 의미가 없다.
> 우리 확산영역 게이트는 여기에 판정 하나를 더한다 — **β = d log MSD / d log t 가 1 근처인가.**
> β 가 0.8 미만이면 아직 cage 안이라 그 구간에서 뽑은 D 는 인용할 수 없다.

---

## 5. MD 통계 규율 ★★★ (서베이 §3 행 수준 정밀)

### 5a. D 정의와 MSD 창 — 창을 데이터로 정당화 (ESI §2)
- **tracer D** (eq 2): D_tr = lim 1/6 d⟨MSD(t)⟩/dt |_{t=t'} — **총 MSD/6t(eq 1)가 아니라 기울기**. 이유: eq 1은 열진동(주기적 원자운동) 기여가 섞여 **비확산계에서 D를 과대**(Fig S2: 매우 확산적인 계는 두 방법 일치, 비확산계는 eq 1이 플래토 ~1e-7에 걸림).
- **창 수렴 검증(Fig S3)**: pinball 전 궤적(D>1e-8)에서 t'=5/10/20/30 ps 기울기를 40 ps 기울기와 비교 — **5 ps = ballistic/cage 운동이 남아 과대(위양성 다수) → 10 ps부터 위양성 급감 → "8–10 ps 창 = 통계 정확도(짧은 t일수록 표본↑)와 확산 영역 진입의 최적 절충"** 판정. → **pinball D = MSD 8–10 ps 선형회귀**.
- **FPMD D = 창 ≥20 ps**(Fig 5 캡션: 20–30 ps 구간 선형 피팅; SI §3: "pinball보다 긴 시간, 최소 20 ps").
- Li 확률밀도(eq 3): 궤적을 Gaussian σ=0.3 Å·10 pts/Å 격자로 스무딩, 등가면 0.1/0.01/0.001 Å⁻³(보라/파랑/시안) — SAMOS.

### 5b. 오차 산정과 자동 수렴 (A.8·A.9·SI §3)
- **오차 = 궤적을 독립 블록으로 쪼개 블록별 D의 분산 → mean ± standard error**(본문 "variance of the diffusion in the independent blocks"; 블록별 MSD가 SI 전 그림의 얇은 실선, 피팅이 점선).
- **pinball 온도 프로토콜(A.8)**: 소수 입자(Li만)라 열화 어려움 + 약결합 조화진동자 성격 → Nosé–Hoover 실패 경향 → **canonical 궤적(충돌빈도 1000 dt의 확률충돌 열욕)에서 3000 dt마다 스냅샷 8개 채취 → 8개 NVE 분기(각 50,000 dt) 병렬**(path-integral MD 기법 차용; Andersen형 열욕이 확산 억제할 위험 회피). dt=0.96 fs. 최소 4회(=**1.5 ns**)~최대 48회(=**18.4 ns**) 반복하며 매 회 **err(mean D) < 1×10⁻⁸ cm²/s 또는 < 5% of mean이면 워크플로 자동 종료**.
- **FPMD(A.9)**: BOMD·dt 1.45 fs·**SVR(stochastic velocity rescaling, Bussi) 열욕 τ=100 dt**(자체 QE 구현)·Γ-only·d_inner 6.5 Å. 연속 궤적을 같은 수렴 기준(1e-8 or 5%)까지 자동 연장 → **궤적 길이가 물질·온도마다 다름**(Table 1·S1: 43.6–726.4 ps).
- 물질·온도당 pinball ≥1.5 ns 확보 — **"통계를 산다"**는 설계 (총 7.6 μs vs FPMD 총 45 ns).

### 5c. 온도 프로토콜과 Ea
- 게이트 온도 **1000 K**(pinball·FPMD 공통) → 유의 확산 시 **750/600/500 K** 추가 = **1/T 등간격 4점**.
- **Ea = 최저온(500 K)에서도 확산이 해상될 때만** Arrhenius 선형 피팅 → 그룹 A만 Ea 부여. **오차 = Bayesian error propagation**(ref 136, Sivia & Skilling).
- 저온 미해상 구조는 Ea를 **아예 안 뽑고** 그룹 B로 강등 — "외삽 신중론"의 모범.

### 5d. 비전도 판정·검출 한계 (정직성의 핵)
- **검출 하한 = D 1×10⁻⁸ cm²/s**: 이보다 낮으면 FPMD로 MSD 수렴 불가 → Fig 15 세로선 = 하한 처리.
- **LLZO 논증(p936, 원문)**: 큐빅 LLZO 500 K 실측 σ 0.02 S/cm → D_tr ≈ 2×10⁻⁷ cm²/s(Haven 1 가정) → 100 ps 동안 6Dt ≈ **1 Å²** — "~100 ps 시뮬레이션으로는 가넷의 500 K 확산도 못 본다. 따라서 이하 물질들(그룹 B)은 상온 전도체일 수 있다." → **"고온만 확산" ≠ "저온 비전도"**를 명문화.
- 그룹 C(70종)는 1000 K에서도 무확산 → "도핑 없인 실험에서도 전도 안 할 것"이라는 **강한 음성 판정**을 MSD 그림 70장(S52–S121)과 함께 전부 공개.
- **σ 환산을 아예 안 함**: 논문 전체가 D_tr만 보고(위 LLZO 역환산 1곳 제외) — Haven/Nernst–Einstein 환산 절대값을 만들지 않는, 우리 "절대 σ 비인용"보다 더 극단적인 보수주의.

## 6. 결과 — 그룹별 전체

### 6a. 기지 전도체 재발견 39종 (스크리닝 자체 검증; FPMD 제외 대상)
- **thio-LISICON/황화물**: Li₇P₃S₁₁, Li₄GeS₄, Li₄SnS₄; LISICON 산화물 Li₄GeO₄, Li₅AlO₄.
- **가넷**: Li₅La₃Ta₂O₁₂(ICSD 68252, 완전점유 entry), Li₅La₃Nb₂O₁₂ (⚠ 큐빅 가넷 Li₇La₃Zr₂O₁₂은 부분점유라 풀에 없음 — 저자 명시).
- **NASICON**: Li₃Sc₂P₃O₁₂? [OCR], Li₃In₂P₃O₁₂, LiZr₂P₃O₁₂, LiTi₂P₃O₁₂, Li₄Zn(PO₄)₂.
- **argyrodite**: **Li₆PS₅I**(ICSD; 질서 배열이라 생존 — FPMD는 그룹 B로, §6c), **산화물 argyrodite Li₆PO₅Cl·Li₆PO₅Br**(ref 23 Kong/Deiseroth 2010), **Li₅PS₄Cl₂**(ref 82 = Zhu/Chu/Ong 2017 — *계산 예측* 조성이 DB에 들어온 사례).
- 기타: Li₃P, (LiI)₂Li₃SbS₃, Li₃Y(PS₄)₂(ref 82), Li–In–I 할라이드(LiInI₄ 계열; OCR 불명확), 플루오로옥소보레이트 Li₂B₃O₄F₃·Li₂B₆O₉F₂, hexaoxometallate Li₇SbO₆·Li₈SnO₆(ref 153 Mühle), LiScP₂O₇, LiAlCl₄, Li₃BN₂, Li₃SbS₃, Li₃BS₃, Li₂B₄O₇, Li₃BP₂O₈, Li₂Ga₂GeS₆ 등 (일부 아첨자는 PDF 추출 한계로 원문 대조 권장 — SI 표에는 이 39종 목록 없음).
- 의미: **"깔때기가 기지 전도체를 통과시킨다"** = 스크리닝의 holistic성(조성 다양성 포괄) 근거.

### 6b. 그룹 A — 신규 fast-ion conductor 5종 + LGPS ★★ (Table 1 + Fig 4–8 + S4–S10)
| 물질 | DB-id | supercell | Δvol(vc-relax) | **Ea (eV)** | D_Li(750 K, cm²/s) | D_Li(500 K) | host 거동 | 비고 |
|---|---|---|---|---|---|---|---|---|
| **Li₁₀GeP₂S₁₂**(LGPS, 레퍼런스) | — | Li₂₀Ge₂P₄S₂₄ | +4.8% | **0.14 ± 0.04** | 1.9e-5 ± 4.6e-6 | 6.2e-6 ± 7.6e-7 | P/S/Ge 전부 ≈0 (안정) | 문헌 정합: Marcolongo-Marzari 0.18, Ong 0.21. c-축 1D 채널 우세(Fig 6) 재현 |
| **Li₅Cl₃O** (Li-oxide chloride) | ICSD 419852 | Li₄₀Cl₂₄O₈ | 0.0% | **0.33 ± 0.04** | 5.7e-6 ± 3.1e-7 | 4.7e-7 ± 1.6e-7 | ⚠ 고온서 Cl·O 약한 확산(1000 K D_Cl 8.8e-7) | 2-supercell 교차(아래 행)로 유한크기 점검. Reckeweg 구조, SSE 용도 실검증 없음. **합성에 원소 Li 필요 → 금속 부산상 리스크**(저자) |
| Li₅Cl₃O (작은 셀) | ICSD 419852 | Li₂₀Cl₁₂O₄ | 0.0% | **0.27 ± 0.04** | 4.2e-6 ± 5.6e-7 | 5.0e-7 ± 2.6e-7 | 위와 동일 | 두 셀 D 호환 → "큰 유한크기 효과 없음"; Ea 차이는 유한 통계 탓(저자) |
| **Li₂CsI₃** | ICSD 245988 | Li₈Cs₄I₁₂ | **−13.1%** | **0.19 ± 0.04** | 3.1e-5 ± 5.7e-6 | 6.1e-6 ± 1.2e-6 | ⚠⚠ **전 온도서 Cs·I 확산**(500 K도 ~9e-7) | 1983 합성(단사정). host 불안정이 실재인지 시뮬 아티팩트인지 미해결(저자 자인) |
| **LiGaI₄** | ICSD 60850 | Li₄Ga₄I₁₆ | **+19.5%** | **0.35 ± 0.06** | 9.1e-5 ± 1.6e-5 | 3.6e-6 ± 1.5e-6 | ⚠ I 확산 잔존(500 K 3.5e-7) | vdW 부재로 +19.5% 팽창 — **Grimme-D3 넣으면 −1.03% 수축**(저자 재계산) → "FPMD 결과 신중 해석; 향후 스크리닝에 vdW 포함해야" |
| **LiGaBr₃** | ICSD 61338 | Li₈Ga₈Br₂₄ | **+14.2%** | **0.26 ± 0.02** | 4.9e-5 ± 5.2e-6 | 5.3e-6 ± 1.2e-6 | ⚠ 1000 K서 host 사실상 융해(D_Ga 2.2e-5·D_Br 2.1e-5) | Hönle-Simon 합성, 층상 Li₂⁺[Ga₂Br₆]²⁻. Li₃InBr₆ 유사성 → Ga-도핑 브로마이드/아이오다이드 제안([Muy] 스크리닝과 교차) |
| **Li₇TaO₆** | ICSD 74950 | Li₅₆Ta₈O₄₈ | +4.0% | **0.29 ± 0.02** | 1.9e-6 ± 3.1e-7 | 2.3e-7 ± 4.7e-8 | ✅ **전 온도 host 완전 안정**(D_O·D_Ta ≈ 0) | **가장 깨끗한 신규 후보**. 3D 단일 연결 성분(Fig 8). 실험 Ea 0.66–0.67 eV(Mühle/Nomura)와 불일치 — 단 실험도 저온(<50 °C)·고온(>400 °C) 저장벽 영역 보고. 알리오밸런트 Ta 치환 제안 |
| (참고) 그룹 A의 나머지 온도 D | | | | | 1000 K: LGPS 3.8e-5 / LiGaI₄ 1.9e-4 / LiGaBr₃ 1.4e-4 / Li₂CsI₃ 4.8e-5 / Li₅Cl₃O 1.9e-5·1.2e-5 / Li₇TaO₆ 7.1e-6 | 600 K: 1.7e-5 / 1.3e-5 / 2.8e-5 / 9.9e-6 / 1.3e-6·1.4e-6 / 4.8e-7 | | SI Fig S4–S10 legend 전사 |
- 시뮬 시간(Table 1, ps; 500/600/750/1000 K): LiGaI₄ 726/726/552/218 · LiGaBr₃ 407/436/232/58 · Li₂CsI₃ 726/726/349/160 · LGPS 726/494/174/218 · Li₅Cl₃O 726/726/232/262 및 726/726/726/218 · Li₇TaO₆ 552/639/203/73 (본문 서술과 일부 ±수십 ps 불일치 — 경미, Table 1 기준).
- **판정의 정직성**: 5종 중 3종(Li₂CsI₃·LiGaI₄·LiGaBr₃)에 host 불안정/vdW 경고를 스스로 달았고, Li₅Cl₃O엔 합성 리스크, Li₇TaO₆엔 실험 불일치를 명기 — "발견"을 팔지 않고 리스크를 전부 공개.

### 6c. 그룹 B — potential fast-ion conductor 40종 (Table S1 19 + Table S2 21)
**(i) multi-T 19종 (Table S1; Fig S11–S30)** — 구조 | DB(id) | supercell | Δvol | 판정 요지:
| 구조 | DB-id | supercell | Δvol | 거동 (D_Li, cm²/s) |
|---|---|---|---|---|
| **Li₄Re₆S₁₁** | COD 1008693 | Li₁₆Re₂₄S₄₄ | +2.6% | 전 T 확산 흔적(750 K 1.1e-5·500 K 3.2e-6), host 안정, 3D(Fig 9) — 단 87–291 ps로 저온 미해상 → A 승급 보류 |
| **Li₆PS₅I** ★ | ICSD 421083 | Li₄₈P₈S₄₀I₈ | +2.9% | **subdiffusive/caged MSD**(1000 K에도 MSD ~12 Å²/35 ps; 500 K 9.6e-7 명목치) — "확산 영역을 해상 못 함" → potential로만 분류. "나중에야 실험·시뮬 문헌(ref 180)을 인지"(정직 고백) |
| Li₂B₂S₅ (perthioborate) | COD 1510745 | Li₈B₈S₂₀ | +5.4% | 1000 K 4.5e-5·750 K 1.1e-5 → **600 K서 급락(≈0)**. "perthioborate족 더 연구할 가치"; **[Sendek17]도 이 조성을 후보로 지목**(직접 교차 인용) |
| LiTaGeO₅ | ICSD 280992 | Li₄Ta₄Ge₄O₂₀ | +3.5% | 1000 K 3.9e-5·600 K 2.7e-6, **500 K 사멸**(3.3e-9). 참조문헌 231 K 상전이(무질서상)는 미채택 — 질서상만 시뮬 |
| Li₂S₂O₇ | ICSD 188009 | Li₁₆S₁₆O₅₆ | +5.4% | **1000 K만** 3.1e-5(host S·O도 ~2e-6 — 불안정 신호), 750 K↓ ≈0 |
| LiIO₃ | ICSD 20032 | Li₁₆I₁₆O₄₈ | **+15.3%** | 1000 K 2.9e-5이나 **host 융해급**(D_O 7.4e-6·D_I 5.4e-6), 500 K ≈0. [Muy] 후보와 교차 |
| LiAlSiO₄ (β-eucryptite) | COD 9000368 | Li₁₂Al₁₂Si₁₂O₄₈ | +3.6% | 1D(c-축) 수송 재현(실험 1980 정합), 1000 K 2.7e-5 → 600 K 무시(2.3e-7) |
| Li₅B(SO₄)₄? [Li₅BS₄O₁₆] | ICSD 428002 | Li₂₀B₄S₁₆O₆₄ | +6.3% | 1000 K 2.7e-5·750 K 2.8e-6(3D, Fig 12), **500 K ≈0**(1.2e-7, MSD 평탄) |
| Li₂Mg₂(SO₄)₃ | COD 2020217 | Li₈Mg₈S₁₂O₄₈ | +4.1% | 1000 K 2.1e-5 → 600 K 2.8e-7 급락. Fe/V 도핑 유도체는 양극재로 연구됨 |
| **LiTiPO₅** | ICSD 39761 | Li₁₆Ti₁₆P₁₆O₈₀ | +5.8% | host 안정·1D 채널(Fig 11), 1000 K 1.4e-5·**500 K에도 1.8e-6 흔적**(정량 불가) — B군 중 A에 가장 근접한 산화물 |
| Li₃CsCl₄ | ICSD 245975 | Li₂₄Cs₈Cl₃₂ | +1.6% | 750 K 8.6e-7 2D 확산(Fig 14) → 600 K 급락(2.5e-8) |
| Li₆Y(BO₃)₃ | COD 1510933 | Li₂₄Y₄B₁₂O₃₆ | +2.8% | 1000 K 9.8e-6·750 K 1.3e-6 → 600 K 이하 사멸; **in-plane 경로가 저온서 꺼짐**(Fig 13, 750 vs 500 K 밀도) — Lopez-Bermudez NEB와 정합 |
| Li₂ZnSnSe₄ | COD 7035178 | Li₁₆Zn₈Sn₈Se₃₂ | +4.2% | 1000 K만 9.4e-6 |
| Li₂Ti₃O₇ (ramsdellite) | ICSD 193803 | Li₈Ti₁₂O₂₈ | +2.6% | 1000 K만 7.2e-6 |
| Li₇RbSi₂O₈ | ICSD 33864 | Rb₄Li₂₈Si₈O₃₂ | +2.8% | 1000 K만 6.2e-6 (Bernet-Hoppe "우연히 합성"된 orthosilicate) |
| Li₃GaF₆ | COD 8101456 | Li₁₈Ga₆F₃₆ | +4.8% | 1000 K만 6.2e-6 |
| Li₂In₂GeS₆ | COD 4329224 | Li₁₆In₁₆Ge₈S₄₈ | +5.6% | 1000 K만 4.0e-6 (비선형광학 결정) |
| LiMoAsO₆ | COD 2014117 | Li₈Mo₈As₈O₄₈ | +8.2% | 1000 K만 3.5e-6 |
| Li₉Ga₃(P₂O₇)₃(PO₄)₂ | COD 2208797 | Li₁₈Ga₆P₁₆O₅₈ | +2.1% | 1000 K 2.8e-6·750 K 9.0e-7 → 600 K ≈0. V-유사체는 양극재 |
**(ii) 1000 K-only 21종 (Table S2; Fig S31–S51)** — "확산은 있으나 저온 계산 비용 대비 우선순위 낮음" 판정: LiGaCl₃(D_Li **1.1e-4**! COD 1530096, Δvol +17.0%) · LiGaBr₄(8.8e-5, **Δvol +30.8%**, host 유동) · Li₆MgBr₈(7.0e-5, Suzuki상) · Li₃P₇(4.1e-5) · Li₃AsS₃ · LiB(SO₃Cl)₄[LiBS₄Cl₄O₁₂] · LiSn₂P₃O₁₂(NASICON) · Li₄Ge₉O₂₀ · LiIO₄ · Rb₂LiTaS₄ · LiP₇ · Li₄P₂O₇ · Li₂Ge₄O₉ · LiAuF₄(ICSD 33953) · Li₂SeO₄ · LiAlSe₂ · LiInP₂O₇ · Li₄TiO₄ · Li₆Si₂O₇ · Li₂In₂SiSe₆ · LiB(SO₄)₂[LiBS₂O₈] (전체 Δvol·시뮬시간 Table S2).
- ⚠ 정량 주의: 21종의 D는 43.6–445 ps 단일 온도 — 랭킹·존재 판정용이지 물성값 아님.

### 6d. 그룹 C — non-diffusive 70종 (Tables S3·S4; Fig S52–S121) — 정직한 음성 결과
- 판정문(원문): "our simulations give evidence that this structure will also **not conduct in experiment, unless doped significantly**".
- **가족별**: 질화물(Li₂CeN₂·Li₅ReN₄·Li₇PN₄·Li₃ScN₂·Li₇NbN₄·Li₃AlN₂·Li₆WN₄·Li₄TaN₃·옥시나이트라이드 Li₁₆Nb₂N₈O) / 할라이드(LiAuF₄[COD 1510140 — S2의 ICSD 33953 entry와 **다른 entry가 반대 판정**: 같은 조성도 구조 entry 따라 갈림]·LiNb₃InCl₉·Li₂Cs₃Br₅·KLiYF₅·Li₂Ta₂O₃F₆·Li–Zr–Be–F) / 붕산염 다수(Li₂AlB₅O₁₀·Li₃Sc(BO₃)₂·Li₃GaB₂O₆×2·Li₂AlBO₄·Li₈Be₅B₆O₁₈·Li₆Be₃B₄O₁₂·Li₃AlB₂O₆·LiBO₂·Li₃B₇O₁₂·Cs₂Li₃B₅O₁₀·NaLi₂BP₂O₈·Rb₂Li₃BP₄O₁₄·Li₂B₃PO₈) / 인산염(Li₂Cd(PO₃)₄·LiPO₃·Li₄Zn(PO₄)₂·**Li₉Mg₃(PO₄)₄F₃ — 실험 보고 전도도와 정면 모순, 저자 명시**) / 규산염(LiBSi₂O₆·Li₂Si₃O₇·LiYSiO₄·Li₃AlSiO₅·Li₂Si₂O₅×2·Li₂MgSiO₄·SrLi₂Si₂N₄) / 텔루르산염(Li₂TeO₃·Li₄TeO₅·Li₆TeO₆·Li₂TeWO₆) / 탄탈·니오브(Li₆Sr₃Ta₂O₁₁·SrLi₂Ta₂O₇·Li₃Ba₂TaN₄·Li₃Ba₂NbN₄·Li₄KNbO₅·**LiNbO₃**) / 아연·몰리브덴·비소(Li₆ZnO₄[Nb 도핑 없인 비전도 — 실험 정합]·LiKZnO₂·LiZnAsO₄·Li₂MoO₄·Li₂Mo₄O₁₃·LiYMo₃O₈·Li₃AlMo₂As₂O₁₄·Li₆Zn₆As₆O₂₄계) / 귀금속 산화물(**Li₃AuO₃ — Filsø의 전자밀도 서술자는 3D 전도체로 예측했으나 완전점유 FPMD는 무확산(서술자 반례)**·Li₂PdO₂·Li₈PtO₆·LiReO₄) / 기타(Li₄SrP₂·LiLa(CO₃)₂류·Li₄KAlO₄·Li₄Ge₅O₁₂·Li₂WO₄·Li₂W... 전량 Tables S3/S4).
- 수치 스타일: 예) Li₂₄Al₈N₁₆ D_Li = (−2.0 ± 5.0)e-9 — **0과 정합한 음수 추정값도 그대로 보고**(MSD 평탄 + 블록 오차) = "no diffusion"의 통계적 정의.

### 6e. 그룹 D — pinball만 확산, FPMD 실패 15종 (Table S5)
SCF 반복 발산 등으로 FPMD 판정 불가: Li₄Mo₃O₈ · LiTaSiO₅ · Li₂PdP₂O₇ · NaLi₂PO₄(nalipoite) · BaNaLi₃B₆O₁₂ · NaLiB₄O₇ · NaLi₂BO₃ · LiAuS₄O₁₄(Δvol +22.1%) · **Li₁₀B₁₄Cl₂O₂₅(boracite형 — 실험적으로 수송 관찰 보고)** · LiAuI₄ · **Li₅La₃Nb₂O₁₂(가넷!)** · LiZr₂As₃O₁₂(NASICON 비소산염) · LiAlGeO₅[표기 그대로; zeolite-framework계, CPMD 선행연구는 무확산] · Li₃ScF₆ · LiNb₃Cl₈.

### 6f. §3.5 Context — 스코프의 정직한 한계와 다음 단계
- **완전점유·화학량론 Li만 스크리닝** — "Li 자리만 부분점유(+타 원소 자리 완전점유)" 구조가 **추가 645개**(비-유니크) 존재 → 미탐색.
- **완전점유인데 왜 전도체가 나오나**(격자간 자리 없이는 공공 없인 확산 불가일 텐데): ① 고온 시뮬 — CIF의 RT 점유는 지시값일 뿐 ② XRD가 저점유 Li 자리를 버리고 보고했을 가능성 → "완전점유 클래스에도 전도체가 *포함*된다"(증명됨).
- 부분점유 스크리닝의 난점(명문): vc-relax는 정수 점유에서만 가능 → **조성별 바닥상태 부피 결정법이 선결 과제**, D의 부피 민감성 때문에 고정밀 필요. (= 우리 disorder-ensemble에서 anneal+FIRE로 부피·기하 이완을 같이 잡는 이유의 문헌 인정)
- **공공 도입 스크리닝 제안**: 모든 물질에 Li 공공을 넣고 확산 급등 여부 → "도핑으로 고전도화 가능" 후보 탐색 — 도구는 이미 준비됨.
- 서술자 부재의 고백(결론): "구조 특징·대칭성에서 **일반 트렌드를 찾지 못했다**" → 데이터 공개(Materials Cloud)로 후속 서술자 연구 촉구.

## 7. Figure set ★ (본문 전체 + SI 핵심)
| Fig | 내용 | 우리가 쓸 점 |
|---|---|---|
| 1 | 깔때기 3D 모식도(구조가 필터 통과하며 낙하; Structural→Band structure→Pinball→FPMD; Excluded/Candidate 바구니; "Powered by AiiDA") | [Xiao] Fig 1과 같은 문법 — 우리 cascade 계보 그림에 "MD-스크리닝 축"으로 병기 |
| 2 | AiiDA DAG provenance (Li₇TaO₆ 1물질의 전 계산 그래프; 파랑=ingestion·초록=밴드/이완/피팅·빨강=pinball 확산) | 재현성 인프라의 시각화 표준 — 우리 tools/ 워크플로 문서화에 참고 |
| 3 | vc-relax 부피변화 히스토그램(N=971; 피크 +4%≈+1.3%/방향; 팽창>수축, PBE 전형) + 꼬리 outlier(vdW 결핍) | PBE 부피 편향의 대규모 통계 — 우리 EOS·격자상수 비교 시 "PBE는 ~+4% 팽창이 정상" 근거 |
| 4 | 그룹 A Arrhenius(4점, 오차막대, 점선 피팅; 범례에 Ea) | **우리 아레니우스 그림과 동일 문법**(3점 vs 4점) — Ea 오차막대·supercell명 표기 관행 |
| 5 | LGPS·Li₅Cl₃O(2셀) 750 K MSD — 굵은선=전 궤적, 얇은선=블록별, 점선=20–30 ps 피팅; **host 종 MSD 동시 표기** | ★ **host-lattice MSD를 Li와 같은 패널에 그리는 관행** — 우리 MD QC 그림에 이식(호스트 안정성 즉시 판독) |
| 6 | LGPS Li 확률밀도 500 K(등가면 3단계; c-축 1D 채널) | 밀도 시각화 파라미터(σ=0.3 Å·10 pts/Å·0.1/0.01/0.001 Å⁻³)가 명문화된 드문 사례 — 우리 VESTA cube 관행과 비교 |
| 7 | Li₅₆Ta₈O₄₈·Li₄Ga₄I₁₆·Li₈Ga₈Br₂₄ 750 K MSD(블록·피팅 동일 문법) | host 확산(D_I·D_Br≠0)이 눈으로 보임 — "fast-ion인데 host도 흐른다" 경고의 원본 |
| 8 | Li₇TaO₆ Li 밀도 500 K — 3D 단일 연결 성분 | 연결성(percolation) 논거를 밀도 등가면으로 — 우리 li_percolation 서사와 같은 시각 언어 |
| 9–11 | Li₁₆Re₂₄S₄₄ 밀도(3D)·Li₁₆Re₂₄S₄₄/Li₁₆Ti₁₆P₁₆O₈₀ MSD·LiTiPO₅ 밀도(1D) | 그룹 B 대표 2종의 차원성 판정 |
| 12–14 | Li₂₀B₄S₁₆O₆₄ 밀도(3D, 600 K)·Li₂₄Y₄B₁₂O₃₆ 밀도(750 vs 500 K — **저온서 경로 꺼짐**)·Li₂₄Cs₈Cl₃₂ 밀도(2D) | **온도별 밀도 비교로 "경로가 꺼진다"를 보이는 문법** — 우리 comp1/modelc 온도별 밀도 비교에 이식 가치 |
| 15 | D_FPMD vs D_PB 산점(1000 K, 음이온 색; 세로선 1e-8=검출하한) | ★ surrogate 검증 그림의 표준 — 우리 UMA-vs-DFT 검증 그림(D 또는 힘)에 같은 문법 |
| 16 | 클러스터별 node-hours 파이(총 ~509k; Bellatrix 69k·Fidis 34k·XC40 266k·XC50 140k) | HT 예산 보고 관행 — 우리 KISTI/gabia 자원 보고에 참고 |
| 17 | 이온 스텝당 node-time 히스토그램: pinball(파랑) vs DFT(초록) — **~4자릿수 차** | "surrogate 절감분을 통계에 재투자" 논거의 정량 그림 |
| S1 | 717종 gap(실험 부피) vs gap(vc-relax 부피) 상관(색=V_rel/V_exp) — 강상관; 무gap→유gap만 발생, 역은 없음 | **"실험 기하 1-shot gap으로 절연체 필터"의 방법 정당화** — 우리도 스크리닝 1차 필터에 차용 가능 |
| S2 | D(총 MSD@50 ps) vs D(기울기 8–10 ps) — 비확산계서 전자가 과대 | MSD 처리의 고전 함정(진동 기여) 시각화 |
| S3 | 기울기 t'=5/10/20/30 ps vs 40 ps 4패널 — 5 ps 과대·10 ps부터 수렴 | ★★ **"MSD 창을 데이터로 정당화"의 원본** — 우리 2–50 ps 창 검증 재현 template |
| S4–S10 | 그룹 A 전 온도 MSD(전 종·블록·오차) | D 수치 전사원(§6b) |
| S11–S51 | 그룹 B MSD(19종 4-T + 21종 1000 K) | 〃 (§6c) |
| S52–S121 | 그룹 C 70종 MSD(평탄; 음수 D±오차 그대로) | "no diffusion"의 통계적 정의 시각화 |

## 7.5 재현 수준 방법 절을 보는 요령

"재현 수준" 이란 **남이 그대로 다시 돌릴 수 있을 만큼** 적었다는 뜻이다. 확인 순서는
① 범함수 ② 유사퍼텐셜(pseudopotential) 종류 ③ 컷오프 ④ k점 ⑤ 스미어링 ⑥ 수렴 임계값.
특히 **유사퍼텐셜**은 같은 원소라도 종류마다 valence 전자 수가 달라서, 다르면 전에너지가
통째로 다른 기준이 된다 — **절대 에너지를 논문 간에 비교하면 안 되는 가장 흔한 이유**다.

---

## 8. DFT/계산 방법 ★ (재현 수준)
| 항목 | 값 |
|---|---|
| code | Quantum ESPRESSO **pw.x** (FPMD·SCF·vc-relax 전부), pinball은 자체 구현(PRM 2018) + AiiDA 워크플로 |
| functional | **PBE** (전 계산) · **vdW 없음**(A.5 명시 "Van-der-Waals contributions are not considered" — LiGaI₄ +19.5% 사례로 한계 자인, D3 재계산 1건만) |
| pseudo | **SSSP Efficiency 1.0** 라이브러리(혼합 PAW/US; 컷오프도 라이브러리 권장값) |
| smearing/판정 | Marzari–Vanderbilt cold smearing **σ=0.02 Ry ≈ 0.27 eV**, 밴드 +20%; **절연체 = E_F 위 최저 준위 점유 < 10⁻³ e** (gap 값 자체는 스크리닝에 미사용 — "PBE가 절연체라면 실험도 절연체"의 단방향 안전 논리) |
| k-points | MP 그리드 밀도 **0.2 Å⁻¹**(SCF·vc-relax) / FPMD는 **Γ-only** |
| vc-relax | 초기 랜덤 변위 σ=0.1 Å(대칭 파괴) → BFGS; 수렴: 힘 <5e-5 Ry/Bohr · ΔE <1e-4 Ry · 압력 <0.5 kbar |
| supercell | Hart–Forcade HNF 전수 + 최소부피·내접구 지름 기준(supercellor): pinball **d_inner=8 Å**(≤500원자), FPMD **6.5 Å** |
| pinball-MD | dt 0.96 fs · canonical(확률충돌 1000 dt) + **8×NVE 분기**(각 50,000 dt) · 1.5–18.4 ns/물질·온도 · T=1000 K |
| FPMD | BOMD · dt 1.45 fs · **SVR 열욕 τ=100 dt**(자체 QE 구현) · 1000→750/600/500 K · 가변 길이(수렴 기준 도달 시 종료) |
| 무질서 처리 | **없음** — 부분점유 구조 입구 제외, 실험 CIF 단일 배열 그대로(질서 구조만) |
| DFT+U / MLIP | 없음 / 없음(pinball은 ML 아님 — 물리항 3-파라미터 회귀) |
| 자동화 | **AiiDA**(전 계산 DAG·데몬 병렬화) · 분석 **SAMOS** · 구조 표준화 COD-tools · 중복 pymatgen StructureMatcher(각도 5°·격자 20%·site 30%) + CMPZ |
| 규모 | SCF 2,503 · vc-relax 5,214 · **pinball-MD 171,370** · **FPMD 11,525**(재시작 포함) · 총 ~509k node-hours(4개 클러스터) |

## 9. Post-processing ★
- **MSD/D**: SAMOS — 블록 분해·기울기 회귀(pinball 8–10 ps·FPMD ≥20 ps)·mean±SE. Ea = Arrhenius 선형 피팅 + **Bayesian 오차 전파**(Sivia).
- **Li 확률밀도**(eq 3): Gaussian σ=0.3 Å·10 pts/Å 격자·등가면 0.1/0.01/0.001 Å⁻³ — 차원성(1D/2D/3D)·연결 성분 판정.
- **host 안정성**: 전 종 MSD 동시 산출(D_host ≈ 0 여부) — fast-ion 판정의 필수 짝.
- **없는 것**: σ 환산(Haven/NE) 없음 · ESW/hull 없음 · NEB 없음 · Bader/COHP/DOS-그림 없음(절연 판정은 점유수만) — 철저히 "확산계수 단일 물성" 논문.

## 10. 우리 DFT/MD 대비 (comp1/modelc; `our_dft_baseline.md`) ★★

### 10a. MD 통계 규율 — 항목별 엄격/느슨 판정
| 항목 | Kahle (pinball/FPMD) | 우리 (UMA MLIP-MD) | 판정 |
|---|---|---|---|
| 힘 계산 | pinball(3-param frozen-host surrogate) → FPMD(BOMD·PBE·Γ) 2단 | UMA-s-1p1(omat) 전 원자 MLIP 단일 | 축이 다름 — "둘 다 AIMD" 화법 금지(그들 FPMD만 진짜 AIMD) |
| MSD 창 | pinball 8–10 ps·FPMD ≥20 ps(20–30 ps) — **창 자체를 Fig S3로 검증** | **2–50 ps 고정**(창이 더 김) | 창 길이는 우리가 위, **창 정당화 절차는 그들이 위** → 우리 창의 S3식 검증 1회 이식 권고 |
| 오차 산정 | 궤적 독립 블록 분산 → mean±SE, **워크플로가 err<1e-8 cm²/s or <5%까지 자동 연장** | 멀티시드(600 K 3-시드) 분산; comp1/modelc Ea는 단일 궤적(오차막대 없음) | per-material 자동 수렴판정은 그들이 위; 시드-간(초기조건) 분산은 우리만 잡음 — **상보적**(블록=궤적 내·시드=궤적 간) |
| 온도 | 1000 K 게이트 → 750/600/500 K(1/T 등간격 4점); Ea는 500 K 해상 시만 | 600/800/1000 K 3점(400/500 K 제외 판정) | 그들이 더 저온까지 시도하되 미해상 시 Ea 자체를 포기(정직); 우리는 저온 제외 사유를 명문화 — 정신 동일 |
| Ea 오차 | **Bayesian error propagation** | 600 K 3-시드 오차막대 | 그들 방식이 문헌 표준화에 유리 — 이식 후보 |
| 비전도 판정 | D<1e-8 cm²/s = 수렴 불가 floor 명문 + LLZO-100 ps 논증("고온만 확산≠비전도") | 400/500 K 제외 판정·frozen artifact 인지(disorder_ensemble d=0) | 동일 정신의 두 구현 — LLZO 논증은 인용 가치 높음 |
| σ 절대값 | **환산 자체를 안 함**(D_tr만; LLZO 역산 1곳 제외) | NE(Haven=1) 환산하되 절대값 인용 금지 | **그들이 더 극단적 보수** — 우리 규율의 상위 선례 |
| 무질서 | 부분점유 전부 제외·단일 실험 배열(질서만) | **disorder ensemble**(라벨스왑 d-level·cfg 3개·anneal+FIRE) | **우리가 압도적으로 엄격** — 그들의 최대 블라인드 스팟(아래 10c) |
| host 처리 | pinball: **완전 동결** / FPMD: 전 원자 | 전 원자(+anneal로 host 이완까지) | 아래 10b |

### 10b. Pinball(frozen host) vs 우리 disorder-ensemble(host 이완) — 정반대 철학 ★
- Kahle의 스크리닝 축은 "host는 동결해도 Li 동역학의 순위는 보존된다"에 베팅 → Fig 15에서 **정량은 무너지고 랭킹만 생존**(top 71%/바닥 21%). 실패 원인 자인 4중에 "**freezing the host lattice could have a larger effect than anticipated**" 포함.
- 우리는 반대로 host를 **적극 이완·동역학 포함**(UMA 전 원자 + anneal 700 K + FIRE) — [KimMTP](`kim2024_mtp_argyrodite_disorder_gb.md`)의 **PS₄ 회전·진동 고정 시 D(600 K) −50%(disordered)/−18%(ordered)** 가 바로 frozen-host 근사가 argyrodite류에서 D를 절반까지 깎을 수 있음을 정량화한 교차점 — **pinball을 argyrodite에 적용했으면 상당한 과소평가가 나왔을 것**(단 pinball 오차는 계 의존적·방향 비보장; Fig 15에는 과대·과소 산포가 모두 있음).
- 종합: **"surrogate는 랭킹, 물성값은 상위 이론"** — Kahle(pinball 랭킹→FPMD 정량)과 우리(UMA 랭킹/trend→DFT 검증·절대값 비인용)는 같은 위계 규율의 두 구현. 차이는 surrogate의 오차 성격(물리 근사 vs PES 학습 각인).

### 10c. Argyrodite 블라인드 스팟과 Li₆PS₅I 삼각검증 ★
- 부분점유 제외 → **Li₆PS₅Cl/Br(우리 comp1·modelc 계열)은 이 깔때기에 입장 자체를 못 함**. 무질서가 σ의 필요조건인 물질군([Klerk]·[KimMTP])은 "완전점유·질서" 스크리닝의 구조적 사각지대 — 우리 disorder-ensemble 파이프라인의 존재 이유를 HT 원전이 반증 형태로 보여줌.
- 살아남은 **Li₆PS₅I(질서 배열)는 FPMD에서 subdiffusive/caged MSD로 "해상 불가"** — 이는 ① [Klerk] all-4a(질서 I형) = intercage 점프 0 ② [Kraft] 실측 σ(I) ~1e-6 S/cm ③ 우리 comp5(Li₆PS₅I) frozen 계열 관찰과 **4자 삼각 정합**: 질서 argyrodite는 cage 내 rattling만 남는다. Kahle의 FPMD가 이를 (본인들은 모르는 채) 재확인한 셈.
- Li₅PS₄Cl₂(Ong 2017 예측 조성)가 "기지 전도체"로 재발견됨 — [Klerk]의 Li₅PS₄X₂ 제안과 같은 halogen-rich end-member 계보.
- 밴드갭: 그들은 gap 값을 아예 안 쓰고 **점유 기준 절연 판정**(PBE 과소평가의 단방향 안전 활용) — 우리 "fixed-occ nscf 고유값만 인정·DOS-threshold 금지" 규율과 **다른 문제를 푸는 다른 규율**(스크리닝 필터 vs 물성값). gap 수치 비교 대상 없음(n/a).
- 이온전도 수치: LGPS Ea 0.14±0.04(FPMD)는 소환값 — 우리 argyrodite Ea(0.253/0.224)와 물질이 달라 직접 비교 없음. 유일한 접점은 **방법 규율**이며 그것이 이 digest의 존재 이유.

## 11. 적용 인사이트 (내 연구에 어떻게)
- ① **방법 규율의 문헌 앵커**: 우리 SEMIFINAL 멀티시드·절대 σ 비인용·저온 제외 판정이 "우리만의 결벽"이 아니라 HT-MD 원전의 규율(블록 오차·자동 수렴·검출 하한·Ea 포기 규칙)과 같은 계보임을 인용으로 보일 수 있음. 특히 **Fig S3(창 수렴 검증)·Bayesian Ea 오차 전파** 두 절차는 우리 파이프라인에 1회씩 이식할 가치(2–50 ps 창의 t'-스캔 검증 + Ea 오차의 Bayesian 산출).
- ② **"host-lattice MSD 동시 플롯" 관행 이식**: fast-ion 판정마다 D_host를 같은 패널에 — 우리 MD QC(특히 도핑 셀·고온 800/1000 K)에서 host 안정성 자동 판독. Kahle의 그룹 A 5종 중 3종이 host 유동 경고를 받은 것이 이 관행의 가치 증명.
- ③ **깔때기 서사(3자 비교)**: [Sendek17] ML 분류기(12,831→317→21) / [Xiao2019] 열역학 게이트(104,082→…→184→3) / **[Kahle2020] 물리 MD(4,963→1,362→1,016→796→132→45)** — 우리 cascade 발표에서 "서술자·게이트·동역학 3축 계보 + 우리는 within-host 개질" 위치 선언에 사용. Kahle 스스로 Sendek 발생률(14%)과 자기 수확(84/796)의 정합을 계산한 것도 인용 포인트.
- ④ **경고로서의 pinball**: "동결 근사 surrogate는 랭킹까지만"을 top 71%/바닥 21%로 정량화 — 우리 UMA 결과 발표 시 "왜 절대값을 안 파는가"의 외부 근거([KimMTP] functional 각인과 쌍).
- ⑤ **후보 광맥**: Li₇TaO₆(host 안정 3D·Ea 0.29)·LiTiPO₅·Li₄Re₆S₁₁·perthioborate Li₂B₂S₅([Sendek17]과 이중 지목) — argyrodite 밖 확장 시 1순위 소환 목록. 단 vdW·host 유동 경고 동반 물질(Ga/Cs 할라이드) 구분.

## 12. 인용 가능 문장 (deck/paper용)
- "Kahle, Marcolongo and Marzari (EES 2020) screened all experimentally reported Li-containing structures in ICSD and COD (4,963 unique) through insulating-state and diffusion filters — 7.6 μs of pinball-model MD on 796 structures followed by 45 ns of first-principles MD on 132 — identifying five new fast-ion conductors (Li₅Cl₃O, Li₂CsI₃, LiGaI₄, LiGaBr₃, Li₇TaO₆; Ea 0.19–0.35 eV) alongside 70 honestly reported non-conductors."
- "In their protocol the diffusion coefficient is taken from the slope of the MSD (8–10 ps for the pinball model, ≥20 ps for FPMD, a window itself validated against 40 ps fits), the uncertainty from the variance over independent trajectory blocks, and each workflow runs until the error of the mean falls below 1×10⁻⁸ cm² s⁻¹ or 5% — with activation energies extracted only when diffusion is resolved down to 500 K, and errors propagated Bayesianly."
- "The frozen-host pinball surrogate fails to reproduce FPMD diffusion coefficients quantitatively, yet ranks candidates effectively: 71% of the top pinball quartile show D > 10⁻⁷ cm² s⁻¹ in FPMD versus 21% in the bottom quartile — a four-orders-of-magnitude-cheaper classifier, not a property predictor."
- "Because the screening excludes partially occupied structures, disorder-stabilized conductors such as Li₆PS₅Cl are structurally invisible to it; the ordered Li₆PS₅I that survives shows only caged, sub-diffusive Li motion in FPMD — consistent with site-disorder being a prerequisite for macroscopic diffusion in argyrodites."

## 13. 주의/한계 (over-claim 방지 — 비판적으로)
- **pinball 정량 실패는 저자 자인** — 이 논문을 "pinball이 D를 재현한다"로 인용하면 오독. 반대로 "스크리닝 무용"도 오독(랭킹 유효·54% 예측률·하한 논증까지가 사실).
- **vdW 부재**: 할라이드 후보(LiGaI₄ +19.5%·LiGaBr₄ +30.8%·LiIO₃ +15.3% 팽창)의 D·Ea는 부피 오차에 실림 — LiGaI₄ D3 재계산(−1.03%)이 증거. 그룹 A 할라이드 수치는 방법-의존 소환값으로만.
- **host 유동**: Li₂CsI₃(전 온도 Cs·I 확산)·LiGaBr₃(1000 K 융해급)·LiIO₃ — "fast-ion conductor" 표제만 보고 안정 SSE로 인용 금지. 가장 깨끗한 후보는 Li₇TaO₆ 하나.
- **Li₇TaO₆ 실험 불일치**: FPMD 0.29 vs 실험 0.66–0.67 eV — 저자는 실험의 저온/고온 저장벽 영역을 들지만 미해결. (후일담: 2022~ Li₇TaO₆ 재조명 실험들이 있으나 이 digest 범위 밖 — 문헌 추가 확인 필요.)
- **FPMD 셋업의 스크리닝 타협**: Γ-only·d_inner 6.5 Å(작은 셀)·PBE·열욕 SVR τ=100 dt·수십~수백 ps — 개별 물질 정밀 논문 대비 거친 설정. D 절대값은 ±수십 %급 흔들릴 수 있는 소환값.
- **8–10 ps(pinball) 창**: fast-ion 전제에서 정당화된 창 — 느린 계에 이식하면 위양성(그들 스스로 Fig S3에서 보임). 우리 2–50 ps와 단순 비교 금지(대상 D 영역이 다름).
- **단일 실험 배열·완전점유**: 무질서·공공 물질군 누락(argyrodite·큐빅 가넷) — "ICSD/COD 전수"라는 표제의 실효 커버리지는 질서 구조 부분집합.
- **분류 경계의 통계성**: 그룹 B↔C 경계는 시뮬 길이에 의존(87 ps짜리 판정 다수) — 개별 물질 재분류 가능성 상존. C의 "실험 모순" 2건(Li₉Mg₃(PO₄)₄F₃·Li₃AuO₃)은 방법 차이(도핑·결함·서술자 한계)일 수 있음.
- **OCR 캐비앗**: 본문 나열식 조성 일부(§6a 기지 39종·§6d 일부)는 PDF 텍스트 추출이 아첨자를 흔들어 표기 불확실 — SI Table이 있는 그룹(A/B/C/D)은 표 기준으로 전사했고, 39종 목록만 원문 재대조 권장.
- **인프라 종속**: 결과 재현엔 AiiDA+자체 pinball 구현 필요 — 값 재현보다 **규율 이식**이 현실적 활용.
