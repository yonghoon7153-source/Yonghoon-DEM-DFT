# R14 α·β 검증 하네스 리뷰

## 1. 판정

**R14 NO-GO — 이번 U18b 이관은 수용하지만, 네 수정의 일반적 종결은 아직 수용할 수 없다. 재계산은 요구하지 않는다.**

요청 §9는 “이 승격과 네 발견의 처리”를 함께 평가한다. 실제 승격된 13개 산출의 현재 계약, 옛 26개 파일의 보존, 공통 수치 불변은 확인했다. 그러나 U18-02의 정상 중첩 출력 경로와 U18-03의 부분 환경 기록 검사가 남는다. 문서의 승격 후 재현 명령에도 문맥 오류가 있다. 아래 **P2 세 건**을 좁게 수정하면 된다. 새 P0/P1이나 이번 데이터의 무효화를 주장하는 보고서가 아니다.

전체 하네스 GO, 본 실행 승인, COMSOL 판정과는 별개다. 요청문이 신고한 조건 6·8, U18-05, openpyxl 기록 누락 등을 새 발견으로 다시 세지 않았다.

| 식별 | 확인값 |
|---|---|
| 대상 HEAD | `1bb45b358db4850c73e185d5f851e35fbcff9ad6` |
| tree | `128fc38539fb7d996610f843b996855bd7f7b99d` |
| 범위 | `bms-balancing/`의 R14 U18 승격 및 관련 수정 |
| 첨부 요청문 SHA-256 | `17995cfd90cd838c1cc1a1df43b6cceecf59ecc615878a75c491e7fea04f9f77` |
| 작업 방식 | 별도 detached 검토 폴더. 대상 코드·정본 산출 변경 없음, 종료 시 Git 상태 비어 있음 |

## 2. 실제 실행과 읽기 검증

| 검사 | 이번 기계의 결과 |
|---|---|
| 선택 pytest | **267 passed, 10 deselected in 242.46s**, rc 0 |
| 현행 `out/ --schema-only` | **자식 rc 0**, 13개, blocker 전부 0 except `baseline_absent=1`, 승격 자격 false |
| legacy archive `--schema-only` | **자식 rc 2**, schema 40 / provenance_cols 25 / content 6 / provenance 1 |
| 현행 out 대 legacy archive | **자식 rc 4**, 명부 13/13/13, numbers 0, inputs_uncomparable 17 / env_uncomparable 1만 남음 |
| 현행 out 대 현재 HEAD | **자식 rc 2**, alias 13, numbers 0 — 요청문·회신의 rc 4와 다름 |
| 현행 out 대 승격 직전 commit | **자식 rc 4**, legacy archive 대조와 같은 blocker |
| `compare_states.py out` | 자식 rc 0 |
| MATLAB 보조 wrapper | rc 0, **Python 4·5단계만 PASS**. Octave 없음으로 1~3단계 미실행 |
| 보관 바이트 | 옛 26개 모두 승격 직전 Git blob과 동일. 새 13개 payload hash와 sidecar 일치 |
| 수치 별도 검산 | 공통 숫자 셀/JSON leaf **5,184개**, 차이 0 |

실제 자식 종료값은 `r14_cli_checks/results.json`에 저장했다. PowerShell/WSL 바깥 셸의 일반 실패값과 제품 CLI의 2·4를 혼동하지 않았다.

보안 관련 실행 우회 재생 10건은 선택에서 제외했다. 과거 재생 러너·변이 감사는 실행하지 않았다. 해당 보관 JSON의 개별 상태와 집계는 읽었지만 새 실행 증거로 세지 않는다. 제외식과 명령은 동봉 `R14_REPRO_README.md`에 있다. 따라서 제공자의 **277개 전수 통과를 이 기계에서 재확인했다고 쓰면 안 된다.**

원자료를 읽어 STATES 최적화를 다시 수행하지 않았다. U18/U18b 실데이터 실행 자체는 사용자 PC의 기록이고, 여기서 확인한 것은 보존·게시 결과·스키마·수치 비교 및 정상 기능 회귀다. COMSOL 및 별건 fit-rails의 과학 결론을 이 리뷰로 승인하지 않는다.

