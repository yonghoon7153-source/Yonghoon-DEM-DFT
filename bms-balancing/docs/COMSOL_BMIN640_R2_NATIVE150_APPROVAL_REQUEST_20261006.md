# B-min r2 native 150 s — 사용자 승인 요청 (1 단계: 범위 · 실행 주체 · 예산 · 중단 · 보존) · 2026-10-06 · 실행 0

> 이 문서는 **승인 요청**이다. 승인 전에는 실행 기계에서 approval / token / runtime / `future_authorizations/*` 파일을 만들지 않고, COMSOL 을 부르지 않는다.
> 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. 게이트 (`degradation-degeneracy/`) · REIL 과 무관 · RUN_SCOPE 0.

## §0 무엇이고 왜 지금인가

- **native 150 s** = 같은 provisional 모델을 **fresh t = 0 → 150 s 로 한 번** 푸는 계산. 바꾸는 것은 **입자 반경 메시 Nel 320 → 640 (두 전극)** 하나뿐이고, 그 결과를
  수용된 NORMAL480 (입자 320) 의 `run/tables` 와 **120 ≤ t ≤ 150 s 의 요청 301 시각 × 전극별 241 좌표**에서 비교한다 (사용자 결정 SPEC §42-1 · 범위
  `COMSOL_BMIN_SCOPE_v2_20261004.md` §1 · 검토자 §56-1 "최대 1 회 · 다시 별도 승인").
- 선행 조건: r2 고정 실행본의 변경부 한정 검증이 **종결**됐다 (보충 검토 `LIMITED_VALIDATION_CLOSED_WITH_DOCUMENTED_SCOPE` · SPEC §62 · `1a9566685`). 그
  회신의 다음 단계가 "같은 고정 실행본의 native 150 초 **별도 승인 요청문 준비** — 준비와 실제 계산은 구분" 이고, 사용자가 2026-10-06 "comsol도 승인 요청문
  준비 부탁해요" 로 요청했다 (SPEC §63).
- 이 문서가 묻는 것은 **1 단계 승인**이다: 범위 · 실행 주체 · 예산 · 중단 · 보존을 정하고, 실행 기계에서 **읽기 전용 사전 관측**을 해도 되는지. 실행 기계의 현재
  값 (prefs · 경로 · 기준 파일 · 디스크) 은 이 저장소에서 볼 수 없으므로, 그 관측을 붙인 **최종 승인 (2 단계)** 이 따로 있다 (이전 native 30–480 s 와 같은 2 단 —
  최종 요청문 · 승인 파일은 Windows 쪽에서 만들어졌다: NORMAL480 ZIP `preexec/FINAL_NATIVE480_APPROVAL_REQUEST.txt` 등).

## §1 한눈에 — 하는 것 / 하지 않는 것

| 하는 것 (2 단계 승인 뒤) | 하지 않는 것 |
|---|---|
| r2 고정 실행본 그대로 · fresh 0 → 150 s · compile ≤ 1 · batch ≤ 1 · solve ≤ 1 | 960 s 연장 · 자동 재시도 · 자동 연장 · 저장 MPH 에서 이어 풀기 · 새 control |
| 입자 Nel 320 → 640 (두 전극) 한 축 | 물리 메시 (300 = 120 / 60 / 120) · 전류 · σ · threshold · rtol · 다른 공간 축 · 유한 σ · 다른 solver 변경 |
| 120–150 s 의 세 필드 판정 (아래 §4) | 480 s 전체 · 전체 / 공간 수렴 · 실험 타당성 주장 · 정상 gate PASS |
| 정책 무변경 경로 (기본 prefs 의 바이트 복사 · 실효 정책 `UNVERIFIED` 명시 수용) | 정책 · 권한 · "All files" 토글 · shell fallback · 생산 코드 변경 · 봉인 파일 수정 |
| 결과 보존 · 수신 검토 | 기존 전체 시험 · NORMAL480 · rtol30 · 한정 검증 반복 |

