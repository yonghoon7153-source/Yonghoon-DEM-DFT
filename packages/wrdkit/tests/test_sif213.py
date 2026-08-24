"""Smart Interface 2.13 파일 — 껍데기 헤더와 고정 레이아웃.

2.13 은 1.x 와 **파일 구조가 다르다**: 헤더 스트림이 둘이 아니라 하나이고,
그 하나가 `DataHeaderBase` 라는 봉투 안에 raw DEFLATE 로 압축돼 들어 있으며,
행 블록은 `HeaderSize` 가 가리키는 곳에서 시작한다.  그리고 **컬럼 목록을
선언하지 않는다** — 이 저장소가 §0.6 으로 금지한 하드코딩을 여기서만 해야
하는 이유이고, 그래서 픽스처가 그 레이아웃의 계약서다.

실측 파일(MJ1 multi-step CCCV, 41,738행)로 확정했고 그 근거는 `wrd.py` 의
`_SIF_213_COLUMNS` 주석과 스펙 문서에 있다.
"""

import numpy as np
import pytest

from wrdkit.wrd import WrdError, read_wrd_bytes

import synthetic


@pytest.fixture
def samples():
    return synthetic.make_cycles(n_cycles=2, points_per_branch=20)


def test_reads_the_envelope_and_the_rows(samples):
    wrd = read_wrd_bytes(synthetic.build_wrd_sif213(samples), source_name="a.wrd")
    meta = wrd.metadata
    # 행이 하나도 안 남거나 남으면 레이아웃이 틀린 것이다.
    assert meta.row_count == len(samples)
    assert meta.declared_row_count == len(samples)
    assert meta.trailing_bytes == 0
    assert len(meta.columns) == 20
    assert meta.model == "WBRS50"
    assert meta.app_version == "2.1.3.1"


def test_rows_start_at_header_size_not_at_the_end_of_the_stream(samples):
    """봉투가 끝나는 곳과 행이 시작하는 곳은 다르다.

    실측 파일에서 스트림은 4770 에서 끝났는데 HeaderSize 는 6767 이었다.
    "마지막 스트림 다음" 에서 읽기 시작하면 쓰레기를 행으로 읽고, 그 뒤의
    모든 숫자가 그럴듯하게 틀린다.
    """
    data = synthetic.build_wrd_sif213(samples, gap=256)
    wrd = read_wrd_bytes(data, source_name="a.wrd")
    assert wrd.metadata.row_count == len(samples)
    assert wrd.metadata.trailing_bytes == 0


def test_values_survive_the_round_trip(samples):
    wrd = read_wrd_bytes(synthetic.build_wrd_sif213(samples), source_name="a.wrd")
    voltage = wrd.data["voltage"]
    assert voltage[0] == pytest.approx(samples[0].voltage)
    assert wrd.data["current"][0] == pytest.approx(samples[0].current)
    # 사이클 분할의 근거가 되는 칸들이 그대로 와야 한다 (§3).
    assert set(np.unique(wrd.data["cell_status"]).tolist()) <= {1, 3, 4}
    assert wrd.data["total_step"][0] == samples[0].total_step


def test_the_schedule_is_found_under_the_private_field_name(samples):
    """2.13 은 스케줄을 `_seqDataSet` 로 쓴다 (1.x 는 `SeqDataSet`).

    한 철자만 보면 2.13 파일이 **스케줄 없이** 파싱된다 — 컷오프도 C-rate 도
    없고, 화면에는 왜 없는지가 안 나온다.
    """
    steps = (synthetic.SchedStep(name="rest", control=7),
             synthetic.SchedStep(name="charge", control=0, value=0.35))
    data = synthetic.build_wrd_sif213(samples, schedule=steps)
    meta = read_wrd_bytes(data, source_name="a.wrd").metadata
    assert meta.schedule is not None
    assert len(meta.schedule.steps) == 2


def test_an_unknown_header_version_is_refused(samples):
    """모르는 버전에 이 레이아웃을 들이대지 않는다.

    한 바이트만 어긋나도 모든 숫자가 그럴듯하게 틀린다 — 조용히 틀리는 것보다
    안 읽히는 편이 낫다 (§0.4).
    """
    data = synthetic.build_wrd_sif213(samples, version="9.9.9.9")
    with pytest.raises(WrdError) as excinfo:
        read_wrd_bytes(data, source_name="a.wrd")
    assert "9.9.9.9" in str(excinfo.value)
    assert "probe" in str(excinfo.value)


def test_a_broken_blob_says_so(samples):
    data = bytearray(synthetic.build_wrd_sif213(samples))
    # 압축 블록 한가운데를 뭉갠다.  헤더 구역은 행 블록보다 앞에 있고,
    # 봉투(클래스 레코드 + 문자열)를 지난 자리가 확실히 압축 데이터다.
    rows = len(samples) * synthetic.SIF_213_ROW_SIZE
    blob_middle = (len(data) - rows) // 2
    for i in range(blob_middle, blob_middle + 16):
        data[i] ^= 0xFF
    with pytest.raises(WrdError):
        read_wrd_bytes(bytes(data), source_name="a.wrd")


def test_end_time_comes_from_a_datetime_not_a_tick_count(samples):
    """1.x 의 EndTime 은 tick(int), 2.13 은 DateTime 이다.

    한쪽 모양만 읽으면 2.13 파일에 종료 시각이 안 붙고, '구동 중/종료' 판정이
    그것을 부분적으로 쓴다 — 빈칸이 화면만의 문제가 아니다.
    """
    meta = read_wrd_bytes(synthetic.build_wrd_sif213(samples), source_name="a.wrd").metadata
    assert meta.end_time is not None
    assert meta.start_time is not None
    assert meta.end_time >= meta.start_time
