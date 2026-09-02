"""Yonghoon Battery Lab Workbench -- HTTP API."""

from __future__ import annotations

import math
import re
import secrets
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
from sqlalchemy.exc import (  # noqa: E402
    DataError,
    DBAPIError,
    IntegrityError,
    ProgrammingError,
)

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
    changelog,
    eis,
    exports,
    feedback,
    gitt,
    groups,
    presets,
    runs,
    samples,
)
from .schemas import basis_choices  # noqa: E402
from .settings import REPO_ROOT, settings  # noqa: E402


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


#: 저장 장치가 사라진 것을 **저장 장치가 사라졌다고** 말한다.
#:
#: 실측 2026-08-30: 데이터 폴더를 둔 외장하드를 뽑았다 끼웠더니 돌던 서버가
#: 죽은 마운트를 계속 쥐고 있었고, 화면에는 `500 Internal Server Error` 만
#: 떴다.  그 한 줄로는 무엇이 잘못됐는지도, 데이터가 남아 있는지도 알 수 없다 —
#: 실제로 "초기화된 건가" 를 먼저 물었다.  §0.4 위반이다: 우리는 이유를 안다.
#:
#: **원인을 아는 것만 원인이라고 적는다.**  sqlite 가 장치·파일 이야기를 하면
#: 데이터 폴더를 짚고, 아니면(잠김·스키마 등) 그냥 sqlite 가 한 말을 그대로
#: 옮긴다.  추측한 처방을 지어내지 않는다.
_STORAGE_GONE = re.compile(
    r"disk i/o error|unable to open database file|input/output error"
    r"|no such file or directory|stale file handle|attempt to write a readonly"
    r"|disk image is malformed|closed database|not a database",
    re.IGNORECASE,
)

#: 사람이 보낸 것이 잘못된 것들.  같은 `DBAPIError` 가지에 달려 있지만 저장소
#: 문제가 아니라서, "외장하드를 보세요" 로 감싸면 안 된다 — 다시 던져서
#: 500 과 traceback 을 그대로 보낸다.
_NOT_STORAGE = (IntegrityError, ProgrammingError, DataError)


#: **`OperationalError` 하나로는 모자랐다.**  드라이브가 죽으면 sqlite 는
#: `OperationalError` 만 내지 않는다 — `database disk image is malformed` 는
#: `DatabaseError` 로, 끊긴 연결은 `InterfaceError` 로 온다.  둘 다
#: `OperationalError` 의 하위가 아니라서 (형제다) 예전 핸들러를 그냥 지나쳐
#: **맨 500 이 그대로** 나갔다 — 고쳤다고 한 바로 그 화면이.
#: 그래서 드라이버가 내는 것(`DBAPIError`) 전부를 받고, 우리 몫이 아닌 것만
#: 도로 던진다.
@app.exception_handler(DBAPIError)
async def _storage_unreadable(request, exc: DBAPIError):
    """503 with a sentence, instead of a bare 500."""
    if isinstance(exc, _NOT_STORAGE):
        raise exc
    said = str(getattr(exc, "orig", None) or exc).strip().splitlines()[0][:200]
    if _STORAGE_GONE.search(said):
        detail = (
            f"데이터 폴더를 읽지 못했습니다 — {settings.data_dir} "
            f"(외장하드가 빠졌거나 마운트가 죽었을 수 있습니다). "
            f"터미널에서 `bml data` 로 확인한 뒤 `bml` 로 다시 띄우세요. "
            f"데이터는 지워지지 않았습니다. [{said}]"
        )
    else:
        detail = f"저장소를 읽지 못했습니다 — {said}"
    # 로그에도 남긴다.  화면에 한 줄이 떠도 `bml logs` 에 아무것도 없으면
    # 뒤늦게 원인을 찾을 근거가 사라진다.
    print(f"storage error on {request.url.path}: {said}", file=sys.stderr, flush=True)
    return JSONResponse(status_code=503, content={"detail": detail})


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
app.include_router(eis.router)
app.include_router(gitt.router)
app.include_router(exports.router)
app.include_router(presets.router)
app.include_router(activity.router)
app.include_router(changelog.router)
app.include_router(feedback.router)


def _served_commit() -> str:
    """이 서버가 **어느 코드로** 떠 있는가.

    `bml` 이 서버를 띄울 때 `.bml/server.head` 에 그때의 HEAD 를 적는다.  지금
    저장소의 HEAD 를 읽지 않는 이유가 여기 있다: `bml` 이 pull 만 하고 서버를
    다시 안 띄웠으면 둘이 다르고, **사람이 보는 화면을 정하는 것은 떠 있는
    쪽**이다.  저장소 쪽을 읽으면 아직 안 바뀐 화면을 두고 "갱신됐습니다" 라고
    말하게 된다.

    파일이 없으면 빈 문자열이다 (`make serve` 로 직접 띄운 경우).  모르면
    모른다고 하고, 화면은 아무 말도 안 한다 -- 없는 것을 지어내지 않는다.
    """
    try:
        return (REPO_ROOT / ".bml" / "server.head").read_text(
            encoding="utf-8").strip()[:40]
    except OSError:
        return ""


