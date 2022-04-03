MAIN_PACKAGE_NAME=multi_video

UIC=pyuic5
UI_DIR=lib/$(MAIN_PACKAGE_NAME)/ui
UI_FILES=$(wildcard $(UI_DIR)/*.ui)
COMPILED_UI_FILES=$(UI_FILES:$(UI_DIR)/%.ui=$(UI_DIR)/%_ui.py)

####################################

.PHONY: all ui compile

all: ui
	@echo "Make all finished"

ui: $(COMPILED_UI_FILES)

$(UI_DIR)/%_ui.py : $(UI_DIR)/%.ui
	$(UIC) $< --from-imports -o $@
