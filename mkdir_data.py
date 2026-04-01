import os
workspace = "C:/Users/admin/.qclaw/workspace"
try:
    os.makedirs(os.path.join(workspace, "data"), exist_ok=True)
    print("OK")
except Exception as e:
    print(f"Error: {e}")
