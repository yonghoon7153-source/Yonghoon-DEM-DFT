#!/usr/bin/env python3
"""patch_dos_nscf.py — 이미 만들어진 `04_nscf_dos.in` 의 수렴 설정만 **제자리**에서 고친다.

⚠⚠ 왜 build_dft_inputs.py 를 다시 돌리면 안 되나
  생성기는 **원본(MP) 구조**로 입력을 다시 쓴다. 그런데 실제로 돌아간 04 는
  `splice_relaxed.py` 가 vc-relax 최종 좌표·셀을 스플라이스해 넣은 기하다.
  재생성하면 그 이완 기하가 날아가고 → tmp/ 의 scf 전하밀도와 **기하가 어긋난 채로**
  nscf 가 돈다. 조용히 틀린 DOS 가 나온다. 그래서 파일을 새로 쓰지 않고 **줄만 고친다.**

무엇을 고치나 (2026-08-07 licl 실패)
  `c_bands (1): too many bands are not converged` → MPI_ABORT.
  LiCl 은 갭 6.26 eV 이온결정이라 빈 전도대가 거의 자유전자꼴이고, nosym 으로 k 점이
  전 BZ 로 늘어난 상태에서 conv_thr 1e-8(ethr ~1e-9)을 제일 위 밴드까지 요구하면 안 닫힌다.
    ① conv_thr        1.0d-8 → 1.0d-6
    ② diago_david_ndim 없음  → 4      (Davidson 부분공간 확대)
    ③ nbnd            +50%             (제일 위 밴드가 제일 늦게 수렴 — 여유가 흡수한다)

  ★ 이 단계에서 문턱을 푸는 게 정당한 이유: 산출이 **DOS 모양**뿐이다. 갭은 03 단계
    fixed-occ 고유값이 정본이고, DOS 의 degauss 0.007 Ry(≈0.095 eV)가 이미 1e-6 Ry 보다
    다섯 자리 굵다. ⛔ 03 단계는 절대 안 푼다 — 그 값이 논문에 실린다.

  python3 tools/sei/patch_dos_nscf.py licl_mp-22905
  python3 tools/sei/patch_dos_nscf.py --all --dry-run
"""
import argparse
import glob
import os
import re
import sys

WORK = os.environ.get("WORK", "/data/work/runs/sei_dft")


def patch(path, nbnd_scale, dry):
    src = open(path, encoding="utf-8", errors="ignore").read()
    out, changed = src, []

    # ⚠ **멱등해야 한다.** 처음 만들 때 nbnd 를 배율로 올리게 짰더니 두 번 돌리면
    #   14 → 25 → 41 로 계속 불어났다(2026-08-07 스모크 테스트에서 잡음). 밴드가 늘면
    #   조용히 느려지기만 해서 눈치채기도 어렵다. `diago_david_ndim` 유무를 표식으로 쓴다
    #   — 이 키는 우리가 넣기 전엔 없고, 넣고 나면 항상 있다.
    if "diago_david_ndim" in src:
        return src, []          # 이미 적용됨 — 아무것도 안 한다

    # ① conv_thr
    m = re.search(r"^(\s*conv_thr\s*=\s*)(\S+)\s*$", out, re.M)
    if m and "1.0d-6" not in m.group(2):
        out = out[:m.start()] + m.group(1) + "1.0d-6" + out[m.end():]
        changed.append(f"conv_thr {m.group(2)} → 1.0d-6")

    # ② diago_david_ndim — &ELECTRONS 안에만 넣는다
    if "diago_david_ndim" not in out:
        m = re.search(r"^(&ELECTRONS\s*)$", out, re.M)
        if not m:
            return None, ["⛔ &ELECTRONS 를 못 찾았다"]
        out = out[:m.end()] + "\n    diago_david_ndim = 4" + out[m.end():]
        changed.append("diago_david_ndim = 4 추가")

    # ③ nbnd
    m = re.search(r"^(\s*nbnd\s*=\s*)(\d+)\s*$", out, re.M)
    if m:
        old = int(m.group(2)); new = int(old * nbnd_scale) + 4
        if new > old:
            out = out[:m.start()] + m.group(1) + str(new) + out[m.end():]
            changed.append(f"nbnd {old} → {new}")
    else:
        changed.append("⚠ nbnd 줄이 없다 — 손대지 않음")

    if changed and not dry:
        open(path + ".bak", "w", encoding="utf-8").write(src)   # 되돌릴 수 있게
        open(path, "w", encoding="utf-8").write(out)
    return out, changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tags", nargs="*", help="비우면 --all 필요")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--work", default=WORK)
    ap.add_argument("--nbnd_scale", type=float, default=1.5)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    tags = a.tags or (sorted(os.path.basename(d) for d in glob.glob(os.path.join(a.work, "*"))
                             if os.path.isdir(d)) if a.all else [])
    if not tags:
        sys.exit("쓰기: python3 tools/sei/patch_dos_nscf.py licl_mp-22905   (또는 --all)")

    n = 0
    for t in tags:
        # 부분 문자열로도 찾게 (licl → licl_mp-22905)
        cands = [d for d in glob.glob(os.path.join(a.work, "*")) if t in os.path.basename(d)]
        if not cands:
            print(f"  ⛔ {t}: 폴더 없음"); continue
        for d in cands:
            p = os.path.join(d, "04_nscf_dos.in")
            if not os.path.isfile(p):
                print(f"  ⛔ {os.path.basename(d)}: 04_nscf_dos.in 없음"); continue
            _, ch = patch(p, a.nbnd_scale, a.dry_run)
            tail = " · ".join(ch) if ch else "이미 적용됨"
            print(f"  {'(연습)' if a.dry_run else '✓'} {os.path.basename(d):26s} {tail}")
            n += bool(ch)
    if not a.dry_run and n:
        print(f"\n{n}개 고침 (.bak 백업 남김). 기하는 안 건드렸다 — "
              f"vc-relax 스플라이스 그대로다.")
        print("다시:  TAG=<tag> bash tools/sei/redo_stages.sh 04 05 06 && "
              "bash tools/sei/run_sei_dft.sh <tag>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
