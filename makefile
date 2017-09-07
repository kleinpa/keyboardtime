
SRC_FILES := db.py foreground.py main.py schema.py setup.py software_info.py
SI_CANDLE_ARGS := $(shell python keyboardtime\software_info.py --candle)
SI_EXE := $(shell python keyboardtime\software_info.py --value exe)
SI_VERSION := $(shell python keyboardtime\software_info.py --value version)

MSI_NAME = $(SI_EXE)-$(SI_VERSION).msi
BUILD_DIR := build/exe.win32-3.6

WIXFLAGS := -ext WixUIExtension -ext WixUtilExtension
WIXLIGHTFLAGS := -sice:ICE61 -sice:ICE69

PYTHON = python
IMAGEMAGICK = magick
WIXHEAT = "$(WIX)/bin/heat"
WIXLIGHT = "$(WIX)/bin/light"
WIXCANDLE = "$(WIX)/bin/candle"

default: $(BUILD_DIR)\$(SI_EXE).exe

install: $(MSI_NAME)

$(BUILD_DIR)/$(SI_EXE).exe: *.py keyboardtime/web
	$(PYTHON) setup.py build

%.bmp: %.svg
	$(IMAGEMAGICK) "$<" "$@"

install/dist.wxs: $(BUILD_DIR)/$(SI_EXE).exe
	$(WIXHEAT) dir $(BUILD_DIR) -ag -cg DistFiles -dr INSTALLFOLDER -indent 2 -sfrag -sreg -srd -var var.DistSrc -out "$@"

install/%.wixobj: install/%.wxs
	$(WIXCANDLE) -nologo $(WIXFLAGS) "$<" $(SI_CANDLE_ARGS) -dDistSrc=$(BUILD_DIR) -out "$@"

$(MSI_NAME): install/Product.wixobj install/SimpleUI.wixobj install/dist.wixobj install/wixui-banner.bmp install/wixui-dialog.bmp
	$(WIXLIGHT) -nologo $(WIXFLAGS) $(WIXLIGHTFLAGS) install/Product.wixobj install/SimpleUI.wixobj install/dist.wixobj -out "$@"

clean :
	-rmdir /S /Q dist
	-rmdir /S /Q __pycache__
	-del /F /Q *.wixobj
	-del /F /Q *.wixpdb
	-del /F /Q dist.wxs
