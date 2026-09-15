# 64차 게이트 리뷰 작업 상태 (정본)

판정: **NO-GO** (2026-09-15 접수 · 리뷰어 제목은 "63차 묶음 5 — 방어적 코드·회귀
검토" 이나 우리 원장 번호로는 **64차**다 — `GATE63_REQUEST.md` 에 대한 답).
요청한 코드 `743f65bead671bf353ce38027c2e8e457738ec08` · 검토 HEAD
`6f8dcc22b7385233f7d215c4af5371f99317fbcb` · `source_digest e9ee7475dea7de1d`
(리뷰어 실측 일치, RUN_SCOPE diff 빈 출력). 새 **P1 2 · P2 1 = 3건**.

새 P0 없음. 접수 원장은 `docs/08_REVIEW_RESPONSE.md` §79, 대응은 §80.

## 발견 원장

| ID | 무엇이 틀렸나 | 자리 | 상태 |
|---|---|---|---|
| N1 (P1) | 부모가 `usercustomize` 를 **무조건** 찾는다 — Python 은 `site.ENABLE_USER_SITE` 가 참일 때만 자동 import 한다. user site 가 꺼진 정상 venv 에서 child `<absent>` vs parent digest → **정상 영수증 거부** | `mutation_replay.py` `_parent_customization_view` | 코드 ✔ |
| N2 (P1) | child 의 customization 해시만 `_d(f)` — 표준 zipimport 의 정상 package 를 OS 파일로 열려다 `[Errno 20] Not a directory` → 영수증 전체 `failed` | `mutation_replay.py` `_env_facts_measured` | 코드 ✔ |
| E2-R (P2) | 원장 §78 은 "잡으면 True · 놓으면 False" 인데 **커밋된 시험에는 True 만** 있다 | `tests/test_gate63_defensive.py` | 코드 ✔ |

RED 관측: `tests/test_gate64_defensive.py` 첫 실행 **6 failed · 4 passed**.
통과한 넷은 "바뀌지 않는다" 를 재는 대조군이다 (일반 파일 customization · 일반
customization 이 가져오는 ZIP module · 활성 user site 의 바이트 대조 · 진짜 읽기
실패는 여전히 `failed`).

## 한 줄 요약

**찾을 수 있는 모듈 ≠ startup 이 실행한 모듈** (N1) · **같은 origin 을 두 규칙으로
읽고 있었다** (N2) · **문구가 시험보다 강했다** (E2-R). 셋 다 정상 입력에서 우리
층이 거부하거나 실패한 것이고 위조 성공이 아니다 — 고칠 방향은 "덜 본다" 가 아니라
"같은 규칙으로 본다" 다.

## 고침

### N1 — 활성 조건을 부모가 **직접 잰다**

`_parent_user_site_enabled()` 가 재생이 실제로 띄우는 것과 **같은 실행 파일·같은
env** 로 인터프리터를 하나 띄워 `site.ENABLE_USER_SITE` 를 묻는다. 비활성이면
`usercustomize` 는 양쪽 `<absent>`, 활성이면 지금까지처럼 바이트 대조.

- child 의 자기 증언은 **안 쓴다** — 믿으면 세탁 통로가 된다.
- 부모 프로세스에서 읽지 않는다 — pytest 가 띄운 프로세스라 child 와 조건이 다를 수 있다.
- 못 재면 fail-closed(`_ReplayError`): 조건을 모르면 대조 규칙을 정할 수 없다.

### N2 — customization 도 `_hash_origin`

파일이면 읽고 아니면 loader 의 `get_data` 에 묻는다 (62차 P1-4 가 `loaded` 루프에
넣어 둔 규칙 그대로). 읽기 실패는 여전히 `_Unreadable` → 섹션 `failed` 다.

**왜 기존 ZIP 회귀는 통과했나**: 62차 시험은 일반 디렉터리의 `sitecustomize` 가
ZIP 안의 **다른** 모듈을 import 한다 — 그 모듈은 `loaded` 루프를 타서 통과했다.
customization **자신**이 ZIP 안에 있는 축은 아무도 안 돌렸다.

### E2-R — 음성 대조군을 커밋한다

`release_run_lock` 은 token 의 `dir_fd` 를 닫고 lock 파일을 **지운다**. 그래서 놓은
뒤의 관측은 token 으로도 지워진 경로로도 열 수 없다 — 그 사실부터
`assert not p.exists()` 로 고정하고, 같은 자리를 되살려 경로 탐침
(`_kernel_lock_held_at`)이 False 를 내는 것을 관측한다. 양성 쪽은 token 판과 경로
판 **둘 다**로 True.

관측 시점 문구도 좁힌다: 이 시험이 보는 것은 `real_phase_done` **호출 직전**의 커널
상태, 반환 뒤의 claim 파일, release 직전의 커널 상태 셋이다. "영속 쓰기의 바로 그
순간" 이라고 쓰지 않는다. 재독 성공은 power-loss durability 의 증거가 아니다.

### 후속 정리 (발견 아님)

§0 ⑦ 의 xfail 을 `raises=shutil.SameFileError` 로 좁혔다.

## 변이 등록부 (64차)

새 축 3 (`-g64`). 셋째는 `tests/test_gate63_defensive.py` 를 겨냥한다 —
`test_docs_lint.py`(`TDL`)에 이미 선례가 있는 모양이다.

```
usercustomize-follows-the-startup-activation-g64   MR    N1
customization-reads-origins-like-the-rest-g64      MR    N2
the-probe-control-asserts-both-directions-g64      G63T  E2-R

--check-preimages   모든 변이 지점이 정확히 한 번 나타난다
-k g64              3/3 물었다 (call 단계) · EXPECT 일치
```

첫 관측의 증인 둘이 tmp 경로와 기계별 digest 를 담고 있어 시험 문구에서 걷어냈다
(62차 ① · 63차 ① 회차와 같은 교훈). 증인 문구는 **기계 독립**이어야 한다.

## 남는 것

§0 의 독립 GO 전제(producer 결속 · trusted launcher · typed 보존 영수증 소비 ·
독립 replay · immutable bundle)는 이번 묶음이 닫지 않는다. 리뷰어도 "이 세 건만
수정해도 본 실행 GO 가 자동으로 되지는 않는다" 고 명시했다.
