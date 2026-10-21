## D (사슬 · 배선 통합) 보고 — 기반 `a76f59d0d`

브리프 묶음 1–6 과 코디네이터 항목 1–7 을 모두 넣었습니다. 회귀 24 개는 전부 통과했고, 새 노브를 다 끈 경로는 a76 과 차이 0 입니다.

**정해야 할 것이 하나 있습니다.** C 의 4판 (로컬 `12e2704d3`, 미병합) 은 단락 (ELECTRODE_SHORT) 을 `NOT_COMPUTED` 로 정했습니다. 저는 3판대로 단락을 +∞ 로 받고 payload 가 단락 팔을 게시하게 구현했습니다 (4판 R4-Q5 의 "+∞ 게시" 쪽). 둘 중 하나를 골라야 하고, 그 밖의 4판 사슬 규칙도 아래 §4 처럼 아직 들어가 있지 않습니다.

worktree `/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82`, 브랜치 `worktree-agent-afe53be7bdb176c82`, HEAD `5dabe6156`. 커밋 10 개, push 안 함, 트리 깨끗.

### 1. 커밋 (시험 먼저 → 구현)
| SHA | 묶음 | 고치기 전 → 뒤 |
|---|---|---|
| c0ab44ac2 → 17f1afbc2 | 영값 · 단락 상태 + SV 반사실 노브 배선 | b6 S+SP 40/83 → 88/88 · runner 16/21 → 21/21 |
| aa37d2d26 → 8090517c2 | SV 증거를 D 모듈 `scripts/ca_ext_svcf.py` 로 (Q-D) · centerline + 접합 입구 거부 (Q-C) | b6 S,P 145/151 → R,P,S 256/256 · runner N6 56/59 → 97/97 |
| 2c4510d88 → 92f5e56f2 | 사슬 3판 + Q-E · Q-F · Q-G | chain 15/139 → 139/139 · e2e 0 PASS 5 FAIL → 13/13 |
| 6e0171bf6 → bce88b913 | 웹앱: 해 상태 · SV 비 · 접합 한정어 | 34/54 → 54/54 |
| e0b4caee3 → 5dabe6156 | `--old-scripts` 허용 목록 하나 (b6 B1 · z3 O) | B0u 0/1 → 21/21 · B 대 47d 5P3F → 30/30 |

- 92f5e56f2 에서 시험을 두 곳 고쳤고 커밋 문장에 밝혔습니다.
  - L13: 옛 세계 (잡음 범프) 는 끝 런 사이가 비단조라, 3판의 정답은 `CALIB_NONMONOTONE` 입니다. 그래서 매끈한 로지스틱 세계로 바꿨습니다.
  - M13 · M14: 변이가 KeyError 로 죽지 않고 값으로 실패하게 고쳤습니다.

### 2. 반례 값 (고치기 전 → 뒤)
| 반례 | 2판 | 3판 |
|---|---|---|
| RCA-01 · PRE-design-05 | 비 8.341 · W 0.4194 PASS · 시험이 M2 (비 189.4 FAIL) 를 통과 | R_lo 10,000 · R_hi 5,990,349.75 · 비 599.03 · 12 점 · W 0.785238 CONSISTENT_WEAK · M12 (= M2) 잡힘 |
| RCA-02 | [3.4962, 4.6867] W 0.2930 PASS | 세 R 점검 → 8 팔 평균 · [2.6629, 6.1450] W 0.8362 WEAK |
| RCA-08 | hull W 0.351 PASS | GAP_ENVELOPE_ONLY |
| RCA-09 | no-op 변이 W 0.0335 FAIL (거짓 SENSITIVE) · 넓은 끝 변이 놓침 | no-op = PASS 유지 · 넓은 끝 변이 → FIBRE_SENSITIVE |
| RCA-10 | 와일드카드 (DIA 때문에 PASS 문장 영구 금지) | 닫힌 차단 집합 11 · ASSUMED_UNVALIDATED 는 보고 범주 |
| RCA-13 | σ 0 → ARM_UNREADABLE · 단락 → CA_EXT_RECORD 멈춤 | zero 받음 (실제 payload E8: σ 0.0 · VALID_ZERO_TOPOLOGY) · 단락 +∞ (§4 첫 줄) |
| RCA-06 | sv_dominant 가 실런에서 늘 걸림 | 반사실 비 > 문턱 → SV_DEPENDENT · 못 읽음 · 문턱 없음 → SV_UNCHECKED |
| PRE-design-01 | hi 끝 1,303,993 에서 arm 1 · 2 σ 1.60669 가 띠 안 | 끝을 바깥으로 밀어 세 origin 모두 띠 밖 |

