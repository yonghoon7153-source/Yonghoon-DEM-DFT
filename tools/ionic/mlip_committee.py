#!/usr/bin/env python3
"""mlip_committee.py — T1: UMA 외삽 대리지표 (모델 위원회).

왜 이게 필요한가
----------------
이상욱 랩은 MTP-MD 스냅샷마다 extrapolation grade gamma 를 계산해
gamma_select ~ gamma_break 사이를 "Accurate region" 으로 관리한다
(kim2026 SEI 논문 실물: gamma_select=2, gamma_break 10->5->2).

⛔ **그 gamma 를 우리가 쓸 수 없다.** gamma 는 MTP 의 **선형 기저 위 maxvol /
D-optimality** 로 정의된다 (원전 = Podryabinkin & Shapeev 2017, Comput. Mater. Sci. 140, 171).

⚠ **2026-08-26 정정** — 초판은 여기에 *"UMA 는 비선형이라 **정의 자체가 없다**"* 라고 썼는데
   **과했다.** Gubaev 2019 (Comput. Mater. Sci. 156, 148) 본문이 정반대를 말한다:
   *"As the model in this paper has a **nonlinear dependence on its parameters**, we apply a
   **generalization of the D-optimality criterion to the nonlinear case**."*
   ⇒ 정의는 일반화될 수 있다. 우리를 막는 것은 **`X`(설계행렬)의 부재가 아니라 OMat24 훈련셋을
   우리가 갖고 있지 않다는 것** — 원리적 장벽이 아니라 실무적 장벽이다.
   이 편이 오히려 이 도구에 유리하다: *"원리적으로 불가"* 가 아니라 *"대리지표를 세우면 된다"* 가 된다.

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

⚠ **위원회 구성의 함정 (2026-08-26, OMat24 보충자료)**
  softening 은 **아키텍처가 아니라 훈련셋 다양성**에서 온다는 것이 측정됐다
  (`db/external/omat24/README.md`: 5개 아키텍처 전부에서 MPtrj -> OMat24 계열로 개선).
  그런데 이 위원회의 MACE-MP-0 과 SevenNet-0 은 **둘 다 MPtrj** 이고 UMA 만 OMat24 다.
  ⇒ **불일치가 "UMA 가 이상하다" 가 아니라 "저 둘이 무르다" 여서 생길 수 있다.**
  불일치의 **부호와 방향**을 봐야 하고, 다수결로 UMA 를 이상치 취급하면 안 된다.

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
        # torch>=2.6 은 torch.load 의 weights_only 기본값을 True 로 바꿨고, sevenn 체크포인트가
        # slice 객체를 담고 있어 로드가 깨진다. 신뢰 가능한 공식 체크포인트이므로 allowlist 한다.
        import torch
        try:
            torch.serialization.add_safe_globals([slice])
        except Exception:
            pass
        from sevenn.calculator import SevenNetCalculator
        try:
            return SevenNetCalculator(model="7net-0", device=device)
        except Exception:
            # allowlist 로도 안 되면 weights_only=False 로 강제 (공식 배포본 한정)
            _orig = torch.load
            torch.load = lambda *a, **k: _orig(*a, **{**k, "weights_only": False})
            try:
                return SevenNetCalculator(model="7net-0", device=device)
            finally:
                torch.load = _orig
    sys.exit(f"모르는 엔진: {engine}")


#: 모델에서 못 읽었을 때만 쓰는 **문헌값**. (값, 출처) — 출처 없이 숫자만 두지 않는다.
KNOWN_CUTOFF_A = {
    "uma": (6.0, "litdb/papers/uma2026_family_of_universal_models_for_atoms.md "
                 "§'공통: 6 Å cutoff' · §164 '6 Å 이내 쌍을 엣지로'"),
    "sevennet": (5.0, "litdb/papers/park2024_sevennet_parallel_gnn_md.md — SevenNet-0 r_c = 5 Å"),
}


def engine_info(engine, device="cpu"):
    """엔진의 **유효 수용영역**을 알아낸다. → dict

    왜 필요한가 (2026-08-26):
      `park2024_sevennet_parallel_gnn_md` 가 명시한다 —
      *"GNN-IPs require a broader region for communication, reaching up to **r_c multiplied by
      the number of message-passing steps**"*. 즉 **유효 수용영역 = cutoff × 층 수** 다.
      그런데 우리는 **UMA 의 층 수를 어디에도 안 적어놨다.** 층 수를 모르면
      ① 슬랩 두께 하한(T3)을 못 정하고 ② 주기셀이 자기 이미지를 보는지 판정 못 한다.

    ⛔ 이 함수가 **못 하는 것**
      · 정확도를 말하지 않는다. 배선(topology)만 본다.
      · 층 수 추정은 **모듈 이름 규칙**에 기댄다 — 이름이 바뀌면 못 찾는다.
        못 찾으면 **0 이나 추측값을 넣지 않고 None 을 돌려준다**.
      · cutoff 가 여러 개인 모델(원소쌍별 등)은 최대값만 본다.
    """
    import re
    out = {"engine": engine, "device": device, "cutoff_A": None,
           "n_message_passing": None, "n_params": None, "source": {}, "notes": []}
    try:
        calc = get_calc(engine, device)
    except Exception as e:
        out["notes"].append(f"⛔ calculator 를 못 만들었다: {type(e).__name__}: {e}")
        return out

    # calculator → nn.Module 을 찾는다. 엔진마다 감싸는 층이 달라 이름을 고정하지 않는다.
    mod = None
    for path in ("model", "predictor.model", "predict_unit.model", "calc.model",
                 "predictor", "predict_unit"):
        o = calc
        try:
            for p in path.split("."):
                o = getattr(o, p)
            if hasattr(o, "named_modules"):
                mod, out["source"]["module_path"] = o, path
                break
        except AttributeError:
            continue
    if mod is None:
        out["notes"].append("⛔ nn.Module 을 못 찾았다 — calculator 구조가 바뀌었다")
        return out

    names = [n for n, _ in mod.named_modules()]
    out["source"]["n_modules"] = len(names)
    try:
        out["n_params"] = sum(p.numel() for p in mod.parameters())
    except Exception:
        pass

    # ① 층 수 — 반복 블록의 최대 인덱스 + 1. 여러 후보 이름을 훑고 **가장 그럴듯한 하나**를 고른다.
    nlay, cands = _detect_layers(names)
    if cands:
        out["n_message_passing"] = nlay
        out["source"]["layer_patterns"] = {k: v for k, v in cands.items()}
        if len(set(cands.values())) > 1:
            out["notes"].append(f"⚠ 층 수 후보가 갈린다 {sorted(set(cands.values()))} — 최대값을 썼다")
    else:
        out["notes"].append("⚠ 반복 블록 이름을 못 찾았다 — 층 수 미상(추측하지 않는다)")

    # ② cutoff — 어디 있는지 모델마다 다르다. **전 서브모듈**을 훑는다.
    #    (초판은 top-level 만 봐서 UMA 에서 못 찾았다 — 2026-08-26 실측)
    found = {}
    KEYS = ("cutoff", "r_max", "rmax", "max_radius", "cutoff_radius", "radius_cutoff")
    def _num(v):
        try:
            import torch
            if isinstance(v, torch.Tensor) and v.numel() == 1:
                return float(v)
        except Exception:
            pass
        return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None
    try:
        for n, b in mod.named_buffers():
            if any(k in n.lower() for k in KEYS) and (x := _num(b)) is not None:
                found[f"buffer:{n}"] = x
    except Exception:
        pass
    for name, sub in [("", mod)] + list(mod.named_modules()):
        for attr in KEYS:
            if (x := _num(getattr(sub, attr, None))) is not None:
                found[f"{name or 'model'}.{attr}"] = x
        # config/hparams 처럼 dict 로 들고 있는 경우
        for cattr in ("config", "model_config", "hparams", "cfg", "backbone_config"):
            d = getattr(sub, cattr, None)
            if isinstance(d, dict):
                for k, v in d.items():
                    if any(kk in str(k).lower() for kk in KEYS) and (x := _num(v)) is not None:
                        found[f"{name or 'model'}.{cattr}[{k}]"] = x
    for attr in KEYS:
        if (x := _num(getattr(calc, attr, None))) is not None:
            found[f"calc.{attr}"] = x

    # 물리적으로 말이 되는 것만 (0 < r < 20 Å). 0.0 이나 1e9 같은 잡값을 컷오프로 삼지 않는다.
    sane = {k: v for k, v in found.items() if 0.5 < v < 20.0}
    if sane:
        out["cutoff_A"] = max(sane.values())
        out["source"]["cutoff_candidates"] = sane
        out["source"]["cutoff_source"] = "introspected"
        if found and len(sane) < len(found):
            out["notes"].append(f"⚠ 범위 밖 후보를 버렸다: "
                                f"{ {k: v for k, v in found.items() if k not in sane} }")
    elif engine in KNOWN_CUTOFF_A:
        # ⛔ 마지막 수단. **측정한 값이 아니라 문헌값**이라는 것을 반드시 기록한다.
        out["cutoff_A"] = KNOWN_CUTOFF_A[engine][0]
        out["source"]["cutoff_source"] = "literature"
        out["notes"].append(
            f"⚠ 모델에서 cutoff 를 못 찾아 **문헌값 {KNOWN_CUTOFF_A[engine][0]} Å** 을 썼다 "
            f"({KNOWN_CUTOFF_A[engine][1]}). **측정값이 아니다** — 체크포인트가 바뀌면 틀릴 수 있다.")
    else:
        out["notes"].append("⚠ cutoff 를 못 찾았고 문헌값도 없다 — 설정 파일에서 직접 확인할 것")

    if out["cutoff_A"] and out["n_message_passing"]:
        out["effective_receptive_field_A"] = out["cutoff_A"] * out["n_message_passing"]
        out["notes"].append(
            f"유효 수용영역 = cutoff {out['cutoff_A']:.2f} Å × {out['n_message_passing']} 층 "
            f"= **{out['effective_receptive_field_A']:.1f} Å**. 주기셀 한 변이 이 값의 "
            f"2배보다 작으면 원자가 자기 이미지를 본다.")
    return out


def cmd_info(a):
    """엔진 배선을 찍는다 — 정확도가 아니라 **유효 수용영역**을 알기 위한 것."""
    import json as _j
    rows = []
    for eng in a.engines:
        r = engine_info(eng, a.device)
        rows.append(r)
        rf = r.get("effective_receptive_field_A")
        print(f"\n══ {eng} ══")
        print(f"  파라미터 {r['n_params']:,}" if r["n_params"] else "  파라미터 미상")
        print(f"  cutoff {r['cutoff_A']} Å · 메시지패싱 {r['n_message_passing']} 층")
        print(f"  **유효 수용영역 {rf:.1f} Å**" if rf else "  유효 수용영역 계산 불가")
        for n in r["notes"]:
            print(f"    {n}")
    ok = all(r.get("effective_receptive_field_A") for r in rows)
    if a.out:
        Path(a.out).write_text(_j.dumps(rows, ensure_ascii=False, indent=2))
        # ⛔ 실패했는데 `✓` 를 찍으면 화면만 보고 '확인됐다' 로 기록된다 (2026-08-26 실측).
        #    파일을 쓴 것과 알아낸 것은 다른 일이다.
        print(f"\n{'✓' if ok else '⚠ (미완)'} → {a.out}")
    if not ok:
        miss = [r["engine"] for r in rows if not r.get("effective_receptive_field_A")]
        print(f"\n⛔ **알아내지 못했다**: {', '.join(miss)}")
        env = [r["engine"] for r in rows
               if any("No module named" in n for n in r["notes"])]
        if env:
            print(f"   → 모듈이 없다. **env 를 켜고 다시** 하라: "
                  f"`conda activate uma` (uma) / `conda activate mlipx` (mace·sevennet)")
    return 0 if ok else 4


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


# ── 2b) DFT 라벨 대조 (bench) ───────────────────────────────────────────────
def stream_labeled(path, stride, limit=None):
    """extxyz 를 **스트리밍**으로 훑어 stride 간격 프레임만 돌려준다. → (idx, Atoms) 제너레이터

    ⛔ `read(index='::N')` 을 쓰지 않는 이유: ase 는 그래도 전 파일을 파싱해 메모리에 올린다.
      실측 대상이 550 MB · 25,000 프레임이라 그 방식은 못 쓴다.
    ⛔ 이 함수가 못 하는 것: 프레임 총수를 미리 모른다 (한 번 훑기 전에는).
    """
    from ase.io import iread
    n = 0
    for i, at in enumerate(iread(str(path), format="extxyz")):
        if i % stride:
            continue
        yield i, at
        n += 1
        if limit and n >= limit:
            return


def force_stats(f_ref, f_pred):
    """참조힘 vs 예측힘 → dict. **성분 단위**로 잰다 (원자당 벡터가 아니라).

    왜 성분인가: 문헌 관례(Shapeev 2016 · Park 2024 · 이상욱 랩 덱)가 전부 성분 MAE 다.
    다른 정의로 재면 우리 값만 자릿수가 달라져 비교가 깨진다.

    ★ **상대오차도 같이 낸다** — Shapeev 2016 이 전 성분 RMS(1.505 eV/Å)로 나눠
      2.8 % 로 보고한다. 같은 0.05 eV/Å 도 딱딱한 계에선 훌륭하고 무른 계에선 형편없다.
    """
    d = (f_pred - f_ref).ravel()
    r = f_ref.ravel()
    rms_ref = float(np.sqrt((r ** 2).mean()))
    return {"n_components": int(d.size),
            "mae_eVA": float(np.abs(d).mean()),
            "rmse_eVA": float(np.sqrt((d ** 2).mean())),
            "max_abs_eVA": float(np.abs(d).max()),
            "rms_ref_eVA": rms_ref,
            "rel_mae_pct": float(np.abs(d).mean() / rms_ref * 100) if rms_ref else None,
            # 성분 상관 — 부호까지 맞는지 (MAE 만으로는 못 본다)
            "pearson_r": float(np.corrcoef(r, f_pred.ravel())[0, 1]) if d.size > 2 else None,
            # ★ **softening 기울기** — OMat24 보충자료의 `force_softening` 과 같은 뜻.
            #   원점을 지나는 최소제곱 기울기 s = Σ(F_ref·F_pred)/Σ(F_ref²).
            #   s < 1 = 예측힘이 참조보다 **작다** = PES 가 무르다. s = 1 이 이상.
            #   ⛔ r 로는 못 본다 — r 은 척도불변이라 힘을 전부 절반으로 줄여도 r=1 이다.
            #   ⚠ 이 한 계에서의 기울기다. "이 모델은 무르다/안 무르다" 로 일반화하지 말 것.
            "softening_slope": (float((r * f_pred.ravel()).sum() / (r ** 2).sum())
                                if (r ** 2).sum() > 0 else None)}


def cmd_bench(a):
    """**DFT 라벨이 붙은 extxyz** 에 엔진을 돌려 힘·에너지를 대조한다.

    이게 왜 `analyze`(위원회)와 다른가: 위원회는 **정답 없이** 모델끼리 비교한다.
    여기는 **정답지가 있다** — 문헌 데이터셋의 DFT 에너지·힘.

    ⛔ **에너지 절대오차를 정확도로 읽지 마라.** 우리 엔진과 그들 DFT 는 pseudo·컷오프·
      기준이 달라 **상수 오프셋**이 반드시 생긴다. 오프셋은 힘에 기여하지 않고 에너지 차이에서
      상쇄된다(2026-08-26 실측: 이상욱 랩 가수분해 데이터에서 MAE 8.77 중 8.77 이 오프셋,
      남는 산포는 1.35 meV/atom). 그래서 여기서는 **편향과 산포를 갈라서** 보고한다.
    ⛔ **힘이 진짜 지표다.** 동역학을 지배하는 것은 힘이고, 힘에는 기준 오프셋이 없다.
    """
    from ase.io import read as _read
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    calc = get_calc(a.engine, a.device)

    rows, FR, FP = [], [], []
    print(f"  {a.xyz} · stride {a.stride}" + (f" · 최대 {a.limit} 프레임" if a.limit else ""))
    for k, (idx, at) in enumerate(stream_labeled(a.xyz, a.stride, a.limit)):
        try:
            e_ref = float(at.get_potential_energy())
            f_ref = np.asarray(at.get_forces(), dtype=float)
        except Exception as e:
            sys.exit(f"⛔ 프레임 {idx} 에 DFT 라벨이 없다 ({type(e).__name__}) — "
                     f"이 파일은 bench 대상이 아니다")
        nat = len(at)
        at2 = at.copy(); at2.calc = calc
        e_p = float(at2.get_potential_energy())
        f_p = np.asarray(at2.get_forces(), dtype=float)
        rows.append({"frame": idx, "n_atoms": nat,
                     "E_ref_eV": e_ref, "E_pred_eV": e_p,
                     "dE_meV_per_atom": (e_p - e_ref) / nat * 1000,
                     "F_mae_eVA": float(np.abs(f_p - f_ref).mean()),
                     "F_rms_ref_eVA": float(np.sqrt((f_ref ** 2).mean()))})
        FR.append(f_ref); FP.append(f_p)
        if (k + 1) % 20 == 0:
            print(f"    {k+1} 프레임")
    if not rows:
        sys.exit("⛔ 프레임을 하나도 못 읽었다")

    FR_l, FP_l = FR, FP                      # 프레임별 배열 (구간 분할용)
    FR, FP = np.concatenate(FR), np.concatenate(FP)
    fs = force_stats(FR, FP)
    dE = np.array([r["dE_meV_per_atom"] for r in rows])
    bias, scat = float(dE.mean()), float(dE.std())
    same_sign = int((np.sign(dE) == np.sign(bias)).sum())

    summ = {"xyz": str(a.xyz), "engine": a.engine, "n_frames": len(rows),
            "stride": a.stride, "force": fs,
            "energy_per_atom_meV": {
                "bias": bias, "scatter_sd": scat,
                "mae_raw": float(np.abs(dE).mean()),
                "mae_after_bias_removal": float(np.abs(dE - bias).mean()),
                "same_sign_frames": f"{same_sign}/{len(dE)}"},
            "⛔_do_not": ["에너지 절대오차를 정확도로 읽지 말 것 — 기준 오프셋이 섞여 있다",
                          "이 값은 '이 데이터셋의 DFT 설정 대비' 다. 다른 설정과 섞지 말 것"]}
    import csv as _csv
    with open(out / f"bench_{a.engine}.csv", "w", newline="") as fh:
        w = _csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    print(f"\n══ {a.engine} vs DFT 라벨 · {len(rows)} 프레임 ══")
    print(f"  힘  MAE  {fs['mae_eVA']:.4f} eV/Å   RMSE {fs['rmse_eVA']:.4f}   최대 {fs['max_abs_eVA']:.3f}")
    print(f"      참조 RMS {fs['rms_ref_eVA']:.3f} eV/Å  →  **상대 {fs['rel_mae_pct']:.2f} %**   r={fs['pearson_r']:.5f}")
    sl = fs.get("softening_slope")
    if sl is not None:
        tag = ("✅ 경직/중립" if sl >= 0.995 else
               "⚠ 약한 softening" if sl >= 0.97 else "🔴 softening")
        print(f"      **softening 기울기 {sl:.4f}**  ({tag})  "
              f"— 1 보다 작으면 예측힘이 참조보다 작다(=PES 가 무르다). r 로는 안 보인다")
    print(f"  에너지  편향 {bias:+.2f} ± 산포 {scat:.2f} meV/atom  "
          f"(같은 부호 {same_sign}/{len(dE)} · 편향 제거 후 MAE {np.abs(dE-bias).mean():.2f})")
    # ── 구간 분할 — melt/quench 처럼 **프레임 번호로 영역이 갈리는** 데이터셋용 ──
    #   합산값만 보면 두 영역이 섞여, "고에너지에서 더 무른가" 를 **원리적으로 못 본다**.
    if a.split_at:
        seg = {}
        for tag, keep in (("< %d" % a.split_at, lambda f: f < a.split_at),
                          (">= %d" % a.split_at, lambda f: f >= a.split_at)):
            idx = [i for i, r in enumerate(rows) if keep(r["frame"])]
            if not idx:
                print(f"\n  ⚠ 구간 [{tag}] 에 프레임이 없다 — --split_at 을 확인하라")
                continue
            fr = np.concatenate([FR_l[i] for i in idx])
            fp = np.concatenate([FP_l[i] for i in idx])
            g = force_stats(fr, fp)
            de = np.array([rows[i]["dE_meV_per_atom"] for i in idx])
            g["n_frames"] = len(idx)
            g["energy_bias_meV_per_atom"] = float(de.mean())
            g["energy_scatter_sd"] = float(de.std())
            seg[tag] = g
        summ["segments"] = seg
        summ["split_at"] = a.split_at
        if len(seg) == 2:
            (t1, g1), (t2, g2) = list(seg.items())
            d = g2["softening_slope"] - g1["softening_slope"]
            summ["segment_softening_delta"] = d
            print(f"\n  ── 구간 분할 (frame {a.split_at} 기준) ──")
            for t, g in seg.items():
                print(f"    [{t:>10}] n={g['n_frames']:>4}  힘 MAE {g['mae_eVA']:.4f}  "
                      f"상대 {g['rel_mae_pct']:5.2f} %  **softening {g['softening_slope']:.4f}**  "
                      f"(참조 RMS {g['rms_ref_eVA']:.3f})")
            # ⛔ 부호를 해석해 주되, 크기 판정은 사람에게 남긴다
            print(f"    Δsoftening = {d:+.4f}  "
                  f"({'뒤 구간이 더 무름' if d < 0 else '뒤 구간이 더 경직' if d > 0 else '동일'})")
            print(f"    ⚠ 이 Δ 가 유의한지는 **구간별 프레임 수와 산포**를 봐야 한다 — "
                  f"이 도구는 판정하지 않는다")

    print(f"  ⛔ 에너지 절대오차 = 정확도가 아니다. **힘이 지표다.**")
    print(f"  📏 눈금: MTP 자체학습 0.073 · SevenNet-0 base 0.070 · 반응계 fine-tune 0.57 eV/Å")
    (out / f"bench_{a.engine}.json").write_text(
        json.dumps(summ, ensure_ascii=False, indent=2))
    print(f"\n✓ → {out}/bench_{a.engine}.{{json,csv}}")
    return 0


# ── 3) 합의 분석 ────────────────────────────────────────────────────────────
def load_preds(d):
    """<dir>/pred_*.npz → {engine: npz}. 최소 2개 아니면 종료."""
    d = Path(d)
    preds = {p.stem[5:]: np.load(p, allow_pickle=True) for p in sorted(d.glob("pred_*.npz"))}
    if len(preds) < 2:
        sys.exit(f"{d}: 엔진이 {len(preds)}개뿐 — 위원회는 최소 2개 필요")
    return preds


def frame_disagreement(F, names):
    """프레임별 **원자당 힘 RMS 불일치** — 쌍별 최대값을 그 프레임의 불일치로.
    ⚠ 온도 스윕 도구(committee_sweep_verdict.py)와 **같은 함수를 써야** 한다.
      복제해 두면 한쪽만 고쳐져 두 판정이 조용히 갈린다."""
    nf = F[names[0]].shape[0]
    per_frame, per_pair = np.zeros(nf), {}
    for i, x in enumerate(names):
        for y in names[i + 1:]:
            dF = F[x] - F[y]
            rms = np.sqrt((dF ** 2).sum(axis=2).mean(axis=1))   # (nframe,)
            per_pair[f"{x}|{y}"] = rms
            per_frame = np.maximum(per_frame, rms)
    return per_frame, per_pair


def force_scale(F, names, mask=None):
    """이 표본의 **평균 힘 크기**(eV/Å). 절대 불일치를 이걸로 나눠야 온도 간 비교가 된다.
    조화 고체에서 RMS 힘 ∝ √T 라 정규화 없이는 고온이 항상 더 나빠 보인다."""
    out = []
    for k in names:
        f = F[k] if mask is None else F[k][:, mask, :]
        out.append(float(np.sqrt((f ** 2).sum(axis=2)).mean()))
    return float(np.mean(out))


def cmd_analyze(a):
    d = Path(a.dir)
    preds = load_preds(d)
    names = sorted(preds)
    F = {k: preds[k]["forces"] for k in names}           # (nframe, natom, 3)
    nf = F[names[0]].shape[0]
    per_frame, per_pair = frame_disagreement(F, names)

    # ── 문턱 ────────────────────────────────────────────────────────────
    # ⚠ **같은 표본에서 뽑은 백분위를 그 표본에 적용하면 정보가 0이다** (p95 초과는 정의상 5%).
    #    그래서 이 도구는 두 모드로 동작한다:
    #      (a) --baseline 없음 → **교정 모드**. 이 표본의 분포를 기준선으로 *저장*만 하고
    #          "초과 몇 개" 를 결과로 주장하지 않는다.
    #      (b) --baseline <json> → **탐지 모드**. 다른(평형 벌크) 표본에서 잡은 기준선을
    #          이 표본에 적용해 초과를 센다. 이때의 초과가 비로소 정보다.
    #    문턱 정의는 kim2026 의 gamma_select/gamma_break 논리(선별/중단 분리)만 차용.
    med = float(np.median(per_frame))
    if a.baseline:
        base = json.loads(Path(a.baseline).read_text())
        bd = base["committee_frame_disagreement"]
        sel, brk = bd["threshold_select"], bd["threshold_break"]
        mode = f"탐지 (기준선: {Path(a.baseline).name})"
    else:
        sel = 2.0 * med
        brk = float(np.percentile(per_frame, 95))
        mode = "교정 (이 표본이 기준선 — 초과 개수는 정의상 자명하므로 결과로 주장하지 않음)"

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
        # ⚠ 절대 RMS 는 **힘 크기를 따라간다** — P 는 PS4 중심이라 힘이 크고 Li 는 느슨해 작다.
        #    정규화 없이 원소 순위를 해석하면 "결합이 센 원소가 불확실하다" 는 동어반복이 된다.
        mag = force_scale(F, names, m)
        by_el[el] = {"abs_eV_per_A": float(np.mean(vals)),
                     "typical_force_eV_per_A": mag,
                     "relative": float(np.mean(vals) / mag) if mag > 1e-9 else None}

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
            "⚠_circularity": (None if a.baseline else
                "**교정 모드에서는 초과 개수가 정보가 아니다** — break=p95 이므로 초과는 "
                "정의상 표본의 5%다. 이 값들은 다른 표본에 적용할 **기준선**으로만 쓴다."),
        },
        "mode": mode,
        "by_element": by_el,
        "by_element_note": ("abs = 힘 RMS 불일치(eV/Å) · typical = 그 원소의 평균 힘 크기 · "
                            "**relative = abs/typical 이 해석해야 할 값**이다. 절대값만 보면 "
                            "결합이 센 원소가 항상 위로 와서 동어반복이 된다."),
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
        "verdict": (
            (f"**교정 완료** — 이 표본(중앙 {med:.4f} eV/Å)을 기준선으로 저장했다. "
             f"이후 다른 표본을 `--baseline` 으로 이 파일을 걸어 평가하라.")
            if not a.baseline else
            ("합의 영역 밖 프레임 없음 — 기준선 대비 이상 없음."
             if (per_frame > brk).sum() == 0 else
             f"**{int((per_frame > brk).sum())}/{nf} 프레임이 기준선 중단 문턱 초과** — "
             "해당 구간 결과는 신뢰구간 밖으로 표시할 것.")),
    }
    (d / "committee_verdict.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")

    print("=" * 70)
    print(f"엔진 {len(names)}종: {', '.join(names)} · 프레임 {nf}")
    for k, v in out["per_pair_force_rms_eV_per_A"].items():
        print(f"  {k:22s} 중앙 {v['median']:.4f}  p95 {v['p95']:.4f}  max {v['max']:.4f} eV/Å")
    c = out["committee_frame_disagreement"]
    print(f"\n  모드: {mode}")
    print(f"  위원회 불일치: 중앙 {c['median']:.4f} · p95 {c['p95']:.4f} · max {c['max']:.4f}")
    print(f"  select({sel:.4f}) 초과 {c['n_above_select']} · break({brk:.4f}) 초과 {c['n_above_break']}")
    if not a.baseline:
        print("  ⚠ 교정 모드 — 위 초과 개수는 정의상 자명하므로 결과가 아니다")
    print("\n  원소별 (abs / 평균힘 / **상대**):")
    for el, v in sorted(by_el.items(), key=lambda kv: -(kv[1]["relative"] or 0)):
        r = f"{v['relative']:.3f}" if v["relative"] is not None else "—"
        print(f"    {el:3s} {v['abs_eV_per_A']:.4f} / {v['typical_force_eV_per_A']:.4f} / **{r}**")
    print("=" * 70)
    print(f"→ {d/'committee_verdict.json'}")


def _detect_layers(names):
    """모듈 이름 목록 → (층 수|None, 패턴별 후보). engine_info 가 쓰는 순수 함수.

    분리해 둔 이유: 모델을 띄우지 않고도 이름 규칙을 시험할 수 있어야 한다.
    """
    import re
    cands = {}
    for pat in (r"(?:^|\.)blocks\.(\d+)(?:\.|$)", r"(?:^|\.)layers\.(\d+)(?:\.|$)",
                r"(?:^|\.)interactions\.(\d+)(?:\.|$)", r"(?:^|\.)(\d+)_convolution",
                r"(?:^|\.)(\d+)_self_interaction", r"(?:^|\.)messages\.(\d+)(?:\.|$)"):
        idx = {int(m.group(1)) for n in names for m in [re.search(pat, n)] if m}
        if idx:
            cands[pat] = max(idx) + 1
    return (max(cands.values()) if cands else None), cands


def cmd_selftest(a=None):
    bad = []
    def chk(c, msg):
        print(("  ✓ " if c else "  ✗ ") + msg)
        if not c:
            bad.append(msg)

    # SevenNet-0 실측 이름 (2026-08-26 checkpoint_best.pth pickle 에서 뽑은 실제 형태)
    n7 = [f"{i}_self_interaction_1" for i in range(5)] + \
         [f"{i}_self_connection_intro.linear" for i in range(5)] + ["edge_embedding.spherical"]
    k, c = _detect_layers(n7)
    chk(k == 5, f"★ SevenNet 이름 규칙에서 5층을 읽는다 (실측 = SevenNet-0 사양) — 얻은 값 {k}")

    chk(_detect_layers(["blocks.0.x", "blocks.1.x", "blocks.2.x"])[0] == 3,
        "blocks.N 규칙")
    chk(_detect_layers(["interactions.0", "interactions.1"])[0] == 2, "interactions.N 규칙")
    chk(_detect_layers(["layers.0.a", "layers.11.a"])[0] == 12,
        "인덱스가 10 이상이어도 센다 (문자열 정렬 함정 회피)")

    # ── 음성 경로 ──
    chk(_detect_layers(["embedding", "readout", "scale_shift"])[0] is None,
        "★ [음성] 반복 블록이 없으면 None — **0 이나 1 을 지어내지 않는다**")
    chk(_detect_layers([])[0] is None, "[음성] 빈 목록도 None")
    chk(_detect_layers(["conv2d.0.weight", "blocks2.0"])[0] is None,
        "★ [음성] 비슷하게 생긴 이름(blocks2)에 속지 않는다")

    # 유효 수용영역 산술 — 값이 하나라도 없으면 계산하지 않는다
    for cut, lay, want in ((6.0, 5, 30.0), (None, 5, None), (6.0, None, None)):
        got = (cut * lay) if (cut and lay) else None
        chk(got == want, f"수용영역 {cut} × {lay} → {want}")

    # ── force_stats (bench) ──
    ref = np.array([[1.0, -2.0, 0.5], [0.0, 3.0, -1.0]])
    fs0 = force_stats(ref, ref.copy())
    chk(fs0["mae_eVA"] == 0.0 and fs0["rel_mae_pct"] == 0.0,
        "★ 완전 일치면 힘 MAE 0 · 상대오차 0")
    chk(abs(fs0["pearson_r"] - 1.0) < 1e-12, "완전 일치면 r = 1")
    fs1 = force_stats(ref, ref + 0.1)
    chk(abs(fs1["mae_eVA"] - 0.1) < 1e-12, "일정 편차 0.1 → MAE 0.1")
    chk(abs(fs1["rms_ref_eVA"] - float(np.sqrt((ref**2).mean()))) < 1e-12,
        "★ 참조 RMS 로 정규화한다 (Shapeev 2016 관례 — 절대 eV/Å 만으로는 계 간 비교 불가)")
    fsn = force_stats(ref, -ref)
    chk(fsn["pearson_r"] < -0.99,
        "★ [음성] 부호가 뒤집히면 r 이 음수 — MAE 만 보면 못 잡는 고장")
    chk(abs(fs0["softening_slope"] - 1.0) < 1e-12, "완전 일치면 softening 기울기 1")
    fs_soft = force_stats(ref, ref * 0.5)
    chk(abs(fs_soft["softening_slope"] - 0.5) < 1e-12,
        "★ 힘을 절반으로 줄이면 기울기 0.5 — **이게 softening 이다**")
    chk(abs(fs_soft["pearson_r"] - 1.0) < 1e-12,
        "★ [음성] 그런데 **r 은 여전히 1** — r 로는 softening 을 원리적으로 못 본다")

    # ── 스트리밍 (bench) ──
    import tempfile as _tf
    from ase import Atoms
    from ase.io import write as _w
    from ase.calculators.singlepoint import SinglePointCalculator as _SP
    with _tf.TemporaryDirectory() as td:
        fp = Path(td) / "t.xyz"
        frames = []
        for i in range(10):
            at = Atoms("H2", positions=[[0, 0, 0], [0, 0, 0.8 + 0.01 * i]], cell=[8, 8, 8], pbc=True)
            at.calc = _SP(at, energy=-1.0 * i, forces=np.zeros((2, 3)))
            frames.append(at)
        _w(str(fp), frames, format="extxyz")
        got = [i for i, _ in stream_labeled(fp, 3)]
        chk(got == [0, 3, 6, 9], f"stride 3 이면 0,3,6,9 (얻음 {got})")
        chk([i for i, _ in stream_labeled(fp, 1, limit=4)] == [0, 1, 2, 3], "limit 이 듣는다")
        chk(len([1 for _ in stream_labeled(fp, 100)]) == 1,
            "★ stride 가 총수보다 커도 최소 1프레임 (0 프레임으로 조용히 끝나지 않는다)")

    print(f"selftest {'PASS' if not bad else 'FAIL'} — {8 + 3 + 8 + 3 - len(bad)} ok, {len(bad)} bad")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample"); s.add_argument("--traj", required=True)
    s.add_argument("-n", type=int, default=200); s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_sample)
    p = sub.add_parser("predict"); p.add_argument("--dir", required=True)
    p.add_argument("--engine", required=True, choices=["uma", "mace", "sevennet"])
    p.add_argument("--device", default="cuda"); p.set_defaults(fn=cmd_predict)
    b = sub.add_parser("bench", help="DFT 라벨 붙은 extxyz 에 엔진을 돌려 힘·에너지 대조")
    b.add_argument("--xyz", required=True); b.add_argument("--engine", default="uma",
                   choices=["uma", "mace", "sevennet"])
    b.add_argument("--stride", type=int, default=250, help="이 간격으로만 계산 (기본 250)")
    b.add_argument("--limit", type=int, default=None, help="최대 프레임 수")
    b.add_argument("--split_at", type=int, default=None,
                   help="이 프레임 번호를 기준으로 앞/뒤 구간을 **따로** 집계 "
                        "(예: li3po4 는 --split_at 25000 = melt|quench)")
    b.add_argument("--device", default="cuda"); b.add_argument("--out", required=True)
    b.set_defaults(fn=cmd_bench)
    t = sub.add_parser("selftest"); t.set_defaults(fn=cmd_selftest)
    i = sub.add_parser("info", help="엔진 배선(cutoff·층 수·유효 수용영역)")
    i.add_argument("--engines", nargs="+", default=["uma"],
                   choices=["uma", "mace", "sevennet"])
    i.add_argument("--device", default="cpu")
    i.add_argument("--out", default=None); i.set_defaults(fn=cmd_info)
    n = sub.add_parser("analyze"); n.add_argument("--dir", required=True)
    n.add_argument("--baseline", default=None,
                   help="다른 표본에서 잡은 committee_verdict.json — 주면 **탐지 모드**")
    n.set_defaults(fn=cmd_analyze)
    a = ap.parse_args()
    # ⛔ 반환값을 버리면 **실패해도 종료코드 0** 이 된다 — 스크립트에서 `&&` 로 이어붙이면
    #   실패가 성공으로 흘러간다 (2026-08-26 실측: info 가 4 를 돌려주는데 0 이 나갔다).
    return a.fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
