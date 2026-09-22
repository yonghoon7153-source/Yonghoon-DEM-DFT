# R17 재현 자료

대상: dfc1fc78b3396c95709650860f1502c0e83ead40, bms-balancing.
production 수정 없음. 실데이터나 COMSOL 계산 없음.

## 이 PC에서 재현
PowerShell 작업 위치:
C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2

다음을 각각 실행한다.

    $env:PYTHONUTF8='1'
    $env:PYTHONDONTWRITEBYTECODE='1'
    & './work/r17-venv/Scripts/python.exe' './outputs/r17_review_20260922/repro_r17.py'
    & './work/r17-venv/Scripts/python.exe' './outputs/r17_review_20260922/science_repro.py'

예상: 두 스크립트 rc 0. 첫 스크립트의 rc 0은 취약한 동작을 검증한 reviewer assertions가 맞았다는 뜻이다. production 교정 후에는 그 assertions가 깨져야 한다.
첫 스크립트는 REPRO_RESULTS.json, 둘째는 SCIENCE_REPRO_RESULTS.json을 갱신한다. 매번 고유 fixtures-*를 만들어 사용자 파일을 덮지 않는다. 기존 결과를 보존하려면 별도 리뷰 폴더 사본에서 재생한다.

의존: Python3.12, numpy2.5.3, scipy1.18.1, pandas3.0.6, openpyxl3.1.5. pip freeze는 REVIEW_IDENTITY.json에 보존한다.
다른 PC에서는 스크립트의 ROOT만 별도 고정 checkout의 bms-balancing으로 바꾸고 그 변경을 기록한다. 변경된 target에는 원래 리뷰 결과를 적용하지 않는다.
legacy 정상 대조군은 42314198e0beee59834d394cdba2757183503b59 객체도 필요하다.

## 안전·증거 범위
- GC --apply의 root는 이 리뷰 폴더가 만든 새 fixture이고 절대 경로 containment를 assert한다. 삭제된 것은 생성한 A 디렉터리 두 파일뿐이며 재생성 가능하다.
- Windows에서는 index 기록의 fcntl 경로를 돌릴 수 없어 문서화된 index를 fixture에 직접 썼다. GC 자체와 목적지 결정 함수는 수정하지 않았다.
- partial canonical 반례는 목적지 반환만 관측했다. canonical 산출 쓰기는 하지 않았다.
- width 입력은 실제 열/receipt 역할을 가진 합성 CSV다. 실데이터 두 파일이 다르다고 주장하는 증거가 아니다.
- negative-tol 반례는 실제 _width_fields 및 최적화 함수 호출이다.
- convex quadratic 사례는 추론의 반례이고 실제 배터리 목적함수가 볼록하다는 주장이 아니다.
- chain rule 분석 곡선은 수학적 일관성 검사다. 작성자 fitting 200배·외부 pyDMA 숫자를 재현한 것이 아니다.
- receipt signature는 공개 hash 함수로 계산했다. 비밀키 서명 위조/원격 시스템 접근을 수행하지 않았다.

R17_REVIEW.md에 각 결과 key, 코드 위치, 기대/실제, 최소 종결 조건이 연결돼 있다.

