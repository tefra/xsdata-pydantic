from datetime import datetime
from unittest import TestCase

from tests.fixtures.common import TypeC

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
        serializer.config.indent = "  "
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
