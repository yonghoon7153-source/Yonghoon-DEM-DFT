"""archive_bundle.py — 산출물을 **외부 clone에서 검증 가능한** 묶음으로 만든다.

★ F62 — 6차 교차리뷰

왜 필요한가
───────────
`validate_provenance()` 는 기록끼리의 자기일관성이 아니라 **디스크의 실물**을
본다 (F56~F58):

  · `manifest_start.yaml`, `attempts/manifest_start_<attempt_id>.yaml` 를 읽어
    manifest 안의 `start_provenance` 와 대조하고,
  · `input_sha256` 에 적힌 **모든 입력 파일을 다시 해시**한다.

그런데 `archive_results.sh` 초판은 `fits.parquet` · `manifest.yaml` · 요약만
복사했다. `curves.parquet` 은 "재생성 5~8분"이라 버렸고, half-cell 캐시
(`.cache/halfcell/*_ocp.json`) 는 `.gitignore` 에 걸려 애초에 저장소에 없으며,
`manifest_start.yaml` 과 `attempts/` 는 존재조차 몰랐다.

결과: **저장소를 clone 한 사람은 보관된 결과를 검증할 수 없다.** 검증기를 세
라운드에 걸쳐 강화해 놓고, 정작 남기는 묶음은 그 검증을 통과할 수 없는 상태였다.
게다가 재생성으로 때울 수도 없다 — curves를 다시 만들면 파일 바이트가 달라져
`입력_digest_재해시` 가 깨진다. digest는 "같은 내용"이 아니라 "같은 파일"을 요구한다.

무엇을 하는가
─────────────
  bundle   run_dir → artifacts/<name>/ 로 검증에 필요한 것을 전부 복사하고,
           run_dir 바깥의 봉인 입력(half-cell 캐시 등)은 `inputs/` 에 넣은 뒤
           원래 경로를 `restore_map.yaml` 에 적는다.
  check    묶음이 검증에 필요한 파일을 다 갖췄는지 본다 (해시 검사 아님).
  restore  묶음을 원래 경로로 되돌린다. 그 뒤 validate_provenance 가 통과한다.

경로에 관하여
─────────────
`input_sha256` 의 키는 실행 당시의 **저장소 root 기준 상대경로**
(`results/halfcell_v3/curves.parquet`, `configs/base.yaml`,
`.cache/halfcell/<hash>_ocp.json`)다. 검증기는 이 경로를 그대로 다시 해시하므로,
묶음을 `artifacts/` 아래 평평하게 놓기만 해선 통과할 수 없다. 그래서 복원이
필요하다 — 묶음은 보관용이고, 검증은 복원 후에 한다.

사용:
    python -m tools.archive_bundle bundle  results/halfcell_v3 artifacts/halfcell_v3
    python -m tools.archive_bundle check   artifacts/halfcell_v3
    python -m tools.archive_bundle restore artifacts/halfcell_v3
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

#: run_dir 안에서 **검증에 필요한** 파일. 하나라도 빠지면 validate_provenance가 깨진다.
REQUIRED_RUN_FILES = ("manifest.yaml", "manifest_start.yaml", "fits.parquet")

#: 검증에는 안 쓰이지만 재생성 비용이 커서 같이 남기는 것들
KEEP_FILES = ("degeneracy_summary.yaml", "objective_comparison.yaml",
              "objective_comparison.csv", "objective_comparison_by_noise.csv",
              "case_comparison.yaml", "weight_sweep.yaml", "weight_sweep_summary.csv")

RESTORE_MAP = "restore_map.yaml"


def _rel(p: Path) -> str:
    """저장소 root 기준 상대경로 문자열 (밖이면 절대경로 그대로)."""
    try:
        return str(Path(p).resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(Path(p).resolve())


def sealed_inputs(run_dir: Path) -> dict[str, str]:
    """manifest에 봉인된 입력 경로 → digest."""
    mp = Path(run_dir) / "manifest.yaml"
    if not mp.exists():
        return {}
    man = yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
    return dict(man.get("input_sha256") or {})


def _attempt_files(run_dir: Path) -> list[Path]:
    d = Path(run_dir) / "attempts"
    return sorted(d.glob("manifest_start_*.yaml")) if d.is_dir() else []


def bundle(run_dir, out_dir) -> dict:
    """run_dir 를 out_dir 로 묶는다. 반환: {"copied": n, "external": [...], "missing": [...]}"""
    run_dir, out_dir = Path(run_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    copied, missing = 0, []

    # ── 검증 필수 + 보관 대상 ──
    #   curves.parquet 은 19 MB지만 **재생성으로 대체할 수 없다** (바이트가 달라진다).
    for name in (*REQUIRED_RUN_FILES, "curves.parquet", *KEEP_FILES):
        src = run_dir / name
        if src.is_file():
            shutil.copy2(src, out_dir / name)
            copied += 1
        elif name in REQUIRED_RUN_FILES:
            missing.append(name)

    # ── attempts/ — F57이 attempt_id 별 파일을 실제로 읽는다 ──
    atts = _attempt_files(run_dir)
    if atts:
        (out_dir / "attempts").mkdir(exist_ok=True)
        for a in atts:
            shutil.copy2(a, out_dir / "attempts" / a.name)
            copied += 1

    for pat in ("hessian_*.parquet",):
        for f in sorted(run_dir.glob(pat)):
            shutil.copy2(f, out_dir / f.name)
            copied += 1

    for sub in ("figures", "wsweep"):
        s = run_dir / sub
        if not s.is_dir():
            continue
        (out_dir / sub).mkdir(exist_ok=True)
        pats = ("*.png",) if sub == "figures" else ("weight_sweep*.yaml",
                                                    "weight_sweep*.csv", "fits.parquet")
        for pat in pats:
            for f in sorted(s.glob(pat)):
                shutil.copy2(f, out_dir / sub / f.name)
                copied += 1

    # ── run_dir 바깥의 봉인 입력 ──
    #   configs/base.yaml 은 git이 추적하므로 clone에 이미 있다. 그러나 half-cell
    #   캐시는 .gitignore(.cache/) 에 걸려 저장소에 없다 — 이게 빠지면 검증 불가.
    inputs_map: dict[str, str] = {}
    external = []
    for path_s in sealed_inputs(run_dir):
        p = Path(path_s)
        if not p.is_absolute():
            p = REPO_ROOT / p
        try:
            inner = Path(p).resolve().relative_to(run_dir.resolve())
        except ValueError:
            inner = None
        if inner is not None:                   # run_dir 안 — 이름 그대로 동봉
            dst = out_dir / inner
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dst)
                copied += 1
            continue
        if not p.exists():
            missing.append(f"{path_s} (봉인 입력이 디스크에 없다)")
            continue
        rel = _rel(p)
        if (REPO_ROOT / rel).exists() and _tracked_by_git(rel):
            continue                            # clone에 이미 있다
        dst = out_dir / "inputs" / Path(rel).name
        dst.parent.mkdir(exist_ok=True)
        shutil.copy2(p, dst)
        inputs_map[str(Path("inputs") / dst.name)] = rel
        external.append(rel)
        copied += 1

    (out_dir / RESTORE_MAP).write_text(yaml.safe_dump(
        {"run_dir": _rel(run_dir), "inputs": inputs_map},
        allow_unicode=True, sort_keys=False), encoding="utf-8")
    return {"copied": copied, "external": external, "missing": missing}


def _tracked_by_git(rel: str) -> bool:
    import subprocess
    try:
        r = subprocess.run(["git", "ls-files", "--error-unmatch", rel],
                           cwd=REPO_ROOT, capture_output=True, text=True)
        return r.returncode == 0
    except OSError:
        return False


def check(bundle_dir) -> dict:
    """묶음이 검증에 필요한 파일을 다 가졌는지 (해시가 아니라 **존재**를 본다)."""
    b = Path(bundle_dir)
    missing = [n for n in REQUIRED_RUN_FILES if not (b / n).is_file()]

    man = {}
    mp = b / "manifest.yaml"
    if mp.is_file():
        man = yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
    aid = (man.get("start_provenance") or {}).get("attempt_id")
    if not aid:
        missing.append("manifest.start_provenance.attempt_id (F51 이전 실행)")
    elif not (b / "attempts" / f"manifest_start_{aid}.yaml").is_file():
        missing.append(f"attempts/manifest_start_{aid}.yaml")

    rmap = {}
    rp = b / RESTORE_MAP
    if rp.is_file():
        rmap = (yaml.safe_load(rp.read_text(encoding="utf-8")) or {}).get("inputs") or {}
    else:
        missing.append(RESTORE_MAP)

    run_rel = str((yaml.safe_load(rp.read_text(encoding="utf-8")) or {}).get("run_dir")
                  if rp.is_file() else "")
    for path_s in (man.get("input_sha256") or {}):
        p = Path(path_s)
        try:
            inner = p.relative_to(run_rel) if run_rel else None
        except ValueError:
            inner = None
        if inner is not None:
            if not (b / inner).is_file():
                missing.append(f"{inner} (봉인 입력)")
        elif path_s in rmap.values():
            pass                                  # inputs/ 에 들어 있다
        elif _tracked_by_git(path_s):
            pass                                  # clone에 있다
        else:
            missing.append(f"{path_s} (묶음에도 저장소에도 없다)")

    return {"ok": not missing, "missing": missing}


def restore(bundle_dir, run_dir=None, force: bool = False) -> dict:
    """묶음을 원래 경로로 되돌린다. 그 뒤라야 validate_provenance 가 통과한다."""
    b = Path(bundle_dir)
    rp = b / RESTORE_MAP
    meta = yaml.safe_load(rp.read_text(encoding="utf-8")) if rp.is_file() else {}
    meta = meta or {}
    dest = Path(run_dir) if run_dir else REPO_ROOT / str(meta.get("run_dir") or
                                                         f"results/{b.name}")
    dest.mkdir(parents=True, exist_ok=True)

    written, skipped = [], []
    for src in sorted(b.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(b)
        if rel.parts[0] == "inputs" or rel.name == RESTORE_MAP:
            continue
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() and not force:
            skipped.append(str(rel))
            continue
        shutil.copy2(src, out)
        written.append(str(rel))

    for arch_rel, orig_rel in (meta.get("inputs") or {}).items():
        src = b / arch_rel
        out = REPO_ROOT / orig_rel
        if not src.is_file():
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() and not force:
            skipped.append(orig_rel)
            continue
        shutil.copy2(src, out)
        written.append(orig_rel)

    return {"run_dir": str(dest), "written": written, "skipped": skipped}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("bundle", help="run_dir → artifacts/<name>")
    b.add_argument("run_dir")
    b.add_argument("out_dir")

    c = sub.add_parser("check", help="묶음이 검증에 필요한 파일을 다 가졌는지")
    c.add_argument("bundle_dir")

    r = sub.add_parser("restore", help="묶음을 원래 경로로 복원")
    r.add_argument("bundle_dir")
    r.add_argument("--run-dir", default=None)
    r.add_argument("--force", action="store_true", help="기존 파일을 덮어쓴다")

    a = ap.parse_args(argv)
    if a.cmd == "bundle":
        res = bundle(a.run_dir, a.out_dir)
        print(f"복사 {res['copied']}개")
        if res["external"]:
            print("  저장소 밖 입력 동봉: " + ", ".join(res["external"]))
        if res["missing"]:
            print("  ⚠ 누락: " + ", ".join(res["missing"]))
        return 0
    if a.cmd == "check":
        res = check(a.bundle_dir)
        if res["ok"]:
            print("검증 가능: 필요한 파일이 모두 있다")
            return 0
        print("검증 불가 — 누락:")
        for m in res["missing"]:
            print(f"  · {m}")
        return 1
    res = restore(a.bundle_dir, a.run_dir, a.force)
    print(f"복원 → {res['run_dir']}  (쓴 파일 {len(res['written'])}개"
          + (f", 이미 있어 건너뜀 {len(res['skipped'])}개" if res["skipped"] else "") + ")")
    print("이제 검증할 수 있다:\n  python -c \"from src.io import validate_provenance;"
          f" import json; print(json.dumps(validate_provenance('{res['run_dir']}'),"
          " ensure_ascii=False, indent=2))\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
