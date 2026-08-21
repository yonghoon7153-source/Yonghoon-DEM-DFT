"""Who is doing this.

**This is attribution, not authentication.**  The name arrives in a header the
browser sets from what somebody typed once, and nothing checks it.  Anyone on
the network can claim any name, and that is the correct trade for a lab
instrument on a private network: the question people actually have is "who
changed this cell's mass", not "prove you are you".

Passwords would answer a question nobody here is asking, and the cost is real
-- a login nobody needs is a login somebody shares, writes on a sticky note,
or gets locked out of at 2am with a cell mid-cycle.  If this ever leaves the
lab network that calculus changes completely, and the fix is a real identity
provider in front, not a password column here.

The name lives in a ``ContextVar`` because the alternative is threading an
actor argument through every route, dependency and service.  One of them gets
missed, and the record it writes is anonymous with nothing to say it should
not have been.
"""

from __future__ import annotations

from contextvars import ContextVar
from urllib.parse import unquote

#: Header the browser sets.  Not a cookie: nothing here is a session, and a
#: cookie would ride along on requests this app does not control.
ACTOR_HEADER = "X-Workbench-User"

#: Longer than any real name, short enough that a stray blob cannot fill a
#: column.  Names are shown in tables, so length is a layout question too.
MAX_ACTOR = 40

_actor: ContextVar[str] = ContextVar("workbench_actor", default="")


def clean_actor(raw: str | None) -> str:
    """A name fit to store, or "" when there is nothing usable.

    Control characters are stripped rather than rejected: this value is
    rendered in tables and written into a header, and a newline in either
    place is somebody else's bug report.  An unusable name degrades to
    anonymous -- a write must never fail because a display name was odd.
    """
    if not raw:
        return ""
    cleaned = "".join(character for character in raw if character.isprintable())
    return cleaned.strip()[:MAX_ACTOR]


def decode_actor(raw: str | None) -> str:
    """Undo the percent-encoding the browser had to apply.

    HTTP header values are bytes in the ASCII/latin-1 range, so a Korean name
    cannot travel in one as itself -- the request is rejected before it leaves
    the browser.  The client percent-encodes; this undoes it.

    A plain ASCII name passes through unchanged, and so does a name with a
    stray ``%`` in it (``unquote`` leaves an invalid escape alone), so this is
    safe to run on anything that arrives.
    """
    if not raw:
        return ""
    try:
        return unquote(raw, errors="replace")
    except (ValueError, UnicodeDecodeError):
        return raw


def set_actor(raw: str | None) -> str:
    value = clean_actor(decode_actor(raw))
    _actor.set(value)
    return value


def current_actor() -> str:
    """Who is writing, or "" when nobody said."""
    return _actor.get()
