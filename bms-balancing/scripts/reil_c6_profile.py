"""REIL C6 — 판 · 환경 고정의 측정 · 봉인 (`docs/REIL_PREREQUISITES_STATUS_20261004.md` §8-2). 버리는 venv 의 python 으로 실행한다.

    <venv>/bin/python bms-balancing/scripts/reil_c6_profile.py emit  <out_dir>   # 측정 → 봉인 파일 (결정적인 것만)
    <venv>/bin/python bms-balancing/scripts/reil_c6_profile.py check <out_dir>   # 같은 venv 에서 다시 만들어 바이트 대조 (다르면 rc 1)

재는 것: 판 · 플랫폼 · 설치 배포판 전부 (lock — `degradation-degeneracy/tools/env_profile.py` 의 `measure()` 를 venv 의 site-packages 에만) ·
NumPy · SciPy 의 빌드 의존성 (BLAS · LAPACK) · COBYQA 옵션 8 개 (부속 A §3-1) 의 이름 · 설명과 실제 전달 (합성 이차 함수 하나 — REIL 자료
아님) · Sobol Phase A 시작점 배열 (부속 A §3-2 · d = 4 · 64 점 · seed 0 · 1 · 단위 입방체와 상자 둘) 의 sha256 식별 · seed 인자 이름
(rng= · 옛 seed= 가 같은 배열을 내는지).

재지 않는 것: REIL xlsx · pkl · 노트북 · P0 · 맞춤 · max_q 에 기대는 배열 · label seed 배열 (부속 A §3-6 · 부속 B §2-1 의 둘째 시점).
봉인 파일에 시각 · 커널 판 · CPU 런타임 특성 · 해 x 의 비트는 넣지 않는다 (같은 판의 다른 기계에서도 같아야 하는 것만 봉인한다).
"""
from __future__ import annotations

import filecmp
import hashlib
import importlib.metadata as md
import importlib.util
import inspect
import json
import platform
import sys
import tempfile
import warnings
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ENV_PROFILE = REPO / "degradation-degeneracy" / "tools" / "env_profile.py"

#: 부속 A §3-1 — 판 기본값에 기대지 않고 모두 명시해 전달한다
COBYQA_OPTIONS = {"maxfev": 2000, "maxiter": 4000, "f_target": float("-inf"), "feasibility_tol": 1e-12,
                  "scale": True, "initial_tr_radius": 1.0, "final_tr_radius": 1e-6, "disp": False}
#: x = (m_P, m_N, d_P, d_N) — A0 = 그들 상자 (v2 §1-1) · A1 · A2 = 넓힌 상자 (v2 §4-1)
BOXES = {"A0_their_box": ([0.6, 0.5, 0.005, 0.0], [1.1, 1.1, 0.5, 1.0]),
         "A1_A2_wide_box": ([0.3, 0.3, -0.5, -0.5], [1.5, 1.5, 1.5, 1.5])}
SOBOL_D, SOBOL_M, SOBOL_SEEDS = 4, 6, (0, 1)          # 2**6 = 64 점 (부속 A §3-2)
PACKAGES = ("numpy", "scipy", "pandas", "openpyxl", "matplotlib", "seaborn", "pymoo")
FILES = ("REIL_C6.lock.txt", "PROFILE.json", "COBYQA_OPTIONS.json", "SOBOL_PHASE_A.json")
#: 봉인 밖 사람용 기록 (시각 · 커널 판이 들어 결정적이지 않다) — MANIFEST 에 넣지 않고 check 도 대조하지 않는다. 그 밖의 파일은 전부 대조한다
HUMAN_RECORDS = ("README.md", "C6_RUN.log")


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n"


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _site_packages() -> list[str]:
    if sys.prefix == sys.base_prefix:
        raise SystemExit("venv 밖이다 — 버리는 venv 의 python 으로만 실행한다 (운영 환경을 재지 않는다)")
    sp = [p for p in sys.path if p.startswith(sys.prefix) and p.endswith("site-packages")]
    if len(sp) != 1:
        raise SystemExit(f"venv site-packages 를 하나로 정하지 못했다: {sp}")
    return sp


