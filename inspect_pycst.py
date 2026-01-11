
import pycst
import inspect
import sys

print(f"Python executable: {sys.executable}")
print("Imported pycst successfully.")
print("pycst dir:", dir(pycst))
try:
    print("pycst file:", pycst.__file__)
except:
    pass
