# 믹서 ibb 자격 영수증 계획 — 문서 준비만

바탕 B `db86ce9b955c2aa13430680f79a431e8a580ed83`; 선행 결정표 `b7ec640bc216`의 믹서 §3·§4·§5를 구체화한다. 이번 비준 내용·공통 경계는 같은 폴더 `README.md`에 기록한다. **전체 HOLD, 실제 영수증 수집·링크 생성·시험·호스트 조회·binary/MPI 실행·예약 변경·재봉인·연구 결과는 모두 0건이다.** 이 문서는 명령이나 실행 승인 파일이 아니다.

## 1. 비준된 준비 범위와 남은 승인

| 항목 | 이번에 고정된 계획 | 여전히 승인되지 않은 것 |
|---|---|---|
| 믹서 Q1 | 대상 별칭 **ibb**, **Linux/SLURM**, **한 설치**, 계획상 자료 제공·자격 담당 **1저자**. 그 대상의 링크/권한·변경통제/binary·MPI/자원 영수증 계획을 작성한다. | 실제 설치 위치·파일시스템/마운트·실제 신원은 `null`. OS/담당 선택은 현장 읽기·링크 생성·파일 생성/변경·binary 실행 권한이 아니다. 접근 범위와 수행 승인은 별도다. |
| 지원 경로 | 현행 비활성 검증기의 일반 native local 경로 계약과 미지원 namespace의 fail-closed 거부를 유지한다. | Windows extended/device/UNC 지원은 이번 목표가 아니다. prefix 제거·별칭 우회·가드 완화 없음. Linux 선택을 해당 저장장치/공유 FS의 실제 자격으로 간주하지 않는다. |
| 믹서 Q4 | **최종 인계 ZIP은 지금 보내지 않는다. 최종 발사 묶음 검토 때 함께 전달한다.** | Claude의 최종 ZIP 미수령 및 중첩 해시 미재대조 상태를 유지한다. 문서/코드 반입과 ZIP 수령을 합치지 않는다. |
| 믹서 Q2/Q3/Q5 | 운영 봉인, host/wave·E0 pilot, 최종 발사·배포는 **미승인**이다. | 운영 봉인 교체, 실제 자격 수행, 예약 생성/해제, pilot·다음 wave·실행 GO 없음. |
| 이미 비준된 정책 | 팔당 **NP20**, 초기 **E0 1팔**, 자격 수용과 별도 wave 승인 뒤 최대 **2팔**, **E0→검토→N0→검토→B1 U/C→B2 U/C→B3 U/C**. | 재비준하지 않는다. 이 정책은 현재 할당/자원·승인 파일·특정 wave GO를 대신하지 않는다. |

## 2. 근거와 읽는 범위

| ID | B 커밋 | 문서·정확한 절/키 |
|---|---|---|
| M0 | `1df1ba5a70716cdefca606031ca36b6804b565ef` | `docs/reviews/mixer_inactive_preparation_20261109/README.md` §출처와 바뀐 범위·§한정 검증·§남는 조건; 같은 폴더 `author_policy_record.json`의 `adopted_policy`·승인 플래그 |
| M1 | `86bceb195b2ba9802e3ab808adfaf1b1f36a11ba` | `docs/reviews/mixer_windows_path_fix_20261109/README.md` §지원 경로와 구현 계약·§시험과 독립 재확인 |
| M2 | `1ffba56fb87840caf410ca85f649a997d9fe7b17` | `docs/reviews/mixer_path_limited_acceptance_20261109/README.md` §한정 종결 범위·§시험 수와 감사 한계의 구분·§Claude 반입과 원장 제안 |
| M3 | `a2e0396241c4e4cddea3c8771872f9fdcc650ef7` | `docs/reviews/mixer_first8_launch_preparation_20261106/README.md`의 `Files:`·`Future GO must name`·`Qualification release is scoped:`·`Mechanical guard details:`·`Stop rules:` 및 MLA-02/03 |
| M4 | `ae9a5ddc4f413c70406ea0ea4fb8dce4e8224722` | `docs/reviews/mixer_first8_launch_preparation_20261106/inventory.md` §Preparation package design (fail closed)의 preflight1–6·§Monitoring, retrieval and stops |
| M5 | `fa9a006f4cd11d83543f476b0066c4e8de01abdb` / `d51be9e704646c24cc309df63a490050277c23db` | `docs/collab/claude_to_codex/20261109-1530_mixer-mipr01-sha-map.md` §1·§3; `docs/collab/claude_to_codex/20261109-1600_mixer-path-limited-acceptance-sha-map.md` 서두·§1–3 |

