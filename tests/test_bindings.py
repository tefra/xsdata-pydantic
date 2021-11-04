from datetime import datetime
from unittest import TestCase

from xsdata.formats.dataclass.serializers.config import SerializerConfig

from tests.fixtures.common import TypeC
from xsdata_pydantic.bindings import JsonParser
from xsdata_pydantic.bindings import JsonSerializer
from xsdata_pydantic.bindings import XmlParser
from xsdata_pydantic.bindings import XmlSerializer
from xsdata_pydantic.compat import AnyElement
from xsdata_pydantic.compat import DerivedElement


class BindingsTests(TestCase):
    def setUp(self):
        self.obj = TypeC(
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

    def test_xml_bindings(self):
        serializer = XmlSerializer()
        serializer.config.pretty_print = True
        serializer.config.xml_declaration = False
        parser = XmlParser()
        ns_map = {
            "xs": "http://www.w3.org/2001/XMLSchema",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }

        expected = (
            '<TypeC xmlns:xs="http://www.w3.org/2001/XMLSchema" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
            "  <one>first</one>\n"
            "  <two>1.1</two>\n"
            "  <three>true</three>\n"
            "  <four>01 January 2002 12:01</four>\n"
            "  <four>05 February 2003 13:05</four>\n"
            "  <foo>bar</foo>\n"
            '  <bar xsi:type="xs:string">1</bar>\n'
            '  <bar xsi:type="xs:short">2</bar>\n'
            "</TypeC>\n"
        )
        self.assertEqual(expected, serializer.render(self.obj, ns_map))
        self.assertEqual(self.obj, parser.from_string(expected))

    def test_serialize_json(self):
        serializer = JsonSerializer(config=SerializerConfig(pretty_print=True))
        parser = JsonParser()

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
        self.assertEqual(expected, serializer.render(self.obj))
        self.assertEqual(self.obj, parser.from_string(expected, TypeC))