## 3. P2-1 — 정상 중첩 OUT이 여전히 코드 변경으로 분류된다

위치: [provenance.py:71](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-target-wsl/bms-balancing/scripts/provenance.py:71), [분류:98](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-target-wsl/bms-balancing/scripts/provenance.py:98), [g28:780](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-target-wsl/bms-balancing/tests/test_r13_codex.py:780).

서로 독립된 새 합성 Git 저장소에 README만 commit한 뒤 정상 산출 파일을 생성했다. 대상 저장소와 원자료는 수정하지 않았다.

| 상태 | 실제 함수의 `git_dirty` / `git_modified_code` | 필요한 결과 |
|---|---|---|
| `OUT=out_alt`, 그 안에 CSV 하나 | false / [] | 현재 결과가 맞음 |
| `OUT=reports/out_u18`, 그 안에 CSV 하나 | **true / ["reports/"]** | false / [] |
| 중첩 OUT + 그 밖 `reports/notes.txt` | true / ["reports/"] | 외부 파일은 계속 구분해야 함 |

실제 호출은 `git_provenance(cwd=fixture, artifact=csv, output_roots=(declared_out, "out"))`이다. 실행 자료: `r14_nested_output_checks/results.json`. Windows 및 WSL에서 관찰한 동일 원인을, 최종 self-contained 재현은 WSL에서 다시 확인했다.

원인: `git status --untracked-files=normal`이 `reports/out_u18/...`를 상위 `reports/` 하나로 접는다. 현재 분류는 그 상위 경로가 지정된 하위 root 안에 있지 않으므로 코드로 센다. 시작·끝에 같은 OUT을 넘겨도 이 문제는 해결되지 않는다. g28은 실제 연속 게시를 수행하지만 얕은 `out_alt`만 사용한다.

무효화하는 주장: 임의의 정상 출력 root에서 코드/산출 분류가 정확하다는 일반화. **실제 U18b의 얕은 `out_u18b`가 잘못됐다는 증거는 아니다.** U18-02의 원래 시작/끝 인자 불일치는 수정됐다.

최소 조건: untracked 실제 파일을 열거하거나 지정 root와 겹치는 접힌 디렉터리를 세분해 분류한다. 중첩 OUT만 있으면 clean, OUT 밖 sibling은 계속 감지하는 회귀가 필요하다. 상위 `reports/` 전체를 면제하는 임시방편이나 CLI default 제거만으로 종결하지 않는다.

## 4. P2-2 — 새 sidecar의 부분 env가 schema-only를 통과한다

위치: [check_u14.py:364](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-target-wsl/bms-balancing/scripts/check_u14.py:364), [비교 전용 검사:424](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-target-wsl/bms-balancing/scripts/check_u14.py:424), [schema ENV_KEYS:73](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-target-wsl/bms-balancing/bms_balancing/schema.py:73).

현행 정상 artifact와 sidecar를 별도 임시 사본에 복사했다. 과학 본문 bytes·SHA·receipt는 바꾸지 않고 환경 기록의 완전성만 검사했다.

| sidecar 상태 | matrix / profile / shape / degeneracy의 실제 자식 rc |
|---|---|
| 현행 완전한 env | 모두 0 |
| `env={"python": 기존 값}` | **모두 0**, schema/content/env blocker 모두 0 |
| env 자체 없음 | 모두 2 |

명령은 각 사본에 `check_u14.py --new <fixture> --schema-only`다. 12개 대조의 입력·명령·stdout·stderr·종료값은 `r14_env_schema_results.json`에 있다. 원본 및 artifact 본문 불변도 확인했다.

원인: sidecar에서는 비어 있지 않은 dict인지까지만 확인한다. `ENV_KEYS`의 python/numpy/scipy/pandas/platform 필수 검사는 baseline 비교 경로에 있고, R13에서 새로 추가한 독립 검사는 degeneracy **본문**에만 적용됐다. 이 사례에서 degeneracy 본문은 정상 그대로다. g09가 본문을 검사하는 것과 모든 sidecar가 완전한 것은 다르다.

