# p10–p19 시각·가독성 및 후반 흐름 검토

검토 범위: 실제 v3 contact sheet, p10–p19 렌더, PPTX 본문 상자/글자 크기, 생성기의 그림 배치. 원본 PPTX·PDF·그림·코드는 수정하지 않았다. 과학적 판정은 이전 검토의 SEM-03/04/05/06/08 등을 이어받으며 이번에는 정본 원자료를 다시 계산하지 않았다. 원래 10-13 템플릿 파일은 없으므로 ‘같은 템플릿과 정확히 일치’한다고 판정하지 않는다. 요청서가 제시한 문법과 현재 렌더의 내부 일관성만 판단한다.

## 첫인상과 전체 판단

3초 첫인상: **실제 연구 그림이 중심인 연구실 진행 보고로 보이지만, 긴 한정문과 작은 그림을 같은 틀에 반복해서 넣어 발표보다 검토 문서처럼 읽힌다.**

같은 틀 12장, 꺾쇠 캡션, 점선 프레임 자체는 제공된 연구실 문법이므로 AI 티라고 일괄 삭제할 근거가 없다. p10–p15에서 그림 높이를 거의 같은 위치에 고정하고 제목·본문 길이에 무관하게 윗부분을 크게 비워둔 결과, 그림의 실제 글자가 지나치게 작아진 점은 수정 대상이다. p11 ‘What survives’의 초고 회고, p14·p16·p17의 등록/봉인/재검증 반복이 과학 이야기보다 검토 절차를 앞세운다. 이를 제거·notes 이관하면 밀도와 기계적인 어조가 같이 줄어든다.

현 상태 그대로는 **NO-GO**. 이는 그림 6칸이 비어서가 아니라 p11 계열 혼동, p13 접촉 종류 오기, p14 HOLD/세대 혼합, p16/17의 포괄적 완료·미완료 문구, p12의 범주 라벨 결손이 남기 때문이다. 아래 P0를 한 번의 편집으로 반영하고 재렌더 확인하면 조건부 GO로 전환할 수 있다. 새 런, 수치 재계산, 19장 순서 변경은 필요하지 않다.

좌표는 10×7.5in 슬라이드의 좌상단 기준 `(x, y, w, h)`이다. 제안 좌표는 원본 수치가 아니라 편집용 배치 사양이다. 절 표지 24pt·로고·바닥글·글꼴·표지 날짜는 그대로 유지한다.

## 공통 글자 크기와 그림 규칙

- 본문 bullet은 요청서의 기준 덱 크기인 **15pt로 복귀**하되 먼저 문장을 줄인다. **■ 주제목은 XML의 상속을 포함한 실제18pt를 유지**한다. 요청서의 ‘제목15pt’와 단순 직접 run 크기 목록은 상속 크기를 반영하지 못한다. 아래15pt 지정은 본문 bullet에만 적용하며 주제목까지 일괄 변경하지 않는다. 내용이 늘어날 때 bullet을13pt로 되돌리지 않는다.
- p10–p13·p15 본문 상자 현재 `(0.61,1.08,8.84,2.25)`는 길이에 비해 일률적으로 크다. 축약 후 `(0.61,1.08,8.84,1.65)` 안에서 제목 1줄+본문 2줄 또는 짧은 2개 bullet을 목표로 한다. 그림 영역을 y=3.45에서 **y=2.95 전후**로 올린다.
- 주장 해석에 필요한 캡션·경고는 **12pt**, 핵심 축/범주/범례는 최종 슬라이드상의 **12pt 이상**을 목표로 한다. 일반 출처 10–11pt, 로고·쪽 번호는 유지 가능하다. 10pt 출처를 청중이 뒷줄에서 읽어야 논지가 성립하는 구성은 피한다.
- F2/F3/F4의 원본은 11×8.2cm, 기본9pt·범례8pt다. 이를 현재 4.1×2.6in fitbox에 넣으면 높이 기준 약0.805배가 되어 최종 약7.3pt·6.4pt다. PPTX 본문을 키우는 것만으로 해결되지 않는다. 새 4그림은 수정 허용 범위이므로 Origin 재제작 시 **최종 배치 크기를 먼저 정하고 축·눈금·범례를 12pt로 지정**한다. 값·범위·데이터는 바꾸지 않는다.
- 재사용 그림은 다시 그리지 않는다. 바깥 흰 여백만 줄이고 축·범례·색상 막대를 보존해 확대한다. 원그림의 작은 내부 글자는 발표용 핵심을 12pt 바깥 캡션으로 설명하거나, 보조 패널을 notes로 옮겨 확대 공간을 확보한다.

