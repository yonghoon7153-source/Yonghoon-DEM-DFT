# LH 강성 민감도 사전등록 — 7차 독립 리뷰 증거

2026-09-29. DEM/MPI/SLURM 실행 및 실제 캠페인 결과 열람 없이, 제출된 초안의 수식과 판정 구조를 검토했다.

- `review.md`: 한국어 회신. 원본은 작업 폴더의 `docs/reviews/codex_review_mixer_highbo_round7_prereg_20260929.md`.
- `attachment_original.txt`: 원 첨부 바이트 그대로. SHA256 `011f7ea89cd4686832e35f054db85daa42bad2e6b7420010dbe475925ad1030b`.
- `prereg_submitted.txt`: LF 정규화 사본. 회신의 P:행 번호 기준. SHA256 `79255022bef5a87092073a24c45519d15b7294502428d88e8f6dee345417e860`.
- `audit_prereg.py`: 제안 역산의 독립 산술, CI/검정력 수치 적분 및 합성 반례. 새 생산 구현이 아니다.
- `audit_results.json`: 118 assertion PASS / 0 FAIL. 결함 반례가 성립함을 검사하는 assertion도 포함한다.
- `baseline/`: 6차 고정 핀의 생성기·판독기, 이전 회신. 새 미제출 코드의 대체물이 아니다.
- `SOURCES.md`: 근거의 원 출처와 검토 한계.
- `MANIFEST.json`: 아래 고정 파일 집합의 SHA256. 자기 자신의 해시는 포함하지 않는다.

## 재현

Python + NumPy + SciPy 환경에서 이 디렉터리를 기준으로:

```bash
python3 audit_prereg.py
```

검토 환경: Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1. 검정력 계산은 정규 모형하의 해석적 확률 적분이며 DEM이나 Monte Carlo 궤적 생성이 아니다. 반례의 M·분산·스케줄 숫자는 실제 캠페인 측정값이 아니다.

`package_evidence.py`는 고정 파일 목록만 ZIP으로 묶고 다시 읽어 해시를 확인한다. 생산 코드나 실행 상태를 바꾸지 않는다. 새 생성기 CLI, 실제 내보낸 경화 덱, Linux launcher, ibb rank/위상/성능, 실제 r/t/q는 검증하지 않았다.
