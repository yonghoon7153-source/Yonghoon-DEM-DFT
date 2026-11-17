# kgy 명령 문서에 붙일 글 — Rint ② 봉인 후보 v2 (11-17 · 문서만 · 결과 0 건 · 실행 0 · σ 열람 0)

- **대상** = `docs/reviews/rint2_kgy_commands_20261020.md` @`64e4d213e` (79,983 B · 603 줄 · sha256 0fe96bb83bf0795a4f1f18e2e1968ba8dacbad3f8ace84f97828d407703fe983 · 11-17 06:56 UTC 측정 = 본 리포 HEAD · 원격 stoic `b3481336c` · stoic-next 끝 `5645b86c8` 의 같은 경로와 바이트 같음 [실측 · 그 시점 값]).  줄 번호 = 그 판.  이 문서는 봉인 커밋에서 **제자리** 를 고친다 (봉인본과 달리 새 파일이 아니다 · 1저자 11-17 봉인 후보 Q1 = 등록 R 만 새 파일).
- **꼴 · 자리표** = 등록 R 붙일 글 (`registration_R_insert.md`) 머리와 같다 (`@op` 한 줄 + `====` 사이 그대로 · 도구 `make_sealed_copy.py` 가 넣는다 · `<봉인 날짜>` · `<봉인본>` · `<봉인 가지>` = 도구가 채움 · `<봉인 커밋>` · `<n>` 꼴 = 실행 때 · 주소 · 포트 · 계정 · 홈 경로는 적지 않는다 (`~` = 실행 셸이 펼친다)).
- **bash 블록 · sh 블록** — 리포 시험 K01 (`scripts/test_rint_r_chain.py` 9602 줄) 은 이 문서와 원본 자리 등록 R 의 `bash` 울타리만 읽고, 두 문서의 인자 이름 집합이 같아야 한다 → 그 블록 (인자 계약 꼴) 은 **주석 줄만** 더한다 (K-01 · K-02 · K-05 · 사슬 인자 그대로).  R 의 실제 실행 줄 = 새 절 §3-1b 의 `sh` 울타리 (K01 은 읽지 않는다 · 1저자 11-17 봉인 후보 Q2) — 그 줄의 인자 대조 = 봉인 기록 `evidence/` (사슬 argparse · 단계 함수 받기만 · 실제 0755 폴더 · 봉인본 R-10 과 인자 이름 같음).
- **모든 사슬 명령 = `--registration ~/dem-ca1/<봉인본>` · S0 단계 2 = `--r-doc <봉인본>`** (봉인 후보 Q1 · 사슬 · S0 기본 경로 = 원본 자리 = 봉인 전 판 → 해시 줄 ⬜ → 멈춤).
- v2.1 (11-17 · 내부 반박 리뷰 · Codex 아님) 에서 바뀐 것: (2) `command -v python3` 기대 = `…/bin/python3` · (2b) venv 켬 + 판 출력 줄 · same-version 대조와 S0 줄을 `&&` 로 묶음 · 끝 rc 줄 (`PIPESTATUS`) · (5) 받는 쪽 = 세워 둔 자리에서 먼저 `pull --ff-only` 뒤 되살림 + `RECV_OK` 기계 대조 · (6) T_hit 의 "(중앙값)" 지움 (3 판 = 한 런 실측 · 봉인본 R-13 ⑩ 과 같은 글).
- v1 (`../seal_candidate/commands_doc_insert.md`) 에서 바뀐 것 (v2): K-01 · K-02 주석 = "실제 실행 = 봉인본 · `--registration`" · K-03 = 모든 사슬 명령 `--registration` · (2b) S0 단계 2 새로 (`--r-doc`) · (2) 봉인본 · 기본 경로 멈춤 확인 줄 · (5) `flock` 없는 기계 규칙 (봉인 후보 Q5) · (6) 안전 규칙 어림 꼴 = 3 판 "팔 전체" (봉인 후보 Q7) · K-05 새로 (§2-3 블록 주석 한 줄).
- **봉인 판 (11-17 밤 · 봉인 20261118 · Codex 2/2 §7-3)** 에서 바뀐 것: K-03 머리 (실행 정책 문장) 에 한정 한 줄 — 그 밖 조각 글 = v2.1 그대로.

## K-01 · §3 실제 명령 bash 블록 머리 (주석 줄)

@op after 480 # ⛔ 발사 금지 — 꼴만 (10-21 · 실제 이름 · 등록 R §11 관문 1–9 뒤)

- 꼴 = 그 줄 뒤에 주석 줄 (블록 안 · K01 은 주석 줄을 읽지 않는다).

====
# ★ (봉인 · <봉인 날짜>) 이 블록 = 인자 계약 꼴 (리포 시험 K01 이 사슬 argparse 와 대조하는 bash 줄) — 실제 실행 = 봉인본 · --registration ~/dem-ca1/<봉인본> (아래 §3-1b 의 sh 블록)
#   (저장본 --cjunc-store · 12 단위 · 넘침 점 · 합치기 · 원장 이어달리기 (가-2) · --max-hours 168 · --machine kgy | gabia · S0 단계 2 = --r-doc <봉인본>)
#   아래 (4) 한 기계 예측 줄 = 이 등록의 경로가 아니다 (원장 하나 = 경로 하나 · 등록 R §10-5 가 ⑮ · 1저자 11-10 Q7)
#   다음 줄의 --untracked-files=no 는 사슬보다 덜 본다 (사슬 · 현장 도구 = normal · 남은 계획 §9 어긋남 7) → §3-1b (2) 의 줄을 쓴다
====

## K-02 · §3 계획 파일 줄 (주석 줄)

@op after 486 # (0) R 런 계획 파일 = 등록 R §2-1 개정 커밋의 파일

