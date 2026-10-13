# ①′ T4-3 `raster_order_size` (원장 `RINTG-11`) — 실행 전 등록 (2026-10-13)

> **지위** — 보고 전용 측정의 **실행 전 등록**.  이 문서를 커밋한 **뒤에** 진단을 돌린다 (등록 커밋 → 시험 · 도구 → 실행 → 결과 커밋).
> 결과는 legacy OFF 계약 (선택 (1) · v3 §1 · v3.1 §2) 을 **바꾸지 않는다** — 크기가 의미 있으면 D21 (선택 (2) canonical bulk · 새 OFF 세대) 을
> 1저자에게 올린다 (v3 §8-2 · 결정은 1저자).  ①′ 정량 채택 · 생산 HOLD 그대로 · 웹앱 화면 없음 (기구 · 시험 전용).
> 근거 = v3 §1 T4-3 (`docs/reviews/contact_resistance_pipeline_draft_v3_20261006.md` L89) · v3.1 §2 (RINTV-02 의 실침대 영향도 여기) ·
> Codex v3 판정 §3 (`docs/reviews/codex_review_rint_g2_v3_20261007.md`) · 원장 `RINTG-11`.

## 1. 무엇을 재나

legacy raster (`step3_sigma.rasterize`) 는 입자 **행 순서**에 따라 sid · pid 가 달라질 수 있다 — `_ball` 은 나중 입자가 덮어쓰고
(서로 다른 AM 종류의 렌즈 겹침 = sid 라벨 · pid) · 브리지 중심식은 (i, j) 계산 순서에 끝자리가 걸린다 (격자 경계 셀의 AM 포함 여부 · RINTV-02).
합성 반례 (Codex) 는 있다 — 혼합 쌍 σ_OFF +4.740683 % · 마스크 3170 ↔ 3171.  **실침대 크기는 미측정** (RINTG-11) — 이것을 잰다.

## 2. 봉인 (실행 전 · 바꾸지 않는다)

| 항목 | 값 |
|---|---|
| 침대 | 리포 안 AM-only scaffold 셋 — `real_14` (`docs/data/real14_am_scaffold.csv`) · `case15` (`docs/data/case15_corner_20261001/case15_am_scaffold.csv`) · `kit_ps_5_5` (`docs/data/kit_ps_scaffolds/kit_ps_5_5__am_scaffold.csv.gz`) |
| 틀 | T4-1 census 와 같다 — LIGGGHTS 상자 × 1000 µm · lo (0, 0, 0) · hi (L, L, max(z + r)) · L = 덤프 상자 옆면 (real_14 50 · case15 100) · kit = `kit_ps_5_5__mpm_input.json` `lateral_box` (50) · 비주기 · dilate_z 1 · 첨가제 · SE 없음 |
| 격자 | `vox0.4_bridge1.2h` (vox 0.4 µm · 브리지 기본 1.2·vox) · `vox0.15_bridge0.24` (vox 0.15 µm · 브리지 0.24 µm 고정) — T4-1 과 같은 둘 |
| 기준 순서 π₀ | scaffold 파일 행 순서 (생산 입력 순서 = 덤프 행 순서 · scaffold 는 그 덤프에서 만든 것 — 같은 순서인지는 확인 안 함 · π₀ 는 "파일 순서" 로만 부른다) |
| 다른 순서 K | **K = 7** — π₁ = 역순 · π₂ … π₇ = `numpy.random.default_rng(seed).permutation(N)` · **seed = 20261013, 20261014, 20261015, 20261016, 20261017, 20261018** (k = 2 … 7 순) · 모든 침대 · 격자에 같은 seed (N 은 침대마다) |
| 비교 | 각 π_k (k = 1 … 7) 의 raster ↔ π₀ 의 raster — 같은 입자 집합 · 같은 틀 · 같은 격자 · `tol_am_um` 0.10 |
| 보고 (raster 만 · 셀 단위) | ① sid 가 다른 셀 수 — 전이별: 라벨 (AM_S ↔ AM_P · 1 ↔ 2) · 마스크 (AM ↔ 비어 있음 · 0 ↔ 1/2) ② pid 가 다른 셀 수 (je · 입자별 전류에 걸린다) ③ 바뀐 셀의 자리: `lens` (셀 중심을 품는 구 ≥ 2) · `bridge` (구 ≤ 1 · 어느 브리지 공 (두 계산 순서) 안) · `other` (그 밖 — 생기면 결함 신호) ④ 렌즈 셀의 종류: 품는 구의 AM 종류 집합 (`AM_S` · `AM_P` · `mixed`) ⑤ π 일곱에 걸친 최소 · 중앙 · 최대 · n_M 대비 비율 |
| σ_OFF (작은 격자만) | `real_14` × `vox0.4_bridge1.2h` (격자 125 × 125 × 79 = 1,234,375 셀) 에서만 — π₀ … π₇ 8 솔브 · 전자 σ 표 AM_S 0.010 · AM_P 0.005 S/cm (생산 `electronic_sigma_table` 기본 AM 값 · 첨가제 없음) · 판 z_bot 0 · z_top = 판 메시 z 30.2845 µm (`docs/data/real14_reference_20260928/README.md`) · 생산 `solve_sigma_z` 를 그대로 부르되 **이 진단 안에서만** `_solve_cg` 를 Jacobi CG rtol 1e−12 · maxiter 200,000 으로 바꾼다 (생산 기본 rtol 1e−8 은 셀 몇 개의 차를 가릴 수 있다) · 보고 = σ_k/σ₀ − 1 (k = 1 … 7) · cg_info · 상대 잔차 |
| σ 비용 상한 | 솔브 하나가 벽시계 20 분을 넘으면 σ 를 멈추고 `not_computed (cost)` 로 적는다 · case15 · kit · vox 0.15 의 σ_OFF = **이 컨테이너에서 하지 않는다** (CPU 4 · RAM 15 GB · GPU 없음 → 생산 기계 몫) |
| 판정 | **없음** (보고 전용) — 문턱 · 합격선을 두지 않는다 · D21 을 올릴지 = 1저자 |

## 3. 하지 않는 것 · 한계

- 생산 침대 (첨가제 · SE 가 덮어쓴 sid) 의 순서 의존 — 리포에 첨가제 점 집합이 없다 (AM-only 침대만).  첨가제 단계는 AM 순서와 무관하지만
  첨가제 **전** AM 마스크가 순서에 걸린다 (v3.1 §2 L127) — 그 몫은 AM-only raster 로 잰다.
- 생산 MPM 프레임과 원점 위상이 같은지 확인 안 함 (T4-1 과 같은 한정) — 셀 단위 재현 주장 아님 · 통계 대표성만.
- 실침대에서 입력 순서를 바꾸는 생산 경로가 있는지 = 미확인 (v3 §1 그대로).
- 결과를 본 뒤 K · seed · 보고 항목 · 격자를 바꾸지 않는다.  바꾸려면 새 등록 문서.

## 4. 실행 (이 등록 커밋 뒤)

```
python3 scripts/rint_t43_order_diag.py --out docs/data/rint_t43_order_20261013
```

산출 = `docs/data/rint_t43_order_20261013/` (JSON + README) · 원장 `RINTG-11` note (보고 전용 · 상태 open 그대로).
