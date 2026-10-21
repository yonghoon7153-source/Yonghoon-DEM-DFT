#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""발송본 사본 → 고친 사본 (원본 발송본은 건드리지 않는다).  대안 판 = PRE-UL-01 을 고치지 않고 보낼 때의 문구 (고치면 새 핀 · 시험 수로 다시 쓴다)."""
import sys

SRC, DST = sys.argv[1:3]
t = open(SRC, encoding='utf-8').read()


def rep(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:80])
    t = t.replace(old, new, 1)


BLOCK = """> **사전 리뷰 반영 (10-21 · 대안 판 — PRE-UL-01 을 고치지 않고 보낼 때 · 고치면 이 블록 ①의 '닫지 않는 것' 첫 줄을 '닫는 것' 으로 옮기고 새 핀 · 시험 수로 다시 쓴다)**
>
> **이번에 닫는 것** — 수정 재확인 판정 (코드 핀 `eaecfba2a`) 의 잔여 P2 셋과 Q2–Q4 를 판정문 §4 · §7 최소 해결대로:
> `ULKRF-01` 같은 경계 RESUME 중복 · 상충 = 승인 없음 + 사유 · `ULKRF-02` 승인된 재시도의 단 끝이 옛 시도보다 짧음 · 같음 · 김 = 새 시도 시작 식별 (무승인 되돌아옴 = 미식별 그대로) ·
> `ULKRF-03` G2c 필수 열 결손 (양쪽 · 실제 restore CLI) = 예외 없이 FAIL + 사유 · Q2 영수증 범위 문구 · Q3 문법 사전 점검 원자료 재판독 · Q4 비차단 셋 · `ULKRR-01` 실행 부분 (실행 2 반입 · §7 Q7).
>
> **이번에 닫지 않는 것** (그대로 열림 · 숨기지 않는다):
> - **이어 돌림의 새 시도가 단 k_r + 1 줄을 다시 쓰기 전에 끝나는 경우** (TIMEOUT · GUARD · 이동 중 TIMEOUT) — 옛 시도의 그 단 줄이 남아 정상 관측으로 쓰인다.  합성 반례 (판독기 실제 함수 사슬):
>   옛 시도가 R_M 단 (k4) 줄 · RM 사건까지 쓰고 요약 전 끊김 → RESUME (k 3 · k3 끝) → 새 시도가 k4 창 둘 뒤 TIMEOUT = **primary OK · ρ 0.2026077873428664 % · UVa ALLOW**
>   (같은 꼴 fresh = UNIDENTIFIED · 거부) · GUARD 로 끝남 · 이동 중 TIMEOUT (새 창 없음) 도 같음 · 교차 전 단이면 LOWER_BOUND 0.2251 → 0.2701 %.  수정 전 (`eaecfba2a`) 에도 같은 결과 (이번 수정이 만든 것 아님).
>   후보 해결 = 단 줄 ↔ 그 단 창 기록 결합 (n_windows · 마지막 창 step) + 버린 옛 사건 구간의 창 · 단 줄 정리 (사전 리뷰 PRE-UL-01).
> - 정수 반올림 (k · w · step 의 소수 토큰 — 판정문 §6 관찰) — 판정문 §7 `resume_recheck.py` 를 고친 트리에서 돌리면 37 중 35 · 남는 둘 = `fractional_resume_event_k` · `fractional_confirmation_k` (이번에 고치지 않음).
> - G2 원자 비교 파서 (`ul_gates._dump_tokens` — 복원 · 중력 팔 G2) 의 머리 step · 선언 수 · ID 고유 미검사 (같은 ID 두 줄 · 다른 TIMESTEP · 열 수 다른 덧줄에도 G2 PASS — 손상 입력 방어 · README §5 '모든 경로에서' 는 G2 에 아직 서지 않는다).
> - G2c 파서 문제의 분류 = 지금 VALUE_MISMATCH (아래 Q3 — 등록 §14-10 은 "관측 결손 = UNCONFIRMED · 수치 불일치 = VALUE_MISMATCH 따로").
> - 수정이 더한 사유 줄 일부는 자체시험이 지키지 않는다 (변이 생존 — `resume_from` 밖 RESUME · k/step 숫자 아님 · 사건 ↔ 상태 파일 불일치 사유 · 사건 되감기 k > k_r 조건 · Q3 kit SHA256SUMS 판독기 줄 대조 · 재판독 rc) — 동작은 사전 리뷰 탐침으로 확인.
> - 재판독은 그 폴더의 **지금** 원자료를 다시 읽는다 — 런 뒤 원자료가 바뀌지 않았다는 영수증 (원자료 sha256 기록) 은 없다 · 원래 자리 한정 · 판독기 판 한정.
> - 본 R · 10:0 연장 · U 의 GO · Windows R32 (Codex 확인 요청 그대로).
"""

rep("> **한 줄**: 수정 재확인 판정", BLOCK + "\n> **한 줄**: 수정 재확인 판정")

