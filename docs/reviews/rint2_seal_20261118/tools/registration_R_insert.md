# 등록 R 봉인본에 넣는 글 — Rint ② 봉인 후보 v2 (11-17 · 문서만 · 결과 0 건 · 실행 0 · σ 열람 0)

- **무엇** = 봉인본 `docs/reviews/rint2_seal_<봉인 날짜>/registration_R_sealed.md` (새 파일 · 1저자 11-17 봉인 후보 Q1 = 넷째 길) 의 바이트를 만드는 조각.  봉인본 = 핀 판 원본 + 아래 조각 R-00 – R-15 (그 밖의 줄 = 원본과 바이트 같음).  원본 자리 (`docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md`) = 핀 판 그대로 + 조각 R-MARK 한 줄.
- **원본** = `git show 64e4d213e:docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` (301,281 B · 747 줄 · sha256 219b63514d8c594d1f96bf7ce610ff9e9bc59dd3482616883475e36fee112bf2 · 11-17 06:56 UTC 측정 = 본 리포 HEAD · 원격 stoic `b3481336c` · stoic-next 끝 `5645b86c8` 의 같은 경로와 바이트 같음 [실측 · 그 시점 값]).  줄 번호 = 그 판.
- **만드는 것** = 기계 (`make_sealed_copy.py` · 이 폴더) — 사람이 붙이지 않는다.  조각마다 `@op <꼴> <원본 줄> <그 줄의 첫 글자들>` 한 줄 (도구가 읽는다 · 자리 = 그 글자로 시작하는 줄이 원본에 하나뿐 · 그 줄 번호 = 적은 번호) + 넣을 글 (`====` 두 줄 사이 · 그대로).  꼴: `last` (그 줄 끝 칸을 바꿈) · `mid+last` (끝 칸 바로 앞에 가운데 글을 이어 쓰고 끝 칸을 바꿈 · `====` 쌍 둘 = 가운데 · 끝) · `after` (그 줄 바로 뒤에 넣음) · `before` (그 줄 바로 앞에 넣음).  옛 글은 지우지 않는다 (줄 그음 · 표지).
- **자리표 — 도구가 채운다**: `<봉인 날짜>` (8 자리 · 예 20261120 · 봉인 때 1저자) · `<봉인본>` (= `docs/reviews/rint2_seal_<봉인 날짜>/registration_R_sealed.md` · 리포 상대) · `<봉인 계획 sha256>` (계획 파일 바이트) · `<계획 숫자 블록>` (핀 사슬 `--stage plan-doc --plan <계획>` 출력 · 사람이 옮기지 않는다) · `<봉인 가지>` (도구에 가지 이름을 줄 때만).  **채우지 않는 자리표**: `<봉인 커밋>` (이 파일을 넣은 커밋 = 자기 sha · 파일 안에 적을 수 없다 · 값 = `git log --diff-filter=A --format=%H -- <봉인본>`) · 실행 때 화면 값 (`<n>` · `<… 항목 번호>` · `<… 채택 번호>` · `<넘김 기록 시각>` · `<원장 가지>`).
- **1저자 결정 표기**: "봉인 후보 Qn" = 봉인 후보 v1 (바) 에 대한 1저자 11-17 결정 (*"권고대로해 · 이런걸로 병목 만들지마"* · 봉인 기록 README 표) · "3 판 Qn" = 시간 다시 어림 3 판 §3-6b · §3-6c 의 1저자 11-17 결정 (stoic 기록 · 봉인 기록 README §사 가 커밋 · 경로를 가리킨다).
- ⚠ 지킬 것 (도구가 센다) — ① 사슬이 세는 계획 숫자 블록 표지 글자를 R-07 밖에 쓰지 않는다 (이 파일 안에도 쓰지 않는다 · 블록 = `<계획 숫자 블록>` 한 줄) ② `| 계획 해시 |` · `| S0 계획 해시 |` 로 시작하는 줄을 더 만들지 않는다 (사슬 `registration_row_hash` = 하나뿐이어야) ③ §2-1 83 줄의 자리 줄 글자 (시험 고정물 `PLAN_DOC_ANCHOR`) 를 다른 줄에 쓰지 않는다 ④ R-MARK = 한 줄 · ①–③ 을 지키고 봉인본 자리 · 봉인 커밋을 가리킨다.
- **봉인 판 (11-17 밤 · 봉인 20261118 · Codex 2/2 §7-3)** 에서 바뀐 것: R-00 끝 두 줄 (봉인 값 · 지위 · 한정 셋) · R-15 의 ⬜ 한 줄 → ✅ 봉인 한 줄 + ⬜ 다음 차례 한 줄 — 그 밖 조각 글 = v2.1 그대로.
- v2.1 (11-17 · 내부 반박 리뷰 · Codex 아님) 에서 바뀐 것: R-13 §10-7 ① 받는 쪽 차례 (세워 둔 자리에서 먼저 `pull --ff-only` 뒤 되살림 · 기계 대조 `RECV_OK`) 뿐 · 그 밖 조각 글 = v2 그대로.
- v1 (`../seal_candidate/registration_R_insert.md`) 에서 바뀐 것 (v2): 대상 = 봉인본 새 파일 (v1 = 원본 자리를 고침) · R-00 · R-MARK 새로 · R-05 끝 칸 · R-07 블록 = 도구가 채움 · R-09 · R-10 = 모든 사슬 명령 `--registration ~/dem-ca1/<봉인본>` · S0 단계 2 줄 (`--r-doc <봉인본>`) 새로 · R-13 = 봉인 후보 Q4 – Q7 · R-12 · R-14 = 3 판 근거를 봉인 기록이 가리킴 · R-15 = 봉인 꼴.

## R-MARK · 원본 자리 머리 표지 한 줄 (원본에만 · 봉인본에는 넣지 않는다)

@op after 1 # 등록 R 초안 — 탄소 접합

- 꼴 = 1 줄 (제목 줄) 바로 뒤에 한 줄 · 원본 자리의 바뀐 곳은 이 줄 하나뿐.

====
> **봉인 표지 (<봉인 날짜>)** — 이 글은 봉인 전 판 그대로다 (Rint 고정 가지 끝 `64e4d213e` 의 바이트 + 이 줄 하나).  R 의 등록 = 봉인본 `<봉인본>` (그 파일을 넣은 커밋 = 봉인 커밋) — 사슬 단계 명령은 `--registration` · S0 단계 2 는 `--r-doc` 로 그 봉인본을 읽는다 · 이 글의 §2-1 해시 칸은 ⬜ 그대로라 사슬 기본 경로로 부르면 멈춘다.
====

## R-00 · 봉인본 머리 절 (봉인본에만)

@op after 1 # 등록 R 초안 — 탄소 접합

- 꼴 = 1 줄 (제목 줄) 바로 뒤에 (빈 줄 · 인용 절).

====

