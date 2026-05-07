# Enaldiev et al. 2021 — TMD Twistronic Adhesion Binding Curves

> **DOI**: 10.1088/2053-1583/abdd92
> **Citation**: Enaldiev, V. V.; Ferreira, F.; Magorrian, S. J.; Fal'ko, V. I. *2D Materials* **8**, 025030 (2021).
> **Group**: Vladimir Fal'ko (Manchester, National Graphene Institute)
> **Acquired**: 2026-05-07 (user PDF text + Figure 2)
> **Relevance**: ==**MEDIUM**== — different system (2D vdW vs 3D ionic) BUT shares methodology with our Phase 1 rigid binding curve.

---

## 1. Why we save this paper

User showed Figure 2 (DFT adhesion energy W(r₀, d) for 6 stackings × 2 orientations) which IS THE SAME OUTPUT TYPE as our `phase1_rigid_binding.py` produces. Different system, same method. Useful as:

1. **Method precedent** for rigid binding curve adhesion analysis with multi-stacking sampling
2. **Analytical interpolation formula** could replace our numerical Phase 1 curves
3. **Citation backing** for our Phase 1 SI figures
4. **Multiscale framework**: DFT local + elasticity mesoscale = inspires our approach (but our system is 3D bulk so direct adoption limited)

==**NOT useful for**==: moiré physics, ferroelectric/piezoelectric domains, twist angle, exciton confinement (all 2D-specific phenomena).

---

## 2. Method (Section 1)

### Computational details
- **Code**: VASP + PAW + GGA-PBE
- **vdW correction**: optB-88vdW (explicit) — *we use UMA which has implicit vdW from training*
- **Cutoff**: 600 eV (for ferroelectric Δ analysis), 816.34 eV / 60 Ry (for adhesion W)
- **k-grid**: 12 × 12 in plane
- **Strain convention**: monolayer lattices strained to mean of WX₂ and MoX₂ (δ = 2(a_Mo - a_W)/(a_Mo + a_W) = 0.2-0.3%)
- **Spin-orbit**: NEGLECTED (set aside intentionally)

### Adhesion energy formula (their Eq. for W in §1.2)

```
W_P/AP(r₀, d) ≈ f(d₀) + ε · z²
              + w₁ · [1 - Q·z] · Σ_n cos(G_n · r₀)
              + w₂ · [1 - G·z] · Σ_n sin(G_n · r₀ + γ_P/AP)

where:
  z = d - d₀                              (deviation from optimal interlayer dist)
  r₀ = lateral offset between layers     (XX → r₀ = 0)
  G_n = first star of reciprocal vectors (n = 1, 2, 3)
  γ_AP = 0, γ_P = π/2                    (orientation-specific phase)
  ε, w₁, w₂, Q, d₀ = fitting parameters  (Table 1 of paper)
```

### Adhesion gain values (Table 1)
| TMD | w₁ (eV/nm²) | w₂ (eV/nm²) | Q (Å⁻¹) | d₀ (Å) |
|---|:-:|:-:|:-:|:-:|
| WS₂/MoS₂ | 0.175 | 0.021 | 3.07 | 6.5 |
| WSe₂/MoSe₂ | 0.128 | 0.020 | 2.93 | 6.9 |

### Ferroelectric charge transfer Δ (Eq. 1)

```
Δ(r₀, d) = A₀ · [1 - q₀·z]                              (ferro term, heterobilayer-specific)
         + A_P/AP · [1 - q_a·z] · Σ_n sin(G_n · r₀)     (piezo-like term, P-orientation)
```

| Atom X | A₀ (meV) | q₀ (Å⁻¹) | A_a (meV) | q_a (Å⁻¹) |
|---|:-:|:-:|:-:|:-:|
| S | 29.9 | 1.73 | 12.8 | 2.53 |
| Se | 26.5 | 1.89 | 9.53 | 3.12 |

### Multiscale lattice reconstruction (§1.3)

Total energy minimized:
```
E_tot = ∫_supercell d²r [(λ_l/2)·(u_ii^l)² + μ_l·u_ij^l u_ji^l + W̃_AP/P(r₀(r))]
```
- l = W or Mo layer
- λ, μ = elastic moduli (Table 1 of paper)
- u^l = lateral displacement field (relaxation)
- Solved via Lagrange-Euler equations + finite-difference + GEKKO Optimization Suite

