""" Type "<esc>a" on the press of a footpedal, and "<esc>" on a release.

"""

from setuptools import setup, find_packages

setup(
        name='vim-clutchify',
        version='0.0.8',
        description='vim-clutch evdev bindings for USB foot pedal. Linux only.',
        long_description="""
Scans evdev for something that looks like a foot pedal.
Listens for keyup and keydown.
Emits a uinput <esc>a on keydown and uinput <esc> on a keyup.
That's it!
See https://github.com/alevchuk/vim-clutch
""",
        author='twitchard',
        author_email='richard.marmorstein@gmail.com',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha'
        ],

        keywords='vim evdev footpedal footswitch vim-clutch clutch',
        packages=find_packages(),
        install_requires=['evdev'],
        scripts=['bin/vim-clutchify']
)
