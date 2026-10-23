# Rint ② 재검토 결함 고치기 — 묶음 A 보고 (10-23)

> 지시서 = `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF.md` 묶음 A (A1–A6) · 1저자 10-23 *"다 권고대로 해줘"* (수정 계획 Q1–Q8 전부 (가)).
> 작업 = 격리 작업 트리 에이전트 · 가지 `rr-fix-a` · 시작 `49a1af626` → 끝 `bd0e85ce6` · 메인 = fast-forward (같은 SHA).
> 이 파일 = 에이전트 마지막 보고를 메인 세션이 옮겨 적은 것 (하네스가 하위 에이전트의 보고 `.md` 파일 쓰기를 막았다).  숫자 = 에이전트 실행 출력 · 메인 재확인 = 병합 뒤 전체 게이트 (같은 시험 묶음을 다시 돈다).
> 하지 않은 것 (지시서대로): push · fetch · `scripts/check_all.sh`.  봉인 32 파일 · `se_material.py` · `lens_geometry.py` = 바뀐 15 파일과 겹침 0.  새 숫자 문턱 없음.

## 1. 커밋 (각 = `author 10-23 ratified Q1-Q8` + 끝 두 줄)

| 항목 | 커밋 | 무엇 |
|---|---|---|
| A1 RCA2-08 | `ddbb6cee3` | 최종 U · W 합 넘침 → `NOT_CERTIFIABLE` · 원장 허용폭 넘침 = 원장 문제 (시험 같은 커밋 · T24 고치기 전 1/7) |
| A2 RCA2-01 · 04 | `ad32382f6` 시험 → `df0f6f01c` 코드 → `584472daf` 웹앱 → `435e73732` 등록 | SV 문턱 = 증서 구간 판정 · 기록 계약 조임 · `read_run` 이 기록의 주 증서를 런의 증서와 대조 (`CA_EXT_RECORD`) |
| A3 RCA2-09 | `c18f39d71` → `aa2bf5a73` → `385e872a0` | `Predict` 안 DBE R 단조 방어 검사 · 새 멈춤 `R_MONOTONE_VIOLATION` |
| A4 RCA2-06 | `b72105582` · `149597bf2` 시험 → `afa5cad8b` 코드 → `1f0a84cb6` 등록 | F4 = 두 성분 상주 시험 QD4 (코드 변경 없음) · F6 = 검증기가 `unsplit_census_mismatch` 를 자기 꼴로 받음 (`_mismatch_problem`) · 사슬 사유에 상태 이름 (`sv_corner_label`) · 시험 = `run_contract.ca_ext_record_ok` 경로 |
| A5 | `dc0c0d1d0` | 원장 |
| A6 | `fba004f2d` · `bd0e85ce6` | 변이 생존 7 을 잡는 상주 시험 · 원장 증거 줄 |

## 2. 시험 수 (고치기 전 판 → 새 시험의 고치기 전 결과 → 끝)

| 묶음 | 고치기 전 | 새 시험 · 고치기 전 판 | 끝 |
|---|---|---|---|
| target_cert 빠른 판 | 252 | T24 1/7 | 260 |
| target_cert `--long` | — | — | 309/309 (T18 변이 37 잡음 · T17c3 생략 = 이 기계에서 OpenBLAS 경로 안 바뀜) |
| conv_cert | 27 | — | 27 |
| carbon_junction | 327 | 20/41 (A2) · 15/16 (A4) | 356 |
| b6 | 357 | 357 통과 / 31 실패 (A2) · S 꼴 195 / 29 실패 (A4) | 427 |
| chain | 218 | 13/18 · 3/9 · 4/6 | 232 |
| e2e | 16 | — | 16 |
| 웹앱 labels | 68 | 68 / 16 실패 | 84 |
| 웹앱 explainer | 55 | 54/62 | 62 |

## 3. 회귀 (끝 트리 · 전부 rc 0)

chain 232 · e2e 16 · b6 427 · runner 128 · z1 95 · z3 84 · verdict 31 · carbon_junction 356 · s0 152 · target_cert 260 빠른 판 / 309 `--long` · conv_cert 27 · ptfe 242 · run_contract 124 · step3 selftest 둘 PASS · `check_method_discipline` 오류 0 (이름 묶음 경고 17) · `--selftest` 128/128 · 웹앱 `webapp/test_*.py` 51 파일 전부 rc 0 (지난 회차 18 파일 목록을 못 찾아 전부 돌림 · scope_labels 31).

## 4. 끈 경로 (노브 끔 · 고치기 전 스크립트 사본 ↔ 끝 트리)

- b6 `--old-scripts --only=B` 30/30.  노브 끔 차이 = cjunc 꼴의 한정어 문장 하나뿐 (기존 RCA1 행이 허용).
- z3 O 11/11.
- 10 꼴 자세한 비교: σ = 10 꼴 전부 비트 같음 · 노브 끔 꼴 차이 0 · SV 켬 꼴 = 새 SV 칸만 더해짐 (차이 3 · 20 · 37) + 한정어 줄 · 기존 SV 값 변화 0.

## 5. 변이표 (한 줄 되돌림 41 · 작업 사본)

