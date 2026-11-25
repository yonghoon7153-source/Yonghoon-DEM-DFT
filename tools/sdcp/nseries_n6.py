#!/usr/bin/env python3
"""nseries_n6.py — n-시리즈(스핀 분포)를 n=6 으로 잇는다. **seed 개입 없음.**

7월 n=1·2·3 을 낸 방법 그대로다:
  ① H-제거 doped 구조를 만든다 (charge 0, doublet)
  ② ORCA r2SCAN-3c 로 **그냥 돌린다** (fresh SCF — MORead·Rotate·NoIter 전부 없음)
  ③ `LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS` 를 그룹별로 합산

왜 이걸 따로 쓰나
  폴라론 pilot(S0)은 *"각 고리에 강제로 앉혀 보고 어느 게 안정한가"* 를 물었고
  그 개입이 막혔다(`kb/questions/polaron_seed_localized_basis_cannot_express_ring_pi.md`).
  이 스크립트는 그 센 질문을 **안 한다.** 7월과 같은 약한 질문 —
  *"그냥 수렴시키면 스핀이 어디 사는가"* — 만 하고, 그건 막힌 적이 없다.

  7월 실측:  n=1 백본 π ~35 % · n=2 32.6 % · n=3(mid) **50.1 %**  (크로스오버)
  이 스크립트가 채우는 칸: **n=6**

⛔ 이 도구가 **못 하는 것 · 안 하는 것**
  · **자가도핑이 일어나는지 판정하지 않는다.** 산화된 상태를 **주고** 그 안에서
    스핀이 어디 사는지 볼 뿐이다. 자가도핑의 자발성은 열역학
    (`db/properties/sdcp_v7c_li_binding.csv` 의 DPE·PA 분석)과 FT-IR 몫이다.
  · **폴라론을 원하는 자리에 놓지 못한다.** 그게 pilot 이고 막혀 있다.
  · SCF 가 여러 해를 가질 때 **어느 해로 갔는지 보증하지 않는다.** fresh start 한 번이다.
    (7월도 같은 한계였다 — n-시리즈끼리는 비교 가능하지만 "전역 최소" 가 아니다.)
  · 기하를 이완할지는 **사람이 정한다**(`--opt`). SP 는 중성 기하 위의 값이라
    폴라론의 격자 완화를 놓친다 — 7월은 Opt 였다. 섞어 인용하지 말 것.

사용:
  python3 tools/sdcp/nseries_n6.py --pilot /data/work/runs/sdcp_polaron_S0_v3 --out n6 --opt
  python3 tools/sdcp/nseries_n6.py --analyze n6        # 돌고 난 뒤
  python3 tools/sdcp/nseries_n6.py --selftest
"""
import argparse
import json
import os
import re
import sys

#: 7월 값 — 비교 기준. 출처: kb/results/sdcp_master_summary_2026_07_16.md §3
JULY = {1: {"so3": 65.0, "bb": 35.0}, 2: {"so3": 62.3, "bb": 32.6},
        "3end": {"so3": 54.6, "bb": 39.8}, "3mid": {"so3": 42.3, "bb": 50.1}}

#: ⛔ 2026-09-06 실물 — 여기 `%%` 를 쓰면 **입력에 그대로 `%%` 가 들어간다.**
#:   `%%` escape 는 %-포맷용이고 이 템플릿은 `.format()` 이다. ORCA 가
#:   `expected an identifier after '%'` 로 즉사했다(잡 하나 날림).
#:   selftest 가 생성물에 `%%` 가 없는지 본다 — 눈으로 안 보이는 종류라 기계가 봐야 한다.
INP = """! UKS r2SCAN-3c {run} TightSCF
%output
  Print[P_Loewdin] 1
end
%maxcore {maxcore}
%pal nprocs {nprocs} end
* xyzfile {charge} {mult} {xyz}
"""