### 3. 코디네이터 항목 1–7
| # | 상태 | 근거 |
|---|---|---|
| 1 PRE-impl-04 (Q-D) | ✅ 사슬 · 배선은 비 · 상태 · 표지만 읽음. 종류는 `counterfactual*` 면 정의 무관, `n_*` 칸은 이름 그대로. 모르는 상태 = 비 없음 → SV_UNCHECKED | b6 S8h · S8i · `ca_ext_svcf.chain_view` |
| 2 PRE-impl-08 | ⚠ 부분. 화면은 `evidence.qualifiers` 를 그대로 띄우고, 세 표지는 렌더 결과에서 확인 (W14). `LABEL_CJUNC` 는 A 파일이라 손대지 않음 → 문구 제안 §6 | web W14a · W14b |
| 3 PRE-design-01 (Q-E) | ✅ 끝 origin 밀기 · 세 origin 합집합 · W 도 그 끝으로 | U10 · L21 · M21 · e2e E1 |
| 4 PRE-design-05 | ✅ 기대값 599.03 · W 0.785238 · 12 점 | U01 · M12 |
| 5 Q-C | ✅ payload `S2_CJUNC_REFUSED\|PTFE_CENTERLINE\|` · 러너 `RUNNER_CA_EXT\|PTFE_CENTERLINE\|` (P0 · P1) | b6 P · runner N6 · N6b |
| 6 Q-F | ✅ 감도 단계는 `--after-main` (주 예측 폴더) 필수, 판정에서 sha256 로 묶음 대조 | F01–F04 · M25 |
| 7 Q-G | ✅ 결과 전 숫자 넷 중 하나라도 null 이면 첫 σ 런 전에 `PLAN_NUMBER_UNREGISTERED`. 지시 ("S0 단계 2 뒤로 못 감") 보다 앞에서 멈춤 | N01–N03 · M24 |

### 4. ⚠ C 4판과 지금 사슬 (`92f5e56f2`) 의 차이 — 4판이 "사슬에 아직 없는 규칙" 으로 적은 것
| 4판 규칙 | 지금 사슬 | 고칠 자리 |
|---|---|---|
| §5-0 단락 = NOT_COMPUTED (R4-Q5) | +∞ 로 받음 · payload 가 σ None + 증서로 게시 · check_arm 이 받음 | `_step3_early` · `sr01_stamp_compare.check_arm` · `run_contract.next_gen_state` · Z02 · Z04 |
| §3-2c NOT_COMPUTED 이름이 먼저 | CALIB_* 가 이김 | `judge_set` |
| §3-2b ③″ 보호 띠 (판독 ± 증서 오차) | 없음. 증서 오차 0 이면 같은 출력 | `outside_band` · `end_pick` · EDGE |
| §4-2 W₊ · origin 상태가 다르면 넘음 | W0 = ∞ 면 전환 없음 · 상태 비교 없음 | `dbe_origin_ok` |
| §5-5b 결정표 오른쪽 칸 (차단 표지 목록 문장) | PASS + 차단 = 문장 없음 · 목록 문장 없음 | `DECISION` |
| §5-6 변이 NOT_COMPUTED → `<V>_UNCHECKED` | `<V>_SENSITIVE` | `assemble` |
| 한정어 ⑰ (감도 미완료) · ⑱ | `QUALIFIERS` 16 개 | — |
| §2-1 R 계획 = `rint-r-plan-v1` (칸 7) | 사슬은 `rint-r-plan-v2` (칸 11) | 문서 쪽 (C) |

