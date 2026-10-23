# LHS214 preflight SHA 형식 수정 증거 — 2026-10-24 KST

> 현재 canonical 전체 gate: **PASS, 155/0, rc 0**. [완료 기록](completion.md)을 따른다. 아래 작성자/초기 반입 시점의 예정·대기 문구는 원 스냅샷의 범위이며 현재 상태를 대신하지 않는다.


기준은 `ffbd438e7522d58eb069561fe58020f4086707ac`의 Git archive 사본이다. 메인 checkout·refs를 바꾸지 않았고, 새 사본의 실행기 두 호출만 수정했다. 실제 WSL 사전 점검·B7 승인 영수증·외부 GO·생산 실행 증거가 아니다.

## 시험 먼저 → 수정

`tools/check_pin_boundaries.py`를 먼저 작성하고 기존 실행기에서 실행했다. 도구는 [이전 프로브](../lhs214_preflight_review_evidence_20261023/tools/pin_probe.py)의 여섯 경계를 명시적 기대 실패 집합으로 검사한다. 정상 synthetic preflight 픽스처는 기존 `supp20_input_receipt._selftest()`가 만들며, 생산 검사 함수를 직접 호출한다. JSON의 `git.sha`만 바꾸고 원본 바이트를 복원한다. 로그 내용·로그 해시·등록·봉인 코드를 고쳐 통과시키지 않는다. 자체시험이 끝나면 원래 검사 함수도 복원한다.

| 실행 | 경계 검사 | 기존 receipt 자체시험 | 실제 종료 코드 |
| --- | --- | --- | --- |
| `red/` — 수정 전 | 6 중 LF 꼬리 하나가 기대와 다름 | 123/123 PASS, rc 0 | 1 |
| `green/` — P7·P10 수정 뒤 | 6/6 기대 일치 | 123/123 PASS, rc 0 | 0 |

여섯 기대: 정상 40자리 → 실패 없음; LF·CRLF·space·NUL 꼬리 → P7/P10 실패; 마지막 hex 하나 변경 → P10 실패. 원래 40개 hex가 승인 SHA와 같은 LF 사례이며 다른 커밋 승인 우회가 아니다. 자체시험의 정상 preflight 및 194·보충 20 합성 launch manifest 회귀도 양쪽 실행에서 통과했다. 로그의 `S8 실제 발사 manifest`는 자체시험이 만든 합성 manifest라는 뜻이며 실제 발사는 없었다.

`runner.diff`는 생산 코드 변경 두 줄 전부다. `_HEX40` 정의와 `launch_eligibility`의 사용처는 그대로이며, P7·P10의 `_HEX40.match(gsha)`만 `_HEX40.fullmatch(gsha)`로 바꿨다. 원문 SHA를 `strip()`하지 않는다. 실행기는 `CODE_FILES` 32 및 `HANDOVER_FILES` 2에 포함되지 않는다. `source-audit-before.json`과 `source-audit-after.json`에 목록·사용처·32개 파일 해시 불변·정확히 두 치환임을 기록했다.

봉인 지문은 red와 green 모두 `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb`이다. runner SHA-256은 `f4048aca55b912628278dbdd7b184ac449723736cd3f4f5cdc7eeca31294921a` → `3220be53fb89cd16c81f0273c8b9f7444f262c5311d02b2017756fd94fd66ac8`이며, receipt 도구는 `3d6110be24d24bf91ad1e71232a2e5dad580cf95178d6135b13aa6ca6de6f950` 그대로다.

## 재현

의존성 환경을 활성화하고, 임시 출력은 해당 환경에서 허용하는 저장소 밖 디렉터리를 사용한다. 현재 클라우드는 activation의 TMPDIR이 승인된 `/var/tmp/codex-nonrint-20261023`인지 확인하고 필요한 도구 승인으로 실행한다. 저장소·sandbox 표식을 제거하지 않는다. 아래 도구는 `--out`이 이미 존재하면 실패하므로 기존 결과를 덮지 않는다.

```bash
REVIEW_REPO=$(git rev-parse --show-toplevel)
REVIEW_TOOLS="$REVIEW_REPO/docs/reviews/lhs214_pin_syntax_fix_evidence_20261024/tools"
# --repo에는 검증하려는 실제 코드 사본을, --out에는 아직 없는 출력 경로를 준다.
python -I "$REVIEW_TOOLS/check_pin_boundaries.py" --repo "$REVIEW_REPO" --out "$TMPDIR/lhs214-pin-recheck-새이름"
```

현재 수정판은 rc 0이 기대다. red를 재현하려면 기준 핀의 별도 Git archive 사본을 `--repo`로 지정한다. 수정 전 사본의 rc 1은 의도한 LF 반례이며 receipt 자체시험 rc 0과 구분한다. 이 사본은 `.git` 없는 Git archive라 자체시험이 사용하는 pin은 synthetic fallback이다. JSON과 로그의 절대 경로는 당시 관측 기록이며 재현 입력 경로가 아니다.

`execution.json`은 실제 명령·환경·종료 코드, `red/`와 `green/`은 전체 receipt 로그·합성 preflight 로그·6경계 상세 JSON·요약, `MANIFEST.sha256`은 이 증거 폴더의 파일 해시다. 이 묶음 작성 시점의 전체 repository gate와 최종 canonical commit 검증은 root가 별도로 수행한다. 기존 155/0 기록을 이번 두 줄 수정의 새 전체 gate로 옮겨 쓰지 않는다.
