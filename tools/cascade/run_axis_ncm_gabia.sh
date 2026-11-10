#!/usr/bin/env bash
# run_axis_ncm_gabia.sh — cascade MP 닫힌계 축 러너: AXIS=ncm (기본 · 축 ① NCM 계면 분해 · D-2026-11-04-cascade-axis-ncm-interface)
#                          · AXIS=hyd (축 ② 가수분해 · D-2026-11-04-cascade-axis-hydrolysis · 같은 91 종 × H2O · 호스트 × H2O)
#                          · AXIS=li  (축 ③ Li 금속 음극 · D-2026-11-04-cascade-axis-li-anode · 같은 91 종 × Li · 호스트 × Li ·
#                                      kink 전부 기록 (--record_kinks · R3 완전 환원 끝점 산물) · 산물 MP 갭)
#                          · AXIS=vol (묶음 2 축 ⑤ ⑥ 부피 갈래 · D-2026-11-10-cascade-axes-bundle2 · 91 종 + 호스트 × 반충 · 만충 LiNiO₂ · Li ·
#                                      --record_kinks --record_volumes · G3b 재현 대조 · Li 쪽 kink 산물 MP 갭)
#                          · AXIS=win (묶음 2 축 ④ 창 갈래 · 같은 결정 · 91 종 + 호스트 단독 Li 열린계 · 8 격자 전압 · 창 산물 MP 갭)
#
# 카드: db/properties/cascade_axis_ncm_interface_estimand_2026_11_04.json §3b
#   닫힌계 pseudo-binary (M6 규약) · 91 대표 조성 × {LiNiO2, Li0.5NiO2} (1차) · {LiCoO2, Li0.5CoO2} (민감도)
#   · 호스트 Li6PS5Cl × 위 넷 + NCM811 만충/반충 (대리 점검 G6) · 산물 MP 갭 · manifest.
#   묶음 2 (AXIS=vol · win): db/properties/cascade_axes_bundle2_estimand_2026_11_10.json §3b — 출력 db/raw/cascade_axes_bundle2_<날짜>/
#   (designs_vol · host_vol · designs_win · host_win .jsonl · product_gaps_win.json · manifest.json · run.log · SHA256SUMS +
#    product_gaps_vol.json · kink_products_vol.jsonl · g3b_check.json · lane_*.log · selftest_*.log). vol 과 win 은 **같은 OUT** 에 차례로 돈다.
#
# ⛔ 이건 QE 가 아니다 — gabia CPU 파이썬 + MP 조회만 (GPU 0 · SCF 0).
# ⛔ 값은 화면에 안 낸다 — runner.log (묶음 2 는 run.log) 에는 단계 · 줄 수 · 판 일치 · 판정 (통과/불통과) 만 (판독기 커밋 전에 값을 안 본다).
#    갈래별 값 출력은 lane_*.log 에만 간다 (회수 대상 · 판독기가 읽는다).
#
# 이 스크립트가 못 하는 것:
#   · 판독 (δ · 도펀트 행방 · 등급 · ΔV/V · f_ins · 순위 · 게이트) — tools/cascade/analyze_cathode_reactivity.py 몫
#   · 오류 행 재시도 — interface_reactivity_v2 · esw_grand_potential --resume 은 오류 행도 '끝남' 으로 센다.
#     오류가 있으면 그 행을 지우고 RESUME=1 로 다시 돈다 (같은 MP 판일 때만 · 카드 §3b).
#   · MP 판이 실행 중에 바뀌는 것을 막지 못한다 — 앞 · 뒤 판을 적고 다르면 알린다 (G3).
#   · 묶음 2 의 G3b 재현 대조 · 교차 불일치 수는 적기만 한다 (판독기가 막는다) — 러너는 불통과여도 다른 갈래를 멈추지 않는다 (rc 로 알린다).
#
# 실행 (gabia · uma env):  bash tools/cascade/run_axis_ncm_gabia.sh
#   env: PY (기본 uma python) · OUT (기본 db/raw/cascade_axis_ncm_v2_2026_11_04 · 묶음 2 는 cascade_axes_bundle2_<오늘>) · RESUME=1 · DRY=1 (검사만)
#   ⭐ 묶음 2 는 OUT 을 한 번 정해 두 번 부른다: OUT=… AXIS=vol bash … && OUT=… AXIS=win bash …
#   ⭐ 2026-11-04 고침 (결과 전 · 카드 개정 1): 설계 91 = 1 단계 계면 표 (cascade_interface_90.jsonl) 의 조성 그대로.
#      첫 판 (ce4fc685) 은 --batch_from (지금 CSV 의 champion_formulas) 이라 90 종 · 그중 9 종 조성이 1 단계와 달랐다 —
#      그 판의 출력 (db/raw/cascade_axis_ncm_2026_11_04) 은 쓰지 않는다 (회수 · 판독 안 함). 새 판은 새 폴더 (v2).
set -uo pipefail
PY=${PY:-/data/apps/miniforge3/envs/uma/bin/python}
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
AXIS=${AXIS:-ncm}
B2_CARD=db/properties/cascade_axes_bundle2_estimand_2026_11_10.json
case "$AXIS" in
  ncm) DEF_OUT=$ROOT/db/raw/cascade_axis_ncm_v2_2026_11_04; DEF_DEC=D-2026-11-04-cascade-axis-ncm-interface
       CARD=db/properties/cascade_axis_ncm_interface_estimand_2026_11_04.json; LANES=(designs_lno designs_lco host); EXPECT="182 · 182 · 6" ;;
  hyd) DEF_OUT=$ROOT/db/raw/cascade_axis_hyd_2026_11_04; DEF_DEC=D-2026-11-04-cascade-axis-hydrolysis
       CARD=db/properties/cascade_axis_hydrolysis_estimand_2026_11_04.json; LANES=(designs_hyd host_hyd); EXPECT="91 · 1" ;;
  li)  DEF_OUT=$ROOT/db/raw/cascade_axis_li_2026_11_04; DEF_DEC=D-2026-11-04-cascade-axis-li-anode
       CARD=db/properties/cascade_axis_li_anode_estimand_2026_11_04.json; LANES=(designs_li host_li); EXPECT="91 · 1" ;;
  vol) DEF_OUT=$ROOT/db/raw/cascade_axes_bundle2_$(date +%Y_%m_%d); DEF_DEC=D-2026-11-10-cascade-axes-bundle2
       CARD=$B2_CARD; LANES=(designs_vol host_vol); EXPECT="273 · 3" ;;
  win) DEF_OUT=$ROOT/db/raw/cascade_axes_bundle2_$(date +%Y_%m_%d); DEF_DEC=D-2026-11-10-cascade-axes-bundle2
       CARD=$B2_CARD; LANES=(designs_win host_win); EXPECT="91 · 1" ;;
  *) echo "⛔ AXIS 는 ncm · hyd · li · vol · win 중 하나 ($AXIS) (rc 9)" >&2; exit 9 ;;
