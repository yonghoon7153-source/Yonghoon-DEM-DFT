# Codex 요청 — 접촉망 세대 2 재검증 7 (G2RR6-01 수정 확인 · 2026-10-11 · 결과 0 건 · 발송 = 1저자)

> **한 줄**: 재검증 6 의 남은 차단 `G2RR6-01` (P2) 을 고쳤다 — S0b 공용 판정이 case15 원자료 sha256 상세와 음수 면적 상세를 다시 판정한다.  이것으로 194 발사 전 차단이 닫히는지 판정해 달라.
> ✅ **1저자 10-11** (*"재검증 7 요청서 끝나고"* = 요청서 완성 지시) — 계획 `docs/reviews/g2rr6_fix_plan_20261011.md` Q2 (해시 자리수) · Q3 (이 요청서 범위) = 권고 (가) 그대로 (12 자리 유지 · G2RR6-01 만 · 보충 20 지원은 따로 짧은 검토).

## 0. 대상 · 지위

- 검토 핀 = 이 요청서가 들어 있는 커밋 · 수정 커밋 = `ec9c51149` (부모 `821f0e151`) · 변경 파일 = `scripts/g2_network_reread.py` (인계 도구 · 실행기 HANDOVER_FILES) · `scripts/wsl_network_smoke.py` (시험 픽스처 2 줄).
- 봉인 32 · `code_fp e8b2496b…` **무변경** · 194 · case15 망 · 시범 셋 **재실행 없음** (판정문 §0 · §6-1) · WSL 재실행 없음 (정상 기록 = 반입한 10-09 기록).
- 판정문 = `docs/reviews/codex_review_gen2_network_reverify6_20261011.md` · 증거 반입 · 우리 재현 = `docs/reviews/codex_gen2_network_reverify6_evidence_20261011/_README_import.md` (§2 고치기 전 · §5 고친 뒤).
- 1저자 결정: 수정 범위 Q1 = (가) Codex 최소 + 같은 함수의 같은 부류 넷 (10-11).

## 1. 판정문 §2-3 최소 해결 ↔ 수정

| §2-3 | 수정 (`scripts/g2_network_reread.py`) |
|---|---|
| ① 원자료 sha256 상세 — 닫힌 키 · actual/expected 형식 · 일치 · 빈 · 없음 = 실패 | `_c15_raw_sha_verdict`: `raw_sha_ok is True` + `raw_sha` = dict · 키 = 등록 네 파일 정확히 · 값 = [actual, expected] 각 소문자 16 진 12 자리 · actual = expected · **expected = 등록 sha256 앞 12 자리** (`CASE15_NEGCTL['raw_sha256']` = `docs/data/case15_corner_20261001/README.md` 표 · selftest 가 README 와 대조).  ⚠ 12 자리 접두 대조 = 64 자리 바이트 재검증 **아님** (판정문 §2-3 ① 문구 그대로 한정) |
| ② 음수 면적 — 등록 두 쌍 · 유한 실수 면적 < 0 · bool · NaN · Inf · 결손 · 0 · 양수 거부 | `_c15_negative_rows`: 목록 · 두 행 · 행 = [id1, id2, 면적 µm², δ µm] 넷 (생산자 `case15_channel_probe` 꼴) · ID = 정수 (bool · 문자열 · 실수 아님) · 유한 실수 · 면적 < 0 · δ > 0 · 중복 없음 · **행 = 등록 표시값** (`negative_rows_ref` — 생산자 `round(·, 6)` · 판정문 §2-3 ② "표시 정밀도 대조") |
| ③ 네 반례를 실제 `--smoke-root` 소비자 회귀로 · 정상 rc 0 유지 | selftest 새 검사 셋 (아래 §2) — 반례 넷 + 같은 부류를 실제 `main(['--smoke-root', …])` 로 · 10-09 실제 WSL 기록 (Codex 입력 그대로) rc 0 |
| (같은 부류 · 1저자 Q1 (가)) | nc1 실패 단계 = [등록 단계] **정확히** (옛 판 = 포함만) · nc2 τ 칸 **어디든** 숫자 금지 (옛 판 = 등록 키 접두만) |

- 바꾸지 않은 것: 검사 ID 일곱 · 이온 허용치 · nc4 · nc5 · S0b 바깥 구조 · launcher-root 경로 · 생산자 보고 꼴.

## 2. 시험 (반례 먼저)

