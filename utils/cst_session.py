
import pycst
import sys

# Global state to hold the CST instance (singleton)
_cst_instance = None

def get_cst():
    global _cst_instance
    if _cst_instance is None:
        print("Starting CST Studio...", file=sys.stderr)
        # pycst.start() loads a local CST session. 
        _cst_instance = pycst.start()
    return _cst_instance
