# Additive × mixing process matrix (the A4 plug-board) — 2026-06-30

Scaffolding so every (additive × mixing-process) combination is an **independent,
explicit slot**. Today only the validated cells carry physics; the rest are wired
placeholders for the **A4 se_coating** GPU result to fill — no re-plumbing later.

## Valid additive combinations
VGCF and Super P are **both conductive carbon → mutually exclusive** (use one).
Valid: **VGCF · Super P · PTFE · VGCF+PTFE · Super P+PTFE**. VGCF+Super P is blocked
in the UI (popup) and the backend (`whatif_additives` + the zip endpoint return an error).

## The 3×3 matrix (`scripts/additives.py` `ADDITIVE_PROCESS`)
`regime` = where the additive ends up: `bulk` (interstices) / `coat_block` (in the
SE-coating-on-CAM, blocks CAM–CAM) / `coat_embed` (embedded in porous SE coat, conductive).

| additive | ball-mill | thinky (dry-coat) | hand-mix |
|---|---|---|---|
| **Super P** | bulk | **coat_block** (Kim2025 → σ_e collapse) | bulk |
| **VGCF** | bulk | **coat_embed** (Kim2025 → σ_e recovers) | bulk |
| **PTFE** | bulk | bulk (TBD A4) | bulk (TBD A4) |

Super P also carries its carbon-black morphology per mixing (`k/surface_frac/step/clump`,
the old `CB_MIX`, now derived from this matrix — ball=thinky uniform, hand=agglomerate).

## What is WIRED now vs TBD(A4)
- ✅ **W2 σ (`grade_engine.whatif_additives`)** reads `additive_regime(name, mixing)`:
  `coat_block` + Super P → σ_e collapse (Kim2025); `coat_embed` + VGCF → flagged
  `vgcf_coat_embed` (σ magnitude **TBD A4**, today = bulk estimate, no change).
- ✅ **MPM seeding (`mpm3d_compaction`)** looks up the regime per additive and prints
  it; the seeding still places every regime in the **bulk** (the `coat_*` SE-coating
  placement is the A4 hook — `# A4 HOOK` in the loop).
- 🔶 **A4 UPDATE (2026-07-09, 97767ae)**: SuperP `coat_block`(thinky) + SDCP `coat` now SEED as an AM-surface film (`seed_coat`, shell 0.2µm, process-row surface_frac) — thinky ≢ ballmill for SuperP from this date.  VGCF `coat_embed` still NOT coat-seeded (fibre branch wins) ⛔; σ_e-direction validation + divergence re-run pending.
- ⛔ **TBD A4**: (i) seed `coat_*` carbon in the SE-coating layer on the AM surface
  (not bulk) in mpm3d_compaction; (ii) the `coat_embed` σ_e-recover magnitude in
  whatif; (iii) VGCF/PTFE per-mixing morphology (fibre length / fibrillation) — the
  `morph` strings record the intended direction.

## Behaviour is unchanged by this scaffolding
`CB_MIX` is byte-identical (derived). The W2 smoke-test still passes (Super P
thinky→collapse / bulk→boost, VGCF thinky→boost+flag). The only new *behaviour* is
the VGCF+Super P block. Everything else is structure + the recorded regime, ready
for A4 to drop in.
