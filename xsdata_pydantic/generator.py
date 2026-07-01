from typing import List
from typing import Optional

from xsdata.codegen.models import Class, Attr
from xsdata.formats.dataclass.filters import Filters
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.models.config import GeneratorConfig
from xsdata.utils.text import stop_words

stop_words.update(["validate"])


class PydanticGenerator(DataclassGenerator):
    """Python pydantic dataclasses code generator."""

    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        return PydanticFilters(config)


class PydanticFilters(Filters):
    def __init__(self, config: GeneratorConfig):
        config.output.format.kw_only = True
        super().__init__(config)
        self.default_class_annotation = None

    def post_meta_hook(self, obj: Class) -> Optional[str]:
        return

    def class_bases(self, obj: Class, class_name: str) -> List[str]:
        result = super().class_bases(obj, class_name)

        if not obj.extensions:
            result.insert(0, "BaseXmlModel")
            result.append(f'tag="{obj.name}"')
        return result

    def field_definition(
        self,
        obj: Class,
        attr: Attr,
        parent_namespace: Optional[str],
    ) -> str:
        """Return the field definition with any extra metadata."""

        ns_map = obj.ns_map
        default_value = self.field_default_value(attr, ns_map)

        kwargs = {}
        if (
            parent_namespace != attr.namespace
            or attr.is_attribute
            and attr.namespace is not None
        ):
            kwargs["ns"] = attr.namespace
        if default_value is not False and not attr.is_prohibited:
            kwargs["default_factory" if attr.is_factory else "default"] = default_value

        if attr.is_element:
            kwargs["tag"] = attr.local_name
            return f"element({self.format_arguments(kwargs, 4)})"

        kwargs["name"] = attr.local_name
        return f"attr({self.format_arguments(kwargs, 4)})"

    @classmethod
    def build_import_patterns(cls) -> dict[str, dict]:
        patterns = super().build_import_patterns()
        patterns.update(
            {
                "dataclasses": {},
                "pydantic_xml": {
                    "BaseXmlModel": ["(BaseXmlModel"],
                    "attr": [" = attr("],
                    "element": [" = element("],
                },
            }
        )

        return {key: patterns[key] for key in sorted(patterns)}
