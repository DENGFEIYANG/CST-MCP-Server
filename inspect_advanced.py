
import pycst
import inspect

def print_sig(name, func):
    try:
        print(f"{name}: {inspect.signature(func)}")
    except Exception as e:
        print(f"{name}: {e}")

print("--- Boolean Operations ---")
print_sig("add", pycst.add)
print_sig("subtract", pycst.subtract)
# intersect not seen on first pass, check if exists
try:
    print_sig("intersect", pycst.intersect)
except:
    pass

print("\n--- Transforms ---")
# Check for transform, translate, rotate
for name in dir(pycst):
    if "transform" in name or "trans" in name or "rot" in name or "scale" in name:
        print(f"Found potential transform: {name}")

print("\n--- Object Management ---")
print_sig("delete", getattr(pycst, "delete", None))
print_sig("rename", getattr(pycst, "rename", None))

print("\n--- MWS COM Inspection (Mock) ---")
# We can't easily inspect the COM object 'mws' dynamically without a running instance, 
# but let's check if pycst has wrappers for getting messages.
