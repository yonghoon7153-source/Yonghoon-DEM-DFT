#!/usr/bin/env bash
# =============================================================================
# gabia_august_evidence.sh — 2026-08 서버 사용 데이터 결과지 (증빙용)
#
# 용도설명서 8월판 5트랙에 대응하는 **실제 산출 수치**를 db 에서 읽어 찍는다.
# 7월 증빙(gabia_july_evidence.sh · 5.pdf)과 같은 양식: `====` 배너 + `▶` 소제목.
#
#   cd ~/Yonghoon-DEM-DFT && bash tools/reports/gabia_august_evidence.sh
#   (한 섹션씩 캡처하려면)  bash tools/reports/gabia_august_evidence.sh 1
#
# ⚠ 값을 하드코딩하지 않는다 — db 파일에서 읽는다. 없으면 그 줄만 건너뛰고
#   무엇이 없는지 알린다(없는 값을 있는 척 찍지 않기 위해).
#
# ⛔ 이 스크립트가 **못 하는 것**
#   · 값의 옳고 그름을 판정하지 않는다. db 가 이미 내린 판정을 옮길 뿐이다.
#   · 인용 가부를 새로 정하지 않는다 — 철회·보류 표시는 db 문구 그대로 나온다.
#   · 서버 밖 산출물(외주 VASP 회신 원본 등)의 존재를 확인하지 않는다.
# =============================================================================
set -u
cd "$(dirname "$0")/../.." || exit 1
ONLY=${1:-0}
PY=${PY:-python3}
SINCE=${SINCE:-2026-08-01}
UNTIL=${UNTIL:-2026-09-01}
bar(){ printf '%s\n' "=============================================================="; }
sec(){ [ "$ONLY" = 0 ] || [ "$ONLY" = "$1" ] || return 1; bar; echo "  $2"; bar; }
sub(){ echo "▶ $*"; }
miss(){ echo "  (없음: $1)"; }
# ⚠ 하우스 CSV 는 Origin 호환으로 BOM 을 붙여 쓴다 → 첫 줄 주석이 grep -v '^#' 에
#   안 걸린다(7월판 실측). BOM 을 먼저 떼고 주석을 거른다.
nocom(){ sed '1s/^\xEF\xBB\xBF//' "$1" | grep -v '^#'; }
# JSON 에서 키 몇 개만 골라 찍는다 (파일 없으면 조용히 miss).
# ⚠ 캡처 한 장에 들어가야 하므로 키당 JMAX 줄에서 자른다 — 자른 것을 숨기지 않고
#   `… (+N 줄, 원본: <경로>)` 로 밝힌다. 전문이 필요하면 JMAX=99 로 다시 돌린다.
JMAX=${JMAX:-4}
jkeys(){ JMAX=$JMAX $PY - "$@" <<'PY'
import json, os, sys, textwrap
p, keys = sys.argv[1], sys.argv[2:]
if not os.path.exists(p):
    print("  (없음: %s)" % p); raise SystemExit
cap = int(os.environ.get("JMAX", "4"))
d = json.load(open(p, encoding="utf-8"))
for k in keys:
    if k not in d:
        continue
    v = d[k]
    v = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
    L = textwrap.wrap(v, 92) or [""]
    for i, ln in enumerate(L[:cap]):
        print(f"  {k if i==0 else '':26s} {ln}")
    if len(L) > cap:
        print(f"  {'':26s} … (+{len(L)-cap} 줄, 원본: {p})")
PY
}

# ═══ ① SDCP-LiNiO2 외주 DFT 회신 — 판정 · 마감 · 재설계 ═══════════════════
if sec 1 "① SDCP - LiNiO2(104) 외주 DFT 30잡 회신 — 자기상태 판정 · 마감 · 재설계"; then
sub "회신 원장 (외주 30잡 · OUTCAR 회수)"
jkeys db/properties/sdcp_wave1_results.json \
      title date wave bundle code n_jobs n_outcar molecule_reference_box \
      box_convergence_meV
