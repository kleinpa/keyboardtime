== KeyboardTime ==
A foreground application logger.

See your data at http://localhost:63874/

Some of the technologies used:

- Python
  - CherryPy
  - Windows API via ctypes
  - sqlalchemy
  - py2exe
- Web
  - Angular
  - D3
  - Bootstrap
- Installer
  - WIX

= Development =

This application was developed on windows with Python 3.4. You'll need to
install the prerequisites first:

- Python 3.4 (maybe others)
- GNU Make for Windows (http://gnuwin32.sourceforge.net/packages/make.htm)
- WiX

and install python dependencies

    pip install -r requirements.txt

then you should be able to build the exe with

    make

and the installer with

    make install
