# R14 후속 확인 — f21cb648

## 판정

**R14 NO-GO 유지 — 세 조건 중 둘은 종결, P2-2의 비공백 검사 한 항목만 남는다.**

이번 U18b 이관 수용과 과학 계산 재실행 불필요 판정은 그대로다. 새 P0/P1, 과학 결과의 손상, 실제 승격 성공 사례를 발견했다는 뜻이 아니다. 이전 P2-2의 좁은 잔여 조건이며 새로운 여러 발견으로 세지 않는다.

- 대상: `f21cb6480fc27857c7aac67e823cae62b1443830`
- 브랜치: `claude/bms-alpha-beta-verify`
- 범위: `bms-balancing/`의 R14 P2 세 건 후속. COMSOL은 범위 밖.
- 대상 코드·원본 out·Git 이력 수정 없음. 검사는 별도 detached 작업트리와 임시 사본에서 수행했다.

## 조건별 판정

| 조건 | 판정 | 실제 근거 |
|---|---|---|
| P2-1 중첩 OUT | **종결** | 이전 리뷰의 동일 세 대조군 재실행. 얕은 OUT clean, 중첩 OUT clean, root 밖 sibling은 dirty이며 `reports/notes.txt`를 정확히 지목 |
| P2-2 새 sidecar env | **부분** | 네 종류 모두 정상 env rc0, python만 남긴 env rc2, env 전체 부재 rc2. 필수 키 누락은 닫혔으나 공백뿐인 값은 아직 rc0 |
| P2-3 재현 문맥 | **종결** | full baseline `42314198…3503b59` 대조 rc4, 현재 HEAD 자기대조 rc2/alias13. 문서의 기준과 실제 결과 일치 |

P2-1의 `_untracked_files()`와 root 밖 sibling 회귀는 원래 지적에 대응한다. 상위 디렉터리 전체를 면제하지 않고 실제 하위 파일을 구분한다.

P2-3에서 원래 첨부 요청문의 잘못된 문맥을 소급 수정하지 않고 정정문을 분리한 것은 적절하다. 요청문과 이전 리뷰 ZIP의 바이트 보존을 확인했다.

## 남은 P2-2 — 비공백이라는 말과 빈 문자열 검사 사이의 차이

위치: [check_u14.py:373](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-response-f21cb648-wsl/bms-balancing/scripts/check_u14.py:373).

현재 구현은 각 ENV_KEYS 값을 `in (None, "")`으로 검사한다. 이 검사는 누락·null·빈 문자열을 거부하지만, 공백 문자열은 거부하지 않는다. 회신 및 코드 주석의 **존재·비공백 요구**가 완전히 구현된 것은 아니다. 기존 degeneracy 본문 검사는 [schema.py:180](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-response-f21cb648-wsl/bms-balancing/bms_balancing/schema.py:180)에서 공백 제거 후 빈값을 판정한다.

### 실제 입력과 결과

정상 `out/matrix_100.csv`와 sidecar를 별도 임시 디렉터리로 복사하고, 사본 sidecar의 `env.scipy`만 바꿨다. 과학 본문·원본 sidecar·artifact hash는 그대로다.

| `env.scipy` 값 | 실제 자식 rc | schema blocker | 필요한 결과 |
|---|---:|---:|---|
| 원래 `"1.18.1"` | 0 | 0 | 정상 |
| `""` | 2 | 1 | 정상 거부 |
| `null` | 2 | 1 | 정상 거부 |
| `"   "` | **0** | **0** | 비공백 계약에 따라 rc2 |
| `"\t\n"` | **0** | **0** | 비공백 계약에 따라 rc2 |

모든 경우 `--schema-only`이며 `promotion_eligible=false`다. **승격을 성공시킨 사례가 아니라 candidate 독립 스키마 검사의 누락**이다.

각 사본에 실행한 명령:

```text
python scripts/check_u14.py --new <별도 fixture 디렉터리> --schema-only
```

동봉 `r14_env_value_checks_f21cb648.py`를 실행하면 위 다섯 대조군을 새 임시 사본에서 만들고 자식 rc·stdout·stderr·원본 불변을 JSON으로 기록한다.

