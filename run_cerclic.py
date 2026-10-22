"""Frozen-app entry point used by PyInstaller."""
import multiprocessing
import sys

from cerclic.app import main

if __name__ == "__main__":
    multiprocessing.freeze_support()
    sys.exit(main())
