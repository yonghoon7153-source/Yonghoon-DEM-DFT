# 83차 게이트 라운드 1 종결 검토

2026-09-30. **G82-N1 P1·G82-N2 P1·G82-N3 P2 종결을 수용한다. 승인된 단계 3 라운드 1의 구현 범위는 종결이다. 이번 범위에서 새 차단 발견은 없다.**

새 validator 세대의 영수증도 수용한다. 이 판정은 실행 GO, 새 연구 leg, 라운드 2 착수 또는 단계 3 전체 완료가 아니다. 76차 종결과 grid_fit_v5 진단 전용 상태를 유지한다.

## 1 대상과 검토 방법

- 판정 코드: `ea2af59e68a85b561c3e185f66b815aec877ca57`.
- 요청문·발송 HEAD: `78e1f518024d0a9c4d00ee7f6784fa8949554325`.
- 독립 재계산한 source digest: `7187bd31740514d4`.
- 비교 기준: 82차 수신 검토와 당시 코드 `c82231c4` 및 발송 HEAD `8f54427c`.

GitHub의 고정 커밋 파일을 읽고 UTF-8 바이트의 Git blob SHA를 대조했다. src/tools/configs/scripts의 재귀 Git tree 네 개와 루트 run.sh/requirements 파일 목록을 확인해 RUN_SCOPE 58개 파일 집합을 재구성했다. 네 tree는 모두 비절단 응답이며 파일별 blob과 일치한다. 실제 코드의 경로 정렬·해시 정의를 읽고, 검토자 자체 코드로 digest를 계산했다. 원격 dirty 작업 사본이나 전체 실행 환경을 조사한 것은 아니다.

이전 발송 HEAD→RED까지 RUN_SCOPE 변경 없음, RED→GREEN 한 커밋에서 승인된 네 파일 변경, GREEN→판정 커밋 변경 없음, 판정→발송 HEAD는 문서 세 파일만 변경인 것을 compare와 파일 바이트로 확인했다. 비교 응답은 각각 300개 미만이며, scope 파일은 별도 tree 목록과 대조했다. 시작 전 표 §10의 dfdd91a9 바이트도 최종 표와 같다.

이번 검토는 **소스·AST·정적 반례/검사 연결·영수증 데이터 대조**다. 받은 함수/모듈을 import하거나 추출 실행하지 않았다. pytest·변이 재생·smoke·분석 프로그램·COMSOL·JVM·복원·영수증 생성은 0회다. 2023 passed·1 xfailed, smoke rc0, 12/12 및 docs-lint 358 passed는 발신자의 고정 커밋 관측으로 기록하며 수신 재실행 실측으로 바꾸지 않는다.

근거: IDENTITY_AUDIT.json, STATIC_AUDIT.json, PRODUCTION_DIFF.patch, evidence의 커밋 고정 응답.

## 2 G82 N1 관측 roster 재구성 종결

**닫힘을 수용한다.** 시작 전 SHA를 그대로 복사하던 경로가 제거됐다.

`observed_roster`는 실제 fits 행의 cond_id를 봉인 curves 조건에 연결하고, lli/lam/type/noise를 행별로 대조한다. 각 관측 cond_id의 objective 목록도 계획과 정확히 일치해야 한다. 관측 noise seed는 fits의 optimizer seed에서 추론하지 않고 봉인 입력에서 가져와 Condition과 roster를 재구성한다. 재구성된 cond_id 집합이 실제 fits의 관측 집합과 같은지도 확인한다.

validator는 `_inputs/*_curves.parquet` 중 **전체 파일 SHA가 계획 inputs.curves_sha256와 같은 것**을 선택한다. 없으면 실패이고, 재구성 SHA·개수를 계획 roster와 대조하며 record의 roster SHA에도 연결한다. writer도 같은 재구성 함수를 사용하며 행과 입력이 어긋나면 candidate map/record 쓰기 전에 오류가 난다. production 호출은 실행이 읽은 스냅샷 df를 넘긴다.

따라서 한 objective의 noise만 바꾸거나 두 noise 실현을 교차시킨 뒤 fits 봉인을 다시 맞춰도 행↔봉인 입력 대조가 거부한다. 같은 개수의 다른 유효 roster SHA를 record에 쓰고 record digest를 맞춰도 재구성 SHA 대조가 거부한다. 이는 SHA 형식/자기일관성만 보는 검사와 다르다.

시험 소스에서 n1_01·02는 `출력봉인_재계산` 통과를 먼저 요구하고 새 roster 검사와 noise 이유를 확인한다. n1_03·04·05는 다른 roster·스냅샷 부재·writer 거부를 각각 검사한다. 이번 리뷰에서 이 시험을 실행한 것은 아니다.

