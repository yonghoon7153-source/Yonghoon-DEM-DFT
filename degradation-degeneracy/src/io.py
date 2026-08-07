"""io.py — parquet 청크 저장/병합 + manifest (resume 지원).

02_CODE_AUDIT.md m1: xlsx 대신 parquet.
03_ARCHITECTURE.md 2.5절: manifest에 git commit / config hash / 환경 기록.

저장 형식 (long format):
  한 조건당 n_interp(300)행 — [cond_id, 축 값들..., x_norm, v_pe, v_ne, v_full, v_full_noisy]
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import subprocess
import time
from pathlib import Path

import pandas as pd
import yaml


def git_info(repo_dir: str | Path | None = None, save_diff_to=None) -> dict:
    """현재 git commit / dirty 여부. git이 없어도 죽지 않는다.

    ★ F30 — dirty 실행이면 **diff를 같이 남긴다.**
      `git_dirty: true`만 적혀 있으면 그 산출물을 만든 코드가 세상에 없다.
      결과 parquet은 재집계할 수 있어도 독립 연구자가 같은 숫자를 만들 수 없어
      인용 근거로 못 쓴다. 실제로 grid_fine_v2·halfcell_v1이 그 상태였다.
    """
    cwd = str(repo_dir) if repo_dir else None
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"],
                                capture_output=True, text=True, cwd=cwd,
                                timeout=10).stdout.strip()
        # ★ dirty = **추적 중인 파일의 수정**만. 무관한 untracked 파일(다른
        #   프로젝트 산출물, venv 등)까지 세면 모든 실행이 영구히 dirty로 찍혀
        #   플래그가 무의미해진다. untracked는 정보로만 남긴다.
        dirty_txt = subprocess.run(["git", "status", "--porcelain",
                                    "--untracked-files=no"],
                                   capture_output=True, text=True, cwd=cwd,
                                   timeout=10).stdout.strip()
        untracked = subprocess.run(["git", "ls-files", "--others",
                                    "--exclude-standard"],
                                   capture_output=True, text=True, cwd=cwd,
                                   timeout=10).stdout.split()
        # ★ F37 — untracked를 **전부** 무시하면 false clean이 된다. 실행에 실제로
        #   import되거나 읽히는 경로(src/tools/configs) 아래의 untracked
        #   code/config는 재현을 막으므로 dirty로 센다. 그 밖(다른 프로젝트
        #   산출물, venv 등)은 개수와 목록만 정보로 남긴다.
        crit = [u for u in untracked
                if u.startswith(("src/", "tools/", "configs/", "scripts/"))
                and u.endswith((".py", ".yaml", ".yml", ".json", ".sh", ".csv"))]
        info = {"git_commit": commit or "unknown",
                "git_commit_short": commit[:8] if commit else "unknown",
                "git_dirty": bool(dirty_txt) or bool(crit),
                "git_dirty_tracked": bool(dirty_txt),
                "git_untracked_count": len(untracked),
                "git_untracked_critical": crit[:50]}
        if dirty_txt and save_diff_to is not None:
            diff = subprocess.run(["git", "diff", "HEAD"], capture_output=True,
                                  text=True, cwd=cwd, timeout=30).stdout
            p = Path(save_diff_to)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(diff, encoding="utf-8")
            info["git_dirty_diff"] = str(p.name)
            info["git_dirty_files"] = dirty_txt.splitlines()[:50]
        return info
    except Exception:  # noqa: BLE001
        return {"git_commit": "unavailable", "git_dirty": None}


def file_digest(path) -> str | None:
    """입력 파일의 SHA-256 (앞 16자). 재현성 검증용. 없으면 None."""
    if path is None:
        return None
    p = Path(path)
    if not p.exists() or not p.is_file():
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()[:16]


def save_chunk(df: pd.DataFrame, out_dir: str | Path, chunk_idx: int,
               subdir: str = "chunks") -> Path:
    """청크 저장. 파일명에 PID를 넣어 프로세스 간 덮어쓰기를 막는다.

    같은 out_dir에 두 프로세스가 붙으면 각자 chunk_idx를 독립적으로 세기 때문에
    이름이 겹쳐 서로의 결과를 덮어쓴다 (완료 표시는 남고 곡선만 사라지는 손실).
    """
    out = Path(out_dir) / subdir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"chunk_{chunk_idx:05d}_{os.getpid()}.parquet"
    df.to_parquet(path, index=False)
    return path


def chunk_files(out_dir: str | Path, subdir: str = "chunks") -> list[Path]:
    """청크 파일을 **생성 순서(mtime)** 로 정렬해 반환. 뒤쪽이 최신.

    이름순이 아니라 mtime순인 이유: 프로세스마다 chunk_idx가 독립이라
    이름 정렬로는 시간 순서를 알 수 없다.
    """
    files = list((Path(out_dir) / subdir).glob("chunk_*.parquet"))
    return sorted(files, key=lambda p: (p.stat().st_mtime_ns, p.name))


def merge_chunks(out_dir: str | Path, name: str = "curves.parquet",
                 subdir: str = "chunks", keys: tuple = ("cond_id",)) -> Path | None:
    """chunks/*.parquet → 단일 parquet 병합.

    같은 조건이 여러 청크에 있으면(같은 디렉터리에 --resume 없이 재실행한 경우)
    **가장 나중 청크만 남긴다.** 중복 행이 남으면 downstream fitting이
    같은 조건을 여러 번 세게 된다.
    """
    out_dir = Path(out_dir)
    files = chunk_files(out_dir, subdir)
    if not files:
        return None
    parts = []
    for i, f in enumerate(files):
        part = pd.read_parquet(f)
        part["_chunk"] = i          # 뒤쪽 청크가 최신
        parts.append(part)
    df = pd.concat(parts, ignore_index=True)

    kk = [k for k in keys if k in df.columns]
    if kk:
        # 키별 최신 청크만 유지 (부분 행이 아니라 블록 단위로 선택)
        newest = df.groupby(kk)["_chunk"].transform("max")
        df = df[df["_chunk"] == newest].reset_index(drop=True)
    df = df.drop(columns="_chunk")

    path = out_dir / name
    df.to_parquet(path, index=False)
    return path


def _pid_alive(pid: int) -> bool:
    """해당 PID가 살아 있고 실제로 이 프로젝트의 grid 프로세스인지 확인."""
    try:
        os.kill(pid, 0)
    except (ProcessLookupError, ValueError):
        return False
    except PermissionError:
        return True   # 살아 있으나 다른 사용자 소유
    cmdline = Path(f"/proc/{pid}/cmdline")
    if cmdline.exists():   # PID 재사용 오탐 방지 (Linux)
        cmd = cmdline.read_text(errors="ignore").replace("\x00", " ")
        # 리뷰 F13/F24: 이 목록이 실제 진입점과 어긋나면 **살아 있는 실행의 lock을
        # stale로 오판해 지운다** → 같은 --out에 두 프로세스가 붙는다.
        # weight_sweep은 `python -m src.weight_sweep`으로 뜨므로 반드시 포함해야
        # 한다 (2026-08-07 실측: 빠져 있어서 sweep 위에 sweep이 겹쳤다).
        return any(m in cmd for m in _RUN_ENTRYPOINTS)
    return True


# 계산을 수행하는 진입점 모듈. lock 판정과 감시 스크립트가 같은 목록을 봐야 한다.
_RUN_ENTRYPOINTS = ("src.grid", "src.fitting", "src.weight_sweep")


def acquire_run_lock(out_dir: str | Path, name: str = ".run.lock") -> Path:
    """출력 디렉터리 실행 잠금. 이미 살아있는 실행이 있으면 RuntimeError.

    같은 --out에 두 프로세스가 붙으면 청크가 서로 덮이고 집계가 어긋난다.
    죽은 프로세스가 남긴 lock은 자동으로 정리한다.
    """
    path = Path(out_dir) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            old_pid = int(path.read_text(encoding="utf-8").split()[0])
        except (ValueError, IndexError):
            old_pid = -1
        if old_pid > 0 and old_pid != os.getpid() and _pid_alive(old_pid):
            raise RuntimeError(
                f"같은 출력 디렉터리에서 이미 실행 중입니다 (PID {old_pid}, {out_dir}). "
                f"동시 실행은 청크를 서로 덮어씁니다. "
                f"그 실행을 기다리거나 종료(kill {old_pid})한 뒤 다시 시도하세요.")
        path.unlink(missing_ok=True)   # stale lock
    path.write_text(f"{os.getpid()} {time.strftime('%Y-%m-%dT%H:%M:%S')}\n",
                    encoding="utf-8")
    return path


def release_run_lock(out_dir: str | Path, name: str = ".run.lock") -> None:
    path = Path(out_dir) / name
    try:
        if path.exists() and path.read_text(encoding="utf-8").split()[0] == str(os.getpid()):
            path.unlink()
    except (OSError, IndexError):
        pass


def load_failed(out_dir: str | Path) -> set[str]:
    """failed.csv의 **고유** cond_id 집합.

    행 수를 세면 재실행 시 중복 기록 때문에 집계가 어긋난다
    (completed.jsonl은 set으로 중복 제거되므로 기준을 맞춘다).
    """
    path = Path(out_dir) / "failed.csv"
    if not path.exists():
        return set()
    with open(path, newline="", encoding="utf-8") as f:
        return {row["cond_id"] for row in csv.DictReader(f) if row.get("cond_id")}


def append_failed(out_dir: str | Path, cond_id: str, cond: dict, reason: str) -> None:
    """실패 조건을 failed.csv에 기록 (전체 실행은 계속)."""
    path = Path(out_dir) / "failed.csv"
    new = not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["cond_id", "condition", "reason", "timestamp"])
        w.writerow([cond_id, json.dumps(cond, ensure_ascii=False), reason,
                    time.strftime("%Y-%m-%dT%H:%M:%S")])


# ---------------------------------------------------------------- manifest

def manifest_path(out_dir: str | Path) -> Path:
    return Path(out_dir) / "manifest.yaml"


def completed_path(out_dir: str | Path, name: str = "completed.jsonl") -> Path:
    return Path(out_dir) / name


def write_manifest(out_dir: str | Path, payload: dict) -> Path:
    """manifest.yaml 기록 (기존 내용에 병합)."""
    path = manifest_path(out_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if path.exists():
        existing = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    existing.update(payload)
    path.write_text(yaml.safe_dump(existing, allow_unicode=True, sort_keys=False),
                    encoding="utf-8")
    return path


def base_manifest(cfg_hash: str, extra: dict | None = None,
                  out_dir=None, inputs=None) -> dict:
    """★ F30 — 재현에 필요한 것을 전부 적는다.

    `config_hash: ''`, `git_dirty: true`만 남은 manifest는 provenance가 아니다.
    out_dir을 주면 dirty diff를 `run_dirty.patch`로 같이 저장하고, inputs를
    주면 입력 파일의 SHA-256을 기록한다.
    """
    import pybamm

    repo = Path(__file__).resolve().parent.parent
    diff_path = Path(out_dir) / "run_dirty.patch" if out_dir else None
    m = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "config_hash": cfg_hash,
        "pybamm_version": pybamm.__version__,
        "platform": platform.platform(),
        "python": platform.python_version(),
        **git_info(repo, save_diff_to=diff_path),
    }
    if inputs:
        m["input_sha256"] = {str(p): file_digest(p) for p in inputs if p is not None}
    if extra:
        m.update(extra)
    # 재현 가능성을 스스로 판정해 적어 둔다 — 읽는 쪽이 놓치지 않게
    m["reproducible"] = bool(cfg_hash) and not m.get("git_dirty", True)
    if not m["reproducible"]:
        m["_주의"] = (
            "이 산출물은 그대로 재현할 수 없다. "
            + ("config_hash가 비어 있다. " if not cfg_hash else "")
            + ("작업 트리가 dirty 상태였다 (diff는 run_dirty.patch). "
               if m.get("git_dirty_tracked") else "")
            + (f"실행 경로에 커밋되지 않은 파일이 있었다: "
               f"{m.get('git_untracked_critical')}. "
               if m.get("git_untracked_critical") else "")
            + "인용하려면 clean commit에서 재생성할 것.")
    return m


# ---------------------------------------------------------------- F38 provenance 검증

def validate_provenance(run_dir) -> dict:
    """★ F38 — 결과를 인용해도 되는 상태인지 **실제로** 검사한다.

    `run_sig` 열이 있는지만 보는 것으로는 부족하다. 임의의 문자열 하나를 넣어도
    통과하므로, 혼합되거나 위조된 provenance에서 인용 금지 배너가 사라진다.

    반환: {"ok": bool, "checks": {이름: (통과, 사유)}, "fail": [실패한 이름]}
    """
    run_dir = Path(run_dir)
    man = {}
    mp = run_dir / "manifest.yaml"
    if mp.exists():
        man = yaml.safe_load(mp.read_text(encoding="utf-8")) or {}

    checks: dict[str, tuple[bool, str]] = {}
    checks["manifest_존재"] = (bool(man), "manifest.yaml이 없다")
    checks["config_hash"] = (bool(man.get("config_hash")), "config_hash가 비어 있다")
    checks["clean_worktree"] = (man.get("git_dirty") is False,
                                "dirty worktree 또는 실행 경로에 untracked 파일")
    digs = man.get("input_sha256") or {}
    checks["입력_digest"] = (bool(digs) and all(v for v in digs.values()),
                             "입력 파일 SHA가 비었거나 없다")
    checks["run_signature_기록"] = (bool(man.get("run_signature")),
                                    "manifest에 run_signature가 없다")

    fp = run_dir / "fits.parquet"
    if not fp.exists():
        checks["fits_존재"] = (False, "fits.parquet이 없다")
    else:
        cols = pd.read_parquet(fp).columns
        need = pd.read_parquet(fp, columns=[c for c in ("run_sig", "restarts_json")
                                            if c in cols])
        has_sig = "run_sig" in need.columns
        checks["행별_서명"] = (has_sig and not need["run_sig"].isna().any()
                               if has_sig else False,
                               "run_sig 열이 없거나 비어 있는 행이 있다")
        uniq = sorted(need["run_sig"].dropna().unique()) if has_sig else []
        checks["단일_서명"] = (len(uniq) == 1, f"서명이 {len(uniq)}종이다")
        checks["manifest와_일치"] = (
            bool(uniq) and str(uniq[0]) == str(man.get("run_signature")),
            "fits의 서명과 manifest의 run_signature가 다르다")
        # restart 출처 — F25/F31이 저장하는 형식인가
        src_ok = False
        if "restarts_json" in need.columns and len(need):
            try:
                first = json.loads(need["restarts_json"].dropna().iloc[0])
                src_ok = bool(first) and isinstance(first[0], dict) \
                    and "source" in first[0]
            except (ValueError, TypeError, IndexError):
                src_ok = False
        checks["restart_출처"] = (src_ok,
                                  "restarts_json에 source가 없다 (F25/F31 이전 형식)")

    fail = [k for k, (ok, _) in checks.items() if not ok]
    return {"ok": not fail, "checks": {k: {"pass": ok, "why": why}
                                       for k, (ok, why) in checks.items()},
            "fail": fail,
            "reasons": [checks[k][1] for k in fail]}


def mark_completed(out_dir: str | Path, cond_id: str,
                   name: str = "completed.jsonl") -> None:
    """완료 조건을 jsonl에 append (resume용, 청크 flush 후 호출)."""
    with open(completed_path(out_dir, name), "a", encoding="utf-8") as f:
        f.write(json.dumps({"cond_id": cond_id}) + "\n")


def load_completed(out_dir: str | Path, name: str = "completed.jsonl") -> set[str]:
    path = completed_path(out_dir, name)
    if not path.exists():
        return set()
    done = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            done.add(json.loads(line)["cond_id"])
    return done