브리프에 없고 Codex 질문 (R4-Q*) 이 걸려 있어 구현하지 않았습니다. 시키면 시험 먼저 한 묶음으로 넣겠습니다.

### 5. 등록이 정하지 않아 제가 정한 곳
| 자리 | 결정 |
|---|---|
| SV 문턱 비교 | 비 > 문턱 (등록 문장 "넘으면"). producer 자기 표지는 ≥ 인데, 배선이 문턱을 None 으로 넘겨 쓰이지 않음 |
| SV 반사실을 도는 곳 | 주 예측의 DBE 모서리만 (계획 `sv_cf_scope` 에 따라 R_j,0 만 또는 세 R). 변이 · origin 런에는 없음 |
| zero · short 모서리의 SV | 반사실 기록이 없으니 SV_UNCHECKED (차단) |
| 끝 origin 런 | 점 수 상한에 안 셈. 밀면서 새로 돈 사다리 점은 셈 |
| 멈춘 변이 단계 | 판정이 그 입력을 받지 않음 (`INPUT_STAGE_STOPPED`) |
| GPU 필수 런에서 반사실 GPU 실패 | 러너가 `--step3-require-gpu` 를 붙이므로 SystemExit 로 런 전체 정지 → 사슬 RUNNER_RC (차단). 재개는 같은 명령 |
| 메모리 (추정 · 실측 아님) | 반사실은 같은 크기 계를 한 번 더 조립하고, 그동안 주 계가 남아 있음. CPU 정점 약 +0.28 kB/dof → 26.8 M dof (옛 DBE vox 0.15 실측) 기준 약 +7.6 GB. GPU 둘째 계 약 3.5 GB. 실측은 첫 kgy 런 peak RSS 로 |

### 6. 이름 맞춤 (C 의 §2-1 · §10-1 · §10-3 몫)
| 코드 이름 | 뜻 |
|---|---|
| `rint-r-plan-v2` = v1 + `max_ladder_points` · `calib_rj_ratio_max` ('none' 허용) · `sv_cf_threshold` · `sv_cf_scope` ('R_j0' · 'all3') | 결과 전 숫자 넷 |
| 사슬 `--s0-plan` (ladder 필수) · `--after-main` (감도 단계 필수) | 두 계획 대조 · Q-F |
| 러너 `CJUNC_SV_CF=1` · payload `--step3-cjunc-sv-cf` · 팔 이름 `_svcf` · 증거 `solve.sv_counterfactual` (+∞ 비 = null + `ratio_limit` 'inf') | SV 반사실 노브 |
| `VALID_ZERO_TOPOLOGY` · `ELECTRODE_SHORT` · `SV_DEPENDENT` · `SV_UNCHECKED` · `GAP_ENVELOPE_ONLY` · `ASSUMED_UNVALIDATED` · `sv_local_dissipation` | 상태 · 표지 |
| `PLAN_NUMBER_UNREGISTERED` · `S0_PLAN_INVALID` · `S0_PLAN_HASH_UNREGISTERED` · `S0_PLAN_HASH_MISMATCH` · `PLAN_CROSS_MISMATCH` · `MAIN_NOT_DONE` · `MAIN_BINDING` · `CALIB_LADDER_EXHAUSTED` | 새 멈춤 이름 |

`LABEL_CJUNC` 제안: 지금 문구 뒤에 *"· 긴 접촉 = 분산판 v0 · 같은 가닥 재방문 = branch 따로 · SV 소산 = 진단 (지배 보증 아님 · 반사실 대조 비 따로)"* (설계 v1 §4-6 문구). 웹앱은 상수를 읽기만 하므로 바꾸면 화면에 그대로 반영됩니다.

