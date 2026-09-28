# LH high-Bo review round 4 — reproduction bundle

Review date: 2026-09-28
Repository: yonghoon7153-source/Yonghoon-DEM-DFT
Reviewed code: ba33a49398b31c79369f032f390b8a62762d2db8

This is an independent, read-only review evidence copy, not a production checkout.
The report is packaged alongside this directory as codex_review_mixer_highbo_round4_20260928.md.
File-and-line links in the report refer to the original local evidence path; the same relative paths and line numbers are present here.

## Safety and scope

No LIGGGHTS/DEM execution, no campaign launch/resume, no Git mutation, and no production code changes.
The probes create temporary synthetic decks, STL and particle dumps, logs, and seals.
They invoke actual source functions, CLI validators, and the extracted Python certificate gate from launch_highbo.sh.
They never launch that shell script or a simulator.
A source generator is called to construct temporary comparison fixtures; this is not generation of production LH run directories.

## Reproduce

Use Python 3 with NumPy and SciPy available. Run from this directory:

~~~bash
python3 verify_sources.py
python3 run_selftests.py
python3 review_round4_probe.py
~~~

The last two commands regenerate their JSON output files.
Temporary paths and timing values may differ; numerical findings and rejection/acceptance outcomes are the reproducible claims.
An exit code of zero for the independent probe means the expected counterexamples and closure controls were observed.
It is NOT approval of the reviewed production code.

Recorded runtime: Windows, Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1.
The source copies are byte-exact Git blobs; verify_sources.py checks them using Git's blob SHA-1 format without invoking Git.

## Contents

- sources.json: exact reviewed commit and 18 source blob hashes.
- verify_sources.py: read-only byte verification.
- run_selftests.py / selftests_output.json: six source selftest groups and full output.
- review_round4_probe.py / review_round4_output.json: independent synthetic tests and results.
- scripts/, dem_scripts/, docs/: pinned source copies.

The independent JSON serializes nonfinite returned numbers as strings (for example "nan") to remain strict JSON.
The actual producer's B-coordinate nonfinite acceptance is preserved in the evidence; this conversion is only output serialization.

## Limitations

The complete test_launcher.sh suite was NOT executed: WSL was unavailable (E_ACCESSDENIED) and portable Bash lacked setsid.
Bash syntax checks were performed for launch_highbo.sh, run_all.sh and test_launcher.sh.
The real Python rest certificate gate WAS extracted from the pinned launcher and executed by the probe.
The full check_all.sh was NOT executed from this partial source snapshot.
The optional real-deck selftest in measure_mixing_index.py was skipped by that source's own test harness.

No actual L/LC overlap, retained-volume, or mixing-effect estimates are claimed.
The WSL v1 raw receipt and v09 PNG were not independently verified.

