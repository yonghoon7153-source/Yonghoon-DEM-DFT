# 연구세미나 v3 재검토 판정

2026-10-13. 대상은 동봉된 17장 PPTX와 그 PDF, 새 그림 10개, 발표 노트다. 리포·원본 발표물·시뮬레이션은 변경하지 않았다.

## 1. 결론

**조건부 GO. 현재 파일 그대로의 발표 승인은 아니다.** 아래 P0 다섯 묶음은 발표 전에 고쳐야 한다. 수정은 출처·비교군 이름·배율 정의·결론의 강도를 바로잡는 작업이다. 새 시뮬레이션, 물성 측정, 캠페인 재설계를 요구하지 않는다.

기존 v2 필수 수정은 반영됐다. 다만 이번 v3는 19장을 17장으로 압축하고 믹서 세 장을 새로 넣은 판이다. 이전 종결 판정이 새 믹서 해석까지 승인한 것은 아니다. **주요 수치가 무너진 덱은 아니지만, 새 라벨과 제목이 수치가 뒷받침하는 범위를 넘어선다.**

이 문서의 등급은 발표물 검토용이다. P0=발표 전 필수 의미·출처 수정, P1=정확도·출처 명료화·가독성 개선, P2=선택 개선이다. 소프트웨어 장애의 P0와 다르다.

| ID | 등급 | 위치 | 발표 전 바로잡을 내용 |
|---|---|---|---|
| SEMV3-01 | P0 | p6, p16 [9] | JES 논문에서 가져온 그림을 다른 JPS 논문으로 인용 |
| SEMV3-02 | P0 | p11–13 본문·그림·notes | 작은 비영 점착 대조군을 `no cohesion / cohesion removed`로 명명 |
| SEMV3-03 | P0 | p11, p15 | 후속 진단의 수치 범주를 물리적 무분리 발견처럼 읽히게 하는 제목·요약 |
| SEMV3-04 | P0 | p12, p13 배율 라벨 | Bo 배율과 CED 배율을 혼용하고, 정규화가 다른 ΔM을 혼합 감소로 번역 |
| SEMV3-05 | P0 | p13 식·도식·notes | 면적당 접착일의 가정을 생략하고 작은 SE의 동종 접촉 우세를 단정 |

아래에서 제공하는 영어는 교체 문구다. 원본을 직접 고치지는 않았다. 내부 팔 식별자는 검토 근거에만 사용하며 발표 화면에 넣을 필요가 없다.

## 2. 검토 대상과 증거의 경계

### 파일 고정

| 파일 | SHA-256 |
|---|---|
| 입력 ZIP | `ad85809cee600a8ed7300ceee04797ff1bf23f37fbd7d45e12d294093423c72d` |
| 실제 PPTX | `baf2bb9899c23bbe94d50ee35f9fc5ccedb8f1fe6121afab2baf248fe2148d9c` |
| 실제 PDF | `bb94b5de7f16c9a52d4e281728883f9b9930fd79547d2f7ddcf1033cba28e726` |

PPTX 17장과 PDF 17쪽을 확인했다. PPTX 본문·notes·삽입 이미지와 PDF를 대조하고, PDF를 별도로 렌더해 17쪽 모두 확인했다. PowerPoint 앱에서 직접 열어 검사했다고 주장하지 않는다.

수치 근거는 과거 검토 때 확보한 코드 핀 `a0439bdf8156236f454bd3f8b5bf4d044e127039`의 저장 자료 및 같은 핀에서 추가 조회한 판독 JSON·입력 덱이다. 문헌 자산은 `6e568c4f0bb7df299959fd0e77e349838ad8ac98`의 정본과 대조했다. **이번 제출물의 정체성은 위 파일 해시로 고정하며, 제출 요청서 커밋과 저장소 HEAD가 같다고 별도로 인증한 것은 아니다.**

검증 수준을 구분한다.

