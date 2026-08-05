"""io.py — parquet 청크 저장/병합 + manifest (resume 지원).

02_CODE_AUDIT.md m1: xlsx 대신 parquet.
03_ARCHITECTURE.md 2.5절: manifest에 git commit / config hash / 환경 기록.

저장 형식 (long format):
  한 조건당 n_interp(300)행 — [cond_id, 축 값들..., x_norm, v_pe, v_ne, v_full, v_full_noisy]
"""

from __future__ import annotations

import csv
import json
import platform
import subprocess
import time
from pathlib import Path

import pandas as pd
import yaml


def git_info(repo_dir: str | Path | None = None) -> dict:
    """현재 git commit / dirty 여부. git이 없어도 죽지 않는다."""
    cwd = str(repo_dir) if repo_dir else None
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True, cwd=cwd,
                                timeout=10).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain"],
                                    capture_output=True, text=True, cwd=cwd,
                                    timeout=10).stdout.strip())
        return {"git_commit": commit or "unknown", "git_dirty": dirty}
    except Exception:  # noqa: BLE001
        return {"git_commit": "unavailable", "git_dirty": None}


def save_chunk(df: pd.DataFrame, out_dir: str | Path, chunk_idx: int) -> Path:
    out = Path(out_dir) / "chunks"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"chunk_{chunk_idx:05d}.parquet"
    df.to_parquet(path, index=False)
    return path


def merge_chunks(out_dir: str | Path, name: str = "curves.parquet") -> Path | None:
    """chunks/*.parquet → 단일 parquet 병합."""
    out_dir = Path(out_dir)
    files = sorted((out_dir / "chunks").glob("chunk_*.parquet"))
    if not files:
        return None
    df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
    path = out_dir / name
    df.to_parquet(path, index=False)
    return path


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


def completed_path(out_dir: str | Path) -> Path:
    return Path(out_dir) / "completed.jsonl"


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


def base_manifest(cfg_hash: str, extra: dict | None = None) -> dict:
    import pybamm

    m = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "config_hash": cfg_hash,
        "pybamm_version": pybamm.__version__,
        "platform": platform.platform(),
        "python": platform.python_version(),
        **git_info(Path(__file__).resolve().parent.parent),
    }
    if extra:
        m.update(extra)
    return m


def mark_completed(out_dir: str | Path, cond_id: str) -> None:
    """완료 조건을 completed.jsonl에 append (resume용, 청크 flush 후 호출)."""
    with open(completed_path(out_dir), "a", encoding="utf-8") as f:
        f.write(json.dumps({"cond_id": cond_id}) + "\n")


def load_completed(out_dir: str | Path) -> set[str]:
    path = completed_path(out_dir)
    if not path.exists():
        return set()
    done = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            done.add(json.loads(line)["cond_id"])
    return done
