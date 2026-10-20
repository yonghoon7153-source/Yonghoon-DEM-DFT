"""Windows diagnostic adapter: only unavailable peak-memory field, no numerics."""
import types
RUSAGE_SELF = 0
def getrusage(_):
    return types.SimpleNamespace(ru_maxrss=float('nan'))
