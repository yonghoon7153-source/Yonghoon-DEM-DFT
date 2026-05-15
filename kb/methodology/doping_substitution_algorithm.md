# LPSCl 도핑 / 치환 알고리즘

> Li₆PS₅Cl (LPSCl) 기반 cation/anion 치환에서 어느 site에 어떤 dopant가
> 들어갈지 자동 결정하고, 모든 경우를 UMA로 평가하는 알고리즘 설계.

---

## 0. 핵심 — Argyrodite의 site 구조

LPSCl 단위격자 (cubic F-43m):

| Site | 점유 (표준) | Wyckoff | Local 환경 | 표면 vs Bulk |
|------|------------|---------|------------|--------------|
| **Li⁺** | Li, partial | 24g / 48h | tetrahedral coordination | distributed |
| **P⁵⁺** | P | 4b | PS₄³⁻ 중심 | bulk |
| **S²⁻ (bonded)** | S in PS₄ | 16e | P-S 공유결합 | bulk |
| **S²⁻ (free)** | S | **4a** | Li 6개 octahedral | **(001) cleavage 평면 = 표면** |
| **Cl⁻** | Cl | **4d** | Li 4개 + PS₄ | **bulk 깊숙이** |

→ **치환 가능 site 5종**:
1. **Li 사이트** (24g/48h): cation 치환 (Na, K, Mg, Al, ...)
2. **P 사이트** (4b): pentavalent cation (Sb, As) 또는 tetravalent (Si, Ge, Sn)
3. **S(bonded) 사이트** (16e): chalcogen (Se, Te)
4. **S(free) 사이트** (4a): chalcogen 또는 halide
5. **Cl 사이트** (4d): halide (F, Br, I) 또는 chalcogen

---

## 1. Dopant 선택 가이드 (Tier-1 후보)

각 site별로 우선 평가할 dopant 후보:

### 1.1 Li 사이트 (cation 치환)

| Dopant | Charge | Radius (Å) | 효과 예상 |
|--------|-------:|-----------:|----------|
| Na⁺ | +1 | 1.02 | Li보다 큼 → 격자 팽창, 전도성 영향 |
| K⁺ | +1 | 1.38 | 더 큼, 가능성 낮음 |
| Mg²⁺ | +2 | 0.72 | aliovalent → vacancy 자동 생성 |
| Al³⁺ | +3 | 0.535 | aliovalent, 2 vacancy/Al |
| Cu⁺ | +1 | 0.77 | covalent 성격 |
| Zn²⁺ | +2 | 0.74 | Mg와 비슷, 평가 |

### 1.2 P 사이트 (PS₄ 변형)

| Dopant | Charge | Radius (Å) | 효과 예상 |
|--------|-------:|-----------:|----------|
| Sb⁵⁺ | +5 | 0.60 | isovalent, larger tetrahedron |
| As⁵⁺ | +5 | 0.46 | isovalent, smaller |
| Si⁴⁺ | +4 | 0.40 | aliovalent → defect |
| Ge⁴⁺ | +4 | 0.53 | aliovalent |
| Sn⁴⁺ | +4 | 0.69 | aliovalent, 큼 |

### 1.3 4a 사이트 (free S²⁻ 자리)

| Dopant | Charge | Radius (Å) | 효과 예상 |
|--------|-------:|-----------:|----------|
| O²⁻ | −2 | 1.40 | smaller, surface 영향 큼 |
| Se²⁻ | −2 | 1.98 | larger, polarizable |
| Te²⁻ | −2 | 2.21 | very large, lattice expansion |
| Cl⁻ | −1 | 1.81 | aliovalent (S↔Cl swap) ← Li5.4 family |
| Br⁻ | −1 | 1.96 | aliovalent (S↔Br swap) ← Li5.4 family |
| F⁻ | −1 | 1.33 | smaller halide |
| I⁻ | −1 | 2.20 | larger halide, polarizable |

### 1.4 4d 사이트 (Cl⁻ 자리)

