# REIL C4-ENV 새 환경 세대 (CPython 3.11.18) 재봉인 승인 요청 — 10월 선례 (§35–§38) 틀 + 검토자 복원 규칙 6 항 · 2026-11-24

> **승인 요청문이다.** 사용자 승인 전에는 venv 생성 · 내려받기 · 설치 · emit · check 를 하지 않는다 (0 회). 지금까지 한 것은 둘이다 (§9).
> (1) **읽기만 한 관측:** interpreter · deb · ensurepip 묶음 · 환경 변수 이름 · 경로 부재 · 디스크. 원문은 `bms-balancing/evidence/reil_c4_env_reseal_pre_20261124/` 에 있다.
> (2) **새 대조기와 자체 시험:** `bms-balancing/scripts/reil_c4_env_reseal_check.py` 를 쓰고 자체 시험 52 / 52 · 변이 증명 13 / 13 을 돌렸다. 쓴 자료는 합성 자료 ·
> 커밋된 10월 봉인과 원문 · 지금 ensurepip 묶음 (읽기만) 뿐이다. 기록은 `bms-balancing/evidence/reil_c4_env_reseal_selftest_20261124/`.
>
> 근거: 상태 문서 `REIL_PREREQUISITES_STATUS_20261004.md` §135 (C4-A 시작 전 환경 확인에서 멈춤) · §38 (검토자 복원 규칙 6 항 · 미승인) · §136 (이 요청서
> 작성 승인 — 사용자 원문 "권고대로해").
>
> **이것은 기존 환경의 동일 복원이 아니다 — 새 환경 세대다.** 2026-10-13 세대 (CPython 3.11.17 · `SP/reil_c4env/venv`) 는 컨테이너 교체로 없어졌다. 지금 해석기는
> 3.11.18 이고, ensurepip 의 pip wheel 도 바뀌었다 (§0). 그래서 §38 의 경계 ("환경이 바뀌면 별도 C4-ENV 승인") 대로 새 세대를 요청한다. 검토자 §5 의 복원 규칙
> 6 항은 원래 "같은 복원" 의 계약이다. 이 요청은 그 6 항을 새 세대의 검사 계약으로 그대로 채운다 (대응표 §8-3). 옛 봉인 · 기록 · 그 위의 C4-0 · C4-E 기록은 고치지
> 않는다 (이력).

## §0 무엇이 달라졌나 (2026-11-24 읽기 관측 · 원문 `evidence/reil_c4_env_reseal_pre_20261124/`)

| 항목 | 10월 세대 (수용 · §38) | 지금 | 판정 |
|---|---|---|---|
| interpreter `/usr/bin/python3.11` | 3.11.17 · build `Oct  1 2026 15:41:07` · sha256 `73bf4b06…cbb99` · 6,644,312 B | 3.11.18 · build `Oct 26 2026 15:28:55` · sha256 `ca969be9adfbddc0a593745da84da0348a4c2baf849daae18806a344708934c4` · 6,644,312 B · GCC 13.3.0 · 일반 파일 | **다름 → 새 세대** |
| deb | `3.11.17-1+noble1` | `3.11.18-1+noble1` (python3.11 · libpython3.11 계열 10 꾸러미) | 다름 |
| 플랫폼 | CPython · Linux · x86_64 · glibc 2.39 | 같음 | 같음 |
| ensurepip `setuptools-79.0.1` | sha256 `e147c054…fc51` | 같음 (1,256,281 B) · deb md5 와도 같음 | 같음 |
| ensurepip `pip-24.0` | sha256 `ba0d021a…69dc` | sha256 `9c51d6ade96c424e64356a9337fe15be2cce412b3ddb962f3efb61f63001d118` · 2,106,360 B | **다름** (아래) |
| 옛 venv | `SP/reil_c4env/venv` | 없음 | — |
| pip 관련 환경 변수 (이름만) | `PIP_CONFIG_FILE` · `PIP_CERT` (§38 · 제출자 보고) | 같은 둘 (`05_env_names.txt`) | 같음 |
| pip 설정 파일 | 없음 | 없음 (후보 4 곳) | 같음 |

**ensurepip pip wheel 의 차이 (읽기만 해서 확인):**

- wheel 안 구성원 524 개 가운데 `pip/_vendor/certifi/cacert.pem` 하나만 10월 설치 RECORD 원문의 행과 다르다. 대조기 `bundled` 모드로 확인했다 (`03_bundled_check.json` ·
  rc 0 · 선언 1 행 밖의 차이 0). 크기는 281,617 → 273,525 B 이고, 새 값은 RECORD 칸으로 `sha256=EtCzPV1HGcSG65jK42uCJO7zOhjjTOo_q8vcC6Q8Btk` 다.
- wheel 의 RECORD 도 그 파일에 맞게 다시 쓰여 있다. 구성원 524 개 모두 wheel 자신의 RECORD 와 맞는다.
- **deb 설치 뒤에 바뀌었다.** `dpkg -V python3.11-venv` 가 이 파일에 `??5??????` 를 보고한다. deb 이 기대하는 md5 는 `74e3c5e4…` 인데 실제는 `ea776773…` 다. 파일 시각
  (2026-10-27 19:51:53) 도 디렉터리 (19:43:22) 보다 뒤다. setuptools wheel 은 deb md5 와 같다 (`02_dpkg.txt`).
- 새 `cacert.pem` 은 certifi 형식의 다른 인증서 묶음으로 보인다. 인증서 블록이 136 개이고, 그 가운데 98 개가 시스템 묶음과 겹친다 (`04_cacert_member.txt`). 바꾼
  주체와 certifi 판은 **확인하지 못했다.**
- **과학 계산과의 관계:** 과학 코드 (`env_profile` · `reil_c6_profile` · COBYQA · Sobol) 는 pip 을 import 하지 않는다. 이 실행의 pip 은 `PIP_CERT` 묶음으로 TLS 를
  확인하므로 이 파일을 쓰지 않는다 (§1-5). 이 차이가 닿는 곳은 lock 의 pip `record-sha256` 한 칸이다. pip 은 wrapper 행 때문에 10월에도 이 칸이 바뀐 배포판이다.

## §1 고정 표 (10월 §1 의 9 항목 그대로 · 바뀐 값만 새로)

### 1-1. 저장소 HEAD · 보호할 원본

- 시작 HEAD 는 이 요청문 · 대조기 · 자체 시험 기록 · 승인 기록 · 보존 규칙이 든 커밋이다 (그 뒤 문서만 바뀐 커밋 포함). 실행 기록에 40 자로 적는다.
- 요청 커밋 뒤에 다음 가운데 하나라도 바뀌었으면 시작하지 않는다: `bms-balancing/scripts/` · `degradation-degeneracy/tools/env_profile.py` · 아래 보호 경로 (git diff 와
  작업트리 둘 다 본다).
- 보호 경로는 시작과 끝에 대조한다. 바뀌면 실패다.

