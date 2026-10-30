# 믹서 D3 유한 후보 판독기 독립 재검토 — 2026-10-27

**판정: 입력 조건부 유한 후보 판독기 범위 GO. 이번 검토에서 새 P1/P2/P3 반례를 찾지 못했다.**

이 GO는 제공된 계약·관측·출처 파일로 유한 후보 집합과 검증 상태를 계산하는 구현에 한정한다. 원자료에서 관측값을 추출하는 정확성, 통계 폭의 정당성, 사전등록·맹검·역사적 seed 미사용, 장비·DEM 실행 자격을 승인하지 않는다. 모든 독립 출력에서 `execution_ready=false`가 유지됐다.

## 1. 고정 신원

- 핀: `e0daf7b234bcc7935259d786e270268372abe2a2`, `codex/mixer-d3-design`.
- 요청서: `docs/reviews/codex_mixer_d3_candidate_reader_request_20261024.md`.
- 대상: `scripts/mixer_d3_candidates.py` 및 계약·시험·증거.
- 받은 ZIP: `codex-mixer-d3-e0daf7b234bc-rebuilt-20261027.zip`.
- ZIP SHA-256: `6cf74df007ea9784b5d3cf256ddd92e9434d596dacba5ef70da11206c91a19ff`.
- 리포 파일 **327/327**을 원격 pin Git blob과 대조: 불일치0. PIN 파일은 이 수에서 제외.
- 주 증거 manifest **257항목**의 실제 SHA-256 대조: 불일치0.
- 소비자 소스 SHA-256: `ea4528156e8eb9762999fef0643985bebf0b0735691202fddb4a2c17814ee7f8`.
- 제출된 canonical gate155/0,rc0의 후보 `9c2f7b47fd4559ee4c08f23e667cdae92badbb04`와 이 pin 사이에 `scripts/`, `webapp/`, `dem_scripts/`, `.github/` 차이0. 전체54파일 변경은 문서·증거다. 이것은 과거 gate와 현재 소스의 연결 확인이며 **새 전체 gate 실행이 아니다**.
- 앞선 병렬 gate154/1의300초 시간 초과와 뒤 순차155/0 기록을 구분했다. 실패 기록을 지웠다는 증거도, 시간 제한을 완화해 통과시켰다는 근거도 이번 자료에서 발견하지 않았다.

## 2. 질문별 판정

| 질문 | 판정 | 코드·독립 관찰 | 남는 경계 |
|---|---|---|---|
| Q1 T1/T2 유한 교집합·순서·빈 집합·이웃 묶음 | 수용 | `:349`–382. 독립 보정4,096조합. 원래 후보 ID 순서, T1/T2 각각의 집합, 교집합, 빈 원인의 구분이 독립 기준과 일치 | 이웃 묶음은 등록 grid의 연속 index 묶음. 연속 Bo 구간·참값 coverage의 증거 아님 |
| Q2 모든 후보×항목, 미평가 우선, 알려진 불일치 보존 | 수용 | `:383`–402. 독립 검증4,096조합. 미평가가 후보 판정에서 우선하지만 원 항목의 incompatible은 보존. S 불변 | `all-compatible`은 입력된 폭 안의 전 칸 양립을 뜻하며 물리 검증 통과와 같지 않음 |
| Q3 누락과 잘못된 공급값 구분 | 수용 | `:202`–269. 실험누락·보정제외 후보 뒤에 숨긴 잘못된 수치/단위/source/불확도/키5종 모두 거부 | 관측 적격 여부를 생산자 대신 판단하거나 수치 재추출하지 않음 |
| Q4 실제 bytes 출처 결합·API 경계 | 수용 | CLI`:453`–462 실제 계약/관측/출처 bytes 검증. 잘못된 source byte와 digest 실제CLI거부 | API digest는 호출자가 준 값. source_ids는 파일 신원 결합이지 그 파일에서 value를 읽었다는 증명 아님 |
| Q5 임의 숫자·seed 선택 금지 | 수용 | `:116`–163,`:296`–335. 명시 폭·규칙 요구. 예약seed3종 거부, manifest 없으면 NOT_PROVIDED 유지 | 과거 사용 기록·독립 표본 여부·미등록 설계 선택을 인증하지 않음 |
| Q6 크기·숫자·파일 오류·덮어쓰기 | **수용, 플랫폼 확인 한정** | 수치 범위·엄격JSON·경로탈출·해시불일치·덮어쓰기 시험과 실제CLI일치. 파일 크기 제한은 읽기 전후검사 | Windows에서 symlink 생성 권한이 없어 symlink 자기시험1개는 직접 재현하지 못함. 아래§5 참조 |