#: 실행 스크립트. 입력만 주면 부르는 쪽이 **처방을 빠뜨린다** — 2026-09-06 이 잡이 그렇게 죽었다.
#: ⚠ 이 템플릿도 `.format()` 이라 셸의 `${{...}}` 는 중괄호를 두 번 쓴다 (위 `%%` 사고와 같은 부류).
RUN_SH = """#!/usr/bin/env bash
# n=6 doped 실행. `nseries_n6.py --opt` 가 만들었다 — 손으로 고치지 말고 다시 만든다.
#   bash run.sh            # 앞에서 돈다
#   nohup bash run.sh > run.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")"

# ⛔⛔ 중복 실행 가드 — 같은 폴더에서 ORCA 가 이미 돌면 **절대** 새로 걸지 않는다.
#   두 인스턴스가 같은 `.gbw` · `.tmp` · `.xyz` 를 덮어써 **둘 다** 망가진다.
#   2026-09-07 실물: 이 가드가 없는 QE 쪽에서 `pw.x` 두 개가 같은 `.save` 에 썼다.
#   ⚠ 전역 `pgrep orca` 로 보면 안 된다 — 다른 폴더의 정상 잡까지 막는다. **cwd 로** 가른다.
_here=$(pwd -P)
for _p in $(pgrep -x orca 2>/dev/null) $(pgrep -f orca_leanscf_mpi 2>/dev/null); do
  _c=$(readlink "/proc/$_p/cwd" 2>/dev/null) || continue
  if [ "$_c" = "$_here" ]; then
    echo "⛔ 이 폴더에서 ORCA 가 이미 돌고 있다 (pid $_p) — 걸지 않는다."
    echo "   상태:  bash <repo>/tools/sdcp/watch_n6.sh $_here"
    echo "   정말 갈아엎으려면 먼저 그 잡을 죽인다:  kill $_p"
    exit 3
  fi
done

# ⛔ MPI 전송층 처방 (정본 한 벌). 이게 없으면 단일노드인데 TCP BTL 로 통신하다
#   LEANSCF 에서 끊긴다 — gs3 두 번(09-05) · n6_doped 한 번(09-06) 실측.
# shellcheck disable=SC1090
. "{repo}/tools/sdcp/orca_mpi_env.sh"
orca_mpi_env_apply
echo "OMPI_MCA_btl=${{OMPI_MCA_btl:-<unset>}}  · $MPI_BTL_NOTE"

# ⛔ `%pal` 을 쓰면 ORCA 는 **전체 경로**로 불러야 한다 (이름으로 부르면 즉사한다 — Li 잡 4개 실물).
ORCA_BIN=${{ORCA:-$(command -v orca)}}
case "$ORCA_BIN" in
  /*) : ;;
  *)  echo "⛔ ORCA 절대경로를 못 찾았다: '${{ORCA_BIN:-<없음>}}' — ORCA=/path/to/orca 로 준다"; exit 2 ;;
esac
[ -x "$ORCA_BIN" ] || {{ echo "⛔ 실행할 수 없다: $ORCA_BIN"; exit 2; }}

# 옛 출력은 지우지 않고 밀어 둔다 — 재구성 이력이 증거다
n=0; while [ -e "n6_doped.out.$(printf %03d $n)" ]; do n=$((n+1)); done
[ -f n6_doped.out ] && mv n6_doped.out "n6_doped.out.$(printf %03d $n)"

echo "▶ $ORCA_BIN n6_doped.inp  ($(date '+%m-%d %H:%M:%S'))"
"$ORCA_BIN" n6_doped.inp > n6_doped.out 2>&1
rc=$?
echo "종료코드 $rc  ($(date '+%m-%d %H:%M:%S'))"
grep -aq HURRAY n6_doped.out && echo "✅ 이완수렴" || echo "⚠ HURRAY 없음 — watch_n6.sh 로 이유를 본다"
exit $rc
"""


def _xyz_symbols(path):
    """xyz → [원소기호]. 못 읽으면 빈 리스트 (조용히 추측하지 않는다)."""
    try:
        ln = open(path, encoding="utf-8").read().splitlines()
        n = int(ln[0].split()[0])
        return [x.split()[0] for x in ln[2:2 + n] if x.split()]
    except Exception:
        return []


