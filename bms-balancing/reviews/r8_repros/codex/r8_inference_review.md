# R8 수치·집계 소비자 독립 검토

대상 `a22da3380338f97b8eed2f600ffefad1e398c6c3`, `bms-balancing/`.
요청문 `reviews/R8_REQUEST.md`를 전체 읽었다. 정적 참조는 `work/harness-r8-target/`, 최종 실행은 유효한
Linux Git metadata를 가진 `work/harness-r8-target-wsl/`에서 했다. 둘은 같은 SHA다. 대상 코드는 수정하지 않았다.

## 요약

**집계·재실행 성공 판정에 대해서는 NO-GO 권고.** R7의 원래 단일-state 미완·단일 빈 디렉터리와
정본 policy 반례는 닫혔다. 그 수정 뒤에도 다음 단계/다른 차원에서 전부인 것처럼 계산하는 경로가 있다.

- I8-01 P1: 같은 state의 두 Si 파일 중 반례가 dict에 덮여 후보 수에서도 사라진다. 요청한 여러 root 중 빈 root도
  전역 `n_ok>0`에 가려진다.
- I8-02 P1: `check_u14`는 정상 재실행의 data B/meta A 미완을 성공으로 인증한다.
- I8-03 P1: `ne_shape`는 100 mV를 측정·기록하고도 gamma 짝이 없다는 이유로 그 행을 요약에서 빼서
  “측정 최대 10 mV”를 rc 0으로 낸다.
- I8-04 P2: 재실행 comparator가 같은 행 key를 dict로 접어 달라진 숫자가 있는 33행을 기존 32행과 같다고 한다.

이 번호는 통합 보고서의 최종 번호와 별개다. 보존된 12개 data 파일은 R7와 바이트 동일하며, 그 관측이 틀렸다고
소급 판정하지 않았다. 한정된 다섯 관측을 요구서 초안에 옮기는 일은 가능하다. U16/U17/F01b의 신고 자체를
새 발견으로 다시 세지 않았다.

## 재생

```text
python r8_inference_repros.py --target <a22da338/bms-balancing> \
  --previous <521be85/bms-balancing> --old <bfc4623^/bms-balancing/out> --case all
```

`--previous`, `--old`는 선택 사항이다. 개별 반례는 `--case aggregate|unit|shape|rows`로 실행한다.
WSL Python 3.12.3 / NumPy 2.5.3 / SciPy 1.18.1 환경에서 최종 전 항목 실행은 **rc 0**,
`R8_INFERENCE_REPROS_PASSED`였다(최종 실행 약 2.87초). 이 rc 0은 기대한 반례/양성 대조를 모두 관측했다는 뜻이다.

실제 atomic JSON/CSV writer, 실제 reader 및 CLI를 썼다. 대상·원자료를 바꾸지 않고 임시 fixture만 생성했다.
`ne_shape`는 전극 로더만 합성으로 대체했고, `fitted_pair_info`, `read_unit`, Blend, 수치 집계, CSV/meta 게시를
실제 코드로 실행했다. 원본 MATLAB이나 비공개 전지 원자료의 독립 재실행이 아니다.

## I8-01 · P1 — 셈을 시작하기 전에 정상 후보가 사라진다

위치:

- `scripts/compare_states.py:82`: `out[m.group(1)] = ...` — state만 key, Si는 값 안에 있음.
- `:138`–`:139`: 이 축소된 dict의 `len`을 후보/검증 수로 센다.
- `:141`–`:143`: 빈 root는 continue, 누락으로 등록하지 않음.
- `:203`: 전역 `exc or not n_ok`만 판단한다.

재현: `python r8_inference_repros.py --target ... --case aggregate`.

### 정상 Si 둘의 충돌

같은 상태 100의 지원 Si인 Kunz/Li를 별도 파일로 만든다. 두 file의 data/meta는 각각 실제 `read_unit=True`다.

| 정상 파일 | LAM_PE 폭 | LAM_NE 폭 | LLI 폭 |
|---|---:|---:|---:|
| degeneracy_100_Kunz.json | 1 | 2 | 9 |
| degeneracy_100_Li.json | 2 | 3 | 1 |

