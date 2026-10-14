# v3.2 문헌·계획 표현 독립 재검토 (문헌 담당)

작성: 2026-10-15. 범위 = 요청서 Q5의 p5 실험 계획, Q6의 신규 문헌 6건, Q8의 인용 대응·연결 문장. 전체 덱의 수치·실행 상태 판정을 대체하지 않는다. 시뮬레이션·생산 코드·덱 변경 없음.

## 요약

- 이 범위에서 **새 P1/P2는 발견하지 않았다**. p7·p10·p14는 문헌의 다른 계·압력 상태·관측량을 우리 결과의 검증으로 승격하지 않도록 중요한 한정어를 갖추고 있다.
- p13 notes의 Kissel 요약 한 문장만 **P3 표현 교정 권고**: 응력 횟수를 배제하는 듯한 `rather than`을 완화할 것. 본문의 과학적 핵심과 드럼 결과 판정은 바뀌지 않는다.
- p5의 `planned`, `no results yet`는 계획을 실험 결과로 읽는 것을 막는다. 대입자 LPSCl은 진행 원장의 승인 상태와 문서 간 시점이 다르므로, 승인/실행 완료를 이 리뷰가 확인한 것으로 쓰지 않는다.

## 자료·핀·확인 수준

- 덱 텍스트: `input/repo/docs/seminar_20261013/slide_text_v32.md`; 출처 연결: `slide_sources_v32.json`; 대상 코드/문서 핀 = `90ca2c8cd` (부모 리뷰에서 확보).
- 신규 litdb 카드 6개는 GitHub 커넥터로 `claude/friendly-meitner-lldvar`에서 읽어 `agents/lit/`에 저장했다. 이 사본은 10-15 조회본이며 **덱 핀과 같은 커밋이라는 뜻이 아니다**. branch HEAD 커밋은 부모 측에서 별도 고정; 아래 원문 크롭은 개별 blob SHA로 고정했다.
- Faka·Thompson·Kissel은 출판사 원문 HTML을 읽었다. Faka Fig. S2, Egermann p.118 문단, Kim Fig. 9는 litdb에 저장된 **원문 이미지 크롭을 직접 시각 판독**했다. 카드 산문만의 반복과 구별한다.
- Hersey: 출판사 서지/초록과 카드 p.42 인쇄문 대조. 전체 원문 p.42를 이번 환경에서 별도로 내려받아 읽은 것은 아니다. Kim은 출판사 서지 및 원문 Fig. 9 크롭; 전체 PDF의 계산 방법은 카드의 페이지별 전사와 대조했다.
- 원문 크롭 자체가 원본 PDF와 동일한지 전체 PDF 단위 해시로 인증한 것은 아니다. 이는 잘못된 인용의 증거가 아니라 검증 범위의 한계다.

## Q5 — p5의 계획 표현

위치: `slide_text_v32.md:116`(화면), `:122`(notes).

**판정: 현재 화면 문구 수용.** `Lab anchor (planned)`와 `no results yet`가 함께 있고, 기존 10 % 순수-SE 보정 타깃은 별도 행이다. 따라서 NCM 0.1/0.2/0.3 g PC·SC, 소립·대립 LPSCl의 예정 측정을 완료된 데이터로 읽을 직접 근거가 없다. EIS/DC 실험 설계의 식별성이나 표본 수를 승인하는 판정은 아니다.

주의: notes는 대립 LPSCl을 저자 10-14 계획이라고 하면서 진행 원장에는 아직 답 대기라고 정확히 밝힌다. 발표 전에 실제 계획 상태를 다시 맞추면 좋지만, **계획임을 이미 명시한 문장을 결과 위조/검증 완료로 판정할 수는 없다.**

## Q6 — 신규 문헌 6건

### [13] Faka 2026 — p7·p10

