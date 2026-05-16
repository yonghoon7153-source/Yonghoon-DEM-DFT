# ML / Automation Platform Survey

> 황화물 코팅 디지털 트윈 구축을 위한 ML/automation 플랫폼 조사 (2026 기준).
> 각 플랫폼의 장단점 + 본 프로젝트 적합도 평가.

---

## TL;DR — 추천 스택

| Layer | 도구 | 이유 |
|-------|------|------|
| **워크플로우 엔진** | **atomate2** + jobflow | UMA, MACE, CHGNet, M3GNet 등 MLIP 직접 지원 (2025 update) |
| **MLIP** | **UMA-s-1p1** (FAIRChem) | 본 연구 검증됨 (R=+0.989). 보조로 MACE-MP-0 |
| **High-throughput 관리** | aiida-core | Provenance tracking + 재현성 |
| **Descriptor 계산** | dscribe + matminer | SOAP, MBTR, Magpie 등 standard ML feature |
| **Surrogate ML** | MACE 또는 SchNet | Graph NN, atomistic ML 표준 |
| **Bayesian 최적화** | scikit-optimize 또는 BoTorch | Active learning |
| **Database** | MongoDB (atomate2 기본) 또는 OPTIMADE | Materials Project 호환 |

---

## 1. 워크플로우 엔진 (High-Throughput 자동화)

### 1.1 atomate2 ⭐ 가장 추천
**Materials Project + 다양한 MLIP 직접 지원**.

- **지원 DFT**: VASP, FHI-aims, ABINIT, CP2K, QE
- **지원 MLIP**: MACE-MP-0, CHGNet, M3GNet, NequIP, SevenNet, GAP, NEP
- **워크플로우**: bulk relax, surface relax, NEB, elastic, MD, band structure, ...
- **modular**: jobflow 기반, custom workflow 작성 쉬움
- **2025년 update**로 MLIP 통합 본격화 — 본 프로젝트에 최적

**설치 + 기본 사용**:
```bash
pip install atomate2[mlff,defects,phonons]
```

**예시 — UMA 기반 relax workflow**:
```python
from atomate2.forcefields.flows.relax import RelaxMaker
from jobflow import run_locally
flow = RelaxMaker(force_field_name="UMA").make(structure)
run_locally(flow)
```

