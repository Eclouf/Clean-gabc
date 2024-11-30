from cx_Freeze import setup, Executable

executables = [Executable("CommandLine.py", copyright="Copyright © 2024 Eclouf")]

setup(
    name="Clean-gabc",
    version="0.1",
    description="Program to clarify gabc partions",
    executables=executables
)