import datetime
import sys
import os

info = {}

info['exe'] = "metrics"
info['name'] = "Metrics"
info['description'] = "Metrics Logger"

info['author'] = "Peter Klein"
info['company_name'] = "Peter Klein"
info['copyright'] = "(c) {0} {1}".format(datetime.datetime.now().year, info['company_name'])

def get_version_data():
    def is_py2exe():
        return hasattr(sys,"frozen") and sys.frozen in ("windows_exe", "console_exe")
    def git_describe():
        """Returns a dict representing the current version:
            - a: Major version; from git tag
            - b: Minor version; from git tag
            - add: commits since minor version
            - hash: current commit hash if clean, otherwise 1
            - dirty: 1 if the working tree has changes, otherwise 0"""

        import subprocess
        import os
        import re

        os.environ["PATH"] += os.pathsep + "C:\\cygwin\\bin"
        os.environ["PATH"] += os.pathsep + "C:\\cygwin64\\bin"

        try:
            st = subprocess.check_output("git.exe describe --tags --dirty --match \"v*\"").decode('utf8')
            m = re.match(r"v(?P<a>\d+)\.(?P<b>\d+)(?:-(?P<add>\d+)-g(?P<hash>[0-9a-f]{7}))?(?P<dirty>-dirty)?", st)
            d = m.groupdict()
            d['dirty'] = 9999999 if d['dirty'] else 0
            d['add'] = d['add'] or 0
            d['hash'] = (d['hash'] or 0) if not d['dirty'] else d['dirty']
            return d
        except Exception:
            return None
    def unpickle_version():
        try:
            import pickle
            root = os.path.abspath(os.path.dirname(os.path.abspath(sys.executable)))
            with open(os.path.join(root, 'version.dat'), 'rb') as f:
                x2=os.path.join(root, 'version.dat')
                return pickle.load(f)
        except Exception:
            return None

    default_version = {'a':'0','b':'0','add':'0','dirty':'0','hash':'0'}

    if is_py2exe():
        return unpickle_version() or default_version
    else:
        return git_describe() or default_version

version_data = get_version_data()
info['version'] = "{a}.{b}.{add}.{hash}".format(**version_data)
info['version4'] = "{a}.{b}.{add}.{dirty}".format(**version_data)

# Some utility functions for accessing data from outside python
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Get the software information.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-v', '--value', help='gets the value associated with the variable VAR', metavar="VAR")
    group.add_argument('-c', '--candle', help='display software info formatted as candle arguments', action='store_true')
    group.add_argument('-p', '--pickle', help='writes a pickled version info', action='store_true')
    parser.add_argument('-o', help='output file for pickled version info', metavar="FILE")
    args = parser.parse_args()

    if args.candle:
        print("".join([" -dsi_{0}=\"{1}\"".format(*x) for x in info.items()]))
    if args.value:
        print(info.get(args.value, None))
    if args.pickle:
        import pickle
        with open(args.o or "version.dat", 'wb') as f:
            version_data = get_version_data()
            pickle.dump(version_data, f)
            print("Version data written to '{0}'".format(args.o or "version.dat"))
