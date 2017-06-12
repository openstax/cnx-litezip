# -*- coding: utf-8 -*-
import pathlib

import versioneer
from setuptools import setup, find_packages


here = pathlib.Path('.')


def read_from_requirements_txt(filepath):
    f = here / filepath
    with f.open() as fb:
        return tuple([x.strip() for x in fb if not x.strip().startswith('#')])


install_requires = read_from_requirements_txt('requirements/main.txt')
tests_require = read_from_requirements_txt('requirements/test.txt')
extras_require = {
    'test': tests_require,
    }
description = "Connexions LiteZip Library"
with open('README.rst', 'r') as readme:
    long_description = readme.read()


setup(
    name='cnx-litezip',
    version=versioneer.get_version(),
    author='Connexions team',
    author_email='info@cnx.org',
    url="https://github.com/connexions/cnx-litezip",
    license='LGPL, See also LICENSE.txt',
    description=description,
    long_description=long_description,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    packages=find_packages(),
    include_package_data=True,
    cmdclass=versioneer.get_cmdclass(),
    entry_points="""\
    [console_scripts]
    completezip2litezip = litezip.cli.completezip2litezip:main
    validate-litezip = litezip.cli.validate:main
    """,
    )
