#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pure-SE 침대 **OAT 민감도** + **E 스윕** LIGGGHTS 입력 생성기.

★★ 왜 (2026-08-25, Coetzee 2017 digest 후):  우리 보정은 "관측량 1개(porosity@300) →
  파라미터 1개(E_eff)" 라 **형식상** 유일하다.  그런데 그 형식을 떠받치는 전제 —
  *"구속 단축압축은 입자강성에만 반응하고 마찰에는 둔감하다"* — 는 **남의 계에서 빌려온
  것**이다 (Coetzee &amp; Els 의 파쇄암·옥수수·저응력 결과).  **우리 계에서 재현된 적이 없다.**

  Coetzee 리뷰 §5 가 요구하는 것은 명확하다:
    "more than one experiment should be conducted and **each experiment should isolate a
     single parameter**"
  ⇒ 우리 시험이 정말 E 를 고립시키는지 **재고 나서** "우리 보정은 파라미터를 고립시킨다"
  라고 쓸 자격이 생긴다.  ∂ε/∂μ ≈ 0 이 나와야 한다.  안 나오면 **보정이 뒤엉킨 것**이고
  그건 그것대로 알아야 할 사실이다.

  ⚠ 이 스크립트는 **입력만 만든다.  시뮬레이션은 돌리지 않는다** (이 보드에서 계산 금지).

## 두 표

**표 A — OAT 민감도** (E_eff 고정 1.35 GPa):
  `mu_pp` · `mu_pw` · `cor` 를 각각 {0.2, 0.4, 0.6} 으로 흔들고 나머지는 생산값.  9 런.

**표 B — E 스윕** (생산 마찰 고정): E ∈ {24, 5, 1.35} GPa.
  출력은 porosity 뿐 아니라 **배위수 · 접촉면적 · σ 삼중항**.
  ⇒ Ng &amp; Asce 가 보고한 *"강성↓ → 배위수↑"* 결합이 우리 24→1.35 구간에서 **미측정**이다.
  역학(porosity)으로 정한 E 가 전달 그래프를 어떻게 바꾸는지 보는 것이 목적.
  ⚠ E=24 는 300 MPa 에서 **덜 압밀될 것**이다 — 그게 결함이 아니라 **측정 대상**이다.

## ⚠⚠ 이 생성기가 원본 입력에 가하는 **구조 변경 1건** (반드시 읽을 것)

원본 `heckel/input_SE_heckel_300.liggghts` 는 **atom type 이 1개**다.  LIGGGHTS 에서 벽은
`type N` 으로 재료 물성을 참조하므로, type 이 하나면 **벽 마찰이 입자 마찰과 같은 값에
묶인다** → `mu_pw` 를 독립적으로 흔들 수 없다.

⇒ 이 생성기는 **type 을 2개로 늘리고 벽에 type 2 를 준다** (입자는 type 1).
   `peratomtype` 는 값 2개, `peratomtypepair` 는 2×2 = 4개가 된다.

⚠⚠ **이건 검증된 입력의 구조를 바꾸는 것**이므로 **대조 런이 필요하다.  그런데 하나로는
   부족하다** — 윈도우 재설치로 옛 LIGGGHTS 바이너리가 사라져 새로 빌드해야 하므로,
   기준선이 옛 기록과 안 맞아도 원인이 **type 리팩터**인지 **다른 빌드**인지 못 가른다.
   ⇒ 대조를 **둘** 돌린다 (합 13 런):
     · `orig_1type` (새 빌드 · 원본 1-type, 출력 경로만 변경)  vs 옛 기록  → **빌드 효과**
     · `base`       (새 빌드 · 2-type 생산값)  vs `orig_1type`  → **리팩터 효과**
   둘 다 0 이어야 OAT 를 믿는다.  러너가 이 순서로 먼저 돌리고 실패하면 멈춘다.

    python3 scripts/gen_dem_oat_sweep.py --check          # 계획만 (쓰지 않음)
    python3 scripts/gen_dem_oat_sweep.py --write          # dem_scripts/oat_sweep/ 에 생성
    python3 scripts/gen_dem_oat_sweep.py --selftest