esac
OUT=${OUT:-$DEF_OUT}
DEC=${DEC:-$DEF_DEC}
B2=0; LOGF=runner.log; SHA_TOOLS="tools/oxidation/interface_reactivity_v2.py tools/oxidation/sei_product_gaps.py tools/cascade/run_axis_ncm_gabia.sh"
PAT="interface_reactivity_v2.py.*$OUT"
case "$AXIS" in vol|win)
  B2=1; LOGF=run.log                       # 카드 §3b 출력 이름 · 묶음 2 는 판독기 · 창 도구 sha 도 적는다
  SHA_TOOLS="$SHA_TOOLS tools/oxidation/esw_grand_potential.py tools/cascade/analyze_cathode_reactivity.py"
  PAT="(interface_reactivity_v2|esw_grand_potential|sei_product_gaps)\.py.*$OUT" ;;
esac
cd "$ROOT" || exit 2
log(){ echo "[$(date '+%F %T')] $*" | tee -a "$OUT/$LOGF"; }
die(){ local c=${2:-3}; echo "⛔ $1 (rc $c)" >&2; [ -d "$OUT" ] && echo "[$(date '+%F %T')] ⛔ $1 (rc $c)" >> "$OUT/$LOGF"; exit "$c"; }

# 0) 결정이 active 인가 — 아니면 시작하지 않는다
python3 - "$DEC" "$CARD" <<'EOF' || die "결정 $DEC 가 active 가 아니거나 카드가 다르다 — 비준 전에는 돌지 않는다" 10
import json, sys
d = json.load(open("db/governance/decisions.json", encoding="utf-8"))
x = [y for y in d["decisions"] if y["id"] == sys.argv[1]]
sys.exit(0 if x and x[0].get("decision_state") == "active" and x[0].get("card") == sys.argv[2] else 1)
EOF
[ -x "$PY" ] || die "파이썬이 없다: $PY (uma env 절대경로)" 11
[ -n "${MP_API_KEY:-}" ] || die "MP_API_KEY 가 환경에 없다 (tmux 는 -e MP_API_KEY=… 로 넘긴다)" 12