## 장별 구체안

### p10 첨가제: 손질, P1

첨가제는 역학 단계에서도 쓰이므로 현재 제목의 ‘enter at the voxel stage’는 최초 도입 시점을 잘못 제한한다(교차검토 SEM-12). 수송용 격자 표현이라는 실제 그림 주제로 바꾼다. 또 왼쪽 두 그림의 아주 작은 상단 제목에만 ‘실제 침대의 seed/합성 preview’ 구분이 들어 있어 두 모식도가 오른쪽 수치 그래프의 실제 관측 상태처럼 읽힐 수 있다. 내부 그림 파일·값은 유지하고 바깥 캡션으로 지위를 설명한다.

■ 제목은18pt, 아래본문 bullet은15pt로 한다.

> Additive geometry used in transport rasterization
>
> VGCF fibres, insulating PTFE and conductive polymer use distinct voxel representations.
>
> The VGCF conductivity order holds across the tested grids and origin offsets (72/72).

직경 보존/centre-line/true-diameter 상세와 ‘104-arm pre-registered’는 notes로 옮긴다. 동일 내용이 p14에도 반복된다. 접촉저항 미포함은 그림 오른쪽 아래 한 줄 `Ideal interfaces in the results shown`로 12pt 표기하면 p9·p11과 연결된다.

- 그림 배치 제안: 왼쪽 `(0.50,3.00,2.75,2.65)`, 가운데 `(3.30,3.00,2.75,2.65)`, G6 `(6.30,2.85,3.35,2.90)`.
- 캡션 y=5.95, 12pt: `< additive seeding illustration >`, `< synthetic morphology example >`, `< VGCF conductivity ordering >`.
- 마지막 캡션의 현재 `σ(e⁻) vs VGCF wt%, three voxel sizes`를 줄이면 오른쪽 캡션의 긴 한 줄을 해소한다. 세 격자 값과 단위는 그래프에 그대로 남긴다.

### p11 격자: 다시, P0

제목이 2줄이고 본문도 4줄, 우측 12pt 회고문까지 있어 핵심 그림이 작다. 시각 개선과 함께 이전 SEM-03을 적용해야 한다. ‘멱법칙 불성립’, ‘does not extrapolate’, ‘changes sign’, ‘the shape is real’를 이 공개 세 점의 결론으로 두지 않는다.

> Problem 1: Grid dependence
>
> The electronic ratio decreases as the voxel spacing decreases. The ionic ratio crosses 1.
>
> Grid convergence has not been established.

- 본문 `(0.61,1.08,8.84,1.55)`, 15pt.
- F2 `(0.65,2.85,5.20,3.15)`. 축 제목 `Conductivity ratio, with / without conductive polymer` 또는 SDCP가 앞에서 정의되어 있을 경우 기존 `with / without SDCP` 유지. ‘gain’으로 축을 줄이지 않는다. 비=1 기준선과 공개한 세 간격을 유지한다.
- 우측 상자 `(6.05,3.05,3.30,1.40)`, 15pt: `No converged conductivity ratio is reported.` 이것 하나로 충분하다. ‘earlier manuscript’, 한 GPU 메모리 및 외삽 논의는 notes로 옮긴다. HOLD 계열 추론을 notes에서 살아 있는 근거로 남기지 않는다.
- 캡션 `(0.65,6.10,5.20,0.45)`, 12pt: `< ratio at three tested voxel spacings >`.
- 내림차순 x축은 작은 격자로 가는 방향이라 유지 가능하다. 차이를 양의 ‘gain’이라고 읽게 하지 않도록 y축은 ratio를 유지한다.

### p12 절대 전도도: 다시, P0

F4는 **다섯 막대인데 0:10과 7:3만 x라벨이 보인다**. 텍스트 선택자가 범주 지정 뒤 덮어써지는 생성기 순서도 확인했으나 코드는 수정하지 않았다. Origin 재제작 또는 생성기 편집에서 다섯 범주를 고정한다: `0:10`, `3:7`, `5:5`, `7:3`, `10:0`. 물리 값 수정은 필요 없다.

