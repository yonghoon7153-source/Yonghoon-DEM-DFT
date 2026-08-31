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

    # ── 2026-08-20 실측 사고 2건을 잠근다 ────────────────────────────────────
    # 사고 ①: `P*rrkjus_psl*` 가 **Po(폴로늄)** 을 물어 인 자리에 꽂았다.
    printf '<PP_HEADER element="Po" pseudo_type="US"/>\n' > "$T/Po.pbe-dn-rrkjus_psl.1.0.0.UPF"
    printf '<PP_HEADER element="P " pseudo_type="US"/>\n'  > "$T/P.pbe-n-rrkjus_psl.1.0.0.UPF"
    printf '<PP_HEADER element="Li" pseudo_type="US"/>\n'  > "$T/li_pbe_v1.4.uspp.F.UPF"
    _el() { python3 - "$1" <<'PY'
import re, sys
t = open(sys.argv[1], errors="ignore").read(8000)
m = re.search(r'element\s*=\s*["\']?\s*([A-Za-z]{1,2})', t, re.I) \
    or re.search(r'^\s*([A-Za-z]{1,2})\s+Element', t, re.I | re.M)
print(m.group(1).strip() if m else "")
PY
    }
    [ "$(_el "$T/Po.pbe-dn-rrkjus_psl.1.0.0.UPF")" = "Po" ] \
        && say "✓" "[음성] Po 파일의 element 를 Po 로 읽는다 (P 로 오독하지 않는다)" \
        || say "✗" "Po element 판독 실패"
    [ "$(_el "$T/P.pbe-n-rrkjus_psl.1.0.0.UPF")" = "P" ] \
        && say "✓" "P 파일의 element 를 P 로 읽는다" || say "✗" "P element 판독 실패"
    # 강화된 패턴은 기호 뒤 구분자를 요구해 Po 를 **구조적으로도** 배제한다
    n=$(ls "$T"/P[._]pbe*rrkjus*UPF 2>/dev/null | wc -l)
    [ "$n" = "1" ] && say "✓" "[음성] 패턴 P[._]pbe*rrkjus* 가 Po 를 안 문다 (후보 $n)" \
        || say "✗" "패턴이 아직 Po 를 문다 (후보 $n)"
    # 원소 확인이 켜져 있어야 한다 — 파일명만 보고 쓰면 같은 사고가 재발한다
    grep -q 'upf_element' "$0" && say "✓" "본문이 UPF element 를 확인한다" \
        || say "✗" "element 확인이 없다 (파일명만 믿는 상태)"

    # 사고 ②: ATOMIC_SPECIES 치환 sed 가 ATOMIC_POSITIONS 줄까지 갈아엎었다.
    cat > "$T/full.in" <<'EOF'
&SYSTEM
    nat   = 3
/
ATOMIC_SPECIES
  Li     6.941  OLD_LI.UPF
  P     30.974  OLD_P.UPF

CELL_PARAMETERS angstrom
     10.0  0.0  0.0
      0.0 10.0  0.0
      0.0  0.0 10.0

ATOMIC_POSITIONS angstrom
  P           5.10245859         5.02755577         5.02754844
  Li          1.10287556         1.24239041         6.27063290
  Li          6.13044979         6.26995588         6.27060613