| 보호 경로 | 식별 (HEAD `c984e07…` 의 git tree · 파일 sha256) |
|---|---|
| `bms-balancing/reil_c6_rebuild_20261013/` (**수용 봉인** · MANIFEST `4f120948…2ebdc`) | tree `f4384bb265ccd73ffc39cd4a43d7507014234bde` |
| `bms-balancing/evidence/reil_c4_env_20261013/` (RECORD 원문 30 + 4 · wheel 기록 28 + 4 · S9 기대값의 원천) | tree `df74b0e340c2c17fec440fa01c790d1c190fdc8e` |
| `bms-balancing/evidence/reil_c4_env_20261013_outer_return/` · `…/reil_c4_env_compare_selftest_20261013/` | tree `3e6808af5c902d882f133fd8d910cd12be3a8291` · `e8dbb40efd11176c8a7f33201cbfa0eb8d5b1759` |
| `bms-balancing/reil_c6_20261005/` · `bms-balancing/reil_c6_rebuild_20261006/` | tree `3ec46373da366265242e92df9c6e112e5ff100e0` · `b55f3a439e23bd41626d64bbb40b8221571f8690` |
| `bms-balancing/evidence/reil_p0_20261006/` · `…/reil_c6_n1_20261006/` · `…/reil_c5_impl_20261006/` | tree `82a74d69c3f3cad363d6f120fe0e88658af0a496` · `fdd12a5f30dc52242e0553b6b616c463a264fe54` · `cfea813242c2d47f559a3807c5bab1bb63f3e183` |
| `bms-balancing/evidence/reil_c5_pilot_20261006/` · `…_wrapper/` | tree `514e4dcd284f831a92e158ad4542136cc455f018` · `6238fff9ff7bc6a54747f28653eca4e3f1b20a2d` |
| `bms-balancing/evidence/reil_c4_env_reseal_pre_20261124/` · `…/reil_c4_env_reseal_selftest_20261124/` (이 요청의 근거 · 요청 커밋에 처음 듦) | tree `1e759c6a5d0e38fb7c84f20fe7233f8b15276cc7` · `6cedd7828d7a0949e70836efacb4b60f1aca3998` |
| `bms-balancing/scripts/reil_c4_env_reseal_check.py` (새 대조기) | `8cf10f3c910a46d4ffcf9eb933760178c439fcbec8636189776cb2bea2dbedb0` |
| `bms-balancing/scripts/reil_c6_profile.py` · `degradation-degeneracy/tools/env_profile.py` | `408afc4bb5eb1069583b955e0eb6215bf48dd9259ad474c230549d1b3642df5d` · `83b0d8365d039d75050d087fe980ad7b64818686b699e5d06da1c0ad63148563` |
| `bms-balancing/scripts/reil_c4_env_compare.py` (10월 도구 · **부르지 않음** · 보호만) · `bms-balancing/scripts/reil_c5_pilot.py` (보호만) | `eff94d3dfd4b3d31c7a19e440dfb968734dab1afb16b584c2fdee354100695e0` · `73bee8dc412b39863afb64b70bc128cbecee2075a3a17914fc7288f353ef11a6` |
| `bms-balancing/evidence/reil_p0_20261006/01_venv_constraints.txt` (`-c`) | `db63333bdaf1835444a86187215ed7faf06897eb8a247c667ed167a5ee1dc772` |

- 작업트리 원문 (`git status --porcelain=v1 --untracked-files=all`) 은 시작과 끝에 그대로 보존한다. 분류 결과와 따로 둔다.

### 1-2. interpreter (S0 에서 다시 잰다 · 하나라도 다르면 시작하지 않고 재확인을 요청한다)

| 항목 | 고정값 (2026-11-24 읽기 관측) |
|---|---|
| 경로 · 종류 · 크기 · sha256 | `/usr/bin/python3.11` · 일반 파일 (심볼릭 링크 아님) · 6,644,312 B · `ca969be9adfbddc0a593745da84da0348a4c2baf849daae18806a344708934c4` |
| 판 · 빌드 · 컴파일러 | `3.11.18` · `["main", "Oct 26 2026 15:28:55"]` · `GCC 13.3.0` |
| 구현 · 플랫폼 · libc | CPython · Linux · x86_64 · glibc 2.39 |
| deb | `python3.11-minimal` · `libpython3.11-stdlib` · `python3.11-venv` = `3.11.18-1+noble1`. apt 원천 기록은 없다 (10월과 같음) |
| `dpkg -V python3.11-venv` | 출력이 정확히 이 한 줄이어야 한다: `??5??????   /usr/lib/python3.11/ensurepip/_bundled/pip-24.0-py3-none-any.whl` |
| ensurepip 묶음 | `pip-24.0-py3-none-any.whl` 2,106,360 B · `9c51d6ad…1d118` / `setuptools-79.0.1-py3-none-any.whl` 1,256,281 B · `e147c054…fc51`. 구성원 대조 규칙은 §1-8 |
| ensurepip · venv 소스 | `/usr/lib/python3.11/ensurepip/__init__.py` `0f4e3b95882c914577a9045e27ac88f78d9a0a931a409d3d0287df1cd49e945a` · `/usr/lib/python3.11/venv/__init__.py` `8671bc5810ee3e52a5ae7aa3b625764688cf12513b2f8e1b0b82aaec93f118a6` |

- 10월 S0 은 ensurepip · venv 소스의 sha 를 재지 않았다. 그래서 이 두 값은 이번 세대의 고정값이고, 10월 값과 같은지는 알 수 없다.

### 1-3. 정확한 경로

모두 지금 없다 (2026-11-24 · `06_paths_disk.txt`). S0 에서 하나라도 있으면 중지한다. 덮어쓰기 · 다른 이름으로 바꾸기 (fallback) 는 없다. `SP` =
`/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad` 다. 세션 스크래치이고, 저장소 밖이며, 저장소와 같은 파일시스템
`/dev/vda` 에 있다. 이 문자열은 10월과 같다.

| 용도 | 경로 |
|---|---|
| 작업 뿌리 · venv · 과학 wheel · 시험 wheel · 시험 도구 · 임시 (`TMPDIR`) | `SP/reil_env18/` · `…/venv/` · `…/wheels/` · `…/wheels_test/` · `…/pytest_t/` · `…/tmp/` |
| 실행기 (승인 뒤 작성 · §2-1) | `SP/c4env18_runner/run.py` (+ 원점 전 점검 출력 `precheck.stdout` · `precheck.meta.json`) |
| 새 봉인 (저장소) | `bms-balancing/reil_c6_rebuild_20261124/` |
| 기록 (저장소) | `bms-balancing/evidence/reil_c4_env_20261124/` (RECORD 원문은 `09_records/` 30 · `09_test_tool_records/` 4) |
| 커밋 뒤 관측 (커밋 밖 → 뒤에 문서 커밋) | `SP/reil_env18/11_after_commit.json` → `bms-balancing/evidence/reil_c4_env_20261124_after/` |

- **뿌리 이름 `reil_env18` 을 고른 이유:**
  - 옛 뿌리 `reil_c4env` 와 같은 10 글자다. 그래서 콘솔 스크립트 첫 줄이 `python` 119 B · `python3.11` 123 B 로 옛것과 같고, 127 B 아래라 옛 형식 그대로다.
  - wrapper 파일 크기도 옛것과 같으므로 RECORD 의 크기 칸이 그대로이고 해시 칸만 바뀐다.
  - 옛 경로 문자열의 앞부분 · 뒷부분이 아니어서 검색할 때 섞이지 않는다.
  - 같은 경로 문자열을 두 세대에 쓰지 않는다. 10월 §1-3 의 원칙이고, C4-0 · C4-E 기록의 `SP/reil_c4env/venv` 는 3.11.17 세대를 가리킨다.
- pip 캐시는 쓰지 않는다 (`--no-cache-dir`). 설정 파일도 읽지 않는다 (`PIP_CONFIG_FILE=/dev/null`). 홈 · 시스템 경로에는 쓰지 않는다.

### 1-4. 과학 lock 30 · 설치 고정 목록 · 시험 도구 (10월과 같음)

- 기준 lock 은 수용 봉인의 `bms-balancing/reil_c6_rebuild_20261013/REIL_C6.lock.txt` (sha256 `ea91156cac99fac17830818f17fd4a260a93722269f720171e0ab9b2a75c1faa`) 다.
  30 배포판과 판은 10월 요청 §1-4 의 목록과 같다.
