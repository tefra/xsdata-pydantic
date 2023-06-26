from typing import Any, Dict, List

from xsdata.codegen.models import Attr, Class
from xsdata.formats.dataclass.filters import Filters
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.models.config import ExtensionType, GeneratorConfig, OutputFormat
from xsdata.utils.text import stop_words
import collections

stop_words.update(("schema", "validate"))


class PydanticBaseGenerator(DataclassGenerator):
    """Python pydantic dataclasses code generator."""

    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        return PydanticBaseFilters(config)


class PydanticBaseFilters(Filters):
    @classmethod
    def build_import_patterns(cls) -> Dict[str, Dict]:
        patterns = Filters.build_import_patterns()
        patterns.update(
            {"pydantic": {"Field": [" = Field("], "BaseModel": ["BaseModel"]}}
        )
        return {key: patterns[key] for key in sorted(patterns)}

    @classmethod
    def filter_metadata(cls, data: Dict) -> Dict:
        data = super().filter_metadata(data)
        data.pop("min_length", None)
        data.pop("max_length", None)
        return data

    @classmethod
    def build_class_annotation(cls, fmt: OutputFormat) -> str:
        # remove the @dataclass decorator
        return ""

    def field_definition(
        self,
        attr: Attr,
        ns_map: dict,
        parent_namespace: str | None,
        parents: list[str],
    ) -> str:
        """Return the field definition with any extra metadata."""
        # updated to use pydantic Field
        default_value = self.field_default_value(attr, ns_map)
        metadata = self.field_metadata(attr, parent_namespace, parents)

        kwargs: dict[str, Any] = {}
        if attr.fixed or attr.is_prohibited:
            kwargs["init"] = False

        if default_value is not False and not attr.is_prohibited:
            key = self.FACTORY_KEY if attr.is_factory else self.DEFAULT_KEY
            kwargs[key] = default_value

        if metadata:
            kwargs["metadata"] = metadata

        return f"Field({self.format_arguments(kwargs, 4)})"

    def class_bases(self, obj: Class, class_name: str) -> List[str]:
        # FIXME ... need to dedupe superclasses
        return super().class_bases(obj, class_name) + ["BaseModel"]
