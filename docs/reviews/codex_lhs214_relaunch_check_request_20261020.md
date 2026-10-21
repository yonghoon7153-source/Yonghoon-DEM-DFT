# Codex 짧은 발사 확인 요청 — LHS214 다시 발사 다섯 단계 (초안 3 · 2026-10-21 · ⬜ 1저자 Q5 · 발송 = 1저자)

> **초안 3 (10-21)** = 초안 2 (`02393562f` · 메인 정정 `7f99be67c`) + Codex 요청 전 사전 공격 리뷰 (독립 검토자 · 결함 PRE-LHS-01–10 · 막는 결함 P1/P2 없음 · 전부 P3) 반영 —
> ① S0b 시험 보강 = 코드 (원장 `SUPR-04` · `SUPR-05` · 1저자 10-21 [LHS] Q1 *"권고대로 해줘"* · B7 핀 앞) ② 문장 정정 (`SELF-129` · PRE-LHS-04 · 05 · 06 · 07 · 09) ③ 한 줄씩 (PRE-LHS-01 · 08 · 10).
> 이번 수정 커밋 넷 (원장 → 시험 먼저 → 고침 → 문서) = `<수정 커밋 · 메인 반영 뒤 채움>` — 작업 트리에서 만들어 메인이 반영한다 (반영 뒤 SHA 로 채운다 · 이 요청서의 다른 SHA = 메인 SHA · `SELF-116`).

## 0. 이번에 닫는 것 / 닫지 않는 것

**닫는 것 (확인 요청)**

| # | 무엇 | 자리 | 상태 (이 컨테이너 · 비준 커밋 트리 · 부록 A — 보강 줄은 보강 판 · 부록 B) |
|---|---|---|---|
| ① | 비준판 문안 — 194 §3 · §5 머리 · §9-8 · §9-9 / 보충 §3 · §5 머리 · §9-3 · §9-4 | 비준 커밋 `f82929b06` | 묶음 §1-4 · §1-5 diff 그대로 — 바꾼 것은 날짜 자리 (`⬜(날짜)` → `10-21 ·`) 뿐 · 두 문서 = 그 diff 를 붙인 바이트 |
| ② | 지문 재결합 — 두 등록 §3 활성 = 실행기 `code_fp(code_hashes())` · 인계 도구 · 배포 빌더 = 194 §3 ✅ 줄 | 비준 커밋 · 묶음 §2 | 다시 잼 = `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` · 보충 컨테이너 영수증 rc 0 · 실패 칸 없음 |
| ③ | B7 승인 핀 — 정의 · 대조 자리 | 묶음 §3 | 정의 그대로 · 핀 값 = ⬜ 1저자 · 후보 = **이번 S0b 시험 보강 커밋들 뒤**의 push 된 본 가지 커밋 (`<수정 커밋 · 메인 반영 뒤 채움>` 의 마지막 또는 그 뒤 문서만 바뀐 커밋) — 비준 커밋 `f82929b06` 은 후보가 아니다 (그 판의 두 등록 §9-9 · §9-4 = *대화 원문 ⬜* · 영수증 도구 = 보강 전 판 · 사전 리뷰 PRE-LHS-10) |
| ④ | 새 핀 · 새 ROOT 둘 WSL 사전 점검 기록 | 묶음 §4 · 반입 폴더 ⬜ | ⬜ — 반입 뒤 이 요청서를 채워 보낸다 |
| — | 보충 영수증 selftest S0b 의 봉인 지문 기대 — 묶음 §6 Q3 (가) 의 상태별 기대를 **앞자리 상수 없이** 구현 ((가) 원문 = 상태별 상수 · 차이 · 잃는 것 · 막는 자리 = Q5 · §6 · 사전 리뷰 PRE-LHS-04) · 1저자 10-21 Q1 | 코드 커밋 `fe23f2b83` · 증거 `docs/reviews/lhs214_relaunch_s0b_evidence_20261021/` | 비준 사본에서 121/122 (S0b) → 고친 판 123/123 (pending · 비준 둘 다) · Q5 · 묶음 문서의 결과 전 기대 수 (§1-6 2 단계 · 명령 주석 · §4 단계 2 = 코드 커밋 전 예상 122/122) 도 123/123 으로 고침 (메인 10-21 통합 · 새 검사 S11g 하나) |
| — | ★ S0b 시험 보강 — 보충 쪽 봉인 지문 문제를 `s0b_fp` 가 받지 않음 (`SUPR-04` · PRE-LHS-02) · 변이 여섯 생존 (`SUPR-05` · PRE-LHS-03) · 1저자 10-21 [LHS] Q1 *"권고대로 해줘"* | `<수정 커밋 · 메인 반영 뒤 채움>` · 증거 같은 폴더 §7 | 시험 먼저 판 ⟦TF_REG⟧ (registered) · ⟦TF_PEND⟧ (pending) — 실패 = S11g · S11h 의 보충 쪽 두 꼴 → 고친 판 ⟦FIX_REG⟧ · ⟦FIX_PEND⟧ · 변이 13 (사전 리뷰 여섯 + m1–m4 + 새 가드 셋) = ⟦MUT_SUMMARY⟧ · 실물 자리 보충 쪽 두 꼴 = S0b 실패 (고치기 전 S0b PASS) · 묶음 결과 전 기대 123/123 → 124/124 (정정 표지) |

