set -uo pipefail
DEST="$PWD"
promoted=(fixture)
n_want=1
n_ok=1
n_bad=0
n_missing=0
index_ok=1
if [[ "${#promoted[@]}" -gt 0 ]]; then
if ! (exit 0)

then
  index_ok=0
  printf '\n  ✗ index 최종화 실패 — %s 는 갱신되지 않았다 (기존 바이트 그대로). archive 는 미완이다 (75차 G75-N1).\n' \
    "$DEST/artifact_index.yaml" >&2
  printf '    이미 승격된 묶음: %s — 승격은 되돌리지 않는다; 옛 index 와 어긋난 상태이므로 사람이 본다 (재실행하면 같은 identity 는 멱등).\n' \
    "${promoted[*]}" >&2
fi
fi

printf '\n요청 %d개 · 검증 가능 %d개 · 불완전 %d개 · 없음 %d개 · 합계 %s\n' \
  "$n_want" "$n_ok" "$n_bad" "$n_missing" "$(du -sh "$DEST" | cut -f1)"
if [[ "$index_ok" -eq 1 ]]; then
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
else
  echo "index 가 미완이므로 commit 안내를 하지 않는다 — 위 ✗ 를 먼저 해결하라 (75차 G75-N1)" >&2
fi

# ★ F71/8-4 — 하나라도 불완전하면 nonzero. 조용히 성공하면 CI·스크립트가
#   "보관됐다"고 믿는다. ★ 75차 G75-N1 — index 최종화 실패도 같은 축이다.
[[ "$n_bad" -eq 0 && "$n_missing" -eq 0 && "$index_ok" -eq 1 ]] || exit 1
