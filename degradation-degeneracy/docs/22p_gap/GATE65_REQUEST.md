# 65차 게이트 리뷰 요청 — 묶음 5 (64차 대응 · 방어층 origin 규칙)

읽는 쪽은 LLM 리뷰어다. 밀도 우선, 완충 문장 없음. **요청문은 증거가 아니다** —
아래 명령을 재실행해 검증하는 것을 전제로 쓴다. 우리 환경에서만 되는 것은 그렇게 밝힌다.

## 판정 대상 (이 블록이 정본이다)

| 항목 | 값 |
|---|---|
| 브랜치 | 루트 `CLAUDE.md` 하드룰 1 의 작업 브랜치 (요청문에 이름을 옮겨 적지 않는다 — lint `no-hardcoded-branch-name`) |
| **판정 대상 코드** | **`743f65bead671bf353ce38027c2e8e457738ec08`** (RUN_SCOPE 를 마지막으로 건드린 커밋 — **64차와 같다**) |
| `source_digest` (RUN_SCOPE `src/ tools/ configs/ scripts/ run.sh requirements*.txt`) | **`e9ee7475dea7de1d`** — **64차와 한 글자도 다르지 않다** |
| 직전 판정 | 64차 **NO-GO** — P1 2 (N1·N2) · P2 1 (E2-R). 리뷰어 제목은 "63차 묶음 5 — 방어적 코드·회귀 검토", 우리 원장 번호로 **64차** |
| 이번 라운드 | 접수 3건 **전부 코드에서 닫음** + 보정 1건(우리가 스스로 찾음) + 신고 8건 유지 |
| 접수·대응 원장 | `docs/08_REVIEW_RESPONSE.md` §79(접수) · §80(대응) · 작업 상태 `docs/GATE64_WORKING_STATE.md` |

### ★ 이 라운드의 가장 중요한 사실 — **과학 코드 identity 가 안 움직였다**

64차 발견 셋의 고침은 **전부 RUN_SCOPE 밖**에 있다:

| 발견 | 고친 파일 | RUN_SCOPE? |
|---|---|---|
| N1 (P1) | `docs/22p_gap/mutation_replay.py` | **밖** |
| N2 (P1) | `docs/22p_gap/mutation_replay.py` | **밖** |
| E2-R (P2) | `tests/test_gate63_defensive.py` · `tests/test_gate64_defensive.py` | **밖** |

그래서 **`source_digest` 가 `e9ee7475dea7de1d` 그대로이고 기존 산출물이 무효화되지
않았다.** 재생성 비용(~28분 + 10시간)을 쓰지 않았다는 뜻이고, 동시에 **이 라운드는
과학 값을 하나도 다시 계산하지 않았다**는 뜻이다.

⚠ 그러므로 **`source_digest` 만 보면 이 라운드가 보이지 않는다.** 판정에 반드시 봐야
할 파일 둘은 RUN_SCOPE 밖이다:

- `docs/22p_gap/mutation_replay.py` — 증거층 + 변이 등록부의 **정본** (N1·N2)
- `tests/test_gate64_defensive.py` · `tests/test_gate63_defensive.py` — 회귀 (E2-R)

> **fetch 는 브랜치 head 로 해 주기 바란다.** 요청문은 자기가 담길 커밋 SHA 를 적을 수 없다.
>
> ```
> git fetch origin <하드룰 1 의 브랜치> && git checkout FETCH_HEAD
> cd degradation-degeneracy
> python3 -c "import sys; sys.path.insert(0,'.'); from src.io import source_digest; print(source_digest())"
> # → e9ee7475dea7de1d 이어야 한다. 아니면 그 자체가 발견이다.
> git log --oneline 743f65b..HEAD -- src tools configs scripts run.sh requirements*.txt
> # → 출력이 비어야 한다. 비지 않으면 위 표가 거짓이다.
> ```

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

64차 리뷰어가 명시했다: **"이 세 건만 수정해도 본 실행 GO 가 자동으로 되지는 않는다."**
그 문장을 그대로 받는다. 아래는 신고이지 종결이 아니다.

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | **미착수** (49차부터 **열여섯 라운드째**) |
| trusted launcher 의 source 측정 | **미착수** |
| **P0-4** typed 보존 영수증 **소비** | **부분** |
| 변이 증거의 **독립 replay** | **미착수** — 이번에도 checker 가 스스로 재생하지 않는다 |
| 묶음을 **immutable content-addressed object** 로 먼저 게시 | **미착수** |
| 실행 class 5종 중 3종 미구현 · 등록부 삭제 절차 | **미착수** |
| baseline·sweep1d·wsweep 계획 gate · 실물 object-lock adapter · power-loss 모델 · publisher 전용 OS principal | **미착수** |
| 외적타당도 **#50** (`truth_provenance` 를 기계 계약에) | **미착수** |