- 설치 고정 목록 `-c` 는 `01_venv_constraints.txt` (28 줄 · 위 sha) 이고, 읽기만 한다. 최상위 요청 7 개도 10월과 같은 순서다.
- 업그레이드 · 추가 패키지 · 판 완화 · 소스 빌드 (`--only-binary=:all:`) 는 없다.
- 시험 도구는 pytest 9.1.1 · pluggy 1.6.0 · iniconfig 2.3.0 · pygments 2.21.0 이다.
  - `pip install --target SP/reil_env18/pytest_t --no-deps` 로 깔고, 과학 venv 밖에 둔다 (lock 30 불변).
  - 쓸 때는 `PYTHONPATH` 로 붙인다. emit / check 때는 `PYTHONPATH` 를 두지 않는다.
  - **이 단계에서 pytest 를 실행하지 않는다.**

### 1-5. 출처 · 네트워크 · argv · 유효 환경 (검토 ENV-P2-04 반영)

- **색인을 argv 로 고정한다:** S2 · S3 에 `--index-url https://pypi.org/simple` 을 넣는다. pip 기본값과 같은 값이지만 명시한다. extra index · find-links 는 S2 · S3 에서
  0 이다. 설치 (S5 · S6) 는 `--no-index --find-links` 로 S2 · S3 의 파일만 쓰며, 네트워크는 0 이다.
- **자식 환경 규칙** (S0 의 대조기 호출과 S1–S9 의 모든 자식):
  1. 비밀 형태 이름을 뺀다. 10월 정규식 그대로이고 (`TOKEN|SECRET|PASSW|ACCESS_KEY|CREDENTIAL|COOKIE|^GIT_CONFIG_` · 대소문자 무시), 뺀 이름만 기록한다.
  2. `PIP_` 로 시작하는 이름은 **`PIP_CERT` 하나만 물려받고** 나머지는 전부 뺀다 (이름 기록). pip 단계에는 실행기가 `PIP_CONFIG_FILE=/dev/null` 을 넣는다. pip 은 이
     값이면 설정 파일을 하나도 읽지 않는다. 이렇게 하면 `PIP_INDEX_URL` · `PIP_EXTRA_INDEX_URL` · `PIP_FIND_LINKS` 같은 출처 변수가 자식에 들어갈 수 없다.
  3. `PIP_CERT` 가 없으면 S0 에서 멈춘다 (유효 환경이 고정 표와 다르다). 그 값 (경로) 은 문서 · 기록에 옮기지 않는다. 가리키는 파일의 크기 · sha256 만 기록한다.
  4. 단계마다, 자식에 넘긴 환경 변수 **이름 전체**와 실행기가 넣은 값 (`TMPDIR` · `PIP_CONFIG_FILE` · `PYTHONDONTWRITEBYTECODE`) 을 meta 에 적는다. 그 밖의 값은 적지
     않는다 (하드룰 2).
- **pip 이 쓰는 CA:** `PIP_CERT` 가 있으면 pip 은 그 묶음으로 TLS 를 확인하고, wheel 안 `cacert.pem` (§0 의 바뀐 파일) 은 쓰지 않는다. 그 파일은 venv 의 pip 안에
  들어갈 뿐이다. 내려받은 바이트가 맞는지는 TLS 가 아니라 S4 의 sha256 대조가 보증한다.
- **파일 호스트 관측 (간접):** pip 24.0 의 `pip/_internal/network/download.py` `_prepare_download` 는 파일 호스트가 `files.pythonhosted.org` 일 때만
  `Downloading <파일 이름>` 으로 쓰고, 그 밖이면 전체 URL 을 쓴다. 지금 묶음의 소스를 읽어서만 확인했다.
  - 그래서 S2 · S3 stdout 의 `Downloading` 줄이 전부 파일 이름 꼴이면, pip 이 본 파일 호스트가 `files.pythonhosted.org` 라는 뜻이다.
  - 결과 보고에 그 줄의 수와 꼴 (이름 꼴 / URL 꼴) 을 센다.
- **한계 (검토 ENV-P2-04 그대로):** 이것은 독립 네트워크 감사가 아니다. 프록시가 본 실제 연결과 색인 페이지의 호스트는 이 기록에 없다. argv 설정 자체도 OS 차단의 증거가
  아니다.
- 모든 명령의 argv · cwd · 환경 (위 규칙) · 시작 / 끝 시각 · rc · stdout / stderr 원문을 기록에 남긴다.

### 1-6. 시험 도구 기록

- wheel 4 개는 S4b 에서 10월 기록과 이름 · 크기 · sha256 을 대조한다.
- 설치된 RECORD 4 개는 S9a 가 원문을 `09_test_tool_records/` 에 보존한다. 같은 단계에서 10월 원문과 행 단위로 대조하고, 해시 있는 행은 `pytest_t` 의 실제 바이트와
  대조한다. 이것이 검토 §5-3 의 "외부 `pytest_t` 별도 결속" 이다.
- 디스크 · 시간은 합계에 넣는다.

### 1-7. 프로필 스크립트 · emit / check

- 프로필 스크립트는 `bms-balancing/scripts/reil_c6_profile.py` (`408afc4b…df5d`) 다. 이 스크립트가 부르는 저장소 소스는 `env_profile.py` (`83b0d836…8563`) 하나다.
- emit: cwd `/home/user/Yonghoon-DEM-DFT` · env `TMPDIR=SP/reil_env18/tmp PYTHONDONTWRITEBYTECODE=1` · argv
  `SP/reil_env18/venv/bin/python bms-balancing/scripts/reil_c6_profile.py emit bms-balancing/reil_c6_rebuild_20261124`.
- check: emit 과 같고 `emit` 자리에 `check` 를 쓴다. 기대 출력은 `check OK` · rc 0 이다.
- **출력 경로 예외 (검토 §5-4 · 이 승인이 정확히 고정한다):**
  - emit 은 빈 디렉터리에만 쓴다. `reil_c6_profile.py` 222–225 행이 비어 있지 않은 출력 폴더를 거부한다.
  - 10월 argv 의 경로를 그대로 쓰면 수용 봉인 폴더와 부딪힌다. 그래서 출력 경로를 `bms-balancing/reil_c6_rebuild_20261124` 하나로 고정한다.
  - 그 밖의 argv · env 는 10월과 같다. 수용 봉인은 읽기만 한다 (S9 기대값의 원천).
  - "같은 argv" 를 임의 변경 권한으로 읽지 않는다.
- **실제 계산 (C4-N1 그대로):**
  - emit 1 회 = lock 측정 + PROFILE + 합성 COBYQA 1 회 + Sobol 경로 1 벌.
  - check 1 회 = 봉인 해시 대조 + 임시 폴더에서 emit 1 회 전부 다시 + 바이트 대조.
  - 합계 = **합성 COBYQA 2 회 · Sobol 경로 2 벌** · REIL 자료 0. 과거 check 를 이번 세대의 실측으로 대신하지 않는다.

### 1-8. 허용 old→new 차이 (옛 = 수용 세대 `reil_c6_rebuild_20261013/` 과 `evidence/reil_c4_env_20261013/`) — 이것만 · 정확 바이트로

