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
from collections import Counter
from pathlib import Path, PurePath

import pandas as pd
import yaml


#: ★ F73 — dirty 판정의 **범위**. 이 실행의 결과를 바꿀 수 있는 경로만 센다.
#:   저장소가 다른 프로젝트(MPM/DEM)와 공유되므로, 저장소 전체로 판정하면
#:   무관한 파일 하나 때문에 열 시간짜리 산출물이 전부 인용 불가가 된다.
#:   (실측: `se_curve/xfer_*.json` 2개가 수정돼 있어 smoke 가 dirty 로 찍혔다)
#:   범위 밖 수정은 `git_dirty_out_of_scope` 로 **정보로는 남긴다** — 판정을
#:   느슨하게 하는 변경이므로 무엇을 뺐는지 보이지 않으면 안 된다.
#: ★ 14차 2차 발견 5 — digest 범위(`_SCOPE_DIRS`/`_SCOPE_FILE_GLOBS`)와 **같은
#:   matcher** 를 쓴다. 예전에는 digest 가 `requirements*.txt` 를 glob 으로 전부
#:   읽는데 여기는 두 이름만 exact match 라, 새 `requirements-dev.txt` 가
#:   digest 에는 들어가고 dirty 판정에는 안 들어갔다 ("RUN_SCOPE 와 1:1" 설명이
#:   깨지는 지점). 표시용 문자열은 아래 RUN_SCOPE, 판정은 `in_run_scope()`.
RUN_SCOPE = ("src/", "tools/", "configs/", "scripts/", "run.sh",
             "requirements*.txt")


#: ★ 14차 3차 발견 3 — 제외 규칙의 **단일 출처**. digest 와 dirty 판정이 같은
#:   파일 집합을 보려면 포함(`in_run_scope`)뿐 아니라 제외도 공유해야 한다.
#:   예전 dirty 쪽 `_SKIP` 은 `.pyc` 를 이름 중간에 포함해도 제외해서,
#:   `configs/model.pyconfig` 같은 실제 입력이 digest 에는 들어가고 dirty
#:   판정에서는 빠질 수 있었다.
_EXCLUDE_DIRS = ("__pycache__", ".ipynb_checkpoints")
_EXCLUDE_SUFFIXES = (".pyc", ".pyo")


def is_scope_excluded(rel: str) -> bool:
    """캐시·바이트코드인가 (digest·dirty 공통 제외 규칙).

    디렉터리는 **경로 성분 단위**로, 확장자는 **suffix 로만** 판정한다.
    """
    parts = PurePath(rel).parts
    if any(p in _EXCLUDE_DIRS for p in parts):
        return True
    return PurePath(rel).suffix in _EXCLUDE_SUFFIXES


def in_run_scope(rel: str, scope: tuple = RUN_SCOPE) -> bool:
    """저장소 상대경로가 RUN_SCOPE 안인가 (digest 범위와 동일 규칙).

    `*` 가 있는 항목은 root 파일 glob, `/` 로 끝나면 디렉터리 접두사,
    나머지는 정확한 파일명이다.
    """
    from fnmatch import fnmatch

    for s in scope:
        if s.endswith("/"):
            if rel.startswith(s):
                return True
        elif "*" in s:
            if "/" not in rel and fnmatch(rel, s):
                return True
        elif rel == s:
            return True
    return False


def git_info(repo_dir: str | Path | None = None, save_diff_to=None,
             scope: tuple = RUN_SCOPE) -> dict:
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
        # ★ F75/발견 4-b — `-z` 로 받는다. 기본 출력은 비ASCII 경로를
        #   "src/\355\225\234..." 로 quoting 해서 `startswith("src/")` 가
        #   실패했다 (한글 파일명 untracked 가 clean 으로 통과).
        untracked = [x for x in subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", "-z"],
            capture_output=True, text=True, cwd=cwd,
            timeout=10).stdout.split("\0") if x]
        # ★ F75/발견 4-c — **ignored 인데 실행 경로에 있는** 파일도 재현을 막는다.
        #   source_digest 는 내용을 해시하지만, clean clone 에는 그 파일이 없어
        #   재검증이 불가능하다 (반례: configs/lookup.parquet, src/settings.local).
        ignored = [x for x in subprocess.run(
            ["git", "ls-files", "--others", "--ignored", "--exclude-standard", "-z"],
            capture_output=True, text=True, cwd=cwd,
            timeout=10).stdout.split("\0") if x]
        # ★ F37 — untracked를 **전부** 무시하면 false clean이 된다. 실행에 실제로
        #   import되거나 읽히는 경로(src/tools/configs) 아래의 untracked
        #   code/config는 재현을 막으므로 dirty로 센다. 그 밖(다른 프로젝트
        #   산출물, venv 등)은 개수와 목록만 정보로 남긴다.
        # ★ F47 — 확장자 allowlist 를 두면 `.toml`/`.ini`/`.cfg`/데이터 캐시 같은
        #   새 입력이 추가될 때 조용히 false clean 이 된다. critical 디렉터리
        #   아래는 **전부** dirty 로 센다 (캐시·바이트코드만 제외).
        # ★ 14차 2차 발견 5 — 범위 판정을 digest 와 **같은 matcher** 로 한다.
        #   예전에는 디렉터리 4개만 하드코딩해서, digest 가 읽는 root 파일
        #   (`run.sh`·`requirements*.txt`)을 새로 만든 채 실행해도 clean 이었다.
        crit = [u for u in untracked + ignored
                if in_run_scope(u, scope) and not is_scope_excluded(u)]
        # ★ F73 — 수정된 tracked 파일을 **실행 범위 안/밖**으로 나눈다.
        #   경로는 `--name-only` 로 받는다. porcelain 을 문자열 슬라이싱하면
        #   상태 문자 폭·rename 표기·따옴표 때문에 첫 글자가 잘린다 (실측).
        # ★ F75/발견 4-a — `--no-renames -z`. rename 탐지가 켜져 있으면
        #   `--name-only` 가 **새 경로만** 줘서, 실행 범위 파일을 밖으로 rename
        #   한 tracked 변경(git mv src/a.py other/)이 clean 으로 승인됐다.
        #   -z 는 비ASCII quoting 도 막는다.
        mod = [x for x in subprocess.run(
            ["git", "diff", "--name-only", "--no-renames", "-z", "HEAD"],
            capture_output=True, text=True, cwd=cwd,
            timeout=10).stdout.split("\0") if x.strip()]
        # ★ git 은 **저장소 root 기준** 경로를 준다. 이 프로젝트는 monorepo 의
        #   하위 디렉터리이므로 그 접두사를 떼야 `src/` 로 매칭된다.
        #   (실측: `src/io.py` 수정이 "범위 밖"으로 분류됐다)
        prefix = subprocess.run(["git", "rev-parse", "--show-prefix"],
                                capture_output=True, text=True, cwd=cwd,
                                timeout=10).stdout.strip()

        def _local(x: str) -> str | None:
            if not prefix:
                return x
            return x[len(prefix):] if x.startswith(prefix) else None

        in_scope = [m for m in mod
                    if (_l := _local(m)) is not None and in_run_scope(_l, scope)]
        out_scope = [m for m in mod if m not in in_scope]
        info = {"git_commit": commit or "unknown",
                "git_commit_short": commit[:8] if commit else "unknown",
                "git_dirty": bool(in_scope) or bool(crit),
                "git_dirty_tracked": bool(in_scope),
                "git_dirty_files_in_scope": in_scope[:50],
                # 판정에는 안 넣지만 반드시 기록한다 — 뺀 것을 숨기지 않는다
                "git_dirty_out_of_scope": out_scope[:50],
                "git_dirty_repo_wide": bool(mod) or bool(crit),
                "git_dirty_scope": list(scope),
                "git_untracked_count": len(untracked),
                "git_untracked_critical": crit[:50]}
        if in_scope and save_diff_to is not None:
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


# ★ 14차-2 — RUN_SCOPE (root CLAUDE.md 하드룰 3 과 1:1). 여기 파일이 바뀌면
#   코드 identity 가 바뀌고 기존 산출물이 무효화된다.
_SCOPE_DIRS = ("src", "tools", "configs", "scripts")
_SCOPE_FILE_GLOBS = ("run.sh", "requirements*.txt")


def _digest_path_key(rel) -> bytes:
    """digest 에 들어가는 경로 키 — OS 무관 POSIX 정규형.

    ★ 14차-2 — `str(relative_to(...))` 는 Windows 에서 `src\\io.py` 를 내
    같은 Git blob 이 환경마다 다른 digest 를 얻었다 (리뷰어 실측:
    POSIX 4fa3e2af0a2e8106 vs `\\` 구분자 7ac22c1055eae262).
    """
    return PurePath(rel).as_posix().encode("utf-8")


def source_digest(root=None, dirs=_SCOPE_DIRS,
                  file_globs=_SCOPE_FILE_GLOBS) -> str:
    """★ F49 — 실제로 import되는 source tree의 내용 해시.

    `run_sig` 에 코드 identity 가 없으면, **코드만 바꾸고 같은 output 에 resume 했을
    때 서로 다른 코드로 만든 행이 같은 서명 아래 섞이고 병합 검사를 통과한다.**
    (2026-08-07 5차 리뷰가 3조건 반례로 재현했다: OLD_CODE 행과 NEW_CODE 행이
    같은 `run_sig` 79f2e9c798ee 로 병합되고 validator 가 ok=True 를 냈다.)

    git commit 만으로는 dirty 실행을 못 잡으므로 파일 내용을 직접 해시한다.

    ★ 14차-2 — (1) 경로 키·정렬을 POSIX 정규형으로 통일해 OS 간 digest 를
    일치시키고, (2) 범위를 RUN_SCOPE 전체(`scripts/`·`run.sh`·
    `requirements*.txt` 포함)로 넓혔다 — 이전엔 실행 진입점을 바꿔도
    digest 가 안 변하는 identity 구멍이 있었다.
    """
    root = Path(root) if root else Path(__file__).resolve().parent.parent
    entries: list[tuple[bytes, Path]] = []
    for d in dirs:
        base = root / d
        if not base.exists():
            continue
        for f in base.rglob("*"):
            # ★ 14차 3차 발견 3 — 제외 규칙을 dirty 판정과 공유한다
            if not f.is_file() or is_scope_excluded(f.relative_to(root)):
                continue
            entries.append((_digest_path_key(f.relative_to(root)), f))
    for g in file_globs:
        for f in root.glob(g):
            if f.is_file():
                entries.append((_digest_path_key(f.relative_to(root)), f))
    h = hashlib.sha256()
    for key, f in sorted(entries):
        h.update(key)
        h.update(f.read_bytes())
    return h.hexdigest()[:16]


