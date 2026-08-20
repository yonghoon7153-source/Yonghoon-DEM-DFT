# 세션 진행 원장 — 2026-08-11 (compact 전 스냅샷)

> ⛔ **HISTORICAL — 이 파일은 작성 시점의 기록이다.  고치지 않고 보존한다.**
> 안에 있는 SR-01 수치(`+52.0 %` · `+5.6 %` · `+42.15 %` · `×35.79` · `f_artifact 0.147`
> 등)는 **2026-08-13 적대 리뷰로 철회**됐다 — 정본은 `CLAUDE.md` SR-01 절과
> `docs/reviews/claims.json` (CL-15 · CL-24).  **원고·발표·인용 금지.**
> (배너 추가 2026-08-20, 철회-문자열 스윕 `check_review_findings.py --ban-sweep`.)

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

## 6. SR-03 — STEP3 CG 전처리: **측정 후** 배선 (기본 OFF)

배선 前에 쟀다.  `scripts/sr03_precond_bench.py` 가 STEP3 의 **실제** `solve_sigma_z` 를 돌리며
전처리만 갈아끼워 (반복수·시간·**σ_eff**) 를 비교한다.  합성 침대(σ 대비 1e5), rtol 1e-8:

| dof | Jacobi it | AMG it | Jacobi | AMG(빌드+) | 속도 |
|---|---|---|---|---|---|
| 61,592 | 3,374 | 218 | 3.9 s | 4.5 s | 0.87× |
| 144,888 | 5,074 | 222 | 15.6 s | 11.3 s | 1.38× |
| 486,963 | 7,088 | **261** | 74.9 s | 51.0 s | 1.47× |

★ **값은 속도가 아니라 반복수 절벽 회피**다.  dof 를 7.9배 늘리는 동안 AMG 는 218→261
(평평)인데 Jacobi 는 3,374→7,088 로 자란다 (겉보기 dof^0.36; 구간지수가 0.48→0.28 로
일정하지 않아 외삽은 **어림값**).  2.7 M dof 어림 Jacobi ≈1.3만 it = maxiter 30,000 의
절반 — 더 미세한 vox·더 높은 대비면 미수렴("σ UNRELIABLE")으로 떨어질 여지가 있고,
그때 잃는 것은 시간이 아니라 런 전체다.

⚠ **속도 이득은 작다** (1.4–1.5×, 2.7M 외삽 ≈2.4×).  벽시계의 진짜 치료는 GPU(cupy)다 —
"58분 → 몇 분" 으로 팔면 안 된다.  (실 arm A 3,485 s 는 위 합성 스케일링의 4.4배 =
실침대가 그만큼 더 어렵다는 뜻이고, 그렇다면 AMG 이득도 더 클 **것으로 보이나** 그것은
추론이지 측정이 아니다.)

★ **해-불변**(채택 조건): 같은 계를 두 전처리로 풀어 σ_eff 비교 — rtol 1e-8 서
0.0007–0.014 %, 1e-10 서 0.0001 %, 출하 경로(플래그) 기준 0.0020 %.
‖Δφ‖_rel 은 1e-3 까지 벌어지지만 전류를 안 나르는 약결합 영역이라 σ 로 안 넘어온다.

배선: `--step3-amg` (기본 OFF = 현행 경로와 bitwise 동일) · `LAST_BACKEND['precond']` 를
manifest 에 도장 · `sr01_stamp_compare.precond_of` 가 두 팔 불일치를 경고 (backend 만 보면
cpu/cpu 인데 Jacobi↔AMG 인 경우가 통과한다).  회귀: step3_sigma `--selftest` +2 (amg-off /
amg-inv), sr01_stamp_compare 31→35.
⚠ **SR-01 A/B 진행 중에는 켜지 말 것** — 두 팔이 같은 전처리여야 한다.
남은 것: 실침대 재확인(위는 합성 침대) · GPU V-cycle 미러 필요성 측정.

## 7. SR-01 재실행 (2026-08-12) — arm A 삼중항 + ★결정론 확인

어제 터미널이 끊겨 arm B 가 시작조차 못 했고, 남아 있던 arm A payload 는
`--check-arm` 판정 결과 **step3 블록이 없는 불완전본**이었다 (파일은 있었다 — 그래서
"파일 존재 = 완료" 로 보던 옛 상태판이 "✓ 완료" 라고 잘못 말했다).  옛 파일은
`mpm_payload_pointstamp.superseded.json` 으로 보존.

