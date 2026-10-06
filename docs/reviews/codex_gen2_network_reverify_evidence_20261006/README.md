# 접촉망 세대 2 재검증 묶음

대상 커밋: `165d0cf61a3e15367a3d1bf68e8f98178b70c25c`.
판정문: `codex_review_gen2_network_reverify_20261006.md`.

원본 저장소와 생산 코드는 수정하지 않았다. `source/`는 고정 Git blob 복사본이며 `source_manifest.json`으로 확인한다. 반례 변이는 `evidence/`의 검토용 자료에만 적용했다. DEM/MPM 및 새 194 실행은 없다.

## 읽는 순서

1. 판정문 Q1–Q7 및 G2RR-01–03.
2. `evidence/acceptance.json`: 실 생산·게시·인계 경로 반례.
3. `evidence/adversarial.json`, `numerics.json`, `real_beds.json`: 실제 수치 함수 재계산.
4. `evidence/reread_extra.json`: 실제 검산기 CLI의 등록 큐 반례.
5. `evidence/tests.json` 및 각 로그: 598 통과·3 SKIP, 14 진입점 rc=0.

## 재현

Python 3와 NumPy, SciPy, NetworkX, Flask, pandas 및 해당 웹앱의 import 의존성을 준비한다. 실행 버전은 `evidence/environment.json`에 있다. 이 묶음을 원 저장소 밖의 별도 폴더에 풀고 최상위에서 실행한다. `reread_extra.py`는 원 검산기의 위치 기반 REPO 탐색 규약 때문에 상위 경로에 `docs`라는 디렉터리가 없는 곳에서 실행한다.

```bash
python3 verify_bundle.py
python3 run_tests.py
python3 probes/adversarial.py
python3 probes/numerics.py
python3 probes/acceptance.py
python3 probes/real_beds.py
python3 probes/reread_extra.py
python3 verify_evidence.py
```

`verify_bundle`은 재실행 **전** 보존본 검증용이다. 재실행하면 새 실행 ID·로그·시간 때문에 evidence의 파일 해시가 달라진다. `verify_evidence`의 PASS는 **기록한 반례가 재현됨**을 포함한다. 따라서 이 도구의 PASS를 생산 승인으로 읽으면 안 된다.

회귀의 SKIP 3개는 원 Git 객체를 읽는 옛 모듈 비교다. 검토 복사본에는 `.git`을 넣지 않았다. 이전 독립 검토의 `prior_real_beds.json`과 현 핀의 실침대 수치 비교는 별도로 보존했다. 전체 check_all 또는 새 194 완료를 주장하지 않는다.

`tmp/`와 다운로드 중간 파일은 배포하지 않는다. `run_tests.py`는 필요할 때 이 묶음 안에 임시폴더를 만든다. Windows 원 실행은 로컬 의존성 폴더를 PYTHONPATH에 추가했으며, 다른 환경에서는 설치된 패키지를 사용하면 된다.
