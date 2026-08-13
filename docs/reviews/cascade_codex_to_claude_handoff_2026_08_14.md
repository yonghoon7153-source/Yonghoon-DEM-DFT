# Cascade Codex → Claude handoff (2026-08-14)

## 1. 릴리스 판정

현재 Cascade 산출물은 **감사·회수 상태로는 공개 가능**하지만, 90종 current leaderboard,
universal Pareto, transport shortlist, winner로는 공개하면 안 된다.

- planned slots: 273
- completed slots: 270
- completed species: 90
- reproducible historical snapshot: 47 species / 141 slots
- approved current leaderboard: 0 species
- explicit pair property labels: 0
- frozen source: `9abe5105cacafa22ab3e185f09e2a4c37118b9a9`

`90종 계산 완료`와 `90종 승인 순위`는 다른 문장이다. 회수된 90종 파일은
`recovered_unvalidated`, 47종 표는 `superseded historical snapshot`으로만 취급한다.

## 2. 이번 재감사에서 닫힌 핵심 오류

### G3

`2.14 V`는 물질 고유 상수가 아니다. LiS4가 포함된 phase set에서는 host onset이
2.140 V이고, LiS4를 제외하면 2.256 V다. 후보와 host를 **같은 phase_set_id**로
재계산하기 전에는 작은 onset 차이를 후보 고유 효과로 비교하지 않는다.

### G4

역사 G4는 canonical BVSE나 전도도가 아니다.

- `blocking`: foreign atom에서 4 Å 안에 있는 Li의 비율
- BVS: 현재 프로젝트 softBV와 다른 legacy Adams parameter
- `transport_norm`: pool min–max BVS에 blocking cutoff를 결합한 composite
- blocking이 실패하면 코드가 `transport_norm=0.05`를 강제로 넣는다.

따라서 역사 6/6 stop은 재현되는 gate pattern이지만 독립적인 산화–Li 수송
trade-off 증거가 아니다. blocking floor를 제거하면 Cr2O3, Ga2O3, In2O3,
Sc2O3, Y2O3 다섯 종은 같은 legacy BVS-only scale에서 통과하고 B2O3만 남는다.

### 90종 회수의 완결성

- champions: 270 rows / 90 species
- GP species summary: 90
- derived rank diagnostic: 89; AlI3 absent
- G1/G5 all-label complete: 88; MgI2 partial; AlI3 absent
- G4 x005 inputs present: 88; MgI2 and AlI3 missing
- G2/G3 records: 90이나 phase-set/branch comparability는 보존되지 않음

기존 `71 complete / 18 partial / 1 dropped`는 선택한 다섯 열의 ingestion 감사다.
사용하지 않는 B0를 포함하고 실제 G5가 쓰는 Pugh를 빼므로 gate completeness가 아니다.

### ML

명시적 pair property label은 0개다. 1081쌍 전역 발굴은 shuffle과 구별되지 않고
(`1.22×`, `p≈0.426`), 이미 고른 40쌍 안의 retrospective ordering만 유의하다
(`3.35×`, `p≈0.010`). ML은 predictor가 아니라 **다음 검증의 계산 순서를 제안하는
acquisition helper**로만 쓴다.

## 3. 웹앱 계약

`/cascade` 기본 화면은 audit-first다.

- 273 / 270 / 90 / 47 / 0 / 0 headline
- current leaderboard, Pareto, Li transport, G4 endpoint 기본 노출 금지
- 5개 audit-current figure + companion CSV만 기본 공개
- recovered files는 manifest hash/bytes/row가 일치할 때만 unvalidated download 허용
- historical 47은 `archive=1` opt-in
- invalid artifacts는 archive에서도 차단
- composition/element/dashboard가 old rank를 current badge로 되살리지 않음

source of truth는 `docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md`,
machine contract는 `db/properties/cascade_audit_manifest.json`이다.

### 기존 화면에 대한 정식 판정

사용자가 붙인 화면은 `90종 회수분` 탭만 새 파일을 읽고 있었고, 나머지 leaderboard,
Pareto, funnel, stability, theme, champions, `Li transport`, ESW, co-doping과 상단
`47 / 4 / 141 / 14` 통계는 47종 시대 결과였다. 이 화면은 “47종 화면 + 90종 탭”을
동시에 현재 결과처럼 보여 줘 scope와 approval status를 섞었다.