[고정 소비자 소스](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/e0daf7b234bcc7935259d786e270268372abe2a2/scripts/mixer_d3_candidates.py)

## 3. 저자 고정물과 다른 독립 판정 기준

`d3/evidence/independent_probe.py`는 grid ID=`low,middle,high`, Bo=`0.4,2.75,18`인 별도 계약을 구성했다. 실물 측정·등록 수치가 아닌 합성 시험 값이다.

각 후보×항목에 다음4상태를 배치했다.

1. 적격·양립.
2. 적격·불일치.
3. 관측누락.
4. 기술실패.

보정 T1/T2의6칸에서 **4⁶=4,096조합**, 검증의 scalar/categorical6칸에서도 **4⁶=4,096조합**을 전수 계산했다. 구현의 집계 함수를 기대값 생성에 재사용하지 않았다. 독립 기준은 “두 보정 칸이 모두 양립인 ID만 S”, “검증 칸에 누락/기술실패가 하나라도 있으면 unassessed, 그렇지 않으면 알려진 불일치 우선”이다.

전 조합에서 다음을 함께 대조했다.

- `S_T1`, `S_T2`, `S`와 원래 grid순서.
- 완전 보정 여부와 `not-empty / both-tests-empty / T1-empty / T2-empty / disjoint` 구분.
- 빈 S의 `validation.aggregate=not-applicable`.
- 후보별 상태와 각 항목의 원 상태 보존.
- 검증 집계의 `incomplete / all-compatible / none-compatible / mixed`.
- 검증 뒤 S가 줄어들지 않음.
- `execution_ready=false`.

추가로 중간 후보만 제외한 비연속 이웃 묶음, 입력 객체 불변, seed manifest 부재, 예약seed3종, 숨은 malformed값5종을 대조했다. Decimal 검사는 `0.4−0.3` 경계와 **10³⁰⁰ 및 ±10⁻³⁰⁰**를 같이 사용했다. 폭10³⁰⁰에서 `10³⁰⁰−10⁻³⁰⁰`는 양립, `10³⁰⁰−(−10⁻³⁰⁰)`는 불일치로 구분됐다. float 반올림으로 둘을 동일시하는 반례가 재발하지 않았다.

이 모든 것을 포함한 독립 스크립트의 **명명 검사27개가 통과**했다. 8,192조합은 그 안의 두 전수 반복이며27과 독립 시험 수처럼 합산하지 않는다. 저자 시험·기존 내부 독립 시험 수와도 합산하지 않는다.

## 4. 실제 CLI 경계

독립 CLI 입력7종을 별도 파일로 만들었다.

| 입력 | 반환 코드 | 파일·출력 의미 |
|---|---:|---|
| 전 후보 양립 정상 | 0 | 결과 생성, 실제 input bytes SHA 일치, execution_ready=false |
| 보정 S가 빈 집합 | 0 | 결과 생성. 과학적 성공으로 승격하지 않음 |
| 검증 항목누락 | 0 | incomplete와 execution_ready=false 보존 |
| 출처 파일 바이트 변조 | 2 | 결과 미생성 |
| 계약 digest 불일치 | 2 | 결과 미생성 |
| 중복 JSON key | 2 | 결과 미생성 |
| 출처 경로 `../...` 탈출 | 2 | 결과 미생성 |

