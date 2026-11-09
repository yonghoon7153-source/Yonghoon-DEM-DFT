# 비 Rint — DEM 첫 합성 연결·LHS O1·믹서 메타 초안 인계

1저자 11-09 밤 후속 지시 범위를 마쳤다. **DEM 합성 연결1·LHS 문서1·믹서 문서2·Q3 질문9, 연구 결과0·전체 HOLD.** Rint와 새 `[DEM 우선 (수영)]` 재설계는 이 인계의 범위가 아니다. 발송·반입은 1저자/Claude가 한다.

## 1. 바탕·반입 순서

| 구분 | 원 신원 / 이 가지 신원 | 처분 |
|---|---|---|
| 시작 B | `e91bd1c948362712def3f16b5b995027cc10011f` | 작업 시작 fetch로 확인한 최신 B 위 새 `codex/nonrint-first-link-1109` |
| 예고된 B/쪽지 | `1f71b5b7c`, `docs/collab/claude_to_codex/20261109-1900_nonrint-approved-forms-sha-map.md` | 시작 fetch에서 미확인. 반입/§6 대조를 완료했다고 쓰지 않음. 전달된 1저자 O1·후속 비준은 대화 근거로 적용 |
| 조건부 선행1 | `6b9d8e14917060465e059d91e6e63f19b1d8bd52` → `43eb8a28c95b92faa120793c0f720d8d3cd409bd` | 승인 준비 양식7. B에 같은 patch/blob가 이미 있으면 건너뜀 |
| 조건부 선행2 | `476e736e251991f4f5916fe02d990454acaa064d` → `b492a206205958a7f5ab2a53d2e14e5403690f2e` | LHS Q1 미수립/선택지 후속3. 동일하게 중복 반입 금지 |
| 새 후보1 | `<<sha:Add synthetic DEM observation boundary bridge with guarded context>>` | DEM 소스·시험·요청/근거5파일. 아래 고정 리뷰 핀과 같은 원 커밋 |
| 새 후보2 | `<<sha:Hand off non-Rint first link and metadata drafts>>` | 공통 README·LHS1·믹서2·이 쪽지5파일 |

새 후보는 위 순서로 `cherry-pick -x`. 동기 merge·superseded 양식 초안·원장 직접 수정을 포함하지 않는다. 실제 전체 SHA 목록과 패치는 Claude 전달 ZIP의 `CHERRY_PICK_COMMITS.md`에 둔다. 선행 사본의 중복 여부는 Claude의 최신 B에서 patch/blob로 확인한다.

## 2. DEM 우선 — 고정 후보와 검증

| 항목 | 상태 | 근거 | 다음 |
|---|---|---|---|
| 연결 | servo→relaxation 오프라인 **진단 후보**1. 모든 새 출력의 physical_ready/execution_go/transition_authorized/gate_write=false | 고정 리뷰 핀 `708add516725cd3566d3b6c0ca3c1b7d15a10435`; `docs/reviews/dem_gen2_observation_bridge_20261109/README.md` §명시 입력 계약·§관측·후보 판정 순서 | 반박 창 한정 검토. 실제 live reader/engine 전이/gate 활성은0 |
| 최종 같은 시험 | 원 소스에서32메서드·assertion/subtest 실패63·오류0 → 수정 후32/32 | 같은 폴더 `verification_summary.json`, final-red/final-green 원 영수증 | 실패63과 메서드32를 고유 시험 수로 더하지 않음 |
| 회귀·변이 | 기존 자격 함수22/22, guard 제거6/6 검출 | 같은 summary와 final-regression/final-mutations | 별도 관측 단위. 전체 gate/CI·실제 T0/T5/T11/T12 통과 아님 |
| 내부 발견 | 중간 후보의 dict subclass explicit-context 후퇴를3호출로 재현. 새 회귀부터 추가해 실패를 남긴 뒤 exact built-in dict 외 거부로 수정 | ZIP 내부 probe·dispatch-red·mapping-red. 최종 rules 지원형식의 명시적 축소 | 외부 판정/새 원장ID로 계상하지 않음. plain dict 무문맥22 회귀 보존 |
| 정적 보존 | 생성기·기존 자격 시험의 blob 동일. 입구 HOLD·7 gate 정의 소스 보존 | `README.md` §보존과 다음, summary preservation | 생성기18/18은 과거 기록; 이번 재실행 아님. 운영 source seal 갱신0 |
| 한계 | 토큰 결속·정수 tick·합성 scalar bounds·선언 유한 예산만. 실제 원천/T0/단위·torque·R-a/S0·serializer·P2 ULPR 미연결 | `README.md` §명시 입력 계약·§관측·후보 판정 순서 | Q2 정량 비준·Q4 실제 자격 미승인. 다음 연결은 별도 지시·고정 핀·반박 검토 |

