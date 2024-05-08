# Data Bindings

All the xsdata
[data bindings](https://xsdata.readthedocs.io/en/latest/data_binding/basics/) are
available. There is an extra requirement to specify the class type of the data models to
the [XmlContext][xsdata.formats.dataclass.context.XmlContext] that among other stuff
also acts as a compatibility layer between dataclasses and pydantic models.

## Specify ClassType

```python
>>> from xsdata.formats.dataclass.parsers import XmlParser
>>> from xsdata.formats.dataclass.parsers import JsonParser
>>> from xsdata.formats.dataclass.serializers import XmlSerializer
>>> from xsdata.formats.dataclass.serializers import JsonSerializer
>>> from xsdata.formats.dataclass.context import XmlContext
...
>>> context = XmlContext(class_type="pydantic")  # Specify class type attrs
>>> xml_parser = XmlParser(context=context)
>>> xml_serializer = XmlSerializer(context=context)
>>> json_parser = JsonParser(context=context)
>>> json_serializer = JsonSerializer(context=context)
```

## Binding Shortcuts

For convenience this plugin comes with subclasses for all the xsdata binding modules
with the attrs context auto initialized.

```python
>>> from xsdata_pydantic.bindings import XmlContext
>>> from xsdata_pydantic.bindings import XmlParser
>>> from xsdata_pydantic.bindings import XmlSerializer
>>> from xsdata_pydantic.bindings import JsonParser
>>> from xsdata_pydantic.bindings import JsonSerializer
>>> from xsdata_pydantic.bindings import UserXmlParser
>>> from xsdata_pydantic.bindings import TreeParser
>>> from xsdata_pydantic.bindings import PycodeSerializer
>>> from xsdata_pydantic.bindings import DictDecoder
>>> from xsdata_pydantic.bindings import DictEncoder
```
