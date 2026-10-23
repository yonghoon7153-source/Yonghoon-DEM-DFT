# [믹서 D3] 유한 후보 판독기 계약 — 2026-10-24 KST

**1저자 비준:** 이 작업의 대화에서 1저자가 “계속 진행”, 이어 “다 비준이야”라고 지시했다. 10-23 설계 v2의 V2-Q1–Q4에 제시된 정책 선택은 사용자 비준으로 진행한다. 이전 날짜의 미비준 보고서는 당시 이력으로 그대로 보존한다. 이 비준은 아직 정하지 않은 장비·실물 기하·Bo 격자·통계 폭·반복·G·시드 값을 채운 기록이 아니다.

이번 구현은 `scripts/mixer_d3_candidates.py`와 `scripts/test_mixer_d3_candidates.py`이다. 명시된 유한 격자와 판정 폭, 출처 파일에 결합한 관측을 읽어 보정 후보 집합 및 후보별 검증 결과를 계산한다. 실제 DEM·실험·기하 판독·S1/S3 등록·C0 실행은 수행하지 않았다. 기존 정책/코호트·공유 검사기·봉인 파일도 바꾸지 않는다.

정본: `docs/reviews/mixer_d3_se_flowability_anchor_design_v2_20261023.md` §2–6. 이번 코드는 등록된 통계 방법을 추정하거나 미지원 기하를 적격으로 만드는 도구가 아니다. 아래 형식은 판독기 입력 계약이며, 그 파일을 만드는 것만으로 사전등록이 성립하지 않는다.

## 1. 실행과 결과 범위

```bash
python3 -I scripts/mixer_d3_candidates.py \
  --contract /absolute/path/contract.json \
  --observations /absolute/path/observations.json \
  --out /absolute/path/new-result.json
python3 -I scripts/test_mixer_d3_candidates.py
```

CLI는 입력 두 파일을 실제 읽은 바이트의 SHA-256으로 기록한다. 관측 파일의 `contract_sha256`은 읽은 계약 파일의 해시와 같아야 한다. 출처 manifest에 적은 모든 파일도 실제 바이트를 읽어 해시를 대조한다. 조건 파일의 해시는 계약의 `condition_sha256`과 같아야 한다. 계약·관측 파일의 종단 symlink, 출처 경로의 symlink·절대경로·`..`를 거부한다. 출처 파일은 관측 JSON의 폴더 아래에 있어야 한다. 출력은 새 파일만 허용하고 기존 파일·symlink·입력을 덮어쓰지 않는다.

종료 코드 0은 입력 계약을 읽고 결과 파일을 작성했다는 뜻이다. `incomplete`·`none-compatible`·빈 S도 정상적인 계산 결과이므로 종료 코드만으로 과학적 통과를 해석하지 않는다. 계약 오류·읽기/쓰기 실패는 2이며 표준 오류에 원인을 낸다. 출력의 `execution_ready`는 항상 false다. 현재 외부 검토·실물 입력·단계별 등록/기계 실행 상태를 이 계산기가 승인하지 않는다.

API `evaluate(..., contract_sha256=..., artifact_loader=...)`는 호출자가 준 digest를 비교한다. 그 결과의 `contract_binding`은 `caller-supplied-digest-compared`다. 파일을 직접 읽고 계산한 CLI 결과만 `actual-input-bytes-verified`와 두 입력의 해시를 추가한다. Python API 호출자가 준 digest를 실제 파일 검증으로 승격하지 않는다.

## 2. 계약 JSON

최상위 필수 키는 다음과 같다. 알 수 없는 키는 거부한다. 전체 합성 예제는 `docs/reviews/mixer_d3_candidate_reader_evidence_20261024/author/synthetic_example/`에 있다. 그 숫자는 소프트웨어 시험용이며 새 과학 격자·시드·반복 설계가 아니다.

| 필드 | 계약 |
|---|---|
| `schema` | `mixer_d3_decision_contract/1` |
| `analysis_id` | ASCII 식별자 |
| `condition_sha256` | 조건 파일의 실제 SHA-256. 조건 내용의 물리적 타당성을 해시만으로 판단하지 않는다. |
| `grid` | `{id, bo}`의 비어 있지 않은 배열. ID는 고유, Bo는 양의 유한 JSON 숫자, 배열 순서는 Bo가 엄격히 증가해야 한다. 입력을 자동 정렬하지 않는다. |
| `calibration` | 정확히 T1·T2. 각각 `unit`, `boundary: "inclusive"`, 모든 grid ID에 대한 `widths`를 명시한다. 폭은 0 이상인 유한 숫자다. |
| `validation` | 하나 이상의 필수 검증항목. 각 항목의 ID와 아래 비교 종류를 명시한다. 목록이 비면 전부 통과하는 경로를 허용하지 않는다. |
| `seed_policy` | 선택. `allowed_role_overlap`에 C0/C1/C2의 허용 짝을 직접 적는다. 빈 배열은 모든 역할 사이 중복을 금한다. 실제 seed manifest를 넣으려면 이 필드는 필수다. |

