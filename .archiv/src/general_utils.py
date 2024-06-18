import sys


def get_idx_to_process():
    # --idx_to_process=5
    for arg in sys.argv:
        if "--idx_to_process" in arg:
            return int(arg.split("=")[1])
    raise Exception("=== get_idx_to_process - no sys.argv ===")