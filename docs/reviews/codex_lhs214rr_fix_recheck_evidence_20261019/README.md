# LHS214 재확인 반례 수정 검토 전달 묶음

먼저 `codex_review_lhs214rr_fix_recheck_20261019.md`를 읽으세요. 기존 수치 P2는 닫힘, R02/R04 닫힘, R03은 공백 반례 때문에 부분입니다. 새 214 발사 승인은 아닙니다.

## 대상과 보존

- 핀 `77d8fd44545c33cd10ab18fc250c7ad3023833ea`.
- 비교 `60ba39e224aff48a030dccfe750342f3bf9db61f`; A4 기준 `6cb2569569ec74b7f5a96e0ef19494e872da5272`.
- source/는 원격 blob 및 SHA256으로 확인한 실행용 스냅샷이며 Git checkout이 아닙니다.
- submitted/는 받은 요청서, evidence/는 제출 증거 대조와 새 계산·렌더링 결과, probes/는 독립 실행기, notes/는 분야별 세부 검토입니다.
- 보존 manifest는 전달 동일성 증거이며 판정의 무오류 인증이 아닙니다. 생산 파일과 원 등록·과거 검토 폴더는 수정하지 않았습니다.

## 실행 환경

Windows / Python 3.12.14 / NumPy 2.5.3 / SciPy 1.16.3. OMP·OpenBLAS·MKL·NumExpr 스레드 수 1, UTF-8, bytecode 비활성화. 제출 Linux/Python3.11과 다르며 이 차이가 R01 실 사슬 경계 fixture에 드러났습니다.

기본 Python은 `C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`입니다. 기존 두 의존성 폴더 `../lhs_coverage_review_20260930/deps`, `../gen2_network_reverify3_20261007/deps`를 사용했습니다. CommonMark 대조용 markdown-it-py 3.0.0 / mdurl 0.1.2만 이번 검토의 deps/에 설치했습니다. 라이브러리는 ZIP에 포함하지 않습니다.

## 재현

아래는 이 작업 공간의 경로 관계를 전제로 합니다. 재실행은 새 작업 사본에서 하세요. 과거 검토 폴더를 읽는 탐침의 원 바이트·경로 어댑터를 보존했으므로 **독립 실행용 설치 패키지**라고 부르지 않습니다. 다른 기계에서는 같은 고정 스냅샷·과거 증거 경로와 의존성을 공급해야 합니다. 생산 코드의 판정 함수를 고쳐 실행하지 마세요.

```powershell
$py = 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$r = 'C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs214rr_recheck_20261019'
& $py -X utf8 -B "$r/probes/root_audit.py" metadata
& $py -X utf8 -B "$r/probes/root_audit.py" a4
& $py -X utf8 -B "$r/probes/root_audit.py" receipt_tests
& $py -X utf8 -B "$r/probes/root_audit.py" fences
& $py -X utf8 -B "$r/probes/root_audit.py" regressions
& $py -X utf8 -B "$r/probes/rr_numeric_independent.py"
& $py -X utf8 -B "$r/probes/rr_numeric_chain_boundary.py"
& $py -X utf8 -B "$r/probes/rr_numeric_scope.py"
& $py -X utf8 -B "$r/probes/rr_consumers_run.py" chain
& $py -X utf8 -B "$r/probes/rr_consumers_run.py" resurrection
& $py -X utf8 -B "$r/probes/rr_consumers_run.py" baseline
& $py -X utf8 -B "$r/probes/rr_consumers_independent.py"
& $py -X utf8 -B "$r/probes/rr_consumers_check_gate.py"
& $py -X utf8 -B "$r/probes/rr_display_run.py" extended_source probes/rr_display_extended.py source
& $py -X utf8 -B "$r/probes/rr_display_run.py" extended_old probes/rr_display_extended.py old
```

root_audit a4의 자료 공급 어댑터는 Git show/archive 대신 보존된 기준 스냅샷을 읽습니다. 영수증 selftest 어댑터는 격리 Python에 설치된 의존성 경로만 공급합니다. 화면·소비자·수치 파생 탐침별 정확한 치환과 원 SHA는 evidence/와 notes/에 있습니다.

R01 제출 시험의 rc1, 화면 확장 탐침의 null 입력 HTTP500, 옛 복원 탐침의 P4 예외는 삭제하지 않았습니다. 각각 시험 전제 실패, UI 반례, 수정 후 의도된 거부를 의미하므로 단순히 모든 종료코드가 0이어야 한다고 집계하면 안 됩니다.

패키지에는 초기 탐침 초안 결과도 일부 남습니다. 최종 권위 파일: `rr_display_extended_source.json`, `rr_display_extended_old.json`, `rr_display_summary.json`; 120사례 초기 `rr_display_extended.json` 대신 128사례 최종 결과를 사용하세요.
