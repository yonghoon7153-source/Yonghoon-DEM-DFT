# REIL C4-ENV (새 환경 세대 준비) 승인 요청 — 검토자 초안의 고정 표를 채운 판 · 2026-10-13

> **승인 요청문이다.** 사용자 승인 전에는 venv 생성 · 내려받기 · 설치 · emit · check 를 하지 않는다 (0 회). 지금까지 한 것은 읽기뿐이다:
> interpreter 식별 · 파일 해시 · 경로가 없는지 확인 · 디스크 관측. 그리고 대조 스크립트 작성과 그 자체 확인 (합성 자료 · 커밋된 봉인 두 개만 · §1-8).
> 틀은 검토자 비활성 초안 `bms-balancing/reviews/prereview_reil_c4_20261013/originals/ENV_APPROVAL_DRAFT_KO.md` (sha256 `012c958427654447…86a4`) 이다. 초안의 "승인 전에 실행 측이
> 채울 고정 표" 9 항목을 §1 에 채웠고, 채택 문구 (§6) 는 초안 문구에 이 문서의 표 참조만 붙였다. 근거: 상태 문서 `REIL_PREREQUISITES_STATUS_20261004.md`
> §35 · 사전 검토 발견 C4-N1 (P1).
> **이것은 기존 환경의 동일 복원이 아니다.** CPython 3.11.15 (2026-03-03 빌드) 환경은 컨테이너 교체로 없어졌다. 이 요청은 현재 interpreter
> (3.11.17) 에 같은 판의 배포판을 까는 **새 환경 세대**다. 이전 봉인 · P0 / C5 기록은 고치지 않는다.

## §1 고정 표 (초안의 9 항목)

### 1-1. 저장소 HEAD · 보호할 원본

- 시작 HEAD 는 이 요청문 · 승인 기록 · 보존 규칙이 든 커밋 (그 뒤 문서만 바뀐 커밋 포함) 이다. 실행 기록에 40 자로 적는다. 그 사이에
  `bms-balancing/scripts/` · `degradation-degeneracy/tools/env_profile.py` · 아래 보호 경로가 바뀌었으면 시작하지 않는다.
- 아래 보호 경로는 시작과 끝에 대조한다. 바뀌면 실패다.

| 보호 경로 | 식별 (현재 HEAD `0c04751f…` 의 git tree · 파일 sha256) |
|---|---|
| `bms-balancing/reil_c6_20261005/` | tree `3ec46373da366265242e92df9c6e112e5ff100e0` (MANIFEST sha256 `e4adba0fed22e51de37d98067a623e2e3e9575cc9e1ea039a3a88363e2378e9f`) |
| `bms-balancing/reil_c6_rebuild_20261006/` | tree `b55f3a439e23bd41626d64bbb40b8221571f8690` (MANIFEST `a14617ecad1954a86122922072b8d1656e9b13fdbf003d131ad32e0ff52a91f5`) |
| `bms-balancing/evidence/reil_c6_n1_20261006/` | tree `fdd12a5f30dc52242e0553b6b616c463a264fe54` |
| `bms-balancing/evidence/reil_p0_20261006/` | tree `82a74d69c3f3cad363d6f120fe0e88658af0a496` |
| `bms-balancing/evidence/reil_c5_impl_20261006/` | tree `cfea813242c2d47f559a3807c5bab1bb63f3e183` |
| `bms-balancing/evidence/reil_c5_pilot_20261006/` · `…_wrapper/` | tree `514e4dcd284f831a92e158ad4542136cc455f018` · `6238fff9ff7bc6a54747f28653eca4e3f1b20a2d` |
| `bms-balancing/scripts/reil_c6_profile.py` | `408afc4bb5eb1069583b955e0eb6215bf48dd9259ad474c230549d1b3642df5d` |
| `degradation-degeneracy/tools/env_profile.py` | `83b0d8365d039d75050d087fe980ad7b64818686b699e5d06da1c0ad63148563` (옛 lock 머리줄에 적힌 sha 와 같다) |
| `bms-balancing/scripts/reil_c4_env_compare.py` (§1-8) | `eff94d3dfd4b3d31c7a19e440dfb968734dab1afb16b584c2fdee354100695e0` |
| `bms-balancing/scripts/reil_c5_pilot.py` | `73bee8dc412b39863afb64b70bc128cbecee2075a3a17914fc7288f353ef11a6` (이 단계에서 부르지 않는다 · 보호만) |

- 작업트리 원문 (`git status --porcelain=v1 --untracked-files=all`) 은 시작과 끝에 그대로 보존한다. 분류 결과와 따로 둔다.

### 1-2. interpreter

