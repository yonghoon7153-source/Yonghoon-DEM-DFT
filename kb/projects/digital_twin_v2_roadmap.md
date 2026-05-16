# Argyrodite Digital Twin Network — Long-term Vision (v2 roadmap)

> "엄청난 데이터베이스를 기반으로 한 딥러닝을 통한 디지털 트윈 네트워크 구축"
> 구조만으로 전기화학적 성능까지 예측. 기계·전기·화학 복합 학습.
> — 2026-05-16, 사용자 비전

이전 v1 (`archive/digital_twin_phase_2026_05/digital_twin_roadmap.md`) 은
일반 platform 기반 계획이었지만 chemistry foundation이 약했음. **v2 = 우리
도핑 파이프라인의 검증된 chemistry를 deep learning으로 일반화**.

---

## ★ 핵심 통찰 (2026-05-16) — 데이터 hierarchy 그대로가 model tier

cascade 자체가 자연스러운 ML tier 구조를 만든다:

| Tier | 데이터 출처 | 데이터 양 | Target |
|------|------------|-----------|--------|
| 1 | screen + anneal | ~ 모든 구조 (n ~ 1000+) | ΔE/atom (stability) |
| 2 | EOS + elastic + BVSE | per-winner (n ~ 100) | B₀, E_young, σ_proxy |
| 3 | DFT (외부 실행) | top-K (n ~ 10) | 정확한 band/Bader/COHP |

**진정한 의의**: tier-1은 *MLIP 데이터만으로 학습 가능*. DFT가 필요 없다. 결과
는 새 후보를 *Tier-1 통과 → Tier-2 예측 → Tier-3 (DFT) 추천* 하는 가벼운
조회 시스템. `chain_predict.py`가 이 게이트를 자동화함.

논문 시점: tier-1 만으로도 SE 도핑 screening의 SOTA가 될 가능성 큼 — 기존
heavy DFT 워크플로우 대비 1000× 빠른 ML 예측.

---

## Phase 1 — Foundation (✅ 완성, 2026-05-16)

`tools/doping/` 16-step factory line + 자동 cascade (`tier_cascade.sh`)

- **데이터 생성**: ~85 compound × 9 sites × 5 seeds × multi-supercell ≈
  수천 구조의 MLIP-relax + EOS + elastic + BVSE 자동 산출
- **데이터 수집**: `collect_dataset.py` → CSV 한 줄당 30+ 컬럼
- **1차 예측기**: `train_predictor.py` (sklearn GBR, per-target)
- **즉시 평가**: `predict_new.py` — 새 (compound, sites, conc) 조합을
  cold-start (chemistry 라벨만) 또는 with-structure (BVSE 1분) 으로 예측
- **Tier-4 bridge**: `generate_dft_inputs.py` — Top-N → QE 인풋

**현재 수준 비유**: 도공 한 명이 매번 손으로 굽는 단계 → 컨베이어 벨트 도입
완료.

---

## Phase 2 — Multi-task Graph Neural Network (계획)

`tools/doping/dgn_predictor/` (TODO)

데이터 ≥10k 구조 모이면 sklearn 한계 → graph neural network 도입.

| 항목 | 선택지 |
|------|--------|
| Architecture | **ALIGNN** (atom + line graph, 정확도 SOTA) 또는 **M3GNet** (energy + force + property) |
| Input | crystal structure (pymatgen Structure) |
| Output (multi-head) | ΔE/atom, B₀, E_young, Pugh G/B, BVSE proxy, σ_Li (proxy) |
| Loss | weighted multi-task L1 + uncertainty calibration |
| Training | transfer learning from MP-trained checkpoint → fine-tune on our cascade dataset |
| Compute | A100 단일 GPU, ~2 일 학습 |

**의의**: composition + sites + concentration → 모든 물성 한 번에 예측.
새 chemistry 도입 시 처음부터 retrain 안 하고 fine-tune만.

---

## Phase 3 — Process-aware predictor (장기)

지금까지 = ideal lattice 구조만. 실제 합성 차이 반영 필요.

| 추가 input | 의미 |
|-----------|------|
| Synthesis method (ball mill / wet / sintering) | porosity, grain boundary 분포 |
| Particle size (nm) | grain interior vs surface 비율 |
| Annealing T / time | site disorder 정도 |
| Post-processing (sintering pressure) | density |

이 input들이 들어가면 **합성 protocol 입력 → 실측 σ_Li / B₀ 예측** 가능.
Sundar 2025 같은 coating screen + 우리 bulk doping을 함께 다루는 single
predictor 가능.

---

## Phase 4 — Electrochemical property bridge

물성 (B₀, E_young, σ) → 셀 레벨 (CCD, cycle life) 예측까지 확장.

실험 데이터셋 필요 (NEI commercial 제품, 우리 그룹 historical results,
Argonne open data 등 통합).

**최종 목표 모델**:
```
(composition + sites + synthesis condition)
   → (B₀, E, σ_Li, bandgap, ΔE_decomp, Wad with NCM)
   → (CCD, cycle life, polarization)
```

---

## 기술 스택

| Layer | 도구 |
|-------|------|
| Crystal representation | pymatgen Structure |
| GNN | ALIGNN-FF or M3GNet (transfer from Materials Project pretrain) |
| MLIP for data generation | UMA-s-1p1 (current), DPA-SSE (sulfide-specialized, Wang 2025) |
| Training | PyTorch + PyG, A100 GPU |
| MLOps | Weights & Biases (experiment tracking), DVC (dataset versioning) |
| Deployment | gradio web UI for interactive prediction |
| Validation | DFT spot-check (Tier-4) for top candidates |

---

## 즉시 활용 (이번 batch 끝나면 가능한 것)

1. **paper #2 (Nd₂O₃)**: cascade에 Nd₂O₃ 다양한 site 결과 + ML 예측 vs
   KISTI DFT 결과 비교 → 모델 calibration
2. **Sundar 2025 cross-validation**: 그들의 Top-3 (MgO/Al₂O₃/ZnO)이 우리
   ranking 어디 있는지 + DFT 검증
3. **새 chemistry 즉시 예측**: 예) "Eu₂O₃ at Li_24g + Cl-rich x=0.5 이거
   좋아?" → `predict_new.py` 0.1초 답변

---

## Repo 진화 로드맵

| 시점 | 마일스톤 |
|------|----------|
| **2026-05-16** | Phase 1 완성 (✅ 현재 commit) |
| ~2026-06 | 첫 cascade batch 1주일 run → 데이터 ~수천 구조 + 첫 GBR predictor |
| ~2026-07 | paper #2 draft (Nd-doped LPSCl, DFT 검증) |
| ~2026-09 | Phase 2 GNN predictor v1 (transfer from ALIGNN/M3GNet) |
| ~2026-12 | Phase 2 with diverse compound classes → 1만+ 구조 데이터 |
| ~2027 | Phase 3 process-aware model |
| ~2028 | Phase 4 cell-level prediction, paper "argyrodite digital twin" |

---

**파일 진입점**:
- `tools/doping/tier_cascade.sh` — 메인 entry
- `kb/methodology/doping_pipeline_critical_review.md` — 현재 한계 + TODO
- `kb/methodology/argyrodite_mechanical_pipeline.md` — 8-step 정량 reference
- `db/literature/` — 10편 핵심 문헌 (Pustorino, D'Amore, Sundar, Yu, Adeli,
  Kraft, Pham, Wang LiBH4, Adams BVSE)

**작성**: 2026-05-16
**상태**: Phase 1 완성, Phase 2 GNN 다음 라운드 시작
