from typing import Dict
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
        return "model_config = ConfigDict(defer_build=True)"

    def class_bases(self, obj: Class, class_name: str) -> List[str]:
        result = super().class_bases(obj, class_name)

        if not obj.extensions:
            result.insert(0, "BaseModel")
        return result

    def field_definition(
        self,
        obj: Class,
        attr: Attr,
        parent_namespace: Optional[str],
    ) -> str:
        """Return the field definition with any extra metadata."""

        result = super().field_definition(obj, attr, parent_namespace)

        if attr.is_prohibited:
            result = result.replace("init=False", "exclude=True, default=None")
        elif attr.fixed:
            result = result.replace("init=False", "const=True")

        return result

    @classmethod
    def build_import_patterns(cls) -> Dict[str, Dict]:
        patterns = super().build_import_patterns()
        patterns.update(
            {
                "dataclasses": {},
                "xsdata_pydantic.fields": {"field": [" = field("]},
                "pydantic": {
                    "BaseModel": ["(BaseModel"],
                    "Field": [" Field("],
                    "ConfigDict": ["model_config = ConfigDict("],
                },
            }
        )

        return {key: patterns[key] for key in sorted(patterns)}
