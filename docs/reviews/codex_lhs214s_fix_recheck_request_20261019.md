# Codex 짧은 재확인 요청 — LHS214 재확인 2 의 새 P3 수정 (L214R-S01 · S02 · S04 · Codex 표기 L214RR2-01 · 02 · 04) (2026-10-19 · 결과 0 건 · 발송 = 1저자)

> **한 줄**: Codex 재확인 2 (10-19 · 리뷰 핀 `77d8fd445` · 판정문 `docs/reviews/codex_review_lhs214rr_fix_recheck_20261019.md` · 수치 인계 코드 HOLD 해제 가능 ·
> R03 전체 종결 부분) 의 새 P3 넷 중 셋 (`L214R-S01` = L214RR2-01 · `L214R-S02` = 02 · `L214R-S04` = 04) 을 판정문 §2 · §4 · §5 의 최소 해결대로 고쳤다.
> 셋이 닫히는지 (특히 S01 로 R03 전체 종결이 되는지) · 새 결함이 있는지 짧게 판정해 달라.
> ✅ **1저자 10-19** *"권고대로 ㄱ"* — 수정 계획 `docs/reviews/lhs214s_fix_plan_20261019.md` Q1–Q5 (S01 = CommonMark 대로 · §3 안 코드 블록 값 안 읽음 · S03 = 다음 세대 ·
> S04 = 같이 · 커밋 하나씩).
> **리뷰 핀** = 이 요청서와 증거 폴더를 담은 본 가지 커밋 (SHA 는 발송 때 1저자가 적는다) · **기준** = `77d8fd445` (Codex 리뷰 핀).
> 증거 = `docs/reviews/lhs214s_fix_evidence_20261019/README.md` · 우리 트리 재현 (고치기 전) = `docs/reviews/codex_lhs214rr_fix_recheck_evidence_20261019/_repro_ours_20261019/README.md`.

## 0. 대상 · 지위

- 코드 diff = `git diff 77d8fd445 <리뷰 핀> -- scripts/supp20_input_receipt.py scripts/test_l214r_r01_restored_full.py webapp/templates/single.html webapp/test_single_null_metrics.py`
  (+ 게이트 `scripts/check_all.sh` 의 새 `run` 줄 하나) · 커밋 = S01 `aa207a6bd` → S02 `72da834ee` → S04 `aa6663bb9` (+ 원장 · 이 요청서 = 리뷰 핀).
- **봉인 32 무변경** — 세 수정 다 봉인 밖 (영수증 도구 · 시험 파일 · 템플릿) ⇒ 대기 지문 `2149f8738bb20b6a…` 그대로 (194 §9-8 · 보충 §9-3 · 영수증 S0b) · 등록 §3 `e8b2496b…` 그대로 ·
  수치 무영향 대조 (A4) 다시 안 함 (봉인 · 수치 경로 바이트 그대로).
- 별건 (LHS 밖 · 같은 커밋 묶음에 들어감): SDCP 앵커 사슬 화면 버퍼 `SELF-122` (`scripts/sdcp_anchor_v2_chain.py` · 판정 대상 아님).
- 새 214 실행 · WSL · 재봉인 · 등록 비준 없음 (GO 뒤 1저자).

## 1. 판정문 최소 해결 ↔ 수정

