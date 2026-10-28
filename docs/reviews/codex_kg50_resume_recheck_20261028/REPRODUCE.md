# KG50 재개 재검토 — 재현 안내

검토 핀: `f118c1fd1e3eb1a558299663dcee6a0bf83b9942`.

판정문: `codex_review_kg50_resume_recheck_20261028.md`.

`repo/`는 수령 ZIP의 42개 파일이다. 생산 코드는 변경하지 않았다. `PIN.txt`, `intake.json`, `remote_identity.json`이 신원을 기록한다. `PACKAGE_MANIFEST.sha256`은 이 리뷰 묶음의 무결성 목록이다.

## 실제 실행한 독립 탐침

ZIP 루트에서 Python 3으로 실행한다. 표준 라이브러리만 필요하다.

```bash
python3 -B independent/deck/reproduce_deck.py
python3 -B independent/scheduler/probe_trial_steps.py
python3 -B independent/scope/probe_state_observability.py
```

- 첫 도구는 고정 SHA를 확인한 뒤 `resume_ckpt.sh`의 내장 Python을 변경 없이 추출해 CLI로 호출한다. 24개 관측의 정본은 `independent/deck/results.json`이다.
- 두 번째는 계속 줄 run 사례의 생산 `check`/`trial_steps`를 실행한다. raw awk 절단의 전사는 제한된 fixture용이며 실제 awk 실행과 구분한다.
- 세 번째는 같은 KE가 같은 입자 상태를 식별하지 못하는 합성 산술이다.
- 위 작업은 `independent/`의 생성 fixture·결과를 덮어쓴다. `repo/`에는 쓰지 않는다. DEM, MPI, 원격 scheduler를 실행하지 않는다.
- false-green 반례에서는 제품 검사의 rc=0이 **결함 재현**이다. 이를 수정된 제품의 PASS로 읽지 않는다.

## 이 환경에서 실행하지 못한 것

Windows Git Bash가 `NtCreateDirectoryObject ... 0xC0000022`로 시작 전에 종료됐다. GNU awk와 전체 fake-SLURM 경로, 저자 87개 전체 시험을 독립 실행했다고 주장하지 않는다.

Bash가 동작하는 Linux의 별도 리뷰 폴더에서만:

```bash
# 자체 생성한 가짜 sbatch/sacct/squeue/sleep만 PATH 앞에 둠
python3 -B independent/scheduler/probe_stale_trial.py
# 저자의 기존 가짜 scheduler 시험
python3 -B repo/scripts/test_resume_ckpt.py
```

실제 `sbatch`, LIGGGHTS 또는 ibb 접근 명령은 이 안내에 없다. 원문 `resume_ckpt.sh`를 실제 작업 폴더에서 직접 실행하는 것은 본 리뷰의 재현 절차가 아니다.

`independent/scheduler/stale_trial_results.json`의 상태는 **NOT_EXECUTED_BASH_RUNTIME_BLOCKED**다. 새 환경에서 재현하면 새 결과와 함께 실행 환경을 기록할 것. 기존 실패 환경 기록을 성공 기록으로 전용하지 않는다.

## 파일 구분

- 최종 판단은 루트 판정문이 우선이다.
- `independent/*/*.md`는 세부 검토 메모다. 해당 영역의 임시 ID(DECK/SCHED)는 최종 `KG50R-*` 번호와 다르다.
- `independent/deck/initial_results.json`, `more_results.json`은 초기 탐색 기록이다. 최종 집계에는 `results.json`을 사용한다.
- `scope/peer_every_result.json`은 별도 최소 fixture를 통한 교차검토다.
- 현재 snapshot의 실제 실행·Q5 dt/감쇠 자격·물리적 GO는 이 묶음이 생성하지 않는다.