| 대상 (단계) | 허용하는 차이 (이것만) | 대조기 모드 · 자체 시험 사례 |
|---|---|---|
| ensurepip 묶음 2 (S0) | setuptools = 10월 sha. pip = §1-2 의 새 크기 · sha. pip wheel 구성원에서 10월 설치 RECORD 행과 다른 것은 `pip/_vendor/certifi/cacert.pem` 한 행뿐이고, 옛 값 (`eU0Dn_3y…` · 281617) → 새 값 (`EtCzPV1H…` · 273525) 이 정확해야 한다. 10월 설치에만 있는 행은 pip 생성 범주뿐이다 (wrapper · 자기 `INSTALLER` · `REQUESTED` · `RECORD` · 해시 없는 pyc). 구성원은 wheel 자신의 RECORD 와 전부 맞아야 한다 | `bundled` · B0–B6 |
| 과학 wheel 28 (S4a) | 10월 `04_artifacts_science.json` 과 이름 · 크기 · sha256 의 정확한 집합 (차이 0) | `wheels` · W0–W5 |
| 시험 wheel 4 (S4b) | 10월 `04_artifacts_test.json` 과 같다 (차이 0) | `wheels` |
| 과학 RECORD 30 · 시험 RECORD 4 (S9a) | 아래 표 | `records` · R1–R20 · R14b |
| `REIL_C6.lock.txt` (S9b) | 옛 lock 에서 두 자리만 바꾼 바이트와 정확히 같아야 한다: (1) `#@ python "3.11.17"` → `"3.11.18"` (2) RECORD 가 바뀐 배포판의 `record-sha256` 칸을 새 원문의 값 (`env_profile` 의 `read_text` 규칙 = universal newline 뒤 utf-8 sha256) 으로. 기대 목록은 cffi · fonttools · numpy · pip 다. 옛 lock 의 record-sha 30 은 옛 원문 30 과 결속을 확인한다. 머리줄 · `#@ files` (7187 / 5301 / 1 / 1) · collision · `dists_without_record` 줄은 한 바이트도 바뀌면 안 된다 | `seal` · S1–S3 · S9 · S10 · P2 |
| `PROFILE.json` | 옛 PROFILE 의 `python.version` · `python.build` 두 값만 §1-2 값으로 바꾸고 같은 직렬화 (`sort_keys` · `indent=1` · 끝 LF) 로 다시 만든 바이트 | S4 · S5 |
| `COBYQA_OPTIONS.json` · `SOBOL_PHASE_A.json` · `.npy` 6 | 바이트 동일 (옵션 8 · 구현 파일 4 의 sha · 합성 호출 결과 · 배열 raw sha 포함) | S7 |
| `MANIFEST.json` | 옛 MANIFEST 의 lock · PROFILE 두 값만 새 sha 로 바꾼 바이트이고, 새 파일 10 개와 맞아야 한다 | S6 |
| 봉인 파일 집합 | 11 개 정확히 | S8 · S8b |

**RECORD 대조 (S9a) 의 규칙** — 검토 §5-3 과 ENV-P2-02 를 닫는 자리:

| 규칙 | 내용 |
|---|---|
| 줄 · 줄 끝 | 줄 수와 줄 끝의 종류 (CRLF · 마지막 줄 포함) 가 옛 원문과 같아야 한다. `splitlines` 로 버리지 않는다 |
| 행 | 행 경로와 순서가 같아야 한다. 각 줄은 CSV 로 다시 쓴 바이트가 원문과 같아야 한다 (정확 재구성). 같은 경로가 두 번 나오면 미허용이다 (dict 로 덮지 않는다) |
| 값이 달라도 되는 행 | (i) **wrapper 13 행** — 과학 10 (cffi 1 · fonttools 4 · numpy 2 · pip 3) · 시험 3 (pytest 2 · pygments 1). 새 파일 첫 줄이 `#!SP/reil_env18/venv/bin/<python\|python3.11>` 이어야 하고, 그 첫 줄만 옛 경로로 되돌린 바이트가 옛 행의 해시 · 크기와 같아야 한다. 본문 · 이름 · 판정 범주를 옛 행에 결속하는 규칙이다. 값이 옛것과 같아 보여도 이 검사는 언제나 한다 (옛 경로가 남은 파일을 잡는다). (ii) **선언 1 행** — pip 의 `cacert.pem` (옛 값 → 새 값 정확). 그 밖의 행 값 차이는 미허용이다 |
| dist-info | 한 RECORD 안의 `*.dist-info/…` 행은 자기 dist-info 의 것뿐이어야 한다. 다른 배포판의 `INSTALLER` · `REQUESTED` · `RECORD` 행은 미허용이다 |
| 설치 바이트 | 해시 있는 행은 전부 실제 설치 바이트 · 크기와 같아야 한다. venv 는 site-packages 기준이고 `../../../bin` · `../../../share` 를 포함한다. `pytest_t` 는 `../../bin/X` 를 `pytest_t/bin/X` 로 읽는다 (pip `--target` 은 bin 을 옮기고 RECORD 를 고치지 않는다) |
| 해시 없는 행 | `__pycache__/*.pyc` 와 자기 `RECORD` 뿐이다 |
| 설명된 충돌 | 1 건 — `../../../LICENSE` (about-time 4.2.1 ↔ alive-progress 3.3.0 · `reil_c6_profile.EXPLAINED_COLLISIONS` 와 같다). 이 행의 디스크 바이트는 주인 (alive-progress) 행과 같아야 한다. 선언과 관측이 다르면 미허용이다 |
| 보존 | 새 원문 30 + 4 를 바이트 그대로 보존한다 (`09_records/` · `09_test_tool_records/`). S9b 의 lock 기대값은 이 보존본에서 계산한다 (결속) |
| 관측만 | RECORD 어디에도 없는 파일 (site-packages · `pytest_t`) 은 수와 첫 50 개를 적고 **판정에 쓰지 않는다.** 10월 세대에 같은 관측이 없어 기준이 없다. 다음 세대의 기준으로 쓸지는 결과 검토에서 정한다 |

- 10월 원문 34 의 규모는 행 13,398 · 해시 있는 행 7,657 · 해시 없는 행 5,741 이다. 이 가운데 과학은 7,188 행이 해시 있음이다 (lock `verified` 7,187 + 충돌 1).
- **대조기:** `bms-balancing/scripts/reil_c4_env_reseal_check.py` (32,342 B · sha256 `8cf10f3c…dbedb0`).
  - stdlib 만 쓰고 `/usr/bin/python3.11 -I -B` 로 돌린다. 과학 패키지 import 는 0 이다.
  - 출력 파일이 이미 있으면 쓰지 않는다 (rc 2). rc 는 0 = 허용만 · 1 = 미허용 · 2 = 사용 오류 · 3 = 도구 오류다.
  - 고정값 (옛 · 새 venv 경로 · 선언 행 · 충돌 · ensurepip 값 · python 판) 은 파일 안의 상수다. 그래서 **이 세대 전용**이고, 범용 자동 복원 검사기가 아니다 (§8-2).
  - 10월 `reil_c4_env_compare.py` 는 부르지 않는다. 그 도구는 그 실행의 증거로 보호만 한다.
- "미허용" 이면 성공으로 채택하지 않는다. 그 자리에서 멈추고, 원문을 보존하고, 보고한다. libc · BLAS · 옵션 · 배열 · 그 밖 RECORD 의 미상 차이는 포괄 승인하지 않는다.

### 1-9. 시간 원점 · 배정 · 디스크 (검토 ENV-P2-01 반영)

- **원점과 전체 한도:** 원점 t0 은 S0 의 첫 명령 직전이다 (UTC 와 monotonic 둘 다 기록). 전체 한도 1,800 s 는 t0 부터 S10 의 로컬 커밋 끝까지다. push 는 한도 밖이고
  기록만 한다.
- **단계별 배정:** §2 표의 timeout 이고, 합계는 정확히 1,800 s 다. 자식마다 timeout 은 min(단계 배정의 남은 몫, 전체의 남은 몫) 이다. S4 a / b 는 30 s 를, S9 a / b 는
  120 s 를 나눠 쓴다. 남은 시간을 다른 단계로 자동으로 돌리지 않는다.