def record_index(paths, normalize) -> dict:
    """배포판마다 RECORD 의 {경로: 해시} — 같은 경로를 여러 배포판이 주장하는지 보려고."""
    import csv
    index = {}
    for dist in md.distributions(path=paths):
        rows = csv.reader((dist.read_text("RECORD") or "").splitlines())
        index[normalize(dist.metadata["Name"])] = {r[0]: r[1] for r in rows if len(r) >= 2 and r[1]}
    return index


def classify_record_mismatches(mismatches, index) -> tuple[list, list]:
    """RECORD 불일치를 둘로 — '설명된 충돌' (site-packages 밖의 경로를 다른 배포판도 주장하고 디스크 바이트가 그쪽 RECORD 와 같다 = 설치
    순서로 덮어쓴 것) 은 기록하고 통과, 그 밖은 전부 fatal (봉인 거부). 2026-10-05 첫 emit 의 about-time · alive_progress LICENSE 충돌에서."""
    fatal, collisions = [], []
    for name, rel, want, got in mismatches:
        others = sorted(n for n, rows in index.items() if n != name and rel in rows)
        disk = [n for n in others if index[n][rel] == got]
        if rel.startswith("../") and disk:
            collisions.append({"path": rel, "dist": name, "claimed_by": sorted([name, *others]), "disk_matches": disk[0]})
        else:
            fatal.append((name, rel, want, got))
    return fatal, collisions


def lock_text() -> str:
    spec = importlib.util.spec_from_file_location("reil_c6_env_profile", ENV_PROFILE)
    ep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ep)
    paths = _site_packages()
    prof = ep.measure(paths=paths)
    bad, collisions = classify_record_mismatches(prof["files"]["mismatches"], record_index(paths, ep.normalize))
    if bad or prof["shadowed"]:
        raise SystemExit(f"설치 파일 RECORD 불일치 (설명 안 됨) {bad} · 가려진 배포판 {prof['shadowed']} — 봉인하지 않는다")
    head = ["# REIL C6 lock — 버리는 venv 의 site-packages 만 (degradation-degeneracy/tools/env_profile.py measure() · 그 파일 sha256 "
            + _sha(ENV_PROFILE.read_bytes()) + ")",
            "# 이름==판 · RECORD 파일의 sha256 · 설치 파일은 RECORD 와 전부 대조했다 (아래 files · 설명된 충돌만 collision 줄로)",
            f'#@ profile "REIL-C6"']
    head += [f"#@ {k} {json.dumps(prof[k], ensure_ascii=False)}" for k in ("python", "implementation", "system", "machine", "libc")]
    head += [f"#@ files {json.dumps({'verified': prof['files']['verified'], 'unhashed': prof['files']['unhashed'], 'mismatches': len(prof['files']['mismatches']), 'explained_collisions': len(collisions)})}"]
    head += [f"#@ collision {json.dumps(c, ensure_ascii=False, sort_keys=True)}" for c in collisions]
    head += [f"#@ dists_without_record {json.dumps(prof['dists_without_record'])}", ""]
    body = [f"{n}=={d['version']}  # record-sha256 {d['record']}" for n, d in sorted(prof["dists"].items())]
    return "\n".join(head + body) + "\n"


def profile() -> dict:
    import numpy as np
    import scipy
    import scipy._lib.cobyqa as cobyqa
    np_cfg = np.show_config(mode="dicts")
    sp_cfg = scipy.show_config(mode="dicts")
    return {
        "python": {"version": platform.python_version(), "implementation": platform.python_implementation(), "build": list(platform.python_build())},
        "platform": {"system": platform.system(), "machine": platform.machine(), "libc": " ".join(platform.libc_ver()).strip()},
        "packages": {p: md.version(p) for p in PACKAGES},
        "build_dependencies": {"numpy": np_cfg.get("Build Dependencies"), "scipy": sp_cfg.get("Build Dependencies")},
        "cobyqa_implementation": {"module": cobyqa.__name__, "version": getattr(cobyqa, "__version__", None)},
    }