sub "인용 확정본 — 자리 대비 dE_site (동일 자세 쌍의 수직 대비만)"
$PY - <<'PY'
import json, os
p = "db/properties/sdcp_wave1_citable.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p)
else:
    d = json.load(open(p, encoding="utf-8"))
    for k, v in (d.get("dE_site_meV") or {}).items():
        print(f"    {k:34s} {v:+9.3f} meV")
    nc = d.get("not_citable")
    if isinstance(nc, dict):
        print("  [인용 불가]")
        for k, v in list(nc.items())[:4]:
            print(f"    {k}: {str(v)[:80]}")
PY
sub "기준 슬랩 자기상태 재계산 (wave1.5 — 2단 유도 후 독립검증 3다리)"
jkeys db/properties/sdcp_wave15_basinA.json 제목 독립_검증_회신문서_아닌_OUTCAR_실측
sub "doped 캠페인 마감 (확정값 · 허용/금지 서술 · 재개 조건)"
jkeys db/properties/sdcp_doped_closed_2026_08_28.json 허용_서술_이대로만 ⛔_금지_서술
sub "neutral 접촉 기하 철회 (좌표 실측이 종전 서술을 반증)"
jkeys db/properties/sdcp_neutral_closed_2026_08_28.json ⛔_철회_접촉기전_2026_08_29
sub "후속 캠페인 사전등록 — 보고량 정의를 계산 전에 고정"
jkeys db/properties/sdcp_c12_claim_prereg_2026_08_31.json status 1_보고량
sub "번들 자체시험 · 실물 종단 검증 (VASP 본계산 착수 전 게이트)"
if [ -f tools/sdcp/vasp_handoff_bundle.py ]; then
  # ⚠ 원문 tail 을 그대로 찍으면 **음성 시험의 의도된 거부**(❌ 줄)가 마지막에 걸려
  #   실패처럼 보인다. 통과 수 · 종료코드 · 종단검증 줄로 요약한다.
  ST=$(mktemp)
  $PY tools/sdcp/vasp_handoff_bundle.py --selftest > "$ST" 2>&1; RC=$?
  echo "  자체시험 통과 $(grep -cE '^ *✔' "$ST") 건 · 종료코드 $RC \
(음성 시험 $(grep -cE '^ *❌' "$ST") 건은 **의도된 거부**라 정상)"
  grep -E 'e2e selftest' "$ST" | tail -1 | sed 's/^/  실물 종단 /'
  rm -f "$ST"
else miss tools/sdcp/vasp_handoff_bundle.py; fi
echo
fi

# ═══ ② 이온수송 통계 판정법 — 귀무분포 재정립 ═════════════════════════════
if sec 2 "② 이온수송 통계 판정법 — 귀무분포 실측으로 beta 문턱 폐기 · 유한크기"; then
sub "beta 게이트 귀무분포 (완전 Fickian 계에 우리 절편·홉 수를 넣은 거짓탈락률)"
# ⚠ head 로 자르면 **우리 운영점 행**(홉 13.9 / 8.4)이 잘려 나간다 — 요지가 그 줄이라
#   홉 수 8 이상만 뽑는다. 전 구간이 필요하면 원본 CSV 를 본다.
for f in db/properties/beta_gate_null_vs_hops_c2_origin.csv \
         db/properties/beta_gate_null_vs_hops_c4_origin.csv; do
  [ -f "$f" ] && { echo "  [$(basename "$f" .csv)]"
                   nocom "$f" | awk -F, 'NR==1 || $1+0>=8' | sed 's/^/    /'; } \
              || miss "$(basename "$f")"
