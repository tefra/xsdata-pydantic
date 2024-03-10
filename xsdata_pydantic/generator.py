from typing import Dict
from typing import List
from typing import Optional

from xsdata.codegen.models import Attr
from xsdata.codegen.models import Class
from xsdata.formats.dataclass.filters import Filters
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.models.config import GeneratorConfig
from xsdata.utils.text import stop_words

stop_words.update(("schema", "validate"))


class PydanticGenerator(DataclassGenerator):
    """Python pydantic dataclasses code generator."""

    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        return PydanticFilters(config)


class PydanticFilters(Filters):
    METADATA_KEY = "json_schema_extra"
    FIXED_KEY = "const"

    def __init__(self, config: GeneratorConfig):
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
        attr: Attr,
        ns_map: Dict,
        parent_namespace: Optional[str],
        parents: List[str],
    ) -> str:
        result = super().field_definition(attr, ns_map, parent_namespace, parents)

        result = result.replace("metadata=", "json_schema_extra=")

        return f"F{result[1:]}"

    @classmethod
    def build_import_patterns(cls) -> Dict[str, Dict]:
        patterns = super().build_import_patterns()
        patterns.update(
            {
                "dataclasses": {"field": [" = field("]},
                "pydantic": {
                    "BaseModel": ["(BaseModel"],
                    "Field": [" Field("],
                    "ConfigDict": ["model_config = ConfigDict("],
                },
            }
        )

        return {key: patterns[key] for key in sorted(patterns)}

    @classmethod
    def filter_metadata(cls, data: Dict) -> Dict:
        data = super().filter_metadata(data)
        data.pop("min_length", None)
        data.pop("max_length", None)
        return data
