# 61차 게이트 리뷰 작업 상태 (정본)

판정: **NO-GO** (2026-09-09). 새 **P0 2건 · P1 4건 · P2 1건**.
검토 head `f7cce7406e9ac233ad4727f6fa3bb4fc538b1de9` · 판정 대상 RUN_SCOPE
`c4e710040c2631d4f8140ee31c2f3c5004d9bcbb` · `source_digest d29650980daf6b9a`
(실측 일치 확인됨).

리뷰어가 **새 발견으로 세지 않은 것**: 요청문 §0 의 미착수·신고 항목,
환경 결손(`pybamm`·`tqdm` 부재)으로 인한 전체 회귀·lifecycle E2E 중단,
리뷰어 환경 receipt 가 달라 fail-closed 한 coverage 합집합.
`--check-preimages` 통과 · 60차 전용 회귀 49건 전부 통과 · wiki lint 0 errors.

## 판정의 한 문장

> **가장 강한 반례 둘은 공격이 아니라 정상 production 순서다.**

60차에도 같은 문장을 들었고, 같은 실수를 한 번 더 했다. 60차는 "report 를
**처음** 더하는" 경우만 시험했고, 61차가 낸 것은 "**이미 report 가 있는**
run 을 resume 한 뒤 그 report 를 갱신하는" 경우다. 시험이 production 의
**순서**가 아니라 순서의 **한 조각**을 봤다.

## 발견 원장

| ID | 무엇이 틀렸나 | 무효화하는 것 | 묶음 | 상태 |
|---|---|---|---|---|
| P0-1 | resume 시 시간 봉인이 **옛 report 를 흡수**한다. 이어지는 정상 report 갱신이 봉인을 stale 로 만들고, 새 content id 에는 class 가 없어 마지막 승격이 거부된다 | P0-1 종결 · 정상 resume 가용성 · execution class | α | 착수 |
| P0-2 | fit 이 논리 경로를 `/proc/self/fd/N` 으로 **대체**하고 그것을 durable manifest·summary·phase receipt 에 적는다. 성공하면 fd 가 닫히고 staged input 도 지워져 **존재하지 않는 경로가 provenance 가 된다** | P0-4 종결 · provenance · 재현 명령 | β | 대기 |
| P1-1 | capability 를 **마지막 사용자보다 먼저** 닫는다 — 닫힌 경로로 phase receipt 를 쓰고 lock 삭제가 `OSError` 를 삼켜 `.fit.lock` 이 남는다 | staged handle 수명 · phase receipt · 정상 cleanup | β | 대기 |
| P1-2 | 복수 `PYTHONPATH` root 의 **동명 module** 이 basename key 하나로 합쳐진다 (root 순서를 뒤집으면 digest 가 바뀐다) | P1-4 importable roots 증언 | γ | 대기 |
| P1-3 | startup-history **측정 실패**가 성공 영수증이 된다 (`{"<unmeasured>": "1"}`) — child rc 미검사 · 해석 실패 누락 · 예외를 정상 dict 로 | P1-3 증언 · coverage evidence 의 fail-closed 주장 | γ | 대기 |
| P1-4 | comprehension 결속을 **부모 scope 에 적용**한다 (Python 3 에서 comprehension target 은 별도 scope) | P0-11 scope 모델의 정확성 | δ | 대기 |
| P2 | `STAGE3_CONTRACT.md:1071` 은 AST 정규형에서 docstring 이 사라진다고 적는데 현재 코드는 보존한다 — 계약 문구가 현재 규칙과 **반대** | 계약 문서의 정확성 | ε | 대기 |

## 묶음

| 묶음 | 축 | 발견 |
|---|---|---|
| α | 내용 identity 의 **member 집합을 무엇이 정하는가** — 우연한 파일 존재가 아니라 선언 | P0-1 |
| β | **논리 경로와 I/O handle 경로의 분리** · capability 수명 | P0-2 · P1-1 |
| γ | 증언의 **키 공간과 실패 전파** | P1-2 · P1-3 |
| δ | producer scope 모델을 Python 과 맞춘다 | P1-4 |
| ε | 계약 문구 | P2 |

## 이번 라운드의 규율 (60차에서 이어받음)

- 발견마다 **RED 를 먼저 눈으로 본다**. 리뷰어 반례는 그대로 회귀로 고정한다.
- **production 의 순서 전체**를 도는 회귀를 쓴다. 조각만 보는 시험이 60차
  P0-1 을 통과시켰다.
