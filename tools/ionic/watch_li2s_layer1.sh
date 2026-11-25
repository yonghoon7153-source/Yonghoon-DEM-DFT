#!/usr/bin/env bash
# watch_li2s_layer1.sh — melt_quench_uma.py 런 진행 감시. **요약만 찍고 판정하지 않는다** (지표 문턱은 카드 §2).
#   watch -n 60 bash .../watch_li2s_layer1.sh [RUN_ROOT] [--cutoff 6.0] [--compete]
#   watch -n 120 bash .../watch_li2s_layer1.sh ~/work/runs/lpscl_smallcell_2026_09_16 --cutoff 6.0 --compete
#   bash .../watch_li2s_layer1.sh --selftest
#
# 보는 것: GPU · 실행 중 프로세스 · 시드별 phase(melt/quench/hold) · t_ps · T · 밀도 · ps/h · ETA ·
#          완료 시 지표 3개 · 배로스탯 대조 잡
#   --cutoff Å : **자기이미지 하드 기준** L/2 > cutoff 을 살아있는 동안 검사한다
#                (소셀 카드 lpscl_smallcell_uma_qe_force_estimand_2026_09_16 §3 표 4행).
#                ⭐ **마지막 줄만 보지 않는다** — 전 구간 최소 부피로도 검사한다. NPT 는 셀을
#                   줄였다 늘리므로 지나간 위반을 마지막 줄에서 놓칠 수 있다.
#   --compete  : 같은 GPU 에서 도는 **다른** 계산을 같이 찍는다 (동시실행 개정의 근거를 화면에 올린다).
#
# ⛔ 이 도구가 **못 하는 것**
#   · 담금질이 물리적으로 괜찮은지 · 결정화 여부 · 지표 문턱 판정 — 전부 카드·사람 몫이다.
#   · 완료(✅)는 **자격이 아니다.** 게이트(G-B1·B2·B3)는 따로 돈다.
#   · `--cutoff` 의 L 은 **등방(정육면체) 가정**이다 (thermo.csv 에 부피만 있다). 비등방 배로스탯이면 틀린다.
#   · 갱신이 10 분 넘게 멈추면 ⚠ 만 찍고 원인은 말하지 않는다.
#   · `--compete` 는 경합 **여부**만 본다. 그것이 느려짐의 원인인지는 판정하지 않는다.
set -uo pipefail
R=""; CUT=""; COMPETE=0; SELFTEST=0
while [ $# -gt 0 ]; do
  case "$1" in
    --cutoff)   CUT=${2:-}; shift 2 ;;
    --compete)  COMPETE=1; shift ;;
    --selftest) SELFTEST=1; shift ;;
    -*)         echo "모르는 플래그: $1" >&2; exit 2 ;;
    *)          R=$1; shift ;;
  esac
done
R=${R:-/data/work/runs/li2s_layer1}
[ -n "$CUT" ] && { case "$CUT" in ''|*[!0-9.]*) echo "⛔ --cutoff 는 수여야 한다: $CUT" >&2; exit 2 ;; esac; }

# ── 명령줄에서 system·seed 를 뽑는다. ⛔ **인자 순서를 가정하지 않는다** ────────
#    2026-09-16: 옛 판은 `--system X --seed N` 이 **붙어 있다고** 보고 한 패턴으로 잡았는데,
#    (B) 는 `--system A --n_fu 12 --seed 1` 이라 중간에 --n_fu 가 껴서 **빈칸이 찍혔다.**
#    오류도 안 났다 — 조용히 틀린 경로다.
_runlabel() {
  local c="$1" s d
  s=$(printf '%s' "$c" | sed -nE 's/.*--system[= ]+([^ ]+).*/\1/p')
  d=$(printf '%s' "$c" | sed -nE 's/.*--seed[= ]+([^ ]+).*/\1/p')
  if [ -n "$s$d" ]; then echo "system ${s:-?} · seed ${d:-?}"; else echo "⚠ 인자를 못 읽음 (명령줄 형식이 바뀌었나)"; fi
}