| 시험 | 고치기 전 (`821f0e151` 판정식) | 고친 뒤 (`ec9c51149`) |
|---|---|---|
| `scripts/g2_network_reread.py --selftest` | 23 / 26 (새 셋 실패) | **26 / 26** |
| └ Codex 넷 + 같은 부류 21 (raw_sha {} · None · 키 하나 삭제 · 키 추가 · 두 값 함께 바꿈 · 16 진 아님 · 빈 문자열 · 원소 셋 / 면적 0 · NaN · bool · 문자열 · 군더더기 행 · 짧은 행 · ID 문자열 · ID 실수 · 다른 음수값 · δ 결손 · 중복 행 / 실패 단계 하나 더 / 등록 밖 τ 숫자 키) — 실제 `--smoke-root` | 전부 rc 0 · S0b ✓ (오수용) ⛔ **정정 10-12 (Codex 재검증 7 `G2RR7-01`)**: 24 개 rc 0 (오수용) + 중복 행 `na_dup_row` 1 개는 옛 판정식도 이미 rc 1 (ID 쌍 목록 불일치) — 기존 오수용 24 새로 차단 + 중복 행 1 계속 거부 = 현행 25 거부 | 전부 rc 1 · S0b ✗ (S0 그대로) |
| └ 10-09 실제 WSL 기록 = Codex 입력 그대로 (`evidence/r6_s0b_*.input.json` 일곱) | 넷 rc 0 (오수용) | positive rc 0 · n_fail 0 · 넷 + 대조 둘 rc 1 · n_fail 1 |
| └ 등록 sha256 = case15 README 표 | (등록 없음) | 같음 |
| `scripts/wsl_network_smoke.py --selftest` (생산자 evaluate = 같은 공용 판정) | — | 16 / 16 |
| `--selftest-real` (실제 case15 파이프라인 → `--smoke-root`) | — | 4 / 4 (rc 0) |
| 우리 구동기 `docs/reviews/codex_gen2_network_reverify6_evidence_20261011/_repro_ours_20261011/repro_s0b_cli.py` (Codex 입력 일곱) | Codex 와 같음 | 넷 rc 1 · positive rc 0 · 대조 둘 rc 1 (`repro_s0b_cli_fixed.json`) |
| 같은 부류 탐침 `probe_same_class.py` (23) | 21 통과 · 2 거부 | 23 / 23 거부 (`probe_same_class_fixed.json`) |
| 게이트 `scripts/check_all.sh` | — | 전부 통과 (수정 커밋 단독 · 이 요청서 커밋) |

## 3. 정정 · 한정

- **`SELF-102` 정오 (재검증 6 §5 Q7)**: 재검증 6 요청서 §5 제목 *"시험 약화 없음"* 의 정확한 표현 = **검사 내용 무변경 (fast + real 두 명령을 모두 돌릴 때 · `chk(…)` 20 = 16 + 4)** · 매 push 자동 범위 = fast 16 (real 4 = 발사 핀 사전 점검 필수).
- **`SELF-104`**: 반입 README · 원장 등에 같은 부류 탐침 결과를 "22 중 20 통과" 로 적었다 — 원자료 = 23 중 21 통과 · 2 거부 (정정 반영).
- 64 자리 전체 SHA 기록 = 다음 기록 형식 (보충 20 지원 변경 · 그 짧은 검토에서) — 이번 범위 밖 (계획 Q2 (가)).
- 보충 20 (판정문 §7) = 이번 범위 밖 — 구현을 병행해 따로 짧은 검토 (계획 Q3 (가)).

## 4. 질문

- **Q1.** `G2RR6-01` 이 판정문 §2-3 ① ② ③ 기준으로 닫히나.
- **Q2.** 같은 부류 넷 (등록 표 대조 · 행 꼴 / 등록 표시값 · 실패 단계 정확히 하나 · τ 칸 숫자 전면) 이 정상 경로를 과잉차단하지 않나 — 10-09 실제 기록 · 실제 case15 파이프라인 (`--selftest-real`) 은 rc 0.
- **Q3.** 이것으로 194 발사 전에 남은 것이 판정문 §6-2 · §6-3 (저자의 별도 발사 승인 · 발사 핀 사전 점검 fast16 + real4 · 깨끗한 트리 · 새 ROOT · 관측 ON · 완료 뒤 SEALED194 · 결합 · 감사 · production194 상세 재독해 · 인계 / 배포 관문) 뿐인가.
