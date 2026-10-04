# GATE90 환경 고정 라운드 검토

2026-10-05. 판정은 **수정 조건부 수용**이다. **G90-N1 P2 1건**이 남는다. C lock·B 역사 프로필·파일 범위·기록 연결·제출된 회귀 근거는 아래 한계로 수용한다. C의 경로 검색 관측을 실제 로드 관측으로 부르는 부분은 정정해야 한다. 실행 GO, 설치, 버전 비교 계산, D 생산 guard 구현을 승인하지 않는다.

## 대상과 검토 방법

- 저장소: yonghoon7153-source/Yonghoon-DEM-DFT
- 요청 HEAD: `24f499ba6a5e45a75613e9842ce99a679b5ce863`.
- 코드: `e2160c2ef276d4944fa4ad76fbaa001671a1a95e`.
- 요청문: `degradation-degeneracy/docs/22p_gap/GATE90_REQUEST.md`.
- 발송 뒤 증거 보충: `4432dfc1ae336617c61c62bb8b15ad3f499c79f7`의 README 및 14번 docs-lint 로그.
- 독립 재계산한 RUN_SCOPE digest: `3f84c0db52d2b9ac`.

GitHub 고정 ref에서 읽은 텍스트 44건의 UTF-8 바이트를 Git blob SHA와 대조했다. 이전 수신 검토의 RUN_SCOPE 원문은 이번 고정 tree의 blob과 전수 대조한 뒤 재사용했다. 60개 파일을 경로·바이트 순서로 다시 해시했다. 제출 프로그램 import·실행, pytest/smoke/변이 재생, 영수증 복원·재채점, COMSOL/JVM/PyBaMM 계산과 설치는 수행하지 않았다.

리뷰어 소유의 데이터·해시·AST 검사와 Python 표준 라이브러리의 불활성 예시만 실행했다. AST는 함수 실행에 사용하지 않았다. 원격 환경이나 설치 파일 24,804개를 이 검토자가 직접 측정했다는 뜻은 아니다.

## G90 N1 실제 로드와 경로 검색을 구분해야 한다

**P2. 위치:** `tools/env_profile.py:8–12,110–130,167–185,297–298,338–343`, 고정 표 §4-1, 요청문 §1·§4·§5의 origin 표현.

`_origin()`은 `PathFinder.find_spec(module, paths)`가 찾은 파일이 유효 배포판 RECORD에 있는지를 확인한다. 현재 프로세스의 `sys.modules[module]`에 들어 있는 객체나 그 객체의 `__file__ / __spec__.origin`은 읽지 않는다. 전체 `sys.meta_path`의 다른 finder 선택도 관측하지 않는다.

따라서 예전에 다른 경로에서 로드한 모듈을 캐시에 유지한 뒤 검색 경로가 정상 설치 경로로 바뀌면, 다음 두 사실이 동시에 성립한다.

1. PathFinder가 정상 설치 파일을 찾아 RECORD 소속 확인에 성공한다.
2. 일반 import는 정상 설치 파일을 새로 읽지 않고 기존 캐시 객체를 반환한다.

현재 대조 코드는 캐시 객체 변경을 입력으로 읽지 않으므로, 설치·RECORD·경로 조건이 같은 두 상태를 구별하지 못한다. 그 상태에서도 origin 확인 수와 MATCH가 같을 수 있다. 이는 정적 제어 경로로 확인한 반례이며, 제출자의 실제 환경에서 이 일이 발생했다고 주장하지 않는다.

