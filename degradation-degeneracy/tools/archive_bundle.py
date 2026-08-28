"""archive_bundle.py — 산출물을 **외부 clone에서 검증 가능한** 묶음으로 만든다.

★ F62 (6차) → ★ F71 (7차 게이트 리뷰 발견 8)

왜 필요한가
───────────
`validate_provenance()` 는 기록끼리의 자기일관성이 아니라 **디스크의 실물**을
본다 (F56~F58, F68, F70): 시작/시도 manifest 를 읽어 대조하고, 봉인된 입력을
전부 다시 해시하고, fits 를 다시 해시한다.

그런데 `archive_results.sh` 초판은 `fits.parquet` · `manifest.yaml` · 요약만
복사했다. `curves.parquet` 은 "재생성 5~8분"이라 버렸는데 — 재생성하면 바이트가
달라져 digest 가 깨진다. **재생성으로 대체할 수 없다.**

F62 가 그걸 고쳤지만 7차 리뷰가 시스템 수준의 구멍 여섯 개를 더 찾았다.

  8-1 half-cell 절대경로가 다른 clone 에서 복원되지 않는다   → F65 로 해결
  8-2 nested sweep 의 provenance 가 묶음에서 사라진다
  8-3 restore 가 기존 파일을 **바이트 비교 없이** 건너뛴다
  8-4 stale bundle 이 남고, missing 이 있어도 exit 0 이다
  8-5 git tracked 입력도 OS 별로 raw byte 가 달라진다 (CRLF)
  8-6 restore_map 의 절대경로·`..` 를 막지 않는다 (저장소 밖에 파일을 쓴다)

이번 판의 원칙
──────────────
  · **fail-closed** — 하나라도 어긋나면 nonzero 로 끝난다
  · **모든 봉인 입력의 exact bytes 를 담는다** — tracked YAML 도 예외 없이 (8-5)
  · **empty staging + 원자적 교체** — 옛 묶음의 잔재가 남지 않는다 (8-4)
  · **payload digest 목록** — bundle/check/restore 가 매번 재해시한다
  · **복원 대상은 비어 있거나 바이트 동일해야 한다** (8-3)
  · **restore 경로는 허용 root 안이어야 한다** (8-6)

경로에 관하여
─────────────
`input_sha256` 의 키는 저장소 root 기준 상대경로다 (F65). 검증기는 이 경로를
그대로 다시 해시하므로, 묶음을 `artifacts/` 아래 평평하게 놓기만 해선 통과할 수
없다. 그래서 복원이 필요하다 — 묶음은 보관용이고, 검증은 복원 후에 한다.

사용:
    python -m tools.archive_bundle bundle  results/halfcell_fit_v3 artifacts/halfcell_fit_v3
    python -m tools.archive_bundle check   artifacts/halfcell_fit_v3
    python -m tools.archive_bundle restore artifacts/halfcell_fit_v3 --run-dir /tmp/iso/run
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

#: ★ F80/9-e — 곡선 producer 는 fitting artifact 가 아니다. fits·manifest_start
#: 를 요구하면 **정상 grid artifact 도 반드시 실패**했다 (기본 대상에 grid 가
#: 있는데도). 종류를 감지해 그에 맞는 스키마를 요구한다.
REQUIRED_PRODUCER_FILES = ("manifest.yaml", "curves_manifest.yaml",
                           "curves_manifest_start.yaml", "curves.parquet")


def artifact_kind(run_dir: Path) -> str:
    """'fit' | 'grid_producer' — manifest 의 `run_type` 으로 판정한다.

    파일 유무로 판정하면 안 된다: fits.parquet 을 **지운** fit artifact 가
    producer 로 오인돼, "fits 누락" 대신 엉뚱한 스키마로 검사된다 (구현 중 실측).
    """
    mp = Path(run_dir) / "manifest.yaml"
    if mp.is_file():
        man = yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
        if str(man.get("run_type")) == "grid":
            return "grid_producer"
    return "fit"


def required_files(run_dir: Path) -> tuple:
    if artifact_kind(run_dir) == "grid_producer":
        req = REQUIRED_PRODUCER_FILES
        # ★ 10차 발견 1 — 실패가 있는 격자는 failed.csv 없이는 F83b 분할
        #   (의도 = 관측 ⊎ 실패, ID 재해시)을 복원 후 증명할 수 없다.
        #   n_failed_total>0 이면 필수로 승격한다.
        cm = Path(run_dir) / "curves_manifest.yaml"
        try:
            man = (yaml.safe_load(cm.read_text(encoding="utf-8")) or {}
                   ) if cm.is_file() else {}
        except Exception:  # noqa: BLE001 — 깨진 manifest 는 check 단계가 잡는다
            man = {}
        if man.get("n_failed_total"):
            req = (*req, "failed.csv")
        return req
    return REQUIRED_RUN_FILES

#: 검증에는 안 쓰이지만 재생성 비용이 커서 같이 남기는 것들
KEEP_FILES = ("degeneracy_summary.yaml", "objective_comparison.yaml",
              # ★ 18차 발견 6 — 파생 분석 provenance (raw 계산 manifest 와 분리)
              "analysis_manifest.yaml",
              "objective_comparison.csv", "objective_comparison_by_noise.csv",
              "objective_comparison_all_conditions.csv",
              "case_comparison.yaml", "weight_sweep.yaml", "weight_sweep_summary.csv",
              "manifest_grid.yaml", "curves_manifest.yaml", "provenance.json")

RESTORE_MAP = "restore_map.yaml"
PAYLOAD = "payload_sha256.yaml"


def _full(path) -> str | None:
    from src.io import file_digest
    return file_digest(path, full=True)


def _rel(p: Path, repo_root=None) -> str:
    """저장소 root 기준 상대경로 문자열 (밖이면 절대경로 그대로).

    ★ 10차 자체 리뷰 — **POSIX 구분자로 정규화**한다. Windows 에서 만든 묶음의
    restore_map 이 `results\\halfcell_v3` 로 적히면 Linux 에서 그 문자열이
    통째로 한 파일명이 되어 복원이 불가능했다 (payload 키는 F80/9-c 에서 이미
    고쳤는데 restore_map 은 남아 있었다).
    """
    root = Path(repo_root) if repo_root else REPO_ROOT
    try:
        return Path(p).resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return Path(p).resolve().as_posix()


def sealed_inputs(run_dir: Path) -> dict[str, str]:
    """manifest에 봉인된 입력 경로 → digest."""
    mp = Path(run_dir) / "manifest.yaml"
    if not mp.exists():
        return {}
    man = yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
    return dict(man.get("input_sha256") or {})


def nested_runs(run_dir: Path) -> list[Path]:
    """★ F71/8-2 — 자기 manifest 를 가진 하위 실행 (예: `wsweep/`).

    초판은 `wsweep/` 에서 fits 와 요약만 복사하고 manifest·start·attempts 를
    버렸다. 그래서 복원된 sweep 은 14개 검사가 실패했는데, 배너는 sweep
    provenance 를 합산하지 않아 조용히 지나갔다.
    """
    return sorted(d for d in Path(run_dir).iterdir()
                  if d.is_dir() and (d / "manifest.yaml").is_file())


def _copy_run(run_dir: Path, out_dir: Path,
              repo_root=None, inputs_root: Path | None = None
              ) -> tuple[int, list[str], dict[str, str]]:
    """한 실행(run_dir)의 검증 필수 + 보관 파일을 out_dir 로 복사.

    ★ 10차 자체 리뷰 — `inputs_root` 는 외부 봉인 입력이 놓일 위치다.
    nested 실행(wsweep)에서 out_dir(=<bundle>/wsweep) 아래 `inputs/` 에 쓰면
    restore 는 `<bundle>/inputs/` 만 읽으므로 **절대 복원되지 않는 사본**이
    된다. bundle() 이 최상위 stage 를 넘겨 한곳에 모은다.

    반환: (복사 수, 누락 목록, {archived_rel(bundle root 기준, POSIX):
    original_repo_rel})
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    copied, missing = 0, []

    #   curves.parquet 은 19 MB지만 **재생성으로 대체할 수 없다** (바이트가 달라진다).
    req = required_files(run_dir)
    for name in (*req, "curves.parquet", "curves_manifest_start.yaml", *KEEP_FILES):
        src = run_dir / name
        if src.is_file():
            if not (out_dir / name).exists():
                shutil.copy2(src, out_dir / name)
                copied += 1
        elif name in req:
            missing.append(f"{run_dir.name}/{name}")

    # attempts/ — F57이 attempt_id 별 파일을 실제로 읽는다
    att_dir = run_dir / "attempts"
    if att_dir.is_dir():
        (out_dir / "attempts").mkdir(exist_ok=True)
        for a in sorted(att_dir.glob("manifest_start_*.yaml")):
            shutil.copy2(a, out_dir / "attempts" / a.name)
            copied += 1

    for pat in ("hessian_*.parquet", "multistart*.parquet"):
        for f in sorted(run_dir.glob(pat)):
            shutil.copy2(f, out_dir / f.name)
            copied += 1

    fig = run_dir / "figures"
    if fig.is_dir():
        (out_dir / "figures").mkdir(exist_ok=True)
        for f in sorted(fig.glob("*.png")):
            shutil.copy2(f, out_dir / "figures" / f.name)
            copied += 1

    # ── run_dir 바깥의 봉인 입력 ──
    #   ★ F71/8-5 — git tracked 파일도 **뺴지 않는다**. 저장소에 EOL 정책이 없어서
    #   Windows clone(`core.autocrlf=true`)의 `configs/base.yaml` 은 LF blob(5,498 B,
    #   26fe6c7c…) 과 다른 바이트(5,620 B, 282c3727…)가 된다. validator 는 raw
    #   bytes 를 재해시하므로, Linux 에서 만든 artifact 를 Windows clone 에서
    #   검증하면 실패한다. exact bytes 를 동봉하는 것이 유일하게 이식 가능한 답이다.
    inputs_map: dict[str, str] = {}
    for path_s in sealed_inputs(run_dir):
        p = Path(path_s)
        if not p.is_absolute():
            p = (Path(repo_root) if repo_root else REPO_ROOT) / p
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
        rel = _rel(p, repo_root)
        # ★ 10차 — 외부 입력은 bundle 최상위 inputs/ 에 모은다 (nested 포함).
        #   같은 이름의 **다른 파일**이 오면 조용히 덮어쓰지 않고 digest 접두사로
        #   구분한다 (예: 서로 다른 base.yaml 두 개).
        base_inputs = (inputs_root or out_dir) / "inputs"
        base_inputs.mkdir(parents=True, exist_ok=True)
        dst = base_inputs / Path(rel).name
        if dst.exists():
            from src.io import file_digest as _fdig
            if _fdig(dst) != _fdig(p):
                dst = base_inputs / f"{str(_fdig(p))[:12]}_{Path(rel).name}"
        if not dst.exists():
            shutil.copy2(p, dst)
            copied += 1
        inputs_map[(Path("inputs") / dst.name).as_posix()] = rel
    return copied, missing, inputs_map


