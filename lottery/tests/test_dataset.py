"""dataset.py 검증 규칙 — 실제 원본을 메모리에서 하나씩 망가뜨려 각 규칙이 잡는지 본다.

새 검증기라 '처음부터 통과'가 당연해 보이지만, 여기서는 변형 하나당 규칙 하나가 걸리는지를
확인한다. 규칙을 꺼 보면 해당 테스트가 실패해야 한다 (커밋 메시지에 변형 실행 결과를 적었다).
"""
import copy
import json

import pytest

import dataset

RAW_L = (dataset.RAW_DIR / "lotto645.json").read_bytes()
RAW_P = (dataset.RAW_DIR / "pension720.json").read_bytes()


def _mut_lotto(fn) -> bytes:
    obj = json.loads(RAW_L)
    rows = sorted(obj["data"]["list"], key=lambda r: r["ltEpsd"])
    fn(rows)
    obj["data"]["list"] = rows
    return json.dumps(obj).encode()


def _mut_pension(fn) -> bytes:
    obj = json.loads(RAW_P)
    rows = sorted(obj["data"]["result"], key=lambda r: r["psltEpsd"])
    fn(rows)
    obj["data"]["result"] = rows
    return json.dumps(obj).encode()


def test_real_snapshot_passes_and_matches_manifest():
    lotto, pension = dataset.parse_lotto(RAW_L), dataset.parse_pension(RAW_P)
    man = json.loads((dataset.RAW_DIR / "MANIFEST.json").read_text())
    assert len(lotto) == man["files"]["lotto645.json"]["records"]
    assert len(pension) == man["files"]["pension720.json"]["records"]
    assert lotto[0].numbers == (10, 23, 29, 33, 37, 40) and lotto[0].bonus == 16


def test_manifest_sha256_matches_raw_bytes():
    import hashlib
    man = json.loads((dataset.RAW_DIR / "MANIFEST.json").read_text())
    for name in ("lotto645.json", "pension720.json"):
        assert hashlib.sha256((dataset.RAW_DIR / name).read_bytes()).hexdigest() == man["files"][name]["sha256"]


@pytest.mark.parametrize("label, mutate, expect", [
    ("회차 빠짐", lambda r: r.pop(500), "연속"),
    ("번호 중복", lambda r: r[10].update(tm2WnNo=r[10]["tm1WnNo"]), "서로 다른 6개"),
    ("범위 밖 번호", lambda r: r[10].update(tm6WnNo=46), "1..45"),
    ("정렬 안 됨", lambda r: r[10].update(tm1WnNo=r[10]["tm2WnNo"], tm2WnNo=r[10]["tm1WnNo"]), "오름차순"),
    ("보너스가 본번호와 겹침", lambda r: r[10].update(bnsWnNo=r[10]["tm3WnNo"]), "보너스"),
    ("요일 어긋남", lambda r: r[700].update(ltRflYmd="20160101"), "요일"),
    ("1회 기준값 어긋남", lambda r: r[0].update(bnsWnNo=17), "1회"),
    ("5등 당첨금 이상", lambda r: r[300].update(rnk5WnAmt=7000), "게임 가격"),
    ("자동+수동+반자동 ≠ 1등", lambda r: r[1200].update(winType1=r[1200]["winType1"] + 1), "합이 1등"),
    ("262회 이전 1등 구분값", lambda r: r[100].update(winType1=1), "이전인데"),
    ("판매액 10% 부풀림", lambda r: [x.update(wholEpsdSumNtslAmt=int(x["wholEpsdSumNtslAmt"] * 1.1)) for x in r], "실측/기대"),
])
def test_lotto_validator_catches(label, mutate, expect):
    with pytest.raises(dataset.DataError, match=expect):
        dataset.parse_lotto(_mut_lotto(mutate))


@pytest.mark.parametrize("label, mutate, expect", [
    ("회차 빠짐", lambda r: r.pop(100), "연속"),
    ("조 범위 밖", lambda r: r[5].update(wnBndNo="6"), "1..5"),
    ("6자리 아님", lambda r: r[5].update(wnRnkVl="12345"), "6자리"),
    ("숫자 아님", lambda r: r[5].update(bnsRnkVl="12a456"), "6자리"),
    ("요일 어긋남", lambda r: r[50].update(psltRflYmd="20210102"), "요일"),
])
def test_pension_validator_catches(label, mutate, expect):
    with pytest.raises(dataset.DataError, match=expect):
        dataset.parse_pension(_mut_pension(mutate))


def test_non_json_and_wrong_shape_fail_closed():
    with pytest.raises(dataset.DataError):
        dataset.parse_lotto(b"<html>moved</html>")
    with pytest.raises(dataset.DataError):
        dataset.parse_lotto(json.dumps({"data": {"list": []}}).encode())