- 배포 CSV 194행, Phase A 원판 96팔 평균 12점, 100 GPa 재현 96팔 및 QC, 21단면 하중 가중 기여율을 저장 자료에서 다시 계산했다.
- 믹서 10런의 최종 25프레임씩, 개발 21런·칸 조합의 최종 100프레임씩에서 `M=(S0−s²)/(S0−SR)`를 재계산했다. 저장 평균과 최대 차이는 각각 `2.22e−16`, `8.88e−16`이다.
- SE 군집 세 런의 100프레임씩에서 평균 및 해상도 범위의 평균을 다시 계산했다.
- 이것은 **저장된 프레임 판독 결과의 독립 산술 검증**이다. 원 입자 덤프에서 접촉·분산을 새로 추출하거나 DEM/MPM/전도도 솔버를 재실행한 것은 아니다. 겹침 오차가 M에 주는 물리 오차도 새로 규명하지 않았다.
- 제작자 selftest를 통과 근거로 쓰지 않았다. 특히 믹서 그림 selftest 일부는 README에 특정 문자열이 있는지만 검사한다. 실제 수치 대조를 대신하지 못한다.

`input/`은 제출물 그대로의 사본, `sources_code/`·`sources_mixing/`은 검산용 자료다. 전달 묶음의 `notes/`에는 재현기와 추가 원자료가 있다. 중간 분야별 메모는 전달에서 제외했으며 **최종 판정은 이 문서**다.

## 3. 기존 수정과 요청 Q-V3-1·4

### 이전 일곱 항목

| 이전 ID | v3 위치 | 이번 판정 |
|---|---|---|
| SEMV2-01 | p6 | **닫힘.** 현재 DEM-seeded servo에서 `f=0 completed`, `f(a) execution failed`가 notes에 정확히 남는다. 화면도 `not one validation series`, independent validation pending을 명시한다. 성공한 AM 하중분담 검증으로 바꾸지 않았다. |
| SEMV2-02 | p10 | **닫힘.** (a) 기하 tortuosity 130+64, 비관통 24개는 130집단, (b) porosity는 130집단. 실제 CSV와 일치한다. |
| SEMV2-03 | p8 | **부분.** 옛 세로축의 바깥 잘림은 해결됐다. 새 3패널 안에서 범례와 옆 세로축이 교차한다(§6). |
| SEMV2-04 | p2 | **닫힘.** native 도형 흐름도의 제목 넘침은 없다. |
| SEMV2-05 | p5 notes | **닫힘.** DFT Young's modulus `E_VRH=22.06 GPa`와 bulk modulus `K/B0=26.23 GPa`를 구분한다. |
| SEMV2-06 | p6 | **닫힘.** 화면의 LPSCl `E≈22 GPa` 출처와 DEM 유효값 1.35 GPa가 구분되고, 미확립 σy 문헌 범위는 화면에서 빠졌다. 단 notes의 잔여 표현은 §6에서 정리한다. |
| SEMV2-07 | p4 | **닫힘.** [8]은 contact-network 방법의 출처이며 선택한 σ0=1.5 mS/cm를 해당 논문 실측으로 귀속하지 않는다. |

### 압축하면서 의미가 바뀌었나

Q-V3-1 답: p5 두 번째 불릿의 MPM·J2 설명과 p7 두 번째 불릿의 첨가제·104팔 순서 설명은 핵심 뜻을 유지한다. 다만 “모든 값·문장이 그대로”라는 포괄 승인은 불가하다. p7의 그림은 원판 캠페인이고 순서 재현 근거는 다른 강성 세대라 출처를 갈라 적어야 한다. 새 p6 문헌 그림은 출처 오류가 생겼고, 믹서의 분야 용어 치환은 비영 대조군을 0으로 바꾸었다.

Q-V3-4 답: notes로 옮겼다는 이유만으로 자동 실패는 아니다. 화면의 주장이 그 세부 없이도 정직한지를 기준으로 했다.

| 장 | notes에 남겨도 되는 내용 | 화면/notes에서 정리할 내용 |
|---|---|---|
| p5 | 문헌 22편 집계, 세부 모델 설명 | 감쇠 58%는 한 침대 압축 구간의 열린 문제다. 제한 사항을 강조하려면 짧게 화면에 복구하되 모든 DEM의 속성으로 일반화하지 않는다. 필수 P0는 아님. |
| p6 | 현재 실행 상태의 상세, 과거 초기화와 두께값 | 화면이 pending을 명시하므로 상태 세 줄의 notes 이동 자체는 허용. `f(a) execution failed`를 삭제하거나 검증 성공으로 바꾸면 안 된다. notes의 `inside the literature range`는 근거를 제시하지 못하면 삭제. |
| p7 | FV 보존식과 스탬핑 세부 | 그림 원판 10 GPa와 100 GPa 재현을 구분하는 출처 세대는 짧게 화면에 표시할 것. |
| p10 | 106/130, 범위 1.3–4.2, CV 상세 | 집단·기하/수송 차이·HOLD·조건부 배포는 이미 화면에 있으므로 추가 필수 복구 없음. |
| p11–13 | 팔별 긴 숫자표·상세 등록 이력 | 비영 대조군, 진단 지위, Bo/CED 구분, 접착일 가정은 결론의 뜻을 바꾸므로 화면에도 필요. |

