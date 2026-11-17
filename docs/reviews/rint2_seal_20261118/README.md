# Rint ② 봉인 기록 (20261118 · 결과 0 건 · 실행 0 · σ 열람 0)

- **무엇** = 등록 R 의 봉인 커밋 기록.  봉인 커밋 = 코드 핀 `64e4d213e` (Rint 고정 가지 `codex/rint-rtr01-receipt-1113` 끝 · 40 자리 64e4d213e8267bafaf3ae5af00a42996cefd3f33) 위 **문서 · 자료 커밋 하나** · 가지 `claude/rint2-seal-20261118` (1저자 11-17 · 새 원격 가지 push 허락 포함).  `scripts/` 무변경 → 풀이 코드 목록 · ⑥ 다시 없음.
- **봉인 꼴** = 넷째 길 (1저자 11-17 봉인 후보 Q1) — 봉인본 = 새 파일 `docs/reviews/rint2_seal_20261118/registration_R_sealed.md` · 원본 자리 `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` = 핀 판 + 머리 표지 한 줄 (해시 칸 ⬜ 그대로) · 사슬의 모든 단계 명령 = `--registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md` · S0 단계 2 = `--r-doc docs/reviews/rint2_seal_20261118/registration_R_sealed.md`.
- **지위** — Codex 2/2 (11-17 · 리뷰 핀 `f40d005ac` · 판정 = **조건부 GO = 봉인 준비 범위만** · 새 P1 · P2 · P3 0) 의 남은 조건 (§7 1–3) 을 채우는 커밋이다.  실제 실행 · 정량 판정 · 운영 GO · 공유 원장 종결은 승인되지 않았다 — 봉인 뒤 현장 자격 (두 기계) · S0 단계 2 · R 실행 승인 = 1저자 · 따로.
- 이 폴더 = `README.md` (이 글) · `tools/` (봉인본을 다시 만드는 도구 + 붙일 글 조각 둘) · `evidence/` (도구 출력 목록 `make_sealed_copy_manifest.json` + 봉인 관문 확인 도구 `evidence/tools/`).  **봉인 관문 영수증 (이 커밋에서 잰 것) 은 이 커밋 안에 둘 수 없다** (커밋 sha 가 바뀐다) → 커밋 밖 stoic 기록 (§다).

## 가. 봉인 값

