"""R16 — 조건 8 축 ③: 조각들을 **한 receipt 로 묶고 소비자가 ancestry 를 검증한다** (2026-09-16).

리뷰어(R12 §5 답변 4)가 남긴 것: *"조각은 다 있다 (`expected_head`·`expected_tree`·`instrument`·
`package_digest`·`materialized`) — **한 receipt 로 묶어 서명하고 consumer 가 검증하는 부분이 없다**."*

조각이 흩어져 있으면 무엇이 문제인가: 증거 JSON 의 필드 하나를 고쳐도 아무도 모른다. 묶어서 **서명**
하면 사후 편집이 드러나고, **ancestry** 를 대면 "이 저장소의 역사에 없는 커밋에서 나왔다는 증거" 를
거부할 수 있다.

### 자기참조를 어떻게 끊나 (R12 Q3, 답이 안 왔다 — 우리가 정하고 근거를 적는다)

Q3 은 "(b) 저장소 안의 검사 스크립트를 만들 텐데 그 스크립트 자신의 봉인은 어느 커밋 기준인가" 였다.

**소비자는 자기를 인증하지 않는다 — 선언한다.** 검증기가 "나는 봉인돼 있다" 고 스스로 말하면 그것은
순환이다 (고친 검증기도 같은 말을 한다). 대신 자기 경로와 digest, 그리고 **어느 커밋을 기준으로
검증했는지**를 출력에 적는다. 그 파일이 변조됐는지는 이미 있는 `instrument_sealed` 가 **바깥에서**
본다. 즉 자기참조는 "주장하지 않고 드러내기" 로 끊는다.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _gate():
    import importlib.util
    spec = importlib.util.spec_from_file_location("_gate16", ROOT / "reviews/evidence_gate.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _head():
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def _tree(head):
    return subprocess.run(["git", "rev-parse", f"{head}^{{tree}}"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()


def _receipt(**over):
    g = _gate()
    head = _head()
    # ⚠ R17 후속 P2-02 — 전 판은 `"0"*64` 였다. 실제 `gate.instrument_digests()` 는 **40자리 git
    #   blob** 을 돌려주고 소비자도 그것과 견준다 (이 시험은 `--skip-instrument` 라 대조를 건너뛰어
    #   64자리 자리표시가 드러나지 않았다). typed 완전성 검사를 넣자 fixture 가 먼저 깨졌다.
    base = dict(head=head, tree=_tree(head), instrument={"reviews/evidence_gate.py": "0" * 40},
                package_digest="1" * 64, materialized={"mode": "sparse detached worktree"},
                runtime={"python": "3.12.3"})
    base.update(over)
    return g, g.run_receipt(**base)


def test_r16_61_the_pieces_are_bound_into_one_signed_object():
    """[R16-61] 조각이 **한 객체**로 묶이고 서명이 그 전부를 덮는다 — 한 글자만 고쳐도 서명이 어긋난다."""
    g, r = _receipt()
    for k in ("receipt_version", "code", "instrument", "package", "runtime", "produced_utc", "signature"):
        assert k in r, (k, sorted(r))
    assert r["code"]["commit"] == _head() and len(r["signature"]) == 64, r["code"]

    assert g.receipt_signature(r) == r["signature"], "자기 서명과 안 맞는다"
    edited = json.loads(json.dumps(r))
    edited["package"]["digest"] = "9" * 64
    assert g.receipt_signature(edited) != edited["signature"], "필드를 고쳤는데 서명이 그대로다"
    # 서명 자체를 갈아 끼워도 계산값과 달라진다 (서명은 내용에서 나온다)
    forged = json.loads(json.dumps(edited))
    forged["signature"] = g.receipt_signature({**edited, "signature": ""})
    assert forged["signature"] != r["signature"], forged["signature"]


def _verify(receipt_path, *args):
    return subprocess.run([sys.executable, str(ROOT / "scripts/verify_run_receipt.py"),
                           "--receipt", str(receipt_path), "--target", str(ROOT), *args],
                          cwd=ROOT, capture_output=True, text=True, timeout=300)


def test_r16_62_a_receipt_from_this_history_verifies(tmp_path):
    """[R16-62] 이 저장소의 역사에서 나온 receipt 는 통과한다 (양성 대조군).

    ⚠ 이것이 없으면 아래 음성 시험들은 "무엇이든 거부한다" 와 구별되지 않는다.
    """
    g, r = _receipt()
    p = tmp_path / "r.json"; p.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    out = _verify(p, "--skip-instrument")
    assert out.returncode == 0, (out.returncode, out.stdout, out.stderr)
    assert "ancestry" in out.stdout or "조상" in out.stdout, out.stdout


def test_r16_63_an_edited_receipt_is_rejected(tmp_path):
    """[R16-63] 사후 편집은 **서명**에서 걸린다 — 묶어서 서명한 이유가 이것이다."""
    g, r = _receipt()
    r["package"]["digest"] = "9" * 64                     # 서명은 그대로 둔다
    p = tmp_path / "r.json"; p.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    out = _verify(p, "--skip-instrument")
    assert out.returncode == 3, (out.returncode, out.stdout, out.stderr)
    assert "서명" in (out.stdout + out.stderr), (out.stdout, out.stderr)


def test_r16_64_a_commit_outside_this_history_is_rejected(tmp_path):
    """[R16-64] **ancestry** — 이 저장소의 역사에 없는 커밋에서 나왔다는 증거는 거부한다.

    서명만 보면 "잘 만든 거짓말" 을 못 막는다. 서명은 **내용이 안 바뀌었다**만 말하고, 그 내용이 이
    저장소와 관계있다는 것은 말하지 않는다. 그래서 둘 다 본다.
    """
    g, r = _receipt(head="0" * 40, tree="0" * 40)
    p = tmp_path / "r.json"; p.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    out = _verify(p, "--skip-instrument")
    assert out.returncode == 3, (out.returncode, out.stdout, out.stderr)
    assert "ancestry" in (out.stdout + out.stderr) or "조상" in (out.stdout + out.stderr), (out.stdout, out.stderr)


def test_r16_65_a_wrong_tree_for_a_real_commit_is_rejected(tmp_path):
    """[R16-65] 커밋은 진짜인데 tree 가 그 커밋의 것이 아니면 거부한다 — 둘의 짝이 맞아야 한다."""
    g, r = _receipt(tree="1" * 40)
    p = tmp_path / "r.json"; p.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    out = _verify(p, "--skip-instrument")
    assert out.returncode == 3, (out.returncode, out.stdout, out.stderr)
    assert "tree" in (out.stdout + out.stderr), (out.stdout, out.stderr)


def test_r16_66_the_consumer_declares_itself_instead_of_certifying_itself(tmp_path):
    """[R16-66 · R12 Q3 의 답] 검증기는 **자기를 인증하지 않는다.**

    "나는 봉인돼 있다" 고 스스로 말하면 순환이다 — 고친 검증기도 같은 말을 한다. 대신 자기 경로·digest·
    기준 커밋을 출력에 **드러내고**, 변조 여부는 바깥의 `instrument_sealed` 가 본다.
    """
    g, r = _receipt()
    p = tmp_path / "r.json"; p.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    out = _verify(p, "--skip-instrument")
    assert out.returncode == 0, out.stdout
    j = json.loads(next(l for l in out.stdout.splitlines() if l.startswith("RUN_RECEIPT_VERIFY "))
                   [len("RUN_RECEIPT_VERIFY "):])
    me = j["verifier"]
    assert me["path"].endswith("verify_run_receipt.py") and len(me["sha256"]) == 64, me
    assert me["checked_against"] == _head(), me
    assert "self_sealed" not in me and "trusted" not in me, (
        "검증기가 자기를 인증하면 순환이다 — 드러내기만 한다", me)


def test_r16_67_the_runner_emits_the_bound_receipt():
    """[R16-67] 러너가 실제로 그 receipt 를 낸다 — 함수만 있고 아무도 안 부르면 축이 안 닫힌다."""
    src = (ROOT / "reviews/r11_repros/replay_codex_r11.py").read_text(encoding="utf-8")
    assert "run_receipt" in src, "러너가 receipt 를 안 만든다"


def test_r16_68_the_receipt_carries_digests_not_status_words():
    """[R16-68] receipt 의 `instrument` 는 **digest** 다 — 상태 문자열(`ok`/`다름`)이 아니다.

    2026-09-16 실측으로 잡힌 내 결함: 러너가 `instrument_sealed` 의 **상태 요약**을 receipt 에 실었다.
    소비자는 그것을 blob sha 와 대 보므로 **깨끗한 트리에서도 언제나 "다름"** 이었다. 단위 시험 일곱은
    전부 초록이었다 — fixture 가 digest 를 직접 넣었기 때문이다 (**끝에서 끝까지 돌려야 보인다**).
    """
    g = _gate()
    got = g.instrument_digests(ROOT, ["reviews/evidence_gate.py"])
    assert set(got) == {"reviews/evidence_gate.py"}, got
    v = got["reviews/evidence_gate.py"]
    assert len(v) == 40 and all(c in "0123456789abcdef" for c in v), ("blob sha 여야 한다", v)

    src = (ROOT / "reviews/r11_repros/replay_codex_r11.py").read_text(encoding="utf-8")
    assert "instrument=gate.instrument_digests(" in src, "러너가 상태 대신 digest 를 실어야 한다"
    assert "instrument=seal_detail" not in src, "상태 요약을 receipt 에 싣지 않는다"


def test_r16_69_the_verifier_resolves_paths_relative_to_the_target_not_the_repo_root():
    """[R16-69] 이 저장소는 **모노레포**다 — `<commit>:<rel>` 은 저장소 루트 기준이라 `./` 없이는 못 찾는다.

    같은 날 잡힌 두 번째 결함. gate 의 `instrument_sealed` 는 이미 `HEAD:./{rel}` 을 쓰고 있었는데
    검증기가 그 `./` 를 빠뜨려, 깨끗한 트리에서도 instrument 가 "다름" 이었다 (규칙이 두 벌이면 갈린다).
    """
    src = (ROOT / "scripts/verify_run_receipt.py").read_text(encoding="utf-8")
    assert '{commit}:./{rel}' in src, "target 기준(`./`)으로 풀어야 한다 — 모노레포에서 루트 기준은 못 찾는다"
