from cx_Freeze import setup, Executable

from keyboardtime.software_info import info

options = {
    'build_exe': {
        "packages": ["packaging", "sqlalchemy.sql.default_comparator"],
        "include_msvcr": True
    }
}

executables = [
    Executable('main.py', base='Win32GUI',
               targetName='{0}.exe'.format(info['exe']))
]

setup(name=info['name'],
      version=info['version4'],
      description=info['description'],
      executables=executables,
      options=options
)
