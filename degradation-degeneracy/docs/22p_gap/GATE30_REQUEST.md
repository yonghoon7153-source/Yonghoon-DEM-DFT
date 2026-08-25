# 30차 게이트 리뷰 요청 — 29차 P0 둘 + P1 넷 + P2 하나

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   c6a65fabfbd06f3c8696536b29327dbcd1f47e86
코드 커밋:   5df3f6a1…      # RUN_SCOPE 변경이 들어간 커밋
직전 대상:   c5ae4c8e…      (29차, NO-GO)

source_digest:
  29차:  0ca9f3d13bf21a59
  현재:  35907dff97b67dc5

재현:      git checkout c6a65fabfbd06f3c8696536b29327dbcd1f47e86
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| P0-1 (저널 자기신고가 권위) · P0-4 (pin 이 CAS 원본 파괴) | 닫혔는가 |
| P1 1~4 (중첩 스키마 · manifest 충돌 · 임의 바이트 · retention 하한) | 어디까지인가 |
| P2 (세대 계약이 가변 YAML) | 닫혔는가 — **반대 방향 과잉 수정을 한 번 했다**, §4 |
| 「최소 증거」 1~3 · 5~8 | 대응표 §5 |
| 4 (crash/reopen drill) · 9 (generation directory) | **미완료로 신고한다** — §6 |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
c6a65fabfbd06f3c8696536b29327dbcd1f47e86
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
860 passed, 1 xfailed in 282.13s (0:04:42)

$ ./scripts/smoke_e2e.sh          # 9a05a906 (clean) 에서
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 -c "…source_digest()"
35907dff97b67dc5

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha 2c36f26adb2a5196

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. P0-1 — 저널이 적은 것이 곧 등록이었다

리뷰가 준 반례 둘을 재현하고 회귀로 고정했다.

| 반례 | 옛 결과 | 지금 |
|---|---|---|
| journal 이 **부분집합**을 선언 | registered: True | `registered: False` |
| 등록 전체를 다른 backend 로 복사 | registered: True | `registered: False` |

원인은 검사 부족이 아니라 **권위의 위치**였다. journal 을 쓰는 쪽과 검증하는
쪽이 같은 문서를 봤다. 이제 `verify_registered_graph(backend, index, leg)`
하나가 권위이고, 출발점이 **pin 에서 읽은 receipt** 다:

```text
1  pin 에서 receipt 회수 (objects/ 를 비워도 회수돼야 한다)
2  닫힌 스키마 + 손에 든 backend 의 URI 로 검증
3  pin 에서 manifest 회수, receipt 집계와 결속
4  receipt+manifest 로 기대 그래프 재도출
5  expected == journal.objects == 디스크 pin 이름   (삼면 일치)
6  pin 된 바이트 전수 + 산출 객체 크기
```

`is_registered(index, leg, backend)` 는 backend 를 받으면 이 함수를 돌린다 —
저장된 bit 가 아니라 backend 에 대고 평가하는 **술어**다.

| 회귀 | 무엇을 고정 |
|---|---|
| `test_a_journal_that_declares_a_subset_is_not_a_registration` | 반례1 |
| `test_a_registration_copied_to_another_backend_is_not_registered` | 반례2 |
| `_DropAfterRead` backend | read 직후 삭제 → pin 단계에서 정지 |

## 3. P0-4 — pin 이 CAS 원본을 0바이트로 만들었다

hardlink 불가 FS 예비 경로가 목적지를 **열어 썼고**, 그 목적지는 같은 inode
의 CAS 원본이었다. 보존 도구가 보존 대상을 파괴했다. 재현:

```
원본 바이트 이후: b''
원본 digest 유효: False
```

목적지를 직접 여는 경로를 없앴다:

| 상황 | 지금 |
|---|---|
| pin 이 이미 있다 | 바이트 대조, 다르면 실패. symlink 는 거부 |
| 경쟁 `EEXIST` | 같은 규칙으로 내용 확인 |
| hardlink 불가 | 임시파일 → `os.link` 원자 배치, temp 항상 정리 |

회귀: `test_pinning_twice_never_truncates_the_cas_original`.

## 4. P2 — 세대 계약, 그리고 **반대 방향 과잉 수정**

닫은 것: role 세대를 `evidence.leg_source_digest` 가 아니라 **봉인된 투영이
적은** `source_digest` 와 대조한다. evidence 와 role 을 함께 바꾸는 변형이
막힌다.

여기서 실수를 하나 했고 그대로 신고한다. 29차 초판은 28차가 죽여 놓은
조건을 `rg == tg` 로 되살렸는데 **너무 넓었다** — v5 다리가 v5 legacy 주장의
정본이 되는 것까지 막아, 24차 보충이 명시적으로 허용한
`LEGACY_PAIRED_FIXED5` 를 깨뜨렸다 (전체 시험이 그 자리에서 빨갛다).

원인: leg-level `inference_role` 이 무엇에 대한 판정인지 잘못 읽었다. 원장이
그 다리를 `diagnostic` 이라 적은 근거는 원장 안에 있다 — "**현행 정본은
아니다**: run_spec 의 `source_digest` 가 현행과 다르다". leg-level 은 **현행
세대에 대한** 역할이지 모든 세대의 상한이 아니다.