| 원장 | 수정 (자리 · 커밋) | 시험 (고치기 전 → 뒤) |
|---|---|---|
| `L214R-S01` (§4 — 탭 들여쓰기 · NBSP · U+2003 꼬리 닫는 줄 뒤 예시 §3 을 활성 등록으로) | `scripts/supp20_input_receipt.py` `_md_indent_cols` · `_md_fence` — 들여쓰기 = **열 수** (탭 = 다음 4 의 배수 열 · CommonMark §2.2 · 0–3 열만 울타리) · `_MD_CLOSE_TAIL` 닫는 줄 꼬리 = **space · tab 만** (§4.5) · Q2 = `registration_values` 가 활성 §3 의 **울타리 코드 블록 밖** 줄에서만 `code_fp` (`_md_section(strip_code=True)`) · ``aa207a6bd`` | selftest 114/118 → 118/118 (S12i = 판정표 32 꼴 · S12i2 지킴 40 · S12i3 탭 여는 줄 · S12j §3 블록 속 값 · S12j2 블록 밖 값 + 다른 값 블록) · 판정표 114 문서 다시 읽기 = 표준 파서와 다름 32 → 0 · 실제 보충 20 등록 영수증 무영향 |
| `L214R-S02` (§2 — R01 경계 시험 하드코딩 입력의 환경 의존 · E4 KeyError · E5 미완결) | `scripts/test_l214r_r01_restored_full.py` — E0 = 이 환경에서 raw q 가 세 경계와 **정확히** 같은 box_y 를 등록 입력에서 ULP 탐색 (상한 512 · 허용 폭 없음 · 엄격 > 그대로) · 못 찾으면 E1–E4 = 전제 불성립 FAIL · E3 아니면 E4 복원 안 함 · E5 독립 묶음 · E′ = 찾은 정확한 입력 ±18 ULP 출발 · 복원 helper = 사유 (KeyError 아님) · ``72da834ee`` | 그대로 27/27 → 30/30 · 등록 입력 +18 ULP (이 컨테이너의 Codex 환경 꼴 · 출발 raw q …962 · …960 · …956) = 고치기 전 **23/26** (판정문과 같음) → 30/30 · −18 ULP 30/30 |
| `L214R-S04` (§5 — 과거 `sigma_ratio` null → `/single` 500) | `webapp/templates/single.html` 툴팁 세 블록 (σ_brug/σ_grain · σ_brug / σ_ionic · σ_Bruggeman) = 숫자일 때만 형식화 · 곱셈 (`is number`) · 아니면 '—' 또는 일반 문구 (키 없음의 옛 '0.0000' 도 '—') · ``aa6663bb9`` | `webapp/test_single_null_metrics.py` 2/6 → 6/6 · 기존 웹앱 시험 그대로 |

## 2. 질문

| Q | 내용 |
|---|---|
| Q1 | S01 로 R03 (`L214R-R03`) 전체 종결에 동의하는가 — 지원 범위 = 울타리 코드 블록 · 0 열 ATX 제목 (들여쓴 코드 블록 · 목록 · 인용 · HTML 블록 · 1–3 칸 들여쓴 제목은 해석 안 함 · 들여쓴 제목은 §3 이 없으면 fail-closed) · Q2 (§3 안 코드 블록 값 배제) 가 판정문 §4 끝의 "추가 범위" 결정으로 충분한가 |
| Q2 | S02 — 탐색으로 전제를 세우는 방식 (허용 폭 · 엄격 > 그대로) 이 판정문 §2 최소 개선과 맞는가 · Codex 환경 (Windows Py3.12 NumPy 2.5.3) 에서 고친 시험이 30/30 인지 (이 컨테이너 재현은 ±18 ULP 이동으로만) |
| Q3 | S04 — 범위 (그 세 툴팁 블록) 로 닫는 데 동의하는가 · 같은 부류 머리 배지 null (`percolation_pct` 실측 500) = 새 원장 `L214R-S05` (P3 · open · 다음 세대 권고) 로 따로 둔 처리 |
| Q4 | S03 (이온 채널 요약 표지 ↔ FULL) = 다음 세대로 미룸 (1저자 Q3) — 새 214 발사의 차단 사유가 아님에 동의하는가 |
| Q5 | 새 214 까지 남은 것 = 등록 개정 비준 (§3 ← 대기 지문 · 대기 선언 삭제 · 역사 표 보존) · 재봉인 · B7 승인 핀 · 새 ROOT · 사전 점검 · 1저자 발사 승인 — 이 밖에 선행 조건이 있는가 |

## 3. 정정 · 한정

- `SELF-121` (판정문 §7 — 대기 지문 설명 낡음) = 10-18 요청서 머리에 정정 표지 · 반입 기록 (10-18 증거 README 는 SHA256SUMS 봉인 → 원문 그대로).
- 이번 증거의 "고치기 전" 은 부모 커밋 코드를 리포 밖 복제본에서 돌린 것 · S02 의 Codex 환경 꼴은 이 컨테이너에서 입력 이동으로 재현한 것 (다른 기계 재실행 아님).
- 같은 부류 점검 (우리): S04 시험 중 머리 배지 null 500 → `L214R-S05` (위 Q3).
