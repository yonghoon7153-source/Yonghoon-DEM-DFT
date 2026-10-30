50kg Y4 draft1 review, pin 52f9e87e1

Read codex_review_kg50_y4_draft1_20261030.md first.
Verdict: conditional acceptance of scope; not final report or physical-run GO.

Reproduce after extracting this ZIP:
  python3 review_probes.py
  python3 check_prior_deck.py
Requires Python 3 and either pypdf or PyMuPDF for PDF text extraction.
No DEM, network solver, Git mutation, scheduler or network invocation occurs in these scripts.

source/ preserves the supplied archive files. independent/reference_report_20261001_draft.pptx is an additional pinned-blob-matched reference.
Remote metadata was fetched through the GitHub connector at the fixed pin; local reruns compare against the recorded metadata (no fetch).
129 assertions include 90 file identity checks and 39 numerical/representation checks, not 129 physical experiments.

SHA256SUMS.txt covers all delivered files except itself. delivery_sha256.txt sits outside the ZIP.
