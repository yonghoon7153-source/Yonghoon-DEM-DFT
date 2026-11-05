# 재현 안내 — 문서·정적 범위만

이 폴더의 판정문과 scope_verdict.json이 최종 범위다. input/은 받은 ZIP의 바이트 사본이며 수정하지 않았다. DELIVERY_VALIDATION은 작성 측 증거다. 이 검토의 독립 근거는 루트 검증 JSON 및 task/에 구분했다. 실제 연구 결과는 0건이다.

현재 폴더에서 다음을 실행하면 패키지 해시·Git blob·캐시된 원격 메타데이터·변경 범위를 다시 읽어 package_recheck.json을 만든다.

```sh
python -I -B -X utf8 verify_package.py
```

이 재현은 네트워크 없이 보존된 원격 응답을 대조한다. 검토 때 실제 조회한 고정 핀의 응답은 remote_* 파일, D0.7 공개 문서는 d07_remote_document.json 및 d07_readme_cc1a9679.md에 있다. 현재 원격 상태나 실제 호스트 완료를 새로 확인하는 명령이 아니다.

수행 환경은 Windows, Python 3.12.14였다. 실제 ibb/WSL/원덤프를 읽거나 inventory·시뮬레이터·회귀·전체 게이트를 실행하지 않았다. 원장 및 입력 파일을 변경하지 않았다. 재현 안내도 이 경계를 확장하지 않는다.

## LHS 정적 경계

task/lhs_boundary/static_comparison.json의 25개는 JSON·해시·문서 경계를 확인한 정적 술어다. 실행 시험 25개가 아니다. NOT_COLLECTED template의 status를 제외한 26개 필드는 모두 null이고 rows=[]/measured_rows=0이다. pressure_inventory.sh는 텍스트/해시로만 대조했으며 실행하거나 import하지 않았다.

task/common_definitions는 두 초안 공통 정의 검토 사본이다. 합성 산술을 LHS 관측/회귀로 세지 않는다. 최초 작성자의 scratch 원문은 제공되지 않았으므로 그 최초 원본과의 동일성은 미인증이다.
