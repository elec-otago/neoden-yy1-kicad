# For development purposes, use the 'develop' target to install this package from the source repository (rather than the public python packages). This
# means that local changes to the code will automatically be used by the package on your machine.
# To do this type
#     make develop
# in this directory.

# Toolchains
PYTHON = python3
LINT = pylint
INSTALLER = pyinstaller
UPX = upx

# Source
MAIN_PY = neoden_kicad.py
PROJECT_NAME = neoden_kicad

# Destination
DIST_DIR = dist


.ONESHELL:

develop:
	$(PYTHON) -m venv venv
	. ./venv/bin/activate
	pip3 install -e .
	deactivate

test:
	. ./venv/bin/activate
	$(PYTHON) $(MAIN_PY) --pos data/CPL-test.csv --out data/CPL-out.csv
	deactivate

test2:
	. ./venv/bin/activate
	$(PYTHON) $(MAIN_PY) --pos data/CPL-test.csv --out data/CPL-out.csv --feeder_map data/feeder_map.csv
	deactivate

test_bin:
	. ./venv/bin/activate
	./dist/$(PROJECT_NAME) --pos data/CPL-test.csv --out data/CPL-out.csv --feeder_map data/feeder_map.csv
	deactivate

lint:
	$(LINT) --extension-pkg-whitelist=numpy --ignored-modules=numpy --extension-pkg-whitelist=astropy tart_tools

install:
	. ./venv/bin/activate
	$(INSTALLER) -F $(MAIN_PY) --specpath $(DIST_DIR)
	deactivate

clean:
	rm -rf $(DIST_DIR) build/ $(PROJECT_NAME).spec $(PROJECT_NAME).egg-info

test_upload:
	$(PYTHON) setup.py sdist
	twine upload --repository testpypi dist/*

upload:
	$(PYTHON) setup.py sdist
	twine upload --repository pypi dist/*
