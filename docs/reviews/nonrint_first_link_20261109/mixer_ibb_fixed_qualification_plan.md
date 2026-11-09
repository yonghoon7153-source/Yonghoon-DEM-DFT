# 믹서 ibb 고정 자격 계획 빈틀 — 현재 메타 수령 전

**서식·검토 순서만 제시 / 실제 대상 결속·자격·실행 계획 고정은 미완료 / NO_GO / 전체 HOLD.** 바탕 B `e91bd1c948362712def3f16b5b995027cc10011f`, 기존 준비 사본 `43eb8a28c`의 `docs/reviews/nonrint_approved_preparation_20261109/mixer_ibb_qualification_receipt_plan.md` §1–5를 따른다. 이번 문서와 [메타 명령 초안](mixer_ibb_metadata_command_draft.md)은 실제 조회·구문 검사·시험 없이 작성했다. 이름의 “고정”은 승인된 실제 자격 계획이 이미 있다는 뜻이 아니다.

## 1. 변하지 않는 결정과 현재 빈칸

| 항목 | 상태 |
|---|---|
| 승인된 준비 대상/담당 | ibb 별칭, Linux/SLURM 한 설치, 1저자. OS 선택은 현장 명령 실행 승인과 다름 |
| 현재 메타 명령 실행 | `PENDING_AUTHOR_DRAFT_CONFIRMATION`; 실제 수령0, `receipt_id=null`, `command_rc=null` |
| 실제 설치/마운트·파일 신원 | `installation_id=null`, `source_evidence_reference=null`, 실제 observed owner/mode/hash/FS 수치 모두 `null` |
| 정책 | NP20/팔, 초기 E0 1팔, 자격 수용+별도 wave 승인 뒤 최대2팔, E0→검토→N0→검토→B1 U/C→B2 U/C→B3 U/C. 재질문하지 않음 |
| 미승인 | Q2 운영 봉인·Q3 host/wave/pilot·Q5 최종 발사/배포. `reseal_approval=null`, `pilot_go=null`, `wave_go=null`, `final_go=null` |
| 최종 인계 ZIP | 지금 미전달, Claude 미수령/중첩 해시 미재대조 유지. 최종 발사 묶음 검토 때 함께 전달 |
| 지원 경계 | 일반 native Linux 경로 대상. Windows extended/device/UNC 지원 확대나 namespace 가드 완화 없음. 모든 OS 전수 자격을 새 필수 조건으로 만들지 않음 |

## 2. 출력 → 계획 필드 연결

모든 실제 값은 아직 `null`이다. 앞으로 rc0와 완전 출력이 들어와도 “관측된 메타”, “1저자 제공/증언”, “미확인”, “자격/승인”을 분리한다. 현재 hash를 실행 당시 사용·물리 자격 또는 승인 문서의 진위로 승격하지 않는다.

| 명령 출력/수동 근거 | 채울 필드 | 이 자료만으로 채우지 못하는 것 | 현재 판정 |
|---|---|---|---|
| `target_alias`, `installation_alias`, `operator_uid`, 수집 UTC | 대상 별칭·제공자/시각·범위 참조, `raw_stdout_reference`, 확인한 명령 버전/예산 | 실제 호스트 실체·시계 신뢰성·권한 위임·한 설치의 실제 운영 root 결속 | NOT_RECEIVED |
| `installation.stat_*` | 관측 mode·UID/GID·device/inode와 수집 시점 | 조상 경로·ACL·그룹 멤버십·다른 writer·마운트 정책·변경통제 | UNKNOWN |
| `filesystem.*` | 관측 FS type hex·block bytes·blocks/inodes, 해석 단위와 특수값 사유 | 사용자 quota·실제 writable budget·공유 FS 정책·회수 목적지 여유·예상 출력 크기 | UNKNOWN |
| `binary.stat_*`, `binary.current_file_sha256` | 지정 파일의 현재 크기/metadata/hash와 별도 출처 참조 | 빌드/소스 provenance·library 결속·문법/물리/로그·실행 당시 사용 | UNKNOWN |
| `mpi_launcher.stat_*`, `mpi_launcher.current_file_sha256` | 지정 파일의 현재 크기/metadata/hash와 별도 launcher 출처 | wrapper/실제 launcher·MPI library·할당과rank·runtime 호환 | UNKNOWN |
| 최종 요소 검사 상태 | 지정 세 역할의 해당 검사 시점에 symlink가 관측되지 않았다는 제한 기록 | 실제 ancestor-link/변경통제·경합·적대적 FS/운영 도구 자격 | PROBE_NEEDED |
| Slurm·quota·runtime 등 `UNKNOWN` 출력 | 누락 사항 목록에 그대로 연결 | 실행 가능한 자원·충분한 시간/저장·등록된 예약 또는 배치 가능성 | UNKNOWN / NO_GO |