현재 구현은 이를 덧대지 않고 기본 화면 자체를 audit-first로 교체했다.

- current leaderboard/Pareto/transport 숫자와 탭을 기본 화면에서 제거
- 47종 표와 그림은 `superseded historical snapshot`으로 archive opt-in
- 90종 파일은 hash/bytes/rows가 manifest와 맞을 때만 `recovered_unvalidated` download
- `Li transport`라는 이름을 제거하고 G4의 실제 legacy BVS + 4 Å proxy를 감사 패널로 분해
- AlI3 absent, MgI2 partial, Li2S/LiCl zero-blocking artifact를 pass/fail과 분리
- composition/element/dashboard 경로가 old rank를 current badge로 되살리는 우회를 차단

따라서 Claude가 기존 8개 탭을 새 숫자로 단순 치환하면 안 된다. 승인된 current rank가
없으므로 “새 leaderboard UI”가 아니라 “감사 상태 UI”가 현재 제품이다.

## 4. 그림 생성기 계약

현재 기본 공개가 가능한 것은 다음 5개 audit panel뿐이다.

1. campaign status
2. G3 phase-set sensitivity
3. historical G4 deconstruction
4. historical post-hoc interface axes
5. ML validation / acquisition

`tools/figures/plot_cascade_audit_2026_08.py`는 pinned source/hash를 검증하고
PNG와 Origin-ready CSV를 함께 만든다. 평소에는 `--validate-only`로 사용한다.
회수 파일 materialize는 깨끗한 release workspace에서 명시 옵션으로만 실행한다.

다음 legacy plotter는 current 90 release에 일괄 실행하면 안 된다.

- concentration/errorbar/litransport/branches/synergy/composite family
- `plot_cascade_esw.py`: hard-coded 47값으로 v2 CSV를 덮을 수 있음
- `fig_cascade_radar.py`: 47 scorecard를 섞고 canonical output을 덮음
- O/F-only parser가 남은 90종 suffix shim
- v2 input이 없으면 old canonical로 fallback하는 plotter

## 5. 발표 계약

18장 본문은 winner 발표가 아니라 다음 흐름을 따른다.

1. 91×3의 체계적 설계
2. 270/273 구조·정적 screen 완주
3. 47종 공개 표가 계산 전체를 대표하지 못한 등록 경계
4. 90종 회수와 승인 0종의 구분
5. G3·G4의 정의 재감사
6. historical interface axis와 ML의 적용 한계
7. VALIDATE → RECOVER → EXPLORE → EXPLICIT PAIRS
8. 최종 산출물은 winner가 아니라 reproducible decision contract

레이아웃은 사용자 2026-06-15 연구세미나 덱의 위계를 따른다. 상단에 짧은 용어 정의,
큰 사각 불릿 주제 1개, 작은 불릿 약 2개, 하단에 scheme·그래프·식 하나를 둔다.
카드 대시보드 반복은 피한다.

## 6. 남은 계산·판정 의존성

다음이 닫히기 전에는 새 leaderboard를 만들지 않는다.

1. 90종 전체 host/candidate를 동일 phase set으로 재계산하고 `phase_set_id` 저장
2. realistic matched x에서 project-canonical softBV 재계산
3. AlI3 champion 복구 또는 명시적 unresolved 유지
4. MgI2 x005 결측 복구; missing을 fail로 세지 않기
5. 경계 후보만 multi-seed MLIP-MD 600/800/1000 K 검증
6. 그 뒤에만 explicit pair structures와 실제 pair property labels 생성
7. pair label이 생긴 뒤 prospective acquisition 성능 검증

## 7. 검증 결과

- audit generator pinned-source validation: pass
- webapp tests: 40/40 pass (`webapp/tests/test_webapp.py` direct runner)
- `/cascade` 실제 1280 px 렌더와 하단 audit/download 영역 확인
- 페이지 가로 overflow 수정
- 브라우저 console error (latest page): 0

PPTX는 본문 18장과 질문 대응 appendix를 분리한다. 최종 render·slides_test·speaker-note
QA 결과와 파일명은 이 문서의 후속 릴리스 노트에 기록한다.

