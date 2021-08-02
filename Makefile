package: COPYING ngus/__init__.py ngus/__main__.py LICENSE README.md setup.py
	python setup.py sdist bdist_wheel

upload: dist/*
	python -m twine upload dist/*

upload-test: dist/*
	python -m twine upload --repository testpypi dist/* 

clean:
	rm -rf build dist ngus/__pycache__ ngus.egg-info
