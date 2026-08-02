PY?=
PELICAN?=pelican
PELICANOPTS=
ORCID_ID ?= 0000-0002-0037-9394
ORCID_SYNC_SCRIPT ?= scripts/sync_orcid.py
GITHUB_USERNAME ?= alxcn
GITHUB_SYNC_SCRIPT ?= scripts/sync_github.py
SITE_META_SCRIPT ?= scripts/generate_site_meta.py
SITE_CANONICAL_URL ?= https://alejandroucanpuc.github.io
ENABLE_UPDATES_RSS ?= 1

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

GITHUB_PAGES_BRANCH=gh-pages
GITHUB_PAGES_COMMIT_MESSAGE=Generate Pelican site


DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

SERVER ?= "0.0.0.0"

PORT ?= 0
ifneq ($(PORT), 0)
	PELICANOPTS += -p $(PORT)
endif


help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make regenerate                     regenerate files upon modification '
	@echo '   make publish                        generate using production settings '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	@echo '   make devserver [PORT=8000]          serve and regenerate together      '
	@echo '   make devserver-global               regenerate and serve on 0.0.0.0    '
	@echo '   make github                         upload the web site via gh-pages   '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

html:
	python3 "$(ORCID_SYNC_SCRIPT)" --orcid "$(ORCID_ID)"
	python3 "$(GITHUB_SYNC_SCRIPT)" --username "$(GITHUB_USERNAME)"
	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)
	python3 "$(SITE_META_SCRIPT)" --output-dir "$(OUTPUTDIR)" --site-url "$(SITE_CANONICAL_URL)" $(if $(filter 1,$(ENABLE_UPDATES_RSS)),--enable-updates-rss,)

clean:
	[ ! -d "$(OUTPUTDIR)" ] || rm -rf "$(OUTPUTDIR)"

regenerate:
	python3 "$(ORCID_SYNC_SCRIPT)" --orcid "$(ORCID_ID)"
	python3 "$(GITHUB_SYNC_SCRIPT)" --username "$(GITHUB_USERNAME)"
	"$(PELICAN)" -r "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)
	python3 "$(SITE_META_SCRIPT)" --output-dir "$(OUTPUTDIR)" --site-url "$(SITE_CANONICAL_URL)" $(if $(filter 1,$(ENABLE_UPDATES_RSS)),--enable-updates-rss,)

serve:
	python3 "$(ORCID_SYNC_SCRIPT)" --orcid "$(ORCID_ID)"
	python3 "$(GITHUB_SYNC_SCRIPT)" --username "$(GITHUB_USERNAME)"
	"$(PELICAN)" -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)
	python3 "$(SITE_META_SCRIPT)" --output-dir "$(OUTPUTDIR)" --site-url "$(SITE_CANONICAL_URL)" $(if $(filter 1,$(ENABLE_UPDATES_RSS)),--enable-updates-rss,)

serve-global:
	python3 "$(ORCID_SYNC_SCRIPT)" --orcid "$(ORCID_ID)"
	python3 "$(GITHUB_SYNC_SCRIPT)" --username "$(GITHUB_USERNAME)"
	"$(PELICAN)" -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS) -b $(SERVER)
	python3 "$(SITE_META_SCRIPT)" --output-dir "$(OUTPUTDIR)" --site-url "$(SITE_CANONICAL_URL)" $(if $(filter 1,$(ENABLE_UPDATES_RSS)),--enable-updates-rss,)

devserver:
	python3 "$(ORCID_SYNC_SCRIPT)" --orcid "$(ORCID_ID)"
	python3 "$(GITHUB_SYNC_SCRIPT)" --username "$(GITHUB_USERNAME)"
	"$(PELICAN)" -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)
	python3 "$(SITE_META_SCRIPT)" --output-dir "$(OUTPUTDIR)" --site-url "$(SITE_CANONICAL_URL)" $(if $(filter 1,$(ENABLE_UPDATES_RSS)),--enable-updates-rss,)

devserver-global:
	python3 "$(ORCID_SYNC_SCRIPT)" --orcid "$(ORCID_ID)"
	python3 "$(GITHUB_SYNC_SCRIPT)" --username "$(GITHUB_USERNAME)"
	"$(PELICAN)" -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS) -b 0.0.0.0
	python3 "$(SITE_META_SCRIPT)" --output-dir "$(OUTPUTDIR)" --site-url "$(SITE_CANONICAL_URL)" $(if $(filter 1,$(ENABLE_UPDATES_RSS)),--enable-updates-rss,)

publish:
	python3 "$(ORCID_SYNC_SCRIPT)" --orcid "$(ORCID_ID)"
	python3 "$(GITHUB_SYNC_SCRIPT)" --username "$(GITHUB_USERNAME)"
	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(PUBLISHCONF)" $(PELICANOPTS)
	python3 "$(SITE_META_SCRIPT)" --output-dir "$(OUTPUTDIR)" --site-url "$(SITE_CANONICAL_URL)" $(if $(filter 1,$(ENABLE_UPDATES_RSS)),--enable-updates-rss,)

github: publish
	ghp-import -m "$(GITHUB_PAGES_COMMIT_MESSAGE)" -b $(GITHUB_PAGES_BRANCH) "$(OUTPUTDIR)" --no-jekyll
	git push origin $(GITHUB_PAGES_BRANCH)


.PHONY: html help clean regenerate serve serve-global devserver devserver-global publish github
