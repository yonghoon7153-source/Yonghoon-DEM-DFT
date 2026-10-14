# Codex 짧은 재확인 요청 — SUPR-01 · SUPR-02 수정 (사전 점검 기계 판독 줄 · 완료 영수증) (2026-10-14 · 초안 · 결과 0 건 · 발송 = 1저자)

> **한 줄**: 보충 20 수정 재검증 (`docs/reviews/codex_review_sup20_fix_reverify_20261014.md` · 리뷰 핀 `a9422d2e7`) 의 새 P2 둘 (Codex 표기 SUP20R-01 · SUP20R-02 → 원장 `SUPR-01` · `SUPR-02`) 을
> 판정문 §4 · §5 의 최소 해결대로 고쳤다 — 두 결함이 닫히는지 · 이 영수증 경로가 발사 전 사전 점검 증거로 충분한지 판정해 달라.
> ✅ **1저자 10-14** — 수정 계획 `docs/reviews/supr_fix_plan_20261014.md` Q1–Q4 = 권고대로 (구현 기록 = 그 문서 §4).
> **리뷰 핀** = 이 요청서 · 원장 claimed_fixed 가 들어간 본 가지 커밋 (push 뒤 1저자에게 알린 SHA · 발송 메시지에 적는다) · **기준** = `a9422d2e7` (지난 리뷰 핀 — 그 뒤 두 파일 · 두 등록 문서 변경 0 · 수정 전 HEAD `f9edcc416`) ·
> 수정 커밋 (본 가지 · cherry-pick 뒤 SHA) = `df43b1210` (비준 기록) · `df45a6219` (반례 먼저) · `8af6cbae3` (구현) · 이 요청서를 담은 문서 커밋.

## 0. 대상 · 지위

- 코드 diff = `git diff a9422d2e7 <리뷰 핀> -- scripts/run_network_194_parallel.py scripts/supp20_input_receipt.py` (실행기 · 영수증 도구 — 둘 다 봉인 32 `CODE_FILES` · `HANDOVER_FILES` 밖).
  문서 = 등록 §4 정정 둘 (`docs/reviews/lhs_network_batch_registration_20261012_supp20.md` · `docs/reviews/lhs_network_batch_registration_20261007_g2.md` — 결과 0 건 · 규칙 · 문턱 · 값 무변경) ·
  수정 계획 §4 · 10-12 수정 계획 `docs/reviews/sup20_fix_plan_20261012.md` "영수증 쓰는 법" 아래 정정 표지 한 줄 (옛 tee · `--dry-run-log` 블록은 원문 보존) ·
  시험 등재 두 줄 (`docs/reviews/selftest_inventory.tsv`).