def _ring_atoms(rings, symbols):
    """manifest 의 rings → **7월 정의**의 고리 원자 (H 제외 · 에테르 O 제외).

    실제 형식 (`pilot_components`)::

        rings["ring0"] = {"core": [고리원자 ∪ 고리H], "ether_O": [...]}

    ⛔ **`core` 를 그대로 쓰면 안 된다** — 고리 H 가 섞여 있다. 7월
      (`build_v7c_dimer.py`: ring = [rS] + alphas + betas)은 H 를 안 넣었다.
      그래서 xyz 의 원소로 H 를 걸러낸다.

    ⛔ 못 하는 것: `symbols` 가 없거나 길이가 안 맞으면 **빈 집합**을 준다.
      H 를 못 가른 채로 "7월 정의" 라고 부르지 않는다.
    """
    if not symbols or not isinstance(rings, dict):
        return set()
    out = set()
    for v in rings.values():
        core = (v.get("core") if isinstance(v, dict) else v) or []
        for i in core:
            i = int(i)
            if 0 <= i < len(symbols) and symbols[i].upper() != "H":
                out.add(i)
    return out


def build(pilot, out, opt, nprocs, maxcore):
    """pilot 산출물에서 기하·그룹을 가져와 n=6 잡을 만든다. **새로 만들지 않는다** —
    pilot 이 이미 봉인한 것을 쓴다(같은 구조를 두 번 정의하면 갈라진다)."""
    man = json.load(open(os.path.join(pilot, "MANIFEST_PILOT.json"), encoding="utf-8"))
    amf = man.get("atom_manifest") or {}
    if "D" not in amf:
        sys.exit("⛔ MANIFEST_PILOT.json 에 atom_manifest.D 가 없다 — 구판 번들이다")
    os.makedirs(out, exist_ok=True)
    # D• 기하: probe 가 쓴 것과 **같은 파일**을 가져온다 (다시 만들지 않는다)
    src = None
    for r, _d, fs in os.walk(os.path.join(pilot, "S0P")):
        for f in fs:
            if f.endswith(".xyz") and "Dradical" in r:
                src = os.path.join(r, f)
                break
        if src:
            break
    if not src:
        sys.exit("⛔ S0P/…/Dradical 밑에서 .xyz 를 못 찾았다 — pilot 경로를 확인하세요")
    xyz = "n6_doped.xyz"
    open(os.path.join(out, xyz), "w").write(open(src, encoding="utf-8").read())
    run = "Opt" if opt else "SP"
    open(os.path.join(out, "n6_doped.inp"), "w").write(
        INP.format(run=run, charge=0, mult=2, xyz=xyz,
                   nprocs=nprocs, maxcore=maxcore))
    # 그룹: manifest 의 D 프레임을 그대로 옮긴다 (0-based → 그대로 쓴다)
    D = amf["D"]
    # ⛔⛔ 7월(n=1·2·3)의 backbone 정의는 **티오펜 고리 원자만**이다
    #   (`build_v7c_dimer.py`: ring = [rS] + alphas + betas — 고리 H 도, 에테르 O 도 없다).
    #   pilot 의 `backbone_strict` 는 거기에 **고리 H 를 더한다**(bb_core = ring_atoms | ring_H).
    #   두 정의를 한 표에 올리면 이 세션에서 반복된 그 실수다. 7월과 **글자 그대로 같은**
    #   분할을 따로 만들어서, n=1→6 을 같은 자로 잰다.
    rings = D.get("rings") or {}
    syms = _xyz_symbols(os.path.join(out, xyz))
    if len(syms) != D["n_atoms"]:
        sys.exit(f"⛔ xyz 원자수({len(syms)}) 가 manifest({D['n_atoms']}) 와 다르다 — "
                 f"기하가 D 프레임이 아니다")
    july = sorted(_ring_atoms(rings, syms))
    groups = {"backbone_july": july,                       # ← n-시리즈 비교는 이걸로
              "backbone_strict": D["derived"]["backbone_strict"],
              "backbone_extended": D["derived"]["backbone_extended"],
              "sulfonate": sorted(D["components"].get("sulfonate", [])),
              "rings": rings}
    if not july:
        sys.exit("⛔ manifest 의 rings 에서 고리 원자를 못 뽑았다 — 7월 정의를 재현할 수 없다. "
                 "구조를 확인하기 전에는 n-시리즈에 값을 얹지 않는다")
    json.dump({"groups": groups, "n_atoms": D["n_atoms"], "symbols": list(syms),
               "source_manifest": os.path.abspath(os.path.join(pilot, "MANIFEST_PILOT.json")),
               "source_xyz": os.path.abspath(src),
               "run": run,
               "⚠": ("7월 n=1·2·3 은 **Opt** 였다. SP 로 돌린 값과 섞어 인용하지 말 것 — "
                     "폴라론은 격자 완화와 얽혀 있어 SP 는 국재화를 과소평가한다.")},
              open(os.path.join(out, "groups.json"), "w"), ensure_ascii=False, indent=1)
    # ⛔⛔ 2026-09-06 실물 — 이 잡이 **LEANSCF 에서 MPI 로 죽었다** (SCF 는 수렴까지 갔다).
    #   같은 고장이 하루 전 gs3 을 두 번 죽였고 처방(`orca_mpi_env.sh`)도 이미 있었는데,
    #   이 러너가 새 파일이라 **물려받지 못했다.** 그래서 입력만 뱉지 말고 **실행 스크립트를
    #   같이** 뱉는다 — 처방이 잡을 따라다니게. `%pal` 은 ORCA 를 전체 경로로 요구한다.
    open(os.path.join(out, "run.sh"), "w").write(RUN_SH.format(
        repo=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))))
    os.chmod(os.path.join(out, "run.sh"), 0o755)
    print(f"→ {out}/  n6_doped.inp ({run}) · n6_doped.xyz ({D['n_atoms']}원자) · groups.json · run.sh")
    print(f"   기하 출처: {src}")
    print(f"   backbone_july {len(july)} (7월 정의 · 고리원자만) · "
          f"strict {len(groups['backbone_strict'])} (+고리H) · "
          f"extended {len(groups['backbone_extended'])} (+에테르O) · "
          f"sulfonate {len(groups['sulfonate'])}")
    print(f"   실행:  cd {out} && $ORCA n6_doped.inp > n6_doped.out")
    if not opt:
        print("   ⚠ SP 다 — 7월(Opt)과 섞어 인용하지 말 것. Opt 는 --opt")


