import ctypes

from pykit.cursor import Cursor

user32 = ctypes.windll.user32
gdi = ctypes.windll.gdi32


def _make_COLORREF(r, g, b):
    return r | g << 8 | b << 16


def _unpack_COLORREF(colorref):
    return colorref & 0xFF, colorref >> 8 & 0xFF, colorref >> 16 & 0xFF


class Screen(object):
    def __init__(self):
        self._dc = user32.GetDC(0)
        self._cursor = Cursor()

    def get_pixel_color(self, x=None, y=None):
        if x or y is None:
            current_x, current_y = self._cursor.get_position()
            x = x or current_x
            y = y or current_y

        colorref = gdi.GetPixel(self._dc, x, y)
        return _unpack_COLORREF(colorref)

    def set_pixel_color(self, r, g, b, x=None, y=None):
        if x or y is None:
            current_x, current_y = self._cursor.get_position()
            x = x or current_x
            y = y or current_y

        colorref = _make_COLORREF(r, g, b)
        gdi.SetPixel(self._dc, x, y, colorref)
