#!/usr/bin/env python
import re
from typing import Optional, Type, Iterable
from types import TracebackType

from xinput import operate_xinput_device, MODE_ENABLE, MODE_DISABLE
from evdev import list_devices, InputDevice, InputEvent, UInput, ecodes as e

class DeviceContext():
    """Context Handler to provide UInput functionality.
    This wraps UInput context handler to disable the xinput device while in use.
    It also provides some uinput helper methods to expose uinput functionality.
    :param device_name: string to use for matching the device name
    """

    def __init__(self, device_name: str):
        devices = [InputDevice(fn) for fn in list_devices()]
        self.device = next(x for x in devices if re.search(device_name, x.name))
        self.uinput = UInput()

    def __enter__(self) -> 'DeviceContext':
        """Context Handler entry.
        Disable the selected device with xinput and call the wrapped entry.
        :return: this object with helpers to expose uinput functionality
        """
        operate_xinput_device(MODE_DISABLE, self.device.name)
        self.uinput.__enter__()
        return self

    def event_loop(self) -> Iterable[InputEvent]:
        """Expose the selected device's event read loop.
        :return: iterate InputEvents from the underlying device functionality
        """
        yield from self.device.read_loop()

    def tap(self, key: str) -> None:
        """Tap a key by sending instantaneous keydown, keyup and syncing.
        :param key: String key name to tap (from evdev.ecodes.KEY_*)
        """
        key = e.ecodes[f'KEY_{key.upper()}']
        # Pylint claims evdev.ecodes.EV_KEY doesn't exists so needs disabling
        self.uinput.write(e.EV_KEY, key, 1)  # pylint: disable=no-member
        self.uinput.write(e.EV_KEY, key, 0)  # pylint: disable=no-member
        self.uinput.syn()

    def __exit__(self, typ: Optional[Type[BaseException]],
                 value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        """Context Handler exit.
        Re-enable the selected device with xinput and call the wrapped exit.
        """
        self.uinput.__exit__(typ, value, traceback)
        operate_xinput_device(MODE_ENABLE, self.device.name)


def main() -> None:
    """Caputure and input device and replace it's keydown/keyup events with
    separate keypresses.
    """
    with DeviceContext('HID 1a86:e026 Keyboard') as device:
        while retry := True:
            try:
                for event in device.event_loop():
                    if event.type == e.EV_KEY:  # pylint: disable=no-member
                        if event.value == 1:
                            device.tap('F11')
                        elif event.value == 0:
                            device.tap('F12')
            except OSError:
                retry = True
            except KeyboardInterrupt:
                retry = False

if __name__ == '__main__':
    main()
