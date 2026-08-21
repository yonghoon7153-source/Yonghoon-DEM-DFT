import '@testing-library/jest-dom/vitest'

// uPlot measures its canvas; jsdom has no layout engine, so give ResizeObserver
// a stub and let the plot component render its empty state in tests.
class ResizeObserverStub {
  observe() {}
  unobserve() {}
  disconnect() {}
}
globalThis.ResizeObserver = globalThis.ResizeObserver ?? (ResizeObserverStub as never)

// jsdom does not implement matchMedia, and uPlot calls it at import time to
// track the device pixel ratio.  A test file that imports Plot -- directly or
// through a page -- otherwise fails before a single test runs.
if (typeof window !== 'undefined' && !window.matchMedia) {
  window.matchMedia = ((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener() {},
    removeListener() {},
    addEventListener() {},
    removeEventListener() {},
    dispatchEvent: () => false,
  })) as never
}
