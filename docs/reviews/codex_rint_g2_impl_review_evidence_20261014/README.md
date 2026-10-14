# Rint G2 ①′ 재검토 전달 묶음

## 먼저 읽을 것

정본 판정: **[codex_review_rint_g2_impl_20261014.md](codex_review_rint_g2_impl_20261014.md)**

- 고정 커밋: `1087a9b2f4a93aa6a3b0debc698a14fffa13488d`
- 브랜치: `claude/stoic-knuth-NObVQ`
- 사용자 승인으로 최신 조회 후 고정. 조회 두 번 동일.
- 판정: RINTV-01·02 제한적 닫힘, 신규 P2 5건·P3 1건, 정량 채택·생산 HOLD 유지.
- 코드·원장·Git 상태 변경 없음. 원격/생산 시뮬레이션 없음. 소규모 CPU FV·기하·원자료 진단만 수행.

## 파일 구성

| 위치 | 내용 |
|---|---|
| `codex_review_rint_g2_impl_20261014.md` | 최종 한국어 판정문·Q1–Q10·해제 조건 |
| `submitted/user_request.txt` | 사용자가 제출한 요청문 사본 |
| `source/` | 핀에서 읽은 769개 검토 파일; 전체 저장소는 아님 |
| `source_manifest.json` | 각 소스 경로·Git blob·SHA256 대조 목록 |
| `source_prior/step3_sigma.py` | 이전 검토 스냅샷의 OFF 비교용 모듈 |
| `probes/` | 독립 반례·기하/순열·호환성 검산 |
| `evidence/` | JSON 수치, 기존 시험 로그, 루트 재실행 기록, Git tree |
| `notes/` | 병렬 검토의 근거 메모; 제안 등급은 초안이며 최종 판정문이 우선 |
| `artifact_manifest.json` | 전달 파일의 크기·SHA256; 이 목록 자신은 제외 |

`tmp/`의 재생성 가능한 변이 덤프와 캐시는 압축본에서 제외했다. 환경의 과거 작업 폴더, NumPy/SciPy 설치물도 포함하지 않는다.

## 재현

ZIP을 풀 때 최상위 폴더명 **`rint_g2_impl_review_20261014`**를 유지한다. 그 폴더 안에서 Python과 NumPy/SciPy가 있는 환경으로 실행한다. 탐침은 핀의 `source/scripts`를 읽으며, 원본이 아니라 `tmp/`에 합성/변이 입력을 만든다. 일부 탐침은 이 워크스페이스의 기존 과학 라이브러리 경로를 우선 탐색하지만, 해당 경로가 없으면 설치된 NumPy/SciPy로 실행 가능하다.

PowerShell 환경 예:

```powershell
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
New-Item -ItemType Directory -Force -Path './tmp' | Out-Null
$env:PYTHONPATH = (Resolve-Path './source/scripts').Path
$env:TEMP = (Resolve-Path './tmp').Path
$env:TMP = $env:TEMP
python -B probes/rrm_probe.py
python -B probes/join_adversarial.py
python -B probes/join_synthetic.py
python -B probes/join_global_precision.py
python -B probes/owner_vox_mismatch.py
python -B probes/owner_independent.py
python -B probes/off_compatibility.py
```

일부 탐침은 JSON을 표준 출력으로, 일부는 `evidence/` 파일로도 기록한다. 재실행 전 전달 원본을 보존하려면 묶음을 별도 위치에 복사한다. `rrm_probe.py`의 경계 대조와 row mutation은 **탐침 프로세스 내부의 독립 실험**이며 `source/` 파일을 패치하지 않는다. 반례의 row fingerprint 재계산은 의미 검사와 우발 변조 검사를 구분하기 위한 것으로 판정문에 한정했다.

### 제공 시험

```powershell
python -B source/scripts/test_rint_g2_am_iface.py
python -B source/scripts/test_rint_g2_rrm.py
python -B source/scripts/test_rint_g2_join.py
python -B source/scripts/test_rint_t2_dev.py
python -B source/scripts/step3_sigma.py --selftest
python -B source/scripts/step3_sigma.py --selftest-rint
```

T4 두 시험은 Linux에서는 해당 파일을 직접 실행한다. Windows에서는 Unix `resource` import를 수치 결함과 혼동하지 않도록 다음 어댑터를 사용했다.

```powershell
python -B probes/windows_telemetry_bootstrap.py test_rint_t4_census.py
python -B probes/windows_telemetry_bootstrap.py test_rint_t43_order.py
```

어댑터는 `ru_maxrss=NaN`으로 메모리 계측만 대신한다. 실제 기하·계수·솔버·기대값은 그대로다. 최초 import 실패도 `evidence/baseline_*`에 남겼다. 작은 풀이 일부에는 동일한 직접 sparse solve를 대조군 양쪽에 사용했으며 각 탐침과 판정문에 명시했다.

## 검토 한계

- 독립 T4 반복은 세 침대 **h=0.4 µm**까지만. h=0.15 및 실침대 σ 재실행은 하지 않았다.
- 제출 σ_OFF 최대 0.338%는 제출된 계산 범위에 한정해 인용했다.
- 미공개 생산 프레임·첨가제·물성·실행 이력은 인증하지 않았다.
- 16개 OFF 비교 통과는 전 입력의 동등성 증명이 아니다.
- 원래 생산 코드와 원장 수정, D12-V 저자 숫자 선택, 생산 발사는 이 산출물에 포함되지 않는다.

`prepare_source.py`, `run_review_tests.py`, `verify_evidence.py`는 이 워크스테이션의 수집·교차실행 보조 도구다. 경로/첨부 파일에 의존하므로 다른 환경에서 반드시 재실행할 필요는 없다. 핵심 재현 진입점은 위 `probes/`다.
