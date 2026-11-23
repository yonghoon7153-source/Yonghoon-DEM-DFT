"""주간 갱신이 무엇을 '새 회차'로 받는가 — 자체 리뷰 1차 A1·A2 (docs/SELF_REVIEW_R1.md).

리뷰 반례: 동행복권이 끝이 잘린 목록(로또 1..1248)을 돌려주면 weekly_update 가 최신 회차가
'바뀌었다'(`!=`)만 보고 새 회차로 받아, 분석과 테스트를 통과시키고 종료 코드 0(커밋·배포)으로
끝났다 — "반영: 로또 1251→1248회". 옛 회차 값이 바뀐 목록(600회를 1~6 으로)도 같았다.

네트워크와 무거운 분석 없이 같은 경로를 재현한다: 실제 fetch_data.main() 과 weekly_update.main()
을 임시 data/ 에서 돌리고 HTTP 응답만 바꿔 끼운다. 분석·테스트 단계는 통과(0)로 둔다 — 리뷰 반례에서
실제 build_results --quick 과 테스트 52개가 통과했다 (그 단계는 잘린 목록을 못 잡는다).
"""
import functools
import hashlib
import json
import sys

import pytest

import dataset
import fetch_data
import weekly_update

RAW = {"lotto645.json": (dataset.RAW_DIR / "lotto645.json").read_bytes(),
       "pension720.json": (dataset.RAW_DIR / "pension720.json").read_bytes()}
KEY = {"lotto645.json": ("list", "ltEpsd"), "pension720.json": ("result", "psltEpsd")}


def body(name: str, edit=None) -> bytes:
    """실제 원본 응답을 회차 순으로 정렬해 edit(rows) 로 고친 응답."""
    obj = json.loads(RAW[name])
    field, rnd = KEY[name]
    rows = sorted(obj["data"][field], key=lambda r: int(r[rnd]))
    if edit:
        rows = edit(rows) or rows
    obj["data"][field] = rows
    return json.dumps(obj).encode()


N_LOTTO = len(dataset.parse_lotto(RAW["lotto645.json"]))
N_PENSION = len(dataset.parse_pension(RAW["pension720.json"]))


@pytest.fixture
def site(tmp_path, monkeypatch):
    """임시 data/ 에서 받기 → 주간 갱신을 돌리는 장치. 저장소의 lottery/data 는 건드리지 않는다."""
    data = tmp_path / "data"
    monkeypatch.setattr(dataset, "RAW_DIR", data / "raw")
    monkeypatch.setattr(fetch_data, "write_csvs", functools.partial(fetch_data.write_csvs, out_dir=data))
    monkeypatch.setattr(weekly_update, "DATA", data)
    monkeypatch.setattr(weekly_update, "MANIFEST", data / "raw" / "MANIFEST.json")
    served: dict[str, bytes] = {}
    monkeypatch.setattr(fetch_data, "_get", lambda url, referer: served[url])

    class Site:
        steps: list[str] = []  # 받기 뒤에 돈 단계 (분석·테스트)

        def serve(self, lotto: bytes, pension: bytes) -> None:
            served[fetch_data.SOURCES["lotto645.json"][0]] = lotto
            served[fetch_data.SOURCES["pension720.json"][0]] = pension

        def fetch(self, *flags: str) -> int:
            monkeypatch.setattr(sys, "argv", ["fetch_data.py", *flags])
            try:
                return fetch_data.main()
            except Exception as e:  # 하위 프로세스라면 잡히지 않은 예외 = 종료 코드 1
                print(f"{type(e).__name__}: {e}")
                return 1

        def weekly(self) -> int:
            return self.weekly_ok()

        def weekly_ok(self) -> int:
            def run(args, label):
                if args == ["fetch_data.py"]:
                    return self.fetch()
                self.steps.append(label)
                return 0
            monkeypatch.setattr(weekly_update, "_run", run)
            monkeypatch.setattr(sys, "argv", ["weekly_update.py"])
            return weekly_update.main()

        def digest(self) -> dict[str, str]:
            return {p.relative_to(data).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted(data.rglob("*")) if p.is_file()}

    s = Site()
    s.steps = []
    return s


