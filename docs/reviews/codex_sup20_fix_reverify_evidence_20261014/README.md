# 보충 20 수정 재검증 증거

판정문: `codex_review_sup20_fix_reverify_20261014.md`.

대상 핀: `a9422d2e772f28417a6e0a5167aaab8d987bf27a`.
기준 핀: `b429c3c1df0956d2721861d89cc29a2d56f2b581`.

결론: SUP20-01·02 닫힘. 신규 P1 없음. dry-run 입력 연결·미완료 로그 수용에 신규 P2 SUP20R-01·02. 실제 발사와 배포 무조건 GO 아님.

## 구성

- `source/`: Git blob SHA와 SHA-256으로 확인한 부분 스냅샷 1,053파일. Git checkout은 아니며 외부 라이브러리를 포함하지 않는다.
- `baseline/`, `evidence/*.diff`: 바뀐 기존 코드와 diff.
- `probes/`: 옛 탐침 두 개는 무변경, 신규 탐침 세 개는 독립 대조용.
- `evidence/`: 실제 로컬 실행 로그·결과·반례 로그. `receipt_extra/`의 manifest와 로그는 합성 시험이며 생산 실행 증서가 아니다.
- `notes/`: 분야별 보조 검토 메모. 최종 등급·범위는 판정문이 우선한다.
- `source_manifest.json`, `tree.json`, `compare.json`: 고정 핀·원본 파일 신원.
- `submitted/request.md`: 사용자 첨부 요청서 원문.
- `MANIFEST.sha256.json`: 이 패키지 파일별 SHA-256.

원본 소스·설계·수치 봉인·원장 수정 없음. 실제 시뮬레이션/194/20 생산/WSL preflight 없음. 로컬 Windows 부분 스냅샷 시험의 한계는 판정문 §7에 적었다. `recorded.git.sha=null`은 부분 스냅샷이라는 뜻이며 새 핀으로 위장하지 않았다.

## 재현

일반 Python 3과 numpy/scipy/matplotlib 등 대상 리포의 검사 의존성이 필요하다. `run_checks.py`는 이전 탐침과 함께 무변경 보존했으며, 현 호스트의 두 추가 deps 경로를 PYTHONPATH에 넣는다. 다른 호스트에서는 그 경로 대신 리포 의존성을 설치한 환경을 사용한다. `run_receipt.py`는 같은 실행 환경을 재사용한다.

Linux에서는 검토 폴더에서 `TMPDIR`를 존재하는 시험용 `tmp`로 지정하고 실행한다. Windows에서는 `TEMP`/`TMP`도 같은 경로로 지정할 수 있다. 원본 리포 대신 `source/`만 읽으며 임시 합성 자료·플롯은 시험 폴더에 생성한다.

```bash
python -X utf8 -B run_checks.py release builder dataset design_probe release_probe receipt_extra
python -X utf8 -B run_receipt.py
python -X utf8 -B probes/release_extra.py
python -X utf8 -B probes/design_extra.py
python -X utf8 -B verify_evidence.py
```

`verify_evidence.py`는 **현재 결함이 재현됨**을 확인한다. 따라서 이 스크립트의 성공을 후보 수정 코드의 합격으로 읽지 않는다.

옛 탐침의 JSON 안 pin 문구는 기준 핀으로 하드코딩돼 있다. 무변경 조건 때문에 유지했다. 실제 재실행 대상은 `source_manifest.json`의 현 핀이다.

패키징은 `tmp/`, `__pycache__/`, 컴파일 캐시와 패키지 자기 자신만 제외한다. 출력 원문과 두 잘못된 로그를 모두 보존한다. 리포에 반입할 때 코드·실행 파일로 오인하지 않도록 증거 디렉터리 안에 둔다.
