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


from ctypes import Structure, windll, c_uint, sizeof, byref



def get_idle_duration():
    GetLastInputInfo = ctypes.windll.user32.GetLastInputInfo
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [
            ('cbSize', c_uint),
            ('dwTime', c_uint),
        ]
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0
