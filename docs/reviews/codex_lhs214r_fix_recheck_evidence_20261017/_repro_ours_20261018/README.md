# 우리 트리 재현 — Codex LHS214 수정 재확인 탐침 (코드 핀 `60ba39e22` · 2026-10-18)

판정문 `docs/reviews/codex_review_lhs214r_fix_recheck_20261017.md` 의 새 반례 셋 (원장 `L214R-R01` · `R02` · `R03` = Codex 표기 L214RR-01–03) 과 그 바탕 사슬을 **우리 기계 (Linux · Python 3.11.17 · NumPy 2.4.6 · SciPy 1.17.1)** 에서 다시 돌렸다.  Codex 탐침 파일은 한 바이트도 바꾸지 않았다.

## 어떻게

- 작업 사본 (리포 밖 scratch) = 이 반입 폴더의 묶음 뿌리 그대로 + `source/` = 코드 핀 `60ba39e22` 의 `git archive` (묶음 `source_manifest.json` 의 1,920 경로 · sha256 1,920/1,920 같음) + `base/` = 기준 `6cb256956` (`base_manifest.json` 682 · 682/682 같음) + 빈 `tmp/`.  묶음 README 의 의존성 폴더 둘 (`../lhs_coverage_review_20260930/deps` 등) 은 없다 — 같은 라이브러리를 시스템에 설치했다 (탐침은 없는 경로를 `sys.path` 에 넣기만 한다).
- 실행 = `python3 -E -X utf8 -B <탐침>` (탐침이 옆 모듈을 import 하므로 `-I` 대신 `-E`) · 묶음 README 의 순서.
  1. `probes/receipt_fences.py` (R03)
  2. `probes/numeric_adversarial.py` (R01 함수 수준 · 경계 · 같은 부류 대조)
  3. `probes/display_run_command.py fresh probes/display_fresh.py source` · `… fresh_base … base` (R02 · 수정 / 기준 트리)
  4. `probes/consumer_chain_derivative.py` — ★ 묶음의 `evidence/consumers_fixtures/` (Codex 기계의 생산자 출력) 를 **치우고** 실행해 작은 생산자 사슬 다섯 (ml_physics · ml_hertz · ml_el · independent_l1_h0 · independent_l2_h0) 을 **우리 기계에서 다시 만들었다** (원 탐침은 fixture 가 있으면 다시 쓰고 없으면 생산자를 돌린다)
  5. `probes/consumer_h0_resurrection.py` (R01 전체 소비 경로 — 4 에서 다시 만든 fixture 위)
- 대조 = `compare_probe_outputs.py <우리 evidence/> <이 폴더 evidence/> compare_probe_outputs.json` (읽기만).  우리 출력 여섯 파일의 sha256 = `compare_probe_outputs.json` 의 `ours_dir_files` (출력 자체는 넣지 않았다 — 크고 다시 만들 수 있다).

## 결과 — 판정값 차이 0

| 탐침 | 우리 | Codex | 같음 |
|---|---|---|---|
| receipt_fences (R03) | 네 백틱 안 예시 §3 = rc 0 · 실패 칸 [] / 세 백틱 예시 = rc 1 · R0 · D1 | 같음 | ✓ (§3 본문 · 사유 · 읽은 code_fp 까지) |
| numeric_adversarial — H0 복원 (R01) | 복원 전 NOT_COMPUTED · full_over_conduction · 표지 True · 배포 HOLD 문구 → 복원 뒤 OK · f 1.62317474 · 표지 False · content / record (True, ok) · 0b None · 증서 결합 [] · 배포 HOLD [] | 같음 | ✓ |
| — Physics 복원 | q 2.593468501694396 · OK · f 2.5934685 | 같음 | ✓ |
| — 경계 | raw q 1.5 · 1.4999999999999998 = computed · 1.5000000000000002 · 2.0 = over_conduction_guard · 저장 q 1.5 · 1.5 · 1.5 · 2.0 · 라벨 복원 뒤 게시 증서 판정 넷 다 None (통과) | 같음 | ✓ |
| — 채택 시도 252 변이 · 장부 36 | 수용 0 · 예외 0 · 실패 0 | 같음 | ✓ |
| — 알려진 K1 · K2 | (inf, 3.0) · inf · OverflowError | 같음 | ✓ |
| display_fresh source (R02) | 13 검사 중 실패 7 (세 레이아웃 · 두 유도값 모두 옛 값의 Δ) · 21 사례 화면 행 전부 같음 | 같음 | ✓ |
| display_fresh base | 실패 10 · 21 사례 같음 | 같음 | ✓ |
| consumer_chain (생산자 다시 만듦) | 다섯 사례 done · τ 상태 · 독립 표지 · 주 타깃 HOLD · 다시 읽기 K1–K7 ok 전부 같음 | 같음 | ✓ |
| consumer_h0_resurrection (R01 전체) | 앞 8 leaf 만 = 정지 ④ 거부 (같은 문구) · 10 leaf (+ 소산 몫 0.797464) = content · record · 정지 ①–⑨ (True, ok) · 증서 수치 무변경 True · leaf 차이 10 · 10 · 10 · 6 · build_v13 = 27 파일 · warnings [] · tau_reread performed · generation g2 ×3 · check_v13 [] | 같음 (out_dir 경로만 다름) | ✓ |

## 판정값이 아닌 차이 (적어 둔다)

- 원 q 끝자리 — H0 `1.6231747351909949` (우리) ↔ `1.6231747351909995` (Codex) · L1 `8.927503013108016` ↔ `…073` · H12 `2.7392746689761913` ↔ `…824` · L2 H12 `44.915381677294796` ↔ `…469` (L2 H0 · Physics 는 같음).  보충 판정 메모 §3 이 제출 Linux ↔ Windows 에서 본 것과 같은 크기 · 8 자리 반올림 (게시 칸) 같음 · 1.5 와의 대소 같음.
- 복원 뒤 τ² `5.529890768418778` ↔ `5.52989076841878` · φ_mc `8.975979010256552` ↔ `…554` (같은 부동소수 끝자리).
- 실행 ID · 출력 경로 · 다시 읽기 검사 문구 안의 ID.

## 한정

- 이것은 **Codex 반례가 우리 트리에서도 같은 판정을 낸다**는 확인이지 수정이 아니다 — R01–R03 은 열린 그대로 (수정 계획 `docs/reviews/lhs214rr_fix_plan_20261018.md`).
- 탐침의 합성 범위 (배포 fixture 214 행 중 선택 1 행만 실제 경로 · 계약용 합성망 · 부피분율 > 1) 는 판정문 · `docs/reviews/codex_lhs214r_fix_recheck_evidence_20261017/notes/consumers.md` 의 한정 그대로.
