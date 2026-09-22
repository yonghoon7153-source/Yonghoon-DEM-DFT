#!/usr/bin/env python3
"""run receipt 의 **소비자** — 서명·ancestry·tree·instrument 를 댄다 (조건 8 축 ③).

    python3 scripts/verify_run_receipt.py --receipt r11.json --target . [--head <40-hex>] [--skip-instrument]

receipt 를 **묶어서 서명한 것만으로는 부족하다.** 서명은 "내용이 안 바뀌었다" 만 말하고, 그 내용이 이
저장소와 관계있다는 것은 말하지 않는다 — 잘 만든 거짓말은 서명도 잘 맞는다. 그래서 넷을 본다:

  ① **서명**      — 필드 하나라도 고쳐졌으면 어긋난다
  ② **ancestry**  — `code.commit` 이 기준 커밋의 **조상(또는 자신)** 인가. 이 저장소의 역사에 없는
                    커밋에서 나왔다는 증거는 거부한다
  ③ **tree**      — 그 커밋의 tree 와 짝이 맞는가 (커밋만 진짜이고 tree 는 남의 것일 수 없다)
  ④ **instrument** — 적힌 도구 digest 가 그 커밋의 blob 과 같은가 (`--skip-instrument` 로 뺄 수 있다 —
                    receipt 가 다른 저장소의 도구를 가리킬 때의 진단용이고, 뺐다는 사실이 출력에 남는다)

### 자기참조 (R12 Q3 의 답: 자기를 인증하지 않고 **선언한다**)

이 스크립트가 "나는 봉인돼 있다" 고 스스로 말하면 그것은 순환이다 — 고친 스크립트도 같은 말을 한다.
그래서 **자기 경로·digest·기준 커밋을 출력에 드러내기만** 한다. 그 파일이 변조됐는지는 이미 있는
`evidence_gate.instrument_sealed` 가 **바깥에서** 본다. 판단의 근거를 내가 만들지 않는 것이 요점이다.

종료 코드: 0 검증됨 · 2 입력 문제 · **3 검증 실패**.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "reviews"))
import evidence_gate as gate                     # noqa: E402

_HEX40 = 40
_HEX64 = 64
_HEXRE = __import__("re").compile(r"^[0-9a-f]+$")


def _is_hex(v, n: int) -> bool:
    return isinstance(v, str) and len(v) == n and bool(_HEXRE.fullmatch(v))


def _typed_problems(r: dict) -> list:
    """run receipt 의 **nested schema** (R17 후속 P2-02).

    생산자(`reviews/evidence_gate.py:run_receipt`)가 실제로 내는 모양이 정본이다:
      code       {commit: 40hex, tree: 40hex}
      instrument {상대경로: 40hex blob} — 비어 있지 않다
      package    {digest: 64hex}         — **검사 상태가 아니라 내용 주소**
      materialized  None **또는** 객체   — 생산자가 둘 다 낸다 (없음도 뜻이 있다)
      runtime    비지 않은 객체
      produced_utc  ISO-8601 시각 문자열
    `materialized=None` 을 금지하지 않는다 — 리뷰어가 짚은 대로 그 상태는 생산자가 허용한다.
    금지하는 것은 **뜻을 알 수 없는 타입**이다 (`17` 은 "무엇이 materialize 됐다" 를 말하지 않는다).
    """
    import datetime as _dt

    p = []
    code = r.get("code")
    if not isinstance(code, dict) or not _is_hex(code.get("commit"), _HEX40) \
            or not _is_hex(code.get("tree"), _HEX40):
        p.append(f"code 가 {{commit: 40hex, tree: 40hex}} 가 아니다 ({code!r})")
    inst = r.get("instrument")
    if not isinstance(inst, dict) or not inst \
            or not all(isinstance(k, str) and _is_hex(v, _HEX40) for k, v in inst.items()):
        p.append("instrument 가 {경로: 40hex blob} 의 비지 않은 객체가 아니다")
    pkg = r.get("package")
    if isinstance(pkg, dict) and not _is_hex(pkg.get("digest"), _HEX64):
        p.append(f"package.digest 가 64자리 hex 내용 주소가 아니다 ({pkg.get('digest')!r}) — "
                 f"검사 상태 문자열을 내용 주소 자리에 넣지 않는다")
    # ⚠ R17 후속 2차 F2-06: 전 판은 **바깥 컨테이너에서 멈췄다** — `materialized` 는 `isinstance(dict)`,
    #   `runtime` 은 `bool(dict)` 만 봤다. 내부 필드의 계약은 `evidence_gate` 에 한 벌로 적고
    #   **생산자와 소비자가 같은 함수**를 부른다 (규칙이 두 벌이면 절반만 구현된다).
    if "materialized" in r:
        p += gate.materialized_problems(r.get("materialized"))
    p += gate.runtime_problems(r.get("runtime"))
    ts = r.get("produced_utc")
    ok_ts = isinstance(ts, str) and bool(ts.strip())
    if ok_ts:
        try:
            _dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            ok_ts = False
    if not ok_ts:
        p.append(f"produced_utc 가 ISO-8601 시각이 아니다 ({ts!r})")
    return p


def _git(target, *args):
    return subprocess.run(["git", "-C", str(target), *args], capture_output=True, text=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--receipt", required=True, type=pathlib.Path)
    ap.add_argument("--target", default=pathlib.Path("."), type=pathlib.Path)
    ap.add_argument("--head", default=None, help="기준 커밋 (기본: target 의 HEAD)")
    ap.add_argument("--skip-instrument", action="store_true",
                    help="도구 digest 대조를 건너뛴다 — **뺐다는 사실이 출력에 남는다**")
    a = ap.parse_args(argv)

    try:
        r = json.loads(a.receipt.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"! receipt 를 못 읽었다 ({a.receipt}): {e}", file=sys.stderr)
        return 2
    if not isinstance(r, dict) or "signature" not in r or "code" not in r:
        print("! run receipt 의 모양이 아니다 (signature·code 가 있어야 한다)", file=sys.stderr)
        return 2

    ref = _git(a.target, "rev-parse", "HEAD")
    if ref.returncode != 0:
        print(f"! target 이 git 저장소가 아니다 ({a.target})", file=sys.stderr)
        return 2
    base = (a.head or ref.stdout).strip()

    me = {"path": str(pathlib.Path(__file__).resolve().relative_to(HERE.parent.parent)
                      if str(HERE.parent.parent) in str(HERE) else pathlib.Path(__file__).name),
          "sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
          "checked_against": base,
          "note": "이 검증기는 **자기를 인증하지 않는다 — 드러낼 뿐이다** (R12 Q3). 변조 여부는 "
                  "`evidence_gate.instrument_sealed` 가 바깥에서 본다"}

    checks, failed = {}, []

    # ⚠ Codex R17 P2-02: 전 판은 code/instrument/signature 만 있는 객체 — receipt_version·package·materialized·
    #   runtime·produced_utc 가 **없는** 것 — 에 `verified=true` 를 줬다 (서명·ancestry·tree 대조는 맞았으므로).
    #   서명은 "내용이 안 바뀌었다" 만 말하고 ancestry 는 "그 커밋이 역사에 있다" 만 말한다 — 둘 다 **run receipt 의
    #   완전성**을 말하지 않는다. typed 필수 구조와 지원 version 을 **먼저** 보고, 빠지면 전체 verified 를 주지 않는다.
    #   부분 대조(코드 참조)가 맞았다는 사실은 `code_reference_verified` 라는 **다른 상태**로 따로 낸다.
    required = ("receipt_version", "code", "instrument", "package", "materialized", "runtime", "produced_utc",
                "signature")
    missing = [k for k in required if k not in r]
    ok_version = r.get("receipt_version") == gate.RUN_RECEIPT_VERSION
    ok_package = isinstance(r.get("package"), dict) and bool(str((r.get("package") or {}).get("digest") or "").strip())
    # ⚠ Codex R17 후속 P2-02: 전 판은 **키가 있는가**만 봤다. 그래서 `runtime=null`·
    #   `runtime="not-a-runtime-object"`·`materialized=17`·`produced_utc="not-a-date"`·
    #   `package.digest="not-a-digest"` 가 전부 `verified=true` 였다 (서명을 정확히 다시 계산한
    #   영수증이므로 암호학적 위조가 아니다 — **typed 완전성**의 문제다). 공개 checksum·ancestry 가
    #   통과한다는 것은 그 객체가 **완전하다**는 뜻이 아니다. 아래가 그 schema 다.
    typed = _typed_problems(r)
    checks["complete"] = not missing and ok_version and ok_package and not typed
    if missing:
        failed.append(f"run receipt 의 필수 결속이 빠졌다: {missing} — 불완전한 객체는 전체 검증을 받지 않는다")
    if not ok_version:
        failed.append(f"receipt_version 이 지원 버전이 아니다 (적힌 {r.get('receipt_version')!r} ≠ "
                      f"{gate.RUN_RECEIPT_VERSION!r})")
    if "package" in r and not ok_package:
        failed.append("package.digest 가 비었다 — 묶음 결속 없는 receipt 는 실행 증거가 아니다")
    failed += typed

    want_sig = gate.receipt_signature(r)
    checks["signature"] = (want_sig == r["signature"])
    if not checks["signature"]:
        failed.append(f"서명이 내용과 다르다 — 사후 편집이다 (계산 {want_sig[:12]} ≠ 적힌 {str(r['signature'])[:12]})")

    commit, tree = str(r["code"].get("commit", "")), str(r["code"].get("tree", ""))
    ok_anc = (len(commit) == _HEX40
              and _git(a.target, "cat-file", "-e", f"{commit}^{{commit}}").returncode == 0
              and _git(a.target, "merge-base", "--is-ancestor", commit, base).returncode == 0)
    checks["ancestry"] = ok_anc
    if not ok_anc:
        failed.append(f"ancestry — receipt 의 커밋 {commit[:12] or '(없음)'} 이 {base[:12]} 의 조상이 아니다 "
                      f"(이 저장소의 역사에 없는 커밋의 증거는 받지 않는다)")

    ok_tree = False
    if ok_anc:
        got = _git(a.target, "rev-parse", f"{commit}^{{tree}}")
        ok_tree = got.returncode == 0 and got.stdout.strip() == tree
    checks["tree"] = ok_tree
    if ok_anc and not ok_tree:
        failed.append(f"tree 가 그 커밋의 것이 아니다 (적힌 {tree[:12] or '(없음)'})")

    if a.skip_instrument:
        checks["instrument"] = None
    else:
        detail = {}
        for rel, want in (r.get("instrument") or {}).items():
            # ⚠ R16 실측: 이 저장소는 모노레포라 `<commit>:<rel>` 은 **저장소 루트** 기준이다 —
            #   `./` 를 붙여야 `-C target` 의 cwd 기준이 된다 (gate 의 `instrument_sealed` 가 쓰는 그 형식).
            #   빠뜨렸더니 깨끗한 트리에서도 언제나 "다름" 이었다.
            got = _git(a.target, "rev-parse", f"{commit}:./{rel}")
            detail[rel] = "ok" if (got.returncode == 0 and got.stdout.strip() == str(want)) else "다름"
        checks["instrument"] = bool(detail) and all(v == "ok" for v in detail.values())
        if not checks["instrument"]:
            failed.append(f"instrument digest 가 그 커밋의 blob 과 다르다: "
                          f"{sorted(k for k, v in detail.items() if v != 'ok')}")

    code_ref_ok = bool(checks["signature"] and checks["ancestry"] and checks["tree"]
                       and (checks["instrument"] in (True, None)))
    verdict = {"verified": not failed, "checks": checks, "failed": failed,
               # 부분 상태 — 코드 참조(서명·ancestry·tree·instrument)만 맞은 객체는 **이것**이고 verified 가 아니다
               "code_reference_verified": code_ref_ok,
               # ⚠ R17 후속 2차 F2-06: 실행환경을 **부분/unknown 으로 적은 것**을 complete 와 구분해 드러낸다
               #   (리뷰어: "부분·unknown 기록을 허용한다면 complete/verified 와 구분한다").
               "runtime_partial": bool(gate.runtime_problems(r.get("runtime"))),
               "receipt": str(a.receipt), "receipt_version": r.get("receipt_version"),
               "code": r.get("code"), "skipped_instrument": bool(a.skip_instrument),
               "verifier": me}
    print(f"\n══ run receipt 검증 — {a.receipt.name} ══")
    print(f"  완전성 {'ok' if checks['complete'] else '**불완전**'} · "
          f"서명 {'ok' if checks['signature'] else '**다름**'} · "
          f"ancestry {'ok' if checks['ancestry'] else '**아님**'} · "
          f"tree {'ok' if checks['tree'] else '**아님**'} · "
          f"instrument {'건너뜀' if checks['instrument'] is None else ('ok' if checks['instrument'] else '**다름**')}")
    print(f"  기준 커밋 {base}")
    for f in failed:
        print(f"  ! {f}")
    print(f"  검증기(자기 인증 아님): {me['path']} {me['sha256'][:12]}")
    print("RUN_RECEIPT_VERIFY " + json.dumps(verdict, ensure_ascii=False))
    return 0 if not failed else 3


if __name__ == "__main__":
    sys.exit(main())
