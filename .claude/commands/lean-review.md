---
description: 현재 diff 에 최소주의 사다리 적용 — 중복·재구현만 겨냥, 검증 코드는 carve-out
---

현재 변경분에 최소주의 사다리를 적용한다. 대상: $ARGUMENTS (비우면 upstream 대비
diff — `git diff "origin/$(git rev-parse --abbrev-ref HEAD)...HEAD"`. 브랜치 이름을
박아 두지 않는다: 루트 `CLAUDE.md` 하드룰 1이 정본이고, 박아 두면 브랜치가 바뀔 때
조용히 실패한다)

ponytail 의 decision ladder 를 이 저장소에 맞춰 **방향을 좁힌** 것이다. 이 저장소는
13라운드 리뷰가 검증 코드를 계속 **늘리라고** 요구해 왔으므로, 사다리를 검증
축에 들이대면 리뷰가 닫은 구멍을 다시 연다. 겨냥할 것은 **중복과 재구현**이다.

## 절대 줄이지 않는 것 (carve-out)

- provenance 서명 필드·`grid_run_spec`/`run_spec` 축
- validator 검사 (`validate_*`, `_verify_*`) 와 그 fail-closed 분기
- 인용 금지 배너·stale 판정 경로
- 회귀 테스트 (특히 리뷰 반례를 고정한 것)
- smoke 단계

이것들이 "중복처럼 보인다"면 그건 대개 **서로 다른 시점·다른 신뢰 경계**를 보는
검사다 (예: fitting preflight 검증 vs artifact validator 재검). 합치기 전에
`docs/08_REVIEW_RESPONSE.md` 에서 왜 둘 다 생겼는지 확인한다.

## 사다리 (읽은 뒤에 적용)

먼저 변경분과 그 주변을 실제로 읽는다. 그 다음:

1. **없어도 되나?** — 이 코드가 없으면 무엇이 깨지는가. 답이 "없음"이면 뺀다.
2. **이미 있나?** — 같은 로직이 이 저장소 다른 곳에 있는가. 있으면 재사용한다.
   (이 저장소 실적: env 결정축 비교가 `baseline.py`·`halfcell.py` 두 곳,
   check 작성 보일러플레이트, smoke 의 heredoc 패턴 반복)
3. **stdlib 로 되나?** — `hashlib`·`pathlib`·`itertools` 로 되는 것을 손으로 짜지 않는다.
4. **이미 깔린 의존성으로 되나?** — pandas/numpy/yaml 로 되는가.
5. **한 줄인가?** — 헬퍼를 만들 만큼 반복되는가, 아니면 한 줄로 끝나는가.
6. **그제서야 최소 구현.**

## 출력

우선순위 붙인 목록으로 보고한다. 각 항목:

- 위치 (`파일:행`)
- 사다리 몇 번에 걸렸는가
- 제안 (구체적으로 — "재사용하라" 가 아니라 "`src/io.py:_verify_observed_curves`
  의 패턴을 쓰면 12줄이 3줄")
- 위험도: carve-out 에 닿는가? 닿으면 **제안만 하고 실행하지 않는다**

## 규칙

- **읽기 전에 자르지 않는다** — "Lazy about the solution, never about reading."
- 이 커맨드는 기본이 **보고**다. 수정은 사용자 승인 후, 그리고 수정했으면
  `python -m pytest tests/ -q` 로 검증하고 숫자를 인용한다.
- 게이트 리뷰 대상 커밋 직전에는 실행하지 않는다 — 리팩터링이 `source_digest` 를
  바꿔 산출물을 무효화한다. 리뷰 사이클 **직후**가 적기다.
