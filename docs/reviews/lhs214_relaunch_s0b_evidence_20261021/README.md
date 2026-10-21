# 증거 — 보충 영수증 selftest S0b 의 봉인 지문 기대 (2026-10-21 · 1저자 10-21 Q1 · LHS214 다시 발사 묶음 §6 Q3)

- 근거: 묶음 문서 `docs/reviews/lhs214_relaunch_package_20261020.md` §1-3 (비준 사본에서 `scripts/supp20_input_receipt.py --selftest` 121/122 · 실패 S0b) · §6 Q3 (가) ·
  1저자 10-21 Q1 (*비준 커밋 앞 작은 코드 커밋*).  기준 트리 = `a76f59d0d` (본 가지 머리).
  ⚠ 정정 10-21 (사전 리뷰 PRE-LHS-06): §1–§6 의 로그 = 작업 트리 (부모 `a76f59d0d` = 그 작업 트리를 만든 때의 본 가지 머리) 에서 만들었다 · 본 가지 판 = 메인 cherry-pick (`fe23f2b83` · 부모 `a69963967`) —
  영수증 도구 · 두 등록 · 실행기는 `a76f59d0d` ↔ `a69963967` 에서 바이트 같다 (`git diff --quiet` rc 0 · 그 사이 바뀐 파일 = 이 넷 밖).  §7 = 10-21 S0b 시험 보강 (본 가지 `7f99be67c` 위 작업 트리 · 메인 반영 = `<수정 커밋 · 메인 반영 뒤 채움>`).
- 기계 = 이 컨테이너 (Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · networkx 3.6.1) — WSL 아님.  selftest = `nice -n 19` · BLAS 한 스레드 · 이 작업에서 한 번에 하나
  (10-21 06:45 뒤의 m2 는 기계 전체 잠금 `flock` 아래 — 그 전 실행은 잠금 없이).
- 이 폴더 = 결과 기록만.  도구 판정 (receipt · R0 · D1 · E2 · F5 · G5) · 봉인 32 · 등록 문서는 이 커밋에서 바뀌지 않는다.
  (§7 보강도 도구 판정 · 봉인 32 무변경 · 그 문서 커밋은 두 등록의 §9-9 · §9-4 인용 한 줄씩만 고친다 — 사전 리뷰 PRE-LHS-09 · 기계 값 칸 · §3 · §5 무변경.)

## 1. 결함

`_selftest` 의 S0b 가 등록 §3 `code_fp` 를 앞자리 상수 `e8b2496b…` 로, 대기 선언을 앞자리 상수 `2149f873…` 로 기대했다 (`a76f59d0d` 판 619–623 줄 · 그 검사 이름의 꼬리 *"커밋마다 갱신"*).
비준판 문안 (묶음 §1-4 · §1-5 diff) 을 넣은 정상 비준 상태 (등록 §3 = 체크아웃 지문 `2149f873…` · 대기 선언 없음) 에서 S0b 하나만 실패한다 — **121/122** (`tests/old_ratified.log`).
도구가 아니라 시험 기대의 결함이다 (같은 상태의 컨테이너 범위 영수증 = rc 0 · 실패 칸 없음).

## 2. 고친 것 (`scripts/supp20_input_receipt.py` 의 `_selftest` 안만)

