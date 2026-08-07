#!/usr/bin/env python3
"""collect_results.py — gabia 작업폴더의 SEI 결과를 **repo 로 회수**한다.

왜 필요한가
  계산은 `/data/work/runs/sei_dft/` 에서 돈다 — repo 밖이다. 컨테이너/서버가 죽으면
  gap.json 도 DOS 곡선도 같이 사라진다. 그림은 나중에 그리므로 **원자료를 지금 repo 에
  넣어 둬야** 한다(사용자 요청 문구: "repo에 저장하게 DOS, pDOS 해서").

무엇을 만드나
  db/properties/sei_electronic.json        갭 정본(9종) + 출처 + 경고
  db/properties/sei_dos/<tag>_dos.csv      total DOS — Origin-ready
  db/properties/sei_dos/<tag>_pdos.csv     원소·궤도별 PDOS 합산 — Origin-ready

⚠ 갭은 **fixed-occ nscf 고유값**이 정본이다(CLAUDE.md). 여기 담는 DOS 는 그림용이지
  갭 판독용이 아니다 — CSV 헤더에도 그렇게 박아 둔다.
⚠ Nd 계 3종(4f 를 원자가에 넣은 PBE)은 갭이 닫힌다. `artifact_4f: true` 로 표시하고
  `db/properties/electronic.json` 에는 **올리지 않는다**.

  # gabia 에서 (repo 루트에서)
  python3 tools/sei/collect_results.py
  python3 tools/sei/collect_results.py --work /data/work/runs/sei_dft
"""
import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime

OUT_JSON = "db/properties/sei_electronic.json"
OUT_DIR = "db/properties/sei_dos"
# 4f 를 원자가에 넣은 PBE 는 4f 준위를 E_F 근처에 놓아 갭을 닫는다 — 물리가 아니라 방법의 실패.
ND_TAGS = ("nd2o3", "nd2s3", "lindo2")
# projwfc 파일명:  <prefix>.pdos_atm#12(Li)_wfc#1(s)
PDOS_RE = re.compile(r"\.pdos_atm#(\d+)\(([A-Za-z]+)\)_wfc#(\d+)\(([spdf])\)")


def read_cols(path, ncol):
    """QE 의 .dos/.pdos 는 '# ...' 주석 한 줄 + 공백구분 숫자다."""
    xs = []
    with open(path, errors="ignore") as f:
        for ln in f:
            if ln.lstrip().startswith("#"):
                continue
            p = ln.split()
            if len(p) < ncol:
                continue
            try:
                xs.append([float(v) for v in p[:ncol]])
            except ValueError:
                continue
    return xs


