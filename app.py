from datetime import datetime, timedelta
from math import fabs

from pynput.keyboard import Controller, Key
from pynput.mouse import Listener, Button


class ClipboardHelper():
    def __init__(self):
        self._last_coord = None
        self.keyborad_controller = Controller()
        self._dbl_t = None
        self._hld_t = None
        self.listener = None
        self._isCopy = False

    def _isMove(self, x, y):
        return True if fabs(self._last_coord[0] - x) > 20 else False
    def _copy(self):
        with self.keyborad_controller.pressed(Key.ctrl):
            self.keyborad_controller.press('c')
            self.keyborad_controller.release('c')
            self._isCopy = True
            print('copy')
    def _paste(self):
        with self.keyborad_controller.pressed(Key.ctrl):
            self.keyborad_controller.press('v')
            self.keyborad_controller.release('v')
            self._isCopy = False
            print('pas')

    def _isHold(self):
        return True if (datetime.now() - self._hld_t) > timedelta(microseconds=700000) else False

    def _isDubleClick(self):
        if self._dbl_t:
            return True if (datetime.now() - self._dbl_t) < timedelta(microseconds=500000) else False
        else:
            return False

    def on_click(self, x, y, button, pressed):

        match button:
            case Button.left:
                if pressed:
                    self._hld_t = datetime.now()
                    self._last_coord = (x, y)
                if not pressed:
                    if self._isHold(): self._isCopy = False
                    if self._isCopy:
                        if (self._isMove(x, y) or self._isDubleClick()):
                            self._paste()
                    else:
                        if (self._isMove(x, y) or self._isDubleClick()):
                            self._copy()
                    self._dbl_t = datetime.now()
            case Button.middle:
                if not pressed:
                    self._paste()

    def start(self):
        with Listener(on_click=self.on_click) as listener:
            listener.join()


    def stop(self):
        self.listener.join()


ClipboardHelper().start()
