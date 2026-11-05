"""REIL C4-0a 시작 identity 대조 (60 s) — 기존 `reil_c5_pilot.env_identity` 에 새 봉인 경로를 명시 인자로 넘기고 전체 MANIFEST sha 를 따로 대조한다.

계산 없음 (lock 재측정 = 설치 파일 읽기 · 해시 · PROFILE = 판 · 빌드 메타데이터 · COBYQA 옵션 · 구현 파일 해시). 전체 C6 check 는 부르지 않는다
(C4-ENV 의 check 1 회가 인정됨 · 상태 문서 §38).
    <venv>/bin/python -I identity_c4.py <venv> <seal> <manifest_sha256> <out_json>
"""
import hashlib
import json
import sys
from pathlib import Path

BMS = Path("/home/user/Yonghoon-DEM-DFT/bms-balancing")
sys.path.insert(0, str(BMS))
from scripts import reil_c5_pilot as c5  # noqa: E402

venv, seal, want, out = sys.argv[1], Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
if out.exists():
    raise SystemExit(f"{out} 가 이미 있다")
r = c5.env_identity(venv=venv, sealed=seal)
got = hashlib.sha256((seal / "MANIFEST.json").read_bytes()).hexdigest()
if got != want:
    r["problems"].append(f"MANIFEST sha256 {got} ≠ 명시 {want}")
    r["ok"] = False
r["seal_path"] = str(seal)
r["manifest_sha256_expected"] = want
r["manifest_sha256_actual"] = got
r["full_c6_check"] = "NOT_RUN — C4-ENV check 1 회로 인정 (상태 문서 §38)"
out.write_text(json.dumps(r, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n", encoding="utf-8")
print(json.dumps({"ok": r["ok"], "problems": r["problems"]}, ensure_ascii=False))
sys.exit(0 if r["ok"] else 3)
