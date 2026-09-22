# 67차 게이트 리뷰 작업 상태 (정본)

판정: **부분 수용 / 종결 NO-GO** — 2026-09-22 접수. 리뷰어가 고정한 HEAD
`cdc49e91af15b2ef968753110cfae3bbe7ab5c2f` · 직전 리뷰 `fa947cc9b17cdbeffbb39447c99159bc2c831e6e`
· 과학 정본 `743f65bead671bf353ce38027c2e8e457738ec08` · `source_digest e9ee7475dea7de1d`
(리뷰어가 직접 실행한 값과 우리 실측이 일치). 새 **P1 2 · P2 1 = 3건**.

새 P0 없음. 리뷰 패키지 원본은 `docs/22p_gap/gate67_review/` (zip 바이트 그대로 + `codex/`
풀어 둔 것, zip sha256 `3ab027349935843f8a2404a87b988b3e7264fa0a9d3266f2e3f20a757bd10220`).

**리뷰어가 닫혔다고 인정한 것** (되돌리지 않는다): G66-N1 A/B/C 원 반례 — 기존 재현기
`--full-sandbox` 5조건 전부 entry ACCEPTED · `PYTHONNOUSERSITE=1` 직접 전제 시험 2 passed ·
문맥 1회 측정 · G66-R1 삭제 사실 정정.

## 발견 원장

| ID | 무엇이 틀렸나 | 자리 | 상태 |
|---|---|---|---|
| G67-N1 (P1) | **부재 위조의 마지막 방어가 `auto` 였다.** user site OFF 면 `auto=False` 이고 표준 namespace 는 origin 이 없어 startup 이력의 파일 목록에도 안 잡힌다 → **부모가 올라와 있다고 잰** 이름을 child 가 `<absent>` 라 적어도 통과했다 | `mutation_replay.py` `_assert_customization_matches_parent` | 코드 ✔ |
| G67-N2 (P1) | **ZIP 분기에 사후 `sys.path` 재탐색이 남아 있었다.** ZIP *package* 의 `dirname(origin)` 은 archive root 가 아니라 `archive.zip/sitecustomize` 이고, 정상 startup 이 자기 archive 를 경로에서 빼면 root 도 final path 에 없다 → **정상 영수증을 거부**했다 (false rejection) | `mutation_replay.py` `_parent_customization_view` | 코드 ✔ |
| G67-T1 (P2) | 전제 회귀의 증거가 `"failed" not in stdout` 하나 → child pytest 가 **사용법 오류(rc 4)** 로 끝나거나 **수집만 하고 실행 0건**이어도 초록이었다. `rc 0` 만 더해도 두 번째는 남는다 | `tests/test_gate66_defensive.py` `_premise_run` | 시험 ✔ |
| G67-T1-b (P2) | 등록 변이 `the-premise-uses-a-controlled-env-g66` 의 witness 에 `stdout[-600:]` 에서 **우연히 잘린 꼬리**(`도 기대와 다르면 그때는`)가 있었다 → 다른 기계에서 `call_witness_matches=false` | `mutation_replay.py` `EXPECT` | 등록부 ✔ |

**RED 관측**: `tests/test_gate67_defensive.py` (17건) 첫 실행 **7 failed · 11 passed**.
(초판은 8 failed 였는데 둘은 내 시험 버그였다 — `EXPECT` 를 `MUTANTS` 로 썼고 `site_file=None`
이 다른 예외를 냈다. 고친 뒤 7.) 수정 뒤 **17 passed**, gate66 과 합쳐 **28 passed**.

## 한 줄 요약

**잰 것과 판정하는 것을 잇지 않았다** (N1 `auto` · N2 사후 재탐색) · **시험이 돌았다는 것과
초록이라는 것을 잇지 않았다** (T1 · T1-b).

## 리뷰어 재현기 — 수정 없이 먼저, 그리고 다시

세 건 다 이 Linux 에서 재현했고 고친 뒤 뒤집혔다.

