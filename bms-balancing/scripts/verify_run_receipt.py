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
            got = _git(a.target, "rev-parse", f"{commit}:{rel}")
            detail[rel] = "ok" if (got.returncode == 0 and got.stdout.strip() == str(want)) else "다름"
        checks["instrument"] = bool(detail) and all(v == "ok" for v in detail.values())
        if not checks["instrument"]:
            failed.append(f"instrument digest 가 그 커밋의 blob 과 다르다: "
                          f"{sorted(k for k, v in detail.items() if v != 'ok')}")

    verdict = {"verified": not failed, "checks": checks, "failed": failed,
               "receipt": str(a.receipt), "receipt_version": r.get("receipt_version"),
               "code": r.get("code"), "skipped_instrument": bool(a.skip_instrument),
               "verifier": me}
    print(f"\n══ run receipt 검증 — {a.receipt.name} ══")
    print(f"  서명 {'ok' if checks['signature'] else '**다름**'} · "
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
