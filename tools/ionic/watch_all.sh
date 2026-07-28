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
            # ⚠ 키 이름을 **가정하지 않는다** — 실제 파일이 msd.json 이었고 키도 달랐다.
            #   json 안을 재귀로 훑어 'sigma' 를 포함한 스칼라 키를 찾는다.
            #   sigma 가 없으면 D(확산계수)라도 잡아 진행 여부만 표시한다.
            def find(o, want):
                if isinstance(o, dict):
                    for k, v in o.items():
                        if want in k.lower() and isinstance(v, (int, float)):
                            return v
                    for v in o.values():
                        r = find(v, want)
                        if r is not None:
                            return r
                elif isinstance(o, list):
                    for v in o[:20]:
                        r = find(v, want)
                        if r is not None:
                            return r
                return None
            hit, kind = None, ""
            for f in sorted(glob.glob(os.path.join(c, f"T{T}", "*.json"))):
                try:
                    d = json.load(open(f))
                except Exception:
                    continue
                hit = find(d, "sigma")
                if hit is not None:
                    kind = "σ"; break
                hit = find(d, "d_cm2")
                if hit is None:
                    hit = find(d, "diffus")
                if hit is not None:
                    kind = "D"; break
            if hit is not None:
                line += f" {T}K✓({kind}{hit:.2e})"; n += 1
            else:
                # json 은 없어도 궤적이 있으면 진행 중
                run = glob.glob(os.path.join(c, f"T{T}", "traj*"))
                line += f" {T}K{'~' if run else '·'}"
        print(f"{line}  [{n}/3]")
PYC
echo "  ordered baseline: comp2 Ea 0.276±0.033 / comp1 0.253  (disorder가 낮추면 가설 확증)"
echo "----------------------------------------------------------------------"

# ── ② SDCP relax ──────────────────────────────────────────────────────
echo "② SDCP complex_doped_v2 relax (k 2×2×1)"
# ⚠ pw.x 의 stdout 이 **파일이 아니라 tmux 페인(/dev/pts/N)** 인 경우가 있다 — 실제로 그랬다.
#   그러면 .out 파일이 아예 없고 출력은 페인 스크롤백에만 산다. 세 경로로 찾는다:
#     ① SDCP_OUT 환경변수(수동)  ② tmux 페인 캡처  ③ .out 파일 검색
SRC=""; VIA=""
if [ -n "$SDCP_OUT" ] && [ -f "$SDCP_OUT" ]; then
  SRC=$(cat "$SDCP_OUT"); VIA="파일 $SDCP_OUT"
else
  for S in ${SDCP_TMUX:-sdcp_cd sdcp p0}; do
    if tmux has-session -t "$S" 2>/dev/null; then
      CAP=$(tmux capture-pane -p -t "$S" -S -4000 2>/dev/null)
      if echo "$CAP" | grep -qa "iteration #\|convergence has been achieved"; then
        SRC="$CAP"; VIA="tmux:$S"; break
      fi
    fi
  done
  if [ -z "$SRC" ]; then
    F=$(ls -t $(find "$HOME" /data -maxdepth 5 -name "*.out" -newermt '-2 days' \
        -path '*sdcp*' 2>/dev/null) 2>/dev/null | head -1)
    [ -n "$F" ] && { SRC=$(cat "$F"); VIA="파일 $F"; }
  fi
fi

if [ -n "$SRC" ]; then
  echo "  source: $VIA"
  echo "$SRC" | grep -a "number of k points" | tail -1 | sed 's/^/  /'
  # ⚠ scf_must_converge=.false. + maxstep 도달 = **가짜 수렴**. 반복수가 maxstep 과 같은지 본다.
  echo "  완료 step별 반복수 (maxstep과 같으면 **가짜 수렴**):"
  echo "$SRC" | grep -a "convergence has been achieved in" | tail -3 | sed 's/^/    /'
  echo "  현재:"
  echo "$SRC" | grep -a "iteration #\|estimated scf accuracy" | tail -2 | sed 's/^/    /'
else
  echo "  (못 찾음. export SDCP_OUT=/경로/파일.out  또는  export SDCP_TMUX=세션명)"
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