```
                              수정 전                      수정 후
namespace_explicit_off        forged entry ACCEPTED   →    REJECTED     ← N1
namespace_explicit_on         forged REJECTED         →    REJECTED     (대조군 유지)
zip_package_remove_path       entry REJECTED          →    ACCEPTED     ← N2
zip_package_plain             entry ACCEPTED          →    ACCEPTED     (대조군 유지)
zip_module_remove_path        entry ACCEPTED          →    ACCEPTED     (대조군 유지)
premise (env_extra 통로)      committed ACCEPTED      →    REJECTED     ← T1
premise (바깥 env 통로)        child rc 4 / call 0건   →    child rc 0   ← T1 경계
gate66 원 반례 5조건           entry ACCEPTED          →    ACCEPTED     (되돌리지 않았다)
```

### ⚠ 한 번은 **거부가 증거가 아니었다** — 그대로 적는다

첫 재실행에서 `repro_boundaries.py` 의 T1 칸이 `committed REJECTED` 로 나왔지만 그 사유는
`TypeError: … missing 1 required positional argument: 'tmp_path'` 였다. 내가 시험 함수에
`tmp_path` fixture 를 더했기 때문이고, **그 거부는 우리 수정의 증거가 아니다.**
서명을 되돌리고(함수 안에서 `tempfile.TemporaryDirectory()` 로 정리한다) 다시 돌려
`AssertionError` 로 거부되는 것을 확인한 다음에야 닫혔다고 적었다.

`tmp_path` 에 **기본값을 주는** 방법도 재 봤는데 버렸다 — pytest 가 기본값이 있는 인자에는
fixture 를 넣지 않아(`--setup-show` 실측) 임시 디렉터리가 새어 나간다.

## 고침

### N1 — 판정의 기준은 **부모가 잰 것** 하나다

`if g != cand:` 를 앞세워 세 종류(absent · hex16 · namespace)를 **한 줄로** 대조하고, `auto` 는
사유 문장에만 쓴다. 이력(`loaded_file`)과의 교차 확인은 그 뒤에 남는다. 리뷰어 Q3 의 답을
그대로 받은 것이다 — *"부재 위조를 거부하는 근거로는 auto 를 쓰면 안 된다."*

정상은 계속 받는다: OFF + 명시 import namespace 의 **정직한** 영수증 · OFF + 정말로 미로드인
`<absent>` (둘 다 양성 대조군으로 고정).

### N2 — archive 와 member 로 읽는다 (`_archive_member_digest`)

origin 경로를 조상 쪽으로 걸어 **실재하는 파일**(archive)을 찾고, 남은 부분을 member 이름으로
써서 `zipfile` 로 그 바이트를 읽는다. 사후 검색 경로를 안 쓰고 **임의 loader 를 부모가 실행하지도
않는다** (stdlib `zipfile` 이 읽는다). 표준 archive 가 아니면 거부, member 를 못 읽으면 거부 —
읽기 실패 거부와 바이트 재확인은 유지했다.

### T1 — 무엇이 돌았는지 기계가 읽는다

child pytest 의 env 에서 `PYTEST_ADDOPTS`·`PYTEST_PLUGINS`·`PYTEST_DISABLE_PLUGIN_AUTOLOAD`·
`PYTEST_CURRENT_TEST` 를 걷고, `--junitxml` (pytest 내장 — plugin 을 더 요구하지 않는다) 로
결과를 받아 **정확히 그 두 node** 가 `passed`/`skipped` 인지 본다. `skipped` 는 통과가 아니라
**미측정**이므로 따로 찍는다.

검사 **순서**가 사유의 정확도를 정한다: 결과 파일 → node 집합 → 각 node 의 결말 → 그 밖의 rc.
rc 를 먼저 보면 어떤 고장이든 "정상 종료하지 않았다" 하나로 뭉개지고, 그러면 변이 증인도 그
뭉갠 문장이 된다 (실제로 한 번 그렇게 나왔다).

### T1-b — witness 는 고정된 이유다

잘린 꼬리를 걷고 **사유 문장까지만** 남겼다. 그리고 재발을 막는 정적 회귀
(`test_g67_14`)를 새로 두었다: 등록 witness 에서 **닫히지 않은 따옴표 뒤에 글자가 남아 있으면**
실패다. 값 직전에서 끊는 기존 관행(`… No such file or directory: '`)은 허용한다.

⚠ 더 넓은 규칙("닫힌 따옴표 조각은 시험 소스에 있어야 한다")도 재 보고 **버렸다** —
`'NoneType'`·`'ok:canonical'`·`'src.scoring:MODES'` 처럼 시험이 **결정적으로** 만드는 repr 이
19건 걸린다. 그것은 가변 꼬리가 아니므로 축을 잘못 겨냥한 규칙이다.

