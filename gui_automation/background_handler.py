# Made by Marcos Boggia
import io
import cv2
import numpy as np
from PIL import Image
import win32gui
import win32ui
from ctypes import windll
from time import sleep
from gui_automation.handler import Handler


class BackgroundHandlerWin32(Handler):
    """
    Handler only for Windows. It can work on background(not viewable) apps. It needs the app name/window name.
    If needed you can pass the full hierarchy names as arguments to select a specific UI element.
    Eg: BackgroundHandlerWin32('window_name', 'main_ui_element', 'child_ui_element')
    If the element is not found raises ElementNotFound exception.
    """

    def __init__(self, app_name, *args):
        """

        :param app_name: app or window name of the desired app to be controlled.
        :param args: if you need to control a specific UI element, you can set these *args to determine the UI hierarchy
        names. Currently the condition asks if given name is 'in' the element name. Should be replaced with regexp in
        the future.
        """
        self.x_dis = 0
        self.y_dis = 0
        result = self.get_gui_elem(app_name, *args)
        if result:
            self.hwnd = result
            self.img_hwnd = result
        else:
            raise ElementNotFound

    def set_img_hwnd(self, app_name, *args, x_dis=0, y_dis=0):
        """
        It is possible that the handler used to control the app returns a black screen or similar.
        This function allows to set a different handler to get the screenshot of that GUI.
        Since there might be some positional difference between the original handler and the one used to obtain the
        image, x_dis and y_dis parameters can be used to fix these displacement.

        :param app_name: app or window name of the desired app to be controlled.
        :param args: if you need to control a specific UI element, you can set these *args to determine the UI hierarchy
        names. Currently the condition asks if given name is 'in' the element name. Should be replaced with regexp in
        the future.
        :param x_dis: displacement in pixels in between the handlers for the X axis.
        :param y_dis: same as x_dis but for the Y axis.
        :return:
        """
        result = self.get_gui_elem(app_name, *args)
        if result:
            self.img_hwnd = result
            self.x_dis = x_dis
            self.y_dis = y_dis
        else:
            raise ElementNotFound

    def screenshot(self):
        """
        Screenshot for background Win32 apps.
        :return: screen as OpenCV image format.
        """

        # OBTAIN IMAGE OF THE WINDOW SCREEN
        left, top, right, bot = win32gui.GetWindowRect(self.img_hwnd.handle)
        w = right - left
        h = bot - top
        hwnd_dc = win32gui.GetWindowDC(self.img_hwnd.handle)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        save_bit_map = win32ui.CreateBitmap()
        save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(save_bit_map)
        result = windll.user32.PrintWindow(self.img_hwnd.handle, save_dc.GetSafeHdc(), 1)
        if result == 0:
            return False
        bmpinfo = save_bit_map.GetInfo()
        bmpstr = save_bit_map.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        win32gui.DeleteObject(save_bit_map.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.img_hwnd.handle, hwnd_dc)
        # CONVERT IT TO OPENCV FORMAT
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img

    def click(self, x, y, clicks=1):
        for _ in range(clicks):
            print(f"HANDLER clicked x: {x + self.x_dis} y: {y + self.y_dis}")
            self.hwnd.click(coords=(x + self.x_dis, y + self.y_dis))

    def move(self, x, y):
        self.hwnd.move_mouse(coords=(x + self.x_dis, y + self.y_dis))

    def hold_click(self, x, y, time):
        refresh_rate = 0.05
        self.hwnd.press_mouse(coords=(x + self.x_dis, y + self.y_dis))
        while time > 0:
            sleep(refresh_rate)
            self.hwnd.move_mouse(coords=(x + self.x_dis, y + self.y_dis))
            time -= refresh_rate

        self.hwnd.release_mouse(coords=(x + self.x_dis, y + self.y_dis))

    def drag_click(self, start_x, start_y, end_x, end_y):
        self.hwnd.drag_mouse(press_coords=(start_x + self.x_dis, start_y + self.y_dis),
                             release_coords=(end_x + self.x_dis, end_y + self.y_dis))

    def press_key(self, key):
        print("Not implemented yet")

    def press_hotkey(self, *keys):
        print("Not implemented yet")

    def write_string(self, key, interval=0):
        print("Not implemented yet")

    @staticmethod
    def get_gui_elem(app_name, *args):
        """

        :param app_name: name of the app. For eg: for Paint is MSPaintApp.
        :param args: name of the descendant elements ordered in hierarchy level.
        :return: returns the HWNDWrapper from pywinauto of the Gui element if found. Otherwise returns False.

        Due to some incompatibility between PyAutoGui and pywinauto, if pywinauto is imported, pyautogui stops working.
        That's why it is imported only when necessary(if this function is called).
        After this import, PyAutoGui will not continue to work. Which means foreground handler won't work neither.
        """
        from pywinauto.controls import hwndwrapper

        data = [elem for elem in args]
        data.insert(0, app_name)
        windows_list = []

        def _append(hwnd, _):
            windows_list.append(hwndwrapper.HwndWrapper(hwnd))

        win32gui.EnumWindows(_append, [])

        for elem in windows_list:
            result = BackgroundHandlerWin32.process_element(elem, data, 0)
            if result:
                return result
        return False

    @staticmethod
    def process_element(elem, data, i):
        """

        :param elem: HWNDWrapper element to start recursive search
        :param data: names of the elements ordered hierarchically.
        :param i: index of the data array.
        :return: returns the HWNDWrapper from pywinauto of the Gui element if found. Otherwise returns False.
        """
        name1 = elem.friendlyclassname
        name2 = elem.element_info.name
        if (name1 is not None and data[i] in name1) or (name2 is not None and data[i] in name2):
            if i == len(data) - 1:
                return elem
            else:
                children = elem.children()
                BackgroundHandlerWin32.load_children(children)
                if children:
                    for next_child in children:
                        hwnd = BackgroundHandlerWin32.process_element(next_child, data, i + 1)
                        if hwnd:
                            return hwnd
        return False

    @staticmethod
    def load_children(children):
        """
        WORKAROUND for children not being loaded. Rarely, printing them fix this issue. Maybe its some lazy loading.
        This supress stdout when printing.
        :param children:
        :return:
        """
        from contextlib import redirect_stdout
        trap = io.StringIO()
        with redirect_stdout(trap):
            print(children)


class ElementNotFound(Exception):
    pass
