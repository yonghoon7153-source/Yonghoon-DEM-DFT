C=fe23f2b839f0a49adb077348fec6d4c85443b62a; R=f82929b0644be39b44e9fba9ea04cf9d60de9146
FILES=$(python3 -c "import sys; sys.path.insert(0, 'scripts'); import run_network_194_parallel as N; print(' '.join(N.CODE_FILES))")
git diff --quiet 34713ac96 "$R" -- $FILES; echo "sealed32 rc=$?"
git diff --quiet 34713ac96 "$R" -- scripts/lhs_design_dataset.py scripts/g2_network_reread.py scripts/lhs_release_build.py scripts/run_network_194_parallel.py scripts/wsl_network_smoke.py; echo "tools rc=$?"
echo "C files: $(git diff --name-only "$C^" "$C" | sed 's#/tests/.*#/tests/*#' | sort -u | tr '\n' ' ')"; echo "C n_files: $(git diff --name-only "$C^" "$C" | wc -l)"
echo "R files: $(git diff --name-only "$R^" "$R" | tr '\n' ' ')"
for d in docs/reviews/lhs_network_batch_registration_20261007_g2.md docs/reviews/lhs_network_batch_registration_20261012_supp20.md; do echo "$d @R $(git show "$R:$d" | sha256sum | cut -c1-64) @34713 $(git show "34713ac96:$d" | sha256sum | cut -c1-64)"; done
echo "tool @C $(git show "$C:scripts/supp20_input_receipt.py" | sha256sum | cut -c1-64) @a76f $(git show "a76f59d0d:scripts/supp20_input_receipt.py" | sha256sum | cut -c1-64)"
python3 - <<'PY'
import sys; sys.path.insert(0, 'scripts')
import run_network_194_parallel as N, supp20_input_receipt as S
print('code_fp', N.code_fp(N.code_hashes()))
v, p = S.registration_values(); print('supp', v['code_fp'], v['code_fp_pending'], p)
v1, p1 = S.registration_values(reg_doc='docs/reviews/lhs_network_batch_registration_20261007_g2.md')
print('194', v1['code_fp'], v1['code_fp_pending'], [x for x in p1 if x.startswith('등록 문서 code_fp')])
r = S.receipt(); print('receipt', r['rc'], sorted(c['id'] for c in r['checks'] if not c['ok']), len(r['checks']))
PY
