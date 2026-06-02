# Phase 1 Quickstart Guide

> 본 repo의 첫 Phase 1 작업 가이드. atomate2 + UMA + doping screening
> POC (100 후보) 시작.

---

## Prerequisites (이미 설치 완료)

```bash
pip install atomate2[mlff,defects,phonons] pyalex semanticscholar dscribe matminer
```

GPU + UMA-s-1p1 (FAIRChem) 가용 가정.

---

## 1단계: Doping site preference 첫 분석 (즉시, 5분)

```bash
# 단일 dopant 평가
python3 scripts/doping/site_preference.py --dopant Mg --n 2

# 알려진 모든 dopant 평가 (29개)
python3 scripts/doping/site_preference.py \
    --batch scripts/doping/dopant_candidates.json \
    --out data/doping_screening/site_preference_initial.json
```

**출력**:
- 각 dopant별 compatible substitution site
- Charge compensation 방법 (isovalent / donor / acceptor)
- 호환성 score (radius + charge)

→ Tier-1 filter 결과 → 다음 단계에서 UMA로 검증할 후보 좁힘.

---

## 2단계: Literature harvest (10-30분, 인터넷 필요)

```bash
# Default 키워드로 ~500 paper 수집
python3 scripts/automation/literature_harvest.py --max 30 --max-s2 20

# 또는 OpenAlex만 빠르게 (S2 rate limit 회피)
python3 scripts/automation/literature_harvest.py --no-s2 --max 50
```

**출력**: `kb/literature_db/raw.json` — paper 메타데이터 DB

다음 step (구현 예정):
- `scripts/automation/auto_summary.py` — Claude API로 한국어 요약
- `scripts/automation/build_semantic_db.py` — chroma DB 구축

---

## 3단계: atomate2 + UMA workflow 테스트 (확인용)

```python
# 첫 atomate2 + UMA test (다음에 작성할 스크립트)
from atomate2.forcefields.flows.relax import RelaxMaker
from atomate2.forcefields.jobs import ForceFieldRelaxMaker
from jobflow import run_locally
from ase.io import read
from pymatgen.io.ase import AseAtomsAdaptor

# LPSCl 구조 로드
atoms = read("data/lpscl_structure.xyz")  # 추가 필요
struct = AseAtomsAdaptor.get_structure(atoms)

# UMA relax
maker = ForceFieldRelaxMaker(force_field_name="UMA")
flow = maker.make(struct)
result = run_locally(flow)
print(f"Relaxed energy: {result['output'].output.energy}")
```

**확인**: UMA가 atomate2에 통합되어 동작함 → Phase 1 production-ready.

---

## 4단계: 100 후보 doping screening (구현 예정)

```bash
# scripts/doping/run_screening.py (다음에 작성)
python3 scripts/doping/run_screening.py \
    --candidates data/doping_screening/site_preference_initial.json \
    --concentrations 0.05 0.10 0.20 \
    --output data/doping_screening/uma_results.json
```

각 후보별 UMA relax → energy → Tier-1 descriptors 자동 계산.

---

## 5단계: 결과 분석 + Top-10 보고

```bash
# scripts/doping/analyze_screening.py (다음에 작성)
python3 scripts/doping/analyze_screening.py \
    --input data/doping_screening/uma_results.json \
    --paper-validation 5  # paper 검증 5개 sanity check
```

**Expected**: paper 검증 5 comp + 신규 95 후보의 Tier-1 ranking.

---

## 다음 implementation TODO

- [ ] `scripts/doping/substitute_struct.py` — LPSCl 구조에 dopant 삽입 (pymatgen)
- [ ] `scripts/doping/run_screening.py` — atomate2 workflow
- [ ] `scripts/descriptors/compute_tier1.py` — 36-reg bond density automated
- [ ] `scripts/automation/auto_summary.py` — Claude API literature summary
- [ ] `scripts/automation/build_semantic_db.py` — chroma DB for semantic search

---

## 참고

전체 로드맵: `kb/projects/digital_twin_roadmap.md`
디스크립터 catalog: `kb/descriptors/coating_descriptor_catalog.md`
ML 플랫폼 stack: `kb/platforms/ml_automation_platforms.md`
Literature 도구: `kb/platforms/literature_db_tools.md`
도핑 알고리즘: `kb/methodology/doping_substitution_algorithm.md`