# 1) 중복 실행 가드 — 출력 폴더 (잡 고유) 로 잡는다 · comm 으로 파이썬만 센다
running(){ for x in $(pgrep -f "$PAT" 2>/dev/null); do
             case "$(cat /proc/$x/comm 2>/dev/null)" in python*) echo "$x";; esac; done; }
[ -z "$(running)" ] || die "이미 돌고 있다 (PID $(running | tr '\n' ' '))" 13
mkdir -p "$OUT"
RES=()
EXIST=0; for f in "${LANES[@]}"; do [ -e "$OUT/$f.jsonl" ] && EXIST=1; done
if [ "$EXIST" = 1 ]; then
  [ "${RESUME:-0}" = 1 ] || die "출력이 이미 있다 — 이어 돌리려면 RESUME=1 (오류 행은 먼저 지운다)" 14
  RES=(--resume)
fi
log "시작 · AXIS=$AXIS · 결정 $DEC active · OUT=$OUT · PY=$PY · resume=${RESUME:-0}"
[ "${DRY:-0}" = 1 ] && { log "DRY=1 — 검사만 하고 끝"; exit 0; }

# 2) 도구 selftest (오프라인) — 묶음 2 는 창 도구 · 판독기도 (판독기는 계산 전에 커밋 · selftest · 카드 §3b)
"$PY" tools/oxidation/interface_reactivity_v2.py --selftest > "$OUT/selftest_iface.log" 2>&1 \
  || die "interface_reactivity_v2 selftest 실패 — $OUT/selftest_iface.log" 15
"$PY" tools/oxidation/sei_product_gaps.py --selftest > "$OUT/selftest_gaps.log" 2>&1 \
  || die "sei_product_gaps selftest 실패 — $OUT/selftest_gaps.log" 16
if [ "$B2" = 1 ]; then
  "$PY" tools/oxidation/esw_grand_potential.py --selftest > "$OUT/selftest_esw.log" 2>&1 \
    || die "esw_grand_potential selftest 실패 — $OUT/selftest_esw.log" 20
  "$PY" tools/cascade/analyze_cathode_reactivity.py --selftest > "$OUT/selftest_reader.log" 2>&1 \
    || die "analyze_cathode_reactivity (판독기) selftest 실패 — $OUT/selftest_reader.log" 21
  log "selftest 넷 통과 (iface · gaps · esw · 판독기)"
else
  log "selftest 둘 통과"
fi

