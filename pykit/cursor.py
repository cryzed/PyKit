import ctypes

from pykit.structures import POINT


user32 = ctypes.windll.user32
gdi = ctypes.windll.gdi32


class Cursor(object):
    def __init__(self):
        self._point = POINT()
        self._point_pointer = ctypes.pointer(self._point)
        self._screen_dc = user32.GetDC(0)

    @staticmethod
    def _make_COLORREF(r, g, b):
        return r | g << 8 | b << 16

    @staticmethod
    def _unpack_COLORREF(colorref):
        return colorref & 0xFF, colorref >> 8 & 0xFF, colorref >> 16 & 0xFF

    @staticmethod
    def set_position(x, y):
        user32.SetCursorPos(x, y)

    def set_position_relative(self, x, y):
        current_x, current_y = self.get_position()
        self.set_position(current_x + x, current_y + y)

    def get_position(self):
        user32.GetCursorPos(self._point_pointer)
        return self._point.x, self._point.y

    def get_position_relative(self, x, y):
        current_x, current_y = self.get_position()
        return current_x - x, current_y - y

    def get_pixel_color(self, x=None, y=None):
        if x or y is None:
            current_x, current_y = self.get_position()
            x = x or current_x
            y = y or current_y

        colorref = gdi.GetPixel(self._screen_dc, x, y)
        return self._unpack_COLORREF(colorref)

    def set_pixel_color(self, r, g, b, x=None, y=None):
        if x or y is None:
            current_x, current_y = self.get_position()
            x = x or current_x
            y = y or current_y

        colorref = self._make_COLORREF(r, g, b)
        gdi.SetPixel(self._screen_dc, x, y, colorref)
