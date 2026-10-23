# 묶음 A′ 보고 — 사전 공격 리뷰 C1–C5 고침 (Rint ② RR · 10-23)

> 이 파일 = 묶음 A′ 에이전트 (작업 트리 · 가지 `rr-fix-a2` · 시작 `fdb48d378`) 의 마지막 보고를 메인 세션이 옮겨 적은 것 (내용 그대로).  메인은 `e07d8c63b` 를 fast-forward 로 받았다 (커밋 SHA 그대로).
> 지시서 = 메인 스크래치 `brief_a2.md` (1저자 10-23 *"권고대로 해"* = Q12–Q14 (가) 범위 · 사전 공격 리뷰 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack/PREATTACK_A.md` §A C1–C5) · 형식 = 지난 묶음 지시서 `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF.md` §보고.

C1–C5 를 모두 고쳤습니다. 커밋 7 개, 가지 `rr-fix-a2`, `fdb48d378` → `e07d8c63b` 입니다.
- 회귀 68 묶음은 전부 rc 0 입니다. 끈 경로는 고치기 전과 비트가 같고, SV 를 켠 꼴에서는 투영 칸이 더해지기만 했습니다.
- 변이 표는 29 개 중 첫 판에서 25 개를 잡았습니다. 생존 4 개는 상주 시험을 더한 뒤 4/4 잡았습니다.
- 남은 것: C1 은 일부 열려 있습니다. 끊은 수까지 맞춘 일관 편집 두 꼴과 위 끝 ← 아래 끝 증서 바꿔 끼우기는 지금도 받습니다. 정상 기록 하나 (FLOAT) 는 새로 거부합니다. 고르지 않았고, 결정 필요 1–3 에 적었습니다.
- 하지 않은 것: push · fetch · `scripts/check_all.sh`.
- 봉인 32 파일과 바뀐 파일의 겹침은 0 입니다. scratch 사본은 지웠습니다.

## 1. 커밋 (각 메시지 = `author 10-23 ratified Q12-Q16` + 끝 두 줄)

| 항목 | 커밋 | 무엇 |
|---|---|---|
| A7 C1 (Q12 가) | `5182fb1fc` | 투영이 증서 위상 수 `CERT_TOPO_KEYS` 를 싣습니다. `_topo_problem` 이 끝마다 주 해 증서 · 기록의 끊은 수와 대조합니다 (생산자 보장 관계 + 핵심 조건). `read_run` 은 주 해 증서 위상 수를 런의 주 증서와 대조합니다 (다르면 `CA_EXT_RECORD`). |
| A8 C2 | `9b920cc3b` | 시험만 추가했습니다 (`test_carbon_junction` QD6 · 방향 반올림 칼날). 리뷰 변이 M7 · M1 을 시험 안에서 잡습니다. |
| A9 C3 (Q13 가) | `7603139b6` | 최종 추정량 검사는 그대로 먼저 돕니다. 그 뒤 이미 구한 origin 마다 세 R 을 봅니다 (`origin_points` · `ORIGIN_NAMES` · `checks.r_monotone[].origins`). 멈춤 이름은 그대로이고, 사유에 origin 이름이 들어갑니다. |
| A10 C4 | `720e401eb` | `arm_band` = [scale·target_lo, scale·target_hi] (그 런 증서 · 정확 분수). `read_run` 이 증서 칸을 싣습니다 (`ARM_PUBLIC` 아님). 칸이 없거나 꼴이 틀리면 `ARM_UNREADABLE` 입니다. |
| A11 C5 (Q14 가) | `5cf848157` | kind · rule = `SV_CF_KIND` · `SV_CF_RULE` (생산자 상수와 같은 값) 만 받습니다. 투영 `_COPY` 에 rule 을 넣었습니다. 접두어 검사는 철회했고, 옛 이름 고정물 3 곳을 고쳤습니다. |
| A12 | `0945ff4db` | 원장과 등록 R 머리 줄입니다. |
| A12b | `e07d8c63b` | 변이 표 생존 4 를 잡는 상주 시험 (QD5 ⑤), QD5 문서 정정, 원장 증거 줄입니다. |

## 2. 시험 수 (새 시험을 고치기 전 코드에 얹어 돌린 수 → 끝)

기준선 (`fdb48d378`) = chain 232 · b6 427 · carbon_junction 356 · e2e 16.

| 항목 | 고치기 전 | 끝 |
|---|---|---|
| A7 | QD5 3/18 (묶음 예외로 중간 정지) · b6 427 PASS / 4 FAIL (S8t ×3 · S8h′) · chain V32 0/1 | carbon_junction 381 · b6 431 · chain 233 · e2e 16 |
| A8 | 시험만 · 글자 변이 (`--only QD2,QD3,QD4,QD6`): M7 46/53 · M1 49/53 (실패는 전부 QD6) | carbon_junction 392 |
| A9 | chain 228/236 (U17 · M44–M47 · U19 · M49 · V33) | 236/236 · e2e 16 |
| A10 | chain 236/239 (U20 · M50 · V34) | 239/239 · e2e 16 |
| A11 | b6 429/449 (S8w ×18 · S8w′ · S8q) · chain 239/240 (V35) | b6 449 · chain 240 · carbon_junction 392 · e2e 16 · 웹앱 labels 84 |
| A12b | 생존 변이 4 | QD5 32/32 · carbon_junction 399/399 |

시험 기대가 바뀐 곳 세 군데:
- b6 S8h 의 칸 이름이 바뀐 꼴은 진단 기록으로 옮겼습니다. 증서 구간 기록은 새 S8h′ 로 거부합니다.
- chain U17 ⑧ 은 PREDICTED 에서 corner_a0 멈춤으로 바뀌었습니다 (C3).
- b6 S8h 의 다른 정의 kind 받음 꼴은 S8w 거부로 옮겼습니다 (C5).

## 3. 회귀 (코드 `0945ff4db` · 전부 rc 0)

- chain 240/240 · e2e 16/16 · b6 449/449 · runner 128 · z1 95 · z3 84 · verdict 31 · s0 152.
- carbon_junction 392/392. A12b 뒤 `e07d8c63b` 에서 399/399 입니다.
- target_cert 빠른 판 260/260, `--long` 309/309 (heavy.sh · T17c3 생략 = 이 기계에서 OpenBLAS 경로가 안 바뀜 · T18 변이 37).
- conv_cert 27 · ptfe 242 · run_contract `--selftest` 124 · step3 `--selftest` · `--selftest-rint` PASS.
- `check_method_discipline` 오류 0 (경고 17) · `--selftest` 128/128.
- 웹앱 `webapp/test_*.py` 51 파일 전부 rc 0 (ca_ext_labels 84 · rint_explainer_page 62 · rint_scope_labels 31).

## 4. 끈 경로 (`fdb48d378` scripts 사본 대비)

- b6 `--old-scripts --only=B` 30/30: payload 일곱 꼴 모두 "허용된 칸 0" 입니다. B0 영수증 44 · B0b 34 짝이 같습니다.
- z3 `--old-scripts --only=O` 11/11: O1 face_alpha 의 σ · n_dof · cg_info · resid 가 비트 같습니다. O2 payload 다섯 꼴은 허용된 칸 0 입니다.
- SV 켬 (`--step3-cjunc-sv-cf` · rtol 1e-12 · fixture 셋: DBE · unsplit z 6.5 · z 12.5):
  - σ 셋 모두 같습니다 (0.00043695843728313 · 0.039231639340228545 · 0.03922245385285839). n_dof 도 같습니다.
  - 차이는 더해진 칸뿐입니다 (9 · 13 · 9 개): 증서 투영의 `target_n_*` 넷과 `rule`. 바뀐 칸 0, 빠진 칸 0.

## 5. 변이 표 (한 줄 되돌림 29 · 되돌리지 않은 사본 기준선은 전부 통과)

| 묶음 | 잡음 |
|---|---|
| C1 (14) | a 위상 검사 끔 · b 위 끝 n_sv_faces_cut = 아래 · c 아래 끝 판 결합 = 주 해 · e 끊은 것 없음 → 같음 · f 끊음 → 다름 · h 위 끝 판 결합 = 주 해 − npc · i 위 ≤ 아래 · l 위 끝 끊음 → 주 해와 다름 · m n_sv_faces_cut 필수 · n read_run 위상 대조 = 잡음. **d 아래 ≤ 주 해 · g 위 ≤ 주 해 · j 더 뺀 것 없음 → 위 = 아래 · k 끊은 것 없음 → 위 = 주 해 = 생존** (다른 검사에 가려졌거나 시험이 없었습니다) → A12b 뒤 4/4 잡음 |
| C3 (5) | origin 런 기록 안 함 · 8 팔 기록 안 함 · origin 검사 끔 · origin 멈춤 끔 · corner_a0 뺌 = 5/5 |
| C4 (7) | 옛 대칭 띠 · 검증 끔 · lo ≤ hi 뺌 · scale > 0 뺌 · 영값 지름길 끔 · err_rel 안 봄 · read_run 칸 안 실음 = 7/7 |
| C5 (3) | 접두어 검사 · rule 검사 끔 · 투영이 rule 버림 = 3/3 |

결과: 첫 판 25/29, 상주 시험 뒤 29/29 입니다. C2 는 위 §2 의 M7 · M1 줄입니다.

## 6. 탐침 재실행 (무변경 · `RINT_REVIEW_SOURCE` = 작업 트리)

| 탐침 | `fdb48d378` | 끝 |
|---|---|---|
| atk_sv A1 ×5 | 계약 None | 계약 None · 구간 같음 |
| atk_sv A2 | None · 표지 [] | 거부 (C1 문장) |
| atk_sv A4 (18) | 16 거부 · kind · rule = None | 18 거부 (kind · rule = C5 문장 · 나머지 16 = 같은 문장) · A3 같음 |
| atk_rmono R1 · R1b · R2 | PREDICTED · STOP (최종 추정량) · 칼날 찾음 | 무변경 = R2 에서 `arm_band` Stop 예외로 rc 1, 출력 없음 · 사본 = R_MONOTONE_VIOLATION · STOP · 칼날 없음 (200,000 회) |
| atk_rmono2 R1c · R1d | PREDICTED · PREDICTED | 무변경 = STOP ARM_UNREADABLE · 사본 = STOP R_MONOTONE_VIOLATION · STOP (넘친 모서리 12 · 최종 추정량 mean8 은 통과) |

- 사본에서 바꾼 줄: `arm()` 이 증서 칸 (`target_lo` 1−e · `target_hi` 1+e · `scale` σ · σ 0 이면 None) 을 싣고, R2 의 A · B 에 (lo · hi · scale 1.0) 을 싣습니다.

Codex 판정문 탐침 (`docs/reviews/codex_rint2_rereview_evidence_20261022/` 사본):
- registration 무변경: `fdb48d378` 은 rc 1 (R 단조 절 · REPORT_A 와 같음), 끝은 rc 1 (RCA02 절 ARM_UNREADABLE · 증서 칸 없음).
- registration 사본 (같은 증서 칸 + R 단조 절 Stop 기록): 옛 ↔ 끝 466 exact · 다름 0. Codex JSON 대비 464 exact · 다름 0 이고, R 단조 절 키만 다릅니다 (stopped R_MONOTONE_VIOLATION).
- certificate: 707 exact. selected 202/202 둘 다 (시간 줄만 다름).
- geometry: 1040 exact. 다름 2 = source sha 입니다. 더해진 칸 27 = 기록 투영의 위상 수 · rule 이고, 판정값은 같습니다.
- provenance: 37 exact. type 4 = F1 head · dirty (옛 사본은 git 밖) 로 REPORT_A 와 같은 환경 차입니다.
- s0: 34 exact.

C1 한계 탐침 (끝 트리 · 생산자 실기록):

| 꼴 | 계약 | 표지 @2 | 원래 |
|---|---|---|---|
| FLOAT (끊은 다리가 판에 안 닿는 성분) | 옛 None → 끝 거부 (⑥) | — | 정상 기록 |
| (a) SVX 아래 끝 ← 주 해 증서 + n_sv_faces_cut 0 | None | [] | SV_DEPENDENT |
| (b) QD2-3 위 끝 ← 주 해 증서 + n_edges_cut 0 | None | [] | SV_UNCHECKED |
| (c) QDX 위 끝 ← 아래 끝 증서 (끊은 수 그대로) | None | [] | SV_UNCHECKED |

## 7. 문서 · 원장 · 기타

- **등록 R** `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md`: 머리 줄 (묶음 A′) · §5-6 SV 행 (C1 · C5 단락) · §10 멈춤 문장 (위상 수 · origin 마다 · 띠 · 시험) · §10-2 ㊹ (C3 · C4 · 물을 것 칸 = 새 띠가 더 좁음) · §10-3 이름 행.
- **코드 문서**: `scripts/ca_ext_svcf.py` 모듈 머리 · `_pos_cert_problem` · `_topo_problem`, `scripts/rint_r_chain.py` STOPS · `arm_band` · `mean_band` · `_r_monotone`, `scripts/test_carbon_junction.py` QD5 문서.  QD5 문서 정정: 옛 문장 "census ≥ 기록 대조" 는 구현에 없던 내용이었습니다.
- **원장** `docs/reviews/findings.json`: RCA2-04 note 에 C1 `5182fb1fc` · C5 `5cf848157` · claimed_fixed_sha `df0f6f01c` → `5cf848157` · evidence 6 줄 추가.  RCA2-09 note 에 C3 `7603139b6` · C4 `720e401eb` · claimed_fixed_sha `aa2bf5a73` → `720e401eb` · evidence 3 줄 추가.  RCA2-01 evidence 에 QD6 줄.  새 ID 없음.  `check_doc_refs` · `check_review_findings` 커밋마다 rc 0.
- **`S0_SAME_FILES`**: 일곱 파일 중 바뀐 것은 없습니다. 바뀐 코드는 `ca_ext_svcf.py` · `rint_r_chain.py` 뿐입니다.
- **웹앱**: 해당 화면 없음. SV 줄 (`webapp/templates/mpm_lab.html`) 은 kind · rule · 위상 수를 보이지 않습니다. 사슬 멈춤 · R 단조 화면도 없습니다.

## 8. 결정 필요 (지금 동작 유지 · 고르지 않음)

1. **C1 ⑥ 거짓 거부 (FLOAT)** — 기록: 끊은 다리 2 · census 끊을 면 행 2 · 아래 끝 증서 = 주 해 증서 · 위상 수 (11, 12, 1, 1) · 비 1.0.  끝 트리는 이 기록을 거부합니다.  병렬 간선 꼴은 코드 읽기만 했고 시험 전입니다.  고를 것: 유지 / 생산자가 판에 닿는 성분의 끊은 수만 세기 (`scripts/carbon_junction.py` = S0_SAME_FILES 라 S0 보고를 다시 만들어야 함) / ⑥ 완화.
2. **끊은 수까지 맞춘 일관 편집 (a) · (b) 를 받음** — census 끊을 면 행 수는 생산자 보장이 ≤ 뿐이라 0 으로 고친 편집을 못 잡습니다 (코드 읽기).  등식으로 묶으면 거짓 거부 위험이 있어 넣지 않았습니다.
3. **위 끝 ← 아래 끝 증서 (c) 를 받음** — 생산자 보장은 위 끝 ≤ 아래 끝 (같음 허용) 뿐입니다.  더 뺐을 때 위 끝 < 아래 끝 은 생산자가 보장하지 않고, 비준된 핵심 조건은 주 해 기준이라 넣지 않았습니다.
4. 위상 수 자체를 지어 낸 위조는 이 대조 밖입니다.
5. **C4 σ 환산 = 증서 scale** — 근거는 계약 관계 I_bot × scale = 증서 σ 입니다.  대안인 게시 σ / I_bot 은 런마다 반올림이 다릅니다 (코드 읽기).  8 팔 평균 띠는 팔마다 그 scale 을 씁니다.
6. **C4 새 띠는 옛 대칭 띠보다 좁음** → 옛 띠가 겹쳐 지나던 증서 구간 모순도 이제 멈춥니다.
7. **C3 기록 꼴** — `ok` = 최종 추정량 결과입니다.  `origins` 는 최종 추정량 검사가 멈추면 None 입니다.  넘친 모서리는 `corner_a0` 와 `origin8_a0` 를 둘 다 봅니다.  origin 이름 글자를 확인해 주세요.
8. **C5** — 상수 이름 `SV_CF_KIND` · `SV_CF_RULE` 을 확인해 주세요.  `webapp/test_ca_ext_labels.py:197–202` 표시 고정물은 옛 kind 글자 그대로입니다 (렌더 전용).
9. **탐침 꼴**: `atk_rmono.py` · `atk_rmono2.py` · Codex registration 탐침은 증서 칸 없는 기록이라 끝 트리에서 ARM_UNREADABLE 입니다.  커밋된 증거 탐침을 고칠지 정해 주세요.
10. **REPORT_A #11 그대로**: b6 B · z3 O 에 SV 켬 꼴을 더할지 정해 주세요.

---

### 메인 메모 (10-23 · 옮겨 적은 뒤)

- 10 = 이미 정해짐 — 1저자 10-23 *"ㄱ"* (REPORT_A §10 결정 11) = 묶음 B 가 b6 B · z3 O 에 SV 켬 꼴 · 허용 행을 더한다 (시험만).
- 1 – 3 = 1저자 결정으로 올림 (등록이 정하지 않은 자리) · 4 – 9 = 지금 동작 유지 + Codex 회차 ① 요청서의 한정 · 질문으로.
