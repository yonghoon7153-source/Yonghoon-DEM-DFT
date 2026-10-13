# 연구세미나 초안 4 — v3 묶음 재확인 및 내용·미감 판정

작성 2026-10-13. 대상: `seminar_20261013_codex_review_v3.zip`, 비교용 v2 ZIP, 별첨 `codex_seminar_deck_review_request_20261013.md`. **현 파일 그대로 최종 발표판으로 확정하는 것은 NO-GO.** 이유는 빈 그림이나 미정 날짜가 아니라, 이전의 과학적 지적 여섯 건이 실제 발표물에 그대로 남아 있기 때문이다. 문장·출처·표시를 고치면 되며, 이 발표자료 수정 때문에 새 시뮬레이션이나 전면 재계산을 요구하지 않는다.

## 0. 먼저 파일부터 구분

**v3는 수정된 PPT/PDF가 아니다.** 처음 첨부했던 PPT/PDF, v2 ZIP 안의 PPT/PDF, v3 ZIP 안의 PPT/PDF가 각각 바이트 단위로 동일하다. 글뿐 아니라 위치·글꼴 설정·노트·삽입 그림을 포함한 파일 전체의 동일성이다.

| 항목 | 확인 결과 |
|---|---|
| PPTX 세 판 | SHA-256 `c7849af7809a04ce19c4e301da9002d80d737bd6e2364c92f9c2667644ef3d7f` |
| PDF 세 판 | SHA-256 `f795f0228abb6c40ba4253246f7670bf4686cdc62e810ecd2d19fc8f71d4e97f` |
| v2 ZIP | `83ed120dd3f34f304f9a189a3fcc36d5738afba763c97b56364e8fd5d2e5465f` |
| v3 ZIP | `59d8f5cb9bb6662bd8743c50e0832e219c73672d33ae1571f67d5382d796e52b` |
| v2→v3 내부 파일 | 각 40개. 변경은 `docs/seminar_20261013/outline_v1.md` 하나 |
| 개요의 변경 | 인용 금지값의 예시를 직접 적던 문장을 제거하고 공개 격자 세 점 범위를 명시. 발표물의 주장 수정은 아님 |
| 발표물 | 19장·19쪽, 10×7.5 in. 실제 본문·notes·삽입 그림·렌더 대조 |

그러므로 이전 SEM-01~06을 새로 발견한 여섯 건으로 중복 등재하지 않는다. 상태는 **전부 열림**이다. 이번 추가분은 요청 Q-SEM-3~11의 미감·밀도·투영 가독성·구체 편집안이다.

### 판정 등급과 한계

- 이 문서는 새 요청서의 등급을 따른다: **P0 = 발표 전에 반드시 수정**, P1 = 되도록 개선, P2 = 후속 그림 보강·구성 변경. 이전 과학 리뷰의 `P1 SEM-01~06`은 이번 편집 우선순위에서 P0에 해당한다. 심각도가 새로 상승했다는 뜻은 아니다.
- 원본 PPT/PDF·리포·생산 코드·원장을 수정하지 않았다. DEM/MPM/FV/접촉망 솔버를 실행하지 않았다. 저장된 수치 자료의 산술만 다시 했다.
- 기존 근거 사본의 코드 핀은 `a0439bdf8156236f454bd3f8b5bf4d044e127039`, 문헌 카드 핀은 `6e568c4f0bb7df299959fd0e77e349838ad8ac98`. 첨부물의 대조 근거이지, 이를 ‘요청서를 담은 커밋’이라고 확인한 것은 아니다. 이번에 최신 브랜치로 판정 범위를 바꾸지 않았다.
- 원래 10-13 템플릿은 동봉되지 않았다. **원 템플릿과의 완전 일치는 판정 불가**다. 현재 PPTX 구조와 동봉 렌더, 요청서가 적은 문법을 평가했다.
- PowerPoint 네이티브 렌더 및 실제 발표장의 투영 시험은 하지 않았다. 글자 크기 권고는 이 4:3 덱에서의 편집 기준이지, 뒷줄 가독성을 실험 인증한 수치가 아니다.
- 그림 생성기의 selftest는 실행하지 않았다. 현재 런타임에 matplotlib가 없다. 대신 입력 상수·CSV·원자료의 반올림·산술과 실제 출력 그림을 독립 대조했다. 숫자 selftest가 초록이어도 범주 라벨 누락은 막지 못한다.

## 1. Q-SEM-1 — 과장·정의·상태: 기존 여섯 건은 닫히지 않음

| 기존 ID / 장 | 상태와 결정적인 근거 | 발표판의 최소 수정 |
|---|---|---|
| SEM-01 / 2·17 | **열림.** `each calibrated to its own experiment`, `cross-validation`이 그대로다. 실제 복셀 입력에는 미보정 상 전도도와 다른 적합식에서 이식한 값이 있다. 공유 입력을 가진 모델 간 일치를 독립 실험 검증으로 부를 수 없음 | 단계별 보정 **표적**과 검증 완료를 구분. F1의 `anchored to conductivity measurements`도 함께 고침 |
| SEM-02 / 8·16·17 | **열림.** 30.7 µm는 옛 cell-filled SE·양방향 servo 결과인데, 본문은 DEM에서 SE 씨앗까지 가져온 계산처럼 연결한다. 현재 등록 f=0 결과는 25.842 µm, f(a)는 실행 실패, 전체 판정 미완료. `nothing below has a result yet`도 틀림 | 역사적 초기화·현재 등록 결과를 분리. AM 하중분담은 후보 설명. 그림 없이도 잘못된 30.7 비교를 삭제하고 방법 한계로 설명 가능 |
| SEM-03 / 11 | **열림.** 공개 세 점은 `R(h)=A+C h^p`에 p=3.1312380389347334로 맞는다. 증분비 3.360103626943009, 표시 정밀도에서 잔차 0. 따라서 `increments follow no power law`는 반례가 있음 | `Grid convergence has not been established.`로 교체. 이 적합 가능성이 외삽 정당화를 뜻하지는 않음. 이온 비는 부호가 아니라 **1을 통과** |
| SEM-04 / 13 | **열림.** 0:10에 큰 입자가 없는데 59.5622427545%가 나온다. 이 값은 큰–큰이 아닌 **AM–AM 전체**의 21단면 하중 가중 몫 | `Large–large`→`NCM–NCM`. 가압 최고점 또는 무하중 제하가 아니라 고정판 이완 상태 명시 |
| SEM-05 / 14 | **열림.** 현재 원장의 h1 추론이 HOLD인데 `gain follows the represented additive volume`을 살아 있는 성과로 제시 | 숫자만 숨기지 말고 **추론도 보류**라고 표시. h1의 물리적 반증이라는 새 판정은 아님 |
| SEM-06 / 14·16·17 | **열림.** 이미 배포된 v1.2와 세대 2 소프트웨어 재검증 7회를 한 이력으로 합친다. 7차 판정은 새 194 발사·완주·v1.3 승인도, 보충 20 승인도 아님 | 배포와 소프트웨어 심사를 별도 행으로. `Every production number...` 전칭 보증 삭제 |