| 무엇 | 내용 |
|---|---|
| `s0b_fp(reg, base, base_probs)` (새) | 상수 없음 — 상태 (`fp_state`) 가 정한 지문 = 체크아웃 `code_fp` 64 자리 전체 (registered = 등록 §3 · pending = 대기 선언) · registered 면 대기 선언 없음 · 보충 등록의 (활성 §3 · 대기 선언) = 194 등록 (`docs/reviews/lhs_network_batch_registration_20261007_g2.md`) 의 값 — 둘 다 도구 함수 `registration_values` 로 읽음 (보충 §3 *"= 194 와 같다"*) · 194 쪽 봉인 지문 문제 (§3 값 둘 · 대기 값 둘 · 대기 = 등록) 면 거짓 (문제면 값이 None 이라 None = None 으로 통과시키지 않는다) · undeclared = 거짓 — ⚠ 정정 10-21 (`SUPR-04` · 사전 리뷰 PRE-LHS-02): 이 판은 **194 쪽** 문제만 받았다 — 보충 쪽 대기 값 둘 · 대기 = 등록 은 값이 None 이 되어 None = None 으로 참 (*"registered 면 대기 선언 없음"* 이 보충 쪽에서 성립하지 않았다 · 실물 자리 합계는 S0 의 R0 가 막음) → 보강 = §7 |
| S0b | §2 네 값 (케이스 20 · ids `991cf115…` · raw `a7aaa3c8…` · 코호트 TSV `69d3f913…` 앞자리 — 등록 입력 집합 · L214 개정의 *바꾸지 않는 것*) 은 그대로 + `s0b_fp` |
| S11g (새 검사) | `s0b_fp` 를 실물 상태와 무관하게 일곱 꼴의 등록 사본 쌍 (보충 · 194 · 지문 토큰만 바꾼 `reg_variant` · 도구 함수로 읽음) 에 — 참 = registered · pending / 거짓 = 보충만 비준 (194 = 대기) · pending 인데 194 등록 §3 다름 · 비준 + 남은 대기 · 194 대기 값 둘 · 선언 없음 |
| `reg_variant(…, src=None)` | 바탕 글 인자 (기본 = 보충 등록 실물 — 옛 호출 그대로) |
| 그대로 | 모듈 최상위 문 59 중 바뀐 것 = `_selftest` 하나 (AST 비교 · 끝 `if __name__` 블록은 줄 번호만 다르고 내용 같음) — receipt · registration_values · 대조 칸 · 판정식 · CLI |
| 봉인 | 이 파일은 `CODE_FILES` (봉인 32) · `HANDOVER_FILES` 밖 → `code_fp(code_hashes())` = `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` 그대로 (다시 잼) |

도구 sha256: 고치기 전 `2c7e0b81dbe81d0518e27c8e1781959b9cc983509a1ce66001028faa3768a2f9` → 고친 판 `3d6110be24d24bf91ad1e71232a2e5dad580cf95178d6135b13aa6ca6de6f950`.

## 3. 시험 — 보충 영수증 `--selftest` (행 = 도구 판 × 등록 문서 상태)

| 도구 판 (sha256 앞 16) | 등록 문서 | 상태 | 결과 | 실패 | 기록 |
|---|---|---|---|---|---|
| 고치기 전 (sha256 `2c7e0b81dbe81d05…`) | 커밋된 문서 | pending | 122/122 | — | `tests/old_pending.log` |
| 고치기 전 | 비준 사본 (둘) | registered | **121/122** | S0b | `tests/old_ratified.log` (재현) |
| 고치기 전 | 194 만 비준 | pending | 122/122 | — (옛 S0b 는 194 를 보지 않는다) | `tests/old_194_only.log` |
| 새 시험 + 옛 S0b 식 (sha256 `a06d4298726090f0…` — 그 판의 바이트는 남기지 않았다 · ⚠ 정정 10-21 (사전 리뷰 PRE-LHS-06): 같은 꼴을 다시 만든 판 = `tests/oldexpr_s0b.patch` · 수 = §7) | 커밋된 문서 | pending | 122/123 | S11g (registered · pending 꼴 = 거짓) | `tests/before_pending.log` |
| 새 시험 + 옛 S0b 식 | 비준 사본 (둘) | registered | 121/123 | S0b · S11g | `tests/before_ratified.log` |
| **고친 판** (sha256 `3d6110be24d24bf9…`) | 커밋된 문서 | pending | **123/123** | — | `tests/after_pending.log` |
| **고친 판** | 비준 사본 (둘) | registered | **123/123** | — | `tests/after_ratified.log` |
| 고친 판 | 보충만 비준 | registered | 122/123 | S0b (보충 ≠ 194) | `tests/after_supp_only.log` |
| 고친 판 | 194 만 비준 | pending | 122/123 | S0b (보충 ≠ 194 — 새 엄격 · §5) | `tests/after_194_only.log` |

