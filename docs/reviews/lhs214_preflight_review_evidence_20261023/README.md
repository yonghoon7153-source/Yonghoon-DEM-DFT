# LHS214 독립 사전 검토 증거 — 2026-10-23

검토 범위와 판정은 [검토문](../codex_review_lhs214_preflight_20261023.md)에 있다.

## 구성과 provenance

- `reviewer/`: 구현에 참여하지 않은 리뷰 에이전트의 실측. JSON과 로그는 최초 결과를 그대로 복사했다.
- `root_reproduction/`: 주 작업자가 별도 출력 폴더에서 같은 핀 반례를 다시 실행한 결과. 리뷰 에이전트의 실행 횟수에 합산하지 않는다.
- `SOURCE_SHA256SUMS`, `source_manifest.json`: 검토 당시 저장소의 40개 관련 파일 해시. 경로 기준은 저장소 루트이며 검토 핀은 `7799a2ff64ba462b42ce05edd3e63b7c2854d557`이다.
- `tools/`: 재생 도구. 최초 클라우드 전용 기본 경로를 제거하고 번들 위치에서 저장소를 찾도록 바꿨다. `tool_packaging.json`은 격리 실행 보강 전 처음 세 도구의 포장 기록이다. 이후 두 도구의 Python 자식 실행에도 `-I`를 추가했다. 계산·검사 본문은 같다. 현재 해시는 `MANIFEST.sha256`, 격리 실행 보강 전후 해시는 `isolated_revalidation/tool_changes.json`에 있다.
- `isolated_revalidation/`: package audit 뒤 네 재생 도구를 `python -I`로 새 출력 폴더에서 다시 실행한 별도 결과. 이전 reviewer·root 결과와 구분하며, 이전 실행이 `-I`였다고 소급하지 않는다.
- `MANIFEST.sha256`: 이 증거 폴더 파일 해시. `MANIFEST.sha256` 자신은 제외한다.

원본·변이 Python 파일 사본, 임시 등록 문서, 임시 사전 점검 JSON·로그 픽스처는 중복 반입하지 않는다. 아래 도구가 실제 저장소와 Git blob에서 다시 만든다. 과거 결과 JSON에 남아 있는 절대 경로는 당시 관측 기록이며 재생 입력 경로가 아니다.

이 묶음에는 전체 저장소 게이트의 통과 기록이 없다. 작성 시점에 전체 게이트는 메인 작업에서 대기 중이다. WSL 사전 점검·발사 승인 증거도 아니다.

## 재생

대상 저장소 루트에서 그 저장소의 Python 환경을 활성화한 뒤 실행한다. 당시 의존성 판은 `reviewer/environment.json`에 있다. Git 비교에는 검토문에 적힌 과거 커밋 객체가 필요하다.

```bash
export REPO_ROOT="$(git rev-parse --show-toplevel)"
export EVIDENCE_OUT="$(mktemp -d -t lhs214-reproduction.XXXXXX)"
REVIEW_TOOLS="$REPO_ROOT/docs/reviews/lhs214_preflight_review_evidence_20261023/tools"
python -I "$REVIEW_TOOLS/audit.py"
python -I "$REVIEW_TOOLS/pin_probe.py"
python -I "$REVIEW_TOOLS/mutations.py"
python -I "$REVIEW_TOOLS/provenance_replay.py"
```

`REPO_ROOT`와 `EVIDENCE_OUT`을 명시하면 도구 위치와 작업 디렉터리를 바꿔도 재생할 수 있다. 생략 시 저장소 기본값은 이 번들의 위치에서 찾고, 출력 기본값은 현재 디렉터리 아래 `lhs214-reproduction`이다. 원래 증거를 덮어쓰지 않도록 새 출력 폴더를 권한다.

네 명령은 모두 격리 모드 `-I`로 실행한다. `mutations.py`와 `provenance_replay.py`가 새로 만드는 Python 자식도 `-I`를 사용한다. 필요한 저장소 모듈 경로는 도구가 명시적으로 추가하며, 계산 코드·판정식을 환경 경로로 바꾸지 않는다.

| 도구 | 출력·기대 |
|---|---|
| `audit.py` | Git/AST/지문/입력 재결합, S0b 독립 진리표 512가지 불일치 0, 실제 문서 반례 7가지 rc 1 |
| `pin_probe.py` | 정상과 LF 꼬리는 P0–P10 통과, CRLF·space·NUL은 P7/P10 실패, 다른 마지막 hex는 P10 실패. 원본 자체시험 123/123 |
| `mutations.py` | 네 가드 변이를 메모리 모듈로 실행. 각 변이는 122/123·rc 1, S11g 하나만 실패해야 도구가 rc 0 |
| `provenance_replay.py` | 비준 diff를 새 사본에 재생해 날짜 자리 8·7개와 비준 커밋 바이트 일치. 수정 전 도구는 현재 비준 문서에서 121/122·rc 1, S0b만 실패 |

도구 rc 0과 고의 변이·수정 전 도구의 rc 1을 구분한다. 정상 픽스처를 생산 검사기에 입력하지만, 이 시험의 합성 원자료·메타데이터를 실제 WSL 사전 점검으로 취급하지 않는다.

## 해시 확인

```bash
sha256sum -c docs/reviews/lhs214_preflight_review_evidence_20261023/SOURCE_SHA256SUMS
(
  cd docs/reviews/lhs214_preflight_review_evidence_20261023
  sha256sum -c MANIFEST.sha256
)
```

첫 명령은 관련 소스가 검토 시점과 같은지 본다. 후속 정상 변경이 있으면 차이가 날 수 있으므로 이전 검토 결과를 새 소스에 그대로 적용하지 않는다.

## 반입 경로 정정

공개 검토문과 최초 패키지 감사의 증거 경로만 저장소 루트 기준으로 정정했다. 반입 전 원문·원 manifest·멤버 전체의 신원과 원본 불변 진술의 시점은 `import-paths/README.md`에 설명한다. 원시 JSON·로그·재생 도구와 하위 원 manifest는 고치지 않았다.