| 항목 | 지금 값 (2026-10-13T05:19Z · 읽기만) | 옛 값 (C5 `evidence/reil_c5_impl_20261006/04_identity.json` · 봉인 PROFILE) |
|---|---|---|
| 경로 | `/usr/bin/python3.11` (일반 파일 · 심볼릭 링크 아님 · 6,644,312 B) | `/usr/bin/python3.11` |
| 파일 sha256 | `73bf4b06fad87996a59b3c0810eb127b91e84846d21e563862fb4acf74fbcb99` | 기록 없음 |
| 판 · 빌드 | `3.11.17` · `["main", "Oct  1 2026 15:41:07"]` | `3.11.15` · `["main", "Mar  3 2026 09:26:23"]` (GCC 13.3.0) |
| 구현 · 플랫폼 · libc | CPython · Linux x86_64 · glibc 2.39 | 같음 |
| 배포 꾸러미 | deb `python3.11-minimal` · `libpython3.11-stdlib` · `python3.11-venv` = `3.11.17-1+noble1`. apt 원천 기록은 남아 있지 않다. `+noble1` 접미사는 deadsnakes 관례로 보이지만 확인하지 않았다 | 기록 없음 |
| ensurepip 묶음 (venv 의 pip · setuptools 원천) | `/usr/lib/python3.11/ensurepip/_bundled/pip-24.0-py3-none-any.whl` (sha256 `ba0d021a166865d2265246961bec0152ff124de910c5cc39f1156ce3fa7c69dc`) · `…/setuptools-79.0.1-py3-none-any.whl` (`e147c0549f27767ba362f9da434eab9c5dc0045d5304feb602a0af001089fc51`) | lock 의 pip 24.0 · setuptools 79.0.1 (같은 판 · 옛 wheel sha 는 기록 없음) |

- S0 에서 다시 잰다. 위 값과 하나라도 다르면 시작하지 않고 재확인을 요청한다.

### 1-3. 정확한 경로

모두 지금 없다 (2026-10-13 확인). S0 에서 하나라도 있으면 중지한다. 덮어쓰기 · 다른 이름으로 바꾸기 (fallback) 는 없다.
`SP` = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad` (세션 스크래치 · 저장소 밖 · 저장소와 같은
파일시스템 `/dev/vda`).

| 용도 | 경로 |
|---|---|
| 작업 뿌리 | `SP/reil_c4env/` |
| 과학 venv | `SP/reil_c4env/venv/` |
| 과학 wheel (내려받기) | `SP/reil_c4env/wheels/` |
| 시험 도구 wheel | `SP/reil_c4env/wheels_test/` |
| 시험 도구 설치 (venv 밖) | `SP/reil_c4env/pytest_t/` |
| 임시 (pip · check 의 `TemporaryDirectory`) | `SP/reil_c4env/tmp/` (`TMPDIR`) |
| 새 봉인 (저장소) | `bms-balancing/reil_c6_rebuild_20261013/` |
| 기록 (저장소) | `bms-balancing/evidence/reil_c4_env_20261013/` (RECORD 원문 30 은 그 아래 `09_records/`) |

- pip 캐시는 쓰지 않는다 (`--no-cache-dir`). pip 설정 파일도 읽지 않는다 (`PIP_CONFIG_FILE=/dev/null`). 지금 환경 변수가 가리키는
  `/root/.config/pip/pip.conf` 은 없고, `/etc/pip.conf` 등 다른 설정 파일도 없다. 홈 · 시스템 경로에는 쓰지 않는다.
- **venv 경로를 옛 `SP/reil_p0/venv` 로 두지 않는 이유:** C5 기록이 그 경로를 3.11.15 환경으로 적고 있다. 같은 경로 문자열이 두 세대를
  가리키지 않게 한다.
- **뿌리 이름을 짧게 (`reil_c4env`) 한 이유:** pip 는 콘솔 스크립트 첫 줄에 venv python 의 절대 경로를 쓴다. 그 줄이 127 B 를 넘으면
  `/bin/sh` 를 거치는 다른 형식으로 쓴다. 옛 venv 는 116 B 이하라 보통 형식이었다. `reil_c4env` 는 `python` 119 B · `python3.11` 123 B 라
  옛 형식과 같다. `reil_c4_env_20261013` 이었으면 129 · 133 B 라 형식이 달라졌을 것이다.
- 경로가 바뀌므로 콘솔 스크립트를 가진 배포판의 RECORD 는 다르다. 원인은 §19 와 같다. 허용 조건은 §1-8.

### 1-4. 과학 lock 30 · 설치 고정 목록

- 기준 lock: `bms-balancing/reil_c6_rebuild_20261006/REIL_C6.lock.txt` (sha256 `b392f7b01f9492337a4c52ef323d9348af076866e6997d96179bc438375fe9ef`).
  30 배포판 = about-time 4.2.1 · alive-progress 3.3.0 · autograd 1.9.1 · cffi 2.1.1 · cma 4.5.0 · contourpy 1.3.3 · cycler 0.12.1 ·
  deprecated 1.3.1 · et-xmlfile 2.0.0 · fonttools 4.66.1 · graphemeu 0.7.2 · kiwisolver 1.5.1 · matplotlib 3.11.2 · moocore 0.3.2 · numpy 2.4.6 ·
  openpyxl 3.1.5 · packaging 26.3 · pandas 3.0.5 · pillow 12.3.0 · pip 24.0 · platformdirs 4.12.3 · pycparser 3.0 · pymoo 0.6.2 · pyparsing 3.3.3 ·
  python-dateutil 2.9.0.post0 · scipy 1.17.1 · seaborn 0.13.2 · setuptools 79.0.1 · six 1.17.0 · wrapt 2.5.0.
- 설치 고정 목록 (`-c`): `bms-balancing/evidence/reil_p0_20261006/01_venv_constraints.txt` (sha256
  `db63333bdaf1835444a86187215ed7faf06897eb8a247c667ed167a5ee1dc772`). 이 28 줄 (30 에서 venv 가 가져오는 pip · setuptools 를 뺀 것) 은 P0 재구축이
  그 lock 을 만들 때 쓴 그대로다. 새로 쓰지 않고 읽기만 한다.
- 최상위 요청 7 (P0 설치 로그 `01_venv_pip_install.stdout` 의 처음 7 개 Collecting 과 같은 순서): `numpy==2.4.6 scipy==1.17.1 pandas==3.0.5
  openpyxl==3.1.5 matplotlib==3.11.2 seaborn==0.13.2 pymoo==0.6.2`. pip 는 최상위로 요청된 배포판에만 RECORD 에 `REQUESTED` 행을 넣는다.
  그래서 요청 집합도 같게 둔다.
- 업그레이드 · 추가 패키지 · 판 완화는 없다. 소스 빌드도 없다 (`--only-binary=:all:`).

### 1-5. 설치 원천 · 네트워크 · argv · 아티팩트 기록

- **원천:** PyPI 기본 색인 `https://pypi.org/simple` (설정 파일 0). 에이전트 프록시를 거친다. 프록시 주소와 CA 는 이미 환경에 있는 값을 쓰고
  (`HTTPS_PROXY` · `PIP_CERT`) 문서에 옮기지 않는다. 허용 호스트는 `pypi.org` · `files.pythonhosted.org` 둘뿐이다. pip · setuptools 는
  interpreter 의 ensurepip 묶음 (§1-2) 에서 오므로 네트워크를 쓰지 않는다.
