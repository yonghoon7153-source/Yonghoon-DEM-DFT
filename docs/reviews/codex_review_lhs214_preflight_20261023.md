# LHS214 다시 발사 묶음 — 독립 사전 검토 (2026-10-23)

**작업 세션의 사전 검토다. 외부 반박 세션의 GO 또는 실제 발사 승인을 대신하지 않는다.** 검토자는 이 구현을 작성하지 않았다.

- 검토 소스: `7799a2ff64ba462b42ce05edd3e63b7c2854d557`의 LHS214 관련 파일.
- 대조 핀: `34713ac9650ece7c8d59b7c4d9a2aefccee693ea`.
- S0b 코드: `fe23f2b839f0a49adb077348fec6d4c85443b62a`; 비준: `f82929b0644be39b44e9fba9ea04cf9d60de9146`.
- 대상: [다섯 단계 묶음](lhs214_relaunch_package_20261020.md), [확인 요청서 초안 2](codex_lhs214_relaunch_check_request_20261020.md), S0b 수정과 두 등록의 재결합.
- 증거: [재생 안내와 파일 구성](lhs214_preflight_review_evidence_20261023/README.md). 관련 소스 40파일의 해시는 같은 폴더의 `SOURCE_SHA256SUMS`와 `source_manifest.json`에 있다.

## 1. 이번에 확인한 것 / 확인하지 않은 것

S0b 수정은 독립 재현에서 타당했다. 정상 비준 문서의 실패가 해소되고, 새 S11g는 네 가드 제거를 모두 검출했다. 두 등록의 비준 내용·봉인·입력 재결합은 요청서의 값과 일치했다.

새 P3 형식 결함 한 건을 제안한다: 사전 점검 영수증의 `git.sha`가 정상 40자리 뒤에 LF를 붙여도 P7·P10을 통과한다 (§3). **다른 승인 커밋을 허용한 반례는 아니다.** 수정은 하지 않았다.

`SUPR-03`의 원장 상태를 직접 바꾸지 않았다. 이 사전 검토만으로 verified로 올리지 않는다. `L214R-S03`·`L214R-S05`, S3, v1.3 배포도 범위 밖이다. 실제 WSL 증거·B7 핀 선택·외부 반박·발사 승인은 남아 있다. **작성 시점에 전체 저장소 게이트는 메인 작업에서 대기 중이며, 이 문서는 전체 게이트 통과를 주장하지 않는다.**

## 2. 독립 실측

환경: Linux x86_64, Python 3.11.17, NumPy 2.4.6, SciPy 1.17.1, networkx 3.6.1. BLAS 스레드 수는 1이다. WSL 실측이 아니다. 반입판의 아래 증거 경로는 저장소 루트 기준이다. 경로 정정 전 원문과 당시 manifest 문맥은 증거 폴더의 import-paths/original-package-docs.zip에 보존했다.

