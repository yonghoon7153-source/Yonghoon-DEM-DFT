#!/usr/bin/env python3
"""sync_magnetization.py — scf 가 **실제로 수렴한** 총 자기모멘트를 fixed-occ nscf 에 옮긴다.

왜 필요한가 (2026-08-07 실측)
  Nd 계를 스핀분극으로 다시 걸었더니 nd2o3 갭이 **−6.460 eV** 로 나왔다
  (VBM 16.159 > CBM 9.700). 이건 "밴드가 겹쳤다"가 아니라 **읽기가 깨진 것**이다.

  ⚠⚠ **이 가설은 실측으로 반증됐다 (2026-08-07 같은 날 저녁).** nd2o3 의 02_scf 수렴
    모멘트는 6.00 μB 이고 03_nscf_gap.in 의 tot_magnetization 도 6 이었다 — **둘이 이미
    맞았다.** 그러니 −6.460 eV 의 원인은 모멘트 불일치가 아니다.
    이 도구는 그래도 남긴다: 스핀분극 계에서 02 와 03 의 모멘트가 어긋날 수 있다는 건
    실재하는 위험이고(가정값을 강제하는 구조였으니), 이 도구가 그걸 막는다. 다만
    **Nd 갭 문제의 해결책은 아니었다.** 아래 원인 서술은 "일어날 수 있는 일" 로 읽을 것.

  원인 (가설 — nd2o3 에서는 해당 없음이 확인됨): 단계별로 자기모멘트를 다르게 다뤘다.
    · 02_scf   : occupations='smearing' → 총 모멘트를 **계가 알아서** 찾는다
    · 03_nscf  : occupations='fixed'  → QE 가 tot_magnetization 을 요구하므로
                 생성기가 `3 × n_Nd` (Nd³⁺ = 4f³ 가정)를 **강제**했다
  scf 가 다른 값으로 수렴했으면 nscf 는 **전하밀도와 어긋난 점유수**로 밴드를 채운다.
  그러면 ↑채널의 점유 최상단이 ↓채널의 비점유 최하단보다 위로 올라갈 수 있고,
  VBM > CBM 이라는 물리적으로 불가능한 조합이 나온다. 정확히 그게 관측된 것이다.

  → 가정을 버리고 **scf 출력에서 읽어** 03 에 넣는다. 정수로 반올림해야 fixed 가 성립하고,
    반올림 오차가 크면(±0.2 μB 초과) 그건 계가 정수 모멘트로 안 간다는 뜻이라 경고한다.

  python3 tools/sei/sync_magnetization.py /data/work/runs/sei_dft/nd2o3_mp-2763
  python3 tools/sei/sync_magnetization.py --all
"""
import argparse
import glob
import os
import re
import sys

WORK = os.environ.get("WORK", "/data/work/runs/sei_dft")
# QE 가 SCF 마다 찍는 줄:  total magnetization       =     5.98 Bohr mag/cell
_MAG = re.compile(r"total magnetization\s*=\s*(-?[\d.]+)\s*Bohr mag/cell")


def converged_mag(scf_out):
    """마지막 SCF 스텝의 총 모멘트. 중간 스텝은 흔들리므로 **끝값**만 쓴다."""
    try:
        t = open(scf_out, errors="ignore").read()
    except OSError:
        return None
    if "JOB DONE" not in t:
        return None                      # 안 끝난 scf 의 중간값을 옮기면 더 나쁘다
    vals = _MAG.findall(t)
    return float(vals[-1]) if vals else None


def sync(d, dry=False):
    scf = os.path.join(d, "02_scf.out")
    tgt = os.path.join(d, "03_nscf_gap.in")
    tag = os.path.basename(d)
    if not os.path.isfile(tgt):
        return f"{tag:26s} ⏭ 03_nscf_gap.in 없음"
    src = open(tgt, encoding="utf-8", errors="ignore").read()
    if "tot_magnetization" not in src:
        return f"{tag:26s} ⏭ 스핀분극 계가 아니다"
    m = converged_mag(scf)
    if m is None:
        return f"{tag:26s} ⛔ 02_scf.out 에서 수렴 모멘트를 못 읽었다 (scf 완주 확인)"
    want = int(round(m))
    cur = re.search(r"tot_magnetization\s*=\s*(-?[\d.]+)", src)
    cur_v = float(cur.group(1)) if cur else None
    off = abs(m - want)
    note = ""
    if off > 0.2:
        note = (f"  ⚠ 수렴값 {m:.3f} 이 정수에서 {off:.3f} 벗어났다 — 계가 정수 모멘트로 "
                f"가지 않는다는 뜻이다. fixed-occ 갭 자체가 의심스러우니 결과를 그대로 믿지 말 것")
    if cur_v is not None and abs(cur_v - want) < 1e-6:
        return f"{tag:26s} ✓ 이미 맞다 (scf {m:.3f} → tot_mag {want}){note}"
    out = re.sub(r"(tot_magnetization\s*=\s*)(-?[\d.]+)", rf"\g<1>{want}", src, count=1)
    if not dry:
        open(tgt + ".bak", "w", encoding="utf-8").write(src)
        open(tgt, "w", encoding="utf-8").write(out)
    return (f"{tag:26s} {'(연습)' if dry else '✓'} tot_magnetization {cur_v} → {want} "
            f"(scf 수렴 {m:.3f} μB){note}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--work", default=WORK)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    dirs = a.dirs or (sorted(x for x in glob.glob(os.path.join(a.work, "*"))
                             if os.path.isdir(x)) if a.all else [])
    if not dirs:
        sys.exit("쓰기: python3 tools/sei/sync_magnetization.py <작업폴더>   (또는 --all)")
    for d in dirs:
        print("  " + sync(d, a.dry_run))
    if not a.dry_run:
        print("\n바뀐 폴더는 03 부터 다시 돌린다:")
        print("  TAG=<tag> bash tools/sei/redo_stages.sh 03 04 05 06")
    return 0


if __name__ == "__main__":
    sys.exit(main())
