"""Reduce a curve to a plottable number of points without losing its shape.

A single 0.2C cycle is a few thousand samples and a 1000-cycle run is
hundreds of thousands.  Sending all of it to a browser is wasteful, but
naive striding flattens exactly the features an electrochemist looks for --
plateau knees, the CV taper, dQ/dV peaks.  Largest-Triangle-Three-Buckets
keeps them because it selects, per bucket, the point that spans the largest
triangle with its neighbours.
"""

from __future__ import annotations

import numpy as np

__all__ = ["lttb", "lttb_indices"]


def lttb_indices(x: np.ndarray, y: np.ndarray, threshold: int) -> np.ndarray:
    """Indices of the *threshold* points that best preserve the curve."""
    n = len(x)
    if threshold >= n or threshold < 3:
        return np.arange(n)

    # First and last points are always kept; the rest are bucketed evenly.
    bucket_edges = np.linspace(1, n - 1, threshold - 1).astype(np.int64)
    selected = np.empty(threshold, dtype=np.int64)
    selected[0] = 0
    selected[-1] = n - 1

    previous = 0
    for i in range(threshold - 2):
        start, stop = bucket_edges[i], bucket_edges[i + 1]
        if stop <= start:
            selected[i + 1] = start
            previous = start
            continue

        next_start, next_stop = bucket_edges[i + 1], bucket_edges[i + 2] if i + 2 < len(bucket_edges) else n
        if next_stop <= next_start:
            next_stop = min(next_start + 1, n)
        avg_x = float(np.mean(x[next_start:next_stop]))
        avg_y = float(np.mean(y[next_start:next_stop]))

        chunk_x = x[start:stop]
        chunk_y = y[start:stop]
        areas = np.abs(
            (x[previous] - avg_x) * (chunk_y - y[previous])
            - (x[previous] - chunk_x) * (avg_y - y[previous])
        )
        chosen = start + int(np.argmax(areas))
        selected[i + 1] = chosen
        previous = chosen

    return np.unique(selected)


def lttb(x: np.ndarray, y: np.ndarray, threshold: int) -> tuple[np.ndarray, np.ndarray]:
    """Downsample a curve to at most *threshold* points."""
    if threshold <= 0 or len(x) <= threshold:
        return x, y
    keep = lttb_indices(np.asarray(x, dtype=np.float64),
                        np.asarray(y, dtype=np.float64), threshold)
    return x[keep], y[keep]
