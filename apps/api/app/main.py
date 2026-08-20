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

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402

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


# --------------------------------------------------------------------------
# Serving the built frontend
#
# `make serve` (and `bml`) run one process on one port: the API under /api,
# the compiled web app everywhere else.  One URL to remember, no CORS, and no
# node process on the lab machine.  During development Vite serves the app
# instead and proxies /api here, so `mount_web` finds no build and only
# installs the "not built yet" notice.
# --------------------------------------------------------------------------
def mount_web(target: FastAPI, dist: Path) -> bool:
    """Serve a built frontend from *dist*.  Returns whether one was found.

    Kept a function rather than module-level code so the routing can be
    tested against a temporary build directory.
    """
    if not (dist / "index.html").is_file():

        @target.get("/", include_in_schema=False)
        def no_build() -> dict:
            """Say what to do, rather than 404 on the address people typed."""
            return {
                "status": "api only",
                "detail": (
                    "The web app has not been built. Run `bml` (or `make serve`) "
                    "to build and serve it on one port, or `bml dev` for the "
                    "development servers. The API is live at /api."
                ),
                "expected_build": str(dist),
                "port": settings.port,
            }

        return False

    root = dist.resolve()
    if (dist / "assets").is_dir():
        target.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

    @target.get("/{path:path}", include_in_schema=False)
    def spa(path: str) -> FileResponse:
        """Serve a built file, falling back to index.html for client routes.

        The browser routes /samples/1 itself, so a deep link must return
        index.html rather than a 404 -- but only for paths that are neither a
        real file nor an API call.
        """
        if path == "api" or path.startswith("api/"):
            # Without this an API typo would render the app and look like it
            # worked; a 404 says what actually happened.
            raise HTTPException(404, "no such endpoint")

        if path:
            # resolve() before the containment check: ../../etc/passwd must not
            # escape the build directory.
            candidate = (root / path).resolve()
            if candidate.is_file() and candidate.is_relative_to(root):
                return FileResponse(candidate)

        return FileResponse(root / "index.html")

    return True


mount_web(app, settings.web_dist)