## 8. Claude에게 그대로 전달할 짧은 메시지

> Cascade의 현재 정본은 90종 순위표가 아니라 감사 상태다. 273개 중 270개 슬롯과
> 90종 계산은 회수됐지만 승인된 current rank는 0종이다. 옛 47종은 역사 snapshot이고,
> G3는 phase-set ID가 빠져 있으며 G4는 canonical BVSE가 아니라 legacy BVS와 4 Å
> foreign-center cutoff를 섞은 circular composite다. 역사 6/6 stop은 재현되지만 물리적
> 산화–수송 trade-off라고 부르면 안 된다. 웹앱은 audit-first로 바꿨고, 기본 공개 그림은
> 5개 audit panel뿐이다. 다음 순서는 same-phase-set GP, matched-x canonical softBV,
> AlI3/MgI2 결측 복구, boundary MD다. 이 정의가 닫힌 뒤에야 explicit pair 계산과 ML
> acquisition을 시작한다. 새 leaderboard·Pareto·winner는 그 전까지 만들지 않는다.

## 9. Claude webapp commits `090d0df2` / `6a0dc0be` 재감사

이 두 커밋은 상단 47종 통계를 내리고 default를 audit tab으로 바꾼 점, G4의 이름을
`Li transport`에서 정적 proxy로 낮춘 점은 올바르다. 하지만 current release로는 아직
**NO-GO**다.

### P0 — 즉시 고쳐야 하는 것

1. `webapp/data.py:963`의 `90종 × 3 = 273`은 틀렸다. 설계 denominator는
   **91 chemistries × 3 nominal labels = 273**이고, 90은 completed species다.
2. `webapp/templates/cascade.html:679`의 `ESW 90종` 탭은
   `casc.oxidation`을 그리는데, loader `webapp/data.py:877-883`은 여전히
   historical `oxidation_stability_cascade.csv`를 읽는다. 즉 **90종 라벨 아래 47종 표**다.
   current tab을 없애거나 hash-pinned v2 recovery를 `recovered_unvalidated`로만 보여야 한다.
3. `cascade.html:146`은 `cascade_pool_audit_v2.json`의 71/18/1을 “gate 입력 결측”으로
   승격한다. 이 sidecar는 unused B0를 세고 used Pugh를 빼므로 gate completeness가 아니다.
   `cascade_audit_gate_completeness.csv`의 axis-specific denominator를 써야 한다.
4. `Champions / Themes / Stability / Co-doping`이 archive 배지 없이 current 탭처럼 남아 있다.
   champions/themes는 historical 47, stability는 post-hoc historical 47, co-doping은 explicit
   pair property label 0이다. 기본 tab bar에서 제거하고 archive/audit status로만 열어야 한다.
5. `webapp/data.py:987`, funnel JSON과 theme JSON은 `@x=0.05`라고 다시 쓴다. x005는
   directory label이고 v23 realized structure는 모두 **actual x=0.25**다.
6. G4 설명은 blocking rule만 쓰고 가장 중요한 circularity를 빠뜨렸다. builder는
   blocking cutoff fail일 때 min-max BVS 값을 `transport_norm=0.05`로 덮는다. 따라서 두
   독립 수송 신호가 아니다. historical 6/6에서 blocking floor를 제거하면 legacy BVS-only
   scale로 5/6이 통과하고 B2O3만 실패한다.
7. `webapp/data.py:1006`은 campaign scope를 Model C라고 하지만, v23 base roster의 실제
   host는 canonical LPSCl/comp1 계열이다. Model C screen으로 부르면 안 된다.
8. `cascade.html:255`의 “게이트 정의·순서민감도 논증은 그대로 유효”는 철회한다. G3는
   phase-set contract가 없고, G4는 circular composite, G5는 roster-relative다. terminal
   intersection의 order invariance도 독립 AND gate의 수학적 성질이지 물리 robustness가 아니다.

### P1 — 릴리스 계약

- `CASCADE_TRUTH` 하드코딩 하나를 source of truth라고 부르지 않는다. commit, sha256, bytes,
  comment-aware row count를 검증하는 `cascade_audit_manifest.json`이 machine contract다.