- **두 단계로 나눈다** (초안: "다운로드 바이트 식별과 설치 후 RECORD 대조를 구분"):
  1. 내려받기 (S2 · S3). 내려받은 파일 전부의 이름 · 크기 · sha256 을 S4 에서 적는다.
     - 과학 wheel 은 **파일 이름 집합**이 P0 설치 로그의 wheel 이름 28 개와 정확히 같아야 한다. 이 기대 목록은 손으로 쓰지 않고 그 로그에서
       읽는다 (부록 A).
     - 시험 도구는 옛 파일 이름 기록이 없다. 그래서 `이름==판` 집합 4 개와 "모두 wheel" 로 대조한다.
     - 다르면 설치 전에 중지한다.
  2. 설치 (S5 · S6). `--no-index --find-links` 로 1 의 파일만 쓴다. 네트워크는 0 이다.
- **정확 argv** 는 §2 표에 있다. 모든 명령의 argv · cwd · env · 시작 / 끝 시각 · rc · stdout / stderr 원문을 기록에 남긴다.

### 1-6. 시험 도구

- 이전 `SP/reil_p0/pytest_t` 는 컨테이너 교체로 없다. 게다가 **그 배포판 · 판은 어디에도 기록되지 않았다.** C5 · P0 시험 로그는 `-q`
  출력이라 머리줄이 없고, 문서에도 판이 없다. 그래서 식별해서 재사용할 수 없고, 새로 준비한다.
- **판:** pytest 9.1.1 · pluggy 1.6.0 · iniconfig 2.3.0 · pygments 2.21.0. 이 저장소의 검증 환경 기록
  `degradation-degeneracy/requirements-validation-C.lock.txt` 의 62 · 123 · 138 · 143 행에 있는 판 그대로다 (임의의 최신판이 아니다).
  - `packaging` 은 과학 venv 의 26.3 을 쓴다. lock 안에 있고, C lock 의 판과도 같다. 따로 깔지 않는다.
  - Python 3.11 이라 `exceptiongroup` · `tomli` 는 필요 없다. `colorama` 는 Windows 전용이다.
- **위치:** `SP/reil_c4env/pytest_t/` (`pip install --target` · `--no-deps`). **과학 venv 에 넣지 않는다** (lock 30 불변). 쓸 때는
  `PYTHONPATH=SP/reil_c4env/pytest_t` 로 붙인다 (C5 부록 38 행과 같은 방식). `reil_c6_profile._site_packages()` 는 venv 접두사 안의
  site-packages 만 재므로, 이 경로는 lock 에 들어가지 않는다. emit / check 때는 `PYTHONPATH` 를 두지 않는다.
- **식별 기록:** wheel 4 개의 이름 · 크기 · sha256 (S4). 설치된 `*.dist-info/RECORD` 4 개의 sha256 과 원문 (S10).
- **이 단계에서 pytest 를 실행하지 않는다.** 첫 실행은 C4-0 의 RED 다.
- 디스크 · 시간은 아래 합계에 넣는다.

