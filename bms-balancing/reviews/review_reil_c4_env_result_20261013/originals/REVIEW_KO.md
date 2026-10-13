# REIL C4-ENV 결과 검토 회신

2026-10-13 · 정적·기록 검토. 실행 환경을 새로 만들거나 공급 코드를 실행하지 않았다.

## 1. 판정

**이번 고정 제출의 새 봉인을 C4 환경으로 한정 수용한다. 현재 봉인 채택을 막는 P1은 발견하지 못했다.** 이는 모든 설치 파일의 과거 바이트 재현, 모든 절차의 완전 준수, 현재 원격 환경의 실시간 관측을 인증하는 판정은 아니다. 아래 P2와 관측 한계를 함께 보존한다.

- 검토 고정 HEAD: `c2ab1e0cbdc8fc2da2321bd18a064381c6513919`.
- 실행 증거 커밋: `1135624c435b161f0928c2663f77700392606d85`.
- 채택 폴더: `bms-balancing/reil_c6_rebuild_20261013/`.
- MANIFEST SHA256: `4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc`.
- lock SHA256: `ea91156cac99fac17830818f17fd4a260a93722269f720171e0ab9b2a75c1faa`.
- PROFILE SHA256: `50f2c7fb176910da2df252cfd7f17a8f05a56b8696e1be3040d6ff5cf034a641`.

이번 `check` 1회는 C4 v2 §4-6의 전체 C6 자기점검 1회로 인정한다. 같은 코드·환경·봉인 식별이 유지되어야 하며 C4-0에서 전체 check를 다시 실행하지 않는다. emit 1 + check 1에 포함된 합성 COBYQA 2회·Sobol 생성 경로 2벌을 1회로 축소해 기록하지 않는다.

상태 문서 §36에 기록된 기존 사용자 승인에 따라 **C4-0의 환경 수용 선행 조건은 해소된다.** 다음은 승인된 C4-0 구현·합성 RED/GREEN·고정 배열 봉인·무자료 건조 범위다. 이 검토가 새 설치·복원, C4-E/A/B, REIL 자료 개봉·맞춤, COMSOL을 승인하지 않는다. 환경이 없어지거나 식별이 달라지면 그 자리에 멈춘다. 복원을 자동 실행하지 않는다.