- 첫 판 = 34/41 잡음 (A2 28 중 22 · A3 5 중 4 · A4 8 중 8).
- 생존 7 = 다른 검사에 가려진 것 (행동이 빠진 것 아님): A2-c7 · c8 · c9 · c10 · c17 (변조한 S8n 꼴이 `ratio_cert_interval` 를 낡은 채 둠) · A2-c15 (`cert_interval` 영 그래프 표지) · A3-r3 (같은 R 가지 · 방어용).
- 새 b6 시험 S8s (일관 변조 48 꼴) · S8r · chain U17b → 다시 돌림 7/7 · 전체 41/41.

## 6. 판정문 탐침 무변경 재실행 (`RINT_REVIEW_SOURCE` = 고친 작업 트리)

- registration: rc 1 — 실제 `Predict` 가 이제 `R_MONOTONE_VIOLATION` 으로 멈추고 탐침이 그것을 잡지 않는다 (= RCA2-09 수정).  그 함수만 감싼 실행에서 나머지 10 절 = Codex JSON 과 같음.
- certificate: 5 노드 넘침 = `OverflowError` 대신 구조화 `NOT_CERTIFIABLE` 기록.  그 밖 차이 = 10-22 재현과 같은 환경 반올림.  선택 시험 202/202.
- provenance: `F1_actual_nongit` 만 다름 (작업 트리가 git 체크아웃 · 판정문 REPRODUCTION.md 경고대로) · s0 같음 — 둘 다 묶음 B 몫.
- geometry (같은 회로 · 증거 완비해 다시):
  - 문턱 넘김: 표지 [] → `SV_DEPENDENT` · 구간 = Codex 와 같음.
  - 기록 변이: 증서 켬에서 7/7 거부.
  - census 불일치: 받음 · `SV_UNCHECKED` · 사유에 상태 이름.
  - 첫 성분만 지우는 생산자 변이: 검증기는 통과 (안에서 일관) — 잡는 것은 QD4.
  - 한정: 탐침이 증거를 census · `I_bot_code` · fp 없이 만들어, 조여진 기록 계약이 탐침의 정상 기록을 그 칸 없음으로 거부한다.

## 7. 원장

RCA2-01 · 04 → claimed_fixed `df0f6f01c` · 06 → `afa5cad8b` · 08 → `ddbb6cee3` · 09 → `aa2bf5a73` · 증거 = 시험 이름 · 수 (고치기 전 수 포함) · RCA-06 `partial_note` 한 줄 · 새 ID 없음 · `check_review_findings` · `check_doc_refs` rc 0.

## 8. 문서

등록 R (10-23 머리 줄 · §5-6 SV 행 · 쉽게 말하면 상자 ④ · §5-6a · §10 멈춤 목록 · §10-2 ㉟ ㊱ ㊶ ㊷ ㊹ ㊺ · §10-3 이름) · `webapp/templates/mpm_lab.html` (두 행) · `webapp/static/explain/rint_overview_20261021.html` (상자 ④).  웹앱에 사슬 멈춤 · SV 사유 화면은 없다 (SV 줄은 이미 "위 끝 unsplit_census_mismatch" 를 보인다).

## 9. `S0_SAME_FILES` (`scripts/rint_r_chain.py:158`)

일곱 중 둘 바뀜 — `carbon_junction.py` · `step3_sigma.py` (`df0f6f01c`).  ⇒ S0 단계 1 · 2 보고는 끝 핀 (이 묶음 뒤 코드) 에서 다시 만들어야 R 에 쓴다.

## 10. 결정 필요 (지금 동작 유지 · 고르지 않음)

1. 이름: `certified_interval` · `diagnostic_uncertified` · `ratio_cert_interval` · `uncertified` · 영 그래프 `cjunc_sv_counterfactual`.
2. 계약에 넣은 census 순서 규칙 (unsplit ≤ bridging ≤ touching).
3. 주 증서 불일치 = 기존 `CA_EXT_RECORD` 재사용 (새 멈춤 이름 없음).
4. 위비 넘침 → None · 아래비 넘침 → 최대 float.
5. 생산자 nominal `flag` 유지 · 웹앱이 "판정 아님" 표시.
6. 무증서 기록 = 계약은 받고 판정 입력은 아님.
7. cjunc 런마다 한정어 한 문장 바뀜.
8. R 단조 띠 = 증서 오차만 · τ_mono 안 더함.
9. `R_MONOTONE_VIOLATION` = 멈춤 (표지 아님) · `BLOCKING_FLAGS` 그대로.
10. A4: 빈 칸 목록 · 무증서 사유에도 상태 이름 · 위 끝이 불일치여도 아래 > t 면 `SV_DEPENDENT` · QD4 시험 문턱 2.5 = 시험값.
11. b6 B · z3 O 에 SV 켬 꼴 · 허용 행을 더할지.
12. Codex 가 geometry 탐침 증거에 census · `I_bot_code` · fp 를 넣을지.

## 11. 남은 것

묶음 B (Q2 · F5 · Q3) · 묶음 C (Q4 · Q9 · RCA2-07 · C6 #7 · #17 · 상자 ⑤ ⑥).  claimed_fixed 다섯 = Codex 검증 전.
