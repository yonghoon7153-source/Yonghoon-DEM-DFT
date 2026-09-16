"""증거 러너의 **공용 gate** — 무엇을 실행했는지 봉인하는 부분만 (Codex R10 P2-4 · P2-5).

R7·R9 닫힘 재생기가 같은 계약을 쓴다. 두 벌로 두면 한쪽만 고쳐지므로 여기 한 자리에 둔다.

닫는 것:

- **assert 로 증거를 판정하지 않는다.** `python -O` 는 `assert` 를 통째로 지운다 — 전 판은 delegated pytest 가 usage
  error 인데 runner rc 0 · `closed: true` 를 냈다. 판정은 `EvidenceError` 를 던지는 명시적 분기이고, optimize 모드
  자체를 fail-closed 한다 (`require_assertions`).
- **`git status` 의 rc 를 본다.** `GIT_INDEX_FILE` 이 디렉터리면 status 는 rc 128 인데 전 판은 stdout 이 비었다는
  이유로 `dirty: false` 였다.
- **실행 bytes 를 expected commit 에서 새로 materialize 한다.** working tree 를 그대로 쓰면 `assume-unchanged` 로
  고친 tracked module 도, ignored `__pycache__` 의 위조 bytecode 도 clean 으로 보이면서 실행됐다. sparse detached
  worktree 는 그 commit 의 blob 만 풀고 자기 index 를 쓰므로 둘 다 닿지 않는다.
"""
from __future__ import annotations
import hashlib, json, os, pathlib, subprocess, sys, tempfile


class EvidenceError(RuntimeError):
    """증거를 만들 수 없는 상태 — 러너는 이것을 잡아 비영 종료한다 (성공으로 넘기지 않는다)."""


def require_assertions() -> None:
    if not __debug__:
        raise EvidenceError(
            "이 러너는 `python -O`(PYTHONOPTIMIZE) 에서 증거를 만들지 않는다 — 보관한 probe 의 반례는 `assert` 로 "
            "쓰여 있고 optimize 모드는 그것을 통째로 지운다. 최적화 없이 다시 부를 것 (Codex R10 P2-4)")


def need(cond, what: str, detail=None) -> None:
    """증거 판정의 **명시적 분기** — `assert` 를 쓰면 `python -O` 에서 통째로 사라진다 (Codex R10 P2-4)."""
    if not cond:
        raise EvidenceError(f"{what}" + (f" — {detail!r}" if detail is not None else ""))


