import overlaywindow
import win32api
import win32gui
import win32con
import asyncio

if __name__ == "__main__":

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
            draw_on_window(hwnd)


    count = 0
    overlay = overlaywindow.OverlayWindow()
    overlay.createWindow()
    game_hwnd = win32gui.FindWindow('MSPaintApp', None)
    if not win32gui.IsWindow(game_hwnd):
        print('no game hwnd, exiting')
        exit()

    x, y, w, h = 0, 0, 0, 0
    win32gui.SetWindowPos(overlay.hWnd, win32con.HWND_TOPMOST, x, y, w, h, win32con.SWP_SHOWWINDOW)
    asyncio.run(redraw_window(game_hwnd))