| 확인 | 결과 | 증거 |
|---|---|---|
| 봉인·도구 | `CODE_FILES` 32/32, 인계 2 + 빌더·실행기·스모크 = 대조 핀 바이트 | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/scope.json` |
| S0b 수정 범위 | 최상위 AST 59개 중 `_selftest` 하나만 변경. 현재 영수증 도구 = 코드 커밋 바이트 | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/scope.json` |
| 비준 diff | 묶음 diff에 날짜 자리 8개·7개만 채워 사본에 적용한 결과 = 비준 커밋 바이트. 현재 두 등록은 그 뒤 대화 원문을 채운 한 줄씩만 다름 | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/ratification-replay.json`, `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/scope.json` |
| 활성 봉인 | 두 등록 §3 = `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb`, 대기 None. 역사 표 + 활성 수정 네 행이 현재 32개 해시와 일치 | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/measurements.json` |
| 인계·빌더 지문 | 세 파일의 전체 SHA-256 = 194 §3 활성 줄 | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/handover-builder-equality.json` |
| 세대·의존성 | g2, 계약 문제 0, 모드 hertz·physics·hertz_h12. 정적 닫힘 30 ⊆ 32. 지연 import 92, 분류 밖·stale·fork 각각 0 | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/measurements.json` |
| 입력 재결합 | production194의 n 194 및 lhs/lhsx·ID·raw 표 지문, supp20의 n 20 및 lhss·ID·raw 표 지문이 묶음의 전체 값과 일치. 결손 raw SHA = [] | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/measurements.json` |
| 컨테이너 영수증 | rc 0, 11칸 전부 통과. 수동 칸 세 개는 모두 `verified_by_tool=false` | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/container_receipt.json` |
| 원본 현재 자체시험 | **123/123 PASS** | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/receipt-selftest.log` |
| 수정 전 도구 + 현재 비준 문서 | **121/122·rc 1**, S0b만 실패. 이전 Git blob을 메모리에서 실행 | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/old_receipt_current_documents.json`, `.log` |
| 독립 진리표 | 등록·대기 값에 None·현재·다른 지문·마지막 hex만 다른 지문을 조합하고 194 파서 오류 유무까지 **512가지**, 독립 기대와 불일치 0 | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/s0b_truth_table.json` |
| 실제 문서 반례 | 마지막 hex 변경은 D1, 63자리·대문자 hex·유니코드 숫자·중간 공백·NaN·Infinity는 R0+D1. 일곱 경우 모두 rc 1 | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/document_counterexamples.json` |
| 네 가드 변이 | 남은 대기·두 등록 일치·194 파서 오류·undeclared 거부를 각각 끄면 **네 경우 모두 122/123·rc 1**, 실패는 S11g 하나씩 | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/mutations.json` 및 네 변이 로그 |
| 검토 무결성 | 검토한 40파일은 리뷰 시작·끝 바이트 동일 | `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/final-integrity.json` |

512개 조합과 일곱 문서 반례는 지문 상태·문법 검사 범위다. 수치 솔버 전체의 비유한 값·넘침 안전성을 인증한 수가 아니다. 기존 제출 로그의 시험 수를 이번 실행 수에 합산하지 않았다.

S0b는 등록 상태에서 체크아웃 지문 64자리 전체를 요구한다. 두 문서가 함께 엉뚱한 활성 지문으로 바뀌어도 현재 지문과 다르면 undeclared로 거부한다. 대기 상태를 자체시험에서 허용하는 것과 발사 영수증 D1 통과는 별개이며, 실제 영수증은 계속 활성 등록 지문만 허용한다.

## 3. 새 P3 제안 — SHA 끝 LF를 허용하는 사전 점검 영수증

임시 ID: `LHS214-PRE-01`. 공유 원장에 직접 추가하지 않았으며 등록 제안은 별도 새 쪽지에 있다.

위치: `scripts/run_network_194_parallel.py:792`의 `_HEX40`, 같은 파일 `:2049`의 P7, `:2082`의 P10.

P7은 `git.sha`를 **40 hex**로 선언한다. 하지만 Python 정규식의 `$`는 마지막 LF 직전에도 일치한다. `^[0-9a-f]{40}$`의 `.match()`가 길이 41인 `"<40 hex>\n"`을 허용하며, 승인 핀의 접두 대조도 이를 차단하지 않는다.

자체시험이 생성한 정상 supp20 사전 점검 JSON·로그를 실제 생산 검사기로 확인했다. JSON의 `git.sha` 하나만 바꾸고 `approved_sha`에는 원래 40자리 전체를 주었다. 로그·로그 해시·생산 소스는 바꾸지 않았고, 각 실행 뒤 임시 원본을 복원했다.

| JSON `git.sha` | 독립 리뷰 에이전트 | 주 작업자 별도 재현 |
|---|---|---|
| 정상 40자리 | P0–P10 통과 | 같음 |
| 정상 40자리 + LF | **P0–P10 통과** | 같음 |
| 정상 40자리 + CRLF | P7·P10 실패 | 같음 |
| 정상 40자리 + space | P7·P10 실패 | 같음 |
| 정상 40자리 + NUL | P7·P10 실패 | 같음 |
| 마지막 hex 한 자리 변경 | P10 실패 | 같음 |

리뷰 에이전트의 증거는 `docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/pin-probe.json`, 주 작업자의 별도 출력 폴더 재현은 `docs/reviews/lhs214_preflight_review_evidence_20261023/root_reproduction/pin-probe.json`과 `summary.json`이다. 두 실행 모두 프로브를 포함한 원본 자체시험의 마지막 줄이 **123/123 PASS**였다. 같은 로컬 Linux 체크아웃의 별도 실행이며, 서로 다른 기계·WSL 또는 외부 반박 세션의 결과로 부르지 않는다.

**영향 한정:** 원래 40개 hex는 승인 핀과 같고, 마지막 hex를 바꾸면 P10이 거부한다. 다른 승인 커밋을 허용한 반례가 아니다. 정상 생산기가 이 LF 꼬리를 기록한다는 증거도 없다. 실제 발사 manifest의 F7·G7은 `re.fullmatch`를 쓰므로 같은 허점을 일반화하지 않는다. 수치·봉인·입력 변경 증거가 아닌 JSON 형식 경계의 P3 제안이다.

**수정 제안:** 검사 전에 `strip()`으로 원문을 고치지 말고 `re.fullmatch(r'[0-9a-f]{40}', gsha)` 또는 동등한 전체 문자열 검사로 거부한다. 위 여섯 대조를 먼저 시험에 추가한다. 공용 `_HEX40` 상수를 바꾸면 `launch_eligibility` 등 모든 사용처의 회귀 범위를 확인해야 한다. 이 검토 묶음은 코드 수정·봉인 갱신을 포함하지 않는다.

## 4. 요청서 Q1–Q6에 대한 답

| 질문 | 이번 사전 검토 |
|---|---|
| Q1 비준 문안 | 활성 §3 변경·역사·결과 열람 뒤 변경 이력 확인. 대기 선언의 자동 승인 승격 없음. 비준 diff 재생 일치 |
| Q2 재결합 | 코드·입력·인계·빌더·세대·의존성의 현재 컨테이너 재계산 일치 |
| Q3 B7 정의·대조 | 핀 정의와 대조 자리 연결 확인. 정확히 40자리라는 보장에는 §3의 P3 제안. 다른 승인 핀 우회 증거 없음 |
| Q4 실제 WSL 사전 점검 | **미검토: 자료 미반입** |
| Q5 S0b 약화 여부 | 이번 범위에서 약화 반례 없음. 정상 비준 통과·이전 실패 재현·독립 진리표·네 변이가 새 기대를 지지 |
| Q6 새 결함 | §3의 P3 한 건 제안. 외부 반박 세션 판정이나 원장 종결을 대신하지 않음 |

## 5. 실제 발사 전에 남는 증거

요청서 빈칸을 컨테이너 결과로 채우지 않았다. 1저자 측에서 다음이 필요하다.

1. 선택한 B7 승인 핀 40자리와 그 핀으로 detached한 깨끗한 작업 트리.
2. 보통·`-I` 실행의 Python·NumPy·SciPy·networkx·실행 파일 출력.
3. 같은 핀의 fast16·real4·reread·runner·receipt 자체시험 전체 로그·종료 코드와 시험 뒤 dirty 0.
4. 새 ROOT 둘의 전체 사전 점검 로그·완료 영수증 및 승인 SHA를 넣은 검증 JSON. 194는 P0–P10, 보충은 P0–P10+E1+E2.
5. 194 등록 §2·§3 여섯 칸을 전체 값으로 대조한 표와 확인자. P0–P10 통과만으로 수동 대조를 대신하지 않는다.
6. 새 ROOT 두 이름이 서로 다르고 기존 실행 ROOT와 다르다는 기록, 반입 묶음 SHA-256과 반입 경로.
7. 증거를 채운 요청서의 외부 반박 판정 및 별도 1저자 발사 승인.

외부 WSL 접속, GPU·LIGGGHTS 실행, 실제 194·보충 20 발사를 하지 않았다. S3·v1.3 및 기존 open 두 건의 한정도 유지한다.
