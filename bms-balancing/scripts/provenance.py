#!/usr/bin/env python3
"""산출물 옆에 붙는 `.meta.json` 의 git 부분 — **한 곳**에서.

## 왜 따로 있나

`run_states.sh` 와 `ne_shape.py` 가 각자 `git status --porcelain` 으로
`git_dirty` 를 계산했다. 그 명령은 **untracked 파일도 센다.** 산출물은 쓰이는
순간 untracked 이고 `cells/` 도 오래 untracked 였으므로, 이 저장소의 meta 는
2026-09-11 확인 시점에 **전부** `git_dirty: true` 였다 — 플래그에 정보가 없었다.
그 위에 §1-12 조건 6 이 "커밋 안 된 변경이 있는 트리에서 돌았다" 고 적었다.
과장이었다.

플래그가 답해야 할 물음은 "**돌린 코드가 `git_commit` 과 같았나**" 다. 그건
추적 파일의 수정 여부이고, untracked 산출물과 무관하다. 그래서
`--untracked-files=no`.

    from provenance import git_state
    sha, dirty = git_state()          # dirty: 추적 파일이 수정됐는가
    sha, dirty = git_state(exclude=[art, art + ".meta.json"])   # 산출물 자신은 뺀다

## 산출물 자신은 뺀다 (2026-09-11, fb62342)

추적된 산출물(`out/*.csv`, `out/*.json`)을 **다시 쓰는 것 자체**가 "추적 파일 수정" 으로
잡혀서, 재생성 meta 는 늘 `git_dirty: true` 였다 — fb62342 의 커밋에는 CSV 와 meta 만
있었는데도. 플래그의 물음은 코드에 대한 것이므로 지금 쓰는 산출물(과 그 meta)은
`exclude` 로 뺀다. 코드 파일이 고쳐져 있으면 여전히 true 다.
"""
from __future__ import annotations
import subprocess


# ── 코드 dirty 와 수정된 산출물을 **분리**한다 (Codex R4-07) ────────────────────────────────
# 산출물 하나만 빼면, 앞 단계에서 다시 쓴 **다른** 산출물이 코드 변경으로 읽혀 두 번째 meta 가
# 다시 dirty 였다. 그렇다고 `out/` 을 통째로 숨기면 계산 **입력**으로 쓰는 artifact(`matrix_*.csv`
# 등)의 변경까지 숨는다. 그래서 둘을 따로 적는다:
#   git_dirty            — 산출 디렉터리 밖의 추적 파일이 수정됐는가 (= 코드가 commit 과 같았나)
#   git_modified_outputs — 산출 디렉터리 안에서 수정된 추적 파일 목록 (지금 쓰는 산출물·meta 제외)


def _git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout


def env_signature() -> dict:
    """계산에 쓰인 인터프리터·라이브러리·플랫폼 (R6 내부 F3: scipy 1.11↔1.17 에서 savgol 이 ULP 로 갈리고 L-BFGS-B
    최적점이 달라지는데 산출 어디에도 버전이 없었다). meta·degeneracy JSON·eval 헤더에 같은 dict 를 적는다."""
    import platform
    def ver(name):
        try:
            return __import__(name).__version__
        except Exception:                                # noqa: BLE001
            return None
    return {"python": platform.python_version(), "numpy": ver("numpy"), "scipy": ver("scipy"),
            "pandas": ver("pandas"), "platform": platform.platform()}