직접 재계산한 13장 AM–AM 몫은 조성 0:10→10:0 순으로 **59.562243 · 54.634924 · 52.371659 · 48.463893 · 56.914398%**다. 값은 맞고 이름이 틀렸다. 같은 자료의 단면 평균 축응력은 **158.25 · 159.93 · 164.44 · 167.14 · 175.48 MPa**다. 최고 가압 300 MPa를 읽는 패널로 바꾸면 안 된다.

### 수정 문구 — 결과를 더 강하게 만들지 않는 짧은 안

**2장**

> A coupled DEM–MPM–transport workflow
>
> Each stage has specific calibration targets and unresolved validation tasks.
>
> Agreement between models sharing inputs is a consistency check, not independent validation.

**8장** — 이번 수정에서는 새로운 결과 숫자를 슬라이드에 추가하지 않는 최소안. 옛 30.7을 넣은 비교 그림 지시도 같이 제거한다.

> Compaction agreement depends on initialization and loading protocol
>
> Historical and current scaffold calculations use different electrolyte initialization and loading protocols.
>
> AM load sharing remains a candidate explanation for over-compaction; the final hypothesis verdict is pending.

30.7을 꼭 남긴다면 `Earlier cell-filled SE calculation with bidirectional servo`라고 같은 화면에서 한정한다. **30.7을 별도 29.95의 정지 결함 때문에 무효라고 말하지 않는다.** 다만 현재 DEM-seeded 결과의 검증값으로 사용할 수 없다. 과거 ε_sphere 1.125%와 현재 MPM porosity 2.585%도 서로 다른 정의이므로 숫자만 바꿔 끼우지 않는다.

**11장**

> Problem 1: Grid dependence
>
> The electronic ratio decreases across the three tested voxel spacings. The ionic ratio crosses 1.
>
> Grid convergence has not been established.

우측은 `No converged conductivity ratio is reported.` 하나면 충분하다. `headline ... is a grid artefact`, `shape ... is real`는 삭제한다. 다른 HOLD 계열의 결론을 notes로 옮겨 살아 있게 하지 않는다. 외삽값·미세 격자값을 새로 추가하지 않는다.

**13장**

> Problem 3: Load sharing during compaction
>
> NCM–NCM contacts contribute 48–60% of vertical stress after relaxation at fixed platen position.
>
> The porosity ranking agrees for the selected five compositions (exploratory comparison).

실험 순위의 `n=5`, 선정된 부분집합, 탐색 비교라는 한정은 유지한다. 순위가 같다는 사실만으로 되튐 기전이나 강성을 역추정하지 않는다.

### 그 밖의 필수 정의 정정

| 장 | 남은 문제 | 권고 |
|---|---|---|
| 3 | `reproduces`가 실험 재현 완료처럼 들림 | `Composition-dependent porosity in five simulated beds`. ‘7:3이 이 다섯 침대 중 최소’는 유지. 조성당 한 침대·시드 반복 없음 유지 |
| 4 | `Hertz constriction`, 길이 효과와의 이분법, notes의 시드 산포 일반화 | `Holm/Maxwell constriction using Hertz contact radii`. 화면에 `T = φ_SE σ₀ / σ_eff`와 **모형 내부 I²R 몫** 표시. 해당 다섯 침대에는 반복이 없으므로 직접 측정한 시드 오차처럼 설명하지 않음 |
| 7 | E≈24 GPa를 LPSCl 단결정 값으로 표기. σy를 문헌에서 독립 고정했다고 표현. `irreducible`의 보편 주장 | 참고값은 Sakuda의 **75Li₂S–25P₂S₅ 유리계**와 구분. σy=0.30 GPa는 보정 스윕의 선택값. `The tested alternatives did not remove the need for effective parameters.` 정도로 한정 |
| 7 | `the earlier citation was retracted` | 논문이 철회된 것처럼 쓰지 말고 `Our earlier attribution to the literature was withdrawn.` |
| 9·17 | 이상 계면 복셀 모델 = 망 CF = 실험 대비 상한으로 혼동 | `ideal-interface voxel model`. 추가 계면저항을 0으로 둔 **같은 기하·물성·경계**의 모형 내 상한이지 일반적인 물리 상한이 아님. 기하학적 목 부분의 저항은 복셀 안에도 생김 |
| 9 | 전기식 한 식으로 열까지 표현 | 본문에서는 `Finite-volume conservation on the phase grid gives electrical and thermal transport.` 식을 남기면 전기 `(σ, φ)`, 열 `(κ, T)`를 구분 |
| 10 | 합성 미리보기와 실제 Phase A 스탬프 혼동 | 왼쪽 `additive seeding illustration`, 가운데 `synthetic morphology example`. 제목 `Additive geometry used in transport rasterization` |
| 12 | 비교의 핵심 조건은 notes에만 있음 | 왼쪽 측정 조건 미확인, 오른쪽 Hertz H0·공통 기준 4.1·경험 크기 인자 OFF·탄소/바인더 없음·조성당 한 침대를 화면에 |
| 15 | loading이 자유 설계축처럼 기재, 두 OOF R²를 직접 비교 | loading 삭제. 130+64 코호트, 조건부 모델 디스크립터라는 지위 명시. CV·입력 규약이 확인되지 않은 협력자 수치와의 승패 비교는 notes로도 하지 않음 |

4장의 73–75%는 저장된 FULL 해의 `ΣI²R_constr / ΣI²R_total` 판독값과 맞는다. **접촉 목이 실물 전극의 저항 75%를 독립적으로 설명한다는 증거는 아니다.** 짧은 문구는 `Contact constriction accounts for 73–75% of Joule dissipation in this network model.`가 적절하다.

