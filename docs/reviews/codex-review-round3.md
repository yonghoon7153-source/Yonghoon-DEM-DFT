---
title: Codex 3차 리뷰 과제 — 2차 갱신 검증
created: 2026-08-20
updated: 2026-08-20
type: guide
tags: [review, audit, crosscheck]
sources: [docs/reviews/codex-review-round2.md]
confidence: high
explored: false
verificationStatus: unverified
---

# Codex 3차 리뷰 — 2차 갱신 검증

2차 리뷰가 지목한 **회귀 8건**과 **안 닫힌 8건**을 고쳤다. 이번 과제는 그것이
정말 닫혔는지, 그리고 **또 새 회귀를 심지 않았는지**를 본다. 2차 리뷰에서
"수정이 새 결함을 심었다" 가 8건이나 나왔으므로, 이번에도 그쪽을 더 의심하는
것이 맞다.

범위: `fffe44af..86797e6a`, 소스 35파일 1,243줄 추가 / 133줄 삭제.

## 1. 동기화

```text
클로드 작업하고 왔어

git fetch origin
git merge --no-ff origin/claude/battery-charge-discharge-webapp-dq4ja3

머지 후 확인:
  git log --oneline -8
  git diff --stat fffe44af..86797e6a -- packages apps tools Makefile .github
```

`b5e89d8d fix: 2차 갱신 5/5` 와 `86797e6a create: 처음 쓰는 사람용 사용법` 이
보이면 준비된 것이다.

## 2. 리뷰 과제 (붙여넣기)