====
# ★ (봉인 · <봉인 날짜>) 코드 = rint-r-plan-v3 · 칸 12 (= 위 v2 칸 11 + exec_policy 8 칸 · rint_r_chain.PLAN_SCHEMA · v2 계획 = PLAN_INVALID · 1저자 11-17 봉인 후보 Q3)
#   봉인 계획 파일 = ~/dem-ca1/docs/data/rint2_r_plan_<봉인 날짜>/ca1_plan.json (아래 cp 줄의 자리표 자리) · 해시 · 블록 = 봉인본 §2-1 (원본 자리의 줄은 ⬜ 그대로)
#   실제 실행 = 봉인본 · --registration ~/dem-ca1/<봉인본> (§3-1b) — 아래 sha256sum 줄의 대조 대상 = 봉인본의 '| 계획 해시 |' 줄
====

## K-05 · §2-3 S0 단계 2 블록 (주석 줄)

@op after 425 # ⛔ (10-21 · PRE-design-14 · 철회) 가지 끝 FETCH_HEAD

- 꼴 = 그 줄 뒤에 주석 두 줄 (블록 안 · 인자 그대로).

====
# ★ (봉인 · <봉인 날짜>) 이 블록 = 인자 계약 꼴 — 실제 S0 단계 2 = §3-1b (2b) (sh 블록 · 인자 커밋 = 봉인 커밋 · --r-doc <봉인본> · --r-plan-path docs/data/rint2_r_plan_<봉인 날짜>/ca1_plan.json)
#   --r-doc 기본값 = 원본 자리 (봉인 전 판 · 해시 줄 ⬜) 라 이 블록 그대로면 관문이 거부한다 (틀린 결과 없음 · 멈춤)
====

## K-03 · 새 절 §3-1b (12 단위 경로 · 두 기계 · 원장 이어달리기 (가-2))

@op before 564 ## 4. 미리 보이는 쟁점

- 꼴 = 그 줄 바로 앞에 (절 · 빈 줄).

====
## 3-1b. ③′ R 의 실제 실행 — 12 단위 경로 · kgy · gabia 동시 · 원장 이어달리기 (가-2) (봉인 · <봉인 날짜> · 1저자 11-10 Q3 · Q4 · Q7 · 3 판 Q1 – Q11 · 봉인 후보 Q1 – Q7 · 결과 0 건)

> **머리 — 실행 정책 문장** (1저자 11-10 Q4 = 등록 R 의 실행 정책 문장 + 이 블록 머리 · 정본 = 봉인본 §10-8)
> - **등록 문서 = 봉인본** `~/dem-ca1/<봉인본>` — 아래 **모든** 사슬 명령에 `--registration ~/dem-ca1/<봉인본>` · S0 단계 2 에 `--r-doc <봉인본>` (봉인 후보 Q1 · 기본 경로 = 원본 자리 = 봉인 전 판 → 해시 줄 ⬜ → 멈춤 · 틀린 결과는 없다).
> - kgy = uid 1003 · **모든 실행 셸에서 `umask 022`** (11-09 · 11-12 현장 = 002) · gabia = uid 0 (root) 그대로 (일반 로그인 계정 없음) — root · 같은 uid 에게 0600 · 단일 작성자 보호는 뜻이 없다 = 운영 규칙.
> - 단일 작성자 — 계획 사본 · 원장 · 시도 폴더 · 저장본 폴더 · 판정 폴더는 실행 사용자 하나만 · 손으로 고치지 않는다 · kgy `~/sdcp` = 0775 (그룹 구성원 [미확인]) · `~/sdcp/scripts` (0777) 는 R 출력 자리로 쓰지 않는다.
> - 값 비열람 — σ · SV 비 · origin 산포 = `verdict_results.json` (0600) 에만 · `--show-results` = 주 판정 런이 다 끝난 뒤 한 번 · 열람 기록 · 그 밖 화면 · 로그 · 보고에 σ 를 옮기지 않는다.
> - 숫자 = 봉인 계획 그대로: `--max-hours 168` · maxiter 5,000,000 (계획 `p2_extra` · 사슬이 편다) · 최대 시도 수 8 · 허용 기계 kgy · gabia · v100 (v100 = 1저자 요청 때만).
> - **한정 (Codex 2/2 §7-3 · 정본 = 봉인본 머리 절 R-00)** — 위 숫자 (5,000,000 · 168 h · 8 · 넘침 점 112 h) = 정책 값 · **완료 보장 아님** · RCA-11 = 이 R 의 입력 · 선택 고정만 한정 종결 (원장 전체 = 부분) · `env_unit` = 같음 대조 단위일 뿐 전체 실행 환경이 아니다 (python 패치 판 · cupy · GPU · 드라이버 · BLAS · SIMD = 사슬이 기록만) · 기준 기록 = 아래 (2) 의 venv 한 줄 · `nvidia-smi` 줄 출력 (두 기계 · 적어 둔다) · 확인 = 1저자 · 실행 승인 = 1저자 (Codex 2/2 = 봉인 준비 범위만).

### (1) 기계마다 바탕 (두 기계 같은 상대 자리 · `~` = 그 기계 실행 사용자 홈)

