# Gate66 회신 — 부분 수용 / NO-GO

고정 HEAD `fa947cc9b17cdbeffbb39447c99159bc2c831e6e`, RUN_SCOPE 정본 `743f65bead671bf353ce38027c2e8e457738ec08`, source_digest 직접 계산 `e9ee7475dea7de1d`. 과학 코드 identity 일치. 본 실행은 이번 판정 대상/승인에 포함하지 않았다.

기존 N1a 명시 import, N1b 상대 cwd, N2b namespace 원 반례의 수정은 수용한다. G65+64 선택 시험은 Windows CPython 3.12.14에서 --noconftest로 24 passed / 2 skipped / 1 deselected. 별도 sandbox의 등록 변이 N1a/N1b/N2b/T1 네 축은 선언한 실패 node 집합·call 단계·witness가 각각 일치했다. 이것은 원래 runner의 Linux replay/coverage 인증이 아니다.

새 반례/증거 문제는 세 항목이다.

## G66-N1 / P1 — post-startup resolver 후보는 실제 startup origin이 아니다

mutation_replay.py:5720,5821,5875. `_replay_context`는 startup 완료 뒤의 sys.path를 주고 parent는 거기서 다시 find_spec한다.

실제 `_make_sandbox()` 전체 복사본과 수정하지 않은 `_execution_receipt()`로:

1. replay cwd에 주석만 있는 sitecustomize.py, PYTHONPATH는 다른 빈 디렉터리, PYTHONNOUSERSITE=1. native `python -c`는 모듈 미로드, 완전한 receipt는 absent인데 parent는 뒤늦게 추가된 cwd 후보를 찾아 REJECTED한다. cwd를 명시적으로 PYTHONPATH에 넣은 대조군은 실제 로드되고 ACCEPTED.
2. PYTHONPATH의 sitecustomize가 정상 import된 뒤 자기 디렉터리만 sys.path에서 제거. 파일·sys.modules 불변. child `714392a77b46c917` / parent absent, 완전성 통과 후 REJECTED.
3. 다른 후보를 경로 앞에 추가하는 변형도 축소 sandbox에서 같은 형태로 거부. 셋은 한 root cause이며 새 P1 하나로 센다.

재현기 `repro_startup.py --repo <subtree> --out <new-dir> --full-sandbox --case plain --case cwd_only_candidate --case cwd_on_pythonpath --case remove_loaded_path`. native 관측과 raw receipt를 함께 저장한다. 시스템 sitecustomize가 있으면 cwd-only 반례가 가려질 수 있으므로 그 통제도 확인할 것.

최소 조건: import 시점·실제 origin/loader·parent byte 검증을 연결하고 최종 후보를 과거 import 증명으로 쓰지 말 것. 기존 changed bytes/위조 absent/origin 없는 module 거부는 유지. 단순 mismatch 허용은 안 된다. ctx=None 경로가 보조 문맥을 두 번 만드는 자리도 정리할 것(별도 finding으로 세지 않음).

## G66-T1 / P2 — 새 전제 시험이 PYTHONNOUSERSITE에 다시 가려짐

tests/test_gate65_defensive.py:95–101은 make_interpreter의 skip을 우회하고 build_interpreter→measurement→assert를 한다. subprocess 환경은 외부 것을 물려받는다.

PYTHONNOUSERSITE=1로 해당 parametrized test를 실행하면 **1 failed / 1 passed**, True 판 `assert False is True`. 변수 없는 대조군 둘은 통과. “전제를 못 만들면 skip” 설명과 다르다.

최소 조건: 생성/측정의 환경을 명시적으로 같게 만들고 외부 비활성과 fixture의 활성 옵션 누락을 구분할 것. True 옵션 삭제 변이는 여전히 실패해야 하며 skip으로 숨기지 말 것.

## G66-R1 / P2 — 이전 리뷰부터 기존 sealed 175건이 실제 삭제됨

git 객체 직접 대조: 5e4cf103… tracked541 → fa947cc9… tracked366. 추가0/생존 JSON 변경0, 삭제175 전부 sealed=true/canonical. fixture87 + leg=L grid88.

삭제 커밋 `d60f25391f9e7a08c210ef559efa0d58589171be`(제목은 BMS R17 대응). Gate66 작업자가 직접 삭제했는지/별도 승인 여부는 단정하지 않는다. 그러나 대상 HEAD에 이 삭제가 있으며 요청문 §2-6의 “기존 sealed 기록 하나도 건드리지 않음”은 이전 리뷰부터의 보존 설명이 될 수 없다.

이번 세션의 새 미추적175건 정리와 이전 커밋의 tracked175건 삭제는 별개다. 기존 격리 미착수를 새 발견으로 센 게 아니다. `registry-audit.json`에 삭제 전체 명부와 이전 record/해시가 있다. 최소 조건은 원장에 기준 SHA·삭제 명부·처리 근거/승인 및 권한 영향의 확인 범위를 기록하는 것. 자동 복원·삭제·class 변경을 승인하지 않는다.

## 질문 답과 미측정

- Q1: 후보/이력의 **시점과 origin 연결**이 빠졌다. 손자 sys.modules라는 인터페이스로 바꾸는 것만으로 종결되지 않는다.
- Q2: builtin/frozen을 명시적 미지원으로 거부하는 정책은 수용 가능. 모든 정상 배포판에 그런 origin이 없다는 보증은 하지 않음.
- Q3: 빈 namespace 객체의 종류/검색 위치 식별에는 현재 방식 수용. 하위 모듈의 실행 bytes까지 무관하다는 확대는 불가. 디렉터리 전체 목록을 이 좁은 수정의 필수조건으로 추가하지 않음.
- Q4: 고정 환경 on/off native 결과는 최소 증거로 인정. 여기서도 확인. 별도로 G66-T1 환경 행렬을 닫을 것.
- Q6 F50b: 다음 RUN_SCOPE 변경에 묶는 (b) 권고, 그동안 같은 commit에서 resume하는 제약 명시. 최초 start와 최신 attempt 전체 대조의 의미는 실행중 코드 불변과 다르다. git_commit을 무조건 삭제하는 수정은 승인하지 않음. doc-only resume 대조와 source/input/env/recipe 변경 거부를 함께 시험할 것.
- Q7 E2-R: 공유 predicate + 같은 live token의 False + 상수True 대조 구조는 수용. lifecycle 중간 lock을 일부러 해제할 필요 없음. 이 PC에서는 native Linux 미실행.

원래 conftest 수집은 /proc/self/mountinfo 부재로 rc3. 원래 `-k g65 --keep-sandbox`는 rc1, scenario5/ran0. 보조 E2-R 변이는 정적 검사2 실패·native1 skip이므로 full EXPECT 일치로 세지 않았다. full pytest/strict smoke/원래 Linux mutation/실제 planned lifecycle 완료 주장 없음.

G66-N1/T1/R1 대응 및 고정 HEAD의 Linux token/control·원래 g64/g65 재생 출력을 받아 재심한다. §0 기존 독립 GO 전제는 그대로. 생산 코드를 이 리뷰에서 수정하지 않았다.