# ── nvidia-smi 의 compute-apps 출력을 표로. ⛔ **못 읽음을 '경합 없음' 으로 두지 않는다** ──
#    2026-09-16 실측: 권한이 막힌 호스트는 `Process-level GPU information is restricted.` 를
#    **정상 출력처럼** 돌려준다. 옛 판은 그 문장을 PID 로 먹고 표를 그렸다.
_compete() {
  local apps="$1" any=0
  if [ -n "$apps" ]; then
    while IFS=, read -r pid mem; do
      pid=$(printf '%s' "$pid" | tr -d ' ')
      case "$pid" in ''|*[!0-9]*) continue ;; esac
      any=1
      local cmd tag; cmd=$(ps -p "$pid" -o args= 2>/dev/null | head -c 150); tag="다른 잡"
      case "$cmd" in
        *melt_quench_uma*)             tag="◀ 이 런 (B)" ;;
        *disorder_ensemble_diffusion*) tag="시드 확장 큐" ;;
        *pw.x*)                        tag="⛔ pw.x — MD 와 동시 금지 대상" ;;
      esac
      printf "  PID %-8s %-10s %-28s %s\n" "$pid" "$(printf '%s' "$mem" | tr -d ' ')" "$tag" "${cmd:-(cmdline 못 읽음)}"
    done <<EOF_APPS
$apps
EOF_APPS
  fi
  if [ "$any" = 0 ]; then
    echo "  ⚠ nvidia-smi 가 프로세스별 정보를 **안 준다** — 경합 없음이 아니라 **못 읽음**이다"
    [ -n "$apps" ] && echo "     돌려준 것: $(printf '%s' "$apps" | head -1)"
    echo "     → 대신 프로세스 목록으로 본다 (GPU 점유량은 모른다):"
    pgrep -af "melt_quench_uma|disorder_ensemble_diffusion|pw\.x" 2>/dev/null \
      | grep -v "watch_\|pgrep" | head -6 | sed 's/^/       /' \
      || echo "       (해당 프로세스 없음)"
  fi
}

# selftest 가 두 함수를 **따로** 부를 수 있게 하는 문. 인자는 env 로 받는다
# (명령줄 문자열이 `--system …` 으로 시작해 플래그 파서에 걸리기 때문).
if [ -n "${_WATCH_UNIT:-}" ]; then
  case "$_WATCH_UNIT" in
    runlabel) _runlabel "${_WATCH_UNIT_ARG:-}" ;;
    compete)  _compete  "${_WATCH_UNIT_ARG:-}" ;;
    *) echo "모르는 _WATCH_UNIT: $_WATCH_UNIT" >&2; exit 2 ;;
  esac
  exit 0
fi

