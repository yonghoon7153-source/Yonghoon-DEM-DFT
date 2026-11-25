# External Review Response (2026-05-16)

외부 LLM이 보낸 비판에 대한 항목별 검증 + 처리 결정.

분류 기준:
- 🔥 **ACCEPT-CRITICAL** — 진짜 버그, 즉시 fix
- ✅ **ACCEPT** — 일리있는 지적, fix
- 🛡 **DEFEND** — 사실 reviewer가 부분적 오해 / context 부재 (수정 없거나 docstring만 보강)
- 📝 **PARTIAL** — 부분적 valid, caveat 추가

---

## 🔥 ACCEPT-CRITICAL (이번 commit에서 즉시 fix)

### CR-1 `tier_cascade.sh:44` cd 한 줄이 잘못된 디렉토리로
**Reviewer 주장**: `cd "$(dirname $(realpath BASE))/.."` 가 `repo_root/db/`로 가서 `tools/doping/...` 못 찾음.
**검증**: BASE=`db/structures/lpscl_F43m_24G_canonical.cif` → realpath 후 dirname = `repo/db/structures` → `/..` = `repo/db`. 정확.
**왜 지금까지 안 터졌나**: 사용자가 `tier_cascade.sh`를 아직 안 돌렸음 (`run_compound_batch.sh` + `run_uma_screening.py` 개별 호출만). cascade 처음 launch 시 stage 00에서 즉시 fail했을 것.
**Fix**: dirname 2번 적용 or 명시적 REPO_ROOT 인자.

### CR-2 `select_winners` grouping key 누락 (chain integrity 깨짐)
**Reviewer 주장**: `substitute_compound.py` record에 `dopant`/`site`/`anion_site_label` 키 없음. `run_compound_batch.sh` 머지가 채워주는 우연한 의존성. standalone 호출 시 전체 'unknown' grouping → 글로벌 best 1개만.
**검증**: `substitute_compound.py:651-660`의 info dict 보면 `cation_site_used`/`anion_site_used`만 있고 `dopant`/`site`/`anion_site_label` 없음. **Reviewer 정확.**
**Fix**: substitute_compound.py info dict에 명시적으로 추가.

### CR-3 BVSE를 unrelaxed 좌표에 적용
**Reviewer 주장**: stage 04 BVSE가 stage 01 (substitute 결과, 미 relax) xyz 사용. BVS는 exp((R0-R)/b) 거리 지수함수라 평형 거리에 매우 sensitive → unrelaxed 좌표의 BVS는 인위적.
**검증**: `tier_cascade.sh:113`에서 `--xyz_dir "$OUT/01_structures/structures"` 확인. **Reviewer 정확.**
**Fix**: cascade에서 stage 04 BVSE를 stage 05 post-anneal 이후로 이동, 또는 stage 02 후로 옮기되 relaxed xyz를 따로 저장하게 run_uma_screening 수정.

### CR-4 BVSE proxy chemistry 부호 오류
**Reviewer 주장**: 우리 `proxy = std × (1 - |mean-1|)`는 "BVS std 클수록 σ 빠르다"는데, Adams 2003/Mo 2014는 정반대 ("BVS≈1 가까운 사이트 많을수록 σ 빠르다, std 작아야"). Threshold `[0.5, 1.5]` 너무 관대 — Adams `[V₀±0.2]≈[0.8, 1.2]` 표준.
**검증**: 문헌 정확. argyrodite처럼 multi-site 시스템도 σ-fast의 핵심은 **평탄한 PES (similar sites)**, 즉 narrow BVS distribution. **Reviewer 정확.**
**Fix**: proxy 부호 반전 + threshold 좁히기.

### CR-5 `--vacancy_cutoff` CLI 옵션 silently ignored
**Reviewer 주장**: `substitute_compound.py:377-379` `select_substitution_sites` 호출에 `cluster_radius=args.vacancy_cutoff` 전달 안 됨. 사용자가 `--vacancy_cutoff 5.0` 줘도 default 4.0 사용.
**검증**: 코드 확인. **Reviewer 정확.**
**Fix**: 인자 전달 추가.

### CR-6 `compute_tier2_metrics` dopant 분류 오류
**Reviewer 주장**: `host_elements = {Li, P, S, Cl, Br, I, O, N, F}` 안에 anion dopant도 포함. Type B halide-rich (Cl-rich)에서 추가 Cl이 dopant인데 host로 분류 → `dopant_blocking_count = 0`.
**검증**: 정확. anion doping (oxysulfide, halide-rich)에서 Tier-2 blocking score가 의미 없어짐.
**Fix**: dopant_idx를 baseline composition (Li24P4S20Cl4) 대비 추가 원소로 정의.

