#!/usr/bin/env bash
# =============================================================================
# run_gap_nscf_gabia.sh — comp1 / modelc **fixed-occupations nscf gap** 재계산.
#   gabia CPU 빌드 전용 (GPU 는 UMA NEB 가 쓰고 있다 — VRAM 42.7/49 GB).
#
# 왜 도는가 (2026-08-20)
#   정본 gap 4종 중 comp1 2.066 / modelc 2.099 의 **실행본이 어디에도 없다**
#   (백업 2벌 + kgy + gabia 전수 실패). 게다가 정본 레코드가 EF 를 함께 적고 있어서
#   그 값은 `extract_gap.py`(fixed-occ 전용, EF 를 안 찍는다)가 아니라
#   `parse_eig_gap.py`(EF 기준 VBM/CBM, smearing/tetrahedra .out 재파싱)에서 나왔다.
#   → 값 자체는 고유값 gap 이 맞지만 **b2o3·lpsocl 과 방법이 다르다.**
#   이 스크립트는 네 계통을 같은 방법(fixed-occ)으로 맞추고, 동시에
#   2.066 / 2.099 가 재현되는지 시험한다.
#
# 계보 확인 훅 ★
#   정본 레코드의 k-point 수를 그대로 겨냥한다:
#     comp1  k 8 8 8 → QE 가 "170" irreducible 을 찍어야 계보 일치
#     modelc k 8 8 2 → "68" irreducible.  (8×8×2=128, 시간반전만 있으면
#         자기역원 8점 제외 (128−8)/2+8 = 68 — 정본의 '68 irr' 과 정확히 맞는다.
#         템플릿 주석의 '6 6 2' 는 근거 없는 추정이라 쓰지 않는다.)
#   QE 가 다른 수를 찍으면 **셋업이 정본과 다르다**는 뜻이다 — 로그에 경고로 찍는다.
#
# 재현 목표 (db/properties/electronic.json eigenvalue_gaps_v100_2026_06_16)
#   comp1  VBM 2.128  CBM 4.194  gap 2.066   (EF 3.724, N_EF 0)
#   modelc VBM 2.445  CBM 4.544  gap 2.099   (EF 3.487, N_EF 0)
#
# 이 스크립트가 **못 하는 것**
#   · 정본을 자동으로 고치지 않는다. 값만 찍는다. 판정·기록은 사람이 한다.
#   · 구조를 이완하지 않는다. repo 의 scf.in 좌표(= 그때의 V0)를 그대로 쓴다.
#     그 좌표가 정본 gap 을 만든 그 좌표인지는 이 스크립트가 보증하지 못한다.
#   · pseudo 를 내려받지 않는다. gabia 에 USPP 4종이 없으면 즉사한다(파일명은
#     KISTI 판/gabia 판 두 표기를 모두 뒤진다).
#   · CPU 라 느리다. 계당 scf 1–3 h + nscf 6–15 h 예상. 밤새 도는 작업이다.
#
# 사용
#   cd /data/work/repo && git pull
#   tmux new -s gapnscf -d 'bash tools/electronic/run_gap_nscf_gabia.sh > /data/work/runs/gap_nscf/run.log 2>&1'
#   tail -f /data/work/runs/gap_nscf/run.log
#   SYSTEMS=comp1 bash ...        # 하나만
#   bash tools/electronic/run_gap_nscf_gabia.sh --selftest
# =============================================================================
set -u; set +H

# ── 셀프테스트 (음성 경로 포함) ─────────────────────────────────────────────
if [ "${1:-}" = "--selftest" ]; then
    T=$(mktemp -d); ok=1
    say() { echo "  $1 $2"; if [ "$1" = "✗" ]; then ok=0; fi; return 0; }

    cat > "$T/scf.in" <<'EOF'
&CONTROL
    calculation = 'scf'
    prefix      = 'comp1'
    outdir      = './tmp'
    pseudo_dir  = '/scratch/x3430a02/kgy/manuscript_support/pseudo'
/
&SYSTEM
    ibrav = 0
    nat   = 52
    ntyp  = 4
    ecutwfc = 60.0
    occupations='smearing'
    smearing='mv'
    degauss=0.01
/
ATOMIC_SPECIES
  Li     6.941  li_pbe_v1_4_uspp_F.UPF
