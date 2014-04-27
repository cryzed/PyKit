import struct
import threading

from winappdbg.win32 import PVOID
from pykit.process import Process

import pyHook
import pythoncom


PATH = r'C:\Program Files (x86)\Carpe Fulgur\Recettear - An Item Shops Tale\recettear.exe'
MOVE_MONSTER_FUNCTION_ADDRESS = 0x00430653
CHARACTER_SPAWN_X_ADDRESS = 0x0438B46E
CHARACTER_SPAWN_Y_ADDRESS = 0x0438B476
CHARACTER_POSITION_X_ADDRESS = 0x056DA45A
CHARACTER_POSITION_Y_ADDRESS = 0x056DA462


class start_new_thread(threading.Thread):
    def __init__(self, callback, *args, **kwargs):
        threading.Thread.__init__(self)
        self.callback = lambda: callback(*args, **kwargs)
        self.start()

    def run(self):
        self.callback()


class VacuumHack(object):
    def __init__(self):
        self.process = None
        self.vacuum_position_x = None
        self.vacuum_position_y = None

        hook_manager = pyHook.HookManager()
        hook_manager.KeyDown = self._on_key_down
        hook_manager.HookKeyboard()

        self.set_vacuum_position = False
        self.enabled = True

    def _on_key_down(self, event):
        if event.Key == 'F1':
            self.set_vacuum_position = True

        if event.Key == 'F2':
            self.enabled = not self.enabled

    def read_unsigned_short(self, address):
        return struct.unpack('@H', self.process.read(address, 2))[0]

    def write_unsigned_short(self, address, value):
        self.process.write(address, struct.pack('@H', value))

    def move_monster(self, event, return_address, monster_address):
        self.process = event.get_process()

        if self.set_vacuum_position:
            self.vacuum_position_x = self.read_unsigned_short(CHARACTER_POSITION_X_ADDRESS)
            self.vacuum_position_y = self.read_unsigned_short(CHARACTER_POSITION_Y_ADDRESS) + 10
            self.set_vacuum_position = False

        if not self.enabled:
            return

        if not self.vacuum_position_x or not self.vacuum_position_y:
            self.vacuum_position_x = self.read_unsigned_short(CHARACTER_SPAWN_X_ADDRESS)
            self.vacuum_position_y = self.read_unsigned_short(CHARACTER_SPAWN_Y_ADDRESS)

        self.write_unsigned_short(monster_address + 0x3F2, self.vacuum_position_x)
        self.write_unsigned_short(monster_address + 0x3FA, self.vacuum_position_y)


def main():
    process = Process(api_hooks=None)
    vacuum_hack = VacuumHack()
    process.hook_function(MOVE_MONSTER_FUNCTION_ADDRESS, post_callback=vacuum_hack.move_monster, signature=(PVOID,))
    process.start(PATH, blocking=False)
    pythoncom.PumpMessages()


if __name__ == '__main__':
    main()
