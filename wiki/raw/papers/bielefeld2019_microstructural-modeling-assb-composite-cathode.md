---
title: "Bielefeld, Weber, Janek 2019 — Microstructural Modeling of Composite Cathodes for All-Solid-State Batteries (J. Phys. Chem. C 123, 1626−1634)"
source_url: local-upload/01._Microstructural_Modeling_of_Composite_Cathodes_for_All-Solid-State_Batteries.pdf
ingested: 2026-09-16
sha256: c19a68f9a38f5bdc20d32ae3ceefb4c92e9d70efe48d3596ce3cd826e750f9cf
---

# 수집 목적

Anja Bielefeld (교신), Dominik A. Weber, Jürgen Janek (교신),
**"Microstructural Modeling of Composite Cathodes for All-Solid-State Batteries"**,
*J. Phys. Chem. C* **123** (2019) 1626−1634 의 **절별 해체분석**.

**이 위키 `assb` 섹션의 첫 논문이다.** 액체셀 계열 20 편과 **섞지 않는다** — 음극 축이
다르고, 이 논문은 애초에 **음극도 전압도 다루지 않는다**.

흡수 이유는 하나다. 닻 질문([[assb-contact-loss-vs-lampe]])의 미결 항목 1 —
**"접촉 손실을 모델에 어떤 형태로 넣나"** — 에 대해 이 논문이 **어휘와 단위를 준다.**
`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §2 의 A1(접촉 손실 / 퍼콜레이션)이
"용량이 준 것처럼 보이는데 물질은 그대로" 라고 적힌 그 양은, 이 논문의 언어로는
**이용률(utilization level) `θ = V_c/V_ν`** (식 6) 이다. DEM 산출을 합성 forward model 에
주입할 때의 **인터페이스 후보**가 여기 있다 (§12).

동시에, 이 논문이 **주지 않는 것**이 주는 것보다 많다 — 그리고 그것이 이 digest 의
절반이다 (§11 의 Q1~Q8 표, §13). 없다는 사실도 이 계보의 관측이다.

**표기 규칙** (이 위키 관례 3구분 + 1):
- `[인쇄]` — 논문 본문/식/표/그림 안에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (**원 데이터가 아니다**; `figure-read ≈`)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 원문 값을 이 세션에서 산술로 옮긴 것 (계산식을 함께 적는다)

> ⛔ **인용 금지.** 이 파일의 숫자는 **사본**이다. 인용 근거는 원문 PDF 이고,
> 우리 연구 수치의 정본은 artifact + `degradation-degeneracy/docs/RESULTS*.md` 다.
> 여기 적힌 수치를 논문·보고서에 옮기려면 원문을 다시 확인한다.
>
> ⚠ **모집단 경고.** 이 논문의 결론은 **탄소·바인더가 없는 2 성분(AM+SE) 복합양극의
> 정적(pristine) 기하 모형** 한 종류에서 나온 것이다. AM 은 겹치지 않는 **균일 크기 구**,
> SE 는 **3 µm 고정** 볼록다면체, 전극 단면 (80×80) µm², 두께 140 µm, 해상도 200 nm —
> 그 밖으로 옮기면 모집단이 다르다. **셀 실험이 0 개**이고, **사이클링·전압·용량이 없다.**

- 원본 파일: 로컬 업로드 PDF
  `01._Microstructural_Modeling_of_Composite_Cathodes_for_All-Solid-State_Batteries.pdf`
  (9 쪽, 2,998,096 bytes, PDF sha256
  `20b1cac28006e8fb27a9cd19cd80da0afada4db6b81e263628366d4bb1f98bc0`; 저장소에
  바이너리를 넣지 않는다). PDF 메타데이터의 `title` 은 `jp8b11043 1..9`,
  `creationDate` 2019-01-15.
- 크로핑 그림: `raw/figures/bielefeld2019_microstructural-modeling-assb-composite-cathode/`
  (fig 10 장 + tab 1 장). **본문 그림 10 장을 전부 Read 로 직접 봤다** (Fig. 1–10).
  Table 1 은 이미지가 아니라 PDF 텍스트로 읽었다. **Supporting Information 은 없다**
  (`Supporting Information` 문자열 0 회, ASSOCIATED CONTENT 절 자체가 없음).
- 페이지 참조는 PDF 페이지 1–9 = 저널 페이지 1626–1634 (PDF p1 = 1626).
- 본문 텍스트는 `pymupdf.get_text()` 로 추출했다. 원문이 **ﬀ·ﬁ 합자(ligature)** 를
  쓰므로 `effective` 를 그대로 검색하면 0 회가 나온다 — 이 digest 의 단어 세기는
  합자를 풀고 센 것이다.

---

# 원문에 없어서 확인이 필요한 것 (읽기 전에 먼저 본다)

| # | 공백 | 왜 문제인가 |
|---|---|---|
| G1 | **유효 전도도(S/cm)가 한 번도 계산되지 않는다.** `conductivit*` 는 18 회 나오지만 `S/cm` 은 **0 회**. 본문 스스로 `[인쇄, p7]` "diffusion lengths in the storage phase, tortuosity, and **resulting effective conductivities** … **are not explicitly treated in this study**". | 그런데 **초록은 유효 전자 전도도의 결과를 주장한다** (§10 불일치 1). 이 논문에서 실제로 계산된 양은 `θ`(이용률)·`A_spec`·`A_spec,a` **셋뿐**이다. |
| G2 | **셀 실험이 0 개.** 이 논문 자신의 측정값이 하나도 없다. 유일한 실험 대조는 Strauss et al.(ref 13) 과의 **정성 비교**이고, 그마저 `[인쇄, p6]` "the total packing density of AM used by Strauss et al. **is not known, as the porosity was not measured**" 로 스스로 무효화된다. | **검증(validation)이 없다.** `validat*` 0 회. 모델은 어떤 측정에도 맞춰지지 않았고 어떤 측정도 예측 검증되지 않았다. |
| G3 | **SE 입자 크기가 3 µm 로 고정**돼 있다 (Table 1). "입자 크기 효과" 는 AM 만 3→15 µm 로 움직인 것이다. | 크기비 `d_AM/d_SE` 가 1 → 5 로 함께 움직인다. 식 (8) 의 `p_c(d)` 가 **AM 절대 크기의 함수인지 크기비의 함수인지 이 자료로는 못 가른다** (교란). |
| G4 | **vol% → wt% 환산에 쓴 밀도가 인쇄돼 있지 않다.** "72/28 vol% ↔ 86/14 wt% for NMC-622 and LPS" 같은 문장이 세 번 나오는데 `ρ_AM`·`ρ_SE` 값이 없다. | 우리가 이 조성을 재사용하려면 밀도가 필요하다. `[재현]` 역산하면 `ρ_AM/ρ_SE ≈ 2.35–2.45` (§7.3) — 세 환산이 서로 **완전히 일치하지도 않는다**. |
| G5 | **"limitation"(전자/이온 제한) 의 판정 기준이 숫자로 정의되지 않는다.** Fig. 7·9 의 회색 영역 경계가 `θ` 의 어느 값에서 그어졌는지 본문에 없다. | Fig. 9 `[도표]` 에서 `θ_SE ≈ 87 %` 인 점이 "ionic … limitation" 으로 칠해져 있다. 임계가 95 % 인지 99 % 인지 모르면 **경계값(69/31·79/21·21 % 공극률)을 재현할 수 없다.** |
| G6 | **`p_c` 정의의 단위가 어긋난다.** `[인쇄, p5]` "the AM volume fraction at which the mean utilization level is at **40 vol%**" — 이용률은 무차원 비(%)이지 vol% 가 아니다. | 사소하지만 `p_c` 는 이 논문의 핵심 출력이고 그 정의문이다. 그리고 이 40 % 라는 문턱 자체가 **임의 선택**이며 감도 분석이 없다. |
| G7 | **오차 막대가 Fig. 4 와 Fig. 6 에만 있다.** Fig. 3·5·7·8·9·10 에는 없고, 본문은 전이 구간 **밖** 점들이 `[인쇄]` "one microstructure was computed for each AM fraction in sub- and super-critical regions" 라고 적는다 — **배열 1 개**. | 이 논문의 가장 많이 인용될 그림들(Fig. 7·8 의 최적 조성)이 **반복 없는 단일 실현**이다. Fig. 4 의 오차 막대 크기(§6.3)를 보면 그 단일 실현의 폭이 작지 않다. |
| G8 | **접촉 저항이 명시적으로 배제돼 있다.** `[인쇄, p4]` "These do not take into account possible resistances occurring at particle−particle interfaces and **constriction resistances**". | 따라서 `θ_AM` 은 **연결됐다/아니다의 이진 기하량**이고, 사용 가능한 AM 의 **상한**이다. 실제 이용 가능 용량은 이보다 작다. |
| G9 | **AM 입자 겹침이 고농도에서 1 %까지 간다.** `[인쇄, p3]` "In case of the highest AM volume fractions (around 65 vol%), the overlap reaches values of up to 1%". | "구는 겹치지 않는다" 는 모델 전제가 **포화 평탄부를 읽는 바로 그 지점에서** 깨진다. 전자 클러스터는 겹침이 있으면 더 잘 이어진다 → 고농도 `θ_AM` 이 **낙관 방향**으로 편향될 수 있다. |
| G10 | **시간축이 없다.** 사이클링·부피 변화·균열·접촉 상실의 **진행**을 모델링하지 않는다. `[인쇄, p8]` "real solid-state battery cells are a time-variant system … However, these issues are **beyond the scope of this study**". | 우리 물음은 **열화 중의 접촉 손실**이다. 이 논문은 **pristine 전극 한 장의 정적 기하**만 준다 (§13-1). |
| G11 | **데이터·코드 공개 없음.** GeoDict(Math2Market, Version 2018 SP 5) 상용 소프트웨어이고 스크립트·미시구조 파일이 제공되지 않는다. | 재현하려면 상용 라이선스가 필요하다. |
| G12 | **난수 시드·배열 생성 절차가 없다.** "10 random microstructures", "eight particle arrangements" 라고만. | Fig. 4·6 의 표준편차를 재현할 수 없다. |
| G13 | **`Aspec` 의 표면적 계산 방식이 없다** (voxel 표면적인지 marching-cube 인지). 200 nm voxel 로 3 µm 구를 표현하면 계단 표면이 생긴다. | 기하 상한(식 7)과의 비(比)를 우리가 재사용하려면 이 정의가 필요하다. Fig. 3 `[도표]` 는 상한의 85 % 에서 포화한다. |
| G14 | **AM 의 이온 전도도를 0 으로, SE 의 전자 전도도를 0 으로 놓는다** (`[인쇄, p3]` "about 5 to 6 orders of magnitude lower"). 참고문헌 하나(ref 35)뿐이고 이 논문에서 값이 인쇄되지 않는다. | 이진 배정이라 **혼합 전도 경로가 원리적으로 안 나온다.** |

---

## 0. 서지사항 (직접 확인)

`[인쇄]` PDF 헤더/푸터 및 저자 정보 블록:

| 항목 | 값 |
|---|---|
| 제목 | Microstructural Modeling of Composite Cathodes for All-Solid-State Batteries |
| 저자 | Anja Bielefeld *^,†,‡ · Dominik A. Weber ‡ · Jürgen Janek *^,†,§ |
| 소속 | † Physikalisch-Chemisches Institut, Justus-Liebig-Universität, 35392 Giessen, Germany · ‡ Volkswagen AG, Group Research, 38436 Wolfsburg, Germany · § Center of Materials Research (LaMa), Justus-Liebig-Universität |
| 교신 | anja.bielefeld@volkswagen.de (A.B.) · juergen.janek@phys.chemie.uni-giessen.de (J.J.) |
| ORCID | Bielefeld 0000-0003-2193-8375 · Janek 0000-0002-9221-4756 |
| 저널 | J. Phys. Chem. C **2019**, 123, 1626−1634 |
| DOI | 10.1021/acs.jpcc.8b11043 |
| 투고/수정/게재 | Received November 14, 2018 · Revised December 25, 2018 · Published December 31, 2018 |
| 자금 | "FELIZIA" 컨소시엄 (03XO0026G), 독일 BMBF |
| 이해관계 | `[인쇄]` "The authors declare no competing financial interest." (제1저자 소속이 폭스바겐이라는 점은 그 자체로 인쇄돼 있다) |
| 소프트웨어 | GeoDict (Math2Market GmbH), Version 2018 SP 5, 2018 (ref 30) |

`[해석]` Janek 그룹(Giessen) + VW 의 산학 공동 연구다. 이 그룹의 실험 논문
(Koerver et al. 2017, ref 7 — "Capacity Fade in Solid-State Batteries: … Chemomechanical
Processes in Nickel-Rich Layered Oxide Cathodes and Lithium Thiophosphate Solid
Electrolytes") 이 **접촉 손실의 실험 원전**으로 인용되고, 이 논문은 그 현상의
**기하학적 무대**를 만든다. 우리가 A1(접촉 손실)의 실험 근거를 찾을 때 다음 후보는
ref 7 이다.

---

## 1. 초록 — 무엇을 주장하는가

`[인쇄, 초록]` 요지 5 문장:

1. ASSB 성능이 제한되는 이유 중 하나가 **복합양극 안의 불충분한 이온·전자 퍼콜레이션**이다.
2. **3 차원 미시구조 모델링**으로 퍼콜레이션 특성을 조사하고, 잘 퍼콜레이팅하는
   네트워크의 **경계 조건**을 정의·이해하는 것이 목표다.
3. **구형 AM 입자 + 볼록다면체 SE** 로 이온·전자 전도 클러스터를 판정하고
   **퍼콜레이션 이론**으로 분석한다 — 조성·공극률·입자 크기·전극 두께를 바꿔 가며.
4. 결과: **작은 AM 입자가 유효 전자 전도도를 높이고**(표면적이 커서 연결 기회가 많다),
   **공극률이 이온·전자 전도 능력에 결정적**이다. 전극 두께의 영향은 **얇은 전극에서만**
   나타나며 거기서는 퍼콜레이션 효과가 억제되어 **유리한 전극 특성을 함의한다**.
5. 주어진 공극률·입자 크기에서 **이상적 조성**과 **설계 지침**을 도출한다.

`[해석]` **문장 4 가 이 논문에서 가장 위험한 문장이다.** (a) "유효 전자 전도도" 는
계산된 적이 없고(G1), (b) 두께 효과는 본문에서 **유한 크기 인공물(finite size effect)**
로 명시되는데 초록은 그것을 **"유리한 전극 특성"** 으로 뒤집는다 (§10 불일치 1).

---

## 2. 서론 — 이 논문이 서 있는 자리

`[인쇄, p1–p2]` 논증 순서:

1. **동기**: 통상 리튬이온전지가 에너지밀도·급속충전의 물리적 한계에 접근 중 → ASSB 가
   후보. 치밀하고 얇지만 덴드라이트에 안전한 **SE 분리막**으로 리튬 금속 음극을 쓰겠다는
   발상이 동력. SE 는 **단일 이온 전도체**(수송률 ≈ 1)라 벌크 분극이 사실상 없다 →
   고전류·급속충전 가능성.
2. **현실**: 100 °C 에서 18 C 로 안정 순환하는 황화물계 고출력 셀(ref 5)이 있음에도
   대부분의 연구에서 ASSB 성능은 매우 제한적이다.
3. **원인 목록** (서로 배타적이지 않다):
   - **복합양극 전반의 접촉 손실 — AM 의 사이클 중 부피 변화 때문.**
     `[인쇄]` "contact loss throughout the composite cathode occurs because of volume
     change of the active material (AM) during cycling, as was exemplarily shown for
     nickel-rich LiNi₀.₈Co₀.₁Mn₀.₁O₂ (NCM-811) and the sulfide-based SE β-Li₃PS₄ (LPS)" (ref 7)
   - SE/양극 계면의 **공간전하층**(ref 8)
   - **덴드라이트** 형성 / Griffith 결함을 따른 계면 결함 전파 (ref 9, 10)
   - 양극 내부의 **이온·전자 전도 제한** (ref 11, 12)
4. **액체셀과의 결정적 차이**: `[인쇄]` "Contrary to conventional battery cells, the
   **rigid SE does not necessarily adhere well to the surface of the AM**. This has to be
   taken into consideration already in the process of cathode manufacturing."
5. **선행 연구 정리** (전부 남의 실험):
   - AM 입자 크기 ↑ (최대 20 µm) → 전자 전도도 **급락**. 무탄소 NCM-622 + LPS (ref 13, Strauss)
   - 조성: AM/SE 부피비 ↑ → 유효 **전자** 전도도 ↑, 유효 **이온** 전도도 ↓.
     NCM-523 + Li₂S–P₂S₅ (ref 14, AC 임피던스)
   - 고 담지(최대 85 wt% AM) → 용량 ↓, 율특성 약화. NCM-622/argyrodite/Super C65/NBR
     (ref 11) — 폴리머 바인더와 적은 SE 분율이 원인으로 지목
   - LCO + LGPS 조성 변화(ref 12), LLTO 코팅 LCO + glass-ceramic LPS + Super P (ref 15)
   - **공극률**이 유효 이온 전도도·굴곡도에 유의한 영향. LCO + Li₂S–P₂S₅–LiI,
     EIS + FIB-SEM 재구성 + 수치 시뮬레이션 (ref 16)
   - **두꺼운 양극**(최대 600 µm)이 상온에서 동작 (ref 17, LPS/LGPS + LCO) — 수송률 ≈ 1 인
     SE 는 액체전해질과 달리 **염 농도 구배**를 만들지 않으므로 두꺼운 고에너지 양극이
     가능할 수 있다
6. **공백 선언**: `[인쇄]` "a **holistic approach** considering porosity, AM particle size,
   and size distribution, as well as composition and electrode thickness as parameters of
   interest, **has not been reported, both experimentally as well as theoretically or from
   a modeling perspective**."

`[해석]` 서론에 **접촉 손실이 원인 목록 1 번으로 등장하지만**, 이 논문의 모델은
그 현상을 **재현하지 않는다** — 부피 변화가 없기 때문이다(G10). 접촉 손실은
**동기(motivation)** 로만 쓰이고 **결과(result)** 로는 나오지 않는다. 이 구분이
Q1 답의 전부다 (§11).

---

## 3. METHODS — 퍼콜레이션 이론 (p2)

`[인쇄]` 출발점은 Lagadec et al. (ref 19): "**all electrochemical systems can be seen as
interwoven electronic and ionic networks, which have to be balanced at all length scales**".

### 3.1 알고리즘

`[인쇄]` 점유/비점유 격자를 만들고 한 **경계면에서 출발**해 이웃 점유 사이트를 클러스터에
붙여 나간다 — **Hoshen−Kopelman 알고리즘**(ref 22). 양쪽 경계를 잇는 클러스터를
**퍼콜레이팅 클러스터**라 한다.

`[인쇄, p3]` 출발 경계면이 무엇인지가 명시된다: **전자**의 경우 **집전체**에 완전히
연결된 면, **이온**의 경우 **SE 분리막**에 연결된 면.

`[해석]` 즉 두 클러스터의 **출발점이 서로 반대편**이다. 이것이 Fig. 10 의 두께 효과를
만든다 — 전자 클러스터는 집전체 쪽에서 자라므로 얇은 전극에서 "처음부터 연결된"
입자의 비중이 커진다 (§9).

### 3.2 임계 거동

`[인쇄]` 퍼콜레이션 임계 `p_c` = 퍼콜레이션이 처음 관측되는 **임계 점유 확률**.
`p < p_c` 를 subcritical, `p > p_c` 를 supercritical 상(相)이라 한다 (ref 21, Grimmett).
임계 바로 위에서 질서 변수는 멱법칙을 따른다:

> **식 (1)**  `Θ ∝ (p − p_c)^β`
> `Θ` = 질서 변수, `β` = 임계 지수(Grimmett 정의), `p` = 임계 근방 위쪽의 점유 확률.

`[인쇄]` 유한계에서는 통계적 변동 때문에 상전이가 **구간에 걸쳐 번진다**.
**무한계만이 잘 정의된 이산 임계값을 갖는다.**

`[해석]` 이 한 문장이 이 논문에서 우리에게 가장 값진 인식론적 진술이다 —
**`p_c` 는 유한 시료에서 점(point)이 아니라 폭(interval)이다.** 우리 계보의
"점추정 대신 폭" 논지([[near-optimal-set-width-measurement]])와 **같은 형태의 주장**이며,
여기서는 그 폭이 **측정 잡음이 아니라 무작위 충전 배열 자체**에서 온다 (§6.3).

### 3.3 왜 퍼콜레이션인가

`[인쇄]` "the application of percolation theory and the identification of conduction
clusters **may allow estimating** the effective ionic and electronic conductivity close to
the percolation threshold for **similar** microstructures." 그리고 임계값 자체도 중요한데,
고성능 ASSB 는 **양극(과 음극) 전반에서 이온·전자 전도가 셀 수명 내내** 유지돼야 하기 때문.

`[해석]` "may allow estimating" — **조건법**이다. 이 논문은 전도도를 추정하지 **않았다**(G1).

---

## 4. METHODS — 미시구조 모델링 (p2–p3)

### 4.1 설계 철학과 배제 목록

`[인쇄]` 목표는 "**가능한 한 단순하면서 현실적 복합양극을 대표**하는" 미시구조.
일반적 ASSB 복합양극은 **5 성분**(AM, SE, 도전재, 바인더, 공극)인데 (ref 11, Nam et al.),
이 연구는 **바인더와 도전재를 뺀다** — Strauss et al.(ref 13) 의 실험 구성과 같다.

`[인쇄]` 탄소를 빼는 실질적 이유: **카본 첨가제가 티오포스페이트 전해질과 접촉해
순환 중 분해 반응을 보인다** (ref 7, 23, 24).

`[인쇄]` AM 코팅(Li₅₆Nb₂₂Ta₂₂-oxide, Li₄Ti₅O₁₂, LiNbO₃, Li₂O–ZrO₂ 등, ref 25–29)은
**나노 두께이고 전하 수송이 충분해 퍼콜레이션 네트워크와 유효 전도도에 미치는 영향이
무시할 만하다**고 본다.

`[인쇄]` 결과적으로 **전자 전도는 오직 연결된 AM 입자만이 제공한다** — SE 는 단일 이온
전도체라 전자 전도도가 무시할 만하므로.

`[해석]` **무탄소 전제는 이 논문의 결론 전부를 지배한다.** 실제 복합양극에 카본이 있으면
전자 퍼콜레이션은 AM 크기와 거의 무관해지고, §6 의 `p_c(d)` 관계(식 8) 는 의미를 잃는다.
이 논문을 인용할 때 반드시 붙어야 할 조건이다.

### 4.2 기하 생성 (Fig. 1)

**Fig. 1 을 직접 봤다.** `[도표]` 3 단 흐름도: (위) 진남색 SE 하부구조 — "Convex polyhedra
with overlap"; (아래) 빨강 AM 하부구조 — "Spherical particles without overlap"; 두 개가
합쳐져 "Composite cathode (overlap assigned to AM)"; 마지막 칸에서 **이온(하늘색)·전자(노랑)
전도 클러스터**가 칠해진다. 각 3D 블록에 **20 µm 스케일바**가 있다. 맨 오른쪽 블록에서
노란색(전자 클러스터)이 **오른쪽 면에서 시작해 왼쪽으로 갈수록 성기어지고**, 왼쪽에는
연결 안 된 빨간 입자가 남아 있다 — 집전체 쪽에서 자라는 클러스터의 모습.

`[인쇄, p3]` 생성 절차:
- **AM**: 균일 입도(uniform size), **겹침 없음**. `[인쇄]` 균일 입도를 고른 이유는
  "**입자 크기 자체의 영향을 분포 설정의 교란에서 분리하기 위해**" 이며 저자들 스스로
  "even though leading to **oversimplification**" 이라고 적는다. 가우시안/이봉/삼봉 분포는
  입력 파라미터를 늘리므로 **후속 연구로 미룬다**.
- 입자는 **무작위 배치** → "none of the modeled microstructures looks like the other".
- 목표 고상 부피분율까지 채운 뒤 **겹침 제거**: 겹친 입자를 하나씩 주어진 거리 안에서
  이동시키고, 안 되면 그 입자에 대해 **10 회 반복**.
  결과 `[인쇄]` 대부분 **≈10⁻⁵ vol%** 까지 겹침을 줄였으나, **최고 AM 분율(≈65 vol%)에서는
  최대 1 %** (등구 최密충전 한계 74 % 에 가까워서). 비균일 분포를 넣으면 이 한계가
  더 높은 충전밀도로 밀린다.
- **SE**: **겹침을 허용한** 볼록다면체. 근거 `[인쇄]` 티오포스페이트의 **낮은 영률
  ≈25 GPa** (ref 32–34) 와 좋은 연성. SE 입자 크기 = **외접구 지름**.
- **합병**: 겹치는 부분을 **AM 에 배정**한다(AM 이 구형을 유지하도록). 그 결과 복합체 안
  SE 가 손실되므로 **미리 더 치밀한 SE 하부구조를 만들어 보상**한다 → 식 (5).

### 4.3 부피분율 정의 (식 2–5) — **인터페이스의 핵심**

> **식 (2)**  `φ = V_pore / V_total`   (공극률)
> **식 (3)**  `φ = 1 − (V_AM + V_SE)/V_total`
> **식 (4)**  `g^V_AM = (1 − φ)(1 − g^S_SE)`
> **식 (5)**  `g^V_SE = (1 − φ) g^S_SE / [ (1 − φ) g^S_SE + φ ]`
> **식 (9, p6)**  `g^S_AM = g^V_AM / (1 − φ)`

`[인쇄]` 표기 규약이 명시된다:
- 위첨자 **`V`** = **전체 구조 부피** 기준 (공극 포함)
- 위첨자 **`S`** = **고상만** 기준 — "**조성 표기에 직접 나타나는 것**"
  (즉 "72/28 vol%" 는 `g^S_AM/g^S_SE` 다)

`[인쇄]` 식 (5) 의 의미: "**SE 하부구조에서 전해질이 차지해야 하는 고상 부피분율**을
계산한다. SE 하부구조를 만드는 시점에는 AM 이 아직 없지만 나중에(합병에서) SE 하부구조의
일부를 잡아먹으므로, 최종적으로 원하는 조성/공극률이 달성되도록."

`[재현]` 식 (5) 의 분모는 `(1−φ)g^S_SE + φ = 1 − (1−φ)g^S_AM = 1 − g^V_AM` 이다 (식 4 사용).
즉 식 (5) 는 **"AM 이 아닌 부피"에 대한 SE 비율**이고, 이것이 SE 하부구조를 얼마나
치밀하게 만들어야 하는지를 준다. **자체 일관적이다.**

`[해석]` ⚠ **표기 충돌 하나.** 논문 스스로 "위첨자 V = 전체 구조 부피 기준" 이라고 정의해
놓고, 식 (5) 의 좌변에 `g^V_SE` 를 쓴다. 그런데 식 (5) 의 출력은 **전체 부피 기준이 아니라
SE 하부구조(= AM 이 아닌 부피) 기준**이다. 전체 부피 기준이라면 단순히 `(1−φ)g^S_SE`
여야 한다. 본문 산문은 올바르게 설명하지만 **기호가 정의를 배반한다.** 이 식을 코드로
옮길 때 걸린다 — 우리가 인터페이스로 쓸 때 주의 (§12).

### 4.4 Table 1 — 입력 파라미터 (PDF 텍스트로 읽음, 이미지 아님)

| parameter | value |
|---|---|
| microstructure dimensions | **(80 × 80 × 140) µm³** |
| resolution | **0.2 µm/voxel** |
| shape of AM | spherical |
| particle size of AM | **{3, 4, 5, 6, 7, 8, 9, 10, 15} µm** |
| particle size distribution of AM | uniform |
| shape of SE | convex polyhedra |
| **particle size of SE** | **3 µm** (고정) |

`[인쇄, p3]` 두께 140 µm 를 고른 이유: "**미래 고체전지 기술의 요구를 반영하는 두꺼운
전극**을 모델링하기 위해"; 해상도 200 nm 는 "3 µm 까지의 입자 크기를 모델링하기에 합리적".

`[재현]` 격자 크기: 400 × 400 × 700 voxel = **1.12 × 10⁸ voxel**.
3 µm 구 = 15 voxel 지름 (부피 ≈ 1767 voxel).
`[해석]` 15 voxel 지름은 표면적 계산에 계단 오차를 남긴다 (G13). 그리고 SE 가 3 µm 고정이라
**SE 도 15 voxel** — SE 다면체의 형상 표현이 거칠다. 논문은 이 수치 오차를 논하지 않는다.

---

## 5. RESULTS — 출력량의 정의 (p4)

### 5.1 이용률 (식 6) — **우리에게 가장 중요한 식**

> **식 (6)**  `θ = V_c / V_ν`

`[인쇄]` "A comparison of the volume fraction of both solid components allows computing the
**utilization level**, which … indicates the ratio of **the volume of AM that is assigned to
the conduction cluster** and the volume of AM that is not part of the cluster and therefore
**lost in terms of battery performance**."
아래첨자 `c` = 클러스터(이온 또는 전자), `ν` = 고상 성분(AM 또는 SE).

`[해석]` ⚠ **산문과 식이 어긋난다.** 산문은 "클러스터에 속한 부피와 **속하지 않은** 부피의
**비(ratio)**" 라고 말하지만, 식 (6) 은 `V_c/V_ν` — **클러스터 부피 / 그 성분의 전체 부피**다.
그림들(Fig. 3·5·7·9)에서 `θ` 가 **100 % 로 포화**하는 것이 식 (6) 이 맞다는 증거다
("속하지 않은 부피" 가 분모면 발산한다). **식을 믿고 산문을 버린다.**
→ **`θ_AM ∈ [0, 1]` = 퍼콜레이팅 전자 클러스터에 속한 AM 부피 분율** (§10 불일치 2).

**그리고 이것이 우리가 찾던 양이다.** 닻 질문의 A1(접촉 손실)이 "물질은 그대로인데 용량이
준 것처럼 보인다" 라면, 그 "보이는 용량" 은 `Q_apparent = θ_AM · Q_material` 이다.
`θ_AM` 은 **재료량이 아니라 기하량**이고, 이 논문은 그것을 (조성, 공극률, 입자 크기)의
함수로 계산한다.

### 5.2 비표면적과 활성 계면적

`[인쇄]` `A_spec` — 구조 부피에 대한 **비표면적**, 단위 **m²/m³**. 이온 클러스터 또는 전자
클러스터에 대해 따로 계산하거나, 둘 **사이**의 **활성 계면적 `A_spec,a`** 로 계산할 수 있다.

`[인쇄]` "**the active interface area is the area available for intercalation of lithium ions
into the AM and should be maximized** to assure high energy and power density."

`[해석]` `A_spec,a` = **이온 클러스터에 속한 SE 와 전자 클러스터에 속한 AM 이 서로 맞닿은
면적**. 즉 "리튬이 실제로 드나들 수 있는 면적". `θ_AM` 이 **열역학적 용량**(얼마나 많은 AM 이
쓰이는가)에 대응한다면 `A_spec,a` 는 **동역학**(얼마나 빨리)에 대응한다. 이 논문은 두 축을
모두 출력하지만 **둘 다 전압으로 번역하지 않는다.**

### 5.3 명시된 배제

`[인쇄]` "these do not take into account possible resistances occurring at particle−particle
interfaces and **constriction resistances** which reflect the fact, that electric contacts have
to be regarded as a large number of interacting microcontacts" (ref 36).

`[해석]` 따라서 `θ_AM` 은 **상한**이다 (G8). 실제 셀에서 "연결됐지만 저항이 너무 큰" AM 은
이 모델에서 100 % 이용률로 계산된다.

---

## 6. RESULTS — 전자 전도 (p4–p6)

### 6.1 Fig. 2 — 입자 크기 3 종의 육안 비교

**Fig. 2 를 직접 봤다.** `[도표]` 3 개 3D 블록, 전부 **AM 55 vol%**, 왼→오 `d = 5, 10, 15 µm`.
노랑 = 전자 클러스터, 빨강 = 연결 안 된 입자. **5 µm: 거의 전부 노랑** (빨간 점 산발).
**10 µm: 노랑과 빨강이 대략 반반**, 노랑이 오른쪽(집전체 쪽)에 몰려 있다.
**15 µm: 거의 전부 빨강**, 오른쪽 면 일부만 노랑 — 퍼콜레이팅 클러스터가 없다.
20 µm 스케일바 있음.

`[인쇄]` "The electronic cluster **percolates well for the small particles**, whereas
medium-sized particles involve a smaller utilization level of AM and **the large particles do
not feature a percolating cluster, at all**."

`[해석]` 그림이 본문과 정확히 일치한다. 그리고 15 µm 블록에서 노란색이 **오른쪽 경계면에만**
붙어 있는 것이 §3.1 의 "경계면에서 출발" 알고리즘을 시각적으로 확인해 준다.

### 6.2 Fig. 3 — 5 µm 에서의 퍼콜레이션 전이

**Fig. 3 을 직접 봤다.** `[도표]` 좌: `Utilization level (%)` vs `Volume fraction of active
material (vol%)`, x ∈ [40, 66]. 우: `A_spec (10⁵ m²/m³)` 같은 x, 점선 = "geometrical limit".

`[도표]` 좌 패널 읽은 값 (figure-read ≈):
| AM (vol%) | 40 | 45 | 47 | 48 | 49 | 50 | 51 | 52 | 55 | 60 | 66 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| θ_AM (%) | ≈3 | ≈5 | ≈4.5 | ≈16 | ≈25 | ≈48 | ≈71 | ≈81 | ≈94 | ≈100 | ≈100 |

`[도표]` 우 패널: 40 → ≈0.15×10⁵, 50 → ≈2.8×10⁵, 52 → ≈4.3×10⁵, 60 → ≈6.7×10⁵,
66 → ≈6.75×10⁵ m²/m³. 점선(기하 상한)은 40 에서 ≈4.8×10⁵, 66 에서 ≈7.95×10⁵.

> **식 (7)**  `A_spec,geo = g^V_AM · A_sphere / V_sphere = 6 g^V_AM / d`

`[재현]` 식 (7) 검산: `d = 5 µm`, `g^V_AM = 0.40` → `6×0.40/5e-6 = 4.80×10⁵ m²/m³`;
`g^V_AM = 0.66` → `7.92×10⁵ m²/m³`. **`[도표]` 로 읽은 점선(≈4.8 / ≈7.95)과 일치한다.**
→ 식 (7) 과 Fig. 3 우측 점선은 서로 검증된다.
`[재현]` 포화점에서 데이터/상한 = `6.75/7.92 ≈ 0.85` — **기하 상한의 85 % 에서 포화**
(나머지 15 %: 격리 입자 + voxel 표면 표현 + 겹침 처리).

`[인쇄]` 본문 서술:
- 48 vol% 미만: 두 값 모두 매우 낮다 → 입자가 잘 연결 안 되고 클러스터가 미시구조 깊이
  들어가지 못한다.
- **45 vol% 의 작은 교란(perturbation)** 은 그 점들이 **배열 1 개**에 기반하기 때문이다.
- **48–52 vol% 의 전이 구간**에서는 각 분율마다 **무작위 미시구조 10 개**를 계산했다.
- `[인쇄, 핵심]` "**Depending on the random packing, some arrangements percolate with AM
  utilization levels around 70 %, while others, at the same AM fraction, do not percolate and
  therefore exhibit utilization levels around 30 %.**"
- 52 vol% 위에서는 기울기가 줄고 둘 다 포화 수준에 도달, 비표면적은 기하 상한(식 7)에
  가까워지며 "only few particles remain isolated".

`[해석]` ★ **이 논문에서 우리에게 가장 중요한 한 문장이 위 인쇄 구절이다.**
**거시 파라미터(조성·공극률·입자 크기)를 전부 고정해도, 무작위 충전 배열만 바꾸면
`θ_AM` 이 ≈30 % 와 ≈70 % 사이에서 이봉(bimodal)으로 갈린다.** 폭이 **≈40 %p**.
→ DEM 이 주는 "독립 라벨" 도 **점이 아니라 폭을 갖는다**. 그것도 잡음이 아니라
**기하학적으로 불가피한** 폭이다 (§13-3).

`[도표]` 다만 Fig. 3 좌 패널에는 **오차 막대가 없다** — 전이 구간 10 배열의 **평균**만
찍혀 있다. 위 문장이 말하는 이봉성은 **그림에서 보이지 않는다.** (G7 · §10 불일치 3)

### 6.3 Fig. 4 — 멱법칙 검증과 오차 막대

**Fig. 4 를 직접 봤다.** `[도표]` log–log, x = `p − p_c (vol%)` ∈ {1,2,3,4,5},
y = `A_spec (10⁵ m²/m³)` ∈ [1, 3.x]. 빨간 점 + 오차 막대 + 점선 맞춤.

`[인쇄, 그림 범례 안]` **`A_Spec(p − p_c) = 1.73·10⁵ ((p − p_c)/vol%)^0.41 m²/m³`**

`[인쇄, 본문]` `d = 10 µm`, **각 충전밀도마다 8 개 배열**, 오차 막대는 **표준편차**.
`[인쇄]` 임계 지수 **0.41** 이 Sur et al.(ref 37) 의 단순입방 격자 3D site-percolation 연구와
"in good agreement" → 멱법칙 적용 가능. 입자 크기는 **임의로 골랐고**(arbitrarily chosen),
연구된 모든 입자 크기에 멱법칙이 적용될 것으로 **기대한다**.

`[도표]` 데이터 점과 오차 막대 (figure-read ≈, ×10⁵ m²/m³):
| p − p_c (vol%) | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 평균 | ≈1.7 | ≈2.4 | ≈2.82 | ≈3.05 | ≈3.17 |
| 표준편차 범위 | ≈1.1 – 2.2 | ≈2.07 – 2.72 | ≈2.67 – 3.0 | ≈2.95 – 3.17 | ≈3.10 – 3.25 |

`[해석]` **임계 바로 위(`p − p_c = 1 vol%`)에서 표준편차가 평균의 ≈±32 %다.**
8 개 배열만으로. 임계에서 멀어질수록(`p−p_c = 5`) ≈±2 % 로 줄어든다.
→ **"임계 근방에서 예측이 흐려진다"가 이 논문 안에서 정량돼 있다.** 이것은
우리가 근최적 집합 폭을 재는 이유와 **같은 구조의 진술**이다.
`[해석]` 그리고 **이 논문에서 오차 막대가 있는 그림은 Fig. 4 와 Fig. 6 둘뿐이다.**
가장 많이 인용될 Fig. 7·8(최적 조성)에는 없다 (G7).

### 6.4 Fig. 5 — 입자 크기 3–15 µm 전수

**Fig. 5 를 직접 봤다.** `[도표]` 좌 `Utilization level (%)`, 우 `A_spec (10⁵ m²/m³)`,
둘 다 vs AM vol% ∈ [40, 66]. 범례 9 개: 3, 4, 5, 6, 7, 8, 9, 10, 15 µm (진남색 → 연두 그라데이션).
점선으로 이은 산점.

`[인쇄]` 전이 구간 밖은 **배열 1 개**, 전이 구간은 **10 개**.
`[인쇄]` "the transition region of **3 µm** particles is located within the interval of
**41−46 vol%**, it shifts toward higher fractions up to the interval of **52−57 vol%** for
**15 µm**-sized particles. **The steepness of the transition region is similar for all particle
sizes.**"
`[인쇄]` "the smaller the particles, the higher the specific surface area gets."

`[도표]` 우 패널 포화값 (66 vol% 부근, ×10⁵ m²/m³):
3 µm ≈10.6 · 4 µm ≈8.3 · 5 µm ≈6.75 · 6 µm ≈5.7 · 7 µm ≈5.0 · 8 µm ≈4.4 ·
9 µm ≈3.9 · 10 µm ≈3.5 · 15 µm ≈2.4.

`[재현]` 식 (7) 상한 (66 vol%): 3 µm → 13.2×10⁵; 15 µm → 2.64×10⁵.
→ 데이터/상한 = **3 µm 에서 0.80, 15 µm 에서 0.91**.
`[해석]` 작은 입자일수록 상한에서 더 멀다 — voxel 표현(3 µm = 15 voxel)과 격리 입자가
작은 입자에서 더 큰 비중을 차지한다는 뜻일 수 있다. 논문은 이 비를 논하지 않는다.

`[도표]` 좌 패널에서 곡선들이 **단조롭지 않다** — 예컨대 9 µm(올리브)와 15 µm(연연두)
곡선이 52–57 vol% 구간에서 서로 교차하고 국소적으로 내려갔다 올라간다.
`[해석]` 배열 1 개 기반 점들의 무작위 변동이다(§6.2 의 "45 vol% 교란"과 같은 원인).
오차 막대가 없어 **어느 교차가 실재이고 어느 것이 잡음인지 그림만으로 판별 불가.**

### 6.5 Fig. 6 · 식 (8) — `p_c(d)` 로그 법칙

**Fig. 6 을 직접 봤다.** `[도표]` x = `Particle size d (µm)` ∈ [3, 15] (선형축),
y = `Percolation threshold p_c (vol%)` ∈ [44, 58]. 빨간 점 + 오차 막대 + 점선 맞춤.

`[인쇄, 그림 범례 안]` **`p_c = [7.83 ln(d/µm) + 36.67] vol%`** — 본문 **식 (8)** 과 동일.

`[인쇄]` `p_c` 정의: "**the AM volume fraction at which the majority of the 10 arrangements
features a percolating cluster. This corresponds to the AM volume fraction at which the mean
utilization level is at 40 vol%.**"

`[도표]` 데이터 점 (figure-read ≈, vol%), 오차 막대 대략 ±1 vol%:
| d (µm) | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 15 |
|---|---|---|---|---|---|---|---|---|---|
| p_c (도표) | ≈44 | ≈48 | ≈50 | ≈51 | ≈52 | ≈53 | ≈54 | ≈55 | ≈57 |
| `[재현]` 식 (8) | 45.27 | 47.52 | 49.27 | 50.70 | 51.91 | 52.95 | 53.87 | 54.70 | 57.87 |

`[해석]` 맞춤은 대체로 좋지만 **`d = 3 µm` 에서 식 (8) 값 45.27 이 데이터 점(≈44)의 오차
막대 위끝(≈45)을 넘어선다** — 그림에서 점선이 그 점 위로 지나가는 것이 보인다.
캡션은 "fitted by a logarithmic function, which represents the data **sufficiently accurate**"
라고만 한다. **가장 작은 입자, 즉 실무에서 가장 관심 있는 쪽에서 맞춤이 가장 나쁘다.**
(figure-read 기반 판단이므로 원문 수치표가 있으면 재확인 필요 — 수치표는 없다.)

`[해석]` 그리고 `p_c` 정의의 "40 %" 문턱은 **임의**다 (G6). 문턱을 30 % 나 50 % 로 잡으면
`p_c(d)` 곡선 전체가 평행이동하고 식 (8) 의 상수 36.67 이 바뀐다. 감도 분석 없음.

### 6.6 실험과의 대조 (p6)

`[인쇄]` "These findings **correlate well** with the observation of high fractions of
**inactive NCM-622 for large AM particle sizes, measured via ex situ X-ray diffraction** and
with their attributed low effective electronic conductivity studied by Strauss et al.(ref 13)"

`[인쇄, 즉시 이어서]` "**Unfortunately, the total packing density of AM used by Strauss et al.
is not known, as the porosity was not measured.**"

`[해석]` ★ **이 두 문장이 붙어 있는 것이 이 논문의 정직한 자리이자 치명적 자리다.**
Strauss 의 XRD "inactive fraction" 은 원리적으로 **`1 − θ_AM` 의 measured 라벨**이다 —
액체셀 계열에서 우리가 그토록 찾던 종류의 **재료 수준 독립 관측**이다. 그런데
**공극률을 안 재서 x 축을 맞출 수 없다.** 정량 대조가 불가능하고, 이 논문은 그림도
표도 없이 "correlate well" 한 마디로 끝낸다.
→ **후속 후보 1 순위: Strauss et al., ACS Energy Lett. 2018, 3, 992−996** (ref 13).
거기에 `1 − θ_AM` 의 measured 값이 있다.

`[인쇄, 소결론]` 무탄소 복합양극의 유효 전자 전도는 AM 충전밀도와 크기에 크게 의존한다.
치밀한 충전이 접촉을 긴밀하게 하고 연결성을 높인다. 작은 입자는 낮은 충전밀도에서도 높은
이용률을 가능하게 해 **높은 공극률을 보상**할 수 있으나, 큰 표면적은 `[인쇄]` "vulnerable
for chemical degradation and formation of passivating cathode/electrolyte interfacial layers
upon charging (ref 7), which may result in performance decrease."

`[해석]` 즉 **작은 입자의 이득에 화학적 대가**가 붙는다는 것을 논문이 스스로 적는다 —
그러나 그 대가는 모델에 들어 있지 않다. 초록의 "small AM particles turn out to enhance …"
는 이 단서 없이 읽힌다.

---

## 7. RESULTS — 이온 전도 (p6–p7)

### 7.1 설정과 식 (9)

`[인쇄]` 이후 계산은 전부 **`d = 5 µm`** 로 고정 — 앞 절에서 작은 입자가 유리했고
Strauss et al. 에 따르면 5 µm 가 NCM 입자로 **현실적**이기 때문.

`[인쇄]` "the cathode composition and its porosity are **not well-defined for a given total
fraction of AM**" → 두 경우로 나눈다: **(A) 공극률 고정 · 조성 변화**, **(B) 조성 고정 ·
공극률 변화**.

> **식 (9)**  `g^S_AM = g^V_AM / (1 − φ)`

`[해석]` ★ **이 한 문장("주어진 총 AM 분율에 대해 조성과 공극률이 유일하게 정해지지
않는다")이 이 논문 안의 유일한 비유일성 진술이다.** `(g^S_AM, φ)` 두 자유도가 `g^V_AM`
하나로 접힌다 — 즉 **총 AM 분율만으로는 미시구조가 결정되지 않는다.** 이 논문은 이것을
"연구 설계를 두 갈래로 나누는 이유" 로만 쓰고, **역문제로 보지 않는다** (Q4, §11).

### 7.2 Fig. 7 — 공극률 20 % 고정, 조성 스캔

**Fig. 7 을 직접 봤다.** `[도표]` 두 패널 모두 **아래 x축 = `Total fraction of active
material (vol%)`** ∈ [40, 68], **위 x축 = `Composition AM/SE (vol%)`** (50/50, 60/40, 70/30,
80/20 눈금). 좌: `Utilization level (%)`, 남색 = Active material, 자주 = Solid electrolyte.
**회색 음영 2 개**: 왼쪽 "electronic limitation", 오른쪽 "ionic limitation", 가운데 흰 띠.
우: `A_spec,a (10⁵ m²/m³)` 올리브색 점.

`[재현]` 두 x 축의 관계 확인: 식 (9) 로 `g^S_AM = g^V_AM/(1−0.2)`.
총 55 vol% → `55/0.8 = 68.75` ≈ **69/31**; 총 63 vol% → `63/0.8 = 78.75` ≈ **79/21**;
총 57.6 vol% → `72/28`. **아래 축과 위 축이 서로 일관된다.**

`[도표]` 좌 패널 읽은 값 (figure-read ≈):
| 총 AM (vol%) | 40 | 45 | 47 | 48 | 49 | 50 | 51 | 52 | 55 | 60 | 65 | 68 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| θ_AM (%) | ≈3 | ≈5 | ≈4.5 | ≈5.5 | ≈22 | ≈63 | ≈64 | ≈78 | ≈94 | ≈100 | ≈100 | ≈100 |
| θ_SE (%) | ≈100 | ≈100 | ≈100 | ≈100 | ≈100 | ≈99 | ≈99 | ≈99 | ≈99 | ≈99 | ≈98 | **≈87** |

`[도표]` 음영 경계: "electronic limitation" 은 40 → **≈55**, "ionic limitation" 은
**≈63** → 68. 우 패널 `A_spec,a` 최대 **≈3.38×10⁵ m²/m³ at 총 ≈57–58 vol%**,
50 vol% 에서 ≈2.2×10⁵, 68 vol% 에서 ≈2.1×10⁵.

`[인쇄]` "While electronic conduction is the limiting factor at compositions **below 69 vol%
AM and 31 vol% SE (69/31 vol%)**, ionic conduction becomes restricting at high AM fractions
and compositions **above 79/21 vol%**. Accordingly, **the interval of well-performing
composites is fairly small.**"
`[인쇄]` "an **optimal composition can be identified at 72/28 vol% which corresponds to
86/14 wt% for NMC-622 and LPS**."
`[인쇄]` "Even though designed to overlap in the model, the SE does not suffice to build
well-connected ionic conduction clusters in highly AM-dominated microstructures."

`[해석]` 그림과 본문이 **정량적으로 일치한다** (69/31 ↔ 총 55, 79/21 ↔ 총 63, 72/28 ↔ 총 57.6
= `A_spec,a` 봉우리). 이 절은 이 논문에서 가장 견고하다.
`[해석]` 다만 **"ionic limitation" 판정 기준이 여전히 없다** (G5): 총 63 vol% 에서
`θ_SE` 는 `[도표]` ≈99 % 다. 68 vol% 에서야 87 % 로 떨어진다. 그런데 음영은 63 에서
시작한다 → 기준은 `θ_SE` 가 아니라 **`A_spec,a` 가 봉우리에서 내려오기 시작하는 지점**
이거나, 논문에 안 적힌 다른 양이다.
`[해석]` **"좋은 조성 구간이 꽤 좁다"** 는 진술을 뒤집으면: **`A_spec,a` 봉우리는 넓고
평평하다**. `[도표]` 총 54–62 vol% 구간에서 `A_spec,a` 가 3.0–3.38 사이 (봉우리의 89 % 이상).
→ **`A_spec,a` 를 관측으로 삼아 조성을 역추정하면 ±4 vol% 는 못 가른다** (§13-4).

### 7.3 Fig. 8 — 공극률 5 / 10 / 20 % 비교

**Fig. 8 을 직접 봤다.** `[도표]` x = `Composition AM/SE (vol%)` (40/60 → 90/10),
y = `A_spec,a (10⁵ m²/m³)` ∈ [0, 6]. 세 색: 진남 5 %, 자주 10 %, 올리브 20 %.
**오른쪽 위에 회색 삼각 영역** — 대각선 라벨 "**closest packing limitation**".

`[도표]` 봉우리: 5 % → ≈5.85×10⁵ (x ≈ 62/38–65/35 사이, **평탄**);
10 % → ≈5.03×10⁵ (x ≈ 65/35–66/34); 20 % → ≈3.38×10⁵ (x ≈ 70/30–72/28).

`[인쇄]` "an optimal composition is reached at **62/38 vol% (80/20 wt% for NMC-622 and LPS)
for 5 % porosity**, whereas **10 % porosity features an optimal composition of 66/34 vol%
(82/18 wt%)**." (20 % → 72/28 = 86/14 wt%, §7.2)
`[인쇄]` "Apart from the shift of the optimal composition toward higher AM fractions for
rising porosity, **the ionic conduction limitation gains importance for higher porosities**:
the drop at compositions above the optimum is more pronounced at a porosity of 20 % compared
to 5 and 10 %."
`[인쇄]` "As small porosities go along with high packing density and high mass loading, the
active interfaces are significantly higher for 5 % porosity than for 10 or 20 %."

`[재현]` **밀도 역산** (G4). `wt%_AM = g^S_AM ρ_AM / (g^S_AM ρ_AM + g^S_SE ρ_SE)` 에서
`r = ρ_AM/ρ_SE` 를 풀면:
| 조성 (vol%) | 인쇄된 wt% | `[재현]` r |
|---|---|---|
| 72/28 | 86/14 | **2.389** |
| 62/38 | 80/20 | **2.452** |
| 66/34 | 82/18 | **2.347** |
→ 세 환산이 **서로 4 % 어긋난다.** 단일 `r` 로는 세 값을 동시에 못 맞춘다 (반올림 탓일
가능성이 크다). `r ≈ 2.4` 는 NCM-622(≈4.7–4.8 g/cm³) / LPS(≈1.9–2.0 g/cm³) 와 정합적이나,
**밀도값 자체는 논문에 없다.** 우리가 이 조성을 재사용하려면 `r` 을 명시해야 한다.

`[해석]` ⚠ **표기 불일치**: 이 절부터 "**NMC**-622" 라고 쓴다. 서론·§6 은 "**NCM**-811",
"**NCM**-622" 다. 같은 논문 안에서 NCM/NMC 가 섞인다 (§10 불일치 5).
`[해석]` `[도표]` 5 % 곡선의 봉우리가 인쇄된 62/38 보다 **오른쪽으로 보인다**(≈63–65).
봉우리가 평탄해서 그림에서 단정할 수 없다 — **그것 자체가 요점**이다 (§13-4).

### 7.4 Fig. 9 — 조성 70/30 고정, 공극률 스캔 (치밀화)

**Fig. 9 를 직접 봤다.** `[도표]` 아래 x = `Total fraction of active material (vol%)`
∈ [40, 68], **위 x = `Porosity (%)`** (40, 30, 20, 10 눈금, **오른쪽으로 갈수록 감소**).
좌: `Utilization level (%)`, 남색 AM · 자주 SE. **음영 2 단**: 진한 회색
"ionic and electronic limitation"(40 → ≈46), 연한 회색 "electronic limitation"(≈46 → ≈55).
우: `A_spec,a (10⁵ m²/m³)` ∈ [0, 6.2].

`[재현]` 위 축 검산: 조성 70/30 이면 `g^V_AM = 0.70(1−φ)` → `φ = 1 − g^V_AM/0.70`.
총 40 → `φ = 42.9 %`; 총 46 → `φ = 34.3 %`; 총 55 → `φ = 21.4 %`; 총 68 → `φ = 2.9 %`.
**본문의 "43 % → 3 %", "above 34 %", "down to 21 %" 와 정확히 일치한다.**

`[인쇄]` "Figure 9 shows the percolation properties for porosities **from 43 % down to 3 %**
at a composition of 70/30 vol%. … **high porosities above 34 %** are accompanied by ionically
and electronically isolated regions in the cathode. The active interface is negligible in this
section and **increases for porosities below 30 %**. **Down to 21 % porosity, the electronic
limitation is still present, but below this value, the cathodes ought to perform well.**"
`[인쇄]` "The behavior of the active interface area in Figure 9 is **not as significant** as in
the case of constant porosity because a lowering of porosity goes along with densification …
The reader may bear in mind that **the active interface area is not normalized with respect to
porosity but with respect to the electrode volume.**"

`[도표]` 좌: `θ_AM` 은 40 →≈3 %, 48 →≈5 %, 49 →≈22 %, 50 →≈63 %, 55 →≈94 %, 57 이상 ≈100 %.
`θ_SE` 는 40 →**≈87 %**, 45 →≈95 %, 47 이상 ≈97–100 %.
우: `A_spec,a` 가 49 vol%(φ ≈ 30 %)부터 상승해 **단조 증가**, 68 vol%(φ = 3 %)에서 ≈6.1×10⁵.
봉우리가 **없다** (Fig. 7·8 과 달리).

`[해석]` 좌 패널의 `θ_SE ≈ 87 %` 점(총 40 vol%, φ ≈ 43 %)이 "ionic and electronic
limitation" 영역의 근거다 — **`θ_SE` 가 100 % 에서 13 %p 떨어진 것으로 "이온 제한" 판정.**
Fig. 7 에서는 총 68 vol% 에서 똑같이 `θ_SE ≈ 87 %` 이고 거기서도 "ionic limitation" 이다.
→ `[해석]` **기준은 대략 `θ_SE ≲ 90 %` 로 보인다**(두 그림 공통). 그러나 **어디에도 인쇄돼
있지 않다** (G5). 우리가 쓰려면 직접 정해야 한다.
`[해석]` `A_spec,a` 가 단조 증가한다는 것은 **"공극률은 낮을수록 좋다"** 가 이 모델 안에서
**무조건**임을 뜻한다 — 압력·제조 한계가 모델에 없으므로 (Q6, §11).

### 7.5 실무 처방 (결론 절에서)

`[인쇄, p8]` "**Although not provided in many studies (ref 5, 7, 11−15, 17), the porosity has
shown to be an important property** … we **strongly propose for future experimental studies to
take the impact of porosity into account. It is worthwhile to make the effort and measure or
calculate this important characteristic for the sake of comparability between experimental
studies.**"
`[인쇄]` 저공극 제조의 선례로 Kim et al.(ref 42): 황화물 SE 를 통상 LCO·흑연 전극에
**침투(infiltrate)** 시켜 공극률 **≈6–8 %** 달성.

`[해석]` ★ **"이 계보의 논문들이 공극률을 보고하지 않는다" 는 전수 관측을 저자들이
직접 적었다** (인용 목록까지 붙여서: ref 5, 7, 11–15, 17 = **8 편**).
이것은 우리 위키의 [[mode-identifiability-unmeasured-lineage]] 가 액체셀 17 편에 대해
"유일성을 잰 논문 0 편" 을 적은 것과 **형식이 완전히 같은 관측**이다 —
**"모두가 보고하지 않는 필수 변수" 를 저자가 세어서 인쇄한 것.**

---

## 8. RESULTS — 전극 두께 (p7)

### 8.1 설정

`[인쇄]` 질문: "**how thick can an electrode get that performs well, even at higher C rates?**"
(ref 38, 39). 그리고 곧바로 **범위를 스스로 좁힌다**:
`[인쇄]` "Percolation represents **one** important aspect … but **diffusion lengths in the
storage phase, tortuosity, and resulting effective conductivities play an additional role in
thick electrodes and are not explicitly treated in this study.**"

`[인쇄]` 방법: 이미 만든 **140 µm 배열을 잘라서** 두께를 바꾼다 ("the initially created
particle arrangements of 140 µm thickness were **cut** at different thicknesses **between 20
and 120 µm**"). 공극률 20 %, `d = 5 µm`.

### 8.2 Fig. 10

**Fig. 10 을 직접 봤다.** `[도표]` 제목 "**Electrode thickness**". 아래 x = `Total fraction
of active material (vol%)` ∈ [40, 68], 위 x = `Composition AM/SE (vol%)`.
y = `A_spec,a (10⁵ m²/m³)` ∈ [0, 3.5]. **범례 7 개: 20, 40, 60, 80, 100, 120, 140 µm.**
오른쪽에 미시구조 2 개 — 위 `l = 20 µm`(초록 테), 아래 `l = 140 µm`(주황 테), 파란 화살표로 연결.

`[도표]` 읽은 구조:
- **총 ≈52 vol% 위에서 7 개 곡선이 사실상 완전히 겹친다.** 공통 봉우리
  ≈**3.38×10⁵ m²/m³ at 총 ≈58 vol%**, 68 vol% 에서 ≈2.1×10⁵ 로 함께 하강.
- **총 50 vol% 아래에서만 갈린다**: 45 vol% 에서 20 µm ≈**1.19**×10⁵ vs 140 µm ≈**0.2**×10⁵
  (`[재현]` 약 **6 배**). 두께가 얇을수록 위로 올라가며 순서가 단조롭다
  (20 > 40 > 60 > 80 > 100 ≈ 120 ≈ 140).
- 총 50 vol% 부근에 20 µm 곡선의 뾰족한 국소 봉우리(≈2.65×10⁵)가 있다.

`[인쇄]` 해석: 전자 클러스터의 **출발점이 집전체 쪽**이라, 얇은 전극에서는 "처음부터
연결된 입자" 가 전체에서 차지하는 비중이 크다 → 낮은 AM 분율에서도 `A_spec,a` 가 부풀려진다.
퍼콜레이션 임계도 **약간** 낮은 AM 분율로 밀린다(입자 크기 효과만큼 뚜렷하지는 않다).
`[인쇄, 핵심]` "**As a result, percolation effects are suppressed in thin electrodes, giving
the impression of favorable electrode properties. This is a direct effect of the reduced model
size, also known as a finite size effect.**"
`[인쇄]` "**In contrast to the electronic conduction, ionic conduction is not affected by the
electrode thickness**: The drop of volume-specific active interface area (compare Figure 7) is
**indistinguishable for all thicknesses**."
`[인쇄, 소결론]` "**solely judged by microstructural modeling, thick electrodes could provide
conduction clustering properties comparable to those of thin electrodes.**" 다만 이 기법은
긴 확산 경로를 반영하지 못하므로 충·방전 성능을 직접 반영하지는 않는다.

`[해석]` **Fig. 10 이 이 논문에서 가장 정직한 그림이다** — 자기 방법의 인공물을 그려서
"이건 인공물" 이라고 적었다. 그리고 그 인공물은 **우리에게도 직접 걸린다**:
DEM 도메인이 작으면 `θ` 가 낙관 방향으로 편향된다 (§13-3).
`[해석]` ⚠ 본문은 "cut … between 20 and **120** µm" 인데 **범례와 캡션은 140 µm 를 포함**
한다 (140 은 자르지 않은 원본). 사소하지만 재현에 걸린다 (§10 불일치 4).

---

## 9. CONCLUSIONS (p8)

`[인쇄]` 요약:
1. ASSB 복합양극의 전자·이온 퍼콜레이션을 평가하는 **미시구조 모델링 방법을 확립**했다.
   AM + SE 2 성분 = **무탄소 고체전지 양극**이며 Strauss et al.(ref 13) 이 실험적으로 뒷받침.
2. **작은 AM 입자가 바람직**하다 (무탄소 복합체의 전자 전도 관점). 반면 큰 AM 표면은
   양극/전해질 계면 열화를 촉진할 수 있다 (ref 7).
3. **공극률을 재라** (§7.5).
4. **이상 조성을 식별**했다 — 입자의 형상·크기·겹침 거동 외에 **어떤 재료 특성도 쓰지 않고**.
5. `[인쇄, 자기 한계]` "**the effective conductivity optimum may differ from the optimum in
   specific active interface area**, especially for the electronic cluster, because therein the
   AM particles are designed to **avoid overlap** and, at low AM fraction, are mainly connected
   by **point contacts** leaving aside constriction resistances."
6. `[인쇄, 자기 한계]` "**real solid-state battery cells are a time-variant system and the
   initial composition may change during cycling, incorporating particle cracks, volume
   changes, and other mechanical or (electro-)chemical issues** (ref 43). AM coating, binder,
   and conductive agent may influence the performance as well as inhomogeneities … **these
   issues are beyond the scope of this study**, whose intent is to provide **design guidelines
   and a performance estimation**, forming a **foundation** for microstructural modeling of
   ASSBs."

`[인쇄]` 확장 방향: 전기화학 반응의 수학적 모델링, 또는 입자 배열을 **저항 네트워크**로
변환 (연료전지에서 Sunde(ref 40), Ott et al.(ref 41) 이 한 것처럼).

`[해석]` 결론 5·6 이 이 논문의 경계를 정확히 긋는다. **저자들 스스로 "이것은 설계 지침이지
성능 예측이 아니다" 라고 적었다.** 우리는 이 경계 안에서만 인용해야 한다.
그리고 **확장 방향(저항 네트워크)이 우리가 필요한 방향과 정확히 같다** — 기하 클러스터를
전기적 양으로 번역하는 층이 빠져 있고, 그 층이 있어야 `θ` 가 전압/용량으로 내려온다.

---

## 10. 본문 · 그림 · 초록 어긋남 원장

| # | 자리 | 어긋남 | 무게 |
|---|---|---|---|
| **1** | 초록 문장 4 ↔ p7 본문 | 초록: "An impact of electrode thickness **on the effective electronic conductivity** is observed exclusively in thin electrodes, where percolation effects are suppressed **implying favorable electrode properties**." · 본문: 잰 것은 `A_spec,a` 이고(전도도는 계산한 적 없음, G1), 본문은 "giving **the impression of** favorable electrode properties. This is a direct effect of the reduced model size, **a finite size effect**." | **크다.** 초록이 (a) 계산되지 않은 양을 결과로 말하고 (b) **인공물을 장점으로 뒤집는다**. 초록만 읽으면 정반대 결론을 갖고 나간다. |
| **2** | 식 (6) ↔ p4 산문 | 산문은 "클러스터에 속한 부피와 **속하지 않은** 부피의 **비**", 식은 `θ = V_c/V_ν`. 그림들이 100 % 로 포화하므로 **식이 맞다**. | 중간. 식 (6) 을 코드로 옮길 때 산문을 따르면 발산한다. |
| **3** | p4 본문 ↔ Fig. 3 | 본문: 같은 AM 분율에서 배열에 따라 `θ` 가 **≈70 % 와 ≈30 % 로 갈린다**(이봉). Fig. 3 에는 **오차 막대도 산포도 없고** 평균 점만 있다. | 중간. 이 논문에서 우리에게 가장 중요한 수치가 **그림으로는 보이지 않는다**. |
| **4** | p7 본문 ↔ Fig. 10 범례·캡션 | 본문 "cut … between 20 and **120** µm" vs 범례·캡션 "20 … **140** µm" (7 개 곡선). | 작다. 140 = 자르지 않은 원본으로 보인다. |
| **5** | §7.2–7.3 ↔ 서론·§6 | 같은 물질을 "**NMC**-622"(결과절) 와 "**NCM**-622"(서론·§6)로 혼용. NCM-811 도 등장. | 작다. 검색·인용 시 주의. |
| **6** | 식 (5) 좌변 기호 ↔ §4.3 의 위첨자 규약 | `g^V_SE` 는 규약상 "전체 부피 기준" 이어야 하나 식 (5) 의 출력은 **SE 하부구조 기준**이다. | 중간. 코드 이식 시 직접 걸린다. |
| **7** | p5 `p_c` 정의 | "the mean utilization level is at **40 vol%**" — 이용률은 vol% 가 아니라 무차원 %. | 작다(단위 오기)지만 핵심 출력의 정의문이다. |
| **8** | 식 (8) ↔ Fig. 6 의 `d = 3 µm` 점 | `[재현]` 식 (8) = 45.27 vol% vs `[도표]` 데이터 ≈44, 오차 막대 위끝 ≈45. 점선이 오차 막대 위를 지난다. | 작다–중간. **가장 작은 입자에서 맞춤이 가장 나쁘다.** figure-read 기반이라 수치표가 있으면 재확인 필요 — **없다.** |

`[해석]` **1 번이 이 논문을 인용할 때의 실질적 위험이다.** "Bielefeld 2019 는 작은 입자가
유효 전자 전도도를 높인다는 것을 보였다" 라는 인용문은 **원문에 근거가 없다** — 보인 것은
`θ_AM` 과 `A_spec` 이지 전도도가 아니다.

---

## 11. 닻 질문 Q1–Q8 (`questions/assb-contact-loss-vs-lampe.md` 의 수집 지침)

> 규칙: **없으면 "없다" 고 적는다. 없다는 사실도 이 계보의 관측이다.**

| # | 항목 | 이 논문이 **주는 것** | 이 논문이 **안 주는 것** |
|---|---|---|---|
| **Q1** | 접촉 손실을 **어떻게 정량**했나 (단위·측정법·모델 형태) | **접촉 손실이라는 이름으로는 정량하지 않는다.** 대신 그 정적 기하 대용량인 **이용률 `θ = V_c/V_ν`** (식 6, 무차원 %) 을 계산한다 — "퍼콜레이팅 전도 클러스터에 속한 성분 부피 / 그 성분 전체 부피". 모델 형태: **3D voxel 미시구조(400×400×700 voxel, 200 nm) + Hoshen−Kopelman 클러스터 판정**. 짝이 되는 동역학 량: **활성 계면적 `A_spec,a` [m²/m³]**. `θ_AM` 은 `(g^S_AM, φ, d_AM)` 의 함수로 표로·그림으로 주어진다. | **시간축이 없다** — 사이클·부피 변화·균열로 인한 접촉 **상실 과정**을 모델링하지 않는다 (G10). "contact loss" 는 서론에서 **동기로 1 회** 나오고 결과에는 없다. 접촉 저항·수축 저항은 **명시적으로 배제** (G8) → `θ` 는 **상한**. |
| **Q2** | 접촉 손실과 LAM 을 가르는 **독립 관측**을 썼나 | **쓰지 않았다 — 이 논문에는 실험이 0 개다.** 다만 **가를 관측이 존재한다는 것을 가리킨다**: Strauss et al.(ref 13) 의 **ex situ XRD 로 잰 inactive NCM-622 분율** = 원리적으로 `1 − θ_AM` 의 **measured 라벨**. | 그 대조가 **정성적이다** ("correlate well"), 그림도 표도 수치도 없다. 그리고 논문 스스로 무효화한다: `[인쇄]` "**the total packing density of AM used by Strauss et al. is not known, as the porosity was not measured**". → **정량 대조 불가.** |
| **Q3** | **라벨 출처 층위** (measured / fitted / 가정) 와 오차 막대 | 층위가 **제3의 것**이다: **computed-geometric** — 측정도 적합도 아닌 **시뮬레이션 산출**. 입력(조성·공극률·입자 크기)은 **우리가 정하는 값**이므로 "라벨" 이 아니라 **설계 변수**다. 오차 막대: **Fig. 4(8 배열 표준편차)와 Fig. 6(10 배열)에만** 존재. | Fig. 3·5·7·8·9·10 에 **오차 막대 없음**, 그리고 전이 구간 **밖** 점들은 `[인쇄]` **배열 1 개** (G7). 이 논문에서 가장 많이 인용될 값(최적 조성 62/38·66/34·72/28)이 **반복 없는 단일 실현**이다. 적합(fitting)은 딱 두 번 — 식 (1) 의 `β = 0.41`(Fig. 4)과 식 (8) 의 `p_c(d)`(Fig. 6). 둘 다 **신뢰구간이 인쇄돼 있지 않다.** |
| **Q4** | **유일성·식별성**을 쟀나 (조건수·근최적 폭·프로파일) | **안 쟀다.** `identifi*` **0 회**, `uniq*` **0 회**, 조건수·프로파일·근최적 집합 전부 없음. 애초에 **역문제를 풀지 않는다**(forward 전용)라는 점에서 액체셀 17 편의 결함과는 종류가 다르다. **그러나 비유일성을 한 번 인쇄한다**: `[인쇄, p6]` "the cathode composition and its porosity are **not well-defined for a given total fraction of AM**" — `(g^S_AM, φ)` 두 자유도가 `g^V_AM` 하나로 접힌다(§7.1). | 그 진술을 **연구 설계를 두 갈래로 나누는 이유로만** 쓰고 **역문제로 보지 않는다.** `[해석]` 그림들이 더 큰 비유일성을 이미 보여 준다: Fig. 8 의 봉우리는 **평탄**하고(±3–4 vol% 구별 불가), Fig. 10 은 **두께 20–140 µm 곡선이 최적 근방에서 겹친다** → **`A_spec,a` 관측 하나로는 (조성, 공극률, 두께)를 되찾을 수 없다.** 논문은 이것을 말하지 않는다. |
| **Q5** | **Li-In 기준 전위 이동** | **없다.** `indium` 0 회, `Li-In` 0 회, `lithium metal` 0 회(음극으로서). 음극은 서론에서 "리튬 금속 음극을 가능케 한다" 는 **동기 문장 1 회**뿐이고 **모델에 음극이 없다** — 복합**양극**만. | 전위·전압 자체가 이 논문에 없다 (`voltage` 1 회, 그마저 참고문헌 제목). |
| **Q6** | **압력** 통제·보고 | **없다. `pressure` 0 회.** 제조 압력·스택 압력·구속 압력 전부 없음. | **공극률 `φ` 는 압력의 대용이 아니라 독립 입력 변수**로 직접 지정된다. 따라서 "공극률은 낮을수록 좋다"(Fig. 9 의 단조 증가)는 **압력 비용이 모델에 없기 때문에** 무조건이 된다. `[해석]` 압력을 상태변수로 놓는 순간 이 논문의 처방(저공극)은 **비용을 갖는 최적화**로 바뀐다. |
| **Q7** | 무음극의 dead Li ↔ SEI Li | **없다.** 무음극(anode-free)·dead Li·SEI 전부 0 회. 양극만 다룬다. | — |
| **Q8** | 양극 화학과 **OCP 기울기** | 화학은 **예시로만** 언급: **NCM-811**(서론, ref 7), **NCM-622 / NMC-622**(§6·§7, 그리고 vol%→wt% 환산), SE 는 **β-Li₃PS₄ (LPS)** / 일반 티오포스페이트. `[재현]` 환산에서 `ρ_AM/ρ_SE ≈ 2.4` 를 역산할 수 있다(§7.3). | **OCP 곡선이 없다. 전압축 자체가 없다.** 화학은 **밀도와 입자 크기의 출처**로만 쓰이고 전기화학은 들어오지 않는다. → **이 논문은 Q8 에 대해 "양극 화학이 기하에 들어오는 유일한 통로는 밀도와 입도" 라는 답을 준다.** |

`[해석]` **Q1·Q3 에서 부분적으로 주고, Q2 에서 다음 논문을 가리키고, Q4–Q8 에서 전부
없다.** 이것은 실패가 아니라 **예상된 분업**이다 — 이 논문은 `assb` 축의 **미시구조 쪽
절반**이고, 전기화학 쪽 절반(OCV·전위·압력·음극)은 다른 논문이 채워야 한다.
**`assb` 섹션이 채워야 할 빈칸이 Q4–Q8 로 확정됐다.**

---

## 12. ★ 인터페이스 사양 — 퍼콜레이션 임계 · 유효 전도도 · 이용률의 변수와 단위

> 왜 이 절이 있나: DEM 산출을 **합성 forward model 에 주입**할 때, 그 인터페이스의 언어가
> 이 논문의 언어가 될 가능성이 높다 (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §3, §5).
> 아래는 **원문에 있는 정의만** 모은 것이다.

### 12.1 상태 변수 (입력)

| 기호 | 정의 | 단위 | 출처 |
|---|---|---|---|
| `φ` | 공극률 `= V_pore/V_total = 1 − (V_AM+V_SE)/V_total` | 무차원 (논문은 %) | 식 (2), (3) |
| `g^V_AM` | **총** AM 부피분율 — **공극 포함** 전체 구조 부피 기준 | vol% | §4.3 · 그림들의 **아래 x 축** |
| `g^S_AM`, `g^S_SE` | **고상 기준** 부피분율 (`g^S_AM + g^S_SE = 1`) — **"조성 표기" 가 이것** | vol% | 식 (9) · 그림들의 **위 x 축** ("72/28 vol%") |
| — | 두 축의 변환 | — | **`g^S_AM = g^V_AM/(1−φ)`** (식 9) · `g^V_AM = (1−φ)(1−g^S_SE)` (식 4) |
| `g^V_SE` (식 5) | ⚠ 이름과 달리 **SE 하부구조(= AM 이 아닌 부피) 기준** SE 충전율 `= (1−φ)g^S_SE / [(1−φ)g^S_SE + φ]` — **생성 절차용**이지 보고용이 아니다 | 무차원 | 식 (5) · §4.3 `[해석]` |
| `d` | **AM** 입자 지름 (균일 분포, 구) | µm, {3…15} | Table 1 |
| `d_SE` | SE 입자 = **외접구 지름**, **3 µm 고정** | µm | Table 1 |
| `l` | 전극 두께 | µm, 20–140 | Fig. 10 |

### 12.2 출력량

| 기호 | 정의 | 단위 | 값의 범위 (이 논문) |
|---|---|---|---|
| **`θ` (이용률)** | `V_c/V_ν` — 성분 `ν`(AM 또는 SE) 중 **퍼콜레이팅 클러스터에 속한 부피 분율**. AM 은 **전자** 클러스터(집전체 면에서 출발), SE 는 **이온** 클러스터(분리막 면에서 출발) | **무차원, %** | 0 – 100 %; 전이 구간에서 배열 간 **≈30 % ↔ ≈70 % 이봉** |
| `A_spec` | 한 클러스터의 표면적 / **구조 부피** | **m²/m³** | ≈0.15 – 10.6 ×10⁵ |
| **`A_spec,a`** | **이온 클러스터와 전자 클러스터 사이의 계면적** / 구조 부피 — "리튬 삽입에 실제로 쓸 수 있는 면적" | **m²/m³** | ≈0 – 6.1 ×10⁵ |
| `A_spec,geo` | 기하 상한 `= 6 g^V_AM / d` (모든 구가 연결됐을 때) | m²/m³ | 식 (7); 데이터는 이것의 **80–91 %** 에서 포화 |
| **`p_c`** | 퍼콜레이션 임계 — **10 개 배열의 평균 `θ_AM` 이 40 % 가 되는 `g^V_AM`** (⚠ 40 % 는 임의 문턱) | **vol% (of AM, 총 부피 기준)** | 44 – 57 vol% (d = 3 – 15 µm) |
| `β` | 임계 지수, `A_spec ∝ (p − p_c)^β` | 무차원 | **0.41** (d = 10 µm, 8 배열) |

### 12.3 이 논문이 주는 닫힌 형태 두 개

> **식 (8)**  `p_c = [ 7.83 · ln(d/µm) + 36.67 ] vol%`
> 적용 조건: **AM 구, 균일 입도, SE 3 µm, 무탄소, 겹침 없음, 전자 클러스터**.
> `[해석]` `d_AM/d_SE` 와 `d_AM` 이 교란돼 있다 (G3).

> **Fig. 4 범례**  `A_spec(p − p_c) = 1.73×10⁵ · ((p − p_c)/vol%)^0.41  m²/m³`
> 적용 조건: **d = 10 µm**, 임계 바로 위 1–5 vol%.
> `[해석]` 프리팩터 `1.73×10⁵` 는 **d = 10 µm 전용**이다. 다른 `d` 로 옮기려면
> 식 (7) 로 스케일해야 하는데 **논문이 그 스케일링을 주지 않는다.**

### 12.4 우리 forward model 로의 번역 (전부 `[해석]` — 논문의 주장이 아니다)

액체셀 판의 아핀 창 좌표계에서 양극 쪽은 `E_PE((x − b_PE)/a_PE)` 이고 `a_PE` 가
**용량 축 스케일**이다 (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1).
이 논문의 양을 그 위에 얹으면:

```
Q_apparent(PE) = θ_AM(g^S_AM, φ, d) · Q_material(PE)
```

- **`θ_AM` 은 `a_PE` 에 곱으로 들어간다** — 재료량 `Q_material` 을 건드리지 않고.
- 따라서 **진짜 `LAM_PE`(재료 소실)와 접촉 손실(`θ_AM` 하락)은 `a_PE` 안에서 곱으로 섞인다.**
  OCV 곡선만 보면 **둘의 곱만 관측된다** → 닻 질문의 A1 축퇴가 **곱셈 축퇴**임이 이 논문의
  언어로 명시된다.
- 가르려면 **`θ_AM` 을 독립으로 주는 관측**이 필요하다. 이 논문이 가리키는 후보는
  (a) **DEM/미시구조 모델** (이 논문이 하는 일), (b) **ex situ XRD 의 inactive fraction**
  (Strauss et al., ref 13).
- ⚠ 그러나 이 논문의 `θ_AM` 은 **pristine 정적 값**이다. 열화 궤적을 주려면
  **AM 수축·간극 생성을 넣고 재계산**해야 하는데 이 논문은 그것을 하지 않는다 (G10).

---

## 13. 우리 프로젝트에 대한 시사점 (전부 `[해석]`)

### 13-1. 이 논문은 "접촉 손실 모델" 이 아니라 "접촉 **상태** 모델" 이다
닻 질문의 미결 항목 1("접촉 손실을 모델에 어떤 형태로 넣나")에 대해 이 논문이 주는 답은
**"용량 축 스케일에 곱해지는 기하 인자 `θ_AM` 으로"** 다 (§12.4). 그것은 명확한 진전이다.
그러나 **`θ_AM` 의 시간 변화**는 이 논문에 없다. 우리가 열화 궤적을 만들려면
`θ_AM(cycle)` 을 **우리가 가정하거나** DEM 을 사이클마다 돌려야 한다.
→ **미결 항목 1 은 "형태" 가 정해졌고 "동역학" 이 남았다.**

### 13-2. `LAM_PE ↔ 접촉 손실` 은 **곱셈 축퇴**다
`Q_apparent = θ_AM · Q_material` 이므로 OCV 형상은 **곱에만 의존**한다.
이것은 [[np-lip-ocv-reparametrization]] 의 "SOC 정규화 OCV 는 비(比)에만 의존" 과
**같은 종류의 닫힌 형태 null 방향**이다 — 다만 여기서는 `LAM_PE` 축 **안에서** 일어난다.
→ **폭 측정기([[near-optimal-set-width-measurement]])를 그대로 걸 수 있다**는 뜻이며,
답은 미리 짐작된다: **OCV 단독으로는 이 곱을 못 가른다.** 재는 것은 "가르는가" 가 아니라
**"독립 관측 하나를 넣으면 폭이 얼마나 줄어드는가"** 여야 한다.

### 13-3. ★ **독립 라벨도 폭을 갖는다** — 이 논문이 자기 안에서 정량한다
`[인쇄, p4]` 같은 AM 분율·같은 공극률·같은 입자 크기에서 **무작위 충전 배열만 바꾸면**
`θ_AM` 이 **≈30 % 와 ≈70 %** 로 갈린다 (폭 ≈40 %p). 그리고 `[인쇄, Fig. 4]` 임계 바로 위에서
`A_spec` 의 표준편차가 평균의 **≈±32 %** 다 (8 배열).
→ **DEM 이 "독립 라벨" 을 준다는 계획은, 그 라벨 자체가 임계 근방에서 이봉·광폭이라는
조건을 달고 출발해야 한다.** 액체셀에서 우리가 "라벨에 오차 막대가 없다" 를 비판해 왔으므로
(`bms-balancing/docs/NEW_MODEL_REQUIREMENTS.md` §5), **우리 DEM 라벨에는 반드시 폭을 붙인다.**
그리고 폭이 작은 곳에서 일해야 한다 — **임계에서 멀리**(`p − p_c ≳ 5 vol%`).
같은 논문 안에 그 처방이 있다: 임계에서 5 vol% 떨어지면 표준편차가 ±2 % 로 줄어든다.

### 13-4. `A_spec,a` 의 봉우리는 평탄하다 — **역추정에 쓸 수 없다**
`[도표]` Fig. 7 에서 총 54–62 vol% 가 봉우리의 89 % 이상, Fig. 8 에서 세 공극률 곡선 모두
봉우리가 평평하며, Fig. 10 에서 두께 7 종이 최적 근방에서 **겹친다**.
→ 만약 누군가 `A_spec,a`(또는 그 전기화학적 대응량)를 관측으로 삼아 미시구조를
역추정한다면 **우리가 액체셀에서 본 flat valley 와 똑같은 것을 만나게 된다.**
이 논문은 **forward 방향이라 그 문제를 만나지 않았을 뿐**이다.
→ **[[fitting-degeneracy]] 의 논지가 화학과 무관하게 재현될 자리가 여기 하나 더 있다.**

### 13-5. 유한 크기 효과 = 우리 DEM 도메인 크기 규율
`[인쇄, Fig. 10]` 얇은 전극에서 `A_spec,a` 가 부풀려지는 것은 **인공물**이다
(45 vol% 에서 20 µm 가 140 µm 의 `[재현]` 약 6 배).
→ DEM 도메인을 작게 잡으면 `θ` 가 **낙관 방향으로 편향**된다. 우리 DEM 산출을 라벨로
쓰려면 **도메인 크기 수렴 시험이 선행 조건**이다. 이 논문이 그 시험의 형태를 보여 준다
(같은 배열을 잘라 가며 출력의 두께 의존을 그린다).

### 13-6. 이 논문이 확인해 주는 것: "공극률을 아무도 안 잰다"
`[인쇄, p8]` 저자들이 **8 편을 지목해**(ref 5, 7, 11–15, 17) "공극률이 보고되지 않는다" 고
적는다. 이는 [[mode-identifiability-unmeasured-lineage]] 가 액체셀 17 편에 대해 한 관측과
**형식이 같다.** `assb` 축에서도 **"모두가 빠뜨린 필수 변수" 의 원장**을 유지할 가치가 있다.
현재 등재: **공극률**(Bielefeld 2019 가 지목), **압력**(우리가 지목 — 이 논문에도 0 회).

### 13-7. 우리가 이 논문에 공급할 수 있는 것
이 논문은 forward 전용이라 **식별 가능성을 물을 이유가 없었다.** 그러나 §7.1 의
`[인쇄]` "조성과 공극률은 총 AM 분율 하나로 정해지지 않는다" 는 **역문제 진술 그 자체**다.
→ 우리 폭 측정기는 **화학에 무관**하므로, `(g^S_AM, φ, d, l) → (θ_AM, A_spec,a)` 라는
이 논문의 forward map 위에 **그대로 걸 수 있다.** "미시구조 관측 몇 개를 재야
미시구조 파라미터가 유일해지는가" 는 **이 논문이 묻지 않은, 우리가 쓸 수 있는 질문**이다.

---

## 14. 후속 논문 후보 (이 논문이 가리키는 것)

`[해석]` 우선순위:

1. **Strauss, Bartsch, de Biasi, Kim, Janek, Hartmann, Brezesinski**, "Impact of Cathode
   Material Particle Size on the Capacity of Bulk-Type All-Solid-State Batteries",
   *ACS Energy Lett.* **2018**, 3, 992−996 (ref 13) — **`1 − θ_AM` 의 measured 라벨**
   (ex situ XRD inactive fraction). **Q2 의 유일한 실마리.**
2. **Koerver, …, Zeier, Janek**, "Capacity Fade in Solid-State Batteries: Interphase Formation
   and Chemomechanical Processes in Nickel-Rich Layered Oxide Cathodes and Lithium
   Thiophosphate Solid Electrolytes", *Chem. Mater.* **2017**, 29, 5574−5582 (ref 7) —
   **접촉 손실의 실험 원전**이며 **용량 감소와 연결**된다. 여기에 전압·용량 축이 있다.
3. **Zhang, Weber, …, Janek**, "Interfacial Processes and Influence of Composite Cathode
   Microstructure Controlling the Performance of All-Solid-State Lithium Batteries",
   *ACS Appl. Mater. Interfaces* **2017**, 9, 17835−17845 (ref 12) — 공저자 Weber 가 겹친다.
4. **Hlushkou, …, Roling, Tallarek**, "The Influence of Void Space on Ion Transport in a
   Composite Cathode for All-Solid-State Batteries", *J. Power Sources* **2018**, 396, 363−370
   (ref 16) — **FIB-SEM 재구성 + 수치 시뮬레이션**, 즉 **실측 미시구조**. 이 논문의 합성
   기하와 대조할 수 있다.
5. **Nam, Oh, Jung, Jung**, *J. Power Sources* **2018**, 375, 93−101 (ref 11) — 5 성분 복합양극
   (바인더·도전재 포함) 의 출처. 이 논문이 **뺀 것**이 무엇인지 확인용.

---

## 15. 이 digest 가 주장하지 않는 것

- 이 논문이 **우리 물음에 답했다고 말하지 않는다.** Q4–Q8 이 전부 "없다" 다.
- `θ_AM` 이 접촉 손실의 **올바른** 모형이라고 주장하지 않는다 — 이 논문의 `θ` 는
  **pristine 정적 기하량**이고 접촉 저항을 배제한 **상한**이다.
- §12.4 의 `Q_apparent = θ_AM · Q_material` 은 **우리 해석**이다. 논문은 용량도 전압도
  쓰지 않는다.
- 여기 적힌 `[도표]` 값은 **원 데이터가 아니다.** 논문에 수치표가 없어 그림에서 읽었고,
  판독 오차가 있다. 인용하려면 원문을 다시 본다.
- 액체셀 계열의 결론을 이 논문으로 옮기지 않았고, 이 논문의 결론을 액체셀로 옮기지 않았다.