| 무엇 | 자리 | 비고 |
|---|---|---|
| 실행 트리 | `~/dem-ca1` = `<봉인 커밋>` 의 분리 작업 트리 · **새로 만든다** (봉인 커밋 = `64e4d213e` 위 문서 커밋 · 기존 트리와 다른 체크아웃) · 깨끗 | R (사다리 시작부터 다시 판정까지) 동안 바꾸지 않는다 · 11-17 현장: kgy 기존 트리 = `<HOME>/dem-p6-64e4d213e` · `<HOME>/dem-s0-64e4d213e` (핀 트리) · gabia = `dem-mt` 없음 · 기존 트리 `<HOME>/dem-siteq-11a794674` · `<HOME>/dem-siteq-db86ce9b9` → 기존 트리는 그대로 두고 그 저장소에서 새 작업 트리를 뗀다 ((2) 첫 줄들) · 이름 `~/dem-ca1` 이 이미 있으면 지우지 않고 1저자 — 다른 이름이면 아래 줄의 `~/dem-ca1` 을 그 이름으로 |
| 봉인본 | `~/dem-ca1/<봉인본>` | 봉인 커밋 안 (등록 R 의 봉인 판) · 원본 자리 `~/dem-ca1/docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` = 봉인 전 판 + 표지 한 줄 (사슬 기본값 · 쓰지 않는다) |
| venv | `~/dem-venv` — **두 기계 같은 자리 · 같은 판** (Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 · cupy 12.3.0 = 계획 `env_unit` 통과 · 11-17 현장 · 1저자 결정 = 패치 판까지 kgy 와 같은 것) | gabia 의 `~/rint-venv38` (3.8.20 · 같은 numpy · scipy · cupy) 은 쓰지 않고 손대지 않는다 (FAM 등록 `docs/reviews/fam_platen_prereg_20260812.md` 951 줄) · 두 기계 기본 `python3` = 3.13 (conda base · 11-17 현장) → venv 를 켜지 않고 사슬을 부르면 env_unit 대조에서 멈춘다 (틀린 결과 없음) · 저장본 열쇠에 venv 실경로가 든다 → R 동안 옮기지 않는다 |
| 킷 뿌리 `--root` | `~/sdcp` (`kit_SBE_vgcf100` · `kit_DBE_sdcp1um_vgcf100` · S0 단계 2 대조용 `kit_DBE`) | gabia 사본 = 11-11 복사 · 해시 같음 (시간 다시 어림 2 판 E-2 의 2) · 사슬이 R 직전 다시 해시해 S0 보고와 대조 |
| 계획 사본 | `~/sdcp/ca1_plan.json` | 봉인 커밋의 파일 바이트 그대로 |
| S0 보고 둘 | `~/sdcp/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json` (11-16 · kgy 원본 · 자리 = 그 런 `run.log` 15 줄 · `meta.txt` `out=`) · `~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json` (아래 (2b) · kgy) | 사다리를 도는 기계에 필요 (gabia = kgy 원본을 바이트 그대로) · 리포 사본 (`docs/data/rint2_s0_sbe_20261116/`) 은 홈 경로를 가린 사본이라 입력으로 쓰지 않는다 |
| S0 계획 | `~/dem-ca1/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json` | 봉인 커밋 안 (가림 없음 · sha256 `6346d9ed…`) |
| 저장본 | `~/ca1_cjstore` | **기계마다 새 빈 폴더** (1저자 11-17 봉인 후보 Q4) · 0755 · 실행 트리 · 원장 밖 · ⑥ 의 `~/p6_cjstore` · S0 시험 저장본 (`cjstore_s0probe_*`) 은 쓰지 않는다 |
| 원장 | `~/sdcp/ca1_ledger` (가진 기계) · `~/sdcp/ca1_ledger.parked` (세워 둔 쪽) | 한 번에 한 기계만 `ca1_ledger` 를 가진다 · 잠금 파일 = `~/sdcp/ca1_ledger/.git/rint_r_ledger.lock` (사슬과 같은 파일) |
| 넘김 묶음 | `~/sdcp/ca1_relay/<UTC 시각>_<보낸>_to_<받는>.bundle` | 지우지 않는다 (넘김 기록의 증거) |
| 사다리 바탕 | `~/sdcp/ca1_ladder_P0` (kgy) · `~/sdcp/ca1_ladder_P1` (gabia) | 1저자 11-17 봉인 후보 Q6 · 다른 기계 = 채택 시도 폴더를 같은 상대 자리로 바이트 그대로 · 판정 전 = 바탕 통째 |
| 단위 바탕 | `~/sdcp/ca1_units` (그 기계) · `~/sdcp/ca1_units_from_gabia` (kgy 가 받은 gabia 바탕 통째) | 재실행 = 원 시도가 돈 바탕에서만 |
| 넘침 점 바탕 | `~/sdcp/ca1_points` · `~/sdcp/ca1_points_from_gabia` | 넘침이 있을 때만 |
| 합친 예측 | `~/sdcp/ca1_predict` (첫 합치기 · 넘침 없으면 이것이 예측) · `~/sdcp/ca1_predict_x` (넘침 뒤 끝 합치기) | kgy (봉인 후보 Q6 · 이름 = 봉인 밖) · 판정 · 다시 판정이 끝날 때까지 지우지 않는다 |
| 판정 | `~/sdcp/ca1_verdict_main` | kgy |
| 로그 | `~/sdcp/ca1_logs/` | nohup 출력 (실행 트리 밖) |

### (2) 두 기계 준비 (R 전 · 봉인 직전 현장 확인과 같은 셸)