**Reference**:
- [Atomate2 paper (Digital Discovery 2025)](https://pubs.rsc.org/en/content/articlehtml/2025/dd/d5dd00019j)
- GitHub: https://github.com/materialsproject/atomate2

### 1.2 aiida-core
**Strong provenance tracking + 워크플로우 재현성**.

- **장점**: 모든 계산 자동 graph로 저장, 재현/검증 강력
- **단점**: 설정 복잡, learning curve 있음, MLIP 통합은 atomate2보다 약함
- **본 프로젝트 적합도**: 중간. atomate2와 병용 가능 (aiida-shell로 atomate2 jobs 관리).

### 1.3 FireWorks (legacy)
atomate1의 backend. atomate2로 이전 추세. 신규 프로젝트엔 atomate2 권장.

### 1.4 ASE database + custom scripts
**가장 가벼움**. 우리 현재 방식 (scripts/ 폴더).
- **장점**: 가장 빠른 prototype
- **단점**: 1000+ 후보 screening 시 한계
- **본 프로젝트 적합도**: POC 단계만 적합. Scale-up 시 atomate2로 이전.

---

## 2. MLIP (Energy/Force Backend)

### 2.1 UMA-s-1p1 (FAIRChem) ⭐ 본 연구 검증됨
- **검증**: R=+0.989 vs paper W_ad (5 argyrodite-NCM 시스템)
- **장점**: universal (모든 원소), DFT 정확도 근접, GPU 가속
- **task_name='omat'**: 산화물/황화물 적합
- **License**: open (Meta FAIR)

### 2.2 MACE-MP-0 (또는 MACE-OFF)
- **장점**: 정확도 매우 높음, message-passing 기반, foundation model
- **본 프로젝트 활용**: surrogate ML 학습 baseline, UMA 결과와 cross-check
- **License**: MIT

### 2.3 CHGNet, M3GNet
- **장점**: Materials Project 데이터로 학습, 빠름
- **단점**: 황화물 정확도 UMA보다 낮음 (typically)
- **본 프로젝트 활용**: quick screening 단계 (Tier-1 pre-filter)

### 2.4 NequIP, Allegro
- **장점**: 매우 정확 (equivariant), system-specific training 가능
- **단점**: foundation model 아님, retrain 필요
- **본 프로젝트 활용**: 우리 system 특화 모델 학습 (Phase 2)

### 2.5 SevenNet, NEP
신규 MLIP들. atomate2가 지원. 검토 대상.

---

## 3. Descriptor 계산 도구

### 3.1 dscribe ⭐
**Atomic environment descriptors** (SOAP, MBTR, ACSF, ...).
```python
from dscribe.descriptors import SOAP
soap = SOAP(species=["Li", "P", "S", "Cl", "Br", "Ni", "Co", "Mn", "O"], ...)
features = soap.create(atoms)
```
- 본 프로젝트: 5 comp + 도핑 변형들에 대한 ML feature 추출.

### 3.2 matminer ⭐
**Composition + structural descriptors** (Magpie, Meredig, ...).
- composition만으로 빠른 screening (Tier-0 pre-filter).
- Materials Project, Citrine integration.

### 3.3 pymatgen
**구조 분석 + 다양한 utility**. 기본 의존성.

---

## 4. Surrogate ML 모델 (Layer 2)

### 4.1 MACE / Allegro (graph NN)
**Layer 1 (UMA) 데이터로 학습 → 더 빠른 surrogate**.
- 우리 system 특화 학습 가능 (transfer learning)

### 4.2 Modnet
**Materials property prediction (composition + structure)**.
- W_ad, σ, Eg 등 multi-target.

### 4.3 GBT / Random Forest
**Quick interpretable baseline**.
- xgboost, lightgbm, scikit-learn.
- 검증된 descriptors (Cl-O, S-O, Li-O 등)을 input으로 R 검증.

### 4.4 ALIGNN, GATGNN, CGCNN
Materials-specific graph NN. 옵션.

---

## 5. Active Learning / Bayesian 최적화

### 5.1 scikit-optimize (skopt)
**가장 가벼움**. Bayesian optimization, Gaussian process.

### 5.2 BoTorch + Ax
**Facebook AI 기반**. Multi-objective Pareto front 잘 됨.
- 본 프로젝트: W_ad + σ + 비용 + 안정성 → 다목적 최적화.

### 5.3 modAL
Active learning framework. 후보 query strategy 다양.

### 5.4 dragonfly
Bayesian opt with discrete + continuous variables.

---

## 6. Database / Provenance

### 6.1 MongoDB (atomate2 기본)
워크플로우 결과 자동 저장.

### 6.2 OPTIMADE
**Materials database 표준 API**. Materials Project, NOMAD, MPDS 등과 연동.
- 본 프로젝트: 외부 DB에서 도핑 후보 organisms fetch.

### 6.3 NOMAD
오픈 데이터 저장소. 우리 결과 공유 가능.

### 6.4 H5 / Apache Parquet
Local 저장. 1000+ 후보 결과 분석 시.

---

## 7. 추천 종합 아키텍처

```
┌────────────────────────────────────────────────────────────┐
│ Layer 3: Active Learning + Inverse Design                  │
│   BoTorch + Ax (multi-objective Pareto)                    │
│   skopt (Bayesian opt for single target)                   │
└────────────────────────────────────────────────────────────┘
                          ↑ feedback
┌────────────────────────────────────────────────────────────┐
│ Layer 2: ML Surrogate                                       │
│   MACE / Allegro (graph NN, atomate2 통합)                  │
│   modnet / GBT (composition + structure features)           │
│   Trained on Layer 1 outputs                                │
└────────────────────────────────────────────────────────────┘
                          ↑ training data
┌────────────────────────────────────────────────────────────┐
│ Layer 1: UMA-s-1p1 (검증됨)                                 │
│   atomate2 workflow orchestration                           │
│   ase + pymatgen + dscribe + matminer for descriptors       │
│   MongoDB for results storage                               │
└────────────────────────────────────────────────────────────┘
                          ↑ occasional spot-check
┌────────────────────────────────────────────────────────────┐
│ Foundation: DFT (VASP/QE)                                   │
│   atomate2-VASP for new chemistry validation                │
│   ~10 calculations/year                                     │
└────────────────────────────────────────────────────────────┘
```

---

## 8. Phase별 도입 계획

### Phase 1 (POC, 3-6개월)
- atomate2 설치 + UMA workflow 구축
- 우리 검증된 scripts/adhesion/ 을 atomate2 module로 wrap
- 100 LPSCl 도핑 후보 자동 screening
- dscribe + matminer로 descriptor 계산
- MongoDB로 결과 저장
- **목표**: 100 candidates, 본 검증 5개 + 95개 신규

### Phase 2 (Scale-up, 6-12개월)
- MACE surrogate 학습 (Layer 1 데이터로)
- Active learning loop (BoTorch + Ax)
- 10,000 후보 screening
- **목표**: 다목적 최적 후보 top-10

### Phase 3 (Production, 12-24개월)
- DFT validation (atomate2-VASP)
- 실험 파트너 partnership
- Literature DB 통합 (다음 문서 참고)
- Inverse design (generative model)
- **목표**: Production-ready 디지털 트윈 플랫폼

---

## 9. 학습 자료

### atomate2
- [Paper (Digital Discovery 2025)](https://pubs.rsc.org/en/content/articlehtml/2025/dd/d5dd00019j)
- [GitHub](https://github.com/materialsproject/atomate2)
- [Documentation](https://materialsproject.github.io/atomate2/)
- Tutorial: Materials Project Workshop (annual)

### UMA / FAIRChem
- [FAIRChem GitHub](https://github.com/FAIR-Chem/fairchem)
- UMA paper / model card

### MACE
- [MACE GitHub](https://github.com/ACEsuit/mace)
- [MACE-MP-0 model card](https://github.com/ACEsuit/mace-mp)

### Active Learning
- [BoTorch tutorials](https://botorch.org/tutorials/)
- [Ax platform](https://ax.dev/)

---

## Sources

- [Atomate2 paper (RSC Digital Discovery 2025)](https://pubs.rsc.org/en/content/articlehtml/2025/dd/d5dd00019j)
- [Atomate2 GitHub](https://github.com/materialsproject/atomate2)
- [PMC: Convergence of Computational Materials Science and AI](https://link.springer.com/article/10.1007/s11664-025-12511-4)
- [Materials Genome Engineering Advances (2023)](https://onlinelibrary.wiley.com/doi/full/10.1002/mgea.11)