if [ "$SELFTEST" = 1 ]; then
  # ── 자기이미지 가드의 양성·음성 경로를 **일부러 깨서** 확인한다 ──────────────
  T=$(mktemp -d); trap 'rm -rf "$T"' EXIT; n=0; bad=0
  mkplan() { mkdir -p "$1"; printf '{"melt_ps":1,"quench_ps":1,"hold_ps":1,"uma_inference_mode":"turbo","quench_rate_K_s":1e12}' > "$1/plan.json"; }
  hdr='t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa'
  chk() { n=$((n+1)); if [ "$2" = "$3" ]; then echo "  ✅ $1"; else echo "  ⛔ $1  (얻음 '$2' ≠ 기대 '$3')"; bad=$((bad+1)); fi; }
  # ① 양성: L/2 = 7.07 > 6.0  (V = 2827 → L 14.14)
  mkplan "$T/A/seed1"; { echo "$hdr"; echo "1.0,300,300,1.5,2827.0,-1,0,0"; } > "$T/A/seed1/thermo.csv"
  o=$(bash "$0" "$T" --cutoff 6.0 2>&1); chk "양성: 여유 있으면 ⛔ 안 뜬다" "$(echo "$o" | grep -c '하드 기준 위반')" "0"
  chk "양성: 자기이미지 줄이 나온다" "$(echo "$o" | grep -c '자기이미지')" "1"
  # ② 음성: L/2 = 5.5 ≤ 6.0  (V = 1331 → L 11.0)
  rm -rf "$T/A"; mkplan "$T/A/seed1"; { echo "$hdr"; echo "1.0,300,300,3.2,1331.0,-1,0,0"; } > "$T/A/seed1/thermo.csv"
  o=$(bash "$0" "$T" --cutoff 6.0 2>&1); chk "⛔음성: 위반을 잡는다" "$(echo "$o" | grep -c '하드 기준 위반')" "1"
  # ③ 음성(핵심): **마지막 줄은 정상, 중간에서 위반** — 마지막 줄만 보면 놓친다
  rm -rf "$T/A"; mkplan "$T/A/seed1"
  { echo "$hdr"; echo "1.0,300,300,1.5,2827.0,-1,0,0"; echo "2.0,300,300,3.2,1331.0,-1,0,0"; echo "3.0,300,300,1.5,2827.0,-1,0,0"; } > "$T/A/seed1/thermo.csv"
  o=$(bash "$0" "$T" --cutoff 6.0 2>&1); chk "⛔음성: 지나간 위반을 전구간 최소로 잡는다" "$(echo "$o" | grep -c '하드 기준 위반')" "1"
  # ④ 음성: --cutoff 없으면 가드가 **아예 안 뜬다** (없는 검사를 통과로 보이게 하지 않는다)
  o=$(bash "$0" "$T" 2>&1); chk "⛔음성: --cutoff 없으면 가드 줄 없음" "$(echo "$o" | grep -c '자기이미지')" "0"
  # ⑤ 음성: 헤더만 있는 thermo.csv 에서 죽지 않는다
  rm -rf "$T/A"; mkplan "$T/A/seed1"; echo "$hdr" > "$T/A/seed1/thermo.csv"
  o=$(bash "$0" "$T" --cutoff 6.0 2>&1); chk "⛔음성: 자료 줄 없어도 죽지 않는다" "$(echo "$o" | grep -c 'Traceback')" "0"
  # ⑥ 음성(fail-closed): 못 읽었을 때 **조용히 넘어가지 않는다**. 줄이 사라지면 사람은 '통과' 로 읽는다.
  #    ⚠ 이 시험이 없던 동안 파괴 시험이 이 경로를 못 잡았다 (2026-09-16 실측).
  chk "⛔음성: 못 읽음을 '검사 못 했다' 로 찍는다 (침묵 금지)" "$(echo "$o" | grep -c '검사 못 했다')" "1"

  # ── _runlabel: 인자 **순서**를 가정하지 않는다 (2026-09-16 실측 버그) ──────────
  rl() { _WATCH_UNIT=runlabel _WATCH_UNIT_ARG="$1" bash "$0"; }
  chk "양성: 붙어 있는 --system/--seed" \
      "$(rl 'python x.py --system A --seed 1 --out o')" "system A · seed 1"
  chk "⛔음성: 사이에 --n_fu 가 껴도 읽는다 (옛 판이 여기서 빈칸을 찍었다)" \
      "$(rl 'python melt_quench_uma.py --system A --n_fu 12 --seed 1 --turbo')" "system A · seed 1"
  chk "⛔음성: 순서가 뒤집혀도 읽는다" \
      "$(rl 'python x.py --seed 7 --system control_li7ps6')" "system control_li7ps6 · seed 7"
  chk "⛔음성: 인자가 없으면 '못 읽음' 이라고 말한다 (빈칸 금지)" \
      "$(rl 'python x.py --dry_run' | grep -c '못 읽음')" "1"

  # ── _compete: 못 읽음을 '경합 없음' 으로 두지 않는다 (2026-09-16 kgy 실측) ─────
  cp2() { _WATCH_UNIT=compete _WATCH_UNIT_ARG="$1" bash "$0" 2>&1; }
  chk "⛔음성: 권한 제한 문장을 PID 로 먹지 않는다" \
      "$(cp2 'Process-level GPU information is restricted.' | grep -c 'PID Process')" "0"
  # ⚠ 문구를 **특정**한다. 예전 판은 '못 읽음' 만 셌는데, 표 안의 `(cmdline 못 읽음)` 에
  #   우연히 걸려서 가드를 뺀 뒤에도 초록이었다 (2026-09-16 파괴 시험에서 드러남).
  chk "⛔음성: 권한 제한이면 '경합 없음이 아니라' 를 말한다" \
      "$(cp2 'Process-level GPU information is restricted.' | grep -c '경합 없음이 아니라')" "1"
  chk "⛔음성: 출력이 비어도 '경합 없음이 아니라' 를 말한다 (침묵 금지)" \
      "$(cp2 '' | grep -c '경합 없음이 아니라')" "1"
  chk "양성: 숫자 PID 행은 표로 그린다" \
      "$(cp2 '1259139, 11544 MiB' | grep -c '^  PID 1259139')" "1"
  # ⑥ 음성: --cutoff 에 수가 아닌 값이면 시작하지 않는다
  bash "$0" "$T" --cutoff abc >/dev/null 2>&1; chk "⛔음성: 비수치 --cutoff 를 거부한다" "$?" "2"
  echo "── selftest $((n-bad))/$n 통과 ──"; [ "$bad" = 0 ] || exit 1; exit 0