def env_fingerprint() -> dict:
    """★ F55 — 결과를 만드는 것은 저장소 파일만이 아니다.

    fitting 은 SciPy `minimize`·NumPy·pandas·joblib 에 의존하고, requirements 는
    하한만 둔다. 같은 source tree 라도 SciPy 버전이 다르면 다른 최적화 결과가
    나올 수 있는데, `source_digest` 만으로는 그 축을 못 잡는다.
    (5차 리뷰: runtime-only 변형으로 같은 `run_sig` 혼합이 재현됐다.)
    """
    import platform
    import sys

    out = {"python": sys.version.split()[0],
           "platform": platform.platform(),
           "machine": platform.machine()}
    # ★ 52차 P0-6 — 결과를 바꾸는 **실제 backend** 도 runtime 축이다.
    #   `DD_SMOOTH_CACHE` 는 목적함수 J 를 bit 단위로 바꾸고 그 J 는 행에
    #   기록되는데, 51차까지 승인에도 지문에도 없었다 (리뷰어 실측).
    try:
        from src.objective import effective_smoothing_backend
        out["smoothing_backend"] = effective_smoothing_backend()
    except Exception:                                     # pragma: no cover
        out["smoothing_backend"] = "unknown"
    for name in ("numpy", "scipy", "pandas", "joblib", "pyarrow", "pybamm",
                 "matplotlib", "yaml"):
        try:
            m = __import__(name)
            out[name] = str(getattr(m, "__version__", "unknown"))
        except Exception:  # noqa: BLE001
            out[name] = "absent"
    # ★ 12차 발견 2 — 수치를 실제로 만드는 solver backend 는 pybamm 과 **별도
    #   배포판**이다 (pybammsolvers 가 IDAKLU 를, casadi 가 fallback 을 제공).
    #   이 둘이 바뀌면 같은 pybamm 버전에서도 값이 달라질 수 있다. import 로는
    #   버전을 못 얻는 패키지가 있어 metadata 로 읽는다.
    import importlib.metadata as _md
    for name in ("pybammsolvers", "casadi"):
        try:
            out[name] = str(_md.version(name))
        except Exception:  # noqa: BLE001
            try:
                out[name] = str(getattr(__import__(name), "__version__", "unknown"))
            except Exception:  # noqa: BLE001
                out[name] = "absent"
    return out


def canonical_input_key(path, repo_root=None) -> str:
    """★ F65 — 봉인 map 의 키를 **저장소 기준 상대경로**로 정규화한다.

    예전에는 `str(path)` 를 그대로 썼다. `.cache/halfcell/*.json` 은 config 의
    `_config_path` 에서 root 를 계산하므로 **절대경로**가 되고, 그 절대문자열이
    manifest 에 박혔다. 그래서
      · 다른 clone 으로 복원하면 `입력_digest_재해시` 가 "파일 없음"으로 실패하고,
      · `archive_bundle` 은 restore map 을 상대경로로 적으므로 `check()` 의
        대조가 어긋나 완비된 묶음도 "검증 불가"로 나왔다.
    저장소 밖 경로는 어쩔 수 없이 절대경로로 남긴다 (그건 애초에 이식 불가다).

    ★ 11차 발견 8 — 구분자를 **POSIX 로 정규화**한다. Windows 에서 만든 manifest
    는 `a\\res\\curves.parquet` 를 키로 적었고, archive 의 restore_map/payload 는
    (F80/9-c, 10차) POSIX 라 두 표기가 어긋나 묶음 검증이 실패했다 (리뷰 실측:
    Windows 에서 nested bundle 테스트 2건 실패). 키는 어느 OS 에서 만들든 같아야
    한다.
    """
    root = Path(repo_root) if repo_root else Path(__file__).resolve().parent.parent
    try:
        return Path(path).resolve().relative_to(root.resolve()).as_posix()
    except (ValueError, OSError):
        return Path(path).as_posix()


def seal_inputs(paths, repo_root=None) -> dict:
    """★ F56 — 입력을 **한 번만** 해시해 봉인하고 그 map 을 끝까지 재사용한다.

    예전에는 시작·run_spec·종료에서 각각 따로 해시해 세 세트가 생겼고, validator 가
    셋 사이의 일치를 확인하지 않았다. 그래서 fitting 후 curves 를 바꿔도
    "행은 옛 곡선, manifest 는 새 곡선"인 artifact 가 통과했다.

    키는 저장소 기준 상대경로다 (F65). 같은 파일을 두 표기로 넘겨도 한 항목이 된다.
    """
    return {canonical_input_key(x, repo_root): file_digest(x)
            for x in paths if x is not None}


def snapshot_inputs(sealed: dict, out_dir, repo_root=None) -> dict:
    """★ F72 — 봉인한 **바이트 자체**를 실행 디렉터리에 복사하고, 계산은 그것만 읽는다.

    F56 은 입력을 시작 시점에 한 번만 해시했다. 그러나 해시한 뒤 **읽기 전까지**
    파일을 바꿀 수 있다. 리뷰가 `run_fit` 에서 실제로 재현했다:

        봉인된 curves cond_id      = SEALED_A
        pd.read_parquet 이 읽은 것 = ACTUALLY_READ_B   ← 사이에 교체
        (읽은 직후 원본으로 복원)
        start/current/manifest digest = 88c9ce154bc038e1  (전부 일치)
        inputs_changed_during_run     = False
        fits cond_id                  = ACTUALLY_READ_B
        validator.ok                  = True

    digest 를 몇 번 더 비교해도 이건 못 막는다 — 비교 시점과 읽기 시점이 다르기
    때문이다. **해시한 바이트를 그대로 읽는 것**만이 답이다.

    복사본은 `<out_dir>/_inputs/<digest12>_<파일명>` 에 content-addressed 로 둔다.
    같은 내용이면 재사용하므로 resume 비용이 없다.

    반환: {원래_키: 스냅샷_경로(Path)}
    """
    root = Path(repo_root) if repo_root else Path(__file__).resolve().parent.parent
    snap_dir = Path(out_dir) / "_inputs"
    snap_dir.mkdir(parents=True, exist_ok=True)
    out = {}
    for key, dig in sealed.items():
        src = Path(key)
        if not src.is_absolute():
            src = root / key
        dst = snap_dir / f"{str(dig)[:12]}_{src.name}"
        if not dst.exists():
            import shutil
            shutil.copy2(src, dst)
        got = file_digest(dst)
        if got != dig:
            # 복사 중에 바뀌었거나 원본이 이미 다른 것 — 계산을 시작하면 안 된다
            raise RuntimeError(
                f"입력 스냅샷이 봉인과 다릅니다: {key} (봉인 {dig}, 스냅샷 {got}). "
                f"실행 중 입력이 바뀌고 있습니다 (F72).")
        out[key] = dst
    return out


def file_digest(path, full: bool = False) -> str | None:
    """파일의 SHA-256. 기본은 앞 16자 (재현성 검증용). 없으면 None.

    `full=True` 는 출력 봉인용이다 (F68) — 인용되는 숫자를 지키는 값이므로
    절단하지 않는다.
    """
    if path is None:
        return None
    p = Path(path)
    if not p.exists() or not p.is_file():
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest() if full else h.hexdigest()[:16]


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
        # ★ 18차 F — 승자가 **모호하면** 조용히 고르지 않는다.
        #
        #   `chunk_files` 는 mtime 순으로 정렬하고 동률이면 이름으로 tie-break
        #   하는데, 이름의 `chunk_idx` 는 **프로세스마다 독립**이라 시간 의미가
        #   없다. 즉 같은 조건이 두 청크에 다른 내용으로 있고 mtime 까지 같으면,
        #   아무 근거 없이 한쪽 곡선을 버리면서 그 사실이 아무 데도 안 남는다.
        #   그 선택이 downstream fit 의 입력을 바꾼다.
        mt = {i: f.stat().st_mtime_ns for i, f in enumerate(files)}
        dup = df[df.duplicated(kk, keep=False)]
        ambiguous = []
        for kv, g in dup.groupby(kk, sort=False):
            chunks = sorted(set(g["_chunk"]))
            if len(chunks) < 2:
                continue
            top = max(chunks, key=lambda c: mt[c])
            tied = [c for c in chunks if mt[c] == mt[top]]
            if len(tied) < 2:
                continue                      # 최신이 유일 → 기존 규칙대로
            cols = [c for c in g.columns if c != "_chunk"]
            blocks = {c: g[g["_chunk"] == c][cols]
                      .sort_values(cols).to_csv(index=False) for c in tied}
            if len(set(blocks.values())) > 1:  # 내용이 실제로 다르다
                ambiguous.append((kv, [files[c].name for c in tied]))
        if ambiguous:
            head = "; ".join(f"{kv} ← {names}" for kv, names in ambiguous[:5])
            raise RuntimeError(
                f"청크 경계에서 최신본을 결정할 수 없습니다 ({len(ambiguous)}건): "
                f"{head}. 같은 조건이 여러 청크에 **다른 내용**으로 있는데 "
                f"mtime 이 같아 순서가 없습니다 (chunk_idx 는 프로세스마다 "
                f"독립이라 이름 정렬에 시간 의미가 없습니다). 재실행할 청크를 "
                f"지우고 다시 만드십시오 — 조용히 한쪽을 고르면 그 선택이 "
                f"downstream fit 입력을 바꿉니다.")

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
    except OSError as e:
        # ★ F53 — Windows 는 없는 PID 에 대해 ProcessLookupError 가 아니라
        #   `OSError [WinError 87] 매개 변수가 틀립니다` 를 낸다. 안 잡으면
        #   예외가 그대로 올라와 stale lock 을 영영 회수하지 못한다.
        #   WinError 87 = 그런 PID 없음 → 죽었다. 그 밖은 **판단 불가 → 살아 있다**
        #   (모르는 상태에서 남의 lock 을 뺏는 것보다 안전하다).
        return getattr(e, "winerror", None) != 87
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
    """manifest.yaml 기록 (기존 내용에 병합).

    ★ F70 — 병합은 `existing.update()` 라 **얕다**. grid 와 fit 을 같은 디렉터리에
    쓰면 fit manifest 가 grid 의 핵심 실행 필드(solver·protocol·조건 수)를 덮어써서,
    나중에 보면 곡선을 누가 어떤 solver 로 만들었는지 알 수 없다. `run_type` 이
    바뀌는 순간 이전 기록을 `manifest_<옛run_type>.yaml` 로 보존한다.
    (곡선 provenance 의 정본은 `curves_manifest.yaml` 이며 이건 안전망이다.)
    """
    path = manifest_path(out_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if path.exists():
        existing = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    old_t, new_t = existing.get("run_type"), payload.get("run_type")
    if old_t and new_t and old_t != new_t:
        keep = path.with_name(f"manifest_{old_t}.yaml")
        if not keep.exists():
            keep.write_text(yaml.safe_dump(existing, allow_unicode=True,
                                           sort_keys=False), encoding="utf-8")
        existing = {}          # 다른 실행의 필드를 물려받지 않는다
    existing.update(payload)
    path.write_text(yaml.safe_dump(existing, allow_unicode=True, sort_keys=False),
                    encoding="utf-8")
    return path


def base_manifest(cfg_hash: str, extra: dict | None = None,
                  out_dir=None, inputs=None, sealed: dict | None = None) -> dict:
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
    # ★ F56 — `sealed` 이 오면 **재해시하지 않고 시작 봉인 map 을 그대로** 쓴다.
    #   종료 시점에 다시 해시하면, 실행 중 입력이 바뀌었을 때 "행은 옛 입력에서
    #   계산됐는데 manifest 는 새 입력"인 artifact 가 만들어진다.
    if sealed is not None:
        m["input_sha256"] = dict(sealed)
        m["input_sha256_source"] = "sealed_at_start"
        # 종료 시점 값도 따로 기록해 대조할 수 있게 한다
        m["input_sha256_at_end"] = {k: file_digest(k) for k in sealed}
        m["inputs_changed_during_run"] = bool(
            m["input_sha256_at_end"] != m["input_sha256"])
    elif inputs:
        m["input_sha256"] = {str(p): file_digest(p) for p in inputs if p is not None}
        m["input_sha256_source"] = "hashed_at_end"
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

_RESTART_SOURCES = {"warm", "base_init", "random"}


def _restart_ok(e) -> bool:
    """restart 원소 하나의 타입·유한성 검사 (F61).

    키 존재만 보면 `{"p": null, "J": null, "i": null, "source": null}` 이 통과한다.
    손상된 multi-start 기록을 인용 가능으로 승인하게 된다.
    """
    import math

    if not isinstance(e, dict):
        return False
    p_, j_, i_, s_ = e.get("p"), e.get("J"), e.get("i"), e.get("source")
    if not isinstance(p_, list) or len(p_) != 4:
        return False
    if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in p_):
        return False
    if not isinstance(j_, (int, float)) or not math.isfinite(j_):
        return False
    if not isinstance(i_, int) or isinstance(i_, bool) or i_ < 0:
        return False
    return s_ in _RESTART_SOURCES