# 3) manifest — 실행 (invocation) 마다 MP 판 앞 · 뒤를 따로 남긴다 (RESUME 로 덧붙여도 G3 가 전부를 본다)
manifest(){ "$PY" - "$1" "$OUT/manifest.json" "$DEC" "$CARD" "$AXIS" "$SHA_TOOLS" <<'EOF'
import json, os, sys, hashlib, subprocess, datetime, platform
from importlib.metadata import version as _v
def version(n):
    for k in (n, n.replace("_", "-")):
        try:
            return _v(k)
        except Exception:
            pass
    return "unknown"
phase, path, dec, card, axis, tools = sys.argv[1:7]
m = json.load(open(path)) if os.path.exists(path) else {}
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
from mp_api.client import MPRester
with MPRester(os.environ["MP_API_KEY"]) as r:
    dbv = r.get_database_version()
    if phase == "before" and not m:
        es = r.get_entries_in_chemsys(["Li", "Ni", "O"],
                                      additional_criteria={"thermo_types": ["GGA_GGA+U"]})
if m and "invocations" not in m:            # 옛 판 runner 의 manifest — 첫 실행을 그대로 옮겨 적는다
    m["invocations"] = [{k: m.get(k) for k in ("started_utc", "finished_utc", "mp_db_version_before", "mp_db_version_after",
                                                "repo_head", "tools_sha16")}]
if phase == "before":
    sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()[:16]
    inv = {"started_utc": now, "host": platform.node(), "resume": os.environ.get("RESUME", "0"),
           "repo_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
           "tools_sha16": {f: sha(f) for f in tools.split()},
           "pymatgen": version("pymatgen"), "mp_api": version("mp_api"), "mp_db_version_before": dbv}
    if axis in ("vol", "win"):              # 묶음 2 — 판독기 G1 이 vol · win 두 갈래 실행을 따로 본다
        inv["axis"] = axis
    if not m:
        adj = sorted({getattr(a, "name", type(a).__name__)
                      for e in es for a in (getattr(e, "energy_adjustments", None) or [])})
        m.update({"decision": dec, "card": card, "started_utc": now, "host": platform.node(),
                  "python": sys.executable, "pymatgen": inv["pymatgen"], "mp_api": inv["mp_api"],
                  "thermo_types": ["GGA_GGA+U"], "correction_names_sample_Li-Ni-O": adj, "n_entries_sample_Li-Ni-O": len(es),
                  "tools_sha16": inv["tools_sha16"], "repo_head": inv["repo_head"], "mp_db_version_before": dbv})
    m.setdefault("invocations", []).append(inv)
else:
    m["invocations"][-1].update({"finished_utc": now, "mp_db_version_after": dbv})
    vers = {x.get(k) for x in m["invocations"] for k in ("mp_db_version_before", "mp_db_version_after")}
    m.update({"finished_utc": now, "mp_db_version_after": dbv, "same_mp_version": len(vers) == 1 and None not in vers})
json.dump(m, open(path, "w"), ensure_ascii=False, indent=1)
print("same" if m.get("same_mp_version", True) else "DIFFERENT")
EOF
}
manifest before > /dev/null || die "manifest (앞) 실패 — MP 조회 · 키 확인" 17
log "manifest 앞 기록"

# 4) 갈래 동시 — 설계 × 상대 · 호스트 × 상대
#    ⭐ 설계 = 카드 §1b 91 종 = **1 단계 계면 표 (cascade_interface_90.jsonl) 의 조성 그대로** (카드 개정 1 · 결과 전 2026-11-04):
#       champion_formulas 를 지금 CSV 에 다시 돌리면 9 종이 다른 조성 (세 라벨 중 '먼저 나온 행' 이 바뀜) 이고 As2S3 는 CSV 에 없다.
IR=tools/oxidation/interface_reactivity_v2.py
ESW=tools/oxidation/esw_grand_potential.py
ROSTER_SRC=db/properties/cascade_interface_90.jsonl
mapfile -t ROSTER < <("$PY" - "$ROSTER_SRC" <<'EOF'
import json, sys
f = {}
for ln in open(sys.argv[1], encoding="utf-8"):
    r = json.loads(ln)
    if r.get("cathode") in ("LCO", "LNO", "LMO") and r.get("formula"):
        if f.setdefault(r["species"], r["formula"]) != r["formula"]:
            sys.exit(f"{r['species']}: 양극마다 조성이 다르다")
if len(f) != 91:
    sys.exit(f"대상 {len(f)} 종 (91 이어야 한다)")
for k in sorted(f):
    print(f"{k}:{f[k]}")
EOF
)
[ "${#ROSTER[@]}" = 91 ] || die "대상 91 종을 못 읽는다 ($ROSTER_SRC → ${#ROSTER[@]} 종)" 19
B2_PARTNERS=("Li0.5NiO2:LNO_half" "LiNiO2:LNO_full" "Li:Li")                    # 카드 §3b 축_⑤_⑥_부피_갈래
B2_VOLTS=(2.50 2.75 3.00 3.25 3.50 3.75 4.00 4.25)                              # 카드 §1b 축_④ 격자 전압 8 점
if [ "$AXIS" = ncm ]; then
"$PY" $IR --only "${ROSTER[@]}" --closed "${RES[@]}" --cathodes "LiNiO2:LNO_full" "Li0.5NiO2:LNO_half" \
   --out "$OUT/designs_lno.jsonl" >> "$OUT/lane_lno.log" 2>&1 & P1=$!