fi

echo "════════ $(date '+%m-%d %H:%M:%S')  melt-quench watch — $R ════════"
G=$(nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader 2>/dev/null); echo "■ GPU ${G:-n/a}"
P=$(pgrep -af "melt_quench_uma.py" | grep -v "pgrep\|watch_" | head -1)
if [ -n "$P" ]; then echo "■ 실행: $(_runlabel "$P")"; else echo "■ 실행 중인 melt_quench 없음"; fi
python3 - "$R" "${CUT:-}" <<'PY'
import sys, os, json, time, glob
R = sys.argv[1]
CUT = float(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] else None
now = time.time(); rows = []; modes = set()

def selfimage(th, cut):
    """thermo.csv 전 구간에서 **최소 부피**를 찾아 L/2 > cutoff 하드 기준을 본다.
    ⛔ 마지막 줄만 보면 NPT 가 줄였다 늘린 구간의 위반을 놓친다 (그래서 전 구간이다).
    ⚠ L = V^(1/3) 은 **등방 가정**이다 — thermo.csv 에 부피만 있다."""
    vs = []
    try:
        for ln in open(th).read().strip().splitlines()[1:]:
            f = ln.split(",")
            if len(f) > 4:
                try: vs.append(float(f[4]))
                except ValueError: pass
    except Exception:
        return None
    if not vs:
        return None
    Vnow, Vmin = vs[-1], min(vs)
    Lnow, Lmin = Vnow ** (1 / 3), Vmin ** (1 / 3)
    ok = (Lmin / 2) > cut
    s = (f"      자기이미지  L {Lnow:.2f} Å (등방 가정, V {Vnow:.0f} Å³) · L/2 {Lnow/2:.2f} · "
         f"감김홉 L/c {Lnow/cut:.2f}")
    if ok:
        s += f"  ✅ 전구간 최소 L/2 {Lmin/2:.2f} > cutoff {cut:.2f} (여유 {Lmin/2-cut:+.2f} Å)"
    else:
        s += (f"\n      ⛔ **하드 기준 위반** — 전구간 최소 L/2 {Lmin/2:.2f} ≤ cutoff {cut:.2f} "
              f"(V_min {Vmin:.0f} Å³): 원자가 자기 이미지와 **직접 엣지**를 맺는다. 이 런은 못 쓴다")
    return s

def g(I, k):
    v = I.get(k); return "  —  " if v is None else f"{v:5.2f}"

def guard(th):
    """--cutoff 가 주어졌을 때만 한 줄. ⛔ 못 읽으면 **'검사 못 했다'** 로 적는다 — 통과로 두지 않는다."""
    if CUT is None:
        return None
    return selfimage(th, CUT) or \
        "      자기이미지  ⚠ thermo.csv 자료가 없어 **검사 못 했다** (못 읽음 ≠ 통과)"