"""
from __future__ import annotations

import argparse
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, '..'))
BASE = os.path.join(_ROOT, 'heckel', 'input_SE_heckel_300.liggghts')
OUTDIR = os.path.join(_ROOT, 'dem_scripts', 'oat_sweep')

#: 생산값 (원본 입력에서 읽은 것 — 추측 아님).  ⚠ 스케일계: E*0.001 (1.35 GPa → 0.135e7)
PROD = {'mu_pp': 0.5, 'mu_pw': 0.5, 'cor': 0.3, 'roll': 0.1, 'E_GPa': 1.35}

#: 표 A — 흔들 노브와 수준 (사용자 지정)
OAT_LEVELS = (0.2, 0.4, 0.6)
OAT_KNOBS = ('mu_pp', 'mu_pw', 'cor')

#: 표 B — E 스윕 (GPa).  1.35 = 생산 · 5 = 중간 · 24 = 실물 결정
E_SWEEP_GPA = (1.35, 5.0, 24.0)


def e_scaled(e_gpa):
    """GPa → 입력 파일의 스케일 단위.  원본 주석: `Scale: r*1000, E*0.001, P*0.001`.

    1.35 GPa = 1.35e9 Pa → ×0.001 → 1.35e6 = 원본의 `0.135e7`.  (일치 확인됨)
    """
    return e_gpa * 1e9 * 0.001


def _tag(knob, val):
    return f'{knob}{str(val).replace(".", "p")}'


def plan():
    """만들 런 목록.  (name, 설명, 파라미터 dict)

    ⚠⚠ 첫 두 런이 **2×2 대조**다 (2026-08-25 추가).  윈도우 재설치로 옛 LIGGGHTS 바이너리가
      사라졌을 수 있는데, 그러면 기준선이 옛 기록과 안 맞아도 그 원인이
      **① type 리팩터** 인지 **② 다른 빌드** 인지 가를 수 없다.  ⇒ 원본(1-type)을 **새 빌드로
      같이 돌린다**:
        · `orig_1type`(새 빌드) vs 옛 기록      → **빌드 효과**
        · `base`(2-type)  vs `orig_1type`      → **type 리팩터 효과**
      둘 다 0 이어야 OAT 결과를 믿을 수 있다.  하나만 돌리면 두 원인이 섞인다.
    """
    runs = [('orig_1type', '⚠ 빌드 대조 — 원본 1-type 그대로 (출력 경로만 변경)', None),
            ('base', '기준선 — 생산값, 2-type (⚠ type 리팩터 음성 대조)', dict(PROD))]
    for knob in OAT_KNOBS:
        for lv in OAT_LEVELS:
            if abs(PROD[knob] - lv) < 1e-12:
                continue                       # 생산값과 같으면 기준선과 중복
            p = dict(PROD)
            p[knob] = lv
            runs.append((f'oat_{_tag(knob, lv)}', f'표A · {knob} = {lv}', p))
    for e in E_SWEEP_GPA:
        if abs(e - PROD['E_GPa']) < 1e-12:
            continue                           # 1.35 는 기준선이 겸한다
        p = dict(PROD)
        p['E_GPa'] = e
        runs.append((f'esweep_E{str(e).replace(".", "p")}', f'표B · E = {e} GPa', p))
    return runs


#: 원본의 물성 블록 (1-type) → 2-type 으로 바꾸는 치환표.
#:  ⚠ 벽(type 2)은 **입자와 같은 값**을 받는다 — 원본이 1-type 이라 벽이 입자 물성을
#:    그대로 썼기 때문이다.  값을 바꾸면 기준선이 원본을 재현하지 못한다.
def _material_block(p):
    E = e_scaled(p['E_GPa'])
    mu_pp, mu_pw = p['mu_pp'], p['mu_pw']
    cor, roll = p['cor'], p['roll']
    #  peratomtypepair 2 → 행우선 2×2: (1,1) (1,2) (2,1) (2,2)
    #  (2,2) = 벽-벽 은 쓰이지 않지만 LIGGGHTS 가 값을 요구한다.
    return f"""#  ⚠ type 1 = SE 입자 · type 2 = **벽 전용**(입자 없음).
