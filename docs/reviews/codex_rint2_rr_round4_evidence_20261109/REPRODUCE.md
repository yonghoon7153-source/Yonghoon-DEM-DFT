# 재현 안내 — Rint ② 회차 ④

고정 핀: 1f9f3607eb2f0118d322eeff780bba6eb17b85a2.
최종 판정: codex_review_rint2_rr_round4_20261109.md.
증거 ZIP은 연구 실행 키트가 아니다. 실제 WSL/ibb/GPU/DEM/S0/R/전체 게이트는 실행하지 않는다.

## 파일 구성

- input/: 원 첨부 ZIP. package/: 원 첨부를 바이트 그대로 푼 것.
- reference_round3/: 이전 고정 핀의 비교용 3파일만. 전체 저장소가 아니다.
- integrity.json, remote_provenance.json, dependency_delta.json: 해시·원격 고정 tree·의존 대조.
- arm_contract/: 독립 ARM 계약 탐침·원 회차③ 반례·오류/성공 로그·assert 변경 diff.
- resume_attack/: 독립 재개 탐침·실제 scratch Git recover 결과·frozen_cases 합성 입력. 개발 scratch Git 폴더는 포장하지 않았다.
- docs_tests/: 문서/시험 diff와 원로그 재집계, 24개 작은 검사, 새 M56 반례.
- scoped_regression.py/json: 제출 상주 시험의 제한된 재실행. 전체 495 검사는 아니다.
- verdict.json: 이 보고의 요약이며 원장 변경 파일이나 실행 허가서가 아니다.
- SHA256SUMS: 증거 파일 바이트 확인. ZIP 자체 해시는 별도 .sha256 파일.

## 안전·환경

이번 직접 실행은 Windows Python 3.12.14 및 설치된 NumPy/SciPy, Git이었다.
POSIX 잠금·부모 생존·프로세스 그룹은 해당 탐침에 적은 합성 대체를 사용했다.
ARM 탐침의 Python 자식은 작은 가짜 payload writer뿐이다. research solver를 호출하지 않는다.
resume 탐침은 **새 scratch Git 원장만** 만들고 실제 제품 Git에는 쓰지 않는다.
일반 임시 파일용 O_NONBLOCK=0을 FIFO·Linux 현장 자격으로 해석하지 않는다.

zip을 새 writable 폴더에 풀고 그 루트에서 아래를 실행한다. 실행한 결과 파일은 해당 증거 폴더에 덮어써지므로 원 ZIP은 보존한다.
Python/Git이 PATH에 있는 환경을 전제로 한다. PowerShell에서는 python 대신 해당 python.exe를 &로 호출할 수 있다.

~~~bash
python -I -X utf8 -B verify_bundle.py
python -I -X utf8 -B verify_remote_binding.py
python -I -X utf8 -B arm_contract/probe_arm_contract.py
python -I -X utf8 -B arm_contract/replay_original.py
python -I -X utf8 -B resume_attack/probe_resume_independent.py
python -I -X utf8 -B docs_tests/audit_docs_tests.py
python -I -X utf8 -B docs_tests/tiny_docs_tests.py
python -I -X utf8 -B docs_tests/probe_m56.py
python -I -X utf8 -B scoped_regression.py
~~~

예상:
- verify_bundle: pin/hash/파일 수 일치. verify_remote_binding: repo403, 의존26동일, 변경2.
- arm_contract: 9검사군, unexpected 빈 목록.
- replay_original: 내부 원문 probe rc1(옛 bug 존재 assert 반전), 두 assert 정정 사본 rc0. wrapper는 rc0. 원 rc1을 숨기지 않는다.
- resume: wrapper rc0. **모든 입력의 자격이 False라는 뜻이 아님.** PC14-02/03는 True로 살아 있는 것이 독립 관측이다. 네 실제 recover는 rc0이며 자격 False/True가 별도 필드다.
- tiny_docs_tests: 24/24.
- probe_m56: current=거부사유, mutant=null, distinguishable=true. 현재 코드의 새 재개 허용 결함이 아니라 동치 주장 반증.
- scoped_regression: t_RR3A/B/C, t_PA14A 4메서드와 PA14C 값 하위26행. 전체 method/full suite로 합산하지 않는다.

## 사용자 트리에서 같은 탐침을 실행할 때

ARM/replay/resume/docs 탐침은 RINT_REVIEW_REPO 환경변수로 **읽을 소스만** 바꿀 수 있다.
입력/출력과 scratch는 여전히 리뷰 증거 폴더 아래다. 무관한 제품 작업 트리를 수정하지 않는다.

~~~powershell
$env:RINT_REVIEW_REPO = 'C:/path/to/pinned/repo'
python -I -X utf8 -B arm_contract/probe_arm_contract.py
python -I -X utf8 -B resume_attack/probe_resume_independent.py
python -I -X utf8 -B docs_tests/probe_m56.py
python -I -X utf8 -B scoped_regression.py --repo 'C:/path/to/pinned/repo'
~~~

Linux 셸에서는 RINT_REVIEW_REPO=/path/to/pinned/repo 를 명령 앞에 지정할 수 있다.
실제 사용자 WSL/ibb에서 수행하라는 지시가 아니다. 로컬/격리 합성 환경에서만 재현한다.
과거 diff를 재계산할 때 RINT_REVIEW_OLD_REPO로 회차③ 트리를 지정할 수 있고, 기본은 동봉 reference_round3이다.
원격 tree 재대조는 저장된 읽기 전용 GitHub 응답에 대한 오프라인 검사다. 재현 시 자동 fetch나 최신 브랜치 해석은 하지 않는다.

## 전달할 때 유지할 한정

작성 측 487/491/495, 3.8, e2e51, 전체 변이 수는 받은 로그 재집계이며 이번 새 실행 횟수가 아니다.
이번 판정은 지정11항목의 한정 닫힘 + 새 RR4-01 P3 + PC14-02/03 열림 및 전체 재개 정책 HOLD다.
현장 자격·실침대·봉인·등록/캠페인 실행·배포·통합·운영 원장 종결은 미승인이다.

