# REIL C4-ENV 새 환경 세대 (CPython 3.11.18) 재봉인 승인 요청 v2 — 사전 검토 (§137) 정정 · 실행기 · 하네스 고정 · 2026-11-24

> **v2 (원장 §138 — 사용자 "권고대로해요").** v1 (`docs/REIL_C4_ENV_RESEAL_REQUEST_20261124.md` · `ae25f895…` · 커밋 `781f357`) 의 사전 검토
> 회신 (원장 §137 · `REVISION_REQUIRED_BEFORE_RESEAL_EXECUTION_APPROVAL`) 을 반영했다. v1 · v1 대조기 (`8cf10f3c…`) · v1 자체 시험 기록 (run1 포함) 은
> 그대로 둔다. 바뀐 자리는 본문에 **(v2 정정 — …)** 로 표시했고, 그 밖의 행은 v1 바이트 그대로다. 대응은 바로 아래 §0-v2 표다.
> **실행 0** — v2 에서 새로 한 것은 대조기 보강 · 실행기 · 하네스 작성과 그 합성 자체 시험뿐이다 (§9-v2). 설치 · venv · pip · emit · check · precheck 0.

## §0-v2 사전 검토 (§137) → v2 의 답

| 검토 | 요구 | v2 의 답 | 자리 |
|---|---|---|---|
| **ENV18-N1** [P2] | `PIP_CERT` 만으로 유효 CA 가 고정되지 않는다 (`REQUESTS_CA_BUNDLE` · `CURL_CA_BUNDLE` 이 앞선다) | 모든 자식 env 에서 `REQUESTS_CA_BUNDLE` · `CURL_CA_BUNDLE` · `SSL_CERT_FILE` · `SSL_CERT_DIR` 를 뺀다 (있던 이름 기록) → pip 의 유효 CA = `PIP_CERT` 파일 하나. 그 파일의 크기 · sha256 을 S0 에 (경로 비공개). TLS 검증은 끄지 않는다. 프록시 변수는 물려준다 (이름만 · 값 · 실제 접속은 관측 밖) | §1-5 · 시험 T1f · T6 · 변이 RM2 |
| **ENV18-N2** [P2] | 커밋 전 `10_end.json` 에 S10 최종 결과를 넣을 수 없다 | `10_end.json` = PRE_COMMIT · S10 PENDING (커밋 결과 없음). 커밋 시도 · 원 rc · timeout · SHA · S10 시작 / 끝 · 한도 판정 = 커밋 **밖** `SP/reil_env18/11_after_commit.json` · 바깥 반환 = 하네스 `outer_return.json` (따로) · 못 얻은 값 null · 실패 뒤 정상 완료 재선언 없음 | §1-9 · §2-1 · T1c · T1d · T9b · T12 |
| **실행 전 조건** | 실행기 · 바깥 하네스를 고정해 정적 검토 | 실행기 (`bf47d9f7…`) · 하네스 (`f4afd4b6…`) 를 이 요청 커밋에 고정 · 10월 실행기 대비 diff 보존 · 정확 argv · cwd · 승인은 원장의 승인 블록 하나 (요청서 · 실행기 · 하네스 · 대조기 sha · 요청 커밋 · 사용자 원문) | §2-1 |
| **ENV18-C1** (비차단) | `Downloading` 꼴은 Link 호스트 | 문장을 "pip 이 처리한 다운로드 Link 의 호스트" 로 좁힘 (redirect 뒤 최종 응답 · 프록시의 실제 접속이 아님) | §1-5 |
| **ENV18-C2** (비차단) | `records` 의 dict 가 같은 Name+Version 의 두 dist-info 를 덮는다 | 사전 (dict) 에 넣기 **전에** 식별 중복 거부 — 재현 시험 R21 · R21b · R21c 를 먼저 쓰고 v1 대조기에서 FAIL 을 확인한 뒤 고침 (RED 52 / 62 → GREEN 62 / 62) · 변이 M13 | §1-8 · §9-v2 |
| **Q3 덧붙임** | seal 은 S9a 성공 · 보존 RECORD 불변을 전제로 | `seal` 모드가 S9a 보고 (`09a_records.json`) 를 필수 입력으로 받아 `allowed_only` 와 보존 RECORD 원문 sha 를 대조 — seal 단독 통과를 RECORD 수용으로 쓰지 않는다 (S11 · S12 · S13 · M15 · M16) | §1-8 · §2-2 |
| **Q5** | v4 결속 좌표 · RECORD 밖 파일 | §6 문안에 v4 §4-3 (318 행) 의 C6 봉인 · §6-2 (458 행) 의 환경을 따로 적음. RECORD 밖 파일 = **전체** 목록 · 크기 · sha256 (v1 은 수와 첫 50 이름) · 실행 경로 관련 (`.pth` · `.py` · `.pyc` · `.pyo` · `.so` · `.pyd`) 은 `adoption_hold` 표지 → 결과 검토에서 처분 (자동 실패도 자동 채택도 아님) (R22 · R23 · R23b · R23c · M14 · M17 · T13) | §1-8 · §6 |
| **Q2** | A 안 조건부 · 잔여 위험은 사용자 선택 | 사용자가 A 안의 잔여 위험 (pip wheel 을 바꾼 주체 · 원래 출처 미확인) 을 수용 (원장 §138). "선언 1 행" = cacert payload 행 하나 — wheel 자신의 RECORD 도 다시 쓰였으므로 "구성원 하나만 달랐다" 로 넓히지 않는다 | §0 · §1-8 |
| **덧붙인 지적** | precheck 한도 · 실행기 폴더 디스크 · timeout 구분 · 순수 Python 초과 · 첫 원인 · 출력 부재 | precheck 60 s (실행기) / 90 s (하네스 절대) · `du` 합에 `SP/c4env18_outer/` · 자식 timeout = min(단계 남은, 전체 남은) + 프로세스 그룹 kill · 순수 Python 작업은 끝난 뒤 탐지 · 절대 반환 = 하네스 (run 1,860 s) · `STOP.json` 은 한 번만 · 뒤 오류는 followups · 모든 출력은 없을 때만 씀 | §1-9 · §2-1 · T7 · T8 · T9 · T10 · T11 · RM3–RM8 |
| **(새) 샌드박스 시험이 잡은 것** | — | 실행기를 import 하는 쪽이 `-B` 없이 돌면 저장소에 pyc 가 생겨 보호 경로가 더러워진다 → 하네스 argv 에 `-B` · 실행기는 `-B` 없으면 거부 (변이 RM1 이 되살려 T1a FAIL 확인) | §2-1 |
| **(새) 변이 증명이 잡은 것** | — | 실행기 변이 증명 1 차 개발 실행 8 / 9 — T2 가 "통제된 거부" 와 "충돌" 을 가르지 못해 RM6 이 살아남음 → T2 를 거부 사유 · traceback 0 까지 보게 강화 · RM6b 더함 (실행기 변경 0 · 원문 보존) | §2-1 |
| **(새) 자체 검토가 잡은 것** | — | 실행기가 승인 블록의 요청서 경로를 고정하지 않음 (다른 요청서 + 그 sha 로 바꿔 넣기가 통과) → `request_rel` 대조 · RED T15 21 / 22 → GREEN 22 / 22 · 변이 RM9 · 앞 최종 기록은 `run1_*` 보존 | §2-1 |
| **작은 지적의 처리 (요청)** | — | 이번 정적 검토에서 남는 지적이 작은 P2 뿐이면, 조건부 수용 (`ACCEPT_IF` — 고칠 것 · 확인 방법) 으로 답해 주기를 청한다. 그 조건은 실행 전에 문서 정정 1 회로 반영하고, 반영 기록을 결과 검토 묶음에 넣는다 | 발송문 |

