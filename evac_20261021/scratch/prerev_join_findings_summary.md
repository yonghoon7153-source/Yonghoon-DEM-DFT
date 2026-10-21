# Rint 조인 수정 (12d894c09 · a2cfd0365 · 654385e4c — 원격 f507bdc74 에 있음) 사전 리뷰 요지 (10-20)

## 공격 (고칠 것 = 1저자 Q1 / PB1 · 권고 (가) 지금)
1. 표지 경계 `rest[0].isspace()` (rint_iface_join.py:283) → `rest[0] in ' \t'` (또는 줄 끝) · 회귀 4 표지 × 4 문자 (U+00A0 · U+3000 · U+2003 · U+001F) = 16
2. 어휘 관문: 덤프 글자 TAB · LF · CR · 0x20–0x7E 밖 = `frame_layout` (lexical) — 머리 열 사이 · 행 · 상자 · step/count 의 NBSP · U+3000 · U+001F · 줄 끝 FF · VT · NEL · U+2028 (13 건)
3. scaffold 실수 열 (x y z r): 주석 아닌 줄에 ASCII 고정소수 `[+-]?[0-9]+(\.[0-9]+)?` + 어휘 검사 (주석 줄 제외 — case15 scaffold 머리줄에 U+2014)
4. `_STEP_RE`: `\d` → `[0-9]+` · `[ \t]*`
5. J13 에 f6 `wd` 만 넘치는 꼴 (변이 M4a · M4c 실패 0 = 틈)
- 검증된 사본: scratchpad/prerev_attack/fix_variants/F2/rint_iface_join.py (diff F2.diff) — 206/206 · real14 · case15 그대로 · Codex 구조 탐침 144 = 헤더 10 거부 + VT/FF step 4 건 사유 하나 더 (여전히 거부) 외 같음.
- 한정 (RIMPR-04 open): sim_to_um 5e-324 언더플로 (r_um 0 통과) · lens_geometry.py:34 OverflowError (반지름 ≈ 1e97 sim) · f5 비교 inf/NaN · 계획이 조인 판 미확인 (같은 프로세스 재계산 · 되읽기 길 없음) · 절 순서 · 비-AM 중복 · 자기 접촉 · id 0/음수 미검사 · ITEM: UNITS / TIME 거부 · 접촉 id ≥ 1e6 (%g) 거부 · 694 행 RuntimeWarning.

## 문장 정정 A–K (결정 불필요 · 다음 커밋)
A. 원장 SELF-124 note "S3 NUMERIC_MODULES 6 무변경" → "두 Rint 커밋 (3b9d51789 · 2b9efa253) ∩ (CODE_FILES 32 ∪ NUMERIC 6) = 0 · 대조 핀 → 리뷰 핀 구간에서는 CODE_FILES 네 파일이 다르고 그중 network_conductivity.py 는 NUMERIC 6 에도 든다" (요청서:15 에도 괄호 한 줄) · Codex 판정문 §7 "여섯 개 동일" 정정 알림 = 다음 요청서 Part B (넣었음 · d1768cf0c)
B. 요청서:15 · 원장: 인용문 안 괄호 끼워 넣음 · "32개" 글자 → 인용은 원문 그대로, 괄호는 밖으로
C. 요청서:22 "78/135 = 시험 작성 중간 시점" 을 판정문 §1 출처로 묶음 → "78/135 = 저자 보고 (커밋에 없어 재현 불가 — 판정문 §1 도 입증 안 함) · 현재 138 을 옛 코드에 = 81/138 (57 FAIL)"
D. 요청서:53 "고치기 전 숫자 78/135 …" 에 정정 표지 없음 → 표지 또는 note 에 "§1 표지로 갈음"
E. note 행 번호 12 · 11 · 19 · 50 = 리뷰 핀 판 → "(현재 14 · 13 · 22 · 53)"
F. 경계 서술 "줄 끝 · 공백 · 탭" ↔ 코드 isspace() → 코드 고침 (Q1 (가)) 이면 서술이 참이 된다
G. a2cfd0365 메시지 "assigned only by marker followed by boundary" 부정확 (실제: 표지로 시작하면 그 절로 읽고 경계 없으면 header_boundary 거부) → 원장 · 진행 기록에 정정 한 줄 (메시지는 못 고침)
H. 시험:999 J13 머리 출력 "고치기 전 = 조인 PASS / 정량 ACCEPT" → "① 정량 ACCEPT · ③④ 는 계획이 이미 join_particles_mismatch"
I. 계획 제목 "결과 0 건 · 초안" → "(등록 시 결과 0 건 · ✅ 비준 10-20 · 수정 결과 = §3 끝)"
J. CLAUDE.md:653 "회귀 전부 · 원장 claimed_fixed" → "회귀 8 통과 · 원장 RIMPR-R01 · 03 · SELF-124 claimed_fixed · RIMPR-04 open"
K. 진행:1138 "J14 전각 22" → "J14 전각 · 아라비아-인도 22"
