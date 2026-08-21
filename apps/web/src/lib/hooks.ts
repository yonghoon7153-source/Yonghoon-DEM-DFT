import { useCallback, useEffect, useRef, useState } from 'react'

import { ApiError } from './api'

export interface AsyncState<T> {
  data: T | null
  error: string | null
  loading: boolean
  reload: () => void
}

/** Run an async loader, keeping the last good value while a reload is in flight.
 *
 * Keeping stale data visible matters here: changing a mass re-fetches the whole
 * cycle table, and blanking the screen on every keystroke would make the panel
 * unusable.
 */
export function useAsync<T>(
  loader: () => Promise<T>,
  deps: unknown[],
  options: { enabled?: boolean; refreshMs?: number } = {},
): AsyncState<T> {
  const enabled = options.enabled ?? true
  const refreshMs = options.refreshMs ?? 0
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(enabled)
  const [nonce, setNonce] = useState(0)
  const latest = useRef(0)

  useEffect(() => {
    if (!enabled) {
      setLoading(false)
      return
    }
    const ticket = ++latest.current
    setLoading(true)
    loader()
      .then((value) => {
        if (ticket !== latest.current) return // a newer request already won
        setData(value)
        setError(null)
      })
      .catch((cause: unknown) => {
        if (ticket !== latest.current) return
        setError(cause instanceof ApiError ? cause.message : String(cause))
      })
      .finally(() => {
        if (ticket === latest.current) setLoading(false)
      })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, nonce, enabled])

  const reload = useCallback(() => setNonce((n) => n + 1), [])

  // Poll, when asked.  One central instance means somebody else's upload is
  // already in the database the moment it lands -- but the page that is open
  // does not know that, so a screen left on the bench shows yesterday until
  // it is reloaded by hand.
  //
  // Paused while the tab is hidden: a cell runs for days, and a browser left
  // open overnight would otherwise ask a question a thousand times that
  // nobody is there to read the answer to.  `visibilitychange` also fires on
  // the way back, which doubles as the refresh you want when you return.
  useEffect(() => {
    if (!enabled || refreshMs <= 0) return
    const tick = () => {
      if (!document.hidden) setNonce((n) => n + 1)
    }
    const timer = setInterval(tick, refreshMs)
    document.addEventListener('visibilitychange', tick)
    return () => {
      clearInterval(timer)
      document.removeEventListener('visibilitychange', tick)
    }
  }, [enabled, refreshMs])

  return { data, error, loading, reload }
}

/** Delay a fast-changing value so typing a mass does not fire a request per key. */
export function useDebounced<T>(value: T, delayMs = 350): T {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delayMs)
    return () => clearTimeout(timer)
  }, [value, delayMs])
  return debounced
}

/** A piece of UI state that survives a reload. */
export function useStickyState<T>(key: string, initial: T): [T, (value: T) => void] {
  const [value, setValue] = useState<T>(() => {
    try {
      const stored = window.localStorage.getItem(key)
      return stored === null ? initial : (JSON.parse(stored) as T)
    } catch {
      return initial
    }
  })
  const update = useCallback(
    (next: T) => {
      setValue(next)
      try {
        window.localStorage.setItem(key, JSON.stringify(next))
      } catch {
        /* private mode; the value simply will not persist */
      }
    },
    [key],
  )
  return [value, update]
}

/** Track an element's width so a plot can resize with its container. */
export function useElementWidth<T extends HTMLElement>(): [React.RefObject<T>, number] {
  const ref = useRef<T>(null)
  const [width, setWidth] = useState(0)

  useEffect(() => {
    const element = ref.current
    if (!element) return
    const observer = new ResizeObserver((entries) => {
      const entry = entries[0]
      if (entry) setWidth(Math.floor(entry.contentRect.width))
    })
    observer.observe(element)
    setWidth(element.clientWidth)
    return () => observer.disconnect()
  }, [])

  return [ref, width]
}
