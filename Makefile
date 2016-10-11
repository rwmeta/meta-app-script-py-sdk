VERSION=$(shell python metaappscriptsdk/info.py)

init:
	pip3 install -r requirements.txt

publish:
	echo $(VERSION)

	python3 setup.py register
	python3 setup.py sdist upload
	python3 setup.py bdist_wheel --universal upload

	$(shell git tag $(VERSION))
	$(shell git push origin $(VERSION))

	rm -fr build dist .egg requests.egg-info