7장의 K=25.5 GPa 산술 자체는 맞다. 잘못된 것은 재료 출처와 파라미터 식별 지위다. 순수 SE 공극률 10%를 미출판 보정 표적이라고 밝힌 것은 유지한다.

12장의 두 비 54/4.47=12.0805369, 70.6/12.4=5.6935484는 맞다. 오른쪽 다섯 값도 원자료를 반올림하면 0.391·0.406·0.402·0.375·0.467 mS/cm다. 원 최소값은 0.3746972909여서 화면의 범위 `0.38–0.47`는 이중 반올림을 거친 표현이다. **기존 수치를 바꾸는 것이 아니라 표기 정밀도를 맞춰 `0.375–0.467 mS cm⁻¹`**로 적거나 본문 범위 중복을 뺀다.

## 2. Q-SEM-2 — 금지값·HOLD·내부 용어

실제 PPTX 본문 19개+notes 19개, 동봉 새 그림 CSV 3개+SVG 4개를 합친 **45개 텍스트 단위**에서 `quotation_ban`의 42개 리터럴 패턴 일치는 **0건**이다. 동봉 래스터 그림도 시각적으로 확인했으며 금지된 미세 격자 전도도·옛 8팔 이득의 직접 숫자를 발견하지 않았다. 완전 OCR·의미 무결성 인증이라고 주장하지 않는다.

중요한 실패는 숫자보다 **추론의 재사용**이다. 11장의 계열이 다른 멱법칙 진단, 14장의 HOLD h1 결론이 그대로 남는다. 문자열 검사로 잡을 수 없는 문제다. 반대로 **Phase A의 격자 간격 설정 0.15 µm 자체**나 별도 공개 p2 비교까지 금지하는 것은 잘못이다.

자리 표시에는 `ps45`, `uma`, `WSL`, `real_14`, `STEP3`, 스크립트 경로가 있다. 이번 초안에서 요청한 제작 지시이므로 내부 정보 누출 결함으로 세지 않는다. **최종 청중용 화면에서는 notes로 옮긴다.** v3에서 개요의 금지값 예시를 지운 것은 문서 위생 개선이지만 발표물 내용의 해제 증거는 아니다.

## 3. Q-SEM-3·Q-SEM-4 — 첫인상과 템플릿 문법

**첫인상: 실제 연구 그림이 있는 연구실 진행 보고이지만, 긴 방어 문장과 작은 그림 때문에 ‘듣는 발표’보다 ‘읽는 심사 문서’처럼 보인다.** 외관만으로 사람이 썼는지 AI가 썼는지는 판정할 수 없다. 수정 가능한 문제는 저작 주체가 아니라 밀도·반복·정보 위계다.

같은 틀 12장, 꺾쇠 캡션, 대칭 두 칸, 점선 프레임 자체는 이 연구실의 지정 문법이다. 이것들을 ‘AI 티’라는 이유로 없애지 않는다. 개선할 곳은 다음이다.

| 요소 | 해당 장 | 유지/변경 |
|---|---|---|
| 긴 판정형 제목과 `X, not Y`·em-dash 반복 | 8·11·14·17 | 짧은 연구 질문/결과 제목으로. ‘what survives’, 과거 원고의 철회 경위는 notes로 |
| 등록·봉인·재검증을 성과처럼 반복 | 14·16·17 | 14는 연구별 현재 상태표, 16은 과학 질문, 17은 결과의 적용 범위로 역할 분리 |
| 제목·본문 길이와 상관없는 같은 그림 높이 | 10–15 | 글 축약 후 그림을 위로 올려 확대. 같은 틀은 유지 |
| 점선 빈 패널 안 장문의 제작 명령 | 4·6·8·9 | 편집본에는 유용. 발표판에서는 실제 그림 또는 방법 설명 한 줄로 |
| 과한 색 강조 | 17 | 모형 이름만 파랑. 근거가 없는 전칭 보증을 빨강으로 강조하지 않음 |

### 글자 크기: 요청서와 실제 파일의 차이

요청서는 ■ 제목을 15pt라고 적지만, 실제 대표 본문 장의 해당 제목에는 직접 크기 설정이 없고 **master의 `otherStyle`/기본 텍스트 스타일 18pt를 상속**한다. 별도 지정된 본문 bullet은 13pt다. 따라서 ‘현재 제목 15pt 그대로’라는 처방을 기계적으로 적용하면 오히려 제목을 줄일 수 있다. 상세 XML 경로는 `notes/visual_1_9.md`에 보존했다.

권고 기준:

- 절 표지 **24pt 유지**, ■ 주제 제목은 **현재 유효 18pt 유지**.
- 본문은 **문장을 먼저 줄이고 15pt**로 복귀. 글을 더 넣기 위해 13pt로 되돌리지 않음.
- 줄 간격도 같이 조정한다. 현재 그림 본문은 대체로150%, 두 칸은110%다. 그림 본문15pt에서120–130%·문단 뒤4–6pt, 두 칸110–115%·문단 앞4pt를 시작값으로 삼고 재렌더한다. 폰트만 키우고150%를 유지하면 다시 과밀해질 수 있다.
- 해석에 필수인 한정어·범례·캡션은 **최종 슬라이드에서 12pt 이상**을 편집 목표로. 일반 출처만 10–11pt 허용. 작은 출처를 읽어야 주장 오류를 피할 수 있게 만들지 않음.
- 캡션 꺾쇠는 유지 가능. 파랑은 핵심 개념, 빨강은 실제 미결/제한에만 사용.
- 학교·연구실 로고, 바닥글, 쪽 번호, 원래 글꼴, **미정 날짜 표지는 그대로**. 이전 첫 판정의 ‘날짜 입력’ 권고는 새 요청에 따라 철회한다.

**출처 줄도 설명과 실물이 다르다.** 요청서는 우상단10pt 출처 줄을 문법으로 적었지만, p01–p09 실제 화면에는 그 source tag가 없다. 생성기 `build_seminar.py:239–241`은 그림 본문 원형의 `TextBox 69`를 지우며, 정의된 `tag()`의 호출이 없다. 이는 ‘원 템플릿과 출처 배치도 동일’이라는 확인을 막는다. 관련 문장/캡션에 검증된 `[n]`을 붙이고 긴 파일 경로는 notes로 두면 된다. 작은 출처 상자를 기계적으로 복원하는 것보다 인용 대응이 먼저다.