- 봉인 32 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` **무변경** (실행기 `code_fp(code_hashes())` 로 확인) · 수치 재계산 · 194 · 보충 20 · WSL 실행 없음.
- 원장 `docs/reviews/findings.json` 의 `SUPR-01` · `SUPR-02` 갱신 = 병합 뒤 본 세션 (이 요청서는 원장을 고치지 않는다).

## 1. 판정문 최소 해결 ↔ 수정

| 판정문 | 수정 |
|---|---|
| §4 ① 사전 점검이 실제 쓴 `INPUT_DIGEST_KEYS` 전부 (코호트별 TSV sha) 를 기계가 읽는 출력에 | 실행기 화면 한 줄 `INPUT_DIGEST_JSON {…}` (`input_digest_json_line` · 사람이 읽는 줄은 그대로 · 본 실행이면 같은 값이 manifest `input_digest`) |
| §4 ② 그 값 = 등록값 = 반입 재계산 · 부재 = 거부 | 영수증 도구 E1 (로그의 그 한 줄 = 등록 §2 = `plan_input_digest` 재계산 · 키 전부) · 실행기 대조 P2 (줄 하나 · JSON · 키 = `INPUT_DIGEST_KEYS` · = 영수증 · = 사람이 읽는 줄) · P9 (= 이 체크아웃에서 같은 인자로 다시 만든 계획) — 부재 · 둘 · JSON 아님 · 키 결손 = 거부 |
| §4 ③ 같은 20 ID · raw 표에서 TSV 만 바꾼 로그 거부 · 정상 통과 · 경로 문자열 비교로 대체 금지 | selftest S7a (첫 행 `deck_sha256` 한 글자 · 실제 `build_plan` · `plan_input_digest` · `print_preflight` · 실행기 rc 0) · S7a2 (Codex `alternate_cohort.tsv` `8d5dcbd2…`) → 실패 칸 = **E1 · P9 둘뿐** (값) · 정상 S7 rc 0 · 경로 비교 없음 (`--lhss-cohort` 로 같은 경로를 덮어쓴 dry-run = P6 하나 · 지문 대조와 따로) |
| §5 ① 필수 세 항목 · `observe_imports=true` 의 명시 성공 값 · 줄 없음 = 실패 | `preflight_check_values` (화면 ✓ · ✗ 와 영수증이 같은 함수 · 값이 없으면 ✗) · P5 (영수증 `ok is True` + 로그 줄 하나씩 ✓) · P4 (영수증 · 인자 · argv 재해석 셋 다 true) |
| §5 ② 한 실행에 결합된 완료 · 정상 종료 · 구조화 영수증 | `run --dry-run --preflight-receipt P.json` — 실행기가 자기 화면 전체를 직접 잡아 P.log + JSON 을 원자적으로 (로그 먼저) · 멈춰도 · LaunchError 여도 (실제 종료코드) · 끝 줄 `PREFLIGHT_DRY_RUN_COMPLETE rc 0` · P1 (로그 sha256 · 바이트) · P3 (completed · 종료코드 0 정수 · 예외 · 멈춘 사유 없음 · ⛔ 없음 · 완료 표지 하나 = 마지막 줄) |
| §5 ③ 원본 전체 로그 · 실행 인자 · 출력 해시 · 종료코드 보존 · 셸 tee/grep 종료코드 ≠ 실행기 | 영수증 JSON = argv (실행기가 읽은 그대로) · 인자 · git · code_fp · 입력 지문 · 세 검사 · 관측 · 완료 · 실제 종료코드 · 멈춘 사유 · 로그 경로 · sha256 · 바이트 · 시각 · 실행기 파일 sha256 · P6 (argv = 등록 명령) · 텍스트 로그 단독 (`--dry-run-log`) = E0 거부 |
| §5 ④ 관측 OFF 전체 · 잘린 앞부분 · 필수 줄 결손 반례 · 정상 대조 상주 | selftest (b) · (c) · (d) + (e) grep · (f) 완료 표지 앞 자름 · (g) JSON 값 · (h) sha · Codex 로그 다섯 (텍스트 · 위조 포장) — 실행기 selftest ㊲a–㊲i |
| §5 끝 등록 grep 명령 정정 | 두 등록 §4 — grep 줄 = 원문 보존 · 대신 `--preflight-receipt` + 대조 명령 (보충 = `supp20_input_receipt.py --preflight-receipt` · 194 = `preflight-verify --expect-set production194`) |
| §6 추가 범위 — E2 짧은 sha ↔ 승인 SHA · H1 ≠ 승인 핀 | `--approved-sha` (Q3) = P10 (영수증 git sha · 로그 짧은 sha) · F7 · G7 (manifest git.sha) · 부재 = notes 경고 |

## 2. 시험 (반례 먼저 — 고치기 전 코드에 반례만 더해 실패 확인)

| 시험 | 고치기 전 | 고친 뒤 |
|---|---|---|
| `scripts/supp20_input_receipt.py --selftest` | 32/88 (56 FAIL · 새 반례 중 옛 판도 거부하던 둘만 통과) | 88/88 |
| `scripts/run_network_194_parallel.py --selftest` | 130/139 (㊲ 9 FAIL) | 139/139 |
| `scripts/supp20_input_receipt.py` (컨테이너 범위) | rc 0 · 11 칸 | rc 0 · 11 칸 |
| `scripts/test_lhs_release_v13.py` | 256/256 | 256/256 |

| Codex 로그 (`evidence/receipt_extra/` · `--dry-run-log`) | 고치기 전 | 고친 뒤 |
|---|---|---|
| `wrong_tsv_full_log` · `wrong_tsv_registered_grep` · `observation_off_truncated_before_stop` · `missing_three_prerequisite_lines` | rc 0 | rc 1 (E0) — 정상 영수증에 sha 를 맞춰 넣어도 P2 · P3 로 거부 (S10b) |
| `observation_off_full_log` | rc 1 | rc 1 (E0) — 같음 |

## 3. 계획과 다른 점

수정 계획 §4 "계획과 다른 점 · 정정" 1–7 그대로 — 요지: 대조 함수는 실행기에 (영수증 도구가 부름) · Q3 를 manifest 에도 · **194 쪽은 등록 §2 표 값 (raw 표 · 코호트 TSV) 을 문서에서 읽어 대조하는 칸이 없다** (손 대조 줄 · ⬜ 1저자) ·
"실행기 지문이 manifest 에 기록된다" 정정 · 194 §1 단계 2 줄 주석 · 화면 ✓ 의 빈 값 = ✗ · 이미 있는 영수증 거부.

## 4. 범위 밖 (이 요청이 묻지 않는 것)

- 194 · 보충 20 발사 · v1.3 · 실제 발사 핀의 WSL dry-run 영수증 · fast16 + real4 · 저자 발사 승인 — 판정문 §6 의 3–7 단계 그대로.
- 판정문 §6 의 194 HANDOVER 해시 대조 (G6 없음 · F6 는 보충만) · `scope=launch` 뜻 — 이번에 바꾸지 않음.
- 같은 JSON 안 사본끼리 대조는 누락 검사 — 영수증 · 로그를 **함께** 일관되게 위조하는 것을 외부 진위 인증 없이 가린다는 뜻이 아니다 (판정문 §5 끝 "암호학적으로 막으라는 요구가 아니다").

## 5. 질문

- **Q1.** `SUPR-01` (판정문 §4 최소 1–3) · `SUPR-02` (§5 최소 1–4 · 등록 명령 정정) 가 이 수정으로 닫히나.
- **Q2.** 실행기 완료 영수증 + `preflight_receipt_checks` (P0–P10) + 영수증 도구 E1 · E2 가 판정문 §3 의 "전체 입력 지문 일치와 정상 dry-run 완료" 증거로 충분한가 — 한정 문구가 더 필요한가.
- **Q3.** 194 쪽 등록 §2 값 (raw 표 · 코호트 TSV) 의 손 대조로 충분한가, `preflight-verify` 에 등록 문서 대조 칸이 필요한가.
- **Q4.** 새 결함이 있나 — 있으면 등급 · 반례.

## 6. 재현 (리뷰 핀 · 컨테이너 Linux · Python 3.11.15)

```bash
git diff a9422d2e7 <리뷰 핀> --stat -- scripts/run_network_194_parallel.py scripts/supp20_input_receipt.py   # 이 검토의 코드 = 이 둘
git diff a9422d2e7 <리뷰 핀> --stat -- scripts/ webapp/                 # 그 사이 다른 변경 13 = Rint G2 (rint_* · test_rint_* · step3_sigma.py) · ps45 σ_e 변형 실행기 — 이 검토와 무관 · 봉인 32 · HANDOVER_FILES 밖 (code_fp e8b2496b… 그대로)
python3 scripts/supp20_input_receipt.py --selftest                     # 88/88
python3 scripts/run_network_194_parallel.py --selftest                 # 139/139 (~1.5 분)
python3 scripts/supp20_input_receipt.py                                # rc 0 · 11 칸 (컨테이너 범위)
python3 scripts/test_lhs_release_v13.py                                # 256 PASS · 0 FAIL
for f in wrong_tsv_full_log wrong_tsv_registered_grep observation_off_full_log observation_off_truncated_before_stop missing_three_prerequisite_lines; do
  python3 scripts/supp20_input_receipt.py --dry-run-log docs/reviews/codex_sup20_fix_reverify_evidence_20261014/evidence/receipt_extra/$f.log >/dev/null; echo "$f rc=$?"; done   # 다섯 다 rc 1
# 진짜 dry-run 영수증 (원 dump 없는 컨테이너 — 원자료 문제 · dirty 면 실행기가 ⛔ rc 2 로 멈추고도 영수증을 쓴다 · 대조가 거부):
python3 scripts/run_network_194_parallel.py run --root /tmp/netsupp20_x --cohorts lhss --dry-run --observe-imports --preflight-receipt /tmp/netsupp20_x_preflight.json; echo "dry-run rc=$?"
python3 scripts/supp20_input_receipt.py --preflight-receipt /tmp/netsupp20_x_preflight.json; echo "receipt rc=$?"
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 bash scripts/check_all.sh   # 병합 뒤 본 세션이 돌린다
```

- 윈도 스냅샷: 영수증 selftest 는 실행기 `_guard_posix` 를 대역으로 바꿔 dry-run 경로를 돈다 (WSL 전용 관문 · 계획 · 화면 · 영수증은 그대로) — 실행기 selftest 는 Linux/WSL 전용이다.
