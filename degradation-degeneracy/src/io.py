"""io.py — parquet 청크 저장/병합 + manifest (resume 지원).

02_CODE_AUDIT.md m1: xlsx 대신 parquet.
03_ARCHITECTURE.md 2.5절: manifest에 git commit / config hash / 환경 기록.

저장 형식 (long format):
  한 조건당 n_interp(300)행 — [cond_id, 축 값들..., x_norm, v_pe, v_ne, v_full, v_full_noisy]
"""

from __future__ import annotations

import csv
import json
import os
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
        # 리뷰 F13: fit lock(.fit.lock)도 이 함수를 쓰므로 fitting 프로세스도 인정
        return any(m in cmd for m in ("src.grid", "src.fitting"))
    return True


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
