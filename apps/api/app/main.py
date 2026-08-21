"""Yonghoon Battery Lab Workbench -- HTTP API."""

from __future__ import annotations

import math
import sys
from pathlib import Path

# Running straight from the repo (make api) must find the science core without
# an editable install first.
_WRDKIT_SRC = Path(__file__).resolve().parents[3] / "packages/wrdkit/src"
if _WRDKIT_SRC.exists() and str(_WRDKIT_SRC) not in sys.path:
    sys.path.insert(0, str(_WRDKIT_SRC))

from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI, HTTPException, Request  # noqa: E402
from fastapi.encoders import jsonable_encoder  # noqa: E402
from fastapi.exceptions import RequestValidationError  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import (  # noqa: E402
    FileResponse,
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
    StreamingResponse,
)
from fastapi.staticfiles import StaticFiles  # noqa: E402

from wrdkit import __version__ as wrdkit_version  # noqa: E402
from wrdkit.composition import Role  # noqa: E402

from . import gate  # noqa: E402
from .actor import ACTOR_HEADER, set_actor  # noqa: E402
from .db import init_db  # noqa: E402
from .live import (  # noqa: E402
    REVISION_HEADER,
    revision,
    revision_stream,
    should_bump,
)
from .routers import (  # noqa: E402
    activity,
    analysis,
    exports,
    groups,
    presets,
    runs,
    samples,
)
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

@app.exception_handler(RequestValidationError)
async def _validation_error(request, exc: RequestValidationError):
    """422 with a body that can actually be serialised.

    Pydantic echoes the offending input back in the error detail.  When that
    input is NaN or Infinity -- exactly the values the new bounds exist to
    reject -- ``json.dumps`` refuses it and the 422 turns into a 500 with a
    stack trace, so the one case the validation was added for reports as a
    server fault instead of bad input.
    """
    def clean(value):
        if isinstance(value, float) and not math.isfinite(value):
            return repr(value)
        if isinstance(value, dict):
            return {key: clean(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [clean(item) for item in value]
        return value

    return JSONResponse(status_code=422,
                        content={"detail": clean(jsonable_encoder(exc.errors()))})


@app.middleware("http")
async def _announce_writes(request, call_next):
    """Bump the revision after anything that changed something.

    Here rather than in each router: a new endpoint is live from the moment it
    exists, and nobody has to remember to announce.  The alternative -- a call
    at the end of every write -- is one that gets forgotten exactly once, and
    the symptom is a screen that is stale for one kind of edit only, which is
    the hardest kind of staleness to notice.
    """
    # Who is writing, for the whole request.  Set here and not in a dependency
    # so it is in place before any route, service or flush listener runs --
    # the listener that stamps rows is the one that most needs it, and it runs
    # far away from anything that could have been given an argument.
    set_actor(request.headers.get(ACTOR_HEADER))
    response = await call_next(request)
    if should_bump(request.method, response.status_code, request.url.path):
        response.headers[REVISION_HEADER] = str(revision.bump())
    return response


@app.middleware("http")
async def _gate(request: Request, call_next):
    """One shared password, and only while the address is outside (ADR 0014).

    Registered after ``_announce_writes`` so it ends up outermost: a request
    that is not getting in should not reach anything that reads the database
    or stamps an actor.

    With no password configured this costs one attribute read, which is the
    point -- the lab-network case must not pay for the away-from-lab one.
    """
    secret = settings.password
    if (not secret
            or gate.is_open(request.url.path)
            or gate.accepts_cookie(request.cookies.get(gate.COOKIE), secret)):
        return await call_next(request)

    # The browser gets a page it can act on; the app's own fetches get JSON,
    # because HTML arriving where JSON was expected fails as a parse error
    # somewhere far away from the actual cause.
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=401, content={"detail": "암호가 필요합니다."})
    return HTMLResponse(gate.login_page(), status_code=401)


@app.post("/__login", include_in_schema=False)
async def login(request: Request):
    """The door.  A plain form post, so it works before any script loads."""
    form = await request.form()
    given = form.get("password")
    if not gate.accepts_password(given if isinstance(given, str) else None,
                                 settings.password):
        return HTMLResponse(gate.login_page(wrong=True), status_code=401)

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(gate.COOKIE, gate.token(settings.password),
                        max_age=gate.MAX_AGE, httponly=True, samesite="lax")
    return response


app.include_router(groups.router)
app.include_router(samples.router)
app.include_router(runs.router)
app.include_router(analysis.router)
app.include_router(exports.router)
app.include_router(presets.router)
app.include_router(activity.router)


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "wrdkit": wrdkit_version,
        "data_dir": str(settings.data_dir),
        "max_upload_mb": settings.max_upload_bytes // (1024 * 1024),
    }


@app.get("/api/revision")
def read_revision() -> dict:
    """What the database is at, for anything that cannot hold a stream."""
    return {"revision": revision.value}


@app.get("/api/events")
async def events(request: Request):
    """Server-sent events: one line whenever somebody changes something.

    What is sent is only the number, not what changed (see ``live.py``).  The
    browser re-fetches whatever that screen is showing, which keeps this
    endpoint from having to know anything about screens.
    """
    return StreamingResponse(
        revision_stream(request.is_disconnected),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            # nginx buffers by default, which would hold each event until the
            # buffer fills -- turning a live stream into a slow one.
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/meta")
def meta() -> dict:
    """Choices the UI renders: capacity bases, cell states, knee methods.

    Composition presets are *not* here.  They are rows now, saved by whoever
    is at the bench, so they are fetched from /api/composition-presets and can
    change without a restart (ADR 0010).
    """
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
