from cx_Freeze import setup, Executable

# Define the script and options
build_exe_options = {
    'packages': [],
    'excludes': [],
    'include_files': [],
    'compress': True  # Enable UPX compression
}

setup(
    name="TimelapseApp",
    version="1.0",
    description="A timelapse capture tool",
    options={"build_exe": build_exe_options},
    executables=[Executable("timelapse.py", base="Win32GUI", icon="icon.ico")],
)
