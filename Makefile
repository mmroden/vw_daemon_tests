VENV?=venv
VIRTUALENVDIR?=$(CURDIR)/$(VENV)
REQUIREMENTS?=$(CURDIR)/requirements.txt
VIRTUALENV=virtualenv
BEHAVE=venv/bin/behave
BEHAVE_ENV?=
BEHAVE_OPTS?=
VW_COMMIT_HASH?=0b1215ca6aac7147549e5e3d5ba6650b0684d233

.PHONY: all clean deps check

all: deps run check

deps: $(VIRTUALENVDIR) $(VIRTUALENVDIR)/.setup.touch
	@hash $(VIRTUALENV) || echo "$(VIRTUALENV) is not installed in the path, please install it."

$(VIRTUALENVDIR):
	virtualenv $(VENV)

$(VIRTUALENVDIR)/.setup.touch: $(REQUIREMENTS) | $(VENV)
	$(VENV)/bin/pip install -r $< && touch $@

check: run
	$(BEHAVE_ENV) $(BEHAVE) $(BEHAVE_OPTS)

check_aws: run_aws
	$(BEHAVE_ENV) $(BEHAVE) $(BEHAVE_OPTS)

clean:
	@echo "cleaning"
	rm -rf $(VIRTUALENVDIR)
	vagrant destroy -f

run: deps
	vagrant up
	vagrant ssh-config > .ssh.config

run_aws: deps
	vagrant up --provider=aws
	vagrant ssh-config > .ssh.config

provision:
	VW_COMMIT_HASH=$(VW_COMMIT_HASH) vagrant provision