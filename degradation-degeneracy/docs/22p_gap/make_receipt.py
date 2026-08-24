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
import json
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
sys.path.insert(0, str(REPO))

#: 산출 manifest 의 semantic digest 규격. 표현이 바뀌어도 내용이 같으면 같다.
CANONICALIZER = "score-semantic/v1"


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _semantic(obj) -> str:
    """dict → 정규 직렬화 digest. 키 순서·YAML 표현에 무관하다."""
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)
        .encode("utf-8")).hexdigest()


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

        # ── 3. 복원본 검증 — cwd 를 빈 root 로 옮겨 원본에 손이 닿지 않게 ──
        cwd = Path.cwd()
        os.chdir(root)
        try:
            v = validate_provenance(run_dir)
        finally:
            os.chdir(cwd)
        if not v.get("ok"):
            raise SystemExit(f"✗ 복원본 validate 실패: {v.get('fail')}")

        # ── 4. 복원한 fits 로만 재채점 ──────────────────────────────────
        outputs = _score_manifest(run_dir)

        core = {
            "leg_id": leg,
            "bundle": {
                "uri": str(bundle.relative_to(REPO)),
                "files": len(members),
                "bytes": sum(p.stat().st_size for p in members),
                "payload_index": str(payload_index.relative_to(REPO)),
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
                "run_dir_relative": str(run_dir.relative_to(root)),
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
            },
            "outputs": outputs,
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

    from src.scoring import (DEFAULT_TOL, add_error_columns, apply_bias_correction,
                             classify_recoverability, clean_bias, summarize)

    fits = run_dir / "fits.parquet"
    df = pd.read_parquet(fits)
    # `row_projection.py` 와 **같은 정규 경로** — 여기서 갈리면 두 감사 도구가
    # 다른 것을 검증하게 된다.
    df = add_error_columns(df, DEFAULT_TOL)
    df = classify_recoverability(df)
    bias = clean_bias(df)
    df = apply_bias_correction(df, bias, DEFAULT_TOL)
    summary = summarize(df, DEFAULT_TOL)

    out = [{
        "role": "rescored_summary",
        "produced_from": "restored fits.parquet only",
        "source_file_sha256": _sha(fits),
        "n_rows": int(len(df)),
        "semantic_schema": "degeneracy-summary/v5",
        "canonicalizer": CANONICALIZER,
        "semantic_sha256": _semantic(summary),
    }]

    # 봉인된 summary 가 묶음 안에 있으면 자리별로 대조한다
    sealed = run_dir / "degeneracy_summary.yaml"
    if sealed.is_file():
        sd = yaml.safe_load(sealed.read_text(encoding="utf-8"))
        out.append({
            "role": "sealed_summary",
            "relative_path": sealed.name,
            "byte_size": sealed.stat().st_size,
            "file_sha256": _sha(sealed),
            "semantic_schema": "degeneracy-summary/v5",
            "canonicalizer": CANONICALIZER,
            "semantic_sha256": _semantic(sd),
        })
    return out


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
        path.write_text(text, encoding="utf-8")
        print(f"✅ {leg}: {path.relative_to(REPO)} · "
              f"검사 {rec['core']['validation']['n_checks']}건 · "
              f"산출 {len(rec['core']['outputs'])}건 · "
              f"core_sha {rec['core_sha256'][:16]}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