## §2 고정 입력 (①)

| 항목 | 값 |
|---|---|
| 실행본 | 이 저장소 `bms-balancing/comsol_candidates/bmin_particle640_r2_20261005/candidate/` — 커밋 `939b544b8bb77dbf20a56520af9f74a82acd0a94` 이후 변경 0 (2026-10-06 실측) |
| CODE_MANIFEST | **`4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25`** (1,050 B · 이전 `9dcb47f0…`) |
| 봉인 5 파일 | `src/Bmin640Candidate.java` 80,813 B `ef0ca60a…62ff` · `src/diagnostic_consumer.py` 26,394 B `c3c8feb3…c812` · `src/candidate_entry.py` 13,995 B `0a0d3081…8fed` · `PARENT_COMMAND.ps1` 24,469 B `fda741a1…e783` · `CONTRACT.json` 55,211 B `98820a84…ce42` |
| 봉인 밖 | `COMMAND_MAP.json` 6,189 B `a8bda4e6…2394` · `NATIVE_APPROVAL_FIELD_SPEC.json` 4,346 B `61aa028f…0f7b` |
| run_id · root | `bmin_particle640_candidate_001` · `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/bmin_particle640_offline_preparation_20261004/` — 위 `candidate/` 바이트를 **그 root 에 그대로** 둔다 (v1 · r1 꾸러미 아님 · 전달 ZIP 사본에서 실행하지 않음 · 경로 변경 · 봉인 코드 수정 금지) |
| 검증 근거 | retry3 결과 ZIP `ed0138b9…b470` (1,619,237 B · manifest `97f51112…`) · 집계 정정표 `16876bb0…4414` · PS01-16 범위 정리 (§61) · 두 수신 검토 ZIP (`cf0f2051…` · `105c84ae…`) · 보충 검토 대상 커밋 `10525ae1e` |
| 기준 NORMAL480 | 결과 ZIP `e991ab4c…cbc30` (420,748,594 B) · CODE_MANIFEST `7a5cc2f1…` · CONTRACT `58d398a6…` · 비교에 쓰는 **`run/tables` 9 파일** (CONTRACT l.119–165 의 크기 · SHA — 예: `axes_profile_N.csv` 203,575,457 B `acdb34de…`) · 실행 기계 경로 `…/outputs/normal480_offline_preparation_20261001/future_run_001/tables/` · ZIP 의 `baseline/` (더 짧은 과거 기준) 으로 대체하지 않는다 |

## §3 명령 · 경로 · 시작 (② · ③)

| 단계 | argv · cwd (`COMMAND_MAP.json` 그대로) |
|---|---|
| 부모 | `C:/WINDOWS/System32/WindowsPowerShell/v1.0/powershell.exe -NoLogo -NoProfile -NoExit -File <root>/PARENT_COMMAND.ps1 -ManifestSha 4cdca2e6…cf25` · cwd `…/outputs/b020_profile_unit_stages_20260927/src` · **사용자가 보이는 PowerShell 5.1 창**에서 실행 · challenge 두 개를 **사용자가 직접 입력** (AI 대리 입력 없음 · 별도 C2 check-only 없음) |
| execute / analyze | `…/codex-primary-runtime/dependencies/python/python.exe -I -S -B -X utf8 <root>/src/candidate_entry.py {execute\|analyze} --approval <root>/future_authorizations/bmin640_001.json --manifest-sha 4cdca2e6…` (python.exe 107,312 B `b7a12c3a…`) |
| compile · batch | `C:/Program Files/COMSOL/COMSOL63/Multiphysics/bin/win64/comsolcompile.exe` (962,024 B `a44b59db…`) · `comsolbatch.exe … -np 16 … -outputfile <run>/result.mph -batchlog <run>/batch.log` (962,024 B `f4e74547…`) · cwd `<run>` = `<root>/future_run_001` · 전용 `-prefsdir` = 승인된 기본 prefs 의 바이트 복사 |
| 지금 없어야 할 경로 | `future_run_001` · `future_parent_001` · `future_authorizations/{bmin640_001.json, VALIDATION_RELEASE.json, USER_DECISION.json}` — 하나라도 있으면 **삭제 · 재사용 · 새 이름 우회 없이 중지** |
| 시작 경로 위험 | PS 5.1 NoProfile 의 모듈 자동 로딩은 이 부모 (r2) 에서 미관측 — 첫 `BHash` 오류 = compile / batch 이전 중지 · 재시도 0 |

