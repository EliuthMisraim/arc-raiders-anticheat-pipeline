import traceback
import sys
import os

log_file = "debug_log.txt"

def log(msg):
    with open(log_file, "a") as f:
        f.write(str(msg) + "\n")
    print(msg)

if os.path.exists(log_file):
    os.remove(log_file)

try:
    log(f"PYTHONPATH: {sys.path}")
    log(f"CWD: {os.getcwd()}")
    import src.model
    log("SUCCESS")
except Exception:
    error = traceback.format_exc()
    log(error)
    sys.exit(1)
