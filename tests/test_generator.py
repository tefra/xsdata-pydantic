import os
from pathlib import Path

from click.testing import CliRunner
from xsdata.cli import cli
from xsdata.models.config import GeneratorConfig
from xsdata.utils.testing import FactoryTestCase

from xsdata_pydantic.generator import PydanticGenerator


class PydanticGeneratorTests(FactoryTestCase):
    def setUp(self):
        super().setUp()
        config = GeneratorConfig()
        self.generator = PydanticGenerator(config)

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
