# REIL C4-E · E1 실행 승인 요청 — 원자료 반입 · E3a 66 호출 · 독립 사전 대조 · 2026-10-15 KST

> **승인 요청문이다 (실행 0).** 사용자 결정 전에는 launcher 복사 · 시험 · 읽기 경로 확보 · 자료 반입 · 개봉 · 실행을 하지 않는다.
> 근거:
> - 상태 문서 §72 — E0 한정 정정 결과 검토 회신 (`reviews/review_reil_c4e_e0_fix_20261015/originals/`): N1 한정 해소 · **E1 승인 요청서 작성 허용 ·
>   실행 승인 아님** · 요청서에 고정할 것 1–5.
> - v3 요청 (`docs/REIL_C4E_APPROVAL_REQUEST_v3_20261014.md` — 수용 §65) 의 §3 (run 순서) · §4 (E1 규칙) · §7 (E1 순서).
> - §71 — 신뢰 소스 목록 `SOURCES.json` 봉인.
>
> **E0 승인 (§66) 과 E0 한정 정정 승인 (§70) 은 E1 로 전용하지 않는다.** E1 의 승인 대상은 이 요청 하나다.
> 순서: 이 요청 → (사전 검토 — §10 의 2) → 사용자 E1 별도 승인 → E1 → 결과 검토. "[산술]" 은 우리 계산이고 보증이 아니다.

## 0. 요약

| 단계 | 내용 | 자료 · 네트워크 · 계산 |
|---|---|---|
| **E1-0** | launcher (독립 사전 대조 · stdlib · 실행 모듈 밖) 와 그 대조 14 — 골격으로 RED → 고정 구현으로 GREEN (E0 21 + N1 6 + 새 14) | 자료 · 네트워크 · optimizer 0 |
| **E1-1** | identity — launcher 경유 | 계산 없음 |
| **E1-2** | 읽기 경로 확보 (`add_repo` · read) → fetch — launcher 경유 · 고정 커밋의 두 경로 | github.com fetch 1 회 |
| **E1-3** | run 1 회 (66 호출) — launcher 경유 · 분리 실행 · 중간 개입 0 | 자료 개봉 · 그들 GA / NSGA |
| **E1-4** | 끝 기록 · 비밀 검사 · 커밋 · 결과 기록 · 결과 검토 발송문 → 멈춤 | — |

## 1. 고정 식별 (§72 조건 1)

- **실행 모듈 다섯 = 구현 커밋 `61b9037e5283419f9ee22129b9a851df06f20cb1` 의 바이트** (검토 HEAD `322a0e53` 에서도 같음 · §72).
- **신뢰 소스 목록:** `bms-balancing/evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json` · 1,100 B ·
  **sha256 `2a7b2b49b9809d1a9301398388894a1f7a73afb55acc1a5070e3f77ce0393d52`**.

  | 경로 (bms-balancing 기준) | bytes | sha256 |
  |---|---:|---|
  | `scripts/reil_c4e_run.py` | 53,853 | `a94f535fd8ab5718b0ed47e0322a067300f808ef42c530cd95668aa77f0a53a9` |
  | `scripts/reil_c4_e3a.py` | 32,311 | `33b855378fb76634eb314f8cfb0428151ce1ec8b9045bc8447d8e17354a41ac3` |
  | `scripts/reil_c4_monitor.py` | 21,546 | `e6ef8ff617342393a9d3a45c98751b563a3f1e9871c6fa3b540b47f4bfbc071b` |
  | `scripts/reil_c5_pilot.py` | 47,164 | `73bee8dc412b39863afb64b70bc128cbecee2075a3a17914fc7288f353ef11a6` |
  | `scripts/reil_p0.py` | 23,941 | `793b326ebf86a6db3b855d828aff4d6b6dddc824bed8d00f4161537b1cc06e3a` |

- **실행 경로 · cwd:** cwd = `/home/user/Yonghoon-DEM-DFT/bms-balancing`. run 자식의 스크립트 = `/home/user/Yonghoon-DEM-DFT/bms-balancing/scripts/reil_c4e_run.py`.
  나머지 넷은 run 이 자기 위치에서 bms-balancing 을 sys.path[0] 에 넣고 `scripts.` 로 import 한다 (run `:43–52`).
