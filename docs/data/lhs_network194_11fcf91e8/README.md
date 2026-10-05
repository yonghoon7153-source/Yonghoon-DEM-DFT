# LHS 194 망 단계 배치 (`11fcf91e8`) — 실행 증거 · WSL 소형 시험 원본 (2026-10-05 밤)

- 실행: 1저자 WSL `~/dem-audit` (detached `11fcf91e8`) · `scripts/run_network_194_parallel.py run --root ~/net194_11fcf91e8` · 22:13–22:49 KST (wall 0.60 h) · 갈래 20 × 1 스레드 · 케이스별 망 lock + 메모리 예산 (최대 동시 18 · 예산 대기 3,777 · backfill 96).
- 등록 · 코드 봉인: `docs/reviews/lhs_network_batch_registration_20261005.md` — `manifest.json` 의 `code_hashes` 19 개 = 등록 표 **19/19 같음** · git `11fcf91e8` · `dirty false` · porcelain 빈칸.
- 결과: **194/194 done** (lhs 130 · lhsx 64) · 실패 0 · 실행 = `runs/run_001.json` 한 번 (`kind run` · **retry 0** · `code_changed_during_run []` · `git_sha_end 11fcf91e8`) · 케이스당 시도 1 · merge `code_changed_since_launch []` · `mixed_generation []` · `anomalies []` · `failures []`.
- 시간 · 메모리 (merge_report): lhs 경과 중앙 71.6 s · 최대 345 s · RSS 중앙 0.81 GB · 최대 1.94 GB / lhsx 경과 중앙 156 s · 최대 718 s · RSS 중앙 1.39 GB · 최대 2.59 GB · 실측/추정 RSS 중앙 1.1 · 1.4 · **최대 2.1 · 2.55** (메모리 추정식이 큰 침대에서 낮게 잡는다 — 예산 관문은 추정 기반 · Codex 4차 §5).
- 이 폴더 = 1저자 증거 tar (`net194_11fcf91e8_evidence.tar.gz` · sha256 `f61c940cfc1823242d85f6533cec0721025fcf6a20dcdcd9ea574a81250627ae`) 그대로 — manifest · runs · progress · merged (merge_report · status · metrics_flat · parallel_cases) · cases/*/worker.json · log.txt.  케이스 결과 원본 (`--work/results/<case>`) 은 WSL 에만 있다 (τ 인계 원천 · 보존).
- `smoke_postfix/` = 고친 코드 (`11fcf91e8`) WSL 소형 시험 원본 보고서 · 요약 · 로그 · 대조 · 케이스 기록 (`net_smoke_11fcf91e8_report.tgz` · sha256 `0c77bc225a6f3142e7fd6537d197038c704ad57ab696709c6f80cd0b3cdfab43` 에서 작업 폴더 · 임시 파일 제외) — 26/26 PASS · rc 0.
- ⚠ 배포 (ML 인계) = Codex 재검증 GO 뒤 (4차 = HOLD · RGLR3-01 · 02 · 03).  이 배치는 retry 경로를 타지 않았다 (RGLR3-01 의 우회 경로 밖).
- `overview_20261005/` = 값 미리보기 (그림 6 패널 · 케이스 값 · 코호트 요약 · 재현 스크립트 — `merged/*/metrics_flat.csv` 만 읽는다 · 수송 tortuosity 표기 · Codex 5차 §6 자료).
