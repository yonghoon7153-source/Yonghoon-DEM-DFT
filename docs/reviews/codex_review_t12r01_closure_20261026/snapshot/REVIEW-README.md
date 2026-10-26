# T12R-01 offline-boundary recheck bundle

Final published pin: 96f15ed17e03181b6096fb65f71ec7f577f17523
Tested source candidate: 3eecce8af503556b678f8f4a02343e6bce3d0b83
Preserved base: bffc42cab29da37b45f8a713e30e8572b91e7da3

Every repository-path member is an exact final Git blob, with object IDs, modes and SHA256 in SOURCES.json. This includes all changes plus inherited T12/ULPRI-closure review essentials. The only existing source change is the pinned consumer snapshot runner; the new offline regression and review evidence are additive. Historical evidence describes its own pinned source and must not be interpreted as tests of changed current files.

Read docs/reviews/dem_gen2_t12r_offline_recheck_request_20261026.md and docs/reviews/dem_gen2_t12r_evidence_20261026/README.md. The external raw report is a byte-exact .original.txt; REPORT.md is an authored archive-path index, not the original report. Local correction remains claimed fixed pending external recheck. Accepted consumer interpretation and narrow ULPRI-01/02 closure remain valid. Physical T12 is NOT_RUN; no broad P1/design GO or production/WSL/Claude integration is authorized.

The shared gate passed155/0 on the exact candidate, with raw log and source manifest included. Direct52/offline regression are separate from those155 lanes. Positive52 is the complete-object case of the offline suite and was not needlessly repeated; the source/contract8 and consumer13 mutants use the updated runner. Counts overlap and are not additive. Actual patched Git coverage is2.52.0; unsupported-option behavior is explicitly a mock, not certification of older Git or Windows.

This subset is not a full Git checkout. Reproducing the offline suite requires local Git objects for consumer4c29705fa1c4ba94737a858b206fa4f4c5bb2bde, Python, and Git recognizing global --no-lazy-fetch. Its --repo points to that complete local object source and --source to this extraction/checkout. Use a new --output path. The runner does not fetch; the regression's control deliberately uses only local file transport to an empty remote. No scientific run is implied.

Root PIN/SOURCES/README/MANIFEST are packaging metadata; MANIFEST covers all other members.