## 변이 등록부 (67차)

`auto` 가 판정에서 빠지면서 preimage 둘이 또 죽어 **자리를 옮겼다** (`-k` 를 넓히지 않았다):

| 축 | 옛 자리 | 새 자리 |
|---|---|---|
| `usercustomize-follows-the-startup-activation-g64` | `elif auto and cand != "<absent>":` | `if g != cand:` (측정과의 동일성 검사) · 위조 대조군 **셋**이 한꺼번에 빨개진다 |
| `explicit-import-is-an-ordinary-import-g65` | `elif not loaded_file:` | `if not loaded_file:` (동일성 검사가 앞에서 `continue` 하므로 `elif` → `if`) |

새 축 2 (`-g67`):

```
zip-bytes-come-from-the-archive-member-g67     MR     G67-N2  (사후 재탐색으로 되돌림)
the-premise-checks-the-child-actually-ran-g67  G66T   G67-T1  (전 판 증거 한 줄로 되돌림)

--check-preimages   모든 변이 지점이 정확히 한 번 나타난다 (rc 0)
-k g63   8/8 물었다 · rc 0      -k g64   3/3 물었다 · rc 0
-k g65   5/5 물었다 · rc 0      -k g66   3/3 물었다 · rc 0
-k g67   2/2 물었다 · rc 0
```

⚠ g67 T1 축은 preimage 를 **두 번** 고쳤다. 처음엔 주석 한 줄을 겨냥했는데 그 주석이 같은 줄에서
이어져 치환이 문장을 잘라 **변이가 수집을 깼다** (`변이가 수집을 깼다` 진단). 완전한 줄
(`assert junit.is_file(), (` + 그 인자 줄)로 옮기고 변이본이 컴파일되는 것을 따로 확인했다.

## 이 라운드가 하지 않은 것

- **P0-1 producer 결속 · trusted launcher · typed 보존 영수증 소비 · 독립 replay ·
  immutable bundle** — 미착수 (65·66차와 같다). 리뷰어도 새 발견으로 세지 않았다.
- **⑩ 등록부 격리** — 미착수. 리뷰어 Q5 의 답(**읽기 전용 영향 확인을 먼저, 복원/삭제/class
  변경/격리 migration 은 별도 승인**)을 받아 순서를 그렇게 적었다. 이번에도 복원하지 않았다.
- **Q6 F50b** — 여전히 (b): 다음 RUN_SCOPE 변경에 묶고 그때까지 "같은 commit 에서 resume" 을
  운영 제약으로 둔다.
- **Q1 의 더 강한 주장** — 리뷰어 지적을 받아 문서 문장을 좁혔다: 탐침이 주는 것은
  *"startup 후 관측한 module origin"* 이지 **로드 순간의 불변 기록이 아니다**. 그 이상은
  trusted launcher/immutable bundle 설계가 필요하고 그것은 미착수 항목이다.
- `source_digest` 는 `e9ee7475dea7de1d` 그대로 — 이번 고침도 전부 RUN_SCOPE 밖이다.
**본 실행 GO 는 요청하지 않는다.**

## 등록부 delta

커밋 직전 실측: tracked **367** · 디스크 **367** · 미추적 **0** · **삭제 0**. 67차 리뷰어가
직접 확인한 366→367 에서 더 움직이지 않았다.

⚠ 전체 회귀를 한 번 시작했다가 **4% 에서 끊었고**(Q1 문장 좁히기를 넣어야 해서), 끊은 탓에
`conftest` 세션 정리가 돌지 못해 미추적 `_exec_class` **175건**이 남았다
(`recorded_at` 13:43:57Z–13:46:31Z · 전부 `sealed`·`canonical` · `leg=L grid` 88 + `fixture` 87).
최종 체인은 13:49:32Z 시작이므로 **최종 트리의 산물이 아니다.** 끊긴 세션의 정리를 대신
수행해 그 175건을 지웠다 — **커밋된 기록은 하나도 건드리지 않았다**(tracked 367 그대로).
G66-R1 의 삭제(이미 커밋된 sealed 기록을 라운드 간에 지움)와는 다른 종류임을 명시한다.
