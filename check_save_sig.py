
import pycst
import inspect

try:
    print(f"save_as_project: {inspect.signature(pycst.save_as_project)}")
except Exception as e:
    print(e)