## 4. Q-SEM-5 — 어디의 글을 지우거나 notes로 옮길까

화면 본문 목표 50–80단어는 이 덱을 위한 편집 목표다. 보편적인 발표 합격선은 아니다. **4·6·9장의 큰 단어 수는 제작 지시가 섞인 수**라서 7·14·16장과 같은 밀도 결함으로 세지 않는다.

| 장 | 화면에 남길 것 | 삭제 또는 notes 이관 | 편집 목표 |
|---|---|---|---|
| 4 | 망의 저항 구성, σ₀, T 정의, I²R 모형 몫 | 전류 추출 경로·명령·카메라. `not in path length` 이분법과 직접 시드 산포 문구는 삭제 | 제작 지시 제외 약55–70단어 |
| 5 | 우리 접촉 모델의 변형 한계, 유효 E, 한 침대의 58% 감쇠 몫 | 22편 분류의 항목별 세부 설명은 notes. 화면에는 `Selected literature survey (22 studies; author classification)` | 약65–80단어 |
| 6 | fixed AM·plastic SE, 2D/3D 차이 | 장문 파일명·기계명·불능 CLI. 대표 조건은 각 그림 캡션으로 | 약40–60단어 |
| 7 | DEM/MPM 유효 입력, 미출판 보정 표적, 독립 검증 미완료 | 긴 문헌 철회 경위·보정 스윕 과정·cap 교차검사 세부는 notes. 잘못된 재료명·irreducible은 이동이 아니라 정정 | 151→약70–90단어 |
| 8 | 초기화/하중 경로가 다른 결과, 후보 가설 | `Pressed honestly`는 가치판단어라 삭제. 잘못 연결한 30.7 그림 지시 삭제 | 약45–65단어 |
| 9 | 유한체적 보존, 이상 계면 규약 | 전류장 추출 지시·스크립트 경로를 notes. `contact-free branch` 등가 주장 삭제 | 약45–60단어 |
| 11 | 세 공개 격자의 의존성, 수렴 미입증 | `What survives` 3항, 옛 원고 회고, GPU 메모리 수치→notes. 잘못된 계열 결론은 삭제 | 약35–55단어 |
| 14 | 다섯 연구 항목과 현재 상태, R/Q 정의 | 팔 수·QC 0.00000%·반복 등록 설명은 notes. HOLD h1·세대 혼합·전칭 보증은 삭제/정정 | 113→약70–90단어 |
| 15 | 130/64, 106/130, 기하 굴곡도, 조건부 디스크립터 | 협력자 R² 대결 문장→조건을 설명한 notes. loading은 삭제 | 약50–65단어 |
| 16 | 미해결 질문별 후속 시험 | `registered contract`, `registration revised twice` 등 반복 절차어→notes. ‘전부 결과 없음’ 삭제 | 109→약65–75단어 |
| 17 | 모형 세 개의 현재 적용 범위 | `Every production number...`는 이동이 아니라 삭제 또는 사실에 맞게 제한 | 약50–70단어 |

## 5. Q-SEM-6·Q-SEM-7 — 그림 가독성과 당위성

### 새 그림의 문제는 PPT 본문 크기와 별개

F2/F3/F4 원 그림은 11×8.2 cm에 기본 9pt·범례 8pt다. 현재 약 4.1×2.6 in 안에 비율 유지 삽입하면, 높이 기준 약 0.805배로 축소돼 **최종 기본 글씨 약7.3pt·범례6.4pt**다. 13pt 본문을 15pt로 키우기만 해서는 해결되지 않는다. Origin 또는 현재 생성기에서 **최종 배치 크기를 기준으로 축·눈금·범례 12pt**를 목표로 한다. 값은 그대로 둔다.

재사용 그림은 다시 그리지 않는다. 바깥 여백만 자르고 축·범례·색상 막대를 보존해 확대하거나, 보조 패널을 notes로 옮긴다. 존재하지 않는 시드 오차막대를 만들지 않는다.

| 장/그림 | 주장 지원 여부·오독 위험 | 허용 범위 안의 수정 |
|---|---|---|
| 2 F1 | 과정 소개에는 필요. 독립 보정 완료 표지는 부정확. 박스 안 긴 문구 넘침 | `DEM packing / Plastic compaction / Voxel transport / Electrode response`로 줄임. 보정·검증 상태를 별도 짧은 문구로. 마지막 응답 단계가 완료된 결과처럼 읽히지 않게 scope 설명 |
| 3 4단계·G1 | 한 침대 과정과 다섯 조성의 차이를 받침 | 3D 아래 세부 라벨은 notes로 보조. 0·47·296·165 MPa의 마지막이 무하중이 아니라는 상태 한정 유지. G1에는 한 침대/조성 표시 |
| 4 두 막대 | 같은 Hertz/H0의 값은 맞음. y축이 잘려 막대 길이가 차이를 과장할 위험 | 재사용 원그림은 보존. 캡션에 `Truncated y-axes; compare numerical values`와 T 정의. 본문에서 배수 차이를 막대 길이로 설명하지 않음. 다음 판 재그리기는 P2 |
| 5 이력 그림 | 모델 구성 설명에 적합, 실험 force trace 아님 | `Contact-law illustration from the implementation` 외부 캡션. 주기 가지 설명 하나를 말로 짚고 그림의 모든 작은 기호를 읽히게 하려 하지 않음 |
| 10 seed·preview·G6 | 앞 둘은 모식/합성, G6만 캠페인 수치. 가운데에 SuperP 등 실제 Phase A와 다른 표지가 있음 | illustration/synthetic 라벨 12pt. 그 합성 그림으로 실제 VGCF/PTFE 스탬프 충실도를 입증하지 않음. G6를 상대적으로 크게 |
| 11 F2 | 공개 세 점의 격자 의존성은 직접 지지. no-power-law는 지지하지 않음 | 비=1 기준선·3개 x좌표 유지. `ratio`를 `gain`으로 바꾸지 않음. F2 확대, 설명 축약 |
| 12 F3 | 비교값은 맞지만 실험 조건 미확인 | `Measurement conditions not yet matched`를 화면에. 로그 축 유지 가능. 새 그림이므로 점 도표도 선택 가능하나 재계산·문헌값 추가는 하지 않음 |
| 12 F4 | 다섯 값은 원자료와 일치. **라벨은 0:10·7:3만 보임** | `0:10 / 3:7 / 5:5 / 7:3 / 10:0` 모두 고정. `set_xticks/set_xticklabels` 뒤 `_fmt`가 locator를 덮는 순서가 원인. 값 교정 없이 범주 표시만 복구 |
| 13 하중·응력 | AM–AM 몫은 지지. 우측 응력은 보조 맥락, 인과 검증 아님 | `NCM–NCM`, fixed-platen relaxation 정정. `SE von Mises stress, 0–150 MPa; wall SE excluded`를 그림 밖 12pt로 |
| 15 G5a/G5b/G3 | 모두 실제 자료이나 작고, ML R²를 직접 보여주는 그림은 아님 | 중앙 G5b는 notes로 옮기고 G5a/G3 확대 권고. G5a의 빨간 ×는 τ≈0.9의 관측값이 아닌 **관통 경로 부재 표지**라고 캡션 명시 |

