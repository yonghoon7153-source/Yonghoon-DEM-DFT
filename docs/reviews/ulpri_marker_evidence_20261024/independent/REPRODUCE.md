# 독립 표지 검사 재현

Python 표준 라이브러리만 사용한다. 아래에서 스크립트가 있는 디렉터리로 이동하고 checkout 경로를 실제 검토 판으로 바꾼다. 각 출력 경로는 새 경로여야 한다. 모든 생성·변이 파일은 지정한 출력 아래에만 둔다. 실제 연구 실행이나 Git 작업은 하지 않는다.

```bash
python3 -I -B probe_marker_boundaries.py \
  --repo /path/to/checkout --output /tmp/ulpri-independent-cli
python3 -I -B probe_single_marker.py \
  --repo /path/to/checkout --output /tmp/ulpri-independent-single
python3 -I -B probe_marker_mutants.py \
  --source /path/to/checkout \
  --expanded /tmp/ulpri-independent-cli \
  --single /tmp/ulpri-independent-single \
  --output /tmp/ulpri-independent-mutants
```

기대 결과는 62/62, 22/22, 의미 변이 6/6이다. 변이 도구는 kit와 명시된 원 덱 archive·보조 모듈만 scratch에 복사하며 전체 checkout이나 Git 데이터베이스를 복사하지 않는다. 기록된 수정 reader SHA256과 실제 소스 지문을 함께 확인한다.

첫 두 스크립트는 기준 핀에서도 실행할 수 있다. 그때에는 아직 없는 거부 동작 때문에 의도적으로 FAIL이다. 보존된 기준 결과와 수정 결과를 대조하면 양성 유지와 음성 해소를 구별할 수 있다. 두 종류의 PASS나 내부 변이 검출은 외부 재확인 GO 또는 실제 물리 실행 자격이 아니다.