```text
fffe44af..86797e6a 의 2차 갱신을 검증해줘. 결과는
docs/reviews/2026-08-20-codex-review-round3.md 로 커밋해줘.

먼저 읽을 것:
- docs/reviews/2026-08-20-codex-review-round2.md — 네가 2차에서 지적한 것
- docs/reviews/2026-08-20-internal-audit.md — H1/M5/L10 의 처리 칸을 네
  지적대로 정정했다. 정정 내용이 이번엔 맞는지도 봐 달라.
- git diff fffe44af..86797e6a -- packages apps tools Makefile .github

A. 네가 지목한 회귀 8건이 실제로 닫혔는가

  1. composition.py — _FORMULA_TAIL(숫자+x/y/z)로 접미사를 넓혔다.
     SiOx/SiOx-C 는 돌아왔는가? 그리고 넓힌 대가로 새 오탐이 생기지
     않았는가 — 특히 am/se/si/gr/cb/cnt 같은 두 글자 힌트에 x/y/z 가 붙는
     조합. 그리고 Si/Gr/LTO/hard carbon/graphene 을 새로 추가했는데(범위
     확대다), 이것이 기존에 other 였던 것을 잘못 active 로 만들지 않는가.
     특히 "Gr" 이 graphite 인지 graphene 인지 모호한 실사용 표기.
  2. analysis.py compare_profiles — 그린 series 에서 basis 를 도출하고
     mixed_basis 를 넣었다. series 가 하나도 없을 때, 요청 basis 가
     비-용량일 때, drawn_cells 가 여럿일 때 resolved_cell 이 뭐가 되는지
     확인해라. 웹이 그 resolved_cell 을 질량 표시에 쓰고 있지 않은가?
  3. storage.py _write_atomically — mkstemp 로 바꿨다. 예외 경로에서
     임시 파일이 남지 않는가? mkstemp 의 fd 와 os.fdopen 의 이중 close
     문제는 없는가? 디렉터리가 없을 때는?
  4. storage.py load_columns — 핸들을 우리가 연다. np.load 가 파일 객체를
     받을 때 mmap/lazy 로딩 동작이 경로를 받을 때와 다른가? 큰 npz 에서
     메모리 사용이 늘지 않았는가? (with 블록을 나가기 전에 배열을
     dict 로 실체화하고 있는데, 그게 의도한 대로인지)
  5. drop_run_cache — 예외를 전부 삼킨다. 진짜 문제(디스크 오류)를
     숨기지 않는가? meta.json 을 먼저 지우는 순서가 정말 안전한가 —
     meta 만 지워지고 npz 가 남은 상태에서 load_columns 가 뭘 하는가?
  6. synthetic.ticks_at — 리터럴 변환으로 바꿨다. 실제 .wrd 의 Kind=Local
     tick 과 이 규약이 같은가? (실측 파일이 있으면 확인해 달라)
     ticks_ago 가 now() 를 쓰는 것과 services 의 datetime.now() 비교가
     정말 짝이 맞는가?
  7. Compare.tsx — mixed_basis 로 경고를 나눴다. cycles 모드와 profiles
     모드에서 mixed_basis 가 없는 옛 응답이 오면 어떻게 되는가?
  8. Makefile .PHONY — test-tools 를 넣었다. 다른 누락은 없는가?

B. 안 닫혔던 8건이 이번엔 닫혔는가

  - H9 taper: Schedule.taper_current_a(direction) 으로 옮기고 루프 스텝으로
    범위를 좁혔다. **반대 방향 오류를 특히 봐 달라** — 루프 안에 taper 가
    없고 formation 에만 있는 스케줄, 루프 판정(_looped_step_names)이 실패
    하는 스케줄에서 정상 사이클이 incomplete 로 떨어지지 않는가?
  - H11 중첩 worktree: "$REPO/apps/api" 로 좁혔다. 이 때문에 우리 서버를
    못 알아보는 경우가 생기지 않는가? (--app-dir 없이 띄운 경우, 심볼릭
    링크를 거친 경로, worktree 자체가 우리인 경우)
  - Codex #14 CRLF: bml repair crlf 를 만들고 문서를 바꿨다. sed -i 가
    바이너리나 큰 파일에 걸리면? find 범위가 tools/ 와 .claude/hooks/ 뿐인데
    충분한가?
  - 수동 cycle_offset 겹침: _overlapping_run 의 경계 조건(cycle_count=0,
    맞닿는 구간, 자기 자신 제외)이 맞는가?
  - L10 NPZ 무결성 / L13 비교 상한 / H1 기준 사이클 출처 / M20 synthetic

C. 이번 갱신이 새로 심은 것 — 여기를 가장 의심해라

  특히 볼 곳:
  - schemas.py 의 새 제약(PositiveMass/Percent/Finite). 지금까지 정상으로
    받아들이던 입력을 막지 않는가? 기존 DB 에 이미 들어 있는 값을 PATCH 로
    되돌려 보낼 때 422 가 나지 않는가? SampleUpdate 와 SampleIn 양쪽에
    같은 제약이 걸렸는지, 한쪽만 걸려 비대칭이 생기지 않았는지.
  - main.py 의 RequestValidationError 핸들러. FastAPI 기본 핸들러가 하던
    일(loc/type/msg 구조)을 그대로 유지하는가? 웹이 422 본문을 파싱하고
    있다면 형식이 바뀌지 않았는가?
  - runs.py 의 session.rollback(). 롤백 후 run 을 다시 get 하는데, 그
    시점에 run 이 없으면(=업로드 자체가 롤백됨) 원본 파일만 남고 DB 에는
    아무 기록이 없는 고아 상태가 되지 않는가?
  - normalize.py 의 composition_names_no_active. 기존에 mAh/g 가 나오던
    셀이 갑자기 안 나오게 되는 경우가 있는가? (역할 판정이 애매한 실제
    조성에서)
  - export.py 의 기본 제외. cycles_csv_string 등 다른 진입점도 같은 기본을
    쓰는가, 아니면 진입점마다 동작이 갈리는가?
  - bml 의 HEAD_FILE. worktree/심볼릭 링크에서 rev-parse 가 기대대로
    동작하는가? HEAD_FILE 이 없거나 비었을 때(옛 버전이 띄운 서버)
    무한 재시작 루프가 되지 않는가?
  - Dashboard 의 trend_cycles. 길이가 안 맞으면 옛 경로로 떨어지는데,
    그 조건이 맞는가?

D. 회귀 테스트가 진짜인가

  이번에 붙인 테스트 중 표본 6개 이상에서 수정을 되돌리고 그 테스트만
  돌려봐라. 통과해 버리면 가짜다. 특히:
  - test_a_truncated_cache_is_dropped_and_the_handle_released — Linux 에선
    수정 전후 모두 통과한다고 우리가 이미 적었다. 이 테스트가 무엇을
    지키는지, 지킬 가치가 있는지 판단해 달라.
  - i18n 의 백엔드 문구 커버리지 목록이 실제 wrdkit 출력과 일치하는가?
    (목록을 손으로 적었으므로 누락이 있을 수 있다)
  - CI 시간대 매트릭스가 실제로 실패를 잡는가?

E. 2차에서 P2 로 미룬 것들

  아직 안 했다. 우선순위가 여전히 맞는지만 확인해 달라:
  - API 통합 테스트의 basis 값 단언 (#13)
  - profile·compare·XLSX 의 미완료 사이클 테스트 (#15)
  - test_uploading_fills_blank_sample_conditions_from_the_schedule 양성 경로 (#14)
  - reference_cycle 이 존재하되 complete=False 인 반례 (#17)

F. 새 문서

  docs/guides/getting-started.md 를 처음 쓰는 대학원생 기준으로 썼다.
  문서가 실제 동작과 어긋나는 곳이 있는지 봐 달라 — 문서-코드 불일치가
  1차·2차 리뷰 모두에서 반복된 주제다.

보고 형식: 2차와 같다.
## 요약 / ## 안 닫힌 것 / ## 새로 심어진 것 / ## 가짜 회귀 테스트 /
## P2 재평가 / ## 문서 / ## 이상 없음
```

