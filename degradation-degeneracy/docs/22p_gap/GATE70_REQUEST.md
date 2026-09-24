# 70차 게이트 리뷰 요청 — **본 실행 GO 요청**

> **상태: 확정 (2026-09-24).** 사용자 결정 B — F50b 를 적용했다 (`src/io.py`, RUN_SCOPE). 기존 산출물의 무효화는 의도된 것이다.
> 사용자 결정 (2026-09-24): **GO 요청문을 보내고, NO-GO 면 게이트를 계속 돈다** — 다만 종료 조건 표를 들고 돈다.

읽는 쪽은 LLM 리뷰어다. 밀도 우선, 완충 문장 없음. **요청문은 증거가 아니다** — 아래 명령을 재실행해 검증하는 것을
전제로 쓴다. 우리 환경에서만 되는 것은 그렇게 밝힌다.

**이 요청문은 62차 이후 처음으로 본 실행 GO 를 요청한다.** 63~69차 요청문은 전부 "GO 를 요청하지 않는다" 였고, 그 사이
과학 코드는 한 바이트도 안 움직였다 (`743f65be`, 64차부터). 그 라운드들이 닫은 것은 검증층이고, 열려 있는 것은
**63차 재심 조건 6 "§0 독립 GO 전제를 구현·입증하고 고정 커밋에서 전 과정·환경별 회귀 완주"** 다. 이 요청문은 그 조건을
**표로 만들어** 정면에 놓고, 무엇이 GO 를 막고 무엇이 결과를 한정하는지를 **예/아니오로** 묻는다.

## 판정 대상 (이 블록이 정본이다)

| 항목 | 값 |
|---|---|
| 브랜치 | 루트 `CLAUDE.md` 하드룰 1 의 작업 브랜치 |
| **판정 대상 코드** | **`f0dfaff3bea1e1caedcd7a34275e908284cc2d4f`** — F50b 를 적용한 커밋 (RUN_SCOPE 를 마지막으로 건드린 커밋). `source_digest` **`5e660a8c73d5663a`** (64~69차의 `743f65be` · `e9ee7475dea7de1d` 에서 **이번에 움직였다** — §3) |
| 검토할 HEAD | 이 요청문을 담은 커밋 (발송문에 SHA. 동일성 문장은 **커밋 뒤에** 잰다 — 68차 D1) |
| 직전 판정 | 69차 **한정 범위 수용 / 종결** (2026-09-24) — 새 차단 발견 없음 · 본실행 GO 없음 · 리뷰어 검토 HEAD `e6ddcd1e` |
| 접수·대응 원장 | `docs/GATE69_WORKING_STATE.md` · 원장 §89 · 리뷰 패키지 원본 `docs/22p_gap/gate69_review/` (zip sha256 `f44c13effce78ee667a2184a5b0cab551a4a8fbd5e10ab23edec2b1f3c96f9bf`, MANIFEST 119/119) |

---

## §0 종료 조건 표 — **이 표가 전부 ✔ 이면 GO 인가?**

63차 재심 조건 6 이 가리키는 "독립 GO 전제" 와 그 뒤 라운드가 더한 항목을 **전부** 모았다. 리뷰어가 매 라운드 "기존 미착수를
새 발견으로 세지 않는다" 고 한 것을 그대로 받되, 이번에는 **목록을 닫는다** — 여기 없는 조건은 GO 조건이 아니라고 답해 달라
(있으면 표에 더해 달라).

