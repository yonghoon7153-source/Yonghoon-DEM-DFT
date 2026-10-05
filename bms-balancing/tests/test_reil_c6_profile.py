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


#: ★ 2026-10-06 C6-N1 — 봉인 lock 13 · 14 행의 실제 판 · RECORD 파일 sha256 (`reil_c6_20261005/REIL_C6.lock.txt`)
REC_AT = "e5a630322aead38c00d7d20ca0050eb7cd2024eb035505a6ef7bab8e5329f0bd"
REC_AP = "00c80da0799ae100798d538d9946e030259eae3b2b39cb70f99e7ff6ac7e9be8"
DISTS = {"about-time": {"version": "4.2.1", "record": REC_AT}, "alive-progress": {"version": "3.3.0", "record": REC_AP},
         "numpy": {"version": "2.4.6", "record": "n" * 64}, "numpy-shadow-claim": {"version": "1.0", "record": "x" * 64}}
LICENSE_MM = ("about-time", "../../../LICENSE", "sha256=A", "sha256=B")


def test_explained_collision_outside_site_packages_is_recorded_not_fatal():
    """허용 목록의 한 건 — 위치 · 배포판 쌍 · 판 · RECORD sha · 방향이 모두 맞고, 해시 셋이 lock 에 값으로 남는다."""
    fatal, collisions = classify_record_mismatches([LICENSE_MM], INDEX, dists=DISTS)
    assert fatal == []
    assert collisions == [{"path": "../../../LICENSE", "dist": "about-time",
                           "claimed_by": ["about-time", "alive-progress"], "disk_matches": "alive-progress",
                           "covered": {"version": "4.2.1", "record_sha256": REC_AT, "expected": "sha256=A"},
                           "disk_owner": {"version": "3.3.0", "record_sha256": REC_AP, "expected": "sha256=B"},
                           "disk": "sha256=B"}]


# ── C6-N1 (2026-10-06 · Codex 검토 `prereview_reil_v2_annexD_c6_20261006`) — 고정 LICENSE 한 건만 허용, 나머지는 봉인 거부 ──
def test_without_dist_identity_even_the_known_license_collision_is_fatal():
    """판 · RECORD 를 모르면 허용 목록과 대조할 수 없다 — fail-closed."""
    fatal, collisions = classify_record_mismatches([LICENSE_MM], INDEX)
    assert fatal == [LICENSE_MM] and collisions == [], "판 · RECORD 없이 LICENSE 충돌을 통과시켰다"


def test_an_executable_outside_site_packages_is_fatal_even_when_another_record_matches_the_disk():
    """회신의 반례 그대로 — `../../../bin/tool` 을 두 배포판이 주장하고 디스크가 두 번째와 같다 (문서 조건 둘 다 만족)."""
    index = {**INDEX, "about-time": {**INDEX["about-time"], "../../../bin/tool": "sha256=A"},
             "alive-progress": {**INDEX["alive-progress"], "../../../bin/tool": "sha256=B"}}
    m = ("about-time", "../../../bin/tool", "sha256=A", "sha256=B")
    for kw in ({}, {"dists": DISTS}):
        fatal, collisions = classify_record_mismatches([m], index, **kw)
        assert fatal == [m] and collisions == [], f"실행 파일 충돌을 설명된 충돌로 통과시켰다 ({kw})"


@pytest.mark.parametrize("who,key,value", [("about-time", "version", "4.2.2"), ("about-time", "record", "0" * 64),
                                           ("alive-progress", "version", "3.3.1"), ("alive-progress", "record", "0" * 64)],
                         ids=["covered-version", "covered-record", "owner-version", "owner-record"])
def test_the_same_license_with_another_version_or_record_is_fatal(who, key, value):
    dists = {**DISTS, who: {**DISTS[who], key: value}}
    fatal, collisions = classify_record_mismatches([LICENSE_MM], INDEX, dists=dists)
    assert fatal == [LICENSE_MM] and collisions == [], f"{who}.{key} 가 달라도 통과시켰다"


def test_the_reversed_direction_is_fatal():
    """덮인 쪽 · 디스크 쪽이 뒤바뀐 설치 순서는 관측된 그 한 건이 아니다."""
    index = {**INDEX, "about-time": {"../../../LICENSE": "sha256=B"}, "alive-progress": {"../../../LICENSE": "sha256=A"}}
    m = ("alive-progress", "../../../LICENSE", "sha256=A", "sha256=B")
    fatal, collisions = classify_record_mismatches([m], index, dists=DISTS)
    assert fatal == [m] and collisions == [], "뒤바뀐 방향을 통과시켰다"


@pytest.mark.parametrize("rel", ["../../LICENSE", "../../../../LICENSE", "../../../LICENSE.txt"],
                         ids=["shallower", "deeper", "suffix"])
def test_other_spellings_of_the_path_are_fatal(rel):
    index = {**INDEX, "about-time": {rel: "sha256=A"}, "alive-progress": {rel: "sha256=B"}}
    m = ("about-time", rel, "sha256=A", "sha256=B")
    fatal, collisions = classify_record_mismatches([m], index, dists=DISTS)
    assert fatal == [m] and collisions == [], f"{rel!r} 를 통과시켰다"


def test_a_third_claimant_is_fatal():
    """관측된 충돌은 두 배포판 사이였다 — 셋째 주장자가 있으면 그 한 건이 아니다."""
    index = {**INDEX, "numpy": {**INDEX["numpy"], "../../../LICENSE": "sha256=C"}}
    fatal, collisions = classify_record_mismatches([LICENSE_MM], index, dists=DISTS)
    assert fatal == [LICENSE_MM] and collisions == [], "셋째 주장자가 있는데 통과시켰다"


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
