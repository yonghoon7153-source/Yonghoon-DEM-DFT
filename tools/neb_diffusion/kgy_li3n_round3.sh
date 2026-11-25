#!/bin/bash
# kgy_li3n_round3.sh — Li3N p0 round-3 continuation on kgy(RTX 3090).
# round1(p0_min MAXSTEP, gabia) → round2(kgy: p0_saddle, p0_min2 — 둘 다 MAXSTEP)
# → round3: 마지막 기하를 이어받아 p0_saddle2 → p0_min3, nstep=300 (kgy는 벽시간이
# 없으므로 이번엔 수렴까지 완주시키는 것이 목적; MAXSTEP 왕복 종료).
#
# 실행법 (kgy 인터랙티브 셸에서 — qegpu 함수가 $MPIRUN/$QEGPU를 채워야 함):
#   cd ~/work/li3n_dft
#   conda deactivate 2>/dev/null; qegpu
#   bash ~/kgy_li3n_round3.sh        # 또는 본문을 그대로 붙여넣기
set -e
cd "$HOME/work/li3n_dft"

echo "== [0] round2 마지막 6스텝 dE(mRy) — 기록용 (아직 가파르면 round3가 정답) =="
for f in p0_min2.out p0_saddle.out; do
    printf "  %-14s" "$f:"
    grep '^!' "$f" | tail -6 | awk '{e[NR]=$5} END{for(i=2;i<=NR;i++) printf " %+.2f",(e[i]-e[i-1])*1000; print ""}'
done

echo "== [1] 이어달리기 입력 생성 (마지막 ATOMIC_POSITIONS + if_pos 보존 + nstep 300) =="
python3 - <<'PYEOF'
import re

def carry(out_f, in_f, new_f, nstep=300):
    out = open(out_f, errors="ignore").read().splitlines()
    nat = None
    for l in out:
        m = re.search(r"number of atoms/cell\s*=\s*(\d+)", l)
        if m:
            nat = int(m.group(1)); break
    assert nat, f"{out_f}: nat not found"
    idx = max(i for i, l in enumerate(out) if l.strip().startswith("ATOMIC_POSITIONS"))
    block = out[idx:idx + nat + 1]          # 헤더(단위 포함) + nat 원자행
    atoms = block[1:]
    assert len(atoms) == nat and all(len(x.split()) >= 4 for x in atoms), f"{new_f}: bad block"
    inp = open(in_f).read().splitlines()
    j = next(i for i, l in enumerate(inp) if l.strip().upper().startswith("ATOMIC_POSITIONS"))
    txt = "\n".join(inp[:j] + block + inp[j + nat + 1:])
    if re.search(r"(?mi)^\s*nstep\s*=", txt):
        txt = re.sub(r"(?mi)^\s*nstep\s*=.*$", "  nstep = %d" % nstep, txt, count=1)
    else:
        txt = re.sub(r"(?mi)^(\s*&control\s*)$", r"\1\n  nstep = %d" % nstep, txt, count=1)
    open(new_f, "w").write(txt + "\n")
    nfix = sum(1 for x in atoms if len(x.split()) == 7)   # if_pos 3열이 붙은 행 수
    print(f"  {new_f}: nat={nat}, if_pos행={nfix}, 단위='{block[0].strip()}', nstep={nstep}")

carry("p0_saddle.out", "p0_saddle.in", "p0_saddle2.in")
carry("p0_min2.out",   "p0_min2.in",   "p0_min3.in")
PYEOF

echo "== [2] 발사 (saddle2 → min3 순차; nohup) =="
: "${MPIRUN:?qegpu를 먼저 실행하세요 (MPIRUN 비어있음)}"
: "${QEGPU:?qegpu를 먼저 실행하세요 (QEGPU 비어있음)}"
cat > run_round3.sh <<'EOF'
#!/bin/bash
# usage: run_round3.sh <MPIRUN> <QEGPU_BIN>   (qegpu 셸에서 값이 인자로 박제됨)
M=$1; Q=$2
cd "$HOME/work/li3n_dft"
for j in p0_saddle2 p0_min3; do
    if grep -q "JOB DONE" "$j.out" 2>/dev/null; then echo "[$j] already done — skip"; continue; fi
    echo "[$j] START $(date)"
    $M -np 1 "$Q/pw.x" -npool 1 -in "$j.in" > "$j.out" 2>&1
    if grep -q "JOB DONE" "$j.out"; then
        conv="MAXSTEP"; grep -q "bfgs converged" "$j.out" && conv="수렴"
        echo "[$j] DONE ($conv)  E=$(grep '^!' "$j.out" | tail -1 | awk '{print $5}') Ry  $(date)"
    else
        echo "[$j] FAILED/interrupted  $(date)"
    fi
done
echo "[round3] chain end $(date)"
EOF
chmod +x run_round3.sh
nohup ./run_round3.sh "$MPIRUN" "$QEGPU" >> chain.log 2>&1 &
echo "  launched (pid $!) — tail -f chain.log"