- **이번에 고정하는 초안 (정적 검사만 · 실행 0):**

  | 초안 | sha256 | bytes | E1 에서 복사할 곳 |
  |---|---|---:|---|
  | `docs/REIL_C4E1_LAUNCHER_DRAFT_20261015.py.txt` (launcher 고정 구현) | `c5bc40a474372e282706ad9069405fbb8bd9238ca26908478056bca2c20f30ff` | 27,507 | `scripts/reil_c4e1_launch.py` (GREEN 직전) |
  | `docs/REIL_C4E1_LAUNCHER_SKELETON_DRAFT_20261015.py.txt` (RED 골격) | `d202a716b652ffcbcd12250474ee80b67000b7355542882d53cd431593a4b458` | 7,989 | 같은 곳 (RED 때) |
  | `docs/REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_20261015.py.txt` (대조 14) | `0b06905a289b78ba788faa859acb433448465b0eba073dee22c87e7bf4b2fca4` | 24,637 | `tests/test_reil_c4e1_launch.py` |

  골격은 초안에서 정적 변환으로 만들었다 — import · 상수 부분이 고정 구현과 문자 그대로 같고 (대조함), 함수 26 개는 서명 + `NotImplementedError` 다.
- **identity helper:** `00_identity_c4.py` · sha256 `92bb3bca2dcd56982bd4d4ddc02bb8ed84615d5b1b6af6385d69b66c8f5df900` (E0 · N1 정정 증거와 같은 바이트) →
  E1 증거 폴더에 복사 (launcher 가 sha 를 고정값으로 대조).
- **E1-0 의 RED · GREEN 단계 실행기:** N1 정정의 `evidence/reil_c4e0_fix_20261014/00_step_runner.py` (`45a055b1…`) 사본 — docstring 첫 줄 · 증거 경로 ·
  scratch 하위 폴더 (`c4e1_steps`) 만 바꾼다 (끝 기록에 diff 와 sha 를 남긴다). launcher 단계 (E1-1 · 2 · 3) 에는 쓰지 않는다.
- **자료 (P0 고정 · §20 · v3 §1):** 출처 `REIL-UConn/Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics` @ `1188c371e5836df4a7e5f5acf336a34ffd4027e6` ·
  `LFP_Data.xlsx` 10,841,377 B `fd50e09542be7adb2270963d65a6e7b5ccae1473a512f68462c2dd419d620ee1` · `util_LFP.py` 33,754 B
  `3c19e45ef8a64ce67cda1f623551e758d4c0f67086bbae02b978428d78de1c76` (원본 · v3 §11-3).
