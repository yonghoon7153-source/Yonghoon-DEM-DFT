#!/usr/bin/env python3
"""mlip_committee.py — T1: UMA 외삽 대리지표 (모델 위원회).

왜 이게 필요한가
----------------
이상욱 랩은 MTP-MD 스냅샷마다 extrapolation grade gamma 를 계산해
gamma_select ~ gamma_break 사이를 "Accurate region" 으로 관리한다
(kim2026 SEI 논문 실물: gamma_select=2, gamma_break 10->5->2).

⛔ **그 gamma 를 우리가 쓸 수 없다.** gamma 는 MTP 의 **선형 기저 위 maxvol /
D-optimality** 로 정의되는데 UMA 는 비선형 등변 GNN 이라 정의 자체가 없다.

이식할 수 있는 것은 **논리 구조**뿐이다:
  ① 대리지표를 하나 정한다
  ② **선별 문턱과 중단 문턱을 분리**한다
  ③ 중단 문턱을 조여 수렴을 판정한다

여기서 쓰는 대리지표 = **모델 위원회 불일치(query-by-committee)**.
같은 스냅샷에 대해 독립 학습된 MLIP 들이 힘을 다르게 예측하면, 그 배열은
**합의 영역 밖**이다. 표준적이고 근거가 탄탄한 불확실도 프록시다.

⚠ 이 지표가 **말하지 않는 것**
------------------------------
- **절대 정확도를 말하지 않는다.** UMA(OMat24)·MACE-MP-0(MPtrj)·SevenNet-0 은
  **전부 PBE 계열**이다. kim2024 는 argyrodite 에서 sigma 를 8배 가르는 것이
  아키텍처가 아니라 **훈련 functional** 임을 보였고, lee2024 는 PBE 계열이 오히려
  틀리는 쪽(optB88 이 실험과 맞음)임을 보였다.
  → **세 모델이 일치해도 절대 sigma 인용 금지 규율은 그대로다.**
- 이 지표가 재는 것은 "이 배열이 훈련 분포에서 이상한가" 뿐이고,
  그 목적에는 같은 functional 계열인 것이 **오히려 무해하다**.

실행
----
  # 1) 스냅샷 뽑기 (엔진 무관, ASE 만 필요)
  python3 tools/ionic/mlip_committee.py sample --traj ~/work/runs/.../traj.traj -n 200

  # 2) 엔진별 힘 계산 (각 env 에서 따로)
  conda activate uma   && python3 ... predict --engine uma
  conda activate mlipx && python3 ... predict --engine mace
  conda activate mlipx && python3 ... predict --engine sevennet

  # 3) 합의 분석
  python3 tools/ionic/mlip_committee.py analyze --dir <workdir>
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np


# ── 1) 스냅샷 표본 ──────────────────────────────────────────────────────────
def cmd_sample(a):
    from ase.io import read, write
    frames = read(a.traj, index=":")
    n = len(frames)
    if n == 0:
        sys.exit(f"{a.traj} 에 프레임이 없다")
    # 균등 표본 — 시간적으로 치우치면 '초기 완화 구간만 이상' 같은 착시가 생긴다
    idx = np.linspace(0, n - 1, min(a.n, n)).round().astype(int)
    idx = sorted(set(idx.tolist()))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    write(str(out / "snapshots.xyz"), [frames[i] for i in idx])
    meta = {"source_traj": str(Path(a.traj).resolve()), "n_frames_total": n,
            "n_sampled": len(idx), "frame_indices": idx,
            "note": "균등 표본. 시간 치우침 방지."}
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"{len(idx)}/{n} 프레임 → {out/'snapshots.xyz'}")


# ── 2) 엔진별 예측 ──────────────────────────────────────────────────────────
def get_calc(engine, device):
    """엔진별 ASE calculator. 각 엔진은 자기 env 에서만 import 된다."""
    if engine == "uma":
        from fairchem.core import pretrained_mlip, FAIRChemCalculator
        pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
        return FAIRChemCalculator(pred, task_name="omat")
    if engine == "mace":
        from mace.calculators import mace_mp
        return mace_mp(model="medium", device=device, default_dtype="float64")
    if engine == "sevennet":
        from sevenn.calculator import SevenNetCalculator
        return SevenNetCalculator(model="7net-0", device=device)
    sys.exit(f"모르는 엔진: {engine}")


def cmd_predict(a):
    from ase.io import read
    d = Path(a.dir)
    frames = read(str(d / "snapshots.xyz"), index=":")
    calc = get_calc(a.engine, a.device)
    E, F = [], []
    for i, at in enumerate(frames):
        at.calc = calc
        E.append(float(at.get_potential_energy()))
        F.append(np.asarray(at.get_forces(), dtype=float))
        if (i + 1) % 20 == 0:
            print(f"  {i+1}/{len(frames)}")
    np.savez_compressed(d / f"pred_{a.engine}.npz",
                        energy=np.array(E), forces=np.array(F),
                        natoms=np.array([len(f) for f in frames]),
                        symbols=np.array(frames[0].get_chemical_symbols()))
    print(f"→ {d/f'pred_{a.engine}.npz'}  ({len(frames)} 프레임)")


# ── 3) 합의 분석 ────────────────────────────────────────────────────────────
def cmd_analyze(a):
    d = Path(a.dir)
    preds = {}
    for p in sorted(d.glob("pred_*.npz")):
        preds[p.stem[5:]] = np.load(p, allow_pickle=True)
    if len(preds) < 2:
        sys.exit(f"엔진이 {len(preds)}개뿐 — 위원회는 최소 2개 필요")
    names = sorted(preds)
    F = {k: preds[k]["forces"] for k in names}           # (nframe, natom, 3)
    nf = F[names[0]].shape[0]

    # 프레임별 **원자당 힘 RMS 불일치** — 쌍별 최대값을 그 프레임의 불일치로
    per_frame, per_pair = np.zeros(nf), {}
    for i, x in enumerate(names):
        for y in names[i + 1:]:
            dF = F[x] - F[y]
            rms = np.sqrt((dF ** 2).sum(axis=2).mean(axis=1))   # (nframe,)
            per_pair[f"{x}|{y}"] = rms
            per_frame = np.maximum(per_frame, rms)

    # ⚠ 문턱은 **분포에서 유도**한다 — 임의 상수를 새로 만들지 않는다.
    #    선별(select) = 중앙값의 2배 · 중단(break) = 95 백분위. 두 문턱 분리는
    #    kim2026 의 gamma_select/gamma_break 논리를 그대로 가져온 것.
    med = float(np.median(per_frame))
    sel = 2.0 * med
    brk = float(np.percentile(per_frame, 95))

    # 원소별 불일치 — 어느 화학이 합의 밖인지
    syms = [str(s) for s in preds[names[0]]["symbols"]]
    by_el = {}
    for el in sorted(set(syms)):
        m = np.array([s == el for s in syms])
        vals = []
        for i, x in enumerate(names):
            for y in names[i + 1:]:
                dF = (F[x] - F[y])[:, m, :]
                vals.append(np.sqrt((dF ** 2).sum(axis=2)).mean())
        by_el[el] = float(np.mean(vals))

    out = {
        "property": "mlip_committee_disagreement", "engines": names,
        "n_frames": int(nf),
        "meta": json.loads((d / "meta.json").read_text()) if (d / "meta.json").exists() else {},
        "per_pair_force_rms_eV_per_A": {k: {"median": float(np.median(v)),
                                            "p95": float(np.percentile(v, 95)),
                                            "max": float(v.max())}
                                        for k, v in per_pair.items()},
        "committee_frame_disagreement": {
            "median": med, "p95": brk, "max": float(per_frame.max()),
            "threshold_select": sel, "threshold_break": brk,
            "n_above_select": int((per_frame > sel).sum()),
            "n_above_break": int((per_frame > brk).sum()),
            "frames_above_break": [int(i) for i in np.where(per_frame > brk)[0]],
        },
        "by_element_mean_force_disagreement_eV_per_A": by_el,
        "honesty": [
            "⛔ **이 지표는 절대 정확도를 말하지 않는다.** UMA(OMat24)·MACE-MP-0(MPtrj)·"
            "SevenNet-0 은 전부 PBE 계열이다. kim2024 는 argyrodite 에서 sigma 를 8배 가르는 것이 "
            "아키텍처가 아니라 **훈련 functional** 임을 보였고, lee2024 는 PBE 계열이 오히려 "
            "틀리는 쪽임을 보였다 → **일치해도 절대 sigma 인용 금지 규율은 그대로다.**",
            "✅ 이 지표가 말하는 것: '이 배열이 훈련 분포에서 이상한가'. 그 목적에는 같은 "
            "functional 계열인 것이 무해하다.",
            "⚠ 문턱(select = 중앙값 x2, break = p95)은 **이 표본의 분포에서 유도**한 것이고 "
            "물리적 절대 기준이 아니다. 계·온도가 바뀌면 다시 뽑아야 한다.",
            "⚠ gamma(MTP) 와 **같은 양이 아니다.** gamma 는 선형 기저 위 maxvol 이고 이건 "
            "모델 간 분산이다 — 논리 구조만 공유한다.",
        ],
        "verdict": ("합의 영역 밖 프레임 없음 — 궤적이 위원회 합의 안에 있다."
                    if (per_frame > brk).sum() == 0 else
                    f"{int((per_frame > brk).sum())}개 프레임이 중단 문턱 초과 — "
                    "해당 구간의 결과는 신뢰구간 밖으로 표시할 것."),
    }
    (d / "committee_verdict.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")

    print("=" * 70)
    print(f"엔진 {len(names)}종: {', '.join(names)} · 프레임 {nf}")
    for k, v in out["per_pair_force_rms_eV_per_A"].items():
        print(f"  {k:22s} 중앙 {v['median']:.4f}  p95 {v['p95']:.4f}  max {v['max']:.4f} eV/Å")
    c = out["committee_frame_disagreement"]
    print(f"\n  위원회 불일치: 중앙 {c['median']:.4f} · p95 {c['p95']:.4f} · max {c['max']:.4f}")
    print(f"  select({sel:.4f}) 초과 {c['n_above_select']} · break({brk:.4f}) 초과 {c['n_above_break']}")
    print("\n  원소별 평균 불일치 (eV/Å):")
    for el, v in sorted(by_el.items(), key=lambda kv: -kv[1]):
        print(f"    {el:3s} {v:.4f}")
    print("=" * 70)
    print(f"→ {d/'committee_verdict.json'}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample"); s.add_argument("--traj", required=True)
    s.add_argument("-n", type=int, default=200); s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_sample)
    p = sub.add_parser("predict"); p.add_argument("--dir", required=True)
    p.add_argument("--engine", required=True, choices=["uma", "mace", "sevennet"])
    p.add_argument("--device", default="cuda"); p.set_defaults(fn=cmd_predict)
    n = sub.add_parser("analyze"); n.add_argument("--dir", required=True)
    n.set_defaults(fn=cmd_analyze)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
