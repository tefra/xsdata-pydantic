from xsdata.codegen.models import Attr, Class
from xsdata.formats.dataclass.filters import Filters
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.models.config import GeneratorConfig
from xsdata.utils.text import stop_words

stop_words.update(["validate"])


class PydanticGenerator(DataclassGenerator):
    """Python pydantic dataclasses code generator."""

    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        """Initialize the pydantic filters."""
        return PydanticFilters(config)


class PydanticFilters(Filters):
    """Pydantic specific template filters."""

    def __init__(self, config: GeneratorConfig):
        """Initialize with kw_only enabled."""
        config.output.format.kw_only = True
        super().__init__(config)
        self.default_class_annotation = None

    def post_meta_hook(self, obj: Class) -> str | None:
        """Inject model_config with deferred build."""
        return "model_config = ConfigDict(defer_build=True)"

    def class_bases(self, obj: Class, class_name: str) -> list[str]:
        """Add BaseModel as a base class for models without extensions."""
        result = super().class_bases(obj, class_name)

        if not obj.extensions:
            result.insert(0, "BaseModel")
        return result

    def field_definition(
        self,
        obj: Class,
        attr: Attr,
        parent_namespace: str | None,
    ) -> str:
        """Return the field definition with any extra metadata."""
        result = super().field_definition(obj, attr, parent_namespace)

        if attr.is_prohibited:
            result = result.replace("init=False", "exclude=True")
        elif attr.fixed:
            result = result.replace("init=False", "const=True")

        return result

    @classmethod
    def build_import_patterns(cls) -> dict[str, dict]:
        """Build import patterns replacing dataclasses with pydantic imports."""
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