for plan in sorted(glob.glob(os.path.join(R, "*", "seed*", "plan.json"))):
    d = os.path.dirname(plan); sysn = os.path.basename(os.path.dirname(d)); seed = os.path.basename(d)
    try:
        Pj = json.load(open(plan))
    except Exception as e:
        rows.append(f"  {sysn:16s} {seed:6s} ⚠ plan.json 못 읽음 ({e})"); continue
    total = Pj["melt_ps"] + Pj["quench_ps"] + Pj["hold_ps"]
    mode = Pj.get("uma_inference_mode") or "?"          # turbo / default — 시드마다 같아야 한다
    modes.add(mode)
    res, th = os.path.join(d, "result.json"), os.path.join(d, "thermo.csv")
    if os.path.isfile(res):
        try:
            I = json.load(open(res))["indicators"]
            rows.append(f"  {sysn:16s} {seed:6s} ✅ 완료   ρ {I['density_g_cm3']:.3f}  PS4 {g(I,'PS4_fraction')}  Cl6 {g(I,'Cl_6coord_fraction')}  S-Li8 {g(I,'S_Li8_fraction_Li2S_like')}")
        except Exception as e:
            rows.append(f"  {sysn:16s} {seed:6s} ⚠ result.json 못 읽음 ({e})")
        if (s := guard(th)): rows.append(s)
        continue
    el = (now - os.path.getmtime(plan)) / 60
    if not os.path.isfile(th) or os.path.getsize(th) < 60:
        rows.append(f"  {sysn:16s} {seed:6s} … 준비(prerelax/초기)  {el:.0f} 분 경과")
        if (s := guard(th)): rows.append(s)
        continue
    last = open(th).read().strip().splitlines()[-1].split(",")
    try:
        t, T, Tset, rho = float(last[0]), float(last[1]), float(last[2]), float(last[3])
        P = float(last[6]) if len(last) > 6 else float("nan")     # P_GPa (옛 런은 열이 없다)
    except ValueError:
        rows.append(f"  {sysn:16s} {seed:6s} … thermo.csv 헤더만")
        if (s := guard(th)): rows.append(s)
        continue
    if t >= total - 1e-9:
        phase = "relax"
    else:
        phase = "melt" if t < Pj["melt_ps"] else ("quench" if t < Pj["melt_ps"] + Pj["quench_ps"] else "hold")
    rate = t / el if el > 0 else 0.0                       # ps/min
    eta = (total - t) / rate / 60 if rate > 0 else float("nan")
    stale = (now - os.path.getmtime(th)) / 60
    flag = f"  ⚠ 갱신 {stale:.0f}분 전" if stale > 10 else ""
    pstr = f"P {P:+6.3f}" if P == P else "P   —  "            # ⛔ 옛 런은 배로스탯 제어변수를 기록 안 했다
    rows.append(f"  {sysn:16s} {seed:6s} {phase:6s} t {t:7.1f}/{total:.0f} ps  T {T:6.0f}(set {Tset:5.0f}) K  ρ {rho:.3f}  {pstr}  {rate*60:5.1f} ps/h  ETA {eta:4.1f} h{flag}")
    if (s := guard(th)): rows.append(s)
print("\n".join(rows) if rows else "  (plan.json 없음 — 아직 시작 안 함)")
if len(modes) > 1:
    print(f"  ⛔ UMA 실행모드가 시드마다 다르다 {sorted(modes)} — 한 묶음으로 못 쓴다")
elif modes:
    print(f"  UMA 실행모드 {modes.pop()} (전 시드 동일) · 담금질 {Pj['quench_rate_K_s']:.0e} K/s")
PY
echo "  ⛔ 지표(PS4·Cl6·S-Li8)는 카드 §2 문턱과 사람이 대조한다 — 이 표는 판정하지 않는다"