- **S10 도 90 s 를 강제한다.** S10 안의 git · 검사 호출마다 남은 몫을 timeout 으로 준다. 10월 실행기는 S10 을 합산해 강제하지 않았고, 전체 한도도 마지막 작업 전에만
  검사했다 (ENV-P2-01).
- **디스크 한도 2,000,000,000 B:** `du -sb` 로 `SP/reil_env18/` · 새 봉인 · 기록 셋을 합산한다.
  - 관측 시점은 S2 · S3 · S5 · S6 · S8 · S9 끝 · S10 커밋 직전 · **커밋 뒤**다. 넘으면 그 자리에서 중지한다.
  - 보고에는 "표본 최대" 라고 적고, 연속 peak 가 아니라고 밝힌다.
  - `df -B1` 여유는 시작과 끝에 참고로만 적는다. 메모리 한도가 아니고 설치 완료를 보증하지도 않는다. 재지 못한 값을 0 이나 PASS 로 바꾸지 않는다.
- **커밋 뒤 관측 (ENV-P2-01):**
  - 로컬 커밋이 끝나면 실행기가 monotonic 끝 시각 · `du -sb` 합 · 커밋 rc · 커밋 SHA 를 `SP/reil_env18/11_after_commit.json` 에 쓴다. 이 파일은 커밋 밖이고, 커밋된
    기록을 고치지 않는다.
  - 실행기의 바깥 반환 (stdout 원문 · rc) 은 실행하는 쪽 (하네스) 이 파일로 받는다.
  - 이 둘은 재실행 없이 별도 문서 커밋으로 `evidence/reil_c4_env_20261124_after/` 에 붙인다.
  - 커밋 뒤 관측이 한도를 넘으면 그 실행을 **한도 초과**로 보고한다. 이미 커밋된 기록은 고치지 않고, 이 파일이 정정 참조가 된다.
- **시작 조건:** 여유가 4,000,000,000 B 이상이어야 한다 (한도의 2 배). 2026-11-24 관측은 26,006,093,824 B 이고, S0 에서 다시 잰다.
- **실패하면:** 만든 파일을 지우지 않는다 (정리 승인 없음 · 스크래치는 세션과 함께 사라진다). 저장소 쪽 (부분 봉인 · 기록) 은 "정지 상태의 기록 · 채택 아님" 으로 커밋한다
  (10월 §1-9 와 같다).

## §2 순서 · 정확 argv

### 2-1. 실행기 (승인 뒤 작성 · 10월 선례 §36)

10월 실행기 (`evidence/reil_c4_env_20261013/00_runner.py` · `5c781a2d…d2cc`) 를 바탕으로 쓰고, 다음 차이만 넣는다. stdlib 만 쓰고 저장소 밖 `SP/c4env18_runner/run.py`
에 둔다. `bms-balancing/scripts/` 에 두지 않는 이유는 §1-1 의 시작 조건이다. S0 은 사본 (`E/00_runner.py`) 과 10월 실행기에 대한 diff (`E/00_runner.diff`) 를 둘 다
보존한다.

1. 경로 · 고정값: §1-2 · §1-3 의 값, 이 요청문의 sha, 요청 커밋, 승인 커밋.
2. 자식 환경 규칙: §1-5.
3. S0 에 더하는 것: `dpkg -V python3.11-venv` 대조 · ensurepip / venv 소스 sha · `PIP_CERT` 존재 · 대조기 `bundled` 호출.
4. S4 · S9 는 새 대조기를 부른다 (10월 도구 대신).
5. S10 강제와 커밋 뒤 관측: §1-9.
6. **원점 전 읽기 전용 점검 1 회 (`precheck`):**
   - 쓰는 것은 그 출력 두 파일 (`SP/c4env18_runner/precheck.stdout` · `precheck.meta.json`) 뿐이고, 디렉터리 생성은 0 이다.
   - 그 원문을 S0 이 `E/00_precheck_before_t0.*` 로 복사한다. 10월 편차 (b) (원문 없이 한 사전 점검) 를 신고된 절차로 바꾼 것이다.
   - 이 1 회 밖의 원점 전 점검은 없다. precheck 이 문제를 보고하면 실행하지 않고 사용자에게 묻는다.

실행: `/usr/bin/python3.11 -I SP/c4env18_runner/run.py precheck` (1 회) → `/usr/bin/python3.11 -I SP/c4env18_runner/run.py` (1 회).

### 2-2. 단계 표

- cwd 는 저장소 뿌리 `/home/user/Yonghoon-DEM-DFT` 다. 공통 env 는 `TMPDIR=SP/reil_env18/tmp` 이고, 환경 규칙은 §1-5 다.
- 줄임말:
  - `V` = `SP/reil_env18/venv/bin/python` · `P` = `/usr/bin/python3.11 -I -B` · `K` = `bms-balancing/scripts/reil_c4_env_reseal_check.py`
  - `C` = `bms-balancing/evidence/reil_p0_20261006/01_venv_constraints.txt` · `OE` = `bms-balancing/evidence/reil_c4_env_20261013`
  - `E` = `bms-balancing/evidence/reil_c4_env_20261124` · `N` = `bms-balancing/reil_c6_rebuild_20261124`
  - `X` = `--no-cache-dir --disable-pip-version-check` · `I` = `--index-url https://pypi.org/simple`
  - pip 단계 env 에는 `PIP_CONFIG_FILE=/dev/null` 을 더한다.

| 단계 | 명령 (argv) | timeout (s) | 네트워크 |
|---|---|---|---|
| S0 사전 대조 | 읽기 대조 (HEAD · porcelain 원문 · §1-1 보호 · §1-2 재측정 · `dpkg -V` · 소스 sha · §1-3 경로 부재 · 여유 · `PIP_CERT`) → `mkdir SP/reil_env18 SP/reil_env18/tmp E` (있으면 실패) → 시작 기록 (precheck 원문 사본 포함) → `P K bundled --bundled /usr/lib/python3.11/ensurepip/_bundled --out E/00_bundled_check.json` (rc ≠ 0 이면 S1 전 중지) | 60 | 0 |
| S1 venv | `/usr/bin/python3.11 -I -m venv SP/reil_env18/venv` | 120 | 0 |
| S2 과학 내려받기 | `V -I -m pip download X I --only-binary=:all: --dest SP/reil_env18/wheels -c C numpy==2.4.6 scipy==1.17.1 pandas==3.0.5 openpyxl==3.1.5 matplotlib==3.11.2 seaborn==0.13.2 pymoo==0.6.2` | 480 | PyPI |
| S3 시험 도구 내려받기 | `V -I -m pip download X I --only-binary=:all: --no-deps --dest SP/reil_env18/wheels_test pytest==9.1.1 pluggy==1.6.0 iniconfig==2.3.0 pygments==2.21.0` | 120 | PyPI |
| S4 wheel 대조 | a `P K wheels --wheels SP/reil_env18/wheels --expect OE/04_artifacts_science.json --out E/04a_wheels_science.json` · b `P K wheels --wheels SP/reil_env18/wheels_test --expect OE/04_artifacts_test.json --out E/04b_wheels_test.json`. rc ≠ 0 이면 설치 전 중지 | 30 | 0 |
| S5 과학 설치 | `V -I -m pip install X --no-index --find-links SP/reil_env18/wheels -c C numpy==2.4.6 scipy==1.17.1 pandas==3.0.5 openpyxl==3.1.5 matplotlib==3.11.2 seaborn==0.13.2 pymoo==0.6.2` | 300 | 0 |
| S6 시험 도구 설치 | `V -I -m pip install X --no-index --find-links SP/reil_env18/wheels_test --no-deps --target SP/reil_env18/pytest_t pytest==9.1.1 pluggy==1.6.0 iniconfig==2.3.0 pygments==2.21.0` | 120 | 0 |
| S7 emit | §1-7 (env `PYTHONDONTWRITEBYTECODE=1` 추가) | 180 | 0 |
| S8 check | §1-7 · `check OK` · rc 0 | 180 | 0 |
| S9 old→new 대조 | a `P K records --venv SP/reil_env18/venv --target SP/reil_env18/pytest_t --records-out E/09_records --test-records-out E/09_test_tool_records --out E/09a_records.json` · b `P K seal --new N --new-records E/09_records --out E/09b_seal.json` | 120 | 0 |
| S10 기록 · 커밋 | 끝 기록 (`E/10_end.json` · 끝 porcelain 원문 · §1-1 보호 대조 · `du -sb` · `df -B1`) → 비밀값 검사 → `git add -f N E` → 스테이지 blob = 디스크 바이트 전수 대조 → 로컬 커밋 → (커밋 밖) `11_after_commit.json` | 90 | 0 |