#     원본은 1-type 이라 벽 마찰이 입자 마찰에 묶여 있었다 → mu_pw 를 못 흔든다.
#     벽 물성은 입자와 **같은 값**으로 둔다 (원본 거동 보존).  마찰만 mu_pw 로 분리.
fix m1 all property/global youngsModulus peratomtype {E:.6g} {E:.6g}
fix m2 all property/global poissonsRatio peratomtype 0.30 0.30
fix m3 all property/global coefficientRestitution peratomtypepair 2 {cor} {cor} {cor} {cor}
fix m4 all property/global coefficientFriction peratomtypepair 2 {mu_pp} {mu_pw} {mu_pw} {mu_pp}
fix m5 all property/global coefficientRollingFriction peratomtypepair 2 {roll} {roll} {roll} {roll}
fix m6 all property/global coefficientMaxElasticStiffness peratomtypepair 2 5.0 5.0 5.0 5.0
fix m7 all property/global coefficientAdhesionStiffness peratomtypepair 2 1.0e6 1.0e6 1.0e6 1.0e6
fix m8 all property/global coefficientPlasticityDepth peratomtypepair 2 0.005 0.005 0.005 0.005
fix m9 all property/global characteristicVelocity scalar 2.0"""


def render(name, desc, p, base_text=None):
    """원본 입력을 읽어 이 런의 입력으로 바꾼다.

    ⚠ **최소 치환만 한다** — 물리·수치 설정(타임스텝·삽입 시드·상 순서·정지 판정)은
      원본 그대로 둔다.  건드리면 기준선이 원본을 재현할 수 없다.
    """
    if base_text is None:
        with open(BASE, encoding='utf-8') as f:
            base_text = f.read()
    t = base_text

    #  ★ p is None = **빌드 대조**.  원본을 한 글자도 안 고치고 **출력 경로만** 바꾼다.
    #    (type 도 물성도 그대로 1-type — 그래야 옛 기록과 like-for-like 비교가 된다)
    if p is None:
        t = t.replace('SE_heckel_300', f'oat_{name}')
        hdr0 = (f'# ============================================================\n'
                f'# {name}: {desc}\n'
                f'#\n'
                f'# ⚠⚠ **빌드 대조다.**  원본 heckel/input_SE_heckel_300.liggghts 와\n'
                f'#    **출력 경로 말고는 한 글자도 다르지 않다** (1-type 그대로).\n'
                f'#    윈도우 재설치로 옛 LIGGGHTS 바이너리가 사라졌으므로, 기준선이 옛 기록과\n'
                f'#    안 맞을 때 그 원인이 **type 리팩터**인지 **다른 빌드**인지 가르려면\n'
                f'#    이 런이 있어야 한다.  이것 없이 base 만 돌리면 두 원인이 섞인다.\n'
                f'# ============================================================\n')
        return re.sub(r'^# =+\n(?:#.*\n)*?# =+\n', hdr0, t, count=1)

    #  ① 물성 블록 통째 교체 (fix m1 ~ fix m9)
    blk = re.search(r'fix m1 all property/global youngsModulus.*?fix m9 all property/global'
                    r' characteristicVelocity scalar 2\.0', t, re.S)
    if not blk:
        raise ValueError('원본에서 물성 블록(m1~m9)을 못 찾았다 — 원본이 바뀌었나?')
    t = t[:blk.start()] + _material_block(p) + t[blk.end():]

    #  ② 박스를 2 타입으로
    t = t.replace('create_box      1 reg_box', 'create_box      2 reg_box')

    #  ③ 벽을 type 2 로 (바닥 primitive · 상단 mesh)
    t = t.replace('primitive type 1 zplane 0.0', 'primitive type 2 zplane 0.0')
    t = t.replace('file plate_SE_heckel_300.stl type 1',
                  'file plate_SE_heckel_300.stl type 2')

    #  ④ 출력 경로·이름을 런별로 (겹쳐 쓰지 않게)
    t = t.replace('SE_heckel_300', f'oat_{name}')

    #  ⑤ 머리말 — **무엇이 왜 바뀌었는지 파일 자신이 말하게**
    hdr = (f'# ============================================================\n'
           f'# {name}: {desc}\n'
           f'#   mu_pp={p["mu_pp"]} · mu_pw={p["mu_pw"]} · COR={p["cor"]} · '
           f'roll={p["roll"]} · E={p["E_GPa"]} GPa (scaled {e_scaled(p["E_GPa"]):.6g})\n'
           f'#\n'
           f'# ⚠ 생성물이다 — 손으로 고치지 말고 scripts/gen_dem_oat_sweep.py 를 고칠 것.\n'
           f'# ⚠ 원본 heckel/input_SE_heckel_300.liggghts 대비 **구조 변경 1건**:\n'
           f'#    atom type 1 → 2 (벽을 type 2 로 분리해야 mu_pw 를 독립으로 흔든다).\n'
           f'#    그래서 `base` 런은 **음성 대조**다 — 원본 porosity 를 재현해야 한다.\n'
           f'# ============================================================\n')
    t = re.sub(r'^# =+\n(?:#.*\n)*?# =+\n', hdr, t, count=1)
    return t


RUNNER = """#!/usr/bin/env bash
# pure-SE OAT 민감도 + E 스윕 — 로컬(WSL/kgy) 실행용.  ⚠ 클라우드 보드에서 돌리지 말 것.
#
#   bash dem_scripts/oat_sweep/run_all.sh                     # 순차
#   LIGGGHTS=~/src/LIGGGHTS-PUBLIC/src/lmp_auto NP=8 bash …    # mpirun -np 8
#   MPI=no bash …                                             # serial 빌드일 때
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
LIGGGHTS="${LIGGGHTS:-liggghts}"
NP="${NP:-1}"
MPI="${MPI:-auto}"          # auto | yes | no
command -v "$LIGGGHTS" >/dev/null 2>&1 || {
  echo "⛔ '$LIGGGHTS' 를 못 찾았다.  LIGGGHTS=<실행파일> 로 지정하거나 PATH 에 넣을 것."
  exit 1; }