| 자리 | 값 |
|---|---|
| 봉인 날짜 · 가지 | 20261118 · `claude/rint2-seal-20261118` |
| 결과 전 등록 넷 (1저자 11-17 20:0x KST · Codex 2/2 판정 뒤 · σ 열람 0) | `max_ladder_points` = **16** · `calib_rj_ratio_max` = **`"none"`** (상한을 두지 않음 · 등록 R §3-2b ④ · 사슬 `PLAN_NO_CAP`) · `sv_cf_threshold` = **1.5745499360744093** (= exp(G0/2) · G0 = ln(4.68/1.8877) = 0.9079389531370043 · IEEE double · 같은 식을 sqrt(4.68/1.8877) 로 세면 끝자리 1.5745499360744095 = 계획 값은 앞의 것) · `sv_cf_scope` = **`"all3"`** (1저자 10-23 결정 그대로) |
| Codex 2/2 Q3 처분 | 판정문의 시험 전용 값 (12 · none · 2.0 · all3) 을 옮긴 것이 아니다 — 넷 다 1저자 결정 (점 상한 16 = 3 판 12 점 가정 + RCA-01 회로 12 점 · 천장 근처 꺾임 망 13 점 위 여유 · none = 등록 글의 "상한 없음" 선택지 · 문턱 = 위 식 · all3 = 10-23) |
| 앞서 정한 봉인 숫자 (3 판 Q1 – Q3 · Q9 – Q11 · 10-23 Q11) | maxiter 5,000,000 (`p2_extra` = `--step3-maxiter 5000000`) · `max_hours` 168 · `max_attempts` 8 · 허용 기계 kgy · gabia · v100 (v100 = 1저자 요청 때만) · `env_unit` = python 3.8 · numpy 1.24.4 · scipy 1.10.1 · 원장 이어달리기 (가-2) · 넘침 점 112 h 규칙 · 마감 12-05 24:00 KST |
| R 계획 파일 | `docs/data/rint2_r_plan_20261118/ca1_plan.json` · 682 B · sha256 d8595a52b67f361d02329eb3fefd1472ebb3b8276305134b34e6190376c2abf8 · 꼴 = `json.dumps(…, indent=1, sort_keys=True)` · ASCII · 끝 줄바꿈 없음 · schema `rint-r-plan-v3` · 후보 (넷 null · f09b3efb…) 에서 바뀐 칸 = 넷뿐 |
| S0 계획 (11-16) | `docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json` · 1,485 B · sha256 6346d9ed5fda248b89d1e28dbcb35c90d67264f060be345673c7da63f9924520 · 두 계획 대조 (사슬 `plans_cross_problems`) = 문제 없음 |
| 계획 숫자 블록 | 핀 사슬 `--stage plan-doc` 출력 그대로 (도구가 넣음) · 블록 바이트 sha256 d67a0dfa2e9725efa33ac3e9f7222e79ac706fd4c3a80d2a58849f77b258ddde |
| 봉인본 | 339,524 B · 909 줄 · sha256 bcc0c118ce3f20999673dabdc6ab5e636f5ad81ccdca890665f8229a180e3ccd (kgy 명령 문서 §3-1b (2) 의 `sha256sum` 둘째 줄이 이 값과 같아야) |
| 원본 자리 (표지 한 줄) | 301,757 B · 748 줄 · sha256 dcdd1d3726284ce54c11ddfe4d727318b12329ee4afc82e91330803a46cfc67a (핀 판 301,281 B · 219b6351… + 한 줄) |
| kgy 명령 문서 (K 조각) | `docs/reviews/rint2_kgy_commands_20261020.md` · 115,083 B · sha256 eda9d541c78b16c6b74520971f2f31965920d4a61875720651da1525bbdd69a7 (핀 판 79,983 B · 0fe96bb8…) |
| 도구 · 조각 | `docs/reviews/rint2_seal_20261118/tools/make_sealed_copy.py` sha256 f923dede1112d6aad8cd60ed18e78125c5b6258bf17b68c4ab3441b93b747b36 (= Codex 2/2 에 낸 v2.1 판 바이트) · `docs/reviews/rint2_seal_20261118/tools/registration_R_insert.md` 14c909d2… · `docs/reviews/rint2_seal_20261118/tools/commands_doc_insert.md` db54057a… |

- 봉인 판 조각 = v2.1 조각 + Codex 2/2 §7-3 문구뿐 — 봉인본 머리 절 R-00 끝 두 줄 (봉인 값 · 지위 · 한정 셋) · R-15 (⬜ 한 줄 → ✅ 봉인 한 줄 + ⬜ 다음 차례 한 줄) · 명령 문서 K-03 머리 한 줄.  그 밖 조각 글 = v2.1 그대로 (봉인본 바뀐 곳 = 핀 판 대비 머리 절 + 조각 자리뿐 · 도구가 대조).
- 같은 입력 = 같은 바이트 (도구 · 입력 파일 이름은 출력에 넣지 않는다) — 재현 = §마.

## 나. Codex 2/2 §7 조건 — 이 커밋의 대응

| 조건 (판정문 §7) | 대응 |
|---|---|
| 1. 1저자가 네 값 · 봉인 날짜 · 가지 · 정책을 결과 전에 확정 · 점 수 등 시간 가정이 바뀌면 기존 모형으로 예산도 갱신 | §가 (11-17 결정) · 시간 예산 = §라 (3 판 모형 그대로 · 사다리 점 12 → 16) |
| 2. 확정 입력으로 도구 `--final` → 새 문서 · 계획 · 명령 · 최종 커밋에서 두 계획 · 해시 · 등록 경로 · 원본 공란 · 고정 참조 · 풀이 코드 다섯 경계 대조 · 봉인 관문 = 실제 그 커밋의 영수증 | 도구 `--final` (출력 목록 = `docs/reviews/rint2_seal_20261118/evidence/make_sealed_copy_manifest.json` · `seal_status` final · 확인 11 + 계획 확인 3 참) · 영수증 = 이 커밋 sha 로 잰 것 (§다 · 커밋 밖) |
| 3. "완료 보장 아님" · RCA-11 한정 종결 · env_unit 과 전체 실행 환경의 차이를 수령 문구 · 실행 절차에 유지 · 환경 고정 계약의 기준 기록과 확인 담당 | 봉인본 머리 절 (R-00 한정 ① ② ③) · kgy 명령 문서 §3-1b 머리 (한정 한 줄) · 이 글 아래 줄 |