> **★ 봉인본 (<봉인 날짜> · 1저자 11-17 봉인 후보 Q1 · 결과 0 건)** — 이 문서 = **등록 R 의 봉인본**.  원본 = `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` @`64e4d213e` (Rint 고정 가지 `codex/rint-rtr01-receipt-1113` 끝 · 301,281 B · 747 줄) — 원본 자리의 글 = 그 바이트 + 머리 표지 한 줄 (봉인 전 판 · §2-1 해시 칸 ⬜).
> - **바뀐 곳 = 이 절 + 조각 R-01 – R-15 뿐** (자리 = 원본 줄 번호 · 조각 글 = `docs/reviews/rint2_seal_<봉인 날짜>/tools/registration_R_insert.md`) — 그 밖의 줄 = 원본과 바이트 같다 · 이 파일 바이트 = 도구 `docs/reviews/rint2_seal_<봉인 날짜>/tools/make_sealed_copy.py` 가 원본 + 조각 + 계획 파일로 다시 만든다 (사람이 블록 · 해시를 옮겨 적지 않는다 · 봉인 기록 `docs/reviews/rint2_seal_<봉인 날짜>/README.md`).
> - **읽는 법** — 사슬 (`scripts/rint_r_chain.py`) 의 모든 단계 명령 = `--registration ~/dem-ca1/<봉인본>` · S0 단계 2 (`scripts/ca_s0_census.py --stage 2`) = `--r-doc <봉인본>` (리포 상대) — 사슬 · S0 의 기본 경로 = 원본 자리 (봉인 전 판) 라 그대로 부르면 해시 줄 ⬜ 에서 멈춘다 (§10-1b).
> - `<봉인 커밋>` (실행 줄의 자리표) = 이 파일을 넣은 커밋 = `git log --diff-filter=A --format=%H -- <봉인본>` — 이 파일 안에는 적을 수 없다 (자기 sha).
> - 줄 번호 — 이 파일 안의 "N 줄" 표기 (등록 R 자기 줄) = **원본 (핀 판) 줄 번호** 다 (이 절 · 조각이 넣은 줄만큼 이 파일에서는 뒤로 밀린다 · 찾을 때는 글로) · 사슬 · 시험 코드 줄 = `64e4d213e` 판.
> - 1저자 결정 표기 — "봉인 후보 Qn" = 봉인 후보 v1 에 대한 1저자 11-17 결정 (*"권고대로해 · 이런걸로 병목 만들지마"* · 표 = 봉인 기록 README) · "3 판 Qn" = 시간 다시 어림 3 판 §3-6b · §3-6c 의 1저자 11-17 결정 (stoic 기록 · 이 가지의 같은 경로 `docs/reviews/rint2_time_reestimate_20261111/README.md` 는 2 판까지 · 3 판의 커밋 · 경로 = 봉인 기록 README §사).
> - **봉인 값 · 지위 (<봉인 날짜> · 결과 0 건)** — 결과 전 등록 넷 = 1저자 11-17 (Codex 2/2 판정 뒤 · σ 열람 0): `max_ladder_points` = 16 (3 판 시간 표의 12 점 가정 → 상한 16 · 시간 다시 셈 = 봉인 기록 README) · `calib_rj_ratio_max` = `"none"` (상한을 두지 않음 · §3-2b ④) · `sv_cf_threshold` = 1.5745499360744093 (= exp(G0/2) · G0 = ln(4.68/1.8877) = 0.9079389531370043) · `sv_cf_scope` = `"all3"` (1저자 10-23) — 값의 정본 = 계획 파일 (§2-1 계획 해시 줄 · 계획 숫자 블록).  Codex 2/2 (11-17 · 리뷰 핀 f40d005ac) = **조건부 GO — 봉인 준비 범위만** · 실제 실행 · 정량 판정 · 운영 GO · 공유 원장 종결은 승인되지 않았다 (현장 자격 · 실행 승인 = 1저자 · 따로).
> - **한정 (Codex 2/2 §7-3 · 옮길 때 빼지 않는다)** — ① maxiter 5,000,000 · 시간 상한 168 h · 시도 8 · 넘침 점 112 h 규칙 = 정책 값 · **완료 보장 아님** (NOT_COMPUTED 가 없다는 보증이 아니다 · 넘침 규칙은 시간 안에 될 점도 보수적으로 멈출 수 있다) ② RCA-11 = **이 R 의 입력 · 선택 고정 (§2-1 u 행) 만 한정 종결** · 원장의 지적 전체 = 부분 (열림 그대로) ③ `env_unit` (python 부 판 · numpy · scipy 판 글자) = 사슬이 대조하는 같음 단위일 뿐 **전체 실행 환경이 아니다** — python 패치 판 · cupy · GPU · 드라이버 · BLAS 계산 경로 · CPU · numpy SIMD 는 사슬이 단계마다 기록만 한다 (대조 · 멈춤 없음 · 사슬 env_record) · 기준 기록 = 봉인 직전 두 기계 현장 확인 출력 (kgy 명령 문서 §3-1b (2)) · 확인 담당 = 1저자 (현장 확인 · 두 기계 조립 같음 11-12 Q10 · R 동안 venv · 드라이버 갱신 멈춤).
====

## R-01 · §2-1 표 u 행 숫자 칸

@op last 72 | u (위치 불확도) |

====
~~⬜~~ → **0.07381254285530132 µm** (봉인 · S0 단계 1 SBE 11-16 · 핀 `64e4d213e` · S0 계획 `values_um.u` = 점 간격 중앙값 0.14762508571060265 µm ÷ 2 · n 1,544,424 · `docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json` · 채택 확인 `docs/data/rint2_s0_sbe_20261116/ADOPTION_CHECK.md`)
====

## R-02 · §2-1 표 tol_ff 행 숫자 칸

@op last 73 | tol_ff |

====
~~⬜~~ → **0.07381254285530132 µm** (= min(u, r_f 0.075) = u · S0 계획 `values_um.tol_ff` · R 계획 `tol_ff_um` 과 같은 float · 사슬 `plans_cross_problems` · S0 단계 2 관문이 대조)
====

## R-03 · §2-1 표 tol_P · tol_sj 행 숫자 칸

@op last 76 | tol_P · tol_sj |

====
~~⬜~~ → **0.07381254285530132 µm** (= tol_ff · S0 계획 `values_um.tol_P` · `tol_sj`)
====

## R-04 · §2-1 표 긴 접촉 행 숫자 칸

@op last 77 | 긴 접촉 |

- 옛 칸 글 "긴 접촉 수 · L_c 분포 · s 분포 · s_min = ⬜ (§2-1b)" 은 아래 글 첫머리에 그대로 둔다.

====
긴 접촉 수 · L_c 분포 · s 분포 · s_min = ~~⬜~~ (§2-1b) → (봉인 · S0 단계 1 11-16 · 핀 `64e4d213e` · 보고 `s0_stage1_kit_SBE_vgcf100.json` 의 `junction_census` 칸 그대로) instance 117,583 · 긴 접촉 30,270 (전부 distinct · 자기 0) · 같은 셀 비연속 재방문 874 쌍 · **s_min = 0 µm** (§2-1b 11-09) · L_c · s 분포 = 그 보고 칸 (`Lc_um` · `revisit.s_um` · 옮겨 적지 않는다) · 11-08 보고 (§2-1b 104 줄) 와 같은 수
====

