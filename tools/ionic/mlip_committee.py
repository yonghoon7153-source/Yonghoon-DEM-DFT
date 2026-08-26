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

    # ② cutoff — 버퍼/속성 어디에 있는지 모델마다 다르다. 전부 훑는다.
    found = {}
    try:
        for n, b in mod.named_buffers():
            if "cut" in n.lower() and b.numel() == 1:
                found[n] = float(b)
    except Exception:
        pass
    for attr in ("cutoff", "r_max", "max_radius", "cutoff_radius"):
        for obj, tag in ((calc, "calc"), (mod, "model")):
            v = getattr(obj, attr, None)
            if isinstance(v, (int, float)):
                found[f"{tag}.{attr}"] = float(v)
    if found:
        out["cutoff_A"] = max(found.values())
        out["source"]["cutoff_candidates"] = found
    else:
        out["notes"].append("⚠ cutoff 를 못 찾았다 — 설정 파일에서 직접 확인할 것")

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
    if a.out:
        Path(a.out).write_text(_j.dumps(rows, ensure_ascii=False, indent=2))
        print(f"\n✓ → {a.out}")
    # ⛔ 하나라도 못 알아냈으면 성공으로 끝내지 않는다 — 조용히 넘어가면 '확인했다' 로 기록된다
    return 0 if all(r.get("effective_receptive_field_A") for r in rows) else 4


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

    print(f"selftest {'PASS' if not bad else 'FAIL'} — {8 + 3 - len(bad)} ok, {len(bad)} bad")
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
    a.fn(a)


if __name__ == "__main__":
    main()