K_POINTS automatic
4 4 4 0 0 0
EOF

    # 양성 ①: scf → nscf 변환이 occupations 3줄을 fixed 한 줄로 바꾼다
    sed -e "s|calculation *=.*|calculation = 'nscf'|" \
        -e "s|occupations *=.*|occupations = 'fixed'|" \
        -e "/smearing *=/d" -e "/degauss *=/d" "$T/scf.in" > "$T/nscf.in"
    grep -q "occupations = 'fixed'" "$T/nscf.in" && say "✓" "occupations → fixed" || say "✗" "fixed 치환 실패"
    grep -q "smearing" "$T/nscf.in" && say "✗" "smearing 잔존 (fixed 와 충돌해 QE 가 거부한다)" || say "✓" "smearing/degauss 제거"
    grep -q "calculation = 'nscf'" "$T/nscf.in" && say "✓" "calculation → nscf" || say "✗" "nscf 치환 실패"

    # 양성 ②: K_POINTS 메시 줄만 갈아끼운다 (헤더는 유지)
    awk '/K_POINTS/{print; getline; print "8 8 8 0 0 0"; next} {print}' "$T/nscf.in" > "$T/n2.in"
    grep -A1 K_POINTS "$T/n2.in" | tail -1 | grep -q "^8 8 8" && say "✓" "k-mesh 교체" || say "✗" "k-mesh 교체 실패"
    [ "$(grep -c K_POINTS "$T/n2.in")" = 1 ] && say "✓" "K_POINTS 헤더 중복 없음" || say "✗" "K_POINTS 중복"

    # 음성 ①: nbnd 를 안 넣으면 빈 밴드가 없어 CBM 이 안 나온다 — 넣었는지 확인
    grep -q "nbnd" "$T/n2.in" && say "✗" "테스트 전제 오류" || say "✓" "nbnd 미삽입 상태를 정확히 인지"
    sed -i "s|    ntyp  = 4|    ntyp  = 4\n    nbnd  = 160|" "$T/n2.in"
    grep -q "nbnd  = 160" "$T/n2.in" && say "✓" "nbnd 삽입" || say "✗" "nbnd 삽입 실패"

    # 음성 ②: extract_gap 는 smearing .out 을 gap 으로 읽으면 안 된다
    printf '     the Fermi energy is     3.7240 ev\n' > "$T/smear.out"
    R=$(python3 "$(dirname "$0")/standard_dos/extract_gap.py" "$T/smear.out" 2>/dev/null)
    echo "$R" | grep -q "rerun with occupations='fixed'" \
        && say "✓" "smearing .out 을 gap 으로 오독하지 않음" || say "✗" "smearing 오독: $R"

    # 음성 ③: HOMO 만 있고 LUMO 가 없으면 nbnd 부족이라고 말해야 한다
    printf '     highest occupied level (ev):     2.1280\n' > "$T/homo.out"
    R=$(python3 "$(dirname "$0")/standard_dos/extract_gap.py" "$T/homo.out" 2>/dev/null)
    echo "$R" | grep -q "Raise nbnd" && say "✓" "LUMO 없음 → nbnd 부족 지적" || say "✗" "nbnd 부족 미검출: $R"

    # 양성 ③: 정상 fixed-occ .out 은 gap 을 찍는다
    printf '     highest occupied, lowest unoccupied level (ev):     2.1280    4.1940\n' > "$T/ok.out"
    R=$(python3 "$(dirname "$0")/standard_dos/extract_gap.py" "$T/ok.out" 2>/dev/null)
    echo "$R" | grep -q "GAP = 2.0660" && say "✓" "fixed-occ .out → GAP 2.0660 (정본 재현 경로)" || say "✗" "gap 파싱 실패: $R"

    # 음성 ④: irr k-point 수 대조 — 다른 수가 나오면 경고해야 한다
    printf '     number of k points=   170\n' > "$T/k.out"
    n=$(grep -a 'number of k points' "$T/k.out" | head -1 | sed 's/.*number of k points=\s*//' | awk '{print $1}')
    [ "$n" = "170" ] && say "✓" "irr k-point 수 파싱 170" || say "✗" "k 수 파싱 실패: $n"
    printf '     number of k points=   260\n' > "$T/k2.out"
    n2=$(grep -a 'number of k points' "$T/k2.out" | head -1 | sed 's/.*number of k points=\s*//' | awk '{print $1}')
    [ "$n2" != "170" ] && say "✓" "다른 k 수(260)를 계보 일치로 오판하지 않음" || say "✗" "계보 오판"

    rm -rf "$T"
    [ "$ok" = 1 ] && { echo "selftest PASS"; exit 0; } || { echo "selftest FAIL"; exit 1; }
fi