> Problem 2: Absolute electronic conductivity
>
> The voxel predictions exceed the available DC-polarization estimates. Measurement conditions remain unverified.
>
> The NCM–SE comparison uses a common NCM conductivity and idealized contacts.

첫 문장에 숫자를 계속 두려면 현 값의 정밀도/범위를 과학 검토안과 맞춰 넣되, 좌측 그림 위 모델-측정 비교와 우측 별도 접촉망 조건을 한 원인 서술로 합치지 않는다. `no interface resistance, unanchored carbon conductivity`는 원인 확정처럼 붙이지 말고 검토 대상 가정으로 notes 또는 별도 짧은 조건문에 둔다.

- F3 `(0.60,2.95,4.35,3.00)`, F4 `(5.10,2.95,4.35,3.00)`.
- 왼쪽 캡션 `(0.60,6.10,4.35,0.50)`, 12pt: `< model and DC-polarization estimates, log scale >`.
- 오른쪽 캡션 `(5.10,6.10,4.35,0.50)`, 12pt: `< NCM–SE contact-network calculation >`.
- 두 캡션을 두 줄 허용하면 지금 중앙에서 거의 붙는 긴 한 줄을 해소한다. 왼쪽은 로그 축을 유지하되, 새 F3의 표시 형식은 **같은 y값의 점 도표**로 바꿔도 된다(P1). 로그 막대의 길이를 ‘차이 비율’로 읽는 위험을 줄이며 값은 변하지 않는다. 오른쪽 막대는 0 시작이므로 그대로 가능하다.
- 측정 조건 미확인과 오른쪽의 `Carbon- and binder-free` 조건은 화면에 남긴다. 긴 Hertz H0·공통4.1·경험 크기 인자 OFF·단일 침대 조건 전체는 과학 검토에서 정한 최소 캡션/각주로 정리하고 12pt로 읽히게 한다. 정보가 늘면 위 본문 숫자 반복을 덜어 공간을 확보한다.

### p13 하중분담: 다시, P0 + P1

현재 본문은 Large–large, 그림 범례는 AM–AM이므로 청중이 같은 열을 서로 다른 대상으로 읽는다. 이전 SEM-04에 따라 AM 전체 접촉으로 정정한다. 열지도 색상 막대는 뒷줄에서 판독 불가능한 수준이고, 벽 SE 제외 조건이 화면에 없다.

> Problem 3: Load sharing during compaction
>
> NCM–NCM contacts carry 48–60% of vertical stress after relaxation at fixed platen position.
>
> The porosity ranking agrees for the selected five compositions (exploratory comparison).

`7:3 is the minimum`은 왼쪽 그래프의 강조점과 notes에 맡겨 본문에서 덜어낼 수 있다. 48–60/n=5 등 기존 수치는 유지한다. 원그림을 압축 최고점·무하중 제하로 설명하지 않는다.

- 왼쪽 주 그림 `(0.50,2.95,4.25,3.00)`, 오른쪽 4단계 그림 `(4.95,3.10,4.65,2.80)`. 오른쪽은 보조 정성 맥락으로 둔다. 4단계 색상만으로 원인이나 되튐을 주장하지 않는다.
- 왼쪽 캡션 `(0.50,6.10,4.25,0.48)`, 12pt: `< vertical-stress contribution by contact type >`.
- 오른쪽 캡션 `(4.95,6.03,4.65,0.58)`, 12pt 두 줄: `< SE von Mises stress, 0–150 MPa >` / `Wall SE particles excluded`.
- 그림 자체 눈금을 고쳐 그리지 않으며, 보존한 색상 막대의 범위를 바깥 캡션에서 읽게 한다. 열지도를 크게 만들기 위해 세부 상태값을 새로 합성하지 않는다.

### p14 진행: 다시, P0

가장 뚜렷한 후반 밀도 병목이다. 현재 탭 `(1.02,2.26,2.03,0.36)`의 `Registered campaigns`가 두 줄로 넘쳐 프레임 안 첫 행에 가까워진다. 오른쪽 13pt 문구는 회색인데 중요한 판정을 담고 있고, 각 행 높이가0.5in라 두 줄 내용이 다음 행과 거의 붙는다. 아래 빨강 HOLD 문구와 첫 행의 살아 있는 듯한 gain 결론도 충돌한다.

