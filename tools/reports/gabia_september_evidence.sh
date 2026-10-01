#!/usr/bin/env bash
# =============================================================================
# gabia_september_evidence.sh — 2026-09 서버 사용 데이터 결과지 (증빙용)
#
# 용도설명서 9월판 ①–⑤ 트랙에 대응하는 **실제 산출 기록**을 db 에서 읽고, gabia 런 폴더에서
# 잡 수·실행 시간·대표 출력 파일을 실측해 찍는다. 양식은 사용자가 준 5.pdf (DEM 캠페인 요약):
# 머리 상자(캠페인 · 기간 · 자원) → `>` 소제목 → 완료 표지 · 대표 파일 `ls -l` · 산출 수 → 기간 총 실행 시간.
#
#   cd <repo> && bash tools/reports/gabia_september_evidence.sh          # 전체
#   bash tools/reports/gabia_september_evidence.sh 3                       # 한 섹션만 (캡처용 · 0–7)
#   ROOTS="/data/work/runs /root/work/runs" bash tools/reports/gabia_september_evidence.sh 7
#
# ⚠ 값을 하드코딩하지 않는다 — db 파일·출력 파일에서 읽는다. 없으면 그 줄만 건너뛰고 무엇이 없는지 알린다.
# ⛔ 이 스크립트가 **못 하는 것**
#   · 값의 옳고 그름을 판정하지 않는다 — db 가 이미 내린 판정을 옮길 뿐이다.
#   · 외주 VASP 계산은 다루지 않는다 (서버 밖 · 용도설명서 9월판에서도 뺐다 — 사용자 10-01).
#   · 점착(W_ad) 값은 찍지 않는다 — 결과 기록이 게재를 라벨 문장으로만 허용한다 (상태·잡 수·게이트만).
#   · li2s 유리는 외부 1저자 트랙이다 — 마감 기록의 허용 서술과 게이트 판정량만 옮긴다.
#   · 런 폴더 실측(섹션 7)은 gabia 에서만 의미가 있다 — 다른 기계에서는 '(없음)' 으로 끝난다.
# =============================================================================
set -u
cd "$(dirname "$0")/../.." || exit 1
ONLY=${1:-0}
PY=${PY:-python3}
export SINCE=${SINCE:-2026-09-01}
export UNTIL=${UNTIL:-2026-10-01}
export ROOTS=${ROOTS:-"/data/work/runs /root/work/runs"}
bar(){ printf '%s\n' "=============================================================="; }
sec(){ [ "$ONLY" = 0 ] || [ "$ONLY" = "$1" ] || return 1; bar; echo "  $2"; bar; }
sub(){ echo; echo "> $*"; }
miss(){ echo "  (없음: $1)"; }
JMAX=${JMAX:-3}
jkeys(){ JMAX=$JMAX $PY - "$@" <<'PY'
import json, os, sys, textwrap
p, keys = sys.argv[1], sys.argv[2:]
if not os.path.exists(p):
    print("  (없음: %s)" % p); raise SystemExit
cap = int(os.environ.get("JMAX", "3"))
d = json.load(open(p, encoding="utf-8"))
for k in keys:
    if k not in d:
        print(f"  (키 없음: {k} · {os.path.basename(p)})"); continue
    v = d[k]
    v = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
    L = textwrap.wrap(v, 88) or [""]
    for i, ln in enumerate(L[:cap]):
        print(f"  {k if i == 0 else '':24s} {ln}")
    if len(L) > cap:
        print(f"  {'':24s} … (+{len(L) - cap} 줄, 원본: {p})")
PY
}
# gabia 런 폴더의 대표 파일 (최근 것부터 N 개) — 폴더가 없으면 (없음)
lsrun(){ local n=$1; shift; local found=0
  for g in "$@"; do
    for d in $ROOTS; do
      for f in $(ls -1td $d/$g 2>/dev/null | head -"$n"); do
        found=1; ls -l --time-style=+"%b %d %H:%M" "$f" 2>/dev/null | sed "s#$d/##; s/^/  /"
      done
    done
  done
  [ $found = 1 ] || echo "  (없음: 이 기계에 ${*} 가 없다 — gabia 에서 돌릴 것)"; }

# ═══ 0 머리 상자 ════════════════════════════════════════════════════════════
if sec 0 "ASSB Sulfide SE — Additive Digital-Twin Screening Platform"; then
echo "  Run: $SINCE ~ $(date -d "$UNTIL -1 day" +%F 2>/dev/null || echo 2026-09-30)  (GABIA GPU SERVER · RTX A6000 48 GB)"
echo "  host: $(hostname) · GPU: $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null | head -1 || echo '—')"
echo "  repo: $(git rev-parse --short HEAD 2>/dev/null) · 용도설명서 kb/reports/gabia_server_usage_2026_09.txt"
bar
fi