K_POINTS automatic
4 4 4 0 0 0
EOF
    # (a) 옛 sed 가 실제로 좌표를 부수는지 재현 — 부수지 않으면 이 시험이 무의미하다
    cp "$T/full.in" "$T/bad.in"
    for e in Li P; do sed -i "s|^\(  *$e  *[0-9.]*  *\).*|\1NEW_$e.UPF|" "$T/bad.in"; done
    bad=$(awk '/^[[:space:]]*ATOMIC_POSITIONS/{f=1;next} f&&NF==4{n++} END{print n+0}' "$T/bad.in")
    [ "$bad" != "3" ] && say "✓" "[음성] 옛 sed 가 좌표를 부순다는 것을 재현 (4열 줄 $bad/3)" \
        || say "✗" "사고 재현 실패 — 이 시험이 아무것도 안 지킨다"

    # (b) 새 awk 는 ATOMIC_SPECIES 만 바꾸고 좌표 3줄을 그대로 둔다
    awk -v li="NEW_LI.UPF" -v pp="NEW_P.UPF" -v ss="NEW_S.UPF" -v cc="NEW_CL.UPF" '
        /^[[:space:]]*ATOMIC_SPECIES/ { inblk=1; print; next }
        inblk && /^[[:space:]]*(CELL_PARAMETERS|ATOMIC_POSITIONS|K_POINTS|OCCUPATIONS|CONSTRAINTS|ATOMIC_VELOCITIES|ATOMIC_FORCES|HUBBARD)/ { inblk=0 }
        inblk && NF==3 {
            f = ($1=="Li") ? li : ($1=="P") ? pp : ($1=="S") ? ss : ($1=="Cl") ? cc : ""
            if (f != "") { printf "  %-5s %8s  %s\n", $1, $2, f; next }
        }
        { print }
    ' "$T/full.in" > "$T/good.in"
    g=$(awk '/^[[:space:]]*ATOMIC_POSITIONS/{f=1;next} f&&NF==4{n++} f&&NF&&NF!=4{f=0} END{print n+0}' "$T/good.in")
    [ "$g" = "3" ] && say "✓" "새 awk 는 좌표 4열 3줄을 그대로 둔다" || say "✗" "좌표가 깨졌다 ($g/3)"
    grep -q "NEW_LI.UPF" "$T/good.in" && grep -q "NEW_P.UPF" "$T/good.in" \
        && say "✓" "ATOMIC_SPECIES 는 새 pseudo 로 바뀐다" || say "✗" "치환이 안 됐다"
    grep -q "OLD_LI.UPF\|OLD_P.UPF" "$T/good.in" && say "✗" "옛 pseudo 가 남았다" \
        || say "✓" "옛 pseudo 잔존 없음"
    # 좌표 줄에 pseudo 파일명이 끼어들면 안 된다
    awk '/^[[:space:]]*ATOMIC_POSITIONS/{f=1;next} f&&/UPF/{bad=1} END{exit bad}' "$T/good.in" \
        && say "✓" "[음성] 좌표 구역에 UPF 파일명이 새어들지 않았다" || say "✗" "좌표 구역이 오염됐다"
    # nat 대조 가드가 실제로 잡아내는지 (음성)
    nat=$(grep -a 'nat *=' "$T/bad.in" | head -1 | sed 's/.*= *//' | awk '{print $1}')
    [ "$bad" != "$nat" ] && say "✓" "[음성] nat 대조가 망가진 입력을 잡아낸다 ($bad ≠ $nat)" \
        || say "✗" "nat 대조가 망가진 입력을 통과시킨다"

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
# ⛔⛔ 2026-08-31 실측 사고 — **BTL 을 안 정하면 OpenMPI 가 단일 노드인데도 TCP 를
#   고른다.** modelc nscf 가 6.5일 돌다가 08-30 09:14 에 로컬 TCP 소켓이 끊겨
#   (`mca_btl_tcp_recv_blocking recv(25) failed: Connection reset by peer`)
#   31시간을 좀비로 서 있었다: 10 랭크 중 9개가 죽은 소켓의 블로킹 recv 에 걸려
#   CPU 0, 남은 1개가 코어 하나를 태우고 12 GB 를 문 채. **로그도 안 남고 죽지도
#   않는다** — 이 조합이 제일 나쁘다.
#   단일 노드에서는 공유메모리 BTL 만 쓴다. `self` = 자기 자신, `vader` = 공유메모리.
#   (판본이 vader 를 sm 으로 부르면 MPI_MCA 를 env 로 덮어라.)
MPI_MCA=${MPI_MCA:---mca btl self,vader}
PHYS=$(lscpu -p=Core,Socket 2>/dev/null | grep -v '^#' | sort -u | wc -l)
[ "${PHYS:-0}" -ge 1 ] || PHYS=$(nproc 2>/dev/null || echo 4)
NP=${NP:-$(( PHYS < 16 ? PHYS : 16 ))}
# ⚠ OMP 를 안 걸면 랭크마다 코어 수만큼 스레드를 띄운다 (2026-07-29 gabia: load 154).
# ⚠ `--oversubscribe` 는 코어보다 랭크를 많이 띄우는 것을 **허용**할 뿐 성능을 주지
#   않는다. 같은 기계에 남의 잡이 있으면 서로 굶는다 — 그때는 `MPI_OVERSUB=` 로 끄고
#   NP 를 실제 여유 코어에 맞춘다.
MPI_OVERSUB=${MPI_OVERSUB---oversubscribe}
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-1}
export MKL_NUM_THREADS=$OMP_NUM_THREADS OPENBLAS_NUM_THREADS=$OMP_NUM_THREADS
# ⛔ 2026-08-21 실측 — 첫 판의 기본값이 재앙이었다.
#   NP=10 → 10%4≠0 → 10%2==0 → NPOOL=2 로 떨어졌고, nscf 가 **2376 s/kpt**,
#   170 k-point 에 **112 시간** ETA 가 나왔다.
#   nscf 는 k-point 를 각각 독립으로 대각화한다 — 거의 완벽하게 병렬화되는 일을
#   pool 2개로 묶어 버린 것이다. 실측 기준 NPOOL 10 이면 같은 계산이 ~22 h 다.
#   ⇒ **pool 을 최대로 잡는다.** NP 를 나누는 가장 큰 약수를 쓴다.
#   ⚠ 메모리 대가가 있다: pool 당 랭크가 줄면 랭크당 데이터가 그만큼 커진다
#     (실측 comp1: 5랭크/pool 에서 633 MB → 1랭크/pool 이면 ~3.2 GB, 총 ~32 GB).
#     좁으면 NPOOL 을 손으로 낮춰라 — 이 값은 env 로 덮을 수 있다.
if [ -z "${NPOOL:-}" ]; then
    NPOOL=1
    for d in $(seq "$NP" -1 1); do
        [ $(( NP % d )) -eq 0 ] && { NPOOL=$d; break; }
    done