```sh
umask 022 && test "$(umask)" = 0022 && echo UMASK_OK
# 실행 트리 = 봉인 커밋 (Rint 고정 가지 위 문서 커밋 · stoic 아님) · 새 작업 트리 · 얕은 저장소 아님
#   <기존 트리> = 그 기계의 기존 리포 체크아웃 (kgy <HOME>/dem-s0-64e4d213e 꼴 · gabia <HOME>/dem-siteq-db86ce9b9 꼴 · 그 트리는 바꾸지 않는다 · 그 origin 이 봉인 가지를 받아야)
git -C <기존 트리> fetch -q origin <봉인 가지>
git -C <기존 트리> worktree add --detach ~/dem-ca1 <봉인 커밋>
git -C ~/dem-ca1 rev-parse HEAD                                    # = <봉인 커밋>
git -C ~/dem-ca1 log --diff-filter=A --format=%H -- <봉인본>       # = 위와 같은 sha (봉인본을 넣은 커밋)
git -C ~/dem-ca1 rev-parse --is-shallow-repository                 # false
git -C ~/dem-ca1 status --porcelain --untracked-files=normal       # 빈 줄 (사슬과 같은 기준)
~/dem-venv/bin/python -c 'import sys,numpy,scipy,cupy;print(sys.version.split()[0],numpy.__version__,scipy.__version__,cupy.__version__)'   # 3.8.10 1.24.4 1.10.1 12.3.0 (두 기계 같은 한 줄 · 같은 답)
. ~/dem-venv/bin/activate && unset SIGMA_VGCF_OVERRIDE
command -v python3                                                 # = ~/dem-venv/bin/python3 (켠 뒤 · conda base 3.13 이 아니다)
# 계획 사본 · 봉인본 · 숫자 블록 대조
cp ~/dem-ca1/docs/data/rint2_r_plan_<봉인 날짜>/ca1_plan.json ~/sdcp/ca1_plan.json
sha256sum ~/sdcp/ca1_plan.json ~/dem-ca1/<봉인본>                  # 첫 줄 = 봉인본 '| 계획 해시 |' 줄 끝 칸 · 둘째 = 봉인 기록의 봉인본 sha256
grep -n '^| 계획 해시 |\|^| S0 계획 해시 |' ~/dem-ca1/<봉인본> | grep -o '`[0-9a-f]\{64\}`'   # 두 줄 (계획 · S0 계획)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage plan-doc --plan ~/sdcp/ca1_plan.json --check-doc --registration ~/dem-ca1/<봉인본>   # PLAN_DOC_SAME (rc 0)
# 저장본 폴더 (기계마다 하나 · 새 빈 폴더) · 글자 · 모드 · 소유자 = 사슬 규칙으로 확인
( umask 022 && mkdir ~/ca1_cjstore )
chmod go-w ~/ca1_cjstore && ls -ld ~/ca1_cjstore                    # drwxr-xr-x · 소유자 = 이 사용자
printf '%s\n' ~/ca1_cjstore | LC_ALL=C grep -n '[^A-Za-z0-9._/-]' && echo '허용 밖 글자 — 1저자 (자리를 바꾼다)'
python3 -c 'import sys; sys.path.insert(0, sys.argv[1]); import rint_r_chain as R; print(R.cjunc_store_dir_problem(sys.argv[2]) or "STORE_DIR_OK")' ~/dem-ca1/scripts ~/ca1_cjstore
( umask 022 && mkdir -p ~/sdcp/ca1_relay ~/sdcp/ca1_logs )
command -v flock || echo 'flock 없음 — 이 기계의 넘김 = (5) 의 flock 없는 기계 규칙'   # 11-17 현장 = 두 기계 다 있음 (util-linux 2.34 · 2.39.3)
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader   # 적어 둔다 (R 동안 같아야 · 자동 갱신 멈춤)
```

- `--registration` 을 빼면 (기본 = 원본 자리 · 봉인 전 판) `plan-doc --check-doc` = rc 3 `PLAN_DOC_MISMATCH` (블록 없음) · 사다리 · 예측 · 판정 = 등록 해시 줄 ⬜ 에서 멈춤 (사슬 `registration_plan_hash` = `PLAN_HASH_UNREGISTERED`) — 틀린 결과는 없고 멈출 뿐이다 (봉인 기록 증거 ④) · 그래서 아래 모든 사슬 줄에 붙인다.
- gabia 만 더: 킷 두 벌 sha256 = kgy 와 같음 (2 판 E-2 의 2 · R 직전 사슬이 다시 대조) · S0 보고 둘을 kgy 원본 바이트 그대로 같은 상대 자리에 (`sha256sum` 두 기계 같음) · 실행 트리 = 기존 트리 (`<HOME>/dem-siteq-*`) 의 저장소에서 새로 뗀다 (`dem-mt` 없음 · 11-17 현장) · venv = `~/dem-venv` (kgy 와 같은 판 · `~/rint-venv38` 은 손대지 않음).
- 11-17 현장 (1저자 읽기만 · 두 기계): `flock` 있음 · 홈 경로 글자 = `[A-Za-z0-9._/-]` 안 · `git bundle create --all` 묶음에 HEAD 실림 (kgy git 2.25.1 · gabia 2.43.0) · 디스크 여유 kgy 240 GB (916 GB 중) · gabia 192 GB (422 GB 중) = 저장본 (SBE 파일 1,340,095,705 B · DBE 파일 크기 [미확인]) 에 충분 · venv 확인 줄 = 두 기계 `3.8.10 1.24.4 1.10.1 12.3.0` · gabia GPU = RTX A6000 49 GB (드라이버 595.58.03 · R 동안 같아야).

### (2b) S0 단계 2 — kgy · 한 번 · 사다리 전 (봉인 계획의 결과 전 등록 넷이 채워져 있어야 관문이 연다 · DBE 분포를 여기서 처음 연다 · 보고 = 사다리 `--s0-stage2-report`)

```sh
cd ~/dem-ca1 && umask 022
# venv (S0 보고의 python · numpy · scipy 판 = 이 셸 · 사슬은 S0 보고의 판 글자를 대조하지 않는다 → 여기서 눈으로 · 다르면 멈추고 1저자)
. ~/dem-venv/bin/activate && python3 -c 'import sys,numpy,scipy;print(sys.version.split()[0],numpy.__version__,scipy.__version__)'   # 3.8.10 1.24.4 1.10.1
# census · registry 일곱 파일 = S0 단계 1 보고의 판 (같으면 SAME_VERSION_OK 뒤 단계 2 · 다르면 && 에서 멈춘다 · §2-3 손 확인과 같은 줄)
#   끝 rc 줄 (bash PIPESTATUS) = 단계 2 의 rc (SAME_VERSION_OK 가 없으면 = git diff 의 rc · 단계 2 를 돌리지 않았다)
H1=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['code']['git_head'])" docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json)
git diff --quiet "$H1" HEAD -- scripts/ca_s0_census.py scripts/carbon_junction.py scripts/ptfe_face_alpha.py scripts/step3_sigma.py \
    scripts/mpm_webapp_payload.py scripts/fibre_segment_raster.py scripts/sr01_stamp_compare.py && echo SAME_VERSION_OK && \
  python3 ~/dem-ca1/scripts/ca_s0_census.py --stage 2 --threshold-commit <봉인 커밋> \
    --plan-path docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json \
    --r-plan-path docs/data/rint2_r_plan_<봉인 날짜>/ca1_plan.json --r-doc <봉인본> \
    --kit ~/sdcp/kit_DBE_sdcp1um_vgcf100 --kit ~/sdcp/kit_DBE --out ~/sdcp/ca1_s0_dbe 2>&1 | tee ~/sdcp/ca1_logs/s0_stage2.log; echo "rc=${PIPESTATUS[0]}"
```

