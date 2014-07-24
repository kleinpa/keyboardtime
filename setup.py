from distutils.core import setup
import py2exe

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "0.5.0"
        self.company_name = "Beckman Coulter"
        self.copyright = "Beckman Coulter"
        self.name = "Metrics Logger"

logger = Target(
    description = "A Metrics Logger",
    script = "logger.py",
    dest_base = "metrics"
    )

setup(
    options = { 'py2exe': {
        'compressed': True,
        'optimize': 2,
        'bundle_files': 1,
        'dist_dir': 'dist',
        'dll_excludes': [
            'msvcp90.dll',
            'w9xpopen.exe'
        ],
        'includes': [
            #'encodings',
            'codecs',
            'sqlalchemy'
        ],
        'excludes': [
        ]}},
    console=[logger],
    zipfile=None
    )