### 7. 회귀 (하나씩 · nice 19 · BLAS 스레드 1 · 잠금 안에서)
| 시험 | 결과 (초) |
|---|---|
| rint_r_chain · e2e | 139/139 (81) · 13/13 (200) |
| ca_ext_b6 · runner · z1 · z3 · verdict | 277 (50) · 128 (106) · 95 (42) · 84 (34) · 31 (41) — 전부 통과 |
| carbon_junction · s0_census · target_cert (빠른 판) · conv_cert | 263 · 126 · 193 · 27 — 전부 통과 |
| ptfe_face_alpha `--old-scripts s1/old` | 253/253 (100) |
| step3 `--selftest` · `--selftest-rint` · run_contract selftest | PASS · PASS · 124/124 |
| webapp ca_ext_labels · rint_scope_labels | 54/54 · 31/31 |
| check_method_discipline `--selftest` · 인자 없이 | 128/128 · 오류 0 (경고 17 중 2 가 제 b6 시험의 try-import 꼴 `PAY` · `SVCF`) |

### 8. 끈 경로 비트 대조 (기반 a76 사본 = 커밋과 633/633 파일 같음)
- 매니페스트 (code_sha · exec_env 빼고) 와 step3 값을 경로 단위로 비교하고 차이 0 을 요구했습니다 (`--expect-identical`).
  - b6 B1: 7 경우 (접합 · rtol · face_alpha 켠 경우 포함) 30/30.
  - z3 O: 11/11.
- runner NB: payload 명령줄 · 영수증 바이트 · OUTDIR · 팔 이름 · 매니페스트 같음 (2/2).
- z1 ZB 3/3 · verdict V4 3/3 (판정 JSON 바이트 같음).
- 음성 대조: 47d 에 `--expect-identical` 을 걸면 켠 경우 넷만 정확히 실패합니다 (허용 목록 없이는 A · B 의 1 회차 새 칸이 걸린다는 뜻).

### 9. 병합 메모
- A 파일 `ca_ext_cjunc.py` 에 제 변경이 한 곳 있습니다. `payload_prepare` 가 반사실 노브를 넘기는 부분이고, 끈 경우는 옛 호출과 바이트 같습니다. A 가 같은 함수를 고치면 충돌할 수 있습니다.
- `ca_ext_svcf.RATIO_STATUSES` 는 A 의 지금 상태 낱말 ('computed' · 'no_through_without_sv') 입니다. A 가 이름을 바꾸면 비를 못 읽어 SV_UNCHECKED 가 됩니다 (차단 쪽).
- A 가 S0 계획에 s_min 을 넣으면 두 계획 대조에 한 줄 (R 계획 `s_min_um` ↔ S0) 을 더해야 합니다.
- `run_contract.py` 는 B 도 만질 수 있는 파일입니다.
- A · B 의 2 회차 새 칸이 들어오면 `OLD_DIFF_ALLOW` 에 세대 한 줄을 같은 커밋으로 올려야 합니다.

### 10. 안 한 것 · 한계
- 웹앱 설명 쪽 `webapp/static/explain/rint_overview_20261021.html` 의 holdout 용어와 10-25 날짜 (PRE-design-07). C 가 D · 메인 몫으로 남겼는데, 제 항목 목록 밖이라 손대지 않았습니다.
- 사슬 판정 표지 (SV_UNCHECKED · GAP_ENVELOPE_ONLY · ASSUMED_UNVALIDATED · 결정표 문장) 를 띄울 웹앱 화면은 없습니다.
- 규칙 어김 1 회: 회귀가 끝난 뒤 기반 사본에서 검사기를 잠금 없이 돌렸고, 170 초에 시간 초과로 끊었습니다. 그 결과는 쓰지 않았습니다.
- push · check_all · git fetch · GPU 런 · kgy 접속 없음. 봉인 32 파일 · 원장 · CLAUDE.md · 진행 기록 · 수정 계획은 손대지 않았습니다.

회귀 로그는 `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaD/logs/` 의 `final_*.log` 입니다. 스크래치의 기반 사본은 지웠습니다.