## §4 물리 · 판정 (⑤) — 바꾸지 않음

- 물리 300 (120 / 60 / 120) · 0.1C 정전류 충전 · σ 1e−20 · threshold 0 · rtol 1e−6 · 초기 step 1e−5 · strict / all stored · 요청 1,637 시각 (NORMAL480 목록의 앞
  1,637 개 · 끝 150 s) · 코어 설정 16.
- 판정 세 필드 (≤ 는 허용): max |ΔV| ≤ 0.001 V **그리고** 두 전극 max |Δx_surface| ≤ 1e−4 → `WITHIN_LIMITS_THIS_WINDOW` · 어느 하나라도 엄격히 크면
  `EXCEEDS_LIMITS` · 부모 성공 상태 `AWAITING_BMIN640_150S_EXTERNAL_ACCEPTANCE`. 비교 · 분석 · 전달 실패에도 `native_completion` 은 남는다.
- **의미 한정:** `WITHIN_LIMITS_THIS_WINDOW` = "이 입력 · 입자 축 · 120–150 s · 선언 표본에서 320 ↔ 640 관측 차이가 한도 안" 까지 — 오차 상한 · 수렴 차수 ·
  참값 정확도 · 물리 축 · 480 s 후반 · 유한 σ 를 주장하지 않는다. 한도 초과를 solver 실패로 바꾸지 않고, rc 0 이나 ZIP 만으로 비교 PASS 가 되지 않는다.

## §5 정책 · 승인 파일 (④)

- 정책 무변경 · 실효 정책 `UNVERIFIED` — 승인 파일의 `effective_policy_unverified_accepted: true` 는 **사용자의 명시 수용**이 필요하다 (아래 §9 문구에 포함).
- 기본 prefs `C:/Users/BML/.comsol/v63/comsol.prefs` 의 **현재** 크기 · SHA · `security.external.enable=on` 은 2 단계 사전 관측으로만 정한다 (과거 1198 시점
  22,252 B `064d1900…` 은 현재 값이 아니다 — 추정해 적지 않는다).
- 승인 파일 순서 (1198 관례): 사용자 결정 원문 (USER_DECISION — 사용자가 2 단계에서 쓴 승인 문장 그대로) → 원문 파일 식별 → 현재 증거 목록과
  VALIDATION_RELEASE (`changed_branch_validation PASS` 는 수용된 실제 검증 결과로만 · `manifest_bytes_unchanged_since_validation true` · evidence = §2 검증 근거)
  → release 바이트 식별을 승인 파일에 연결 → 부모 / entry 의 기존 검사. 승인 파일을 미리 만들거나 시험 fixture 승인을 재사용하지 않는다.

## §6 자원 · 예산 (⑥) — 제안값 그대로 · 상한