def _sha256_lines(items) -> str:
    return hashlib.sha256("\n".join(items).encode()).hexdigest()


def fits_seal(fits_path, cond_ids=None, objective_order=None) -> dict:
    """★ F68 — 출력 자체를 봉인한다.

    여섯 라운드 동안 "인용 가능성"을 판정하는 장치를 강화하면서, 정작 인용되는
    **숫자는 한 번도 검사하지 않았다.** validator 가 fits 에서 읽는 열은
    `run_sig` 와 `restarts_json` 둘뿐이었다. 그래서 리뷰가 실제로 재현해 보인
    조작들이 전부 `ok=True` 였다 — 값 변조(`lam_pe_hat=0.999`), 열 전체 이동
    (`+0.5`), 행 삭제(3조건 → 1조건).

    봉인 내용:
      file_sha256   파일 전체. 한 바이트라도 바뀌면 깨진다
      n_rows        행 삭제/추가를 잡는다
      key_sha256    (cond_id, objective) 정렬 키 집합
      cond_sha256   조건 집합 — run_spec.condition_ids_sha256 과 대조된다
      n_conditions / n_objectives

    `cond_ids`·`objective_order` 를 주면 **완전성**도 같이 계산한다: 기대 격자
    (조건 × 목적함수)에 대해 missing/extra/duplicated 를 돌려준다. 이 셋이
    비어 있지 않은 채로 봉인하면 분모가 조용히 달라진다.
    """
    import pandas as pd

    fp = Path(fits_path)
    df = pd.read_parquet(fp, columns=["cond_id", "objective"])
    keys = [f"{c}|{o}" for c, o in zip(df["cond_id"].astype(str),
                                       df["objective"].astype(str))]
    conds = sorted(set(df["cond_id"].astype(str)))
    objs = sorted(set(df["objective"].astype(str)))
    seen = Counter(keys)
    out = {
        "file_sha256": file_digest(fp, full=True),
        "n_rows": int(len(df)),
        "key_sha256": _sha256_lines(sorted(keys)),
        "cond_sha256": _sha256_lines(conds)[:16],
        "n_conditions": len(conds),
        "n_objectives": len(objs),
        "objectives": objs,
    }
    if cond_ids is not None and objective_order is not None:
        want = {f"{c}|{o}" for c in cond_ids for o in objective_order}
        out["missing"] = sorted(want - set(keys))
        out["extra"] = sorted(set(keys) - want)
        out["duplicated"] = sorted(k for k, n in seen.items() if n > 1)
    return out


#: 곡선 한 조건을 정의하는 identity 필드 (Condition 과 1:1)
_COND_FIELDS = ("lli", "lam_pe", "lam_ne", "lam_pe_type", "lam_ne_type",
                "noise", "seed")


#: ★ 13차 발견 1 — fitting 결과를 직접 결정하는 물리 열. 하나라도 없으면
#: 곡선이 무엇을 재현하는지 증명되지 않는다 (특히 `v_full_noisy` 가 없으면
#: fitting 이 경고 없이 `v_full` 로 fallback 해 격자의 2/3 가 noiseless 가 된다).
_PHYS_COLS = ("protocol", "q_mah", "v_pe", "v_ne", "v_full", "v_full_noisy")


def _verify_observed_curves(curves_path: Path, spec: dict) -> dict:
    """★ 12차 발견 1 + 13차 발견 1 — 관측 곡선의 identity·완전성·**물리 정합**.

    identity/완전성 (12차):
      · 조건마다 7개 identity 필드가 **단일값**이고 유한한가
      · 그 값으로 만든 canonical `Condition.cond_id` 가 기록 ID 와 같은가
      · 조건마다 행 수가 서명된 `postprocess.n_interp` 와 같은가
      · `x_norm` 이 정확히 `linspace(0, 1, n_interp)` 인가 (13차: 공통이기만
        하면 통과하던 것을 절대 격자로 강화 — 축소된 창이 통과했다)

    물리 정합 (13차 — 이게 없으면 LAM/LLI 가 0% ↔ 50% 로 바뀔 수 있다):
      · 필수 물리 열 존재 (`_PHYS_COLS`)
      · 조건별 `q_mah` 단일값·유한·양수 — fitting 이 첫 행으로 r=q/q_ref 를 만든다
      · 모든 `v_*` 유한 — 목적함수가 비유한점을 조용히 버려 표본이 줄어든다
      · `v_full == v_pe - v_ne` — 아니면 full-cell target 과 두 전극이 같은 셀이 아니다
      · `v_full_noisy == add_noise(v_full, noise, seed)` — 같은 runtime 을 서명하므로
        결정적으로 재계산 가능
      · 조건별 `protocol` 단일값이며 `grid_run_spec.protocol_unified` 와 일치

    행의 저장 순서는 강제하지 않는다 (fitting 이 조건별로 x_norm 정렬 후 쓴다).
    """
    import numpy as np

    from src.curves import add_noise
    from src.grid import Condition

    checks: dict[str, tuple[bool, str]] = {}
    n_interp = ((spec.get("postprocess") or {}) or {}).get("n_interp")
    want_proto = spec.get("protocol_unified")
    try:
        df = pd.read_parquet(curves_path,
                             columns=["cond_id", "x_norm", *_COND_FIELDS])
    except Exception as e:  # noqa: BLE001
        checks["관측조건_스키마"] = (
            False, f"곡선에 조건 identity 열이 없다 ({e}) — 12차 이전 형식이다. "
                   f"곡선을 다시 생성해야 모집단을 증명할 수 있다")
        return checks

    # ★ 13차 발견 1 — 물리 열은 **있는지부터** 본다. 없으면 뒤 검사를 할 수 없고,
    #   그 자체가 실패다 (조용한 fallback 을 만드는 통로).
    try:
        phys = pd.read_parquet(curves_path, columns=["cond_id", *_PHYS_COLS])
    except Exception as e:  # noqa: BLE001
        checks["관측_필수열"] = (
            False, f"필수 물리 열 {list(_PHYS_COLS)} 중 없는 것이 있다 ({e}) — "
                   f"곡선이 무엇을 재현하는지 증명되지 않는다 (13차 발견 1)")
        phys = None
    else:
        checks["관측_필수열"] = (True, "")

    bad_multi, bad_id, bad_rows, bad_x = [], [], [], []
    bad_q, bad_vfin, bad_vsum, bad_noise, bad_proto = [], [], [], [], []
    ref_grid = (np.linspace(0.0, 1.0, n_interp)
                if isinstance(n_interp, int) and n_interp >= 1 else None)
    for cid, g in df.groupby("cond_id", sort=True):
        cid = str(cid)
        uniq = {k: g[k].unique() for k in _COND_FIELDS}
        if any(len(v) != 1 for v in uniq.values()):
            bad_multi.append(
                f"{cid}({[k for k, v in uniq.items() if len(v) != 1]})")
            continue
        vals = {k: v[0] for k, v in uniq.items()}
        try:
            cond = Condition(
                lli=float(vals["lli"]), lam_pe=float(vals["lam_pe"]),
                lam_ne=float(vals["lam_ne"]),
                lam_pe_type=str(vals["lam_pe_type"]),
                lam_ne_type=str(vals["lam_ne_type"]),
                noise=float(vals["noise"]), seed=int(vals["seed"]))
        except Exception as e:  # noqa: BLE001
            bad_id.append(f"{cid}(조건 재구성 불가: {type(e).__name__})")
            continue
        if cond.cond_id != cid:
            bad_id.append(f"{cid}(재계산 {cond.cond_id})")
        if isinstance(n_interp, int) and len(g) != n_interp:
            bad_rows.append(f"{cid}({len(g)}행, {n_interp} 필요)")
        x = g["x_norm"].to_numpy(dtype=float)
        if not np.all(np.isfinite(x)) or len(set(x.tolist())) != len(x):
            bad_x.append(f"{cid}(비유한 또는 중복 x_norm)")
            continue
        xs = np.sort(x)
        # ★ 13차 발견 1 — "모든 조건이 같은 격자" 만으로는 부족하다. 전 조건이
        #   함께 [0.2, 0.8] 로 줄어도 통과했다. 서명된 n_interp 의 0→1 절대
        #   격자와 대조한다.
        if ref_grid is None:
            bad_x.append(f"{cid}(n_interp 가 서명에 없어 격자를 대조할 수 없다)")
        elif len(xs) != len(ref_grid) or not np.allclose(xs, ref_grid,
                                                         rtol=0.0, atol=1e-12):
            bad_x.append(f"{cid}(x_norm 이 linspace(0,1,{n_interp}) 가 아니다: "
                         f"[{xs[0]:.6g}, {xs[-1]:.6g}])")

        # ── 물리 정합 (13차 발견 1) ──
        if phys is None:
            continue
        pg = phys[phys["cond_id"] == cid]
        q = pg["q_mah"].to_numpy(dtype=float)
        if len(set(q.tolist())) != 1 or not np.isfinite(q[0]) or q[0] <= 0:
            bad_q.append(f"{cid}(고유값 {len(set(q.tolist()))}개, 첫값 {q[0]})")
        pr = set(pg["protocol"].astype(str))
        if len(pr) != 1 or (want_proto is not None
                            and next(iter(pr)) != str(want_proto)):
            bad_proto.append(f"{cid}({sorted(pr)} vs 서명 {want_proto})")
        vs = {c: pg[c].to_numpy(dtype=float)
              for c in ("v_pe", "v_ne", "v_full", "v_full_noisy")}
        nonfinite = {c: int((~np.isfinite(a)).sum()) for c, a in vs.items()}
        if any(nonfinite.values()):
            bad_vfin.append(f"{cid}({ {c: n for c, n in nonfinite.items() if n} })")
            continue          # 비유한이면 아래 정합 검사는 의미가 없다
        d_sum = float(np.max(np.abs(vs["v_full"] - (vs["v_pe"] - vs["v_ne"]))))
        if d_sum > 1e-12:
            bad_vsum.append(f"{cid}(max|v_full-(v_pe-v_ne)| = {d_sum:.3g})")
        # noise 실현값 재계산 — 저장 순서와 무관하게 x_norm 정렬 기준으로 본다
        order = np.argsort(pg["x_norm"].to_numpy(dtype=float)) \
            if "x_norm" in pg.columns else np.argsort(x)
        _sig = float(vals["noise"])
        _seed = int(vals["seed"])
        want_noisy = add_noise(vs["v_full"][order], _sig, _seed)
        d_noise = float(np.max(np.abs(vs["v_full_noisy"][order] - want_noisy)))
        if d_noise > 1e-12:
            bad_noise.append(f"{cid}(max|Δ| = {d_noise:.3g}, noise={_sig})")

    checks["관측조건_단일성"] = (
        not bad_multi,
        f"{len(bad_multi)}개 조건의 truth 필드가 한 값이 아니다: {bad_multi[:3]}")
    checks["관측조건_ID결합"] = (
        not bad_id,
        f"{len(bad_id)}개 조건의 cond_id 가 그 행들의 물리조건에서 재계산한 "
        f"canonical ID 와 다르다: {bad_id[:3]} — label 이 truth 와 어긋났다")
    checks["관측조건_행수"] = (
        isinstance(n_interp, int) and not bad_rows,
        f"n_interp 가 서명에 없거나({n_interp}) 행 수가 다른 조건이 "
        f"{len(bad_rows)}개다: {bad_rows[:3]}")
    checks["관측_x_norm_공통격자"] = (
        not bad_x,
        f"{len(bad_x)}개 조건의 x_norm 이 비유한·중복이거나 "
        f"linspace(0,1,n_interp) 가 아니다: {bad_x[:3]}")
    # ── 13차 발견 1: 물리 정합 ──
    if phys is not None:
        checks["관측_q_mah"] = (
            not bad_q,
            f"{len(bad_q)}개 조건의 q_mah 가 단일값·유한·양수가 아니다: "
            f"{bad_q[:3]} — fitting 은 첫 행으로 r=q/q_ref 를 만들므로 "
            f"섞이면 LAM/LLI 환산이 통째로 달라진다")
        checks["관측_전압_유한"] = (
            not bad_vfin,
            f"{len(bad_vfin)}개 조건에 비유한 전압이 있다: {bad_vfin[:3]} — "
            f"목적함수가 그 점을 조용히 버려 실제 표본이 줄어든다")
        checks["관측_전압_정합"] = (
            not bad_vsum,
            f"{len(bad_vsum)}개 조건에서 v_full ≠ v_pe - v_ne: {bad_vsum[:3]} — "
            f"full-cell target 과 두 전극 곡선이 같은 합성 셀이 아니다")
        checks["관측_noise_재현"] = (
            not bad_noise,
            f"{len(bad_noise)}개 조건의 v_full_noisy 가 "
            f"add_noise(v_full, noise, seed) 와 다르다: {bad_noise[:3]}")
        checks["관측_protocol"] = (
            not bad_proto,
            f"{len(bad_proto)}개 조건의 protocol 이 단일값이 아니거나 서명된 "
            f"protocol_unified 와 다르다: {bad_proto[:3]}")
    return checks