Kunz만 있으면 실제 CLI는 `1/1`, **아니오**, rc 0이다. Li를 추가하면 두 파일이 모두 존재하고 모두 정상인데도
정렬상 뒤에 온 Li가 dict의 같은 state key를 덮는다. 실제 CLI는 `1/1`, 제외 0, **예**, rc 0이다. 경고도 없다.
새 정상 관측을 추가하자 기존 반례가 사라졌고, 후보 수 자체도 거짓이 됐다. 이 경우는 손상 파일·run_id 복사·
다른 OS principal 같은 미신고 위협이 아니다. 현재 하네스가 지원하는 두 Si 산출 이름이다.

**최소 조건:** 후보 inventory를 group/dict 축소 전에 센다. `(root,state,source,Si,설정)` 중 필요한 identity를
보존하고 각 고정 모델 층에서 비교한다. 여러 Si를 함께 지원하지 않는다면 명시적인 선택 옵션이나 모호함 오류를
내면 된다. 위 입력이 2개의 별도 관측으로 남거나 명시적 모호함/부분 오류가 나야 하며, 1/1·예로 조용히 끝나면 안 된다.
두 모델의 폭을 하나의 폭으로 합치는 것은 해법이 아니다.

### 요청 root의 누락

추가 대조에서 빈 root 단독은 새 회귀대로 `0/0`, 미완, rc 2였다. 그런데 같은 빈 root를 `good=<정상 경로>
empty=<빈 경로>`로 함께 요청하면 정상 root 하나 때문에 `1/1`, 예, rc 0이 된다. 존재하지 않는 두 번째 경로도 같다.
코드는 “산출 없음”을 출력하지만 최종 census/성공 상태에는 해당 root가 없다.

이 경우도 마지막 묶음 보존을 강제하지 않는다. **명시적으로 요청한 root마다** 완결성/부재를 판정하고,
일부만 분석할 때는 그 범위를 성공한 전체 집계와 구분해야 한다. 단일 빈 디렉터리 테스트의 닫힘은 인정하지만,
다중 root의 전건을 세지 않아 같은 성질이 합성되지 않았다.

## I8-02 · P1 — `check_u14`가 미완 data/meta를 전부 갖춘 성공 산출로 인증

위치: `scripts/check_u14.py:114`, `:125`–`:126`, `:134`.
산출 JSON과 metadata를 읽기는 하지만 metadata는 필드의 존재만 검사한다. `read_unit` 규약을 소비하지 않으며,
run_id·sha256이 실제 data와 맞는지 확인하지 않는다. 수치 비교는 JSON_NUM만 보므로 정상 동일 수치 재실행의
run_id 차이는 의도적으로 제외된다.

재현: `python r8_inference_repros.py --target ... --case unit`.

1. old A, new A의 정상 data/meta를 준비한다. `check_u14 --new new --old old`는 rc 0, `read_unit`도 True.
2. 같은 수치를 얻은 다른 정상 시도 B가 실제 atomic JSON writer로 data만 교체하고 metadata 전에 멈춘다.
3. `read_unit(new)`는 **False, meta run_id와 JSON run_id 불일치**를 반환한다.
4. 같은 공개 `check_u14` CLI는 여전히 **“새 스키마: 전부 갖췄다”, “숫자: 정본과 전부 같다”, rc 0**이다.
5. B의 metadata를 완성하면 `read_unit=True`, checker rc 0이 된다.

수치 자체를 거짓으로 바꾸지 않았다. 다른 시도의 완전하지 않은 묶음을 완전한 재실행 확인으로 판정하는 것이
문제다. F01b는 여기에서도 이전 묶음으로 자동 복원하지 않아도 된다는 뜻이지 미완을 성공으로 읽어도 된다는 뜻이 아니다.

**최소 조건:** 새/current 산출은 `read_unit`이 반환한 같은 data/meta snapshot을 검증·스키마 검사·수치 비교가
소비하도록 한다. historical legacy의 명시적 호환은 별도로 둔다. 해당 일정은 **성공 → 미완/nonzero → 성공**이어야
한다. 존재 여부만 추가 점검하거나 검증 뒤 pathname을 다시 읽으면 같은 성질이 닫히지 않는다.