- 방어를 심으면 **축을 심는다**. 그리고 방어를 넓히면 **다른 시험의 축이
  가려지는지** 마감에 다시 센다 (60차에 네 번 났다).
- 새 시험이 처음부터 통과하면 fixture 가 진실을 가린 신호다.

## 좌표

- 봉인: `tools/preserve.py` `RUN_MANIFEST_SCHEMA:4254` · `_sealed_manifest_parts` ·
  `_present_manifest_parts:4420` · `seal_run_identity:4446` · `run_content_id:4528`
- staging: `src/fitting.py:1011`(경로 대체) · `:1571`(`manifest.input`) ·
  `:1587`(`fits_parquet`) · `:1594-1597`(commit 뒤 fd 경로 반환) ·
  `:1028`(phase receipt) · `:1031`(lock 삭제)
- lock 삭제가 오류를 삼키는 자리: `src/io.py:518`
- 증언: `docs/22p_gap/mutation_replay.py:4295`(child rc) · `:4305-4312`(해석·예외) ·
  `:4322`(basename key) · `:4423-4429`(receipt reader)
- scope: `docs/22p_gap/row_projection.py:1427`(`_own_shadows`) · `:1456-1467`
- 계약: `docs/22p_gap/STAGE3_CONTRACT.md:1071`

## 마감 진행

### 이번 라운드 방어의 축 감사 — 여섯이 없었다

60차 마감의 교훈(방어를 심었으면 축을 심는다)대로 다섯 묶음 전부를 셌다.

| 새 축 | 발견 | 결과 |
|---|---|---|
| `derived-manifests-are-outside-the-identity-g61` | P0-1 | 문다 |
| `records-keep-the-logical-input-g61` | P0-2 | 문다 |
| `records-keep-the-logical-output-g61` | P0-2 | 문다 |
| `the-run-lock-is-released-g61` | P1-1 | 문다 |
| `lock-release-failure-is-not-swallowed-g61` | P1-1 | 문다 |
| `comprehensions-are-their-own-scope-g61` (MULTI 2자리) | P1-4 | 문다 |

마지막 것이 또 같은 교훈을 줬다. 처음엔 `if _is_comprehension(sub):` 를
`if False:` 로 두는 변이로 썼는데 **안 물었다** — 그러면 comprehension 안으로
들어가기만 하고 target 은 여전히 안 묶여서 결함이 복원되지 않는다. **축은
"지운 검사" 가 아니라 고치기 전 코드를 되돌려야 한다.** 61차 이전 문장
(`if isinstance(sub, ast.comprehension): out |= …`)을 되살리자 리뷰어의 반례가
그대로 증인이 됐다.

그리고 γ 를 닫으면서 죽은 축 2건을 재조준하고(α 가 schema 선언을 갈랐고 γ 가
`packages` 문장을 바꿨다), 가려진 축 1건을 떼어 냈다. 떼어 내고 보니 남은
`env` 자리 하나로는 안 물어서(`_env_facts()` 안에도 같은 결속이 있다) 두 자리를
함께 되돌리는 MULTI 로 바꿨다.

등록부 (이 시점): **MUTANTS 202 · MULTI 31 · EXPECT 224 · DECLARED_MASKED 10**.
전수 재생이 중복 축 하나를 떼어 내면서 최종값은
**MUTANTS 201 · MULTI 31 · EXPECT 223 · DECLARED_MASKED 10** 이 됐다 (아래
"12조각 전수 재생" — 합집합 232 축).

### 세대 전환 (g15 → g16)

```
g15_2026_09_08  active → frozen  (journal seq 14)
g16_2026_09_09  새 active · docs/22p_gap/proj_g16

pin  compute            3b94bda70dc63869 → fa5b9324c01ab7f0
     row_projection     a425da3233253625 → 0e22767966646d49
     producer_semantic  6518c2fa47f1e8c4 → 2e2ddce417ecf0db
     src_scoring        69e69cb046f4b4ae (변동 없음)
영수증 core              d15881088e022ce6… → fc1cf9c0ef22490f…
validator                d29650980daf6b9a → 4227b40871fa0c10
행 바이트                 ad598fe77e75afec — **열두 세대째 같다**
```

pin 을 움직인 것은 δ(P1-4) 다 — analyzer 가 comprehension 을 자식 scope 로
다루게 됐다. `src_scoring` 이 그대로이고 행 바이트가 안 움직인 것이 "계산식은
안 건드렸다" 를 실물로 말한다.

