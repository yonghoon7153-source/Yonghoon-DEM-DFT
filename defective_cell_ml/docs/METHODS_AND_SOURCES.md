# 문서·브랜치에서 차용한 내용과 범위

첨부 문서는 참고 자료로 읽었으며 문서 안의 지시를 실행 권한으로 취급하지 않았다. 문서 검토는 PDF 26개, 총 612쪽의 내용·도표 확인을 거쳤다. 브랜치 검토는 ML 관련 문서·코드 및 litdb 인덱스/핵심 digest를 선별한 범위로, 저장소 전체와 모든 논문을 정독했다는 뜻은 아니다.

## 적용한 원칙

1. **선택과 평가 분리.** 강의의 규제·검증 내용과 stoic의 중첩 검증 구조를 참고했다. DEM 전용 특징·임계값·제외 규칙은 옮기지 않았다. `ridge_capacity.py`에서 선택 전부를 바깥 학습 자료 안에서 수행한다.
2. **같은 생성원을 공유하는 표본 분리.** friendly 방법론의 그룹 검증 논점을 셀·제조 배치로 연결했다. 새 배치 일반화에는 실제 배치 식별자가 필요하다.
3. **단순 기준선과 공정한 비교.** 첨부 강의 D03/D26의 선형모델·정규화 내용을 기준으로 평균, 1 kHz 크기 단독, OCV 단독을 포함했다. 표본이 적다는 이유만으로 복잡한 모델이 우수하다고 가정하지 않았다.
4. **EIS 성분의 의존성.** Re/Im과 크기/위상은 같은 복소 측정의 표현이다. 보간 뒤 관계를 유지한다. 계수·대역 선택은 예측 모델의 의존도이며 결함의 원인 증명이 아니다. 주파수당 열은 4개지만 `mag=hypot(re,im)`, `phase=atan2(im,re)`로 유도되므로 **자유도는 2**다. 위상이 작은 저주파에서는 `mag≈re`, 고주파에서는 `phase≈im/re`가 되어 사실상 중복 열이 되고, Ridge/L2 Logistic은 같은 정보에 페널티 예산을 나눠 쓴다. 따라서 `03_reg_coefs`의 표준화 계수는 중복 표현 사이에서 임의로 분할된 값이며 **개별 특징 단위로 식별되지 않는다.** 계수의 부호·크기를 특징별 중요도로 읽지 않는다.
5. **라벨·점수·운영 임계값 분리.** 용량 미달 기준, Logistic 점수, 운영 판정선을 구분한다. 외부 검증이나 확률 보정을 완료한 것으로 표시하지 않는다.
6. **실패·제외 이력 유지.** 입력·실패 셀, 사전 제외 사유, 선택 파일, 실행 환경과 코드 해시를 남긴다.

## 주파수 격자와 후보 대역의 근거와 한계

기본 격자는 0.01 Hz–1 MHz의 decade당 1점 9개이고, 후보 대역은 `single_1e3`(1 kHz), `band_1e3_1e5`(1e3–1e5 Hz), `band_low`(0.1–10 Hz), `full`(전체) 네 가지로 고정되어 있다. 이 구성은 **사전에 고정한 저해상도 표현**이며, 아래 한계를 알고 쓰는 것이 전제다.

