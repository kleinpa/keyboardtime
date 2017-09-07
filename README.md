# KeyboardTime

KeyboardTime uses the Windows API to periodically check what program is in the
foreground to chart and analyze your computer usage habits. The logs are stored
in a SQLite database so offline analysis is also possible. Historical charts are
available through a [built-in web server](http://localhost:63874/).

KeyboardTime is written in Python and distributed as a standalone installer
which can be found on the
[releases page](https://github.com/kleinpa/keyboard-time/releases).

Whenever the foreground application changes or the computer goes idle (no
interactions in the past 60 seconds), an entry is added to the database
including the hostname, the application name, start time, duration, and
"activeness". "activeness" is the average time between interactions while that
application was running. The application name used is the process image name
which may or may not actually be descriptive.

## Development

Prerequisites for building the application and installer:

- Python 3.6
- [GNU Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm)
- [ImageMagick](https://www.imagemagick.org/script/download.php#windows) (installer only)
- [WiX](http://wixtoolset.org/releases/v3.11/stable) (installer only)

The python dependencies can be installed with

    pip install -r requirements.txt

then you should be able to build the exe with

    make

and the installer with

    make install

### Docker

If Docker is available and configured to run Windows containers, the
`install/docker-build.bat` script will download all the dependencies and build
the whole application in a repeatable way.