- GP recovery는 행 수가 90이어도 phase_set/branch comparability가 빠져 있다. “complete ESW
  result”가 아니라 “90 recovered GP records; comparison contract incomplete”라고 쓴다.
- Na2S의 B/G=2.50은 partial diagnostic에서 나온 값이므로 default headline의 새 발견처럼
  올리지 않는다. 결측이 닫힌 뒤에만 chemistry statement로 승격한다.
- 추가된 6개 테스트는 UI 라벨 회귀는 잡지만 잘못된 71/18/1 계약을 고정한다. manifest
  tamper, 90-label/47-data mismatch, generic API/archive bypass, phase_set, G4 circular rescore를
  회귀 테스트에 추가한다.

## 10. Frozen-origin 최종 line-level 판정

`090d0df2`가 실제 webapp 변경이고 `6a0dc0be`는 lint/frontmatter 정리다. 최종 판정은
**NO-GO / P0 잔존**이다. 표면의 숫자와 탭 이름은 바뀌었지만, 다음 경로에서 historical,
recovered-unvalidated, approved-current 상태가 다시 섞인다.

### P0

1. **ESW 90종 라벨 아래 47종 데이터**  
   `webapp/templates/cascade.html:110,675-680`은 `Oxidation ESW 90종`이라고 쓰면서
   `casc.oxidation`을 렌더한다. 이 객체는 `webapp/data.py:877-883,1019-1020`의 historical
   `oxidation_stability_cascade.csv`다. v2 recovery는 `data.py:888-892,1041-1044`에 별도로
   존재한다. 즉 가장 눈에 띄는 탭부터 label/data denominator가 다르다.

2. **composition / element / API에서 옛 rank가 우회 노출**  
   `/composition`은 `app.py:225-226` → `data.py:1138-1159` →
   `composition.html:58-76` 경로로 legacy rank와 score를 `Cascade hit`로 노출한다.
   `/api/element`도 `app.py:325-329` → `data.py:2791-2796,2863-2880` →
   `elements.html:127-134`에서 같은 값을 current처럼 되살린다. `/api/csv`와 `/api/file`
   (`app.py:402-414`)도 path safety만 있고 artifact-status/archive envelope가 없다.

3. **승인 0과 모순되는 peer result tabs**  
   `cascade.html:107-118`의 Champions, Themes, Stability, Co-doping은 status-only archive가
   아니라 동급 결과 탭이다. `:629-643`은 historical combined score를, `:573-625`는
   superseded theme JSON에서 새 조합 ranking을, `:506-570`은 post-hoc 축을 현재 판정처럼,
   `:684-695,779-781`은 explicit pair property label 0인데도 top-40 queue를 순위처럼 보여 준다.

4. **진단용 89행을 endpoint와 leaderboard로 승격**  
   `cascade.html:834-855`는 recovered waterfall과 G4 endpoint 28종을, `:879-890`은 89종
   ranking 전체를 노출한다. raw 270 / GP90 recovery는 registration evidence이지 scientific
   approval이 아니다. 다운로드 허용과 후보 endpoint 노출을 분리해야 한다.

5. **G4 circularity와 actual concentration 오류**  
   `build_screening_funnel.py:128-143`은 blocking이 실패하면 BVS 값과 무관하게
   `transport_norm=0.05`를 강제한다. 하지만 `webapp/data.py:982-999`와
   `cascade.html:656-665`는 두 조건을 독립 신호처럼 설명하고 `:843-848`에서 endpoint로
   사용한다. `data.py:987`의 `@x=0.05`도 틀리다. x005는 nominal label이고 realized
   concentration은 0.25다.

### P1

- G3 v2 JSON에는 `phase_set_id`, snapshot, hash가 없다. `2.140 V`를 절대 문턱으로 적용한
  90행은 same-phase-set candidate/host 비교를 증명하지 않는다. LiS4 제외 시 host onset은
  `2.256 V`다. overlap drift 0은 재실행 일치일 뿐 방법 비교 승인도 아니다.
- `CASCADE_TRUTH` (`data.py:958-971`)는 manifest-derived source of truth가 아니라 또 하나의
  하드코드다. `90종 × 3 = 273`이라는 설명도 틀리고, 계획 denominator는 `91 × 3`이다.
