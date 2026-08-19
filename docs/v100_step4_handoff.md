# STEP 4 격자 스윕 — 메모리 예산 + (예비) V100 이관 (2026-08-18)

> ★★ **결론 먼저: kgy 로 전부 된다.  이관 불필요.**  `nvidia-smi` 실측 = **RTX 3090 24 GB**,
> 호스트 62 GB.  vox 0.10 의 VRAM 피크(~15 GB)·호스트 피크(36.6 GB) 를 둘 다 넘긴다.
> 아래 §1–3 (전송·세팅)은 **쓰지 않는다** — 나중에 다른 호스트가 필요해질 때를 위한 예비 절이다.

`STEPS="4"` (구 스탬프 vox {0.125, 0.10} × 8팔 × 2침대) 의 메모리 예산과, 필요 시의
전송 목록 · 세팅 · 실행.  ⚠ **kgy 에서 죽은 원인은 VRAM 이 아니라 호스트 RAM 이었다** (DR3-08) —
이번 `--no-collector` 수정으로 팔당 솔브가 **3회 → 1회**가 되어 예산이 반 이하로 준다.

---

## 0. 메모리 예산 (실측 dof 기반, 추정 아님)

STEP 1 CPU 원장이 잰 전도 dof: **45,362,494** (vox 0.125) · **86,768,963** (vox 0.10).
계수는 vox 0.15 실측에서 나온 **VRAM 140 B/dof · 호스트 415 B/dof** (호스트 쪽은 +2 % 로 검증됨).

| vox | 전도 dof | **VRAM/솔브** | 호스트/솔브 | 상주(격자+점) | **LEAN=2 피크** | 옛 LEAN=1 피크 |
|---|---|---|---|---|---|---|
| 0.15 | 26.9 M | **3.5 GB** | 10.4 | 1.0 | **12.9 GB** | 23.3 |
| 0.125 | 45.4 M | **5.9 GB** | 17.5 | 1.2 | **20.2 GB** | 37.8 |
| 0.10 | 86.8 M | **11.3 GB** | 33.5 | 1.6 | **36.6 GB** | 70.2 |

### VRAM — **kgy 의 RTX 3090 24 GB 로 충분하다** (2026-08-18 실측 확인)

- vox 0.125 → **5.9 GB** · vox 0.10 → **11.3 GB** (일시 피크 ~15 GB).
- kgy = **RTX 3090 24 GB** ⇒ 0.10 에서도 헤드룸 **~9 GB**.  ✅ 이관 불필요.
- ★ prereg v3 §3 이 "87 M 셀 ≈ 12.8 GB → RTX 3090 24 GB 에 들어간다" 고 적었던 것은
  **CPU 조립 수치를 VRAM 예산으로 읽은 혼동**이었는데(DR3-08), 실측 dof 로 다시 계산한
  VRAM 11.3 GB 가 공교롭게 그 근처다 — **수는 맞았고 논거가 틀렸었다**.  이제 둘 다 확인됐다.
- 근거 점검(자릿수): 7-점 스텐실 CSR = data 8·7 + idx 4·7 + indptr 4 ≈ 88 B/dof,
  CG 작업벡터 6개 × 8 B ≈ 48 B/dof → **≈ 136 B/dof** — 실측 계수 140 과 맞는다.
- ⚠ CuPy 메모리풀이 해제 블록을 붙들고 COO→CSR 변환에 일시 피크가 있으므로 **×1.3 여유**를
  본다: 0.10 에서 **~15 GB**.  16 GB 카드면 다른 프로세스가 GPU 를 안 쓰는 상태여야 한다.

### 호스트 RAM — 여기가 진짜 병목이었다

- **vox 0.125: 24 GB 이상** (피크 20.2 + 여유).  ⇒ 지금 kgy(62 GB)로도 **된다** — 이번 수정으로.
- **vox 0.10: 48 GB 이상** (피크 36.6 + 여유).  64 GB 권장.
- ⚠ kgy 가 두 번 죽은 이유는 솔브가 **겹쳐서**다: 1차는 이온계(36.7 M dof)가 전자계(45.1 M) 위에,
  2차는 집전체 기하 솔브 2회가 그 위에.  `LEAN=2` 는 이제 셋 다 끄고 **σ_e 솔브 1회만** 돈다.

