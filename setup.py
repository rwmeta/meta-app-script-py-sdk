#!/usr/bin/env python
import setuptools
from os import path

from metaappscriptsdk import info

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

packages = [
    'metaappscriptsdk',
    'metaappscriptsdk.logger',
]

setup_requires = [
    'starter_api',
    'elasticsearch',
    'jsonklog',
    'fluent-logger'
]

setuptools.setup(
    name=info.__package_name__,
    version=info.__version__,

    description='Meta App Scripts SDK',
    long_description=long_description,

    url='https://github.com/rw-meta/meta-app-script-py-sdk',

    author='Artur Geraschenko',
    author_email='arturgspb@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    setup_requires=setup_requires,
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'metaappscriptsdk': 'metaappscriptsdk'},
    include_package_data=True,
)