---

## 3. Quantitative results — adhesion (Figure 2)

==**Y-axis: eV/nm²**==. ==**Conversion: 1 eV/nm² × 0.16 = J/m²**==.

| Stacking gain | eV/nm² | J/m² | Comment |
|---|:-:|:-:|---|
| 2H/3R domain over averaged baseline | ~0.5 | **~0.08** | vdW binding gain |
| Total adhesion depth (rough) | 2-3 | 0.32-0.48 | Total binding ≈ 0.5 J/m² |
| Strain cost for lattice match | (λ_W + λ_Mo)·δ² ~ 0.01 | 0.0016 | Negligibly small |

==**TMD-TMD vdW: ~0.5 J/m² total**==. 우리 LPSCl/NCM ionic: ~1-2 J/m² (==**3-4× 더 강함**==, chemistry vs vdW).

### Optimal interlayer distance d₀
- WSe₂/MoSe₂: 6.56 Å (DFT optB-88vdW) vs 6.46 Å (homobilayer experiment) — Δ = 0.1 Å
- WS₂/MoS₂: 6.25 Å (DFT) vs 6.15 Å (experiment) — Δ = 0.1 Å

### Ferroelectric jump Δ
~25-30 meV potential step at MoX₂/WX₂ interface (vertical charge double layer).

---

## 4. Comparison with our paper #2 work

| Aspect | Enaldiev 2021 | Our paper #2 |
|---|---|---|
| **System** | 2D-on-2D (TMD/TMD) | 3D-on-3D (LPSCl/NCM) |
| **Bonding** | vdW (~0.5 J/m²) | Ionic + chemistry (~1-2 J/m²) |
| **Method** | DFT rigid + multiscale elasticity | UMA LBFGS + sandwich relax |
| **Code** | VASP + optB-88vdW | UMA (fairchem) |
| **Stackings** | 6 high-sym (XX, WX, MX...) | 6 high-sym + 30 random |
| **Output** | E(d) curves + Δ ferroelectric | W_ad J/m² per registry |
| **Domain physics** | moiré reconstruction, twist angle | n/a (3D bulk, no moiré) |
| **What we adopt** | ⭐ analytical interpolation formula concept | — |
| **What we don't** | piezo/ferro electric, exciton, twist | — |

---

## 5. Potential adoption for paper #2

### A. Phase 1 (rigid binding) interpolation formula

Currently `phase1_rigid_binding.py` outputs numerical E(d, registry) data. We could fit:

```python
# Pseudo (NOT implemented yet — proposal only)
def W_interpolation(r_lateral, d, params):
    """Enaldiev-style interpolation for our LPSCl/NCM rigid binding."""
    z = d - d0
    sum_cos = sum(np.cos(np.dot(G_n, r_lateral)) for G_n in star_G)
    sum_sin = sum(np.sin(np.dot(G_n, r_lateral) + gamma) for G_n in star_G)
    return f_d0 + eps * z**2 + w1 * (1 - Q*z) * sum_cos + w2 * (1 - G*z) * sum_sin
```

**Pro**: analytical model, smoother curves, can predict W at any (r, d).
**Con**: assumes hexagonal/triangular reciprocal symmetry — works for NCM (LiNiO2 R-3m) but check if SE 2x2x{1,3} has matching symmetry.

### B. SI methodology citation

> "Following the rigid-binding-curve approach established by Enaldiev et al. (2021) for TMD heterobilayers, we evaluate the lateral-position-dependent adhesion energy W(r, d) at fixed registries..."

### C. NOT to adopt
- ❌ Moiré reconstruction — our system has no moiré (cell-commensurate stacking)
- ❌ Piezoelectric / ferroelectric analysis — LPSCl is centrosymmetric, no piezo
- ❌ Twist angle — our SE/NCM stack with fixed orientation

---

## 6. Locations to potentially cite

- `필독/adhesion/phase2a_v10b_sandwich_se_fixed.py` (header) — Method precedent
- `kb/papers/computational_methods_draft.md` (when finalizing paper #2 Methods) — interpolation formula option
- `kb/results/adhesion_v5_full_report.md` (Section "Methods context") — multi-stacking precedent

---

#literature #must-read #TMD #twistronic #vdW #DFT-adhesion #binding-curve #interpolation-formula #multiscale #Fal'ko-group #method-precedent #Phase1-relevant #2D-materials