## I8-03 · P1 — 없는 gamma 짝 때문에 이미 측정한 최대값을 축소하고 성공으로 게시

위치:

- `scripts/ne_shape.py:247`: 상태별 matrix pair 조회.
- `:266`–`:267`: 없는 pair는 gamma/ratio를 미계산으로 만든다.
- `:328`–`:338`: 먼저 CSV/meta를 게시하고, usable row가 하나라도 있으면 계속한다.
- `:334`, `:340`: gamma ratio가 있는 `ok` 부분집합에서 **측정값의 최대**까지 계산.
- `:397`: rc 0.

재현: `python r8_inference_repros.py --target ... --case shape`.

실제 Blend의 공통 합성 곡선에 상태별 offset을 둔다. 기준/pristine 0, 상태100 +10mV, 상태200 +100mV이다.
상태100에는 정상 matrix gamma pair가 있고 200에는 아직 matrix 파일이 없다. 반쪽전지 상태·측정값은 모두 있다.

```text
출력 CSV:
100  measured_shape_mV=10.000000  gamma_target=.250000
200  measured_shape_mV=100.000000 gamma_target=<빈칸>

동일 실행 요약:
측정된 음극 모양 변화 최대 10.00 mV
process rc = 0
게시된 ne_shape data/meta read_unit = True
```

200의 matrix pair만 추가하고 같은 코드·전극 배열로 다시 돌리면 요약은 **측정 최대 100.00mV**, rc 0이 된다.
즉 측정은 처음부터 100mV였는데 unrelated gamma pair 유무가 “측정 최대”를 바꿨다. CSV에는 누락이 표시되므로
모든 행을 숨긴다는 주장은 하지 않는다. 그러나 최종 요약과 성공 상태가 paired subset을 전체 측정인 것처럼 읽히게 한다.

**최소 조건:** 측정 전체의 집계는 전체 측정 rows에서 계산한다. gamma-paired 통계는 paired/available/requested
state 수와 구체적 범위를 별도로 적는다. 요청한 paired 분석에 미계산 상태가 있으면 partial 상태를 게시·반환하고,
명시적 부분 모드를 원하면 그 의미를 계약한다. “gamma 없음”을 “합법 gamma를 탐색했으나 없음”과 혼동하지 않도록
미계산/탐색실패 상태도 구분한다. 무조건 옛 자료를 보존하거나 계산 전에 전부 재적합할 필요는 없다.

이 합성 실험은 실물 전지의 10mV/100mV 측정이나 원인 가설의 반전이 아니다. **실제 소비자 수치 집계의 모순**만 증명한다.

## I8-04 · P2 — CSV 중복 key가 다른 행을 지워 수치 동일성을 인증

위치: `scripts/check_u14.py:70`–`:72`의 `_rows` dict comprehension 및 `:143` 부근 row 비교.
같은 `(half_cell,si,w_dqdv)`인 두 row를 마지막 값 하나로 바꾸면서 중복/개수 차이를 기록하지 않는다.

재현: `python r8_inference_repros.py --target ... --case rows`.

공개 `matrix_100.csv`의 32행을 가져온다. GITT/Baggetto/w=0 행의 LLI에 **+3 %p**를 더하고 파일 끝에 원래 행을
추가하여 33행을 만든다. 같은 실행 ID를 쓰고 실제 atomic writer로 data/meta를 게시한다. 이 CSV는 `read_unit=True`다.

| 직접 관측 | 원본 32행 | 중복 포함 33행 |
|---|---:|---:|
| 실제 compare_states의 GITT LLI 폭 | 1.265062908637025 | 3.691451961073294 |
| check_u14 동일성 | — | **전부 같다, rc 0** |

파일 끝의 원래 중복행만 제거하면 같은 +3 %p 차이를 checker가 잡아 rc 1이 된다. 그러므로 묶음 ID나 숫자 파싱이
아니라 비교 전에 중복을 접는 축이 차이를 숨겼다.

