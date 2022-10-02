.. image:: https://raw.githubusercontent.com/tefra/xsdata-pydantic/master/docs/_static/logo.svg
    :target: https://xsdata-pydantic.readthedocs.io/

xsdata powered by pydantic!
===========================

.. image:: https://github.com/tefra/xsdata/workflows/tests/badge.svg
    :target: https://github.com/tefra/xsdata-pydantic/actions

.. image:: https://readthedocs.org/projects/xsdata-pydantic/badge
    :target: https://xsdata-pydantic.readthedocs.io/

.. image:: https://codecov.io/gh/tefra/xsdata-pydantic/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/tefra/xsdata-pydantic

.. image:: https://img.shields.io/github/languages/top/tefra/xsdata-pydantic.svg
    :target: https://xsdata-pydantic.readthedocs.io/

.. image:: https://www.codefactor.io/repository/github/tefra/xsdata-pydantic/badge
   :target: https://www.codefactor.io/repository/github/tefra/xsdata-pydantic

.. image:: https://img.shields.io/pypi/pyversions/xsdata-pydantic.svg
    :target: https://pypi.org/pypi/xsdata-pydantic/

.. image:: https://img.shields.io/pypi/v/xsdata-pydantic.svg
    :target: https://pypi.org/pypi/xsdata-pydantic/

--------

xsData is a complete data binding library for python allowing developers to access and
use XML and JSON documents as simple objects rather than using DOM.

Now powered by pydantic!


Install
=======

.. code:: console

    $ # Install with cli support
    $ pip install xsdata-pydantic[cli]


Generate Models
===============

.. code:: console

    $ # Generate models
    $ xsdata http://rss.cnn.com/rss/edition.rss --output pydantic
    Parsing document edition.rss
    Analyzer input: 9 main and 0 inner classes
    Analyzer output: 9 main and 0 inner classes
    Generating package: init
    Generating package: generated.rss

.. code-block:: python

    from dataclasses import field
    from pydantic.dataclasses import dataclass

    @dataclass
    class Rss:
        class Meta:
            name = "rss"

        version: Optional[float] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        channel: Optional[Channel] = field(
            default=None,
            metadata={
                "type": "Element",
            }
        )

    ...


XML Parsing
===========

.. code:: python

    >>> from xsdata_pydantic.bindings import XmlParser
    >>> from urllib.request import urlopen
    >>> from generated.rss import Rss
    >>>
    >>> parser = XmlParser()
    >>> with urlopen("http://rss.cnn.com/rss/edition.rss") as rq:
    ...     result = parser.parse(rq, Rss)
    ...
    >>> result.channel.item[2].title
    "'A total lack of discipline': Clarissa Ward visits abandoned Russian foxholes"

    >>> result.channel.item[2].pub_date
    'Fri, 08 Apr 2022 22:56:33 GMT'
    >>> result.channel.item[2].link
    'https://www.cnn.com/videos/world/2022/04/08/ukraine-chernihiv-visit-ward-pkg-tsr-vpx.cnn'


Changelog: 22.10 (2022-10-02)
-----------------------------
- Initial Release