def parse_loewdin(txt):
    """마지막 `LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS` 블록 → {idx: spin}.

    ⛔ 못 하는 것: 블록이 없으면 None 을 준다 — 0 이 아니다. 미완료를 완료로 읽지 않는다.
    """
    hdr = "LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS"
    if hdr not in txt:
        return None
    seg = txt.split(hdr)[-1]
    out = {}
    for ln in seg.splitlines()[1:]:
        m = re.match(r"\s*(\d+)\s+\w+\s*:\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)", ln)
        if m:
            out[int(m.group(1))] = float(m.group(3))
        elif out:
            break
    return out or None


def _xyz_coords(path):
    """xyz → [(sym, x, y, z)]. 좌표가 필요한 것은 도핑 자리 추적뿐이다."""
    out = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        n = int(f.readline().split()[0]); f.readline()
        for _ in range(n):
            t = f.readline().split()
            out.append((t[0], float(t[1]), float(t[2]), float(t[3])))
    return out


def doping_site(d, g):
    """어느 고리의 SO₃H 에서 H 를 뗐나 → ("ring3", 근거) | (None, 사유).

    라벨(`B_ring3`)을 **믿지 않고** 실물에서 찾는다: 도핑 구조에서 **양성자가 없는**
    sulfonate 를 찾고, 그 S 에서 곁사슬을 따라가 처음 만나는 고리를 돌려준다.

    ⛔ 못 하는 것
      · 결합을 양자화학으로 판정하지 않는다 — 원소별 공유결합 반경 합 × 1.25 의 거리 기준이다.
      · SO₃H 가 둘 이상 탈양성자된 구조(다중 도핑)는 다루지 않는다 — 그런 경우 None 을 준다.
      · 고리 번호의 **의미**(사슬 어느 끝부터 세는가)는 groups.json 이 정한다. 여기서는
        그 키를 그대로 돌려줄 뿐이다.
    """
    xp = os.path.join(d, "n6_doped.xyz")
    if not os.path.isfile(xp):
        return None, "n6_doped.xyz 가 없다"
    at = _xyz_coords(xp)
    gr = g.get("groups") or {}
    rings = gr.get("rings") or {}
    if not isinstance(rings, dict) or not rings:
        return None, "groups.json 에 rings dict 가 없다"
    RCOV = {"H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66, "S": 1.05}

    def bonded(i, j):
        (a, x1, y1, z1), (b, x2, y2, z2) = at[i], at[j]
        r = RCOV.get(a.capitalize(), 0.8) + RCOV.get(b.capitalize(), 0.8)
        return ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2) ** 0.5 < r * 1.25

    nbr = {i: [j for j in range(len(at)) if j != i and bonded(i, j)] for i in range(len(at))}
    sul = set(gr.get("sulfonate") or [])
    s_idx = [i for i in sul if at[i][0].capitalize() == "S"]
    # 탈양성자된 S: 그 S 의 산소 중 어느 것에도 H 가 안 붙어 있다
    bare = []
    for i in s_idx:
        oxy = [j for j in nbr[i] if at[j][0].capitalize() == "O"]
        if not any(at[k][0].capitalize() == "H" for j in oxy for k in nbr[j]):
            bare.append(i)
    if len(bare) != 1:
        return None, f"탈양성자된 sulfonate 가 {len(bare)}개다 (1개여야 한다)"
    # 고리 원자 집합 (core 그대로 — 여기서는 H 제외가 중요하지 않다)
    ring_of = {}
    for k, v in rings.items():
        for i in ((v.get("core") if isinstance(v, dict) else v) or []):
            ring_of[i] = k
    # S 에서 시작해 산소를 건너 곁사슬을 따라간다 (BFS)
    seen, q = {bare[0]}, [bare[0]]
    while q:
        cur = q.pop(0)
        for j in nbr[cur]:
            if j in seen:
                continue
            if j in ring_of:
                return ring_of[j], (f"탈양성자 S={bare[0]} → 곁사슬 → 원자 {j} "
                                    f"({at[j][0]}) 가 {ring_of[j]} 에 속한다")
            seen.add(j); q.append(j)
    return None, f"탈양성자 S={bare[0]} 에서 고리에 도달하지 못했다"