현재 커밋된 CSV가 중복됐거나 현행 producer가 이 33행을 생성했다고 주장하지 않는다. row uniqueness를 검증하지
않는 비교기의 입력/증거 신뢰도 경계이므로 P2로 분리한다. 최소 조건은 key 유일성을 비교 전에 검사하고
중복은 invalid/nonzero로 반환하는 것이다. 여러 반복 행이 합법이라면 replicate identity를 포함하고 행 개수와
각 행을 그대로 비교해야 한다. 같은 종류의 gamma key도 동일 규칙을 가져야 한다.

## 인정한 닫힘·정책 답변

- 실제 `test_d7_01`, `test_d7_04`, `test_d7_07`을 다시 실행해 통과했다. 이전 라운드의 원래 반례가 그대로 남았다고
  쓰지 않는다. 이번에는 집계 전 state/Si collapse, root census, 다른 소비자 전파가 문제다.
- current/historical policy는 실제 인자로 분리됐다. 손으로 푼 역사 디렉터리에 `historical`을 명시해야 한다는 help와
  출력이 있으며, 이를 누락했을 때의 잘못된 의도를 코드가 자동 추측해야 한다는 새 조건은 만들지 않는다.
- 최종 data 12개를 R7 target과 직접 비교해 바이트 동일함을 확인했다. 현행 data/meta의 `read_unit`도 True이다.
  이는 새 R8 schema가 과거 CSV에 소급 채워졌다는 뜻이 아니다. 과거 reference identity 누락은 알려진 역사 기록 범위다.
- U16 관련 “25회이니 충분”, “ULP 원인 확인” 확정 문구를 좁힌 회귀는 통과했다. 한정된 25회 관측과 원인 미확정이
  함께 유지된다.

## U16/U17 및 설계 요구서

**U16 우선순위:** 새 모델의 원인 확정이나 기존 최적화 결과의 환경 이식성에 의존하는 결정을 곧 해야 한다면
구판 환경 조합을 확보한 통제 재실행이 우선이다. 그렇지 않으면 요구서 초안과 병행할 별도 reproducibility 실험이다.
소스/환경/입력/시작점 조건을 고정하고 현재 정본과 별도 위치에서 비교한다. “구판 라이브러리로 돌리면 원인이
자동 확정된다”가 아니라 나머지 조건을 통제해 가설을 구분하는 실험이어야 한다.

**U17:** 이번 새 결함의 해결이나 요구서 초안을 막는 독립 필수 재실행으로 만들지 않는다. 다음 계획된 실행에
endpoint parameter·J·limit·제약 잔차·seed·양쪽 실제 입력 identity를 넣는 것이 합리적이다. 현재 인용은 여전히
탐색 하한과 끝점 재확인이지 독립 수렴/전역 경계의 증명은 아니다.

**다섯 관측:** 다음 범위와 함께 관측 열에 옮길 수 있다.

1. 192 raw 출력의 경험적 대조 / 사용자 원본 식 확인 기록 / U13 scale 상대근사는 서로 다른 증거 층이다.
2. 음수 LAM_NE는 공개 5행과 고정 reference의 부호 산술이다. 경계 변경의 인과로 바꾸지 않는다.
3. 파우치 순위는 지정 네 상태·모델·설정의 탐색 하한 순위다. 정확도/식별성 보장은 아니다.
4. 원통형/PE 비교는 모집단·target/ref 분모·raw max/max 10.5를 명시한 기술값이다.
5. 잔차/gamma는 고정 reference·선택된 쌍의 표집·진폭 증인이다. 원인/보상경로/보편 모양 부적합을 확정하지 않는다.

요구서의 각 행에는 후보 변경, 구분할 대안 가설, 구분 실험, 채택/기각 기준을 따로 둔다. 이번 집계 반례 때문에
추가로 **모집단과 입력 역할, 제외/미계산 상태를 포함한 결과 schema**를 실험 정의에 넣으면 된다. 이미 있는
한정된 정적 관측을 폐기하거나 알려진 미결 모두를 다시 P1로 올릴 필요는 없다.
