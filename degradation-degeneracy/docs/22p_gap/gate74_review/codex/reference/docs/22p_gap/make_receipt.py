"""make_receipt.py — 보존 묶음의 **재생 가능한 구조화 영수증**을 만든다.

★ 25차 발견 4 — 초판 영수증은 42줄 텍스트였고, 머리에 적힌 재생성 명령
  (`print(validate_provenance(...))`) 은 그 형식을 만들지 않는다. 함수는 dict 를
  돌려준다. formatter 도 capture 명령도 없었으므로 **손으로 쓴 것과 구별할 수
  없었다.** 게다가 영수증이 bundle URI · payload-index SHA · 복원 root ·
  validator identity · score/analyze 산출과 결속돼 있지 않아, 다른 묶음에서 만든
  성공문을 옮겨 적어도 확인할 방법이 없었다.

이 스크립트가 하는 것 — 리뷰가 요구한 순서 그대로:

    1. 묶음 member 전수 재해시      (tools.archive_bundle.check)
    2. **truly empty root** 로 복원  (원본 results/ 에 접근하지 않는다)
    3. 복원본에 validate_provenance
    4. 복원한 fits 로만 재채점 → score/analyze 산출 manifest
    5. 위 전부를 한 YAML 로 봉인

산출 manifest 는 **두 digest 를 다 담는다** (25차 Q2):

    file_sha256      복원한 바이트가 정확한가 — transport/audit 계약
    semantic_sha256  표현이 바뀌어도 과학 내용이 같은가 — computation 계약

왜 `tools/` 가 아니라 `docs/` 인가:
  `tools/` 는 RUN_SCOPE 라 여기 파일을 만들면 `source_digest` 가 움직이고
  기존 산출물의 code identity 대조가 흔들린다. 이 스크립트는 감사 도구이지
  계산 경로가 아니므로 `row_projection.py` 와 같은 자리에 둔다. 계약 v4
  묶음 9 의 **강제** gate 는 `tools/` 로 들어간다 (그때 digest 를 동결한다).

사용:
    python3 docs/22p_gap/make_receipt.py paired_fixed5_v4
    python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check   # 재생성 대조만
"""

from __future__ import annotations

import argparse
import hashlib
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent.parent
RECEIPTS = REPO / "docs" / "22p_gap" / "receipts"
sys.path.insert(0, str(REPO))          # `tools.` import 보다 **먼저** 와야 한다

from tools.preserve import canonical_bytes    # noqa: E402

#: 산출 manifest 의 semantic digest 규격. 표현이 바뀌어도 내용이 같으면 같다.
CANONICALIZER = "score-semantic/v3"

#: 정규 view — 두 summary 를 비교하기 전에 **양쪽에서** 떼는 키.
#:
#: ★ 27차 P1-6 — v2 는 `_F4_주의` 까지 떼고 있었다. 그런데 그것은 실행 메타가
#:   아니라 `summarize()` 가 **결정론적으로 만드는 인용 금지 경고**다
#:   (`src/scoring.py:369`). 떼어 놓으니 "이 블록을 인용하지 말 것" 을
#:   "인용해도 안전" 으로 바꿔도 semantic digest 가 같았다. 안전 문구를
#:   hash 밖으로 버린 것이다. → 뺐다. 양쪽이 다 만드는 값이므로 비교된다.
#:
#: 남는 것은 `_채점원본` 하나다 — `run_scoring` 이 붙이는 실행 메타라 재채점이
#: 만들 수 없다. 다만 그 안에는 `canonical`·`봉인상태`·`인용가능` 같은
#: **인용 안전 flag** 가 있으므로 통째로 버리지 않고 §citation_safety 로
#: 따로 검사한다 (아래 `_citation_safety`).


