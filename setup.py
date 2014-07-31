from distutils.core import setup
import datetime
import py2exe
import os

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
    dest_base = info['exe'],
    icon_resources = [(1, "resources/app.ico")]
    )

def list_data_files(root):
    return [(folder, [os.path.join(folder, f) for f in files]) for
                (folder, subfolders, files) in os.walk(root)]

setup(
    options = { 'py2exe': {
        'compressed': True,
        'optimize': 2,
        'bundle_files': 2,
        'dist_dir': 'dist',
        'dll_excludes': [],
        'includes': [
            'cherrypy.wsgiserver.wsgiserver3',
        ],
        'excludes': [ # Mostly trial and error here
            'sqlalchemy.dialects.drizzle',
            'sqlalchemy.dialects.firebird',
            'sqlalchemy.dialects.mssql',
            'sqlalchemy.dialects.mysql',
            'sqlalchemy.dialects.oracle',
            'sqlalchemy.dialects.postgresql',
            'sqlalchemy.dialects.sybase',
            'win32com',
            'unittest',
            'distutils',
            'pydoc_data'
        ]}},
    windows=[logger],
    data_files = list_data_files('web'),
    #zipfile=None,
    author=info['author'],
    version=info['version'],
    )
