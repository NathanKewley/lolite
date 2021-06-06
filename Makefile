.PHONY: rebuild
rebuild:
	pip3 uninstall dist/lolite-0.0.3-py3-none-any.whl -y && python3 -m build && pip3 install dist/lolite-0.0.3-py3-none-any.whl

.PHONY: build
build:
	python3 -m build && pip3 install dist/lolite-0.0.3-py3-none-any.whl

.PHONY: test
test:
	pytest

.PHONY: uploadToPyPi
uploadToPyPi:
	python3 -m twine upload --repository lolite --repository-url https://upload.pypi.org/legacy/ dist/*