### 1-7. 프로필 스크립트 · emit / check

- `bms-balancing/scripts/reil_c6_profile.py` (sha256 `408afc4b…df5d`). 부르는 저장소 소스는 `degradation-degeneracy/tools/env_profile.py`
  (`83b0d836…8563` · `spec_from_file_location`) 하나다.
- emit: cwd `/home/user/Yonghoon-DEM-DFT` · env `TMPDIR=SP/reil_c4env/tmp PYTHONDONTWRITEBYTECODE=1` · argv
  `SP/reil_c4env/venv/bin/python bms-balancing/scripts/reil_c6_profile.py emit bms-balancing/reil_c6_rebuild_20261013`.
- check: 위와 같고 `emit` 자리에 `check` 를 쓴다. 기대 출력은 `check OK` · rc 0 이다.
- 위 꼴은 옛 P0 재구축의 `evidence/reil_p0_20261006/02_emit.meta.txt` · `03_check.meta.txt` 와 같다. 봉인 경로와 env 두 개만 다르다.
  - `TMPDIR`: check 의 임시 폴더를 정해진 경로에 두어 디스크 합산에 넣는다.
  - `PYTHONDONTWRITEBYTECODE`: `env_profile.py` 를 읽을 때 `degradation-degeneracy/tools/__pycache__/` 에 쓰지 않게 한다. `source_digest` 는
    `__pycache__` 를 빼지만, 저장소 안 쓰기 자체를 없앤다.
  - 둘 다 봉인 바이트에는 영향이 없다. `env_profile` · `reil_c6_profile` 은 interpreter 플래그 · 환경 변수를 읽지 않는다 (정적 확인).
- **실제 계산 (C4-N1 그대로 수용):**
  - emit 1 회 = lock 측정 (설치 파일 ↔ RECORD 해시 대조) + PROFILE + **합성 이차 함수의 COBYQA 최적화 1 회** + **Sobol 경로 1 벌** (주 생성
    seed 0 · 1 → 단위 · 상자 2 = 배열 6, 옛 인자 비교용 생성 4 회 포함).
  - check 1 회 = 봉인 해시 대조 + 임시 폴더에서 emit 1 회 전부 다시 + 바이트 대조.
  - 합계 = **합성 COBYQA 2 회 · Sobol 경로 2 벌** · REIL 자료 0.

### 1-8. 허용 old→new 차이 (옛 = `bms-balancing/reil_c6_rebuild_20261006/`)

| 파일 | 옛 sha256 | 허용하는 차이 (이것만) | 그 밖 |
|---|---|---|---|
| `REIL_C6.lock.txt` | `b392f7b0…e9ef` | (1) `#@ python "3.11.15"` → `#@ python "3.11.17"` 한 줄. (2) RECORD sha 가 다른 배포판 집합이, 새 venv 에서 RECORD 에 `../../../bin/` 행이 있는 배포판 집합과 정확히 같을 때. 이것은 §19 규칙 (i) 이고, 기대 집합은 cffi · fonttools · numpy · pip 다. 그리고 그 배포판마다 아래 RECORD 행 대조를 통과해야 한다 | 아래가 하나라도 바이트 동일이 아니면 미허용: 30 배포판 집합 · 판 · 머리 3 줄 (env_profile sha 포함) · `#@ implementation/system/machine/libc` · `#@ files` 집계 (7187 / 5301 / 1 / 1) · `#@ collision` 줄 · `#@ dists_without_record []` |
| `PROFILE.json` | `c9449c28…191d` | `python.version` `"3.11.15"` → `"3.11.17"` 와 `python.build` `["main", "Mar  3 2026 09:26:23"]` → `["main", "Oct  1 2026 15:41:07"]` (S0 재확인 값) 두 값만. 판정은 이 두 값만 바꾼 옛 PROFILE 을 같은 직렬화로 다시 만들어 새 파일과 **바이트 동일**한지로 한다 | BLAS / LAPACK (numpy scipy-openblas 0.3.31.188.0 · scipy 0.3.30) · libc · packages 7 · COBYQA 1.1.3 · 형식 등 한 바이트라도 다르면 미허용 |
| `COBYQA_OPTIONS.json` | `0317d11b240a948f86b75f049a75cef59a6673a7585fb32f8257901d99b9ee14` | 없음 (옵션 8 · 구현 파일 4 의 sha · 합성 호출 결과) | 미허용 |
| `SOBOL_PHASE_A.json` | `887654728fc3d58c4a7c596e3254560a2d48a07dca0e1a50d7d4da007e18cc52` | 없음 (배열 6 의 raw float64 sha · .npy sha · 서명 · 경고 · 옛 인자 비교) | 미허용 |
| `.npy` 6 | `916ac373…` (A0 s0) · `0e8dacca…` (A0 s1) · `2e7ba141…` (A1A2 s0) · `72a33726…` (A1A2 s1) · `e8ca4cc0…` (unit s0) · `870eec2c…` (unit s1) — 전체는 옛 MANIFEST | 없음 | 미허용 |
| `MANIFEST.json` | `a14617ec…91f5` | 키 집합이 같고 lock · PROFILE 두 항목 값만 다르며, 새 MANIFEST 가 새 파일들과 맞을 때 | 미허용 |