- 관문이 보는 것 (`ca_s0_census.verify_plan_commit` · 아니면 거부): 인자 커밋 = HEAD 의 조상 (같은 커밋 포함) · 그 커밋 `<봉인본>` 의 `| S0 계획 해시 |` 끝 칸 = S0 계획 sha256 · `| 계획 해시 |` 끝 칸 = R 계획 sha256 · R 계획 꼴 · 결과 전 등록 넷 · 실행 정책 값 넷 (null = 거부) · tol_ff · len_law 두 계획 대조.  보내 주세요: 화면 요약 · 보고 JSON 둘 (→ `docs/data/rint2_s0_dbe_<날짜>/`).

### (3) 원장 시작 — kgy · 한 번

```sh
cd ~/sdcp && umask 022
mkdir -p ~/sdcp/ca1_ledger && git -C ~/sdcp/ca1_ledger init -q
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --init --plan ~/sdcp/ca1_plan.json --registration ~/dem-ca1/<봉인본>
git -C ~/sdcp/ca1_ledger symbolic-ref --short HEAD                 # 원장 가지 → 아래 넘김 기록 머리에 한 번 적는다
```

### (4) 시도 하나 — 항목 → 띄움 → 시작 확인 (사다리 · 단위 · 넘침 점 모두 같은 꼴 · 원장이 그 기계에 있을 때만)

```sh
# 사다리 P0 (kgy) — 먼저 같은 인자 + --dry-run (--ledger · --attempt 없이 · 런 env 만 · 원장 · 폴더 무변경) → 항목 (화면 ATTEMPT_ADDED n=<n>) → 그 번호로 곧바로 본 시도
#   (항목만 두고 띄우지 않으면 안 된다 — 같은 대상의 다음 항목은 앞 항목의 결과 줄 뒤에만 · 폴더 없는 원장 시도 = 결과 뒤 · Q9 설계 §3-5 128 · 134 줄)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --plan ~/sdcp/ca1_plan.json --registration ~/dem-ca1/<봉인본> \
    --s0-plan ~/dem-ca1/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json \
    --s0-stage2-report ~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json \
    --s0-stage1-report ~/sdcp/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json \
    --max-hours 168 --machine kgy --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_ladder_P0 --dry-run
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target ladder:P0 --machine kgy \
    --plan ~/sdcp/ca1_plan.json --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --registration ~/dem-ca1/<봉인본>
cd ~/sdcp && nohup python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 \
    --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --plan ~/sdcp/ca1_plan.json --registration ~/dem-ca1/<봉인본> \
    --s0-plan ~/dem-ca1/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json \
    --s0-stage2-report ~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json \
    --s0-stage1-report ~/sdcp/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json \
    --max-hours 168 --machine kgy --ledger ~/sdcp/ca1_ledger --attempt <n> \
    --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_ladder_P0 > ~/sdcp/ca1_logs/ladder_P0_a<n>.log 2>&1 &
# 사다리 P1 (gabia) = 위 세 줄에서 ladder:P1 · --law P1 · --machine gabia · --out ~/sdcp/ca1_ladder_P1 · 로그 이름만 다르다

# 단위 (그 기계 · 이름 = 아래 (6) 표) — 두 사다리 채택 시도 폴더가 이 기계에 있어야 한다
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target unit:P0_c0_R_j0 --machine kgy \
    --plan ~/sdcp/ca1_plan.json --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --registration ~/dem-ca1/<봉인본>
cd ~/sdcp && nohup python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/<봉인본> --ledger ~/sdcp/ca1_ledger --attempt <n> --unit P0_c0_R_j0 \
    --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_units > ~/sdcp/ca1_logs/unit_P0_c0_R_j0_a<n>.log 2>&1 &
# gabia 단위 = 같은 두 줄 · --machine gabia · unit:<이름> · --unit <이름> (예 P1_c1_R_j_hi)

# 시작 확인 — 둘 다 참이면 그 사슬은 끝날 때까지 원장을 건드리지 않는다 → 원장을 넘겨도 된다
python3 -c 'import json, subprocess, sys; L = subprocess.run(["git", "-C", sys.argv[1], "show", "HEAD:rint_r_attempts.jsonl"], capture_output=True, text=True, check=True).stdout.splitlines(); x = json.loads(L[-1]); print(x.get("kind"), x.get("n"))' ~/sdcp/ca1_ledger   # start <n>
ls ~/sdcp/ca1_units/attempt_<n>/groups/ | grep -c 'launch.json$'   # 1 이상 (사다리면 ~/sdcp/ca1_ladder_<법칙>/attempt_<n>/groups/)
```

### (5) 원장 넘김 — 보낸 쪽 · 받는 쪽 (수단 = 1저자 · 묶음 파일만 옮긴다)