| 항목 | 상한 (CONTRACT `budgets_seconds` · 사용자 승인 대상) |
|---|---:|
| 사전 · 입력 | 180 s |
| compile + batch | 9,000 s (높은 비용 가정 ≈ 5,916 s 의 ≈ 1.5 배 · NORMAL480 실측 compile+batch 6,500 s 는 480 s 계산) |
| 소유 프로세스 정리 | 120 s |
| 분석 | 900 s |
| 전달 | 300 s |
| **전체** | **10,500 s** (초과 → INCOMPLETE · `evidence_validity` INVALID · `mesh_comparison` INCONCLUSIVE · 미사용분 전용 없음) |
| 코어 · 디스크 · RAM | 16 코어 요청 (실제 이용률 UNVERIFIED) · 시작 디스크 ≥ 15 GiB · RAM 은 시작 때 관측만 (새 하한 · working-set 감시 없음 — 미구현) |
| 시도 | **1 회.** 실패하면 보존하고 멈춘다 — 다시 하려면 새 승인 |

실제 150 s 비용 · peak RAM 은 모른다 (계획 ≈ 3,824–5,916 s · MPH ≈ 6.1–7.2 GB · 메모리 ≈ 2.5 GB 는 추정).

### 6-1. 예산 경계 — 부모 기록까지 · 포장은 별도 (2026-10-06 Codex 질문에 답해 덧붙임)

- **위 표의 시계는 부모 `PARENT_COMMAND.ps1` 의 `$bClock` 하나**다 — 부모 시작 (207 행 `PARENT_START`) 부터 **POST_WRITE 콘솔 줄** (239–246 행) 까지. `delivery`
  300 s 는 분석 반환 뒤 (216 행 `$bDeliveryStart`) 부터 POST_WRITE 까지 — 판정 계산 · `PARENT_LOCAL_DECISION.json` · `FINAL_BOUNDARY.json` 쓰기 / 다시 읽기 · 최종 줄
  출력이다. `overall` 10,500 s 도 POST_WRITE 에서 끝난다 (222 · 234 · 241 행). 봉인 코드는 고치지 않는다.
- **결과 수집 · ZIP 포장 · 다시 읽기 대조 (Codex 몫) 는 이 두 예산 밖**의 별도 단계다. 제안 규칙:
  - 시작은 사용자가 부모 프롬프트 복귀를 관측한 **뒤** · 시작 / 끝 시각과 소요를 포장 기록에 따로 적는다 (부모 예산 · 판정 필드에 더하지 않는다).
  - 상한 1,800 s (제안 · 사용자 승인 대상) · 한 번 · 넘거나 실패하면 원 산출을 그대로 두고 멈춘다 — COMSOL 재실행 · 부모 재실행 · 원 파일 수정 · 재포장으로 덮기 없음.
  - 읽기 전용 복사만 · 결과 MPH 는 넣지 않고 식별만 (§8) · 포장 실패 · 초과는 native 결과나 세 필드를 바꾸지 않는다 (포장 기록에 따로 적는다).

## §7 중단 조건 (첫 오류에서 보존하고 멈춘다)

entry / 부모의 기존 거부를 그대로 쓴다: `EXISTING_RUN_NO_RETRY` · `CWD` · `START_OPTIONS` · `PYTHON_IDENTITY` · `MANIFEST_IDENTITY` · `BASELINE_IDENTITY` (기준 9
파일 · compile 전) · `DISK_START` · `OTHER_NATIVE_BATCH_PRESENT` · `PREFS_PATH` · `DEFAULT_PREFS_CHANGED` · `PRIVATE_POLICY_CHANGED` · `ATTEMPT_DUPLICATE` · 승인 /
release 비활성 · 예산 초과 · 첫 `BHash` 오류 · `NATIVE_FATAL_RC0` 로그 패턴. 다른 프로세스 종료 · 자동 재시도 · 다른 shell / 권한 / 정책 fallback 은 없다 (정리는
소유 Job 만).

## §8 결과 수집 · 보존 (⑦)

- 최종 값 = 부모 PRE_WRITE + **POST_WRITE 콘솔 줄** (`USER_PARENT_FINAL_RETURN` 의 `fields`) · 자식 rc · 사용자 프롬프트 복귀. NoExit 의 OS rc = null —
  프롬프트 복귀는 OS 종료 코드가 아니고, 보호 중단 · 오류는 정상 완료가 아니다.