DEM 반박용 파일=`codex_dem_observation_bridge_708add516725_review_20261109.zip`, **392111 B**, SHA256=`fb5c392ecf997646dc7a250faaf55ae0778c72d568e935881f7da164fa7f94d3`. 파일103·최상위 해시102·Git snapshot13·원증거 목록78항목을 확인했다. CRC·안전 경로·중복·정확 파일 집합 대조도 통과했다. 외부 판정은 **PENDING**이다. 원로그/시험 출처에 로컬 위치가 포함될 수 있으므로 ZIP 증거는 리포에 넣지 않고 지정 snapshot/patch만 반입한다.

## 3. 믹서 — 초안만

| 항목 | 상태 | 근거 | 다음 |
|---|---|---|---|
| ASCII 메타 초안 | 문서1, 실행·구문 검사·현장 조회0 | `docs/reviews/nonrint_first_link_20261109/mixer_ibb_metadata_command_draft.md` §1–4 | 1저자가 범위·대상·시간/bytes 예산을 본 뒤 실행 여부 별도 결정 |
| 고정 계획 빈틀 | 문서1, 수령0·실제 필드null/UNKNOWN | 같은 폴더 `mixer_ibb_fixed_qualification_plan.md` §1–4 | 현재 owner/mode/hash/FS 관측과 실제 링크/권한·변경통제/binary/MPI/자원 자격을 분리 |
| 승인 경계 | NP20/초기 E0 1/자격+별도 wave 뒤 최대2 및 순서 유지. Q2/Q3/Q5 미승인 | 같은 계획 §1·§4 | 운영 봉인·예약·pilot·wave·발사/배포0. 고정 범위 반박 GO+1저자 별도 GO 유지 |
| 과거 최종 ZIP | 미전달·Claude 미수령 그대로 | 같은 계획 §1·§5 | 최종 발사 묶음 검토 때 함께. 이번 새 문서 인계 ZIP과 혼동하지 않음 |

## 4. LHS — Q1=O1만

| 항목 | 상태 | 근거 | 다음 |
|---|---|---|---|
| 좁은 현재 신원 | 문서1: 지정 덱1개/회, 안전한 별칭·선언 종류·bytes·현재 SHA256·관측 UTC만 | `docs/reviews/nonrint_first_link_20261109/lhs_current_identity_only_draft.md` §1–4 | WSL 1저자가 대상·읽기 예산 확인 뒤만 실행. 지금 실행·구문 검사0 |
| 실행 신원 | `NOT_ESTABLISHED`, 현재 hash를 과거 사용 증명으로 대입0 | 같은 초안 §2·§5 | 원 실행 영수증이 없다는 제공자 보고와 현재 신원을 구분 |
| 남은 경계 | 원로그 본문·값 수령0, Q2–Q4 질문0 | 같은 초안 §5 | 실제 신원/정본·구간·A/C·명부/쌍·노출·값 GO를 자동 확정하지 않음 |

## 5. DEM Q3 — 1저자 한 번에 답할 질문

아래는 `43eb8a28c:docs/reviews/nonrint_approved_preparation_20261109/dem_nonresult_intake_form.md` §2–4를 답하기 쉽게 옮긴 **기존 메타·규약 질문**이다. 예시는 답 형식이며 실제 사실이나 새 정책 권고가 아니다. 이미 보유한 메타만 답하고, 없으면 `UNKNOWN`/`NOT_PROVIDED`. 새 호스트 조회·hash 산출·자격 수행·원로그/측정값 열람을 요청하지 않는다. 공통으로 제공 시각/시간대와 근거 문서 ID·판을 붙이며 외부 위치·주소·포트는 제외한다.

