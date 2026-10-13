# 연구세미나 덱의 주장과 근거 검토

검토일 2026-10-13. 대상은 첨부한 19장 PPTX와 PDF, 동봉 ZIP이다. **현 상태 그대로 최종 발표판으로 확정하는 것은 HOLD**다. 큰 줄기의 연구 소개와 상당수 수치는 유지할 수 있으나, 주장의 대상이나 검증 상태가 달라지는 P1 6건을 먼저 고쳐야 한다. 새 시뮬레이션이 아니라 **문장·출처·세대 구분을 바로잡는 작업**이 대부분이다.

이 판정은 발표자료에 대한 것이다. 194 배치, 보충 20, MPM, 믹서 등의 실행 승인·기존 생산 판정을 변경하지 않는다. 원본 PPTX/PDF, 생산 코드, 원장을 수정하지 않았고 시뮬레이션도 실행하지 않았다.

## 1. 결론과 수정 순서

| 우선순위 | 장 | 지금의 문제 | 발표 전에 필요한 최소 수정 |
|---|---|---|---|
| P1 SEM-01 | 2·17 | 세 단계가 각각 실험으로 이미 보정·교차검증됐다는 총론 | 실험 검증과 공유 입력을 가진 모델 간 일관성 검사를 분리 |
| P1 SEM-02 | 8·16·17 | 서로 다른 MPM 초기화·하중 이력을 한 결과로 연결하고 AM 하중분담을 확정 원인으로 서술 | 30.7의 역사적 조건, 현재 25.842, 미완료 판정 및 가설 지위를 구분 |
| P1 SEM-03 | 11 | 공개한 거친 격자 세 점에 다른 HOLD 계열의 ‘멱법칙 불성립’을 적용 | ‘격자 수렴 미입증’으로 교체. ratio changes sign도 crosses 1로 정정 |
| P1 SEM-04 | 13 | AM–AM 전체 하중 몫을 large–large로 바꿈 | NCM–NCM 전체 접촉으로 정정. 0:10에는 큰 입자가 없음 |
| P1 SEM-05 | 14 | 숫자만 숨기고 HOLD 상태인 h1 결론은 현재 성과로 발표 | 절차만 설명하거나 역사적 철회·보류 결론임을 명시 |
| P1 SEM-06 | 14·16·17 | 이미 배포한 v1.2와 아직 미발사인 세대 2의 재검증 7회를 합침 | 두 세대·두 시점을 별도 행으로 표시. ‘모든 수치 사전등록’ 일반화 제거 |
| P2 SEM-07 | 7 | E 24의 재료 오기, 항복응력의 보정 이력 누락, 연화 불가피성 과장 | 유리 전해질 참고값·보정값·시험한 모형의 한계로 각각 구분 |
| P2 SEM-08 | 9·17 | 이상 계면 복셀 계산을 접촉망 CF 및 물리적 상한과 동일시 | ideal-interface voxel model, 고정 기하·물성에서만 상한 |
| P2 SEM-09 | 12 | 조건부 비교의 핵심 각주가 notes에만 있고, 조성 축 라벨 3개 누락 | 측정 조건 미확인·Hertz H0·공통 기준·인자 OFF를 화면에. 축 복구 |
| P2 SEM-10 | 15 | 통합 R²를 맥락 없이 대조하고 loading을 설계축으로 기재 | 코호트별 성능·외부 CV 미확인·조건부 디스크립터 배포를 표시 |
| P2 SEM-11 | 4 | 수송 인자와 길이 굴곡도, 모형 소산 몫과 실물 원인을 혼동할 표현 | 식과 I²R 정의를 화면에 표시 |
| P2 SEM-12 | 4·6·8·9·10 | 자리 표시 명령 일부 불능, 합성 예시를 실제 스탬프와 혼동 가능 | 실제 파일·조건 확인, 유효 CLI, 모식도/계산 결과 구분 |
| P2 SEM-13 | 7·12·18 | 핵심 물성 입력·MPM·협착 법칙의 인용 연결이 빠짐 | Wang, Sakuda 및 사용한 수치방법의 출처를 장별 연결 |
| P3 SEM-14 | 1·2·7 등 | 가림·텍스트 넘침·미완성 표지 | 표지·도식·제목 선 정리, 마지막 렌더 확인 |

P1은 발표의 과학적 결론이나 증거 지위를 바꾸는 오류, P2는 해석·재현·정량 독해에 필요한 수정, P3는 편집 사항으로 구분했다. 이번 검토에서 P0는 부여하지 않는다.

**유지 가능한 핵심:** 다섯 조성의 망 수치, 새 PC 크기 인자 OFF 전자전도도, 21단면에서 집계한 AM–AM 몫, Phase A의 72/72 순서 비교, LHS 관통 수와 기하 굴곡도는 아래 범위에서 대조된다. 이들을 모두 폐기하거나 재실행하라는 판정이 아니다.

## 2. 검토 범위와 고정 자료

- 외부 첨부 PDF/PPTX는 ZIP 안 동명 파일과 각각 바이트 단위로 동일하다. PPTX 19장, PDF 19쪽, 숨긴 장 없음. 4:3 비율이다.
- 실제 PPTX 본문과 발표자 노트를 추출했고, PDF 19쪽 모두 렌더해서 확인했다. 설명 문서만 읽고 발표물 대신 판정하지 않았다.
- 근거 리포의 보조 스냅샷은 `a0439bdf8156236f454bd3f8b5bf4d044e127039`, 문헌 카드 스냅샷은 `6e568c4f0bb7df299959fd0e77e349838ad8ac98`이다. 요청서에 적힌 ‘이 요청서가 든 커밋’은 원격 조회에서 확인되지 않았다. 따라서 **첨부물 자체가 심사 대상의 정본이고, 위 커밋은 대조용이지 요청서 커밋이라고 주장하지 않는다.**
- 원자료 표, 104개 축약 팔 JSON, 21단면 기록, LHS 194행 등에 저장된 값으로 산술을 다시 했다. 원 DEM/MPM/FV 계산 자체를 다시 풀거나 전체 실험 원자료를 재측정한 것은 아니다. 협착 전력 몫은 저장된 판독값까지 대조했으며, 부재한 간선별 전류로 재합산했다고 주장하지 않는다.
- 받아 둔 근거 245파일은 고정 Git tree의 blob 해시와 대조했다. 과학 그림 17개 사용처는 원본 PNG와 SHA-256이 일치한다. 그림 해시 일치는 출처 동일성의 증거이지 물리 타당성의 증명은 아니다.