- Na2S의 `B/G=2.50` 카드는 삭제해야 한다. 원자료에는 x100의 음수 Hill bulk modulus와 음수
  G/B가 섞여 있고, 2.50은 `1 / mean(G/B)`라 `mean(B/G)`도 아니다. 부분 회수 diagnostic을
  연성 경험칙 반증으로 승격할 수 없다.
- 추가 테스트는 경고 문자열만 잠근다. ESW 90/47 binding, archive/API 우회, phase-set,
  G4 circularity와 actual x, pair labels 0, diagnostic rank 미노출, Na2S 유효성을 검사하지 않는다.

### 최소 release gate

1. ESW recovery를 hash-pinned `recovered_unvalidated`로 정확히 bind하고 47종 historical과 분리
2. legacy/diagnostic tabs와 composition/elements/API를 fail-closed archive policy로 통일
3. approved rank가 0인 동안 rank, Pareto, endpoint 후보명을 기본 화면에서 숨김
4. G3 same-`phase_set_id`와 matched host가 없으면 blocked
5. G4 canonical softBV/MD 재정의 전 blocked; 4 Å proxy와 강제 floor는 audit-only
6. explicit pair property labels가 0이면 co-doping은 status-only
7. 모든 headline을 pinned manifest에서 derive하고 Na2S 카드를 제거
8. 위 계약을 tamper/API/row-binding 회귀 테스트로 잠금

## 11. `23ba5244` 재감사 — P0 8건 중 1건만 닫힘

최신 webapp 커밋 `23ba5244`를 다시 동결 감사했다. 판정은 **1건 닫힘, 3건 부분,
4건 잔존 — strict audit-first NO-GO**다.

| 항목 | 판정 | 재감사 결론 |
|---|---|---|
| ESW 90종 바인딩 | 닫힘 | `casc.v2.oxidation` 90행을 실제로 렌더한다. 단 v2 부재 시 47종 fallback과 90종 배지가 갈릴 여지는 남는다. |
| legacy rank 우회 | 잔존 | composition, elements, `/api/element`, generic file/CSV API가 47종 rank/score를 상태 없이 노출한다. |
| Champions/Themes/Stability/Co-doping 상태 | 부분 | 경고 배너는 생겼지만 배너 아래 ranking, 후보, verdict가 그대로 남아 승인 0과 모순된다. |
| recovered endpoint/rank | 잔존 | G4 28종 endpoint와 89종 sortable ranking을 기본 결과처럼 계속 전시한다. |
| G4 circularity와 actual x | 부분 | 순환과 actual x=0.25 설명은 추가됐지만 circular score와 endpoint는 유지된다. builder/JSON의 `concentration_convention`도 아직 x=0.05다. |
| G3 `phase_set_id` | 잔존 | 결손 경고만 붙었고 row-level phase inventory, MP snapshot, hash가 없다. 2.140 V 절대 cutoff는 계속 적용된다. |
| manifest-derived truth | 부분 | `91 × 3 = 273` 문구는 고쳤지만 manifest에서 derive하지 않고 상수로 중복한다. 과거 71/18/1 문구도 일부 남는다. |
| Na2S/Pugh 카드 | 잔존 | 음의 Hill bulk modulus가 섞인 행에서 `1 / mean(G/B)`로 만든 2.50을 연성 반증처럼 유지한다. 삭제 또는 blocked가 필요하다. |

테스트도 같은 경계를 가진다. ESW 90행과 gate 입력 열 검사는 개선됐지만,
legacy/archive API 우회, diagnostic endpoint 비노출, row-level `phase_set_id`, manifest tamper,
Na2S 카드 제거를 검증하지 않는다. 일부 테스트는 패널 내용이 아니라 경고 문자열 존재만
확인하고, G4 테스트는 순환 제거가 아니라 순환 코드의 존재를 고정한다.

따라서 `23ba5244`의 정확한 상태는 다음과 같다.

> ESW 배선은 고쳤다. 그러나 historical·recovered diagnostic·approved current를 격리하는
> 계약과 과학적 승인 조건은 아직 닫히지 않았다. raw recovery 다운로드는 허용할 수 있지만,
> 89종 ranking, G4 endpoint, Na2S 결론은 기본 화면과 세미나 근거에서 계속 차단해야 한다.
