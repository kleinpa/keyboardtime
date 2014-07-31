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
    dest_base = info['exe'],
    icon_resources = [(1, "resources/app.ico")]
    )

setup(
    options = { 'py2exe': {
        'compressed': True,
        'optimize': 2,
        'bundle_files': 1,
        'dist_dir': 'dist',
        'dll_excludes': [],
        'includes': [
            'cherrypy.wsgiserver.wsgiserver3',
        ],
        'excludes': [
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
    zipfile=None,
    author=info['author'],
    version=info['version']
    )
