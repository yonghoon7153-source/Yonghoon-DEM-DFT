# UMA MLIP — LPSCl 검증 및 MD 이온전도도 분석 스크립트 가이드

> 작성일: 2026-03-09
> 목적: Meta FAIR Chemistry `UMA (Universal Models for Atoms)` MLIP을 이용한 Li₆PS₅Cl argyrodite 고체전해질 검증 및 Li 이온 확산 분석
> 서버: NVIDIA A40 (`ssh -i NVIDIA_A40_20260309_102904.pem -p 22 ubuntu@machine.runyour.ai`)

---

## 목차
1. [전체 워크플로우](#전체-워크플로우)
2. [Script 1 — validate_lpscl.py](#script-1--validate_lpscl-py)
3. [Script 2 — md_lpscl.py](#script-2--md_lpscl-py)
4. [주요 물리 공식 정리](#주요-물리-공식-정리)
5. [결과 해석 기준](#결과-해석-기준)
6. [실행 명령어 모음](#실행-명령어-모음)

---

## 전체 워크플로우

```
DFT (VASP PBEsol vc-relax)
        ↓
LPSCl_relaxed_conv_52atoms.cif  ← 입력 구조
        ↓
[Script 1] validate_lpscl.py
  - UMA 단일점 에너지 계산
  - UMA vc-relaxation
  - DFT vs UMA 격자상수/에너지 비교
        ↓
LPSCl_UMA_relaxed.cif  ← UMA relaxed 구조
        ↓
[Script 2] md_lpscl.py
  - MLIP-MD @ 600 / 800 / 1000 K
  - MSD 계산 → 확산계수 D
  - Arrhenius 외삽 → 300K D, σ
        ↓
ionic conductivity σ (S/cm)
```

---

## Script 1 — validate_lpscl.py

### 목적
DFT(VASP)로 relaxation된 LPSCl 구조를 UMA가 얼마나 잘 재현하는지 검증한다.
신뢰성 확보 후 MD를 진행하기 위한 선행 단계.

### 코드 설명

#### 1-1. 구조 로드 및 정보 출력
```python
atoms = read("LPSCl_relaxed_conv_52atoms.cif")
cell = atoms.get_cell()
a, b, c = np.linalg.norm(cell[0]), np.linalg.norm(cell[1]), np.linalg.norm(cell[2])
```
- `LPSCl_relaxed_conv_52atoms.cif`: VASP PBEsol vc-relax 완료된 conventional cell
- 화학식: Li₂₄P₄S₂₀Cl₄ = **(Li₆PS₅Cl) × 4**, 총 52 atoms
- cubic, a = b = c = **10.096 Å**

#### 1-2. UMA 모델 로드
```python
predictor = pretrained_mlip.get_predict_unit("uma-s-1p2", device="cuda")
calc = FAIRChemCalculator(predictor, task_name="omat")
```
| 파라미터 | 값 | 설명 |
|----------|-----|------|
| `model` | `uma-s-1p2` | UMA Small v1.2 (~31M active params) |
| `device` | `cuda` | NVIDIA A40 GPU 사용 |
| `task_name` | `omat` | Open Materials (결정성 재료 최적화) |

> **task_name 선택 이유**: `omat` task는 OMat24 데이터셋(무기 결정 재료)으로 학습됨. LPSCl 같은 할라이드 고체전해질에 최적.

#### 1-3. 단일점 에너지 계산
```python
e_singlepoint = atoms.get_potential_energy()
forces = atoms.get_forces()
fmax_initial = np.max(np.linalg.norm(forces, axis=1))
```
- DFT 구조 그대로 UMA로 에너지/힘 계산
- `fmax`: 초기 구조의 최대 원자 힘 (eV/Å)
  - 낮을수록 DFT 구조가 UMA 에너지 면에서도 이미 잘 relaxed됨을 의미

#### 1-4. UMA vc-relaxation
```python
opt = FIRE(FrechetCellFilter(atoms_relax), logfile="relax_lpscl.log")
opt.run(fmax=0.02, steps=200)
```
| 항목 | 설명 |
|------|------|
| `FIRE` | Fast Inertial Relaxation Engine 최적화 알고리즘 |
| `FrechetCellFilter` | 원자 좌표 + 격자 벡터 동시 최적화 (vc-relax 동등) |
| `fmax=0.02` | 수렴 기준: 모든 원자 힘 < 0.02 eV/Å |

#### 1-5. 결과 비교 및 저장
```python
write("LPSCl_UMA_relaxed.cif", atoms_relax)
```
- 격자상수 오차 계산: `|a_UMA - a_DFT| / a_DFT × 100 (%)`
- UMA relaxed 구조를 CIF로 저장 → **Script 2의 입력 구조**

### 실행 결과 (검증 완료)
```
격자상수 DFT  : 10.0960 Å
격자상수 UMA  : 10.1198 Å
오차          : 0.236 %  ✅ (< 1% 기준 만족)
E/atom        : -3.8528 eV/atom
ΔE (relax)    : -2.9458 eV
```

---

## Script 2 — md_lpscl.py

### 목적
MLIP-MD (UMA가 힘 계산)로 고온 MD를 수행하여 Li 이온 확산계수와 이온전도도를 추정한다.

> **MLIP-MD vs AIMD 비교**
> | | AIMD | MLIP-MD |
> |--|------|---------|
> | 힘 계산 | DFT (QE/VASP) | UMA (신경망) |
> | 시간 스케일 | ~수 ps | ~수십~수백 ps |
> | 속도 | 느림 | **100~1000× 빠름** |
> | 정확도 | Ground truth | DFT 수준 근사 |

### 코드 설명

#### 2-1. 구조 및 모델 로드
```python
atoms = read("LPSCl_UMA_relaxed.cif")  # Script 1 출력 사용
predictor = pretrained_mlip.get_predict_unit("uma-s-1p2", device="cuda")
calc = FAIRChemCalculator(predictor, task_name="omat")
```
- Script 1에서 UMA로 relaxed된 구조를 입력으로 사용
- UMA 에너지 면에서 이미 최적화된 구조 → MD 초기 불안정성 최소화

#### 2-2. Li 인덱스 추출
```python
li_indices = [i for i, s in enumerate(atoms.get_chemical_symbols()) if s == 'Li']
```
- MSD 계산 시 Li 원자만 추적 (P, S, Cl는 골격 원자로 거의 이동 안 함)
- 총 24개 Li 원자

#### 2-3. MD 파라미터 설정
```python
TEMPS = [600, 800, 1000]  # K
dt = 2.0 * units.fs       # 시간 간격
equil_steps = 2500        # 5 ps equilibration
prod_steps  = 25000       # 50 ps production
```
| 파라미터 | 값 | 이유 |
|----------|-----|------|
| 온도 | 600, 800, 1000 K | 고온에서 충분한 확산 관측 후 300K 외삽 |
| dt | 2 fs | 일반적 MLIP-MD 시간간격 (안정성-효율 균형) |
| equil | 5 ps | 온도 평형화 |
| prod | 50 ps | 통계적으로 충분한 MSD 계산 구간 |

#### 2-4. Langevin NVT MD
```python
dyn = Langevin(at, timestep=dt, temperature_K=T, friction=0.01/units.fs)
```
- **Langevin thermostat**: NVT 앙상블 (온도 일정)
- `friction=0.01/fs`: 열욕(heat bath)과의 결합 세기
  - 너무 크면 dynamics가 damped → 확산 과소평가
  - 너무 작으면 온도 제어 불안정
  - 0.01/fs는 고체전해질 MD의 표준값

#### 2-5. 궤적 저장
```python
traj = Trajectory(traj_file, 'w', at)
dyn.attach(traj.write, interval=10)  # 10 steps = 20 fs마다 저장
```
- 20 fs 간격으로 저장 → 총 2,500 프레임 (50 ps)
- 저장 파일: `md_600K.traj`, `md_800K.traj`, `md_1000K.traj`

#### 2-6. MSD (Mean Square Displacement) 계산
```python
positions = np.array([t.get_positions()[li_indices] for t in traj_read])
for i in range(1, n_frames):
    disp = positions[i] - positions[0]
    msd[i] = np.mean(np.sum(disp**2, axis=1))
```
- **MSD(t) = ⟨|r(t) - r(0)|²⟩**: 시간에 따른 Li 원자 평균 변위 제곱
- shape: `(n_frames, n_Li, 3)` → 각 Li의 xyz 변위 → 평균
- 후반 2/3 구간으로 선형 fit (초기 탄도 구간 제외)

> ⚠️ **주의**: PBC(주기적 경계조건) 처리가 없어 Li가 셀 경계를 넘을 때 오차 발생 가능. 정확한 분석은 `unwrap_positions` 적용 필요 (추후 개선).

#### 2-7. 확산계수 D 계산
```python
slope, intercept = np.polyfit(times[fit_start:], msd[fit_start:], 1)
D = slope / 6.0  # Å²/ps
D_cm2s = D * 1e-16 / 1e-12  # cm²/s
```
**Einstein 관계식 (3D)**:
$$MSD(t) = 6Dt$$
$$D = \frac{1}{6} \frac{d\langle|r(t)-r(0)|^2\rangle}{dt}$$

단위 변환:
$$1 \text{ Å}^2/\text{ps} = \frac{10^{-16} \text{ cm}^2}{10^{-12} \text{ s}} = 10^{-4} \text{ cm}^2/\text{s}$$

#### 2-8. 이온전도도 σ 계산 (Nernst-Einstein)
```python
n_density = n_Li / vol   # cm⁻³
sigma = n_density * q**2 * D_cm2s / (k * T)
```
**Nernst-Einstein 방정식**:
$$\sigma = \frac{n q^2 D}{k_B T}$$

| 기호 | 의미 | 값 |
|------|------|-----|
| n | Li 수밀도 (cm⁻³) | 24 / V_cell |
| q | 전하 | 1.602 × 10⁻¹⁹ C |
| D | 확산계수 (cm²/s) | MD에서 추출 |
| k_B | Boltzmann 상수 | 1.381 × 10⁻²³ J/K |
| T | 온도 (K) | 600 / 800 / 1000 |

> ⚠️ **Haven ratio** (H_R) 미적용. 정확한 σ는 `σ_actual = H_R × σ_NE` (H_R ≈ 0.3~1.0 for argyrodites)

#### 2-9. Arrhenius 외삽 → 300K
```python
slope_arr, intercept_arr = np.polyfit(inv_T, ln_D, 1)
Ea = -slope_arr * 8.617e-5   # eV
D_300K = np.exp(intercept_arr + slope_arr / 300)
```
**Arrhenius 관계식**:
$$D(T) = D_0 \exp\left(-\frac{E_a}{k_B T}\right)$$
$$\ln D = \ln D_0 - \frac{E_a}{k_B} \cdot \frac{1}{T}$$

- `1/T` vs `ln D` 선형 fit → slope = -E_a/k_B
- 300K에서 외삽 → 실온 이온전도도 추정

### 출력 파일
| 파일 | 내용 |
|------|------|
| `md_600K.traj` | 600K MD 궤적 (ASE binary) |
| `md_800K.traj` | 800K MD 궤적 |
| `md_1000K.traj` | 1000K MD 궤적 |
| `msd_600K.dat` | time(ps) vs MSD(Å²) |
| `msd_800K.dat` | time(ps) vs MSD(Å²) |
| `msd_1000K.dat` | time(ps) vs MSD(Å²) |
| `uma_md_results.txt` | D, σ, Ea, 300K 외삽값 |

---

## 주요 물리 공식 정리

### Einstein 관계식
$$D = \frac{1}{6} \lim_{t \to \infty} \frac{d}{dt} \langle |r(t) - r(0)|^2 \rangle$$

### Nernst-Einstein
$$\sigma = \frac{nq^2D}{k_BT}$$

### Arrhenius
$$\sigma T = A \exp\left(-\frac{E_a}{k_BT}\right)$$

### 단위 변환
$$1 \text{ Å}^2/\text{ps} = 10^{-4} \text{ cm}^2/\text{s}$$

---

## 결과 해석 기준

### 격자상수 오차 (Script 1)
| 오차 | 평가 |
|------|------|
| < 1% | ✅ 우수 — MD 진행 가능 |
| 1~2% | ⚠️ 양호 — 주의 필요 |
| > 2% | ❌ 불량 — 모델 재검토 |

### 이온전도도 σ (Script 2)
| 값 | 평가 |
|----|------|
| ~10⁻³ S/cm | ✅ 실험값 수준 (Li₆PS₅Cl 문헌값) |
| 10⁻⁴~10⁻³ S/cm | ✅ 합리적 |
| < 10⁻⁵ S/cm | ⚠️ 과소평가 의심 (MD 시간 부족) |

### 활성화 에너지 Ea
| 값 | 평가 |
|----|------|
| 0.1~0.2 eV | ✅ argyrodite 문헌 범위 |
| > 0.3 eV | ⚠️ 과대평가 의심 |

---

## 실행 명령어 모음

```bash
# 서버 접속
ssh -i NVIDIA_A40_20260309_102904.pem -p 22 ubuntu@machine.runyour.ai

# Script 1: DFT vs UMA 검증
python validate_lpscl.py

# Script 2: MLIP-MD (백그라운드 실행)
nohup python -u md_lpscl.py > md_output.log 2>&1 &
tail -f md_output.log

# 프로세스 확인
ps aux | grep md_lpscl

# 결과 확인
cat uma_md_results.txt
```

---

## 향후 개선 사항

- [ ] PBC unwrapping 적용 (MSD 정확도 향상)
- [ ] Haven ratio 보정 (σ 정확도 향상)
- [ ] Supercell 확장 (2×2×2) → 통계 개선
- [ ] LPSCl₁.₆ (할로겐 rich) 동일 분석 → Nd₂O₃ doping 효과 비교
- [ ] production time 연장 (50 ps → 200 ps)
- [ ] NVE 앙상블로 전환 (Langevin friction 영향 제거)

---

#UMA #MLIP #LPSCl #argyrodite #ionic-conductivity #MLIP-MD #MSD #Arrhenius #fairchem #BML