⇒ **결론 (2026-08-18, 사용자 판단 "필요없으면 그냥 kgy에서 해")**: **V100 이관 불필요.**
kgy 는 호스트 RAM **62 GB · 가용 57 GB** 라 `--no-collector` 후 피크(0.125 → 20.2 · 0.10 → 36.6 GB)를
**둘 다** 넉넉히 넘긴다.  러너의 RAM 게이트(22 / 40 GB 요구)도 통과한다.

**VRAM 도 확인됨** (`nvidia-smi`: RTX 3090 24,576 MiB):
- vox 0.125 (5.9 GB) — 이미 7팔이 돌았으므로 증명됨.
- vox 0.10 (11.3 GB, 피크 ~15 GB) — 24 GB 에 **헤드룸 ~9 GB**.  ✅

⇒ **두 격자 모두 kgy 에서 끝낸다.**  아래 §1–3 은 예비 절.
⚠ 그래도 남는 감시 포인트: CuPy 가 터지면 `step3_sigma._solve_cg` 가 **조용히 CPU 로 내려간다**
(느려질 뿐 안 죽는다).  판정기의 `backend` 고정-인자 게이트가 혼입을 잡지만, 로그에
`CG running (GPU, …)` 가 계속 찍히는지 눈으로도 확인할 것.

---

## 1. 전송 목록 (rsync)

두 덩어리 — **코드**(작다)와 **침대**(크다).  결과 payload JSON(팔당 ~131 MB)은 **보내지 않는다**.

```bash
# 변수 (V100 쪽 주소로 바꿀 것)
V100=user@v100-host
REM=/home/user            # V100 쪽 홈

# ① 코드 — git 이 있으면 clone 이 낫다 (버전이 남는다)
ssh $V100 "git clone -b claude/stoic-knuth-NObVQ <repo-url> $REM/dem-sk" \
  || rsync -avz --delete ~/dem-sk/scripts/ $V100:$REM/dem-sk/scripts/

# ② 침대 — 이것만 있으면 STEP 4 가 돈다 (압밀 재실행 불요)
#    ⚠ --dry-run 으로 먼저 크기를 확인할 것
rsync -avzP --dry-run \
  --include='*/' \
  --include='se_dump.npy' --include='se_dump_eps.npy' \
  --include='phase.npy' --include='fibre.npy' --include='fibre_dia.npy' \
  --include='am_scaffold.csv' --include='se_scaffold.csv' \
  --include='run_mpm.sh' --include='latest_run' \
  --exclude='*' \
  ~/sdcp/kit_SBE ~/sdcp/kit_DBE $V100:$REM/sdcp/
```

크기 어림: `se_dump.npy` 가 6,790 만 점 × 3 × float32 ≈ **0.8 GB/침대** 로 가장 크다.
두 침대 합쳐 **~2–3 GB** 예상 — `--dry-run` 의 `total size` 로 확인하고 보낼 것.

**보내지 말 것**: `prereg_v2_*/p2_*.json` (팔당 131 MB × 수십) · `step4_grid_*.npz` ·
`post_*/` 덤프 · `phase_ledger/` (CPU 로 다시 만들면 된다).

### 이미 끝난 팔을 살리려면 (선택)

vox 0.125 의 7팔은 kgy 에 있다.  V100 으로 이어 쓰려면 그 JSON 만 따로 보낸다 (~0.9 GB):

```bash
rsync -avzP ~/sdcp/prereg_v2_vox0125_sph_b048_lean2/ \
  $V100:$REM/sdcp/prereg_v2_vox0125_sph_b048_lean2/
```
⚠ 안 보내도 **손해는 시간뿐**이다 (러너가 SKIP 판정을 payload 내용으로 하므로 없으면 다시 돈다).
⚠ 그 7팔은 `--no-collector` **이전** 규약이지만 **σ_e 는 동일**하다 (집전체 솔브는 σ_e 에 무영향;
`check_arm` 도 σ_e 만 본다).  섞어도 안전하다.

