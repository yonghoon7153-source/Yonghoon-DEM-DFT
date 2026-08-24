import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from wrdkit import read_wrd, read_wrd_bytes  # noqa: E402

import synthetic  # noqa: E402


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


@pytest.fixture
def sample_mpr():
    """A real BioLogic ``.mpr``, when one is pointed at by ``WRDKIT_EIS_SAMPLE``.

    Same bargain as ``sample_wrd``: opt-in, physics-only assertions, so it
    holds for any PEIS record rather than the one file used to work the format
    out.  ``WRDKIT_EIS_SAMPLE=/path/to/file.mpr pytest``
    """
    path = os.environ.get("WRDKIT_EIS_SAMPLE")
    if not path or not Path(path).exists():
        pytest.skip("set WRDKIT_EIS_SAMPLE to a real .mpr file to run this test")
    from wrdkit.eis import read_mpr_bytes
    return read_mpr_bytes(Path(path).read_bytes())
