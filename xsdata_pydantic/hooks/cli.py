from xsdata.codegen.writer import CodeWriter

from xsdata_pydantic.generator import PydanticGenerator

CodeWriter.register_generator("pydantic", PydanticGenerator)
