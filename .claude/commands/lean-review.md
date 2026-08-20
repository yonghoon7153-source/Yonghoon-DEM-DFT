---
description: 현재 diff 에 최소주의 사다리 적용 — 중복·재구현만 겨냥, 검증 코드는 carve-out
---

현재 변경분에 최소주의 사다리를 적용한다. 대상: $ARGUMENTS (비우면 upstream 대비
diff):

```bash
# base 결정 순서. **자동 fallback 금지** — 못 찾으면 멈추고 사람에게 묻는다.
base="${1:-}"                                   # 1) 인자로 준 것이 최우선
if [ -z "$base" ]; then                         # 2) attached + upstream 있으면 그것
  base=$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null) || base=""
fi
if [ -z "$base" ]; then                         # 3) 그 밖에는 중단
  echo "비교 base 를 못 정했다 (detached HEAD 이거나 upstream 이 없다)."
  echo "  base 를 인자로 줘라:  /lean-review <ref>"
  echo "  origin/HEAD 로 자동 대체하지 않는다 — 기본 브랜치와 비교하면"
  echo "  이 브랜치와 무관한 diff 가 나온다 (20차 발견 11 · 22차 발견 8)."
  exit 1
fi
git diff "$base...HEAD"
```

★ 두 번 틀렸다. 초판은 `origin/$(git rev-parse --abbrev-ref HEAD)` 였고
(detached 에서 `--abbrev-ref HEAD` 가 문자열 `HEAD` 를 반환한다 — 20차 발견 11),
2판은 upstream 조회 실패 시 `origin/HEAD` 로 **자동 대체**했다. 그러면 detached
checkout 에서 결국 기본 브랜치와 비교한다 — 22차 발견 8. 조립도 대체도 하지
않고, 못 정하면 **멈춘다**.

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