def git_provenance(cwd: str | None = None, artifact=None, output_roots=("out",)) -> dict:
    """{git_commit, git_dirty(코드), git_modified_outputs[...], git_modified_code[...]}. git 이 없으면 None 들.
    `cwd` 를 안 주면 **이 스크립트가 속한 `bms-balancing/`** 이 기준이다 (R6 내부 F7: 호출자의 cwd 에 따라 같은
    산출이 False/True/None 으로 갈렸다)."""
    import pathlib
    base = pathlib.Path(cwd).resolve() if cwd else pathlib.Path(__file__).resolve().parents[1]
    try:
        sha = _git(str(base), "rev-parse", "HEAD").strip()
        top = pathlib.Path(_git(str(base), "rev-parse", "--show-toplevel").strip()).resolve()
        # ⚠ Codex R5-11: 기본 `--porcelain` 은 비ASCII 경로를 따옴표·8진수로 찍는다 ("out/\354\270\241…").
        #   `-z` 레코드는 경로를 그대로 준다; rename/copy 는 새 경로 뒤에 원 경로가 한 레코드 더 온다.
        # ⚠ Codex R11 P1-9: `--untracked-files=no` 는 **실행되는 코드**도 숨겼다 — 저장소 루트의 untracked
        #   `sitecustomize.py` 가 실제로 import 돼 marker 를 쓰는데 provenance 는 `git_dirty: false` 를 적었다.
        #   untracked 도 본다; 산출 root 안이면 산출로, 밖이면 **코드**로 센다 (아래 분류).
        raw = _git(top, "status", "--porcelain", "-z", "--untracked-files=normal")
    except Exception:
        return {"git_commit": "", "git_dirty": None, "git_modified_outputs": None, "git_modified_code": None}
    lines, parts, i = [], raw.split("\0"), 0
    while i < len(parts):
        rec = parts[i]; i += 1
        if not rec:
            continue
        xy, path_ = rec[:2], rec[3:]
        if "R" in xy or "C" in xy:
            i += 1                                 # 원 경로 레코드는 건너뛴다 (새 경로가 수정된 파일)
        lines.append(f"{xy} {path_}")
    skip = set()
    if artifact:
        a = pathlib.Path(artifact)
        a = (a if a.is_absolute() else base / a).resolve()
        skip = {a, a.with_name(a.name + ".meta.json")}
    roots = [(pathlib.Path(r) if pathlib.Path(r).is_absolute() else base / r).resolve()
             for r in output_roots if r]                       # 빈 문자열(미설정 $OUT)은 루트가 아니다
    outputs, code = [], []
    for ln in lines:
        # ⚠ Codex R6-05: `-z` 레코드의 경로는 이미 정확하다. 사람용 rename 표기(" -> ")로 다시 쪼개거나 앞뒤 공백을
        #   깎으면 정상 파일명 `out/a -> b.csv` 가 `b.csv`(코드) 로 분류된다. 그대로 쓴다.
        rel = ln[3:]
        path = (top / rel).resolve()
        if path in skip:
            continue
        inside = any(root == path or root in path.parents for root in roots)
        if ln[:2] == "??":
            # ⚠ Codex R11 P1-9: untracked 는 **산출 root 안이면 무시, 밖이면 코드**다. 산출은 쓰이는 순간
            #   untracked 라 안쪽까지 세면 플래그가 늘 켜져 정보가 사라진다 (그래서 전 판이 `-uno` 였다). 하지만
            #   바깥의 untracked 는 실행되는 코드일 수 있다 — `sitecustomize.py` 가 실제로 import 돼 돌았는데
            #   provenance 는 clean 이라고 적었다. 모르는 채로 clean 이라고 말하지 않는다.
            if not inside:
                code.append(rel)
            continue
        if inside:
            outputs.append(str(path.relative_to(base)) if base in path.parents else rel)
        else:
            code.append(rel)
    # ⚠ untracked 디렉터리는 git 이 `dir/` 하나로 접어서 준다 — 그 안에 importable 이 있으면 코드다. 여기서는
    #   접힌 항목도 그대로 코드로 센다 (모르는 채로 clean 이라고 말하지 않는다).
    return {"git_commit": sha, "git_dirty": bool(code),
            "git_modified_outputs": sorted(outputs), "git_modified_code": sorted(code)}


