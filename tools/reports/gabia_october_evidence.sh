#!/usr/bin/env bash
# =============================================================================
# gabia_october_evidence.sh — 2026-10 서버 사용 데이터 결과지 (증빙용 · 5 번 서류)
#
# 용도설명서 10월판 (kb/reports/gabia_server_usage_2026_10.txt) ①–⑤ 트랙에 대응하는 **실제 산출 기록**을 db 에서 읽고,
# gabia 런 폴더에서 잡 수·실행 시간·대표 출력 파일을 실측해 찍는다. 양식은 9월판 (gabia_september_evidence.sh · 5.pdf) 과 같다:
# 머리 상자 → `>` 소제목 → 완료 표지 · 대표 파일 `ls -l` · 산출 수 → 기록 활동 → 기간 총 실행 시간.
#
#   cd <repo> && bash tools/reports/gabia_october_evidence.sh          # 전체
#   bash tools/reports/gabia_october_evidence.sh 3                      # 한 섹션만 (캡처용 · 0–7)
#   ROOTS="/data/work/runs /root/work/runs" bash tools/reports/gabia_october_evidence.sh 7
#
# 트랙이 9월과 다르다 (① 유리 소셀 · ② Nd–CEI · ③ SEI 장벽 셀 수렴 · ④ 탄성 · ⑤ 점착·열역학 조회) — ⑦ 의 트랙 묶음은
# tools/reports/tracks_2026_10.json 을 gpu_runtime_tally.py --tracks 로 넘겨 맞춘다 (9월 기본 지도는 그대로 둔다).
#
# ⚠ 값을 하드코딩하지 않는다 — db 파일·출력 파일에서 읽는다. 없으면 그 줄만 건너뛰고 무엇이 없는지 알린다.
# ⛔ 이 스크립트가 **못 하는 것**
#   · 값의 옳고 그름을 판정하지 않는다 — db 가 이미 내린 판정을 옮길 뿐이다.
#   · 판독 전 값 (CEI 생성물 띠틈 · Li₂S 4×4×4 장벽 · 탄성 fit) 은 찍지 않는다 — 상태 · 시간 · 파일 목록만.
#     Li₂S 사슬 로그는 'activation' · 'eV' 줄을 걸러서 찍는다 (사슬이 끝나면 마지막 줄에 장벽이 찍히기 때문).
#   · 점착(W_ad) 값 · li2s 절대 수송값 · 인용위험 원장의 값은 찍지 않는다 (허용 문장만).
#   · 외주 VASP · kgy 계산은 다루지 않는다 (서버 밖 · 용도설명서도 맺음 문단에서만 이름).
#   · 런 폴더 실측 (섹션 ①–⑤ 의 파일 목록 · 섹션 7) 은 gabia 에서만 의미가 있다 — 다른 기계에서는 '(없음)' 으로 끝난다.
# =============================================================================
set -u
cd "$(dirname "$0")/../.." || exit 1
export TZ=${TZ:-Asia/Seoul}            # 기간 경계·git 날짜를 KST 로 (gabia 현지 시각과 같다)
ONLY=${1:-0}
PY=${PY:-python3}
export SINCE=${SINCE:-2026-10-01}
export UNTIL=${UNTIL:-2026-11-01}
export ROOTS=${ROOTS:-"/data/work/runs /root/work/runs"}
TRACKS_JSON=${TRACKS_JSON:-tools/reports/tracks_2026_10.json}
MTAG="${SINCE:0:4}_${SINCE:5:2}"       # 2026_10 — 리뷰 파일 이름의 달 꼬리표
DPRE="D-${SINCE:0:7}-"                 # D-2026-10- — 결정 원장 ID 머리
bar(){ printf '%s\n' "=============================================================="; }
sec(){ [ "$ONLY" = 0 ] || [ "$ONLY" = "$1" ] || return 1; bar; echo "  $2"; bar; }
sub(){ echo; echo "> $*"; }
miss(){ echo "  (없음: $1)"; }
JMAX=${JMAX:-3}
# jpath FILE 'key' 'key/sub/…' — 레코드 안의 값 하나를 (중첩 경로 허용) 88 자로 접어 JMAX 줄까지 찍는다
jpath(){ JMAX=$JMAX $PY - "$@" <<'PY'
import json, os, sys, textwrap
p, paths = sys.argv[1], sys.argv[2:]
if not os.path.exists(p):
    print("  (없음: %s)" % p); raise SystemExit
cap = int(os.environ.get("JMAX", "3"))
d = json.load(open(p, encoding="utf-8"))
for path in paths:
    v, ok = d, True
    for k in path.split("/"):
        if isinstance(v, dict) and k in v:
            v = v[k]
        else:
            ok = False; break
    if not ok:
        print(f"  (키 없음: {path} · {os.path.basename(p)})"); continue
    v = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
    L = textwrap.wrap(v, 88) or [""]
    lab = path.split("/")[-1]
    for i, ln in enumerate(L[:cap]):
        print(f"  {lab if i == 0 else '':24s} {ln}")
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
P=db/properties

# ═══ 0 머리 상자 ════════════════════════════════════════════════════════════
if sec 0 "ASSB Sulfide SE — Additive Digital-Twin Screening Platform"; then
echo "  Run: $SINCE ~ $(date -d "$UNTIL -1 day" +%F 2>/dev/null || echo 2026-10-31)  (GABIA GPU SERVER · RTX A6000 48 GB)"
echo "  host: $(hostname) · GPU: $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null | head -1 || echo '—')"
echo "  repo: $(git rev-parse --short HEAD 2>/dev/null) · 용도설명서 kb/reports/gabia_server_usage_${MTAG}.txt"
bar
fi

# ═══ ① 유리 소셀 (외부 1저자 트랙 · 10-30 마감) ═══════════════════════════════
if sec 1 "① glass small cell (Li transport) — measurable-temperature cards · track closed 10-30"; then
sub "Runs on this server — completion lines only (no β · D · MSD)"
jpath $P/lpscl_smallcell_glass_md_v2_runlog_2026_10_01.json "✅_완주_2026_10_03/gabia"
jpath $P/lpscl_glass_control_li3ps4_runlog_2026_10_05.json "✅_gabia_몫_끝_2026_10_11/seed3" "✅_gabia_몫_끝_2026_10_11/seed4" "✅_gabia_몫_끝_2026_10_11/seed5"
jpath $P/lpscl_glass_control_li3ps4_runlog_2026_10_05.json "✅_완주_600K_2026_10_14/gabia"
jpath $P/lpscl_glass_bmeas_650k_runlog_2026_10_14.json "✅_완주_gabia_2026_10_16/런"
sub "Model check — k-point DFT single point on this server (machine check against the other server)"
JMAX=2 jpath $P/lpscl_glass_model_check_runlog_2026_10_19.json "✅_sp_판독_2026_10_23/기계_대조_카드_개정_10" "✅_sp_판독_2026_10_23/대조"
sub "Closure (10-30) — allowed sentences only"
JMAX=4 jpath $P/lpscl_smallcell_glass_control_bmeasurable_closed_2026_10_30.json "2_허용_서술_이대로만"
JMAX=2 jpath $P/lpscl_smallcell_glass_track_closed_2026_10_30.json "5_재개_조건"
sub "UMA MD / quench runs on this server (runtime from result files)"
$PY - <<'PY'
import glob, json, os
rows = []
pats = ("lpscl_glass_md_v2_2026_09_30", "lpscl_glass_control_li3ps4_600K_2026_10_13", "lpscl_glass_bmeas_650K_2026_10_14")
for root in os.environ.get("ROOTS", "/data/work/runs /root/work/runs").split():
    for pat in pats:
        for p in sorted(glob.glob(f"{root}/{pat}/**/ensemble_results.json", recursive=True)):
            try:
                d = json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            rt = d.get("runtime_min")
            rows.append((os.path.relpath(p, root), f"T {d.get('temperatures')} · {d.get('prod_ps')} ps · " + (f"{rt / 60:.1f} h" if rt else "진행/중단")))
    for p in sorted(glob.glob(f"{root}/lpscl_glass_control_li3ps4_2026_10_05/**/result.json", recursive=True)):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        w = (d.get("run") or {}).get("wall_min")
        rows.append((os.path.relpath(p, root), "quench · " + (f"{w / 60:.1f} h" if w else "시간 없음")))
if not rows:
    print("  (없음: 10월 유리 런 폴더 — gabia 에서 돌릴 것)")
for rel, info in rows:
    print(f"  {rel:66s} {info}")
PY
sub "Key output files (gabia run folders)"
lsrun 2 'lpscl_glass_bmeas_650K_2026_10_14/*/*/ensemble_results.json' 'lpscl_glass_md_v2_2026_09_30/*/*/ensemble_results.json' 'li2s_k222_gabia_2026_10_23/*/*/scf.out'
fi

# ═══ ② Nd 양극 계면(CEI) ═══════════════════════════════════════════════════
if sec 2 "② Nd cathode interface (CEI) — Bader/ELF · S-vacancy · decomposition · CEI products · Methods"; then
sub "Nd Q3 Bader · ELF on this server (Sept frozen-4f structure · 120 atoms) — run lines only"
JMAX=2 jpath $P/nd_q3_bader_elf_runlog_2026_10_19.json "Bader_결과_2026_10_19/실행" "ELF_완주_2026_10_19_1736/끝"
sub "Neutral S-vacancy (closed 10-20 · SCF on this server) — allowed sentence only"
jpath $P/nd_s_vacancy_closed_2026_10_20.json "2_허용_서술(이대로만)"
sub "Closed-system decomposition driving force (DFT on the other server · hull basis queried here) — allowed sentence only"
JMAX=4 jpath $P/nd_q2_decomp_readout_2026_10_26.json "허용_문장(카드_§5·구조_결정_①)"
jpath $P/nd_q2_decomp_runlog_2026_10_23.json "✅_블록_①_회수_2026_10_23/회수"
sub "CEI products (11 phases) — polymorph · magnetism queried here · computed on the other server · read-out pending"
JMAX=2 jpath $P/cei_product_gap_runlog_2026_10_27.json "①_gabia_결과/다형" "관측_2026_10_31_2052/완주"
sub "Manuscript Methods (NdO-LPSCl1.6 · 4.5 DFT calculations · sent 10-28)"
ls -l --time-style=+"%b %d %H:%M" kb/papers/ndo_lpscl16_methods_2026_10_28.md kb/projects/handoff_ndo_methods_2026_10_28.md 2>/dev/null | sed 's/^/  /' || miss "NdO Methods 파일"
sub "Key output files (gabia run folders)"
lsrun 2 'nd_q3_elf_2026_10_19/*.out' 'nd_s_vacancy_2026_10_20/*/scf.out' 'nd_anion_removal_2026_10_19/*/scf.out'
fi

# ═══ ③ SEI 장벽 셀 크기 수렴 ═══════════════════════════════════════════════
if sec 3 "③ SEI barrier cell convergence — Li3Nd 3×3×3 control · Li2S 4×4×4 NEB"; then
sub "Li3Nd 3×3×3 pristine control relax (r2) — closed as not converged (decision 10-26)"
JMAX=4 jpath $P/li3nd_p333_control_runlog_2026_10_11.json "✅_r2_닫음_2026_10_26/닫는_숫자"
JMAX=2 jpath $P/li3nd_p333_control_runlog_2026_10_11.json "✅_r2_닫음_2026_10_26/정지"
sub "Li2S 4×4×4 (decision cell) — automatic chain on this server (no barrier values)"
JMAX=2 jpath $P/li2s_neb_cellconv_runlog_2026_10_09.json "단계_4x4x4_gabia_사슬_2026_10_30/상태" "단계_4x4x4_gabia_사슬_2026_10_30/관측/10_30_13:27:50_P1"
found=0
for d in $ROOTS; do
  R=$d/li2s_neb_cellconv_444_1027; [ -f "$R/chain.log" ] || continue; found=1
  echo "  chain.log (끝 · 'activation'·'eV' 줄 거름):"
  tail -n 6 "$R/chain.log" | grep -av "activation\|eV" | cut -c1-140 | sed 's/^/    /'
  [ -f "$R/chain_neb.log" ] && grep -a "■" "$R/chain_neb.log" | tail -n 4 | cut -c1-140 | sed 's/^/    /'
done
[ $found = 1 ] || echo "  (없음: li2s_neb_cellconv_444_1027/chain.log — gabia 에서 돌릴 것)"
sub "Key output files (gabia run folders)"
lsrun 2 'sei_control/li3nd_mp-976264_p333_r2/00_control_relax*.out' 'li2s_neb_cellconv_444_1027/neb/li2s/*/relax.out' 'li2s_neb_cellconv_444_1027/neb/li2s/neb.out'
fi

# ═══ ④ 탄성 상수 ═══════════════════════════════════════════════════════════
if sec 4 "④ elastic constants (relaxed-ion · 12 strains · QE-GPU) — fit after 12/12"; then
sub "Point states on this server"
found=0
for d in $ROOTS; do
  D=$d/elastic_modelc_2x; [ -d "$D" ] || continue; found=1
  n_ok=$(grep -la "bfgs converged" $D/strain_*.out 2>/dev/null | wc -l)
  n_all=$(ls $D/strain_*.in 2>/dev/null | wc -l)
  n_seg=$(ls $D/strain_*.out* 2>/dev/null | wc -l)
  echo "  modelc_2x: converged $n_ok / $n_all strain points · output segments $n_seg (EXIT 로 세운 뒤 이어 돈 조각 포함)"
  ls -lt --time-style=+"%b %d %H:%M" $D/strain_*.out* 2>/dev/null | head -4 | sed "s#$d/##; s/^/  /"
done
[ $found = 1 ] || echo "  (없음: elastic_modelc_2x — gabia 에서 돌릴 것)"
sub "BFGS gate amendment (10-14 · before the fit)"
JMAX=2 jpath $P/shear_b2o3_vs_lpscl16_2x_amendment_2026_10_14_bfgs_gate.json "0_관측" "1_바꾸는_것"
sub "GPU hand-over chain (10-30 · hold → GPU idle check → memory test → next job → always release)"
$PY - <<'PY'
import json, os
p = "db/governance/decisions.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p); raise SystemExit
for x in json.load(open(p, encoding="utf-8")).get("decisions", []):
    if x.get("id") == "D-2026-10-30-li2s-444-after-12p":
        print(f"  {x['id']} · {x.get('decision_state')} · " + " · ".join(str(e) for e in (x.get("evidence") or [])[:1])[:120])
PY
fi

# ═══ ⑤ 점착(W_ad) · 열역학 조회 ═══════════════════════════════════════════
if sec 5 "⑤ W_ad interface (DEM input) · thermodynamic queries"; then
sub "Adhesion pipeline ledger — systems · runs on this server (값은 결과 기록에만)"
$PY - <<'PY'
import json, os
p = "db/pipelines/adhesion_pipeline.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p); raise SystemExit
d = json.load(open(p, encoding="utf-8"))
for s in d.get("systems", []):
    print(f"  {s.get('id', '?'):6s} {s.get('state', '?'):5s} {str(s.get('title', ''))[:40]}")
since, until = os.environ.get("SINCE", "2026-10-01"), os.environ.get("UNTIL", "2026-11-01")
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
sub "SE particle pairs — UMA+D3 relax (10-01 · 8 models · W values only in the result record)"
JMAX=2 jpath $P/wad_se_pairs_uma_result_2026_10_01.json "실행/기계" "실행/시간" "실행/메모리"
sub "ESW Li2S reference correction (MP ThermoDoc query on this server)"
JMAX=2 jpath $P/esw_e2b_li2s_correction_2026_10_03.json "실행"
sub "Dopant dissolution-energy demo (UMA relax · CPU on this server)"
JMAX=2 jpath $P/cascade_dissolution_energy_demo_readout_2026_10_14.json "실행"
sub "Key output files (gabia run folders)"
lsrun 2 'wad_se_pairs_uma_2026_10_01/*' 'cascade_dissolution_2026_10_14/result/*'
fi

# ═══ ⑥ 당월 기록 활동 ═════════════════════════════════════════════════════
if sec 6 "⑥ records — git · decision ledger · reviews · literature ($SINCE ~ $UNTIL)"; then
# 얕은 clone 이어도 경계 커밋이 전부 기간 앞이면 기간 안 기록은 빠짐없다 — 그때만 센다
SHALLOW=false
if [ "$(git rev-parse --is-shallow-repository 2>/dev/null)" = true ]; then
  for c in $(cat "$(git rev-parse --git-common-dir)/shallow" 2>/dev/null); do
    [[ "$(git log -1 --format=%cs "$c" 2>/dev/null)" < "$SINCE" ]] || SHALLOW=true
  done
fi
if [ "$SHALLOW" = true ]; then echo "  commits            : (얕은 clone 이라 셀 수 없다 — 전체 clone 에서 다시 돌릴 것)"
else echo "  commits            : $(git log --since="$SINCE 00:00" --until="$UNTIL 00:00" --oneline 2>/dev/null | wc -l)"; fi
DPRE=$DPRE $PY - <<'PY'
import json, os
from collections import Counter
p, pre = "db/governance/decisions.json", os.environ["DPRE"]
if os.path.exists(p):
    ds = json.load(open(p, encoding="utf-8")).get("decisions", [])
    mon = [x for x in ds if str(x.get("id", "")).startswith(pre)]
    c = Counter(x.get("decision_state", x.get("status", "?")) for x in mon)
    print(f"  decisions ({pre[2:9]}) : {len(mon)}  (" + " · ".join(f"{k} {v}" for k, v in sorted(c.items())) + ")")
PY
echo "  review letters     : prompts $(ls kb/reviews | grep -c "_prompt_.*${MTAG}") · replies $(ls kb/reviews | grep -c "_reply_.*${MTAG}")"
[ "$SHALLOW" = true ] && echo "  literature digests : (얕은 clone — 셀 수 없다)" || \
  echo "  literature digests : $(git log --since="$SINCE 00:00" --until="$UNTIL 00:00" --diff-filter=A --name-only --format= -- 'litdb/papers/*.md' 2>/dev/null | sort -u | grep -c .)"
$PY tools/db/validate_canonical.py 2>/dev/null | tail -2 | sed 's/^/  /'
fi

# ═══ ⑦ 기간 총 실행 시간 (gabia 런 폴더 실측) ═══════════════════════════════
if sec 7 "⑦ campaign total runtime — measured from the run folders on this server"; then
any=0; for d in $ROOTS; do [ -d "$d" ] && any=1; done
if [ $any = 1 ]; then
  $PY tools/reports/gpu_runtime_tally.py --roots $ROOTS --since "$SINCE" --until "$UNTIL" --keys 2 --tracks "$TRACKS_JSON"
else
  miss "런 폴더 ($ROOTS) — gabia 에서 돌릴 것"
fi
fi