### CR-7 Type B' (mixed_halides) / Type D (multi_compound) merge 누락
**Reviewer 주장**: `run_compound_batch.sh:198-200` merge가 `A_compound`/`B_halide_rich`/`C_chain_halide_rich`만 인식. Type B' (mixed halides) / D (multi-compound) record는 `dopant='unknown'`이 됨.
**검증**: 코드 확인 — 정확.
**Fix**: merge에 `B_mixed_halide` + `D_multi_compound` step 추가.

---

## ✅ ACCEPT (이번 commit에서 fix)

### A-1 `--require_converged` cascade 미적용
**Reviewer 주장**: `select_winners --require_converged` flag 있지만 cascade에서 사용 안 함. nonconverged record가 winner 되면 신뢰도 낮음.
**Fix**: cascade의 select_winners 호출에 `--require_converged` 추가.

### A-2 Bi5/Eu2/Mn4 등 dead DB entries
**Reviewer 주장**: `parse_compound("Bi2O5")`는 `Bi`(=+3)만 찾고 `Bi5` 못 찾음. `ALTERNATIVE_VALENCES['Bi']=[+3, +5]`가 우회하므로 `Bi5` entry 자체는 dead.
**검증**: 정확. 이중 system → 혼란.
**Fix**: 변종 entry 정리. ALTERNATIVE_VALENCES만 single source of truth로.

### A-3 EOS r² gate 없음
**Reviewer 주장**: 발산한 BM3 fit (r² < 0.95)도 `B0_GPa`이 그대로 reported → `combine_rankings` modulus axis 오염.
**Fix**: B0/V0 reporting 시 r² gate 적용.

### A-4 docstring vs 코드 불일치
**Reviewer 주장**:
- `run_mlip_postproc.py:6` "96-106% in 7 steps" — 실제 94-106%
- README "75+ DOPANT_DB" — 실제 71
- spread "deterministic" — seed-fixed reproducible (seed 바꾸면 결과 변함)
**Fix**: 모든 docstring 정정.

### A-5 POSITIVE_CONTROL dead code
**Reviewer 주장**: `preflight.py:36`에 list 정의됐는데 사용 안 함.
**Fix**: preflight에 실제 mini-batch positive control 추가 — Nd2O3/Al2O3/Cl_rich가 substitute → UMA quick relax → Tier-2 metric 정상 나오는지 확인.

---

## 🛡 DEFEND (reviewer 부분 오해 / 우리가 의도한 동작)

### D-1 Cij 부호 convention
**Reviewer**: ASE stress 부호 검증 안 됨, C11 음수 가능성.
**우리 입장**: ASE convention `atoms.get_stress(voigt=True)`은 "negative of dE/dV" (= 압축이 +). 우리 식 `dσ/dε = (σ(+ε) - σ(-ε)) / (2ε)`은 ASE 부호 사용 시 양수 C11 자연 산출. 우리 batch 결과 (B0 ≈ 19~30 GPa, 양수)가 sign 정확함의 증거. **Reviewer가 standalone code 검토만 했고 실제 결과는 못 봄.**
**Action**: 코드에 부호 convention 주석 추가 (수정 불필요).

### D-2 `run_anneal.py` "Li-selective"
**Reviewer**: docstring "PS4/Cl rigid"인데 FixAtoms constraint 없음 → 광고와 불일치.
**우리 입장**: **500K에서의 Li-selective는 constraint가 아니라 thermal threshold로 실현**. Li hop Eₐ ≈ 0.2 eV, kT@500K = 0.043 eV → 활발한 Li 운동. P-S bond ≈ 3.5 eV ≫ kT → 진동만. Cl⁻ cage 이온결합도 500K에서 안정. 즉 **constraint 없이도 물리적으로 Li-selective**. 800K 넘으면 Cl hop 시작 (우리 docstring에서 이미 경고). FixAtoms로 강제하면 오히려 부자연스러움 (실험은 강제 X).
**Action**: docstring을 더 명확히 — "thermally Li-selective via kT threshold (no explicit constraint)" — 수정 불필요한 chemistry.

