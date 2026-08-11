#!/usr/bin/env bash
# =============================================================================
#  archive_results.sh — 계산 결과를 **외부 clone에서 검증 가능한** 형태로 남긴다
#
#  사용:
#    ./scripts/archive_results.sh                      # 기본 실행 보관
#    ./scripts/archive_results.sh results/halfcell_v3  # 특정 실행만
#
#  왜 필요한가
#  ───────────
#  .gitignore가 results/ 와 *.parquet 을 통째로 제외한다. 용량 때문에 맞는
#  기본값이지만, 그 결과 **계산 결과가 서버에만 존재**하게 된다.
#  V100 컨테이너가 회수되면 fitting 14시간이 사라진다.
#
#  ★ F62 — 무엇을 남길지의 기준이 바뀌었다
#  ───────────────────────────────────────
#  초판의 기준은 "재생성 비용"이었다. 그래서 curves.parquet(재생성 5~8분)을
#  버렸다. 그런데 validate_provenance 는 봉인된 입력을 **다시 해시**한다 (F56).
#  재생성한 curves는 바이트가 달라서 digest가 안 맞는다 — 재생성으로 대체할 수
#  없다. manifest_start.yaml 과 attempts/ 도 마찬가지로 검증기가 디스크에서
#  직접 읽는다 (F57). half-cell 캐시는 .cache/ 가 gitignore라 저장소에 아예 없다.
#
#  즉 기준은 이제 "**clone 한 사람이 이 결과를 검증할 수 있는가**"다.
#  검증에 필요한 것은 비용과 무관하게 전부 남긴다.
#
#    fits.parquet          ★ 조건당 4~10초 × 3,069조건 = 시간 단위
#    manifest.yaml         ★ 서명·run_spec·입력 digest
#    manifest_start.yaml   ★ F57 — 검증기가 디스크에서 읽어 대조한다
#    attempts/*.yaml       ★ F57 — attempt_id 별 시작 기록
#    curves.parquet        ★ F56 — 재생성 불가(바이트가 달라진다). 19 MB지만 남긴다
#    inputs/*_ocp.json     ★ half-cell 캐시. .gitignore 때문에 동봉해야 한다
#    *_summary.yaml, 비교표, figures/*.png    작고 보고서가 읽는다
#
#    degeneracy_map / chunks / completed.jsonl   버린다 (fits에서 재생성)
#
#  복원 — 묶음은 보관 형태이고, 검증은 복원한 뒤에 한다:
#    python -m tools.archive_bundle restore artifacts/halfcell_v3
# =============================================================================
set -uo pipefail   # ★ 개별 실행 실패를 집계해야 하므로 -e 는 쓰지 않는다

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PY="${PYTHON:-python3}"
DEST="artifacts"
RUNS=("$@")
if [[ ${#RUNS[@]} -eq 0 ]]; then
  # ★ F71/8-4 — 기본 대상이 옛 v1/v2 여서, 새 실행을 묶으려던 사람이 무심코
  #   실행하면 quarantine 산출물만 다시 묶였다. 현재 pipeline 의 구조를 따른다.
  RUNS=(results/grid_curves_v3 results/grid_fit_v3 results/halfcell_fit_v3
        results/paired_fixed5_v3)
fi

mkdir -p "$DEST"
n_ok=0
n_bad=0
n_missing=0
n_want=${#RUNS[@]}

for run in "${RUNS[@]}"; do
  name="$(basename "$run")"
  if [[ ! -d "$run" ]]; then
    # ★ F89/9차 발견 10 — 기본 대상이 **전부 없어도** "검증 가능 0개, 불완전
    #   0개" + exit 0 으로 끝났다. paired 나 producer 가 보관되지 않은 상태를
    #   완료로 오인하게 된다. 요청한 artifact 가 없으면 실패다.
    printf '없음 (보관 대상 누락): %s\n' "$run"
    n_missing=$((n_missing+1))
    continue
  fi
  out="$DEST/$name"

  printf '\n── %s ──\n' "$name"

  # ★ F80/9-a — provenance.json 을 bundle **전에** 원본 실행 디렉터리에 쓴다.
  #   예전에는 bundle 뒤 묶음 안에 추가해서, 방금 만든 payload digest 목록과
  #   즉시 어긋나 **정상 묶음을 스스로 무효화**했다 (리뷰 실측).
  #   KEEP_FILES 에 provenance.json 이 있으므로 bundle 이 알아서 담는다.
  #   grid producer 는 fitting validator 가 아니라 곡선 validator 로 검증한다 (9-e).
  "$PY" - "$run" <<'PYEOF'
import json, sys
from pathlib import Path
from src.io import validate_curves_provenance, validate_provenance
from tools.archive_bundle import artifact_kind
run = Path(sys.argv[1])
v = (validate_curves_provenance(run) if artifact_kind(run) == "grid_producer"
     else validate_provenance(run))
(run / "provenance.json").write_text(
    json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"  원본 provenance: {'통과' if v['ok'] else '실패 — ' + ', '.join(v['fail'][:4])}")
PYEOF

  "$PY" -m tools.archive_bundle bundle "$run" "$out"

  ok=1
  "$PY" -m tools.archive_bundle check "$out" | sed 's/^/  /' || ok=0

  # ★ F71 — **격리 복원 검증까지 자동으로 한다.** 원본 results/ 가 남아 있는
  #   서버에서 restore→validate 하면 묶음을 전혀 확인하지 않고 원본을 다시
  #   검증할 수 있다 (8-3). 빈 임시 root 에 풀어서 거기서 검증한다.
  # 원래 상대경로 그대로 격리 root 안에 푼다 — 봉인된 입력 경로가 저장소 root
  # 기준이므로 (F65), run_dir 을 임의로 바꾸면 재해시가 어긋난다.
  iso="$(mktemp -d)"
  if "$PY" -m tools.archive_bundle restore "$out" --repo-root "$iso" >/dev/null 2>&1 \
     && "$PY" - "$iso" "$run" <<'PYEOF' | sed 's/^/  /'
import sys
from pathlib import Path
from src.io import validate_curves_provenance, validate_provenance
from tools.archive_bundle import artifact_kind, nested_runs
iso, run = Path(sys.argv[1]), sys.argv[2]
rd = iso / run
bad = []
for d in [rd] + nested_runs(rd):
    v = (validate_curves_provenance(d) if artifact_kind(d) == "grid_producer"
         else validate_provenance(d, repo_root=iso))
    tag = d.name if d != rd else "본체"
    print(f"격리 복원 검증[{tag}]: "
          + ("통과" if v["ok"] else "실패 — " + ", ".join(v["fail"][:4])))
    if not v["ok"]:
        bad.append(tag)
sys.exit(1 if bad else 0)
PYEOF
  then :; else ok=0; echo "  격리 복원 검증 실패"; fi
  rm -rf "$iso"

  if [[ "$ok" == "1" ]]; then n_ok=$((n_ok+1)); else n_bad=$((n_bad+1)); fi
  # ★ 10차 자체 확인 1 — 진본성 앵커. payload 목록의 해시 하나로 묶음 전체가
  #   고정된다. 이 묶음이 git 에 커밋되는 순간 이 값이 저장소 이력에 남아,
  #   이후의 "값 변조 + 재봉인"은 이력과의 대조로 드러난다. 리뷰 요청문에
  #   이 값을 그대로 인용할 것.
  [[ -f "$out/payload_sha256.yaml" ]] && \
    printf '  진본성 앵커 bundle_sha256: %s\n' \
      "$(sha256sum "$out/payload_sha256.yaml" | cut -c1-16)"
  printf '  용량 %s\n' "$(du -sh "$out" | cut -f1)"
done

printf '\n요청 %d개 · 검증 가능 %d개 · 불완전 %d개 · 없음 %d개 · 합계 %s\n' \
  "$n_want" "$n_ok" "$n_bad" "$n_missing" "$(du -sh "$DEST" | cut -f1)"
cat <<'EOF'

다음:
  git add artifacts && git commit -m "chore(artifacts): 계산 결과 보관" && git push

clone 한 쪽에서 복원 + 검증:
  python -m tools.archive_bundle restore artifacts/halfcell_v3
  python -c "from src.io import validate_provenance; import json; \
             print(json.dumps(validate_provenance('results/halfcell_v3'), \
             ensure_ascii=False, indent=2))"
  ./run.sh --mode score --in results/halfcell_fit_v3   # 채점 이후는 몇 초다
EOF

# ★ F71/8-4 — 하나라도 불완전하면 nonzero. 조용히 성공하면 CI·스크립트가
#   "보관됐다"고 믿는다.
[[ "$n_bad" -eq 0 && "$n_missing" -eq 0 ]] || exit 1
