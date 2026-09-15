# 예제 입력

이 폴더의 CSV·TXT·MPT는 모두 **가상 데이터**다. 실제 셀 측정값과 학습 완료 모델은 포함하지 않는다.

`demo_features.csv`는 가상 12셀의 용량·CC 비율·EIS 특징을 담는다. `raw/cycle`과 `raw/eis`는 같은 수치를 원시 입력 형식으로 옮긴 파일이며 장비의 모든 출력 변형을 재현하지는 않는다. `selection_manifest.csv`는 선택 파일과 가상 배치 3개의 대응표다.

`new_features.csv`와 `raw/new_eis`는 예측 경로를 확인하려고 같은 가상 특징에 새 셀 번호 61–72를 붙였다. 독립 신규 셀 검증 자료가 아니다. 예측 라벨이나 점수를 성능 근거로 사용하지 않는다.

CSV/원시 예제를 학습할 때 `--synthetic-data`를 붙여 결과·모델에 가상 데이터 표시를 남긴다. `--demo`는 자동 표시한다. 실제 측정 자료 실행에서는 이 옵션을 생략한다.

`config_eis_only.json`은 OCV를 사용하지 않는 예시다. `config_group.json`은 바깥 배치 하나를 통째로 남기는 평가 예시이며 `batch_id`가 필요하다. 두 설정은 부분 패치가 아니라 전체 설정 파일이다.

`raw/cycle`의 가상 cycler 파일은 `|Q|(Ah)` 열을 직접 써 넣은 것이라 같은 파일의 `Current(A)`·`Test Time(s)`를 적분한 값과 일치하지 않는다. 형식 검증용 픽스처이며 쿨롱 정합성을 시험하는 자료가 아니다.

`python examples/generate_examples.py`는 이 폴더의 예제와 기본 `config.json`을 다시 생성한다. 수정한 설정이 있다면 실행 전에 별도로 보관한다. 일반 실행에는 재생성이 필요 없다.

**배포본 무결성을 확인하기 전에는 재생성하지 않는다.** 다른 OS에서 실행하면 `np.hypot`의 플랫폼 libm 차이(마지막 자리 1e-15 수준)와 줄바꿈 차이(CRLF↔LF) 때문에 `demo_features.csv`·`new_features.csv`·`raw/eis`·`raw/new_eis`가 배포본과 비트 단위로 달라져 `MANIFEST.sha256` 검증이 깨진다. 학습 결과의 의미는 달라지지 않지만, 재생성 후에는 `MANIFEST.sha256`도 함께 다시 만들어야 한다.
