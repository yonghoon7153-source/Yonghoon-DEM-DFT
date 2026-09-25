# 사전등록 — VGCF 탄성계수 (MPM 첨가제 강성) 민감도 · SBE 킷 3팔 (2026-09-25)

> 실행 계약.  **런 전에** 등록한다 (규율: 결과 보고 창을 옮기면 무효).
> 계기 = Methods SI 표 리뷰 (강준희 09-25): *"VGCF Young's modulus 10 GPa 도 그냥 Assumed?"* — 원장 `CL-42`
> (`ADD_E_SET_20260818`: *"사용자 지정 · 근거 문헌/측정 미기재"*).  문헌 단섬유값은 180–245 GPa (Ozkan 2010) 로 우리 값의 20 배.
> 비준 = 사용자 09-25 *"민감도 런을 kgy 에서 진행해보자"*.

## 0. 무엇을 묻나 (한 줄)

**VGCF 재료점의 탄성계수 E 를 1 → 10 → 100 GPa 로 바꿔 같은 침대를 다시 압밀하면 ε_sphere · 두께 · σ_e 가 얼마나 움직이나.**
움직임이 작으면 표의 10 GPa 는 "유효 강성 (2차 입력)" 으로 정직하게 라벨할 수 있고, 크면 앵커 (문헌 단섬유값 또는 섬유를
재료점 구름에서 제외) 없이는 표에 못 둔다.

## 1. E 가 들어가는 자리 (코드 실측)

- `scripts/mpm3d_compaction.py` `ADD_E_NU['VGCF'] = (10.00, 0.30)` — ① CFL dt 가드 (`_M = max(…, λ+2μ)`) ② ADD 표 → 섬유 재료점의 Lamé 상수.
  σ_y 2.0 GPa ≫ 가압 0.3 GPa 라 섬유는 **탄성**으로만 반응한다.
- STEP3 σ 에는 **직접 안 들어간다** — MPM 압밀 기하 (SE 형상 · 공극) 를 거쳐서만.
- 생산 침대 (Phase A 킷 · SDCP W2 SBE/DBE) 는 전부 `--dilate-z` + `--fibre-buckle` 모드 = **강체 strut 아님** (dilation 이 strut 을
  대체, `mpm_input_from_case.py:707`).  ⇒ 두께는 dilation (λ_dz, Cho 보정) 이 정하고 E 는 그 틀 안의 국소 형상만 바꾼다.
- 이미 있는 상한: 2026-07-02 `--fibre-stiff` (E→∞ 강체 핀) — `input_6mAh_real_4` · n_grid 256 · VGCF 4 wt%: porosity 8.63 → 9.38 % (+0.75 %p) ·
  두께 +0.9 µm · SE 소성변형 0.195 → 0.006 (`docs/additive_test_campaign.md` §해결).  σ_e 미측정 · 다른 침대.

## 2. 설계

| 항목 | 값 |
|---|---|
| 침대 | Phase A 킷 `VGCF_PTFE_3_1` (6 mAh · P:S 7:3 · VGCF 3 wt% · PTFE 1 wt% = SBE 조성) — `docs/data/phase_a_6mah/kits/VGCF_PTFE_3_1/` |
| 팔 | E_VGCF ∈ {**1**, **10** (생산값, 같은 코드로 재압밀), **100**} GPa — 킷을 세 폴더로 복사, `run_mpm.sh` 에 `--add-e-override VGCF=<E>` 만 추가.  seed · dilation · buckle · n_grid 256 · mach 0.03 · 그 밖 전부 동일 |
| STEP3 | `scripts/sdcp_gain_vox015_8arm.sh` · `VOX=0.15 BRIDGE_UM=0.24 PTFE_STAMP=centerline LEAN=2 ARMS=1` · 새 OUTDIR (SKIP 캐시 함정 회피) |
| 잰다 | ① `porosity_sphere` (ε_sphere, `mpm_metrics.json`) ② 두께 (`wall_z` → µm) ③ σ_e(SBE) (mS/cm, origin 0) ④ 부수: `settled_over_target` · SE 소성변형 합 · coverage AM |
| 대조 | 10 GPa 팔 = 기준.  1 · 100 의 차이를 기준 대비로 |
| 기계 | kgy (사용자 로컬 GPU) — 압밀 3 회 + STEP3 3 회 |