## 이번에 바뀐 것 (참고)

| 영역 | 파일 |
|---|---|
| 조성 인식 | `composition.py` (`_FORMULA_TAIL`, 음극 힌트 4종) |
| 정규화 | `normalize.py` (`composition_names_no_active`) |
| 스케줄·사이클 | `schedule.py` (`taper_current_a`), `cycles.py` |
| 내보내기 | `export.py` (`include_incomplete`), `cli.py` (`--all-cycles`) |
| 픽스처 | `synthetic.py` (`ticks_at` 리터럴 변환) |
| API 검증 | `schemas.py` (물리량 타입), `main.py` (422 핸들러) |
| API 저장 | `storage.py` (mkstemp, 핸들 소유, 무결성, fail-safe 삭제) |
| API 라우터 | `analysis.py`, `groups.py` (`GroupUpdate`), `runs.py` (롤백, 겹침) |
| 웹 | `Compare.tsx`, `Dashboard.tsx`, `SampleDetail.tsx`, `CellSpecPanel.tsx`, `CompositionEditor.tsx`, `i18n.ts`, `types.ts` |
| 도구 | `bml` (`repair crlf`, `HEAD_FILE`, 중첩 worktree), `Makefile`, `ci.yml` (시간대 매트릭스) |

검사 결과: `346 passed, 14 skipped` (UTC / Asia/Seoul / America/Los_Angeles
전부), vitest 93, bml 회귀 32, ruff·문서 린트 통과.

## 실측 파일이 있어야 답할 수 있는 것 (2차에서 이월)

`WRDKIT_SAMPLE=/path/to.wrd` 를 걸면 확인 가능하다.

- `cycles.py` — CC→CV 전환 행에서 두 Q 값이 같은가?
- `Plot.tsx` — 용량 plateau 에서 같은 x 가 중복되는가?
- `schedule.py` — `planned_cycles = max(loop_count)` 가 formation 을 포함하는가?
- `synthetic.ticks_at` — 실제 파일의 `Kind=Local` tick 규약과 같은가? (신규)

## 끝나면

"codex 3차 리뷰 나왔어" 라고 알려 주면 3차 갱신을 돌린다. 순서는 같다 —
**새로 심어진 것 먼저**, 그 다음 안 닫힌 것, 그 다음 P2.
