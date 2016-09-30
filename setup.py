#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""It's the ``setup.py``; you know the drill."""
import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    """Read the contents of a file and return them."""
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='cwmon',
    version='0.1.6',
    license='BSD',
    description='CloudWatch-based monitoring for your servers.',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Hank Gay',
    author_email='hank@rescuetime.com',
    url='https://github.com/RescueTime/cwmon',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Monitoring',
    ],
    keywords=[
        'monitoring', 'AWS', 'CloudWatch',
    ],
    install_requires=[
        'click',
        'boto3',
        'psutil',
        'click-plugins',
        'colorama',
    ],
    extras_require={
        'dev': [
            'tox',
            'wheel',
            'bumpversion',
            'gitchangelog',
            'twine',
        ],
    },
    entry_points={
        'console_scripts': [
            'cwmon = cwmon.cli:cwmon',
        ]
    },
)