- **RECORD 행 대조** (미상의 RECORD 차이를 포괄 수용하지 않기 위해 · 읽기와 해시만):
  - 30 배포판 각각에서, wheel 안 `*.dist-info/RECORD` 에 있는 행은 설치된 RECORD 에 경로 · 해시 · 크기가 같은 채로 있어야 한다.
  - 설치된 RECORD 에서 wheel 에 없는 행은 pip 가 만드는 것뿐이어야 한다: `../../../bin/*` · `INSTALLER` · `REQUESTED` · 해시 없는
    `__pycache__/*.pyc` · `RECORD` 자신.
  - `../../../bin/*` 의 첫 줄은 `#!` 다음에 새 venv 의 절대 경로가 와야 한다 (원인 확인).
  - pip · setuptools 는 ensurepip 묶음 wheel (§1-2 의 sha) 과 대조한다.
  - 30 RECORD 원문은 전부 기록에 보존한다. 각 원문을 env_profile 식으로 읽은 sha 가 새 lock 의 그 배포판 record-sha256 과 같아야 한다 (결속).
  - 이로써 §19 의 한계 ("옛 RECORD 원문이 없어 직접 대조 못 함") 는 다음 세대부터 닫힌다.
- **도구:** `bms-balancing/scripts/reil_c4_env_compare.py` (sha256 `eff94d3d…95e0` · stdlib 만 · 시스템 python `-I` 로 실행 · 과학 패키지 import 0).
  - `artifacts` = S4. `compare` = S9 (위 표 · RECORD 행 대조 · 결속). 허용 밖이 있으면 rc 1.
  - **자체 확인 23 / 23** (2026-10-13 · 합성 자료와 커밋된 봉인 두 개만): `evidence/reil_c4_env_compare_selftest_20261013/`. 내용은 셋이다.
    1. P0 로그에서 wheel 이름 28 개를 읽는다. 과학 wheel 의 집합이 다르거나, 시험 도구 판이 다르거나, sdist 가 섞이면 잡는다.
    2. 옛 두 봉인 (`reil_c6_20261005` → `rebuild_20261006`) 대조. `record_sha_differs` 가 정확히 cffi · fonttools · numpy · pip 로 나온다.
       `#@ collision` 줄 변화는 이 규칙에서 미허용으로 잡는다. 다음 넷도 미허용으로 잡는다: python 줄의 예상 밖 판 · 판 변경 · `#@ files`
       집계 변경 · PROFILE 의 libc · BLAS · 형식 변경.
    3. 합성 venv · wheel 의 RECORD 행 대조. 깨끗한 경우는 통과한다. 다음 넷은 잡는다: 해시 변조 · `direct_url.json` 행 · 해시 있는 pyc ·
       다른 venv 의 첫 줄. CRLF 를 정규화한 RECORD sha 가 원문 sha 와 다른 것도 확인했다.
- "미허용" 이면 성공으로 채택하지 않는다. 그 자리에서 멈추고, 원문을 보존하고, 보고한다.
- Python 판 · 빌드 변화는 위 두 자리로만 허용한다. libc · BLAS · 옵션 · 배열 · 그 밖 RECORD 의 미상 차이는 포괄 승인하지 않는다 (초안
  그대로).

### 1-9. 시간 원점 · 배정 · 디스크

- **원점 t0** = S0 의 첫 명령 직전이다. UTC 와 monotonic 둘 다 기록한다. 승인 기록과 보존 규칙 커밋은 t0 전에 한다 (문서다).
- **전체 한도 1,800 s** = t0 부터 S10 끝 (로컬 커밋 포함) 까지다. push 는 한도 밖이고 기록만 한다.
- **단계별 배정:** §2 표의 timeout 이다. 합계는 정확히 1,800 s 이고, 남은 시간을 다른 단계로 자동으로 돌리지 않는다.
- **디스크 한도 2,000,000,000 B:** `du -sb` (겉보기 바이트) 로 다음 셋을 합산한다.
  - `SP/reil_c4env/` (venv · wheel 둘 · 시험 도구 · 임시)
  - 새 봉인
  - 기록
- **관측:** S2 · S3 · S5 · S6 · S8 · S10 끝마다 적는다. 넘으면 그 자리에서 중지한다. `df -B1` 여유는 시작과 끝에 참고로만 적는다 (한도 아님).
  이 수치는 메모리 한도가 아니고, 설치 완료를 보증하지도 않는다. 재지 못한 값을 0 이나 PASS 로 바꾸지 않는다.