이는 **R13 P2-4의 검사 범위 잔존 한 건**이지 종류별 네 발견이 아니다. `promotion_eligible=false`였으므로 승격 성공 반례도 아니다. 현재 실제 13개 sidecar는 모두 다섯 환경 축을 갖추고 있어 이번 이관 자료가 불완전하다는 증거는 아니다. 다만 “새 산출의 환경 계약은 schema-only가 독립적으로 강제한다”는 U18-03의 합성 논리는 완결되지 않았다.

최소 조건: 모든 새 sidecar에 공통 ENV_KEYS 존재·형식·비공백 검사를 baseline과 무관하게 적용한다. 하나씩 빠진 축은 schema-only에서도 rc 2여야 한다. 완전한 새 자료 대 env 없는 옛 baseline은 계속 rc 4·승격 불가로 남긴다. `openpyxl`을 계약에 추가하는 기신고 문제와는 별개다.

## 5. P2-3 — 승격 후 재현 명령에 이전 HEAD 문맥이 남아 있다

위치: [R13_RESPONSE.md:167](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-target-wsl/bms-balancing/reviews/R13_RESPONSE.md:167), [증거 README:13](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-target-wsl/bms-balancing/reviews/r13_repros/replay_ours_after_fixes/README.txt:13), 첨부 R14 요청문 §2.

대상 HEAD에서 그대로 실행한 결과:

```text
python3 scripts/check_u14.py --new out --old-rev HEAD
→ child rc 2; alias 13; numbers 0; inputs_uncomparable 0; env_uncomparable 0

python3 scripts/check_u14.py --new out --old-rev 42314198e0beee59834d394cdba2757183503b59
→ child rc 4; alias 0; numbers 0; inputs_uncomparable 17; env_uncomparable 1
```

두 번째 full SHA는 `37a889b^`, 즉 승격 직전 commit이다. 현재 HEAD의 out은 이미 새 정본이므로 첫 명령은 동일 run_id 13개를 가진 사본과 비교한다. **자기대조를 거부하는 코드가 맞게 동작한 것**이지 수정해야 할 rc 결함이 아니다. 문서의 “승격 뒤 HEAD 대조 rc 4”가 틀렸다.

증거 README의 `git diff ef8e8f6 HEAD --name-only -- '*.py' '*.sh'`도 대상 HEAD에서 **17개**를 출력한다. 반면 요청문의 올바른 코드 정본 `df6413d649ef51ace16d634c3856f857d598c79d`와 대상 HEAD 사이에서는 **0개**다. 같은 보관 폴더를 새 증거로 갱신하며 옛 명령 문맥이 남았다.

최소 조건: 실행 당시 target commit, old baseline commit, cwd, 정확한 명령 및 관측 rc를 함께 고정한다. 승격 전/후 명령을 구분하고 current HEAD 자기대조는 rc 2로 기록한다. 증거 코드 동일성 명령은 df6413d→1bb45b3 범위로 정정한다. 기존 실행 로그나 산출물을 소급 수정할 필요는 없다.

## 6. U18 및 조건 7 판정표

| 항목 | 판정 | 근거 |
|---|---|---|
| U18-01 shape source | 해당 원인 닫힘 | main은 SHAPE_SRC 또는 GITT만 읽음. g27은 production 전체의 argv 선택·override 축을 실제 실행 |
| U18-02 alternate OUT | 원래 인자 불일치 닫힘 / 일반화 부분 | 시작·끝 OUT 일치, g28 통과. 정상 중첩 OUT에는 P2-1 |
| U18-03 old env 부재 | 분류 방향 수용 / 새 sidecar 계약 부분 | old 부재 rc4, new 전체 부재 rc2. 부분 env에는 P2-2 |
| U18-04 schema fixture | 구현 수정 수용 | SHAPE_NON_NUMERIC 공유, legacy fixture 분리, current rc0 대조군 및 선택 회귀 통과 |
| U18-04 동시 replay 간섭 | 신고된 실행 제약 유지 | 이번에는 과거 재생 자체를 실행하지 않음. 선택 시험 성공을 해당 동시성 검증으로 세지 않음 |
| 조건 7 — 보존·새 정본·배선 | 이관 수용 | 옛 26/26 bytes, 새 13개 계약, 5,184 수치 동일, shape matrix 참조 3건 hash·행 결속 확인 |
| 조건 7 — 원자료 최적화 | 사용자 PC 실행 기록 | 여기서 실데이터 STATES 계산을 다시 수행한 것은 아님 |

