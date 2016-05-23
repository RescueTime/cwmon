========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/cwmon/badge/?style=flat
    :target: https://readthedocs.org/projects/cwmon
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/RescueTime/cwmon.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/RescueTime/cwmon

.. |coveralls| image:: https://coveralls.io/repos/RescueTime/cwmon/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/RescueTime/cwmon

.. |version| image:: https://img.shields.io/pypi/v/cwmon.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/cwmon

.. |downloads| image:: https://img.shields.io/pypi/dm/cwmon.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/cwmon

.. |wheel| image:: https://img.shields.io/pypi/wheel/cwmon.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/cwmon

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/cwmon.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/cwmon

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/cwmon.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/cwmon


.. end-badges

CloudWatch-based monitoring for your servers.

* Free software: BSD license

Installation
============

::

    pip install cwmon

Documentation
=============

https://cwmon.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