"$PY" $IR --only "${ROSTER[@]}" --closed "${RES[@]}" --cathodes "LiCoO2:LCO_full" "Li0.5CoO2:LCO_half" \
   --out "$OUT/designs_lco.jsonl" >> "$OUT/lane_lco.log" 2>&1 & P2=$!
"$PY" $IR --only "HOST:Li6PS5Cl" --closed "${RES[@]}" --cathodes "LiNiO2:LNO_full" "Li0.5NiO2:LNO_half" \
   "LiCoO2:LCO_full" "Li0.5CoO2:LCO_half" "LiNi0.8Co0.1Mn0.1O2:NCM_full" "Li0.5Ni0.8Co0.1Mn0.1O2:NCM_half" \
   --out "$OUT/host.jsonl" >> "$OUT/lane_host.log" 2>&1 & P3=$!
elif [ "$AXIS" = hyd ]; then            # AXIS=hyd — 상대 H2O (카드 §1b · 같은 91 종)
"$PY" $IR --only "${ROSTER[@]}" --closed "${RES[@]}" --cathodes "H2O:H2O" \
   --out "$OUT/designs_hyd.jsonl" >> "$OUT/lane_hyd.log" 2>&1 & P1=$!
"$PY" $IR --only "HOST:Li6PS5Cl" --closed "${RES[@]}" --cathodes "H2O:H2O" \
   --out "$OUT/host_hyd.jsonl" >> "$OUT/lane_host_hyd.log" 2>&1 & P2=$!
P3=
elif [ "$AXIS" = li ]; then             # AXIS=li — 상대 Li 금속 (축 ③ 카드 §1b · §3b · 같은 91 종 · kink 전부 기록)
"$PY" $IR --only "${ROSTER[@]}" --closed --record_kinks "${RES[@]}" --cathodes "Li:Li" \
   --out "$OUT/designs_li.jsonl" >> "$OUT/lane_li.log" 2>&1 & P1=$!
"$PY" $IR --only "HOST:Li6PS5Cl" --closed --record_kinks "${RES[@]}" --cathodes "Li:Li" \
   --out "$OUT/host_li.jsonl" >> "$OUT/lane_host_li.log" 2>&1 & P2=$!
P3=
elif [ "$AXIS" = vol ]; then            # AXIS=vol — 묶음 2 ⑤ ⑥ (같은 91 종 · 세 상대 · kink 전부 · 같은 PhaseDiagram 의 구조 부피)
"$PY" $IR --only "${ROSTER[@]}" --closed --record_kinks --record_volumes "${RES[@]}" --cathodes "${B2_PARTNERS[@]}" \
   --out "$OUT/designs_vol.jsonl" >> "$OUT/lane_vol.log" 2>&1 & P1=$!
"$PY" $IR --only "HOST:Li6PS5Cl" --closed --record_kinks --record_volumes "${RES[@]}" --cathodes "${B2_PARTNERS[@]}" \
   --out "$OUT/host_vol.jsonl" >> "$OUT/lane_host_vol.log" 2>&1 & P2=$!
