# RJ 323957 G2c 진단 — 실제 두 contact 파일 실행 (2026-10-27 23시대 KST · ibb · 1저자)

- 도구 = `docs/reviews/codex_p1_g2c_diagnosis_20261027/paste-diagnostic.sh` (sha256 `93d0bb954343b54d521580b0bad155f586f740fafe1e1b73c2808e3f54b52640` · 읽기 전용 · 1저자가 ibb 로 복사해 `bash` 로 실행 · rc 0).
- 출력 = `diagnostic_output.json` (1저자가 올린 그대로 · sha256 `9f1563b548246804e612296e0e82889a9d2dc2328ee4c4e2d6a4d96b49945e09`) · `diagnostic_status = COMPLETE_NUMERIC_BREAKDOWN_NOT_A_VERDICT` · `recorded_gate_match = true` · `diagnostic_sha256` `46e899b7…`.
- 입력 신원 = 원본 (ibb · ps_7_3_r45 의 in 폴더 contact 3200000 덤프) (149,687,008 B · sha256 `53ae293b…` · 562,605 행) · 시험 (ibb · ps_7_3_r45 의 RJ/R/g2 폴더 같은 step 덤프) (149,729,924 B · sha256 `193e6e6c…` · 562,605 행) · job 323957 · 수용 핀 `4c29705fa` · 기록 판정 = FAIL · `VALUE_MISMATCH` · 누락 · 추가 · 중복 충돌 0.

## 성분별 (다른 쌍 수 · 기존 식 delta > 1e-5 × max(|원본|, 원본 열 중앙값) · 허용폭 바꾸지 않음)

| 묶음 | 다른 쌍 | 최대 |Δ| |
|---|---|---|
| 위치 c_cpl[1–6] | 0 | 0 |
| 합력 c_cpl[10–12] | 303,528 · 300,475 · 284,670 (묶음 447,282) | 0.0165 · 0.0207 · 0.0236 |
| 법선력 c_cpl[13–15] | 2,056 · 1,811 · 1,217 (묶음 3,295) | 1.0e-4 · 7.0e-5 · 1.22e-4 |
| 접선력 c_cpl[16–18] | 472,136 · 471,323 · 471,113 (묶음 544,890) | 0.0165 · 0.0207 · 0.0236 |
| 면적 c_cpl[22] · 겹침 c_cpl[23] · 접점 c_cpl[24–26] | 0 | 0 |

- 방향 바뀐 쌍 22,853 (정규화로 맞춤) · 0 아닌 값의 부호 바뀜 = 열마다 1–337.
- ⚠ 수치 분해일 뿐 판정 · 원인 단정이 아니다 (도구 한정: "No threshold changes, new acceptance verdict or cause inference") — 기하 (위치 · 겹침 · 면적 · 접점) 는 같고 차이는 대부분 접선력에 있다는 관찰까지.  재실행 · 후속 팔 · 허용폭 변경 승인 없음 (그대로).