> **승인 요청문이다.** 사용자 승인 전에는 venv 생성 · 내려받기 · 설치 · emit · check 를 하지 않는다 (0 회). 지금까지 한 것은 둘이다 (§9) — **(v2)** 셋째는 아래 (3) (§9-v2).
> (1) **읽기만 한 관측:** interpreter · deb · ensurepip 묶음 · 환경 변수 이름 · 경로 부재 · 디스크. 원문은 `bms-balancing/evidence/reil_c4_env_reseal_pre_20261124/` 에 있다.
> (2) **새 대조기와 자체 시험:** `bms-balancing/scripts/reil_c4_env_reseal_check.py` 를 쓰고 자체 시험 52 / 52 · 변이 증명 13 / 13 을 돌렸다. 쓴 자료는 합성 자료 ·
> 커밋된 10월 봉인과 원문 · 지금 ensurepip 묶음 (읽기만) 뿐이다. 기록은 `bms-balancing/evidence/reil_c4_env_reseal_selftest_20261124/`.
> (3) **(v2)** 대조기 v2 · 실행기 · 하네스 · 그 합성 자체 시험 (대조기 62 / 62 · 변이 18 / 18 · 실행기 샌드박스 22 / 22 · 실행기 변이 11 / 11) — `bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/` (§9-v2).
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
- **(v2 정정 — Q2)** 그래서 아래의 "선언 1 행" 은 cacert payload 의 허용 차이 1 행이다. wheel 구성원 단위로는 `cacert.pem` 과 wheel 자신의 RECORD 가
  다르다 ("구성원 하나만 달랐다" 로 넓히지 않는다). 사용자는 이 출처 미확인의 잔여 위험을 알고 A 안을 골랐다 (원장 §138).
- **과학 계산과의 관계:** 과학 코드 (`env_profile` · `reil_c6_profile` · COBYQA · Sobol) 는 pip 을 import 하지 않는다. 이 실행의 pip 은 `PIP_CERT` 묶음으로 TLS 를
  확인하므로 이 파일을 쓰지 않는다 (§1-5). 이 차이가 닿는 곳은 lock 의 pip `record-sha256` 한 칸이다. pip 은 wrapper 행 때문에 10월에도 이 칸이 바뀐 배포판이다.

## §1 고정 표 (10월 §1 의 9 항목 그대로 · 바뀐 값만 새로)

### 1-1. 저장소 HEAD · 보호할 원본

- 시작 HEAD 는 이 요청문 · 대조기 · **(v2) 실행기 · 하네스** · 자체 시험 기록 · 승인 기록 (승인 블록) · 보존 규칙이 든 커밋이다 (그 뒤 문서만 바뀐 커밋
  포함). 실행 기록에 40 자로 적는다. **(v2)** 요청 커밋은 승인 블록의 `request_commit` 이 정한다 (§2-1).
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
| `bms-balancing/scripts/reil_c4_env_reseal_check.py` (**v2 대조기** · 35,309 B — v1 `8cf10f3c…` 는 커밋 `781f357` 에 그대로) | `0049e7e9a153ec3a0fe8b38f5f106ecc4264c75d8c819c7b14886ba6f7e079c0` |
| `bms-balancing/scripts/reil_c4_env_reseal_run.py` (**v2 · 실행기** · 40,438 B) · `…/reil_c4_env_reseal_harness.py` (**v2 · 하네스** · 4,851 B) | `bf47d9f7a883d87740be0db8649c3b140f9d9efb554986ccc3b6e0a18df0bb92` · `f4afd4b61cf5d798ced37770a8673d7fa32f30352334fd61b1dfced4fa252642` |
| `bms-balancing/docs/REIL_C4_ENV_RESEAL_REQUEST_20261124.md` (v1) · `bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/` (**v2 근거**) | `ae25f895051ec28f06aebf0bf43f07a9e58b77cb24e3a7abb6448572ed0e0791` · tree `6b29febe0afa950ec6ddd9d53a24dfdffc63fdda` |
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
| 실행기 · 하네스 (**v2 정정 — 저장소 · 요청 커밋에 고정** · §2-1) | `bms-balancing/scripts/reil_c4_env_reseal_run.py` · `bms-balancing/scripts/reil_c4_env_reseal_harness.py` |
| 하네스 출력 (**v2** · 저장소 밖) | `SP/c4env18_outer/precheck/` · `SP/c4env18_outer/run/` (stdout · stderr 원문 · `outer_return.json`) |
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

### 1-5. 출처 · 네트워크 · argv · 유효 환경 (검토 ENV-P2-04 반영 · **v2 정정 — ENV18-N1 · C1**)

- **색인을 argv 로 고정한다:** S2 · S3 에 `--index-url https://pypi.org/simple` 을 넣는다. pip 기본값과 같은 값이지만 명시한다. extra index · find-links 는 S2 · S3 에서
  0 이다. 설치 (S5 · S6) 는 `--no-index --find-links` 로 S2 · S3 의 파일만 쓰며, 네트워크는 0 이다.
- **자식 환경 규칙** (S0 의 대조기 호출과 S1–S9 의 모든 자식 · **v2**: 실행기의 `child_env` 한 곳):
  1. 비밀 형태 이름을 뺀다. 10월 정규식 그대로이고 (`TOKEN|SECRET|PASSW|ACCESS_KEY|CREDENTIAL|COOKIE|^GIT_CONFIG_` · 대소문자 무시), 뺀 이름만 기록한다.
  2. `PIP_` 로 시작하는 이름은 **`PIP_CERT` 하나만 물려받고** 나머지는 전부 뺀다 (이름 기록). pip 단계에는 실행기가 `PIP_CONFIG_FILE=/dev/null` 을 넣는다. pip 은 이
     값이면 설정 파일을 하나도 읽지 않는다. 이렇게 하면 `PIP_INDEX_URL` · `PIP_EXTRA_INDEX_URL` · `PIP_FIND_LINKS` 같은 출처 변수가 자식에 들어갈 수 없다.
  3. `PIP_CERT` 가 없거나 파일이 아니면 S0 에서 멈춘다 (유효 환경이 고정 표와 다르다 · **v2**: precheck 에서도). 그 값 (경로) 은 문서 · 기록에 옮기지 않는다. 가리키는 파일의 크기 · sha256 만 기록한다.
  4. 단계마다, 자식에 넘긴 환경 변수 **이름 전체** · 뺀 이름 (**v2**: 비밀 형태 · PIP · CA 를 따로) 과 실행기가 넣은 값 (`TMPDIR` · `PIP_CONFIG_FILE` · `PYTHONDONTWRITEBYTECODE`) 을 meta 에 적는다. 그 밖의 값은 적지
     않는다 (하드룰 2).
  5. **(v2 정정 — ENV18-N1)** `REQUESTS_CA_BUNDLE` · `CURL_CA_BUNDLE` · `SSL_CERT_FILE` · `SSL_CERT_DIR` 를 뺀다 (있던 이름만 기록). 2026-11-24 관측으로 앞의 셋이
     지금 환경에 있다 (`evidence/reil_c4_env_reseal_pre_20261124/05_env_names.txt`).
