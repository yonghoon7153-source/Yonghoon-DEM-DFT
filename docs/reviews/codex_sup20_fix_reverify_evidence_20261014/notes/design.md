# SUP20-02 · 입력 반입 독립 대조

검토 핀 a9422d2e772f28417a6e0a5167aaab8d987bf27a, 기준 b429c3c1df0956d2721861d89cc29a2d56f2b581. 원본 수정·시뮬레이션·배치 실행 없음.

## SUP20-02: 닫힘

- `scripts/lhs_design_dataset.py:2263–2265,2278–2281`의 네 정의가 실제 슬롯과 일치한다. `lhsx_design_adapter.py:73–86`은 bimodal에서만 `wP/(wP+wS)`를 쓰고 mono에서는 kind로 1/0과 AM 크기 칸을 배정한다. `lhss_design_adapter.py`는 이 함수를 재사용한다.
- 별도 CSV 파싱·계산: lhss 20행, lhsx 64행 전체에서 새 정의와 `ps_frac` 불일치 0. lhss mono_AM_S 001/002/003/020은 P=0.3/0.3/0.3/0.375, S=0, 옛 무조건 식=1, 실제 ps_frac=0. lhsx mono_AM_S 8행도 같은 구조. lhss 종류 수 14/2/4, lhsx 48/8/8 (bimodal/monoP/monoS).
- 수정 전후 AST에서 자체시험 함수와 네 사전 문자열만 제외하면 나머지가 완전히 동일하다. 따라서 이 패치는 계산·열 구성 변경이 아니라 설명 수정이라는 주장을 뒷받침한다.
- lhss 설계 CSV, 변환 CSV, 두 어댑터 모듈, 실행기 모두 기준 핀과 바이트 동일하다. 변환 CSV SHA-256 `df505b79a756ee3fe2759c740bfb43282dd69035c5a9fb9354a657300117dc0c`.
- 현재 스냅샷에 있는 v1.2 lhsx 인계 사전(`docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/lhsx_handover_v12_20261006_columns.tsv:28`)에는 일반 문구가 있고 해당 잘못된 비율 식은 없다. SELF-107의 이 한 사례는 지지한다. 역사 4개 전수를 이번 부분 스냅샷으로 확인했다고 말하지 않는다.
- 새 결함 없음. 이미 알려진 fixed loading 임의값 허용 등은 재개하지 않는다.

## 봉인·반입: 컨테이너 범위 대조 성립

후보 실행기의 CODE_FILES를 AST에서 추출해 파일별 SHA-256을 독립 계산했다. 32/32가 기준과 바이트 동일, 정렬 지도 SHA-256은 `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`이다. 수치 봉인 불변을 문서 선언만으로 수용하지 않았다.

원 tgz를 메모리에서 읽은 결과:

- r2 30항목 SHA `baa03b6b65d57b7850df151a011d8102b605fc15d81aa9f58969629ac9d00aff`.
- r3 29항목 SHA `e4aa0b9492a48368d47ad20555cd71114da53488badedbaea330835c467b9958`.
- 절대경로·상위 이동·링크 없음. r3 harvest_head 파일 `1e09f661d83edd674a1686b22552f609b61a34b6`.
- 20 descriptor 반입 바이트가 묶음과 동일. summary·cohort·union도 동일. `_design_family.csv`는 CRLF→LF 정규화 후 동일(등록한 예외).
- r2/r3 20개 모든 공통 키에서 다른 값은 `contact_area_check.producer_model.pin_file` 한 종류뿐(각 20행). r2 전용 잎 키는 mono 6행에서 각 28개, bimodal 14행에서 각 42개. 전체 키 종류 합집합 42개이며 모두 wall_near_tangent 진단. r3 전용 키 0. “42키”는 행마다 42라는 뜻으로 확대하면 안 된다.
- r2/r3 union은 셀뿐 아니라 바이트도 동일. cohort TSV도 두 묶음 및 반입본이 바이트 동일.

원본 descriptor에서 별도 정렬·직렬화하여 재계산한 입력 지문:

- 20 ID: `991cf1150b183f64bc69926a8b3e7c05453ec47e13b89ba3a6ad2fd2c981c694`
- raw SHA 표: `a7aaa3c8c7683f1835a096acb83ecdb055eaf5f129221f7067c5f34462807d0e`
- cohort TSV: `69d3f913072288b1d6b8ca8a14e43b0bc8f80e8836a8f79a9b26b2d8ed6dcaf7`
- 20×4 원자료 SHA 필드 결손 0. 모두 등록 문서 값과 일치.

중요한 한정: 이것은 커밋된 **수확 결과/입력 해시 표의 대조**다. WSL 원 atom/contact/mesh/deck 80파일의 실제 바이트를 다시 읽은 검증이 아니다. harvest_head 파일 역시 선언한 판을 확인한 것이지 원 런 실행을 독립 관측한 것은 아니다. r3 기록의 값을 다시 생성했다고도 말하지 않는다.

## Q3·남는 순서에 대한 의견

컨테이너 증거는 SUP20-02 수정 및 반입·등록의 바이트/정의 일치 확인에는 충분하다. 발사 핀의 실행 환경·원자료 실재와 값·import 관측·깨끗한 트리·새 ROOT·fast16+real4를 증명하지 못한다. 따라서 “구현 수정 닫힘 / WSL 사전 점검 진입 허용”과 “발사 GO”를 분리해야 한다. 기존 판정문의 §4 최소 순서대로 사전 점검과 dry-run 영수증을 **실제 발사 허용 전에** 완료해야 한다. 승인 뒤에 사전 점검을 한다는 문구를 남긴다면 그 승인은 명시적인 조건부 승인일 뿐, 실행 관문을 면제하는 승인이 아니다.

독립 재현: `python -X utf8 -B probes/design_extra.py` (리뷰 폴더에서). 수집 증거 `evidence/design_extra.json`. 이 탐침은 대상 영수증/실행기를 import하거나 판정을 호출하지 않고 AST·바이트·CSV·tgz만 읽는다. 부모 에이전트가 별도로 돌리는 기존 design_probe의 실제 어댑터 재생성/800셀 대조와 상보적이다.
