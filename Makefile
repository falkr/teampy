all:
	@echo "Specify a target."

docs:
	pdoc --html --overwrite --html-dir ./docs ./teampy

pypi: docs
	sudo python2 setup.py register sdist upload

code:
	python3 -m isort ./
	python3 -m black .

dev-install: docs
	rm -rf ./dist
	python3 setup.py sdist
	pip3 install -v -U dist/*.tar.gz

deploy: docs
	rm -rf ./dist
	python setup.py sdist
	twine upload dist/*

pep8:
	pep8-python2 pdoc/__init__.py scripts/pdoc

push:
	git push origin master
	git push github master

runtests:
	python -m unittest tests/test_teampy.py