**전환 중에 층 셋이 물었다** (전부 이 저장소가 앞선 라운드에 세운 것이다):

1. 얼린 cohort 를 복사하면서 `frozen_reason` 이 딸려 오자 —
   "status 만 active 로 되돌린 해동이다. 얼린 cohort 는 자라지 않는다".
2. `evidence.cohorts` 양방향 대조가 g16 누락을 잡았다.
3. 원장의 `validator_identity.source_digest` 가 새 영수증과 어긋난다고 잡았다.

### 12조각 전수 재생 — 세 번 만에

| 회차 | 결과 | 원인 |
|---|---|---|
| ① | 3조각 빨강 | 새 축 하나가 58차 축과 **preimage 공유** · α 가 60차 P0-1 축을 가림 · 증인에 박힌 content id 가 v4 로 바뀜 |
| ② | 5조각 "baseline 이 이미 빨갛다" | ①에서 증인을 자르며 남긴 **꼬리 공백 한 칸** (`aa901eb5`) |
| ③ | 12/12 통과 (`54b7be67`) | 합집합 **232 축** (실행 222 · 선언 10) |

②의 교훈: **증인은 접두 대조다.** 경계를 한 글자 틀리면 그 조각 전체를 못 재게
만든다 — 그리고 그 실패는 "변이가 안 물었다" 가 아니라 "baseline 이 이미
빨갛다" 로 나와서, 원인을 찾을 때 변이 쪽을 먼저 보게 만든다.

### 마감 산출

| 무엇 | 상태 |
|---|---|
| 발견 7건 전부 코드에서 닫힘 | ✔ `3911c2be` `3a08f589` `7dafdfbd` `2f7acafb` `6dfa8615` |
| 새 축 6개 + 재조준 3 + 중복 제거 1 | ✔ `3a7d102b` `faa838c2` `aa901eb5` |
| g15 → g16 · 투영 재생성 · 영수증 | ✔ `e37bff80` |
| 12조각 전수 재생 증거 | ✔ `54b7be67` |
| 원장 §73(판정)·§74(대응) | ✔ |
| webapp `/trust` §6 · `/handover` 신설 | ✔ `6f731382` |
| 전체 회귀 + strict smoke | ✔ 1615 passed, 1 xfailed · smoke exit 0 (아래 실측) |
| 요청문 | ✔ `docs/22p_gap/GATE61_REQUEST.md` |

### 신고 (요청문 §0 로 옮길 것)

- `docs/22p_gap/_exec_class/` 에 **커밋 안 된 레코드가 쌓인다.**

  실측 (2026-09-09 13:16, 전체 회귀가 도는 중):

  ```
  git ls-files … | wc -l        16      (추적)
  ls …/*.json    | wc -l       104      (디스크)
  mtime 분포                    08:05 4건 · 12:36–12:39 100건
  _exec_class/local/            6471    (gitignored — 58차 L14 대로)
  ```

  88건이 **이번 실행 창(12:36–12:39) 안에** 생겼다. 즉 시험 또는 smoke 가
  공유 등록부 자리에 `canonical`/legacy 레코드를 남긴다 — `.gitignore:52` 는
  그 두 분류를 **감사 대상이라 커밋한다**고 선언하므로, 시험이 만든 것이
  거기 섞이는 것은 선언과 어긋난다.

  **아직 안 한 것**: 어느 시험이 쓰는지 못 좁혔다. 후보는 원장을
  monkeypatch 하지 않는 넷이다 — `tests/test_compare.py` ·
  `test_exec_class_capability_59.py` · `test_fitting.py` ·
  `test_handle_carry_59.py` (실측: `canonical_ledger` 문자열이 없는 파일).
  회귀가 끝난 뒤 지우고 하나씩 돌려서 좁힌다.

  산출물 identity 나 `source_digest` 에는 영향이 없다 (`docs/` 는 RUN_SCOPE
  밖). 이번 라운드에서 **고치지 않는다** — RUN_SCOPE 를 건드리면 영수증·g16·
  전수 재생을 전부 다시 만들어야 한다. 요청문 §0 에 신고하고 다음 라운드로.

