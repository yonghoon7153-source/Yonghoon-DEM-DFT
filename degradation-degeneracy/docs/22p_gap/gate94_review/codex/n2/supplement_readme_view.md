# G93-N2 원 로그 보충 (2026-10-06 · 재실행 0)

93차 회신 G93-N2: 요청 커밋 `0e3c244ea` 의 `gate93_evidence/` 에는 README 만 있었다. 원인은 `*.log` 이 gitignore 대상이라
증거 커밋 `2ab61069b` 의 `git add` 가 로그를 조용히 건너뛴 것이다. 원 로그는 **요청 커밋 뒤** `e0e9f213d` 에서 `git add -f` 로 들어갔다
(요청 커밋 기준 tree 에는 없다 — 회신의 관측이 맞다).

이 디렉터리는 그 로그를 검토자에게 첨부할 수 있게 묶은 것이다.

| 파일 | 크기 (B) | sha256 |
|---|---|---|
| `GATE93_N2_ORIGINAL_LOGS.zip` | 128,409 | `b76e663dcf9fba7ce18a0381e01b1777ad7e594d341d42a74376669d37c3f7c6` |
| `GATE93_N2_LOG_MANIFEST.json` | 11,913 | `b2ee0d56a10be75c16dcd81fd23d65c4f1814ef6426b3fddabb37e08ec577620` |

- zip 안 14 로그 = `e0e9f213d:degradation-degeneracy/docs/22p_gap/gate93_evidence/*.log` 의 blob 바이트 그대로 (zip 항목 시각은 고정값 —
  당시 시각은 manifest 의 `scratch_mtime_utc`).
- 14 개 모두 당시 스크래치 원본 (`g92_red.log` · `g92_emit.log` · `g92_check.log` · `g92_k07.log` · `kext1.log` · `kext2.log` ·
  `g92ev/06…14` · `g92ev/run{1,2}_aborted/10_pytest.log`) 과 **sha256 동일** (`scratch_original_byte_equal: true`). 원본 수정 시각
  12:30:38Z (00 RED) … 19:17:57Z (14 docs-lint) — 모두 요청 커밋 이전 실행이다.
- 파일별 실행 상태는 manifest 의 `status_lines` (로그 자체의 마지막 rc · 시작 / 끝 HEAD · dirty · pytest 요약 줄 발췌).
  요약: 00 RED `41 failed, 97 passed` rc 1 · 10 `2320 passed, 1 xfailed` rc 0 · 11 smoke rc 0 · 12 재생 `ran 421` (scenario 432 · executable 421) rc 0 ·
  10 · 11 · 12 의 끝 HEAD `3ec8aadb1` dirty 0 · 14 docs-lint `360 passed` rc 0 (끝 HEAD `0e3c244ea` dirty 0) · 중단 두 실행 (run1 F4 · run2 F1) 은 시작 줄만.
- 재실행은 하지 않았다. 이 묶음은 당시 파일의 인계일 뿐 새 검증이 아니다.