done
echo "  → false_fail_pct = 참으로 Fickian 인 계를 beta>=0.8 게이트가 탈락시키는 비율"
sub "다중 시간원점(MTO) 창 스캔 — 시드 산포 축소"
jkeys db/properties/mto_window_scan_arrhenius6pt_2026_08_27.json why protocol ⛔_STATUS_2026_08_27
sub "유한크기 — 셀을 키우면 D 와 기울기가 함께 움직이는가 (3x3x1, 558원자)"
jkeys db/properties/lpsocl_box331_two_point_2026_08_31.json status 질문 예비_답 실측
jkeys db/properties/modelc_box331_600K_2026_08_27.json 결과 판정 ⛔_인용_금지
sub "아레니우스 굽음 — 전구간 단일 Ea 철회 (구간 Ea 로 분리)"
jkeys db/properties/b2o3_md_arrhenius.json ⛔_RETRACTED_2026_08_23
sub "확산영역 게이트 실계기 (MSD 창 2-50 ps 고정 · 자유절편 D)"
MSDDIR=""
for c in "$HOME/work/runs/comp2_disorder_relaxed" /root/work/runs/comp2_disorder_relaxed \
         /data/work/runs/comp2_disorder_relaxed; do
  [ -d "$c" ] && { MSDDIR="$c"; break; }
done
if [ -n "$MSDDIR" ]; then
  $PY tools/ionic/msd_diffusive_check.py --glob "$MSDDIR/d0.50_cfg*/T*/msd.json" 2>/dev/null \
    | head -12 | sed 's/^/  /'
else miss "comp2_disorder_relaxed (MD 산출 디렉토리)"; fi
echo
fi

# ═══ ③ MLIP 신뢰도 독립 정량화 ════════════════════════════════════════════
if sec 3 "③ 머신러닝 포텐셜 신뢰도 — 외부 정답지 힘 벤치마크 · 연화 · 위원회 온도스윕"; then
sub "힘 정확도 (문헌 공개 DFT 라벨이 정답지 — 우리 모델은 미학습)"
$PY - <<'PY'
import json, os
p = "db/properties/mlip_bench_li3ps4_uma.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p)
else:
    f = (json.load(open(p, encoding="utf-8")).get("results") or {}).get("forces") or {}
    if "MAE_eV_per_A" in f:
        print(f"    전체 MAE            {f['MAE_eV_per_A']*1000:8.1f} meV/A")
    for el, r in (f.get("per_element") or {}).items():
        if isinstance(r, dict) and "MAE" in r:
            print(f"    원소 {el:<16s} {r['MAE']*1000:8.1f} meV/A")
PY
sub "힘 연화(softening) — 같은 프레임 · 같은 정답지에서 두 엔진 대조"
$PY - <<'PY'
import json, os
p = "db/properties/uma_force_benchmark.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p)
else:
    d = json.load(open(p, encoding="utf-8"))
    print(f"    {'run':<22s}{'MAE eV/A':>10s}{'rel %':>8s}{'pearson r':>11s}{'softening':>11s}")
    for k, r in (d.get("runs") or {}).items():
        f = r.get("force") or {}
        if not f:
            continue
        print(f"    {k:<22s}{f.get('mae_eVA', 0):10.4f}{f.get('rel_mae_pct', 0):8.2f}"
              f"{f.get('pearson_r', 0):11.5f}{f.get('softening_slope', 0):11.4f}")
    v = d.get("★_T1b_verdict_2026_08_26")
    if v:
        print("  [T1b 판정] " + str(v)[:150])
PY
sub "위원회 온도 스윕 — 고온이 외삽인가 (절대 불일치 vs 힘크기 정규화)"
$PY - <<'PY'
import json, os
p = "db/properties/committee_temperature_sweep.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p)
else:
    d = json.load(open(p, encoding="utf-8"))
    bt = d.get("by_T") or {}
    print(f"    {'T(K)':>6s}{'n':>6s}{'힘크기':>10s}{'중앙(abs)':>11s}{'중앙(rel)':>11s}"
          f"{'고정초과':>10s}{'스케일초과':>11s}")
    for T in sorted(bt, key=int):
        r = bt[T]
        print(f"    {T:>6s}{r.get('n_frames', 0):6d}{r.get('force_scale_eV_per_A', 0):10.4f}"
              f"{r.get('median', 0):11.4f}{r.get('relative_median', 0):11.4f}"
              f"{r.get('n_above_fixed', 0):10d}{r.get('n_above_scaled', 0):11d}")
    print(f"    상대 표류(고온 vs 기준선 T{d.get('base_T')}): {d.get('relative_drift_pct', 0):+.1f} %")
    print("  [판정] " + str(d.get("verdict", ""))[:150])
