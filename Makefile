build:
	python -m build
	make lint

patch:
	bump2version patch

minor:
	bump2version minor

major:
	bump2version major

upload:
	python -m twine upload --verbose dist/*

tests:
	tox

lint:
	python -m twine check dist/*

.PHONY: build patch minor major upload tests lint