- **시작 조건:** 여유 ≥ 4,000,000,000 B (한도의 2 배). 지금 관측은 27,106,410,496 B (2026-10-13T05:19Z · 제출자 관측) 이고, S0 에서 다시 잰다.
- **실패하면:** 만든 파일을 지우지 않는다 (정리 승인 없음 · 스크래치는 세션과 함께 사라진다). 저장소 쪽 (부분 봉인 · 기록) 은
  "정지 상태의 기록 · 채택 아님" 으로 커밋한다 (§18 선례).

## §2 순서 · 정확 argv

- 공통 env: `TMPDIR=SP/reil_c4env/tmp`. pip 단계에는 `PIP_CONFIG_FILE=/dev/null` 도 둔다.
- cwd 는 저장소 뿌리 `/home/user/Yonghoon-DEM-DFT` 다.
- `V` = `SP/reil_c4env/venv/bin/python` · `C` = `bms-balancing/evidence/reil_p0_20261006/01_venv_constraints.txt` · `P` = `/usr/bin/python3.11 -I`
  · `E` = `bms-balancing/evidence/reil_c4_env_20261013`.

| 단계 | 명령 (argv) | timeout | 네트워크 |
|---|---|---|---|
| S0 사전 대조 (읽기만) | HEAD · porcelain 원문 · §1-2 재측정 · §1-1 보호 대조 · §1-3 경로 부재 · `df -B1`. 그다음 `mkdir SP/reil_c4env SP/reil_c4env/tmp E` (이미 있으면 실패) · 시작 기록 | 60 s | 0 |
| S1 venv | `/usr/bin/python3.11 -I -m venv SP/reil_c4env/venv` | 120 s | 0 |
| S2 과학 내려받기 | `V -I -m pip download --no-cache-dir --disable-pip-version-check --only-binary=:all: --dest SP/reil_c4env/wheels -c C numpy==2.4.6 scipy==1.17.1 pandas==3.0.5 openpyxl==3.1.5 matplotlib==3.11.2 seaborn==0.13.2 pymoo==0.6.2` | 480 s | PyPI |
| S3 시험 도구 내려받기 | `V -I -m pip download --no-cache-dir --disable-pip-version-check --only-binary=:all: --no-deps --dest SP/reil_c4env/wheels_test pytest==9.1.1 pluggy==1.6.0 iniconfig==2.3.0 pygments==2.21.0` | 120 s | PyPI |
| S4 아티팩트 식별 | `P bms-balancing/scripts/reil_c4_env_compare.py artifacts --wheels SP/reil_c4env/wheels --expect-log bms-balancing/evidence/reil_p0_20261006/01_venv_pip_install.stdout --out E/04_artifacts_science.json`. 그리고 `… artifacts --wheels SP/reil_c4env/wheels_test --expect-dists pytest==9.1.1,pluggy==1.6.0,iniconfig==2.3.0,pygments==2.21.0 --out E/04_artifacts_test.json`. rc ≠ 0 이면 설치 전 중지 | 30 s | 0 |
| S5 과학 설치 | `V -I -m pip install --no-cache-dir --disable-pip-version-check --no-index --find-links SP/reil_c4env/wheels -c C numpy==2.4.6 scipy==1.17.1 pandas==3.0.5 openpyxl==3.1.5 matplotlib==3.11.2 seaborn==0.13.2 pymoo==0.6.2` | 300 s | 0 |
| S6 시험 도구 설치 | `V -I -m pip install --no-cache-dir --disable-pip-version-check --no-index --find-links SP/reil_c4env/wheels_test --no-deps --target SP/reil_c4env/pytest_t pytest==9.1.1 pluggy==1.6.0 iniconfig==2.3.0 pygments==2.21.0` | 120 s | 0 |
| S7 emit | §1-7 (env `PYTHONDONTWRITEBYTECODE=1` 추가) | 180 s | 0 |
| S8 check | §1-7 · `check OK` · rc 0 | 180 s | 0 |
| S9 old→new 대조 (읽기 · 해시만) | `P bms-balancing/scripts/reil_c4_env_compare.py compare --old bms-balancing/reil_c6_rebuild_20261006 --new bms-balancing/reil_c6_rebuild_20261013 --venv SP/reil_c4env/venv --wheels SP/reil_c4env/wheels --wheels /usr/lib/python3.11/ensurepip/_bundled --python-version 3.11.17 --python-build 'main\|Oct  1 2026 15:41:07' --records-out E/09_records --out E/09_old_new_diff.json` | 120 s | 0 |
| S10 기록 · 커밋 | 다음을 기록한다: 시험 도구 RECORD 4 의 sha256 과 원문 (`E/10_test_tool_records/`) · `du -sb` · `df -B1` · 끝 porcelain 원문 · §1-1 보호 대조 · 끝 시각. 그다음 `git add -f` (새 봉인 · 기록) 와 로컬 커밋 | 90 s | 0 |

- S9 의 `--python-version` · `--python-build` 는 S0 에서 다시 잰 값이 §1-2 와 같을 때만 이 값으로 둔다. 다르면 S0 에서 이미 멈춘다.
  표 안의 `\|` 는 마크다운 표 때문에 붙은 것이다. 실제 인자는 `main|Oct  1 2026 15:41:07` 이다 (Oct 와 1 사이 공백 둘).