fi
ts() { date '+%m-%d %H:%M:%S'; }
echo "[$(ts)] repo=$REPO  out=$OUT  np=$NP -nk $NPOOL  OMP=$OMP_NUM_THREADS"
echo "[$(ts)] mpi: ${MPI_OVERSUB:-(no-oversubscribe)} $MPI_MCA  ← 단일 노드는 TCP 를 쓰지 않는다 (2026-08-31 사고)"

# ── pseudo 4종 (USPP) — KISTI 표기 / gabia 표기 둘 다 뒤진다 ────────────────
#
# ⛔⛔ 2026-08-20 실측 사고. 첫 판의 P 패턴이 `P*rrkjus_psl*UPF` 였는데
#    `find -iname` 이 **`Po.pbe-dn-rrkjus_psl.1.0.0.UPF`(폴로늄)** 를 물어왔고
#    스크립트는 그걸 인(P) 자리에 그대로 꽂았다. 파일명이 그럴듯해서 로그만 봐서는
#    안 걸린다 — 원소가 틀린 계산이 조용히 끝까지 돌 뻔했다.
#    ⇒ 교훈: **파일명으로 원소를 정하지 않는다. UPF 안의 element 를 읽어 확인한다.**
#    패턴도 기호 뒤에 구분자를 강제해(`P[._]`) Po/Pb/Si 류를 구조적으로 배제한다.
PSE=$OUT/pseudo; mkdir -p "$PSE"
declare -A WANT=( [Li]='li[._]pbe*uspp*UPF'   [P]='P[._]pbe*rrkjus*UPF'
                  [S]='s[._]pbe*uspp*UPF'     [Cl]='cl[._]pbe*uspp*UPF' )

# UPF 헤더의 element 를 읽는다 (v2 `element="P "` / v1 `  P   Element` 둘 다).
upf_element() {
    python3 - "$1" <<'PY'
import re, sys
t = open(sys.argv[1], errors="ignore").read(8000)
m = re.search(r'element\s*=\s*["\']?\s*([A-Za-z]{1,2})', t, re.I) \
    or re.search(r'^\s*([A-Za-z]{1,2})\s+Element', t, re.I | re.M)
print(m.group(1).strip() if m else "")
PY
}