M3/M4의 과거 NP·동시성·순서 미비준 문구는 M0의 후속 비준으로 구분한다. M1의 당시 부분 해결/재확인 대기는 M2 및 M5의 한정 수용·처분으로 구분한다. MIP-01은 `claimed_fixed`에 한정 종결 근거가 붙었으며 `verified`가 아니다. 같은 범위의 새 반박 요청을 만들지 않는다.

후보43·의존86·현재 후보 자산40의 보존/합성 근거는 실제 운영 자격이 아니다. Windows 새 시험과 Claude Linux 일반 경로 재현은 서로 다른 범위이며, Linux에서 Windows 전용 시험은 설계대로 거부됐다. 실제 링크/적대적 동시 변경/모든 OS의 자격은 이 수용에 포함되지 않는다. 필요한 자격은 **선택한 실제 운영 대상과 계약**에 한정하여 검토하며 모든 OS 전수 지원을 새 필수 조건으로 만들지 않는다. [M0–M2; M5 §3]

## 3. 공통 영수증 틀과 사전 접근 경계

모든 영수증은 **계획만 존재 / `NOT_COLLECTED`**다. 아래 `null`은 미확정이며 빈 영수증에 PASS나 승인 사실을 채우지 않는다. 실제 수집 전 1저자가 별도 접근·수행 범위, 허용 동작, 기록/반환 대상, 담당·중단 조건을 고정해야 한다. 명령·실행 스크립트는 이번에 작성하지 않는다.

| 필드 | 현재 값/기록 규칙 |
|---|---|
| `target_alias`, `target_platform`, `installation_count` | `ibb`, `Linux/SLURM`, `1` — 승인된 계획값 |
| `planned_collection_owner` | `1저자` — 실제 수집·실행 위임을 뜻하지 않음 |
| `receipt_id`, `installation_id`, `observed_by`, `observed_at_utc` | 모두 `null`; 실제 수령 건수 `0` |
| `access_approval_reference`, `execution_or_fixture_approval_reference`, `authorized_actions` | 모두 `null`; 실제 접근/수행 승인 상태 `NOT_GRANTED` |
| `subject_pin`, `manifest_sha256`, `environment_identity_reference`, `collection_method_reference` | 모두 `null`; 현장에 놓인 실제 바이트/환경과 승인된 수집 방법의 결속을 나중에 기록 |
| `raw_evidence_reference`, `raw_evidence_sha256`, `copy_receipt_reference` | 모두 `null`; 원증거는 보존하고 검토용 복사본과 전달 신원을 구분 |
| `captured_at_utc`, `maximum_age_seconds`, `valid_until_utc`, `review_reference` | 모두 `null`; 승인된 신선도 기준이 없으면 실행 판단에 사용할 수 없음 |
| `missing_fields`, `mismatch_details`, `disposition` | 아직 판정 전: `NOT_COLLECTED`. 수령 뒤 `INCOMPLETE`/`MISMATCH`/`EXPIRED`/`REVIEW_PENDING` 등 사유를 보존; 자동 GO 없음 |

리포에는 별칭·안전한 상대 식별자·해시만 기록한다. 실제 주소·리포 밖 경로·포트는 리포에 넣지 않는다. 현장 원증거에 그런 문자열이 있으면 별도 보존하고, 리포용 제한 기록은 원본 해시와 비공개 증거 식별자로 결속한다. 원자료 본문·연구 결과/값·연구 로그를 이 자격 계획에 자동 포함하지 않는다.

## 4. 영수증별 수집·판정 계획

모든 행의 계획상 제공자는 1저자다. Codex는 승인된 범위의 복사본/제한 기록만 수령·대조한다. 실제 현장 동작은 아래 문서만으로 시작할 수 없으며 각 행의 실제 값과 승인 참조는 현재 `null`이다.

