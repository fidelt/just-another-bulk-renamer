import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages" : [ "os", "re", "sys", "traceback", "tkinter" ], 
    "excludes" : []
}

base = None
if sys.platform == "win32" :
  base = "Win32GUI"

setup(
    name = "jabr",
    version = "0.9",
    description = "Just Another Bulk Renamer",
    options = { "build_exe" : build_exe_options },
    executables = [ Executable("jabr.py", base=base, icon="icon.ico") ]
)