# 재현 안내 — 문서·정적 범위만

이 폴더의 판정문과 scope_verdict.json이 최종 범위다. input/은 받은 ZIP의 바이트 사본이며 수정하지 않았다. DELIVERY_VALIDATION은 작성 측 증거다. 이 검토의 독립 근거는 루트 검증 JSON 및 task/에 구분했다. 실제 연구 결과는 0건이다.

현재 폴더에서 다음을 실행하면 패키지 해시·Git blob·캐시된 원격 메타데이터·변경 범위를 다시 읽어 package_recheck.json을 만든다.

```sh
python -I -B -X utf8 verify_package.py
```

이 재현은 네트워크 없이 보존된 원격 응답을 대조한다. 검토 때 실제 조회한 고정 핀의 응답은 remote_* 파일, D0.7 공개 문서는 d07_remote_document.json 및 d07_readme_cc1a9679.md에 있다. 현재 원격 상태나 실제 호스트 완료를 새로 확인하는 명령이 아니다.

수행 환경은 Windows, Python 3.12.14였다. 실제 ibb/WSL/원덤프를 읽거나 inventory·시뮬레이터·회귀·전체 게이트를 실행하지 않았다. 원장 및 입력 파일을 변경하지 않았다. 재현 안내도 이 경계를 확장하지 않는다.

## 메모리 덱 정적 대조

검토에 사용한 로컬 Python에는 NumPy/SciPy가 설치되어 있었다. 다음은 덱 bytes 8개를 메모리에서 만들고 독립 명령 파서로 해시·명령·계획 시간을 읽는 한정 탐침이다. 덱 파일 작성이나 DEM 실행이 아니다.

```sh
python -I -B -X utf8 task/damping_static/static_probe.py
```

static_probe.json의 cases, 비교 결과, source_unchanged 및 forbidden_side_effect_attempts를 읽는다. 생성 중 파일 쓰기·프로세스·네트워크를 거부한 시도는 0이며 input/ 32파일은 전후 동일했다. 초기 결과 static_probe_original_path.json은 그대로 보존했다. 이후 탐침의 ROOT만 상대 경로로 고친 재실행 결과는 바이트 동일하다(harness_portability_check.json). 이를 추가 시험 8건으로 세지 않는다.

task/damping_definitions의 산술은 합성 예시이며 기존 합성 suite 또는 실제 관측이 아니다.
