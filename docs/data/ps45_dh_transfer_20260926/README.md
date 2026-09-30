# ps45 표본 밖 시험 — 원자료 · 채점 (2026-09-30)

사전등록 = [`docs/reviews/ps45_dh_transfer_prereg_20260926.md`](../../reviews/ps45_dh_transfer_prereg_20260926.md) (§4 판정선 · §6 결과).
**판정 = PARTIAL** (밖 1 · HOLD 0 · 채점 5/5) — 등록된 뜻은 *"한 침대 예외"* 이다 (h1 TRANSFERS 도 h0 FAILS 도 아니다).

## 무엇이 여기 있나

| 파일 | 내용 |
|---|---|
| `ps45_score_20260930.json` | v100 채점 출력 그대로 (`score_dh_transfer.py` · 스키마 `dh_transfer_score_v1`) |
| `metrics/xfer_eq288r45_*.json` · `.log` | MPM 15 런 (침대 5 × φ 3 점) 의 지표 · 런 로그 — v100 `~/Yonghoon-DEM-DFT/se_curve/` 원본 |
| `kits/<kit>__{am,se}_scaffold.csv.gz` · `__mpm_input.json` | 다섯 킷 스캐폴드 (`kit_ps_scaffolds/` 와 같은 `<kit>__<파일>` 규약 · CSV 는 gzip -9 -n) |
| `eq288r45.log` | 배치 로그 — `repo HEAD 93a8b2d27` · mpm3d md5 `866c8ed1` · `--allow-fast-platen` (mach 0.03 = 상대 비교 전용) |

받은 묶음: `v100_ps45_rep288.tar.gz` sha256 `4c831f660b83d0714f7d6af8320765688254760ba695d44e103cd05524ddf1ae` (사용자 v100 → WSL → 세션 첨부 · 같은 묶음의
rep288 두 점은 [`../rep288_20260928/`](../rep288_20260928/)).  채점 JSON sha256 앞 16 자리 `03f4dc4c60071f51`.

## 실행 이력

- MPM 15 런: v100 · 코드 `93a8b2d27` (d_h 288 대등화 8 런과 같은 코드 · 발사 뒤 pull 없음) · n_grid 288 · sub 160 · `--protocol hold --periodic --platen-mach 0.03` ·
  φ 0.66 · 0.72 · 0.81 (ε 목표 15.3–15.4 · 12.0–12.1 · 7.6 — ⚠ 로그 표지 *"겹침 미보정 · ε 목표가 ~1 %p 밀린다"* · 채점은 0.75 를 감싼 두 점의 보간이라 판정에 무관) ·
  15/15 EXIT 0 · 런 한 번 wall 11,056–15,121 s · 배치 끝 2026-09-30 18:17 KST.
- 채점: v100 `~/dem-score` worktree @ `a9f310769` (등록 커밋 `e49847e53` 이후 채점기 · 동결선 변경 없음) · uma 파이썬 · `--selftest` 12/12 · 등록 명령 그대로 (§5-D).
- ✅ **커밋본 재실행 = 같은 답** (09-30 · 컨테이너): 아래 명령이 채점 JSON 을 다시 만들고, 입력 경로 문자열 (`inputs.frozen` · `inputs.dir`) 말고는 **모든 키가 같다**.

```
python3 scripts/unpack_kit_scaffolds.py --archive docs/data/ps45_dh_transfer_20260926/kits \
  --metrics docs/data/ps45_dh_transfer_20260926/metrics --out /tmp/ps45_repro
python3 scripts/score_dh_transfer.py --frozen docs/data/dh_frozen_288_phi075_20260926.json \
  --dir /tmp/ps45_repro --kit-root /tmp/ps45_repro \
  --kits kit_ps_0_10_r45,kit_ps_3_7_r45,kit_ps_5_5_r45,kit_ps_7_3_r45,kit_ps_10_0_r45 --n-grid 288 --mach 0.03
```

## 결과 (판정선 불변 — 등록 §4)

동결선 ln σ = −0.6832 − 0.5753 · ln d_h (288 · φ 0.75 · mach 0.03) · 띠 ±2·sd = ±0.1534 · r = ln(σ_meas / σ_pred).

| 킷 | d_h (nm) | 칸 (dx 0.189 µm) | σ_meas (GPa) | σ_pred (GPa) | r | 판정 |
|---|---|---|---|---|---|---|
| `kit_ps_0_10_r45` | 480.6 | 2.55 ⚠저해상 | 0.9155 | 0.7698 | **+0.173** | **밖** |
| `kit_ps_3_7_r45` | 577.0 | 3.06 ⚠저해상 | 0.6883 | 0.6930 | −0.007 | 안 |
| `kit_ps_5_5_r45` | 669.1 | 3.55 | 0.7155 | 0.6363 | +0.117 | 안 |
| `kit_ps_7_3_r45` | 789.3 | 4.18 | 0.6104 | 0.5786 | +0.053 | 안 |
| `kit_ps_10_0_r45` | 1080.7 | 5.73 | 0.5348 | 0.4830 | +0.102 | 안 |

⇒ **PARTIAL** (최대 |r| 0.173 · 평균 r +0.088).  등록 §3: 저해상 침대가 밖인데 **r > 0** 이면 해상도로 설명되지 않는다 (미해상 협착은 σ 를 **낮게** 낸다) —
등록 문구대로 *"접힘 자체의 문제"* 로 적는다.

## 한정어 (그대로 전파)

- 쓸 수 있는 문장: *"동결한 288/φ0.75 선이 AM_P 4.5 µm 침대 5 개 중 4 개의 σ 를 ±2 sd 안에서 예측했다 — 한 침대 (가장 좁은 채널, `ps_0_10_r45`) 예외."*
  |b| 는 288 에서의 **하한** · mach 0.03 = **상대 전용** · "established" · "transferable" 낱말 금지 (CDX-14).
- **기술 (판정 아님 · 결과 뒤 관찰)**: `ps_0_10_r45` 는 AM_P 가 없어 옛 `ps_0_10` 과 **같은 설계 · 새 시드**다 (d_h 480.6 vs 480.7 nm) — 그런데 σ 가 옛 점보다
  +8.4 % (ln +0.081) 높고, 옛 점 자신도 동결선보다 +0.093 위였다 (r = 0.093 + 0.081).  AM_P 크기를 바꾼 네 침대는 4/4 띠 안이다.
  ⚠ 이 "새 크기 4/4" 는 **사후 분할**이라 주장으로 쓰려면 새 등록 (예: 같은 설계의 시드 반복으로 좁은 끝의 시드 산포 측정) · 독립 리뷰가 먼저다.
- 세대: MPM 런 코드 `93a8b2d27` · 동결선은 옛 세대 점으로 만들어졌다 — 세대 점검 (rep288 두 점) = **세대 무해** ([`../rep288_20260928/`](../rep288_20260928/) · verdict §⑩-b).