### backend — GPU 를 못 썼다 (그러나 **일관되게** 못 썼다)
```
GPU solve unavailable (ImportError: Failure finding "libcublasLt.so") → CPU fallback
solve 시작 7 + 반응 1 = 폴백 8   ⇒ 모든 솔브가 CPU
```
cupy 14.1.1 은 깔렸고 `cp.zeros(1).sum()` 도 되지만 **cuBLAS/cuSPARSE 가 없다**.
⚠ 내 backend 탐지기가 바로 그 이유로 "gpu" 라고 잘못 답했다 — `cp.zeros(1).sum()` 은
솔버가 쓰는 라이브러리를 건드리지 않는다.  탐지는 **솔버가 쓰는 경로 그대로**(cupyx
sparse CG) 찔러야 한다.  고침: `sr01_stamp_ab.sh: probe_backend`.
⚠ **A/B 진행 중에는 cupy 라이브러리를 깔지 말 것** — STEP3 는 `import cupy` 를 **솔브마다**
하므로, 도중에 깔면 남은 채널만 GPU 가 되어 **한 팔 안에서 backend 가 섞인다**.
A/B 종료 후: `pip install nvidia-cublas-cu12 nvidia-cusparse-cu12` → probe 로 검증.

### arm A (점 스탬프, CPU, **60 °C**) — 삼중항
| 채널 | 값 | dof | resid | 시간 |
|---|---|---|---|---|
| σ_e | **0.005122 S/cm** (share AM_S 39 / AM_P 57 / **VGCF 4** / SE 0 %) | 2,713,168 | 1.0e-08 | 3,715 s |
| σ_ion | **0.001982 S/cm** (share SE 100 %) | 1,597,970 | 9.9e-09 | 239 s |
| κ | **1.963 W/m·K** | — | 9.9e-09 | — |

⚠ 이 런은 **60 °C** 조건이다 (`[T] sigma_ion x4.785 @ 60 °C, Ea=0.41 eV, Ea-band
×2.929–5.871`).  절대값을 인용할 때 온도와 밴드를 함께 적을 것.  ⚠ 베드 자체가
rate-오염(V/c_P 0.428)이라 절대값은 여전히 인용 금지 — Δ 만 유효(§1).

### ★ 결정론 확인 (덤으로 얻은 것)
어제와 오늘은 **독립 실행**인데 σ_e_eff 가 `0.005122` 로 같고 dof·resid·share 도 같다.
⇒ 파이프라인이 결정론적이다 = A/B 에서 Δ 가 나오면 **그것이 스탬프 탓임이 보장**된다.
지금까지 "두 팔은 같은 npy 를 읽으니 교란변수 0" 은 **논증**이었는데, 이제 같은 팔을 두 번
돌려 **측정**으로 확인됐다.  (CPU↔CPU 재현이므로 backend 무해성은 아직 미측정 — 그건
cupy 를 고친 뒤 CPU-A vs GPU-A 로 따로 잰다.)

## 8. ★★ SR-01 종결 (2026-08-12) — Δσ_e = ×35.8, 점 스탬프가 과소평가 ★★

두 팔 GPU 완주 (각 ~21분).  kit_ps_7_3, 같은 압밀 베드, 60 °C.

| | arm A (점) | arm B (선분) | Δ |
|---|---|---|---|
| **σ_e_eff** | 0.005122 | **0.1833** S/cm | **×35.79 (+3,479 %)** |
| 소산 share **VGCF** | **4 %** | **95 %** | 탄소 백본 부활 |
| share AM_S / AM_P | 39 / 57 % | 3 / 3 % | AM 우회 소멸 |
| σ_ion_eff | 0.001982 | 0.001835 | −7.4 % |
| κ_eff | 1.963 | 2.01 W/m·K | +2.4 % |
| n_dof 전자 / 이온 | 2,713,168 / 1,597,970 | 2,786,279 / 1,553,369 | +2.7 % / −2.8 % |

**H1 확정** (H2 과대평가·H3 무영향 기각).  기전은 share 가 직접 말한다 — 점 스탬프에서
탄소는 전류의 4 % 만 나르고 AM 이 96 % 를 진다.  선분에서 탄소 95 % 로 뒤집힌다.
σ(VGCF)~1e3 vs σ(AM)~5e-3 이므로 백본 부활 시 두 자릿수 도약이 정합.  이온 −7.4 %(이온
dof −2.8 %)는 탄소가 SE 단면을 잠식한 것, κ +2.4 % 는 탄소가 열전도체인 것과 정합.

★ **어제 중간값 해석이 틀렸다.**  arm A 의 "VGCF 4 % → 아티팩트 상한이 작다(H3 쪽)" 는
반대였다.  그때 단 단서("조각남이 탄소 몫을 억눌러 4 %로 보일 수도")가 사실이고 **4 %
자체가 결함의 크기**였다.  교훈: 진행 중 중간값을 신호로 읽을 때 **그 값이 이미 결함의
산물일 수 있다** — 결함을 재려는 실험에서는 더욱.