# ── 환경 ────────────────────────────────────────────────────────────────────
REPO=${REPO:-/data/work/repo}
[ -d "$REPO/tools/electronic" ] || REPO=$HOME/Yonghoon-DEM-DFT
[ -d "$REPO/tools/electronic" ] || { echo "ERROR: repo 못 찾음 (REPO=... 로 지정)"; exit 1; }
OUT=${OUT:-/data/work/runs/gap_nscf}; mkdir -p "$OUT"
SRC=$REPO/tools/electronic/standard_dos
CPU=${CPU:-/data/apps/qe-7.4.1-cpu/bin}
[ -x "$CPU/pw.x" ] || { echo "ERROR: CPU 빌드 pw.x 없음 ($CPU) — ls /data/apps 붙여줘"; exit 1; }

# 중복 실행 가드: pgrep 은 tmux 래퍼까지 물어서 못 쓴다 (chain_gpu_release.sh:34, 2026-08-03).
exec 9>"$OUT/.lock"
flock -n 9 || { echo "이미 도는 중이다 ($OUT/.lock) — 중복 실행 안 한다"; exit 0; }

MPIRUN=${MPIRUN:-/usr/bin/mpirun}; [ -x "$MPIRUN" ] || MPIRUN=mpirun
PHYS=$(lscpu -p=Core,Socket 2>/dev/null | grep -v '^#' | sort -u | wc -l)
[ "${PHYS:-0}" -ge 1 ] || PHYS=$(nproc 2>/dev/null || echo 4)
NP=${NP:-$(( PHYS < 16 ? PHYS : 16 ))}
# ⚠ OMP 를 안 걸면 랭크마다 코어 수만큼 스레드를 띄운다 (2026-07-29 gabia: load 154).
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-1}
export MKL_NUM_THREADS=$OMP_NUM_THREADS OPENBLAS_NUM_THREADS=$OMP_NUM_THREADS
NPOOL=${NPOOL:-$(( NP % 4 == 0 ? 4 : (NP % 2 == 0 ? 2 : 1) ))}
ts() { date '+%m-%d %H:%M:%S'; }
echo "[$(ts)] repo=$REPO  out=$OUT  np=$NP -nk $NPOOL  OMP=$OMP_NUM_THREADS"

# ── pseudo 4종 (USPP) — KISTI 표기 / gabia 표기 둘 다 뒤진다, find-or-fail ──
PSE=$OUT/pseudo; mkdir -p "$PSE"
declare -A WANT=( [Li]='li*v1[._]4*uspp*UPF' [P]='P*rrkjus_psl*UPF'
                  [S]='s*v1[._]4*uspp*UPF'  [Cl]='cl*v1[._]4*uspp*UPF' )
declare -A GOT
for e in Li P S Cl; do
    f=$(ls "$PSE"/${WANT[$e]} 2>/dev/null | head -1)
    if [ -z "$f" ]; then
        f=$(find /data/work /data/apps /root "$HOME" -maxdepth 6 -iname "${WANT[$e]}" 2>/dev/null | head -1)
        [ -n "$f" ] && cp "$f" "$PSE/" && f="$PSE/$(basename "$f")"
    fi
    [ -n "$f" ] || { echo "ERROR: $e USPP pseudo 못 찾음 (패턴 ${WANT[$e]}) — gabia 어디에 있는지 붙여줘"; exit 1; }
    GOT[$e]=$(basename "$f"); echo "[pseudo] $e <- ${GOT[$e]}"
done

# ── 계통별 파라미터 ────────────────────────────────────────────────────────
#   nbnd = ceil(N_occ × 1.33).  comp1 240 e → N_occ 120 → 160
#                               modelc 294 e → N_occ 147 → 190
declare -A KMESH=( [comp1]='8 8 8 0 0 0'  [modelc]='8 8 2 0 0 0' )
declare -A NBND=(  [comp1]=160            [modelc]=190 )
declare -A KIRR=(  [comp1]=170            [modelc]=68 )   # 정본 레코드의 irr 수
declare -A TGAP=(  [comp1]=2.066          [modelc]=2.099 )
declare -A TVBM=(  [comp1]=2.128          [modelc]=2.445 )
declare -A TCBM=(  [comp1]=4.194          [modelc]=4.544 )

