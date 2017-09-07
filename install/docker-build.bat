@ECHO # Preparing Build Image

@docker build -t keyboardtime_dev -f %~dp0Dockerfile %~dp0..

@ECHO.
@ECHO # Starting Build Container

@docker run --rm -v "%~dp0..:C:\output" keyboardtime_dev powershell -Command "make install; cp *.msi C:\output"