| 축 | 지금 |
|---|---|
| 비교 대상 | `tg == current` (옛 세대는 `role_compatibility` 가 관장) |
| `current` | 선언이 아니라 **도출** — 산출물이 도달한 가장 새로운 세대. `v6` 은 산출물이 없어 현행이 될 수 없다 |
| 세대표 위조 | 표의 모든 digest 가 **봉인된 투영에 묶여** 있어야 한다 |

네 규칙이 실제로 무는 것을 변이로 확인했다:

| 변이 | 실패하는 회귀 |
|---|---|
| leg-level 조항을 `False` 로 | `..._legacy_claim...` · `..._self_promote...` |
| `tg == current` → `rg == tg` (29차 판) | 위 둘 + 본 계약 시험 |
| 세대표 anchoring 삭제 | `..._anchored_to_sealed_projections` |
| `current` 도출을 선언으로 | 셋 |

변이를 걸 수 있게 계약 본문을 `_claim_role_problems` 순수 함수로 꺼냈다.
인라인일 때는 규칙을 고쳐도 "고친 규칙이 실제로 무는가" 를 보일 수 없었다 —
35.7 의 "이름이 검사보다 강한 시험" 의 다른 얼굴이다.

## 5. 「최소 증거」 대응표

| 항 | 요구 | 대응 | 상태 |
|---|---|---|---|
| 1 | 두 경로를 통합하는 단일 권위 | `verify_registered_graph` §2 | 닫음 |
| 2 | subset/extra/duplicate journal · receipt 부재 · foreign backend | 반례 둘 + 회귀 | 닫음 |
| 3 | pin read-then-delete · `EEXIST` · symlink preseed · hardlink 불가 fallback | §3 세 갈래 + 회귀 | 닫음 |
| 4 | fsync 순서 + **crash/reopen drill** | 순서는 고침, **drill 없음** | **부분** |
| 5 | 중첩 receipt/planned/validation/output 스키마 · manifest 결속 · 출력↔CAS 바이트 · retention 정책 | 닫힌 키 집합 · `MIN_RETENTION_DAYS = 365` | 닫음 |
| 6 | LF/CRLF/NUL 임의 바이트 CAS 왕복 | 6종 왕복 + `os.O_BINARY` | 닫음 |
| 7 | 대소문자/NFC manifest 충돌 · 재귀 design domain · warm objective 필수 | 셋 다 | 닫음 |
| 8 | role digest 를 등록 receipt/투영 source digest 에 결속 | §4 | 닫음 |
| 9 | immutable cohort generation + 단일 `CURRENT` 승격 + crash 주입 | **미착수** | **미착수** |

## 6. 닫지 않은 것 — 그대로 적는다

| # | 무엇 | 왜 이번에 안 했나 |
|---|---|---|
| 4 | crash/reopen drill | fsync **순서**만 고쳤다. 프로세스 중단 주입 하네스가 없다 |
| 9 | generation directory + 단일 `CURRENT` | `row_projection` 승격이 여전히 fixed-name 세 파일 — set atomicity 가 아니다. 다음 checkpoint |

계약 §13 의 열 묶음은 여전히 **미착수/부분**이며 "닫음" 으로 바꾸지 않았다.

## 7. 자체 발견 — spec 이 거짓을 선언하고 있었다

`ANALYSIS_SPEC.summary_comparison.skip_top_level_keys` 가
`[_채점원본, _F4_주의]` 라고 적혀 있었지만 비교기는 `SEMANTIC_SKIP` 을 썼다.
이력을 확인했다:

* 23차 `f49cd66e` — 비교기도 둘 다 뗐다. 선언이 참이었다.
* 28차 — 비교기를 `("_채점원본",)` 로 좁히면서 **선언은 안 고쳤다**. 직전
  커밋 `2e505317` 에 `_SKIP = set(SEMANTIC_SKIP)` 과 옛 선언이 공존한다.
* 29차 — spec 이 `SEMANTIC_SKIP` 을 읽는다.

`analysis_spec_sha256` 이 `f1898eb6…` → `43d74dd3…` 로 움직인 것은 **비교 규칙이
바뀐 것이 아니라 거짓 선언이 사라진 것**이다. 원장 g2 항목이 이 값을 g1 과
바이트 동일이라 적고 있었으므로 그 산문도 정정했다. 행 바이트
(`projection_sha256`·`restart_projection_sha256`·`fits_sha256`)는 g1 과 동일하다.

## 8. 산출물 재생성

`g2_2026_08_25` 투영과 영수증을 clean tree 에서 다시 만들었다
(`validator_tree_dirty: false`, commit `eb98e0ad`). 원장 pin:

```text
compute_sha256                    fe9d7473b6ef0e87 → 3084596353e63426
row_projection_py_sha256          9f7dde01a0308856 → 53ae8205d201517c
analysis_spec_sha256              f1898eb6…        → 43d74dd3…
verification_receipt_core_sha256  069e277e…        → 2c36f26a…
validator_identity.source_digest  0ca9f3d13bf21a59 → 35907dff97b67dc5
```

`g1_2026_08_20` 은 frozen — 손대지 않았다.