변이 — 고친 판의 `s0b_fp` 가드를 하나씩 끈 판 (`if False and …` · 그 밖 바이트 같음):

| 변이 | 등록 문서 (상태) | 결과 | S11g 이 잡은 꼴 (참으로 뒤집힘) | 기록 |
|---|---|---|---|---|
| m1 남은 대기 검사 끔 | 커밋된 문서 (pending) | 122/123 | ratified_pending_left | `tests/mut_m1_no_leftover_pending.log` |
| m2 두 등록 대조 끔 | 커밋된 문서 (pending) | 122/123 | supp_only_ratified · pending_base_differs | `tests/mut_m2_no_cross_doc.log` |
| m3 194 문제 검사 끔 | 비준 커밋 트리 (registered) | 122/123 | base_pending_conflict | `tests/mut_m3_no_base_problems.log` |
| m4 undeclared 거짓 끔 | 비준 커밋 트리 (registered) | 122/123 | undeclared | `tests/mut_m4_undeclared_ok.log` |

m3 · m4 는 이 폴더를 만든 코드 커밋 **뒤** 비준 커밋 트리에서 돌렸다 (S11g 은 등록 사본 쌍을 스스로 만들어 실물 상태와 무관 — 위 표의 고친 판 pending · registered 둘 다 S11g 통과).
⚠ 정정 10-21 (`SUPR-05` · 사전 리뷰 PRE-LHS-03): 이 네 변이는 `s0b_fp` 의 네 if 가드만 겨눴다 — 교차 대조의 대기 반쪽 (§3 만) · 64 자리 비교 (앞 12 자리 · 교차 대조 · 상태 판정) · S0b 배선 (`REG194` = 보충 문서 · 194 문제 안 넘김 · 판정식이 `fp0_ok` 안 씀) 의 변이 여섯은 이 판에서 123/123 으로 살았다 → 보강 = §7.
비준 커밋 트리의 고친 판 그대로 = 123/123 (`tests/final_ratified_commit.log` · 상태 registered).

- "비준 사본" = 묶음 §1-4 · §1-5 diff (`⬜(날짜)` → `10-21 ·`) 를 작업 트리에 `git apply` 한 문서 — 다음 비준 커밋과 같은 diff · 돌린 뒤 `git checkout` 으로 되돌림.
  "보충만 · 194 만 비준" = 그 diff 하나만.
- "새 시험 + 옛 S0b 식" = 고친 판에서 `s0b_fp` 본문만 옛 S0b 식 (앞자리 상수 둘) 으로 바꾼 판 (그 밖 바이트 같음 · 시험 먼저의 "고치기 전") — 작업 트리에 잠시 넣고 돌린 뒤 되돌림.
- 시간 = 32–52 s (잠금 대기 제외 · 같은 기계 부하에 따라).

## 4. 봉인 · 범위 대조 (이 커밋 · 이 컨테이너)

- 코드 커밋이 바꾼 파일 (`a76f59d0d` 대비) = 이 도구 · 재고 대장 (`docs/reviews/selftest_inventory.tsv` 의 이 도구 행) · 이 폴더 (README + 로그 11 — m3 · m4 · 비준 커밋 트리 로그 셋과 이 README 의 그 행들은 뒤 문서 커밋).
  ⚠ 정정 10-21 (사전 리뷰 PRE-LHS-06): 기준 = 본 가지 코드 커밋 `fe23f2b83` 의 **부모 `a69963967` 대비 = 14 파일** (이 도구 · 재고 대장 · README · 로그 11 — `git diff --name-only a69963967 fe23f2b83` 다시 셈) · 옛 표기 *"`a76f59d0d` 대비"* = 그 사이 메인 커밋까지 81 파일.