- **pip 이 쓰는 CA (v2 정정 — ENV18-N1):** v1 은 여기서 "`PIP_CERT` 가 있으면 pip 은 그 묶음으로 TLS 를 확인한다" 고 적었다. 그것만으로는 고정되지 않는다.
  pip 24.0 은 `PIP_CERT` 를 `session.verify` 에 넣는다 (`pip/_internal/cli/req_command.py`). 그런데 vendored requests 의 `merge_environment_settings` 는 요청마다
  `REQUESTS_CA_BUNDLE` → `CURL_CA_BUNDLE` 을 먼저 보고, 그 값이 `session.verify` 를 이긴다 (`pip/_vendor/requests/sessions.py` · 검토 §137). 규칙 5 로 두 이름이
  자식에 없으므로 유효 CA 는 `PIP_CERT` 파일 하나다. CA 파일을 받으면 vendored urllib3 1.26 은 그 파일만 읽고 기본 CA 는 읽지 않는다 (`pip/_vendor/urllib3/util/ssl_.py` ·
  `connection.py`). `SSL_CERT_FILE` · `SSL_CERT_DIR` 는 기본 CA 경로를 바꾸는 이름이라 그 길에 닿지 않지만, 모호함을 없애려고 같이 뺀다. TLS 검증은 끄지 않는다.
  그래서 wheel 안 `cacert.pem` (§0 의 바뀐 파일) 은 쓰지 않는다. 그 파일은 venv 의 pip 안에
  들어갈 뿐이다. 내려받은 바이트가 맞는지는 TLS 가 아니라 S4 의 sha256 대조가 보증한다.
  **(v2)** 이 정정 뒤에도 바뀐 wheel 의 출처 미확인은 남는다 (사용자 수용 · 원장 §138). 위 소스 세 곳은 지금 ensurepip 묶음의 wheel 안 파일을 읽어서만 확인했다.
- **파일 호스트 관측 (간접 · v2 정정 — ENV18-C1):** pip 24.0 의 `pip/_internal/network/download.py` `_prepare_download` 는 **pip 이 처리한 다운로드 Link** 의
  호스트가 `files.pythonhosted.org` 일 때만
  `Downloading <파일 이름>` 으로 쓰고, 그 밖이면 전체 URL 을 쓴다. 지금 묶음의 소스를 읽어서만 확인했다.
  - 그래서 S2 · S3 stdout 의 `Downloading` 줄이 전부 파일 이름 꼴이면, **pip 이 처리한 Link 의** 호스트가 `files.pythonhosted.org` 라는 뜻이다 (**v2**: redirect
    뒤의 최종 응답 호스트도, 프록시의 실제 접속도 아니다).
  - 결과 보고에 그 줄의 수와 꼴 (이름 꼴 / URL 꼴) 을 센다.
- **(v2) 프록시 변수:** `HTTPS_PROXY` · `https_proxy` · `NO_PROXY` · `no_proxy` 는 빼지 않는다 (네트워크에 필요 · 2026-11-24 관측으로 넷 다 있다). 이름만 기록하고
  값은 적지 않는다. `~/.netrc` 는 있는지만 기록한다.
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
| 과학 RECORD 30 · 시험 RECORD 4 (S9a) | 아래 표 | `records` · R1–R20 · R14b · **(v2) R21–R23c** |
| **(v2 정정 — Q3)** S9a ↔ S9b 결속 | `seal` 은 S9a 보고 (`09a_records.json`) 를 필수 입력으로 받는다. 보고가 `allowed_only` 가 아니거나, 보존 RECORD 원문의 sha 가 보고와 다르면 미허용이다 — seal 단독 통과를 RECORD 수용으로 쓰지 않는다 | `seal` · S11 · S12 · S13 |
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
| **배포판 식별 (v2 정정 — ENV18-C2)** | 같은 정규화 Name + Version 을 내는 dist-info 가 둘 이상이면 미허용이다 (과학 · 시험 도구 둘 다). 사전 (dict) 에 넣기 **전에** 거부하고, 덮어쓰지 않는다 |
| 값이 달라도 되는 행 | (i) **wrapper 13 행** — 과학 10 (cffi 1 · fonttools 4 · numpy 2 · pip 3) · 시험 3 (pytest 2 · pygments 1). 새 파일 첫 줄이 `#!SP/reil_env18/venv/bin/<python\|python3.11>` 이어야 하고, 그 첫 줄만 옛 경로로 되돌린 바이트가 옛 행의 해시 · 크기와 같아야 한다. 본문 · 이름 · 판정 범주를 옛 행에 결속하는 규칙이다. 값이 옛것과 같아 보여도 이 검사는 언제나 한다 (옛 경로가 남은 파일을 잡는다). (ii) **선언 1 행** — pip 의 `cacert.pem` (옛 값 → 새 값 정확). 그 밖의 행 값 차이는 미허용이다 |
| dist-info | 한 RECORD 안의 `*.dist-info/…` 행은 자기 dist-info 의 것뿐이어야 한다. 다른 배포판의 `INSTALLER` · `REQUESTED` · `RECORD` 행은 미허용이다 |
| 설치 바이트 | 해시 있는 행은 전부 실제 설치 바이트 · 크기와 같아야 한다. venv 는 site-packages 기준이고 `../../../bin` · `../../../share` 를 포함한다. `pytest_t` 는 `../../bin/X` 를 `pytest_t/bin/X` 로 읽는다 (pip `--target` 은 bin 을 옮기고 RECORD 를 고치지 않는다) |
| 해시 없는 행 | `__pycache__/*.pyc` 와 자기 `RECORD` 뿐이다 |
| 설명된 충돌 | 1 건 — `../../../LICENSE` (about-time 4.2.1 ↔ alive-progress 3.3.0 · `reil_c6_profile.EXPLAINED_COLLISIONS` 와 같다). 이 행의 디스크 바이트는 주인 (alive-progress) 행과 같아야 한다. 선언과 관측이 다르면 미허용이다 |
| 보존 | 새 원문 30 + 4 를 바이트 그대로 보존한다 (`09_records/` · `09_test_tool_records/`). S9b 의 lock 기대값은 이 보존본에서 계산한다 (결속) |
| 관측 (**v2 정정 — Q5**) | RECORD 어디에도 없는 파일 (site-packages · `pytest_t`) 은 **전체** 목록 · 크기 · sha256 을 적는다 (v1 은 수와 첫 50 개). rc 판정에는 쓰지 않는다 (10월 세대에 같은 관측이 없어 기준이 없다). 다만 실행 경로에 닿을 수 있는 것 (`.pth` · `.py` · `.pyc` · `.pyo` · `.so` · `.pyd` — `sitecustomize` · `usercustomize` 포함) 이 하나라도 있으면 `adoption_hold` 표지를 세우고 사유를 적는다 → 실행은 계속되고 기록 · 커밋 제목에 그 표지가 남으며, **결과 검토에서 처분하기 전에는 채택하지 않는다** (일반 잉여 파일로 묵인하지 않는다) |