---

## 2. V100 세팅

```bash
ssh $V100
# ① venv
python3 -m venv ~/dem-venv && . ~/dem-venv/bin/activate
pip install -U pip numpy scipy
# ② CuPy — CUDA 버전에 맞춰 (nvidia-smi 로 확인)
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
pip install cupy-cuda12x     # CUDA 12.x.  11.x 면 cupy-cuda11x
# ③ 확인 (fail-closed 게이트가 이걸 안 봐주므로 먼저 눈으로)
python3 -c "import cupy; print(cupy.cuda.runtime.getDeviceProperties(0)['name'], cupy.cuda.Device(0).mem_info)"
python3 -c "import scipy, numpy; print(scipy.__version__, numpy.__version__)"
# ④ 리포 게이트 통과 확인 (러너가 시작 전에 이걸 돌린다)
PYTHONUTF8=1 python3 ~/dem-sk/scripts/check_method_discipline.py | tail -1
PYTHONUTF8=1 python3 ~/dem-sk/scripts/check_undefined_names.py \
  ~/dem-sk/scripts/mpm_webapp_payload.py ~/dem-sk/scripts/step3_sigma.py \
  ~/dem-sk/scripts/viz_mpm_continuum.py ~/dem-sk/scripts/additives.py \
  ~/dem-sk/scripts/sr01_stamp_compare.py | tail -1
# ⑤ 침대 확인 (러너가 latest_run 또는 run_* 에서 se_dump.npy 를 찾는다)
ls -la ~/sdcp/kit_SBE/latest_run/se_dump.npy ~/sdcp/kit_DBE/latest_run/se_dump.npy
free -g | awk '/^Mem:/{print "호스트 RAM:", $2, "GB total,", $7, "GB available"}'
```

⚠ `latest_run` 이 **심볼릭 링크**면 rsync 에 `-L`(역참조)를 붙이거나 링크 대상 디렉터리를 함께
보낼 것 — 링크만 가면 러너가 침대를 못 찾는다 (`ABORT — kit_* 압밀 런 없음`).

---

## 3. 실행

```bash
cd ~/sdcp && . ~/dem-venv/bin/activate
# 스모크 1팔 (~20–30 분) — 규약·GPU·메모리를 한 번에 검증
VOX=0.125 SDCP_SPHERE_D=0.30 ARMS=1 LEAN=2 bash ~/dem-sk/scripts/sdcp_gain_vox015_8arm.sh

# 본 스윕
setsid nohup env STEPS="4" bash ~/dem-sk/scripts/sdcp_next_1234.sh > next4.log 2>&1 &
tail -f next4.log
```

RAM 게이트가 시작 전에 막는다 (**0.125 → 22 GB · 0.10 → 40 GB** 요구).  V100 호스트 RAM 이
그보다 작으면 `SWEEP_VOX="0.125"` 로 먼저 0.125 만 돌린다.

### 결과 회수

```bash
# 판정에 필요한 것은 σ_e 뿐 — 전체 payload(131 MB×16) 대신 요약만 가져오면 된다
ssh $V100 "cd ~/sdcp && python3 ~/dem-sk/scripts/sdcp_gain_verdict.py \
  --dir prereg_v2_vox0125_sph_b048_lean2 --collect-only"
# 원장에 넣을 때는 payload 도 필요하면:
rsync -avzP $V100:~/sdcp/prereg_v2_vox0125_sph_b048_lean2/ ./
```

---

## 4. 지금까지의 상태 (이관 전 스냅샷)

- vox 0.125 **7/16 팔 완료** (SBE a0–a3 · DBE a0–a2 는 JSON 있음; DBE a3 는 σ_e 0.06071 이
  로그에만 있고 파일 없음 — **다시 돌아야 한다**).
- 4팔 쌍대응 참고값 R = 1.14527 (SE 0.135 %p) — ⚠ **형식 판정은 HOLD** (8팔 아님 · a3 payload 부재).
  정본은 원장 CL-41.
- vox 0.10 은 **0팔**.

⚠ 8팔을 채우기 전에는 CL-41 의 수를 결론으로 쓰지 않는다 (prereg §5).