# ═══ ① 점착(W_ad) — DEM 협업 입력 ═══════════════════════════════════════════
if sec 1 "① W_ad interface (DEM input) — UMA+D3 relax · memory probes · interface DFT"; then
sub "Adhesion pipeline ledger — systems · runs on this server (값은 결과 기록에만)"
$PY - <<'PY'
import json, os
p = "db/pipelines/adhesion_pipeline.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p); raise SystemExit
d = json.load(open(p, encoding="utf-8"))
for s in d.get("systems", []):
    print(f"  {s.get('id', '?'):6s} {s.get('state', '?'):5s} {str(s.get('title', ''))[:40]}")
since, until = os.environ.get("SINCE", "2026-09-01"), os.environ.get("UNTIL", "2026-10-01")
from collections import Counter
for r in d.get("runs", []):
    if "gabia" not in str(r.get("machine", "")) or not (since <= str(r.get("started", ""))[:10] < until):
        continue                                   # 이 서버 · 이 기간에 시작한 run 만
    jobs = [j for j in (r.get("jobs") or []) if isinstance(j, dict)]
    c = Counter(j.get("state", "?") for j in jobs)
    wall = sum(j.get("wall_s") or 0 for j in jobs) / 3600
    print(f"  run {r.get('id')}: jobs {len(jobs)} (" + " · ".join(f"{k} {v}" for k, v in sorted(c.items())) + ")"
          + (f" · wall {wall:.1f} h" if wall else "") + f" · started {r.get('started', '—')}")
PY
sub "A′ S2 — UMA+D3 interface relaxations (12 models → candidates · excluded)"
jkeys db/properties/wad_aprime_s2_result_2026_09_25.json S2_실행 판정_카드_G2_그대로
sub "Pre-run memory probes (QE CPU estimate · gabia · PID kill after the estimate line)"
$PY - <<'PY'
import json, os
p = "db/raw/wad_aprime_s3_probe_2026_09_25/probe_cpu_e70_2026_09_25.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p); raise SystemExit
d = json.load(open(p, encoding="utf-8"))
for k, r in (d.get("results") or {}).items():
    print(f"  {k:34s} nat {r.get('nat', '—'):>4} · nbnd {r.get('nbnd', '—'):>5} · RAM total {r.get('ram_total_GB', '—')} GB")
print("  → 48 GB GPU 한 장에 안 드는 모형은 이 서버에서 돌리지 않았다 (프로브만)")
PY
sub "V4 benzene-fragment interface DFT (QE-GPU · 9 jobs) — status · gates only"
jkeys db/properties/wad_aprime_pilot_result_v4_2026_09_28.json status G3_끝점_조각 G4_수치_조각
sub "Key output files (gabia run folders)"
lsrun 2 'wad_aprime_s4_v4_2026_09_27/*/pw.out' 'wad_aprime_s2_relax_2026_09_25/*/*/relax/relax_meta.json'
fi

# ═══ ② Nd 양극 계면(CEI) ═══════════════════════════════════════════════════
if sec 2 "② Nd cathode interface (CEI) — band gaps · LOBSTER · additivity · hull scans"; then
sub "Discriminating-species band gaps (fixed-occupation nscf · gabia)"
$PY - <<'PY'
import json, os
p = "db/properties/cei_gap_results_2026_09_19.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p); raise SystemExit
d = json.load(open(p, encoding="utf-8"))
print(f"  {'phase':14s}{'gap eV':>9s}{'MP eV':>9s}{'diff %':>9s}")
for r in d.get("rows", []):
    print(f"  {str(r.get('phase')):14s}{r.get('gap_eV', 0):9.3f}{r.get('mp_ref_eV', 0):9.3f}{r.get('diff_pct', 0):9.2f}")
a = (d.get("집계") or {}).get("재현_9종") or {}
print(f"  → 재현 {a.get('n')} 종 · 평균 offset {a.get('mean_offset_eV')} eV · 최대 {a.get('max_abs_diff_pct')} %")
PY
sub "Li-matched additivity GA (pre-registered · gabia 2026-09-29)"
$PY - <<'PY'
import json, os
p = "db/properties/cei_ga_verdicts_2026_09_29.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p); raise SystemExit
d = json.load(open(p, encoding="utf-8"))
g0 = d.get("G0_reproduce") or {}
print(f"  G0 reproduce : {g0.get('verdict')} (compared {g0.get('n_compared')} · max |Δ| {g0.get('max_abs_delta')})")
for site, r in (d.get("GA_additivity") or {}).items():
    print(f"  GA {site:3s}       : residual {r.get('residual'):+.6f} vs tol {r.get('tol')} → {'PASS' if r.get('pass') else 'FAIL'} (cells {r.get('n_cells')})")
