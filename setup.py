import sys
from cx_Freeze import setup, Executable

setup(
    name = "AnimalShowdown",
    version = "0.52",
    description = "Indie Game",
    executables = [Executable("main.py", base = "Win32GUI")])