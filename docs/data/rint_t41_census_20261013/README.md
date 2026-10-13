# ①′ T4-1 `ledger_census` — 리포 안 AM-only scaffold 의 raster 원장 조사 (2026-10-13)

> **지위 — 보고 전용.**  σ 솔브 없음 · 예외 법칙 (D4′) 결정 아님 · **결과를 보고 법칙을 바꾸지 않았다** (v3 §7-1 T4-1) ·
> ①′ 정량 채택 · 생산 HOLD 그대로 · 웹앱 화면 없음 (기구 · 시험 전용).
> 근거 = v2 §4 T4-1 (L414) · §3-6 (D4′ = 이 census 뒤) · v3 §7-1 (L327) · v3.1 §1 N8b · Codex v3 판정 (`docs/reviews/codex_review_rint_g2_v3_20261007.md` — census 개발 GO).
> 산출 = `census.json` (침대 × 격자 6 작업 · 작업마다 하위 프로세스) · 도구 = `scripts/rint_t41_census.py` (셈 시험 `scripts/test_rint_t4_census.py` 8/8 · `--selftest`).

## 1. 입력 · 틀 · 격자

| 침대 | scaffold | AM_P · AM_S | 옆면 L | δ_bound (µm) | DEM 대조 |
|---|---|---|---|---|---|
| real_14 | `docs/data/real14_am_scaffold.csv` | 36 · 421 | 50 µm (덤프 상자) | 0.002915 — 조인 `g_geo.delta_bound_um` (scaffold 자릿수 + 덤프 실측 반폭) | ✅ 조인 PASS (atom · contact 2,060,000) |
| case15 | `docs/data/case15_corner_20261001/case15_am_scaffold.csv` | 104 · 0 | 100 µm (덤프 상자) | 0.002915 — 같음 | ✅ 조인 PASS (1,710,000) |
| kit_ps_5_5 | `docs/data/kit_ps_scaffolds/kit_ps_5_5__am_scaffold.csv.gz` | 88 · 2,292 | 50 µm (`kit_ps_5_5__mpm_input.json` `lateral_box`) | 0.003544 — scaffold 자릿수 + 덤프 `%g` 6 유효숫자 **가정** (덤프 리포에 없음 · 확인 안 됨) | — (덤프 없음) |

- 틀 = LIGGGHTS 상자 × 1000 µm · lo (0, 0, 0) (바닥 z 0) · hi (L, L, max(z + r)) · **비주기** raster · dilate_z 1 · AM-only (첨가제 · SE 없음 → sid_pre = sid).
  생산 MPM 프레임과 원점 위상이 같은지 확인 안 함 → **통계 대표성만 · 셀 단위 재현 주장 아님**.  킷 생산 run_mpm.sh 는 `--dilate-z 1.0214` 를 쓴다 — ①′ 은 그 기하를 N1 로 거부한다 (이 census 는 DEM 기하 dz 1).
- 격자 (생산 규약 둘): `vox0.4_bridge1.2h` = vox 0.4 µm · 브리지 기본 1.2·vox (0.48 µm) — 킷 run_mpm.sh `--step3-vox 0.4` · `vox0.15_bridge0.24` = vox 0.15 µm · 브리지 0.24 µm 고정 — Phase A · Lee STEP3 러너 (VOX=0.15 BRIDGE_UM=0.24 · CL-87 · CL-88).  쌍 규칙 tol 0.10 µm.
- 코드: 실행 시작 커밋 `c0414e8e2` · `census.json` 의 `git_head` (`a7d1ea108`) 는 **쓰기 시점** HEAD — 그 사이 커밋은 문서 · T4-3 도구뿐이고 세 코드 blob (`step3_sigma.py` ad202738 · `rint_iface_join.py` 08de177c · `rint_t41_census.py` ecffaa4e) 은 두 커밋에서 같다 (확인).  Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · CPU 4.

## 2. 결과 (`census.json` 그대로 · 해석은 §3)

| | real_14 · 0.4 | real_14 · 0.15 | case15 · 0.4 | case15 · 0.15 | kit · 0.4 | kit · 0.15 |
|---|---|---|---|---|---|---|
| 격자 | 125·125·79 | 334·334·209 | 250·250·51 | 667·667·136 | 125·125·284 | 334·334·756 |
| 등록 쌍 (gap ≤ 0.10 µm) | 659 | 659 | 124 | 124 | 3,503 | 3,503 |
| contact · ambiguous · gap_bridged | 563 · 27 · 69 | 563 · 27 · 69 | 106 · 3 · 15 | 106 · 3 · 15 | 3,010 · 91 · 402 | 3,010 · 91 · 402 |
| support/true (contact) p10 · p50 · p90 · max | 2.05 · 3.95 · 18.1 · 77.5 | 1.75 · 2.47 · 7.18 · 29.1 | 1.72 · 2.42 · 12.0 · 58.4 | 1.61 · 1.92 · 5.69 · 20.0 | 2.62 · 5.51 · 17.0 · 78.0 | 1.99 · 3.02 · 7.13 · 28.5 |
| a < h (contact / 전체 contact) | 268 / 563 | 42 / 563 | 20 / 106 | 0 / 106 | 2,153 / 3,010 | 203 / 3,010 |
| a < h (ambiguous, A_hi) | 27 / 27 | 27 / 27 | 3 / 3 | 1 / 3 | 91 / 91 | 90 / 91 |
| 3중 면 있는 접점 · 청구자 ≥ 3 셀 · ε 띠 > 1 셀 | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 |
| 미실현 (box_clip · no_support · carbon) | 0 (0 · 0 · 0) | 0 | 0 | 0 | 0 | 0 |
| 미등록 owner 쌍 면 (쌍) | 195 (89) | 1 (1) | 72 (13) | 1 (1) | 1,035 (483) | 29 (20) |
| 옆면 이음매로만 닿는 쌍 (닿음 · 브리지 규칙) | 70 · 75 | 70 · 75 | 10 · 12 | 10 · 12 | 164 · 187 | 164 · 187 |
| N8 정확 중복 · N8b 동심 비동일 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 |
| 원장 거부 사유 | 없음 | 없음 | 없음 | 없음 | 없음 | 없음 |
| 탄소 덮인 목 몫 | 0 (정의상) | 0 | 0 | 0 | 0 | 0 |
| 시간 (raster · 원장 s) · 최대 RSS | 0.06 · 0.75 · 458 MB | 0.21 · 35.0 · 2.3 GB | 0.02 · 1.7 · 733 MB | 0.58 · 81.8 · 4.6 GB | 0.72 · 4.6 · 484 MB | 1.22 · 136 · 7.4 GB |