rep("`evidence/*.json` · 탐침 글로 반례를 읽고 우리 시험으로 다시 만들었다 · 판정문 §7 탐침을 고친 트리에서 다시 돌려 주면 좋다).",
    "`evidence/*.json` · 탐침 글로 반례를 읽고 우리 시험으로 다시 만들었다 · 판정문 §7 탐침을 고친 트리에서 다시 돌려 주면 좋다 — 사전 리뷰 (10-21) 가 고친 트리에서 돌려 본 결과:\n"
    "  `resume_recheck.py` 37 중 35 (남는 둘 = 정수 반올림 관찰 · 위 '닫지 않는 것') · `grammar_provenance.py` 는 **그 합성 kit 사본 (`kit_metadata/`) 에 `read_history.py` · `history_params.json` 이 없어**\n"
    "  양성 (`positive_actual_reader`) 까지 '승인 밖 판독기' 로 거부된다 (Q3 설계대로 — 실제 ibb kit 사본에는 두 파일이 있다) · kit 사본에 두 파일 (봉인 바이트) 을 넣으면 양성 허용 · 음성 11 그대로 거부 ·\n"
    "  원자료 변조 넷 = 재판독 FAIL 로 거부 · `different_reader_runner_seal` = kit 목록 대조로 거부 (옛 기대 `gate True` 다섯 = Q3 가 의도해서 뒤집은 것) ·\n"
    "  `receipt_ids_recheck.py` 는 끝 정밀도 블록 (줄 296) 에서 `IndexError` — 토큰 `1.0000000000000001` 을 Q4 가 파서 문제로 거부해 행이 없다 (Q4 가 의도대로 동작) ·\n"
    "  그 블록만 빈 행을 허용하면 92 단언 중 기대 불일치 하나 = `g2c_missing_column_actual_cli` — 그 기대가 옛 결함 꼴 (KeyError · rc 1) 을 적어 둔 것이라 고친 트리의 rc 2 · VALUE_MISMATCH · 다음 UB 거부가\n"
    "  '불일치' 로 찍힌다 (= ULKRF-03 수정 신호) · `g2c_c_cpl7_missing` · `g2c_c_cpl8_missing` = 충족).")

rep("| Q3 | `ULKRF-03` — G2c 열 결손 = 기존 FAIL 경로 (복원 VALUE_MISMATCH) 로 충분한가 · 관측 결손이라 UNCONFIRMED 로 나눠야 하는가 (지금은 G2c 의 다른 파서 문제 — 소수 쌍 참조 등 — 와 같은 FAIL) |",
    "| Q3 | `ULKRF-03` — G2c 열 결손 = 기존 FAIL 경로 (복원 VALUE_MISMATCH) 로 충분한가 · 관측 결손이라 UNCONFIRMED 로 나눠야 하는가 (지금은 G2c 의 다른 파서 문제 — 소수 쌍 참조 등 — 와 같은 FAIL · "
    "⚠ 우리 등록 §14-10 · `ul_gates.restoration_verdict` 설명은 \"관측 결손 = UNCONFIRMED · 수치 불일치와 섞지 않는다\" 라 적는다 — 지금 분류는 그 문장과 어긋난다 · 관문 영향 없음 (둘 다 RESTORED 아님)) |")

rep("| Q2 | `ULKRF-02` — 새 시도 시작 = step 역행 (창 · 단) 또는 단 기록 k 되돌아옴 (먼저 오는 쪽) 이 짧음 · 같음 · 김 · 무승인을 다 가르는가 · 창 기록은 step 역행만으로 충분한가 (덱이 같은 단의 창 끝을 같은 step 에 쓴다 — 새 시도 첫 창 = 옛 시도 첫 창 step) |",
    "| Q2 | `ULKRF-02` — 새 시도 시작 = step 역행 (창 · 단) 또는 단 기록 k 되돌아옴 (먼저 오는 쪽) 이 짧음 · 같음 · 김 · 무승인을 다 가르는가 · 창 기록은 step 역행만으로 충분한가 (덱이 같은 단의 창 끝을 같은 step 에 쓴다 — 새 시도 첫 창 = 옛 시도 첫 창 step) · "
    "⚠ 다섯째 경우 = 새 시도가 그 단 줄을 쓰기 전에 끝남 (위 '닫지 않는 것' 첫 줄 — 지금 판독기는 옛 줄을 남긴다) |")

rep("- `GRAMMAR_VERDICT` 권고 = 실행 2 런 (`~/ps45_unload_hist_20261013/gram_20261015_030225/grammar_verdict.json` · 첫 PASS) · 반복도 같은 판정 · ⬜ 1저자 확인 (발사 때).",
    "- `GRAMMAR_VERDICT` = 실행 2 런 (`~/ps45_unload_hist_20261013/gram_20261015_030225/grammar_verdict.json` · 첫 PASS) · 반복도 같은 판정 · ✅ 1저자 10-15 확인 (발송 메모 · `4b1d67f62`).\n"
    "- 사전 리뷰 (10-21) 재확인: 묶음 sha256 = SLURM 화면 \"보낼 것\" 값 (넷) · 절대 경로 접두를 바꾼 '원래 자리' 모의 (kit 사본 = 리포 `history_test` 바이트 = `799459c85` kit 바이트 + 묶음의 kit SHA256SUMS) 에서\n"
    "  재판독 PASS · 검사 19 = 런 JSON · `ul_reader.grammar_prereq` 전체 PASS · 문제 0 (실행 2 · 반복) — ibb kit 사본 자체로 돈 것은 아니다.")

open(DST, 'w', encoding='utf-8', newline='\n').write(t)
print('written', DST, len(t))
