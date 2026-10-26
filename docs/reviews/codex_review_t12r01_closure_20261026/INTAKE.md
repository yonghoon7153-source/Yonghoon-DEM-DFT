# External T12R-01 closure intake

The external [report](codex_review_t12r01_closure_20261026.md) is preserved with its
original filename and every original byte, including line endings. It is identical
to the supplied pasted report, SHA256
`33c9ed412be21bb76f798f7a76da851a15ed146e1cb27cbe9b882fc0c8164839`.

Original received archive SHA256:
`ac769edf998d83639fdd051a498bc9c989f0275d1b6726bae70042771ec4d8a3`.
Reviewed submission ZIP SHA256:
`fd52dd397e47ee93d91432b4c045c43196b51527d5c52038b4c863d233518bb7`.
The original received archive and pasted bytes are preserved outside the repository.
The reviewed pin is96f15ed17e03181b6096fb65f71ec7f577f17523; candidate3eecce8af503556b678f8f4a02343e6bce3d0b83;
basebffc42cab29da37b45f8a713e30e8572b91e7da3; consumer4c29705fa1c4ba94737a858b206fa4f4c5bb2bde.

T12R-01 is externally CLOSED only for automatic-fetch prevention during fixed
consumer snapshot reads and preservation of the52 results. Prior contract acceptance
and ULPRI-01/02 closure remain valid. Physical T12 is NOT_RUN; no P2 registration,
physical launch, broad design approval or integration validation follows from this.

This selected subset includes the raw report, scope/provenance receipts, all13 actual
condition traces/stdout/stderr,52positive/8loader/13mutant receipts, original probe and
harness files, six consumer blobs and exact object metadata. Full snapshot copies and
bulky repeated fixture/source trees are omitted. Root MANIFEST.sha256 remains the
original2217-entry archive manifest, not a manifest of this subset. Snapshot metadata
still describes the original373-member submitted ZIP.

The external harness records before/after whole-repository file hash equality. Scratch
repositories and separate before/after hash maps were intentionally excluded from the
received archive; intake verifies that recorded result and the hash comparison code,
not an independently available before/after byte comparison. Raw fetch/environment
traces and positive result/source hashes were independently checked without rerunning
completed tests. See archive-verification.json and receipt-verification.json.

The included object builder and independent offline probe retain their relative inputs.
If deliberately replayed, use a fresh extracted copy and a new output path. Existing
receipts must not be overwritten. The8/13 harness wrapper retains fixed output locations;
read its instructions and use a separate copy/new outputs before any replay. Scripts
are archived evidence, not execution authorization. The full received archive remains
the source for omitted snapshot/fixture material. No suite was rerun during intake.

Actual external execution was Windows/Python3.12.14/Git2.55.0.windows.3. Unsupported Git
behavior is explicitly mocked, not real-old-Git certification. Shared155 is submitted
log audit only; the author offline suite was source-reviewed and independently
reimplemented, not directly rerun. These scopes must remain distinct.
