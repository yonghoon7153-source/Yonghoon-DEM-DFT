#!/bin/bash
# watch_all.sh — gabia 전체 작업 한 화면. 관례: watch -n 30 bash tools/ionic/watch_all.sh
# 커버: ① comp2 disorder MD ② SDCP relax ③ MLIP 위원회 온도 스윕 ④ 체인 게이트
#
# ⚠ JSON 은 grep 이 아니라 python 으로 판다. grep '"median"' | head -1 은 중첩 JSON 에서
#   **다른 블록의 첫 median** 을 집어 조용히 틀린 값을 띄운다(실제로 겪음 — 프레임 단위
#   중앙값 대신 mace|sevennet 쌍 중앙값이 표시됐다).
set +e
W=$HOME/work
PY=$(command -v python3)
echo "=============== gabia 전체 상황  $(date '+%m-%d %H:%M') ==============="

GPU=$(nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total \
      --format=csv,noheader,nounits 2>/dev/null)
echo "GPU: ${GPU:-(조회 실패)}   [util%, used MiB, total MiB]"
echo "  pw.x $(pgrep -x pw.x >/dev/null && echo ALIVE || echo '-')  ·  \
MLIP-MD $(pgrep -f 'aimd_mlip|disorder_ensemble_diffusion' >/dev/null && echo ALIVE || echo '-')"
echo "----------------------------------------------------------------------"

# ── ① comp2 disorder ensemble ─────────────────────────────────────────
# 결과 파일 이름을 가정하지 않고 **찾는다** (aimd_results.json / ensemble_results.json 등)
echo "① comp2 DISORDER ensemble"
$PY - "$W" <<'PYC' 2>/dev/null || echo "  (파싱 실패)"
import json, os, re, sys, glob
W = sys.argv[1]
roots = sorted(glob.glob(os.path.join(W, "runs", "comp2_disorder*")))
if not roots:
    print("  (comp2_disorder* 디렉터리 없음)")
for r in roots:
    print(f"  [{os.path.basename(r)}]")
    cfgs = sorted(glob.glob(os.path.join(r, "d*_cfg*")))
    if not cfgs:
        print("    (cfg 디렉터리 없음)")
    for c in cfgs:
        line, n = f"    {os.path.basename(c)} :", 0
        for T in (600, 800, 1000):
            # 온도 디렉터리 아래 어떤 이름이든 sigma 를 담은 json 을 찾는다
            hit = None
            for f in glob.glob(os.path.join(c, f"T{T}", "*.json")):
                try:
                    d = json.load(open(f))
                except Exception:
                    continue
                s = d.get("sigma_NE_Scm_Li")
                if s is not None:
                    hit = s
                    break
            if hit is not None:
                line += f" {T}K✓({hit:.3e})"; n += 1
            else:
                line += f" {T}K·"
        print(f"{line}  [{n}/3]")
PYC
echo "  ordered baseline: comp2 Ea 0.276±0.033 / comp1 0.253  (disorder가 낮추면 가설 확증)"
echo "----------------------------------------------------------------------"

# ── ② SDCP relax ──────────────────────────────────────────────────────
echo "② SDCP complex_doped_v2 relax (k 2×2×1)"
# 실행 중인 pw.x 의 열린 파일에서 .out 을 역추적 — 경로를 추측하지 않는다
SO=$(for p in $(pgrep -x pw.x); do
       ls -l /proc/$p/fd 2>/dev/null | grep -o '/[^ ]*\.out$'
     done | head -1)
[ -z "$SO" ] && SO=$(ls -t $(find "$HOME" /data -maxdepth 5 -name "*.out" -newermt '-2 days' \
                    -path '*sdcp*' 2>/dev/null) 2>/dev/null | head -1)
if [ -n "$SO" ] && [ -f "$SO" ]; then
  echo "  out: $SO"
  grep -a "number of k points" "$SO" | tail -1 | sed 's/^/  /'
  echo "  완료 step별 반복수 (maxstep과 같으면 **가짜 수렴**):"
  grep -a "convergence has been achieved in" "$SO" | tail -3 | sed 's/^/    /'
  grep -a "iteration #\|estimated scf accuracy" "$SO" | tail -2 | sed 's/^/    /'
else
  echo "  (out 못 찾음. 수동 지정: export SDCP_OUT=/경로/파일.out)"
  [ -n "$SDCP_OUT" ] && [ -f "$SDCP_OUT" ] && \
    grep -a "iteration #\|estimated scf accuracy" "$SDCP_OUT" | tail -2 | sed 's/^/    /'
fi
echo "----------------------------------------------------------------------"

# ── ③ MLIP 위원회 온도 스윕 (T1) ──────────────────────────────────────
echo "③ MLIP 위원회 온도 스윕 — T1 외삽 대리지표"
echo "   기준선(600 K 교정): 프레임 중앙 0.3175 · p95 0.3669 eV/Å"
$PY - "$W" <<'PYC' 2>/dev/null || echo "  (파싱 실패)"
import json, os, sys, glob
W = sys.argv[1]
ds = sorted(glob.glob(os.path.join(W, "committee_modelc_T*")),
            key=lambda p: int(p.rsplit("_T", 1)[1]))
if not ds:
    print("  (아직 없음)")
for d in ds:
    T = d.rsplit("_T", 1)[1]
    n = len(glob.glob(os.path.join(d, "pred_*.npz")))
    v = os.path.join(d, "committee_verdict.json")
    if not os.path.exists(v):
        print(f"  T{T}: 엔진 {n}/3 · 판정 대기"); continue
    try:
        j = json.load(open(v))
    except Exception:
        print(f"  T{T}: 엔진 {n}/3 · JSON 파싱 실패"); continue
    # ⚠ 반드시 committee_frame_disagreement 에서 — 최상위 first-match 는 쌍별 값이다
    c = j.get("committee_frame_disagreement", {})
    mode = (j.get("mode") or "")
    tag = "탐지" if mode.startswith("탐지") else ("교정" if mode.startswith("교정") else "?")
    med, ab = c.get("median"), c.get("n_above_break")
    nf = j.get("n_frames", "?")
    mark = ""
    if tag == "탐지" and isinstance(ab, int) and isinstance(nf, int) and nf:
        r = ab / nf
        mark = "  ⚠⚠ 급증" if r > 0.25 else ("  ⚠ 증가" if r > 0.10 else "  ok")
    print(f"  T{T}: 엔진 {n}/3 · 프레임중앙 {med if med is None else round(med,4)}"
          f" · break초과 {ab}/{nf} · [{tag}]{mark}")
PYC
echo "   ⚠ '교정'의 초과는 정의상 5% — **'탐지' 값만 정보다.** 1000 K 급증이면 Arrhenius 상단 위험"
echo "----------------------------------------------------------------------"

# ── ④ 체인 게이트 ─────────────────────────────────────────────────────
echo "④ 후속 체인 (GPU 해방 대기 → QE 단일점 + Li 슬랩)"
tail -1 "$HOME/logs/chain2.log" 2>/dev/null | sed 's/^/  /' || echo "  (chain2 미가동)"
echo "----------------------------------------------------------------------"
echo "tmux: $(tmux ls 2>/dev/null | cut -d: -f1 | tr '\n' ' ')"