PY
echo
fi

# ═══ ④ SEI 분해상 갭 · 이동장벽 · 수렴 규율 ═══════════════════════════════
if sec 4 "④ SEI 분해상 밴드갭 · NEB 셀 효과 · 미수렴 중단 판정"; then
sub "밴드갭 (고정점유 nscf VBM/CBM 고유값 — DOS 문턱 판독 금지)"
$PY - <<'PY'
import json, os
# ⚠ **정본 블록(eigenvalue_gaps_*)만** 읽는다 — electronic.json 에는 비교용 하위블록도
#   있어서 전체를 훑으면 정본이 아닌 값이 섞인다 (7월판 실측 주석).
p = "db/properties/electronic.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p)
else:
    d = json.load(open(p, encoding="utf-8"))
    for blk, v in d.items():
        if not blk.startswith("eigenvalue_gaps") or not isinstance(v, dict):
            continue
        print(f"  [{blk}]")
        for s, rec in v.items():
            if isinstance(rec, dict) and "gap_eV" in rec:
                print(f"    {s:24s} {rec['gap_eV']:.4f} eV")
PY
sub "SEI 분해상 갭 사다리 (우리 계산 — MP 값과 섞지 않는다)"
# ⚠ b2o3_sei_gaps.json 은 **MP 소환값**이다. 우리 nscf 고유값은 이 CSV 가 정본이라
#   섞어 인용하지 않는다 (파일 머리 주석이 그렇게 못박고 있다).
[ -f db/properties/sei_gap_ladder_origin.csv ] \
  && nocom db/properties/sei_gap_ladder_origin.csv | sed 's/^/    /' \
  || miss sei_gap_ladder_origin.csv
sub "NEB 셀 크기 효과 (작은 셀이 장벽을 부풀리는가 — 4화합물 6홉)"
$PY - <<'PY'
import json, os
p = "db/properties/sei_neb_uma_scout.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p)
else:
    d = json.load(open(p, encoding="utf-8"))
    print("  " + str(d.get("what", ""))[:92])
    for k in ("provisional", "not_for_publication"):
        if d.get(k):
            print(f"  [{k}] {str(d[k])[:88]}")
    runs = d.get("runs")
    rows = runs if isinstance(runs, list) else [
        dict(r, tag=k) for k, r in (runs or {}).items() if isinstance(r, dict)]
    print(f"    {'계·홉':<26s}{'셀':>10s}{'장벽 eV':>10s}")
    for r in rows[:10]:
        if not isinstance(r, dict):
            continue
        tag = str(r.get("tag") or r.get("system") or r.get("compound") or r.get("hop") or "?")
        cell = r.get("supercell") or r.get("cell") or ""
        ea = r.get("Ea_eV") or r.get("barrier_eV") or r.get("Ea_forward_eV")
        print(f"    {tag[:26]:<26s}{str(cell):>10s}"
              + (f"{ea:>10.3f}" if isinstance(ea, (int, float)) else f"{'—':>10s}"))
PY
sub "3x3x3 대형 NEB 중단 판정 (장벽은 내려가는데 힘이 역주행)"
jkeys db/properties/neb_cc333_force_history_2026_08_27.json property status ⛔_중단_근거
echo
fi

# ═══ ⑤ 거버넌스 4원장 · 자율검증 인프라 ═══════════════════════════════════
if sec 5 "⑤ 거버넌스 원장 4축 + 자율검증 인프라 + 당월 git 활동"; then
sub "원장 무결성 (판례 · 판정 · 산출물 — 매달린 간선 · 승인 지문 검사)"
if [ -f tools/db/validate_canonical.py ]; then
  $PY tools/db/validate_canonical.py 2>/dev/null | tail -4 | sed 's/^/  /'
