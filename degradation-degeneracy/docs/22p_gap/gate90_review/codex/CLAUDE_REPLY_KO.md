# GATE90 검토자 회신

2026-10-05. 요청 HEAD `24f499ba6a5e45a75613e9842ce99a679b5ce863`, 코드 `e2160c2ef`를 검토했습니다.

**판정: 수정 조건부 수용. G90-N1 P2 1건. 실행 GO 아님.**

C lock의 정규형·170개 배포판/가려진 2개/RECORD 없는 22개, B 네 manifest의 여덟 env 자리, requirements 요구 줄 12개 불변, smoke/stamp 연결, 영수증 history 보존은 수용합니다. RUN_SCOPE 60개 바이트로 `3f84c0db52d2b9ac`를 독립 재계산했습니다. 제출 로그 17개 크기/SHA를 확인했고, 2177 passed·smoke rc0·410/410·발송 docs-lint 358 passed는 제출 원문 확인으로 구분합니다.

**G90-N1:** `tools/env_profile.py:110–130`은 PathFinder가 현재 경로에서 찾은 파일만 RECORD와 대조합니다. sys.modules에 이미 로드된 객체와 meta-path 선택은 확인하지 않습니다. 기존 캐시 객체가 다른 경로에서 왔어도 PathFinder는 정상 설치 파일을 찾을 수 있으므로, 이를 “실제 로드된 module origin 확인”이라고 부를 수 없습니다. 현재 환경에서 실제 오염이 있었다는 판정은 아닙니다.

권고하는 최소 종결은 이번 C를 **경로 검색 결과와 설치 RECORD의 기록 대조**로 명확히 좁히는 것입니다. origins_verified·요청문·고정 표의 유효 정정·stamp 설명을 그 의미로 맞추고 실제 loaded-origin은 미측정으로 남기세요. 기존 MATCH와 과거 수치 수용은 이 범위로 보존합니다. 실제 loaded-origin 보장이 필요하다면 그 변경·한정 검증은 새 승인 범위로 분리하세요. D guard나 계산을 이 회신으로 시작하지 않습니다.

비차단 C1: “UNMEASURED는 pytest도 막지 않는다”와 e06의 UNMEASURED 실패는 적용 범위를 구분해 적어 주세요. CLI/운영 호출의 기록 전용 상태와 측정 기능 회귀의 환경 전제를 나누면 됩니다.

이번 리뷰는 제출 프로그램 import/실행·회귀·smoke·변이 재생·복원·계산·설치를 하지 않았습니다. 리뷰어 데이터 검사와 표준 라이브러리 불활성 예시만 실행했습니다. N1 정정 접수 전 무조건 종결은 보류하며, 나머지 수용 부분을 다시 열 필요는 없습니다.