## R-05 · §2-1 표 계획 해시 행

@op mid+last 80 | 계획 해시 |

- 가운데 칸 끝에 이어 쓸 글 (첫 `====` 쌍) · 끝 칸 (둘째 쌍 · 64 자 hex 하나 · 백틱 한 쌍 · 사슬은 끝 칸에서 백틱 · 빈칸만 걷는다).

====
 · **(봉인 · <봉인 날짜> · 1저자 · 결과 0 건) 계획 = `docs/data/rint2_r_plan_<봉인 날짜>/ca1_plan.json`** — 코드 = `rint-r-plan-v3` · 칸 12 = 위 v2 칸 11 + `exec_policy` (값 칸 넷 `max_hours` · `max_attempts` · `allowed_machines` · `env_unit` + 규칙 칸 넷 · `rint_r_chain.PLAN_SCHEMA` 301 줄 · `EXEC_POLICY_RULES` 311 줄 · v2 계획 = `PLAN_INVALID` · 위 "v2 · 칸 11" 표기는 10-27 묶음 C1a 전 글 · 1저자 11-17 봉인 후보 Q3) · 꼴 = `json.dump(indent=1, sort_keys=True)` · 끝 줄바꿈 없음 · 숫자 칸 ~~⬜~~ → 그 파일 바이트의 sha256 · 숫자 블록 = 아래 자리 줄 바로 다음
====

====
`<봉인 계획 sha256>`
====

## R-06 · §2-1 표 S0 계획 해시 행

@op mid+last 81 | S0 계획 해시 |

====
 · **(봉인 · <봉인 날짜>) S0 계획 = `docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json`** (S0 단계 1 SBE · 11-16 · 핀 `64e4d213e` · 1,485 B · 정준 바이트 = `ca_s0_census.plan_bytes_of` 와 같음 · 같은 폴더 `cjunc_plan.sha256` 선언과 같음 · 보고 `plan.sha256` 과 같음 · 채택 확인 = 그 자료 폴더 `ADOPTION_CHECK.md` · E1–E4 · T1–T3 기대대로) · 숫자 칸 ~~⬜~~ → 아래
====

====
`6346d9ed5fda248b89d1e28dbcb35c90d67264f060be345673c7da63f9924520`
====

## R-07 · §2-1 계획 숫자 블록

