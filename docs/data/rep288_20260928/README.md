# rep288 — d_h 288 세대 점검 재현 2 런 (2026-09-28 발사 · 판정 2026-09-30)

판정선 = [`docs/se_curve_transfer_verdict_20260806.md`](../../se_curve_transfer_verdict_20260806.md) §⑩-b (결과 전 등록 09-28):
두 점 모두 |Δ ln σ| ≤ 0.01 · |Δ두께| ≤ 0.01 µm → **세대 무해** / 하나라도 넘으면 세대 교란.  비교량 = 적합기가 읽는 두 값 (`thickness_um` · `final_stress_GPa`).

**판정 = 세대 무해** (두 점 모두 판정선 안 — 두께는 셋째 자리까지 같고 σ 는 넷째 자리만 다르다 · 바이트 동일은 아니다).

| 점 | 옛 파일 (리포 `docs/data/se_curve_metrics/`) · 세대 | 두께 옛 → 새 (µm) | σ 옛 → 새 (GPa) | Δ ln σ | settled_over_target 옛 → 새 |
|---|---|---|---|---|---|
| ps_10_0 ε 11.81 | `xfer_res_kit_ps_10_0_g288_e1181.json` · 08-06/07 | 108.419 → 108.419 | 0.4037 → 0.4039 | +0.00050 | 1.3467 → 1.3472 |
| ps_7_3 ε 11.73 | `xfer_kit_ps_7_3_g288_e1173.json` (= `xfer_res_…` 사본 · settled 1.7558) · 08-11 준정적 게이트 **전** | 108.455 → 108.455 | 0.5268 → 0.5266 | −0.00038 | 1.7559 → 1.7553 |

- 판정선 대비 여유: σ 20 · 26 배 · 두께 0 (JSON 반올림 해상도 1e-3 µm · Δln ~3e-4 ≪ 판정선).
- `porosity_at_target_pct` 11.762 · 11.721 = 같음 · `n_pts` · `frames_budget` 400 = 같음.
- 그 밖에 달라진 키 = **새 세대가 새로 기록하는 메타** (`seed` — 옛 `xfer_res` 는 기록 안 함 · 옛 `xfer_kit` 은 3 = 새 3 · `add_rng_per_phase` · `quasistatic_*` ·
  `platen_mach_Vc*` · `coverage_boundary` · `am_load_split`) — 값의 차이가 아니다.
- 실행: v100 `~/rep288` (적합기 글롭이 못 보는 따로 폴더 · 태그 `rep288`) · 코드 `93a8b2d27` · mpm3d md5 `866c8ed1` · wall 10,382 · 9,395 s · 배치 끝 09-28 14:35 KST
  (`rep288.log` · 첫 발사는 conda 환경 문제로 재발사 — `SELF-57`).

⇒ 대등화 표 (§⑩-b) · ps45 동결선 (`docs/data/dh_frozen_288_phi075_20260926.json`) 은 **그대로** · §⑩-b 의 ③ · ④ 판정은 잠정이 아니다 · 옛 점 7 개 재실행 없음.

받은 묶음: `v100_ps45_rep288.tar.gz` sha256 `4c831f66…511a` (ps45 원자료와 같은 묶음 — [`../ps45_dh_transfer_20260926/`](../ps45_dh_transfer_20260926/)).