def _git(target, *args, check=True) -> str:
    p = subprocess.run(["git", "-C", str(target), *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise EvidenceError(f"`git {' '.join(args)}` 이 rc {p.returncode} 로 끝났다 — 저장소 상태를 모르는 채로 "
                            f"증거를 만들지 않는다 (Codex R10 P2-5): {p.stderr.strip()[:300]}")
    return p.stdout


def git_head(target) -> str:
    return _git(target, "rev-parse", "HEAD").strip()


def dirty_paths(target) -> list:
    """working tree 의 변경 목록. **rc 를 본다** — 모르는 상태는 clean 이 아니다 (Codex R10 P2-5 반례 A)."""
    out = _git(target, "status", "--porcelain", "--untracked-files=normal", "--", ".")
    return [ln for ln in out.splitlines() if ln.strip()]


def package_digest(pkg: pathlib.Path, sums: pathlib.Path):
    """보관한 패키지 bytes 가 SHA256SUMS 와 같은가 → (전부 ok, {파일: ok|mismatch|missing})."""
    status = {}
    for ln in sums.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        want, name = ln.split(None, 1)
        f = pkg / name.strip()
        status[name.strip()] = ("missing" if not f.is_file()
                                else ("ok" if hashlib.sha256(f.read_bytes()).hexdigest() == want else "mismatch"))
    return bool(status) and all(v == "ok" for v in status.values()), status


def parse_probes(text: str, known):
    """`--probes` → (목록, 문제). 빈 이름·모르는 이름·중복은 전부 거부한다 (Codex R9 P2-1)."""
    want = [p.strip() for p in str(text).split(",")]
    problems = []
    if not str(text).strip() or any(not p for p in want):
        problems.append("빈 probe 이름")
    unknown = [p for p in want if p and p not in known]
    if unknown:
        problems.append(f"모르는 probe {unknown} (아는 것: {list(known)})")
    dup = sorted({p for p in want if p and want.count(p) > 1})
    if dup:
        problems.append(f"중복 probe {dup}")
    return want, problems


def materialize(target, head: str, keep=None):
    """expected commit 의 **격리 snapshot** 을 만든다 → (실행할 target 경로, cleanup 함수).

    sparse detached worktree 라 (i) 그 commit 의 blob 만 풀리고 (ii) 자기 index 를 쓰므로 원본의
    `assume-unchanged`/`skip-worktree` 가 따라오지 않으며 (iii) ignored `__pycache__` 같은 untracked bytes 가
    애초에 없다. `git rev-parse HEAD` 도 expected commit 그대로라 중첩 러너의 계약이 살아 있다.
    """
    target = pathlib.Path(target).resolve()
    prefix = _git(target, "rev-parse", "--show-prefix").strip().strip("/")
    _git(target, "worktree", "prune", check=False)
    dest = pathlib.Path(keep) if keep else pathlib.Path(tempfile.mkdtemp(prefix="evidence-snap-")) / "snap"
    if dest.exists():
        raise EvidenceError(f"snapshot 자리가 이미 있다: {dest}")
    _git(target, "worktree", "add", "--detach", "--no-checkout", str(dest), head)

    def cleanup():
        _git(target, "worktree", "remove", "--force", str(dest), check=False)
        _git(target, "worktree", "prune", check=False)

    try:
        if prefix:
            # `.gitignore` 도 같이 — probe 가 **저장소 루트의 ignore 정책**을 보고 clone 을 만든다 (ignored-pyc case).
            # 없으면 sparse 가 조용히 넘어간다.
            _git(dest, "sparse-checkout", "set", "--no-cone", prefix, "/.gitignore")
        _git(dest, "checkout")
        got = git_head(dest)
        if got != head:
            raise EvidenceError(f"snapshot 의 HEAD 가 다르다: {got} ≠ {head}")
        inner = dest / prefix if prefix else dest
        if not inner.is_dir():
            raise EvidenceError(f"snapshot 에 {prefix} 가 없다")
    except BaseException:
        cleanup()
        raise
    return inner, cleanup


def isolate_bytecode(env: dict | None = None) -> str:
    """이미 놓인 `__pycache__` 를 **읽지 않게** 한다 — 캐시 위치를 임시 prefix 로 돌린다 (Codex R10 P2-5 반례 C).

    트리를 건드리지 않는다 (지우지 않는다). in-process import 와 자식 프로세스 둘 다에 건다.
    """
    prefix = tempfile.mkdtemp(prefix="evidence-pycache-")
    sys.pycache_prefix = prefix
    os.environ["PYTHONPYCACHEPREFIX"] = prefix
    if env is not None:
        env["PYTHONPYCACHEPREFIX"] = prefix
    return prefix


def instrument_sealed(target, rel_paths) -> tuple:
    """**도구 자신**(러너·gate)의 bytes 가 expected commit 의 blob 과 같은가 → (bool, {경로: ok|다름|없음}).

    대상 트리를 격리 snapshot 에서 읽어도 러너가 수정된 채라면 그 증거는 그 커밋의 것이 아니다. index 를 거치지 않는
    `hash-object` ↔ `rev-parse HEAD:<path>` 로 댄다 (Codex R10 P2-5 의 identity 요구를 도구에도 적용).
    """
    detail = {}
    for rel in rel_paths:
        f = pathlib.Path(target) / rel
        if not f.is_file():
            detail[rel] = "없음"; continue
        try:
            # ⚠ 자체 리뷰 C07: `--no-filters` 없이 해싱하면 committed `.gitattributes` + `clean` 드라이버 하나로
            #   **주입 코드가 든 러너**가 ok 로 봉인된다 (아래 `verify_snapshot_bytes` 는 이미 쓰고 있었다 —
            #   한쪽만 닫은 비대칭이었다). index·filter 를 안 거치는 bytes 를 댄다.
            have = _git(target, "hash-object", "--no-filters", "--", str(f)).strip()
            want = _git(target, "rev-parse", f"HEAD:./{rel}").strip()
        except EvidenceError:
            detail[rel] = "커밋에 없음"; continue
        detail[rel] = "ok" if have == want else "다름"
    return all(v == "ok" for v in detail.values()), detail


def instrument_digests(target, rel_paths) -> dict:
    """도구 파일의 **실제 bytes digest** — `{경로: sha}`. receipt 가 실어야 하는 것은 이것이다.

    ⚠ R16 실측: 처음에 `instrument_sealed` 의 **상태 문자열**(`ok`/`다름`)을 receipt 에 실었다. 소비자는
      그것을 blob sha 와 대 보므로 **언제나 "다름"** 이었다 — 깨끗한 트리에서 끝까지 돌려 보고서야
      드러났다. 상태는 사람용 요약이고 receipt 는 **값**을 실어야 한다.

    index·filter 를 안 거치는 `hash-object --no-filters` 다 (자체 리뷰 C07 과 같은 이유).
    """
    out = {}
    for rel in rel_paths:
        f = pathlib.Path(target) / rel
        if not f.is_file():
            continue
        try:
            out[rel] = _git(target, "hash-object", "--no-filters", "--", str(f)).strip()
        except EvidenceError:
            continue
    return out


def index_skip_flags(target) -> list:
    """`assume-unchanged`·`skip-worktree` 가 걸린 tracked 파일 — 봉인 전에 배제한다.

    ⚠ Codex R11 P2-5: 전 판은 **소문자만** 봤다. git 은 skip-worktree 를 대문자 `S` 로 찍고 (소문자가 되는 것은
    assume-unchanged 가 같이 걸렸을 때뿐이다) — `S reviews/evidence_gate.py` 가 통째로 새어나가 러너가
    rc 0 · eligible true 를 냈다. 두 태그를 다 본다.
    """
    out = _git(target, "ls-files", "-v", "--", ".")
    return [ln[2:] for ln in out.splitlines() if ln[:1].islower() or ln[:1] == "S"]


def verify_snapshot_bytes(snap, head: str) -> list:
    """materialize 한 트리의 tracked **bytes** 가 expected commit 의 blob 과 같은가 → 다른 것들의 목록.

    ⚠ Codex R11 P1-10 반례 B: checkout 은 filter(smudge)·eol·ident 를 거친다. committed `.gitattributes` 에
    smudge driver 하나만 걸어도 snapshot 의 `verify.py` 가 다른 bytes 로 풀리는데 `git rev-parse HEAD` 는 그대로다 —
    "그 커밋을 돌렸다" 가 거짓이 된다. index·filter 를 안 거치는 `hash-object --no-filters` 로 파일 bytes 를 직접
    해싱해 `<head>` 트리의 object id 와 댄다. 파일 수가 많으므로 batch 로 한 번씩만 부른다.
    """
    snap = pathlib.Path(snap).resolve()
    want = {}
    for ln in _git(snap, "ls-tree", "-r", "-z", head, "--", ".").split("\0"):
        if not ln.strip():
            continue
        info, _, name = ln.partition("\t")
        mode, kind, oid = info.split()
        if kind == "blob":
            want[name] = (mode, oid)
    names = [n for n in _git(snap, "ls-files", "-z", "--", ".").split("\0") if n]
    problems = []
    if set(names) - set(want):
        problems += [f"{n}: expected commit 에 없는 tracked 파일" for n in sorted(set(names) - set(want))]
    if set(want) - set(names):
        problems += [f"{n}: snapshot 에 안 풀렸다" for n in sorted(set(want) - set(names))]
    todo = [n for n in names if n in want and want[n][0] != "120000"]      # symlink 는 bytes 비교 대상이 아니다
    missing = [n for n in todo if not (snap / n).is_file()]
    problems += [f"{n}: snapshot 에 파일이 없다" for n in missing]
    todo = [n for n in todo if n not in set(missing)]
    if todo:
        # ⚠ `--stdin-paths` 는 cwd 가 아니라 worktree 최상위 기준으로 연다 — **절대 경로**로 넘긴다
        p = subprocess.run(["git", "-C", str(snap), "hash-object", "--no-filters", "--stdin-paths"],
                           input="\n".join(str(snap / n) for n in todo) + "\n",
                           capture_output=True, text=True)
        if p.returncode != 0:
            raise EvidenceError(f"snapshot bytes 해싱이 rc {p.returncode}: {p.stderr.strip()[:300]}")
        have = p.stdout.split()
        if len(have) != len(todo):
            raise EvidenceError(f"해시 개수가 안 맞는다: {len(have)} ≠ {len(todo)}")
        for n, h in zip(todo, have):
            if h != want[n][1]:
                problems.append(f"{n}: bytes 가 blob 과 다르다 ({h[:12]} ≠ {want[n][1][:12]})")
    return problems


def full_head(target, expected: str) -> str:
    """`--expected-head` 를 **full canonical object id** 로 확정한다 (Codex R11 P2-6).

    전 판은 `git rev-parse <arg>` 결과끼리만 대조해서 7 자 prefix 도 통과했고, 그 짧은 값이 그대로 증거에
    expected head 로 적혔다. prefix 는 커밋 하나를 지목하지 못한다 (ambiguous 가 되면 나중에 다른 커밋을 가리킨다).
    """
    e = (expected or "").strip()
    if len(e) != 40 or any(c not in "0123456789abcdef" for c in e.lower()):
        raise EvidenceError(f"--expected-head 는 40 자리 full object id 여야 한다 (짧은 prefix·ref 이름 불가): {e!r}")
    p = subprocess.run(["git", "-C", str(target), "rev-parse", "--verify", f"{e.lower()}^{{commit}}"],
                       capture_output=True, text=True)
    got = p.stdout.strip()
    if p.returncode != 0 or got != e.lower():
        raise EvidenceError(f"HEAD mismatch — --expected-head 가 이 저장소의 commit 이 아니다: {e!r}")
    return got


def tree_of(target, head: str) -> str:
    """commit 의 tree id — 증거에 같이 적는다. 같은 tree 를 가리키는 다른 커밋과 구별할 근거다 (Codex R11 P2-6)."""
    return _git(target, "rev-parse", f"{head}^{{tree}}").strip()





EXCLUSION_KINDS = ("전제 변경", "환경상 불가", "우리 코드 밖", "미실행 (그룹 중단)")


#: run receipt 의 판 — 묶는 규칙이 바뀌면 올린다 (옛 서명과 새 서명이 섞여 보이지 않게).
RUN_RECEIPT_VERSION = "r16.1"


def _canonical(obj) -> str:
    """서명이 덮는 **정규 직렬화** — 키 순서·공백이 서명을 바꾸면 그 서명은 내용을 말하지 않는다."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def receipt_signature(receipt: dict) -> str:
    """`signature` 를 뺀 **나머지 전부**의 digest. 필드 하나만 고쳐도 달라진다."""
    body = {k: v for k, v in receipt.items() if k != "signature"}
    return hashlib.sha256((RUN_RECEIPT_VERSION + "\n" + _canonical(body)).encode("utf-8")).hexdigest()


def run_receipt(*, head: str, tree: str, instrument: dict, package_digest: str,
                materialized=None, runtime=None) -> dict:
    """조각들을 **한 객체**로 묶고 서명한다 (조건 8 축 ③).

    왜 묶나 (R12 §5 답변 4): 조각이 흩어져 있으면 증거 JSON 의 필드 하나를 고쳐도 아무도 모른다.
    묶어서 서명하면 사후 편집이 드러나고, 소비자가 `code.commit` 의 **ancestry** 를 대면 "이 저장소의
    역사에 없는 커밋에서 나왔다는 증거" 를 거부할 수 있다.

    ⚠ 서명은 **내용이 안 바뀌었다**만 말한다. 그 내용이 이 저장소와 관계있다는 것은 말하지 않는다 —
      그래서 소비자가 ancestry 와 tree 짝을 따로 본다 (`scripts/verify_run_receipt.py`).
    """
    import datetime as _dt
    r = {"receipt_version": RUN_RECEIPT_VERSION,
         "code": {"commit": str(head), "tree": str(tree)},
         "instrument": dict(instrument or {}),
         "package": {"digest": str(package_digest)},
         "materialized": materialized,
         "runtime": dict(runtime or {}),
         "produced_utc": _dt.datetime.now(_dt.timezone.utc).isoformat()}
    r["signature"] = receipt_signature(r)
    return r


def summarize_verdicts(records: dict, requested, substitutes: dict | None = None) -> dict:
    """러너 넷이 **같은** 규칙으로 종결을 적는다 (Codex R13 P1-3).

    전 판은 러너마다 집계가 따로였고, 셋은 전제 변경·환경상 불가·우리 코드 밖을 `unresolved` 에서 빼고는
    `closed: true` · "모든 case 가 닫혔다" 라고 적었다 — 요청문의 "닫힘으로 세지 않았다" 와 기계용 결론이 달랐다.
    이제 네 가지를 **별도 필드**로 둔다:

      report_complete         요청한 leaf 마다 판정이 있고 `오류` 가 없다        ← rc 0 의 뜻
      closed                  요청한 leaf 가 **전부** `반례 소멸`                  ← 엄격
      closed_with_substitutes 제외된 leaf 마다 대체 증거의 **이름**이 있고 나머지는 반례 소멸
      excluded                제외 leaf 와 그 이유·대체 증거

    미실행/전제 변경은 대체 증거 없이는 `closed` 의 근거가 아니다. GO 소비자는 rc 가 아니라 `closed` 를 읽는다.
    """
    substitutes = dict(substitutes or {})
    requested = list(requested)
    statuses = {k: (r or {}).get("상태") for k, r in records.items()}
    leaf = {k: statuses.get(k, "미실행") for k in requested}
    missing = [k for k in requested if k not in statuses]
    excluded = {k: {"상태": s, "대체": substitutes.get(k), "세부": (records[k] or {}).get("세부")}
                for k, s in statuses.items() if s in EXCLUSION_KINDS}
    errors = {k: s for k, s in statuses.items() if s != "반례 소멸" and s not in EXCLUSION_KINDS}
    gone = [k for k, s in statuses.items() if s == "반례 소멸"]
    unsubstituted = [k for k, v in excluded.items() if not v["대체"]]
    report_complete = not missing and not errors
    kinds = {}
    for v in excluded.values():
        kinds[v["상태"]] = kinds.get(v["상태"], 0) + 1
    kinds_txt = " · ".join(f"{k} {n}" for k, n in kinds.items()) or "없음"
    if report_complete:
        reason = (f"보고 완료 — 반례 소멸 {len(gone)}/{len(requested)} · 제외 {len(excluded)} ({kinds_txt}). "
                  f"closed 는 반례 소멸만 센다; closed_with_substitutes 는 대체 증거가 이름 붙은 제외까지 센다"
                  + (f"; 대체 증거 없는 제외 {unsubstituted}" if unsubstituted else ""))
    else:
        reason = f"보고 미완 — 오류 {errors} · 미실행 {missing}"
    return {
        "leaf_cases": leaf,
        "counts": {"반례 소멸": len(gone), "제외": len(excluded), "오류": len(errors), "미실행": len(missing)},
        "excluded": excluded, "errors": errors, "missing": missing,
        "report_complete": report_complete,
        "closed": report_complete and not excluded,
        "closed_with_substitutes": report_complete and not unsubstituted,
        "rc_reason": reason,
    }
