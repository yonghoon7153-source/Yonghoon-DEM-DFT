# A round 2 (pre-review impl fixes) — working plan (scratch, not a report)

Base a76f59d0d. Files: carbon_junction.py, ca_ext_cjunc.py, step3_sigma.py (hook), ca_s0_census.py, tests.

## Q-A (01, 06) different pieces = different fibres
- _distinct_instances filter: piece_i != piece_j (was fid) -> same-fid broken pieces = distinct rule (d <= D -> R_j)
- face classification keyed by piece pair (bits same when 1 piece/fid)
- closed path (Q[0]==Q[-1] exact, kind path, len>=3): with gaps -> join last+first piece through seam (open path);
  no gaps = ring piece: segs ring_L>0, cyclic arc s, pos seam alias (pos 0 / last same cell -> one dof),
  axial wrap (k 0 <-> ng-1) for face-adjacent seam
- census: n_instances_same_fid_pieces, n_piece_cell_meets (same fid, diff piece, same cell)

## Q-B (02) self = centreline pairs d<=D + per-pair s rule
- same-piece segment pairs, s = arc between closest points (cyclic ring)
- floor (census, s_min None): s > D ; registered: s >= s_min ; s_min must be > D (ValueError)
- candidates = floor groups (census s_cp, kept/filtered); instances = groups of s>=s_min pairs
- Lc self = touch length restricted to (S,Q) combos with s passing; sub-edges same restriction
- self faces: junction pair between positions' segments -> K_CUT_SELF; else s_face < s_cont -> fused; else unreg
- ports self: candidates = side positions (segment range ∩ side segs)

## Q-C (03) no relocation
- port candidates include dead positions; picked dead -> unrealized reason covered_<sid>/out_of_box; none in r_port -> no_port_in_rport
- centerline + cjunc rejected: cjunc_plan, cjunc_require_quantitative, ca_ext protocol + block validator
- test_ca_ext_z3 A12 tuple ('centerline','P0') True->False (report shared file)

## Q-D (04) SV split counterfactual
- per SDCP 6-comp: touched VGCF positions grouped (same piece & (arc gap < s_cont or path through comp cells only)); seam alias same node
- comp with >=2 groups -> copies per extra group: SV edges to own copy, SDCP-SDCP replicated, SDCP-X replicated, plate couplings replicated
- record kind counterfactual_split_sv_bridges_v1, n_sdcp_components_touching, n_bridging_components, n_sv_faces_split, n_sdcp_copy_dofs
- statuses unchanged names (D reads computed / no_through_without_sv)

## 05 k boundary: pin magnitude test (prod units) + comment
## 09 MUT-RCA mutant signature certify=None, exceptions in mutated check = harness failure
## design-04 stage 2 gate: S0 row exact, R-plan row 64hex, R-plan file sha, load_plan, s_min>D, tol_ff equal; --r-plan-path