#: ★ 14차 발견 1 — noise family 의 키. noise·seed 를 뺀 truth identity 다.
_FAMILY_FIELDS = ("lli", "lam_pe", "lam_ne", "lam_pe_type", "lam_ne_type")


def _verify_noise_families(curves_path: Path, spec: dict, d: Path) -> dict:
    """★ 14차 발견 1 — noise family 교차 invariant.

    noise 는 solve **이후에만** 얹히므로(`src/grid.py`: `add_noise(curves["v_full"],
    ...)`) 같은 (lli, lam_pe, lam_ne, 유형) family 의 멤버는 clean truth 를
    공유해야 한다. 조건별 검사(`_verify_observed_curves`)는 전부
    `groupby("cond_id")` 안이라 **조건 사이** 갈림을 못 본다 — 리뷰 실측:
    noise=0 멤버 q=4000·4.2V, noise=0.005 멤버 q=2000·3.2V 인 producer 가
    ok=True 를 받았다. 그러면 같은 truth 를 놓고 noise 조건마다 다른 셀을
    fitting 하게 되어 degeneracy 판별의 분자·분모가 함께 어긋난다.

      1. family 마다 서명된 noise 집합(`spec.noise`)을 **정확히 한 번씩** 가진다
      2. family 가 observed / failed 로 쪼개지면 실패
      3. observed family 안 q_mah 최대 편차 ≤ 1e-6 mAh
      4. x_norm 정렬 후 v_pe·v_ne·v_full pointwise 최대 편차 ≤ 1e-10 V
         (실측 2-worker 샘플에서 셋 다 정확히 0 — 같은 solve 의 후처리라 결정적)
    """
    import numpy as np

    checks: dict[str, tuple[bool, str]] = {}
    want_noise = spec.get("noise")
    ok_want = (isinstance(want_noise, (list, tuple)) and len(want_noise) > 0
               and all(isinstance(v, (int, float)) and not isinstance(v, bool)
                       and np.isfinite(v) for v in want_noise)
               and len({float(v) for v in want_noise}) == len(want_noise))
    checks["관측_noise_기대집합"] = (
        ok_want,
        f"grid_run_spec.noise 가 없거나 유한 실수의 중복 없는 목록이 아니다 "
        f"({want_noise!r}) — family 완전성을 대조할 서명된 기준이 없다 "
        f"(14차 발견 1, grid_sig_version 5 필수 항목)")
    if not ok_want:
        return checks
    want = sorted(float(v) for v in want_noise)

    cols = ["cond_id", "x_norm", *_FAMILY_FIELDS, "noise", "q_mah",
            "v_pe", "v_ne", "v_full"]
    try:
        df = pd.read_parquet(curves_path, columns=cols)
    except Exception as e:  # noqa: BLE001
        checks["관측_noise_family_스키마"] = (
            False, f"family 검증에 필요한 열을 읽지 못했다 ({e})")
        return checks

    def _famkey(lli, pe, ne, pt, nt):
        return (float(lli), float(pe), float(ne), str(pt), str(nt))

    fams: dict[tuple, list] = {}
    for cid, g in df.groupby("cond_id", sort=True):
        # 필드 단일성·유한성은 관측조건_단일성/ID결합이 이미 검사한다 — 여기서는
        # 첫 행을 family 좌표로 쓴다 (재구성 불가면 그 검사가 실패한다).
        try:
            key = _famkey(*(g[k].iloc[0] for k in _FAMILY_FIELDS))
            noise = float(g["noise"].iloc[0])
        except Exception:  # noqa: BLE001 — 단일성 검사가 잡는다
            continue
        fams.setdefault(key, []).append((noise, str(cid), g))

    bad_set, bad_q, bad_v = [], [], []
    # ★ 15차 발견 D — 정렬 키는 family 좌표(kv[0])만이다. `key=repr` 는 값의
    #   DataFrame 까지 `to_string()` 으로 렌더해 검증을 수십 분으로 만들었다
    #   (실측 16.47s → 0.838s). 판정은 동일하다.
    for key, members in sorted(fams.items(), key=lambda kv: kv[0]):
        noises = sorted(n for n, _, _ in members)
        if noises != want:
            bad_set.append(f"{key}(noise {noises} ≠ 서명 {want})")
        qs = [float(g["q_mah"].iloc[0]) for _, _, g in members]
        if max(qs) - min(qs) > 1e-6:
            bad_q.append(f"{key}(q_mah 편차 {max(qs) - min(qs):.6g} mAh)")
        arrs = []
        for _, _, g in sorted(members, key=lambda t: t[0]):
            gg = g.sort_values("x_norm")
            arrs.append({c: gg[c].to_numpy(dtype=float)
                         for c in ("v_pe", "v_ne", "v_full")})
        base = arrs[0]
        if any(len(a["v_full"]) != len(base["v_full"]) for a in arrs[1:]):
            bad_v.append(f"{key}(멤버 간 행 수 불일치)")
            continue
        dev = max((float(np.max(np.abs(a[c] - base[c])))
                   for a in arrs[1:] for c in ("v_pe", "v_ne", "v_full")),
                  default=0.0)
        if dev > 1e-10:
            bad_v.append(f"{key}(max|Δv| = {dev:.3g} V)")

    # 규칙 2 — failed.csv 의 condition payload 로 실패 family 좌표를 만든다.
    #   payload 파손·ID 불일치는 실패목록_ID결합이 fail-closed 로 잡으므로
    #   여기서는 파싱되는 행만 본다.
    # ★ 14차 2차 발견 1 — noise 를 **버리지 않는다**. 예전에는 family `set` 으로
    #   축약해서, noise {0, 0.001} 만 failed 이고 0.005 는 의도 집합에도 없는
    #   family 가 통과했다 (리뷰 실측: ok=True, fail=[]). 그러면 의도·실패
    #   조건 수와 noise 별 제외율이 달라져 인용 모집단의 근거가 무효가 된다.
    fail_fams: dict[tuple, list[float]] = {}
    fp = d / "failed.csv"
    if fp.exists():
        import csv as _csv
        with open(fp, newline="", encoding="utf-8") as f:
            for row in _csv.DictReader(f):
                try:
                    c = json.loads(row.get("condition") or "{}")
                    key = _famkey(c["lli"], c["lam_pe"], c["lam_ne"],
                                  c["lam_pe_type"], c["lam_ne_type"])
                    fail_fams.setdefault(key, []).append(float(c["noise"]))
                except Exception:  # noqa: BLE001
                    continue
        split = sorted(set(fams) & set(fail_fams))
    else:
        split = []

    # 전부 failed 인 family 는 허용하되(관측 모집단에 없으므로 분할이 아니다),
    # 그 family 도 서명된 noise 집합을 **정확히 한 번씩** 가져야 한다.
    # 교차 family 는 위 분할 검사가 이미 실패시키므로 여기서 제외한다.
    bad_fail_set = []
    for key, noises in sorted(fail_fams.items(), key=lambda kv: kv[0]):
        if key in fams:
            continue
        got = sorted(noises)
        if got != want:
            bad_fail_set.append(f"{key}(noise {got} ≠ 서명 {want})")

    checks["관측_noise_family_완전성"] = (
        not bad_set,
        f"{len(bad_set)}개 family 의 noise 집합이 서명된 {want} 와 다르다: "
        f"{bad_set[:3]} — noise 축 표본이 조용히 달라졌다")
    checks["관측_noise_family_분할"] = (
        not split,
        f"{len(split)}개 family 가 observed 와 failed 에 걸쳐 있다: "
        f"{[repr(k) for k in split[:3]]} — 같은 truth 인데 noise 조건마다 "
        f"모집단이 다르면 degeneracy 분모가 어긋난다")
    checks["실패_noise_family_완전성"] = (
        not bad_fail_set,
        f"{len(bad_fail_set)}개 fully-failed family 의 noise 집합이 서명된 "
        f"{want} 와 다르다(누락 또는 중복): {bad_fail_set[:3]} — guard 불능은 "
        f"noise 와 무관하므로 family 전체가 같은 판정을 받아야 한다. 어긋나면 "
        f"의도·실패 조건 수와 noise 별 제외율이 달라져 인용 모집단의 근거가 "
        f"무효다 (14차 2차 발견 1)")
    checks["관측_noise_family_q_mah"] = (
        not bad_q,
        f"{len(bad_q)}개 family 안에서 q_mah 가 1e-6 mAh 넘게 갈린다: "
        f"{bad_q[:3]} — noise 는 solve 이후에만 얹히므로 clean 용량은 "
        f"family 안에서 같아야 한다")
    checks["관측_noise_family_전압"] = (
        not bad_v,
        f"{len(bad_v)}개 family 안에서 clean 전압(v_pe·v_ne·v_full)이 "
        f"1e-10 V 넘게 갈린다: {bad_v[:3]} — 같은 truth 의 solve 가 아니다")
    return checks


