# D3 verified gate timeout — original failure preserved

The actual gate finished at 2026-10-23T20:02:53.269689+00:00 with **154 PASS / 1 FAIL, rc 1**. The last inventory driver passed 191/192 tests in 384 seconds; `scripts/run_network_194_parallel.py --selftest` hit its existing 300-second timeout (rc 124). Canonical docrefs preflight and in-gate docrefs passed. Candidate HEAD/source identity and clean state remained unchanged.

The inventory driver defaults to six workers. Three full gates may therefore run up to eighteen test subprocesses on the observed four-CPU quota (`400000 100000`). Resource contention is a plausible cause, not a proven exclusive diagnosis. The shared gate, driver, failed selftest and inventory are byte-identical between the fixed D3 parent and candidate. No diagnostic test was rerun.

All 15 original top-level runtime files are preserved byte-for-byte in `raw/` and `original-gate-records.zip`, with SHA256 manifests. The original run remains unchanged. No completion overlay or publication PASS was generated. Current other runs remain untouched; future scheduling and complete fresh reruns belong to root.