#  ⚠⚠ 2026-08-25 실측 — MPI 빌드를 `mpirun` **없이** 직접 실행하면 `MPI_Init` 에서 **무한 대기**한다.
#    증상: 배너도 안 나오고 · CPU 0 % · RSS 12 MB 고정 · `/proc/<pid>/wchan` = `wait_woken` ·
#    fd 에 socket/eventpoll/eventfd (= OpenMPI ORTE 기계).  39분을 그렇게 서 있었다.
#    ⇒ `mpirun` 이 있으면 **np=1 이라도 반드시 거친다**.  옛 판은 NP>1 일 때만 썼다.
USE_MPI=0
case "$MPI" in
  yes) USE_MPI=1;;
  no)  USE_MPI=0;;
  *)   command -v mpirun >/dev/null 2>&1 && USE_MPI=1;;
esac
[ "$USE_MPI" = 1 ] && echo "[실행] mpirun -np $NP" || echo "[실행] 직접 (mpirun 없음/MPI=no)"
[ "$USE_MPI" = 0 ] && [ "$NP" -gt 1 ] && { echo "⛔ NP=$NP 인데 mpirun 이 없다"; exit 1; }

#  ⚠ 로그가 파일로 나가면 stdio 가 **4 KB 블록 버퍼**를 써서, 살아 있어도 로그가 비어 보인다
#    (님이 실제로 그것 때문에 죽은 줄 알았다).  줄 단위로 흘려 `tail -f` 가 되게 한다.
STDBUF=""
command -v stdbuf >/dev/null 2>&1 && STDBUF="stdbuf -oL -eL"

#  ★★ 대조 **두 개**를 먼저, 정해진 순서로 돌린다 (2×2):
#     ① orig_1type (새 빌드, 원본 1-type) vs 옛 기록  → **빌드 효과**
#     ② base (2-type)         vs orig_1type          → **type 리팩터 효과**
#     둘 다 0 이어야 OAT 를 믿는다.  하나만 돌리면 두 원인이 섞인다.
CONTROLS=("in.orig_1type.liggghts" "in.base.liggghts")
for c in "${CONTROLS[@]}"; do
  [ -f "$c" ] || { echo "⛔ $c 가 없다 — 생성기를 다시 돌릴 것"; exit 1; }
done

