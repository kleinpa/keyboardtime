import sys
import os.path
import ctypes
import ctypes.wintypes

def window_name():
    GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow
    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    GetProcessImageFileName = ctypes.windll.psapi.GetProcessImageFileNameA
    OpenProcess = ctypes.windll.kernel32.OpenProcess

    hwnd = GetForegroundWindow()
    pid = ctypes.c_ulong()
    GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

    MAX_PATH = 260
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

    hProcess = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)

    path = (ctypes.c_char*MAX_PATH)()
    GetProcessImageFileName(hProcess, path, MAX_PATH)>0

    return os.path.splitext(os.path.basename(path.value))[0].decode('UTF-8')

def get_idle_duration():
    GetLastInputInfo = ctypes.windll.user32.GetLastInputInfo
    GetTickCount = ctypes.windll.kernel32.GetTickCount

    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [
            ('cbSize', ctypes.c_uint),
            ('dwTime', ctypes.c_uint),
        ]
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
    GetLastInputInfo(ctypes.byref(lastInputInfo))
    millis = GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0