검증 비교의 `kind: "scalar"`는 보정과 같이 `unit`, `boundary: "inclusive"`, 모든 grid ID의 `widths`를 요구한다. `kind: "categorical"`는 `unit`, `rule: "exact-match"`, 고유한 `labels` 목록을 요구한다. 범주형은 사전에 정의한 상태 라벨끼리의 같은/다름만 계산한다. 정지·중도절단을 임의 긴 시간으로 바꾸지 않으며, 복합 중도절단 통계는 현재 지원하지 않는다. 이 비교 종류가 실물 T3의 필요한 판정표를 충족하는지는 별도 검토해야 한다.

폭 A의 통계적 의미·단위·상관 처리·다중 후보 처리·독립 표본 수·자유도·유효 관측 범위는 S3 입력이다. 이 구현은 A를 추정하거나 2u를 신뢰구간으로 부르지 않는다. 경계 동률은 명시적으로 `|prediction−experiment| ≤ width`를 사용한다. 다른 동률 규칙은 현재 버전이 거부한다.

## 3. 관측과 출처

관측 JSON은 `schema: "mixer_d3_observations/1"`, `contract_sha256`, `condition_artifact`, `artifacts`를 필수로 가진다. `artifacts`는 고유 `{id, path, sha256}` 배열이다. `condition_artifact`는 그중 조건 파일 ID다. 같은 path의 중복 별칭도 거부한다. 해시는 반드시 소문자 전체 SHA-256이다.

`calibration`과 `validation`은 계약의 항목 ID를 키로 하고, 각 항목은 `experiment`와 grid ID별 `predictions`를 가진다. 항목·관측·예측이 없으면 미평가로 남는다. 계약에 없는 항목·후보 ID는 거부한다. 보정에서 나중에 탈락할 후보의 검증 관측까지 입력 전부를 검증하므로 그 안의 잘못된 단위나 숫자를 숨길 수 없다.

적격 관측의 필드는 다음과 같다.

```json
{
  "state": "eligible",
  "value": 10,
  "unit": "synthetic-unit",
  "source_ids": ["raw"],
  "uncertainty": {
    "value": 0.1,
    "unit": "synthetic-unit",
    "n": 2,
    "df": 1,
    "method": "synthetic supplied uncertainty"
  },
  "flags": ["INSENSITIVE"]
}
```

위 값도 합성 입력 예시다. scalar는 명시된 불확도 값·단위·n·자유도·방법이 필요하다. n은 양의 정수, df는 양의 유한수다. **이 구조 검사만으로 표본 설계와 불확도 추정의 정당성을 인증하지 않는다.** n=1의 표본 SD를 계산하거나 0으로 대입하지 않는다. 공급된 방법/수치가 정당한지는 원자료·S3·별도 통계 검사에서 확인해야 한다. categorical은 등록된 라벨 문자열을 쓰고 scalar 불확도 필드를 허용하지 않는다.

실제 파일 해시는 관측에 적은 값과 원자료 내용이 과학적으로 일치한다는 증명이 아니다. 이 판독기는 출처 파일을 불투명한 바이트로 대조하며 원 덤프·장비 자료·성공 영수증을 다시 파싱하지 않는다. `eligible`은 공급자의 선언이다. 이 제한을 결과 JSON의 `limitations`에도 남긴다. 성공 영수증과 실제 덱/출력의 일치는 기하/관측 판독기 검토에서 별도로 확보해야 한다.

관측 value·unit·source_ids 또는 scalar 불확도가 빠지거나 null이면 `UNASSESSED`다. 반면 **제공된 잘못된** 숫자/단위/출처 ID/필드/불확도 구조는 다른 필드가 누락되어 있어도 전체 입력 오류다. bool·문자열 수·유니코드 수 문자열·NaN/Infinity·중복 JSON key를 허용하지 않는다.

비적격 상태는 `technical-failure`, `observable-undefined`, `unsupported-contract`, `missing`과 이유다. 각각의 원인이 결과에 보존되며 수치나 불확도를 함께 실어 비교하지 않는다. 유효한 평탄 응답은 `eligible`과 `flags: ["INSENSITIVE"]`로 기록할 수 있다. 이는 후보 양립 계산에서 자동 제외하지 않으며 식별성 검증을 주장하지 않는다. 별도 민감도 자격 기준을 새로 구현한 것은 아니다.

## 4. 결과 의미

