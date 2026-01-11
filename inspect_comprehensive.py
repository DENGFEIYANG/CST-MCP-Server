
import pycst
import inspect

def print_sig(name, func):
    try:
        print(f"{name}: {inspect.signature(func)}")
    except Exception as e:
        print(f"{name}: {e}")

# Check for geometry
geo_types = ["sphere", "cone", "torus", "torus_circular", "rotation", "extrude"]
print("--- Geometry ---")
for g in geo_types:
    if hasattr(pycst, g):
        print_sig(g, getattr(pycst, g))
    else:
        print(f"{g}: Not found in pycst")

# Check for save
print("\n--- Project ---")
print_sig("save_project", getattr(pycst, "save_project", None))
print_sig("save_as_project", getattr(pycst, "save_as_project", None))
print_sig("backup", getattr(pycst, "backup", None))

# Check "transform" or similar in full dir
print("\n--- Searching for Transform/Rotate/Scale ---")
for d in dir(pycst):
    if "rot" in d.lower() or "trans" in d.lower() or "scale" in d.lower() or "mirr" in d.lower():
        print(f"Found: {d}")
        try:
             print_sig(d, getattr(pycst, d))
        except: pass