입력 SHA-256:

| 파일 | SHA-256 |
|---|---|
| PPTX | `c7849af7809a04ce19c4e301da9002d80d737bd6e2364c92f9c2667644ef3d7f` |
| PDF | `f795f0228abb6c40ba4253246f7670bf4686cdc62e810ecd2d19fc8f71d4e97f` |
| 요청 ZIP | `5f7400cfd99ecc4dead9a963d8b8e0ce6147552e1442fc9cdf6d33cd95263ebf` |

## 3. 발표의 결론을 바꾸는 여섯 항목

### SEM-01 단계별 독립 실험 보정이 완료됐다는 주장은 성립하지 않음

**P1 · 2장과 17장 · REFUTED.**

2장은 세 단계가 각각 자기 실험으로 보정됐고, 단계 사이의 일치를 cross-validation으로 취급한다고 쓴다. 새 도식도 복셀 전도를 conductivity measurements에 anchored됐다고 표현한다. 그러나 `step3_sigma.py:20–37`은 전자상 입력의 일부가 거시 모델 적합값의 이식이며, 탄소상 계수가 미보정된 동결값임을 기록한다. `CLAUDE.md:586–613`은 복셀 솔버를 독립된 두 번째 전도도 측정처럼 읽는 해석을 이미 철회한다.

같은 기하·씨앗·물성·보정 표적을 공유하면 두 계산의 일치는 **모형 조건부 일관성**일 수 있다. 실험 검증과 같지 않으며, ML의 교차검증이라는 표현과도 다르다. 7장의 미출판 보정 표적 고지는 옳지만, 그 사실이 2장의 포괄적 실험 검증 완료를 뒷받침하지는 않는다.

**교체 문장:**

> A coupled DEM–MPM–transport workflow with stage-specific calibration targets. Experimental validation is distinguished from consistency checks between models sharing geometry or material inputs.

도식의 마지막 줄은 `Conductivity inputs and experimental comparisons under review` 정도로 낮춘다. 연구 목표로 독립 보정을 지향한다고 쓰는 것은 가능하지만 완료형과 구분해야 한다.

**닫힘 증거:** 2장 본문·F1 그림·17장 요약을 같이 수정한 렌더. ‘calibrated’만 지우고 도식에 같은 주장이 남으면 미해결이다.

근거: [복셀 솔버 입력 설명](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/scripts/step3_sigma.py:20), [두 솔버의 증거 지위 정정](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/CLAUDE.md:586).

### SEM-02 MPM의 서로 다른 결과와 아직 미결인 원인을 합치면 안 됨

**P1 · 8·16·17장 · 혼합 서술 REFUTED, 개별 역사값은 조건부 보존.**

| 결과 | 실제 조건과 지위 |
|---|---|
| 30.7 µm vs DEM 30.28 µm | 옛 **cell-filled SE, se_frac 0.27, 양방향 servo** 결과. 상대차 +1.39% |
| 29.95 µm | 별도의 DEM 좌표 SE 시딩·hold 경로. 알려진 운동학적 정지 결함의 대상 |
| 25.842 µm vs 30.28 µm | 현재 등록 결과의 f=0 평형 팔. −14.66%, 두께 일치 창 밖 |
| 29.491 µm | 앞선 f(b) 규약 팔의 결과. f(a) 실행 실패 때문에 전체 등록 판정·순서 판정은 미배정 |
| 역사적 ε_sphere 1.125% vs 참고 15.6% | 과압축의 관측 기록. 그 차이 전부가 AM 하중분담 때문이라는 인과 증명은 아님 |

**30.7을 29.95의 결함과 같은 이유로 무효화하지 않는다.** 오히려 8장이 cell-filled 결과를 ‘SE seeds also come from DEM’이라는 설명에 이어 붙인 것이 문제다. 상태·입자 수·초기화·하중 경로가 같지 않은 결과를 한 검증으로 읽으면 안 된다.

또한 “AM load sharing is the missing piece”는 가설을 확정 원인으로 올린다. 원장에는 그 설명이 미검증이라고 명시돼 있다. J2 항복응력과 판의 평균 축응력은 같은 스칼라가 아니다. 예를 들어 300 MPa 정수압 상태의 von Mises 응력은 0이다. 따라서 두 수치가 0.30 GPa라고 해서 SE의 필연적인 붕괴나 그 오차의 원인이 입증되지 않는다.

16장의 `nothing below has a result yet`도 틀리다. f=0과 f(b)의 결과 및 f(a)의 실행 실패가 이미 있다. **일부 결과 존재와 최종 가설 판정 미완료를 구분**해야 한다.

**8장 교체안:**

> An earlier cell-filled servo calculation gave 30.7 µm, close to the DEM thickness of 30.28 µm. With DEM-seeded SE and an equilibrated loading protocol, the no-load-sharing run gives 25.84 µm (−14.7%). These are different initialization and loading protocols.
>
> Missing AM load sharing is a candidate explanation for over-compaction; its sufficiency remains unresolved.

짧게 줄일 경우 옛 30.7 비교를 빼고 현재의 25.84와 미완료 판정만 보여주는 편이 명확하다. 이때 현재 등록 JSON의 MPM porosity 2.585%를 역사적 ε_sphere 1.125%와 같은 정의로 대체하지 않는다. 현재 JSON에 ε_sphere 필드가 없다는 등록의 한정도 지킨다.

**16장 교체안:** `Follow-up tests address unresolved questions; completed diagnostic results are distinguished from pending confirmatory verdicts.`

**닫힘 증거:** 8장의 수치·상태·시딩 규약이 한 세트로 맞는 표/그림, 16장의 진행 상태 정정, 17장의 두께 검증 완료 뉘앙스 제거. 새 런은 이 문장 수정의 선행조건이 아니다.

근거: [옛 cell-fill 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/mpm3d_calibration.md:160), [30.7 경로를 별도 취급한 정지 결함 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/mpm_platen_kinematic_stop_defect.md:218), [현재 등록 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/reviews/fam_platen_prereg_20260812.md:905), [원인 설명의 미검증 지위](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/reviews/claims.json:84).