- 서지: V. Faka et al., *How Particle Size Affects Consolidation Behavior, Strain and Properties of Li6PS5Cl Fast Ionic Conductors*, **Advanced Energy Materials 16, e05186 (2026)**. [출판사 본문](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/aenm.202505186).
- 본문 §4.2는 가압 중 상대밀도, 피스톤 이동으로 얻는 실험 밀도와 결정학적 밀도의 구분을 설명한다. p7의 `in the die at 0.3 GPa`는 적절하다. p10 notes의 in-die와 out-of-die/elastic recovery 구분도 맞는다.
- Fig. S2 원그림을 직접 보면 p=0.3 GPa에서 40/20/11/4 µm 곡선의 상대밀도는 대략 87/84/77.5/74 %다. 따라서 ε=100−ρ_rel의 **약 13–26 %** 표기는 그림 판독 정밀도에 맞는다. notes의 12.9/16.0/22.5/26.3 %는 카드의 정밀 디지타이즈 값이며 이번 육안 판독으로 그 소수 첫 자리까지 독립 인증하지는 않는다.
- 위치: `slide_text_v32.md:146`, `:148`, `:191`. `not composite beds`, `Neither is a validation ...` 유지 권고. 순수 SE의 값으로 복합양극 공극률을 검증했다고 하지 않는다.
- **판정: 수용.**

### [12] Thompson 2026 — p7·p10 notes

- 서지: O. Thompson et al., **Advanced Functional Materials 36, e75195 (2026)**, DOI 10.1002/adfm.75195. [출판사 본문](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adfm.75195?af=R).
- 원문 CT 설명: 1.277 µm 공간 샘플링, 479 MPa에서 대부분의 입계 공극 닫힘, 1155 MPa에서 분해 가능한 공극 소실. 더 작은 잔류 공극 가능성을 논문도 남긴다. 덱의 **`no pores resolved`**는 `porosity=0`과 다르며 적절하다.
- 감압에서 피크 위치 복원과 피크 폭/전도도 변화의 잔류를 구별한다. 덱은 감압 하한 ≈1.1–1.8 GPa, 별도 전도도 셀, 순수 LPSCl이라는 한정을 보존했다. 이를 무하중 springback 실험이라고 바꾸면 안 된다.
- 위치: `slide_text_v32.md:148`, `:191`.
- **판정: 수용.**

### [4] Hersey 1975 — p12·p14

