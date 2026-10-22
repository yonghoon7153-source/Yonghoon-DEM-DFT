# Rint ② PF2 단계 ② 보고 — 사전 리뷰 2 회차 고침 A–H (10-22 · 연장 세션 pqwtv8)

> 근거 = 브리프 `docs/handoff_rint_pf2_20261022/pf2_fix_BRIEF.md` · 결정 = 수정 계획 `docs/reviews/rint2_design_fix_plan_20261021.md` §6 (1저자 10-22 Q1 (다) · Q2 · Q3 권고대로 · 쉽게 말하면 상자 ① ② ③).
> 범위 = 커밋 `89e596954` 뒤 31 커밋 (끝 커밋 `220158095`) + 이 보고 커밋.  묶음마다 메인에 fast-forward → 전체 게이트 "✓ 전부 통과" → push.
> 1저자 10-22 단계 ② 중 *"여기서는 안물어봐도돼"* ⇒ 등록이 정하지 않은 자리는 고르지 않고 지금 방식을 유지했다 → §6 "결정 필요" 에 모음.
> 숫자 = 각 묶음 에이전트의 실행 출력 (시험 판 · 범위 병기) + 메인 게이트.  정량 판정 · 런 결과 = 0 건 (코드 · 등록 문서 고침만).

## 1. 묶음

| 묶음 | 커밋 (기반 → 끝) | 무엇 |
|---|---|---|
| A — Q1 (다) SV 반사실 괄호 (PRE2-impl-01 · 04) | `89e596954` → `427452341` (4) | 시험 먼저 `8ca09822d` · `0ae9f9846` → 구현 + 웹앱 `eb571a458` (생산자 두 번 풀이 · 사슬 괄호 판정 · `mpm_lab.html` 두 곳 "[아래, 위] · 못 가른 덩어리 n" · 한정어 10 번째 문장) → 등록 §5-6 · ㉟ ㊱ `427452341` |
| B–E — 계획 하나 봉인 · 시간 · 같은 판 · 검증기 수 대조 (PRE2-design-01 · 02 · 03 · 06 · 08 · PRE2-impl-02 · 03) | `427452341` → `368c49ce6` (13) | B 계획 해시 정확 대조 (새 멈춤 `S0_REPORT_MISMATCH`) · §11 순서 (⑥ 숫자 탐침을 단계 2 앞으로) · C §10-4 다시 어림 (주 판정 ① ≈ 191–231 h · 추정 · 합성 침대 반복 비) + 결과 전 문장 셋 · D 코드 지문 12 + dirty 대조 · R 런 ↔ S0 census · registry 지문 · E SV 기록 수 재대조 · 계획 넘침 · 중복 칸 · 등급 칼날 |
| F–H — 문서 · 웹앱 상자 · 원장 · 회귀 · 끈 경로 · 변이 | `368c49ce6` → `220158095` (14) | F 낡은 "지금" 서술 16 + 같은 사실 7 · kgy 인자 (`--r-plan-path` · `--s0-plan` · `--after-main`) · 등급 문턱 = 정확값 G0/2 · G0 · §11 ④ · §3-2b ③ ③′ · 웹앱 설명 상자 ① ② ③ (다크 모드) · 등록 머리 줄 · G RCA-06 메모 · H 회귀 |

## 2. 시험 수 (고치기 전 → 뒤)

| 시험 | A (새 시험을 고치기 전 판에 → 고친 뒤) | B–E | F–H |
|---|---|---|---|
| `scripts/test_carbon_junction.py` | 313/327 → 327/327 | 327 | 327 |
| `scripts/test_rint_r_chain.py` | 176/179 → 179/179 | 179 → 217 | 217 → 218 (K01) |
| `scripts/test_ca_ext_b6.py` | 296/319 → 319/319 | 319 → 357 | 357 |
| `scripts/test_ca_s0_census.py` | — | 147 → 152 | 152 |
| `webapp/test_ca_ext_labels.py` | 54/68 → 68/68 | 68 | 68 |
| `webapp/test_rint_explainer_page.py` | — | — | 24 → 55 (시험 먼저 24/53) |

## 3. 회귀 · 끈 경로 · 변이