### SEM-03 표시한 격자 세 점으로 멱법칙 불가능을 주장할 수 없음

**P1 · 11장 · REFUTED.**

공개한 전자 비는 h=0.4/0.3/0.25 µm에서 1.4215/1.1621/1.0849다. 이 세 점에 `R(h)=A+C·h^p`를 진단적으로 대입하면:

- 증분비 `(1.4215−1.1621)/(1.1621−1.0849)=3.360103626943009`
- 이를 만족하는 양의 지수 `p=3.1312380389347334`
- 표시 정밀도에서 세 점 잔차 0

따라서 `The increments follow no power law`는 이 그림의 반례로 무너진다. **세 점·세 매개변수 적합이 가능하다는 것과 Richardson 외삽이 정당하다는 것은 전혀 다른 문제**다. 여기서 연속체 외삽값은 보고하지 않으며, 수렴 미입증이라는 결론은 유지한다.

‘양의 지수로 맞지 않는다’는 다른 미세 격자·구 스탬프 계열의 HOLD 근거다. 그 결론을 공개한 거친 격자 그림으로 입증한 것처럼 옮기지 않는다. 그림의 모든 이온 비는 양수이므로 `ionic ratio changes sign`도 `ionic ratio crosses 1`로 고친다. 부호가 바뀌는 것은 `ratio−1`이다.

**교체 문장:**

> Across the three tested voxel spacings, the electronic ratio decreases and the ionic ratio crosses 1. Grid convergence and a continuum limit have not been established; no extrapolated value or lower bound is reported.

`the headline ... is a grid artefact`, `the shape ... is real`도 ‘이 범위·표현 규약에서 관측된 격자 의존성’으로 제한한다. 물리 효과 전부가 가짜라거나 해당 형태가 연속체 법칙임을 증명한 것이 아니다.

**닫힘 증거:** 제목·본문·우측 결론·notes가 같은 계열을 설명하는 렌더. 다른 HOLD 값들을 추가해 억지로 현재 결론을 유지하지 않는다.

근거: [공개 계열 CL-24](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/reviews/claims.json:1002), [독립 산술 출력](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/evidence/verify_results_stdout.txt).

### SEM-04 AM 전체 접촉을 큰 입자끼리의 접촉으로 바꾼 명백한 오기

**P1 · 13장 · REFUTED.**

21단면의 하중 가중 평균 `Σ(load×share)/Σload`를 다시 계산하면:

| 큰 입자 : 작은 입자 | AM–AM 몫 (%) | 단면 평균 축응력 (MPa) |
|---|---:|---:|
| 0:10 | 59.5622427545 | 158.2458 |
| 3:7 | 54.6349239825 | 159.9299 |
| 5:5 | 52.3716590207 | 164.4425 |
| 7:3 | 48.4638932255 | 167.1374 |
| 10:0 | 56.9143984590 | 175.4783 |

숫자는 맞다. 그러나 **0:10에는 큰 AM이 하나도 없는데 59.56%가 나온다.** 이 열은 AM_P–AM_P, AM_P–AM_S, AM_S–AM_S를 합친 AM–AM 전체다. 따라서 large–large라는 이름은 성립하지 않는다.

읽은 상태도 가압 최고점 300 MPa가 아니라 **판 위치 고정 후 이완 상태**다. 이를 압축 정점 또는 무하중 제하 상태로 바꾸지 않는다.

**교체 문장:**

> NCM–NCM contacts contribute 48–60% of the vertical stress after compression and relaxation at fixed platen position, with the lowest contribution at 7:3.

실험 공극률과의 순위 일치는 현재의 `n=5, exploratory, selected subset`을 유지하면 탐색 관측으로 남길 수 있다. 되튐 기전·강성 역추정·AM 골격의 유일한 하중 몫으로 승격하지 않는다.

**닫힘 증거:** AM–AM 정의와 상태가 본문·범례·설명에서 일치. 막대/곡선 수치 자체를 바꿀 필요는 없다.

근거: [단면 원장 설명](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/data/ps45_plane_load_20261007/README.md:68), [21단면 원자료](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json).

### SEM-05 숫자를 빼도 HOLD 결론의 인용 문제는 남음

**P1 · 14장 첫 행 · 현재 성과로 인용 불가, 원가설의 반증 판정은 아님.**

`gain follows the represented additive volume (procedure and verdict only)`는 현재 성과로 놓여 있다. 요청서도 ‘절차·판정만’ 남기는 방침을 적었지만, 대조 원장의 CL-33은 hypothesis 자체가 `hold`이며 옛 전극 규칙에서 나온 수치·비의 재측정 전 인용을 금지한다. **요청서의 표현 방침과 원장의 현재 지위가 어긋난다.** 판정에 사용한 값이 미결이면 숫자를 숨겼다는 이유로 판정만 살아나지 않는다. 이것은 h1이 물리적으로 거짓이라는 새 판정이 아니다.

**교체 문장:**

> Historical eight-origin protocol for testing voxel representation effects. Its conductivity estimates and resulting inference remain on hold after the electrode-boundary correction.

더 짧게는 그 행을 ‘등록된 비교 절차의 예’로만 두고 h1 결과를 빼면 된다. 아래쪽 `only the procedure and the verdict are reported` 역시 함께 수정한다.

**닫힘 증거:** 화면에서 현재 유효한 성과와 역사적 보류 사례가 구분되거나, 해당 결과 행이 제거됨.

근거: [CL-33 상태와 보류 사유](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/reviews/claims.json:1209).

### SEM-06 v1.2 배포와 세대 2 소프트웨어 재검증은 다른 일임

**P1 · 14·16·17장 · REFUTED.**

14장은 `194 LHS beds → descriptor dataset v1.2`에 `7 external re-verification rounds before launch`를 붙인다. 하지만 v1.2는 **10-06의 5차 조건부 디스크립터 인계**, 기존 **세대 1** 산출물에서 열을 선별한 배포다. 10-12의 재검증 7차는 별도의 **세대 2 소프트웨어**를 심사했고, 판정문은 194 발사 승인·완주·v1.3 PASS가 아니라고 명시한다. 두 이력을 합치면 미래 생산이 이미 끝난 배포를 보증한 것처럼 보인다.

