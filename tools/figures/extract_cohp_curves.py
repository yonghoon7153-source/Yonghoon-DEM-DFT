#!/usr/bin/env python3
"""extract_cohp_curves.py — COHPCAR.lobster → **컴팩트** 패널 곡선 CSV.

왜 이게 따로 필요한가
  COHPCAR.lobster 원본은 수십 MB(결합 수 × 에너지점)라 gzip+base64 로 회수할 수 없다.
  그림에 실제로 필요한 건 **원소쌍별로 합쳐진 곡선 몇 개**뿐이다. 그래서 원격에서
  이 스크립트로 줄여서 뽑고, CSV 만 회수한다.

  파서는 **복제하지 않는다** — tools/modelc_v3/plot_lobster_4panel.py 의
  parse_cohpcar/aggregate_bond_pair 를 그대로 import 한다(드리프트 방지).
  그 모듈이 matplotlib 를 최상단에서 import 하므로, 계산 노드에 matplotlib 이
  없으면 더미를 꽂아 파서만 살려서 쓴다(아래 _import_parser 참조).

⚠ 정규화 규약이 family 와 **다르다** — 의도적이다.
  plot_lobster_4panel.py 는 매칭된 결합의 -pCOHP 를 **합(sum)** 하고 ICOHP 상자는
  **결합당 평균**을 찍는다. 그러면 곡선의 적분 ≠ 상자 값이고, N 이 크게 다른 패널끼리
  (P-O N=1 vs Li-S N=106) 높이 비교가 무의미해진다.
  여기서는 곡선도 **결합당 평균**으로 낸다 → 패널 간 높이가 곧 결합당 세기다.
  참고용으로 sum 곡선도 같은 CSV 에 함께 낸다(_sum 접미사; --no_sum 으로 뺄 수 있다).

⚠ **곡선 적분 ≠ ICOHP** 인 경우가 있다 — 창 잘림.
  COHPCAR 의 에너지 격자는 -infinity 에서 시작하지 않는다(LPSOCl 실측 E_min = -15.03 eV).
  IpCOHP 열은 누적값이라 첫 점에서 이미 0 이 아니고, 그 아래(deep) 결합 기여는 곡선에 없다.
  실측: P-O 는 ICOHP 의 **30% 만** 창 안에 있었다 (O 2s 가 -15 eV 아래).
  → 각 쌍마다 window_coverage 를 함께 낸다. 1 보다 작으면 그 패널의 곡선 면적으로
     ICOHP 를 주장하면 안 된다. 곡선은 '어느 에너지에서 결합/반결합인가' 만 말한다.

  python3 tools/figures/extract_cohp_curves.py \
      --lobster_dir /data/work/runs/lpsocl_dft/lobster_ext \
      --out db/properties/lpsocl_cohp_curves_origin.csv \
      --pairs 'P-S:2.6,P-O,Li-S,Li-Cl,Li-O,S-S' \
      --emin -12 --emax 6
"""
import argparse
import csv
import importlib.util
import json
import sys
import types
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PARSER_SRC = ROOT / "tools" / "modelc_v3" / "plot_lobster_4panel.py"

# numpy 2.x 는 trapz 를 제거했다(trapezoid 로 개명). gabia/KISTI 가 섞여 있으니 둘 다 받는다.
_trapz = getattr(np, "trapezoid", None) or np.trapz

# 원소쌍별 제외 규칙 — plot_lobster_4panel.py 의 PANEL_CONFIG 와 동일하게 유지한다.
#   S-S 는 P/Li/Cl 을 낀 3체 항목이 ICOHPLIST 에 섞여 들어와서 제외가 필요하고,
#   P-S 는 dmax 2.6 Å 로 잘라야 사면체 결합만 남는다(생성기 컷오프 안쪽의 긴 접촉 2개 탈락).
DEFAULT_EXCLUDE = {"P-S": ["Li"], "S-S": ["P", "Li", "Cl"]}
DEFAULT_DMAX = {"P-S": 2.6}