- 회귀 (끝 판 `220158095` 와 `35ed5486e` · F–H 에이전트 실행): chain 218 · e2e 16 · b6 357 · carbon_junction 327 · s0 152 · runner 128 · z1 95 · z3 84 · verdict 31 · target_cert 빠른 판 252 · `--long` 296/296 (heavy.sh · 한 검사 T17c3 = 이 기계에서 OpenBLAS 경로가 안 바뀌어 생략) · conv_cert 27 · ptfe 242 · run_contract 124 · step3 selftest 둘 PASS · 웹앱 18 파일 rc 0 · check_method_discipline 0 오류 · `--selftest` 128/128.
- 끈 경로 (`bf79d44c2` ↔ 끝 판 · payload 끝-끝 11 경우) = "차이 0" 이 **아니다** — 접합 끈 6 경우 = 매니페스트 차이 0 · σ 비트 같음 · 접합 켬 = σ 비트 같음 · 차이 = `qualifiers` 한 칸 (A 의 10 번째 한정어 · 의도) · SV 노브 켬 = 옛 SV 칸 값 같음 + 새 칸 5 (`bracket_rule` · `ratio_limit_hi` · `status_hi` · `sv_counterfactual_ratio_hi` · `upper`) · 못 가른 덩어리 0 = 위 끝 = 아래 끝 · 두 섬유 침대 = 아래 1.0 · 위 111.546.
- 변이 (고친 줄 한 줄 되돌림): A 19/19 · B–E 63/63 (판정문 Ml 포함) · F–G 23/32 — 생존 9 = 기계 검사가 없는 산문 · 원장 메모 되돌림 (새 규칙은 만들지 않음).
- 메인 게이트 (묶음마다 · `scripts/check_all.sh` 전체): A 끝 · B–E 끝 = "✓ 전부 통과" (156 ✓ · 0 ✗).

## 4. 원장

- `docs/reviews/findings.json` 은 RCA-06 하나만 바뀜 — 메모 덧붙임 ("10-22 사전 리뷰 2 회차 PRE2-impl-01 = 못 가른 다리 (옆 자리) → Q1 (다) 고침") · `claimed_fixed_sha` `3b3aa50e2` → `eb571a458` · evidence 8 · 상태 claimed_fixed 그대로 · 새 ID 없음 · 다른 804 항목 바이트 같음.

## 5. 문서 고친 자리

- 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md`: 머리 줄 · §2 · §2-1 · §2-1b · §3-2b · §5-2 · §5-6 · §10 · §10-1 · §10-2 (㉟–㊸ · ⑪) · §10-3 · §10-4 · §11 · §12 · §13 · §13-2 (새 · PF2-Q1).
- kgy 명령 `docs/reviews/rint2_kgy_commands_20261020.md` · 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` (§3-2 · §4-1 · §7 · K4).
- 웹앱 `webapp/templates/mpm_lab.html` (SV 줄) · `webapp/static/explain/rint_overview_20261021.html` (상자 ① ② ③ · 용어 "SV 반사실 비" · 10-31 문장).
- 증거 `docs/reviews/rint2_pf2_fix_evidence_20261022/` (E 의 여유 실측 · 이 보고).

## 6. 결정 필요 (고르지 않고 지금 방식 유지 · 묶음 순 번호)

A
1. 모서리 묶기 — 브리프 글은 배타처럼 읽힌다 ↔ 지금 사슬은 두 표지 (`SV_DEPENDENT` · `SV_UNCHECKED`) 를 함께 붙인다 (등록 ㉟).
2. 아래 끝 못 읽음 + 위 끝 ≤ 문턱 → 지금 = `SV_UNCHECKED` (글자 순서대로면 "표지 없음") (㊱).
3. 증서 오차를 SV 문턱 비교에 넣는 방식 — 지금 여유 없음 · 두 끝 같게 (등록이 정하지 않음).
4. 생산자 자기 표지 (`flag`) = 아래 끝만 읽음 (이 배선의 문턱 = 늘 None).
5. census 불일치 때 위 끝 상태 이름 `unsplit_census_mismatch` — 이름 승인.
6. `CJUNC_QUALIFIERS` 10 번째 문장 = 모든 접합 런의 `qualifiers` 칸이 바뀜 (세대 표지는 안 올림).
7. "아래 ≤ 위" 수치 대조의 여유 → E 에서 증서 폭 꼴로 구현 (아래 17).