제목 `Registered studies and current status`, 상단 포괄 보증 bullet은 삭제하고 세부 절차는 notes로 옮긴다. 탭은 같은 위치/크기에서 `Study status` 한 줄, 15pt. 점선 프레임 문법은 유지한다.

좌우 상자 폭을 바꿔 항목 이름을 줄이고 설명 영역을 넓힌다. 왼쪽 x=0.80,w=3.75, 오른쪽 x=4.75,w=4.55. 전체 점선 프레임 `(0.55,2.40,8.90,3.25)`로 높이를 늘린다. 다섯 행 y=2.72/3.26/3.80/4.34/4.88, 높이0.48in, 글자14–15pt. 중요한 상태문은 본문색, HOLD만 빨강.

| 왼쪽 항목 | 오른쪽 최소 문구 |
|---|---|
| Historical eight-origin study | Conductivity estimates and inference remain on hold |
| VGCF ordering study | Ordering holds across tested grids and offsets (72/72) |
| Absolute-conductivity comparison | R = 2.07 (Tier 1), Q = 0.84 |
| 194-bed dataset v1.2 | Released for conditional use as model descriptors |
| Updated transport software | Seven reviews completed. Production remains pending |

4행의 배포와5행의 재검증은 이전 SEM-06의 다른 세대 이력을 분리한 것이다. 내부 세대 코드 대신 평범한 이름을 쓰며 상세 날짜/판정범위는 notes에 둔다. 8팔 h1 결과 문장은 notes까지 현재 성과로 인용하지 않는다(SEM-05).

R/Q는 그 자체로 낯선 기호이므로 `(0.80,5.85,8.60,0.58)`, 12pt에 `R: model / literature conductivity. Q: conductivity retained after PTFE treatment.`를 넣는다. 기존 `prediction met`·`order-of-magnitude agreement`는 긴 결론 대신 필요한 Tier 1 한정을 남긴다. replay0.00000%,104arms,16arms 및 등록·봉인 설명은 notes로 이동 가능하다. 값은 삭제/notes 이관일 뿐 변경하지 않는다.

바닥 HOLD는 중복이므로 첫 행에서 명확히 표시되면 삭제 가능하다. 유지한다면 `(0.55,6.40,8.90,0.35)`, 14pt `The historical eight-origin result remains on hold.` 한 줄만 둔다. 현재 `only the procedure and the verdict are reported`는 함께 제거한다.

목표 화면 어수: 113에서 약70–80. 표 행 이름과 조건의 명료성이 단순 글자 축소보다 우선이다.

### p15 데이터셋: 손질, P1 (범위 문구는 P0)

세 그래프가 모두 데이터여서 장식은 아니다. 다만 세 개를2.9in폭에 넣은 결과 눈금·범례가 매우 작고, 본문은 ML 설명인데 그림에는 ML 검증 결과가 없다. 기존 ‘loading’ 조건과 R²의 의미는 과학 검토안에 맞춰 정정한다.

> Morphology descriptors from 194 beds
>
> Dataset v1.2 contains 130 baseline beds and 64 SE-rich beds.
>
> In the 130-bed set, 106 beds have an SE path. The finite geometric tortuosity spans 1.3–4.2.

R² 비교와 five design knobs는 notes로 이동한다. 원그림의 축 의미와 모델 디스크립터라는 지위는 유지한다. shortest-path임을 캡션으로 명시한다.

- 권장: 중앙 G5b를 notes로 옮기고, G5a `(0.55,2.95,4.30,3.00)`, G3 `(5.05,2.95,4.30,3.00)`로 확대한다. 원그림은 그대로 사용한다.
- 캡션 y=6.10,h=0.48,12pt: `< geometric shortest-path tortuosity >`, `< porosity and SE fraction >`.
- 3개 패널을 반드시 유지해야 하면 15pt 본문을2줄로 축약하고 그림을y=2.70부터 높여 키우되, 범례의 작은 글자까지 뒷줄에서 읽히는 장이라고 판정하지 않는다. 세 그래프 평균적인 크기보다 좌측 geometric 정의와 우측130-point 범위의 읽힘이 우선이다.

### p16 계획: 다시, P0 + P1

