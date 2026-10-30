# D0.7-50 한 건 범위 검토 전달본

- 판정: `codex_review_kg50_d07_scoped_go_20261030.md`.
- 고정 핀: `09ae533d05f6f165c9754ff4edd42cd97c7c3c06`.
- 범위: 제공된 D0.7-50 정착 재개. 수동 영수증 대조·Q6 중단을 적용하는 한 건 GO.
- 일반 도구 종결, 후속 물리 자격, 본 제출 실행 증거로 확대하지 않는다.
- 추가 받은 원 로그를 포함한다. 서버 원본↔도구 사본 cmp는 미수령이다.

## 재현

압축을 풀고 `evidence/`에서:

```bash
python3 -I -B reproduce.py
```

결과 55/55. 표준 라이브러리만 사용한다. 원본은 읽고, `independent/`에 재계산 파일을 쓴다.
LIGGGHTS·MPI·SLURM·WSL·원격 제출은 호출하지 않는다. Git blob/manifest는 현재 파일에서 다시 계산하여 수령한 원격 핀 메타데이터와 대조한다.

## 증거 구분

- `evidence/repo/`: 원격 핀과 대조한 원본 15개.
- `evidence/trial/`: 실제 -T 로그·덱·러너·영수증 사본.
- `evidence/input/kg50_d07_b50_ins1_log.liggghts`: 후속 첨부 원 로그.
- `evidence/input/kg50_d07_T_1030.tgz`: 최초 시험 원묶음.
- `evidence/independent/checks.json`: 최신 독립 확인 55항.
- `evidence/independent/original_log_recomputed.json`: G1/G3 직접 비교.
- `evidence/independent/new_call_duration_change.json`: 새 호출에서 원·재개 덱을 함께 바꾸면 210001 끝점이 통과하는 반례.
- `evidence/independent/gate_probe/`: Bash 초기화 실패 기록. PASS 증거가 아니다. 가짜 체크포인트는 실물 체크포인트가 아니다.
- `evidence/independent/gate_model/`: 별도의 조건 모형. 실제 제출 시험이 아니다.
- `evidence/independent/harness_initial_checks.json`: 독립 탐침 초판의 공백/플랫폼 줄바꿈 비교 오류 기록. 수정 후 55항 결과와 혼동하지 않는다.
- `evidence/probe_submit_gate.py`: 선택적 Linux 가짜 제출 탐침. 실제 sbatch를 함수로 대체한다. 이 검토 환경에서 완료하지 못했으며 GO 근거 수에 포함하지 않는다.
- `evidence/intake.py`: 최초 로컬 파일 수령 스크립트. 사용자 PC 경로가 들어 있으므로 기본 재현 명령이 아니다.

체크포인트 바이너리·실행 바이너리·헬퍼 원문·원격 sacct 원문은 패키지에 없다. 기록된 해시와 받은 실행 로그의 일치 범위만 판정했다.
`evidence/MANIFEST.sha256`는 최초 수령 ZIP의 manifest이고, `PACKAGE_MANIFEST.sha256`는 이 검토 전달본의 manifest다.
재현은 파생 파일을 다시 쓰므로 재현 전 전달본 manifest를 먼저 검증한다.
