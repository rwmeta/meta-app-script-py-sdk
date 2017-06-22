VERSION=$(shell python metaappscriptsdk/info.py)

init:
	pip3 install -r requirements.txt

publish:
	echo $(VERSION)

	python3 setup.py sdist bdist_wheel
	twine upload dist/*

	$(shell git tag $(VERSION))
	$(shell git push origin $(VERSION))

	rm -fr build dist .egg requests.egg-info