| 번호 | 한 줄 질문 | 답 예시(사실 아님) |
|---|---|---|
| M1 | 사용할 DEM 프로그램·빌드·코드/입력 계약 판의 **이미 보유한** 신원과 그 기록의 제공자/시각은 무엇인가요? | `프로그램=<이름/버전>; build=<기록ID>; 기존 SHA=<있으면>; 계약판=<ID>; 기록자/시각=<...>; 미확인=UNKNOWN` |
| M2 | 기존 T0·이력·복원·dt/2·재개 자격 기록은 어떤 ID·작성/검토일·빌드·실제/합성·P1/P2 범위를 가리키나요? | `기록=<ID>; 날짜=<...>; build=<ID>; 합성/실제=<...>; P1/P2=<...>; 제외범위=<문장>; 없으면 UNKNOWN` |
| M3 | 비교에서 “50 kg”은 질량 표지·장치 하중 설정·다른 규약 중 무엇이며 적용 단계/출처는 무엇인가요? | `뜻=<질량/장치설정/다른정의/UNKNOWN>; 단계=<규약상 단계>; 근거=<ID/판>` |
| M4 | 압력 면적은 다이·판·시료 중 무엇이며 기존 선언 면적/명목 치수의 단위와 고정/변동 규약은 무엇인가요? | `면적종류=<...>; 기존 선언값/단위=<있으면>; 고정/변동=<...>; 근거=<ID>; 측정값은 제외` |
| M5 | 0.7 µm·1 µm는 직경·반경·분포 대표값 중 무엇이며 두 팔의 명목 분포/절삭 규약은 같나요? | `정의=<직경/반경/대표값/UNKNOWN>; 분포/절삭=<규약문장>; 두 팔 정의=<동일/차이/UNKNOWN>; 근거=<ID>` |
| M6 | 두 입경 팔의 재료·레시피에서 유지/변경하는 선언 항목과 질량/부피 분율의 정의는 무엇인가요? | `논리 팔ID=<둘>; 유지=<규약항목>; 변경=<규약항목>; 분율=<질량/부피/UNKNOWN>; 근거=<ID>` |
| M7 | 두 팔을 비교할 규약상 측정 상태와 가압→유지→이완→제하/탈형/재하의 순서는 무엇인가요? | `비교상태=<규약상 단계>; 이력순서=<문장>; 두 팔 적용=<동일/다름/UNKNOWN>; 근거=<ID>` |
| M8 | 보고할 관측량의 연산자·단위·분모·전체/안쪽 영역은 기존 규약에서 어떻게 정의하나요? | `명칭=<...>; 연산자=<sphere/union/실험 질량-기하/기타>; 단위/분모/영역=<정의>; 근거=<ID>` |
| M9 | 대응 표본·seed·반복·기기/공통오차는 기존 규약에서 어떻게 연결하며 자료 제공 책임은 누구인가요? | `대응/반복=<기존 규약문장 또는 UNKNOWN>; 오차구분=<규약>; 보관/제공 역할=<...>; 근거=<ID>` |

답은 `M1=…`부터 `M9=…`까지 한 번에 주면 된다. 명목 면적·입경·버전 같은 **선언 메타**와 실제 압력·힘·N·porosity·KE·프레임/로그 값은 다르다. 후자는 이번 답에 넣지 않는다. M9는 새 표본 수·seed·허용폭·coverage 선택을 요구하지 않으며, Q2/Q4는 고정안·증거 준비 뒤 다시 묻는 상태를 유지한다.

## 6. 수령 범위

Rint 파일/시험/리뷰·원장·공유 진행 기록·운영 봉인 변경0. 실제 엔진·MPI·Slurm·연구 호스트·원자료 접근0. LHS/믹서 ASCII 블록은 문서의 ASCII 바이트만 확인했으며 셸에 넣지 않았다. 전체 gate/CI는 수행하지 않았고 이 합성 검증을 그 통과로 표기하지 않는다. Claude의 최신 B 통합·대응표와 DEM 반박 판정은 별도다. **전체 HOLD**.
