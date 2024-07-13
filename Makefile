# This file may be generated from template.
# If you want to customize it, then place custom content between
# special markers `START_SKIP_AREA`, `END_SKIP_AREA`.

# START_SKIP_AREA
PACKAGE_NAME=multi_video
PYTHON_EXEC=. ../manager_standalone_env/bin/activate && python
# END_SKIP_AREA

# programs to compile `ui` to `.py`
UIC=pyuic5

################################ additional variables
MAIN_PACKAGE_PATH=src/${PACKAGE_NAME}


UI_FILES=$(shell find -type f -name "*.ui")
COMPILED_UI_FILES=$(UI_FILES:%.ui=%_ui.py)

################################ generate pyqt ui files
.PHONY: ui _ui_header
ui: _ui_header $(COMPILED_UI_FILES)

_ui_header:
	@echo "------------------------------------------------"
	@echo "Generating python files from ui files."
	@echo "------------------------------------------------"
	$(info $(COMPILED_UI_FILES))

%_ui.py: %.ui
	$(UIC) "${^}" --from-imports -o "./${@}"
	sed -i 's/from Py\(Qt\|Side\)[0-9]\+ import/from qtpy import/' "./$@"
	touch "./$(shell dirname $@)/__init__.py"

	sed -i 's=":\/="${PACKAGE_NAME}:=g' $@
	@if grep "import resource_rc" --max-count 1 $@ ; then\
		touch "$(dir $@)/resource_rc.py";\
	fi

################################ others
MAKE_DIR:=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))
$(info Running make in dir: $(MAKE_DIR))
$(info Using python executable: "$(PYTHON_EXEC)")
IS_VENV=$(shell $(PYTHON_EXEC) -c 'import os; print(os.getenv("VIRTUAL_ENV"))' )
PIP_FLAGS=$(shell $(PYTHON_EXEC) -c 'import os; print("" if os.getenv("VIRTUAL_ENV") else "--user")' )

install_system:
	python -m pip install -e .[all]

install:
	$(info Is virtual env: "$(IS_VENV)")
	$(info Pip flags: "$(PIP_FLAGS)")
	$(PYTHON_EXEC) -m pip install $(PIP_FLAGS) -e .[all]

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name "__pycache__" -delete

pre_commit_install:
	$(info Is virtual env: "$(IS_VENV)")
	$(info Pip flags: "$(PIP_FLAGS)")
	$(PYTHON_EXEC) -m pip install $(PIP_FLAGS) pre-commit
	$(PYTHON_EXEC) -m pre_commit install

pre_commit_uninstall:
	-$(PYTHON_EXEC) -m pre_commit uninstall

pre_commit:
	$(PYTHON_EXEC) -m pre_commit run --all-files

mypy:
	$(info Using mypy cache dir: "$(MYPY_CACHE_DIR)")
	$(PYTHON_EXEC) -m mypy --version

	( $(PYTHON_EXEC) -m mypy \
		--install-types --non-interactive \
		--config-file ./pyproject.toml \
 		./src \
		 2>&1 1>&3 3>&- | \
		awk --assign "PRE=$(MAKE_DIR)" '{print PRE "/" $$0}' \
		1>&2 3>&-) 3>&1

	@# (cmd 2>&1 >&3 3>&- | stderr-filter >&2 3>&-) 3>&1
	@# 		process only stderr, `sh` variant
	@# 		https://stackoverflow.com/a/52575213
	@# 		https://stackoverflow.com/a/13299397
	@# awk --assign PRE=$(MAKE_DIR) '{print PRE"/" $$0}'
	@#		add prefix to output
	@#		(to have absolute path, and be able to link in IDE)

pyright:
	$(PYTHON_EXEC) -m pyright --version
	$(PYTHON_EXEC) -m pyright ./src
