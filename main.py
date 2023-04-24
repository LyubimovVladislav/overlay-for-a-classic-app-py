import win32api
import win32gui
import win32con
import asyncio


class OverlayWindow:

    def __init__(self):
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

    def wndProc(self, hWnd, message, wParam, lParam):
        if message == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        elif message == win32con.WM_ERASEBKGND:
            return False
        elif message == win32con.WM_PAINT:
            hdc, paintStruct = win32gui.BeginPaint(hWnd)
            global count
            count += 1
            brush = win32gui.CreateSolidBrush(win32api.RGB(255, 0, 0))
            win32gui.FillRect(hdc, (200, 200, 300, 300), brush)
            win32gui.DrawTextW(hdc, f'{1 + count}', len(f'{1 + count}'), (350, 350, 400, 400), win32con.DT_CENTER)
            win32gui.ReleaseDC(hWnd, hdc)
            win32gui.DeleteObject(brush)
            win32gui.EndPaint(hWnd, paintStruct)
            return 0
        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

    # def wndProc(self, hWnd, message, wParam, lParam):
    #     if message == win32con.WM_PAINT:
    #         hdc, paintStruct = win32gui.BeginPaint(hWnd)
    #         win32gui.EndPaint(hWnd, paintStruct)
    #         return 0
    #     elif message == win32con.WM_DESTROY:
    #         win32gui.PostQuitMessage(0)
    #         return 0
    #     else:
    #         return win32gui.DefWindowProc(hWnd, message, wParam, lParam)
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


if __name__ == "__main__":

    # def get_window_class_names():
    #     class_names = []
    #     def enum_callback(hwnd, _):
    #         class_name = win32gui.GetClassName(hwnd)
    #         class_names.append(class_name)
    #         return True
    #     win32gui.EnumWindows(enum_callback, None)
    #     return class_names
    # class_names = get_window_class_names()
    # for class_name in class_names:
    #     print(class_name)

    def draw_on_window(hwnd):
        global count
        count += 1
        hdc = win32gui.GetDC(hwnd)
        brush = win32gui.CreateSolidBrush(win32api.RGB(255, 0, 0))
        win32gui.FillRect(hdc, (200, 200, 300, 300), brush)
        win32gui.DrawTextW(hdc, f'{1 + count}', len(f'{1 + count}'), (350, 350, 400, 400), win32con.DT_CENTER)
        win32gui.ReleaseDC(hwnd, hdc)
        win32gui.DeleteObject(brush)


    async def redraw_window(hwnd):
        global overlay
        while True:
            if not win32gui.IsWindow(game_hwnd):
                print('no game hwnd, exiting')
                break
            message = win32gui.GetMessage(None, 0, 0)
            if message == -1:
                print('exiting')
                break
            # x, y, w, h = win32gui.GetWindowRect(game_hwnd)
            # win32gui.SetWindowPos(overlay.hWnd, win32con.HWND_TOPMOST, x, y, w, h, win32con.SWP_NOSENDCHANGING)
            draw_on_window(hwnd)
            # win32gui.InvalidateRect(overlay.hWnd, None, True)
            # win32gui.SendMessage(overlay.hWnd, win32con.WM_PAINT, 0, 0)
            # await asyncio.sleep(0.1)


    count = 1
    overlay = OverlayWindow()
    overlay.createWindow()
    game_hwnd = win32gui.FindWindow('MSPaintApp', None)
    if not win32gui.IsWindow(game_hwnd):
        print('no game hwnd, exiting')
        exit()

    x, y, w, h = win32gui.GetWindowRect(game_hwnd)
    win32gui.SetWindowPos(overlay.hWnd, win32con.HWND_TOPMOST, x, y, w, h, win32con.SWP_SHOWWINDOW)
    asyncio.run(redraw_window(game_hwnd))
