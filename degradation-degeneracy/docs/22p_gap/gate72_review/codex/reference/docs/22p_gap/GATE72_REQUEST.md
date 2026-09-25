# 72차 게이트 리뷰 요청 — 71차 잔여 둘(E3-R · E9-R)에 대한 답 · **한정 실행 GO 재요청**

> **상태: 확정 (2026-09-25).** 71차 회신(한정 GO 보류 — E3-R [P1] 소비 계약 · E9-R [P2] 재개 명세)의 §5 "다음 회신에 필요한 최소 자료" ①②③ 에 답한다.
> 범위는 리뷰어가 정한 대로 **E3-R + E9-R + 문구 정정** 이다. E1/E2/E4 전면 구현·과거 class 정리는 요구되지 않았고 하지 않았다.
> 이 요청은 여전히 **한정 실행 GO** 를 묻는다 (무제한 독립 GO 아님). 계획 항목(prospective)은 아직 쓰지 않았다 — 리뷰어: "지금 prospective 계획 항목을 작성/커밋하거나 본 실행을 시작하라는 승인이 아니다."

## 판정 대상 (이 블록이 정본이다)

| 항목 | 값 |
|---|---|
| 요청문 커밋 | `(이 파일을 담은 커밋 — 발송문에 실측해 적는다)` (브랜치 head SHA 와 함께, 커밋 뒤 실측) |
| **판정 대상 코드** | **`82854571d0240951c929d4a9b90260e53ca38e88`** — RUN_SCOPE 마지막 변경 커밋 (71차 E3-R, `tools/preserve.py`) · `source_digest` **`518d4f63076b77e3`** (71차 대상 `87642956` · `b705a21a1237ec73` → E3-R `82854571` · `518d4f63076b77e3`). 그 뒤 커밋은 영수증·원장·문서뿐 (RUN_SCOPE diff 0) |
| 리뷰 원자료 | 71차 패키지 `docs/22p_gap/gate71_review/` (zip `e65ab85f…`, MANIFEST 37/37) — `-text !eol` 규칙 먼저 커밋 |
| 발견 원장 | `docs/08_REVIEW_RESPONSE.md` §94(접수) · §95(E3-R 대응 + E9-R/D6~D9) · 작업 상태 `docs/GATE70_WORKING_STATE.md` |
| 새 시험 | `tests/test_gate71_defensive.py` 14 node (RED 12 → GREEN 14) · 변이 3건 (`mutation_replay.py -k g71`) |

## §0 71차 잔여에 대한 답

