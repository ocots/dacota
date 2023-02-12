import os

# Code recovered from numpy/core/__init__.py
# distutils in windows stores the dll create by the extension in a .libs folder
# does dlls need to be loades manually before importing the extension
if os.name == "nt":
    from ctypes import WinDLL
    from pathlib import Path

    libs_path = Path(Path(__file__).absolute().parents[0], ".libs")
    if libs_path.exists():
        for filename in libs_path.glob("*dll"):
            WinDLL(str(filename.absolute()))

from .tools import *
