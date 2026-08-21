/** One connection to the server's "something changed" stream.
 *
 * The workbench is one instance that several people share, so what another
 * person just uploaded, renamed or re-weighed should appear on this screen
 * without anybody pressing reload.
 *
 * One subscription for the whole tab, not one per screen: a page shows half a
 * dozen lists at once, and six event streams to say the same thing six times
 * is six connections a browser will not give you anyway (it caps them per
 * origin, and the seventh request on the page then blocks).
 *
 * What arrives is a number, never a description of what changed.  Screens
 * re-fetch what they are showing when it moves.  That is slightly more
 * fetching than strictly needed and it means no screen can be forgotten when
 * a new kind of edit is added -- which is the failure that would be hardest
 * to notice, because only one kind of edit would go missing.
 */

/** Response header a write carries back: the revision it produced. */
export const REVISION_HEADER = 'x-workbench-revision'

type Listener = (revision: number) => void

const listeners = new Set<Listener>()
let current = 0
/** The highest revision this tab caused itself.  Its own writes already
 *  updated the screen that made them, so re-fetching for them is churn. */
let mine = 0
let source: EventSource | null = null
let poll: ReturnType<typeof setInterval> | null = null
let retryMs = 1000

function announce(next: number) {
  if (next <= current) return
  current = next
  if (next <= mine) return
  for (const listener of listeners) listener(next)
}

/** Record that this tab produced a revision, so its own echo is ignored.
 *
 * Tolerant of a response with no headers to read.  This runs on the path
 * every single request takes, and skipping an optimisation is the right
 * failure -- throwing here would turn "the echo could not be suppressed" into
 * "the save did not happen", which is the same shape as a lost edit. */
export function noteOwnWrite(response: {
  headers?: { get(name: string): string | null }
}) {
  const header = response.headers?.get(REVISION_HEADER)
  if (!header) return
  const value = Number(header)
  if (Number.isFinite(value) && value > mine) mine = value
}

/** Ask the server where things are, for browsers or proxies that break SSE. */
async function pollOnce() {
  try {
    const response = await fetch('/api/revision')
    if (!response.ok) return
    const body = (await response.json()) as { revision?: number }
    if (typeof body.revision === 'number') announce(body.revision)
  } catch {
    /* offline; the next tick tries again */
  }
}

function startPolling() {
  if (poll) return
  // Slower than the stream by design: this path exists because the stream
  // could not be had, and a fallback that hammers the server is worse than a
  // screen that is fifteen seconds behind.
  poll = setInterval(() => {
    if (!document.hidden) void pollOnce()
  }, 15_000)
  void pollOnce()
}

function connect() {
  if (source || typeof EventSource === 'undefined') {
    if (!source) startPolling()
    return
  }
  const stream = new EventSource('/api/events')
  source = stream
  stream.addEventListener('revision', (event) => {
    retryMs = 1000 // the connection works; forget any earlier backoff
    const value = Number((event as MessageEvent<string>).data)
    if (Number.isFinite(value)) announce(value)
  })
  stream.onerror = () => {
    // EventSource reconnects on its own, but not when the server is gone for
    // good (a laptop that closed, a restart mid-deploy).  Close and come back
    // with a growing delay so a downed server is not hammered by every tab.
    stream.close()
    if (source === stream) source = null
    if (!listeners.size) return
    retryMs = Math.min(retryMs * 2, 30_000)
    setTimeout(connect, retryMs)
  }
}

/** Hear about changes.  Returns the unsubscribe. */
export function subscribe(listener: Listener): () => void {
  listeners.add(listener)
  connect()
  return () => {
    listeners.delete(listener)
    if (listeners.size) return
    source?.close()
    source = null
    if (poll) {
      clearInterval(poll)
      poll = null
    }
  }
}

/** The revision this tab has heard about. */
export function currentRevision(): number {
  return current
}

/** Test seam: forget everything between cases. */
export function _reset() {
  listeners.clear()
  source?.close()
  source = null
  if (poll) clearInterval(poll)
  poll = null
  current = 0
  mine = 0
  retryMs = 1000
}
