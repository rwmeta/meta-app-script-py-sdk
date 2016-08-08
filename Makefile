VERSION=$(shell python metaappscriptsdk/info.py)

init:
	pip install -r requirements.txt

publish:
	echo $(VERSION)

	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel --universal upload

	$(shell git tag $(VERSION))
	$(shell git push origin $(VERSION))

	rm -fr build dist .egg requests.egg-info