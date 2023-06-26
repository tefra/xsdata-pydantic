from xsdata.codegen.writer import CodeWriter

from xsdata_pydantic.base_model.generator import PydanticBaseGenerator
from xsdata_pydantic.generator import PydanticGenerator

CodeWriter.register_generator("pydantic", PydanticGenerator)
CodeWriter.register_generator("pydantic-base-model", PydanticBaseGenerator)
