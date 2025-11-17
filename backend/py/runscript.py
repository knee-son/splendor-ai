import sys

from utils import *

cmd = sys.argv[1]

if cmd not in globals():
    raise SystemExit(f"Unknown command: {cmd}")

fn = globals()[cmd]

print(f"Running {cmd} ...")
fn()
