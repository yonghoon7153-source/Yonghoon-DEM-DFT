# Root reproduction receipts

The six external cases were run on the original 01c1 consumer and the fixed main working tree. Both command logs and result JSON files are preserved. The first postcheck mistakenly expected one manifest per fixture; fixtures have both RJ and UT manifests. The corrected receipt rereads the same outputs using explicit RJ/UT mapping; it does not count a second CLI execution. Input CSV/manifest pairs and source freeze hashes were verified unchanged. External HOLD remains unchanged.
