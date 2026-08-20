import '@testing-library/jest-dom/vitest'

// uPlot measures its canvas; jsdom has no layout engine, so give ResizeObserver
// a stub and let the plot component render its empty state in tests.
class ResizeObserverStub {
  observe() {}
  unobserve() {}
  disconnect() {}
}
globalThis.ResizeObserver = globalThis.ResizeObserver ?? (ResizeObserverStub as never)
