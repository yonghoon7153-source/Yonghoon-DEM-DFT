"""Windows-only report field adapter. No numerical/model behavior supplied."""
import types
RUSAGE_SELF = 0
def getrusage(_):
    return types.SimpleNamespace(ru_maxrss=float('nan'))