- 10월 §2 와 다른 argv 는 넷이다: S2 · S3 의 `I` (명시) · S4 · S9 의 새 대조기 · S7 · S8 의 출력 경로 · S0 의 대조기 호출. 그 밖은 10월과 같다.
- 위 명령 밖의 설치 · 실행은 없다. pytest · 변이 증명 · C5 재측정 · REIL 자료 · C4-A 는 포함하지 않는다.

## §3 중지 조건 (그 자리에서 멈춤 · 첫 오류와 확보된 기록 보존 · 재시도 0)

1. precheck 또는 S0 사전 조건 실패: HEAD · 보호 · interpreter · deb · `dpkg -V` · 소스 sha · 경로 · 여유 · `PIP_CERT`.
2. S0 의 `bundled` rc ≠ 0 (ensurepip 묶음이 §1-2 · §1-8 과 다름 · S1 전).
3. 어느 단계든 rc ≠ 0 이거나 timeout (S10 포함).
4. S4 의 이름 · 크기 · sha256 불일치 (설치 전).
5. 디스크 관측 > 2,000,000,000 B, 또는 t0 부터 1,800 s 초과.
6. S8 check 가 OK 가 아님 (새 환경 안에서도 재현이 안 된다는 뜻).
7. S9a · S9b 에 미허용 차이 (§1-8). 채택하지 않고, 정지 상태 기록으로 커밋한다.
8. S10 에서 보호 경로가 바뀜 · 비밀값 검사에 걸림 · 스테이지 대조 실패. 실패로 보고한다.
9. 커밋 뒤 관측이 한도를 넘음. 이미 커밋된 기록은 그대로 두고, 한도 초과로 보고한다.

하지 않는 것: 임의 재시도 · 패키지 판 완화 · 다른 interpreter · 새 경로 fallback · 코드 수정 · ensurepip 묶음 우회 (§7 Q3 의 B 안은 이 승인 밖이다). 실패 뒤 다음
걸음은 사용자에게 다시 묻는다.

## §4 결과 제출 · 수용 (10월 초안의 7 조건 + 검토자 복원 규칙 6 항)

| 조건 | 이 요청에서 |
|---|---|
| 1 승인 원문 · 고정 표 · 명령 · cwd · 원점 · 시작 / 끝 HEAD · 작업트리 목록 보존 | `E/00_*` 에 둔다: 승인 원문 사본 · 이 문서 sha · t0 · precheck 원문 · 실행기 사본과 10월 diff. 단계별 meta 에 argv · cwd · env 이름 · 시각 · rc 를 적고, porcelain 원문은 시작과 끝에 둔다 |
| 2 과학 배포판 · Python 판 / 빌드 · 플랫폼 / libc · BLAS / LAPACK · RECORD · 파일 대조 · 충돌 표를 old / new 나란히 | `E/09a_records.json` · `E/09b_seal.json` 을 결과 보고서의 사람용 표로 옮긴다. lock 의 `#@ files` 집계와 collision 줄 · wrapper 13 행 · 선언 1 행 · 설치 바이트 대조 수 · 관측 (RECORD 밖 파일) 도 포함한다 |
| 3 COBYQA 옵션 · 구현 파일 · Sobol 6 의 .npy sha 와 raw sha 를 각각 대조 | 바이트 동일 판정을 하고, 보고서 표에 sha 쌍을 하나씩 적는다 |
| 4 새 봉인과 옛 봉인을 각각 독립 식별 · 새 lock 을 과거 실행이 썼다고 소급 기록 금지 | 새 MANIFEST · lock · PROFILE 의 sha 를 따로 적는다. 옛 봉인 · C4-0 · C4-E 기록은 바이트 그대로 둔다 |
| 5 시간 · 디스크 · 최종 기록의 실제 관측 경계 | t0 / 단계 시각 (monotonic) · `du -sb` 표본과 시점 · 커밋 뒤 관측 · 바깥 반환 원문을 낸다. 내부 snapshot 과 외부 wall 은 더하지 않는다 |
| 6 미결이 없고 새 봉인을 검토 수용한 뒤, C4 실행기의 봉인 경로 · 기대 MANIFEST 를 고정 · 옛 기본 경로의 암묵적 사용 금지 | §7. 수용 뒤에 새 봉인 경로와 MANIFEST sha 를 C4 환경으로 명시 연결한다. 옛 `reil_c6_rebuild_20261013` · `SP/reil_c4env` 를 암묵적으로 쓰지 않는다 |
| 7 수용된 check 1 회를 C4 의 전체 환경 자기점검 1 회분으로 인정하는 안 | 10월 판정처럼, 같은 코드 · 환경 · 봉인 식별이 유지될 때만 인정한다. 환경이 다시 바뀌면 그 결속은 무효다 |
| 복원 규칙 1–6 | §8-3 대응표 |

**새 emit / check 가 성공해도 새 봉인을 자동 채택하지 않는다.** 결과를 검토자에게 보내고, 차이 검토가 수용된 뒤에야 C4 환경으로 연결한다.

## §5 하지 않는 것

- REIL 원자료 (`LFP_Data.xlsx`) · pickle · 노트북 개봉, 실측 자료 맞춤, E3a / H 실행, pytest 실행, 변이 증명, C5 재측정은 하지 않는다.
- **C4-A 구현** (§135 의 승인은 살아 있으나 이 실행에 포함하지 않는다) 과 COMSOL (사용자 보류) 도 하지 않는다.
- 기존 사본 정리, 옛 봉인 · 기록 · 코드 수정, 운영 (시스템) Python 에 설치하는 일도 없다.
- ensurepip 묶음은 바꾸거나 되돌리지 않는다 (읽기만).

## §6 채택 문구 (사용자 승인에 쓰는 문안 · 10월 §6 을 이 세대에 맞춘 것)