### 회귀가 보는 것과 안 보는 것

[test_h02:74](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-response-f21cb648-wsl/bms-balancing/tests/test_r14_codex.py:74)는 네 종류 각각에서 온전 대조군, 다섯 필수 키를 하나씩 제거, python만 남김, env 전체 부재를 실제 CLI로 검사한다. **키 누락 축은 제대로 검사한다.** 그러나 키가 존재하면서 값이 공백뿐인 경우는 실행하지 않는다. 그 때문에 이 수정에 대한 기존 회귀 통과와 위 잔여 입력이 동시에 성립한다.

### 최소 종결 조건

1. 본문·sidecar의 필수 환경 값 판정을 공통화하거나 같은 비공백 규칙을 적용한다. 적어도 `"   "`, 탭, 줄바꿈만 있는 값은 거부해야 한다.
2. 네 종류 sidecar에 대해 정상 문자열은 rc0, 각 필수 축의 공백뿐인 값은 rc2임을 대조한다. 오류가 해당 env 축 때문임을 확인한다.
3. 기존 누락·null·빈 문자열 거부와 정상 candidate 대 legacy baseline의 rc4를 유지한다.

**이 조건에 과학 재계산이나 기존 산출·옛 sidecar 수정은 필요 없다.** 승인 범위를 새 계약 항목으로 확대하는 요구도 아니다.

## 실행 결과

선택 pytest: **274 passed, 10 deselected in 296.40s (0:04:56), rc0**. 새 `test_h01` 3개·`test_h02` 4개를 모두 포함한다. 이전 검토와 같은 동적 우회 관련 시험 10개를 제외했으므로 사용자 측 **284 전수 통과를 이 기계에서 재확인한 것은 아니다**. 일반 회귀에서 실패한 항목은 없다. Octave 및 과거 동적 재생은 이번에도 실행하지 않았다. 구체적 선택식은 동봉 재현 안내에 기록했다.

| CLI | 실제 결과 |
|---|---|
| 현행 `out --schema-only` | rc0, 새 13개. baseline_absent1 외 blocker0 |
| legacy archive `--schema-only` | rc2, schema40 / provenance_cols25 / content6 / provenance1 |
| 현행 대 legacy archive | rc4, numbers0, inputs_uncomparable17 / env_uncomparable1 |
| 현행 대 현재 HEAD | rc2, alias13, numbers0 |
| 현행 대 full 승격 직전 commit | rc4, numbers0, inputs_uncomparable17 / env_uncomparable1 |

CLI 결과는 셸 바깥의 일반 실패값이 아니라 실제 자식 returncode를 저장했다. 기존 R14 검토 스크립트의 정상 경로·부분 env 대조도 새 커밋에 그대로 실행했다.

보관 확인:

- `out/` tree: 이전과 현재 모두 `1da2e9f5600dc5f91dd0a989188ef7b0ecb19437`.
- 새 payload13 + sidecar13 + legacy26 = **52개 파일**, 모두 이전 `1bb45b3` Git blob과 바이트 동일.
- 요청문: 15,827 bytes, SHA `17995cfd90cd838c1cc1a1df43b6cceecf59ecc615878a75c491e7fea04f9f77`. 당시 별도 첨부였으며 이번 저장소의 보존본과 일치.
- 이전 리뷰 ZIP: 38,222 bytes, SHA `72f9556e2230e7c3638303176b9bf6b9a7364f27c8273427f5a628c7450114bd`. 23 payload 및 추출본 일치, CRC 정상.
- 문서의 `df6413d(full) → 1bb45b3(full)` `.py/.sh` diff는 0개, 옛 `ef8e8f6 → 1bb45b3` 범위는 17개.

`legacy_transition_approved`와 기록용 CLI 인자 필수화는 앞선 §7 권고·다음 설계 항목이다. 이번 세 종결 조건을 확대해 그 미구현을 새 차단 사유로 세지 않는다. 전체 하네스의 다른 기신고 미결도 별도로 유지한다.

**최종 범위 판정: R14 완전 종결은 NO-GO, P2-1/P2-3은 수용, P2-2 공백값 검사만 보완. 실제 U18b 이관 수용·재계산 불필요는 유지.**