PY
sub "Protection all-cells round (4 cathodes × 6 V × 5 x)"
jkeys db/properties/cei_protection_allcells_result_2026_09_21.json 집계
sub "Nd–S bonding (ICOHP · PP swap) — cause closed"
jkeys db/properties/nd_icohp_pp_swap_closed_2026_09_24.json 답 확정값
sub "Key output files (gabia run folders)"
lsrun 2 'cei_gap/*/gap.json' 'cei_ga_2026_09_29/*.log' 'nd_ppswap_2026_09_16/*/lobsterout'
fi

# ═══ ③ 유리 소셀 (외부 1저자 트랙) ═════════════════════════════════════════
if sec 3 "③ glass small cell (Li transport) — rules by the external first author"; then
sub "UMA vs QE force check (120-atom glass · closed 09-18)"
jkeys db/properties/lpscl_smallcell_closed_2026_09_18.json 1_확정값
sub "NEB branch (closed 09-19)"
jkeys db/properties/lpscl_smallcell_neb_closed_2026_09_19.json 1_확정값
sub "Glass equilibrium MD — gate counts · closure 09-30 (allowed sentence only)"
JMAX=4 jkeys db/properties/lpscl_smallcell_glass_md_closed_2026_09_30.json 2_허용_서술_이대로만
sub "Main runs on this server (UMA MD · runtime from ensemble_results.json)"
$PY - <<'PY'
import glob, json, os
rows = []
for root in os.environ.get("ROOTS", "/data/work/runs /root/work/runs").split():
    for p in sorted(glob.glob(f"{root}/lpscl_glass_md_main_2026_09_28/*/ensemble_results.json")):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        rows.append((os.path.relpath(p, root), d.get("temperatures"), d.get("prod_ps"), d.get("runtime_min")))
if not rows:
    print("  (없음: lpscl_glass_md_main_2026_09_28 — gabia 에서 돌릴 것)")
for rel, T, ps, rt in rows:
    print(f"  {rel:60s} T {T} · {ps} ps · {('%.1f h' % (rt / 60)) if rt else '진행/중단'}")
PY
fi

# ═══ ④ 결정계 수송 · 골격 · 탄성 ══════════════════════════════════════════
if sec 4 "④ crystalline transport · framework · elastic"; then
sub "3×3×1 (558-atom) 400 ps campaigns — status · seeds (Ea 는 계 간 상대차로만 인용 · 여기선 안 찍음)"
$PY - <<'PY'
import json, os
p = "db/properties/canonical_registry.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p); raise SystemExit
for e in json.load(open(p, encoding="utf-8")).get("entries", []):
    if str(e.get("system", "")).endswith("box331_cell_conditioned"):
        print(f"  {e['system']:34s} {e.get('status')} · n_seed {str(e.get('n_seed'))[:40]}")
q = "db/properties/lpsocl_box331_closed_2026_09_11.json"
if os.path.exists(q):
    r = json.load(open(q, encoding="utf-8")).get("확정값_갱신_2026_09_23_R5") or {}
    new = (r.get("새_확정값") or {}).get("값_eV"); old = r.get("종전_값")
    try:
        oldv = float(str(old).split()[0])
        print(f"  seed extension 3 → 5 (LPSOCl): Δ = {1000 * (new - oldv):+.2f} meV  (마감 그대로 · 확정값만 갱신)")
    except Exception:
        print("  (R5 갱신 줄을 못 읽었다)")
PY
sub "B2O3 framework-site event rate (sealed statements · 15 runs)"
JMAX=2 jkeys db/properties/b2o3_framework_event_rate_result_2026_09_26.json "대조군(카드)" 허용_서술
sub "UMA vs DFT framework forces (b2o3 vs control)"
jkeys db/properties/b2o3_uma_vs_dft_force_result_2026_09_11.json ★_판정_봉인문구_그대로
sub "modelc band gap — fixed-occupation nscf recalculation (gabia gap_nscf)"
$PY - <<'PY'
import json, os
p = "db/properties/canonical_registry.json"
for e in json.load(open(p, encoding="utf-8")).get("entries", []) if os.path.exists(p) else []:
    m = e.get("method_integrity_flag")
    if e.get("system") == "modelc" and isinstance(m, dict):
        print(f"  modelc gap {e.get('value')} {e.get('unit', 'eV')} · {e.get('status')} · {str(m.get('severity'))[:40]}")
