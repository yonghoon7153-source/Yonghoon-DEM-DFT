# External ULPRI recheck intake

This is a selected, byte-preserved subset of the external 2026-10-26 review.
The report closes ULPRI-01/02 marker-boundary integrity only at commit
`4c29705fa1c4ba94737a858b206fa4f4c5bb2bde`. It does not authorize physical runs.

The original archive SHA256 is
`21ca7a2798ed0d99849b5450248ca1ae3a36c1520a93c0ee881944c68e7552fa`.
The report and supplied pasted text are byte-identical, SHA256
`e317b1b81a76b67bd20f2b48ad97bdf1f487d0868d9bb251e72d5af075eacec8`.
The original archive and pasted file are preserved outside the repository.
`archive-verification.json` records safe extraction and all 14165 manifest hashes;
`receipt-verification.json` records source and raw case evidence verification.

The root MANIFEST.sha256 is the original external archive manifest, not a manifest
of this selected subset. The snapshot metadata describes the previously submitted
528-member review ZIP. Snapshot source copies, baseline copies, mutant source
copies, and per-case synthetic fixture trees are retained in the original archive,
not duplicated here. No fixture suite was rerun during intake.

Scripts are preserved as review evidence, not execution authorization. The independent
probe and six-case reproducer can use an exact reviewed checkout with fresh outputs.
The mutant script requires snapshot and matrix fixture trees from the full archive;
this selected subset alone is not its runnable distribution. Preserve existing results.
Windows raw311/35 selftest and UTF8-adapted346/0 diagnostics remain distinct.
The report's relative references to omitted fixture trees refer to the full archive.
