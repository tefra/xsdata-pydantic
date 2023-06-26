from xsdata.formats.dataclass.compat import class_types

from xsdata_pydantic.base_model.compat import PydanticBaseModel
from xsdata_pydantic.compat import Pydantic

class_types.register("pydantic", Pydantic())
class_types.register("pydantic-base-model", PydanticBaseModel())
