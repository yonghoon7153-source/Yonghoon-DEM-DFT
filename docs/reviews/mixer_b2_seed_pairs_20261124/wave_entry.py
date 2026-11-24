"""Entry point used by the frozen per-arm monitor subprocess."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import repeat
if __name__=="__main__":
    mode,arm,job=sys.argv[1:]
    repeat.need(mode=="monitor","monitor action required")
    repeat.monitor(HERE.name,arm,job)