```sh
# 보낸 쪽 — (4) 의 시작 확인 뒤 (또는 그 기계에서 도는 사슬이 없을 때) · 원장 잠금 (사슬과 같은 잠금 파일 · 1저자 11-17 봉인 후보 Q5) 아래에서 묶고 세워 둔다
cd ~/sdcp && umask 022
T=$(date -u +%Y%m%dT%H%M%SZ); FROM=kgy; TO=gabia; B=~/sdcp/ca1_relay/${T}_${FROM}_to_${TO}.bundle
flock -x -w 120 ca1_ledger/.git/rint_r_ledger.lock -c "git -C ca1_ledger bundle create \"$B\" --all && mv ca1_ledger ca1_ledger.parked"
git -C ca1_ledger.parked rev-parse HEAD; sha256sum "$B"; echo "$T"      # 넘김 기록 한 줄 (시각 · 원장 끝 커밋 · 묶음 sha256)
test ! -e ca1_ledger && echo PARKED_OK
# 받는 쪽 — 묶음을 ~/sdcp/ca1_relay/ 에 같은 이름으로 둔 뒤 (T · FROM · TO · 가지 = 넘김 기록)
cd ~/sdcp && umask 022
T=<넘김 기록 시각>; FROM=kgy; TO=gabia; BR=<원장 가지>; RB=~/sdcp/ca1_relay/${T}_${FROM}_to_${TO}.bundle
sha256sum "$RB"                                                     # = 넘김 기록
git bundle list-heads "$RB" | grep "refs/heads/$BR"                 # 커밋 = 넘김 기록의 원장 끝 커밋
# 세워 둔 사본이 있으면 그 자리에서 먼저 받고 (그동안 이 기계 사슬은 원장 자리 ca1_ledger 를 못 연다 = 창 없음) 받은 뒤에만 되살린다 ·
#   -c pull.rebase=false = 사용자 설정을 이 줄에서만 끈다 ([추정] 옛 git 에서 rebase 설정이 --ff-only 보다 앞설 수 있다)
if [ -d ca1_ledger.parked ]; then git -C ca1_ledger.parked -c pull.rebase=false pull -q --ff-only "$RB" "$BR" && mv ca1_ledger.parked ca1_ledger; else git clone -q -b "$BR" "$RB" ca1_ledger; fi
test "$(git -C ca1_ledger rev-parse HEAD)" = <넘김 기록의 원장 끝 커밋> && echo RECV_OK   # RECV_OK 가 없으면 멈추고 1저자 (사슬을 띄우지 않는다)
```

- (11-17 현장 = 두 기계 다 `flock` 있음 → 아래 줄은 한정으로만 남긴다) **`flock` 이 없는 기계** ((2) 의 확인 줄) = 위 보낸 쪽 셋째 줄을 `git -C ca1_ledger bundle create "$B" --all && mv ca1_ledger ca1_ledger.parked` 로 (잠금 없이) 쓰되, **그 기계의 사슬이 (4) 의 시작 확인 뒤 도는 중일 때만 넘긴다** (1저자 11-17 봉인 후보 Q5 · 그 밖의 때 = 그 기계의 사슬이 시작 기록 · 결과 줄을 쓸 수 있는 때).
- 잠금 파일 = 사슬과 같은 파일 (`rint_r_chain.LEDGER_LOCK_FILE` · 원장 저장소 `.git` 안 · 대기 상한 120 s = 사슬 `LEDGER_LOCK_WAIT_S` 와 같은 값) — 같은 호스트에서 사슬의 덧붙임과 묶기 · 이름 바꾸기가 겹치지 않는다 · 세워 둔 뒤 그 기계에서 끝나는 사슬은 잠금 파일을 못 열어 rc 3 (아래 (6) 정상 끝).

**넘김 기록** (넘길 때마다 한 줄 · 원장 가지 = `<원장 가지>` (`--init` 뒤 한 번))

| 시각 (UTC · 묶음 이름) | 보낸 기계 | 받는 기계 | 원장 끝 커밋 | 묶음 sha256 | 잠금 (flock · 없음 = 시작 확인 뒤 도는 중) | 누가 |
|---|---|---|---|---|---|---|
| (빈칸 — R 때) | | | | | | |

### (6) (가-2) 정상 흐름 — 차례 · 각 단계에서 원장이 어디 있어야 하나

| # | 기계 | 그 일 전 원장 자리 | 할 일 | 정상 끝 |
|---|---|---|---|---|
| 0 | kgy | — | (2b) S0 단계 2 | rc 0 · 보고 JSON 둘 |
| 1 | kgy | kgy (시작) | (3) 원장 시작 | rc 0 · 원장 머리 = 계획 sha256 |
| 2 | kgy | kgy | (4) `ladder:P0` 항목 → 사다리 P0 → 시작 확인 | 시작 기록 · 러너 그룹 |
| 3 | kgy → gabia | kgy | (5) 넘김 | gabia 가 원장을 가진다 · kgy = 세워 둠 |
| 4 | gabia | gabia | (4) `ladder:P1` 항목 → 사다리 P1 → 시작 확인 | 시작 기록 · 러너 그룹 |
| 5 | (두 사다리 도는 중) | gabia | 먼저 끝난 기계가 원장을 받는다 — 원장이 없는 동안 끝난 사슬 = 아래 rc 3 (정상) | — |
| 6 | 끝난 기계 | 그 기계 | `--stage recover --out <그 시도 폴더> --ledger ~/sdcp/ca1_ledger --registration ~/dem-ca1/<봉인본>` | rc 0 · 결과 줄 (by recover) |
| 7 | 두 기계 | — | 사다리 채택 시도 폴더를 서로 옮김 (P0 → gabia · P1 → kgy · 같은 상대 자리 · 바이트 그대로 · `sha256sum` 이나 폴더 요약을 맞춘다) | 두 기계에 두 사다리 채택 폴더 |
| 8 | 단위 시작마다 그 기계 | 그 기계 | (4) `unit:<이름>` 항목 → 단위 → 시작 확인 → 다른 기계가 기다리면 (5) 넘김 | 단위가 끝날 때 원장이 그 기계에 있으면 사슬이 결과 줄 (rc 0) · 없으면 rc 3 → 원장이 돌아온 뒤 6 번 |
| 9 | 원장을 받는 차례 | — | 단위가 끝난 기계 (recover + 다음 단위) 가 먼저 · 도는 중인 기계는 원장이 없어도 된다 · 같은 기계에서 사슬 둘을 띄우지 않는다 | — |
| 10 | gabia → kgy | — | 단위 12 의 결과 줄이 다 있으면 gabia `~/sdcp/ca1_units` 바탕 통째 → kgy `~/sdcp/ca1_units_from_gabia` · 원장 → kgy · 사다리 P1 바탕 통째 → kgy | kgy 에 원장 · 모든 시도 폴더 |
| 11 | kgy | kgy | (7) 첫 합치기 | rc 0 = 예측 (PREDICTED · NOT_COMPUTED · STOPPED = 그 결과) · rc 4 = 넘침 (`expansion.json`) |
| 12 | (rc 4) 점마다 그 기계 | 그 기계 | 넘침 점 배정 안전 규칙 (아래) → `point:<이름>` 항목 → 점 시도 (gabia 면 `expansion.json` 을 바이트 그대로) → 다 끝나면 gabia `ca1_points` 통째 → kgy `ca1_points_from_gabia` → 끝 합치기 | rc 0 |
| 13 | kgy | kgy | (7) 주 판정 · 다시 판정 | 판정 rc 0 · `REVERIFY_SAME` |