- **한정 (옮길 때 빼지 않는다)** — ① maxiter 5,000,000 · 168 h · 시도 8 · 넘침 점 112 h 규칙 = 정책 값 · **완료 보장 아님** (NOT_COMPUTED 가 없다는 보증이 아니다 · 넘침 규칙은 시간 안에 될 점도 보수적으로 멈출 수 있다 · 판정문 §6 의 2) ② RCA-11 = **이 R 의 입력 · 선택 고정 (등록 R §2-1 u 행 = 원래 MPM 경로 표본화) 만 한정 종결** · 원장의 지적 전체 = 부분 (열림 그대로) ③ `env_unit` = 사슬이 대조하는 같음 단위 (python 부 판 · numpy · scipy 판 글자) 일 뿐 **전체 실행 환경이 아니다** — python 패치 판 · 실행 파일 · cupy · GPU · 드라이버 · BLAS 계산 경로 · OPENBLAS_CORETYPE · CPU 모델 · numpy SIMD 는 사슬이 단계마다 환경 지문의 기록만 칸에 적고 대조하지 않는다 (`scripts/rint_r_chain.py` 의 env_record · 핀 판 1074 줄).
- **환경 고정 계약 — 기준 기록 · 확인 담당** — 기준 기록 = 봉인 직전 두 기계 현장 확인 출력 (kgy 명령 문서 §3-1b (2) 의 venv 한 줄 `3.8.10 1.24.4 1.10.1 12.3.0` · `nvidia-smi` 줄 · 1저자가 적어 둔다) + 사슬 첫 단계 요약의 환경 지문 · 확인 담당 = 1저자 (현장 확인 · 두 기계 조립 같음 11-12 Q10 · R 동안 venv · 드라이버 갱신 멈춤) · 사슬 (`env_unit` 다르면 멈춤 · 시도마다 같은 설정 = 계획 · 코드 · 침대 · 환경 지문).
- 3 판 R3-19 (보조 `time_budget_v3.py` 의 5M 주 + 이어 29.1 / 42.4 h 출력 = 이어 반복당 시간을 주 값으로 쓴 P3) = 판정문 §6 의 1 그대로 — 바른 값 29.8 / 43.3 h (3 판 본문) · 이 봉인의 5M · 168 h 선택을 바꾸지 않는다 · 옛 보조 출력을 다시 쓸 때 본문 값과 맞춘다.

## 다. 봉인 관문 영수증 — 이 커밋 밖 (stoic 기록)

- 자리 = stoic (`claude/stoic-knuth-NObVQ`) 의 docs/data/rint2_seal_receipts_20261118/ (봉인 push 뒤 다음 stoic 커밋 · 이 가지에는 없다) — 이 커밋 sha 를 머리에 적고 잰다.
- 항목 (후보 v2.1 증거와 같은 꼴 · 봉인 값으로 다시): ③ sh 사슬 명령 인자 대조 (`check_sh_commands.py` · 기대 셈 = 그때 독립 셈) · ④ `--stage plan-doc --check-doc` (봉인본 = `PLAN_DOC_SAME` rc 0 · 기본 = 원본 자리 = rc 3) · ④′ 사슬 함수 (해시 줄 둘 = 계획 · S0 sha256 · 원본 자리 = `PLAN_HASH_UNREGISTERED`) · ⑤ S0 단계 2 관문 `ca_s0_census.verify_plan_commit` (이 커밋 · `--r-doc` = 봉인본 · 결과 전 넷이 채워졌으니 **통과**가 기대 · 기본 r_doc = 거부) · 사슬 시험 전체 `scripts/test_rint_r_chain.py` · e2e `E17` · `K01` · `PC18` · `PC20` · `EP06` · 원본 자리를 읽는 게이트 시험 셋 · `scripts/check_doc_refs.py` · 핀 판 `scripts/check_method_discipline.py` · 철회값 등록부 (바뀐 파일) · 다섯 경계 (`check_seal_files.py`) · 도구 `--selftest` · 게이트 (이 커밋 · 두 조각 이상 · 실패 0 뒤 push).
- 후보 단계 증거 (v2.1 · 이름 `seal-form-scratch` 의 G″ · 보기 날짜 20261120 · 넷 null) = Codex 2/2 요청 ZIP (sha256 7da8e749ed0954d5777bffd0d16f86ce490e2b15ed371077f3174a88e1503f88) 과 stoic 의 docs/reviews/rint2_seal_round2_20261117/ 기록 묶음 (`f40d005ac` 판) — 이 커밋에는 옮기지 않았다 (봉인 값이 아니고 경로 · 날짜가 다르다).