앞의 정상 의미3종은 같은 출력 경로로 재호출하면 모두rc2이고 기존 결과 bytes가 그대로였다. 따라서 **rc0의 의미는 판독·기록의 정상 종료**이며, 입력의 과학적 수용이나 물리 실행 승인을 뜻하지 않는다. 이 차이는 출력 상태에 드러나므로, 호출하는 다음 계층도 rc0만 보고 실행을 풀어서는 안 된다.

D2에서 찾은 newline 결합 반례를 D3에도 일반화하지 않았다. D3는 `read_bytes`에 해당하는 `_read_regular` 반환 바이트 자체를 해시한 뒤 JSON으로 디코딩한다(`:453`–461). 두 구현은 실제로 다르다.

## 5. 직접 검증의 한계

1. 저자의28 unittest를 그대로 실행했을 때 **27개 통과,1개 환경오류**였다. `test_artifact_path_escape_and_symlink_refused`에서 Windows가 symlink 생성을 권한오류1314로 막았다. 소비자가 잘못 수용한 실패가 아니라 시험 파일 자체를 만들지 못한 경우다. 이를28/28로 보고하지 않는다.
2. 정적 코드상 `_artifact_loader`는 구성 경로의 symlink를 거부하고, 최종 파일은 `O_NOFOLLOW`가 지원되는 환경에서 이를 사용한다(`:418`–442). 이번 환경은 해당 플래그를 제공하지 않는다. 계약/관측 입력 경로를 포함한 symlink 동작을 **모든 OS에서 인증한 것은 아니다**. Linux 대상의 제출된 symlink 시험 증거는 보존되지만, 이번 Windows 재실행의 대체 실적으로 합산하지 않는다.
3. 임의 동시 파일 변경·파일시스템 공격에 대한 보안 인증은 수행하지 않았다. 요청서도 접근통제를 소비자 범위에서 제외한다.
4. 관측의 uncertainty 객체 구조와 명시 폭은 검증하지만, 그 폭이 실험 반복에서 타당하게 추정됐는지는 이 코드가 확인하지 않는다. source artifact는 해시가 일치하는 파일이며 수치 파서가 아니다.
5. 새 판독기 시험은 아직 공유 전체 gate에 직접 배선되지 않았다. 제출된155 PASS를 이 새 시험의 실행으로 오독하지 않는다. 통합 시 별도 직접 시험 또는 명시 CI 연결이 필요하다. 이 요청서가 이미 공개한 경계이므로 새 finding으로 중복 등재하지 않는다.
6. 후보·시드 정책은 이미 비준된 것을 재선택하지 않았다. 실제 등록값·실물조건·원자료·물리 자격은 미수령/미실행 상태 그대로다.

## 6. 재현과 결과 보존

증거 ZIP을 새 폴더에 풀고, Python3.11이상에서:

```bash
python3 -I -X utf8 -B d3/evidence/independent_probe.py
python3 -I -X utf8 -B d3/snapshot/scripts/test_mixer_d3_candidates.py
```

첫 명령은 새 `cli-replay-*` 폴더에서 생성·거부·덮어쓰기 시험을 수행하고 `independent_results.json`에 독립 기준 대조 결과를 기록한다. 기존 CLI 결과를 덮어써서 통과시키지 않는다. 두 번째는 저자 원본 시험이며 Windows symlink 권한 제한은 위와 같다. 기존 전체 gate를 이 명령으로 대체하지 않는다.

주요 증거:

- `d3/evidence/independent_probe.py`, `independent_results.json`.
- `d3/evidence/cli/` 및 최신 `cli-replay-*`: 실제 입력·결과·프로세스 로그.
- `d3/evidence/selftest-workspace-temp.log`: 원본28시험의27통과/1환경오류.
- `d3/blob_verification.json`, `evidence_manifest_verification.json`, `gate_pin_comparison.json`.

**GO — 고정 계약에 조건부인 유한 후보 판독기 구현에 한정. 실제 실행·S1/S3 등록·통계적 또는 물리적 타당성 GO는 아니다.**
