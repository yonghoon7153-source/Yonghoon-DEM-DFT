# LHS214 SHA 형식 재확인 증거

판정은 `codex_review_lhs214_pin_syntax_20261028.md`에서 읽는다. 이 ZIP은 독립 검토 자료이며 실행용 214 배치 또는 완전한 Git checkout이 아니다. 실제 발사 명령은 포함하지 않는다.

## 재현

압축을 새 폴더에 풀어 원본 증거를 보존한 뒤, 해당 폴더에서 실행한다. NumPy·SciPy·networkx가 설치된 Python이 필요하다. 이번 독립 검토 환경은 Python 3.12.14 / NumPy 2.5.3 / SciPy 1.16.3 / networkx 3.7이었다. WSL 원 실행의 환경은 `wsl/.../env.txt`에서 별도로 확인한다.

```text
python -I -X utf8 -B probe_receipts.py
python -I -X utf8 -B probe_launch_contract.py
python -I -X utf8 -B run_canonical_complete_env.py
python -I -X utf8 -B audit_delivery.py
```

각 명령은 자기 위치를 기준으로 `repo/`, `before/`, `wsl/`를 읽는다. 새 폴더에서도 Git fetch·checkout·WSL·DEM 계산은 필요 없다. `repo/`는 필요한 고정 소스와 입력 자료만 담은 부분 스냅샷이다. 경계 시험 wrapper는 작업 폴더의 `tmp/`를 사용한다. `canonical_boundary_complete_env/`와 `independent/`의 출력은 재실행 시 갱신되므로 원 증거 ZIP을 보존한다.

기대 결과:

- `receipt_probe.json`: 실제 두 영수증의 P0–P10 정상, 120개 기대 결과 일치, 수정 전 LF 반례 재현.
- `launch_contract_probe.json`: 15개 기대 결과 일치. 승인값 없는 두 manifest의 동시 LF가 통과하는 기존 경계도 결과에 포함됨.
- `canonical_boundary_complete_env/summary.json`: boundary_cases 6, failed_boundaries [], receipt_selftest_rc 0, 123/123 PASS, test_rc 0.
- `supp20_reverified.json`: 실제 보충 영수증 전체 24칸, rc 0.

## 출처 구분

`input/`는 사용자 첨부 원본 4개, `wsl/`는 그 TGZ의 안전하게 푼 원문이다. `repo/`의 source는 리뷰 핀 b7a979032...이며 관련 파일의 실제 WSL 핀 35f032737... 동일성은 `b7_to_35_identity.json`과 `registration_pin_identity.json`에 기록했다. `before/`는 수정 전 runner만 담았다.

`independent/*_relocated.json`은 원 영수증에서 log.path만 로컬의 원 로그 파일로 연결한 사본이다. 원문은 `wsl/`에 그대로 있다. 현재 컴퓨터에서 원 WSL raw dump를 재측정한 증거는 아니다.

`canonical_boundary_run/` 및 `canonical_boundary_workspace_tmp/`는 의존성·역사 fixture 준비 전 실패한 검토 실행 기록이다. 최종 판정 근거는 `canonical_boundary_complete_env/`다. `launch_contract_probe_initial_fixture_error.json`은 검토용 두 manifest를 같은 ROOT에 두어 H1에 걸렸던 최초 fixture를 설명한다. 정상 두 ROOT를 분리한 뒤 통과한 자료가 별도로 있다.

`context/`의 실행표는 고정 WSL 핀 이후의 문서 맥락이다. 이를 그 핀의 파일인 것처럼 쓰지 않는다. GitHub 비교의 300파일 제한 때문에 전체 diff 응답만으로 동일성을 판단하지 않았다. `trees/`와 Git blob 재계산 자료가 관련 파일의 근거다.

기존 전체 게이트 155 PASS 기록은 과거 후보에 대한 기록이다. 이번 독립 검토에서 전체 check_all을 다시 실행하지 않았다. 첨부 WSL 자체시험 출력과 이번 로컬 123개 자체시험 결과도 구별한다.

`MANIFEST.sha256`는 배포 파일들의 SHA-256 목록이다. ZIP 제작 뒤 모든 entry를 다시 읽어 이 목록과 대조했다. 이 검증은 포장 바이트 보존에 대한 것이며 물리 실행 승인은 아니다.