def analyze(d):
    g = json.load(open(os.path.join(d, "groups.json"), encoding="utf-8"))
    p = os.path.join(d, "n6_doped.out")
    if not os.path.isfile(p):
        sys.exit(f"⛔ {p} 가 없다 — 아직 안 돌았다")
    txt = open(p, encoding="utf-8", errors="ignore").read()
    if "ORCA TERMINATED NORMALLY" not in txt:
        print("⚠ ORCA 정상종료 표시가 없다 — 아래 값은 중간값일 수 있다")
    sp = parse_loewdin(txt)
    if sp is None:
        sys.exit("⛔ Loewdin 스핀 블록이 없다 — 계산이 거기까지 안 갔다")
    tot = sum(sp.values())
    print(f"총 스핀 = {tot:.3f}  (더블렛이면 ~1.0)")
    if abs(tot - 1.0) > 0.15:
        print("  ⚠ 1.0 에서 멀다 — 스핀 오염이나 다른 해로 갔을 수 있다")
    gr = g["groups"]
    res = {}
    for name in ("sulfonate", "backbone_july", "backbone_strict", "backbone_extended"):
        idx = gr.get(name) or []
        res[name] = 100.0 * sum(sp.get(i, 0.0) for i in idx) / tot if tot else 0.0
        print(f"  {name:20s} {res[name]:6.1f} %  ({len(idx)}원자)")
    site, why = doping_site(d, g)
    if site:
        print(f"\n  ★ 도핑 자리 = **{site}** — {why}")
        print(f"     (라벨 `{os.path.basename(os.path.dirname(g.get('source_xyz','') or 'x/y'))}` "
              "가 아니라 실물 구조에서 찾은 값이다)")
    else:
        print(f"\n  ⚠ 도핑 자리 미확인 — {why}")
    rings = gr.get("rings") or {}
    if isinstance(rings, dict) and rings:
        # ⛔ 2026-09-08 실물 — "고리별:" 헤더만 찍히고 행이 하나도 없었다. rings 값은
        #   manifest 형식 그대로 **dict** ({"core": [...], "ether_O": [...]}) 인데 이 루프는
        #   list 만 받아 조용히 건너뛰었다 (fail-silent). 7월 표의 '고리별 분해' 열
        #   (A 14.0 / B 21.3 / C 14.9) 이 n=6 에서 비어 나가는 결과였다.
        #   core 에는 고리 H 가 섞여 있으므로(7월은 H 제외) **두 값을 나눠** 찍는다.
        syms = g.get("symbols") or []
        if not syms:
            # ⚠ 옛 groups.json(2026-09-08 이전)에는 symbols 가 없다. 같은 폴더의 n6_doped.xyz 에서
            #   읽는다 — ORCA Opt 가 좌표는 덮어쓰지만 **원자 순서는 보존**하므로 원소열은 그대로다.
            #   (실측: 이 폴백이 없어 ring0·ring5 의 말단 α-H 를 못 걸러 '+고리H' 값이 나갔다.)
            _xp = os.path.join(d, "n6_doped.xyz")
            if os.path.isfile(_xp):
                try:
                    syms = _xyz_symbols(_xp)
                    if len(syms) != g.get("n_atoms", len(syms)):
                        syms = []          # 원자수가 다르면 믿지 않는다
                except Exception:
                    syms = []
        print("  고리별 (7월 정의 = 고리 원자만 · 참고 = +고리H):")
        any_row = False
        for k in sorted(rings):
            v = rings[k]
            core = (v.get("core") if isinstance(v, dict) else v) or []
            core = [int(i) for i in core]
            july_idx = [i for i in core if not (0 <= i < len(syms) and syms[i].upper() == "H")] if syms else None
            pj = 100.0 * sum(sp.get(i, 0.0) for i in (july_idx if july_idx is not None else core)) / tot
            pc = 100.0 * sum(sp.get(i, 0.0) for i in core) / tot
            tag = "" if syms else "  (⚠ symbols 없음 — H 못 걸러 +고리H 값)"
            print(f"    {k:12s} {pj:6.1f} %   (참고 +고리H {pc:5.1f} % · {len(core)}원자){tag}")
            any_row = True
        if not any_row:
            print("    ⚠ rings 에 원자 목록이 없다 — 고리별 분해를 낼 수 없다")
    print()
    print("  n-시리즈 (7월, Opt · kb/results/sdcp_master_summary_2026_07_16.md §3):")
    print(f"    n=1        SO3 {JULY[1]['so3']:.1f} / 백본 {JULY[1]['bb']:.1f}")
    print(f"    n=2        SO3 {JULY[2]['so3']:.1f} / 백본 {JULY[2]['bb']:.1f}")
    print(f"    n=3 end    SO3 {JULY['3end']['so3']:.1f} / 백본 {JULY['3end']['bb']:.1f}")
    print(f"    n=3 mid    SO3 {JULY['3mid']['so3']:.1f} / 백본 {JULY['3mid']['bb']:.1f}  ← 크로스오버")
    print(f"    n=6        SO3 {res['sulfonate']:.1f} / 백본 {res['backbone_july']:.1f}"
          f"   ← 이번 (7월과 같은 분할: 고리 원자만)")
    print(f"      참고    같은 계를 다른 분할로: strict(+고리H) {res['backbone_strict']:.1f} · "
          f"extended(+에테르O) {res['backbone_extended']:.1f}")
    print("      ⛔ 위 표에 올리는 것은 **backbone_july 뿐이다** — 다른 분할을 7월 값 옆에 놓지 않는다")
    print()
    print(f"  ⚠ 이번 실행은 **{g['run']}** 이다. {g['⚠']}")
    print("  ⛔ 이 값은 '자가도핑이 일어난다' 의 증거가 아니다 — 산화된 상태를 **주고**")
    print("     그 안에서 스핀이 어디 사는지 본 것이다. 자발성은 열역학·FT-IR 몫이다.")


