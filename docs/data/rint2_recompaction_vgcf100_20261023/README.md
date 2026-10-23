# Rint ② 다음 세대 침대 — VGCF E 100 GPa 재압밀 (kgy · 2026-10-23)

- **무엇** — 두 침대 (SBE `kit_SBE` · DBE `kit_DBE_sdcp1um`) 를 VGCF E 10 → 100 GPa 로 다시 압밀한 새 킷 `kit_SBE_vgcf100` · `kit_DBE_sdcp1um_vgcf100`.
  - 근거 = 등록 R 머리 줄 7 (`docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md`) · 설계 §1-5 (`docs/reviews/rint_carbon_additive_design_v1_20261020.md`) · 1저자 10-20 밤 · Q18 = VGCF E 만 바꾼다 · 이름 = **"E + dt + 재하율 세대 전환"**.
  - 명령 = `docs/reviews/rint2_kgy_commands_20261020.md` §1-1 · §1-2 (Q13 (가) = payload 줄의 `--joule-heat` · `--save-step4-grid` 두 토큰 뺌).
- **기계 · 코드** — kgy (RTX 3090 24 GB · 발사 전 사용 3.1 GB) · 압밀 코드 = 핀 `298a73197` (kgy `~/dem-anchor1019b` · dirty False · `mpm3d_compaction.py` sha256 `b8bb85278b09e423`).
- **시도** — SBE 시도 1 = 10-20 22:48:27 (Taichi CUDA OOM · 계산 전 · 마커 없음 · 폴더 보존 · 진행 기록 10-20 22) · SBE 시도 2 = 10-23 21:04:42 완주 · DBE 시도 1 = 10-23 21:32:24 완주.
  - 시간 = SBE 는 DBE 시작 (21:32:24) 전에 끝났다 (DBE 줄은 SBE 완료 마커가 있어야 뜬다) · DBE 는 22:11:59 감시 화면에서 완주 → 침대당 ≈ 30–40 분 (어림 · 명령 문서 어림 1.5–2 h 보다 짧음).
- **원자료 (1저자 화면 그대로)** — `docs/data/rint2_recompaction_vgcf100_20261023/s1_4_output.txt` (§1-4 · 첫 실행 실패 포함) · `docs/data/rint2_recompaction_vgcf100_20261023/s1_4b_output.txt` (§1-4b) · `docs/data/rint2_recompaction_vgcf100_20261023/displacement_output.txt` (§1-4c · 기술 보고).

## 1. 결과 전 기대와 대조 (명령 문서 §1-4 · §1-4b 의 "결과 전 기대" 표)

| 칸 | 기대 | SBE (옛 → 새) | DBE (옛 → 새) | 대조 |
|---|---|---|---|---|
| `E_anchor` | 둘 다 `ADD_E_SET_20260926_VGCF100GPa` | None → 같음 | `…+override:VGCF=10.0GPa` → 같음 | 일치 |
| VGCF `E_GPa` | 10 → 100 | 10 → 100 | 10 → 100 | 일치 |
| `dt_effective` | ≈ 1.3108617603 × 10⁻⁴ | None → 1.3108617602605851 × 10⁻⁴ | 2.0 × 10⁻⁴ → 같은 값 | 일치 |
| `dt_cfl_limited` · CFL 제한 상 | True · VGCF (M ≈ 134.6) | True · VGCF (M_max 134.61538) | 같음 | 일치 |
| `platen_mach_VcP` | 0.2717 → ≈ 0.41 | 0.4145 | 0.4145 | 일치 |
| `porosity_at_target_pct` | 숫자 (None 아님 = 목표 도달) | 7.86 | 7.368 | 일치 |
| 두께 · `porosity_settled_pct` | 옛 값과 비교만 | 72.534 µm · 7.86 % → **같음** | 72.534 µm · 7.368 % → **같음** | — |
| `phase` · `fibre` · `fibre_kind` · `fibre_dia` | 같음 | 같음 | 같음 | 일치 |
| `se_dump` | 다름 | 다름 | 다름 | 일치 |
| 상별 점 수 | 기준 침대와 같음 | SE 66,044,152 · VGCF 1,643,483 · PTFE 235,046 · 합 67,922,681 | 합 67,919,722 · SDCP 116,532 | 일치 (SBE 의 SE · 합 = 이번이 첫 기록) |
| 종료 이유 | hold → 도달 뒤 40 프레임 이완 | `✓ held at target` · FINAL 있음 | 같음 | 일치 |
| 누적 코드 시간 | 150 프레임 예산 0.7865 이하 | 0.215–0.236 (첫 비-descend frame 5 · ±5) | 같음 | 일치 |
| 재시도 · 선별 | 실패 시도 포함 전부 | 10-20 시도 1 (마커 없음) + 10-23 완주 | 10-23 완주 하나 | 일치 (목록에 파일이 섞임 = `SELF-130`) |
| 실행 코드 | `~/dem-anchor1019b/scripts` · HEAD `298a73197` · dirty False | 같음 | 같음 | 일치 |

기대가 없던 칸 (기록만): `stop_mode` legacy_moving · `platen_mach_VcS` 2.9602 · `settled_over_target` 0.0005 · 0.001 · wallP (frame 줄) 최대 4.039 · 4.06 GPa → 끝 0.0005 · 0.0006 GPa · `quasistatic_violation` True (옛 런도 True — 킷 = `--allow-fast-platen` 등급 B).

## 2. SE 위치 변화 (§1-4c · 기술 보고 · 판정 미사용)

