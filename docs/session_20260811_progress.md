# 세션 진행 원장 — 2026-08-11 (compact 전 스냅샷)

> 컨텍스트 압축 전에 **진행 중 판정·수치**를 내려둔 것.  압축은 한정어부터 깎으므로
> (context_meter 훅이 경고하는 그것) 여기 원문으로 남긴다.

## 1. SR-01 A/B — 실행 중 (최우선)

**질문**: STEP3 탄소 래스터를 점→선분으로 바꾸면 Δσ_e 의 **부호와 크기**가 얼마인가.
자체리뷰와 Codex 가 각각 부호를 추론했다가 **반대 결론**에 닿은 자리 → 측정으로만 결정.
카드: `wiki/questions/sr01-delta-sigma-sign.md` · 원장: findings.json SR-01.

### 침대 (두 팔 공통)
`~/Yonghoon-DEM-DFT/se_curve/kit_ps_7_3/run_VGCF1_PTFE1_20260811_211127_54669`
- 압밀 완료 (9분): porosity 13.65 % · thickness 115.10 µm · wallP **0.0148 GPa**(목표 0.3)
- ⚠ **문서화된 플래튼 결함을 그대로 재현**: V/c_P **0.428** · V/c_S **3.05(전단 초음속)**.
  `docs/mpm_platen_kinematic_stop_defect.md` §1 표의 P:S 7:3 행(118.91→115.10 µm,
  wallP 0.0148)과 **완전 일치**.  플래튼이 프레임 5 에서 멈춘 뒤 안 움직였다 =
  300 MPa 도달이 아니라 갭 산술이 정한 4 걸음.
- ⇒ **이 베드의 절대값(σ_e·porosity·coverage)은 인용 금지** (`scope: relative-only`).
  두 팔 Δ 는 공통모드라 유효.
- 산출물: se_dump.npy · fibre.npy(**28,844 섬유**) · phase.npy · fibre_dia.npy

### arm A (점 스탬프) — 전자 채널 **완료**
```
STEP3 σ_e_eff = 0.005122 S/cm   (vox 0.4 µm, 2,713,168 dof, resid 1.0e-08, 3485 s)
   dissipation share: AM_S 39 %  AM_P 57 %  VGCF 4 %  SE 0 %
   econn 100 % (0 isolated) · carbon clusters 6,912
   Joule hot-spot: hot_frac_50 0.055 · conc 858.8×
   collector(cycled):   SBE_bare_110 1.03e-4 / DBE_bare_46 2.39e-4 /
                        SBE_CSUS_30_proxy 3.57e-4 / isotech_SUS_150 7.56e-5 S/cm
   collector(PRISTINE): SBE_bare_18 5.68e-4 / DBE_bare_12 8.08e-4 /
                        SBE_CSUS_10_proxy 9.40e-4 / isotech_SUS_50 2.20e-4 S/cm
   (R_bulk 2.2 Ωcm² ≪ 계면)
```
★ **조기 신호**: VGCF 가 전자 전류의 **4 %** 만 나른다 → 탄소상 래스터 아티팩트가
σ_e 를 움직일 **상한이 작다**(H3 쪽).  ⚠ 단 이건 **점-스탬프 팔** 값이라 조각남이
탄소 몫을 억눌러 4 % 로 보일 수도 있다 — 선분 팔에서 이 share 가 오르면 그게 답이다
(`dissipation_share` 를 비교표에 넣어둔 이유).  carbon clusters 6,912 도 같은 단서.

이온 채널 진행 중 (2,713,128 dof).  이후 열 채널.  **미수렴 경고(⚠ σ UNRELIABLE)는
아직 없음** — resid 1.0e-08 로 정상 수렴.

### 남은 절차
```bash
# arm B 까지 러너가 자동으로 돈다 (이미 실행 중).  끝나면:
#   <run>/sr01_stamp_ab.csv  +  mpm_payload_{point,seg}stamp.json
python3 ~/dem-sk/scripts/sr01_stamp_compare.py <A.json> <B.json> --label kit_ps_7_3
```
판독기가 검사하는 것: 스탬프 도장(manifest) · `fibre_stamp_applied` · vox 일치 ·
**backend 일치** · CG 수렴.  하나라도 어긋나면 Δ 인용 금지 경고.

## 2. cupy — 깔았으나 **이번 A/B 에는 안 쓴다**

```
~/cupy_lib  (--target 설치, venv 밖)   cupy 14.1.1 · CUDA 13.0 → cuda12x · 검증 OK
```
- **arm A 는 CPU 로 확정** (전자 채널이 이미 CPU 로 돌았고, 두 팔은 같은 backend 여야 함).
  `--target` 이라 돌고 있는 프로세스는 이 경로를 모른다 → 오염 없음.