P3=
else                                    # AXIS=win — 묶음 2 ④ (같은 91 종 · 조성마다 자기 chemsys · Li 열린계 · 8 전압)
"$PY" $ESW --batch_from "$ROSTER_SRC" --at_voltages "${B2_VOLTS[@]}" "${RES[@]}" \
   --out "$OUT/designs_win.jsonl" >> "$OUT/lane_win.log" 2>&1 & P1=$!
"$PY" $ESW --batch_from "HOST:Li6PS5Cl" --at_voltages "${B2_VOLTS[@]}" "${RES[@]}" \
   --out "$OUT/host_win.jsonl" >> "$OUT/lane_host_win.log" 2>&1 & P2=$!
P3=
fi
log "갈래 발사 (PID $P1 $P2 $P3 · 대상 ${#ROSTER[@]} 종 · $ROSTER_SRC) — 기대 줄 수 $EXPECT"
wait $P1; R1=$?; wait $P2; R2=$?; R3=0; [ -n "$P3" ] && { wait $P3; R3=$?; }
log "갈래 끝 · rc ${LANES[*]} = $R1 $R2 $R3"

# 5) 줄 세기 (값 없이) + manifest (뒤)
"$PY" - "$OUT" "${LANES[*]}" "$R1" "$R2" "$R3" "$B2" <<'EOF' | tee -a "$OUT/$LOGF"
import json, sys, collections
out, lanes = sys.argv[1], sys.argv[2].split()
rcs = dict(zip(lanes, sys.argv[3:6]))
b2 = sys.argv[6] == "1"
m = json.load(open(f"{out}/manifest.json"))
m.setdefault("lanes", {}) if b2 else m.__setitem__("lanes", {})     # 묶음 2 는 vol · win 이 같은 manifest 에 갈래를 더한다
for k in lanes:
    rows = [json.loads(l) for l in open(f"{out}/{k}.jsonl")] if __import__("os").path.exists(f"{out}/{k}.jsonl") else []
    c = collections.Counter("error" if "error" in r else "skipped" if "skipped" in r
                            else "ok" if ("dE_eV_per_atom" in r or (r.get("mode") == "grand_potential_window"
                                                                   and isinstance(r.get("by_voltage"), dict)))
                            else "other" for r in rows)
    dup = sum(v - 1 for v in collections.Counter((r.get("species"), r.get("cathode")) for r in rows).values() if v > 1)
    m["lanes"][k] = {"rc": int(rcs[k]), "rows": len(rows), **dict(c), "duplicate_pairs": dup}
    extra = ""
    if b2:                              # 값 없이 수만 — 부피 기록 거부 · 창 교차 불일치
        vref = sum(1 for r in rows if isinstance(r.get("volumes"), dict) and r["volumes"].get("ok") is not True)
        gpx = sum(1 for r in rows for v in (r.get("by_voltage") or {}).values() if isinstance(v, dict) and v.get("gp_same") is False)
        m["lanes"][k].update({"volumes_refused": vref, "window_crosscheck_differ": gpx})
        extra = f" · 부피 거부 {vref} · 창 교차 불일치 {gpx}"
    print(f"  {k:12s} rc {rcs[k]} · 줄 {len(rows)} · " + " · ".join(f"{a} {b}" for a, b in sorted(c.items())) + f" · 중복 {dup}" + extra)
json.dump(m, open(f"{out}/manifest.json", "w"), ensure_ascii=False, indent=1)
EOF
SAME=$(manifest after) || die "manifest (뒤) 실패" 18
log "MP 판 앞뒤: $SAME"