- 10월 원문 34 의 규모는 행 13,398 · 해시 있는 행 7,657 · 해시 없는 행 5,741 이다. 이 가운데 과학은 7,188 행이 해시 있음이다 (lock `verified` 7,187 + 충돌 1).
- **대조기 (v2 정정):** `bms-balancing/scripts/reil_c4_env_reseal_check.py` (35,309 B · sha256 `0049e7e9a153ec3a0fe8b38f5f106ecc4264c75d8c819c7b14886ba6f7e079c0`) — v1 (32,342 B · `8cf10f3c…dbedb0`) 에
  위 세 자리 (식별 중복 · S9a 결속 · 전체 관측 + 채택 보류) 만 더했다. CLI 의 `seal` 에 `--records-report` 가 필수로 붙었다.
  - stdlib 만 쓰고 `/usr/bin/python3.11 -I -B` 로 돌린다. 과학 패키지 import 는 0 이다.
  - 출력 파일이 이미 있으면 쓰지 않는다 (rc 2). rc 는 0 = 허용만 · 1 = 미허용 · 2 = 사용 오류 · 3 = 도구 오류다.
  - 고정값 (옛 · 새 venv 경로 · 선언 행 · 충돌 · ensurepip 값 · python 판) 은 파일 안의 상수다. 그래서 **이 세대 전용**이고, 범용 자동 복원 검사기가 아니다 (§8-2).
  - 10월 `reil_c4_env_compare.py` 는 부르지 않는다. 그 도구는 그 실행의 증거로 보호만 한다.
- "미허용" 이면 성공으로 채택하지 않는다. 그 자리에서 멈추고, 원문을 보존하고, 보고한다. libc · BLAS · 옵션 · 배열 · 그 밖 RECORD 의 미상 차이는 포괄 승인하지 않는다.

### 1-9. 시간 원점 · 배정 · 디스크 (검토 ENV-P2-01 반영 · **v2 정정 — ENV18-N2 · 덧붙인 지적**)

- **원점과 전체 한도:** 원점 t0 은 S0 의 첫 명령 직전이다 (UTC 와 monotonic 둘 다 기록). 전체 한도 1,800 s 는 t0 부터 S10 의 로컬 커밋 끝까지다. push 는 한도 밖이고
  기록만 한다.
- **(v2) precheck:** 원점 전 1 회다. 실행기 자신의 한도는 60 s, 하네스의 절대 상한은 90 s 다. 쓰는 것은 하네스 출력 (`SP/c4env18_outer/precheck/`) 뿐이고,
  1,800 s 에 넣지 않는다. 그 원문을 S0 이 기록 폴더 (`E/00_precheck_before_t0/`) 로 복사한다.
- **단계별 배정:** §2 표의 timeout 이고, 합계는 정확히 1,800 s 다. 자식마다 timeout 은 min(단계 배정의 남은 몫, 전체의 남은 몫) 이다. S4 a / b 는 30 s 를, S9 a / b 는
  120 s 를 나눠 쓴다. 남은 시간을 다른 단계로 자동으로 돌리지 않는다.
- **(v2) 넘으면 · 남으면:** 자식은 **프로세스 그룹째** TERM → 5 s → KILL 하고 멈춘다. rc 0 으로 끝났는데 같은 그룹에 남은 자식이 있으면 끊고 멈춘다.
- **(v2 · 덧붙인 지적) 순수 Python 작업:** 실행기 안의 해시 · `du` · 기록 쓰기 · git 호출은 도중에 끊지 못한다. 그 작업이 끝날 때마다 단계 · 전체 초과를
  **사후 탐지**해 멈춘다. git 호출은 남은 몫을 timeout 으로 받는다. **절대 반환**은 바깥 하네스가 보장한다 (run 1,860 s 에서 그룹째 끊음 · rc 124 · §2-1).
- **S10 도 90 s 를 강제한다.** S10 안의 git · 검사 호출마다 남은 몫을 timeout 으로 준다. 10월 실행기는 S10 을 합산해 강제하지 않았고, 전체 한도도 마지막 작업 전에만
  검사했다 (ENV-P2-01).
- **(v2 정정 — ENV18-N2) S10 의 순서:**
  1. 커밋 전 기록 `E/10_end.json` — `phase: PRE_COMMIT` · `s10.status: PENDING` · 커밋 결과 칸 없음 (그때 알 수 없으므로).
  2. 비밀값 검사 (걸리면 커밋하지 않는다).
  3. 남은 몫이 5 s 미만이면 `git add` · `commit` 을 **시작하지 않는다** — git 을 도중에 죽이면 `index.lock` 이 남을 수 있다. 기록은 작업트리에 남고 사후 문서
     커밋으로 넣는다.
  4. `git add -f` → 스테이지 blob = 디스크 바이트 전수 대조 → 로컬 커밋 (timeout = 남은 몫 · 넘으면 `index.lock` 남음을 기록).
  5. 커밋 **밖** `SP/reil_env18/11_after_commit.json` (아래 '커밋 뒤 관측').
- **디스크 한도 2,000,000,000 B:** `du -sb` 로 `SP/reil_env18/` · 새 봉인 · 기록 · **(v2 정정 — 덧붙인 지적)** 하네스 출력 `SP/c4env18_outer/` 넷을
  합산한다.
  - 관측 시점은 S2 · S3 · S5 · S6 · S8 · S9 끝 · S10 커밋 직전 · **커밋 뒤**다. 넘으면 그 자리에서 중지한다.
  - 보고에는 "표본 최대" 라고 적고, 연속 peak 가 아니라고 밝힌다.
  - `df -B1` 여유 (**v2**: `shutil.disk_usage` 의 free — S0 과 표본마다) 는 참고로만 적는다. 메모리 한도가 아니고 설치 완료를 보증하지도 않는다. 재지 못한 값을 0 이나 PASS 로 바꾸지 않는다.
- **커밋 뒤 관측 (ENV-P2-01 · v2 정정 — ENV18-N2):**
  - 로컬 커밋이 끝나면 (**v2**: 시작하지 않았거나 실패해도) 실행기가 monotonic 끝 시각 · `du -sb` 합 · 커밋 rc · 커밋 SHA 를 `SP/reil_env18/11_after_commit.json` 에 쓴다. 이 파일은 커밋 밖이고, 커밋된
    기록을 고치지 않는다.
  - **(v2)** 그 칸: 커밋 시도 여부 · argv · 원 rc · timeout · 커밋 SHA · 새 커밋인가 · S10 시작 / 끝 / 걸린 s · S10 · 전체 · 디스크 한도 판정 · `10_end.json` 의
    sha · 스테이지 파일 수 · 채택 보류 표지 · ok. 못 얻은 값은 null 이다. 실패 뒤에 정상 완료를 다시 선언하지 않는다.
  - 실행기의 바깥 반환 (stdout 원문 · rc) 은 실행하는 쪽 (하네스) 이 파일로 받는다 (**v2**: `SP/c4env18_outer/run/` 의 stdout · stderr 원문 · `outer_return.json`
    — argv · cwd · env 이름 · 시작 / 끝 · 걸린 s · rc · 상한 kill 여부 · 크기 · sha). 각 파일은 자기 뒤의 쓰기 · 반환을 증명하지 않는다. 하네스를 부른 쪽
    (Claude Code 의 Bash 도구) 의 반환은 그 대화 기록이다.
  - 이 둘 (**v2**: + precheck 의 하네스 출력) 은 재실행 없이 별도 문서 커밋으로 `evidence/reil_c4_env_20261124_after/` 에 붙인다.
  - 커밋 뒤 관측이 한도를 넘으면 그 실행을 **한도 초과**로 보고한다. 이미 커밋된 기록은 고치지 않고, 이 파일이 정정 참조가 된다.
