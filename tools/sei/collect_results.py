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
# 종결된 판정 — 회수기가 돌 때마다 다시 찍는다(기록이 재생성에 날아가지 않게).
ND_VERDICT = (
    "⛔ 폐기. 원인 확정(2026-08-07): 4f 를 원자가에 둔 PBE(+U) 의 SCF 해가 **금속**이다. "
    "Nd₂O₃ 의 02_scf.out 이 'highest occupied/lowest unoccupied' 가 아니라 "
    "'the Fermi energy is 11.4539 ev' 를 찍었고, 직전에 'failed to find Fermi energy: "
    "reverting to bisection'(E_F 에 극도로 평평한 상태 = 4f 다중항) 경고가 떴다. "
    "금속 해에 occupations='fixed' 를 강제한 결과가 VBM>CBM(−6.460 eV)이다 — 버그가 아니라 "
    "**정의되지 않은 양을 억지로 읽은 것**. LiNdO₂ 는 scf accuracy 가 5.7e-6 Ry 에서 평탄 정체, "
    "Nd₂S₃ 는 3.4e-4~6.3e-3 로 두 자릿수 출렁임 — iteration 을 더 줘도 안 닫히고 닫혀도 같은 "
    "금속 해다. U 를 키우면 갭이 열리지만 그건 답이 나올 때까지 U 를 고르는 것이라 방어가 안 된다. "
    "→ **Nd 상 갭은 MP frozen-4f 인용.** 상세: kb/projects/sei_products_2026_08_06.md")
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
    # ⚠⚠ 기존 JSON 을 **덮어쓰기 전에** 읽는다 (2026-08-07).
    #   이 회수기는 작업폴더를 훑어 JSON 을 새로 쓴다. 그런데 Nd 재계산 때 폴더를
    #   옮기고 다시 만드는 바람에 gap.json 이 없는 종이 생겼고, 그대로 돌리면
    #   **repo 의 판정 기록(status=rejected · do_not_cite)이 통째로 사라진다.**
    #   → 이번 실행에서 못 본 종은 지우지 않고 `not_in_this_run` 을 달아 보존한다.
    prev = {}
    if os.path.isfile(OUT_JSON):
        try:
            prev = json.load(open(OUT_JSON, encoding="utf-8")).get("results", {})
        except (OSError, ValueError):
            prev = {}
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

        # ⚠⚠ **곡선 파일은 실패한 실행에서도 살아남는다** (2026-08-07 licl).
        #   redo_stages.sh 는 `.out` 만 지우고 `.dos`/`.pdos_atm#*` 는 그대로 둔다.
        #   그래서 04 가 죽어 05·06 이 아예 안 돌았는데도 **옛 실행의 곡선**이 폴더에 남아
        #   회수기가 그걸 집어 갔다(실물: licl DOS 는 물리적으로는 멀쩡했지만 다른 04 설정
        #   에서 나온 것이었다). 이제 05·06 의 JOB DONE 을 확인하고, 아니면 stale 로 찍는다.
        def done(stem):
            p = os.path.join(d, stem + ".out")
            try:
                return "JOB DONE" in open(p, errors="ignore").read()
            except OSError:
                return False
        fresh = done("04_nscf_dos") and done("05_dos")
        g["dos_chain_complete"] = fresh
        if not fresh:
            g["dos_provenance_warning"] = (
                "05_dos.out 에 JOB DONE 이 없다 — 이 폴더의 .dos/.pdos 는 **이전 실행**의 "
                "잔존물일 수 있다(설정이 다른 04 에서 나왔을 수 있음). 갭은 03 단계 값이라 "
                "영향 없지만, **DOS/PDOS 곡선은 재실행 후 다시 회수할 것.**")

        # ⚠⚠ 2026-08-11 자체검토 P1-7 — electronic_class=metal/undetermined 상의
        #   gap.json 은 `{"gap": null, "verdict": "NOT_APPLICABLE(metal)"}` 라 vbm/cbm 이
        #   **없다**. 아래 CSV 들이 전부 `g["vbm"]` 로 에너지 영점을 잡으므로 KeyError 로
        #   죽는다 — 그것도 그 WORK 의 **모든** 상에 대한 결산이 통째로 날아간다.
        #   금속은 VBM 이 없으니 영점을 **E_F** 로 잡아야 맞다. 없으면 0 으로 두고 밝힌다.
        _zero = g.get("vbm")
        _zero_label = "VBM"
        if _zero is None:
            _zero = g.get("efermi", 0.0)
            _zero_label = "E_F" if g.get("efermi") is not None else "0 (no reference)"
        _gap_txt = (f"{g['gap']:.3f} eV" if g.get("gap") is not None
                    else f"NOT_APPLICABLE ({g.get('verdict', 'metal/undetermined')})")

        # ── total DOS (dos.x): E, dos, int_dos ──────────────────────────────
        dosf = glob.glob(os.path.join(d, "*.dos"))
        if dosf:
            rows = read_cols(dosf[0], 3)
            if rows:
                p = os.path.join(OUT_DIR, f"{t}_dos.csv")
                write_csv(p, ["E_eV", f"E_minus_{_zero_label.split()[0]}_eV",
                              "DOS_states_per_eV", "integrated_DOS_states"],
                          [[r[0], r[0] - _zero, r[1], r[2]] for r in rows],
                          f"{t} total DOS (QE dos.x, degauss 0.007 Ry). "
                          f"Energy zero = {_zero_label} ({_zero:.3f} eV). Gap: {_gap_txt}. "
                          + ("Gap from fixed-occ nscf eigenvalues. "
                             "DO NOT read the gap off this curve "
                             "(smearing underestimates ~0.3 eV)."
                             if g.get("gap") is not None else
                             "This phase has no gap by declaration "
                             "(db/properties/sei_electronic_class.json) — "
                             "the curve is for E_F occupancy inspection only."))
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
            write_csv(p, ["E_eV", f"E_minus_{_zero_label.split()[0]}_eV"] + keys,
                      [[egrid[i], egrid[i] - _zero] + [cols[k][i] for k in keys]
                       for i in range(len(egrid))],
                      f"{t} PDOS summed by element+orbital (QE projwfc.x). "
                      f"Columns are states/eV. Energy zero = {_zero_label} ({_zero:.3f} eV). "
                      f"Gap: {_gap_txt}"
                      + ("" if g.get("gap") is not None else
                         " — no gap by declaration; use this to check whether "
                         "states exist at E_F and what fraction is Nd_f."))
            g["files"]["pdos_csv"] = p; made.append(p)
            g["pdos_channels"] = keys
        # ★ Nd 판정은 종결됐다(2026-08-07) — 회수기가 매번 다시 찍어 기록이 안 날아가게 한다.
        if nd:
            g["status"] = "rejected"
            g["do_not_cite"] = ND_VERDICT
        res[t] = g
        mark = "⚠4f" if nd else "   "
        stale = "" if fresh or not g["files"] else "  ⚠ STALE 곡선 (05 미완주)"
        print(f"  ✓ {t:26s} gap "
              + (f"{g['gap']:7.3f} eV" if g.get("gap") is not None else "    N/A   ")
              + f" {mark} "
              f"{'dos' if 'dos_csv' in g['files'] else '   '} "
              f"{'pdos' if 'pdos_csv' in g['files'] else '    '}{stale}")

    # 이번 실행에서 못 본 종을 되살린다 (판정 기록 보존)
    kept = []
    for t, old in prev.items():
        if t in res:
            continue
        old["not_in_this_run"] = ("이번 회수에서 작업폴더에 gap.json 이 없었다 — "
                                  "옛 기록을 그대로 보존한다(지우지 않음).")
        res[t] = old
        kept.append(t)
    if kept:
        print(f"\n  ↺ 이번에 못 본 {len(kept)}종을 옛 기록으로 보존: {', '.join(kept)}")

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
        # ⚠⚠ 최상위 판정 키를 **매번 다시 쓴다** (2026-08-07 재발 수정).
        #   앞선 판에서 항목별 do_not_cite 만 되박고 이 키는 안 썼더니, 회수기를 돌릴
        #   때마다 최상위 판정문이 조용히 사라졌다 — 실측으로 확인(diff 에 `-` 만 남음).
        #   항목 보존(prev)은 `results` 안만 훑으므로 최상위 키를 못 살린다.
        "nd_verdict_2026_08_07": (
            "Nd 3종의 갭은 우리 QE 계산으로 **정의되지 않는다** — 못 낸 게 아니라 PBE+U 해가 "
            "금속이라 fixed-occ 갭이라는 양이 성립하지 않는다. 인용은 MP frozen-4f. "
            "상세: kb/projects/sei_products_2026_08_06.md §진단이 끝났다. "
            "Li 계 6종의 갭은 정상이며 그대로 인용 가능하다. "
            "재계산 경로는 tools/sei/nd_frozen4f.py --plan (frozen-4f PP 확보)."),
        "results": res,
    }, open(OUT_JSON, "w"), ensure_ascii=False, indent=2)

    ok = [t for t, g in res.items() if not g["artifact_4f"]]
    stale = [t for t, g in res.items() if g["files"] and not g["dos_chain_complete"]]
    print(f"\n→ {OUT_JSON}  ({len(res)}종 · 인용가능 {len(ok)}종)")
    print(f"→ {OUT_DIR}/  CSV {len(made)}개 (Origin-ready)")
    print("⚠ db/properties/electronic.json 등재는 **인용가능 6종만** — Nd 3종은 제외.")
    if stale:
        print(f"\n⚠⚠ 곡선 출처 불명 {len(stale)}종: {', '.join(stale)}")
        print("   05_dos 가 이번 실행에서 안 끝났다 — 폴더에 남아 있던 **옛 곡선**을 집었을 수 있다.")
        print("   갭은 03 단계 값이라 무관하지만, 그림용 DOS/PDOS 는 재실행 뒤 다시 회수할 것.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
