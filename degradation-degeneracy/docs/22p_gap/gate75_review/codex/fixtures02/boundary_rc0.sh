set -uo pipefail
DEST="$PWD"
promoted=(fixture)
n_want=1
n_ok=1
n_bad=0
n_missing=0
if [[ "${#promoted[@]}" -gt 0 ]]; then
  (exit 0)

fi

printf '\n요청 %d개 · 검증 가능 %d개 · 불완전 %d개 · 없음 %d개 · 합계 %s\n' \
  "$n_want" "$n_ok" "$n_bad" "$n_missing" "$(du -sh "$DEST" | cut -f1)"
cat <<'EOF'

다음:
  git add artifacts && git commit -m "chore(artifacts): 계산 결과 보관" && git push

clone 한 쪽에서 복원 + 검증:
  python -m tools.archive_bundle restore artifacts/halfcell_fit_v4
  python -c "from src.io import validate_provenance; import json; \
             print(json.dumps(validate_provenance('results/halfcell_fit_v4'), \
             ensure_ascii=False, indent=2))"
  ./run.sh --mode score --in results/halfcell_fit_v4   # 채점 이후는 몇 초다
EOF

# ★ F71/8-4 — 하나라도 불완전하면 nonzero. 조용히 성공하면 CI·스크립트가
#   "보관됐다"고 믿는다.
[[ "$n_bad" -eq 0 && "$n_missing" -eq 0 ]] || exit 1
