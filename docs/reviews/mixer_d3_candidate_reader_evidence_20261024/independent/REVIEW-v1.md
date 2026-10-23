# D3 candidate reader independent review — v1 snapshot

판정: **P3 두 건 보완 필요**. 검토한 수치·집합·불완전 상태 경로에서는 새 P1/P2 오판 반례를 찾지 못했다. 이 결론은 입력 조건부 계산기 범위이며 실물 관측·통계 추정·원자료 추출·사전등록·맹검·실행 GO를 인증하지 않는다.

검토자는 이 구현의 작성자가 아니다. 설계 정본 `d5ab56ba9a9416e5cae2becf3c85b7c54d30d1d2`의 `mixer_d3_se_flowability_anchor_design_v2_20261023.md`와 보존한 코드/시험을 먼저 읽었다. 독립 probe는 작성자 fixture를 import하지 않고 세 점을 별도로 구성했다. 이후 공개될 구현 계약 문서의 범위도 대조했다. 원문 문헌·실험 원자료는 새로 검증하지 않았다.

검토 입력: `reviewed-v1/mixer_d3_candidates.py` SHA256 **3160506f199983e2ff2bcc00ab8aaa461c0cb6dea82adecd163f7cdd86b1c5ad**; 시험 SHA256 **489e51c9f2f00635c45db53422a3f0e1dd1a6f2f9fea99b7a25a8b335f387fb3**. 정확한 정본 hash는 `reviewed-v1-sha256.json`이다. 작성자가 이후 고친 파일을 이 판의 결과로 세지 않는다.

| ID | 위치와 재현 | 판정·수정 방향 |
|---|---|---|
| D3IR-01 · P3 | `loads_strict`의 `parse_float=Decimal`. CLI 계약의 Bo를 `1e9999999999999999999999` 또는 `1e-9999999999999999999999`로 바꾸면 `decimal.InvalidOperation`이 처리되지 않아 traceback·rc1이다. 결과 파일은 생성되지 않았다. | 입력 거부 자체는 유지되므로 잘못된 과학 판정은 아니다. 계약 오류 rc2/원인 메시지 계약을 깨는 오류 처리 누락이다. Decimal 변환 예외를 ContractError로 정규화하고 실제 CLI에서 rc2·traceback 없음·출력 없음 시험을 먼저 추가한다. |
| D3IR-02 · P3 | 설계 §1은 Bo_po=Bo_code/6.75 병기를 요구한다. v1 결과 `grid`는 `id,bo_code`만 낸다. | 보고 계약 누락. 정확한 정의와 표시 정밀도를 명시한 Bo_po 산술을 병기하고 큰/작은 값·유한성·단위/범위 한정을 확인한다. 실입자 Bo의 측정으로 쓰지 않는다. |

검사 결과:

- 작성자 시험을 보존 사본에서 실행: **24 unittest, rc0**. 이는 독립 작성 시험 수가 아니다.
- `probe_independent.py`: **15개 명명 검사, 15 PASS**, 그중 교집합은 세 점×두 시험의 C/I/U **729조합**을 독립 열거했다. 평탄 `INSENSITIVE`도 관측/폭이 유효하면 S에 남고 식별성 주장을 하지 않는다. 불확도 누락은 UNASSESSED이며 이웃 후보를 연결하지 않는다.
- 검증 미평가 우선·이미 알려진 불일치 칸 보존·S 불변, 정확한 0.4−0.3=0.1 경계, 64자리 경계 밖, ±1e300·1e−300 차이, malformed 숫자, 예약 세 시드×세 역할 및 명시/미명시 중복을 공격했다.
- **7개 guard 변이, 7개가 지정된 AssertionError로 검출**: 경계 `<`, 교집합→합집합, 미평가 틈 연결, 불확도 요구 제거, 예약 시드 검사 제거, raw hash 검사 제거, incompatible가 incomplete를 덮는 변경. 예외 발생만으로 검출 성공이라 세지 않았다. 첫 변이 준비 스크립트는 보존 코드의 `accepted_sets` 이름을 옛 `accepted`로 지정해 설정 단계에서 중단됐으며, `mutations-v1/`은 그 중간 산출물이다. 완료 7개는 `mutations-v1-complete/summary.json`이다.
- 실제 CLI control rc0·결과 생성; 중복 JSON key rc2·결과 없음; 위 두 거대 지수는 rc1·결과 없음. 원 stderr는 `v1-results/cli-probes.json`이다.

출처 범위의 작은 반례도 남겼다. 같은 raw bytes와 hash를 두고 공급 관측 숫자만 바꾸면 S가 `[a,b,c]`에서 빈 집합으로 바뀐다. 이는 **현재 파일 무결성/입력 결합이 원자료에서 관측 수치를 재추출하는 검증은 아니라는 것**이다. 구현 계약 §3은 출처를 불투명 bytes로 읽고 eligible을 공급자 선언으로 취급한다고 명시한다. 그 한정 아래 새 오판 finding으로 세지 않는다. 실제 영수증/원자료/수치/물리 자격 결합은 미래 생산자·관측 판독기 단계에서 여전히 필요하다.

API digest는 호출자 공급값, CLI digest만 실제 입력 바이트 계산이라는 표시가 구현돼 있다. 시드 manifest 검사는 입력된 역할 집합의 겹침/예약 ID 검사이며 역사적 미사용·독립 표본의 증명이 아니다. 빈 역할 배열·누락 manifest가 실행 준비로 승격되지 않는다. 전체 repository gate, 실제 DEM/실험, 물리 적격성이나 통계 방법의 정당성은 이번 검토에서 실행하지 않았다.
