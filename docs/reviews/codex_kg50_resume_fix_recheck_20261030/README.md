# KG50 수정 재확인 전달본 · 2026-10-30

판정은 `codex_review_kg50_resume_fix_recheck_20261030.md`이다. 고정 핀 `bf8cf21c6466cdb9411f9320711b871c2d1c651e`.

**부분 수용 / HOLD.** 새 P1 두 건은 준비 설정값의 보존과 실제 실행 입력의 연결에 관한 반례다. 별도 Q5 로그 provenance P2 하나도 포함한다. 실제 KG50 물리 계산이 실패했다는 판정은 아니다.

- `repo/`, `PIN.txt`: 받은 ZIP의 282개 고정 리포 파일과 봉인 목록. 제품 변경 없음.
- `independent/`: 이번 CPU 탐침 코드·입력·실제 반환값·보조 검토. 생성된 로그/덤프/checkpoint는 명시된 합성 자료이며 실제 실행 자료가 아니다.
- `baseline/resume_ckpt.sh`, `resume_independent.diff`: 비교 기준 도구와 독립 diff.
- `intake.json`, `source_identity_verified.json`: 입력 ZIP 및 원격 blob 대조.
- `bash_probe.json`: Bash 기동 실패 원문. 저자 216개 셸 시험을 독립 실행했다고 주장하지 않는다.
- `run_receipt_packaging_check.json`: 전달 폴더에서 새 디렉터리로 재현한 결과. rc 0은 반례 재현 성공이지 대상 도구 GO가 아니다.
- `MANIFEST.sha256`: 이 전달 폴더의 바이트 목록. ZIP 자신의 SHA는 옆 `.sha256` 파일에 별도 기록한다.

Python 3.10 이상에서 새 폴더에 CPU 검토를 재현한다(이번 환경 3.12.14).

```bash
python3 -I -B reproduce.py --out /새로운/빈_결과폴더
```

Windows 예:

```powershell
python -I -B .\reproduce.py --out C:\review-output\kg50-new-run
```

재현기는 기존 출력 폴더를 덮지 않는다. 리포 사본은 읽기만 하고 별도 출력 사본을 사용한다. Bash·네트워크·스케줄러·MPI·LIGGGHTS를 호출하지 않는다. 입력 43개, Q5 생성 가지 11개, 등록에서 독립 재구성한 본문 8개, W2 거부 5개와 새 반례 세 개를 확인한다. 셸 부분의 조건 전사는 실제 Bash 실행과 구분한다.

받은 원문 요청서의 경로는 `repo/docs/reviews/codex_kg50_resume_fix_recheck_request_20261028.md`이다. 실제 실행·본 제출·Q5 물리 GO는 이 자료로 생성하지 않는다.
