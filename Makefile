test:
	python -m unittest discover -s tests

venv:
	source .venv/bin/activate

build:
	python -m build

upload-test:
	python -m twine upload --repository testpypi dist/*

# python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps granavi

upload:
	python -m twine upload dist/*

doc:
	sphinx-build -b html docs/source docs/build