- ⚠⚠ **numpy 그림자 위험**: 이 설치가 `~/cupy_lib/numpy 2.2.6` 을 같이 깔았다.
  `PYTHONPATH=~/cupy_lib` 를 걸면 그 numpy 가 **venv numpy 를 가린다**.  venv 가
  numpy 1.x 면 taichi/scipy/skimage 가 ABI 로 깨지거나 조용히 다르게 돈다.
  **다음 런 전 반드시 확인**:
  ```bash
  ~/Yonghoon-DEM-DFT/venv/bin/python3 -c "import numpy; print(numpy.__version__)"
  # venv 가 1.x 면:  rm -rf ~/cupy_lib/numpy ~/cupy_lib/numpy-*   (venv 것을 쓰게)
  #   단 cupy 14 는 numpy>=2.0 요구 → 그 경우 cupy 13.x 로 낮추거나 venv numpy 를 올린다
  #   (venv numpy 를 올리면 **기존 코퍼스와 수치 동일성**을 먼저 확인할 것)
  ```
- 근본 원인은 SR-03: STEP3 CG 전처리가 **Jacobi 뿐**.  pyamg 는 이미 의존성(STEP4 사용)
  → AMG 전처리가 후보.  ⚠ 솔버를 바꾸면 두 팔이 같은 솔버여야 하므로 **SR-01 종료 후**.

## 3. 다음 순서 (GPU 한 대 = 한 런)

1. SR-01 A/B 종료 → Δσ_e 부호 확정 → 카드/원장 갱신
2. **d_h 288 프로토콜 대등화 = 8런** (12 아님 — 중간점 4개 기존, planner ε 격자 무관 확인)
   ```bash
   cd ~/Yonghoon-DEM-DFT/se_curve
   bash ~/dem-sk/scripts/run_se_curve_batch.sh --repo ~/dem-sk --data ~/Yonghoon-DEM-DFT \
     --kits kit_ps_0_10,kit_ps_3_7,kit_ps_5_5,kit_ps_10_0 \
     --phi 0.66,0.72,0.81 --n-grid 288 --sub 160 --mach 0.03 --gpu-mem 28 \
     --tag eq288 --skip-existing --dry      # ← 먼저 dry: **8** 이 나와야 한다
   ```
   ≈13–15 h.  완료 후 `fit_dh_collapse.py --n-grid 288 --mach 0.03 --phi 0.75`
   → 보간 5·외삽 0 이 되면 "소규모 외삽 포함" 라벨 해제.
   (d_h 배치는 mpm3d 만 부르므로 **cupy 무관** — taichi 가 이미 GPU)

## 4. 오늘 커밋 (claude/stoic-knuth-NObVQ)

| commit | 내용 |
|---|---|
| 4c751ed6 | 준정적 게이트 회귀 수정(킷 전부 거부되던 것) + SR-01 하네스 |
| 98d529b0 | A/B 러너가 두 팔 직접 실행 + production 산출물 보호 (sed 안내가 틀렸음) |
| a00a59af | 배치 `--skip-existing` · dry-run venv 완화 · 검증서 §⑩ (288 5침대·φ선택·8런) |
| 5379a772 | trace_deps importlib 간선 (skimage 결손 원인) + `--check` 잠복버그 |
| d92d4253 | **wiki/ 신설** — llm-wiki-kit v1.7 을 리포 규약으로 개조, 시드 20페이지 |
| 781616b2 | context_budget — CLAUDE.md 예산 + 닫힌 이력 발췌 (Stage 21 −2,810 tok) |
| 719f6454 | sr01_stamp_compare backend·수렴 가드 |
| 977ff6dd | context_meter — 컨텍스트 점유율 훅 (실측 usage) |
| 4200279d | 컨텍스트 실측 규율(CLAUDE.md 는 1.9 % = 레버 아님) + SR-03 등재 |
| cc9b075f | trace_deps 비용 등급(COSTLY_OPTIONAL) + setup 이 cupy 를 깐다 |

## 5. 교훈 (규율로 승격된 것)

- **optional ≠ 안 깔아도 됨.**  cupy 를 optional 로 읽고 건너뛰어 STEP3 를 58분 태웠고,
  그때는 이미 A/B 가 돌아 backend 를 못 바꿨다.  창은 셋업 때 한 번만 열린다.
  → `COSTLY_OPTIONAL` 이 실측 비용을 항상 인쇄한다.
- **토큰 레버는 CLAUDE.md 가 아니었다** (세션 누적의 1.9 %).  실제는 Read 출력 32 %
  (PDF/이미지 9건 = 10 %) · Bash 입력 19 %(heredoc) · Bash 출력 17 %.
- **고치기 전에 재현 테스트 먼저** — 오늘 6b(스탬프 도장 경로) · 8b(importlib 간선) ·
  5b(제약 문단 절단)가 전부 그 순서에서 잡혔다.