**닫지 않는 것**

| 무엇 | 상태 |
|---|---|
| ⑤ 1저자 발사 승인 · 실제 194 · 보충 20 실행 · 결과 · 등록 §5 관문 | ⛔ 별도 승인 (비준 ≠ 발사 승인 — 두 등록 머리 줄) |
| v1.3 배포 | HOLD — H0 model_limit 행 = 주 타깃 배포 HOLD (194 §9-8 ⑤) |
| S3 | 별도 HOLD — `scripts/network_conductivity.py` 바뀜 → 재봉인 의무 |
| `L214R-S03` · `L214R-S05` | open · 한정 유지 (S05 = v1.3 뒤 · 1저자 10-20 Q6) |
| σ₀ 1.5 솔버 상수 | 이번 재봉인 밖 (1저자 10-20 Q4) |
| SUP20 영수증을 일반 실행 게이트에 | 넣지 않음 (1저자 10-20) |
| 194 등록 §1 기대 표 (2 · 5 행 — 봉인 `e8b2496b…` · 지연 import 분류 90) | 10-07 사전 점검 기록 (옛 봉인 기대) — **비준 표지 없음** · 활성 기대 = 194 §3 끝 ✅ 줄 (`2149f873…` · 지연 import 92) · 다시 발사 사전 점검의 기대 = 묶음 §4 · 등록 문서에 역사 표지를 넣을지 = 1저자 (B7 전 · 사전 리뷰 PRE-LHS-08) |
| (닫힘 · 기록) 등록 194 §9-9 · 보충 §9-4 의 *대화 원문* | 비준 커밋 `f82929b06` 은 날짜 자리만 채웠다 → 메인이 같은 날 뒤 커밋 (`7f99be67c`) 에서 1저자 10-21 원문 (*"다 진행하자"* · [LHS] Q1) 을 두 줄에 채움 → 이번 정정이 같은 두 줄에 개정 · 활성 지문 비준 결정 (1저자 10-20 22 *"q는 권고대로"* — 용훈 포메이션 [LHS] Q3 · 진행 기록 10-20 22 줄) 을 더함 (사전 리뷰 PRE-LHS-09) — 리뷰 핀의 두 등록 문서 = 비준 커밋 판 + 그 두 줄 (`git diff f82929b06 <리뷰 핀> -- <두 등록 문서>` = 그 두 줄뿐 · 기계 값 칸 · §3 · §5 · §9-8 · §9-3 무변경) |

## 1. 핀

