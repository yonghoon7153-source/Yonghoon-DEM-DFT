# 재현 안내

리뷰 본문: `codex_review_rint2_rr_round1_20261026.md`.
핀: `9bec6b7646374daed0d3edbb9647f9f46d302750`. 비교: `0b3012460fb8e8b7d53484b0efe399e2dc506aec`.

ZIP에는 검토에 쓴 `repo/`, `baseline/`, `historical/`의 읽기 전용 사본과 증거/탐침이 들어 있다. 전체 Git checkout이나 전체 test fixture 모음은 아니다. 생산 소스를 수정하거나 원격 Git에 기록하지 않는다. 아래 명령은 작은 합성 회로·판정·프로세스 시험만 실행한다. S0·DEM·GPU·R 생산 런은 없다.

## 환경

독립 실행: Windows / Python3.12.14 / NumPy2.5.3 / SciPy1.16.3 / BLAS 스레드1. NumPy/SciPy 의존 라이브러리 자체는 ZIP에 넣지 않았다. 이 두 라이브러리가 설치된 Python으로 실행한다. 제출자의3.8·3.11 로그와 이 독립 실행은 별개다.

탐침은 현재 묶음의 `repo/scripts`를 먼저 import한다. 기존 로컬 캐시 경로도 bootstrap에 있지만 해당 경로가 없는 다른 컴퓨터에서는 설치된 Python 라이브러리를 사용한다. 캐시가 있는 원래 작업공간에서 다른 환경을 시험하려면 그 캐시 경로 삽입을 제거하거나 묶음을 다른 폴더로 풀어라. 생산 모듈은 바꾸지 않는다.

현재 로컬 Python:
`C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`

명령의 현재 디렉터리 = 이 README가 있는 리뷰 루트. PowerShell에서 아래 환경을 먼저 둔다.

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPATH=(Join-Path (Get-Location) 'repo/scripts')
$env:TEMP=(Join-Path (Get-Location) 'tmp')
$env:TMP=$env:TEMP
New-Item -ItemType Directory -Force $env:TEMP | Out-Null
```

## 핵심 반례와 독립 검산

```text
python -X utf8 -B evidence/agent_sv/probe_actual.py
python -X utf8 -B evidence/agent_sv/probe_weighted.py
python -X utf8 -B evidence/agent_sv/probe_deferred.py
python -X utf8 -B evidence/agent_sv/probe_rounding.py
python -X utf8 -B evidence/agent_sv/run_resident_sm.py
python -X utf8 -B evidence/agent_chain/chain_review_probe.py --repo repo
python -X utf8 -B evidence/agent_runtime/probe_runtime.py
python -X utf8 -B evidence/agent_runtime/probe_diagnostic_overflow.py
python -X utf8 -B evidence/agent_runtime/run_targeted_tests.py
python -X utf8 -B evidence/q9_design_probe.py
```

`probe_actual`은 real producer→증서→실제 ca_ext 계약→SV 판정을 실행한다. 전체 사슬의 파일/등록 `read_run`은 실행하지 않는다. `probe_weighted`는 생산 조립 결과를 잡아 별도 정확 유리수 소거를 한다. `q9_design_probe`의 자식은 잠깐 기다렸다가 합성 표지만 쓰고 종료한다. 부모 사망 처리의 플랫폼 사실을 보는 시험이며 수치 solver가 아니다.

선택 상주 검사:

```text
python -X utf8 -B repo/scripts/test_carbon_junction.py --only QD2,QD3,QD4,QD5,QD6,QD7
python -X utf8 -B repo/scripts/test_ca_ext_b6.py --only S --skip-payload
```

기록된 결과:126/126,254/254. B6 payload subgroup은 의도적으로 생략했다. 직접 SM37개는 겹치는 검사이므로254와 합쳐 독립 검사 수로 보고하지 않는다. 런타임30개와 T24의8개 역시 범위가 다른 선택 실행이다.

## 이전 탐침의 스키마 적응

원래10-22 탐침/JSON은 `evidence/prior_artifact/`에 bytes 그대로 보존했다. 어댑터는 합성 팔의 증서 구간/scale만 더하고 생산 함수는 변경하지 않는다.

```text
python -X utf8 -B evidence/agent_chain/registration_adapter.py --repo repo --original evidence/prior_artifact/probe_registration_current.py --label current
python -X utf8 -B evidence/agent_chain/registration_adapter.py --repo baseline --original evidence/prior_artifact/probe_registration_current.py --label baseline
python -X utf8 -B evidence/agent_chain/compare_registration.py
```

기대:baseline↔원결과466 scalar leaves 동일, 현재↔baseline에서 R단조절 제외457 동일, 그 절만 새 STOP. `comparison.json`에 검산한 소스 지문이 있다. 기존 증거 JSON의 절대경로는 실제 실행 당시 자리라서 현재 묶음 위치와 다를 수 있다.

## 판정의 한계

- 현재 fresh 실험은3.12 환경이다. 3.8.20 제공 로그를 재실행했다고 쓰지 않는다.
- Q9는 설계다. 합치기·회복 프로세스·원장 전체를 구현해 테스트한 것이 아니다.
- k=0의1.01 문턱은 허용되는 예시다. 생산 문턱은 미봉인이므로 실제 생산 오분류율이 아니다.
- 정상 생산자가 잘못된 G를 낸다는 반례가 아니라, 같은 런의 다른 끝 증서를 옮긴 기록이 소비자에서 통과하는 반례다.
- 기존 알려진X6/X3/X5, origin/SV범위 한정은 그대로다.

`final_integrity.json`은 판정 작성 뒤 받은 소스의 Git blob/SHA256가 바뀌지 않았음을 기록한다. `MANIFEST.sha256`는 배포 파일 목록이다. 재실행하면 일부 증거 JSON/로그가 갱신되므로 비교하려면 원 ZIP을 따로 보존하라.