def _verify_failed_reasons(d: Path, spec: dict, ds: dict) -> dict:
    """실패 행을 **서명된 recipe** 로 재검한다 (11차 발견 2·3).

    두 가지를 함께 본다.
      1. ID↔물리조건 결합 — 행의 `condition` payload 로 `Condition.cond_id` 를
         다시 만들어 CSV 의 `cond_id` 와 같아야 한다. 아니면 "그 ID 의 조건이
         실패했다"가 증명되지 않는다 (payload 만 불능인 위조).
      2. 불능성 재평가 — `infeasible:` 사유는 spec 의 `replay_recipe`
         (baseline·guards) + 서명된 완방상태로 `build_overrides` 를 다시 돌려
         정말 InfeasibleConditionError 가 나는지 확인한다.
    결정적 재검이 불가능한 사유(solver 실패 등)는 fail-closed 로 남긴다.
    """
    import csv as _csv

    from src.baseline import DischargedState as _DState
    from src.grid import Condition as _Cond
    from src.modes import Baseline as _Bl
    from src.modes import InfeasibleConditionError as _Infe
    from src.modes import build_overrides as _bov

    checks: dict[str, tuple[bool, str]] = {}
    recipe = (spec or {}).get("replay_recipe") or {}
    if not recipe.get("baseline"):
        checks["실패사유_recipe"] = (
            False, "grid_run_spec 에 replay_recipe(baseline·guards)가 없다 — "
                   "실패 라벨을 producer 기준으로 재검할 수 없다 (11차 발견 3)")
        return checks
    if not (d / "failed.csv").exists():
        return checks                     # 존재 검사는 호출부가 이미 했다
    try:
        _bl = _Bl(**{k: float(v) for k, v in recipe["baseline"].items()})
        _dst = _DState(**{k: float(ds[k])
                          for k in ("ne_primary", "ne_secondary", "pe")})
    except Exception as e:  # noqa: BLE001
        checks["실패사유_recipe"] = (
            False, f"서명된 recipe 로 baseline/완방상태를 구성하지 못했다: {e}")
        return checks

    _guards = recipe.get("guards") or {}
    _forged, _unbound, _unver = [], [], []
    with open(d / "failed.csv", newline="", encoding="utf-8") as f:
        for row in _csv.DictReader(f):
            cid = str(row.get("cond_id"))
            try:
                c = json.loads(row.get("condition") or "{}")
                cond = _Cond(lli=float(c["lli"]), lam_pe=float(c["lam_pe"]),
                             lam_ne=float(c["lam_ne"]),
                             lam_pe_type=str(c["lam_pe_type"]),
                             lam_ne_type=str(c["lam_ne_type"]),
                             noise=float(c["noise"]), seed=int(c["seed"]))
            except Exception as e:  # noqa: BLE001
                _unbound.append(f"{cid}(payload 파손: {type(e).__name__})")
                continue
            if cond.cond_id != cid:
                _unbound.append(f"{cid}(payload 의 canonical ID {cond.cond_id})")
                continue
            if not str(row.get("reason") or "").startswith("infeasible"):
                _unver.append(cid)
                continue
            try:
                _bov(cond.lli, cond.lam_pe, cond.lam_ne, cond.lam_pe_type,
                     cond.lam_ne_type, _bl, _dst, _guards)
            except _Infe:
                continue                  # 정말 불능 — 라벨이 참
            except Exception as e:  # noqa: BLE001
                _unver.append(f"{cid}(재평가 예외: {type(e).__name__})")
                continue
            _forged.append(cid)
    checks["실패목록_ID결합"] = (
        not _unbound,
        f"{len(_unbound)}행의 cond_id 가 그 행의 condition payload 에서 다시 "
        f"계산한 canonical ID 와 다르다: {_unbound[:3]} — 그 ID 의 조건이 "
        f"실패했다는 것이 증명되지 않는다 (11차 발견 2)")
    checks["실패사유_불능재검"] = (
        not _forged,
        f"guard 를 통과하는(=풀리는) 조건 {len(_forged)}건이 실패로 계상돼 "
        f"있다 — 모집단 임의 축소: {_forged[:3]}")
    checks["실패사유_미검증"] = (
        not _unver,
        f"{len(_unver)}건의 실패 사유가 결정적 재검 불가다 (solver 실패 등): "
        f"{_unver[:3]} — 봉인된 재실행 근거 없이 인용 모집단에서 제외할 수 없다")
    return checks