#: 이 프로세스의 이름표.  뜰 때 한 번 만들고, 죽을 때까지 안 바뀐다.
#:
#: **터널이 정말 이 서버로 오는지 확인하는 데 쓴다** (Codex #8).  공개 주소가
#: HTTP 200 을 줬다는 것만으로는 "이번에 연 터널이 열렸다" 가 증명되지 않는다.
#: 도메인이 아직 옛 VPS 를 가리키거나, 저쪽 5003 을 옛 터널이 잡고 있으면,
#: 이번 ssh 가 실패했는데도 **다른 워크벤치**가 200 을 준다.  화면은 열렸다고
#: 하고, 그 주소를 받은 사람은 남의 데이터를 본다 -- 우리 데이터인 줄 알고.
#: 그래서 여기 값과 공개 주소의 값이 같은지 본다.
#:
#: 비밀이 아니다.  ADR 0014 대로 `/api/health` 는 문 밖이라 암호를 모르는
#: 사람도 읽는데, 이 값으로 할 수 있는 일이 없어야 한다 -- 그래서 무작위이고,
#: 아무것도 열지 않으며, 서버를 다시 띄우면 버려진다.  예측 불가능할 필요도
#: 없다 (같은지 다른지만 본다).  `secrets` 를 쓰는 것은 그것이 이 자리에서
#: 가장 싼 무작위라서지, 이 값을 지켜야 해서가 아니다.
INSTANCE = secrets.token_hex(8)


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "instance": INSTANCE,
        "wrdkit": wrdkit_version,
        "data_dir": str(settings.data_dir),
        "max_upload_mb": settings.max_upload_bytes // (1024 * 1024),
    }


@app.get("/api/revision")
def read_revision() -> dict:
    """What the database is at, for anything that cannot hold a stream.

    떠 있는 코드도 함께 낸다.  `/api/health` 가 아니라 여기인 이유: health 는
    **문 밖**이라 (ADR 0014) 거기 담기는 것은 암호를 모르는 사람도 본다.
    커밋 해시가 비밀은 아니지만, 문 밖에 두는 것은 꼭 필요한 것만이어야 한다 --
    그 줄이 한 번 넓어지면 다음에 무엇을 더 넣을지 정할 근거가 없어진다.
    갱신 알림은 어차피 문 안에서 보는 화면의 일이다.
    """
    return {"revision": revision.value, "served_commit": _served_commit()}


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
            {"value": "dbw", "label": "Double Bacon-Watts (onset + point)"},
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
        target.mount("/assets", _ImmutableStatic(directory=dist / "assets"),
                     name="assets")

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
                return FileResponse(candidate, headers=_cache_headers(path))

        return FileResponse(root / "index.html", headers=_SHELL_CACHE)

    return True


class _ImmutableStatic(StaticFiles):
    """``/assets`` with the long cache its hashed filenames have earned.

    The mount handles these requests itself, so the header the SPA route sets
    never reaches them.  Left alone they get no ``Cache-Control`` at all and
    the browser revalidates a file that cannot have changed -- a round trip per
    bundle per page load, on a lab wifi, for nothing.
    """

    def file_response(self, *args, **kwargs):  # type: ignore[override]
        response = super().file_response(*args, **kwargs)
        response.headers.setdefault("Cache-Control", _ASSET_CACHE["Cache-Control"])
        return response


#: The one file that must never be served from cache without asking.
#:
#: Vite gives every build a new asset name (``index-DqARYaLz.js``), so the
#: bundles are safe to cache forever -- but ``index.html`` is what *names* them.
#: With no ``Cache-Control`` the browser falls back to heuristic freshness and
#: may keep serving the old shell, which keeps requesting the old bundle.  The
#: server then has the new build on disk and the screen still shows the old
#: one, with nothing anywhere saying so.
#:
#: This is the "pull 했는데 화면이 그대로다" failure, and it survives a server
#: restart, which is what makes it so hard to place: every other explanation
#: (stale checkout, stale build, wrong branch) is ruled out by evidence, and
#: the remaining one leaves no trace on the machine you are looking at.
#:
#: ``no-cache`` does not mean "do not store" -- it means "revalidate before
#: use".  The conditional request costs one round trip on an unchanged shell
#: (304, no body) and is the difference between shipping a fix and not.
_SHELL_CACHE = {"Cache-Control": "no-cache"}

#: Hashed assets, on the other hand, can be cached as long as the browser
#: likes: a changed file gets a changed name, so there is nothing to
#: invalidate.  A year is the conventional ceiling.
_ASSET_CACHE = {"Cache-Control": "public, max-age=31536000, immutable"}


def _cache_headers(path: str) -> dict[str, str]:
    """How long the browser may keep *path* without asking again.

    Anything whose name carries a content hash is immutable; everything else
    -- an icon, a manifest, a stray file dropped into the build -- gets the
    shell's treatment.  Guessing "immutable" for an unhashed file is the same
    bug as not setting a header on the shell, one directory down.
    """
    name = Path(path).name
    return _ASSET_CACHE if _HASHED.match(name) else _SHELL_CACHE


#: Vite's pattern: ``<name>-<hash>.<ext>``, hash being at least eight
#: characters of base64url.  Deliberately strict -- a false positive here
#: freezes a file in browsers for a year.
_HASHED = re.compile(r"^.+-[A-Za-z0-9_-]{8,}\.[A-Za-z0-9]+$")


mount_web(app, settings.web_dist)
