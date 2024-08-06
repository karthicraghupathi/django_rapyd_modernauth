build:
	rm -rf dist
	python -m build
	make lint

patch:
	bump2version patch

minor:
	bump2version minor

major:
	bump2version major

testupload:
	twine upload -r testpypi --verbose dist/*

upload:
	twine upload -r pypi --verbose dist/*

tests:
	tox

lint:
	twine check dist/*

.PHONY: build patch minor major testupload upload tests lint