| Dopant | Charge | Radius (Å) | 효과 예상 |
|--------|-------:|-----------:|----------|
| Br⁻ | −1 | 1.96 | LPSBr family |
| I⁻ | −1 | 2.20 | LPSI family, 큰 lattice |
| F⁻ | −1 | 1.33 | small, frustration 가능 |
| O²⁻ | −2 | 1.40 | aliovalent, oxysulfide |
| N³⁻ | −3 | 1.46 | aliovalent, nitride |

---

## 2. Site preference 결정 알고리즘

새 dopant가 LPSCl에 들어갈 때 **어느 site로 갈지 자동 판단** 방법:

### 2.1 1차 필터 (이온 크기 + 전하)

```python
def site_preference_filter(dopant, charge, radius):
    """Returns list of compatible sites based on simple rules."""
    candidates = []
    sites = {
        'Li_24g':   {'host': 'Li',  'host_charge': +1, 'host_radius': 0.76, 'tol_radius': 0.30},
        'P_4b':     {'host': 'P',   'host_charge': +5, 'host_radius': 0.17, 'tol_radius': 0.30},
        'S_16e':    {'host': 'S',   'host_charge': -2, 'host_radius': 1.84, 'tol_radius': 0.20},
        'S_4a':     {'host': 'S',   'host_charge': -2, 'host_radius': 1.84, 'tol_radius': 0.40},
        'Cl_4d':    {'host': 'Cl',  'host_charge': -1, 'host_radius': 1.81, 'tol_radius': 0.40},
    }
    for site_name, info in sites.items():
        # 전하 호환성: 같은 부호
        if charge * info['host_charge'] <= 0:
            continue
        # 반지름 호환성: tolerance 이내
        if abs(radius - info['host_radius']) > info['tol_radius']:
            continue
        candidates.append(site_name)
    return candidates
```

### 2.2 2차 필터 (Charge balancing)

Aliovalent dopant (예: Mg²⁺ on Li⁺) 도입 시 charge balance 위한 추가 변화:
- Mg²⁺ on Li⁺: 1 extra +charge → 1 Li vacancy or 1 anion charge increase 필요
- F⁻ on S²⁻: -1 less charge → 1 cation vacancy or H⁺ proton 필요

**알고리즘**:
```python
def charge_balance(host_charge, dopant_charge, n_dopant):
    delta_q = (dopant_charge - host_charge) * n_dopant
    if delta_q == 0:
        return {'compensation': 'isovalent', 'mechanism': None}
    elif delta_q > 0:
        # 양전하 과잉 → cation vacancy 또는 음전하 anion 증가
        return {'compensation': 'cation_vacancy', 'n': delta_q,
                'alternative': 'anion_substitution_higher_charge'}
    else:
        # 음전하 과잉 → anion vacancy 또는 양전하 cation 증가
        return {'compensation': 'anion_vacancy', 'n': -delta_q,
                'alternative': 'cation_substitution_higher_charge'}
```

### 2.3 3차 평가 (UMA energy)

이론적으로 가능한 모든 (site, charge compensation) 조합을 enumerate →
UMA로 substitution energy 계산 → 가장 낮은 site가 thermodynamic preference.

```python
def find_lowest_energy_site(dopant, n_dopants, lpscl_struct):
    candidates = site_preference_filter(dopant, ...)
    results = []
    for site in candidates:
        compensation = charge_balance(...)
        for comp_method in compensation['alternatives']:
            modified_struct = substitute(lpscl_struct, dopant, site, n_dopants, comp_method)
            E_modified = uma_calculator.get_potential_energy(modified_struct)
            sub_energy = E_modified - E_reference
            results.append({'site': site, 'compensation': comp_method, 'E_sub': sub_energy})
    return min(results, key=lambda x: x['E_sub'])
```

---

## 3. 자동 enumeration 알고리즘

### 3.1 Single dopant screening (1 종 도펀트)

```python
# scripts/doping/screen_single_dopant.py (구현 예정)
DOPANTS = {
    'cation_for_Li': ['Na', 'K', 'Mg', 'Al', 'Cu', 'Zn'],
    'cation_for_P':  ['Sb', 'As', 'Si', 'Ge', 'Sn'],
    'anion_for_S':   ['Se', 'Te', 'O'],
    'anion_for_Cl':  ['F', 'Br', 'I'],
    'cross_anion':   [('Cl', 'O'), ('S', 'O')],  # S↔Cl swap, ...
}

CONCENTRATIONS = [0.05, 0.10, 0.20, 0.50, 1.00]  # mole fraction

for dopant_class, dopants in DOPANTS.items():
    for d in dopants:
        for x in CONCENTRATIONS:
            site = find_lowest_energy_site(d, x, lpscl)
            # 결과 저장
```

