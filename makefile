MAIN_PACKAGE_NAME=multi_vlc
UI_DIR=src/ui
COMPILED_UI_DIR=$(MAIN_PACKAGE_NAME)/ui

UIC=pyuic5
RCC=pyrcc5
####################################

UI_FILES=$(wildcard $(UI_DIR)/*.ui)
COMPILED_UI_FILES=$(UI_FILES:$(UI_DIR)/%.ui=$(COMPILED_UI_DIR)/ui_%.py)
RESOURCE_SRC=$(shell grep '^ *<file' resources.qrc | sed 's@</file>@@g;s/.*>//g' | tr '\n' '')

all: ui resources


ui: $(COMPILED_UI_FILES)

$(COMPILED_UI_DIR)/ui_%.py : $(UI_DIR)/%.ui
	$(UIC) $< --from-imports -o $@


resources: src/resources.qrc $(RESOURCES_SRC)
	$(RCC) -o $(COMPILED_UI_DIR)/resources_rc.py  $<