⚠ 100 GPa 는 SE 스택 (M ≈ 26.2 GPa) 을 넘어 CFL 가드가 dt 를 캡한다 (`mpm3d_compaction.py` 1686–1699) — 더 느릴 뿐 결과 해석에는
문제 없다 (가드가 그 목적).  E 는 재료점 Lamé 상수로만 들어가고 다른 상수는 안 바뀐다.

## 3. 판정선 (런 전 고정)

- **h0 "2차 입력"**: 1 ↔ 100 GPa 사이에서 **|Δε_sphere| ≤ 0.3 %p** **그리고** **|Δσ_e / σ_e(10)| ≤ 2 %** (팔-폭 0.68 % 의 3 배, `CL-33/34` 실측).
  ⇒ Methods 표: *"10 GPa — Assumed (effective compliance of sub-grid fibre material points; σ_e insensitive over 1–100 GPa, Δ ≤ x %)"*.
- **h1 "앵커 필요"**: 둘 중 하나라도 넘으면 ⇒ 표에 10 GPa 를 둘 수 없다.  후속 = 문헌 단섬유 245 GPa (Ozkan 2010) 로 재압밀하거나
  섬유를 재료점 구름에서 제외 (strut 또는 dilation 만).  이 사전등록은 그 후속을 **지시하지 않는다** (별도 등록).
- 두께: 보고만 (dilation 이 정하므로 판정 축이 아니다).  |Δ두께| 가 1 셀 (0.39 µm @256) 을 넘으면 원인 서술.
- 반올림 규약: ε %p 소수 둘째 · σ_e 상대 % 소수 둘째.  판정은 반올림 전 값으로.

## 4. 무효 조건

- 세 팔의 `mpm_metrics.json` 이 `add_e_override` · `E_anchor` 태그를 안 들고 있으면 (같은 코드 · 같은 seed 증명 실패) 무효.
- 어느 팔이든 `reached` 가 아니거나 (`porosity_at_target_pct` None) STEP3 미수렴이면 그 팔은 결측 — 판정 보류 (다른 팔로 대체 금지).
- 10 GPa 재압밀이 옛 `latest_run` 과 ε_sphere 0.05 %p 이상 다르면 **재현성 문제**로 먼저 기록 (판정은 세 새 팔끼리).

## 5. 예측 (기록용 — 판정 아님)

E 가 σ_y 아래 탄성 응답에만 들어가고 두께는 dilation 이 고정하므로 **h0 쪽**을 예상한다 (Δε < 0.1 %p · Δσ_e < 1 %).  strut 극한 (+0.75 %p @4 wt%,
frozen AM) 이 상한이므로 100 GPa 팔이 그것을 넘으면 코드 결함을 의심한다.

## 6. 산출물 · 등재

- 결과 = `docs/data/vgcf_e_sensitivity_20260925/` (팔별 `mpm_metrics.json` 발췌 + STEP3 영수증 + 요약 TSV) · 이 문서 §7 에 판정.
- 원장: `CL-42` (ADD_E_SET) 에 결과 링크 · Methods 표 라벨 (`scripts/build_methods_docx.py`).
- 코드: `--add-e-override` (`mpm3d_compaction.py`) — selftest 로 파서 · 적용 · 매니페스트 태그 · 거부 (미지 상 · 비수치 · 0 이하) 를 고정.

## 7. 결과 (런 진행 중 — 팔이 끝날 때마다 채운다)

### 7-1. 실행 환경 (kgy, 2026-09-25)
- 코드 `9da8df0e7` 분리 워크트리 `~/dem-vgcfE` (kgy 의 `~/dem-mt` 는 이름만 같은 다른 히스토리 — 미사용) · 킷 `~/dem-vgcfE/kits/VGCF_PTFE_3_1_E{1,10,100}` ·
  `kits/scripts → ~/dem-vgcfE/scripts` 심링크 · `MPM_NO_VENV=1 MPM_NO_PULL=1`.
