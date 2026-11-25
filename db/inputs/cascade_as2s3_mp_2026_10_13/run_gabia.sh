#!/bin/bash
# cascade 1단계 보충 — 트랙 cascade (사용자 = 1저자) · 사용자 10-13 "안된거 … db 나 명령어 필요하면 얘기"
#   ① As₂S₃ 안정창 — rank_combined==1 세 행 (x020 · x050 · x100) 을 host Li24P4S20Cl4 와 같은 실행에서 잰다
#      → db/properties/oxidation_stability_cascade_as2s3_addendum_2026_10_13.json  (v3_pinned 의 90 종은 안 건드린다)
#   ② As₂S₃ 계면 — As2S3:As2Cl4Li28P2S20 (interface_reactivity_v2.champion_formulas 와 같은 규칙 = 종당 rank 1 첫 행)
#      × LiCoO2 · LiNiO2 · LiMn2O4 (2.5–4.3 V) · Li 금속 (닫힌계) · 탄소 (닫힌계) → 기존 JSONL 셋에 이어 붙인다 (--resume)
#      ⛔ --batch_from cascade_all_302 로 돌리지 않는다 — CSV 순서가 달라 기존 12 종의 조성식이 바뀐다 (10-13 확인)
#   ③ 계면 산물 밴드갭 — 고친 sei_product_gaps.py 로 다시 만든다 (HZ-cascade-product-gaps-nonground-polymorph 의 fix)
#      → db/properties/cascade_product_gaps.json 을 덮어쓴다 (옛 판은 git 이력 · 반응 출처는 run_cascade_extras.sh (B) 와 같다)
#   새 DFT 0 · GPU 안 씀 · MP 조회 + pymatgen (CPU 파이썬 하나씩 차례로)
#
# 쓰는 법 (gabia · 새 worktree 루트에서):
#   bash db/inputs/cascade_as2s3_mp_2026_10_13/run_gabia.sh --dry-run   # MP 조회 없이 키 · 모듈 · selftest · 입력 · 계획만
#   bash db/inputs/cascade_as2s3_mp_2026_10_13/run_gabia.sh             # 실행 (tmux 안에서 · 로그 = db/raw/cascade_as2s3_mp_2026_10_13/run.log)
#
# 이 스크립트가 못 하는 것
#   · MP 데이터베이스 판을 고정하지 못한다 — v3_pinned 의 90 종은 2026.04.13 판이다. 지금 판이 다르면 As₂S₃ 행은
#     다른 판에서 나온다 (manifest.json 에 판을 적는다 · 계면 JSONL 행에는 판 칸이 없다).
#   · 별도 상 표 (stability_axes) · 문헌 기준 표 (funnel) 는 안 건드린다 — 풀 목록이 고정이다.
#   · cascade_product_bvse.json (산물 BVSE) 은 다시 만들지 않는다 — 그 파일의 HOLD 는 남는다.
#   · AlI₃ 1순위 배치의 UMA 탄성 · EOS · BVS 는 GPU 일이라 여기서 안 한다.
set -euo pipefail
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
cd "$(dirname "$(realpath "$0")")/../../.."
REPO=$(pwd)
PY=${PY:-/data/apps/miniforge3/envs/uma/bin/python}
OUT=db/raw/cascade_as2s3_mp_2026_10_13
ALL=db/properties/cascade_all_302_2026_08_25.csv
WIN=db/properties/oxidation_stability_cascade_as2s3_addendum_2026_10_13.json
J90=db/properties/cascade_interface_90.jsonl; JLI=db/properties/cascade_interface_li.jsonl; JC=db/properties/cascade_interface_carbon.jsonl
GAPS=db/properties/cascade_product_gaps.json; AXES=db/properties/cascade_stability_axes.csv
HOST=Li24P4S20Cl4; SP=As2S3; FORM_EXPECT=As2Cl4Li28P2S20
mkdir -p "$OUT"; LOG=$OUT/run.log; [ "$DRY" = 1 ] && LOG=$OUT/dry_run.log
exec > >(tee -a "$LOG") 2>&1
say(){ echo "[$(date '+%F %T')] $*"; }
exec 9>/tmp/cascade_as2s3_mp_2026_10_13.lock
flock -n 9 || { say "⛔ 이미 도는 중 (lock) — 두 번 띄우지 않는다"; exit 3; }
say "== cascade As₂S₃ 보충 · $([ "$DRY" = 1 ] && echo DRY-RUN || echo 실행) · repo $(git rev-parse --short HEAD) · $REPO"