@op after 83 - **(10-28 · 묶음 C1a · REPORT_C §11 ②

- 꼴 = 자리 줄 뒤에 (빈 줄 · 블록 · 빈 줄) · 블록 = 도구가 핀 사슬로 `--stage plan-doc --plan <봉인 계획>` 을 돌린 출력 그대로 (같은 계획으로 사슬 안 함수 `plan_doc_block` 도 불러 같은지 본다 · 대조 = `--stage plan-doc --plan <계획> --check-doc --registration <봉인본>` rc 0 `PLAN_DOC_SAME`).

====

<계획 숫자 블록>

====

## R-08 · §10 머리 기계 줄

@op after 334 - 기계 = kgy (RTX 3090 24 GB

====
  - (봉인 · <봉인 날짜> · 3 판 Q7 · Q9 · 1저자 11-17 봉인 후보 Q6 · 결과 0 건) 기계 = **kgy · gabia** (두 대 동시 · 원장 이어달리기 (가-2) · §10-7) · 사다리 P0 = kgy · P1 = gabia · 단위 첫 배정 kgy 7 · gabia 5 · 합치기 · 판정 = kgy (배정 = 봉인 밖) · v100 = 1저자가 요청할 때만 (허용 목록 안 · §10-4 문장 3) — 위 "기계 = kgy" 는 10-20 글 (남은 계획 §9 어긋남 8) · 실행 줄 = §10-1b
====

## R-09 · §10-1 실제 명령 블록 머리 (bash 블록 안 · 주석 줄)

@op after 391 # (0) 작업 트리 고정 (핀 = 구현

- 꼴 = 그 줄 뒤에 주석 줄 넷 (블록 안 · 이 블록 = 인자 계약 꼴 · 원본 자리의 같은 블록 = 시험 K01 이 읽는 곳 · 이 봉인본의 블록은 K01 이 읽지 않는다).

====
# ★ (봉인 · <봉인 날짜>) 이 블록 = 인자 계약 꼴 (원본 자리의 같은 블록을 리포 시험 K01 이 사슬 argparse 와 대조한다) · R 의 실제 실행 줄 = §10-1b (sh 블록)
#   — 실제 줄의 모든 사슬 명령 = --registration ~/dem-ca1/<봉인본> · S0 단계 2 = --r-doc <봉인본> (기본 경로 = 원본 자리 = 봉인 전 판 → 멈춤)
#   — 저장본 --cjunc-store · 12 단위 --unit · 넘침 점 --point · 합치기 --merge · 원장 이어달리기 (가-2) · 시간 상한 168 · 기계 이름표 · 아래 (4) 의 한 기계 예측 줄 (--attempt <predict 항목 번호>) 은 이 등록의 경로가 아니다 (원장 하나 = 경로 하나 · §10-5 가 ⑮)
#   작업 트리 = 봉인 커밋 (Rint 고정 가지 끝 64e4d213e 위 문서 커밋 · stoic 아님 · 3 판 Q5) · 깨끗 = --untracked-files=normal 기준
====

## R-10 · §10-1b 새 절 (12 단위 경로 실행 줄)

@op after 458 - R 런 계획 파일 (`~/sdcp/ca1_plan.json`)

- 꼴 = 그 줄 뒤에 (빈 줄 · 절).  명령 줄 = kgy 명령 문서 §3-1b 와 같은 인자 (두 문서 대조 = 봉인 기록 `evidence/` 의 argparse 대조 · 시험 K01 은 sh 블록을 읽지 않는다 — 1저자 11-17 봉인 후보 Q2).

====

### 10-1b. 12 단위 경로 — R 의 실제 실행 줄 (봉인 · <봉인 날짜> · 1저자 11-10 Q3 · Q7 · 3 판 Q2 · Q3 · Q6 · Q7 · Q9 – Q11 · 봉인 후보 Q1 – Q7 · 결과 0 건)

- **경로** = S0 단계 2 (kgy · 한 번) → 사다리 둘 (P0 · P1 · 법칙마다 시도 하나 · 끝에 no-op) → 예측 12 단위 (`unit:<법칙>_c<c>_<R 역할>` · 시도 하나 = 단위 하나 · Q9 설계 §3-1) → 첫 합치기 (`--merge` · 넘침이 없으면 이것이 예측) → (넘침이면 rc 4 · `expansion.json` → 넘침 점 `point:<이름>` · 끝 합치기 `--expand`) → 원장 판정 → 다시 판정.  한 원장 = 이 경로 하나 (`predict` 대상 = 쓰지 않는다 · §10-5 가 ⑮).
- **등록 문서 = 이 봉인본** — 사슬의 **모든** 단계 명령에 `--registration ~/dem-ca1/<봉인본>` (1저자 11-17 봉인 후보 Q1 · 사슬 기본값 = 원본 자리 = 봉인 전 판 → 해시 줄 ⬜ → `PLAN_HASH_UNREGISTERED` 멈춤) · 이 문서를 실제로 읽는 단계 = 사다리 · 예측 (단위 · 점 · 합치기) · 판정 · `plan-doc --check-doc` [코드 · 사슬 6656 · 6880 · 7347 · 7715 · 8606 줄] · 원장 `--init` · `--add` · recover 는 읽지 않고 · 다시 판정은 판정 JSON 에 적힌 등록 경로를 다시 읽는다 [코드 · 8260 줄] — 그래도 같은 꼴로 붙인다 (한 규칙) · S0 단계 2 = `--r-doc <봉인본>` (리포 상대 · ASCII · `ca_s0_census.verify_plan_commit` 이 봉인 커밋의 이 파일에서 두 해시 줄을 읽는다).
- **기계** = kgy · gabia 동시 (원장 이어달리기 (가-2) · §10-7) · 사다리 P0 = kgy · P1 = gabia · 단위 첫 배정 kgy 7 · gabia 5 · 합치기 · 판정 · 다시 판정 = kgy · 합친 예측 폴더 = `~/sdcp/ca1_predict` (첫 합치기) · `~/sdcp/ca1_predict_x` (넘침 뒤 끝 합치기) (1저자 11-17 봉인 후보 Q6 · 배정 · 폴더 이름 = 봉인 밖) · 넘침 점 = kgy 먼저 + 안전 규칙 (§10-8 ⑩) · 기계 이름표 = 계획 `exec_policy.allowed_machines` 안.
- **숫자** = 계획 그대로 — `--max-hours 168` (= `exec_policy.max_hours` · 단위 · 넘침 점 · 재실행 · 합치기 하나하나의 마감 · Q9 설계 §3-2 2) · maxiter 5,000,000 (`p2_extra` · 사슬이 러너 env `P2_EXTRA` 로 편다) · 최대 시도 수 8 (같은 대상 원장 항목 수 · 풀기 전 거부 · 재실행 포함 · §10-5 나 ⑦).
- **저장본** = 사다리 · 단위 · 넘침 점 런에만 `--cjunc-store ~/ca1_cjstore` (기계마다 새 빈 폴더 · 1저자 11-17 봉인 후보 Q4 · §10-6) · 합치기 · 판정 · 다시 판정 · 봉인 원천에는 주지 않는다 (사슬이 받지 않는다 · §10-6 ②).
- **아래 줄의 꼴** = 원장 시도 꼴 (`--ledger` · `--attempt`) · 단위 · 점 이름 = 낱말 그대로 (사슬 `UNIT_RE` · 2991 줄) · 자리표 `<…>` 만 사람이 채운다 · `~` = 실행 셸이 펼친다 (사슬 · 러너는 절대 경로를 받는다 · 저장본 폴더 = 절대 · 정규화 · 글자 `[A-Za-z0-9._/-]`).

```sh
# (0) 두 기계 — 실행 트리 = 봉인 커밋 · 깨끗 · venv · 계획 사본 · 저장본 폴더 (자세한 줄 = kgy 명령 문서 §3-1b (1) · (2))
umask 022
git -C ~/dem-ca1 rev-parse HEAD                                   # = <봉인 커밋> (= git -C ~/dem-ca1 log --diff-filter=A --format=%H -- <봉인본>)
git -C ~/dem-ca1 status --porcelain --untracked-files=normal      # 빈 줄
. ~/dem-venv/bin/activate && unset SIGMA_VGCF_OVERRIDE         # 두 기계 같은 자리 · 같은 판 (env_unit · 확인 줄 = kgy 명령 문서 §3-1b (2))
cp ~/dem-ca1/docs/data/rint2_r_plan_<봉인 날짜>/ca1_plan.json ~/sdcp/ca1_plan.json && sha256sum ~/sdcp/ca1_plan.json   # = §2-1 계획 해시 줄 끝 칸
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage plan-doc --plan ~/sdcp/ca1_plan.json --check-doc --registration ~/dem-ca1/<봉인본>   # PLAN_DOC_SAME (rc 0)

# (1) S0 단계 2 — kgy · 한 번 · R 전 (인자 커밋 = 봉인 커밋 · 결과 전 등록 넷이 든 봉인 계획이어야 관문이 연다 · 손 확인 = kgy 명령 문서 §3-1b (2b))
python3 ~/dem-ca1/scripts/ca_s0_census.py --stage 2 --threshold-commit <봉인 커밋> \
    --plan-path docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json \
    --r-plan-path docs/data/rint2_r_plan_<봉인 날짜>/ca1_plan.json --r-doc <봉인본> \
    --kit ~/sdcp/kit_DBE_sdcp1um_vgcf100 --kit ~/sdcp/kit_DBE --out ~/sdcp/ca1_s0_dbe

# (2) 원장 시작 — kgy · 한 번 (머리 = 위 계획 sha256)
mkdir -p ~/sdcp/ca1_ledger && git -C ~/sdcp/ca1_ledger init -q
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --init --plan ~/sdcp/ca1_plan.json --registration ~/dem-ca1/<봉인본>

# (3) 사다리 — 법칙마다 항목 → 시도 (P0 = kgy · P1 = gabia) · 시작 확인 뒤 원장을 넘긴다 (§10-7)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target ladder:P0 --machine kgy \
    --plan ~/sdcp/ca1_plan.json --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --registration ~/dem-ca1/<봉인본>
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --plan ~/sdcp/ca1_plan.json --registration ~/dem-ca1/<봉인본> \
    --s0-plan ~/dem-ca1/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json \
    --s0-stage2-report ~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json \
    --s0-stage1-report ~/sdcp/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json \
    --max-hours 168 --machine kgy --ledger ~/sdcp/ca1_ledger --attempt <ladder:P0 항목 번호> \
    --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_ladder_P0
#   P1 = 같은 두 줄 · gabia · ladder:P1 · --law P1 · --machine gabia · --out ~/sdcp/ca1_ladder_P1

# (4) 단위 — 12 개 (이름 = Q9 설계 §7 · 남은 계획 §4-2 표 · 첫 배정 = 명령 문서 §3-1b (6)) · 단위마다 항목 → 시도 · 두 사다리 채택 시도 폴더가 그 기계에 있어야 (바이트 그대로 옮김)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target unit:P0_c0_R_j0 --machine kgy \
    --plan ~/sdcp/ca1_plan.json --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --registration ~/dem-ca1/<봉인본>
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/<봉인본> --ledger ~/sdcp/ca1_ledger --attempt <unit:P0_c0_R_j0 항목 번호> --unit P0_c0_R_j0 \
    --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_units

# (5) 첫 합치기 — kgy (러너 · 두 킷 · 원장 · 모든 단위 시도 폴더 · gabia 바탕 = 바이트 그대로 옮긴 사본) · rc 0 = 예측 · rc 4 = 넘침 (expansion.json)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/<봉인본> --ledger ~/sdcp/ca1_ledger --merge ~/sdcp/ca1_units ~/sdcp/ca1_units_from_gabia --out ~/sdcp/ca1_predict

# (6) 넘침 점 (rc 4 일 때만 · expansion.json 의 points 마다 · 그 기계 = 안전 규칙 §10-8 ⑩) → 끝 합치기
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target point:P0_c0_R_j0 --machine kgy \
    --plan ~/sdcp/ca1_plan.json --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --registration ~/dem-ca1/<봉인본>
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/<봉인본> --ledger ~/sdcp/ca1_ledger --attempt <point:P0_c0_R_j0 항목 번호> --point P0_c0_R_j0 \
    --expand ~/sdcp/ca1_predict/expansion.json --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_points
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/<봉인본> --ledger ~/sdcp/ca1_ledger \
    --merge ~/sdcp/ca1_units ~/sdcp/ca1_units_from_gabia ~/sdcp/ca1_points ~/sdcp/ca1_points_from_gabia \
    --expand ~/sdcp/ca1_predict/expansion.json --out ~/sdcp/ca1_predict_x

# (7) 주 판정 · 다시 판정 — kgy · --runs = 사다리 채택 시도 둘 + 합친 예측 폴더 (넘침 없음 = ca1_predict · 넘침 = ca1_predict_x)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --runs ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> \
    ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> ~/sdcp/ca1_predict --root ~/sdcp --registration ~/dem-ca1/<봉인본> \
    --ledger ~/sdcp/ca1_ledger --out ~/sdcp/ca1_verdict_main
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --reverify ~/sdcp/ca1_verdict_main --root ~/sdcp --registration ~/dem-ca1/<봉인본>

# (8) 원장이 없는 동안 끝난 시도 (rc 3 · 원장 잠금 파일을 못 연다) — 원장이 그 기계로 돌아온 뒤 그 시도 폴더에서 (§10-7 ③)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage recover --out ~/sdcp/ca1_units/attempt_<n> --ledger ~/sdcp/ca1_ledger --registration ~/dem-ca1/<봉인본>
```

- 판정의 값 열람 (`--show-results`) = 주 판정 런이 다 끝난 뒤 한 번 (§4-1 · §10-4) — 위 (7) 의 첫 줄에 붙인다 · 감도 단계 (FIBRE · UNREG · GRID · SVORDER) = 이 절 밖 (경로 = R 시작 전 따로 · 1저자 11-17 봉인 후보 Q8 · ⬜).
- 이 절의 줄 = kgy 명령 문서 §3-1b 의 줄과 같은 인자 (그 문서가 운영 순서 · 원장 넘김 · 기록 · 규칙을 싣는다).

====

## R-11 · §10-4 문장 3 뒤 (허용 기계 값)

@op after 590 - (10-22 · PF2 C · D) 문장 3 의 자리 = 사슬 `--machine`

====
- (봉인 · <봉인 날짜>) 문장 3 의 값 = 계획 `exec_policy.allowed_machines` = `["kgy","gabia","v100"]` (589 줄 · 1저자 10-23 *"kgy, gabia에서 돌릴거야"* · Q11 · v100 = 요청할 때만 · 쓰지 않아도 됨 · 쓸 때 같은 판 venv = `exec_policy.env_unit` · Q9 설계 §3-3) · 위 괄호 "러너 경로도 같은 키라 기계마다 경로가 다르면 멈춘다" = 10-22 글 (코드 키 = 저장소 상대 경로 · 110 줄 · 12 단위 끝-끝 시험 D6c · 남은 계획 §9 어긋남 6).
====

## R-12 · §10-4 시간 상한 줄

@op after 601 - ⚠ 주 판정을 본 뒤 감도를 빼거나 바꾸지 않는다

====
- (봉인 · <봉인 날짜> · 3 판 Q3) 위 줄의 "시간 상한 `--max-hours` 숫자 = ⬜" → **168 h** (계획 `exec_policy.max_hours` · 사슬 `exec_check_or_stop` 이 `--max-hours` 와 정확히 대조 · 다르면 `NOT_REGISTERED`) · 단계 · 시도 하나하나의 마감 (12 단위 경로 = 단위 · 넘침 점 · 재실행 · 합치기 하나하나) · 근거 = 시간 다시 어림 3 판 §3-4 (stoic 기록 · 커밋 · 경로 = 봉인 기록 `docs/reviews/rint2_seal_<봉인 날짜>/README.md` §사 · 가장 긴 한 런 = 넘침 점 8 팔 gabia 첫 점 60.4 h [추정] 의 2.78 배) · 168 h 를 넘는 8 팔 점은 결과 뒤 TIME_LIMIT 라 같은 기계 재실행만 → 넘침 점 배정 안전 규칙 (§10-8 ⑩ · 3 판 Q11).
====

## R-13 · §10-6 · §10-7 · §10-8 새 절 (저장본 · 원장 공유 · 실행 정책 문장)

@op after 660     - 고치지 않음 · 한정 = 증거 README §5

- 꼴 = §10-5 의 끝 줄 뒤에 (빈 줄 · 세 절).

====

### 10-6. 탄소 접합 원장 저장본 (봉인 · <봉인 날짜> · 1저자 11-12 Q2 · 3 판 Q6 · 봉인 후보 Q4 · 결과 0 건 · 시간 다시 어림 2 판 E-2 의 4 ①–④ 의 처분)

- ① **새 산출물 · 무엇에 묶나** — 저장본 = 폴더 하나 안의 파일 `cjreg_<열쇠>.npz` (`scripts/cjunc_store.py` · 0444 · 단일 작성자) · 열쇠 (`Store.key_parts` → sha256) = 꼴 판 `cjstore-v1` · 모델 판 (`carbon_junction.CJUNC_MODEL_VERSION`) · 스키마 (`CJUNC_SCHEMA`) · 코드 파일 넷 (`carbon_junction.py` · `step3_sigma.py` · `fibre_segment_raster.py` · `cjunc_store.py` 의 이름 + sha256) · 환경 (python 부 판 · numpy · scipy 판 글자 + venv 접두 · numpy · scipy 패키지 실경로 지문) · 기계 (`/etc/machine-id` 지문) · sid 격자 지문 (origin 을 바꾸면 바뀐다) · lo · vox · 입력 넷 (점 · 상 · fid · kind 정준 값 지문) · 문턱 칸 → **기계 · 침대 · origin 마다 파일 하나** (R_j · 법칙 · c · SV 노브는 열쇠 밖 — 계획 (R_j · 법칙 · c · SV) 은 팔마다 다시 만든다).  팔 JSON · 매니페스트 · 영수증 · 이름 = 저장본 끔과 바이트 같다 → 저장본 켬의 기록 = 단계 요약 칸 `cjunc_store` · `cjunc_store_arms` (사슬 6647 · 6716 줄 = 사다리 · 6853 · 6933 줄 = 예측) 과 팔 곁 파일 `cjstore_audit_<팔>.json` 뿐 (판정 · 같음 대조 · 재개 바이트 대조에 쓰지 않는다).
- ② **봉인 원천 (조립만) 은 저장본을 읽지 않는다** — 사슬이 봉인 원천 런 env 에서 뺀다 (`rint_r_chain.py` 5901 줄) · 러너가 `CJUNC_STORE` + `CJUNC_GRAPH_ONLY=1` 을 거부 (`sdcp_gain_vox015_8arm.sh` 593–594 줄) · payload 가 거부 · 합치기 · 판정 · 다시 판정 = `--cjunc-store` 를 받지 않는다 (사슬 8687–8689 줄).  **한정**: 저장본 밖 독립 대조 = 봉인 원천 재조립이고 그것은 **SV 모서리 팔 (끝 그래프 지문) 만** 덮는다 — 사다리 (SBE 전부) · DBE origin 팔 · 넘침 점 팔은 독립 대조 없이 열쇠 · 폴더 · 파일 권한 · 같은 코드 · 환경의 결정성에 기댄다 · 같은 열쇠 아래 자기 일관 위조 (내용 · 머리 · 지문을 모두 다시 센 파일) 는 저장본 혼자 가리지 못한다 (`scripts/cjunc_store.py` 머리 글 35–37 줄 그대로).
- ③ **자리 · 권한** — 기계마다 **새 빈 폴더 `~/ca1_cjstore`** (1저자 11-17 봉인 후보 Q4 · ⑥ 의 `~/p6_cjstore` · S0 저장본 시험 폴더 (`cjstore_s0probe_*`) 를 쓰지 않는다 — ⑥ · S0 산출은 R 에 쓰지 않는다 · 개발 탐침 원장 §2) · 절대 · 정규화 경로 · 글자 `[A-Za-z0-9._/-]` · 마지막 성분 심볼릭 링크 아님 · 있는 폴더 · 소유자 = 실행 사용자 · 그룹 · 남 쓰기 없음 (사슬 `cjunc_store_dir_problem` 5626 줄 · 러너 583–612 줄 · 저장본 `Store` 같은 규칙) → 만드는 줄 = umask 022 셸에서 `mkdir` · `chmod go-w` · `ls -ld` 확인 · 사슬 함수로 확인 (kgy 명령 문서 §3-1b (2)) · 실행 트리 · 원장 저장소 밖.  디스크: 쓰기 전 여유 < 2 × 파일 크기 + 1 GiB 면 쓰지 않는다 (`built_write_skipped` · 팔 결과 무관 · `cjunc_store.py` 664–671 줄).
- ③′ (E-2 의 4 ③ — ⑥ 다시 재기 원장 줄) = 개발 탐침 원장 §2 핀 칸 개정 (풀이 코드 목록 기준 · 1저자 11-12 Q5) · §3 시도 3 · 4 줄 (11-16 · 핀 `64e4d213e` · 저장본 짓기 · 읽기) — 이 봉인 커밋에 함께 (`docs/reviews/rint2_dev_probe_ledger_20261026.md` · 묶음 `docs/data/rint2_probe6_a3_20261116/` · `docs/data/rint2_probe6_a4_20261116/`).
- ④ **읽은 원장을 입력에 묶는 지문 = 구현됨** — 열쇠의 `inputs` (입력 넷 정준 값 지문 · `cjunc_store.py` 525 줄 `_inputs_fp`) + sid 격자 · lo · vox · 문턱 → 2 판의 "PTFE · SDCP 점을 묶는 지문이 없다 → 새로 정해야" 는 이 구현으로 닫는다.
- ⑤ **실패 처분** — 못 읽음 (CRC 로 확인한 멤버를 손에 넣기 전 · 끊긴 복사 · 디스크) = 다시 짓기 + ⚠ (`unreadable_rebuilt` · 팔 결과 = 새로 지은 원장 · 시간만 는다 · R 동안 그 파일을 지우지 않는다 = 기록 · R 뒤 정리) · **어긋남** (머리 · 열쇠 · 뼈대 · 엄격 지문 · 원장 지문 · sid · 링크 · 소유자 · 모드 · 머리 중복 칸) = **멈춤** (payload `S2_CJUNC_STORE|INCONSISTENT|` · rc ≠ 0 → 사슬 원인 = 러너 rc 길 · 자동 재실행 없음 · 여러 팔 런의 중간이면 결과 뒤 → 그 대상의 결과 = 멈춤 · 사람이 본다) · 기계 id 못 읽음 · 런 도중 열쇠 코드 파일 stat 바뀜 (`git checkout` · `touch` 꼴 포함) = 꺼짐 (그 런은 매번 짓기 · 틀린 결과 아님 · `cjunc_store.py` 760–778 줄) → **R 동안 실행 트리 · 저장본 폴더에 손대지 않는다** (§10-8).

### 10-7. 원장 공유 — (가-2) 원장 이어달리기 · 두 대 동시 (봉인 · <봉인 날짜> · 1저자 11-10 Q3 · 3 판 Q9 · 봉인 후보 Q5 · Q6 · 결과 0 건)

- ① **한 번에 한 기계만 원장을 쓴다** — 원장 = git 저장소 하나 (`~/sdcp/ca1_ledger` · 한 줄 역사 · 덧붙이기만 · 실행 트리와 다른 체크아웃) · 쓰는 사본은 한 기계에만 · 넘김 = 가진 기계에서 **사슬과 같은 잠금 파일 (`~/sdcp/ca1_ledger/.git/rint_r_ledger.lock` · 사슬 `LEDGER_LOCK_FILE` 3060 줄 · `_ledger_lock_path` 3164 줄) 에 `flock`** 을 잡고 `git bundle create <묶음> --all` → 원장을 세워 둠 (이름 바꿈 `~/sdcp/ca1_ledger.parked` · 사슬이 쓰지 못하게) (1저자 11-17 봉인 후보 Q5) → 묶음을 받는 기계로 (수단 = 1저자 · 리포에 주소 · 포트 · 계정 · 홈 경로를 적지 않는다) → 받는 기계: 세워 둔 사본이 있으면 **그 자리 (`ca1_ledger.parked`) 에서 먼저** `git pull --ff-only <묶음> <가지>` 를 받고 받은 뒤에만 되살린다 (이름 바꿈 · 그동안 그 기계 사슬은 원장 자리를 못 연다 = 받는 창 없음 · v2.1) · 없으면 `git clone -b <가지> <묶음> ~/sdcp/ca1_ledger` → 원장 끝 커밋이 넘김 기록과 같은지 기계로 확인 (`RECV_OK` · 아니면 멈춤) (원장 공유 선택지 메모 §2 (가) 꼴 · 12 단위 끝-끝 시험 `relay`).  **`flock` 이 없는 기계** = 그 기계의 사슬이 시작 확인 (아래 ②) 뒤 도는 중일 때만 넘긴다 (봉인 후보 Q5 · 11-17 현장 = 두 기계 다 `flock` 있음 → 이 문장 = 한정).  명령 = kgy 명령 문서 §3-1b (5) · 넘김마다 그 문서의 넘김 기록 블록에 한 줄.
- ② **넘기는 때** = 그 기계에서 도는 사슬이 원장을 쓰지 않는 때 — 시작 기록이 커밋되고 (원장 끝 줄 `kind start` · 그 번호) 첫 러너 그룹이 뜬 뒤 (`<시도 폴더>/groups/*.launch.json`) · 사슬은 그 뒤 끝날 때까지 원장을 건드리지 않는다 (12 단위 끝-끝 시험 D1b · D3h · 원장 공유 선택지 메모 §1 끝).  단위 · 넘침 점 · 사다리의 시도를 시작할 때마다 원장이 그 기계에 있어야 한다.
- ③ **원장이 없는 동안 끝난 사슬 = rc 3 (정상 흐름)** — 화면 끝 줄 `멈춤 [ATTEMPT_LEDGER_MISMATCH] … 원장 잠금 파일을 못 연다 (…)` · 그 시각 그 기계에 원장 없음 (세워 둠) · 시도 폴더에 단계 요약 (`ladder_summary.json` · `unit_summary.json` · `point_summary.json`) 이 있음 → 실패가 아니다 · 결과 줄 = 원장이 그 기계로 돌아온 뒤 `--stage recover --out <그 시도 폴더> --ledger ~/sdcp/ca1_ledger` (그 시도가 돈 바탕 · 같은 부팅 · §10-5 아 ④ · 다른 부팅이면 운영자 확인 표지) · 위 세 조건 중 하나라도 아니면 = 진짜 멈춤 (요약의 멈춤 이름 · 원장 공유 선택지 메모 §2 (가-2) 열).
- ④ **사슬이 막는 것 · 운영 규칙으로만 지키는 것** — 사슬이 막는다: 받은 원장이 덧붙이기만이 아님 · 병합으로 숨긴 판 (`ledger_history_problem`) · 옮긴 시도 폴더 바이트 ≠ 결과 줄 · 폴더 빠짐 · 한 항목 폴더 둘 · 두 사본에 각각 쓴 뒤 섞음 · 결과 줄 없는 시도를 입력으로 (`ATTEMPT_LEDGER_MISMATCH` "recover 먼저") · 같은 대상 다음 항목 (`ATTEMPT_ORDER_MISMATCH`) · 옮긴 폴더에서 recover (rc 3).  운영 규칙: 한 번에 한 기계 (보낸 쪽 세워 두기 · 사슬은 자기 앞 사본이 가장 새 것인지 모른다) · 넘김 수단 · 넘김 기록 · rc 3 를 위 ③ 으로 가르기 · recover 를 그 기계 · 그 바탕에서 (원장 공유 선택지 메모 §2 (가) 표 그대로 · 규칙 · 기계적 보장 아님).
- ⑤ **배정 · 폴더 옮김** (1저자 11-17 봉인 후보 Q6 · 배정 · 폴더 이름 = 봉인 밖) — 사다리 P0 = kgy · P1 = gabia · 단위 첫 배정 kgy 7 · gabia 5 (명령 문서 §3-1b (6) 표) · 합치는 기계 = kgy.  사다리 채택 시도 폴더 = 단위를 도는 다른 기계로 바이트 그대로 (같은 상대 자리 `~/sdcp/ca1_ladder_<법칙>/attempt_<n>`) · 합치기 · 판정 전 = 다른 기계의 바탕 폴더 통째 (모든 `attempt_<n>` · 거부 기록 포함 · 단위 = `~/sdcp/ca1_units_from_<기계>` · 넘침 점 = `~/sdcp/ca1_points_from_<기계>` · 사다리 = 같은 이름 바탕) → 합치기 · 판정이 폴더 요약 sha256 = 원장 결과 줄을 대조 · 합친 예측 폴더 = `~/sdcp/ca1_predict` (첫 합치기) · `~/sdcp/ca1_predict_x` (넘침 뒤 끝 합치기) · 사본 보관 = 판정 · 다시 판정이 끝날 때까지 지우지 않는다 (Q9 설계 ⑯ 240 줄 · ㉔ 247 줄 = 합치기에 러너 · 킷이 필요).
- ⑥ **넘김 지연** = 시간 어림 밖 — 3 판 표는 넘김 지연 0 의 꼴 (kgy 쪽 임계 경로에 단위 시작 7 번 → 넘김 한 번 평균 d h 면 +7d · 3 판 §3-3 (2) 아래 줄 · [추정]).
- ⑦ 한정 — 12 단위 끝-끝 시험은 한 컨테이너 세 바탕에서 이 꼴 (사다리 하나 · 단위 하나 = (가-2) · 나머지 (가-1)) 을 봤다 · 실제 두 기계 · 실제 전송 · 12 단위 전부를 (가-2) 로 · 원장이 떠난 사이 재부팅 = 보지 않았다 (`docs/reviews/rint2_e2e12_20261111/README.md` §9 · 선택지 메모 §2 (가) 표 "못 보인 것").

### 10-8. 실행 정책 문장 · R 동안 운영 규칙 (봉인 · <봉인 날짜> · 1저자 11-10 Q4 · 3 판 Q7 · Q10 · Q11 · 봉인 후보 Q7 · 결과 0 건 · 규칙 · 기계적 보장 아님 표지가 붙은 것은 사슬이 막지 않는다)

- ① **실행 사용자 · umask** — kgy = uid 1003 · 실행 셸마다 `umask 022` (11-09 · 11-12 현장 = 002 · 남은 계획 §2-3 A1) · gabia = uid 0 (root) 그대로 (로그인할 수 있는 일반 계정 없음 · 남은 계획 §0-3 · A3) — root 에게 권한 기반 보호 (단일 작성자 · 0600 값 파일) 는 뜻이 없다 = 운영 규칙.
- ② **단일 작성자** — 계획 사본 · 원장 저장소 · 시도 폴더 · 저장본 폴더 · 판정 폴더 = 실행 사용자 하나만 쓴다 · 손으로 고치지 않는다 (판정이 결과 줄을 폴더 증거로 다시 센다 · §10-5 아 ①) · kgy 의 `~/sdcp` 는 0775 (같은 그룹이 바꿀 수 있다 · 그룹 구성원 [미확인]) · 이미 있는 0777 폴더 (`~/sdcp/scripts`) 는 R 출력 자리로 쓰지 않는다 (남은 계획 §0-3) — 규칙 · 기계적 보장 아님.
- ③ **값 비열람** — σ · SV 비 · origin 산포 = 판정 결과 파일 (`verdict_results.json` · 0600) 에만 · `--show-results` = 주 판정 런이 다 끝난 뒤 한 번 · 열람 기록 (§4-1 · §10-4) · root · 같은 uid 는 0600 을 막지 못한다 = 운영 규칙 (남은 계획 §2-3 A4 · 판정문 [J6] 77 줄의 한정).
- ④ **R 동안 (사다리 시작부터 다시 판정까지) 바꾸지 않는 것** — 두 기계의 실행 트리 (`~/dem-ca1` = 봉인 커밋 · 깨끗 · `git checkout` · `pull` · `touch` · 파일 추가 없음 · 사슬이 단계마다 코드 키 · HEAD · dirty 를 대조 · 판정 JSON 이 이 봉인본의 sha256 · 절대 경로를 싣고 다시 판정이 바이트 대조) · 이 봉인본 (실행 트리의 사본 · 원본 자리의 봉인 전 판도) · 계획 사본 · 저장본 폴더 (지우기 · 이름 바꾸기 · 모드 바꾸기 · 넣기 없음) · venv (`~/dem-venv` · 두 기계 · 판 · 자리 — 저장본 열쇠에 venv 실경로가 든다) · **두 기계의 GPU 드라이버 · CUDA (자동 갱신 멈춤 · 재실행 자격 = 원 시도 환경 지문 모든 칸 · Q9 설계 §3-5 147 줄 · 방법 = 1저자 · 기계마다)**.
- ⑤ **GPU 비움** — R 동안 두 기계 GPU 에 다른 계산을 띄우지 않는다 (kgy = 1저자 DFT 얼림 · ⑥ 시도 3 · 4 의 조건 · 3 판 R3-16) · 같은 기계에서 사슬 둘을 동시에 띄우지 않는다 (호스트 메모리 2 × 26–34 GB > 62.7 GiB · 2 판 E-2 의 5 · 9).
- ⑥ **띄우는 꼴** — `nohup` · 작업 폴더 = `~/sdcp` (실행 트리 밖) · 출력 = 실행 트리 밖 로그 파일로 돌린다 (`nohup.out` 은 `.gitignore` 밖 → 실행 트리 안에 생기면 dirty = `CODE_PIN_MISMATCH` · 남은 계획 §2-2 C5) — 규칙.
- ⑦ **재실행** — 원 시도가 돈 그 `--out` 바탕에서만 · 같은 기계 · 환경 지문 모든 칸 (§10-5 나 ⑩) · 멈춘 GPU 런은 `--resume` 하지 않고 결과 전 재시도 규칙대로 새 시도 (§10-5 라) · 다른 바탕에서 재실행을 한 번 시도해 거부되면 원 바탕의 재실행도 거부된다 (12 단위 끝-끝 시험 관찰 (다) · 푸는 길 = 문서 · 시험에 없음) — 규칙.
- ⑧ **원장 밖 킷 풀이 금지** (Q9 설계 §3-5 159 줄 · SBE · DBE · 계획의 어떤 런이든 · 환경 시험 = 합성 · 게이트 · S0 단계만) — 규칙.
- ⑨ **최대 시도 수 8** — 같은 대상의 원장 항목 수 (풀기 전 거부 · 재실행 포함 · §10-5 나 ⑦) · 채택 = 원장 차례로 처음 결과 전 멈춤이 아닌 시도 + 재실행 사슬 (수가 커도 고르는 길이 늘지 않는다 · Q9 설계 §3-5 152 줄) · 3 판 Q10 (처음 제안 5 → 8 · 10-19 재압밀 기록 = 계산 전 멈춤 넷 뒤 다섯째).
- ⑩ **넘침 점 배정 안전 규칙** (3 판 Q11 · 명령 문서 운영 규칙 · 기준 값 2/3 은 바꿀 수 있다) — 점을 주기 전에 그 기계의 첫 DBE 모서리 팔 실측 비로 그 기계의 첫 점 (8 팔 · 짓기 5) 시간을 다시 어림해 **112 h (= 168 h 의 2/3)** 를 넘으면 그 기계에 주지 않는다 · 둘 다 넘으면 멈추고 1저자 · 넘침 점은 kgy 먼저 (배정 = 봉인 밖) · **어림 꼴 = 시간 다시 어림 3 판 §3-3 (4) 의 "팔 전체" 꼴** (1저자 11-17 봉인 후보 Q7): 첫 점 ≈ r × (8 × T_hit + 5 × (T_first − T_hit)) · r = T_DBE ÷ T_first (T_DBE = 그 기계 첫 단위의 모서리 런 · T_first = 그 기계 사다리에서 저장본을 지은 첫 보통 점 런 · T_hit = 그 사다리의 적중 런 · 시간 = 런 기록 `seconds` · σ 를 열지 않는다) · 3 판 값 (kgy 4,932 · 9,067 · gabia 6,682 · 10,817 s · r 2.933) 이면 kgy 49.0 h · gabia 60.4 h (3 판 §3-3 (4) 와 같음) · 줄 = kgy 명령 문서 §3-1b (6).

====

## R-14 · §11 ⑥ 뒤 (숫자 탐침 기록)

@op after 674 6. 실침대 숫자 탐침 (값 봉인) → 전처리 · maxiter · 시간 상한을 §10 에 기록.

====
   - (봉인 · <봉인 날짜> · 3 판 Q2 · Q3 · Q5) ⑥ = 개발 탐침 원장 (`docs/reviews/rint2_dev_probe_ledger_20261026.md`) §3 시도 3 · 4 (11-16 · kgy · 핀 `64e4d213e` = 봉인 커밋과 풀이 코드 목록 같음 · 원장 §2 핀 칸 = 풀이 코드 목록 기준 · 1저자 11-12 Q5) · 묶음 `docs/data/rint2_probe6_a3_20261116/` · `docs/data/rint2_probe6_a4_20261116/` · 시간 다시 어림 3 판 (stoic 기록 · 봉인 기록 README §사) → **전처리 = Jacobi (C 꼴 · 64e4d213e 코드 기본) · maxiter = 5,000,000 (계획 `p2_extra`) · 시간 상한 = 168 h (`exec_policy.max_hours`)** · 값 (σ) 열람 0 · ⑥ 의 값은 이 세 숫자에만 쓴다 (원장 §2 채택 불가).
====

## R-15 · §12 실행 기록

@op after 696 - ⬜ 숫자 탐침

====
- ✅ (11-11 · 11-16) 숫자 탐침 = 개발 탐침 원장 §3 시도 1 – 4 (시도 3 · 4 = 최종 핀 `64e4d213e` · σ 열람 0) · 결정점 = 시간 다시 어림 3 판 (11-17)
- ✅ (<봉인 날짜>) 봉인 = 이 봉인본을 넣은 커밋 — §2-1 숫자 · 두 해시 · 계획 숫자 블록 · 실행 정책 · §10-1b · §10-6 – §10-8 · 결과 전 등록 넷 (1저자 11-17 · Codex 2/2 조건부 GO 뒤 · 머리 절 R-00) · 그 커밋의 봉인 관문 영수증 = 커밋 밖 기록 (자리 = 봉인 기록 README)
- ⬜ 현장 확인 (두 기계 · PIN = 봉인 커밋) · 두 기계 조립 같음 (11-12 Q10) → S0 단계 2 (DBE · 인자 커밋 = 봉인 커밋 · `--r-doc <봉인본>`) → R (모든 사슬 단계 `--registration ~/dem-ca1/<봉인본>`) — 실행 승인 = 1저자 (Codex 2/2 는 실행 승인이 아니다)
====
