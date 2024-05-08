[![image](https://github.com/tefra/xsdata-pydantic/raw/main/docs/logo.svg)](https://xsdata-pydantic.readthedocs.io/)

# xsdata powered by pydantic!

[![image](https://github.com/tefra/xsdata-pydantic/workflows/tests/badge.svg)](https://github.com/tefra/xsdata-pydantic/actions)
[![image](https://readthedocs.org/projects/xsdata-pydantic/badge)](https://xsdata-pydantic.readthedocs.io/)
[![image](https://codecov.io/gh/tefra/xsdata-pydantic/branch/main/graph/badge.svg)](https://codecov.io/gh/tefra/xsdata-pydantic)
[![image](https://img.shields.io/github/languages/top/tefra/xsdata-pydantic.svg)](https://xsdata-pydantic.readthedocs.io/)
[![image](https://www.codefactor.io/repository/github/tefra/xsdata-pydantic/badge)](https://www.codefactor.io/repository/github/tefra/xsdata-pydantic)
[![image](https://img.shields.io/pypi/pyversions/xsdata-pydantic.svg)](https://pypi.org/pypi/xsdata-pydantic/)
[![image](https://img.shields.io/pypi/v/xsdata-pydantic.svg)](https://pypi.org/pypi/xsdata-pydantic/)

---

xsData is a complete data binding library for python allowing developers to access and
use XML and JSON documents as simple objects rather than using DOM.

Now powered by pydantic!

```console
$ xsdata http://rss.cnn.com/rss/edition.rss --output pydantic
Parsing document edition.rss
Analyzer input: 9 main and 0 inner classes
Analyzer output: 9 main and 0 inner classes
Generating package: init
Generating package: generated.rss
```

```python
class Rss(BaseModel):
    class Meta:
        name = "rss"

    model_config = ConfigDict(defer_build=True)
    version: float = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    channel: Channel = field(
        metadata={
            "type": "Element",
            "required": True,
        }
    )
```

```console

>>> from xsdata_pydantic.bindings import XmlParser
>>> from urllib.request import urlopen
>>> from generated.rss import Rss
>>>
>>> parser = XmlParser()
>>> with urlopen("http://rss.cnn.com/rss/edition.rss") as rq:
...     result = parser.parse(rq, Rss)
...
>>> result.channel.item[2].title
'Vatican indicts 10 people, including a Cardinal, over an international financial scandal'
>>> result.channel.item[2].pub_date
'Sat, 03 Jul 2021 16:37:14 GMT'
>>> result.channel.item[2].link
'https://www.cnn.com/2021/07/03/europe/vatican-financial-scandal-intl/index.html'

```

## Changelog: 24.5 (2024-05-08)

- Support pydantic v2 models
- Add missing parser/serializer shortcuts
- General project maintenance