## 4. 발표 전 필수 수정 P0

### SEMV3-01 — p6 그림은 JES 논문인데 크레딧은 JPS

**위치:** 실제 p6 상단·그림 아래·[9], p16 [9]. 생성기 `build_seminar_v3.py:395,581,593,782`. 추출문 `evidence/all_slide_text.txt:110,126,300`.

생성기는 `so2021_dem_fabrication_degradation_ductile_particles/fig_4.png`를 읽는다. 해당 자산의 정본 메타데이터는 **So et al., Journal of The Electrochemical Society 168, 030538 (2021), Fig.4**, 원 PDF 6쪽을 가리킨다. 현재 화면의 **J. Power Sources 508, 230344 (2021)**는 다른 논문이다.

이것은 파일명만 보고 한 추정이 아니다. [출판사 제공 미리보기와 Figure 목록](https://www.researchgate.net/publication/349934624_Simulation_of_Fabrication_and_Degradation_of_All-Solid-State_Batteries_with_Ductile_Particles)의 상대밀도 그림·첫 페이지 및 [같은 저자들의 MethodsX 원문 References 1–2](https://catalog.lib.kyushu-u.ac.jp/opac_download_md/7161227/7161227.pdf)에서 두 논문을 교차 구분했다. 상세는 `evidence/so_source_verification.md`에 보존했다.

**최소 교체:**

> So et al., J. Electrochem. Soc. 168, 030538 (2021), Fig. 4a [9]

참고문헌 [9]:

> M. So et al., “Simulation of Fabrication and Degradation of All-Solid-State Batteries with Ductile Particles,” J. Electrochem. Soc. 168, 030538 (2021). DOI: 10.1149/1945-7111/abed23.

현재 [9]의 화면 용도는 p6이므로 **[9]를 교체하면 참고문헌 수 16개는 유지**할 수 있다. “참고문헌 내용도 불변”을 우선할 경우에는 JPS 논문의 실제 해당 그림으로 교체하고 패널 번호를 다시 확인해야 한다. 현재 그림과 현재 JPS 크레딧을 동시에 보존할 수는 없다. 정본 카드에 남은 `abe796`도 전사하지 말 것. 출판사 미리보기와 저자 원문이 확인해 주는 DOI는 `abed23`이다.

**무너지지 않는 것:** 우리 MPM 입력·보정 수치가 틀렸다는 지적이 아니다. 문헌 예시의 귀속 오류다. 별도 시각 문제인 500 MPa 끝 잘림은 §6에 있다.

### SEMV3-02 — 0이 아닌 대조군을 무점착으로 되돌려 부름

**위치:** p11–13의 `No NCM–NCM cohesion`, `cohesion removed`, `non-cohesive NCM`, ΔM 축 및 notes. 생성기 `build_seminar_v3.py:688,706,722`와 그림 생성기의 MIX 라벨.

비교군 LC는 0이 아니다. 실제 개발 입력 덱의 AM_P–AM_P CED는 **108,795 J/m³**, AM_S–AM_S는 **142,562 J/m³**다. 등록 §0에도 큰/작은 AM의 Bo_code **0.00109/0.00553** 및 “작지만 0이 아니다”라는 정정이 남는다. 전 쌍 0인 음성대조 **L0는 따로 있다**. 용어를 쉽게 바꾸는 과정에서 이미 철회한 물리 해석을 되살렸다.

**최소 교체:**

- 해당 비교군: `Low NCM–NCM cohesion` 또는 `Low-cohesion comparator`
- ΔM 축: `ΔM = M(low-cohesion comparator) − M(arm)`
- p12 스냅샷 출처: `Low versus higher NCM cohesion, two revolutions`
- p11의 별도 L0 `No cohesion (control)`은 맞으므로 **유지**.

notes에는 작은 비영 점착과 NCM–벽 동반 개입을 남긴다. 작은 값을 0으로 바꿔 부를 만큼 무시 가능한지 새로 입증하지 않은 상태에서 `removed`를 쓰면 안 된다.

**닫힘 증거:** 본문·그림 PNG/SVG·CSV 라벨·notes의 비교군 표현을 함께 교체. 팔 데이터·수치·시드를 바꿀 필요는 없다.

### SEMV3-03 — 등록 수치 분기와 원 등록 전체 적격성이 다름

**위치:** p11 제목 `no segregation detected`, 본문 `registered "no segregation" category`, p15 요약.

같은 시드의 LC−LA 차이를 재계산하면

`d = (−0.01335676548, +0.00984870277, +0.00715116880)`

이고, **ΔM=+0.00121436870, seed SE=0.00732706480**다. 따라서 `|ΔM|≤SE`라는 **수치 분류식**은 맞는다. 이를 반증했다고 하지 않는다.

그러나 원 등록의 1% 겹침 조건은 NOT_MET다. 등록 정본 `mixer_layered_prereg_20260921.md:20,151–160`은 중간 M 열람 후 진단 전용으로 고친 **후속 분석**임을 명시한다. E0 저장 프레임 최대 겹침 4.7–5.8%와 벽 4.5–5.7%는 1%를 넘는다. 이 사실을 화면에 쓴 점은 좋지만, 제목과 Summary의 “무분리 검출 없음”은 후속 진단 범주보다 넓게 읽힌다. 측정 런 모두가 실패했다고 확대하는 것도 잘못이다.

**최소 교체:**

제목:

> Layered-bed mixing: unresolved mixing-index contrast

본문:

> Low NCM–NCM cohesion versus the reference setting gives an unresolved paired contrast at 16×16×4 bins (ΔM = 0.0012, seed SE = 0.0073).

화면의 짧은 한정:

> Subsequent diagnostic classification. The original 1% overlap condition was not met.

등록 이름을 유지하려면 notes 또는 충분히 읽히는 하단에:

> The numerical rule maps this contrast to the registered “no segregation” category. This does not establish compliance with the original registration, equivalence, or a physical absence of segregation.

p15 Mixing:

> Unresolved diagnostic mixing-index contrast under an unmet overlap condition. Exploratory cohesion results without a verdict.

**무너지지 않는 것:** 10개 M 막대, 짝차·SE, 등록 분기 계산, 시험한 칸 규약에서 방향·크기를 구분하지 못했다는 결론. 추가 시드나 런을 발표의 전제조건으로 요구하지 않는다.

### SEMV3-04 — p12의 같은 ×10은 같은 입력 개입이 아님

**위치:** p12 제목·두 불릿·F_mix2 범주, p13 all-pair 배율. 생성기 `build_seminar_v3.py:705–717`, `make_seminar_figs.py:53–62`.

실제 입력 덱 여섯 개를 대조한 결과:

| 계열 | 실제 변화 | 현재 표기의 문제 |
|---|---|---|
| NCM 쌍 계열 | 큰 NCM 자기쌍 Bo_code 38.4 → 384 → 1152 | ×10/×30은 **Bo_code** 배율 |
| 그 계열의 큰 NCM CED | 3.56348e6 → 7.67728e6 → 1.10725e7 J/m³ | CED 배율은 약 **2.154/3.107**, 10/30이 아님 |
| 전 쌍 계열 | 작은 비영 점착 대조군의 비영 CED 9항을 ×10/×14.422496 | ×10/×14는 **CED** 배율이며 기준군도 다름 |

p11의 `reference cohesion`은 Bo_code 3.0인데 p12 같은 이름은 38.4다. 같은 이름을 이어 쓰면 같은 입력 수준으로 오독한다. **모형 Bond number와 응집 에너지 밀도(CED)를 각각 정의하고, 어느 기준의 배율인지 분리해야 한다.**

또한 `stronger cohesion lowers mixing`는 지표 차이를 물리적 혼합 저하로 바로 옮긴다. 높은 NCM 점착 팔의 M은 세 칸에서 **−0.9683/−1.4072/−2.2826**까지 내려가며, 팔별 S0가 달라 ΔM에는 시작 상태와 정규화 차이가 포함된다. 아래쪽 `no verdict`가 제목의 인과 결론을 취소하지 않는다.

**최소 교체:**

제목:

> Exploratory cohesion settings produce different mixing indices

본문 1:

> Single-seed, two-revolution runs vary the large-NCM self-pair model Bond number (38.4, 384, 1152) or scale all nonzero cohesion-energy-density entries by 10 or 14.42 relative to the low-cohesion comparator.

본문 2:

> Within each explored series, ΔM increases with the imposed cohesion level in each bin grid. These post-hoc comparisons also change wall adhesion and include start-state differences. No verdict is drawn.

그림 범주 예시:

`NCM-pair Bo 38.4 / NCM-pair Bo 384 / NCM-pair Bo 1152 / All-pair CED ×10 / All-pair CED ×14.42`

공간이 좁으면 계열 둘을 시각적으로 구획하고 정의를 그림 위에 짧게 둔다. `one seed chosen after earlier runs`도 `one seed per arm; cohesion levels selected after earlier runs`의 뜻으로 고친다. 후자는 **수준의 사후 선택**이고 seed 자체를 사후 선별했다는 주장은 별개다.

**중요한 비지적:** 실제 LC/LH/높은 NCM/전 쌍 개발 덱은 전부 같은 SE 영률 **2e8 Pa**다. SE×20 경화는 이 개발 비교의 공통 조건이다. 전 쌍 런에만 새로운 강성 교란이 있다고 지적하지 않는다. p11의 원 soft 캠페인과 직접 이어 해석할 때는 세대가 다름을 밝힌다.

### SEMV3-05 — 접착일 식은 조건부 항등식이지 군집 생존의 증명이 아님

**위치:** p13 본문 1·접착 도식·notes. 생성기 `build_seminar_v3.py:722`, `make_seminar_figs.py`의 `fig_mix3_scheme`. 근거 논지 `sources_code/docs/hetero_thesis.md:51–82`.

식 자체를 버릴 필요는 없다. 다만 다음 가정이 필요하다.

\[
W_{AA}=2\gamma_A,\quad W_{SS}=2\gamma_S,\quad
W_{AS}=2\sqrt{\gamma_A\gamma_S}\quad\text{(assumed rule)}
\]

이면

\[
\Delta W=W_{AA}+W_{SS}-2W_{AS}
=2(\sqrt{\gamma_A}-\sqrt{\gamma_S})^2\ge0
\]

이다. **단위는 J/m²**이며, 기하평균 결합 규칙을 둔 **면적당 접착일**의 비교다. 실제 두 접촉을 교환하는 총 에너지와 바로 같지 않다. 네 접촉의 비교 면적이 동일한 A일 때 해당 접착 에너지 기여는 `ΔU=−AΔW`가 된다. 접촉 면적 변화·변형 에너지·동역학은 별도다.

간단한 산술 반례: γA=4, γS=1이면 ΔW=+2 J/m²다. 그러나 AA·SS 면적을 각각 0.1, 원 AS 두 면적을 각각 1로 두면 접착으로 얻는 에너지 차는 `8×0.1+2×0.1−2×4×1=−7`이다. **이는 침대 실측이 아니라, 접촉 수만으로 실제 방출 에너지의 부호를 정할 수 없다는 합성 반례**다.

크기 논거도 비교 대상을 구분해야 한다. 같은 W에서 SE–SE의 무게 정규화 점착력이 큰 NCM–NCM보다 약194.4배라는 산술은 맞는다. 하지만 같은 SE 입자를 붙잡는 상대를 비교하면, 구형 JKR의 `F_pull-off∝WR*`에서:

\[
\frac{F_{SE-NCM}}{F_{SE-SE}}
=\frac{2r_{NCM}}{r_{NCM}+r_{SE}}
\]

이고 `rSE=0.5 µm`, `rNCM=4.5/2.0 µm`에서 **1.8/1.6**이다. 따라서 “SE가 작으므로 동종 접촉을 가장 잘 유지한다”는 결론은 나오지 않는다.

기하평균 근사까지 넣으면 SE–SE pull-off가 SE–큰 NCM보다 커지는 조건은 `γNCM/γSE<0.308642`이다(작은 NCM 비교는0.390625). **이것도 두 접촉의 힘 비교 조건이지 군집 생존의 필요·충분조건이 아니다.** 현재 notes의 `clusters ... would have to be below about 0.31`도 이 한정으로 고친다.

**최소 교체:**

본문 1:

> With equal contact areas and an assumed geometric-mean adhesion rule, ΔW = 2(√γ_A − √γ_S)² ≥ 0 is an adhesive-work difference per unit area. SE–SE cluster survival also depends on relative surface energies and contact dynamics.

도식 위:

> Assumed W_AS = 2√(γ_Aγ_S). Equal contact areas.

도식 식에 `(J m⁻²)`를 붙이고 `like–like ... favoured` 및 `small SE ... holds on most`를 다음으로 교체:

> Conditional adhesive-work comparison. Contact survival is not determined by particle size alone.

본문 2:

> Exploratory all-pair CED scaling retains a larger SE–SE cluster fraction than the low-cohesion comparator. The confirmatory 18-run block remains on hold.

우상단:

> This work: exploratory contact statistics (left), conditional adhesion model (right)

**현재 모델과의 관계도 정확히:** notes의 “SE–SE를 바꾸지 않았다”는 설명은 새 전 쌍 CED 런에는 맞지 않는다. 이 런은 SE–SE도 바꾼다. 남는 한계는 **측정된 표면 에너지·코팅 선택성으로 위 접착 규칙을 보정한 모델이 아니라는 것**이다. `The CED-scaling runs do not validate a surface-energy-based coating mechanism.` 정도로 제한한다.

**무너지지 않는 것:** 전 쌍 CED 런의 큰 SE–SE 군집 분율, 덤프 해상도 구간의 비중첩, 18런 HOLD, 가정하의 ΔW 항등식. 실 코팅 효과나 실제 분말의 분리 메커니즘 검증으로 승격하는 부분만 불허한다.

## 5. Q-V3-2 새 그림 10개 수치 대조

| 그림 | 실제 대조 결과 | 판정 |
|---|---|---|
| F_poro | 원 union값 20.5892·18.6664·17.6696·16.4941·16.8990% → 20.59·18.67·17.67·16.49·16.90 | 일치 |
| F_trans | τ 7.2433·5.9733·5.4495·5.0297·5.2864, σion 0.0587·0.0730·0.0814·0.0893·0.0838 mS/cm | 저장 원값 반올림과 일치. 두 y축 0 시작 |
| F_limits | 공개 격자비, 54.0/70.6 대4.47/12.4, ps45 인자 끔0.391·0.406·0.402·0.375·0.467 mS/cm | 일치. 미세격자 HOLD 값 없음. 새 조판 겹침은 별도 |
| F_load | 21단면에서 Σ(load×share)/Σload로 재계산. NCM–NCM59.562243·54.634924·52.371659·48.463893·56.914398% | 일치. 단면비율의 단순평균이나 NCM 상 전체 몫 아님 |
| F_vgcf | 원판 10 GPa primary96의 평균12점 재계산 | 12/12 일치. 100 GPa 재현과 출처 분리 필요 |
| F_dataset | 배포 CSV194행, (a) 유한τ170+비관통24, (b)130행 | 행별 일치. 고체 중 SE분율 축도 맞음 |
| F_mix1 | 열 런 최종 M와 bin 내 SD, 주 짝차·seed SE | 일치. 물리·등록 해석 제한은 §4 |
| F_mix2 | 저장 s²와 M에서15개 ΔM 재계산 | 13/15는 세 자리 반올림 일치. 두 점은 §6 교정 |
| F_mix3 | 세 런×100프레임의 군집율/lo/hi 평균 | 두 평균 및 모든 범위 일치. 비교군 평균은 .401→.400 |
| F_mix3_scheme | 실제 측정 그림이 아니라 조건부 모델 산술 | 가정·단위·생존 추론을 §4대로 고쳐야 함 |

하중 기여율의 0:10 세 항 합이99.999%인 것은 0.001%p 반올림 잔차로, 별도 결함이 아니다. 비관통24개의 ×를 y=1에 둔 것도 실제 τ=1 대입이 아니다. CSV는 결측이며 그림의 표시 위치다. 의미를 더 분명히 하려면 `×: no spanning path (display position only)`를 선택적으로 덧붙인다.

SE 군집 구간은 통계적 CI가 아니다. 재계산 결과는 다음과 같다.

| 설정 | 평균 | 덤프 해상도 범위 |
|---|---:|---|
| 작은 비영 점착 대조군 | 0.400491487 | [0.143419088, 0.541985854] |
| 전 쌍 CED×10 | 0.953993836 | [0.875368565, 0.956633860] |
| 전 쌍 CED×14.42 | 0.987893195 | [0.980641540, 0.987929571] |

두 높은 점착 설정의 하한은 대조군 상한보다 각각0.333383,0.438656 크다. 이 **한 시드 개발 자료의 해상도 범위 비교**는 유지된다. seed uncertainty, 무작위 기준 대비 응집, 실제 코팅 효과의 증거는 아니다.

## 6. P1과 선택적 P2

### SEMV3-06 — P1 수치 반올림 세 곳

| 위치 | 원자료 계산 | 현재 | 권장 세 자리 |
|---|---:|---:|---:|
| p12 NCM Bo384, 12×12×3 | 0.927486131 | 0.928 | **0.927** |
| p12 전 쌍 CED×14.42, 16×16×4 | 0.865460626 | 0.866 | **0.865** |
| p13 작은 비영 점착 대조군 평균 | 0.400491487 | 0.401 | **0.400** |

README의 요약 반올림을 베낀 차이다. 원 프레임 산술에서 바로 반올림하고 상수·CSV·그림·notes를 같이 맞춘다. 순위나 효과 분류가 바뀌는 오류로 과장하지 않는다.

### SEMV3-07 — P1 p7 그림과 순서 재현의 강성 세대 구분

현재 그림은 `phase_a_104arms_20260921`의 **VGCF E=10 GPa 원판**이다. `notes/sources/report_make_figs.py:139–147`이 그96팔을 읽고, 이번에도 실제96팔을 다시 평균 내12점 일치를 확인했다. notes가 연결하는 `phase_a_rep100_20260930`은 **100 GPa 재현**이다.

예를 들어 vox0.15, wt2/3의 원판 평균은 **15.238690545/59.338749268 mS/cm**로 현재15.24/59.34와 맞는다. 새100 GPa 평균은 **15.290288606/59.545460512 mS/cm**다. 따라서 현재 그림을 후자 평균으로 설명하면 틀린다. 두 세대 모두 순서72/72는 유지된다.

그림값을 바꿀 필요 없이 캡션에:

> Original Phase A campaign (VGCF E = 10 GPa). Means of 96 primary arms.

notes에서100 GPa 재현의72/72를 별도로 연결한다. 이 수정은 절대값의 출처를 명확히 하는 것이며 순서 판정의 철회가 아니다.

### SEMV3-08 — P1 p9 순위 일치 대상에 experimental 복구

현재 `The porosity ranking agrees ...`는 앞 p3의 DEM 공극률과 같은 순위라는 뜻으로 읽힌다. 실제 오름차순은:

- DEM 공극률: **7:3 < 10:0 < 5:5 < 3:7 < 0:10**
- NCM–NCM 하중 기여율: **7:3 < 5:5 < 3:7 < 10:0 < 0:10**

둘의 Spearman ρ는0.7이다. 기존 허용 문장의 일치 대상은 **선택된 실험 공극률 요약값**이었다. 다음으로 명시한다.

> The NCM–NCM stress-share ranking matches the experimental porosity summaries for the selected five compositions (exploratory, n = 5).

선택된3-of-n 평균·불확도 미확립은 notes에 유지. 되튐 원인이나 강성 역산을 입증했다고 하지 않는 기존 한정도 그대로다.

### SEMV3-09 — P1 실제 렌더에서 남은 네 조판 문제

| 장 | 확인된 문제 | 최소 조치 |
|---|---|---|
| p6 | So 크롭의 우측500 눈금·끝 데이터가 잘림 | `SO_CROP` 오른쪽 경계0.475를 원 패널 전체가 들어오도록 확장. 데이터는 수정하지 않음 |
| p8 | `DC polarization` 범례와(c) `Electronic conductivity` 세로축 교차. 제목(b)/(c)도 붙음 | 범례 위치/줄바꿈과 패널 간격 조정. 폰트를 더 줄이지 않음 |
| p11 | 첫 두 x축 범주가 붙음 | §4의 정확한 라벨로 바꾼 뒤 줄바꿈·그룹 간격 확보 |
| p12 | 첫 세 x축 범주가 겹침 | Bo/CED 구획 후 폭·비율·tick배치 조정 |

PPT 본문15pt 및 해석12pt 시험은 그림 속 글씨까지 보장하지 않는다. 실제 배치 환산으로 p8 조성tick 약8pt, p11 범주9.3pt, p12 범주8.6pt, p13 범주9.2pt다. 다만 작은 그림 전체를 일괄 실패로 보지 않고 실제 충돌을 우선한다.

**p13 우측 잘림은 없다.** 독립1600px 렌더에서 출처 줄과 도식 마지막 줄이 슬라이드 내부임을 확인했다. 대화창 미리보기의 표시 폭과 실제 파일 잘림을 혼동하지 않았다.

### SEMV3-10 — P1 제한 설명의 잔여 정리

- p6 notes의 `inside the literature range`는 해당σy 범위의 독립 근거 없이 남겨둘 수 없다. `selected in the pure-SE calibration sweep`까지만 두면 충분하다.
- p5 `No shape change and no yield cap`은 모든 DEM의 한계처럼 쓰지 말고 **우리 fixed-shape 구현**의 설명으로 제한한다. 문헌 그림은 더 넓은 탄소성 접촉 모델이다.
- p11 `M=1: fully mixed` 대신 `M=1: random-reference variance`가 정확하다. 모든 길이 척도에서 완전혼합이라는 뜻은 아니다.
- p13 현재모델 설명은 §4대로 고친다. 새 all-pair 런에도 “SE–SE를 안 바꿨다”는 옛 설명을 붙이지 않는다.

P2 선택 개선: p9 stress 색막대가 투사에서 너무 작으므로 외부에 큰0/75/150 MPa 눈금을 덧붙일 수 있다. p10 범례를 실제 고τ점에서 떼고 Tier1을 `order-of-magnitude agreement`로 풀어도 좋다. p5 압축 구간 감쇠58%와 p6 현재 실행 상태는 청중이 이슈를 이해하는 데 도움이 되지만, 현 pending 한정 아래에서는 화면 복구 자체를 필수 P0로 만들지 않는다.

## 7. 최종 답과 종결 확인표

| 질문 | 답 |
|---|---|
| Q-V3-1 | p5/p7의 합친 설명은 핵심 의미 유지. 모든 변경을 “그대로”로 묶을 수는 없음. 새로운 출처·용어 오류는 위 항목별 수정 |
| Q-V3-2 | 주요 수치·194행·하중 가중·원판VGCF 평균 일치. 믹서 반올림 세 점과 출처 세대, 새 그림 내부 조판 수정 |
| Q-V3-3 | 한 시드·사후 수준·공동 벽·QC 해칭·미판정 표지는 대체로 좋음. 그러나 비영 대조군·등록 전체와 진단 분기·Bo/CED·접착일 가정은 P0 |
| Q-V3-4 | p5/6/7/10의 상세 notes 이동은 대체로 허용. 결론을 한정하는 믹서 정의·가정은 화면에도 복구 |
| Q-V3-5 | **조건부 GO. SEMV3-01–05 수정 후 발표 가능.** 현 파일을 무수정 최종판으로 승인하지 않음 |

다음 반입에서 전면 재심할 필요는 없다. (1) p6/[9] 실제 출처, (2) p11–13 모든 비교군·배율 라벨, (3) p11/12/15 제목과 진단 지위, (4) p13 가정·단위·군집 해석, (5) 세 반올림 및 새 조판을 **수정한 실제 PPT와 PDF**에서 확인하면 된다. P1은 가능한 한 같은 편집에서 정리하되 새로운 물리 검증 캠페인으로 확대하지 않는다.

의도된 네 공백(p5우측,p7좌측,p11우측,p12우측), 표지 날짜,17장 압축은 결함으로 세지 않았다. 이후 발표자가 새 캡처를 넣으면 그 캡처의 팔·상태·전류/응력 단위는 별도 확인 대상이다. 이 판정은 시뮬레이션 발사나194/보충20/v1.3 배포 승인이 아니다.

### 재현

검토 폴더에서 표준 Python으로 저장 자료 산술만 실행한다.

```bash
python notes/audit_root.py
python notes/audit_charts.py --save
python notes/audit_mixing.py --save
```

주요 증거: `evidence/root_checks.json`, `charts_arithmetic.json`, `mixing_repro.json`, `mixing_frame_recalculation.json`, `so_figures_source.json`, 실제 본문·notes 추출 `all_slide_text.txt`, 독립 렌더17쪽. 재현기는 시뮬레이션이나 그림 생성기를 호출하지 않는다. `inspect_delivery.py`는 이 환경의 원 ZIP·이전 v2 비교자료를 읽었던 추출 기록이며 위 세 산술 재현기의 필수 의존성은 아니다.

**최종 판정: 조건부 GO**