- 위 명령 외에 다른 설치 · 실행은 없다. pytest · 변이 증명 (`reil_c6_mutation_proof.py`) · C5 재측정 · REIL 자료는 포함하지 않는다.

## §3 중지 조건 (그 자리에서 멈춤 · 첫 오류와 확보된 기록 보존 · 재시도 0)

1. S0 사전 조건 실패: HEAD · 보호 · interpreter · 경로 · 여유 디스크.
2. 어느 단계든 rc ≠ 0 이거나 timeout.
3. S4 의 이름 · 판 집합 불일치 (설치 전).
4. 디스크 관측 > 2,000,000,000 B, 또는 t0 부터 1,800 s 초과.
5. S8 check 가 OK 가 아님 (새 환경 안에서도 재현이 안 된다는 뜻).
6. S9 에 미허용 차이 (§1-8). 채택하지 않고, 정지 상태 기록으로 커밋한다.
7. S10 에서 보호 경로가 바뀌었음. 실패로 보고한다.

다음은 하지 않는다: 임의 재시도 · 패키지 판 완화 · 다른 interpreter · 새 경로로 바꾸기 · 코드 수정. 실패 뒤 다음 걸음은 사용자에게
다시 묻는다.

## §4 결과 제출 · 수용 (초안의 7 조건 대응)

| 초안 조건 | 이 요청에서 |
|---|---|
| 1 승인 원문 · 고정 표 · 명령 · cwd · 원점 · 시작 / 끝 HEAD · 작업트리 목록 보존 | `E/00_*` (승인 원문 사본 · 이 문서 sha · t0) · 단계별 meta (argv · cwd · env · 시각 · rc) · porcelain 원문 시작 / 끝 |
| 2 과학 배포판 전체 · Python 판 / 빌드 · 플랫폼 / libc · BLAS / LAPACK · RECORD · 파일 대조 · 충돌 표를 old / new 나란히 | `E/09_old_new_diff.json` 을 결과 보고서의 사람용 표로 옮긴다. lock `#@ files` 집계와 collision 줄도 포함한다 |
| 3 COBYQA 옵션 8 · 구현 파일 4 · Sobol 6 의 .npy sha 와 raw payload sha 를 각각 대조 | `COBYQA_OPTIONS.json` · `SOBOL_PHASE_A.json` · `.npy` 6 의 바이트 동일 판정. 보고서 표에는 sha 쌍을 하나씩 적는다 |
| 4 새 봉인과 옛 봉인을 각각 독립 식별 · 새 lock 을 과거 C5 가 썼다고 소급 기록 금지 | 새 MANIFEST · lock · PROFILE 의 sha 를 따로 적는다. 옛 봉인 · C5 기록은 바이트 그대로 둔다 |
| 5 시간 · 디스크 · 최종 기록의 실제 관측 경계 | t0 / 단계 시각 (monotonic) · `du -sb` 관측 시점 · 마지막 관측이 S10 의 어디였는지 적는다. 내부 snapshot 과 외부 wall 을 더하지 않는다 |
| 6 미결이 없고 새 봉인을 검토 수용한 뒤, C4 실행기의 봉인 경로 · 기대 MANIFEST 를 고정 · 옛 기본 경로의 암묵적 사용 금지 | C4-0 구현 항목이다. `reil_c5_pilot.py` 60 행 `SEALED = …/reil_c6_rebuild_20261006` 같은 상수를 그대로 물려받지 않고, 새 봉인의 경로와 MANIFEST sha 를 명시 인자로 받게 한다 (C4 요청 v2 §4) |
| 7 수용된 check 1 회를 C4 전체 환경 자기점검 1 회분으로 인정하는 안 | C4 요청 v2 §4-6 · §5-5. 같은 코드 · 환경 · 봉인 식별이 유지될 때만이다. 환경이 다시 바뀌면 그 결속은 무효다 |

**새 emit / check 가 성공해도 새 봉인을 자동 채택하지 않는다.** 결과를 검토자에게 보내고, 차이 검토가 수용된 뒤에야 C4 환경으로 연결한다.

## §5 하지 않는 것

REIL 원자료 (`LFP_Data.xlsx`) · pickle · 노트북 개봉 · 실측 자료 맞춤 · E3a / H 실행 · pytest 실행 · 변이 증명 · C5 재측정 · COMSOL · 기존
사본 정리 · 옛 봉인 / C5 원문 / 코드 수정 · 운영 (시스템) Python 에 설치.

## §6 채택 문구 (초안 그대로 + 고정 표 참조)