이렇게 5 class × ~5 dopants × 5 concentrations = **125 후보** screening
(POC 단계).

### 3.2 Multi-dopant (co-doping)

```python
# scripts/doping/screen_codoping.py
# Cation + Anion 동시 도핑
PAIRS = [
    ('Mg', 'Li_24g', 'F', 'Cl_4d'),  # charge balanced co-doping
    ('Al', 'Li_24g', 'O', 'S_4a'),
    # ...
]
```

### 3.3 SQS (Special Quasi-random Structure)

Mixed compositions (예: Cl₀.₈Br₀.₂, Cl₀.₅Br₀.₅) 의 lowest-energy ordering을
찾는 표준 방법.

**도구**: pymatgen의 `SQS` module, ICET, ATAT.

본 프로젝트: comp4 (Cl=Br=0.8) 같은 frustrated 조성에서 SQS로 정확한 lowest-E
ordering 사용 → cell artifact 회피 (Section 8.4 mechanism MD 참조).

---

## 4. UMA workflow (atomate2 기반)

```python
# scripts/doping/run_doping_workflow.py (구현 예정)
from atomate2.forcefields.flows.relax import RelaxMaker
from atomate2.forcefields.jobs import ForceFieldStaticMaker
from jobflow import Flow, run_locally

def doping_screening_flow(host_struct, dopants, concentrations):
    jobs = []
    for dopant, conc in product(dopants, concentrations):
        modified = substitute(host_struct, dopant, conc, ...)
        relax_job = RelaxMaker(force_field_name="UMA").make(modified)
        descriptor_job = compute_descriptors_maker(relax_job.output.structure)
        jobs.extend([relax_job, descriptor_job])
    return Flow(jobs)

flow = doping_screening_flow(lpscl, all_dopants, all_concentrations)
run_locally(flow)
```

---

## 5. Output — Doping screening DB

각 후보별 자동 기록:
```json
{
  "dopant": "Mg",
  "site": "Li_24g",
  "concentration": 0.05,
  "compensation": "Li_vacancy",
  "relaxed_structure": "structures/Mg005_Li24g.xyz",
  "tier1_descriptors": {
    "Cl_O_density": 0.092,
    "S_O_density": 0.001,
    "Li_O_density": 0.108,
    "predicted_Wad": 0.91
  },
  "tier2_descriptors": {
    "binding_curve_well": -1.85,
    "d_eq": 1.42,
    "Wad_alpha": 1.05
  },
  "tier3_descriptors": {
    "vacancy_ΔWad": 0.55,
    "ionic_conductivity_NEB": "TBD"
  },
  "composite_score": 0.87,  # weighted Pareto
  "uma_substitution_energy_eV": -1.23,
  "rank": 7
}
```

---

## 6. Phase별 구현

### Phase 1 (POC, 1-2개월)
- [ ] `scripts/doping/site_preference.py` — Tier-1 필터
- [ ] `scripts/doping/substitute_struct.py` — 구조 생성
- [ ] `scripts/doping/run_single_dopant.py` — UMA screening 100개

### Phase 2 (Scale, 2-6개월)
- [ ] atomate2 통합
- [ ] SQS for mixed compositions
- [ ] Co-doping enumeration
- [ ] 1000 후보 screening

### Phase 3 (ML, 6-12개월)
- [ ] MACE surrogate 학습
- [ ] Active learning (BoTorch)
- [ ] 10,000 candidates

---

## 7. 참고 — 실험 partner와 협업

각 후보의 합성 가능성 평가도 중요:
- precursor 가격 (Sb, Te → 비쌈, 우선 낮음)
- 합성 온도 (oxysulfide → ambient OK; nitride → 어려움)
- 안전성 (Cd, Hg, Tl 등 toxic → 제외)

→ **screening 후보 작성 시 cost/safety filter** 미리 적용.