---

## 1. 발견별 대응

| # | 리뷰어 반례 | 원인 | 고침 | 회귀 |
|---|---|---|---|---|
| **N1** (P1) | user site 가 꺼진 정상 venv 에서 child `usercustomize` `<absent>` vs parent digest → **정상 영수증 거부** | 부모가 `usercustomize` 를 **무조건** 찾았다. Python 은 `site.ENABLE_USER_SITE` 가 참일 때만 자동 import 한다 — **찾을 수 있는 모듈 ≠ startup 이 실행한 모듈** | `_parent_user_site_enabled()` 가 **재생이 실제로 띄우는 것과 같은 실행 파일·같은 env** 로 인터프리터를 하나 띄워 `site.ENABLE_USER_SITE` 를 묻는다. 비활성이면 양쪽 `<absent>`, 활성이면 바이트 대조. child 의 자기 증언은 **안 쓴다**(믿으면 세탁 통로). 부모 프로세스에서 읽지 않는다(pytest 가 띄운 프로세스라 조건이 다를 수 있다). 못 재면 **fail-closed**(`_ReplayError`) | `usercustomize-follows-the-startup-activation-g64` |
| **N2** (P1) | 표준 zipimport 의 정상 package 를 OS 파일로 열려다 `[Errno 20] Not a directory` → 영수증 전체 `failed` | child 의 customization 해시만 `_d(f)` — **같은 origin 을 두 규칙으로 읽고 있었다** | customization 도 `_hash_origin`: 파일이면 읽고 아니면 loader 의 `get_data` 에 묻는다 (62차 P1-4 가 `loaded` 루프에 넣어 둔 규칙 그대로). 읽기 실패는 여전히 `_Unreadable` → 섹션 `failed` | `customization-reads-origins-like-the-rest-g64` |
| **E2-R** (P2) | 원장 §78 은 "잡으면 True · 놓으면 False" 인데 **커밋된 시험에는 True 만** | 문구가 시험보다 강했다 | 음성 대조군을 커밋한다. `release_run_lock` 이 token 의 `dir_fd` 를 닫고 lock 파일을 지우므로 **놓은 뒤에는 token 으로도 지워진 경로로도 열 수 없다** — 그 사실부터 시험이 적는다 | `the-probe-control-asserts-both-directions-g64` |

**왜 기존 ZIP 회귀가 N2 를 놓쳤나**: 62차 시험은 일반 디렉터리의 `sitecustomize` 가
ZIP 안의 **다른** 모듈을 import 한다 — 그 모듈은 `loaded` 루프를 타서 통과했다.
customization **자신**이 ZIP 안에 있는 축은 아무도 안 돌렸다.

### RED 관측 (고치기 전, 눈으로 봤다)

```
tests/test_gate64_defensive.py 첫 실행 → 6 failed · 4 passed
```

통과한 넷은 "바뀌지 않는다" 를 재는 **대조군**이다: 일반 파일 customization ·
일반 customization 이 가져오는 ZIP module · 활성 user site 의 바이트 대조 ·
진짜 읽기 실패는 여전히 `failed`.

### 변이 축

```
usercustomize-follows-the-startup-activation-g64   MR    N1
customization-reads-origins-like-the-rest-g64      MR    N2
the-probe-control-asserts-both-directions-g64      G63T  E2-R

--check-preimages   모든 변이 지점이 정확히 한 번 나타난다
-k g64              3/3 물었다 (call 단계) · EXPECT 일치
```

---

## 2. 우리가 스스로 찾은 보정 — **증인이 문맥 의존이었다**

`-k g64` 3/3 과 방어 시험 단독 GREEN 을 보고 넘어갔는데 `tests/test_evidence_layer_58.py`
셋이 빨갰다. N1 축의 증인으로 **production 의 `_ReplayError` 문구를 그대로** 썼던 것이
원인이다 — 그 문구에는 부모가 resolver 로 찾은 파일의 digest 가 들어 있고, 그 값은
pytest 를 어떻게 띄우느냐(어느 `usercustomize` 를 먼저 찾느냐)에 따라 달라진다.
`--emit-expect` 로 관측한 문구와 증거층 sandbox 재생에서 나온 문구가 갈렸다.