- **그 밖:** P0 결과 `3875e650…` · 노트북 발췌 `95cca5f3…` · 봉인 `reil_c6_rebuild_20261013/MANIFEST.json` `4f120948…` · venv
  `SP/reil_c4env/venv` (python 3.11.17 · `include-system-site-packages = false`) · launcher 해석기 `/usr/bin/python3.11 -I` (stdlib 만).
  SP = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad`.
- **바뀌면:** 다섯 모듈 · 목록 → 다시 봉인 · 검토 · 승인 (§72). launcher · 골격 · 대조 초안 · helper → 이 요청을 고쳐 다시 승인.

## 2. 독립 사전 대조 — launcher (§72 조건 2)

### 2-1. 왜 run 밖에서 하는가

run 은 `:43–52` 에서 e3a · monitor · c5 (→ p0) 를 import 한 **뒤에야** `prepare` 의 내부 대조 (`:562–`) 를 한다. 내부 검사가 util 적재 전이라는 사실은
실행 모듈 import 전 보호가 아니다 (§72 한정 2). fetch 자식도 같은 run 모듈을, identity helper 는 c5 (→ p0) 를 import 한다. 그래서 launcher 가 **세
자식 (identity · fetch · run) 모두 앞에서** 대조하고, 통과할 때만 자식을 띄운다. launcher 는 stdlib 만 쓰고 다섯 모듈을 import 하지 않는다 (대조 l14 가
AST 로 확인).

### 2-2. 사전 대조 항목 (자식 시작 전 · 하나라도 어긋나면 자식 0)

| 항목 | 기준 | 근거 함수 |
|---|---|---|
| 목록 | 일반 파일 · 바이트 sha256 = `2a7b2b49…` · JSON · schema `reil-c4e-sources-v1` · 경로 정확히 다섯 · 항목 (sha256 소문자 16 진 64 · bytes 정수 ≥ 0 · bool 거부) | `load_sources` |
| 다섯 모듈 | 일반 파일 (심볼릭 링크 거부) · `resolve()` = 대조 경로 (링크된 상위 폴더 거부) · bytes · sha256 = 목록 | `read_regular` · `check_files` |
| 실행 스크립트 | fetch · run: argv 의 스크립트 = 대조한 run 모듈 경로 · identity: 증거 폴더의 helper · sha = `92bb3bca…` | `precheck` |
| 해석기 · 플래그 | argv 머리 = `<venv>/bin/python -I -B -X pycache_prefix=<새 빈 폴더>` | `interp` · `precheck` |
| 탐침 | 같은 해석기 · 플래그 · env · cwd 로 `-c` 탐침 (json · sys 만) → isolated · ignore_environment · no_user_site · safe_path · dont_write_bytecode · pycache_prefix · executable = 고정값 | `probe` · `flag_problems` |
| 섀도 | 탐침이 본 sys.path 의 어느 항목 (폴더 · zip) 에도 `scripts` 정규 패키지 · 모듈 (소스 · 바이트코드 · 확장) 없음 · bms-balancing 에 `scripts/__init__*` · `scripts.*` 모듈 파일 없음 | `shadow_problems` |
| 자료 | run: `SP/c4e1/data` 의 두 파일 = 고정 sha · bytes · fetch: 자료 폴더가 아직 없음 | `check_files` · `precheck` |

사전 대조가 띄우는 프로세스는 탐침 하나뿐이다 (우리 모듈 import 0). 실패하면 `<단계>.precheck.json` · `<단계>.meta.json` (launched false · stage false) 을
쓰고 rc 1 로 끝난다 — stdout / stderr 로그는 만들지 않는다 (대조 l9).

### 2-3. 실제 실행 · 적재 경로 ↔ 대조 경로의 연결

1. 자식 argv 의 실행 스크립트는 launcher 가 해시한 절대 경로와 같은 상수에서 만든다 (`build_argv`) · 사전 대조가 같음을 다시 확인한다.
2. 승인 바이트의 run 모듈은 자기 경로에서 bms-balancing 을 sys.path[0] 에 넣고 `scripts.` 로 넷을 import 한다 (`:43–52`).
3. `bms-balancing/scripts/` 는 `__init__` 없는 네임스페이스다. 자식 sys.path 의 다른 항목에 `scripts` 정규 패키지 · 모듈이 있으면 그쪽이 먼저 잡히므로,
   탐침으로 없음을 확인한다 (지금 venv sys.path 의 stdlib · lib-dynload · site-packages 에 없음 — 정적 확인).
4. 자식은 `-B -X pycache_prefix=<새 빈 폴더>` 로 띄운다. 소스 트리의 `__pycache__` 를 읽지도 쓰지도 않으므로 적재되는 코드는 대조한 소스 바이트다
   (지금 `scripts/__pycache__/` 에 이전 `-I` 실행들 — C4-ENV · C4-0 계열 · E0 plan-e — 이 남긴 바이트코드 7 개가 있다 (2026-10-13 · 14). 지우지 않고,
   읽히지 않게 한다). 끝난 뒤 새 pycache 폴더가 비어 있어야 한다.
5. **사후 결속:** run 의 `IDENTITY.json` 시작 · 끝 표에서 모듈 다섯 행의 `path` (run 이 import 한 모듈의 `__file__` 로 적은 실제 적재 경로) · sha256 · bytes
   = launcher 의 대조 경로 · 목록 (`identity_link`).

### 2-4. 자식 · 프로세스 그룹 · 사후 대조

- 자식은 새 세션 (프로세스 그룹) 으로 띄운다. timeout 이면 그룹 전체를 SIGKILL 한다. 끝난 뒤 5 s 안에 그룹에 살아 있는 (좀비 아닌) 구성원이 남으면
  정리하고 사후 대조 실패로 둔다 (`run_child` · `alive_after` — /proc 의 pgid · 상태).
- **사후 대조:** 다섯 모듈 재해시 · (fetch · run) 자료 두 파일 재해시 (launcher 가 직접) · (run) `IDENTITY.json` 결속 · pycache 폴더 파일 0 · 그룹 잔존 0.
- 기록 (모두 `<단계>.` 접두 · 덮어쓰기 거부): `precheck.json` (자식 전) · `stdout.log` · `stderr.log` · `porcelain_start.txt` · `porcelain_end.txt` ·
  `meta.json` (argv · cwd · env 이름 · 자식 rc · timeout · 경과 · 그룹 · 사후 대조 · 단계 판정 · launcher 자신의 sha · HEAD · 디스크 · 최대 자식 RSS) ·
  `launcher.log` (launcher 의 한 줄 요약 — 셸 재지정).

## 3. 고정 명령 · env · cwd (§72 조건 1 · 4)

### 3-1. launcher 호출 (E1-1 · 2 · 3)

```
<L> = /usr/bin/python3.11 -I /home/user/Yonghoon-DEM-DFT/bms-balancing/scripts/reil_c4e1_launch.py
<E> = /home/user/Yonghoon-DEM-DFT/bms-balancing/evidence/reil_c4e1_<착수 UTC 날짜 YYYYMMDD>      (미리 만든 폴더 · 이름 규칙은 launcher 가 확인)
§NN = 사용자 E1 승인 기록 절

