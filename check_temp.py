import tempfile
import os

# Try to find a writable temp dir
test_dirs = [
    "C:/Users/admin/AppData/Local/Temp",
    "C:/Windows/Temp",
    "C:/temp",
    "C:/tmp",
    os.path.expanduser("~"),
    "C:/Users/admin/.qclaw/workspace"
]

for d in test_dirs:
    try:
        test_file = os.path.join(d, f"test_{os.getpid()}.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print(f"WRITABLE: {d}")
    except Exception as e:
        print(f"NOT_WRITABLE: {d} - {e}")

# Try tempfile.gettempdir
try:
    td = tempfile.gettempdir()
    print(f"tempfile.gettempdir(): {td}")
    test_file = os.path.join(td, "test2.txt")
    with open(test_file, 'w') as f:
        f.write("test")
    os.remove(test_file)
    print(f"WRITABLE via tempfile: YES")
except Exception as e:
    print(f"tempfile.gettempdir() failed: {e}")