수령 기록에는 `received_by`, `received_at_utc`, `command_confirmation_reference`, `scope_reference`, `captured_start/end_utc`, `maximum_age_seconds`, `valid_until_utc`, `review_reference` 칸을 둔다. 현재 모두 `null`이다. 원본 stdout는 보존하고 제한 기록과 근거 해시를 연결하되 실제 리포 밖 경로·주소·포트·전체 환경은 리포에 넣지 않는다. 허용되지 않은 내용이 섞이면 분석을 확장하지 않고 분리 보류한다.

## 3. 고정안에 필요한 추가 영수증/자격

| 항목 | 1저자가 제공/확정할 계획·증거 | 수행/수령 경계·STOP | 완료 기준 |
|---|---|---|---|
| 한 설치·경로 | 실제 대상의 안전한 식별 참조, FS/마운트·공유 여부, 지정 사본과 운영 영역의 구분, 필요한 ancestor/link 유형 | 별도 범위 확인 전 조회/링크 생성 없음. symlink/bind mount를 이번 단일 요소 검사로 합격 처리하지 않음 | 선택 환경의 계약·필요 음성 기준과 해당 범위 검토 참조; 현재 PROBE_NEEDED |
| 권한·변경통제 | 실제 작성자/승인자·쓰기 권한·그룹/ACL 근거, 불변 창, drift 감시/STOP·보존·수동 대조 | 새 ACL/권한 변경·잠금 생성·경합 실행 없음. 승인 문서 SHA는 사람의 승인 진위를 대신하지 않음 | 근거·책임·제어된 자격 방법의 고정과 수용; 현재 UNKNOWN |
| binary/MPI 환경 | 파일 hash와 독립된 빌드/소스·의존·library·wrapper·관측 형식 계약의 기존 안전한 영수증 | 원본 파일 실행·version/help·MPI probe는 이 초안 밖. 필요 시 별도 고정 계획의 검토·승인 뒤만 | 현재 파일·예정 deck/STL/runner·실제 환경에 결속된 자격; 현재 UNKNOWN |
| Slurm/live/예약 | 본인 한 설치의 승인된 정확 job/receipt 참조, 필요한 partition/QoS·tasks/ranks/threads·현재 live와보유예약 집계·시각. 다른 본인 작업까지 cap에 영향이 있으면 그 최소 집계의 허용 범위를 먼저 정함 | 명령 초안은 Slurm client를 호출하지 않음. 전체 유저/job dump·타인 자료·제출·예약 생성/해제·lock 삭제 없음. 미관측/애매한 상태는 NO_GO | 승인 cap·NP20·해당 wave·현재 예약과 실제 할당의 근거. 설치 일부만 보고 전체 cap 만족을 추정하지 않음 |
| quota·저장·회수 | 파일시스템 free와별도인 사용자 quota/한도, inode/실제 여유, dump/restart/log 및 회수 예산과 안전한 참조 | `stat -f`만으로 충분/쓰기 가능 판정 없음. quota query가 필요하면 대상·출력필드를 별도 확인; 파일 생성/쓰기 probe는 미승인 | 승인된 수치/단위·시각·회수 대상/보존과 STOP 문턱; 현재 null |
| 시간·감시·중단 | walltime 요청과 runtime 추정 근거의 분리, 관측 신선도·진행/오류·저장 STOP, 정확 ID에만 한정한 중단·회수 책임 | 역사 속도·빈 queue 보고를 실측으로 채우지 않음. 예산/telemetry 불명·실패/부분이면 후속 wave STOP, 자동 retry/resume 없음 | 계획·실제 환경 근거·승인 참조가 결속된 시간/STOP 기준; 현재 null |
| 최종 운영 묶음 | 실제 source/deck/STL·driver/runner·physical manifest·binary/MPI·정책·승인 문서·운영자·case/wave·예약·종료/회수의 연결 | 기존 비활성43/86이나 MIP 한정 수용은 최종 봉인/배포 승인 아님. Q2/Q3/Q5는 별도 | 고정 묶음에 대한 해당 반박 창 GO와 1저자 별도 GO; 현재 NO_GO |