| # | 전제 (리뷰어 원문의 이름) | 처음 나온 라운드 | 상태 (70차 발송 시점) | 닫는 계획 — 무엇을 · 어디에 · 회귀 | 우리 제안 분류 |
|---|---|---|---|---|---|
| E1 | **P0-1 producer 결속** — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | 49차 | **미착수** (7 라운드째) | `tools/archive_bundle.py` producer 가 manifest 를 typed schema 로 발행하고 payload 를 재해시해 영수증에 넣는다 · 소비자는 그 영수증만 믿는다 · 회귀: 위조 manifest/재압축 payload 거부 | **결과 한정** — 실행의 정확성이 아니라 묶음의 제3자 검증 가능성 |
| E2 | **trusted launcher** — 실행되는 source bytes 를 launcher 가 측정 | 53차 (조건 5) | **미착수** | `run.sh` 앞단에 측정 launcher: 실제 import 되는 모듈의 bytes 를 실행 **직전에** 재고 receipt 에 넣는다 (지금은 startup 뒤 관측) · 회귀: decoy 모듈 주입 거부 | **결과 한정** (P0-5③ decoy 반례는 이미 닫힘 — 경계만 남음) |
| E3 | **P0-4 typed 보존 영수증 소비** | 49차 | **부분** | `tools/preserve.py` 소비자가 typed receipt 를 재귀 exact schema 로 읽고, 부분 필드는 `unperformed` 로 | **실행 차단 후보** — 보존 판정이 결과 정본에 직접 붙는다 |
| E4 | **변이 증거의 독립 replay** — checker 가 스스로 재생 | 54차 | **미착수** | `mutation_replay.py --check-coverage` 가 조각 JSON 을 믿지 않고 sandbox 에서 표본 재생 (전수는 시간 초과 — 표본·seed 명시) | **결과 한정** |
| E5 | **P0-8 경로 무관 typed·sealed 실행 class marker** | 52차 | ~~**미착수**~~ **D4 정정 (70차 리뷰): 부분 구현** — 내용 identity·seal·capability·등록 lock·read-back·충돌 거부는 58~62차에 이미 있다. 남은 것은 reader(`_read_exec_class_at`)가 class enum + content_id 만 보는 것 (두 키만 있는 레코드·타입 틀린 레코드 수용 — 리뷰어 실측) → 71차 E5 로 닫음 | ~~`_exec_class` 레코드에 경로 대신 내용 identity 만 · 이동/복사 뒤에도 class 유지 · 회귀: 경로 바꾼 복사본의 class 일치~~ typed modern/legacy variant · content/seal 결속 · writer→reader→promotion 회귀 (리뷰어 §5) | **실행 차단 후보** — 본 실행 산출물의 class 등록이 이것에 걸린다 |
| E6 | **⑩ 등록부 격리** (별도 계약; 복원·class 변경은 별도 승인) | 66차 | **미착수** — 68차 Q5: 읽기 전용 영향·의존성 지도 먼저 | 1 단계 읽기 전용 지도(`docs/22p_gap/registry_impact.md`) · 2 단계 격리 migration 은 별도 승인 | **결과 한정** (1 단계는 이번 라운드에 낸다) |
| E7 | **F50b** — `start_파일_일치` 목록의 `git_commit` (RUN_SCOPE) | 66차 §2-5 | **✔ 적용 (이 커밋)** — RED `test_compare.py::test_f50b_start_file_check_ignores_git_commit_like_the_run_check` 를 본 뒤 고침, 대조군(다른 `source_digest`) 유지 | `src/io.py` 비교 목록에서 `git_commit` 제거 (`실행중_코드불변` 과 같은 판단) · RED: 문서 커밋만으로 resume 이 깨지는 재현 → GREEN · 새 `source_digest` | **실행 차단** — 10 시간 실행 중 문서 커밋 한 번이면 resume 이 5 건 연쇄 실패한다 (66차 실측) |
| E8 | 68차 G68-T1 (call-phase 증거) | 68차 | **✔ 69차 종결 수용** (신뢰 경계 답: 범위 타당, 추가 보안 설계 불요) | — | — |

**질문 1 (예/아니오):** 위 표의 E1~E8 이 전부 ✔ 이면 `f0dfaff3` 에 GO 인가. **아니오면 빠진 조건을 표에 추가해 달라.**

**질문 2:** 우리 분류 제안 — **실행 차단** = E3 · E5 · E7 (본 실행의 산출물·보존·class 등록에 직접 걸리는 것) ·
**결과 한정** = E1 · E2 · E4 · E6 (제3자 독립 검증의 전제 — 미닫힘이면 결과 문서에 한정 조건으로 적는다). 이 분류에 동의하는가.
동의하지 않으면 **어느 항목이 왜 실행 차단인지** 를 실행의 어느 산출물이 어떻게 틀리는지로 답해 달라.

