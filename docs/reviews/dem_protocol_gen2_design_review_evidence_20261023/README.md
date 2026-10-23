# DEM 프로토콜 세대 2 설계 요청서 — 사전 검산·독립 리뷰 반입 (2026-10-23)

최종 통합 상태는 [전체 게이트 영수증](full_gate_receipt.json)과 `final-gate/` 로그가 정본이다. 아래 및 원 검토문·쪽지의 작성 당시 대기 표현은 이력으로 보존한다. 깨끗한 후보 커밋에서 축소 없는 전체 게이트를 실행했고, 이후 커밋은 이 영수증·로그와 새 상태 쪽지만 기록한다. 외부 GO·비준·발송·실제 기계 실행 상태는 승격하지 않는다.

요청서: `docs/reviews/codex_dem_protocol_gen2_design_request_20261023.md`.

독립 재확인 `independent/RECHECK-v2.md`는 **G2IR-01(P2)·G2IR-02(P3)의 문서 범위 해소와 v1→v2 변경의 새 회귀 finding 없음**을 판정했다. 요청서 반입·최종 묶음 준비가 가능한 상태다. 외부 발송·등록·실제 실행·물리 검증 GO는 아니다. 언로딩 키트 외부 GO와 T12 적용 핀, 최종 리뷰 핀·ZIP은 대기다. 필수 전체 게이트의 최신 상태는 `full_gate_receipt.json`을 참조한다. Q7–Q9 실측 자료도 미확인이다.

## 1. 원본과 반입판

| 자료 | 보존·범위 |
|---|---|
| `author/` | 반입 전 작성자 자료 16개의 원 바이트는 원본 ZIP에 보존. 현재 live 초안 두 개는 경로만 정규화했고 두 manifest는 live 반입 지문이다. 최초 v1·수정 v2, 작성자 산술 탐침·결과, G2IR 대응표·diff, 두 원 manifest는 원본 ZIP에서 확인한다. 그 안의 ‘재확인 대기’는 당시 기록이며 고치지 않음 |
| `independent/` | 독립 리뷰 자료 9개를 바이트 그대로 복사. 최초 REVIEW·프로브 2개·결과 2개·manifest, RECHECK-v2·재확인 증거·재확인 manifest |
| `request-v2-to-import.diff` | 독립 검토 v2→저장소 요청서의 차이. 재확인 상태·경로·기준 스냅숏 검증 범위를 정리. 새 물리 결정·문턱 비준 없음 |
| `import-provenance.json` | 원본 파일별 sha256, 반입 요청서의 경로·sha256, 읽은 소스 핀 |
| `tools/` | 장소에 의존하지 않는 재현 도구. 원 독립 probe와 분리한 portable adapter의 diff를 포함 |
| `package-audit/` | 최종 문서 패키지 독립 감사 원문·감사 입력 요청서·replay JSON 요약을 보존. 감사 뒤 chunk 표기 및 gate receipt 참조의 변경은 별도 diff |
| `full_gate_receipt.json` | 최종 반영판 필수 게이트의 상태·명령별 rc·대상 신원·로그를 메인 작업자가 기록하는 영수증. PENDING은 통과가 아님 |
| `portable-replay/` | 기준 핀 blob에서 재현한 명령 결과. 네 프로브 rc 0, 비교 항목 7개 동일. 실제 캠페인·전체 게이트 결과가 아님 |

검토 입력 SHA256:

- v1: `0e9b62b26ac73ac0173e73c4d3ceff0a8f8e57a76d2a0dd9d866ebcb2c458d61`.
- v2: `4ee2d07ccd392c9233d57262d2511ae0d32bfac52a95a9808593e97cf26929a2`.
- v1→v2 diff: `47a0d33d159c3134d96c56dd2ce3c83a8ac5e66b8ce521644a008986b1adbded`.

## 2. 22개·32개 대조가 말하는 것

최초 작성자·독립 검산은 **기준 `7799a2ff64ba462b42ce05edd3e63b7c2854d557`**의 자료 22개와 봉인 `CODE_FILES` 32개를 확인했다. 자료 22개에는 당시의 언로딩 등록·README가 들어 있다. 이후 ULPR 수정판이나 다른 트랙 최종판도 그 바이트와 같다는 주장이 아니다. 원 manifest의 신원 기준을 바꾸거나 과거 결과를 새 판 검사로 승격하지 않는다.

문헌 대조는 계획서 §10의 카드 45개에 대해 `9dc235c38f6347c1d94febc598b1d93ee2ffef68`과 `aaa275e2081ce43a6892c7dde40ea4d8f82576de`의 blob을 비교한 것이다. 44개 동일, Sakuda 카드 1개는 원문 대조 정정 추가. PDF/SI 45편을 새로 읽은 전수 검증이 아니다.

## 3. 작은 반례의 판정 범위

작성자 A1–A5를 독립 리뷰가 별도 식으로 확인했다. 회복→공극 산술, 측정오차가 걸친 밀도 경계, MC 1σ 조건, E 사다리 설명, 이산 제어 강성 경계는 **설계의 검토 후보**다. 원계획서·등록 문턱을 이 묶음에서 고치지 않았다.

- MC 예시의 status OK 8개 중 1σ 밖 3개는 의도한 합성 반례다. 이를 기능검사 ‘8/8 통과’나 실패율의 추정치로 부르지 않는다.
- 독립 산술·신원 probe의 16/16 assert는 해당 검사 수다. T0–T14·실제 언로딩·DEM 캠페인의 통과 수가 아니다.
- G2IR-01·02 해소는 요청서 요약 계약과 발송 조건의 문서 판정이다. 아직 없는 덱·입력 manifest·실험 판정기가 조건을 강제한다는 증거가 아니다.
- 기준 원장에서 MV-01–09·DEMP-01/02는 11개 모두 open이다. 이번 반입은 원장 상태를 바꾸지 않는다.