`UNKNOWN`은 0·빈 queue·무제한 quota·링크 없음·정상 진행을 뜻하지 않는다. 수치 TTL·walltime·disk/진행 STOP 문턱은 임의로 정하지 않으며 미정이면 자격/실행에 사용할 수 없다. 고정 파일도 바이트/환경/권한/설치 변경 시 관련 근거를 재검토하고, 동적 자원은 승인된 시점·신선도 기준으로 재확인한다. 준비→staging→job-start의 실제 결속 재확인을 수령 문서로 생략하지 않는다.

## 4. 고정과 승인 순서

1. 1저자가 ASCII 초안의 대상·범위·예산을 보고 실제 실행 여부를 별도로 정한다. 미확인 상태에서는 아무 현장 명령도 수행하지 않는다.
2. 승인된 수집이 이뤄진 경우 완전 stdout/rc와 기존 허용 영수증만 받아 위 필드에 연결한다. 부족한 필드는 UNKNOWN/PROBE_NEEDED로 남긴다. 이 단계는 자격 수행·운영 승인 아님.
3. 대상·소스·환경·선택된 실제 자격 항목·필수 증거·판정/STOP·책임을 갖춘 특정 버전의 계획을 제출한다. 합격 근거가 없는 칸을 먼저 PASS로 채우지 않는다. 실제 probe가 필요한 경우 그 범위의 검토와 별도 승인이 선행한다.
4. 운영 전환/재봉인과 E0 pilot·후속 map/wave·최종 발사/배포는 각 고정 범위의 **반박 창 GO와 1저자 별도 GO** 뒤만 가능하다. 계획 검토 전에는 NO_GO다.

E0 pilot에서 확보할 실제100k 결과를 pilot의 선행 완료 사실로 요구하거나 꾸미지 않는다. 대신 pilot 자체의 신원·현장/자원·위험수용·감시/STOP·회수의 필수 검토/GO를 유지한다. 실제 자격 결과를 수용한 다음에만 MAP_CASE_GO와 이후 wave를 별도로 심사한다. 제출 뒤 런 실패의 자동 캠페인 HOLD 전파가 없으므로 승인 운영자가 후속 wave를 멈추고 예약을 수동 대조해야 한다. 자동 해제·재시도·resume 없음.

## 5. 근거 핀과 남는 상태

- `1df1ba5a70716cdefca606031ca36b6804b565ef`: `docs/reviews/mixer_inactive_preparation_20261109/README.md` §한정 검증·§남는 조건, 같은 폴더 `author_policy_record.json`의 `adopted_policy`·승인 플래그.
- `86bceb195b2ba9802e3ab808adfaf1b1f36a11ba`: `docs/reviews/mixer_windows_path_fix_20261109/README.md` §지원 경로와 구현 계약·§시험과 독립 재확인.
- `1ffba56fb87840caf410ca85f649a997d9fe7b17`: `docs/reviews/mixer_path_limited_acceptance_20261109/README.md` §한정 종결 범위·§시험 수와 감사 한계의 구분. MIP-01 claimed_fixed+한정 종결 근거 유지, 같은 범위 새 반박 요청 없음.
- `a2e0396241c4e4cddea3c8771872f9fdcc650ef7`: `docs/reviews/mixer_first8_launch_preparation_20261106/README.md`의 `Files:`·`Future GO must name`·`Qualification release is scoped:`·`Mechanical guard details:`·`Stop rules:` 및 MLA-02/03.
- `ae9a5ddc4f413c70406ea0ea4fb8dce4e8224722`: 같은 준비 폴더 `inventory.md` §Preparation package design (fail closed)의 preflight1–6·§Monitoring, retrieval and stops.
- `d51be9e704646c24cc309df63a490050277c23db`: `docs/collab/claude_to_codex/20261109-1600_mixer-path-limited-acceptance-sha-map.md` 서두·§2–3. 최종 ZIP 미수령은 이후 저자의 최종 발사 검토 때 전달 결정과 함께 유지한다.

이번 문서의 현장 영수증·실제 조회·링크/경합 fixture·binary/MPI 실행·새 구현/시험·운영 봉인·예약 변경·원장 수정·연구 결과는 모두0건이다. **전체 HOLD**.