- 가지 `claude/stoic-knuth-NObVQ` · 대조 핀 = `34713ac9650ece7c8d59b7c4d9a2aefccee693ea` (Codex 10-20 판정 `docs/reviews/codex_review_lhs214cx_fix_recheck_20261020.md` 의 검토 핀) · 초안 1 · 2 를 쓴 작업 트리를 만든 때의 본 가지 머리 = `a76f59d0d16c58b2f7816d67a3432f94367e46f0` (대조용 기준 — 지금 본 가지 머리가 아니다 · 사전 리뷰 PRE-LHS-05).
- 코드 커밋 (S0b) = `fe23f2b839f0a49adb077348fec6d4c85443b62a` (부모 = 메인 `a6996396774064fa159d360da0e1d26877b66c33`) · 비준 커밋 = `f82929b0644be39b44e9fba9ea04cf9d60de9146` (부모 = 코드 커밋) · 메인 정정 = `7f99be67c` — 본 가지 커밋 (에이전트 작업 트리 판을 메인이 10-21 cherry-pick · 충돌 0 · 내용 같음 · 부록 A 를 이 두 SHA 로 다시 돌려 출력이 글자까지 같음).  기준 머리 `a76f59d0d` 와 메인 부모 `a69963967` 사이에 영수증 도구 · 두 등록 문서 · 실행기는 바뀌지 않았다 (`git diff a76f59d0d a69963967 -- <넷>` 빈 출력) — 아래 "`a76f59d0d` 판" 대조는 메인 부모 판과 같은 바이트다.
- `02393562f` 커밋 메시지의 작업 트리 SHA `a45a980e9` · `e9267000b` = 같은 내용의 작업 트리 판 (메인 반영 = 비준 커밋 `f82929b06` · 코드 커밋 `fe23f2b83` — 바이트 · 메시지 같음 · 본 가지에서는 닿지 않는다 · 사전 리뷰 PRE-LHS-01).
- S0b 시험 보강 = `<수정 커밋 · 메인 반영 뒤 채움>` (넷 — 원장 · 시험 먼저 · 고침 · 문서 · 작업 트리 판을 메인이 반영).
- ⚠ 보내기 전 (메인): 이 요청서 · 묶음 · 증거 README · 두 등록 · 원장이 적은 커밋 SHA 전부 = push 된 본 가지의 조상 (`git merge-base --is-ancestor <sha> origin/claude/stoic-knuth-NObVQ` rc 0 — 사전 리뷰 PRE-LHS-01: 10-21 리뷰 때 `a69963967` · `fe23f2b83` · `f82929b06` · `02393562f` · `7f99be67c` 다섯은 원격 머리의 조상이 아니었다 = push 전 · B7 = push 된 커밋 · WSL `git fetch` 의 전제).
- B7 승인 핀 = ⬜ (1저자 · §0 ③) · 리뷰 핀 = ⬜ (메인 — 사전 점검 기록을 반입한 커밋 · 코드 = 승인 핀과 바이트 같음 · 문서만 다름).
- 보낼 때 함께: WSL 사전 점검 묶음 `lhs_preflight_<S>_<T>.tgz` (sha256 ⬜) · 반입 폴더 ⬜ · 194 손 대조 표 (묶음 §5 · 채운 판) ⬜.
- ⚠ ⬜ 칸 · `<…채움>` 자리가 남아 있으면 보내지 않는다.

## 2. 대조 핀 → 비준 커밋 — LHS214 발사 관련 파일 (부록 A · 보강 줄 = 부록 B)

