import os
from pathlib import Path
from unittest import mock

from click.testing import CliRunner
from xsdata.cli import cli
from xsdata.models.config import GeneratorConfig
from xsdata.utils.testing import ClassFactory
from xsdata.utils.testing import FactoryTestCase

from xsdata_pydantic.generator import PydanticGenerator


class PydanticGeneratorTests(FactoryTestCase):
    def setUp(self):
        super().setUp()
        config = GeneratorConfig()
        self.generator = PydanticGenerator(config)

    @mock.patch.object(PydanticGenerator, "validate_imports")
    def test_render(self, mock_validate_imports):
        classes = [
            ClassFactory.elements(2, package="foo"),
            ClassFactory.elements(3, package="foo"),
        ]

        classes[0].attrs[0].restrictions.max_occurs = 3

        iterator = self.generator.render(classes)

        actual = [(out.path, out.title, out.source) for out in iterator]

        expected = (
            "from typing import List\n"
            "\n"
            "from pydantic import BaseModel, ConfigDict\n"
            "\n"
            "from xsdata_pydantic.fields import field\n"
            "\n"
            '__NAMESPACE__ = "xsdata"\n'
            "\n"
            "\n"
            "class ClassB(BaseModel):\n"
            "    class Meta:\n"
            '        name = "class_B"\n'
            "\n"
            "    model_config = ConfigDict(defer_build=True)\n"
            "    attr_b: List[str] = field(\n"
            "        default_factory=list,\n"
            "        metadata={\n"
            '            "name": "attr_B",\n'
            '            "type": "Element",\n'
            '            "max_occurs": 3,\n'
            "        },\n"
            "    )\n"
            "    attr_c: str = field(\n"
            "        metadata={\n"
            '            "name": "attr_C",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )\n"
            "\n"
            "\n"
            "class ClassC(BaseModel):\n"
            "    class Meta:\n"
            '        name = "class_C"\n'
            "\n"
            "    model_config = ConfigDict(defer_build=True)\n"
            "    attr_d: str = field(\n"
            "        metadata={\n"
            '            "name": "attr_D",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )\n"
            "    attr_e: str = field(\n"
            "        metadata={\n"
            '            "name": "attr_E",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )\n"
            "    attr_f: str = field(\n"
            "        metadata={\n"
            '            "name": "attr_F",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )\n"
        )

        self.assertEqual(2, len(actual))
        self.assertEqual(3, len(actual[1]))

        self.assertEqual("foo.tests", actual[1][1])
        self.assertEqual(expected, actual[1][2])

        mock_validate_imports.assert_called_once_with()

    def test_complete(self):
        runner = CliRunner()
        schema = Path(__file__).parent.joinpath("fixtures/schemas/po.xsd")
        os.chdir(Path(__file__).parent.parent)

        result = runner.invoke(
            cli,
            [
                str(schema),
                "--package",
                "tests.fixtures.po.models",
                "--structure-style=single-package",
                "--output",
                "pydantic",
                "--config",
                "tests/fixtures/pydantic.conf.xml",
            ],
            catch_exceptions=True,
        )

        self.assertIsNone(result.exception)