def validate_curves_provenance(curves_dir, repo_root=None) -> dict:
    """★ F74 — 곡선 producer 를 **독립적으로** 검증한다 (8차 리뷰 발견 1).

    검사: manifest 존재 · grid_run_spec/sig 존재 · **서명 재계산** · 시작 기록
    대조 · curves 재해시 · **모든 행의 grid_run_sig 일치** · 조건 집합 서명 대조 ·
    의도 = 관측 ⊎ 실패 ID 분할(F83b) · **실패 행의 ID↔조건 결합과 불능성
    재평가**(11차 발견 2·3, 서명된 `replay_recipe` 로) · 생성 시점 clean ·
    실행 중 코드 불변.

    호출자 cfg 를 받지 않는다 — 재검 기준은 producer 가 서명한 recipe 하나뿐
    이라, archive·격리 복원 등 어느 경로에서 불러도 같은 판정이 나온다.

    fitting 이 시작 전에 이걸 호출한다. 수제 parquet 은 `grid_run_sig` 열이
    없어서, 다른 config 의 resume 혼합은 행 서명이 갈려서 걸린다.

    ★ 신뢰 경계 (10차 자체 확인 1): 이 검증이 증명하는 것은 기록↔bytes 의
    **자기일관성**과 코드·설정·조건집합의 identity 다. curves_manifest 는
    untracked 라, **값 변조 후 digest 일체를 재계산해 넣는 위조**는 여기서
    구분할 수 없다 (형식적으로 완전한 기록이 되기 때문). 진본성의 앵커는
    저장소 이력이다 — git 에 커밋되는 artifacts/ 묶음(payload_sha256)과
    보고서에 렌더·커밋되는 digest 를 대조해야 진본성이 성립한다.
    """
    d = Path(curves_dir)
    checks: dict[str, tuple[bool, str]] = {}
    mp = d / "curves_manifest.yaml"
    man = (yaml.safe_load(mp.read_text(encoding="utf-8")) or {}) if mp.exists() else {}
    checks["producer_manifest"] = (bool(man), "curves_manifest.yaml이 없다")
    spec = man.get("grid_run_spec") or {}
    sig = man.get("grid_run_sig")
    checks["grid_spec_존재"] = (bool(spec) and bool(sig),
                                "grid_run_spec/sig가 없다 (F74 이전 산출물)")
    # ★ F82b/10차 발견 2-c — 버전과 필수 물리 필드를 강제한다. 예전에는
    #   discharged=None 으로 만든 spec 도, F82 이전 버전도 그대로 통과했다.
    checks["grid_sig_version"] = (
        spec.get("grid_sig_version") == 5,
        f"grid_sig_version이 {spec.get('grid_sig_version')}이다 (5 필요 — "
        f"14차: 서명된 noise 집합 미포함 형식은 family 완전성을 대조할 수 없다)")
    # ★ 12차 발견 2 — 실제로 쓰인 solver 가 서명에 있어야 한다.
    _es = spec.get("effective_solver") or {}
    checks["effective_solver_identity"] = (
        bool(_es.get("effective_class")) and bool(_es.get("pybamm"))
        and _es.get("pybammsolvers") is not None and _es.get("casadi") is not None,
        f"effective_solver(실제 클래스·backend 버전)가 서명에 없다: {_es}")
    # ★ 12차 발견 6 — replay_recipe 는 실패 건수와 무관하게 v4 의 필수 항목이다
    #   (예전에는 n_failed>0 일 때만 검사해 실패 0건 producer 가 빠져나갔다).
    # ★ 13차 발견 9 — 존재만 보면 `baseline={"bogus": 1.0}` 도 통과한다.
    #   Baseline 필수 키 **집합**과 유한 실수, guards 형식을 실패 건수와
    #   무관하게 검사한다 (실패 0건 producer 도 v4 schema 를 주장한다).
    _rr = spec.get("replay_recipe") or {}
    _rb = _rr.get("baseline")
    _rg = _rr.get("guards")
    _why = None
    if not isinstance(_rb, dict) or not isinstance(_rg, dict):
        _why = f"replay_recipe(baseline·guards)가 없거나 dict 가 아니다: {sorted(_rr) if _rr else None}"
    else:
        import math as _m
        from dataclasses import fields as _dc_fields

        from src.modes import Baseline as _Bl
        _want = {f.name for f in _dc_fields(_Bl)}
        _got = set(_rb)
        if _got != _want:
            _why = (f"baseline 키 집합이 Baseline 과 다르다 "
                    f"(없음 {sorted(_want - _got)[:3]}, 잉여 {sorted(_got - _want)[:3]})")
        else:
            _badv = [k for k, v in _rb.items()
                     if not isinstance(v, (int, float))
                     or isinstance(v, bool)
                     or not _m.isfinite(v)]
            if _badv:
                _why = f"baseline 값이 유한 실수가 아니다: {_badv[:3]}"
            else:
                # ★ 14차 발견 5 — 예전 검사는 **아무 키나 허용하고 bool 도
                #   통과**시켰다. 오타 키(`max_mode_valu`)는 replay 의
                #   `g.get(키, 기본값)` 에서 조용히 무시돼 서명된 recipe 와
                #   실제 재검 기준이 달랐다. canonical 3-key 정확 일치 +
                #   bool 거부 + 물리 범위를 요구한다 (producer 는
                #   `canonical_guards()` 로 채워 서명한다).
                from src.modes import canonical_guards as _cg
                if set(_rg) != {"max_mode_value", "max_porosity", "min_vf"}:
                    _why = (f"guards 키 집합이 canonical 3-key 가 아니다: "
                            f"{sorted(_rg)}")
                else:
                    try:
                        if _cg(_rg) != {k: float(v) for k, v in _rg.items()}:
                            _why = f"guards 값이 canonical 정규형이 아니다: {_rg}"
                    except (ValueError, TypeError) as _e:
                        _why = f"guards 가 유효하지 않다: {_e}"
    checks["replay_recipe_schema"] = (_why is None, _why or "")
    _ds = spec.get("discharged_state")
    import math as _math
    _ds_ok = (isinstance(_ds, dict)
              and all(isinstance(_ds.get(k), (int, float))
                      and _math.isfinite(_ds.get(k)) and _ds.get(k) >= 0
                      for k in ("ne_primary", "ne_secondary", "pe")))
    checks["완방상태_서명"] = (
        _ds_ok, f"discharged_state가 없거나 유효하지 않다: {_ds}")
    _dsha = spec.get("discharged_state_sha")
    checks["완방상태_digest"] = (
        isinstance(_dsha, str) and len(_dsha) == 64,
        f"discharged_state_sha가 full digest(64자)가 아니다: {_dsha}")
    if spec and sig:
        recomputed = hashlib.sha1(
            json.dumps(spec, sort_keys=True, default=str).encode()).hexdigest()[:12]
        checks["grid_sig_재계산"] = (
            recomputed == str(sig),
            f"spec을 다시 해시하면 {recomputed}인데 기록은 {sig}다")

    sp = d / "curves_manifest_start.yaml"
    start = (yaml.safe_load(sp.read_text(encoding="utf-8")) or {}) if sp.exists() else {}
    checks["시작기록_존재"] = (bool(start), "curves_manifest_start.yaml이 없다")
    if start and sig:
        checks["시작기록_서명일치"] = (
            str(start.get("grid_run_sig")) == str(sig),
            f"시작 서명 {start.get('grid_run_sig')} ≠ 종료 {sig}")
        checks["생성시점_clean"] = (
            start.get("git_dirty") is False,
            "곡선이 dirty worktree에서 생성됐다")
    checks["실행중_코드불변"] = (
        man.get("source_digest_changed_during_run") is False,
        "곡선 생성 도중 src/tools/configs가 바뀌었다")

    cp = d / "curves.parquet"
    if not cp.exists():
        checks["curves_존재"] = (False, "curves.parquet이 없다")
    else:
        checks["curves_재해시"] = (
            bool(man.get("curves_sha256"))
            and file_digest(cp, full=True) == man.get("curves_sha256"),
            "curves.parquet이 manifest의 digest와 다르다")
        try:
            df = pd.read_parquet(cp, columns=["cond_id", "grid_run_sig"])
            sigs = set(df["grid_run_sig"].astype(str))
            checks["행별_grid서명"] = (
                sigs == {str(sig)},
                f"행 서명이 {sorted(sigs)[:3]}이다 ({sig} 필요) — "
                f"다른 config/코드의 resume 혼합이거나 수제 parquet이다")
        except Exception as e:  # noqa: BLE001
            checks["행별_grid서명"] = (
                False, f"grid_run_sig 열을 읽지 못했다 ({e}) — F74 이전이거나 수제 parquet")
            df = pd.read_parquet(cp, columns=["cond_id"])
        want = spec.get("condition_ids_sha256")
        got = hashlib.sha256("\n".join(
            sorted(set(df["cond_id"].astype(str)))).encode()).hexdigest()[:16]
        n_obs = df["cond_id"].nunique()
        checks["곡선_조건수"] = (
            man.get("n_curves") == n_obs,
            f"manifest n_curves {man.get('n_curves')} ≠ 실제 {n_obs}")
        # ★ F83/9차 발견 4 — 의도 = 관측 ⊎ 실패 **정확한 분할**을 강제한다.
        #   예전에는 이 항목이 `_참고` 로만 남아, 어려운 조건이 통째로 빠지고
        #   n_curves 를 맞춰 놓아도 통과했다 (INTENDED 3 / OBSERVED 2 / ok=True).
        #   그러면 recovery·degeneracy 비율의 **모집단이 조용히 달라진다**.
        n_int = spec.get("n_conditions_intended")
        n_fail = man.get("n_failed_total")
        checks["조건집합_분할"] = (
            isinstance(n_int, int) and isinstance(n_fail, int)
            and n_obs + n_fail == n_int,
            f"의도 {n_int} ≠ 관측 {n_obs} + 실패 {n_fail} — 조건이 조용히 빠졌다")
        # ★ F83b/10차 발견 1 — **개수가 아니라 ID 집합**으로 분할을 검사한다.
        #   개수만 세면, 관측 조건 하나를 다른 ID 로 바꿔치기해도 (의도 3 = 관측
        #   3 + 실패 0) 통과했다 (리뷰 실측: replacement_condition, AFTER_OK=True).
        #   "3,069조건" 은 guard 통과분이므로, 실패 924개가 정확히 나머지임을
        #   failed.csv 를 **다시 읽어** 증명해야 한다.
        obs_ids = set(df["cond_id"].astype(str))
        # ★ 12차 발견 1 — **관측 곡선 자체**의 identity·완전성을 검증한다.
        #   지금까지 곡선에서 독립적으로 읽은 것은 cond_id·grid_run_sig 뿐이라,
        #   조건 label 이 잘못 조립되거나(truth 필드 불일치) 점이 일부 누락돼도
        #   (48점 → 24점) 통과했다 (리뷰 실측: 둘 다 ok=True). fitting 은 그
        #   label 을 truth 로 채점하므로 복원오차·degeneracy 의 분자·분모가
        #   직접 달라진다. 위조가 아니라 **정상 실행의 회귀**를 잡는 검사다.
        checks.update(_verify_observed_curves(cp, spec))
        # ★ 14차 발견 1 — 조건별 검사는 groupby(cond_id) 안이라 **조건 사이**
        #   갈림을 못 본다. noise family 교차 invariant 는 별도 pass 로 검사한다.
        checks.update(_verify_noise_families(cp, spec, d))
        fail_ids = load_failed(d)
        if n_fail and not (d / "failed.csv").exists():
            checks["실패목록_존재"] = (False,
                f"n_failed_total={n_fail}인데 failed.csv가 없다")
        else:
            _rehash = hashlib.sha256(
                "\n".join(sorted(fail_ids)).encode()).hexdigest()[:16]
            checks["실패목록_재해시"] = (
                _rehash == man.get("failed_ids_sha256"),
                f"failed.csv 재해시 {_rehash} ≠ 기록 {man.get('failed_ids_sha256')}")
            _union = hashlib.sha256(
                "\n".join(sorted(obs_ids | fail_ids)).encode()).hexdigest()[:16]
            _overlap = obs_ids & fail_ids
            checks["조건집합_ID분할"] = (
                not _overlap and _union == want and len(fail_ids) == (n_fail or 0),
                f"관측∩실패 {len(_overlap)}건, (관측∪실패) 해시 {_union} ≠ "
                f"의도 {want}, 실패 {len(fail_ids)} ≠ 기록 {n_fail} — "
                f"ID 수준에서 분할이 성립하지 않는다")
        # ★ 10차 자체 확인 2 / 11차 발견 2·3 — 분할이 ID 수준에서 맞아도 "실패"
        #   라벨 자체가 위조면(= 풀리는 조건을 failed 로 재선언) 관측∪실패가
        #   불변이라 전부 통과하고, 모집단(분모)이 공격자 선택으로 줄어든다.
        #   재검은 **서명된 replay_recipe** 로만 한다 (11차 발견 3: 호출자 cfg 에
        #   의존하면 cfg 를 안 주는 경로가 재검을 통째로 건너뛰었다). 그리고
        #   행의 `condition` payload 로 canonical cond_id 를 다시 만들어 CSV 의
        #   `cond_id` 와 **결합**한다 (11차 발견 2: payload 는 진짜 불능인데 ID 는
        #   다른 조건인 위조가 통과했다).
        if n_fail:
            checks.update(_verify_failed_reasons(d, spec, _ds))
        checks["_참고_조건집합"] = (True, f"의도 {want} / 곡선 {got}")

    fail = [k for k, (ok, _) in checks.items() if not ok]
    return {"ok": not fail,
            "checks": {k: "통과" if ok else f"실패 — {why}"
                       for k, (ok, why) in checks.items()},
            "fail": fail,
            "reasons": [checks[k][1] for k in fail]}


