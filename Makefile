.PHONY: test-py2 test-py3 docs deploy clean

PKG = flask.ext.reqarg
PY2 = python
PY3 = python3
NOSE_PY2 = nosetests
NOSE_PY3 = nosetests-3.3
NOSE_OPTS = --with-coverage --cover-package $(PKG)
DEPLOY_OPTS = sdist bdist_egg upload

test: test-py2 test-py3

test-py2:
	$(NOSE_PY2) $(NOSE_OPTS)

test-py3:
	$(NOSE_PY3) $(NOSE_OPTS)

docs:
	$(MAKE) -C docs html

deploy:
	$(PY2) setup.py $(DEPLOY_OPTS)
	$(PY3) setup.py $(DEPLOY_OPTS)

clean:
	$(RM) -r Flask_ReqArg.egg-info
	$(RM) -r dist
	$(RM) -r build