def cobyqa_options() -> dict:
    import numpy as np
    from scipy.optimize import Bounds, minimize, show_options
    import scipy
    text = show_options("minimize", "cobyqa", disp=False)
    lines = text.splitlines()
    table = {}
    for name, value in COBYQA_OPTIONS.items():
        hit = [i for i, ln in enumerate(lines) if " : " in ln and not ln.startswith(" ") and ln.split(" : ")[0].strip() == name]
        desc = []
        if hit:
            for ln in lines[hit[0] + 1:]:
                if not ln.startswith(" "):
                    break
                desc.append(ln.strip())
        table[name] = {"planned": repr(value), "documented": bool(hit), "type": lines[hit[0]].split(" : ", 1)[1].strip() if hit else None,
                       "description": " ".join(desc) or None}
    impl = Path(scipy.__file__).parent / "_lib" / "cobyqa"
    impl_files = {f"scipy/_lib/cobyqa/{n}": _sha((impl / n).read_bytes()) for n in ("main.py", "problem.py", "framework.py", "settings.py")}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        res = minimize(lambda x: float(np.sum((x - 0.3) ** 2)), np.full(4, 0.9), method="COBYQA",
                       bounds=Bounds([0.0] * 4, [1.0] * 4), options=dict(COBYQA_OPTIONS))
    messages = sorted({f"{w.category.__name__}: {w.message}" for w in caught})
    unknown = [m for m in messages if "Unknown solver options" in m]
    return {
        "options": table,
        "implementation_files_sha256": impl_files,
        "all_documented": all(v["documented"] for v in table.values()),
        "synthetic_call": {"function": "sum((x - 0.3)**2) · x0 = 0.9 × 4 · bounds [0, 1]^4 (REIL 자료 아님)",
                           "warnings": messages, "unknown_option_warnings": unknown, "success": bool(res.success),
                           "x_within_1e-6_of_0.3": bool(np.all(np.abs(res.x - 0.3) <= 1e-6))},
        "accepted": all(v["documented"] for v in table.values()) and not unknown and bool(res.success),
    }


def sobol(out: Path) -> dict:
    import numpy as np
    from scipy.stats import qmc
    params = inspect.signature(qmc.Sobol).parameters
    kw = "rng" if "rng" in params else "seed"
    arrays, warn = {}, []
    for seed in SOBOL_SEEDS:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            unit = qmc.Sobol(d=SOBOL_D, scramble=True, **{kw: seed}).random_base2(m=SOBOL_M)
        warn += [f"{w.category.__name__}: {w.message}" for w in caught]
        arrays[f"unit_seed{seed}"] = unit
        for box, (lo, hi) in BOXES.items():
            arrays[f"{box}_seed{seed}"] = qmc.scale(unit, lo, hi)
    # 부속 A §3-1 "판에 따라 seed 인자 이름과 생성 배열이 다를 수 있으므로" — 옛 이름 seed= 가 같은 정수로 같은 배열을 내는지 (1.17.1: 아니다 · 경고 없음)
    legacy = {}
    if kw == "rng" and "seed" in params:
        for seed in SOBOL_SEEDS:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                old = qmc.Sobol(d=SOBOL_D, scramble=True, seed=seed).random_base2(m=SOBOL_M)
            gen = qmc.Sobol(d=SOBOL_D, scramble=True, rng=np.random.default_rng(seed)).random_base2(m=SOBOL_M)
            legacy[f"seed{seed}"] = {"seed_keyword_same_array_as_rng": bool(np.array_equal(old, arrays[f"unit_seed{seed}"])),
                                     "seed_keyword_warnings": sorted({f"{w.category.__name__}: {w.message}" for w in caught}),
                                     "rng_default_rng_same_array_as_rng_int": bool(np.array_equal(gen, arrays[f"unit_seed{seed}"]))}
    rec = {}
    for name, a in sorted(arrays.items()):
        a = np.ascontiguousarray(a, dtype="<f8")
        np.save(out / f"sobol_{name}.npy", a, allow_pickle=False)
        rec[name] = {"shape": list(a.shape), "raw_float64_le_sha256": _sha(a.tobytes()),
                     "npy_sha256": _sha((out / f"sobol_{name}.npy").read_bytes())}
    return {"call": f"scipy.stats.qmc.Sobol(d={SOBOL_D}, scramble=True, {kw}=<seed>).random_base2(m={SOBOL_M})",
            "seed_keyword": kw, "signature": str(inspect.signature(qmc.Sobol)), "boxes": BOXES,
            "warnings": sorted(set(warn)), "arrays": rec, "legacy_seed_keyword": legacy,
            "seal_note": "식별 — 정식 봉인은 부속 B §2-1 의 '맞춤 전 (P0 뒤 · 첫 지역 실행 전)' 에 같은 판에서 다시 만들어 이 sha256 과 대조"}