- **시작 조건:** 여유가 4,000,000,000 B 이상이어야 한다 (한도의 2 배). 2026-11-24 관측은 26,006,093,824 B 이고, S0 에서 다시 잰다 (**v2**: precheck 에서도).
- **실패하면:** 만든 파일을 지우지 않는다 (정리 승인 없음 · 스크래치는 세션과 함께 사라진다). 저장소 쪽 (부분 봉인 · 기록) 은 "정지 상태의 기록 · 채택 아님" 으로 커밋한다
  (10월 §1-9 와 같다).
- **(v2) 첫 원인:** 첫 원인은 `E/STOP.json` 에 **한 번만** 쓴다. 뒤의 오류는 followups (`10_end.json` · `11_after_commit.json`) 로 간다. 저장소 쪽 커밋은
  S10 의 남은 몫이 5 s 이상일 때만 한다 (위 'S10 의 순서' 3).

## §2 순서 · 정확 argv

### 2-1. 실행기 · 바깥 하네스 (**v2 정정 — 실행 승인 전에 고정 · 검토 §137 Q4**)

| 파일 (이 요청 커밋에 고정) | 크기 · sha256 | 하는 일 |
|---|---|---|
| `bms-balancing/scripts/reil_c4_env_reseal_run.py` | 40,438 B · `bf47d9f7a883d87740be0db8649c3b140f9d9efb554986ccc3b6e0a18df0bb92` | 실행기 — `precheck` (읽기만 · 쓰기 0) · `run` (S0–S10 1 회) |
| `bms-balancing/scripts/reil_c4_env_reseal_harness.py` | 4,851 B · `f4afd4b61cf5d798ced37770a8673d7fa32f30352334fd61b1dfced4fa252642` | 바깥 하네스 — 실행기를 정확한 argv · cwd 로 1 회 · 절대 상한 · 바깥 반환 |
| `bms-balancing/scripts/reil_c4_env_reseal_check.py` | 35,309 B · `0049e7e9a153ec3a0fe8b38f5f106ecc4264c75d8c819c7b14886ba6f7e079c0` | 대조기 v2 (S0 · S4 · S9) |
| `bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/runner_vs_oct.diff` | 61,518 B · `33235a366fac16d8c1520d9319b91d78e526c5ab48403925dcec01541bb7cfd0` | 10월 실행기 (`evidence/reil_c4_env_20261013/00_runner.py` · `5c781a2d…d2cc`) 대비 unified diff — S0 이 같은 diff 를 다시 만들어 기록에 둔다 |

- **부르는 법 (정확 argv · cwd = 저장소 뿌리 `/home/user/Yonghoon-DEM-DFT`):**
  1. `/usr/bin/python3.11 -I bms-balancing/scripts/reil_c4_env_reseal_harness.py precheck` — 하네스가 `/usr/bin/python3.11 -I -B
     bms-balancing/scripts/reil_c4_env_reseal_run.py precheck` 를 부른다 (상한 90 s).
  2. precheck 가 rc 0 · 문제 0 이면 `/usr/bin/python3.11 -I bms-balancing/scripts/reil_c4_env_reseal_harness.py run` — 하네스가 `… reil_c4_env_reseal_run.py run`
     을 부른다 (상한 1,860 s).
  - 하네스는 Claude Code 의 Bash 도구가 한 번씩 부른다 — precheck 는 전경 (도구 timeout 300,000 ms) · run 은 배경 (도구 timeout **2,400,000 ms** — 도구의 배경
    기본값 1,800,000 ms 는 하네스 상한 1,860 s 보다 짧아 하네스보다 먼저 끊을 수 있다 · 도구 최대 7,200,000 ms). 실행기는 `-I` · `-B` 가 둘 다 아니면 시작하지 않는다.
  - precheck 가 문제를 보고하면 run 을 부르지 않고 사용자에게 묻는다. 이 1 회 밖의 원점 전 점검은 없다 (v1 §2-1 그대로 — 10월 편차 (b) "원문 없이 한 사전 점검"
    을 신고된 절차로 바꾼 것).
- **v1 과 다른 자리:** v1 은 실행기를 승인 뒤에 쓰므로 저장소 밖 `SP/c4env18_runner/` 에 두었다 (§1-1 의 시작 조건 — 요청 커밋 뒤 `scripts/` 변경 0). v2 는 실행기 ·
  하네스를 **요청 커밋에** 넣으므로 같은 조건과 맞는다. precheck 출력은 하네스 출력 폴더 (`SP/c4env18_outer/precheck/`) 이고, S0 의 diff 이름은
  `E/00_runner_vs_oct.diff` 다 (v1 의 `E/00_runner.diff` 자리).
- **승인 블록 (실행기가 읽는 유일한 승인):** 사용자 승인 (§6 문안) 뒤, 원장에 아래 꼴의 블록 **하나**를 덧붙여 커밋한다 (C4-A v4 §4-2 의 `c4a-approval` 블록
  선례). 실행기는 이 sha 들을 품지 않는다 — 자기 sha 를 품을 수 없기 때문이다. 블록과 대조한다:

  ```c4env-reseal-approval
  {"kind": "C4ENV_RESEAL_EXECUTION", "decision": "APPROVED",
   "request": {"path": "bms-balancing/docs/REIL_C4_ENV_RESEAL_REQUEST_v2_20261124.md", "sha256": "<64 hex>"},
   "request_commit": "<40 hex>", "runner_sha256": "<64 hex>", "harness_sha256": "<64 hex>", "checker_sha256": "<64 hex>",
   "user_text": "<사용자 원문>"}
  ```
  (실행기는 원장 파일 안에서만 이 머리줄을 찾는다 — 이 요청서 안의 위 예시는 세지 않는다.)
- **precheck · S0 의 대조 (읽기만):**
  - 실행 interpreter = `/usr/bin/python3.11` · `-I` · `-B`.
  - 원장 (HEAD) 의 승인 블록이 정확히 하나 · `kind` · `decision` · 필수 칸 · **블록의 요청서 경로 = 이 요청서 v2** (실행기의 `request_rel` 이 고정 — 다른
    요청서를 그 sha 와 함께 넣으면 거부) · 요청서 (HEAD) sha · 실행기 / 하네스 / 대조기 sha (HEAD 와 작업트리 둘 다) · 지금 도는 실행기 파일의 sha · 요청 커밋이
    HEAD 의 조상 · 블록을 넣은 커밋이 정확히 하나이고 요청 커밋 뒤.
  - 요청 커밋 뒤 보호 경로 (`bms-balancing/scripts/` · `env_profile.py` · §1-1 의 tree) 변경 0 · 작업트리 변경 0 · tree / 파일 sha.
  - §1-2 의 interpreter · deb · `dpkg -V` · 소스 sha · `PIP_CERT` · CA / PIP / 비밀 형태 / 프록시 이름 · `~/.netrc` 유무 · 경로 부재 · 여유 디스크.
  - (run 만) precheck 의 바깥 반환이 rc 0 · 문제 0 · 같은 실행기 sha.
- **S0 이 쓰는 것 (대조 통과 뒤에만):** `SP/reil_env18/` · `…/tmp/` · 기록 폴더 생성 (있으면 실패) → `00_porcelain_start.txt` · `00_runner.py` · `00_harness.py`
  (사본) · `00_runner_vs_oct.diff` · `00_precheck_before_t0/` (precheck 원문 사본) · `00_s0_precheck.json` · `00_approval.json` → S0 의 남은 몫으로 대조기
  `bundled`.