- **rc 3 = 정상 끝** 은 셋이 다 맞을 때만 — ① 화면 끝 줄 `멈춤 [ATTEMPT_LEDGER_MISMATCH] … 원장 잠금 파일을 못 연다 (…)` ② 그 시각 그 기계에 `~/sdcp/ca1_ledger` 가 없다 (세워 둠 · `ca1_ledger.parked` 만) ③ 그 시도 폴더에 단계 요약 (`ladder_summary.json` · `unit_summary.json` · `point_summary.json`) 이 있다.  하나라도 아니면 진짜 멈춤 — 요약 · 로그의 멈춤 이름을 1저자에게 · 그 대상의 다음 시도를 띄우지 않는다.
- recover 는 그 시도가 돈 기계 · 그 바탕 · 같은 부팅에서 (옮긴 폴더에서 = rc 3 · 원장 무변경) · 사슬이 아직 살아 있으면 recover 는 아무것도 하지 않는다 (rc 3 · 끝난 뒤 다시) · 다른 부팅이면 그 그룹이 끝났음을 확인한 뒤 `--operator-confirm <시도 번호> --operator-why "<확인한 것 · 한 줄>"` (§3 끝 줄 · 등록 R §10-5 아 ④).
- 단위 ↔ 기계 **첫 배정** (봉인 밖 · 1저자 11-17 봉인 후보 Q6 · 3 판 Q7 · gabia 첫 사다리 팔 실측으로 고칠 수 있다 · 배정을 바꿔도 원장 · 폴더 · 규칙이 시도를 정한다):

| 기계 | 단위 (이 차례로) |
|---|---|
| kgy (7) | `P0_c0_R_j0` · `P0_c0_R_j_lo` · `P0_c0_R_j_hi` · `P0_c1_R_j0` · `P0_c1_R_j_lo` · `P0_c1_R_j_hi` · `P1_c0_R_j0` |
| gabia (5) | `P1_c0_R_j_lo` · `P1_c0_R_j_hi` · `P1_c1_R_j0` · `P1_c1_R_j_lo` · `P1_c1_R_j_hi` |

- **넘침 점 배정 안전 규칙** (3 판 Q11 · 운영 규칙 · 기준 값 2/3 은 바꿀 수 있다): 점을 주기 전에 그 기계의 첫 DBE 모서리 팔 실측 비로 그 기계의 첫 점 (8 팔 · 짓기 5) 시간을 다시 어림해 **112 h (= 168 h 의 2/3)** 를 넘으면 그 기계에 주지 않는다 · 둘 다 넘으면 멈추고 1저자 · 점은 kgy 먼저.
  - **어림 꼴 = 시간 다시 어림 3 판 §3-3 (4) 의 "팔 전체" 꼴** (1저자 11-17 봉인 후보 Q7 · 보수 쪽): 첫 점 ≈ r × (8 × T_hit + 5 × (T_first − T_hit)) · r = T_DBE ÷ T_first · T_DBE = 그 기계 첫 단위의 모서리 런 · T_first = 그 기계 사다리에서 저장본을 지은 첫 보통 점 런 · T_hit = 그 사다리의 적중 런 · 시간 = 런 기록 `seconds` (아래 줄 · 이름 · 역할 · 시간만 · σ 를 열지 않는다).  확인: 3 판 값 (kgy T_hit 4,932 · T_first 9,067 · gabia 6,682 · 10,817 s · r 2.933) 을 넣으면 kgy 49.0 h · gabia 60.4 h (3 판 §3-3 (4) 와 같음).
  - 모서리 런에 SV 반사실 풀이가 들면 (`sv_cf_scope`) r 이 커진다 = 보수 쪽.

```sh
python3 -c 'import json, sys; s = json.load(open(sys.argv[1])); [print(r.get("name"), r.get("role"), r.get("arms"), r.get("seconds")) for r in s.get("runs") or []]' ~/sdcp/ca1_units/attempt_<n>/unit_summary.json
python3 -c 'import json, sys; s = json.load(open(sys.argv[1])); [print(r.get("name"), r.get("role"), r.get("arms"), r.get("seconds")) for r in s.get("runs") or []]' ~/sdcp/ca1_ladder_P0/attempt_<n>/ladder_summary.json
python3 -c 'import sys; th, tf, td = map(float, sys.argv[1:4]); r = td / tf; print(round(r, 3), round(r * (8 * th + 5 * (tf - th)) / 3600, 1), "h (112 h 넘으면 그 기계에 주지 않는다)")' <T_hit> <T_first> <T_DBE>
```

### (7) 합치기 · 넘침 점 · 판정 — kgy (넘침 점 시도만 배정된 기계)