| 영수증 | 승인 뒤 받아야 할 필드·사전 범위 | 신선도/보존·판정·중단 기준 | 근거 |
|---|---|---|---|
| R0 대상·범위·책임 | 한 설치 식별자, 실제 OS/FS·마운트/공유 여부의 안전한 증거 참조, 담당, 읽기/fixture/수행을 구분한 허용 동작, 목적·반환물·검토자 | ibb 별칭만으로 실체를 인증하지 않는다. 대상/권한/범위 불명·다른 설치면 수집/수행 중단 후 HOLD 반환. 아직 접근 승인 없음 | M0 §남는 조건; M3 `Future GO must name`; M4 preflight1 |
| R1 Linux 링크·경로 | 선택 대상의 경로 구성요소/조상 링크·파일 유형 판정 계약, 필요한 링크 종류·새 사본 fixture·권한·원본/복사본 그래프와 해시, 거부 시점·사유 | 실제 링크 생성은 별도 fixture 승인 뒤만. 사전 거부와 파일/디렉터리 불변을 함께 확인한다. 경로/마운트/권한 변동 시 결과 무효; 미지원 namespace를 정규화하여 통과시키지 않는다. mock/다른 OS 기록으로 대체하지 않음 | M1 두 절; M2 §한정 종결 범위 |
| R2 권한·변경통제 | 한 설치의 소유/쓰기 권한·승인된 작성자, 입력/승인/driver/runner의 불변 창, 변경 감지 신원, 제어된 경합 음성 계획·관측 순서, 원본 보존/대조 | 허용되지 않은 writer·변경·출처 불명·검사 후 drift면 STOP/증거 보존. 범용 적대적 파일시스템 방어라고 인증하지 않는다. 권한·설치·변경통제 계약이 바뀌면 재검토 | M0 §한정 검증·§남는 조건; M3 `Independent bounded review fixes:` 및 MLA-02 |
| R3 binary/MPI·환경 | 실제 binary/build/의존·MPI launcher/library·Python/runtime·환경의 신원/해시, 승인된 확인 방법, 예정 deck/STL·관측 형식과의 호환 자격 계획 | 경로 이름·버전 문자열·hash 단독으로 물리/로그 호환을 PASS로 만들지 않는다. `--help`/version 등 binary 시작도 이번 승인 아님. 준비→staging→할당 job-start의 실제 결속 재확인 필요; 바이트/환경 변경 시 무효 | M3 `Files:`·`Mechanical guard details:`; M4 preflight2–3 |
| R4 SLURM·자원·예약 | 현재 할당/정책·task/node/CPU/thread, 예정 NP20과 실제 ranks 일치, 관련 live job와 보유 예약의 합산 근거·시각, 한 설치의 admission 상태 및 수동 대조 책임 | 현재 자원과 승인된 cap을 관측해야 한다. 최대2팔 정책은 지금2팔 실행 허가가 아니다. live/예약 불명·애매한 제출/실패 영수증·cap 불충족이면 HOLD. 예약 생성/해제·lock 삭제·정책 전환·retry는 이번에 하지 않음 | M0 정책·§남는 조건; M3 MLA-01/02; M4 preflight4 |
| R5 시간·저장·회수 | 승인된 walltime과 별도 runtime 추정 근거, 실제 free/quota/inode·dump/restart/log 예산·여유/회수 공간, progress/저장 STOP 문턱, 정확한 대상 ID로 중단·새 복사본 반환하는 절차 | 수치 한계/유효기간은 현재 `null`; 역사 속도·빈 queue 보고로 채우지 않는다. 미관측/오래된 telemetry는 정상 아님. threshold/진행/저장 증거 불명·초과면 후속 wave STOP. 원자료를 삭제/덮어쓰기해 공간을 만들지 않음 | M3 `Historical estimate only:`·`Stop rules:`; M4 preflight5–6·§Monitoring, retrieval and stops |
| R6 최종 결속·검토 | 운영 후보 source/deck/STL/driver/runner/physical manifest·승인 문서의 실제 신원, 해당 범위 반박 검토 참조, 저자 별도 봉인/특정 case-wave GO, 사전/시작/종료·회수 영수증 연결 | 현재 필드/승인 모두 `null`. 기존 비활성43/86이나 MIP 경로 수용은 최종 운영 묶음 승인이 아니다. 불일치·미결·승인 범위 초과 시 실행 불가. 봉인 교체/현장 실행은 Q2/Q3/Q5 별도 승인 뒤 | M0 §남는 조건; M3 `Future GO must name`·`Qualification release is scoped:` |