## 라. 시간 예산 — 사다리 점 상한 16 (Codex 2/2 §7-1 · 3 판 모형 그대로 · 추정)

- 모형 = stoic `b3481336c:docs/reviews/rint2_time_reestimate_20261111/v3/work/time_budget_v3.py` (같은 바이트 = `f40d005ac` 판 · blob 5289b6024470d877f6f5270b700354926efb282c) · 바꾼 것 = 법칙마다 사다리 팔 수 한 줄 (`LADDER_ARMS = 12 + 4 + 2 + 1` → `16 + 4 + 2 + 1` · 끝 origin 4 · SBE origin 2 · no-op 1 그대로) · 12 점 판 출력 = 3 판 리포 JSON 과 바이트 같음 (재현 확인) · 그 밖 가정 = 3 판 그대로 (R 시작 11-20 · s · r · m · gabia 속도 · 넘침 없음 · DBE 는 재지 않았다).
- 상한 16 = 최악 (사다리가 16 점을 다 쓸 때) · 13 점 (천장 근처 꺾임 망) 도 함께 셈.

| 꼴 (3 판 표 이름) | 12 점 (3 판) | 13 점 | 16 점 (상한) |
|---|---|---|---|
| 사다리 단계 한 법칙 (팔 꼴 · s 1 · 등록 비) kgy · gabia | 29.5 · 38.7 h | 30.8 · 40.6 h | 35.0 · 46.1 h |
| 주 · 두 대 · GPU 팔 끝 (팔 꼴 · s 1) | 184.2 – 208.7 h | 186.0 – 210.5 h | 191.6 – 216.1 h |
| 그 여유 (12-06 00:00 = 12-05 24:00 까지 · 시작 11-20) | 175.3 – 199.8 h | 173.5 – 198.0 h | 167.9 – 192.4 h |
| 넘침 하나 더한 GPU 끝 여유 (팔 꼴 · s 1) | 48.9 h | 47.0 h | 41.4 h |
| 두 대 나눔이 무너져 kgy 한 대 (팔 꼴 · s 1 · 높은 끝) 여유 | 44.4 h | 41.6 h | 33.4 h |
| 민감도 m 2 (높은 끝) 여유 | 36.4 h | 33.0 h | 22.8 h |
| 민감도 DBE 비 두 배 (5.866 · 높은 끝) 여유 · 끝 | **5.9 h** · 12-05 18시 | 4.0 h · 12-05 20시 | **−1.6 h** · 12-06 01시 |
| 3 판에서 이미 마감 밖이던 꼴 (넘침 · 팔 꼴 · s 1 · ×2 · 민감도 DBE 비 두 배 · m 2) | −246.3 · −242.5 h | −248.2 · −245.9 h | −253.7 · −256.1 h |

