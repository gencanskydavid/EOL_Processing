from cx_Freeze import setup, Executable


build_exe_options = {"excludes": ["tkinter","jupyter"],
                     "include_files": ["config.yaml"]}

executables = [
    Executable(
        'main.py',
        base = None,
        targetName = 'EOL_proccesing',
    )
]

setup(
    name="EOL_Processing_Files",
    version="0.5.1",
    description="EOL Processing Files program",
    options={"build_exe": build_exe_options},
    executables=executables
)
