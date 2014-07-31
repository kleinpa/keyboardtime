
SRC_FILES := db.py foreground.py logger.py schema.py setup.py software_info.py
SI_CANDLE_ARGS := $(shell python software_info.py --candle)
SI_NAME := $(shell python software_info.py --value name)
SI_EXE := $(shell python software_info.py --value name)
SI_VERSION := $(shell python software_info.py --value version)

MSI_NAME := $(SI_NAME)\ $(SI_VERSION)
WIXEXTENSIONS := -ext WixUIExtension -ext WixUtilExtension

default: dist/$(SI_EXE).exe

install: $(MSI_NAME).msi

dist/$(SI_EXE).exe: *.py
	python setup.py py2exe

files.wxs: $(shell ./web-files)
	heat dir dist -ag -cg Web -dr INSTALLDIR -indent 2 -sfrag -var var.WebSrc -out "$@"

install.wixobj: install.wxs dist/metrics.exe
	candle -nologo $(WIXEXTENSIONS) "$<" $(SI_CANDLE_ARGS)

$(MSI_NAME).msi: install.wixobj
	light -nologo $(WIXEXTENSIONS) "$<" -out "$@"

.PHONY : clean
clean :
	-rmdir /S /Q dist
	-rmdir /S /Q __pycache__
	-del /F /Q *.wixobj
	-del /F /Q *.wixpdb
	-del /F /Q *.msi
