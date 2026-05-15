# TIMELOG

> 시간순 작업 로그. 자세한 결과는 `kb/` 폴더 참조.

---

## 2026-05-15

### 19:30 — Kickoff: 디지털 트윈 ML 플랫폼 프로젝트 본격 시작

**전환점**: 단발 paper 검증 → 장기 디지털 트윈 platform 프로젝트로 확장.

**Repo 구조 전면 재정비**:
- 새 디렉토리 구조 (`kb/{papers,descriptors,platforms,methodology,projects}/`,
  `scripts/{adhesion,doping,descriptors,automation}/`, `archive/`)
- README.md 새로 작성 (project bible)
- 검증된 scripts 7개 → `scripts/adhesion/` (재사용 가능)
- Deprecated scripts 8개 → `archive/deprecated_scripts/`

**Foundation 문서 5개 신규 작성**:
- `kb/descriptors/coating_descriptor_catalog.md` — 60+ descriptor 카탈로그,
  Tier-1 (Cl-O, S-O, Li-O) ★ 검증됨 표시
- `kb/platforms/ml_automation_platforms.md` — atomate2, MACE, UMA, BoTorch
  추천 stack + 설치 가이드
- `kb/platforms/literature_db_tools.md` — OpenAlex + Semantic Scholar
  + chroma DB 기반 "Bible" 구축 방법
- `kb/methodology/doping_substitution_algorithm.md` — LPSCl 5 사이트
  (Li/P/S_4a/S_16e/Cl_4d) 도핑 알고리즘 + 후보 dopant 가이드
- `kb/projects/digital_twin_roadmap.md` — Phase 0-4 (24-36개월) 로드맵
  + KPI + 리스크 매트릭스

**핵심 stack 결정** (다음 phase에서 도입):
- Workflow: atomate2 + jobflow
- MLIP Layer 1: UMA-s-1p1 (이미 검증)
- MLIP Layer 2: MACE (transfer learning surrogate)
- Active learning: BoTorch + Ax (multi-objective)
- Literature: OpenAlex + Semantic Scholar + chroma (semantic search)
- AI 요약: Claude API

**다음 단계 (Phase 1, 3-6개월)**:
1. atomate2 설치 + UMA workflow 테스트
2. `scripts/doping/site_preference.py` 구현
3. 100 LPSCl 도핑 후보 자동 screening
4. literature harvest script (OpenAlex)

---

## 2026-05-14 (Day-long sprint)

### 19:00 — Paper mechanism MD 최종 완성

**핵심 결과** (Section 4-7, `kb/papers/mechanism_anion_O_descriptor.md`):
- UMA W_ad가 paper 5/5 strict rank 재현 (R=+0.989, ρ=+1.000)
- 3대 표면 contact driver:
  - Cl-O density R=+0.975 (Cl-Li-O 가교)
  - S-O density R=−0.973 (S²⁻-O²⁻ Pauli)
  - Li-O density R=+0.771 (universal attraction)
- Family 분리: Li-vacancy migration Li₅.₄ +0.58 vs Li₆ +0.22 (2.6×)
- Family 내부: bulk Cl 함량 R=+0.97 (subsurface Madelung)
- 할로겐 깊이: Cl<1Å 표면, Br>5Å 벌크 (literature 일관)

**Cherry-pick defense 7-axis convergence**:
- Bond density (3 drivers) ✓
- Vacancy migration ✓
- Bulk Cl regression ✓
- Halogen depth ✓
- α robustness [0.8, 1.5] ✓
- Li-O cutoff robustness [2.4, 3.6] Å ✓
- Slab dataset v1 vs v2 ✓

**Literature support 추가**:
- Strauss 2023 (Cl surface LiCl nanoparticles)
- Science 2024 (universal halide segregation)
- Schwöbel 2016 (Li2S termination standard)
- Sufyan 2024 (argyrodite (001) Li2S exposure)
- Stamminger 2020 (anion site disorder 4a/4d)

### 18:00 — Bond density 36-reg vectorized + Li-O cutoff sensitivity
- `bond_density_36reg_FAST.py`: 1.7초 (vs 10분 non-vectorized)
- Cl-O R=+0.975, S-O R=−0.973 확립
- 이전 P-O killer 가설 폐기 (single-config artifact였음)
- Li-O cutoff [2.4, 3.6] Å sweep: R 항상 양수, plateau [2.8, 3.4]

### 17:00 — Vacancy migration 5-comp face A 통일
- Li6 ΔW_ad(N=3) = +0.22 (평균), Li5.4 = +0.58 (평균)
- 2.6배 family gap이 binding well 깊이 family 비율과 일치

### 14-16 — Paper figure 완성 + α sensitivity
- `plot_R0988_TIGHT_FIT.py`: 7-start global Morse fit
- α robustness: uniform Li5.4 dW=0.44에서 α ∈ [0.8, 1.5] strict rank
- Per-comp dW (eiso fix)는 어떤 α에서도 rank 안 맞음

### 09-13 — Final combo 결정 + figure
- 5 comp Cl-coherent termination 선택 (R=+0.989, ρ=+1.000)
- comp1 face A, comp2 face A, comp3 preShift_B, comp4 shift2_B, comp5 shift2_A
- Halogen depth로 자연 표면 정렬 입증
- 640 face combo enumeration

---

## 이전 (요약)

- v1 face_flip face A 조합 BBABA: R=+0.908, ρ=+0.900
- v2 z-shift sweep: shift 2 = Cl/Cl 공통 종단
- comp4_v2 cell anomaly 발견 (4% 압축, 50:50 Cl/Br frustration)
- Uniform Li5.4 dW=0.44 채택 결정
- bond density killer descriptor 가설 (P-O, 나중에 폐기)
