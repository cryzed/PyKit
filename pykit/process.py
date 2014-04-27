import os
import threading
from winappdbg import EventHandler, Debug, System


class HookingEventHandler(EventHandler):
    def __init__(self, hooks):
        EventHandler.__init__(self)
        self.hooks = hooks

    def create_process(self, event):
        pid = event.get_pid()
        for address, pre_callback, post_callback, signature in self.hooks:
            event.debug.hook_function(pid, address, pre_callback, post_callback, signature=signature)


class start_new_thread(threading.Thread):
    def __init__(self, callback, *args, **kwargs):
        threading.Thread.__init__(self)
        self.callback = lambda: callback(*args, **kwargs)
        self.start()

    def run(self):
        self.callback()


class Process(object):
    def __init__(self, api_hooks=None):
        System.request_debug_privileges()
        self.apiHooks = api_hooks
        self.hooks = []
        self.debugger = None

    def _loop(self):
        try:
            self.debugger.loop()
        except KeyboardInterrupt:
            self.debugger.stop()

    def hook_function(self, address, pre_callback=None, post_callback=None, signature=None):
        if not pre_callback and not post_callback:
            return

        self.hooks.append((address, pre_callback, post_callback, signature))

    def start(self, path, kill_process_on_exit=True, anti_anti_debugger=True, blocking=True):
        def function():
            os.chdir(os.path.dirname(path))
            self.debugger = Debug(HookingEventHandler(self.hooks), bKillOnExit=anti_anti_debugger)
            self.debugger.execv([path])
            self._loop()

        if blocking:
            function()
        start_new_thread(function)

    def attach(self, pid, anti_anti_debugger=True, blocking=True):
        def function():
            self.debugger = Debug(HookingEventHandler(self.hooks), bHostileCode=anti_anti_debugger)
            self.debugger.attach(pid)
            self._loop()

        if blocking:
            function()
        start_new_thread(function)