def write_csv(path, header, rows, note):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# " + note + "\n")
        f.write(",".join(header) + "\n")
        for r in rows:
            f.write(",".join(f"{v:.6g}" for v in r) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=os.environ.get("WORK", "/data/work/runs/sei_dft"))
    a = ap.parse_args()

    tags = sorted(os.path.basename(d) for d in glob.glob(os.path.join(a.work, "*"))
                  if os.path.isdir(d))
    if not tags:
        sys.exit(f"⛔ {a.work} 에 작업 폴더가 없다")

    res, made = {}, []
    for t in tags:
        d = os.path.join(a.work, t)
        gj = os.path.join(d, "gap.json")
        if not os.path.isfile(gj):
            print(f"  ⏭ {t:26s} gap.json 없음 — 건너뜀")
            continue
        g = json.load(open(gj))
        nd = any(k in t.lower() for k in ND_TAGS)
        g["artifact_4f"] = nd
        if nd:
            g["do_not_cite"] = ("Nd 4f in valence (PBE) closes the gap — method artifact, "
                                "not physics. Cite MP frozen-4f values instead.")
        g["files"] = {}

        # ── total DOS (dos.x): E, dos, int_dos ──────────────────────────────
        dosf = glob.glob(os.path.join(d, "*.dos"))
        if dosf:
            rows = read_cols(dosf[0], 3)
            if rows:
                p = os.path.join(OUT_DIR, f"{t}_dos.csv")
                write_csv(p, ["E_eV", "E_minus_VBM_eV", "DOS_states_per_eV",
                              "integrated_DOS_states"],
                          [[r[0], r[0] - g["vbm"], r[1], r[2]] for r in rows],
                          f"{t} total DOS (QE dos.x, degauss 0.007 Ry). "
                          f"VBM {g['vbm']:.3f} / CBM {g['cbm']:.3f} / gap {g['gap']:.3f} eV "
                          f"from fixed-occ nscf eigenvalues. "
                          f"DO NOT read the gap off this curve (smearing underestimates ~0.3 eV).")
                g["files"]["dos_csv"] = p; made.append(p)

        # ── PDOS (projwfc): 원소·궤도로 합산 ────────────────────────────────
        cols, egrid = {}, None
        for f in sorted(glob.glob(os.path.join(d, "*.pdos_atm#*"))):
            m = PDOS_RE.search(os.path.basename(f))
            if not m:
                continue
            el, l = m.group(2), m.group(4)
            rows = read_cols(f, 3)
            if not rows:
                continue
            # 파일 형식: E, ldos, pdos... — ldos(2열)가 그 wfc 의 기여 합이다
            if egrid is None:
                egrid = [r[0] for r in rows]
            elif len(rows) != len(egrid):
                print(f"  ⚠ {t}: {os.path.basename(f)} 격자 길이 불일치 — 건너뜀")
                continue
            key = f"{el}_{l}"
            acc = cols.setdefault(key, [0.0] * len(egrid))
            for i, r in enumerate(rows):
                acc[i] += r[1]
        if egrid and cols:
            keys = sorted(cols)
            p = os.path.join(OUT_DIR, f"{t}_pdos.csv")
            write_csv(p, ["E_eV", "E_minus_VBM_eV"] + keys,
                      [[egrid[i], egrid[i] - g["vbm"]] + [cols[k][i] for k in keys]
                       for i in range(len(egrid))],
                      f"{t} PDOS summed by element+orbital (QE projwfc.x). "
                      f"Columns are states/eV. VBM {g['vbm']:.3f} eV. "
                      f"Gap is the fixed-occ nscf value ({g['gap']:.3f} eV), not a DOS threshold.")
            g["files"]["pdos_csv"] = p; made.append(p)
            g["pdos_channels"] = keys
        res[t] = g
        mark = "⚠4f" if nd else "  "
        print(f"  ✓ {t:26s} gap {g['gap']:7.3f} eV {mark}  "
              f"{'dos' if 'dos_csv' in g['files'] else '   '} "
              f"{'pdos' if 'pdos_csv' in g['files'] else ''}")

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    json.dump({
        "property": "sei_electronic",
        "method": ("QE PBE. vc-relax → scf → **fixed-occupation nscf** (갭은 이 단계 고유값) "
                   "→ nscf(DOS k-mesh) → dos.x → projwfc.x."),
        "gap_rule": ("갭은 fixed-occ nscf 의 VBM/CBM 고유값만 정본이다. "
                     "DOS 문턱 판독 금지 (~0.3 eV 과소 — CLAUDE.md 데이터 규율)."),
        "warning": ("PBE 갭은 넓은 갭 절연체에서 30–50% 과소평가된다. 실험값과 나란히 놓지 말고 "
                    "**순위**로만 쓸 것. Nd 계 3종은 4f 를 원자가에 넣은 탓에 갭이 닫히는데 "
                    "이는 방법의 실패지 금속성이 아니다(artifact_4f) — 인용은 MP frozen-4f 값으로."),
        "source_dir": a.work,
        "collected": datetime.now().strftime("%Y-%m-%d"),
        "results": res,
    }, open(OUT_JSON, "w"), ensure_ascii=False, indent=2)

    ok = [t for t, g in res.items() if not g["artifact_4f"]]
    print(f"\n→ {OUT_JSON}  ({len(res)}종 · 인용가능 {len(ok)}종)")
    print(f"→ {OUT_DIR}/  CSV {len(made)}개 (Origin-ready)")
    print("⚠ db/properties/electronic.json 등재는 **인용가능 6종만** — Nd 3종은 제외.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