# ── 배로스탯 대조 잡 (같은 루트 밑 npt_control*) ──────────────────────────────
echo "── 대조 잡 (배로스탯) ──"
python3 - "$R" <<'PY'
import sys, os, json, glob
R = sys.argv[1]; found = False
for d in sorted(glob.glob(os.path.join(R, "npt_control*"))):
    if not os.path.isdir(d):
        continue
    found = True; name = os.path.basename(d); cj = os.path.join(d, "control.json")
    if os.path.isfile(cj):
        try:
            c = json.load(open(cj))
        except Exception as e:
            print(f"  {name:22s} ⚠ control.json 못 읽음 ({e})"); continue
        # ⛔ 옛 판 control.json 은 키가 아예 없다 — None 을 포맷하면 watch 가 죽는다 (2026-09-12)
        def f(k, fmt="%.3f", dash="—"):
            v = c.get(k)
            return dash if v is None else (fmt % v)
        ref = c.get("reference_for_drift", "?"); dr = c.get("drift_vs_UMA_0K")
        ok = c.get("plumbing_ok")
        print(f"  {name:22s} ✅ 완료  {c.get('n_atoms','?')}원자 폭 {f('min_cell_width_A','%.2f')} Å  "
              f"ρ파일 {f('rho_file_g_cm3')} → 0K {f('rho_UMA_0K_g_cm3')} → "
              f"NPT {f('rho_NPT_mean_last_half_g_cm3')}  P {f('P_NPT_mean_last_half_GPa','%+.3f')} GPa")
        # ⭐ 판정은 **압력**이다. 밀도 drift 는 0 K↔T 열팽창이라 판정이 아니다 (2026-09-12 오판)
        verdict = ("⭕ 배선 정상" if ok else ("⛔ 배선 이상" if ok is not None else "— 판정 없음"))
        pt = c.get("P_tol_GPa")
        basis = (f"⟨P⟩ {f('P_NPT_mean_last_half_GPa','%+.3f')} GPa vs ±{pt}" if pt is not None
                 else "⚠ 옛 판정(밀도 drift 기준) — 압력으로 다시 보라")
        print(f"  {'':22s}    {basis} → {verdict}"
              f"{'' if c.get('cell_wide_enough', True) else '  ⚠ 셀이 얇다 — 조건부'}")
        print(f"  {'':22s}    0K→T 밀도 {('%+.2f %%' % (100*dr)) if dr is not None else '—'} "
              f"(기준 {ref}) = **열팽창, 판정 아님**")
        if c.get("cell_relax_note"): print(f"  {'':22s}    0K 완화: {c['cell_relax_note']}")
    else:
        th = os.path.join(d, "thermo.csv"); cl = os.path.join(d, "cellrelax.log")
        if os.path.isfile(th) and os.path.getsize(th) > 60:
            last = open(th).read().strip().splitlines()[-1].split(",")
            try:
                t, T, rho = float(last[0]), float(last[1]), float(last[3])
                P = float(last[6]) if len(last) > 6 else float("nan")
                print(f"  {name:22s} … NPT  t {t:5.2f} ps  T {T:5.0f} K  ρ {rho:.4f}  P {P:+.3f} GPa")
            except ValueError:
                print(f"  {name:22s} … thermo.csv 헤더만")
        elif os.path.isfile(cl):
            ln = [x for x in open(cl).read().strip().splitlines() if x.strip()]
            print(f"  {name:22s} … 0 K 셀 완화  {ln[-1].strip() if ln else '(빈 로그)'}")
        else:
            print(f"  {name:22s} … 준비(UMA 로드)")
if not found:
    print("  (대조 잡 없음)")
print("  ⛔ drift 판정은 **배선(배로스탯·단위)** 에 한정된다. UMA 자신의 밀도 오차는 그 판정 밖이다.")
PY

# ── --compete: 같은 GPU 를 나눠 쓰는 다른 계산 ──────────────────────────────
if [ "$COMPETE" = 1 ]; then
  echo "── 같은 GPU 경합 (동시실행 개정의 근거를 화면에 올린다) ──"
  _compete "$(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader 2>/dev/null)"
  echo "  ⛔ 경합 **여부**만 본다 — 느려짐의 원인인지는 판정하지 않는다."
  echo "     근거 조항: G1 §6b *\"힘·에너지 값 자체는 GPU 경합과 무관하다\"* ·"
  echo "     소셀 카드 §3-b ⚠_동시실행_개정 (MD 만 동시 · **QE 단일점은 제외**)"
fi
echo "  ⛔ ✅완료는 **자격이 아니다** — 게이트 G-B1(수렴)·G-B2(겹침)·G-B3(힘·에너지)는 따로 돈다."
