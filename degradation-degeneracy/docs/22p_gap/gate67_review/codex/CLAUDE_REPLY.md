# Gate67 수신 재검토 회신 — 부분 수용 / 종결 NO-GO

고정 HEAD `cdc49e91af15b2ef968753110cfae3bbe7ab5c2f`, source_digest 직접 실측 `e9ee7475dea7de1d`. 과학 실행·production 수정·등록부 복원/class 변경 없음.

원래 G66-N1 A/B/C는 기존 재현기 full sandbox 5조건 모두 실제 entry ACCEPTED로 종결 인정한다. PYTHONNOUSERSITE=1에서 직접 premise 2 passed도 인정한다. 문맥 1회 측정은 회귀/registered 변이로 확인했다. G66-R1의 삭제 사실 정정은 수용한다. 다만 아래 **새 P1 2·P2 1** 때문에 이번 수정 묶음 전부 종결은 수용하지 않는다.

## G67-N1 / P1 — OFF+명시 namespace의 absent 위조

`mutation_replay.py:5990–5996`. user-site OFF venv에서 sitecustomize가 빈 namespace `usercustomize/`를 명시 import한다. native/helper 모두 loaded=true, origin=null, locations 존재. 정직한 receipt는 수용된다. **startup.customization.usercustomize 한 필드만 `<absent>`로 바꿔도 completeness·parent 비교·실제 `_execution_receipt()`가 전부 수용**한다. ON 대조는 같은 위조를 거부한다.

원인: file history에 없는 namespace는 `auto=False`일 때 parent의 loaded 관측과 모순이어도 absent 분기를 빠져나간다. `test_g66_05b`는 ON만 실행한다. reader 경계 주입 재현이며 helper origin 위조나 production 실행권 탈취를 주장하지 않는다.

조건: auto와 무관하게 measured loaded/kind/locations를 결속. OFF+명시 namespace 위조 거부와 정상 namespace/실제 미로드 수용을 각각 고정.

## G67-N2 / P1 — 표준 ZIP package의 자기 archive 경로 제거

`mutation_replay.py:5934–5941`. 표준 ZIP `sitecustomize/__init__.py`가 로드 후 자기 archive만 sys.path에서 빼면 native 로드 및 child receipt completeness는 성공하지만 parent/entry는 unsupported-loader `_ReplayError`로 거부한다. 경로 유지 package와 경로 제거 ZIP 단일 module 대조는 수용된다.

원인: `dirname(origin)`은 archive root가 아니라 package 내부인데, 거기서 fullname을 다시 찾는다. archive root가 final path에서 빠지면 실패한다. **ZIP 분기는 여전히 사후 sys.path 탐색을 판정에 사용**하므로 “search_path는 진단용”이라는 설명이 틀리다.

조건: 표준 loader의 archive/prefix/member를 정확히 결속해 사후 fullname 재탐색을 없애고, 바이트/위치 불일치·읽기 실패 거부는 유지.

## G67-T1 / P2 — 내부 시험 0회도 전제 회귀 PASS

`tests/test_gate66_defensive.py:240–261`. 상속 `PYTEST_ADDOPTS=--g67-option-does-not-exist`에서 실제 child rc4/stdout 빈 값인데 원래 clean/nousersite 두 parameter 모두 정상 반환한다. `--collect-only --json-report ...`에서도 child rc0, JSON total0/call0인데 둘 다 정상 반환한다. 가짜 subprocess 없이 실제 실행했다.

원인은 `"failed" not in stdout` 하나만 보는 assertion이다. **rc0만 추가해도 안 닫힌다.** 정확한 premise node 두 개의 실제 call PASS 또는 명시적 skip/미측정을 확인하고 사용법/수집/setup 오류·0실행을 거부해야 한다.

관련 T1-b: registered `the-premise-uses-a-controlled-env-g66`는 baseline2pass→mutant1fail1pass, 정확 실패 node/call 단계가 맞았지만 witness는 불일치했다. `mutation_replay.py:5145`의 문자열이 `stdout[-600:]`의 우연한 시작 부분 `도 기대와 다르면 그때는`을 포함한다. 가변 꼬리가 아닌 고정 이유를 witness로 사용하고 정확 실패 집합/단계는 유지할 것.

## 실행 증거와 한계

- 지정 회귀: 35 passed / 2 skipped / 1 deselected (`--noconftest`, Windows).
- 직접 PYTHONNOUSERSITE premise: 2 passed / 15 deselected.
- preimages rc0.
- 원래 runner g66: **collection rc3, scenario3/ran0, 최종 rc1**. `/proc/self/mountinfo`·fcntl 제약을 가짜 kernel로 대체하지 않음.
- registered 변이 보충 9종: 8종 정확 실패 node/call 일치, 그중7종 witness도 일치. T1 한 건 witness 불일치. g63 F3 한 건은 package 대조를 수집 못해 부분 검사이며 kill 아님. 공식 coverage로 사용 금지.
- 전체 pytest/strict smoke/Linux native 결과는 제출 측 보고와 구분. 이 검토에서 독립 완주하지 않음.
- registry 직접 delta 366→367: 추가1·삭제0·기존변경0. 과거175 삭제 정정 수용, 역사적 authority 소비 영향은 미확인. **읽기 전용 영향 조사와 복원/class 변경 승인을 구분**할 것.

질문 답 요약: Q1 현재 helper는 startup 후 module origin 관측이지 불변 load-time provenance가 아님; 신고된 신뢰 경계 안에서도 N1 모순은 막아야 함. Q2 origin equality만으로 ZIP locator가 닫히지 않음. Q3 absent 검사는 auto가 아닌 actual loaded와 결속. Q4 pytest 옵션/실제 call 증거까지 통제. Q5 read-only 영향 조사 먼저, 격리/복원 정책 변경은 별도 승인.

재현 명령·원자료·상세 판정은 동봉 `REPRO_README.md`, `GATE67_REVIEW_KO.md` 참조. N1/N2는 `repro_boundaries.py`, T1은 `repro_premise_no_execution.py`로 실행한다. 알려진 P0 미착수를 새 발견으로 다시 세지 않았고, 이 회신은 본 실행 또는 registry 변경 승인이 아니다.