§6-a의 봉인 입력 출처 선택과 §6-b의 정확 비교를 수용한다. 같은 고정 입력에서 옮긴 truth의 결속을 검사하는 자리이므로 수치 허용차를 새로 도입할 필요가 없다. fits에 없는 관측 seed를 직접 측정했다는 뜻은 아니다.

코드: [io.py 관측 재구성](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/ea2af59e68a85b561c3e185f66b815aec877ca57/degradation-degeneracy/src/io.py#L1573), [validator 소비](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/ea2af59e68a85b561c3e185f66b815aec877ca57/degradation-degeneracy/src/io.py#L1895), [writer](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/ea2af59e68a85b561c3e185f66b815aec877ca57/degradation-degeneracy/src/fitting.py#L1402).

## 3 G82 N2 bank 선언과 구현 결속 종결

**닫힘을 수용한다.** 지원 profile은 pcg64, v6.0, H(pair_group_id, bank_version), float64, little, unit_cube 하나로 고정됐고 별칭은 없다.

`check_bank_profile`이 계획 봉인, 실행 전 `_prepare_stage3`, validator `_stage3_rederive`에 연결된다. 설계와 envelope가 같은 미지원 선언을 해도 각각 지원 profile과 비교하므로 양쪽 문자열 일치만으로 통과하지 않는다. 기존 bank 생성/RNG·직렬화·ID 함수 본문은 이전 코드와 같다. 골든 수치를 이번에 다시 생성하지는 않았다.

§6-c의 넓은 선언 reader 유지도 수용한다. **문법상 읽을 수 있는 설계**와 **이번 실행 경로가 지원하는 설계**는 다른 조건이다. 설계 digest를 계산할 수 있다고 실행 가능한 것으로 표시하지 않는 한 reader까지 일괄 제한할 필요는 없다. 향후 다른 실행 진입점을 붙일 때에도 profile 검사를 우회하지 않아야 한다.

§6-d의 envelope 단계 거부를 수용한다. n2_03(a)의 dtype 반례는 envelope 봉인을 통과한 설계를 실제 시작 전 profile 검사에 도달시킨다. (b)의 stub은 PlannedLegV4 객체 생성만 우회하며 `_prepare_stage3`의 `check_planned_envelope`까지 우회하는 것은 아니다. (b) 하나로 뒤쪽 profile 분기 도달을 증명한다고 쓰지 않으면 된다. (a)와 해당 분기 변이가 이를 별도로 담당한다.

작은 문서 정정: 요청문에서 `check_design`이라 부른 선언 검사는 실제로 `pairing_design_sha256`→`_check_design_nested` 경로다. 다음 문서 갱신 때 이름만 맞추면 된다. 코드 수정·새 시험·추가 게이트의 조건이 아니다.

코드: [지원 profile](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/ea2af59e68a85b561c3e185f66b815aec877ca57/degradation-degeneracy/tools/design_wire.py#L560), [시작 전 검사](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/ea2af59e68a85b561c3e185f66b815aec877ca57/degradation-degeneracy/src/fitting.py#L1317), [검증 경로](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/ea2af59e68a85b561c3e185f66b815aec877ca57/degradation-degeneracy/src/io.py#L1660).

## 4 G82 N3 선언 세대 연결 종결

**닫힘을 수용한다.** v6 시작 경로는 계획 protocol_generation을 명시적으로 v6에 묶는다. validator의 `세대_연결`은 sig 6, 계획 v6, record v6, 행 전체의 record_generation 집합 {v6}를 각각 대조하며 열을 읽지 못하면 실패한다. 계획과 record가 함께 v5인 자기일관 자료도 통과하지 않는다. 기존 sig5의 v6 표식 충돌 검사와 legacy/prep reader는 유지됐다.

§6-e의 v4 envelope 세대 문법 유지도 수용한다. **envelope 형식 버전 v4와 실험 프로토콜 세대 v6는 같은 번호 체계가 아니다.** v4 계획이 문법상 v5를 표현할 수 있어도 v6 실행·validator가 거부하면 이번 닫힘 조건에 맞는다. 역사적 읽기를 좁히거나 과거 자료를 소급 변경할 필요가 없다.

RED→GREEN 시험 diff는 n3_02의 일반 protocol_generation 확인을 계획/record 두 이유 각각의 확인으로 강화한 것이다. 대조 하나를 지워도 다른 하나가 같은 검사명을 실패시키는 은폐를 막는 정정이며, 실패를 없애기 위한 assertion 완화가 아니다.

코드: [시작 전 세대 검사](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/ea2af59e68a85b561c3e185f66b815aec877ca57/degradation-degeneracy/src/fitting.py#L1300), [세대 연결](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/ea2af59e68a85b561c3e185f66b815aec877ca57/degradation-degeneracy/src/io.py#L1816).

## 5 영수증과 절차 기록

| 항목 | 수신 대조 결과 |
| --- | --- |
| 82차 2차 영수증의 history 보존 | 두 leg 모두 이전 수신 원본과 바이트 동일 |
| 새 validator digest | 7187bd31740514d4, 독립 코드 digest와 같음 |
| src_io_sha256 | e0577ad8af02b0b3, 실제 io.py 해시 앞 16자리와 같음 |
| 검사 수 | paired 35 / grid 34, 이전과 같음 |
| 안정된 core 부분 | producer 항목·validation 검사·bundle·outputs·restore 텍스트 동일 |
| 바뀐 부분 | core_sha256, validator_source_digest, src_io_sha256, stamp |
| 원장 | 두 leg의 receipt core SHA와 validator digest만 갱신, 새 영수증과 일치 |

새 paired core는 `1eb98e213edb9f8b8112adf595a72f9bc8f06e212656397848f43d9244b3e049`, grid core는 `ee7c405a1495eff06af6d6187b2e936d7ca345a3bf8833118e77e23aba6f14ea`다. 이번 대조는 텍스트/필드/바이트 수준이며 core canonicalizer 실행이나 payload 재복원·재채점을 한 것은 아니다.

paired stamp의 dirty=false, grid의 dirty=true를 그대로 유지한다. clean 커밋에서 순서대로 생성했다는 설명과 두 영수증 각각이 모두 clean이라는 주장은 다르다. 과거 두 leg의 sig5 검사 수가 그대로인 것은 새 검사가 sig6 경로에 추가됐기 때문이며, 두 영수증이 실물 v6 연구 leg의 완주 증거가 되는 것은 아니다.

§6-f의 첫 등록부 시험 3 failed 및 증인 공백 정정은 숨기지 않은 이력으로 수용한다. RED의 18 failed를 18개 독립 결함 재현으로 세지 않는다. 신고한 7개 무관 예외는 제외하고, 이미 다른 검사에 거부되던 사례와 새 검사 부재도 실제 위조 수용 반례와 구분한다. n1_01·02 등 정확한 봉인 상태의 위조와 해당 검사 이유를 핵심 근거로 삼는다.

AST로 19개 매개변수화 시험 node와 12개 변이/EXPECT를 확인했고 각 변이 preimage가 최종 대상에서 정확히 한 번 나타남을 문자열로 확인했다. 이는 변이를 실행해 12/12를 재현했다는 뜻이 아니다. 전체 회귀와 smoke의 작은 계산은 발신 수행 범위이며 새 연구 계산과 구분한다.

## 6 질문별 최종 답과 다음 경계

| 질문 | 답 |
| --- | --- |
| Q1 N1·N2·N3가 닫혔는가 | 세 건 모두 종결 수용 |
| Q2 라운드 1 종결인가 | 승인된 라운드 1 범위 종결. 단계 3 전체 완료는 아님 |
| Q3 봉인 입력 출처·넓은 선언 reader·v4 세대 문법 | 현재 분리 방식 수용. 위의 용어/검사 도달 설명만 정확히 유지 |
| Q4 새 세대 영수증 | 해당 validator 세대의 기록으로 수용. 같은 코드에서 추가 재생성 불필요 |

다음은 원장 §118에 수신 판정과 세 종결을 추가하고, **라운드 2의 고정 범위를 사용자에게 별도로 승인 요청하는 단계**다. 이번 리뷰는 원장 편집이나 구현을 직접 수행하지 않았다. 다음 범위안은 실물 v6 leg gate 연결, 계획/source/input/base-config/runtime 결속, 세대 등록, p_ini 지원/거부 정책, dead 정의 정리, 계약 정정, returned와 유한·수렴 결과의 구분을 서로 나눠 제시하면 된다. 정책 선택을 p_ini 구현 또는 연구 실행 승인으로 확대하지 않는다.

현재 코드에 새 결함이 없다는 범용 보증이 아니라, 82차가 정한 잔여와 이번 승인 범위의 종결 판정이다. 새 연구 leg·floor·pilot·provider 운영 canary·class 변경·투영 게시·라운드 2·실행 GO는 여전히 별도다. 76차 종결과 grid_fit_v5 진단 전용 상태를 다시 열지 않는다.