else miss tools/db/validate_canonical.py; fi
sub "판례 원장 (승인 없이 active 불가 · proposed 는 사람이 비준)"
$PY - <<'PY'
import json, os
p = "db/governance/decisions.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p)
else:
    ds = json.load(open(p, encoding="utf-8")).get("decisions", [])
    from collections import Counter
    # ⚠ 상태 필드는 `decision_state` 가 정본이고 `status` 가 별칭이다 (둘 다 쓰인다).
    #   한쪽만 읽으면 '?' 로 찍힌다 — 실제로 그래서 2026-09-01 에 검사기 구멍을 찾았다.
    st = lambda d: d.get("decision_state", d.get("status", "?"))
    c = Counter(st(d) for d in ds)
    print(f"  결정 {len(ds)} 건 · " + " · ".join(f"{k} {v}" for k, v in sorted(c.items())))
    for d in ds[-4:]:
        print(f"    {d['id']:<44s} [{st(d)}] {str(d.get('title',''))[:44]}")
PY
sub "인용위험 원장 (인용 금지 · 보류 · 조건부를 한 곳에)"
$PY - <<'PY'
import json, os
from collections import Counter
p = "db/properties/citation_hazards.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p)
else:
    d = json.load(open(p, encoding="utf-8"))
    h = d.get("hazards", [])
    c = Counter(x.get("level") for x in h)
    print(f"  위험 {len(h)} 건 (갱신 {d.get('updated')}) · "
          + " · ".join(f"{k} {v}" for k, v in sorted(c.items())))
    for x in h[:3]:
        print(f"    [{x.get('level')}] {x.get('file')}")
        print(f"      {str(x.get('what'))[:88]}")
PY
sub "db 에 박힌 인용 규율 플래그 (결과 파일이 스스로 제약을 들고 다닌다)"
$PY - <<'PY'
import glob, json, os, re
# ⚠ cut -c 는 UTF-8 을 바이트로 잘라 글자를 깨뜨린다(7월판 실측) → 파이썬에서 자른다.
hits, files = [], set()
pat = re.compile(r"인용 금지|인용 보류|표시 전용|절대값 인용")
for p in sorted(glob.glob("db/properties/*.json")):
    try:
        txt = open(p, encoding="utf-8").read()
    except Exception:
        continue
    for m in re.finditer(r'"([A-Za-z_]+)"\s*:\s*"((?:[^"\\]|\\.)*)"', txt):
        if pat.search(m.group(2)):
            files.add(p)
            hits.append((os.path.basename(p), m.group(1), re.sub(r"\s+", " ", m.group(2))))
seen, shown = set(), []
for h in hits:
    if h[0] in seen:
        continue
    seen.add(h[0]); shown.append(h)
for f, k, v in shown[:3]:
    print(f"  [{f}] {k}")
    print(f"    {v[:96]}")
print(f"  → 인용 제약을 스스로 들고 다니는 db 항목 {len(files)} 개 / 플래그 {len(hits)} 건")
PY
sub "웹 대시보드 자동 시험 (화면과 원장의 일치를 상시 검증)"
if [ -d webapp/tests ]; then
  ( cd webapp && $PY -m pytest tests/ -q 2>&1 | tail -2 | sed 's/^/  /' )
else miss webapp/tests; fi
sub "외부 적대 리뷰 라운드 (지적 → 이행 → 기록)"
echo "  프롬프트 $(ls kb/reviews/codex_*_prompt_* 2>/dev/null | wc -l) 건 · \
회신 $(ls kb/reviews/*_reply_* 2>/dev/null | wc -l) 건 (kb/reviews/INDEX.md 가 사슬 정본)"
sub "당월 git 활동 (전량 git-tracked)"
echo "  커밋 $(git log --since=$SINCE --until=$UNTIL --oneline | wc -l) 건 · \
변경파일 $(git log --since=$SINCE --until=$UNTIL --name-only --pretty=format: | sort -u | grep -c .) 종"
echo "  db/properties 등록 항목 $(ls db/properties | wc -l) 개 · \
kb/results 기록 $(ls kb/results 2>/dev/null | wc -l) 편 · \
litdb digest $(ls litdb/papers/*.md 2>/dev/null | wc -l) 편"
sub "감시 도구 실계기 (다중 작업 생존 · 진행 판정)"
$PY tools/ionic/watch_all.py 2>/dev/null | head -12 | sed 's/^/  /'
echo
fi