> 이 문서 (`bms-balancing/docs/REIL_C4_ENV_APPROVAL_REQUEST_20261013.md`) §1 의 고정 표와 이 문서의 범위로 C4-ENV 새 환경 준비 1건만 승인합니다. 기존 환경의 동일 복원이라고 표현하지 않습니다.
>
> 지정된 새 경로에서 확인된 interpreter에 기존 과학 lock의 전체 30개 배포판을 같은 판으로 준비합니다. 사전에 명시된 별도 시험 도구 범위만 포함합니다. 기존 환경·코드·봉인·C5 원문을 덮어쓰거나 삭제하지 않습니다.
>
> **emit 1회와 check 1회만** 허용합니다. check 내부의 emit을 포함하여 **합성 COBYQA 최적화 총 2회, 전체 Sobol 생성 경로 총 2회**임을 수용합니다. 여기에는 seed/rng 비교 생성과 check의 임시 파일 쓰기도 포함됩니다. pytest·변이 시험·C5 재측정은 포함하지 않습니다.
>
> 전체 1,800초·디스크 2,000,000,000 B를 한도로 합니다. venv·다운로드/캐시·별도 시험 도구·봉인·임시 파일·기록의 새 파일을 합산합니다. 이 수치는 메모리 한도가 아니며 설치 완료 보증도 아닙니다. 미측정은 0 또는 PASS로 바꾸지 않습니다.
>
> 설치 실패·배포판 집합/판 불일치·기존 경로 충돌·예산 초과·예상 밖 차이는 최초 오류와 확보된 기록을 남기고 중지합니다. 임의 재시도·패키지 판 완화·다른 interpreter·새 경로 fallback·코드 수정은 하지 않습니다.
>
> old→new 차이표와 새 MANIFEST를 제출하고 멈춥니다. 새 emit/check 성공만으로 새 봉인을 자동 채택하지 않습니다. 차이 검토 수용과 정정된 C4-0 범위 확인 뒤 그 봉인을 C4 환경으로 명시 연결합니다.
>
> REIL 원자료·pickle·노트북 개봉, 실측 자료 맞춤, E3a/H 실행, COMSOL, 기존 사본 정리는 승인하지 않습니다.

## §7 앞으로의 컨테이너 교체 (검토자 제안 기록 · 지금 결정하지 않음)

검토자는 두 경우를 나눠 다루자고 제안했다. 우리 의견은 **동의**다. 이번 요청은 후자다.

- **승인된 동일 아티팩트**를 동일 프로필로 복원하는 범위: 경로 · 횟수 · 예산 · identity 대조 · 실패 중지를 고정하면 미리 승인할 수 있다.
- interpreter · 빌드 · 배포판 · 설명 안 된 RECORD 가 달라지는 **새 환경 세대**: 매번 별도의 차이 검토와 채택 승인을 받는다.

"같은 판을 다시 깔고 emit / check 만 되면 자동 채택" 하는 포괄 규칙은 두지 않는다. 이번에 보존하는 wheel sha 28 + 4 와 RECORD 원문 30 + 4 는
나중에 "동일 아티팩트 복원" 을 판정할 근거가 된다. 그 규칙을 둘지는 그때 따로 묻는다.

## 부록 A — S4 의 과학 wheel 기대 이름 28 (P0 설치 로그 `01_venv_pip_install.stdout` 에서 읽은 값 · 참고용 사본)

정본은 로그다. S4 는 이 표가 아니라 로그에서 읽는다.

`about_time-4.2.1-py3-none-any.whl` · `alive_progress-3.3.0-py3-none-any.whl` · `autograd-1.9.1-py3-none-any.whl` ·
`cffi-2.1.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl` · `cma-4.5.0-py3-none-any.whl` ·
`contourpy-1.3.3-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl` · `cycler-0.12.1-py3-none-any.whl` ·
`deprecated-1.3.1-py2.py3-none-any.whl` · `et_xmlfile-2.0.0-py3-none-any.whl` ·
`fonttools-4.66.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl` · `graphemeu-0.7.2-py3-none-any.whl` ·
`kiwisolver-1.5.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl` ·
`matplotlib-3.11.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl` ·
`moocore-0.3.2-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl` ·
`numpy-2.4.6-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl` · `openpyxl-3.1.5-py2.py3-none-any.whl` ·
`packaging-26.3-py3-none-any.whl` · `pandas-3.0.5-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl` ·
`pillow-12.3.0-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl` · `platformdirs-4.12.3-py3-none-any.whl` ·
`pycparser-3.0-py3-none-any.whl` · `pymoo-0.6.2-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl` · `pyparsing-3.3.3-py3-none-any.whl` ·
`python_dateutil-2.9.0.post0-py2.py3-none-any.whl` · `scipy-1.17.1-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl` ·
`seaborn-0.13.2-py3-none-any.whl` · `six-1.17.0-py2.py3-none-any.whl` ·
`wrapt-2.5.0-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl`.

PyPI 는 같은 파일 이름의 재업로드를 허용하지 않는다. 그래서 같은 이름은 같은 바이트다 (색인 정책에 기댄 판단 · 옛 wheel 의 sha 기록은 없다).
같은 판에 다른 태그의 wheel 이 나중에 추가돼 pip 의 선택이 바뀌면, S4 에서 설치 전에 멈춘다.