# ---- 준비 점검 (dry-run 도 여기까지는 같다) ----
[ -x "$PY" ] || { say "⛔ 파이썬 없음: $PY"; exit 2; }
"$PY" -c "import pymatgen, mp_api" 2>/dev/null || { say "⛔ $PY 에 pymatgen · mp_api 가 없다 (uma env 를 쓴다)"; exit 2; }
[ -n "${MP_API_KEY:-}${PMG_MAPI_KEY:-}" ] || { say "⛔ MP_API_KEY 가 환경에 없다"; exit 2; }
for f in "$ALL" "$J90" "$JLI" "$JC" "$GAPS" "$AXES"; do [ -s "$f" ] || { say "⛔ 입력 없음: $f"; exit 2; }; done
[ -e "$WIN" ] && { say "⛔ $WIN 가 이미 있다 — 덮어쓰지 않는다"; exit 4; }
"$PY" tools/oxidation/esw_cascade_batch.py --selftest > "$OUT/selftest_esw.txt" 2>&1 || { say "⛔ esw selftest"; tail -n 5 "$OUT/selftest_esw.txt"; exit 5; }
"$PY" tools/oxidation/interface_reactivity_v2.py --selftest > "$OUT/selftest_iface.txt" 2>&1 || { say "⛔ interface selftest"; tail -n 5 "$OUT/selftest_iface.txt"; exit 5; }
"$PY" tools/oxidation/sei_product_gaps.py --selftest > "$OUT/selftest_gaps.txt" 2>&1 || { say "⛔ product-gaps selftest"; tail -n 5 "$OUT/selftest_gaps.txt"; exit 5; }
say "selftest 셋 ✓"
"$PY" - "$ALL" "$OUT/as2s3_rows_from_all_302.csv" "$SP" "$FORM_EXPECT" "$J90" "$JLI" "$JC" <<'PY'
import csv, json, sys
sys.path.insert(0, "tools/oxidation")
src, dst, sp, fexp, *jl = sys.argv[1:]
rows = list(csv.DictReader(open(src, encoding="utf-8")))
keep = [r for r in rows if r.get("dopant") == sp]
r1 = [r["name"] for r in keep if r.get("rank_combined") == "1"]
assert len(keep) == 45 and len(r1) == 3, f"As2S3 행 {len(keep)} · rank1 {len(r1)} (기대 45 · 3)"
with open(dst, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(keep)
import interface_reactivity_v2 as I
f = I.champion_formulas(src).get(sp)
assert f == fexp, f"계면 조성식 {f} ≠ {fexp} — 원장이 바뀌었다"
done = {p: sum(1 for x in open(p, encoding="utf-8") if x.strip() and json.loads(x).get("species") == sp) for p in jl}
print(f"  안정창 대상 (rank 1): {', '.join(r1)}")
print(f"  계면 조성식 {sp}:{f} (종당 rank 1 첫 행 규칙)")
print("  JSONL 에 이미 있는 As2S3 행: " + " · ".join(f"{p.split('/')[-1]} {n}" for p, n in done.items()))
PY
say "계획 ① 안정창 → $WIN · ② 계면 LCO·LNO·LMO / Li / C → JSONL 셋에 이어 붙임 · ③ 산물 밴드갭 → $GAPS 덮어씀"
if [ "$DRY" = 1 ]; then say "DRY-RUN 끝 (MP 조회 0) ✅"; exit 0; fi

# ---- 실행 ----
T0=$(date +%s)
DBV=$("$PY" -c "import os; from mp_api.client import MPRester; k=os.environ.get('MP_API_KEY') or os.environ.get('PMG_MAPI_KEY'); m=MPRester(k); print(m.get_database_version())" 2>/dev/null || echo unknown)
say "MP 데이터베이스 판 = $DBV (v3_pinned 90 종 = 2026.04.13)"
n_before(){ grep -c . "$1" || true; }
B90=$(n_before "$J90"); BLI=$(n_before "$JLI"); BC=$(n_before "$JC")
say "① 안정창"
"$PY" tools/oxidation/esw_cascade_batch.py --csv "$OUT/as2s3_rows_from_all_302.csv" --rank 1 --host "$HOST" --out "$WIN"
say "② 계면 — 양극 셋 (grand potential · 2.5–4.3 V)"
"$PY" tools/oxidation/interface_reactivity_v2.py --only "$SP:$FORM_EXPECT" --resume \
  --cathodes LiCoO2:LCO LiNiO2:LNO LiMn2O4:LMO --voltages 2.5 3.0 3.5 4.0 4.3 --out "$J90"
say "② 계면 — Li 금속 (닫힌계)"
"$PY" tools/oxidation/interface_reactivity_v2.py --only "$SP:$FORM_EXPECT" --resume --closed --cathodes "Li:Li_metal" --out "$JLI"
say "② 계면 — 탄소 (닫힌계)"
"$PY" tools/oxidation/interface_reactivity_v2.py --only "$SP:$FORM_EXPECT" --resume --closed --cathodes "C:carbon" --out "$JC"
say "③ 계면 산물 밴드갭 (고친 도구로 다시 만듦)"
"$PY" tools/oxidation/sei_product_gaps.py --from_reactions "$AXES" "$J90" "$JLI" --out "$GAPS"
"$PY" - "$OUT/manifest.json" "$DBV" "$T0" "$B90" "$BLI" "$BC" "$J90" "$JLI" "$JC" "$GAPS" "$WIN" <<'PY'
import hashlib, json, subprocess, sys, time
out, dbv, t0, b90, bli, bc, j90, jli, jc, gaps, win = sys.argv[1:]
def n(p): return sum(1 for x in open(p, encoding="utf-8") if x.strip())
def sha16(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
g = json.load(open(gaps, encoding="utf-8")).get("gaps", {})
rows = g.values() if isinstance(g, dict) else g
nonground = sum(1 for r in rows if isinstance(r, dict) and (r.get("e_above_hull") or 0) > 0)
w = json.load(open(win, encoding="utf-8")).get("results", {})
m = {"date": time.strftime("%Y-%m-%d %H:%M:%S"), "repo_head": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
     "mp_db_version": dbv, "v3_pinned_db_version": "2026.04.13", "seconds": int(time.time()) - int(t0),
     "window": {"file": win, "rows": {k: {x: v.get(x) for x in ("dopant", "window_V", "reduction_limit_V", "oxidation_limit_V", "db_version", "error") if x in v} for k, v in w.items()}},
     "interface_rows_added": {j90: n(j90) - int(b90), jli: n(jli) - int(bli), jc: n(jc) - int(bc)},
     "product_gaps": {"file": gaps, "n_formulas": len(g), "n_e_above_hull_gt_0": nonground, "sha16": sha16(gaps)},
     "tools_sha16": {t: sha16(t) for t in ("tools/oxidation/esw_cascade_batch.py", "tools/oxidation/interface_reactivity_v2.py", "tools/oxidation/sei_product_gaps.py")},
     "not_done": ["stability_axes · funnel 표 (풀 고정)", "cascade_product_bvse.json (HOLD 유지)", "AlI3 1순위 배치 UMA 탄성·EOS·BVS (GPU)"]}
json.dump(m, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps({k: m[k] for k in ("mp_db_version", "seconds", "interface_rows_added", "product_gaps")}, ensure_ascii=False))
PY
say "끝 ✅ — 올릴 파일: $WIN · $J90 · $JLI · $JC · $GAPS · $OUT/"