> 이 문서 (`bms-balancing/docs/REIL_C4_ENV_RESEAL_REQUEST_20261124.md`) §1 의 고정 표와 이 문서의 범위로 C4-ENV 새 환경 세대 (CPython 3.11.18) 준비 1건만 승인합니다. 기존 환경의 동일 복원이라고 표현하지 않습니다.
>
> 지정된 새 경로에서 확인된 interpreter에, 수용 봉인 lock의 전체 30개 배포판을 같은 판으로 준비합니다. wheel은 10월 기록과 이름·크기·SHA256이 같은 것만 씁니다. ensurepip pip wheel이 deb 설치 뒤 바뀐 것(`cacert.pem` 한 행)은 §1-8의 선언 행으로만 허용합니다. 사전에 명시된 별도 시험 도구 범위만 포함합니다. 기존 환경·코드·봉인·기록을 덮어쓰거나 삭제하지 않습니다.
>
> 원점 전 읽기 전용 점검 1회, **emit 1회와 check 1회만** 허용합니다. check 내부의 emit을 포함하여 **합성 COBYQA 최적화 총 2회, 전체 Sobol 생성 경로 총 2회**임을 수용합니다. 여기에는 seed/rng 비교 생성과 check의 임시 파일 쓰기도 포함됩니다. pytest·변이 시험·C5 재측정은 포함하지 않습니다.
>
> 전체 1,800초(S10의 커밋 포함)·디스크 2,000,000,000 B를 한도로 합니다. venv·다운로드·별도 시험 도구·봉인·임시 파일·기록의 새 파일을 합산합니다. 이 수치는 메모리 한도가 아니며 설치 완료 보증도 아닙니다. 미측정은 0 또는 PASS로 바꾸지 않습니다. 커밋 뒤 관측은 별도 문서 커밋으로 붙입니다.
>
> 설치 실패·배포판 집합/판/SHA 불일치·기존 경로 충돌·예산 초과·예상 밖 차이는 최초 오류와 확보된 기록을 남기고 중지합니다. 임의 재시도·패키지 판 완화·다른 interpreter·새 경로 fallback·코드 수정은 하지 않습니다.
>
> old→new 차이표와 새 MANIFEST를 제출하고 멈춥니다. 새 emit/check 성공만으로 새 봉인을 자동 채택하지 않습니다. 차이 검토가 수용된 뒤 그 봉인을 C4 환경으로 명시 연결합니다. C4-A 요청서 v4의 환경 결속(§4-3의 C6 봉인·봉인 venv)을 새 세대로 바꾸는 정정은 따로 확인받습니다.
>
> REIL 원자료·pickle·노트북 개봉, 실측 자료 맞춤, E3a/H 실행, C4-A 구현, COMSOL, 기존 사본 정리는 승인하지 않습니다.

## §7 C4-A 로 이어지는 자리 · 검토자에게 묻는 것

- **순서:** Codex 검토 → 사용자 승인 (§6) → precheck 1 회 → 재봉인 1 회 → 결과 검토 → 수용되면 C4 환경 연결 → C4-A 구현 (§135 승인 · 요청서 v4 §7 의 a 부터).
- **C4-A 쪽 결속:** 요청서 v4 §4-3 은 "C6 봉인 (`4f120948…`)" 을 입력으로 적었고, §6-2 는 "봉인된 venv (C4-ENV identity)" 를 환경으로 적었다. 새 봉인이 수용되면 이
  두 자리가 새 세대 (새 MANIFEST · `SP/reil_env18/venv` · `SP/reil_env18/pytest_t`) 를 가리켜야 한다.

| # | 질문 | 우리 안 |
|---|---|---|
| Q1 | C4-A v4 의 두 결속 자리를 새 세대로 바꾸는 일을 어떻게 확인받을까 | 결과 검토 발송문에 "v4 결속 정정 2 줄" (옛 값 → 새 값 · 그 밖 v4 바이트 그대로) 을 붙여 같은 회신에서 확인받는다. v5 를 따로 쓰지 않는다. 검토자가 v5 가 필요하다고 보면 그렇게 한다 |
| Q2 | C4-E 결과 (E1-2 · E1-3 · E3a COMPLETE · `c4a_gate` · §122) 는 3.11.17 세대에서 나왔다. 새 세대로 이월되는가 | 이 요청은 이월을 주장하지 않는다. 새 세대의 증거는 emit / check 의 합성 COBYQA 결과와 Sobol 배열이 바이트로 같은지뿐이다. 그것만으로 E3a 재현을 뜻하지 않는다. C4-A 구현 (자료 없음) 은 새 세대에서 진행하고, C4-A 실자료 실행 전에 E3a 를 새 세대에서 다시 확인할지는 그 실행 요청서에서 따로 정한다 |
| Q3 | ensurepip pip wheel 의 차이를 이렇게 다뤄도 되는가 | **A (권고):** 바뀐 묶음을 그대로 쓰되, 차이를 선언 1 행으로 정확히 묶는다 (§1-8). 10월 절차 (venv 는 ensurepip) 를 바꾸지 않는다. **B (대안 · 이 승인 밖):** `--without-pip` 로 venv 를 만들고, PyPI 의 pip 24.0 wheel (sha 가 10월 묶음 `ba0d021a…` 와 같아야 함) 로 pip 을 깐다. 절차가 10월과 달라져 새 변수 (설치 방식 · 스크립트 집합) 가 생기므로 권하지 않는다 |
| Q4 | RECORD 밖 파일을 이번 세대에서는 관측만 하고 판정에 쓰지 않는 것이 맞는가 | 맞다고 본다. 10월에 같은 관측이 없어 기준이 없다. 이번 관측을 다음 세대의 기준으로 삼을지는 결과 검토에서 정한다 |

## §8 검토 발견 대응표 (§38 의 비차단 P2 넷)

### 8-1. ENV-P2-01 — 종료 · 자원 수치의 관측 경계

| 지적 | 이 요청의 답 |
|---|---|
| 36.446 s · 556,020,307 B 가 마지막 기록 쓰기 · 커밋 전 snapshot 이었다 | 커밋 뒤 관측 (`11_after_commit.json` · 커밋 밖) + 바깥 반환 원문을 재실행 없이 문서 커밋으로 붙인다 (§1-9) |
| S10 의 별도 rc / timeout 이 없었다 · runner 가 S10 90 s 를 강제하지 않았다 | S10 도 90 s 강제 · S10 안의 호출마다 남은 몫을 timeout 으로 · S10 결과를 `10_end.json` 의 steps 에 넣는다 (§1-9 · §2-1 의 5) |
| 전체 한도를 마지막 작업 전에만 검사했다 | 자식마다 min(단계 몫, 전체 몫) · 커밋 뒤 관측으로 마지막 경계를 확인한다 |
| 디스크 값은 표본 중 최대다 | 표본 시점에 커밋 뒤를 더하고, 보고에 "표본 최대 · 연속 peak 아님" 이라고 적는다 |
| 원점 전 점검의 원문이 없었다 (편차 b) | precheck 1 회를 절차로 정하고, 원문을 S0 이 기록 폴더로 복사한다 (§2-1 의 6) |

### 8-2. ENV-P2-02 — 비교기 통과와 범용 방어력은 다르다

| 약점 (10월 도구) | 새 대조기에서 | 자체 시험 · 변이 증명 |
|---|---|---|
| `splitlines()` 가 줄바꿈 종류 · 마지막 줄바꿈을 버린다 | `parse_record` 가 줄 끝 목록을 돌려주고, 옛 원문과 그대로 대조한다 | R2 · R3 · M2 |
| RECORD 를 dict 로 만들어 중복 경로가 덮인다 | 중복 경로는 미허용이다. 행은 목록으로 순서까지 대조한다 | R4 · M1 |
| 추가 bin 행을 wheel entry point 와 결속하지 않는다 | wrapper 행은 첫 줄만 옛 경로로 되돌린 바이트가 옛 행 해시 · 크기와 같아야 한다 (본문 · 이름이 옛 수용 세대에 결속). 값이 같아 보여도 언제나 검사한다 | R5 · R6 · R7 · R14b · M3 · M11 · M12 |
| INSTALLER / REQUESTED / RECORD 허용이 해당 dist-info 로 한정되지 않는다 | 다른 dist-info 의 행은 옛 · 새 어느 쪽에 있어도 미허용이다 | R8 · M4 |
| (덧붙임) RECORD 비교 함수가 설치 파일 본문을 해시하지 않았다 | 해시 있는 행 전부를 실제 바이트 · 크기와 대조한다 (`pytest_t` 포함) | R11 · R12 · M5. wrapper 행은 wrapper 검사 안에서 새 행 ↔ 새 바이트를 따로 대조한다 (R14) |
| (덧붙임) `compare()` · `manifest_diff()` 전체 경로 시험이 없었다 | 봉인 대조를 진짜 10월 봉인 위에서 기대 변환 · 변조 사례로 시험한다 (기대 변환은 시험 쪽에서 따로 구현) | S1–S10 · M6 |