B–E
8. 새 멈춤 이름 `S0_REPORT_MISMATCH`.
9. 단계 2 보고 = 새 DBE 킷만 · 단계 1 = 새 SBE 킷만.
10. 예측 · 판정은 보고 파일을 다시 읽지 않고 사다리 요약에 남은 투영을 같은 함수로 대조.
11. §10-4 ② 감도 줄 = 옛 어림 그대로 ("더 길다 · 추정" · 결정점 ① 에서 다시).
12. 지문 대조 코드 파일 12 — 뺀 것 (`mpm3d_compaction.py` · payload 가 부르는 `ca_ext_cjunc` · `additives` · `se_material` · `lens_geometry` · `step4_dyn` · `rint_cycle_traj`) 은 HEAD + dirty 로만 막힌다.
13. dirty = 저장소 전체의 추적 파일 · git 밖에서 돌면 기록만.
14. `runner_path` 가 대조 키에 남음 (Q3-b 로 기계를 늘리면 같은 절대 경로가 필요).
15. 기계 이름표 = 글자 · 숫자 · `_` · `-` · 길이 상한 없음 · 판정 단계에 주면 rc 2.
16. S0 보고의 git_head · git_dirty = 기록만 (대조 = 일곱 파일 지문).
17. 여유 (1−τ)/(1+τ) (τ = 1e-4 · 증서 폭 꼴) 를 증서 없는 기록에도 적용.
18. 사슬의 SV 읽기 = 유한 양수 · +∞ 만 (여유 하한 = 검증기 몫).
19. G_full · G_cut = float 만 (정수 · bool 거부).
20. 중복 칸 거부를 R 계획 밖 (S0 보고 · 사슬이 읽는 S0 계획) 으로 넓힘 · 점 수 상한 넘침 = 구조화 멈춤.

F–H
21. 판정문 "15 곳" ↔ 행 번호로 세면 16 — 16 전부 + 같은 사실 7 자리 고침 · 판정문 (반입 기록) 은 안 고침.
22. 판정문 표 밖 같은 부류 2 자리 (설계 v1 K4 · §3-2 raster) 도 표지 (뜻 바꿈 없음 · 범위 넓힘).
23. 웹앱 그림 6 은 날짜만이 아니라 순서도 상자 ② 로 다시 그림 (범위 넓힘).
24. 상자 색 = 새 토큰 `--hl` · `--hlb` (밝은 #fff4d6 · #c9932a / 어두운 #2c2516 · #e0a54a) — 1저자 확인.
25. §13-2 PF2-Q1 (끝을 늘린 뒤 다시 좁힐지) = 새 Codex 질문 — 요청서로 옮기는 것은 Codex 요청 때.
26. RCA-06 = claimed_fixed 그대로 (verified = Codex 몫) · sha 만 `eb571a458` 로 (옛 sha 는 메모에).
27. 원장 RCA-07 증거 "--long 297/297" ↔ 이 기계 296/296 (T17c3 환경 생략) — 안 고침.
28. check_doc_refs 는 같은 줄에 '커밋' 낱말이 없는 번호를 UNSURE 로 둔다 — F 가 더한 네 자리만 고침 · 검사기 규칙은 그대로.
29. 산문 · 메모 되돌림 변이 생존 9 = 기계 검사 없음 · 새 규칙 안 만듦.
30. 등록 §2-1 의 s_min_um 값 ↔ §2-1b = 손 확인 (관문은 값을 대조하지 않음).

## 7. 다음 (단계마다 1저자 승인)

- ③ 짧은 독립 재확인 (고친 사람 설명 없이 · 판정문 탐침 재실행 + 고친 자리 새 반례) → 게이트 → push.
- ④ stoic-knuth 로 fast-forward 병합 인계 문서 (꼴 = `docs/handoff_merge_to_stoic_knuth_20261020.md`).
- ⑤ (1저자) 10-23 kgy 재압밀 → S0 단계 1 → ⑥ 숫자 탐침 → Codex 요청.
