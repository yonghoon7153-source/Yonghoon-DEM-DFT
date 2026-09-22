"""R17 후속 **3차** 재검토 (대상 `e834b01e` · BMS 수정 `7f09804f`) — NO-GO · P1 1 · P2 2.

리뷰어가 닫혔다고 인정한 것: F2-01~06 의 **구체적 반례** 여섯. 특히 F2-04 는 실제 합성
producer 계산으로 닫힘을 독립 확인했다 (reader rc 0 · row cycle 제거 대조군 rc 2).

받지 못한 것 — 한 줄로: **경로를 아는 것과 그 바이트·존재를 아는 것은 다르다** (F3-01) ·
**한 의미를 두 이름으로 세면 정상 변경이 표현 불가능해진다** (F3-02) · **검사한 것과 소비하는
것이 또 갈라졌다** (F3-03).

| ID | 무엇이 틀렸나 | 자리 |
|---|---|---|
| F3-01 (P1) | GC 의 index↔디스크 대조가 **단방향**이다. `on_disk - known` 과 미등록 파일만 보고, **등록된 파일이 실재하는가**·**그 바이트가 index 가 지목한 것인가**는 안 본다 → ① 경로의 바이트가 바뀌어 있어도 rc 0 으로 삭제 ② 최신 보존 파일이 없어도 rc 0 으로 **유일하게 남은 이전 파일**을 삭제 | `scripts/gc_partial.py:68,98,111,134,188,197` |
| F3-02 (P2) | `starts` 와 `n_multistart` 는 **같은 실행 축의 두 이름**인데, 단일 파일에서는 일치를 강요하고 비교에서는 **독립 축 둘로** 센다 → 정상 producer 의 starts 1/2 비교가 `--axis starts` 로도 `--axis n_multistart` 로도 rc 2 | `scripts/width_report.py:49,197,350` |
| F3-03 (P2) | typed 검사가 `code=null`·`instrument=["not-a-map"]` 을 **찾아 놓고**, 이어서 같은 객체에 `.get`/`.items()` 를 호출한다 → `AttributeError` · rc 1 · `RUN_RECEIPT_VERIFY` 출력 없음. verified=true 수용 반례가 아니라 **구조화 실패 경로**의 문제다 | `scripts/verify_run_receipt.py:144,160,181` |

**한 줄 요약**: 삭제의 근거(F3-01) · 정상 비교의 표현 가능성(F3-02) · 오류 판정의 경계(F3-03).

리뷰어 재현기(`reviews/r17_followup3/codex/repro_followup3.py`)를 이 Linux 에서 **수정 없이**
먼저 돌려 셋이 모두 재현되는 것을 확인했다:

```
--part fast       gc_changed_bytes 0 · gc_missing_retained 0     ← F3-01 (둘 다 rc 2 여야 한다)
                  gc_valid_control 0 · gc_unindexed_control 2      (대조군 정상)
                  receipt_code_null 1 · receipt_instrument_list 1 ← F3-03 (rc 3 여야 한다)
                  receipt_valid_control 0                          (대조군 정상)
--part producer   starts1_single 0 · starts2_single 0
                  starts_axis_compare 2 · n_multistart_axis_compare 2  ← F3-02 (rc 0 이어야 한다)
```

그 관측을 아래 회귀로 고정한다.
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bms_balancing import schema as S          # noqa: E402
from bms_balancing import verify as V          # noqa: E402


def _run(script, *args, cwd=ROOT):
    return subprocess.run([sys.executable, str(ROOT / script), *map(str, args)], cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8", timeout=900)


# ══════════════════════════════════════════════════════════════════════════════════
# F3-01 — 경로를 아는 것과 그 바이트·존재를 아는 것은 다르다
# ══════════════════════════════════════════════════════════════════════════════════

def _two_attempts(out: Path) -> tuple:
    """정상 producer 로 A→B 두 시도를 만든다 (같은 kind·artifact, `--keep 1` 이면 A 가 버려진다)."""
    paths = {}
    for rid, body in (("A", "100-old"), ("B", "100-new")):
        canonical = out / "matrix_100.csv"
        d = V.publish_target(canonical, "partial", run_id=rid)
        d.write_text(body, encoding="utf-8")
        V.record_partial(canonical, d, status="partial", run_id=rid)
        paths[rid] = d
    return paths["A"], paths["B"]


def test_fu3_01_gc_refuses_when_a_doomed_payload_has_other_bytes(tmp_path):
    """★ F3-01 ① — 버릴 항목의 **경로에 다른 바이트**가 들어 있다. index 의 SHA 는 원래 것 그대로다.

    GC 는 경로 집합만 보고 지웠다 — 로그에는 **원래 SHA** 를 인쇄하면서 **다른 바이트**를 지운다
    (리뷰어 실측 rc 0). 동시성 가정이 아니라 **GC 시작 전의 정적 불일치**다.
    `rmtree` 를 버린 것은 옳았지만, 삭제 단위를 파일로 줄이는 것과 **그 파일의 동일성을 검증하는
    것**은 다르다.
    """
    out = tmp_path / "gc"; out.mkdir()
    a, b = _two_attempts(out)
    a.write_text("다른 바이트 — index 의 SHA 와 안 맞는다", encoding="utf-8")
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert a.exists(), ("index 가 지목한 바이트가 아닌 파일을 GC 가 지웠다 (F3-01 ①)",
                        r.returncode, r.stdout[-500:], r.stderr[-500:])
    assert r.returncode == 2, ("SHA 불일치를 보고도 rc 0 이었다 (F3-01 ①)",
                               r.returncode, r.stderr[-500:])


def test_fu3_02_gc_refuses_when_a_retained_payload_is_missing(tmp_path):
    """★ F3-01 ② — **최신 보존 파일 B 가 없다** (index·디렉터리는 그대로). 그런데 GC 는
    유일하게 남은 A 를 지웠다 → payload 0 개, 남은 index 는 **없는 B** 를 가리킨다 (리뷰어 실측).

    "모르면 안 지운다" 는 **모르는 것이 무엇인지**까지 봐야 참이 된다 — 등록된 파일의 부재는
    "모르는 상태" 다."""
    out = tmp_path / "gc"; out.mkdir()
    a, b = _two_attempts(out)
    b.unlink()
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert a.exists(), ("보존 대상이 사라진 상태에서 유일하게 남은 payload 를 지웠다 (F3-01 ②)",
                        r.returncode, r.stdout[-500:], r.stderr[-500:])
    assert r.returncode == 2, ("등록된 보존 파일의 부재를 보고도 rc 0 이었다 (F3-01 ②)",
                               r.returncode, r.stderr[-500:])


def test_fu3_03_gc_refuses_when_a_retained_payload_has_other_bytes(tmp_path):
    """★ F3-01 — ①의 **보존 쪽** 짝. 지울 항목은 멀쩡한데 **보존 항목**의 바이트가 바뀌어 있다.
    리뷰어는 이 조합을 따로 내지 않았지만 같은 계약("삭제·보존 **전체** 항목")의 반대편이다."""
    out = tmp_path / "gc"; out.mkdir()
    a, b = _two_attempts(out)
    b.write_text("보존 쪽 바이트가 바뀌었다", encoding="utf-8")
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert a.exists() and b.exists(), (r.returncode, r.stdout[-500:], r.stderr[-500:])
    assert r.returncode == 2, (r.returncode, r.stderr[-500:])


def test_fu3_04_gc_refuses_before_writing_the_index(tmp_path):
    """★ F3-01 — "**index 포함 쓰기/삭제 0**" 을 따로 고정한다. 거부한 뒤 index 가 줄어 있으면
    다음 GC 가 그 잘린 index 로 판단한다 (리뷰어 실측: 남은 index 가 없는 B 를 가리켰다)."""
    out = tmp_path / "gc"; out.mkdir()
    a, b = _two_attempts(out)
    idx_path = out / "partial" / "index.json"
    before = idx_path.read_text(encoding="utf-8")
    b.unlink()
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert r.returncode == 2, (r.returncode, r.stderr[-400:])
    assert idx_path.read_text(encoding="utf-8") == before, \
        "거부했는데 index 가 바뀌었다 — 쓰기 0 이 아니다 (F3-01)"


def test_fu3_05_gc_still_collects_a_healthy_tree(tmp_path):
    """대조군(양성) — 전부 정상이면 계속 rc 0 이고 A 가 지워져야 한다. F3-01 수정이
    "전부 거부" 로 가면 여기서 잡힌다."""
    out = tmp_path / "gc"; out.mkdir()
    a, b = _two_attempts(out)
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert r.returncode == 0, (r.returncode, r.stdout[-500:], r.stderr[-500:])
    assert not a.exists() and b.exists(), "정상 GC 가 아무것도 안 했다"


def test_fu3_06_gc_still_keeps_the_cross_artifact_control(tmp_path):
    """대조군 — 리뷰어가 두 라운드에 걸쳐 인정한 원 반례(A/100 · A/200 · B/100)는 계속
    rc 0 이고 A/200 이 남아야 한다."""
    out = tmp_path / "gc-cross"; out.mkdir()
    for name, rid, body in [("matrix_100.csv", "A", "100-old"), ("matrix_200.csv", "A", "200-only"),
                            ("matrix_100.csv", "B", "100-new")]:
        canonical = out / name
        d = V.publish_target(canonical, "partial", run_id=rid)
        d.write_text(body, encoding="utf-8")
        V.record_partial(canonical, d, status="partial", run_id=rid)
    survivor = out / "partial" / "matrix" / "A" / "matrix_200.csv"
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert r.returncode == 0, (r.returncode, r.stderr[-400:])
    assert survivor.exists(), "A/200 이 사라졌다 — 앞선 라운드의 수정이 되돌아갔다"


def test_fu3_07_gc_dry_run_also_refuses_a_mismatch(tmp_path):
    """★ F3-01 — dry-run 도 **거부**해야 한다. "지우지 않으니 괜찮다" 가 아니라, dry-run 의
    출력은 *무엇을 지울지*의 예고이고 그 예고가 틀린 바이트를 가리키면 사람이 그것을 믿는다."""
    out = tmp_path / "gc"; out.mkdir()
    a, b = _two_attempts(out)
    a.write_text("다른 바이트", encoding="utf-8")
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1")      # --apply 없음
    assert r.returncode == 2, (r.returncode, r.stdout[-400:], r.stderr[-400:])


# ══════════════════════════════════════════════════════════════════════════════════
# F3-02 — 한 의미를 두 이름으로 세지 않는다
# ══════════════════════════════════════════════════════════════════════════════════

def _produce(src: Path, wb: Path, out: Path, n_starts: int) -> Path:
    """실제 게시 CLI 로 합성 2사이클 산출을 만든다 (`--starts` 만 바꾼다)."""
    r = _run("scripts/fit_cycles.py", "--data-root", src,
             "--half-cell", src / "data/half_cell/GITT/pristine.xlsx", "--full-cell", wb,
             "--cell", "syn", "--si-source", "Li", "--objective-version", "legacy_matlab",
             "--starts", n_starts, "--seed", 0, "--scale-seed", 0,
             "--widths", "--width-tol", 0.01, "--width-starts", 0, "--width-grid", 0,
             "--run-id", "synthetic-production", "--out", out)
    assert r.returncode == 0, (r.returncode, r.stdout[-1500:], r.stderr[-1500:])
    return out / "cycles_syn_Li.csv"


@pytest.fixture(scope="module")
def starts_pair(tmp_path_factory):
    """`n_starts` 1 ↔ 2 만 다른 두 산출.

    ⚠ **같은 합성 원자료·같은 workbook** 에서 두 번 돌린다. 처음엔 tag 마다 `_synth_root` 를
    따로 만들었는데 그러면 `consumed_inputs` 의 **경로**가 달라져 `guard_same_identity` 가
    먼저 막는다 — 그건 이 시험이 묻는 축이 아니다 (리뷰어도 같은 workbook 으로 두 번 돌렸다).
    fixture 가 축을 하나 더 흔들고 있었던 것이고, 그것을 여기 적어 둔다.
    """
    sys.path.insert(0, str(ROOT / "tests"))
    from test_r6_internal import _synth_root                     # noqa: PLC0415
    from test_cycles import _cycle_workbook                      # noqa: PLC0415
    d = tmp_path_factory.mktemp("starts")
    src = _synth_root(d)
    wb = _cycle_workbook(src, d / "syn.xlsx", n_cycles=2)
    return (_produce(src, wb, d / "n1", 1), _produce(src, wb, d / "n2", 2))


@pytest.mark.parametrize("axis", ["starts", "n_multistart"])
def test_fu3_08_a_real_starts_change_is_comparable(starts_pair, axis):
    """★ F3-02 — **정상 producer 가 만든** starts 1/2 두 벌은 비교 가능해야 한다. 지금은
    `--axis starts` 면 `n_multistart` 가, `--axis n_multistart` 면 `starts` 가 남아 **둘 다 rc 2** 다.

    두 이름은 같은 실행 축이다 (`fit_cycles.py` 가 `--starts` 하나를 받아 sidecar 에 `starts` 와
    `n_multistart` 로 두 번 적는다). 단일 파일 안의 일치 요구(F2-02)는 옳지만, 비교에서 **독립
    축 둘로 세면** 정상 변경이 표현 불가능해진다.
    """
    a, b = starts_pair
    r = _run("scripts/width_report.py", a, b, "--axis", axis)
    assert r.returncode == 0, (f"정상 starts 비교가 `--axis {axis}` 로 거부됐다 (F3-02)",
                               r.returncode, r.stdout[-800:], r.stderr[-800:])


def test_fu3_09_each_starts_file_alone_is_still_accepted(starts_pair):
    """대조군(양성) — 두 파일 각각은 계속 rc 0 이다 (리뷰어도 그렇게 관측했다)."""
    for p in starts_pair:
        r = _run("scripts/width_report.py", p)
        assert r.returncode == 0, (r.returncode, r.stdout[-500:], r.stderr[-500:])


def test_fu3_10_a_broken_alias_inside_one_file_is_still_rejected(starts_pair, tmp_path):
    """대조군(음성) — **단일 파일 안의** `starts != n_multistart` 는 계속 거부 (F2-02 가 세운 축).
    비교를 열면서 이것까지 열리면 안 된다."""
    a, _ = starts_pair
    d = tmp_path / "alias"; d.mkdir()
    art = d / a.name
    art.write_bytes(a.read_bytes())
    meta = json.loads(a.with_name(a.name + ".meta.json").read_text(encoding="utf-8"))
    meta["starts"] = int(meta["n_multistart"]) + 5
    art.with_name(art.name + ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, (r.returncode, r.stdout[-600:])


def test_fu3_11_a_row_n_starts_mismatch_is_still_rejected(starts_pair, tmp_path):
    """대조군(음성) — 행의 `n_starts` 가 sidecar 와 어긋나면 계속 거부 (F2-02)."""
    a, _ = starts_pair
    d = tmp_path / "row"; d.mkdir()
    art = d / a.name
    rows = list(csv.DictReader(a.open(encoding="utf-8", newline="")))
    for row in rows:
        row["n_starts"] = "999"
    with art.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(S.CYCLES_ROW), lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    meta = json.loads(a.with_name(a.name + ".meta.json").read_text(encoding="utf-8"))
    meta["sha256"] = hashlib.sha256(art.read_bytes()).hexdigest()
    art.with_name(art.name + ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, (r.returncode, r.stdout[-600:])


def test_fu3_12_a_second_changed_setting_still_blocks_the_comparison(starts_pair, tmp_path):
    """대조군(음성) — starts 말고 **seed 까지** 바뀌면 계속 거부. 별칭을 한 축으로 묶으면서
    "아무 검사나 빼서 양성만 여는" 것이 아닌지 (리뷰어의 금지 조건)."""
    a, b = starts_pair
    d = tmp_path / "twoaxis"; d.mkdir()
    art = d / b.name
    art.write_bytes(b.read_bytes())
    meta = json.loads(b.with_name(b.name + ".meta.json").read_text(encoding="utf-8"))
    meta["seed"] = int(meta["seed"]) + 7
    art.with_name(art.name + ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    r = _run("scripts/width_report.py", a, art, "--axis", "starts")
    assert r.returncode == 2, (r.returncode, r.stdout[-600:], r.stderr[-600:])


def test_fu3_13_an_unchanged_starts_axis_is_still_rejected(starts_pair, tmp_path):
    """대조군(음성) — 고른 축이 **안 움직였으면** 그 비교는 그 축의 것이 아니다. 별칭 정규화가
    이 검사를 지우지 않았는지 (`--axis starts` 인데 두 파일의 starts 가 같은 경우)."""
    a, _ = starts_pair
    d = tmp_path / "same"; d.mkdir()
    art = d / a.name
    art.write_bytes(a.read_bytes())
    art.with_name(art.name + ".meta.json").write_bytes(
        a.with_name(a.name + ".meta.json").read_bytes())
    r = _run("scripts/width_report.py", a, art, "--axis", "starts")
    assert r.returncode == 2, (r.returncode, r.stdout[-600:], r.stderr[-600:])


# ══════════════════════════════════════════════════════════════════════════════════
# F3-03 — 검사한 것과 소비하는 것이 또 갈라졌다
# ══════════════════════════════════════════════════════════════════════════════════

def _receipt(tmp_path: Path, **over) -> Path:
    """실제 생산자가 내는 유효 receipt 를 만들고, 준 필드만 덮은 뒤 공개 checksum 을 **다시**
    계산한다 — 비밀키 위조가 아니라 **입력 schema** 시험이다 (리뷰어와 같은 전제)."""
    sys.path.insert(0, str(ROOT / "reviews"))
    import evidence_gate as gate                                      # noqa: PLC0415
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    tree = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD^{tree}"],
                                   text=True).strip()
    blob = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", f"{head}:./scripts/verify_run_receipt.py"],
        text=True).strip()
    r = gate.run_receipt(head=head, tree=tree,
                         instrument={"scripts/verify_run_receipt.py": blob},
                         package_digest="a" * 64, materialized=None,
                         runtime={"python": sys.version.split()[0], "platform": sys.platform})
    r.update(over)
    r["signature"] = gate.receipt_signature(r)
    p = tmp_path / "receipt.json"
    p.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


@pytest.mark.parametrize("name,over", [
    ("code_null", {"code": None}),
    ("code_list", {"code": ["not", "a", "map"]}),
    ("instrument_list", {"instrument": ["not-a-map"]}),
    ("instrument_null", {"instrument": None}),
], ids=lambda v: v if isinstance(v, str) else "")
def test_fu3_14_a_structurally_invalid_receipt_fails_in_a_structured_way(tmp_path, name, over):
    """★ F3-03 — typed 검사는 `code=null`·`instrument=["not-a-map"]` 을 **찾아 놓고**, 이어서
    같은 객체에 `r["code"].get(...)` · `instrument.items()` 를 호출한다 → `AttributeError` ·
    **rc 1** · `RUN_RECEIPT_VERIFY` 출력 없음 (리뷰어 실측).

    verified=true 로 수용한 반례가 **아니다** — 검증 실패를 **구조화된 판정**으로 내지 못하는
    것이 문제다. traceback 없이 rc 3 과 판정 객체가 나와야 한다.
    """
    p = _receipt(tmp_path, **over)
    r = _run("scripts/verify_run_receipt.py", "--receipt", p, "--target", ROOT)
    both = r.stdout + r.stderr
    assert "Traceback" not in both, (f"{name}: 구조화 실패 대신 예외로 죽었다 (F3-03)", both[-900:])
    assert r.returncode == 3, (f"{name}: 검증 실패 rc 가 3 이 아니다 (F3-03)", r.returncode,
                               both[-600:])
    assert "RUN_RECEIPT_VERIFY " in r.stdout, (f"{name}: 판정 객체가 없다 (F3-03)", r.stdout[-600:])
    verdict = json.loads(r.stdout.split("RUN_RECEIPT_VERIFY ", 1)[1].splitlines()[0])
    assert verdict["verified"] is False, verdict
    assert verdict["checks"].get("complete") is False, verdict["checks"]


def test_fu3_15_an_unperformed_check_is_not_reported_as_success(tmp_path):
    """★ F3-03 — **못 한 검사를 성공으로 채우지 않는다** (리뷰어의 명시 조건). `code` 가
    구조적으로 틀리면 ancestry·tree 는 **수행할 수 없다** — `false` 도 `true` 도 아니고
    "안 함" 이어야 하고, 그 사실이 판정 객체에 보여야 한다."""
    p = _receipt(tmp_path, code=None)
    r = _run("scripts/verify_run_receipt.py", "--receipt", p, "--target", ROOT)
    verdict = json.loads(r.stdout.split("RUN_RECEIPT_VERIFY ", 1)[1].splitlines()[0])
    for k in ("ancestry", "tree"):
        assert verdict["checks"].get(k) is None, (
            f"`code` 가 틀렸는데 {k} 를 수행한 것처럼 적었다", verdict["checks"])
    assert verdict["code_reference_verified"] is False, verdict


def test_fu3_16_a_valid_receipt_is_still_verified(tmp_path):
    """대조군(양성) — 실제 생산자가 내는 유효 receipt 는 계속 rc 0 이어야 한다."""
    p = _receipt(tmp_path)
    r = _run("scripts/verify_run_receipt.py", "--receipt", p, "--target", ROOT)
    assert r.returncode == 0, (r.returncode, r.stdout[-800:])


def test_fu3_17_materialized_none_is_still_legal(tmp_path):
    """대조군(양성) — `materialized=None` 은 생산자가 실제로 내는 합법 상태다 (F2-06 에서
    리뷰어가 명시적으로 유지하라고 한 것)."""
    p = _receipt(tmp_path, materialized=None)
    r = _run("scripts/verify_run_receipt.py", "--receipt", p, "--target", ROOT)
    assert r.returncode == 0, (r.returncode, r.stdout[-800:])


def test_fu3_18_a_wrong_typed_value_still_fails_with_rc3(tmp_path):
    """대조군(음성) — F2-06 이 닫은 축(내부 필드가 뜻 없는 runtime)은 계속 rc 3 이어야 한다.
    구조화 실패 경로를 만들면서 그쪽을 느슨하게 하지 않았는지."""
    p = _receipt(tmp_path, runtime={"irrelevant": True})
    r = _run("scripts/verify_run_receipt.py", "--receipt", p, "--target", ROOT)
    assert r.returncode == 3, (r.returncode, r.stdout[-800:])


# ══════════════════════════════════════════════════════════════════════════════════
# §5 리뷰어의 **별도 권고** 셋 — 독립 결함으로 세지 않은 것들. 결정하고 닫는다.
# ══════════════════════════════════════════════════════════════════════════════════

def test_fu3_19_a_common_receipt_that_already_says_a_cycle_is_refused():
    """★ §5-1 — 리뷰어: *"공통 receipt 의 cycle 키를 금지할지, 파생 과정에서 무시 가능한
    필드로 명시할지 결정하라."* → **금지한다.**

    공통 receipt 는 정의상 cycle 을 말하지 않는다 (그것이 '공통' 의 뜻이다). 거기 cycle 이
    적혀 있으면 생산자와 sidecar 중 하나가 틀린 것이고, 전 판은 그것을 행의 cycle 로 **조용히
    덮어썼다** — 덮어쓰면 틀린 선언이 사라져 아무도 못 본다. 입력 교체 우회는 아니지만
    (리뷰어도 그렇게 세지 않았다) 조용한 정정은 우리 규율이 아니다.
    """
    common = {"half_cell": {"path": "h.xlsx", "sha256": "c" * 64},
              "full_cell": {"path": "f.xlsx", "sha256": "a" * 64, "cycle": 999},
              "literature": {"si": {"path": "s.xlsx", "sha256": "e" * 64}}}
    with pytest.raises(ValueError, match="cycle"):
        S.per_cycle_receipt(common, 0)


def test_fu3_20_a_cycle_free_common_receipt_still_derives():
    """대조군(양성) — cycle 이 없는 정상 공통 receipt 는 계속 파생된다."""
    common = {"half_cell": {"path": "h.xlsx", "sha256": "c" * 64},
              "full_cell": {"path": "f.xlsx", "sha256": "a" * 64},
              "literature": {"si": {"path": "s.xlsx", "sha256": "e" * 64}}}
    assert S.per_cycle_receipt(common, 3)["full_cell"]["cycle"] == 3


def test_fu3_21_a_tree_oid_is_not_accepted_as_an_instrument_blob(tmp_path):
    """★ §5-2 — 리뷰어: *"파일 전용인지 tree 도 허용하는지 계약을 맞출 것."* → **파일 blob 전용.**

    `git rev-parse <commit>:./<rel>` 은 그 자리 객체의 OID 를 주므로 **디렉터리**를 적으면
    tree OID 가 나오고, 전 판은 그것도 `ok` 로 받았다 (리뷰어 실측 rc 0). 무결성 우회는
    아니지만 문서는 blob 이라고 적고 있었다 — 도구는 파일이므로 계약을 문서 쪽에 맞춘다.
    """
    sys.path.insert(0, str(ROOT / "reviews"))
    import evidence_gate as gate                                      # noqa: PLC0415
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    tree = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD^{tree}"],
                                   text=True).strip()
    dir_oid = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", f"{head}:./bms_balancing"], text=True).strip()
    r = gate.run_receipt(head=head, tree=tree, instrument={"bms_balancing": dir_oid},
                         package_digest="a" * 64, materialized=None,
                         runtime={"python": sys.version.split()[0], "platform": sys.platform})
    p = tmp_path / "receipt.json"
    p.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    out = _run("scripts/verify_run_receipt.py", "--receipt", p, "--target", ROOT)
    assert out.returncode == 3, ("디렉터리의 tree OID 가 instrument blob 으로 통과했다 (§5-2)",
                                 out.returncode, out.stdout[-700:])


def test_fu3_22_an_out_of_box_solver_return_is_not_used_as_a_witness():
    """★ §5-3 — 리뷰어: 명시적 solver 반환 주입에서 `_in_box` 가 **최종 SLSQP `r.x`** 에 적용되지
    않아 참 상자 범위 ±16.6667 %p 대신 −733.3333 %p 가 나왔다.

    리뷰어가 분명히 한정한 대로 **실제 SciPy 가 그 값을 만들었다는 native 반례가 아니다** —
    의존 solver 의 비정상 반환까지 방어한다는 계약을 유지하려면 같은 술어를 거기에도 걸어야
    한다는 뜻이고, 그래서 걸었다. "모든 후보에 같은 술어" 는 solver 가 돌려준 점도 후보라는 뜻이다.
    """
    from unittest.mock import patch                                   # noqa: PLC0415

    import numpy as np                                                # noqa: PLC0415
    from bms_balancing import model                                   # noqa: PLC0415

    lo = np.asarray(model.LB5, float)
    hi = np.asarray(model.UB5, float)
    bp = (lo + hi) / 2.0
    far = np.array([25.0, 0.0, 3.0, 0.0, 0.1])                        # 리뷰어가 주입한 그 점
    assert np.any(far > hi) or np.any(far < lo), "주입점이 상자 안이면 이 시험은 뜻이 없다"

    real = V.minimize

    def _inject(fun, x0, **kw):
        r = real(fun, x0, **kw)
        if kw.get("method") == "SLSQP":
            r.x = far.copy()                                          # solver 가 상자 밖을 돌려준다
        return r

    with patch.object(V, "minimize", _inject):
        ext = V.near_optimal_extrema(lambda p: 1.0, bp, 1.0, 1.0, bp.copy(), 1.0, tol=0.01,
                                     seeds=[], n_starts=0, seed=0, lb=model.LB5, ub=model.UB5)
    assert ext["LAM_PE"]["min"] > -100.0, (
        "상자 밖 solver 반환이 폭의 끝점이 됐다 (§5-3)", ext["LAM_PE"])