현재 ‘closing the three problems’라는 제목에 비해 왼쪽은 절대 전도도와 물성 입력, 오른쪽은 역학과 혼합이고 **Problem 1 격자 의존성에 해당하는 명시적 계획이 없다**. 실제 등록 계획이 확인되지 않은 격자 후속 런을 새로 약속하지 않는다. 제목을 `Tests for unresolved model limits`로 바꾸면 여섯 계획이 세 문제와 일대일 대응한다는 암시를 없앤다.

`nothing below has a result yet`는 이전 SEM-02에 따라 삭제한다. 대체 상단 문구는 `Grid sensitivity remains unresolved. Diagnostic results exist, while confirmatory verdicts remain pending.`로 한다. 상단 본문 상자를 `(0.61,1.08,8.84,1.10)`으로 늘리고 15pt의 두 줄까지 허용한다. 이는 격자 문제의 미해결 상태를 명시할 뿐 새 캠페인이나 후속 런을 약속하지 않는다.

두 칸 좌표는 유지해도 된다: 제목 `(0.55,2.20,4.25,0.36)`, `(5.05,2.20,4.40,0.36)` 15pt. 본문 `(0.55,2.66,4.25,2.75)`, `(5.05,2.66,4.40,2.75)`를15pt로 하고 다음처럼 줄인다.

왼쪽 `Electronic transport`:

> Interface resistance: film model implemented, production on hold
>
> Carbon conductivity: comparison with DC polarization
>
> NCM conductivity: literature-based input review

오른쪽 `Compaction and mixing`:

> AM load sharing: final hypothesis verdict pending
>
> Unloading: springback and measured thickness
>
> Mixing: an adhesion parameter for SE–SE contacts

`default off`, `re-run registered`, `registered contract`, `registration revised twice`, `before confirmatory runs`는 notes로 옮긴다. 이들은 반복해서 화면에 남길 만큼 새 과학 정보를 주지 않는다. 원래 계획의 실행 지위는 notes에서 보존한다.

바닥 `(0.55,5.75,8.90,0.58)`,14pt: `Pending: separate launch approvals for the updated 194-bed run and the 20-bed extension.` 이미 완료된7차 소프트웨어 재검증과 194개 본 런·20개 확장 런의 별도 발사 승인을 구분한다. 이 문구는 소프트웨어 검토가 아직 미완료라는 뜻도, 두 런이 이미 승인됐다는 뜻도 아니다. 세대 검토의 정확한 범위는 이전 SEM-06에 따른다. 목표어수109에서약65–75.

### p17 요약: 다시, P0

현재 상자3.0in 높이에15pt 긴4개 bullet을 넣어 실제 텍스트가 상자높이보다 아래까지 그려진다. 페이지 밖 클리핑은 없지만 생성기의 높이가 실제 점유와 다르다. 가장 강한 빨강 문장이 과학 결과가 아닌 모든 생산값에 대한 검증 보증이다. 삭제한다.

제목 `Current findings and limitations`, 본문 `(0.61,1.08,8.84,3.75)`,15pt.

> DEM and contact networks: composition trends from one bed per composition
>
> MPM: plastic deformation, with compaction agreement dependent on initialization and loading protocol
>
> Voxel transport: results with ideal interfaces, with grid dependence and unresolved absolute conductivity
>
> Confirmatory model tests remain in progress

‘contact-free upper branch’와‘stress-stop thickness’ 대신 앞 장에서 정의한 구체 조건을 말한다. 포괄적인 ‘Every production number…’는 notes로 옮겨서 살아 있게 하지 말고 삭제/사실에 맞게 제한한다. 파랑은 DEM/MPM/Voxel transport 핵심 이름만 남긴다. 네 번째를 경고색 빨강으로 강조할 필요는 없다.

### p18 참고문헌: 그대로 또는 손질, P1

14편이라는 숫자 때문에 지저분한 장은 아니다. 현재11pt의 빽빽한 두 열을 청중이 현장에서 모두 읽기는 어렵다. 현재 상자 `(0.50,1.00,4.45,5.85)`, `(5.05,1.00,4.45,5.85)`에는 아래 여백이 넓다. 같은 서지를 보존한 채 **12pt**로 올리고 항목 사이3–4pt 간격을 주는 안이 합리적이다. 14개 서지를 기억으로 보충하지 않는다. 본문 해당 주장에 작은[n]을 붙여 목록을 회수할 수 있게 하는 것이 참고문헌 장 자체를 늘리는 것보다 유용하다. 필수 원전 누락/카드 처리의 과학 판단은 부모 검토안에 따른다.