def emit(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        raise SystemExit(f"{out} 가 비어 있지 않다 — emit 은 빈 디렉터리에만 쓴다 (봉인을 덮어쓰지 않는다 · 다시 대조는 check)")
    (out / "REIL_C6.lock.txt").write_text(lock_text(), encoding="utf-8")
    (out / "PROFILE.json").write_text(_dump(profile()), encoding="utf-8")
    cob = cobyqa_options()
    (out / "COBYQA_OPTIONS.json").write_text(_dump(cob), encoding="utf-8")
    if not cob["accepted"]:   # 실패 기록은 남기고 Sobol · MANIFEST 는 쓰지 않는다 (완결된 봉인처럼 보이지 않게)
        raise SystemExit("COBYQA 옵션 대조 실패 — 부속 A §3-1 의 fail-closed: 실행하지 않고 표를 새 등록으로 고친다")
    (out / "SOBOL_PHASE_A.json").write_text(_dump(sobol(out)), encoding="utf-8")
    names = sorted(p.name for p in out.iterdir() if p.is_file() and p.name != "MANIFEST.json")
    (out / "MANIFEST.json").write_text(_dump({n: _sha((out / n).read_bytes()) for n in names}), encoding="utf-8")


def check(sealed: Path) -> int:
    man = json.loads((sealed / "MANIFEST.json").read_text(encoding="utf-8"))
    bad = [n for n, h in man.items() if not (sealed / n).is_file() or _sha((sealed / n).read_bytes()) != h]
    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / "fresh"
        emit(fresh)
        # MANIFEST.json 도 대조 (항목을 뺀 MANIFEST 를 잡는다) · 봉인 쪽에만 있는 파일도 대조 대상 (fresh 에 없으니 다름)
        names = sorted((set(man) | {p.name for p in fresh.iterdir()} | {p.name for p in sealed.iterdir()}) - set(HUMAN_RECORDS))
        bad += [n for n in names if not (sealed / n).is_file() or not (fresh / n).is_file()
                or not filecmp.cmp(sealed / n, fresh / n, shallow=False)]
    for n in sorted(set(bad)):
        print("다름:", n)
    print("check", "OK" if not bad else f"FAIL ({len(set(bad))})")
    return 0 if not bad else 1


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("emit", "check"):
        raise SystemExit(__doc__)
    if sys.argv[1] == "emit":
        emit(Path(sys.argv[2]))
        print("emit OK", sys.argv[2])
    else:
        sys.exit(check(Path(sys.argv[2])))