- 읽기 — 점 넷을 더하면 늦은 기계 (gabia) 사다리가 +7.4 h · 그만큼 뒤 단계가 밀린다.  주 어림과 대체 꼴은 16 점에서도 12-05 안 (주 여유 167.9 h · kgy 한 대 33.4 h · 넘침 하나 41.4 h) · ⚠ **민감도 "DBE 비 두 배" 의 높은 끝은 12 점에서 여유 5.9 h → 16 점에서 −1.6 h (12-06 01시 끝 · 시작 11-20 00:00 가정)** — 16 점을 다 쓰고 DBE 비가 두 배일 때만 · 시작이 그보다 2 h 이상 이르면 다시 안 (봉인 11-18 · 시작 가정 11-20 은 3 판 가정 그대로).  3 판에서 이미 밖이던 꼴은 그대로 밖.  사다리 단계 한 시도 (최대 46.1 h) < `max_hours` 168.  추정 · 새 기준 · 합격선 아님.
- 셈 원자료 (모형 사본 · 12 · 13 · 16 점 출력 JSON · 비교 스크립트) = §다 의 stoic 기록에 함께 둔다.

## 마. 재현 (`python3 -I` · 리포 밖 빈 폴더)

```sh
# 핀 판 원본 둘 · 사슬 (읽기만)
git show 64e4d213e:docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md > pin_reg.md   # sha256 219b6351…
git show 64e4d213e:docs/reviews/rint2_kgy_commands_20261020.md > pin_cmd.md                         # sha256 0fe96bb8…
git archive 64e4d213e scripts | tar -x -C pin_tree                                                 # 사슬 = pin_tree/scripts/rint_r_chain.py
# 봉인 꼴 파일 넷 (이 커밋의 tools/ · 계획 · S0 계획)
python3 -I make_sealed_copy.py --pin-reg pin_reg.md --pin-cmd pin_cmd.md \
    --reg-insert registration_R_insert.md --cmd-insert commands_doc_insert.md \
    --plan ca1_plan.json --s0-plan cjunc_plan.json --chain pin_tree/scripts/rint_r_chain.py \
    --seal-date 20261118 --seal-branch claude/rint2-seal-20261118 --final --out <빈 폴더>
#   → 출력 넷 = 이 커밋의 같은 경로 바이트 · _manifest.json = evidence/make_sealed_copy_manifest.json
```

## 바. 1저자 결정 (11-17 · 봉인 후보 Q1 – Q8 · *"권고대로해 · 이런걸로 병목 만들지마"*)

| # | 결정 | 반영 자리 |
|---|---|---|
| Q1 | 봉인 꼴 = 봉인본 새 파일 `docs/reviews/rint2_seal_<봉인 날짜>/registration_R_sealed.md` (원본 등록 R = 핀 판 그대로 + 머리 표지 한 줄 · `scripts/` 무변경 · ⑥ 다시 없음) · 모든 사슬 단계 명령에 `--registration <봉인본>` · S0 단계 2 명령에 `--r-doc <봉인본>` | 도구 · R-00 · R-MARK · R-09 · R-10 · K-01 – K-05 |
| Q2 | 12 단위 · 저장본 실행 줄 = `sh` 블록 (K01 은 `bash` 만 읽는다) + 사슬 argparse 대조 기록을 봉인 기록에 | R-10 · K-03 · 영수증 ③ (§다) |
| Q3 | 계획 자리 = `docs/data/rint2_r_plan_<봉인 날짜>/ca1_plan.json` · 꼴 = indent 1 · sort_keys · 끝 줄바꿈 없음 · schema `rint-r-plan-v3` (문서의 "v2 · 칸 11" = 낡은 글 → 표지) | R-05 · K-02 · §가 |
| Q4 | R 저장본 = 기계마다 새 빈 폴더 `~/ca1_cjstore` (⑥ · S0 시험 저장본 안 씀) | R-10 · R-13 §10-6 ③ · K-03 (1) (2) |
| Q5 | 원장 넘김 = 사슬과 같은 잠금 파일에 `flock` (gabia 에 없으면 "그 기계 사슬이 시작 확인 뒤 도는 중일 때만 넘긴다" · 11-17 현장 = 두 기계 다 있음 → 이 규칙 = 한정만) | R-13 §10-7 ① · K-03 (2) (5) |
| Q6 | 사다리 P0 = kgy · P1 = gabia · 12 단위 첫 배정 kgy 7 · gabia 5 · 합치는 기계 = kgy · 합친 폴더 `ca1_predict` · `ca1_predict_x` (봉인 밖) | R-08 · R-10 · R-13 §10-7 ⑤ · K-03 (1) (6) |
| Q7 | 넘침 점 안전 규칙 어림 = 3 판 §3-3 (4) "팔 전체" 꼴 | R-13 §10-8 ⑩ · K-03 (6) (줄 + 셈 한 줄) |
| Q8 | 감도 (FIBRE · UNREG · GRID · SVORDER) 경로 = R 시작 전 따로 (이 봉인 밖 · ⬜) | R-10 끝 줄 |
| 11-17 현장 뒤 | R venv = 두 기계 `~/dem-venv` (3.8.10 · 1.24.4 · 1.10.1 · cupy 12.3.0 = kgy 와 패치 판까지 같음 · gabia `~/rint-venv38` 3.8.20 = 손대지 않음) · 봉인 직전 확인 줄 = 두 기계 같은 한 줄 · 기대 `3.8.10 1.24.4 1.10.1 12.3.0` | R-10 (0) · R-13 §10-8 ④ · K-03 (1) (2) |
| 11-17 밤 (Codex 2/2 뒤) | 결과 전 등록 넷 · 봉인 날짜 20261118 · 가지 `claude/rint2-seal-20261118` (§가) | 계획 파일 · R-00 · R-15 |