PY
lsrun 1 'gap_nscf/modelc/nscf_gap.out'
sub "Elastic constants (relaxed-ion · 12 strains · QE-GPU) — point states on this server"
found=0
for d in $ROOTS; do
  D=$d/elastic_modelc_2x; [ -d "$D" ] || continue; found=1
  n_ok=$(grep -la "bfgs converged" $D/strain_*.out 2>/dev/null | wc -l)
  n_all=$(ls $D/strain_*.in 2>/dev/null | wc -l)
  n_seg=$(ls $D/strain_*.out* 2>/dev/null | wc -l)
  echo "  modelc_2x: converged $n_ok / $n_all strain points · output segments $n_seg (EXIT 로 세운 뒤 이어 돈 조각 포함)"
  ls -lt --time-style=+"%b %d %H:%M" $D/strain_*.out* 2>/dev/null | head -3 | sed "s#$d/##; s/^/  /"
done
[ $found = 1 ] || echo "  (없음: elastic_modelc_2x — gabia 에서 돌릴 것)"
lsrun 2 'b2o3_221_eventrate_400ps/*/ensemble_results.json'
fi

# ═══ ⑤ SDCP 자가도핑 (분자) ═══════════════════════════════════════════════
if sec 5 "⑤ SDCP self-doping — oxidized oligomer n = 1 → 6 (r2SCAN-3c · CPU)"; then
sub "Hole partition by chain length (SO3 vs thiophene backbone · molecular model level)"
$PY - <<'PY'
import json, os
p = "db/properties/sdcp_nseries_spin_2026_09_08.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p); raise SystemExit
d = json.load(open(p, encoding="utf-8"))
print(f"  {'n':>3s}  {'site':8s}{'SO3 %':>8s}{'backbone %':>12s}")
for r in d.get("값", []):
    print(f"  {r.get('n'):>3}  {str(r.get('site')):8s}{r.get('SO3_pct', 0):8.1f}{r.get('backbone_pct', 0):12.1f}")
PY
sub "Key output files (gabia run folders · ORCA)"
lsrun 2 'sdcp_n6b/*.out' 'sdcp_n6c/*.out'
fi

# ═══ ⑥ 당월 기록 활동 ═════════════════════════════════════════════════════
if sec 6 "⑥ records — git · decision ledger · reviews · literature ($SINCE ~ $UNTIL)"; then
SHALLOW=$(git rev-parse --is-shallow-repository 2>/dev/null)
if [ "$SHALLOW" = true ]; then echo "  commits            : (얕은 clone 이라 셀 수 없다 — 전체 clone 에서 다시 돌릴 것)"
else echo "  commits            : $(git log --since="$SINCE 00:00" --until="$UNTIL 00:00" --oneline 2>/dev/null | wc -l)"; fi
$PY - <<'PY'
import json, os
from collections import Counter
p = "db/governance/decisions.json"
if os.path.exists(p):
    ds = json.load(open(p, encoding="utf-8")).get("decisions", [])
    sep = [x for x in ds if str(x.get("id", "")).startswith("D-2026-09-")]
    c = Counter(x.get("decision_state", x.get("status", "?")) for x in sep)
    print(f"  decisions (Sep)    : {len(sep)}  (" + " · ".join(f"{k} {v}" for k, v in sorted(c.items())) + ")")
PY
echo "  review letters     : prompts $(ls kb/reviews | grep -c '_prompt_.*2026_09') · replies $(ls kb/reviews | grep -c '_reply_.*2026_09')"
[ "$SHALLOW" = true ] && echo "  literature digests : (얕은 clone — 셀 수 없다)" || \
  echo "  literature digests : $(git log --since="$SINCE 00:00" --until="$UNTIL 00:00" --diff-filter=A --name-only --format= -- 'litdb/papers/*.md' 2>/dev/null | sort -u | grep -c .)"
$PY tools/db/validate_canonical.py 2>/dev/null | tail -2 | sed 's/^/  /'
fi

# ═══ ⑦ 기간 총 실행 시간 (gabia 런 폴더 실측) ═══════════════════════════════
if sec 7 "⑦ campaign total runtime — measured from the run folders on this server"; then
any=0; for d in $ROOTS; do [ -d "$d" ] && any=1; done
if [ $any = 1 ]; then
  $PY tools/reports/gpu_runtime_tally.py --roots $ROOTS --since "$SINCE" --until "$UNTIL" --keys 2
else
  miss "런 폴더 ($ROOTS) — gabia 에서 돌릴 것"
fi
fi