def _payload_map(bundle_dir: Path) -> dict[str, str]:
    """묶음 안 모든 파일의 full SHA-256 (payload 목록 자신은 제외).

    ★ F80/9-c — 키는 **POSIX 구분자**로 정규화한다. `str(relative_to())` 는
    Windows 에서 `attempts\\manifest_...` 를 만들어, Linux 에서 만든 묶음을
    Windows 에서 check 하면 같은 파일이 두 키로 보여 실패했다.
    """
    out = {}
    for f in sorted(bundle_dir.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(bundle_dir).as_posix()
        if rel == PAYLOAD:
            continue
        out[rel] = _full(f)
    return out


def bundle(run_dir, out_dir, repo_root=None) -> dict:
    """run_dir 를 out_dir 로 묶는다 (empty staging → 원자적 교체).

    반환: {"copied", "external", "missing", "nested"}
    """
    run_dir, out_dir = Path(run_dir), Path(out_dir)
    # ★ F71/8-4 — 같은 out_dir 에 다시 묶을 때, source 에서 사라진 파일이 옛
    #   묶음에 남아 `check()` 를 통과시켰다. 빈 staging 에 만들고 통째로 바꾼다.
    stage = out_dir.with_name(out_dir.name + ".staging")
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    copied, missing, inputs_map = _copy_run(run_dir, stage, repo_root)

    nested = []
    for sub in nested_runs(run_dir):
        # ★ 10차 — 외부 입력은 **최상위** inputs/ 로 모은다. 예전에는
        #   <bundle>/wsweep/inputs/ 에 떨어져 restore 가 절대 읽지 않았다.
        n_c, n_m, n_i = _copy_run(sub, stage / sub.name, repo_root,
                                  inputs_root=stage)
        copied += n_c
        missing += n_m
        inputs_map.update(n_i)
        nested.append(sub.name)

    # ★ 10차 자체 리뷰 — **봉인과 어긋난 bytes 는 묶지 않는다.** 예전에는 실행
    #   후 변조된 fits/curves 도 현재 bytes 그대로 담아 payload 를 만들었으므로
    #   check() 가 "온전"을 인증했고, 재보관이 마지막 정상 묶음을 staging 교체로
    #   파괴했다. 불일치 발견 시 기존 묶음을 남기고 실패한다.
    run_rel = _rel(run_dir, repo_root)
    seal_bad = _seal_conflicts(stage, run_rel, nested, inputs_map)
    if seal_bad:
        shutil.rmtree(stage)
        raise RuntimeError(
            "봉인 불일치 — 이 실행 디렉터리는 기록과 다른 bytes 를 담고 있어 "
            "묶지 않습니다 (기존 묶음은 그대로 둡니다):\n  "
            + "\n  ".join(seal_bad))

    (stage / RESTORE_MAP).write_text(yaml.safe_dump(
        {"run_dir": run_rel, "inputs": inputs_map, "nested": nested},
        allow_unicode=True, sort_keys=False), encoding="utf-8")
    (stage / PAYLOAD).write_text(yaml.safe_dump(
        _payload_map(stage), allow_unicode=True, sort_keys=False), encoding="utf-8")

    if out_dir.exists():
        shutil.rmtree(out_dir)
    stage.rename(out_dir)
    return {"copied": copied, "external": sorted(inputs_map.values()),
            "missing": missing, "nested": nested}


def _seal_conflicts(b: Path, run_rel: str, nested: list[str],
                    inputs_map: dict[str, str]) -> list[str]:
    """묶인 bytes 를 manifest 의 봉인 기록과 대조한다 (10차).

    누락은 check() 의 몫이고, 여기서는 **존재하는데 digest 가 다른** 것만 잡는다
    — 그것이 "변조된 산출물을 인증된 묶음으로 만드는" 통로였다.
    """
    from src.io import file_digest

    bad: list[str] = []
    rev: dict[str, str] = {}
    for arch, orig in inputs_map.items():
        rev.setdefault(orig, arch)
    for sub in [""] + list(nested):
        base = b / sub if sub else b
        pre = f"{sub}/" if sub else ""
        mp = base / "manifest.yaml"
        man = (yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
               ) if mp.is_file() else {}
        sub_rel = f"{run_rel}/{sub}" if sub else run_rel
        for path_s, want in (man.get("input_sha256") or {}).items():
            try:
                inner = Path(path_s).relative_to(sub_rel)
            except ValueError:
                inner = None
            src = (base / inner if inner is not None
                   else (b / rev[path_s] if path_s in rev else None))
            if src is None or not src.is_file():
                continue
            got = file_digest(src)
            if got != want:
                bad.append(f"{pre or ''}{path_s}: 봉인 {want} ≠ 현재 {got}")
        seal = man.get("fits_seal") or {}
        fp = base / "fits.parquet"
        if seal.get("file_sha256") and fp.is_file() \
                and _full(fp) != seal["file_sha256"]:
            bad.append(f"{pre}fits.parquet: manifest.fits_seal 과 다르다")
        cm = base / "curves_manifest.yaml"
        if cm.is_file():
            cman = yaml.safe_load(cm.read_text(encoding="utf-8")) or {}
            cp = base / "curves.parquet"
            if cman.get("curves_sha256") and cp.is_file() \
                    and _full(cp) != cman["curves_sha256"]:
                bad.append(f"{pre}curves.parquet: curves_manifest 와 다르다")
    return bad


def check(bundle_dir) -> dict:
    """묶음이 검증에 필요한 파일을 다 가졌고 **바이트가 온전한지**."""
    b = Path(bundle_dir)
    missing: list[str] = []

    rp, pp = b / RESTORE_MAP, b / PAYLOAD
    meta = (yaml.safe_load(rp.read_text(encoding="utf-8")) or {}) if rp.is_file() else {}
    if not rp.is_file():
        missing.append(RESTORE_MAP)
    rmap = meta.get("inputs") or {}
    run_rel = str(meta.get("run_dir") or "")

    # ★ F71 — payload 재해시. 묶음 안에서 파일이 바뀌었으면 여기서 걸린다.
    if not pp.is_file():
        missing.append(PAYLOAD)
    else:
        rec = yaml.safe_load(pp.read_text(encoding="utf-8")) or {}
        now = _payload_map(b)
        for k in sorted(set(rec) | set(now)):
            if rec.get(k) != now.get(k):
                missing.append(f"{k} (payload digest 불일치)")

    for sub in [""] + list(meta.get("nested") or []):
        base = b / sub if sub else b
        pre = f"{sub}/" if sub else ""
        kind = artifact_kind(base)
        missing += [pre + n for n in required_files(base) if not (base / n).is_file()]
        mp = base / "manifest.yaml"
        man = (yaml.safe_load(mp.read_text(encoding="utf-8")) or {}) if mp.is_file() else {}
        if kind == "fit":
            aid = (man.get("start_provenance") or {}).get("attempt_id")
            if not aid:
                missing.append(f"{pre}manifest.start_provenance.attempt_id (F51 이전 실행)")
            elif not (base / "attempts" / f"manifest_start_{aid}.yaml").is_file():
                missing.append(f"{pre}attempts/manifest_start_{aid}.yaml")

        for path_s in (man.get("input_sha256") or {}):
            p = Path(path_s)
            sub_rel = f"{run_rel}/{sub}" if sub else run_rel
            try:
                inner = p.relative_to(sub_rel) if sub_rel else None
            except ValueError:
                inner = None
            if inner is not None:
                if not (base / inner).is_file():
                    missing.append(f"{pre}{inner} (봉인 입력)")
            elif path_s not in rmap.values():
                missing.append(f"{path_s} (묶음에 없다)")

    return {"ok": not missing, "missing": missing}


def _safe_target(rel: str, root: Path) -> Path:
    """★ F71/8-6 — 절대경로·`..` 탈출을 막는다.

    반례: `restore_map.yaml` 에 `inputs/payload.txt: ../escaped.txt` 를 넣으면
    저장소 root 밖에 파일을 썼다. 외부에서 받은 묶음에 restore 를 돌릴 수 있으므로
    임의 쓰기는 그 자체로 결함이다.
    """
    p = Path(rel)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"허용되지 않는 복원 경로: {rel}")
    out = (root / p).resolve()
    # ★ F80/9-f — 문자열 startswith 는 `/a` 가 `/ab/...` 에 매칭되는 고전적
    #   접두사 버그가 있고, Windows junction 으로도 우회됐다. 경로 의미론으로 본다.
    try:
        ok = out.is_relative_to(root.resolve())
    except AttributeError:                      # py<3.9 없음 (우린 3.10+)
        import os
        ok = os.path.commonpath([str(out), str(root.resolve())]) == str(root.resolve())
    if not ok:
        raise ValueError(f"허용 root 밖으로 나간다: {rel}")
    return out


