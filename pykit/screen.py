import ctypes

from pykit.cursor import Cursor

user32 = ctypes.windll.user32
gdi = ctypes.windll.gdi32


def _make_COLORREF(color):
    r, g, b = color
    return r | g << 8 | b << 16


def _unpack_COLORREF(colorref):
    return colorref & 0xFF, colorref >> 8 & 0xFF, colorref >> 16 & 0xFF


class Screen(object):
    def __init__(self):
        self._dc = user32.GetDC(0)
        self._cursor = Cursor()
        self.width = user32.GetSystemMetrics(0)
        self.height = user32.GetSystemMetrics(1)

    def get_pixel_color(self, position=None):
        position = position or self._cursor.get_position()
        colorref = gdi.GetPixel(self._dc, *position)
        return _unpack_COLORREF(colorref)

    # TODO: This is terribly inefficient -- needs to be improved by taking a
    # screenshot of the region and searching for the correct pixel (PIL?)
    def find_pixel(self, color, region=None, limit=1, step_x=1, step_y=1):
        locations = []
        region = region or ((0, 0), (self.width - 1, self.height - 1))

        x1, y1 = region[0]
        x2, y2 = region[1]
        x, y = x1, y1

        while (not limit or len(locations) < limit) and y <= y2:
            print x, y
            color_ = self.get_pixel_color((x, y))
            if color_ == color:
                locations.append((x, y))

            if x == x2:
                x = x1
                y += step_y

            x += step_x
        return locations

    def set_pixel_color(self, color, position=None):
        position = position or self._cursor.get_position()
        colorref = _make_COLORREF(color)
        gdi.SetPixel(self._dc, position[0], position[1], colorref)