- **10월 실행기에서 바뀐 것 (diff 의 요약):** ① 경로 · 고정값 · 승인 블록 읽기 (상수 대신) ② 자식 env 규칙 (§1-5) ③ S0 에 승인 · CA · `dpkg -V` · 소스 sha ·
  precheck 확인 ④ S4 · S9 = 새 대조기 · S9b 에 S9a 보고 ⑤ 프로세스 그룹 · 남은 자식 · 사후 초과 탐지 ⑥ S10 의 PRE_COMMIT · 5 s 보호 · 커밋 밖 기록 ⑦ 첫 원인
  한 번만 · followups ⑧ 모든 출력은 없을 때만 씀 (`x` 모드 · mkdir 실패 · 대조기 rc 2) ⑨ precheck 모드 (stdout 만).
- **샌드박스 자체 시험 (`bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/selftest_runner.py` · 22 / 22):** 임시 git 저장소에 실행기 · 하네스 · 대조기 사본 · 가짜 요청서 · 원장
  (승인 블록) 을 두고, 단계 argv 를 가짜 명령으로 바꿔 하네스 → 실행기를 끝까지 돌린다. 진짜 단계 (venv · pip · 설치 · emit · check) 는 0 이고, S0 의 읽기
  대조만 진짜 시스템을 읽는다. 자식 env 는 최소 env + 가짜 값이다 (진짜 환경 변수 값을 파일에 옮기지 않는다).

  | 사례 | 확인 |
  |---|---|
  | T1a–T1g · T14 | precheck 쓰기 0 · run → 새 커밋 1 (새 봉인 · 기록만) · `10_end` PRE_COMMIT · `11_after_commit` (커밋 밖) · 바깥 반환 · 자식 env (CA 넷 · PIP · 비밀 형태 빠짐 · `PIP_CERT` · `PIP_CONFIG_FILE=/dev/null`) · `PIP_CERT` 크기 / sha (경로 없음) · precheck 사본 · 실행기 사본 · 10월 diff · 같은 출력 폴더 재실행 거부 |
  | T2 · T3 · T4 · T5 · T6 | precheck 없이 run · 승인 블록 0 · 2 · 실행기 sha 틀림 · `PIP_CERT` 없음 → rc 2 · 쓰기 0 (T2 는 거부 사유 · traceback 0 까지) |
  | T7 · T8 | 자식 timeout → 그룹째 끊음 (손주 포함) · rc 0 인데 남은 자식 → 끊고 멈춤 |
  | T9 · T9b | 첫 원인 보존 (S5 rc 3 뒤 S10 비밀값 검사 실패 → `STOP.json` 그대로 · followups) · 커밋 실패 (pre-commit hook) → `11_after_commit` 에 rc 1 |
  | T10 · T12 | 전체 배정 소진 · S10 5 s 미만 → git add · commit 시작 안 함 (스테이지 0) |
  | T11 | 하네스 절대 상한 → 그룹째 끊음 · rc 124 |
  | T13 | 채택 보류 표지가 `10_end` · `11_after_commit` · 커밋 제목에 그대로 |
  | T15 | 승인 블록이 다른 요청서 (경로 · sha 는 서로 맞음 · 예: v1) 를 가리킴 → precheck rc 2 |
- **샌드박스 시험이 잡은 결함 (1 차 실행):** 실행기를 import 하는 쪽 (시험의 감싸개) 이 `-B` 없이 돌면 저장소 `scripts/__pycache__/` 에 pyc 가 생겨 보호 경로가
  더러워졌다 (precheck 가 문제로 잡음). 운영 경로 (스크립트 직접 실행) 에서는 생기지 않는 길이지만 막았다 — 하네스 argv 에 `-B` · 실행기는 `-B` 없으면 거부.
  1 차 출력은 파일로 보존하지 않았다. 대신 변이 RM1 이 그 상태를 되살려 T1a 가 FAIL 함을 보인다.
- **실행기 변이 증명 (`bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/mutation_proof_runner.py` · 11 / 11):** RM1 (`-B` 뺌) · RM2 (CA 변수 안 뺌) · RM3 (그룹 대신 본 자식만 끊음) · RM4 (뒤
  오류가 첫 원인 자리를 차지) · RM5 (5 s 보호 끔) · RM6 (precheck 선행 확인 중 존재 검사만 뺌) · RM6b (precheck 선행 요구 전부 끔) · RM7 (승인 블록 sha 대조 끔) · RM8
  (남은 자식 검사 끔) · RM9 (요청서 경로 대조 끔) — 각각 겨냥한 사례가 FAIL · 대조군 통과.
- **자체 검토가 잡은 것 (실행기 시험의 최종 기록 1 차 뒤):** 실행기가 승인 블록의 요청서 **경로**를 고정하지 않았다 — sha 만 대조하고 경로는 블록에서 읽었으므로,
  블록이 다른 요청서 (예: v1) 를 그 요청서의 맞는 sha 와 함께 가리키면 precheck 를 통과했다 (C4-A v4 검토 N6 "요청서 + 인자 동시 교체 거부" 와 같은 꼴). 재현 시험
  T15 를 먼저 써서 고치기 전 실행기로 돌린 RED (`bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/red_runner.*`) 는 21 / 22 (T15 만 FAIL · rc 1) 이다. 실행기에 `request_rel` 대조를 더한
  뒤 GREEN 22 / 22 · 변이 RM9 를 더했다. 그 앞의 최종 기록 1 차 (실행기 `459b5f4c…` · 21 / 21 · 10 / 10) 와 그때의 실행기 · 시험 사본은
  `bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/run1_*` 로 보존했다 (`run1_README.txt`).
- **변이 증명의 1 차 개발 실행은 8 / 9 였다 (원문 `bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/dev1_mutation_proof_runner.*` 보존).** RM6 이 살아남았다 — 존재 검사를 빼면 실행기가 없는 파일을 읽다
  예외로 죽는데, 기록 폴더 전이라 rc 2 · 쓰기 0 으로 끝난다. 그래서 rc · 폴더만 보던 T2 가 "통제된 거부" 와 "충돌" 을 가르지 못했다. T2 를 거부 사유 (stdout) ·
  traceback 0 (stderr) 까지 보게 강화하고 RM6b 를 더했다. 실행기 · 하네스 · 대조기는 바꾸지 않았다.
- **한계 (그대로 밝힘):** 실행기 자신의 env (git 포함) 는 정리하지 않는다 (10월과 같음). 순수 Python 작업은 사후 탐지다. 샌드박스는 진짜 pip · 설치 · emit / check
  를 돌리지 않으므로, 그 단계의 시간 · 디스크 · 출력은 실제 실행에서 처음 본다. 하네스를 부르는 Bash 도구의 반환은 대화 기록이고 파일 원문이 아니다.

### 2-2. 단계 표 (**v2 정정 — S0 · S9b · S10**)

- cwd 는 저장소 뿌리 `/home/user/Yonghoon-DEM-DFT` 다. 공통 env 는 `TMPDIR=SP/reil_env18/tmp` 이고, 환경 규칙은 §1-5 다. **(v2)** 실행기는 하네스가
  부른다 (§2-1).
- 줄임말:
  - `V` = `SP/reil_env18/venv/bin/python` · `P` = `/usr/bin/python3.11 -I -B` · `K` = `bms-balancing/scripts/reil_c4_env_reseal_check.py`
  - `C` = `bms-balancing/evidence/reil_p0_20261006/01_venv_constraints.txt` · `OE` = `bms-balancing/evidence/reil_c4_env_20261013`
  - `E` = `bms-balancing/evidence/reil_c4_env_20261124` · `N` = `bms-balancing/reil_c6_rebuild_20261124`
  - `X` = `--no-cache-dir --disable-pip-version-check` · `I` = `--index-url https://pypi.org/simple`
  - pip 단계 env 에는 `PIP_CONFIG_FILE=/dev/null` 을 더한다.

