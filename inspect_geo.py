
import pycst
import inspect

def print_sig(name, func):
    try:
        print(f"{name}: {inspect.signature(func)}")
        # print(f"{name} doc: {func.__doc__}")
    except Exception as e:
        print(f"{name}: {e}")

print_sig("brick", pycst.brick)
print_sig("cylinder", pycst.cylinder)
print_sig("sphere", pycst.sphere)
print_sig("material", pycst.material)
print_sig("pick_face", pycst.pick_face)
print_sig("discrete_port", pycst.discrete_port)