<L> identity --evidence <E> --approval-section §NN > <E>/03_identity.launcher.log 2>&1
<L> fetch    --evidence <E> --approval-section §NN > <E>/04_fetch.launcher.log 2>&1
setsid nohup <L> run --evidence <E> --approval-section §NN > <E>/05_run.launcher.log 2>&1 < /dev/null &
```

run 은 분리 실행한다 — 세션 도구의 실행 시간 한도와 무관하게 launcher 가 자식의 끝 (또는 10,800 s timeout) 까지 기다린다. 진행 관측은 읽기만 (프로세스 ·
파일 크기) 이고 중간 개입 · 실행 중 커밋은 0 이다.

### 3-2. 자식 argv (launcher `build_argv` — 대조 l14 가 문자 그대로 고정)

```
<P> = SP/reil_c4env/venv/bin/python -I -B -X pycache_prefix=SP/c4e1/pycache/<단계 이름>

identity: <P> <E>/00_identity_c4.py SP/reil_c4env/venv <BMS>/reil_c6_rebuild_20261013
              4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc <E>/03_identity.json
fetch:    <P> <BMS>/scripts/reil_c4e_run.py fetch --dest SP/c4e1/data
run:      <P> <BMS>/scripts/reil_c4e_run.py run --venv SP/reil_c4env/venv --seal <BMS>/reil_c6_rebuild_20261013
              --seal-manifest-sha256 4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc
              --xlsx SP/c4e1/data/LFP_Data.xlsx --util SP/c4e1/data/util_LFP.py
              --sources <BMS>/evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json
              --sources-sha256 2a7b2b49b9809d1a9301398388894a1f7a73afb55acc1a5070e3f77ce0393d52
              --out <E>/run --approval "상태 문서 §NN (사용자 E1 승인 · docs/REIL_C4E_E1_APPROVAL_REQUEST_20261015.md)"
```

(`<BMS>` = `/home/user/Yonghoon-DEM-DFT/bms-balancing` · 단계 이름 = `03_identity` · `04_fetch` · `05_run` · 자식 timeout = 60 · 300 · 10,800 s.)

### 3-3. 자식 env

- **뺀다 (이름만 기록):** 이름에 TOKEN · SECRET · PASSW · ACCESS_KEY · CREDENTIAL · COOKIE 가 있거나 `GIT_CONFIG_` 로 시작하는 것 (세션의 ssh → https
  insteadOf 둘 · `credential.interactive` — https URL 에는 쓰이지 않는다) · `GIT_ASKPASS` · `SSH_ASKPASS`.
- **둔다 (값은 기록하지 않음):** `HTTPS_PROXY` / `https_proxy` (로컬 agent proxy · http · 계정 정보 없음 — 형태만 확인) · `NO_PROXY` · `GIT_SSL_CAINFO` ·
  `SSL_CERT_FILE` (`/root/.ccr/ca-bundle.crt`) · `PATH` · `HOME`. git 은 `/root/.gitconfig` (`http.proxyauthmethod basic`) 와 `/etc/gitconfig` (git-lfs
  필터 — `git show` 의 blob 출력에는 쓰이지 않는다) 를 그대로 읽는다.
- **넣는다:** `MPLBACKEND=Agg` · `MPLCONFIGDIR` · `TMPDIR` (`SP/c4e1/mpl` · `SP/c4e1/tmp`) · `OMP` / `OPENBLAS` / `MKL_NUM_THREADS=1` · `GIT_TERMINAL_PROMPT=0`.
  fetch 는 여기에 `GIT_ALLOW_PROTOCOL=https` · `GIT_TERMINAL_PROMPT=0` 을 더한다 (run `:690`). run 은 BLAS 변수 셋을 `1` 로 다시 둔다 (`:828–829`).

### 3-4. fetch 안의 git (run `:665–716` — 목록 sha 로 고정된 코드 · 실패 시 재시도 없음)

cwd = `SP/c4e1/data` · git 단계마다 timeout 240 s (자식 전체 300 s 안):

1. `git init -q SP/c4e1/data/git`
2. `git -C SP/c4e1/data/git remote add origin https://github.com/REIL-UConn/Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics.git`
3. `git -C SP/c4e1/data/git fetch --depth 1 --filter=blob:none origin 1188c371e5836df4a7e5f5acf336a34ffd4027e6`
4. `git -C SP/c4e1/data/git show 1188c371e5836df4a7e5f5acf336a34ffd4027e6:LFP_Data.xlsx` → `SP/c4e1/data/LFP_Data.xlsx` (새 파일만)
5. `git -C SP/c4e1/data/git show 1188c371e5836df4a7e5f5acf336a34ffd4027e6:util_LFP.py` → `SP/c4e1/data/util_LFP.py` (새 파일만)