| ID | 71차 판정 | 이번 상태 | 근거 |
|---|---|---|---|
| **E3-R** | P1 미종결 — 소비자가 비교 쌍·실제 일치·source fits·복원 자리를 안 봄 | **닫음** — `_receipt_output_pair()` (역할별 닫힌 키 · 역할마다 하나 · hex64 · 같은 schema·canonicalizer 의 짝 필수 · semantic digest **실제 일치** — 생산자 `_outputs_agree` 와 같은 판단을 소비 쪽에서 다시) · `rescored.source_file_sha256 == bundle.fits_sha256` · identity 7 값 hex16 · `_assert_receipt_bound_to_bundle()` (묶음 `restore_map.run_dir` == `restore.run_dir_relative` · `sealed_summary.file_sha256` == 묶음 `degeneracy_summary.yaml` 바이트) · attach 가 원장 `evidence.out` 과 대조. **fixture 를 생산 계약으로 되돌렸다** (두 산출 한 쌍 · restore_map · 봉인 summary). 거부 시 원장 불변(모든 부정 시험이 바이트 대조) | §95 · `test_gate71_defensive.py::test_g71_e3r_*` 13 node: 양성 1(e3r_00) · R04 · R05(+05b 중복 역할) · R06 · R09 · R07(+07b 원장 out · +07c 지도 없음) · 봉인 summary sha(e3r_11) · R08 · R10 · 실물 양성(e3r_12) · 변이 3 (`-k g71` 3/3) |
| **E9-R** | P2 — "같은 명령" 은 chunk 재개가 아님 | **명세 고정 (D6):** 실패 **즉시 정지** → 사람이 같은 plan/token/`source_digest`(`precheck_leg_run` `kind == resume`) 와 부분 산출(chunk 기록·`fit_completed.jsonl`)을 확인 → **명시적 재개 argv 정확히 1회** `./run.sh --mode all --leg grid_fit_v5 --config configs/grid_fine.yaml --nproc "$(nproc)" --out results/grid_fit_v5 --resume` → 2회째 실패는 재승인(새 계획 항목). `--resume` 이 모든 실패를 복구한다고 보증하지 않는다 | `GATE71_REQUEST.md` §2 E9-4 (취소선 정정) · 원장 §93 같은 정정 · 이 요청문 §2 |
| 문구 정정 | 차단 항목 아님 | **D7** 실행 checkout = prospective 항목을 커밋한 **최종 승인 HEAD** (코드 기준 `82854571` 과 RUN_SCOPE diff 0 을 함께 적는다) · **D8** `unset CANONICAL_RUN LEG` 명시 · **D9** E4 표본 = premise 4 + g70 4 + g71 3 = **11** 시나리오로 통일 · **E6** 격리 tree 에 `requirements*.txt` 복사, `test_g71_e6_*` 가 자식 프로세스로 `source_digest` 동일을 잰다 | `GATE71_REQUEST.md` §2 · `tests/conftest.py` |
| E1/E2/E4 · E5 · E6(한정) · E7 · E8 · E10 · G70-N1 | 수용 (71차) | 변경 없음 — 다시 열지 않는다 | — |

## §1 결과 라벨 (71차 §1 그대로 — E4 수량만 정정)

> **실행 허용 범위:** 합의된 synthetic grid/fit 재실행 (E9-0), 계획 항목 `grid_fit_v5` (한정 GO 뒤 사람이 커밋 — 아직 없음).
> **코드/입력/실행 식별:** 판정 대상 `82854571d0240951c929d4a9b90260e53ca38e88` · `source_digest 518d4f63076b77e3` · config `configs/grid_fine.yaml` · OUT `results/grid_fit_v5` · 실행 checkout = 최종 승인 HEAD (RUN_SCOPE diff 0 to `82854571`).
> **현지 검증:** `python -m pytest tests/ -q` → 0 failed · 1869 passed · 2 xfailed (34:59) (rc 0) · `./scripts/smoke_e2e.sh` → rc 0 · `mutation_replay.py --check-preimages` 전 지점 1회 · `-k premise` 4/4 · `-k g70` 4/4 · `-k g71` 3/3.
> **E1:** projection producer 독립 결속 미검증. **E2:** 실행 source 자기 측정, 독립 launcher attestation 미구현. **E4:** 변이 보고서 일관성 검사 + 표본 replay 11 시나리오(우리 실행), 독립 replay 범위 = 리뷰어 정적 대조.
> **E6:** 이번 실행 권한 영역의 격리/배타 사용 근거 = 시험 authority 격리(RUN_SCOPE + requirements 복사 tree) + 운영 불변 검사 + 배타 운영 창(전후 snapshot, delta +2 기대); 과거 351 시험 레코드 이관은 별건.
> **execution_class / 보존 / validation / inference_role:** 실행 뒤 실제 값으로 채운다 (기대: canonical·sealed / full_bundle / current_validated / diagnostic).
> **archive / 복원 / retention:** archive_results.sh + make_receipt(empty-root 복원·재채점) 수행, `attach_bundle_evidence`(짝·일치·source fits·복원 자리·봉인 summary 결속) 수행; retention/object-lock/power-loss 는 **미수행·보증 안 함**.
> **실패 처리:** 실패 즉시 정지 · 명시적 `--resume` 1회 · 그 뒤 재승인.
> 이 한계는 더 강한 독립 provenance·외부 셀 타당성·미시험 내구성의 보증이 아니다.

## §2 실행 명세 — 71차 §2 (= 원장 §93) 에 D6~D9 정정을 얹은 것이 정본이다. 바뀐 줄만 여기 다시 적는다

