"""Entry point of Cerclic.exe (PyInstaller) and of `pythonw run_cerclic.py`."""
import multiprocessing
import os
import sys

if __name__ == "__main__":
    # A windowed app has no console: give libraries that print somewhere to
    # write (first, so that worker processes get it too).
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w", encoding="utf-8")
    multiprocessing.freeze_support()   # a worker process stops here
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from cerclic.launcher import main
    sys.exit(main())
