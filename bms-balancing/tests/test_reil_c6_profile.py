"""reil_c6_profile 의 RECORD 불일치 분류 — '설명된 충돌' 만 기록하고 통과, 나머지는 봉인 거부 (fail-closed).

출발점 (2026-10-05 첫 emit): about-time 4.2.1 · alive_progress 3.3.0 의 wheel 이 둘 다 venv 꼭대기 `../../../LICENSE` 를 RECORD 에
적고, 나중에 깔린 쪽이 먼저 깔린 쪽을 덮어써 RECORD 불일치 1 로 멈췄다. 같은 경로를 두 배포판이 주장하면 어떤 설치 순서로도 한쪽은
어긋난다 — 그 경우만 좁게 풀고, 그 밖의 불일치는 지금처럼 멈춘다.
"""
import pytest

from scripts import reil_c6_profile as prof
from scripts.reil_c6_profile import classify_record_mismatches

INDEX = {
    "about-time": {"../../../LICENSE": "sha256=A", "about_time/__init__.py": "sha256=T"},
    "alive-progress": {"../../../LICENSE": "sha256=B"},
    "numpy": {"numpy/__init__.py": "sha256=N"},
    "numpy-shadow-claim": {"numpy/__init__.py": "sha256=X"},
}


def test_explained_collision_outside_site_packages_is_recorded_not_fatal():
    fatal, collisions = classify_record_mismatches([("about-time", "../../../LICENSE", "sha256=A", "sha256=B")], INDEX)
    assert fatal == []
    assert collisions == [{"path": "../../../LICENSE", "dist": "about-time",
                           "claimed_by": ["about-time", "alive-progress"], "disk_matches": "alive-progress"}]


def test_mismatch_inside_site_packages_is_fatal_even_when_another_record_matches_the_disk():
    m = ("numpy", "numpy/__init__.py", "sha256=N", "sha256=X")
    fatal, collisions = classify_record_mismatches([m], INDEX)
    assert fatal == [m] and collisions == []


def test_outside_mismatch_without_another_claimant_is_fatal():
    m = ("about-time", "../../../bin/about", "sha256=A", "sha256=B")
    fatal, collisions = classify_record_mismatches([m], INDEX)
    assert fatal == [m] and collisions == []


def test_outside_collision_whose_disk_bytes_match_no_claimant_is_fatal():
    m = ("about-time", "../../../LICENSE", "sha256=A", "sha256=Z")
    fatal, collisions = classify_record_mismatches([m], INDEX)
    assert fatal == [m] and collisions == []


# check — 봉인 디렉터리를 같은 venv 의 새 emit 과 바이트 대조. emit 은 가짜로 바꾼다 (venv · 측정 없이 대조 규칙만 본다).
def _fake_emit(out):
    out.mkdir(parents=True, exist_ok=True)
    (out / "A.txt").write_bytes(b"a")
    (out / "MANIFEST.json").write_text(prof._dump({"A.txt": prof._sha(b"a")}), encoding="utf-8")


def _sealed(tmp_path, monkeypatch):
    monkeypatch.setattr(prof, "emit", _fake_emit)
    sealed = tmp_path / "sealed"
    _fake_emit(sealed)
    return sealed


def test_check_passes_on_unchanged_seal_next_to_the_human_records(tmp_path, monkeypatch):
    sealed = _sealed(tmp_path, monkeypatch)
    (sealed / "README.md").write_text("사람용", encoding="utf-8")
    (sealed / "C6_RUN.log").write_text("시각", encoding="utf-8")
    assert prof.check(sealed) == 0


def test_check_fails_when_sealed_bytes_differ_from_a_fresh_emit_even_with_a_consistent_manifest(tmp_path, monkeypatch):
    sealed = _sealed(tmp_path, monkeypatch)
    (sealed / "A.txt").write_bytes(b"b")
    (sealed / "MANIFEST.json").write_text(prof._dump({"A.txt": prof._sha(b"b")}), encoding="utf-8")
    assert prof.check(sealed) == 1


def test_check_fails_when_a_manifest_entry_is_dropped(tmp_path, monkeypatch):
    sealed = _sealed(tmp_path, monkeypatch)
    (sealed / "MANIFEST.json").write_text(prof._dump({}), encoding="utf-8")
    assert prof.check(sealed) == 1


def test_check_fails_on_an_unexpected_extra_file(tmp_path, monkeypatch):
    sealed = _sealed(tmp_path, monkeypatch)
    (sealed / "sobol_extra.npy").write_bytes(b"x")
    assert prof.check(sealed) == 1


def test_emit_leaves_no_manifest_when_cobyqa_is_not_accepted(tmp_path, monkeypatch):
    """COBYQA 대조 실패 (부속 A §3-1 fail-closed) 면 실패 기록은 남기되 MANIFEST 는 쓰지 않는다 — 완결된 봉인처럼 보이면 안 된다."""
    monkeypatch.setattr(prof, "lock_text", lambda: "lock\n")
    monkeypatch.setattr(prof, "profile", lambda: {})
    monkeypatch.setattr(prof, "cobyqa_options", lambda: {"accepted": False})
    monkeypatch.setattr(prof, "sobol", lambda out: {})
    out = tmp_path / "seal"
    with pytest.raises(SystemExit):
        prof.emit(out)
    assert (out / "COBYQA_OPTIONS.json").is_file()
    assert not (out / "MANIFEST.json").exists()
