.PHONY: rebuild
rebuild:
	pip3 uninstall dist/lolite-0.0.1-py3-none-any.whl -y && python3 -m build && pip3 install dist/lolite-0.0.1-py3-none-any.whl

.PHONY: build
build:
	python3 -m build && pip3 install dist/lolite-0.0.1-py3-none-any.whl

.PHONY: test
test:
	pytest
