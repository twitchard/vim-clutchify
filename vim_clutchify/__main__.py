#!/usr/bin/env python
import re
from typing import Optional, Type, Iterable
from types import TracebackType

from xinput import operate_xinput_device, MODE_ENABLE, MODE_DISABLE
from evdev import list_devices, InputDevice, InputEvent, UInput, ecodes as e

class DeviceContext():
    def __init__(self, deviceName: str):
        devices = [InputDevice(fn) for fn in list_devices()]
        self.device = next(x for x in devices if re.search(deviceName, x.name))
        self.uinput = UInput()

    def __enter__(self) -> 'DeviceContext':
        operate_xinput_device(MODE_DISABLE, self.device.name)
        self.uinput.__enter__()
        return self

    def event_loop(self) -> Iterable[InputEvent]:
        yield from self.device.read_loop()

    def tap(self, key: str) -> None:
        key = getattr(e, 'KEY_%s' % key.upper())
        self.uinput.write(e.EV_KEY, key, 1)
        self.uinput.write(e.EV_KEY, key, 0)
        self.uinput.syn()

    def __exit__(self, typ: Optional[Type[BaseException]],
                 value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self.uinput.__exit__(typ, value, traceback)
        operate_xinput_device(MODE_ENABLE, self.device.name)


def main() -> None:
    with DeviceContext('FootSwitch') as device:
        for event in device.event_loop():
            if event.type == e.EV_KEY:
                if event.value == 1:
                    device.tap('F11')
                elif event.value == 0:
                    device.tap('F12')

if __name__ == '__main__':
    main()