- **grid 의 콘솔 요약이 staged 경로를 적는다** (`src/grid.py:806`).

  실측 (이번 마감 strict smoke 출력):

  ```
  ── 1. PyBaMM 합성 격자 (producer artifact) ──
  { "n_ok": 6, ..., "out_dir": "/proc/self/fd/3" }
  ```

  β 가 고친 것은 durable 기록이고, grid 의 durable 기록은 이미 `named_out` 을
  쓴다 (`:837` `"out": str(named_out)` · `write_curves_manifest(named_out, …)`).
  남은 것은 `print(json.dumps(summary))` 한 줄 — **파일로 안 남는다.** 그래도
  운용자가 다음 명령에 복사할 경로를 거짓으로 말한다.

  **다음 라운드 첫 항목.** 한 줄이지만 RUN_SCOPE 라 `source_digest` 가 움직이고,
  그러면 영수증(~28분)·전체 회귀(44분)·strict smoke 를 통째로 다시 만들어야
  한다. 판정 뒤에 한 번에 하는 편이 싸다.

### 전체 회귀 + strict smoke (마감 실측, `54b7be67` 트리)

```
python -m pytest tests/ -q      1615 passed, 1 xfailed   (44분 26초, exit 0)
./scripts/smoke_e2e.sh          pipeline smoke 통과 (✅ 52건, exit 0)
```

## 62차 준비 메모 (2026-09-14, 서브 브랜치 merge 뒤)

서브(`claude/bms-alpha-beta-verify`)를 `cf9bad4` 로 merge 했다. 서브가
`bms-balancing/HANDOFF_TO_GATE.md` §2d 에 적어 둔 62차 제안을 본체가 읽고
**아직 실행하지 않은 채** 여기 옮긴다 — 정본은 그 문서다.

| 제안 | 본체 판단 |
|---|---|
| 정상 production 순서 **전체**를 도는 e2e (grid 굳힘 → fit → commit → report → **resume** → report 갱신 → 승격) | **한다.** 60·61차가 같은 축에서 연속 P0 를 냈다 — 조각 시험이 순서를 못 봤다. 62차 요청 전 첫 작업 |
| 요청 전 `/self-review` (렌즈 `순서-TOCTOU` · `sig-완전성`) | **한다.** 10차에 CONFIRMED 3건이 전부 외부 리뷰와 같은 축이었다 |
| pyDMA 외부 검증을 요청문에 싣기 (`bms-balancing/reviews/BML_R1_RESPONSE.md` §12) | **싣는다.** LLI 세 구현 0.09~0.18 %p 일치 · LAM 두 축 1.0~1.5 %p 흩어짐 · γ 설정 12배 이동에도 CU2 네 값 불변 — 합성 진실 밖의 독립 근거. ⚠ 데이터 한 세트·optimizer 한 종·pyDMA 는 기록값이라는 경고를 같이 옮긴다 |
| 축퇴 폭 측정법(근최적 집합 위 제약 최적화 + 등식 프로파일)을 본체에 쓸지 | **보류.** 서브 스스로 "하한이고 tol 은 통계가 아니다" 라 적었다. `hessian.py` 처럼 참고 진단이면 몰라도 결론 근거로 쓰려면 봉인 fits 에서 재계산되는 provenance 가 먼저다 |
| `wiki/` 후보 — 방법론 개념 페이지 · Schmitt 2022 실측 추가 · chain rule 결함 | **보류.** ingest 는 논문 에이전트 비용이 크다. 서브 §3 목록을 그대로 후보로 둔다 |

**서브가 던진 확인 하나** (HANDOFF §3-3): 규진팀 `dv_cell_model` 은 좌표를
`(x−b)/a` 로 바꾸면서 도함수에 `1/a` 를 안 곱한다 (7~15 % 계통 오차). 본체의
dV/dQ 항에 같은 자리가 있는지 — 확인 결과는 이 절 아래에 적는다.

이 라운드의 61차 NO-GO(P0 8건)는 그대로 열려 있다. 위 표는 그 대응과 별개로
**요청문을 보내기 전**에 할 일이다.

**확인 결과 (방금 읽음)**: 본체에는 그 자리가 **구조적으로 없다.**
`src/objective.py:249` 가 `compute_features(target.x, v_model, …)` 로 **재구성한
full-cell 전압을 full-cell 축 x 로 직접 수치 미분**한다
(`:168` `np.gradient(_smooth(v), x)`). 규진팀 코드처럼 반쪽전지 dV/dQ 표를
변환 좌표 `(x−b)/a` 로 찾아 쓰는 경로가 없으므로 곱해야 할 `1/a` 자체가
등장하지 않는다. 즉 해당 없음 — 다만 이것은 "본체 dV/dQ 항이 옳다" 의 증명이
아니라 **그 특정 결함이 들어올 자리가 없다**는 확인이다.
