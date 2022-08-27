build:
	python -m build

patch:
	bump2version patch

minor:
	bump2version minor

major:
	bump2version major

upload:
	python -m twine upload --verbose dist/*

.PHONY: build patch minor major upload
