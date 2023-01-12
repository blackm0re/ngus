package: COPYING src/ngus/__init__.py src/ngus/__main__.py LICENSE README.md setup.py pyproject.toml setup.cfg
	python -m build

upload: dist/*
	python -m twine upload dist/*

upload-test: dist/*
	python -m twine upload --repository testpypi dist/* 

clean:
	rm -rf dist src/ngus/__pycache__ src/ngus.egg-info
