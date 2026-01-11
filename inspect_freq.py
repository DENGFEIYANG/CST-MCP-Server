
import pycst
import inspect

try:
    print(f"frequency_range: {inspect.signature(pycst.frequency_range)}")
except Exception as e:
    print(f"Error: {e}")