| 무엇 | 실측 |
|---|---|
| 봉인 32 (`CODE_FILES`) | `git diff --quiet 34713ac96 f82929b06 -- <32>` rc 0 · `code_fp` = `2149f873…c3eb` |
| 인계 도구 2 · 배포 빌더 · 실행기 · 스모크 | rc 0 (sha256 = 묶음 §2 #14–#17 · #19 그대로) |
| `scripts/supp20_input_receipt.py` | 코드 커밋만 — `_selftest` 안 (AST: 최상위 문 59 중 바뀐 것 = `_selftest` 하나) · sha256 `2c7e0b81…` → `3d6110be…` (묶음 §2 #18 *"Q3 이면 또 바뀐다"*) |
| 두 등록 문서 | 비준 커밋만 — 194 sha256 `7fd158cb…` → `2c3ed36f…` · 보충 `b2389709…` → `7cad47d1…` (= 묶음 diff 를 붙인 바이트) |
| 기록 | 재고 대장 한 줄 (`docs/reviews/selftest_inventory.tsv` · 영수증 도구 행 · 기록만) · 증거 폴더 · 이 요청서 |
| ★ 보강 (이번 수정 · `7f99be67c` → 보강 판) | 영수증 도구 = 다시 `_selftest` 안만 (AST: 최상위 문 59 중 바뀐 것 = `_selftest` 하나 · `_selftest` 앞 · 뒤 글 바이트 같음) · sha256 `3d6110be…` → `7ad98a0b…` · 봉인 32 · 인계 도구 2 · 배포 빌더 · 실행기 · 스모크 = `git diff --quiet 7f99be67c <보강 판>` rc 0 (`code_fp` 그대로) · 그 밖에 바뀐 파일 = ⟦CHANGED_FILES⟧ |

## 3. 질문

- **Q1.** 비준판 문안이 판정문 §5 ① — 대기 선언을 승인 지문으로 자동 취급하지 않음 · 역사 보존 · 결과 열람 뒤 변경 이력 — 을 채우는가.  (실측: 보충 `registration_values` = §3 `2149f873…` · 대기 None · 문제 0 · 컨테이너 영수증 rc 0 · 비준 전 문서는 rc 1 [D1])
- **Q2.** 재결합 (묶음 §2 — 봉인 32 · 기대 세대 · 입력 ID · raw 표 · 코호트 TSV · 인계 도구 · 배포 빌더 · 지연 import 90 → 92 의 이유) 이 ② 를 채우는가 · 인계 도구 · 배포 빌더 지문을 194 §3 ✅ 줄에 두는 자리가 맞는가.
- **Q3.** B7 승인 핀 정의와 대조 자리 (P10 · E2 · D1 · F5–F7 · G5 · G7 · H1 · `runner.sha256` = 기록 전용 — 묶음 §3 · 그 표의 줄 번호 = 계산 트리 `a69963967` 판 · `_selftest` 뒤 줄은 판마다 움직인다) 가 ③ 을 채우는가.
- **Q4.** WSL 사전 점검 기록 (같은 핀 · 같은 지문 · fast16 + real4 · 관측된 의존성 = 보통 / 격리 (-I) 판 · P5 · P8 · 두 새 ROOT · 전체 로그 + 완료 영수증 · 194 손 대조 전체 값) 이 ④ 를 채우는가.  ⬜ 반입 뒤.
- **Q5.** S0b 의 새 기대 (+ 보강) 가 시험 약화가 아닌가.
  - 무엇: 앞자리 상수 둘 (`e8b2496b…` · `2149f873…`) 을 빼고 — 상태가 정한 지문 (registered = 등록 §3 · pending = 대기 선언) = 체크아웃 `code_fp` 64 자리 전체 · registered 면 대기 선언 없음 · 보충 등록의 (§3 · 대기) = 194 등록 (같은 함수 `registration_values`) · 두 등록 어느 쪽이든 봉인 지문 문제 = 거짓 (보강 `SUPR-04` — 옛 판은 194 쪽만) · 판정 = 경로 함수 `s0b_docs` 하나 (두 문서의 신원 = 실행기 등록 표 supp20 · production194 · S0b 가 실물 경로로 · S11h 가 섞인 경로 쌍으로 — 보강 `SUPR-05`).
  - 상수를 없앤 이유 · 잃는 것 · 막는 자리 = §6 (묶음 §6 Q3 (가) 원문은 상태별 **상수** — 구현은 상수 없이 체크아웃 지문과 두 등록을 대조한다 · 사전 리뷰 PRE-LHS-04).
  - 수 (S0b · fe23f2b83): 고치기 전 판 122/122 (pending) · 비준 사본 121/122 (S0b) → 새 시험 + 옛 식 122/123 (S11g) · 121/123 (S0b · S11g) → 고친 판 123/123 (둘 다 · 비준 커밋 트리도 123/123) · 변이 넷 (가드 하나씩 끔 · m1 · m2 = 커밋된 문서 · m3 · m4 = 비준 커밋 트리) = 넷 다 122/123 · S11g 실패 (잡은 꼴 = ratified_pending_left · supp_only_ratified + pending_base_differs · base_pending_conflict · undeclared).
  - 수 (보강 · 증거 §7): 사전 리뷰가 찾은 것 = 보충 쪽 상충 대기 둘 · 대기 = 등록 을 S0b 가 참으로 냄 (실물 자리 110/123 · S0b PASS · 합계는 S0 의 R0 가 막음) · 변이 여섯 (교차 대조 §3 만 · 교차 대조 앞 12 자리 · 상태 판정 앞 12 자리 · `REG194` = 보충 문서 · 194 문제 안 넘김 · 판정식이 `fp0_ok` 안 씀) 123/123 생존 → 시험 먼저 판 ⟦TF_REG⟧ → 고친 판 ⟦FIX_REG⟧ (registered) · ⟦FIX_PEND⟧ (pending) · 변이 13 = ⟦MUT_SUMMARY⟧ · 실물 자리 (고친 판) = ⟦INSITU_SUMMARY⟧.
  - 새 엄격: 한 등록만 비준한 트리 = S0b 실패 (옛 판은 194 만 비준이면 122/122 통과 · 보강 판 = ⟦ONE_SIDE⟧) — 맞는가 (증거 §3 · §5 · §7).
- **Q6.** 새 결함이 있나 — 있으면 등급 · 반례.

## 4. 회귀 (이 컨테이너 · `nice -n 19` · BLAS 한 스레드 · 60 s 안의 것은 그대로 · 넘는 것은 기계 전체 잠금 아래 한 번에 하나)

비준 커밋 트리:

| 시험 | 결과 |
|---|---|
| `scripts/supp20_input_receipt.py --selftest` | rc 0 · **123/123** · 상태 registered (35 s) |
| `scripts/g2_network_reread.py --selftest` | rc 0 · *"✓ 전부 통과"* · 검사 줄 ✓ 29 · ✗ 0 (12 s) |
| `scripts/run_network_194_parallel.py --selftest` | rc 0 · *"✓ 전부 통과 (139/139)"* (기계 잠금 아래 · 잠금 대기 포함 565 s) — 묶음 §4 단계 2 의 실행기 기대 139/139 와 같음 (이 컨테이너) |
| `python3 scripts/check_doc_refs.py` | rc 0 · *"✓ 깨진 참조 없음"* — 이 요청서 · 증거 README 마지막 판 (문서 커밋 직전 작업 트리) 에서 다시 돌려 같음 |
| `python3 scripts/check_review_findings.py` | rc 0 · *"원장 자기일관 ✓"* (26 s) |
| `python3 scripts/check_method_discipline.py` | rc 0 · *"0 오류 (15 경고)"* — 경고 15 = 다른 파일 (grade_engine · lhs_design_dataset · mpm3d 등 지역 import 그림자) · 이 커밋들의 파일 없음 (50 s) |
| 변이 m3 · m4 (`s0b_fp` 가드 끔 · 비준 커밋 트리) | 둘 다 122/123 · S11g 실패 (base_pending_conflict · undeclared) — 되돌린 뒤 도구 sha256 `3d6110be…` |

★ 보강 판 (이번 수정 커밋들 · 문서 커밋 직전 작업 트리 — 영수증 도구 · 두 등록 = 커밋할 바이트):

| 시험 | 결과 |
|---|---|
| `scripts/supp20_input_receipt.py --selftest` | ⟦FINAL_SELFTEST⟧ |
| `scripts/wsl_network_smoke.py --selftest` (fast16) | ⟦FAST16⟧ |
| `scripts/wsl_network_smoke.py --selftest-real` (real4 · 기계 잠금 아래) | ⟦REAL4⟧ |
| `scripts/g2_network_reread.py --selftest` | ⟦REREAD⟧ |
| `python3 scripts/check_doc_refs.py` · `python3 scripts/check_review_findings.py` · `python3 scripts/check_selftest_inventory.py` | ⟦DOC_CHECKS⟧ |

`scripts/check_all.sh` 전체 = 메인 (이 회차에서 돌리지 않았다) · 실행기 selftest = 위 비준 커밋 트리 값 (실행기 바이트 그대로 · 보강 판에서 다시 돌리지 않았다).
fast16 · real4 = 이 컨테이너에서도 돈다 (커밋된 case15 · real14 원자료 — 위 표 · 초안 2 의 *"이 컨테이너엔 원자료가 없다"* 철회 · 사전 리뷰 PRE-LHS-05) · 이 컨테이너에 없는 것 = LHS 원 dump (묶음 §4 단계 3 · 4 dry-run 의 원자료) · WSL 사전 점검 2 단계 = 발사 환경 (B7 핀 · WSL 의 Python · NumPy · SciPy 판) 실측 (Codex 10-20 판정 §5 ④ · 묶음 §4).

## 5. 하지 않은 것 (요청 범위 밖)

실제 194 · 보충 20 발사 · 결과 · §5 관문 · 인계 · v1.3 배포 · S3 · 재봉인 · A4 재수행 (봉인 32 무변경) · `scripts/check_all.sh` 전체 · 진행 기록 · CLAUDE.md (메인).
⚠ 정정 (사전 리뷰 PRE-LHS-05): 초안 2 의 *"묶음 문서 고침 (기대 수 = §0 표) · 원장 · 진행 기록 (메인)"* 은 메인이 `7f99be67c` 에서 했다 (묶음 기대 수 122/122 → 123/123 정정 표지 셋 · 원장 `SUPR-03` · 진행 10-21 07) · 이번 수정이 고친 것 = 묶음 기대 수 123/123 → 124/124 (정정 표지) · 원장 (`SUPR-04` · `SUPR-05` · `SELF-129` = open · claimed_fixed = 메인 반영 뒤).

## 6. 한정

- 수는 이 컨테이너 (Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · networkx 3.6.1) 의 실측이다 — WSL 실측이 아니다 (10-14 WSL = Python 3.12.3 · NumPy 2.5.2 · SciPy 1.18.1 · networkx 3.7).
- S0b 의 기대 = 상태 유도 (사전 리뷰 PRE-LHS-04 · 묶음 §6 Q3 (가) 의 원문 = 상태별 상수 — pending = 등록 `e8b2496b…` + 대기 `2149f873…` · registered = 등록 `2149f873…` + 대기 없음):
  ① 상수를 없앤 이유 — 재봉인 · 비준마다 시험의 상수를 고쳐야 했고 (안 고치면 정상 비준 상태가 121/122) 그 상수는 앞 8 자리 비교였다 · 상태 유도는 체크아웃 지문 64 자리 전체와 두 등록 (같은 함수) 을 대조한다.
  ② 잃는 것 — 체크아웃과 독립인 기대값: 코드와 두 등록이 **같은 새 값으로 함께** 바뀐 재봉인은 S0b 가 통과시킨다 (기준이 같이 움직인다) · pending 상태의 §3 값은 어떤 상수에도 묶이지 않는다 (두 문서가 같은 엉뚱한 §3 + 대기 = 체크아웃 = S0b 참).
  ③ 막는 자리 — 묶음 §5 손 대조 (code_fp 전체 값 ↔ 등록) · 영수증 D1 · E2 · F5 · G5 (= 등록 §3 값만 — 대기 선언을 통과시키지 않는다 · pending 상태는 여기서 막힌다) · 새 §3 값의 Codex 확인 · 1저자 비준.
- 보강 (`SUPR-05`) 의 두 문서 신원 = 실행기 등록 표 (supp20 · production194) 의 §2 케이스 수 · `ids_sha256` — 다른 문서가 같은 두 값을 담으면 가르지 못한다 · S11g · S11h 의 사본 = 실물 + 지문 토큰 변환 (다른 칸은 실물) · 변이 = 13 꼴 (전수 아님 · 증거 §7).

## 부록 A. 명령 · 출력 (이 컨테이너 · 10-21 · 작업 트리 = 비준 커밋 + 이 요청서)

```bash
C=fe23f2b839f0a49adb077348fec6d4c85443b62a; R=f82929b0644be39b44e9fba9ea04cf9d60de9146
FILES=$(python3 -c "import sys; sys.path.insert(0, 'scripts'); import run_network_194_parallel as N; print(' '.join(N.CODE_FILES))")
git diff --quiet 34713ac96 "$R" -- $FILES; echo "sealed32 rc=$?"
git diff --quiet 34713ac96 "$R" -- scripts/lhs_design_dataset.py scripts/g2_network_reread.py scripts/lhs_release_build.py scripts/run_network_194_parallel.py scripts/wsl_network_smoke.py; echo "tools rc=$?"
git diff --name-only "$C^" "$C"; git diff --name-only "$R^" "$R"
for d in docs/reviews/lhs_network_batch_registration_20261007_g2.md docs/reviews/lhs_network_batch_registration_20261012_supp20.md; do git show "$R:$d" | sha256sum; git show "34713ac96:$d" | sha256sum; done
git show "$C:scripts/supp20_input_receipt.py" | sha256sum; git show "a76f59d0d:scripts/supp20_input_receipt.py" | sha256sum
python3 - <<'PY'
import sys; sys.path.insert(0, 'scripts')
import run_network_194_parallel as N, supp20_input_receipt as S
print('code_fp', N.code_fp(N.code_hashes()))
v, p = S.registration_values(); print('supp', v['code_fp'], v['code_fp_pending'], p)
v1, p1 = S.registration_values(reg_doc='docs/reviews/lhs_network_batch_registration_20261007_g2.md')
print('194', v1['code_fp'], v1['code_fp_pending'], [x for x in p1 if x.startswith('등록 문서 code_fp')])
r = S.receipt(); print('receipt', r['rc'], sorted(c['id'] for c in r['checks'] if not c['ok']), len(r['checks']))
PY
```

출력 (요지 — 파일 목록은 줄여 적음):

```text
sealed32 rc=0
tools rc=0
C 가 바꾼 파일 = scripts/supp20_input_receipt.py · docs/reviews/selftest_inventory.tsv · docs/reviews/lhs214_relaunch_s0b_evidence_20261021/ (README.md + tests/ 로그 11)
R 가 바꾼 파일 = docs/reviews/lhs_network_batch_registration_20261007_g2.md · docs/reviews/lhs_network_batch_registration_20261012_supp20.md
194   @R 2c3ed36f97aa7ec8b0c377cfe3c07093b7902cb552f7bdc3da6a607659303114 · @34713ac96 7fd158cb5b130e2150e58e5938c92b80731fc3292ef8e363346adfc2b62e1699
보충  @R 7cad47d191445bb6adb4ae0c6aeebd4fb147c2ce3824792f365b47f8ebfd8397 · @34713ac96 b2389709695cf3e94095a1855014b44868914362d112e5e0e29d084fc9e11032
영수증 도구 @C 3d6110be24d24bf91ad1e71232a2e5dad580cf95178d6135b13aa6ca6de6f950 · @a76f59d0d 2c7e0b81dbe81d0518e27c8e1781959b9cc983509a1ce66001028faa3768a2f9
code_fp 2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb
supp 2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb None []
194 2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb None []
receipt 0 [] 11
```

- 날짜 자리 대조: 비준 커밋의 두 문서에서 `10-21 ·` 을 `⬜(날짜)` 로 되돌리면 비준 전 문서 (코드 커밋 판 = `a76f59d0d` 판 = 대조 핀 판) 에 묶음 diff (원문 그대로) 를 붙인 글과 같다 — 194 = 8 자리 · 보충 = 7 자리 (묶음 diff 의 `⬜(날짜)` 수와 같음) · 비준 전 문서에 `10-21 ·` 0 개.
- AST: `a76f59d0d` 판 ↔ 코드 커밋 판 — 최상위 문 59 · 바뀐 것 `_selftest` 하나 (끝 `if __name__` 블록 = 줄 번호만 다름).

## 부록 B. 보강 판 (이번 수정 · 이 컨테이너 · 10-21)

⟦APPENDIX_B⟧