def selftest():
    ok = bad = 0

    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m)
        ok, bad = (ok + 1, bad) if c else (ok, bad + 1)

    good = ("LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS\n"
            "-----\n"
            "   0 C :   -0.123456    0.400000\n"
            "   1 O :    0.111111    0.600000\n"
            "\nTimings\n")
    sp = parse_loewdin(good)
    chk(sp == {0: 0.4, 1: 0.6}, "판독: 인덱스와 **스핀 열**(3번째 수)을 읽는다")
    chk(parse_loewdin("아무것도 없음") is None,
        "⛔음성: 블록이 없으면 None — 0 이 **아니다**(미완료를 완료로 안 읽는다)")
    chk(parse_loewdin(good.replace("0.400000", "x")) == {1: 0.6},
        "⛔음성: 깨진 줄은 건너뛰고 조용히 0 으로 채우지 않는다")
    two = good + "LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS\n-----\n   0 C :  0.0  0.900000\n\nTimings\n"
    chk(parse_loewdin(two) == {0: 0.9},
        "블록이 여럿이면 **마지막**을 쓴다 (Opt 중간 블록을 안 읽는다)")
    # 전하 열을 스핀으로 잘못 읽으면 안 된다 — 음수 전하가 그대로 나오면 실패
    chk(all(v >= 0 for v in (parse_loewdin(good) or {}).values()),
        "⛔음성: 2번째 열(전하)을 스핀으로 읽지 않는다")
    # ── 입력 생성 (2026-09-06 실물 버그: `%%` 가 그대로 남아 ORCA 즉사) ──
    txt = INP.format(run="Opt", charge=0, mult=2, xyz="x.xyz", nprocs=8, maxcore=2500)
    chk("%%" not in txt, "⛔음성: 생성된 입력에 `%%` 가 남지 않는다 (ORCA 가 즉사한다)")
    chk(txt.count("%pal") == 1 and txt.count("%maxcore") == 1 and txt.count("%output") == 1,
        "블록 셋이 각각 한 번씩 들어간다")
    chk("nprocs 8" in txt and "%maxcore 2500" in txt and "0 2 x.xyz" in txt,
        "인자가 실제로 꽂힌다 (전하 0 · 다중도 2 = doublet)")
    chk("{" not in txt and "}" not in txt, "⛔음성: 안 채워진 자리표시자가 남지 않는다")
    # ── run.sh (2026-09-06 실물: 처방을 안 물려받아 LEANSCF 에서 MPI 로 죽었다) ──
    sh = RUN_SH.format(repo="/REPO")
    chk("orca_mpi_env.sh" in sh and "orca_mpi_env_apply" in sh,
        "⛔음성: 실행 스크립트가 **MPI 처방을 달고 나온다** (입력만 주면 부르는 쪽이 빠뜨린다)")
    # ⚠ 이 시험의 v1 은 `"{" not in sh` 였다 — **틀렸다.** 셸의 `${...}` 는 남아야 맞다.
    #   INP 쪽 규칙(자리표시자가 안 남아야 한다)을 생각 없이 옮긴 것이다.
    #   봐야 할 것은 셋: 이스케이프가 풀렸나 · 이중중괄호가 새 나갔나 · 안 채운 자리가 있나.
    chk("${OMPI_MCA_btl" in sh, "셸 변수 확장이 살아남는다 (`{{}}` 이스케이프가 풀렸다)")
    chk("{{" not in sh and "}}" not in sh, "⛔음성: 이중중괄호가 그대로 새 나가지 않는다")
    chk("{repo}" not in sh and "/REPO/tools/sdcp/orca_mpi_env.sh" in sh,
        "⛔음성: 안 채운 자리표시자가 남지 않는다 (repo 경로가 실제로 꽂힌다)")
    chk("command -v orca" in sh and "exit 2" in sh,
        "⛔음성: ORCA 를 **절대경로로 못 찾으면 돌리지 않고 멈춘다** (%pal 은 full pathname 요구)")
    chk("n6_doped.out." in sh, "옛 .out 을 지우지 않고 밀어 둔다 (재구성 이력이 증거다)")
    # ── 중복 실행 가드 (2026-09-07: QE 쪽에서 pw.x 둘이 같은 .save 에 썼다) ──
    chk("readlink" in sh and "/proc/" in sh and "cwd" in sh,
        "⛔음성: 중복 판정을 **cwd 로** 한다 (전역 pgrep 은 다른 폴더의 정상 잡까지 막는다)")
    chk("exit 3" in sh and sh.index("pgrep -x orca") < sh.index("orca_mpi_env.sh"),
        "⛔음성: 가드가 **실행보다 먼저** 온다 (뒤에 있으면 이미 파일을 건드린 뒤다)")
    import subprocess as _sp
    chk(_sp.run(["bash", "-n", "-c", sh], capture_output=True).returncode == 0,
        "⛔음성: 생성된 run.sh 가 **문법으로 성립한다** (bash -n — 돌려 봐야 아는 건 너무 늦다)")
    # ── rings 판독 (2026-09-06 실물: core 는 고리원자 ∪ 고리H 다) ──
    R = {"ring0": {"core": [0, 1, 2, 3], "ether_O": [9]},
         "ring1": {"core": [4, 5, 6], "ether_O": []}}
    SY = ["S", "C", "C", "H", "S", "C", "H", "X", "X", "O"]
    chk(_ring_atoms(R, SY) == {0, 1, 2, 4, 5},
        "⛔음성: core 에서 **고리 H 를 뺀다** (그냥 쓰면 7월 정의가 아니다)")
    chk(_ring_atoms(R, []) == set(),
        "⛔음성: 원소를 모르면 빈 집합 — H 를 못 가른 채 '7월 정의' 라 부르지 않는다")
    chk(_ring_atoms({"r": [0, 1, 3]}, SY) == {0, 1},
        "core 키가 없는 옛 형식도 받는다")
    chk(_ring_atoms(R, SY).isdisjoint({9}),
        "⛔음성: 에테르 O 를 고리에 넣지 않는다")
    # ── 도핑 자리 추적 (합성 구조) ──────────────────────────────────────
    import tempfile as _tf
    with _tf.TemporaryDirectory() as _d:
        # S(0)–O(1,2,3), O3–H(4) 는 **양성자 있음**;  S(5)–O(6,7,8) 은 없음(탈양성자)
        # 곁사슬: O8–C(9)–C(10) 이고 C10 이 ring1 의 core 에 속한다
        rows = [("S", 0, 0, 0), ("O", 1.45, 0, 0), ("O", -1.45, 0, 0), ("O", 0, 1.45, 0),
                ("H", 0, 2.4, 0),
                ("S", 0, 0, 10), ("O", 1.45, 0, 10), ("O", -1.45, 0, 10), ("O", 0, 1.45, 10),
                ("C", 0, 2.85, 10), ("C", 0, 4.3, 10)]
        with open(os.path.join(_d, "n6_doped.xyz"), "w") as f:
            f.write(f"{len(rows)}\ntest\n")
            for sy, x, y, z in rows:
                f.write(f"{sy} {x} {y} {z}\n")
        gg = {"groups": {"sulfonate": [0, 1, 2, 3, 4, 5, 6, 7, 8],
                         "rings": {"ring0": {"core": [99]}, "ring1": {"core": [10]}}}}
        st, wh = doping_site(_d, gg)
        chk(st == "ring1", f"★ 탈양성자 sulfonate 에서 곁사슬을 따라 ring1 을 찾는다 (얻음 {st})")
        gg2 = json.loads(json.dumps(gg)); gg2["groups"]["sulfonate"] = [5, 6, 7, 8]
        st2, wh2 = doping_site(_d, gg2)
        chk(st2 == "ring1", "sulfonate 목록에 탈양성자 S 만 있어도 찾는다")
        gg3 = json.loads(json.dumps(gg)); gg3["groups"]["rings"] = {}
        chk(doping_site(_d, gg3)[0] is None, "⛔음성: rings 가 없으면 None (추측하지 않는다)")
        # ⛔음성: 탈양성자 S 가 둘이면 판정하지 않는다
        rows2 = rows[:4] + [("H", 0, 2.4, 99)] + rows[5:]     # 첫 S 의 H 를 멀리 보낸다
        with open(os.path.join(_d, "n6_doped.xyz"), "w") as f:
            f.write(f"{len(rows2)}\ntest\n")
            for sy, x, y, z in rows2:
                f.write(f"{sy} {x} {y} {z}\n")
        chk(doping_site(_d, gg)[0] is None, "⛔음성: 탈양성자 S 가 2개면 판정하지 않는다")

    print(f"  selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", help="폴라론 pilot 디렉터리 (MANIFEST_PILOT.json 이 있는 곳)")
    ap.add_argument("--out", default="n6")
    ap.add_argument("--opt", action="store_true", help="기하 이완 (7월과 같은 조건)")
    ap.add_argument("--nprocs", type=int, default=8)
    ap.add_argument("--maxcore", type=int, default=2500)
    ap.add_argument("--analyze", help="돌고 난 디렉터리")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.analyze:
        return analyze(a.analyze)
    if not a.pilot:
        ap.error("--pilot 또는 --analyze 또는 --selftest")
    return build(a.pilot, a.out, a.opt, a.nprocs, a.maxcore)


if __name__ == "__main__":
    sys.exit(main() or 0)