- checkout · 전체 clone 없음 · 두 경로만 (그 밖 경로 요청은 run 이 거부 `:679–682`) · 목적지는 저장소 밖 새 폴더만 (`:683–688`) · sha · bytes 대조 (run
  `:711–714`) + launcher 의 직접 재해시 (사후 대조).
- 네트워크: github.com 하나 (agent proxy 경유) · 4–5 의 지연 blob 읽기도 같은 origin 이다. **성공은 아직 검증되지 않았다.**
- **실패하면 그 자리에서 멈춘다** (git rc ≠ 0 · 프록시 403 / 407 · 연결 끊김 · sha / bytes 불일치 · timeout). 대체 출처 (P0 가 썼던
  raw.githubusercontent.com 포함) · 다른 URL · 다른 커밋 · 자동 재시도는 0 이다. 정책 거부면 막힌 호스트를 보고한다.

### 3-5. 읽기 경로 확보 (fetch 앞 · v3 §7 의 2)

`add_repo` (owner `REIL-UConn` · repo `Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics` · access `read`) 1 회. 결과 문구를
`<E>/04_read_path.txt` 에 남긴다. 거부 · 오류면 멈춘다 (fetch 0).

## 4. 단계 수용 (§72 조건 3)

- **단계 판정 = precheck_ok AND child_ok AND rc_0 AND timeout_false AND postcheck_ok** (launcher `stage_verdict` · 대조 l6).
  - child_ok — identity · fetch: 자식 stdout 마지막 줄의 `ok` 가 true. run: `ok` true **AND** `final.complete` true (run 최종 판정 = v3 §4-7 조건 1–6).
  - rc_0 은 bool 을 0 으로 받지 않는다.
  - **postcheck_ok 는 §72 의 넷에 더한 항이다** (더 엄격하다 · §8 의 2).
- run 모듈의 `stage_verdict` (`:392–398`) 는 rc · timeout 만 AND 하고 **사전 대조를 포함하지 않는다** — E1 에서는 쓰지 않는다.
- **E3a COMPLETE (C4-A 관문) = run 단계의 판정 complete.** 하나라도 어긋나면 E3a INCOMPLETE 이고, 행 · 파일 · 오류는 지우지 않는다 (v3 §4-7).

## 5. E1 순서 · 배정 · 중지 (§72 조건 5)

### 5-1. 순서

| # | 단계 | 배정 | 기대 | 어긋나면 |
|---|---|---|---|---|
| a | 승인 기록 § · 보존 규칙 (`evidence/reil_c4e1_<날짜>/** -text`) 커밋 → 착수 기록 (t0 · HEAD · 디스크 · 초안 sha) — 증거 폴더 · `SP/c4e1` 이 이미 있으면 멈춤 | — | — | 멈춤 |
| b | 복사 넷 (대조 → `tests/` · 골격 → `scripts/` · helper → `<E>` · 단계 실행기 → `<E>`) · sha 대조 · 커밋 | — | sha 일치 | 멈춤 |
| c | RED (단계 실행기 · 새 14 만) · 커밋 | 120 s | 14 실패 · 모두 `NotImplementedError` | 멈춤 |
| d | 고정 구현 복사 (sha 대조) → GREEN (E0 21 + N1 6 + 새 14) · 커밋 | 600 s | 41 passed | 멈춤 |
| e | **E1-1** identity (launcher) · 커밋 | 자식 60 s | 단계 complete | 멈춤 |
| f | 읽기 경로 (`add_repo`) | — | 거부 없음 | 멈춤 |
| g | **E1-2** fetch (launcher) · 커밋 (자료 제외) | 자식 300 s | 단계 complete | 멈춤 |
| h | **E1-3** run (launcher · 분리 실행) | 자식 10,800 s | 결과 그대로 (COMPLETE / INCOMPLETE) | 보고 · 멈춤 |
| i | 끝 기록 · 비밀 검사 · 커밋 · push · 결과 기록 § · 결과 검토 발송문 → 멈춤 | — | — | — |

