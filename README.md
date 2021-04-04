Scans evdev for something that looks like a foot pedal.
Listens for keyup and keydown.
Emits a uinput <esc>a on keydown and uinput <esc> on a keyup.
That's it!
See https://github.com/alevchuk/vim-clutch

Steps:

1. Run Linux (and X windows)
2. Plug in USB footpedal named something like 'RDing FootSwitch1F1.'
3. Disable the footpedal as an input into X.
4. Run this program as root.
4. When you press the pedal down `<esc>a` will be typed.
5. When you release it, `<esc>` will be typed.

Concretely:
```
# Install it
pip3 install vim-clutchify

# Get input id of switch.
xinput | grep FootSwitch

# Disable the switch sending keys to X directly.
xinput disable ${ID_FROM_PREVIOUS_STEP}

# Launch it!
sudo vim-clutchify

# Open vim
vim
# Profit!
```

Inspired by this [project by Aleksandr Levchuk](https://github.com/alevchuk/vim-clutch).