새 matrix는 32/32/32/16행, profile 네 개는 각각 21행, shape는 3행이다. old/new 행 identity·순서가 같고, body run_id와 sidecar가 일치한다. 과거 불완전 sidecar를 고쳐 재실행한 것처럼 만든 흔적은 확인하지 못했다. 승격 커밋 본문도 rc4와 `promotion_eligible:false`를 그대로 남긴다.

보관 재생 JSON은 R7 5/6·closed false, R9 12/12·true, R10 20/22·false, R11 32/37·false이며 R11의 대체 없는 미실행이 남는다. 보고 완료와 엄격 종결을 분리한 새 표기는 확인했다. 이 문장은 **보관 JSON 읽기 결과**이지 독립 재생 인증이 아니다.

## 7. 요청 §7 질문에 대한 답

1. **env_uncomparable 분류를 수용한다.** 옛 baseline의 기록 부재는 새 산출의 위반과 다르다. 비교를 전면 금지할 필요는 없지만, 수치 동일성과 입력/환경 재현 동일성은 별개이며 rc4·비승격을 유지해야 한다. 새 candidate 독립 env 검사는 P2-2로 완성한다.

2. **일회성 legacy 이관과 일반 승격을 분리한다.** 이번 이관은 26개 보존, 13개 명부·신규 계약, 공통 숫자 불변을 실제로 확인했으므로 수용한다. 앞으로는 포괄적인 `--accept-uncomparable`로 정상 승격 rc0을 만들기보다, old/new 묶음 식별·대상 코드·검사 결과·허용된 unknown 사유·승인 기록을 가진 별도 `legacy_transition_approved` 판정을 남기는 편이 좋다. `promotion_eligible:false`를 지우지 않는다. 이는 데이터를 다시 계산하라는 요구가 아니다.

3. **기본은 (a) 단일 commit을 권한다.** 결과가 달라질 수 있는 `.m`, 설정, 의존성 등을 `.py/.sh`만으로 일반적으로 덮을 수 없다. 이번 9개@0668665 + 4개@419c1ab 혼재는 기신고 U18-05다. 실제 두 commit의 변경 목록은 작업 기록·COMSOL 문서·리뷰·보관 목록이므로 이번 자료에 대해 이미 수행한 범위 한정 검토는 인정한다. 일반 허용 규칙으로 승격하지 말고 두 full commit과 코드 동등성 검토 범위를 고정한 이전 예외로 기록한다.

4. **생산 기록용 시작/끝은 같은 명시 output-root 설정을 공유해야 한다.** 기록용 CLI에서 인자 생략을 오류로 만드는 방향이 명확하다. 호환성 때문에 기본 out 진단을 남긴다면 별도 명시 모드로 구분한다. 단, 인자 필수화만으로 P2-1의 접힌 상위 경로 문제는 해결되지 않는다.

5. **실제 역사 bytes를 유지한다.** archive + 고정 digest와 현행 합성 fixture + 실제 producer 시험은 서로 보완한다. 역사 표본을 합성 자료로 전부 바꾸지도, live out을 영구적인 실패 fixture로 삼지도 않는다. U18-04의 분리 방향은 맞다.

## 8. R14 종결을 위한 최소 후속 조건

1. 정상 중첩 OUT의 분류를 수정하고, 출력 밖 sibling을 구분하는 대조군까지 고정한다.
2. 종류별 새 sidecar의 필수 env 축을 독립 검사한다. 부분 env는 rc2, legacy-only 부재는 rc4를 유지한다.
3. 승격 전/후 HEAD 문맥과 코드 동일성 범위를 문서에서 full commit으로 고정하고 관측 결과를 정정한다.

**현행 과학 결과를 다시 계산하거나 옛 sidecar를 고치는 일은 필요하지 않다.** 위 후속은 코드·일반 기능 회귀·문서 정정이다. 별도로 신고된 전체 하네스의 GO 전제는 이번 좁은 R14 종결과 분리해 관리한다.

최종: **R14 NO-GO. 이번 실제 이관은 수용, 재계산 불필요, 세 P2의 좁은 후속 필요.**