### D-3 ML predictor data leakage
**Reviewer**: random KFold은 dopant leakage. GroupKFold로 dopant 그룹 단위 stratified 해야.
**우리 입장**: 우리 use case = "이미 본 dopant의 새로운 (site, conc, seed) 조합 예측". cold-start "새 dopant" 예측은 cascade의 use case가 아님 (지금 단계는). 따라서 random KFold는 우리 task에 적절. 단, cold-start (`predict_new.py` 호출 with 새 dopant)는 의미 무 — 이건 README에 명시 필요.
**Action**: `train_predictor.py` 출력에 caveat 추가 + `predict_new.py` 도 warn.

### D-4 `cluster` 알고리즘이 "anti-spread"가 아닌 "chain"
**Reviewer**: cluster가 매번 가장 가까운 다음 atom을 추가하는 chain. PS4 내 클러스터링은 안 됨 (인접 PS4로 흘러감).
**우리 입장**: 우리 verified test (`mean pair distance = 3.40 Å = PS₄ S-S edge`) 자체가 cluster method가 같은/인접 PS₄ 내에서 작동한다는 증거. 12 S 안에서 3 picks의 mean pair distance ≈ 3.40 Å는 인접 PS₄ S들로 모인 결과. PS₄ 내 ≥ 4 anions clustering이 정확히 필요한 use case (PO₄ 형성)는 아직 검증 못 했지만 PSO₃ 패턴 (3 different P에 1 O씩)과 PO₄ 패턴 (1 P에 3-4 O 모임)이 random seeds로 둘 다 나오는 게 정상.
**Action**: docstring을 "chain-based clustering — picks atoms by successive nearest-neighbor extension" 으로 명확히.

### D-5 spread "deterministic" claim
**Reviewer**: 첫 seed가 random.
**우리 입장**: seed-fixed면 deterministic. **이게 표준 random seed semantic**. 외부 reviewer가 "deterministic = seed 무관"으로 해석한 것은 비정상.
**Action**: docstring을 "reproducible given fixed seed" 로 명확히.

### D-6 file size of substitute_compound.py (800+ lines)
**Reviewer**: 유지보수 어려움.
**우리 입장**: 한 시점에 모든 chemistry가 한 파일에 있는 게 navigation에 유리. 800줄은 큰 편이지만 docstring + 5 type doping + auto-valence + interstitial 다 들어있어 정상. dataclass refactor는 long-term.
**Action**: 현 단계 무 (Phase 2에서 refactor).

---

## 📝 PARTIAL / 향후 fix

### P-1 Li_24g vs Li_48h 미구분 (self-review 이미 인정)
**Reviewer**: Li_24g vs Li_48h 같은 처리. argyrodite diffusion network 역할 다름.
**우리 입장**: self-review에서 이미 TODO C2로 명시. 24g/48h는 UMA relax 후 (Pustorino 2025 Table 3) 사실상 동등 (ΔE/atom 차이 < 0.0001 eV/atom).
**Action**: cascade 결과에서 명시적으로 Li_24g/Li_48h dedup하거나, 그냥 Li_24g만 사용. 다음 commit.

### P-2 acceptor charge balance, single-element path
**Reviewer**: `substitute_struct.py`의 acceptor는 imbalanced. `substitute_compound.py`에서만 interstitial.
**우리 입장**: substitute_struct는 legacy single-element substitution. compound path가 main 워크플로우. 둘 다 동일 로직이려면 substitute_struct에 interstitial 위임.
**Action**: substitute_struct의 `add_li_vacancy`처럼 `add_li_interstitial` 추가 + apply_charge_compensation에서 acceptor 시 호출.

### P-3 EOS Stage 07/08 중복 relax
**Reviewer**: 같은 xyz를 stage 07, 08에서 두 번 relax. 일관성 약점.
**Action**: stage 07이 relaxed xyz를 caches에 저장, stage 08이 그것 사용. 다음 commit.

---

## 통계

| 분류 | 항목 수 | 비고 |
|------|--------|------|
| 🔥 ACCEPT-CRITICAL | 7 | 이번 commit fix |
| ✅ ACCEPT | 5 | 이번 commit fix |
| 🛡 DEFEND | 6 | docstring 보강만 |
| 📝 PARTIAL | 3 | 다음 commit |
| **합계** | **21** | — |

→ 12개 실제 fix, 6개 docstring 보강, 3개 다음 commit.

**다음 commit 내용**: CR-1 ~ CR-7 + A-1 ~ A-5 + docstring 정리.