def restore(bundle_dir, run_dir=None, force: bool = False,
            repo_root=None) -> dict:
    """묶음을 원래 경로로 되돌린다. 그 뒤라야 validate_provenance 가 통과한다.

    ★ F71/8-3 — 기존 파일을 **바이트 비교 없이** 건너뛰지 않는다. 예전에는
    `results/<run>` 이 남은 서버에서 restore→validate 하면 묶음의 내용을 전혀
    확인하지 않고 원본을 다시 검증했다. 즉 "묶음을 검증했다"는 말이 거짓이었다.
    """
    b = Path(bundle_dir)
    root = Path(repo_root) if repo_root else REPO_ROOT
    # ★ F80/9-d — 복원 전에 **payload 무결성을 강제**한다. 예전에는 변조된 묶음
    #   (check=False)도 direct restore 가 통과시켰고, 복원본 validator 는 파생
    #   YAML 을 안 보므로 변조가 최종 보고까지 흘러갈 수 있었다.
    pre = check(b)
    if not pre["ok"]:
        return {"run_dir": None, "written": [], "conflict":
                [f"check 실패: {m}" for m in pre["missing"]], "ok": False}
    rp = b / RESTORE_MAP
    meta = (yaml.safe_load(rp.read_text(encoding="utf-8")) or {}) if rp.is_file() else {}
    rd = str(meta.get("run_dir") or f"results/{b.name}")
    if run_dir:
        dest = Path(run_dir)
    elif Path(rd).is_absolute():
        # 원래 경로가 저장소 밖이면 (예: 임시 디렉터리에서 만든 묶음)
        # 허용 root 안의 대응 위치로 복원한다 — 임의 절대경로 쓰기는 막는다.
        dest = root / "restored" / Path(rd).name
    else:
        dest = _safe_target(rd, root)
    dest.mkdir(parents=True, exist_ok=True)

    written, conflict = [], []

    def _put(src: Path, out: Path):
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            if _full(out) == _full(src):
                return                       # 이미 동일 — 무해
            if not force:
                conflict.append(str(out))
                return
        shutil.copy2(src, out)
        written.append(str(out))

    for src in sorted(b.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(b)
        if rel.parts[0] == "inputs" or rel.name in (RESTORE_MAP, PAYLOAD):
            continue
        _put(src, dest / rel)

    for arch_rel, orig_rel in (meta.get("inputs") or {}).items():
        src = b / arch_rel
        if src.is_file():
            _put(src, _safe_target(orig_rel, root))

    # ★ F72 — `_inputs/` 스냅샷은 **묶지 않고 복원 때 다시 만든다.**
    #   content-addressed 라 봉인된 입력에서 정확히 재생성되고(digest 검사 포함),
    #   묶음에 넣으면 curves.parquet 을 두 번 담게 된다 (19 MB → 38 MB).
    # ★ F80/9-b — **nested 실행에도** 만든다. 최상위만 만들면 복원된 sweep 이
    #   `입력_스냅샷` 에서 실패했다 (리뷰 실측: wsweep validate fail).
    from src.io import snapshot_inputs
    for sub in [None] + list(meta.get("nested") or []):
        rd = dest / sub if sub else dest
        mp2 = rd / "manifest.yaml"
        if not mp2.is_file():
            continue
        man = yaml.safe_load(mp2.read_text(encoding="utf-8")) or {}
        sealed = (man.get("start_provenance") or {}).get("input_sha256") or {}
        if sealed and not conflict:
            try:
                snapshot_inputs(sealed, rd, repo_root=root)
            except (RuntimeError, FileNotFoundError) as e:
                conflict.append(f"{'wsweep ' if sub else ''}_inputs 재생성 실패: {e}")

    return {"run_dir": str(dest), "written": written, "conflict": conflict,
            "ok": not conflict}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("bundle", help="run_dir → artifacts/<name>")
    b.add_argument("run_dir")
    b.add_argument("out_dir")

    c = sub.add_parser("check", help="묶음이 완비·무결한지")
    c.add_argument("bundle_dir")

    r = sub.add_parser("restore", help="묶음을 원래 경로로 복원")
    r.add_argument("bundle_dir")
    r.add_argument("--run-dir", default=None)
    r.add_argument("--repo-root", default=None,
                   help="복원 허용 root (격리 검증 시 임시 clone 을 지정)")
    r.add_argument("--force", action="store_true",
                   help="기존 파일이 달라도 덮어쓴다")

    a = ap.parse_args(argv)
    if a.cmd == "bundle":
        # ★ 48차 P0-8 — 보관도 승격이다 (`artifacts/` 는 인용되는 자리다).
        from tools.preserve import assert_not_smoke_provenance
        assert_not_smoke_provenance([a.run_dir], "보관 묶음")
        res = bundle(a.run_dir, a.out_dir)
        print(f"복사 {res['copied']}개"
              + (f", 하위 실행 {res['nested']}" if res["nested"] else ""))
        if res["external"]:
            print("  저장소 밖 입력 동봉: " + ", ".join(res["external"]))
        if res["missing"]:
            print("  ⚠ 누락: " + ", ".join(res["missing"]))
            return 1              # ★ F71/8-4 — 조용히 성공하지 않는다
        return 0
    if a.cmd == "check":
        res = check(a.bundle_dir)
        if res["ok"]:
            print("검증 가능: 필요한 파일이 모두 있고 digest가 일치한다")
            return 0
        print("검증 불가 — 문제:")
        for m in res["missing"]:
            print(f"  · {m}")
        return 1
    res = restore(a.bundle_dir, a.run_dir, a.force, a.repo_root)
    if not res["ok"]:
        print(f"복원 중단 — 기존 파일이 묶음과 다르다 ({len(res['conflict'])}개):")
        for x in res["conflict"][:5]:
            print(f"  · {x}")
        print("  --force 로 덮어쓰거나, 비어 있는 --run-dir 로 복원하세요.")
        return 1
    print(f"복원 → {res['run_dir']}  (쓴 파일 {len(res['written'])}개)")
    print("이제 검증할 수 있다:\n  python -c \"from src.io import validate_provenance;"
          f" import json; print(json.dumps(validate_provenance('{res['run_dir']}'),"
          " ensure_ascii=False, indent=2))\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
