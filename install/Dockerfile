FROM microsoft/dotnet-framework:3.5-windowsservercore-10.0.14393.1480

# Setup shell
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

# Wix
RUN powershell.exe -Command \
  Invoke-WebRequest http://wixtoolset.org/downloads/v3.11.0.1528/wix311.exe -OutFile "C:\wix.exe"; \
  Start-Process "C:\wix.exe" -ArgumentList '/install /silent' -NoNewWindow -Wait; \
  rm "C:\wix.exe";

# Python
RUN powershell.exe -Command \
  Invoke-WebRequest "https://www.python.org/ftp/python/3.6.1/python-3.6.1.exe" -OutFile "C:\python.exe"; \
  Start-Process 'C:\python.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -NoNewWindow -Wait; \
  rm "C:\python.exe";

# ImageMagick
RUN powershell.exe -Command \
  Invoke-WebRequest "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs921/gs921w32.exe" -OutFile "C:\ghostscript.exe"; \
  Start-Process "C:\ghostscript.exe" -ArgumentList '/S' -NoNewWindow -Wait; \
  rm "C:\ghostscript.exe"; \
	$env:PATH = \"C:\Program Files (x86)\gs\gs9.21\bin;\" + $env:PATH; \
  Invoke-WebRequest "https://www.imagemagick.org/download/binaries/ImageMagick-7.0.7-0-Q16-x64-dll.exe" -OutFile "C:\imagemagick.exe"; \
  Start-Process "C:\imagemagick.exe" -ArgumentList '/SILENT' -NoNewWindow -Wait; \
  rm "C:\imagemagick.exe"; \
	$env:PATH = \"C:\Program Files\ImageMagick-7.0.7-Q16\;\" + $env:PATH; \
	[Environment]::SetEnvironmentVariable('PATH', $env:PATH, [EnvironmentVariableTarget]::Machine);

# Make
RUN powershell.exe -Command \
  Invoke-WebRequest "https://downloads.sourceforge.net/project/gnuwin32/make/3.81/make-3.81.exe" -UserAgent "DockerCI" -OutFile "C:\make.exe"; \
  Start-Process "C:\make.exe" -ArgumentList '/SILENT' -NoNewWindow -Wait; \
  rm "C:\make.exe"; \
	$env:PATH = \"C:\Program Files (x86)\GnuWin32\bin\;\" + $env:PATH; \
	[Environment]::SetEnvironmentVariable('PATH', $env:PATH, [EnvironmentVariableTarget]::Machine);

COPY requirements.txt .
RUN pip install -r requirements.txt;

WORKDIR C:/app

COPY . .
