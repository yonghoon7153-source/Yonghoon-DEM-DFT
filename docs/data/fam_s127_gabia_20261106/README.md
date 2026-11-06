# FAM §12-7 gabia 원자료 (2026-11-06 수령)

- **출처**: 1저자가 gabia ~/fam_s127 의 결과를 묶어 (11-06 10:05 KST) 이 세션에 첨부했다.  묶은 명령은 원본 폴더에 아무것도 쓰지 않는다 (합 파일은 홈에 만들고 tar -C ~ 로 넣었다).
- **tgz**: `docs/data/fam_s127_gabia_20261106/fam_s127_raw_20261106.tgz` · 31,295 B · sha256 43f40d64ca02ab3f56230c41e3fb48d1c749340b49a94ec23ce88ec46b2b9032.  1저자 화면의 값과 같고, 받은 파일 그대로다.
- **풀어 둔 파일 8 + 합 파일 1**: 빈 폴더에 풀어 sha256sum -c fam_s127_SHA256SUMS.txt 를 돌렸고 8/8 OK 다 (이 세션 · 11-06).
- **빠진 것**: dryrun · dryrun_r2 폴더 (11-04 건식 실행 · 결과 아님).  corner_fa 의 JSON 은 팔이 rc 1 로 끝나 처음부터 생성되지 않았다.
- **등록 · 러너**: `docs/reviews/fam_platen_prereg_20260812.md` §12-7 · `docs/reviews/fam_s127_runner/run_s127.sh`.
- **판정 · 해석**: `docs/reviews/codex_review_fam_s127_results_20261106.md` · `docs/session_20260923_progress.md` 11-06 절.

## 기록 대조 (이 세션 · JSON 과 로그를 직접 읽음)

| 팔 | thickness_um | porosity_at_target_pct | settled_over_target | am_load_split.f_am_cut | stop_mode | am_load_applied_to | dt_cfl_limited | platen_mach_V_over_cP | 로그 수렴 표지 |
|---|---|---|---|---|---|---|---|---|---|
| confirm_fb | 29.491 | 14.638 | 0.1904 | 0.9983915629250772 | freeze_probe | descend+servo_setpoint | False | 0.01 | 1 |
| corner_fb | 12.715 | 0.0 | 0.0994 | 0.9479947350462171 | freeze_probe | descend+servo_setpoint | True | 0.01 | 1 |
| corner_fa | (JSON 없음) | — | — | — | — | — | — | — | 0 |
| corner_f0 | (실행 실패 · 아래) | — | — | — | — | — | — | — | 0 |

- 위 값은 진행 기록 11-06 의 FAM 줄과 같다.
- 로그 수렴 표지는 정확한 문자열 `✓ converged: σzz equilibrated at target` 의 개수다.
- JSON 의 thickness_um 은 소수 셋째 자리로 반올림돼 저장된다.  그래서 29.491 의 일치는 0.001 µm 저장 정밀도에서의 일치다 (Codex 11-06 Q2).
- corner_fb 의 platen_mach_V_over_cP 는 개정값 0.0099999 가 저장 때 반올림된 값이다.
- porosity_at_target_pct 0.0 은 0 클립이 적용된 값이라 완전 치밀화를 입증하지 않는다 (Codex 11-06 Q3).

⚠ **열람 기록**: 대조 스크립트가 corner_f0 (실행 실패 팔 · 플래그로 내보낸 미수렴 JSON) 의 값까지 화면에 찍었다.  그 값은 판정에도 보고에도 쓰지 않고, 여기에도 적지 않는다.
