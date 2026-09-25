# VGCF 탄성계수 민감도 — SBE 킷 3 팔 결과 (2026-09-25, kgy)

사전등록: `docs/reviews/vgcf_e_sensitivity_prereg_20260925.md` (판정 §7-3).  코드 `9da8df0e7` (kgy 분리 워크트리 `~/dem-vgcfE`).
킷 `VGCF_PTFE_3_1` (6 mAh · P:S 7:3 · VGCF 3 wt% · PTFE 1 wt%) 을 `--add-e-override VGCF=1 / 10 / 100` 만 바꿔 재압밀 (n_grid 256 · mach 0.03 ·
hold · legacy_moving) → STEP3 σ_e (vox 0.15 · bridge 0.24 µm · PTFE centerline · LEAN=2 · origin 1 팔 · GPU).

| 파일 | 무엇 |
|---|---|
| `summary.tsv` | 팔별 한 줄 — 태그 · porosity · 두께 · wall_z · settled/target · 정착 응력 · σ_e · dof · CG 수렴 |
| `mpm_metrics_E{1,10,100}.json` | 압밀 산출 `mpm_metrics.json` 원본 (kgy `VGCF_PTFE_3_1_E*/latest_run/`) |
| `step3_arms_pruned.json` | STEP3 팔 JSON 3 개에서 긴 배열 (시각화 · 필드, 200 원소 초과) 을 떼어 낸 발췌 — σ_e 와 수렴 정보는 원본 그대로 |
| `step3_run_receipt.json` | 러너 영수증 (vox · bridge · PTFE 규약 · expect_backend gpu · code_sha) |
| `step3_runner.log` | 러너 로그 (세 팔 · rc 0) |
| `vgcf_e_tags_20260925.txt` | 압밀 태그 확인 출력 |

- 원본 팔 JSON (각 100 MB 급, 시각화 배열 포함) 은 커밋하지 않았다 — kgy `~/dem-vgcfE/kits/vgcf_e_sens_20260925_arm1/` 와 사용자 PC 에 있다.
- ⚠ `mpm_metrics_E100.json` 의 `dt` 0.0002 는 **요청값**이다 — 실제 dt 는 CFL 가드로 1.347 × 10⁻⁴ (원장 `SELF-50`).
- 한정: 한 침대 · origin 1 팔 (origin 위상 산포 0.68 % 가 팔 간 차이보다 크다) · 1–100 GPa 만 시험 (문헌 단섬유 180–245 GPa 는 범위 밖).