**질문 3:** 분류에 동의하면 — E3 · E5 · E7 을 닫은 커밋에 **조건부 GO** (결과 문서에 "E1·E2·E4·E6 미닫힘" 라벨) 를 낼 수 있는가.

---

## §1 본 실행 계획 (GO 가 나오면 이대로 돈다 — 미리 합의한다)

| 항목 | 값 |
|---|---|
| 명령 | `./run.sh` (정본 config, 변경 없음) — 실행 receipt · `_exec_class` 등록 · archive bundle 까지 한 실행 |
| 예상 시간 | ~28 분(grid) + ~10 시간(fit) — 이 컨테이너 Linux |
| HEAD 고정 | 실행 시작 HEAD = 종료 HEAD. **실행 중 이 브랜치에 커밋하지 않는다** (E7 적용 뒤에도 운영 제약으로 유지) |
| 산출물 | `results/grid_fit_v4/` (gitignored) + `docs/RESULTS*.md` 갱신 + archive bundle (bytes · manifest · run receipt) |
| 보존 증거 | run receipt(서명·ancestry·tree·instrument) · `_exec_class` 등록 delta · smoke 재실행 · 실행 로그 전문 |
| 결과 라벨 | §0 의 미닫힘 항목을 **그대로** 문서 머리에 적는다 — "provenance: 자체 검증층 통과 · 독립 검증 전제 {N}/{M} 미닫힘" |
| 실패 시 | 실행 도중 실패는 고치지 않고 **실패로 보존**한다 (INCOMPLETE 유지) — COMSOL 갈래와 같은 규칙 |

---

## §2 우리가 GO 를 묻지 않았던 이유와, 지금 묻는 이유

62차 P0 3 건(temporal seal · run lock · producer scope)은 **그때 돌렸으면 결과를 통째로 버렸을** 결함이었다 — 첫 실행이
둘째의 bytes 를 봉인하고, 지운 grid 가 정본으로 승격됐다. 그 뒤 P0 는 0 건이고 심각도는 P1 2·P2 1 → P2 1 로 내려왔다.
검증층은 수렴했다. 반면 §0 표의 E1~E6 은 49~54차에 생겨 **한 번도 정면에 놓인 적이 없다** — 매 라운드 새 발견만 닫았고
요청문은 "GO 를 요청하지 않는다" 를 스스로 적었다. 종료 조건을 안 쓴 루프는 끝나지 않는다. 이 요청문이 그 조건을 쓴다.

---

## §3 F50b 를 GO 대상 커밋에 묶었다 (제안 B — 사용자 결정 2026-09-24)

F50b 는 RUN_SCOPE(`src/io.py`) 변경이라 `source_digest` 가 움직이고 **기존 산출물이 무효화**된다. 그래서 66차 리뷰어가 "(b) 다음
RUN_SCOPE 변경에 묶어라" 고 했고 우리는 보류했다. **본 실행이 곧 그 "다음" 이다** — 어차피 산출물을 새로 만드는 실행이므로,
F50b 를 그 커밋에 넣어야 (i) 실행 중 문서 커밋 한 번에 resume 이 깨지는 66차 실측이 재발하지 않고 (ii) 실행 뒤 F50b 를 적용하려고
10 시간을 한 번 더 쓰지 않는다. 변경은 한 줄의 목록에서 `git_commit` 하나를 빼는 것이고, `실행중_코드불변` 이 이미 같은 판단을 한다.