Python 공식 문서도 import가 먼저 sys.modules를 확인하며, PathFinder는 경로 기반 finder임을 구분한다. [모듈 캐시와 import hooks](https://docs.python.org/3.11/reference/import.html#the-module-cache), [PathFinder](https://docs.python.org/3.11/library/importlib.html#importlib.machinery.PathFinder).

리뷰어의 `IMPORT_SEMANTICS_ILLUSTRATION.json`은 같은 구분을 표준 라이브러리로만 확인했다. 임의의 독립 이름으로 메모리 ModuleType을 캐시에 두고, PathFinder는 별도 불활성 파일을 찾도록 했다. 제출 env_profile이나 과학 패키지는 import하지 않았고 fixture 파일 본문도 실행하지 않았다. **이 예시는 제출 compare_lock을 실행한 시험이 아니다.**

### 최소 종결 조건

권고는 **이번 기록 대조의 주장을 정확히 좁히는 정정**이다.

- 확인한 것은 “PathFinder 경로 검색 결과와 설치 RECORD 소속”이라고 기록한다.
- `origins_verified`의 단위도 이 범위로 명시한다. 실제 이미 로드된 모듈·다른 meta finder·메모리 상태의 확인이라고 부르지 않는다.
- 실제 loaded-origin 대조는 미측정으로 남긴다. 기존 MATCH는 이 좁은 의미로 보존하고 과거 수치 결과를 실패로 소급 변경하지 않는다.
- 요청문·고정 표의 유효 정정·영수증 stamp 설명·최종 요약이 같은 의미를 사용해야 한다.

실제 loaded-origin을 이번에 보장하려는 선택을 하면, 별도 승인 범위에서 이미 로드된 객체와 경로 검색을 구분하여 관측하고, 불명확한 값은 확인 수로 올리지 않는 한정 보완이 필요하다. 정상 대조·캐시 origin 불일치·origin 없음 등의 반례가 대상이며, 이를 이유로 native 계산이나 D guard 범위를 자동 확대하지 않는다. 단순히 이 리뷰를 받았다고 수정·재시험이 승인되는 것은 아니다.

## 비차단 문구 보완

**C1. D3의 pytest 설명을 정밀하게 한다.** 고정 표 §4-4는 UNMEASURED가 pytest도 막지 않는다고 쓰지만 `tests/test_gate90_env_profile.py:386–390`의 e06은 그 상태를 명시적으로 실패시킨다. e08 역시 실제 측정이 가능하다는 전제 아래 MISMATCH를 요구한다.

요청문 §6-g가 이미 이 사실을 신고했고, 대조기 CLI·smoke·stamp의 기록 전용 처리와 “측정 기능 자체를 시험하는 회귀”는 구분할 수 있으므로 별도 차단 항목으로 세지 않았다. “C 일치 여부는 실행 gate가 아니나, 측정 기능을 요구하는 회귀의 지원 환경에서는 측정 불가를 시험 실패로 본다”로 경계를 명시하는 편이 정확하다. 모든 장비에서 전체 suite가 UNMEASURED를 수용한다는 주장은 하지 않는다.

## 판정 요청별 답

| 요청 | 판정 |
|---|---|
| 1 C lock 내용·닫힌 문법·정규형 | 커밋된 lock의 6개 지시·170개 유효 배포판·가려진 2개·RECORD 없는 22개와 정규형 고정점을 독립 데이터 검사로 확인. 수용 |
| 2 대조와 D3 경계 | 일반 오류의 typed UNMEASURED 및 None 처리, 상태별 CLI rc0 구조는 수용. 실제 origin 주장은 N1 정정 필요. C1의 회귀 적용 경계 명시 |
| 3 smoke·stamp·증거 연결 | smoke의 단일 호출과 도구 자체 실패 처리, core 밖 stamp 연결은 수용. loaded-origin 증명으로 확대하지 않음 |
| 4 B 역사 기록 | 네 producer manifest의 크기·SHA와 여덟 env 자리의 13개 값 일치 확인. solver 전사와 역사적 한계 명시는 수용. B 재설치 가능성·B=C·수치 동등은 미주장 |
| 5 requirements | 요구 줄 12개 불변 확인. 주석 정정 수용. C lock은 pip 설치 처방이 아니며 requirements 하한은 그대로 |
| 6 회귀·변이·영수증 | 제출 원문 근거로 수용. 독립 재실행은 아님. N1을 덮는 시험은 현 목록에서 확인되지 않음 |

## 독립 확인한 파일과 근거

- 89차 코드 기준과 요청 HEAD의 RUN_SCOPE 순변경은 lock·env_profile·requirements 주석·smoke의 네 파일이다. 판정 코드에서 요청 HEAD까지 RUN_SCOPE 순차이는 0이다. 이는 고정 끝점 대조이며 모든 중간 커밋의 파일 변경 이력을 전수 실행 감사한 주장은 아니다.
- C lock SHA-256: `d886f30ff675fef723fb9bcedd98297910fb1f8f1809370c18d8980dc5e63b39`.
- 제출 증거 로그 **17개**의 크기·SHA를 README와 독립 대조했다. 뒤에 추가된 14번 docs-lint도 포함한다.
- 전체 회귀 원문: clean `257d4cc1c`, **2177 passed / 1 xfailed / rc0**. xfail은 기존 저장소 밖 입력 staging 한 건이다.
- strict smoke 원문: **rc0**. 내부의 작은 계산은 제출자 실행 이력이며 이번 리뷰는 재실행하지 않았다.
- 전체 재생 로그 줄머리를 독립 집계: **물었다 410 / 안 물었다 0 / 실행오류 0**. 시작·종료 및 rc 기록도 제출 원문에서 확인했다.
- 발송 HEAD docs-lint 원문: **358 passed / rc0**, 시작·끝 HEAD `24f499ba6`, dirty 0.
- 두 이전 영수증은 89차 발송 ref의 원문과 현재 history 사본이 바이트 동일하다. core의 내용 차이는 validator_source_digest와 make_receipt_sha256뿐이며 bundle·restore·validation·outputs 내용은 불변이다. 새 core_sha256은 원장에 결속되어 있다. 이 검토는 YAML을 재직렬화하여 core hash를 재생성하거나 복원·재채점하지 않았다.
- 새 grid 영수증의 dirty=true를 지우거나 clean으로 바꾸어 읽지 않았다. paired/grid 순차 작성 시점의 stamp와 전체 검증의 clean 관측은 서로 다른 기록이다.

## 자체 신고와 검토 한계

요청문 §6 a–k 중 목록 확대·메시지 결정화·경로 중복·다른 드라이브의 측정 불가·RECORD 없는 배포판·장비 차이·e06의 측정 가능성 전제·핵심 모듈 목록·범위 밖 문서 커밋·env 7→8 정정·profile_not_c 추가를 읽었다. 현재 보고된 통과를 임의 실패로 바꾸지 않는다. RECORD 없는 항목, 해시 없는 파일, native 라이브러리 및 loaded-origin은 확인된 범위를 넘겨 주장하지 않는다.

리뷰어 첫 텍스트 검사도 YAML anchor/alias를 누락해 중지했다. 리뷰어 판독기만 보완한 뒤 통과했으며, 제출 소스·시험 실패로 세지 않았다. 선택적 PyYAML 확인이 실패했지만 설치하지 않았고 제한된 텍스트/anchor 대조를 사용했다. 해당 사실은 REVIEWER_TOOL_RETURNS.json에 기록했다.

## 다음 단계

N1의 관측 범위 정정과 C1의 경계 문구를 제출받아 이 기록 대조 라운드를 닫는다. 기존 정본·89차 수용·B 역사 기록·검증 실행 원문은 보존한다. D 생산 guard, 버전 간 수치 비교, 새 연구 leg, 운영 v6 계획, 세대표, p_ini, COMSOL, 설치는 여전히 별도 범위다.