def _import_parser():
    """plot_lobster_4panel.py 를 matplotlib 없이도 import 한다 (파서만 쓸 거라서)."""
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        # 계산 노드에 matplotlib 이 없을 수 있다. 파서는 numpy 만 쓰므로 더미로 통과시킨다.
        mpl = types.ModuleType("matplotlib")
        mpl.use = lambda *a, **k: None
        plt = types.ModuleType("matplotlib.pyplot")
        patches = types.ModuleType("matplotlib.patches")
        patches.FancyBboxPatch = object
        sys.modules.update({"matplotlib": mpl, "matplotlib.pyplot": plt,
                            "matplotlib.patches": patches})
        print("[note] matplotlib 없음 → 더미로 대체 (파서만 사용, 그림은 로컬에서 그린다)")
    spec = importlib.util.spec_from_file_location("_p4", PARSER_SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_pairs(s):
    """'P-S:2.6,P-O,Li-S' → [(label, [a,b], exclude, dmax), ...]"""
    out = []
    for tok in s.split(","):
        tok = tok.strip()
        if not tok:
            continue
        spec, _, dm = tok.partition(":")
        a, _, b = spec.strip().partition("-")
        lab = f"{a}-{b}"
        out.append((lab, [a, b], DEFAULT_EXCLUDE.get(lab, []),
                    float(dm) if dm else DEFAULT_DMAX.get(lab)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lobster_dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pairs", default="P-S:2.6,P-O,Li-S,Li-Cl,Li-O,S-S")
    ap.add_argument("--emin", type=float, default=-12.0, help="회수 크기 절감 — 그림 창만 남긴다")
    ap.add_argument("--emax", type=float, default=6.0)
    ap.add_argument("--smooth", type=float, default=0.10, help="Gaussian sigma (eV); family 와 동일 0.10")
    ap.add_argument("--stride", type=int, default=0,
                    help="0 = --max_rows 로 자동. >0 이면 그 간격으로 솎는다")
    ap.add_argument("--max_rows", type=int, default=700,
                    help="회수(base64 붙여넣기) 크기 상한용. sigma 0.10 eV 평활 뒤라 "
                         "0.03 eV 격자면 충분하다 — 이보다 촘촘한 건 정보가 아니라 무게다")
    ap.add_argument("--decimals", type=int, default=4)
    ap.add_argument("--no_sum", action="store_true",
                    help="sum_ 열을 빼서 전송량을 반으로 (그림은 mean_ 만 쓴다)")
    ap.add_argument("--label", default="", help="CSV 머리말에 넣을 계 이름")
    args = ap.parse_args()

    P = _import_parser()
    work = Path(args.lobster_dir)
    cohp_path = work / "COHPCAR.lobster"
    if not cohp_path.exists():
        raise SystemExit(f"missing COHPCAR.lobster in {work}")

    E, bonds_meta = P.parse_cohpcar(cohp_path)
    print(f"parsed {len(bonds_meta)} bond entries × {len(E)} energy points "
          f"(E {E.min():.2f} .. {E.max():.2f} eV)")

    pairs = parse_pairs(args.pairs)
    mean_curves, sum_curves, meta = {}, {}, {}
    for lab, keys, exc, dmax in pairs:
        csum, ibox, nb = P.aggregate_bond_pair(E, bonds_meta, keys, exc, dmax)
        if nb == 0:
            print(f"  · {lab:6s} 매칭 0건 — 열에서 제외")
            continue
        s_sum = P.gaussian_smooth(csum, E, args.smooth)
        s_mean = s_sum / nb
        sum_curves[lab] = s_sum
        mean_curves[lab] = s_mean
        # ⚠ 자기일관 검사의 올바른 기준은 **총 ICOHP 가 아니라 창 안 몫**이다.
        #   COHPCAR 격자는 -infinity 에서 시작하지 않으므로(LPSOCl: E_min = -15.03 eV),
        #   창 밖의 deep 결합 기여가 곡선에 없다. 총 ICOHP 와 비교하면 멀쩡한 파일도
        #   "안 맞는다"고 나오고(P-O 30%), 반대로 진짜 파싱 오류를 놓친다.
        matched = P.match_bonds(bonds_meta, keys, exc, dmax)
        i_ef = float(np.mean([b["icohp"] for b in matched]))
        i_lo = float(np.mean([b.get("icohp_at_emin", 0.0) for b in matched]))
        in_window = i_ef - i_lo                     # 창 안에서 쌓인 ICOHP (음수)
        cov = in_window / i_ef if abs(i_ef) > 1e-9 else float("nan")
        m = E <= 0.0
        integ = float(_trapz(s_mean[m], E[m]))
        resid = abs(integ + in_window) / max(abs(in_window), 1e-9)
        ok = "정상" if resid < 0.05 else f"⚠ 불일치 {resid*100:.0f}%"
        meta[lab] = {"N": nb, "ICOHP_per_bond_eV": round(ibox, 4),
                     "ICOHP_in_window_eV": round(in_window, 4),
                     "window_coverage": round(cov, 4),
                     "integral_to_EF_eV": round(integ, 4),
                     "dmax_A": dmax, "exclude": exc}
        print(f"  · {lab:6s} N={nb:3d}  ICOHP/bond {ibox:+.3f} eV  "
              f"창 안 {in_window:+.3f} ({cov*100:5.1f}%)  ∫곡선 {-integ:+.3f}  [{ok}]")

    if not mean_curves:
        raise SystemExit("매칭된 결합쌍이 하나도 없다 — --pairs 원소기호 확인")

    sel = (E >= args.emin) & (E <= args.emax)
    nsel = int(sel.sum())
    stride = args.stride if args.stride > 0 else max(1, -(-nsel // max(1, args.max_rows)))
    idx = np.where(sel)[0][::stride]
    if stride > 1:
        dE = abs(E[1] - E[0]) * stride
        print(f"[stride] {nsel} → {len(idx)} rows (간격 {dE:.4f} eV, "
              f"평활 sigma {args.smooth} eV 대비 {args.smooth/dE:.1f} pt/sigma)")
    labs = list(mean_curves)
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    fmt = f"%.{args.decimals}f"
    with open(outp, "w", newline="", encoding="utf-8") as f:
        f.write(f"# energy-resolved COHP curves{(' — ' + args.label) if args.label else ''}\n")
        f.write(f"# source {cohp_path}  ·  Gaussian sigma {args.smooth} eV  ·  "
                f"window [{args.emin}, {args.emax}] eV, stride {stride}\n")
        f.write("# sign: -pCOHP > 0 = BONDING, < 0 = ANTIBONDING;  E = E - E_F (E_F at 0)\n")
        f.write("# mean_ = per-bond average (integral to E_F == -ICOHP/bond); "
                "sum_ = family convention (plot_lobster_4panel.py)\n")
        f.write("# " + json.dumps(meta, ensure_ascii=False) + "\n")
        f.write("# ⚠ window_coverage: 이 창 안에 담긴 ICOHP 비율. 1 보다 작으면 "
                "창 아래(deep) 결합 기여가 곡선에 없다 — 곡선 적분으로 ICOHP 를 재현할 수 없다.\n")
        w = csv.writer(f)
        cols = [f"mean_pCOHP_{k}" for k in labs]
        if not args.no_sum:
            cols += [f"sum_pCOHP_{k}" for k in labs]
        w.writerow(["E_minus_EF_eV"] + cols)
        for i in idx:
            row = [f"{E[i]:.4f}"] + [fmt % mean_curves[k][i] for k in labs]
            if not args.no_sum:
                row += [fmt % sum_curves[k][i] for k in labs]
            w.writerow(row)
    kb = outp.stat().st_size / 1024
    print(f"\n→ {outp}   {len(idx)} rows × {1 + (1 if args.no_sum else 2)*len(labs)} cols   {kb:.1f} KB")
    sidecar = outp.with_suffix(".meta.json")
    sidecar.write_text(json.dumps(
        {"source": str(cohp_path), "smooth_eV": args.smooth,
         "window_eV": [args.emin, args.emax], "stride": stride,
         "pairs": meta}, ensure_ascii=False, indent=2) + "\n")
    print(f"→ {sidecar}")


if __name__ == "__main__":
    main()