run_one() {
  local f="$1"; local n="${f#in.}"; n="${n%.liggghts}"
  echo "── $n ─────────────────────────────"
  local t0=$SECONDS
  echo "   진행 보기:  tail -f $(pwd)/log.$n.txt"
  if [ "$USE_MPI" = 1 ]; then
    $STDBUF mpirun -np "$NP" "$LIGGGHTS" -in "$f" > "log.$n.txt" 2>&1
  else
    $STDBUF "$LIGGGHTS" -in "$f" > "log.$n.txt" 2>&1
  fi
  local rc=$?
  echo "   exit=$rc · $((SECONDS-t0))s · log.$n.txt"
  #  ★ exit 0 이어도 **아무것도 안 만들었으면 실패다** (MPI 행처럼 조용히 죽는 경우)
  if [ $rc -eq 0 ] && [ ! -d "post_oat_$n" ]; then
    echo "   ⛔ exit=0 인데 post_oat_$n/ 이 없다 — 실행이 시작조차 못 했을 수 있다."
    echo "      로그 크기: $(stat -c %s "log.$n.txt" 2>/dev/null || echo 0) 바이트"
    rc=1
  fi
  [ $rc -ne 0 ] && { echo "   ⛔ 실패 — 로그 마지막:"; tail -12 "log.$n.txt"; }
  return $rc
}

for c in "${CONTROLS[@]}"; do
  run_one "$c" || { echo; echo "⛔⛔ 대조 런이 실패했다.  나머지를 돌리지 않는다."; exit 1; }
done
echo
echo "★★ 대조 2건 완료.  **계속하기 전에 두 비교를 확인할 것**:"
echo "   ① post_oat_orig_1type/ 최종 porosity  vs  옛 기록(docs/data/heckel_pure_se_dem.csv)"
echo "      → 다르면 **빌드가 다르다**.  그 차이를 먼저 기록하고, OAT 는 새 빌드 안에서만 해석."
echo "   ② post_oat_base/ (2-type)  vs  post_oat_orig_1type/ (1-type)"
echo "      → 다르면 **type 리팩터가 무언가를 바꿨다**.  OAT 결과는 무효다."
echo "   ⚠ ①만 보고 ②를 건너뛰면 두 원인이 섞인다.  둘 다 볼 것."
echo
for f in in.*.liggghts; do
  skip=0
  for c in "${CONTROLS[@]}"; do [ "$f" = "$c" ] && skip=1; done
  [ "$skip" = 1 ] && continue
  run_one "$f"