```bash
# 실행 전용 checkout · 사람이 prospective 항목을 커밋한 최종 승인 HEAD (RUN_SCOPE diff 0 to 82854571) · clean tree
# 실행 중 커밋/pytest/smoke 금지 (E6-b 창)
unset CANONICAL_RUN LEG          # 상속된 환경변수를 명시적으로 지운다 — 보고서는 docs/RESULTS_grid_fit_v5.md 로
cd degradation-degeneracy
./run.sh --mode all --leg grid_fit_v5 --config configs/grid_fine.yaml --nproc "$(nproc)" --out results/grid_fit_v5
# 실패 시: 즉시 정지 → 확인(같은 plan/token/source_digest · 부분 산출 온전) → 아래를 정확히 1회 → 2회째는 재승인
./run.sh --mode all --leg grid_fit_v5 --config configs/grid_fine.yaml --nproc "$(nproc)" --out results/grid_fit_v5 --resume
```

archive → `make_receipt.py grid_fit_v5` → `attach_bundle_evidence('grid_fit_v5', 'docs/22p_gap/receipts/grid_fit_v5.validate.yaml')` → 사람이 `claim_roles`·`근거` → 창 닫기 (71차 §2 E9-3 그대로).
attach 는 이제 영수증의 두 산출 한 쌍·같은 semantic·`source_file_sha256 = bundle.fits_sha256`·`restore_map.run_dir`·봉인 summary 바이트·원장 `evidence.out` 을 대조한다.

## §3 리뷰어에게 묻는 것

1. **E3-R 종결 수용** — 예/아니오. 아니오면 남은 조건 한 줄.
2. **E9-R 정책 수용** — "실패 즉시 정지 · 명시적 `--resume` 1회 · 그 뒤 재승인" 이 71차 §3 의 종결 조건을 만족하는가.
3. **한정 실행 GO** — 위 둘이 예이면 `82854571d0240951c929d4a9b90260e53ca38e88` + (GO 뒤) 사람이 커밋한 계획 항목에 한정 실행 GO 인가 (예/아니오/조건부).

## §4 실행 출력 (커밋 뒤 실측)

```
판정 대상 코드                                82854571d0240951c929d4a9b90260e53ca38e88
source_digest                                 518d4f63076b77e3
전체 pytest (tests/)                          0 failed · 1869 passed · 2 xfailed (34:59)   (시작 HEAD = 끝 HEAD = b921333322f17a9ac5d92153865da441dc0c9bd7 · 미추적 0)
strict smoke (scripts/smoke_e2e.sh)           EXIT 0
pytest gate63~71 묶음                          152 passed · 1 xfailed (gate63~68 + gate70 + gate71, 21.5 s)
mutation_replay --check-preimages · -k premise · -k g70 · -k g71   전 지점 1회 · 4/4 · 4/4 · 3/3
등록부                                        tracked 367 · 디스크 367 · 미추적 0
```

## §5 우리가 스스로 신고하는 것

- 영수증 서명은 없다 (같은 principal 이 만들고 소비한다) — 71차 리뷰어가 요구하지 않은 것을 더하지 않았다.
- `attach_bundle_evidence` 의 복원 자리 결속은 묶음의 `restore_map.yaml` 에 기댄다 — 그 지도는 `archive_bundle bundle` 이 쓰고 `check` 가 재해시하는 구성원이다(payload index 에 든다). 지도 자체의 독립 attestation 은 없다.
- `test_g70_e3_17`·`test_g71_e3r_12` 는 현행 검증기의 실물 영수증 양성 대조군이라 RUN_SCOPE 가 바뀔 때마다 영수증을 다시 만든다 (이번에도 그랬다: `b9213333`).
- 71차 §4 그대로: 1855/2/smoke rc0 류의 수치는 송신 실행 증거다.

## §6 예산과 발송 규칙

70차 §6 그대로. 이 요청문과 발송문은 같은 말을 한다: **한정 실행 GO 를 재요청한다.**
