"""Service-layer behaviour that no router exposes directly."""

import os
import re
import time
from datetime import datetime, timedelta

import pytest
from sqlmodel import Session

from app import services
from app.db import engine
from app.models import Sample


@pytest.fixture
def instrument_clock(monkeypatch):
    """Run the test as if the lab PC were on KST, as it is in Yongin."""
    if not hasattr(time, "tzset"):
        pytest.skip("changing the process time zone needs a POSIX platform")
    # Put back whatever was there, not "nothing".  CI runs this suite under a
    # timezone matrix (TZ=Asia/Seoul, America/Los_Angeles); popping the
    # variable would leave every later test on UTC, so a zone-sensitive bug
    # would pass or fail depending on which test ran first.
    previous = os.environ.get("TZ")
    monkeypatch.setenv("TZ", "KST-9")
    time.tzset()
    yield
    # monkeypatch restores the variable, but only tzset re-reads it.
    if previous is None:
        os.environ.pop("TZ", None)
    else:
        os.environ["TZ"] = previous
    time.tzset()


def _report(client, sample_id, wrd_bytes, end_time: datetime):
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("c_012.wrd", wrd_bytes, "application/octet-stream")})
    with Session(engine) as session:
        sample = session.get(Sample, sample_id)
        for run in sample.runs:
            run.end_time = end_time
            session.add(run)
        session.commit()
        session.refresh(sample)
        return services.build_cell_report(session, sample)


def _recency(report):
    return [e for e in report.evidence if e.signal == "recency"]


def test_a_run_with_no_schedule_keeps_formation_uncertain():
    """스케줄을 못 읽은 파일은 "모름" 이지 무표가 아니다 (§0.4).

    건너뛰면 남은 파일 하나의 "no" 가 셀 전체의 "no" 가 되고, 기준이 1 로
    옮겨 간다 -- formation 을 담은 파일이 바로 그 못 읽은 쪽일 수 있다.
    """
    from types import SimpleNamespace as NS
    no = NS(schedule_json='{"formation": "no"}')
    silent = NS(schedule_json="")
    assert services.sample_formation(NS(runs=[no, silent])) == "unclear"
    assert services.sample_formation(NS(runs=[no])) == "no"
    yes = NS(schedule_json='{"formation": "yes"}')
    assert services.sample_formation(NS(runs=[yes, silent])) == "yes"
    assert services.sample_formation(NS(runs=[])) == "unclear"


def test_a_cell_silent_for_hours_is_not_called_running(
        client, sample_id, wrd_bytes, instrument_clock):
    """The file's clock is the lab PC's, so ours has to be read the same way.

    Subtracting a KST wall clock from a naive UTC "now" makes every record
    look nine hours younger, which keeps a stopped cell "running" for a whole
    working day.
    """
    report = _report(client, sample_id, wrd_bytes,
                     datetime.now() - timedelta(hours=3))

    assert [e.points_to for e in _recency(report)] == ["finished"]
    assert report.state == "finished"


def test_a_timestamp_from_a_clock_we_do_not_share_gives_no_recency_evidence(
        client, sample_id, wrd_bytes):
    """A future last sample would read as fresh and print a negative age."""
    report = _report(client, sample_id, wrd_bytes,
                     datetime.now() + timedelta(hours=9))

    assert _recency(report) == []
    assert not any(re.search(r"-\d", e.detail) for e in report.evidence)


def test_a_timestamp_a_minute_ahead_still_counts_as_just_now(
        client, sample_id, wrd_bytes):
    """Two PCs drift by seconds; that is not a reason to withhold a verdict."""
    report = _report(client, sample_id, wrd_bytes,
                     datetime.now() + timedelta(minutes=1))

    assert [e.points_to for e in _recency(report)] == ["running"]
    assert "0.0 h" in _recency(report)[0].detail
