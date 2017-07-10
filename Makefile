STATEDIR = $(PWD)/.state
BINDIR = $(STATEDIR)/env/bin

# Short descriptions for commands (var format _SHORT_DESC_<cmd>)
_SHORT_DESC_BUILD := "Build the app for dev and/or deployment"
_SHORT_DESC_LINT := "Run linting tools on the codebase"
_SHORT_DESC_PYENV := "Set up the python environment"
_SHORT_DESC_TEST := "Run the tests"

default : help
	@echo "You must specify a command"
	@exit 1


# ###
#  Helpers
# ###

_REQUIREMENTS_FILES = requirements/main.txt requirements/test.txt requirements/lint.txt
VENV_EXTRA_ARGS =

$(STATEDIR)/env/pyvenv.cfg : $(_REQUIREMENTS_FILES)
	# Create our Python 3 virtual environment
	rm -rf $(STATEDIR)/env
	python3 -m venv $(VENV_EXTRA_ARGS) $(STATEDIR)/env

	# Upgrade tooling requirements
	$(BINDIR)/python -m pip install --upgrade pip setuptools wheel

	# Install requirements
	$(BINDIR)/python -m pip install $(foreach req,$(_REQUIREMENTS_FILES),-r $(req))

$(STATEDIR)/docker-build : Dockerfile requirements/main.txt
	# Build our docker container(s) for this project.
	docker-compose build

	# Mark the state so we don't rebuild this needlessly.
	mkdir -p $(STATEDIR)
	touch $(STATEDIR)/docker-build

# /Helpers


# ###
#  Help
# ###

help :
	@echo ""
	@echo "Usage: make <cmd> [<VAR>=<val>, ...]"
	@echo ""
	@echo "Where <cmd> can be:"  # alphbetical please
	@echo "  * help -- this info"
	@echo "  * help-<cmd> -- for more info"
	@echo "  * build -- ${_SHORT_DESC_BUILD}"
	@echo "  * lint -- ${_SHORT_DESC_LINT}"
	@echo "  * pyenv -- ${_SHORT_DESC_PYENV}"
	@echo "  * test -- ${_SHORT_DESC_TEST}"
	@echo "  * version -- Print the version"
	@echo ""
	@echo "Where <VAR> can be:"  # alphbetical please
	@echo ""

# /Help


# ###
#  Pyenv
# ###

help-pyenv :
	@echo "${_SHORT_DESC_PYENV}"
	@echo "Usage: make pyenv"
	@echo ""
	@echo "Where <VAR> could be:"  # alphbetical please
	@echo "  * VENV_EXTRA_ARGS -- extra arguments to give venv (default: '$(VENV_EXTRA_ARGS)')"

pyenv : $(STATEDIR)/env/pyvenv.cfg

# /Pyenv


# ###
#  Test
# ###

TEST =
TEST_EXTRA_ARGS =

help-test :
	@echo "${_SHORT_DESC_TEST}"
	@echo "Usage: make test [<VAR>=<val>, ...]"
	@echo ""
	@echo "Where <VAR> could be:"  # alphbetical please
	@echo "  * TEST -- specify the test to run (default: '$(TEST)')"
	@echo "  * TEST_EXTRA_ARGS -- extra arguments to give pytest (default: '$(TEST_EXTRA_ARGS)')"
	@echo "    (see also setup.cfg's pytest configuration)"

test : $(STATEDIR)/docker-build
	docker-compose run testing bin/test $(TEST_EXTRA_ARGS) $(TEST)

# /Test


# ###
#  Version
# ###

version help-version : .git
	@python3 setup.py --version

# /Version


# ###
#  Lint
# ###

help-lint :
	@echo "${_SHORT_DESC_LINT}"
	@echo "Usage: make lint"

lint : $(STATEDIR)/env/pyvenv.cfg setup.cfg
	$(BINDIR)/python -m flake8 .

# /Lint


# ###
#  Build
# ###

help-build :
	@echo "${_SHORT_DESC_BUILD}"
	@echo "Usage: make build"

build :
	# This is duplicate of $(STATEDIR)/docker-build to force the build.

	# Build our docker container(s) for this project.
	docker-compose build

	# Mark the state so we don't rebuild this needlessly.
	mkdir -p $(STATEDIR)
	touch $(STATEDIR)/docker-build

# /Build
