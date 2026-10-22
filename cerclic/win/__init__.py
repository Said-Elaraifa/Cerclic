"""Windows-only glue: global mouse hook, Explorer selection, autostart.

These modules import ctypes/pywin32 and only run on Windows. They are kept out
of the pure `actions` package so the engine stays testable everywhere.
"""
