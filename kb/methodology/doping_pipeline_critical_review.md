# Doping Pipeline — Critical Self-Review (2026-05-16)

기록 목적: 우리 doping pipeline (tools/doping/) 의 알려진 한계점을 명시.
새 세션에서 이 파일 + CODE_INVENTORY.md 같이 읽으면 무엇이 부족한지 즉시 파악.

`tools/doping/`: site_preference.py, substitute_struct.py, substitute_compound.py,
run_uma_screening.py, run_anneal.py, analyze_screening.py, run_compound_batch.sh

---

## A. Chemistry coverage gaps

### A1. Multi-cation 화합물 (e.g., MgAl₂O₄ spinel, LaAlO₃, LiNbO₃) — ⚠ 부분 지원
- 현재 `classify_compound` 가 모든 양이온을 **하나의 cation_site** 에 일괄 배치.
- LaAlO₃에서 La와 Al이 같은 Li 자리에 같이 들어감 → 이건 진짜 화학과 다름.
- **TODO**: per-cation cation_site mapping (La→Li_24g, Al→P_4b 같이).

### A2. High-entropy doping (5+ cations 동시)
- 학계 hot topic (high-entropy oxide → high-entropy sulfide SE 시작 단계).
- 현재: 한 batch run에 compound 하나만 가능.
- **TODO**: `--compounds A,B,C --ratios x,y,z` 다중 compound 동시 모드.

### A3. Cluster doping (precipitate as 2nd phase)
- Coating literature (Sundar 2025) 에선 NdOₓ가 별도 phase로 표면 존재 가능.
- 현재 모델: 항상 lattice substitution만.
- **TODO**: surface model + 2-phase 처리는 별도 워크플로우 (Wad pipeline).

### A4. Partial occupancy / fractional dopant
- 실제 NMR: Mg와 Li가 같은 24g 자리를 50:50 점유 가능.
- 현재: 원자 단위 결정론적 substitution.
- **TODO**: virtual atom approximation (vca) or stochastic occupancy.