DEM 대조 (덤프 있는 침대 · `rint_iface_join` 조인 PASS · `step3_sigma._iface_join_crosscheck` — **보고만**):

| | real_14 (두 격자 같음) | case15 (두 격자 같음) |
|---|---|---|
| DEM AM–AM 접촉 행 · 이음매 (seam) · 비주기 | 660 · 70 · 590 | 119 · 10 · 109 |
| contact 부류 중 DEM 에 있음 | 563 / 563 | 106 / 106 |
| ambiguous 부류 중 DEM 에 있음 | 27 / 27 | 3 / 3 |
| gap_bridged 부류 중 DEM 에 있음 | 0 / 69 | 0 / 15 |
| DEM 비주기 접촉 중 원장에 미등록 | 0 | 0 |

## 3. 읽는 법 · 한정어

- **support/true** = CNC 의 support 면적 (N_c^0·h²) ÷ 참 원판 (A_true) — 중앙값 1.9–5.5 · 최대 78 (vox 0.4).  RINTG-02 (총량 정규화 ≠ 국소 막 연산자) 가 다루는 *"support ≠ 참 원판"* 의 실침대 크기다.
  **편향 크기가 아니다** — CNC 편향은 T2-4 · T3-B (D12-V 뒤) 가 잰다.
- **a < h** = CNC 편향 미인증 범위 (v3 §2-1 · RRM 기준이면 `unresolved_subgrid`).  vox 0.4 에서 contact 의 48 % (real_14) · 72 % (kit) · vox 0.15 에서 7 % · 7 % · 0 % (case15).
- **ambiguous 전부 DEM 접촉 · gap_bridged 전부 DEM 비접촉** (real_14 · case15) — scaffold 단독 경로의 모호 부류 (|δ_scaf| ≤ δ_bound) 가 이 두 침대에서는
  덤프 경로에서 전부 접촉으로 풀린다.  ⚠ **예외 법칙 (D4′) 결정이 아니다** — 두 침대 · 이 δ_bound 의 관찰이고, 덤프 경로의 부류 채택은 미구현이다 (조인 = 출처 증명만).
- **3중 · 다중 청구 · ε 띠 = 0** — 이 AM-only 침대들에서 셋 이상이 다투는 셀이 없다 (겹침 δ 가 작아 세 구 · 브리지가 한 셀을 함께 덮지 않는다).
  시험 픽스처 (세 구 · ε 세 청구자) 에서는 그 셀이 생긴다 (`scripts/test_rint_g2_am_iface.py` T0-1′ ⓑ ⓓ) — 도구가 못 세는 것이 아니다.
- **미등록 면** = 등록 쌍 (gap ≤ 0.10 µm) 이 아닌데 두 주인이 면을 공유 (양자화 융합 · 브리지가 셋째를 찌름 · v2 §3-6) — vox 0.4 에서 많고 (kit 483 쌍) vox 0.15 에서 거의 없다.
  정량 모드는 `unreg_law` 선언 없이는 거부한다 (N6 · 자동 fallback 없음).
- **이음매** (seam_unrepresented) = 옆면 주기 영상으로만 닿는 쌍 — scaffold 기하로 센 수 (70 · 10) 가 DEM 덤프의 이음매 행 수 (70 · 10) 와 **같다**.  비주기 raster 가 표현 못 한다 (N2 · 주기 정량 모드 거부).
- **탄소 덮인 목 몫 = 0 은 정의상** — 리포에 첨가제 (VGCF · SDCP · SuperP) 점 집합이 없어 AM-only raster 만 했다 (N_c^surv = N_c^0).  실침대의 탄소 가림 몫은 첨가제 점 집합이 있는 기계에서.
- kit 의 δ_bound 는 덤프 자릿수를 **가정**했다 (리포에 덤프 없음) — 모호 부류 수 (91) 가 그 가정에 걸린다.

## 4. 재현

```
python3 scripts/test_rint_t4_census.py                         # 셈 시험 (합성 · 8/8)
python3 scripts/rint_t41_census.py --selftest
python3 scripts/rint_t41_census.py --out docs/data/rint_t41_census_20261013   # 6 작업 · 약 5 분 · 최대 RSS 7.4 GB (kit · 0.15)
```