**두 행으로 분리:**

> 194-bed dataset v1.2: released for conditional use as model descriptors after review.
>
> Generation-2 transport update: seven software re-verifications completed; launch and production results remain pending.

16장의 194+20은 이 세대 2 이후 별도 계획으로 둔다. 재검증 7차가 보충 20까지 승인했다고 읽히면 안 된다.

`Every production run/number is pre-registered ... externally re-verified before it is reported`도 이 사례들만으로 전체 과거 결과에 성립하지 않는다. 보정·탐색·과거 오류 발견 사례를 소개하는 덱에서 포괄적 보증은 특히 부정확하다.

> Recent campaigns use pre-specified comparisons, fixed code, and independent review; exploratory and historical results are labeled separately.

**닫힘 증거:** 세대·날짜·승인 범위가 분리된 표, 16장과 모순 없음, 17장 전칭 문구 수정.

근거: [v1.2 배포의 범위](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/data/lhs_release_20261006_v12/README.md:1), [재검증 7차 판정 범위](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/reviews/codex_review_gen2_network_reverify7_20261012.md:10).

## 4. 조건과 표현을 보완할 항목

### SEM-07 7장의 물성 출처와 연화의 지위

**P2 · 수치 산술은 일부 CONFIRMED, 재료 출처 표기는 REFUTED, 보편성은 NOT ESTABLISHED.**

`E=1.53 GPa, ν=0.49`에서 K=25.5 GPa는 맞고, DFT 26.23 GPa 대비 약 −2.8%다. 전단탄성계수는 G=0.5134228 GPa다. 그러나 σ_y=0.30 GPa는 문헌에서 독립적으로 고정한 값이 아니라 0.15/0.20/0.25/0.30 스윕을 거쳐 순수 SE 10% 표적에 맞춘 값이다.

