import os,sys
_here=os.path.dirname(__file__)
sys.path[:]=[p for p in sys.path if os.path.abspath(p)!=_here]