Phase A는 저장된 96 primary+8 QC JSON에서 72개 인접 조성 비교를 다시 계산해 등록 문턱 위반 0, 지정 QC 최대 replay 차이 0을 확인했다. **72개 독립 물리 실험이나 격자 수렴 증명은 아니다.** 현재 한정된 순서 주장은 유지할 수 있다.

LHS는 130 중 106, 확장64 중64가 유한 기하 τ를 갖는다. 1.2918749–4.1505645는 130 집합의 유한값 범위다. 194 전체 또는 비관통 사례에 이 범위를 씌우지 않는다. 기록상 physical-target HOLD는 59/130+62/64이며, 배포를 물리적으로 검증된 타깃으로 소개하지 않는다. 통합 R²≈0.98와 별도 검증 규약 미확인 0.99의 직접 비교는 이 두 구조 그림으로 정당화되지 않는다.

이번 수정에 문헌 그림 추가를 권하지 않는다. 필요한 그림은 이미 있고, 새 litdb 크롭의 더 나은 적합성을 이번에 전수 검색한 것은 아니다. 장식용 문헌 그림을 넣기보다 기존 데이터의 정의·범주·가독성을 먼저 고치는 편이 적절하다.

## 6. Q-SEM-8 — 여섯 자리 표시: 제작 지시와 발표 내용은 분리

| 위치 | 제작 지시의 충분성 | 채우기 전 확인 | 발표 전 못 채우면 |
|---|---|---|---|
| 4 전류 경로 | **부분**. 침대·모드는 있으나 `top 50% current` 해석이 빠짐 | 같은 7:3 H0/FULL 이온 해, origin/세대, 1V, 색의 `j=|I|/A` 정의. share50은 단순 간선 개수 상위절반이 아님 | 두 기존 그래프로 설명 가능. 명령·빈 타일은 빼고 T 정의 또는 모형 범위 한 줄로 |
| 6 왼쪽 2D | **부분**. 실제 파일은 리포 밖 | 실제 이미지 확보, 2D 조건/시점, 길이 눈금. 3D와 독립 검증 비교처럼 두지 않음 | 그림 대신 `Illustration pending; method description only` 또는 짧은 방법 설명. 모사 이미지를 실결과로 만들지 않음 |
| 6 오른쪽 3D | **미충족**. `viz_mpm_morphology.py <run> --slice xz`는 parser와 불일치 | 실제 `--se` 파일 필수, scaffold·단위·시점 확인. `--dg` 소성변형과 `--eps` total strain 구분 | 잘못된 명령은 notes에서도 수정. 방법만 설명 가능 |
| 8 DEM↔MPM | **미충족**. 셀 채움 결과와 DEM-seeded 설명이 섞임 | 같은 초기화·하중 이력·상태의 실제 자료. 같은 카메라보다 이 조건이 먼저 | 옛 수치 비교 대신 §1의 초기화/하중 경로 제한을 표시. 없는 패널 때문에 새 런을 요구하지 않음 |
| 9 phase grid | **부분**. 규약·실파일 연결 부족 | full sid grid, origin, vox, phase mapping, 전극 규칙, run 해시 | 도식임을 명시한 방법 설명으로. 생산 결과인 것처럼 제시하지 않음 |
| 9 전류밀도 | **부분**. S16/S17 지목만으로 파일·해·단위 확정 못 함 | 같은 해의 1V 정규화 및 A cm⁻² 환산 확인 | phase grid 하나만 있어도 방법 설명 가능. 미확인 색상 막대 대신 글로 |

6장 CLI의 **문법 예시**는 아래와 같다. 이 파일명이 존재한다는 뜻은 아니다.

```text
python3 scripts/viz_mpm_morphology.py --se ACTUAL_SE_POINTS.npy --scaffold ACTUAL_AM_SCAFFOLD.csv --y 0.5 --out morphology.png
```

자리 표시를 유지한 **검토용 초안**은 정직하다. 그러나 제작 명령이 가득한 상자를 그대로 청중에게 보여줄 필요는 없다. 이 처리는 19장·순서 고정 조건을 깨지 않는다. 장을 합치는 것은 후속 P2 선택지일 뿐 요구하지 않는다.

## 7. Q-SEM-9 — 이야기 흐름과 용어

① 방법 → ② DEM 한계 → ③ MPM → ④ 복셀 → ⑤ 첨가제 → ⑥ 세 문제 → ⑦ 진행 → ⑧ 계획의 순서는 성립한다. 끊기는 곳은 **14장의 과거 HOLD/현재 완료/미발사 소프트웨어를 한 성공 목록으로 묶은 부분**이다. 이를 현재 상태표로 바꾸면 순서를 재배치할 이유가 없다.

16장의 `closing the three problems`는 특히 격자 문제에 대응하는 명시적 계획을 보여주지 않는다. 새 격자 캠페인을 즉석 약속하기보다 제목을 `Tests for unresolved model limits`로 바꾸고 `Grid sensitivity remains unresolved.`라고 상태만 밝힌다.

| 현재 용어 | 권장 영어 |
|---|---|
| heterogeneous-technology pipeline | coupled DEM–MPM–transport workflow |
| rigid-sphere DEM | soft-sphere DEM with fixed spherical particle shapes |
| transport tortuosity | transport tortuosity factor, T = φ_SE σ₀ / σ_eff |
| geometric tortuosity | geometric shortest-path tortuosity |
| Hertz constriction | Holm/Maxwell constriction using Hertz contact radii |
| contact-free branch | ideal-interface voxel model |
| stress-stop thickness | thickness at the prescribed axial-stress stopping criterion |
| origin-replicated | tests across voxel-grid origin offsets |
| voxel electronic gain | electronic conductivity ratio, with / without conductive polymer |
| DC polarization | DC-polarization electronic-conductivity measurement |