**유효기간:** 고정 바이트 신원도 대상/환경/권한/설치 변경으로 관련 자격이 무효화될 수 있다. 자원·예약·저장·진행 상태는 정적 문서가 아니라 해당 판단 시점의 동적 영수증이다. `maximum_age_seconds`와 재수집 시점은 최종 범위의 승인된 기준으로 채우며 지금 임의 TTL을 정하지 않는다. 해당 기준이 없거나 만료·시각 불명·드리프트가 있으면 `UNKNOWN/HOLD`다. job-start 재확인은 이전 수령만으로 생략하지 않는다. [M3; M4 preflight1–6]

## 5. STOP·반환·검토 책임과 다음 단계

| 책임 | 계획 |
|---|---|
| 1저자 | Q1의 계획상 수집/자격 담당. 실제 접근·fixture/수행·반환 범위를 별도로 승인하고, Q2/Q3/Q5와 최종 구체안을 따로 심사한다. 이번 OS 선택은 수행 승인으로 쓰지 않는다. |
| Codex | 비활성 양식·합격/거부 기대·증거 결속을 문서화한다. 승인된 제한 자료가 도착하면 원본/복사본 신원·결손을 구분하고 원장 제안/쪽지를 준비한다. 실제 값·현장 상태를 추정하여 채우지 않는다. |
| 반박 창 | 실제 자격 계획·후속 구현·최종 발사 묶음의 고정 범위를 별도로 검토한다. 현행 MIP-01 동일 범위는 재개방하지 않는다. 기존 경로 수용을 다른 실제 자격의 GO로 전용하지 않는다. |
| Claude | 코드/문서 반입·범위 처분과 원장 적용을 맡는다. 최종 ZIP은 지금 보내지 않고 최종 발사 묶음 검토 때 함께 전달한다. 그때 수령/중첩 해시 대조 범위를 새로 기록한다. 현재 미수령 상태는 그대로다. |

실제 접근/수행이 나중에 승인되어도 결손·불일치·만료·오류·중단·부분 자료를 성공으로 반환하지 않는다. 원증거와 부분 산출물은 원바이트로 남기고, 새 복사본의 명부·해시·완전성 및 중단 원인으로 반환한다. 정확한 승인 대상/job ID 외의 취소·삭제를 하지 않는다. 자동 예약 해제·재시도·resume·다음 wave 제출은 없다. 제출 후 런 실패의 자동 캠페인 HOLD 전파가 없으므로 승인된 운영자가 후속 wave를 멈추고 수동 대조·검토를 요청해야 한다. [M0 §남는 조건; M3 `Stop rules:`·MLA-02/03]

E0 자격 pilot은 실제100k 양성을 얻기 위한 별도 제한 단계다. 아직 없는100k 결과를 pilot의 선행 완료 사실로 넣지 않는다. 대신 pilot 자체의 source/입력/실제 환경·위험수용·시간/저장·감시/STOP·회수의 필수 검토와 **반박 창 GO + 1저자 별도 GO**가 필요하다. 이후 실제 자격 결과를 수용한 뒤에만 MAP_CASE_GO와 각 후속 wave를 따로 심사한다. Q1의 문서 비준이나 이미 비준된 NP/순서는 이 순서를 낮추지 않는다. [M0 §남는 조건; M3 `Qualification release is scoped:`]

**이번 믹서 산출물은 이 계획 문서 하나뿐이다.** 신원·권한·시간·자원·수치 문턱의 실제 미확정값은 모두 미확정으로 남고, 실제 영수증 수령/판정·링크/경합 fixture·코드/시험·현장 접근·운영 전환·예약 변경·연구 결과는 0건이다. 전체 HOLD.
