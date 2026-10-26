# ULPRI marker-boundary recheck bundle

Final review pin: 4c29705fa1c4ba94737a858b206fa4f4c5bb2bde
Tested code candidate: 643344fee22a5d1131a59c8cd46bcf6c9a09d65b
Original reviewed pin (preserved): 01c1aaf5be8acdf7d1716f34cc86fc77d8e27362

All repository-path members are exact blobs from the final Git commit, including
all changed paths, the complete94-file kit, registration, original request/NOTE,
the thirteen-command list, and required source fixture archives/density deck.
SOURCES.json records Git blob IDs, modes, hashes and selection roles. PIN.txt,
SOURCES.json and this README are packaging metadata. MANIFEST.sha256 covers all
other members. This is a review subset, not a complete Git repository.

The final commit only adds gate evidence and a completion note. The shared gate
ran on the candidate and passed155/0 with rc0; its original log and source
manifest are included. The kit's13 direct commands are separate from those155
lanes. Their raw logs, actual counts and tested source hashes are also included.
The sole post-test README sentence clarification is bound to the original tested
bytes by the committed author delta and independently reviewed exact patch.
Packaging checks recorded-output consistency and source binding; it does not
re-execute these tests or replace independent semantic review of their coverage.

After extracting to a new directory on Linux with Python3, NumPy and Bash,
run the thirteen synthetic kit commands from the extraction root as follows:

    python3 -I docs/reviews/ulpri_marker_evidence_20261024/author/run_marker_suite.py --repo . --out /tmp/ulpri-kit-review-new

The output path must not exist. This driver reads the included original command
list and runs the included kit and fixture files without Git or network access.
The focused received counterexamples can also be replayed with a new output:

    python3 -I -B docs/reviews/codex_review_unloading_ulpr_integer_20261024/repro_boundary.py --repo . --out /tmp/ulpri-boundary-review-new

For that original external script, ensure its output directory does not exist
before invoking it; the script itself accepts existing output paths. Its report
at the old pin is preserved separately from observations on this corrected pin.
The kit's runner tests supply synthetic binaries.
The included historical tgz is read as fixture evidence only. No actual
LIGGGHTS/MPI/WSL research run is authorized or performed by creating this ZIP.
Full repository checks need a complete Git checkout; this subset cannot replace it.

The original request and NOTE are included as historical review context. Read
docs/reviews/codex_dem_unloading_ulpri_recheck_request_20261024.md and the new
ulpri_marker_evidence_20261024 notes for the current, narrower correction scope.
External review accepted the previous exact-integer correction but held Q2/Q3
integrity closure for ULPRI-01/02. These local changes are claimed fixes awaiting
external recheck. This package does not release that HOLD or authorize production.
The original01c1 pin and previously submitted ZIP were not rewritten.