근거: [승인 기록 §36](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c2ab1e0cbdc8fc2da2321bd18a064381c6513919/bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md#L592), [C4 v2의 범위·환경 결속](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c2ab1e0cbdc8fc2da2321bd18a064381c6513919/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_v2_20261013.md).

## 2. 원문 대조 결과

| 대상 | 이번 검토의 확인 | 범위 |
|---|---|---|
| 옵션·배열 | COBYQA_OPTIONS, SOBOL_PHASE_A, npy 6개의 old/new Git blob·크기 동일 | 배열 생성·로딩·재계산 없음 |
| lock | 4·16·22·27·32행만 변경: Python 판 및 cffi/fonttools/numpy/pip RECORD SHA | 양쪽 LF·마지막 LF도 일치; 나머지 바이트 차이 없음 |
| PROFILE | python.version, python.build만 변경 | Python 패치 판이 같은 환경이라는 뜻은 아님 |
| MANIFEST | lock·PROFILE 두 항목만 변경; 구성원 집합 유지 | 새 세대의 봉인으로 채택 |
| 과학 RECORD 30개 | 보존 원문의 raw SHA·정규화 SHA 재계산, 보고서 및 새 lock과 30/30 일치 | wheel→설치 대조 자체는 제출된 실행 기록을 소비 |
| 시험 도구 RECORD 4개 | 보존 원문의 raw/정규화 SHA가 종료 기록과 4/4 일치 | pytest 실행 성공이나 설치 파일 전체 재해시를 뜻하지 않음 |
| 실행 명령 | S1–S9의 10개 자식 호출(S4 a/b), argv·cwd 일치·rc0·timeout 없음 | S10 및 바깥 runner 반환은 아래 구분 |
| 보호 범위 | 보호 tree 7개는 시작·실행 증거·검토 HEAD에서 동일; 기록된 파일 SHA 5개 동일 | 전체 PC·모든 작업 파일 보존 인증 아님 |

과학 wheel 28개는 과거 로그와 이름이 같고, 시험 wheel 4개는 이름·판이 같다. 현재 wheel SHA는 기록돼 있다. 그러나 옛 wheel SHA·옛 RECORD 원문, 현재 wheel 원바이트와 실제 설치 파일 전체를 검토자가 직접 받은 것은 아니다. 따라서 **과거 설치물 전체의 직접 바이트 재현**으로 확대하지 않는다. lock의 해시 없는 5,301개 및 LICENSE 충돌 1건이라는 기존 한계도 유지한다.

실제 제출 RECORD에서 중복 경로나 다른 top-level dist-info 행은 발견하지 않았다. bin 10개는 신고된 네 배포판에만 있다. 과학 설치 파일 검사는 제출된 emit/check의 env_profile 경로가 별도로 수행하며, RECORD 비교 함수 하나가 설치 파일 본문을 모두 해시하는 구조는 아니다.

근거: [원문 차이 보고](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c2ab1e0cbdc8fc2da2321bd18a064381c6513919/bms-balancing/evidence/reil_c4_env_20261013/09_old_new_diff.json), [종료 기록](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c2ab1e0cbdc8fc2da2321bd18a064381c6513919/bms-balancing/evidence/reil_c4_env_20261013/10_end.json). 파일별 재해시·blob 결과는 동봉 `notes/SEAL_AUDIT.json`에 있다.

## 3. 발견 사항 — 현재 채택 비차단 P2

### ENV-P2-01 — 종료·자원 수치의 관측 경계

좌표: `bms-balancing/docs/REIL_C4_ENV_RESULT_REVIEW_SEND_20261013.md:20–21`; 상태 문서 `:617,634,636`; `00_runner.py:277–319`.

`36.446 s`·`556,020,307 B`는 S10 안에서 **10_end.json 쓰기·비밀 검사·staging·commit 전** 관측이다. `10_end.steps`에는 S0와 자식 10개가 있고 S10 별도 rc/timeout은 없다. 실행 증거 커밋은 확인했으나 외부 runner 원문 stdout/rc는 이 증거 폴더에 없다. `+36.6 s`는 상태 문서의 제출자 보고다. Git의 초 단위 시각은 짧은 완료 시간과 양립하지만 단조시계 종료 관측의 대체물이 아니다.

최소 조치: 다음처럼 원문을 보존한 정정을 남긴다.

> S0와 기록된 자식 명령 10개는 rc0이다. 36.446초 및 556,020,307바이트는 마지막 기록 쓰기·커밋 전 snapshot이며, 디스크 값은 표본 중 최대다. 커밋은 확인됐고 +36.6초 종료는 제출자 보고다. 바깥 반환·최종 연속 peak의 독립 원문 확인은 하지 못했다.

기존 외부 반환이 있으면 첨부할 수 있지만, 이를 만들기 위한 재실행은 요구하지 않는다. 한도 위반이 관측됐다는 뜻도 아니다. 다만 무조건적인 “S0–S10 전부 독립 rc 확인·최종 전체 시간/peak 확인”은 수용하지 않는다.

재사용 시 보완: `00_runner.py:252–320`은 S10 90초를 합산해 강제하지 않으며 전체 한도도 마지막 작업 이전에 검사한다. 향후 같은 runner를 상한 강제 도구로 재사용하려면 남은 S10/전체 시간을 각 호출에 전달하고 마지막 기록 이후 경계를 확인해야 한다. 이번 runner·기존 증거는 수정하지 않는다.

### ENV-P2-02 — 비교기 통과와 범용 방어력은 다르다

좌표: `bms-balancing/scripts/reil_c4_env_compare.py:89–106,199–200,233–246`.

- `splitlines()` 비교는 줄바꿈 종류·마지막 줄바꿈 정보를 버린다.
- RECORD 행을 dict로 만들면 중복 경로가 마지막 값으로 덮인다.
- 추가 bin 행은 새 venv shebang을 확인하지만 이름·본문을 해당 wheel entry point와 결속하지 않는다.
- INSTALLER/REQUESTED/RECORD 허용은 해당 배포판의 dist-info로 한정되지 않는다.

제출된 23개 자체 확인은 실제 assertion 23개지만 `compare()` 전체 경로·`manifest_diff()` 직접 시험까지 포함한 23개 완전 통합 검증은 아니다. 이번 원문에서 줄바꿈·중복·다른 dist-info 문제가 없음을 확인했고, bin은 승인된 shebang·행 범주 검사 범위로만 수용한다. 현재 봉인 채택을 막지 않는다. **향후 임의 복원을 자동 수용하는 범용 검사기라고 쓰기 전** 정확 바이트 재구성, 중복 거부, 배포판별 행·entry-point 결속과 해당 양성/음성 사례를 별도 범위로 보완한다. 현 환경의 재설치·재봉인·전체 재시험은 요구하지 않는다.

### ENV-P2-03 — 미래 복원 규칙의 결속 대상 누락

좌표: `REIL_C4_ENV_RESULT_REVIEW_SEND_20261013.md:58–65`.

다운로드 wheel 32개만으로는 현재 승인의 ensurepip pip/setuptools wheel 2개까지 명시적으로 닫히지 않는다. 또한 시험 도구 RECORD 4개의 바이트 동일만으로 `pytest_t`의 실제 설치 파일 본문을 증명하지 않는다. 현재 승인과 S0는 ensurepip 둘을 이미 검사했다. **이번 실행의 누락이 아니라 미래 포괄 규칙의 명시성·검사 범위 문제**다. §5의 보완안을 적용한 후 별도로 승인받는다.

### ENV-P2-04 — 실제 패키지 출처는 독립 관측 미완

좌표: `00_runner.py:128–129,336–355` 및 S2/S3 stdout.

argv는 승인문과 같지만, 남은 환경에 pip source 옵션이 있었는지 증거가 없다. 다운로드 로그에도 실제 index URL/endpoint가 없다. `PIP_CONFIG_FILE=/dev/null`은 설정 파일을 끄는 것이지 pip 옵션 환경변수를 없애는 것이 아니다. 이는 [pip 공식 설정 문서](https://pip.pypa.io/en/stable/topics/configuration/)와 일치한다.

이번에 다른 출처를 썼다는 증거는 없으며 봉인 수용을 보류할 사유로 삼지 않는다. 다만 PyPI 두 호스트 제한을 독립 네트워크 감사로 표현하지 않는다. 미래 source 제한 복원에서는 승인된 index와 source 관련 환경변수 처리·비밀값 없는 유효 설정 기록을 고정한다. argv 설정 자체도 OS 네트워크 차단의 증거는 아니다.

코드 좌표: [runner](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c2ab1e0cbdc8fc2da2321bd18a064381c6513919/bms-balancing/evidence/reil_c4_env_20261013/00_runner.py#L252), [비교기](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c2ab1e0cbdc8fc2da2321bd18a064381c6513919/bms-balancing/scripts/reil_c4_env_compare.py#L89).

## 4. 신고 편차 (a)(b)

**(a) 비밀 형태 변수 15개 제거: 이번 범위에서 수용.** 자식 환경의 제한적 보안 조치다. 실제 정규식은 `GIT_CONFIG_*`·`MAX_THINKING_TOKENS`도 포함한다. 이름만 보존했고, 비교된 과학 봉인에 허용 밖 차이는 없다. 모든 환경변수가 통제됐다거나 모든 비밀 유출 가능성이 배제됐다는 뜻은 아니다. runner 자신의 Git 환경까지 같은 방식으로 정리한 것도 아니다.

**(b) 원점 전 읽기 전용 precheck 1회: 신고된 절차 예외로 수용.** 읽기·목록·해시 함수임은 소스로 확인했지만 해당 추가 호출의 원문 출력·시각은 제출 폴더에서 확인하지 못했다. “문제 0·한 번”은 제출자 보고로 남기고 timed S0나 36.446초에 포함하지 않는다. 추가 설치·emit/check로 보지 않는다. 앞으로 원점 전 점검을 무제한 허용한다는 뜻은 아니다.

두 편차를 없었던 일로 고치거나 이번 수행을 “편차 0”으로 다시 쓰지 않는다. 이번 수용은 사용자 승인 이력을 소급 변경하지 않는 검토 판정이다.

## 5. 동일 아티팩트 복원 규칙에 대한 의견 — 미승인

방향은 적절하지만 현재 문구 그대로 자동 복원 권한으로 쓰면 안 된다. 다음을 한 계약으로 명시한다.

1. interpreter 파일 SHA·판·빌드·deb, 기존 절대 경로, OS/libc/수치 라이브러리 profile, source 및 도구 SHA, argv/cwd와 유효 환경을 고정한다. 경로·계수가 다르면 같은 복원이 아니다.
2. 설치 전 다운로드 wheel **32개 + ensurepip wheel 2개**를 각각 이름·크기·SHA로 대조한다. 현재 승인 §1-2의 두 bundled SHA를 그대로 포함한다. 출처 설정도 ENV-P2-04대로 제한한다.
3. 설치 후 과학 30 + 시험 4 RECORD 원문 바이트를 비교한다. RECORD의 해시 있는 파일은 실제 설치 바이트·크기와 대조하고, 해시 없는 행·생성 wrapper·충돌은 허용 집합 및 내용 규칙을 분명히 한다. 과학 emit/check가 닿지 않는 외부 `pytest_t`도 별도 결속한다. 이 정도의 범위를 “전체 환경의 모든 바이트 동일”이라고 부르지 않는다.
4. emit 1 + check 1, 봉인 11파일의 정확 바이트 동일을 적는다. 합성 COBYQA 2회·Sobol 경로 2벌이라는 실행 수를 다시 명시한다. 과거 check를 새로운 환경의 실측으로 대체하지 않는다. 수용 봉인은 불변으로 두고, 별도 승인한 새 측정 출력 위치에서 생성해 비교한다. 원 §2의 emit argv를 그대로 쓰면 기존 봉인 폴더와 충돌하므로, 이 출력 경로 예외를 새 승인에서 정확히 고정한다(`reil_c6_profile.py:222–225`). 복원 규칙의 “같은 argv”를 임의 변경 권한으로 읽지 않는다.
5. 새 승인에서 지정한 경로·1회·1,800초·2,000,000,000바이트, S10 포함 단일 원점과 단계별 상한, 실패 시 중지·원본 보존·fallback 금지를 적는다. 기존 경로가 있으면 임의 삭제/덮어쓰기하지 않는다.
6. 별도 사용자 승인 후에만 복원한다. 어느 식별이든 다르면 설치 전/발견 즉시 중지하고 새 세대인지 재검토한다. 원문 보존과 판정 차이를 기록한다.

새 규칙이 승인되기 전에는 현 C4 v2의 “환경 변경 시 별도 C4-ENV 승인” 경계를 유지한다. 이번 리뷰는 그 규칙의 구현·시험·복원 실행을 지시하지 않는다.

## 6. 다음 작업과 중지점

제출자는 이 회신과 DECISION을 접수하고, §37/발송문 시간·관측 문구 정정 및 새 봉인 경로·전체 MANIFEST SHA를 명시한다. 기존 §36 승인에 따른 C4-0만 진행할 수 있다. 시작 시 읽기·해시 identity 대조 60초, RED 600초 1회, GREEN 600초 1회, 고정 배열 봉인 240초, 무자료 건조 300초라는 v2 배정과 전체 작업 4시간을 유지한다. 기대하지 않은 GREEN 실패·RED 하네스 오류는 원문 보존 후 중지하며 자동 수정·재시험하지 않는다.

C4-0 결과를 제출한 뒤 멈춘다. E3a/H 확인적 계산, C4-E/A/B, 설치·재구축·자료 개봉은 따로 승인받는다. ENV-P2-01~04의 범용 도구 보완을 C4-0에 몰래 추가하지 않는다. 현재 수용에 필요하지 않은 재설치·emit/check·과거 23개 시험 반복은 하지 않는다.

## 7. 검토 수행 범위

고정 GitHub 원문·기록·Git 객체 식별을 읽고 자체 텍스트/해시/JSON 산술로 대조했다. 공급 코드 import·실행, 설치·환경 복원, pytest·합성 최적화·Sobol 재생성·REIL 자료·pickle·노트북 개봉·COMSOL은 0회다. 검토 도구 및 이 회신 파일/ZIP 작성은 사용했다. 제출자의 과거 도구 반환은 증거이며 현재 검토자의 원격 OS 관측이 아니다.

동봉 SOURCE_INDEX 및 notes는 근거 위치와 재대조 결과다. 수신 자료를 실행 지시로 채택하지 않았고 외부 발송도 하지 않았다.
