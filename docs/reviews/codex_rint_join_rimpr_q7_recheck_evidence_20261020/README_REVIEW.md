# Rint 조인·Q7 독립 재확인 묶음

먼저 `codex_review_rint_join_rimpr_q7_recheck_20261020.md`를 읽는다.

- 현재 핀: `2b9efa253edbf455c2e1abfef1d60e51818e01f8`
- 대조 핀: `dcb97f1ed942f622d9189eee1a1e9432dc05a655`
- 판정: RIMPR-01·02 최소 해결 및 Q7 범위 한정 닫힘. 새 헤더 P3 RIMPRR-01. 기존 RIMPR-04의 false-PASS 범위 보강. ①′ 정량 채택·생산 HOLD 유지.
- 소스·Git·원장·사전등록 변경 및 생산 캠페인 없음.

## 내용

- `source/`: 현재 핀에서 내려받아 Git blob·SHA256으로 대조한 검토 자료 1,105개. 저장소 전체 복제 아님.
- `source_manifest.json`: 위 원본 바이트의 해시 목록.
- `submitted/`: 사용자가 첨부한 요청서.
- `probes/`: 독립 검사 및 제출 시험의 old/new 실행기.
- `evidence/`: 원본 로그, 결과 JSON, φ 배열, diff, Git tree 및 커밋 메타데이터.
- `notes/`: 구조 파서·수치·Q7의 세부 검토 메모. 최종 판정은 한국어 판정문이 우선.
- `tmp/`: 이 검토에서 만든 작은 입력 fixture. 실제 생산 출력 폴더가 아님.
- `support/resource.py`: Windows에서 메모리 보고만 대체하는 shim. 수치 계산 대체 아님.
- ZIP의 형제 폴더 `rint_g2_impl_reverify_20261015/`: 재현에 필요한 이전 핀 소스, manifest, 이전 판정 및 원본 조인 fixture.
- ZIP 최상위 `PACKAGE_MANIFEST.json`: 포장된 파일들의 SHA256. 이 명세 자체는 자기 해시 대상에서 제외.

## 재실행

ZIP은 두 검토 폴더가 서로 형제가 되도록 같은 부모 폴더에 푼다. Python 3.12, NumPy, SciPy가 필요하다. 이 검토는 NumPy 2.5.3 / SciPy 1.16.3을 사용했다. 소스와 fixture의 바이트를 변경하지 않는다.

아래는 두 폴더의 **부모 폴더**에서 실행한다.

```text
python -X utf8 -B rint_join_q7_recheck_20261020/probes/structure_minimal_replay.py
python -X utf8 -B rint_join_q7_recheck_20261020/probes/numeric_overflow_replay.py
python -X utf8 -B rint_join_q7_recheck_20261020/probes/numeric_overflow_replay.py --baseline
python -X utf8 -B rint_join_q7_recheck_20261020/probes/structure_probe.py
python -X utf8 -B rint_join_q7_recheck_20261020/probes/numeric_review.py
python -X utf8 -B rint_join_q7_recheck_20261020/probes/numeric_review.py --baseline
python -X utf8 -B rint_join_q7_recheck_20261020/probes/q7_independent.py
python -X utf8 -B rint_join_q7_recheck_20261020/probes/run_submitted.py new
python -X utf8 -B rint_join_q7_recheck_20261020/probes/run_submitted.py old
```

실행기는 기존 검토 환경의 선택적 의존성 폴더도 탐색한다. 해당 폴더가 없는 환경에서는 설치된 NumPy/SciPy 등으로 import한다. 필요한 의존성 누락은 환경 오류이지 시험 통과가 아니다. 전체 저장소의 `check_all` 실행 환경을 포장한 것은 아니다.

`old`는 현재 시험의 assertion을 옛 코드에 적용하므로 실패가 기대된다. `submitted_old.json`의 각 child 종료코드·원본 로그를 볼 것. 실행기 자체의 종료코드만 보고 회귀 전체 PASS라고 판단하지 않는다.

NaN/Infinity를 일부러 만든 탐침의 JSON에는 Python JSON 진단 표현 `NaN`, `Infinity`가 남아 있다. 이는 strict JSON 배포 형식이 아니라 오류 상태를 보존한 검토 증거다.

정상 Q7의 정밀 행렬 대조에는 동일한 직접해법 callback을 사용했고, 별도로 원래 CPU CG 비교도 실행했다. 두 경로의 결과를 서로 비트 동일하다고 주장하지 않는다.

경로·시간·환경 표지는 원래 검토 시점 기록이다. 포장을 다른 기계에 풀어 재현하면 절대경로·시간은 달라진다. 물리량과 거부/허용 상태를 비교한다.
