
SRC_FILES := db.py foreground.py logger.py schema.py setup.py software_info.py
SI_CANDLE_ARGS := $(shell python software_info.py --candle)
SI_NAME := $(shell python software_info.py --value name)
SI_EXE := $(shell python software_info.py --value name)
SI_VERSION := $(shell python software_info.py --value version)

MSI_NAME := $(SI_NAME)\ $(SI_VERSION)
WIXEXTENSIONS := -ext WixUIExtension -ext WixUtilExtension

default: dist/$(SI_EXE).exe dist/version.dat

install: $(MSI_NAME).msi

dist/$(SI_EXE).exe: *.py
	python setup.py py2exe

dist/version.dat: .FORCE
	python software_info.py -p -o "$@"

.FORCE:

dist: dist/$(SI_EXE).exe dist/version.dat

dist.wxs: dist
	heat dir dist -ag -cg Files -dr INSTALLDIR -indent 2 -sfrag -srd -var var.DistSrc -out "$@"

%.wixobj: %.wxs
	candle -nologo $(WIXEXTENSIONS) "$<" $(SI_CANDLE_ARGS) -dDistSrc=dist

$(MSI_NAME).msi: install.wixobj dist.wixobj
	light -nologo $(WIXEXTENSIONS) install.wixobj dist.wixobj -out "$@"

.PHONY : clean
clean :
	-rmdir /S /Q dist
	-rmdir /S /Q __pycache__
	-del /F /Q *.wixobj
	-del /F /Q *.wixpdb
#	-del /F /Q *.msi
	-del /F /Q dist.wxs