def _row_projection():
    """정본 채점 경로를 가진 모듈. import 로 묶어 복제를 막는다."""
    import importlib.util

    src = REPO / "docs" / "22p_gap" / "row_projection.py"
    spec = importlib.util.spec_from_file_location("_rp_receipt", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _plain(o):
    """JSON 기본형으로만 이루어진 구조로 낮춘다 (numpy 스칼라 등)."""
    if isinstance(o, dict):
        return {str(k): _plain(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_plain(v) for v in o]
    if isinstance(o, bool) or o is None or isinstance(o, (int, str)):
        return o
    if isinstance(o, float):
        return o
    item = getattr(o, "item", None)                  # numpy 스칼라
    return _plain(item()) if callable(item) else str(o)


def _semantic_skip() -> tuple:
    """★ 28차 P1-4 — semantic view 를 여기서 **정의하지 않는다.**

    `row_projection.py` 의 비교기와 갈리면 한쪽이 안전 문구를 떼고도 통과한다
    (실제로 그랬다). 정본은 `row_projection.SEMANTIC_SKIP` 하나다.
    """
    return tuple(_row_projection().SEMANTIC_SKIP)


def _semantic_view(obj):
    """비교 대상 정규 view. 실행 메타를 떼고 JSON 기본형으로 낮춘다."""
    return _plain({k: v for k, v in obj.items() if k not in _semantic_skip()}
                  if isinstance(obj, dict) else obj)


def _semantic(obj) -> str:
    """dict → 정규 직렬화 digest. 키 순서·YAML 표현에 무관하다.

    ★ 자체 발견 — 초판은 여기서 직렬화를 **따로** 적었다 (기본 구분자).
      `tools.preserve.canonical_bytes` 는 고정 구분자를 쓴다. 둘 다 산출
      manifest 에 `canonicalizer: score-semantic/v1` 이라고 적었으므로 **한
      버전 라벨이 두 바이트 스트림을 가리켰다.** 정규화는 한 곳이어야 한다.
    """
    return hashlib.sha256(canonical_bytes(_semantic_view(obj))).hexdigest()


def _git(*args: str) -> str:
    try:
        return subprocess.run(("git", *args), cwd=REPO, capture_output=True,
                              text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def build(leg: str) -> dict:
    """묶음 하나의 영수증을 만든다. 어느 단계든 어긋나면 SystemExit."""
    from src.io import source_digest, validate_provenance
    from tools.archive_bundle import check as bundle_check
    from tools.archive_bundle import restore

    bundle = REPO / "artifacts" / leg
    if not bundle.is_dir():
        raise SystemExit(f"✗ 묶음이 없다: {bundle}")

    # ── 1. member 전수 재해시 ────────────────────────────────────────────
    chk = bundle_check(bundle)
    if not chk.get("ok"):
        raise SystemExit(f"✗ archive_bundle.check 실패: {chk.get('missing')[:5]}")
    members = sorted(p for p in bundle.rglob("*") if p.is_file())
    payload_index = bundle / "payload_sha256.yaml"

    # ── 2. truly empty root 로 복원 ──────────────────────────────────────
    root = Path(tempfile.mkdtemp(prefix=f"receipt_{leg}_"))
    try:
        res = restore(bundle, repo_root=root)
        if not res.get("ok") or res.get("conflict"):
            raise SystemExit(f"✗ empty-root 복원 실패: {res.get('conflict')[:3]}")
        run_dir = Path(res["run_dir"])

        # ── 3. 복원본 검증 ──────────────────────────────────────────────
        # ★ 26차 P1-5 — `os.chdir` 로는 검증 root 가 바뀌지 않는다. 검증기는
        #   cwd 가 아니라 `src/io.py` 가 있는 저장소를 root 로 잡으므로
        #   (`src/io.py:1328`), 봉인 입력을 **원본 checkout** 에서 풀었다.
        #   그래서 이 컨테이너에서는 통과하고 리뷰어의 clean checkout 에서는
        #   `producer_곡선일치`·`입력_digest_재해시` 로 실패했다.
        v = validate_provenance(run_dir, repo_root=root)
        if not v.get("ok"):
            raise SystemExit(f"✗ 복원본 validate 실패: {v.get('fail')}")

        # ── 4. 복원한 fits 로만 재채점 ──────────────────────────────────
        outputs = _score_manifest(run_dir)

        core = {
            "leg_id": leg,
            "bundle": {
                "uri": bundle.relative_to(REPO).as_posix(),
                "files": len(members),
                "bytes": sum(p.stat().st_size for p in members),
                "payload_index": payload_index.relative_to(REPO).as_posix(),
                "payload_index_sha256": _sha(payload_index),
                "member_rehash": "tools.archive_bundle.check",
                "member_mismatches": 0,
                "fits_sha256": _sha(bundle / "fits.parquet"),
            },
            "restore": {
                "mode": "empty_root",
                "command": ("python3 -c \"from tools.archive_bundle import restore; "
                            f"restore('artifacts/{leg}', repo_root=<empty>)\""),
                "files_written": len(res["written"]),
                "run_dir_relative": Path(os.path.relpath(run_dir, root)).as_posix(),
                "conflicts": 0,
            },
            "validation": {
                "validator": "src.io.validate_provenance",
                "ok": bool(v["ok"]),
                "fail": list(v["fail"]),
                "n_checks": len(v["checks"]),
                "checks": {k: str(v["checks"][k]) for k in sorted(v["checks"])},
            },
            "identity": {
                # validator 쪽 (현행 트리). 여기 있는 것은 전부 **소스 바이트**라
                # 재생성해도 같다 — commit·시각·dirty 는 stamp 로 뺐다.
                "validator_source_digest": source_digest(),
                "src_io_sha256": _sha(REPO / "src" / "io.py")[:16],
                "src_scoring_sha256": _sha(REPO / "src" / "scoring.py")[:16],
                "archive_bundle_sha256": _sha(REPO / "tools" / "archive_bundle.py")[:16],
                "make_receipt_sha256": _sha(Path(__file__).resolve())[:16],
                # ★ 27차 P1-6 — 정본 채점 경로가 여기 있는데 identity 에
                #   없었다. `docs/` 는 RUN_SCOPE 밖이라 source_digest 도 안 본다.
                "row_projection_sha256": _sha(
                    REPO / "docs" / "22p_gap" / "row_projection.py")[:16],
                "row_projection_compute_sha256": _row_projection()._compute_sha256(),
            },
            "outputs": outputs,
            # ★ 26차 P1-6 — 대조 **결과**를 적는다. 초판은 두 digest 를 나란히
            #   두기만 하고 비교하지 않았고, 실제로 달랐다.
            "outputs_agree": _outputs_agree(outputs),
        }
        return {
            "schema_version": 2,
            "_주의": ("이 파일은 손으로 쓰지 않는다. "
                    "`python3 docs/22p_gap/make_receipt.py <leg>` 가 만들고 "
                    "`--check` 가 **core 바이트 동일** 재생성을 확인한다."),
            # ★ core 와 stamp 를 가르는 이유: commit SHA·실행 시각·dirty 여부는
            #   영수증을 커밋하는 순간 바뀐다. 그것들을 core 에 두면 커밋된
            #   영수증이 원리적으로 재생 불가능해진다. core 는 **묶음 바이트와
            #   validator 소스에서만** 나오므로 언제 어디서 돌려도 같다.
            "core_sha256": hashlib.sha256(
                _dump(core).encode("utf-8")).hexdigest(),
            "core": core,
            "stamp": {
                "_주의": "기록용. core 재생성 대조에서 제외된다.",
                "validator_commit": _git("rev-parse", "HEAD"),
                "validator_tree_dirty": bool(_git("status", "--porcelain")),
                "generated_at_utc": datetime.now(timezone.utc)
                                    .strftime("%Y-%m-%dT%H:%M:%SZ"),
                "runtime": {"python": platform.python_version(),
                            "platform": platform.platform()},
            },
        }
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _score_manifest(run_dir: Path) -> list[dict]:
    """복원한 fits 만으로 재채점하고 산출을 두 digest 로 적는다."""
    import pandas as pd

    from src.scoring import DEFAULT_TOL, summarize

    fits = run_dir / "fits.parquet"
    df = pd.read_parquet(fits)
    # `row_projection.py` 의 **정본** 채점 경로를 그대로 부른다 — 복제하지 않는다.
    rp = _row_projection()
    scored = rp.score_canonical(df)
    summary = summarize(scored, DEFAULT_TOL)
    # ★ 26차 P1-6 — `summarize()` 는 `multistart`·`multistart_random_only` 를
    #   만들지 않는다 (`run_scoring` 이 restart trace 에서 따로 붙인다). 그것을
    #   빼고 봉인본과 비교하면 **영원히 다르다** — 초판이 정확히 그 상태였고,
    #   두 digest 를 나란히 적어 놓고 비교는 안 했으므로 아무도 몰랐다.
    rp._add_multistart_blocks(scored, summary)

    # 재채점 결과를 **실제 파일로** 떨궈 byte digest 도 남긴다 (25차 Q2 는
    # file SHA 와 semantic digest 를 **둘 다** 요구한다)
    rescored_path = run_dir / "_rescored_summary.yaml"
    # ★ 27차 P1-7 — `write_text` 는 기본 newline 변환을 쓴다. Windows 에서
    #   CRLF 가 되어 byte size·file SHA·core sha 가 OS 마다 달라졌다
    #   (리뷰 실측: 8877 → 9087 bytes). LF 로 고정한다.
    rescored_path.write_bytes(
        yaml.safe_dump(_plain(summary), allow_unicode=True,
                       sort_keys=True).encode("utf-8"))

    out = [{
        "role": "rescored_summary",
        "produced_from": "restored fits.parquet only",
        "source_file_sha256": _sha(fits),
        "relative_path": rescored_path.name,
        "byte_size": rescored_path.stat().st_size,
        "file_sha256": _sha(rescored_path),
        "n_rows": int(len(df)),
        "semantic_schema": "degeneracy-summary/v5",
        "canonicalizer": CANONICALIZER,
        "semantic_view_drops": list(_semantic_skip()),
        "semantic_sha256": _semantic(summary),
    }]

    # 봉인된 summary 를 **정규 view 로 대조**한다 — append 만 하지 않는다.
    # ★ 27차 P1-6 — 없으면 "일치" 가 아니라 **비교 불가**다.
    sealed = run_dir / "degeneracy_summary.yaml"
    if not sealed.is_file():
        raise SystemExit(f"✗ 봉인 summary 가 없다: {sealed} — 대조 없이 영수증을 "
                         "만들지 않는다 (27차 P1-6)")
    if True:
        sd = yaml.safe_load(sealed.read_text(encoding="utf-8"))
        _citation_safety(sd, _sha(fits))
        out.append({
            "role": "sealed_summary",
            "relative_path": sealed.name,
            "byte_size": sealed.stat().st_size,
            "file_sha256": _sha(sealed),
            "semantic_schema": "degeneracy-summary/v5",
            "canonicalizer": CANONICALIZER,
            "semantic_view_drops": list(_semantic_skip()),
            "semantic_sha256": _semantic(sd),
        })
    return out


def _citation_safety(sealed: dict, fits_sha: str) -> dict:
    """봉인 summary 의 **인용 안전 flag** 를 값으로 검사한다.

    ★ 27차 P1-6 — `_채점원본` 을 통째로 정규 view 에서 빼면 그 안의
      `canonical`·`봉인상태`·`인용가능` 을 반대로 바꿔도 digest 가 같다.
      equality 로는 못 보므로 **명시적 assertion** 으로 본다.
    """
    src = (sealed or {}).get("_채점원본") or {}
    want = {"canonical": True, "봉인상태": "정상", "인용가능": True}
    bad = [f"{k}={src.get(k)!r} ≠ {v!r}" for k, v in want.items()
           if src.get(k) != v]
    if src.get("fits_sha256") != fits_sha:
        bad.append(f"fits_sha256 이 재채점한 파일과 다르다 "
                   f"({str(src.get('fits_sha256'))[:16]} ≠ {fits_sha[:16]})")
    if bad:
        raise SystemExit("✗ 봉인 summary 의 인용 안전 flag 가 어긋난다: "
                         + "; ".join(bad) + "\n  (27차 P1-6)")
    return {"checked": sorted(want), "fits_sha256_bound": True,
            "fits_path_basename": str(src.get("fits", "")).rsplit("/", 1)[-1]}


def _outputs_agree(outputs: list[dict]) -> bool:
    """같은 schema·canonicalizer 를 쓰는 산출끼리 semantic digest 가 같은가.

    다르면 `build()` 가 여기서 멈춘다 — 영수증에 `false` 를 적어 두고 통과시키면
    "대조했다" 는 말이 다시 거짓이 된다.
    """
    by: dict[tuple, list] = {}
    for o in outputs:
        by.setdefault((o["semantic_schema"], o["canonicalizer"]),
                      []).append(o["semantic_sha256"])
    # ★ 27차 P1-6 — 초판은 산출이 **하나뿐이어도** `True` 였다. 비교 대상이
    #   없는데 "일치" 라고 적으면 그 말이 다시 거짓이 된다. 짝이 없으면 실패.
    lonely = [k for k, v in by.items() if len(v) < 2]
    if lonely:
        raise SystemExit(
            f"✗ 대조할 짝이 없다: {lonely} — 산출이 하나뿐이면 "
            "'일치' 가 아니라 **비교 불가**다 (27차 P1-6)")
    bad = [k for k, v in by.items() if len(set(v)) > 1]
    if bad:
        raise SystemExit(
            f"✗ 같은 schema·canonicalizer 인데 semantic digest 가 갈렸다: {bad}\n"
            "  같은 object 가 아니면 schema/role 을 갈라라 (26차 P1-6)")
    return True


def _dump(rec: dict) -> str:
    return yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, width=100)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("legs", nargs="+")
    ap.add_argument("--check", action="store_true",
                    help="다시 만들어 커밋된 것과 바이트 동일한지만 본다")
    a = ap.parse_args(argv)

    RECEIPTS.mkdir(parents=True, exist_ok=True)
    rc = 0
    for leg in a.legs:
        rec = build(leg)
        text = _dump(rec)
        path = RECEIPTS / f"{leg}.validate.yaml"
        if a.check:
            if not path.is_file():
                print(f"❌ {leg}: 영수증이 없다 {path}")
                rc = 1
                continue
            old = yaml.safe_load(path.read_text(encoding="utf-8"))
            same = (_dump(old.get("core")) == _dump(rec["core"])
                    and old.get("core_sha256") == rec["core_sha256"])
            print(f"{'✅' if same else '❌'} {leg}: core 재생성 "
                  f"{'바이트 동일' if same else '불일치'} · "
                  f"core_sha {rec['core_sha256'][:16]}")
            if not same:
                rc = 1
            continue
        path.write_bytes(text.encode("utf-8"))   # LF 고정 (27차 P1-7)
        print(f"✅ {leg}: {path.relative_to(REPO)} · "
              f"검사 {rec['core']['validation']['n_checks']}건 · "
              f"산출 {len(rec['core']['outputs'])}건 · "
              f"core_sha {rec['core_sha256'][:16]}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