- 대조 핀 `34713ac96` (Codex 10-20 검토 핀) → 이 커밋: `CODE_FILES` 32 · 인계 도구 2 · 배포 빌더 · 실행기 · 스모크 · 두 등록 문서 = `git diff --quiet` rc 0 (바이트 같음).
- 고친 판으로 잰 컨테이너 범위 영수증: 커밋된 등록 문서 (pending) = rc 1 · 실패 칸 [D1] · 비준 사본 = rc 0 · 실패 칸 없음 — 고치기 전 판과 같다 (도구 판정 무변경).

## 5. 한정

- **새 엄격** — 고친 S0b 는 두 등록이 같은 상태 · 같은 값일 것을 요구한다: 194 만 비준하고 보충은 그대로인 트리에서 옛 판 122/122 · 고친 판 S0b 실패 (§3 표).
  두 등록은 한 봉인이다 (보충 §3 *"= 194 와 같다"* · 묶음 §1 diff 가 둘을 함께 바꾼다).
- 두 문서가 **같은 엉뚱한 값으로 함께** 바뀌면 고친 S0b 의 두 등록 대조는 그것을 못 잡는다 (옛 판의 앞자리 상수는 잡았지만 정상 비준을 막았다).
  registered 상태 (발사 대조가 통과할 수 있는 유일한 상태) 에서는 기준이 체크아웃 지문 64 자리 전체라 엉뚱한 값 = undeclared = 실패 · pending 상태는 발사 대조 (D1 · E2 · F5 · G5) 가 이미 막는다.
  ⚠ 정정 10-21 (사전 리뷰 PRE-LHS-04): 기준이 체크아웃 지문이므로 **코드와 두 등록이 같은 새 값으로 함께** 바뀐 재봉인은 S0b 가 통과시킨다 (기준이 같이 움직인다 · 체크아웃과 독립인 기대값을 잃었다) — 막는 자리 = 묶음 §5 손 대조 (code_fp 전체 값) · 영수증 D1 · E2 · F5 · G5 (등록 §3 값만) · 새 §3 값의 Codex 확인 · 1저자 비준 (확인 요청서 §6).
- §2 네 값의 앞자리 상수는 그대로다 (등록 입력 집합 — §9-3 *바꾸지 않는 것*).
- WSL 실측 아님 — 사전 점검 2 단계에서 다시 잰다.  기대 = 비준 커밋 뒤 **123/123** (묶음 §1-6 2 단계 · 명령 주석과 §4 결과 전 기대 단계 2 의 *"122/122"* 는 이 커밋 전 예상 — 새 검사 S11g 하나만큼 다르다).
  ⚠ 정정 10-21 (S0b 시험 보강 · §7): 보강 뒤 기대 = **124/124** (검사 S11h 하나 더 · 묶음 같은 자리 정정 표지).

## 6. 다시 돌리기 (리포 뿌리)

```bash
python3 scripts/supp20_input_receipt.py --selftest | tail -1                       # 고친 판 · 커밋된 문서
# 비준 사본: 묶음 문서 §1-4 · §1-5 의 ````diff 블록 둘을 떼어 ⬜(날짜) → '10-21 ·' 로 바꾼 뒤
git apply ratify_194.patch && git apply ratify_supp20.patch
python3 scripts/supp20_input_receipt.py --selftest | tail -1                       # 123/123
git checkout -- docs/reviews/lhs_network_batch_registration_20261007_g2.md docs/reviews/lhs_network_batch_registration_20261012_supp20.md
# 고치기 전: git show a76f59d0d:scripts/supp20_input_receipt.py > /tmp/old.py — 작업 트리의 scripts/ 에 잠시 넣어 돌린다
#            (도구가 자기 자리 (scripts/) 기준으로 리포 파일을 읽는다 — 다른 폴더에서 돌리면 경로가 어긋난다)
```