⚠ 신뢰 범위: 1 킷 1 베드(단절률 킷마다 20.6–75.8 % → 배수는 킷마다 재야 함) · 베드
rate-오염 → **절대값 인용 금지, 비만 유효** · 60 °C.  어느 쪽이 옳은지는 이 실험이 직접
말하지 않으나, 선분이 6-face 연결을 보존하는 기하학적으로 올바른 래스터화이므로 점 쪽이 오차.
⇒ **파급**: 탄소를 가진 모든 침대의 STEP3 σ_e 절대값·소산 share 가 과소평가.  첨가제
headline 비교(P1 blocker)는 선분 스탬프로 재산출 필요.

### ★ 덤 — backend 무해성이 **측정**됐다
같은 arm A 를 CPU(어제·오늘)와 GPU(오늘)로 각각 돌았다:
```
CPU: σ_e 0.005122 (3,715 s) · σ_ion 0.001982 (239 s) · κ 1.963
GPU: σ_e 0.005122 (  332 s) · σ_ion 0.001982 ( 10 s) · κ 1.963   (CPU fallback 0 건)
```
인쇄 자릿수까지 동일.  "같은 행렬·같은 rtol 이니 backend swap only" 는 이제 **가정이 아니라
측정**이다.  가속 11.2× · 23.9×.

### 오늘 태운 4시간 — 원인과 처방
cupy 를 **"깔렸나"로만 확인하고 "되나"로 확인하지 않았다**.  `pip install cupy-cuda12x` 는
cuBLAS/cuSPARSE 를 안 가져오는데, setup 의 검증이 `import cupy` 라 그 상태를 "cupy OK" 로
통과시켰고, 아침에 러너에 넣은 탐지기도 `cp.zeros(1).sum()` 이라 같은 구멍이었다 (그 연산은
cuBLAS 를 안 건드린다).  결과: `--step3-gpu` 를 주고도 8/8 솔브가 CPU 폴백, arm A 가 20분 대신
4시간.  ⇒ 고침: setup 과 러너 **둘 다** cupyx sparse CG 를 실제로 1회 돌아 검증
(`gpu_solver_ok` / `probe_backend`) + `nvidia-{cublas,cusparse,cusolver,nvjitlink,cuda-runtime,
cuda-nvrtc}-cu12` 를 함께 설치.  = scipy→pandas→networkx→skimage 드립과 **같은 뿌리**
(설치 성공 ≠ 능력 확보).

## 9. 다음 작업 큐 (2026-08-12, 사용자 지시로 등재)

GPU 가 살아나 payload 재실행이 **팔당 ~21분**(옛 ~4h)이라 아래 셋 다 현실적 비용이 됐다.

1. **래스터 충실도 리뷰** — `docs/reviews/sr01_raster_fidelity_review_request_20260812.md`
   (Codex 외부 + 내부 3각 동시).  판정 대상: SDCP +52 % 가 점-스탬프 아티팩트에 의존하는가 ·
   다른 첨가제 결론의 오염 범위 · ×35.8 의 일반화 한계 · **선분 스탬프의 반대편 편향**
   (vox 0.4 µm 가 VGCF 직경 아래를 해상 못 해 단면적이 1 복셀로 양자화 → 과대평가 여지).
2. **f_AM 하중분담 — 안 닫힘, 이어서 갈 것.**  코너 케이스용 보정에 두 운용 규약이 있고
   (contact-network `σzz^AM-AM/σzz^total` vs symmetric phase virial = 전자 + 0.5·share_AM-SE)
   **어느 쪽도 진짜 플래튼 반력으로 검증되지 않았다**.  실측 4점: AM-AM 0.517/0.598/0.675/0.620 ·
   phase 0.726/0.768/0.794/0.763 (P=100/200/300/600).  ⚠ Hertz 재구성 추정기는 실측 대비
   1.30–1.36× 과대 → 사용 금지; 실측엔 contact dump(`pair/gran/local`) 또는 atom dump c_strs[3] 필요.
   → **_10 corner 런을 0 / AM-AM / phase 세 팔로** 돌려 판정.
3. **플래튼 운동학적 정지 결함 — 해결할 것.**  오늘 베드가 그 결함의 재현이다: 플래튼이
   목표 300 MPa 도달이 아니라 **갭 산술이 정한 걸음 수**로 멈춰 wallP 0.0148 GPa (목표 0.3),
   V/c_P 0.428 (준정적 게이트 0.01 위반).  ⇒ 그 베드의 절대값은 전부 `relative-only`.
   정본: `docs/mpm_platen_kinematic_stop_defect.md`.  고치면 **절대값 등급이 B→A 로 올라가고**
   SR-01 재측정도 절대값으로 인용 가능해진다.
