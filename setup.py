from distutils.core import setup
import datetime
import py2exe

from software_info import info

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = info['version']
        self.company_name = info['company_name']
        self.copyright = info['copyright']
        self.name = info['description']

logger = Target(
    description = info['description'],
    script = "logger.py",
    dest_base = info['exe']
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
    author=info['author'],
    version=info['version']
    )