done
echo "완료."
"""


def write_all(outdir=None):
    outdir = outdir or OUTDIR
    os.makedirs(outdir, exist_ok=True)
    with open(BASE, encoding='utf-8') as f:
        base_text = f.read()
    made = []
    for name, desc, p in plan():
        path = os.path.join(outdir, f'in.{name}.liggghts')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(render(name, desc, p, base_text))
        made.append(path)
    rp = os.path.join(outdir, 'run_all.sh')
    with open(rp, 'w', encoding='utf-8') as f:
        f.write(RUNNER)
    os.chmod(rp, 0o755)
    #  매니페스트 — 무엇을 왜 돌렸는지 나중에 알 수 있게
    mp = os.path.join(outdir, 'manifest.csv')
    with open(mp, 'w', encoding='utf-8') as f:
        f.write('run,table,mu_pp,mu_pw,cor,roll,E_GPa,n_atom_types,desc\n')
        for name, desc, p in plan():
            tbl = ('A' if name.startswith('oat_') else
                   'B' if name.startswith('esweep') else 'control')
            if p is None:                       # 빌드 대조 — 원본 값 그대로, 1-type
                f.write(f'{name},{tbl},{PROD["mu_pp"]},{PROD["mu_pw"]},{PROD["cor"]},'
                        f'{PROD["roll"]},{PROD["E_GPa"]},1,"{desc}"\n')
            else:
                f.write(f'{name},{tbl},{p["mu_pp"]},{p["mu_pw"]},{p["cor"]},{p["roll"]},'
                        f'{p["E_GPa"]},2,"{desc}"\n')
    return made, rp, mp


def _selftest():
    n = [0, 0]

    def chk(m, ok):
        n[1] += 1
        n[0] += bool(ok)
        print(f'  {"PASS" if ok else "FAIL"}  {m}')

    chk('① 원본 입력이 있다', os.path.exists(BASE))
    chk(f'② E 스케일이 원본과 일치 (1.35 GPa → {e_scaled(1.35):.6g} = 0.135e7)',
        abs(e_scaled(1.35) - 1.35e6) < 1.0)
    runs = plan()
    names = [r[0] for r in runs]
    #  기준선 1 + 표A 9(3노브×3수준, 생산값과 겹치는 수준 없음) + 표B 2(1.35 는 기준선이 겸함)
    chk(f'③ 런 목록 {len(runs)}개 = 대조2 + 9 + 2', len(runs) == 13)
    chk('④ ★★ 대조 **둘**이 맨 앞, 빌드 대조가 먼저',
        names[0] == 'orig_1type' and names[1] == 'base')
    chk('⑤ 생산값과 같은 수준은 중복 생성 안 함 (mu 0.5·E 1.35 없음)',
        'oat_mu_pp0p5' not in names and 'esweep_E1p35' not in names)
    a = [x for x in names if x.startswith('oat_')]
    b = [x for x in names if x.startswith('esweep')]
    chk(f'⑥ 표A {len(a)}런 · 표B {len(b)}런', len(a) == 9 and len(b) == 2)

    with open(BASE, encoding='utf-8') as f:
        bt = f.read()
    t = render('base', 'x', dict(PROD), bt)
    chk('⑦ ★ 박스가 2 타입으로', 'create_box      2 reg_box' in t)
    chk('⑧ ★ 벽이 type 2 로 (바닥·상단 둘 다)',
        'primitive type 2 zplane' in t and '.stl type 2' in t)
    chk('⑨ ★ peratomtypepair 가 2×2 (값 4개)',
        re.search(r'coefficientFriction peratomtypepair 2 0\.5 0\.5 0\.5 0\.5', t) is not None)
    chk('⑩ ★ peratomtype 이 값 2개', 'poissonsRatio peratomtype 0.30 0.30' in t)
    #  ★★ 최소 치환 — 물리·수치 설정을 건드리지 않았나
    for keep in ('timestep        ${{dt}}', 'seed 78049', 'variable target_press equal 0.300',
                 'volumefraction_region 0.281', 'pair_style      gran model hooke/hysteresis'):
        chk(f'⑪ 원본 설정 보존: `{keep[:38]}`', keep in t)
    chk('⑫ ★ 출력 경로가 런별로 분리 (원본 이름 안 남음)',
        'SE_heckel_300' not in t.replace('input_SE_heckel_300.liggghts', '')
        .replace('plate_SE_heckel_300.stl', 'X'))
    #  mu_pw 가 실제로 비대각에만 들어가나
    t2 = render('x', 'x', {**PROD, 'mu_pw': 0.2}, bt)
    chk('⑬ ★★ mu_pw 는 **비대각**(1,2)(2,1)에만 — 대각은 mu_pp 유지',
        'coefficientFriction peratomtypepair 2 0.5 0.2 0.2 0.5' in t2)
    t3 = render('x', 'x', {**PROD, 'mu_pp': 0.2}, bt)
    chk('⑭ ★ mu_pp 는 대각(1,1)(2,2)에만',
        'coefficientFriction peratomtypepair 2 0.2 0.5 0.5 0.2' in t3)
    t4 = render('x', 'x', {**PROD, 'E_GPa': 24.0}, bt)
    chk(f'⑮ E=24 GPa → 스케일 {e_scaled(24):.6g}', 'peratomtype 2.4e+07 2.4e+07' in t4)
    #  ★ 머리말이 구조 변경을 **경고**하는가 (조용히 바꾸지 않는다)
    chk('⑯ ★★ 머리말이 type 리팩터와 음성 대조를 경고한다',
        'atom type 1 → 2' in t and '음성 대조' in t)
    #  ★ 러너가 기준선을 먼저 돌리고, 실패하면 멈추는가
    chk('⑰ ★★ 러너가 대조 먼저 + 실패 시 중단',
        'in.base.liggghts' in RUNNER and '나머지를 돌리지 않는다' in RUNNER)
    #  ★★ 2026-08-25 실측 결함 두 개 — 사용자가 39분을 멈춘 프로세스 앞에서 보냈다
    chk('㉓ ★★ mpirun 이 있으면 **np=1 이라도 거친다** (MPI_Init 행 방지)',
        'USE_MPI' in RUNNER and 'command -v mpirun' in RUNNER
        and 'MPI_Init' in RUNNER)
    chk('㉔ ★★ 로그를 줄 단위로 흘린다 (`tail -f` 가 되게)',
        'stdbuf -oL' in RUNNER and '4 KB 블록 버퍼' in RUNNER)
    chk('㉕ ★★ exit=0 이어도 **산출물이 없으면 실패**로 잡는다',
        'exit=0 인데 post_oat_' in RUNNER and 'rc=1' in RUNNER)
    chk('㉖ NP>1 인데 mpirun 이 없으면 **조용히 직렬로 떨어지지 않는다**',
        'NP=$NP 인데 mpirun 이 없다' in RUNNER)
    #  ★★ 빌드 대조 — 출력 경로 말고는 원본과 **한 글자도 달라선 안 된다**
    o = render('orig_1type', 'x', None, bt)
    o_body = re.sub(r'^# =+\n(?:#.*\n)*?# =+\n', '', o, count=1)
    b_body = re.sub(r'^# =+\n(?:#.*\n)*?# =+\n', '', bt, count=1)
    chk('⑲ ★★ 빌드 대조는 출력 경로만 다르다 (본문 완전 동일)',
        o_body == b_body.replace('SE_heckel_300', 'oat_orig_1type'))
    chk('⑳ ★ 빌드 대조는 **1-type 그대로** (create_box 1, 물성 값 1개)',
        'create_box      1 reg_box' in o and 'poissonsRatio peratomtype 0.30\n' in o
        and 'primitive type 1 zplane' in o)
    chk('㉑ ★★ 머리말이 왜 이 런이 필요한지 말한다 (빌드 vs 리팩터 분리)',
        '빌드 대조' in o and 'type 리팩터' in o and '섞인다' in o)
    chk('㉒ ★ 러너가 대조 2건을 먼저, 실패 시 중단',
        'in.orig_1type.liggghts' in RUNNER and 'CONTROLS' in RUNNER
        and '나머지를 돌리지 않는다' in RUNNER)
    #  ⚠ 원본을 건드리지 않았나
    with open(BASE, encoding='utf-8') as f:
        chk('⑱ ★ 원본 파일은 **읽기만** 했다 (1-type 그대로)',
            'create_box      1 reg_box' in f.read())

    print(f'\ngen_dem_oat_sweep selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--outdir')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    runs = plan()
    print(f'생성할 런 **{len(runs)}개**  (원본: {os.path.relpath(BASE, _ROOT)})\n')
    print(f'  {"run":26s} {"표":4s} {"mu_pp":>6s} {"mu_pw":>6s} {"COR":>5s} {"E(GPa)":>7s}  types')
    for name, desc, p in runs:
        tbl = ('A' if name.startswith('oat_') else
               'B' if name.startswith('esweep') else '대조')
        q = PROD if p is None else p            # 빌드 대조는 생산값 그대로 (1-type)
        print(f'  {name:26s} {tbl:4s} {q["mu_pp"]:6.2f} {q["mu_pw"]:6.2f} '
              f'{q["cor"]:5.2f} {q["E_GPa"]:7.2f}  {"1-type" if p is None else "2-type"}')
    print('\n⚠ 구조 변경 1건: atom type 1 → 2 (벽을 분리해야 mu_pw 가 독립 노브가 된다).')
    print('  ⇒ `base` 런은 **음성 대조**다 — 원본(1-type) porosity 를 재현해야 한다.')
    print('  ⇒ 재현 못 하면 OAT 결과 전체가 무효다.  러너가 기준선을 먼저 돌리고 멈춘다.')
    if a.write:
        made, rp, mp = write_all(a.outdir)
        print(f'\n✓ 입력 {len(made)}개 + 러너 + 매니페스트 → '
              f'{os.path.relpath(os.path.dirname(rp), _ROOT)}/')
        print(f'  실행(로컬):  bash {os.path.relpath(rp, _ROOT)}')
    else:
        print('\n(--check 모드 — 쓰지 않았다.  실제로 쓰려면 --write)')