- launcher 마다 탐침 ≤ 60 s. 계산 합 ≤ 120 + 600 + 60 + 300 + 10,800 + 탐침 180 = **12,060 s**.
- 전체 작업 (착수 기록 → 끝 기록) **6 h = 21,600 s** (v3 §7). 끝 기록은 커밋 · push · 문서 전 snapshot 이다.
- run 의 내부 시간 규칙은 v3 §4-1 그대로다 (원점 t0 = run 시작 · prep 900 · 측정 마감 9,000 · 기록 마감 9,900 · 단계 끝 10,800 s — `LIMITS` `:78–79`).
  [산술] 기대 경과 ≈ 35–45 분 (v3 §4-1 · C5 단가 기반 · 보증 아님).
- 재시도 0 · 실행 중 예산 변경 0 · run 이 INCOMPLETE 여도 다시 돌리지 않는다 (다시 돌리는 것은 새 승인).

### 5-2. v3 §7 과 다른 점

1. identity 를 fetch 앞에 둔다 (환경 식별이 깨졌으면 자료를 받지 않는다). v3 는 fetch → identity → run 이었다.
2. 세 자식이 모두 launcher (사전 · 사후 대조 · 그룹 정리) 를 거친다. 그 launcher 의 대조 단계 (E1-0) 가 새로 들어간다.

### 5-3. 중지 — 첫 예상 밖 실패에서 멈춘다

- 위 표의 "어긋나면" · launcher 단계 판정 false (사전 대조 실패 · rc ≠ 0 · timeout · child_ok false · 사후 대조 실패) · `add_repo` 거부 · 비밀 검사 적중 ·
  50 MB 넘는 파일.
- 멈추면: 그때까지의 기록을 지우지 않고 커밋 (자료 제외) · 보고한다. 다음 단계는 새 승인이다.
- run 안의 중지 조건 (대조 실패 · 시간 · 비용 규칙 · 구조 오류 · 감시) 은 v3 §4-5 그대로다. 그들 util 의 지역 오류는 중지가 아니라 INCOMPLETE 다.

## 6. 범위 · 자원 · 출력 · 제출 경계

### 6-1. 범위

- **자료 개봉 = run 안에서 그들 util 함수 (`visualize_LFP_data` · `extract_battery_data`) 로 xlsx 를 읽는 것뿐이다** (P0 · C5 와 같은 함수 · 인자 · v3 §3).
  util 은 run 안에서 sha · AST 최상위 검사 뒤 로드한다 (`c5.load_util`). launcher 는 두 파일을 해시만 한다 (파싱 0).
- 66 호출 · 호출당 상한 · 비용 규칙 · 자료 결속 · 판정은 v3 §4-1–§4-7 그대로다 (코드는 목록 sha 로 고정).
- pkl · 노트북 실행 · 출판 비교 · 해 선택 · 결과 요약 · C4-A / B · E3b · H4 · 설치 · 환경 재구축 · COMSOL 은 0 이다.

### 6-2. 자원

- run 안 (감시 · 강제 — v3 §4-4): RSS 표본 합 ≤ 4 GiB · 새 산출 ≤ 1 GiB (`<E>/run`) · 디스크 여유 ≥ 5 GiB · 작업자 4 · BLAS 스레드 1 · 동시 실행 금지.
- launcher (사후 관측 · 강제 아님): 최대 단일 자식 RSS (RUSAGE_CHILDREN) · 디스크 여유 · 증거 바이트.
- 저장소 밖 `SP/c4e1/`: 자료 ≈ 10.9 MB + git 객체 · pycache 폴더 (비어 있어야 한다) · mpl · tmp.

### 6-3. 출력 폴더

`bms-balancing/evidence/reil_c4e1_<착수 UTC 날짜>/` (없을 때만 만든다):

| 파일 | 쓰는 것 |
|---|---|
| `00_start.txt` · `00_porcelain_start.txt` · `00_identity_c4.py` · `00_step_runner.py` | 착수 · 복사 |
| `01_red.*` · `02_green.*` (meta · stdout · stderr · porcelain · source_sha256) | 단계 실행기 |
| `03_identity.*` · `03_identity.json` | launcher · helper |
| `04_read_path.txt` · `04_fetch.*` | `add_repo` 결과 · launcher (fetch 기록은 argv · sha · bytes 만 — 파일 바이트 없음) |
| `05_run.*` · `run/` (ROWS · AGGREGATE · OPERATION · RESOURCES · RULE · IDENTITY · HEADER · END_RECORD) | launcher · run (`final_record`) |
| `06_porcelain_end.txt` · `06_source_sha256_end.txt` · `07_end.json` | 끝 기록 |