def sidecar_dict(name: str, data: bytes, *, run_id: str, started, argv, pv: dict, extra: dict | None = None) -> dict:
    """U14 sidecar 의 **공통** 축 — 산출 이름 · run_id · 지금 bytes 의 sha256 · 본문에서 유도한 roster · 끝 git 상태 ·
    시작 git 상태와 그 차이 · 시작/작성 시각 · env · argv. `run_states.sh write_meta`(heredoc) 가 matrix·profile·degeneracy
    에 적는 것과 같은 키다 (Codex R13 §Q6 뒤 shape 가 같은 계약을 갖게 됐고, `fit_cycles` 가 셋째 producer 라 한 자리로).

    `started` 는 `{"utc": iso, "git": git_provenance() 결과}` (계산 **전** — R6 내부 F04) 또는 None,
    `pv` 는 끝 상태의 `git_provenance(artifact=…)`. `extra` 는 종류별 필드 (실행 조건·pairing 등) — 공통 키를 덮지 않는다.
    roster 는 `bms_balancing.schema.body_roster` 로 **같은 bytes** 에서 유도한다; 패키지를 못 찾으면 None 과 이유를 적는다
    (지어내지 않는다 — 승격 gate 가 막는다). 등록되지 않은 이름은 ValueError 그대로 (fail-closed, Codex R13 §Q6).
    """
    import datetime, hashlib, pathlib as _pl, sys as _sys
    pre = (started or {}).get("git") or {}
    try:
        from bms_balancing.schema import body_roster
    except ModuleNotFoundError:
        _sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
        try:
            from bms_balancing.schema import body_roster
        except ModuleNotFoundError as e:                       # 합성 fixture 트리 — 명부를 지어내지 않는다
            body_roster, roster_err = None, f"bms_balancing 를 못 찾았다: {e}"
    meta = {
        "artifact": name, "run_id": run_id, "sha256": hashlib.sha256(data).hexdigest(),
        "roster": (body_roster(name, data) if body_roster else None),
        "git_commit": pv.get("git_commit"), "git_dirty": pv.get("git_dirty"),
        "git_modified_outputs": pv.get("git_modified_outputs"), "git_modified_code": pv.get("git_modified_code"),
        "git_commit_at_start": pre.get("git_commit"), "git_dirty_at_start": pre.get("git_dirty"),
        "git_modified_code_at_start": pre.get("git_modified_code"),
        "git_state_changed_during_run": bool(pre) and (
            pre.get("git_commit") != pv.get("git_commit") or pre.get("git_dirty") != pv.get("git_dirty")
            or pre.get("git_modified_code") != pv.get("git_modified_code")),
        "started_utc": (started or {}).get("utc"),
        "env": env_signature(),
        "argv": list(argv if argv is not None else _sys.argv),
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    if body_roster is None:
        meta["roster_error"] = roster_err
    for k, v in (extra or {}).items():
        meta.setdefault(k, v)
    return meta


def sha256_file(path) -> str:
    import hashlib, pathlib
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def check_run_id_bytes(name: str, data: bytes, rid: str):
    """`data`(이미 읽은 bytes)가 **필드로** 이 시도의 id 를 담고 있는가 (Codex R5-08). CSV → 모든 행의 `run_id` 열;
    JSON → 최상위 `run_id`. 경로가 아니라 bytes 를 받는 이유: 검증한 bytes 와 소비하는 bytes 가 같아야 한다 (Codex R6-01)."""
    import csv, io, json
    if not rid:
        return False, "run id 없음"
    try:
        txt = data.decode("utf-8-sig")
        if name.lower().endswith(".csv"):
            header = next(csv.reader(io.StringIO(txt)), [])
            n_col = header.count("run_id")
            if n_col != 1:                           # R6 내부 V6-08: DictReader 는 같은 이름의 마지막 열만 본다
                return False, ("run_id 열 없음" if n_col == 0 else f"run_id 열이 {n_col} 개")
            rows = list(csv.DictReader(io.StringIO(txt)))
            if not rows:
                return False, "행 없음"
            bad = [r.get("run_id") for r in rows if r.get("run_id") != rid]
            return (not bad), ("전 행 일치" if not bad else f"다른 run_id 행 {len(bad)}/{len(rows)}: {bad[:2]}")
        d = json.loads(txt)
        ok = isinstance(d, dict) and d.get("run_id") == rid
        return ok, ("일치" if ok else f"JSON run_id={d.get('run_id') if isinstance(d, dict) else None!r}")
    except Exception as e:                           # noqa: BLE001
        return False, f"읽기 실패: {e}"


def check_run_id(path, rid: str):
    """경로 판 — 파일을 한 번 읽어 `check_run_id_bytes` 로."""
    import pathlib
    p = pathlib.Path(path)
    if not p.is_file():
        return False, "파일 없음"
    try:
        return check_run_id_bytes(p.name, p.read_bytes(), rid)
    except OSError as e:
        return False, f"읽기 실패: {e}"


def is_modern_bytes(name: str, data: bytes):
    """이 산출이 **현행 schema**(run_id 를 담는다) 인가 — Codex R6-02: 현행 산출에 meta 가 없으면 옛 파일이 아니라
    게시가 중단된 것이다. CSV → 헤더에 `run_id`; JSON → 최상위 `run_id` 키. 해석 불가면 None."""
    import csv, io, json
    try:
        txt = data.decode("utf-8-sig")
        if name.lower().endswith(".csv"):
            return "run_id" in next(csv.reader(io.StringIO(txt)), [])
        d = json.loads(txt)
        return isinstance(d, dict) and "run_id" in d
    except Exception:                                # noqa: BLE001
        return None


def verify_unit_bytes(name: str, data: bytes, meta, rid: str | None = None):
    """**이미 읽은** 산출 bytes 와 meta dict 가 같은 시도의 한 묶음인가 (Codex R5-04 · R6-01). → (ok, 설명).

    - ok True : 이 bytes 와 이 meta 를 그대로 소비해도 된다.
    - ok None : 옛 산출(run_id 없음) — 호환 경로. 현행 산출은 여기로 오지 않는다 (Codex R6-02).
    - ok False: 소비 금지 (섞임 · 미완 · 줄끝).
    `rid` 를 주면 그 묶음이 **이 시도**의 것이어야 한다 (R6 내부 F05a)."""
    import hashlib
    modern = is_modern_bytes(name, data)
    if meta is None:
        if modern:
            return False, "현행 산출(run_id 있음)인데 meta 가 없다 — 게시가 중단됐거나 write_meta 를 안 거쳤다: 미완 (Codex R6-02)"
        return None, "meta 없음 (옛 산출, run_id 없음 — 호환 경로)"
    m_rid, digest = meta.get("run_id"), meta.get("sha256")
    if not m_rid or not digest:
        if modern:
            return False, "현행 산출(run_id 있음)인데 옛 meta(run_id/sha256 없음) — 미완 (Codex R6-02)"
        return None, "옛 meta (run_id/sha256 없음)"
    if meta.get("artifact") and meta["artifact"] != name:  # R6 내부 V6-05: 묶음이 맞는 이름 아래 있는가
        return False, f"meta 의 artifact({meta['artifact']!r}) 가 파일 이름({name!r}) 과 다르다"
    if rid and rid != m_rid:
        return False, f"meta 의 run_id({m_rid}) 가 이 시도({rid}) 의 것이 아니다 — 다른 시도가 뒤에 게시했다"
    ok_id, why = check_run_id_bytes(name, data, m_rid)
    if not ok_id:
        return False, f"meta 의 run_id 가 산출물과 다르다: {why}"
    if hashlib.sha256(data).hexdigest() != digest:
        # ⚠ U14-01: 줄끝만 바뀐 경우(git 정규화 · Windows 체크아웃)를 "다른 시도가 게시했다" 로 읽지 않게 짚는다.
        for nm, alt in (("CRLF→LF", data.replace(b"\r\n", b"\n")), ("LF→CRLF", data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))):
            if hashlib.sha256(alt).hexdigest() == digest:
                return False, (f"**줄끝**만 다르다 ({nm} 이면 sha256 이 맞는다) — 내용은 같고 게시 뒤 정규화된 "
                               f"것이다 (git `.gitattributes` · Windows 체크아웃). 산출은 LF 로 쓴다")
        return False, "meta 의 sha256 이 지금 bytes 와 다르다"
    return True, "일치"