- 파이썬: 새 conda env `ti310` (Python 3.10 · taichi 1.7.3) — 기존 `~/Yonghoon-DEM-DFT/venv` (py3.13 taichi) 는 kgy glibc (Ubuntu 20.04, < 2.32) 에서 import 실패.
- GPU: RTX 3090 24 GB (`--gpu-mem 20` 그대로).
- ⚠ kgy 의 `~/pa/kits/VGCF_PTFE_3_1/run_mpm.sh` 는 **스모크 변형** (`--frames 150` · `--platen-mach` 없음 · align 0.665 · target 0.1585) 이었다 →
  세 팔 모두 리포 등록본 `docs/data/phase_a_6mah/kits/VGCF_PTFE_3_1/run_mpm.sh` (2500 프레임 · mach 0.03 · 0.666 · 0.1589) 로 덮고 `--add-e-override` 만 추가.
  scaffold CSV 두 개는 kgy 사본 그대로.
- STEP3 준비 (09-25 16:2x ~ 17:0x): `ti310` 에 `cupy-cuda12x` 14.2.0 설치 → `step3_sigma._solve_cg` 소형 계에서 `LAST_BACKEND used = gpu` 확인 ·
  `pyflakes` 설치 (러너의 미정의-이름 게이트가 없으면 오탐으로 선다 — Phase A · Lee 전례).  판정용 러너는 `--step3-require-gpu` 라 세 팔 모두 GPU.
  ⚠ payload 미리보기 (vox 0.4) 의 STEP3 는 E=1 · E=10 CPU (cupy 설치 전) · E=100 GPU — 미리보기는 판정에 안 쓴다.
- GPU 공유: kgy 에 **우리 것이 아닌 GPU 작업**이 ~12.2 GB · 98 % 로 떠 있었다 (16:13 · 17:03 · 18:09 관측, 그때 우리 GPU 작업 없음).
  E=100 압밀은 taichi VRAM 상한 (빈 VRAM 의 90 %, `scripts/mpm3d_compaction.py:1737`) 안에서 돌았다.

#### 7-1-b. 운영 사고 셋 (결과에 영향 없음 — 기록)
1. **watch 명령의 자기매칭** — 내가 준 watch 명령줄에 `mpm3d_compaction.py` 문자열이 들어 있어, `run_mpm.sh` 의 "다른 MPM 이 도는 중"
   검사 (`pgrep -f mpm3d_compaction.py`) 가 watch 를 런으로 오인했다.  16:21 루프의 E=100 발사가 `ABORT — an MPM run is already active` 로
   막혔고, 루프도 같은 검사에 속아 E=100 마커를 기다렸다 → 17:10 수동 발사 (약 50 분 손실).  고친 watch 는 `[m]pm3d_…` 패턴.
   ⬜ 재발 방지 제안 (미비준): 킷 생성기 (`scripts/mpm_input_from_case.py`) 의 검사를 python 프로세스만 보게.
2. **E=10 GPU 재실행 지시는 불필요했다** — E=10 은 16:20 에 CPU payload 로 이미 완주했다 (마커 시각 16:20 그대로 = 재실행 스크립트는 효과 없음).
3. **자동 실행 스크립트 두 판** — 두 번째 블록이 실행 중이던 `after_arms.sh` 를 덮어써, 첫 판이 18:07 에 바뀐 파일을 이어 읽었다
   (로그 섞임 · `Permission denied` 한 줄).  러너는 하나 (18:07, 둘째 판 PID 2342285 의 자식) — 18:10 에 둘로 보인 것은 러너가 팔마다 만드는
   하위 셸이라 명령줄이 같게 보인 것으로 판단 (중복이었다 해도 그 PID 는 이미 종료).  E=1 팔 JSON 생성 · 러너 로그에 ABORT/FAILED/OOM 없음.

### 7-2. 팔별 (mpm_metrics.json)