### p19 끝: 그대로

Thank you와 연락처는 읽힌다. 사진과 제목 배치는 기존 틀 그대로 유지한다. 이메일도 정상으로 보이며 새 연락처나 날짜를 넣을 근거가 없다.

## 후반부 스토리와 용어

현재도 첨가제→문제1/2/3→진행→계획의 순서는 읽힌다. 끊기는 지점은 ‘문제들이 있는데 그래서 무엇을 완료했나’에 답해야 할p14가 등록 절차와 과거 HOLD 결과를 한꺼번에 성공처럼 소개하는 데 있다. p14를 상태표, p15를 실제 디스크립터 범위, p16을 미결 가설의 시험 계획으로 읽히게 하면 순서를 바꾸지 않아도 된다. p16의 격자 후속계획 부재는 제목의 약속을 줄이는 방식으로 처리한다.

권장 ■ 제목 연결:

`Additive geometry used in transport rasterization` → `Problem 1: Grid dependence` → `Problem 2: Absolute electronic conductivity` → `Problem 3: Load sharing during compaction` → `Registered studies and current status` → `Morphology descriptors from 194 beds` → `Tests for unresolved model limits` → `Current findings and limitations`.

분야 문구는 다음처럼 다듬는다. 기존 사실 범위를 넘는 동의어를 쓰지 않는다.

| 현재 | 권장 |
|---|---|
| heterogeneous-technology pipeline | coupled DEM–MPM–transport workflow |
| voxel electronic gain | voxel conductivity ratio (with / without conductive polymer) |
| origin-replicated | tests across voxel-grid origin offsets |
| contact-free branch / upper branch | ideal-interface voxel model |
| stress-stop thickness | thickness at the prescribed axial-stress stopping criterion |
| transport tortuosity | transport tortuosity factor, 정의식 병기 |
| contact constriction | contact constriction resistance |
| DC polarization | DC-polarization electronic-conductivity measurement |

origin 변경은 같은 침대의 격자 원점 민감도다. 독립 제조·시드 반복처럼 들리는 replicated보다 offsets가 낫다. geometric shortest-path tortuosity와 transport tortuosity factor는 서로 대체하지 않는다.

## 부모 판정문에 넣을 장별 한 줄

| 장 | 그대로 / 손질 / 다시 | 걸리는 것 | 고칠 것 |
|---|---|---|---|
| 10 | 손질 | 최초 첨가 시점을 잘못 제한한 제목, 합성 그림 지위가 작은 내부 제목에만 있음 | 수송 격자 표현 제목18pt, 바깥12pt 캡션으로 illustration/synthetic 구분, 본문15pt 축약 |
| 11 | 다시 | 공개3점에 다른 계열 결론, 긴 회고문 | grid dependence/ionic ratio crosses1로 정정, F2확대 |
| 12 | 다시 | F4의3개 범주라벨 결손, 두 모형 조건 혼합 |5개 라벨 복구, 조건 각주12pt, 그림 확대 |
| 13 | 다시 | Large–large와 AM–AM 불일치, 작은 색상 막대 | NCM–NCM·fixed-platen relaxation, wallSE 제외 캡션 |
| 14 | 다시 | 탭 줄넘침, HOLD와 성과·다른 세대 혼합 | 탭 한 줄, 5행 상태표, HOLD 추론 제거, 배포/소프트웨어 검토 구분 |
| 15 | 손질 |3개 작은 그래프, geometric/ML/범위가 한 문장 | G5b notes이관,2개 확대,130/64 및 geometric 범위 명시 |
| 16 | 다시 | ‘모두 결과없음’ 오류,3문제 대응 약속 불일치 | 제목 완화, 미결 판정 상태 정정, 절차문 notes이관 |
| 17 | 다시 | 포괄 보증·상한·두께 주장, 실제텍스트높이 초과 | 검증 상태에 맞춘4개 짧은 요약, 상자높이3.75in |
| 18 | 손질 |11pt 서지의 투영 가독성 | 서지그대로12pt, 본문[n]연결 |
| 19 | 그대로 | 없음 | 기존마무리유지 |
