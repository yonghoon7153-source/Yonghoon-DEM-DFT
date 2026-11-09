# 회차⑤ 독립 검토 증거 재현

검토 핀 abf0911ebc994167ac50132c78207c6c8d4421f1. 문서·합성·제공 원자료 읽기 범위다.
실제 연구 실행, S0 재계산, σ 풀이, ibb/WSL, MPI, 등록/배포/통합은 하지 않는다.

## 내용

- codex_review_rint2_rr_round5_20261109.md: 통합 판정
- inputs/: 원 회차⑤ ZIP, 후속 원 S0 TGZ, 사용자 전달문(바이트 보존)
- input_verification.json, remote/: 포장807 및 원격 blob806 대조
- baseline/repo/scripts/: 이전 회차④ 전달본에서 읽은 비교 소스28개. Git worktree를 변경하지 않음
- root_audit/: M56, 상주 RR4C, 원로그 변이회계, 생산자 동일성
- resume_agent/: 실제 함수·원 탐침·기대만 변경한 탐침, summaryless 경계
- s0_agent/: 원자료/NPZ 읽기, importer 7소형 입력과 결과
- smin_agent/: 실제 registry 고정 최소 반례와 발견 과정
- SHA256SUMS: 이 증거 묶음의 모든 파일(자기 자신 제외)

큰 scratch Git 폴더·중복 frozen 입력 복제·__pycache__는 넣지 않았다. 스크립트가 새 scratch를 만든다.
원 리뷰 ZIP 안의 806개 repo파일은 inputs의 원 ZIP에 보존했다. 다음 검증기로 안전한 상대 경로/CRC/해시를 검사한 뒤 package/repo로 복원한다.

## 포장·신원

~~~bash
python -I -B -X utf8 verify_input.py --zip inputs/codex_rint2_rr_round5_abf0911ebc99.zip
python -I -B -X utf8 audit_root.py
~~~

audit_root.py는 저장한 원격 tree 응답으로 806 blob을 다시 대조하고 baseline 소스 및 M56을 검사한다.
원격 응답을 새로 받는 명령이 아니며 네트워크 요청이 없다. 응답은 검토 당시 GitHub 커넥터로 읽은 고정핀 tree다.
원격을 별도로 재검증하려면 이 핀의 tree661308db21702ab3b344d9ad85194467336ec260과 비교하면 된다.

## 후보 리포에서 최소 반례

아래 REPO는 고정 핀의 repo 경로다. 새 빈 디렉터리에서 실행한다.
Python, NumPy, SciPy와 Git이 필요하다. 원 CLI 탐침은 Git의 가짜 로컬 원장만 사용한다.

~~~bash
python -I -B -X utf8 resume_agent/probe_resume_focus.py /path/to/REPO
python -I -B -X utf8 resume_agent/probe_summaryless_copy.py /path/to/REPO
python -I -B -X utf8 smin_agent/reproduce_smin_counterexample.py --repo /path/to/REPO --out fixed.json
python -I -B -X utf8 s0_agent/audit_s0_raw.py --repo /path/to/REPO --raw inputs/s0fix_1106_done.tgz
python -I -B -X utf8 s0_agent/probe_import_rc.py --repo /path/to/REPO --out /path/to/new-parser-output
~~~

S0 명령은 tar/NPZ 원자료만 읽는다. 연구 함수나 solver를 호출하지 않는다.
parser 출력 경로는 존재하지 않는 새 경로여야 한다.

원 회차④ 탐침의 재실행:
~~~powershell
$env:RINT_REVIEW_REPO='C:/path/to/REPO'
python -I -B -X utf8 resume_agent/original_probe/probe_resume_independent.py
# 위 무수정본은 옛 false-green 단언181행에서 실패하는 것이 기대됨.
python -I -B -X utf8 resume_agent/expectation_adjusted/probe_resume_independent.py
~~~

Linux에서는 export RINT_REVIEW_REPO=/path/to/REPO로 바꾸면 된다.
원 탐침의 내장 pin은 역사값 그대로다. 실제 실행 소스는 환경변수와 결과의 source SHA로 확인한다.
expectation_only.diff는 입력/변조/호출을 그대로 둔 단언 변경이다.

## 플랫폼·관측수 한정

검토자는 Windows Python3.12.14에서 실행했다. 일반 파일 O_NONBLOCK=0 호환, 가짜 실행기, 직렬 lock 대체,
죽은 부모 모의 등은 각 probe의 docstring/판정문에 명시했다. 실제 POSIX·Linux·현장 시스템 자격이 아니다.
작성측 Linux3.8/3.11 506개 전체사슬·51끝-끝·71전수변이는 이번 독립 실행 수에 합산하지 않는다.

동일 사례를 원형/기대변경/집중경로로 반복했으므로 파일행수·함수호출수를 고유시험 총합으로 쓰지 않는다.
M56 후보/변이, S0의18파일/6산출물/8사본/7코드는 서로 중첩되는 확인 단위다.

## 검토 도구 실패 이력

- 최초 추출: Windows 긴 경로에서 FileNotFoundError. 확장 경로 접두사를 사용해 동일 ZIP 바이트를 복원.
- 최초 remote 비교 one-liner: 기본 cp949 읽기에서 UnicodeDecodeError. UTF-8 명시 후 대조.
- 최초 재개 API: Windows에 os.O_NONBLOCK 상수가 없어 실패. 일반 파일 호환만 넣고 다시 실행; POSIX 인증 없음.
- 최초 S0 audit: 모든 배열의 첫 축이 같다는 검토기 단언이 sub_*에서 실패. 주행/부분간선/섬유집계 축을 구분.
  원형과 실패 메모를 s0_agent에 보존.
- 원 회차④ 탐침181행 AssertionError는 환경 오류가 아니라 이전 false-green 기대가 뒤집힌 관측이다.

이 실패들은 입력/생산 코드 수정의 근거가 아니며 성공 시험 수로 세지 않았다.
원 자료·고정repo·사용자 작업 트리·원장은 변경하지 않았다.

## 수용 경계

지정 결속 수정 및 이번 SBE 단계1 채택은 한정 수용. Q6 전칭은 불수용.
RR5-01(P2)은 s_min 영향 범위/동등성 설명의 수정 요청이다. s_min=0 자체를 기각하지 않는다.
전체 HOLD, S0 단계2·R런·실제 실행/배포 GO 없음.

