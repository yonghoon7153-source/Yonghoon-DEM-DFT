# D0.7 Q3(나) 한 건 — 최종 독립 검토 패키지

정본 판정: `codex_review_kg50_d07_compress_resume_20261103.md`.

최종 수령 ZIP PIN: `4d2b8fc42dc4d65845570c1bf4de5a67924ad311`.
수령 ZIP SHA256: `564e72ecfbba61ff23513c3e89cfeafbbecc47e199f86228043e6d113cb0dbcc`.
198개 manifest 항목을 검증했다. `received_zip/`가 수령 내용이다.
최종 원격 PIN 조회는 실패했으므로 최종 문서/증거는 ZIP 바이트 기준이다.

`source/repo/`는 먼저 원격으로 읽은 후보 커밋 `50b5fb4b74c14df8738a3f34cdb36c53c6448bc1`의 부분 사본이다.
독립 탐침이 쓰는 코드/시험/본 덱은 최종 ZIP과 바이트 동일하다. 이를 `zip_intake.json`에 기록했다.
최종 요청서는 `received_zip/REQUEST.md`다. 초기 보고와 addendum 사이 충돌은 최종 정본 판정을 따른다.

실제 DEM, MPI, WSL, SLURM 제출/취소, Git 상태 변경, 원본 코드 수정을 수행하지 않았다.
합성 입력의 덱/러너는 검증 산출물이며 실행할 자료가 아니다.
실제337078 시험은 수령한 화면 전사/grep 기록이다. 원 덤프/실행 덱/바이너리를 다시 측정했다는 주장이 아니다.

재현 (이 디렉터리에서 Python3.10 이상, 외부 패키지 불필요):

```text
python -I -X utf8 -B verify_snapshot.py
python -I -X utf8 -B verify_received_package.py
python -I -X utf8 -B phase_review/phase_probe.py
python -I -X utf8 -B fix_order_review/probe_fix_order.py
python -I -X utf8 -B operations_review/probe_identity_mapping.py
python -I -X utf8 -B operations_review/probe_final_schedule.py
python -I -X utf8 -B probe_trial_receipt.py
```

탐침은 자기 디렉터리의 합성 산출물을 갱신한다. `intake_zip.py`는 최초 로컬 수령 기록용이며 재현에 필요하지 않다.
`PACKAGE_MANIFEST.sha256`은 포장 당시 모든 파일을 봉인한다. 재실행 후 탐침 산출물 경로/메타데이터는 달라질 수 있다.