declare -A GOT
for e in Li P S Cl; do
    f=""
    for cand in $(ls "$PSE"/${WANT[$e]} 2>/dev/null) \
                $(find /data/work /data/apps /root "$HOME" -maxdepth 6 -iname "${WANT[$e]}" 2>/dev/null); do
        [ -s "$cand" ] || continue
        got=$(upf_element "$cand")
        if [ "${got,,}" != "${e,,}" ]; then
            echo "[pseudo] ⚠ $cand 는 element='$got' — $e 가 아니다. 버린다."
            continue
        fi
        f="$cand"; break
    done
    [ -n "$f" ] || { echo "ERROR: $e USPP pseudo 못 찾음 (패턴 ${WANT[$e]}, element 확인 통과분 없음)"; exit 1; }
    [ "$(dirname "$f")" = "$PSE" ] || cp "$f" "$PSE/"
    GOT[$e]=$(basename "$f")
    echo "[pseudo] $e <- ${GOT[$e]}   (element 확인 완료)"
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

# 실패를 조용히 넘기지 않는다 — 첫 판이 6초 만에 두 계 다 죽고도 마지막 줄은
# "끝. 산출: ..." 였다. 성공한 것처럼 읽힌다.
FAILED=""
fail() { FAILED="$FAILED $1"; echo "!! $1: $2"; }