### 6-4. 제출 경계

- **커밋한다:** 증거 폴더 전부 · `scripts/reil_c4e1_launch.py` · `tests/test_reil_c4e1_launch.py`.
- **커밋하지 않는다:** `SP/c4e1/` 전부 (xlsx · util 원본 · git 폴더 · pycache · mpl · tmp) — 저장소 밖이고, 원자료는 저장소에 넣지 않으며 (v2 §6-4),
  이미 보존된 util 텍스트를 다시 넣지 않는다 (v3 §2).
- **커밋 전:** 비밀 검사 (env 값 · 형태) + URL 계정 정보 형태 (`scheme://user:pass@`) 검사 · 파일 하나 ≤ 50 MB (넘으면 커밋하지 않고 멈춰서 묻는다).
- 자료는 E1 동안 `SP/c4e1/data` 에 그대로 둔다 (지우는 것은 E1 범위 밖).

## 7. 대조 14 · RED 선언 (E1-0)

| ID | 무엇을 막는가 |
|---|---|
| l1 | 양성 대조 — 고정 목록 · 정확한 다섯 바이트 · 탐침 플래그 · 섀도 없음 · 자료 → 사전 대조 통과 |
| l2 | 목록 sha 불일치 · schema · 넷 · 목록 밖 · 대문자 sha · 음수 · bool bytes · JSON 아님 → 각각 실패 |
| l3 | 모듈 +1 바이트 · 같은 크기 다른 바이트 · 없음 · 심볼릭 링크 · 링크된 상위 폴더 → 각각 실패 |
| l4 | 자식 sys.path 의 `scripts` 정규 패키지 · 모듈 · zip 항목 · 빈 항목 · 우리 `scripts/__init__.py` · bms 의 `scripts.py` → 실패 (`__init__` 없는 같은 이름 폴더는 통과) |
| l5 | 탐침 플래그 하나라도 다름 · argv 머리 변경 · 실행 스크립트 경로 변경 → 실패 |
| l6 | 단계 판정 = 다섯 항 AND — 각 항 거짓 · rc None / False / 2 / −9 · timeout → incomplete |
| l7 | 자식 결과 — run 은 마지막 줄 `ok` AND `final.complete` · 마지막 줄이 JSON 객체가 아니면 거짓 |
| l8 | `IDENTITY.json` 결속 — 경로 · sha 다름 · 표 · 행 없음 · 읽기 실패 · 모듈 다섯 아님 → 문제 |
| l9 | 사전 대조 실패 → 자식 0 (가짜 run 표식 없음) · `launched false` · 로그 없음 |
| l10 | 사전 대조 통과 → 고정 argv 의 가짜 run · 자식 env 에 토큰 · `GIT_CONFIG_*` 없음 · 모든 항 참일 때만 complete · INCOMPLETE (rc 2) · 경로 결속 실패 → false |
| l11 | timeout → 손주까지 그룹 SIGKILL · timed_out · stage false |
| l12 | 기록 · pycache 폴더가 이미 있으면 SystemExit — 탐침 · 자식 0 · 쓰기 0 |
| l13 | 자식 도중 모듈 변경 → launcher 재해시로 사후 실패 · fetch 의 틀린 바이트 → 사후 실패 · 맞으면 complete · 자료 폴더가 이미 있으면 fetch 사전 실패 |
| l14 | stdlib 만 import · 동적 import · exec 0 · 고정 상수 · 세 argv 문자 그대로 · env 위생 · main 의 승인 절 · 증거 폴더 규칙 |

- **RED 선언:** 골격에서 **14 실패 · 모두 `NotImplementedError`** (각 시험이 골격 함수를 부르는 지점에서). 다르면 멈춘다.
- **GREEN:** 고정 구현에서 **41 passed** (E0 21 + N1 6 + 새 14). 기존 시험 파일 · 다섯 모듈은 고치지 않는다 (목록 sha 그대로).
- 대조가 띄우는 자식: tmp 의 가짜 run (stdlib) · 탐침 (`-c`) · l11 의 손주 sleep 하나. 자료 · 네트워크 · 실제 run · optimizer · 우리 모듈 import 0.
- RED 는 인터페이스 수준이다 (E0 · N1 과 같음). 틀린 구현을 잡는 근거는 GREEN 의 음성 대조 (l2–l5 · l9 · l11–l13) 다.

