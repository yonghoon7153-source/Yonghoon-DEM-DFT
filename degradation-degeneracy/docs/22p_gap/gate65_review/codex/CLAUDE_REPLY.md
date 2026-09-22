# Gate65 수신 리뷰 회신 — 전부 종결 불수용 / 부분 수용

리뷰 HEAD `5e4cf1038f0f26a6a624d9984386cfd046657ac3` 고정.
과학 코드 `743f65bead671bf353ce38027c2e8e457738ec08` / source_digest `e9ee7475dea7de1d` 실측 일치.
RUN_SCOPE log/diff 빈 출력. 증거층 파일 SHA는 동봉 FINAL_AUDIT.json에 별도로 고정했다.
이 판정은 N1·N2·E2-R 대응 검토이며 본 실행 GO가 아니다.

새 확인: **P1 3건·P2 1건**. 이미 신고한 §0 GO 전제와 registry 오염은 새 발견으로 세지 않았다.

## G65-N1a / P1

mutation_replay.py:5668–5673. `ENABLE_USER_SITE=False`인 정상 venv에서 sitecustomize가 `import usercustomize`를 명시적으로 수행하면 실제 로드는 성공한다. `VALUE=42` 파일의 child digest는 `1cfeb13a2258c8d8`지만 부모는 `<absent>`로 덮는다.

원래 ROOT·replay_env·`_execution_receipt()`에서 `receipt_complete=true` 뒤 `_ReplayError`로 거부됐다. 자동 import 비활성은 명시 import 금지가 아니다. 비활성 미로드/비활성 명시 로드/활성 자동 로드를 구분하고 바이트 변경 거부까지 시험해 달라.

## G65-N1b / P1

mutation_replay.py:5578,5654–5656. 호출 cwd에만 `startup/sitecustomize.py`를 두고 `PYTHONPATH=startup`으로 호출하면 child는 실제 ROOT에서 `<absent>`, 부모는 호출 cwd의 `2e252a13409dfd33`을 기대한다. 완전한 정상 receipt를 실제 `_execution_receipt()`가 거부했다. 호출 cwd를 ROOT에 두고 upstream runner의 실제 sandbox 및 ROOT 밖 상대 PYTHONPATH를 사용해도 같은 거부를 재현했다. 저장소 안에서 실행하라는 안내만으로는 닫히지 않는다.

같은 실행파일·같은 env 문자열만으로는 같은 경로 문맥이 아니다. cwd/argv/env/검색 경로를 하나의 replay context로 고정하고 부모 pytest의 sys.path를 child의 경로로 가정하지 말아 달라.

위 두 건: `repro_real_entry.py --repo <고정 DD 절대 경로> --out <새 디렉터리>`를 기본 venv Python으로 실행하면 재현된다. 생산 함수·ROOT·replay_env를 monkeypatch하지 않는다.

## G65-N2b / P1

mutation_replay.py:5229,5346–5350. PYTHONPATH 아래 `sitecustomize/` 빈 디렉터리(표준 namespace package, __init__.py 없음)는 정상 import지만 __file__이 None이다. customization을 absent로 접은 뒤 -v의 성공 기록과 모순이라며 startup_history=failed로 거부한다.

`repro_namespace.py`는 원본 probe 본문과 완전성 검사로 재현한다. Windows cp949 진단 출력 오류와 분리하기 위해 JSON 전송만 ensure_ascii=True로 했다. 원래 frame 경로의 native 성공으로 포장하지 않는다. 실제 미로드/namespace/파일·ZIP/읽기 실패를 구분해 달라. 기존 ZIP 반례 자체는 닫힌 것을 인정한다.

## G65-T1 / P2

test_gate64_defensive.py:105–127의 활성 대조군은 환경변수만 지울 뿐 venv에서 user site를 활성화하지 않는다.

- 활성 환경: 9 passed, 1 deselected.
- 일반 비활성 venv: 1 failed, 8 passed, 1 deselected. line122 child='<absent>'.

활성/비활성 interpreter fixture를 명시적으로 만들고 실제 조건을 확인해 달라. 활성 assertion 삭제나 모든 환경 skip은 대체 증거가 아니다.

## E2-R / 실행 미확인 및 후속 사항

새 path 탐침의 음성 assertion은 확인했다. 파일 열기 실패를 False로 삼키지도 않는다. 다만 actual planned lifecycle은 token 함수 `_kernel_lock_held`를 쓰고 음성은 별도 `_kernel_lock_held_at`이다. token 함수의 상수 True 변이까지 검출하는지는 아직 입증되지 않았다.

`repro_e2_linux_NOT_RUN.py`는 Linux 후속용이며 이번 Windows에서 미실행이다. 실제 token을 쥔 채 flock만 해제해 같은 token/inode의 False를 확인하고, token helper 상수 True에서 커밋된 대조군이 실패하는지 확인해 달라. 아직 실행한 새 발견으로 세지 않았다.

## 실측과 환경 한계

`--check-preimages`: rc0, 133.594초.
`-k g64 --keep-sandbox`: rc1, scenario3, **ran0**. collection rc3의 원인은 conftest frozen seal bootstrap이 `/proc/self/mountinfo`를 읽지 못한 것. fcntl 직접 시험도 import 실패였다. Windows stdout cp949/부모UTF8 불일치는 원시 바이트 진단으로 분리했다. WSL 접근 거부는 우회하지 않았다.

선택된 9건은 --noconftest로 실행한 한정 검증이다. 전체 pytest·strict smoke·변이 전수·evidence_layer_58·실제 planned lifecycle의 통과를 독립 확인했다고 쓰지 않는다. 요청문의 전체 pytest 칸은 여전히 실행 중이다.

## 추가 신고⑩ 답변

현재 고정 HEAD root registry는 **541개**이며 evidence 문자열상 합성 fixture261, leg=L phase=grid264, re-key/legacy16이다. 191/366 또는 전부 동일 fixture라는 설명을 현재 실측으로 재사용하지 말아 달라. 이 분류도 provenance 검증은 아니다.

필요한 것은 운영 authority와 테스트 authority의 구조적 격리다. 임시 원장/registry를 모든 시험·자식에 주입하고 production registry 불변을 검사하라. 격리된 테스트 canonical positive fixture는 유지할 수 있지만 그것이 운영 canonical 권한을 얻으면 안 된다. local/·gitignore만으로 닫지 않는다. 기존 오염은 증거 목록 고정 후 reader가 반영하는 append-only revocation/supersession/epoch 절차를 별도 계약으로 설계하라. 이번 리뷰에서 삭제·소급 수정은 하지 않았다.

상세 근거·최소 조건·유효/무효 진단 구분은 GATE65_REVIEW_KO.md와 재현 묶음에 있다. **이번 방어층 전부 종결은 NO-GO, 기존 특정 수정은 부분 수용. 본 실행 승인은 별개다.**
