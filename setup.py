#!/usr/bin/env python
from os import path

import setuptools
from pip.req import parse_requirements

from metaappscriptsdk import info

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

packages = [
    'metaappscriptsdk',
    'metaappscriptsdk.logger',
    'metaappscriptsdk.services',
    'metaappscriptsdk.starter',
]

install_reqs = parse_requirements(path.join(here, 'requirements.txt'), session=False)

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

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
        'Programming Language :: Python :: 3'
    ],
    install_requires=reqs,
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'metaappscriptsdk': 'metaappscriptsdk'},
    include_package_data=True,
)