| E_VGCF | 시작 → 마커 | override / E_anchor | additives.VGCF.E_GPa | porosity@target (%) | settled (%) | 두께 (µm) | wall_z | settled/target | wallP 정착 (GPa) | 유효 |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | 13:32:49 → 15:09:36 (압밀 ~32 분 + payload ~65 분) | `VGCF=1` / `ADD_E_SET_20260818+override:VGCF=1.0GPa` | 1.0 | 14.749 | 14.749 | 121.669 | 2.2881 | 0.4662 | 0.1403 | ✅ (§4 충족: 태그 · 도달 non-None) |
| **10** | 15:10:34 → 16:20 | `VGCF=10` / `ADD_E_SET_20260818+override:VGCF=10.0GPa` | (tgz) | 14.889 | 14.889 | 121.869 | 2.2918 | 0.467 | (tgz) | ✅ |
| **100** | ~17:10 → 18:06 | `VGCF=100` / `ADD_E_SET_20260818+override:VGCF=100.0GPa` | (tgz) | 14.929 | 14.929 | 121.926 | 2.2928 | 0.4558 | (tgz) | ✅ |

- 공통: `stop_mode legacy_moving` · `frames_budget 2500` · `wall_z_at_floor False`.  출처 = kgy `vgcf_e_tags_20260925.txt` (세 팔 `mpm_metrics.json` 발췌).
  `(tgz)` 칸은 결과 묶음 수신 뒤 채운다.
- **재현성 (§4 셋째)**: E=10 이 Phase A 생산 침대 재생성값 (`docs/data/phase_a_6mah/regen_20260914_metrics.tsv` 의 `VGCF_PTFE_3_1` 행:
  14.889 · 14.889 · 0.467 · 121.869) 과 **인쇄 자릿수까지 같다** ⇒ Δ 0.000 %p (허용 0.05) ✅.
- ⚠ **등록 결함 — 지표 이름**: §2 ① 이 적은 `porosity_sphere` 는 `mpm_metrics.json` 에 **없다** (있는 것은 `porosity_at_target_pct` ·
  `porosity_settled_pct`, MPM 규약).  세 팔은 고체 부피가 같아 (1 − ε)·H = 103.724 · 103.724 · 103.724 µm 로 일정하다 ⇒ 팔 사이 차이는
  두께 H 하나로만 정해지고, 규약을 바꿔도 그 규약의 (1 − ε) 비만큼 (~1 %) 만 달라진다.  ⇒ 판정은 `porosity_at_target_pct` 로 한다.
- **porosity 축 (§3)**: 1 → 100 GPa 에서 **Δε = +0.180 %p** (14.749 → 14.889 → 14.929, 단조) ≤ 0.3 ⇒ **통과**.
  §5 예측 (< 0.1 %p) 보다는 컸다 — 기록.  두께 +0.257 µm < 한 셀 (0.39 µm @256) ⇒ 원인 서술 불요 (§3).
- ⚠ **E=100 만의 비대칭 (런 뒤 발견, 설계는 그대로)**: 100 GPa 섬유의 P 파 탄성률 (λ + 2μ = 134.6 GPa) 이 SE 스택 (26.2) 을 넘어 CFL 가드가
  dt 를 2.0 × 10⁻⁴ → 1.347 × 10⁻⁴ 로 줄였다.  플래튼 속도는 SE 파속 기준이라 **물리 재하율은 세 팔이 같다** (`scripts/mpm3d_compaction.py:2917`).
  다만 (i) 프레임당 플래튼 걸음이 0.068 → 0.046 µm 로 작아 정지 위치의 양자화가 다르다 — E=10 → 100 차이 (+0.057 µm · +0.04 %p) 는
  이 걸음 크기 수준이고, E=1 → 10 (+0.200 µm · +0.14 %p, 같은 dt) 은 약 3 걸음이다.  (ii) hold 40 프레임의 물리 이완시간이 1.485 배 짧다 —
  porosity 는 무관 (플래튼 고정), `settled_over_target` (0.4558 vs 0.467) · SE 형상에는 영향 가능.
- σ_e 축: STEP3 (vox 0.15 · origin 1 팔 · GPU) 진행 중 — E=1 팔 완료 (18:4x 확인), E=10 · E=100 대기.  판정 (§3) 은 σ_e 까지 받은 뒤.
