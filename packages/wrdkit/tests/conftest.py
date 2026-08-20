import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import synthetic  # noqa: E402
from wrdkit import read_wrd, read_wrd_bytes  # noqa: E402


@pytest.fixture(scope="session")
def synthetic_bytes() -> bytes:
    return synthetic.build_wrd(synthetic.make_cycles(n_cycles=3, points_per_branch=40))


@pytest.fixture(scope="session")
def synthetic_wrd(synthetic_bytes):
    return read_wrd_bytes(synthetic_bytes, source_name="synthetic.wrd")


@pytest.fixture(scope="session")
def sample_wrd():
    """A real instrument file, when one is pointed at by ``WRDKIT_SAMPLE``.

    Instrument files are tens of megabytes and cannot live in the repository,
    so these checks are opt-in: ``WRDKIT_SAMPLE=/path/to/file.wrd pytest``.
    """
    path = os.environ.get("WRDKIT_SAMPLE")
    if not path or not Path(path).exists():
        pytest.skip("set WRDKIT_SAMPLE to a real .wrd file to run this test")
    return read_wrd(path)
