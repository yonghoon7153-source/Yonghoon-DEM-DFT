"""R16 — `openpyxl` 을 환경 축에 넣는다 (R13 §7 · R14 §5 의 열린 항목, 2026-09-16).

리뷰어 정적 지적: 과학 입력이 전부 `pd.read_excel` 로 읽히고 pandas 는 **openpyxl 로** xlsx 를 연다.
그런데 `env_signature()` 도 `ENV_KEYS` 도 openpyxl 을 안 적는다. 같은 pandas 에서 openpyxl 만 바뀌어도
입력 파싱이 달라질 수 있으므로, 자체 리뷰 C18 이 pandas 를 넣은 것과 **같은 논거**다 —
"적고 안 대면 그 서명은 무엇을 고정하는지 말할 수 없다."

왜 별도 라운드인가 (R14 §5 가 그렇게 적었다): 축 하나를 더하면 **이미 게시된 정본이 계약 위반이 된다.**
2026-09-16 실측 — `ENV_KEYS` 에 openpyxl 을 그냥 넣자 `check_u14 --new out --schema-only` 가
**rc 0 → rc 2** 로 바뀌고 정본 13 개가 전부 "새 스키마 누락" 이 됐다. 그 묶음은 사용자 기계의 실데이터
재실행으로 승격한 것(`37a889b`)이라 다시 만들 수 없다.

U18-03 이 같은 모양을 이미 닫았다 — **"정본의 나이는 새 산출의 위반이 아니다."** 그것을 env 축에 적용한다:

| 사이드카의 env | 판정 |
|---|---|
| 여섯 축이 다 있다 | 정상 |
| v1 다섯은 다 있고 **openpyxl 키 자체가 없다** | **나이** — soft(`env_contract_legacy`), 승격은 계속 불가 |
| openpyxl 키가 **있는데 비어 있다** | **위반** — 선언해 놓고 값이 없는 것은 R11 P1-9 의 바로 그 패턴 |
| v1 축이 하나라도 없다/비었다 | **위반** (그대로) |

즉 **부재는 안전값이 아니다** 를 지키되, "그 축이 존재하지 않던 시절" 과 "있는데 안 채웠다" 를 가른다.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests"))
from bms_balancing import schema as S          # noqa: E402

V1 = {"python": "3.12.3", "numpy": "2.5.3", "scipy": "1.18.1", "pandas": "3.0.5", "platform": "Linux-x"}


def _prov():
    import importlib.util
    spec = importlib.util.spec_from_file_location("_prov16", ROOT / "scripts/provenance.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


# ── R16-1 ────────────────────────────────────────────────────────────────
def test_r16_01_openpyxl_is_recorded_and_compared():
    """[R16-1] 서명이 적는 것과 비교 축이 **같아야** 한다 (C18). openpyxl 이 둘 다에 있어야 한다."""
    env = _prov().env_signature()
    assert set(env) == set(S.ENV_KEYS), ("서명과 ENV_KEYS 가 갈렸다", sorted(env), sorted(S.ENV_KEYS))
    assert "openpyxl" in S.ENV_KEYS, S.ENV_KEYS
    assert str(env.get("openpyxl") or "").strip(), ("이 기계에는 openpyxl 이 깔려 있다 — 값이 나와야 한다", env)


# ── R16-2 ────────────────────────────────────────────────────────────────
def test_r16_02_an_older_sidecar_is_aged_not_broken():
    """[R16-2] v1 다섯만 적은 사이드카는 **위반이 아니다** — 그 축이 없던 시절에 쓰인 것이다 (U18-03 의 논리).

    `env_axes_missing` 은 계약 위반만 센다. 나이는 `env_axes_legacy` 가 따로 센다 — 둘을 한 통에 넣으면
    "옛 정본이 깨졌다" 와 "새 산출이 축을 뺐다" 를 구별할 수 없다.
    """
    # 계약 자체는 **엄격**하다 — 빠지면 빠진 것이다. 봐주는 것은 원장이지 이 함수가 아니다.
    assert S.env_axes_missing(dict(V1)) == ["openpyxl"], S.env_axes_missing(dict(V1))
    assert S.env_axes_added_only(["openpyxl"]) is True
    assert S.env_axes_added_only(["pandas"]) is False, "v1 축이 빠진 것은 어떤 기록도 덮지 못한다"
    assert S.env_axes_added_only(["openpyxl", "pandas"]) is False
    assert S.env_axes_added_only([]) is False

    full = dict(V1, openpyxl="3.1.5")
    assert S.env_axes_missing(full) == [], (full,)


# ── R16-3 ────────────────────────────────────────────────────────────────
def test_r16_03_declared_but_blank_is_a_violation_not_age():
    """[R16-3] **선언해 놓고 비운 것**은 나이가 아니라 위반이다 — R11 P1-9 "신고된 위험은 값으로 소비한다".

    이 줄이 없으면 축을 `""` 로 적는 것이 축을 지우는 것보다 싸진다 (게이트가 침묵에 보상하는 자체 리뷰
    C03 의 그 모양). 공백문자·NBSP 도 값이 아니다.
    """
    for blank in ("", "   ", "\t\n", " "):
        e = dict(V1, openpyxl=blank)
        assert S.env_axes_missing(e) == ["openpyxl"], (blank, S.env_axes_missing(e))
    # v1 축이 빠진 것은 openpyxl 유무와 무관하게 계속 위반이다
    no_pandas = {k: v for k, v in V1.items() if k != "pandas"}
    assert "pandas" in S.env_axes_missing(no_pandas)


# ── R16-4 ────────────────────────────────────────────────────────────────
def test_r16_04_the_message_does_not_hardcode_the_axis_count():
    """[R16-4] 오류 문구가 "환경 축 **다섯**" 으로 개수를 박아 두고 있었다 — 축을 더하면 문구가 거짓이 된다.

    `test_cy_01` 이 5 개 튜플을 박아 뒀던 것과 같은 자리다. 개수는 `ENV_KEYS` 에서 읽는다.
    """
    src = (ROOT / "scripts/check_u14.py").read_text(encoding="utf-8")
    assert "환경 축 다섯" not in src, "개수를 문구에 박지 않는다 — ENV_KEYS 에서 읽는다"
    body = (ROOT / "bms_balancing" / "schema.py").read_text(encoding="utf-8")
    assert "다섯 축" not in body, "schema 쪽 문구도 같다"


# ── R16-5 ────────────────────────────────────────────────────────────────
def test_r16_05_the_promoted_canonical_bundle_still_passes_schema_only():
    """[R16-5] **이 라운드가 지켜야 하는 것** — 이미 승격한 정본(`out/`, `37a889b`)이 계속 rc 0 이어야 한다.

    그 13 산출은 사용자 기계의 실데이터 재실행으로 만든 것이고 다시 만들 수 없다. 축을 더하면서 그것을
    깨면 이 라운드는 하네스 항목 하나를 닫는 대신 **과학 산출을 무효로 만든다.**
    """
    out = ROOT / "out"
    metas = sorted(out.glob("*.meta.json"))
    assert metas, "정본 사이드카가 있어야 이 시험이 뜻을 가진다"
    envs = [json.loads(p.read_text(encoding="utf-8")).get("env") for p in metas]
    assert all(isinstance(e, dict) and "openpyxl" not in e for e in envs), \
        "이 시험의 전제 — 정본은 openpyxl 을 안 적은 세대다"

    r = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(out), "--schema-only"],
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, ("정본이 깨졌다", r.returncode, r.stdout[-2500:])
    promo = json.loads(next(l for l in r.stdout.splitlines() if l.startswith("PROMOTION "))[len("PROMOTION "):])
    assert promo["blocked_by"]["schema"] == 0, promo["blocked_by"]
    assert promo["blocked_by"].get("env_contract_legacy", 0) == len(metas), \
        ("나이는 세되 위반으로 세지 않는다", promo["blocked_by"])


# ── R16-6 ────────────────────────────────────────────────────────────────
def test_r16_06_a_sidecar_that_blanks_the_new_axis_is_still_rejected(tmp_path):
    """[R16-6] 음성 대조군 — 정본과 **같은 자료**인데 openpyxl 을 `""` 로 적으면 rc 2 여야 한다.

    R16-5 가 "봐주는 길" 을 열었으므로, 그 길이 **비우는 것까지** 봐주지 않는다는 것을 같은 경로에서
    관측한다. 이것이 없으면 R16-5 는 통로가 된다.
    """
    import shutil
    d = tmp_path / "out"
    shutil.copytree(ROOT / "out", d, ignore=shutil.ignore_patterns("archive", "recompare", "*.lock"))
    for p in sorted(d.glob("*.meta.json")):
        m = json.loads(p.read_text(encoding="utf-8"))
        m["env"] = dict(m["env"], openpyxl="")
        p.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(d), "--schema-only"],
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    assert r.returncode == 2, (r.returncode, r.stdout[-1500:])
    assert "openpyxl" in r.stdout, r.stdout[-1500:]


# ── R16-7 ────────────────────────────────────────────────────────────────
def test_r16_07_an_unrecorded_aged_bundle_is_a_violation_not_age(tmp_path):
    """[R16-7] **기록에 없는** 옛 세대 묶음은 나이가 아니라 위반이다 — 원장이 **유일한 문**이다.

    처음에는 "축의 이름으로" 면제하려 했다 (openpyxl 이 없으면 나이). 그러면 `test_h02` 가 재는 계약
    ("한 축씩 빼도 전부 걸려야 한다")이 그 축에 대해 **영구히** 약해지고, 누구든 그 축을 지워 통과한다.
    그래서 면제를 `reviews/PROMOTION_DECISIONS.json` 이 **sha256 으로 지목한 산출에만** 걸었다.

    이 시험은 그 문이 닫혀 있는지 본다 — 기록에 없는 bytes 는 아무리 "옛날 모양" 이어도 rc 2 다.
    """
    from bms_balancing import verify as V                  # noqa: PLC0415
    from test_r7_codex import _sign                        # noqa: PLC0415
    from test_r8_codex import _full_matrix_rows            # noqa: PLC0415

    d = tmp_path / "unrecorded"; d.mkdir()
    f = d / "matrix_100.csv"
    rows = _full_matrix_rows("r16-unrecorded")
    V.atomic_write_csv(f, rows, list(rows[0]))
    _sign(f, "r16-unrecorded", "100", full=True)
    m = f.with_name(f.name + ".meta.json")
    j = json.loads(m.read_text(encoding="utf-8"))
    j["env"] = {k: v for k, v in j["env"].items() if k != "openpyxl"}      # 옛 세대 모양
    assert S.env_axes_missing(j["env"]) == ["openpyxl"], j["env"]
    m.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    r = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(d), "--schema-only"],
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    promo = json.loads(next(l for l in r.stdout.splitlines() if l.startswith("PROMOTION "))[len("PROMOTION "):])
    assert r.returncode == 2, ("기록에 없는데 통과했다 — 원장이 유일한 문이어야 한다", r.returncode, r.stdout[-1500:])
    assert promo["blocked_by"]["schema"] > 0 and promo["blocked_by"]["env_contract_legacy"] == 0, promo["blocked_by"]

    # 그리고 면제는 **승격의 문이 아니다** — 버킷이 UNKNOWN_BLOCKERS 안에 있어야 승격이 계속 막힌다
    import importlib.util
    spec = importlib.util.spec_from_file_location("_cu16", ROOT / "scripts/check_u14.py")
    cu = importlib.util.module_from_spec(spec); spec.loader.exec_module(cu)
    assert "env_contract_legacy" in cu.UNKNOWN_BLOCKERS, cu.UNKNOWN_BLOCKERS


# ── R16-8 ────────────────────────────────────────────────────────────────
def test_r16_08_schema_only_never_gets_the_not_promotable_code():
    """[R16-8] `--schema-only` 는 **승격을 묻지 않은** 진단이다 — 거기에 4 를 주면 스키마 점검 도구로 못 쓴다
    (코드가 그 규칙을 주석으로 못박아 뒀다).

    2026-09-16 실측: `env_legacy` 를 `not_promotable` 에 그냥 넣자 `--new out --schema-only` 가 rc 0 → **rc 4**
    가 됐다. R16-5 가 그것을 잡았고, 조건을 "승격 대조를 물었을 때만" 으로 좁혔다. 이 시험은 그 좁힘을 고정한다.
    """
    r = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"),
                        "--new", str(ROOT / "out"), "--schema-only"],
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    promo = json.loads(next(l for l in r.stdout.splitlines() if l.startswith("PROMOTION "))[len("PROMOTION "):])
    assert r.returncode == 0, (r.returncode, r.stdout[-1200:])
    assert promo["blocked_by"]["env_contract_legacy"] > 0, "나이는 **세되** rc 를 바꾸지 않는다"
    assert promo["promotion_eligible"] is False and promo["blocked_by"]["baseline_absent"] == 1, promo
