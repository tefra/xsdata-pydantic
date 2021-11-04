from typing import Dict

from xsdata.formats.dataclass.filters import Filters
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.models.config import GeneratorConfig


class PydanticGenerator(DataclassGenerator):
    """Python pydantic dataclasses code generator."""

    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        return PydanticFilters(config)


class PydanticFilters(Filters):
    @classmethod
    def build_import_patterns(cls) -> Dict[str, Dict]:
        patterns = super().build_import_patterns()
        patterns.update(
            {
                "dataclasses": {"field": [" = field("]},
                "pydantic.dataclasses": {"dataclass": ["@dataclass"]},
            }
        )

        return {key: patterns[key] for key in sorted(patterns)}