## 4. 재현 — 현재 작업트리를 바꾸지 않는다

Python 3.11 환경과 NumPy·NetworkX가 필요하다. Git 저장소에 위 소스 핀과 두 문헌 핀의 객체가 있어야 한다. 원 리뷰의 절대 scratch 경로는 당시 기록이며, 아래 도구는 그 경로를 사용하지 않는다.

원 재현 도구는 검토 당시 초안의 request SHA를 원 독립 결과와 대조한다. 따라서 경로 정규화된 live 초안이 아니라 원본 ZIP에서 함께 복원한 원 도구·초안·독립 결과를 사용한다. Git 객체 저장소는 현재 저장소를 읽되 실제 복원 소스는 원 source manifest의 고정 핀이다. 정규화본의 신원은 별도 import provenance로 확인한다. 이 방법의 실제 재확인은 `import-paths/original-input-replay/receipt.json` 및 로그에 기록했다.

저장소 루트에서 **아직 없는 출력 디렉터리**를 골라 실행한다:

```bash
# 활성화한 환경의 TMPDIR 아래 두 경로는 모두 아직 없어야 한다.
G2_ORIGINAL="$TMPDIR/dem-gen2-original-docs-new"
G2_REPLAY="$TMPDIR/dem-gen2-original-replay-new"
test -n "$TMPDIR" && test ! -e "$G2_ORIGINAL" && test ! -e "$G2_REPLAY" &&
python -I -B -m zipfile -e \
  docs/reviews/dem_protocol_gen2_design_review_evidence_20261023/import-paths/original-package-docs.zip \
  "$G2_ORIGINAL" &&
python -I -B "$G2_ORIGINAL/docs/reviews/dem_protocol_gen2_design_review_evidence_20261023/tools/replay_evidence.py" \
  --repo "$PWD" \
  --out "$G2_REPLAY"
```

도구는 `git show`로 기준 핀의 필요한 파일 55개(자료 22개 + 봉인 32개 + 그 목록을 정의한 실행기)를 출력 디렉터리에 복원한다. `.git`을 만들지 않으며 checkout·worktree·branch를 만들거나 변경하지 않는다. Git 객체 읽기와 임시 source snapshot을 분리한다. 이미 존재하는 출력 디렉터리는 거부한다.

`probe_independent_portable.py`는 원 독립 probe의 산술·검사를 유지하고 `--repo`(기준 파일 사본)와 `--git-repo`(읽을 객체 저장소)만 분리했다. 결과의 HEAD도 source pin과 object-store HEAD로 구분했다. 원본은 `independent/probe_independent.py`, 변경 목록은 `tools/portable-adapter.diff`에 있다. 이 adapter 재실행은 새 독립 리뷰가 아니다.

기록된 재현: Python 3.11.17, `-I -B`; 작성자 산술·기존 MV 산술·독립 산술 adapter·실제 MC 함수 probe 네 개 모두 rc 0. `portable-replay/replay-summary.json`의 JSON/검사/소스 해시/문헌/요청서 해시/MC 증거 비교 7개는 모두 true다. 환경 문자열과 객체 저장소의 현재 HEAD는 산술 결과 동등성 항목이 아니다. 재현 결과를 다시 낼 때도 실패를 덮어쓰지 않는다.

## 5. 남는 절차

- 적용 대상 가지: `codex/dem-gen2-request`. 예정 커밋: `<<sha:Prepare DEM generation 2>>`. 이 문서 작성 시 commit·push 완료를 주장하지 않는다.
- 최종 반영 후 문서 참조·원장 자기일관·`scripts/check_all.sh` **전체**가 필요하다. 최신 실행 상태·로그는 `full_gate_receipt.json`에 기록하며 PENDING 또는 증거 누락이면 미완료다. 위 국소 재현은 전체 게이트를 대체하지 않는다.
- 실제 최종 리뷰 핀·ZIP은 메인 작업자가 commit 뒤 핀 blob에서 구성한다. 이 폴더의 `MANIFEST.sha256`은 반입 증거 파일 목록이며 최종 발송 ZIP·`PIN.txt`의 대체물이 아니다.
- 언로딩 외부 GO·T12 적용 핀은 별도로 반입해야 한다. ULPR 내부 수정·시험이나 이 문서 재확인으로 대신하지 않는다.
- Q7–Q9 미확인 자료가 있는 조건부 설계 검토의 발송 여부는 1저자가 정한다. 이 조건부 범위도 언로딩 외부 GO·최종 핀/묶음·필수 게이트를 면제하지 않는다.
- shared ledger·CLAUDE·진행 기록은 직접 수정하지 않았다. 제안 문안은 새 Codex→Claude 쪽지에만 둔다.

## 경로 정규화 반입의 원본·현재 구분

현재 저장소 문서 참조 검사를 위해 누락 경로 토큰만 실제 저장소 상대 경로로 확장했다. 숫자·판정·설계·미비준·실행 한계는 바꾸지 않았다. 원문 안의 “그대로/변경하지 않음”과 입력 SHA·원 diff·검토 행 번호는 당시 검토판의 이력이다. 원 바이트는 `import-paths/original-package-docs.zip`에서 확인한다. 현재 파일과 혼동하지 않도록 각 원본/반입 SHA·토큰 치환·diff를 `import-paths/provenance.json`에 기록했다. 아래 live manifest만 경로 정규화본의 반입 manifest로 재계산했으며, 같은 이름의 원 manifest는 ZIP에 그대로 있다: `author/MANIFEST.sha256`, `author/MANIFEST.v2.sha256`. 원 source/literature 지문과 수치 JSON·로그·도구는 변경하지 않았다.
