# A round 2 — design decisions (scratch, rebuilt after restart 10-21)

Base a76f59d0d. Model version -> r3-carbon-junction-port-v3 (schema cjunc-v2 kept: plan rows unchanged).

## Q-A + 06 (pieces = fibres; closed path seam continuous)
- _segments_of: arc per piece (local); closed path (kind path, len>=3, Qc[0]==Qc[-1] exact):
  gaps -> join last+first piece through seam (ixs[1:-1] + [ixs[-1] ++ ixs[0][1:]]); no gaps -> ring piece, ring_L = length.
- _positions: ring piece with ng>=2 -> alias last position -> first (pos['alias']); alias excluded from extra dofs, assembler pos_dof[alias] = pos_dof[target];
  axial face rows still use the alias position (dof same).
- _distinct_instances: filter piece_i != piece_j (same fid allowed). by_pair keyed by piece pair. instances get fi==fj possible.
- revisit census: same PIECE, same cell, non-consecutive positions (alias pair excluded). n_piece_cell_meets: cells with >=2 pieces of one fid.
- census: n_instances_same_fid_pieces, n_ring_pieces, n_seam_alias, n_closed_paths_joined.

## Q-B (self = centreline pairs d<=D, s rule)
- pairs from KD query (same as distinct), same piece, canonical i<j (index), d via seg_seg_closest(i,j).
- s = |arc_i(C_i) - arc_j(C_j)|, ring -> min(s, L-s).
- floor: s > D (always). continuity(s) := s <= D or (s_min not None and s < s_min). junction = d<=D & ~continuity (uses _self_is_junction hook for s>=s_min).
- candidate groups = floor pairs union-find (neighbour (i+-1,j+-1), ring wrap); instances = junction pairs union-find.
- census: n_self_candidates (floor groups), n_self_kept (= #self instances), n_self_filtered (candidate groups with no junction pair), self_s_um (CP s of candidate groups).
- self instance: CP rule same as distinct (eps band d2, lexmin midpoint); Si/Sj = unique i/j; d0 = min d; s = s at CP pair; L_c = touch restricted to allowed combos (s passes) both sides; sub-edges restricted the same; _nearest_on restricted to allowed partners of X's segment.
- ports self: candidates = side positions (seg range ∩ side segs) within r_port (Q-C rule: any liveness; dead -> unrealized).
- faces same piece non-axial: footprint (side membership + D_fp like distinct) -> K_CUT_SELF; else s_face (exact arc gap of positions) continuity -> K_SELF_FUSED; else K_UNREG.
- instance fields kept: self_dk_min = |k(port_j)-k(port_i)| or -1; self_n_revisit = side-i x side-j same-cell pairs; self_n_face = faces cut; self_A/self_B side positions.
- self_revisit_pairs (registry) = same-piece revisit pairs not joined by a realized junction sub-edge (path only).

## Q-C (no relocation)
- port candidates = positions (any liveness) within r_port; pick by rule; picked dead -> unrealized reason covered_<sid> | out_of_box; none -> no_port_in_rport.
- centerline + cjunc rejected: cjunc_plan (always), cjunc_require_quantitative, ca_ext_cjunc.cjunc_protocol_record + block validator. test_ca_ext_z3 A12 flips (shared file — report).

## Q-D (SV counterfactual, cut-only, Rayleigh-safe)
- per SDCP 6-component C: touched owner positions of K_VX rows (SDCP side in C) -> continuity groups: same piece & (arc gap continuity OR all positions strictly between are dead with cell in C (covered-through)); ring cyclic.
- groups<=1 -> keep; else cut rows of non-passing groups; >=2 passing -> unsplit (bridge kept, counted).
- ft['sv_cut'] bool (fingerprinted). assembler carries CF flag per edge; counterfactual drops CF edges. ratio >= 1 by Rayleigh (subgraph).
- record kind 'counterfactual_cut_sv_bridges_keep_self_v1'; n_sdcp_components_touching, n_bridging_components, n_sv_faces_cut, n_sv_faces_kept_self, n_unsplit_bridging_components.
- step3 main_unconverged record kind -> CJ constant.

## 05: pin test (prod units R_j 1e2/1e4/1e6 jumps ~ -0.98% / -2.1e-4 / -2.1e-6, scale ~1/R_j) + comment in _n_sub.
## 09: MUT-RCA cf mutant signature certify=None; exceptions inside mutated checks = harness failure (_TRY_EXC counter).
## design-04: verify_plan_commit(repo, sha, plan_path, r_doc, r_plan_path): S0 row exact == S0 plan sha; R row 64hex (rint_r_chain.registration_plan_hash); R plan file sha == row; load_plan; tol_ff_um == values_um.tol_ff; s_min_um > D = 2 r_f + tol_ff. CLI --r-plan-path; run_stage r_plan_path.

## Test fixtures (new)
- GAP same cell (z 3.15/3.85), face-adj (2.85/3.5), prod units (0.47/0.59, 0.40/0.52; vox .15 rf .075 tol .03 smin .3 Rj 1e6 sig 7853.98)
- RING (probe), RING_GAP (one gap on right leg)
- XC self crossing: (1.5,1.5,.5)->(1.5,1.5,4.5)->(1.5,4.5,4.5)->(2.3,4.5,4.5)->(2.3,4.5,2.5)->(2.3,.5,2.5)->(2.3,.5,7.5); s_cp 10.8; L_c 1.2; ports (1,1,2)-(2,1,2)
- KW legs 1.2 > D -> no instance, faces UNREG
- SVY: A vertical through SDCP (1,1,3); B x-run from (1.5,2.5,3.5) to (4.5,2.5,3.5) up to (4.5,2.5,7.5)