## 8. 밝힐 것

1. launcher 는 새 검증 코드다. 정확성의 근거는 대조 14 와 검토 (정적) 뿐이고, 실제 E1 환경 (venv · 프록시 · 실제 모듈) 에서의 첫 실행이 E1-1 이다.
2. 단계 판정에 사후 대조 (모듈 · 자료 재해시 · `IDENTITY.json` 결속 · pycache 0 · 그룹 0) 를 더했다 — §72 의 넷보다 엄격하다.
3. TOCTOU — 사전 대조와 자식 import 사이, run 의 시작 대조와 끝 재해시 사이의 변경은 run 끝 재해시 · launcher 사후 대조가 잡지만 연속 감시는 아니다.
4. 해석기 · stdlib · site-packages · `sitecustomize` (`/usr/lib/python3.11/sitecustomize.py` 가 있다 — 탐침이 경로를 기록) · `.pth`
   (`distutils-precedence.pth`) 는 launcher 대조 밖이다 (C4-ENV identity · 봉인 MANIFEST 의 범위).
5. 그룹 판정은 /proc 의 pgid · 상태 (Linux) 로 하고, 좀비는 살아 있는 것으로 세지 않는다 (이 컨테이너의 PID 1 이 거두지 않을 수 있다).
6. 네트워크 성공 · 지연 blob 읽기 · 프록시 정책은 미검증이다. 실패하면 멈추고, 다른 출처로 바꾸지 않는다.
7. 기존 `scripts/__pycache__/` (gitignore · 바이트코드 7 개) 는 지우지 않는다 — E1 자식은 `-X pycache_prefix` 로 그것을 읽지 않는다. 이전 라운드의
   `-I` 자식 (identity · plan-e 등) 은 `-B` 없이 돌아 그 폴더에 쓸 수 있었다 (`-I` 는 `PYTHONDONTWRITEBYTECODE` 를 무시한다). 바이트코드는 소스의 mtime ·
   크기로 무효화되므로 그 기록들에 영향이 있었다는 근거는 없지만, 같은 크기 · 같은 초의 변경까지 막는 보장은 아니었다 — 이번에는 읽지 않게 한다.
8. identity 를 fetch 앞으로 옮겼다 (§5-2).
9. 시간 · 자원 표기 — 자식 경과는 launcher 의 외부 측정이고 run 의 상대 시각과 더하지 않는다 · RSS 는 사후 관측 · 끝 기록은 커밋 전 snapshot 이다.
10. legacy 라이브러리 경로 · plan-e 는 E1 에서 쓰지 않는다 (run CLI 는 목록을 요구한다 · plan-e 의 `identity_ok` 는 모듈 출처 확인이 아니다).
11. launcher 는 자기 sha 를 meta 에 적을 뿐 스스로 검증하지 않는다. 고정값 대조는 착수 · 끝 기록의 sha 표와 결과 검토에서 한다.
12. RED · GREEN 의 단계 실행기는 launcher 를 거치지 않는다 (시험은 실행 모듈을 자식으로 띄우지 않고 pytest 안에서 import 한다 — E0 · N1 과 같은 방식).

## 9. 하지 않는 것

H (C4-A · C4-B) · E3b · H4 · ray · pickle · 노트북 실행 · 출판 비교 · 해 선택 · 결과 요약 · 재시도 · 실행 중 예산 변경 · 설치 · 환경 재구축 · 정식 배열
재봉인 · 원자료 커밋 · 전체 clone · 대체 출처 · COMSOL. 다섯 모듈 · 목록 · 기존 시험 · 기존 증거는 바꾸지 않는다.

## 10. 정하실 것

1. **E1 승인** — (가) **E1-0 → E1-4 를 한 번의 승인으로 · 첫 예상 밖 실패에서 멈춤 (권장)** / (나) E1-0 만 먼저 → 결과 검토 → fetch · run 은 따로 승인.
2. **사전 검토** — **이 요청과 초안 셋을 Codex 에 먼저 보낸다 (권장 · 발송문 `docs/REIL_C4E_E1_PREREVIEW_SEND_20261015.md`)** / 사전 검토 없이 승인.
   권장 이유: launcher 는 새 검증 코드이고, E1 은 원자료를 처음 여는 되돌릴 수 없는 단계다.
