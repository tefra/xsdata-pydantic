from xsdata.formats.dataclass.compat import class_types

from xsdata_pydantic.compat import Pydantic

class_types.register("pydantic", Pydantic())
