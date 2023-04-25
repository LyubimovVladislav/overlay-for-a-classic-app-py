import win32api
import win32gui
import win32con


class OverlayWindow:

    def __init__(self):
        self.height = None
        self.width = None
        self.hInstance = win32api.GetModuleHandle(None)
        className = 'OverlayWindowClass'
        wndClass = win32gui.WNDCLASS()
        wndClass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wndClass.lpfnWndProc = self.wndProc
        wndClass.hInstance = self.hInstance
        wndClass.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
        wndClass.hbrBackground = win32gui.GetStockObject(win32con.NULL_BRUSH)
        wndClass.lpszClassName = className
        self.wndClassAtom = win32gui.RegisterClass(wndClass)
        self.hWnd = None
        self.count = 1

    def wndProc(self, hWnd, message, wParam, lParam):
        if message == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

    def createWindow(self):
        exStyle = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST | win32con.WS_EX_TOOLWINDOW | win32con.WS_EX_NOACTIVATE
        style = win32con.WS_POPUP | win32con.WS_DISABLED | win32con.WS_CLIPSIBLINGS
        self.hWnd = win32gui.CreateWindowEx(exStyle,
                                            self.wndClassAtom,
                                            None,
                                            style,
                                            0, 0, 0, 0,
                                            None,
                                            None,
                                            self.hInstance,
                                            None)
        win32gui.SetLayeredWindowAttributes(self.hWnd, 0, 0, win32con.LWA_ALPHA | win32con.LWA_COLORKEY)
