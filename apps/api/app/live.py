"""One number that says "something changed", and a stream that announces it.

The workbench is one instance that several people share (ADR 0011), so a page
somebody left open is a page showing what the database said when they opened
it.  Polling closes that gap, and polling every screen every few seconds asks
the same question a thousand times a day to hear "no" -- on a laptop, over
wifi, for a cell that changes twice an hour.

Instead there is a single counter.  Every write bumps it; browsers hold one
event stream and re-fetch what they are showing when the number moves.  The
counter is deliberately *not* an event log: it says that something changed,
not what, so no endpoint has to describe its own changes and nothing goes
stale when a new one is added.  The cost is that one edit re-fetches slightly
more than it strictly must, which for a lab-sized dataset is nothing.

This lives in process memory, which is correct for exactly one server process
-- what ``bml`` runs.  Under several uvicorn workers each would keep its own
count and browsers would see whichever they were routed to; the fix then is a
shared broadcast (Redis, postgres LISTEN), not a bigger number here.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field


@dataclass
class Revision:
    """A monotonic counter with a way to wait for it to move."""

    value: int = 0
    #: Replaced -- not merely set -- on every bump.  A waiter holds the old
    #: event object, so swapping in a fresh one wakes everybody exactly once
    #: without a window where a bump lands between "check" and "wait" and is
    #: therefore missed.
    _changed: asyncio.Event = field(default_factory=asyncio.Event)

    def bump(self) -> int:
        self.value += 1
        previous, self._changed = self._changed, asyncio.Event()
        previous.set()
        return self.value

    async def wait_past(self, seen: int, timeout: float) -> int:
        """The current value once it is beyond *seen*, or *seen* on timeout.

        Returning on timeout rather than blocking forever is what lets the
        stream send a heartbeat: a connection that says nothing for minutes is
        one that proxies and phone radios quietly drop, and the browser only
        finds out when somebody wonders why the screen stopped updating.
        """
        if self.value > seen:
            return self.value
        waiter = self._changed
        try:
            await asyncio.wait_for(waiter.wait(), timeout)
        except (asyncio.TimeoutError, TimeoutError):
            return seen
        return self.value


#: The process-wide counter.
revision = Revision()

#: Methods that can change something worth telling other people about.
WRITE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})

#: Response header carrying the revision a write produced.  The browser that
#: made the write already has the answer, so it uses this to ignore its own
#: announcement instead of immediately re-fetching what it just sent.
REVISION_HEADER = "X-Workbench-Revision"

#: How long a stream waits before sending a heartbeat instead of an update.
HEARTBEAT_SECONDS = 20.0


async def revision_stream(is_disconnected, *, heartbeat: float = HEARTBEAT_SECONDS):
    """The server-sent-events body: one line per change, plus heartbeats.

    Takes ``is_disconnected`` rather than a request so the loop can be run and
    stopped in a test.  Streaming an endless generator through a test client
    hangs it -- the client waits for a body that never ends, and the server
    only learns the client left by asking, which the client never gets far
    enough to answer.
    """
    # The opening line tells a browser that just connected where the database
    # already is.  Without it a page opened during somebody else's edit sits
    # one revision behind until the *next* edit happens.
    seen = revision.value
    yield f"event: revision\ndata: {seen}\n\n"
    while not await is_disconnected():
        current = await revision.wait_past(seen, heartbeat)
        if current > seen:
            seen = current
            yield f"event: revision\ndata: {seen}\n\n"
        else:
            # A comment line: valid SSE, ignored by the client, and enough
            # traffic to keep proxies and sleeping radios from dropping a
            # connection that has been silent for minutes.
            yield ": keep-alive\n\n"


def should_bump(method: str, status_code: int, path: str) -> bool:
    """Did this request change something other people should hear about?

    Failed writes are excluded: a 422 from a bad mass changed nothing, and
    bumping would make every open page re-fetch because one person typed a
    letter into a number field.

    Exports are excluded too even though they are GETs today -- the rule is
    about writes, and this keeps the answer readable in one place.
    """
    return method.upper() in WRITE_METHODS and status_code < 400 \
        and path.startswith("/api/")
