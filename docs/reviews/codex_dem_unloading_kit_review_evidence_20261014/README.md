# DEM 언로딩 키트 독립 리뷰 증거

판정문: `codex_review_dem_unloading_kit_20261014.md`.

핀: `2783061ead9f192ab742a2f0b14b0182a98a4966`.
판정: **HOLD**. 실제 작은 침대 이력 시험은 수용하지만 본 키트의 복원·판독·후속 관문에는 재현된 결함이 남아 있다.

## 다시 읽기

Python 3 표준 라이브러리만으로 다음을 실행한다.

```text
python -X utf8 -B reproduce.py
```

이 명령은 원본 해시를 확인하고, 동봉 실제 이력 시험 자료를 다시 판독하고, 합성 파일을 실제 Python 함수로 읽는다. 덱 시험은 입자 연산을 하지 않는 제어문 해석이다. DEM·MPI·SLURM·셸 러너·Git·네트워크는 호출하지 않는다. 출력은 이 리뷰 폴더의 `evidence/`에만 생성된다. **현재 핀의 결함을 재현하는 탐침이며 수정 코드의 합격시험이 아니다.**

`evidence/baseline.json`과 자체시험 로그는 성공과 Windows 셸 제한을 함께 보존한다. 셸 모의 시험은 전부 통과했다고 주장하지 않는다. 실제 이력 시험 원 TGZ는 `source/docs/reviews/dem_unloading_history_test_20261014/`에 있다.

`PACKAGE_MANIFEST.json`은 포장 파일별 SHA256이다. ZIP의 외부 영수증은 ZIP 자체 해시와 CRC/누락 검사를 담는다. 로컬 실행 결과 안의 절대 경로는 실행 당시 주소이며, 다른 경로에서 재현하면 달라질 수 있다.

`source/`, `upstream/`는 고정 소스 사본이다. 수정한 생산 코드나 새로운 시뮬레이션 결과가 아니다. `prepare_sources.py`와 `fetch_more_upstream.py`는 출처 수집 기록용이며, offline 재현에는 실행할 필요가 없다.
