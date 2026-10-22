"""Tie helper processes (ffmpeg, PDF workers) to Cerclic's life: if Cerclic
ends, even killed by the Task Manager or an installer, Windows ends them too,
so nothing keeps running or writing in the background."""
from __future__ import annotations

import ctypes
import os
from ctypes import wintypes

_job = None


class _IO(ctypes.Structure):
    _fields_ = [(n, ctypes.c_ulonglong) for n in (
        "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
        "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]


class _Basic(ctypes.Structure):
    _fields_ = [("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", wintypes.DWORD),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", ctypes.c_size_t),
                ("PriorityClass", wintypes.DWORD),
                ("SchedulingClass", wintypes.DWORD)]


class _Extended(ctypes.Structure):
    _fields_ = [("BasicLimitInformation", _Basic), ("IoInfo", _IO),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t)]


JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000
JobObjectExtendedLimitInformation = 9
PROCESS_SET_QUOTA, PROCESS_TERMINATE = 0x0100, 0x0001


def kill_with_cerclic(pid: int) -> bool:
    """Put process `pid` in a job that Windows closes when Cerclic ends."""
    global _job
    if os.name != "nt" or not pid:
        return False
    try:
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateJobObjectW.restype = wintypes.HANDLE
        k32.OpenProcess.restype = wintypes.HANDLE
        k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        k32.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int,
                                                ctypes.c_void_p, wintypes.DWORD]
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        if _job is None:
            job = k32.CreateJobObjectW(None, None)
            if not job:
                return False
            info = _Extended()
            info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            if not k32.SetInformationJobObject(job, JobObjectExtendedLimitInformation,
                                               ctypes.byref(info), ctypes.sizeof(info)):
                k32.CloseHandle(job)
                return False
            _job = job
        h = k32.OpenProcess(PROCESS_SET_QUOTA | PROCESS_TERMINATE, False, int(pid))
        if not h:
            return False
        try:
            return bool(k32.AssignProcessToJobObject(_job, h))
        finally:
            k32.CloseHandle(h)
    except Exception:
        return False