# 6) 산물 MP 갭 (축 ① · ③ · 묶음 2 · 값은 로그 · json 에만 · 축 ② 카드는 갭을 안 쓴다) · 묶음 2 vol 은 G3b 대조 (판정만 화면에)
R4=0; R5=0
if [ "$AXIS" = ncm ]; then
"$PY" tools/oxidation/sei_product_gaps.py --from_reactions "$OUT/designs_lno.jsonl" "$OUT/designs_lco.jsonl" \
   "$OUT/host.jsonl" --out "$OUT/product_gaps.json" > "$OUT/lane_gaps.log" 2>&1; R4=$?
log "산물 갭 rc=$R4"
elif [ "$AXIS" = li ]; then
"$PY" tools/oxidation/sei_product_gaps.py --from_reactions "$OUT/designs_li.jsonl" "$OUT/host_li.jsonl" \
   --out "$OUT/product_gaps.json" > "$OUT/lane_gaps.log" 2>&1; R4=$?
log "산물 갭 rc=$R4"
elif [ "$AXIS" = vol ]; then
B1N=db/raw/cascade_axis_ncm_v2_2026_11_04; B1L=db/raw/cascade_axis_li_2026_11_04
"$PY" $IR --closed_repro "$OUT/designs_vol.jsonl" "$OUT/host_vol.jsonl" \
   --closed_repro_ref "$B1N/designs_lno.jsonl" "$B1N/host.jsonl" "$B1L/designs_li.jsonl" "$B1L/host_li.jsonl" \
   --closed_repro_out "$OUT/g3b_check.json" > "$OUT/lane_g3b.log" 2>&1; R5=$?
log "G3b 재현 대조 rc=$R5 · $(tail -n 1 "$OUT/lane_g3b.log")"
#   ⑥ 의 Li 쪽 산물 갭 — 최소 kink 만이 아니라 kink 전부 (거의 겹친 kink · 10 meV/atom 안 kink 의 ⑥ 을 판독기가 낸다).
#   sei_product_gaps --from_reactions 가 읽는 꼴로 산물 이름만 넘긴다 (부피 기록의 산물 열쇠 = 같은 hull 의 안정 엔트리 — 문자열을 다시 파싱하지 않는다).
"$PY" - "$OUT" <<'EOF' > "$OUT/lane_kink_products.log" 2>&1
import json, sys
out, n = sys.argv[1], 0
with open(f"{out}/kink_products_vol.jsonl", "w", encoding="utf-8") as fh:
    for nm in ("designs_vol", "host_vol"):
        for ln in open(f"{out}/{nm}.jsonl", encoding="utf-8"):
            r = json.loads(ln)
            v = r.get("volumes") if isinstance(r.get("volumes"), dict) else {}
            if r.get("cathode") == "Li" and v.get("ok") is True and v.get("products"):
                fh.write(json.dumps({"species": r["species"], "cathode": "Li|kink_products",
                                     "reaction": "kink_products -> " + " + ".join(sorted(v["products"]))}) + "\n")
                n += 1
print(f"Li 쪽 행 {n}")
EOF
"$PY" tools/oxidation/sei_product_gaps.py --from_reactions "$OUT/kink_products_vol.jsonl" \
   --out "$OUT/product_gaps_vol.json" > "$OUT/lane_gaps_vol.log" 2>&1; R4=$?
log "Li 쪽 kink 산물 갭 rc=$R4 · $(tail -n 1 "$OUT/lane_kink_products.log")"
elif [ "$AXIS" = win ]; then
"$PY" tools/oxidation/sei_product_gaps.py --from_reactions "$OUT/designs_win.jsonl" "$OUT/host_win.jsonl" \
   --out "$OUT/product_gaps_win.json" > "$OUT/lane_gaps_win.log" 2>&1; R4=$?
log "창 산물 갭 rc=$R4"
fi

# 7) 끝 줄을 먼저 쓰고 해시 (로그가 해시 뒤에 안 바뀌게)
log "끝 — 회수 블록은 판독기 커밋 뒤에 받는다 (카드 §8 ③)"
( cd "$OUT" && sha256sum *.jsonl *.json *.log > SHA256SUMS )
[ "$R1$R2$R3$R4$R5" = 00000 ] && [ "$SAME" = same ] || exit 4