- 대역과 물리 과정의 대응은 가설 수준이다. 대략 고주파(≥1 kHz)는 SE 벌크·입계와 접촉 저항, 중간 주파수(10 Hz–1 kHz)는 복합 양극 계면·전하전달, 저주파(≤10 Hz)는 확산·분극 쪽으로 읽히지만, 황화물 ASSB에서 이 시간상수들은 서로 겹친다. 대역 선택 결과를 특정 계면의 원인 증거로 읽지 않는다.
- 고정 4개 대역에는 **10 Hz–1 kHz 단독 후보가 없다.** 100 Hz·0.01 Hz·1 MHz 격자점은 `full`에만 들어간다. 사용자 정의 대역을 설정으로 넣는 기능은 없다.
- decade당 1점 격자는 반원 정점을 직접 담지 못한다. 예를 들어 특성 주파수 300 Hz인 반원은 격자에서 100 Hz와 1 kHz 두 점으로만 보이므로, 시간상수 이동에는 민감하지만 저항 크기 자체를 담지 못한다.
- 로그 주파수 선형 보간의 오차는 원시 sweep 밀도에 달려 있다. 25 Ω 규모의 arc에서 decade당 6점 이상이면 보간 오차가 0.2 Ω 이하로 무시할 만하지만, 3점이면 0.7 Ω, 2점이면 1.4 Ω 수준까지 커져 셀 간 차이와 비교 가능한 크기가 된다. **원시 sweep은 decade당 6점 이상을 권장한다.** 현재 `data_audit.json`에는 `raw_rows`와 `support_hz`만 기록되므로 decade당 점수는 사용자가 두 값으로 확인해야 한다.
- 100 kHz 이상 격자점은 배선·셀 인덕턴스가 지배할 수 있어 계면 정보로 읽기 어렵다.

## 추가 자료 확보 후 검토할 후보

GPR의 불확실성, TabPFN, DRT·등가회로 특징, 앙상블, 배치별 calibration, permutation 중요도와 능동 실험 설계는 이번 패키지에 기본 모델로 넣지 않았다. 새 후보를 지표가 좋아 보이는 순서대로 추가하면 선택 편향이 다시 생긴다. 별도 실험 설계와 원시 자료·표본 수가 필요하다.

litdb의 Kim/Choi 임피던스 논점은 압력·SOC·계면 조건을 관리하고 EIS를 원인별로 과해석하지 않는 근거로 사용했다. Hollmann의 TabPFN과 Duquesnoy의 제조 최적화는 후속 비교 후보로만 남겼다. 양쪽 브랜치에 중복되는 문헌을 독립 증거 두 건으로 세지 않았다. digest 내용은 원 논문의 모든 세부 수치를 독립 검증한 자료와 구분했다.

## 추적 가능한 출처

- 원본 ZIP SHA-256: `064c66181a50cf33eb01f4400c00a1bb7d721334f760ec94913e758aa5aacd0b`
- friendly 검토 시점: `634da438bf329b4e4baccd19c37e009a7168d67f`
- stoic 검토 시점: `be0ae956895cc7fb06817c427cff465aee9b4758`
- [stoic 중첩 검증 코드](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/be0ae956895cc7fb06817c427cff465aee9b4758/scripts/nested_cv_sat.py)
- [friendly 방법론 이전 카드](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/634da438bf329b4e4baccd19c37e009a7168d67f/kb/methodology/microstructure_ml_transfer_to_cascade_2026_08_25.md)
- [stoic EIS/DRT 자료](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/be0ae956895cc7fb06817c427cff465aee9b4758/docs/eis_drt_ica_cv.md)
- [Kim 2025 digest](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/634da438bf329b4e4baccd19c37e009a7168d67f/litdb/papers/kim2025_impedance_decoupling_tlm_assb.md)
- [Choi 2024 digest](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/634da438bf329b4e4baccd19c37e009a7168d67f/litdb/papers/interfacial_impedance_formulation_assb_cathode.md)
- [Hollmann 2025 digest](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/634da438bf329b4e4baccd19c37e009a7168d67f/litdb/papers/hollmann2025_tabpfn_tabular_foundation_model.md)
- [Duquesnoy 2023 digest](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/634da438bf329b4e4baccd19c37e009a7168d67f/litdb/papers/duquesnoy2023_ml_multiobjective_manufacturing_optimization.md)
- [scikit-learn 중첩 CV 설명](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html)
- [확률 보정의 의미와 한계](https://scikit-learn.org/stable/modules/calibration.html)

상세한 1차 구조 검토, 문서별 정독 기록, 2차 반증 보고서는 `docs/reviews/`에 동봉했다. 이들은 각 단계 당시의 상태를 기록한 문서다. 실행·설정은 현재 README와 `docs/CHANGES.md`를 따른다.
