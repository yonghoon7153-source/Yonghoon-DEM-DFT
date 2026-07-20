#!/usr/bin/env bash
# watch_vgcf_hbn.sh — status snapshot for the h-BN@VGCF Li-adsorption QE run (kgy).
# One-shot (run directly) or under watch:
#   watch -n 30 'bash ~/Yonghoon-DEM-DFT/tools/vgcf_hbn/watch_vgcf_hbn.sh'
set +H
W=${WORK:-$HOME/work/vgcf_hbn}
F2eVA=25.71104   # Ry/Bohr -> eV/A

echo "══ h-BN@VGCF · Li adsorption (QE PBE-D3BJ, 4x4)  $(date '+%m-%d %H:%M:%S') ══"

# --- current pw.x + GPU + stall detection ---
cur=$(pgrep -af 'pw\.x .*-in' 2>/dev/null | grep -aoE '[A-Za-z_]+\.in' | head -1)
gpu=$(nvidia-smi --query-gpu=memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
if [ -n "$cur" ]; then
  lg="$W/${cur%.in}.out"
  age=$(( $(date +%s) - $(stat -c %Y "$lg" 2>/dev/null || date +%s) ))
  echo "  실행중: ${cur%.in}  | 로그 ${age}s 전 갱신  | GPU ${gpu} (used,free,util%)"
else
  echo "  실행중: (없음 — 완료/대기/중단)  | GPU ${gpu}"
fi

# --- per-calc table ---
ORDER="Li_atom graphene hbn Li_on_graphene Li_on_hbn bilayer Li_in_gallery"
echo "── 계산별 상태 (relax) ──"
for n in $ORDER; do
  o="$W/$n.out"
  if [ ! -f "$o" ]; then printf "  %-16s · 대기\n" "$n"; continue; fi
  if grep -aq "JOB DONE" "$o"; then
    e=$(grep -a '^!' "$o" | tail -1 | awk '{print $(NF-1)}')
    printf "  %-16s ✅ done    E=%s Ry\n" "$n" "$e"
  else
    steps=$(grep -ac "Total force" "$o")
    fmax=$(grep -a "Total force" "$o" | tail -1 | awk '{print $4}')
    acc=$(grep -a "estimated scf accuracy" "$o" | tail -1 | awk '{print $(NF-1)}')
    eva=$(awk -v f="${fmax:-0}" -v k=$F2eVA 'BEGIN{printf "%.3f", f*k}')
    printf "  %-16s ↻ ion%-3s |F|=%s Ry/au (%s eV/Å →0.026) acc=%s\n" \
           "$n" "${steps:-0}" "${fmax:-?}" "$eva" "${acc:-?}"
  fi
done

# --- E_ads + Shi eq5 sandwich verdict (completed only) ---
echo "── E_ads = E(Li+X) − E(X) − E(Li_atom) ──"
python3 - "$W" <<'PY'
import re, sys, os
W = sys.argv[1]; Ry = 13.605693
def E(n):
    p = f"{W}/{n}.out"
    if not os.path.exists(p): return None
    t = open(p).read()
    if "JOB DONE" not in t: return None
    m = re.findall(r"^!\s+total energy\s+=\s+(-\d+\.\d+)", t, re.M)
    return float(m[-1]) if m else None
li = E("Li_atom"); v = {}
for lab, cx, sub in [("VGCF(graphene)", "Li_on_graphene", "graphene"),
                     ("h-BN",           "Li_on_hbn",      "hbn"),
                     ("gallery(sandwich)", "Li_in_gallery", "bilayer")]:
    ec, es = E(cx), E(sub)
    if ec and es and li:
        v[lab] = (ec - es - li) * Ry
        print(f"    Li/{lab:18s} {v[lab]:+.3f} eV")
    else:
        print(f"    Li/{lab:18s} (대기)")
if len(v) == 3:
    g, h, s = v["VGCF(graphene)"], v["h-BN"], v["gallery(sandwich)"]
    print(f"  ── Shi eq5: gallery {s:+.3f}  vs  VGCF({g:+.3f})+hBN({h:+.3f})={g + h:+.3f} ──")
    if s < min(g, h):
        print("  ✅ 샌드위치가 두 단일표면보다 강함 → VGCF가 Cu 역할 (샌드위치 성립)")
    else:
        print("  ⚠ 샌드위치가 단일표면보다 약함 → VGCF ≠ Cu (그 자체가 발견)")
    print("    lithiophobicity 판정: 위 값 + 1.63 eV(bulk-Li 보정); +면 lithiophobic")
PY