```sh
cd ~/sdcp && umask 022
# 첫 합치기 (rc 0 = 예측 · rc 4 = 넘침 · 그 밖 = 멈춤 이름을 1저자에게)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/<봉인본> --ledger ~/sdcp/ca1_ledger --merge ~/sdcp/ca1_units ~/sdcp/ca1_units_from_gabia --out ~/sdcp/ca1_predict
python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["points"])' ~/sdcp/ca1_predict/expansion.json   # rc 4 일 때만 · 넘침 점 이름
# 넘침 점 (점마다 · 그 기계) — 항목 → 시도
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target point:P0_c0_R_j0 --machine kgy \
    --plan ~/sdcp/ca1_plan.json --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --registration ~/dem-ca1/<봉인본>
cd ~/sdcp && nohup python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/<봉인본> --ledger ~/sdcp/ca1_ledger --attempt <n> --point P0_c0_R_j0 \
    --expand ~/sdcp/ca1_predict/expansion.json --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_points > ~/sdcp/ca1_logs/point_P0_c0_R_j0_a<n>.log 2>&1 &
# 끝 합치기 (넘침 점이 다 끝난 뒤 · gabia 점 바탕 통째를 받은 뒤 · 없으면 그 자리를 뺀다)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/<봉인본> --ledger ~/sdcp/ca1_ledger \
    --merge ~/sdcp/ca1_units ~/sdcp/ca1_units_from_gabia ~/sdcp/ca1_points ~/sdcp/ca1_points_from_gabia \
    --expand ~/sdcp/ca1_predict/expansion.json --out ~/sdcp/ca1_predict_x
# 주 판정 (값 열람 = 주 판정 런이 다 끝난 뒤 한 번 · --show-results 를 이 줄에) · 다시 판정 (읽기 전용 바이트 대조 · 판정 JSON 에 적힌 등록 경로를 다시 읽는다)
#   --runs 의 셋째 = 넘침 없음 ~/sdcp/ca1_predict · 넘침 ~/sdcp/ca1_predict_x
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --runs ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> \
    ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> ~/sdcp/ca1_predict --root ~/sdcp --registration ~/dem-ca1/<봉인본> \
    --ledger ~/sdcp/ca1_ledger --out ~/sdcp/ca1_verdict_main
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --reverify ~/sdcp/ca1_verdict_main --root ~/sdcp --registration ~/dem-ca1/<봉인본>
# 원장이 없는 동안 끝난 시도 → 원장이 돌아온 뒤 (그 기계 · 그 바탕)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage recover --out ~/sdcp/ca1_units/attempt_<n> --ledger ~/sdcp/ca1_ledger --registration ~/dem-ca1/<봉인본>
```

### (8) R 동안 운영 규칙 (정본 = 봉인본 §10-8 · 규칙 · 기계적 보장 아님 표지 그대로)

1. 실행 트리 · 봉인본 (원본 자리 포함) · 계획 사본 · 저장본 폴더 · venv = R (사다리 시작부터 다시 판정까지) 동안 바꾸지 않는다 — `git -C ~/dem-ca1 rev-parse HEAD` = `<봉인 커밋>` · `status --porcelain --untracked-files=normal` 빈 줄을 시도마다 본다.
2. 두 기계 GPU 드라이버 · CUDA 자동 갱신 멈춤 (재실행 자격 = 원 시도 환경 지문 모든 칸) · (2) 의 `nvidia-smi` 줄 값이 R 동안 같아야 한다 (방법 = 1저자 · 기계마다).
3. GPU 비움 — 두 기계 GPU 에 다른 계산 없음 (kgy = 1저자 DFT 얼림) · 같은 기계에서 사슬 둘을 동시에 띄우지 않는다.
4. 저장본 폴더 = 손대지 않음 (못 읽는 파일 `unreadable_rebuilt` = 기록 · 시간만 는다 · R 뒤 정리 · 어긋남 = 멈춤 → 1저자).
5. 재실행 = 원 시도가 돈 그 `--out` 바탕에서만 (틀린 바탕에서 시도하지 않는다 — 한 번 거부되면 원 바탕의 재실행도 거부된다) · 멈춘 GPU 런은 `--resume` 하지 않고 새 시도.
6. 원장 밖 킷 풀이 없음 · 원장 · 시도 폴더 · 넘김 묶음을 손으로 고치거나 지우지 않는다.
7. 띄우기 = `cd ~/sdcp && nohup … > ~/sdcp/ca1_logs/<이름>.log 2>&1 &` (실행 트리 밖 · `nohup.out` 을 실행 트리에 만들지 않는다).
8. 최대 시도 수 8 (같은 대상 · 풀기 전 거부 · 재실행 포함) — 넘으면 `ATTEMPT_LIMIT` · 그 대상 = 1저자.
9. `--add` 로 받은 번호 = 곧바로 그 번호의 시도를 띄운다 (항목만 두고 같은 대상 항목을 더하지 않는다 · 사다리는 dry-run 을 `--add` 앞에) — 폴더 없는 원장 시도 = 결과 뒤 (Q9 설계 §3-5 134 줄).
10. 사슬 명령에서 `--registration ~/dem-ca1/<봉인본>` 을 빼지 않는다 (빼면 원본 자리 = 봉인 전 판 → 해시 줄 ⬜ → 멈춤 · 틀린 결과는 없다).

====

## K-04 · §5 기록 머리 (넘김 기록의 자리 알림)

@op after 590 ## 5. 기록 (빈칸 · 결과 0 건)

====

- (봉인 · <봉인 날짜>) R 의 원장 넘김 기록 = §3-1b (5) 의 표 (넘길 때마다 한 줄 · 이 문서 · 3 판 Q9) · 시도 결과 = 원장 (`~/sdcp/ca1_ledger`) 이 정본 (이 문서에 옮겨 적지 않는다) · 등록 = 봉인본 `<봉인본>`.
====