옛 · 새 침대는 시딩이 같아 (`phase` 같음) 점 순서가 같다 → 점마다 최종 위치 차.  단위 = metrics `um_box_um` 54.3478 µm / 상자 단위 · 옆 경계 = 주기 (로그 `xy=periodic`) → 최소 영상으로 접음 (주기 = 격자 242 칸 = 0.92015209 단위 = 50.0082 µm).

| 상 | SBE 중앙 · p99 · p99.9 · 최대 (µm) | SBE > 0.15 µm · > 0.4 µm | DBE 중앙 · p99 · p99.9 · 최대 (µm) | DBE > 0.15 µm · > 0.4 µm |
|---|---|---|---|---|
| SE | 0.00045 · 0.07920 · 0.13125 · 0.4611 | 0.032 % · 0.000 % | 0.00040 · 0.07456 · 0.12104 · 0.4401 | 0.019 % · 0.000 % |
| VGCF | 0.00044 · 0.06296 · 0.12311 · 0.4221 | 0.020 % · 0.000 % | 0.00039 · 0.05749 · 0.11255 · 0.3962 | 0.011 % · 0.000 % |
| PTFE | 0.00057 · 0.05888 · 0.11913 · 0.4377 | 0.036 % · 0.004 % | 0.00047 · 0.05811 · 0.12089 · 0.4118 | 0.052 % · 0.002 % |
| SDCP | — | — | 0.00038 · 0.05806 · 0.10989 · 0.3265 | 0.023 % · 0.000 % |

주기 경계를 넘은 점 (최소 영상으로 접은 수) = SBE SE 7,288 · VGCF 77 · PTFE 12 / DBE SE 5,721 · VGCF 69 · PTFE 6 · SDCP 1.

## 3. 읽는 법 (한정)

- **두께 · porosity 가 소수 셋째 자리까지 같은 이유** — `--protocol hold` 에서 판은 프레임마다 같은 거리를 내려가다 wallP 가 목표에 처음 닿는 프레임에서 고정된다.  두께는 그 프레임 번호로, porosity 는 두께로 정해진다 (고체 부피 = 시딩 고정).  두 세대가 같은 프레임에서 닿았다고 보인다 (추정 — frame 줄이 5 프레임마다라 ±5).  CLAUDE.md DO-NOT ① *"같은 스트로크면 기하가 소수점까지 같다"* 와 같은 꼴.
- **SE 위치는 바뀌었지만 작다** — SE 점의 99 % 가 0.08 µm 안 · 0.15 µm (STEP3 고운 격자 한 칸) 넘는 점 0.032 · 0.019 % · 0.4 µm 넘는 점 0 (PTFE 만 0.004 · 0.002 %).
- ⇒ STEP3 상 지도 (vox 0.15 µm) 가 바뀌는 칸은 드물다 (추정 · 래스터 전).  **σ_e 차이는 R 런에서 나온다** — 지금 크기 주장 없음.
- ⛔ **"VGCF E 효과" 라 쓰지 않는다** — CFL 이 VGCF 에 걸려 dt 가 2.0 → 1.31 × 10⁻⁴ 로 · 재하율이 Mach 0.27 → 0.41 로 같이 바뀌었다 = "E + dt + 재하율 세대 전환" (Q18 · Phase A 재현 등록의 덧붙임 ① 과 같은 한정).

## 4. 검사 스크립트 결함 · 정정

- **`SELF-130`** — 명령 문서 §1-4 첫 판이 옛 킷의 `latest_run` 을 기준으로 읽었다.  kgy 의 `kit_SBE/latest_run` = v100 시절 절대 경로 링크 (`/home/ubuntu/…`) · 가리키는 런 = 08-12 런 → kgy 에서 FileNotFoundError.  링크가 살아 있었다면 등록 기준 08-27 런 (`docs/reviews/table_s3_data_20260827.md` §② 5/5 일치) 대신 08-12 런 (3/5) 과 비교했을 것이다.  §1-4b 의 `run_*` 글롭은 파일도 셌다 (재시도 목록에 `run_mpm.sh` · `run_a1_anchors.sh` · `run_mpm.sh.orig`).  고침 = 명령 문서 §1-4 (기준 런을 기록의 폴더로 직접 지정) · §1-4b (`run_*/` = 디렉터리만) · 고친 §1-4 는 10-23 kgy 에서 이미 돌았다 (원자료 둘째 실행).
- **`SELF-131`** — 변위 검사 첫 판 (채팅 · 리포 밖) 이 `se_dump` 좌표를 1 단위 = 1000 µm 로 읽었다 (scaffold CSV 단위 — `scripts/cbd_contacts_per_am.py` 주석을 좌표 배열에 옮겨 씀).  값이 18.40 배 (= 1000 / 54.3478) 컸고, 그 위에서 쓴 *"SE 점의 12–13 % 가 격자 한 칸 넘게 움직였다 · σ_e 가 바뀔 여지"* 와 *"침대 밖으로 튄 점"* 은 철회 (최대 0.92015 단위 = 주기 한 바퀴).  고친 판 = 명령 문서 §1-4c.

## 5. 다음

- S0 단계 1 (CPU · raster 만 · 솔브 없음) = 명령 문서 §2 · ⬜ 1저자 승인.  지금 판으로 돌리면 **개발 자료** — R 용 S0 보고는 R 끝 핀에서 다시 만든다 (`S0_SAME_FILES` 일곱 중 `carbon_junction.py` 가 묶음 A″ 에서 바뀜 · `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_A3.md` §8).