for S in ${SYSTEMS:-comp1 modelc}; do
    D=$OUT/$S; mkdir -p "$D"
    SCF0=$SRC/$S/${S}_scf.in
    [ -f "$SCF0" ] || { echo "!! $SCF0 없음 — 건너뜀"; continue; }

    # ---- scf 입력 패치 (pseudo_dir / pseudo 파일명 / outdir) ----
    #
    # ⛔⛔ 2026-08-20 실측 사고. 첫 판이
    #      sed -i "s|^\(  *$e  *[0-9.]*  *\).*|\1${GOT[$e]}|"
    #    였는데, 이 정규식은 ATOMIC_SPECIES 뿐 아니라 **ATOMIC_POSITIONS 줄도 문다**:
    #      "  P           5.10245859     5.02755577     5.02754844"
    #    → "  P           5.10245859P.pbe-...UPF"  (4열이 2열로 뭉개진다)
    #    QE 가 "wrong number of columns in ATOMIC_POSITIONS" 로 즉사했다.
    #    ⇒ 치환은 **ATOMIC_SPECIES 블록 안에서만**, 그리고 그 블록의 줄은 정확히 3열이다.
    #      (NF==3 가드가 두 번째 방어선 — 좌표 줄은 4열이라 구조적으로 안 걸린다.)
    sed -e "s|pseudo_dir *=.*|pseudo_dir  = '$PSE'|" \
        -e "s|outdir *=.*|outdir      = './tmp'|" "$SCF0" \
      | awk -v li="${GOT[Li]}" -v pp="${GOT[P]}" -v ss="${GOT[S]}" -v cc="${GOT[Cl]}" '
          /^[[:space:]]*ATOMIC_SPECIES/ { inblk=1; print; next }
          inblk && /^[[:space:]]*(CELL_PARAMETERS|ATOMIC_POSITIONS|K_POINTS|OCCUPATIONS|CONSTRAINTS|ATOMIC_VELOCITIES|ATOMIC_FORCES|HUBBARD)/ { inblk=0 }
          inblk && NF==3 {
              f = ($1=="Li") ? li : ($1=="P") ? pp : ($1=="S") ? ss : ($1=="Cl") ? cc : ""
              if (f != "") { printf "  %-5s %8s  %s\n", $1, $2, f; next }
          }
          { print }
      ' > "$D/scf.in"

    # 치환이 실제로 됐고, **좌표가 안 망가졌는지** 둘 다 확인한다.
    for e in Li P S Cl; do
        grep -q "${GOT[$e]}" "$D/scf.in" || { fail "$S" "$e pseudo 치환 실패"; continue 2; }
    done
    NAT=$(grep -a 'nat *=' "$D/scf.in" | head -1 | sed 's/.*= *//' | awk '{print $1}')
    NPOS=$(awk '/^[[:space:]]*ATOMIC_POSITIONS/{f=1;next} f&&NF==4{n++} f&&NF&&NF!=4{f=0} END{print n+0}' "$D/scf.in")
    if [ "${NPOS:-0}" != "${NAT:-x}" ]; then
        fail "$S" "ATOMIC_POSITIONS 4열 줄이 $NPOS 개인데 nat=$NAT 다 — 입력이 망가졌다"
        continue
    fi
    echo "[$(ts)] $S 입력 확인: nat=$NAT · 좌표 4열 $NPOS 줄 · pseudo 4종 치환 완료"

    # ---- ① scf (smearing 그대로 — 밀도만 만들면 된다) ----
    if grep -aq "JOB DONE" "$D/scf.out" 2>/dev/null && [ -d "$D/tmp" ]; then
        echo "[$(ts)] $S scf: 이미 완료 — 건너뜀"
    else
        echo "[$(ts)] $S scf 시작 (k $(grep -A1 K_POINTS "$D/scf.in" | tail -1))"
        ( cd "$D" && "$MPIRUN" $MPI_OVERSUB $MPI_MCA -np "$NP" "$CPU/pw.x" -nk "$NPOOL" -in scf.in > scf.out 2>&1 )
        grep -aq "JOB DONE" "$D/scf.out" || { fail "$S" "scf 실패 — 마지막 20줄:"; grep -a . "$D/scf.out" | tail -20; continue; }
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
        grep -q "$chk" "$D/nscf_gap.in" || { fail "$S" "nscf 입력에 '$chk' 없음"; continue 2; }
    done
    grep -q "smearing\|degauss" "$D/nscf_gap.in" && { fail "$S" "smearing 잔존 — fixed 와 충돌한다"; continue; }

    echo "[$(ts)] $S nscf(fixed, nbnd ${NBND[$S]}, k ${KMESH[$S]}) 시작 — 몇 시간 간다"
    ( cd "$D" && "$MPIRUN" $MPI_OVERSUB $MPI_MCA -np "$NP" "$CPU/pw.x" -nk "$NPOOL" -in nscf_gap.in > nscf_gap.out 2>&1 )

    # ---- ③ 계보 확인: irreducible k-point 수 ----
    NK=$(grep -a 'number of k points' "$D/nscf_gap.out" | head -1 | sed 's/.*number of k points=\s*//' | awk '{print $1}')
    if [ "$NK" = "${KIRR[$S]}" ]; then
        echo "   ★ irr k-point $NK = 정본 기록과 일치 — 셋업 계보 확인"
    else
        echo "   ⚠ irr k-point $NK ≠ 정본 기록 ${KIRR[$S]} — **셋업이 정본과 다르다**"
    fi

    grep -aq "JOB DONE" "$D/nscf_gap.out" || { fail "$S" "nscf 실패 — 마지막 20줄:"; grep -a . "$D/nscf_gap.out" | tail -20; continue; }

    # ---- ④ gap: fixed-occ 정본 경로 + 옛 경로 둘 다 찍어 대조 ----
    echo "[$(ts)] $S — fixed-occ (정본 규칙):"
    python3 "$SRC/extract_gap.py" "$D/nscf_gap.out" | sed 's/^/   /'
    echo "   ── 참고: 옛 comp1/modelc 값을 만든 EF-기준 파서 ──"
    python3 "$SRC/parse_eig_gap.py" "$D/nscf_gap.out" 2>/dev/null | sed 's/^/   /' || echo "   (EF 없음 = fixed-occ 정상)"
    echo "   ── 재현 목표: VBM ${TVBM[$S]}  CBM ${TCBM[$S]}  gap ${TGAP[$S]} ──"
done

if [ -n "$FAILED" ]; then
    echo "[$(ts)] ⛔ 실패한 계:$FAILED — **gap 값이 안 나왔다.** 위 오류를 먼저 고쳐야 한다."
    exit 1
fi
echo "[$(ts)] 끝. 산출: $OUT/{comp1,modelc}/{scf.in,scf.out,nscf_gap.in,nscf_gap.out}"
echo "  ⚠ 정본(db/properties/electronic.json)은 **자동으로 안 고친다.** 위 숫자를 붙여주면 판정한다."
