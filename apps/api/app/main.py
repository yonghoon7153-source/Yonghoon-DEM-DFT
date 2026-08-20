"""Yonghoon Battery Lab Workbench -- HTTP API."""

from __future__ import annotations

import sys
from pathlib import Path

# Running straight from the repo (make api) must find the science core without
# an editable install first.
_WRDKIT_SRC = Path(__file__).resolve().parents[3] / "packages/wrdkit/src"
if _WRDKIT_SRC.exists() and str(_WRDKIT_SRC) not in sys.path:
    sys.path.insert(0, str(_WRDKIT_SRC))

from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from wrdkit import PRESETS as COMPOSITION_PRESETS  # noqa: E402
from wrdkit import __version__ as wrdkit_version  # noqa: E402
from wrdkit.composition import Role  # noqa: E402

from .db import init_db  # noqa: E402
from .routers import analysis, exports, groups, runs, samples  # noqa: E402
from .schemas import basis_choices  # noqa: E402
from .settings import settings  # noqa: E402

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Battery Lab Workbench",
    version="0.1.0",
    summary="Read WonATech .wrd files, normalise them, and compare cells.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(groups.router)
app.include_router(samples.router)
app.include_router(runs.router)
app.include_router(analysis.router)
app.include_router(exports.router)


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "wrdkit": wrdkit_version,
        "data_dir": str(settings.data_dir),
        "max_upload_mb": settings.max_upload_bytes // (1024 * 1024),
    }


@app.get("/api/meta")
def meta() -> dict:
    """Choices the UI renders: capacity bases, cell states, knee methods."""
    return {
        "bases": [choice.model_dump() for choice in basis_choices()],
        "states": ["auto", "running", "finished"],
        "knee_methods": [
            {"value": "segmented", "label": "Segmented fit (two-line break point)"},
            {"value": "slope_ratio", "label": "Fade rate multiple of early life"},
            {"value": "threshold", "label": "Retention threshold crossing"},
            {"value": "curvature", "label": "Maximum curvature"},
        ],
        "default_plot_points": settings.default_plot_points,
        "composition_presets": list(COMPOSITION_PRESETS),
        "component_roles": [
            {"value": Role.ACTIVE, "label": "활물질 (AM)"},
            {"value": Role.ELECTROLYTE, "label": "고체전해질 (SE)"},
            {"value": Role.CONDUCTIVE, "label": "도전재"},
            {"value": Role.BINDER, "label": "바인더"},
            {"value": Role.OTHER, "label": "기타"},
        ],
    }