@pytest.mark.parametrize("game", ["lotto645.json", "pension720.json"])
def test_truncated_list_is_not_a_new_round(site, capsys, game):
    """A1: 최신 회차가 줄어든 목록 → 종료 코드 1, 분석·배포 단계 없음, data/ 그대로."""
    site.serve(body("lotto645.json"), body("pension720.json"))
    assert site.fetch() == 0
    kept = site.digest()
    cut = {"lotto645.json": body("lotto645.json"), "pension720.json": body("pension720.json")}
    cut[game] = body(game, lambda rows: rows[:-3])
    site.serve(cut["lotto645.json"], cut["pension720.json"])

    rc = site.weekly()
    out = capsys.readouterr().out
    assert rc == 1, out
    assert "반영" not in out and site.steps == []
    assert site.digest() == kept


def test_changed_old_round_is_not_accepted(site, capsys):
    """A2: 새 회차 하나 + 옛 600회 번호가 바뀐 목록 → 종료 코드 1, 무엇이 바뀌었는지 출력, data/ 그대로."""
    site.serve(body("lotto645.json", lambda rows: rows[:-1]), body("pension720.json"))
    assert site.fetch() == 0
    kept = site.digest()

    def alter(rows):
        rows[599].update({f"tm{k}WnNo": k for k in range(1, 7)})
    changed = body("lotto645.json", alter)
    dataset.parse_lotto(changed)  # 형식 검증은 통과한다 — 잡아야 하는 것은 이력 비교다
    site.serve(changed, body("pension720.json"))

    rc = site.weekly()
    out = capsys.readouterr().out
    assert rc == 1, out
    assert "반영" not in out and site.steps == []
    assert "600회" in out
    assert site.digest() == kept


def test_genuine_new_round_still_goes_through(site, capsys):
    """대조: 옛 회차가 그대로이고 끝에 새 회차가 붙은 목록은 지금처럼 반영된다."""
    site.serve(body("lotto645.json", lambda rows: rows[:-1]), body("pension720.json", lambda rows: rows[:-1]))
    assert site.fetch() == 0
    site.serve(body("lotto645.json"), body("pension720.json"))

    rc = site.weekly()
    out = capsys.readouterr().out
    assert rc == 0, out
    assert f"로또 {N_LOTTO - 1}→{N_LOTTO}회" in out and f"연금 {N_PENSION - 1}→{N_PENSION}회" in out
    assert site.steps == ["분석", "테스트"]


def test_human_can_accept_an_official_correction(site):
    """공식 정정이 맞다고 사람이 확인하면 받을 수 있어야 한다 (주간 작업은 이 플래그를 쓰지 않는다)."""
    site.serve(body("lotto645.json"), body("pension720.json"))
    assert site.fetch() == 0
    site.serve(body("lotto645.json", lambda rows: rows[:-3]), body("pension720.json"))
    assert site.fetch() == 1
    assert site.fetch("--allow-history-change") == 0
    assert len(dataset.load_lotto(dataset.RAW_DIR)) == N_LOTTO - 3  # 기본 인자는 실제 data/raw 에 묶여 있다


def test_failed_analysis_restores_data_so_a_retry_sees_the_new_round(site, capsys, monkeypatch):
    """자체 리뷰 D1 (PARTIAL): 분석·테스트가 실패하면(2) 받은 파일이 남고 백업은 지워져, 같은 사본에서 다시 돌리면
    '새 회차 없음'(3) 으로 끝났다. 실패하면 data/ 를 받기 전으로 되돌려야 다시 돌렸을 때 새 회차를 다시 본다."""
    site.serve(body("lotto645.json", lambda rows: rows[:-1]), body("pension720.json"))
    assert site.fetch() == 0
    kept = site.digest()
    site.serve(body("lotto645.json"), body("pension720.json"))
    assert _weekly_with(site, monkeypatch, lambda args, label: 1 if label == "분석" else 0) == 2
    assert site.digest() == kept, "실패한 주간 작업이 받은 파일을 남겼다"
    capsys.readouterr()
    assert site.weekly_ok() == 0, "다시 돌리면 새 회차를 다시 봐야 한다"


def _weekly_with(site, monkeypatch, step):
    """주간 작업을 돌리되 받기 뒤 단계(분석·테스트)는 step(args, label) 이 정한다."""
    def run(args, label):
        if args == ["fetch_data.py"]:
            return site.fetch()
        return step(args, label)
    monkeypatch.setattr(weekly_update, "_run", run)
    monkeypatch.setattr(sys, "argv", ["weekly_update.py"])
    return weekly_update.main()
