#!/bin/bash
# kgy_li3n_round4_min.sh — Li3N p0 round-4: min 마무리 단독런 (kgy RTX 3090).
#
# 상황 (2026-07-14 16:48): p0_saddle3 bfgs 수렴 E=-2176.43605123 Ry (확정 앵커).
# p0_min3는 ion 20에서 중단(러너 사망) — 중간E -2176.43174 Ry, 등속 -0.08 mRy/step
# 하강 중이었음. 현재 스냅샷은 saddle3가 min3보다 4.4 mRy 아래(=위상 역전 상태)지만
# min이 미수렴이라 최종 순서는 min4가 수렴해야 확정:
#   - min4가 saddle3 위에서 수렴  → UMA 위상 역전 DFT 확정 (진단 그림)
#   - min4가 아래로 뚫고 수렴     → 정상 순서, 그러나 격차는 수십 meV 수준
# 어느 쪽이든 UMA-PES 171 meV와는 불일치 → drag 프로파일이 본편이라는 방침 유지.
#
# 실행법 (kgy):
#   cd ~/work/li3n_dft
#   conda deactivate 2>/dev/null; qegpu
#   bash ~/kgy_li3n_round4_min.sh        # 또는 본문 그대로 붙여넣기
set -e
cd "$HOME/work/li3n_dft"

echo "== [0] min3 마지막 6스텝 dE(mRy) — 기록용 =="
grep '^!' p0_min3.out | tail -6 | awk '{e[NR]=$5} END{for(i=2;i<=NR;i++) printf " %+.2f",(e[i]-e[i-1])*1000; print ""}'

echo "== [1] p0_min4.in 생성 (min3 ion-20 기하 승계 + adatom행 검증) =="
python3 - <<'PYEOF'
import re
out = open("p0_min3.out", errors="ignore").read().splitlines()
nat = None
for l in out:
    m = re.search(r"number of atoms/cell\s*=\s*(\d+)", l)
    if m:
        nat = int(m.group(1)); break
assert nat, "nat not found"
idx = max(i for i, l in enumerate(out) if l.strip().startswith("ATOMIC_POSITIONS"))
block = out[idx:idx + nat + 1]
atoms = block[1:]
assert len(atoms) == nat and all(len(x.split()) >= 4 for x in atoms), "bad/truncated block"
inp = open("p0_min3.in").read().splitlines()
j = next(i for i, l in enumerate(inp) if l.strip().upper().startswith("ATOMIC_POSITIONS"))
old_ad = " ".join(inp[j + nat].split()[1:4])
open("p0_min4.in", "w").write("\n".join(inp[:j] + block + inp[j + nat + 1:]) + "\n")
chk = open("p0_min4.in").read().splitlines()
new_ad = " ".join(chk[j + nat].split()[1:4])
want = " ".join(block[nat].split()[1:4])
nfix = sum(1 for x in atoms if len(x.split()) == 7)
ok = "OK" if new_ad == want else "FAIL"
print(f"  nat={nat}, if_pos행={nfix}, 단위='{block[0].strip()}'")
print(f"  adatom {old_ad} -> {new_ad} | verify={ok}")
assert ok == "OK"
PYEOF

echo "== [2] 발사 (min4 단독; nohup) =="
: "${MPIRUN:?qegpu를 먼저 실행하세요 (MPIRUN 비어있음)}"
: "${QEGPU:?qegpu를 먼저 실행하세요 (QEGPU 비어있음)}"
cat > run_round4.sh <<'EOF'
#!/bin/bash
# usage: run_round4.sh <MPIRUN> <QEGPU_BIN>
M=$1; Q=$2
cd "$HOME/work/li3n_dft"
j=p0_min4
if grep -q "JOB DONE" "$j.out" 2>/dev/null; then
    echo "[$j] already done — skip"
else
    echo "[$j] START $(date)"
    $M -np 1 "$Q/pw.x" -npool 1 -in "$j.in" > "$j.out" 2>&1
    if grep -q "JOB DONE" "$j.out"; then
        conv="MAXSTEP"; grep -q "bfgs converged" "$j.out" && conv="수렴"
        echo "[$j] DONE ($conv)  E=$(grep '^!' "$j.out" | tail -1 | awk '{print $5}') Ry  $(date)"
    else
        echo "[$j] FAILED/interrupted  $(date)"
    fi
fi
S=$(grep '^!' p0_saddle3.out | tail -1 | awk '{print $5}')
M4=$(grep '^!' p0_min4.out 2>/dev/null | tail -1 | awk '{print $5}')
[ -n "$S" ] && [ -n "$M4" ] && awk -v s="$S" -v m="$M4" \
    'BEGIN{d=(s-m)*13605.7; printf "[round4] barrier(saddle3-min4) = %+.1f meV %s\n", d, (d<0?"<- UMA 위상 역전 확정":"")}'
echo "[round4] chain end $(date)"
EOF
chmod +x run_round4.sh
nohup ./run_round4.sh "$MPIRUN" "$QEGPU" >> chain.log 2>&1 &
echo "  launched (pid $!) — tail -f chain.log"