| 단계 | 명령 (argv) | timeout (s) | 네트워크 |
|---|---|---|---|
| S0 사전 대조 | **(v2)** precheck 바깥 반환 확인 · 승인 블록 (§2-1) · 읽기 대조 (HEAD · porcelain 원문 · §1-1 보호 · §1-2 재측정 · `dpkg -V` · 소스 sha · §1-3 경로 부재 · 여유 · `PIP_CERT`) → `mkdir SP/reil_env18 SP/reil_env18/tmp E` (있으면 실패) → 시작 기록 (precheck 원문 사본 포함 · **v2**: 실행기 · 하네스 사본 · 10월 diff · 승인 블록 사본) → `P K bundled --bundled /usr/lib/python3.11/ensurepip/_bundled --out E/00_bundled_check.json` (rc ≠ 0 이면 S1 전 중지) | 60 | 0 |
| S1 venv | `/usr/bin/python3.11 -I -m venv SP/reil_env18/venv` | 120 | 0 |
| S2 과학 내려받기 | `V -I -m pip download X I --only-binary=:all: --dest SP/reil_env18/wheels -c C numpy==2.4.6 scipy==1.17.1 pandas==3.0.5 openpyxl==3.1.5 matplotlib==3.11.2 seaborn==0.13.2 pymoo==0.6.2` | 480 | PyPI |
| S3 시험 도구 내려받기 | `V -I -m pip download X I --only-binary=:all: --no-deps --dest SP/reil_env18/wheels_test pytest==9.1.1 pluggy==1.6.0 iniconfig==2.3.0 pygments==2.21.0` | 120 | PyPI |
| S4 wheel 대조 | a `P K wheels --wheels SP/reil_env18/wheels --expect OE/04_artifacts_science.json --out E/04a_wheels_science.json` · b `P K wheels --wheels SP/reil_env18/wheels_test --expect OE/04_artifacts_test.json --out E/04b_wheels_test.json`. rc ≠ 0 이면 설치 전 중지 | 30 | 0 |
| S5 과학 설치 | `V -I -m pip install X --no-index --find-links SP/reil_env18/wheels -c C numpy==2.4.6 scipy==1.17.1 pandas==3.0.5 openpyxl==3.1.5 matplotlib==3.11.2 seaborn==0.13.2 pymoo==0.6.2` | 300 | 0 |
| S6 시험 도구 설치 | `V -I -m pip install X --no-index --find-links SP/reil_env18/wheels_test --no-deps --target SP/reil_env18/pytest_t pytest==9.1.1 pluggy==1.6.0 iniconfig==2.3.0 pygments==2.21.0` | 120 | 0 |
| S7 emit | §1-7 (env `PYTHONDONTWRITEBYTECODE=1` 추가) | 180 | 0 |
| S8 check | §1-7 · `check OK` · rc 0 | 180 | 0 |
| S9 old→new 대조 | a `P K records --venv SP/reil_env18/venv --target SP/reil_env18/pytest_t --records-out E/09_records --test-records-out E/09_test_tool_records --out E/09a_records.json` · b (a 가 rc 0 일 때만 — §3) `P K seal --new N --new-records E/09_records` **`--records-report E/09a_records.json`** `--out E/09b_seal.json` | 120 | 0 |
| S10 기록 · 커밋 | **(v2 정정 — ENV18-N2)** 커밋 전 기록 (`E/10_end.json` — PRE_COMMIT · S10 PENDING · 끝 porcelain 원문 · §1-1 보호 대조 · `du -sb` · 여유) → 비밀값 검사 → (남은 몫 ≥ 5 s 일 때만) `git add -f N E` → 스테이지 blob = 디스크 바이트 전수 대조 → 로컬 커밋 → (커밋 밖) `SP/reil_env18/11_after_commit.json` | 90 | 0 |

- 10월 §2 와 다른 argv 는 넷이다: S2 · S3 의 `I` (명시) · S4 · S9 의 새 대조기 · S7 · S8 의 출력 경로 · S0 의 대조기 호출. **(v2)** 다섯째는 S9b 의
  `--records-report`, 여섯째는 실행기를 하네스가 `-I -B` 로 부르는 꼴이다 (§2-1). 그 밖은 10월과 같다.
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
10. **(v2)** 승인 블록 · 요청서 · 실행기 / 하네스 / 대조기 sha 가 맞지 않음 · precheck 바깥 반환이 없거나 rc ≠ 0 (precheck · S0 · 쓰기 전).
11. **(v2)** 하네스 절대 상한 (precheck 90 s · run 1,860 s) — 그룹째 끊음 · rc 124 · 바깥 반환에 기록.
12. **(v2)** S10 의 남은 몫이 5 s 미만 — git add · commit 을 시작하지 않는다 (작업트리의 기록을 사후 문서 커밋).
- **(v2) 멈춤이 아닌 것:** `adoption_hold` 표지 (RECORD 밖 실행 경로 관련 파일) — 실행은 계속하고, 결과 검토에서 처분하기 전에는 채택하지 않는다.

하지 않는 것: 임의 재시도 · 패키지 판 완화 · 다른 interpreter · 새 경로 fallback · 코드 수정 · ensurepip 묶음 우회 (§7 Q3 의 B 안은 이 승인 밖이다). 실패 뒤 다음
걸음은 사용자에게 다시 묻는다.

## §4 결과 제출 · 수용 (10월 초안의 7 조건 + 검토자 복원 규칙 6 항)

