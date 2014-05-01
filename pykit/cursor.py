import ctypes

from pykit.structures import POINT

user32 = ctypes.windll.user32


class Cursor(object):
    def __init__(self):
        self._point = POINT()
        self._point_pointer = ctypes.pointer(self._point)

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