for S in ${SYSTEMS:-comp1 modelc}; do
    D=$OUT/$S; mkdir -p "$D"
    SCF0=$SRC/$S/${S}_scf.in
    [ -f "$SCF0" ] || { echo "!! $SCF0 없음 — 건너뜀"; continue; }

    # ---- scf 입력 패치 (pseudo_dir / pseudo 파일명 / outdir) ----
    sed -e "s|pseudo_dir *=.*|pseudo_dir  = '$PSE'|" \
        -e "s|outdir *=.*|outdir      = './tmp'|" "$SCF0" > "$D/scf.in"
    for e in Li P S Cl; do
        sed -i "s|^\(  *$e  *[0-9.]*  *\).*|\1${GOT[$e]}|" "$D/scf.in"
    done
    grep -q "${GOT[Li]}" "$D/scf.in" || { echo "!! $S: ATOMIC_SPECIES 치환 실패 — 건너뜀"; continue; }

    # ---- ① scf (smearing 그대로 — 밀도만 만들면 된다) ----
    if grep -aq "JOB DONE" "$D/scf.out" 2>/dev/null && [ -d "$D/tmp" ]; then
        echo "[$(ts)] $S scf: 이미 완료 — 건너뜀"
    else
        echo "[$(ts)] $S scf 시작 (k $(grep -A1 K_POINTS "$D/scf.in" | tail -1))"
        ( cd "$D" && "$MPIRUN" --oversubscribe -np "$NP" "$CPU/pw.x" -nk "$NPOOL" -in scf.in > scf.out 2>&1 )
        grep -aq "JOB DONE" "$D/scf.out" || { echo "!! $S scf 실패 — 마지막 20줄:"; grep -a . "$D/scf.out" | tail -20; continue; }
        echo "[$(ts)] $S scf 완료  E=$(grep -a '^!' "$D/scf.out" | tail -1 | awk '{print $5}') Ry"
    fi

    # ---- ② nscf: occupations='fixed' + nbnd + 조밀 k ----
    sed -e "s|calculation *=.*|calculation = 'nscf'|" \
        -e "s|occupations *=.*|occupations = 'fixed'|" \
        -e "/smearing *=/d" -e "/degauss *=/d" \
        -e "s|conv_thr *=.*|conv_thr = 1.0d-10|" \
        -e "s|^\( *ntyp *= *[0-9]*\)$|\1\n    nbnd  = ${NBND[$S]}|" "$D/scf.in" \
      | awk -v k="${KMESH[$S]}" '/K_POINTS/{print; getline; print k; next} {print}' > "$D/nscf_gap.in"
    grep -q "nbnd" "$D/nscf_gap.in" || sed -i "s|    ecutwfc|    nbnd  = ${NBND[$S]}\n    ecutwfc|" "$D/nscf_gap.in"
    for chk in "occupations = 'fixed'" "calculation = 'nscf'" "nbnd"; do
        grep -q "$chk" "$D/nscf_gap.in" || { echo "!! $S: nscf 입력에 '$chk' 없음 — 건너뜀"; continue 2; }
    done
    grep -q "smearing\|degauss" "$D/nscf_gap.in" && { echo "!! $S: smearing 잔존 — fixed 와 충돌한다. 건너뜀"; continue; }

    echo "[$(ts)] $S nscf(fixed, nbnd ${NBND[$S]}, k ${KMESH[$S]}) 시작 — 몇 시간 간다"
    ( cd "$D" && "$MPIRUN" --oversubscribe -np "$NP" "$CPU/pw.x" -nk "$NPOOL" -in nscf_gap.in > nscf_gap.out 2>&1 )

    # ---- ③ 계보 확인: irreducible k-point 수 ----
    NK=$(grep -a 'number of k points' "$D/nscf_gap.out" | head -1 | sed 's/.*number of k points=\s*//' | awk '{print $1}')
    if [ "$NK" = "${KIRR[$S]}" ]; then
        echo "   ★ irr k-point $NK = 정본 기록과 일치 — 셋업 계보 확인"
    else
        echo "   ⚠ irr k-point $NK ≠ 정본 기록 ${KIRR[$S]} — **셋업이 정본과 다르다**"
    fi

    grep -aq "JOB DONE" "$D/nscf_gap.out" || { echo "!! $S nscf 실패 — 마지막 20줄:"; grep -a . "$D/nscf_gap.out" | tail -20; continue; }

    # ---- ④ gap: fixed-occ 정본 경로 + 옛 경로 둘 다 찍어 대조 ----
    echo "[$(ts)] $S — fixed-occ (정본 규칙):"
    python3 "$SRC/extract_gap.py" "$D/nscf_gap.out" | sed 's/^/   /'
    echo "   ── 참고: 옛 comp1/modelc 값을 만든 EF-기준 파서 ──"
    python3 "$SRC/parse_eig_gap.py" "$D/nscf_gap.out" 2>/dev/null | sed 's/^/   /' || echo "   (EF 없음 = fixed-occ 정상)"
    echo "   ── 재현 목표: VBM ${TVBM[$S]}  CBM ${TCBM[$S]}  gap ${TGAP[$S]} ──"
done

echo "[$(ts)] 끝. 산출: $OUT/{comp1,modelc}/{scf.in,scf.out,nscf_gap.in,nscf_gap.out}"
echo "  ⚠ 정본(db/properties/electronic.json)은 **자동으로 안 고친다.** 위 숫자를 붙여주면 판정한다."
