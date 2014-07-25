from distutils.core import setup
import datetime
import py2exe

import software_info

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = software_info.version
        self.company_name = software_info.company_name
        self.copyright = software_info.copyright
        self.name = software_info.description

logger = Target(
    description = software_info.description,
    script = "logger.py",
    dest_base = software_info.exe
    )

setup(
    options = { 'py2exe': {
        'compressed': True,
        'optimize': 2,
        'bundle_files': 1,
        'dist_dir': 'dist',
        'dll_excludes': [],
        'includes': [],
        'excludes': [
            '_ssl','win32ui'
        ]}},
    windows=[logger],
    zipfile=None,
    author=software_info.author,
    version=software_info.version
    )
