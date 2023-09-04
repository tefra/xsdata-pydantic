from datetime import datetime

import pytest

from xsdata.formats.dataclass.serializers.config import SerializerConfig

from tests.fixtures.common import TypeC, BTypeC
from xsdata_pydantic.bindings import JsonParser
from xsdata_pydantic.bindings import JsonSerializer
from xsdata_pydantic.bindings import XmlParser
from xsdata_pydantic.bindings import XmlSerializer
from xsdata_pydantic.compat import AnyElement
from xsdata_pydantic.compat import DerivedElement
from xsdata_pydantic.base_model.compat import AnyElement as BAnyElement
from xsdata_pydantic.base_model.compat import DerivedElement as BDerivedElement

from xsdata_pydantic.base_model.bindings import JsonParser as BJsonParser
from xsdata_pydantic.base_model.bindings import JsonSerializer as BJsonSerializer
from xsdata_pydantic.base_model.bindings import XmlParser as BXmlParser
from xsdata_pydantic.base_model.bindings import XmlSerializer as BXmlSerializer


TYPE_C = TypeC(
    one="first",
    two=1.1,
    four=[
        datetime(2002, 1, 1, 12, 1),
        datetime(2003, 2, 5, 13, 5),
    ],
    any=AnyElement(
        children=[
            AnyElement(qname="foo", text="bar"),
            DerivedElement(qname="bar", value="1"),
            DerivedElement(qname="bar", value=2),
        ]
    ),
)

BTYPE_C = BTypeC(
    one="first",
    two=1.1,
    four=[
        datetime(2002, 1, 1, 12, 1),
        datetime(2003, 2, 5, 13, 5),
    ],
    any=BAnyElement(
        children=[
            BAnyElement(qname="foo", text="bar"),
            BDerivedElement(qname="bar", value="1"),
            BDerivedElement(qname="bar", value=2),
        ]
    ),
)


@pytest.mark.parametrize(
    "type_c, Serializer,Parser",
    [(TYPE_C, XmlSerializer, XmlParser), (BTYPE_C, BXmlSerializer, BXmlParser)],
)
def test_xml_bindings(type_c, Serializer, Parser):
    serializer = Serializer()
    serializer.config.pretty_print = True
    serializer.config.xml_declaration = False
    parser = Parser()
    ns_map = {
        "xs": "http://www.w3.org/2001/XMLSchema",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }

    type_name = type_c.__class__.__name__
    expected = (
        f'<{type_name} xmlns:xs="http://www.w3.org/2001/XMLSchema" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
        "  <one>first</one>\n"
        "  <two>1.1</two>\n"
        "  <three>true</three>\n"
        "  <four>01 January 2002 12:01</four>\n"
        "  <four>05 February 2003 13:05</four>\n"
        "  <foo>bar</foo>\n"
        '  <bar xsi:type="xs:string">1</bar>\n'
        '  <bar xsi:type="xs:short">2</bar>\n'
        f"</{type_name}>\n"
    )
    assert expected == serializer.render(type_c, ns_map)
    assert type_c == parser.from_string(expected)


@pytest.mark.parametrize(
    "type_c, Serializer,Parser",
    [(TYPE_C, JsonSerializer, JsonParser), (BTYPE_C, BJsonSerializer, BJsonParser)],
)
def test_serialize_json(type_c, Serializer,Parser):
    serializer = Serializer(config=SerializerConfig(pretty_print=True))
    parser = Parser()

    expected = (
        "{\n"
        '  "one": "first",\n'
        '  "two": 1.1,\n'
        '  "three": true,\n'
        '  "four": [\n'
        '    "01 January 2002 12:01",\n'
        '    "05 February 2003 13:05"\n'
        "  ],\n"
        '  "any": {\n'
        '    "qname": null,\n'
        '    "text": null,\n'
        '    "tail": null,\n'
        '    "children": [\n'
        "      {\n"
        '        "qname": "foo",\n'
        '        "text": "bar",\n'
        '        "tail": null,\n'
        '        "children": [],\n'
        '        "attributes": {}\n'
        "      },\n"
        "      {\n"
        '        "qname": "bar",\n'
        '        "value": "1",\n'
        '        "type": null\n'
        "      },\n"
        "      {\n"
        '        "qname": "bar",\n'
        '        "value": 2,\n'
        '        "type": null\n'
        "      }\n"
        "    ],\n"
        '    "attributes": {}\n'
        "  }\n"
        "}"
    )
    assert expected == serializer.render(type_c)
    assert type_c == parser.from_string(expected, type(type_c))