def read_unit(path, rid: str | None = None):
    """산출 bytes 와 meta 를 **한 번씩** 읽어 서로 대조하고 그 snapshot 을 돌려준다 → (ok, 설명, data, meta).

    ⚠ Codex R6-01: 독자가 데이터를 읽은 뒤 경로를 다시 검사하면, 그 사이 끼어든 정상 게시 B 가 검사를 통과해
      A 데이터에 B meta 가 붙었다 (반대 순서로는 A 를 검증하고 B 행을 읽었다). 검증한 bytes 만 소비하려면 독자는
      **이 함수가 돌려준 data·meta 만** 써야 한다 — 어느 읽기 경계에 게시가 끼든 결과는 A/A · B/B · 미완뿐이다."""
    import json, pathlib
    p = pathlib.Path(path)
    try:
        data = p.read_bytes()
    except OSError as e:
        return False, f"읽기 실패: {e}", None, None
    mp = p.with_name(p.name + ".meta.json"); meta = None
    if mp.is_file():
        try:
            meta = json.loads(mp.read_text(encoding="utf-8"))
        except Exception as e:                       # noqa: BLE001
            return False, f"meta 읽기 실패: {e}", data, None
    ok, why = verify_unit_bytes(p.name, data, meta, rid)
    return ok, why, data, meta