더 중요한 재료 오기: **E≈24 GPa는 Sakuda 2013의 75Li₂S–25P₂S₅ 유리** 참고값이다. 고밀도 열간가압 시편의 초음파 측정이지 단결정 LPSCl 값이 아니다. 원문 Results와 Methods가 이를 명시한다. [Sakuda 등의 원문](https://pmc.ncbi.nlm.nih.gov/articles/PMC3719077/). `single-crystal LPSCl range`를 그대로 두면 안 된다. σ_y 범위 역시 양 끝의 재료·규모·측정법을 특정하지 못한 상태에서 단결정 고유물성 범위라 단정하지 않는다.

`softening is irreducible for a resolved-grain continuum`도 시험한 소수 cap/jamming 설정의 실패보다 강하다. 해당 **2D 비교 절차**에서는 연화 기준 모형도 전체 압력–공극률 곡선을 맞추지 못했다. 이를 현재 3D 모델의 전 압력 검증으로 옮기지 않는다. ‘어떤 연속체 모형으로도 해소할 수 없음’이 아니라 **시험한 구현에서 미해결**이라고 쓴다.

**교체 문장:**

> The bulk modulus is kept close to our DFT value. Effective shear stiffness and yield stress are calibration parameters; σy=0.30 GPa was selected to reproduce the 10% pure-SE porosity target.
>
> The tested cap and jamming variants did not resolve the compaction mismatch. In the same 2D comparison harness, the softened baseline also failed to reproduce the full pressure–porosity curve.

`earlier citation was retracted`는 문헌 자체가 철회된 것처럼 들릴 수 있다. `Our earlier attribution of this calibration target to the literature was withdrawn`으로 바꾼다. 미출판 랩 표본이라는 현재 고지는 유지한다.

근거: [보정 스윕](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/mpm3d_calibration.md:73), [cap와 jamming 대조 범위](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/mpm_dpc_cap_crosscheck.md:25).

### SEM-08 복셀의 이상 계면 가정과 접촉망 CF를 분리

**P2 · 9·17장 · 수정 필요.**

추가 계면저항을 두지 않아도, 복셀로 표현한 좁은 목 자체의 기하학적 협착은 존재한다. 따라서 복셀 결과가 다른 그래프 솔버의 `CONTACT_FREE` 결과와 같아지는 것은 아니다.

동일한 기하·물성·경계에서 비음의 계면저항만 추가하는 경우에는 이상 계면 결과가 그 모형군의 상한이다. 다른 기하·상전도도·펠릿 입력·실험 전극까지 포함한 물리적 상한이라고 할 수는 없다. 4.04배 같은 그래프 내부 민감도를 복셀–실험 오차로 옮기지 않는다.

> The results shown use ideal interfaces, with no additional interparticle resistance. An upper-bound interpretation applies only when geometry and phase conductivities are held fixed.

또한 현재 코드에는 기본 OFF인 계면저항 기능이 있으므로 ‘솔버에 해당 항이 없다’보다는 **여기서 보인 계산이 쓰지 않는다**고 쓴다.

열전도도는 실제 구현돼 있다. 이를 미구현이라고 지적하지 않는다. 다만 열까지 한 식으로 쓸 경우 `∇·(a∇u)=0`, 전기 `(a,u)=(σ,φ)`, 열 `(κ,T)`로 구분하면 정확하다.

근거: [선택적 계면저항](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/scripts/step3_sigma.py:1696), [열전도 물성과 풀이](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/scripts/step3_sigma.py:2240).

### SEM-09 12장의 두 비교는 유지하되 조건과 축을 고침

**P2 · 수치 CONFIRMED, 한정어·표시 수정.**

왼쪽의 배수는 54.0/4.47=12.0805369, 70.6/12.4=5.6935484로 맞다. 54.0/70.6은 현재 살아 있는 p2/centerline 이력값이며, 무조건 옛 p1 금지값으로 분류하지 않는다. 그러나 온도·두께·성형 및 측정 압력·전극 조건이 미확인인 DC 값과의 비교다. 이 차이가 계면저항 또는 탄소상 입력 하나 때문이라고 식별된 것은 아니다.

화면 각주:

> Uncalibrated voxel predictions versus available DC-polarization values; measurement conditions remain to be confirmed. Potential contributors to the gap include ideal interfaces and unanchored carbon-phase conductivities.

오른쪽은 **새 다섯 침대 계산이 실제로 반입된 상태**다. 과거의 ‘혼합 조성은 아직 풀지 않았다’는 지적을 반복하면 오판이다.

| 조성 | 공통 기준 4.1 mS/cm의 Hertz H0, PC 인자 OFF (mS/cm) |
|---|---:|
| 0:10 | 0.390802043366 |
| 3:7 | 0.405815017085 |
| 5:5 | 0.402465946148 |
| 7:3 | 0.374697290936 |
| 10:0 | 0.467174544623 |

저장된 `q×4.1`과 일치하며, 대조 팔의 저장값 상대차는 0이다. 원 tgz 속 TSV도 외부 TSV와 동일하다. 공통 기준 입력은 PC와 SC의 실제 고유전도도가 같다는 측정 증거가 아니다.

화면 각주:

> Hertz/Maxwell network; common NCM reference 4.1 mS/cm; empirical PC size factor off. One bed per composition; values are conditional on the reference and contact model, not an experimental validation.

범위는 중간 반올림을 피해서 **0.375–0.467 mS/cm**로 쓰면 좋다. 실제 최솟값을 직접 소수 둘째 자리로 반올림하면 0.37이므로, 현재 0.38은 0.375를 다시 반올림한 표현이다.

그림에는 막대 다섯 개 중 **0:10과 7:3만 라벨이 보이고 나머지 셋은 빠져 있다.** 생성기에서 범주 눈금을 지정한 뒤 `_fmt`가 숫자 locator를 덮는다. `_fmt` 뒤에 다섯 범주 눈금을 지정하거나 x축 formatter를 건드리지 않도록 바꾼 뒤 실제 렌더를 확인해야 한다. 이번 리뷰에서는 이 생성기를 재실행하지 않고 납품 PDF와 호출 순서를 대조했다.

근거: [새 실행 TSV](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/data/ps45_sigmae_factor_off_20261013/factor_off_electronic.tsv), [F4의 눈금 덮어쓰기](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/input/docs/seminar_20261013/figs/make_seminar_figs.py:117), [12장 렌더](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/renders/slide-12.png).

### SEM-10 15장의 ML 성능과 인계 지위

**P2 · 수량 일부 CONFIRMED, 비교 범위 수정.**

- 130행 중 SE 관통 106행, 유한 기하 τ=1.29187488–4.15056452. 64행 확장분은 64/64 관통, τ=1.26220009–1.59991930이다. 106/130은 194 전체의 관통 수가 아니다.
- pooled OOF R²=0.9803796, MAE=0.5410 %p라는 저장 결과는 확인된다. 하지만 같은 모델의 64행 부분 R²는 0.5477643이다. 공극률 전체 분산 중 두 코호트 평균 차이가 차지하는 몫은 원 CSV 재계산으로 34.5828%다. 높은 통합 점수만으로 모든 영역을 잘 예측한다고 말하지 않는다.
- 협력자의 0.990은 v1.1 대상이고 입력 열·모델·CV 절차가 확보되지 않았다. `0.99 vs 0.98`을 동일 조건의 재현 대조로 읽히게 하면 안 된다. 누설이 있다고 단정할 증거도, 없다고 인증할 증거도 아니다.
- 배포 v1.2는 조건부 **모형 디스크립터**다. `physical_target_status=HOLD`가 59/130+62/64=121/194행이다. 이는 데이터셋을 전부 폐기하라는 뜻이 아니라 물리적으로 검증된 학습 정답과 구분해야 한다는 뜻이다.
- 130행의 loading은 모두 2.0000 mAh/cm²이며 64행 파일에는 해당 열이 없다. 저장된 다섯 입력은 AM 비율, PC 비율, 세 입경이다. 현재 근거로 loading을 독립 설계축이라 나열하지 않는다.

**교체 문장:**

> 130 base-design beds and 64 SE-rich extension beds provide model-derived structural descriptors. A five-input surrogate gives pooled porosity OOF R²=0.98, with cohort-dependent performance (R²≈0.55 in the extension).

도형의 24개 비관통 점은 유한 τ<1인 실제값처럼 보이지 않게 ‘undefined / no spanning path’ 전용 표시 영역으로 분리하면 더 명확하다.

근거: [ML 대조 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/data/lhs_ml_crosscheck_20261005/README.md:8), [배포 조건](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/docs/data/lhs_release_20261006_v12/README.md:10).

### SEM-11 수송 굴곡도와 협착 소산 몫의 이름

**P2 · 4장 · 숫자는 유지, 정의를 본문으로.**

| 큰 : 작은 AM | 수송 인자 T | σ_ion, σ₀=1.5 mS/cm (mS/cm) | 협착 소산 몫 (%) | 같은 규약의 CF 인자 |
|---|---:|---:|---:|---:|
| 0:10 | 7.2433 | 0.0587485 | 73.7348 | 1.7885 |
| 3:7 | 5.9733 | 0.0730145 | 73.3205 | 1.5030 |
| 5:5 | 5.4495 | 0.0814040 | 73.3018 | 1.3719 |
| 7:3 | 5.0297 | 0.0892940 | 72.9793 | 1.2816 |
| 10:0 | 5.2864 | 0.0837870 | 74.7437 | 1.2472 |

화면의 `transport tortuosity`는 **T=φ_SEσ₀/σ_eff**라는 수송 인자다. 경로 길이비도, 그 식의 제곱근도 아니다. `Hertz constriction`은 `Holm/Maxwell constriction resistance using Hertz contact radii`가 더 정확하다.

73–75%는 FULL 해의 `Σ I_e²R_constr,e / Σ I_e²R_total,e`다. 일정 총전류 조건에서 유효저항의 소산 분담으로 표현하는 것 자체가 틀린 것은 아니다. 그러나 이를 ‘나머지는 순수한 길이 효과’ 또는 ‘실험적으로 접촉 목이 75%를 차지함’이라고 읽히게 하면 안 된다. CF의 원기둥 bulk 근사 등도 남는다.

> Contact-constriction elements account for 73–75% of Joule dissipation in this network model.

`7:3 vs 10:0 is within seed scatter`는 이 다섯 침대의 반복 실험으로 얻은 오차막대가 아니다. 다른 시드 진단을 이 코호트의 직접 산포처럼 넣지 말고, 여기서는 조성당 한 침대라고만 제한하는 것이 안전하다.

### SEM-12 그림과 자리 표시의 재현 조건

**P2 · 4·6·8·9·10장.** 자리 표시를 둔 것 자체는 요청대로다. **네 장의 자리 표시, 빈 패널은 총 여섯 개**다. 다만 적힌 지시가 실행 가능하거나 올바른 비교를 보장하는지 별도로 봐야 한다.

| 장 | 현재 문제 | 채우기 전 필요한 것 |
|---|---|---|
| 4 | top 50% current의 정의·세대 불명확 | 같은 7:3 H0/FULL 이온 결과. top share50은 32개 z단면 평균 통과전류 몫 기준. 색은 1 V에서 j=|I|/A인지 명시 |
| 6 | `viz_mpm_morphology.py <run dir> --slice xz`는 실제 parser와 불일치 | `--se` 점군 파일 필수. 대응 scaffold·단위·시점 확인. 소성변형은 `--dg`, total strain `--eps`와 구분 |
| 8 | real_14와 격자 수만으로 30.7의 출처를 특정 못 함 | SEM-02의 초기화·servo·시점이 일치하는 실제 기록. 같은 카메라보다 먼저 같은 물리 상태 확인 |
| 9 | phase-grid·전류장 파일과 해의 대응이 없음 | full sid grid, origin, vox, phase 매핑, 전극 규칙, run 해시, 1 V와 전류밀도 단위 |

6장의 문법상 가능한 **템플릿**은 다음과 같다. 이 이름의 파일이 실제로 존재한다는 뜻은 아니다.

```text
python3 scripts/viz_mpm_morphology.py --se ACTUAL_SE_POINTS.npy --scaffold ACTUAL_AM_SCAFFOLD.csv --y 0.5 --out morphology.png
```

4장은 기존 망 그래프 수치만으로도 주장을 설명할 수 있다. 6·9장은 방법 소개로 남길 수 있다. 8장은 그림이 없어도 출처가 맞는 수치 비교표로 대체할 수 있다. 없는 계산 결과를 예시 그림으로 대신해 검증한 것처럼 보이게 하지 않는다.

10장 가운데 이미지는 **PREVIEW (synthetic)**이며 SuperP 범례를 포함한다. 실제 Phase A VGCF–PTFE 결과나 해당 캠페인의 복셀 스탬프 실물로 제시하지 않는다. 왼쪽은 첨가제 시딩 모식도다. 제목도 `Additive geometry used in transport rasterization`이 현재 근거에 가깝다. 첨가제가 물리·기계 경로에서는 전혀 없고 마지막 단계에서만 처음 생긴다는 의미로 일반화하지 않는다.

근거: [형태 렌더러 CLI](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/sources/code/scripts/viz_mpm_morphology.py:104), [10장 렌더](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/seminar_review_20261013/renders/slide-10.png).

### SEM-13 참고문헌 수보다 주장과 인용의 대응이 필요

**P2 · 7·12·18장.** 기존 14편의 수가 적어서가 아니라, 핵심 입력과 방법을 떠받치는 인용이 빠져 있다.

| 대상 | 필요한 인용/조치 |
|---|---|
| 12장 4.1 mS/cm | Wang et al., *Journal of Power Sources* 393, 75–82 (2018), DOI [10.1016/j.jpowsour.2018.05.005](https://doi.org/10.1016/j.jpowsour.2018.05.005). 펠릿 기준값을 공통 입력으로 채택한 가정 명시 |
| 7장 E≈24 GPa | Sakuda, Hayashi, Tatsumisago, *Scientific Reports* 3, 2261 (2013), DOI [10.1038/srep02261](https://doi.org/10.1038/srep02261). 재료는 위 유리계이며 LPSCl 단결정이 아님 |
| 4장 협착 법칙 | Holm, *Electric Contacts: Theory and Application*, 4th ed. (1967), DOI [10.1007/978-3-662-06688-1](https://doi.org/10.1007/978-3-662-06688-1). 실제 구현의 접촉 면적·반경 규약과 함께 인용 |
| 6장 MPM | Sulsky, Chen, Schreyer, *CMAME* 118, 179–196 (1994), DOI [10.1016/0045-7825(94)90112-0](https://doi.org/10.1016/0045-7825(94)90112-0). [저자 출판 목록](https://www.math.unm.edu/~sulsky/research/mpm.html)에서도 서지 확인 |
| J2 알고리즘 | 실제 return-mapping/유한변형 구현에 해당하는 출처. 일반 참고 후보는 Simo & Hughes, *Computational Inelasticity* (1998), DOI [10.1007/b98904](https://doi.org/10.1007/b98904). 책 존재가 코드 구현의 일치 증명은 아님 |

Sakuda는 원문에서 재료와 측정법을 확인했다. Wang 수치의 세부 조건은 반입된 정본 카드와 등록 기록을 대조했다. Holm·MPM·Simo는 원문 카드 보강 후보이며 이번에 덱에 삽입하지 않았다. 저자·출판사 서지를 확인한 것과 책/논문 전체 식을 구현에 맞춰 검증한 것을 혼동하지 않는다.

기존 서지 중 **LIGGGHTS 3.8.0, commit 3d5c00f (2024)**는 해당 스냅샷 날짜로 성립한다. 이를 버전 파일의 오래된 갱신 연도로 억지 정정하지 않는다. Shi의 2020, So의 권 508도 오류로 잡지 않는다. 개별 세부 서지와 확인 범위는 증거 묶음의 `notes/references_terms.md`에 있다.

### SEM-14 시각적 완성도

**P3.** 내용 수정 뒤 다음을 손보면 된다.

- 1장: 이메일이 아래 그림에 가려진다. 날짜도 미정 표지다.
- 2장 F1: 긴 단계 설명이 박스 밖으로 나온다. 문구를 줄이거나 박스 폭·줄바꿈을 재조정한다.
- 7장: 오른쪽 소제목의 anchor가 가로선과 겹친다. `Calibration target and limitations`처럼 줄이거나 선을 내린다.
- 12장: 빠진 축 라벨은 장식 문제가 아니라 조성 식별 문제이므로 SEM-09의 P2로 처리한다.
- 4장: 잘린 y축의 막대는 조성 차이를 크게 보이게 한다. 0 시작 막대 또는 점·오차 표현 없는 점도표를 고려한다. 시드 반복이 없으므로 가짜 오차막대를 만들지 않는다.
- 14장: 표 글씨 밀도가 높다. 과거 보류, 현재 유효 결과, 향후 세대를 분리하면서 행별 문장을 짧게 한다.

## 5. 요청 Q1부터 Q6까지의 답

### Q1 과장과 누락

- **3장 densest of five:** 이 다섯 개 계산 침대에서 7:3이 최소라는 기술은 가능하다. 반복 없는 한 조성 최적화나 일반적 최적비로 부르지 않는다. 제목은 `DEM predicts a composition-dependent porosity`가 실험 재현 완료를 암시하는 `reproduces`보다 안전하다.
- **4장 73–75%:** 저장값은 맞다. 모형의 I²R 몫이라는 정의를 화면에 둔다. 실물의 유일한 제한 요인이나 순수 경로 길이와의 분해로 표현하지 않는다.
- **12장 ×12/×5.7:** 나눗셈은 맞다. 비교 조건 미확인과 미보정 예측이라는 지위를 화면에 둔다.
- **13장 순위 일치:** n=5·선택된 실험 집합·탐색이라는 현재 한정은 유지할 수 있다. 그러나 대상은 large–large가 아니라 AM–AM이고, 고정판 이완 상태다.
- 더 중요한 총론 과장은 SEM-01·02·05·06이다. 제목·그림·요약이 notes의 한정을 뒤집지 않도록 함께 수정해야 한다.

### Q2 금지값과 내부 용어

실제 PPTX 본문+notes에서 **quotation_ban 42개 문자열의 일치 0건**이다. 열람한 그림에서도 금지된 미세 격자 전도도나 옛 8팔 이득의 직접 숫자 누출은 발견하지 않았다. 다만 이것은 OCR·모든 의미적 인용의 무결성 증서가 아니다.

실제 위반은 **의미 수준**에서 있다. 11장의 다른 HOLD 계열 진단, 14장의 HOLD h1 결론이다. 숫자만 안 쓰면 되는 것이 아니다. 반대로 Phase A의 0.15 µm 설정, 72/72, 별도의 살아 있는 p2 값까지 일괄 금지하면 오판이다.

내부 용어 0도 전역적 사실은 아니다. 4·6·8·9장 자리 표시에는 ps45, uma, WSL, real_14, STEP3, 스크립트 경로가 남는다. 요청자가 채우기 지시를 명시적으로 요구한 **초안 예외**이므로 이를 비밀 누출로 보지는 않는다. 발표판에서는 notes로 옮긴다. 생성기의 좁은 regex가 이 단어들을 보지 않는다는 사실은 수정을 필요로 하는 검사 범위 설명이다.

### Q3 그림의 출처와 세대

| 장 | 실제 삽입 그림 | 판정 |
|---|---|---|
| 2 | F1 새 도식 | 출처 일치, 문구 과장 SEM-01 및 넘침 수정 |
| 3 | ps73 aligned checkpoint 4단계, G1 | 해시 일치. 31.8/25.1/16.7/16.5는 정렬한 checkpoint 판. 마지막 165 MPa는 무하중 제하 아님 |
| 4 | p14 Hertz 인자, p15 σ₀=1.5 | 해시·표 산술 일치. 생성 세대와 φ/L 규약 유지 |
| 5 | 이력 주기 코드 재현 그림 | 원본과 동일. 실험 force trace가 아니라 모델 그림 |
| 10 | 첨가제 seed, synthetic preview, G6 | 원본 일치. 앞 두 그림은 모식도/합성 예시이며 Phase A 실제 결과와 분리 |
| 11 | F2 공개 세 점 | CSV와 일치. 멱법칙 결론은 불일치 |
| 12 | F3·F4 | 수치 파일 일치. F4의 범주 눈금 결손 |
| 13 | 하중 기여, SE 응력 4단계 | 원본 일치. 응력 색은 0–150 MPa 선형 판. AM–AM 오역 정정 |
| 15 | G5a·G5b·G3 | 해시 일치. 106/130 및 유한 τ 범위 재계산 일치; 194 전체로 확대하지 않음 |

합계 **재사용 그림 13개+동봉 새 그림 4개=17개** 사용처를 확인했다. 나머지 그림 사용처는 템플릿 배경·로고·장식 계열이다. 과학 이미지 해시 일치와 원자료 재풀이의 검증 수준은 다르다.

### Q4 표준 용어

| 현재 표현 | 권장 표현 |
|---|---|
| rigid-sphere DEM | soft-sphere DEM with fixed spherical particle shapes |
| transport tortuosity | transport tortuosity factor, T=φ_SEσ₀/σ_eff |
| geometric tortuosity | geometric shortest-path tortuosity, τ_geo=L_path/L_z |
| Hertz constriction | Holm/Maxwell constriction using Hertz contact radii |
| contact-free branch | ideal-interface voxel model, no additional interparticle resistance |
| stress-stop thickness | thickness at the prescribed axial-stress stopping criterion; 목표와 평형/순간 판독 시점 명시 |
| origin-replicated | eight voxel-grid origin offsets / grid-origin sensitivity analysis |
| DC polarization | DC-polarization electronic-conductivity measurement |
| Heckel test | tested compaction-curve / cap-model cross-check |

grid origin 변경은 같은 침대를 다시 복셀화한 수치 민감도이지 8개의 독립 제조 표본이 아니다. DEM·MPM·FV·AM·SE·VGCF·PTFE·OOF·SBE/DBE는 처음 등장할 때 이름을 풀어준다. 14장의 R과 Q는 각각 모델/문헌 실험 비와 PTFE 처리 뒤 유지비로 정의한다. Q=0.84의 ‘예측 적중’은 실험값 적중이 아니라 등록했던 약한 차단 민감도 예측의 적중이다.

### Q5 자리 표시

‘자료 없음’ 표지 자체는 정직하며 요청에 맞다. 하지만 6장 명령은 고쳐야 하고, 8장의 비교는 SEM-02를 해결한 뒤 채워야 한다. 나머지도 파일·run·단위·세대·시점이 확인돼야 한다. 외부 그림이 확보되지 않으면 방법 설명이나 수치표로 남겨도 되며, 보여주기 위해 근거 없는 전류장·형태 그림을 만들 필요는 없다.

### Q6 문헌

14편이라는 개수 자체에는 합격선이 없다. 발표의 실제 식·수치가 연결되는지가 기준이다. 가장 시급한 누락은 **4.1 mS/cm의 Wang**, **E24의 Sakuda**, **협착 법칙의 Holm**, **MPM 기본 문헌**이다. 원문 카드가 없다는 이유로 서지를 발명하지 않은 것은 옳지만, 그 상태를 최종 인용 완료로 볼 수도 없다. 18장 목록만 늘리지 말고 관련 장에 짧은 인용 번호를 붙인다.

## 6. 수치 확인에서 살아남은 것

- 3장 조성별 exact-union 공극률 20.59·18.67·17.67·16.49·16.90%는 표시와 자료가 맞는다. 7:3의 기술적 최소를 유지할 수 있다. 실제 구 합집합 부피를 새로 적분한 검증은 아니다.
- 5장 감쇠 57.9→58% 및 22편 집계는 원 보고서와 일치한다. 문헌 통계는 ‘선정 문헌에 대한 저자 분류’이며, 0/22를 전 분야 부재 증명으로 쓰지 않는다. 원 표에는 추가 논문이 별도로 함께 있으므로 선정 집합과 보충 사례의 경계를 notes에 남긴다. 이번에 22편 전체 원문을 모두 다시 심사한 것은 아니다.
- Phase A는 96 primary+8 QC JSON을 읽어 72개 인접 조성 비교를 다시 계산했다. 등록 수치 문턱에서 위반 0, 지정 QC 묶음의 최대 replay 차이 0이다. 지지되는 것은 **시험한 세 격자·여덟 origin에서의 순서**다. 72개 독립 물리 실험, 전체 수렴 증명, 모든 조성의 replay 증명은 아니다.
- 12장 새 PC 인자 OFF 다섯 값은 반입 결과와 맞는다. 내부 50 mS/cm를 실측값처럼 재인용하거나 경험 크기 인자 ON의 하락 추세를 그대로 유지하는 문제는 이 패널에서 발견되지 않았다.
- 13장 AM–AM 값은 21단면에서 독립 재집계했다. 순위는 살아남지만 정의를 고쳐야 한다.
- Lee의 R≈2.074와 Q≈0.840은 원 기록에 부합한다. 2배 밴드 통과라고 쓰지 않은 것은 옳다. Tier 1 오더 대조라는 한정과 측정/모형 차이를 유지한다.

## 7. 장별 최종 편집 체크리스트

| 장 | 결정 |
|---|---|
| 1 | 이메일 가림 제거, 날짜 입력 |
| 2 | SEM-01 적용. F1까지 고침 |
| 3 | 수치 유지. ‘다섯 단일 침대 중 최소’, fixed-platen relaxation 표기 |
| 4 | T 정의·H0·I²R 모형 몫 화면 표시. 전류 그림은 실제 기록 확보 후 |
| 5 | 우리 구현의 한계로 제목 제한, 22편 선정 분류라고 표시 |
| 6 | 방법 소개 유지. 유효 CLI와 실제 파일 확인, 임의 그림 금지 |
| 7 | 재료 오기·보정 이력·보편적 irreducible 주장 정정, 소제목 충돌 제거 |
| 8 | 다른 초기화/하중 이력 분리. 30.7을 현재 R3-v2 검증값으로 사용하지 않음 |
| 9 | ideal-interface 규약, 열의 변수 구분, 그림 run 확인 |
| 10 | 72/72 유지. 합성 예시 라벨, grid origin 민감도 범위 명시 |
| 11 | 멱법칙 불가능 삭제, crosses 1, 수렴 미입증으로 제한 |
| 12 | 값 유지, 최소값 범위 정리, 화면 각주 및 다섯 x라벨 |
| 13 | large–large→NCM–NCM, 이완 상태 명시. 탐색 순위 한정 유지 |
| 14 | HOLD 결론과 현재 성과 분리. v1.2·세대2 이력 분리, R/Q 정의 |
| 15 | loading 제거, 130/64 범위·R² 조건·모형 디스크립터 지위 표시 |
| 16 | 이미 있는 fAM 결과와 미완료 판정 구분 |
| 17 | 독립 검증 완료·물리 상한·모든 수치 보증 문구 제거 |
| 18 | 핵심 물성/방법 인용 보강 및 관련 장 번호 연결 |
| 19 | 특별한 과학 내용 없음. 표지와 연락처 표기 일치 확인 |

## 8. 재현과 해제 확인

증거 묶음의 루트는 `seminar_review_20261013/`이다. `sources/code/`와 `sources/lit/`에는 고정 커밋의 읽기 전용 사본이 있다. 전체 재료는 패키지 manifest로 해시를 확인할 수 있다.

```text
python -X utf8 -B seminar_review_20261013/audit_artifacts.py
python -X utf8 -B seminar_review_20261013/verify_results.py
```

두 명령은 저장 자료의 판독·산술만 수행한다. DEM·MPM·FV·배치 러너를 부르지 않는다. PPTX/PDF 추출과 입력 동일성은 `inspect_bundle.py`, 검사 결과는 `evidence/`에 있다. `finalize_evidence.py`는 이 작업 폴더와 원 다운로드 경로가 유지된 환경에서 원본 무변경 및 소스 tree 해시까지 확인하는 포장 도구다.

해제 확인은 새 PPTX와 그 렌더 PDF에서 다음을 보면 된다.

1. SEM-01부터 06의 본문·그림·notes·요약이 서로 일치함.
2. 7·9·12·15장의 주요 한정이 발표자 노트에만 숨지 않고 화면에 있음.
3. 13장의 AM–AM 정의, 11장의 같은 데이터 계열, 14장의 세대·HOLD 상태가 고쳐짐.
4. 12장의 다섯 조성 라벨이 모두 보임.
5. 자리 표시를 채운 경우 실제 run·상태·단위 출처를 추가함. 못 채웠다면 이를 방법 설명으로 제한함.
6. 원본 값에 새 수치나 새 성과를 추가했다면 그 항목만 추가 확인함.

**최종 판정: 발표판 확정 HOLD. 위 문장·출처·표시 수정 후 재확인 대상이며, 이 검토가 새 생산 실행이나 전면 재계산을 요구하는 것은 아니다.**