- 결과 ZIP + PACKAGE_MANIFEST · 선택 보존 before / after 목록 · 사전 관측 원문 (`preexec/`) · 승인 파일 원문 (`authorization/`) — 이전 NORMAL480 형식.
- **결과 MPH (≈ 6–7 GB):** ZIP 에 넣지 않고 크기 · SHA 식별만 보내며, 실행 기계에서 **수신 검토가 끝날 때까지 지우지 않는다** (제안 — §9 결정 4).
- 원 실패 · pending · 원복 · recipient=null · 정상 gate / overall `INCOMPLETE` · 실효 정책 `UNVERIFIED` · 실제 코어 UNVERIFIED 는 그대로 남긴다.
- 이 저장소 쪽: 받은 바이트 그대로 보존 (`.gitattributes -text` 먼저) → SPEC 새 절 접수.

## §9 사용자가 정할 것 (1 단계)

| # | 결정 | 제안 |
|---|---|---|
| 1 | 실행 주체 | **이전 native 와 같은 분담** — Windows 쪽 Codex 가 읽기 전용 사전 관측 · 최종 승인 요청문 (2 단계) · 승인 뒤 승인 파일 생성 · 결과 포장을 맡고, **사용자가** 보이는 PS 5.1 창에서 부모를 실행하고 challenge 를 직접 입력한다 |
| 2 | 사전 관측 범위 (읽기 전용 · 실행 기계) | r2 바이트가 root 에 놓였는지 (v1 · r1 바이트와의 충돌 포함) · 지금 없어야 할 경로 5 개의 부재 · NORMAL480 `run/tables` 9 파일의 현재 크기 · SHA · 기본 prefs 크기 · SHA · security 값 · 외부 의존 16 개 · COMSOL exe 둘 · python.exe 의 현재 해시 · 디스크 · RAM · 다른 COMSOL 프로세스 부재. **쓰기 · 이동 · 복사 · 설정 변경 0** (r2 바이트를 root 에 두는 일이 필요하면 그것도 2 단계 승인 항목으로 따로 적는다) |
| 3 | 예산 | §6 의 10,500 s 그대로 (연장 없음 · 부모 POST_WRITE 까지) · 포장 단계는 별도 상한 1,800 s (§6-1) |
| 4 | MPH 보존 | 식별만 전달 · 수신 검토 끝까지 실행 기계에 유지 |
| 5 | 실효 정책 | `UNVERIFIED` 를 명시 수용 (이전 native 와 같음) |

**채택 문구 (이대로 또는 고쳐서):**

> B-min r2 native 150 s 의 1 단계를 이 문서 (`bms-balancing/docs/COMSOL_BMIN640_R2_NATIVE150_APPROVAL_REQUEST_20261006.md`) 의 범위로 승인합니다. Codex 는
> 실행 기계에서 §9-2 의 읽기 전용 사전 관측만 하고, 그 결과를 붙인 최종 승인 요청문을 만들어 주세요. approval / token / runtime · `future_authorizations/*` 생성과
> COMSOL 실행은 최종 승인 뒤에만 합니다. 예산은 §6 그대로 (전체 10,500 s · 연장 없음 · 1 회), 실효 정책 UNVERIFIED 를 수용하고, 결과 MPH 는 식별만 보내고 수신
> 검토가 끝날 때까지 지우지 않습니다.

## §10 승인 뒤 순서

1 단계 승인 기록 (SPEC 새 절) → Codex 에 사전 관측 요청 (발송문 · 고정 커밋) → 사전 관측 원문 + 최종 승인 요청문 (2 단계) 수신 · 보존 → 사용자 최종 승인 (원문 =
USER_DECISION) → Codex 가 승인 파일 생성 → 사용자가 부모 실행 · challenge 입력 → 결과 포장 → 수신 검토 · 접수. 어느 단계든 §7 조건이면 그 자리에서 멈춘다.
