Data Bindings
=============

All the xsdata :ref:`XML <xsdata:XML Binding>` and :ref:`JSON <xsdata:JSON Binding>`
bindings are available. There is an extra requirement to specify the class type of
the data models to the :class:`~xsdata.formats.dataclass.context.XmlContext` that
among other stuff also acts as a compatibility layer between :mod:`python:dataclasses`
and pydantic dataclasses

.. warning::

    The plugin is using xsdata's data bindings to parse json/xml, only xsdata's
    :ref:`types <xsdata:Data Types>` are supported!


Specify ClassType
-----------------

.. code-block:: python
    :emphasize-lines: 7

    >>> from xsdata.formats.dataclass.parsers import XmlParser
    >>> from xsdata.formats.dataclass.parsers import JsonParser
    >>> from xsdata.formats.dataclass.serializers import XmlSerializer
    >>> from xsdata.formats.dataclass.serializers import JsonSerializer
    >>> from xsdata.formats.dataclass.context import XmlContext
    ...
    >>> context = XmlContext(class_type="pydantic")  # Specify class type pydantic
    >>> xml_parser = XmlParser(context=context)
    >>> xml_serializer = XmlSerializer(context=context)
    >>> json_parser = JsonParser(context=context)
    >>> json_serializer = JsonSerializer(context=context)


Binding Shortcuts
-----------------

For convenience this plugin comes with subclasses for all the xsdata binding modules
with the pydantic context auto initialized.

.. code-block:: python

    >>> from xsdata_pydantic.bindings import XmlContext
    >>> from xsdata_pydantic.bindings import XmlParser
    >>> from xsdata_pydantic.bindings import XmlSerializer
    >>> from xsdata_pydantic.bindings import JsonParser
    >>> from xsdata_pydantic.bindings import JsonSerializer
    >>> from xsdata_pydantic.bindings import UserXmlParser