- **범위 (주장하지 않는 것):** 이 대조기는 이 세대 전용이다 (옛 · 새 경로 · 선언 행 · 충돌 · 묶음 값이 상수). "향후 임의 복원을 자동 수용하는 범용 검사기" 가 아니다.
  그렇게 쓰려면 상수를 입력으로 바꾸고 다시 검토받는다.

### 8-3. ENV-P2-03 — 복원 규칙 6 항 (검토자 §5) 을 이 요청에 채운 자리

| 규칙 | 내용 (요약) | 이 요청 |
|---|---|---|
| 1 | interpreter 파일 SHA · 판 · 빌드 · deb, 기존 절대 경로, OS / libc / 수치 라이브러리 profile, source · 도구 SHA, argv / cwd · 유효 환경을 고정. 경로 · 계수가 다르면 같은 복원이 아니다 | §1-2 · §1-3 · §1-5 · §2. 경로와 interpreter 가 다르므로 **같은 복원이 아니라 새 세대**라고 적는다. 수치 라이브러리 profile 은 PROFILE 의 BLAS / LAPACK 이 옛것과 바이트로 같아야 한다 (§1-8) |
| 2 | 설치 전 wheel 32 + ensurepip 2 를 이름 · 크기 · SHA 로 대조 · 출처 설정 제한 | S4a / b = 28 + 4 를 10월 기록과 정확 집합으로 대조한다. S0 `bundled` = ensurepip 2 를 대조하는데, pip 은 10월 sha 와 다르므로 그 차이를 선언 1 행으로 묶는다 (§0 · §7 Q3). 출처는 §1-5 |
| 3 | RECORD 30 + 4 원문 바이트 비교 · 해시 있는 행 = 실제 설치 바이트 · 해시 없는 행 · wrapper · 충돌의 허용 집합과 내용 규칙 · 외부 `pytest_t` 별도 결속. "전체 환경의 모든 바이트 동일" 이라 부르지 않음 | S9a (§1-8 의 RECORD 규칙 표). "전체 환경 바이트 동일" 이라고 쓰지 않는다. pyc 내용 · RECORD 밖 파일 · venv 의 interpreter 링크는 대조 밖이다 |
| 4 | emit 1 + check 1 · 봉인 11 파일 정확 바이트 · 합성 COBYQA 2 · Sobol 2 · 과거 check 대체 금지 · 수용 봉인 불변 · 새 출력 위치 · emit argv 경로 예외 | §1-7 · S9b. 11 파일 모두 정확한 기대 바이트로 대조한다 (변경 자리는 lock 두 자리 · PROFILE 두 값 · MANIFEST 두 값) |
| 5 | 지정 경로 · 1 회 · 1,800 s · 2,000,000,000 B · S10 포함 단일 원점 · 단계별 상한 · 실패 시 중지 · 원본 보존 · fallback 금지 · 기존 경로 삭제 / 덮어쓰기 금지 | §1-3 · §1-9 · §2 · §3 |
| 6 | 별도 사용자 승인 후에만 · 어느 식별이든 다르면 설치 전 / 발견 즉시 중지 · 새 세대인지 재검토 | 이 요청 자체가 그 재검토다. §6 의 사용자 승인 뒤에만 한다. precheck · S0 · S4 에서 식별이 다르면 설치 전에 멈춘다 |

### 8-4. ENV-P2-04 — 실제 패키지 출처는 독립 관측 미완

| 지적 | 이 요청의 답 |
|---|---|
| 남은 환경에 pip source 옵션이 있었는지 증거가 없다 | `PIP_*` 는 `PIP_CERT` 하나만 물려받는다. 나머지는 빼고 이름을 기록한다. 자식 env 이름 전체도 단계마다 기록한다 (§1-5) |
| 다운로드 로그에 실제 index URL / endpoint 가 없다 | `--index-url` 을 argv 에 명시한다. `Downloading` 줄의 꼴 (이름 꼴 = `files.pythonhosted.org`) 을 세어 보고한다 (§1-5) |
| `PIP_CONFIG_FILE=/dev/null` 은 설정 파일만 끈다 | 위 env 규칙이 환경 변수 쪽을 막는다 |
| 독립 네트워크 감사가 아니다 | 그대로 한계로 적는다 (§1-5) |

## §9 이 요청 전에 한 것 (읽기 · 대조기 · 자체 시험)

- **읽기만 한 관측** (`evidence/reil_c4_env_reseal_pre_20261124/` · 2026-11-24T10:58Z):
  - `01_interpreter.txt` 는 ls · stat · sha256 · file · `sys.version` · `python_build` · 컴파일러 · libc · `ensurepip.version()` · ensurepip / venv 소스 sha 다.
  - `02_dpkg.txt` 는 deb 판 10 · 묶음 소유 · `dpkg -V` · deb md5 기대 · 실제 md5 · 묶음 디렉터리 시각이다.
  - `03_bundled_check.json` 은 대조기 `bundled` 의 결과다 (rc 0 · 허용만 · pip 의 선언 1 행).
  - `04_cacert_member.txt` 는 바뀐 구성원의 크기 · sha · 인증서 블록 비교다.
  - `05_env_names.txt` 는 환경 변수 **이름만** 과 pip 설정 파일 후보 4 곳의 유무다.
  - `06_paths_disk.txt` 는 새 경로 부재 · `df -B1` 이다.
- **대조기** `scripts/reil_c4_env_reseal_check.py` (`8cf10f3c…dbedb0`).
- **자체 시험** (`evidence/reil_c4_env_reseal_selftest_20261124/`):
  - `selftest.py` (`dc1d4eb9…875d`) 는 **52 / 52 PASS** 다 (rc 0 · 2026-11-24T10:57:18Z–10:57:22Z).
  - 그룹은 P1–P3 (10월 원문 34 의 파싱 · 줄 끝 CRLF · lock 결속) · R1–R20 + R14b (합성 venv / `pytest_t`) · S1–S10 (진짜 10월 봉인 위의 기대 변환 · 변조) · B0–B6
    (지금 묶음 · 합성 wheel) · W0–W5 · C1–C3 (CLI · 덮어쓰기 거부 · 고정 경로) 이다.
- **변이 증명** (`mutation_proof.py` · `8a1200f4…acc2`):
  - 대조기의 검사 자리를 하나씩 끈 사본 12 개 + 대조군 1 개를 저장소 밖 임시 거울에서 돌린다.
  - **1 차 (`run1_*` 보존) 는 11 / 12 였다.** M3 (wrapper 본문 결속 끔) 에서 기대한 R14 가 FAIL 하지 않았다. R14 는 RECORD↔바이트 검사로도 잡히는 사례였고,
    `pytest_t` 쪽 본문 결속만 겨냥한 사례는 없었다. 규율 2 의 "처음부터 통과한 시험은 fixture 가 진실을 가린 신호" 그대로다.
  - 그래서 R14b (본문을 바꾸고 RECORD 도 맞춘 사례) 와 M12 (`../../bin` 대응 끔) 를 더했다. 대조기 코드는 바꾸지 않았다.
  - **2 차는 13 / 13 기대대로**다 (rc 0 · 10:57:22Z–10:58:21Z).
- **하지 않은 것:** venv · pip · 설치 · 내려받기 · emit · check · 네트워크 (PyPI) · pytest · 저장소 안 pyc 쓰기 (`-B`) 는 모두 0 이다.