- `S_T1`, `S_T2`, `S`는 원래 grid ID 순서를 보존한다. S는 두 보정 집합의 교집합이다. `empty_case`는 두 시험 모두 빈 경우, 한 시험만 빈 경우, 각각 비어 있지 않지만 교집합이 빈 경우를 구분한다. 미평가 존재는 `calibration_complete`로 별도 표시한다.
- `neighbor_groups`는 등록한 grid **인덱스**의 이웃 묶음이다. 탈락·미평가 점을 가로질러 연결하지 않는다. min/max 연속 구간·기하 중심·단일 앵커를 만들지 않는다. 빈 S는 해당 유한 grid에서 후보를 찾지 못한 결과이며 연속 모델 전체의 기각이 아니다.
- grid 각 점의 `bo_code`와 `bo_po_approx`를 보고한다. 후자는 설계 정의 Bo_code/6.75를 50자리 십진 연산으로 표시한 산술이며 실입자 Bo의 측정이 아니다.
- 양 끝 후보 또는 양 끝 미평가가 남으면 `range_limited`다. 격자 확장·새 Bo를 자동으로 만들지 않는다.
- 검증은 S의 모든 후보×모든 필수 항목의 표를 남긴다. 후보의 필수항목 하나라도 미평가면 요약은 `unassessed`, 모두 평가했고 모두 양립하면 `compatible`, 모두 평가했고 하나라도 불일치면 `incompatible`다. 미평가 요약 아래에서도 이미 확인된 불일치 칸과 이유는 보존된다.
- S가 비면 검증 집계는 `not-applicable`이다. S가 있으면 `incomplete`가 우선이며, 전부 평가했을 때만 `all-compatible / mixed / none-compatible`를 구분한다. 검증 결과로 S를 다시 줄이지 않는다. `all-compatible`도 입력된 검증 조건의 양립이며 응용 타당성이나 실행 GO가 아니다.

출력의 측정 관련 십진 값은 `numeric_encoding: "decimal-text"` 문자열이다. JSON 입력의 십진 토큰을 Decimal로 읽고 차이를 충분한 정밀도로 계산하여 0.4−0.3=0.1 같은 경계에서 이진 부동소수점 오차로 판정이 달라지지 않도록 한다. 해당 입력 범위는 숫자당 유효숫자 64자리, 비영값의 10진 자릿수 지수 −300…300이다. 입력은 JSON당 16 MiB, 출처 단일 64 MiB/합계 256 MiB, grid 10,000점, 필수 검증 64항목, grid×전체 시험 20,000칸, 출력 64 MiB로 제한한다. 이들은 지원 크기 한도이며 과학적 합격선이 아니다.

## 5. 실제 seed manifest를 넣었을 때의 검사

관측의 선택 `seed_manifest`는 정확히 C0·C1·C2 키와 각 정수 배열이다. 역할 안 중복, 예약 확인 시드 **15485863·86028121·104395301**, 미선언 역할 간 중복을 거부한다. 허용한 역할 짝의 중복은 ID와 함께 결과에 남기며 독립 표본이라고 인증하지 않는다. 이 세 예약 ID의 출처는 v2 §6 및 보존한 10-23 독립 seed-confirmation 부록이다.

manifest가 없으면 `NOT_PROVIDED`, 있으면 그 입력 내용을 대조한 `CHECKED_SUPPLIED_MANIFEST`다. 과거 실행에서 시드를 사용하지 않았다는 역사적 사실을 검사한 것은 아니며 `historical_nonuse_verified: false`를 유지한다. 빈 역할 배열은 그 역할이 이번 manifest에서 비어 있음을 나타낼 뿐 역할 실행 준비를 인증하지 않는다. seed를 새로 뽑지 않는다.

## 6. 현재 검증·후속

신규 구현 전 시험 파일은 존재하지 않는 reader를 로드하지 못해 실패했다. 이는 기존 구현 결함의 재현이 아닌 새 기능 부재의 red다. 작성 중 SyntaxError 로그도 별도로 보존했다. 작성자 초기 회귀는 24 unittest이며 그 안에 보정 상태 81조합과 검증 상태 81조합의 별도 전수 열거가 있다. 독립 검토·후속 수정 뒤 최종 수와 소스 신원은 증거 README를 따른다.

새 시험은 공유 `scripts/check_all.sh`에 아직 연결하지 않았다. 전체 gate의 기존 시험과 이 reader의 직접 시험은 따로 실행·기록한다. 받아 가는 쪽에 공유 gate 추가 명령을 쪽지로 제안한다. 이 패키지의 코드·숫자·경계 동작에 대한 독립 공격 검토, root 반입 후 전체 gate, 외부 검토와 실제 입력/등록은 각각 분리한다.
