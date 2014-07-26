

SRC_FILES = db.py foreground.py logger.py schema.py setup.py software_info.py
SI_CANDLE_ARGS = $(shell python software_info.py --candle)
SI_NAME = $(shell python software_info.py --value name)

all: install

install: $(SI_NAME).msi

dist/metrics.exe: *.py
	python setup.py py2exe

install.wixobj: dist/metrics.exe
	candle install.wxs $(SI_CANDLE_ARGS)

$(SI_NAME).msi: install.wixobj
	light install.wixobj -out $(SI_NAME).msi

.PHONY : clean
clean :
	-del dist *.wixobj *.wixpdb install.msi