def validate_provenance(run_dir, repo_root=None, fits_path=None) -> dict:
    """★ F38/F43 — 결과를 인용해도 되는 상태인지 **실제로** 검사한다.

    필드의 형식적 자기일관성만 보면 안 된다 (F43). 초판은
      · `input_sha256` 값이 truthy 한지만 보고 **파일을 다시 해시하지 않았고**
      · manifest 의 `run_signature` 와 fits 의 `run_sig` 문자열이 같은지만 보고
        **`run_spec` 을 다시 해시해 대조하지 않았으며**
      · `restarts_json` 의 **첫 행만** 형식을 확인했다.
    그래서 양쪽을 같은 가짜 문자열로 맞춘 위조가 그대로 통과했다 — 실제로
    이 저장소의 테스트 fixture(가짜 digest `aaaa1111`)가 통과하고 있었다.

    ★ 신뢰 경계 (10차 자체 확인 1): 이 검증이 증명하는 것은 기록↔bytes 의
    **자기일관성**과 코드·입력·조건집합의 identity 다. manifest 와 fits 는
    untracked 라, **출력 값 변조 후 fits_seal 일체를 재계산해 넣는 위조**는
    형식적으로 완전한 기록이 되어 여기서 구분할 수 없다 (10차 실측: *_hat
    +0.5 변조 + reseal → 추가 실패 검사 0개). 진본성의 앵커는 저장소 이력이다
    — git 에 커밋되는 artifacts/ 묶음(payload_sha256)과 보고서(RESULTS.md)에
    렌더·커밋되는 fits digest 를 대조해야 진본성이 성립한다.

    반환: {"ok": bool, "checks": {이름: "통과"|"실패 — 사유"}, "fail": [...], "reasons": [...]}
    """
    run_dir = Path(run_dir)
    root = Path(repo_root) if repo_root else Path(__file__).resolve().parent.parent
    man = {}
    mp = run_dir / "manifest.yaml"
    if mp.exists():
        man = yaml.safe_load(mp.read_text(encoding="utf-8")) or {}

    checks: dict[str, tuple[bool, str]] = {}
    checks["manifest_존재"] = (bool(man), "manifest.yaml이 없다")
    checks["config_hash"] = (bool(man.get("config_hash")), "config_hash가 비어 있다")
    checks["clean_worktree"] = (man.get("git_dirty") is False,
                                "dirty worktree 또는 실행 경로에 untracked 파일")

    # ── F50: 무엇이 **반드시** 있어야 하는지부터 정한다 ──
    #   임의 파일 하나만 있어도 통과하던 문제. reference 별 필수 입력을 못 박는다.
    spec0 = man.get("run_spec") or {}
    ref = str(spec0.get("reference") or man.get("reference") or "grid")
    digs = man.get("input_sha256") or {}
    hc_mismatch = ""
    need_kinds = ["curves.parquet", "base.yaml", "curves_manifest.yaml"]
    if ref == "halfcell":
        # ★ F64 — recipe 기록(.meta.yaml)도 봉인 대상이다. 배열만 있는 캐시는
        #   "어떤 branch·n_points 로 만들었는가"를 증명하지 못한다.
        #   ★ 파일명은 `<baseline>_<method>_<recipe>.json` 이라 recipe 해시가
        #     가운데 끼어든다. `_ocp.json` 으로 찾으면 **한 건도 안 걸린다** —
        #     실제로 F64 직후 모든 half-cell 실행이 `필수_입력_존재` 에서 막혔고,
        #     e2e smoke 가 이걸 잡았다 (단위 테스트의 fixture 는 이름을 직접
        #     지어서 통과했다).
        #   ★ 13차 자체 리뷰 — 그 뒤 부분문자열이 `"_ocp_"` 로 굳었는데, 이건
        #     **기본 method 에서만 우연히 맞는** 대용품이었다. `_ocpbias_`·
        #     `_sim_` 캐시에는 `"_ocp_"` 가 없어 정상 artifact 가 영원히
        #     거부된다 (실측: 모델 오차 민감도 fit 이 `['_ocp_']` 로 FAIL).
        #     run_spec 에 **실제 쓴 캐시 경로**가 이미 봉인돼 있으므로 그것을
        #     그대로 요구한다 — 대용품보다 좁고 정확하다.
        _hc = str(spec0.get("halfcell_cache") or "")
        _m = str((spec0.get("halfcell_recipe") or {}).get("method") or "")
        if _hc:
            _stem = _hc[:-5] if _hc.endswith(".json") else _hc
            need_kinds += [_hc, _stem + ".meta.yaml"]
            # 선언(recipe.method)과 봉인된 파일명이 어긋나면 무엇을 읽었는지
            # 증명되지 않는다 — 경로만 맞추고 method 를 속이는 길을 막는다.
            if _m and f"_{_m}_" not in _hc:
                hc_mismatch = f"halfcell_recipe.method={_m} 인데 봉인 캐시는 {_hc}"
        else:
            # F64 이전 artifact — 경로 기록이 없다. method 로 유도한다.
            need_kinds += [f"_{_m or 'ocp'}_", ".meta.yaml"]
    missing_kind = [k for k in need_kinds
                    if not any(k in str(x) for x in digs)]
    checks["필수_입력_존재"] = (
        not missing_kind and not hc_mismatch,
        hc_mismatch or f"필수 입력이 없다: {missing_kind}")

    # ── run_spec 필수 키 ──
    need_keys = ["sig_version", "objectives", "reference", "bounds", "bounds_preset",
                 "n_restarts", "warm_start", "v_col", "obj_cfg", "inventory",
                 "curves_sha", "base_config_sha", "git_commit", "source_digest",
                 "env", "sealed_inputs",
                 # ★ F67 — 설정이 아니라 **계산**을 고정하는 축들
                 "objective_order", "condition_ids_sha256", "n_conditions",
                 "selection", "optimizer",
                 # ★ F70 — upstream truth. "어떤 parquet 을 fit 했다"만으로는
                 #   'PyBaMM 합성 truth' 라는 이 연구의 전제가 봉인되지 않는다.
                 "producer_sha", "producer"]
    if ref == "halfcell":
        # ★ F64 — 캐시 파일만이 아니라 그 파일을 만든 recipe 도 필수다
        need_keys += ["halfcell_sha", "halfcell_cache", "halfcell_meta_sha",
                      "halfcell_recipe", "p_ini"]
    missing_key = [k for k in need_keys if k not in spec0 or spec0.get(k) is None]
    checks["run_spec_schema"] = (not missing_key,
                                 f"run_spec에 필수 키가 없거나 비었다: {missing_key}")
    # ★ F58 — 존재만 보면 안 된다. 버전 값도 확인한다.
    checks["sig_version"] = (spec0.get("sig_version") == 5,
                             f"sig_version이 {spec0.get('sig_version')}이다 (5 필요)")
    # ★ F67 — optimizer 정책은 서명에 있기만 하면 안 되고 완전해야 한다.
    _opt = spec0.get("optimizer") or {}
    _need_opt = [k for k in ("method", "adaptive", "n_restarts", "seed_scheme")
                 if k not in _opt or _opt.get(k) is None]
    checks["optimizer_정책"] = (not _need_opt,
                                f"optimizer 블록에 {_need_opt}가 없다")
    # ★ F70 — producer 가 주장하는 curves digest 와 우리가 봉인한 curves 가 같은가.
    #   producer 기록만 있고 다른 곡선을 읽었다면 전제가 성립하지 않는다.
    _prod = spec0.get("producer") or {}
    _cur_full = None
    for k, v in (digs or {}).items():
        if k.endswith("curves.parquet"):
            cand = Path(k) if Path(k).is_absolute() else root / k
            _cur_full = file_digest(cand, full=True) if cand.exists() else None
    checks["producer_곡선일치"] = (
        bool(_prod.get("curves_sha256")) and _cur_full is not None
        and _prod.get("curves_sha256") == _cur_full,
        f"producer가 기록한 곡선 {str(_prod.get('curves_sha256'))[:16]}과 "
        f"실제 읽은 곡선 {str(_cur_full)[:16]}이 다르다")

    # ★ F67 — 목적함수 순서는 warm 연쇄를 바꾼다. 정렬된 dict 와 별개로 남아야 하고,
    #   두 표현이 같은 집합을 가리켜야 한다.
    _order = spec0.get("objective_order")
    checks["목적함수_순서"] = (
        isinstance(_order, list) and bool(_order)
        and sorted(_order) == sorted(spec0.get("objectives") or {}),
        "objective_order가 objectives와 다른 집합이다")

    # ★ F56 — 시작 봉인 / run_spec / 종료 / 현재 파일 **네 곳이 모두 같아야** 한다.
    #   ★ F72 — 예전에는 시작↔spec, 시작↔종료 **두 쌍**만 보고, 종료 시점 map
    #   (`input_sha256_at_end`)의 내용은 보지 않은 채 `inputs_changed_during_run`
    #   이라는 **manifest 안의 boolean 자기신고**를 믿었다. 그래서
    #   `input_sha256_at_end={'forged': 'not-a-digest'}` 에 boolean 만 false 로
    #   맞춰도 통과했다. 네 곳을 **각각 다시 계산해** 비교한다.
    sp0 = man.get("start_provenance") or {}
    sealed_start = sp0.get("input_sha256") or {}
    sealed_spec = spec0.get("sealed_inputs") or {}
    sealed_end = man.get("input_sha256_at_end") or {}
    cross = []
    if sealed_start and sealed_spec and sealed_start != sealed_spec:
        cross.append("시작 봉인 ≠ run_spec.sealed_inputs")
    if sealed_start and digs and sealed_start != digs:
        cross.append("시작 봉인 ≠ 종료 manifest.input_sha256")
    if sealed_start and sealed_end and dict(sealed_start) != dict(sealed_end):
        cross.append(f"시작 봉인 ≠ 종료 재해시 (차이: "
                     f"{sorted(set(sealed_start) ^ set(sealed_end))[:3] or '값'})")
    if sealed_start and not sealed_end:
        cross.append("input_sha256_at_end가 없다 (F56 이전 산출물)")
    checks["입력봉인_교차일치"] = (not cross, "; ".join(cross))

    # ★ F72 — 계산이 **봉인한 바이트를 그대로** 읽었는가. digest 비교만으로는
    #   해시 시점과 읽기 시점 사이의 교체를 못 막는다 (리뷰가 run_fit 에서 재현).
    snap_dir = run_dir / "_inputs"
    snap_bad = []
    if not snap_dir.is_dir():
        snap_bad.append("_inputs 스냅샷이 없다 (F72 이전 산출물)")
    else:
        for key, dig in (sealed_start or {}).items():
            cand = snap_dir / f"{str(dig)[:12]}_{Path(key).name}"
            if not cand.is_file():
                snap_bad.append(f"{Path(key).name}: 스냅샷 없음")
            elif file_digest(cand) != dig:
                snap_bad.append(f"{Path(key).name}: 스냅샷 내용이 봉인과 다름")
    checks["입력_스냅샷"] = (not snap_bad, "; ".join(snap_bad[:3]))

    # ★ 11차 발견 3 — producer 검증을 fit artifact 에서도 **독립적으로 재수행**
    #   한다. 예전에는 fitting 이 시작 전에 한 번 보고 abort 여부에만 썼기에,
    #   복원본을 검증하는 쪽은 곡선 모집단(실패 라벨 포함)을 전혀 확인하지
    #   않았다. 스냅샷은 봉인된 바이트이고 restore 가 재생성하므로, 그 사본으로
    #   같은 검증을 돌린다.
    if not snap_bad and snap_dir.is_dir():
        _need = ("curves.parquet", "curves_manifest.yaml",
                 "curves_manifest_start.yaml", "failed.csv")
        _pv = {Path(k).name: snap_dir / f"{str(v)[:12]}_{Path(k).name}"
               for k, v in (sealed_start or {}).items()
               if Path(k).name in _need}
        if "curves.parquet" in _pv and "curves_manifest.yaml" in _pv:
            import shutil as _sh
            import tempfile as _tf
            with _tf.TemporaryDirectory() as _td:
                for _name, _src in _pv.items():
                    _sh.copy2(_src, Path(_td) / _name)
                _pcv = validate_curves_provenance(_td)
            checks["곡선_producer_재검"] = (
                _pcv["ok"],
                f"봉인된 곡선 producer 가 검증에 실패한다: {_pcv['fail'][:4]} — "
                f"이 fit 의 조건 모집단을 신뢰할 수 없다 (11차 발견 3)")
        else:
            checks["곡선_producer_재검"] = (
                False, "봉인 입력에 curves/producer 기록이 없다 (F70 이전 산출물)")

    # ── 코드 identity: 서명에 들어 있고 dirty가 아니어야 한다 (F49) ──
    checks["코드_identity"] = (
        bool(spec0.get("source_digest")) and spec0.get("git_dirty") is False,
        "run_spec에 source_digest가 없거나 dirty 실행이다")

    # ── 시작/종료 provenance 대조 (F42/F51) ──
    sp = man.get("start_provenance") or {}
    checks["시작_provenance"] = (bool(sp.get("attempt_id")),
                                 "start_provenance가 없다 (F51 이전 실행)")
    # ★ F57 — nested 사본만 보면, archive 과정에서 독립 start/attempt 파일을
    #   빠뜨린 artifact 도 통과한다. 파일을 **실제로 읽어** 대조한다.
    msp = run_dir / "manifest_start.yaml"
    att = run_dir / "attempts" / f"manifest_start_{sp.get('attempt_id')}.yaml"
    if not msp.exists():
        checks["start_파일_존재"] = (False, "manifest_start.yaml 파일이 없다")
    else:
        disk = yaml.safe_load(msp.read_text(encoding="utf-8")) or {}
        checks["start_파일_존재"] = (True, "")
        checks["attempt_파일_존재"] = (
            att.exists(), f"attempts/manifest_start_{sp.get('attempt_id')}.yaml 없다")
        # ★ F72 — 세 필드만 보면, 나머지가 어긋난 축약본이 통과한다. **전체 문서**를
        #   비교한다 (리뷰: 축약된 start/attempt 파일로 통과가 재현됐다).
        if att.exists():
            a = yaml.safe_load(att.read_text(encoding="utf-8")) or {}
            adiff = sorted(k for k in set(a) | set(sp) if a.get(k) != sp.get(k))
            checks["attempt_파일_일치"] = (
                not adiff, f"attempt 파일과 start_provenance가 다르다: {adiff[:4]}")
        # 대표 start 파일은 **최초 시도**의 기록이라 attempt_id 등이 다를 수 있다.
        # 그러나 코드·입력·환경은 같아야 한다 (다르면 다른 코드로 이어붙인 것이다).
        sdiff = sorted(k for k in ("source_digest", "git_commit", "git_dirty",
                                   "env", "input_sha256", "halfcell_recipe")
                       if disk.get(k) != sp.get(k))
        checks["start_파일_일치"] = (
            not sdiff,
            f"manifest_start.yaml과 start_provenance의 {sdiff}가 다르다")
    # ★ F50b — 판정 기준은 **실제로 돌아간 코드가 바뀌었는가**(source_digest)다.
    #   `git_commit` 은 문서만 커밋해도 바뀌므로 그것까지 실패로 보면 무해한
    #   변경에 발목이 잡힌다 (실측: 실행 중 회답 문서를 커밋했더니 걸렸다).
    #   git commit 변경은 아래 별도 항목에 정보로만 남긴다.
    checks["실행중_코드불변"] = (
        man.get("source_digest_changed_during_run") is False,
        "실행 도중 src/tools/configs 내용이 바뀌었다")
    if man.get("git_commit_changed_during_run"):
        # 코드가 그대로면 실패는 아니지만, 읽는 쪽이 알아야 한다
        checks["_참고_git이동"] = (
            True, "실행 중 git commit이 바뀌었으나 source_digest는 그대로다")
    checks["시작종료_서명일치"] = (
        not sp or sp.get("source_digest") == spec0.get("source_digest"),
        "시작 시점 source_digest가 run_spec과 다르다")

    # ★ F72 — validator 가 `source_digest()` 를 **한 번도 다시 계산하지 않았다.**
    #   기록된 문자열끼리만 맞춰봤으므로, 그 문자열이 실제 코드와 무관해도 통과했다.
    #   같은 저장소·같은 commit·clean 상태일 때는 재계산해서 대조할 수 있다.
    _now = git_info(root)
    if (_now.get("git_commit") == spec0.get("git_commit")
            and _now.get("git_dirty") is False):
        checks["코드_재계산"] = (
            source_digest(root) == spec0.get("source_digest"),
            f"같은 commit·clean 인데 source_digest가 다르다 "
            f"(현재 {source_digest(root)}, 기록 {spec0.get('source_digest')})")
    else:
        # 다른 commit 에서 검증 중이면 재계산이 불가능하다 — 사실만 남긴다
        checks["_참고_코드재계산불가"] = (
            True, f"검증 시점 commit({str(_now.get('git_commit'))[:8]})이 "
                  f"기록({str(spec0.get('git_commit'))[:8]})과 달라 재계산을 건너뛴다")

    # ── 입력 digest: 값이 있는지가 아니라 **파일을 다시 해시해** 맞는지 ──
    if not digs:
        checks["입력_digest"] = (False, "input_sha256이 없다")
    else:
        bad = []
        for path_s, dig in digs.items():
            if not dig:
                bad.append(f"{path_s}: digest 없음")
                continue
            # ★ 15차-3 — 봉인 키는 F65 로 **저장소 root 상대**임이 보장된다.
            #   예전에는 CWD 상대 경로를 먼저 보고 없을 때만 root 로 갔는데,
            #   격리 복원 검증은 cwd = 원본 저장소에서 돌기 때문에 복원본이
            #   아니라 **원본 파일**이 대조됐다 (실측: 격리 root 의 half-cell
            #   meta 를 위조해도 ok=True). root 로만 푼다 — 없으면 fail-closed.
            cand = Path(path_s)
            if not cand.is_absolute():
                cand = root / path_s
            if not cand.exists():
                bad.append(f"{path_s}: 파일 없음")
            elif file_digest(cand) != dig:
                bad.append(f"{path_s}: 내용이 바뀜")
        checks["입력_digest_재해시"] = (not bad, "; ".join(bad[:4]))

    # ── run_spec 을 다시 해시해 run_signature 와 대조 ──
    spec, sig_man = spec0, man.get("run_signature")
    checks["run_signature_기록"] = (bool(sig_man), "manifest에 run_signature가 없다")
    if not spec:
        checks["run_spec_기록"] = (False, "manifest에 run_spec이 없다")
    else:
        recomputed = hashlib.sha1(
            json.dumps(spec, sort_keys=True, default=str).encode()).hexdigest()[:12]
        checks["run_signature_재계산"] = (
            recomputed == str(sig_man),
            f"run_spec을 다시 해시하면 {recomputed}인데 기록은 {sig_man}이다")

    # ★ F59 — 검증 대상과 채점 대상이 달라선 안 된다. compare 가 임의 parquet 을
    #   채점하면서 검증은 run_dir/fits.parquet 에 했더니, 파일 인자 하나로
    #   degeneracy 를 94.4% → 0% 로 바꾸고도 통과했다.
    fp = Path(fits_path) if fits_path else run_dir / "fits.parquet"
    checks["채점파일_정본"] = (
        fp.resolve() == (run_dir / "fits.parquet").resolve(),
        f"채점 대상이 정본이 아니다: {fp}")
    if not fp.exists():
        checks["fits_존재"] = (False, "fits.parquet이 없다")
    else:
        # ── ★ F68 — 출력 봉인 재계산 ──
        #   지금까지 validator 가 fits 에서 읽은 열은 `run_sig` 와 `restarts_json`
        #   둘뿐이었다. 그래서 `lam_pe_hat = 0.999` 로 바꾸거나 열 전체에 `+0.5`
        #   를 하거나 조건 행을 지워도 전부 `ok=True` 였다. 파일을 다시 해시하고
        #   키 집합·행 수·완전성을 **기록이 아니라 실물에서** 다시 계산한다.
        rec = man.get("fits_seal") or {}
        if not rec:
            checks["출력봉인_기록"] = (False, "manifest에 fits_seal이 없다 (F68 이전 산출물)")
        else:
            try:
                now = fits_seal(fp, cond_ids=None, objective_order=None)
            except Exception as e:  # noqa: BLE001
                now = {}
                checks["출력봉인_재계산"] = (False, f"fits를 읽지 못했다: {e}")
            if now:
                bad = [k for k in ("file_sha256", "n_rows", "key_sha256",
                                   "cond_sha256", "n_conditions", "n_objectives")
                       if rec.get(k) != now.get(k)]
                checks["출력봉인_재계산"] = (
                    not bad,
                    "; ".join(f"{k}: 기록 {rec.get(k)} vs 실제 {now.get(k)}"
                              for k in bad[:3]))
                # 조건 집합이 **서명된 것과 같은가** — 행을 지우면 여기서 걸린다
                checks["조건집합_서명일치"] = (
                    now.get("cond_sha256") == spec0.get("condition_ids_sha256"),
                    f"fits의 조건 집합 {now.get('cond_sha256')}가 "
                    f"run_spec.condition_ids_sha256 {spec0.get('condition_ids_sha256')}와 다르다")
                # (조건 × 목적함수) 격자가 빠짐없이 채워졌는가
                _order = spec0.get("objective_order") or []
                exp = int(spec0.get("n_conditions") or 0) * len(_order)
                checks["출력_완전성"] = (
                    bool(exp) and now.get("n_rows") == exp
                    and sorted(now.get("objectives") or []) == sorted(_order),
                    f"행이 {now.get('n_rows')}개다 "
                    f"(조건 {spec0.get('n_conditions')} × 목적함수 {len(_order)} = {exp} 필요)")
                # ★ F76/8차 발견 5 — 집합·행수·digest 로는 **정확한 곱집합**이
                #   보장되지 않는다. 반례: ('c0','b') 행을 ('c1','b') 중복으로
                #   바꾸고 fits_seal 을 재계산해 넣으면, 조건 집합 {c0,c1} 도
                #   행 수도 그대로라 전부 통과했다. 관측된 조건 × 서명된
                #   목적함수의 각 조합이 **정확히 한 번씩** 있는지 센다.
                _kdf = pd.read_parquet(fp, columns=["cond_id", "objective"])
                _seen = Counter(zip(_kdf["cond_id"].astype(str),
                                    _kdf["objective"].astype(str)))
                _conds_obs = sorted({c for c, _ in _seen})
                _want = {(c, o) for c in _conds_obs for o in _order}
                _dup = sorted(k for k, n in _seen.items() if n > 1)
                _miss = sorted(_want - set(_seen))
                _extra = sorted(set(_seen) - _want)
                checks["출력_격자완전성"] = (
                    not (_dup or _miss or _extra),
                    f"중복 {len(_dup)} (예 {_dup[:2]}), 누락 {len(_miss)} "
                    f"(예 {_miss[:2]}), 잉여 {len(_extra)} (예 {_extra[:2]})")
        cols = list(pd.read_parquet(fp).columns)
        want = [c for c in ("run_sig", "restarts_json") if c in cols]
        need = pd.read_parquet(fp, columns=want) if want else pd.DataFrame()
        has_sig = "run_sig" in need.columns
        checks["행별_서명"] = (has_sig and not need["run_sig"].isna().any()
                               if has_sig else False,
                               "run_sig 열이 없거나 비어 있는 행이 있다")
        uniq = sorted(need["run_sig"].dropna().unique()) if has_sig else []
        checks["단일_서명"] = (len(uniq) == 1, f"서명이 {len(uniq)}종이다")
        checks["manifest와_일치"] = (
            bool(uniq) and str(uniq[0]) == str(sig_man),
            "fits의 서명과 manifest의 run_signature가 다르다")
        # ── restart 출처: 첫 행이 아니라 **모든 행** ──
        if "restarts_json" not in need.columns:
            checks["restart_출처"] = (False, "restarts_json 열이 없다")
        else:
            # ★ F50 — `.dropna()` 를 쓰면 **전부 null 이어도 통과**한다. 그리고
            #   `rs[0]` 만 보면 두 번째 원소부터 source 가 없어도 통과한다.
            #   모든 행 · 모든 원소를 본다.
            n_bad, n_null = 0, 0
            for v in need["restarts_json"]:
                if v is None or (isinstance(v, float) and pd.isna(v)):
                    n_null += 1
                    continue
                try:
                    rs = json.loads(v)
                except (ValueError, TypeError):
                    n_bad += 1
                    continue
                # ★ F61 — 키 존재만 보면 값이 전부 null 이어도 통과한다.
                if not rs or not all(_restart_ok(e) for e in rs):
                    n_bad += 1
            checks["restart_출처"] = (
                n_bad == 0 and n_null == 0,
                f"{n_bad}행이 형식 위반, {n_null}행이 비어 있다 "
                f"(모든 원소가 p·J·i·source 를 가져야 한다)")
            # ★ F86/9차 발견 7 — `adaptive=False` 는 "조기 종료 안 함"일 뿐,
            #   개별 restart 가 예외로 실패하면 조용히 건너뛴다 (fitting.py 의
            #   `except` → 다음 restart). 그러면 실제 index 가 [0,2,4] 처럼 줄어
            #   **두 목적함수의 탐색 예산이 달라지고**, "fixed5" 라는 이름이
            #   거짓이 된다. paired 진단의 전제가 여기서 무너진다.
            _opt = spec0.get("optimizer") or {}
            if _opt.get("adaptive") is False:
                _n = int(_opt.get("n_restarts") or 0)
                _want_idx = set(range(_n))
                _short = 0
                for v in need["restarts_json"]:
                    try:
                        rs = json.loads(v)
                    except (ValueError, TypeError):
                        _short += 1
                        continue
                    if {e.get("i") for e in rs} != _want_idx:
                        _short += 1
                checks["restart_예산_완주"] = (
                    _short == 0 and _n > 0,
                    f"{_short}행의 restart index 집합이 {sorted(_want_idx)}와 다르다 "
                    f"— adaptive=False 인데 예산을 못 채웠다 (실패한 restart가 있다)")

    fail = [k for k, (ok, _) in checks.items() if not ok]
    # 통과한 검사에 실패 사유를 같이 실으면 전부 실패한 것처럼 읽힌다.
    return {"ok": not fail,
            "checks": {k: "통과" if ok else f"실패 — {why}"
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