| 조건 | 이 요청에서 |
|---|---|
| 1 승인 원문 · 고정 표 · 명령 · cwd · 원점 · 시작 / 끝 HEAD · 작업트리 목록 보존 (**v2**: 승인 블록 사본 `00_approval.json` · precheck 원문 `00_precheck_before_t0/` · 하네스 사본 · 10월 diff) | `E/00_*` 에 둔다: 승인 원문 사본 · 이 문서 sha · t0 · precheck 원문 · 실행기 사본과 10월 diff. 단계별 meta 에 argv · cwd · env 이름 · 시각 · rc 를 적고, porcelain 원문은 시작과 끝에 둔다 |
| 2 과학 배포판 · Python 판 / 빌드 · 플랫폼 / libc · BLAS / LAPACK · RECORD · 파일 대조 · 충돌 표를 old / new 나란히 | `E/09a_records.json` · `E/09b_seal.json` 을 결과 보고서의 사람용 표로 옮긴다. lock 의 `#@ files` 집계와 collision 줄 · wrapper 13 행 · 선언 1 행 · 설치 바이트 대조 수 · 관측 (RECORD 밖 파일) 도 포함한다 |
| 3 COBYQA 옵션 · 구현 파일 · Sobol 6 의 .npy sha 와 raw sha 를 각각 대조 | 바이트 동일 판정을 하고, 보고서 표에 sha 쌍을 하나씩 적는다 |
| 4 새 봉인과 옛 봉인을 각각 독립 식별 · 새 lock 을 과거 실행이 썼다고 소급 기록 금지 | 새 MANIFEST · lock · PROFILE 의 sha 를 따로 적는다. 옛 봉인 · C4-0 · C4-E 기록은 바이트 그대로 둔다 |
| 5 시간 · 디스크 · 최종 기록의 실제 관측 경계 (**v2 정정 — ENV18-N2**: 커밋 전 `10_end.json` 과 커밋 밖 `11_after_commit.json` · 하네스 `outer_return.json` 을 나눠 낸다) | t0 / 단계 시각 (monotonic) · `du -sb` 표본과 시점 · 커밋 뒤 관측 · 바깥 반환 원문을 낸다. 내부 snapshot 과 외부 wall 은 더하지 않는다 |
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
> **(v2)** 실행은 이 요청 커밋에 고정된 실행기 (`bf47d9f7a883…`) · 하네스 (`f4afd4b61cf5…`) · 대조기 (`0049e7e9a153…`) 로만 하며, 원장에 승인 블록 하나를 넣은 뒤 하네스로 precheck 1회 → run 1회만 부릅니다. 자식 env 에서 CA 관련 변수 넷을 빼 pip 의 CA 를 `PIP_CERT` 하나로 고정합니다.
>
> 원점 전 읽기 전용 점검 1회, **emit 1회와 check 1회만** 허용합니다. check 내부의 emit을 포함하여 **합성 COBYQA 최적화 총 2회, 전체 Sobol 생성 경로 총 2회**임을 수용합니다. 여기에는 seed/rng 비교 생성과 check의 임시 파일 쓰기도 포함됩니다. pytest·변이 시험·C5 재측정은 포함하지 않습니다.
>
> 전체 1,800초(S10의 커밋 포함)·디스크 2,000,000,000 B를 한도로 합니다. venv·다운로드·별도 시험 도구·봉인·임시 파일·기록의 새 파일을 합산합니다. 이 수치는 메모리 한도가 아니며 설치 완료 보증도 아닙니다. 미측정은 0 또는 PASS로 바꾸지 않습니다. 커밋 뒤 관측은 별도 문서 커밋으로 붙입니다.
>
> 설치 실패·배포판 집합/판/SHA 불일치·기존 경로 충돌·예산 초과·예상 밖 차이는 최초 오류와 확보된 기록을 남기고 중지합니다. 임의 재시도·패키지 판 완화·다른 interpreter·새 경로 fallback·코드 수정은 하지 않습니다.
>
> old→new 차이표와 새 MANIFEST를 제출하고 멈춥니다. 새 emit/check 성공만으로 새 봉인을 자동 채택하지 않습니다. 차이 검토가 수용된 뒤 그 봉인을 C4 환경으로 명시 연결합니다. **(v2 정정 — Q5)** C4-A 요청서 v4 (`85e148b4…`) 의 환경 결속 두 자리 — §4-3 (318 행) 의 C6 봉인 · §6-2 (458 행) 의 봉인 venv — 를 새 세대로 바꾸는 정정은 결과 검토에서 따로 확인받습니다. RECORD 밖 실행 경로 관련 파일로 채택 보류 표지가 서면, 그 처분 전에는 채택하지 않습니다. ensurepip pip wheel 의 출처 미확인은 남는 위험으로 알고 수용합니다 (원장 §138).
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

### 7-v2. §137 의 답 · v2 의 질문

- §137 의 답: Q1 (v4 결속 정정 2 줄) 수용 — 정확 좌표 · old→new · 새 식별 · 효력 조건을 담은 별도 정정 기록으로 · Q2 (C4-E 미이월) 수용 · Q3 (A 안) 조건부 → 사용자
  잔여 위험 수용 (원장 §138) · Q4 (RECORD 밖 파일) 한정 관측 수용 + 전체 목록 · 실행 경로 관련 보류 (§1-8 · v2).

| # | v2 의 질문 | 우리 안 |
|---|---|---|
| Q6 | 실행기 · 하네스의 계약 (§2-1 · §1-9) 과 시험 (샌드박스 · 변이) 이 §137 Q4 의 점검 목록 (원점 · 남은 시간 · 순수 Python 초과 · 첫 원인 · S10 · 바깥 반환 · 출력 부재 · timeout 과 절대 반환의 구분 · precheck 한도 · 실행기 폴더 디스크) 을 덮는가 | 덮는다고 본다 (§0-v2 의 마지막 두 줄 · §2-1 의 시험 표) |
| Q7 | 승인 블록 방식 (C4-A v4 §4-2 선례 · 실행기는 sha 를 품지 않고 블록과 대조) 이 승인 결속으로 충분한가 | 충분하다고 본다. 원장이 사용자 원문을 인용해 덧붙이는 기록이라는 한계 (블록을 쓴 사람의 인증 아님) 는 v4 와 같다 |
| Q8 | 남는 지적이 작은 P2 뿐이면 조건부 수용 (`ACCEPT_IF`) 으로 답해 줄 수 있는가 | 그 조건은 실행 전에 문서 정정 1 회로 반영하고, 반영 기록을 결과 검토 묶음에 넣는다 |

## §8 검토 발견 대응표 (§38 의 비차단 P2 넷)

> **(v2)** §137 의 판정: ENV-P2-01 = OPEN (N2 · 실행기 검토 대기) → v2 의 §1-9 · §2-1 · ENV-P2-02 = 원래 네 약점 보완 (정적 · 제출 증거 범위) · ENV-P2-03 = 결속
> 제안됨 (미실행) · ENV-P2-04 = 개선 (N1 필요) → v2 의 §1-5. §137 의 새 지적 (ENV18-N1 · N2 · C1 · C2) 은 §0-v2 표다. 아래 표는 v1 그대로다.

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

## §9-v2 v2 에서 한 것 (대조기 보강 · 실행기 · 하네스 · 합성 시험 · 실행 0)

- **대조기 v2** (`0049e7e9a153…`) — 재현 시험을 먼저 썼다. `bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/red_selftest.py` 를 v1 대조기 (`8cf10f3c…`) 로 돌린 RED 기록
  (`red.*`) 은 **52 / 62** — 새 사례 10 (R21 · R21b · R21c · R22 · R23 · R23b · R23c · S11 · S12 · S13) 이 모두 FAIL 이고, 특히 R21 (검토자 반례 그대로) 은 v1 이
  아무 문제도 내지 않았다. 고친 뒤 `selftest.py` **62 / 62** · 변이 증명 `mutation_proof.py` **18 / 18** (v1 의 M1–M12 + M13–M17 ·
  대조군 1).
- **실행기 · 하네스** — §2-1. 샌드박스 자체 시험 `selftest_runner.py` **22 / 22** · 실행기 변이 증명 `mutation_proof_runner.py`
  **11 / 11** (RM1–RM9 · RM6b · 대조군 1). 1 차 샌드박스 실행이 잡은 결함 (pyc → 보호 경로 더러워짐) · 변이 증명 1 차 개발 실행 8 / 9 (RM6 생존 →
  T2 강화) · 자체 검토가 잡은 요청서 경로 결속 (RED `red_runner.*` 21 / 22 → 고침 · 앞 최종 기록 `run1_*` 보존) 과 그 처리는 §2-1.
- **기록:** `bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/` (tree `6b29febe0afa950ec6ddd9d53a24dfdffc63fdda`) — 각 시험의 meta (argv · cwd · 시작 / 끝 · rc · 도구 sha) · stdout / stderr 원문 · `runner_vs_oct.diff`.
- **하지 않은 것:** venv · pip · 내려받기 · 설치 · emit · check · precheck · 네트워크 (PyPI) · pytest · 저장소 안 pyc 쓰기 (`-B`) 는 모두 0 이다. 샌드박스의 git
  커밋은 임시 저장소 안에서만 일어났다.