## 사. stoic 기록 가리킴 (이 가지에 넣지 않은 것 · `<커밋>:<경로>` · blob · 11-17 밤 `git cat-file -e` 로 다시 확인)

| 무엇 | 가리킴 | blob · 나무 | 쓰는 곳 |
|---|---|---|---|
| 시간 다시 어림 3 판 (README 끝 절 · §3-2 · §3-3 (4) · §3-4 · §3-6b · §3-6c = 3 판 Q1 – Q11) | `b3481336c:docs/reviews/rint2_time_reestimate_20261111/README.md` (그 꼴이 된 커밋 = `b80f10d08` · 첫 반입 = `c0c3b1ff5` · 셋 다 원격 stoic 안) | blob 8e4781ac4e89b5968e788ed21d486824ed3fcf45 | 봉인본 R-00 · R-12 · R-13 ⑩ · R-14 · 명령 문서 §3-1b (6) · 이 글 §라 |
| 3 판 숫자 · 산술 | `b3481336c:docs/reviews/rint2_time_reestimate_20261111/v3/numbers_sources.tsv` · `…/v3/work/time_budget_v3.py` | 나무 (v3) b07ecf38e1fa620b3b9e81fc51b0f282670cfb1f | 같음 · §라 |
| 11-16 S0 kit JSON 의 등록부 `allowed_in` | 원격 stoic `2da71fe5a` (`docs/reviews/claims.json`) | blob 3f83245436d927dc534880fa32a958bc99ce7ddf | 이 커밋의 `docs/reviews/claims.json` = 같은 바이트 |
| Codex 2/2 요청서 · ZIP 만드는 도구 (리뷰 핀) | `f40d005ac:docs/reviews/codex_rint2_seal_round2_request_20261117.md` (원격 stoic · 리뷰 핀 = 그 커밋) | — | §나 · §다 |
| Codex 2/2 판정문 · 증거 | 1저자가 전한 증거 ZIP (sha256 98f95a774bd7be8e4cdb991ac27d8858b7d7f081465614933e50c33abe63b499 · 432 항목) — stoic 반입 = 봉인 push 뒤 다음 stoic 커밋 | — | §나 |

- 이 가지의 같은 경로 `docs/reviews/rint2_time_reestimate_20261111/README.md` = 2 판까지 (3 판 절 없음) · 원장 §2 핀 칸 문장의 근거 "11-17 Q5" 는 3 판 (위 가리킴) 에 있다.
- 이 커밋에 넣은 공유 파일 44 개 (자료 폴더 셋 40 · 개발 탐침 원장 · q14 준비 둘 · `docs/reviews/claims.json`) = stoic 끝 (11-17 밤 · 반입 ⑩ 줄 845fa2672 · 봉인 때 아직 원격 밖) 의 같은 경로와 blob 44/44 같음 [실측].
