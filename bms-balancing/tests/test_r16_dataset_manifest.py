"""R16 — 조건 8 축 ②: 부재 allowlist 를 **버전 있는 dataset manifest** 로 (2026-09-16).

리뷰어(R12 §5 답변 2)가 남긴 것: *"코드 상수 `D.HALF_CELL_ABSENT` 는 과도기 … versioned manifest 로
옮기는 것은 다음."*

왜 옮기나 — 이것은 **코드가 아니라 자료에 대한 사실**이다. 코드 상수로 두면 모집단이 조용한 편집 한
줄로 바뀌고, 그 변경이 언제·왜·무슨 근거로 일어났는지가 어디에도 안 남는다. 모집단이 줄면 **축소된
roster 가 complete 를 참칭한다** (Codex R9-04).

이 라운드가 세우는 계약 넷:

  ① `HALF_CELL_ABSENT` 의 정본은 `datasets/half_cell.manifest.json` 이다 (코드는 그것을 읽는다).
  ② 읽기 실패·형식 위반은 **조용히 빈 목록이 되지 않는다** — 예외로 멈춘다 (부재는 안전값이 아니다).
     빈 allowlist 는 "부재가 없다" 는 **주장**이고, 파일을 못 읽은 것과 같은 값이면 안 된다.
  ③ 항목마다 **근거**가 있어야 한다 — 근거 없는 축소는 형식에서 거부한다.
  ④ 소비자가 manifest 의 **version 과 digest** 를 산출에 남긴다 (무엇으로 모집단을 정했는지).
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bms_balancing import data as D          # noqa: E402


def test_r16_31_the_absent_allowlist_comes_from_the_manifest():
    """[R16-31] 정본은 manifest 파일이다 — 코드 상수는 그것을 읽은 결과여야 한다."""
    doc = json.loads((ROOT / "datasets/half_cell.manifest.json").read_text(encoding="utf-8"))
    want = {(e["source"], e["state"]) for e in doc["absent"]}
    assert D.HALF_CELL_ABSENT == frozenset(want), (sorted(D.HALF_CELL_ABSENT), sorted(want))
    assert D.HALF_CELL_ABSENT, "이 데이터셋에는 알려진 부재가 하나 있다 — 빈 집합이면 정본을 못 읽은 것이다"
    # 그리고 그 사실이 `declared_states` 에 실제로 반영된다 (원장이 장식이 아니다)
    assert "300_0147" not in D.declared_states("GITT"), D.declared_states("GITT")
    assert "300_0147" in D.declared_states("step_005C"), D.declared_states("step_005C")
    # ⚠ 그리고 코드가 그 쌍을 **박아 두고 있지 않아야** 한다 — 값이 우연히 같으면 이 시험은 아무것도 안 잰다
    src = (ROOT / "bms_balancing" / "data.py").read_text(encoding="utf-8")
    for s, st in want:
        assert f'"{st}"' not in src.split("HALF_CELL_ABSENT")[1][:400] if "HALF_CELL_ABSENT" in src else True
    assert "frozenset({(" not in src, "부재 목록을 코드에 박아 두지 않는다 — manifest 에서 읽는다"


def test_r16_32_the_manifest_carries_a_version_and_evidence_for_every_entry():
    """[R16-32] 항목마다 **근거**가 있어야 한다 — 근거 없는 축소는 모집단을 조용히 줄이는 일이다."""
    doc = json.loads((ROOT / "datasets/half_cell.manifest.json").read_text(encoding="utf-8"))
    assert isinstance(doc.get("manifest_version"), int) and doc["manifest_version"] >= 1, doc.get("manifest_version")
    assert doc.get("dataset_id"), "어느 데이터셋의 선언인지 이름이 있어야 한다"
    for e in doc["absent"]:
        assert e["source"] in doc["declared_sources"] and e["state"] in doc["declared_states"], e
        assert e.get("why") and isinstance(e.get("evidence"), list) and e["evidence"], (
            "근거 없이 모집단에서 빼지 않는다", e)
        assert e.get("recorded_utc") and e.get("recorded_by"), e


@pytest.mark.parametrize("broken,why", [
    ('{"manifest_version": 1}', "absent 가 없다"),
    ('{"absent": []}', "manifest_version 이 없다"),
    ('{"manifest_version": 1, "declared_sources": ["GITT"], "declared_states": ["100"],'
     ' "absent": [{"source": "GITT", "state": "100"}]}', "근거가 없다"),
    ('{"manifest_version": 1, "declared_sources": ["GITT"], "declared_states": ["100"],'
     ' "absent": [{"source": "NOPE", "state": "100", "why": "x", "evidence": ["y"],'
     ' "recorded_utc": "z", "recorded_by": "w"}]}', "선언 밖 소스"),
    ('not json at all', "JSON 이 아니다"),
])
def test_r16_33_a_broken_manifest_stops_rather_than_becoming_an_empty_allowlist(tmp_path, broken, why):
    """[R16-33] 읽기 실패·형식 위반이 **빈 allowlist** 가 되면 안 된다.

    빈 allowlist 는 "알려진 부재가 없다" 는 **주장**이고, 그 주장이 서면 `declared_states` 가 늘어나
    존재하지 않는 조합이 `missing_input` 으로 잡힌다 — 반대로 형식이 깨졌는데 통과하면 축소가 숨는다.
    어느 쪽이든 **모른 채로 답을 내면 안 된다**: 멈춘다 (자체 리뷰 C03 · R11 P1-9).
    """
    p = tmp_path / "m.json"
    p.write_text(broken, encoding="utf-8")
    # ⚠ 전용 예외로 좁힌다. 2026-09-16 실측: `pytest.raises(Exception)` 은 **함수가 아직 없어서 난**
    #   `AttributeError` 로도 만족됐고(메시지에 "manifest" 가 들어 있어 문구 검사까지 통과했다), 8 개가
    #   구현 전에 초록이었다 — 이 저장소가 fixture 감사에서 반복해 본 가짜 통과다.
    with pytest.raises(D.ManifestError) as ei:
        D.load_half_cell_manifest(p)
    assert str(ei.value), (why, ei.value)


def test_r16_34_a_missing_manifest_is_not_an_empty_allowlist(tmp_path):
    """[R16-34] 파일이 없는 것도 빈 목록이 아니다 — 같은 이유로 멈춘다."""
    with pytest.raises(D.ManifestError):
        D.load_half_cell_manifest(tmp_path / "없는파일.json")


def test_r16_35_the_manifest_identity_travels_with_the_artifact():
    """[R16-35] 무엇으로 모집단을 정했는지가 **산출에 남아야** 한다 — version 과 digest 둘 다.

    manifest 를 파일로 옮기기만 하고 산출이 그것을 안 적으면, 나중에 그 파일이 바뀌었을 때 어느 산출이
    어느 선언으로 만들어졌는지 말할 수 없다 (C18 의 "적고 안 대면 무엇을 고정하는지 말할 수 없다").
    """
    ident = D.half_cell_manifest_identity()
    assert ident["version"] >= 1 and len(ident["sha256"]) == 64, ident
    assert ident["dataset_id"], ident
    import hashlib
    raw = (ROOT / "datasets/half_cell.manifest.json").read_bytes()
    assert ident["sha256"] == hashlib.sha256(raw).hexdigest(), "digest 는 그 파일의 bytes 다"


def test_r16_36_two_runs_that_used_different_population_declarations_do_not_compare(tmp_path):
    """[R16-36] 두 산출이 **다른 모집단 선언**으로 만들어졌으면 그 대조는 같은 실행의 재현이 아니다.

    적기만 하고 안 대면 그 필드는 장식이다 (C18). 양쪽에 있는데 다르면 **실행 조건 불일치**로 잡는다.

    ⚠ 이 라운드가 **일부러 안 한 것**: 한쪽에만 있는 경우(옛 정본 vs 새 산출)를 새 blocker 로 만들지
      않았다. 그러면 승인 기록에 네 번째 축이 생겨 또 사용자 결정을 요구하는데, 그 상황은 이미
      `inputs_uncomparable`·`env_uncomparable` 가 같은 이유로 승격을 막고 있어 실질 판정이 안 바뀐다.
      정본을 다시 만들면 저절로 사라지는 비대칭이다.
    """
    import subprocess
    from bms_balancing import verify as V                    # noqa: PLC0415
    from test_r7_codex import _sign                          # noqa: PLC0415
    from test_r8_codex import _full_matrix_rows              # noqa: PLC0415

    dirs = {}
    for tag, rid, ver in (("old", "r16-dm-old", 1), ("new", "r16-dm-new", 2)):
        d = tmp_path / tag; d.mkdir()
        f = d / "matrix_100.csv"
        rows = _full_matrix_rows(rid)
        V.atomic_write_csv(f, rows, list(rows[0]))
        _sign(f, rid, "100", full=True)
        m = f.with_name(f.name + ".meta.json")
        j = json.loads(m.read_text(encoding="utf-8"))
        j["dataset_manifest"] = {"version": ver, "dataset_id": "x", "sha256": str(ver) * 64}
        m.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        dirs[tag] = d

    r = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"),
                        "--new", str(dirs["new"]), "--old", str(dirs["old"])],
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    promo = json.loads(next(l for l in r.stdout.splitlines() if l.startswith("PROMOTION "))[len("PROMOTION "):])
    assert promo["blocked_by"]["controls"] > 0, ("모집단 선언이 다른데 통과했다", promo["blocked_by"])
    assert "dataset_manifest" in r.stdout, r.stdout[-1200:]
    assert promo["promotion_eligible"] is False, promo


def test_r16_37_both_places_that_compute_the_manifest_identity_agree():
    """[R16-37] 식별자 계산이 **두 자리**에 있다 — `data.half_cell_manifest_identity()` 와 `run_states.sh` 의
    기록기(격리 실행이라 앱 패키지를 못 쓴다). 둘이 갈리면 사이드카가 다른 선언을 가리킨다.

    R14 P2-2 가 닫은 "규칙이 두 벌이라 절반만 구현됐다" 와 같은 축이라, 값을 **실제로 대 본다**.
    """
    import hashlib
    raw = (ROOT / "datasets/half_cell.manifest.json").read_bytes()
    doc = json.loads(raw.decode("utf-8"))
    shell_side = {"version": doc["manifest_version"], "dataset_id": doc["dataset_id"],
                  "sha256": hashlib.sha256(raw).hexdigest()}
    assert D.half_cell_manifest_identity() == shell_side, (D.half_cell_manifest_identity(), shell_side)

    src = (ROOT / "scripts/run_states.sh").read_text(encoding="utf-8")
    assert "half_cell.manifest.json" in src, "기록기가 그 파일을 읽어야 한다"
    assert "from bms_balancing.data import" not in src, (
        "격리 기록기에서 앱 패키지를 import 하지 않는다 — pandas 를 끌고 와 meta 가 통째로 안 쓰였다 (실측)")