- 서지: J. A. Hersey, *Ordered Mixing: A New Concept in Powder Mixing Practice*, **Powder Technology 11, 41–44 (1975)**. [출판사](https://www.sciencedirect.com/science/article/pii/0032591075800210), DOI 10.1016/0032-5910(75)80021-0.
- 미분이 큰 운반 입자 표면에 붙어 단위체를 이루는 혼합을 소개한 인용은 적절하다. 무작위 기준 균질 지수의 한계는 카드의 p.42 원문 전사와 맞는다. 이는 현재 드럼에서 그 형태가 실현됐다는 실험 증거가 아니다.
- 덱은 현재 M이 무작위 기준임을 밝히고, 문헌의 용어를 현재 코팅 재현의 증거로 사용하지 않는다.
- 위치: `slide_text_v32.md:219`, `:243`, `:245`.
- **판정: 수용(전체 원문 독립 열람 한계는 위 참조).**

### [5] Egermann & Orr 1983 — p12·p14

- 서지: H. Egermann and N. A. Orr, *Ordered mixtures — Interactive mixtures*, **Powder Technology 36, 117–118 (1983)**, DOI 10.1016/0032-5910(83)80016-3.
- p.118 원문 크롭은 혼합물 유형을 interactive/non-interactive로, 균질 정도를 ordered(σ<σ_R)/pseudo-random/incomplete로 나누자고 명시한다. 덱의 두 용어 구별은 원문과 맞는다.
- **용어 제안**이라는 지위가 중요하다. ordered와 interactive의 동의어 사용, 또는 interactive이면 반드시 σ<σ_R라는 해석은 금지지만, 덱은 그렇게 쓰지 않는다.
- 위치: `slide_text_v32.md:219`, `:243`, `:245`.
- **판정: 수용.**

### [6] Kissel 2026 — p13 notes

- 서지: M. Kissel et al., *Mechanofusion-derived cathode composite microstructures with scalable mixed conducting matrix coatings for solid state batteries*, **Nature Communications 17, 3215 (2026)**. [출판사 본문](https://www.nature.com/articles/s41467-026-71305-2).
- 고강도 믹서의 coarse-grained DEM으로 전체 응력 조건을 추정한 것이고, coating progression 자체를 DEM으로 재현하지 않았다는 구별은 원문과 맞는다. 다른 재료·믹서라는 덱의 한정도 적절하다.
- **P3 후보 LIT32-01:** 위치 `slide_text_v32.md:231`, 마지막 문헌 요약. `coverage followed the stress intensity rather than the number of stress events`는 횟수의 영향을 배제하는 쪽으로 읽힌다. 원문 Fig. 6c,d 설명은 같은 횟수라도 강도가 다르면 피복이 달라지지만, 낮은 강도에서도 횟수/시간이 증가하면 피복이 증가한다고 명시한다. 이는 문장 압축의 문제이지 드럼 실측 반례는 아니다.
- 교체안: **“Coating coverage depended on stress intensity as well as stress number; increasing stress number alone did not collapse results across rotor speeds.”**
- XPS coverage가 순수 기하 표면 피복과 같지 않다는 원문 한정도 발표 중 질문에 대비할 만하다. 현 덱은 그 값을 우리 표면 피복률과 수치 비교하지 않으므로 추가 HOLD 사유는 아니다.
- **판정: 본질적 인용 수용, 문장 교정 권고(P3).**

### [7] Kim, Lee & Kang 2012 — p14

- 서지: Y. Kim, H. Lee and S. Kang, *First-principles and experimental investigation of the morphology of layer-structured LiNiO2 and LiCoO2*, **Journal of Materials Chemistry 22, 12874–12881 (2012)**. [출판사](https://pubs.rsc.org/en/content/articlelanding/2012/jm/c2jm31145c), DOI 10.1039/C2JM31145C.
- Fig. 9 원그림의 다섯 면 모두 LiNiO2 표지가 LiCoO2보다 낮다. 덱의 `clean-slab DFT γ: LiNiO₂ < LiCoO₂`는 이 비교를 정성적으로 충실히 옮긴다.
- notes는 끝 조성(우리 NCM 아님), 0 K 청정 슬랩, 입자 접촉의 W와 다름을 유지한다. 따라서 이것을 NCM/SE 접착비의 실측으로 쓰지 않는다. Ni 함량만으로 실제 분말의 부착력을 예측한다는 과장도 없다.
- 위치: `slide_text_v32.md:243`, `:245`.
- **판정: 수용.**

## Q8 — 인용 번호·연결 문장

텍스트 전수 검색 후 숫자 구간 `[0, 1]`과 p17의 옛→새 번호 설명을 인용으로 오독하지 않도록 수작업 대조했다. 사용 번호는 1–13이고 모두 p17에 대응한다. 신규 여섯은 [4]·[5]·[6]·[7]·[12]·[13]로 본문 또는 notes에 실제 쓰인다. 고아 문헌/새 번호 오연결은 발견하지 않았다.

15개 Bridge 문장은 이동 경로를 안내한다. `Model chain set`(p6)은 검증 완료라는 뜻으로 해석할 여지가 조금 있으나, p2의 unresolved validation 및 p6 본문 한정과 함께 읽으면 새 과학적 주장으로 보기 어렵다. 원하면 `Model components outlined — next: results from the simulated beds`로 더 명확히 할 수 있으며 **필수 수정 finding은 아니다.**

## 원문 이미지 증거

아래 `.png`는 GitHub base64 원문 응답을 디코딩한 파일. 이미지 편집 없음. 저장 위치 `agents/lit/`.

| 파일 | repo blob SHA | 로컬 SHA256 |
|---|---|---|
| faka_fig_S2.png | 287381b4808ae0e27c4b40953eff080d6d419e3b | 133f162da4154a4f8604415e842aba4fef06258c4d1bddc778cd56842ac43c0a |
| egermann_p118.png | 26204df72de2523afd7861cbe363f9f8286c4225 | c7bcac0162aa7bc69ed49a1528b3a821c3d5b1cf899115621c37bd6f31420f7c |
| kim_fig_9.png | 4f86f45311495ec5ade363ab42b8c99b34d342c0 | 15ad01919b17910d43f1f1ccff7ecbfa4fec1f2f08aef51ce31235604ace2668 |

## 최종 한정

**문헌 추가·인용 정리·계획 표기만으로 덱 전체 GO를 내리는 것은 아니다.** p9의 실행 상태, p11의 프로토콜 판정, p12–p14 원자료 수치는 해당 담당 리뷰를 따른다. 이 문헌 범위의 필수 차단점은 새로 확인되지 않았다.
