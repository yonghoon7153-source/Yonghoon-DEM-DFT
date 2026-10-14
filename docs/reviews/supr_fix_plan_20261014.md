# SUPR-01 · SUPR-02 수정 계획 (2026-10-14 · ✅ 1저자 비준 10-14 (Q1–Q4 권고대로 · *"lhs는 권고대로 하고"*) · 결과 0 건)

> 근거 = Codex 보충 20 수정 재검증 `docs/reviews/codex_review_sup20_fix_reverify_20261014.md` (리뷰 핀 `a9422d2e7`) · 반입 · 우리 트리 재현 = `docs/reviews/codex_sup20_fix_reverify_evidence_20261014/_README_import.md`.
> 판정 요지: SUP20-01 · 02 **닫힘 (verified)** · 새 P1 없음 · 새 P2 둘 (영수증 경로 · Codex 표기 SUP20R-01 · 02 → 원장 `SUPR-01` · `SUPR-02`) · **사전 점검 진입 허용 · 실제 194 · 보충 20 발사와 v1.3 배포 = HOLD**.
> 범위: 고치는 파일 = `scripts/supp20_input_receipt.py` (영수증) · `scripts/run_network_194_parallel.py` (사전 점검 출력) · 등록 §4 명령 문구.  둘 다 수치 봉인 32 (`CODE_FILES` · `code_fp e8b2496b…`) **밖** — 봉인 · 수치 · 계산은 바뀌지 않는다.  실행기 파일 지문은 바뀌므로 발사 manifest 에 기록된다.

## 1. 결함과 최소 해결 (판정문 §4 · §5 그대로)

| 원장 | 무엇이 새나 | 우리 재현 (10-14 · HEAD) | 최소 해결 |
|---|---|---|---|
| `SUPR-01` | 사전 점검 로그의 입력 지문에 코호트 TSV 해시가 없고 영수증 E1 · 코호트 줄도 이름 · 개수만 본다 → 다른 TSV 로 돈 dry-run 로그가 통과 | `wrong_tsv_full_log` rc 0 | 사전 점검이 실제 쓴 `INPUT_DIGEST_KEYS` 전부 (코호트별 TSV sha 포함) 를 기계가 읽는 출력으로 · 영수증이 등록값 · 반입 재계산과 비교 · 부재 = 거부 · TSV 만 바꾼 로그 거부 시험 상주 |
| `SUPR-02` | E5 가 ⛔ · ✗ 부재만 본다 → 중단 사유 앞에서 잘린 로그 · 필수 검사 줄 셋이 빠진 로그가 통과 | `observation_off_truncated_before_stop` rc 0 · `missing_three_prerequisite_lines` rc 0 · 대조 `observation_off_full_log` rc 1 | 필수 세 항목 + `observe_imports=true` 의 명시 성공 값 · 한 실행에 결합된 완료 상태와 정상 종료 · 원본 전체 로그 · 인자 · 출력 해시 · 종료코드 보존 · 잘린 · 결손 반례 상주 · 등록 §4 grep 명령 정정 |

## 2. 1저자가 정할 것

| Q | 질문 | 선택지 | 권고 |
|---|---|---|---|
| Q1 | `SUPR-01` 입력 지문 연결 | (가) 사전 점검이 `INPUT_DIGEST_JSON {…}` 한 줄 (전체 키 · 코호트별 TSV sha) 을 내고 영수증이 등록 §2 값 · 반입 재계산과 셋을 대조 · 부재 거부 (나) 파일 경로 문자열 대조 | **(가)** — Codex 가 (나) 를 대체로 인정하지 않는다 (판정문 §4 ③) |
| Q2 | `SUPR-02` 완료 증거 | (가) 사전 점검이 끝날 때 구조화 영수증 JSON (필수 세 항목 · `observe_imports` · 완료 표지 · 종료코드 · 인자 · 전체 로그 sha256) 을 원자적으로 쓰고 영수증 도구는 그 JSON + 전체 로그를 요구 (grep 로그 단독 = 거부) (나) 텍스트 로그 유지 + 완료 줄 · 성공 줄 명시 요구 | **(가)** — 판정문 §5 ② "가능하면 구조화 영수증" · 등록 §4 명령은 grep 대신 전체 로그 + JSON 보존으로 정정 |
| Q3 | 같은 도구에서 E2 (로그의 git short) 를 승인 SHA 와 대조할지 (판정문 §6 "추가 범위 주의" — 새 결함 아님) | (가) `--approved-sha` 인자로 대조 · 부재 = 경고 (나) 그대로 | **(가)** — 같은 파일 · 작은 변경 · 발사 핀 확인이 손으로만 남지 않게 |
| Q4 | 발사 승인을 미리 적을 때의 문구 | 판정문 §3 문구 그대로 | **그대로** — *"수정본의 사전 점검 착수를 승인한다. 실제 생산 발사는 최종 핀의 fast16+real4, 깨끗한 트리, 두 새 ROOT, import 관측 ON, 전체 입력 지문 일치와 정상 dry-run 완료가 모두 확인된 뒤에만 허용한다."* |

> ✅ **1저자 비준 10-14** — Q1–Q4 **권고대로** (Q1 (가) `INPUT_DIGEST_JSON` 한 줄 · 셋 대조 · Q2 (가) 구조화 완료 영수증 + 전체 로그 · grep 로그 단독 거부 · Q3 (가) `--approved-sha` · 부재 = 경고 · Q4 = 판정문 §3 문구 그대로) ·
> 1저자 *"lhs는 권고대로 하고"* → §3 순서대로 (반례 먼저).  Q4 문구는 조건부 승인이다 — 실제 발사 승인이 아니다.

## 3. 순서 (비준 뒤)

1. 반례 먼저 — Codex 로그 셋 (`wrong_tsv_full_log` · `observation_off_truncated_before_stop` · `missing_three_prerequisite_lines`) 을 영수증 시험에 상주 → 고치기 전 실패 확인 · 정상 로그 · `observation_off_full_log` 대조.
2. Q1 · Q2 (· Q3) 구현 → 영수증 · 실행기 자체 시험 · `test_lhs_release_v13` · 게이트.
3. 등록 §4 명령 정정 (보충 20 등록 · 194 등록의 사전 점검 줄) — 결과 0 건 문구 정정.
4. Codex 짧은 재확인 (수정 diff + 반례 재실행) → 판정문 §6 의 2–7 단계 (WSL 사전 점검 → 1저자 실제 발사 승인 → 194 → 보충 20 → 배치별 감사 · 다시 읽기 · τ/인계 관문 → v1.3 결합 관문).
