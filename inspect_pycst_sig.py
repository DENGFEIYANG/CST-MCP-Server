
import pycst
import inspect

def print_sig(name, func):
    try:
        print(f"{name}: {inspect.signature(func)}")
        print(f"{name} doc: {func.__doc__}")
    except Exception as e:
        print(f"{name}: {e}")

print_sig("start", pycst.start)
print_sig("session", pycst.session)
print_sig("save_project", pycst.save_project)
print_sig("time_domain_solver", pycst.time_domain_solver)
print_sig("export_touchstone", pycst.export_touchstone)
print_sig("quit_project", pycst.quit_project)
