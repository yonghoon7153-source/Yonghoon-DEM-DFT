> # ⛔ σ "4배" · 절대 σ · 조성 간 Ea 대조는 **인용 금지** (배너 2026-09-09)
>
> 이 카드는 comp1↔modelc 의 **σ 비(~4×)와 절대 σ(3.35 → 13.96 mS/cm)** 를 헤드라인으로 쓴다.
> 값은 **이력으로 보존**하되, 지금은 아래가 이긴다:
> - **σ 절대값 인용 금지** (CLAUDE.md 데이터 규율 — Nernst–Einstein Haven=1 은 **상한**이다).
>   정본 `db/properties/li_transport.json` 스스로 같은 ~14 를 *"실험보다 3–5배 높다"* 고 적는다.
>   ⇒ *"실험 x=0.6 = 11.34 mS/cm 와 일치"* 류의 문장은 **다른 조성의 실험값을 골라 맞춘 것**이라 쓰지 않는다.
> - **조성 간 순위·비 금지** — `canonical_registry.json` 의 `MD_Ea_eV_singleseed@comp1`(0.2532)은
>   **단일시드 · `provisional`** 이고 `prohibitions` 에 `absolute_sigma` · `cross_composition_ranking` ·
>   `cite_until_beta_gate_passes` 가 걸려 있다. 계간 Ea 직접 비교는 `HZ-cross-system-Ea` = **BLOCKED**.
>   (`md_axis_status_2026_09_07.md` §0: *"지금 이 축에서 원고에 넣을 수 있는 활성화에너지는 0개"*.)
> - **방법 라벨**: 여기서 "AIMD" 라고 쓴 것은 실제로 **MLIP-MD (UMA-s-1p1, task=omat)** 다.
>   ab initio MD 논문과 나란히 놓으면 방법 오기가 된다 (2026-07-27 정정).
> - ✅ **살아 있는 것**: 구조 관측(anti-site Cl · Li 공공 · Voronoi/BVSE 기하)과 **계 내부** 서술.
>   ⚠ "장벽↓ + 캐리어↑" 기전은 두 조성의 Ea·D₀ 대조 위에 서 있으므로, **조성 간 정량 대조로는
>   쓰지 않는다** — 기전을 말하려면 축이 먼저 열려야 한다.
>
> ⛔ 아래 본문은 지우지 않는다 (kb/SCHEMA.md Update Policy).

# Slides 4–7 (Ionic conductivity) — 추가 슬라이드 콘텐츠 (2026-06-21)

슬라이드 4(Arrhenius) → 5(BVSE/percolation) → 6(Voronoi disorder) → 7(disorder 제어) 흐름에
아래 2장을 끼워 넣으면 "왜 σ가 오르나"가 정량적으로 닫힌다.

---

## ★ NEW 슬라이드 (5 뒤에) — Li⁺ percolation (AIMD 밀도 기반)

**그림:** `docs/figures/elf_licl/Li_percolation_barrier_comp1_modelc.png`

**Header:** Li⁺ percolation network — inter-cage 경로 평탄화 (AIMD 밀도)

**Bullets:**
- AIMD Li 밀도 ρ(r) → 자유에너지 지형 **F = −k_BT·ln(ρ/ρ_max)** (PMF; "그 자리에 도달하는 에너지 비용")
- F 낮은 곳부터 채우며 **연결된 최대 Li 클러스터** 추적 → *percolation threshold* = 셀 전체를 잇는 Li 망이 생기는 F
- **comp1: F = 0.19 eV**에서야 percolate (높은 장벽) / **modelc: F = 0.08 eV** (≈ **2.4× 낮음**)
- → modelc의 **inter-cage 경로가 훨씬 평탄** = Ea↓를 **BVSE와 독립적으로(AIMD 동역학)** 재확인
- **"cluster-count 역설" 해소**: modelc가 disorder·국소 클러스터는 더 많아도 *더 쉽게* 연결됨

**연결:** 슬라이드 5(BVSE bimodal channel)의 "percolated network" 주장을 **정량 에너지(0.08 vs 0.19 eV)로 뒷받침**.
(BVSE는 정적·vacancy 못 봄 → 채널 수는 오히려 −15%인데 σ는 ×4. percolation/AIMD가 그 역설을 푼다.)

---

## ★ NEW 슬라이드 (7 뒤에, 섹션 마무리) — 이중 메커니즘 정량 분해

**핵심 한 줄:** σ(300K) 비 ≈ **×4.2 = (Ea 인자) ×3.2 × (carrier/D₀ 인자) ×1.41**

| 인자 | 출처 | 값 | 의미 |
|---|---|---|---|
| Ea 인자 | exp(ΔEa/k_BT), ΔEa=0.253−0.224=0.029 eV @300K | **×3.2** | anti-site Cl disorder → inter-cage 장벽 평탄화 |
| carrier/D₀ 인자 | D₀(modelc)/D₀(comp1) = 5.8e-4 / 4.11e-4 | **×1.41** | Li vacancy → 운반자·시도빈도 ↑ |
| **곱** | | **×4.5 (≈ 실측 14/3.4 = ×4.1)** | 잔차 거의 없음 |

**Bullets:**
- 두 독립 효과의 **곱**으로 σ 설명 — anti-site(장벽↓) × vacancy(운반자↑).
- Ea 인자는 **T 의존**: 600K ×1.75 → 300K ×3.2 (저온일수록 disorder 효과 ↑).
- disorder를 인위로 동일화하면(슬라이드 7) Ea 수렴(0.177≈0.173) → **Ea 차이는 배열(disorder) 탓**임을 증명.

---

## 추가 예정 (HPC 결과 대기)
- **ε∞ (격자 분극률)** — ph.x epsil 진행 중. Kraft 2017 "분극률→전도도" 메커니즘을 우리 DFT로 직접 연결할 슬라이드.
- **CDD 비교** — comp1 완료(공유 PS₄/이온 Li 재배치), modelc 진행 중 → 두 조성 나란히.

## 자산 위치
- 침투장벽: `docs/figures/elf_licl/Li_percolation_barrier_comp1_modelc.png`
- Li-density core/spread: `docs/figures/elf_licl/Li_density_core_spread_comp1_modelc.png`
- MSD: `docs/figures/msd_compare/msd_compare_comp1_modelc.{png,csv}`
- CDD(comp1): `docs/figures/cdd/comp1_CDD_{3d,slice}.png`