def verify_unit(path, rid: str | None = None):
    """경로 판 — `read_unit` 의 판정만. 소비할 bytes 가 필요하면 `read_unit` 을 쓸 것 (Codex R6-01)."""
    ok, why, _, _ = read_unit(path, rid)
    return ok, why


def git_state(cwd: str | None = None, exclude=()) -> tuple[str, bool | None]:
    """(HEAD sha, **코드**가 수정됐는가). git 이 없으면 ("", None). `exclude[0]` 은 지금 쓰는 산출물."""
    pv = git_provenance(cwd, artifact=(list(exclude) or [None])[0])
    return pv["git_commit"], pv["git_dirty"]


if __name__ == "__main__":
    import json, sys
    if hasattr(sys.stdout, "reconfigure"):               # R6 내부 F9: ASCII 기본 stdout 에서 한글 메시지로 죽지 않게
        sys.stdout.reconfigure(errors="backslashreplace")
    if len(sys.argv) >= 4 and sys.argv[1] == "--check-run-id":     # run_states.sh 가 쓴다 (R5-08)
        ok, why = check_run_id(sys.argv[2], sys.argv[3]); print(why); sys.exit(0 if ok else 1)
    if len(sys.argv) >= 3 and sys.argv[1] == "--verify-unit":      # run_states.sh 가 쓴다 (R5-04 · R6 F05a: [run id])
        ok, why = verify_unit(sys.argv[2], sys.argv[3] if len(sys.argv) >= 4 else None); print(why); sys.exit(0 if ok else 1)
    # ⚠ U18-02 (2026-09-13 실측): 전 판은 output_roots 를 못 받아 **기본값 ("out",)** 으로 답했다. `run_states.sh`
    #   의 시작 provenance 가 이 CLI 이므로, `OUT=out_u18` 실행에서는 그 untracked 디렉터리가 "코드 변경" 으로
    #   잡혀 13 산출 중 11 개가 `git_state_changed_during_run: true` 였다 (끝 상태는 `write_meta` 가
    #   `output_roots=(out_dir, "out")` 로 물어 false). 플래그가 늘 켜지면 신호가 죽는다 — 이 파일 머리말의 그 고장이다.
    #   둘째 인자부터가 산출 root 다 (없으면 `out` 만; write_meta 와 같이 `out` 은 늘 포함한다).
    print(json.dumps(git_provenance(artifact=sys.argv[1] if len(sys.argv) > 1 else None,
                                    output_roots=(*sys.argv[2:], "out"))))
