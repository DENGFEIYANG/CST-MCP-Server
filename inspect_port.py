
import pycst
import inspect

def print_sig(name, func):
    try:
        print(f"{name}: {inspect.signature(func)}")
    except Exception as e:
        print(f"{name}: {e}")

print_sig("waveguide_port", pycst.waveguide_port)