### A5. Antisite defects 자체 (도펀트 없이)
- Li-P antisite, S-Cl inversion (이미 D'Amore/Pustorino reference).
- 현재 모델: dopant introduction 위주.
- **TODO**: anti-site mutation mode (도펀트 없이 host atom swap만).

### A6. Interstitial dopants — ★ **가장 중요 missing**
- B³⁺/Si⁴⁺ at P_4b는 acceptor → Li interstitial이 charge compensation.
- 우리 코드: `li_vacancies_needed`가 음수면 그냥 0 처리 → 전하 불균형으로 UMA 자동 거절.
- 진짜 처리: Li interstitial site (보통 16e octahedral void) 찾아서 추가 Li 배치.
- **TODO**: interstitial.py — void finding + Li 삽입.

---

## B. Site preference & radii

### B1. Coordination-dependent Shannon radii — ⚠ 단일 값 사용
- Shannon 반경은 CN에 따라 다름 (Li 4-coord = 0.59, 6-coord = 0.76).
- 우리 DB: 한 element당 한 값 (대부분 CN=6).
- P-site (CN=4 tetrahedral) → 4-coord 값 써야 정확.
- **TODO**: DB에 `radius_cn` dict, host site의 CN으로 lookup.

### B2. Strict / Moderate / Exotic 3-tier preference
- 현재 ALLOW_EXOTIC binary (filter or no-filter).
- 더 좋은 모델: tier별 다른 confidence weight.
- **TODO**: site_preference에 tier 라벨 추가.

### B3. Pauling's 2nd rule (local charge balance) 무시
- 결합력 합 ≈ 음이온 전하. 현재 cell-global 전하만 본다.
- **TODO**: 후처리로 local bond-valence sum 체크.

### B4. 자동 valence 추론 ★ 즉시 fix
- 현재 `MnO2` → {Mn:1, O:2}, Mn=+2 lookup → 전하 -2 → 오류.
- DB에 `Mn4` 별도 entry 추가했지만 parser는 자동으로 못 찾음.
- ★ **이번 commit에서 구현**: 전하 불균형 시 compound 안 cation의 valence를
  중성 조건으로 자동 추론.

---

## C. Vacancy placement

### C1. 'Random' vacancy = uniform random ★ 한계
- 실제 LPSCl₁₊ₓ: Li vacancy가 aliovalent cation 근처에 cluster (local charge
  compensation).
- 우리 'random': cation 위치와 무관.
- ★ **이번 commit에서 구현**: `--vacancy_near_cation` (vacancy를 cation 근방에).

### C2. Li_24g vs Li_48h vacancy 선호 무시
- 48h half-occupied → 실험적으로 vacancy 48h에 형성 우세.
- 우리: 모든 Li 동등하게 취급.
- **TODO**: `--vacancy_site Li_48h` 옵션 (요구 시 즉시 추가 가능).

### C3. Vacancy ordering temperature 효과
- 0K에선 vacancy ordering이 잡힐 수 있음 (artifact).
- anneal에서 disorder 회복 — 그래서 anneal 모든 후보에 권장.

---

## D. Algorithm subtleties

### D1. 'Cluster' 알고리즘 — 진짜 cluster radius 없음
- 현재: 가장 가까운 host atom 추가만 함 (chain).
- 진짜 cluster: 첫 atom 근처 R Å 안의 모든 host atom 중 선택.
- **TODO**: `--cluster_radius 4.0` 추가.

### D2. Spread/cluster seed sensitivity
- 'spread': 초기 atom만 random, 나머지 deterministic → seed 효과 제한.
- 'cluster': 동일.
- 'random'만 진짜 ensemble 다양성.
- → ensemble 보고 시 method='random' n_seeds≥5 권장.

### D3. 구조적 deduplication 없음
- 다른 seed가 cell symmetry로 동등한 구조 만들 수 있음.
- 우리 dedup은 (composition, ΔE) → 같은 구조 다른 ΔE는 못 잡음.
- **TODO**: SOAP descriptor or RMSD-based dedup.

---

## E. Workflow integration

### E1. Single-shot screening — multi-stage filter cascade 없음
- 현재: 460개 후보를 모두 같은 분해능으로 처리.
- 좋은 모델: Tier-1 (loose) → Tier-2 (anneal Top-50) → Tier-3 (EOS Top-10).
- **TODO**: cascade.py — Tier별 fmax/steps/method 설정.

### E2. Anneal-then-rescreen 자동화 ★ 부분 구현
- 현재: `run_anneal.py` 가 anneal만 함, post-anneal ranking은 수동.
- → ★ **이번 commit**: anneal 후 자동 ΔE/atom 갱신 + 새 분석.

### E3. Reproducibility 메타데이터
- UMA model name + version, ASE version, Python version 기록 안 됨.
- **TODO**: 모든 결과 JSON에 `provenance` block 추가.

### E4. Failure tracking
- 실패 시 generic exception print만, 원인 코드 없음.
- **TODO**: 실패 원인 분류 (site collision / charge imbalance / not converged / OOM).

### E5. Anneal 진단 (RMSD, phase transition)
- 현재: pre/post energy만.
- **TODO**: trajectory에서 RMSD(t), composition stability, transition 감지.

---

## 우선순위 (이번 세션 즉시 fix)

| 번호 | 항목 | 영향 |
|------|------|------|
| **B4** | Auto-valence from neutrality | MnO2, Fe3O4, CrO3 등 즉시 작동 |
| **C1** | --vacancy_near_cation | 실제 chemistry 부합 |
| **D1** | --cluster_radius | 진짜 cluster 가능 |
| **E2** | post-anneal 자동 재분석 | 워크플로우 완결 |

나머지는 다음 세션 작업 — 이 파일 새 세션에서 첫 5분 안에 읽고 우선순위 정할 것.

---

**작성**: 2026-05-16
**관련 commit**: 다음 commit이 B4 + C1 + D1 + E2 동시 처리.