**62차 ① 의 `unfiled=22`, 63차 ① 의 같은 자리에 이어 세 번째다.** 앞의 둘은 "개수를
빼라" 로 끝났지만 이번 것은 더 넓은 교훈이다 — **production 메시지는 환경을 담도록
만들어져 있고, 증인은 담으면 안 된다.** 시험이 자기 고정 문구로 실패하게 바꿨다.

**그리고 첫 전수 실행이 무효였다.** 회귀가 도는 **중에** HEAD 가 움직여
(`d396f8a` → `f1ef8e2`) 9 건이 빨갰다 — 그중 셋이 위 결함이고 여섯은 트리 이동이다.
**회귀가 도는 동안 커밋하지 않는다** (이 저장소에서 두 번째로 겪었다).

재관측 뒤: `-k g64` **3/3** · `tests/test_gate64_defensive.py` **10 passed** ·
`tests/test_evidence_layer_58.py` **8 passed**.

---

## 3. 검증 — 방금 실행

<!-- FILL: 전체 pytest 결과 (이 요청문을 보내기 전에 실측으로 채운다) -->

```
$ python -m pytest tests/ -q
<대기: 실행 중>
```

**환경 안내** (62·63·64차 리뷰어 환경에서도 같은 이유로 빨갰던 것들 — 코드 발견이 아니다):

- 전체 회귀는 `pybamm`·`tqdm`·`pyarrow` 를 요구한다 (`requirements.txt`).
- `tests/test_docs_lint.py::test_a_smoke_run_cannot_be_promoted_to_a_canonical_report`
  는 **작업 트리에 `results/grid_fit_v4` 가 있어야** 초록이다 (gitignored 실물 산출;
  fresh clone 에는 없다).
- `test_fit_phase_receipt_is_written_while_the_kernel_lock_is_held` 는 **clean
  커밋에서만** 돈다 (dirty 면 skip + 사유 출력) — 진짜 producer 가 git 상태를 적고
  fit 의 producer 검증(F74/F85)이 dirty worktree 곡선을 거부한다. detached clean
  worktree 에서는 돈다.

---

## 4. 이번 라운드가 스스로 신고하는 것 (8건 — 63차 ①–⑧ 유지)

**①** 영수증 frame 의 한계 — child 의 startup 코드 전부는 못 막는다. 부모 대조 층이
N1·N2 로 Python resolver 와 **같은 규칙**이 됐지만, 위조자가 자기 해시를 정직하게 적으면
여전히 못 막는다. 종결은 §0 의 **독립 replay** 다.

**②** 승격이 막는 것은 "등록되지 않은 상태" 이지 "과거 상태로의 되돌림" 이 아니다.

**③~⑧** 63차 요청문 §신고 ③–⑧ 를 그대로 유지한다 (이번 라운드가 건드리지 않았다).

**⑨ 새로 신고 — N1 의 fail-closed 가 새 거부 경로를 만든다.** 조건을 못 재면
`_ReplayError` 다. 이는 의도이지만, **인터프리터를 하나 더 띄울 수 없는 환경에서는
정상 영수증도 거부된다.** 우리 환경에서는 재현되지 않았다 — 리뷰어 환경에서 이 축을
쳐 주기 바란다. 반례가 나오면 그것이 이 라운드의 발견이다.

---

## 5. 리뷰어에게 묻는 것

1. **N1 의 "같은 실행 파일·같은 env" 가 충분한가.** 재생이 띄우는 프로세스와 우리가
   조건을 재려고 띄우는 프로세스가 **같은 조건**이라는 보장이 어디서 오는가.
   `PYTHONNOUSERSITE`·`-s`·`-S`·venv `pyvenv.cfg` 의 조합에서 갈리는 반례가 있는가.
2. **N2 의 `get_data` 위임이 모든 loader 에 있는가.** `importlib.abc.ResourceReader`
   가 없는 서드파티 loader 에서 `_Unreadable` 로 떨어지면 정상 영수증이 `failed` 가 된다 —
   N2 와 같은 형태의 반대편 결함이다.
3. **E2-R 음성 대조군이 진짜 음성인가.** lock 을 놓은 뒤 열 수 없다는 것을 시험이
   "놓쳤다" 로 읽는지 "잡았다" 로 읽는지, 구현을 망가뜨려도 실패하는지.
4. **증인 문맥 의존이 세 번째다.** production 문구를 증인으로 쓰지 말라는 규칙을
   기계로 강제할 수 있는가 — 현재는 사람이 지키는 규율이다.

**판정 요청**: 위 셋이 닫혔는지, ⑨ 의 fail-closed 가 새 결함인지.
**§0 의 GO 전제는 이 라운드가 닫지 않는다** — GO 를 묻지 않는다.