origin 8개는 같은 침대를 복셀화하는 원점 민감도다. 독립 제조·시드 반복이라는 의미의 replication으로 읽히지 않게 한다. DEM, MPM, SE, AM, VGCF, PTFE 및 SBE/DBE는 첫 등장 또는 그림 범례에서 정의한다. 공간이 부족하면 쓰지 않아도 되는 약어를 먼저 줄인다.

## 8. Q-SEM-10 — 참고문헌 14편의 처리

14라는 개수는 합격선이 아니다. **핵심 입력·계산법과 연결된 인용이 빠져 있고, 나머지 14편 전체의 내용이 화면에 쓰이는 것도 아니다.** 현재 두 열은 유지해도 된다. 각 장의 주장 옆에 짧은 `[n]`을 붙여 관련 원전을 회수할 수 있게 하는 것이 우선이다.

- **7장 E≈24 GPa**: Sakuda et al., 2013, *Scientific Reports* 3, 2261. [DOI](https://doi.org/10.1038/srep02261). 이미 대조한 자료는 유리계 전해질이다. LPSCl 단결정이라고 읽히는 인용은 안 됨.
- **12장 공통 기준4.1 mS/cm**: Wang et al., 2018, *Journal of Power Sources* 393, 75–82. [DOI](https://doi.org/10.1016/j.jpowsour.2018.05.005). 펠릿 기준값을 두 NCM 종류에 공통 채택한 **모형 가정**을 같이 적음.
- **4장 협착, 6장 MPM**: Holm 및 실제 사용 MPM 수치법의 원전 연결 필요. 카드 부재를 기억으로 메우지 않은 것은 옳지만, 그래서 최종판의 필수 출처가 없어도 된다는 뜻은 아님. 원문 카드 확인 뒤 추가하거나 그 전에는 확인된 구현 출처와 ‘사용 모델’ 지위를 명확히 함.
- **J2 알고리즘**: 일반 교과서 이름만 붙여 코드 구현과 일치한다고 주장하지 않음. 실제 응력 갱신/return mapping의 출처를 대응시켜야 함.
- ‘22편 중 0/22’ 등 문헌 통계는 **선정한 문헌과 저자 분류**라고 표시. 전 분야 부재를 입증한 체계적 문헌고찰로 확대하지 않음.

이 두 DOI와 원전 후보의 서지는 앞선 검토에서 확인한 내용을 잇는다. 이번에는 새 문헌 전수조사나 22편 원문 재감사를 하지 않았다. 기존 서지의 LIGGGHTS commit 연도 2024, Shi 2020, So 권508은 이전 확인에서 오류가 아니었다. 이를 임의로 고치지 않는다. 문헌값을 새 그래프에 얹으라는 제안도 아니다.

## 9. Q-SEM-11 — 생성기에 반영할 편집 사양

좌표는 슬라이드 좌상단 기준 `(x, y, w, h)`, 단위 in. 아래는 **제안 배치**이며 원래 값과 구분한다. 그림 좌표는 비율 유지 fit 영역이므로 원본 비율에 따라 실제 점유 폭/높이가 작아질 수 있다. 위치·줄바꿈은 적용 뒤 PowerPoint/PDF 렌더로 확인해야 한다. 주제 제목18pt, 본문15pt, 해석용 캡션12pt를 기본으로 한다. 제안 상자 안에서도 한 줄이 넘치면 폰트를 줄이기보다 문장을 더 줄인다.

### P0 — 내용과 식별을 먼저

| 장 | 대상 | 구체 조치 |
|---|---|---|
| 2 | 본문·F1 | §1 문구로 교체. F1 아래 독립 보정 완료 표지를 정정. 본문 영역 `(0.61,1.08,8.84,1.65)` 안 짧은 제목+두 bullet, F1 `(0.77,3.00,8.46,3.15)`, 캡션 `(1.00,6.28,8.00,0.36)`12pt |
| 7 | 물성·보정 설명, 제목 충돌 | 왼쪽 제목 `Effective material inputs`, 오른쪽 `Calibration target and limits`. 오른쪽 `(5.05,2.20,4.40,0.36)` 15pt, 가로선 아래로 줄이 내려오지 않게. 본문은 각 칸 `(0.55/5.05,2.66,4.25/4.40,2.75)`에15pt. 틀린 물성 출처·보편 연화 문장은 정정 |
| 8 | 혼합된 비교 | §1 최소안으로 교체. 오래된30.7을 현재 그림에 붙이는 제작 지시 삭제. 본문 `(0.61,1.08,8.84,1.75)`, 하단은 검증 상태표 또는 그림 확보 후 조건 명시 |
| 9·17 | CF/상한 등가 문구 | ideal-interface로 정정. 열 변수 구분. 기본에 계면 저항이 없다는 말과 구현에 기능이 전혀 없다는 말을 구분 |
| 11 | 계열·비의 정의·그림 | §1 문구. F2 `(0.65,2.85,5.20,3.15)`, 우측 한 문장 `(6.05,3.05,3.30,1.40)`15pt. 캡션 `(0.65,6.10,5.20,0.45)`12pt |
| 12 | F4 범주와 핵심 조건 | 다섯 라벨 복구. F3 `(0.60,2.95,4.35,3.00)`, F4 `(5.10,2.95,4.35,3.00)`. 캡션 y6.10,h0.50에12pt. 줄 수 부족 시 본문 숫자 중복을 삭제 |
| 13 | 접촉 분류·상태 | NCM–NCM·fixed-platen relaxation. 왼쪽 `(0.50,2.95,4.25,3.00)`, 오른쪽 `(4.95,3.10,4.65,2.80)`. 우측 캡션 `(4.95,6.03,4.65,0.58)`12pt, wall SE excluded 표시 |
| 14 | HOLD·세대·상태 | 아래5행 표로. 탭 `Study status` 한 줄15pt. 점선틀 `(0.55,2.40,8.90,3.25)`. 왼쪽 x0.80,w3.75, 오른쪽 x4.75,w4.55, 행y2.72/3.26/3.80/4.34/4.88,h0.48,14–15pt |
| 15 | 배포와 ML 범위 | loading·동일하지 않은 CV 승패 문장 제거. 130/64 구분, 모델 디스크립터라는 조건을 화면에 |
| 16·17 | 완료·미완료와 전칭 보증 | ‘모두 결과 없음’·‘모든 수치 사전등록 검증’ 삭제. 아래 짧은 문구 적용 |

**12장 화면 문구** — 본문 숫자 반복을 줄이고 캡션이 조건을 맡도록 한다.

> Problem 2: Absolute electronic conductivity
>
> Voxel predictions exceed the available DC-polarization estimates; measurement conditions remain unverified.
>
> The NCM–SE comparison uses a common reference conductivity and a specified contact model.

왼쪽 캡션:

> Model and DC-polarization estimates — log scale; conditions not yet matched

오른쪽 캡션/각주:

> Carbon- and binder-free NCM–SE beds; Hertz H0 contacts
>
> Common NCM reference: 4.1 mS cm⁻¹; empirical size factor off; one bed per composition

12pt 두 줄 이상이 필요하므로 캡션 상자는 `h=0.65`까지 늘려도 된다. 그림의 실제 높이를 조금 줄이는 경우에도 최종 축 폰트12pt를 유지해야 한다. 오른쪽은 접촉 협착이 있는 망이므로 `contact-free`라고 이름 붙이지 않는다.

**14장 상태표**

| 왼쪽 | 오른쪽 |
|---|---|
| Historical eight-origin study | Conductivity estimates and inference remain on hold |
| VGCF ordering study | Ordering holds across tested grids and offsets (72/72) |
| Absolute-conductivity comparison | R = 2.07 (Tier 1); Q = 0.84 |
| 194-bed dataset v1.2 | Released for conditional use as model descriptors |
| Updated transport software | Seven reviews completed; production remains pending |

표의 제목은 `Registered studies and current status`. R/Q 정의는 `(0.80,5.85,8.60,0.58)`12pt:

> R: model / literature conductivity. Q: conductivity retained after PTFE treatment.

Q의 ‘예측 적중’은 등록한 모형 민감도 예측이지 실험 적중이 아니다. 팔 수와 replay 세부는 notes로 옮겨도 된다. 첫 행에 HOLD가 분명하므로 하단 긴 빨강 문장은 삭제 가능하다. 유지한다면 `(0.55,6.40,8.90,0.35)`14pt `The historical eight-origin result remains on hold.` 하나로 줄인다. `only the procedure and the verdict are reported`는 삭제한다.

**16장**

제목 `Tests for unresolved model limits`. 위 설명:

> Grid sensitivity remains unresolved. Diagnostic results exist, while final hypothesis verdicts remain pending.

양쪽 본문은 기존 두 칸 위치에서15pt, 세 항목씩:

| Electronic transport | Compaction and mixing |
|---|---|
| Interface resistance: film model implemented, production on hold | AM load sharing: final hypothesis verdict pending |
| Carbon conductivity: comparison with DC polarization | Unloading: springback and measured thickness |
| NCM conductivity: literature-based input review | Mixing: an adhesion parameter for SE–SE contacts |

하단 `(0.55,5.75,8.90,0.65)`14pt:

> Pending: separate launch approvals for the updated 194-bed run and the 20-bed extension.

이 문구는 이미 완료된 세대 2 소프트웨어 재검증을 다시 미완료로 만들지 않고, 발사와 보충20 범위를 분리한다. 새 런 계획을 만들어 붙이지 않는다.

**17장**

제목 `Current findings and limitations`, 본문 상자 `(0.61,1.08,8.84,3.75)`15pt. 단순 높이3.0in로 선언된 상자 밖으로 텍스트가 그려지던 상태도 정리한다.

> DEM and contact networks: composition trends from one bed per composition
>
> MPM: plastic deformation, with compaction agreement dependent on initialization and loading protocol
>
> Voxel transport: ideal-interface calculations with grid dependence and unresolved absolute conductivity
>
> Final model-validation verdicts remain pending

### P1 — 발표 품질 개선

- **1장** 이메일과 캠퍼스 그림이 겹친다. 그림은 그대로, 저자 블록 `(0.68,2.98,8.40,0.75)`에 이름16pt·소속/이메일14pt 세 줄, 세로 안쪽 여백0·행 간격18pt·문단 간격0으로 정리하는 안이다. 블록 아래가 그림 상단 y3.84보다 위에 오도록 재렌더한다. 날짜는 그대로 둔다.
- **2장** F1의 박스 제목/설명을 축약. 흐름도에서 모든 긴 보정 문장을 읽게 하지 않는다.
- **4·6·9장** 제작 지시를 notes로 옮기고 실제 그림 또는 짧은 방법 설명으로. 미완성 숫자라고 새 런을 강요하지 않는다.
- **10장** 바깥12pt 캡션으로 모식/합성/실제 수치를 구분. G6를 상대적으로 크게 둔다.
- **15장** 중앙 G5b를 notes로 옮기고 G5a `(0.55,2.95,4.30,3.00)`, G3 `(5.05,2.95,4.30,3.00)`로 확대. 재사용 이미지 자체는 무변경. 캡션12pt에서 geometric·범위를 명시한다.
- **18장** 두 열 `(0.50,1.00,4.45,5.85)`, `(5.05,1.00,4.45,5.85)`에 서지12pt, 항목 간3–4pt 간격. 검증된 인용과 본문 번호를 먼저 연결하고 기억으로 누락 칸을 채우지 않는다.

### P2 — 이번 확정의 필수조건은 아님

- 실제 그림 확보 후 6·9장 형태/전류장 보강, 필요 시 장 합치기·재배치. 현재19장·순서는 유지한다.
- 재사용4장 막대의 다음 세대 그림에서 0 시작 또는 점 도표 검토. 이번에는 원그림 재작성 금지 조건을 지킨다.
- ML 검증 규약이 맞춰진 뒤 별도 성능 그림 추가. 현0.99/0.98를 비교 성과로 끌어올리지 않는다.

## 10. 장별 한 줄 판정

`다시`는 해당 장의 글·캡션·정보 배치를 다시 정리하라는 뜻이며 새 시뮬레이션·수치 재생성을 뜻하지 않는다.

| 장 | 그대로 / 손질 / 다시 | 걸리는 것 | 고칠 것 |
|---|---|---|---|
| 1 | 손질 | 이메일과 건물 그림 겹침 | 겹침 제거. 날짜 미정 유지 |
| 2 | 다시 | 실험 보정·독립 교차검증 완료 주장, F1 넘침 | stage-specific targets와 consistency checks로. 그림도 같이 |
| 3 | 손질 | 실험 재현 완료 뉘앙스·이완 상태 | 다섯 단일 침대 중 최소. 최적비/무하중 해석 금지 |
| 4 | 손질 | T·협착 소산 정의, 잘린 축 | 식·I²R 모형 몫·축 한정 표시. 제작 지시 notes |
| 5 | 손질 | 우리 구현의 한계를 DEM 전체로 일반화 | fixed-shape soft-sphere 모델로 한정. 문헌 선정 분류 표지 |
| 6 | 손질 | 불능 CLI, 아직 없는 형태 그림 | 실제 파일·유효 명령 확인. 없어도 방법 소개 가능 |
| 7 | 다시 | 재료 출처·보정값·연화 보편성, 소제목 선 겹침 | 물성 지위 정정,70–90단어,15pt, 소제목 단축 |
| 8 | 다시 | 서로 다른 초기화/하중 이력과 확정 원인 혼합 | 역사 결과/현재 등록 분리. 원인은 후보로 |
| 9 | 다시 | 이상 계면=망CF·열 변수 혼동 | ideal-interface와 보존식 변수 구분. 같은 run 그림 |
| 10 | 손질 | 합성 예시가 실물처럼 읽힘 | illustration/synthetic 라벨.72/72는 시험 범위로 |
| 11 | 다시 | 공개계열로 반증되는 멱법칙 문구·ratio 부호 | 수렴 미입증/crosses1. F2 확대 |
| 12 | 다시 | 조성 라벨3개 누락·조건 notes에 숨음 | 다섯 라벨, 비교조건, 접촉모델/공통입력 화면 표시 |
| 13 | 다시 | large–large 오기·상태 혼동 | NCM–NCM, 고정판 이완, wallSE 제외 |
| 14 | 다시 | HOLD 추론·다른 세대 성과 혼합·탭 넘침 | 다섯 행 현재 상태표. R/Q 정의 |
| 15 | 손질 | loading·CV비교·194범위 혼합·작은3그림 |130/64·geometric·조건부배포, 두 그림 확대 |
| 16 | 다시 | ‘전부 결과 없음’, 세 문제를 닫는다는 약속 | 진단결과와 미결 판정 분리. 새 런 약속 없이 질문 정리 |
| 17 | 다시 | 두께 검증·상한·모든수치 보증 | 모형별 현재 적용 범위 네 줄 |
| 18 | 손질 | 핵심 입력/방법 인용 연결 부족 | 검증된 원전 연결,12pt. 서지 발명 금지 |
| 19 | 그대로 | 뚜렷한 문제 없음 | 기존 끝장 유지 |

## 11. 증거와 재확인 조건

새 증거:

- `evidence/input_manifest.json`: 두 ZIP의 전 파일 목록·SHA와 차이.
- `evidence/followup_checks.json`: 세 판 PPT/PDF 동일성,42패턴 스캔, F4 원자료/CSV/반올림 대조, 원본 입력 SHA.
- `evidence/saved_data_recheck_stdout.txt`: Phase A72비교,21단면 가중 집계, 공개3점 산술 반례, LHS130/64 범위 재계산.
- `evidence/v3_pptx.json`, `v3_all_slide_text.txt`, `v3_pdf_text.json`: 실제 발표물의 본문·노트·좌표·미디어 기록. 이 JSON의 폰트 목록은 직접 크기 지정만 포함하므로 제목 상속 판독과 혼동하지 않음.
- `notes/visual_1_9.md`, `notes/visual_10_19.md`: 장별 상세 배치안. **상충하면 이 통합 판정문이 우선**한다.
- 앞선 `seminar_review_20261013/codex_review_seminar_20261013.md`와 고정 소스·산술 증거를 함께 보존. 이번 문서는 그 과학 검토의 교체가 아니라 첨부물 동일성 확인과 편집 상세의 추가다.

핵심 원자료 위치는 이전 고정 사본 기준으로 다음과 같다.

| 내용 | 근거 파일/위치 |
|---|---|
| 상 전도도 입력의 미보정/이식 지위 | `scripts/step3_sigma.py:20–37`, `CLAUDE.md:586–613` |
| 옛30.7와 별도 정지 결함 | `docs/mpm3d_calibration.md:160–178`, `docs/mpm_platen_kinematic_stop_defect.md:218–235` |
| 현재 fAM 결과·미배정 판정 | `docs/reviews/fam_platen_prereg_20260812.md:905–928` |
| 공개3점·HOLD h1 | `docs/reviews/claims.json:1002–1023`, `:1209–1232` |
| AM–AM 원 집계 | `docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json` |
| v1.2 범위·별도7차 심사 | `docs/data/lhs_release_20261006_v12/README.md`, `docs/reviews/codex_review_gen2_network_reverify7_20261012.md:10` |
| F4 원자료 | `docs/data/ps45_sigmae_factor_off_20261013/factor_off_electronic.tsv` |
| F4 범주 누락 원인 | 동봉 `docs/seminar_20261013/figs/make_seminar_figs.py`, `_fmt`와`fig_ps45_sigma_e`의 호출 순서 |

다음 재확인에서는 **수정된 PPT와 그 파일에서 내보낸 PDF**가 필요하다. 개요만 바뀐 ZIP으로는 닫을 수 없다. 먼저 본문·notes·그림·요약에서 SEM-01~06이 동시에 고쳐졌는지, 이어7/9/12/15장의 해석 조건과12장의 다섯 라벨을 확인하면 된다. 자리 표시를 채웠다면 추가한 이미지의 run·상태·단위만 별도 확인한다.

새 자료가 없는 곳은 방법 설명으로 낮추거나 역사 결과로 구분할 수 있다. **덱 전체 폐기·19장 순서 변경·새 시뮬레이션은 이번 판정의 요구가 아니다.** 다만 아직 수정본을 보지 않았으므로 ‘고치면 될 것’이라는 예상만으로 조건부 GO를 선지급하지 않는다.

**최종 판정: NO-GO — 현재 파일 그대로의 발표판 확정. 위 P0 편집 후 수정 PPT/PDF 재확인.**