- RED 먼저: 같은 `source_digest` 로 start 파일의 `git_commit` 만 다른 artifact → `start_파일_일치` 실패 재현 (실측 사유: "코드는 같은데 git commit 이 다르다고 start 파일 대조가 실패했다") → 목록에서 `git_commit` 제거 → GREEN. 대조군: `source_digest` 가 다르면 여전히 실패.
- 변경은 `src/io.py` 한 곳 — 비교 tuple 에서 `"git_commit"` 하나를 뺐고 주석을 달았다. `실행중_코드불변` 과 같은 판단이다. commit 이동은 `_참고_git이동` 에 정보로 남는다.
- `source_digest` **`e9ee7475dea7de1d` → `5e660a8c73d5663a`**. 기존 산출물의 무효화는 **의도된 것**이고 본 실행이 다시 만든다. `--check-preimages` 는 변경 뒤에도 모든 지점 1 회.
- **질문 6:** `git_dirty` 는 목록에 남겼다 (~~문서 작업만으로도 dirty 가 되지만,~~ **D5 정정 (70차 리뷰 Q6): 이 전제가 틀렸다 — `git_info` 는 RUN_SCOPE 기준이라 범위 밖 문서 수정은 dirty 가 아니다.** 코드 수정은 dirty 로 나타난다 — `source_digest` 가 그것을 따로 잡는다). 이것도 빼야 하는가, 남겨야 하는가. → **답: 유지한다** (리뷰어).

---

## §4 실행 출력 (발송 직전 · 커밋 뒤 실측 — 채운다)

```
pytest gate63~68 묶음                          90 passed · 1 xfailed  (22.25 s)  EXIT=0   (gate63~68 방어 회귀, gate68 13 node 포함)
python3 -m pytest tests/ -q -p no:cacheprovider
        1 failed · 1804 passed · 2 xfailed  in 2425.16s (0:40:25)   EXIT=1   (실패 1 = tests/test_docs_lint.py::test_a_smoke_run_cannot_be_promoted_to_a_canonical_report — 67~69차와 같은 기존 환경 실패: 이 컨테이너에 results/grid_fit_v4 가 없다. f0dfaff3 첫 회귀의 다른 실패 1 은 옛 검증기로 만든 보존 영수증이 '낡았다' 는 예상된 결과였고 make_receipt.py 재검증(34/34)으로 닫았다 — 영수증 커밋 eb5209cf)
./scripts/smoke_e2e.sh
        ✅ pipeline smoke 통과   EXIT=0   (시작 HEAD = 끝 HEAD = eb5209cf)
source_digest                                 5e660a8c73d5663a
등록부                                        tracked 367 · 디스크 367 · 미추적 0 · 삭제 0
mutation_replay --check-preimages · -k premise  check-preimages: 모든 변이 지점이 정확히 한 번 · -k premise: 4 건(g65·g66·g67·g68) 전부 기대 node 를 call 단계에서 물었다
```

---

## §5 리뷰어에게 묻는 것 (§0 의 셋 + 셋)

4. **F50b 를 GO 대상 커밋에 묶는 데 동의하는가** (66차 (b) 의 "다음 RUN_SCOPE 변경" = 이 실행).
5. **결과 라벨 문구** — §1 의 "provenance: 자체 검증층 통과 · 독립 검증 전제 N/M 미닫힘" 이 충분한가. 부족하면 문구를 달라. → **답: 아니오** — 실제 통과/실패/미수행과 미닫힌 ID·영향을 적는다, `N/M` 은 보조 요약만 (리뷰어 §6 라벨 예시를 GATE71 §1 이 그대로 받는다).
6. **`git_dirty`** — §3 끝의 물음.

---

## §6 예산과 발송 규칙 (우리 정책 — 리뷰어 판정과 무관하게 적어 둔다)

**발송 규칙 (69차 교훈):** 발송문에 **요청문 커밋 SHA 와 브랜치 head SHA 를 둘 다** 적고, 둘 사이 dd diff 를 커밋 뒤에 잰 값으로 적는다.


이 요청 뒤 **최대 2 라운드**. 그 안에 GO 나 조건부 GO 가 없으면 §0 표의 상태와 리뷰어 답을 그대로 결과 문서에 적고
**사용자 결정으로** 실행 여부를 정한다. 게이트 루프는 우리가 만든 규칙이지 외부 의무가 아니다 — 다만 그 경우에도 결과 문서는
"GO 없이 실행 · 전제 {N} 미닫힘" 을 첫 줄에 적는다. 이 예산은 리뷰어에게 압력을 주려는 것이 아니라 **우리 루프에 종료 조건을
두는 것**이다 (62~69차 두 달의 교훈).
