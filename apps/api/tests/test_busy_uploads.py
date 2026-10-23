"""업로드가 도는 동안에도 화면은 답한다 (ADR 0048).

업로드 셋은 `async def` 였고 파싱·맞춤을 이벤트 루프 위에서 돌렸다.  실측:
EIS 한 장을 자동 맞춤으로 올리는 25 초 동안, 다른 사람이 연 셀 목록이 0.13 초에서
25.6 초가 됐다 -- 서버가 한 번에 한 가지밖에 못 했다.

여기서는 맞춤 자리에 2 초 잠을 넣고, 그동안 다른 요청이 곧바로 답하는지 본다.
TestClient 는 요청을 한 이벤트 루프에서 돌리므로, 업로드가 루프를 붙잡으면 이
테스트의 두 번째 요청도 똑같이 2 초를 기다린다.
"""

import threading
import time

import synthetic_eis as S

from app.routers import eis

#: 맞춤 자리에 넣는 잠.  다른 요청은 이것보다 한참 빨리 와야 한다.
_HOLD = 2.0


def _mpr(rs=5.0) -> bytes:
    frequency = S.log_sweep(1e6, 1e-2, 8)
    return S.build_mpr(S.spectrum_columns(
        frequency, S.randles(frequency, rs=rs, r1=20.0, q1=1e-5, n1=0.9,
                             r2=40.0, q2=1e-3, n2=0.8)))


def _upload(client, content, out, name="slow.mpr"):
    out.append(client.post(
        "/api/eis/spectra/upload", params={"kind": "liquid", "fit": "auto"},
        files={"file": (name, content, "application/octet-stream")}))


def test_a_screen_answers_while_a_file_is_being_fitted(client, monkeypatch):
    started = threading.Event()

    def slow_fit(*args, **kwargs):
        started.set()
        time.sleep(_HOLD)

    monkeypatch.setattr(eis, "_run_auto", slow_fit)
    done: list = []
    worker = threading.Thread(target=_upload, args=(client, _mpr(), done))
    worker.start()
    try:
        assert started.wait(10), "업로드가 맞춤까지 가지 못했다"
        t0 = time.perf_counter()
        listed = client.get("/api/samples")
        waited = time.perf_counter() - t0
    finally:
        worker.join(30)
    assert listed.status_code == 200
    assert waited < _HOLD / 2, (
        f"셀 목록이 업로드를 {waited:.2f} 초 기다렸다 -- 업로드가 서버를 붙잡고 있다")
    assert done and done[0].status_code == 201, done and done[0].text


def test_two_uploads_of_the_same_bytes_still_make_one_spectrum(client, monkeypatch):
    """업로드는 이제 스레드에서 돈다 -- 그래도 업로드끼리는 한 줄이다.

    같은 바이트가 두 기계에서 동시에 올라오면, 중복 검사와 삽입 사이에 다른
    업로드가 끼면 둘 다 "처음 보는 파일" 로 읽는다.  파싱을 느리게 해서 그 틈을
    넓혀도 스펙트럼은 하나, 둘째는 중복으로 돌아와야 한다.
    """
    parse = eis._parse_sweeps

    def slow_parse(*args, **kwargs):
        time.sleep(0.5)
        return parse(*args, **kwargs)

    monkeypatch.setattr(eis, "_parse_sweeps", slow_parse)
    monkeypatch.setattr(eis, "_run_auto", lambda *args, **kwargs: None)
    content = _mpr(rs=6.5)
    done: list = []
    workers = [threading.Thread(target=_upload, args=(client, content, done, f"same_{i}.mpr"))
               for i in range(2)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join(30)
    assert sorted(response.status_code for response in done) == [201, 201]
    assert sum(1 for response in done if response.json().get("duplicate")) == 1
    listed = client.get("/api/eis/spectra").json()
    assert len([row for row in listed if row["n_points"]]) == 1
